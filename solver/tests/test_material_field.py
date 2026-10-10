# 안정 영역으로 상 고르기 시험 — SeaFreeze 상은 최소 G, 다른 출처 상은 선언 곡선, 경계는 고압 쪽, 없음·겹침은 거절 (phase-2 impl note 6)
"""Impl note 6: branched phase choice by stability field, on a toy H₂O-like record (SeaFreeze water1 and VI as gibbs
phases, a bm2 «VII» as a sourced phase bounded by declared VI–VII and liquid–VII curves).

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_material_field
"""
import copy
import math
import unittest

from solver import material_view as mv
from solver import stepper as st
from solver.tests.test_material_library import lib_record
from solver.tests.test_material_registry import GOOD, const

T = 300.0
P_VI_VII = 2.2e9          # the toy declared VI–VII line at 300 K (a 0 Pa/K Clapeyron line, printed range 250–350 K)


def field_record():
    water = lib_record(submodel="water1")["phases"][0]
    water.update(id="water1")
    water["field"] = {"kind": "gibbs"}
    water["window"] = {"p_min": 1.0e5, "p_max": 2.3e9, "t_min": 250.0, "t_max": 350.0}
    vi = copy.deepcopy(water)
    vi.update(id="VI", state="solid")
    vi["eos"]["library"]["submodel"] = "VI"
    vii = copy.deepcopy(GOOD["phases"][0])
    vii.update(id="VII")
    vii["field"] = {"kind": "sourced", "source": vii["field"]["source"]}
    vii["window"] = {"p_min": 1.0e9, "p_max": 1.0e10, "t_min": 250.0, "t_max": 350.0}
    vii["edges"] = {"t_min": {"refusal": "input.material_out_of_data"}, "t_max": {"refusal": "input.material_out_of_data"}}
    curve = {"form": "clapeyron", "p0": const(P_VI_VII, "Pa"), "t0": const(T, "K"), "slope": const(0.0, "Pa/K"),
             "t_min": const(250.0, "K"), "t_max": const(350.0, "K")}
    d = {"id": "toy_h2o", "label": "toy", "kind": "branched", "choice": "field", "system": "H2O",
         "fit_composition": "H2O", "phases": [water, vi, vii],
         "boundaries": [{"between": ["VI", "VII"], "kind": "solid_solid", "curve": curve},
                        {"between": ["water1", "VII"], "kind": "melting", "curve": copy.deepcopy(curve)}],
         "formula_checks": GOOD["formula_checks"]}
    return d


class Field(unittest.TestCase):
    def setUp(self):
        self.v = mv.RecordView(field_record(), T)

    def ph(self, p, t=T):
        got = self.v._phase_at(p, t)
        return got if isinstance(got, st.Stop) else got.id

    def test_min_g_picks_within_seafreeze(self):
        self.assertEqual(self.ph(0.5e9), "water1")
        self.assertEqual(self.ph(1.5e9), "VI")

    def test_declared_curve_bounds_both_phases(self):
        """FB1: between the VI–VII line (2.2 GPa) and VI's window end (2.3 GPa) only VII holds."""
        self.assertEqual(self.ph(2.25e9), "VII")
        self.assertEqual(self.ph(2.15e9), "VI")

    def test_points_on_the_curve_take_the_high_p_side(self):
        """FB2: on the curve and one ulp either side: VII, VII, VI (no overlap)."""
        self.assertEqual(self.ph(P_VI_VII), "VII")
        self.assertEqual(self.ph(math.nextafter(P_VI_VII, math.inf)), "VII")
        self.assertEqual(self.ph(math.nextafter(P_VI_VII, 0.0)), "VI")

    def test_curve_outside_its_t_range_refuses_by_name(self):
        s = self.ph(2.25e9, 349.0)
        self.assertNotIsInstance(s, st.Stop)
        rec = field_record()
        for b in rec["boundaries"]:
            b["curve"]["t_max"] = const(320.0, "K")
        s = mv.RecordView(rec, T)._phase_at(2.25e9, 330.0)
        self.assertIsInstance(s, st.Stop)
        self.assertIn("curve is absent", s.record.why)

    def test_boundary_is_inert_where_the_other_phase_cannot_be(self):
        """c8: the liquid–VII curve printed only above 355 K must not refuse VII at 4 GPa / 300 K, where the liquid's
        window (to 2.3 GPa) cannot reach; where both are candidates a missing curve still refuses."""
        rec = field_record()
        rec["boundaries"][1]["curve"]["t_min"] = const(355.0, "K")
        rec["boundaries"][1]["curve"]["t_max"] = const(715.0, "K")
        v = mv.RecordView(rec, T)
        self.assertEqual(v._phase_at(4.0e9, 300.0).id, "VII")
        s = v._phase_at(2.25e9, 300.0)                     # liquid's window holds here too: the curve is needed
        self.assertIsInstance(s, st.Stop)
        self.assertIn("curve is absent", s.record.why)

    def test_no_phase_and_overlap_refuse(self):
        rec = field_record()
        rec["phases"][2]["window"]["p_min"] = 2.25e9        # VII starts above the line: 2.2–2.25 GPa has no phase
        s = mv.RecordView(rec, T)._phase_at(2.22e9, T)
        self.assertIsInstance(s, st.Stop)
        self.assertIn("no phase here", s.record.why)
        rec = field_record()
        rec["boundaries"] = rec["boundaries"][1:]           # VI no longer bounded by VII: 2.25 GPa is claimed by both
        s = mv.RecordView(rec, T)._phase_at(2.25e9, T)
        self.assertIsInstance(s, st.Stop)
        self.assertEqual(s.record.refusal, "material.field_overlap")          # 68 N37: a record defect, own id


class RefusalRegion(unittest.TestCase):
    """c8 (h2o's VI–VII before Bridgman/Pistorius): a declared refusal region wins over the fields it covers, so an
    unsourced boundary band is a named refusal, not an overlap."""

    def _rec(self):
        rec = field_record()
        rec["boundaries"] = rec["boundaries"][1:]                        # no VI–VII line: VI and VII overlap above
        rec["refusals"] = [{"id": "input.material_out_of_data", "reason": "VI–VII boundary not cached (toy)",
                            "box": {"p_min": 2.14e9, "p_max": 2.3e9, "t_min": 250.0, "t_max": 350.0}}]
        return rec

    def test_region_refuses_by_its_id_and_reason(self):
        s = mv.RecordView(self._rec(), T)._phase_at(2.2e9, T)
        self.assertIsInstance(s, st.Stop)
        self.assertEqual(s.record.refusal, "input.material_out_of_data")
        self.assertIn("not cached", s.record.why)

    def test_without_the_region_it_is_an_overlap(self):
        rec = self._rec()
        rec.pop("refusals")
        self.assertEqual(mv.RecordView(rec, T)._phase_at(2.2e9, T).record.refusal, "material.field_overlap")

    def test_probe_sees_no_overlap_and_the_region_is_not_empty(self):
        from solver.tests.test_materials_generated import empty_refusal_regions, probe_overlaps
        rec = self._rec()
        rec["field_probe"] = {"box": {"p_min": 2.0e9, "p_max": 2.3e9, "t_min": 290.0, "t_max": 310.0},
                              "dp": 0.05e9, "dt": 10.0}
        self.assertEqual(probe_overlaps(rec)[1], [])
        self.assertEqual(empty_refusal_regions(rec), [])
        rec["refusals"][0]["box"]["p_min"] = 2.31e9                       # a region off the grid is flagged empty
        self.assertEqual(len(empty_refusal_regions(rec)), 1)

    def test_unchecked_triple_point_needs_a_region(self):
        from solver import material_registry as mr
        rec = self._rec()
        rec["triple_points"] = [{"phases": ["water1", "VI", "VII"], "p": const(2.2e9, "Pa"), "t": const(300.0, "K"),
                                 "unchecked": "inside the declared VI–VII refusal band",
                                 "tolerance": {"dp": 0.02e9, "dt": 1.0, "reason": "toy"}}]
        self.assertIsNone(mr.triple_point_misses(rec, "toy.yaml"))
        rec["refusals"] = []
        self.assertEqual(mr.triple_point_misses(rec, "toy.yaml").id, "material.triple_point_miss")


class RecordFunctions(unittest.TestCase):
    """c8: curve() and melt_p() in the C4 grammar, so R14-08's verification values can be formula checks."""

    def test_curve_and_melt_p(self):
        from solver import material_checks as mc
        rec = field_record()
        v = mv.RecordView(rec, T)
        fns = mc.view_record_fns(v)
        got = mc.evaluate("curve(boundaries[0] @ T=300.0)", rec["phases"][0], {}, None, fns)
        self.assertEqual(got, P_VI_VII)
        p = mc.evaluate("melt_p(VI, water1 @ T=300.0)", rec["phases"][0], {}, None, fns)
        self.assertAlmostEqual(p / 1e9, 0.994, places=2)                 # SeaFreeze's water1–VI crossing at 300 K
        for bad in ("curve(boundaries[0] @ T=400.0)", "melt_p(VI, VII @ T=300.0)", "__curve__(0, 300.0)"):
            with self.subTest(expr=bad):
                self.assertIsInstance(mc.evaluate(bad, rec["phases"][0], {}, None, fns), mc.CheckStop)


class TriplePoint(unittest.TestCase):
    """Impl note 6 item 4: at a declared mixed triple point the declared curves and the min-G boundary meet within the
    tolerance set before measuring. Toy point: water1–VI–VII at 354 K, 2.2 GPa (SeaFreeze's water1–VI crossing there
    is 2.2049 GPa; the toy VI–VII and liquid–VII lines sit at 2.2 GPa); tolerance 0.02 GPa."""

    def _rec(self, p_tp=2.2e9, vi_vii=P_VI_VII):
        rec = field_record()
        for b in rec["boundaries"]:
            b["curve"]["t_max"] = const(360.0, "K")
        rec["boundaries"][0]["curve"]["p0"] = const(vi_vii, "Pa")
        rec["triple_points"] = [{"phases": ["water1", "VI", "VII"], "p": const(p_tp, "Pa"), "t": const(354.0, "K"),
                                 "tolerance": {"dp": 0.02e9, "dt": 1.0, "reason": "toy: set before measuring"}}]
        return rec

    def test_meets_within_tolerance(self):
        from solver import material_registry as mr
        self.assertIsNone(mr.triple_point_misses(self._rec(), "toy.yaml"))

    def test_shifted_declared_curve_stops(self):
        from solver import material_registry as mr
        got = mr.triple_point_misses(self._rec(vi_vii=2.3e9), "toy.yaml")
        self.assertEqual(got.id, "material.triple_point_miss")
        self.assertIn("('VI', 'VII')", got.evidence["why"])

    def test_printed_point_off_the_min_g_boundary_stops(self):
        """Curves moved with the point, so only the min-G boundary (2.2049 GPa) misses 2.3 GPa."""
        from solver import material_registry as mr
        rec = self._rec(p_tp=2.3e9, vi_vii=2.3e9)
        rec["boundaries"][1]["curve"]["p0"] = const(2.3e9, "Pa")
        got = mr.triple_point_misses(rec, "toy.yaml")
        self.assertEqual(got.id, "material.triple_point_miss")
        self.assertIn("min-G boundary water1–VI", got.evidence["why"])


if __name__ == "__main__":
    unittest.main()
