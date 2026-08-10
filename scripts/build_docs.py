# reference/plans 산문 문서를 GitHub 스타일 HTML 뷰어로 빌드 (preview-md.sh + 한/영 토글 + 사이드바)
"""Build a sidebar-navigated static doc site, matching the local preview viewer.

This mirrors scripts/preview-md.sh exactly: client-side rendering via
**marked.js** (GitHub-flavored markdown) styled with **github-markdown-css**.
It deliberately does NOT pull in the DB site's design (style.css) — that
broke tables and re-skinned the docs. The only additions over the local
preview are a 한/EN toggle and a left sidebar.

Covers docs/reference/*.md (+ ko/ mirrors) and plans/*.md (+ ko/plans/
mirrors). Each page embeds the raw markdown for each available language
and marked renders the selected one client-side — no server-side parser,
so every GFM feature (tables included) renders correctly.

Outputs under docs/wiki/:
  - index.html                 # docs hub
  - reference__<slug>.html
  - plans__<slug>.html

Usage: python3 scripts/build_docs.py

Internal *.md links are rewritten to the generated page when the target
is one of the built docs.
"""

from __future__ import annotations

import html
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'pipeline'))
from _nav import global_bar  # noqa: E402
BAR = global_bar('../', 'Wiki')

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / 'docs' / 'wiki'

# vendored locally (docs/assets/) — marked@12.0.2 / github-markdown-css@5.5.0 (v2 dark)
MARKED = '../assets/marked.min.js'
GH_CSS = '../assets/github-markdown-dark.min.css'
GH_BLOB = 'https://github.com/Vannadin/nearstars-db/blob/main/'

# slug → output filename, filled by collect_docs(); used to rewrite links.
_LINK_MAP: dict[str, str] = {}

_FRONTMATTER_RE = re.compile(r'^---\n.*?\n---\n+', re.DOTALL)
_FULL_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def _strip_frontmatter(md: str) -> tuple[str, str]:
    """Drop a leading YAML frontmatter block; return (body, title_from_fm)."""
    title = ''
    m = _FRONTMATTER_RE.match(md)
    if m:
        fm = m.group(0)
        tm = re.search(r'^title:\s*(.+)$', fm, re.MULTILINE)
        if tm:
            title = tm.group(1).strip()
        md = md[m.end():]
    return md, title


def _rewrite_links(md: str, src_dir: Path) -> str:
    """Rewrite internal links for the docs/wiki/ page context.

    - internal .md that maps to a built wiki page → point at it.
    - other relative repo targets → re-resolve from the source md's
      directory. Inside docs/ → re-express relative to docs/wiki/ (the
      page the reader is on; a source-relative ../../../docs/x.html is
      valid in the repo file view but escapes the site root from wiki/).
      Outside docs/ but in the repo (scripts, LICENSE, phase3/…) → the
      GitHub blob URL. Nonexistent → drop to plain text (no 404 on site).
    """
    docs_root = (REPO / 'docs').resolve()
    wiki_dir = docs_root / 'wiki'

    def repl(m):
        text, target = m.group(1), m.group(2)
        if target.startswith(('http://', 'https://', '#', 'mailto:', '/')):
            return m.group(0)
        base, _, anchor = target.partition('#')
        suffix = ('#' + anchor) if anchor else ''
        if base.endswith('.md'):
            out = _LINK_MAP.get(Path(base).stem)
            if out:
                return f'[{text}]({out}{suffix})'
            return text  # unbuilt internal .md → de-link
        resolved = (src_dir / base).resolve()
        if not resolved.exists():
            return m.group(0) if not base.endswith('.html') else text
        if resolved.is_relative_to(docs_root):
            rel = os.path.relpath(resolved, wiki_dir)
            return f'[{text}]({rel}{suffix})'
        if resolved.is_relative_to(REPO):
            rel = resolved.relative_to(REPO).as_posix()
            return f'[{text}]({GH_BLOB}{rel}{suffix})'
        return text  # outside the repo → de-link
    return _FULL_LINK_RE.sub(repl, md)


def _first_h1(md: str) -> str:
    for ln in md.splitlines():
        if ln.startswith('# '):
            return ln[2:].strip()
    return ''


def _prep(md_path: Path) -> tuple[str, str]:
    """Read a markdown file → (rendered-ready markdown, title)."""
    raw = md_path.read_text(encoding='utf-8')
    body, fm_title = _strip_frontmatter(raw)
    body = _rewrite_links(body, md_path.parent)
    title = fm_title or _first_h1(body) or md_path.stem
    return body, title


def _embed(md: str) -> str:
    """Escape a markdown string for embedding in a <script> block."""
    return md.replace('</script>', '<\\/script>')


# ── doc discovery ────────────────────────────────────────────────────────────
def collect_docs() -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {'reference': [], 'plans': []}

    for md in sorted((REPO / 'docs' / 'reference').glob('*.md')):
        slug = md.stem
        ko = REPO / 'ko' / 'docs' / 'reference' / f'{slug}.md'
        out = f'reference__{slug}.html'
        _LINK_MAP[slug] = out
        groups['reference'].append({'slug': slug, 'out': out, 'en': md,
                                    'ko': ko if ko.exists() else None})

    for md in sorted((REPO / 'plans').glob('*.md')):
        if md.stem in {'_template', 'README'}:
            continue
        slug = md.stem
        ko = REPO / 'ko' / 'plans' / f'{slug}.md'
        out = f'plans__{slug}.html'
        _LINK_MAP[slug] = out
        groups['plans'].append({'slug': slug, 'out': out, 'en': md,
                                'ko': ko if ko.exists() else None})

    return groups


# ── templating ───────────────────────────────────────────────────────────────
def sidebar_html(groups: dict[str, list[dict]], active: str) -> str:
    rows = [
        '<nav class="side">',
        '<a class="brand" href="index.html">NearStars <span>docs</span></a>',
        '<a class="nav-x" href="https://github.com/Vannadin/nearstars-db/wiki" target="_blank" rel="noopener">↗ GitHub wiki</a>',
    ]
    labels = {'reference': 'Reference', 'plans': 'Plans'}
    for g in ('reference', 'plans'):
        rows.append(f'<div class="nav-grp">{labels[g]}</div>')
        for d in groups[g]:
            cls = 'nav-i on' if d['out'] == active else 'nav-i'
            rows.append(f'<a class="{cls}" href="{d["out"]}">{html.escape(d["title"])}</a>')
    rows.append('</nav>')
    return '\n'.join(rows)


_CSS = """
:root { --side-w: 256px }
* { box-sizing: border-box }
body { margin: 0;
  background:
    radial-gradient(60% 50% at 18% -10%, rgba(122,168,255,.07), transparent 70%),
    radial-gradient(50% 45% at 92% 110%, rgba(224,144,208,.05), transparent 70%),
    #06070a;
  background-attachment: fixed; color: rgba(255,255,255,.80);
  font-family: 'Geist', 'Inter', system-ui, -apple-system, "Apple SD Gothic Neo", "Noto Sans KR", sans-serif }
.layout { display: flex; align-items: flex-start; min-height: 100vh }
.side { width: var(--side-w); flex: 0 0 var(--side-w); position: sticky; top: 0; height: 100vh;
  overflow-y: auto; border-right: 1px solid rgba(255,255,255,.07); background: rgba(255,255,255,.014);
  padding: 16px 12px; font-size: 13px }
.side .brand { display: block; font-weight: 700; font-size: 15px; color: rgba(255,255,255,.94);
  text-decoration: none; margin: 2px 6px 14px }
.side .brand span { color: rgba(255,255,255,.40); font-weight: 600 }
.side .nav-grp { text-transform: uppercase; font-size: 10px; letter-spacing: .6px; color: rgba(255,255,255,.36);
  margin: 16px 6px 4px; font-weight: 700 }
.side a { display: block; text-decoration: none; color: rgba(255,255,255,.72); padding: 5px 8px;
  border-radius: 6px; line-height: 1.4 }
.side a:hover { background: rgba(255,255,255,.05) }
.side a.on { background: rgba(122,168,255,.18); color: #aac8ff; font-weight: 600 }
.side a.nav-x { color: rgba(255,255,255,.50) }
.content-wrap { flex: 1; min-width: 0; padding: 0 16px }
.topbar { max-width: 980px; margin: 0 auto; padding: 16px 45px 0; display: flex; justify-content: flex-end }
@media (max-width: 767px) { .topbar { padding: 12px 15px 0 } }
.lang-only { color: rgba(255,255,255,.36); font-size: 12px }
.markdown-body { box-sizing: border-box; min-width: 200px; max-width: 980px; margin: 0 auto;
  padding: 24px 45px 60px; background: transparent !important }
@media (max-width: 767px) { .markdown-body { padding: 15px } }
.markdown-body table { display: table; width: 100% }
.markdown-body blockquote { color: #7aa8ff; border-left-color: #7aa8ff; background: rgba(122,168,255,.08);
  padding: 8px 16px; border-radius: 4px }
.markdown-body h1 { border-bottom: 2px solid rgba(255,255,255,.09) }
.markdown-body h2 { border-bottom: 1px solid rgba(255,255,255,.09); margin-top: 28px }
.markdown-body a { color: #7aa8ff }
.markdown-body code { color: rgba(255,255,255,.86) }
@media (max-width: 767px) {
  .layout { flex-direction: column }
  .side { width: auto; flex: none; height: auto; position: static;
    border-right: none; border-bottom: 1px solid rgba(255,255,255,.09) }
}
"""

def page_html(title: str, sidebar: str, en_md: str, ko_md: str | None) -> str:
    bilingual = ko_md is not None
    if bilingual:
        toggle = ('<div class="seg" id="lang-seg">'
                  '<button data-lang="ko">한</button>'
                  '<button data-lang="en">EN</button></div>')
        ko_block = f'<script type="text/markdown" id="md-ko">{_embed(ko_md)}</script>'
    else:
        toggle = '<span class="lang-only">EN only</span>'
        ko_block = ''
    en_block = f'<script type="text/markdown" id="md-en">{_embed(en_md)}</script>'

    return f'''<!DOCTYPE html>
<!-- autogenerated by scripts/build_docs.py — do not edit by hand -->
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} · NearStars docs</title>
<link rel="stylesheet" href="../assets/fonts/geist.css">
<link rel="stylesheet" href="{GH_CSS}">
<script src="{MARKED}"></script>
<style>{_CSS}</style>
</head>
<body>
{BAR}
<div class="layout">
{sidebar}
<div class="content-wrap">
  <div class="topbar">{toggle}</div>
  <article class="markdown-body" id="content"></article>
</div>
</div>
{en_block}
{ko_block}
<script>
const srcs = {{}};
const en = document.getElementById('md-en'); if (en) srcs.en = en.textContent;
const ko = document.getElementById('md-ko'); if (ko) srcs.ko = ko.textContent;
const content = document.getElementById('content');
function render(l) {{
  if (!srcs[l]) l = srcs.ko ? 'ko' : 'en';
  document.documentElement.lang = l;
  content.innerHTML = marked.parse(srcs[l], {{ gfm: true, breaks: false }});
  const seg = document.getElementById('lang-seg');
  if (seg) seg.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.lang === l));
}}
let lang = localStorage.getItem('nearstars-lang') || 'en';
render(lang);
const seg = document.getElementById('lang-seg');
if (seg) seg.addEventListener('click', e => {{
  const b = e.target.closest('button[data-lang]'); if (!b) return;
  lang = b.dataset.lang; localStorage.setItem('nearstars-lang', lang); render(lang);
}});
</script>
</body>
</html>
'''


def build() -> None:
    groups = collect_docs()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # pass 1: prep markdown + titles (sidebar needs every title)
    for g in groups.values():
        for d in g:
            d['en_md'], d['title'] = _prep(d['en'])
            d['ko_md'] = _prep(d['ko'])[0] if d['ko'] else None

    # pass 2: emit pages
    count = 0
    for g in groups.values():
        for d in g:
            sb = sidebar_html(groups, active=d['out'])
            (OUT_DIR / d['out']).write_text(
                page_html(d['title'], sb, d['en_md'], d['ko_md']), encoding='utf-8')
            count += 1

    # hub
    hub_en = ('# NearStars documentation\n\n'
              'Reference docs and planning notes for the NearStars KSP planet pack. '
              'Reference docs and mirrored plans carry a 한/EN toggle. '
              'Pick a page from the sidebar.\n')
    hub_ko = ('# NearStars 문서\n\n'
              'NearStars KSP 행성팩의 레퍼런스 문서와 기획 노트입니다. '
              '레퍼런스 문서와 미러된 기획 노트에는 한/EN 토글이 있습니다. '
              '왼쪽 사이드바에서 페이지를 고르세요.\n')
    (OUT_DIR / 'index.html').write_text(
        page_html('Docs', sidebar_html(groups, active='index.html'), hub_en, hub_ko),
        encoding='utf-8')

    print(f'build_docs: wrote {count} doc pages + hub → {OUT_DIR.relative_to(REPO)}/')


if __name__ == '__main__':
    build()
