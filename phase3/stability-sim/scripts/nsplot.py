# 안정성 런 PNG를 사이트 v2 다크 팔레트로 그리기 위한 공용 matplotlib 스타일.
"""Shared dark matplotlib style for the stability-sim figures.

The gallery and validation pages render these PNGs as thumbnails on the site's
near-black canvas; matplotlib's default white figure punched a bright hole in
every card. Tokens mirror docs/style.css (v2): canvas #06070a, white-alpha
foregrounds, #7aa8ff accent.

Call apply_dark() once, before creating any figure.
"""
import matplotlib

BG = "#06070a"
PANEL = "#0c0e14"
FG = "#e8e9ee"
FG_DIM = "#9a9daa"
GRID = "#20232c"
ACCENT = "#7aa8ff"


def apply_dark():
    matplotlib.rcParams.update({
        "figure.facecolor": BG,
        "figure.edgecolor": BG,
        "savefig.facecolor": BG,
        "savefig.edgecolor": BG,
        "axes.facecolor": PANEL,
        "axes.edgecolor": GRID,
        "axes.labelcolor": FG,
        "axes.titlecolor": FG,
        "text.color": FG,
        "xtick.color": FG_DIM,
        "ytick.color": FG_DIM,
        "grid.color": GRID,
        "legend.facecolor": PANEL,
        "legend.edgecolor": GRID,
        "legend.labelcolor": FG,
    })
