# Polyphemus 위성계 안정성 런 시각화 — 위성별 궤도/이심률/장반경드리프트/경사 4패널 PNG.
"""Visualize a moon-system stability run (Polyphemus / Alpha Centauri A b).

Unlike plot_orbits.py (planet-only, MEGNO-required), this plots the hypothetical
MOONS around their parent planet and tolerates leapfrog/trace runs (megno=None).

Reads  <dir>/<label>_summary.json  +  <dir>/<label>_timeseries.csv
Writes <dir>/<label>_moons.png

Usage: python3 scripts/plot_moons.py --dir results/_principia2000 [--label alpha_centauri]
"""
import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RJUP_KM = 71492.0
AU_KM = 1.495978707e8

ap = argparse.ArgumentParser()
ap.add_argument("--dir", required=True, type=Path, help="results dir holding the run")
ap.add_argument("--label", default="alpha_centauri")
args = ap.parse_args()

d = args.dir if args.dir.is_absolute() else (Path(__file__).resolve().parent.parent / args.dir)
summary = json.loads((d / f"{args.label}_summary.json").read_text())

moons = [h for h in summary["hypotheticals"] if h["type"] == "moon"]
moon_names = {m["name"] for m in moons}
parent_name = moons[0]["parent"]
j2 = summary.get("j2", {})
R_p = j2.get("r_eq_au", RJUP_KM / AU_KM) * AU_KM  # planet equatorial radius (km)

# per-moon time series: (t, a_km, e, inc_deg)
ts = defaultdict(list)
with (d / f"{args.label}_timeseries.csv").open() as f:
    for r in csv.DictReader(f):
        if r["body"] in moon_names:
            ts[r["body"]].append((float(r["t_yr"]), float(r["a_au"]) * AU_KM,
                                  float(r["e"]), float(r["inc_deg"])))

# initial inclination (deg) from first timeseries sample, for labels
inc0 = {name: sorted(s)[0][3] for name, s in ts.items()}

colors = plt.cm.plasma([0.12 + 0.76 * i / max(1, len(moons) - 1) for i in range(len(moons))])
cmap = {m["name"]: c for m, c in zip(moons, colors)}

fig, axs = plt.subplots(2, 2, figsize=(14, 11))
(axo, axe), (axa, axi) = axs

# --- panel 1: top-down moon orbits (initial, planet at focus) ---
fa = [i * 2 * math.pi / 400 for i in range(401)]
for m in moons:
    a = m["a_km"] / R_p
    e = m.get("e", 0.0)
    xs = [a * (1 - e * e) / (1 + e * math.cos(t)) * math.cos(t) for t in fa]
    ys = [a * (1 - e * e) / (1 + e * math.cos(t)) * math.sin(t) for t in fa]
    axo.plot(xs, ys, color=cmap[m["name"]], lw=1.6,
             label=f"{m['name']}  {m['a_km']/1000:.0f}k km"
                   f"  i={inc0.get(m['name'], 0):.0f}°")
axo.add_patch(plt.Circle((0, 0), 1.0, color="tan", alpha=0.7))  # planet (1 R_p)
axo.plot(0, 0, marker="+", color="k", ms=10)
axo.set_aspect("equal")
axo.set_xlabel("planet radii (R_p)"); axo.set_ylabel("R_p")
axo.set_title(f"Moon orbits (top-down, initial) — parent {parent_name}")
axo.legend(loc="upper right", fontsize=8)
axo.grid(alpha=0.25)

# --- panel 2: eccentricity vs time ---
for m in moons:
    s = sorted(ts[m["name"]])
    axe.plot([t for t, *_ in s], [e for _, _, e, _ in s],
             color=cmap[m["name"]], lw=1.2, label=m["name"])
axe.set_xlabel("time (yr)"); axe.set_ylabel("eccentricity")
axe.set_title("Eccentricity evolution")
axe.set_ylim(bottom=0)
axe.legend(loc="upper right", fontsize=8); axe.grid(alpha=0.25)

# --- panel 3: semi-major-axis drift Δa/a0 vs time ---
for m in moons:
    s = sorted(ts[m["name"]])
    a0 = s[0][1]
    axa.plot([t for t, *_ in s], [(a - a0) / a0 for _, a, _, _ in s],
             color=cmap[m["name"]], lw=1.2, label=m["name"])
axa.axhline(0, color="k", lw=0.6, alpha=0.4)
axa.set_xlabel("time (yr)"); axa.set_ylabel("Δa / a₀")
axa.set_title("Semi-major-axis drift (bounded ⇒ stable)")
axa.legend(loc="upper right", fontsize=8); axa.grid(alpha=0.25)

# --- panel 4: inclination vs time (rel. to parent orbital plane) ---
for m in moons:
    s = sorted(ts[m["name"]])
    axi.plot([t for t, *_ in s], [inc for _, _, _, inc in s],
             color=cmap[m["name"]], lw=1.2, label=m["name"])
axi.set_xlabel("time (yr)"); axi.set_ylabel("inclination (deg)")
axi.set_title("Inclination (simulation reference frame)")
axi.legend(loc="upper right", fontsize=8); axi.grid(alpha=0.25)

j = summary["judgment"]
integ = summary["integration"]
hill = summary.get("hill_track", {})
hill_str = ", ".join(f"{k.split()[-1]}:{v['frac_max']:.2f}"
                     for k, v in hill.items()) if hill else "n/a"
dt_min = integ["dt_yr"] * 365.25 * 24 * 60
fig.suptitle(
    f"{summary['system']} — verdict: {j['overall'].upper()}   "
    f"[{integ['integrator']}, dt={dt_min:.1f} min, "
    f"|ΔE/E|={integ['energy_relative_error']:.1e}]\n"
    f"J2={j2.get('J2', '–')}   max Hill-frac → {hill_str}",
    fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.95])
out = d / f"{args.label}_moons.png"
fig.savefig(out, dpi=130)
print(f"wrote {out}")
