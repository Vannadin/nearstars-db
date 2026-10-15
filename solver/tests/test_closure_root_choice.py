# 두 근 닫힘의 근 고르기 시험 — 따뜻한 쪽 T_pot 쓸기와 이어지는 근 (오너 F12 82de8c46, 솔버 전체 f3463ebe)
"""Tests of the owner's F12 rule (owner-direction 82de8c46; solver-wide, f3463ebe): where the closure F has two roots, the answer is the root
continuous with the warm-side T_pot sweep, with the other root named in a `closure_root_choice` note.

`warm_continuation` is tested on synthetic sweeps (a fold like Mars's, where the upper root leaves the range on the warm
side; its mirror; a sweep that never resolves; one that meets a refusal). `solve` is tested end to end with `_solve`
replaced by a synthetic closure, so the half-range split, the note and the unchanged single-root path are exercised
without a real body.

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_closure_root_choice
"""
import dataclasses
import unittest

from solver import context, from_v1, refusals, result
from solver import solve as sv


def fold(lower_survives=True):
    """Roots at T_pot t: two roots that spread as t rises, one leaving the range [0.13, 0.25] by t = 1625 (Mars's
    shape: the upper one); its mirror keeps the upper root in range and sends the lower one out."""
    def at(t):
        if lower_survives:
            a, b = 0.2227 - 0.0012 * (t - 1600) / 10, 0.2370 + 0.0087 * (t - 1600) / 10
        else:
            a, b = 0.2227 - 0.0400 * (t - 1600) / 10, 0.2370 + 0.0005 * (t - 1600) / 10
        if t >= 1625:
            return ("root", a) if lower_survives else ("root", b)
        return "two_roots", (a, b)
    return at


def no_bracket():
    return refusals.make("solve.no_bracket", "fixture", x=None, closure_kind="composition", pass_kind="scan",
                         x_lo=0.13, x_hi=0.25, F_lo=1.0, F_hi=1.0, walls=[], solved_regions=[], n_scan=17)


class Continuation(unittest.TestCase):
    def test_lower_root_continues(self):
        chosen, trace, why = sv.warm_continuation(fold(True), 1600.0, (0.2227, 0.2370), 10.0)
        self.assertIsNone(why)
        self.assertEqual(chosen, 0.2227)
        self.assertEqual([t for t, _r in trace], [1600.0, 1610.0, 1620.0, 1630.0])

    def test_mirror_upper_root_continues(self):
        """The rule follows continuity, not «the lower root»: if the upper branch survives, it is chosen."""
        chosen, _trace, why = sv.warm_continuation(fold(False), 1600.0, (0.2227, 0.2370), 10.0)
        self.assertIsNone(why)
        self.assertEqual(chosen, 0.2370)

    def test_never_resolves(self):
        chosen, trace, why = sv.warm_continuation(lambda t: ("two_roots", (0.2, 0.3)), 1600.0, (0.2, 0.3), 10.0, 5)
        self.assertIsNone(chosen)
        self.assertEqual(len(trace), 6)
        self.assertIn("two roots persist", why)

    def test_meets_a_refusal(self):
        chosen, _trace, why = sv.warm_continuation(
            lambda t: ("other", "solve.material_record") if t > 1605 else ("two_roots", (0.2, 0.3)), 1600.0,
            (0.2, 0.3), 10.0)
        self.assertIsNone(chosen)
        self.assertIn("solve.material_record", why)


class EndToEnd(unittest.TestCase):
    """`solve` with `_solve` replaced by a synthetic closure on Mars's body file (no real integration)."""

    def setUp(self):
        got = from_v1.load_v1("engine/bodies/mars.yaml")
        self.body = got[0] if isinstance(got, tuple) else got
        self.real = sv._solve
        self.calls = []

    def tearDown(self):
        sv._solve = self.real

    def fake(self, roots_at):
        def _solve(body, options, warm, views, registry, _first=None, _id_options=None):
            t, lo, hi = body.surface.t_pot, body.closure.lo, body.closure.hi
            self.calls.append((t, lo, hi, options.sensitivity_dt))
            kind, val = roots_at(t) if t is not None else ("two_roots", (0.2227, 0.2370))
            roots = [val] if kind == "root" else list(val) if kind == "two_roots" else []
            inside = [r for r in roots if lo <= r <= hi]
            if kind == "other" or not inside:
                return no_bracket(), None
            if len(inside) == 2:
                return refusals.make("solve.two_roots", "fixture", x=None, closure_kind="composition",
                                     pass_kind="scan", roots=inside, F_scan=[], n_scan=17), None
            return result.Answer((), (), {}, (), (result.Note("graze", f"x={inside[0]}", {"x": inside[0]}),)), inside[0]
        return _solve

    def test_two_roots_answered_by_the_rule(self):
        sv._solve = self.fake(fold(True))
        out, _w = sv.solve(self.body, context.Options())
        self.assertIsInstance(out, result.Answer)
        note = next(n for n in out.notes if n.kind == "closure_root_choice")
        self.assertEqual(note.fields["chosen"], 0.2227)
        self.assertEqual(list(note.fields["others"]), [0.2370])
        self.assertEqual(list(note.fields["closure"]["range"]), [self.body.closure.lo, self.body.closure.hi])
        lo, hi = note.fields["closure"]["solved_in"]
        self.assertTrue(lo <= 0.2227 <= hi < 0.2370)
        self.assertEqual(next(n for n in out.notes if n.kind == "graze").fields["x"], 0.2227)
        self.assertTrue(all(c[3] == 0.0 for c in self.calls[1:-1]))      # sweep solves carry no sensitivity

    def test_second_value_is_the_chosen_root(self):
        """68 B1: on the rule path solve returns the chosen root as its second value, so member_of's forward member
        gets it (its float(x) on the closure axis)."""
        sv._solve = self.fake(fold(True))
        out, x = sv.solve(self.body, context.Options())
        self.assertEqual(x, 0.2227)
        from solver import member as mb
        seen = []

        class _Got(Exception):
            pass

        def capture(body, a, x):
            seen.append(x)
            raise _Got()
        real = mb.forward_member
        try:
            mb.forward_member = capture
            with self.assertRaises(_Got):
                mb.member_of(self.body)
        finally:
            mb.forward_member = real
        self.assertEqual(seen, [0.2227])

    def test_mirror_end_to_end(self):
        """68 G2: when the upper branch survives, the half solved is the upper half, without the lower root in it."""
        sv._solve = self.fake(fold(False))
        out, x = sv.solve(self.body, context.Options())
        self.assertEqual(x, 0.2370)
        note = next(n for n in out.notes if n.kind == "closure_root_choice")
        lo, hi = note.fields["closure"]["solved_in"]
        self.assertTrue(0.2227 < lo <= 0.2370 <= hi)

    def test_half_that_does_not_answer_keeps_the_refusal(self):
        """68 G3: if the chosen half does not answer alone, the two_roots refusal stands."""
        fake = self.fake(fold(True))

        def half_fails(body, options, warm, views, registry, _first=None, _id_options=None):
            if body.closure.hi < self.body.closure.hi or body.closure.lo > self.body.closure.lo:
                return no_bracket(), None
            return fake(body, options, warm, views, registry)
        sv._solve = half_fails
        out, x = sv.solve(self.body, context.Options())
        self.assertEqual((out.id, x), ("solve.two_roots", None))

    def test_fixture_views_never_take_the_rule(self):
        """68 G4: a solve with fixture views returns the two_roots refusal as it is."""
        sv._solve = self.fake(fold(True))
        out, _x = sv.solve(self.body, context.Options(), views={"core": object()})
        self.assertEqual(out.id, "solve.two_roots")
        self.assertEqual(len(self.calls), 1)

    def test_step_is_the_sensitivity_step(self):
        """68 G8: the sweep steps by options.sensitivity_dt when set (here 5 K), else WARM_STEP_K."""
        sv._solve = self.fake(fold(True))
        sv.solve(self.body, context.Options(sensitivity_dt=5.0))
        sweep = [c[0] for c in self.calls[1:] if c[1] == self.body.closure.lo and c[2] == self.body.closure.hi]
        self.assertEqual(sweep[:3], [1605.0, 1610.0, 1615.0])

    def test_mutant_picking_root_2_fails(self):
        """A negative control: had the rule taken the other root, the answer would carry it; it must not."""
        sv._solve = self.fake(fold(True))
        out, _w = sv.solve(self.body, context.Options())
        self.assertNotEqual(next(n for n in out.notes if n.kind == "graze").fields["x"], 0.2370)

    def test_single_root_unchanged(self):
        """A negative control: a closure with one root is answered exactly as before, with no note and no sweep."""
        sv._solve = self.fake(lambda t: ("root", 0.21))
        out, _w = sv.solve(self.body, context.Options())
        self.assertIsInstance(out, result.Answer)
        self.assertFalse([n for n in out.notes if n.kind == "closure_root_choice"])
        self.assertEqual(len(self.calls), 1)

    def test_undecided_sweep_keeps_the_refusal(self):
        sv._solve = self.fake(lambda t: ("two_roots", (0.20, 0.24)))
        out, _w = sv.solve(self.body, context.Options())
        self.assertIsInstance(out, result.Refusal)
        self.assertEqual(out.id, "solve.two_roots")
        self.assertNotIn("warm_sweep", out.evidence)                    # unchanged: C1's evidence fields

    def test_no_t_pot_keeps_the_refusal(self):
        sv._solve = self.fake(fold(True))
        b = dataclasses.replace(self.body, surface=dataclasses.replace(self.body.surface, t_pot=None))
        out, _w = sv.solve(b, context.Options())
        self.assertEqual(out.id, "solve.two_roots")


if __name__ == "__main__":
    unittest.main()
