# 중심 급수 시험 — 핵 온도가 m_ε 끝값이 아닌 참 중심값(T_ε + dT/dP·ΔP)인지, r 바닥 끝은 그대로인지 (stage-A prereg-centre-series, note 1)
"""Stage-A registration prereg-centre-series (frozen a9a2c54a; note 1 77f36a7f): the record's core_pressure already
carries P's centre series; core_temperature now carries T_c = T_ε + (dT/dP)_ε·ΔP at an m_ε end, with ΔP the same term.
On a uniform body with a constant dT/dP = γ, T(P) = T_pot + γ·P is exact along the walk, so the true centre is
T_pot + γ·P_c with P_c the reported core_pressure. Run: solver/.venv/bin/python -m unittest solver.tests.test_centre_series"""
import dataclasses
import math
import unittest

from solver import body as b, context, rhs, result, solve as sv
from solver.tests.test_physics import PolytropeN1

M = 5.0e24
GAMMA = 2.0e-8                      # K/Pa


class Uniform:
    def __init__(self, rho, dtdp):
        self.rho, self.dtdp = rho, dtdp
        self.mat = None
        self.p_floor = 0.0

    def state(self, p, t, guess):
        return (self.rho, self.dtdp, ())


def _body(core_rho, t_pot=1600.0, eps=None):
    layers = (b.Layer("core", "core", "x", b.Extent("mass_fraction", 0.5)), b.Layer("mantle", "mantle", "y"))
    body = b.Body("fixture", "planet", b.SurfaceState(M, t_pot=t_pot), layers, b.Closure("R", 1e5, 1e8))
    return body, {"core": Uniform(core_rho, GAMMA), "mantle": Uniform(5000.0, GAMMA)}


def q(ans, key):
    return next(x.point for x in ans.quantities if x.key == key)


class TemperatureSeries(unittest.TestCase):
    def test_the_reported_centre_temperature_is_the_true_centre(self):
        """T_c = T_pot + γ·P_c to the walk's accuracy. Mutant (T_c = T_ε): short by γ·ΔP, ~1e-4 of γ·P_c."""
        body, views = _body(6000.0)
        ans, _ = sv.solve(body, views=views)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        p_c, t_c = q(ans, "core_pressure"), q(ans, "core_temperature")
        want = 1600.0 + GAMMA * p_c
        self.assertLess(abs(t_c - want) / (GAMMA * p_c), 1e-7, (t_c, want))

    def test_an_r_floor_end_keeps_the_end_temperature(self):
        """A pass ended at the r floor (ρ_c/ρ̄ > 10³) keeps T_ε: T_c sits below T_pot + γ·P_c by γ·ΔP (P's shipped
        series still applies there), and the floor note is on the answer."""
        body, views = _body(1.0e7)
        ans, _ = sv.solve(body, views=views)
        self.assertIsInstance(ans, result.Answer, getattr(ans, "text", None))
        self.assertIn("centre_closed_at_floor", [n.kind for n in ans.notes])
        p_c, t_c = q(ans, "core_pressure"), q(ans, "core_temperature")
        self.assertLess(t_c, 1600.0 + GAMMA * p_c)


class PressureSeries(unittest.TestCase):
    """Condition 1 (analytic controls) for the shipped P series the T series reuses."""

    def test_uniform_body_reports_the_analytic_centre(self):
        """A uniform body (one density in both layers): |P_c/P0 − 1| ≤ 1e-7 at m_ε 1e-6 and 1e-8, P0 = (2π/3)Gρ²R²."""
        body, _v = _body(6000.0)
        views = {"core": Uniform(6000.0, 0.0), "mantle": Uniform(6000.0, 0.0)}
        for eps in (1e-6, 1e-8):
            ans, _ = sv.solve(body, dataclasses.replace(context.Options(), eps=eps), views=views)
            R = q(ans, "radius")
            p0 = 2.0 * math.pi / 3.0 * rhs.G * 6000.0 ** 2 * R ** 2
            self.assertLess(abs(q(ans, "core_pressure") / p0 - 1.0), 1e-7, eps)

    def test_n1_polytrope_series_to_its_next_order(self):
        """n = 1 (P = Kρ², analytic P_c), rtol 1e-12: the end plus centre_dp is within 2e-8 of P_c at m_ε 1e-6 and
        1e-8. Mutant (no series): −1.5e-4 and −6.9e-6."""
        K, Mp = 4.0e5, 5.0e24
        k = math.sqrt(2 * math.pi * rhs.G / K)
        R = math.pi / k
        rho_c = Mp * k ** 3 / (4 * math.pi ** 2)
        pc = K * rho_c ** 2
        for eps in (1e-6, 1e-8):
            p = rhs.inward_pass(PolytropeN1(K), Mp, R, 1e-8 * pc, 0.0, 3 * Mp / (4 * math.pi * R ** 3),
                                rhs.PassOptions(eps=eps, rtol=1e-12))
            got = p.y[1] + sv.centre_dp(p.rho_end, p.y[0])
            self.assertLess(abs(got / pc - 1.0), 2e-8, eps)
            self.assertGreater(abs(p.y[1] / pc - 1.0), 1e-6)          # control: the end alone is short


if __name__ == "__main__":
    unittest.main()
