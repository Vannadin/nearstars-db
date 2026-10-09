# A6 흔적 분리 가드 — Answer 출처의 계수가 받아들인 사격의 계수와 같고, 시행 계수가 새면 잡히는지 본다 (phase1-design §T A6 셋째)
"""phase1-design.frozen.md §T, A6 guard 3: the provenance counters of an Answer equal the accepted pass's counters; a
planted trial counter leaking into provenance fails.

Every `solve.inward` call of one Earth solve is recorded (its counters copied at return). With the sensitivity
passes off, the last call is the accepted pass (solve.py records it as «accepted» after the closure's trials). The
provenance counters of every quantity must equal that pass's own counters, apart from `surface_rho0_fallbacks`,
which solve adds from the views after the pass (reset before it, M1) and is not a pass counter.

Planted leak: a wrapper hands every pass one shared counter dict, so the trials' counts pile into the accepted
pass's. Each pass's own counters are recorded before the sharing, so the same check must fail on it.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_a6_trace
"""
import unittest
from unittest import mock

from solver import context, from_v1, result, solve as sv

ADDED_AFTER = "surface_rho0_fallbacks"


def _solve_recording(leak: bool):
    """(answer, [counters of each inward call, in order]) for Earth at its declared state, sensitivity off."""
    real = sv.inward
    calls, shared = [], {}

    def wrapped(body, views, x, opt):
        out = real(body, views, x, opt)
        if not isinstance(out, sv.st.Stop):
            calls.append(dict(out.counters))           # the pass's own counters
            if leak:                                   # planted: one counter dict for every pass
                for k, v in out.counters.items():
                    shared[k] = shared.get(k, 0) + v
                out.counters = shared
        return out

    body, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
    with mock.patch.object(sv, "inward", wrapped):
        ans, _x = sv.solve(body, context.Options(sensitivity_dt=0.0))
    return ans, calls


def separated(ans, calls) -> bool:
    """The guard: every quantity's provenance counters equal the last (accepted) pass's, bar the key added after."""
    acc = {k: v for k, v in calls[-1].items() if k != ADDED_AFTER}
    for q in ans.quantities:
        prov = {k: v for k, v in q.provenance.solver.counters if k != ADDED_AFTER}
        if prov != acc:
            return False
    return True


class TraceSeparation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ans, cls.calls = _solve_recording(leak=False)
        cls.leak_ans, cls.leak_calls = _solve_recording(leak=True)

    def test_answer(self):
        self.assertIsInstance(self.ans, result.Answer, getattr(self.ans, "text", None))
        self.assertGreater(len(self.calls), 1)                              # trials, then the accepted pass

    def test_provenance_is_the_accepted_pass(self):
        self.assertTrue(separated(self.ans, self.calls))

    def test_trials_would_differ(self):
        """Control: the trials' summed counters are not the accepted pass's, so a leak would show."""
        total = {}
        for c in self.calls:
            for k, v in c.items():
                total[k] = total.get(k, 0) + v
        acc = self.calls[-1]
        self.assertNotEqual({k: v for k, v in total.items() if k != ADDED_AFTER},
                            {k: v for k, v in acc.items() if k != ADDED_AFTER})

    def test_planted_leak_fails(self):
        self.assertIsInstance(self.leak_ans, result.Answer)
        self.assertEqual(self.leak_calls, self.calls)                       # the same passes ran
        self.assertFalse(separated(self.leak_ans, self.leak_calls))


if __name__ == "__main__":
    unittest.main()
