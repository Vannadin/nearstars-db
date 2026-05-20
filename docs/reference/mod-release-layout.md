# NearStars Mod-Release Repo Layout

> Moved from `guideline.md §4–6` on 2026-05-20. This file documents the
> mod-release repository (`NearStars-Configs/` + `NearStars-Textures/`),
> which is **separate** from the `nearstars-db` data-engine repo this
> file lives in. The mod-release repo does not yet exist as a standalone
> Git repo; the layout below is the target structure for when it spins
> off.

---

## 1. Repository Structure

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

## 2. Config Conventions

### 2.1 Patch tags and dual-compatibility strategy

> Status: Sol-only is the current MVP. The RSS-side patches below are documented as the future target structure — they are not currently shipped.
>
> Exception: Principia patches (`@principia_gravity_model`,
> `@principia_initial_state`) deliberately diverge from the
> `:NEEDS:FOR[NearStarsSystem]` form below — see the
> [`principia-cfg` skill](../../.claude/skills/principia-cfg/SKILL.md)
> for the rationale (they edit nodes Sol-Configs already authored, so
> `:FOR[NearStarsSystem]` claims authorship spuriously).

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

### 2.2 Body identifier

Follows Sol's pattern: `identifier = NearStars/BodyName`

### 2.3 Minimum star definition

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

### 2.4 Minimum planet definition

Follows Earth-Kopernicus.cfg pattern:
- `Template { name = Kerbin; removeAllPQSMods = True }` — wipe the template
- `PQS > Mods > VertexHeightMapBicubic` — 16-bit heightmap
- `PQS > Mods > VertexColorMap` — color map
- `PQS > Mods > Parallax` — Parallax Continued integration
- Atmospheric bodies: `Atmosphere` block + `AtmosphereFromGround`

### 2.5 File separation per body

| File | Contents |
|------|----------|
| `[Body]-Kopernicus.cfg` | Orbit, physics, atmosphere, PQS, biomes |
| `[Body]-Localization.cfg` | Display name and description (localization keys) |
| `[Body]-ScienceDefs.cfg` | Science experiment result text |
| `[Body]-ParallaxTerrain.cfg` | Parallax terrain settings |
| `[Body]-ParallaxScatters.cfg` | Parallax scatter objects |

---

## 3. Texture Conventions

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
