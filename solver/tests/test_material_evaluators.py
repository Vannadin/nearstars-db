# 평가기 시험 — French & Redmer 2015 평가기가 옛 ice_fr2015 와 비트까지 같음, 괄호 밖은 붙잡지 않고 거절 (phase-2 P3b)
"""P3b (3): the french_redmer2015 evaluator from record params.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_material_evaluators
"""
import unittest

from solver import legacy_materials  # noqa: F401  (engine/ on the path)
from solver import material_view as mv

import ice_fr2015 as L  # noqa: E402


def legacy_params():
    """The legacy module's constants as record params (a fixture: c8's record carries them as read)."""
    p = {f"a{i}": v for i, v in enumerate(L.UE_HSE)}
    p.update({f"b{i}": v for i, v in enumerate(L.UN_B)})
    p.update(t_d=L.T_D, t_e=L.T_E, a_d=L.A_D, a_e=L.A_E, k0=L.K0, rho_search_min=1600.0, rho_search_max=5750.0)
    p.update({f"alpha_0_m{-k}": v for (_i, k), v in L.ALPHA.items()})
    p.update({f"gamma_{j}_m{-k}": v for (j, k), v in L.GAMMA.items()})
    return {k: {"value": v} for k, v in p.items()}


class FrenchRedmer(unittest.TestCase):
    def setUp(self):
        self.ev = mv.FrenchRedmer2015(legacy_params())

    def test_bit_identical_to_legacy_inside_the_bracket(self):
        n = 0
        for p in (20e9, 60e9, 150e9, 300e9):
            for t in (300.0, 800.0, 1500.0):
                with self.subTest(p=p, t=t):
                    a, b = self.ev.at(p, t), L.thermal_at(p, t)
                    for k in ("dpdt_v", "c_v", "gruneisen", "k_t", "density"):
                        self.assertEqual(a[k], b[k], k)
                    n += 1
        self.assertEqual(n, 12)

    def test_outside_the_bracket_refuses_where_legacy_clamps(self):
        """Legacy returns ρ = 1.6 g/cm³ (the bracket wall) at 5 GPa / 800 K (C82); the evaluator refuses."""
        self.assertEqual(L.density_at(5.0, 800.0), 1.6)
        with self.assertRaises(ValueError):
            self.ev.at(5e9, 800.0)

    def test_evaluator_form_phase_gives_rho_and_dtdp(self):
        """c8: form evaluator — the view's ρ and (dT/dP)_S come from the potential; outside the bracket it refuses."""
        import copy
        from solver import stepper as st
        from solver.tests.test_material_registry import GOOD
        d = copy.deepcopy(GOOD)
        ph = d["phases"][0]
        ph["eos"] = {"form": "evaluator", "reference": ph["eos"]["reference"],
                     "evaluator": {"name": "french_redmer2015", "source": {"formula": "toy"}, "params": legacy_params()}}
        for k in ("sets", "gamma_window", "phase_constants"):
            ph["thermal"].pop(k, None)
        ph["window"] = {"p_min": 1.0e9, "p_max": 1.0e11, "t_min": 250.0, "t_max": 2000.0}
        v = mv.RecordView(d, 300.0)
        rho, dtdp, _n = v.state(60e9, 800.0)
        x = L.thermal_at(60e9, 800.0)
        self.assertEqual(rho, x["density"])
        ks = x["k_t"] + x["dpdt_v"] * x["gruneisen"] * 800.0
        self.assertEqual(dtdp, x["gruneisen"] * 800.0 / ks)
        self.assertIsInstance(v.state(5e9, 800.0), st.Stop)               # outside the ρ bracket: a named Stop

    def test_set_evaluator_failure_is_a_named_stop(self):
        """68 N35: an evaluator failing inside a thermal set (outside its ρ bracket) gives a Stop, not an exception."""
        import copy
        from solver import stepper as st
        from solver.tests.test_material_registry import GOOD
        d = copy.deepcopy(GOOD)
        d["phases"][0]["thermal"]["sets"][0]["evaluator"] = {"name": "french_redmer2015", "source": {"formula": "toy"},
                                                             "params": legacy_params()}
        s = mv.RecordView(d, 300.0).state(5e9, 800.0)
        self.assertIsInstance(s, st.Stop)
        self.assertIn("FrenchRedmer2015", s.record.why)

    def test_missing_param_refuses(self):
        p = legacy_params()
        p.pop("gamma_3_m2")
        with self.assertRaises(ValueError):
            mv.FrenchRedmer2015(p)


IAPWS06 = dict(g00=-632020.233449497, g01=0.655022213658955, g02=-1.89369929326131e-08, g03=3.39746123271053e-15,
               g04=-5.56464869058991e-22, s0=189.13, t1_re=3.68017112855051e-02, t1_im=5.10878114959572e-02,
               r1_re=44.7050716285388, r1_im=65.6876847463481, t2_re=0.337315741065416, t2_im=0.335449415919309,
               r20_re=-72.597457432922, r20_im=-78.100842711287, r21_re=-5.57107698030123e-05,
               r21_im=4.64578634580806e-05, r22_re=2.34801409215913e-11, r22_im=-2.85651142904972e-11,
               t_t=273.16, p_t=611.657, p0=101325.0)


class Iapws06(unittest.TestCase):
    """IAPWS R10-06 ice Ih with c8's Table 2 readings; Table 11's verification values (ρ), and c_P at the triple
    point (Table 11: 2096.78 J/kg/K)."""

    def setUp(self):
        self.ev = mv.Iapws06Ih({k: {"value": v} for k, v in IAPWS06.items()})

    def test_table_11(self):
        for t, p, rho in ((273.16, 611.657, 916.709), (100.0, 100e6, 941.68), (0.0, 0.0, 933.79),
                          (250.0, 200e6, 939.94), (50.0, 150e6, 946.33)):
            with self.subTest(t=t, p=p):
                self.assertAlmostEqual(self.ev.at(p, t)["density"], rho, delta=0.006)
        self.assertAlmostEqual(self.ev.at(611.657, 273.16)["c_p"], 2096.78, delta=0.006)

    def test_missing_param_refuses(self):
        with self.assertRaises(ValueError):
            mv.Iapws06Ih({k: {"value": v} for k, v in IAPWS06.items() if k != "r22_im"})


if __name__ == "__main__":
    unittest.main()
