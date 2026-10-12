# 속도 묶음 S2 시험 — 민감도 풀이의 출발점 (phase-1 design note 15 §2; §3·§4 는 15a·15b 로 빠짐)
"""Speed batch S2 on real bodies (phase-1 design post-freeze note 15 §2, as amended by 15a; items 3 and 4 were dropped by
notes 15a and 15b, so nothing here tests them). Each test fails on 9de992d4.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_s2
"""
import unittest
from unittest import mock

from solver import closure as cl, context, from_v1, solve as sv


def _earth():
    body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
    return body


def _sens_passes(refine_on: bool):
    """(sensitivity values, F2 passes) of one Earth solve, with refine on or forced to fall back."""
    calls = []
    real_inward, real_refine = sv.inward, cl.refine

    def inward(body, views, x, opt, **kw):
        if body.surface.t_pot != _earth().surface.t_pot:
            calls.append(x)
        return real_inward(body, views, x, opt, **kw)
    with mock.patch.object(sv, "inward", inward), \
            mock.patch.object(cl, "refine", real_refine if refine_on else (lambda *a, **k: None)):
        ans, _x = sv.solve(_earth(), context.Options())
    return {q.key: q.sensitivity for q in ans.quantities if q.sensitivity is not None}, len(calls)


class SensitivityRefine(unittest.TestCase):
    """Note 15 §2: the T_pot + δ solve starts from the root already found."""

    def test_fewer_passes_and_the_same_sensitivity_within_its_noise(self):
        on, n_on = _sens_passes(True)
        off, n_off = _sens_passes(False)
        self.assertLess(n_on, n_off)
        self.assertEqual(set(on), set(off))
        for k in on:
            self.assertLess(abs(on[k] - off[k]), 1e-4 * abs(off[k]) + 1e-12, k)   # note 15: ≤ 2.6e-5 measured


if __name__ == "__main__":
    unittest.main()
