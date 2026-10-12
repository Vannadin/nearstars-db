# 리뷰 수정 A4 시험 — 봉합선 착지 뒤 첫 걸음은 새 쪽에서(적응 모드), 곡선 이음매는 스침이 아님
"""Post-phase-1 review fix batch A4 (rewrite/p1review/fix-plan.md): G1-C-01 on the review's toy (probe p4: Earth M,
R; ρ 3717 → 4407 kg/m³ at 23.83 GPa), G1-R-01 on a planted solidus walk across the 20 GPa Monteux join (part 1, fail on
af27819c); G3-C-02, phase-1 design notes 13 §1 / 13a / 13b, the band test on a planted table (part 2, fail on
75af30d3).

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


# ---- part 2: notes 13 §1 / 13a / 13b, the band test --------------------------------------------------------------

import dataclasses                                   # noqa: E402
import importlib                                     # noqa: E402
from types import SimpleNamespace as NS              # noqa: E402
from unittest import mock                            # noqa: E402

from solver import legacy_materials as _lm           # noqa: E402,F401  (puts engine/ on sys.path)

mc = importlib.import_module("mantle_composition")
smooth = importlib.import_module("smooth_table")
KEY = "a4_planted_table"
W = mc.BLEND_K
OFF = 0.5 * mc.T_STEP


class _Table:
    """A planted upper edge E(ln P) on a uniform 0.05 ln P grid from 1 GPa: flat at E0, with an optional bump."""
    def __init__(self, e0=2000.0, bump=None):
        self.lnp = [math.log(1.0e9) + 0.05 * i for i in range(40)]
        self.edge = [e0 + (bump(i) if bump else 0.0) for i in range(40)]
        self.edge_ys = list(self.edge)

    def edge_at(self, p):
        x = math.log(p)
        i = min(max(int((x - self.lnp[0]) / 0.05), 0), len(self.lnp) - 2)
        return smooth.cubic1(x, self.lnp, self.edge_ys, i)


def _check(table):
    ph = NS(table_key=KEY)
    mat = NS(name="planted", phases=(ph,), phase_at=lambda p: ph)
    patch = mock.patch.dict(mc._TABLES, {KEY: table})
    patch.start()
    return events.band_check(mat)(), patch


def _y(p, t):
    return (0.0, p, t, t, 0.0, 0.0)


K = (1.0, 1.0, 0.0, 0.0, 0.0, 0.0)            # k[P] = 1, k[T] = 0: an isothermal step, so L is E's slope alone


def _slope_k(p):
    """Stages with P·dT/dP = 128 K per ln P, so ½·h_floor·L = ½·(0.05/64)·2·128 ≈ 0.1 K at the floor."""
    s = 128.0 / p
    return (1.0, 1.0, s, s, 0.0, 0.0)


class BandTest(unittest.TestCase):
    """Notes 13 §1 / 13a: the Lipschitz test, on a planted table, called as the stepper's step_check."""

    def tearDown(self):
        mock.patch.stopall()

    def test_a_sub_cell_bump_is_not_stepped_over(self):
        """§1 «bump»: g = −10 K at both ends, a +30 K bump of E in a cell between them: the step is halved."""
        chk, _p = _check(_Table(bump=lambda i: 30.0 if i == 10 else 0.0))
        pa, pb = math.exp(_Table().lnp[8]), math.exp(_Table().lnp[12])
        t = 2000.0 - OFF + 10.0
        self.assertEqual(chk(0.0, _y(pa, t), 1.0, _y(pb, t), K, K), "halve")

    def test_control_flat_edge_passes(self):
        chk, _p = _check(_Table())
        pa, pb = math.exp(_Table().lnp[8]), math.exp(_Table().lnp[12])
        self.assertIsNone(chk(0.0, _y(pa, 2000.0 - OFF + 10.0), 1.0, _y(pb, 2000.0 - OFF + 10.0), K, K))

    def test_a_bump_from_above_across_w(self):
        """13a item 2: g = W + 10 K at both ends and a −30 K dip of E between them reaches across g = W."""
        chk, _p = _check(_Table(bump=lambda i: -30.0 if i == 10 else 0.0))
        pa, pb = math.exp(_Table().lnp[8]), math.exp(_Table().lnp[12])
        t = 2000.0 - OFF - W - 10.0
        self.assertEqual(chk(0.0, _y(pa, t), 1.0, _y(pb, t), K, K), "halve")

    def test_a_crossing_step_is_accepted(self):
        """13a item 1: g changes sign across an edge over the step: accepted as is (no band event exists)."""
        chk, _p = _check(_Table())
        pa, pb = math.exp(_Table().lnp[8]), math.exp(_Table().lnp[12])
        self.assertIsNone(chk(0.0, _y(pa, 2000.0 - OFF + 10.0), 1.0, _y(pb, 2000.0 - OFF - 10.0), K, K))

    def test_the_t_margin_is_exercised(self):
        """§1 «margin»: with E flat, L is BAND_T_MARGIN·|P·dT/dP| at the ends; a step that passes at the true slope
        fails once the margin doubles it."""
        chk, _p = _check(_Table())
        pa = math.exp(_Table().lnp[8])
        pb = pa * math.exp(0.01)
        slope = 1.0e-7                               # dT/dP [K/Pa]: P·dT/dP ≈ 270 K per ln P at 2.7 GPa
        k = (1.0, 1.0, slope, slope, 0.0, 0.0)
        lt = max(pa, pb) * slope
        g = 0.5 * 0.01 * lt * 1.5                    # above ½·h·L at the true slope, below at 2× it
        t = 2000.0 - OFF - g
        self.assertEqual(chk(0.0, _y(pa, t), 1.0, _y(pb, t - 0.0), k, k), "halve")

    def test_a_true_touch_is_disclosed_once(self):
        """§1 «tangent touch» with 13b: g approaches 0 from below, touches at the floor and turns away: one band_graze."""
        chk, _p = _check(_Table())
        lnp0 = _Table().lnp[8]
        floor = 0.05 / events.BAND_FLOOR_DIV
        k = _slope_k(math.exp(lnp0))
        g_seq = [-0.05, -0.02, -0.01, -0.03, -0.2]           # closing in at the floor, then away on the same side
        got = []
        for i in range(len(g_seq) - 1):
            pa, pb = math.exp(lnp0 + i * floor), math.exp(lnp0 + (i + 1) * floor)
            r = chk(0.0, _y(pa, 2000.0 - OFF - g_seq[i]), 1.0, _y(pb, 2000.0 - OFF - g_seq[i + 1]), k, k)
            got.append(r)
        grazes = [r for r in got if isinstance(r, dict)]
        self.assertEqual(len(grazes), 1, got)
        self.assertEqual((grazes[0]["edge"], round(grazes[0]["min_abs_g"], 6)), (0.0, 0.01))

    def test_an_approach_that_crosses_is_not_a_graze(self):
        """13b: the same approach, then g crosses 0: no band_graze (the candidate is dropped)."""
        chk, _p = _check(_Table())
        lnp0 = _Table().lnp[8]
        floor = 0.05 / events.BAND_FLOOR_DIV
        k = _slope_k(math.exp(lnp0))
        g_seq = [-0.05, -0.02, -0.01, 0.02, 0.2]
        got = []
        for i in range(len(g_seq) - 1):
            pa, pb = math.exp(lnp0 + i * floor), math.exp(lnp0 + (i + 1) * floor)
            got.append(chk(0.0, _y(pa, 2000.0 - OFF - g_seq[i]), 1.0, _y(pb, 2000.0 - OFF - g_seq[i + 1]), k, k))
        self.assertFalse([r for r in got if isinstance(r, dict)], got)


class BandTestScope(unittest.TestCase):
    """13a item 5 and acceptance: no band test without a table phase (Earth, Venus); none in the fixed mode."""

    def test_earth_has_no_band_test(self):
        from solver import from_v1, solve as sv
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        views = sv._views(body)
        self.assertTrue(all(sv._band(v) is None for v in views.values()))

    def test_fixed_mode_mars_is_unchanged_by_the_test(self):
        from solver import context, from_v1, member as mb, solve as sv
        body, _aside = from_v1.load_v1("engine/bodies/mars.yaml")
        body, _m = mb.member_of(body)
        opt = context.Options(sensitivity_dt=0.0, fixed_dr=2000.0)
        x = 0.5 * (body.closure.lo + body.closure.hi)
        a = sv.inward(body, sv._views_at(body, sv._views(body), x), x, opt)
        with mock.patch.object(events, "band_check", lambda *aa, **kk: None):
            b = sv.inward(body, sv._views_at(body, sv._views(body), x), x, opt)
        self.assertIsInstance(a, sv.PassOut, a)
        self.assertEqual((a.F, a.y), (b.F, b.y))

    def test_control_adaptive_mars_is_changed_by_the_test(self):
        from solver import context, from_v1, member as mb, solve as sv
        body, _aside = from_v1.load_v1("engine/bodies/mars.yaml")
        body, _m = mb.member_of(body)
        body = dataclasses.replace(body, surface=dataclasses.replace(body.surface, t_pot=1980.0))
        opt = context.Options(sensitivity_dt=0.0)
        _ans, x = sv.solve(body, opt)
        a = sv.inward(body, sv._views_at(body, sv._views(body), x), x, opt)
        with mock.patch.object(events, "band_check", lambda *aa, **kk: None):
            b = sv.inward(body, sv._views_at(body, sv._views(body), x), x, opt)
        self.assertGreater(a.counters.get("band_halved", 0), 0)
        self.assertNotEqual(a.F, b.F)


class LidReadsItsOwnT(unittest.TestCase):
    """13a item 4: in a lid the cap reads y[3] (the profile T), in a segment y[2]."""

    def test_t_index(self):
        from solver import from_v1, member as mb, solve as sv
        body, _aside = from_v1.load_v1("engine/bodies/mars.yaml")
        body, _m = mb.member_of(body)
        mat = sv._views(body)["mantle"].mat
        p = 5.0e9
        ph = mat.phase_at(p)
        from solver import legacy_materials as lm
        edge, off = lm.table_band(ph)[:2]
        t_in = edge(p) - off - 0.5 * W                       # in the band
        t_far = t_in - 1000.0                                # far above the band: g = −1000 + … far outside
        y = (0.0, p, t_far, t_in, 0.0, 0.0)
        k1 = (0.0, 1.0, 1.0e-8, 1.0e-8, 0.0, 0.0)
        hc = p * lm.table_cell_factor(ph)
        self.assertEqual(events.step_cap(mat, t_index=3)(0.0, y, k1), hc)
        self.assertGreater(events.step_cap(mat, t_index=2)(0.0, y, k1), hc)


if __name__ == "__main__":
    unittest.main()
