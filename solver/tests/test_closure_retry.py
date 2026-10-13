# 닫힘 재시도 시험 (설계 노트 18 초안) — 잔차 검사에 걸린 근을 rtol/10 으로 한 번 다시 닫고, 그래도 걸리면 거절하는지
"""Phase-1 design note 18 (draft): the accepted root failing note 8's residual check is re-closed once at rtol/10.
Planted on ClosureDiscontinuous's forward (R) two-layer body: a step in F just below the root, either at rtol 1e-10
only (noise that a tighter pass removes) or at every rtol (a real jump)."""
import math
import unittest

from solver import closure as cl
from solver import context, result, solve as sv
from solver import stepper as st
from solver.tests import test_solve                         # its TestCase is not bound here, so it is not rerun


class ClosureRetry(unittest.TestCase):
    _bodies = test_solve.ClosureDiscontinuous._bodies                  # the fixtures only, not ClosureDiscontinuous's tests
    _slope = test_solve.ClosureDiscontinuous._slope
    _slope_sign = test_solve.ClosureDiscontinuous._slope_sign

    def _solve_with(self, body, views, x_step, jump, only_rtol=None):
        """F + jump past x_step, on passes at `only_rtol` (all passes if None); counts the closures run."""
        orig, orig_scalar, closures = sv.inward, cl.solve_scalar, []

        def stepped(bd, vw, x, opt, **kw):
            got = orig(bd, vw, x, opt, **kw)
            if (not isinstance(got, st.Stop) and got.F is not None and x > x_step
                    and (only_rtol is None or opt.rtol == only_rtol)):
                got.F += jump
            return got

        def counted(*a, **k):
            closures.append(1)
            return orig_scalar(*a, **k)
        sv.inward, cl.solve_scalar = stepped, counted
        try:
            return sv.solve(body, views=views), len(closures)
        finally:
            sv.inward, cl.solve_scalar = orig, orig_scalar

    def test_noise_at_rtol_is_retried_and_answers(self):
        """A step only at the solve's rtol (1e-10): the first closure refuses on the residual, the retry at rtol/10
        answers, the Answer carries Note closure_retried with the first attempt, and the solve_id is the request's."""
        (fwd, views, r0), _inv = self._bodies()
        plain, _x = sv.solve(fwd, views=views)
        sg = self._slope_sign(fwd, views, r0)
        (got, x), n = self._solve_with(fwd, views, r0 * (1 - 1e-7), sg * 1e-5, only_rtol=context.Options().rtol)
        self.assertIsInstance(got, result.Answer, getattr(got, "text", None))
        self.assertEqual(n, 2)                                   # the first closure, then the single retry
        note = next(n_ for n_ in got.notes if n_.kind == "closure_retried")
        first = note.fields["first_attempt"]
        self.assertEqual(first["rtol"], context.Options().rtol)
        self.assertGreater(abs(first["F_root"]), first["tol_F"])
        self.assertEqual(note.fields["rtol"], context.Options().rtol / sv.CLOSURE_RETRY_RTOL_DIV)
        self.assertLessEqual(abs(note.fields["F_root"]), note.fields["tol_F"])
        self.assertLess(abs(x / r0 - 1.0), 1e-9)
        sid = lambda a: {q.provenance.solver.solve_id for q in a.quantities}
        self.assertEqual(sid(got), sid(plain))                    # the request's options, not rtol/10
        self.assertEqual(len(sid(got)), 1)

    def test_a_real_jump_refuses_after_one_retry(self):
        """A step at every rtol: the retry fails the same check and the refusal names the first attempt."""
        (fwd, views, r0), _inv = self._bodies()
        sg = self._slope_sign(fwd, views, r0)
        (got, _x), n = self._solve_with(fwd, views, r0 * (1 - 1e-7), sg * 1e-5)
        self.assertIsInstance(got, result.Refusal)
        self.assertEqual(got.id, "solve.closure_discontinuous")
        self.assertEqual(n, 2)                                   # one retry, never a second
        self.assertEqual(got.evidence["rtol"], context.Options().rtol / sv.CLOSURE_RETRY_RTOL_DIV)
        first = got.evidence["first_attempt"]
        self.assertEqual(first["rtol"], context.Options().rtol)
        self.assertGreater(abs(first["F_root"]), first["tol_F"])

    def test_a_clean_root_runs_one_closure_and_no_note(self):
        (fwd, views, r0), _inv = self._bodies()
        (got, x), n = self._solve_with(fwd, views, math.inf, 0.0)
        self.assertIsInstance(got, result.Answer, getattr(got, "text", None))
        self.assertEqual(n, 1)
        self.assertNotIn("closure_retried", [n_.kind for n_ in got.notes])


if __name__ == "__main__":
    unittest.main()
