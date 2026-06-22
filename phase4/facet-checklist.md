<!-- Phase 4 facet 커버리지 트래커 — 바디 × 전체 축 메뉴, 모든 facet에 오너가 최소 1번 선택했는지 추적 -->
# Phase 4 — Facet Coverage Checklist (α Centauri system)

The board (`alpha_centauri.yaml`) records only **decisions/deltas**, so it can't show
*coverage*. This tracker lists **every relevant axis** of the SPEC §0 menu per body, so no
facet is silently skipped (the owner makes ≥1 explicit call on each — see
`feedback_phase4_facet_choices`).

Status: ✅ gated · ▫ passthrough (confirm) · ∅ N/A for this body type · ⬜ **TODO**

## Alpha Centauri A b — Polyphemus (gas giant)
| group | axis | status |
|---|---|---|
| identity | body_type (gas giant) | ▫ |
| identity | designation (A b) / cultural (Polyphemus) | ✅ |
| identity | discoverability — ResearchBodies (candidate → observe to discover; star always visible) | ✅ |
| orbit | a / e / inclination | ✅ |
| orbit | Ω / ω / mean_anomaly (absolute) | ▫ (free emit-orientation) |
| orbit | lagrange_placement (Poly-L4/L5 co-orbital planetoids) | ✅ none (dropped 2026-06-22) |
| bulk | mass / radius / j2 / obliquity / rotation | ✅/▫ |
| bulk | spin_axis_orientation (pole) — free emit, eclipse-favorable | ✅ |
| bulk | internal_heat (T_int<110K) / age (inherited) | ▫ |
| atmosphere | composition / pressure / temperature | ▫ (Phase 3) |
| atmosphere | scale_height / greenhouse / escape | ▫ |
| atmosphere | breathability | ∅ |
| surface | (cloud-deck = appearance) | ∅ |
| appearance | banding / haze / aurora / rings | ✅ |
| appearance | clouds (Jovian turbulent banding + 1 mid-lat great storm) | ✅ |
| appearance | emission_glow / specular / artificial | ∅ |
| magnetism | magnetic_field / magnetosphere / belts | ✅ |
| environment | radiation | ✅ |
| environment | stellar_wind / activity / heliosphere / habitable_zone | ∅ (star-level) |
| rings | structure / composition / plane | ✅ |
| satellites | moons list | ✅ |
| satellites | co_orbitals (Poly-L4/L5 dropped) / dust_sources (Chaos→ring ✅) | ✅ none |
| gameplay | SOI auto / biome map (flight biomes: lat bands + great storm) / full ScienceValues / difficulty | ✅ |

## Dante — A b I (volcanic moonlet)
| group | axis | status |
|---|---|---|
| identity | body_type / designation (A b I) / cultural | ▫/✅ |
| identity | discoverability | ⬜ |
| orbit | a / e / inc (roster, stability-gated) | ✅ (via satellites) |
| orbit | Ω / ω / M | ▫ |
| bulk | mass / radius (8e21 / 900 km, invented) | ⬜ (affirm as Phase 4 row) |
| bulk | rotation (tidal-locked ~9.2 h) / obliquity / spin_axis | ⬜ (confirm lock) |
| bulk | tidal_heating | ✅ |
| atmosphere | composition / pressure (thin SO₂) | ✅ |
| atmosphere | breathability (no) / scale_height / escape | ▫ |
| surface | surface_type / tectonics / terrain (rift) | ✅ |
| surface | albedo / surface_temperature | ⬜ |
| surface | hydrosphere / ice_caps / biosphere | ∅ |
| appearance | surface look / emission_glow | ✅ |
| appearance | clouds / haze / aurora / specular / rings | ∅ |
| magnetism | magnetic_field (none) / magnetosphere | ⬜ (confirm none) |
| environment | radiation | ✅ |
| environment | stellar_wind / activity / heliosphere | ∅ |
| rings | (none) | ∅ |
| satellites | (none) | ∅ |
| gameplay | landing / biomes | ✅ |

## Hades — A b II (gray Ganymede-like)
| group | axis | status |
|---|---|---|
| identity | body_type / designation (A b II) / cultural | ✅ |
| identity | discoverability (fictional → RB `F F F F`) | ✅ |
| orbit | a / e / inc | ✅ (via satellites) |
| orbit | Ω / ω / M | ▫ |
| bulk | mass / radius (5e21 / 750 km, affirmed) | ✅ |
| bulk | rotation (locked 14.4h) / obliquity (~0) / spin_axis | ✅ |
| bulk | tidal_heating | ✅ |
| atmosphere | composition / breathability (none) | ▫ |
| surface | surface_type (rock, not ice) / tectonics (grooves) / terrain | ✅ |
| surface | albedo (0.30) / surface_temperature (~225K) | ✅ |
| surface | hydrosphere / ice_caps / biosphere | ∅ |
| appearance | surface look (Ganymede palette) | ✅ |
| appearance | emission_glow / clouds / aurora / specular / rings | ∅ |
| magnetism | magnetic_field (none) / magnetosphere | ✅ |
| environment | radiation | ✅ |
| rings / satellites | (none) | ∅ |
| gameplay | landing / biomes | ✅ |

## Pandora — A b III (Earth-like Na'vi homeworld) — **mostly TODO**
| group | axis | status |
|---|---|---|
| identity | body_type / designation (A b III) / cultural | ▫/✅ |
| identity | discoverability | ⬜ |
| orbit | a / e / inc (32 h lock, 252,393 km) | ✅ (via satellites) |
| orbit | Ω / ω / M | ▫ |
| bulk | mass (0.72 M⊕) / radius (5724 km) / gravity (0.8 g) | ⬜ (affirm canon) |
| bulk | rotation (32 h lock) / obliquity (29° canon) / spin_axis | ⬜ |
| bulk | tidal_heating / internal_heat | ⬜ (climate study exists) |
| atmosphere | composition (N₂/O₂/CO₂>18%/Xe/H₂S) | ⬜ |
| atmosphere | breathability (O₂ present, toxic) / pressure (1.1 atm) / scale_height / greenhouse | ⬜ |
| surface | surface_type / hydrosphere (oceans) / biosphere (lush, biolum) | ⬜ |
| surface | tectonics (volcanism, fast drift) / terrain (floating mtns) / ice_caps / albedo / surface_temp | ⬜ |
| appearance | base colour / clouds / biolum (cyan) / aurora / specular (oceans) / city-lights(Na'vi?) | ⬜ |
| magnetism | magnetic_field / magnetosphere | ✅ |
| magnetism | radiation_belts (between two belts) | ✅ (env note) |
| environment | radiation (between belts, shielded) | ⬜ (formalize Pandora row) |
| rings / satellites | (none) | ∅ |
| gameplay | biomes (incl. flux-vortex region) / SOI / difficulty | ⬜ (seed exists) |

## Stars A / B (context)
Activity / wind / heliosphere ▫ passthrough; magnetic_field ✅ (proxy); appearance
(color/granulation/spots/corona) ⬜ — deferred unless we do stellar appearance.

---
## Delicate Kopernicus emit values (curves / maps / pitfalls)
These facets emit as **curves/maps, not scalars** — generated at emit from anchors+models, with
real pitfalls. Schema authority = `kopernicus-cfg` skill refs. Many take our Phase 4 facet
choices as INPUTS (obliquity→axial curve, e→eccentricity curve, tidal-lock→longitude heat).

- **Atmosphere thermal model** (`atmosphere.md`) — a static curve lookup baked at config time
  (does NOT read luminosity/distance — that's the separate auto solar-flux channel). Curves:
  `temperatureCurve`(alt) + `pressureCurve`(alt) + offset terms `temperatureSunMultCurve`,
  `temperatureLatitudeBiasCurve`(poles), `temperatureLatitudeSunMultCurve`(day/night),
  `temperatureAxialSunBiasCurve`(true-anomaly season; ← **obliquity** input) ×`…AxialSunMultCurve`(lat),
  `temperatureEccentricityBiasCurve`(← **heliocentric e**; the great-season).
  - ⚠️ **eccentricity curve divide-by-zero**: normalizes by (ApR−PeR); on e≈0 → body silently
    loses its atmosphere. Emit ONLY when e ≳ 0.02–0.05 (Polyphemus e=0.1 ok; default-circular: never).
  - For a **moon** the eccentricity curve uses the **parent planet's** orbit position → one curve
    on Pandora captures Polyphemus's heliocentric great-season. (Kopernicus' own "Pandora" precedent.)
- **Tidal-lock temperature** — ⚠️ our moons are locked to **Polyphemus, not the star**, so the
  star-lock flattening (`atmosphere.md`: flatten LatitudeSunMult + high LatitudeBias) does NOT
  apply — they have a 9–32 h day/night vs the star (normal sun model). A locked moon's temperature
  STILL varies over its orbit via 3 channels: (1) **great-season** — `temperatureEccentricityBiasCurve`
  on a moon reads the **PARENT (Polyphemus)'s** orbit position → the moon inherits the 705-day
  heliocentric swing (this is how Pandora gets its ~15–25 K season); (2) **day/night** — the locked
  moon's sun-facing side rotates once per orbit → `temperatureSunMultCurve`/sunDot (auto); (3)
  **eclipse cooling** — auto real-flux drop in Polyphemus's shadow. Only the **sub-Polyphemus
  hemisphere** is fixed: Dante's sub-planet lava = hazardousBody `LongitudeCurve` at the locked
  face; planetshine/Polyphemus IR warming that hemisphere = non-native KSP (cosmetic/flag).
- **HazardousBody heat** (`hazardous-body.md`) — [VERIFIED 2026-06-22 vs Kopernicus source]
  base = **`ambientTemp`** (⚠️ NOT `heat` — our `hazardous-body.md` ref is WRONG, fix before emit)
  × `AltitudeCurve`(⚠️ input = **center-distance in scene units**, not ASL alt) × `LatitudeCurve`
  × `LongitudeCurve`(body-fixed `vessel.longitude` → pins a fixed face) × `HeatMap`(body-fixed);
  + `sumTemp` bool (add vs replace), `biomeName` filter. → Dante (sub-Polyphemus lava via
  LongitudeCurve at the locked face), Hades (mild).
- **Biomes + science** (`planet-body.md`) — `biomeMap` (⚠️ R-channel only, `RGBA(n,255,255,255)`) +
  `Biomes` + `ScienceValues`. → gameplay group + science-report text + Pandora flux-vortex biome.
  ⚠️ **CORRECTED 2026-06-22**: an earlier note claimed "gas giant = NO biome map" — that was the
  **Sun.cfg** (star) pattern misapplied. A **gas giant DOES carry a biome map** (Jool / RSS Sol
  Jupiter precedent): with no surface you can't land, but the biome map still defines **atmospheric
  flight biomes** ("flying over X"). Polyphemus → lat-band biomes + the great-storm eye as its own
  biome. Still define the FULL `ScienceValues` block (landed/splashed are token/inert, unreachable).
  Pandora (surfaced) gets a full biome map incl. the flux-vortex region.
- **Star Light** (`star-body.md`) — `IntensityCurve` etc. (distance→brightness) for A/B.
- **Ocean** (`ocean.md`) — OceanFX tuning curves → Pandora.
- **PQS terrain** (`pqs-terrain.md`) — heightmaps/noise → floating mountains, Dante chasma, Pandora terrain (art/terrain pass).
- **Misc** — `timewarpAltitudeLimits` (array), `sphereOfInfluence` (manual for binaries/moons).
- **Auto (not a curve)** [VERIFIED] — in-flight **heating** flux scales with real luminosity/distance
  every frame, **summed over A+B** + **eclipse-occluded** (Kopernicus raycast, hard umbra, no penumbra).
  Independent of the cosmetic temperature curves. ⚠️ But **solar-PANEL power is STOCK** — tracks only the
  single brightest *active* star (not the A+B sum, separate eclipse logic). Design power around one sun.

---
**TODO summary (fill systematically):** Polyphemus → ✅ FULL MENU WALKED (identity/orbit/bulk/atmosphere/magnetism/environment/rings/satellites/gameplay gated; surface N/A). Dante/Hades → bulk mass/radius/rotation rows,
magnetism=none, albedo/surface_temp, identity. Pandora → nearly everything (bulk, atmosphere,
surface/biosphere, appearance, environment, gameplay).
