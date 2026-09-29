# 모듈 수준 가변 상태가 전부 process_state 레지스트리에 있는지 세는 시험 (structure-grid 덧붙임 44)
"""Every module-level name that a function rebinds with ``global`` or whose contents a function mutates
must be listed in `process_state.REGISTRY` — a new cache without an entry fails the gate.

Counted forms (closed list): ``global NAME`` in a function; inside a function, on a module-level NAME:
subscript assignment ``NAME[k] = …``, any augmented assignment ``NAME[k] += …`` / ``NAME += …``,
``del NAME[k]``, and the methods update · setdefault · pop · popitem · clear · append · extend · insert ·
remove · add · discard. Not seen: setattr on modules, another module's attribute (``other.NAME = …``),
class attributes, attributes of module-level objects, contextvars, mutable default arguments, C extensions,
functools caches.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import process_state

HERE = Path(__file__).resolve().parent
METHODS = {"update", "setdefault", "pop", "popitem", "clear", "append", "extend", "insert", "remove", "add",
           "discard"}


def _root(node):
    while isinstance(node, (ast.Subscript, ast.Attribute)):
        node = node.value
    return node.id if isinstance(node, ast.Name) else None


def mutated_names(source: str) -> set[str]:
    """Module-level names this source rebinds or mutates from inside a function (the forms above)."""
    tree = ast.parse(source)
    top = {t.id for n in tree.body if isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign))
           for t in (n.targets if isinstance(n, ast.Assign) else [n.target]) if isinstance(t, ast.Name)}
    found = set()
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            continue
        for n in ast.walk(fn):
            if isinstance(n, ast.Global):
                found.update(n.names)
            elif isinstance(n, (ast.Assign, ast.AugAssign, ast.Delete)):
                targets = n.targets if isinstance(n, (ast.Assign, ast.Delete)) else [n.target]
                for t in targets:
                    if isinstance(t, ast.Subscript) or (isinstance(n, ast.AugAssign) and isinstance(t, ast.Name)):
                        r = _root(t)
                        if r in top:
                            found.add(r)
            elif (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in METHODS
                  and isinstance(n.func.value, ast.Name) and n.func.value.id in top):
                found.add(n.func.value.id)
    return found & top | {g for fn in ast.walk(tree) if isinstance(fn, ast.Global) for g in fn.names}


def engine_modules() -> list[Path]:
    return sorted(p for p in HERE.glob("*.py")
                  if not p.name.startswith("test_") and p.name not in ("process_state.py",))


def unregistered() -> list[str]:
    out = []
    for p in engine_modules():
        for name in sorted(mutated_names(p.read_text(encoding="utf-8"))):
            if (p.stem, name) not in process_state.REGISTRY:
                out.append(f"{p.stem}.{name}")
    return out


FIXTURE_GLOBAL = "X = 0\ndef f():\n    global X\n    X = 1\n"
FIXTURE_DICT = "D = {}\ndef f(k):\n    D.update({k: 1})\n"
FIXTURE_CONST = "C = {'a': 1}\ndef f():\n    return C['a']\n"


def main() -> int:
    fails = []
    got = (mutated_names(FIXTURE_GLOBAL), mutated_names(FIXTURE_DICT), mutated_names(FIXTURE_CONST))
    ok = got == ({"X"}, {"D"}, set())
    print(f"  [{'PASS' if ok else 'FAIL'}] 자기 시험 — global 재묶음 {sorted(got[0])} · 모듈 dict .update "
          f"{sorted(got[1])} · 상수 읽기 {sorted(got[2])}(0 이어야)")
    if not ok:
        fails.append("self-test")
    bad = unregistered()
    ok = not bad
    print(f"  [{'PASS' if ok else 'FAIL'}] 레지스트리 밖 모듈 수준 가변 상태 {len(bad)} 개"
          + (f": {', '.join(bad)} — `process_state.REGISTRY` 에 부류 · 까닭과 함께 등록" if bad else
             f" (모듈 {len(engine_modules())} · 등록 {len(process_state.REGISTRY)})"))
    if not ok:
        fails.append("unregistered")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
