# NearStars — Flux Tube Renderer (DEFERRED / future feature)

Status: **planned, not implemented.** Locked in as a future feature on 2026-06-01.
This is a prototype skeleton, **not compiled or tested** (no KSP/Unity DLLs in this repo).

## What it is

Renders the star↔planet magnetic **flux tube** for YZ Cet b — the visible analogue
of the confirmed SPI radio aurora (Pineda & Villadsen 2023; Trigilio 2023). Visually
kin to the *Project Hail Mary* Petrova line, but anchored pole-to-pole with a
near-dipole arc and footprint glows.

Why a C# plugin and not a `.cfg`: the declarative stack (Kopernicus / Scatterer /
EVE / Firefly) only attaches effects to a single body. Drawing a glowing curve
between two *moving* bodies needs a per-frame `ScaledSpace` `LineRenderer`.

## Files

- `FluxTubeRenderer.cs` — the prototype. ScaledSpace LineRenderer, dipole bezier,
  magnetic pole ≈ `bodyTransform.up`, brightness keyed to `orbit.trueAnomaly`,
  alpha bright at both poles → faint at center.

## Done in the skeleton

- ScaledSpace correctness (layer 10, `LocalToScaledSpace`, width `/ScaleFactor`).
- Orbital-phase brightness pulse (the SPI burst physics).
- Pole→center alpha falloff gradient + flowing texture scroll.

## TODO before it ships

- Verify additive shader name + `_TintColor` property against live KSP.
- Match `StarName`/`PlanetName` to the real Kopernicus `CelestialBody.name`.
- Tracking Station scene (currently Flight + KSC only).
- Footprint billboard quads at both poles.
- `.csproj` with refs (Assembly-CSharp, UnityEngine.*); output to `GameData/NearStars/Plugins/`.
- Move tunables (colors, bow, width) into a `.cfg` read via GameDatabase.

Companion visual reference: `/tmp/petrova-vs-fluxtube.svg` (Petrova line vs flux tube).
Pairs well with any future Principia C# work.
