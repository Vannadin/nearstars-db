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
        self.assertIn("fields overlap", s.record.why)


if __name__ == "__main__":
    unittest.main()
