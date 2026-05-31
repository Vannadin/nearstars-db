# reference/plans 산문 문서를 사이드바 달린 정적 HTML 위키로 빌드 (en/ko 통짜 토글)
"""Build a sidebar-navigated static doc site from the prose docs.

Covers docs/reference/*.md (with ko/ mirrors → 한/EN toggle) and
plans/*.md (English only). Unlike scripts/phase3/build_html.py, this
renders each language **whole** and toggles visibility, so it needs no
block-level en/ko parity — robust for hand-written prose that drifts.

Outputs under docs/wiki/:
  - index.html                         # docs hub (sidebar landing)
  - reference__<slug>.html             # one page per reference doc
  - plans__<slug>.html                 # one page per plans doc

Usage: python3 scripts/build_docs.py      (builds everything)

Self-contained markdown subset: frontmatter strip, ATX headings, hr,
fenced code, blockquotes, bullet + ordered lists (one nesting level),
pipe tables, paragraphs, inline bold/italic/code/links. No images.
Internal `*.md` links are rewritten to the generated page when the
target is one of the built docs.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / 'docs' / 'wiki'

# ── inline markdown (mirrors scripts/phase3/build_html.py) ──────────────────
_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
_INLINE_CODE_RE = re.compile(r'`([^`]+)`')
_BOLD_RE = re.compile(r'\*\*([^*]+)\*\*')
_ITALIC_RE = re.compile(r'(?<!\*)\*([^*]+)\*(?!\*)')

# slug → output filename, filled by collect_docs(); used to rewrite links.
_LINK_MAP: dict[str, str] = {}


def _rewrite_target(target: str) -> str:
    """Rewrite an internal *.md link to its generated page, else leave it."""
    if target.startswith(('http://', 'https://', '#', 'mailto:')):
        return target
    # strip any anchor, take the basename without .md
    base = target.split('#', 1)[0]
    if not base.endswith('.md'):
        return target
    slug = Path(base).stem
    return _LINK_MAP.get(slug, target)


def inline_md(text: str) -> str:
    out = html.escape(text)
    out = _LINK_RE.sub(lambda m: f'<a href="{html.escape(_rewrite_target(m.group(2)), quote=True)}">{m.group(1)}</a>', out)
    out = _INLINE_CODE_RE.sub(lambda m: f'<code>{m.group(1)}</code>', out)
    out = _BOLD_RE.sub(lambda m: f'<b>{m.group(1)}</b>', out)
    out = _ITALIC_RE.sub(lambda m: f'<i>{m.group(1)}</i>', out)
    return out


# ── block parser → HTML ─────────────────────────────────────────────────────
_HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*$')
_TABLE_SEP_RE = re.compile(r'^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$')
_BULLET_RE = re.compile(r'^(\s*)[-*]\s+(.+)$')
_ORDERED_RE = re.compile(r'^(\s*)\d+\.\s+(.+)$')
_FENCE_RE = re.compile(r'^```(\w*)\s*$')
_HR_RE = re.compile(r'^---+\s*$')


def _split_table_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip('|').split('|')]


def _strip_frontmatter(lines: list[str]) -> tuple[list[str], dict[str, str]]:
    """If the doc opens with a --- fence, pull it off and parse simple keys."""
    meta: dict[str, str] = {}
    if lines and lines[0].strip() == '---':
        i = 1
        while i < len(lines) and lines[i].strip() != '---':
            if ':' in lines[i]:
                k, _, v = lines[i].partition(':')
                meta[k.strip()] = v.strip()
            i += 1
        return lines[i + 1:], meta
    return lines, meta


def _render_list(lines: list[str], i: int, ordered: bool) -> tuple[str, int]:
    """Render a (possibly one-level-nested) list starting at line i."""
    tag = 'ol' if ordered else 'ul'
    rx = _ORDERED_RE if ordered else _BULLET_RE
    out = [f'<{tag}>']
    while i < len(lines):
        m = rx.match(lines[i])
        if not m:
            # allow the other list type at the same spot to break out cleanly
            break
        indent = len(m.group(1))
        if indent >= 2:
            # nested item belongs to a sublist — handled by recursion below;
            # if we reach here at top level it's malformed, treat as flat.
            pass
        item_html = inline_md(m.group(2))
        i += 1
        # gather wrapped continuation lines (indented, non-blank, non-list)
        cont = []
        sub_html = ''
        while i < len(lines):
            nxt = lines[i]
            if nxt.strip() == '':
                break
            bm, om = _BULLET_RE.match(nxt), _ORDERED_RE.match(nxt)
            if bm and len(bm.group(1)) >= 2:
                sub_html, i = _render_list(lines, i, ordered=False)
                continue
            if om and len(om.group(1)) >= 2:
                sub_html, i = _render_list(lines, i, ordered=True)
                continue
            if bm or om:
                break
            if not nxt.startswith('  '):
                break
            cont.append(nxt.strip())
            i += 1
        if cont:
            item_html += ' ' + inline_md(' '.join(cont))
        out.append(f'<li>{item_html}{sub_html}</li>')
    out.append(f'</{tag}>')
    return ''.join(out), i


def md_to_html(text: str) -> tuple[str, str]:
    """Render a whole markdown doc → (body_html, title). Title = first H1."""
    lines = text.replace('\r', '').split('\n')
    lines, meta = _strip_frontmatter(lines)
    title = meta.get('title', '')
    parts: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        m = _HEADING_RE.match(line)
        if m:
            level = len(m.group(1))
            txt = m.group(2)
            if level == 1 and not title:
                title = txt
                i += 1
                continue
            parts.append(f'<h{level}>{inline_md(txt)}</h{level}>')
            i += 1
            continue

        if _HR_RE.match(line):
            parts.append('<hr>')
            i += 1
            continue

        m = _FENCE_RE.match(line)
        if m:
            lang = m.group(1)
            body = []
            i += 1
            while i < n and not _FENCE_RE.match(lines[i]):
                body.append(lines[i])
                i += 1
            i += 1
            cls = f' class="lang-{lang}"' if lang else ''
            parts.append(f'<pre><code{cls}>{html.escape(chr(10).join(body))}</code></pre>')
            continue

        if stripped.startswith('>'):
            quote = []
            while i < n and lines[i].strip().startswith('>'):
                quote.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            inner = inline_md(' '.join(q.strip() for q in quote if q.strip()))
            parts.append(f'<blockquote>{inner}</blockquote>')
            continue

        if stripped.startswith('|') and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1]):
            header = _split_table_row(line)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(_split_table_row(lines[i]))
                i += 1
            thead = ''.join(f'<th>{inline_md(c)}</th>' for c in header)
            tbody = ''.join(
                '<tr>' + ''.join(f'<td>{inline_md(c)}</td>' for c in r) + '</tr>'
                for r in rows
            )
            parts.append(f'<div class="tbl"><table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div>')
            continue

        if _BULLET_RE.match(line):
            blk, i = _render_list(lines, i, ordered=False)
            parts.append(blk)
            continue
        if _ORDERED_RE.match(line):
            blk, i = _render_list(lines, i, ordered=True)
            parts.append(blk)
            continue

        # paragraph
        para = [line]
        i += 1
        while i < n:
            nxt = lines[i]
            ns = nxt.strip()
            if not ns or _HEADING_RE.match(nxt) or _HR_RE.match(nxt) or _FENCE_RE.match(nxt):
                break
            if ns.startswith('>') or _BULLET_RE.match(nxt) or _ORDERED_RE.match(nxt):
                break
            if ns.startswith('|') and i + 1 < n and _TABLE_SEP_RE.match(lines[i + 1]):
                break
            para.append(nxt)
            i += 1
        parts.append(f'<p>{inline_md(" ".join(p.strip() for p in para))}</p>')

    return '\n'.join(parts), (title or 'Untitled')


# ── doc discovery ────────────────────────────────────────────────────────────
def collect_docs() -> dict[str, list[dict]]:
    """Return {group: [ {slug, out, en_path, ko_path|None, title}, ... ]}."""
    groups: dict[str, list[dict]] = {'reference': [], 'plans': []}

    for md in sorted((REPO / 'docs' / 'reference').glob('*.md')):
        slug = md.stem
        ko = REPO / 'ko' / 'docs' / 'reference' / f'{slug}.md'
        out = f'reference__{slug}.html'
        _LINK_MAP[slug] = out
        groups['reference'].append(
            {'slug': slug, 'out': out, 'en': md, 'ko': ko if ko.exists() else None})

    for md in sorted((REPO / 'plans').glob('*.md')):
        if md.stem in {'_template', 'README'}:
            continue
        slug = md.stem
        ko = REPO / 'ko' / 'plans' / f'{slug}.md'
        out = f'plans__{slug}.html'
        _LINK_MAP[slug] = out
        groups['plans'].append({'slug': slug, 'out': out, 'en': md, 'ko': ko if ko.exists() else None})

    return groups


# ── page templating ──────────────────────────────────────────────────────────
def sidebar_html(groups: dict[str, list[dict]], active: str = '') -> str:
    rows = [
        '<nav class="side">',
        '<div class="brand">NearStars <span>docs</span></div>',
        '<a class="nav-x" href="../index.html">⌗ System database</a>',
        '<a class="nav-x" href="../reports.html">▤ Phase 2/3 reports</a>',
    ]
    labels = {'reference': 'Reference', 'plans': 'Plans'}
    for g in ('reference', 'plans'):
        rows.append(f'<div class="nav-grp">{labels[g]}</div>')
        for d in groups[g]:
            cls = 'nav-i on' if d['out'] == active else 'nav-i'
            rows.append(f'<a class="{cls}" href="{d["out"]}">{html.escape(d["title"])}</a>')
    rows.append('</nav>')
    return '\n'.join(rows)


_PAGE_CSS = """
:root { --side-w: 264px }
body { margin: 0 }
.layout { display: flex; min-height: 100vh }
.side { width: var(--side-w); flex: 0 0 var(--side-w); box-sizing: border-box;
  background: var(--bg-card-alt, #0c1119); border-right: 1px solid var(--bd-soft, #1a2434);
  padding: 18px 14px; position: sticky; top: 0; align-self: flex-start; height: 100vh;
  overflow-y: auto; font-size: 12.5px }
.side .brand { font-weight: 800; letter-spacing: .5px; font-size: 15px; margin: 2px 6px 16px;
  color: var(--fg-emph, #e6eef7) }
.side .brand span { color: var(--fg-dim, #6b7d93); font-weight: 600 }
.side .nav-grp { text-transform: uppercase; font-size: 9.5px; letter-spacing: .7px;
  color: var(--fg-dim, #6b7d93); margin: 16px 6px 5px; font-weight: 700 }
.side a { display: block; text-decoration: none; color: var(--fg, #b0c4d8);
  padding: 5px 8px; border-radius: 5px; line-height: 1.35 }
.side a:hover { background: var(--bg-input, #131c28); color: var(--fg-emph, #e6eef7) }
.side a.on { background: var(--accent-soft, #16314d); color: var(--fg-emph, #e6eef7); font-weight: 600 }
.side a.nav-x { color: var(--fg-dim, #8aa0b6) }
.docmain { flex: 1; min-width: 0; padding: 30px 42px 80px; max-width: 980px }
.docmain h1 { font-size: 26px; margin: 0 0 4px }
.docmain h2 { font-size: 19px; margin: 30px 0 10px; padding-bottom: 5px; border-bottom: 1px solid var(--bd-soft, #1a2434) }
.docmain h3 { font-size: 15px; margin: 20px 0 8px }
.docmain h4 { font-size: 13px; margin: 16px 0 6px; color: var(--fg-dim, #8aa0b6) }
.docmain p, .docmain li { font-size: 14px; line-height: 1.72 }
.docmain a { color: var(--accent, #5aa0ff) }
.docmain hr { border: none; border-top: 1px solid var(--bd-soft, #1a2434); margin: 26px 0 }
.docmain blockquote { margin: 12px 0; padding: 8px 16px; border-left: 3px solid var(--bd-strong, #2a3a50);
  background: var(--bg-card-alt, #0c1119); color: var(--fg-dim, #9fb3c8); border-radius: 0 5px 5px 0 }
.docmain pre { background: var(--bg-card-alt, #0c1119); border: 1px solid var(--bd-soft, #1a2434);
  border-radius: 5px; padding: 12px 14px; overflow-x: auto }
.docmain pre code { font-size: 12.5px; background: none; padding: 0 }
.docmain code { background: var(--bg-input, #131c28); padding: 1px 5px; border-radius: 3px;
  font-family: var(--mono, ui-monospace, monospace); font-size: 12.5px }
.tbl { overflow-x: auto; margin: 12px 0 }
.tbl table { border-collapse: collapse; font-size: 13px; width: 100% }
.tbl th { text-align: left; padding: 7px 11px; background: var(--bg-card-alt, #0c1119);
  border-bottom: 1px solid var(--bd-strong, #2a3a50); font-size: 11px; text-transform: uppercase;
  letter-spacing: .4px; color: var(--fg-dim, #8aa0b6) }
.tbl td { padding: 7px 11px; border-top: 1px solid var(--bd-soft, #1a2434); vertical-align: top; line-height: 1.55 }
.topbar { display: flex; align-items: center; gap: 12px; margin-bottom: 18px }
.lang-only { color: var(--fg-dim, #6b7d93); font-size: 11.5px }
.seg { display: inline-flex; border: 1px solid var(--bd-strong, #2a3a50); border-radius: 6px; overflow: hidden }
.seg button { background: var(--bg-input, #131c28); color: var(--fg-dim, #8aa0b6); border: none;
  padding: 4px 12px; cursor: pointer; font-size: 12px; font-family: inherit }
.seg button.on { background: var(--accent-soft, #16314d); color: var(--fg-emph, #e6eef7) }
@media (max-width: 760px) {
  .layout { flex-direction: column }
  .side { width: auto; flex: none; height: auto; position: static; border-right: none;
    border-bottom: 1px solid var(--bd-soft, #1a2434) }
  .docmain { padding: 20px 18px 60px }
}
"""


def page_html(title: str, sidebar: str, en_body: str, ko_body: str | None) -> str:
    bilingual = ko_body is not None
    if bilingual:
        toggle = ('<div class="seg" id="lang-seg">'
                  '<button class="on" data-lang="ko">한</button>'
                  '<button data-lang="en">EN</button></div>')
        bodies = (f'<div data-langbody="ko">{ko_body}</div>'
                  f'<div data-langbody="en" style="display:none">{en_body}</div>')
    else:
        toggle = '<span class="lang-only">EN only</span>'
        bodies = f'<div data-langbody="en">{en_body}</div>'

    script = """
const seg = document.getElementById('lang-seg');
if (seg) {
  function applyLang(l){
    document.documentElement.lang = l;
    document.querySelectorAll('[data-langbody]').forEach(d =>
      d.style.display = (d.dataset.langbody === l) ? '' : 'none');
    seg.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.lang === l));
  }
  let lang = localStorage.getItem('nearstars-lang') || 'ko';
  applyLang(lang);
  seg.addEventListener('click', e => {
    const b = e.target.closest('button[data-lang]'); if(!b) return;
    lang = b.dataset.lang; localStorage.setItem('nearstars-lang', lang); applyLang(lang);
  });
}
"""
    return f'''<!DOCTYPE html>
<!-- autogenerated by scripts/build_docs.py — do not edit by hand -->
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)} · NearStars docs</title>
<link rel="stylesheet" href="../style.css">
<style>{_PAGE_CSS}</style>
</head>
<body>
<div class="layout">
{sidebar}
<main class="docmain">
<div class="topbar">{toggle}</div>
{bodies}
</main>
</div>
<script>{script}</script>
</body>
</html>
'''


def build() -> None:
    groups = collect_docs()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # first pass: render bodies + titles (titles needed for the sidebar)
    for g in groups.values():
        for d in g:
            d['en_body'], d['title'] = md_to_html(d['en'].read_text(encoding='utf-8'))
            d['ko_body'] = (md_to_html(d['ko'].read_text(encoding='utf-8'))[0]
                            if d['ko'] else None)

    # second pass: emit pages (sidebar now has every title)
    count = 0
    for g in groups.values():
        for d in g:
            sb = sidebar_html(groups, active=d['out'])
            page = page_html(d['title'], sb, d['en_body'], d['ko_body'])
            (OUT_DIR / d['out']).write_text(page, encoding='utf-8')
            count += 1

    # hub landing
    intro_en = ('<h1>NearStars documentation</h1>'
                '<p>Reference docs and planning notes for the NearStars KSP planet pack. '
                'Reference docs carry a 한/EN toggle; planning notes are English only. '
                'Pick a page from the sidebar.</p>')
    intro_ko = ('<h1>NearStars 문서</h1>'
                '<p>NearStars KSP 행성팩의 레퍼런스 문서와 기획 노트입니다. '
                '레퍼런스 문서는 한/EN 토글이 있고, 기획 노트는 영어만 있습니다. '
                '왼쪽 사이드바에서 페이지를 고르세요.</p>')
    hub = page_html('Docs', sidebar_html(groups, active='index.html'), intro_en, intro_ko)
    (OUT_DIR / 'index.html').write_text(hub, encoding='utf-8')

    print(f'build_docs: wrote {count} doc pages + hub → {OUT_DIR.relative_to(REPO)}/')


if __name__ == '__main__':
    build()
