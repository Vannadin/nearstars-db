# Brent 잡음 멈춤 시험 — 매끄러운 굽은 F 는 끝까지 닫고, 잡음 낀 F 는 잡음 폭에서 멈추며, 폭 보호·곡률 감시·고장판 (stage-A prereg-k8-stop)
"""Stage-A registration prereg-k8-stop (frozen 3ea24b5d), §3 controls 1, 4 and 6, each with its mutant.

F(x) = A·tanh(c·(x − x*)) on a bracket of half-width w handed to Brent: its local slope at the root is A·c (set to
2.4e-7 /m, Earth's closure slope), the handed secant s0 = A·tanh(c·w)/w, so s_loc/s0 = c·w/tanh(c·w). Planted jitter
1e-8 is then about 4 cm in x, as on the «on» states. Run from the worktree root:
  solver/.venv/bin/python -m unittest solver.tests.test_noise_stop"""
import math
import random
import unittest

from solver import closure as cl

X0, W = 1.0e6, 1.0e3                       # root and half-width: the bracket is 2e-3·|x| wide (≥ 1e-6·|x|)


def _cw(ratio):
    """c·w with c·w/tanh(c·w) = ratio (bisection)."""
    lo, hi = 1e-6, 50.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mid / math.tanh(mid) < ratio:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


SLOPE = 2.4e-7


def _f(ratio, jitter=0.0, seed=7):
    c = _cw(ratio) / W
    amp = SLOPE / c
    rng = random.Random(seed)
    return lambda x: amp * math.tanh(c * (x - X0)) + (rng.uniform(-jitter, jitter) if jitter else 0.0)


def _close(F, a=X0 - W, b=X0 + W * 1.0001):
    log, trials = [], []
    root, prob, final = cl._brent(F, a, F(a), b, F(b), trials, noise_log=log)
    return root, prob, final, log


class Smooth(unittest.TestCase):
    def test_a_curved_smooth_f_closes_to_close_tol(self):
        """Control 1(a): s_loc/s0 = K/2 − 0.5 = 3.5; the rule never fires and Brent reaches CLOSE_TOL."""
        root, prob, final, log = _close(_f(cl.NOISE_STOP_K / 2 - 0.5))
        self.assertIsNone(prob)
        self.assertEqual(log, [])
        self.assertLessEqual(abs(final[2] - final[0]), 2 * (cl.CLOSE_TOL * abs(root) + 4.4e-16 * abs(root)))
        self.assertLess(abs(root - X0), 1e-9 * X0)

    def test_mutant_k_half_fires_on_the_smooth_f(self):
        saved = cl.NOISE_STOP_K
        cl.NOISE_STOP_K = 0.5
        try:
            _r, _p, _f2, log = _close(_f(cl.NOISE_STOP_K / 2 + 3.0))
        finally:
            cl.NOISE_STOP_K = saved
        self.assertTrue(log)


class Jitter(unittest.TestCase):
    def test_a_jittered_f_stops_at_its_noise(self):
        """Control 1(b): the 1(a) F (s_loc/s0 = 3.5) plus uniform 1e-8 jitter stops with |m| ≤ 2·σ_F/(K·s0)."""
        sigma = 1e-8
        F = _f(cl.NOISE_STOP_K / 2 - 0.5, jitter=sigma)
        a, b = X0 - W, X0 + W * 1.0001
        s0 = abs(F(b) - F(a)) / (b - a)
        root, prob, final, log = _close(F, a, b)
        self.assertIsNone(prob)
        self.assertEqual(len(log), 1)
        self.assertLessEqual(abs(log[0]["m"]), 2 * sigma / (cl.NOISE_STOP_K * s0))

    def test_a_noise_stop_on_an_ordinary_f_is_not_named(self):
        """Control 6, first half: a jitter stop where the local slope is ordinary (s_loc/s0 = 1.2) is not named.
        (1(a)'s own 3.5 sits on the watch's threshold, so the not-named half uses an ordinary F.)"""
        _r, _p, _f2, log = _close(_f(1.2, jitter=1e-8))
        self.assertEqual(len(log), 1)
        self.assertFalse(log[0]["named"], log[0])
        self.assertLess(log[0]["ratio"], 1.5)

    def test_a_firing_on_strong_curvature_is_named(self):
        """Control 6, second half: s_loc/s0 forced to 6; the firing (by the jitter) reads the noise-free local slope
        and is named. Mutant (s_loc from the final bracket's secant) names the ordinary stop above too."""
        _r, _p, _f2, log = _close(_f(6.0, jitter=1e-8))
        self.assertEqual(len(log), 1)
        self.assertTrue(log[0]["named"], log[0])
        self.assertGreaterEqual(log[0]["ratio"], 4.0)


class WidthGuard(unittest.TestCase):
    def test_a_hair_wide_bracket_runs_without_the_rule(self):
        """Control 4: a handed bracket narrower than 1e-6·|x| leaves s0 undefined: no noise stop, even in jitter."""
        F = _f(1.2, jitter=1e-8)
        root, prob, final, log = _close(F, X0 - 0.2, X0 + 0.2)            # 4e-7·|x| wide
        self.assertEqual(log, [])

    def test_mutant_without_the_guard_fires_at_once(self):
        saved = cl.NOISE_STOP_MIN_WIDTH
        cl.NOISE_STOP_MIN_WIDTH = 0.0
        try:
            _r, _p, _f2, log = _close(_f(1.2, jitter=1e-8), X0 - 0.2, X0 + 0.2)
        finally:
            cl.NOISE_STOP_MIN_WIDTH = saved
        self.assertTrue(log)


class Reach(unittest.TestCase):
    def test_solve_scalar_and_refine_carry_the_log(self):
        """The log reaches the outcomes (n3): solve_scalar's detail and refine's detail both carry noise_stops."""
        F = _f(1.2, jitter=1e-8)
        out = cl.solve_scalar(F, 0.5 * X0, 2.0 * X0)
        self.assertEqual(out.kind, "root")
        self.assertIn("noise_stops", out.detail)
        ref = cl.refine(F, out.roots[0], 0.5 * X0, 2.0 * X0)
        self.assertIsNotNone(ref)
        self.assertIn("noise_stops", ref.detail)


if __name__ == "__main__":
    unittest.main()
