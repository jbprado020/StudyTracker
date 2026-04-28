"""Matplotlib / Seaborn styling helpers for Study Tracker charts."""
from typing import List
import matplotlib as mpl
import seaborn as sns


# Color tokens aligned with app theme
PRIMARY = "#0f766e"
ACCENT = "#0ea5a2"
HIGHLIGHT = "#f59e0b"
SURFACE = "#ffffff"
TEXT = "#1f2937"


def apply_chart_style(font_size: int = 11, high_contrast: bool = False) -> None:
    """Apply a consistent visual style for matplotlib/seaborn charts.

    Args:
        font_size: base font size for chart text
        high_contrast: if True, use higher contrast palette
    """
    mpl.rcParams.update({
        "font.family": "Segoe UI",
        "font.size": font_size,
        "axes.titlesize": font_size + 2,
        "axes.titleweight": "bold",
        "axes.labelsize": font_size,
        "xtick.labelsize": max(8, font_size - 1),
        "ytick.labelsize": max(8, font_size - 1),
        "figure.facecolor": SURFACE,
        "axes.facecolor": "#fafcfb",
        "axes.edgecolor": "#e6efe9",
        "legend.frameon": False,
        "figure.autolayout": False,
    })

    sns.set_theme(style="whitegrid")

    if high_contrast:
        sns.set_palette(["#111111", PRIMARY, ACCENT, HIGHLIGHT])
    else:
        sns.set_palette([PRIMARY, ACCENT, HIGHLIGHT, "#6ee7b7", "#60a5fa"])


def get_palette(n: int) -> List[str]:
    """Return a palette of `n` colors derived from the theme.

    Args:
        n: number of colors required

    Returns:
        list of hex color strings
    """
    base = sns.color_palette()
    if n <= len(base):
        return [mpl.colors.to_hex(c) for c in base[:n]]
    # generate an extended palette
    return [mpl.colors.to_hex(c) for c in sns.color_palette("husl", n)]
