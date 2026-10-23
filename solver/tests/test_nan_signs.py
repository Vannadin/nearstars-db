# solver 쪽 NaN 규칙 시험 — 부호 검사가 NaN 을 부호로 안 받고, 이분이 NaN 끝으로 수렴하지 않으며, 유한한 근은 비트까지 그대로인지 (유한↔NaN 경계 심기)
"""The NaN rule in solver (artifacts ea-jobA pc/ea-f13b/nanbisect/plan.md; 68 pc/audit68-nanbisect 4911b80e): planted
functions, finite on one side and NaN past an edge that is no root. The old rule converged onto the edge (the inline
mutant shows it); the fixed bisection refuses, and a finite root is unchanged bit for bit.

Run from the worktree root:  <solver venv>/python -m unittest solver.tests.test_nan_signs
"""
import unittest

from solver import rho_fall_build as rfb, signs as sg

NAN = float("nan")


def _old_bisect(f, a, b, fa, n=60):
    for _ in range(n):
        m = 0.5 * (a + b)
        fm = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return 0.5 * (a + b)


def _hole(x):
    return -1.0 if x < 0.2 else (NAN if x < 0.7 else 1.0)


class NaNSigns(unittest.TestCase):
    def test_nan_free(self):
        self.assertTrue(sg.nan_free(1.0, -1.0, 0.0))
        self.assertFalse(sg.nan_free(1.0, NAN))

    def test_bisect_refuses_a_nan_band(self):
        old = _old_bisect(_hole, 0.0, 1.0, -1.0)
        self.assertLess(min(abs(old - 0.2), abs(old - 0.7)), 1e-9)      # the mutant lands on a NaN edge
        self.assertIsNone(rfb._bisect(_hole, 0.0, 1.0, -1.0))

    def test_finite_root_bit_identical(self):
        f = lambda x: x * x - 0.3                                       # noqa: E731
        self.assertEqual(rfb._bisect(f, 0.0, 1.0, -0.3), _old_bisect(f, 0.0, 1.0, -0.3))


if __name__ == "__main__":
    unittest.main()
