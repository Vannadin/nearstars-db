# 오라클 대조용 풀이 드라이버 — 천체 v1 파일과 점 목록을 받아 (천체, 상태)마다 비교기 계약 JSON 하나를 쓴다 (비교기 등록 §4)
"""Rewrite side of the regression-oracle comparison (c8's comparator registration §4; b9 registration S10).

    solver/.venv/bin/python -m solver.run_oracle BODY_YAML POINTS_JSON OUT_DIR

- BODY_YAML: a v1 body file (engine/bodies/<stem>.yaml).
- POINTS_JSON: rewrite/oracle/points.py's gen() output [[body, t_pot, tag], …], or «-» for the declared state only.
  The declared state is always written; each row of POINTS_JSON whose body is this file's stem adds one state.
- OUT_DIR: one JSON per (body, state), named <stem>__declared.json or <stem>__<repr(t_pot)>.json.

A T_pot state overrides the potential temperature in memory, on both sides: the Body's SurfaceState for the solve, and
the old BodyState's `potential_temperature` input for legacy_view's chain. Floats are written by repr; the record
fields are fixed by the registration (a missing field is the comparator's STOP).
"""
from __future__ import annotations

import dataclasses
import json
import os
import subprocess
import sys
from pathlib import Path

from solver import context, from_v1, legacy_view as lv, result, solve as sv
from solver import legacy_materials as lm

interior = lm.interior


def _header(options, solve_id):
    import numpy
    import scipy
    tree = subprocess.run(["git", "-C", str(Path(__file__).resolve().parent.parent), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    return {"tree": tree, "venv": sys.prefix, "python": sys.version.split()[0], "numpy": numpy.__version__,
            "scipy": scipy.__version__, "options": result.plain(dataclasses.asdict(options)), "solve_id": solve_id}


def _legacy_nodes(chain) -> dict:
    out = {}
    for node, r in chain.body.results.items():
        if node == "interior_layers":
            continue
        out[node] = {"verdict_kind": interior.verdict_of(r).kind, "applicable": bool(r.applicable),
                     "values": result.plain(dict(r.values)), "units": dict(r.units)}
    return out


def _with_t_pot(body, t_pot):
    return dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=t_pot))


def one(body_yaml: str, state, options=context.Options()) -> dict:
    """The comparator record of one (body, state). `state` is «declared» or a T_pot float."""
    stem = Path(body_yaml).stem
    got = from_v1.load_v1(body_yaml)
    body = got[0] if isinstance(got, tuple) else got
    rec = {"header": None, "body": stem, "state": state, "outcome_kind": None, "quantities": [], "boundaries": [],
           "refusal": None, "no_answer": None, "legacy_nodes": {}, "table_read": False}
    if isinstance(body, result.Refusal):
        rec.update(header=_header(options, ""), outcome_kind="refusal",
                   refusal={"id": body.id, "evidence": result.plain(dict(body.evidence))})
        return rec
    if state != "declared":
        body = _with_t_pot(body, float(state))
    out, _warm = sv.solve(body, options)
    if isinstance(out, result.Answer):
        sid = out.quantities[0].provenance.solver.solve_id if out.quantities else ""
        rec.update(header=_header(options, sid), outcome_kind="answer",
                   quantities=[result.plain(q) for q in out.quantities],
                   boundaries=[result.plain(b) for b in out.boundaries])
        chain = lv.run_chain(body_yaml, out, t_pot=None if state == "declared" else float(state))
        rec["legacy_nodes"] = _legacy_nodes(chain)
        r = chain.body.results.get("core_thermal_history")
        rec["table_read"] = bool(r is not None and r.applicable)
    elif isinstance(out, result.NoAnswer):
        rec.update(header=_header(options, ""), outcome_kind="no_answer",
                   no_answer={"reason": out.reason, "evidence": result.plain(dict(out.evidence))})
    else:
        rec.update(header=_header(options, ""), outcome_kind="refusal",
                   refusal={"id": out.id, "evidence": result.plain(dict(out.evidence))})
    return rec


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 3:
        print(__doc__)
        return 2
    body_yaml, points_json, out_dir = argv
    stem = Path(body_yaml).stem
    states = ["declared"]
    if points_json != "-":
        rows = json.loads(Path(points_json).read_text(encoding="utf-8"))
        states += [float(t) for b, t, _tag in rows if b == stem]
    os.makedirs(out_dir, exist_ok=True)
    for state in states:
        rec = one(body_yaml, state)
        name = f"{stem}__{'declared' if state == 'declared' else repr(state)}.json"
        Path(out_dir, name).write_text(json.dumps(rec, ensure_ascii=False, allow_nan=False, indent=1) + "\n",
                                       encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
