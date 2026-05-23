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

NearStars uses **1000+, with 100 indices per system**, which sits in
the empty band between Sol-Configs' planetary IDs (≤916) and its
asteroid IDs (≥9000). RSS-Origin 2 (CharonSSS, v1.0.0 2026-05-21)
does not assign explicit `flightGlobalsIndex` values at all — it
relies on Kopernicus auto-assignment.

| Range | Owner |
|-------|-------|
| 0–99 | Stock KSP / RealSolarSystem (KSP-RO/RealSolarSystem occupies 1–25, 50, 60, 91–95) |
| `10`, `100`–`916` | Sol-Configs planets and moons (NAIF SPK-style IDs: Sol=`10`, Mercury=`100`, …, Neptune=`800`, Pluto system=`901–916`) |
| `9xxx`–`9xxxxxx` | Sol-Configs asteroids (`9` + asteroid number, e.g. Ida=`9243`) |
| `10xxxxxx`+ | Sol-Configs TNOs / dwarf planets (Eris=`10134340`) |
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
