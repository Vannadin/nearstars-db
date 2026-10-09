# 전도 덮개 시험 — 마디의 T = A/r + B, 바닥 온도 고정점의 수축, 지구 덮개 수렴, 어긋난 출발값 잡기 (등록 S6)
"""S6 acceptance of rewrite/phase1-a1-impl.frozen.md, each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_lid
"""
import math
import unittest

from solver import lid, rhs, legacy_materials as lm
from solver import stepper as st

M_E, R_E = 5.972e24, 6.371e6


class Thermal:
    """ρ = ρ0 (1 − α (T − 1600)), constant dT/dP on the adiabat: a lid whose density feels its temperature."""
    def __init__(self, rho0=3300.0, alpha=3e-5, dtdp=1e-8):
        self.rho0, self.alpha, self.k = rho0, alpha, dtdp

    def state(self, p, t, guess):
        return (self.rho0 * (1.0 - self.alpha * (t - 1600.0)), self.k)


def _earth_lid(view, **kw):
    rs = rhs.r_scale_of(M_E, 5514.0)
    return lid.lid_pass(view, M_E, R_E, 135e3, 0.0, 293.0, 1600.0, rs, **kw)


class Profile(unittest.TestCase):
    def test_nodes_follow_a_over_r_plus_b(self):
        res = _earth_lid(Thermal())
        self.assertIsInstance(res, lid.LidResult)
        worst = max(abs(y[3] - (res.a / y[0] + res.b)) / (res.a / y[0] + res.b) for _m, y, _k in res.path)
        self.assertLess(worst, 1e-9)
        self.assertAlmostEqual(res.y[0], R_E - 135e3, delta=1e-12 * R_E * 10)
        self.assertEqual(res.y[3], res.t_b)                       # continuous into the adiabat below

    def test_trail_contracts(self):
        res = _earth_lid(Thermal())
        d = [abs(b - a) for a, b in zip(res.trail, res.trail[1:])]
        self.assertTrue(all(y <= x for x, y in zip(d, d[1:])), d)
        self.assertLess(len(res.trail) - 1, 8)

    def test_control_forced_offset_is_caught(self):
        res = _earth_lid(Thermal(alpha=3e-5), t_b_seed=5000.0, lid_iters=1)
        self.assertIsInstance(res, st.Stop)
        self.assertEqual(res.kind, "lid_unconverged")
        self.assertEqual(res.record["trail"][0], 5000.0)


class EarthLid(unittest.TestCase):
    def test_converges_on_earth_mantle_material(self):
        mat = lm.interior._stack(0.325, 0.0, "fe_prem")[1][1]
        view = lm.LegacyView("silicate", mat, 1600.0)
        res = _earth_lid(view)
        self.assertIsInstance(res, lid.LidResult, getattr(res, "record", None))
        self.assertLess(len(res.trail) - 1, 8)
        self.assertGreater(res.t_b, 293.0)
        self.assertLess(res.t_b, 1700.0)


if __name__ == "__main__":
    unittest.main()
