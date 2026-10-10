# 검산식 문법 시험 — 산술 · 경로 이름 · 모호한 이름 멈춤 · 문법 밖 멈춤 · 집합 퍼짐 함수 · fe_prem 검산 (phase-2 impl note 3 C4)
"""Note 3 C4: the formula-check grammar, with its controls.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_material_checks
"""
import unittest

from solver import material_checks as mc
from solver import material_registry as mr
from solver import material_view as mv
from solver.from_v1 import thaw


def phase():
    return thaw(mr.load()["fe_prem"])["phases"][0]


class Grammar(unittest.TestCase):
    def test_arithmetic_and_paths(self):
        ph = phase()
        got = mc.evaluate("pressure.alpha_k * (T - T0) + 0.5 * pressure.alpha_k_dt * (T - T0)**2", ph,
                          {"T": 6000.0, "T0": 300.0})
        self.assertAlmostEqual(got / 1e9, 81.6411, places=4)                 # I&A: 68.97 + 12.67
        self.assertAlmostEqual(mc.evaluate("sets[0].alpha_k / (rho * sets[0].c_v)", ph, {"rho": 8083.0}),
                               2.7309, places=4)                             # Huang Table 1 recomputed

    def test_controls(self):
        ph = phase()
        cases = (("alpha_k * 2", "material.check_ambiguous"),          # pressure.alpha_k and sets[0].alpha_k
                 ("nothing * 2", "material.check_unknown_name"),
                 ("__import__('os')", "material.check_grammar"),
                 ("pressure.alpha_k if T else 0", "material.check_grammar"),
                 ("gamma_spread(sets[1] @ P=35e9 ; printed=2.66)", "material.check_grammar"),
                 ("__spread__(T, 0, 1, 2, 3)", "material.check_grammar"),          # 68 G1
                 ("abs(1, 2)", "material.check_grammar"),                          # 68 G2
                 ("max()", "material.check_grammar"),
                 ("(-8)**(1/3)", "material.check_grammar"),                        # 68 G3: complex
                 ("10.0**400", "material.check_grammar"))
        for expr, id_ in cases:
            with self.subTest(expr=expr):
                got = mc.evaluate(expr, ph, {"T": 1.0})
                self.assertIsInstance(got, mc.CheckStop, got)
                self.assertEqual(got.id, id_)

    def test_spread_reads_the_set_through_the_view(self):
        rec = thaw(mr.load()["fe_prem"])
        v = mv.RecordView(rec, 1600.0)
        g = mc.evaluate("gamma_spread(sets[1] @ P=35.0e9, T=2400.0 ; printed=2.66)", rec["phases"][0], {},
                        mc.view_spread(v))
        direct = abs(v.phases[0].sets[1].evaluator.at(35.0e9, 2400.0)["gruneisen"] / 2.66 - 1.0)
        self.assertEqual(g, direct)
        self.assertIsInstance(mc.evaluate("gamma_spread(sets[1] @ P=35.0e9, T=2400.0 ; printed=2.66)",
                                          rec["phases"][0], {}), mc.CheckStop)      # no view, no spread


if __name__ == "__main__":
    unittest.main()
