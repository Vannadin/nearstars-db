# Phase 3 마크다운(영문+ko/ 미러) → 단일 HTML 빌더 (한/영 토글 내장)
"""Build a Phase 3 web report from paired English + Korean markdown.

Usage:
    python3 scripts/phase3/build_html.py <slug>

For example, ``build_html.py trappist-1-d`` reads:
    docs/phase3/trappist-1-d.md          (English source of truth)
    ko/docs/phase3/trappist-1-d.md       (Korean mirror per AGENTS.md §2.1)

…and emits ``docs/phase3/trappist-1-d.html``: a single static page with
the synthesis content rendered bilingually, gated by a 한/EN segmented
toggle that flips an i18n dictionary embedded in the page.

Pairing rule: sections are matched by H2/H3 heading **order**, not text.
The two files must have the same H2/H3 structure or the build fails
loudly. Use ``scripts/check-mirrors.sh`` to catch staleness first.

Only the patterns actually used in Phase 3 synthesis files are parsed
(headings, paragraphs, tables, simple bullet lists, fenced code,
HTML comments). This is not a general markdown processor.
"""

from __future__ import annotations

import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# ── markdown → block tree ───────────────────────────────────────────────────

@dataclass
class Block:
    kind: str         # 'heading' | 'paragraph' | 'table' | 'list' | 'code' | 'comment'
    level: int = 0    # heading level (1-6) — 0 for non-heading
    text: str = ''    # heading text or paragraph/code raw text
    rows: list = field(default_factory=list)   # table: list of list[str]; first row is header
    items: list = field(default_factory=list)  # list: list[str]
    lang: str = ''    # code fence language


_HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*$')
_TABLE_SEP_RE = re.compile(r'^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?\s*$')
_LIST_RE = re.compile(r'^\s*[-*]\s+(.+)$')
_FENCE_RE = re.compile(r'^```(\w*)\s*$')
_HTML_COMMENT_RE = re.compile(r'<!--.*?-->', re.DOTALL)


def _split_table_row(line: str) -> list[str]:
    """| a | b | c |  →  ['a', 'b', 'c']"""
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    return cells


def parse_md(path: Path) -> list[Block]:
    text = path.read_text(encoding='utf-8')
    text = _HTML_COMMENT_RE.sub('', text)
    lines = text.split('\n')

    blocks: list[Block] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # heading
        m = _HEADING_RE.match(line)
        if m:
            blocks.append(Block(kind='heading', level=len(m.group(1)), text=m.group(2)))
            i += 1
            continue

        # fenced code
        m = _FENCE_RE.match(line)
        if m:
            lang = m.group(1)
            body = []
            i += 1
            while i < len(lines) and not _FENCE_RE.match(lines[i]):
                body.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            blocks.append(Block(kind='code', lang=lang, text='\n'.join(body)))
            continue

        # table — detect by next-line being separator
        if stripped.startswith('|') and i + 1 < len(lines) and _TABLE_SEP_RE.match(lines[i + 1]):
            header = _split_table_row(line)
            i += 2  # skip header + separator
            rows = [header]
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append(_split_table_row(lines[i]))
                i += 1
            blocks.append(Block(kind='table', rows=rows))
            continue

        # bullet list — consume bullets + their indented continuation lines
        if _LIST_RE.match(line):
            items = []
            while i < len(lines):
                m = _LIST_RE.match(lines[i])
                if not m:
                    break
                current = m.group(1)
                i += 1
                # continuation: indented (2+ spaces) non-blank, non-bullet
                while i < len(lines):
                    nxt = lines[i]
                    if nxt.strip() == '': break
                    if _LIST_RE.match(nxt): break
                    if not nxt.startswith('  '): break
                    current += ' ' + nxt.strip()
                    i += 1
                items.append(current)
            blocks.append(Block(kind='list', items=items))
            continue

        # paragraph — gather until blank line, heading, table, list, or fence
        para_lines = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            ns = nxt.strip()
            if not ns: break
            if _HEADING_RE.match(nxt): break
            if _LIST_RE.match(nxt): break
            if _FENCE_RE.match(nxt): break
            if ns.startswith('|') and i + 1 < len(lines) and _TABLE_SEP_RE.match(lines[i + 1]): break
            para_lines.append(nxt)
            i += 1
        blocks.append(Block(kind='paragraph', text=' '.join(l.strip() for l in para_lines)))

    return blocks


# ── pair English + Korean ──────────────────────────────────────────────────

def pair_blocks(en: list[Block], ko: list[Block], slug: str) -> list[tuple[Block, Block]]:
    """Pair English and Korean block sequences by position.

    Both lists must have the same sequence of block kinds. Heading levels
    must match. Mismatches abort the build with a diagnostic.
    """
    if len(en) != len(ko):
        raise SystemExit(
            f'[{slug}] block count mismatch: en={len(en)} ko={len(ko)}. '
            'Heading or block structure has drifted — fix the ko/ mirror.'
        )
    pairs = []
    for idx, (a, b) in enumerate(zip(en, ko)):
        if a.kind != b.kind:
            raise SystemExit(
                f'[{slug}] block #{idx} kind mismatch: en={a.kind} ko={b.kind}'
            )
        if a.kind == 'heading' and a.level != b.level:
            raise SystemExit(
                f'[{slug}] heading #{idx} level mismatch: en=h{a.level} ko=h{b.level} '
                f'(en="{a.text}" ko="{b.text}")'
            )
        if a.kind == 'table':
            if len(a.rows) != len(b.rows) or any(len(ra) != len(rb) for ra, rb in zip(a.rows, b.rows)):
                raise SystemExit(
                    f'[{slug}] table block #{idx}: row/column count mismatch '
                    f'(en {len(a.rows)}x{len(a.rows[0]) if a.rows else 0}, '
                    f'ko {len(b.rows)}x{len(b.rows[0]) if b.rows else 0})'
                )
        if a.kind == 'list' and len(a.items) != len(b.items):
            raise SystemExit(
                f'[{slug}] list block #{idx}: item count mismatch (en={len(a.items)} ko={len(b.items)})'
            )
        pairs.append((a, b))
    return pairs


# ── inline markdown → HTML ─────────────────────────────────────────────────

_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
_INLINE_CODE_RE = re.compile(r'`([^`]+)`')
_BOLD_RE = re.compile(r'\*\*([^*]+)\*\*')
_ITALIC_RE = re.compile(r'(?<!\*)\*([^*]+)\*(?!\*)')


def inline_md(text: str) -> str:
    """Render inline markdown (bold/italic/code/links) to HTML.

    Text is HTML-escaped first; markdown markers then translate to tags.
    """
    out = html.escape(text)
    # links: [text](url)
    out = _LINK_RE.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', out)
    # inline code
    out = _INLINE_CODE_RE.sub(lambda m: f'<code>{m.group(1)}</code>', out)
    # bold (run before italic to avoid ** being eaten as two *)
    out = _BOLD_RE.sub(lambda m: f'<b>{m.group(1)}</b>', out)
    # italic
    out = _ITALIC_RE.sub(lambda m: f'<i>{m.group(1)}</i>', out)
    return out


# ── HTML rendering with i18n ───────────────────────────────────────────────

# JS-safe representation of an HTML snippet for use as a JS string value.
def _js_string(s: str) -> str:
    return (s.replace('\\', '\\\\')
              .replace('"', '\\"')
              .replace('\n', '\\n')
              .replace('\r', ''))


def render_html(slug: str, title_en: str, title_ko: str, pairs: list[tuple[Block, Block]]) -> str:
    body_html_parts: list[str] = []
    i18n_en: dict[str, str] = {}
    i18n_ko: dict[str, str] = {}

    key_counter = 0
    def new_key(prefix: str) -> str:
        nonlocal key_counter
        key_counter += 1
        return f'{prefix}_{key_counter}'

    in_section = False  # whether we have an open <section>

    def close_section_if_open():
        nonlocal in_section
        if in_section:
            body_html_parts.append('</section>')
            in_section = False

    for en, ko in pairs:
        if en.kind == 'heading':
            if en.level == 1:
                # H1 is the page title; rendered in <header>, not in main body
                continue
            if en.level == 2:
                close_section_if_open()
                body_html_parts.append('<section>')
                in_section = True
                key = new_key('h2')
                i18n_en[key] = inline_md(en.text)
                i18n_ko[key] = inline_md(ko.text)
                body_html_parts.append(f'<h2 data-i18n="{key}"></h2>')
            else:  # h3 / h4 / ...
                key = new_key(f'h{en.level}')
                i18n_en[key] = inline_md(en.text)
                i18n_ko[key] = inline_md(ko.text)
                body_html_parts.append(f'<h{en.level} data-i18n="{key}"></h{en.level}>')

        elif en.kind == 'paragraph':
            key = new_key('p')
            i18n_en[key] = inline_md(en.text)
            i18n_ko[key] = inline_md(ko.text)
            body_html_parts.append(f'<p class="intro" data-i18n="{key}"></p>')

        elif en.kind == 'list':
            body_html_parts.append('<ul class="intro">')
            for idx, (e_item, k_item) in enumerate(zip(en.items, ko.items)):
                key = new_key('li')
                i18n_en[key] = inline_md(e_item)
                i18n_ko[key] = inline_md(k_item)
                body_html_parts.append(f'<li data-i18n="{key}"></li>')
            body_html_parts.append('</ul>')

        elif en.kind == 'code':
            # code is language-neutral
            esc = html.escape(en.text)
            cls = f' class="lang-{en.lang}"' if en.lang else ''
            body_html_parts.append(f'<pre><code{cls}>{esc}</code></pre>')

        elif en.kind == 'table':
            body_html_parts.append('<div class="card"><table class="dt"><thead><tr>')
            for c_en, c_ko in zip(en.rows[0], ko.rows[0]):
                key = new_key('th')
                i18n_en[key] = inline_md(c_en)
                i18n_ko[key] = inline_md(c_ko)
                body_html_parts.append(f'<th data-i18n="{key}"></th>')
            body_html_parts.append('</tr></thead><tbody>')
            for r_en, r_ko in zip(en.rows[1:], ko.rows[1:]):
                body_html_parts.append('<tr>')
                for c_en, c_ko in zip(r_en, r_ko):
                    key = new_key('td')
                    i18n_en[key] = inline_md(c_en)
                    i18n_ko[key] = inline_md(c_ko)
                    body_html_parts.append(f'<td data-i18n="{key}"></td>')
                body_html_parts.append('</tr>')
            body_html_parts.append('</tbody></table></div>')

    close_section_if_open()

    # title (H1)
    title_key = 'title'
    i18n_en[title_key] = inline_md(title_en)
    i18n_ko[title_key] = inline_md(title_ko)

    # serialize i18n
    def kv_block(d: dict[str, str]) -> str:
        return ',\n  '.join(f'"{k}":"{_js_string(v)}"' for k, v in d.items())

    body_html = '\n'.join(body_html_parts)

    return f'''<!DOCTYPE html>
<!-- {slug} Phase 3 report — autogenerated by scripts/phase3/build_html.py from docs/phase3/{slug}.md + ko/ mirror -->
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title data-i18n="title"></title>
<link rel="stylesheet" href="../style.css">
<style>
main {{ max-width: 1080px }}
section {{ margin-bottom: 32px }}
h3 {{ font-size: 14px; margin: 16px 0 8px }}
.intro {{ font-size: 13.5px; line-height: 1.7 }}
ul.intro {{ padding-left: 22px }}

.dt {{ width: 100%; border-collapse: collapse; font-size: 12.5px; margin-top: 6px }}
.dt th {{ padding: 8px 10px; background: var(--bg-card-alt); color: var(--fg-dim); font-size: 10.5px; text-transform: uppercase; text-align: left; font-weight: 700; letter-spacing: .5px; border-bottom: 1px solid var(--bd-strong) }}
.dt td {{ padding: 7px 10px; border-top: 1px solid var(--bd-soft); color: #b0c4d8; font-family: var(--mono); font-size: 12px; vertical-align: top; line-height: 1.55 }}

pre {{ background: var(--bg-card-alt); border: 1px solid var(--bd-soft); border-radius: 4px; padding: 10px 12px; overflow-x: auto; margin: 8px 0 }}
pre code {{ background: none; padding: 0; font-size: 12px }}

.lang-toggle {{ margin-left: auto }}

@media (max-width: 600px) {{
  section {{ margin-bottom: 24px }}
  .dt thead {{ display: none }}
  .dt, .dt tbody, .dt tr, .dt td {{ display: block; width: 100% }}
  .dt tr {{ border: 1px solid #1a2333; border-radius: 6px; padding: 8px 11px; margin-bottom: 6px; background: #0a1018 }}
  .dt td {{ display: block; border: none; padding: 3px 0; font-size: 12px }}
}}
</style>
</head>

<body>

<header>
  <h1 data-i18n="title"></h1>
  <div class="crumb"><a href="../index.html" data-i18n="back_db"></a> · <a href="../reports.html" data-i18n="reports_index"></a></div>
  <div class="seg lang-toggle" id="lang-seg">
    <button class="on" data-lang="ko">한</button>
    <button data-lang="en">EN</button>
  </div>
</header>

<main>
{body_html}
</main>

<footer>
  <span data-i18n="footer_note"></span>
</footer>

<script>
const T = {{
  en: {{
  {kv_block(i18n_en)},
  "back_db": "← Back to database",
  "reports_index": "Reports index",
  "footer_note": "NearStars · Phase 3 synthesis report · autogenerated from {slug}.md + ko/ mirror"
  }},
  ko: {{
  {kv_block(i18n_ko)},
  "back_db": "← 데이터베이스로",
  "reports_index": "보고서 인덱스",
  "footer_note": "NearStars · Phase 3 합성 보고서 · {slug}.md + ko/ 미러에서 자동 생성"
  }}
}};

let lang = localStorage.getItem('nearstars-lang') || 'ko';

function applyLang() {{
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach(el => {{
    const v = T[lang][el.dataset.i18n];
    if (v !== undefined) el.innerHTML = v;
  }});
  document.querySelectorAll('#lang-seg button').forEach(b => {{
    b.classList.toggle('on', b.dataset.lang === lang);
  }});
}}

document.getElementById('lang-seg').addEventListener('click', e => {{
  const btn = e.target.closest('button[data-lang]');
  if (!btn) return;
  lang = btn.dataset.lang;
  localStorage.setItem('nearstars-lang', lang);
  applyLang();
}});

applyLang();
</script>

</body>
</html>
'''


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    slug = sys.argv[1]

    # locate repo root from this script's location: scripts/phase3/build_html.py → repo/
    here = Path(__file__).resolve()
    repo = here.parent.parent.parent

    en_path = repo / 'docs' / 'phase3' / f'{slug}.md'
    ko_path = repo / 'ko' / 'docs' / 'phase3' / f'{slug}.md'

    if not en_path.exists():
        raise SystemExit(f'English source not found: {en_path}')
    if not ko_path.exists():
        raise SystemExit(f'Korean mirror not found: {ko_path}. Per AGENTS.md §2.1, every '
                         f'docs/phase3/*.md must have a ko/ mirror.')

    en_blocks = parse_md(en_path)
    ko_blocks = parse_md(ko_path)

    # extract H1 titles for the page <title> and <h1>
    title_en = next((b.text for b in en_blocks if b.kind == 'heading' and b.level == 1), slug)
    title_ko = next((b.text for b in ko_blocks if b.kind == 'heading' and b.level == 1), slug)

    pairs = pair_blocks(en_blocks, ko_blocks, slug)

    html_out = render_html(slug, title_en, title_ko, pairs)

    out_path = repo / 'docs' / 'phase3' / f'{slug}.html'
    out_path.write_text(html_out, encoding='utf-8')
    print(f'wrote {out_path.relative_to(repo)}  ({len(html_out):,} bytes, '
          f'{len(pairs)} blocks paired)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
