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

NearStars uses **1000+, with 100 indices per system** to stay clear of
both Sol-Configs and RSS-Origin.

| Range | Owner |
|-------|-------|
| 0–99 | Stock KSP / RealSolarSystem (KSP-RO/RealSolarSystem occupies 1–25, 50, 60, 91–95) |
| 100–199 | Sol-Configs (RSS-Reborn) |
| 1000–1099 | NearStars (Proxima Centauri system) |
| 1100–1199 | NearStars (Alpha Centauri system) |
| 1200–1299 | NearStars (Barnard's Star) |
| 1300+ | NearStars (additional systems — +100 per system) |

Within a system's 100-index block, increment by 1 per body. Stars,
planets, moons, and barycenters share the same block. 100 slots are
enough for the most complex multi-star + multi-planet + moon hierarchies
in the catalog (e.g. α Centauri AB + Proxima + their planets fits well
under 100).

## NearStars-KopernicusSettings.cfg

```cfg
@Kopernicus:FOR[NearStarsSystem]
{
    useOnDemand             = true
    onDemandLoadOnMissing   = true
    onDemandLogOnMissing    = false
    onDemandForceCollect    = false
}
```
