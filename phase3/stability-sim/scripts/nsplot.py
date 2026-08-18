# 안정성 런 PNG를 사이트 v2 팔레트(다크/라이트)로 그리기 위한 공용 matplotlib 스타일.
"""Shared matplotlib theme for the stability-sim figures, in both site themes.

The gallery and validation pages render these PNGs as thumbnails, and the site
follows the reader's `prefers-color-scheme`. A dark-only figure punches a hole in
a light page exactly as matplotlib's default white one did in a dark page, so both
palettes live here and the caller picks. Tokens mirror docs/style.css (v2).

Call apply_theme() once, before creating any figure. `FG_DIM` is exported so
callers can draw neutral guide lines that stay visible in whichever theme is live —
matplotlib's "k" is invisible on the dark panel.
"""
import matplotlib

BG = "#06070a"
PANEL = "#0c0e14"
FG = "#e8e9ee"
FG_DIM = "#9a9daa"
GRID = "#20232c"
ACCENT = "#7aa8ff"

_THEMES = {
    "dark": dict(bg=BG, panel=PANEL, fg=FG, fg_dim=FG_DIM, grid=GRID,
                 # plasma 0.12-0.88: deep violet through to yellow, legible on near-black
                 series=(0.12, 0.88)),
    "light": dict(bg="#f5f6fa", panel="#ffffff", fg="#0c1122", fg_dim="#5b6070",
                  grid="#d8dae2",
                  # plasma stops short of the yellow end, which washes out on white
                  series=(0.05, 0.72)),
}

_active = "dark"


def apply_theme(theme: str = "dark"):
    """Set the rcParams for `theme` and remember it for series_colors()."""
    global _active, FG, FG_DIM
    t = _THEMES[theme]
    _active = theme
    FG, FG_DIM = t["fg"], t["fg_dim"]
    matplotlib.rcParams.update({
        "figure.facecolor": t["bg"],
        "figure.edgecolor": t["bg"],
        "savefig.facecolor": t["bg"],
        "savefig.edgecolor": t["bg"],
        "axes.facecolor": t["panel"],
        "axes.edgecolor": t["grid"],
        "axes.labelcolor": t["fg"],
        "axes.titlecolor": t["fg"],
        "text.color": t["fg"],
        "xtick.color": t["fg_dim"],
        "ytick.color": t["fg_dim"],
        "grid.color": t["grid"],
        "legend.facecolor": t["panel"],
        "legend.edgecolor": t["grid"],
        "legend.labelcolor": t["fg"],
    })


def apply_dark():
    """Back-compat entry point for the callers that only ever want the dark figure."""
    apply_theme("dark")


def series_colors(n: int):
    """`n` per-body colors from plasma, over the active theme's legible sub-range."""
    import matplotlib.pyplot as plt
    lo, hi = _THEMES[_active]["series"]
    return plt.cm.plasma([lo + (hi - lo) * i / max(1, n - 1) for i in range(n)])
