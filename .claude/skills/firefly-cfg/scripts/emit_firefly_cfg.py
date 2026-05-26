# Phase 3 합성문 → Firefly ATMOFX_BODY + ATMOFX_PLANET_PACK cfg 일괄 emitter
"""Emit Firefly ATMOFX cfgs from Phase 3 syntheses + the element plasma DB.

Reads per planet:
  docs/phase3/<slug>.md         — Decisions table (atmosphere fields)

Reads project-wide:
  db/refs/element_plasma_colors.yaml  — per-element hex (for streak/trace species)

Writes:
  dist/NearStars-Configs/Patches/Firefly/<KopernicusName>.cfg  — one per atm body
  dist/NearStars-Configs/Patches/Firefly/NearStarsPlanetPack.cfg

Per [[composition-color]] §3, the bulk-gas color palette is determined by
the DOMINANT atmospheric species in the Phase 3 Decisions table. The
emitter holds the palette table inline (a small finite set of physics-
grounded palettes) — see PALETTES below. Element-level streak colors
come from the shared `element_plasma_colors.yaml` DB.

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
    "gas_giant": {
        "_match": lambda dom, others: dom == "H2" and "He" in others,
        "trail_primary":   (191, 99, 110, 3.0),
        "trail_secondary": (191, 80, 80, 1.5),
        "trail_tertiary":  (255, 180, 90, 2.0),
        "wrap_layer":      (255, 200, 100, 2.0),
        "shockwave":       (255, 180, 90, 3.0),
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
    "CH4": (100, 191, 130, 2.0),
    "H2O": (191, 130, 130, 2.0),
    "He":  (255, 200, 100, 2.0),
    "SO2": (150, 200, 180, 2.0),
    "H2S": (150, 200, 180, 2.0),
    "Na":  (255, 200, 60, 2.5),
    "K":   (180, 100, 191, 2.5),
    "Fe":  (191, 191, 100, 2.0),
    "Mg":  (100, 191, 100, 2.0),
    "CN":  (130, 80, 191, 2.0),    # tholin haze
    "O2":  (180, 180, 255, 2.0),   # uncommon as secondary but possible
    "N2":  (74, 90, 191, 2.0),
    "Ar":  (160, 107, 255, 2.0),
}

# Default ATMOFX_BODY values per atmofx-body.md
DEFAULTS_HEX_RGB = {
    "glow":     (191, 80, 50, 1.4),
    "glow_hot": (191, 90, 65, 2.5),
}

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


def render_atmofx_body(kop_name: str, palette_name: str, palette: dict,
                       streak_rgb: tuple, pressure_pa: float,
                       temp_k: float | None) -> str:
    pressure_bar = pressure_pa / 100_000.0
    strength = pressure_to_strength(pressure_bar)
    fresnel = 1 if pressure_bar >= 1.0 else 0
    particle_threshold = 1500 if (temp_k is not None and temp_k > 300) else 1800

    glow = DEFAULTS_HEX_RGB["glow"]
    glow_hot = DEFAULTS_HEX_RGB["glow_hot"]

    return f"""// Generated by .claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py
// Bulk-gas palette: {palette_name} (composition-color.md §3)
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
\t\ttrail_primary   = {fmt_color(palette['trail_primary'])}
\t\ttrail_secondary = {fmt_color(palette['trail_secondary'])}
\t\ttrail_tertiary  = {fmt_color(palette['trail_tertiary'])}
\t\ttrail_streak    = {fmt_color(streak_rgb)}
\t\twrap_layer      = {fmt_color(palette['wrap_layer'])}
\t\twrap_streak     = {fmt_color(streak_rgb)}
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

    pressure_raw = dec.get("atmosphere_surface_pressure_pa") or dec.get("atmosphere_pressure_pa")
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
    palette_name, palette = pick_palette(dominant, species_set)
    if palette_name == PALETTE_FALLBACK and not PALETTES[PALETTE_FALLBACK]["_match"](dominant, species_set):
        outcome.warnings.append(
            f"{slug}: dominant species {dominant} doesn't match any palette; falling back to {PALETTE_FALLBACK}"
        )

    # Streak species: first secondary (0.5–10%) that's in our streak palette
    streak_rgb = palette["trail_primary"]  # default fallback
    for sp, pct in species[1:]:
        if pct is None or 0.5 <= pct <= 10.0:
            if sp in STREAK_PALETTE:
                streak_rgb = STREAK_PALETTE[sp]
                break
            elif sp in element_db and element_db[sp]["status"] == "visible":
                # Convert hex → RGB
                hx = element_db[sp]["hex"].lstrip("#")
                streak_rgb = (int(hx[0:2], 16), int(hx[2:4], 16), int(hx[4:6], 16), 2.0)
                break

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
