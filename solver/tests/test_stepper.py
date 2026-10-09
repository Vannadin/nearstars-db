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

    def test_earliest_crossing_wins_even_if_listed_later(self):
        f = lambda x, y: (1.0,)
        a = st.Event("A", lambda x, y: y[0] - 0.45, terminal=False)
        b = st.Event("B", lambda x, y: y[0] - 0.40, terminal=True)
        r = st.run(f, 0.0, (0.0,), 1.0, _opts(h0=0.3, h_max=0.3), [a, b])
        self.assertEqual((r.stop.kind, r.event), ("event", "B"))
        self.assertLessEqual(abs(r.y[0] - 0.40), 1e-12)

    def test_both_crossings_in_one_step_land_in_order(self):
        f = lambda x, y: (1.0,)
        a = st.Event("A", lambda x, y: y[0] - 0.45, terminal=False)
        b = st.Event("B", lambda x, y: y[0] - 0.40, terminal=False)
        r = st.run(f, 0.0, (0.0,), 1.0, _opts(h0=0.3, h_max=0.3), [a, b])
        self.assertEqual([e[0] for e in r.events], ["B", "A"])


def _cap(r):
    return r.stop.kind, (r.stop.record or {}).get("cap_name")


class Guard(unittest.TestCase):
    """Each cap of the event guard trips with its own name, and each has a control that does not trip (r2 B2)."""
    f = staticmethod(lambda x, y: (1.0,))

    def test_min_progress(self):
        ev = st.Event("double", lambda x, y: (y[0] - 0.5) * (y[0] - 0.505), terminal=False)
        r = st.run(self.f, 0.0, (0.0,), 1.0, _opts(h0=3e-3, h_max=3e-3, event_min_progress=1e-2), [ev])
        self.assertEqual(_cap(r), ("chatter", "EVENT_MIN_PROGRESS"))
        r = st.run(self.f, 0.0, (0.0,), 1.0, _opts(h0=3e-3, h_max=3e-3, event_min_progress=0.0), [ev])
        self.assertEqual(r.stop.kind, "end")
        self.assertEqual(len(r.events), 2)                      # control: both crossings land, none skipped

    def test_restarts_step(self):
        evs = [st.Event(f"e{k}", (lambda x, y, c=0.40 + 0.01 * k: y[0] - c), terminal=False) for k in range(6)]
        r = st.run(self.f, 0.0, (0.0,), 1.0, _opts(h0=0.3, h_max=0.3, event_restarts_step=4), evs)
        self.assertEqual(_cap(r), ("chatter", "EVENT_RESTARTS_STEP"))
        r = st.run(self.f, 0.0, (0.0,), 1.0, _opts(h0=0.3, h_max=0.3, event_restarts_step=10), evs)
        self.assertEqual((r.stop.kind, len(r.events)), ("end", 6))

    def test_restarts_solve(self):
        evs = [st.Event(f"e{k}", (lambda x, y, c=(k + 0.5) / 60: y[0] - c), terminal=False) for k in range(60)]
        r = st.run(self.f, 0.0, (0.0,), 1.0, _opts(h0=1e-3, h_max=1e-3, event_restarts_run=50), evs)
        self.assertEqual(_cap(r), ("chatter", "EVENT_RESTARTS_SOLVE"))
        r = st.run(self.f, 0.0, (0.0,), 1.0, _opts(h0=1e-3, h_max=1e-3, event_restarts_run=100), evs)
        self.assertEqual((r.stop.kind, len(r.events)), ("end", 60))

    def test_rewalks(self):
        ev = st.Event("curved", lambda x, y: math.tanh(50 * (y[0] - 0.4123)), terminal=False)
        r = st.run(self.f, 0.0, (0.0,), 1.0, _opts(h0=0.3, h_max=0.3, event_rewalks=1), [ev])
        self.assertEqual(_cap(r), ("chatter", "EVENT_REWALKS"))
        r = st.run(self.f, 0.0, (0.0,), 1.0, _opts(h0=0.3, h_max=0.3, event_rewalks=40), [ev])
        self.assertEqual(r.stop.kind, "end")
        self.assertLessEqual(abs(r.events[0][2][0] - 0.4123), 1e-12)

    def test_max_steps_is_a_stop(self):
        r = st.run(self.f, 0.0, (0.0,), 1.0, _opts(h0=1e-3, h_max=1e-3, max_steps=80))
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


class HminRecord(unittest.TestCase):
    def test_h_min_stop_carries_registry_fields(self):
        f = lambda x, y: (1.0 / (x - 0.5) ** 2 if x != 0.5 else 1e300,)     # a pole: the step can't pass it
        r = st.run(f, 0.0, (0.0,), 1.0, _opts(h0=0.1, h_min=1e-9))
        self.assertEqual(r.stop.kind, "h_min")
        for k in ("h", "h_min", "m_at", "err_norm", "rejected_in_row"):
            self.assertIn(k, r.stop.record)
        self.assertGreater(r.stop.record["rejected_in_row"], 0)
