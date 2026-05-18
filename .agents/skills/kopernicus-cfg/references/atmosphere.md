# Atmosphere CFG

Reference: `RSS-Reborn/Sol-Configs` → `Configs/03_Earth-System/03_Earth/Earth-Kopernicus.cfg`
Kopernicus source: `ballisticfox/Kopernicus` → `src/Kopernicus/Configuration/AtmosphereLoader.cs`

## Full Atmosphere block

```cfg
Atmosphere
{
    enabled  = True
    oxygen   = False                         // True only for Earth-like bodies
    adiabaticIndex         = 1.4             // heat capacity ratio (N₂/O₂ mix ≈ 1.4)
    atmosphereDepth        = 100000          // meters — top of atmosphere
    atmosphereMolarMass    = 0.029           // kg/mol (Earth air = 0.0289644)
    shockTemperatureMultiplier = 1.0         // reentry heating multiplier
    pressureCurveIsNormalized   = False      // False = absolute altitude (meters)
    temperatureCurveIsNormalized = False
    ambientColor = 0.15,0.08,0.04,1         // tint of objects inside atmosphere
    lightColor   = 0.6,0.35,0.15,0.5        // AFG waveLength (sky color source)
    addAFG       = True                      // atmospheric glow from orbit
    temperatureSeaLevel = 280

    pressureCurve                            // kPa vs altitude (meters)
    {
        key = 0      101.325 0 -0.012
        key = 10000   26.5   -0.004 -0.004
        key = 30000    1.2   -0.0002 -0.0002
        key = 60000    0.002 -0.00001 -0.00001
        key = 100000   0     0 0
    }
    temperatureCurve                         // K vs altitude (meters)
    {
        key = 0      280 0 -0.007
        key = 12000  216 -0.001 -0.001
        key = 30000  226 0.002 0.002
        key = 60000  248 0 0
        key = 100000 180 -0.001 0
    }
    temperatureSunMultCurve                  // day/night temperature modifier by altitude
    {
        key = 0     1 0 0
        key = 10000 0.65 0 0
        key = 60000 0 0 0
    }
    temperatureLatitudeBiasCurve             // pole-equator temperature difference
    {
        key = 0  10 0 0
        key = 45  0 -0.5 -0.5
        key = 90 -25 -0.4 0
    }
    temperatureLatitudeSunMultCurve          // equatorial solar heating
    {
        key = 0  10 0 0
        key = 45 8 0 0
        key = 90 4 0 0
    }
}
```

## Minimal atmosphere (thin/trace)

```cfg
Atmosphere
{
    enabled  = True
    oxygen   = False
    adiabaticIndex      = 1.67              // monatomic (CO₂-like)
    atmosphereDepth     = 50000
    atmosphereMolarMass = 0.044             // CO₂
    shockTemperatureMultiplier = 0.8
    pressureCurveIsNormalized   = False
    temperatureCurveIsNormalized = False
    ambientColor = 0.05,0.02,0.01,1
    addAFG = True
    temperatureSeaLevel = 210
    pressureCurve
    {
        key = 0     0.7  0 -0.00002
        key = 20000 0.05 -0.000002 -0.000002
        key = 50000 0    0 0
    }
    temperatureCurve
    {
        key = 0     210 0 -0.002
        key = 25000 160 0 0
        key = 50000 140 0 0
    }
}
```

## Notes

- `pressureCurve` key format: `altitude pressure tangentIn tangentOut` (kPa)
- `temperatureCurve` key format: `altitude temperature tangentIn tangentOut` (K)
- Final pressure key must be `0` at `atmosphereDepth`
- `lightColor` drives AFG and Scatterer's base sky color — match to star spectrum
- For tidally-locked bodies, flatten `temperatureLatitudeSunMultCurve` and set high `temperatureLatitudeBiasCurve` values
