# 출하 데이터 건너뜀 검사 시험 — «shipped» 를 이유로 건너뛰는 모든 skipUnless·skipTest 조건이 기록이 실린 TIP 에서 참인지
"""A guard that skips a test when the shipped data is absent must not skip at a tip that ships it (directing 10-18: a
«*.json» glob against tables shipped as «*.json.gz» skipped test_planted_coverage_real at every tip, and the EVC physics
gate, which fails on any skip, caught it on the PC).

Every guard in solver/tests whose reason names shipped data — a «@unittest.skipUnless(cond, "… shipped …")» decorator,
or «if not cond: self.skipTest("… shipped …")» — is found by reading the test sources, and its condition is evaluated in
its own module. A NEARSTARS_HEAVY operand of an «and» is dropped (that half is the environment's, not the data's). When
this tip ships the SLB records, every such condition must be true."""
import ast
import importlib
import unittest
from pathlib import Path

from solver import material_registry as mr

TESTS = Path(__file__).resolve().parent
RECORDS = sorted(mr.MATERIALS_DIR.glob("silicate_slb_*.yaml"))          # the anchor: the record files, not a table glob


def _is_heavy(node):
    src = ast.unparse(node)
    return src == "HEAVY" or "NEARSTARS_HEAVY" in src


def _data_part(cond):
    """The condition without its NEARSTARS_HEAVY operands (None if nothing else is left)."""
    if isinstance(cond, ast.BoolOp) and isinstance(cond.op, ast.And):
        rest = [v for v in cond.values if not _is_heavy(v)]
        if not rest:
            return None
        return rest[0] if len(rest) == 1 else ast.BoolOp(op=ast.And(), values=rest)
    return None if _is_heavy(cond) else cond


def _reason(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else ""


def guards():
    """[(module, line, condition source, reason)] for every shipped-data guard in solver/tests."""
    out = []
    for path in sorted(TESTS.glob("test_*.py")):
        tree = ast.parse(path.read_text())
        mod = f"solver.tests.{path.stem}"
        for node in ast.walk(tree):
            if (isinstance(node, ast.Call) and ast.unparse(node.func) in ("unittest.skipUnless", "skipUnless")
                    and len(node.args) == 2 and "shipped" in _reason(node.args[1])):
                cond = _data_part(node.args[0])
                if cond is not None:
                    out.append((mod, node.lineno, ast.unparse(cond), _reason(node.args[1])))
            if isinstance(node, ast.If) and isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not):
                for st in node.body:
                    call = st.value if isinstance(st, ast.Expr) else None
                    if (isinstance(call, ast.Call) and ast.unparse(call.func).endswith("skipTest") and call.args
                            and "shipped" in _reason(call.args[0])):
                        out.append((mod, node.lineno, ast.unparse(node.test.operand), _reason(call.args[0])))
    return out


class ShippedGuards(unittest.TestCase):
    def test_the_scan_finds_the_guards(self):
        """Control: the scan sees the known guards (the glob fixed 10-18 and the module-level _shipped helpers), so an
        empty scan cannot pass for «every guard true»."""
        found = guards()
        mods = {m for m, *_ in found}
        self.assertGreaterEqual(len(found), 12)
        for m in ("solver.tests.test_material_assemblage", "solver.tests.test_assemblage_c1",
                  "solver.tests.test_assemblage_boundaries", "solver.tests.test_read_determinism",
                  "solver.tests.test_switchover", "solver.tests.test_closure"):
            self.assertIn(m, mods)

    @unittest.skipUnless(RECORDS, "no SLB record yaml at this tip (an engine branch without records)")
    def test_every_shipped_guard_is_true_at_a_tip_that_ships(self):
        """At a tip that ships the SLB records (their yaml), no shipped-data guard may skip: each condition is true in
        its own module."""
        for mod, line, cond, why in guards():
            with self.subTest(guard=f"{mod}:{line}", cond=cond):
                ns = vars(importlib.import_module(mod))
                self.assertTrue(eval(compile(cond, f"{mod}:{line}", "eval"), ns), f"{cond!r} is false: «{why}»")

    def test_a_wrong_glob_is_caught(self):
        """Control: the old guard, a «*.json» glob against the gzipped tables, evaluates false here."""
        self.assertFalse(sorted((mr.MATERIALS_DIR / "tables").glob("silicate_slb_*.json")))


if __name__ == "__main__":
    unittest.main()
