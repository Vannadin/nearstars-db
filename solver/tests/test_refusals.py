# 거절 사전 시험 — 모르는 id · 빠지거나 덧붙은 근거 칸 · 칸만으로 문장 · 거절 문장 파싱 금지 검사 (등록 c8 T-registry)
"""T-registry of rewrite/phase1-impl-c8.frozen.md, each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_refusals
"""
import re
import string
import unittest
from pathlib import Path

from solver import refusals as rf
from solver import result as rs

ROOT = Path(__file__).resolve().parents[2]
SOLVE_IDS = ("solve.no_bracket", "solve.two_roots", "solve.material_domain", "solve.unlocated_discontinuity",
             "solve.event_chatter", "solve.layer_order", "solve.lid_unconverged", "solve.basal_unconverged",
             "solve.basal_not_attached")

#: X3: no consumer decides control flow from a reason string. These forms are what the old engine did
#: (`startswith(TIGHT_REFUSAL_HEADS)`, `"…" in r.reason`, regex over a reason).
PARSE_PATTERNS = (
    re.compile(r"\.(text|reason)\s*\.\s*(startswith|endswith|find|index|split)\s*\("),
    re.compile(r"""["'][^"']*["']\s+(not\s+)?in\s+[\w.]*\.(text|reason)\b"""),
    re.compile(r"\bre\.\w+\([^)]*\.(text|reason)\b"),
)


def parse_hits(source: str) -> list:
    return [(i, line.strip()) for i, line in enumerate(source.splitlines(), 1)
            if any(p.search(line) for p in PARSE_PATTERNS)]


def _evidence(entry):
    return {f: 0 for f in entry.fields}


class TRegistry(unittest.TestCase):
    def test_b9_solve_ids_present(self):
        for i in SOLVE_IDS:
            self.assertIn(i, rf.REGISTRY)
            for f in rf.SOLVE_COMMON:
                self.assertIn(f, rf.REGISTRY[i].fields)
            self.assertIn("state", rf.REGISTRY[i].optional)

    def test_unknown_id(self):
        with self.assertRaises(ValueError):
            rf.make("solve.no_such", "x")

    def test_missing_and_undeclared_fields(self):
        e = rf.REGISTRY["input.unknown_key"]
        with self.assertRaises(ValueError):
            rf.make(e.id, "f.yaml", key="potental_temperature")                       # nearest missing
        with self.assertRaises(ValueError):
            rf.make(e.id, "f.yaml", key="k", nearest="n", extra=1)                     # undeclared
        r = rf.make(e.id, "f.yaml", key="potental_temperature", nearest="potential_temperature")
        self.assertIsInstance(r, rs.Refusal)
        self.assertEqual(r.id, "input.unknown_key")
        self.assertEqual(rs.outcome_kind(r), "refusal")

    def test_check_control(self):
        # control: with the field check disabled, an undeclared field gets through
        saved = rf._check_fields
        rf._check_fields = lambda e, ev: None
        try:
            rf.make("input.unknown_key", "f.yaml", key="k", nearest="n", extra=1)
        finally:
            rf._check_fields = saved

    def test_pass_kind_and_budget(self):
        ev = dict(x=None, closure_kind="R", pass_kind="guess", x_lo=1, x_hi=2, F_lo=1, F_hi=1, n_scan=8,
                  walls=[], solved_regions=[])
        with self.assertRaises(ValueError):
            rf.make("solve.no_bracket", "solve", **ev)
        ev["pass_kind"] = "scan"
        rf.make("solve.no_bracket", "solve", **ev)
        with self.assertRaises(ValueError):
            rf.no_answer("unconverged", "solve", budget_name="T_PASSES", budget_value=8, last_residual=1e-3)
        n = rf.no_answer("unconverged", "solve", budget_name="CLOSE_ITERS", budget_value=60, last_residual=1e-3)
        self.assertEqual(rs.outcome_kind(n), "no_answer")

    def test_every_template_renders_from_its_fields_alone(self):
        for reg in (rf.REGISTRY, rf.NO_ANSWER_REGISTRY):
            for e in reg.values():
                with self.subTest(id=e.id):
                    names = {f for _, f, _, _ in string.Formatter().parse(e.template) if f}
                    self.assertLessEqual(names, set(e.fields) | {"where"}, f"{e.id} template reads undeclared fields")
                    rf.render(e, "w", _evidence(e))

    def test_ids_unique(self):
        with self.assertRaises(ValueError):
            rf._index((rf.Entry("a", (), "t"), rf.Entry("a", (), "t")))


class TNoReasonParsing(unittest.TestCase):
    def test_solver_has_no_reason_parsing(self):
        hits = []
        for p in sorted((ROOT / "solver").glob("*.py")):
            hits += [(p.name, *h) for h in parse_hits(p.read_text(encoding="utf-8"))]
        self.assertEqual(hits, [], "X3: control flow must read Refusal.id / evidence, not text")

    def test_planted_control(self):
        planted = ('if r.text.startswith("표면온도"):\n    pass\n'
                   'ok = "답 둘" in result.reason\n'
                   'm = re.search("x", why.text)\n')
        self.assertEqual(len(parse_hits(planted)), 3)


if __name__ == "__main__":
    unittest.main()
