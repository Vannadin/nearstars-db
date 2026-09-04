# 인용 체커 자기검증 — 일부러 썩힌 앵커와 애매한 앵커에서 실제로 FAIL 하는지 (C33)
"""Prove the citation checker fails on citations that are wrong.

    python3 engine/test_check_refs.py

A checker that only ever passes is the thing being replaced: the line-number scheme "passed" for
two weeks while `internal-heat-luminosity-methodology.md:119` walked from one contract block's
Needs line to another block's, and then to a Returns line. So the checker is aimed at a synthetic
document, in a temporary tree, where the three outcomes are known by construction.

1. Unique phrase → resolves, one match.
2. Phrase that is not in the document → **rotten**, and `main()` returns 1.
3. Phrase that appears twice → **ambiguous**, and `main()` returns 1. This is the case the old
   scheme could not even express: a line number is never ambiguous, it is just silently wrong.
4. A line-number citation is counted as unmigrated and does NOT fail (the migration is in batches).
5. A recipe module's bare `doc @«…»` resolves against the doc its own `RECIPE` declares.
"""
from __future__ import annotations

import io
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

import check_refs

DOC = """# A synthetic document

The unique sentence lives here and nowhere else.

A repeated sentence.
A repeated sentence.
"""


def main() -> int:
    fails: list[str] = []

    def ok(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "docs" / "reference").mkdir(parents=True)
        (root / "engine").mkdir()
        (root / "docs" / "reference" / "synthetic-methodology.md").write_text(DOC, encoding="utf-8")

        # 1-3, plus 4: one of each kind in a file the checker scans
        (root / "engine" / "cited.py").write_text(
            '# 합성 인용 표본\n'
            'RECIPE = "synthetic-methodology"\n'
            'A = "synthetic-methodology.md@«The unique sentence lives here»"\n'
            'B = "synthetic-methodology.md@«a phrase that was deleted from the document»"\n'
            'C = "synthetic-methodology.md@«A repeated sentence.»"\n'
            'D = "synthetic-methodology.md:3"\n'
            'E = "doc @«nowhere and nowhere else»"\n',
            encoding="utf-8")

        check_refs.ROOT, check_refs.DOCS = root, root / "docs" / "reference"
        check_refs.SCAN = (("engine/*.py",),)
        check_refs.CACHE.clear()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check_refs.main()
        out = buf.getvalue()

        ok(rc == 1, "2/3: a rotten or ambiguous anchor must make the run fail")
        ok("해석 성공 1" in out, f"1: exactly one anchor should resolve, got:\n{out}")
        ok("no such phrase" in out and "was deleted from the document" in out,
           "2: the deleted phrase must be reported as rotten, by name")
        ok("matches 2x" in out, "3: the twice-occurring phrase must be reported as ambiguous")
        ok("미이행 줄번호 1건" in out, f"4: the line-number citation must count as unmigrated, got:\n{out}")
        ok("nowhere and nowhere else" in out,
           "5: a bare `doc @«…»` must resolve against the module's own RECIPE doc (and here be rotten)")

        # 5 again, positively: the same bare form with a phrase that IS there resolves
        (root / "engine" / "cited.py").write_text(
            '# 합성 인용 표본\n'
            'RECIPE = "synthetic-methodology"\n'
            'A = "doc @«The unique sentence lives here»"\n',
            encoding="utf-8")
        check_refs.CACHE.clear()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check_refs.main()
        ok(rc == 0 and "해석 성공 1" in buf.getvalue(),
           f"5: the module's own doc must resolve, got rc={rc}\n{buf.getvalue()}")

    for f in fails:
        print(f"  [FAIL] {f}")
    if fails:
        return 1
    print("  [PASS] 인용 체커 자기검증 — 고유 1회 통과 · 삭제된 구절 썩음 판정 · 2회 매치 애매 판정 · "
          "줄번호는 미이행 카운트 · RECIPE 자기문서 해석")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
