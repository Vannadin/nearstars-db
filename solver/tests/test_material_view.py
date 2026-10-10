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
    W-L1-01 αK_T, P5-F1 Dorogokupets V0). The evaluator's molar mass is added where the record does not carry it."""
    rec = thaw(mr.load()["fe_prem"])
    ev = rec["phases"][0]["thermal"]["sets"][1]["evaluator"]
    ev["params"].setdefault("molar_mass", {"value": 0.055845, "unit": "kg/mol"})
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


if __name__ == "__main__":
    unittest.main()
