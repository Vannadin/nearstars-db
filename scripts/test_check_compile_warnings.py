#!/usr/bin/env python3
# check_compile_warnings 시험 — 심은 잘못된 이스케이프(비raw 문서문자열의 `\|`, f-문자열의 `\d`)는 빨강, raw 로 고치면 초록이고 값은 같음, 문법 오류도 빨강, 게이트 모드가 실제 추적 트리를 다 읽음 (FIX3)
"""python3 scripts/test_check_compile_warnings.py"""
import ast
import subprocess
import sys
import tempfile
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_compile_warnings as cw  # noqa: E402

FAILS = []


def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        FAILS.append(name)


def run(*args, cwd=None):
    return subprocess.run([sys.executable, str(Path(cw.__file__)), *args], capture_output=True, text=True, cwd=cwd)


DOC_BAD = '"""split on every unescaped `|`, where `\\|` is the only escape."""\n'      # the shape of check_md_tables.py's docstring
DOC_RAW = 'r' + DOC_BAD
F_BAD = 'import re\np = "".join(f"(?P<p{i}>-?\\d+)" for i in range(2))\n'               # the shape of c1check.py's f-string pattern
F_RAW = F_BAD.replace('f"(?P', 'rf"(?P')

with tempfile.TemporaryDirectory() as td:
    d = Path(td)
    for name, src in (("bad.py", DOC_BAD), ("raw.py", DOC_RAW), ("fbad.py", F_BAD), ("fraw.py", F_RAW),
                      ("syntax.py", "def f(:\n")):
        (d / name).write_text(src)
    r = run(str(d / "bad.py"))
    check("(1) planted `\\|` in a non-raw docstring: rc 1 and a [FAIL] line naming line 1",
          r.returncode == 1 and "bad.py" + ":1 — " in r.stdout and "\\|" in r.stdout)
    check("(2) the same docstring raw: rc 0", run(str(d / "raw.py")).returncode == 0)
    with warnings.catch_warnings():               # this test's own parse of the planted source prints nothing
        warnings.simplefilter("ignore")
        same_doc = ast.get_docstring(ast.parse(DOC_BAD), clean=False) == ast.get_docstring(ast.parse(DOC_RAW), clean=False)
        same_f = ast.dump(ast.parse(F_BAD)) == ast.dump(ast.parse(F_RAW))
    check("(3) raw leaves the docstring's value unchanged", same_doc)
    r = run(str(d / "fbad.py"))
    check("(4) planted `\\d` in an f-string: rc 1", r.returncode == 1 and "fbad.py" + ":2" in r.stdout)
    check("(5) rf leaves the f-string's parts unchanged and rc 0",
          run(str(d / "fraw.py")).returncode == 0 and same_f)
    check("(6) a SyntaxError is a finding", "SyntaxError" in run(str(d / "syntax.py")).stdout)
    # --tree: a planted tracked file in a fresh git tree is read by the tree mode (the artifacts tree's path)
    g = d / "tree"
    g.mkdir()
    subprocess.run(["git", "init", "-q", str(g)], check=True)
    (g / "ok.py").write_text("x = 1\n")
    (g / "sub").mkdir()
    (g / "sub" / "bad.py").write_text(DOC_BAD)
    (g / "untracked.py").write_text(DOC_BAD)
    subprocess.run(["git", "-C", str(g), "add", "ok.py", "sub/bad.py"], check=True)
    r = run("--tree", str(g))
    check("(7) --tree reads the tracked files only: rc 1 on sub/bad.py, untracked.py not read",
          r.returncode == 1 and "sub/bad.py" + ":1" in r.stdout and "untracked.py" not in r.stdout)
r = run()
check(f"(8) gate mode on this tree: rc 0 with a PASS line ({r.stdout.strip()[-60:]})",
      r.returncode == 0 and r.stdout.startswith("compile-warnings: PASS — "))
print("test_check_compile_warnings: 모두 통과" if not FAILS else f"test_check_compile_warnings: 실패 {len(FAILS)}")
sys.exit(1 if FAILS else 0)
