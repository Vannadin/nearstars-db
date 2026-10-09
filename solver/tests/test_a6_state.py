# A6 상태 가드 — solver/ 에 고칠 수 있는 모듈 수준 객체와 global 이 없는지 AST 로 훑는다 (phase1-design §T A6 첫째)
"""phase1-design.frozen.md §T, A6 guard 1: an AST scan of `solver/` finds no mutable module-level assignment and no
`global`; a planted one fails. §A6: «There are no mutable module-level objects, no `global`, no id()-keyed side
tables (A10)». The scan reads every `solver/**/*.py` except the tests and dot-directories (the venv).

Run from the worktree root:  solver/.venv/bin/python -m unittest solver.tests.test_a6_state
"""
import ast
import dataclasses
import importlib
import pathlib
import types
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

#: Calls that build a mutable container.
MUTABLE_CALLS = {"list", "dict", "set", "bytearray", "defaultdict", "OrderedDict", "Counter", "deque", "ChainMap",
                 "sorted"}

#: Findings that are known and owned, each removed by its owner's commit. An entry that no longer fires fails the
#: test (stale), so the list only shrinks. (file, line text start) → owner and reason.
KNOWN = {
    ("legacy_materials.py", "_PRISTINE"): "b9: §A6 adapter debt, the process_state snapshot taken at import",
    ("legacy_materials.py", "_NOT_AT_REST"): "b9: §A6 adapter debt, the import-time at-rest check",
}


def _mutable(v) -> bool:
    if isinstance(v, (ast.List, ast.Dict, ast.Set, ast.ListComp, ast.DictComp, ast.SetComp)):
        return True
    if isinstance(v, ast.Call):
        f = v.func
        name = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
        return name in MUTABLE_CALLS
    return False


def _target_name(t) -> str:
    return t.id if isinstance(t, ast.Name) else ast.unparse(t)


LOCAL_RESULT = "module-level binding of a local function's result"


def _local_factory_call(v, local_defs) -> bool:
    """A call to a function defined in the same module: its result (e.g. a closure over a memo) can carry state."""
    return isinstance(v, ast.Call) and isinstance(v.func, ast.Name) and v.func.id in local_defs


def findings(source: str, name: str) -> list:
    """(file, target, line, what) for each module-level mutable assignment, module-level binding of a same-module
    function's result (r2), module-level augmented assignment, and `global` statement anywhere in `source`."""
    tree = ast.parse(source)
    out = []
    local_defs = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    for n in tree.body:
        value = getattr(n, "value", None)
        if isinstance(n, (ast.Assign, ast.AnnAssign)) and value is not None and _local_factory_call(value, local_defs):
            targets = n.targets if isinstance(n, ast.Assign) else [n.target]
            out += [(name, _target_name(t), n.lineno, LOCAL_RESULT) for t in targets]
        elif isinstance(n, ast.Assign) and _mutable(n.value):
            out += [(name, _target_name(t), n.lineno, "mutable module-level assignment") for t in n.targets]
        elif isinstance(n, ast.AnnAssign) and n.value is not None and _mutable(n.value):
            out.append((name, _target_name(n.target), n.lineno, "mutable module-level assignment"))
        elif isinstance(n, ast.AugAssign):
            out.append((name, _target_name(n.target), n.lineno, "module-level augmented assignment"))
    for n in ast.walk(tree):
        if isinstance(n, ast.Global):
            out += [(name, g, n.lineno, "global statement") for g in n.names]
    return out


_ATOMS = (str, bytes, int, float, complex, bool, type(None), type, types.BuiltinFunctionType)


def deep_frozen(x, _seen=None) -> bool:
    """True if `x` cannot change: atoms, and tuples, frozensets, read-only mappings, frozen dataclasses and functions
    whose contents (closure cells, defaults) are themselves deep-frozen."""
    _seen = set() if _seen is None else _seen
    if id(x) in _seen:
        return True
    _seen.add(id(x))
    if isinstance(x, _ATOMS):
        return True
    if isinstance(x, (tuple, frozenset)):
        return all(deep_frozen(v, _seen) for v in x)
    if isinstance(x, types.MappingProxyType):
        return all(deep_frozen(k, _seen) and deep_frozen(v, _seen) for k, v in x.items())
    if dataclasses.is_dataclass(x) and not isinstance(x, type):
        return x.__dataclass_params__.frozen and all(deep_frozen(getattr(x, f.name), _seen)
                                                     for f in dataclasses.fields(x))
    if isinstance(x, types.FunctionType):
        cells = [c.cell_contents for c in (x.__closure__ or ())]
        return all(deep_frozen(v, _seen) for v in cells + list(x.__defaults__ or ()))
    if hasattr(x, "pattern") and hasattr(x, "flags"):               # a compiled regex
        return True
    return False


def scan() -> list:
    """The static findings, with a same-module function's result checked at run time: kept only if the bound value
    is not deep-frozen (e.g. ROLES and REGISTRY are read-only mappings of frozen entries)."""
    out = []
    for p in sorted(ROOT.rglob("*.py")):
        parts = p.relative_to(ROOT).parts
        if "tests" in parts or any(x.startswith(".") for x in parts):     # the tests, and the venv
            continue
        rel = str(p.relative_to(ROOT))
        for f in findings(p.read_text(encoding="utf-8"), rel):
            if f[3] == LOCAL_RESULT:
                mod = importlib.import_module("solver." + rel[:-3].replace("/", "."))
                if deep_frozen(getattr(mod, f[1])):
                    continue
            out.append(f)
    return out


class NoModuleState(unittest.TestCase):
    def test_solver_has_no_unowned_module_state(self):
        got = scan()
        new = [f for f in got if (f[0], f[1]) not in KNOWN]
        self.assertEqual(new, [], "mutable module state or global in solver/ (phase1-design §A6)")

    def test_known_entries_still_fire(self):
        """An owned entry that was fixed must leave KNOWN in the same commit (the list only shrinks)."""
        fired = {(f[0], f[1]) for f in scan()}
        self.assertEqual(sorted(k for k in KNOWN if k not in fired), [])

    def test_the_scan_reads_files(self):
        self.assertGreater(len(list(ROOT.glob("*.py"))), 10)                 # control: it is looking at solver/


class PlantedControls(unittest.TestCase):
    def test_each_planted_form_fails(self):
        for src, what in (("_X = {}", "mutable module-level assignment"),
                          ("_X: list = []", "mutable module-level assignment"),
                          ("_X = dict(a=1)", "mutable module-level assignment"),
                          ("_X = sorted(y)", "mutable module-level assignment"),
                          ("_X = collections.defaultdict(int)", "mutable module-level assignment"),
                          ("Loader.table = {k: 1 for k in 'ab'}", "mutable module-level assignment"),
                          ("_N = 0\n_N += 1", "module-level augmented assignment"),
                          ("def f():\n    global _N\n    _N = 1", "global statement"),
                          ("def _make():\n    memo = {}\n    return lambda k: memo.setdefault(k, k)\nget = _make()",
                           "module-level binding of a local function's result")):
            with self.subTest(src=src):
                self.assertIn(what, [f[3] for f in findings(src, "planted.py")])

    def test_deep_frozen(self):
        def make():
            memo = {}
            return lambda k: memo.setdefault(k, k)
        self.assertFalse(deep_frozen(make()))                              # planted: a closure over a memo
        self.assertFalse(deep_frozen(types.MappingProxyType({"a": [1]})))  # planted: a list inside a proxy
        self.assertTrue(deep_frozen(types.MappingProxyType({"a": (1, "x")})))
        from solver import body as bd, refusals
        self.assertTrue(deep_frozen(bd.ROLES))
        self.assertTrue(deep_frozen(refusals.REGISTRY))

    def test_immutable_forms_pass(self):
        for src in ("_X = (1, 2)", "_X = frozenset({1})", "_X = types.MappingProxyType({'a': 1})", "_X = 'a'",
                    "def f():\n    x = {}\n    x['a'] = 1", "class C:\n    pass"):
            with self.subTest(src=src):
                self.assertEqual(findings(src, "planted.py"), [])


if __name__ == "__main__":
    unittest.main()
