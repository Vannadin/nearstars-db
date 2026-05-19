# Star Body CFG

Reference: `RSS-Reborn/Sol-Configs` → `Sol-Configs/Configs/00_Sol-Kopernicus.cfg`

## Top-Level Fields

```cfg
Body
{
    name = Proxima
    identifier = NearStars/Proxima
    barycenter = False
    finalizeOrbit = False
    flightGlobalsIndex = 2000             // must be globally unique
    cacheFile = ParallaxContinued/Models/ScaledMesh.bin
    Template
    {
        name = Sun
        removeAllPQSMods = True
    }
}
```

## Properties

```cfg
Properties
{
    displayName = Proxima Centauri
    description = ...
    radius = 107218000                    // meters
    gravParameter = 1.0869E+19            // m³/s² (GM)
    rotates = True
    rotationPeriod = 7480800              // seconds
    tidallyLocked = False
    initialRotation = 0
    inverseRotThresholdAltitude = 100000
    albedo = 0
    emissivity = 0.99
    coreTemperatureOffset = 0
    sphereOfInfluence = Infinity
    solarRotationPeriod = False
    navballSwitchRadiusMult = 0.06
    navballSwitchRadiusMultLow = 0.055
    useTheInName = False
    selectable = True
    RnDVisibility = Visible
    ScienceValues
    {
        inSpaceLowDataValue  = 8
        inSpaceHighDataValue = 3
        recoveryValue        = 5
        spaceAltitudeThreshold = 5E+08
    }
}
```

## ScaledVersion

```cfg
ScaledVersion
{
    type = Star
    fadeStart = 0
    fadeEnd = 0
    Light
    {
        sunlightColor          = 1.0,0.5,0.3,1
        sunlightShadowStrength = 0.75
        scaledSunlightColor    = 1.0,0.5,0.3,1
        IVASunColor            = 1.0,0.5,0.3,1
        ambientLightColor      = 0.04,0.02,0.01,1
        sunLensFlareColor      = 1.0,0.5,0.3,1
        givesOffLight          = True
        sunAU                  = 13599840256
        luminosity             = 0.0017              // relative (Sol = 1360)
        insolation             = 0.15
        radiationFactor        = 1
        brightnessCurve
        {
            key = -0.01573471 0.217353 1.706627 1.706627
            key = 5.084181 3.997075 -0.001802375 -0.001802375
            key = 38.56295 1.82142 0.0001713 0.0001713
        }
        IntensityCurve
        {
            key = 0 0.9 0 0
            key = 1 0.9 0 0
            key = 1.49597871e11 0.9 0 0
            key = 1.49597871e12 0.9 0 0
            key = 1.49597871e13 0 0 0
        }
        ScaledIntensityCurve
        {
            key = 0 1 0 0
            key = 1000000 1 0 0
            key = 10000000 0 0 0
        }
        IVAIntensityCurve
        {
            key = 0 0.8 0 0
            key = 1 0.8 0 0
        }
    }
    Material
    {
        emitColor0   = 0.8,0.4,0.2,1
        emitColor1   = 0.7,0.35,0.15,1
        rimColor     = 0.9,0.4,0.2,1
        rimPower     = 0.8
        rimBlend     = 4.0
        noiseMap     = NearStars-Textures/PluginData/ProximaCentauri/Kopernicus/Proxima_Sunspots.dds
        sunspotTex   = NearStars-Textures/PluginData/ProximaCentauri/Kopernicus/Proxima_Sunspots.dds
        sunspotPower = 1
        sunspotColor = 1,1,1,1
    }
    Coronas
    {
        Value
        {
            scaleSpeed     = 0.007
            scaleLimitY    = 5
            scaleLimitX    = 5
            updateInterval = 5
            speed          = -1
            rotation       = 0
            Material
            {
                texture      = NearStars-Textures/PluginData/ProximaCentauri/Kopernicus/Proxima_Corona.dds
                mainTexScale = 1,0.9
            }
        }
    }
}
```

---

## Sol reference (star — Sun)

For the complete Sol-Configs Sun cfg, see:
[`Sol-Configs/Configs/00_Sol-Kopernicus.cfg`](https://github.com/RSS-Reborn/Sol-Configs/blob/main/Sol-Configs/Configs/00_Sol-Kopernicus.cfg)
(raw: https://raw.githubusercontent.com/RSS-Reborn/Sol-Configs/main/Sol-Configs/Configs/00_Sol-Kopernicus.cfg).

The standard KSP-Kopernicus pattern for a star body is:

```cfg
@Kopernicus:FOR[YourPack]
{
    Body
    {
        name                = <StarName>
        identifier          = YourPack/<StarName>
        flightGlobalsIndex  = <unique integer>
        Template            { name = Sun; removeAllPQSMods = True }

        Properties
        {
            radius            = <m>
            gravParameter     = <m^3/s^2>
            rotationPeriod    = <s>
            sphereOfInfluence = Infinity
        }

        ScaledVersion
        {
            type      = Star
            fadeStart = 0
            fadeEnd   = 0
            Light
            {
                sunAU       = <m, distance to '1 AU' reference>
                luminosity  = <W/m^2 at sunAU, used for stock light falloff>
                brightnessCurve     { ... }
                IntensityCurve      { ... }
                ScaledIntensityCurve{ ... }
                IVAIntensityCurve   { ... }
            }
            Material { noiseMap = ...; emitColor0 = ...; rimColor = ...; ... }
            Coronas  { Value { Material { texture = ... } } }
        }
    }
}
```

Sun physical constants (R ≈ 6.957e8 m, GM ≈ 1.3271244e20 m³/s²,
sidereal period ≈ 25.38 d) are public-domain values from IAU 2015 and
the NASA Sun Fact Sheet
(https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html).
Sol-Configs' specific brightness/intensity curves are tuned for KSP
visual presentation and are at the raw URL above.
