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
         "alpha_range": {"min": 0.0, "max": 3.0e-4, "origin": "toy"},
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
        ea, eb = v.source_density(0, "a", 8.0e9, 450.0), v.source_density(0, "b", 8.0e9, 450.0)
        self.assertAlmostEqual(notes[0].error, max(abs(rb - ra) / ra, abs(eb - ea) / ea))   # floored at the T edge
        self.assertEqual(v.state(8.0e9, 400.0)[2], ())               # inside the data T range: no note

    def test_t_extrapolation_refuses_where_the_other_source_cannot_answer(self):
        d = rec_taper()
        d["phases"][0]["sources"][0]["data_range"].update(t_min=300.0, t_max=450.0)
        s = mv.RecordView(d, 300.0).state(3.0e9, 800.0)            # F&R below its ρ bracket there
        self.assertIsInstance(s, st.Stop)

    def test_zone_and_t_extrapolation_both_ride(self):
        """68 N49: inside the zone and past the measured T range, both grades ride, with the larger band."""
        d = rec_taper()
        d["phases"][0]["sources"][0]["data_range"].update(t_min=300.0, t_max=450.0)
        notes = mv.RecordView(d, 300.0).state(12.6e9, 500.0)[2]
        self.assertEqual(len(notes), 1)
        self.assertIn("blended", notes[0].grade)
        self.assertIn("extrapolated in T", notes[0].grade)

    def test_zone_checks_pass_and_catch_a_planted_inversion(self):
        """r2 (1): the toy zone rises with P and records a K_T distortion ≥ 1; a planted 10 % denser measured source
        over a narrow declared zone makes ρ fall with P somewhere, and the check names it."""
        v = mv.RecordView(rec_taper(), 300.0)
        j = v.record["phases"][0]["joins_within"][0]
        ok = mj.taper_zone_checks(v, 0, j, [400.0])
        self.assertEqual(ok["failures"], [])
        self.assertGreaterEqual(ok["max_kt_factor"], 1.0)
        d = rec_taper()
        d["phases"][0]["sources"][0]["eos"]["params"]["rho0"] = const(1442.4 * 1.10, "kg/m3")   # a denser than b:
        # going up in P the blend moves toward the lighter b, and over a narrow zone that outruns compression
        d["phases"][0]["joins_within"][0]["width"] = {"p_end": 10.3e9, "reason": "toy narrow",
                                                      "declared_before_comparison": "2026-10-11"}
        v2 = mv.RecordView(d, 300.0)
        bad = mj.taper_zone_checks(v2, 0, v2.record["phases"][0]["joins_within"][0], [400.0])
        self.assertTrue(any("rise" in f[2] for f in bad["failures"]), bad)

    def test_alpha_outside_its_declared_range_refuses(self):
        """r2 XB1: α of the extrapolated source outside the declared range refuses (11.58e-5 /K against a max of
        5e-5)."""
        d = rec_taper()
        d["phases"][0]["sources"][0]["data_range"].update(t_min=300.0, t_max=450.0)
        d["phases"][0]["sources"][0]["alpha_range"]["max"] = 5.0e-5
        s = mv.RecordView(d, 300.0).state(8.0e9, 500.0)
        self.assertIsInstance(s, st.Stop)
        self.assertIn("outside its declared range", s.record.why)

    def test_taper_side_without_c_p_stops(self):
        from solver import material_registry as mr
        d = rec_taper()
        d["phases"][0]["sources"][0].pop("c_p_from")
        try:
            mr._sources_and_joins(d["phases"][0], "toy.yaml")
            self.fail("no STOP")
        except mr._Stop as e:
            self.assertEqual(e.stop.id, "material.join_rule")


def rec_preferred():
    """rec_two_sources with b (K0 +1 %) preferred, and c_P from a SeaFreeze VI source a (c_p_from)."""
    d = rec_two_sources()
    ph = d["phases"][0]
    ph["joins_within"][0]["between"] = ["b", "a"]
    for s in ph["sources"]:
        s["c_p_from"] = "a"
    ph["sources"][0]["eos"] = {"form": "library", "reference": ph["sources"][0]["eos"]["reference"],
                               "library": {"name": "SeaFreeze", "version": "1.1.0", "sha256": "0" * 64,
                                           "submodel": "VI"}}
    return d


class PreferredSource(unittest.TestCase):
    """c8 (IAPWS-06 Ih): a phase whose cross-check's preferred source declares an eos other than the phase's own
    answers from that source; a declared note rides in its box."""

    def test_answers_from_the_preferred_source_with_its_note(self):
        d = rec_preferred()
        d["phases"][0]["notes"] = [{"box": {"p_min": 1.0e9, "p_max": 2.0e9, "t_min": 0.0, "t_max": 320.0},
                                    "text": "toy caveat", "source": dict(CITE)}]
        v = mv.RecordView(d, 300.0)
        rho, dtdp, notes = v.state(1.5e9, 300.0)
        self.assertEqual(rho, v.source_density(0, "b", 1.5e9, 300.0))
        self.assertGreater(dtdp, 0.0)
        self.assertEqual([n.text for n in notes], ["toy caveat"])
        self.assertEqual(v.state(1.5e9, 330.0)[2], ())                   # outside the note's box

    def test_outside_the_preferred_sources_data_range_refuses(self):
        """68 N57: the preferred source never answers bare outside its data_range."""
        d = rec_preferred()
        d["phases"][0]["sources"][1]["data_range"] = {"p_min": 1.0e9, "p_max": 2.2e9, "t_min": 250.0, "t_max": 310.0}
        v = mv.RecordView(d, 300.0)
        self.assertIsInstance(v.state(1.5e9, 300.0), tuple)
        for p, t in ((1.5e9, 315.0), (2.25e9, 300.0)):
            with self.subTest(p=p, t=t):
                s = v.state(p, t)
                self.assertIsInstance(s, st.Stop)
                self.assertIn("data_range", s.record.why)
                self.assertIsInstance(v.density(p, t), st.Stop)

    def test_an_evaluator_source_gives_alpha_and_cp_analytically(self):
        """68 N58: IAPWS-06 as the preferred source answers down to 0 K without a T difference below zero."""
        from solver.tests.test_material_evaluators import IAPWS06
        d = rec_two_sources()
        ph = d["phases"][0]
        ph["sources"][1]["eos"] = {"form": "evaluator", "reference": ph["sources"][1]["eos"]["reference"],
                                   "evaluator": {"name": "iapws06_ih",
                                                 "params": {k: {"value": x} for k, x in IAPWS06.items()}}}
        ph["sources"][1].pop("thermal_model")
        ph["sources"][1]["data_range"] = {"p_min": 0.0, "p_max": 2.1e8, "t_min": 0.0, "t_max": 273.16}
        ph["joins_within"][0]["between"] = ["b", "a"]
        v = mv.RecordView(d, 300.0)
        x = mv.Iapws06Ih({k: {"value": y} for k, y in IAPWS06.items()}).at(1.0e8, 100.0)
        got = mj.source_state(v, 0, "b", 1.0e8, 100.0)
        self.assertEqual(got, (x["density"], x["alpha"] * 100.0 / (x["density"] * x["c_p"])))
        for t in (0.3, 0.0):
            with self.subTest(t=t):
                rho, dtdp = mj.source_state(v, 0, "b", 1.0e8, t)
                self.assertTrue(math.isfinite(rho) and math.isfinite(dtdp) and dtdp >= 0.0)

    def test_by_region_sigma_takes_the_smallest_holding_box(self):
        """c8 / IAPWS-06 Table 7: σ by region; overlapping boxes give the smallest; outside every box, else."""
        sig = {"kind": "by_region", "regions": [
            {"box": {"p_min": 0.0, "p_max": 2.0e9, "t_min": 238.0, "t_max": 273.0}, "value": 0.002, "where": "T7"},
            {"box": {"p_min": 0.0, "p_max": 1.6e9, "t_min": 268.0, "t_max": 273.0}, "value": 0.0002, "where": "T7"}],
            "else": {"kind": "not_printed", "where": "Fig. 8"}}
        d = rec_two_sources(sigma_b=sig)
        d["phases"][0]["sources"][1]["sigma_kind"] = "1sigma"
        v = mv.RecordView(d, 300.0)
        for p, t, want in ((1.5e9, 250.0, 0.002), (1.5e9, 270.0, 0.0002), (1.8e9, 270.0, 0.002),
                           (1.5e9, 300.0, 0.0)):
            with self.subTest(p=p, t=t):
                self.assertEqual(mj.source_sigma(v, 0, "b", p, t), want)


class BlendGate(unittest.TestCase):
    """Impl note 3 A3–A4: the conflict gate runs on blends only, pointwise at k = 2; a blend answers a P-only V-blend."""

    @staticmethod
    def _blend(sigma, shared=True, kind="blend"):
        d = rec_two_sources(shared=shared)
        ph = d["phases"][0]
        for src in ph["sources"]:
            src["sigma"] = {"kind": "constant", "value": sigma, "reduction": "toy"}
            src["sigma_kind"] = "1sigma"
        j = ph["joins_within"][0]
        j["kind"] = kind
        if kind == "blend":
            j["weight"] = "smoothstep_p"
        return d

    def test_gate_fires_just_above_k_and_passes_just_below(self):
        """r2 JB3: a planted max r of 1.01·k fails and 0.99·k passes."""
        from solver import material_registry as mr
        v = mv.RecordView(self._blend(1.0), 300.0)
        band = mj.cross_check(v, 0, v.record["phases"][0]["joins_within"][0])["band"]
        for factor, fires in ((1.01, True), (0.99, False)):
            with self.subTest(factor=factor):
                got = mr.source_conflicts(self._blend(band / (factor * mr.K_GATE)), "toy.yaml")
                self.assertEqual(got is not None, fires)
                if fires:
                    self.assertEqual(got.id, "material.source_conflict")
                    self.assertAlmostEqual(got.evidence["max_r"], factor * mr.K_GATE, places=9)
                    self.assertEqual(got.evidence["sigma_allow_formed"], "max (shared data)")

    def test_shared_data_and_quadrature_give_different_verdicts(self):
        """Shared data uses max(σ1, σ2), independent sources √(σ1² + σ2²): with equal σ, r differs by √2."""
        from solver import material_registry as mr
        v = mv.RecordView(self._blend(1.0), 300.0)
        band = mj.cross_check(v, 0, v.record["phases"][0]["joins_within"][0])["band"]
        sigma = band / (1.2 * mr.K_GATE)              # shared: r = 2.4 (fails); quadrature: r = 2.4/√2 = 1.70 (passes)
        self.assertIsNotNone(mr.source_conflicts(self._blend(sigma, shared=True), "toy.yaml"))
        self.assertIsNone(mr.source_conflicts(self._blend(sigma, shared=False), "toy.yaml"))

    def test_a_cross_check_is_never_gated(self):
        """A2: the same failing pair declared as a cross-check is not gated (it is banded and disclosed)."""
        from solver import material_registry as mr
        v = mv.RecordView(self._blend(1.0), 300.0)
        band = mj.cross_check(v, 0, v.record["phases"][0]["joins_within"][0])["band"]
        self.assertIsNotNone(mr.source_conflicts(self._blend(band / 4.0), "toy.yaml"))
        self.assertIsNone(mr.source_conflicts(self._blend(band / 4.0, kind="cross_check"), "toy.yaml"))

    def test_a_node_a_side_cannot_answer_stops_the_gate(self):
        """68 H1: one planted Stop node inside the grid is material.source_conflict naming the side, never skipped."""
        from unittest import mock
        from solver import material_registry as mr
        d = self._blend(1.0)
        real = mv.RecordView.source_density

        def planted(view, pi, sid, p, t):
            if sid == "b" and abs(p - 1.7e9) < 1.0 and t == 320.0:
                return st.Stop("refused", "planted")
            return real(view, pi, sid, p, t)
        with mock.patch.object(mv.RecordView, "source_density", planted):
            got = mr.source_conflicts(d, "toy.yaml")
        self.assertEqual(got.id, "material.source_conflict")
        self.assertIn("side b cannot answer", got.evidence["sigma_allow_formed"])

    def test_overlap_and_sampling_tied_to_the_data_ranges(self):
        """68 H2: the overlap lies in both data ranges and the sampling box is the overlap; a plant of each STOPs."""
        from solver import material_registry as mr

        def ph():
            d = rec_preferred()                                # c_P on both sides (a library source, c_p_from)
            d["phases"][0]["joins_within"][0].update(kind="blend", weight="smoothstep_p")
            return d["phases"][0]
        mr._sources_and_joins(ph(), "toy.yaml")
        wide = ph()
        wide["joins_within"][0]["overlap"] = {"p_min": 1.0e9, "p_max": 2.2e9}           # a's data starts at 1.3 GPa
        wide["joins_within"][0]["sampling"]["box"].update(p_min=1.0e9)
        off = ph()
        off["joins_within"][0]["sampling"]["box"].update(p_max=2.0e9)
        topen = ph()                                       # 68 N60: a T-open overlap, a's data ends at 330 K
        topen["sources"][0]["data_range"]["t_max"] = 330.0
        for name, ph in (("overlap past a data range", wide), ("sampling box not the overlap", off),
                         ("sampling T past a data range", topen)):
            with self.subTest(name), self.assertRaises(mr._Stop) as cm:
                mr._sources_and_joins(ph, "toy.yaml")
            self.assertEqual(cm.exception.stop.id, "material.join_rule")

    def test_blend_is_a_p_only_v_blend(self):
        """A4: inside the overlap V = (1 − w)V_a + w·V_b with w the C¹ smoothstep in P over the overlap's P span; the
        answer is graded «blended (a, b)» with the full |Δρ|/ρ as its band; below the overlap a alone answers."""
        d = rec_preferred()
        ph = d["phases"][0]
        ph["joins_within"][0].update(kind="blend", weight="smoothstep_p")
        v = mv.RecordView(d, 300.0)
        lo, hi = 1.3e9, 2.2e9
        for p in (1.5e9, 1.75e9, 2.0e9):
            with self.subTest(p=p):
                s_ = (p - lo) / (hi - lo)
                w = s_ * s_ * (3 - 2 * s_)
                a, b = ph["joins_within"][0]["between"]
                ra, rb = v.source_density(0, a, p, 300.0), v.source_density(0, b, p, 300.0)
                rho, _dtdp, notes = v.state(p, 300.0)
                self.assertAlmostEqual(rho, 1.0 / ((1 - w) / ra + w / rb), places=9)
                self.assertIn(f"blended ({a}, {b})", notes[-1].grade)
                self.assertAlmostEqual(notes[-1].error, abs(rb - ra) / ra, places=12)
                # 68 on 924e9336: the c_P Maxwell bound rides on its own field, labelled for (dT/dP)_S
                self.assertTrue(notes[-1].dtdp_error is not None and notes[-1].dtdp_error >= 0.0)
                self.assertIn("(dT/dP)_S", notes[-1].dtdp_origin)


if __name__ == "__main__":
    unittest.main()
