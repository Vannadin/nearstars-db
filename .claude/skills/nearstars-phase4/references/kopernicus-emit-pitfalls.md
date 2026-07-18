# Kopernicus emit pitfalls — the curve/map facets that bite the gate

Lifted from `phase4/_audit/facet-checklist.md` (α Cen appendix) because it is reusable
cross-body knowledge, not α-Cen-specific. Many facets emit as **curves/maps, not
scalars**, generated at emit from anchors + models, and take Phase 4 choices as
INPUTS (obliquity → axial curve, e → eccentricity curve, tidal-lock → longitude
heat). Schema authority = the `kopernicus-cfg` skill refs. These matter at the
**gate**: e.g. an e≈0 choice silently deletes the atmosphere at emit.

## Atmosphere thermal model (`atmosphere.md`)

A static curve lookup baked at config time (does NOT read luminosity/distance —
that is the separate auto solar-flux channel). Curves: `temperatureCurve`(alt) +
`pressureCurve`(alt) + offsets `temperatureSunMultCurve`,
`temperatureLatitudeBiasCurve`(poles), `temperatureLatitudeSunMultCurve`(day/night),
`temperatureAxialSunBiasCurve`(true-anomaly season; ← **obliquity** input)
×`…AxialSunMultCurve`(lat), `temperatureEccentricityBiasCurve`(← **heliocentric e**).

- ⚠️ **eccentricity-curve divide-by-zero**: it normalizes by (ApR−PeR); on e≈0
  the body **silently loses its atmosphere**. Emit ONLY when e ≳ 0.02–0.05
  (Polyphemus e=0.1 ok; a default-circular body: never — flag suppression or a
  synthetic-e floor). **This is a gate consideration**, not just an emit detail.
- For a **moon**, the eccentricity curve reads the **parent planet's** orbit
  position → one curve on the moon captures the parent's heliocentric great-season.

## Tidal-lock temperature — locked to the planet, not the star

A moon locked to its planet (not the star) does NOT get the star-lock flattening
(`atmosphere.md`: flatten LatitudeSunMult + high LatitudeBias). It has a normal
day/night vs the star. Its temperature still varies via three channels:
(1) great-season — `temperatureEccentricityBiasCurve` reads the **parent's** orbit;
(2) day/night — sun-facing side rotates once per orbit (`temperatureSunMultCurve`);
(3) eclipse cooling — auto real-flux drop in the planet's shadow. Only the
**sub-planet hemisphere** is fixed (a hazardousBody `LongitudeCurve` at the locked
face); planetshine/IR warming is non-native KSP (cosmetic/flag).

## HazardousBody heat (`hazardous-body.md`) — [verified vs Kopernicus source]

- base = **`ambientTemp`** — ⚠️ **NOT `heat`**; the repo's `hazardous-body.md` ref
  is wrong, fix before emit.
- × `AltitudeCurve` (⚠️ input = **center-distance in scene units**, not ASL alt)
  × `LatitudeCurve` × `LongitudeCurve` (body-fixed → pins a fixed face)
  × `HeatMap` (body-fixed); + `sumTemp` bool (add vs replace); `biomeName` filter.

## Biomes + science (`planet-body.md`)

`biomeMap` (⚠️ **R-channel only**, `RGBA(n,255,255,255)`) + `Biomes` +
`ScienceValues`. ⚠️ **A gas giant DOES carry a biome map** (Jool / RSS Jupiter
precedent) — an earlier "gas giant = no biome map" note misapplied the Sun.cfg
(star) pattern. With no surface you can't land, but the map still defines
**atmospheric flight biomes** ("flying over X"). Define the FULL `ScienceValues`
block even where landed/splashed are inert/unreachable.

## Other

- **Star Light** (`star-body.md`) — `IntensityCurve` (distance → brightness).
- **Ocean** (`ocean.md`) — OceanFX tuning curves.
- **PQS terrain** (`pqs-terrain.md`) — heightmaps/noise (art/terrain pass).
- **Misc** — `timewarpAltitudeLimits` (array), `sphereOfInfluence` (manual for
  binaries/moons).

## Multi-star flux — [verified]

In-flight **heating** flux scales with real luminosity/distance every frame,
**summed over A+B** + eclipse-occluded (hard umbra, no penumbra) — independent of
the cosmetic temperature curves. ⚠️ But **solar-PANEL power is STOCK**: it tracks
only the single brightest *active* star (not the A+B sum, separate eclipse logic).
Design power budgets around one sun.
