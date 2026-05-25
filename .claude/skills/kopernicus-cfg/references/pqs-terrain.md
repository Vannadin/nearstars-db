# PQS Terrain CFG

Reference: `RSS-Reborn/Sol-Configs` → `Configs/01_Mercury/Mercury-Kopernicus.cfg` (vacuum), `Configs/03_Earth-System/03_Earth/Earth-Kopernicus.cfg` (atmospheric)
Kopernicus source: `ballisticfox/Kopernicus` → `src/Kopernicus/Configuration/PQSLoader.cs`, `ModLoader/`

## Full PQS block

```cfg
PQS
{
    maxQuadLengthsPerFrame = 0.03
    minLevel = 2
    maxLevel = 12                         // 13 for high-detail bodies
    minDetailDistance = 8
    deactivateAltitude = 120000           // must be > fadeEnd
    fadeStart = 102000
    fadeEnd   = 117000

    materialType = AtmosphericTriplanarZoomRotation   // atmospheric bodies
    // materialType = SphereSegment                   // vacuum bodies

    Material
    {
        factor           = 9
        factorBlendWidth = 0.01
        factorRotation   = 30
        saturation       = 1
        contrast         = 1
        tintColor        = 1,1,1,0
        specularColor    = 0,0,0,0
        albedoBrightness = 1

        steepPower    = 1
        steepTexStart = 20000
        steepTexEnd   = 30000
        steepTex      = BUILTIN/terrain_rock00
        steepTexScale = 1,1
        steepTexOffset = 0,0
        steepBumpMap   = BUILTIN/Cliff (Layered Rock)_NRM
        steepBumpMapScale  = 1,1
        steepBumpMapOffset = 0,0
        steepNearTiling = 1
        steepTiling     = 1

        lowTex    = BUILTIN/MunFloor [Diffuse]
        lowTexScale  = 1,1
        lowTexOffset = 0,0
        lowTiling = 50000

        midTex    = BUILTIN/MunFloor [Diffuse]
        midTexScale  = 1,1
        midTexOffset = 0,0
        midTiling    = 50000
        midBumpMap   = BUILTIN/MunFloor [Normal]
        midBumpMapScale  = 1,1
        midBumpMapOffset = 0,0
        midBumpTiling    = 50000

        highTex   = BUILTIN/MunFloor [Diffuse]
        highTexScale  = 1,1
        highTexOffset = 0,0
        highTiling    = 50000

        lowStart  = -1
        lowEnd    = -1
        highStart = 2
        highEnd   = 2

        globalDensity    = 1
        fogColorRamp     =
        fogColorRampScale  = 1,1
        fogColorRampOffset = 0,0
        planetOpacity    = 1
        oceanFogDistance = 1000
    }

    Mods
    {
        Parallax
        {
            subdivisionLevel  = 8       // 6–8 typical; higher = more geometry
            subdivisionRadius = 500
            order = 999999
        }
        VertexColorMap
        {
            map     = NearStars-Textures/PluginData/ProximaB/Kopernicus/ProximaB_Color.dds
            order   = 10
            enabled = True
        }
        VertexHeightMapBicubic
        {
            map                    = NearStars-Textures/PluginData/ProximaB/Kopernicus/ProximaB_VertexHeight.dds
            offset                 = 0
            deformity              = 12000.0    // max terrain height in meters
            scaleDeformityByRadius = False
            order   = 20
            enabled = True
        }
    }
}
```

## Debug block

Append during development, remove before release:

```cfg
Debug
{
    exportMesh = True
    update     = False
    showSOI    = False
}
```

## Notes

- `deactivateAltitude` must be greater than `fadeEnd` or terrain flickers
- Delete `Kopernicus/Cache/<BodyName>.bin` when changing mesh-affecting settings
- `VertexHeightMapBicubic` is preferred over `VertexHeightMap` for smoother terrain
- Parallax mod in `PQS.Mods` is required even if `ParallaxTerrain.cfg` handles the visual layer
