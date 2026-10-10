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
(the paper cache is found through the git common dir; set NEARSTARS_PAPERS for a clone elsewhere)
"""
import copy
import hashlib
import math
import os
import sys
import tempfile
import unittest
from collections.abc import Mapping
from pathlib import Path

from solver import material_checks as mc
from solver import material_registry as mr
from solver import material_view as mv
from solver import stepper as st
from solver.from_v1 import thaw

from solver.material_p4 import (PAPERS, PAPERS_ABSENT_DECLARED, T_POT, _cache_cites, _records,  # noqa: E402,F401
                                 _walk, cite_problems, edge_probes, empty_refusal_regions, probe_grids,
                                 probe_overlaps, seam_problems)


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
                    if rec.get("kind") == "branched":
                        # beyond one phase's edge another phase may hold the point; the phase itself never does
                        got = v._phase_at(p, t)
                        if not isinstance(got, st.Stop):
                            self.assertNotEqual(got.id, rec["phases"][i]["id"], f"beyond {name} still {got.id}")
                            continue
                        s = got
                    else:
                        s = v.state(p, t)
                    self.assertIsInstance(s, st.Stop, f"beyond {name} gave {s!r}")
                    if "refusal" in e and rec.get("kind") != "branched":
                        self.assertEqual(s.record.refusal, e["refusal"])

    def test_formula_checks(self):
        """Each check within tolerance, or a disclosed fail (a cached source prints the disagreement) that still
        misses; a disclosed check that passes is stale and fails."""
        for rid, rec in self.recs.items():
            for r in mc.run_formula_checks(rec, mv.RecordView(rec, T_POT)):
                with self.subTest(record=rid, check=r["quantity"]):
                    self.assertNotIn("stop", r, r.get("stop"))
                    self.assertTrue(r["passed"], ("stale disclosure: " if r.get("disclosed") else "") + repr(r))

    def test_band_methods_evaluate(self):
        """68 N26: every band method in a shipped record evaluates through the grammar, so a broken method fails the
        suite before any solve meets it."""
        n = 0
        for rid, rec in self.recs.items():
            v = mv.RecordView(rec, T_POT)
            for pi, ph in enumerate(rec["phases"]):
                for si, s in enumerate(ph["thermal"].get("sets", ())):
                    band = (s.get("edge_above") or {}).get("band") or {}
                    if "method" not in band:
                        continue
                    with self.subTest(record=rid, phase=pi, set=si):
                        got = mc.evaluate(band["method"], ph, {}, mc.view_spread(v, pi))
                        self.assertNotIsInstance(got, mc.CheckStop, got)
                        n += 1
        self.assertGreater(n, 0)

    def test_declared_refusal_regions_are_not_empty(self):
        """c8: each declared refusal region holds at least one node of the record's probe grid."""
        for rid, rec in self.recs.items():
            regions = rec.get("refusals") or ()
            if not regions:
                continue
            with self.subTest(record=rid):
                self.assertTrue(probe_grids(rec))
                self.assertEqual(empty_refusal_regions(rec), [])

    def test_field_records_have_no_overlap_on_their_probe_grid(self):
        for rid, rec in self.recs.items():
            if rec.get("kind") == "branched" and rec.get("choice") == "field":
                with self.subTest(record=rid):
                    self.assertTrue(probe_grids(rec), "a field record declares its probe grid(s) (impl note 6 item 5)")
                    n, bad = probe_overlaps(rec)
                    self.assertGreater(n, 0)
                    self.assertEqual(bad, [])

    def test_source_seams_are_nil(self):
        """Phase-2 design note 5 (r2 SB1): a source seam in T inside one physical phase is a STOP above the nil step."""
        for rid, rec in self.recs.items():
            if rec.get("source_seams"):
                with self.subTest(record=rid):
                    self.assertEqual(seam_problems(rec), [])

    def test_taper_zones_pass_their_physical_checks(self):
        """r2 on 48770cb0 (1): every shipped taper zone, walked at its measured source's data-range T ends and
        midpoint, has ρ rising with P; a failure means the join must be declared a seam (note 4 item 1.5)."""
        from solver import material_joins as mj
        for rid, rec in self.recs.items():
            v = mv.RecordView(rec, T_POT)
            for pi, ph in enumerate(rec["phases"]):
                for j in ph.get("joins_within", ()):
                    if j["kind"] != "taper":
                        continue
                    a = next(s for s in ph["sources"] if s["id"] == j["between"][0])
                    dr = a["data_range"]
                    temps = [float(dr["t_min"]), 0.5 * (float(dr["t_min"]) + float(dr["t_max"])), float(dr["t_max"])] \
                        if "t_min" in dr and "t_max" in dr else [T_POT]
                    with self.subTest(record=rid, phase=ph["id"], join=tuple(j["between"])):
                        out = mj.taper_zone_checks(v, pi, j, temps)
                        # 68 N51: the K_T distortion is printed for every taper, passing or not
                        sys.stderr.write(f"\n[P4] taper {rid}/{ph['id']} {tuple(j['between'])}: "
                                         f"max K_T distortion ×{out['max_kt_factor']:.3g} over T {temps}\n")
                        # 68 N50: a refusal inside the zone fails too, unless a declared refusal region holds it
                        bad = [f for f in out["failures"] if v.refusal_region_at(f[0], f[1]) is None]
                        self.assertEqual(bad, [])

    def test_cache_cites_exist_with_their_hash(self):
        if not PAPERS.is_dir():
            self.fail(f"paper cache not found at {PAPERS}; set NEARSTARS_PAPERS, or NEARSTARS_PAPERS_ABSENT=declared")
        n = 0
        n, bad = cite_problems(self.recs)
        self.assertEqual(bad, [])
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

    def test_second_cite_of_a_file_with_another_files_sha_fails(self):
        """68 T4 (N25: runs everywhere, no real cache): two cites of one file, the second carrying the other registered
        file's sha256, give exactly one problem."""
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp, "a.pdf"), Path(tmp, "b.pdf")
            a.write_bytes(b"%PDF-1.4 a\n")
            b.write_bytes(b"%PDF-1.4 b\n")
            sa, sb = (hashlib.sha256(x.read_bytes()).hexdigest() for x in (a, b))
            rec = {"x": {"cache": "a.pdf", "sha256": sa}, "y": {"cache": "a.pdf", "sha256": sb},
                   "z": {"cache": "b.pdf", "sha256": sb}}
            self.assertEqual(cite_problems({"toy": rec}, Path(tmp))[0], 3)
            self.assertEqual(len(cite_problems({"toy": rec}, Path(tmp))[1]), 1)
            rec["y"]["sha256"] = sa
            self.assertEqual(cite_problems({"toy": rec}, Path(tmp))[1], [])

    def test_probe_finds_an_overlap(self):
        """Impl note 6 item 5 control: the toy field record with VI no longer bounded by VII overlaps above 2.2 GPa;
        intact, it does not."""
        from solver.tests.test_material_field import field_record
        rec = field_record()
        rec["field_probe"] = {"box": {"p_min": 2.0e9, "p_max": 2.3e9, "t_min": 290.0, "t_max": 310.0},
                              "dp": 0.05e9, "dt": 10.0}
        self.assertEqual(probe_overlaps(rec)[1], [])
        rec["boundaries"] = rec["boundaries"][1:]
        self.assertGreater(len(probe_overlaps(rec)[1]), 0)

    def test_edge_without_a_bound_fails(self):
        """68 N21: a declared edge whose bound is not in the window is a failure, not a skip."""
        rec = _records()["fe_prem"]
        rec["phases"][0]["edges"]["t_max"] = {"refusal": "input.material_out_of_data"}
        with self.assertRaises(AssertionError):
            list(edge_probes(rec))

    def test_disclosed_fail_passes_and_goes_stale(self):
        rec = _records()["fe_prem"]
        fc = rec["formula_checks"][0]
        exp0 = float(fc["expected"])
        fc["disclosed_fail"] = {"source": {"cache": "x.pdf", "page": "1", "where": "p", "sha256": "0" * 64},
                                "why": "toy", "bound": {"value": 2.0e9, "unit": fc["unit"]}}
        self.assertFalse(mc.run_formula_checks(rec)[0]["passed"])          # within tolerance: stale disclosure
        fc["expected"] = exp0 + 1.0e9                                       # a miss inside the printed bound
        r = mc.run_formula_checks(rec)[0]
        self.assertTrue(r["passed"], r)
        self.assertEqual(r["disclosed"], "toy")
        fc["expected"] = exp0 + 5.0e9                                       # a miss beyond the printed bound fails
        self.assertFalse(mc.run_formula_checks(rec)[0]["passed"])
        fc["disclosed_fail"]["bound"] = {"value": 0.6, "unit": "K", "slope": "3.0e9"}   # 0.6 K × 3 GPa/K = 1.8 GPa
        fc["expected"] = exp0 + 1.0e9
        self.assertTrue(mc.run_formula_checks(rec)[0]["passed"])
        fc["disclosed_fail"]["bound"] = {"value": 0.6, "unit": "K"}                     # K without a slope: no way
        self.assertIn("stop", mc.run_formula_checks(rec)[0])
        fc["disclosed_fail"]["bound"] = {"value": 0.6, "unit": "K", "slope": "3.0e9"}   # a literal slope: load STOPs
        self.assertEqual(mr.check_record(rec, "fe_prem.yaml", frozenset(
            s for _p, _n, s in _cache_cites(rec))).id, "material.bad_shape")            # 68 N42
        fc["disclosed_fail"]["source"] = {"doi": "doi:10.1/x"}
        self.assertEqual(mr.check_record(rec, "fe_prem.yaml", frozenset(
            s for _p, _n, s in _cache_cites(rec))).id, "material.bad_cite")

    def test_a_real_step_at_a_seam_fails(self):
        """r2 SB1: a seam between two different-family sources with a 1e-3 Δρ fails P4."""
        class Stub:
            def phase_props(self, pid, p, t):
                return {"rho": 1000.0 * (1.001 if pid == "b" else 1.0), "alpha": 1e-4, "c_p": 2000.0}
        rec = {"source_seams": [{"between": ["a", "b"], "t": {"value": 130.0},
                                 "sampling": {"p_min": 1e5, "p_max": 2e5, "dp": 1e5}}]}
        from solver import material_joins as mj
        got = mj.seam_delta(Stub(), rec["source_seams"][0])
        self.assertAlmostEqual(got["rho"], 1e-3, places=12)
        self.assertEqual(got["nodes"], 2)
        self.assertFalse(got["rho"] <= mr.SEAM_NIL["rho"])

    def test_undeclared_edge_stops_at_load(self):
        rec = copy.deepcopy(_records()["fe_prem"])
        rec["phases"][0]["edges"].pop("p_max")
        self.assertEqual(mr.check_record(rec, "fe_prem.yaml", frozenset(
            s for _p, _n, s in _cache_cites(rec))).id, "material.edge_undeclared")


if __name__ == "__main__":
    unittest.main()
