# 논문 레퍼런스 일괄 링크화 — md 본문의 bibcode/arXiv id를 ADS/arXiv 마크다운 링크로 변환.
# one-shot: CONVENTIONS §3.3 retrofit (2026-07-20 오너 지시), 이후 신규 문서는 작성 시 준수
"""Retrofit bare paper ids in md narrative into markdown links (CONVENTIONS §3.3).

Safety model:
- arXiv ids are converted ONLY when whitelisted — id appears in
  docs/phase3/_bib/*.yaml `arxiv_id:` values, OR is written with an explicit
  `arXiv:` prefix at the use site. Bare number-like tokens never convert.
- bibcodes match the strict 19-char ADS form.
- Skipped contexts: fenced code blocks, inline backtick spans, YAML
  frontmatter, lines that are YAML machine fields (`arxiv_id:`, `bibcode:`),
  ids already inside a markdown link.

Targets: *.md under docs/ plans/ phase2/ phase3/ phase4/ ko/ (excluding
docs/wiki renders and _papers cache). Run with --dry for a report only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
ROOTS = ["docs", "plans", "phase2", "phase3", "phase4", "gameplay", "ko"]
EXCLUDE_PARTS = {"wiki", "_papers", "node_modules"}

BIB = re.compile(r"\b((?:1[89]|20)\d{2}[A-Za-z&][A-Za-z&.]{4}[A-Za-z0-9&.]{8}[A-Z])\b")
ARX_PREFIXED = re.compile(r"\barXiv:\s?(\d{4}\.\d{4,5})(v\d+)?\b")
ARX_BARE = re.compile(r"\b(\d{4}\.\d{4,5})(v\d+)?\b")
MACHINE_LINE = re.compile(r"^\s*(arxiv_id|bibcode|doi)\s*:")


def load_whitelist() -> set[str]:
    ids: set[str] = set()
    for f in (REPO / "docs" / "phase3" / "_bib").glob("*.yaml"):
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                v = node.get("arxiv_id")
                if isinstance(v, str):
                    ids.add(v)
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    return ids


def split_protected(line: str) -> list[tuple[bool, str]]:
    """Split a line into (protected, text) spans: backtick code + existing links protected."""
    spans: list[tuple[bool, str]] = []
    pattern = re.compile(r"(`[^`]*`|\[[^\]]*\]\([^)]*\))")
    pos = 0
    for m in pattern.finditer(line):
        if m.start() > pos:
            spans.append((False, line[pos:m.start()]))
        spans.append((True, m.group(0)))
        pos = m.end()
    if pos < len(line):
        spans.append((False, line[pos:]))
    return spans


def convert_text(text: str, whitelist: set[str]) -> tuple[str, int]:
    n = 0

    def bib_sub(m: re.Match) -> str:
        nonlocal n
        n += 1
        return f"[{m.group(1)}](https://ui.adsabs.harvard.edu/abs/{m.group(1)})"

    def arx_pref_sub(m: re.Match) -> str:
        nonlocal n
        n += 1
        full = m.group(1) + (m.group(2) or "")
        return f"[arXiv:{full}](https://arxiv.org/abs/{m.group(1)})"

    def arx_bare_sub(m: re.Match) -> str:
        nonlocal n
        if m.group(1) not in whitelist:
            return m.group(0)
        n += 1
        return f"[{m.group(0)}](https://arxiv.org/abs/{m.group(1)})"

    out_lines = []
    in_fence = False
    in_frontmatter = False
    for i, line in enumerate(text.splitlines(keepends=True)):
        stripped = line.strip()
        if i == 0 and stripped == "---":
            in_frontmatter = True
            out_lines.append(line)
            continue
        if in_frontmatter:
            out_lines.append(line)
            if stripped == "---":
                in_frontmatter = False
            continue
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence or MACHINE_LINE.match(line):
            out_lines.append(line)
            continue
        # apply each pattern in its own pass, re-protecting between passes so
        # a link created by pass N is opaque to pass N+1 (no nested links)
        for regex, sub in ((BIB, bib_sub), (ARX_PREFIXED, arx_pref_sub), (ARX_BARE, arx_bare_sub)):
            rebuilt = ""
            for protected, span in split_protected(line):
                rebuilt += span if protected else regex.sub(sub, span)
            line = rebuilt
        out_lines.append(line)
    return "".join(out_lines), n


def main() -> None:
    dry = "--dry" in sys.argv
    whitelist = load_whitelist()
    print(f"whitelist: {len(whitelist)} arXiv ids from _bib")
    total_files = total_links = 0
    targets = [REPO / "README.md", REPO / "CONVENTIONS.md"]  # reader-facing root docs
    for root in ROOTS:
        targets.extend(sorted((REPO / root).rglob("*.md")))
    for p in targets:
        if EXCLUDE_PARTS & set(p.parts) or not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        new, n = convert_text(text, whitelist)
        if n:
            total_files += 1
            total_links += n
            if not dry:
                p.write_text(new, encoding="utf-8")
            print(f"  {p.relative_to(REPO)}: {n}")
    print(f"{'DRY: ' if dry else ''}{total_links} links in {total_files} files")


if __name__ == "__main__":
    main()
