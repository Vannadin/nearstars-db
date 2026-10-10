# 출처 잇기 시험 — 출처별 밀도(차가운 곡선 + exp_alpha), 교차 확인 띠와 r, σ 전파·공유 자료·인쇄 안 된 σ (phase-2 impl notes 3–4)
"""Impl notes 3 A1–A3 and 4: source densities and the cross-check computation, on a toy phase whose two sources
are BM2 fits that differ by a known amount.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_material_joins
"""
import copy
import math
import unittest

from solver import material_joins as mj
from solver import material_view as mv
from solver import stepper as st
from solver.tests.test_material_registry import CITE, GOOD, const


def rec_two_sources(k0_b=14.05e9 * 1.01, shared=True, sigma_b=None):
    d = copy.deepcopy(GOOD)
    ph = d["phases"][0]
    bm2 = lambda rho0, k0: {"form": "bm2", "params": {"rho0": const(rho0, "kg/m3"), "k0": const(k0, "Pa")},  # noqa: E731
                            "reference": {"kind": "state", "p": const(1e5, "Pa"), "t": const(300.0, "K")}}
    exp = {"kind": "exp_alpha", "alpha0": const(14.6e-5, "1/K"), "t0": const(300.0, "K")}
    ph["sources"] = [
        {"id": "a", "source": dict(CITE), "basis": "measured", "data_range": {"p_min": 1.3e9, "p_max": 2.2e9},
         "data_range_where": "t", "eos": bm2(1270.0, 14.05e9), "thermal_model": exp,
         "sigma": {"kind": "propagated", "from": {"k0": 0.23e9}, "correlation": "not_printed"}, "sigma_kind": "1sigma"},
        {"id": "b", "source": dict(CITE), "basis": "measured", "data_range": {"p_min": 1.0e9, "p_max": 2.2e9},
         "data_range_where": "t", "eos": bm2(1270.0, k0_b), "thermal_model": exp,
         "sigma": sigma_b or {"kind": "not_printed", "where": "§"}, "sigma_kind": "not_applicable"}]
    join = {"between": ["a", "b"], "kind": "cross_check", "overlap": {"p_min": 1.3e9, "p_max": 2.2e9},
            "sampling": {"box": {"p_min": 1.3e9, "p_max": 2.2e9, "t_min": 300.0, "t_max": 340.0},
                         "dp": 0.1e9, "dt": 20.0}, "k": 2}
    if shared:
        join["shared_data"] = "toy: b's fit includes a's points"
    ph["joins_within"] = [join]
    ph["precedence"] = {"by": "declared", "declared_before_comparison": "2026-10-11"}
    return d


class SourceDensity(unittest.TestCase):
    def test_exp_alpha_scales_the_cold_density(self):
        v = mv.RecordView(rec_two_sources(), 300.0)
        r300, r340 = v.source_density(0, "a", 1.5e9, 300.0), v.source_density(0, "a", 1.5e9, 340.0)
        self.assertAlmostEqual(r340 / r300, math.exp(-14.6e-5 * 40.0), places=12)


class CrossCheck(unittest.TestCase):
    def test_band_r_and_disclosure_threshold(self):
        v = mv.RecordView(rec_two_sources(), 300.0)
        out = mj.cross_check(v, 0, v.record["phases"][0]["joins_within"][0])
        self.assertEqual(len(out["nodes"]), 10 * 3)
        self.assertGreater(out["band"], 0.0)
        self.assertLess(out["band"], 0.01)                       # a 1 % K0 difference moves ρ by well under 1 %
        n = out["nodes"][0]
        self.assertAlmostEqual(n["r"], n["rel"] / n["sigma_allow"])

    def test_identical_sources_give_zero_band(self):
        v = mv.RecordView(rec_two_sources(k0_b=14.05e9), 300.0)
        self.assertEqual(mj.cross_check(v, 0, v.record["phases"][0]["joins_within"][0])["band"], 0.0)

    def test_shared_data_uses_max_and_independent_uses_quadrature(self):
        sig_b = {"kind": "constant", "value": 0.003, "reduction": "toy"}
        for shared in (True, False):
            with self.subTest(shared=shared):
                d = rec_two_sources(shared=shared, sigma_b=sig_b)
                d["phases"][0]["sources"][1]["sigma_kind"] = "1sigma"
                v = mv.RecordView(d, 300.0)
                n = mj.cross_check(v, 0, v.record["phases"][0]["joins_within"][0])["nodes"][0]
                sa = mj.source_sigma(v, 0, "a", n["p"], n["t"])
                want = max(sa, 0.003) if shared else math.sqrt(sa ** 2 + 0.003 ** 2)
                self.assertAlmostEqual(n["sigma_allow"], want, places=15)

    def test_ci90_converts_and_unprinted_is_zero(self):
        d = rec_two_sources(sigma_b={"kind": "constant", "value": 0.0329, "reduction": "toy"})
        d["phases"][0]["sources"][1]["sigma_kind"] = "ci90"
        v = mv.RecordView(d, 300.0)
        self.assertAlmostEqual(mj.source_sigma(v, 0, "b", 1.5e9, 300.0), 0.0329 / 1.645)
        self.assertEqual(mj.source_sigma(mv.RecordView(rec_two_sources(), 300.0), 0, "b", 1.5e9, 300.0), 0.0)


def rec_taper():
    """A toy VII: measured side a = BM2 + exp_alpha (Bezacier-like, c_P from b), computed side b = the F&R evaluator;
    taper from P_e 10.1 GPa to 15.15 GPa (the default 1.5·P_e)."""
    from solver.tests.test_material_evaluators import legacy_params
    d = copy.deepcopy(GOOD)
    ph = d["phases"][0]
    ph["sources"] = [
        {"id": "a", "source": dict(CITE), "basis": "measured", "data_range": {"p_min": 2.2e9, "p_max": 10.1e9},
         "data_range_where": "t", "c_p_from": "b",
         "eos": {"form": "bm2", "params": {"rho0": const(1442.4, "kg/m3"), "k0": const(20.15e9, "Pa")},
                 "reference": {"kind": "state", "p": const(1e5, "Pa"), "t": const(300.0, "K")}},
         "thermal_model": {"kind": "exp_alpha", "alpha0": const(11.58e-5, "1/K"), "t0": const(300.0, "K")},
         "sigma": {"kind": "not_printed", "where": "§"}, "sigma_kind": "not_applicable"},
        {"id": "b", "source": dict(CITE), "basis": "computed", "data_range": {"p_min": 3.3e9, "p_max": 1.0e12},
         "data_range_where": "t",
         "eos": {"form": "evaluator", "reference": {"kind": "state", "p": const(1e5, "Pa"), "t": const(300.0, "K")},
                 "evaluator": {"name": "french_redmer2015", "source": {"formula": "toy"}, "params": legacy_params()}},
         "sigma": {"kind": "not_printed", "where": "§"}, "sigma_kind": "not_applicable"}]
    ph["joins_within"] = [{"between": ["a", "b"], "kind": "taper", "edge_p": 10.1e9, "side": "upper",
                           "weight": "smoothstep_p", "k": 2}]
    ph["precedence"] = {"by": "basis"}
    ph["window"]["p_max"] = 1.0e11
    ph["field"]["box"]["p_max"] = 1.0e11
    return d


class Taper(unittest.TestCase):
    def setUp(self):
        self.v = mv.RecordView(rec_taper(), 300.0)

    def test_measured_below_computed_above(self):
        for p, sid in ((8.0e9, "a"), (20.0e9, "b")):
            with self.subTest(p=p):
                rho, _g, notes = self.v.state(p, 400.0)
                self.assertEqual(rho, self.v.source_density(0, sid, p, 400.0))
                self.assertEqual(notes, ())

    def test_zone_blends_and_carries_the_band(self):
        rho, dtdp, notes = self.v.state(12.6e9, 400.0)
        ra, rb = self.v.source_density(0, "a", 12.6e9, 400.0), self.v.source_density(0, "b", 12.6e9, 400.0)
        self.assertTrue(min(ra, rb) < rho < max(ra, rb))
        self.assertEqual(len(notes), 1)
        self.assertAlmostEqual(notes[0].error, abs(rb - ra) / ra)
        self.assertIn("blended (a extrapolated, b)", notes[0].grade)
        self.assertGreater(dtdp, 0.0)

    def test_continuous_at_the_zone_ends(self):
        for edge in (10.1e9, 15.15e9):
            with self.subTest(edge=edge):
                lo, hi = self.v.state(edge * (1 - 1e-9), 400.0)[0], self.v.state(edge * (1 + 1e-9), 400.0)[0]
                self.assertLess(abs(hi - lo) / lo, 1e-6)

    def test_t_extrapolation_is_graded_and_banded(self):
        """Note 4 item 1.4: below P_e and outside the measured T range (a's data_range 300–450 K here), a's thermal
        model is extrapolated, graded and banded by its difference from b at the same state."""
        d = rec_taper()
        d["phases"][0]["sources"][0]["data_range"].update(t_min=300.0, t_max=450.0)
        v = mv.RecordView(d, 300.0)
        rho, _g, notes = v.state(8.0e9, 500.0)
        self.assertEqual(rho, v.source_density(0, "a", 8.0e9, 500.0))
        self.assertEqual(len(notes), 1)
        self.assertIn("extrapolated in T", notes[0].grade)
        ra, rb = v.source_density(0, "a", 8.0e9, 500.0), v.source_density(0, "b", 8.0e9, 500.0)
        self.assertAlmostEqual(notes[0].error, abs(rb - ra) / ra)
        self.assertEqual(v.state(8.0e9, 400.0)[2], ())               # inside the data T range: no note

    def test_t_extrapolation_refuses_where_the_other_source_cannot_answer(self):
        d = rec_taper()
        d["phases"][0]["sources"][0]["data_range"].update(t_min=300.0, t_max=450.0)
        s = mv.RecordView(d, 300.0).state(3.0e9, 800.0)            # F&R below its ρ bracket there
        self.assertIsInstance(s, st.Stop)

    def test_taper_side_without_c_p_stops(self):
        from solver import material_registry as mr
        d = rec_taper()
        d["phases"][0]["sources"][0].pop("c_p_from")
        try:
            mr._sources_and_joins(d["phases"][0], "toy.yaml")
            self.fail("no STOP")
        except mr._Stop as e:
            self.assertEqual(e.stop.id, "material.join_rule")


if __name__ == "__main__":
    unittest.main()
