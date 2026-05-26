# db/refs/element_plasma_colors.yaml + emit_firefly_cfg.py 의 팔레트 상수를 단일 HTML 시각화 페이지로 렌더
"""Render docs/firefly-colors.html — a single-page visualization of:

  1. The periodic table colored by db/refs/element_plasma_colors.yaml
     (replaces visual reference to the gradient-blurry Helmenstine chart).
  2. The 6 bulk-gas reentry palettes from emit_firefly_cfg.py PALETTES.
  3. The secondary streak palette from emit_firefly_cfg.py STREAK_PALETTE.
  4. The currently-emitted bodies' full ATMOFX_BODY color stacks,
     derived from docs/phase3/*.md the same way the emitter does.

Bilingual (한/EN toggle) following the project's data-i18n + lang-seg
pattern. Output is self-contained except for the shared style.css.

Run after editing the YAML DB or the emitter constants.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".claude/skills/firefly-cfg/scripts"))
from emit_firefly_cfg import (  # noqa: E402
    PALETTES, STREAK_PALETTE, DEFAULTS_HEX_RGB,
    parse_present, parse_pressure_pa, parse_composition,
    extract_decisions, pick_palette, pressure_to_strength,
    PRESSURE_THRESHOLD_PA, slug_to_kopernicus_name, planet_letter_uppercase,
)

DB_PATH = ROOT / "db" / "refs" / "element_plasma_colors.yaml"
PHASE3_DIR = ROOT / "docs" / "phase3"
OUT = ROOT / "docs" / "firefly-colors.html"


# ── Periodic-table layout ──────────────────────────────────────────

def build_layout() -> dict[int, tuple[int, int]]:
    """atomic_number → (grid_row, grid_column). Rows 8–9 = f-block."""
    pos = {1: (1, 1), 2: (1, 18)}
    pos.update({3: (2, 1), 4: (2, 2)})
    pos.update({z: (2, c) for c, z in zip(range(13, 19), range(5, 11))})
    pos.update({11: (3, 1), 12: (3, 2)})
    pos.update({z: (3, c) for c, z in zip(range(13, 19), range(13, 19))})
    pos.update({z: (4, c) for c, z in enumerate(range(19, 37), start=1)})
    pos.update({z: (5, c) for c, z in enumerate(range(37, 55), start=1)})
    pos.update({55: (6, 1), 56: (6, 2)})
    pos.update({z: (6, c) for c, z in enumerate(range(72, 87), start=4)})
    pos.update({87: (7, 1), 88: (7, 2)})
    pos.update({z: (7, c) for c, z in enumerate(range(104, 119), start=4)})
    # f-block: La..Lu (57..71) in row 8 cols 3..17, Ac..Lr (89..103) in row 9 cols 3..17
    pos.update({z: (8, c) for c, z in enumerate(range(57, 72), start=3)})
    pos.update({z: (9, c) for c, z in enumerate(range(89, 104), start=3)})
    return pos


# ── Color helpers ──────────────────────────────────────────────────

def luminance(hexstr: str) -> float:
    """Relative luminance per WCAG; for picking light vs dark text."""
    r, g, b = (int(hexstr[i:i + 2], 16) / 255 for i in (1, 3, 5))
    def chan(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def text_on(hexstr: str) -> str:
    return "#000" if luminance(hexstr) > 0.4 else "#fff"


def rgb_intensity_to_hex(rgb_i: tuple) -> str:
    r, g, b, _ = rgb_i
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


# ── Periodic table HTML ────────────────────────────────────────────

STATUS_CHIP_EN = {
    "visible": "",
    "no_flame_color": "no flame",
    "not_visible_to_humans": "UV/IR only",
    "too_radioactive": "radioactive",
    "too_short": "synthetic",
    "no_data": "no data",
}

STATUS_CHIP_KO = {
    "visible": "",
    "no_flame_color": "불꽃없음",
    "not_visible_to_humans": "가시광선밖",
    "too_radioactive": "방사능",
    "too_short": "합성원소",
    "no_data": "자료없음",
}


def render_periodic_table(db: dict, layout: dict) -> str:
    cells = []
    for sym, e in db.items():
        z = e["atomic_number"]
        if z not in layout:
            continue
        row, col = layout[z]
        hex_val = e.get("hex")
        if hex_val:
            bg = f"background:{hex_val}"
            fg = f"color:{text_on(hex_val)}"
            cls = "element-cell"
            chip = ""
        else:
            bg = ""
            fg = ""
            cls = "element-cell no-data"
            chip = f'<span class="chip">{STATUS_CHIP_EN[e["status"]]}</span>'
        tip_basis = html.escape(e.get("basis", ""))
        tip_source = html.escape(e.get("source", ""))
        cells.append(
            f'<div class="{cls}" style="grid-row:{row};grid-column:{col};{bg};{fg}" '
            f'title="{html.escape(e["name"])} ({sym}, Z={z}) — {tip_basis}">'
            f'<span class="z">{z}</span>'
            f'<span class="sym">{sym}</span>'
            f'<span class="name">{html.escape(e["name"])}</span>'
            f'{chip}'
            f'</div>'
        )
    return '<div class="periodic-table">\n' + "\n".join(cells) + "\n</div>"


# ── Palette card HTML ──────────────────────────────────────────────

PALETTE_DESCRIPTORS = {
    "earth_like":  ("N2 + O2 (Earth/Trappist-1 e)",  "N2 또는 O2 우점 (Earth/Trappist-1 e)"),
    "co2":         ("CO2 (Mars/Venus)",              "CO2 우점 (Mars/Venus)"),
    "gas_giant":   ("H2 + He (Gas giant)",           "H2 + He (가스 자이언트)"),
    "methane":     ("CH4 (Titan)",                   "CH4 (타이탄)"),
    "steam":       ("H2O (Steam atmosphere)",        "H2O (수증기 대기)"),
    "pure_h2":     ("Pure H2 (Cold sub-Neptune)",    "순수 H2 (차가운 sub-Neptune)"),
}


def render_palette_card(name: str, palette: dict) -> str:
    desc_en, desc_ko = PALETTE_DESCRIPTORS[name]
    swatches = []
    # Show all 9 ATMOFX_BODY Color keys in canonical order
    ordered = [
        ("glow",            DEFAULTS_HEX_RGB["glow"]),
        ("glow_hot",        DEFAULTS_HEX_RGB["glow_hot"]),
        ("trail_primary",   palette["trail_primary"]),
        ("trail_secondary", palette["trail_secondary"]),
        ("trail_tertiary",  palette["trail_tertiary"]),
        ("trail_streak",    palette["trail_primary"]),   # default streak fallback
        ("wrap_layer",      palette["wrap_layer"]),
        ("wrap_streak",     palette["trail_primary"]),
        ("shockwave",       palette["shockwave"]),
    ]
    for role, rgb_i in ordered:
        hex_val = rgb_intensity_to_hex(rgb_i)
        r, g, b, i = rgb_i
        fg = text_on(hex_val)
        swatches.append(
            f'<div class="palette-swatch" style="background:{hex_val};color:{fg}">'
            f'<span class="role">{role}</span>'
            f'<span class="hex">{hex_val}</span>'
            f'<span class="rgbi">{int(r)} {int(g)} {int(b)} ×{i:g}</span>'
            f'</div>'
        )
    return (
        f'<div class="palette-card" data-palette="{name}">'
        f'<h3><span data-i18n-h="palette_{name}_label"></span></h3>'
        f'<p class="palette-rule"><span data-i18n="palette_{name}_rule"></span></p>'
        f'<div class="palette-swatches">'
        + "".join(swatches)
        + f'</div>'
        f'<p class="palette-note"><span data-i18n="palette_{name}_note"></span></p>'
        f'</div>'
    )


def render_palettes_section(palettes: dict) -> str:
    cards = "\n".join(render_palette_card(name, p) for name, p in palettes.items())
    return f'<div class="palette-grid">{cards}</div>'


# ── Streak table ──────────────────────────────────────────────────

STREAK_USECASE_EN = {
    "CO2": "CN/Swan band in N2/O2 atmosphere",
    "CH4": "Titan-class secondary",
    "H2O": "Steam admixture",
    "He":  "Gas-giant secondary",
    "SO2": "Venus-class trace sulfur",
    "H2S": "Reducing atmosphere sulfur",
    "Na":  "Lava world / sub-Neptune alkali",
    "K":   "Alkali vapor on hot rocky",
    "Fe":  "Rock ablation / vapor",
    "Mg":  "Meteor-class rock vapor",
    "CN":  "Tholin haze chemistry",
    "O2":  "Oxygenic photochemistry trace",
    "N2":  "Reducing trace nitrogen",
    "Ar":  "Noble-gas trace",
}

STREAK_USECASE_KO = {
    "CO2": "N2/O2 대기 안의 CN/Swan 밴드",
    "CH4": "타이탄 계열 2차 종",
    "H2O": "수증기 혼합",
    "He":  "가스 자이언트 2차",
    "SO2": "Venus 계열 황 화합물",
    "H2S": "환원성 대기 황",
    "Na":  "용암 행성 / sub-Neptune 알칼리",
    "K":   "고온 암석 행성 알칼리 vapor",
    "Fe":  "암석 ablation/증기",
    "Mg":  "유성 계열 암석 증기",
    "CN":  "Tholin haze 광화학",
    "O2":  "산소성 광화학 미량",
    "N2":  "환원 미량 질소",
    "Ar":  "비활성 기체 trace",
}


def render_streak_table() -> str:
    rows = []
    for sp, rgb_i in STREAK_PALETTE.items():
        hex_val = rgb_intensity_to_hex(rgb_i)
        r, g, b, i = rgb_i
        fg = text_on(hex_val)
        rows.append(
            f'<tr>'
            f'<td class="sp">{sp}</td>'
            f'<td><span class="swatch-inline" style="background:{hex_val};color:{fg}">{hex_val}</span></td>'
            f'<td class="rgbi">{int(r)} {int(g)} {int(b)} ×{i:g}</td>'
            f'<td data-i18n="streak_{sp}_use"></td>'
            f'</tr>'
        )
    return (
        '<table class="streak-table"><thead><tr>'
        '<th data-i18n="th_streak_species"></th>'
        '<th data-i18n="th_streak_color"></th>'
        '<th data-i18n="th_streak_rgb"></th>'
        '<th data-i18n="th_streak_use"></th>'
        '</tr></thead><tbody>'
        + "".join(rows) +
        '</tbody></table>'
    )


# ── Currently-emitted bodies ───────────────────────────────────────

def derive_body_palette(slug: str, db: dict):
    """Re-derive the palette decision for a body the same way the emitter does."""
    md_path = PHASE3_DIR / f"{slug}.md"
    if not md_path.exists():
        return None
    text = md_path.read_text(encoding="utf-8")
    dec = extract_decisions(text)
    if not dec or "atmosphere_present" not in dec:
        return None
    if not parse_present(dec["atmosphere_present"]):
        return None
    pressure_raw = dec.get("atmosphere_surface_pressure_pa") or dec.get("atmosphere_pressure_pa")
    if not pressure_raw:
        return None
    pressure_pa = parse_pressure_pa(pressure_raw)
    if pressure_pa is None or pressure_pa < PRESSURE_THRESHOLD_PA:
        return None
    comp_raw = dec.get("atmosphere_composition") or "N2 78%, O2 21%"
    species = parse_composition(comp_raw) or [("N2", 78), ("O2", 21)]
    species_set = {s for s, _ in species}
    dominant = species[0][0]
    palette_name, palette = pick_palette(dominant, species_set)

    # Streak: first matching secondary
    streak_rgb = palette["trail_primary"]
    streak_sp = None
    for sp, pct in species[1:]:
        if pct is None or 0.5 <= pct <= 10.0:
            if sp in STREAK_PALETTE:
                streak_rgb = STREAK_PALETTE[sp]
                streak_sp = sp
                break
            elif sp in db and db[sp]["status"] == "visible":
                hx = db[sp]["hex"].lstrip("#")
                streak_rgb = (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16), 2.0)
                streak_sp = f"{sp} (from element DB)"
                break

    return {
        "slug": slug,
        "kop_name": planet_letter_uppercase(slug_to_kopernicus_name(slug)),
        "palette_name": palette_name,
        "palette": palette,
        "streak_rgb": streak_rgb,
        "streak_sp": streak_sp,
        "pressure_pa": pressure_pa,
        "strength": pressure_to_strength(pressure_pa / 100_000.0),
        "dominant": dominant,
        "secondaries": [s for s, _ in species[1:][:4]],
    }


def render_body_card(body: dict) -> str:
    p = body["palette"]
    ordered = [
        ("glow",            DEFAULTS_HEX_RGB["glow"]),
        ("glow_hot",        DEFAULTS_HEX_RGB["glow_hot"]),
        ("trail_primary",   p["trail_primary"]),
        ("trail_secondary", p["trail_secondary"]),
        ("trail_tertiary",  p["trail_tertiary"]),
        ("trail_streak",    body["streak_rgb"]),
        ("wrap_layer",      p["wrap_layer"]),
        ("wrap_streak",     body["streak_rgb"]),
        ("shockwave",       p["shockwave"]),
    ]
    swatches = []
    for role, rgb_i in ordered:
        hex_val = rgb_intensity_to_hex(rgb_i)
        fg = text_on(hex_val)
        swatches.append(
            f'<div class="palette-swatch" style="background:{hex_val};color:{fg}">'
            f'<span class="role">{role}</span><span class="hex">{hex_val}</span></div>'
        )
    p_bar = body["pressure_pa"] / 100_000
    secondaries = ", ".join(body["secondaries"]) or "—"
    streak_label = body["streak_sp"] or "(falls back to trail_primary)"
    return (
        f'<div class="body-card">'
        f'<h3>{body["kop_name"]} '
        f'<span class="body-slug">({body["slug"]})</span></h3>'
        f'<p class="body-meta">'
        f'<span data-i18n="body_palette_lbl"></span> <b>{body["palette_name"]}</b> · '
        f'<span data-i18n="body_pressure_lbl"></span> <code>{p_bar:.4g} bar</code> · '
        f'<span data-i18n="body_strength_lbl"></span> <code>{body["strength"]:.2f}</code></p>'
        f'<p class="body-meta">'
        f'<span data-i18n="body_dominant_lbl"></span> <code>{body["dominant"]}</code> · '
        f'<span data-i18n="body_secondary_lbl"></span> <code>{secondaries}</code> · '
        f'<span data-i18n="body_streak_lbl"></span> <code>{streak_label}</code></p>'
        f'<div class="palette-swatches">'
        + "".join(swatches) +
        f'</div></div>'
    )


# ── Build i18n dict ────────────────────────────────────────────────

def build_t(palettes, palette_descriptors):
    t_en = {
        "title": "Plasma & reentry color reference",
        "intro_1": "Per-element flame/plasma colors plus the bulk-gas reentry palettes used by the Firefly emitter. Source of truth: <code>db/refs/element_plasma_colors.yaml</code> + <code>.claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py</code> constants.",
        "intro_2": "Hover any periodic-table cell for its spectroscopic basis. Bulk-gas swatches show the values the emitter writes for each ATMOFX_BODY Color key.",
        "h_periodic": "Periodic table — atomic plasma colors",
        "h_bulk": "Bulk-gas reentry palettes",
        "h_streak": "Secondary-species streak palette",
        "h_bodies": "Currently emitted bodies",
        "th_streak_species": "Species",
        "th_streak_color":   "Color",
        "th_streak_rgb":     "RGB · intensity",
        "th_streak_use":     "Use case",
        "body_palette_lbl":  "palette:",
        "body_pressure_lbl": "P:",
        "body_strength_lbl": "strength:",
        "body_dominant_lbl": "dominant:",
        "body_secondary_lbl": "secondaries:",
        "body_streak_lbl":   "streak:",
    }
    t_ko = {
        "title": "플라즈마 & 재진입 색 레퍼런스",
        "intro_1": "원소별 불꽃/플라즈마 색 + Firefly emitter 가 쓰는 bulk-gas 재진입 팔레트. 정본 데이터: <code>db/refs/element_plasma_colors.yaml</code> + <code>.claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py</code> 상수.",
        "intro_2": "주기율표 셀에 마우스를 올리면 분광학적 근거가 보입니다. Bulk-gas swatch 는 emitter 가 각 ATMOFX_BODY Color 키에 쓰는 값입니다.",
        "h_periodic": "주기율표 — 원소별 플라즈마 색",
        "h_bulk": "Bulk-gas 재진입 팔레트",
        "h_streak": "2차 종 streak 팔레트",
        "h_bodies": "현재 emit 된 행성들",
        "th_streak_species": "종",
        "th_streak_color":   "색",
        "th_streak_rgb":     "RGB · 강도",
        "th_streak_use":     "사용 시점",
        "body_palette_lbl":  "팔레트:",
        "body_pressure_lbl": "압력:",
        "body_strength_lbl": "strength:",
        "body_dominant_lbl": "우점:",
        "body_secondary_lbl": "2차종:",
        "body_streak_lbl":   "streak:",
    }
    # Palette card labels
    for name in palettes:
        desc_en, desc_ko = palette_descriptors[name]
        t_en[f"palette_{name}_label"] = name
        t_ko[f"palette_{name}_label"] = name
        t_en[f"palette_{name}_rule"] = f"Trigger: {desc_en}"
        t_ko[f"palette_{name}_rule"] = f"적용 조건: {desc_ko}"
        t_en[f"palette_{name}_note"] = ""
        t_ko[f"palette_{name}_note"] = ""
    # Streak use cases
    for sp in STREAK_PALETTE:
        t_en[f"streak_{sp}_use"] = STREAK_USECASE_EN.get(sp, "")
        t_ko[f"streak_{sp}_use"] = STREAK_USECASE_KO.get(sp, "")
    return t_en, t_ko


# ── Final HTML ─────────────────────────────────────────────────────

TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title data-i18n="title"></title>
<link rel="stylesheet" href="style.css">
<style>
.periodic-table {{
  display: grid;
  grid-template-columns: repeat(18, 1fr);
  grid-template-rows: repeat(9, auto);
  gap: 3px;
  margin: 1rem 0;
}}
.element-cell {{
  position: relative;
  aspect-ratio: 1;
  padding: 4px 4px 2px 4px;
  border-radius: 3px;
  font-size: 9px;
  line-height: 1.1;
  overflow: hidden;
  cursor: help;
  border: 1px solid rgba(0,0,0,0.3);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}}
.element-cell .z {{ position: absolute; top: 2px; left: 4px; font-size: 9px; opacity: 0.85 }}
.element-cell .sym {{ font-size: 16px; font-weight: bold }}
.element-cell .name {{ font-size: 7px; opacity: 0.75; text-align: center }}
.element-cell .chip {{ position: absolute; bottom: 1px; right: 2px; font-size: 6px; opacity: 0.6 }}
.element-cell.no-data {{
  background-image: repeating-linear-gradient(45deg, #1a1828 0 4px, #2a1a38 4px 8px);
  color: #6a7898;
  border-color: #2a2030;
}}
@media (max-width: 1100px) {{
  .element-cell .sym {{ font-size: 12px }}
  .element-cell .name {{ display: none }}
}}

.palette-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}}
.palette-card {{
  background: var(--bg-card);
  border: 1px solid var(--bd-mid);
  border-radius: 4px;
  padding: 1rem;
}}
.palette-card h3 {{ margin: 0 0 0.25rem 0; font-size: 1rem; color: var(--fg-emph) }}
.palette-card .palette-rule {{ font-size: 0.85rem; color: var(--fg-muted); margin: 0 0 0.75rem 0 }}
.palette-card .palette-note {{ font-size: 0.75rem; color: var(--fg-dim); margin: 0.5rem 0 0 0 }}
.palette-swatches {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3px;
}}
.palette-swatch {{
  padding: 6px 4px;
  border-radius: 3px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 9px;
  line-height: 1.2;
  border: 1px solid rgba(0,0,0,0.3);
}}
.palette-swatch .role {{ font-weight: 600; font-size: 10px }}
.palette-swatch .hex {{ font-family: var(--mono); font-size: 9px; opacity: 0.85 }}
.palette-swatch .rgbi {{ font-family: var(--mono); font-size: 8px; opacity: 0.7 }}

.streak-table {{
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}}
.streak-table th, .streak-table td {{
  padding: 6px 8px;
  border-bottom: 1px solid var(--bd-soft);
  text-align: left;
  font-size: 13px;
}}
.streak-table td.sp {{ font-family: var(--mono); font-weight: 600 }}
.streak-table td.rgbi {{ font-family: var(--mono); font-size: 12px; color: var(--fg-muted) }}
.swatch-inline {{
  display: inline-block;
  padding: 2px 8px;
  border-radius: 3px;
  font-family: var(--mono);
  font-size: 12px;
}}

.body-card {{
  background: var(--bg-card);
  border: 1px solid var(--bd-mid);
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
}}
.body-card h3 {{ margin: 0 0 0.25rem 0; font-size: 1rem; color: var(--fg-emph) }}
.body-card .body-slug {{ font-size: 0.8rem; color: var(--fg-dim); font-weight: normal }}
.body-card .body-meta {{ font-size: 0.85rem; color: var(--fg-muted); margin: 0.25rem 0 }}
.body-card code {{ font-family: var(--mono); color: var(--fg-primary) }}

.lang-toggle {{ margin-left: auto }}
.crumb a {{ color: var(--accent); text-decoration: none }}
.crumb a:hover {{ color: var(--accent-hover); text-decoration: underline }}

main {{ padding: 1rem 1.5rem; max-width: 1500px; margin: 0 auto }}
section {{ margin: 2rem 0 }}
section h2 {{ font-size: 1.2rem; color: var(--fg-emph); margin-bottom: 0.5rem }}
.intro {{ color: var(--fg-muted); margin-bottom: 0.5rem }}
header {{
  display: flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  background: var(--bg-header);
  border-bottom: 1px solid var(--bd-soft);
}}
header h1 {{ font-size: 1.1rem; color: var(--fg-emph); margin: 0 1rem 0 0 }}
.seg {{ display: inline-flex; border: 1px solid var(--bd-input); border-radius: 4px; overflow: hidden }}
.seg button {{
  background: var(--bg-input);
  color: var(--fg-muted);
  border: none;
  padding: 4px 12px;
  cursor: pointer;
  font-family: var(--sans);
  font-size: 12px;
}}
.seg button.on {{ background: var(--bg-input-on); color: var(--fg-emph) }}
</style>
</head>
<body>
<header>
  <h1 data-i18n="title"></h1>
  <div class="crumb"><a href="index.html">← DB</a> · <a href="reports.html">reports</a></div>
  <div class="seg lang-toggle" id="lang-seg">
    <button class="on" data-lang="ko">한</button>
    <button data-lang="en">EN</button>
  </div>
</header>
<main>

<p class="intro" data-i18n="intro_1"></p>
<p class="intro" data-i18n="intro_2"></p>

<section>
<h2 data-i18n="h_periodic"></h2>
{periodic_table}
</section>

<section>
<h2 data-i18n="h_bulk"></h2>
{palettes_section}
</section>

<section>
<h2 data-i18n="h_streak"></h2>
{streak_table}
</section>

<section>
<h2 data-i18n="h_bodies"></h2>
{bodies_section}
</section>

</main>

<script>
const T = {t_json};
let lang = localStorage.getItem('nearstars-lang') || 'ko';

function applyLang() {{
  document.documentElement.lang = lang;
  document.querySelectorAll('[data-i18n]').forEach(el => {{
    const v = T[lang][el.dataset.i18n];
    if (v !== undefined) el.innerHTML = v;
  }});
  document.querySelectorAll('[data-i18n-h]').forEach(el => {{
    const v = T[lang][el.dataset.i18nH];
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
"""


def main() -> int:
    import json
    with open(DB_PATH, encoding="utf-8") as f:
        db = yaml.safe_load(f)

    layout = build_layout()
    periodic = render_periodic_table(db, layout)
    palettes_section = render_palettes_section(PALETTES)
    streak_table = render_streak_table()

    # Bodies
    body_results = []
    for slug in sorted(p.stem for p in PHASE3_DIR.glob("*.md")):
        res = derive_body_palette(slug, db)
        if res:
            body_results.append(res)
    bodies_section = "\n".join(render_body_card(b) for b in body_results)

    t_en, t_ko = build_t(PALETTES, PALETTE_DESCRIPTORS)
    t_json = json.dumps({"en": t_en, "ko": t_ko}, ensure_ascii=False)

    html_out = TEMPLATE.format(
        periodic_table=periodic,
        palettes_section=palettes_section,
        streak_table=streak_table,
        bodies_section=bodies_section,
        t_json=t_json,
    )
    OUT.write_text(html_out, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} "
          f"({len(db)} elements, {len(PALETTES)} bulk-gas palettes, "
          f"{len(STREAK_PALETTE)} streak species, {len(body_results)} bodies)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
