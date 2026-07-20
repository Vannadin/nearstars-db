# 페이즈 경계 정합성 게이트(check.sh gate 10) — phase4 body↔db 대조·로스터 완결성·Decisions 파싱 검증.
# regenerable: read-only gate, no writes
"""Pipeline-flow gate (docs/reference/pipeline-contract.md §1).

FAIL (exit 1) on structural violations:
  10a  phase4 board `system:` != filename stem; real-body `body:` key not in db
       and not marked fictional (identity row discoverability=fictional).
  10c  a docs/phase3 report whose `## Decisions` section exists but yields 0
       parseable rows (interface break for the md-scraping emitters).

WARN (exit 0) on completeness gaps (tracked work, not regressions):
  10b  confirmed-roster matrix (db/roster.yaml): missing boards, board rows not
       covering db bodies, missing phase3 reports.
       Also: reports with no Decisions section; duplicate Decision labels.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from pipeline._naming import to_url_slug  # noqa: E402
from pipeline.phase3_decisions import duplicate_labels, parse_decisions  # noqa: E402

fail = 0
warnings: list[str] = []


def _fail(msg: str) -> None:
    global fail
    print(f"  [FAIL] {msg}")
    fail = 1


# ── db name universe ─────────────────────────────────────────────────
db_names: set[str] = set()                 # every star/planet name
system_bodies: dict[str, dict] = {}        # stem -> {star: str|None, planets: [names]}
for f in sorted((REPO / "db" / "systems").glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    stars = [s.get("name") for s in d.get("stars", []) if s.get("name")]
    planets = [p.get("name") for p in d.get("planets", []) if p.get("name")]
    db_names.update(stars)
    db_names.update(planets)
    system_bodies[f.stem] = {"stars": stars, "planets": planets}


def is_fictional(rows_for_body: list[dict]) -> bool:
    for row in rows_for_body:
        cfg = row.get("discoverability_cfg")
        if isinstance(cfg, dict) and cfg.get("category") == "fictional":
            return True
        for fld in row.get("fields") or []:
            if (
                isinstance(fld, dict)
                and fld.get("name") == "discoverability"
                and "fictional" in str(fld.get("value", ""))
            ):
                return True
    return False


# ── 10a: phase4 boards ↔ db ─────────────────────────────────────────
boards: dict[str, dict] = {}               # board stem -> parsed yaml
board_bodies: dict[str, set[str]] = {}     # board stem -> body keys (sans "*")
for f in sorted((REPO / "phase4").glob("*.yaml")):
    board = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    boards[f.stem] = board
    if board.get("system") != f.stem:
        _fail(f"phase4/{f.name}: system '{board.get('system')}' != filename stem '{f.stem}'")
    rows = board.get("decisions") or []
    by_body: dict[str, list[dict]] = {}
    for row in rows:
        b = str(row.get("body", "")).strip()
        if b:
            by_body.setdefault(b, []).append(row)
    board_bodies[f.stem] = {b for b in by_body if b != "*"}
    for b, rws in by_body.items():
        if b == "*" or b in db_names:
            continue
        if is_fictional(rws):
            continue
        _fail(
            f"phase4/{f.name}: body '{b}' not in db names and not marked fictional "
            f"(SPEC §3 naming contract)"
        )

# ── 10c: Decisions tables parse ──────────────────────────────────────
no_decisions: list[str] = []
for md in sorted((REPO / "docs" / "phase3").glob("*.md")):
    rows = parse_decisions(md.read_text(encoding="utf-8"))
    if rows is None:
        no_decisions.append(md.name)
        continue
    if not rows:
        _fail(f"docs/phase3/{md.name}: '## Decisions' present but 0 parseable rows")
        continue
    dups = duplicate_labels(rows)
    if dups:
        warnings.append(f"docs/phase3/{md.name}: duplicate Decision labels {dups}")
if no_decisions:
    warnings.append(f"reports with no Decisions section ({len(no_decisions)}): {', '.join(no_decisions)}")

# ── 10b: roster completeness matrix (warnings only) ─────────────────
roster = yaml.safe_load((REPO / "db" / "roster.yaml").read_text(encoding="utf-8"))
for entry in roster.get("confirmed", []):
    stem, cls, board_stem = entry["system"], entry["class"], entry["board"]
    sysb = system_bodies.get(stem)
    if sysb is None:
        _fail(f"roster.yaml: system '{stem}' has no db/systems file")
        continue
    tag = f"{stem} [{cls}]"
    if board_stem not in boards:
        warnings.append(f"{tag}: board phase4/{board_stem}.yaml MISSING")
        board_cover: set[str] = set()
        has_wildcard = False
    else:
        board_cover = board_bodies[board_stem]
        has_wildcard = any(
            str(r.get("body", "")).strip() == "*"
            for r in (boards[board_stem].get("decisions") or [])
        )
    for star in sysb["stars"]:
        if not (REPO / "docs" / "phase3" / f"{to_url_slug(star)}.md").exists():
            warnings.append(f"{tag}: no star-level phase3 report for '{star}'")
        if board_stem in boards and star not in board_cover:
            warnings.append(f"{tag}: board has no rows for star '{star}'")
    host = sysb["stars"][0] if sysb["stars"] else stem
    for planet in sysb["planets"]:
        # report slug convention: host url-slug + planet letter
        # (== to_url_slug(planet name) except when the db planet name omits
        # the host suffix, e.g. 'Barnard b' -> barnards-star-b). Contract §2.
        letter = planet.split()[-1].lower()
        candidates = {f"{to_url_slug(host)}-{letter}", to_url_slug(planet)}
        if not any((REPO / "docs" / "phase3" / f"{c}.md").exists() for c in candidates):
            warnings.append(f"{tag}: no phase3 report for planet '{planet}'")
        if board_stem in boards and planet not in board_cover and not has_wildcard:
            warnings.append(f"{tag}: board has no rows for planet '{planet}' (and no '*' wildcard)")

# ── 10d: phase-2 measurement floor, all curated hosts ≤ 50 ly ────────
# contract §4. Class by spectype: D*→WD, L/T/Y→BD, O/B/A→A-type, else FGKM host.
FLOORS = {
    "wd":   {"teff", "radius", "mass", "age"},
    "bd":   {"teff", "radius", "luminosity", "mass", "age"},
    "a":    {"teff", "radius", "luminosity", "mass", "age", "rotation"},
    "fgkm": {"teff", "radius", "luminosity", "mass", "age", "rotation", "activity"},
}
LY_50_PC = 50 / 3.26156

curated = json.loads((REPO / "db" / "stellar_props_curated.json").read_text(encoding="utf-8"))
star_meta: dict[str, dict] = {}   # star name -> {dist_pc, spectype}
for f in sorted((REPO / "db" / "systems").glob("*.json")):
    d = json.loads(f.read_text(encoding="utf-8"))
    for s in d.get("stars", []):
        star_meta[s.get("name")] = {
            "dist_pc": (s.get("derived") or {}).get("distance_pc"),
            "spectype": (s.get("raw") or {}).get("spectype") or "",
        }

def star_class(sp_raw: str) -> str:
    """Spectral type → floor class. Handles WD 'DA/DB/...' (uppercase D +
    class letter), dwarf/subdwarf prefixes 'd'/'sd'/'esd' (dM4, sdM1), and
    L/T/Y brown dwarfs."""
    sp = (sp_raw or "").strip()
    import re as _re
    if _re.match(r"^D[ABCOQZX]", sp):
        return "wd"
    sp = _re.sub(r"^(esd|sd|d)", "", sp)  # dwarf-notation prefixes, lowercase only
    first = sp[:1].upper()
    if first in ("L", "T", "Y"):
        return "bd"
    if first in ("O", "B", "A"):
        return "a"
    return "fgkm"


floor_detail = "--floor-detail" in sys.argv
floor_gaps_by_cls: dict[str, int] = {}
for name, entry in sorted(curated.items()):
    meta = star_meta.get(name)
    if not meta or not meta["dist_pc"] or meta["dist_pc"] > LY_50_PC:
        continue
    cls = star_class(entry.get("spectype") or meta["spectype"])
    missing = sorted(
        cat for cat in FLOORS[cls]
        if not entry.get(f"{cat}_measurements")
    )
    if missing:
        floor_gaps_by_cls[cls] = floor_gaps_by_cls.get(cls, 0) + 1
        if floor_detail:
            warnings.append(f"floor[{cls}] {name}: missing {', '.join(missing)}")
if floor_gaps_by_cls:
    total = sum(floor_gaps_by_cls.values())
    by = ", ".join(f"{c}:{n}" for c, n in sorted(floor_gaps_by_cls.items()))
    warnings.append(
        f"phase-2 floor: {total} curated hosts ≤50 ly below floor ({by}) — "
        f"backfill worklist; per-host detail: check_pipeline_flow.py --floor-detail"
    )

# ── 10e: planets_curated legacy dict-form census ─────────────────────
pl_curated = json.loads((REPO / "db" / "planets_curated.json").read_text(encoding="utf-8"))
dict_blocks = 0
dict_hosts: set[str] = set()
for host, planets in pl_curated.items():
    for pl in planets if isinstance(planets, list) else []:
        for blk in ("orbital", "physical", "environment", "atmosphere", "rings"):
            if isinstance(pl.get(blk), dict):
                dict_blocks += 1
                dict_hosts.add(host)
if dict_blocks:
    warnings.append(
        f"planets_curated: {dict_blocks} legacy dict-form blocks across "
        f"{len(dict_hosts)} hosts (Phase-2 canonical = list+method; upgrade on touch)"
    )

# ── 10f: field-alignment coverage (phase4 menu name ↔ phase3 key) ────
# An unmapped board field is not an error — it emits under its board name —
# but it can never override a phase3 decision, so the gap must stay visible.
sys.path.insert(0, str(REPO / "scripts" / "pipeline"))
from resolve_emit_values import load_alignment  # noqa: E402

alignment = load_alignment()
unmapped: dict[str, set[str]] = {}
for bf in sorted((REPO / "phase4").glob("*.yaml")):
    board = yaml.safe_load(bf.read_text(encoding="utf-8")) or {}
    for row in board.get("decisions") or []:
        for fld in row.get("fields") or []:
            if isinstance(fld, dict) and fld.get("name"):
                name = str(fld["name"])
                if name not in alignment:
                    unmapped.setdefault(name, set()).add(bf.stem)
if unmapped:
    warnings.append(
        f"field alignment: {len(unmapped)} phase4 field name(s) unmapped in "
        f"scripts/pipeline/field_alignment.yaml — cannot override phase3: "
        + ", ".join(sorted(unmapped))
    )

# ── report ───────────────────────────────────────────────────────────
for w in warnings:
    print(f"  [WARN] {w}")
if fail:
    print(f"  [FAIL] 파이프라인 경계 게이트 실패 (경고 {len(warnings)}건 별도)")
else:
    print(f"  [PASS] 파이프라인 경계 게이트 통과 (완결성 경고 {len(warnings)}건)")
sys.exit(fail)
