# 리뷰 수정 A5 시험 — 걸음 합이 순서·파이썬 판에 무관한지(fsum), 엔진 스위치 둘이 solve_id 에 들어가는지
"""Post-phase-1 review fix batch A5, b9's part (rewrite/p1review/fix-plan.md): G1-C-02 (the stepper's stage and error
sums are math.fsum, so Python 3.11's naive sum and 3.12's compensated sum agree) and G3-R-01 (NEARSTARS_REFERENCE_BUILD
and MANTLE_TABLE_DIR change material numbers without a file change; their state now enters material_bytes and so
solve_id). Each test fails on 99f35fff.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_p1fix_a5
"""
import importlib
import itertools
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from solver import legacy_materials as lm
from solver import stepper as st

# one component whose naive sum depends on the order: 1e16 + 1 − 1e16 is 0 left to right, 1 right to left
KS = [(1.0e16, 0.0), (1.0, 0.0), (-1.0e16, 0.0)]


class OrderFreeSums(unittest.TestCase):
    def test_axpy_is_the_same_in_every_order(self):
        w = (1.0, 1.0, 1.0)
        got = {st._axpy((0.0, 0.0), 1.0, [KS[i] for i in perm], [w[i] for i in perm])
               for perm in itertools.permutations(range(3))}
        self.assertEqual(got, {(1.0, 0.0)})

    def test_the_error_sum_is_correctly_rounded(self):
        """step()'s error sum, with the error weights planted (1, 1, −1, 0, …) so each product is exact: 1e16 + 1 − 1e16
        is 0 left to right and 1 correctly rounded."""
        ks = iter([(1.0,), (1.0e16,), (0.0,), (0.0,), (0.0,), (0.0,)])     # stages 2 … 7; stage 1 is 1e16
        with mock.patch.object(st, "_E", (1.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0)):
            _y, err, _k7 = st.step(lambda x, y: next(ks), 0.0, (0.0,), 1.0, (1.0e16,))
        self.assertEqual(err[0], 1.0)


class EngineSwitchesInTheId(unittest.TestCase):
    """G3-R-01: each switch's state moves material_bytes; the default state adds nothing; the table directory enters by
    content, not by path."""

    def test_reference_adiabat_off_moves_the_bytes(self):
        eos = importlib.import_module("eos")
        base = lm.material_bytes()
        with mock.patch.dict(eos.REFERENCE_ADIABAT, clear=True):
            off = lm.material_bytes()
        self.assertNotEqual(base, off)
        self.assertEqual(base, lm.material_bytes())

    def test_a_table_directory_enters_by_content(self):
        mc = importlib.import_module("mantle_composition")
        base = lm.material_bytes()
        src = Path(mc.HERE) / "mantle_tables"
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            for d in (a, b):
                for f in sorted(src.glob("*.json"))[:3]:
                    shutil.copy(f, d)
            with mock.patch.object(mc, "TABLE_DIR", Path(a)):
                in_a = lm.material_bytes()
            with mock.patch.object(mc, "TABLE_DIR", Path(b)):
                in_b = lm.material_bytes()
            first = sorted(Path(b).glob("*.json"))[0]
            first.write_bytes(first.read_bytes() + b" ")
            with mock.patch.object(mc, "TABLE_DIR", Path(b)):
                edited = lm.material_bytes()
        self.assertNotEqual(base, in_a)
        self.assertEqual(in_a, in_b)                  # same content, another path: the same id
        self.assertNotEqual(in_a, edited)

    def test_control_the_default_directory_adds_nothing(self):
        mc = importlib.import_module("mantle_composition")
        with mock.patch.object(mc, "TABLE_DIR", Path(mc.HERE) / "mantle_tables"):
            self.assertEqual(lm._switch_bytes(), b"")


if __name__ == "__main__":
    unittest.main()
