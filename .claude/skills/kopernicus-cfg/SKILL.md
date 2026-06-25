---
name: kopernicus-cfg
description: >
  Write and review Kopernicus .cfg files for KSP planet packs. Use this skill
  when the user wants to create, modify, or debug a Kopernicus config for a
  new star, planet, moon, gas giant, or ocean world — including requests like
  "add a planet", "write a cfg for X", "how do I configure Y in Kopernicus",
  or "generate a cfg from the DB". Grounded in Sol (RSS-Reborn/Sol-Configs)
  and ballisticfox/Kopernicus source. NearStars-specific decisions are
  pre-set; never ask the user about scale, Parallax, or mod name.
---

# Kopernicus CFG Writing Guide

> **Scope.** This skill is the **NearStars-specific Kopernicus cfg
> implementation** — which body templates to use, NearStars-fixed
> values (MM tag, texture paths, etc.), and skill-internal references
> for syntax (`references/nodes-quick-ref.md`, etc.).
>
> Project-level conventions that NearStars commits to (and that this
> skill must follow) live in the docs tree:
> - `docs/reference/mod-release-layout.md` §2 — cfg patterns
>   (`@Kopernicus:FOR[NearStarsSystem]`, identifier convention, file
>   separation per body)
> - `docs/reference/guideline.md` §7 — `flightGlobalsIndex` allocation
>   (1000+ for NearStars, 100 indices per system)
>
> When the docs and this skill drift, the docs are canonical. Open an
> issue and update the skill side.

Source repos:
- **Sol examples**: `RSS-Reborn/Sol-Configs` — `Sol-Configs/Configs/`
- **Kopernicus source**: `ballisticfox/Kopernicus` — `src/Kopernicus/Configuration/`

---

## 1. Kopernicus Syntax

Before writing any cfg, identify the body type — this determines which nodes are required:

| Type | Template | Required nodes |
|------|----------|----------------|
| Star | `Sun` | Properties, Orbit, ScaledVersion (type=Star, Light, Coronas) |
| Rocky — no atmosphere | `Mun` | Properties, Orbit, ScaledVersion (type=Vacuum), PQS |
| Rocky — with atmosphere | `Kerbin` | Properties, Orbit, ScaledVersion (type=Atmospheric), Atmosphere, PQS |
| Gas giant | `Mun` | Properties, Orbit, ScaledVersion (type=Atmospheric), Atmosphere, PQS (deformity=0) |
| Ocean world | `Kerbin` | Same as rocky+atmosphere, plus Ocean node |
| Moon | `Mun` | Same as rocky, referenceBody = parent planet name |

Node field tables for all nodes: [references/nodes-quick-ref.md](references/nodes-quick-ref.md)

Module Manager patch syntax (FOR, NEEDS, AFTER, operators): [references/module-manager.md](references/module-manager.md)

---

## 2. NearStars-Specific Decisions

These values are fixed for this mod. Do not ask the user about them.

| Setting | Value |
|---------|-------|
| MM patch header | `@Kopernicus:FOR[NearStarsSystem]` |
| Scale | Real scale (no reduction) |
| Parallax Continued | Always enabled |
| cacheFile | `ParallaxContinued/Models/ScaledMesh.bin` |
| Texture path prefix | `NearStars-Textures/PluginData/<BodyName>/Kopernicus/` |
| Blank normal map | `NearStars-Textures/PluginData/_Misc/Kopernicus/Blank_Normal.dds` |
| flightGlobalsIndex | 1000+, 100 indices per system — see file-structure.md |
| Orbit epoch | `epoch = 0` (KSP start ≈ JD2433647.5) |

### DB → cfg value mapping

When generating from `db/systems/<system>.json`:

**Star (from stars[]):**

| JSON field | cfg field | Conversion |
|-----------|-----------|------------|
| `principia.gravitational_parameter_km3_s2` | `Properties.gravParameter` | × 1e9 (km³/s² → m³/s²) |
| `principia.mean_radius_km` | `Properties.radius` | × 1000 (km → m) |

**Planet (from planets[].kopernicus):**

| JSON field | cfg field | Conversion |
|-----------|-----------|------------|
| `kopernicus.semi_major_axis_m` | `Orbit.semiMajorAxis` | direct |
| `kopernicus.eccentricity` | `Orbit.eccentricity` | direct |
| `kopernicus.inclination_deg` | `Orbit.inclination` | direct |
| `kopernicus.mean_anomaly_deg` | `Orbit.meanAnomalyAtEpochD` | direct |
| `kopernicus.longitude_of_ascending_node_deg` | `Orbit.longitudeOfAscendingNode` | direct |
| `kopernicus.argument_of_periapsis_deg` | `Orbit.argumentOfPeriapsis` | direct |
| `raw.mass_mearth` | `Properties.gravParameter` | × 3.986004418e14 (m³/s² per M⊕) |
| `raw.radius_rearth` | `Properties.radius` | × 6.371e6 (m per R⊕) |

If `kopernicus.semi_major_axis_m` is null, cfg generation is blocked — notify user and stop.

File structure and flightGlobalsIndex ranges: [references/file-structure.md](references/file-structure.md)

Common errors and fixes: [references/pitfalls.md](references/pitfalls.md)

---

## 3. Bulk emission

For repetitive cfg generation, use `scripts/emit_kopernicus_cfg.py` instead of hand-writing every body. The emitter reads `db/systems/<star>.json` + `docs/phase3/<slug>.md` and writes Module Manager patches.

**Current scope** (v1.1, 2026-05-27):

- Circumstellar disk Rings (star body) — reads `stars[0].raw.disk_measurements` (Phase 2, commit `641754b`), applies `disk_tint_rgb_hex` + `disk_opacity` from Phase 3 Decisions, converts AU → body-radius multipliers using `stars[0].principia.mean_radius_km`.
- Multi-paper geometry merge: when the `recommended: true` entry per belt has a null field, the emitter scans non-recommended same-belt entries to backfill. Recommended stays canonical for non-null fields.
- Planetary ring Rings (planet body) — same primitive; reads `phase3/<system>/kopernicus_extras.yaml` (sidecar yaml; not yet populated for any system).

**CLI.**

```bash
python3 .claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py [<system_slug>...] [--dry-run] [--output PATH]
```

No slugs → emit for every star with `disk_measurements`. Output combined into `dist/NearStars-Configs/Patches/Kopernicus/disk-rings.cfg` (gitignored).

**Static checks the emitter runs on its own output:** Module Manager `@Kopernicus:FOR[NearStarsSystem]` header present, brace balance, every Ring has `innerRadius` `outerRadius` `color` `angle`.

**Out of scope** (manual §1–§2 procedure still applies):

- Full Properties block (gravParameter, mean radius, displayName, description)
- Orbit block
- PQS terrain
- Atmosphere
- Star body Light / Coronas / GalacticOrbit
- `flightGlobalsIndex` per-system allocation

For these, hand-write per the templates in §4 (Sol-Based References) below or wait for the v2 emitter expansion.

**Open issues v2 → v3:**

- Tau Ceti `stars[0].principia.mean_radius_km` is null; emitter errors out. Needs Phase 1 curation pass before emission.
- Fomalhaut `inner_warm` (Gáspár 2023) has null geometry with no sibling entries to backfill. Manual override needed (extension of `kopernicus_extras.yaml` to stellar disks).
- 1.2× outer-radius fallback for narrow rings (Vega warm, ε Eri belts) — sensible visual placeholder but not measurement-grounded.
- Texture pipeline: emitter writes placeholder paths under `NearStars-Textures/PluginData/<belt>/disk.dds`; assets do not yet exist.

---

## 4. Sol-Based References

Read the relevant file for the body type being created. Each file contains a complete cfg block based on real Sol data, adapted to NearStars naming conventions.

| Body type | File | Covers |
|-----------|------|--------|
| Star | [references/star-body.md](references/star-body.md) | Light, Coronas, ScaledVersion Star Material |
| Rocky planet (vacuum or atmospheric) | [references/planet-body.md](references/planet-body.md) | Biomes, ScaledVersion, Atmospheric Gradient |
| Gas giant | [references/gas-giant.md](references/gas-giant.md) | Rings, AtmosphereFromGround, deformity=0 PQS |
| Orbit | [references/orbit.md](references/orbit.md) | Star/planet/moon orbit, cameraSmaRatioBounds |
| PQS terrain | [references/pqs-terrain.md](references/pqs-terrain.md) | VertexHeightMapBicubic, VertexColorMap, Parallax mod |
| Oblate / triaxial figure | [references/oblate-figure.md](references/oblate-figure.md) | VertexHeightOblateAdvanced — visual J2/C22 ellipsoid |
| Atmosphere | [references/atmosphere.md](references/atmosphere.md) | Pressure/temperature curves, thin atmosphere |
| Binary / multi-star system | [references/barycenter.md](references/barycenter.md) | Barycenter body, mass/SOI calculation, triple-system hierarchy |
| Ocean world | [references/ocean.md](references/ocean.md) | Ocean node, FallbackMaterial, HazardousOcean |
| Hazardous surface | [references/hazardous-body.md](references/hazardous-body.md) | AltitudeCurve, HeatMap, radiation belt |

---

## Related

- [methodology](../../../docs/reference/methodology.md) — DB schema that feeds Kopernicus values (radius, mass → gravParameter, etc.)
- [mod-release-layout](../../../docs/reference/mod-release-layout.md) — §2 cfg conventions this skill follows (`@Kopernicus:FOR[NearStarsSystem]`, file separation, identifier convention)
- [guideline](../../../docs/reference/guideline.md) — §7 flightGlobalsIndex allocation policy
- [mod-reference](../../../docs/reference/mod-reference.md) — Kopernicus dependency tier
- [principia-cfg-reference](../../../docs/reference/principia-cfg-reference.md) — paired downstream consumer (Principia + Kopernicus together)
- entity pages in `docs/phase3/*` — input data this skill consumes
