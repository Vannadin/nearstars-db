# 리뷰 수정 A7 시험 — 옛 조회 기록이 꺼지면 읽기 검사가 «통과» 가 아니라 멈춤인지
"""Post-phase-1 review fix batch A7 (rewrite/p1review/fix-plan.md): G3-C-03. With the old lookup log off
(NEARSTARS_LOOKUP_LOG=0) the chain records no lookup, and check_reads returned [] even for a chain that serves a
structure key from the declared side. Now reads/check_reads raise LookupLogOff. Fails on 0bb04347.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p1fix_a7
"""
import unittest
from unittest import mock

from solver import legacy_view as lv
from solver.tests.test_legacy_view import _run


class LookupLogOff(unittest.TestCase):
    def test_log_off_stops_instead_of_passing(self):
        """Venus with its CMF served from the declared side, run and checked with the log off: a STOP, not []."""
        with mock.patch.object(lv.BodyState, "_LOG", False):
            _ans, bad = _run("venus", serve_cmf_from_declared=True)
            self.assertEqual(bad.body.lookups, [])
            with self.assertRaises(lv.LookupLogOff):
                lv.check_reads(bad)
            with self.assertRaises(lv.LookupLogOff):
                lv.reads(bad)

    def test_an_empty_log_stops_even_when_switched_on(self):
        """A log turned on only after the run is empty: still a STOP (the run itself recorded nothing)."""
        with mock.patch.object(lv.BodyState, "_LOG", False):
            _ans, bad = _run("venus", serve_cmf_from_declared=True)
        with self.assertRaises(lv.LookupLogOff):
            lv.check_reads(bad)

    def test_control_log_on_catches_the_declared_cmf(self):
        _ans, bad = _run("venus", serve_cmf_from_declared=True)
        self.assertIn("structure key served from the declared side", [v[2] for v in lv.check_reads(bad)])


if __name__ == "__main__":
    unittest.main()
