# 적분법 항 드라이버 시험 — 상대차 d 의 규칙(0 기준 · 결과 종류 다름 제외)과 (천체, 키) 항 집계
"""solver.method_term's rules (rewrite/oracle/t2-method-term-registration.md «Rule»), on synthetic records."""
import json
import tempfile
import unittest
from pathlib import Path

from solver import method_term as mt


class Diff(unittest.TestCase):
    def test_relative_and_zero_reference(self):
        d, flags = mt._diff({"a": 2.0, "z": 0.0, "zz": 0.0, "s": "solid"}, {"a": 2.002, "z": 1.0, "zz": 0.0, "s": "x"})
        self.assertAlmostEqual(d["a"], 1e-3)
        self.assertIsNone(d["z"])
        self.assertEqual(flags, {"z": "zero_reference"})          # control: 0 → 0 is no flag
        self.assertNotIn("s", d)


class Terms(unittest.TestCase):
    def test_max_abs_over_included_states(self):
        rows = [{"body": "b", "state": "declared", "d": {"k": 1e-4}, "flags": {}},
                {"body": "b", "state": 1500.0, "d": {"k": -3e-4}, "flags": {}},
                {"body": "b", "state": 1600.0, "flag": "outcome_differs"}]   # control: excluded, listed
        p = Path(tempfile.mkdtemp(), "t.jsonl")
        p.write_text("".join(json.dumps(r) + "\n" for r in rows))
        t = mt.terms([str(p)])
        self.assertEqual(t["terms"]["b"]["k"], {"term": 3e-4, "count": 2, "at": 1500.0})
        self.assertEqual(t["flagged"], [["b", 1600.0, "outcome_differs"]])


if __name__ == "__main__":
    unittest.main()
