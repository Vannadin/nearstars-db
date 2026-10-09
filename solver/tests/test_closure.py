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
