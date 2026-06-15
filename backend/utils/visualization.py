"""MATPLOTLIB heatmap visualization for DAT results."""

import logging
from datetime import datetime
from pathlib import Path

import matplotlib
import matplotlib.colors as colors
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

from backend.config import STATIC_DIR, FONT_PATH
from backend.services.embedding import get_active_provider

logger = logging.getLogger(__name__)

# Configure matplotlib for Chinese support
matplotlib.use("Agg")

# Try to find a suitable Chinese font
_chinese_font = None
_font_candidates = ["STHeiti", "Heiti TC", "PingFang HK", "Lantinghei SC", "Songti SC", "STFangsong"]

font_path = Path(FONT_PATH)
if font_path.exists():
    try:
        fm.fontManager.addfont(str(font_path))
        plt.rcParams["font.family"] = "sans-serif"
        plt.rcParams["font.sans-serif"] = _font_candidates
        plt.rcParams["axes.unicode_minus"] = False
    except Exception:
        plt.rcParams["font.sans-serif"] = _font_candidates
        plt.rcParams["axes.unicode_minus"] = False
else:
    plt.rcParams["font.sans-serif"] = _font_candidates
    plt.rcParams["axes.unicode_minus"] = False


def generate_heatmap(valid_words: list, dat_score: int) -> str:
    """
    Generate a heatmap image for the DAT result.

    Args:
        valid_words: list of valid words
        dat_score: the computed DAT score

    Returns:
        relative URL path to the generated image (e.g., /assets/img/...)
    """
    n = len(valid_words)

    if n < 5:
        return "/assets/img/tips.jpg"

    # Get vectors - prefer Word2Vec for visualization (always available, no API cost)
    from backend.services.embedding import get_provider
    w2v = get_provider("word2vec")
    if w2v is None:
        logger.warning("Word2Vec provider not available for heatmap")
        return "/assets/img/tips.jpg"

    vectors = []
    for w in valid_words:
        # Use sync method for Word2Vec
        v = w2v.model[w] if w2v.model and w in w2v.model else None
        if v is not None:
            vectors.append(v)
        else:
            # Word not in vocab - should not happen since we already filtered
            return "/assets/img/tips.jpg"

    vectors = np.stack(vectors)
    from sklearn.metrics.pairwise import cosine_similarity
    sim_matrix = cosine_similarity(vectors)
    dist_matrix = (1 - sim_matrix) * 100  # Scale to 0-100 like original

    # Mask upper triangle and diagonal for display
    mask = np.triu(np.ones_like(dist_matrix), k=1)
    display_matrix = np.where(mask == 1, 0, dist_matrix)

    # Plot
    plt.figure(dpi=600)
    plt.xticks(range(n), labels=valid_words, rotation=60)
    plt.yticks(range(n), labels=valid_words)

    for i in range(n):
        for j in range(n):
            if i > j:  # Only lower triangle
                plt.text(j, i, int(display_matrix[i, j]),
                         ha="center", va="center", color="w", fontsize=8)

    cmap = colors.ListedColormap([
        "azure", "paleturquoise", "lightskyblue", "cornflowerblue", "royalblue"
    ])
    plt.imshow(display_matrix, cmap=cmap)

    # Save
    now = datetime.now()
    timestamp = now.timestamp()
    filename = f"thescoreis{dat_score}{timestamp}.jpg"

    img_dir = Path(STATIC_DIR) / "assets" / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    filepath = img_dir / filename
    plt.savefig(str(filepath))
    plt.close()

    return f"/assets/img/{filename}"
