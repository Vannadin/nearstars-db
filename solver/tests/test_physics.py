# 해석해 시험 — 균일 밀도 구와 n = 1 폴리트로프를 안쪽 적분 + 중심 잔차 근으로 재현 (등록 S2)
"""S2 acceptance of rewrite/phase1-a1-impl.frozen.md, each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_physics
"""
import math
import unittest

from solver import closure, rhs
from solver import stepper as st


class Uniform:
    """ρ = ρ0 everywhere, no thermal constants (dT/dP = 0)."""
    def __init__(self, rho0):
        self.rho0 = rho0

    def state(self, p, t, guess):
        return (self.rho0, 0.0)


class PolytropeN1:
    """P = K ρ² (n = 1). ρ(P_s = 0) = 0, so it carries its near-surface series to second order in z/R:
    with depth z and g(z) ≈ g_s (1 + 2z/R) (the shell's own mass is higher order), dP/dz = ρ g and P = Kρ² give
    ρ = (g_s / 2K)(z + z²/R). At the start pressure P′, ρ′ = √(P′/K) fixes z, and the shell mass is
    ∫ 4π r² ρ dz ≈ 4π R² (g_s / 2K)(z²/2 − z³/(3R)). A first-order shell (ρ = g z/2K) leaves a relative R error of
    order P′/P_c, about 1e-8 at P′ = 1e-8 P_c (measured 1.02e-8), which this second-order shell removes."""
    def __init__(self, k):
        self.k = k

    def state(self, p, t, guess):
        if p < 0.0:
            return st.Stop("domain", {"p": p})
        return (math.sqrt(p / self.k), 0.0)

    def surface_shell(self, p_start, g, radius):
        d0 = 2.0 * self.k * math.sqrt(p_start / self.k) / g        # z + z²/R = d0
        z = 0.5 * radius * (math.sqrt(1.0 + 4.0 * d0 / radius) - 1.0)
        dm = 4.0 * math.pi * radius ** 2 * g / (2.0 * self.k) * (0.5 * z * z - z ** 3 / (3.0 * radius))
        return dm, z


M = 5.0e24


class UniformSphere(unittest.TestCase):
    rho0 = 5000.0

    def _solve(self, view):
        r_true = (3 * M / (4 * math.pi * self.rho0)) ** (1 / 3)
        F = lambda R: rhs.inward_pass(view, M, R, 0.0, 0.0, self.rho0).F
        out = closure.solve_scalar(F, 0.5 * r_true, 2.0 * r_true)
        return r_true, out

    def test_radius_and_pressure(self):
        r_true, out = self._solve(Uniform(self.rho0))
        self.assertEqual(out.kind, "root")
        R = out.roots[0]
        self.assertLess(abs(R - r_true) / r_true, 1e-10)
        p = rhs.inward_pass(Uniform(self.rho0), M, R, 0.0, 0.0, self.rho0)
        r_end, p_end = p.y[0], p.y[1]
        p_exact = 2 * math.pi / 3 * rhs.G * self.rho0 ** 2 * (R * R - r_end * r_end)
        self.assertLess(abs(p_end - p_exact) / p_exact, 1e-9)       # rtol 1e-10 accumulated over the pass
        p_c = 3 * rhs.G * M ** 2 / (8 * math.pi * R ** 4)
        # P_c = 3GM²/(8πR⁴) at the solved R vs the exact sphere's (2π/3)Gρ²R_true². This only restates the R check
        # (R to 1e-10 gives P_c to 4e-10, r2 N7); the pressure check proper is p_end against the exact profile above.
        self.assertLess(abs(p_c - 2 * math.pi / 3 * rhs.G * self.rho0 ** 2 * r_true ** 2) / p_c, 5e-10)

    def test_control_perturbed_density_fails(self):
        r_true, out = self._solve(Uniform(self.rho0 * (1 + 1e-6)))
        self.assertGreater(abs(out.roots[0] - r_true) / r_true, 1e-10)


class Polytrope(unittest.TestCase):
    R_true = 7.0e6

    def _solve(self, rtol):
        K = 2 * rhs.G * self.R_true ** 2 / math.pi          # k = √(2πG/K) = π/R
        view = PolytropeN1(K)
        rho_c = math.pi * M / (4 * self.R_true ** 3)
        p_start = 1e-8 * K * rho_c ** 2
        rho_mean = 3 * M / (4 * math.pi * self.R_true ** 3)
        opt = rhs.PassOptions(rtol=rtol)
        F = lambda R: rhs.inward_pass(view, M, R, p_start, 0.0, rho_mean, opt).F
        return closure.solve_scalar(F, 0.7 * self.R_true, 1.4 * self.R_true)

    def test_radius(self):
        out = self._solve(1e-10)
        self.assertEqual(out.kind, "root")
        self.assertLess(abs(out.roots[0] - self.R_true) / self.R_true, 1e-8)

    def test_control_loose_rtol_fails(self):
        out = self._solve(1e-3)
        self.assertGreater(abs(out.roots[0] - self.R_true) / self.R_true, 1e-8)


class BrentAgainstScipy(unittest.TestCase):
    def test_same_root(self):
        from scipy.optimize import brentq
        rho0 = 5000.0
        r_true = (3 * M / (4 * math.pi * rho0)) ** (1 / 3)
        F = lambda R: rhs.inward_pass(Uniform(rho0), M, R, 0.0, 0.0, rho0).F
        ours = closure.solve_scalar(F, 0.5 * r_true, 2.0 * r_true).roots[0]
        ref = brentq(F, 0.5 * r_true, 2.0 * r_true, xtol=1e-13 * r_true)
        self.assertLess(abs(ours - ref) / ref, 2 * closure.CLOSE_TOL)   # ours to CLOSE_TOL, scipy's 10× tighter


if __name__ == "__main__":
    unittest.main()
