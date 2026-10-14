# N1 반영 증명 — C1 직전 커밋에서 뜬 해시와 지금 풀이(solve_id 제외)가 같은지 한 번 확인하는 스크립트, 시험 묶음 밖 (prereg-t-eq-stellar N1, 68 L1)
"""Landing proof N1 of `rewrite/nodes/prereg-t-eq-stellar.frozen.md`: run once, output recorded in the landing note.

It lives outside solver/tests on purpose (audit 68, L1): the captured sha256s are whole-answer byte hashes taken on
the Mac, and a Linux PC round may differ at round-off (macOS libm vs glibc), which would fail the EVC physics gate.
N2 (registry and render, machine-independent) stays in solver/tests/test_node_additive.py.

    solver/.venv/bin/python -m unittest nodes.landing.n1_identity
"""
import json
import math
import unittest

from solver.tests.test_node_additive import CAPTURED, PARENT, _digest, _solve_plain  # noqa: F401  (PARENT documents the capture)


class N1Identity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plain = {n: _solve_plain(n) for n in CAPTURED}

    def test_solves_equal_parent_without_solve_id(self):
        for n, want in CAPTURED.items():
            self.assertEqual(_digest(self.plain[n]), want, n)

    def test_planted_one_ulp_fails(self):
        p = json.loads(json.dumps(self.plain["mars"]))
        q = p[0]["quantities"][0]
        q["point"] = math.nextafter(q["point"], math.inf)
        self.assertNotEqual(_digest(p), CAPTURED["mars"])

    def test_planted_solve_id_only_passes(self):
        p = json.loads(json.dumps(self.plain["mars"]))
        p[0]["quantities"][0]["provenance"]["solver"]["solve_id"] = "0" * 64
        self.assertEqual(_digest(p), CAPTURED["mars"])


if __name__ == "__main__":
    unittest.main()
