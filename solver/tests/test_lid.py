# 전도 덮개 시험 — 계수가 양 끝 온도를 맞추는지, 밀도를 어느 온도에서 읽는지, 단열선 출발, 고정점 수축, 거절 (등록 S6, r2 HOLD)
"""S6 acceptance of rewrite/phase1-a1-impl.frozen.md, rewritten after r2's S6 HOLD (audit-b9-s4fix-s6): each test
pins one piece of physics, and each names the wrong implementation it catches.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_lid
"""
import unittest

from solver import lid, rhs, legacy_materials as lm
from solver import stepper as st

M_E, R_E = 5.972e24, 6.371e6
T_S, T_POT, D = 293.0, 1600.0, 135e3
RS = rhs.r_scale_of(M_E, 5514.0)


class Toy:
    """ρ = ρ0 (1 − α (T − 1600)) and a constant adiabatic dT/dP = k. Records the T of every density read."""
    def __init__(self, rho0=3300.0, alpha=3e-5, k=1e-8):
        self.rho0, self.alpha, self.k = rho0, alpha, k
        self.reads = []

    def state(self, p, t, guess):
        self.reads.append((p, t))
        return (self.rho0 * (1.0 - self.alpha * (t - 1600.0)), self.k)


def _lid(view, **kw):
    return lid.lid_pass(view, M_E, R_E, D, 0.0, T_S, T_POT, RS, **kw)


class Coefficients(unittest.TestCase):
    """Catches wrong coefficients (r2: a T(r_b) 178 K off T_b passed before)."""

    def test_profile_meets_both_ends(self):
        res = _lid(Toy())
        r_b = R_E - D
        self.assertAlmostEqual(res.a / R_E + res.b, T_S, delta=1e-9 * T_S)
        self.assertLess(abs(res.a / r_b + res.b - res.trail[-2]), 1e-9 * res.t_b)     # the T_b this pass used
        self.assertLess(abs(res.t_profile_base - (res.a / r_b + res.b)), 1e-8 * res.t_b)   # stepped = formula
        self.assertLess(abs(res.t_profile_base - res.t_b), 1e-8 * res.t_b)


class AdiabatStart(unittest.TestCase):
    """T_ad starts at T_pot at the surface and follows the adiabat on the lid's own P (R-LITHO-4): with a constant
    k, T_b = T_pot + k·P_b. Catches «T_ad started at T_s» (r2: Earth T_b 309 K passed before)."""

    def test_t_b_on_the_adiabat(self):
        toy = Toy()
        res = _lid(toy)
        self.assertLess(abs(res.t_b - (T_POT + toy.k * res.y[1])), 1e-8 * res.t_b)


class DensityTemperature(unittest.TestCase):
    """The lid's density is read at the conductive T = a/r + b, not at T_ad. Catches «density at T_ad»."""

    def test_reads_at_conductive_temperatures(self):
        toy = Toy()
        res = _lid(toy)
        lid_reads = [t for p, t in toy.reads if 0.0 < p < res.y[1]]
        self.assertTrue(any(t < T_POT - 500.0 for t in lid_reads))    # cold near the surface, far below T_pot
        self.assertTrue(all(T_S - 1e-6 <= t <= res.t_b + 1.0 or t >= T_POT for t in lid_reads))


class FixedPoint(unittest.TestCase):
    def test_t_sensitive_trail_contracts_over_two_or_more_steps(self):
        res = _lid(Toy(alpha=3e-5))
        d = [abs(b - a) for a, b in zip(res.trail, res.trail[1:])]
        self.assertGreaterEqual(len(d), 2)
        self.assertTrue(all(y < x for x, y in zip(d, d[1:])), d)

    def test_control_far_seed_reaches_the_same_t_b(self):
        """The fixed point corrects an offset seed (it is the map, not the seed, that sets T_b)."""
        ref = _lid(Toy())
        far = _lid(Toy(), t_b_seed=5000.0)
        self.assertEqual(far.trail[0], 5000.0)
        self.assertLess(abs(far.t_b - ref.t_b), 1e-8 * ref.t_b)

    def test_iteration_cap_is_named(self):
        res = _lid(Toy(), t_b_seed=5000.0, lid_iters=1)
        self.assertIsInstance(res, st.Stop)
        self.assertEqual(res.kind, "lid_unconverged")
        self.assertEqual(res.record["layer_id"], "lid")


class EarthLid(unittest.TestCase):
    def test_converges_on_earth_mantle_material(self):
        """Converges, but proves little about the fixed point: the engine silicate's solid density barely moves
        with T at these pressures (r2), so one iteration suffices; the toy tests above carry the physics."""
        mat = lm.interior._stack(0.325, 0.0, "fe_prem")[1][1]
        res = _lid(lm.LegacyView("silicate", mat, T_POT))
        self.assertIsInstance(res, lid.LidResult, getattr(res, "record", None))
        self.assertGreater(res.t_b, T_POT)


class InputRefusals(unittest.TestCase):
    """R-LITHO-6: a named stop, not an unnamed h_min or a TypeError."""

    def test_zero_depth(self):
        res = lid.lid_pass(Toy(), M_E, R_E, 0.0, 0.0, T_S, T_POT, RS)
        self.assertEqual((res.kind, res.record["field"]), ("lid_input", "depth"))

    def test_missing_surface_temperature(self):
        res = lid.lid_pass(Toy(), M_E, R_E, D, 0.0, None, T_POT, RS)
        self.assertEqual((res.kind, res.record["field"]), ("lid_input", "surface_temperature_k"))


if __name__ == "__main__":
    unittest.main()
