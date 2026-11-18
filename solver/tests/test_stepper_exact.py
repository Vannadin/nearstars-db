# EXACT 시험 — 걸친 거절 시도를 옛쪽 뿌리 걸음으로 바꾸는지, 거짓 교차(오차만 넘긴 끝값)에서 착지 없이 제어기 h 로 가는지, 진짜 교차는 착지하는지, 집계가 맞는지 (A1 impl note 9 E1·E6·E7, N2·N4; C2)
"""A1 impl post-freeze note 9 (frozen, artifacts main 21646821a): E1, E6, E7 and the mutants N2, N4, on analytic rhs.

Run from the worktree root:  PY -B -m unittest solver.tests.test_stepper_exact
"""
import math
import unittest
from unittest import mock

from solver import stepper as st

A, W = 1.0, 3.0
PMAX = 2 * A / W


def sine(x, y):
    return (0.0, A * math.sin(W * x), 0.0, 0.0, 0.0, 0.0)


def opt(h0=3.0):
    return st.Options(rtol=1e-8, floors=(1.0, 1e-9, 1.0, 1.0, 1.0, 1.0), h0=h0, h_min=1e-12, h_max=50.0,
                      max_steps=100000, event_tol=1e-12, event_rewalks=32, event_min_progress=1e-9)


def seam_at(pc):
    return st.Event("seam", lambda x, y: y[1] - pc, scale=1.0, terminal=False, seam=True, component=1)


def run(f, pc, h0=3.0, x1=4.0):
    nodes = []
    r = st.run(f, 0.0, (1.0, 0.0, 1.0, 1.0, 0.0, 0.0), x1, opt(h0), [seam_at(pc)],
               on_accept=lambda x, y: nodes.append((x, y[1])))
    return r, nodes


class FalsePositive(unittest.TestCase):
    """E6: a rejected trial whose end crosses only through its error (sine, seam at 1.02 × the true maximum)."""

    def test_trial_end_overshoots_no_landing(self):
        r, nodes = run(sine, 1.02 * PMAX)
        c = r.counters
        self.assertGreater(c.exact_tried, 0)
        self.assertEqual(len(r.events), 0)
        self.assertTrue(all(p < 1.02 * PMAX for _, p in nodes))
        self.assertEqual(r.stop.kind, "end")
        self.assertEqual(c.exact_tried, c.exact_unlanded + c.exact_failed + c.exact_replaced)
        self.assertEqual(c.exact_no_landing, c.exact_replaced)

    def test_replacement_accepted_without_landing_takes_the_controllers_h(self):
        self.planted_case()

    def planted_case(self):
        hs = []
        real_land, real_stepper = st._land, st._stepper

        def planted_land(f, ev, x, y, k1, h, out, g0, o, cnt):
            return ((x + 0.002 * h, None, None), None)

        def logging(o, stage_f=None):
            step = real_stepper(o, stage_f)

            def go(f, x, y, h, k1):
                hs.append(h)
                return step(f, x, y, h, k1)
            return go
        with mock.patch.object(st, "_land", planted_land), mock.patch.object(st, "_stepper", logging):
            r, nodes = run(sine, 1.02 * PMAX)
        c = r.counters
        self.assertEqual((c.exact_tried, c.exact_replaced, c.exact_no_landing), (1, 1, 1))
        self.assertEqual(len(r.events), 0)
        self.assertEqual(hs[0], 3.0)                         # the rejected trial
        self.assertAlmostEqual(hs[1], 0.006)                 # the replacement, to the planted root
        self.assertLessEqual(hs[2], 5 * 0.006 + 1e-12)       # the controller's next h
        self.assertNotEqual(hs[2], 3.0)                      # never h_restart without a landing
        return hs

    def test_N4_keeping_h_restart_fails(self):
        """N4: a mutant that keeps h_restart after a replacement with no landing restarts at the rejected h."""
        import inspect
        import textwrap
        src = textwrap.dedent(inspect.getsource(st.run))
        a = "        if h_restart is not None:                     # A1 impl note 9: a replacement accepted with nothing landed\n            cnt.exact_no_landing += 1\n        h_restart = None\n"
        self.assertIn(a, src)
        mut = src.replace(a, "        if h_restart is not None:\n            cnt.exact_no_landing += 1\n            h, h_restart = h_restart, None\n")
        ns = dict(vars(st))
        exec(mut, ns)
        with mock.patch.object(st, "run", ns["run"]):
            with self.assertRaises(AssertionError):
                self.planted_case()


class TrueCrossing(unittest.TestCase):
    """E6's control and E1: a seam the path does cross lands within event_tol, and no accepted step straddles it."""

    def test_lands_and_no_straddle(self):
        pc = 0.98 * PMAX
        r, nodes = run(sine, pc)
        self.assertGreater(len(r.events), 0)
        y_l = r.events[0][2]
        self.assertLessEqual(abs(y_l[1] - pc), 1e-12 * 1.0 + 1e-15)
        for (x0, p0), (x1, p1) in zip(nodes, nodes[1:]):
            if x1 > x0:                                       # a same-m pair is the landing's second node
                self.assertFalse((p0 - pc) * (p1 - pc) < 0.0 and abs(p0 - pc) > 1e-9 and abs(p1 - pc) > 1e-9,
                                 f"an accepted step straddles the seam: {p0} → {p1}")

    def test_kink_rhs_replacement_counted(self):
        """A derivative jump at the seam (dP/dx 1 → 3): the straddling trial is replaced, the seam lands."""
        pc = 0.5

        def kink(x, y):
            return (0.0, 1.0 if y[1] < pc else 3.0, 0.0, 0.0, 0.0, 0.0)
        r, nodes = run(kink, pc, h0=2.0, x1=2.0)
        self.assertEqual([e[0] for e in r.events], ["seam"])
        self.assertGreaterEqual(r.counters.exact_replaced, 1)
        self.assertLessEqual(abs(r.events[0][2][1] - pc), 1e-12)
        self.assertAlmostEqual(r.y[1], pc + 3.0 * (2.0 - pc), delta=1e-7)


class N2_NoRestart(unittest.TestCase):
    """N2: without h_restart the run takes more accepted steps after the landing (the kink case)."""

    def counts(self, src_patch=None):
        pc = 0.5

        def kink(x, y):
            return (0.0, 1.0 if y[1] < pc else 3.0, 0.0, 0.0, 0.0, 0.0)
        if src_patch is None:
            return run(kink, pc, h0=2.0, x1=2.0)[0].counters.accepted
        import inspect
        import textwrap
        src = textwrap.dedent(inspect.getsource(st.run))
        a = "            h = direction * min(abs(h_restart if h_restart is not None else h), opt.h_max)    # A1 impl note 9\n"
        self.assertIn(a, src)
        ns = dict(vars(st))
        exec(src.replace(a, "            h = direction * min(abs(h), opt.h_max)\n"), ns)
        with mock.patch.object(st, "run", ns["run"]):
            return run(kink, pc, h0=2.0, x1=2.0)[0].counters.accepted

    def test_restart_saves_steps(self):
        self.assertLess(self.counts(), self.counts(src_patch=True))


if __name__ == "__main__":
    unittest.main()
