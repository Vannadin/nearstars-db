# Hades 구제 스캔의 생존 지형도 — 후보별 판정·최대 이심률을 공명 위치와 함께 한 장에.
"""Survival-landscape figure for the Hades rescue scan.

`plot_moons.py` draws ONE run's four panels; this draws the whole scan — every
candidate semi-major axis against its verdict, over the resonance comb that
explains the verdicts. Two panels share the x axis (Hades' semi-major axis in km):

  top     max eccentricity reached, log scale, with the e >= 0.9 ejection
          criterion as a dashed line. A candidate that ejects another moon is
          ringed, since it is disqualified even when Hades itself survives.
  bottom  the low-order (q <= 4) mean-motion resonances with Dante below and
          Pandora above, each at the semi-major axis where it falls — the comb
          whose teeth cover the corridor.

Reads results/hades_rescue/*/alpha_centauri_summary.json (the a-grid candidates
plus the a=150,000 robustness battery) and writes both site palettes:

  results/hades_rescue/rescue_scan.png        (dark)
  results/hades_rescue/rescue_scan_light.png  (light)

Usage: python3 scripts/plot_rescue_scan.py [--theme dark|light|both]
"""
from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

import nsplot

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "results" / "hades_rescue"

A_DANTE_KM = 110_000.0
A_PANDORA_KM = 252_393.0
A_SHIPPED_KM = 148_000.0
E_EJECT = 0.9          # the suite's "orbit nearly unbound" criterion
E_CLIP = 3.0           # ejected candidates run to ~1e9; park them on one row


def read_grid():
    """(a_km, e_max, bound, collateral[]) per a-only candidate, sorted by a."""
    rows = []
    for d in SCAN.glob("a_*"):
        if not re.fullmatch(r"a_\d+", d.name):        # skip the battery variants
            continue
        s = d / "alpha_centauri_summary.json"
        if not s.exists():
            continue
        j = json.loads(s.read_text())
        hades = j["per_body"]["Hades"]
        bound = j["hill_track"]["Hades"]["bound"] and hades["e_max"] < E_EJECT
        coll = [n for n, p in j["per_body"].items()
                if n != "Hades" and (p["e_max"] >= E_EJECT
                                     or not j["hill_track"].get(n, {}).get("bound", True))]
        rows.append((int(d.name[2:]), hades["e_max"], bound, coll))
    return sorted(rows)


def read_battery():
    """{variant: survived} for the a=150,000 robustness runs.

    Keys are the variant tags: `ma<deg>` re-runs with a different initial mean
    anomaly (a phase test), `dt5` halves the timestep (a resolution test). They
    answer different questions, so the caller must not pool them.
    """
    out = {}
    for d in sorted(SCAN.glob("a_150000_*")):
        s = d / "alpha_centauri_summary.json"
        if not s.exists():
            continue
        j = json.loads(s.read_text())
        hades = j["per_body"]["Hades"]
        out[d.name.replace("a_150000_", "")] = (
            j["hill_track"]["Hades"]["bound"] and hades["e_max"] < E_EJECT)
    return out


def resonances(a_other_km: float, inner: bool, lo: float, hi: float):
    """Low-order p:q resonances with a moon at `a_other_km`, inside [lo, hi] km.

    `inner=True` means the other moon is INSIDE Hades (Dante), so Hades' period is
    the longer one: a_H = a_other · (p/q)^(2/3). For an outer moon (Pandora) the
    ratio inverts.
    """
    out = []
    for q in range(1, 5):
        for p in range(q + 1, 4 * q + 1):
            if math.gcd(p, q) != 1:                   # 10:4 IS 5:2 — one tooth, one label
                continue
            ratio = (p / q) ** (2 / 3)
            a = a_other_km * (ratio if inner else 1 / ratio)
            if lo <= a <= hi:
                out.append((a, f"{p}:{q}"))
    return sorted(out)


def draw(theme: str):
    nsplot.apply_theme(theme)
    import matplotlib.pyplot as plt

    grid, batt = read_grid(), read_battery()
    if not grid:
        raise SystemExit(f"no candidates found under {SCAN}")

    lo = min(a for a, *_ in grid) - 3_000
    hi = max(a for a, *_ in grid) + 3_000
    ok_col, bad_col = "#48c78e", "#e1566a"

    fig, (ax, axr) = plt.subplots(
        2, 1, figsize=(13, 8.2), sharex=True,
        gridspec_kw={"height_ratios": [3, 1], "hspace": 0.08})

    # resonance guide lines spanning both panels, drawn first so points sit on top
    for a, _ in resonances(A_DANTE_KM, True, lo, hi) + resonances(A_PANDORA_KM, False, lo, hi):
        for a_ in (ax, axr):
            a_.axvline(a, color=nsplot.FG_DIM, lw=0.6, alpha=0.28, zorder=0)

    # --- top: e_max per candidate ---
    ax.axhline(E_EJECT, color=nsplot.FG_DIM, lw=1.0, ls="--", alpha=0.8)
    ax.text(hi, E_EJECT * 1.08, "ejection criterion  e = 0.9", ha="right", va="bottom",
            fontsize=8, color=nsplot.FG_DIM)
    for a, e_max, bound, coll in grid:
        y = min(e_max, E_CLIP)
        ax.plot([a], [y], marker="o" if bound else "x", ms=9 if bound else 8,
                mew=2.0, color=ok_col if bound else bad_col, zorder=3)
        if coll:                                       # also ejected another moon
            ax.plot([a], [y], marker="o", ms=17, mfc="none", mew=1.3,
                    color=bad_col, zorder=2)
            ax.annotate(f"+{coll[0]}", (a, y), textcoords="offset points",
                        xytext=(0, -17), ha="center", fontsize=7, color=bad_col)
    ax.axvline(A_SHIPPED_KM, color=nsplot.ACCENT, lw=1.4, alpha=0.9, zorder=1)
    ax.annotate("shipped 148,000 km\n(ejects at 56 kyr)", (A_SHIPPED_KM, 1.35),
                textcoords="offset points", xytext=(-8, 0), ha="right", va="center",
                fontsize=8, color=nsplot.ACCENT)
    ax.text(lo + 1_200, E_CLIP * 1.5, "ejected candidates clipped for display "
                                      "(true e ≫ 1: the orbit is hyperbolic)",
            ha="left", va="center", fontsize=7.5, color=nsplot.FG_DIM)

    # the one clean survivor, and why it still fails. Phase variants and the
    # timestep variant answer different questions, so they are counted separately:
    # the base run's own phase counts toward the phase tally, dt5 never does.
    if batt:
        phases = {k: v for k, v in batt.items() if k.startswith("ma")}
        surv = next((r for r in grid if r[0] == 150_000), None)
        if surv and phases:
            n_ok = sum(1 for v in phases.values() if v) + 1        # + the base phase
            dt_note = ("holds at half the timestep" if batt.get("dt5")
                       else "fails at half the timestep")
            ax.annotate(
                f"150,000 km — the only clean survivor,\n"
                f"but holds only {n_ok} of {len(phases) + 1} initial phases "
                f"({dt_note})\n→ chaotic-zone edge, not a stable island",
                (150_000, min(surv[1], E_CLIP)), textcoords="offset points",
                xytext=(34, 30), ha="left", fontsize=8.5, color=ok_col,
                arrowprops=dict(arrowstyle="->", color=ok_col, lw=1.1, alpha=0.9))

    ax.set_yscale("log")
    ax.set_ylim(3e-3, E_CLIP * 2.6)
    ax.set_ylabel("Hades max eccentricity over 10⁵ yr")
    ax.set_title("Hades rescue scan — every candidate semi-major axis over 10⁵ yr "
                 "(leapfrog, dt = 10 min, J2 on)")
    ax.grid(alpha=0.22)
    ax.plot([], [], "o", color=ok_col, ms=9, label="Hill-bound at 10⁵ yr")
    ax.plot([], [], "x", color=bad_col, ms=8, mew=2, label="ejected")
    ax.plot([], [], "o", mfc="none", color=bad_col, ms=13, mew=1.3,
            label="also ejected another moon")
    ax.legend(loc="lower right", fontsize=8, ncol=3)

    # --- bottom: the resonance comb ---
    # both comb rows take a legible mid-plasma color — series_colors' first stop is
    # a deep violet that disappears against the dark panel
    comb = nsplot.series_colors(5)
    for a_other, inner, row, name, col in ((A_DANTE_KM, True, 0.30, "Dante", 2),
                                           (A_PANDORA_KM, False, 0.72, "Pandora", 4)):
        c = comb[col]
        for a, lab in resonances(a_other, inner, lo, hi):
            axr.plot([a], [row], marker="|", ms=15, mew=2.0, color=c)
            axr.annotate(lab, (a, row), textcoords="offset points", xytext=(0, 9),
                         ha="center", fontsize=7.5, color=c)
        axr.text(lo + 400, row, f"{name} ", ha="left", va="center",
                 fontsize=9, color=c, fontweight="bold")
    axr.set_ylim(0, 1.02)
    axr.set_yticks([])
    axr.set_xlim(lo, hi)
    axr.set_xlabel("Hades semi-major axis (km)   ·   Dante at 110,000 · Pandora at 252,393")
    axr.set_title("low-order mean-motion resonances (q ≤ 4) falling in this corridor",
                  fontsize=9, pad=2)
    axr.grid(alpha=0.15, axis="x")

    fig.text(0.5, 0.012,
             "Pandora is 860× Hades' mass, so its resonances tile the whole corridor: "
             "no gap between them holds a robust orbit. "
             "Earlier 10⁴ yr runs saw every one of these as stable.",
             ha="center", fontsize=8.5, color=nsplot.FG_DIM)

    out = SCAN / ("rescue_scan.png" if theme == "dark" else "rescue_scan_light.png")
    fig.savefig(out, dpi=135, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {out}  ({len(grid)} candidates, {len(batt)} battery variants)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--theme", choices=["dark", "light", "both"], default="both")
    a = ap.parse_args()
    for t in (["dark", "light"] if a.theme == "both" else [a.theme]):
        draw(t)
