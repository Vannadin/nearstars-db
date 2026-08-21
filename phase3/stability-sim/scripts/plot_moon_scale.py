# 폴리페무스 위성계 실척 도해 — 위성 크기 비교와 궤도 거리, 둘 다 같은 축척으로.
"""True-scale diagrams of a moon system: body sizes, and orbital distances.

Two figures, both drawn to scale from the design-of-record in
`hypotheticals/<system>.json` (radius_km, semi_major_axis_km) — nothing here is
schematic, which is the point: the moons turn out to be specks against the planet
and the orbits are mostly empty space.

  <system>_moon_sizes.png   bodies at true relative size, with Luna and Earth as
                            references, and again against the planet's limb
  <system>_moon_orbits.png  orbital radii to scale — inner system, then the full
                            extent — with the Roche limit and the synchronous
                            orbit marked, since they decide which way tides push

Both write the dark and light site palettes, and every render is kept via
scripts/viz/render_outputs.save_versioned rather than overwriting.

Usage: python3 scripts/plot_moon_scale.py [--system alpha_centauri] [--theme both]
"""
from __future__ import annotations

import argparse
import io
import json
import math
import sys
from pathlib import Path

import nsplot

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(REPO / "scripts" / "viz"))
from render_outputs import save_versioned                          # noqa: E402

R_JUP_KM = 71_492.0
R_LUNA_KM = 1_737.4
R_EARTH_KM = 6_371.0
G = 6.674e-11
M_EARTH_KG = 5.972e24

# Polyphemus, from the phase4 board: 120.873 M_E (planet + folded moons),
# 10.35 h day, 1 R_Jup equatorial radius.
PLANET = {"name": "Polyphemus", "r_km": R_JUP_KM,
          "mass_kg": 120.873 * M_EARTH_KG, "rot_h": 10.35,
          "roche_rp": 1.31}          # rocky-moon Roche limit (design note)


def load_moons(system: str):
    d = json.loads((ROOT / "hypotheticals" / f"{system}.json").read_text())
    ms = [m for m in d["bodies"] if m.get("type") == "moon"]
    return sorted(ms, key=lambda m: m["semi_major_axis_km"])


def synchronous_km() -> float:
    p = PLANET["rot_h"] * 3600.0
    return (G * PLANET["mass_kg"] * p * p / (4 * math.pi ** 2)) ** (1 / 3) / 1e3


def _keep(fig, name, label):
    from PIL import Image
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=140, bbox_inches="tight")
    buf.seek(0)
    return save_versioned(Image.open(buf), name, label, root=str(REPO / "dist/_scratch/renders"))


def fig_sizes(system: str, theme: str):
    nsplot.apply_theme(theme)
    import matplotlib.pyplot as plt

    moons = load_moons(system)
    cols = nsplot.series_colors(len(moons))
    refs = [("Luna", R_LUNA_KM, nsplot.FG_DIM), ("Earth", R_EARTH_KM, "#4a90d9")]

    fig, (ax, axp) = plt.subplots(2, 1, figsize=(13, 9),
                                  gridspec_kw={"height_ratios": [2, 1], "hspace": 0.22})

    # --- top: moons + references, true relative size, sitting on one baseline ---
    items = [(m["name"], m["radius_km"], cols[i]) for i, m in enumerate(moons)] + refs
    rmax = max(r for _, r, _ in items)
    gap = rmax * 0.16
    x = 0.0
    for name, r, c in items:
        ax.add_patch(plt.Circle((x + r, r), r, color=c, alpha=0.9))
        # labels in offset POINTS, so text never scales with the data range
        ax.annotate(f"{name}\n{r:,.0f} km", (x + r, 0), textcoords="offset points",
                    xytext=(0, -9), ha="center", va="top", fontsize=9, color=c)
        x += 2 * r + gap
    ax.set_xlim(-gap, x)
    ax.set_ylim(-rmax * 0.62, 2 * rmax * 1.05)     # room below for two label lines
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"{PLANET['name']}'s moons at true relative size "
                 f"(Luna and Earth for scale)", fontsize=12)

    # --- bottom: the same moons against the planet's limb ---
    Rp = PLANET["r_km"]
    axp.add_patch(plt.Circle((0, 0), Rp, color="#c9a06a", alpha=0.55))
    axp.annotate(f"{PLANET['name']}\n{Rp:,.0f} km", (0, 0), ha="center", va="center",
                 fontsize=10, color=nsplot.FG)
    # a COLUMN, not a row: at this ruler every moon is a dot whose name is far wider
    # than the dot, so any horizontal arrangement collides. One row each, label right.
    xm = Rp * 1.45
    step = Rp * 0.42
    y0 = step * (len(moons) - 1) / 2
    for i, m in enumerate(moons):
        y = y0 - i * step
        axp.add_patch(plt.Circle((xm, y), m["radius_km"], color=cols[i], alpha=0.95))
        axp.annotate(f"{m['name']}  {m['radius_km']:,.0f} km", (xm, y),
                     textcoords="offset points", xytext=(12, 0), ha="left",
                     va="center", fontsize=8.5, color=cols[i])
    axp.set_xlim(-Rp * 1.12, Rp * 3.1)
    axp.set_ylim(-Rp * 1.12, Rp * 1.12)
    axp.set_aspect("equal")
    axp.axis("off")
    big = max(moons, key=lambda m: m["radius_km"])
    axp.set_title(f"…and against the planet: {big['name']}, the largest, is "
                  f"1/{Rp / big['radius_km']:.0f} of {PLANET['name']}'s radius", fontsize=11)

    out = _keep(fig, f"{system}-moon-sizes", theme)
    plt.close(fig)
    return out


def fig_orbits(system: str, theme: str):
    nsplot.apply_theme(theme)
    import matplotlib.pyplot as plt

    moons = load_moons(system)
    cols = nsplot.series_colors(len(moons))
    Rp = PLANET["r_km"]
    sync = synchronous_km()
    roche = PLANET["roche_rp"] * Rp

    # inner panel stops just past the third moon; the wide panel holds everything
    inner_lim = moons[min(2, len(moons) - 1)]["semi_major_axis_km"] * 1.25
    outer_lim = moons[-1]["semi_major_axis_km"] * 1.12

    fig, axes = plt.subplots(1, 2, figsize=(14, 7.4))
    for ax, lim, title, first in (
            (axes[0], inner_lim, "inner system", True),
            (axes[1], outer_lim, "full extent", False)):
        ax.add_patch(plt.Circle((0, 0), Rp, color="#c9a06a", alpha=0.55, zorder=3))
        for r, c, lab, ls in ((roche, "#e1566a", "Roche limit (rocky)", ":"),
                              (sync, "#4a90d9", "synchronous orbit", "--")):
            ax.add_patch(plt.Circle((0, 0), r, fill=False, ec=c, ls=ls, lw=1.1,
                                    alpha=0.85, zorder=2))
            if first:            # annotated once; on the wide panel they are a blur
                ax.annotate(lab, (0, r), textcoords="offset points", xytext=(4, 3),
                            fontsize=7.5, color=c, zorder=4)
        for i, m in enumerate(moons):
            a = m["semi_major_axis_km"]
            if a > lim:
                continue
            ax.add_patch(plt.Circle((0, 0), a, fill=False, ec=cols[i], lw=1.2,
                                    alpha=0.9, zorder=2))
            # the body itself, also true scale — usually sub-pixel, which is the point
            ax.add_patch(plt.Circle((a, 0), m["radius_km"], color=cols[i], zorder=5))
            # label centred under its OWN circle, so labels separate by radius
            # instead of piling up along one line. The wide panel only labels the
            # moons the inner panel could not show.
            if first or a > inner_lim:
                ax.annotate(f"{m['name']}  {a:,.0f} km ({a / Rp:.2f} R$_p$)",
                            (0, -a), textcoords="offset points", xytext=(0, -5),
                            ha="center", va="top", fontsize=8, color=cols[i], zorder=4)
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(f"{title} — {lim / Rp:.1f} R$_p$ across", fontsize=11)

    hill_rp = 160.0     # α Cen A b: computed in the rescue-scan README
    fig.suptitle(f"{PLANET['name']}'s moon orbits at true scale "
                 f"(planet, orbits and moons all to the same ruler)", fontsize=13)
    fig.text(0.5, 0.03,
             f"Everything is to scale, including each moon — at this ruler even the "
             f"largest is a dot. Tides push a moon outward beyond the synchronous "
             f"orbit ({sync / Rp:.2f} R$_p$) and inward inside it. "
             f"The Hill radius, {hill_rp:.0f} R$_p$, is {hill_rp / (outer_lim / Rp):.0f}× "
             f"wider than the right panel.",
             ha="center", fontsize=8.5, color=nsplot.FG_DIM)

    out = _keep(fig, f"{system}-moon-orbits", theme)
    plt.close(fig)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--system", default="alpha_centauri")
    ap.add_argument("--theme", choices=["dark", "light", "both"], default="both")
    a = ap.parse_args()
    for t in (["dark", "light"] if a.theme == "both" else [a.theme]):
        print("sizes :", fig_sizes(a.system, t))
        print("orbits:", fig_orbits(a.system, t))
