# 궤도 뷰어 배치 드라이버 — 매니페스트대로 전 시스템을 Principia 방식으로 재실행하고 뷰어+갤러리 생성.
"""Batch-build the orbit dynamics viewers from viewer-manifest.yaml.

For each system in the manifest it:
  1. re-runs the sim the Principia way (fixed-step leapfrog, dt = 10 min) into
     results/_viewers/<system>/  — skipped if the summary is already fresh
     (newer than the manifest) unless --force.
  2. renders the static 4-panel PNG (plot_moons.py) + the 3D animation
     (animate_orbits.py) from that one run.
  3. copies both into docs/phase4/orbit-viewers/<slug>/ and writes a bilingual
     gallery index.

Reproducible single source: the manifest holds every per-system run parameter,
so `python build_viewers.py` re-derives the whole gallery. Existing WHFast/TRACE
summaries are never reused — the viewer must reflect the in-game integrator.

Usage:
  python scripts/build_viewers.py                 # all systems, skip-if-fresh
  python scripts/build_viewers.py --systems trappist_1 tau_cet
  python scripts/build_viewers.py --force         # re-run every sim
  python scripts/build_viewers.py --quick         # tiny run (plumbing smoke test)
  python scripts/build_viewers.py --gallery-only  # just rebuild the index
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

SIM = Path(__file__).resolve().parent.parent          # phase3/stability-sim
ROOT = SIM.parent.parent                               # repo root
SCRIPTS = SIM / "scripts"
MANIFEST = SIM / "viewer-manifest.yaml"
GALLERY = ROOT / "docs/phase4/orbit-viewers"
PY = sys.executable


def slug(name):
    return name.replace("_", "-")


def is_fresh(summary, ref_mtime, force):
    return (not force) and summary.exists() and summary.stat().st_mtime >= ref_mtime


def run_sim(name, cfg, defaults, out_dir, quick):
    years = 50 if quick else cfg.get("years", defaults["years"])
    snaps = 200 if quick else cfg.get("snapshots", defaults["snapshots"])
    cmd = [PY, str(SCRIPTS / "run.py"), "--system", name,
           "--integrator", defaults["integrator"], "--dt-minutes", str(defaults["dt_minutes"]),
           "--years", str(years), "--snapshots", str(snaps), "--out-dir", str(out_dir)]
    if cfg.get("hypotheticals"):
        cmd += ["--hypotheticals", str(SIM / cfg["hypotheticals"])]
    cmd += cfg.get("extra_args", [])
    print(f"  ▶ sim: {name}  ({years} yr, {snaps} snapshots, leapfrog dt={defaults['dt_minutes']}min)")
    subprocess.run(cmd, check=True)


def render(name, cfg, out_dir):
    center = cfg.get("center")
    for viz in ("plot_moons.py", "animate_orbits.py", "plot_interactive.py"):
        cmd = [PY, str(SCRIPTS / viz), "--dir", str(out_dir), "--label", name]
        if center:
            cmd += ["--center", center]
        subprocess.run(cmd, check=True)


def collect(name, out_dir):
    """Copy the three artifacts into the gallery dir; return meta for the index."""
    dst = GALLERY / slug(name)
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(out_dir / f"{name}_orbits.png", dst / "orbits.png")
    shutil.copy2(out_dir / f"{name}_orbit3d.html", dst / "orbit3d.html")
    shutil.copy2(out_dir / f"{name}_interactive.html", dst / "interactive.html")
    summary = json.loads((out_dir / f"{name}_summary.json").read_text())
    integ = summary["integration"]
    return {
        "name": name, "slug": slug(name),
        "system": summary["system"],
        "verdict": summary["judgment"]["overall"],
        "n_planets": len(summary.get("planets", [])),
        "n_moons": len([h for h in summary.get("hypotheticals", []) if h.get("type") == "moon"]),
        "integrator": integ["integrator"],
        "dt_min": round(integ["dt_yr"] * 365.25 * 24 * 60, 1),
        "dE": f"{integ['energy_relative_error']:.1e}",
    }


def write_gallery(cards):
    GALLERY.mkdir(parents=True, exist_ok=True)
    rows = []
    for c in cards:
        vclass = {"stable": "ok", "chaotic_but_hill_stable": "warn"}.get(c["verdict"], "bad")
        bodies = (f'{c["n_planets"]} <span data-i18n>행성</span><span data-en hidden>planets</span>'
                  if c["n_moons"] == 0 else
                  f'{c["n_moons"]} <span data-i18n>위성</span><span data-en hidden>moons</span>')
        rows.append(f"""  <div class="card">
    <a href="{c['slug']}/interactive.html"><img src="{c['slug']}/orbits.png" alt="{c['system']}" loading="lazy"></a>
    <div class="meta"><h3>{c['system']}</h3>
      <span class="pill {vclass}">{c['verdict']}</span>
      <span class="sub">{bodies} · {c['integrator']} dt={c['dt_min']}min · |ΔE/E|={c['dE']}</span>
      <div class="links"><a href="{c['slug']}/interactive.html"><span data-i18n>인터랙티브</span><span data-en hidden>Interactive</span></a>
        <a href="{c['slug']}/orbit3d.html"><span data-i18n>3D 애니메이션</span><span data-en hidden>3D animation</span></a></div></div>
  </div>""")
    html = f"""<!-- 궤도 동역학 뷰어 갤러리 (자동 생성, build_viewers.py) -->
<!doctype html><meta charset="utf-8"><title>NearStars — Orbit dynamics viewers</title>
<style>
  body{{margin:0;background:#0a0c12;color:#cdd6e6;font:14px/1.6 system-ui,sans-serif}}
  header{{padding:20px 24px;border-bottom:1px solid #1c2436}}
  h1{{margin:0;font-size:19px}} .lead{{color:#8a94a8;font-size:13px;margin-top:4px;max-width:70ch}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:16px;padding:22px}}
  .card{{background:#11141d;border:1px solid #1c2436;border-radius:10px;overflow:hidden;transition:border-color .15s}}
  .card:hover{{border-color:#3b78d0}}
  .card img{{width:100%;display:block;background:#06070d}}
  .meta{{padding:11px 13px}} .meta h3{{margin:0 0 5px;font-size:15px;color:#cdd6e6}}
  .links{{margin-top:8px;display:flex;gap:8px}}
  .links a{{font-size:12px;color:#7fb0ff;text-decoration:none;border:1px solid #2c3a5a;border-radius:5px;padding:2px 9px}}
  .links a:hover{{background:#1c2740}}
  .pill{{font-size:11px;padding:2px 8px;border-radius:5px;font-family:ui-monospace,monospace}}
  .pill.ok{{color:#8fe3a0;background:rgba(143,227,160,.13)}}
  .pill.warn{{color:#e8c561;background:rgba(232,197,97,.13)}}
  .pill.bad{{color:#e57;background:rgba(229,85,119,.13)}}
  .sub{{display:block;color:#8a94a8;font-size:11px;margin-top:6px;font-variant-numeric:tabular-nums}}
  .seg{{float:right}} .seg button{{background:#1c2740;color:#cdd6e6;border:1px solid #2c3a5a;border-radius:6px;padding:4px 10px;cursor:pointer}}
</style>
<header>
  <div class="seg"><button id="ko" class="on">한국어</button><button id="en">EN</button></div>
  <h1><span data-i18n>궤도 동역학 뷰어</span><span data-en hidden>Orbit dynamics viewers</span></h1>
  <div class="lead"><span data-i18n>각 시스템을 Principia와 동일한 고정 스텝 leapfrog(dt 10분)로 재실행한 결과. 인터랙티브(범례 토글·호버·줌) 또는 3D 궤도 진화 애니메이션으로 볼 수 있습니다.</span><span data-en hidden>Each system re-run with Principia's fixed-step leapfrog (dt 10 min). View interactively (legend toggle / hover / zoom) or as a 3D orbit-evolution animation.</span></div>
</header>
<div class="grid">
{chr(10).join(rows)}
</div>
<script>
const ko=document.getElementById('ko'),en=document.getElementById('en');
function set(e){{document.querySelectorAll('[data-i18n]').forEach(x=>x.hidden=e);document.querySelectorAll('[data-en]').forEach(x=>x.hidden=!e);ko.classList.toggle('on',!e);en.classList.toggle('on',e);}}
ko.onclick=()=>set(false);en.onclick=()=>set(true);
</script>
"""
    (GALLERY / "index.html").write_text(html)
    print(f"  → wrote gallery {GALLERY / 'index.html'}  ({len(cards)} systems)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systems", nargs="*", help="subset of manifest system keys")
    ap.add_argument("--force", action="store_true", help="re-run sims even if fresh")
    ap.add_argument("--quick", action="store_true", help="tiny run for plumbing smoke test")
    ap.add_argument("--gallery-only", action="store_true", help="just rebuild the index from existing outputs")
    args = ap.parse_args()

    man = yaml.safe_load(MANIFEST.read_text())
    defaults, systems = man["defaults"], man["systems"]
    ref_mtime = MANIFEST.stat().st_mtime
    keys = args.systems or list(systems)

    cards = []
    for name in keys:
        cfg = systems[name] or {}
        out_dir = SIM / "results" / "_viewers" / name
        out_dir.mkdir(parents=True, exist_ok=True)
        summary = out_dir / f"{name}_summary.json"
        print(f"■ {name}")
        if not args.gallery_only:
            if is_fresh(summary, ref_mtime, args.force):
                print(f"  ✓ sim fresh — skipping (use --force to re-run)")
            else:
                run_sim(name, cfg, defaults, out_dir, args.quick)
            render(name, cfg, out_dir)
        if summary.exists():
            cards.append(collect(name, out_dir))
        else:
            print(f"  ! no summary for {name} — run without --gallery-only first")

    write_gallery(cards)


if __name__ == "__main__":
    main()
