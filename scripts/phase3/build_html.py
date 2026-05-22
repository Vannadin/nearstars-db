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


# ── color visualization ────────────────────────────────────────────────────
# Decisions tables curate per-planet color palettes. We render:
#   1. a palette band above each Decisions table (one swatch per color field)
#   2. an inline chip beside every `#xxxxxx` hex code in any text
#   3. a wavelength-spectrum gradient bar for aurora rows (emissive light,
#      not reflected, so it doesn't share the reflective-surface logic)

PALETTE_FIELDS = {
    'atmosphere_tint_rgb_hex':       'Atmos',
    'cloud_tint_rgb_hex':            'Cloud',
    'ocean_tint_rgb_hex':            'Ocean',
    'surface_tint_rgb_hex_primary':  'Surf · 1',
    'surface_tint_rgb_hex_accent':   'Surf · 2',
    'sunset_color_hex':              'Sunset',
    'aurora_color_primary_hex':      'Aurora · 1',
    'aurora_color_secondary_hex':    'Aurora · 2',
}
EMISSIVE_FIELDS = {'aurora_color_primary_hex', 'aurora_color_secondary_hex'}

_HEX_RE = re.compile(r'#([0-9A-Fa-f]{6})\b')
_HEX_IN_CODE_RE = re.compile(r'<code>#([0-9A-Fa-f]{6})</code>')
# Wavelength range: "580–700 nm", "580-700 nm", "~330–400 nm"
_NM_RANGE_RE = re.compile(r'(?:~)?(\d{2,4})\s*[–\-]\s*(\d{2,4})\s*nm')
# Single line: "557.7 nm", "289 nm" — 3+ digits to avoid catching things like "8 nm"
_NM_SINGLE_RE = re.compile(r'(?:~)?(\d{3,4}(?:\.\d+)?)\s*nm')

# Auroral emission species → wavelength fallback for descriptions without explicit nm.
# (substring, value) where value is either a single nm or a (start, end) tuple.
# Order matters — more specific substrings should come first.
_SPECIES_FALLBACK = [
    ('Lyman-Birge-Hopfield', (130, 200)),   # N₂ LBH — far UV
    ('Vegard-Kaplan',        (200, 280)),   # N₂ VK — UV
    ('Fox–Duffendack',       (580, 700)),   # CO₂⁺ FDB band
    ('Fox-Duffendack',       (580, 700)),
    ('Cameron',              (180, 260)),   # CO Cameron — UV
    ('Meinel',               (670, 720)),   # N₂⁺ Meinel — red/NIR
    ('OH(A-X)',              308.0),        # OH band — UV
    ('OH band',              308.0),
    ('[OI]',                 557.7),
    ('[NI]',                 520.0),
    ('N₂⁺',                  391.4),        # default to First Negative if no band specified
]
# Bruton's wavelength→RGB is defined for 380–780 nm. Outside that we render a UV/IR badge
# rather than a partial gradient — partial-UV bands look mostly black, which is misleading.
_VISIBLE_MIN = 380.0
_VISIBLE_MAX = 780.0


def _wavelength_to_rgb(wl: float) -> tuple:
    """Bruton's approximation for visible wavelength → linear RGB (380–780 nm)."""
    R = G = B = 0.0
    if 380 <= wl < 440:    R, B = -(wl - 440) / 60, 1.0
    elif wl < 490:          G, B = (wl - 440) / 50, 1.0
    elif wl < 510:          G, B = 1.0, -(wl - 510) / 20
    elif wl < 580:          R, G = (wl - 510) / 70, 1.0
    elif wl < 645:          R, G = 1.0, -(wl - 645) / 65
    elif wl <= 780:         R = 1.0
    # intensity falloff at the spectrum edges
    f = 1.0
    if wl < 420:    f = 0.3 + 0.7 * (wl - 380) / 40
    elif wl > 700:  f = 0.3 + 0.7 * (780 - wl) / 80
    gamma = 0.8
    return tuple(0.0 if c == 0 else max(0.0, min(1.0, c * f)) ** gamma for c in (R, G, B))


def _rgb_to_hex(rgb: tuple) -> str:
    return '#' + ''.join(f'{int(round(max(0, min(1, c)) * 255)):02x}' for c in rgb)


def spectrum_gradient(start: int, end: int, steps: int = 12) -> str:
    """CSS linear-gradient string sampling Bruton's curve across [start, end] nm."""
    stops = [_rgb_to_hex(_wavelength_to_rgb(start + (end - start) * i / steps))
             for i in range(steps + 1)]
    return f'linear-gradient(to right, {", ".join(stops)})'


def parse_aurora_wavelength(text: str):
    """Return (start_nm, end_nm, marker_or_None) or None if no wavelength is found.

    Search order:
    1. Explicit nm range (highest priority — paper-specific values)
    2. Explicit single nm line (±20 nm window with a marker at the exact line)
    3. Known emission-species substring (e.g. "[OI]" → 557.7 nm, "Fox–Duffendack" → 580–700)

    Species fallback handles auroras described by chemistry rather than nm,
    e.g. d's "Trace [OI] green if oxygen present" → 557.7 nm.
    """
    m = _NM_RANGE_RE.search(text)
    if m:
        return (int(m.group(1)), int(m.group(2)), None)
    m = _NM_SINGLE_RE.search(text)
    if m:
        wl = float(m.group(1))
        return (int(round(wl)) - 20, int(round(wl)) + 20, wl)
    for substr, val in _SPECIES_FALLBACK:
        if substr in text:
            if isinstance(val, tuple):
                return (val[0], val[1], None)
            return (int(round(val)) - 20, int(round(val)) + 20, val)
    return None


def is_uv_or_ir(start: float, end: float) -> bool:
    """True if the band is essentially outside Bruton's visible range."""
    return end < _VISIBLE_MIN or start > _VISIBLE_MAX


def is_wide_band(start: float, end: float) -> bool:
    """True if the band is wider than 60 nm — wide bands get edge-fade via CSS mask."""
    return (end - start) > 60


def _contrast_text(hex_code: str) -> str:
    """Pick black or white text per simple luma threshold."""
    r = int(hex_code[1:3], 16) / 255
    g = int(hex_code[3:5], 16) / 255
    b = int(hex_code[5:7], 16) / 255
    luma = 0.299 * r + 0.587 * g + 0.114 * b
    return '#000' if luma > 0.55 else '#fff'


def _extract_hex(text: str):
    m = _HEX_RE.search(text)
    return '#' + m.group(1).lower() if m else None


def is_decisions_table(rows) -> bool:
    """Decisions tables have a header containing 'Field' and 'Confidence'."""
    if not rows or len(rows[0]) < 3:
        return False
    headers = [h.strip().lower() for h in rows[0]]
    return any('field' in h for h in headers[:1]) and any('confidence' in h for h in headers)


def parse_palette_swatches(rows) -> list:
    """Walk a Decisions table and extract per-field data for the palette band."""
    out = []
    for row in rows[1:]:
        if len(row) < 2:
            continue
        field = row[0].strip().strip('`').strip()
        if field not in PALETTE_FIELDS:
            continue
        value = row[1]
        basis = row[3] if len(row) >= 4 else ''
        if field in EMISSIVE_FIELDS:
            wave = parse_aurora_wavelength(value + ' ' + basis)
            hex_code = _extract_hex(value)
            if not wave and not hex_code:
                continue
            out.append({'field': field, 'label': PALETTE_FIELDS[field],
                        'kind': 'emissive', 'wave': wave, 'hex': hex_code})
        else:
            hex_code = _extract_hex(value)
            if not hex_code:
                continue  # 'n/a' etc.
            out.append({'field': field, 'label': PALETTE_FIELDS[field],
                        'kind': 'reflective', 'hex': hex_code})
    return out


def render_palette_band(swatches: list) -> str:
    if not swatches:
        return ''
    parts = ['<div class="palette-band">']
    for s in swatches:
        if s['kind'] == 'reflective':
            hex_code = s['hex']
            parts.append(
                f'<div class="palette-swatch" style="background:{hex_code};color:{_contrast_text(hex_code)}">'
                f'<span class="role">{html.escape(s["label"])}</span>'
                f'<span class="hex">{hex_code}</span></div>'
            )
        else:
            if s['wave']:
                start, end, marker = s['wave']
                if is_uv_or_ir(start, end):
                    # Outside Bruton visible — palette swatch uses the curated hex
                    # (since UV/IR has no perceived gradient color) but keeps the
                    # emissive label and shows the band edge.
                    band = 'UV' if end < _VISIBLE_MIN else 'IR'
                    fallback_hex = s.get('hex') or '#2a2a2a'
                    parts.append(
                        f'<div class="palette-swatch palette-swatch-emissive palette-swatch-invisible" '
                        f'style="background:{fallback_hex};color:{_contrast_text(fallback_hex)}">'
                        f'<span class="role">{html.escape(s["label"])}</span>'
                        f'<span class="hex">{band} · {int(start)}–{int(end)} nm</span></div>'
                    )
                else:
                    marker_html = ''
                    if marker:
                        pos = (marker - start) / (end - start) * 100
                        marker_html = f'<div class="palette-marker" style="left:{pos:.1f}%"></div>'
                    parts.append(
                        f'<div class="palette-swatch palette-swatch-emissive" '
                        f'style="background:{spectrum_gradient(start, end)}">'
                        f'{marker_html}'
                        f'<span class="role">{html.escape(s["label"])}</span>'
                        f'<span class="hex">{int(start)}–{int(end)} nm</span></div>'
                    )
            elif s['hex']:
                # No parseable wavelength even via species lookup — flat hex chip.
                hex_code = s['hex']
                parts.append(
                    f'<div class="palette-swatch palette-swatch-emissive" '
                    f'style="background:{hex_code};color:{_contrast_text(hex_code)}">'
                    f'<span class="role">{html.escape(s["label"])}</span>'
                    f'<span class="hex">{hex_code}</span></div>'
                )
    parts.append('</div>')
    return ''.join(parts)


def augment_hex_chips(html_text: str) -> str:
    """Insert a small color chip before every <code>#xxxxxx</code>."""
    return _HEX_IN_CODE_RE.sub(
        lambda m: (f'<span class="hex-chip" style="background:#{m.group(1).lower()}"></span>'
                   f'<code>#{m.group(1)}</code>'),
        html_text,
    )


def _render_spectrum_marker(start: float, end: float, marker) -> str:
    """White vertical marker line at exact wavelength inside a spectrum bar."""
    if not marker:
        return ''
    pos = (marker - start) / (end - start) * 100
    return f'<div class="marker" style="left:{pos:.1f}%"></div>'


def render_spectrum_widget(start: float, end: float, marker, hex_code: str = '') -> str:
    """Render the wavelength widget (bar or UV badge) + range caption.

    Three visual modes:
    - **visible narrow** (≤60 nm): full-intensity gradient
    - **visible wide** (>60 nm): gradient with CSS mask fading edges so the
      visual weight sits at the center, not across the full yellow-to-red span
    - **UV / IR**: muted "non-visible" badge instead of a mostly-black gradient
    """
    if is_uv_or_ir(start, end):
        # Outside Bruton visible — render a muted "UV" or "IR" badge.
        band = 'UV' if end < _VISIBLE_MIN else 'IR'
        bar = (f'<span class="spectrum-bar spectrum-bar-invisible" '
               f'title="{int(start)}–{int(end)} nm (outside visible spectrum)">'
               f'{band}</span>')
        caption = (f'<span class="spectrum-range">{int(start)}–{int(end)} nm · {band}'
                   + (f' · peak {marker} nm' if marker else '')
                   + '</span>')
        return bar + caption

    # Visible-range gradient. Wide bands get edge-fade via CSS mask.
    cls = 'spectrum-bar'
    if is_wide_band(start, end):
        cls += ' spectrum-bar-wide'
    bar = (f'<span class="{cls}" style="background:{spectrum_gradient(start, end)}">'
           f'{_render_spectrum_marker(start, end, marker)}</span>')
    caption = (f'<span class="spectrum-range">{int(start)}–{int(end)} nm'
               + (f' · peak {marker} nm' if marker else '')
               + '</span>')
    return bar + caption


def render_aurora_value(value_md: str, basis_md: str) -> str:
    """Render a Decisions-table Value cell for an aurora row.

    Combines the wavelength widget (spectrum bar or UV badge, picked by
    `render_spectrum_widget`) with the curated hex (chip + code) and any
    remaining inline description. Falls back to chip-only rendering if no
    wavelength can be parsed even via species substring lookup.
    """
    wave = parse_aurora_wavelength(value_md + ' ' + basis_md)
    if not wave:
        return augment_hex_chips(inline_md(value_md))
    start, end, marker = wave
    widget = render_spectrum_widget(start, end, marker)
    hex_code = _extract_hex(value_md)
    hex_html = ''
    if hex_code:
        hex_html = (f' <span class="hex-chip" style="background:{hex_code}"></span>'
                    f'<code>{hex_code}</code>')
    desc = _HEX_RE.sub('', value_md)
    desc = re.sub(r'`+', '', desc).strip()
    if desc.startswith('(') and desc.endswith(')'):
        desc = desc[1:-1].strip()
    return widget + hex_html + (' ' + inline_md(desc) if desc else '')


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
            i18n_en[key] = augment_hex_chips(inline_md(en.text))
            i18n_ko[key] = augment_hex_chips(inline_md(ko.text))
            body_html_parts.append(f'<p class="intro" data-i18n="{key}"></p>')

        elif en.kind == 'list':
            body_html_parts.append('<ul class="intro">')
            for idx, (e_item, k_item) in enumerate(zip(en.items, ko.items)):
                key = new_key('li')
                i18n_en[key] = augment_hex_chips(inline_md(e_item))
                i18n_ko[key] = augment_hex_chips(inline_md(k_item))
                body_html_parts.append(f'<li data-i18n="{key}"></li>')
            body_html_parts.append('</ul>')

        elif en.kind == 'code':
            # code is language-neutral
            esc = html.escape(en.text)
            cls = f' class="lang-{en.lang}"' if en.lang else ''
            body_html_parts.append(f'<pre><code{cls}>{esc}</code></pre>')

        elif en.kind == 'table':
            decisions = is_decisions_table(en.rows)
            if decisions:
                # Palette band: locale-independent visual summary; emit before the table.
                band = render_palette_band(parse_palette_swatches(en.rows))
                if band:
                    body_html_parts.append(band)
            body_html_parts.append('<div class="card"><table class="dt"><thead><tr>')
            for c_en, c_ko in zip(en.rows[0], ko.rows[0]):
                key = new_key('th')
                i18n_en[key] = inline_md(c_en)
                i18n_ko[key] = inline_md(c_ko)
                body_html_parts.append(f'<th data-i18n="{key}"></th>')
            body_html_parts.append('</tr></thead><tbody>')
            for r_en, r_ko in zip(en.rows[1:], ko.rows[1:]):
                field_name = r_en[0].strip().strip('`').strip() if r_en else ''
                aurora_row = decisions and field_name in EMISSIVE_FIELDS
                body_html_parts.append('<tr>')
                for col_idx, (c_en, c_ko) in enumerate(zip(r_en, r_ko)):
                    key = new_key('td')
                    if aurora_row and col_idx == 1:
                        # Value cell of an aurora row → spectrum bar instead of plain hex chip
                        basis_en = r_en[3] if len(r_en) >= 4 else ''
                        basis_ko = r_ko[3] if len(r_ko) >= 4 else ''
                        i18n_en[key] = render_aurora_value(c_en, basis_en)
                        i18n_ko[key] = render_aurora_value(c_ko, basis_ko)
                    else:
                        i18n_en[key] = augment_hex_chips(inline_md(c_en))
                        i18n_ko[key] = augment_hex_chips(inline_md(c_ko))
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

/* color visualization: palette band above Decisions tables */
.palette-band {{ display: flex; gap: 2px; margin: 10px 0 8px; height: 60px; border-radius: 4px; overflow: hidden; border: 1px solid var(--bd-strong) }}
.palette-swatch {{ flex: 1; display: flex; flex-direction: column; justify-content: space-between; padding: 5px 7px; font-family: var(--mono); font-size: 9.5px; line-height: 1.2; transition: flex-grow 0.15s ease; position: relative; overflow: hidden }}
.palette-swatch:hover {{ flex-grow: 2.2 }}
.palette-swatch .role {{ opacity: 0.88; font-weight: 600; text-transform: uppercase; letter-spacing: .3px; font-size: 9px }}
.palette-swatch .hex {{ opacity: 0.72; font-size: 10px }}
.palette-swatch-emissive {{ color: rgba(0,0,0,0.88) }}
.palette-marker {{ position: absolute; top: 0; bottom: 0; width: 2px; background: rgba(255,255,255,0.85); box-shadow: 0 0 3px rgba(0,0,0,0.6); pointer-events: none }}

/* color visualization: inline chip beside every <code>#xxxxxx</code> */
.hex-chip {{ display: inline-block; width: 11px; height: 11px; border-radius: 2px; border: 1px solid rgba(255,255,255,0.18); vertical-align: -1px; margin-right: 5px }}

/* color visualization: aurora rows render a wavelength gradient bar */
.spectrum-bar {{ display: inline-block; height: 13px; width: 110px; border-radius: 2px; border: 1px solid rgba(255,255,255,0.20); vertical-align: -2px; margin-right: 6px; position: relative }}
.spectrum-bar .marker {{ position: absolute; top: -2px; bottom: -2px; width: 2px; background: rgba(255,255,255,0.85); box-shadow: 0 0 3px rgba(0,0,0,0.6); pointer-events: none }}
/* Wide bands (>60 nm) fade their edges via mask so visual weight sits at the band center —
   stops a 580–700 nm CO₂⁺ FDB band from reading as a full yellow→red rainbow. */
.spectrum-bar-wide {{ mask-image: linear-gradient(to right, transparent, #000 25%, #000 75%, transparent); -webkit-mask-image: linear-gradient(to right, transparent, #000 25%, #000 75%, transparent) }}
/* UV / IR bands lie outside Bruton's visible curve — render a muted badge rather than a black gradient. */
.spectrum-bar-invisible {{ background: repeating-linear-gradient(45deg, #1a1f2a, #1a1f2a 4px, #232838 4px, #232838 8px); color: var(--fg-dim); text-align: center; font-family: var(--mono); font-size: 9.5px; font-weight: 700; line-height: 13px; letter-spacing: .5px; width: 50px }}
.palette-swatch-invisible {{ background-image: repeating-linear-gradient(45deg, rgba(255,255,255,0.04), rgba(255,255,255,0.04) 6px, transparent 6px, transparent 12px) }}
.spectrum-range {{ font-size: 10px; color: var(--fg-dim); margin-left: 4px; font-family: var(--mono) }}

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
