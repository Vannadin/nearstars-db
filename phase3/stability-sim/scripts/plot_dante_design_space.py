# Dante 설계 공간 한 장 — 크기와 용암호 면적을 고르면 호수 온도가 결정된다는 관계도.
"""The Dante design space: one chart instead of a pile of tables.

The whole tangle of surface temperature, conduction, and local heating reduces to
ONE budget with one usable exit:

  1. All the tidal heat generated inside has to leave through the surface.
  2. Rock conducts badly. A lithosphere thick enough to hold up topography
     (kilometres, as on Io) passes only ~0.1 W/m² — nothing. So the cold plains
     are not an exit, and they simply sit at starlight equilibrium (223 K here).
     A warmer plains temperature is not a choice; it is a claim that the lid is
     metres thick, which cannot support a landscape.
  3. That leaves the lava lakes. They radiate σT⁴ per unit area, so
        heat generated (set by SIZE)  =  lake area × σ T_lake⁴
     Pick any two of {size, lake area, lake temperature} and the third follows.

The chart draws that last line. Contours are the lake temperature the budget
demands; the shaded band is where a real crusted lava lake can actually sit
(~300–900 K, from Io observations). Above it the "lake" would have to be
crust-free molten rock across the whole area, which is the assumption that broke
the 900 km design.

Sanity check built in: run the same relation on Io itself (2.5 W/m² through ~0.05 %
of its area) and it returns ~545 K — squarely in the observed band. The model is
not tuned to Dante.

Writes both site palettes via scripts/viz/render_outputs.save_versioned.

Usage: python3 scripts/plot_dante_design_space.py [--theme both]
"""
from __future__ import annotations

import argparse
import io
import math
import sys
from pathlib import Path

import numpy as np
import nsplot

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO / "scripts" / "viz"))
from render_outputs import save_versioned                       # noqa: E402

SB = 5.67e-8
F_STAR = 141.0                  # absorbed starlight → the plains' floor
R0, F0, P0 = 900.0, 11_500.0, 1200.0     # the shipped Dante: radius, flux, output
LAKE_LO, LAKE_HI = 300.0, 900.0          # crusted lava lake, from Io observations
IO = dict(r=1821.0, flux=2.5, frac=0.0005)


def tidal_flux(r_km):
    """Surface tidal flux, W/m². Io scaling: total ∝ R⁵, so flux ∝ R³."""
    return F0 * (r_km / R0) ** 3


def lake_temp(r_km, frac):
    """Effective lake temperature the heat budget demands (cold plains)."""
    return (tidal_flux(r_km) / frac / SB) ** 0.25


def draw(theme: str):
    nsplot.apply_theme(theme)
    import matplotlib.pyplot as plt

    rr = np.linspace(200, 900, 400)
    ff = np.logspace(math.log10(0.004), math.log10(0.35), 320)
    Rg, Fg = np.meshgrid(rr, ff)
    Tg = (F0 * (Rg / R0) ** 3 / Fg / SB) ** 0.25

    fig, ax = plt.subplots(figsize=(12.4, 7.6))

    # feasible band: a real crusted lake can sit here
    ax.contourf(Rg, 100 * Fg, Tg, levels=[LAKE_LO, LAKE_HI],
                colors=["#48c78e"], alpha=0.16, zorder=0)
    cs = ax.contour(Rg, 100 * Fg, Tg,
                    levels=[300, 450, 600, 750, 900, 1100, 1350],
                    colors=[nsplot.FG_DIM], linewidths=0.9, alpha=0.85)
    ax.clabel(cs, fmt=lambda v: f"{v:.0f} K", fontsize=8.5, inline_spacing=6)
    ax.contour(Rg, 100 * Fg, Tg, levels=[LAKE_HI], colors=["#e1566a"], linewidths=2.0)
    ax.contour(Rg, 100 * Fg, Tg, levels=[LAKE_LO], colors=["#4a90d9"], linewidths=2.0)
    ax.contour(Rg, 100 * Fg, Tg, levels=[1350.0], colors=["#ff2d55"],
               linewidths=2.0, linestyles="--")
    ax.text(952, 3.0, "1350 K silicate melting point —\nnothing works below this line",
            fontsize=8, color="#ff2d55", ha="right", va="center")
    # the shaded band IS the feasible one; name both of its edges on the plot
    ax.text(268, 12.5, "crusted lava lakes can live here — dark plates with\n"
            "glowing cracks (300–900 K, as observed on Io)",
            fontsize=9, color="#48c78e", va="center")
    ax.text(690, 0.78, "too hot: the budget would demand that the LAKES' OWN area\n"
                       "be crust-free exposed melt end to end (not the whole surface).\n"
                       "Past ~1350 K even that fails — it exceeds the silicate melting\n"
                       "point, which is where the shipped 900 km / 5 % design sat.",
            fontsize=8.5, color="#e1566a", va="center", ha="center")
    ax.text(905, 26, "900 K ceiling", fontsize=8.5, color="#e1566a",
            ha="right", va="center", rotation=-38)

    # candidate points at the owner's 5 % coverage
    frac = 0.05
    cands = [(300, ""), (350, ""), (400, ""), (450, "recommended"),
             (500, ""), (600, ""), (714, ""), (900, "shipped")]
    for i, (r, note) in enumerate(cands):
        T = lake_temp(r, frac)
        ok = LAKE_LO <= T <= LAKE_HI
        ax.plot([r], [100 * frac], "o", ms=10 if note else 7,
                color="#48c78e" if ok else "#e1566a", zorder=5,
                mec=nsplot.FG if note else "none", mew=1.4)
        ax.annotate(f"{r} km\n{P0 * (r / R0) ** 5:.0f}× Io\n{T:.0f} K"
                    + (f"\n{note}" if note else ""),
                    (r, 100 * frac), textcoords="offset points",
                    xytext=(0, 16 if i % 2 else -14), ha="center",
                    va="bottom" if i % 2 else "top", fontsize=8,
                    color="#48c78e" if ok else "#e1566a")
    ax.axhline(100 * frac, color=nsplot.FG_DIM, lw=0.8, ls="--", alpha=0.7)
    ax.text(898, 100 * frac * 1.06, "owner's target: lakes over 5 % of the surface",
            ha="right", fontsize=8.5, color=nsplot.FG_DIM)

    ax.set_xscale("linear")
    ax.set_yscale("log")
    ax.set_xlim(200, 960)
    ax.set_ylim(0.4, 35)
    ax.set_xlabel("Dante radius (km)   — sets how much heat there is (total ∝ R⁵)")
    ax.set_ylabel("lava-lake share of the surface (%)")
    ax.set_title("Dante design space — pick a size and a lake area, and the heat "
                 "budget fixes the lake temperature")
    ax.set_yticks([0.5, 1, 2, 5, 10, 20, 30])
    ax.set_yticklabels(["0.5", "1", "2", "5", "10", "20", "30"])
    ax.grid(alpha=0.18)

    io_T = (IO["flux"] / IO["frac"] / SB) ** 0.25
    fig.text(0.5, 0.015,
             "The plains are not an exit: a lithosphere thick enough to hold up "
             "topography passes ~0.1 W/m², so they just sit at starlight "
             f"equilibrium ({(F_STAR / SB) ** 0.25:.0f} K). All the heat leaves "
             "through the lakes, which is why area and temperature trade off.   "
             f"Model check — the same relation applied to Io (2.5 W/m² over "
             f"{100 * IO['frac']:.2f} % of its area) returns {io_T:.0f} K, inside "
             "the observed band.",
             ha="center", fontsize=8.5, color=nsplot.FG_DIM, wrap=True)

    from PIL import Image
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight")
    buf.seek(0)
    out = save_versioned(Image.open(buf), "dante-design-space", theme,
                         root=str(REPO / "dist/_scratch/renders"))
    plt.close(fig)
    print(f"wrote {out}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", choices=["dark", "light", "both"], default="both")
    a = ap.parse_args()
    for t in (["dark", "light"] if a.theme == "both" else [a.theme]):
        draw(t)
