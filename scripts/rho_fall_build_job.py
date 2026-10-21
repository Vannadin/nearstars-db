# ρ 떨어짐 집합 빌드의 unitq 작업 진입점 — 표의 T 칸마다 한 단위로 solver.rho_fall_build.cell_falls 를 돌리고 한 문서로 모음(작업자별 뷰 캐시는 solver/ 밖에서, §A6)
"""The unitq job for solver/rho_fall_build.py's build, one unit per T cell. From the engine tree root (PYTHONPATH=.):

    python3 <unitq.py> scripts/rho_fall_build_job.py OUTDIR --slots N -- RECORD_ID

It lives outside solver/ (directing 10-21, 68's recommendation on test_a6_state): the per-worker view cache below is a
job runner's state, not the solver's (phase1-design §A6 scans solver/). The build itself — cell_falls, document, the
stamp — is solver.rho_fall_build's; the set file is the same (its stamp's tool_blob names rho_fall_build.py)."""
import json

from solver import rho_fall_build as rfb

_V = {}                                                  # record id → its view, built once per worker process


def _v(rid):
    if rid not in _V:
        _V[rid] = rfb._view(rid)
    return _V[rid]


def setup(argv):
    v = _v(argv[0])
    return {"units": [(["ib", ib], {"rid": argv[0], "ib": ib}) for ib in range(len(v.ts) - 1)]}


def identity(argv):
    return {"record": argv[0], **rfb._stamp(), "read_blob": rfb._ma().read_blob()}   # parts of one build share one read


def run(payload):
    return rfb.cell_falls(_v(payload["rid"]), payload["ib"])


def plan(state, results):
    todo = [(k, p) for k, p in state["units"] if canon(k) not in results]  # noqa: F821 (set by unitq)
    if todo:
        return todo
    rid = state["units"][0][1]["rid"]
    per_cell = {p["ib"]: results[canon(k)] for k, p in state["units"]}  # noqa: F821
    doc = rfb.document(_v(rid), per_cell)
    return {"files": {f"{rid}.json": json.dumps(doc) + "\n"}}
