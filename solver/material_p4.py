# 기록별 생성 검사 — 가장자리 너머 · 검산식 · 장 겹침 · 빈 거절 영역 · 이음매 · 인용 해시 · 어디서도 답하지 않는 기록 (impl P4, note 3 C2)
"""The per-record checks of P4, shared by the test suite (solver/tests/test_materials_generated.py) and the checker
(`python -m solver.materials check`, impl note 3 C2: «every load check, then the record's generated tests and formula
checks»). Each check returns data; the caller asserts or prints."""
from __future__ import annotations

import hashlib
import math
import os
from collections.abc import Mapping
from pathlib import Path

from solver import material_checks as mc
from solver import material_registry as mr
from solver import material_view as mv
from solver import stepper as st
from solver.from_v1 import thaw

T_POT = 1600.0


def _default_papers() -> Path:
    """The main checkout's paper cache: the git common dir's parent (any worktree of ~/Desktop/NearStars finds it),
    else beside the worktree (68 N20). NEARSTARS_PAPERS overrides both."""
    import subprocess
    here = Path(__file__).resolve().parent
    p = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=here,
                       capture_output=True, text=True)
    if p.returncode == 0 and p.stdout.strip():
        return Path(p.stdout.strip()).parent / "docs/phase3/_papers"
    return here.parents[2] / "NearStars/docs/phase3/_papers"


PAPERS = Path(os.environ.get("NEARSTARS_PAPERS") or _default_papers())
PAPERS_ABSENT_DECLARED = os.environ.get("NEARSTARS_PAPERS_ABSENT") == "declared"


def _records():
    reg = mr.load()
    if isinstance(reg, mr.LoadStop):
        raise AssertionError(f"registry STOP: {reg.id} {dict(reg.evidence)}")
    return {k: thaw(v) for k, v in reg.records.items()}


def _cache_cites(x, path="record"):
    if isinstance(x, Mapping):
        if "cache" in x and "sha256" in x:
            yield path, x["cache"], x["sha256"]
        for k, v in x.items():
            yield from _cache_cites(v, f"{path}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _cache_cites(v, f"{path}[{i}]")


def edge_probes(rec):
    """(phase index, edge name, P, T) just beyond each declared window edge."""
    for i, ph in enumerate(rec["phases"]):
        w = ph["window"]
        mid_t = 0.5 * (float(w.get("t_min", 300.0)) + float(w.get("t_max", 3000.0)))
        mid_p = 0.5 * (float(w["p_min"]) + min(float(w["p_max"]), 1e11))
        for name, e in ph["edges"].items():
            if name not in w:                                       # 68 N21
                raise AssertionError(f"phase {ph['id']}: edge {name} declared without a bound in the window")
            b = float(w[name])
            if not math.isfinite(b):                               # an edge at infinity is never reached
                continue
            if name == "p_max":
                yield i, name, b * 1.001, mid_t, e
            elif name == "p_min" and b > 0.0:
                yield i, name, b * 0.999, mid_t, e
            elif name == "t_max":
                yield i, name, mid_p, b + 1.0, e
            elif name == "t_min" and b > 0.0:
                yield i, name, mid_p, b - 1.0, e


def cite_problems(recs, papers: Path = None) -> tuple:
    """68 T4: every (path, file, sha256) triple is compared, each file hashed once; not one cite per file.
    Returns (cites checked, [problem texts])."""
    papers = PAPERS if papers is None else papers
    hashes, n, bad = {}, 0, []
    for rid, rec in recs.items():
        for path, name, sha in _cache_cites(rec):
            f = papers / name
            if not f.is_file():
                bad.append(f"{rid} {path}: {name} not in the cache")
                continue
            if name not in hashes:
                hashes[name] = hashlib.sha256(f.read_bytes()).hexdigest()
            if hashes[name] != sha:
                bad.append(f"{rid} {path}: sha256 {sha[:12]}… is not {name}'s {hashes[name][:12]}…")
            n += 1
    return n, bad


def probe_grids(rec) -> list:
    """The record's declared probe grids: field_probe (one) and field_probes (several boxes, own dp/dt each)."""
    return ([rec["field_probe"]] if rec.get("field_probe") else []) + list(rec.get("field_probes") or ())


def _walk(pr):
    box = pr["box"]
    p_lo, p_hi, t_lo, t_hi = (float(box[k]) for k in ("p_min", "p_max", "t_min", "t_max"))
    dp, dt = float(pr["dp"]), float(pr["dt"])
    p = p_lo
    while p <= p_hi + 1e-9 * dp:
        t = t_lo
        while t <= t_hi + 1e-9 * dt:
            yield p, t
            t += dt
        p += dp


def probe_overlaps(rec) -> tuple:
    """Impl note 6 item 5: walk a field record's declared probe grids; every node must give one phase or a declared
    refusal, and an overlap anywhere is a failure. Returns (nodes walked, [overlap nodes])."""
    grids = probe_grids(rec)
    if not grids:
        return 0, []
    v = mv.RecordView(rec, T_POT)
    n, bad = 0, []
    for pr in grids:
        for p, t in _walk(pr):
            got = v._phase_at(p, t)
            n += 1
            if isinstance(got, st.Stop) and got.record.refusal == "material.field_overlap":
                bad.append((p, t, got.record.why))
    return n, bad


def empty_refusal_regions(rec) -> list:
    """Ids/reasons of declared refusal regions that hold no node of any probe grid."""
    v = mv.RecordView(rec, T_POT)
    hit = set()
    for pr in probe_grids(rec):
        for p, t in _walk(pr):
            r = v.refusal_region_at(p, t)
            if r is not None:
                hit.add(r["reason"])
    return [r["reason"] for r in rec["refusals"] if r["reason"] not in hit]


def seam_problems(rec) -> list:
    """Phase-2 design note 5: each source seam's measured step against the global SEAM_NIL; (between, step, why)."""
    from solver import material_joins as mj
    v = mv.RecordView(rec, T_POT)
    out = []
    for sm in rec.get("source_seams", ()):
        got = mj.seam_delta(v, sm)
        if isinstance(got, st.Stop):
            out.append((tuple(sm["between"]), None, f"cannot evaluate: {got.record.why}"))
            continue
        over = {k: got[k] for k in mr.SEAM_NIL if not got[k] <= mr.SEAM_NIL[k]}
        if got["nodes"] == 0 or over:
            out.append((tuple(sm["between"]), got, f"above the nil step {dict(mr.SEAM_NIL)}: {over}"))
    return out




def answers_inside(rec) -> list:
    """C7's first cold-run stuck point: a record can load and answer nowhere (a cold curve with no thermal model:
    γ is asked at every point). Each phase is asked at its window's middle; [(phase, P, T, why)] where it refuses."""
    v = mv.RecordView(rec, T_POT)
    out = []
    for ph in rec["phases"]:
        w = ph["window"]
        p_hi = float(w["p_max"]) if math.isfinite(float(w["p_max"])) else max(10.0 * float(w["p_min"]), 1e10)
        p = 0.5 * (float(w["p_min"]) + p_hi)
        t = 0.5 * (float(w.get("t_min", 300.0)) + float(w.get("t_max", 3000.0)))
        got = v._phase_at(p, t)
        if isinstance(got, st.Stop) or got.id != ph["id"]:
            continue                                    # another phase holds the middle (a branched record)
        s = v.state(p, t)
        if isinstance(s, st.Stop):
            out.append((ph["id"], p, t, getattr(s.record, "why", repr(s.record))))
    return out


def record_problems(rec, papers: Path = None) -> list:
    """Every generated check on one record, as [(what is wrong, how to fix)] (impl note 3 C2)."""
    out = []
    for r in mc.run_formula_checks(rec, mv.RecordView(rec, T_POT)):
        if "stop" in r:
            out.append((f"formula check «{r['quantity']}» cannot be evaluated: {r['stop'].why}",
                        "use the check grammar: constants by path (params.k0), state values, curve(), melt_p(), rho()"))
        elif not r["passed"]:
            out.append((f"formula check «{r['quantity']}»: got {r['got']:.6g}, expected {r['expected']:.6g} ± "
                        f"{r['tolerance']:.3g}{' (a disclosed fail that now passes: stale)' if r.get('disclosed') else ''}",
                        "re-read the printed value and its unit; never widen the tolerance after seeing the miss"))
    v = mv.RecordView(rec, T_POT)
    for i, name, p, t, e in edge_probes(rec):
        if "band" in e:                                 # a band edge answers past the bound, with its band
            continue
        got = v._phase_at(p, t) if rec.get("kind") == "branched" else v.state(p, t)
        pid = rec["phases"][i]["id"]
        if not isinstance(got, st.Stop):
            if rec.get("kind") == "branched" and got.id != pid:
                continue
            out.append((f"phase {pid}: just beyond its {name} edge ({p:g} Pa, {t:g} K) it still answers",
                        "the window bound and the edge must agree: move the bound or declare the edge"))
        elif "refusal" in e and rec.get("kind") != "branched" and got.record.refusal != e["refusal"]:
            out.append((f"phase {pid}: beyond {name} it refuses as {got.record.refusal}, declared {e['refusal']}",
                        "declare the refusal the view gives there, or fix the window"))
    for pid, p, t, why in answers_inside(rec):
        out.append((f"phase {pid} answers nowhere: at its window's middle ({p:g} Pa, {t:g} K) it refuses ({why})",
                    "the record must answer inside its window; read the reason. «γ asked …» means no thermal model: "
                    "give thermal.pressure constants (alpha_k, c_v) with phase_constants over the γ window, or thermal "
                    "sets, or use a library / evaluator / table form"))
    if rec.get("kind") == "branched" and rec.get("choice") == "field":
        n, bad = probe_overlaps(rec)
        if not probe_grids(rec):
            out.append(("a field record declares no probe grid", "add field_probe {box, dp, dt} (impl note 6 item 5)"))
        for p, t, why in bad:
            out.append((f"fields overlap at ({p:g} Pa, {t:g} K): {why}", "make the declared curves and fields meet"))
    if rec.get("refusals"):
        for reason in empty_refusal_regions(rec):
            out.append((f"refusal region «{reason}» holds no probe node", "widen the probe grid or move the region"))
    for between, _got, why in seam_problems(rec):
        out.append((f"source seam {between}: {why}", "a seam in T needs one family and a nil step (design note 5)"))
    papers = PAPERS if papers is None else papers
    if papers.is_dir():
        _n, bad = cite_problems({rec["id"]: rec}, papers)
        out += [(b, "register the PDF with add-source and copy its sha256 into the cite") for b in bad]
    return out
