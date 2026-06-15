"""DAT calculation engine with vectorized optimization."""

import logging
from typing import List, Tuple

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from backend.services.embedding import get_word_vector, word_in_vocabulary

logger = logging.getLogger(__name__)


def compute_cosine_scores(valid_words: List[str]) -> np.ndarray:
    """
    Compute pairwise cosine distances for all valid words.
    Uses vectorized computation instead of double for-loop.

    Returns a 1D array of distances (lower triangle, no diagonal).
    """
    if len(valid_words) < 2:
        return np.array([])

    # Stack all word vectors into a single matrix (n_words, dim)
    vectors = np.stack([get_word_vector(w) for w in valid_words])

    # Compute cosine similarity matrix in one shot
    sim_matrix = cosine_similarity(vectors)

    # Extract lower triangle indices (excluding diagonal)
    n = len(valid_words)
    tri_idx = np.tril_indices(n, -1)

    # Convert similarities to distances
    distances = 1.0 - sim_matrix[tri_idx]

    return distances


def compute_dat_score(words_dict: dict) -> dict:
    """
    Calculate DAT score from a dict of 10 words.

    Args:
        words_dict: dict with keys word1..word10

    Returns:
        dict with dat_score, effective_num, valid_words
    """
    # Collect all words
    words = []
    for key in sorted(words_dict.keys()):
        if key.startswith("word"):
            words.append(words_dict[key])

    # Filter valid words (those in vocabulary)
    valid_words = [w for w in words if w and word_in_vocabulary(w)]
    effective_num = len(valid_words)

    if effective_num < 2:
        return {
            "dat_score": 0,
            "effective_num": effective_num,
            "valid_words": valid_words,
        }

    # Compute all pairwise cosine distances vectorized
    distances = compute_cosine_scores(valid_words)

    # Average distance * 100 = DAT score
    dat_score = int(np.mean(distances) * 100)

    return {
        "dat_score": dat_score,
        "effective_num": effective_num,
        "valid_words": valid_words,
    }
