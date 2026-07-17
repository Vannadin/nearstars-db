# 안정성 런 인터랙티브 4패널 뷰어 — Plotly HTML(범례 토글·호버·줌). plot_moons.py의 인터랙티브 짝.
"""Interactive 4-panel viewer for a stability run (Plotly, self-contained HTML).

Same data + center logic as plot_moons.py, but renders to an interactive HTML so
overlapping orbits can be read: click a body in the legend to toggle it across
ALL four panels, hover to read exact values, box-zoom / pan to separate tightly
packed inner bodies from a distant outer one.

Panels: top-down orbits (initial) · eccentricity(t) · Δa/a₀(t) · inclination(t).
Works for both hierarchy levels (planet-center moons / star-center planets).

Reads  <dir>/<label>_summary.json  +  <dir>/<label>_timeseries.csv
Writes <dir>/<label>_interactive.html   (Plotly from CDN; open in a browser)

Usage: python3 scripts/plot_interactive.py --dir results/_validation/alpha_centauri [--label alpha_centauri] [--center <body>]
"""
import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

RJUP_KM = 71492.0
AU_KM = 1.495978707e8

ap = argparse.ArgumentParser()
ap.add_argument("--dir", required=True, type=Path)
ap.add_argument("--label", default="alpha_centauri")
ap.add_argument("--center", default=None)
ap.add_argument("--max-points", type=int, default=2500,
                help="decimate each body's time series to at most this many points")
args = ap.parse_args()

d = args.dir if args.dir.is_absolute() else (Path(__file__).resolve().parent.parent / args.dir)
summary = json.loads((d / f"{args.label}_summary.json").read_text())

# ── center + orbiting set (same rule as plot_moons / animate_orbits) ──
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

# per-body time series: (t, a_disp, e, inc)
ts = defaultdict(list)
with (d / f"{args.label}_timeseries.csv").open() as f:
    for r in csv.DictReader(f):
        if r["body"] in name_set:
            ts[r["body"]].append((float(r["t_yr"]), float(r["a_au"]) * AU_KM / unit_km,
                                  float(r["e"]), float(r["inc_deg"])))
for n in names:
    ts[n].sort()


def decimate(seq, k):
    if len(seq) <= k:
        return seq
    step = len(seq) / k
    return [seq[int(i * step)] for i in range(k)]


# plasma palette — the project standard (matches the 3D viewer + the static
# plot_moons PNG). Kept identical for cross-tool consistency.
PALETTE = ["#7e03a8", "#b12a90", "#e16462", "#fca636", "#f0f921", "#0d0887", "#46039f"]
short = {n: n.split()[-1] for n in names}

traces = []
for i, n in enumerate(names):
    col = PALETTE[i % len(PALETTE)]
    s = decimate(ts[n], args.max_points)
    t = [r[0] for r in s]
    a0 = ts[n][0][1]

    # panel 1 (x/y): initial orbit ellipse — the one trace carrying the legend
    a, e = ts[n][0][1], ts[n][0][2]
    fa = [j * 2 * math.pi / 240 for j in range(241)]
    ox = [a * (1 - e * e) / (1 + e * math.cos(f)) * math.cos(f) for f in fa]
    oy = [a * (1 - e * e) / (1 + e * math.cos(f)) * math.sin(f) for f in fa]
    traces.append({"x": ox, "y": oy, "type": "scatter", "mode": "lines",
                   "name": short[n], "legendgroup": n, "line": {"color": col, "width": 2},
                   "hovertemplate": f"{short[n]}<br>%{{x:.4g}}, %{{y:.4g}} {unit}<extra></extra>"})
    # panel 2 (x2/y2): eccentricity
    traces.append({"x": t, "y": [r[2] for r in s], "type": "scattergl", "mode": "lines",
                   "name": short[n], "legendgroup": n, "showlegend": False,
                   "line": {"color": col, "width": 1}, "xaxis": "x2", "yaxis": "y2",
                   "hovertemplate": f"{short[n]}<br>t=%{{x:.0f}} yr<br>e=%{{y:.4f}}<extra></extra>"})
    # panel 3 (x3/y3): Δa/a₀
    traces.append({"x": t, "y": [(r[1] - a0) / a0 for r in s], "type": "scattergl", "mode": "lines",
                   "name": short[n], "legendgroup": n, "showlegend": False,
                   "line": {"color": col, "width": 1}, "xaxis": "x3", "yaxis": "y3",
                   "hovertemplate": f"{short[n]}<br>t=%{{x:.0f}} yr<br>Δa/a₀=%{{y:.2e}}<extra></extra>"})
    # panel 4 (x4/y4): inclination
    traces.append({"x": t, "y": [r[3] for r in s], "type": "scattergl", "mode": "lines",
                   "name": short[n], "legendgroup": n, "showlegend": False,
                   "line": {"color": col, "width": 1}, "xaxis": "x4", "yaxis": "y4",
                   "hovertemplate": f"{short[n]}<br>t=%{{x:.0f}} yr<br>i=%{{y:.2f}}°<extra></extra>"})

# central body marker in panel 1
cmark = ("star" if mode == "star" else "cross")
ccol = ("#e8b923" if mode == "star" else "#c9a06a")
traces.append({"x": [0], "y": [0], "type": "scatter", "mode": "markers",
               "name": center, "showlegend": False,
               "marker": {"symbol": cmark, "size": 16, "color": ccol},
               "hovertemplate": f"{center}<extra></extra>"})

j = summary["judgment"]
integ = summary["integration"]
megno = integ.get("megno_final")
dt_min = integ["dt_yr"] * 365.25 * 24 * 60
tspan = int(round(max(ts[names[0]][-1][0], 0)))
sub = (f"{integ['integrator']} · dt={dt_min:.1f} min · {tspan:,} yr · "
       f"|ΔE/E|={integ['energy_relative_error']:.1e}"
       + (f" · MEGNO={megno:.2f}" if megno is not None else " · MEGNO n/a (drift verdict)"))

# ── theme palettes (base layout = light; a button swaps to dark at runtime) ──
LIGHT = {"paper": "#ffffff", "plot": "#ffffff", "font": "#1a1a1a",
         "grid": "#dfe3ea", "zero": "#b8c0cc", "zero_hi": "#8a93a3",
         "sub": "#5a6473", "legend_bg": "rgba(255,255,255,.65)"}
DARK = {"paper": "#0a0c12", "plot": "#0a0c12", "font": "#cdd6e6",
        "grid": "#1c2436", "zero": "#1c2436", "zero_hi": "#3a4560",
        "sub": "#8a94a8", "legend_bg": "rgba(10,13,22,.6)"}

ANN = [
    f"Orbits (top-down, initial) — {'star' if mode=='star' else 'parent'} {center}",
    "Eccentricity",
    "Semi-major-axis drift Δa/a₀ (bounded ⇒ stable)",
    "Inclination (sim reference frame)",
]
ANN_POS = [(0.0, 1.0, "left"), (1.0, 1.0, "right"), (0.0, 0.44, "left"), (1.0, 0.44, "right")]


def build_layout(T):
    return {
        "title": {"text": f"{summary['system']} — {j['overall'].upper()}<br>"
                          f"<span style='font-size:12px;color:{T['sub']}'>{sub}</span>"},
        "paper_bgcolor": T["paper"], "plot_bgcolor": T["plot"],
        "font": {"color": T["font"], "size": 12},
        "hovermode": "closest", "showlegend": True,
        "legend": {"title": {"text": "click = toggle"}, "bgcolor": T["legend_bg"]},
        "margin": {"t": 70},
        "grid": {"rows": 2, "columns": 2, "pattern": "independent"},
        "xaxis": {"title": {"text": f"{unit}"}, "gridcolor": T["grid"], "zerolinecolor": T["zero"]},
        "yaxis": {"title": {"text": f"{unit}"}, "gridcolor": T["grid"], "zerolinecolor": T["zero"],
                  "scaleanchor": "x", "scaleratio": 1},
        "xaxis2": {"title": {"text": "time (yr)"}, "gridcolor": T["grid"], "zerolinecolor": T["zero"]},
        "yaxis2": {"title": {"text": "eccentricity"}, "gridcolor": T["grid"], "rangemode": "tozero", "zerolinecolor": T["zero"]},
        "xaxis3": {"title": {"text": "time (yr)"}, "gridcolor": T["grid"], "zerolinecolor": T["zero"]},
        "yaxis3": {"title": {"text": "Δa / a₀"}, "gridcolor": T["grid"], "zerolinecolor": T["zero_hi"]},
        "xaxis4": {"title": {"text": "time (yr)"}, "gridcolor": T["grid"], "zerolinecolor": T["zero"]},
        "yaxis4": {"title": {"text": "inclination (deg)"}, "gridcolor": T["grid"], "zerolinecolor": T["zero"]},
        "annotations": [
            {"text": txt, "x": x, "y": y, "xref": "paper", "yref": "paper", "showarrow": False,
             "xanchor": anchor, "font": {"size": 12, "color": T["font"]}}
            for txt, (x, y, anchor) in zip(ANN, ANN_POS)
        ],
    }


layout = build_layout(LIGHT)
# relayout patch to switch themes at runtime (flat keys Plotly.relayout understands)
def theme_patch(T):
    p = {"paper_bgcolor": T["paper"], "plot_bgcolor": T["plot"], "font.color": T["font"],
         "legend.bgcolor": T["legend_bg"],
         "title.text": f"{summary['system']} — {j['overall'].upper()}<br>"
                       f"<span style='font-size:12px;color:{T['sub']}'>{sub}</span>"}
    for ax in ("xaxis", "yaxis", "xaxis2", "yaxis2", "xaxis3", "yaxis3", "xaxis4", "yaxis4"):
        p[f"{ax}.gridcolor"] = T["grid"]
        p[f"{ax}.zerolinecolor"] = T["zero_hi"] if ax == "yaxis3" else T["zero"]
    for i in range(len(ANN)):
        p[f"annotations[{i}].font.color"] = T["font"]
    return p

THEMES = {"light": theme_patch(LIGHT), "dark": theme_patch(DARK)}

HTML = """<!-- __TITLE__ : 안정성 런 인터랙티브 4패널 (자동 생성, plot_interactive.py). Plotly CDN. -->
<!doctype html><meta charset="utf-8"><title>__TITLE__</title>
<style>
  html,body{margin:0;height:100%;background:#ffffff;transition:background .2s}
  body.dark{background:#0a0c12}
  #p{width:100%;height:100vh}
  #theme{position:fixed;top:8px;right:12px;z-index:10;background:#eef1f6;color:#1a1a1a;
    border:1px solid #c8cfdb;border-radius:6px;padding:5px 11px;cursor:pointer;font:13px system-ui}
  body.dark #theme{background:#1c2740;color:#cdd6e6;border-color:#2c3a5a}
</style>
<script src="https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.2/plotly.min.js"></script>
<button id="theme">🌙 Dark</button>
<div id="p"></div>
<script>
const THEMES = __THEMES__;
Plotly.newPlot('p', __TRACES__, __LAYOUT__,
  {responsive:true, displaylogo:false, scrollZoom:true,
   modeBarButtonsToRemove:['select2d','lasso2d']});
let dark=false;
document.getElementById('theme').onclick=function(){
  dark=!dark;
  document.body.classList.toggle('dark',dark);
  this.textContent = dark ? '☀️ Light' : '🌙 Dark';
  Plotly.relayout('p', dark ? THEMES.dark : THEMES.light);
};
</script>
"""
title = f"{summary['system']} — interactive orbit analysis"
html = (HTML.replace("__TRACES__", json.dumps(traces))
            .replace("__LAYOUT__", json.dumps(layout))
            .replace("__THEMES__", json.dumps(THEMES))
            .replace("__TITLE__", title))
out = d / f"{args.label}_interactive.html"
out.write_text(html)
print(f"wrote {out}  ({mode}-center '{center}', {len(names)} bodies, unit {unit})")
