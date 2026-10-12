# SR1 시험 — 감도의 근 자리 분해능 노트: 들쭉날쭉한 F 의 시행 폭, 매끈한 대조의 guard 항, 탐침 쪽 규칙, 빠지는 경우, 값 불변
"""SR1 «sensitivity_resolution» (rewrite/sr1-sensitivity-resolution-registration.frozen.md §4). Each test fails on
707aa7a4 (no such Note there).

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_sr1
"""
import dataclasses
import unittest
from types import SimpleNamespace as NS
from unittest import mock

from solver import closure as cl, context, from_v1, solve as sv
from solver import stepper as st

X2 = 1000.0
RT = {"tol_F": 1e-6, "s": 1e-6, "delta": 0.01, "far": (None, None)}      # guard term 2·tol/s = 2.0


def _q(key, s):
    return NS(key=key, point=1.0, sensitivity=s)


def _res(trials, sides, kept, new=(_q("radius", 0.5),), q2=None):
    acc2 = NS(F=0.0)
    b2 = NS()
    with mock.patch.object(sv, "_quantities", lambda b, p, sid, x: p.quantities):
        return sv._sensitivity_resolution(b2, X2, acc2, q2 or {"radius": 2.0}, list(new), 10.0, RT, trials, sides,
                                          kept).fields


def _sides(plus=None, minus=None):
    return [{"side": -1.0, "x1": X2 - 0.01, "x2": X2 - 0.02, "F1": None, "F2": None},
            {"side": 1.0, "x1": X2 + 0.01, "x2": X2 + 0.02, "F1": None, "F2": None}], \
        {X2 + 0.01: plus, X2 - 0.01: minus}


def _pass(r):
    return NS(quantities=[NS(key="radius", point=r)])


class Extent(unittest.TestCase):
    def test_a_jagged_crossing_set_is_measured_from_the_trials(self):
        """A sawtooth with excursions ±tol/2 sampled at ±25 around x2 (a crossing set 50 wide): x_res comes from
        «trials» and is the run of near trials, 50, ≫ the guard's 2.0; the far scan points beyond it are not taken
        (E is a lower bound)."""
        trials = [cl.Trial(X2 + d, (5e-7 if i % 2 else -5e-7), None, "brent") for i, d in enumerate(range(-25, 26, 5))]
        trials += [cl.Trial(X2 - 200.0, -1.0, None, "scan"), cl.Trial(X2 + 200.0, 1.0, None, "scan")]
        sides, kept = _sides(plus=_pass(2.0 + 1e-3))
        got = _res(trials, sides, kept)
        self.assertEqual(got["x_res_from"], "trials")
        self.assertAlmostEqual(got["x_res"], 50.0, delta=1e-9)

    def test_control_smooth_f_gives_the_guard_term(self):
        trials = [cl.Trial(X2 - 100.0, -0.1, None, "scan"), cl.Trial(X2 + 100.0, 0.1, None, "scan")]
        sides, kept = _sides(plus=_pass(2.0 + 1e-3))
        got = _res(trials, sides, kept)
        self.assertEqual((got["x_res_from"], got["x_res"]), ("guard", 2.0))

    def test_per_key_follows_dq_dx(self):
        trials = [cl.Trial(X2 - 100.0, -0.1, None, "scan"), cl.Trial(X2 + 100.0, 0.1, None, "scan")]
        sides, kept = _sides(plus=_pass(2.0 + 1e-3))              # dq/dx = 1e-3 / 0.01 = 0.1 per unit x
        got = _res(trials, sides, kept)
        self.assertAlmostEqual(got["per_key"]["radius"], 0.1 * 2.0 / 10.0 / 0.5, delta=1e-12)


class ProbeSide(unittest.TestCase):
    def test_the_minus_side_when_the_plus_side_stopped(self):
        trials = [cl.Trial(X2 - 100.0, -0.1, None, "scan"), cl.Trial(X2 + 100.0, 0.1, None, "scan")]
        sides, kept = _sides(plus=st.Stop("refused"), minus=_pass(2.0 - 1e-3))
        got = _res(trials, sides, kept)
        self.assertEqual(got["probe_side"], -1.0)
        self.assertIn("radius", got["per_key"])

    def test_both_stopped_leaves_per_key_empty_and_names_both(self):
        trials = [cl.Trial(X2 - 100.0, -0.1, None, "scan"), cl.Trial(X2 + 100.0, 0.1, None, "scan")]
        sides, kept = _sides(plus=st.Stop("refused"), minus=st.Stop("chatter"))
        got = _res(trials, sides, kept)
        self.assertEqual(dict(got["per_key"]), {})
        self.assertIn("refused", got["probe_side"])
        self.assertIn("chatter", got["probe_side"])


def _earth():
    body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
    return body


class OnRealSolves(unittest.TestCase):
    def test_earth_carries_one_resolution_note(self):
        ans, _x = sv.solve(_earth(), context.Options())
        n = [x for x in ans.notes if x.kind == "sensitivity_resolution"]
        self.assertEqual(len(n), 1)
        self.assertEqual(n[0].fields["scope"], "root placement")
        self.assertEqual(n[0].fields["probe_side"], 1.0)            # both probe passes answer: the + side first (68)
        self.assertEqual(set(n[0].fields["per_key"]), {q.key for q in ans.quantities if q.sensitivity is not None})

    def test_omitted_sensitivity_gives_no_resolution(self):
        real, calls = sv._root_tolerance, []

        def rt(*a, **k):
            out = real(*a, **k)
            calls.append(1)
            return {**out, "tol_F": 0.0} if len(calls) == 2 else out
        with mock.patch.object(sv, "_root_tolerance", rt):
            ans, _x = sv.solve(_earth(), context.Options())
        kinds = [x.kind for x in ans.notes]
        self.assertIn("sensitivity_not_measured", kinds)
        self.assertNotIn("sensitivity_resolution", kinds)

    def test_fixed_mode_gives_none(self):
        ans, _x = sv.solve(_earth(), context.Options(fixed_dr=20000.0))
        self.assertNotIn("sensitivity_resolution", [x.kind for x in getattr(ans, "notes", ())])

    def test_values_are_unchanged_by_the_note(self):
        ans, _x = sv.solve(_earth(), context.Options())
        from solver import result
        with mock.patch.object(sv, "_sensitivity_resolution", lambda *a, **k: result.Note("sensitivity_resolution", "x", {})):
            bare, _x2 = sv.solve(_earth(), context.Options())
        self.assertEqual([(q.key, q.point, q.sensitivity) for q in ans.quantities],
                         [(q.key, q.point, q.sensitivity) for q in bare.quantities])


if __name__ == "__main__":
    unittest.main()
