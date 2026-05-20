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

## 3. Sol-Based References

Read the relevant file for the body type being created. Each file contains a complete cfg block based on real Sol data, adapted to NearStars naming conventions.

| Body type | File | Covers |
|-----------|------|--------|
| Star | [references/star-body.md](references/star-body.md) | Light, Coronas, ScaledVersion Star Material |
| Rocky planet (vacuum or atmospheric) | [references/planet-body.md](references/planet-body.md) | Biomes, ScaledVersion, Atmospheric Gradient |
| Gas giant | [references/gas-giant.md](references/gas-giant.md) | Rings, AtmosphereFromGround, deformity=0 PQS |
| Orbit | [references/orbit.md](references/orbit.md) | Star/planet/moon orbit, cameraSmaRatioBounds |
| PQS terrain | [references/pqs-terrain.md](references/pqs-terrain.md) | VertexHeightMapBicubic, VertexColorMap, Parallax mod |
| Atmosphere | [references/atmosphere.md](references/atmosphere.md) | Pressure/temperature curves, thin atmosphere |
| Binary / multi-star system | [references/barycenter.md](references/barycenter.md) | Barycenter body, mass/SOI calculation, triple-system hierarchy |
| Ocean world | [references/ocean.md](references/ocean.md) | Ocean node, FallbackMaterial, HazardousOcean |
| Hazardous surface | [references/hazardous-body.md](references/hazardous-body.md) | AltitudeCurve, HeatMap, radiation belt |
