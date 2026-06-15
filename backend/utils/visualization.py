"""Heatmap visualization for DAT results - matplotlib fallback only."""

import logging
from datetime import datetime
from pathlib import Path

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np

from backend.config import STATIC_DIR, FONT_PATH

logger = logging.getLogger(__name__)

matplotlib.use("Agg")

# Chinese font setup
_font_candidates = ["STHeiti", "Heiti TC", "PingFang HK", "Lantinghei SC", "Songti SC", "STFangsong"]
font_path = Path(FONT_PATH)
if font_path.exists():
    try:
        fm.fontManager.addfont(str(font_path))
    except Exception:
        pass

plt.rcParams["font.sans-serif"] = _font_candidates
plt.rcParams["axes.unicode_minus"] = False


def generate_heatmap(valid_words: list, dat_score: int, lang: str = "zh") -> str:
    """
    Generate a clean heatmap image as fallback (ECharts is the primary renderer).

    Uses the 'RdYlBu_r' colormap: blue=close, red=far — intuitive for distance.
    """
    n = len(valid_words)

    if n < 5:
        return "/assets/img/tips.jpg"

    from backend.services.embedding import get_provider
    from sklearn.metrics.pairwise import cosine_similarity

    w2v = get_provider("word2vec")
    if w2v is None or w2v.model is None:
        return "/assets/img/tips.jpg"

    # Build distance matrix
    vectors = []
    for w in valid_words:
        v = w2v.model[w] if w in w2v.model else None
        if v is None:
            return "/assets/img/tips.jpg"
        vectors.append(v)

    vectors = np.stack(vectors)
    sim_matrix = cosine_similarity(vectors)
    dist_matrix = (1 - sim_matrix) * 100

    # Build a full symmetric matrix for display
    # Lower triangle = data, upper + diagonal = NaN (won't be colored)
    display = np.full((n, n), np.nan)
    for i in range(n):
        for j in range(i + 1, n):
            display[i, j] = dist_matrix[i, j]
            display[j, i] = dist_matrix[i, j]

    # Create figure with clean proportions
    figsize = max(6, n * 0.7)
    fig, ax = plt.subplots(figsize=(figsize, figsize), dpi=150)

    # Use a proper diverging colormap: blue (close) → white → red (far)
    cmap = plt.cm.RdYlBu_r

    # Mask NaN cells (diagonal) with white
    cmap.set_bad("white")

    im = ax.imshow(display, cmap=cmap, aspect="equal", vmin=0, vmax=100)

    # Add value text in each cell (lower triangle only)
    for i in range(n):
        for j in range(i + 1, n):
            val = display[i, j]
            # Dark text on light bg, light text on dark bg
            text_color = "white" if val > 50 else "#1a1a2e"
            ax.text(j, i, f"{val:.0f}",
                    ha="center", va="center",
                    fontsize=10, fontweight="bold",
                    color=text_color)
            # Mirror value in upper triangle
            ax.text(i, j, f"{val:.0f}",
                    ha="center", va="center",
                    fontsize=10, fontweight="bold",
                    color=text_color)

    # Ticks and labels
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(valid_words, fontsize=11, rotation=30, ha="right")
    ax.set_yticklabels(valid_words, fontsize=11)

    # Clean styling
    ax.tick_params(top=False, bottom=False, left=False, right=False)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, shrink=0.82, pad=0.02)
    from backend.i18n import t as i18n_t
    cbar.set_label(i18n_t("viz.distance_label", lang), fontsize=11)
    cbar.ax.tick_params(labelsize=9)

    # Title
    ax.set_title(
        i18n_t("viz.title", lang, score=dat_score),
        fontsize=13, fontweight="bold", pad=12,
    )

    plt.tight_layout()

    # Save
    now = datetime.now()
    timestamp = now.timestamp()
    filename = f"heatmap_{dat_score}_{timestamp:.0f}.png"
    img_dir = Path(STATIC_DIR) / "assets" / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    filepath = img_dir / filename
    plt.savefig(str(filepath), bbox_inches="tight", facecolor="white")
    plt.close()

    return f"/assets/img/{filename}"
