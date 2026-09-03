# 논문 캐시의 .md 렌더가 .html 렌더의 표를 떨어뜨린 자리를 보고한다 — 재확인 목록이지 결함 목록이 아니다 (Brief 48)
"""Report where a cached paper's .md render lost a table the .html render has. Report only; never a gate.

    python3 scripts/check_paper_tables.py            # papers cited in engine/ and docs/reference/
    python3 scripts/check_paper_tables.py --all      # every cached paper with both renders
    python3 scripts/check_paper_tables.py --cache DIR

⚠ READ THIS FIRST: every row below is a place to ASK which render a value was read from. It is not a
defect. Measured 2026-09-03: Seager+ 2007 (0707.2895) lost the body of Table 1 in its .md while keeping
the caption, and every value eos.py takes from that table is nonetheless correct — it was read from the
.html or the PDF. The list says where to look; it never says a number is wrong.

Two signals, because one is not enough:
1. caption parity — captioned tables ("Table N:" / "Table N.") present in the .html and absent from the
   .md. Catches total losses (the .md of 2203.01065 has none of RM22's ten tables).
2. numeric density — for a table captioned in BOTH renders, the count of numeric tokens in a window after
   the caption; when the .html window has many and the .md window has almost none, the body is gone while
   the caption survived (the Seager case). Rough by construction: the window is fixed, the threshold is a
   declaration (below), and prose numbers count. Locations, not verdicts.

Why it is not in check.sh: it needs both renders of a gitignored cache that a checkout may not have —
a gate that depends on a directory that may be absent is the --fast fingerprint lesson.
"""
from __future__ import annotations

import glob
import html
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(REPO, "docs", "phase3", "_papers")
WINDOW = 4000          # characters after the caption to count numbers in
MD_HTML_RATIO = 0.25   # declared: md window has under a quarter of the html window's numbers → body likely gone
MIN_HTML_NUMBERS = 12  # declared: below this the html window is not table-like enough to judge

CAPTION = re.compile(r"\bTable\s+(\d{1,2})\s*[:.]")
NUMBER = re.compile(r"(?<![\w.])[-−]?\d+(?:\.\d+)?(?:\s*[×x]\s*10|e[-−]?\d+)?")


def cited_ids(repo: str) -> set[str]:
    ids: set[str] = set()
    for pattern in ("engine/*.py", "engine/*.md", "docs/reference/*.md"):
        for f in glob.glob(os.path.join(repo, pattern)):
            t = open(f, encoding="utf-8", errors="ignore").read()
            ids.update(re.findall(r"(?:arXiv:?\s*|arxiv\.org/abs/)(\d{4}\.\d{4,5})", t))
            ids.update(re.findall(r"(?:arXiv:?\s*|arxiv\.org/abs/)(astro-ph/\d{7})", t))
    return ids


def strip_html(t: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def captions(t: str) -> dict[int, int]:
    """table number → position of its first caption."""
    out: dict[int, int] = {}
    for m in CAPTION.finditer(t):
        out.setdefault(int(m.group(1)), m.end())
    return out


def numbers_after(t: str, pos: int) -> int:
    return len(NUMBER.findall(t[pos:pos + WINDOW]))


def report(cache: str, ids: set[str] | None) -> int:
    rows: list[tuple[str, str]] = []
    papers = 0
    for md_path in sorted(glob.glob(os.path.join(cache, "*.md"))):
        base = os.path.basename(md_path)[:-3]
        if ids is not None and base.replace("_", "/") not in ids and base not in ids:
            continue
        html_path = md_path[:-3] + ".html"
        if not os.path.exists(html_path):
            continue
        papers += 1
        md = re.sub(r"\s+", " ", open(md_path, encoding="utf-8", errors="ignore").read())
        ht = strip_html(open(html_path, encoding="utf-8", errors="ignore").read())
        cm, ch = captions(md), captions(ht)
        lost = sorted(set(ch) - set(cm))
        if lost:
            rows.append((base, f"caption missing in .md: Table {', '.join(map(str, lost))}"))
        hollow = []
        for n in sorted(set(cm) & set(ch)):
            n_html, n_md = numbers_after(ht, ch[n]), numbers_after(md, cm[n])
            if n_html >= MIN_HTML_NUMBERS and n_md < MD_HTML_RATIO * n_html:
                hollow.append(f"{n} ({n_md}/{n_html} numbers)")
        if hollow:
            rows.append((base, f"caption kept, body likely gone in .md: Table {'; '.join(hollow)}"))
    print(__doc__.split("\n\n")[1])
    print(f"\ncache {cache} · papers with both renders{' (cited only)' if ids is not None else ''}: {papers} · "
          f"rows: {len(rows)} (re-check list, not defects)")
    for base, what in rows:
        print(f"  {base:24s} {what}")
    return 0


def main(argv: list[str]) -> int:
    cache = CACHE
    if "--cache" in argv:
        cache = argv[argv.index("--cache") + 1]
    if not os.path.isdir(cache):
        print(f"  [SKIP] paper cache not present at {cache} — nothing to compare (this is not a failure)")
        return 0
    ids = None if "--all" in argv else cited_ids(REPO)
    return report(cache, ids)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
