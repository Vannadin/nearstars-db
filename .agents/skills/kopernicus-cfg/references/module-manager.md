# Module Manager Patch Syntax

Reference: `sarbian/ModuleManager` wiki

## NearStars patch header

```cfg
@Kopernicus:FOR[NearStarsSystem]
{
    Body { ... }
}
```

- `FOR[NearStarsSystem]` — runs after all `:AFTER[]` patches, ensures NearStars bodies exist before other mods patch them
- One `@Kopernicus` block per cfg file is conventional; multiple bodies can share one block

## Conditional patches (NEEDS)

```cfg
// Runs only if Scatterer is installed
@Kopernicus:FOR[NearStarsSystem]:NEEDS[Scatterer]
{
    ...
}

// Runs only if both Parallax and NearStars are installed
@Kopernicus:FOR[NearStarsSystem]:NEEDS[Parallax]
{
    ...
}

// Runs if EVE-Redux OR EVE Volumetrics is installed
@Kopernicus:FOR[NearStarsSystem]:NEEDS[EnvironmentalVisualEnhancements]
{
    ...
}
```

## Patching existing bodies (Sol compatibility)

```cfg
// Add NearStars data to an existing Sol body
@Kopernicus:FOR[NearStarsSystem]:NEEDS[SolSystem]
{
    @Body[Earth]
    {
        @Properties
        {
            %someNearStarsField = value
        }
    }
}
```

## Removing stock bodies (Sol does this)

```cfg
@Kopernicus:FOR[SolSystem]
{
    !Body[Kerbin] {}
    !Body[Mun] {}
    !Body[Minmus] {}
}
```

## Scale patches (Rescale compatibility)

```cfg
// Quarter scale
@Body[ProximaB]:NEEDS[NearStarsSystem,Rescale125]:FOR[NearStars_Rescale]
{
    @Properties
    {
        @radius *= 0.25
    }
    @Orbit
    {
        @semiMajorAxis *= 0.25
    }
}
```

## Common operators

| Operator | Meaning |
|----------|---------|
| `@Node` | Edit existing node |
| `%key = value` | Set (create or overwrite) |
| `@key = value` | Edit existing key only |
| `!key,*` | Delete all matching keys |
| `#key` | Rename |
| `+Node` | Copy node |
| `:NEEDS[X]` | Conditional — mod X must be installed |
| `:FOR[X]` | Run pass for mod X |
| `:AFTER[X]` | Run after mod X's FOR pass |
| `:BEFORE[X]` | Run before mod X's FOR pass |
| `:FINAL` | Run last, after everything |
