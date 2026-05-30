# 수동 fetch 후속 페이퍼 목록 → HTML 변환기 (docs/phase3/manual-fetch.html)
"""Build a single discovery page from per-system manual-paper-followup.md
files.

Phase 3 synthesis surfaces ADS papers without arXiv preprints — Claude
can't auto-fetch them. The per-system markdown
(`phase3/<system>/manual-paper-followup.md`) records them at three
tiers; this script aggregates each system's Tier A + Tier B tables
into a single bilingual HTML page so the user (or a future session)
can scan all pending fetches at a glance.

Outputs:
  - docs/phase3/manual-fetch.html

Usage:
    python3 scripts/phase3/build_manual_fetch.py
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import yaml


ADS_BASE = 'https://ui.adsabs.harvard.edu/abs/'

# Per-row Korean text for "Why it matters" goes into the i18n dict and gets
# swapped on language toggle. Per-cell keys are generated as why_<n> so each
# row is independently translatable. Module-level state because rendering is
# spread across several helpers.
_ROW_I18N_EN: dict[str, str] = {}
_ROW_I18N_KO: dict[str, str] = {}
_ROW_KEY_COUNTER = {'n': 0}


def _reset_row_i18n():
    _ROW_I18N_EN.clear()
    _ROW_I18N_KO.clear()
    _ROW_KEY_COUNTER['n'] = 0


def _new_row_key() -> str:
    _ROW_KEY_COUNTER['n'] += 1
    return f'why_{_ROW_KEY_COUNTER["n"]}'


def parse_table(section: str) -> list[list[str]]:
    """Extract the first markdown table inside a section. Returns header + data rows."""
    lines = section.split('\n')
    i = 0
    while i < len(lines) - 1:
        if lines[i].strip().startswith('|') and re.match(r'^\s*\|\s*:?-{2,}', lines[i + 1]):
            rows = [[c.strip() for c in lines[i].strip().strip('|').split('|')]]
            i += 2
            while i < len(lines) and lines[i].strip().startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
            return rows
        i += 1
    return []


def parse_md(path: Path) -> dict:
    """Return {'A': [rows], 'B': [rows], 'C_prose': str, 'fetching_tips': str}.

    A/B rows include the header row at index 0. C is parsed as descriptive prose.
    """
    text = path.read_text(encoding='utf-8')
    out = {'A': [], 'B': [], 'C_prose': '', 'fetching_tips': ''}

    for tier in ('A', 'B'):
        header = f'## Tier {tier}'
        idx = text.find(header)
        if idx < 0:
            continue
        next_idx = text.find('\n## ', idx + len(header))
        section = text[idx:next_idx] if next_idx > 0 else text[idx:]
        out[tier] = parse_table(section)

    # Tier C: prose only (typically a one-paragraph "skip unless context needed" note)
    idx = text.find('## Tier C')
    if idx >= 0:
        next_idx = text.find('\n## ', idx + 10)
        section = text[idx:next_idx] if next_idx > 0 else text[idx:]
        prose_lines = []
        for line in section.split('\n')[1:]:
            s = line.strip()
            if not s or s.startswith('|') or s.startswith('## '):
                if prose_lines and not s:
                    prose_lines.append('')
                continue
            prose_lines.append(s)
        out['C_prose'] = ' '.join(l for l in prose_lines if l).strip()

    idx = text.find('## Fetching tips')
    if idx >= 0:
        next_idx = text.find('\n## ', idx + len('## Fetching tips'))
        section = text[idx:next_idx] if next_idx > 0 else text[idx:]
        # Pass through as a bulleted list extraction
        tips = []
        for line in section.split('\n')[1:]:
            m = re.match(r'^\s*\d+\.\s+(.+)$', line)
            if m:
                tips.append(m.group(1).strip())
        out['fetching_tips'] = tips
    return out


# inline markdown → HTML
_LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
_BOLD_RE = re.compile(r'\*\*([^*]+)\*\*')
_AUTOLINK_RE = re.compile(r'<(https?://[^>]+)>')
_INLINE_CODE_RE = re.compile(r'`([^`]+)`')
# Bibcodes inside narrative text (not the table) — turn into ADS links
_BIBCODE_INLINE_RE = re.compile(r'(?<![\w/])(\d{4}[A-Za-z][A-Za-z&\.][\w\.&]+\.\.[\w\.\d][\w\d])')


def inline_md(text: str) -> str:
    out = html.escape(text)
    out = _AUTOLINK_RE.sub(lambda m: f'<a href="{m.group(1)}" target="_blank" rel="noopener">{m.group(1)}</a>', out)
    out = _LINK_RE.sub(lambda m: f'<a href="{m.group(2)}" target="_blank" rel="noopener">{m.group(1)}</a>', out)
    out = _INLINE_CODE_RE.sub(lambda m: f'<code>{m.group(1)}</code>', out)
    out = _BOLD_RE.sub(lambda m: f'<b>{m.group(1)}</b>', out)
    return out


def render_paper_row(row: list[str], ko_lookup: dict | None = None) -> str:
    """Render one paper row → <tr>.

    Bibcode column may carry alternates separated by " / "; the first one is
    used for the ADS link and for ko_lookup.

    If ko_lookup contains a matching bibcode, the "Why it matters" cell gets
    a generated i18n key so the Korean version can be swapped in by the
    lang toggle. Without a ko entry, the cell is plain English with no key.
    """
    cells = (row + [''] * 5)[:5]
    bibcode_raw = cells[0].strip().strip('`')
    bibcode_first = bibcode_raw.split(' / ')[0].strip()
    ads_url = ADS_BASE + bibcode_first + '/abstract'

    why_en_html = inline_md(cells[4])
    why_cell_attr = ''
    if ko_lookup and bibcode_first in ko_lookup:
        key = _new_row_key()
        _ROW_I18N_EN[key] = why_en_html
        _ROW_I18N_KO[key] = inline_md(ko_lookup[bibcode_first])
        why_cell_attr = f' data-i18n="{key}"'

    return (
        f'        <tr>\n'
        f'          <td class="bib" data-label="Bibcode"><a href="{html.escape(ads_url)}" target="_blank" rel="noopener">{html.escape(bibcode_raw)}</a></td>\n'
        f'          <td class="year" data-label="Year">{html.escape(cells[1])}</td>\n'
        f'          <td class="planet" data-label="Planet">{html.escape(cells[2])}</td>\n'
        f'          <td class="title" data-label="Title">{inline_md(cells[3])}</td>\n'
        f'          <td class="why" data-label="Why"{why_cell_attr}>{why_en_html}</td>\n'
        f'        </tr>'
    )


def render_table(rows: list[list[str]], ko_lookup: dict | None = None) -> str:
    """Render a parsed Tier table (incl. header row)."""
    if not rows:
        return '<p class="empty">(none)</p>'
    body_rows = '\n'.join(render_paper_row(r, ko_lookup) for r in rows[1:])
    return (
        '<div class="card"><table class="mft">\n'
        '      <thead><tr>\n'
        '        <th data-i18n="th_bibcode"></th>\n'
        '        <th data-i18n="th_year"></th>\n'
        '        <th data-i18n="th_planet"></th>\n'
        '        <th data-i18n="th_title"></th>\n'
        '        <th data-i18n="th_why"></th>\n'
        '      </tr></thead>\n'
        '      <tbody>\n'
        f'{body_rows}\n'
        '      </tbody>\n'
        '    </table></div>'
    )


PAGE_TEMPLATE = r'''<!DOCTYPE html>
<!-- NearStars Phase 3 — manual paper follow-up index, autogenerated by scripts/phase3/build_manual_fetch.py -->
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title data-i18n="title"></title>
<link rel="stylesheet" href="../style.css">
<style>
main { max-width: 1080px }
section { margin-bottom: 32px }
h2 { font-size: 17px; margin: 28px 0 10px; color: var(--fg-emph); border-bottom: 1px solid var(--bd-strong); padding-bottom: 6px }
h3 { font-size: 13px; margin: 18px 0 6px; color: var(--fg-muted); text-transform: uppercase; letter-spacing: .5px }
.intro { font-size: 13.5px; line-height: 1.7 }
.note { color: var(--fg-dim); font-size: 12px; font-style: italic; margin: 6px 0 12px }
.empty { color: var(--fg-faint); font-style: italic }

.mft { width: 100%; border-collapse: collapse; font-size: 12px; margin: 4px 0 12px }
.mft th { padding: 7px 9px; background: var(--bg-card-alt); color: var(--fg-dim); font-size: 10px; text-transform: uppercase; text-align: left; font-weight: 700; letter-spacing: .5px; border-bottom: 1px solid var(--bd-strong) }
.mft td { padding: 6px 9px; border-top: 1px solid var(--bd-soft); color: #b0c4d8; vertical-align: top; line-height: 1.5 }
.mft td.bib { font-family: var(--mono); font-size: 11px; white-space: nowrap }
.mft td.bib a { color: var(--accent); text-decoration: none }
.mft td.bib a:hover { text-decoration: underline }
.mft td.year { font-family: var(--mono); font-size: 11px; color: var(--fg-muted) }
.mft td.planet { font-family: var(--mono); font-size: 11px; color: var(--fg-muted) }
.mft td.title { color: var(--fg-emph); font-weight: 500 }
.mft td.why { color: var(--fg-primary); font-size: 11.5px }
.mft code { background: var(--bg-card-alt); padding: 1px 5px; border-radius: 3px; font-size: 10.5px }

.tier-pill { display: inline-block; padding: 2px 9px; border-radius: 10px; font-size: 11px; font-weight: 700; letter-spacing: .3px; margin-right: 6px }
.tier-A { background: rgba(216,160,64,0.15); color: var(--warn-soft); border: 1px solid rgba(216,160,64,0.35) }
.tier-B { background: rgba(74,136,184,0.12); color: var(--accent-hover); border: 1px solid rgba(74,136,184,0.30) }
.tier-C { background: var(--bg-card-alt); color: var(--fg-dim); border: 1px solid var(--bd-strong) }

.system-card { border: 1px solid var(--bd-strong); border-radius: 6px; padding: 16px 18px; background: var(--bg-card); margin-bottom: 24px }
.system-card h3.sys { font-family: var(--sans); font-size: 15px; color: var(--fg-emph); text-transform: none; letter-spacing: 0; margin: 0 0 4px; font-weight: 700 }
.system-card .stat { color: var(--fg-muted); font-size: 11.5px; margin: 0 0 12px }

.tips { list-style: decimal; padding-left: 24px; color: var(--fg-muted); font-size: 12.5px; line-height: 1.7 }
.tips li { margin-bottom: 4px }

.lang-toggle { margin-left: auto }

@media (max-width: 600px) {
  .mft thead { display: none }
  .mft, .mft tbody, .mft tr, .mft td { display: block; width: 100% }
  .mft tr { border: 1px solid #1a2333; border-radius: 6px; padding: 8px 11px; margin-bottom: 8px; background: #0a1018 }
  .mft td { display: flex; justify-content: space-between; align-items: baseline; border: none; padding: 3px 0; gap: 10px; font-size: 12px }
  .mft td::before {
    content: attr(data-label);
    color: #5a7090; font-size: 10px; text-transform: uppercase; letter-spacing: .4px;
    font-family: var(--sans); font-weight: 600; flex-shrink: 0
  }
  .mft td.title, .mft td.why { display: block }
  .mft td.title::before, .mft td.why::before { display: block; margin-bottom: 3px }
}
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
<section>
  <p class="intro" data-i18n="intro_p1"></p>
  <p class="intro" data-i18n="intro_p2"></p>
</section>

__SYSTEMS__

__BIB_AUTO__

<section>
  <h2 data-i18n="tips_h2"></h2>
  <ol class="tips">
__TIPS__
  </ol>
</section>
</main>

<footer>
  <span data-i18n="footer_note"></span>
</footer>

<script>
const T = __I18N_DICT__;

let lang = localStorage.getItem('nearstars-lang') || 'ko';

function applyLang() {
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const v = T[lang][el.dataset.i18n];
    if (v !== undefined) el.innerHTML = v;
  });
  document.querySelectorAll('#lang-seg button').forEach(b => {
    b.classList.toggle('on', b.dataset.lang === lang);
  });
}

document.getElementById('lang-seg').addEventListener('click', e => {
  const btn = e.target.closest('button[data-lang]');
  if (!btn) return;
  lang = btn.dataset.lang;
  localStorage.setItem('nearstars-lang', lang);
  applyLang();
});

applyLang();
</script>

</body>
</html>
'''


def display_system_name(slug: str) -> str:
    """trappist_1 → TRAPPIST-1, alpha_centauri_proxima → Alpha Centauri Proxima."""
    parts = slug.split('_')
    # 토큰 2개 + 마지막이 숫자 → acronym + 번호 패턴 (trappist_1, gj_667)
    if len(parts) == 2 and parts[-1].isdigit():
        return f"{parts[0].upper()}-{parts[-1]}"
    # 일반 시스템 → Title Case + 공백 join
    return ' '.join(p.capitalize() for p in parts)


def render_systems(systems: list) -> str:
    """systems = [{'slug', 'name', 'data', 'ko'}] — ko is sidecar dict or {}."""
    out = []
    for s in systems:
        data = s['data']
        ko = s.get('ko') or {}
        ko_a = ko.get('tier_a', {})
        ko_b = ko.get('tier_b', {})
        a_count = max(0, len(data['A']) - 1)
        b_count = max(0, len(data['B']) - 1)
        out.append(
            f'<section class="system-card">\n'
            f'  <h3 class="sys">{html.escape(s["name"])}</h3>\n'
            f'  <p class="stat"><span data-i18n="stat_label"></span> '
            f'<span class="tier-pill tier-A">A · {a_count}</span>'
            f'<span class="tier-pill tier-B">B · {b_count}</span>'
            + (f'<span class="tier-pill tier-C" title="{html.escape(data["C_prose"])}">'
               'C · skip-list</span>' if data['C_prose'] else '')
            + '</p>\n'
            f'  <h3 data-i18n="tier_A_h3"></h3>\n'
            f'  {render_table(data["A"], ko_a)}\n'
            f'  <h3 data-i18n="tier_B_h3"></h3>\n'
            f'  {render_table(data["B"], ko_b)}\n'
            + (f'  <h3 data-i18n="tier_C_h3"></h3>\n'
               f'  <p class="note">{inline_md(data["C_prose"])}</p>\n'
               if data['C_prose'] else '')
            + '</section>'
        )
    return '\n'.join(out)


def render_tips(systems: list) -> str:
    """Tips are the same across systems for now — take the first system's tip list."""
    tips = []
    for s in systems:
        if s['data']['fetching_tips']:
            tips = s['data']['fetching_tips']
            break
    return '\n'.join(f'    <li>{inline_md(t)}</li>' for t in tips)


def build_i18n(systems: list) -> str:
    """Return JS-literal i18n dictionary, including per-row translations
    collected during table rendering (see render_paper_row)."""
    en_dict = {
        **_ROW_I18N_EN,
        'title': 'NearStars · Phase 3 manual paper fetch',
        'back_db': '← Back to database',
        'reports_index': 'Reports index',
        'intro_p1': 'Papers surfaced by ADS but without an arXiv preprint at retrieval time. Claude cannot fetch these automatically, so the Phase 3 synthesis was built without their full text.',
        'intro_p2': 'Bibcodes link to the ADS abstract page. If you can access any of these (institutional library, Nature subscription, etc.), paste the abstract or full text back into a Phase 3 session and the affected synthesis files can be revised.',
        'stat_label': 'Pending fetches:',
        'bibauto_h2': 'Auto-tracked from bibliographies',
        'bibauto_note': 'Papers flagged manual-fetch in the curated Phase 2/3 bibliographies (no arXiv preprint / paywalled / VizieR-only). Auto-aggregated from docs/phase3/_bib/*.yaml — stays current as curation proceeds.',
        'tier_A_h3': 'Tier A — likely to change cfg decisions',
        'tier_B_h3': 'Tier B — useful context',
        'tier_C_h3': 'Tier C — conference proceedings / catalogs',
        'th_bibcode': 'Bibcode',
        'th_year': 'Year',
        'th_planet': 'Planet',
        'th_title': 'Title',
        'th_why': 'Why it matters',
        'tips_h2': 'How to fetch',
        'footer_note': 'NearStars · Manual fetch index · autogenerated from phase3/<system>/manual-paper-followup.md',
    }
    ko_dict = {
        **_ROW_I18N_KO,
        'title': 'NearStars · Phase 3 수동 fetch 논문 목록',
        'back_db': '← 데이터베이스로',
        'reports_index': '보고서 인덱스',
        'intro_p1': 'ADS 에는 등록되어 있으나 fetch 시점에 arXiv preprint 가 없었던 논문들입니다. Claude 가 자동으로 가져올 수 없어서, Phase 3 합성은 이 논문들의 본문을 보지 못한 채 작성되었습니다.',
        'intro_p2': 'Bibcode 를 클릭하면 ADS abstract 페이지로 이동합니다. 어떤 경로로든 접근 가능하시면 (소속 도서관, Nature 구독 등) abstract 나 본문을 Phase 3 세션에 붙여 주시면 해당 합성 파일이 갱신됩니다.',
        'stat_label': '수동 fetch 대기:',
        'bibauto_h2': '서지에서 자동 집계',
        'bibauto_note': '큐레이션된 Phase 2/3 서지에서 수동 fetch 로 표시된 논문들 (arXiv preprint 없음 / 페이월 / VizieR 전용). docs/phase3/_bib/*.yaml 에서 자동 집계되어, 큐레이션이 진행될수록 자동으로 갱신됩니다.',
        'tier_A_h3': 'Tier A — cfg 결정을 바꿀 가능성 높음',
        'tier_B_h3': 'Tier B — 맥락에 유용',
        'tier_C_h3': 'Tier C — 학회 proceedings · catalog',
        'th_bibcode': 'Bibcode',
        'th_year': '연도',
        'th_planet': '행성',
        'th_title': '제목',
        'th_why': '왜 중요한가',
        'tips_h2': 'Fetch 방법',
        'footer_note': 'NearStars · 수동 fetch 인덱스 · phase3/<system>/manual-paper-followup.md 에서 자동 생성',
    }
    return json.dumps({'en': en_dict, 'ko': ko_dict}, ensure_ascii=False, indent=2)


def collect_bib_manual(repo: Path) -> list:
    """Auto-track manual-fetch papers from the curated Phase 2/3 bibliographies.

    Reads docs/phase3/_bib/*.yaml and collects entries flagged
    status=manual_followup/skipped (papers that can't be auto-fetched but bear
    on the synthesis). Auto-harvested mega-bibs (where >=50% of entries are
    un-fetched) and _system-* files are skipped, so only the genuine
    curation-relevant manual papers surface. Self-updating: as curation adds
    such an entry to any anchor bib, it appears here on the next build.
    """
    bib_dir = repo / 'docs' / 'phase3' / '_bib'
    out = []
    for f in sorted(bib_dir.glob('*.yaml')):
        if f.name.startswith('_system-'):
            continue
        try:
            doc = yaml.safe_load(f.read_text(encoding='utf-8')) or {}
        except Exception:
            continue
        papers = doc.get('papers') or []
        if not papers:
            continue
        manual = [p for p in papers
                  if p.get('status') in ('manual_followup', 'skipped')
                  or p.get('category') == 'manual_followup']
        if not manual or len(manual) / len(papers) >= 0.5:
            continue  # nothing to track, or an auto-harvested mega-bib
        rows = []
        for p in manual:
            bib = (p.get('ads_bibcode') or '').strip()
            yr = bib[:4] if bib[:4].isdigit() else ''
            rows.append({
                'bibcode': bib,
                'arxiv': (p.get('arxiv_id') or '').strip(),
                'title': p.get('title') or '',
                'year': yr,
            })
        out.append({'host': doc.get('host') or f.stem, 'papers': rows})
    return out


def render_bib_auto(bib_systems: list) -> str:
    """One card per system, listing its bibliography manual-fetch entries."""
    if not bib_systems:
        return ''
    cards = []
    for s in bib_systems:
        body = '\n'.join(
            '        <tr>'
            '<td class="bib" data-label="Bibcode">'
            + (f'<a href="{html.escape(ADS_BASE + p["bibcode"] + "/abstract")}" target="_blank" rel="noopener">{html.escape(p["bibcode"])}</a>'
               if p['bibcode'] else html.escape(p['arxiv'] or '—'))
            + '</td>'
            f'<td class="year" data-label="Year">{html.escape(p["year"])}</td>'
            f'<td class="title" data-label="Title">{inline_md(p["title"])}</td>'
            '</tr>'
            for p in s['papers'])
        cards.append(
            '<section class="system-card">\n'
            f'  <h3 class="sys">{html.escape(s["host"])}</h3>\n'
            '  <table class="mft">\n'
            '    <thead><tr><th data-i18n="th_bibcode"></th><th data-i18n="th_year"></th><th data-i18n="th_title"></th></tr></thead>\n'
            f'    <tbody>\n{body}\n    </tbody>\n'
            '  </table>\n'
            '</section>')
    return (
        '<section>\n'
        '  <h2 data-i18n="bibauto_h2"></h2>\n'
        '  <p class="note" data-i18n="bibauto_note"></p>\n'
        + '\n'.join(cards)
        + '\n</section>')


def main() -> int:
    here = Path(__file__).resolve()
    repo = here.parent.parent.parent

    phase3_root = repo / 'phase3'
    md_files = sorted(phase3_root.glob('*/manual-paper-followup.md'))

    if not md_files:
        print('No phase3/<system>/manual-paper-followup.md found — nothing to build.')
        return 0

    _reset_row_i18n()
    systems = []
    for md in md_files:
        slug = md.parent.name
        ko_sidecar = md.with_suffix('.ko.json')
        ko_data = {}
        if ko_sidecar.exists():
            ko_data = json.loads(ko_sidecar.read_text(encoding='utf-8'))
        systems.append({
            'slug': slug,
            'name': display_system_name(slug),
            'data': parse_md(md),
            'ko': ko_data,
        })

    # Render in this order — render_systems populates _ROW_I18N_* dicts
    # which build_i18n then reads.
    systems_html = render_systems(systems)
    tips_html = render_tips(systems)
    bib_auto = collect_bib_manual(repo)
    bib_auto_html = render_bib_auto(bib_auto)
    page = (PAGE_TEMPLATE
        .replace('__SYSTEMS__', systems_html)
        .replace('__BIB_AUTO__', bib_auto_html)
        .replace('__TIPS__', tips_html)
        .replace('__I18N_DICT__', build_i18n(systems)))

    out = repo / 'docs' / 'phase3' / 'manual-fetch.html'
    out.write_text(page, encoding='utf-8')
    total_a = sum(max(0, len(s['data']['A']) - 1) for s in systems)
    total_b = sum(max(0, len(s['data']['B']) - 1) for s in systems)
    total_bib = sum(len(s['papers']) for s in bib_auto)
    print(f'wrote {out.relative_to(repo)}  ({len(systems)} md-systems, '
          f'{total_a} Tier A + {total_b} Tier B; {len(bib_auto)} bib-systems, '
          f'{total_bib} auto-tracked papers)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
