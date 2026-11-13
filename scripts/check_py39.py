# 파이썬 3.9 호환 점검 — 시스템 python3(맥 3.9)으로 손으로 돌리는 scripts/ 도구(pipeline·phase4·refs·viz)가 3.9 문법으로 읽히고 실행 때 평가되는 PEP 604 합집합이 없는가
"""python3 scripts/check_py39.py            gate mode: every tracked .py under the system-python dirs (DIRS)
   python3 scripts/check_py39.py FILE...   the named files only (tests)

**Scope since 2026-11-13** (owner, artifacts directing-owner-1113 f075fa770: engine, solver and scripts code runs and
gates under 3.12 only; check.sh refuses an older gate interpreter by name). What still runs on the Mac's system
python3 (3.9.6) by design is the hand-run tooling below, which imports no engine/ or solver/ code and is not a gate step:
- scripts/pipeline/: the owner's DB pipeline, invoked as `python3 scripts/pipeline/<tool>.py` (the settings
  allow-list); not changed by the owner's decision (directing 11-13);
- scripts/phase4/, scripts/refs/, scripts/viz/: hand-run report, reference and render tools with a `python3` shebang.
Every other `python3`-shebang file under scripts/ (build_sitemap, check_citation_links, check_compile_warnings,
check_md_dupes, check_md_tables, check_phase4_gate, test_check_compile_warnings) is a gate step and runs under the gate
python (3.12); direct invocation under 3.9 is unsupported.
History: engine/ and scripts/ were the scope (VR-base 7); solver/ was excluded by directing ruling (A) on two premises
(no check.sh step runs solver code under the gate python; solver runs only in its own venv) that stopped holding, so
solver/signs.py's `str | None` (2075a4ee, 10-23) left the 3.9 solver discover at 81 import errors unflagged; the
3.12-only rule retires the question for engine/, solver/ and the gate's scripts.

Two things break a module there and not on 3.10+:
1. **3.10+ syntax** (`match`, parenthesized context managers, …): `ast.parse(src, feature_version=(3, 9))` refuses it.
   `feature_version` is best-effort in CPython; the second rule is the one that caught VR-base 7.
2. **A PEP 604 union evaluated at run time**, in a module without `from __future__ import annotations`:
   - a function's argument or return annotation (evaluated when the `def` runs, nested defs included);
   - a module- or class-level annotated assignment (`x: int | None = …`). A function-local one is not evaluated;
   - the type argument of `isinstance` / `issubclass` (`isinstance(x, int | None)`), with or without the future
     import, since that is an expression, not an annotation.
   A `|` inside a string annotation is not evaluated and is not flagged.
   Stated limit (r2 n3): a union reached through an alias (`Opt = int | None` then `x: Opt`), a `cast(int | None, …)`
   or a `TypeVar(bound=A | B)` is not followed; at 30f7cbcd the tree has none (r2's scan finds only re/os flag ORs).
Each finding is one `[FAIL] py39 <file>:<line> — <what>` line; rc 1 if any, else «py39: PASS» and rc 0."""
import ast
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRS = ("scripts/pipeline/", "scripts/phase4/", "scripts/refs/", "scripts/viz/")   # the system-python tools (docstring)


def _has_union(node) -> bool:
    return any(isinstance(n, ast.BinOp) and isinstance(n.op, ast.BitOr) for n in ast.walk(node))


def _future(tree) -> bool:
    return any(isinstance(n, ast.ImportFrom) and n.module == "__future__" and any(a.name == "annotations" for a in n.names)
               for n in tree.body)


def _evaluated_annotations(tree):
    """(node, what) for every annotation Python evaluates at run time without the future import."""
    def walk(body, scope):
        for n in body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                a = n.args
                for arg in a.posonlyargs + a.args + a.kwonlyargs + [x for x in (a.vararg, a.kwarg) if x]:
                    if arg.annotation is not None:
                        yield arg.annotation, f"annotation of argument «{arg.arg}» of {n.name}()"
                if n.returns is not None:
                    yield n.returns, f"return annotation of {n.name}()"
                yield from walk(n.body, "function")
            elif isinstance(n, ast.ClassDef):
                yield from walk(n.body, "class")
            elif isinstance(n, ast.AnnAssign) and scope != "function":
                yield n.annotation, f"{scope}-level annotation of «{ast.unparse(n.target) if hasattr(ast, 'unparse') else '?'}»"
            else:
                for field in ("body", "orelse", "finalbody", "handlers"):
                    sub = getattr(n, field, None)
                    if isinstance(sub, list):
                        yield from walk([x for x in sub if isinstance(x, ast.AST)], scope)
    yield from walk(tree.body, "module")


def check_source(src: str, name: str) -> list:
    fails = []
    try:
        tree = ast.parse(src, filename=name, feature_version=(3, 9))
    except SyntaxError as e:
        return [f"{name}:{e.lineno} — not Python 3.9 syntax: {e.msg}"]
    if not _future(tree):
        for node, what in _evaluated_annotations(tree):
            if _has_union(node):
                fails.append(f"{name}:{node.lineno} — PEP 604 union in the {what}, evaluated at run time on 3.9 "
                             "(add `from __future__ import annotations`)")
    for n in ast.walk(tree):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("isinstance", "issubclass")
                and len(n.args) == 2 and _has_union(n.args[1])):
            fails.append(f"{name}:{n.lineno} — PEP 604 union as the type argument of {n.func.id}() (3.10+ at run time)")
    return fails


def tracked() -> list:
    out = subprocess.run(["git", "ls-files", "-z", "--", *[d + "*.py" for d in DIRS]], cwd=ROOT, capture_output=True,
                         check=True).stdout.decode().split("\0")
    return [f for f in out if f]


def main(argv) -> int:
    files = argv or tracked()
    fails = []
    for f in files:
        p = Path(f) if Path(f).is_absolute() else ROOT / f
        fails += check_source(p.read_text(encoding="utf-8"), f)
    for x in fails:
        print(f"  [FAIL] py39 {x}")
    print(f"py39: {'FAIL' if fails else 'PASS'} — {len(files)} files")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
