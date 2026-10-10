# 기록마다 만들어지는 시험 — 적재 · 선언된 가장자리 너머 질의 · 검산식 · 인용 파일 존재와 해시 (phase-2 등록 P4)
"""P4 of rewrite/phase2-impl.frozen.md, generated from the registry: one set of checks per shipped record, nothing
hand-listed. Per record:
- it loads, and its view builds;
- every declared window edge, queried just beyond, gives its declared outcome (a refusal by its id);
- every formula check evaluates through the grammar (note 3 C4) and lies within its stated tolerance;
- every cache cite names a file that exists in the paper cache with the cited sha256 (impl P2/P4, note 3 C3).
  Where the cache is absent the test fails loudly; a host without it by design sets NEARSTARS_PAPERS_ABSENT=declared,
  and the test is then an expected failure counted in the summary, never a silent skip.
Per-side continuity across boundaries (P4's fourth item) waits for the first branched record (P6).

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_materials_generated
"""
import copy
import hashlib
import os
import unittest
from collections.abc import Mapping
from pathlib import Path

from solver import material_checks as mc
from solver import material_registry as mr
from solver import material_view as mv
from solver import stepper as st
from solver.from_v1 import thaw

T_POT = 1600.0
PAPERS = Path(os.environ.get("NEARSTARS_PAPERS") or Path(__file__).resolve().parents[4] / "NearStars/docs/phase3/_papers")
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
            b = float(w[name]) if name in w else None
            if b is None:
                continue
            if name == "p_max":
                yield i, name, b * 1.001, mid_t, e
            elif name == "p_min" and b > 0.0:
                yield i, name, b * 0.999, mid_t, e
            elif name == "t_max":
                yield i, name, mid_p, b + 1.0, e
            elif name == "t_min" and b > 0.0:
                yield i, name, mid_p, b - 1.0, e


class Generated(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recs = _records()

    def test_some_record_is_shipped(self):
        self.assertGreater(len(self.recs), 0)

    def test_views_build(self):
        for rid, rec in self.recs.items():
            with self.subTest(record=rid):
                mv.RecordView(rec, T_POT)

    def test_edges_give_their_declared_outcome(self):
        self.assertGreater(sum(1 for r in self.recs.values() for _ in edge_probes(r)), 0)
        for rid, rec in self.recs.items():
            v = mv.RecordView(rec, T_POT)
            for i, name, p, t, e in edge_probes(rec):
                with self.subTest(record=rid, phase=i, edge=name):
                    s = v.state(p, t)
                    self.assertIsInstance(s, st.Stop, f"beyond {name} gave {s!r}")
                    if "refusal" in e:
                        self.assertEqual(s.record.refusal, e["refusal"])

    def test_formula_checks(self):
        for rid, rec in self.recs.items():
            for r in mc.run_formula_checks(rec, mv.RecordView(rec, T_POT)):
                with self.subTest(record=rid, check=r["quantity"]):
                    self.assertNotIn("stop", r, r.get("stop"))
                    self.assertTrue(r["passed"], r)

    def test_cache_cites_exist_with_their_hash(self):
        if not PAPERS.is_dir():
            self.fail(f"paper cache not found at {PAPERS}; set NEARSTARS_PAPERS, or NEARSTARS_PAPERS_ABSENT=declared")
        n = 0
        for rid, rec in self.recs.items():
            seen = {}
            for path, name, sha in _cache_cites(rec):
                seen.setdefault(name, (path, sha))
            for name, (path, sha) in seen.items():
                with self.subTest(record=rid, file=name):
                    f = PAPERS / name
                    self.assertTrue(f.is_file(), f"{path}: {name} not in the cache")
                    self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(), sha, path)
                    n += 1
        self.assertGreater(n, 0, "no cache cite was checked")

    # A host without the cache by declaration: the test above becomes an expected failure, counted in the summary
    # («expected failures=1»), never a silent skip (impl P2).
    if not PAPERS.is_dir() and PAPERS_ABSENT_DECLARED:
        test_cache_cites_exist_with_their_hash = unittest.expectedFailure(test_cache_cites_exist_with_their_hash)


class Controls(unittest.TestCase):
    """P4's planted controls: a formula check off by 2× its tolerance fails; an undeclared edge STOPs at load."""

    def test_formula_check_off_by_twice_its_tolerance_fails(self):
        rec = _records()["fe_prem"]
        fc = rec["formula_checks"][0]
        fc["expected"] = float(fc["expected"]) + 2.0 * float(fc["tolerance"]) + abs(
            mc.run_formula_checks(rec)[0]["got"] - float(fc["expected"]))
        self.assertFalse(mc.run_formula_checks(rec)[0]["passed"])

    def test_undeclared_edge_stops_at_load(self):
        rec = copy.deepcopy(_records()["fe_prem"])
        rec["phases"][0]["edges"].pop("p_max")
        self.assertEqual(mr.check_record(rec, "fe_prem.yaml", frozenset(
            s for _p, _n, s in _cache_cites(rec))).id, "material.edge_undeclared")


if __name__ == "__main__":
    unittest.main()
