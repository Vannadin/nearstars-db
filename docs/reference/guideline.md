# Nearby Star Systems KSP Mod — Project Guideline

**Goal:** Add nearby star systems to KSP 1.12.x following Sol ecosystem conventions, with compatibility for both Sol and RSS.

---

## 1. Project Overview

| Item | Detail |
|------|--------|
| Mod name | NearStars |
| KSP version | 1.12.x |
| License | CC-BY-NC-SA-4.0 (matching Sol) |
| Type | Dual-compatible addon — works with Sol **or** RSS; primary conventions follow Sol |

The mod adds new star systems; it does not touch or replace existing bodies in either Sol or RSS. Either Sol-Configs or RealSolarSystem satisfies the dependency — not both at once.

---

## 2. Dependencies

**One of the following (mutually exclusive):**

| Solar system mod | Tag used |
|-----------------|----------|
| Sol-Configs | `FOR[SolSystem]` |
| RealSolarSystem | `FOR[RSSConfig]` |

**Always required:**

| Mod | Role |
|-----|------|
| Kopernicus (ballisticfox fork) | Body definition framework |
| Module Manager | Conditional patching (`NEEDS[]`) |
| Parallax Continued | Terrain shaders and scatters |
| EVE Volumetrics V5 | Cloud layers (atmospheric bodies only) |
| BurstPQS | Terrain generation optimization |

Note: RSS-Origin v1.x does not support Sol. v2 with Sol support is in development but unreleased. This mod must solve the dual-compatibility problem independently.

---

## 3. Target Star Systems

### 3.1 Distance limits

| Engine | Max range | Source |
|--------|-----------|--------|
| Kopernicus (rendering + SOI) | ~50 ly | REX developer |
| Principia (gravitational perturber) | ~80 ly | RSS-Origin developer |

Kopernicus bodies beyond ~50 ly risk map-view failures, floating-point glitches in the renderer, or engine crashes. This is a hard constraint — all Kopernicus bodies must be within 50 ly.

Principia registers stars as gravitational perturbers through a separate mechanism that is not subject to KSP's rendering limits. Stars in the 50–80 ly range are therefore candidates for **Principia-only entries** (no Kopernicus body, no visual presence, gravity effect only).

### 3.2 Scope

The current data pipeline covers all confirmed planetary systems and noteworthy stellar systems within 50 ly — 136 systems / 144 stellar components as of 2026-05-18. This fully covers the Kopernicus range. A separate Principia-only pass for the 50–80 ly band can be added later if desired.

### 3.3 Development order

**Build one complete system first, then expand.** The first system serves as the template and reference implementation for all subsequent systems. Do not start a second system until the first is fully playable (Phase 1 + Phase 2 complete for that system).

Final system list and selection order are TBD — candidates include Proxima Centauri (nearest, single-star, 2 planets), Barnard's Star (5.96 ly), Alpha Centauri (famous, but triple system complexity), and others.

---

## 4. Repository Structure

Mirrors Sol-Configs layout. The `Patches/` folder is expanded to hold per-mod compatibility configs.

```
NearStars/
├── NearStars-Configs/
│   ├── Configs/
│   │   ├── 00_NearStars-Localization.cfg
│   │   ├── 01_[SystemName]/
│   │   │   ├── 01_[StarName]/
│   │   │   │   ├── [Star]-Kopernicus.cfg
│   │   │   │   ├── [Star]-Localization.cfg
│   │   │   │   └── [Star]-ScienceDefs.cfg
│   │   │   └── 01-01_[PlanetName]/
│   │   │       ├── [Planet]-Kopernicus.cfg
│   │   │       ├── [Planet]-Localization.cfg
│   │   │       ├── [Planet]-ScienceDefs.cfg
│   │   │       ├── [Planet]-ParallaxTerrain.cfg
│   │   │       └── [Planet]-ParallaxScatters.cfg
│   │   └── 02_[SystemName]/
│   │       └── ...
│   ├── Patches/
│   │   ├── Sol/                   // Sol-specific overrides (NEEDS[SolSystem])
│   │   └── RSS/                   // RSS-specific overrides (NEEDS[RSSConfig])
│   ├── Rescale/
│   │   ├── NearStars-Rescale-Quarter.cfg   // Sol quarter scale
│   │   ├── NearStars-Rescale-Stock.cfg     // Sol stock scale
│   │   └── NearStars-Rescale-RSS.cfg       // RSS 1:1 real scale
│   ├── NearStars-Configuration.cfg
│   ├── NearStars-KopernicusSettings.cfg
│   └── Credits-License.md
└── NearStars-Textures/
    └── PluginData/
        └── 01_[SystemName]/
            └── 01_[BodyName]/
                └── Kopernicus/
                    ├── [Body]_Icon.png
                    ├── [Body]_VertexHeight.dds
                    ├── [Body]_VertexColor.dds
                    └── [Body]_Biomes.dds
```

---

## 5. Config Conventions

### 5.1 Patch tags and dual-compatibility strategy

Both RSS and Sol define their central star as `name = Sun`, so `referenceBody = Sun` works in both without modification. The compatibility split happens in two places only:

**A. The main body definition** — uses a neutral tag, loads regardless of which solar system mod is installed:

```cfg
@Kopernicus:FOR[NearStarsSystem]
{
    Body
    {
        name = StarName
        referenceBody = Sun     // valid in both Sol and RSS
        ...
    }
}
```

**B. Mod-specific patches** — placed in `Patches/Sol/` or `Patches/RSS/`, loaded conditionally:

```cfg
// Patches/Sol/StarName-EVE.cfg  — only loads when Sol is installed
@EVE_CLOUDS:NEEDS[SolSystem]:FOR[NearStarsSystem]
{
    ...
}

// Patches/RSS/StarName-EVE.cfg  — only loads when RSS is installed
@EVE_CLOUDS:NEEDS[RSSConfig]:FOR[NearStarsSystem]
{
    ...
}
```

**What goes in patches vs. main config:**

| Aspect | Main config | Sol patch | RSS patch |
|--------|------------|-----------|-----------|
| Body definition, orbit, PQS | Yes | — | — |
| EVE cloud configs | — | Yes (V5) | Yes (V3/V5) |
| Scatterer atmosphere | — | Yes | Yes |
| Scale-dependent orbit values | — | If needed | If needed |
| Principia gravity model | — | Yes | Yes |

### 5.2 Body identifier

Follows Sol's pattern: `identifier = NearStars/BodyName`

### 5.3 Minimum star definition

```cfg
@Kopernicus:FOR[NearStarsSystem]
{
    Body
    {
        name = StarName
        identifier = NearStars/StarName
        flightGlobalsIndex = 1001   // Must not collide with Sol-Configs indices

        Orbit
        {
            referenceBody = Sun
            semiMajorAxis = ...     // From real astronomical data
            eccentricity = ...
            inclination = ...
            iconTexture = NearStars-Textures/PluginData/.../Icon.png
        }

        Properties
        {
            displayName = #NearStars_StarName_name
            description = #NearStars_StarName_desc
            radius = ...
            gravParameter = ...
            rotationPeriod = ...
            ScienceValues { ... }
        }

        ScaledVersion
        {
            type = Star
            ...
        }
    }
}
```

### 5.4 Minimum planet definition

Follows Earth-Kopernicus.cfg pattern:
- `Template { name = Kerbin; removeAllPQSMods = True }` — wipe the template
- `PQS > Mods > VertexHeightMapBicubic` — 16-bit heightmap
- `PQS > Mods > VertexColorMap` — color map
- `PQS > Mods > Parallax` — Parallax Continued integration
- Atmospheric bodies: `Atmosphere` block + `AtmosphereFromGround`

### 5.5 File separation per body

| File | Contents |
|------|----------|
| `[Body]-Kopernicus.cfg` | Orbit, physics, atmosphere, PQS, biomes |
| `[Body]-Localization.cfg` | Display name and description (localization keys) |
| `[Body]-ScienceDefs.cfg` | Science experiment result text |
| `[Body]-ParallaxTerrain.cfg` | Parallax terrain settings |
| `[Body]-ParallaxScatters.cfg` | Parallax scatter objects |

---

## 6. Texture Conventions

| Purpose | Format | Resolution |
|---------|--------|------------|
| Heightmap | DDS BC4 | 8k–16k |
| Color map | DDS BC7 | 8k–16k |
| Biome map | DDS | 4k |
| Icon | PNG | 256x256 |
| Normal map | DDS BC5 | 4k–8k |

Texture path pattern:
```
NearStars-Textures/PluginData/[##_SystemFolder]/[##_BodyFolder]/Kopernicus/[BodyName]_[Type].dds
```

Note: BC5/BC7 are not formally supported on macOS — same limitation as Sol.

---

## 7. flightGlobalsIndex Allocation

Must not collide with Sol-Configs **or** RSS-Origin. NearStars uses
1000+ with 100 indices per system.

| Range | Owner |
|-------|-------|
| 0–99 | Stock KSP / RealSolarSystem (KSP-RO/RealSolarSystem occupies 1–25, 50, 60, 91–95) |
| 100–199 | Sol-Configs (RSS-Reborn) |
| 1000–1099 | NearStars — first star system (TBD) |
| 1100–1199 | NearStars — second star system (TBD) |
| 1200–1299 | NearStars — third star system (TBD) |
| 1300+ | NearStars — further systems (+100 per system) |

Within each 100-index block, increment by 1 per body. Stars, planets,
moons, and barycenters share the block.

---

## 8. Astronomical Data Sources

All orbital parameters and physical constants must come from real observational data.

- **Orbital data:** NASA JPL Horizons, SIMBAD
- **Exoplanets:** NASA Exoplanet Archive
- **Stellar physics:** SIMBAD Astronomical Database
- Texture sources must be documented in `Credits-License.md`

---

## 9. Development Phases

**Rule: complete one system end-to-end before starting the next.**

### Phase 1 — First system: star skeleton (MVP)
- [ ] Choose pilot system (recommendation: Proxima Centauri)
- [ ] Repository structure setup
- [ ] Star body definition: orbit, ScaledVersion, Properties
- [ ] Icon and localization key skeleton
- [ ] Verify load in Kopernicus (Sol + RSS)

### Phase 2 — First system: planets
- [ ] Planet definitions (atmosphere, PQS, biomes)
- [ ] Verify all bodies load and orbit correctly

### Phase 3 — First system: visuals
- [ ] Texture production (heightmaps, color maps)
- [ ] Parallax terrain and scatters
- [ ] EVE cloud layers for atmospheric bodies
- [ ] Scatterer atmosphere configs

### Phase 4 — First system: polish + expand
- [ ] Science experiment text for all bodies
- [ ] Compatibility patches (Principia, Kerbalism if applicable)
- [ ] Performance pass
- [ ] Begin second system using Phase 1–3 as template

---

## 10. Open Decisions

- [x] Final mod name — settled as `NearStars`
- [ ] Pilot system selection (Proxima Centauri recommended)
- [ ] Inter-stellar distance scaling strategy — real distances are physically impossible in KSP; symbolic compression required. Must be consistent across Sol stock, Sol quarter, and RSS 1:1 scales. Kopernicus hard limit: ~50 ly (see §3.1).
- [x] macOS texture format compatibility strategy — Windows-only mod; BC5/BC7/BC4 DDS usable without restriction
- [ ] RSS EVE version: V3 (free) vs V5 (Patreon) — whether to support both or V5 only like Sol
- [ ] Principia compatibility: requires separate gravity model cfgs per scale variant; Principia-only entries for 50–80 ly stars are possible (no Kopernicus body needed)
