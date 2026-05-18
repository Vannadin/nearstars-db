# Orbit CFG

Values from JPL Horizons. Sol uses epoch = 0 (sampled at JD2433647.5, A.D. 1951-Jan-01).

## Star orbit (distant from Sol)

```cfg
Orbit
{
    referenceBody            = Sun
    semiMajorAxis            = 3.97E+13     // meters — Proxima ≈ 4.24 ly from Sol
    eccentricity             = 0.0
    inclination              = 0.0
    meanAnomalyAtEpochD      = 0
    longitudeOfAscendingNode = 0
    argumentOfPeriapsis      = 0
    epoch                    = 0
    color      = 1.0,0.3,0.1,1
    nodeColor  = 1.0,0.3,0.1,1
    iconTexture = NearStars-Textures/PluginData/ProximaCentauri/Kopernicus/Proxima_Icon.png
    icon = ALL
}
```

## Planet orbit (around new star)

```cfg
Orbit
{
    referenceBody            = Proxima
    semiMajorAxis            = 7.5E+09      // meters (~0.05 AU, habitable zone for red dwarf)
    eccentricity             = 0.02
    inclination              = 1.5
    meanAnomalyAtEpochD      = 45.0
    longitudeOfAscendingNode = 120.0
    argumentOfPeriapsis      = 60.0
    epoch                    = 0
    color      = 0.4,0.6,0.8,1
    nodeColor  = 0.4,0.6,0.8,1
    iconTexture = NearStars-Textures/PluginData/ProximaB/Kopernicus/ProximaB_Icon.png
    icon = ALL
    cameraSmaRatioBounds = 0.03 25
}
```

## Moon orbit

```cfg
Orbit
{
    referenceBody            = ProximaB
    semiMajorAxis            = 3.84E+08     // meters (~Earth-Moon distance)
    eccentricity             = 0.05
    inclination              = 5.0
    meanAnomalyAtEpochD      = 0
    longitudeOfAscendingNode = 0
    argumentOfPeriapsis      = 0
    epoch                    = 0
    color     = 0.6,0.6,0.6,1
    nodeColor = 0.6,0.6,0.6,1
    icon = ALL
}
```

## Notes

- `semiMajorAxis` is always in **meters** (not AU or km)
- `epoch = 0` aligns with Sol's JD2433647.5 reference — set in `Sol-KopernicusSettings.cfg` via `@Kopernicus { @name = Sol }`
- For NearStars stars orbiting Sol at stellar distances, eccentricity/inclination/meanAnomaly are effectively decorative
- `cameraSmaRatioBounds` controls camera zoom limits in map view; omit for stars
