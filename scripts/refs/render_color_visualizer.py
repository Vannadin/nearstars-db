# db/refs/element_plasma_colors.yaml + molecular_plasma_colors.yaml + emitter PALETTES 를 단일 HTML 시각화로 렌더 (regime toggle)
"""Render docs/firefly-colors.html — multi-regime visualization.

Sections:
  1. Regime toggle: atomic_flame | reentry_plasma | aurora
  2. Periodic table — 118 cells colored per active regime
  3. Molecular panel — diatomic + polyatomic species per active regime
  4. Bulk-gas reentry palettes from emit_firefly_cfg.py PALETTES (always shown)
  5. Currently-emitted bodies (always shown)

All regime data is embedded as JSON; JavaScript swaps cell colors when
the user toggles regime. No server round-trip.

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
sys.path.insert(0, str(ROOT / ".claude/skills/firefly-cfg/scripts"))
from emit_firefly_cfg import (  # noqa: E402
    PALETTES, STREAK_PALETTE, DEFAULTS_HEX_RGB,
    parse_present, parse_pressure_pa, parse_composition,
    extract_decisions, pick_palette, pressure_to_strength,
    PRESSURE_THRESHOLD_PA, slug_to_kopernicus_name, planet_letter_uppercase,
)

ELEMENT_DB = ROOT / "db" / "refs" / "element_plasma_colors.yaml"
MOLECULAR_DB = ROOT / "db" / "refs" / "molecular_plasma_colors.yaml"
PLASMA_TEMP_DB = ROOT / "db" / "refs" / "plasma_temperature_colors.yaml"
LTE_PLASMA_DB = ROOT / "db" / "refs" / "lte_plasma_colors.yaml"
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


# ── Build element data for JS ──────────────────────────────────────

def build_element_data(db: dict, lte: dict | None = None) -> dict:
    """Per-element regime data, suitable for JSON embedding. `lte` is the
    computed lte_plasma_colors.yaml, merged in as the `lte_plasma` regime."""
    lte = lte or {}
    data = {}
    for sym, e in db.items():
        entry = {
            "z": e["atomic_number"],
            "name": e["name"],
            "regimes": {},
        }
        for regime_name in ("atomic_flame", "reentry_plasma", "aurora", "phosphor_emission"):
            r = e["regimes"].get(regime_name)
            if r is None:
                entry["regimes"][regime_name] = None
                continue
            entry["regimes"][regime_name] = {
                "status": r["status"],
                "hex": r.get("hex"),
                "hex_basis": r.get("hex_basis"),
                "basis": r.get("basis", ""),
                "source": r.get("source", ""),
            }
        lr = lte.get(sym)
        entry["regimes"]["lte_plasma"] = None if lr is None else {
            "status": lr["status"],
            "hex": lr.get("hex"),
            "hex_basis": "computed",
            "basis": lr.get("basis", ""),
            "source": "computed from NIST ASD neutral lines"
                      + (f" — {lr['confidence']} confidence" if lr.get("confidence") else ""),
        }
        data[sym] = entry
    return data


# ── Build molecular data for JS ────────────────────────────────────

def build_molecular_data(mdb: dict) -> dict:
    data = {}
    for formula, m in mdb.items():
        entry = {
            "formula": m["formula"],
            "atoms": m["atoms"],
            "mass_amu": m["mass_amu"],
            "regimes": {},
        }
        for regime_name in ("reentry_plasma", "aurora"):
            r = m["regimes"].get(regime_name)
            if r is None:
                entry["regimes"][regime_name] = None
                continue
            entry["regimes"][regime_name] = {
                "status": r["status"],
                "hex": r.get("hex"),
                "hex_basis": r.get("hex_basis"),
                "basis": r.get("basis", ""),
                "source": r.get("source", ""),
                "dissociation_products": r.get("dissociation_products"),
                "upgrade_when": r.get("upgrade_when"),
            }
        data[formula] = entry
    return data


# ── Periodic table (cells without colors; JS fills per regime) ────

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


# ── Reentry scene SVG (per-palette mini diorama) ──────────────────

def _hex_op(rgb_i, max_intensity=3.0):
    """(R, G, B, intensity) → ('#rrggbb', opacity 0..1)."""
    r, g, b, i = rgb_i
    hex_val = f"#{int(r):02x}{int(g):02x}{int(b):02x}"
    opacity = min(1.0, i / max_intensity)
    return hex_val, opacity


def render_reentry_scene_svg(palette_name: str, palette: dict, scene_id: str) -> str:
    """Refined side-view diorama showing how a palette's 9 ATMOFX_BODY
    colors compose in real reentry rendering.

    Composition (back to front):
      atmospheric backdrop with star field → outer shock ring → trail
      (multi-stop gradient) → streak particles (animated drift) →
      wrap layer envelope → hull glow (radial) → main bow shock arc →
      Apollo-style capsule with heatshield.
    """
    glow_h,    glow_o    = _hex_op(DEFAULTS_HEX_RGB["glow"])
    ghot_h,    ghot_o    = _hex_op(DEFAULTS_HEX_RGB["glow_hot"])
    tp_h,      tp_o      = _hex_op(palette["trail_primary"])
    ts_h,      ts_o      = _hex_op(palette["trail_secondary"])
    tt_h,      tt_o      = _hex_op(palette["trail_tertiary"])
    wl_h,      wl_o      = _hex_op(palette["wrap_layer"])
    sw_h,      sw_o      = _hex_op(palette["shockwave"])
    streak_h            = tp_h   # default streak follows trail_primary

    # Per-scene staggered animation delays so motion isn't synchronized across cards.
    seed = sum(ord(c) for c in scene_id) % 7

    return f'''<svg class="reentry-scene" viewBox="0 0 320 160" preserveAspectRatio="xMidYMid meet">
  <defs>
    <!-- atmospheric backdrop: deep space → faint haze near bottom -->
    <linearGradient id="atm-{scene_id}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%"  stop-color="#01030a"/>
      <stop offset="65%" stop-color="#02060f"/>
      <stop offset="100%" stop-color="#0a0e1a"/>
    </linearGradient>

    <!-- main trail: hot core → primary → secondary → tertiary → fade -->
    <radialGradient id="trail-{scene_id}" cx="78%" cy="50%" r="78%">
      <stop offset="0%"   stop-color="{ghot_h}" stop-opacity="{ghot_o:.3f}"/>
      <stop offset="8%"   stop-color="{tp_h}"   stop-opacity="{tp_o:.3f}"/>
      <stop offset="30%"  stop-color="{tp_h}"   stop-opacity="{tp_o*0.85:.3f}"/>
      <stop offset="55%"  stop-color="{ts_h}"   stop-opacity="{ts_o*0.6:.3f}"/>
      <stop offset="80%"  stop-color="{tt_h}"   stop-opacity="{tt_o*0.25:.3f}"/>
      <stop offset="100%" stop-color="{tt_h}"   stop-opacity="0"/>
    </radialGradient>

    <!-- hull glow: hot core → cooler rim -->
    <radialGradient id="glow-{scene_id}" cx="50%" cy="50%" r="50%">
      <stop offset="0%"  stop-color="{ghot_h}" stop-opacity="{ghot_o:.3f}"/>
      <stop offset="45%" stop-color="{glow_h}" stop-opacity="{glow_o*0.85:.3f}"/>
      <stop offset="100%" stop-color="{glow_h}" stop-opacity="0"/>
    </radialGradient>

    <!-- wrap layer: soft envelope falloff -->
    <radialGradient id="wrap-{scene_id}" cx="50%" cy="50%" r="50%">
      <stop offset="40%"  stop-color="{wl_h}" stop-opacity="{wl_o*0.55:.3f}"/>
      <stop offset="100%" stop-color="{wl_h}" stop-opacity="0"/>
    </radialGradient>

    <!-- bloom filter — soft glow on emissive layers -->
    <filter id="bloom-{scene_id}" x="-25%" y="-25%" width="150%" height="150%">
      <feGaussianBlur stdDeviation="1.6" result="b1"/>
      <feGaussianBlur stdDeviation="3" in="SourceGraphic" result="b2"/>
      <feMerge>
        <feMergeNode in="b2"/>
        <feMergeNode in="b1"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- soft blur for trail body -->
    <filter id="soft-{scene_id}">
      <feGaussianBlur stdDeviation="1.2"/>
    </filter>

    <!-- subtle star field pattern -->
    <pattern id="stars-{scene_id}" x="0" y="0" width="160" height="160"
             patternUnits="userSpaceOnUse">
      <circle cx="22"  cy="34"  r="0.5" fill="#fff" opacity="0.35"/>
      <circle cx="78"  cy="18"  r="0.4" fill="#fff" opacity="0.28"/>
      <circle cx="45"  cy="92"  r="0.6" fill="#fff" opacity="0.4"/>
      <circle cx="118" cy="55"  r="0.4" fill="#fff" opacity="0.3"/>
      <circle cx="135" cy="118" r="0.5" fill="#fff" opacity="0.34"/>
      <circle cx="90"  cy="135" r="0.3" fill="#fff" opacity="0.22"/>
      <circle cx="12"  cy="115" r="0.4" fill="#fff" opacity="0.28"/>
      <circle cx="62"  cy="58"  r="0.3" fill="#fff" opacity="0.25"/>
    </pattern>
  </defs>

  <!-- backdrop -->
  <rect width="320" height="160" fill="url(#atm-{scene_id})"/>
  <rect width="320" height="160" fill="url(#stars-{scene_id})"/>

  <!-- outer shock ripple (faint, atmospheric distortion) -->
  <ellipse cx="252" cy="80" rx="55" ry="40" fill="none"
           stroke="{sw_h}" stroke-width="0.5"
           opacity="{sw_o*0.18:.3f}" filter="url(#soft-{scene_id})"/>

  <!-- main plasma trail (multi-stop radial, soft blur) -->
  <path d="M 248,80 Q 200,52 60,72 Q 25,80 12,82 Q 25,80 60,88 Q 200,108 248,80 Z"
        fill="url(#trail-{scene_id})" filter="url(#soft-{scene_id})"/>

  <!-- streak particles (varied sizes; animated drift via CSS class) -->
  <g class="streaks" filter="url(#bloom-{scene_id})" style="animation-delay: {seed*0.3:.1f}s">
    <circle class="streak streak-1" cx="220" cy="74" r="2.6" fill="{streak_h}" opacity="0.95"/>
    <circle class="streak streak-2" cx="188" cy="84" r="2.2" fill="{streak_h}" opacity="0.85"/>
    <circle class="streak streak-3" cx="152" cy="76" r="1.9" fill="{streak_h}" opacity="0.7"/>
    <circle class="streak streak-4" cx="112" cy="83" r="1.6" fill="{streak_h}" opacity="0.55"/>
    <circle class="streak streak-5" cx="72"  cy="78" r="1.3" fill="{streak_h}" opacity="0.4"/>
    <circle class="streak streak-6" cx="38"  cy="80" r="1.0" fill="{streak_h}" opacity="0.25"/>
  </g>

  <!-- wrap layer envelope -->
  <ellipse cx="252" cy="80" rx="34" ry="24" fill="url(#wrap-{scene_id})"
           filter="url(#soft-{scene_id})"/>

  <!-- hull glow (bright core radial) -->
  <ellipse cx="252" cy="80" rx="22" ry="15" fill="url(#glow-{scene_id})"
           filter="url(#bloom-{scene_id})"/>

  <!-- bow shock — three layered arcs (outer soft, mid, sharp inner) -->
  <path d="M 272,52 Q 296,80 272,108" stroke="{sw_h}" stroke-width="0.7"
        fill="none" opacity="{sw_o*0.3:.3f}" stroke-linecap="round"
        filter="url(#soft-{scene_id})"/>
  <path d="M 268,56 Q 290,80 268,104" stroke="{sw_h}" stroke-width="1.6"
        fill="none" opacity="{sw_o*0.55:.3f}" stroke-linecap="round"
        filter="url(#bloom-{scene_id})"/>
  <path d="M 264,62 Q 282,80 264,98" stroke="{sw_h}" stroke-width="2.8"
        fill="none" opacity="{sw_o*0.95:.3f}" stroke-linecap="round"
        filter="url(#bloom-{scene_id})"/>

  <!-- Apollo-style capsule -->
  <g class="capsule">
    <!-- conical heatshield (right-facing, slightly darker rim) -->
    <path d="M 254,68 L 263,73 L 266,80 L 263,87 L 254,92 Z"
          fill="#3a2820" stroke="#150a06" stroke-width="0.5"/>
    <!-- capsule body (light gray) -->
    <path d="M 226,68 L 254,68 L 254,92 L 226,92 Q 222,80 226,68 Z"
          fill="#9a9a9a" stroke="#3a3a3a" stroke-width="0.6"/>
    <!-- window strip -->
    <rect x="234" y="77" width="7" height="3.2" rx="0.8" fill="#0a0a14"/>
    <!-- detail lines (panel seams) -->
    <line x1="226" y1="74" x2="252" y2="74" stroke="#5e5e5e" stroke-width="0.35"/>
    <line x1="226" y1="86" x2="252" y2="86" stroke="#5e5e5e" stroke-width="0.35"/>
  </g>
</svg>'''


def render_reentry_scenes_section() -> str:
    cards = []
    for name, palette in PALETTES.items():
        svg = render_reentry_scene_svg(name, palette, name)
        cards.append(
            f'<div class="reentry-card">'
            f'<div class="reentry-card-head">'
            f'<h4>{name}</h4>'
            f'<p class="scene-rule" data-i18n="palette_{name}_rule"></p>'
            f'</div>'
            f'{svg}'
            f'</div>'
        )
    return f'<div class="reentry-grid">{"".join(cards)}</div>'


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
        "intro_1": "Multi-regime element/molecular plasma colors. Source of truth: <code>db/refs/element_plasma_colors.yaml</code>, <code>db/refs/molecular_plasma_colors.yaml</code>, and <code>.claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py</code> constants.",
        "intro_2": "Toggle regime to see how the same element shifts color between flame test, reentry plasma, and aurora. Hover any cell for spectroscopic basis.",
        "h_periodic": "Periodic table — atomic emission",
        "h_molecular": "Molecular emitters",
        "h_scenes": "Reentry scene previews",
        "h_bulk": "Bulk-gas reentry palettes (Firefly emitter)",
        "h_streak": "Secondary-species streak palette",
        "h_plasma_temp": "Plasma color vs temperature (1000K steps)",
        "plasma_temp_caption": "Top strip = blackbody thermal color (Planck→CIE, exact). Grid = first-principles LTE isothermal-slab color per composition — thermal continuum + atomic lines (NIST A-values) + molecular bands, with ionization (Saha), excitation (Boltzmann) and dissociation all computed. No tuned weight. LTE caveat — high-lying bands (N2 1P/2P, 7–11 eV) are thermally faint, so air's observed reentry blue-violet (a non-LTE electron-impact effect) does not appear, while C2 Swan green and H Balmer pink do. Hover for the dominant regime + ionization/molecular/emission fractions.",
        "bt_blackbody": "Blackbody (thermal)",
        "ptc_air": "N2/O2 (Earth-like)",
        "ptc_co2": "CO2 (Mars/Venus)",
        "ptc_h2_he": "H2/He (gas giant)",
        "ptc_ch4": "CH4 (Titan-class)",
        "ptc_h2o": "H2O (steam)",
        "ptc_nh3": "NH3 (ice-giant)",
        "h_bodies": "Currently emitted bodies",
        "regime_label": "Regime:",
        "regime_atomic_flame": "Flame test (~2000K)",
        "regime_reentry_plasma": "Reentry plasma (~10000K)",
        "regime_aurora": "Aurora (low density)",
        "regime_phosphor_emission": "Phosphor (Ln3+ in matrix)",
        "regime_lte_plasma": "Atomic emission (computed)",
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
        "intro_1": "온도 영역별 원소/분자 플라즈마 색. 정본 데이터: <code>db/refs/element_plasma_colors.yaml</code>, <code>db/refs/molecular_plasma_colors.yaml</code>, <code>.claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py</code> 상수.",
        "intro_2": "Regime 을 전환하면 같은 원소가 불꽃 / 재진입 / 오로라 영역에서 어떻게 색이 바뀌는지 비교할 수 있습니다. 셀에 마우스를 올리면 분광학적 근거가 보입니다.",
        "h_periodic": "주기율표 — 원자 emission",
        "h_molecular": "분자 emitter",
        "h_scenes": "재진입 장면 미리보기",
        "h_bulk": "Bulk-gas 재진입 팔레트 (Firefly emitter)",
        "h_streak": "2차 종 streak 팔레트",
        "h_plasma_temp": "온도별 플라스마 색 (1000K 간격)",
        "plasma_temp_caption": "위 띠 = 흑체 열복사 색(Planck→CIE, 정확). 그리드 = 조성별 1차원리 LTE 등온 슬랩 색입니다. 열복사 연속 + 원자선(NIST A계수) + 분자 밴드를 합치고, 이온화(Saha)·들뜸(Boltzmann)·해리를 모두 계산합니다. 손맛 가중치는 없습니다. LTE 한계 — 상위준위가 높은 밴드(N₂ 1P/2P, 7~11 eV)는 열적으로 거의 안 채워져서 공기의 관측된 재진입 청보라(비-LTE 전자충돌 효과)는 여기 안 나오고, C₂ Swan 초록과 H Balmer 핑크는 나옵니다. 셀에 마우스를 올리면 우세 영역과 이온화·분자·방출 분율이 보입니다.",
        "bt_blackbody": "흑체 (열복사)",
        "ptc_air": "N2/O2 (지구형)",
        "ptc_co2": "CO2 (화성/금성)",
        "ptc_h2_he": "H2/He (가스자이언트)",
        "ptc_ch4": "CH4 (타이탄형)",
        "ptc_h2o": "H2O (수증기)",
        "ptc_nh3": "NH3 (아이스자이언트)",
        "h_bodies": "현재 emit 된 행성들",
        "regime_label": "영역:",
        "regime_atomic_flame": "불꽃 (~2000K)",
        "regime_reentry_plasma": "재진입 plasma (~10000K)",
        "regime_aurora": "오로라 (저밀도)",
        "regime_phosphor_emission": "Phosphor (Ln3+ 고체)",
        "regime_lte_plasma": "원자 방출 (계산)",
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
.regime-bar {{
  display: flex; align-items: center; gap: 0.75rem;
  margin: 1rem 0; padding: 0.5rem 0.75rem;
  background: var(--bg-card); border: 1px solid var(--bd-mid);
  border-radius: 4px;
}}
.regime-bar .label {{ color: var(--fg-muted); font-size: 0.9rem }}

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

.reentry-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 0.9rem; margin: 1rem 0;
}}
.reentry-card {{
  background: linear-gradient(180deg, #0a1018 0%, #050810 100%);
  border: 1px solid var(--bd-mid);
  border-radius: 6px;
  padding: 0;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0,0,0,0.4), 0 1px 8px rgba(0,0,0,0.2);
  transition: border-color 0.25s ease, box-shadow 0.25s ease, transform 0.25s ease;
}}
.reentry-card:hover {{
  border-color: var(--accent);
  box-shadow: 0 2px 6px rgba(0,0,0,0.5), 0 4px 16px rgba(74,136,184,0.18);
  transform: translateY(-1px);
}}
.reentry-card-head {{
  padding: 0.6rem 0.8rem 0.4rem 0.8rem;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}}
.reentry-card h4 {{
  margin: 0; font-family: var(--mono);
  font-size: 0.95rem; color: var(--fg-emph);
  letter-spacing: 0.02em;
}}
.reentry-card .scene-rule {{
  font-size: 0.74rem; color: var(--fg-muted);
  margin: 0.18rem 0 0 0;
  font-weight: 400;
}}
.reentry-scene {{
  width: 100%; height: auto; display: block;
  background: #000;
}}

/* Subtle drift animation on streak particles */
.streak {{
  transform-origin: 0 0;
  animation: streak-drift 6s ease-in-out infinite;
}}
.streak-1 {{ animation-duration: 5.5s; animation-delay: -0.4s }}
.streak-2 {{ animation-duration: 6.2s; animation-delay: -1.1s }}
.streak-3 {{ animation-duration: 5.8s; animation-delay: -2.0s }}
.streak-4 {{ animation-duration: 6.5s; animation-delay: -2.7s }}
.streak-5 {{ animation-duration: 5.3s; animation-delay: -3.4s }}
.streak-6 {{ animation-duration: 6.8s; animation-delay: -4.1s }}
@keyframes streak-drift {{
  0%, 100% {{ transform: translateX(0) translateY(0); opacity: var(--o, 0.7) }}
  50%      {{ transform: translateX(-22px) translateY(2px); opacity: 0.3 }}
}}

@media (prefers-reduced-motion: reduce) {{
  .streak {{ animation: none }}
}}

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
  <span class="label" data-i18n="regime_label"></span>
  <div class="seg" id="regime-seg">
    <button class="on" data-regime="atomic_flame" data-i18n="regime_atomic_flame"></button>
    <button data-regime="reentry_plasma" data-i18n="regime_reentry_plasma"></button>
    <button data-regime="aurora" data-i18n="regime_aurora"></button>
    <button data-regime="phosphor_emission" data-i18n="regime_phosphor_emission"></button>
    <button data-regime="lte_plasma" data-i18n="regime_lte_plasma"></button>
  </div>
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
<h2 data-i18n="h_scenes"></h2>
{reentry_scenes_section}
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
</section>

<section>
<h2 data-i18n="h_bodies"></h2>
{bodies_section}
</section>

</main>

<script>
const T = {t_json};
const ELEMENTS = {element_json};
const MOLECULES = {molecule_json};

let lang = localStorage.getItem('nearstars-lang') || 'ko';
let regime = localStorage.getItem('nearstars-regime') || 'atomic_flame';

function luminance(hex) {{
  const r = parseInt(hex.substr(1,2),16)/255;
  const g = parseInt(hex.substr(3,2),16)/255;
  const b = parseInt(hex.substr(5,2),16)/255;
  const chan = c => c <= 0.03928 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4);
  return 0.2126*chan(r) + 0.7152*chan(g) + 0.0722*chan(b);
}}
function textOn(hex) {{ return luminance(hex) > 0.4 ? '#000' : '#fff'; }}

function applyRegime() {{
  document.querySelectorAll('.el-cell').forEach(cell => {{
    const sym = cell.dataset.sym;
    const data = ELEMENTS[sym];
    const r = data.regimes[regime];
    cell.classList.remove('visible');
    cell.style.background = '';
    cell.style.color = '';
    const chip = cell.querySelector('.chip');
    chip.textContent = '';
    if (r && r.status === 'visible' && r.hex) {{
      cell.classList.add('visible');
      cell.style.background = r.hex;
      cell.style.color = textOn(r.hex);
      cell.title = `${{data.name}} (${{sym}}, Z=${{data.z}}) — ${{r.basis}}`;
    }} else {{
      const status = r ? r.status : 'no_data';
      const label = ({{
        'visible': '', 'no_flame_color': 'no flame', 'not_visible_to_humans': 'UV/IR',
        'too_radioactive': 'radioactive', 'too_short': 'synthetic',
        'no_data': 'no data', 'not_emitter': 'no emit',
        'no_measured_spectra': 'no spectra',
      }})[status] || status;
      chip.textContent = label;
      cell.title = `${{data.name}} (${{sym}}, Z=${{data.z}}) — ${{r ? r.basis : 'no data for this regime'}}`;
    }}
  }});

  document.querySelectorAll('.mol-cell').forEach(cell => {{
    const formula = cell.dataset.formula;
    const mol = MOLECULES[formula];
    if (!mol) return;
    // Molecular only has reentry_plasma + aurora regimes — other regimes n/a
    if (regime === 'atomic_flame' || regime === 'phosphor_emission') {{
      cell.classList.remove('visible', 'research-pending');
      cell.style.background = '';
      cell.style.color = '';
      const status = cell.querySelector('.mol-status');
      const label = regime === 'atomic_flame' ? 'atomic regime n/a' : 'phosphor regime n/a';
      status.textContent = label;
      cell.title = `${{formula}} — molecular emitters don't have a ${{regime}} regime`;
      return;
    }}
    const r = mol.regimes[regime];
    const status = cell.querySelector('.mol-status');
    cell.classList.remove('visible', 'research-pending');
    cell.style.background = '';
    cell.style.color = '';
    if (r && r.status === 'visible' && r.hex) {{
      cell.classList.add('visible');
      cell.style.background = r.hex;
      cell.style.color = textOn(r.hex);
      status.textContent = '';
      cell.title = `${{formula}} (${{mol.atoms}}-atom) — ${{r.basis}}`;
    }} else {{
      let lbl = '';
      let tipExtra = '';
      if (r && r.status === 'not_emitter') {{
        lbl = r.dissociation_products ? '→ ' + r.dissociation_products.join('+') : 'no emit';
      }} else if (r && r.status === 'not_visible_to_humans') {{
        lbl = 'UV/IR';
      }} else if (r && r.status === 'no_data') {{
        lbl = 'research pending';
        cell.classList.add('research-pending');
        if (r.upgrade_when) tipExtra = `\\nupgrade when: ${{r.upgrade_when}}`;
      }} else {{
        lbl = r ? r.status : 'no data';
      }}
      status.textContent = lbl;
      cell.title = `${{formula}} (${{mol.atoms}}-atom) — ${{r ? r.basis : 'no data'}}${{tipExtra}}`;
    }}
  }});

  document.querySelectorAll('#regime-seg button').forEach(b => {{
    b.classList.toggle('on', b.dataset.regime === regime);
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

document.getElementById('regime-seg').addEventListener('click', e => {{
  const btn = e.target.closest('button[data-regime]');
  if (!btn) return;
  regime = btn.dataset.regime;
  localStorage.setItem('nearstars-regime', regime);
  applyRegime();
}});

applyLang();
applyRegime();
</script>
</body>
</html>
"""


def main() -> int:
    with open(ELEMENT_DB, encoding="utf-8") as f:
        db = yaml.safe_load(f)
    with open(MOLECULAR_DB, encoding="utf-8") as f:
        mdb = yaml.safe_load(f)
    lte = yaml.safe_load(LTE_PLASMA_DB.read_text(encoding="utf-8")) if LTE_PLASMA_DB.exists() else {}

    layout = build_layout()
    periodic = render_periodic_table(db, layout)
    molecular = render_molecular_panel(mdb)
    reentry_scenes_section = render_reentry_scenes_section()
    palettes_section = render_palettes_section()
    streak_table = render_streak_table()
    plasma_temp_grid = render_plasma_temp_grid()

    body_results = []
    for slug in sorted(p.stem for p in PHASE3_DIR.glob("*.md")):
        res = derive_body_palette(slug, db)
        if res:
            body_results.append(res)
    bodies_section = "\n".join(render_body_card(b) for b in body_results)

    element_data = build_element_data(db, lte)
    molecule_data = build_molecular_data(mdb)
    t_en, t_ko = build_t(PALETTES)
    t_json = json.dumps({"en": t_en, "ko": t_ko}, ensure_ascii=False)
    element_json = json.dumps(element_data, ensure_ascii=False)
    molecule_json = json.dumps(molecule_data, ensure_ascii=False)

    html_out = TEMPLATE.format(
        periodic_table=periodic,
        molecular_panel=molecular,
        reentry_scenes_section=reentry_scenes_section,
        palettes_section=palettes_section,
        streak_table=streak_table,
        plasma_temp_grid=plasma_temp_grid,
        bodies_section=bodies_section,
        t_json=t_json,
        element_json=element_json,
        molecule_json=molecule_json,
    )
    OUT.write_text(html_out, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} "
          f"({len(db)} elements, {len(mdb)} molecules, "
          f"{len(PALETTES)} bulk-gas palettes, {len(STREAK_PALETTE)} streak, "
          f"{len(body_results)} emitted bodies)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
