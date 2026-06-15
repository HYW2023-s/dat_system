"""Word2Vec embedding service - model loaded once, reused for all requests."""

import logging
from pathlib import Path

import numpy as np
from gensim.models import KeyedVectors

from backend.config import WORD2VEC_MODEL_PATH

logger = logging.getLogger(__name__)

# Global model instance
_word2vec_model = None


def load_model_on_startup():
    """Load the Word2Vec model into memory on application startup."""
    global _word2vec_model
    model_path = Path(WORD2VEC_MODEL_PATH)

    if not model_path.exists():
        logger.warning(f"Word2Vec model not found at {model_path}. "
                       f"Word2Vec-based calculations will not work.")
        return

    logger.info(f"Loading Word2Vec model from {model_path}...")
    _word2vec_model = KeyedVectors.load(str(model_path))
    logger.info(f"Word2Vec model loaded. Vocabulary size: {len(_word2vec_model.key_to_index)}")


def get_model():
    """Get the loaded model instance."""
    return _word2vec_model


def get_word_vector(word: str) -> np.ndarray | None:
    """Get the vector for a word. Returns None if word not in vocabulary."""
    if _word2vec_model is None:
        return None
    try:
        return _word2vec_model[word]
    except KeyError:
        return None


def word_in_vocabulary(word: str) -> bool:
    """Check if a word exists in the vocabulary."""
    if _word2vec_model is None:
        return False
    return word in _word2vec_model
