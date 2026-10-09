# 적분 걸음 시험 — 계수표(scipy 대조), 정확도, 사건 착지, 조밀 출력, 폭주 방지, 거절 멈춤 (등록 S1)
"""S1 acceptance of rewrite/phase1-a1-impl.frozen.md, each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_stepper
"""
import math
import unittest
from fractions import Fraction as Fr

from solver import stepper as st


def _opts(**kw):
    base = dict(rtol=1e-10, floors=(1e-12,), h0=1e-3, h_min=1e-14, h_max=0.1, max_steps=100000)
    base.update(kw)
    return st.Options(**base)


def table_mismatches(C, A, B5, B4, rk):
    """Entries of a DP table that differ from scipy's RK45 (C, A, B, E with E = b − b̂ in scipy)."""
    bad = []
    for i, c in enumerate(C[:6]):                # scipy keeps the six stage nodes; the 7th (FSAL) is c = 1
        if float(c) != rk.C[i]:
            bad.append(("C", i))
    for i, row in enumerate(A[:6]):              # scipy's A is 6 × 5; our row 7 is b̂ (checked as B below)
        for j, a in enumerate(row):
            if float(a) != rk.A[i][j]:
                bad.append(("A", i, j))
    if A[6] != tuple(B5[:6]):
        bad.append(("A", 6))
    for i in range(6):
        if float(B5[i]) != rk.B[i]:
            bad.append(("B", i))
    for i in range(7):
        if float(B4[i] - B5[i]) != rk.E[i]:      # scipy's E is b − b̂ (opposite sign to b̂ − b)
            bad.append(("E", i))
    return bad


class Coefficients(unittest.TestCase):
    def test_equal_scipy_rk45(self):
        from scipy.integrate._ivp.rk import RK45
        self.assertEqual(table_mismatches(st.C, st.A, st.B5, st.B4, RK45), [])

    def test_control_planted_entry_fails(self):
        from scipy.integrate._ivp.rk import RK45
        A = list(st.A)
        A[3] = (A[3][0], A[3][1] + Fr(1, 10**9), A[3][2])
        self.assertEqual(table_mismatches(st.C, tuple(A), st.B5, st.B4, RK45), [("A", 3, 1)])

    def test_row_sums_are_c(self):
        for i in range(1, 7):
            self.assertEqual(sum(st.A[i]), st.C[i])
        self.assertEqual(sum(st.B5), 1)
        self.assertEqual(sum(st.B4), 1)


class Accuracy(unittest.TestCase):
    def test_exponential_both_directions(self):
        f = lambda x, y: (y[0],)
        r = st.run(f, 0.0, (1.0,), 1.0, _opts())
        self.assertEqual(r.stop.kind, "end")
        self.assertLess(abs(r.y[0] - math.e) / math.e, 1e-9)
        r = st.run(f, 1.0, (math.e,), 0.0, _opts())
        self.assertLess(abs(r.y[0] - 1.0), 1e-9)

    def test_control_loose_rtol_misses(self):
        f = lambda x, y: (y[0],)
        r = st.run(f, 0.0, (1.0,), 1.0, _opts(rtol=1e-3, h0=0.5, h_max=1.0))
        self.assertGreater(abs(r.y[0] - math.e) / math.e, 1e-9)


class Dense(unittest.TestCase):
    def test_reproduces_nodes(self):
        f = lambda x, y: (math.cos(x),)
        r = st.run(f, 0.0, (0.0,), 3.0, _opts())
        for x, y, _ in r.path:
            self.assertLessEqual(abs(st.dense(r.path, x)[0] - y[0]), 1e-14)

    def test_between_nodes(self):
        f = lambda x, y: (math.cos(x),)
        r = st.run(f, 0.0, (0.0,), 3.0, _opts())
        # cubic Hermite midpoint error ≤ h⁴/384 · max|y⁗| (+ the step's own error); y⁗ = sin, |·| ≤ 1
        for a, b in zip(r.path, r.path[1:]):
            xm = 0.5 * (a[0] + b[0])
            bound = (b[0] - a[0]) ** 4 / 384 + 1e-9
            self.assertLessEqual(abs(st.dense(r.path, xm)[0] - math.sin(xm)), bound)


class Events(unittest.TestCase):
    def test_lands_on_event(self):
        f = lambda x, y: (1.0 + 0.3 * math.sin(5 * x),)
        target = 0.37
        ev = st.Event("cross", lambda x, y: y[0] - target)
        r = st.run(f, 0.0, (0.0,), 2.0, _opts(h0=0.05), [ev])
        self.assertEqual((r.stop.kind, r.event), ("event", "cross"))
        self.assertLessEqual(abs(r.y[0] - target), 1e-12)
        self.assertGreaterEqual(r.y[0] - target, 0.0)          # landed on the new side

    def test_control_events_off_passes_through(self):
        f = lambda x, y: (1.0 + 0.3 * math.sin(5 * x),)
        r = st.run(f, 0.0, (0.0,), 2.0, _opts(h0=0.05))
        self.assertEqual(r.stop.kind, "end")

    def test_non_terminal_event_continues(self):
        f = lambda x, y: (1.0,)
        ev = st.Event("mid", lambda x, y: y[0] - 0.5, terminal=False)
        r = st.run(f, 0.0, (0.0,), 1.0, _opts(h0=0.3, h_max=0.3), [ev])
        self.assertEqual(r.stop.kind, "end")
        self.assertEqual([e[0] for e in r.events], ["mid"])
        self.assertLessEqual(abs(r.events[0][1] - 0.5), 1e-12)

    def test_chatter_guard_trips(self):
        f = lambda x, y: (1.0,)
        ev = st.Event("buzz", lambda x, y: math.sin(1e4 * x) + 1e-3, terminal=False)
        r = st.run(f, 0.0, (0.0,), 1.0, _opts(h0=1e-2, h_max=1e-2, event_restarts_run=50), [ev])
        self.assertEqual(r.stop.kind, "chatter")

    def test_control_raised_caps_still_stop(self):
        f = lambda x, y: (1.0,)
        ev = st.Event("buzz", lambda x, y: math.sin(1e4 * x) + 1e-3, terminal=False)
        r = st.run(f, 0.0, (0.0,), 1.0, _opts(h0=1e-2, h_max=1e-2, event_restarts_run=5000, max_steps=80), [ev])
        self.assertEqual(r.stop.kind, "max_steps")


class Refusal(unittest.TestCase):
    def test_refusing_rhs_stops_at_the_wall(self):
        wall = 0.6
        f = lambda x, y: st.Stop("domain", {"x": x}) if x > wall else (1.0,)
        r = st.run(f, 0.0, (0.0,), 1.0, _opts(h0=0.1, h_min=1e-10))
        self.assertEqual(r.stop.kind, "refused")
        self.assertLessEqual(wall - r.x, 1e-9)
        self.assertLessEqual(r.x, wall)


if __name__ == "__main__":
    unittest.main()
