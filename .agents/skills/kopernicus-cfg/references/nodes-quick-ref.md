# Kopernicus Node Quick Reference

Source: kopernicuswiki.github.io

---

## Body node

| Field | Type | Description |
|-------|------|-------------|
| name | String | Internal name (no spaces). Used in referenceBody, Template, etc. |
| identifier | String | Unique Body Identifier: `StarName/BodyName` |
| finalizeOrbit | Boolean | Whether orbit should be finalized |
| flightGlobalsIndex | Integer | Unique integer ID. Stock: Sun=0, Kerbin=1, Mun=2, etc. Use 100+ for custom |
| barycenter | Boolean | Makes body unselectable (for barycenters) |
| randomMainMenuBody | Boolean | Can appear on main menu |
| contractWeight | Integer | Weight for contract generation (default 30) |
| cacheFile | File Path | Path to .bin mesh cache. Use `ParallaxContinued/Models/ScaledMesh.bin` if using Parallax |

Subnodes: `Template`, `Properties`, `Orbit`, `ScaledVersion`, `Atmosphere`, `PQS`, `Ocean`, `Rings`, `Particles`, `HazardousBody`, `SpaceCenter`, `Debug`, `PostSpawnOrbit`

---

## Template node

| Field | Type | Description |
|-------|------|-------------|
| name | String | Stock body to copy as base (Sun, Kerbin, Mun, Minmus, Moho, Eve, Duna, Ike, Jool, Laythe, Vall, Tylo, Bop, Pol, Eeloo, Gilly, Dres) |
| removeAllPQSMods | Boolean | Remove all terrain mods from template (use when providing own heightmap) |
| removePQS | Boolean | Remove PQS entirely |
| removeAtmosphere | Boolean | Remove atmosphere from template |
| removeBiomes | Boolean | Remove biome data |
| removeOcean | Boolean | Remove ocean |
| removeCoronas | Boolean | Remove coronas (for Sun template) |

---

## Orbit node

| Field | Type | Description |
|-------|------|-------------|
| referenceBody | String | Name of parent body |
| semiMajorAxis | Double | Average distance from parent center, **meters** |
| eccentricity | Double | 0 = circle, 0–1 = ellipse |
| inclination | Double | Degrees. 0 = coplanar, 90 = polar |
| meanAnomalyAtEpochD | Double | Starting position on orbit in **degrees** (preferred over radians version) |
| longitudeOfAscendingNode | Double | Degrees |
| argumentOfPeriapsis | Double | Degrees |
| epoch | Double | Reference time for meanAnomaly (0 = KSP start) |
| color | Color | Orbit line color `R,G,B,A` (0–1) |
| nodeColor | Color | Maneuver node color |
| iconTexture | File Path | Custom orbit icon texture |
| icon | OrbitDrawIcons | `NONE`, `OBJ`, `OBJ_PE_AP`, `ALL` |

**AU to meters**: 1 AU = 1.49597871e11 m

---

## Properties node

| Field | Type | Description |
|-------|------|-------------|
| displayName | String | In-game name (supports localization tags) |
| description | String | Info box description |
| radius | Double | Body radius in **meters** |
| gravParameter | Double | G×M in m³/s² (preferred over mass for precision) |
| mass | Double | kg (use gravParameter instead when possible) |
| geeASL | Double | Surface gravity in Gs (can derive from gravParameter/radius²) |
| rotationPeriod | Double | Sidereal rotation period in **seconds** |
| tidallyLocked | Boolean | Locks rotation to orbit |
| initialRotation | Double | Starting rotation angle (degrees, 0–360) |
| solarRotationPeriod | Boolean | Use solar day instead of sidereal |
| rotates | Boolean | Whether body rotates at all |
| albedo | Double | 0–1 reflectivity |
| emissivity | Double | 0–1 heat emission |
| isHomeWorld | Boolean | Marks as KSC home (only one body should have this) |
| sphereOfInfluence | Double | SOI in meters; omit to auto-calculate |
| timewarpAltitudeLimits | Integer[] | 8 altitude thresholds for time warp levels |
| navballSwitchRadiusMult | Double | Navball frame switch altitude (fraction of radius) |
| biomeMap | File Path | DDS biome map texture |
| RnDVisibility | Enum | `Visible`, `Noicon`, `Hidden`, `Skip` |
| maxZoom | Single | Max map view zoom in meters |

### ScienceValues subnode

| Field | Description |
|-------|-------------|
| landedDataValue | Science multiplier when landed |
| splashedDataValue | Science multiplier when splashed |
| flyingLowDataValue | Flying low science |
| flyingHighDataValue | Flying high science |
| inSpaceLowDataValue | Low orbit science |
| inSpaceHighDataValue | High orbit science |
| recoveryValue | Recovery multiplier |
| flyingAltitudeThreshold | Altitude (m) dividing low/high flight |
| spaceAltitudeThreshold | Altitude (m) dividing low/high space |

### Biomes subnode

```cfg
Biomes
{
    Biome
    {
        name = BiomeName           // Internal name
        displayName = Display Name // Shown in-game
        value = 1                  // Science multiplier
        color = RGBA(R,G,B,255)   // Must match biome map pixel color exactly
    }
}
```

---

## ScaledVersion node

| Field | Type | Description |
|-------|------|-------------|
| type | Enum | `Vacuum`, `Atmospheric`, `Star` |
| fadeStart | Double | Altitude (m) where ScaledSpace transition starts |
| fadeEnd | Double | Altitude (m) where transition ends |
| sphericalModel | Boolean | Use sphere mesh |
| deferMesh | Boolean | Defer mesh generation |

### Material subnode (Vacuum/Atmospheric)
```cfg
Material
{
    texture = Path/To/color.dds
    normals = Path/To/normal.dds
    shininess = 0.05             // 0 = matte, 1 = very shiny
    specular = 0.1,0.1,0.1,1
    // Atmospheric only:
    rimPower = 2.4               // Atmosphere rim glow falloff
    rimBlend = 1.1
    Gradient
    {
        0.0 = R,G,B,A            // At terminator
        0.6 = R,G,B,A            // Night side
        1.0 = R,G,B,A
    }
}
```

### Light subnode (Stars only)
```cfg
Light
{
    sunlightColor = 1,1,1,1
    sunlightShadowStrength = 0.75
    scaledSunlightColor = 1,1,1,1
    IVASunColor = 1,0.977,0.896,1
    ambientLightColor = 0.06,0.06,0.06,1
    givesOffLight = True
    sunAU = 13599840256          // KSP's 1 AU in meters
    luminosity = 1360            // Solar constant at 1 AU (W/m²)
    brightnessCurve { key = ... }
    IntensityCurve { key = ... }
    ScaledIntensityCurve { key = ... }
    IVAIntensityCurve { key = ... }
}
```

---

## Atmosphere node

| Field | Type | Description |
|-------|------|-------------|
| enabled | Boolean | Whether atmosphere exists |
| oxygen | Boolean | Whether atmosphere is breathable |
| atmosphereDepth | Double | Height of atmosphere in meters |
| adiabaticIndex | Double | Heat capacity ratio (dry air = 1.4) |
| atmosphereMolarMass | Double | kg/mol (Earth air = 0.0289644) |
| staticPressureASL | Double | Sea level pressure in kPa |
| temperatureSeaLevel | Double | Sea level temperature in K |
| ambientColor | Color | Ambient light color inside atmosphere |
| lightColor | Color | Same as wavelength in AtmosphereFromGround |
| addAFG | Boolean | Add AtmosphereFromGround scattering |
| shockTemperatureMultiplier | Double | Aeroheating multiplier |
| pressureCurveIsNormalized | Boolean | Use 0–1 range instead of 0–atmosphereDepth |
| temperatureCurveIsNormalized | Boolean | Same for temperature |

### Curve format
```cfg
pressureCurve
{
    key = altitude  pressure  inTangent  outTangent
    // altitude in meters, pressure in kPa
    // equal in/out tangents = smooth spline
    key = 0     101.325  0        -0.012
    key = 10000 27.4635  -0.004   -0.004
    key = 80000 0        0        0
}
```

---

## PQS node

| Field | Type | Description |
|-------|------|-------------|
| maxQuadLengthsPerFrame | Single | Performance: max quads loaded per frame |
| minLevel | Integer | Minimum terrain detail level |
| maxLevel | Integer | Maximum terrain detail level (12–15) |
| minDetailDistance | Double | Minimum camera distance for detail |
| deactivateAltitude | Double | Altitude where PQS turns off |
| fadeStart | Double | Altitude where PQS starts fading |
| fadeEnd | Double | Altitude where PQS fully fades |
| materialType | Enum | Terrain shader type |

### Key PQS Mods (inside `Mods { }`)

| Mod | Fields | Purpose |
|-----|--------|---------|
| `VertexHeightMap` | map, offset, deformity, scaleDeformityByRadius, order, enabled | Apply grayscale heightmap |
| `VertexHeightMapBicubic` | same as above | Smoother heightmap (Sol uses for Mercury) |
| `VertexColorMap` | map, order, enabled | Apply color texture |
| `VertexSimplexHeightAbsolute` | deformity, frequency, octaves, persistence, seed, order, enabled | Procedural simplex noise terrain |
| `VertexSimplexNoiseColor` | deformity, frequency, ... | Procedural noise coloring |
| `Parallax` | subdivisionLevel, subdivisionRadius, order | Parallax Continued support |

```cfg
VertexHeightMap
{
    map = YourMod/PluginData/planet_height.dds
    offset = 0                  // Height offset in meters
    deformity = 10000           // Max terrain height above/below sea level, meters
    scaleDeformityByRadius = false
    order = 20
    enabled = true
}
```

---

## Rings node

```cfg
Rings
{
    Ring
    {
        innerRadius = 1.5        // Multiplier of body radius
        outerRadius = 2.5
        angle = 0                // Tilt in degrees
        color = 0.6,0.5,0.4,0.8
        lockRotation = false
        unlit = false
        useNewShader = true
        texture = YourMod/PluginData/ring.dds
    }
}
```

---

## Debug node

```cfg
Debug
{
    exportMesh = True    // Export ScaledSpace mesh as .bin cache
    update = False       // Force mesh regeneration (set True once, then False)
    showSOI = False
}
```
