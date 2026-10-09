# 고정 걸음 모드 시험 — RK4 4차, 걸음 안 온도 고정의 1차, 반지름 균일 격자의 질량 꼴 되돌림, 풀이 연결 (T2 적분법 항 등록)
"""Acceptance of the fixed-step mode (rewrite/oracle/t2-method-term-registration.md, «Code» items), each with a control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_fixed_grid
"""
import math
import unittest

from solver import body as b, context, fixed_grid, result, rhs, solve as sv
from solver import stepper as st
from solver.tests.test_solve import Uniform, _two_layer, q


def _rk4_end(n):
    """y' = y on [0, 1] with n fixed RK4 steps through stepper.run."""
    opt = st.Options(rtol=1.0, floors=(math.inf,), h0=1.0 / n, h_min=0.0, h_max=1.0 / n, max_steps=10 * n, fixed=True)
    return st.run(lambda x, y: (y[0],), 0.0, (1.0,), 1.0, opt).y[0]


class Rk4Order(unittest.TestCase):
    def test_fourth_order(self):
        e1, e2 = abs(_rk4_end(20) - math.e), abs(_rk4_end(40) - math.e)
        self.assertTrue(14.0 < e1 / e2 < 18.0, e1 / e2)

    def test_control_adaptive_mode_untouched(self):
        opt = st.Options(rtol=1e-10, floors=(1e-12,), h0=0.1, h_min=1e-12, h_max=1.0, max_steps=10000)
        res = st.run(lambda x, y: (y[0],), 0.0, (1.0,), 1.0, opt)
        self.assertLess(abs(res.y[0] - math.e), 1e-8)
        self.assertGreater(res.counters.accepted, 1)


class FrozenTemperature(unittest.TestCase):
    """dT/dP = c·T in a uniform sphere: the exact T(P) = T₀ exp(c (P − P₀)). The old path's step-start T is Euler in
    P, so the error halves with dr (first order). Control: with T not frozen, RK4 makes it fourth order."""

    class View(Uniform):
        C = 2.0e-11                                   # 1/Pa: T rises by e^(c ΔP) ≈ 1.2 over the fixture's ~10 GPa

        def state(self, p, t, guess):
            return (self.rho, self.C * t, ())

    def _err(self, n, frozen=True):
        M, R = 5.0e23, 2.5e6
        rho = 3.0 * M / (4.0 * math.pi * R ** 3)
        view = self.View(rho)
        f = rhs.make_rhs(view)
        if frozen:
            res = fixed_grid.run_r(f, M, (R, 1e5, 1000.0, 1000.0, 0.0, 0.0), 1e-6 * M, 0.5 * R, "half", R / n,
                                   m_scale=M)
        else:
            def fr(r, z):
                k = f(z[0], (r, *z[1:]))
                return (1.0 / k[0], *(c / k[0] for c in k[1:]))
            opt = st.Options(rtol=1.0, floors=(math.inf,) * 6, h0=R / n, h_min=0.0, h_max=R / n, max_steps=10 ** 6,
                             fixed=True)
            out = st.run(fr, R, (M, 1e5, 1000.0, 1000.0, 0.0, 0.0), 0.5 * R, opt)
            res = st.Result(out.y[0], (out.x, *out.y[1:]), out.stop)
        p = res.y[1]
        self.assertEqual(res.event if frozen else "half", "half")
        return abs(res.y[2] - 1000.0 * math.exp(view.C * (p - 1e5))), res

    def test_first_order_when_frozen(self):
        e1, _ = self._err(400)
        e2, _ = self._err(800)
        self.assertTrue(1.8 < e1 / e2 < 2.2, e1 / e2)

    def test_control_unfrozen_is_fourth_order(self):
        e1, _ = self._err(100, frozen=False)
        e2, _ = self._err(200, frozen=False)
        self.assertTrue(12.0 < e1 / e2 < 20.0, e1 / e2)

    def test_mass_and_pressure_exact_for_uniform_density(self):
        """m(r) = (4/3)πρr³, P(r) = P₀ + (2π/3)Gρ²(R² − r²) — m is cubic, so RK4 is exact for it to rounding."""
        _e, res = self._err(1500)
        M, R = 5.0e23, 2.5e6
        rho = 3.0 * M / (4.0 * math.pi * R ** 3)
        r = res.y[0]
        self.assertAlmostEqual(r, 0.5 * R, delta=1e-9 * R)
        self.assertLess(abs(res.x - 4.0 / 3.0 * math.pi * rho * r ** 3) / M, 1e-12)
        p_exact = 1e5 + 2.0 * math.pi / 3.0 * rhs.G * rho ** 2 * (R ** 2 - r ** 2)
        self.assertLess(abs(res.y[1] - p_exact) / p_exact, 1e-11)
        self.assertEqual(res.path[-1][0], res.x)               # the path comes back in the mass form
        self.assertAlmostEqual(res.path[-1][2][0], 1.0 / (4.0 * math.pi * r * r * rho), delta=1e-9 / (r * r * rho))


class SeamLanding(unittest.TestCase):
    """A density jump at a pressure seam (ρ 3700 → 4400 kg/m³ at P_b, the old branch read at P = P_b exactly, as the
    legacy materials do). The fixed mode lands the seam with the stages on the old side and starts the next step from
    a k1 read on the new side; it then matches the adaptive mode's r(m) to the grid's own error. Control: with the k1
    left on the seam (old branch), the step after the landing loses ~Δρ/ρ · dr / 6 of radius."""

    class Jump(Uniform):
        P_B = 2.0e10

        def state(self, p, t, guess):
            return (3700.0 if p <= self.P_B else 4400.0, 0.0, ())

    def _ends(self):
        M, R = 4.0e24, 6.0e6
        view = self.Jump(0.0)
        f = rhs.make_rhs(view)
        seam = st.Event("seam", lambda m, y: y[1] - self.Jump.P_B, scale=self.Jump.P_B, terminal=False, seam=True,
                        component=1)
        y0 = (R, 1e5, 0.0, 0.0, 0.0, 0.0)
        m_end = 0.5 * M
        fx = fixed_grid.run_r(f, M, y0, m_end, 1e3, "floor", R / 1500.0, [seam], m_scale=M)
        opt = st.Options(rtol=1e-10, floors=rhs.floors(M, R), h0=1e-3 * M, h_min=1e-15 * M, h_max=M / 20.0,
                         max_steps=200000)
        ad = st.run(f, M, y0, m_end, opt, [seam])
        self.assertEqual((fx.stop.kind, ad.stop.kind), ("end", "end"))
        self.assertEqual([e[0] for e in fx.events], ["seam"])
        return fx.y[0], ad.y[0], R / 1500.0

    def test_matches_adaptive_after_the_seam(self):
        rf, ra, dr = self._ends()
        self.assertLess(abs(rf - ra), 1e-3 * dr)

    def test_control_k1_on_the_seam_loses_radius(self):
        orig = st._new_side_k1
        st._new_side_k1 = lambda f, ev, x, y, k1, g0: k1
        try:
            rf, ra, dr = self._ends()
        finally:
            st._new_side_k1 = orig
        self.assertGreater(abs(rf - ra), 0.01 * dr)


class SolveWiring(unittest.TestCase):
    """context.Options.fixed_dr reaches every segment: a uniform two-layer body answers with the same radius in both
    modes (uniform density has no truncation error worth the name), and a radius-ended core is entered."""

    def test_two_layer_same_radius(self):
        body, views = _two_layer(9000.0)
        a, _ = sv.solve(body, context.Options(sensitivity_dt=0.0), views=views)
        r = q(a, "radius")
        f, _ = sv.solve(body, context.Options(sensitivity_dt=0.0, fixed_dr=r / 1500.0), views=views)
        self.assertIsInstance(f, result.Answer, getattr(f, "text", None))
        self.assertLess(abs(q(f, "radius") - r) / r, 1e-9)

    def test_radius_ended_core_entered(self):
        M = 5.0e24
        layers = (b.Layer("core", "core", "x", b.Extent("radius_from_centre", 3.0e6)), b.Layer("mantle", "mantle", "y"))
        body = b.Body("fixture", "planet", b.SurfaceState(M, t_pot=0.0), layers, b.Closure("R", 1e5, 1e8))
        views = {"core": Uniform(9000.0), "mantle": Uniform(3000.0)}
        a, _ = sv.solve(body, context.Options(sensitivity_dt=0.0), views=views)
        f, _ = sv.solve(body, context.Options(sensitivity_dt=0.0, fixed_dr=q(a, "radius") / 1500.0), views=views)
        self.assertIsInstance(f, result.Answer, getattr(f, "text", None))
        self.assertLess(abs(q(f, "radius") - q(a, "radius")) / q(a, "radius"), 1e-9)

    def test_control_solve_id_differs(self):
        body, _views = _two_layer(9000.0)
        c = sv._canonical(body)
        self.assertNotEqual(context.solve_id_of(c, b"", context.Options()),
                            context.solve_id_of(c, b"", context.Options(fixed_dr=1.0)))


if __name__ == "__main__":
    unittest.main()
