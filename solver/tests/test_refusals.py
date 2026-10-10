# 거절 사전 시험 — 모르는 id · 빠지거나 덧붙은 근거 칸 · 칸만으로 문장 · 거절 문장 파싱 금지 검사 (등록 c8 T-registry)
"""T-registry of rewrite/phase1-impl-c8.frozen.md, each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_refusals
"""
import ast
import math
import string
import unittest
from unittest import mock

from solver import refusals as rf
from solver import result as rs
from solver.tests.test_types import solver_sources

SOLVE_IDS = ("solve.no_bracket", "solve.two_roots", "solve.material_domain", "solve.unlocated_discontinuity",
             "solve.event_chatter", "solve.layer_order", "solve.lid_unconverged", "solve.basal_unconverged",
             "solve.basal_not_attached", "solve.closure_discontinuous")
#: Names that hold reason text. X3: no consumer decides control flow from them.
TEXT_NAMES = ("text", "reason", "message_old", "why")
TEXT_KEYS = ("message_old", "why", "detail", "error", "rule")          # evidence fields that hold prose
CASE_METHODS = ("lower", "upper", "casefold", "strip", "lstrip", "rstrip")
X3_OK_MARKERS = 1             # pinned: result.py's construction guard; a new marker needs this number changed
STR_METHODS = ("startswith", "endswith", "find", "rfind", "index", "rindex", "split", "count", "__contains__",
               "partition", "rpartition")
RE_FUNCS = ("search", "match", "fullmatch", "findall", "finditer", "sub", "subn", "split")


def _texty(node) -> bool:
    """A reason-text expression: x.text / x.reason / x.message_old / *_reason, x.evidence["message_old"], str(x)."""
    if isinstance(node, ast.Attribute):
        return node.attr in TEXT_NAMES or node.attr.endswith("_reason")
    if isinstance(node, ast.Name):
        return node.id in TEXT_NAMES or node.id.endswith("_reason")
    if isinstance(node, ast.Subscript):
        key = node.slice.value if isinstance(node.slice, ast.Constant) else None
        return key in TEXT_KEYS or (_texty(node.value) and not isinstance(key, str))
    if isinstance(node, ast.Call):
        if getattr(node.func, "id", None) == "str":
            return True
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == "get" and node.args and isinstance(node.args[0], ast.Constant) \
                    and node.args[0].value in TEXT_KEYS:
                return True                                   # evidence.get("message_old")
            if node.func.attr in CASE_METHODS and _texty(node.func.value):
                return True                                   # r.text.lower()
    return False


def parse_hits(source: str) -> list:
    """X3 (r2 N5): reason text used under ==/!=/in, as a str-method receiver, or as a regex argument. A line marked
    «# x3-ok: <why>» is a construction guard on the type's own field, not control flow on a refusal, and is skipped."""
    lines = source.splitlines()
    hits = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Compare) and any(isinstance(op, (ast.In, ast.NotIn, ast.Eq, ast.NotEq))
                                                 for op in node.ops):
            if any(_texty(x) for x in [node.left] + list(node.comparators)):
                hits.append((node.lineno, "compare"))
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in STR_METHODS and _texty(node.func.value):
                hits.append((node.lineno, f".{node.func.attr}"))
            elif node.func.attr in RE_FUNCS and any(_texty(a) for a in node.args):
                hits.append((node.lineno, f"re.{node.func.attr}"))
    return [h for h in hits if "# x3-ok:" not in lines[h[0] - 1]]


def _evidence(entry):
    return {f: 0 for f in entry.fields}


def _solve_ev(**kw):
    ev = dict(x=None, closure_kind="R", pass_kind="scan", x_lo=1, x_hi=2, F_lo=1, F_hi=1, n_scan=8,
              walls=[], solved_regions=[])
    ev.update(kw)
    return ev


class TRegistry(unittest.TestCase):
    def test_b9_solve_ids_present(self):
        for i in SOLVE_IDS:
            self.assertIn(i, rf.REGISTRY)
            for f in rf.SOLVE_COMMON:
                self.assertIn(f, rf.REGISTRY[i].fields)
            for f in ("state", "scan"):
                self.assertIn(f, rf.REGISTRY[i].fields + rf.REGISTRY[i].optional)

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

    def test_check_control_on_a_non_templated_field(self):
        # `walls` is required on no_bracket but not read by its template: only the field check refuses its absence
        ev = _solve_ev()
        del ev["walls"]
        with self.assertRaises(ValueError):
            rf.make("solve.no_bracket", "solve", **ev)
        with mock.patch.object(rf, "_check_fields", lambda e, ev: None):          # control
            rf.make("solve.no_bracket", "solve", **ev)

    def test_b9_evidence_fields(self):
        # §A1.5: the scan rides on any solve.* refusal; a MAX_STEPS wall's NoAnswer carries its trial
        rf.make("solve.material_domain", "solve", x=1.0, closure_kind="R", pass_kind="wall", material_id="fe_prem",
                axis="P", bound=1e12, bound_kind="upper", source="s", message_old="m", scan=[[1.0, 0.1]])
        n = rf.no_answer("unconverged", "solve", budget_name="MAX_STEPS_SOLVE", budget_value=1e5,
                         last_residual=0.1, x=1.0, pass_kind="wall", state={"m": 1.0}, scan=[], m_at=0.5)
        self.assertEqual(n.evidence["pass_kind"], "wall")
        rf.make("solve.event_chatter", "solve", x=1.0, closure_kind="R", pass_kind="brent", event_name="solidus",
                count=9, cap_name="EVENT_REWALKS", cap_value=8, g=1e-11, tol=1e-12)
        for budget in ("CLOSE_ITERS", "MAX_STEPS_SOLVE", "WALL_SHOTS", "MAX_SPLITS"):
            rf.no_answer("unconverged", "solve", budget_name=budget, budget_value=1, last_residual=0.0)

    def test_vocabularies(self):
        with self.assertRaises(ValueError):
            rf.make("solve.no_bracket", "solve", **_solve_ev(pass_kind="guess"))
        with self.assertRaises(ValueError):
            rf.make("solve.no_bracket", "solve", **_solve_ev(closure_kind="radius"))
        with self.assertRaises(ValueError):
            rf.no_answer("unconverged", "solve", budget_name="T_PASSES", budget_value=8, last_residual=1e-3)
        with self.assertRaises(ValueError):
            rf.make("solve.event_chatter", "solve", x=1.0, closure_kind="R", pass_kind="brent", event_name="e",
                    count=9, cap_name="EVENT_FOREVER", cap_value=8)
        rf.make("solve.no_bracket", "solve", **_solve_ev())

    def test_wall_records(self):
        good = {"x": 1.0, "outcome_kind": "no_answer", "id_or_reason": "unconverged", "state": {}, "located": False}
        rf.make("solve.no_bracket", "solve", **_solve_ev(walls=[good]))
        for bad in ({**good, "located": "no"}, {**good, "outcome_kind": "crash"}, {k: v for k, v in good.items()
                                                                                 if k != "located"}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                rf.make("solve.no_bracket", "solve", **_solve_ev(walls=[bad]))

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

    def test_evidence_frozen_and_typed_at(self):
        r = rf.make("solve.no_bracket", "solve", at=rs.Where("layer", "core"), **_solve_ev(walls=[]))
        self.assertIsInstance(r.evidence["walls"], tuple)
        self.assertEqual(r.at.id, "core")
        n = rf.no_answer("unconverged", "solve", budget_name="CLOSE_ITERS", budget_value=1, last_residual=math.inf)
        self.assertIn("inf", rs.canonical(n))


class TNoReasonParsing(unittest.TestCase):
    def test_solver_has_no_reason_parsing(self):
        hits = []
        for p in solver_sources():
            hits += [(p.name, *h) for h in parse_hits(p.read_text(encoding="utf-8"))]
        self.assertEqual(hits, [], "X3: control flow must read Refusal.id / evidence, not text")

    def test_planted_control(self):
        planted = '\n'.join([
            'if r.text.startswith("표면온도"): pass',
            'ok = "답 둘" in result.reason',
            'm = re.search("x", why.text)',
            'any(h in r.text for h in HEADS)',
            'if r.text == "답 둘": pass',
            'PAT.search(r.text)',
            'str(r).find("x")',
            'r.evidence["message_old"].startswith("x")',
            'x = (\n  r.reason\n  .startswith("y"))',
            'if solver_reason == BAND_NOT_MEASURED: pass',
            'if self.solver_reason == X: pass  # x3-ok: construction guard',
            'r.evidence.get("message_old").startswith("x")',
            'if r.evidence["detail"] == "y": pass',
            'r.text.lower().startswith("z")',
        ])
        self.assertEqual(len(parse_hits(planted)), 13)

    def test_x3_ok_markers_pinned(self):
        n = sum(p.read_text(encoding="utf-8").count("# x3-ok:") for p in solver_sources())
        self.assertEqual(n, X3_OK_MARKERS, "a new x3-ok marker must be reviewed and pinned here")
        self.assertEqual(parse_hits('if r.id == "solve.no_bracket": pass\nn = len(r.evidence)\n'), [])


if __name__ == "__main__":
    unittest.main()
