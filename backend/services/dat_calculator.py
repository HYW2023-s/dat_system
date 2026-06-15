"""DAT calculation engine - supports multiple embedding models."""

import logging
from typing import List

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from backend.services.embedding import get_active_provider
from backend.services.vector_cache import get_cached_vectors

logger = logging.getLogger(__name__)


def compute_cosine_scores_from_vectors(vectors: np.ndarray) -> np.ndarray:
    """
    Compute pairwise cosine distances from a matrix of vectors.
    Uses vectorized computation.

    Args:
        vectors: (n_words, dim) numpy array

    Returns:
        1D array of cosine distances
    """
    n = len(vectors)
    if n < 2:
        return np.array([])

    # Vectorized: compute entire similarity matrix at once
    sim_matrix = cosine_similarity(vectors)

    # Extract lower triangle (excluding diagonal)
    tri_idx = np.tril_indices(n, -1)
    distances = 1.0 - sim_matrix[tri_idx]
    return distances


async def compute_dat_score(words_dict: dict) -> dict:
    """
    Calculate DAT score from a dict of 10 words.

    Uses the currently active embedding provider.
    All words are filtered and vectors are fetched (with caching for API models).

    Args:
        words_dict: dict with keys word1..word10

    Returns:
        dict with dat_score, effective_num, valid_words, provider_name
    """
    provider = get_active_provider()

    if provider is None:
        return {
            "dat_score": 0,
            "effective_num": 0,
            "valid_words": [],
            "provider_name": "none",
            "error": "No embedding provider available",
        }

    # Collect all words
    words = []
    for key in sorted(words_dict.keys()):
        if key.startswith("word"):
            words.append(words_dict[key])

    # Filter non-empty words
    input_words = [w for w in words if w]

    if not input_words:
        return {
            "dat_score": 0,
            "effective_num": 0,
            "valid_words": [],
            "provider_name": provider.model_name,
        }

    # For local models, use direct lookup
    if provider.is_local:
        valid_words = [w for w in input_words if provider.word_exists(w)]
        effective_num = len(valid_words)

        if effective_num < 2:
            return {
                "dat_score": 0,
                "effective_num": effective_num,
                "valid_words": valid_words,
                "provider_name": provider.model_name,
            }

        # Batch get vectors
        vectors = []
        for w in valid_words:
            v = await provider.get_vector(w)
            vectors.append(v)
        vectors = np.stack(vectors)

    else:
        # For API models, use caching
        valid_words = input_words  # API models don't have vocabulary check
        effective_num = len(valid_words)

        if effective_num < 2:
            return {
                "dat_score": 0,
                "effective_num": effective_num,
                "valid_words": valid_words,
                "provider_name": provider.model_name,
            }

        # Get vectors with caching
        vector_map = await get_cached_vectors(provider, valid_words)

        # Filter to words that got valid vectors
        vectors_list = []
        actual_valid_words = []
        for w in valid_words:
            v = vector_map.get(w)
            if v is not None and len(v) > 0:
                vectors_list.append(v)
                actual_valid_words.append(w)

        valid_words = actual_valid_words
        effective_num = len(valid_words)

        if effective_num < 2:
            return {
                "dat_score": 0,
                "effective_num": effective_num,
                "valid_words": valid_words,
                "provider_name": provider.model_name,
            }

        vectors = np.stack(vectors_list)

    # Compute all pairwise cosine distances (vectorized)
    distances = compute_cosine_scores_from_vectors(vectors)

    # Average distance * 100 = DAT score
    dat_score = int(np.mean(distances) * 100)

    return {
        "dat_score": dat_score,
        "effective_num": effective_num,
        "valid_words": valid_words,
        "provider_name": provider.model_name,
    }
