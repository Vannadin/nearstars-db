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

**Second rule: cells per row.** A body row whose cell count differs from its header's is ragged. GFM
pads a short row with empty cells and **truncates a long one, so the extra cells are not rendered at
all** — the text is in the file and invisible on the page. The count is taken the way GFM takes it:
split on every unescaped `|`, where `\|` is the only escape, and do **not** protect code spans. A
pipe inside backticks still ends a cell in GFM, so `` `4π r² k |dT/dr|_ad` `` silently becomes three
cells; stripping code spans first hides eight such rows and invents two that GFM does not see.
A table's rows run from the delimiter row to the next blank line, so a soft-wrapped row counts as its
own one-cell row — which is what GFM renders.

Exit code 1 on any unexempted hit of either rule.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "_papers", "node_modules", ".archive"}
# ⚠ **a venv is matched by prefix** (191, 2026-09-12): the set held the exact string
#   `.venv`, which does not reach `engine/.venv-burnman`. Markdown **does** sit under that venv —
#   six files, `pyparsing/ai/best_practices.md` and five `LICENSE.md` — and they were scanned and
#   happened not to break a rule. That is luck, not absence: the scan counted 833 files where the
#   pre-venv gate counted 827. `.gitignore` speaks to git, not to scanners.
SKIP_PREFIXES = (".venv",)
DELIM = re.compile(r"^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$")
# GFM 는 백슬래시로 이스케이프한 `\|` 만 셀 구분자로 보지 않는다 — 코드 스팬 안의 파이프도 셀을 끊는다
UNESCAPED_PIPE = re.compile(r"(?<!\\)\|")

# 예외는 파일이 아니라 **이유**가 등록된다. 이유가 없으면 그건 미수리이지 예외가 아니다.
EXEMPT: dict[str, str] = {
    "engine/c32-k4-basename-notes.ko.md":
        "preserved verbatim from the parallel seat's scratch — its own header says 원문 무편집 and "
        "separates the author's revisions from work-seat edits. Inserting a blank line to rescue the "
        "rendering would break the guarantee the file exists to make; a broken table is the cheaper "
        "loss. Do not 'fix' this one.",
}

# 들쭉날쭉한 행의 예외도 같은 규칙 — 파일이 아니라 이유가 등록된다
EXEMPT_RAGGED: dict[str, str] = {
    "engine/c32-m-batch-a-notes.ko.md":
        "same guarantee as the k4 file above: its own header says 원문 무편집 / 'preserved verbatim "
        "from the parallel seat's scratch'. The short row is row 2 of the M-A table, where the record "
        "deliberately carries a two-cell aside instead of the full seven columns. GFM pads a short "
        "row, so nothing is hidden from the reader; editing the record to satisfy a checker would "
        "break the only thing the file promises.",
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


def cell_count(line: str) -> int:
    """Cells in one table line, counted the way GFM counts them."""
    s = line.strip()
    parts = UNESCAPED_PIPE.split(s)
    # 줄 앞뒤의 파이프는 칸을 만들지 않는다 — 이스케이프된 파이프로 끝나는 줄은 앞뒤 파이프가 아니다
    if s.startswith("|"):
        parts = parts[1:]
    if len(parts) > 1 and s.endswith("|") and not s.endswith("\\|"):
        parts = parts[:-1]
    return len(parts)


def ragged(path: Path) -> list[tuple[int, int, int, str]]:
    """Body rows whose cell count differs from their header's: (line, cells, header cells, text)."""
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[tuple[int, int, int, str]] = []
    fence = False
    n = 0
    while n < len(lines):
        line = lines[n]
        if line.lstrip().startswith("```"):
            fence = not fence
            n += 1
            continue
        if fence or n == 0 or "|" not in line or not DELIM.match(line) or "|" not in lines[n - 1]:
            n += 1
            continue
        want = cell_count(lines[n - 1])
        # 표의 행은 구분선 다음 줄부터 빈 줄(또는 코드펜스·파일 끝)까지 — GFM 이 표로 삼는 범위
        r = n + 1
        while r < len(lines) and lines[r].strip() and not lines[r].lstrip().startswith("```"):
            got = cell_count(lines[r])
            if got != want:
                out.append((r + 1, got, want, lines[r].strip()[:70]))
            r += 1
        n = r
    return out


def main() -> int:
    bad: list[str] = []
    torn: list[str] = []
    exempted = 0
    exempted_ragged = 0
    scanned = 0
    for path in sorted(ROOT.rglob("*.md")):
        if any(p in SKIP_DIRS or p.startswith(SKIP_PREFIXES) for p in path.parts):
            continue
        scanned += 1
        rel = path.relative_to(ROOT).as_posix()
        for line_no, above in hits(path):
            if rel in EXEMPT:
                exempted += 1
                continue
            bad.append(f"{rel}:{line_no} — the header row is glued to prose, so the table renders as "
                       f"text. Above it: {above!r}")
        for line_no, got, want, text in ragged(path):
            if rel in EXEMPT_RAGGED:
                exempted_ragged += 1
                continue
            verdict = "GFM 가 잘라내 안 보임" if got > want else "GFM 가 빈 칸으로 채움"
            torn.append(f"{rel}:{line_no} — cells={got} header={want} ({verdict}). Row: {text!r}")

    for b in bad:
        print(f"  [FAIL] 표가 산문에 붙어 렌더 안 됨 — {b}")
    for c in torn:
        print(f"  [FAIL] 행의 칸 수가 헤더와 다름 — {c}")
    if bad or torn:
        if bad:
            print(f"\n  빈 줄 하나면 됩니다. 표가 리스트 항목 안에 들여쓰여 있으면 빈 줄로도 안 되니 "
                  f"목록 밖으로 내어쓰십시오.")
        if torn:
            print(f"\n  칸 수를 헤더와 맞추십시오. 칸 구분이 아닌 파이프는 `\\|` 로 이스케이프합니다 — "
                  f"코드 스팬 안이라도 GFM 은 칸을 끊습니다. 행이 다음 줄로 넘어가 있으면 한 줄로 붙이십시오.")
        return 1
    print(f"  [PASS] 마크다운 표 렌더 — {scanned}개 파일, 산문에 붙은 표 0건, 칸 수 어긋난 행 0건 "
          f"(의도적 예외 {exempted + exempted_ragged}건: "
          f"{', '.join(sorted(set(EXEMPT) | set(EXEMPT_RAGGED))) if exempted + exempted_ragged else '없음'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
