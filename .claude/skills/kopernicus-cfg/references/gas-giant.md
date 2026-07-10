# Gas Giant Body CFG

Reference: `RSS-Reborn/Sol-Configs` → `Sol-Configs/Configs/05_Jupiter-System/05_Jupiter/Jupiter-Kopernicus.cfg`

## Key characteristics vs rocky planets

- Template is `Mun` + `removeAllPQSMods = True` (not `Jool` — Sol uses Mun as a clean base)
- PQS block is present but `deformity = 0` — renders cloud color texture only, no terrain displacement
- Atmosphere is extremely deep — curve data below is from Sol Jupiter Galileo probe; scale to match actual planet
- Rings use `backlitTexture` (separate texture for unlit face) and `steps = 16384`
- `AtmosphereFromGround` subnode controls the scattering shell radius independently of `atmosphereDepth`

## Full cfg (NearStars placeholder — Sol Jupiter values as reference)

```cfg
@Kopernicus:FOR[NearStarsSystem]
{
    Body
    {
        name = GasGiantName
        identifier = NearStars/GasGiantName
        finalizeOrbit = false
        flightGlobalsIndex = 1XXX             // NearStars range, 1000+ — see file-structure.md
        cacheFile = ParallaxContinued/Models/ScaledMesh.bin

        Template
        {
            name = Mun
            removeAllPQSMods = true
        }

        Orbit
        {
            referenceBody               = Sun
            semiMajorAxis               = 778343793651.4404   // 5.2 AU
            eccentricity                = 0.04832471317106279
            inclination                 = 1.3048279272665066
            meanAnomalyAtEpochD         = 332.9883674471718
            longitudeOfAscendingNode    = 100.3930097175018
            argumentOfPeriapsis         = 274.00170198072
            epoch                       = 0
            color                       = 0.857,0.745,0.552,1
            iconTexture = NearStars-Textures/PluginData/<BodyName>/Kopernicus/Jupiter_Icon.png
            icon = ALL
        }

        Properties
        {
            displayName = Gas Giant Name
            description = ...

            radius = 66316000                     // 1000 bar reference surface; 1 bar surface = ~69911 km
            gravParameter = 1.266865319E+17       // m³/s²
            rotationPeriod = 35729.711            // 9h 55m 29.711s
            rotates = true
            tidallyLocked = false
            initialRotation = -100
            solarRotationPeriod = False
            albedo = 0.343
            emissivity = 0.657

            biomeMap = NearStars-Textures/PluginData/<BodyName>/Kopernicus/Jupiter_Biomes.dds
            // color may be any RGB (e.g. `color = #C9A26B`) as long as it exactly matches the
            // biomeMap pixel; the R-channel-only RGBA(n,255,255,255) below is just one convention.
            Biomes
            {
                Biome { name = Equatorial Bands;    value = 1; color = RGBA(0,255,255,255)   }
                Biome { name = Great Red Spot;      value = 1; color = RGBA(51,255,255,255)  }
                Biome { name = South Temperate Bands; value = 1; color = RGBA(102,255,255,255) }
                Biome { name = South Polar Bands;   value = 1; color = RGBA(153,255,255,255) }
                Biome { name = North Temperate Bands; value = 1; color = RGBA(204,255,255,255) }
                Biome { name = North Polar Bands;   value = 1; color = RGBA(255,255,255,255) }
            }

            ScienceValues
            {
                flyingLowDataValue   = 8
                flyingHighDataValue  = 7.5
                inSpaceLowDataValue  = 7
                inSpaceHighDataValue = 6
                recoveryValue        = 7
                flyingAltitudeThreshold = 186000
                spaceAltitudeThreshold  = 40000000
            }
        }

        ScaledVersion
        {
            type = Atmospheric
            fadeStart = 1800000
            fadeEnd   = 1900000
            Material
            {
                texture   = NearStars-Textures/PluginData/<BodyName>/Kopernicus/Jupiter_Dummy.dds
                normals   = NearStars-Textures/PluginData/_Misc/Kopernicus/Blank_Normal.dds
                shininess = 0.05
                specColor = 0,0,0.1,1
                rimPower  = 2.0
                rimBlend  = 1.1
                Gradient
                {
                    0.0 = 0.35,0.40,0.45,1.0
                    0.2 = 0.10,0.15,0.20,1.0
                    0.4 = 0.00,0.00,0.00,1.0
                    1.0 = 0.00,0.00,0.00,1.0
                }
            }
        }

        Atmosphere
        {
            enabled = true
            oxygen  = false
            adiabaticIndex      = 1.4775           // H₂/He mixture from Galileo data
            atmosphereMolarMass = 0.0022105         // kg/mol
            ambientColor = 0.10,0.05,0.10,1
            lightColor   = 0.680,0.674,0.626,0.5
            staticPressureASL = 101325             // Pa at reference surface

            temperatureSeaLevel = 166              // K at 1-bar cloud level

            // Pressure curve: Galileo probe data (Pa vs altitude in meters)
            // Zero altitude = 1000 bar reference point (deep interior)
            // 1 bar level ≈ 380,000 m
            pressureCurve
            {
                key = 0      98078.6  -1.96157   -1.96157
                key = 100000 20568.6  -0.30853   -0.30853
                key = 250000 2208.53  -0.034141  -0.034141
                key = 380000 101.325  -0.004095  -0.004095   // ~1 bar (cloud tops)
                key = 440000 4.4322   -0.0003026 -0.0003026
                key = 600000 0.005674 -2.565E-07 -2.565E-07
                key = 1000000 1.5E-06 -1.247E-11 -1.247E-11
                key = 1550000 5.28E-08 -2.64E-13 -2.64E-13
            }

            // Temperature curve: complex stratosphere inversion + thermosphere rise
            temperatureCurve
            {
                key = 0      152    0.12047  0.12047   // deep interior (fudge for emissivity)
                key = 250000 426.5  -0.00205 -0.00205
                key = 380000 166.1  -0.00201 -0.00201  // ~1 bar cloud tops ~166 K
                key = 420000 113.2  -0.000125 -0.000125 // tropopause minimum
                key = 460000 143.8  0.000885 0.000885  // stratosphere warming
                key = 700000 195.2  0.000425 0.000425
                key = 800000 393.2  0.00284  0.00284   // thermosphere
                key = 1200000 884.4 0.000205 0.000205
                key = 1550000 915.9 3.6E-05  3.6E-05
            }

            temperatureSunMultCurve
            {
                key = 0      0 0 0
                key = 538000 0 0 0
                key = 576000 1 5E-06 5E-06
                key = 1550000 4 0 0
            }
            temperatureLatitudeBiasCurve
            {
                key = 0  0  0 0
                key = 90 -3 0 0
            }
            temperatureLatitudeSunMultCurve
            {
                key = 0  3 0 0
                key = 90 0 0 0
            }
            temperatureAxialSunBiasCurve
            {
                key = 0   0.017452  0        0.017451
                key = 89  1         0        0
                key = 179 0        -0.017453 -0.017453
                key = 269 -1        0        0
                key = 359 0         0.017453  0.017453
                key = 360 0.017452  0.017451  0
            }
            temperatureAxialSunMultCurve
            {
                key = 0  0 0 0.018
                key = 90 1 0 0
            }
            temperatureEccentricityBiasCurve
            {
                key = 0 2  0  -4
                key = 1 -2 -4  0
            }

            // Scattering shell — separate from atmosphereDepth
            AtmosphereFromGround
            {
                innerRadius = 69211890   // meters (just below 1-bar radius)
                outerRadius = 70981000   // meters
                waveLength  = 0.505,0.52,0.55,1.0
            }
        }

        Rings
        {
            Ring
            {
                angle = 0
                longitudeOfAscendingNode = 0
                texture        = NearStars-Textures/PluginData/_Misc/Kopernicus/Transparent.png
                backlitTexture = NearStars-Textures/PluginData/<BodyName>/Kopernicus/Jupiter_RingsUnlitSide.dds
                innerRadius = 1046.097   // multiplier of body radius
                outerRadius = 3423.005
                color = 1,1,1,1
                unlit = False
                useNewShader = True
                penumbraMultipler = 1000.0
                lockRotation = True
                steps = 16384
                albedoStrength  = 1
                scatteringStrength = 1
                anisotropy = 0.9
                fadeoutMinAlpha = 1
            }
        }

        // Gas giants still have a PQS block — used to render the cloud color texture.
        // deformity = 0 means no actual terrain displacement.
        PQS
        {
            materialType = AtmosphericTriplanarZoomRotation
            maxQuadLengthsPerFrame = 0.03
            minLevel = 2
            maxLevel = 8
            minDetailDistance = 12
            fadeStart = 2000000
            fadeEnd   = 2100000
            deactivateAltitude = 2200000       // must be > fadeEnd
            Material
            {
                factor           = 6
                factorBlendWidth = 0.01
                factorRotation   = 30
                saturation       = 0.4
                contrast         = 2.5
                tintColor        = 1,1,1,0
                specularColor    = 0,0,0,0
                albedoBrightness = 1.8
                // steep/low/mid/high tex fields — use BUILTIN textures as placeholders
                steepTex  = BUILTIN/gillySteep_diffuse
                steepBumpMap = BUILTIN/gillySteep_nrm
                lowTex    = BUILTIN/ikeGround_diffuse
                midTex    = BUILTIN/ikeGround_diffuse
                midBumpMap = BUILTIN/ikeGround_nrm
                highTex   = BUILTIN/ikeGround_diffuse
                lowStart  = -1; lowEnd = -1
                highStart = 2;  highEnd = 2
                lowTiling = 70000; midTiling = 50000; highTiling = 70000
                steepTexStart = 20000; steepTexEnd = 30000
                globalDensity = 1; planetOpacity = 1; oceanFogDistance = 1000
            }
            Mods
            {
                Parallax
                {
                    subdivisionLevel  = 4
                    subdivisionRadius = 500
                    order = 999999
                }
                VertexColorMap
                {
                    map     = NearStars-Textures/PluginData/<BodyName>/Kopernicus/Jupiter_Color.dds
                    order   = 99993
                    enabled = true
                }
                VertexHeightMapBicubic
                {
                    map                    = NearStars-Textures/PluginData/<BodyName>/Kopernicus/Jupiter_VertexHeight.dds
                    offset                 = -537926.82   // negative offset pushes surface below sea level
                    deformity              = 0            // no terrain displacement
                    scaleDeformityByRadius = false
                    order   = 10
                    enabled = true
                }
            }
        }

        Debug
        {
            exportMesh = True
            update     = False
        }
    }
}
```

## Notes

- `radius` is the 1000-bar reference surface, not the visible cloud top (1 bar ≈ 69,911 km for Jupiter)
- `VertexHeightMapBicubic.offset` is large and negative to keep the visual surface below the reference radius
- `AtmosphereFromGround` sets the scattering shell independently of `atmosphereDepth`
- Rings: `innerRadius`/`outerRadius` are **multipliers** of body radius, not meters
- `backlitTexture` renders the ring's unlit face separately — omit for simple rings
- Pressure curve data source: Galileo probe ASI (1995); altitude zero = 1000-bar level
