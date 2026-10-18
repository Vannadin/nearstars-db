# 단계 A 틈새 사격·가장 가까운 벽 시험 — 사격은 매 스캔 뒤(F12 가 판정), 틈새 문제의 이름, 공개 기록, 벽 추세는 스캔 점에서·도달 확인
"""prereg-gap-wall (frozen f786704e, 68 CLEAR 08699f14) with post-freeze note 1: G1–G4 (gap shots after every scan,
named, disclosed), W1–W4 (the nearest-wall trend on scan points with a reach check), and review 2's T-02 (the halving
loop's other branches and its bound).

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_gap_wall
"""
import math
import unittest
from types import SimpleNamespace as NS
from unittest import mock

from solver import closure as cl, context, from_v1, material_view as mv, refusals, solve as sv
from solver import stepper as st


def _deep(x, top=43.0):
    return st.Stop("refused", {"p": 3.5e11 * (top / x)})          # too deep: P above a material's top


def _shallow(x, bottom=46.0):
    return st.Stop("refused", {"p": 1.2e10 * (bottom / x)})       # too shallow: P under its bottom


def F_root_and_pair(x):
    """68's probe: a solvable gap at 43–46 between opposite walls, and a solved branch with its own root at 80."""
    if x < 43.0:
        return _deep(x)
    if x <= 46.0:
        return x - 44.0
    if x <= 70.0:
        return _shallow(x)
    return x - 80.0


def _only_when_nothing_solved(saved):
    """The mutant R2-R-S-01 named: shoot the gaps only when no scan point solved."""
    def mutant(F, trials, lo, hi):
        if any(t.F is not None for t in trials if t.kind == "scan"):
            return []
        return saved(F, trials, lo, hi)
    return mutant


class GapShotsAfterEveryScan(unittest.TestCase):
    def test_g1_a_gap_root_beside_a_scan_root_is_two_roots_and_disclosed(self):
        """G1: the scan brackets 80; the gap shot finds 44, so the outcome is two_roots, the gap's entry names 44 as
        its root and the kind without it as root. Control: the «only when nothing solved» mutant gives root [80]."""
        out = cl.solve_scalar(F_root_and_pair, 1.0, 100.0)
        self.assertEqual(out.kind, "two_roots")
        self.assertEqual(sorted(round(r, 9) for r in out.roots), [44.0, 80.0])
        (g,) = out.detail["gaps"]
        self.assertTrue(g["solved"])
        self.assertEqual([round(r, 9) for r in g["roots_from_gap"]], [44.0])
        self.assertEqual((g["outcome_kind"], g["kind_without"]), ("two_roots", "root"))
        self.assertGreater(g["calls"], g["shots"])           # the gap's walls and Brent trials count too
        with mock.patch.object(cl, "_gap_shots", _only_when_nothing_solved(cl._gap_shots)):
            no = cl.solve_scalar(F_root_and_pair, 1.0, 100.0)
        self.assertEqual((no.kind, [round(r, 9) for r in no.roots]), ("root", [80.0]))

    def test_g1_no_gap_no_entry(self):
        """A scan with no opposite-wall pair shoots nothing and discloses an empty list."""
        out = cl.solve_scalar(lambda x: x - 50.0, 1.0, 100.0)
        self.assertEqual((out.kind, out.detail["gaps"]), ("root", []))

    def test_g2_two_roots_reach_solve_two_roots_with_both(self):
        """G2: G1's outcome, mapped by solve's outcome step, is solve.two_roots with both roots (F12's input), and
        the gap's trace is recorded. F12 itself runs only without fixture views; it keeps its own tests."""
        out = cl.solve_scalar(F_root_and_pair, 1.0, 100.0)
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        rec = []
        orig = context.SolveContext.record
        def spy(self, kind, **data):
            rec.append((kind, data))
            return orig(self, kind, **data)
        with mock.patch.object(cl, "solve_scalar", return_value=out), \
                mock.patch.object(context.SolveContext, "record", spy):
            got, _w = sv._solve(body, context.Options(sensitivity_dt=0.0), None, None, None)
        self.assertEqual(got.id, "solve.two_roots")
        self.assertEqual(sorted(round(r, 9) for r in got.evidence["roots"]), [44.0, 80.0])
        gaps = [d for k, d in rec if k == "gap_shots"]
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0]["kind_without"], "root")

    def test_g3_a_brent_problem_in_a_gap_is_named(self):
        """G3: a Brent problem whose bracket lies in a shot gap gives NoAnswer unconverged with pass_kind «gap» and x
        inside the gap. Control: with in_gap blinded the tag is absent."""
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        trials = [cl.Trial(42.0, None, _deep(42.0), "scan"), cl.Trial(44.0, 1.0, None, "gap"),
                  cl.Trial(47.0, None, _shallow(47.0), "scan"), cl.Trial(79.0, -1.0, None, "scan"),
                  cl.Trial(81.0, 1.0, None, "scan")]
        out = cl.Outcome("unconverged", roots=[80.0], walls=[], trials=trials,
                         detail={"problems": [("unconverged", 44.5, 0.3)], "lo": 1.0, "hi": 100.0, "n_scan": 17,
                                 "gaps": [{"lo": 42.0, "hi": 47.0, "shots": 1, "solved": True}]})
        with mock.patch.object(cl, "solve_scalar", return_value=out):
            got, _w = sv._solve(body, context.Options(sensitivity_dt=0.0), None, None, None)
        self.assertEqual((got.reason, got.evidence.get("pass_kind"), got.evidence.get("x")),
                         ("unconverged", "gap", 44.5))
        with mock.patch.object(cl, "solve_scalar", return_value=out), \
                mock.patch.object(cl, "in_gap", lambda x, gaps: False):
            got, _w = sv._solve(body, context.Options(sensitivity_dt=0.0), None, None, None)
        self.assertNotIn("pass_kind", got.evidence)

    def test_g4_gap_is_a_registered_pass_kind(self):
        """G4 (R2-R-S-05): «gap» is a pass kind the registry accepts."""
        self.assertIn("gap", refusals.PASS_KINDS)
        refusals.no_answer("unconverged", "closure", budget_name="CLOSE_ITERS", budget_value=cl.CLOSE_ITERS,
                           last_residual=0.1, x=1.0, pass_kind="gap")


class GapHalvingLoop(unittest.TestCase):
    """Review 2 T-02: the planted gap test ends after two shots; the loop's other branches and its bound."""

    @staticmethod
    def _pair():
        return [cl.Trial(10.0, None, _deep(10.0, 10.0), "scan"), cl.Trial(40.0, None, _shallow(40.0, 40.0), "scan")]

    def test_a_shot_refusing_on_the_shallow_side_moves_the_upper_end(self):
        """A shot refusing opposite to the lower end (too shallow) replaces the upper end; the next shot lies between
        the lower end and it."""
        seen = []
        def F(x):
            seen.append(x)
            return _shallow(x, 40.0) if len(seen) == 1 else x - 15.0
        trials = self._pair()
        (g,) = cl._gap_shots(F, trials, 1.0, 100.0)
        self.assertEqual((g["shots"], g["solved"]), (2, True))
        self.assertAlmostEqual(seen[0], 20.0)
        self.assertTrue(10.0 < seen[1] < seen[0])

    def test_a_shot_refusing_on_the_deep_side_moves_the_lower_end(self):
        """The elif: a shot refusing like the lower end (too deep) replaces the lower end."""
        seen = []
        def F(x):
            seen.append(x)
            return _deep(x, 10.0 * 3.0) if len(seen) == 1 else x - 30.0
        (g,) = cl._gap_shots(F, self._pair(), 1.0, 100.0)
        self.assertEqual((g["shots"], g["solved"]), (2, True))
        self.assertTrue(seen[0] < seen[1] < 40.0)

    def test_a_shot_opposite_to_neither_end_stops(self):
        """The else-break: a shot refusing at a P that pairs with neither end (another material) ends the gap."""
        def F(x):
            return st.Stop("refused", {"p": 1.0e11, "material_id": "other"})
        (g,) = cl._gap_shots(F, self._pair(), 1.0, 100.0)
        self.assertEqual((g["shots"], g["solved"]), (1, False))

    def test_the_shot_budget_bounds_a_gap_that_never_solves(self):
        """GAP_SHOTS: a gap whose shots keep refusing on alternating sides stops after GAP_SHOTS shots."""
        n = []
        def F(x):
            n.append(x)
            return _shallow(x, 40.0) if len(n) % 2 else _deep(x, 1.0e3)
        (g,) = cl._gap_shots(F, self._pair(), 1.0, 100.0)
        self.assertEqual((g["shots"], g["solved"], len(n)), (cl.GAP_SHOTS, False, cl.GAP_SHOTS))


def _t(x, F, kind="scan"):
    return cl.Trial(x, F, None if F is not None else st.Stop("refused"), kind)


def _old_nearest_wall(out):
    """The rule before prereg-gap-wall (5c79511f), for W1's and W2's controls: the trend on the wall's nearest solved
    trial and the next one, with no reach check."""
    order = sorted((t for t in out.trials if t.kind != "isolated"), key=lambda t: t.x)
    best = None
    for w in out.walls:
        sgn = 1.0 if w.solved_side > w.x else -1.0
        side = sorted((t for t in order if t.F is not None and (t.x - w.x) * sgn > 0.0), key=lambda t: abs(t.x - w.x))
        if not side:
            continue
        a = side[0]
        b = side[1] if len(side) > 1 and not any(min(side[0].x, side[1].x) < t.x < max(side[0].x, side[1].x)
                                                  and t.F is None for t in order) else None
        if b is None or abs(a.F) >= abs(b.F):
            continue
        across = next((t for t in sorted((t for t in order if (t.x - w.x) * sgn < 0.0), key=lambda t: abs(t.x - w.x))
                       if t.F is not None), None)
        if across is not None and across.F * a.F > 0.0:
            continue
        if best is None or abs(a.F) < best[0]:
            best = (abs(a.F), w)
    return None if best is None else best[1]


class NearestWallOnScanPoints(unittest.TestCase):
    wall = cl.Wall(3.0, st.Stop("refused"), 2.99)

    def _out(self, trials, lo=0.5, hi=10.0):
        return NS(kind="no_bracket", trials=trials, walls=[self.wall], roots=[], detail={"lo": lo, "hi": hi})

    def test_w1_the_trend_is_read_on_scan_points_not_on_wall_trials(self):
        """W1: the scan points fall toward the wall while the wall bisection's last two trials rise (noise): the
        wall is named. Reversed: none. Control: the old rule reads the wall trials and answers the other way both
        times."""
        falls = self._out([_t(1.0, 1.0), _t(2.0, 0.5), _t(2.98, 0.30, "wall"), _t(2.99, 0.31, "wall"),
                           _t(3.0, None, "wall"), _t(4.0, None)])
        self.assertIs(sv._nearest_wall(falls), self.wall)
        self.assertIsNone(_old_nearest_wall(falls))
        rises = self._out([_t(1.0, 0.5), _t(2.0, 1.0), _t(2.98, 0.31, "wall"), _t(2.99, 0.30, "wall"),
                           _t(3.0, None, "wall"), _t(4.0, None)])
        self.assertIsNone(sv._nearest_wall(rises))
        self.assertIs(_old_nearest_wall(rises), self.wall)

    def test_w2_the_linear_zero_must_not_land_past_the_refusing_stretch(self):
        """W2: the scan points fall toward the wall, but F's linear zero lies past the next solved trial across the
        wall: none (no_bracket stands), and the wall is logged for W5. With the far end beyond the zero: the wall.
        Control: the old rule names the wall in the first case."""
        far = [_t(1.0, 1.0), _t(2.0, 0.9), _t(3.0, None, "wall"), _t(4.0, None), _t(5.0, -0.2)]
        log = []
        self.assertIsNone(sv._nearest_wall(self._out(far, hi=20.0), log))
        self.assertEqual([round(e["d"], 9) for e in log], [9.0])
        self.assertEqual(log[0]["far_end"], 5.0)
        self.assertIs(_old_nearest_wall(self._out(far, hi=20.0)), self.wall)
        open_end = [_t(1.0, 1.0), _t(2.0, 0.9), _t(3.0, None, "wall"), _t(4.0, None)]
        self.assertIsNone(sv._nearest_wall(self._out(open_end, hi=8.0)))      # range end 8: zero at 11 lies past it
        self.assertIs(sv._nearest_wall(self._out(open_end, hi=20.0)), self.wall)

    def test_w3_a_short_stretch_reads_its_ends_only_when_wide_enough(self):
        """W3: one scan point and a wall trial far enough apart give the trend; two trials closer than
        NOISE_STOP_MIN_WIDTH·|x| give none."""
        one = self._out([_t(1.0, None), _t(2.0, 0.5), _t(2.9, 0.3, "wall"), _t(3.0, None, "wall"), _t(4.0, None)])
        self.assertIs(sv._nearest_wall(one), self.wall)
        hair = self._out([_t(1.0, None), _t(2.9, 0.31, "wall"), _t(2.9 + 1e-7, 0.30, "wall"),
                          _t(3.0, None, "wall"), _t(4.0, None)])
        self.assertIsNone(sv._nearest_wall(hair))

    def test_w5_solve_records_the_reach_fallback(self):
        """W5's count: a no_bracket outcome whose wall fails the reach alone is recorded as nearest_wall_reach and
        stays solve.no_bracket."""
        body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
        node = {"m": 1.0, "r": 1.0, "P": 1.0e11, "T": 3000.0}
        stop = st.Stop("refused", mv.RecordRefusal("fe_prem_legacy", 1.1e11, 3010.0, "input.material_out_of_data",
                                                   "planted"), node)
        trials = [_t(1.0, 1.0), _t(2.0, 0.9), cl.Trial(3.0, None, stop, "wall"), cl.Trial(4.0, None, stop, "scan")]
        out = cl.Outcome("no_bracket", roots=[], walls=[cl.Wall(3.0, stop, 2.0)], trials=trials,
                         detail={"problems": [], "lo": 0.5, "hi": 8.0, "n_scan": 17})   # zero at 11, past 8
        rec = []
        orig = context.SolveContext.record
        def spy(self, kind, **data):
            rec.append((kind, data))
            return orig(self, kind, **data)
        with mock.patch.object(cl, "solve_scalar", return_value=out), \
                mock.patch.object(context.SolveContext, "record", spy):
            got, _w = sv._solve(body, context.Options(sensitivity_dt=0.0), None, None, None)
        self.assertEqual(got.id, "solve.no_bracket")
        self.assertEqual([d["wall"] for k, d in rec if k == "nearest_wall_reach"], [3.0])


if __name__ == "__main__":
    unittest.main()
