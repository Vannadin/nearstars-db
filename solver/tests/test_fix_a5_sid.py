# 사후 검토 수정 A5 (c8 몫) 시험 — solve_id 는 솔버가 읽는 값만 묶는다: 출처 문장 · 나이 · int/float 표기는 id 를 안 바꾸고 값은 바꾼다
"""P1R-G4-SP-01 with LOWs G4-C-15 and G4-R-11. Fails at engine/rewrite-p2 3fd0e147 (solve_id hashed repr(body)).

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_fix_a5_sid
"""
import copy
import unittest

from solver import context
from solver import solve as sv
from solver import validate as vd
from solver.tests.test_validate import BASE


def sid(raw):
    body = vd.validate(raw)
    return context.solve_id_of(sv._canonical(body), b"", context.Options())


def doc(**inputs):
    d = copy.deepcopy(BASE)
    d["inputs"].update(inputs)
    return d


RADIUS = {"value": 1.0, "grade": "measured", "source": "IAU 2015 Resolution B3", "counter_evidence_searched": "c"}


class SolveIdBindsWhatTheSolveReads(unittest.TestCase):
    def test_source_sentence_keeps_the_id(self):
        a = sid(doc(radius_earth=RADIUS))
        b = sid(doc(radius_earth={**RADIUS, "source": "IAU 2015 B3, nominal equatorial radius"}))
        self.assertEqual(a, b)

    def test_unread_field_keeps_the_id(self):
        self.assertEqual(sid(doc(age_gyr=4.5)), sid(doc(age_gyr=4.6)))

    def test_int_or_float_spelling_keeps_the_id(self):
        self.assertEqual(sid(doc(mass_earth=1)), sid(doc(mass_earth=1.0)))

    def test_control_a_read_value_moves_the_id(self):
        self.assertNotEqual(sid(doc(mass_earth=1.0)), sid(doc(mass_earth=1.01)))
        self.assertNotEqual(sid(doc(radius_earth=RADIUS)), sid(doc(radius_earth={**RADIUS, "value": 1.001})))


if __name__ == "__main__":
    unittest.main()
