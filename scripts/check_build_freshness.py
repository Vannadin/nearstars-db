# 파이프라인 빌드 산출물의 신선도 + 매니페스트 커버리지 점검
"""Verify that docs/ derived artifacts are up to date with their sources,
and that reports-manifest.json covers every host that should be there.

The original bug class:
- run_pipeline.sh [8/8] build_site.py was skipped while db/ rebuilds
  happened, leaving docs/data.json 8 days stale.
- build_reports_index.py left "orphan" slug-only keys (`barnards`,
  `barnards-star`, `delta`) because slug functions diverged from the
  Phase 3 file naming convention.

Both classes are mechanical to detect.

Checks (FAIL on any failure, prints PASS otherwise):

1. docs/data.json must be no older than the newest db/systems/*.json
2. docs/reports.html / docs/reports-manifest.json must be no older than
   the newest docs/phase{2,3}/*.html
3. reports-manifest.json must have one key per host display name and
   zero "orphan" slug-only keys (the signature of slug-convention drift)
4. Every Phase 2 / Phase 3 html under docs/ must appear in the manifest
   (no dangling file)

Run manually via `scripts/check.sh` section 7, or directly:
    python3 scripts/check_build_freshness.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DB = ROOT / "db"

failures: list[str] = []


def newest_mtime(paths) -> float:
    paths = [p for p in paths if p.exists()]
    if not paths:
        return 0.0
    return max(p.stat().st_mtime for p in paths)


# 1. data.json freshness vs db/systems/
systems_files = list((DB / "systems").glob("*.json"))
data_json = DOCS / "data.json"
if not data_json.exists():
    failures.append("docs/data.json missing — run build_site.py")
else:
    newest_system = newest_mtime(systems_files)
    if newest_system > data_json.stat().st_mtime + 1.0:   # 1s grace
        from datetime import datetime
        d_dt = datetime.fromtimestamp(data_json.stat().st_mtime)
        s_dt = datetime.fromtimestamp(newest_system)
        failures.append(
            f"docs/data.json stale: mtime {d_dt:%Y-%m-%d %H:%M} vs newest "
            f"db/systems/ {s_dt:%Y-%m-%d %H:%M} — run build_site.py"
        )

# 2. reports.html / reports-manifest.json freshness vs docs/phase{2,3}/
phase_html = [
    f for f in (list((DOCS / "phase2").glob("*.html")) + list((DOCS / "phase3").glob("*.html")))
    # manual-fetch.html + _-prefixed are not per-host reports; they're freshness-
    # gated separately (manual-fetch by section 5) and must not drive reports.html.
    if not f.stem.startswith("_") and f.stem != "manual-fetch"
]
reports_html = DOCS / "reports.html"
reports_manifest = DOCS / "reports-manifest.json"
for target_name, target in (("docs/reports.html", reports_html),
                             ("docs/reports-manifest.json", reports_manifest)):
    if not target.exists():
        failures.append(f"{target_name} missing — run build_reports_index.py")
        continue
    newest_phase = newest_mtime(phase_html)
    if newest_phase > target.stat().st_mtime + 1.0:
        from datetime import datetime
        t_dt = datetime.fromtimestamp(target.stat().st_mtime)
        p_dt = datetime.fromtimestamp(newest_phase)
        failures.append(
            f"{target_name} stale: mtime {t_dt:%Y-%m-%d %H:%M} vs newest "
            f"docs/phase{{2,3}}/ {p_dt:%Y-%m-%d %H:%M} — run build_reports_index.py"
        )

# 3 + 4. reports-manifest coverage + orphan-key absence
if reports_manifest.exists():
    manifest = json.loads(reports_manifest.read_text(encoding="utf-8"))

    # Compute the canonical host name set from source layer.
    stellar = json.loads((DB / "stellar_props_curated.json").read_text(encoding="utf-8"))
    target_list = json.loads((DB / "target_list.json").read_text(encoding="utf-8"))
    disks = (DB / "disks_curated.json")
    disks_data = json.loads(disks.read_text(encoding="utf-8")) if disks.exists() else {}

    known_hosts: set[str] = set()
    known_hosts.update(stellar.keys())
    known_hosts.update(disks_data.keys())
    for tgt in target_list:
        known_hosts.update(tgt.get("components", []))

    # 3. orphan keys — keys that look like slugs (lowercase + '-', no apostrophes)
    #    but are not actual host display names.
    orphan_keys = [k for k in manifest if k not in known_hosts]
    if orphan_keys:
        failures.append(
            f"docs/reports-manifest.json has {len(orphan_keys)} orphan key(s) "
            f"(slug-only or unknown): {sorted(orphan_keys)} — slug convention "
            f"drift between Phase 2/3 builders. Rebuild + check."
        )

    # 4. every html file must be linked from manifest
    referenced_paths: set[str] = set()
    for entry in manifest.values():
        if isinstance(entry, dict):
            p2 = entry.get("phase2")
            if p2: referenced_paths.add(p2)
            for path in (entry.get("phase3") or {}).values():
                referenced_paths.add(path)
    dangling: list[str] = []
    for f in phase_html:
        rel = f"phase2/{f.name}" if f.parent.name == "phase2" else f"phase3/{f.name}"
        # _-prefixed files are infrastructure (skipped by scan_reports too).
        if f.stem.startswith("_"): continue
        if f.stem == "manual-fetch": continue
        if rel not in referenced_paths:
            dangling.append(rel)
    if dangling:
        failures.append(
            f"docs/reports-manifest.json missing {len(dangling)} html file(s): "
            f"{sorted(dangling)[:5]}{'...' if len(dangling) > 5 else ''} — "
            f"rebuild reports index."
        )


# 5. manual-fetch.html freshness vs its sources (_bib/*.yaml + manual-paper-followup.md)
manual_fetch = DOCS / "phase3" / "manual-fetch.html"
mf_sources = (list((DOCS / "phase3" / "_bib").glob("*.yaml"))
              + list((ROOT / "phase3").glob("*/manual-paper-followup.md")))
if not manual_fetch.exists():
    failures.append("docs/phase3/manual-fetch.html missing — run build_manual_fetch.py")
else:
    newest_mf_src = newest_mtime(mf_sources)
    if newest_mf_src > manual_fetch.stat().st_mtime + 1.0:
        from datetime import datetime
        m_dt = datetime.fromtimestamp(manual_fetch.stat().st_mtime)
        s_dt = datetime.fromtimestamp(newest_mf_src)
        failures.append(
            f"docs/phase3/manual-fetch.html stale: mtime {m_dt:%Y-%m-%d %H:%M} vs newest "
            f"_bib/manual-paper-followup {s_dt:%Y-%m-%d %H:%M} — run build_manual_fetch.py"
        )


# 6. every Phase-2-grade host must have a docs/phase2/<slug>.html
#    (build_phase2_html.py coverage — catches the "curated Phase 2 but viewer
#    page never regenerated" gap that left new hosts showing Phase 3 only).
try:
    sys.path.insert(0, str(ROOT / "scripts" / "pipeline"))
    from build_phase2_html import find_phase2_hosts
    from _naming import to_url_slug
    stellar_c = json.loads((DB / "stellar_props_curated.json").read_text(encoding="utf-8"))
    missing_p2 = [h for h in find_phase2_hosts(stellar_c)
                  if not (DOCS / "phase2" / f"{to_url_slug(h)}.html").exists()]
    if missing_p2:
        failures.append(
            f"{len(missing_p2)} Phase-2 host(s) missing docs/phase2/*.html: "
            f"{sorted(missing_p2)[:6]}{'...' if len(missing_p2) > 6 else ''} "
            f"— run build_phase2_html.py"
        )
except Exception as e:
    failures.append(f"phase2-coverage check errored: {e}")


# Output
if failures:
    for msg in failures:
        print(f"  [FAIL] {msg}")
    sys.exit(1)
else:
    print(f"  [PASS] 빌드 산출물 신선도 + 매니페스트 커버리지 ({len(systems_files)} systems, "
          f"{len(phase_html)} phase html)")
    sys.exit(0)
