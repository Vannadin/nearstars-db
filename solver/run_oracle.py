# 오라클 대조용 풀이 드라이버 — 천체 v1 파일과 점 목록을 받아 (천체, 상태)마다 비교기 계약 JSON 하나를 쓴다 (비교기 등록 §4)
"""Rewrite side of the regression-oracle comparison (c8's comparator registration §4; b9 registration S10).

    solver/.venv/bin/python -m solver.run_oracle BODY_YAML POINTS_JSON OUT_DIR [--sensitivity-dt K]

- BODY_YAML: a v1 body file (engine/bodies/<stem>.yaml).
- POINTS_JSON: rewrite/oracle/points.py's gen() output [[body, t_pot, tag], …], or «-» for the declared state only.
  The declared state is always written; each distinct T_pot of POINTS_JSON whose body is this stem adds one state.
- OUT_DIR: must be absent or empty (no stale files). One JSON per (body, state), <stem>__declared.json or
  <stem>__<repr(t_pot)>.json, written to a temporary directory first and moved into place only when every state ran.
- --sensitivity-dt: the §A1.7 sensitivity δ in K (default 10; 0 switches the field off). It is in each header's options.
- --no-chain-for-points: T_pot states skip the old chain (legacy_nodes {}, table_read false; header «chain» false). The
  O9 comparison reads interior_layers and the verdict only (compare.py judge_point); declared states keep the chain.
Exit 0 on success; 2 on any STOP (bad arguments, a non-empty OUT_DIR, an exception), with nothing written.

A T_pot state overrides the potential temperature in memory, on both sides: the Body's SurfaceState for the solve, and
the old BodyState's `potential_temperature` for legacy_view's chain. A body that declares no T_pot gets no T_pot state:
such a row is a refusal record (rule `t_pot_state_without_t_pot`). On a refusal or no-answer the old chain still runs,
with the refusal injected as interior_layers' out-of-domain result, so the old nodes decline as they did (r2 B3).
"""
from __future__ import annotations

import dataclasses
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from solver import context, from_v1, legacy_view as lv, member as mb, result, solve as sv
from solver import legacy_materials as lm

interior = lm.interior
ORACLE_TREE = "097a8aa3cfaf0b42f0b8c3a451a391095cc5c6cc"
REPO = Path(lm._ENGINE).parent


def _git(*args) -> str:
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def _header(options, solve_id):
    import numpy
    import scipy
    engine_same = subprocess.run(["git", "-C", str(REPO), "diff", "--quiet", ORACLE_TREE, "--", "engine"]).returncode == 0
    return {"tree": _git("rev-parse", "HEAD"), "venv": sys.prefix, "python": sys.version.split()[0],
            "numpy": numpy.__version__, "scipy": scipy.__version__,
            "options": result.plain(dataclasses.asdict(options)), "solve_id": solve_id,
            "engine_identical_to_oracle_tree": engine_same, "oracle_tree": ORACLE_TREE,
            "dirty": bool(_git("status", "--porcelain", "--", "solver", "engine"))}


def _committed_blob(rel_path: str) -> str:
    return _git("rev-parse", f"{ORACLE_TREE}:{rel_path}")


def _legacy(rec, chain):
    out = {}
    for node, r in chain.body.results.items():
        if node == "interior_layers":
            continue
        out[node] = {"verdict_kind": interior.verdict_of(r).kind, "applicable": bool(r.applicable),
                     "values": result.plain(dict(r.values)), "units": dict(r.units)}
    rec["legacy_nodes"] = out
    # table_read: the history actually read O3's table, i.e. load_for returned a grid from a file whose blob equals the
    # oracle tree's committed table (t2 note 2's frozen-table mode; r2 run_oracle B1)
    rec["table_read"] = any(ok and blob is not None and blob == _committed_blob(path) for path, blob, ok in
                            chain.table_reads)


def _sid(body, options, answer=None) -> str:
    if answer is not None and answer.quantities:
        return answer.quantities[0].provenance.solver.solve_id
    return context.solve_id_of(sv._canonical(body), lm.material_bytes(), options) if body is not None else ""


def one(body_yaml: str, state, options=context.Options(), chain: bool = True) -> dict:
    """The comparator record of one (body, state). `state` is «declared» or a T_pot float. `chain` False skips the old
    chain (legacy_nodes stays {}), for O9 states only (--no-chain-for-points)."""
    rec = _one(body_yaml, state, options, chain if state != "declared" else True)
    rec["header"]["chain"] = chain or state == "declared"
    return rec


def _one(body_yaml: str, state, options, chain: bool) -> dict:
    stem = Path(body_yaml).stem
    got = from_v1.load_v1(body_yaml)
    body = got[0] if isinstance(got, tuple) else got
    rec = {"header": None, "body": stem, "state": state, "outcome_kind": None, "quantities": [], "boundaries": [],
           "refusal": None, "no_answer": None, "legacy_nodes": {}, "table_read": False}
    t_pot = None if state == "declared" else float(state)
    if isinstance(body, result.Refusal):
        rec.update(header=_header(options, ""), outcome_kind="refusal",
                   refusal={"id": body.id, "evidence": result.plain(dict(body.evidence))})
        chain and _legacy(rec, lv.run_chain(body_yaml, None, refusal_text=body.text, t_pot=t_pot))
        return rec
    if t_pot is not None and body.surface.t_pot is None:
        rec.update(header=_header(options, _sid(body, options)), outcome_kind="refusal",
                   refusal={"id": "input.cross_field", "evidence": {
                       "rule": "t_pot_state_without_t_pot",
                       "detail": f"{stem} declares no potential temperature; a T_pot state has no meaning for it"}})
        return rec
    if t_pot is not None:
        got_m = mb.member_for(body_yaml, body)         # an inverse body's T_pot state is its forward member (ruling)
        if got_m is not None:
            fb, info = got_m
            rec["member"] = result.plain(info)
            if fb is None:
                rec.update(header=_header(options, _sid(body, options)), outcome_kind="refusal",
                           refusal={"id": "input.cross_field", "evidence": {
                               "rule": "member_needs_declared_answer",
                               "detail": f"{stem}'s declared state did not answer, so it has no forward member"}})
                return rec
            body = fb
        body = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=t_pot))
    out, _warm = sv.solve(body, options)
    if isinstance(out, result.Answer):
        rec.update(header=_header(options, _sid(body, options, out)), outcome_kind="answer",
                   quantities=[result.plain(q) for q in out.quantities],
                   boundaries=[result.plain(b) for b in out.boundaries])
        chain and _legacy(rec, lv.run_chain(body_yaml, out, t_pot=t_pot))
    elif isinstance(out, result.NoAnswer):
        rec.update(header=_header(options, _sid(body, options)), outcome_kind="no_answer",
                   no_answer={"reason": out.reason, "evidence": result.plain(dict(out.evidence))})
        chain and _legacy(rec, lv.run_chain(body_yaml, None, refusal_text=out.text, t_pot=t_pot))
    else:
        rec.update(header=_header(options, _sid(body, options)), outcome_kind="refusal",
                   refusal={"id": out.id, "evidence": result.plain(dict(out.evidence))})
        chain and _legacy(rec, lv.run_chain(body_yaml, None, refusal_text=out.text, t_pot=t_pot))
    return rec


def states_for(stem: str, points_json: str) -> list:
    states = ["declared"]
    if points_json != "-":
        rows = json.loads(Path(points_json).read_text(encoding="utf-8"))
        for b, t, _tag in rows:
            if b == stem and float(t) not in states:
                states.append(float(t))
    return states


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    dt = 10.0
    if "--sensitivity-dt" in argv:
        i = argv.index("--sensitivity-dt")
        try:
            dt = float(argv[i + 1])
        except (IndexError, ValueError):
            print("STOP: --sensitivity-dt needs a number")
            return 2
        del argv[i:i + 2]
    chain = "--no-chain-for-points" not in argv
    if not chain:
        argv.remove("--no-chain-for-points")
    if len(argv) != 3:
        print(__doc__)
        return 2
    body_yaml, points_json, out_dir = argv
    out = Path(out_dir)
    if out.exists() and any(out.iterdir()):
        print(f"STOP: {out} is not empty (stale files would mix into the comparison)")
        return 2
    options = context.Options(sensitivity_dt=dt)
    stem = Path(body_yaml).stem
    tmp = Path(tempfile.mkdtemp(prefix=f"run_oracle_{stem}_"))
    try:
        for state in states_for(stem, points_json):
            rec = one(body_yaml, state, options, chain)
            name = f"{stem}__{'declared' if state == 'declared' else repr(state)}.json"
            (tmp / name).write_text(json.dumps(rec, ensure_ascii=False, allow_nan=False, indent=1) + "\n",
                                    encoding="utf-8")
    except Exception as exc:                         # a STOP: nothing is written to OUT_DIR
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"STOP: {type(exc).__name__}: {exc}")
        return 2
    out.mkdir(parents=True, exist_ok=True)
    for f in sorted(tmp.iterdir()):
        shutil.move(str(f), out / f.name)
    tmp.rmdir()
    return 0


if __name__ == "__main__":
    sys.exit(main())
