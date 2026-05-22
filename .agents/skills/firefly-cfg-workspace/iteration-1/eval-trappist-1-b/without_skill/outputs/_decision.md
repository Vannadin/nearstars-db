# Trappist1b — Firefly cfg decision: SKIP (no cfg written)

## Decision
No Firefly cfg should be written for `Trappist1b`. The body is airless.

## Why Firefly is not applicable
Firefly (M1rageDev) is a re-entry plasma / atmospheric heating
effects mod. Every shipped example cfg in
`GameData/Firefly/Configs/{Stock,RSS,OPM,Kcalbeloh,KSRSS,MPE}`
targets a body with a non-trivial atmosphere (Kerbin, Eve, Duna,
Jool, Earth, Venus, Mars, Titan, Jupiter, Saturn, Uranus, Neptune).
Airless bodies (Mun, Minmus, Moho, Dres, Gilly, Bop, Pol, the Joolian
ice moons, Mercury, the Moon, Pluto, etc.) ship no Firefly cfg.

A re-entry plasma envelope requires gas to ionize and a measurable
dynamic pressure on the vehicle. With surface pressure = 0 Pa neither
exists, so a `BODY { name = Trappist1b ... }` block would never be
exercised by the Firefly plugin (the trigger is `vessel.dynamicPressurekPa`
> threshold inside an atmosphere — see Firefly/Source/Firefly/
ModuleFirefly.cs).

## Phase 3 evidence (from docs/phase3/trappist-1-b.md)
- `atmosphere_present` = **false** (high confidence)
- `atmosphere_surface_pressure_pa` = **0**
- `atmosphere_composition` = n/a (airless)
- `atmosphere_scale_height_km` = n/a
- `atmospheric_shielding_g_cm2` = 0

Observational basis: Ducrot 2025 (arXiv:2509.02128) MIRI 15 μm phase
curve excludes ≳1 bar atmospheres; Ih 2023 (arXiv:2305.10414) rules
out CO₂ atmospheres > 0.3 bar at 3σ; Greene 2023 (arXiv:2303.14849)
dayside brightness temperature of ~503 K matches a bare ultramafic
rock; cross-system consistency with c's lack of CO₂ (Zieba 2023)
removes the only Ducrot-2024-allowed thick-CO₂ alternative.

## Re-evaluate if
- A future JWST result revises the upper limit *upward* and a CO₂
  atmosphere ≳ 0.1 bar becomes viable again (currently the literature
  is converging the other way — see Ducrot 2025, Allen 2025).
- A `cfg variant` for the "thick CO₂ + photochemical haze" branch
  is later promoted from Phase 3.5 alternative to the primary
  interpretation; in that case a Firefly cfg derived from the Venus
  template would be appropriate.
