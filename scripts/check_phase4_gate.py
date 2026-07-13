#!/usr/bin/env python3
# Phase 4 결정 보드 emit-게이트 검증 — 고증 게이트(pass-in-window / documented-divergence)와
# 스키마 v2 정합성을 강제해 비정규 값이 cfg emit까지 조용히 새는 것을 막는다.
"""Validate phase4/*.yaml decision boards.

schema_version: 2  -> STRICT. Hard-fails on enum / gate / divergence violations.
legacy (no v2)     -> SOFT. Only prints a one-line non-conformance summary; never fails.

This lets boards migrate to v2 one file at a time without turning check.sh red.

Hard fails (v2 only):
  - board has no `decisions:` list (catches the key-typo silent-pass bypass)
  - decision row is not a mapping, or lacks body/axis/status
  - status not in the lifecycle enum
  - axis group not in the §0 menu
  - two non-superseded rows share the same (body, axis)
  - fields[] entry is not a mapping, or lacks a name/value, or has an off-enum op
  - refs is not a list of strings
  - colors map value is not a #RRGGBB hex
  - gated/emitted row: missing gate, or verdict not in {pass-in-window, documented-divergence}
  - a documented-divergence (row- or field-level) with a null/empty divergence_note
  - passthrough row that carries a gate block
  - SPEC §3.2 bulk template STRUCTURE: a real body with live rows but no bulk anchor
    row, an anchor without a valid body_class, a field with neither value nor na_reason

Warnings (v2, non-fatal): missing evidence, no machine-readable value on a gated row,
  no refs on a gated row, a field name outside the §0 axis menu, empty decisions list,
  a §3.2 template slot not yet covered (open work, per-decision philosophy),
  c22 on a star, gravity drifting >2% from the row's own GM/R².

`schema_version` is normalized (2 / 2.0 / "2" all mean v2) so a quoting slip cannot
silently downgrade a strict board to the legacy soft path.
"""
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
BOARDS = sorted((REPO / "phase4").glob("*.yaml"))

AXIS_GROUPS = {
    "identity", "orbit", "bulk", "atmosphere", "surface", "appearance",
    "magnetism", "environment", "rings", "satellites", "gameplay",
}
# §0 axis names per group (for soft name validation).
AXIS_NAMES = {
    "identity": {"body_type", "spectral_class", "designation", "cultural_name", "discoverability"},
    "orbit": {"semi_major_axis_au", "eccentricity", "inclination_deg", "longitude_ascending_node",
              "argument_periapsis", "mean_anomaly", "epoch", "spin_orbit_resonance",
              "tidal_lock", "lagrange_placement"},
    "bulk": {"mass", "radius", "gravity", "geopotential_j2", "reference_radius",
             "flattening", "geopotential_c22", "j4", "rotation_period", "obliquity",
             "spin_axis_orientation", "internal_heat", "intrinsic_luminosity", "age",
             "cooling_age", "tidal_heating", "tidal_surface_flux"},
    "atmosphere": {"composition", "pressure", "temperature", "scale_height",
                   "breathability", "oxygen", "greenhouse", "escape", "loss"},
    "surface": {"surface_type", "hydrosphere", "ocean", "ice_caps", "glaciation",
                "tectonics", "volcanism", "terrain", "surface_temperature", "albedo", "biosphere"},
    "appearance": {"banding", "base_colour", "base_color", "clouds", "haze", "aurora",
                   "rings", "surface", "emission_glow", "specular", "artificial",
                   "city_lights", "granulation", "limb_darkening", "spots_faculae",
                   "corona", "flares", "beam", "color", "colour"},
    "magnetism": {"magnetic_field", "magnetosphere", "radiation_belts"},
    "environment": {"radiation", "stellar_wind", "activity", "heliosphere", "flares",
                    "space_weather", "uv_xray_flux", "habitable_zone"},
    "rings": {"ring_structure", "ring_composition", "ring_color", "ring_colour",
              "ring_opacity", "ring_plane", "circumstellar_disk", "debris_belt", "asteroid_belt"},
    "satellites": {"co_orbitals", "trojans", "dust_sources"},
    "gameplay": {"sphere_of_influence_tuning", "science_biomes", "timewarp_limits", "difficulty"},
}
STATUS = {"passthrough", "open", "art-directed", "gated", "emitted", "superseded"}
VERDICT = {"pass-in-window", "documented-divergence"}
FIELD_OPS = {"set", "scale", "passthrough"}
HEX_RE = re.compile(r"^#[0-9a-fA-F]{6}$")

# SPEC §3.2 — bulk template convention. A slot is satisfied by an anchor-row field
# OR a live dedicated `bulk.<name>` row (union rule); alternates count for their slot.
BODY_CLASSES = {"star", "tidally_locked", "free_rotator"}
BULK_CORE = {"mass", "radius", "gravity", "rotation_period", "spin_axis_orientation",
             "geopotential_j2", "reference_radius", "flattening", "age"}
BULK_TEMPLATE = {
    "star": BULK_CORE,
    "tidally_locked": BULK_CORE | {"obliquity", "geopotential_c22", "internal_heat"},
    "free_rotator": BULK_CORE | {"obliquity", "geopotential_c22", "internal_heat"},
}
BULK_SLOT_ALTERNATES = {"age": {"cooling_age"}, "internal_heat": {"intrinsic_luminosity"}}


def nonempty(v):
    return v is not None and str(v).strip() != "" and str(v).strip().lower() != "null"


def is_v2(doc):
    """2 / 2.0 / "2" all count — a quoting slip must not downgrade a strict board."""
    return str(doc.get("schema_version", "")).strip() in {"2", "2.0"}


def check_fields(loc, fields, fails):
    """SPEC §3.1 typed-field shape: every entry is a mapping with a name and a value
    (an emit number living only in prose is exactly what the gate exists to prevent)."""
    for f in fields:
        if not isinstance(f, dict):
            fails.append(f"{loc}: fields[] entry is not a mapping: {f!r}")
            continue
        if not nonempty(f.get("name")):
            fails.append(f"{loc}: fields[] entry has no name")
        if not nonempty(f.get("value")):
            # SPEC §3.2: an n/a slot stays present as value: null + na_reason.
            if not nonempty(f.get("na_reason")):
                fails.append(f"{loc}: field '{f.get('name')}' has no value and no na_reason "
                             "(prose-only numbers are illegal; n/a slots need na_reason)")
        op = f.get("op")
        if op is not None and op not in FIELD_OPS:
            fails.append(f"{loc}: field '{f.get('name')}' op '{op}' not in {sorted(FIELD_OPS)}")
        colors = f.get("colors")
        if colors is not None:
            if not isinstance(colors, dict):
                fails.append(f"{loc}: field '{f.get('name')}' colors is not a mapping")
            else:
                for cname, chex in colors.items():
                    if not isinstance(chex, str) or not HEX_RE.match(chex.strip()):
                        fails.append(f"{loc}: colors['{cname}'] = {chex!r} is not #RRGGBB")


def check_v2(path, doc):
    fails, warns = [], []
    if not isinstance(doc.get("decisions"), list):
        fails.append(f"{path.name}: no 'decisions:' list at top level "
                     "(missing or misspelled key would silently skip every row)")
        return fails, warns
    rows = doc["decisions"]
    if not rows:
        warns.append(f"{path.name}: decisions list is empty")
    seen_axes = {}
    bodies_with_rows = set()   # real bodies (not `*`) that have any live row
    bulk_anchors = {}          # body -> live `axis: bulk` anchor row
    bulk_named = {}            # body -> {name} from live dedicated bulk.<name> rows
    for i, row in enumerate(rows):
        loc = f"{path.name} decisions[{i}]"
        if not isinstance(row, dict):
            fails.append(f"{loc}: row is not a mapping")
            continue
        body = row.get("body", "?")
        axis = row.get("axis")
        status = row.get("status")
        loc = f"{path.name} [{body} / {axis}]"

        for req in ("body", "axis", "status"):
            if not nonempty(row.get(req)):
                fails.append(f"{loc}: missing required field '{req}'")
        if not axis:
            continue

        group = str(axis).split(".", 1)[0]
        name = str(axis).split(".", 1)[1] if "." in str(axis) else None
        if group not in AXIS_GROUPS:
            fails.append(f"{loc}: axis group '{group}' not in the §0 menu")
        if name and name not in AXIS_NAMES.get(group, set()):
            warns.append(f"{loc}: axis name '{name}' not in the §0 menu for '{group}'")

        if status not in STATUS:
            fails.append(f"{loc}: status '{status}' not in {sorted(STATUS)}")

        # one live decision per (body, axis); replaced rows must be `superseded`
        if status != "superseded":
            key = (str(body), str(axis))
            if key in seen_axes:
                fails.append(f"{loc}: duplicate live row for this (body, axis) — "
                             f"also decisions[{seen_axes[key]}]; supersede one of them")
            else:
                seen_axes[key] = i
            # SPEC §3.2 bookkeeping (skip the `*` / system-wide wildcard)
            if str(body).strip("* ").strip():
                b = str(body)
                bodies_with_rows.add(b)
                if group == "bulk":
                    if name is None:
                        bulk_anchors[b] = row
                    else:
                        # a dedicated row satisfies its own axis name AND the field
                        # names it carries (e.g. reference_radius inside a J2 row)
                        s = bulk_named.setdefault(b, set())
                        s.add(name)
                        s.update(f.get("name") for f in row.get("fields") or []
                                 if isinstance(f, dict) and f.get("name"))

        gate = row.get("gate")
        fields = row.get("fields") or []
        if not isinstance(fields, list):
            fails.append(f"{loc}: fields is not a list")
            fields = []
        check_fields(loc, fields, fails)

        refs = row.get("refs")
        if refs is not None and (not isinstance(refs, list)
                                 or any(not isinstance(r, str) for r in refs)):
            fails.append(f"{loc}: refs must be a list of strings, got {refs!r}")

        if status == "passthrough" and gate:
            fails.append(f"{loc}: passthrough row carries a gate block (must have none)")

        if status in ("gated", "emitted"):
            if not isinstance(gate, dict):
                fails.append(f"{loc}: {status} row has no gate block")
                continue
            verdict = gate.get("verdict")
            if verdict not in VERDICT:
                fails.append(f"{loc}: gate.verdict '{verdict}' not in {sorted(VERDICT)}")
            if not nonempty(gate.get("evidence")):
                warns.append(f"{loc}: gate.evidence is empty")

            # divergence_note required wherever a divergence verdict is declared.
            row_div = verdict == "documented-divergence"
            if row_div and not nonempty(gate.get("divergence_note")):
                fails.append(f"{loc}: documented-divergence (row) with null divergence_note")
            for f in fields:
                if isinstance(f, dict) and f.get("verdict") == "documented-divergence" \
                        and not nonempty(f.get("divergence_note")):
                    fails.append(f"{loc}: field '{f.get('name')}' documented-divergence "
                                 f"with null divergence_note")

            # machine-readable value present?
            has_value = nonempty(row.get("value")) or bool(fields) \
                or bool(row.get("discoverability_cfg")) or nonempty(gate.get("value"))
            if not has_value:
                warns.append(f"{loc}: gated row has no machine-readable value/fields")
            if not row.get("refs"):
                warns.append(f"{loc}: gated row has no refs[]")

    # ── SPEC §3.2: bulk template convention ──────────────────────────────
    for b in sorted(bodies_with_rows):
        loc = f"{path.name} [{b} / bulk]"
        anchor = bulk_anchors.get(b)
        if anchor is None:
            fails.append(f"{loc}: no live bulk anchor row for this body (SPEC §3.2)")
            continue
        bc = anchor.get("body_class")
        if bc not in BODY_CLASSES:
            fails.append(f"{loc}: bulk anchor body_class '{bc}' not in {sorted(BODY_CLASSES)}")
            continue
        have = {f.get("name") for f in anchor.get("fields") or [] if isinstance(f, dict)}
        have |= bulk_named.get(b, set())
        # Coverage gaps are open work, not schema violations — Phase 4 is
        # per-decision, so an un-walked slot warns (visibly) instead of failing.
        for slot in sorted(BULK_TEMPLATE[bc]):
            if slot in have or (BULK_SLOT_ALTERNATES.get(slot, set()) & have):
                continue
            warns.append(f"{loc}: template slot '{slot}' not yet covered for class '{bc}' "
                         "(fill with a decision, or value: null + na_reason)")
        if bc == "star" and "geopotential_c22" in have:
            warns.append(f"{loc}: geopotential_c22 on a star (physically n/a for this class)")
        _gravity_guard(loc, anchor, warns)
    return fails, warns


G_SI = 6.674e-11
STD_G = 9.80665


def _num(v):
    try:
        return float(str(v).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def _gravity_guard(loc, anchor, warns):
    """SPEC §3.2: gravity is a derived echo of GM/R² — warn when it drifts >2%
    from the anchor row's own mass/radius. Best-effort: only fires when all three
    fields parse in known units (kg, km/m, g / m/s²)."""
    vals = {}
    for f in anchor.get("fields") or []:
        if isinstance(f, dict) and f.get("name") in ("mass", "radius", "gravity"):
            vals[f["name"]] = (_num(f.get("value")), str(f.get("unit") or "").strip())
    if not all(k in vals and vals[k][0] for k in ("mass", "radius", "gravity")):
        return
    m, mu = vals["mass"]
    r, ru = vals["radius"]
    g, gu = vals["gravity"]
    if mu != "kg":
        return
    if ru == "km":
        r *= 1000.0
    elif ru != "m":
        return
    if gu == "g":
        g *= STD_G
    elif gu not in ("m/s2", "m/s^2", "m/s²"):
        return
    g_calc = G_SI * m / r ** 2
    if abs(g_calc / g - 1.0) > 0.02:
        warns.append(f"{loc}: gravity {g:.3f} m/s² drifts from GM/R² = {g_calc:.3f} m/s² "
                     "(>2%) — re-derive from the row's mass/radius")


def summarize_legacy(path, doc):
    """One-line non-conformance count for un-migrated boards."""
    rows = doc.get("decisions") or []
    group_only = sum(1 for r in rows if isinstance(r, dict)
                     and r.get("axis") and "." not in str(r["axis"]))
    bad_status = sum(1 for r in rows if isinstance(r, dict)
                     and r.get("status") not in STATUS)
    return f"{len(rows)} rows · {group_only} group-only axis · {bad_status} off-enum status"


def main():
    any_fail = False
    print("── Phase 4 emit-gate (schema v2 strict / legacy soft) ──")
    for path in BOARDS:
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as e:
            print(f"  [FAIL] {path.name}: YAML parse error: {e}")
            any_fail = True
            continue

        if is_v2(doc):
            try:
                fails, warns = check_v2(path, doc)
            except Exception as e:  # isolate a crash to this board; keep checking the rest
                print(f"  [FAIL] {path.name}: validator crashed: {type(e).__name__}: {e}")
                any_fail = True
                continue
            if fails:
                any_fail = True
                print(f"  [FAIL] {path.name} (v2): {len(fails)} error(s), {len(warns)} warning(s)")
                for m in fails:
                    print(f"      ✗ {m}")
                for m in warns:
                    print(f"      · {m}")
            else:
                print(f"  [PASS] {path.name} (v2): 0 errors, {len(warns)} warning(s)")
                for m in warns:
                    print(f"      · {m}")
        else:
            print(f"  [warn] {path.name} (legacy v1, soft): {summarize_legacy(path, doc)}")

    print("  [PASS] Phase 4 emit-gate" if not any_fail else "  [FAIL] Phase 4 emit-gate")
    return 1 if any_fail else 0


if __name__ == "__main__":
    sys.exit(main())
