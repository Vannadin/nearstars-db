# 플라스마/재진입 색 레퍼런스를 단일 HTML로 렌더 (온도 슬라이더 + 조성/오로라 그리드)
"""Render docs/firefly-colors.html — plasma & reentry color reference.

Sections:
  1. Temperature slider: colors the periodic table + molecular panel by their
     computed LTE plasma emission at the selected temperature (1000-15000K)
  2. Periodic table — 118 cells, 75 with computed temperature colors
  3. Molecular panel — 30 diatomic/polyatomic species, computed vs temperature
  4. Bulk-gas reentry palettes from emit_firefly_cfg.py PALETTES (always shown)
  5. Composition / element / aurora grids; currently-emitted bodies

Temperature color tables (element_temperature_colors.yaml +
molecular_temperature_colors.yaml) are embedded as JSON; JavaScript swaps cell
colors as the slider moves. No server round-trip.

Run after any DB update or palette change.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "refs"))
import cie_color                        # noqa: E402  (aurora emitter swatches)
sys.path.insert(0, str(ROOT / ".claude/skills/firefly-cfg/scripts"))
from emit_firefly_cfg import (  # noqa: E402
    PALETTES, STREAK_PALETTE, DEFAULTS_HEX_RGB,
    parse_present, parse_pressure_pa, parse_composition,
    extract_decisions, pick_palette, pressure_to_strength,
    engine_palette, escape_velocity_kms,
    PRESSURE_THRESHOLD_PA, slug_to_kopernicus_name, planet_letter_uppercase,
)

ELEMENT_DB = ROOT / "db" / "refs" / "element_plasma_colors.yaml"
MOLECULAR_DB = ROOT / "db" / "refs" / "molecular_plasma_colors.yaml"
PLASMA_TEMP_DB = ROOT / "db" / "refs" / "plasma_temperature_colors.yaml"
ELEMENT_TEMP_DB = ROOT / "db" / "refs" / "element_temperature_colors.yaml"
MOL_TEMP_DB = ROOT / "db" / "refs" / "molecular_temperature_colors.yaml"
AURORA_COLORS_DB = ROOT / "db" / "refs" / "aurora_colors.yaml"
AURORA_LINES_DB = ROOT / "db" / "refs" / "aurora_lines.yaml"
PHASE3_DIR = ROOT / "docs" / "phase3"
OUT = ROOT / "docs" / "firefly-colors.html"


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
    pos.update({z: (8, c) for c, z in enumerate(range(57, 72), start=3)})
    pos.update({z: (9, c) for c, z in enumerate(range(89, 104), start=3)})
    return pos


def luminance(hexstr: str) -> float:
    r, g, b = (int(hexstr[i:i + 2], 16) / 255 for i in (1, 3, 5))
    def chan(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def text_on(hexstr: str) -> str:
    return "#000" if luminance(hexstr) > 0.4 else "#fff"


def rgb_intensity_to_hex(rgb_i: tuple) -> str:
    r, g, b, _ = rgb_i
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"


# ── Build element data for JS (temperature table) ──────────────────

def build_element_temp_data(etc: dict) -> dict:
    """Per-element temperature colors for the slider:
    {sym: {z, name, colors: {T: {hex, ion}}}}."""
    data = {}
    for sym, e in etc.get("elements", {}).items():
        colors = {str(T): {"hex": c["hex"], "ion": c.get("ionization_fraction", 0)}
                  for T, c in e.get("colors", {}).items()}
        data[sym] = {"z": e.get("z"), "name": e.get("name"), "colors": colors}
    return data


# ── Build molecular data for JS (temperature table) ────────────────

def build_molecule_temp_data(mtc: dict) -> dict:
    """Per-molecule temperature colors for the slider:
    {formula: {atoms, dropped?, note?, colors: {T: {hex, dom}}}}."""
    data = {}
    for formula, m in mtc.get("molecules", {}).items():
        colors = {str(T): {"hex": c["hex"], "dom": c.get("dominant", "")}
                  for T, c in m.get("colors", {}).items()}
        entry = {"atoms": m.get("atoms"), "colors": colors}
        if m.get("dropped"):
            entry["dropped"] = m["dropped"]
        if m.get("note"):
            entry["note"] = m["note"]
        data[formula] = entry
    return data


# ── Periodic table (cells without colors; JS fills per slider temperature) ────

def render_periodic_table(db: dict, layout: dict) -> str:
    cells = []
    for sym, e in sorted(db.items(), key=lambda kv: kv[1]["atomic_number"]):
        z = e["atomic_number"]
        if z not in layout:
            continue
        row, col = layout[z]
        cells.append(
            f'<div class="el-cell" data-sym="{sym}" '
            f'style="grid-row:{row};grid-column:{col}">'
            f'<span class="z">{z}</span>'
            f'<span class="sym">{sym}</span>'
            f'<span class="name">{html.escape(e["name"])}</span>'
            f'<span class="chip"></span>'
            f'</div>'
        )
    return '<div class="periodic-table" id="periodic-table">\n' + "\n".join(cells) + "\n</div>"


# ── Molecular panel ────────────────────────────────────────────────

def render_molecular_panel(mdb: dict) -> str:
    cards = []
    # Diatomic first, then polyatomic
    diatomic = [(f, m) for f, m in mdb.items() if m["atoms"] == 2]
    polyatomic = [(f, m) for f, m in mdb.items() if m["atoms"] >= 3]
    for formula, m in diatomic + polyatomic:
        kind = "diatomic" if m["atoms"] == 2 else "polyatomic"
        cards.append(
            f'<div class="mol-cell" data-formula="{formula}" data-kind="{kind}">'
            f'<span class="mol-formula">{html.escape(formula)}</span>'
            f'<span class="mol-atoms">{m["atoms"]}-atom</span>'
            f'<span class="mol-status"></span>'
            f'</div>'
        )
    return (
        '<div class="molecular-panel" id="molecular-panel">'
        + "".join(cards)
        + '</div>'
    )


# ── Bulk-gas palettes (always shown) ───────────────────────────────

PALETTE_DESCRIPTORS = {
    "earth_like":  ("N2 / O2 (Earth, Trappist-1 e)",  "N2 / O2 우점 (Earth, Trappist-1 e)"),
    "co2":         ("CO2 (Mars / Venus)",             "CO2 우점 (Mars / Venus)"),
    "ice_giant":   ("H2 + He + CH4 / NH3 (Uranus / Neptune)",
                    "H2 + He + CH4 / NH3 (Uranus / Neptune)"),
    "gas_giant":   ("H2 + He (Jupiter / Saturn)",     "H2 + He (Jupiter / Saturn)"),
    "methane":     ("CH4-dominant (hypothetical — Titan is N2-bulk)",
                    "CH4 우점 (가상 — 타이탄은 N2 벌크)"),
    "steam":       ("H2O (Steam atmosphere)",         "H2O (수증기 대기)"),
    "pure_h2":     ("Pure H2 (Cold sub-Neptune)",     "순수 H2 (차가운 sub-Neptune)"),
}


def render_palette_card(name: str, palette: dict) -> str:
    swatches = []
    ordered = [
        ("glow",            DEFAULTS_HEX_RGB["glow"]),
        ("glow_hot",        DEFAULTS_HEX_RGB["glow_hot"]),
        ("trail_primary",   palette["trail_primary"]),
        ("trail_secondary", palette["trail_secondary"]),
        ("trail_tertiary",  palette["trail_tertiary"]),
        ("trail_streak",    palette["trail_primary"]),
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
        f'<h3>{name}</h3>'
        f'<p class="palette-rule"><span data-i18n="palette_{name}_rule"></span></p>'
        f'<div class="palette-swatches">'
        + "".join(swatches) +
        f'</div>'
        f'</div>'
    )


def render_palettes_section() -> str:
    cards = "\n".join(render_palette_card(name, p) for name, p in PALETTES.items())
    return f'<div class="palette-grid">{cards}</div>'


# ── Streak table ───────────────────────────────────────────────────

STREAK_USECASE_EN = {
    "CO2": "CN/Swan band in N2/O2 atmosphere",
    "CH4": "Titan-class CH4 → CN violet (blue, N2-rich)",
    "NH3": "Ice-giant ammonia → NH2 alpha-band (amber)",
    "H2O": "Steam admixture",
    "He":  "Gas-giant He → D3 587nm yellow (corrects Firefly scarlet)",
    "SO2": "Venus-class trace sulfur",
    "H2S": "Reducing atmosphere sulfur",
    "Na":  "Lava world / sub-Neptune alkali",
    "K":   "Alkali vapor on hot rocky",
    "Fe":  "Rock ablation / vapor",
    "Mg":  "Meteor-class rock vapor",
    "CN":  "Tholin haze chemistry",
    "O2":  "Oxygenic photochemistry trace",
    "N2":  "Venus-class N2 → N2 1st Positive (orange)",
    "Ar":  "Noble-gas trace",
}

STREAK_USECASE_KO = {
    "CO2": "N2/O2 대기 안의 CN/Swan 밴드",
    "CH4": "타이탄 계열 CH4 → CN violet (청자, N2 우점)",
    "NH3": "아이스자이언트 암모니아 → NH2 알파밴드 (호박)",
    "H2O": "수증기 혼합",
    "He":  "가스자이언트 He → D3 587nm 노랑 (Firefly 진홍 교정)",
    "SO2": "Venus 계열 황 화합물",
    "H2S": "환원성 대기 황",
    "Na":  "용암 행성 / sub-Neptune 알칼리",
    "K":   "고온 암석 행성 알칼리 vapor",
    "Fe":  "암석 ablation/증기",
    "Mg":  "유성 계열 암석 증기",
    "CN":  "Tholin haze 광화학",
    "O2":  "산소성 광화학 미량",
    "N2":  "Venus 계열 N2 → N2 1st Positive (주황)",
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


# ── Plasma color vs temperature (composition × 1000K grid) ──

def render_plasma_temp_grid() -> str:
    data = yaml.safe_load(PLASMA_TEMP_DB.read_text(encoding="utf-8"))
    cell = ("display:inline-block;width:34px;height:26px;font-size:9px;"
            "text-align:center;line-height:26px")
    head = "display:inline-block;width:34px;font-size:9px;text-align:center;color:#888"
    lab = "flex:0 0 150px;font-size:12px"
    row = "display:flex;align-items:center;margin:2px 0"

    bb = data["_blackbody"]
    bb_cells = "".join(
        f'<div style="{cell};background:{e["hex"]};color:{text_on(e["hex"])}" '
        f'title="{t}K · {e["hex"]} · {e.get("note","")}">{t // 1000}k</div>'
        for t, e in bb.items()
    )
    bb_row = (f'<div style="{row}"><div style="{lab}" data-i18n="bt_blackbody"></div>'
              f'<div>{bb_cells}</div></div>')

    comp_keys = [k for k in data if not k.startswith("_")]
    temps = sorted(data[comp_keys[0]]["colors"].keys())
    header = (f'<div style="{row}"><div style="{lab}"></div><div>'
              + "".join(f'<div style="{head}">{t // 1000}k</div>' for t in temps)
              + "</div></div>")
    rows = [header]
    for k in comp_keys:
        blk = data[k]
        cells = ""
        for t in temps:
            c = blk["colors"][t]
            hx = c["combined_hex"]
            tip = (f'{t}K · {hx} · {c["dominant"]} · '
                   f'ionz={c["ionization_fraction"]} mol={c["molecular_fraction"]} '
                   f'emis={c["emission_fraction"]}')
            cells += (f'<div style="{cell};background:{hx};color:{text_on(hx)}" '
                      f'title="{tip}"></div>')
        rows.append(f'<div style="{row}"><div style="{lab}" data-i18n="ptc_{k}"></div>'
                    f'<div>{cells}</div></div>')

    return (f'<div style="margin-bottom:8px">{bb_row}</div>'
            f'<p class="muted" data-i18n="plasma_temp_caption" '
            f'style="font-size:12px;margin:4px 0 8px"></p>'
            + "".join(rows))


# ── Per-element plasma color vs temperature (element × 1000K grid) ──

def render_element_temp_grid() -> str:
    if not ELEMENT_TEMP_DB.exists():
        return ""
    data = yaml.safe_load(ELEMENT_TEMP_DB.read_text(encoding="utf-8"))
    cell = ("display:inline-block;width:30px;height:20px;font-size:8px;"
            "text-align:center;line-height:20px")
    head = "display:inline-block;width:30px;font-size:8px;text-align:center;color:#888"
    lab = "flex:0 0 84px;font-size:11px"
    row = "display:flex;align-items:center;margin:1px 0"

    elems = data["elements"]
    temps = sorted(next(iter(elems.values()))["colors"].keys())
    bb = data["_blackbody"]
    bb_cells = "".join(
        f'<div style="{cell};background:{bb[t]["hex"]};color:{text_on(bb[t]["hex"])}" '
        f'title="{t}K · {bb[t]["hex"]} · {bb[t].get("note","")}">{t // 1000}</div>'
        for t in temps)
    bb_row = (f'<div style="{row}"><div style="{lab}" data-i18n="bt_blackbody"></div>'
              f'<div>{bb_cells}</div></div>')
    header = (f'<div style="{row}"><div style="{lab}"></div><div>'
              + "".join(f'<div style="{head}">{t // 1000}k</div>' for t in temps)
              + "</div></div>")

    rows = [header]
    for sym in sorted(elems, key=lambda s: elems[s]["z"]):
        e = elems[sym]
        cells = ""
        for t in temps:
            c = e["colors"][t]
            hx = c["hex"]
            tip = f'{e["name"]} ({sym}) · {t}K · {hx} · ionized {c["ionization_fraction"]}'
            cells += (f'<div style="{cell};background:{hx};color:{text_on(hx)}" '
                      f'title="{tip}"></div>')
        rows.append(f'<div style="{row}"><div style="{lab}">{e["z"]} {sym}</div>'
                    f'<div>{cells}</div></div>')

    return (f'<div style="margin-bottom:6px">{bb_row}</div>'
            f'<p class="muted" data-i18n="element_temp_caption" '
            f'style="font-size:12px;margin:4px 0 8px"></p>'
            + "".join(rows))


# ── Firefly stock cfg colors (reference) ──
# Extracted from Firefly (M1rageDev/Firefly, GPL-3.0) GameData/Firefly/Configs/
# Default.cfg + Stock/*.cfg. The 9 ATMOFX_BODY Color slots [R G B intensity].
FIREFLY_STOCK = {
    "Default": {"glow":[191,80,50,1.4],"glow_hot":[191,90,65,2.5],"trail_primary":[191,99,72,3.0],
        "trail_secondary":[191,70,42,1.5],"trail_tertiary":[74,80,191,2.0],"trail_streak":[74,80,191,2.0],
        "wrap_layer":[69,69,191,2.0],"wrap_streak":[191,99,72,3.0],"shockwave":[74,90,191,3.0]},
    "Kerbin (N2/O2)": {"glow":[191,80,50,1.4],"glow_hot":[191,90,65,2.5],"trail_primary":[191,99,72,3.0],
        "trail_secondary":[191,70,42,1.5],"trail_tertiary":[74,80,191,2.0],"trail_streak":[74,80,191,2.0],
        "wrap_layer":[69,69,191,2.0],"wrap_streak":[191,99,72,3.0],"shockwave":[74,90,191,3.0]},
    "Eve (CO2)": {"glow":[191,80,50,1.4],"glow_hot":[191,90,65,2.5],"trail_primary":[83,92,191,2.0],
        "trail_secondary":[52,102,191,2.0],"trail_tertiary":[122,191,170,2.0],"trail_streak":[122,191,170,2.0],
        "wrap_layer":[125,185,191,2.0],"wrap_streak":[70,95,191,1.5],"shockwave":[96,191,159,3.0]},
    "Duna (CO2 thin)": {"glow":[191,80,50,1.4],"glow_hot":[191,90,65,2.5],"trail_primary":[76,116,191,2.5],
        "trail_secondary":[151,130,191,1.8],"trail_tertiary":[191,124,73,2.0],"trail_streak":[191,124,73,2.0],
        "wrap_layer":[191,124,73,2.0],"wrap_streak":[76,116,191,2.5],"shockwave":[34,41,191,3.0]},
    "Jool (H2/He)": {"glow":[191,80,50,1.4],"glow_hot":[191,90,65,2.5],"trail_primary":[32,20,191,1.4],
        "trail_secondary":[191,6,6,3.0],"trail_tertiary":[191,191,88,1.7],"trail_streak":[191,191,88,1.7],
        "wrap_layer":[69,69,191,2.0],"wrap_streak":[32,20,191,1.4],"shockwave":[140,191,161,1.0]},
}
FIREFLY_SLOTS = [
    ("shockwave", "bow shock"), ("wrap_layer", "envelope"), ("wrap_streak", "envelope streak"),
    ("trail_primary", "trail (inner)"), ("trail_secondary", "trail (mid)"), ("trail_tertiary", "trail (outer)"),
    ("trail_streak", "trail streak"), ("glow_hot", "hull (hot)"), ("glow", "hull"),
]


def render_firefly_stock() -> str:
    cell = ("display:inline-block;width:62px;height:40px;font-size:8px;text-align:center;"
            "line-height:1.1;border-radius:3px;margin:1px;vertical-align:top;padding-top:2px")
    lab = "flex:0 0 120px;font-size:12px"
    row = "display:flex;align-items:flex-start;margin:3px 0"
    head = ('<div style="' + row + '"><div style="' + lab + '"></div><div>'
            + "".join(f'<div style="display:inline-block;width:62px;font-size:8px;text-align:center;'
                      f'color:#888;margin:1px">{slot}<br>{region}</div>' for slot, region in FIREFLY_SLOTS)
            + '</div></div>')
    rows = [head]
    for body, cols in FIREFLY_STOCK.items():
        cells = ""
        for slot, _ in FIREFLY_SLOTS:
            r, g, b, inten = cols[slot]
            hx = f"#{r:02x}{g:02x}{b:02x}"
            cells += (f'<div style="{cell};background:{hx};color:{text_on(hx)}" '
                      f'title="{body} · {slot} = {r} {g} {b} (×{inten})">{r} {g} {b}<br>×{inten}</div>')
        rows.append(f'<div style="{row}"><div style="{lab}">{html.escape(body)}</div><div>{cells}</div></div>')
    return ('<p class="muted" data-i18n="firefly_stock_caption" style="font-size:12px;margin:4px 0 8px"></p>'
            + "".join(rows))


# ── Aurora color vs density/altitude (non-LTE, quenching) ──

def render_aurora_grid() -> str:
    """Density-slider skeleton: one cell per atmosphere, JS-colored at the selected
    density (≈ altitude). The AURORA color data is embedded as JSON in main()."""
    if not AURORA_COLORS_DB.exists():
        return ""
    data = yaml.safe_load(AURORA_COLORS_DB.read_text(encoding="utf-8"))
    cells = "".join(
        f'<div class="aurora-cell" data-atm="{key}">'
        f'<span class="aurora-atm">{html.escape(blk["label"])}</span>'
        f'<span class="aurora-dom"></span><span class="aurora-hex"></span></div>'
        for key, blk in data.items()
    )
    return (
        '<p class="muted" data-i18n="aurora_caption" style="font-size:12px;margin:4px 0 8px"></p>'
        '<div class="regime-bar" id="aurora-bar">'
        '<span class="label" data-i18n="density_label"></span>'
        '<input type="range" id="density-slider" min="7" max="14" step="1" value="11">'
        '<span id="density-readout" class="temp-readout"></span></div>'
        f'<div class="aurora-panel" id="aurora-panel">{cells}</div>'
    )


# ── Aurora emitter catalog (per-emitter table: lines, band, color) ──

def _aurora_emitter_color(lines: list):
    """A-weighted CIE color from an emitter's own lines; None if no visible content."""
    inten = []
    for lam in cie_color.LAMBDAS:
        j = 0.0
        for ln in lines:
            d = (lam - ln["nm"]) / 2.5
            if -6 < d < 6:
                j += ln["A"] * 2.718 ** (-0.5 * d * d)
        inten.append(j)
    return cie_color.spectrum_to_hex(inten) if max(inten) > 0 else None


def _aurora_band(lines: list) -> str:
    nm = max(lines, key=lambda l: l["A"])["nm"]      # brightest line
    return "FUV" if nm < 200 else "UV" if nm < 380 else "vis" if nm <= 750 else "NIR"


def render_aurora_emitters() -> str:
    if not AURORA_LINES_DB.exists():
        return ""
    data = yaml.safe_load(AURORA_LINES_DB.read_text(encoding="utf-8"))["emitters"]
    rows = []
    for name, e in data.items():
        lines = e["lines"]
        band = _aurora_band(lines)
        hexv = _aurora_emitter_color(lines) if band == "vis" else None
        nm_list = ", ".join(f'{ln["nm"]:g}' for ln in lines)
        typ_key = "ae_forbidden" if e.get("forbidden") else "ae_allowed"
        catalog = ' <span class="muted">· catalog</span>' if e.get("catalog_only") else ""
        forb = 1 if e.get("forbidden") else 0
        atot = e.get("A_total", "")                      # for the φ(n) survival curve
        ksum = sum(e["quench"].values()) if e.get("quench") else ""
        if hexv:
            sw = (f'<span class="swatch-inline" style="background:{hexv};'
                  f'color:{text_on(hexv)}">{hexv}</span>')
        else:
            sw = f'<span class="swatch-inline" style="background:#1b1b1b;color:#888">{band}</span>'
        rows.append(
            f'<tr data-forbidden="{forb}" data-atot="{atot}" data-ksum="{ksum}">'
            f'<td>{sw}</td><td class="sp">{html.escape(name)}</td>'
            f'<td>{html.escape(str(e["source"]))}</td>'
            f'<td class="rgbi">{nm_list}</td>'
            f'<td>{band}{catalog}</td>'
            f'<td data-i18n="{typ_key}"></td>'
            f'<td class="ae-surv rgbi"></td></tr>'
        )
    return (
        '<p class="muted" data-i18n="aurora_emitters_caption" style="font-size:12px;margin:4px 0 8px"></p>'
        '<table class="streak-table" id="aurora-emitters"><thead><tr>'
        '<th data-i18n="th_ae_color"></th><th data-i18n="th_ae_emitter"></th>'
        '<th data-i18n="th_ae_source"></th><th data-i18n="th_ae_lines"></th>'
        '<th data-i18n="th_ae_band"></th><th data-i18n="th_ae_type"></th>'
        '<th data-i18n="th_ae_survival"></th>'
        '</tr></thead><tbody>' + "".join(rows) + '</tbody></table>'
    )


# ── Emitted body cards (same logic as before; uses atomic_flame for element streak) ──

def derive_body_palette(slug: str, db: dict):
    md_path = PHASE3_DIR / f"{slug}.md"
    if not md_path.exists():
        return None
    text = md_path.read_text(encoding="utf-8")
    dec = extract_decisions(text)
    if not dec or "atmosphere_present" not in dec:
        return None
    if not parse_present(dec["atmosphere_present"]):
        return None
    # Gas/ice giants have no solid surface, so Phase 3 records their cfg-reference
    # level under atmosphere_reference_pressure_pa instead of *_surface_pressure_pa.
    # Mirror emit_firefly_cfg.py's lookup so the visualizer shows the same bodies
    # the cfg writer actually emits.
    pressure_raw = (dec.get("atmosphere_surface_pressure_pa")
                    or dec.get("atmosphere_pressure_pa")
                    or dec.get("atmosphere_reference_pressure_pa"))
    if not pressure_raw:
        return None
    pressure_pa = parse_pressure_pa(pressure_raw)
    if pressure_pa is None or pressure_pa < PRESSURE_THRESHOLD_PA:
        return None
    comp_raw = dec.get("atmosphere_composition") or "N2 78%, O2 21%"
    species = parse_composition(comp_raw) or [("N2", 78), ("O2", 21)]
    species_set = {s for s, _ in species}
    dominant = species[0][0]
    # Mirror emit_firefly_cfg.process_slug: engine-computed palette primary,
    # hand-tuned PALETTES only as fallback. (Without this the preview showed the
    # fallback, NOT what the cfg writer actually emits.)
    velocity = escape_velocity_kms(dec) or 7.8
    ep = engine_palette(species, velocity)
    if ep is not None:
        palette, palette_name = ep, f"engine:{dominant}@{velocity:.1f}km/s"
    else:
        palette_name, palette = pick_palette(dominant, species_set)

    streak_rgb = palette["trail_primary"]
    streak_sp = None
    for sp, pct in species[1:]:
        if pct is None or 0.5 <= pct <= 10.0:
            if sp in STREAK_PALETTE:
                streak_rgb = STREAK_PALETTE[sp]
                streak_sp = sp
                break
            elif sp in db and db[sp]["regimes"]["atomic_flame"].get("status") == "visible":
                hx = db[sp]["regimes"]["atomic_flame"]["hex"].lstrip("#")
                streak_rgb = (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16), 2.0)
                streak_sp = f"{sp} (from element DB atomic_flame)"
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


def build_t(palettes):
    t_en = {
        "title": "Plasma & reentry color reference",
        "intro_1": "First-principles LTE plasma emission colors (Saha–Boltzmann → CIE). The periodic table &amp; molecular panel are driven by the temperature slider — <code>db/refs/element_temperature_colors.yaml</code> + <code>db/refs/molecular_temperature_colors.yaml</code>. Lower sections: composition grids, the Firefly emitter palettes, and aurora.",
        "intro_2": "Drag the temperature slider — every element and molecule is colored by its computed LTE plasma emission at that temperature. Watch the molecular → atomic → ionic march. Hover a cell for detail; dim cells have no computed color at that temperature.",
        "h_periodic": "Periodic table — atomic emission",
        "h_molecular": "Molecular emitters",
        "h_bulk": "Bulk-gas fallback palettes (hand-tuned, not computed)",
        "h_streak": "Secondary-species streak palette (curated)",
        "h_plasma_temp": "Plasma color vs temperature (1000K steps)",
        "h_element_temp": "Reentry plasma color per element vs temperature (1000K steps)",
        "h_firefly_stock": "Firefly stock cfg colors (reference)",
        "firefly_stock_caption": "The 9 ATMOFX_BODY Color slots in Firefly's shipped Default + Stock configs (M1rageDev/Firefly, GPL-3.0), R G B (×HDR intensity). Slots group by region: shockwave = bow shock (hottest), wrap_* = plasma envelope, trail_* = wake (inner→outer cooling), glow* = hull surface heating (material, not gas). Note the pattern: warm glow/hull + a cool blue/green shockwave & wrap — i.e. a temperature ladder. *_streak = secondary-species accents.",
        "h_aurora": "Aurora color vs altitude/density (non-LTE)",
        "h_aurora_emitters": "Aurora / airglow emitter catalog",
        "aurora_emitters_caption": "Every non-LTE emitter in the model — forbidden lines, allowed bands, the meteoric-metal layer, plus UV / near-IR lines (catalog only, outside the visible grid) kept for a future spectral visualization. Swatch = the emitter's own CIE color (visible only); FUV/UV/NIR show a band badge. The 'survival' column + swatch dimming track the density slider — forbidden metastables (O¹D/O¹S) quench at high density while allowed lines stay 100%.",
        "th_ae_color": "Color", "th_ae_emitter": "Emitter", "th_ae_source": "Source",
        "th_ae_lines": "Lines (nm)", "th_ae_band": "Band", "th_ae_type": "Type",
        "th_ae_survival": "Survival @ density",
        "ae_forbidden": "forbidden/metastable", "ae_allowed": "allowed",
        "density_label": "Density (≈ altitude):",
        "aurora_caption": "Drag the density slider to scrub altitude. Aurora is NON-LTE — color is set by quenching of metastable forbidden lines, NOT temperature, so the axis is density (≈ altitude). Earth shows the real stratification: red (O ¹D 630nm, high altitude where the 114s metastable survives) → green (O ¹S 557.7nm, mid) → pink (N₂ 1st-positive bands, dense low altitude), warming at the densest rows toward the ~80-105km airglow / meteoric-metal layer (Na 589nm yellow + OH Meinel red + traces of Li/K/Ca⁺). CO₂ atmospheres quench red hard (CO₂ is a strong quencher); gas giants glow H-Balmer pink. Other emitters in the catalog: O I 777nm (bright-aurora deep red). Computed from measured A-values + quenching coefficients; cell label = dominant emitter (by production). This is the non-LTE counterpart to the (LTE) reentry tables; aurora feeds aurora/EVE, not Firefly.",
        "element_temp_caption": "Per-element analog of the table above. Each row is a pure element's LTE plasma color at each temperature: an incandescence stand-in (top strip = blackbody, exact) + neutral AND first-ion (X II) atomic line emission (NIST A-values, Boltzmann), weighted by the Saha neutral/ion fractions. Low T thermal glow → mid T the element's neutral lines (Cu green, Ca violet, Na yellow) → high T ionizes and ion lines take over (e.g. Ba II violet). ATOMIC only (no molecular bands); no free-free/bound continuum; 2nd ionization neglected. 75 elements with NIST A-values; complex spectra without A (Zr, lanthanides, actinides) omitted — same coverage as the periodic table above. Hover for ionization fraction.",
        "plasma_temp_caption": "Top strip = blackbody thermal color (Planck→CIE, exact). Grid = first-principles LTE isothermal-slab color per composition — thermal continuum + atomic lines (NIST A-values) + molecular bands, with ionization (Saha), excitation (Boltzmann) and dissociation all computed. No tuned weight. LTE caveat — high-lying bands (N2 1P/2P, 7–11 eV) are thermally faint, so air's observed reentry blue-violet (a non-LTE electron-impact effect) does not appear, while C2 Swan green and H Balmer pink do. Hover for the dominant regime + ionization/molecular/emission fractions.",
        "bt_blackbody": "Blackbody (thermal)",
        "ptc_air": "N2/O2 (Earth-like)",
        "ptc_co2": "CO2 (Mars/Venus)",
        "ptc_h2_he": "H2/He (gas giant)",
        "ptc_ch4": "CH4 (Titan-class)",
        "ptc_h2o": "H2O (steam)",
        "ptc_nh3": "NH3 (ice-giant)",
        "h_bodies": "Currently emitted bodies (engine-derived)",
        "temp_label": "Temperature:",
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
        "legend_visible":    "visible",
        "legend_no_data":    "no data / dim / dissociated",
    }
    t_ko = {
        "title": "플라즈마 & 재진입 색 레퍼런스",
        "intro_1": "1차원리 LTE 플라스마 발광색 (Saha–Boltzmann → CIE). 주기율표와 분자 패널은 온도 슬라이더로 구동됩니다 — <code>db/refs/element_temperature_colors.yaml</code> + <code>db/refs/molecular_temperature_colors.yaml</code>. 아래 섹션은 조성 그리드, Firefly emitter 팔레트, 오로라입니다.",
        "intro_2": "온도 슬라이더를 움직이면 각 원소·분자가 그 온도의 LTE 플라스마 발광색으로 칠해집니다. 분자 → 원자 → 이온 행진을 볼 수 있습니다. 셀에 올리면 상세가 보이고, 흐린 셀은 그 온도의 계산 색이 없는 것입니다.",
        "h_periodic": "주기율표 — 원자 emission",
        "h_molecular": "분자 emitter",
        "h_bulk": "Bulk-gas 폴백 팔레트 (손튜닝, 비계산)",
        "h_streak": "2차 종 streak 팔레트 (큐레이트)",
        "h_plasma_temp": "온도별 플라스마 색 (1000K 간격)",
        "h_element_temp": "원소별 재진입 플라스마 색 — 온도별 (1000K 간격)",
        "h_firefly_stock": "Firefly 기본 cfg 색상 (레퍼런스)",
        "firefly_stock_caption": "Firefly 기본(Default) + 스톡 cfg(M1rageDev/Firefly, GPL-3.0)의 ATMOFX_BODY 9개 Color 슬롯, R G B (×HDR 강도). 슬롯은 부위별로 묶입니다. shockwave = 활충격(최고온), wrap_* = 플라스마 envelope, trail_* = 후류(안→밖 냉각), glow* = 동체 표면 가열(가스 아닌 재료). 패턴을 보세요 — 따뜻한 glow/동체 + 차가운 청록 shockwave·wrap, 즉 온도 사다리. *_streak = 2차 종 악센트.",
        "h_aurora": "고도/밀도별 오로라 색 (비-LTE)",
        "h_aurora_emitters": "오로라 / airglow 발광종 카탈로그",
        "aurora_emitters_caption": "모델의 모든 비-LTE 발광종 — 금지선, 허용 밴드, 유성기원 금속층, 그리고 UV / 근적외 라인(카탈로그 전용, 가시 그리드 밖)까지. 나중 스펙트럼 시각화용으로 보존합니다. 스와치 = 발광종 자체의 CIE 색(가시영역만), FUV/UV/NIR은 대역 배지. '밀도별 생존율' 컬럼과 스와치 디밍은 밀도 슬라이더에 연동됩니다 — 금지 준안정선(O¹D/O¹S)은 고밀도에서 quench되고 허용선은 100% 유지합니다.",
        "th_ae_color": "색", "th_ae_emitter": "발광종", "th_ae_source": "소스",
        "th_ae_lines": "라인 (nm)", "th_ae_band": "대역", "th_ae_type": "종류",
        "th_ae_survival": "밀도별 생존율",
        "ae_forbidden": "금지/준안정", "ae_allowed": "허용",
        "density_label": "밀도 (≈ 고도):",
        "aurora_caption": "밀도 슬라이더를 움직여 고도를 훑어보세요. 오로라는 비-LTE — 색은 온도가 아니라 준안정 금지선의 quenching이 정하므로 축은 밀도(≈고도)입니다. 지구는 실제 층리를 재현합니다. 적색(O ¹D 630nm, 114초 준안정이 살아남는 고고도) → 녹색(O ¹S 557.7nm, 중간) → 분홍(N₂ 1차 양성대, 조밀한 저고도), 가장 조밀한 행에선 ~80-105km airglow/유성기원 금속층(Na 589nm 노랑 + OH Meinel 적색 + Li/K/Ca⁺ 미량)으로 따뜻해집니다. CO₂ 대기는 적색을 강하게 quench(CO₂가 강한 소광체), 가스자이언트는 H-Balmer 핑크. 카탈로그의 다른 발광종: O I 777nm(밝은 오로라 심적색). 측정 A계수 + quenching 계수로 계산, 셀 라벨 = 우세 발광종(생산량 기준). LTE 재진입 표의 비-LTE 짝이며, 오로라는 Firefly가 아니라 aurora/EVE로 갑니다.",
        "element_temp_caption": "위 표의 원소별 버전입니다. 각 행은 순수 원소의 LTE 플라스마 색을 온도별로 보여줍니다. 백열 대용 항(위 띠 = 흑체, 정확) + 중성 및 1차이온(X II) 원자선 발광(NIST A계수, Boltzmann)을 Saha 중성/이온 분율로 가중합니다. 저온 열복사 글로우 → 중온 중성 고유선(Cu 초록, Ca 보라, Na 노랑) → 고온 이온화되며 이온선이 우세(예: Ba II 보라). 원자 전용(분자 밴드 없음), 자유-자유/속박 연속 없음, 2차 이온화 무시. NIST A계수 있는 75개 원소, A 없는 복잡 스펙트럼(Zr·란타넘·악티늄)은 제외 — 위 주기율표와 같은 커버리지입니다. 셀에 올리면 이온화 분율이 보입니다.",
        "plasma_temp_caption": "위 띠 = 흑체 열복사 색(Planck→CIE, 정확). 그리드 = 조성별 1차원리 LTE 등온 슬랩 색입니다. 열복사 연속 + 원자선(NIST A계수) + 분자 밴드를 합치고, 이온화(Saha)·들뜸(Boltzmann)·해리를 모두 계산합니다. 손맛 가중치는 없습니다. LTE 한계 — 상위준위가 높은 밴드(N₂ 1P/2P, 7~11 eV)는 열적으로 거의 안 채워져서 공기의 관측된 재진입 청보라(비-LTE 전자충돌 효과)는 여기 안 나오고, C₂ Swan 초록과 H Balmer 핑크는 나옵니다. 셀에 마우스를 올리면 우세 영역과 이온화·분자·방출 분율이 보입니다.",
        "bt_blackbody": "흑체 (열복사)",
        "ptc_air": "N2/O2 (지구형)",
        "ptc_co2": "CO2 (화성/금성)",
        "ptc_h2_he": "H2/He (가스자이언트)",
        "ptc_ch4": "CH4 (타이탄형)",
        "ptc_h2o": "H2O (수증기)",
        "ptc_nh3": "NH3 (아이스자이언트)",
        "h_bodies": "현재 emit된 행성들 (엔진 산출)",
        "temp_label": "온도:",
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
        "legend_visible":    "관측 가능",
        "legend_no_data":    "자료 없음 / 너무 어두움 / 해리됨",
    }
    for name in palettes:
        desc_en, desc_ko = PALETTE_DESCRIPTORS[name]
        t_en[f"palette_{name}_rule"] = f"Trigger: {desc_en}"
        t_ko[f"palette_{name}_rule"] = f"적용 조건: {desc_ko}"
    for sp in STREAK_PALETTE:
        t_en[f"streak_{sp}_use"] = STREAK_USECASE_EN.get(sp, "")
        t_ko[f"streak_{sp}_use"] = STREAK_USECASE_KO.get(sp, "")
    return t_en, t_ko


TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title data-i18n="title"></title>
<link rel="stylesheet" href="style.css">
<style>
/* The shared style.css sets `html, body {{ overflow-x: hidden }}`, which makes
   body a scroll container and breaks position:sticky on the temperature bar.
   `overflow-x: clip` clips horizontally WITHOUT creating a scroll container,
   so the sticky bar pins to the viewport again. Scoped to this page. */
html, body {{ overflow-x: clip; }}
.regime-bar {{
  display: flex; align-items: center; gap: 0.75rem;
  margin: 1rem 0; padding: 0.5rem 0.75rem;
  background: var(--bg-card); border: 1px solid var(--bd-mid);
  border-radius: 4px;
  position: sticky; top: 0; z-index: 20;
  box-shadow: 0 2px 10px rgba(0,0,0,0.45);
}}
.regime-bar .label {{ color: var(--fg-muted); font-size: 0.9rem }}
#temp-slider {{ flex: 1; max-width: 460px; cursor: pointer; accent-color: var(--accent); }}
.temp-readout {{ font-family: var(--mono); font-size: 0.95rem; color: var(--fg-emph);
  min-width: 5.5em; text-align: right; }}
#aurora-bar {{ position: static; box-shadow: none; }}   /* local, not sticky */
#density-slider {{ flex: 1; max-width: 460px; cursor: pointer; accent-color: var(--accent); }}
.aurora-panel {{ display: flex; gap: 0.6rem; flex-wrap: wrap; margin: 0.5rem 0 1rem; }}
.aurora-cell {{ flex: 1 1 200px; min-height: 64px; border-radius: 6px; padding: 0.55rem 0.8rem;
  display: flex; flex-direction: column; justify-content: center; gap: 2px;
  border: 1px solid var(--bd-mid); transition: background 0.15s ease, color 0.15s ease; }}
.aurora-cell .aurora-atm {{ font-size: 0.9rem; font-weight: 600 }}
.aurora-cell .aurora-dom {{ font-family: var(--mono); font-size: 0.8rem; opacity: 0.95 }}
.aurora-cell .aurora-hex {{ font-family: var(--mono); font-size: 0.72rem; opacity: 0.7 }}

.periodic-table {{
  display: grid;
  grid-template-columns: repeat(18, 1fr);
  grid-template-rows: repeat(9, auto);
  gap: 3px; margin: 1rem 0;
}}
.el-cell {{
  position: relative;
  aspect-ratio: 1;
  padding: 4px 4px 2px 4px;
  border-radius: 3px;
  font-size: 9px; line-height: 1.1;
  overflow: hidden;
  cursor: help;
  border: 1px solid rgba(0,0,0,0.3);
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  transition: background 0.4s ease, color 0.4s ease;
  background-image: repeating-linear-gradient(45deg, #1a1828 0 4px, #2a1a38 4px 8px);
  color: #6a7898;
}}
.el-cell.visible {{ background-image: none; border-color: rgba(0,0,0,0.5) }}
.el-cell .z {{ position: absolute; top: 2px; left: 4px; font-size: 9px; opacity: 0.85 }}
.el-cell .sym {{ font-size: 16px; font-weight: bold }}
.el-cell .name {{ font-size: 7px; opacity: 0.75; text-align: center }}
.el-cell .chip {{ position: absolute; bottom: 1px; right: 2px; font-size: 6px; opacity: 0.7 }}
@media (max-width: 1100px) {{
  .el-cell .sym {{ font-size: 12px }}
  .el-cell .name {{ display: none }}
}}

.molecular-panel {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 6px; margin: 1rem 0;
}}
.mol-cell {{
  background-image: repeating-linear-gradient(45deg, #1a1828 0 4px, #2a1a38 4px 8px);
  color: #6a7898;
  border-radius: 3px; padding: 8px 6px;
  font-size: 11px; text-align: center;
  border: 1px solid rgba(0,0,0,0.3);
  cursor: help;
  transition: background 0.4s ease, color 0.4s ease;
}}
.mol-cell.visible {{ background-image: none; border-color: rgba(0,0,0,0.5) }}
.mol-cell.research-pending {{
  background-image: repeating-linear-gradient(45deg, #1f1f10 0 4px, #2c2c14 4px 8px);
  border-color: #4a4818;
  color: #c8b870;
}}
.mol-cell .mol-formula {{ display: block; font-weight: bold; font-size: 14px }}
.mol-cell .mol-atoms {{ display: block; font-size: 8px; opacity: 0.75; margin-top: 2px }}
.mol-cell .mol-status {{ display: block; font-size: 7px; margin-top: 2px; opacity: 0.7 }}
.mol-cell[data-kind="polyatomic"] {{ border-style: dashed }}

.palette-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 1rem; margin: 1rem 0;
}}
.palette-card {{
  background: var(--bg-card); border: 1px solid var(--bd-mid);
  border-radius: 4px; padding: 1rem;
}}
.palette-card h3 {{ margin: 0 0 0.25rem 0; font-size: 1rem; color: var(--fg-emph); font-family: var(--mono) }}
.palette-card .palette-rule {{ font-size: 0.85rem; color: var(--fg-muted); margin: 0 0 0.75rem 0 }}
.palette-swatches {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3px;
}}
.palette-swatch {{
  padding: 6px 4px;
  border-radius: 3px;
  display: flex; flex-direction: column; align-items: center;
  font-size: 9px; line-height: 1.2;
  border: 1px solid rgba(0,0,0,0.3);
}}
.palette-swatch .role {{ font-weight: 600; font-size: 10px }}
.palette-swatch .hex {{ font-family: var(--mono); font-size: 9px; opacity: 0.85 }}
.palette-swatch .rgbi {{ font-family: var(--mono); font-size: 8px; opacity: 0.7 }}

.streak-table {{ width: 100%; border-collapse: collapse; margin: 1rem 0 }}
.streak-table th, .streak-table td {{
  padding: 6px 8px; border-bottom: 1px solid var(--bd-soft);
  text-align: left; font-size: 13px;
}}
.streak-table td.sp {{ font-family: var(--mono); font-weight: 600 }}
.streak-table td.rgbi {{ font-family: var(--mono); font-size: 12px; color: var(--fg-muted) }}
.swatch-inline {{ display: inline-block; padding: 2px 8px; border-radius: 3px; font-family: var(--mono); font-size: 12px }}

.body-card {{
  background: var(--bg-card); border: 1px solid var(--bd-mid);
  border-radius: 4px; padding: 1rem; margin-bottom: 1rem;
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
  display: flex; align-items: center;
  padding: 0.75rem 1.5rem;
  background: var(--bg-header);
  border-bottom: 1px solid var(--bd-soft);
}}
header h1 {{ font-size: 1.1rem; color: var(--fg-emph); margin: 0 1rem 0 0 }}
.seg {{ display: inline-flex; border: 1px solid var(--bd-input); border-radius: 4px; overflow: hidden }}
.seg button {{
  background: var(--bg-input); color: var(--fg-muted);
  border: none; padding: 4px 12px;
  cursor: pointer; font-family: var(--sans); font-size: 12px;
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

<div class="regime-bar">
  <span class="label" data-i18n="temp_label"></span>
  <input type="range" id="temp-slider" min="1000" max="15000" step="1000" value="4000">
  <span id="temp-readout" class="temp-readout">4000 K</span>
</div>

<section>
<h2 data-i18n="h_periodic"></h2>
{periodic_table}
</section>

<section>
<h2 data-i18n="h_molecular"></h2>
{molecular_panel}
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
<h2 data-i18n="h_plasma_temp"></h2>
{plasma_temp_grid}

<h2 data-i18n="h_element_temp"></h2>
{element_temp_grid}

<h2 data-i18n="h_firefly_stock"></h2>
{firefly_stock_grid}

<h2 data-i18n="h_aurora"></h2>
{aurora_grid}

<h2 data-i18n="h_aurora_emitters"></h2>
{aurora_emitters}
</section>

<section>
<h2 data-i18n="h_bodies"></h2>
{bodies_section}
</section>

</main>

<script>
const T = {t_json};
const ELEMENT_TEMP = {element_temp_json};
const MOLECULE_TEMP = {molecule_temp_json};
const AURORA = {aurora_json};

let lang = localStorage.getItem('nearstars-lang') || 'ko';
let temp = parseInt(localStorage.getItem('nearstars-temp') || '4000', 10);
let density = parseInt(localStorage.getItem('nearstars-density') || '11', 10);

function luminance(hex) {{
  const r = parseInt(hex.substr(1,2),16)/255;
  const g = parseInt(hex.substr(3,2),16)/255;
  const b = parseInt(hex.substr(5,2),16)/255;
  const chan = c => c <= 0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4);
  return 0.2126*chan(r) + 0.7152*chan(g) + 0.0722*chan(b);
}}
function textOn(hex) {{ return luminance(hex) > 0.4 ? '#000' : '#fff'; }}

function applyTemp(t) {{
  const key = String(t);
  document.querySelectorAll('.el-cell').forEach(cell => {{
    const sym = cell.dataset.sym;
    const data = ELEMENT_TEMP[sym];
    cell.classList.remove('visible');
    cell.style.background = '';
    cell.style.color = '';
    const chip = cell.querySelector('.chip');
    chip.textContent = '';
    const c = data && data.colors ? data.colors[key] : null;
    if (c) {{
      cell.classList.add('visible');
      cell.style.background = c.hex;
      cell.style.color = textOn(c.hex);
      cell.title = `${{data.name}} (${{sym}}, Z=${{data.z}}) @ ${{t}}K — ionz ${{Math.round((c.ion||0)*100)}}%`;
    }} else {{
      chip.textContent = 'no data';
      cell.title = data ? `${{data.name}} (${{sym}}, Z=${{data.z}}) — no computed temperature color`
                        : `${{sym}} — no data`;
    }}
  }});

  document.querySelectorAll('.mol-cell').forEach(cell => {{
    const formula = cell.dataset.formula;
    const mol = MOLECULE_TEMP[formula];
    const status = cell.querySelector('.mol-status');
    cell.classList.remove('visible', 'research-pending');
    cell.style.background = '';
    cell.style.color = '';
    const c = mol && mol.colors ? mol.colors[key] : null;
    if (c) {{
      cell.classList.add('visible');
      cell.style.background = c.hex;
      cell.style.color = textOn(c.hex);
      status.textContent = c.dom || '';
      const drop = (mol.dropped && mol.dropped.length) ? ` · no data for ${{mol.dropped.join('/')}}` : '';
      cell.title = `${{formula}} (${{mol.atoms}}-atom) @ ${{t}}K — ${{c.dom}}${{drop}}`;
    }} else {{
      status.textContent = 'no data';
      cell.title = `${{formula}} — ${{mol && mol.note ? mol.note : 'no computed temperature color'}}`;
    }}
  }});

  document.getElementById('temp-readout').textContent = t + ' K';
}}

function applyDensity(n) {{
  const key = String(n);
  document.querySelectorAll('.aurora-cell').forEach(cell => {{
    const c = AURORA[cell.dataset.atm].colors[key];
    if (!c) return;
    cell.style.background = c.hex;
    cell.style.color = textOn(c.hex);
    cell.querySelector('.aurora-dom').textContent = c.dom.replace(/_/g, ' ');
    cell.querySelector('.aurora-hex').textContent = c.hex;
  }});
  const alt = AURORA.earth.colors[key].alt;
  document.getElementById('density-readout').textContent = '1e' + n + ' cm⁻³ · ' + alt;
  // catalog: fade forbidden metastables by their survival φ(n) = A/(A + Σk·n)
  const nlin = Math.pow(10, n);
  document.querySelectorAll('#aurora-emitters tbody tr').forEach(tr => {{
    const forb = tr.dataset.forbidden === '1';
    const atot = parseFloat(tr.dataset.atot);
    const ksum = parseFloat(tr.dataset.ksum);
    const surv = tr.querySelector('.ae-surv');
    const sw = tr.querySelector('.swatch-inline');
    if (forb && atot && ksum) {{
      const phi = atot / (atot + ksum * nlin);
      surv.textContent = phi >= 0.01 ? Math.round(phi * 100) + '%' : (phi * 100).toFixed(1) + '%';
      if (sw) sw.style.opacity = Math.max(0.12, phi).toFixed(2);
    }} else if (forb) {{
      surv.textContent = '—';
      if (sw) sw.style.opacity = 1;
    }} else {{
      surv.textContent = '100%';
      if (sw) sw.style.opacity = 1;
    }}
  }});
}}

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

const tempSlider = document.getElementById('temp-slider');
tempSlider.value = temp;
tempSlider.addEventListener('input', e => {{
  temp = parseInt(e.target.value, 10);
  localStorage.setItem('nearstars-temp', temp);
  applyTemp(temp);
}});

const densitySlider = document.getElementById('density-slider');
densitySlider.value = density;
densitySlider.addEventListener('input', e => {{
  density = parseInt(e.target.value, 10);
  localStorage.setItem('nearstars-density', density);
  applyDensity(density);
}});

applyLang();
applyTemp(temp);
applyDensity(density);
</script>
</body>
</html>
"""


def main() -> int:
    with open(ELEMENT_DB, encoding="utf-8") as f:
        db = yaml.safe_load(f)
    with open(MOLECULAR_DB, encoding="utf-8") as f:
        mdb = yaml.safe_load(f)
    layout = build_layout()
    periodic = render_periodic_table(db, layout)
    molecular = render_molecular_panel(mdb)
    palettes_section = render_palettes_section()
    streak_table = render_streak_table()
    plasma_temp_grid = render_plasma_temp_grid()
    element_temp_grid = render_element_temp_grid()
    firefly_stock_grid = render_firefly_stock()
    aurora_grid = render_aurora_grid()
    aurora_emitters = render_aurora_emitters()

    body_results = []
    for slug in sorted(p.stem for p in PHASE3_DIR.glob("*.md")):
        res = derive_body_palette(slug, db)
        if res:
            body_results.append(res)
    bodies_section = "\n".join(render_body_card(b) for b in body_results)

    etc = yaml.safe_load(ELEMENT_TEMP_DB.read_text(encoding="utf-8"))
    mtc = yaml.safe_load(MOL_TEMP_DB.read_text(encoding="utf-8"))
    element_temp_data = build_element_temp_data(etc)
    molecule_temp_data = build_molecule_temp_data(mtc)
    t_en, t_ko = build_t(PALETTES)
    t_json = json.dumps({"en": t_en, "ko": t_ko}, ensure_ascii=False)
    element_temp_json = json.dumps(element_temp_data, ensure_ascii=False)
    molecule_temp_json = json.dumps(molecule_temp_data, ensure_ascii=False)
    aurora_raw = (yaml.safe_load(AURORA_COLORS_DB.read_text(encoding="utf-8"))
                  if AURORA_COLORS_DB.exists() else {})
    aurora_data = {k: {"colors": {str(ln): {"hex": c["hex"], "dom": c["dominant"],
                                            "alt": c["altitude_hint"]}
                                  for ln, c in v["colors"].items()}}
                   for k, v in aurora_raw.items()}
    aurora_json = json.dumps(aurora_data, ensure_ascii=False)

    html_out = TEMPLATE.format(
        periodic_table=periodic,
        molecular_panel=molecular,
        palettes_section=palettes_section,
        streak_table=streak_table,
        plasma_temp_grid=plasma_temp_grid,
        element_temp_grid=element_temp_grid,
        firefly_stock_grid=firefly_stock_grid,
        aurora_grid=aurora_grid,
        aurora_emitters=aurora_emitters,
        bodies_section=bodies_section,
        t_json=t_json,
        element_temp_json=element_temp_json,
        molecule_temp_json=molecule_temp_json,
        aurora_json=aurora_json,
    )
    OUT.write_text(html_out, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} "
          f"({len(db)} elements, {len(mdb)} molecules, "
          f"{len(PALETTES)} bulk-gas palettes, {len(STREAK_PALETTE)} streak, "
          f"{len(body_results)} emitted bodies)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
