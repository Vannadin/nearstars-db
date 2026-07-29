# docs/ 사이트 내부 링크(정적 href + 임베드 마크다운)의 404를 잡는 게이트
"""Check every site-internal link in the published docs/ tree.

GitHub Pages serves docs/ as the site root, so any relative link must
resolve to a file inside docs/. Two link surfaces are scanned:

1. static `href="..."` attributes in every docs/**/*.html
2. markdown links `[text](target)` inside embedded
   `<script type="text/markdown">` blocks (the wiki pages render these
   client-side, so a broken target never appears as a static href —
   the class of bug found on 2026-07-29)

Skipped: docs/phase3/_papers/ (archival mirrors of external pages),
external/mailto/anchor/data URLs, and JS-template hrefs (`${...}`).

Exit 0 if clean, 1 with a listing otherwise.
"""
from __future__ import annotations

import re
import sys
import urllib.parse
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / 'docs'

HREF_RE = re.compile(r'href="([^"#]+)(?:#[^"]*)?"')
MD_BLOCK_RE = re.compile(r'<script type="text/markdown"[^>]*>(.*?)</script>', re.S)
MD_LINK_RE = re.compile(r'\[[^\]]*\]\(([^)#\s]+)(?:#[^)\s]*)?\)')
SKIP_PREFIX = ('http://', 'https://', 'mailto:', 'javascript:', 'data:', 'tel:')


def _targets(page: Path) -> set[str]:
    text = page.read_text(encoding='utf-8', errors='replace')
    out = set(HREF_RE.findall(text))
    for block in MD_BLOCK_RE.findall(text):
        out.update(MD_LINK_RE.findall(block))
    return out


def main() -> int:
    broken: list[tuple[Path, str]] = []
    for page in sorted(DOCS.rglob('*.html')):
        if '_papers' in page.parts:
            continue
        for raw in sorted(_targets(page)):
            if raw.startswith(SKIP_PREFIX) or '${' in raw or raw.startswith('#'):
                continue
            target = (page.parent / urllib.parse.unquote(raw)).resolve()
            inside = target.is_relative_to(DOCS)
            if not inside or not target.exists():
                broken.append((page.relative_to(REPO), raw))
    if broken:
        for page, raw in broken:
            print(f"  [FAIL] {page}: dead site link → {raw}")
        print(f"  [FAIL] site-link gate: {len(broken)} dead link(s)")
        return 1
    print("  [PASS] site-link gate: docs/ internal links all resolve")
    return 0


if __name__ == '__main__':
    sys.exit(main())
