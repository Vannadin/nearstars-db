# 인용을 열거·해석·판정한다 — 앵커 구절이 대상 문서에서 정확히 1회 매치되는지 (C33)
"""Resolve every citation in the engine against the document it names.

    python3 engine/check_refs.py            # report + verdict
    python3 engine/check_refs.py --list     # also list every citation it found

A line number is not a citation, it is a bet that the document will not grow. It keeps losing:
`internal-heat-luminosity-methodology.md:119` was a contract block's Needs line when 30 edges were
drawn against it, then another block's Needs line, and then — inside the very commit that went to
*fix* citations (25980fdc) — a Returns line. Nothing failed at any step, because nothing resolved
the number. So the engine cites **phrases**, and this checker makes the citation carry its own test.

The anchor form, everywhere (chain.yaml, code comments and strings, notes):

    <doc>.md@«a phrase that occurs exactly once in that document»

and, inside a recipe module that declares `RECIPE = "<slug>"`, the same thing against its own doc:

    doc @«…»

Verdicts per anchor: exactly one match → ok. Zero → **rotten** (the phrase is gone or was never
there). Two or more → **ambiguous** (the anchor cannot say which place it means). Both fail.

Citations still written as `<doc>.md:123` or inline `doc :123` are counted as **unmigrated** and
listed, but do not fail: C33 is migrating them in batches. Tighten the last line of `main()` to
require zero once that is done.

Guillemets delimit the phrase because a phrase may contain quotes and apostrophes ("against
Earth's `T_eq ≈ 255 K`") and must survive being embedded in YAML, Python and Markdown without
escaping. The phrase is matched **verbatim**, including runs of spaces: the heat doc's
`⇒  T_eff⁴  =  T_eq⁴  +  T_int⁴` is unique only with its double spaces.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DOCS = ROOT / "docs" / "reference"

ANCHOR = re.compile(r"([a-z0-9-]+\.md)@«([^»]*)»")
SELF_ANCHOR = re.compile(r"(?<![a-z0-9-])doc @«([^»]*)»")
LINE_REF = re.compile(r"([a-z0-9-]+\.md):([0-9]+(?:[-–][0-9]+)?)")
SELF_LINE = re.compile(r"(?<![a-z0-9-])doc :([0-9]+(?:[-–][0-9]+)?)")
RECIPE_DECL = re.compile(r'^RECIPE = "([a-z0-9-]+)"', re.M)

SCAN = (("engine/chain.yaml",), ("engine/bindings.yaml",),
        ("engine/*.py",), ("engine/tools/*.py",), ("engine/*.md",),
        ("scripts/**/*.py",))
CACHE: dict[Path, str] = {}


def text(path: Path) -> str:
    if path not in CACHE:
        CACHE[path] = path.read_text(encoding="utf-8")
    return CACHE[path]


# The self-test builds deliberately rotten anchors against a synthetic document; scanning them here
# would report the test's own fixtures as failures.
SKIP = {"test_check_refs.py"}


def files() -> list[Path]:
    out: list[Path] = []
    for (pattern,) in SCAN:
        out += sorted(ROOT.glob(pattern))
    return [p for p in out if p.is_file() and p.name not in SKIP]


def own_doc(path: Path) -> str | None:
    """The doc a module's bare `doc :N` / `doc @«…»` means: its own declared RECIPE."""
    if path.suffix != ".py":
        return None
    m = RECIPE_DECL.search(text(path))
    return f"{m.group(1)}.md" if m else None


def resolve(doc: str, phrase: str) -> tuple[str, int]:
    target = DOCS / doc
    if not target.exists():
        return "no such document", 0
    return "", text(target).count(phrase)


def main() -> int:
    listing = "--list" in sys.argv
    rotten: list[str] = []
    ambiguous: list[str] = []
    unmigrated: list[str] = []
    ok = 0

    for path in files():
        rel = path.relative_to(ROOT)
        mine = own_doc(path)
        for i, line in enumerate(text(path).splitlines(), 1):
            hits = [(m.group(1), m.group(2)) for m in ANCHOR.finditer(line)]
            hits += [(mine, m.group(1)) for m in SELF_ANCHOR.finditer(line) if mine]
            for doc, phrase in hits:
                why, n = resolve(doc, phrase)
                where = f"{rel}:{i}: {doc}@«{phrase[:60]}»"
                if why:
                    rotten.append(f"{where} — {why}")
                elif n == 0:
                    rotten.append(f"{where} — no such phrase in {doc}")
                elif n > 1:
                    ambiguous.append(f"{where} — matches {n}x, the anchor cannot say which")
                else:
                    ok += 1
                    if listing:
                        print(f"  [ok] {where}")
            for m in LINE_REF.finditer(line):
                unmigrated.append(f"{rel}:{i}: {m.group(1)}:{m.group(2)}")
            for m in SELF_LINE.finditer(line):
                unmigrated.append(f"{rel}:{i}: {mine or 'doc'} :{m.group(1)}")

    print(f"인용 점검 — 앵커 {ok + len(rotten) + len(ambiguous)}건 (해석 성공 {ok}) · "
          f"미이행 줄번호 {len(unmigrated)}건 · 문서 {len(list(DOCS.glob('*.md')))}종")
    for label, rows in (("썩은 앵커", rotten), ("애매한 앵커", ambiguous)):
        for r in rows:
            print(f"  [FAIL] {label} — {r}")
    if unmigrated and listing:
        for u in unmigrated:
            print(f"  [미이행] {u}")
    if rotten or ambiguous:
        print(f"[FAIL] 인용 {len(rotten) + len(ambiguous)}건이 해석되지 않는다")
        return 1
    # C33 이 끝나면 여기서 미이행 0 을 요구하도록 조인다.
    print(f"  [PASS] 앵커 {ok}건 전부 대상 문서에서 정확히 1회 매치 · 미이행 {len(unmigrated)}건은 배치 이행 대기")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
