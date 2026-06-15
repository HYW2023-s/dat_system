"""Vector cache service - stores API embeddings to avoid redundant calls."""

import io
import logging
from datetime import datetime

import numpy as np
from sqlalchemy import select, Column, Integer, String, DateTime, LargeBinary, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import Base, async_session

logger = logging.getLogger(__name__)


class EmbeddingCache(Base):
    """Cache table for embedding vectors."""
    __tablename__ = "embedding_cache"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(64), nullable=False, index=True)
    dimension = Column(Integer, nullable=False)
    word = Column(String(128), nullable=False)
    vector = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    __table_args__ = (
        UniqueConstraint("model_name", "word", name="uq_model_word"),
    )


def _serialize_vector(vec: np.ndarray) -> bytes:
    """Serialize a numpy array to bytes."""
    buf = io.BytesIO()
    np.save(buf, vec, allow_pickle=False)
    return buf.getvalue()


def _deserialize_vector(data: bytes) -> np.ndarray:
    """Deserialize bytes back to numpy array."""
    buf = io.BytesIO(data)
    return np.load(buf, allow_pickle=False)


async def get_cached_vector(
    model_name: str,
    word: str,
) -> np.ndarray | None:
    """Look up a cached vector. Returns None if not found."""
    async with async_session() as session:
        result = await session.execute(
            select(EmbeddingCache).where(
                EmbeddingCache.model_name == model_name,
                EmbeddingCache.word == word,
            )
        )
        cache_entry = result.scalar_one_or_none()

        if cache_entry:
            return _deserialize_vector(cache_entry.vector)
        return None


async def set_cached_vector(
    model_name: str,
    dimension: int,
    word: str,
    vector: np.ndarray,
) -> None:
    """Store a vector in the cache."""
    async with async_session() as session:
        # Check if already exists
        result = await session.execute(
            select(EmbeddingCache).where(
                EmbeddingCache.model_name == model_name,
                EmbeddingCache.word == word,
            )
        )
        existing = result.scalar_one_or_none()

        if existing:
            existing.vector = _serialize_vector(vector)
            existing.created_at = datetime.now()
        else:
            entry = EmbeddingCache(
                model_name=model_name,
                dimension=dimension,
                word=word,
                vector=_serialize_vector(vector),
            )
            session.add(entry)

        await session.commit()


async def get_cached_vectors(
    provider,
    words: list[str],
) -> dict[str, np.ndarray | None]:
    """
    Get vectors for multiple words, using cache first, API as fallback.

    Args:
        provider: An EmbeddingProvider instance
        words: list of words to get vectors for

    Returns:
        dict mapping word -> vector (or None if unavailable)
    """
    model_name = provider.model_name
    results = {}
    words_to_fetch = []

    # Step 1: Check cache for all words
    for word in words:
        cached = await get_cached_vector(model_name, word)
        if cached is not None:
            results[word] = cached
        else:
            words_to_fetch.append(word)

    # Step 2: Fetch missing words via API (batch)
    if words_to_fetch:
        logger.info(
            f"Cache miss for {len(words_to_fetch)}/{len(words)} words "
            f"in model '{model_name}'. Fetching via API..."
        )
        fetched = await provider.get_vectors(words_to_fetch)

        for word, vector in fetched.items():
            if vector is not None:
                # Store in cache
                await set_cached_vector(model_name, provider.dimension, word, vector)
                results[word] = vector
            else:
                results[word] = None

    return results


async def clear_cache(model_name: str = None) -> int:
    """Clear embedding cache. If model_name is None, clear all."""
    async with async_session() as session:
        from sqlalchemy import delete

        if model_name:
            stmt = delete(EmbeddingCache).where(
                EmbeddingCache.model_name == model_name
            )
        else:
            stmt = delete(EmbeddingCache)

        result = await session.execute(stmt)
        await session.commit()
        count = result.rowcount
        logger.info(f"Cleared {count} cached vectors" + (f" for {model_name}" if model_name else ""))
        return count


async def get_cache_stats() -> dict:
    """Get cache statistics."""
    async with async_session() as session:
        from sqlalchemy import func

        result = await session.execute(
            select(
                EmbeddingCache.model_name,
                func.count(EmbeddingCache.id).label("count"),
            ).group_by(EmbeddingCache.model_name)
        )
        stats = {}
        for row in result:
            stats[row.model_name] = row.count
        return stats
