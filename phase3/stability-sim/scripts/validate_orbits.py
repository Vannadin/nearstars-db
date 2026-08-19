# 궤도 검증 세트 드라이버 — 매니페스트의 "2방식 × 계층" 매트릭스를 전 시스템에 실행하고 페이지 생성.
"""Run the two-method orbit-validation matrix from validation-manifest.yaml.

The validation contract (STABILITY_REPORT.md) requires every shipping system to be
integrated **both** ways on **each** hierarchy it has:

    accurate  IAS15 (or TRACE) + MEGNO   — physics baseline, long horizon
    leapfrog  fixed 10-min step          — Principia's real ephemeris step, play window

This was executed by hand on α Cen. Here the matrix is data: for each manifest system
the driver expands the cells, runs any that are missing, renders the 4-panel PNG + the
interactive HTML, and generates docs/phase4/orbit-viewers/<slug>-validation/index.html
plus the validation index.

Two things are derived rather than copied from α Cen:
  * the accurate horizon, from `long_inner_orbits` × the system's own innermost period
    (α Cen's 10^8 yr is 5.2e7 inner orbits; the same orbit count is ~7.3e5 yr at Proxima).
  * the planetary rows' folded moon mass, summed from the hypotheticals per parent.

A cell is skipped when its results already exist AND reach the manifest horizon — the
accurate cells cost hours, so freshness is judged on the run itself rather than on file
mtimes. Raising `long_inner_orbits` therefore marks the affected cells stale instead of
silently letting an under-length run stand. Use --force to re-run regardless.

Usage:
  python scripts/validate_orbits.py                      # every manifest system, skip existing
  python scripts/validate_orbits.py --systems proxima_cen
  python scripts/validate_orbits.py --cells planets_leapfrog
  python scripts/validate_orbits.py --force              # re-run even if results exist
  python scripts/validate_orbits.py --jobs 6             # run up to 6 cells concurrently
  python scripts/validate_orbits.py --pages-only         # regenerate the HTML from existing runs
  python scripts/validate_orbits.py --dry-run            # print the plan (with horizons) and stop

REBOUND is single-threaded per simulation (no OpenMP in this build, and these integrators
are serial anyway), and every cell writes its own directory, so cells are embarrassingly
parallel — `--jobs N` runs N at a time, one core each. Each parallel cell logs to
`<cell-dir>/run.log` instead of the terminal, since interleaved progress is unreadable.
"""
import argparse
import csv
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import yaml

SIM = Path(__file__).resolve().parent.parent            # phase3/stability-sim
ROOT = SIM.parent.parent                                 # repo root
SCRIPTS = SIM / "scripts"
MANIFEST = SIM / "validation-manifest.yaml"
RESULTS = SIM / "results" / "_validation"
GALLERY = ROOT / "docs/phase4/orbit-viewers"
PY = sys.executable

sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(ROOT / "scripts" / "pipeline"))
import run as runmod                                     # noqa: E402  (SYSTEMS + build)
from load import MSUN_KG, MEARTH_KG                       # noqa: E402
from _nav import global_bar                               # noqa: E402


# ---------------------------------------------------------------- cell expansion

def _acen_kwargs(args):
    """Pull the --acen-* overrides back out of a manifest arg list.

    The binary loader needs them to build the same system the cells run, which is how
    we get the innermost period the horizon is derived from.
    """
    keys = {"--acen-a-au": "acen_a", "--acen-e": "acen_e", "--acen-incl-deg": "acen_incl"}
    out = {}
    for flag, key in keys.items():
        if flag in args:
            out[key] = float(args[args.index(flag) + 1])
    return out


def _build(system, args, hyp_path=None):
    return runmod.build(system, hyp_path, **_acen_kwargs(args))


def fold_moon_masses(system, args, hyp_path):
    """`--set PARENT.mass_mearth=...` for each planet that carries moons.

    The planetary hierarchy drops the moons and folds their mass into the parent — the
    standard way to avoid the inner-moon step limit on a long run.
    """
    _, meta = _build(system, args, hyp_path)
    moons = {}
    for h in meta["hypotheticals"]:
        if h.get("type") == "moon":
            moons[h["parent"]] = moons.get(h["parent"], 0.0) + h["mass_msun"]
    out = []
    for p in meta["planets"]:
        if p["name"] in moons:
            folded = (p["mass_msun"] + moons[p["name"]]) * MSUN_KG / MEARTH_KG
            out += ["--set", f"{p['name']}.mass_mearth={folded:.6f}"]
    return out


def inner_period_yr(system, args, hyp_path=None):
    """Innermost orbital period about its true primary — the unit the horizon counts in."""
    sim, meta = _build(system, args, hyp_path)
    star = sim.particles[0]
    periods = []
    for pm in meta["planets"]:
        orb = sim.particles[pm["name"]].orbit(primary=star)
        if 0 < orb.a < 1e6:
            periods.append(2 * math.pi * math.sqrt(orb.a ** 3 / (sim.G * star.m)))
    for h in meta.get("hypotheticals", []):
        primary = sim.particles[h["parent"]]
        orb = sim.particles[h["name"]].orbit(primary=primary)
        if 0 < orb.a < 1e6:
            periods.append(2 * math.pi * math.sqrt(orb.a ** 3 / (sim.G * primary.m)))
    return min(periods) if periods else 1.0


def expand(system, cfg, defaults):
    """The system's matrix cells: (planets | moons) × (leapfrog | accurate)."""
    common = list(cfg.get("args", []))
    moons = cfg.get("moons")
    hyp = SIM / moons["hypotheticals"] if moons else None
    accurate = cfg.get("accurate_integrator", defaults["accurate_integrator"])
    play = float(cfg.get("play_window_years", defaults["play_window_years"]))
    snaps = int(cfg.get("snapshots", defaults["snapshots"]))

    planet_args = common + (fold_moon_masses(system, common, hyp) if moons else [])
    if cfg.get("long_years") is not None:
        long_years = float(cfg["long_years"])
    else:
        orbits = float(cfg.get("long_inner_orbits", defaults["long_inner_orbits"]))
        long_years = orbits * inner_period_yr(system, planet_args)

    anim_years = float(cfg.get("anim_years", defaults["anim_years"]))
    cells = [
        {"key": "planets_leapfrog", "hierarchy": "planets", "method": "leapfrog",
         "integrator": "leapfrog", "dt_minutes": float(defaults["dt_minutes"]),
         "years": play, "snapshots": snaps, "args": planet_args,
         "anim_years": anim_years},
        {"key": "planets_accurate", "hierarchy": "planets", "method": "accurate",
         "integrator": accurate, "dt_minutes": None,
         "years": long_years, "snapshots": snaps, "args": planet_args},
    ]
    if moons:
        margs = common + list(moons.get("args", []))
        myears = float(moons.get("years", defaults["moon_years"]))
        cells += [
            {"key": "moons_leapfrog", "hierarchy": "moons", "method": "leapfrog",
             "integrator": "leapfrog", "dt_minutes": float(defaults["dt_minutes"]),
             "years": play, "snapshots": snaps, "args": margs, "hypotheticals": hyp,
             "anim_years": anim_years},
            {"key": "moons_accurate", "hierarchy": "moons", "method": "accurate",
             "integrator": accurate, "dt_minutes": None,
             "years": myears, "snapshots": snaps, "args": margs, "hypotheticals": hyp},
        ]
    return cells


# ---------------------------------------------------------------- running

def cell_dir(system, cell):
    return RESULTS / system / cell["key"]


def reached_years(system, cell):
    """How far the stored run actually got, or None if there is no run."""
    d = cell_dir(system, cell)
    if not (d / f"{system}_summary.json").exists():
        return None
    ts = d / f"{system}_timeseries.csv"
    if not ts.exists():
        return None
    with ts.open() as f:
        return max(float(r["t_yr"]) for r in csv.DictReader(f))


def cell_state(system, cell):
    """'run' (nothing stored) | 'stale' (stored run is short of the manifest horizon) | 'have'."""
    got = reached_years(system, cell)
    if got is None:
        return "run", None
    return ("have" if got >= cell["years"] * 0.99 else "stale"), got


def cell_cmd(system, cell, out_dir):
    cmd = [PY, str(SCRIPTS / "run.py"), "--system", system,
           "--integrator", cell["integrator"],
           "--years", repr(cell["years"]), "--snapshots", str(cell["snapshots"]),
           "--out-dir", str(out_dir)]
    if cell["dt_minutes"] is not None:
        cmd += ["--dt-minutes", str(cell["dt_minutes"])]
    if cell.get("hypotheticals"):
        cmd += ["--hypotheticals", str(cell["hypotheticals"])]
    return cmd + cell["args"]


def run_cells(jobs_list, jobs):
    """Run the queued cells, at most `jobs` at a time. One core each.

    Serial runs stream progress to the terminal as before; parallel ones go to
    <cell-dir>/run.log, because N interleaved progress streams are unreadable.
    """
    failed = []
    if jobs <= 1:
        for system, cell, out_dir in jobs_list:
            print(f"  ▶ {system} / {cell['key']}")
            if subprocess.run(cell_cmd(system, cell, out_dir)).returncode != 0:
                failed.append((system, cell["key"]))
        return failed

    queue, running = list(jobs_list), []
    while queue or running:
        while queue and len(running) < jobs:
            system, cell, out_dir = queue.pop(0)
            log = (out_dir / "run.log").open("w")
            print(f"  ▶ {system} / {cell['key']}  → {out_dir / 'run.log'}")
            running.append((system, cell,
                            subprocess.Popen(cell_cmd(system, cell, out_dir),
                                             stdout=log, stderr=subprocess.STDOUT), log))
        system, cell, proc, log = running.pop(0)
        rc = proc.wait()
        log.close()
        status = "done" if rc == 0 else f"FAILED (rc={rc})"
        print(f"  ■ {system} / {cell['key']} {status}")
        if rc != 0:
            failed.append((system, cell["key"]))
    return failed


def render(system, out_dir, anim_years=None):
    """Both palettes of the 4-panel PNG, per-body cuts, plus the interactive HTML.

    The site follows the reader's prefers-color-scheme, so the pages serve each figure
    as a pair through <picture>. The per-body cuts draw one body on top and dim the
    rest: a Phase 4 board page shows the two methods for the body whose page it is, and
    in the system view that body is usually buried.
    """
    def panel(*extra):
        for theme in ("dark", "light"):
            subprocess.run([PY, str(SCRIPTS / "plot_moons.py"), "--dir", str(out_dir),
                            "--label", system, "--theme", theme, *extra], check=True)

    panel()
    for body in cell_bodies(system, out_dir):
        panel("--highlight", body)
    subprocess.run([PY, str(SCRIPTS / "plot_interactive.py"), "--dir", str(out_dir),
                    "--label", system], check=True)
    if anim_years:
        subprocess.run([PY, str(SCRIPTS / "animate_orbits.py"), "--dir", str(out_dir),
                        "--label", system, "--max-years", repr(anim_years)], check=True)


def cell_bodies(system, out_dir):
    """The orbiting bodies this cell integrated (the star is not one of them)."""
    f = out_dir / f"{system}_summary.json"
    if not f.exists():
        return []
    d = json.loads(f.read_text())
    return ([p["name"] for p in d.get("planets", [])]
            + [h["name"] for h in d.get("hypotheticals", [])])


# ---------------------------------------------------------------- reading results

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def fmt_years(y):
    """10⁴ yr for exact powers of ten, 7.3×10⁵ yr otherwise, plain below 10⁴."""
    if y < 10000:
        return f"{y:,.0f} yr"
    e = int(math.floor(math.log10(y)))
    m = y / 10 ** e
    exp = str(e).translate(SUP)
    return f"10{exp} yr" if abs(m - 1) < 0.005 else f"{m:.1f}×10{exp} yr"


def read_cell(system, cell):
    """Summary + the horizon the run actually reached (from the timeseries)."""
    d = cell_dir(system, cell)
    sp = d / f"{system}_summary.json"
    if not sp.exists():
        return None
    s = json.loads(sp.read_text())
    ts = d / f"{system}_timeseries.csv"
    with ts.open() as f:
        t_end = max(float(r["t_yr"]) for r in csv.DictReader(f))
    integ = s["integration"]
    return {
        "key": cell["key"], "hierarchy": cell["hierarchy"], "method": cell["method"],
        "verdict": s["judgment"]["overall"], "integrator": integ["integrator"],
        "megno": integ["megno_final"], "dE": integ["energy_relative_error"],
        "lyapunov_yr": s["judgment"].get("lyapunov_time_yr"),
        "t_end": t_end,
        "n_planets": len(s.get("planets", [])),
        "n_moons": len([h for h in s.get("hypotheticals", []) if h.get("type") == "moon"]),
        "system_label": s["system"],
    }


# 복사되는 전체화면 뷰어(plotly·three)에 띄우는 되돌아가기 크럼. ?embed=1 이면 제거된다 —
# Phase 4 천체 페이지가 iframe 으로 물 때 남의 페이지 안의 "뒤로" 링크는 함정이라서.
_CRUMB_STYLE = "color:#7aa8ff;text-decoration:none"
VIEWER_CRUMB = (
    '<nav id="ns-crumb" style="position:fixed;top:8px;left:12px;z-index:1000;'
    'font:12px system-ui,sans-serif;background:rgba(10,12,18,.78);'
    'padding:4px 10px;border-radius:6px">'
    f'<a href="index.html" style="{_CRUMB_STYLE}">← Orbit viewers</a>'
    f' &nbsp;·&nbsp; <a href="../../index.html" style="{_CRUMB_STYLE}">Phase 4</a>'
    f' &nbsp;·&nbsp; <a href="../../../index.html" style="{_CRUMB_STYLE}">DB</a></nav>'
    '<script>if(new URLSearchParams(location.search).get("embed")==="1")'
    'document.getElementById("ns-crumb").remove()</script>')

# docs/assets/ 사본으로 CDN 을 로컬화. three(ES 모듈)만 예외 — Chromium 계열이 file:// 모듈
# 임포트를 CORS 로 막아 로컬 사본이 로드되지 않는다(클래식 <script>인 plotly 는 무관).
_CDN_LOCAL = {
    "https://cdn.jsdelivr.net/npm/plotly.js-dist-min@2.35.2/plotly.min.js":
        "../../../assets/plotly.min.js",
    "../../../assets/three.module.js":
        "https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js",
    "../../../assets/jsm/":
        "https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/",
}


def publish_viewer(src: Path, dst: Path):
    """Copy a full-screen viewer page in, with the back-crumb and local CDN refs."""
    html = src.read_text()
    for cdn, local in _CDN_LOCAL.items():
        html = html.replace(cdn, local)
    if 'id="ns-crumb"' not in html:
        new, n = re.subn(r"(<body[^>]*>)", r"\1" + VIEWER_CRUMB, html, count=1)
        if n == 0 and "</head>" in html:
            new = html.replace("</head>", "</head>" + VIEWER_CRUMB, 1)
        elif n == 0 and "</style>" in html:      # 암시적 head/body 구조인 뷰어 페이지
            new = html.replace("</style>", "</style>" + VIEWER_CRUMB, 1)
        elif n == 0:
            new = html + VIEWER_CRUMB
        html = new
    dst.write_text(html)

# ---------------------------------------------------------------- page generation

CSS = (SIM / "assets" / "validation-page.css").read_text()

VERDICT_CLASS = {"stable": "v-ok", "chaotic_but_hill_stable": "v-warn", "flagged": "v-warn"}
VERDICT_TEXT = {"stable": "STABLE", "chaotic_but_hill_stable": "CHAOTIC · HILL-STABLE",
                "flagged": "FLAGGED", "unstable": "UNSTABLE"}
# The index lists four cells per card, so it uses the short form of the same verdicts.
VERDICT_SHORT = {**VERDICT_TEXT, "chaotic_but_hill_stable": "CHAOTIC"}
HIERARCHY = {"planets": ("행성계", "Planet orbit"), "moons": ("위성계", "Moon system")}
LANG_JS = """<script>
const ko=document.getElementById('ko'),en=document.getElementById('en');
function set(e){document.querySelectorAll('[data-i18n]').forEach(x=>x.hidden=e);document.querySelectorAll('[data-en]').forEach(x=>x.hidden=!e);ko.classList.toggle('on',!e);en.classList.toggle('on',e);}
ko.onclick=()=>{set(false);localStorage.setItem('nearstars-lang','ko');};
en.onclick=()=>{set(true);localStorage.setItem('nearstars-lang','en');};
set(localStorage.getItem('nearstars-lang')!=='ko');
</script>"""


def i18n(ko, en):
    return f"<span data-i18n>{ko}</span><span data-en hidden>{en}</span>"


def slug(name):
    return name.replace("_", "-")


def cell_summary_line(r):
    """The one mono line under the verdict: horizon + the diagnostic that method yields."""
    bits = [fmt_years(r["t_end"])]
    if r["megno"] is None:
        bits.append("|ΔE/E|=" + f"{r['dE']:.1e}".replace("e-0", "e-"))
    else:
        bits.append(f"MEGNO {r['megno']:.2f}")
        lyap = r.get("lyapunov_yr")
        if lyap and math.isfinite(lyap) and r["verdict"] != "stable":
            bits.append(f"t<sub>Lyap</sub>≈{lyap / 1e6:.1f} Myr")
    return " · ".join(bits)


def matrix_table(rows, notes):
    head = ("<tr><th></th>"
            f"<th>leapfrog · {i18n('인게임 정합', 'in-game fidelity')}</th>"
            f"<th>IAS15/TRACE + MEGNO · {i18n('카오스 판정', 'chaos diagnosis')}</th></tr>")
    body = []
    for hier, cells in rows:
        ko, en = HIERARCHY[hier]
        any_cell = next(iter(cells.values()))
        count = (f'{any_cell["n_moons"]} moons' if hier == "moons"
                 else f'{any_cell["n_planets"]} bodies')
        tds = []
        for method in ("leapfrog", "accurate"):
            r = cells.get(method)
            if r is None:
                tds.append(f'<td class="note">{i18n("미실행", "not run")}</td>')
                continue
            note = notes.get(r["key"], {}).get("note")
            extra = (f'<br><span class="note">{i18n(note["ko"], note["en"])}</span>'
                     if note else "")
            tds.append(f'<td><span class="{VERDICT_CLASS.get(r["verdict"], "v-bad")}">'
                       f'{VERDICT_TEXT.get(r["verdict"], r["verdict"].upper())}</span>'
                       f'<br><span class="mono">{cell_summary_line(r)}</span>{extra}</td>')
        body.append(f'<tr><th>{i18n(ko, en)}<br><span class="mono">{count}</span></th>'
                    + "".join(tds) + "</tr>")
    return '<table class="matrix">' + head + "".join(body) + "</table>"


def figure(dst, key, alt):
    """<picture> when a light companion exists, plain <img> otherwise."""
    img = f'<img src="{key}.png" alt="{alt}" loading="lazy">'
    if (dst / f"{key}_light.png").exists():
        return (f'<picture><source media="(prefers-color-scheme: light)" '
                f'srcset="{key}_light.png">{img}</picture>')
    return img


def cards(dst, hier, cells):
    out = []
    for method in ("leapfrog", "accurate"):
        r = cells.get(method)
        if r is None:
            continue
        title = ("leapfrog" if method == "leapfrog" else f'{r["integrator"].upper()}+MEGNO')
        alt = f'{HIERARCHY[hier][1]} orbital elements, {r["integrator"]} integrator'
        out.append(
            f'<div class="card"><a href="{r["key"]}.html">{figure(dst, r["key"], alt)}</a>'
            f'<div class="m"><h3>{title} · {fmt_years(r["t_end"])}</h3>'
            f'<div class="sub">{cell_summary_line(r)} · '
            f'<a href="{r["key"]}.html">{i18n("인터랙티브", "interactive")}</a>'
            + (f' · <a href="{r["key"]}_orbit3d.html">{i18n("3D 애니메이션", "3D animation")}</a>'
               if (dst / f'{r["key"]}_orbit3d.html').exists() else "")
            + '</div></div></div>')
    return '<div class="grid">' + "".join(out) + "</div>"


def write_page(system, cfg, defaults, results):
    """One system's validation page: the matrix, then a card pair per hierarchy."""
    dst = GALLERY / slug(system)
    dst.mkdir(parents=True, exist_ok=True)
    for r in results:
        src = cell_dir(system, {"key": r["key"]})
        for name, target in ((f"{system}_orbits.png", f'{r["key"]}.png'),
                             (f"{system}_orbits_light.png", f'{r["key"]}_light.png'),
                             ):
            if (src / name).exists():
                (dst / target).write_bytes((src / name).read_bytes())
        for name, target in ((f"{system}_interactive.html", f'{r["key"]}.html'),
                             (f"{system}_orbit3d.html", f'{r["key"]}_orbit3d.html')):
            if (src / name).exists():
                publish_viewer(src / name, dst / target)
        for cut in sorted(src.glob(f"{system}_orbits_*.png")):   # per-body cuts
            tail = cut.name[len(f"{system}_orbits_"):]
            if tail == "light.png":
                continue
            (dst / f'{r["key"]}-{tail}').write_bytes(cut.read_bytes())

    by_hier = {}
    for r in results:
        by_hier.setdefault(r["hierarchy"], {})[r["method"]] = r
    order = [h for h in ("moons", "planets") if h in by_hier]
    notes = cfg.get("cells", {}) or {}

    lead = cfg.get("lead", defaults["lead"])
    sections = []
    for h in order:
        ko, en = HIERARCHY[h]
        sections.append(f"<h2>{i18n(ko, en)}</h2>" + cards(dst, h, by_hier[h]))
    bl = cfg.get("bottom_line")
    bottom = f'<p class="note">{i18n(bl["ko"], bl["en"])}</p>' if bl else ""
    nt = cfg.get("note")
    tail = (f'<p class="note" style="margin-top:20px">{i18n(nt["ko"], nt["en"])}</p>'
            if nt else "")
    title = cfg.get("title", system)

    html = f"""<!-- {title} 궤도 안정성 검증 매트릭스 (자동 생성, scripts/validate_orbits.py) -->
<!doctype html><html lang="en" class="ns-light-ok"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — orbit stability validation</title>
<style>
{CSS}</style>
{global_bar('../../../', 'Phase 4')}
<header>
  <div class="seg"><button id="ko">한</button><button id="en" class="on">EN</button></div>
  <nav style="font-size:12px;margin-bottom:8px"><a href="../index.html" style="color:#7aa8ff;text-decoration:none">← {i18n('궤도 뷰어', 'Orbit viewers')}</a></nav>
  <h1>{title} — {i18n('궤도 안정성 검증', 'orbit stability validation')}</h1>
  <div class="lead">{i18n(lead['ko'], lead['en'])}</div>
</header>
<main>
  {matrix_table([(h, by_hier[h]) for h in order], notes)}
  {bottom}
  {"".join(sections)}
  {tail}
</main>
{LANG_JS}
"""
    (dst / "index.html").write_text(html)
    print(f"  → wrote {dst / 'index.html'}")


def write_index(entries):
    """The landing page listing every validated system, one image card each."""
    rows = []
    for e in entries:
        by_key = {r["key"]: r for r in e["results"]}
        # thumbnail: the hierarchy the player actually inhabits, if the system has one
        thumb = next((k for k in ("moons_leapfrog", "planets_leapfrog", "moons_accurate",
                                  "planets_accurate") if k in by_key), None)
        lines = []
        for r in e["results"]:
            cls = VERDICT_CLASS.get(r["verdict"], "v-bad")
            lines.append(f'<tr><td class="mono">{r["key"]}</td>'
                         f'<td class="mono">{fmt_years(r["t_end"])}</td>'
                         f'<td class="{cls}">{VERDICT_SHORT.get(r["verdict"], r["verdict"])}</td></tr>')
        href = f'{slug(e["system"])}/index.html'
        vdir = GALLERY / slug(e["system"])
        img = ""
        if thumb:
            fig = figure(vdir, thumb, f'{e["title"]} validation matrix')
            fig = fig.replace(f'"{thumb}', f'"{vdir.name}/{thumb}')
            img = f'<a href="{href}">{fig}</a>'
        rows.append(f'<div class="card">{img}<div class="m">'
                    f'<h3><a href="{href}">{e["title"]}</a></h3>'
                    f'<table class="cells">{"".join(lines)}</table></div></div>')
    html = f"""<!-- 궤도 검증 세트 인덱스 (자동 생성, scripts/validate_orbits.py) -->
<!doctype html><html lang="en" class="ns-light-ok"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NearStars — orbit stability validation sets</title>
<style>
{CSS}
  table.cells{{border-collapse:collapse;margin-top:7px;font-size:12px}}
  table.cells td{{padding:2px 10px 2px 0;vertical-align:top;white-space:nowrap}}
  table.cells td:nth-child(2){{color:rgba(255,255,255,.52);text-align:right}}
  @media (prefers-color-scheme: light) {{
    html.ns-light-ok table.cells td:nth-child(2){{color:rgba(9,12,22,.60)}}
  }}
</style>
{global_bar('../../', 'Phase 4')}
<header>
  <div class="seg"><button id="ko">한</button><button id="en" class="on">EN</button></div>
  <h1>{i18n('궤도 동역학 뷰어', 'Orbit dynamics viewers')}</h1>
  <div class="lead">{i18n(
      '시스템마다 계층(행성계·위성계)별로 두 방식을 교차 실행합니다. leapfrog(고정 10분 스텝)는 '
      'Principia 인게임 적분기와 정합하고, IAS15/TRACE+MEGNO는 결정론적 카오스와 장기 생존을 판정합니다. '
      '장기 구간은 연수가 아니라 안쪽 궤도 바퀴 수(기준 10⁸바퀴)로 맞춥니다.',
      'Each system is run both ways on every hierarchy it has. Leapfrog (fixed 10-min step) '
      "matches Principia's in-game integrator; IAS15/TRACE+MEGNO judges deterministic chaos and "
      'long-term survival. Long horizons are matched in inner-orbit count (10⁸ orbits), not years.')}</div>
</header>
<main><div class="grid">{"".join(rows)}</div></main>
{LANG_JS}
"""
    (GALLERY / "index.html").write_text(html)
    print(f"  → wrote {GALLERY / 'index.html'}  ({len(entries)} systems)")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systems", nargs="*", help="subset of manifest system keys")
    ap.add_argument("--cells", nargs="*", help="subset of cell keys (e.g. planets_leapfrog)")
    ap.add_argument("--force", action="store_true", help="re-run cells that already have results")
    ap.add_argument("--jobs", type=int, default=1,
                    help="run up to N cells concurrently (one CPU core each; default 1)")
    ap.add_argument("--pages-only", action="store_true", help="regenerate HTML from existing runs")
    ap.add_argument("--dry-run", action="store_true", help="print the plan and stop")
    args = ap.parse_args()

    man = yaml.safe_load(MANIFEST.read_text())
    defaults, systems = man["defaults"], man["systems"]
    keys = args.systems or list(systems)

    planned, queued = [], []
    for system in keys:
        cfg = systems[system] or {}
        print(f"■ {system}")
        cells = expand(system, cfg, defaults)
        if args.cells:
            cells = [c for c in cells if c["key"] in args.cells]
        planned.append((system, cfg, cells))
        for cell in cells:
            state, got = cell_state(system, cell)
            tag = {"have": "[have]", "run": "[run]",
                   "stale": f"[stale: {fmt_years(got or 0)} stored]"}[state]
            print(f'  {cell["key"]:18s} {cell["integrator"]:9s} '
                  f'{fmt_years(cell["years"]):>12s}  {tag}')
            if not args.dry_run and not args.pages_only and (state != "have" or args.force):
                out_dir = cell_dir(system, cell)
                out_dir.mkdir(parents=True, exist_ok=True)
                queued.append((system, cell, out_dir))
    if args.dry_run:
        return

    if queued:
        print(f"\n▶ {len(queued)} cell(s), {args.jobs} at a time")
        failed = run_cells(queued, args.jobs)
        if failed:
            print("\n! failed cells: " + ", ".join(f"{s}/{k}" for s, k in failed))

    for system, cfg, cells in planned:
        if not args.pages_only:
            for cell in cells:
                if (cell_dir(system, cell) / f"{system}_summary.json").exists():
                    render(system, cell_dir(system, cell), cell.get("anim_years"))
        results = [r for r in (read_cell(system, c) for c in cells) if r]
        if not results:
            print(f"  ! no results yet for {system}")
            continue
        write_page(system, cfg, defaults, results)

    # The landing page always lists EVERY manifest system that has stored results:
    # --systems/--cells narrow what runs and which system pages re-render, but must
    # not shrink the gallery — a filtered invocation used to overwrite the index
    # with just its subset, dropping the other systems from the site.
    entries = []
    for system, cfg in ((s, systems[s] or {}) for s in systems):
        results = [r for r in (read_cell(system, c)
                               for c in expand(system, cfg, defaults)) if r]
        if results:
            entries.append({"system": system, "title": cfg.get("title", system),
                            "results": results})
    if entries:
        write_index(entries)


if __name__ == "__main__":
    main()
