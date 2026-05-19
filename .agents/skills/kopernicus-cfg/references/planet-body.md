# Planet Body CFG (Atmospheric & Vacuum)

Reference: `RSS-Reborn/Sol-Configs` → `Configs/01_Mercury/` (vacuum), `Configs/03_Earth-System/03_Earth/` (atmospheric)

## Top-Level Fields

```cfg
Body
{
    name = ProximaB
    identifier = NearStars/ProximaB
    barycenter = False
    finalizeOrbit = False
    flightGlobalsIndex = 2001             // globally unique
    cacheFile = ParallaxContinued/Models/ScaledMesh.bin
    Template
    {
        name = Kerbin      // atmospheric — inherits stock atmosphere scaffold
        // name = Mun      // vacuum / airless
        removeAllPQSMods = True
    }
}
```

## Properties

```cfg
Properties
{
    displayName = Proxima b
    description = ...
    radius = 7200000
    gravParameter = 5.4E+13
    solarRotationPeriod = False
    rotates = True
    rotationPeriod = 1069200
    tidallyLocked = False
    initialRotation = 0
    isHomeWorld = False
    albedo = 0.3
    emissivity = 0.9
    timewarpAltitudeLimits = 0 30000 30000 60000 300000 600000 900000 1200000
    navballSwitchRadiusMult = 0.016
    navballSwitchRadiusMultLow = 0.015

    biomeMap = NearStars-Textures/PluginData/ProximaB/Kopernicus/ProximaB_Biomes.dds
    Biomes
    {
        Biome
        {
            name = Terminator Zone
            displayName = Terminator Zone
            value = 1.0
            color = RGBA(128,255,255,255)
        }
        Biome
        {
            name = Dayside
            displayName = Dayside
            value = 1.2
            color = RGBA(255,255,255,255)
        }
        Biome
        {
            name = Nightside
            displayName = Nightside
            value = 1.2
            color = RGBA(0,255,255,255)
        }
    }
    ScienceValues
    {
        landedDataValue      = 8
        inSpaceLowDataValue  = 6
        inSpaceHighDataValue = 5
        recoveryValue        = 7
        flyingAltitudeThreshold = 30000
        spaceAltitudeThreshold  = 500000
    }
}
```

## ScaledVersion

### Atmospheric planet

```cfg
ScaledVersion
{
    type = Atmospheric
    fadeStart = 100000
    fadeEnd   = 102000
    sphericalModel = True
    Material
    {
        texture   = NearStars-Textures/PluginData/ProximaB/Kopernicus/ProximaB_Dummy.dds
        normals   = NearStars-Textures/PluginData/_Misc/Kopernicus/Blank_Normal.dds
        color     = 1.3,1.3,1.3,1
        shininess = 0.1
        specular  = 0.3,0.3,0.3,1
        rimPower  = 2.5
        rimBlend  = 1.1
        Gradient
        {
            0.0 = 0.5,0.35,0.2,1.0
            0.3 = 0.2,0.12,0.05,1.0
            0.6 = 0.0,0.0,0.0,1.0
            1.0 = 0.0,0.0,0.0,1.0
        }
    }
}
```

### Vacuum body

```cfg
ScaledVersion
{
    type = Vacuum
    fadeStart = 100000
    fadeEnd   = 102000
    Material
    {
        texture   = NearStars-Textures/PluginData/ProximaB/Kopernicus/ProximaB_Dummy.dds
        normals   = NearStars-Textures/PluginData/_Misc/Kopernicus/Blank_Normal.dds
        shininess = 0.0
        specular  = 0,0,0,1
    }
}
```

---

## Sol reference (vacuum body — Mercury)

For the complete Sol-Configs Mercury cfg, see the upstream file:
[`Sol-Configs/Configs/01_Mercury/Mercury-Kopernicus.cfg`](https://github.com/RSS-Reborn/Sol-Configs/blob/main/Sol-Configs/Configs/01_Mercury/Mercury-Kopernicus.cfg)
(raw: https://raw.githubusercontent.com/RSS-Reborn/Sol-Configs/main/Sol-Configs/Configs/01_Mercury/Mercury-Kopernicus.cfg).

The standard KSP-Kopernicus pattern for a vacuum rocky body looks like:

```cfg
@Kopernicus:FOR[YourPack]
{
    Body
    {
        name                = <BodyName>
        identifier          = YourPack/<BodyName>
        flightGlobalsIndex  = <unique integer>
        Template            { name = Mun; removeAllPQSMods = True }

        Orbit         { referenceBody = Sun; semiMajorAxis = ...; eccentricity = ...; ... }
        Properties    { radius = ...; gravParameter = ...; rotationPeriod = ...; ... }
        ScaledVersion { type = Vacuum; Material { texture = ...; normals = ... } }
        PQS           { Mods { Parallax {...}; VertexHeightMapBicubic {...}; ... } }
    }
}
```

Mercury's real physical values (radius, gravParameter, rotation period,
albedo) are public-domain facts available from the
[NASA Mercury Fact Sheet](https://nssdc.gsfc.nasa.gov/planetary/factsheet/mercuryfact.html).
Sol-Configs wires those values into the Kopernicus template above, plus
texture paths and biome definitions specific to the Sol-Configs mod.

---

## Sol reference (atmospheric body — Earth)

For the complete Sol-Configs Earth cfg, see:
[`Sol-Configs/Configs/03_Earth-System/03_Earth/Earth-Kopernicus.cfg`](https://github.com/RSS-Reborn/Sol-Configs/blob/main/Sol-Configs/Configs/03_Earth-System/03_Earth/Earth-Kopernicus.cfg)
(raw: https://raw.githubusercontent.com/RSS-Reborn/Sol-Configs/main/Sol-Configs/Configs/03_Earth-System/03_Earth/Earth-Kopernicus.cfg).

Differences vs the vacuum pattern above:

- `ScaledVersion.type = Atmospheric`
- `ScaledVersion.Material` adds a `Gradient` block for atmospheric rim glow
- A top-level `Atmosphere` node is required with at minimum:

```cfg
Atmosphere
{
    enabled             = True
    oxygen              = True | False
    atmosphereDepth     = <m>
    atmosphereMolarMass = <kg/mol>
    adiabaticIndex      = <unitless>
    temperatureSeaLevel = <K>
    temperatureCurve    { ... }
    pressureCurve       { ... }
}
```

Real-world Earth atmospheric profiles (US Standard Atmosphere 1976) used
as input to `temperatureCurve` / `pressureCurve` are public-domain
references — see https://ntrs.nasa.gov/citations/19770009539. Sol-Configs'
specific curve keypoints are at the raw URL above.
