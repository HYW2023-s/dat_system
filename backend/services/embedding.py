"""Embedding service - multi-model support with caching."""

import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import numpy as np
from gensim.models import KeyedVectors

from backend.config import WORD2VEC_MODEL_PATH

logger = logging.getLogger(__name__)

# Global registry
_providers: dict[str, "EmbeddingProvider"] = {}
_active_provider: Optional["EmbeddingProvider"] = None


class EmbeddingProvider(ABC):
    """Abstract base class for embedding model providers."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Unique model identifier."""
        ...

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Vector dimension."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description."""
        ...

    @property
    def is_local(self) -> bool:
        """Whether this model runs locally (no API call needed)."""
        return True

    @abstractmethod
    async def get_vector(self, word: str) -> Optional[np.ndarray]:
        """Get embedding vector for a single word. Returns None if not found."""
        ...

    async def get_vectors(self, words: list[str]) -> dict[str, Optional[np.ndarray]]:
        """Get embeddings for multiple words. Uses batch API if available."""
        results = {}
        for word in words:
            results[word] = await self.get_vector(word)
        return results

    def word_exists(self, word: str) -> bool:
        """Check if word is available in this model. Default sync check."""
        return True


class Word2VecProvider(EmbeddingProvider):
    """Local Tencent Word2Vec model (200-dim)."""

    def __init__(self):
        self._model = None
        self._load()

    def _load(self):
        model_path = Path(WORD2VEC_MODEL_PATH)
        if not model_path.exists():
            logger.warning(f"Word2Vec model not found at {model_path}")
            return
        logger.info(f"Loading Word2Vec model from {model_path}...")
        self._model = KeyedVectors.load(str(model_path))
        logger.info(f"Word2Vec loaded. Vocabulary: {len(self._model.key_to_index)} words")

    @property
    def model_name(self) -> str:
        return "word2vec"

    @property
    def dimension(self) -> int:
        return 200

    @property
    def description(self) -> str:
        return "Tencent Word2Vec (200维) - 本地运行，无需 API Key"

    @property
    def is_local(self) -> bool:
        return True

    async def get_vector(self, word: str) -> Optional[np.ndarray]:
        if self._model is None:
            return None
        try:
            return self._model[word]
        except KeyError:
            return None

    def word_exists(self, word: str) -> bool:
        if self._model is None:
            return False
        return word in self._model

    @property
    def model(self):
        return self._model


class AliQwenProvider(EmbeddingProvider):
    """Aliyun Bailian text-embedding-v4 (1024-dim) via API."""

    BASE_URL = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"

    def __init__(self, api_key: str = ""):
        self._api_key = api_key

    @property
    def model_name(self) -> str:
        return "ali-qwen-v4"

    @property
    def dimension(self) -> int:
        return 1024

    @property
    def description(self) -> str:
        return "阿里百炼 text-embedding-v4 (1024维) - 需要提供 API Key"

    @property
    def is_local(self) -> bool:
        return False

    def set_api_key(self, key: str):
        self._api_key = key

    async def get_vector(self, word: str) -> Optional[np.ndarray]:
        if not self._api_key or not word:
            return None

        import httpx
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "text-embedding-v4",
            "input": {"texts": [word]},
            "parameters": {"text_type": "query"},
        }

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(self.BASE_URL, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    embeds = data.get("output", {}).get("embeddings", [])
                    if embeds:
                        return np.array(embeds[0]["embedding"], dtype=np.float32)
                else:
                    logger.warning(f"AliQwen API error {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            logger.error(f"AliQwen API request failed: {e}")

        return None

    async def get_vectors(self, words: list[str]) -> dict[str, Optional[np.ndarray]]:
        """Batch fetch embeddings - up to 25 texts per request."""
        valid_words = [w for w in words if w]
        if not valid_words or not self._api_key:
            return {w: None for w in words}

        # Batch: process in chunks of 25
        results = {}
        chunk_size = 25

        import httpx
        async with httpx.AsyncClient(timeout=60) as client:
            for i in range(0, len(valid_words), chunk_size):
                chunk = valid_words[i:i + chunk_size]
                headers = {
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                }
                payload = {
                    "model": "text-embedding-v4",
                    "input": {"texts": chunk},
                    "parameters": {"text_type": "query"},
                }

                try:
                    resp = await client.post(self.BASE_URL, json=payload, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        embeds = data.get("output", {}).get("embeddings", [])
                        for j, emb in enumerate(embeds):
                            if j < len(chunk):
                                results[chunk[j]] = np.array(emb["embedding"], dtype=np.float32)
                    else:
                        logger.warning(f"AliQwen batch API error: {resp.status_code}")
                        for w in chunk:
                            results[w] = None
                except Exception as e:
                    logger.error(f"AliQwen batch request failed: {e}")
                    for w in chunk:
                        results[w] = None

        # Fill in empty words
        for w in words:
            if w not in results:
                results[w] = None

        return results


def register_provider(provider: EmbeddingProvider):
    """Register an embedding provider."""
    _providers[provider.model_name] = provider
    logger.info(f"Registered embedding provider: {provider.model_name}")


def get_provider(name: str) -> Optional[EmbeddingProvider]:
    """Get a registered provider by name."""
    return _providers.get(name)


def get_active_provider() -> Optional[EmbeddingProvider]:
    """Get the currently active embedding provider."""
    global _active_provider
    return _active_provider


def set_active_provider(name: str) -> bool:
    """Switch the active embedding provider."""
    global _active_provider
    provider = _providers.get(name)
    if provider:
        _active_provider = provider
        logger.info(f"Switched to embedding provider: {name}")
        return True
    return False


def list_providers() -> list[dict]:
    """List all registered providers with metadata."""
    global _active_provider
    return [
        {
            "name": p.model_name,
            "description": p.description,
            "dimension": p.dimension,
            "is_local": p.is_local,
            "is_active": _active_provider is not None and _active_provider.model_name == p.model_name,
        }
        for p in _providers.values()
    ]


def load_model_on_startup():
    """Initialize all providers on application startup."""
    # Register Word2Vec (always available if model file exists)
    w2v = Word2VecProvider()
    register_provider(w2v)

    # Set Word2Vec as default
    global _active_provider
    _active_provider = w2v

    # AliQwen will be registered later when API key is provided
    # OpenAI etc. can be added similarly


# Legacy compatibility
def get_model():
    """Legacy: get the Word2Vec model directly."""
    provider = get_provider("word2vec")
    if isinstance(provider, Word2VecProvider):
        return provider.model
    return None


def get_word_vector(word: str) -> Optional[np.ndarray]:
    """Legacy: get word vector from Word2Vec model."""
    provider = get_provider("word2vec")
    if isinstance(provider, Word2VecProvider):
        try:
            return provider.model[word]
        except KeyError:
            return None
    return None


def word_in_vocabulary(word: str) -> bool:
    """Legacy: check if word exists in Word2Vec."""
    provider = get_provider("word2vec")
    if isinstance(provider, Word2VecProvider):
        return provider.word_exists(word)
    return False
