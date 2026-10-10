# 물질 기록 뷰 시험 — 형식 항등식, fe_prem 기록 뷰가 옛 LegacyView 와 비트까지 같음(옮긴 상수만 되돌린 채), 창 밖은 선언대로, 띠 Note (phase-2 등록 P3)
"""P3 acceptance of rewrite/phase2-impl.frozen.md: the record view.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_material_view
"""
import math
import unittest

from solver import legacy_materials as lm
from solver import material_registry as mr
from solver import material_view as mv
from solver import stepper as st
from solver.from_v1 import thaw

import eos  # noqa: E402  (engine/, put on the path by legacy_materials)

T_POT = 1600.0
#: Earth's core path and the set seams, plus the printed-scope edge of the Dorogokupets set (350 GPa).
NODES = [(10e9, 2000.0), (19.0e9, 2100.0), (25e9, 2300.0), (35.0e9, 2400.0), (136e9, 4000.0), (250e9, 5000.0),
         (349.99e9, 5400.0), (350.01e9, 5400.0), (358e9, 5500.0)]


def fe_prem(legacy_constants: bool):
    """The shipped record; with `legacy_constants` the constants a finding moved are put back (stage (a) fixtures:
    W-L1-01 αK_T, P5-F1 Dorogokupets V0). Every other value comes from the record (68 H1)."""
    rec = thaw(mr.load()["fe_prem"])
    ev = rec["phases"][0]["thermal"]["sets"][1]["evaluator"]
    if legacy_constants:
        rec["phases"][0]["thermal"]["pressure"]["alpha_k"] = {"value": 0.00121e9, "unit": "Pa/K"}
        ev["params"]["v0"] = {"value": 7.95784e-6, "unit": "m3/mol"}
    return rec


class Forms(unittest.TestCase):
    def test_bm2_is_bme3_at_k0p_4(self):
        a, b = mv._cold_pressure("bm2", 7050.0, 201e9, 9.9), mv._cold_pressure("bme3", 7050.0, 201e9, 4.0)
        for rho in (7050.0, 9000.0, 13000.0):
            self.assertEqual(a(rho), b(rho))

    def test_k0_at_reference(self):
        """Each form's ρ dP/dρ at ρ0 is K0 (eqs (4), (5) at η = 1)."""
        for form in ("bm2", "bme3", "vinet"):
            with self.subTest(form=form):
                p = mv._cold_pressure(form, 4000.0, 2.0e11, 4.5)
                h = 4000.0 * 1e-6
                self.assertAlmostEqual(4000.0 * (p(4000.0 + h) - p(4000.0 - h)) / (2 * h) / 2.0e11, 1.0, places=6)
                self.assertEqual(p(4000.0), 0.0)

    def test_bme4_and_unknown_are_not_built(self):
        with self.assertRaises(ValueError):
            mv._cold_pressure("bme4", 4000.0, 2.0e11, 4.0)


class LegacyNumerics(unittest.TestCase):
    """With the moved constants put back, the record view reproduces LegacyView of fe_prem bit for bit on Earth's core
    path, through the 19/35 GPa set seams and across the 350 GPa printed-scope edge."""

    def test_bit_identical(self):
        v, leg = mv.RecordView(fe_prem(True), T_POT), lm.LegacyView("fe_prem", eos.FE_PREM, T_POT)
        for p, t in NODES:
            with self.subTest(p=p, t=t):
                a, b = v.state(p, t), leg.state(p, t)
                self.assertIsInstance(a, tuple, a)
                self.assertEqual((a[0], a[1]), (b[0], b[1]))

    def test_control_corrected_record_moves(self):
        """Control: the record as shipped (corrected αK_T, V0 as printed) differs from legacy; the equivalence above is
        not vacuous."""
        v, leg = mv.RecordView(fe_prem(False), T_POT), lm.LegacyView("fe_prem", eos.FE_PREM, T_POT)
        a, b = v.state(136e9, 4000.0), leg.state(136e9, 4000.0)
        self.assertNotEqual((a[0], a[1]), (b[0], b[1]))


class Edges(unittest.TestCase):
    def setUp(self):
        self.v = mv.RecordView(fe_prem(False), T_POT)

    def test_past_the_window_refuses_by_its_declared_id(self):
        s = self.v.state(1.3e13, 6000.0)
        self.assertIsInstance(s, st.Stop)
        self.assertEqual(s.record.refusal, "input.material_out_of_data")

    def test_band_note_past_the_printed_scope_only(self):
        self.assertEqual(self.v.state(349.0e9, 5400.0)[2], ())
        notes = self.v.state(351.0e9, 5400.0)[2]
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].grade, "extrapolated beyond printed scope")
        self.assertAlmostEqual(notes[0].error, 0.47418, places=5)        # the method, evaluated from the record

    def test_band_method_that_does_not_evaluate_refuses(self):
        rec = fe_prem(False)
        rec["phases"][0]["thermal"]["sets"][1]["edge_above"]["band"]["method"] = "nothing * 2"
        s = mv.RecordView(rec, T_POT).state(351.0e9, 5400.0)
        self.assertIsInstance(s, st.Stop)
        self.assertEqual(s.record.refusal, "material.check_unknown_name")

    def test_view_holds_its_own_copy(self):
        """68 N27: changing the caller's record after construction does not reach the view."""
        rec = fe_prem(False)
        v = mv.RecordView(rec, T_POT)
        rec["phases"][0]["thermal"]["sets"][1]["edge_above"]["band"]["method"] = "nothing * 2"
        self.assertAlmostEqual(v.state(351.0e9, 5400.0)[2][0].error, 0.47418, places=5)

    def test_seams(self):
        self.assertEqual(self.v.seams(), (19.0e9, 35.0e9, 1.2e13))     # 350 GPa is a band edge, not a seam
        self.assertEqual(self.v.transitions(), ())

    def test_set_delta_t_never_reads_the_phase_table(self):
        """68 N4: a set measures ΔT from its own t_ref, even when the phase carries an adiabat table."""
        ph = self.v.phases[0]
        s = ph.sets[0]
        self.assertIsNotNone(ph.adiabat)
        self.assertEqual(self.v._set_delta_t(s, 3000.0), 3000.0 - s.t_ref)
        self.assertNotEqual(self.v._delta_t(ph, 3000.0, 25e9), 3000.0 - s.t_ref)

    def test_gamma_past_a_lower_edge_limit_refuses_by_its_id(self):
        """68 H2: a set edge whose limit is below the phase window; above the limit γ refuses by the declared id, never
        the phase constants."""
        rec = fe_prem(False)
        th = rec["phases"][0]["thermal"]
        th["sets"][1]["edge_above"]["limit"] = 400e9
        th["sets"][1]["edge_above"]["refusal"] = "solve.toy_gamma_limit"
        v = mv.RecordView(rec, T_POT)
        self.assertIsInstance(v.state(399e9, 5600.0), tuple)
        s = v.state(401e9, 5600.0)
        self.assertIsInstance(s, st.Stop)
        self.assertEqual(s.record.refusal, "solve.toy_gamma_limit")

    def test_undeclared_gap_inside_the_gamma_window_refuses(self):
        """68 N19: without the declared 0–19 GPa phase-constants span, 10 GPa is a gap no set covers; γ refuses."""
        rec = fe_prem(False)
        self.assertIsInstance(mv.RecordView(rec, T_POT).state(10e9, 2000.0), tuple)
        rec["phases"][0]["thermal"].pop("phase_constants")
        self.assertIsInstance(mv.RecordView(rec, T_POT).state(10e9, 2000.0), st.Stop)

    def test_band_edge_refuses_until_bands_are_evaluated(self):
        rec = fe_prem(False)
        rec["phases"][0]["edges"]["p_max"] = {"band": {"form": "relative", "error": 0.1, "grade": "g", "origin": "o"}}
        s = mv.RecordView(rec, T_POT).state(1.3e13, 6000.0)
        self.assertIsInstance(s, st.Stop)
        self.assertIn("band evaluation not built", s.record.why)


class Branched(unittest.TestCase):
    """D-P1: a branched record picks its phase by the declared boundary curve at T, not by P windows alone."""

    def _rec(self):
        from solver.tests.test_material_registry import GOOD, const
        import copy
        d = copy.deepcopy(GOOD)
        a = d["phases"][0]
        b = copy.deepcopy(a)
        a["id"], b["id"] = "lo", "hi"
        d["phases"].append(b)
        b["eos"]["params"]["rho0"] = const(5000.0, "kg/m3")
        d["kind"], d["choice"] = "branched", "chain"
        d["boundaries"] = [{"between": ["lo", "hi"], "kind": "solid_solid",
                            "curve": {"form": "clapeyron", "p0": const(1.0e10, "Pa"), "t0": const(1000.0, "K"),
                                      "slope": const(3.0e6, "Pa/K"), "t_min": const(300.0, "K"),
                                      "t_max": const(2500.0, "K")}}]
        return d

    def test_side_of_the_curve(self):
        v = mv.RecordView(self._rec(), T_POT)
        # at 1000 K the boundary is at 10 GPa; at 2000 K it is at 13 GPa
        self.assertEqual(v._phase_at(9.9e9, 1000.0).id, "lo")
        self.assertEqual(v._phase_at(10.1e9, 1000.0).id, "hi")
        self.assertEqual(v._phase_at(12.0e9, 2000.0).id, "lo")          # the same P, hotter: still the low-P phase
        self.assertEqual(v._phase_at(13.1e9, 2000.0).id, "hi")
        self.assertEqual(len(v.transitions()), 1)

    def test_clapeyron_outside_its_printed_range_refuses(self):
        """68 N32."""
        self.assertIsInstance(mv.RecordView(self._rec(), T_POT)._phase_at(12.0e9, 3000.0), st.Stop)

    def test_ln_sum_curve_iapws_r14_vii(self):
        """IAPWS R14-08 eq. (5), ice VII melting, with c8's printed constants; P_b at 355/400/500/600/715 K against
        c8's computed values (MPa), and absent outside 355–715 K."""
        from solver.tests.test_material_registry import const
        curve = {"form": "ln_sum", "p_star": const(2216.0e6, "Pa"), "t_star": const(355.0, "K"),
                 "terms": [{"a": const(1.73683, "1"), "b": const(-1.0, "1")},
                           {"a": const(-0.0544606, "1"), "b": const(5.0, "1")},
                           {"a": const(0.806106e-7, "1"), "b": const(22.0, "1")}],
                 "t_min": const(355.0, "K"), "t_max": const(715.0, "K")}
        v = mv.RecordView(self._rec(), T_POT)
        for t, mpa in ((355.0, 2216.0), (400.0, 2816.6), (500.0, 4695.6), (600.0, 8964.0), (715.0, 20617.8)):
            with self.subTest(t=t):
                self.assertAlmostEqual(v.boundary_pressure(curve, t) / 1e6, mpa, delta=0.1)
        self.assertIsNone(v.boundary_pressure(curve, 354.0))
        self.assertIsNone(v.boundary_pressure(curve, 716.0))

    def test_table_curve_outside_its_nodes_refuses(self):
        rec = self._rec()
        rec["boundaries"][0]["curve"] = {"form": "table", "nodes": [[500.0, 9.0e9], [1500.0, 11.0e9]]}
        v = mv.RecordView(rec, T_POT)
        self.assertEqual(v._phase_at(10.5e9, 1000.0).id, "hi")         # P_b(1000 K) = 10 GPa
        self.assertIsInstance(v._phase_at(10.5e9, 2000.0), st.Stop)     # no curve at 2000 K: no guess


if __name__ == "__main__":
    unittest.main()
