# 리뷰 수정 A2 시험 — 근 찾기: Brent 안의 고립 거절·Brent 시행의 새 괄호·민감도 근의 닫힘 검사
"""Post-phase-1 review fix batch A2 (rewrite/p1review/fix-plan.md): G2-C-01, G2-C-02 on synthetic F, as the review's
probes (probe1–3) built them; G2-C-03 (phase-1 design note 13 §2) on Earth with the guard's verdict planted. Each test
fails on 2fdcd7f1.

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


if __name__ == "__main__":
    unittest.main()
