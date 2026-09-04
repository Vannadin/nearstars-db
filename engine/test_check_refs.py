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
6. Every enumeration hole the 2026-09-05 audit found, one assertion each, because `5a056357` closed
   five of them and added no test — and the parse switch in that same commit opened two new silent
   passes that no test caught: an unparseable `chain.yaml` reported "0 failures" over the 8 % of
   citations it could still see, and citations inside YAML comments stopped being read. Both are
   asserted here now, along with an upper-case file name, a non-`.md` target, `bodies/*.yaml` being
   in the scan, a citation folded across lines by a `note: >` block, a bare file name being counted,
   a `chain.yaml` that parses but has lost its `edges` key, and a sentence-length anchor that spans
   the document's hard wrap.
7. **Rule 2**, the contract owner: an edge whose citation lands inside `## Contract — `X`` must have
   `X` as one of its own endpoints. Landing on *a* contract block is fine and common; landing on
   **another node's** is the failure that rotted 30 edges, and it is the only part of that failure a
   machine can see, because the five blocks' Needs lines read almost the same.
8. **Rule 3**, landings that cannot be meant: a blank line, a table separator, a horizontal rule. In
   wiring or code these fail; in a note they warn, because a note records what was true when written
   while chain.yaml is live wiring that has to resolve today.
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

## Contract — `alpha`

**Needs** — `x` [—]

## Contract — `beta`

**Needs** — `x` [—]

## 3. Body

The last paragraph.
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

        # 6, 7: a chain-shaped file, so the checker can see each citation's edge endpoints
        (root / "engine" / "chain.yaml").write_text(
            "edges:\n"
            '  - {from: gamma, to: alpha, ref: "synthetic-methodology.md@«## Contract — `alpha`»"}\n'
            '  - {from: gamma, to: beta, ref: "synthetic-methodology.md:14"}\n'
            '  - {from: gamma, to: delta, ref: "synthetic-methodology.md:14"}\n'
            '  - {from: gamma, to: delta, ref: "synthetic-methodology.md:4"}\n',
            encoding="utf-8")

        check_refs.ROOT, check_refs.DOCS = root, root / "docs" / "reference"
        check_refs.SCAN = (("engine/*.py",), ("engine/chain.yaml",))
        check_refs.CACHE.clear()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check_refs.main()
        out = buf.getvalue()

        ok(rc == 1, "2/3: a rotten or ambiguous anchor must make the run fail")
        ok("해석 성공 2" in out, f"1: the unique phrase and the alpha heading should both resolve, got:\n{out}")
        ok("no such phrase" in out and "was deleted from the document" in out,
           "2: the deleted phrase must be reported as rotten, by name")
        ok("matches 2x" in out, "3: the twice-occurring phrase must be reported as ambiguous")
        ok("미이행 줄번호 4건" in out, f"4: line-number citations must count as unmigrated, got:\n{out}")
        ok("nowhere and nowhere else" in out,
           "5: a bare `doc @«…»` must resolve against the module's own RECIPE doc (and here be rotten)")
        ok("계약 주인 불일치" in out and "delta" in out,
           f"6: an edge landing in another node's contract block must fail by name, got:\n{out}")
        ok(out.count("계약 주인 불일치") == 1,
           f"6: exactly one citation mismatches — the anchor into alpha's block on the gamma→alpha edge "
           f"and the line into beta's block on the gamma→beta edge must both pass, got:\n{out}")
        ok("있을 수 없는 착지" in out and "blank line" in out,
           f"7: a blank-line landing in chain.yaml must fail, got:\n{out}")

        # ── the five enumeration holes, and the two the parse switch opened ──────────────────
        (root / "docs" / "reference" / "UPPER_CASE_EVIDENCE.md").write_text(
            "# Evidence\n\nA sentence only this file has.\n", encoding="utf-8")
        (root / "engine" / "bodies").mkdir()
        (root / "engine" / "bodies" / "b.yaml").write_text(
            'inputs:\n  x: 1   # source: UPPER_CASE_EVIDENCE.md:3\n', encoding="utf-8")
        (root / "engine" / "chain.yaml").write_text(
            "edges:\n"
            '  - {from: gamma, to: alpha, ref: "UPPER_CASE_EVIDENCE.md@«A sentence only this file has.»"}\n'
            '  - {from: gamma, to: alpha, ref: "synthetic-methodology.md"}\n'
            '  - {from: gamma, to: alpha, ref: "cited.py:3"}\n'
            "  - from: gamma\n"
            "    to: alpha\n"
            "    note: >\n"
            "      a folded note whose citation is broken across lines:\n"
            "      synthetic-methodology.md@«The unique sentence lives here and nowhere\n"
            "      else.»\n"
            '  - {from: gamma, to: alpha}   # comment citation: synthetic-methodology.md:3\n',
            encoding="utf-8")
        check_refs.SCAN = (("engine/*.py",), ("engine/chain.yaml",), ("engine/bodies/*.yaml",))
        check_refs.CACHE.clear()
        buf = io.StringIO()
        argv = sys.argv[:]
        sys.argv = [argv[0], "--list"]          # the unmigrated rows only print when asked for
        with redirect_stdout(buf):
            rc = check_refs.main()
        sys.argv = argv
        out = buf.getvalue()
        ok("해석 성공 3" in out, f"hole 1/4: the upper-case name and the folded anchor must both resolve, "
                                 f"got:\n{out}")
        ok("bodies/b.yaml" in out, f"hole 3: engine/bodies/*.yaml must be scanned, got:\n{out}")
        ok("cited.py:3" in out, f"hole 2: a non-.md target must be enumerated, got:\n{out}")
        ok("문서 전체 인용 1건" in out, f"hole 5: a bare file name must be counted, got:\n{out}")
        ok("(folded)" in out, f"hole 4: a citation folded across lines must be read from the parsed "
                              f"value, got:\n{out}")
        ok(out.count("synthetic-methodology.md:3") >= 1,
           f"comments: a citation inside a YAML comment must stay visible, got:\n{out}")

        # a YAML that cannot be read at all must FAIL, not report zero problems over what it did read
        (root / "engine" / "chain.yaml").write_text("edges:\n  - {from: a, to: b\n", encoding="utf-8")
        check_refs.CACHE.clear()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check_refs.main()
        ok(rc == 1 and "does not parse" in buf.getvalue(),
           f"parse: an unparseable YAML must fail by name, got rc={rc}\n{buf.getvalue()}")
        # and one that parses but has lost the key the citations live under
        (root / "engine" / "chain.yaml").write_text("connections: []\n", encoding="utf-8")
        check_refs.CACHE.clear()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check_refs.main()
        ok(rc == 1 and "no edges" in buf.getvalue(),
           f"shape: a chain.yaml without its expected keys must fail, got rc={rc}\n{buf.getvalue()}")

        # the audit's control experiment: the SAME dead citation, bare and wrapped in a quotation.
        # Wrapping must not turn a failure green — an exemption from being rewritten is not an
        # exemption from being checked — and a quotation without a date is not a record at all.
        (root / "engine" / "chain.yaml").unlink(missing_ok=True)
        for name, body, want_fail in (
                ("bare.md", "A citation with no quoting: synthetic-methodology.md:4\n", True),
                ("wrapped.md", 'Quoted with a date, note (2026-09-04): *"synthetic-methodology.md:4"*\n', True),
                ("nodate.md", 'Quoted with no date: *"synthetic-methodology.md:4"*\n', True)):
            (root / "engine" / name).write_text(body, encoding="utf-8")
            check_refs.SCAN = ((f"engine/{name}",),)
            check_refs.CACHE.clear()
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = check_refs.main()
            got = buf.getvalue()
            ok(rc == (1 if want_fail else 0) and ("있을 수 없는 착지" in got) == want_fail,
               f"quote exemption ({name}): a blank-line landing must be reported either way, "
               f"got rc={rc}\n{got}")
            (root / "engine" / name).unlink()

        # a bare file name that two files in the repo share must fail with the candidates, instead of
        # being resolved by whichever copy sits nearest the citing file. The repo has 68 files called
        # checklist.md; proximity was choosing among them silently.
        (root / "one").mkdir(); (root / "two").mkdir()
        (root / "one" / "checklist.md").write_text("# one\n\nAlpha line.\n", encoding="utf-8")
        (root / "two" / "checklist.md").write_text("# two\n\nBeta line.\n", encoding="utf-8")
        (root / "engine" / "chain.yaml").write_text(
            "edges:\n"
            '  - {from: a, to: b, ref: "checklist.md:3"}\n'
            '  - {from: a, to: b, ref: "one/checklist.md:3"}\n', encoding="utf-8")
        check_refs.BASENAMES.clear()
        check_refs.SCAN = (("engine/chain.yaml",),)
        check_refs.CACHE.clear()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check_refs.main()
        out = buf.getvalue()
        ok(rc == 1 and "모호한 문서 이름" in out and "checklist.md" in out,
           f"ambiguous name: a shared base name must fail with its candidates, got rc={rc}\n{out}")
        ok(out.count("모호한 문서 이름") == 1,
           f"ambiguous name: the path-qualified citation must be accepted, got:\n{out}")
        check_refs.BASENAMES.clear()

        # a citation form nobody taught the checker must fail, not vanish: `<doc>.md:Contract` sat in no
        # bucket at all — not an anchor, not a line number, not a whole-document ref — and the run was
        # green. A file name followed immediately by `:` or `@` is a pointer into that file and must
        # land in a known form. Prose that merely names a file, and `module.py::symbol`, are not.
        (root / "engine" / "chain.yaml").write_text(
            "edges:\n"
            '  - {from: a, to: b, ref: "synthetic-methodology.md:Contract"}\n'
            '  - {from: a, to: b, note: "synthetic-methodology.md: a file named in prose"}\n'
            '  - {from: a, to: b, note: "cited.py::some_symbol names a symbol, not a place"}\n',
            encoding="utf-8")
        check_refs.SCAN = (("engine/chain.yaml",),)
        check_refs.CACHE.clear()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check_refs.main()
        out = buf.getvalue()
        ok(rc == 1 and "알 수 없는 인용 형식" in out and ":Contract" in out,
           f"unknown: an unrecognised citation form must fail by name, got rc={rc}\n{out}")
        ok(out.count("알 수 없는 인용 형식") == 1,
           f"unknown: prose naming a file and `py::symbol` must not be read as citations, got:\n{out}")

        # a file citing itself: writing the anchor puts the phrase in the file a second time, and that
        # second occurrence must not make its own citation ambiguous. radiogenic.py's heat-pipe refusal
        # is exactly this, and it ships as a result value.
        (root / "engine" / "cited.py").write_text(
            '# 합성 인용 표본\n'
            'RECIPE = "synthetic-methodology"\n'
            'def the_decision():\n'
            '    return "cannot-say (see cited.py@«def the_decision():»)"\n',
            encoding="utf-8")
        (root / "engine" / "chain.yaml").unlink(missing_ok=True)
        check_refs.SCAN = (("engine/*.py",),)
        check_refs.CACHE.clear()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check_refs.main()
        ok(rc == 0 and "해석 성공 1" in buf.getvalue(),
           f"self: a file citing itself must resolve, not read its own citation as a second place, "
           f"got rc={rc}\n{buf.getvalue()}")

        # a sentence-length anchor across the document's hard wrap
        (root / "docs" / "reference" / "wrapped-methodology.md").write_text(
            "# Wrapped\n\nThe transport test must land inside the measured band, and\n"
            "comfortably below the ceiling.\n", encoding="utf-8")
        (root / "engine" / "chain.yaml").write_text(
            "edges:\n"
            '  - {from: a, to: b, ref: "wrapped-methodology.md@«must land inside the measured band, '
            'and comfortably below the ceiling.»"}\n', encoding="utf-8")
        check_refs.SCAN = (("engine/chain.yaml",),)   # only the wrapped fixture, so rc is about it
        check_refs.CACHE.clear()
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = check_refs.main()
        ok(rc == 0 and "해석 성공 1" in buf.getvalue(),
           f"wrap: an anchor spanning the document's hard wrap must resolve, got rc={rc}\n{buf.getvalue()}")

        # 5 again, positively: the same bare form with a phrase that IS there resolves
        (root / "engine" / "cited.py").write_text(
            '# 합성 인용 표본\n'
            'RECIPE = "synthetic-methodology"\n'
            'A = "doc @«The unique sentence lives here»"\n',
            encoding="utf-8")
        (root / "engine" / "chain.yaml").unlink()      # the chain fixtures are done with
        check_refs.SCAN = (("engine/*.py",),)
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
    print("  [PASS] 인용 체커 자기검증 — 고유 1회 통과 · 삭제된 구절 썩음 · 2회 매치 애매 · 남의 계약 블록 착지 · "
          "빈 줄 착지 · 줄번호는 미이행 카운트 · RECIPE 자기문서 해석 · 대문자 파일명 · bodies 스캔 · "
          "비-.md 대상 · 접힌 인용 · 문서명만 계수 · YAML 파싱 실패 FAIL · 키 상실 FAIL · 주석 안 인용 · 하드랩 앵커 · "
          "알 수 없는 형식 FAIL · 자기 인용 · 모호한 문서 이름 FAIL")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
