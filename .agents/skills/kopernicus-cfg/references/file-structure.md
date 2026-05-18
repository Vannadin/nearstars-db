# File Structure & Naming Convention

## Directory layout

```
GameData/NearStars/
├── Configs/
│   ├── 00_ProximaCentauri/
│   │   ├── ProximaCentauri-Kopernicus.cfg
│   │   ├── ProximaCentauri-Scatterer.cfg          NEEDS[Scatterer]
│   │   ├── ProximaCentauri-EVE.cfg                NEEDS[EnvironmentalVisualEnhancements]
│   │   └── ProximaCentauri-DOE.cfg                NEEDS[DistantObject]
│   ├── 01_ProximaB/
│   │   ├── ProximaB-Kopernicus.cfg
│   │   ├── ProximaB-ParallaxTerrain.cfg           NEEDS[Parallax]
│   │   ├── ProximaB-ParallaxScatters.cfg          NEEDS[Parallax]
│   │   ├── ProximaB-Scatterer.cfg                 NEEDS[Scatterer]
│   │   ├── ProximaB-EVE.cfg                       NEEDS[EnvironmentalVisualEnhancements]
│   │   ├── ProximaB-Firefly.cfg                   NEEDS[Firefly]
│   │   ├── ProximaB-PlanetShine.cfg               NEEDS[PlanetShine]
│   │   └── ProximaB-ScienceDefs.cfg
│   └── 01_ProximaB-Moon/
│       ├── ProximaBMoon-Kopernicus.cfg
│       └── ...
└── NearStars-KopernicusSettings.cfg               global settings patch
```

## Texture path convention

```
GameData/NearStars-Textures/PluginData/
├── _Misc/
│   └── Kopernicus/
│       └── Blank_Normal.dds                       shared blank normal map
├── ProximaCentauri/
│   └── Kopernicus/
│       ├── Proxima_Sunspots.dds
│       ├── Proxima_Corona.dds
│       └── Proxima_Icon.png
└── ProximaB/
    └── Kopernicus/
        ├── ProximaB_Color.dds                     VertexColorMap
        ├── ProximaB_VertexHeight.dds              VertexHeightMapBicubic
        ├── ProximaB_Biomes.dds                    biomeMap
        ├── ProximaB_Dummy.dds                     ScaledVersion placeholder
        └── ProximaB_Icon.png                      orbit icon
```

## flightGlobalsIndex reservation

| Range | Owner |
|-------|-------|
| 0–99 | Stock KSP |
| 100–199 | Sol (RSS-Reborn) |
| 2000–2999 | NearStars (Proxima Centauri system) |
| 3000–3999 | NearStars (Alpha Centauri system) |

Increment by 1 per body. Stars and planets share the same range.

## NearStars-KopernicusSettings.cfg

```cfg
@Kopernicus:FOR[NearStars]
{
    useOnDemand             = true
    onDemandLoadOnMissing   = true
    onDemandLogOnMissing    = false
    onDemandForceCollect    = false
}
```
