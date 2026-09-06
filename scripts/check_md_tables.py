#!/usr/bin/env python3
# 마크다운 표가 실제로 표로 렌더되는지 본다 — 게이트 열 몇 개가 내용은 보면서 렌더는 안 봤다
"""Find Markdown tables that will not render as tables.

    python3 scripts/check_md_tables.py

A GFM table starts with a header row followed by a delimiter row (`|---|---|`). It renders as a table
only if it **begins a block**: a non-blank prose line immediately above the header makes the whole
thing continuation text, and the reader sees pipes. Nothing in this repository's gates looked at that,
so the class was caught only by eye — twice on 2026-09-06, each costing a report, a repair and a
24-minute re-gate.

**Detection is by the delimiter row, not by a leading pipe.** The obvious test — "a line starting with
`|` after prose" — was tried first and is wrong here: `|g|/α ≈ 1`, `|ΔE/E| ≈ 3.6e-3` and `|dE/E| =
9.5e-9` are absolute values in running prose, three false positives out of seven hits. Requiring the
delimiter row removed all three **and** found a real case the loose version had missed. Precision and
recall moved the same way, which is worth remembering the next time a checker looks too quiet.

Also skipped: fenced code blocks, headings and block quotes above a table (both legitimately start a
block), and a table opening right after a closing fence.

Exit code 1 on any unexempted hit.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "_papers", "node_modules", ".venv", ".archive"}
DELIM = re.compile(r"^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$")

# 예외는 파일이 아니라 **이유**가 등록된다. 이유가 없으면 그건 미수리이지 예외가 아니다.
EXEMPT: dict[str, str] = {
    "engine/c32-k4-basename-notes.ko.md":
        "preserved verbatim from the parallel seat's scratch — its own header says 원문 무편집 and "
        "separates the author's revisions from work-seat edits. Inserting a blank line to rescue the "
        "rendering would break the guarantee the file exists to make; a broken table is the cheaper "
        "loss. Do not 'fix' this one.",
}


def hits(path: Path) -> list[tuple[int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[tuple[int, str]] = []
    fence = False
    for n, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence or n < 2:
            continue
        if "|" not in line or not DELIM.match(line) or "|" not in lines[n - 1]:
            continue
        above = lines[n - 2]
        if not above.strip():
            continue
        if above.lstrip()[0] in "|#>" or above.lstrip().startswith("```"):
            continue
        # 1-기준 줄번호 — 편집기가 세는 것과 같아야 한다
        out.append((n + 1, above.strip()[:70]))
    return out


def main() -> int:
    bad: list[str] = []
    exempted = 0
    scanned = 0
    for path in sorted(ROOT.rglob("*.md")):
        if any(p in SKIP_DIRS for p in path.parts):
            continue
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()
        for line_no, above in hits(path):
            if rel in EXEMPT:
                exempted += 1
                continue
            bad.append(f"{rel}:{line_no} — the header row is glued to prose, so the table renders as "
                       f"text. Above it: {above!r}")

    for b in bad:
        print(f"  [FAIL] 표가 산문에 붙어 렌더 안 됨 — {b}")
    if bad:
        print(f"\n  빈 줄 하나면 됩니다. 표가 리스트 항목 안에 들여쓰여 있으면 빈 줄로도 안 되니 "
              f"목록 밖으로 내어쓰십시오.")
        return 1
    print(f"  [PASS] 마크다운 표 렌더 — {scanned}개 파일, 산문에 붙은 표 0건 "
          f"(의도적 예외 {exempted}건: {', '.join(EXEMPT) if exempted else '없음'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
