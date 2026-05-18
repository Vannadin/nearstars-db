# HazardousBody Node CFG

Reference: Kopernicus Wiki → `kopernicuswiki.github.io/main/HazardousBody.html`

`HazardousBody {}` is a **top-level Body subnode** (sibling of Atmosphere, PQS, etc.) that applies continuous heat damage to vessels on or near the surface. Use it for extreme environments: lava worlds, high-radiation bodies, crushingly hot planets.

> Note: heat damage inside a liquid ocean uses `HazardousOcean` inside `Ocean.Mods` instead — see `ocean.md`.

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `heat` | Double | Base heat applied per interval (in game heat units) |
| `interval` | Single | Seconds between each heat application |
| `AltitudeCurve` | FloatCurve | Multiplier on `heat` at a given altitude (meters). Key format: `altitude multiplier` |
| `LatitudeCurve` | FloatCurve | Multiplier on `heat` at a given latitude (degrees, 0 = equator, 90 = pole) |
| `LongitudeCurve` | FloatCurve | Multiplier on `heat` at a given longitude (degrees) |
| `HeatMap` | File Path | Grayscale DDS — black = 0×, white = 1× multiplier on `heat`. Overrides or combines with curves |

All curve multipliers stack multiplicatively with each other and with `heat`.

## Example — volcanic lava world

Heat is extreme at low altitude and near the equator, survivable in polar highlands.

```cfg
@Kopernicus:FOR[NearStars]
{
    Body
    {
        name = Ignis
        // ... other nodes ...

        HazardousBody
        {
            heat     = 1.0      // base heat per interval
            interval = 0.5      // apply every 0.5 seconds

            // Altitude: surface (0 m) = full heat, 30 km up = no heat
            AltitudeCurve
            {
                key = 0     1.0
                key = 5000  0.8
                key = 15000 0.3
                key = 30000 0.0
            }

            // Latitude: equator (0°) = full heat, poles (90°) = 20% heat
            LatitudeCurve
            {
                key = 0  1.0
                key = 45 0.6
                key = 90 0.2
            }

            // Longitude: uniform (no longitude variation)
            LongitudeCurve
            {
                key = 0   1.0
                key = 360 1.0
            }
        }
    }
}
```

## Example — radiation belt (high altitude danger zone)

Heat peaks at a specific altitude band, zero at surface and space.

```cfg
HazardousBody
{
    heat     = 2.0
    interval = 1.0

    AltitudeCurve
    {
        key = 0       0.0    // surface: safe
        key = 100000  0.0
        key = 200000  1.0    // radiation belt peak
        key = 400000  0.0    // above belt: safe again
    }

    LatitudeCurve   { key = 0 1.0; key = 90 1.0 }  // uniform by latitude
    LongitudeCurve  { key = 0 1.0; key = 360 1.0 }
}
```

## Example — HeatMap (fine-grained control)

Grayscale DDS: black pixels = 0 heat multiplier, white = 1.0. Useful for hot spots like volcanoes or specific terrain features.

```cfg
HazardousBody
{
    heat     = 1.5
    interval = 0.5
    HeatMap = NearStars-Textures/PluginData/Ignis/Kopernicus/Ignis_HeatMap.dds

    AltitudeCurve
    {
        key = 0     1.0
        key = 20000 0.0
    }
}
```

## Notes

- `heat` units are arbitrary — tune by playtesting. Values around 0.5–2.0 with `interval = 0.5` create noticeable but survivable danger for unshielded craft
- If no `LatitudeCurve` or `LongitudeCurve` is set, heat is uniform around the body
- `AltitudeCurve` alone is sufficient for most use cases (uniform surface danger)
- For tidally locked bodies, use `LongitudeCurve` to make the dayside hotter (0°/360° = sub-stellar point)
