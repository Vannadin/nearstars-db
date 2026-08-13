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
GH_CSS_DARK = '../assets/github-markdown-dark.min.css'
GH_CSS_LIGHT = '../assets/github-markdown-light.min.css'
GH_BLOB = 'https://github.com/Vannadin/nearstars-db/blob/main/'

# slug → output filename, filled by collect_docs(); used to rewrite links.
_LINK_MAP: dict[str, str] = {}

_FRONTMATTER_RE = re.compile(r'^---\n.*?\n---\n+', re.DOTALL)
_FULL_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def _strip_frontmatter(md: str) -> tuple[str, str]:
    """Drop a leading YAML frontmatter block; return (body, title_from_fm).

    Repo convention puts a one-line Korean HTML comment on line 1 of every doc, so
    the frontmatter can sit just after it; skip past that comment before matching.
    """
    title = ''
    lead = ''
    cm = re.match(r'^<!--.*?-->\n', md, re.DOTALL)
    if cm:
        lead, md = cm.group(0), md[cm.end():]
    m = _FRONTMATTER_RE.match(md)
    if m:
        fm = m.group(0)
        tm = re.search(r'^title:\s*(.+)$', fm, re.MULTILINE)
        if tm:
            title = tm.group(1).strip()
        md = md[m.end():]
    return lead + md, title


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
# 사이드바 묶음 — 50개 넘는 reference 를 한 덩어리로 늘어놓지 않기 위한 분류.
# 파일명 규칙만 보고 나누므로 새 문서가 들어와도 자동으로 자리를 찾는다.
def _ref_group(slug: str) -> str:
    if slug.endswith('-methodology') or slug in {'planetary-dynamo-scaling',
                                                 'methodology', 'methodology-index',
                                                 'plasma-color-methodology-review'}:
        return 'methodology'
    if slug.startswith(('principia-', 'mod-', 'ksp-', 'planet-pack')) or slug in {
            'science-system', 'nearstars-plugin-grounding', 'body-tree-spec',
            'rex-data-comparison', 'solar-system-external-observer'}:
        return 'engine'
    if slug in {'data-sources', 'pipeline-contract', 'binary-epoch-pipeline',
                'adding_stars', 'site-map', 'tools', 'guideline', 'archive_issues'}:
        return 'pipeline'
    return 'reference'


def collect_docs() -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {'guide': [], 'methodology': [], 'engine': [],
                                     'pipeline': [], 'reference': [], 'plans': []}

    # docs/guide/ = 독자용 안내 문서(개요·설치·FAQ·항성계 소개…). reference 와 섞으면
    # _ref_group 이 파일명만 보고 'Reference' 로 분류해 실제 레퍼런스를 묻어버린다.
    for md in sorted((REPO / 'docs' / 'guide').glob('*.md')):
        slug = md.stem
        ko = REPO / 'ko' / 'docs' / 'guide' / f'{slug}.md'
        out = f'guide__{slug}.html'
        _LINK_MAP[slug] = out
        groups['guide'].append({'slug': slug, 'out': out, 'en': md,
                                'ko': ko if ko.exists() else None})

    for md in sorted((REPO / 'docs' / 'reference').glob('*.md')):
        slug = md.stem
        ko = REPO / 'ko' / 'docs' / 'reference' / f'{slug}.md'
        out = f'reference__{slug}.html'
        _LINK_MAP[slug] = out
        groups[_ref_group(slug)].append({'slug': slug, 'out': out, 'en': md,
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
        '<a class="nav-x" href="https://github.com/Vannadin/nearstars-db" target="_blank" rel="noopener">↗ Repository</a>',
    ]
    # 사이드바도 본문 토글을 따라간다 — 두 언어 제목을 함께 심고 CSS 가 html[lang] 로 고른다.
    # 문서 제목은 각 언어 파일의 H1 에서 오므로 별도 번역표가 없다(미러 없으면 양쪽 동일).
    labels = {'guide': ('Guide', '안내'), 'methodology': ('Methodology', '방법론'),
              'engine': ('Engine & mods', '엔진·모드'), 'pipeline': ('Pipeline & data', '파이프라인·데이터'),
              'reference': ('Reference', '레퍼런스'), 'plans': ('Plans', '기획')}

    def bi(en: str, ko: str) -> str:
        if en == ko:
            return html.escape(en)
        return (f'<span class="l-en">{html.escape(en)}</span>'
                f'<span class="l-ko">{html.escape(ko)}</span>')

    for g in ('guide', 'methodology', 'engine', 'pipeline', 'reference', 'plans'):
        rows.append(f'<div class="nav-grp">{bi(*labels[g])}</div>')
        for d in groups[g]:
            cls = 'nav-i on' if d['out'] == active else 'nav-i'
            rows.append(f'<a class="{cls}" href="{d["out"]}">'
                        f'{bi(d["title"], d.get("title_ko", d["title"]))}</a>')
    rows.append('</nav>')
    return '\n'.join(rows)


_CSS = """
:root { --side-w: 256px;
  --w-bg: #06070a;
  --w-grad:
    radial-gradient(60% 50% at 18% -10%, rgba(122,168,255,.07), transparent 70%),
    radial-gradient(50% 45% at 92% 110%, rgba(224,144,208,.05), transparent 70%);
  --w-fg1: rgba(255,255,255,.94); --w-fg2: rgba(255,255,255,.80);
  --w-fg3: rgba(255,255,255,.72); --w-fg4: rgba(255,255,255,.50);
  --w-s1: rgba(255,255,255,.014); --w-s2: rgba(255,255,255,.05);
  --w-bd: rgba(255,255,255,.07);
  --w-on-bg: rgba(122,168,255,.18); --w-on-fg: #aac8ff }
/* 라이트 테마 — 브라우저 설정을 따른다 (마크다운 본문은 github-markdown-light 가 담당) */
@media (prefers-color-scheme: light) {
  html.ns-light-ok {
    --w-bg: #f5f6fa;
    --w-grad:
      radial-gradient(58% 48% at 16% -12%, rgba(47,102,216,.07), transparent 70%),
      radial-gradient(48% 44% at 94% 108%, rgba(168,58,142,.05), transparent 70%);
    --w-fg1: rgba(9,12,22,.95); --w-fg2: rgba(9,12,22,.80);
    --w-fg3: rgba(9,12,22,.76); --w-fg4: rgba(9,12,22,.62);
    --w-s1: rgba(12,17,34,.022); --w-s2: rgba(12,17,34,.055);
    --w-bd: rgba(12,17,34,.10);
    --w-on-bg: rgba(17,78,221,.13); --w-on-fg: #0a3fb0 }
}
* { box-sizing: border-box }
body { margin: 0;
  background: var(--w-grad), var(--w-bg);
  background-attachment: fixed; color: var(--w-fg2);
  font-family: 'Geist', 'Inter', system-ui, -apple-system, "Apple SD Gothic Neo", "Noto Sans KR", sans-serif }
.layout { display: flex; align-items: flex-start; min-height: 100vh; min-height: 100dvh }
.side { width: var(--side-w); flex: 0 0 var(--side-w); position: sticky; top: 0; height: 100vh; height: 100dvh;
  overflow-y: auto; border-right: 1px solid var(--w-bd); background: var(--w-s1);
  padding: 16px 12px; font-size: 13px }
.side .brand { display: block; font-weight: 700; font-size: 15px; color: var(--w-fg1);
  text-decoration: none; margin: 2px 6px 14px }
.side .brand span { color: var(--w-fg4); font-weight: 600 }
.side .nav-grp { text-transform: uppercase; font-size: 11px; letter-spacing: .6px; color: var(--w-fg4);
  margin: 16px 6px 4px; font-weight: 700 }
.side a { display: block; text-decoration: none; color: var(--w-fg3); padding: 5px 8px;
  border-radius: 6px; line-height: 1.4 }
.side a:hover { background: var(--w-s2) }
.side a.on { background: var(--w-on-bg); color: var(--w-on-fg); font-weight: 600 }
.side a.nav-x { color: var(--w-fg4) }
/* 사이드바 언어 전환 — render() 가 html[lang] 을 세팅하므로 JS 없이 CSS 로 고른다.
   기본(lang 미설정) 은 영어, 한글 제목은 lang=ko 일 때만 나온다. */
.l-ko { display: none }
html[lang="ko"] .l-en { display: none }
html[lang="ko"] .l-ko { display: inline }
.content-wrap { flex: 1; min-width: 0; padding: 0 16px }
.topbar { max-width: 980px; margin: 0 auto; padding: 16px 45px 0; display: flex; justify-content: flex-end }
@media (max-width: 767px) { .topbar { padding: 12px 15px 0 } }
.lang-only { color: var(--w-fg4); font-size: 12px }
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
  /* 사이드바를 세로로 다 펼치면 문서 59개가 본문 앞을 막는다 → 자체 스크롤 영역으로 */
  .side { width: auto; flex: none; position: static; max-height: 42vh; overflow-y: auto;
    border-right: none; border-bottom: 1px solid var(--w-bd); padding: 10px 10px 12px }
  .side .brand { position: sticky; top: -10px; margin: 0 0 10px; padding: 8px 6px;
    background: var(--w-bg); z-index: 1 }
  .side a { min-height: 40px; display: flex; align-items: center; padding: 6px 10px }
  .side .nav-grp { margin: 14px 6px 2px }
  /* 본문 폭 고정: 넓은 표는 페이지가 아니라 표 자신이 스크롤한다 */
  .content-wrap { max-width: 100%; padding: 0 }
  .markdown-body { min-width: 0; max-width: 100% }
  .markdown-body table { display: block; width: 100%; max-width: 100%; overflow-x: auto }
  .markdown-body pre { overflow-x: auto }
  .topbar { max-width: 100% }
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
<html lang="ko" class="ns-light-ok">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} · NearStars docs</title>
<link rel="stylesheet" href="../assets/fonts/geist.css">
<link rel="stylesheet" href="{GH_CSS_DARK}" media="(prefers-color-scheme: dark)">
<link rel="stylesheet" href="{GH_CSS_LIGHT}" media="(prefers-color-scheme: light)">
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
            if d['ko']:
                d['ko_md'], ko_title = _prep(d['ko'])
                d['title_ko'] = ko_title or d['title']
            else:
                d['ko_md'], d['title_ko'] = None, d['title']   # 미러 없으면 양쪽 같은 제목

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
