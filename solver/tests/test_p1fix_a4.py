# 리뷰 수정 A4 시험 — 봉합선 착지 뒤 첫 걸음은 새 쪽에서(적응 모드), 곡선 이음매는 스침이 아님
"""Post-phase-1 review fix batch A4 (rewrite/p1review/fix-plan.md): G1-C-01 on the review's toy (probe p4: Earth M,
R; ρ 3717 → 4407 kg/m³ at 23.83 GPa), G1-R-01 on a planted solidus walk across the 20 GPa Monteux join. Each test
fails on af27819c.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p1fix_a4
"""
import math
import unittest

from solver import events, rhs
from solver import stepper as st

M, R, PB = 5.972e24, 6.371e6, 23.83e9


class _Two:
    """ρ jumps at PB; at exactly PB the lower-pressure phase is read (eos.Material.phase_at: p ≤ p_max)."""
    def __init__(self, lo=3717.0, hi=4407.0):
        self.lo, self.hi = lo, hi

    def state(self, p, t, guess):
        return (self.lo if p <= PB else self.hi, 0.0)


class _One:
    def __init__(self, rho):
        self.rho = rho

    def state(self, p, t, guess):
        return (self.rho, 0.0)


def _opt(rtol, h0):
    rs = rhs.r_scale_of(M, 3.0 * M / (4.0 * math.pi * R ** 3))
    return st.Options(rtol=rtol, floors=rhs.floors(M, rs), h0=h0 * M, h_min=1e-15 * M, h_max=M / 20.0,
                      max_steps=200000)


Y0 = (R, 0.0, 1600.0, 1600.0, 0.0, 0.0)


def _seam(terminal=False):
    return st.Event("seam", lambda m, y: y[1] - PB, scale=PB, terminal=terminal, seam=not terminal, component=1)


def _reference():
    """Two segments at rtol 1e-13: the old phase to the seam, then the new phase from the landed state."""
    a = st.run(rhs.make_rhs(_One(3717.0)), M, Y0, 0.5 * M, _opt(1e-13, 1e-4), [_seam(terminal=True)])
    b = st.run(rhs.make_rhs(_One(4407.0)), a.x, a.y, 0.5 * M, _opt(1e-13, 1e-4), [])
    return b.y[0]


class NewSideAfterASeamLanding(unittest.TestCase):
    """G1-C-01: r at m = M/2 against the two-segment reference, at rtol 1e-10, three step placements. The review
    measured −0.029 … −0.070 m as is and ≤ 1e-4 m with k1 read past the seam. Here (Mac): −0.0663 m on af27819c,
    +6.8e-5 … +7.9e-5 m with the fix, against the clean single-phase run's 1.9e-4 … 2.4e-4 m at the same rtol."""

    def test_error_is_back_to_the_clean_level(self):
        ref = _reference()
        for h0 in (1e-3, 7.3e-4, 1.37e-3):
            with self.subTest(h0=h0):
                res = st.run(rhs.make_rhs(_Two()), M, Y0, 0.5 * M, _opt(1e-10, h0), [_seam()])
                self.assertEqual([e[0] for e in res.events], ["seam"])
                self.assertLess(abs(res.y[0] - ref), 5e-4, res.y[0] - ref)


class _Solidus:
    """A one-curve material whose onset T has a −1 K step at the 20 GPa join, as eos.silicate_solidus (p < join: old
    branch), and the solidus-curve name so `curve_seams` lists the joins."""
    name = "planted"
    onset_curve_names = ("고상선",)

    def __init__(self, join):
        self.join = join

    def onset_curves(self, p, t):
        base = 2400.0 + 15.0e-9 * (p - self.join)
        return [("고상선", base if p < self.join else base - 1.0)]


class GrazeAcrossAJoin(unittest.TestCase):
    """G1-R-01: T − T_sol falls by 0.3 K per node toward the join from +0.8 K, then the landed node reads the new
    branch (+1 K): Δg changes sign at the last old-branch node, |g| ≤ GRAZE_K. Not a graze."""

    def _walk(self, mon, join):
        g_old = [3.2, 2.0, 0.8, 0.5]            # old-branch g at the nodes before the join
        ps = [join - 4e8, join - 3e8, join - 2e8, join - 1e8]
        for p, g in zip(ps, g_old):
            t = 2400.0 + 15.0e-9 * (p - join) + g
            mon(0.0, (0.0, p, t, t))
        t = 2400.0 + 15.0e-9 * 0.0 + 0.2         # at P = join: old-branch g would be 0.2, the new branch reads 1.2
        mon(0.0, (0.0, join, t, t))
        return mon

    def test_no_graze_across_the_join(self):
        from solver.legacy_materials import eos
        join = float(eos.MONTEUX_JOIN_PA)
        self.assertIsNone(self._walk(events.GrazeMonitor(_Solidus(join)), join).best)

    def test_control_the_same_walk_without_a_join_grazes(self):
        """The same g sequence with the step removed (the join moved far away): the turn is a graze."""
        from solver.legacy_materials import eos
        join = float(eos.MONTEUX_JOIN_PA)
        mat = _Solidus(join)
        mon = events.GrazeMonitor(mat)
        mon.joins = []                                     # as before the fix: no join known
        self.assertIsNotNone(self._walk(mon, join).best)


if __name__ == "__main__":
    unittest.main()
