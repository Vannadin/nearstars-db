# A6 결정성 가드 — 지구 6점 훑기를 풀 1·풀 3 과 두 작업 순서로 돌려 Answer 가 바이트까지 같은지 본다 (phase1-design §T A6 둘째)
"""phase1-design.frozen.md §T, A6 guard 2 (exact, R-RUL-13 (a)): two solves give identical Answers; a 6-point Earth
sweep at pool 1 and pool 3, in two job orders, is byte-identical (W-L9-05). All four (pool, order) runs are compared
on the whole (Answer, warm) in the project's canonical bytes (`result.canonical`: sorted keys, floats by repr, §A6),
not only its quantities. (An Answer holds read-only mappings, which pickle refuses.)

Planted control, from the same runs: each worker also reports how many jobs it had run before this one (a
worker-local counter, the module state §A6 forbids). At pool 1 it depends on the job order, so the same comparison
must see the forward and reversed runs differ on it; if it did not, the comparison could not see state that leaks
across jobs. (At pool 3 the count also depends on which worker the scheduler hands a job, so it is not asserted.)

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_a6_determinism
"""
import concurrent.futures as cf
import dataclasses
import multiprocessing as mp
import unittest

POINTS = (1600.0, 1650.0, 1700.0, 1750.0, 1800.0, 1850.0)
_SEEN = [0]                        # the planted worker-local state (test code only; solver/ is scanned by test_a6_state)


def _job(t_pot):
    from solver import from_v1, result, solve as sv
    e, _aside = from_v1.load_v1("engine/bodies/earth.yaml")
    body = dataclasses.replace(e, surface=dataclasses.replace(e.surface, t_pot=t_pot))
    ans, warm = sv.solve(body)
    before = _SEEN[0]
    _SEEN[0] += 1
    return t_pot, result.canonical((ans, warm)).encode(), before


def _run(pool, order):
    with cf.ProcessPoolExecutor(pool, mp_context=mp.get_context("spawn")) as ex:
        got = list(ex.map(_job, order))
    return {t: b for t, b, _n in got}, {t: n for t, _b, n in got}


class PoolAndOrder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fwd, rev = POINTS, tuple(reversed(POINTS))
        cls.runs = {(p, o): _run(p, seq) for p in (1, 3) for o, seq in (("forward", fwd), ("reversed", rev))}

    def test_byte_identical_across_pool_and_order(self):
        ref = self.runs[(1, "forward")][0]
        self.assertEqual(sorted(ref), sorted(POINTS))
        for k, (answers, _n) in self.runs.items():
            with self.subTest(run=k):
                self.assertEqual(answers, ref)

    def test_points_differ(self):
        """Control: the six answers are not one answer repeated."""
        self.assertEqual(len(set(self.runs[(1, "forward")][0].values())), len(POINTS))

    def test_planted_worker_state_is_seen(self):
        """Control: worker-local state that leaks across jobs differs between the runs, and the comparison sees it."""
        seen = {k: n for k, (_a, n) in self.runs.items()}
        self.assertNotEqual(seen[(1, "forward")], seen[(1, "reversed")])


if __name__ == "__main__":
    unittest.main()
