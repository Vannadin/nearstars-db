#!/usr/bin/env python3
# 추적 .py 를 모두 컴파일해 SyntaxWarning(3.12)·DeprecationWarning(3.9, 잘못된 이스케이프)·SyntaxError 를 잡는다 — 경고 출력이 linecache 로 자기 소스를 다시 읽어 읽기 감사를 흔든 ES-f6 착지 group 4 의 부류 (FIX3)
"""python3 scripts/check_compile_warnings.py                gate mode: every git-tracked .py in this tree
   python3 scripts/check_compile_warnings.py --tree DIR     every git-tracked .py in DIR (the artifacts tree)
   python3 scripts/check_compile_warnings.py FILE...        the named files only (tests)

Each file is compiled with every warning recorded, as `-W error::SyntaxWarning` would refuse it on 3.12. A finding is
a SyntaxWarning (3.12: an invalid escape such as `\\|` or `\\d` in a non-raw string, `is` with a literal, …), a
DeprecationWarning raised by the compile itself (3.9 and 3.11 report the same invalid escapes that way), or a
SyntaxError.
Why it is a gate step: on 3.12 the warning is printed with its source line, which Python re-reads through linecache.
Under the gate's read audit (GATE_MASS_LOG) that re-read was recorded as the step reading its own file, undeclared:
the ES-f6 landing gate's group 4, «scripts/check_md_tables.py read scripts/check_md_tables.py, not declared», from a
`\\|` in check_md_tables.py's docstring (c8, 11-06). The fix is a raw string; the value does not change when the escape
is not a real one, and the guard keeps the class out.
Each finding is one `[FAIL] compile <file>:<line> — <Category>: <message>` line; rc 1 if any, else
«compile-warnings: PASS — N files (Python X.Y.Z)» and rc 0."""
import subprocess
import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def findings(path, src):
    """[(line, category, message)] for one source."""
    out = []
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            compile(src, str(path), "exec", dont_inherit=True)
        except SyntaxError as e:
            out.append((e.lineno or 0, "SyntaxError", str(e.msg)))
    for x in w:
        if issubclass(x.category, (SyntaxWarning, DeprecationWarning)):
            out.append((x.lineno or 0, x.category.__name__, str(x.message)))
    return out


def tracked(tree):
    r = subprocess.run(["git", "-C", str(tree), "ls-files", "-z", "*.py"], capture_output=True, check=True)
    return [Path(tree) / p for p in r.stdout.decode().split("\0") if p]


def main(argv):
    if argv[:1] == ["--tree"]:
        tree = Path(argv[1]).resolve()
        files, base = tracked(tree), tree
    elif argv:
        files, base = [Path(a) for a in argv], Path.cwd()
    else:
        files, base = tracked(ROOT), ROOT
    bad = 0
    for f in files:
        try:
            rel = f.resolve().relative_to(base)
        except ValueError:
            rel = f
        for line, cat, msg in findings(rel, f.read_bytes()):
            print(f"[FAIL] compile {rel}:{line} — {cat}: {msg}")
            bad += 1
    if bad:
        return 1
    print(f"compile-warnings: PASS — {len(files)} files (Python {sys.version.split()[0]})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
