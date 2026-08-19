# 안정성 런 4패널 시각화(궤도·이심률·Δa드리프트·경사) — 위성계·행성계 공통, plot_orbits.py 대체.
"""Visualize a stability run as a 4-panel PNG: top-down orbits, e(t), Δa/a₀(t),
inclination(t). Works for BOTH hierarchy levels from sim output alone:

  - planet-center (moons around a parent planet, unit = R_p), or
  - star-center   (planets around the star, unit = AU).

Center is chosen by --center; default is the moon parent if the run has moons,
else the star. Unlike plot_orbits.py (planet-only, MEGNO-required) it tolerates
leapfrog/trace runs (megno=None).

Reads  <dir>/<label>_summary.json  +  <dir>/<label>_timeseries.csv
Writes <dir>/<label>_orbits.png  (or <label>_orbits_light.png with --theme light,
so both themes can sit side by side for a <picture> swap on the site).
--highlight NAME draws that body last and dims the rest, and names the output
<label>_orbits_<slug>.png — the per-body cut a board page attaches to its orbit row,
where the point is that body's curve rather than the system's.

Usage: python3 scripts/plot_moons.py --dir results/_principia2000_dense [--label alpha_centauri] [--center "TRAPPIST-1"] [--theme light]
"""
import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts" / "pipeline"))
from _naming import to_url_slug   # noqa: E402  — slugs are canonical, never re-derived

import nsplot
from nsplot import apply_theme, series_colors

RJUP_KM = 71492.0
AU_KM = 1.495978707e8

ap = argparse.ArgumentParser()
ap.add_argument("--dir", required=True, type=Path, help="results dir holding the run")
ap.add_argument("--label", default="alpha_centauri")
ap.add_argument("--center", default=None,
                help="central body name. Default: the moon parent if the run has "
                     "moons, else the star. Pass the star name to plot planets.")
ap.add_argument("--theme", choices=["dark", "light"], default="dark",
                help="site palette to draw in; light writes <label>_orbits_light.png")
ap.add_argument("--highlight", default=None,
                help="draw this body on top of the others (and dim them); writes a "
                     "per-body <label>_orbits_<slug>.png")
args = ap.parse_args()

apply_theme(args.theme)

d = args.dir if args.dir.is_absolute() else (Path(__file__).resolve().parent.parent / args.dir)
summary = json.loads((d / f"{args.label}_summary.json").read_text())

# ── resolve the central body and the orbiting set (same rule as animate_orbits) ──
star_name = summary["star"]["name"]
moons_all = [h for h in summary.get("hypotheticals", []) if h.get("type") == "moon"]
if args.center:
    center = args.center
elif moons_all:
    center = moons_all[0]["parent"]
else:
    center = star_name

if center != star_name:
    mode, unit = "planet", "R_p"
    bodies_meta = [m for m in moons_all if m["parent"] == center]
    unit_km = summary.get("j2", {}).get("r_eq_au", RJUP_KM / AU_KM) * AU_KM
else:
    mode, unit = "star", "AU"
    bodies_meta = list(summary.get("planets", []))
    unit_km = AU_KM

names = [b["name"] for b in bodies_meta]
name_set = set(names)
if not names:
    raise SystemExit(f"no bodies orbit '{center}' in {args.label} — nothing to plot")

# per-body time series: (t, a_disp, e, inc_deg) with a in display units
ts = defaultdict(list)
with (d / f"{args.label}_timeseries.csv").open() as f:
    for r in csv.DictReader(f):
        if r["body"] in name_set:
            ts[r["body"]].append((float(r["t_yr"]), float(r["a_au"]) * AU_KM / unit_km,
                                  float(r["e"]), float(r["inc_deg"])))

# clip each body at its escape (e ≥ 1 or a ≤ 0) — same policy as plot_interactive:
# post-escape hyperbolic elements are meaningless and would set every panel's axis range.
escape_t = {}
for n in names:
    s = sorted(ts[n])
    for k, (_, a_disp, e, _) in enumerate(s):
        if e >= 1.0 or a_disp <= 0.0:
            escape_t[n] = s[k][0]
            s = s[:k]
            break
    ts[n] = s

inc0 = {n: sorted(s)[0][3] for n, s in ts.items()}      # initial inclination (deg), labels
a0disp = {n: sorted(s)[0][1] for n, s in ts.items()}     # initial a (display units)

cmap = {n: c for n, c in zip(names, series_colors(len(names)))}
# Plot order decides who is on top. With the highlight set, everyone else is drawn
# first and faded, so the body whose page this is reads at a glance instead of being
# buried under whichever body happened to come last in the run.
hi = args.highlight if args.highlight in names else None
if args.highlight and hi is None:
    # Writing anyway would land on <label>_orbits.png and quietly replace the canonical
    # system panel with an unhighlighted re-render. Nothing to cut here, so stop.
    print(f"[skip] --highlight {args.highlight!r} not in this view: {names}")
    raise SystemExit(0)
order = ([n for n in names if n != hi] + [hi]) if hi else list(names)
alpha = {n: (0.32 if hi and n != hi else 1.0) for n in names}
width = {n: (2.1 if n == hi else 1.2) for n in names}
short = {n: n.split()[-1] for n in names}                # legend-friendly short name

fig, axs = plt.subplots(2, 2, figsize=(14, 11))
(axo, axe), (axa, axi) = axs

# --- panel 1: top-down orbits (initial elements, central body at focus) ---
fa = [i * 2 * math.pi / 400 for i in range(401)]
for n in order:
    a, e = a0disp[n], sorted(ts[n])[0][2]
    xs = [a * (1 - e * e) / (1 + e * math.cos(t)) * math.cos(t) for t in fa]
    ys = [a * (1 - e * e) / (1 + e * math.cos(t)) * math.sin(t) for t in fa]
    lab = (f"{short[n]}  {a:.4f} {unit}  i={inc0.get(n, 0):.0f}°" if mode == "star"
           else f"{short[n]}  {a:.1f} {unit}  i={inc0.get(n, 0):.0f}°")
    axo.plot(xs, ys, color=cmap[n], lw=width[n] + 0.4, alpha=alpha[n], label=lab)
if mode == "planet":
    axo.add_patch(plt.Circle((0, 0), 1.0, color="tan", alpha=0.7))       # planet at 1 R_p
    axo.plot(0, 0, marker="+", color=nsplot.FG_DIM, ms=10)
else:
    axo.plot(0, 0, marker="*", color="#e8b923", ms=20)                    # star at focus
axo.set_aspect("equal")
axo.set_xlabel(unit); axo.set_ylabel(unit)
axo.set_title(f"Orbits (top-down, initial) — {'parent' if mode == 'planet' else 'star'} {center}")
axo.legend(loc="upper right", fontsize=8)
axo.grid(alpha=0.25)

# --- panel 2: eccentricity vs time ---
for n in order:
    s = sorted(ts[n])
    axe.plot([t for t, *_ in s], [e for _, _, e, _ in s], color=cmap[n], lw=width[n],
             alpha=alpha[n], label=short[n])
axe.set_xlabel("time (yr)"); axe.set_ylabel("eccentricity")
axe.set_title("Eccentricity evolution")
# explicit headroom: a constant e (2-body Kepler) otherwise sits exactly on the
# axis top and renders invisible
e_max = max(e for s in ts.values() for _, _, e, _ in s)
axe.set_ylim(bottom=0, top=max(e_max * 1.15, 0.01))
axe.legend(loc="upper right", fontsize=8); axe.grid(alpha=0.25)

# --- panel 3: semi-major-axis drift Δa/a0 vs time ---
for n in order:
    s = sorted(ts[n])
    a0 = s[0][1]
    axa.plot([t for t, *_ in s], [(a - a0) / a0 for _, a, _, _ in s],
             color=cmap[n], lw=width[n], alpha=alpha[n], label=short[n])
axa.axhline(0, color=nsplot.FG_DIM, lw=0.6, alpha=0.6)
axa.set_xlabel("time (yr)"); axa.set_ylabel("Δa / a₀")
axa.set_title("Semi-major-axis drift (bounded ⇒ stable)")
axa.legend(loc="upper right", fontsize=8); axa.grid(alpha=0.25)

# --- panel 4: inclination vs time (simulation reference frame) ---
for n in order:
    s = sorted(ts[n])
    axi.plot([t for t, *_ in s], [inc for _, _, _, inc in s],
             color=cmap[n], lw=width[n], alpha=alpha[n], label=short[n])
axi.set_xlabel("time (yr)"); axi.set_ylabel("inclination (deg)")
axi.set_title("Inclination (simulation reference frame)")
# no offset notation, and pad near-constant inclinations: a body pinned to 1e-5 deg
# otherwise renders as a fake quantization step under matplotlib's offset scaling
axi.ticklabel_format(useOffset=False, axis="y")
incs = [i for s in ts.values() for _, _, _, i in s]
if max(incs) - min(incs) < 0.5:
    mid = (max(incs) + min(incs)) / 2
    axi.set_ylim(mid - 0.5, mid + 0.5)
axi.legend(loc="upper right", fontsize=8); axi.grid(alpha=0.25)

# escape markers on the time panels (same dashed convention as the interactive viewer)
for n, t_esc in escape_t.items():
    for ax in (axe, axa, axi):
        ax.axvline(t_esc, color=cmap[n], lw=0.9, ls=":", alpha=0.8)
    axe.annotate(f"✗ {short[n]} unbound", (t_esc, 1.0), xycoords=("data", "axes fraction"),
                 ha="left", va="bottom", fontsize=7, color=cmap[n])

j = summary["judgment"]
integ = summary["integration"]
hill = summary.get("hill_track", {})
dt_min = integ["dt_yr"] * 365.25 * 24 * 60
line2 = (f"unit={unit} · center={center}"
         + (f"   max Hill-frac → " + ", ".join(f"{k.split()[-1]}:{v['frac_max']:.2f}"
                                                for k, v in hill.items())
            if hill else ""))
fig.suptitle(
    f"{summary['system']} — verdict: {j['overall'].upper()}   "
    f"[{integ['integrator']}, dt={dt_min:.1f} min, "
    f"|ΔE/E|={integ['energy_relative_error']:.1e}]\n{line2}",
    fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.95])
stem = f"{args.label}_orbits"
if hi:
    stem += "_" + to_url_slug(hi)
out = d / (f"{stem}.png" if args.theme == "dark" else f"{stem}_light.png")
fig.savefig(out, dpi=130)
print(f"wrote {out}  ({mode}-center '{center}', {len(names)} bodies, unit {unit})")
