# 결과·천체 꼴 시험 — 유한성 · 띠 안의 점 · 띠 없는 까닭 · 측정 안 된 수치 띠 · 역할로 찾는 경계 (등록 c8 T-types · T-layers)
"""T-types and T-layers of rewrite/phase1-impl-c8.frozen.md, each with its negative control.

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_types
"""
import ast
import math
import unittest
from pathlib import Path
from unittest import mock

from solver import body as bd
from solver import result as rs

ROOT = Path(__file__).resolve().parents[2]


def _prov(grade="analog"):
    return rs.Provenance(grade=grade, solver=rs.SolverInfo(solve_id="0" * 64))


def _sources(solver_band=None):
    if solver_band is None:      # Q4 ②: the numerical band was not measured; the input corners compute the band
        return rs.Sources(input=rs.SourceBand(-0.1, 0.1, "input corners"), model=None, solver=None,
                          model_reason="phase 2", solver_not_measured=True)
    return rs.Sources(input=None, model=None, solver=solver_band, input_reason="no declared input band",
                      model_reason="phase 2")


def _q(point=1.0, band=None, band_reason="not yet computed", **kw):
    return rs.Quantity(key="x", unit="K", point=point, kind="exact", method="direct",
                       where=rs.Where("body"), provenance=_prov(), band=band, band_reason=band_reason, **kw)


def _band(lo, hi):
    return rs.Band(lo=lo, hi=hi, method="rtol/10 re-solve", sources=_sources(rs.SourceBand(lo - 1, hi - 1, "solver")))


class TQuantity(unittest.TestCase):
    def test_non_finite_point_raises(self):
        for bad in (math.nan, math.inf, -math.inf, "1.0", None, True):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                _q(point=bad)

    def test_non_finite_point_control(self):
        # control: with the finiteness check disabled, a NaN point is built
        with mock.patch.object(rs, "check_finite", lambda name, x: x):
            self.assertTrue(math.isnan(_q(point=math.nan).point))

    def test_point_outside_band_raises(self):
        with self.assertRaises(ValueError):
            _q(point=5.0, band=_band(0.0, 1.0), band_reason=None)
        self.assertEqual(_q(point=0.5, band=_band(0.0, 1.0), band_reason=None).point, 0.5)

    def test_null_band_needs_reason(self):
        with self.assertRaises(ValueError):
            _q(band=None, band_reason=None)
        with self.assertRaises(ValueError):
            _q(band=None, band_reason="")

    def test_band_checks(self):
        with self.assertRaises(ValueError):
            rs.Band(lo=2.0, hi=1.0, method="m", sources=_sources())
        with self.assertRaises(ValueError):
            rs.Band(lo=0.0, hi=1.0, method="m", sources=_sources(), basis="sigma")      # never σ (R-STEP0-11)
        with self.assertRaises(ValueError):
            rs.Band(lo=0.0, hi=1.0, method="", sources=_sources())
        with self.assertRaises(ValueError):
            rs.Band(lo=0.0, hi=math.nan, method="m", sources=_sources())

    def test_q4_option_2_not_measured(self):
        # post-freeze note 1: a direct solve's band without a solver source must carry the typed flag
        q = _q(point=1.0, band=rs.Band(lo=0.9, hi=1.1, method="input corners", sources=_sources()), band_reason=None)
        self.assertIsNone(q.band.sources.solver)
        self.assertTrue(q.band.sources.solver_not_measured)
        self.assertEqual(q.band.sources.solver_reason, "numerical band not measured")
        free = rs.Sources(input=rs.SourceBand(-0.1, 0.1, "input"), model=None, solver=None,
                          model_reason="phase 2", solver_reason="anything")
        with self.assertRaises(ValueError):                 # a direct solve with a free-text solver reason
            _q(point=1.0, band=rs.Band(lo=0.9, hi=1.1, method="input corners", sources=free), band_reason=None)
        with self.assertRaises(ValueError):                 # the registry string is the flag, not a free reason
            rs.Sources(input=None, model=None, solver=None, input_reason="a", model_reason="b",
                       solver_reason=rs.BAND_NOT_MEASURED)
        with self.assertRaises(ValueError):                 # a null source without a reason is refused
            rs.Sources(input=None, model=None, solver=None, input_reason="a", model_reason="b")
        # an interpolated value may carry another solver reason (the table's own band is elsewhere)
        rs.Quantity(key="x", unit="K", point=1.0, kind="exact", method="interpolated", where=rs.Where("body"),
                    provenance=_prov(), band=rs.Band(lo=0.9, hi=1.1, method="m", sources=free))

    def test_q4_control(self):
        # control: with the direct-band check disabled, the free-text reason gets through
        free = rs.Sources(input=rs.SourceBand(-0.1, 0.1, "input"), model=None, solver=None,
                          model_reason="phase 2", solver_reason="anything")
        with mock.patch.object(rs, "check_direct_band", lambda q: None):
            _q(point=1.0, band=rs.Band(lo=0.9, hi=1.1, method="m", sources=free), band_reason=None)

    def test_band_needs_a_computing_source(self):
        none = rs.Sources(input=None, model=None, solver=None, input_reason="a", model_reason="b", solver_reason="c")
        with self.assertRaises(ValueError):
            rs.Band(lo=0.0, hi=1.0, method="input corners", sources=none)

    def test_kind_method_where(self):
        with self.assertRaises(ValueError):
            rs.Quantity(key="x", unit="K", point=1.0, kind="approx", method="direct", where=rs.Where("body"),
                        provenance=_prov(), band_reason="r")
        with self.assertRaises(ValueError):
            rs.Quantity(key="x", unit="K", point=1.0, kind="exact", method="fitted", where=rs.Where("body"),
                        provenance=_prov(), band_reason="r")
        with self.assertRaises(ValueError):
            rs.Where("boundary", "core/mantle")              # a boundary needs its side (C153)
        with self.assertRaises(ValueError):
            rs.Where("layer", "mantle", "lower")
        rs.Where("boundary", "core/mantle", "equal_by_convention")

    def test_frozen(self):
        q = _q()
        with self.assertRaises(Exception):
            q.point = 2.0
        n = rs.Note(kind="k", text="t", fields={"a": 1, "l": [1, {"b": 2}]})
        with self.assertRaises(TypeError):
            n.fields["a"] = 2
        self.assertIsInstance(n.fields["l"], tuple)                  # deep: lists become tuples
        with self.assertRaises(TypeError):
            n.fields["l"][1]["b"] = 3
        q = _q(labels=[rs.Label("known_wrong", "shipped", "R-RUL-17", "r")])
        self.assertIsInstance(q.labels, tuple)
        a = rs.Answer(quantities=[_q()], profiles={"m": {"r": [1.0, 2]}})
        self.assertIsInstance(a.quantities, tuple)
        self.assertEqual(a.profiles["m"]["r"], (1.0, 2.0))
        with self.assertRaises(ValueError):
            rs.Answer(quantities=[_q()], profiles={"m": {"r": [1.0, math.nan]}})

    def test_numbers_normalised(self):
        self.assertEqual(rs.canonical(_q(point=-0.0)), rs.canonical(_q(point=0.0)))
        self.assertEqual(rs.canonical(_q(point=1)), rs.canonical(_q(point=1.0)))
        with self.assertRaises(ValueError):
            _q(point=10 ** 400)                                      # ValueError, not OverflowError

    def test_canonical_carries_non_finite_evidence(self):
        from solver import refusals as rf
        n = rf.no_answer("unconverged", "solve", budget_name="CLOSE_ITERS", budget_value=60, last_residual=math.nan)
        self.assertIn('"__float__":"nan"', rs.canonical(n))


class TAnswer(unittest.TestCase):
    def test_grade_is_worst(self):
        a = rs.Answer(quantities=(
            rs.Quantity(key="a", unit="K", point=1.0, kind="exact", method="direct", where=rs.Where("body"),
                        provenance=_prov("measured"), band_reason="r"),
            rs.Quantity(key="b", unit="K", point=1.0, kind="exact", method="direct", where=rs.Where("body"),
                        provenance=_prov("judgment"), band_reason="r")))
        self.assertEqual(a.grade, "judgment")
        self.assertEqual(rs.outcome_kind(a), "answer")

    def test_missing_must_be_typed(self):
        with self.assertRaises(ValueError):
            rs.Answer(quantities=(_q(),), missing=(("y", "cannot-say"),))    # W-L12-01: no strings in a slot

    def test_duplicate_quantity(self):
        with self.assertRaises(ValueError):
            rs.Answer(quantities=(_q(), _q()))

    def test_typed_slots(self):
        with self.assertRaises(ValueError):
            rs.Answer(quantities=(_q(),), notes=("free text",))
        with self.assertRaises(ValueError):
            rs.Answer(quantities=(_q(),), boundaries=(("cmb", 1.0),))
        with self.assertRaises(ValueError):
            rs.Span(0.0, 1.0, "refusal", reasons=("text",))

    def test_canonical_is_deterministic(self):
        a = rs.Answer(quantities=(_q(point=0.1),), notes=(rs.Note("k", "t", {"b": 2, "a": 1}),))
        self.assertEqual(rs.canonical(a), rs.canonical(a))
        self.assertIn('"point":0.1', rs.canonical(a))


class TGradeVocabulary(unittest.TestCase):
    def test_matches_engine_payload(self):
        # read engine/payload.py by AST (solver/ never imports engine/ outside the adapter)
        tree = ast.parse((ROOT / "engine" / "payload.py").read_text(encoding="utf-8"))
        got = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) \
                    and node.targets[0].id in ("GRADES", "GRADE_WORDS"):
                got[node.targets[0].id] = ast.literal_eval(node.value)
        self.assertEqual(got["GRADES"], rs.GRADES)
        self.assertEqual(got["GRADE_WORDS"], rs.GRADE_WORDS)


def _L(i, role, ext=None, **kw):
    return bd.Layer(id=i, role=role, material="m", extent=ext, **kw)


def _body(layers, closure=None, **kw):
    return bd.Body(name="t", kind="planet", surface=bd.SurfaceState(m=6e24, t_pot=1600.0), layers=tuple(layers),
                   closure=closure or bd.Closure(kind="R", lo=1e6, hi=1e8), **kw)


class TLayers(unittest.TestCase):
    def test_ten_layers(self):
        roles = ["core"] + ["mantle"] * 9
        layers = [_L(f"l{i}", r, bd.Extent("mass_fraction", 0.1)) for i, r in enumerate(roles)]
        b = _body(layers)
        self.assertEqual(len(b.boundaries), 9)
        self.assertEqual(b.interface("cmb").name, "l0/l1")
        self.assertIsNone(b.interface("icb"))

    def test_two_core(self):
        b = _body([_L("ic", "core.inner", bd.Extent("radius_from_centre", 1.22e6)),
                   _L("oc", "core.outer", bd.Extent("radius_from_centre", 3.48e6)),
                   _L("m", "mantle")])
        self.assertEqual(b.interface("icb").name, "ic/oc")
        self.assertEqual(b.interface("cmb").name, "oc/m")       # the CMB, not the ICB (W-L15-02)

    def test_order_rules(self):
        with self.assertRaises(ValueError):                      # core not at the centre
            _body([_L("m", "mantle", bd.Extent("mass_fraction", 0.7)), _L("c", "core")])
        with self.assertRaises(ValueError):                      # something after the envelope
            _body([_L("c", "core", bd.Extent("mass_fraction", 0.3)), _L("e", "envelope", bd.Extent("mass_fraction", 0.1)),
                   _L("m", "mantle")])
        with self.assertRaises(ValueError):                      # outer core below inner core
            _body([_L("oc", "core.outer", bd.Extent("mass_fraction", 0.2)), _L("ic", "core.inner", bd.Extent("mass_fraction", 0.1)),
                   _L("m", "mantle")])

    def test_order_control(self):
        # control: with no order rules, the mis-ordered body is accepted
        with mock.patch.object(bd, "order_violations", lambda layers: []):
            _body([_L("m", "mantle", bd.Extent("mass_fraction", 0.7)), _L("c", "core")])

    def test_one_remainder_and_unique_ids(self):
        with self.assertRaises(ValueError):
            _body([_L("c", "core"), _L("m", "mantle")])
        with self.assertRaises(ValueError):
            _body([_L("a", "core", bd.Extent("mass_fraction", 0.3)), _L("a", "mantle")])

    def test_unknown_role_and_jump(self):
        with self.assertRaises(ValueError):
            _L("x", "rock")
        with self.assertRaises(ValueError):
            _body([_L("c", "core", bd.Extent("mass_fraction", 0.3)), _L("m", "mantle")],
                  jumps={"c/x": bd.Declared(100.0, "K")})
        b = _body([_L("c", "core", bd.Extent("mass_fraction", 0.3)), _L("m", "mantle")],
                  jumps={"cmb": bd.Declared(100.0, "K")})
        self.assertIn("cmb", b.jumps)

    def test_closure_shapes(self):
        with self.assertRaises(ValueError):
            bd.Closure(kind="R", lo=2.0, hi=1.0)
        with self.assertRaises(ValueError):
            bd.Closure(kind="composition", lo=0.1, hi=0.2, layer="c")
        with self.assertRaises(ValueError):
            _body([_L("c", "core", bd.Extent("mass_fraction", 0.3)), _L("m", "mantle")],
                  closure=bd.Closure(kind="boundary_mass", lo=0.1, hi=0.5, layer="nope"))

    def test_no_layer_count_constant(self):
        hits = []
        for p in solver_sources():
            hits += [(p.name, *h) for h in layer_count_hits(p.read_text(encoding="utf-8"))]
        self.assertEqual(hits, [], "layer count or stack index used as a code constant (W-L15-01/-02)")

    def test_layer_count_planted_control(self):
        planted = ("if 3 == len(layers): pass\n"
                   "if 1 < len(body.layers) < 4: pass\n"
                   "if len(body.layers) in (2, 3): pass\n"
                   "N_LAYERS = 3\nif len(layers) == N_LAYERS: pass\n"
                   "x = layers[1]\n"
                   "y = body.layers[2]\n")
        self.assertEqual(len(layer_count_hits(planted)), 6)
        self.assertEqual(layer_count_hits("a = layers[0]\nb = layers[-1]\nn = len(layers)\nif len(roots) == 2: pass\n"), [])


def solver_sources() -> list:
    """Every solver source file, recursively, without tests and without dot-directories (the venv)."""
    base = ROOT / "solver"
    return [p for p in sorted(base.rglob("*.py"))
            if not any(part == "tests" or part.startswith(".") for part in p.relative_to(base).parts)]


def _is_len(node):
    """len() of a layers/stack name. An alias (`ls = body.layers; len(ls)`) is not followed: that needs data flow,
    and widening to every len() flags unrelated counts (roots, event history)."""
    return isinstance(node, ast.Call) and getattr(node.func, "id", None) == "len" \
        and any(_layers_name(a) for a in node.args)


def _const_like(node):
    """An integer literal > 1, an UPPER_CASE name, or a tuple/set/list of integer literals."""
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        return node.value > 1
    if isinstance(node, ast.Name) and node.id.isupper():
        return True
    if isinstance(node, (ast.Tuple, ast.Set, ast.List)):
        return any(_const_like(e) for e in node.elts)
    return False


def _layers_name(node):
    n = node.attr if isinstance(node, ast.Attribute) else getattr(node, "id", "")
    return n.endswith("layers") or n == "stack"


def layer_count_hits(source: str) -> list:
    """Comparisons of len(...) with a constant (either side, chained, membership), and integer stack indices other
    than 0 (centre) and -1 (surface) on a layers/stack name (r2 B3)."""
    hits = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Compare):
            sides = [node.left] + list(node.comparators)
            if any(_is_len(x) for x in sides) and any(_const_like(x) for x in sides):
                hits.append((node.lineno, "len() compared with a constant"))
        elif isinstance(node, ast.Subscript) and _layers_name(node.value):
            idx = node.slice
            val = idx.value if isinstance(idx, ast.Constant) else \
                (-idx.operand.value if isinstance(idx, ast.UnaryOp) and isinstance(idx.operand, ast.Constant) else None)
            if isinstance(val, int) and val not in (0, -1):
                hits.append((node.lineno, f"stack index {val}"))
    return hits

if __name__ == "__main__":
    unittest.main()
