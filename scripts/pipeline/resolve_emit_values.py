# emit 값 해석기 — db → phase3 Decisions → phase4 fields[]를 바디별 단일 유효값으로 병합 (드라이런 전용).
# regenerable: read-only resolver; cfg writing stays in the emitter skills (rewired at emit time)
"""Resolve effective per-body emit values (pipeline-contract.md §3).

Layering, later wins:

    db/systems derived  <  phase3 Decisions (parsed)  <  phase4 fields[] (gated)

This module is the single place the three stores meet. Emitters format cfg
syntax from this output at emit-rewiring time; until then it serves as the
dry-run proving the chain (a phase4 edit visibly lands in `effective`).

Usage:
    python3 scripts/pipeline/resolve_emit_values.py <board_stem> [--json]
e.g.
    python3 scripts/pipeline/resolve_emit_values.py alpha_centauri

Output per body:
    db        — the body's db/systems record (reference layer; principia-class
                fields come straight from here)
    phase3    — {decision label: value} from the report's Decisions table
    phase4    — {axis: [field dicts]} from gated/emitted board rows
    effective — {field: {value, op, source}} — phase3 names overlaid by
                phase4 field names; source ∈ {phase3, phase4}
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _naming import to_url_slug  # noqa: E402
from phase3_decisions import as_simple_dict, parse_decisions  # noqa: E402

APPLY_STATUSES = {"gated", "emitted"}  # passthrough = no override; superseded/open skipped


def _load_db_bodies(roster: list[dict], board_stem: str) -> dict[str, dict]:
    """db records for every body of every roster system mapped to this board."""
    bodies: dict[str, dict] = {}
    for entry in roster:
        if entry.get("board") != board_stem:
            continue
        f = REPO / "db" / "systems" / f"{entry['system']}.json"
        d = json.loads(f.read_text(encoding="utf-8"))
        for s in d.get("stars", []):
            bodies[s["name"]] = {"kind": "star", "host": s["name"], "record": s}
        host = d["stars"][0]["name"] if d.get("stars") else entry["system"]
        for p in d.get("planets", []):
            bodies[p["name"]] = {"kind": "planet", "host": host, "record": p}
    return bodies


def _phase3_for(body: str, kind: str, host: str) -> dict[str, str]:
    """Parsed Decisions for the body's report (slug rule: contract §2)."""
    candidates = [to_url_slug(body)]
    if kind == "planet":
        letter = body.split()[-1].lower()
        candidates.insert(0, f"{to_url_slug(host)}-{letter}")
    for slug in candidates:
        md = REPO / "docs" / "phase3" / f"{slug}.md"
        if md.exists():
            rows = parse_decisions(md.read_text(encoding="utf-8"))
            return as_simple_dict(rows or [])
    return {}


def resolve(board_stem: str) -> dict[str, dict]:
    roster = yaml.safe_load((REPO / "db" / "roster.yaml").read_text(encoding="utf-8"))["confirmed"]
    board_path = REPO / "phase4" / f"{board_stem}.yaml"
    board = yaml.safe_load(board_path.read_text(encoding="utf-8")) if board_path.exists() else {}
    db_bodies = _load_db_bodies(roster, board_stem)

    # phase4 rows grouped per body (fiction bodies appear here without a db record)
    rows_by_body: dict[str, list[dict]] = {}
    for row in (board.get("decisions") or []):
        b = str(row.get("body", "")).strip()
        rows_by_body.setdefault(b, []).append(row)

    out: dict[str, dict] = {}
    for body in sorted(set(db_bodies) | {b for b in rows_by_body if b != "*"}):
        info = db_bodies.get(body)
        p3 = _phase3_for(body, info["kind"], info["host"]) if info else {}
        p4_axes: dict[str, list[dict]] = {}
        effective: dict[str, dict] = {
            name: {"value": val, "op": "set", "source": "phase3"}
            for name, val in p3.items()
        }
        # wildcard rows apply to every db planet; body rows apply to that body
        applicable = list(rows_by_body.get(body, []))
        if info and info["kind"] == "planet":
            applicable += rows_by_body.get("*", [])
        for row in applicable:
            if row.get("status") not in APPLY_STATUSES:
                continue
            axis = str(row.get("axis", ""))
            flds = [f for f in (row.get("fields") or []) if isinstance(f, dict) and f.get("name")]
            if flds:
                p4_axes.setdefault(axis, []).extend(flds)
            for f in flds:
                effective[str(f["name"])] = {
                    "value": f.get("value"),
                    "op": f.get("op", "set"),
                    "source": "phase4",
                }
        out[body] = {
            "db": info["record"] if info else None,
            "phase3": p3,
            "phase4": p4_axes,
            "effective": effective,
        }
    return out


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    resolved = resolve(args[0])
    if "--json" in sys.argv:
        print(json.dumps(resolved, ensure_ascii=False, indent=2, default=str))
        return
    for body, r in resolved.items():
        n4 = sum(len(v) for v in r["phase4"].values())
        n_over = sum(1 for e in r["effective"].values() if e["source"] == "phase4")
        print(
            f"{body:28s} db:{'Y' if r['db'] else '-'} "
            f"phase3:{len(r['phase3']):3d} decisions  "
            f"phase4:{n4:3d} fields  effective:{len(r['effective']):3d} "
            f"({n_over} overridden by phase4)"
        )


if __name__ == "__main__":
    main()
