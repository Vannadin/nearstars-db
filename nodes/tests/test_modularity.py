# 노드 모듈성 시험 — 다른 노드 import·전역·파일 접근 금지, 가짜 입력으로 단독 실행, 구현 교체 시 아래쪽만 낡음, 실행 중 열린 파일 (prereg-t-eq-stellar 사후 노트 1, N14–N17)
"""Post-freeze note 1 of `rewrite/nodes/prereg-t-eq-stellar.frozen.md`: N14–N17 (owner: nodes are truly modular).

    solver/.venv/bin/python -m unittest nodes.tests.test_modularity
"""
import ast
import builtins
import copy
import io
import math
import shutil
import tempfile
import unittest
from pathlib import Path

from solver.result import Answer, Band, Quantity, SolverInfo, Sources, SourceBand, Where

from nodes import records, run_id as rid, spec as sp
from nodes.runner import Runner
from nodes.types import NodeProvenance

REPO = Path(__file__).resolve().parents[2]
ALLOWED_IMPORTS = {"math"}
FORBIDDEN_NAMES = {"open", "__import__", "eval", "exec", "globals", "compile", "importlib"}
PROXIMA_B = {"name": "Proxima Cen b", "kind": "planet", "hosts": ["Proxima Cen"], "parent": None,
             "companions": ["Alpha Centauri A", "Alpha Centauri B"]}


def computed_modules():
    return {n: REPO / "nodes" / f"{n}.py" for n, s in sp.load_all().items() if s["kind"] == "computed"}


def scan(source: str) -> list:
    """Violations of N14 in one computed node module's source."""
    bad = []
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            bad += [f"import {a.name}" for a in node.names if a.name.split(".")[0] not in ALLOWED_IMPORTS]
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in ALLOWED_IMPORTS | {"__future__"}:
                bad.append(f"from {node.module} import …")
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN_NAMES:
            bad.append(f"name {node.id}")
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            bad.append("global/nonlocal statement")
    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.Import, ast.ImportFrom)):
            continue
        if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
            continue                                            # docstring
        if isinstance(stmt, (ast.Assign, ast.AnnAssign)):
            targets = stmt.targets if isinstance(stmt, ast.Assign) else [stmt.target]
            if all(isinstance(t, ast.Name) and t.id.isupper() for t in targets) and \
                    isinstance(stmt.value, ast.Constant):
                continue                                        # UPPERCASE constant
        bad.append(f"module-level statement at line {stmt.lineno}")
    return bad


def stub(key, point, grade="measured", half=None, run="stub"):
    band, reason = None, "stub"
    if half:
        band = Band(lo=point - half, hi=point + half, method="stub",
                    sources=Sources(input=SourceBand(-half, half, "stub"), model=None, solver=None,
                                    model_reason="stub", solver_reason="stub"))
        reason = None
    return Quantity(key=key, unit="x", point=point, kind="exact", method="read", where=Where("body"), band=band,
                    band_reason=reason, provenance=NodeProvenance(grade=grade, solver=SolverInfo(solve_id=run)))


EARTH = {"l_host": [stub("star_physical.luminosity", 3.828e26)], "a": stub("orbit_elements.a", 1.495978707e11),
         "e": stub("orbit_elements.e", 0.0167), "albedo": stub("bond_albedo_declared.bond_albedo", 0.306)}
EARTH_BODY = {"name": "Earth (stub)", "kind": "planet", "hosts": ["Sun (stub)"], "parent": None}


class N14ImportsAndGlobals(unittest.TestCase):
    def test_every_computed_module_is_clean(self):
        for n, path in computed_modules().items():
            self.assertEqual(scan(path.read_text()), [], n)

    def test_planted_violations_fail(self):
        src = (REPO / "nodes/t_eq_stellar.py").read_text()
        for plant in ("import json\n", "from nodes import records\n", "_CACHE = {}\n", "from solver import result\n"):
            self.assertNotEqual(scan(src + plant), [], plant)
        self.assertNotEqual(scan(src.replace("def compute(ctx):", "def compute(ctx):\n    open('x')", 1)), [])


class N15AloneWithStubs(unittest.TestCase):
    def test_t_eq_alone(self):
        r = Runner()                                   # specs are loaded before the guard goes up
        code = {str((REPO / p).resolve()) for p in rid.code_blobs(r.specs["t_eq_stellar"])}
        real_open, real_io_open, real_load = builtins.open, io.open, records._load
        refused = []

        def guard(file, *a, **k):                      # only the run id's code blobs may be read (contract §6)
            if str(Path(file).resolve()) not in code:
                refused.append(str(file))
                raise AssertionError(f"opened {file} during a stubbed run")
            return real_io_open(file, *a, **k)

        def no_records(*a, **k):
            refused.append("records._load")
            raise AssertionError("records were read during a stubbed run")

        builtins.open = io.open = guard
        records._load = no_records
        try:
            out, run = r.run_with_inputs("t_eq_stellar", EARTH_BODY, dict(EARTH, radius=stub("x.radius", 1.0)))
        finally:
            builtins.open, io.open, records._load = real_open, real_io_open, real_load
        self.assertEqual(refused, [])
        self.assertIsInstance(out, Answer)
        t = next(q for q in out.quantities if q.key == "t_eq_stellar.t_eq")
        self.assertLess(abs(t.point - 254.047) / 254.047, 1e-4)
        self.assertEqual(r._memo, {})                   # no upstream node ran

    def test_missing_stub_refuses(self):
        given = dict(EARTH)
        given.pop("albedo")
        out, _ = Runner().run_with_inputs("t_eq_stellar", EARTH_BODY, given)
        self.assertEqual((out.id, out.evidence["input"]), ("node.input_missing", "albedo"))


class N16SwapStalesOnlyDownstream(unittest.TestCase):
    FILES = ("solver/result.py", "solver/refusals.py", "nodes/types.py", "nodes/runner.py", "nodes/records.py",
             "nodes/t_eq_stellar.py", "nodes/spec.py", "nodes/quantities.yaml")

    def test_swap(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        for p in self.FILES:
            (tmp / p).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(REPO / p, tmp / p)
        specs = copy.deepcopy(sp.load_all())
        down = copy.deepcopy(specs["t_eq_stellar"])
        down.update(id="downstream", code=["nodes/runner.py"],
                    inputs={"t": {"from": "t_eq_stellar.t_eq", "scope": "self", "unit": "K"}})
        body = PROXIMA_B

        def ids():
            base = {n: rid.run_id(s, upstream={}, records={}, body=body, repo=tmp) for n, s in specs.items()}
            base["downstream"] = rid.run_id(down, upstream={"t": [base["t_eq_stellar"]]}, records={}, body=body,
                                            repo=tmp)
            return base

        before = ids()
        snapshot = {p: (tmp / p).read_bytes() for p in self.FILES}
        alt = (tmp / "nodes/t_eq_stellar.py").read_text().replace(
            "return (s * (1.0 - albedo) / (4.0 * SIGMA)) ** 0.25",
            "return math.sqrt(math.sqrt(s * (1.0 - albedo) / (4.0 * SIGMA)))")
        self.assertNotEqual(alt, (tmp / "nodes/t_eq_stellar.py").read_text())
        (tmp / "nodes/t_eq_stellar.py").write_text(alt)
        changed = [p for p in self.FILES if (tmp / p).read_bytes() != snapshot[p]]
        self.assertEqual(changed, ["nodes/t_eq_stellar.py"])
        after = ids()
        self.assertNotEqual(before["t_eq_stellar"], after["t_eq_stellar"])
        self.assertNotEqual(before["downstream"], after["downstream"])
        for n in ("star_physical", "orbit_elements", "bond_albedo_declared"):
            self.assertEqual(before[n], after[n], n)
        ns_old, ns_new = {"math": math}, {"math": math}
        exec(compile((REPO / "nodes/t_eq_stellar.py").read_text(), "old", "exec"), ns_old)
        exec(compile(alt, "new", "exec"), ns_new)
        for s, albedo in ((1361.0, 0.3), (897.6, 0.33), (5.0, 0.0)):
            a, b = ns_old["t_eq"](s, albedo), ns_new["t_eq"](s, albedo)
            self.assertLess(abs(a - b) / a, 1e-12)


class N17NoReachAround(unittest.TestCase):
    def test_opened_files(self):
        import nodes.t_eq_stellar as teq
        opened, during = [], []
        in_compute = [False]
        real_open, real_io_open, real_compute = builtins.open, io.open, teq.compute

        def spy(file, *a, **k):
            p = str(Path(file).resolve()) if not isinstance(file, int) else str(file)
            opened.append(p)
            if in_compute[0]:
                during.append(p)
            return real_io_open(file, *a, **k)

        def wrapped(ctx):
            in_compute[0] = True
            try:
                return real_compute(ctx)
            finally:
                in_compute[0] = False

        records._CACHE.clear()
        builtins.open = io.open = spy
        teq.compute = wrapped
        try:
            r = Runner()
            out, _ = r.result("t_eq_stellar", PROXIMA_B)
        finally:
            builtins.open, io.open, teq.compute = real_open, real_io_open, real_compute
        self.assertIsInstance(out, Answer)
        self.assertEqual(during, [])
        specs = sp.load_all()
        allowed = {str((REPO / s["reads"]["file"]).resolve()) for s in specs.values() if s.get("reads")}
        allowed |= {str(p.resolve()) for p in (REPO / "nodes").glob("*.yaml")}
        for s in specs.values():
            allowed |= {str((REPO / p).resolve()) for p in rid.code_blobs(s)}
        extra = sorted({p for p in opened if p.startswith(str(REPO)) and p not in allowed})
        self.assertEqual(extra, [])
        self.assertTrue(any(p.endswith("db/stellar_props_curated.json") for p in opened))


if __name__ == "__main__":
    unittest.main()
