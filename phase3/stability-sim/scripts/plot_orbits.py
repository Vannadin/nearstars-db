# 안정성 런의 궤도 해를 시각화 — top-down 궤도 + 이심률 시간진화 2패널 PNG 생성.
"""Plot a stability run's orbit solution: top-down orbits + eccentricity-vs-time.

Reads results/<label>_summary.json (initial elements + masses + verdict) and
results/<label>_timeseries.csv (e(t) per body), writes results/<label>_orbits.png.

Usage: python3 scripts/plot_orbits.py [label]   (default: barnards_star_i60)
"""
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent / "results"
label = sys.argv[1] if len(sys.argv) > 1 else "barnards_star_i60"

summary = json.loads((RESULTS / f"{label}_summary.json").read_text())
MEARTH_MSUN = 5.9722e24 / 1.98892e30
planets = summary["planets"]
colors = plt.cm.viridis([i / max(1, len(planets) - 1) for i in range(len(planets))])

# eccentricity time series per body
series = defaultdict(list)
with (RESULTS / f"{label}_timeseries.csv").open() as f:
    for r in csv.DictReader(f):
        series[r["body"]].append((float(r["t_yr"]), float(r["e"])))

fig, (axo, axe) = plt.subplots(1, 2, figsize=(13, 6))

# --- panel 1: top-down orbits (star at focus) ---
fa = [i * 2 * math.pi / 400 for i in range(401)]
for p, c in zip(planets, colors):
    a, e = p["a_au"], p["e"]
    om = p.get("omega_rad", 0.0)
    xs = [a * (1 - e * e) / (1 + e * math.cos(t)) * math.cos(t + om) for t in fa]
    ys = [a * (1 - e * e) / (1 + e * math.cos(t)) * math.sin(t + om) for t in fa]
    m_e = p["mass_msun"] / MEARTH_MSUN
    axo.plot(xs, ys, color=c, lw=1.6,
             label=f"{p['name'].split()[-1]}  {a:.4f} AU  {m_e:.2f} M⊕  e={e:.2f}")
axo.plot(0, 0, marker="*", color="orange", ms=18, label="Barnard's Star")
axo.set_aspect("equal")
axo.set_xlabel("AU"); axo.set_ylabel("AU")
axo.set_title("Orbits (top-down)")
axo.legend(loc="upper right", fontsize=8)
axo.grid(alpha=0.25)

# --- panel 2: eccentricity vs time ---
for p, c in zip(planets, colors):
    s = sorted(series.get(p["name"], []))
    if s:
        axe.plot([t / 1000 for t, _ in s], [ev for _, ev in s],
                 color=c, lw=1.2, label=p["name"].split()[-1])
axe.set_xlabel("time (kyr)"); axe.set_ylabel("eccentricity")
axe.set_title("Eccentricity evolution (10⁴ yr)")
axe.set_ylim(bottom=0)
axe.legend(loc="upper right", fontsize=8)
axe.grid(alpha=0.25)

j = summary["judgment"]
fig.suptitle(f"{summary['system']} — {j['overall']}  "
             f"(MEGNO {summary['integration']['megno_final']:.0f}, "
             f"hottest ecc: {j['ecc_class_max']})", fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.96])
out = RESULTS / f"{label}_orbits.png"
fig.savefig(out, dpi=130)
print(f"wrote {out}")
