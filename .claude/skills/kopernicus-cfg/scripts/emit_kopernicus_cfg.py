#!/usr/bin/env python3
# DB → Kopernicus cfg emitter: star bodies (render) + circumstellar/planet rings
"""Emit Kopernicus cfg patches for NearStars.

Two layers, two output files:
  * stars.cfg       — full star bodies: Properties + ScaledVersion
                      {Light, Material, Coronas}, colors/luminosity derived
                      from curated Teff/L/R (see star_fields.py; the base
                      photospheric color comes from the grounded engine
                      scripts/refs/stellar_photospheric_color.py).
  * disk-rings.cfg  — stellar debris-disk rings (from
                      db/systems/*.json `stars[0].raw.disk_measurements`) and
                      Saturn-like planet rings (from
                      `phase3/<system>/kopernicus_extras.yaml`).

Still deferred: full planet bodies (Properties/Orbit/PQS/Atmosphere), and
the star `Orbit` is a placeholder (Principia owns the real state).

Inputs:
    db/systems/<slug>.json
        stars[0].raw.disk_measurements[]   ← per-belt geometry, per-paper
    docs/phase3/<slug>.md
        Decisions table                     ← disk_tint_rgb_hex, disk_opacity
    phase3/<system>/kopernicus_extras.yaml  (optional)
        <planet>:                           ← ring_present, ring_*_au, ring_color_hex
            ring_present: true
            ring_inner_au: ...
            ...

Output:
    dist/NearStars-Configs/Patches/Kopernicus/stars.cfg
        one Body{} per star (Template Sun + Properties + ScaledVersion render).
    dist/NearStars-Configs/Patches/Kopernicus/disk-rings.cfg
        single combined MM patch — one @Body[<Star>] per star w/ disk,
        plus one @Body[<Planet>] per planet w/ ring_present=true.

Usage:
    python3 .claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py
    python3 .claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py --dry-run
    python3 .claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py vega fomalhaut
    python3 .claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py --output /tmp/foo.cfg

See `.claude/skills/kopernicus-cfg/references/gas-giant.md` for the
upstream Ring node template + `phase3/kopernicus-emit-workspace/`
for the design notes.
"""
# TODO(emit_kopernicus_cfg.py v3): full Properties block (gravParameter, radius, displayName, description)
# TODO(emit_kopernicus_cfg.py v3): full Orbit block (referenceBody, semiMajorAxis, eccentricity, …)
# TODO(emit_kopernicus_cfg.py v3): PQS terrain mods (Parallax + standard PQSMods chain)
# TODO(emit_kopernicus_cfg.py v3): Atmosphere node (pressureCurve, temperatureCurve, ScaledVersion type)
# DONE(v3): star bodies — Properties + ScaledVersion{Light, Material, Coronas} from Teff/L/R
#   (star_fields.py; base color from grounded engine scripts/refs/stellar_photospheric_color.py)
# TODO(v3): star Orbit is a placeholder — wire real galactic placement / GalacticOrbit (Principia overrides for now)
# TODO(emit_kopernicus_cfg.py v3): Module Manager NEEDS / AFTER ordering beyond FOR[NearStarsSystem]
# TODO(emit_kopernicus_cfg.py v3): flightGlobalsIndex allocation per system (sidecar yaml top-level)
# v2 fix (2026-05-27): Ring nesting + units corrected per gas-giant.md / nodes-quick-ref.md /
#   mod-grounded-fields.md (canonical). Rings is now a direct child of @Body (sibling to
#   ScaledVersion); innerRadius/outerRadius are body-radius multipliers (not km); tilt field
#   renamed `rotation` → `angle`; standard default fields added; multi-paper geometry merge
#   backfills nulls on the recommended belt entry from non-recommended same-belt entries.

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import star_fields  # noqa: E402  (sibling module — Teff/L → ScaledVersion field synthesis; base color from the grounded engine)

REPO_ROOT = Path(__file__).resolve().parents[4]
DB_SYSTEMS_DIR = REPO_ROOT / "db" / "systems"
PHASE3_DOCS_DIR = REPO_ROOT / "docs" / "phase3"
PHASE3_WORKSPACE_DIR = REPO_ROOT / "phase3"
DEFAULT_OUTPUT = REPO_ROOT / "dist" / "NearStars-Configs" / "Patches" / "Kopernicus" / "disk-rings.cfg"
DEFAULT_STARS_OUTPUT = REPO_ROOT / "dist" / "NearStars-Configs" / "Patches" / "Kopernicus" / "stars.cfg"

# Placeholder Kopernicus Orbit for a NearStars star body. Principia's
# initial_state overrides the trajectory in n-body mode; real Kopernicus
# galactic placement is a separate task (db/systems has no distance field yet).
STAR_ORBIT_PLACEHOLDER_SMA_M = 1.0e16   # ~1.06 ly — clearly a placeholder
STAR_CACHE_FILE = "ParallaxContinued/Models/ScaledMesh.bin"
SECONDS_PER_DAY = 86400.0

MM_HEADER = "@Kopernicus:FOR[NearStarsSystem]"

# 1 AU in km — IAU 2012 definition. Kopernicus Ring innerRadius/outerRadius are
# **body-radius multipliers** (NOT km) per `gas-giant.md` § Rings and
# `mod-grounded-fields.md` § "Circumstellar disk → Kopernicus Ring". Converted as
# `(au × AU_TO_KM) / body_radius_km`.
AU_TO_KM = 1.495978707e8

# Defaults for missing optional fields (warned, not aborted)
DEFAULT_DISK_OPACITY = 0.10
DEFAULT_DISK_TINT_HEX = "#b0a090"           # neutral warm-grey
DEFAULT_RING_OPACITY = 0.80
DEFAULT_RING_TINT_HEX = "#cab48c"           # Saturn-ish buff
# Narrow-ring width fallback when DB has inner but not outer (or vice versa)
NARROW_RING_WIDTH_FACTOR = 1.2              # outer = inner × 1.2


# ─────────────────────────────────────────────────────────────────────
# Body-name normalization (matches emit_principia_cfg.py)
# ─────────────────────────────────────────────────────────────────────

def normalize_body_name(raw: str) -> str:
    parts: list[str] = []
    for word in raw.split():
        token = re.sub(r"[^A-Za-z0-9]", "", word)
        if not token:
            continue
        if any(c.isupper() for c in token):
            parts.append(token)
        else:
            parts.append(token[0].upper() + token[1:])
    return "".join(parts)


def slug_to_kopernicus_name(slug: str) -> str:
    """proxima-cen-b → ProximaCenB. Mirrors emit_firefly_cfg.py."""
    parts = slug.split("-")
    out = []
    for p in parts:
        out.append(p if p.isdigit() else p.capitalize())
    name = "".join(out)
    # planet-letter uppercase: 'Trappist1d' → 'Trappist1D'
    if name and name[-1].islower():
        name = name[:-1] + name[-1].upper()
    return name


# ─────────────────────────────────────────────────────────────────────
# Phase 3 Decisions table extraction (factored from emit_firefly_cfg.py)
# ─────────────────────────────────────────────────────────────────────

DECISIONS_HEADER = re.compile(r"^##\s+Decisions\s*$", re.MULTILINE)
ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|", re.MULTILINE)


def extract_decisions(md: str) -> dict[str, str]:
    """Return {field_name: raw_value_cell_text} for every Decisions row."""
    m = DECISIONS_HEADER.search(md)
    if not m:
        return {}
    after = md[m.end():]
    nxt = re.search(r"^##\s+", after, re.MULTILINE)
    block = after[:nxt.start()] if nxt else after
    decisions = {}
    for r in ROW_RE.finditer(block):
        decisions[r.group(1).strip()] = r.group(2).strip()
    return decisions


# ─────────────────────────────────────────────────────────────────────
# Color helpers
# ─────────────────────────────────────────────────────────────────────

HEX_RE = re.compile(r"#?([0-9a-fA-F]{6})")


def parse_hex_rgb(raw: str) -> tuple[float, float, float] | None:
    """Pull the first #RRGGBB from prose like '#ffd9a8 (warm-amber …)'.

    Returns floats in [0, 1] for Kopernicus color cfg.
    """
    if not raw:
        return None
    m = HEX_RE.search(raw)
    if not m:
        return None
    hx = m.group(1)
    return (int(hx[0:2], 16) / 255.0,
            int(hx[2:4], 16) / 255.0,
            int(hx[4:6], 16) / 255.0)


def parse_opacity(raw: str) -> float | None:
    """Pull a leading float from prose like '0.06 (cold belt); 0.02 …'.

    The first numeric is taken — for multi-belt prose, the cfg uses the
    most-visible value (cfg author's responsibility to put that first).
    """
    if not raw:
        return None
    m = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", raw)
    return float(m.group(0)) if m else None


def fmt_color(rgb: tuple[float, float, float], alpha: float) -> str:
    """Kopernicus expects comma-separated 0–1 floats per nodes-quick-ref.md."""
    r, g, b = rgb
    return f"{r:.3f},{g:.3f},{b:.3f},{alpha:.3f}"


# ─────────────────────────────────────────────────────────────────────
# Belt + ring data classes
# ─────────────────────────────────────────────────────────────────────

@dataclass
class DiskRing:
    """One Ring node's worth of data for a star body."""
    belt: str | None
    inner_au: float
    outer_au: float
    inclination_deg: float
    reference: str
    bibcode: str | None


@dataclass
class StarDisk:
    """All recommended belts + Phase 3 visual decisions for a star."""
    body_name: str
    system_slug: str          # for traceability + Phase 3 md lookup
    star_radius_km: float     # for AU → body-radius-multiplier conversion
    rings: list[DiskRing] = field(default_factory=list)
    tint_rgb: tuple[float, float, float] = (0, 0, 0)
    opacity: float = DEFAULT_DISK_OPACITY


@dataclass
class PlanetRing:
    """One Ring node's worth of data for a planet body (sidecar yaml)."""
    body_name: str
    planet_key: str           # original key from kopernicus_extras.yaml
    system_slug: str
    planet_radius_km: float   # for AU → body-radius-multiplier conversion
    inner_au: float
    outer_au: float
    tint_rgb: tuple[float, float, float]
    opacity: float


# ─────────────────────────────────────────────────────────────────────
# Loaders
# ─────────────────────────────────────────────────────────────────────

class EmitError(RuntimeError):
    """Raised on structurally fatal input problems."""


@dataclass
class StarRender:
    """One star body's render inputs (Properties + ScaledVersion Light/Material/Coronas)."""
    body_name: str
    display_name: str
    radius_m: float
    grav_parameter: float
    rotation_period_s: float
    teff_k: float
    luminosity_lsun: float
    spectype: str | None


@dataclass
class Outcome:
    star_disks: list[StarDisk] = field(default_factory=list)
    planet_rings: list[PlanetRing] = field(default_factory=list)
    star_renders: list[StarRender] = field(default_factory=list)
    skipped_no_disk: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def discover_slugs() -> list[str]:
    """Every db/systems/*.json stem, sorted."""
    if not DB_SYSTEMS_DIR.is_dir():
        raise EmitError(f"db dir not found: {DB_SYSTEMS_DIR}")
    return sorted(p.stem for p in DB_SYSTEMS_DIR.glob("*.json"))


def load_star_disk(slug: str, outcome: Outcome) -> StarDisk | None:
    """Read DB + Phase 3 md and return a StarDisk if any recommended belts exist.

    Returns None if the star has no disk_measurements (silently skipped) or
    if no belt is marked `recommended` (warned + treated as no-disk).
    Appends per-field validation errors to `outcome.errors`.
    """
    db_path = DB_SYSTEMS_DIR / f"{slug}.json"
    if not db_path.exists():
        outcome.errors.append(f"{slug}: db/systems/{slug}.json missing")
        return None

    with db_path.open(encoding="utf-8") as f:
        data = json.load(f)

    stars = data.get("stars") or []
    if not stars:
        outcome.errors.append(f"{slug}: no stars in DB file")
        return None
    star = stars[0]
    raw = star.get("raw") or {}
    disk_measurements = raw.get("disk_measurements")

    if not disk_measurements:
        outcome.skipped_no_disk.append(slug)
        return None

    # Per-belt validation: every entry must have a `recommended` field
    # (True or False — schema docs say it's required).
    missing_rec = [
        f"  belt entry #{i} ({entry.get('belt') or '<unnamed>'}, "
        f"ref={entry.get('reference')!r}) has no `recommended` field"
        for i, entry in enumerate(disk_measurements)
        if "recommended" not in entry
    ]
    if missing_rec:
        outcome.errors.append(
            f"{slug}: disk_measurements has entries missing `recommended`:\n"
            + "\n".join(missing_rec)
        )
        return None

    recommended = [e for e in disk_measurements if e.get("recommended")]
    if not recommended:
        outcome.warnings.append(
            f"{slug}: disk_measurements has {len(disk_measurements)} entries but "
            f"none marked recommended=true — skipping disk emission"
        )
        outcome.skipped_no_disk.append(slug)
        return None

    # Multi-paper geometry merge: for each recommended belt, scan all same-belt
    # entries (recommended OR not) and backfill nulls on the recommended entry
    # from non-null values elsewhere. Recommended remains canonical for its own
    # non-null fields. Each backfilled field is logged to stderr for audit.
    MERGEABLE_FIELDS = ("inner_radius_au", "outer_radius_au", "inclination_deg")
    merged_recommended: list[dict] = []
    for rec in recommended:
        merged = dict(rec)  # shallow copy — we only patch top-level scalars
        belt = rec.get("belt")
        for fld in MERGEABLE_FIELDS:
            if merged.get(fld) is not None:
                continue
            # Look for a same-belt sibling with a non-null value for this field.
            for sib in disk_measurements:
                if sib is rec:
                    continue
                if sib.get("belt") != belt:
                    continue
                val = sib.get(fld)
                if val is None:
                    continue
                merged[fld] = val
                merged.setdefault("_backfill_log", []).append(
                    f"{fld}={val} from {sib.get('reference') or '?'}"
                    + (f" ({sib.get('bibcode')})" if sib.get('bibcode') else "")
                )
                outcome.warnings.append(
                    f"{slug} {belt}: {fld} backfilled from "
                    f"{sib.get('reference') or '?'}"
                    + (f" ({sib.get('bibcode')})" if sib.get('bibcode') else "")
                    + f" → {val}"
                )
                break
        merged_recommended.append(merged)
    recommended = merged_recommended

    # Star mean radius — required for AU → body-radius-multiplier conversion.
    star_radius_km = (star.get("principia") or {}).get("mean_radius_km")
    if star_radius_km is None:
        outcome.errors.append(
            f"{slug}: stars[0].principia.mean_radius_km is null — cannot convert "
            f"AU geometry to Kopernicus body-radius multipliers. Curate the "
            f"radius before re-running, or add a fallback for this star."
        )
        return None

    # Phase 3 visual decisions (tint + opacity). Phase 3 md filename uses
    # hyphens (eps-eri.md), DB uses underscores (eps_eri.json).
    md_slug = slug.replace("_", "-")
    md_path = PHASE3_DOCS_DIR / f"{md_slug}.md"
    decisions: dict[str, str] = {}
    if md_path.exists():
        decisions = extract_decisions(md_path.read_text(encoding="utf-8"))
    else:
        outcome.warnings.append(
            f"{slug}: docs/phase3/{md_slug}.md not found — using default tint + opacity"
        )

    tint = parse_hex_rgb(decisions.get("disk_tint_rgb_hex", "")) \
        or parse_hex_rgb(DEFAULT_DISK_TINT_HEX)
    opacity = parse_opacity(decisions.get("disk_opacity", "")) \
        or DEFAULT_DISK_OPACITY
    if "disk_tint_rgb_hex" not in decisions and md_path.exists():
        outcome.warnings.append(
            f"{slug}: no `disk_tint_rgb_hex` in Decisions — using default {DEFAULT_DISK_TINT_HEX}"
        )
    if "disk_opacity" not in decisions and md_path.exists():
        outcome.warnings.append(
            f"{slug}: no `disk_opacity` in Decisions — using default {DEFAULT_DISK_OPACITY}"
        )

    # Build DiskRing entries from recommended belts. Per-belt geometry
    # comes from the DB (not the Phase 3 markdown, which collapses multi-
    # belt info into a single overall-extent row).
    rings: list[DiskRing] = []
    for entry in recommended:
        inner = entry.get("inner_radius_au")
        outer = entry.get("outer_radius_au")
        # Width fallback: if only one is set, synthesize the other
        if inner is None and outer is None:
            outcome.warnings.append(
                f"{slug}: belt={entry.get('belt')} (ref={entry.get('reference')}) "
                f"has no inner_radius_au or outer_radius_au — skipping this belt"
            )
            continue
        if inner is None:
            inner = outer / NARROW_RING_WIDTH_FACTOR
            outcome.warnings.append(
                f"{slug}: belt={entry.get('belt')} (ref={entry.get('reference')}) "
                f"has no inner_radius_au — synthesizing as outer / {NARROW_RING_WIDTH_FACTOR} = {inner:.2f}"
            )
        if outer is None:
            outer = inner * NARROW_RING_WIDTH_FACTOR
            outcome.warnings.append(
                f"{slug}: belt={entry.get('belt')} (ref={entry.get('reference')}) "
                f"has no outer_radius_au — synthesizing as inner × {NARROW_RING_WIDTH_FACTOR} = {outer:.2f}"
            )

        rings.append(DiskRing(
            belt=entry.get("belt"),
            inner_au=float(inner),
            outer_au=float(outer),
            inclination_deg=float(entry.get("inclination_deg") or 0.0),
            reference=str(entry.get("reference") or "unknown"),
            bibcode=entry.get("bibcode"),
        ))

    if not rings:
        outcome.warnings.append(
            f"{slug}: all recommended belts lacked geometry — skipping disk emission"
        )
        outcome.skipped_no_disk.append(slug)
        return None

    body_name = star.get("kopernicus_body_name") \
        or normalize_body_name(star.get("name") or slug)

    return StarDisk(
        body_name=body_name,
        system_slug=slug,
        star_radius_km=float(star_radius_km),
        rings=rings,
        tint_rgb=tint,
        opacity=opacity,
    )


def load_planet_rings(slug: str, outcome: Outcome) -> list[PlanetRing]:
    """Read phase3/<slug>/kopernicus_extras.yaml if it exists.

    Only emits PlanetRing for entries with `ring_present: true`.
    """
    # The phase3 workspace dir uses underscores like the DB slug.
    extras_path = PHASE3_WORKSPACE_DIR / slug / "kopernicus_extras.yaml"
    if not extras_path.exists():
        return []

    with extras_path.open(encoding="utf-8") as f:
        extras = yaml.safe_load(f) or {}

    # Look up the DB planets list for body-name resolution + radius lookup.
    # Planets may carry a `kopernicus_body_name` override; radius is read from
    # `principia.mean_radius_km` (preferred) or `derived.radius_m` (fallback).
    db_path = DB_SYSTEMS_DIR / f"{slug}.json"
    planet_name_overrides: dict[str, str] = {}
    planet_radius_km: dict[str, float] = {}
    if db_path.exists():
        with db_path.open(encoding="utf-8") as f:
            data = json.load(f)
        for p in data.get("planets") or []:
            pname = p.get("name")
            if not pname:
                continue
            ko = p.get("kopernicus_body_name")
            if ko:
                planet_name_overrides[pname] = ko
            pr = (p.get("principia") or {}).get("mean_radius_km")
            if pr is None:
                rm = (p.get("derived") or {}).get("radius_m")
                if rm is not None:
                    pr = float(rm) / 1000.0
            if pr is not None:
                planet_radius_km[pname] = float(pr)

    rings: list[PlanetRing] = []
    for planet_key, fields in extras.items():
        if not isinstance(fields, dict):
            continue
        if not fields.get("ring_present"):
            continue
        inner = fields.get("ring_inner_au")
        outer = fields.get("ring_outer_au")
        if inner is None or outer is None:
            outcome.errors.append(
                f"{slug}/{planet_key}: ring_present=true but ring_inner_au/"
                f"ring_outer_au is missing (got inner={inner}, outer={outer})"
            )
            continue
        radius_km = planet_radius_km.get(planet_key)
        if radius_km is None:
            outcome.errors.append(
                f"{slug}/{planet_key}: ring_present=true but planet radius is "
                f"unavailable (no principia.mean_radius_km and no derived.radius_m "
                f"in db/systems/{slug}.json planets[] for name='{planet_key}'). "
                f"Cannot convert AU geometry to Kopernicus body-radius multipliers."
            )
            continue
        tint = parse_hex_rgb(fields.get("ring_color_hex") or DEFAULT_RING_TINT_HEX)
        opacity = float(fields.get("ring_opacity") or DEFAULT_RING_OPACITY)
        body_name = planet_name_overrides.get(planet_key) \
            or slug_to_kopernicus_name(planet_key)
        rings.append(PlanetRing(
            body_name=body_name,
            planet_key=planet_key,
            system_slug=slug,
            planet_radius_km=radius_km,
            inner_au=float(inner),
            outer_au=float(outer),
            tint_rgb=tint or (0.79, 0.71, 0.55),
            opacity=opacity,
        ))
    return rings


# ─────────────────────────────────────────────────────────────────────
# Rendering
# ─────────────────────────────────────────────────────────────────────

def render_ring_node(
    inner_multiplier: float,
    outer_multiplier: float,
    color_str: str,
    angle_deg: float,
    texture_path: str,
    comment: str | None = None,
) -> list[str]:
    """Render one `Ring` subnode at indent level 2 (8 spaces).

    innerRadius/outerRadius are body-radius multipliers per `gas-giant.md` §
    Rings and `mod-grounded-fields.md`. All standard default fields are
    emitted; callers supply only the geometry + color + texture.
    """
    lines = [
        "        Ring",
        "        {",
    ]
    if comment:
        lines.append(f"            // {comment}")
    lines += [
        f"            innerRadius = {inner_multiplier:.4f}",
        f"            outerRadius = {outer_multiplier:.4f}",
        f"            angle = {angle_deg:g}",
        "            longitudeOfAscendingNode = 0",
        f"            color = {color_str}",
        "            unlit = false",
        "            useNewShader = true",
        "            lockRotation = true",
        "            penumbraMultipler = 1000.0",
        "            albedoStrength = 1",
        "            scatteringStrength = 1",
        "            anisotropy = 0.9",
        "            fadeoutMinAlpha = 1",
        "            steps = 128",
        f"            texture = {texture_path}",
        "        }",
    ]
    return lines


def _texture_slug(belt: str | None) -> str:
    """Placeholder texture-path slug. Texture pipeline is deferred."""
    if not belt:
        return "_misc"
    return re.sub(r"[^A-Za-z0-9_]", "_", belt).strip("_") or "_misc"


def render_star_block(sd: StarDisk) -> str:
    """Emit `@Body[Star] { Rings { Ring … } }`.

    `Rings` is a direct child of `@Body`, sibling to `ScaledVersion` —
    NOT nested inside it. See `gas-giant.md` § Rings template.
    """
    color_str = fmt_color(sd.tint_rgb, sd.opacity)
    lines = [
        f"@Body[{sd.body_name}]",
        "{",
        f"    // -- Circumstellar disk Rings (emit_kopernicus_cfg.py v2 2026-05-27) --",
        f"    // source system: db/systems/{sd.system_slug}.json",
        f"    // star mean radius: {sd.star_radius_km:.1f} km (used for AU→multiplier conversion)",
        "    Rings",
        "    {",
    ]
    for r in sd.rings:
        inner_mult = (r.inner_au * AU_TO_KM) / sd.star_radius_km
        outer_mult = (r.outer_au * AU_TO_KM) / sd.star_radius_km
        bib = f" {r.bibcode}" if r.bibcode else ""
        belt_label = r.belt or "unnamed"
        comment = f"belt: {belt_label}, paper: {r.reference}{bib}"
        texture = f"NearStars-Textures/PluginData/{_texture_slug(r.belt)}/disk.dds"
        lines.extend(render_ring_node(
            inner_multiplier=inner_mult,
            outer_multiplier=outer_mult,
            color_str=color_str,
            angle_deg=r.inclination_deg,
            texture_path=texture,
            comment=comment,
        ))
    lines += [
        "    }",
        "}",
    ]
    return "\n".join(lines)


def render_planet_block(pr: PlanetRing) -> str:
    """Emit `@Body[Planet] { Rings { Ring … } }` for a Saturn-like planetary ring."""
    color_str = fmt_color(pr.tint_rgb, pr.opacity)
    inner_mult = (pr.inner_au * AU_TO_KM) / pr.planet_radius_km
    outer_mult = (pr.outer_au * AU_TO_KM) / pr.planet_radius_km
    lines = [
        f"@Body[{pr.body_name}]",
        "{",
        f"    // -- Planetary ring (emit_kopernicus_cfg.py v2 2026-05-27) --",
        f"    // source: phase3/{pr.system_slug}/kopernicus_extras.yaml ({pr.planet_key})",
        f"    // planet mean radius: {pr.planet_radius_km:.1f} km",
        "    Rings",
        "    {",
    ]
    lines.extend(render_ring_node(
        inner_multiplier=inner_mult,
        outer_multiplier=outer_mult,
        color_str=color_str,
        angle_deg=0.0,
        texture_path=f"NearStars-Textures/PluginData/{pr.body_name}/ring.dds",
        comment=None,
    ))
    lines += [
        "    }",
        "}",
    ]
    return "\n".join(lines)


def render_combined(star_disks: list[StarDisk], planet_rings: list[PlanetRing]) -> str:
    lines = [
        "// NearStars — Kopernicus disk + planetary ring patches",
        "// Generated by .claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py",
        "// Do not hand-edit; regenerate from db/systems/*.json + docs/phase3/*.md + phase3/<sys>/kopernicus_extras.yaml.",
        "",
        MM_HEADER,
        "{",
    ]
    # Emit star disks sorted by body name, then planet rings sorted by name
    for sd in sorted(star_disks, key=lambda x: x.body_name):
        lines.append(render_star_block(sd))
    for pr in sorted(planet_rings, key=lambda x: x.body_name):
        lines.append(render_planet_block(pr))
    lines += [
        "}",
        "",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# Static checks on the emitted cfg
# ─────────────────────────────────────────────────────────────────────

def static_check(cfg_text: str) -> list[str]:
    """Return a list of failure messages. Empty list = all checks passed."""
    failures: list[str] = []

    # 1. MM header present exactly once
    header_count = len(re.findall(r"@Kopernicus:FOR\[NearStarsSystem\]", cfg_text))
    if header_count != 1:
        failures.append(f"MM header @Kopernicus:FOR[NearStarsSystem] count = {header_count}, expected 1")

    # 2. Brace balance
    open_count = cfg_text.count("{")
    close_count = cfg_text.count("}")
    if open_count != close_count:
        failures.append(f"brace imbalance: {{ count = {open_count}, }} count = {close_count}")

    # 3. Each Ring subnode has innerRadius, outerRadius, color.
    # Find every "Ring { … }" block by scanning brace depth from each Ring header.
    for m in re.finditer(r"^\s*Ring\s*$", cfg_text, re.MULTILINE):
        # Walk forward to find the matching close brace
        start = m.end()
        # Skip whitespace + the opening brace
        rest = cfg_text[start:]
        brace_open = rest.find("{")
        if brace_open == -1:
            failures.append(f"Ring at offset {m.start()} has no opening brace")
            continue
        depth = 1
        idx = brace_open + 1
        while idx < len(rest) and depth > 0:
            ch = rest[idx]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            idx += 1
        ring_body = rest[brace_open + 1: idx - 1]
        for required in ("innerRadius", "outerRadius", "color", "angle"):
            if required not in ring_body:
                failures.append(
                    f"Ring at offset {m.start()} missing required field `{required}`"
                )
    return failures


# ─────────────────────────────────────────────────────────────────────
# Star-body rendering (v3): Properties + ScaledVersion{Light,Material,Coronas}
# ─────────────────────────────────────────────────────────────────────

def load_star_renders(slug: str, outcome: Outcome) -> list[StarRender]:
    """One StarRender per star in db/systems/<slug>.json.

    Mechanical values (radius, GM) come from `principia`; Teff/L/spectype from
    `raw`/`derived`. Missing Teff/L/rotation are warned + defaulted (so the body
    still emits). Missing radius/GM are hard errors (cannot render a star body)."""
    db_path = DB_SYSTEMS_DIR / f"{slug}.json"
    if not db_path.exists():
        outcome.errors.append(f"{slug}: db/systems/{slug}.json missing")
        return []
    with db_path.open(encoding="utf-8") as f:
        data = json.load(f)
    stars = data.get("stars") or []
    if not stars:
        outcome.errors.append(f"{slug}: no stars in DB file")
        return []

    out: list[StarRender] = []
    for star in stars:
        raw = star.get("raw") or {}
        derived = star.get("derived") or {}
        principia = star.get("principia") or {}
        body_name = star.get("kopernicus_body_name") \
            or normalize_body_name(star.get("name") or slug)
        display_name = star.get("name") or body_name

        radius_km = principia.get("mean_radius_km")
        gm_km3 = principia.get("gravitational_parameter_km3_s2")
        if radius_km is None or gm_km3 is None:
            # No mechanical values yet (uncurated star) — skip + warn, don't abort
            # the whole batch. Render the stars that DO have radius/GM.
            outcome.warnings.append(
                f"{slug}/{body_name}: principia.mean_radius_km or "
                f"gravitational_parameter_km3_s2 is null — skipped (no star body emitted)")
            continue

        teff = raw.get("teff_k")
        if teff is None:
            outcome.warnings.append(f"{slug}/{body_name}: no teff_k — defaulting to Sun (5772 K)")
            teff = star_fields.SOLAR_TEFF
        l_lsun = derived.get("luminosity_lsun")
        if l_lsun is None:
            outcome.warnings.append(f"{slug}/{body_name}: no derived.luminosity_lsun — defaulting to 1.0")
            l_lsun = 1.0
        rot_days = derived.get("rotation_period_days")
        if rot_days is None:
            outcome.warnings.append(f"{slug}/{body_name}: no rotation_period_days — defaulting to 25 d")
            rot_days = 25.0

        out.append(StarRender(
            body_name=body_name,
            display_name=display_name,
            radius_m=float(radius_km) * 1000.0,
            grav_parameter=float(gm_km3) * 1e9,   # km³/s² → m³/s²
            rotation_period_s=float(rot_days) * SECONDS_PER_DAY,
            teff_k=float(teff),
            luminosity_lsun=float(l_lsun),
            spectype=raw.get("spectype"),
        ))
    return out


def _kv_block(name: str, fields: dict[str, str], indent: str) -> str:
    inner = "\n".join(f"{indent}    {k} = {v}" for k, v in fields.items())
    return f"{indent}{name}\n{indent}{{\n{inner}\n{indent}}}"


def render_star_body_block(sr: StarRender) -> str:
    """A full `Body { … }` creation node (Template Sun + Properties + ScaledVersion)."""
    tex = f"NearStars-Textures/PluginData/{sr.body_name}/Kopernicus/{sr.body_name}"
    i = "        "  # Body node indent inside @Kopernicus { … }
    j = "                "  # ScaledVersion-child level (Light/Material/Coronas)

    light_fields = star_fields.light_block(sr.teff_k, sr.luminosity_lsun, sr.spectype)
    light_inner = "\n".join(f"{j}    {k} = {v}" for k, v in light_fields.items())
    curves = star_fields.intensity_curves_text(sr.luminosity_lsun, indent=j + "    ")
    light_node = f"{j}Light\n{j}{{\n{light_inner}\n{curves}\n{j}}}"
    material = star_fields.material_block(sr.teff_k, sr.spectype, f"{tex}_Sunspots.dds")

    properties = {
        "displayName": sr.display_name,
        "radius": f"{sr.radius_m:.6g}",
        "gravParameter": f"{sr.grav_parameter:.6g}",
        "rotates": "True",
        "rotationPeriod": f"{sr.rotation_period_s:.6g}",
        "tidallyLocked": "False",
        "albedo": "0",
        "emissivity": "0.99",
        "sphereOfInfluence": "Infinity",
        "useTheInName": "False",
        "selectable": "True",
        "RnDVisibility": "Visible",
    }

    # Corona: the grounded reference schema (star-body.md § Coronas) is texture +
    # mainTexScale only — no documented color field — so we do not invent one. The
    # corona's visible tint comes from the surrounding grounded base-hex Material
    # (emitColor/rimColor) and Light (sunLensFlareColor) it blends into.
    coronas = (
        f"{j}Coronas\n{j}{{\n"
        f"{j}    Value\n{j}    {{\n"
        f"{j}        scaleSpeed     = 0.007\n"
        f"{j}        scaleLimitY    = 5\n"
        f"{j}        scaleLimitX    = 5\n"
        f"{j}        updateInterval = 5\n"
        f"{j}        speed          = -1\n"
        f"{j}        rotation       = 0\n"
        f"{j}        Material\n{j}        {{\n"
        f"{j}            texture      = {tex}_Corona.dds\n"
        f"{j}            mainTexScale = 1,0.9\n"
        f"{j}        }}\n"
        f"{j}    }}\n"
        f"{j}}}"
    )

    return "\n".join([
        f"{i}Body",
        f"{i}{{",
        f"{i}    name = {sr.body_name}",
        f"{i}    identifier = NearStars/{sr.body_name}",
        f"{i}    cacheFile = {STAR_CACHE_FILE}",
        f"{i}    // flightGlobalsIndex: auto-assigned by Kopernicus (TODO: allocate per",
        f"{i}    // file-structure.md — 1000+, 100 indices per system).",
        f"{i}    Template",
        f"{i}    {{",
        f"{i}        name = Sun",
        f"{i}        removeAllPQSMods = True",
        f"{i}    }}",
        _kv_block("Properties", properties, i + "    "),
        f"{i}    Orbit",
        f"{i}    {{",
        f"{i}        // PLACEHOLDER — Principia initial_state overrides this in n-body mode.",
        f"{i}        // Real Kopernicus galactic placement is TODO (db/systems has no distance yet).",
        f"{i}        referenceBody = Sun",
        f"{i}        semiMajorAxis = {STAR_ORBIT_PLACEHOLDER_SMA_M:.6g}",
        f"{i}        eccentricity = 0",
        f"{i}        inclination = 0",
        f"{i}    }}",
        f"{i}    ScaledVersion",
        f"{i}    {{",
        f"{i}        type = Star",
        f"{i}        fadeStart = 0",
        f"{i}        fadeEnd = 0",
        light_node,
        _kv_block("Material", material, j),
        coronas,
        f"{i}    }}",
        f"{i}}}",
    ])


def render_stars_combined(star_renders: list[StarRender]) -> str:
    lines = [
        "// NearStars — Kopernicus star bodies (Properties + ScaledVersion render)",
        "// Generated by .claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py",
        "// Do not hand-edit; regenerate from db/systems/*.json.",
        "// Base star color: grounded stellar-photospheric-color methodology (docs/reference/",
        "//   stellar-photospheric-color-methodology.md) via scripts/refs/stellar_photospheric_color.py —",
        "//   FGK/WD→blackbody(Teff), M→Pickles real-SED tint, L/T/Y→blackbody (deep dim red).",
        "//   rim/sunspot/emit/ambient colors are rendering derivations of that one base hex.",
        "// luminosity = 1360 × L/Lsun (Sol convention).",
        "",
        MM_HEADER,
        "{",
    ]
    for sr in sorted(star_renders, key=lambda x: x.body_name):
        lines.append(render_star_body_block(sr))
    lines += ["}", ""]
    return "\n".join(lines)


def static_check_stars(cfg_text: str) -> list[str]:
    """Failure messages for the stars.cfg. Empty = pass."""
    failures: list[str] = []
    header_count = len(re.findall(r"@Kopernicus:FOR\[NearStarsSystem\]", cfg_text))
    if header_count != 1:
        failures.append(f"MM header count = {header_count}, expected 1")
    if cfg_text.count("{") != cfg_text.count("}"):
        failures.append(f"brace imbalance: {{={cfg_text.count('{')} }}={cfg_text.count('}')}")
    # every Body must carry the star essentials
    body_count = len(re.findall(r"^\s*Body\s*$", cfg_text, re.MULTILINE))
    for token in ("type = Star", "luminosity", "sunlightColor", "Coronas", "gravParameter"):
        if cfg_text.count(token) < body_count:
            failures.append(f"only {cfg_text.count(token)} `{token}` for {body_count} Body node(s)")
    return failures


# ─────────────────────────────────────────────────────────────────────
# Driver
# ─────────────────────────────────────────────────────────────────────

def _rel(p: Path) -> Path:
    """Path relative to the repo root for display; falls back to the path as-is
    when it lives outside the repo (e.g. a /tmp test output)."""
    return p.relative_to(REPO_ROOT) if REPO_ROOT in p.resolve().parents else p


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("system", nargs="*", help="System slugs to process; defaults to all")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print cfg to stdout instead of writing")
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                    help=f"disk+ring cfg path (default: {DEFAULT_OUTPUT.relative_to(REPO_ROOT)})")
    ap.add_argument("--stars-output", type=Path, default=DEFAULT_STARS_OUTPUT,
                    help=f"star-body cfg path (default: {DEFAULT_STARS_OUTPUT.relative_to(REPO_ROOT)})")
    args = ap.parse_args()

    try:
        slugs = args.system if args.system else discover_slugs()
    except EmitError as e:
        print(f"ABORT: {e}", file=sys.stderr)
        return 2

    outcome = Outcome()
    for slug in slugs:
        sd = load_star_disk(slug, outcome)
        if sd is not None:
            outcome.star_disks.append(sd)
        outcome.planet_rings.extend(load_planet_rings(slug, outcome))
        outcome.star_renders.extend(load_star_renders(slug, outcome))

    if outcome.errors:
        print(f"ABORT: {len(outcome.errors)} validation error(s):", file=sys.stderr)
        for e in outcome.errors:
            print(f"  - {e}", file=sys.stderr)
        return 2

    if not outcome.star_disks and not outcome.planet_rings and not outcome.star_renders:
        print("ABORT: nothing to emit (no disks/rings, no star bodies).", file=sys.stderr)
        return 2

    rings_text = (render_combined(outcome.star_disks, outcome.planet_rings)
                  if (outcome.star_disks or outcome.planet_rings) else None)
    stars_text = render_stars_combined(outcome.star_renders) if outcome.star_renders else None

    for label, text, check in (("disk-rings", rings_text, static_check),
                               ("stars", stars_text, static_check_stars)):
        if text is None:
            continue
        failures = check(text)
        if failures:
            print(f"ABORT: {len(failures)} static check failure(s) in {label}.cfg:", file=sys.stderr)
            for f in failures:
                print(f"  - {f}", file=sys.stderr)
            return 3

    if args.dry_run:
        if rings_text:
            sys.stdout.write(rings_text)
        if stars_text:
            sys.stdout.write(stars_text)
    else:
        if rings_text is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rings_text, encoding="utf-8")
            print(f"wrote {_rel(args.output)}")
            print(f"  disk star bodies: {len(outcome.star_disks)} "
                  f"({sum(len(sd.rings) for sd in outcome.star_disks)} belt rings total)")
            print(f"  planet rings:     {len(outcome.planet_rings)}")
        if stars_text is not None:
            args.stars_output.parent.mkdir(parents=True, exist_ok=True)
            args.stars_output.write_text(stars_text, encoding="utf-8")
            print(f"wrote {_rel(args.stars_output)}")
            print(f"  star bodies:      {len(outcome.star_renders)}")

    # Report
    if outcome.skipped_no_disk:
        print(f"\nskipped (no disk_measurements): {len(outcome.skipped_no_disk)} system(s)",
              file=sys.stderr)
        if len(outcome.skipped_no_disk) <= 25:
            for s in outcome.skipped_no_disk:
                print(f"  {s}", file=sys.stderr)
    if outcome.warnings:
        print(f"\nwarnings: {len(outcome.warnings)}", file=sys.stderr)
        for w in outcome.warnings:
            print(f"  {w}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
