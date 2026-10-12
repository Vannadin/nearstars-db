# 리뷰 수정 A2 시험 — 근 찾기: Brent 안의 고립 거절·Brent 시행의 새 괄호·민감도 근의 닫힘 검사
"""Post-phase-1 review fix batch A2 (rewrite/p1review/fix-plan.md): G2-C-01, G2-C-02 on synthetic F, as the review's
probes (probe1–3) built them; G2-C-03 (phase-1 design note 13 §2) on Earth with the guard's verdict planted. Each test
fails on 2fdcd7f1. Rebased onto S2 (3d170377): the guard on refine's Outcome and r2's two H2 tests (note 15a §2), refine
keeping «any refusal falls back» under G2-C-01's confirmation, and the screen's «< 2 solved → refine» branch (68 N75).

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p1fix_a2
"""
import math
import unittest

from unittest import mock

from solver import closure as cl, context, from_v1, solve as sv
from solver import stepper as st

X0 = 3.4e6
LO, HI = 0.05 * X0, 30.0 * X0


def _brent_xs(F):
    out = cl.solve_scalar(F, LO, HI)
    return [t.x for t in out.trials if t.kind == "brent"]


def _with_isolated(F, x_bad):
    """F with one isolated refusal at exactly x_bad (a landing failure, as at Earth 2064.76 K)."""
    def G(x):
        return st.Stop("chatter", {"event": "planted", "count": 9, "cap_name": "EVENT_REWALKS", "cap_value": 8}) \
            if x == x_bad else F(x)
    return G


def smooth(x):
    return math.tanh((x - X0) / 1.0e6)


def jittered(amp):
    def F(x):
        return 5.0e-7 * (x - X0) + amp * math.sin(x * 7.3e3)      # deterministic jitter at the root's resolution
    return F


class IsolatedInsideBrent(unittest.TestCase):
    def test_a_late_isolated_refusal_still_gives_the_root(self):
        """G2-C-01 (probe3): an isolated refusal at a late Brent trial gave unconverged/MAX_SPLITS."""
        xs = _brent_xs(smooth)
        for k in (3, 4):
            with self.subTest(k=k):
                out = cl.solve_scalar(_with_isolated(smooth, xs[k]), LO, HI)
                self.assertEqual(out.kind, "root")
                self.assertAlmostEqual(out.roots[0], X0, delta=1e-6 * X0)
                self.assertIn("isolated", [t.kind for t in out.trials])

    def test_control_a_confirmed_wall_still_splits(self):
        """Control: a refusal that its confirming shot repeats (a real wall around the root) is not isolated."""
        def walled(x):
            return st.Stop("refused", {"planted": True}) if abs(x - X0) < 1.0e3 else smooth(x)
        out = cl.solve_scalar(walled, LO, HI)
        self.assertNotEqual(out.kind, "root")


class BrentTrialsOpenNoBracket(unittest.TestCase):
    def test_jitter_near_the_root_gives_one_root(self):
        """G2-C-02 (probe1): after a split, Brent's near-root trials joined the sign search and split one root in two."""
        for amp in (1.0e-8, 1.0e-7):
            F = jittered(amp)
            xs = _brent_xs(F)
            for k in range(2, min(len(xs), 12)):
                with self.subTest(amp=amp, k=k):
                    out = cl.solve_scalar(_with_isolated(F, xs[k]), LO, HI)
                    self.assertEqual(out.kind, "root", (out.kind, out.roots))


class SensitivityRoot(unittest.TestCase):
    """G2-C-03 (phase-1 design note 13 §2): the T_pot + δ root gets the closure guard. Earth's real solve, with the
    guard's verdict planted on the sensitivity call only (the accepted root's guard runs first, its probes after)."""

    def _solve(self, **patches):
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        with mock.patch.multiple(sv, **patches):
            ans, _x = sv.solve(body, context.Options(materials="legacy"))
        return ans

    def test_a_jump_at_the_sensitivity_root_omits_the_sensitivity(self):
        real, calls = sv._root_tolerance, []

        def rt(*a, **k):
            out = real(*a, **k)
            calls.append(1)
            return {**out, "tol_F": 0.0} if len(calls) == 2 else out      # 2nd call: the sensitivity root
        ans = self._solve(_root_tolerance=rt)
        notes = [n for n in ans.notes if n.kind == "sensitivity_not_measured"]
        self.assertEqual([n.fields["reason"] for n in notes], ["closure_discontinuous"])
        self.assertTrue(all(q.sensitivity is None for q in ans.quantities))

    def test_a_failing_probe_side_keeps_the_sensitivity_and_discloses(self):
        real, calls = sv._side_check, []

        def side(*a, **k):
            out = real(*a, **k)
            calls.append(1)
            return {**out, "ok": False} if len(calls) <= 2 else out         # the sensitivity root's two sides
        ans = self._solve(_side_check=side)
        self.assertEqual([n.kind for n in ans.notes if n.kind.startswith("sensitivity")],
                         ["sensitivity_probe_disclosure"])
        self.assertTrue(any(q.sensitivity is not None for q in ans.quantities))
        self.assertNotIn("closure_probe_disclosure", [n.kind for n in ans.notes])   # the accepted root's are clean


class RefineGuard(unittest.TestCase):
    """Phase-1 design note 15a §2 (r2 H2): note 13 §2's guard applies to the root refine returns."""

    def _solve(self, refine, **patches):
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        with mock.patch.object(cl, "refine", refine), mock.patch.multiple(sv, **patches):
            ans, _x = sv.solve(body, context.Options(materials="legacy"))
        return ans

    def test_a_jump_at_the_refined_root_omits_the_sensitivity(self):
        real, got = cl.refine, []

        def refine(*a, **k):
            out = real(*a, **k)
            got.append(out)
            return out
        real_rt, calls = sv._root_tolerance, []

        def rt(*a, **k):
            out = real_rt(*a, **k)
            calls.append(a[3])
            return {**out, "tol_F": 0.0} if len(calls) == 2 else out
        ans = self._solve(refine, _root_tolerance=rt)
        self.assertEqual([o.kind for o in got], ["root"])                       # the sensitivity root is refine's
        self.assertEqual(calls[1], got[0].detail["brackets"][got[0].roots[0]])  # and the guard read refine's bracket
        self.assertEqual([n.fields["reason"] for n in ans.notes if n.kind == "sensitivity_not_measured"],
                         ["closure_discontinuous"])
        self.assertTrue(all(q.sensitivity is None for q in ans.quantities))

    def test_a_root_at_the_start_point_has_a_slope_and_is_guarded(self):
        """F2(x0) = 0 exactly: refine returns x0 with the pair (x0, x1) of finite width, s is finite and the guard runs
        (here it refuses: the planted zero is not F2's value at x0, so |F2(x0)| > tol_F)."""
        real, got = cl.refine, []

        def refine(F, x0, *a, **k):
            out = real(lambda x: 0.0 if x == x0 else F(x), x0, *a, **k)
            got.append(out)
            return out
        real_rt, rts = sv._root_tolerance, []

        def rt(*a, **k):
            out = real_rt(*a, **k)
            rts.append(out)
            return out
        ans = self._solve(refine, _root_tolerance=rt)
        out = got[0]
        x0 = out.roots[0]
        a, fa, b, fb = out.detail["brackets"][x0]["scan"]
        self.assertEqual((a, fa), (x0, 0.0))
        self.assertGreater(b - a, 0.0)
        self.assertTrue(math.isfinite(rts[1]["s"]) and rts[1]["s"] > 0.0)
        self.assertEqual([n.fields["reason"] for n in ans.notes if n.kind == "sensitivity_not_measured"],
                         ["closure_discontinuous"])


class RefineFallsBackOnARefusal(unittest.TestCase):
    """Note 15a §2: any refusal inside refine falls back (None); G2-C-01's confirmation inside Brent is not refine's."""

    def test_a_refusal_at_a_brent_trial_returns_none(self):
        x0 = X0 * (1.0 + 2.0e-5)
        clean = cl.refine(smooth, x0, LO, HI)
        xs = [t.x for t in clean.trials if t.kind == "brent"]
        self.assertGreater(len(xs), 1)
        self.assertIsNone(cl.refine(_with_isolated(smooth, xs[1]), x0, LO, HI))

    def test_control_solve_scalar_confirms_the_same_refusal(self):
        x0 = X0 * (1.0 + 2.0e-5)
        xs = [t.x for t in cl.refine(smooth, x0, LO, HI).trials if t.kind == "brent"]
        out = cl.solve_scalar(_with_isolated(smooth, xs[1]), LO, HI)
        self.assertEqual(out.kind, "root")


class ScreenRefinesWithFewerThanTwoSolved(unittest.TestCase):
    """Note 15 §1's screen (68 N75): fewer than two solved trials on the wall's solved side → the wall is refined."""

    def test_one_solved_trial_beside_the_wall_hides_a_root(self):
        w = cl.Wall(10.0, st.Stop("refused", {}), 9.0, located=False, tol=cl.WALL_TOL_COARSE)
        self.assertTrue(cl._root_may_hide(w, [cl.Trial(9.0, 5.0, None, "scan"), cl.Trial(10.0, None, w.stop, "scan")]))

    def test_control_two_far_solved_trials_clear_it(self):
        w = cl.Wall(10.0, st.Stop("refused", {}), 9.0, located=False, tol=cl.WALL_TOL_COARSE)
        trials = [cl.Trial(8.0, 101.0, None, "scan"), cl.Trial(9.0, 100.0, None, "scan"), cl.Trial(10.0, None, w.stop, "scan")]
        self.assertFalse(cl._root_may_hide(w, trials))


if __name__ == "__main__":
    unittest.main()
