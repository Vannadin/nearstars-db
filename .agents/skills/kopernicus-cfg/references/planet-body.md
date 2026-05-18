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

## Sol Source — Mercury (vacuum)

Source: `Sol-Configs/Configs/01_Mercury/Mercury-Kopernicus.cfg`

```cfg
@Kopernicus:FOR[SolSystem]
{
    Body
    {
        name = Mercury
        identifier = Sol/Mercury
        flightGlobalsIndex = 100
        cacheFile = ParallaxContinued/Models/ScaledMesh.bin

        Template
        {
            name = Mun
            removeAllPQSMods = True
        }

        Orbit
        {
            referenceBody            = Sun
            semiMajorAxis            = 57909081859.97428
            eccentricity             = 0.2056264110797241
            inclination              = 7.0064631630008085
            meanAnomalyAtEpochD      = 12.23374264650345
            longitudeOfAscendingNode = 48.39193279902154
            argumentOfPeriapsis      = 28.98861975116913
            epoch                    = 0
            color       = 0.429,0.412,0.375,1
            icon        = ALL
            iconTexture = Sol-Textures/PluginData/01_Mercury/Kopernicus/Mercury_Icon.png
        }

        Properties
        {
            displayName = #Sol_Mercury_name
            radius = 2439400
            gravParameter = 2.203186855E+13
            rotationPeriod = 5067027.00596      // 58.65 days
            tidallyLocked = false
            initialRotation = 285
            albedo = 0.106
            emissivity = 0.77
            timewarpAltitudeLimits = 0 5000 30000 30000 100000 300000 600000 1000000
            biomeMap = Sol-Textures/PluginData/01_Mercury/Kopernicus/Mercury_Biomes.dds
            Biomes
            {
                Biome { name = Lowlands;      value = 1; color = RGBA(0,255,255,255)   }
                Biome { name = Highlands;     value = 1; color = RGBA(73,255,255,255)  }
                Biome { name = Young Craters; value = 1; color = RGBA(255,255,255,255) }
            }
            ScienceValues
            {
                landedDataValue      = 7
                inSpaceLowDataValue  = 6
                inSpaceHighDataValue = 5.5
                recoveryValue        = 6
                flyingAltitudeThreshold = 27000
                spaceAltitudeThreshold  = 2000000
            }
        }

        ScaledVersion
        {
            type = Vacuum
            fadeStart = 100000
            fadeEnd   = 102000
            Material
            {
                texture  = Sol-Textures/PluginData/01_Mercury/Kopernicus/Mercury_Dummy.dds
                normals  = Sol-Textures/PluginData/_Misc/Kopernicus/Blank_Normal.dds
                shininess = 0.0
                specular  = 0,0,0,1
            }
        }

        PQS
        {
            maxQuadLengthsPerFrame = 0.03
            minLevel = 2
            maxLevel = 13
            minDetailDistance = 12
            deactivateAltitude = 167000
            fadeStart = 102000
            fadeEnd   = 127000
            materialType = AtmosphericTriplanarZoomRotation
            Mods
            {
                Parallax { subdivisionLevel = 8; subdivisionRadius = 500; order = 999999 }
                VertexColorMap
                {
                    map     = Sol-Textures/PluginData/01_Mercury/Kopernicus/Mercury_Color.dds
                    order   = 10
                    enabled = true
                }
                VertexHeightMapBicubic
                {
                    map                    = Sol-Textures/PluginData/01_Mercury/Kopernicus/Mercury_VertexHeight.dds
                    offset                 = 0
                    deformity              = 20578.0
                    scaleDeformityByRadius = false
                    order   = 20
                    enabled = true
                }
            }
        }
    }
}
```

---

## Sol Source — Earth (atmospheric, key excerpts)

Source: `Sol-Configs/Configs/03_Earth-System/03_Earth/Earth-Kopernicus.cfg`

ScaledVersion and Atmosphere only. PQS structure is identical to Mercury.

```cfg
ScaledVersion
{
    type = Atmospheric
    Material
    {
        texture   = Sol-Textures/PluginData/03_Earth/Kopernicus/Earth_Dummy.dds
        normals   = Sol-Textures/PluginData/_Misc/Kopernicus/Blank_Normal.dds
        shininess = 0.2
        specular  = 0.5,0.5,0.5,1
        rimPower  = 2.4
        rimBlend  = 1.1
        Gradient
        {
            0.0 = 0.45,0.55,0.7,1.0
            0.3 = 0.2,0.15,0.05,1.0
            0.6 = 0.0,0.0,0.0,1.0
            1.0 = 0.0,0.0,0.0,1.0
        }
    }
}

Atmosphere
{
    enabled  = True
    oxygen   = True
    adiabaticIndex      = 1.4
    atmosphereDepth     = 140000
    atmosphereMolarMass = 0.0289644
    ambientColor = 0.243,0.251,0.255,1
    lightColor   = 0.65,0.57,0.475,0.5
    addAFG       = True
    temperatureSeaLevel = 288
    temperatureCurve
    {
        key = 0      282.5  0       -0.0025
        key = 8000   240.5  -0.006  -0.006
        key = 15000  212    -0.0025 -0.0025
        key = 30000  228    0.002   0.002
        key = 80000  256    0.009   0
        key = 140000 560    0.007   0
    }
    pressureCurve
    {
        key = 0      101.325  0        -0.0119729
        key = 10000  27.4635  -0.004   -0.004
        key = 30000  1.208    -0.00018 -0.00018
        key = 80000  0.00107  -1.8E-7  -1.8E-7
        key = 140000 0        0        0
    }
}
```
