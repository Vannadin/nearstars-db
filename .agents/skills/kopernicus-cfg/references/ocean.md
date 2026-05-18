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

## Full Ocean block (Sol/Earth — realistic water)

```cfg
Ocean
{
    ocean       = True
    oceanColor  = 0.071,0.102,0.157,1
    oceanHeight = 0                       // sea level offset in meters
    density     = 1
    minLevel    = 2
    maxLevel    = 8
    minDetailDistance    = 8
    maxQuadLengthsPerFrame = 0.03

    Material
    {
        color          = 0.451,0.525,0.525,1
        colorFromSpace = 0.141,0.231,0.278,1
        specColor      = 1,1,1,1
        shininess      = 0.698
        gloss          = 0.2
        tiling         = 1000
        waterTex       = BUILTIN/sea-water1
        waterTex1      = BUILTIN/sea-water2
        bTiling        = 800
        bumpMap        = BUILTIN/quiet
        displacement   = 0.05
        texDisplacement = -0.31
        dispFreq       = 0.15
        mix            = 0.368
        oceanOpacity   = 0.5
        falloffPower   = 1.1
        falloffExp     = 2
        fogColor       = 0.918,0.918,1,1
        heightFallOff  = 0.2
        globalDensity  = -8E-06
        atmosphereDepth = 70000
        fogColorRamp   = BUILTIN/AerialRampKerbin2
        fadeStart      = 20000
        fadeEnd        = 60000
        planetOpacity  = 1
        normalXYFudge  = 1.4
        normalZFudge   = 1.18
    }

    FallbackMaterial
    {
        color          = 0.494,0.553,0.627,1
        colorFromSpace = 0.051,0.165,0.216,1
        specColor      = 1,1,1,1
        shininess      = 1
        gloss          = 0.433
        tiling         = 1000
        waterTex       = BUILTIN/sea-water2
        waterTex1      = BUILTIN/sea-water3
        fadeStart      = 20000
        fadeEnd        = 60000
        planetOpacity  = 0
    }

    Fog
    {
        afgAltMult          = 0.05
        afgBase             = 0.6
        afgLerp             = False
        afgMin              = 0.05
        fogColorEnd         = 0,0.085,0.123,1
        fogColorStart       = 0,0.340,0.490,1
        fogDensityAltScalar = -0.0008
        fogDensityEnd       = 0.025
        fogDensityExponent  = 1
        fogDensityPQSMult   = 0.02
        fogDensityStart     = 0.005
        skyColorMult        = 1.1
        skyColorOpacityAltMult = 15
        skyColorOpacityBase = 0.25
        sunAltMult          = 0.01
        sunBase             = 0.5
        sunMin              = 0.05
        useFog              = True
    }

    Mods
    {
        AerialPerspectiveMaterial
        {
            atmosphereDepth     = 5000
            DEBUG_SetEveryFrame = False
            globalDensity       = -7.5E-06
            heightFalloff       = 0.2
            oceanDepth          = 0
            order   = 100
            enabled = True
        }
        OceanFX
        {
            angle            = 0
            blendA           = 0
            blendB           = 0
            framesPerSecond  = 10
            oceanOpacity     = 0
            spaceAltitude    = 0
            spaceSurfaceBlend = 0
            specColor        = 0,0,0,0
            texBlend         = 0.469
            txIndex          = -2147483648
            order   = 100
            enabled = True
            Watermain
            {
                value = BUILTIN/sea-water1
                value = BUILTIN/sea-water2
                value = BUILTIN/sea-water3
                value = BUILTIN/sea-water4
                value = BUILTIN/sea-water5
                value = BUILTIN/sea-water6
                value = BUILTIN/sea-water7
                value = BUILTIN/sea-water8
                value = BUILTIN/sea-water1
            }
        }
    }
}
```

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
