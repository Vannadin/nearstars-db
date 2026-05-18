# Binary / Multiple Star System — Barycenter CFG

Reference: Real Exoplanets (REX) → `AlphaCentauriSystem/Alpha Centauri Barycenter.cfg`

## How it works

- `barycenter = true` — marks body as unselectable
- `ScaledVersion { invisible = True }` — hides it visually (`barycenter = true` alone is not enough)
- Assign combined mass of all stars to the barycenter → realistic gravity from outside the system
- Set `sphereOfInfluence` manually to enclose all member stars
- `hiddenRnD = True` — keeps barycenter out of R&D archive
- Template: `Jool` + `removeAtmosphere = true` + `removeCoronas = true`

## Barycenter body

```cfg
@Kopernicus:FOR[NearStars]
{
    Body
    {
        name = AlphaCenBary               // used as referenceBody by member stars
        barycenter = true
        finalizeOrbit = false
        flightGlobalsIndex = 3000         // see file-structure.md for NearStars ranges
        cacheFile = ParallaxContinued/Models/ScaledMesh.bin

        Template
        {
            name = Jool
            removeAtmosphere = true
            removeCoronas = true
        }

        Orbit
        {
            referenceBody            = Sun
            semiMajorAxis            = 4.132E+13   // meters — Alpha Cen ~4.37 ly
            eccentricity             = 0
            inclination              = 0
            meanAnomalyAtEpochD      = 0
            longitudeOfAscendingNode = 0
            argumentOfPeriapsis      = 0
            epoch                    = 0
            color                    = 1.0,0.9,0.8,1
            icon                     = ALL
            iconTexture = NearStars-Textures/PluginData/AlphaCen/Kopernicus/AlphaCen_Icon.png
        }

        Properties
        {
            displayName = α Centauri
            description = ...
            radius               = 1E+11          // dummy radius — never rendered
            mass                 = <M_A + M_B kg> // combined mass of all member stars
            sphereOfInfluence    = <calculated>   // enclose all member star orbits
            hiddenRnD            = True
        }

        ScaledVersion
        {
            invisible = True
            Light { givesOffLight = False }
        }
    }
}
```

## Member stars — orbiting the barycenter

```cfg
@Kopernicus:FOR[NearStars]
{
    Body
    {
        name = AlphaCenA
        // ... see star-body.md for Properties, ScaledVersion, Light, Coronas

        Orbit
        {
            referenceBody            = AlphaCenBary   // barycenter name
            semiMajorAxis            = <a × M_B / (M_A + M_B)>   // meters
            eccentricity             = 0.5179
            inclination              = <observed value>
            meanAnomalyAtEpochD      = 0
            longitudeOfAscendingNode = <observed value>
            argumentOfPeriapsis      = <observed value>
            epoch                    = 0
        }
    }
}
```

```cfg
@Kopernicus:FOR[NearStars]
{
    Body
    {
        name = AlphaCenB
        // ...

        Orbit
        {
            referenceBody            = AlphaCenBary
            semiMajorAxis            = <a × M_A / (M_A + M_B)>
            // same orbital plane as A; 180° phase offset
            meanAnomalyAtEpochD      = 180
        }
    }
}
```

## Mass and SOI calculations

**Barycenter mass:**
```
mass_kg = (M_A_msun + M_B_msun) × 1.989e+30
```

**Each star's distance from barycenter:**
```
r_A = a_total × M_B / (M_A + M_B)
r_B = a_total × M_A / (M_A + M_B)
```
`a_total` = mean separation between the two stars in meters

**Barycenter SOI (Hill sphere):**
```
r_Hill = a_sys × (M_bary / (3 × M_sun))^(1/3)
```
`a_sys` = barycenter's semi-major axis around Sol. Use result as `sphereOfInfluence`.

## Planet placement

Planets orbit their **host star**, not the barycenter:

```cfg
Orbit { referenceBody = AlphaCenB; semiMajorAxis = ...; ... }
```

## Notes

- Both `barycenter = true` and `ScaledVersion { invisible = True }` are required — neither alone is sufficient
- `radius = 1E+11` is a dummy value; the body is never rendered
- Triple systems (e.g. GJ 667 A/B/C): create an A-B barycenter first, then have C orbit that barycenter
