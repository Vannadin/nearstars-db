# 안정성 런 인터랙티브 4패널 뷰어 — Plotly HTML(범례 토글·호버·줌). plot_moons.py의 인터랙티브 짝.
"""Interactive 4-panel viewer for a stability run (Plotly, self-contained HTML).

Same data + center logic as plot_moons.py, but renders to an interactive HTML so
overlapping orbits can be read: click a body in the legend to toggle it across
ALL four panels, hover to read exact values, box-zoom / pan to separate tightly
packed inner bodies from a distant outer one.

Panels: top-down orbits (initial) · eccentricity(t) · Δa/a₀(t) · inclination(t).
Works for both hierarchy levels (planet-center moons / star-center planets).

Sampling slider: the FULL recorded series is embedded and a 1/1 · 1/2 · 1/4 … slider
decimates it client-side. Coarse levels keep each bin's min AND max point (not every
Nth sample), so sliding down yields an honest envelope instead of aliased noise, and
sliding up reveals the precession waveform where the recording is dense enough.
A body that goes unbound (e ≥ 1 or a ≤ 0) is clipped at the escape: the hyperbolic
garbage would otherwise stretch the e/Δa axes by ~1e8 and flatten everyone else.
The escape moment is drawn as a dashed line in the time panels.

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

# clip each body at its escape (e ≥ 1 or a ≤ 0): the post-escape hyperbolic elements
# are numerically meaningless and one unbound body otherwise dictates every axis range.
escape_t = {}
for n in names:
    for k, (_, a_disp, e, _) in enumerate(ts[n]):
        if e >= 1.0 or a_disp <= 0.0:
            escape_t[n] = ts[n][k][0]
            ts[n] = ts[n][:k]
            break

# full series per body, embedded for the client-side sampling slider
SERIES = {}
for n in names:
    a0 = ts[n][0][1]
    SERIES[n] = {
        "t": [round(r[0], 2) for r in ts[n]],
        "e": [round(r[2], 6) for r in ts[n]],
        "da": [round((r[1] - a0) / a0, 8) for r in ts[n]],
        "inc": [round(r[3], 4) for r in ts[n]],
    }

# plasma palette — the project standard (matches the 3D viewer + the static
# plot_moons PNG). Kept identical for cross-tool consistency.
PALETTE = ["#7e03a8", "#b12a90", "#e16462", "#fca636", "#f0f921", "#0d0887", "#46039f"]
short = {n: n.split()[-1] for n in names}

traces = []
for i, n in enumerate(names):
    col = PALETTE[i % len(PALETTE)]

    # panel 1 (x/y): initial orbit ellipse — the one trace carrying the legend
    a, e = ts[n][0][1], ts[n][0][2]
    fa = [j * 2 * math.pi / 240 for j in range(241)]
    ox = [a * (1 - e * e) / (1 + e * math.cos(f)) * math.cos(f) for f in fa]
    oy = [a * (1 - e * e) / (1 + e * math.cos(f)) * math.sin(f) for f in fa]
    traces.append({"x": ox, "y": oy, "type": "scatter", "mode": "lines",
                   "name": short[n], "legendgroup": n, "line": {"color": col, "width": 2},
                   "hovertemplate": f"{short[n]}<br>%{{x:.4g}}, %{{y:.4g}} {unit}<extra></extra>"})
    # panels 2-4 (e / Δa/a₀ / inclination): data arrives from SERIES via the
    # sampling slider (applyStride fills x/y right after newPlot), so the traces
    # start empty — embedding them here too would double the page size.
    for ax, hover in (("2", "e=%{y:.4f}"), ("3", "Δa/a₀=%{y:.2e}"), ("4", "i=%{y:.2f}°")):
        traces.append({"x": [], "y": [], "type": "scattergl", "mode": "lines",
                       "name": short[n], "legendgroup": n, "showlegend": False,
                       "line": {"color": col, "width": 1}, "xaxis": f"x{ax}", "yaxis": f"y{ax}",
                       "hovertemplate": f"{short[n]}<br>t=%{{x:.0f}} yr<br>{hover}<extra></extra>"})

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
tspan = int(round(max(ts[n][-1][0] for n in names)))
sub = (f"{integ['integrator']} · dt={dt_min:.1f} min · {tspan:,} yr · "
       f"|ΔE/E|={integ['energy_relative_error']:.1e}"
       + (f" · MEGNO={megno:.2f}" if megno is not None else " · MEGNO n/a (drift verdict)"))

# ── theme palettes (base layout = light; the page swaps to dark to match the reader) ──
LIGHT = {"paper": "#ffffff", "plot": "#ffffff", "font": "#1a1a1a",
         "grid": "#dfe3ea", "zero": "#b8c0cc", "zero_hi": "#8a93a3",
         "sub": "#5a6473", "legend_bg": "rgba(255,255,255,.65)"}
DARK = {"paper": "#06070a", "plot": "#06070a", "font": "rgba(255,255,255,.82)",
        "grid": "rgba(255,255,255,.09)", "zero": "rgba(255,255,255,.09)", "zero_hi": "rgba(255,255,255,.18)",
        "sub": "rgba(255,255,255,.52)", "legend_bg": "rgba(10,12,18,.6)"}

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
        ] + [
            # escape labels keep the body's own color so they read in both themes
            {"text": f"✗ {short[n]} unbound", "x": t_esc, "xref": "x2",
             "y": 1, "yref": "y2 domain", "yanchor": "bottom", "showarrow": False,
             "font": {"size": 11, "color": PALETTE[names.index(n) % len(PALETTE)]}}
            for n, t_esc in escape_t.items()
        ],
        "shapes": [
            {"type": "line", "x0": t_esc, "x1": t_esc, "xref": f"x{ax}",
             "y0": 0, "y1": 1, "yref": f"y{ax} domain",
             "line": {"color": PALETTE[names.index(n) % len(PALETTE)],
                      "width": 1, "dash": "dot"}}
            for n, t_esc in escape_t.items() for ax in (2, 3, 4)
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
<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>__TITLE__</title>
<style>
  html,body{margin:0;height:100%;background:#ffffff;transition:background .2s}
  @media (max-width:700px){
    nav{font-size:13px !important}
    nav a{min-height:38px;display:inline-flex;align-items:center;padding:0 6px}
    /* plotly 자체 모드바도 터치 규격으로 */
    .modebar-btn{min-width:38px !important;min-height:38px !important}
    .modebar-btn svg{transform:scale(1.15)}
  }
:focus-visible { outline:2px solid #7aa8ff; outline-offset:2px; border-radius:4px }
@media (prefers-color-scheme:light) {
  html.ns-light-ok :focus-visible { outline-color:#2f66d8 } }
@media (prefers-reduced-motion:reduce) {
  *, *::before, *::after { animation-duration:.01ms !important;
    animation-iteration-count:1 !important; transition-duration:.01ms !important;
    scroll-behavior:auto !important } }
  body.dark{background:#06070a}
  /* right-aligned so the published pages' nav pill (injected top-left by
     publish_viewer) never covers the control */
  #bar{display:flex;align-items:center;justify-content:flex-end;gap:10px;height:40px;
       padding:0 14px;font:12px system-ui,sans-serif;color:#5a6473;user-select:none}
  body.dark #bar{color:rgba(255,255,255,.6)}
  #bar input{flex:0 1 220px;accent-color:#b12a90}
  #p{width:100%;height:calc(100vh - 40px);height:calc(100dvh - 40px)}
</style>
<script src="https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.2/plotly.min.js"></script>
<div id="bar">
  <span>sampling</span>
  <input id="stride" type="range" min="0" max="0" step="1" value="0"
         aria-label="display sampling density">
  <span id="strideLabel"></span>
</div>
<div id="p"></div>
<script>
const THEMES = __THEMES__;
const SERIES = __SERIES__;
const NAMES = __NAMES__;
Plotly.newPlot('p', __TRACES__, __LAYOUT__,
  {responsive:true, displaylogo:false, scrollZoom:true,
   modeBarButtonsToRemove:['select2d','lasso2d']});

// ── sampling slider: decimate client-side, keeping each TIME bin's min AND max ──
// A plain every-Nth stride would re-alias the precession into sawtooth noise, and
// index-based bins would let a dense head (animation cadence) swallow the whole bin
// budget while the coarse tail collapses to a few segments. Binning by TIME keeps
// the envelope honest across mixed cadences: dense stretches compress, sparse
// stretches pass through unchanged. Slider left = full recorded resolution
// (waveform), right = coarsest envelope.
function minmaxBinsByTime(t, y, nbins){
  if (t.length <= 2 * nbins) return [t, y];
  const t0 = t[0], w = (t[t.length - 1] - t0) / nbins || 1;
  const xt = [], xy = [];
  let s = 0;
  for (let b = 0; b < nbins && s < t.length; b++){
    const end = t0 + (b + 1) * w;
    let iMin = s, iMax = s, j = s;
    for (; j < t.length && (t[j] <= end || b === nbins - 1); j++){
      if (y[j] < y[iMin]) iMin = j;
      if (y[j] > y[iMax]) iMax = j;
    }
    s = j;
    const i1 = Math.min(iMin, iMax), i2 = Math.max(iMin, iMax);
    xt.push(t[i1]); xy.push(y[i1]);
    if (i2 !== i1){ xt.push(t[i2]); xy.push(y[i2]); }
  }
  return [xt, xy];
}
const nFull = Math.max(...NAMES.map(n => SERIES[n].t.length));
// level 0 = everything; deeper levels halve the time-bin count down to 256.
// Levels that would not actually reduce the series are dropped up front.
const LEVELS = [Infinity].concat(
  [8192, 4096, 2048, 1024, 512, 256].filter(b => 2 * b < nFull));
function applyLevel(k){
  const nbins = LEVELS[k];
  const xs = [], ys = [], idx = [];
  NAMES.forEach((n, i) => {
    const S = SERIES[n];
    [["e", 1], ["da", 2], ["inc", 3]].forEach(([key, off]) => {
      const [xt, xy] = nbins === Infinity ? [S.t, S[key]]
                                          : minmaxBinsByTime(S.t, S[key], nbins);
      xs.push(xt); ys.push(xy); idx.push(4 * i + off);
    });
  });
  Plotly.restyle('p', {x: xs, y: ys}, idx);
}
const slider = document.getElementById('stride');
const label = document.getElementById('strideLabel');
slider.max = LEVELS.length - 1;
slider.value = Math.min(1, LEVELS.length - 1);
function onStride(){
  const k = Number(slider.value);
  label.textContent = k === 0
    ? `all ${nFull.toLocaleString()} samples`
    : `min/max envelope · ${LEVELS[k].toLocaleString()} time bins`;
  applyLevel(k);
}
slider.addEventListener('input', onStride);
onStride();
// The rest of the site follows the reader's prefers-color-scheme, so this page does
// too rather than asking again with a button. It also follows a live change, which a
// manual toggle could not.
const mq = matchMedia('(prefers-color-scheme: dark)');
function applyTheme(){
  document.body.classList.toggle('dark', mq.matches);
  Plotly.relayout('p', mq.matches ? THEMES.dark : THEMES.light);
}
applyTheme();
mq.addEventListener('change', applyTheme);
</script>
"""
title = f"{summary['system']} — interactive orbit analysis"
html = (HTML.replace("__TRACES__", json.dumps(traces))
            .replace("__LAYOUT__", json.dumps(layout))
            .replace("__THEMES__", json.dumps(THEMES))
            .replace("__SERIES__", json.dumps(SERIES))
            .replace("__NAMES__", json.dumps(names))
            .replace("__TITLE__", title))
out = d / f"{args.label}_interactive.html"
out.write_text(html)
print(f"wrote {out}  ({mode}-center '{center}', {len(names)} bodies, unit {unit})")
