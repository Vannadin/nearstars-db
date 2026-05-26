---
name: firefly-cfg
description: >
  Write and review Firefly atmospheric-effects .cfg files for KSP planet
  packs, especially NearStars. Use this skill when the user wants to
  create, modify, or debug a Firefly cfg — `ATMOFX_BODY`,
  `ATMOFX_PLANET_PACK`, `ATMOFX_PART`, `ATMOFX_PARTICLES`,
  `ATMOFX_SETTINGS` — or any time the user mentions reentry colors,
  plasma trails, atmospheric entry effects, the periodic table of plasma
  colors, thunderchild's chart, or asks "what color should this
  planet's reentry plasma be?". Also use when synthesizing Firefly cfg
  output from Phase 3 atmosphere composition / pressure / temperature.
  Grounded in `M1rageDev/Firefly` source (master, GPL-3.0) — every
  schema claim cites `ConfigManager.cs:line`.
mod_version: 1.0.6
---

# Firefly CFG Writing Guide

> **Scope.** Firefly is a KSP atmospheric-effects mod (re-entry plasma,
> trails, particles, bow shock). This skill covers the cfg authoring
> surface — five top-level node types, the HDR color value format, and
> the Phase 3 → Firefly cfg synthesis pipeline used by NearStars.
>
> NearStars-fixed conventions (MM directive, file layout) are pre-set;
> do not ask the user about them.

Source of truth:
- **Firefly source**: `M1rageDev/Firefly`
  (`Source/Firefly/ConfigManager.cs`, `SettingsManager.cs`, `Utils.cs`)
- **Shipped examples**: `GameData/Firefly/Configs/Default.cfg` plus
  `Stock/`, `RSS/`, `OPM/`, `KSRSS/`, `Kcalbeloh/`, `MPE/`.

If the mod version diverges from 1.0.6 (see frontmatter `mod_version`),
re-run the schema research pass before trusting outputs.

---

## 1. Five cfg node types

| Node | Purpose | Reference |
|---|---|---|
| `ATMOFX_BODY` | Per-celestial-body reentry config (colors + multipliers). The main authoring target. | [atmofx-body](references/atmofx-body.md) |
| `ATMOFX_PLANET_PACK` | Pack-level wrapper. Applies a strength multiplier across all bodies a pack ships. | [atmofx-planet-pack](references/atmofx-planet-pack.md) |
| `ATMOFX_PART` | Per-part color override (e.g., a specific heatshield). Color-only, no multipliers. | [atmofx-part](references/atmofx-part.md) |
| `ATMOFX_PARTICLES` | Particle system definitions (Sparks, Debris, Smoke). Mod-wide; not per-body. | [atmofx-particles](references/atmofx-particles.md) |
| `ATMOFX_SETTINGS` | Global mod toggles (HDR override, disable bowshock). User-side preference; don't ship. | [atmofx-settings](references/atmofx-settings.md) |

HDR color value format (used in every `Color { … }` block): [color-format](references/color-format.md).

Common authoring mistakes and fixes: [pitfalls](references/pitfalls.md).

---

## 2. NearStars-specific decisions

These values are fixed for this mod. Do not ask the user.

| Setting | Value |
|---|---|
| Pack node tag | `ATMOFX_PLANET_PACK:NEEDS[NearStarsSystem]` |
| Pack `name` | `NearStars` |
| Pack `strength_multiplier` | `1.0` (per-body multipliers do the system-wide tuning) |
| Pack `transition_offset` | `0.2` (matches Firefly's shipped RSS pack) |
| Body file layout | One `ATMOFX_BODY` per file, path `GameData/NearStarsSystem/Configs/Firefly/<Body>.cfg` |
| Per-body `name` | Must match the Kopernicus body name verbatim (no spaces, no dashes) |
| `config_version` | Always `5` |
| `ATMOFX_PART` / `ATMOFX_PARTICLES` / `ATMOFX_SETTINGS` | Do not ship from NearStars |

---

## 3. Phase 3 → Firefly cfg workflow

The skill ships a generic emitter: `scripts/emit_firefly_cfg.py`. Run
it from project root after Phase 3 syntheses are committed.

```bash
python3 .claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py
python3 .claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py --dry-run
python3 .claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py --slug trappist-1-e
```

Output: `dist/NearStars-Configs/Patches/Firefly/<KopernicusName>.cfg`
per atmospheric body plus `NearStarsPlanetPack.cfg` covering all of
them. The emitter is deterministic and idempotent — re-running on
unchanged inputs produces byte-identical output.

### What the emitter does

For each Phase 3 markdown (`docs/phase3/<slug>.md`):

1. **Gate.** Extract `atmosphere_present` from the Decisions table.
   Skip if false or pressure < 100 Pa (Mars-thin threshold).
2. **Pressure → multipliers.** Apply the piecewise table from
   [phase3-mapping](references/phase3-mapping.md) §3:
   - ≤ 0.01 bar → strength 0.5, fresnel 0
   - 0.01–0.5 bar → strength 0.7
   - 0.5–2 bar (Earth-like) → strength 1.0, fresnel 1 if ≥ 1 bar
   - 2–20 bar → strength 1.1
   - 20–50 bar → strength 1.2
   - 50+ bar → strength 1.3
3. **Composition → bulk-gas palette.** Match the dominant species
   against the palette set in [composition-color](references/composition-color.md)
   §3 (Earth-like / CO2 / Gas-giant / CH4 / Steam / Pure-H2).
4. **Secondary species → streak.** First 0.5–10% volume secondary that
   matches the streak palette ([composition-color §4](references/composition-color.md))
   or `db/refs/element_plasma_colors.yaml`. Falls back to
   `trail_primary` when no secondary matches.
5. **Temperature → particle_threshold.** Reads `equilibrium_temp_k`
   or `surface_temp_substellar_k`; > 300 K → 1500, else 1800.
6. **Emit `ATMOFX_BODY`** with all 9 Color keys filled, multipliers
   from steps 2–5, plus glow/glow_hot at Default values (material-
   driven, not gas-driven).
7. **Emit `NearStarsPlanetPack.cfg`** listing every body that got an
   `ATMOFX_BODY`.

### Element plasma colors

For trace-species streaks the emitter reads `db/refs/element_plasma_colors.yaml`
— a curated per-element hex DB replacing pixel-sampling of the
Helmenstine 2017 plasma chart. Companion human-readable view:
[`docs/reference/element-plasma-colors.md`](../../../docs/reference/element-plasma-colors.md).

To update an element's color: edit the YAML, run
`python3 scripts/refs/validate_element_colors.py`, then
`python3 scripts/refs/render_element_colors_doc.py` to refresh the
companion doc (en + ko mirror).

### When you do it manually (audit pass)

The full step-by-step manual procedure (parse Phase 3 by hand, apply
each lookup, validate Color block) is preserved in earlier versions of
this section for audit / cross-check purposes. If you need to verify
what the emitter is doing for a specific body, the procedure is:

1. Read `atmosphere_present`, `atmosphere_surface_pressure_pa`,
   `atmosphere_composition` from the Decisions table.
2. Apply the pressure piecewise from §3 above.
3. Pick the bulk palette from [composition-color §3](references/composition-color.md).
4. Pick the streak color from [composition-color §4](references/composition-color.md)
   or `db/refs/element_plasma_colors.yaml`.
5. Cross-check against the emitter output in
   `dist/NearStars-Configs/Patches/Firefly/<Body>.cfg`.

Discrepancy → bug in the emitter or the Decisions table; investigate
both.

**Do NOT** echo aurora_color_* into streaks. Aurora and reentry plasma
are different physical regimes (upper-atmosphere low-density
forbidden-line emission vs. lower-atmosphere shock-heated ionization).
Aurora feeds EVE/aurora mods, not Firefly.
- `name` matches the Kopernicus body name exactly.
- `config_version = 5`.
- If the body name is in `affected_bodies`, the pack tag has
  `:NEEDS[NearStarsSystem]`.

Common failure modes: [pitfalls](references/pitfalls.md).

---

## 4. Worked example reference

For a complete TRAPPIST-1 e walk-through (Phase 3 inputs → derived
fields → emitted cfg with rationale), see
[phase3-mapping](references/phase3-mapping.md) §7. The example covers
both the full-atmosphere case (e) and the airless edge case (b).

---

## 5. Reference index

| File | Covers |
|---|---|
| [atmofx-body](references/atmofx-body.md) | Per-body schema, all keys, defaults, validation checklist |
| [atmofx-planet-pack](references/atmofx-planet-pack.md) | Pack wrapper schema, MM directives |
| [atmofx-part](references/atmofx-part.md) | Per-part color override (NearStars rarely needs this) |
| [atmofx-particles](references/atmofx-particles.md) | Particle system definitions (mod-internal) |
| [atmofx-settings](references/atmofx-settings.md) | Global player toggles (don't ship) |
| [color-format](references/color-format.md) | HDR color string syntax — read before any `Color { … }` |
| [composition-color](references/composition-color.md) | Atmosphere composition → reentry color, verified against spectroscopy |
| [phase3-mapping](references/phase3-mapping.md) | Phase 3 row → Firefly field mapping with worked examples |
| [pitfalls](references/pitfalls.md) | Common parse / load / visual mistakes |

---

## 6. Versioning and refresh

If Firefly ships a new version (check `firefly-repo/CHANGELOG.md`
against the `mod_version` in this skill's frontmatter):

1. Re-clone Firefly: `git clone --depth 1 https://github.com/M1rageDev/Firefly.git`
2. Diff `ConfigManager.cs` and `SettingsManager.cs` against the version
   pinned in this skill.
3. Update references that reference changed fields.
4. Bump `mod_version` in the frontmatter.

The schema reference files cite specific `ConfigManager.cs:line`
locations — these are the canary for drift detection.

---

## Related

- [methodology](../../../docs/reference/methodology.md) — DB schema source (atmosphere composition, pressure feed into reentry palette)
- [mod-reference](../../../docs/reference/mod-reference.md) — Firefly dependency tier
- [mod-release-layout](../../../docs/reference/mod-release-layout.md) — Firefly patch placement
- entity pages: [trappist-1-e](../../../docs/phase3/trappist-1-e.md), [proxima-cen-b](../../../docs/phase3/proxima-cen-b.md) — atmosphere-bearing bodies whose Phase 3 outputs feed `ATMOFX_BODY` here
- [nearstars-phase3](../nearstars-phase3/SKILL.md) — upstream procedure that produces the atmosphere fields this skill consumes
