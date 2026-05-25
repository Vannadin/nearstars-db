# Ocean Node CFG

References:
- `RSS-Reborn/Sol-Configs` → `Sol-Configs/Configs/03_Earth-System/03_Earth/Earth-Kopernicus.cfg`
- `Kopernicus/KopernicusExamples` → `Creating New Bodies/OceanBody/Oceanus.cfg`

## Key points

- `Ocean {}` is a sibling of `PQS {}`, not inside it
- The PQS `offset` on `VertexHeightMap` controls what counts as "below sea level" — negative offset pushes terrain down so the ocean covers it
- `HazardousOcean` (heat damage inside the ocean) lives inside `Ocean.Mods`, not in `HazardousBody`
- Two Material blocks are required: `Material` (normal rendering) and `FallbackMaterial` (low-quality fallback)
- `OceanFX` inside `Ocean.Mods` handles the animated water surface

## Minimal Ocean block (Kopernicus example — Oceanus)

```cfg
Ocean
{
    maxQuadLengthsPerFrame = 0.03
    minLevel = 2
    maxLevel = 16
    minDetailDistance = 16
    oceanColor = 0.15,0.25,0.35,1

    Material
    {
        colorFromSpace = 0.15,0.25,0.35,1
        color          = 0.15,0.25,0.35,1
    }
    FallbackMaterial
    {
        colorFromSpace = 0.15,0.25,0.35,1
        color          = 0.15,0.25,0.35,1
    }

    Mods
    {
        AerialPerspectiveMaterial
        {
            globalDensity    = -0.00001
            heightFalloff    = 6.75
            atmosphereDepth  = 150000
            DEBUG_SetEveryFrame = true
            enabled = true
            order   = 200
        }
        OceanFX
        {
            Watermain
            {
                waterTex-0 = BUILTIN/sea-water1
                waterTex-1 = BUILTIN/sea-water2
                waterTex-2 = BUILTIN/sea-water3
                waterTex-3 = BUILTIN/sea-water4
                waterTex-4 = BUILTIN/sea-water5
                waterTex-5 = BUILTIN/sea-water6
                waterTex-6 = BUILTIN/sea-water7
                waterTex-7 = BUILTIN/sea-water8
            }
            framesPerSecond  = 1
            spaceAltitude    = 150000
            blendA           = 0
            blendB           = 0
            texBlend         = 0
            angle            = 0
            specColor        = 0.0,0.0,-1,1
            oceanOpacity     = 0
            spaceSurfaceBlend = 0
            enabled = true
            order   = 200
        }
    }

    Fog
    {
        fogColorEnd   = 0.15,0.25,0.35,1
        fogColorStart = 0.15,0.25,0.35,1
        skyColorOpacityBase = 0.7
    }
}
```

## Sol reference (realistic water — Earth)

For the complete Sol-Configs Earth Ocean block (Material, FallbackMaterial,
Fog, Mods/OceanFX with full tuning curves), see the upstream file:
[`Sol-Configs/Configs/03_Earth-System/03_Earth/Earth-Kopernicus.cfg`](https://github.com/RSS-Reborn/Sol-Configs/blob/main/Sol-Configs/Configs/03_Earth-System/03_Earth/Earth-Kopernicus.cfg)
(raw: https://raw.githubusercontent.com/RSS-Reborn/Sol-Configs/main/Sol-Configs/Configs/03_Earth-System/03_Earth/Earth-Kopernicus.cfg).

The Sol-Configs Ocean block extends the minimal Oceanus pattern above with:

- Detailed `Material` block (specColor, shininess, gloss, multi-texture
  tiling, bump map, fog/aerial perspective parameters)
- Separate `FallbackMaterial` block for the low-quality fallback render
- A standalone top-level `Fog` block (different from Material fog) tuned
  for Earth-like sky-blue scattering — afgBase, fogColorStart/End,
  fogDensityAltScalar, skyColorOpacityAltMult, sun parameters
- An `OceanFX` mod with framesPerSecond=10 and the full 8-frame water
  animation sequence in `Watermain`

These additional nodes are not strictly required for Kopernicus to render
an ocean — they fine-tune visual realism. Start from the minimal Oceanus
pattern above when prototyping a new ocean world, then inspect the
Sol-Configs raw URL above when you need a reference for fully-tuned
aesthetic values.

## HazardousOcean (heat damage inside the ocean)

This lives inside `Ocean.Mods`, not in `HazardousBody`. Keys are depth (meters below surface) → heat value.

```cfg
// Source: Kopernicus/KopernicusExamples → Hazardous Oceans Example/EveOceanHazard.cfg
@Body[Eve]
{
    Ocean
    {
        HazardousOcean
        {
            key = 1000  0      // 1000 m depth: no extra heat
            key = 500   5
            key = 250   25
            key = 0     100    // at the surface: full heat
        }
    }
}
```

## PQS setup for ocean worlds

The `VertexHeightMap` offset must be negative to push terrain below sea level:

```cfg
PQS
{
    Mods
    {
        VertexHeightMap
        {
            map      = NearStars-Textures/PluginData/MyPlanet/Kopernicus/MyPlanet_VertexHeight.dds
            offset   = -500        // pushes terrain 500 m below sea level → ocean covers lowlands
            deformity = 7000.0
            scaleDeformityByRadius = false
            order   = 20
            enabled = true
        }
    }
}
```
