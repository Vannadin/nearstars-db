# 근 찾기 시험 — 거절 시행은 벽, 벽 위치, 두 근 보고, 벽 찾기 시행의 부호 바뀜 합류(N4) (등록 S3)
"""S3 acceptance of rewrite/phase1-a1-impl.frozen.md, each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_closure
"""
import unittest

from solver import closure
from solver import stepper as st

WALL = 3.0


def refusing_above(f):
    return lambda x: st.Stop("domain", {"x": x}) if x >= WALL else f(x)


def escalating(F, lo, hi):
    """The forbidden policy: the first refusing trial ends the solve."""
    for x in closure.scan_points(lo, hi):
        v = F(x)
        if isinstance(v, st.Stop):
            return closure.Outcome("refused", detail={"stop": v})
    return closure.solve_scalar(F, lo, hi)


def finds_root_beside_wall(solver) -> bool:
    out = solver(refusing_above(lambda x: x - 2.0), 1.0, 10.0)
    return out.kind == "root" and abs(out.roots[0] - 2.0) <= closure.CLOSE_TOL * 2.0 * 10


class Walls(unittest.TestCase):
    def test_root_on_solved_side_and_wall_located(self):
        out = closure.solve_scalar(refusing_above(lambda x: x - 2.0), 1.0, 10.0)
        self.assertEqual(out.kind, "root")
        self.assertAlmostEqual(out.roots[0], 2.0, delta=2.0 * closure.CLOSE_TOL * 10)
        self.assertEqual(len(out.walls), 1)
        w = out.walls[0]
        self.assertLessEqual(abs(w.x - WALL), closure.WALL_TOL * WALL)
        self.assertLess(w.solved_side, WALL)
        self.assertGreaterEqual(w.x, WALL)

    def test_control_escalation_fails(self):
        self.assertTrue(finds_root_beside_wall(closure.solve_scalar))
        self.assertFalse(finds_root_beside_wall(escalating))

    def test_no_bracket_names_walls(self):
        out = closure.solve_scalar(refusing_above(lambda x: x + 1.0), 1.0, 10.0)
        self.assertEqual(out.kind, "no_bracket")
        self.assertEqual(len(out.walls), 1)

    def test_nothing_solves(self):
        out = closure.solve_scalar(lambda x: st.Stop("domain", {}), 1.0, 10.0)
        self.assertEqual(out.kind, "no_solved")


class TwoRoots(unittest.TestCase):
    def test_u_shape_reports_both(self):
        out = closure.solve_scalar(lambda x: (x - 2.0) * (x - 5.0), 1.0, 10.0)
        self.assertEqual(out.kind, "two_roots")
        self.assertEqual(len(out.roots), 2)
        self.assertAlmostEqual(min(out.roots), 2.0, delta=1e-10)
        self.assertAlmostEqual(max(out.roots), 5.0, delta=1e-10)

    def test_control_single_root_is_not_two(self):
        out = closure.solve_scalar(lambda x: x - 2.0, 1.0, 10.0)
        self.assertEqual(out.kind, "root")


class N4(unittest.TestCase):
    """The only sign change lies between a scan point and a wall-location trial: F = 2.92 − x, wall at 3.0.
    The scan (17 log points on [1, 10]) has 2.74 (F > 0) next to 3.16 (wall); no scan pair changes sign."""
    F = staticmethod(refusing_above(lambda x: 2.92 - x))

    def test_wall_trials_join_the_search(self):
        out = closure.solve_scalar(self.F, 1.0, 10.0)
        self.assertEqual(out.kind, "root")
        self.assertAlmostEqual(out.roots[0], 2.92, delta=1e-10)

    def test_control_without_wall_trials_misses(self):
        out = closure.solve_scalar(self.F, 1.0, 10.0, use_wall_trials=False)
        self.assertEqual(out.kind, "no_bracket")


if __name__ == "__main__":
    unittest.main()


class BrentRefusal(unittest.TestCase):
    """A refusal met inside a Brent bracket is a wall: located, split, re-searched (r2 B3)."""

    @staticmethod
    def island(lo, hi, f):
        return lambda x: st.Stop("domain", {"x": x}) if lo < x < hi else f(x)

    def test_island_around_the_only_root(self):
        F = self.island(4.00, 4.05, lambda x: x - 4.02)
        out = closure.solve_scalar(F, 1.0, 10.0)
        self.assertNotEqual(out.kind, "root")          # the root sits inside the refusing island: not solvable
        self.assertEqual(out.roots, [])
        self.assertGreaterEqual(len(out.walls), 2)      # both island edges located
        self.assertTrue(all(w.located for w in out.walls))

    def test_island_beside_a_root_and_a_clean_root(self):
        F = self.island(4.03, 4.06, lambda x: (x - 4.02) * (x - 8.0))
        out = closure.solve_scalar(F, 1.0, 10.0)
        self.assertEqual(out.kind, "two_roots")
        self.assertAlmostEqual(min(out.roots), 4.02, delta=1e-10)
        self.assertAlmostEqual(max(out.roots), 8.0, delta=1e-10)


class NonFinite(unittest.TestCase):
    def test_none_residual_is_a_wall_not_solved(self):
        F = lambda x: None if x >= WALL else x - 2.0
        out = closure.solve_scalar(F, 1.0, 10.0)
        self.assertEqual(out.kind, "root")
        w = out.walls[0]
        self.assertLess(w.solved_side, WALL)
        self.assertGreaterEqual(w.x, WALL)
        self.assertEqual(w.stop.kind, "no_residual")

    def test_wall_shots_exhausted_is_flagged(self):
        import solver.closure as c
        saved = c.WALL_SHOTS
        try:
            c.WALL_SHOTS = 2
            out = c.solve_scalar(refusing_above(lambda x: x - 2.0), 1.0, 10.0)
            self.assertFalse(out.walls[0].located)
        finally:
            c.WALL_SHOTS = saved


class MaterialWall(unittest.TestCase):
    """S3 through the real chain: a material refusing above a pressure, rhs → stepper → closure (r2 N7)."""

    def test_root_found_beside_a_pressure_wall(self):
        import math
        from solver import rhs
        M, rho0 = 5.0e24, 5000.0
        r_true = (3 * M / (4 * math.pi * rho0)) ** (1 / 3)
        p_c = 3 * rhs.G * M ** 2 / (8 * math.pi * r_true ** 4)

        class Capped:
            def state(self, p, t, guess):
                return st.Stop("domain", {"p": p}) if p > 1.5 * p_c else (rho0, 0.0)

        def F(R):
            res = rhs.inward_pass(Capped(), M, R, 0.0, 0.0, rho0)
            return res.F if res.F is not None else res.stop

        out = closure.solve_scalar(F, 0.5 * r_true, 2.0 * r_true)
        self.assertEqual(out.kind, "root")
        self.assertLess(abs(out.roots[0] - r_true) / r_true, 1e-10)
        self.assertGreaterEqual(len(out.walls), 1)
        self.assertEqual(escalating(F, 0.5 * r_true, 2.0 * r_true).kind, "refused")   # control: escalation fails here


class MaxSplits(unittest.TestCase):
    def test_split_budget_gives_unconverged(self):
        import solver.closure as c
        scan = set(c.scan_points(1.0, 10.0))
        # inside (1.5, 3) only the scan points solve: Brent's first probe in the bracket around the root 2.0 refuses
        F = lambda x: x - 2.0 if (x in scan or not 1.5 < x < 3.0) else st.Stop("domain", {})
        saved = c.MAX_SPLITS
        try:
            c.MAX_SPLITS = 0
            out = c.solve_scalar(F, 1.0, 10.0)
            self.assertEqual((out.kind, out.detail.get("budget")), ("unconverged", "MAX_SPLITS"))
            c.MAX_SPLITS = 16                            # control: with budget, the split is walled and searched
            out = c.solve_scalar(F, 1.0, 10.0)
            self.assertNotEqual(out.kind, "unconverged")
        finally:
            c.MAX_SPLITS = saved

    def test_budget_name_is_registered(self):
        from solver import refusals
        self.assertIn("MAX_SPLITS", refusals.NO_ANSWER_BUDGETS)
