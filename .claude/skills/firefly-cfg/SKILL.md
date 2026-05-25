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

When generating from a Phase 3 host directory (e.g.,
`docs/phase3/trappist-1-e.md`):

### Step 0 — Confirm Firefly cfg is appropriate

Skip Firefly cfg entirely if:
- `atmosphere_present = false` → no `ATMOFX_BODY` written.
- `atmosphere_pressure_pa < 100 Pa` → atmosphere is below the visible-effect threshold; skip unless Phase 3 explicitly marks "thin reentry plasma desired".

### Step 1 — Read Phase 3 inputs

Required fields from the Phase 3 Decisions table:
- `atmosphere_present`
- `atmosphere_pressure_pa`
- `atmosphere_composition_volume_pct` (dominant species + traces)
- `atmosphere_temperature_K_surface` (optional but informs particle threshold)
- `body_kopernicus_name`
- `aurora_color_primary_hex` (optional; used for streak echo)

If Phase 3 declares any of the optional `atmofx_*_hex_intensity`
override fields (see [phase3-mapping](references/phase3-mapping.md) §2),
prefer them over the composition-derived defaults.

### Step 2 — Derive multipliers from pressure

Use the table in [phase3-mapping](references/phase3-mapping.md) §3:

```
pressure_bar           strength    wrap_fresnel
≤ 0.01                 0.5         0
0.01 – 0.5             0.6–0.8     0
0.5 – 2 (Earth-like)   1.0         0 (clear) / 1 (hazy)
2 – 20                 1.0–1.2     1
50+                    1.0–1.5     1
gas giant outer        1.0         1
```

### Step 3 — Pick colors from composition (two layers)

**Bulk gas (>50% volume)** → trail_primary, trail_secondary,
trail_tertiary, wrap_layer, shockwave. Pick a row from
[composition-color](references/composition-color.md) §3:

- N2 + O2 → Earth-like palette (warm trail, blue-violet shockwave).
- CO2 → Mars/Venus palette (blue trail, green shockwave).
- H2 + He → physics pink-yellow OR stylized deep blue (see §5 stock case study).
- CH4, H2O, pure-H2 → specialty rows.

**Secondary species (0.5–10% volume)** → trail_streak, wrap_streak.
Pick a row from [composition-color](references/composition-color.md) §4
(secondary-species table). Examples: CO2 1–10% in N2 → green streak;
He in H2 → yellow streak; SO2 trace in CO2 → pale blue-green streak.

If atmosphere has no significant secondary, streak = `trail_primary`
(default fallback, no separate streak chemistry).

**Do NOT** echo aurora_color_* into streaks. Aurora and reentry plasma
are different physical regimes (upper-atmosphere low-density
forbidden-line emission vs. lower-atmosphere shock-heated ionization).
Aurora feeds EVE/aurora mods, not Firefly.

### Step 4 — Default `glow` / `glow_hot`

These are hull-surface heating, not gas-specific. Use the shipped
Default values unless the user explicitly overrides:

```
glow     = 191 80 50 1.4
glow_hot = 191 90 65 2.5
```

### Step 5 — Set particle / streak fields

| Field | Default | Override when |
|---|---|---|
| `particle_threshold` | 1800 | Hot atmosphere (T > 300 K) → 1500. Lava world → 1200. |
| `streak_probability` | 0.07 if atmosphere, else 0 | Phase 3 says "no streaks" |
| `streak_threshold` | 0 | Empirically tuned; -0.5 to 0 typical |

### Step 6 — Emit `ATMOFX_BODY`

Concatenate the values into the schema in
[atmofx-body](references/atmofx-body.md) skeleton. Verify with the
checklist in that file before saving.

### Step 7 — Emit / update `ATMOFX_PLANET_PACK`

NearStars ships one pack covering every atmosphere-bearing body. The
pack's `affected_bodies` list grows as bodies are added. Do not ship
a per-body pack node — one pack only.

### Step 8 — Validate

- Every color in `Color { … }` is `R G B intensity` (4 space-separated
  tokens). Run a regex check.
- Every multiplier is a bare float (no `f` suffix, no comma).
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
