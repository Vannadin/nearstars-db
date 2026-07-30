#!/usr/bin/env python3
# 방법론 문서(docs/reference + ko 미러)의 bibcode/arXiv 인용이 전부 클릭 가능한 링크인지 검사하는 게이트
"""Fail if a bibcode or arXiv ID appears in docs/reference (or its ko mirror)
without being wrapped in a markdown link.

Convention (feedback_citation_links): every citation is clickable —
[`<bibcode>`](https://ui.adsabs.harvard.edu/abs/<bibcode, & → %26>).

Skipped contexts: fenced code blocks (cfg/YAML/JSON examples may carry
placeholder or literal bibcodes), existing markdown links, raw URLs, and
bibcodes embedded in longer inline-code spans (field examples).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC_DIRS = [ROOT / "docs" / "reference", ROOT / "ko" / "docs" / "reference"]

BIBCODE = re.compile(r"[12][0-9]{3}[A-Za-z&.]{5}[0-9.]{4}[A-Z.][0-9.A-Z]{4}[A-Z]")
ARXIV = re.compile(r"arXiv:\s?[0-9]{4}\.[0-9]{4,5}")


def fence_spans(text):
    spans = []
    opens = list(re.finditer(r"^(```+|~~~+)", text, re.M))
    i = 0
    while i < len(opens) - 1:
        spans.append((opens[i].start(), opens[i + 1].end()))
        i += 2
    if len(opens) % 2 == 1:
        spans.append((opens[-1].start(), len(text)))
    return spans


def skip_spans(text):
    spans = fence_spans(text)
    for m in re.finditer(r"\[[^\]\n]*\]\([^)\n]*\)", text):
        spans.append((m.start(), m.end()))
    for m in re.finditer(r"https?://[^\s)\]>]+", text):
        spans.append((m.start(), m.end()))
    return spans


def main():
    bad = []
    for doc_dir in DOC_DIRS:
        for path in sorted(doc_dir.glob("*.md")):
            text = path.read_text()
            spans = skip_spans(text)
            inline_codes = list(re.finditer(r"`[^`\n]+`", text))
            for pat in (BIBCODE, ARXIV):
                for m in pat.finditer(text):
                    if any(s <= m.start() < e for s, e in spans):
                        continue
                    host = next(
                        (c for c in inline_codes if c.start() <= m.start() and m.end() <= c.end()),
                        None,
                    )
                    if host is not None and host.group(0) != f"`{m.group(0)}`":
                        continue  # part of a longer code example
                    line = text.count("\n", 0, m.start()) + 1
                    bad.append(f"{path.relative_to(ROOT)}:{line}: unlinked citation {m.group(0)}")
    if bad:
        for b in bad:
            print(f"  [FAIL] {b}")
        print(f"  {len(bad)} unlinked citation(s) — wrap as [`<bibcode>`](https://ui.adsabs.harvard.edu/abs/<bibcode, & → %26>)")
        return 1
    print("  [PASS] docs/reference 인용 링크 전부 클릭 가능")
    return 0


if __name__ == "__main__":
    sys.exit(main())
