# Phase 3 합성문 → Firefly ATMOFX_BODY + ATMOFX_PLANET_PACK cfg 일괄 emitter
"""Emit Firefly ATMOFX cfgs from Phase 3 syntheses + the element plasma DB.

Reads per planet:
  docs/phase3/<slug>.md         — Decisions table (atmosphere fields)

Reads project-wide:
  db/refs/element_plasma_colors.yaml  — per-element hex (for streak/trace species)

Writes:
  dist/NearStars-Configs/Patches/Firefly/<KopernicusName>.cfg  — one per atm body
  dist/NearStars-Configs/Patches/Firefly/NearStarsPlanetPack.cfg

The 5 bulk-gas color slots (shockwave / wrap_layer / trail_primary/secondary/
tertiary) are COMPUTED by the LTE Saha-Boltzmann plasma engine
(`scripts/refs/saha_boltzmann.py`) from the atmosphere composition + the
planet's entry velocity (≈ escape velocity from Phase 3 mass/radius). The 9
Firefly Color slots form a temperature ladder — shockwave = bow shock (peak T,
non-LTE for N2-family blue), wrap = envelope, trail = wake (cooling), glow =
hull (material default). The hardcoded PALETTES below are now a FALLBACK for
compositions the engine can't resolve. Element-level streak colors come from
`element_plasma_colors.yaml`. See [[composition-color]] + plasma-color-
methodology-review.md.

Usage:
    python3 .claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py
    python3 .claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py --dry-run
    python3 .claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py --slug trappist-1-e

Bodies with no atmosphere (or pressure < 100 Pa per the Mars threshold)
are skipped silently; that's the documented trigger condition.
"""
from __future__ import annotations

import argparse
import math
import re
import sys
import unicodedata
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
PHASE3_DIR = ROOT / "docs" / "phase3"
ELEMENT_DB = ROOT / "db" / "refs" / "element_plasma_colors.yaml"
OUT_DIR = ROOT / "dist" / "NearStars-Configs" / "Patches" / "Firefly"

PRESSURE_THRESHOLD_PA = 100.0

# ─────────────────────────────────────────────────────────────────────
# Bulk-gas palette — sourced from composition-color.md §3.
# Each palette specifies the 7 ATMOFX_BODY trail/wrap/shockwave fields
# (glow + glow_hot are material-driven, kept at Default).
# ─────────────────────────────────────────────────────────────────────

PALETTES = {
    "earth_like": {
        "_match": lambda dom, others: dom in {"N2", "O2"},
        "trail_primary":   (191, 99, 72, 3.0),
        "trail_secondary": (191, 70, 42, 1.5),
        "trail_tertiary":  (74, 80, 191, 2.0),
        "wrap_layer":      (69, 69, 191, 2.0),
        "shockwave":       (74, 90, 191, 3.0),
    },
    "co2": {
        "_match": lambda dom, others: dom == "CO2",
        "trail_primary":   (83, 92, 191, 3.0),
        "trail_secondary": (60, 70, 150, 1.5),
        "trail_tertiary":  (96, 191, 159, 2.0),
        "wrap_layer":      (96, 191, 159, 2.0),
        "shockwave":       (96, 191, 159, 3.0),
    },
    # ice_giant must precede gas_giant — both match H2+He, but ice_giant
    # additionally requires CH4 or NH3 trace (the ice-giant photochemistry
    # signature). Order in PALETTES is iteration order; first match wins.
    # Follows Firefly's shipped Neptune.cfg verbatim (mod-original colors).
    "ice_giant": {
        "_match": lambda dom, others: dom == "H2" and "He" in others
                                       and ("CH4" in others or "NH3" in others),
        "trail_primary":   (141, 91, 191, 2.5),
        "trail_secondary": (90, 8, 191, 3.0),
        "trail_tertiary":  (191, 138, 68, 2.0),    # amber inner streak (NH3)
        "wrap_layer":      (191, 19, 110, 2.0),    # magenta rim
        "shockwave":       (64, 41, 191, 3.0),
    },
    # Follows Firefly's shipped Jupiter.cfg verbatim (mod-original colors).
    "gas_giant": {
        "_match": lambda dom, others: dom == "H2" and "He" in others,
        "trail_primary":   (136, 98, 191, 2.5),
        "trail_secondary": (36, 7, 191, 3.5),
        "trail_tertiary":  (128, 27, 191, 2.0),
        "wrap_layer":      (143, 25, 191, 2.8),
        "shockwave":       (11, 29, 191, 3.0),
    },
    "methane": {
        "_match": lambda dom, others: dom == "CH4",
        "trail_primary":   (100, 191, 130, 3.0),
        "trail_secondary": (80, 150, 100, 1.5),
        "trail_tertiary":  (130, 100, 191, 2.0),
        "wrap_layer":      (100, 191, 130, 2.0),
        "shockwave":       (100, 191, 130, 3.0),
    },
    "steam": {
        "_match": lambda dom, others: dom == "H2O",
        "trail_primary":   (191, 130, 130, 3.0),
        "trail_secondary": (150, 100, 100, 1.5),
        "trail_tertiary":  (191, 130, 130, 2.0),
        "wrap_layer":      (191, 130, 130, 2.0),
        "shockwave":       (130, 150, 191, 3.0),
    },
    "pure_h2": {
        "_match": lambda dom, others: dom == "H2" and "He" not in others,
        "trail_primary":   (230, 80, 100, 3.0),
        "trail_secondary": (191, 60, 80, 1.5),
        "trail_tertiary":  (230, 80, 100, 2.0),
        "wrap_layer":      (230, 80, 100, 2.0),
        "shockwave":       (180, 60, 80, 3.0),
    },
}

# Default fallback (Earth-like) when no match
PALETTE_FALLBACK = "earth_like"

# Streak palette per secondary species — composition-color.md §4.
# Keys are normalized species strings (CO2, CH4, H2O, He, SO2, Na, K, etc.).
# Values: (R, G, B, intensity).
STREAK_PALETTE = {
    "CO2": (96, 191, 159, 2.0),
    "CH4": (86, 93, 191, 2.0),     # CH 431nm / CN violet 388nm — blue streak in N2-rich
                                   # atmo (Titan); carbon binds N→CN, not C2 Swan green
    "NH3": (191, 138, 68, 2.0),    # NH2 alpha-band 597-666nm red-orange (ice-giant ammonia)
    "H2O": (191, 130, 130, 2.0),
    "He":  (255, 200, 100, 2.0),    # D3 587nm yellow — brightest He line. Deliberate
                                   # correction of Firefly's scarlet He (191 21 21), which
                                   # weights only the weaker 667/706nm red lines. See
                                   # composition-color.md §5.
    "SO2": (150, 200, 180, 2.0),
    "H2S": (150, 200, 180, 2.0),
    "Na":  (255, 200, 60, 2.5),
    "K":   (180, 100, 191, 2.5),
    "Fe":  (191, 191, 100, 2.0),
    "Mg":  (100, 191, 100, 2.0),
    "CN":  (130, 80, 191, 2.0),    # tholin haze
    "O2":  (180, 180, 255, 2.0),   # uncommon as secondary but possible
    "N2":  (191, 138, 68, 2.0),    # N2 1st Positive red-orange (cooler inner/streak);
                                   # shock front keeps N2+ 391nm blue (Venus-class)
    "Ar":  (160, 107, 255, 2.0),
}

# Streak selection priority — "strongest visible emitter wins"
# (composition-color.md §4). Lower number = stronger → picked first when
# several secondaries qualify. Without this, an ordinary He (or O2) that
# merely appears first in the composition string shadows a notable NH3 / CO2
# (e.g. eps Ind A b's 11σ NH3, or TRAPPIST-1 e's CO2 worked example).
# Species not listed fall to a neutral middle rank.
STREAK_PRIORITY = {
    "Na": 0, "K": 1,            # alkali resonance lines — brightest in the visible
    "CN": 2,                    # tholin-haze violet
    "CO2": 3, "CH4": 4,         # CN / Swan band emitters
    "NH3": 5,                   # NH2 alpha-band
    "N2": 6,                    # N2 1st Positive
    "SO2": 7, "H2S": 7,         # sulfur bands
    "Fe": 8, "Mg": 8,           # rock-ablation vapor
    "H2O": 9,                   # weak Halpha
    "He": 10,                   # D3 — ordinary gas-giant secondary
    "O2": 11, "Ar": 12,         # weak / noble-gas trace
}

# Default ATMOFX_BODY values per atmofx-body.md
DEFAULTS_HEX_RGB = {
    "glow":     (191, 80, 50, 1.4),
    "glow_hot": (191, 90, 65, 2.5),
}

# ─────────────────────────────────────────────────────────────────────
# Engine-computed bulk-gas colors — the 5 plasma slots derived from the
# composition + the planet's entry velocity, instead of hardcoded palettes.
#
# Firefly cfg semantics (verified against M1rageDev/Firefly source):
#   each Color slot → a shader global (AtmoFxModule.cs:322-333):
#     shockwave→_ShockwaveColor (bow shock, hottest), wrap_layer→_LayerColor
#     (plasma envelope), trail_primary/secondary/tertiary→_Primary/_Secondary/
#     _TertiaryColor (wake, inner→outer cooling), glow/glow_hot→_Glow/_HotGlow
#     (hull surface, material-driven), *_streak→secondary-species accents.
#   HDR value = (R/255, G/255, B/255) × 2^intensity  (Utils.cs SDRI_To_HDR).
# So the 9 slots are a TEMPERATURE LADDER: shock (peak, non-LTE) → wrap (hot) →
# trail (cooling) → hull blackbody. The engine fills the 5 gas slots' HUE from
# the LTE/2-T plasma model at that ladder of temperatures; intensity stays at the
# Firefly-shipped per-slot values (the mod author's brightness balance).
# ─────────────────────────────────────────────────────────────────────
sys.path.insert(0, str(ROOT / "scripts" / "refs"))
try:
    import saha_boltzmann as _sb          # noqa: E402
    import cie_color as _cie              # noqa: E402
    import reentry_color as _rc           # noqa: E402
    import emit_atmosphere_color as _eac  # noqa: E402
    _ENGINE_OK = True
except Exception:                          # engine unavailable → keep hardcoded palettes
    _ENGINE_OK = False

# per-slot HDR intensity (Firefly shipped balance) + temperature-ladder fraction
# of the peak (shock) gas temperature; shock+wrap also get the non-LTE T_elec.
_SLOT = {  # slot: (intensity, T_fraction, use_nlte)
    "shockwave":       (3.0, 1.00, True),
    "wrap_layer":      (2.0, 0.85, True),
    "trail_primary":   (3.0, 0.60, False),
    "trail_secondary": (1.5, 0.45, False),
    "trail_tertiary":  (2.0, 0.35, False),
}
_ENGINE_DBS = None


def _num_lead(s: str) -> float | None:
    m = re.search(r"-?\d+\.?\d*(?:[eE][-+]?\d+)?", (s or "").replace(",", ""))
    return float(m.group()) if m else None


def escape_velocity_kms(dec: dict) -> float | None:
    """Entry velocity ≈ escape velocity from the Phase 3 Decisions mass + radius.
    v_esc = 11.186·sqrt(M/R) [km/s] (Earth units). Falls through mass/radius in
    Earth, then Jupiter units, then surface gravity + radius."""
    me, re_ = _num_lead(dec.get("mass_mearth", "")), _num_lead(dec.get("radius_rearth", ""))
    if me and re_ and re_ > 0:
        return 11.186 * (me / re_) ** 0.5
    mj, rj = _num_lead(dec.get("mass_mjup", "")), _num_lead(dec.get("radius_rjup", ""))
    if mj and rj and rj > 0:
        return 11.186 * (mj * 317.83 / (rj * 11.209)) ** 0.5
    g, re2 = _num_lead(dec.get("surface_gravity_g_earth", "")), _num_lead(dec.get("radius_rearth", ""))
    if g and re2 and re2 > 0:
        return 11.186 * (g * re2) ** 0.5   # v=sqrt(2gR), Earth sqrt(2·1·1)=11.186
    return None


def engine_palette(species: list, velocity: float):
    """Physics-derived 5-slot palette {slot:(R,G,B,intensity)} from composition +
    entry velocity, or None if the engine can't resolve the composition."""
    if not _ENGINE_OK:
        return None
    global _ENGINE_DBS
    if _ENGINE_DBS is None:
        _ENGINE_DBS = _sb.load_dbs()
    atomic, mol_db = _ENGINE_DBS
    comp_str = ",".join(f"{s}:{(pct if pct else 1.0)}" for s, pct in species)
    elems, _dropped, _mols = _eac.composition_to_atoms(comp_str)
    if not elems:
        return None
    bands = _eac.select_bands(elems, mol_db)
    t_gas, t_elec = _rc.velocity_to_temps(velocity)
    out = {}
    for slot, (inten, frac, nlte) in _SLOT.items():
        T = max(1000, min(15000, round(t_gas * frac / 500) * 500))
        spec, _d = _sb.slab_spectrum_custom(elems, bands, T, atomic, mol_db,
                                            t_elec=(t_elec if nlte else None))
        r, g, b = _cie.hex_to_rgb(_cie.spectrum_to_hex(spec))
        out[slot] = (round(r * 255), round(g * 255), round(b * 255), inten)
    return out

# ─────────────────────────────────────────────────────────────────────
# Parsing helpers
# ─────────────────────────────────────────────────────────────────────

# Strip Unicode subscript digits → ASCII so "N₂" → "N2"
SUBSCRIPT_MAP = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
SUPERSCRIPT_MAP = str.maketrans({"⁰": "0", "¹": "1", "²": "2", "³": "3",
                                  "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7",
                                  "⁸": "8", "⁹": "9", "⁻": "-", "⁺": "+"})


def normalize_species(s: str) -> str:
    """N₂ → N2, CO₂ → CO2, H₂O → H2O."""
    return s.translate(SUBSCRIPT_MAP).strip()


def parse_pressure_pa(raw: str) -> float | None:
    """Parse strings like '100000', '100 000', '10⁻⁹', '100000 (1 bar)'."""
    s = raw.translate(SUPERSCRIPT_MAP)
    # Strip parenthetical
    s = re.sub(r"\(.*?\)", "", s)
    # Handle scientific notation 10⁻⁹ → 10-9 → 1e-9 (sign required to
    # disambiguate from large plain integers like "100000")
    m = re.match(r"\s*10\s*([+-]\d+)\s*$", s)
    if m:
        return 10.0 ** int(m.group(1))
    # Handle compact "100 000" → "100000"
    s = re.sub(r"(\d)\s+(\d)", r"\1\2", s)
    # Pull first float
    m = re.search(r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?", s)
    return float(m.group(0)) if m else None


def parse_present(raw: str) -> bool:
    """Parse 'true', 'true (very thin)', 'false (vestigial)' → bool."""
    s = raw.strip().lower()
    return s.startswith("true")


# Match "N₂ 78%", "O₂ ~5%", "CO₂ 5%", "H₂O 0.1–1%"
SPECIES_PCT_RE = re.compile(
    r"([A-Z][A-Za-z]?\d?(?:[A-Z][a-z]?\d*)*[₀-₉\d]*)\s*"  # species
    r"(?:~)?\s*"
    r"(\d+(?:[.–—-]\d+)?)\s*%",
)


def parse_composition(raw: str) -> list[tuple[str, float | None]]:
    """Phase 3 prose like 'N₂ 78%, O₂ ~5%, CO₂ ~1%' → [('N2', 78), ('O2', 5), ('CO2', 1)].

    For tokens without explicit %, returns (species, None) preserving order.
    Returns [] if no species can be parsed.
    """
    norm = normalize_species(raw)
    results = []
    matched_spans = []
    for m in SPECIES_PCT_RE.finditer(norm):
        sp = m.group(1)
        pct_str = m.group(2)
        # Handle ranges like "0.1–1" → take midpoint
        pct_str = pct_str.replace("–", "-").replace("—", "-")
        if "-" in pct_str:
            try:
                lo, hi = [float(x) for x in pct_str.split("-")]
                pct = (lo + hi) / 2
            except Exception:
                pct = None
        else:
            try:
                pct = float(pct_str)
            except Exception:
                pct = None
        results.append((sp, pct))
        matched_spans.append((m.start(), m.end()))

    if results:
        return results

    # No percentages — try to extract bare species names in listed order.
    bare_species_re = re.compile(r"\b([A-Z][a-z]?[0-9]*(?:O|H|N|C|S|F|Cl|Br)?\d*)\b")
    seen = []
    for m in bare_species_re.finditer(norm):
        sp = m.group(1)
        if sp not in seen and len(sp) <= 4:
            seen.append(sp)
    return [(sp, None) for sp in seen]


def slug_to_kopernicus_name(slug: str) -> str:
    """proxima-cen-b → ProximaCenB; trappist-1-d → Trappist1D."""
    parts = slug.split("-")
    out = []
    for p in parts:
        if p.isdigit():
            out.append(p)
        else:
            out.append(p.capitalize())
    return "".join(out)


def planet_letter_uppercase(name: str) -> str:
    """For 'Trappist1d' → 'Trappist1D' (last lowercase letter uppercased)."""
    if name and name[-1].islower():
        return name[:-1] + name[-1].upper()
    return name


# ─────────────────────────────────────────────────────────────────────
# Decisions-table extraction
# ─────────────────────────────────────────────────────────────────────

DECISIONS_HEADER = re.compile(r"^##\s+Decisions\s*$", re.MULTILINE)
ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|", re.MULTILINE)


def extract_decisions(md: str) -> dict[str, str]:
    """Return {field_name: value_cell_text} for every Decisions table row.

    Stops at the next ## heading.
    """
    m = DECISIONS_HEADER.search(md)
    if not m:
        return {}
    after = md[m.end():]
    nxt = re.search(r"^##\s+", after, re.MULTILINE)
    block = after[:nxt.start()] if nxt else after

    decisions = {}
    for r in ROW_RE.finditer(block):
        field = r.group(1).strip()
        value = r.group(2).strip()
        decisions[field] = value
    return decisions


# ─────────────────────────────────────────────────────────────────────
# Emit core
# ─────────────────────────────────────────────────────────────────────

def pick_palette(dominant: str, others: set[str]) -> tuple[str, dict]:
    for name, palette in PALETTES.items():
        if palette["_match"](dominant, others):
            return name, palette
    return PALETTE_FALLBACK, PALETTES[PALETTE_FALLBACK]


def fmt_color(rgb_intensity: tuple) -> str:
    r, g, b, i = rgb_intensity
    return f"{int(r)} {int(g)} {int(b)} {i:g}"


def pressure_to_strength(p_bar: float) -> float:
    """Piecewise from phase3-mapping.md §3 calibration table."""
    if p_bar < 0.01:  return 0.5
    if p_bar < 0.5:   return 0.7
    if p_bar < 2.0:   return 1.0
    if p_bar < 20.0:  return 1.1
    if p_bar < 50.0:  return 1.2
    return 1.3


def pressure_to_alpha_damp(p_bar: float) -> float:
    """Trail/wrap layer alpha damping for thin atmospheres.

    Mirrors Firefly mod's Tekto / Thatmo / Ervo pattern: low-pressure
    bodies get alpha multiplied down on the visible plasma layers, not
    just the overall strength_multiplier. Without this, thin atmospheres
    look too vivid relative to the strength_multiplier reduction alone.
    """
    if p_bar < 0.01:  return 0.30   # Mars-thin and below
    if p_bar < 0.1:   return 0.55   # thin
    if p_bar < 0.5:   return 0.75   # thin-to-medium
    return 1.0                       # Earth-like and thicker — no damp


def _damp(rgb_i: tuple, factor: float) -> tuple:
    """Multiply intensity (4th component) of an (R, G, B, i) tuple."""
    r, g, b, i = rgb_i
    return (r, g, b, i * factor)


def render_atmofx_body(kop_name: str, palette_name: str, palette: dict,
                       streak_rgb: tuple, pressure_pa: float,
                       temp_k: float | None) -> str:
    pressure_bar = pressure_pa / 100_000.0
    strength = pressure_to_strength(pressure_bar)
    fresnel = 1 if pressure_bar >= 1.0 else 0
    particle_threshold = 1500 if (temp_k is not None and temp_k > 300) else 1800

    # Apply thin-atmosphere alpha damping to trail + wrap layers.
    # glow / glow_hot are hull-surface (material-driven), not damped.
    # shockwave is the leading edge — keep at full intensity even in thin
    # atmospheres so the shock is still visible.
    alpha_damp = pressure_to_alpha_damp(pressure_bar)
    trail_p = _damp(palette["trail_primary"],   alpha_damp)
    trail_s = _damp(palette["trail_secondary"], alpha_damp)
    trail_t = _damp(palette["trail_tertiary"],  alpha_damp)
    trail_streak = _damp(streak_rgb, alpha_damp)
    wrap_layer = _damp(palette["wrap_layer"],   alpha_damp)
    wrap_streak = _damp(streak_rgb, alpha_damp)

    glow = DEFAULTS_HEX_RGB["glow"]
    glow_hot = DEFAULTS_HEX_RGB["glow_hot"]

    damp_note = f" (alpha damp ×{alpha_damp:.2f})" if alpha_damp < 1.0 else ""

    return f"""// Generated by .claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py
// Bulk-gas palette: {palette_name}{damp_note}
ATMOFX_BODY:NEEDS[NearStarsSystem]
{{
\tname = {kop_name}
\tconfig_version = 5

\tstrength_multiplier = {strength:.2f}
\tlength_multiplier = 1
\topacity_multiplier = 1
\tglow_multiplier = 1
\twrap_opacity_multiplier = 1
\twrap_fresnel_modifier = {fresnel}

\tparticle_threshold = {particle_threshold}
\tstreak_probability = 0.07
\tstreak_threshold = 0

\tColor
\t{{
\t\tglow            = {fmt_color(glow)}
\t\tglow_hot        = {fmt_color(glow_hot)}
\t\ttrail_primary   = {fmt_color(trail_p)}
\t\ttrail_secondary = {fmt_color(trail_s)}
\t\ttrail_tertiary  = {fmt_color(trail_t)}
\t\ttrail_streak    = {fmt_color(trail_streak)}
\t\twrap_layer      = {fmt_color(wrap_layer)}
\t\twrap_streak     = {fmt_color(wrap_streak)}
\t\tshockwave       = {fmt_color(palette['shockwave'])}
\t}}
}}
"""


def render_planet_pack(bodies: list[str]) -> str:
    body_list = ", ".join(bodies)
    return f"""// Generated by .claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py
ATMOFX_PLANET_PACK:NEEDS[NearStarsSystem]
{{
\tname = NearStars

\tstrength_multiplier = 1
\ttransition_offset = 0.2

\taffected_bodies = {body_list}
}}
"""


# ─────────────────────────────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────────────────────────────

class EmitOutcome:
    def __init__(self):
        self.emitted: list[tuple[str, str]] = []        # (slug, kop_name)
        self.skipped_no_atm: list[str] = []
        self.skipped_thin: list[str] = []
        self.warnings: list[str] = []
        self.errors: list[str] = []


def process_slug(slug: str, element_db: dict, outcome: EmitOutcome,
                 dry_run: bool) -> tuple[str, str] | None:
    md_path = PHASE3_DIR / f"{slug}.md"
    if not md_path.exists():
        outcome.errors.append(f"{slug}: Phase 3 markdown missing")
        return None

    text = md_path.read_text(encoding="utf-8")
    dec = extract_decisions(text)
    if not dec:
        outcome.errors.append(f"{slug}: no Decisions section")
        return None

    # Star Phase 3 files (no atmosphere) — skip
    if "atmosphere_present" not in dec:
        outcome.skipped_no_atm.append(slug)
        return None

    if not parse_present(dec["atmosphere_present"]):
        outcome.skipped_no_atm.append(slug)
        return None

    # Gas giants have no solid surface, so Phase 3 records their cfg-reference
    # level under atmosphere_reference_pressure_pa (typically 1 bar = 100000 Pa,
    # the cloud-deck render reference) instead of *_surface_pressure_pa.
    pressure_raw = (dec.get("atmosphere_surface_pressure_pa")
                    or dec.get("atmosphere_pressure_pa")
                    or dec.get("atmosphere_reference_pressure_pa"))
    if not pressure_raw:
        outcome.warnings.append(f"{slug}: atmosphere_present=true but no pressure field; skipping")
        outcome.skipped_no_atm.append(slug)
        return None
    pressure_pa = parse_pressure_pa(pressure_raw)
    if pressure_pa is None:
        outcome.warnings.append(f"{slug}: pressure unparseable {pressure_raw!r}; skipping")
        return None
    if pressure_pa < PRESSURE_THRESHOLD_PA:
        outcome.skipped_thin.append(f"{slug} (P={pressure_pa:g} Pa)")
        return None

    comp_raw = dec.get("atmosphere_composition")
    if not comp_raw:
        outcome.warnings.append(f"{slug}: missing atmosphere_composition; using Earth-like default")
        species = [("N2", 78.0), ("O2", 21.0)]
    else:
        species = parse_composition(comp_raw)
        if not species:
            outcome.warnings.append(f"{slug}: composition unparseable {comp_raw!r}; using Earth-like")
            species = [("N2", 78.0), ("O2", 21.0)]

    species_set = {s for s, _ in species}
    dominant = species[0][0]

    # Bulk-gas colors: prefer the physics engine (composition + entry velocity
    # → temperature ladder + non-LTE shock); fall back to the hardcoded
    # composition palette only if the engine can't resolve the composition.
    velocity = escape_velocity_kms(dec) or 7.8
    ep = engine_palette(species, velocity)
    if ep is not None:
        palette, palette_name = ep, f"engine:{dominant}@{velocity:.1f}km/s"
    else:
        palette_name, palette = pick_palette(dominant, species_set)
        if palette_name == PALETTE_FALLBACK and not PALETTES[PALETTE_FALLBACK]["_match"](dominant, species_set):
            outcome.warnings.append(
                f"{slug}: engine + palette unmatched for {dominant}; fell back to {PALETTE_FALLBACK}")

    # Streak species: among all qualifying secondaries (0.5–10% by volume, or
    # unquantified trace), pick the STRONGEST visible emitter per the
    # composition-color.md §4 priority — not merely the first in document order.
    streak_rgb = palette["trail_primary"]  # default fallback
    candidates = []  # (priority, rgb_tuple)
    for sp, pct in species[1:]:
        if pct is None or 0.5 <= pct <= 10.0:
            rgb = None
            if sp in STREAK_PALETTE:
                rgb = STREAK_PALETTE[sp]
            elif sp in element_db:
                # v2 schema: prefer reentry_plasma regime (matches Firefly physics);
                # fall back to atomic_flame if no reentry data
                regimes = element_db[sp].get("regimes", {})
                pick = regimes.get("reentry_plasma") or regimes.get("atomic_flame")
                if pick and pick.get("status") == "visible" and pick.get("hex"):
                    hx = pick["hex"].lstrip("#")
                    rgb = (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16), 2.0)
            if rgb is not None:
                candidates.append((STREAK_PRIORITY.get(sp, 8), rgb))
    if candidates:
        candidates.sort(key=lambda c: c[0])
        streak_rgb = candidates[0][1]

    # Temperature for particle_threshold
    temp_k = None
    for tkey in ("atmosphere_temperature_K_surface", "equilibrium_temp_k",
                 "surface_temp_substellar_k"):
        if tkey in dec:
            v = parse_pressure_pa(dec[tkey])
            if v is not None:
                temp_k = v
                break

    kop_name = planet_letter_uppercase(slug_to_kopernicus_name(slug))
    cfg = render_atmofx_body(kop_name, palette_name, palette, streak_rgb, pressure_pa, temp_k)

    if not dry_run:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / f"{kop_name}.cfg").write_text(cfg, encoding="utf-8")
    outcome.emitted.append((slug, kop_name))
    return slug, kop_name


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="Compute outputs and report but don't write files")
    ap.add_argument("--slug", action="append", default=[],
                    help="Limit to specific phase3 slug(s) (repeatable); default = all")
    args = ap.parse_args()

    with open(ELEMENT_DB, encoding="utf-8") as f:
        element_db = yaml.safe_load(f)

    if args.slug:
        slugs = args.slug
    else:
        slugs = sorted(p.stem for p in PHASE3_DIR.glob("*.md"))

    outcome = EmitOutcome()
    for slug in slugs:
        process_slug(slug, element_db, outcome, args.dry_run)

    bodies = [kop for _, kop in outcome.emitted]
    if bodies and not args.dry_run:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / "NearStarsPlanetPack.cfg").write_text(render_planet_pack(bodies), encoding="utf-8")

    # Report
    mode = "DRY-RUN" if args.dry_run else "WROTE"
    print(f"=== Firefly emit {mode} ===")
    print(f"emitted ATMOFX_BODY: {len(outcome.emitted)}")
    for slug, kop in outcome.emitted:
        print(f"  {slug:25s} → {kop}.cfg")
    if outcome.skipped_no_atm:
        print(f"\nskipped (no atmosphere): {len(outcome.skipped_no_atm)}")
        for s in outcome.skipped_no_atm:
            print(f"  {s}")
    if outcome.skipped_thin:
        print(f"\nskipped (pressure < {PRESSURE_THRESHOLD_PA:g} Pa): {len(outcome.skipped_thin)}")
        for s in outcome.skipped_thin:
            print(f"  {s}")
    if outcome.warnings:
        print(f"\nwarnings: {len(outcome.warnings)}")
        for w in outcome.warnings:
            print(f"  {w}")
    if outcome.errors:
        print(f"\nERRORS: {len(outcome.errors)}")
        for e in outcome.errors:
            print(f"  {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
