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
| identity | body_type / designation (A b I) / cultural | ✅ |
| identity | discoverability (fictional → RB `F F F F`) | ✅ |
| orbit | a / e / inc (roster, stability-gated) | ✅ (via satellites) |
| orbit | Ω / ω / M | ▫ |
| bulk | mass / radius (8e21 / 900 km, affirmed) | ✅ |
| bulk | rotation (tidal-locked ~9.2 h) / obliquity (~0) / spin_axis | ✅ |
| bulk | tidal_heating | ✅ |
| atmosphere | composition / pressure (thin SO₂) | ✅ |
| atmosphere | breathability (no) / scale_height / escape | ▫ |
| surface | surface_type / tectonics / terrain (rift) | ✅ |
| surface | albedo (0.30 bimodal sulfur/basalt) / surface_temperature (~230K + lava ~600K) | ✅ |
| surface | hydrosphere / ice_caps / biosphere | ∅ |
| appearance | surface look (sulfur/basalt half-half) / emission_glow | ✅ |
| appearance | clouds / haze / aurora / specular / rings | ∅ |
| magnetism | magnetic_field (none) / magnetosphere | ✅ |
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

## Pandora — A b III (Earth-like Na'vi homeworld) — ✅ full walk (2026-06-22)
| group | axis | status |
|---|---|---|
| identity | body_type / designation (A b III) / cultural | ✅ |
| identity | discoverability (fictional → RB `F F F F`) | ✅ |
| orbit | a / e / inc (32 h lock, 252,393 km) | ✅ (via satellites) |
| orbit | Ω / ω / M | ▫ |
| bulk | mass (B: 0.645 M⊕, re-sim STABLE) / radius (5724 km) / gravity (0.8 g) | ✅ |
| bulk | rotation (32 h lock) / obliquity (~10° eff, not 29°) / spin_axis | ✅ |
| bulk | tidal_heating / internal_heat (drives volcanism + dynamo) | ✅ |
| atmosphere | composition (N₂/O₂/CO₂>18%/Xe/H₂S) | ✅ |
| atmosphere | breathability (O₂ present, lore-toxic) / pressure (1.1 atm) / scale_height / greenhouse (+70K→290K) | ✅ |
| surface | surface_type (land:ocean ~50:50) / hydrosphere / biosphere (lush, biolum) | ✅ |
| surface | tectonics (volcanism, fast drift) / terrain (mountainous, floating-mtn arches) / ice_caps (peaks+poles) / albedo (0.30) / surface_temp (~290K) | ✅ |
| appearance | base colour (Earth-green) / clouds / biolum (subtle cyan) / aurora (intense, multi-colour) / specular (oceans) / city-lights (∅ Na'vi pre-industrial) | ✅ |
| magnetism | magnetic_field / magnetosphere | ✅ |
| magnetism | radiation_belts (between two belts) | ✅ (env note) |
| environment | radiation (between belts, shielded → habitable) | ✅ |
| rings / satellites | (none) | ∅ |
| gameplay | biomes (7, incl. flux-vortex + structures + local aurora) / SOI / difficulty | ✅ |

## Cassandra — A b IV (outer retrograde; Archean-analog marginal life) — ✅ full walk (2026-06-22)
| group | axis | status |
|---|---|---|
| identity | body_type / designation (A b IV) / cultural / discoverability (fictional → RB `F F F F`) | ✅ |
| orbit | a / e / inc (600,000 km, retrograde 176°) | ✅ (via satellites) |
| bulk | mass / radius (9e23 / 3400 km, density kept) / rotation (free ~39h, 3:1-ish) / obliquity (~20°, seasons) | ✅ |
| atmosphere | composition (N₂/CO₂/CH₄/H₂, anoxic reducing) / pressure (~1 bar) / temp (~270-275K) / greenhouse / breathability (no O₂) | ✅ |
| surface | water seas (partial ice) / biosphere (anaerobic microbial) / tectonics / ice_caps / albedo (0.35) | ✅ |
| appearance | Archean orange CH₄ haze / seas / no biolum / weak aurora | ✅ |
| magnetism | magnetic_field (weak dipole, iron core) | ✅ |
| environment | radiation (low: outer 8.4 R_p + weak-field shield); wind/activity/helio/flares/uv/HZ = ∅ star-level | ✅ |
| rings | all ∅ (no own rings; is Polyphemus E-ring inner shepherd) | ∅ |
| satellites | all ∅ (no submoons / co-orbitals; dust source = Chaos) | ∅ |
| gameplay | biomes (6; microbial-mat 7th = candidate, add if non-overlapping) / SOI / difficulty | ✅ |

## Chaos — A b V (outermost retrograde icy moonlet; E-ring source) — ✅ full walk (2026-06-23)
| group | axis | status |
|---|---|---|
| identity | body_type / designation (A b V) / cultural / discoverability (fictional → RB `F F F F`) | ✅ |
| orbit | a / e / inc (1.5M km, retrograde 179°, e 0.02) | ✅ (via satellites) |
| bulk | mass / radius (5.4e20 / 400 km) / rotation (free 9.5h) / obliquity (15°) / oblateness (f~0.06-0.075) | ✅ |
| atmosphere | none (0.023g) + plume vapor halo | ✅ |
| surface | icy + **water cryovolcanic plumes** (Enceladus-analog, art-first divergence) / Miranda fractures / albedo (~0.7) | ✅ |
| appearance | bright bluish-white ice / tiger-stripe plume jets / dramatic fractures | ✅ |
| magnetism | magnetic_field (none) | ✅ |
| environment | radiation (low/variable, 21 R_p magnetopause); star-level ∅ | ✅ |
| rings | all ∅ (no own rings) | ∅ |
| satellites | submoons/co-orbitals ∅; **dust_source = Chaos plumes feed E-ring** | ✅ |
| gameplay | biomes (5; plume vents = hotspot; corona dropped) / SOI / difficulty (ultra-low-g) | ✅ |

## Stars A / B (context) — ✅ appearance walked (2026-06-23, observation-based)
Activity / wind / heliosphere ▫ passthrough; magnetic_field ✅ (proxy). **appearance ✅** —
all observation-derived (Teff colour, granulation, limb darkening, corona, flares passthrough);
**starspot amount decided for texture**: A (G2V, quiet) = sparse ~0.1–0.3% coverage; B (K1V,
more active, X-ray ×10 swing, 8.84 yr cycle) = moderate ~1–3% (more spot groups). A colour
yellow-white ~#fff4ea, B yellow-orange ~#ffdcb0.

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

## Proxima Centauri b (α Cen C) — continental lake world (separate board `proxima_cen.yaml`)
Methodology-grounded walk 2026-06-23, all 11 groups gated.
| group | axis | status |
|---|---|---|
| identity | body_type (rocky lake world) / designation / discoverability (confirmed → T F F F) | ✅ |
| orbit | a / e≈0 / inclination (non-transit) / lock / Ω·ω·M (free emit) | ▫ (measured passthrough) |
| bulk | mass 1.22 M⊕ (isotropic median) / radius 1.07 R⊕ (M–R tie-break) / g / ρ / obliquity~0 | ✅ |
| atmosphere | pressure 0.7 bar (owner) / N₂+CO₂ ~3% / μ 28.5 / H~7km / Teq 228K / breathability ∅ | ✅ |
| surface | 2-tone mafic/anorthosite (ferrous, not red) / lakes / night ice / intrinsic hex / Bond cascade A~0.33 | ✅ |
| appearance | Proxima-lit reddened palette / warm ochre disk / faint flare-aurora (magenta-violet, comp-lock) | ✅ |
| magnetism | weak rocky dynamo (RM22 + tidal-lock penalty), unmeasured, conf low | ✅ |
| environment | radiation harsh / strong wind / deep astrosphere (derived from star + weak field) | ✅ |
| rings | none | ✅ |
| satellites | none (grounded — close-in tidal env forbids a stable moon) | ✅ |
| gameplay | landable lake world / splashdown / no-breathe / high radiation / interstellar flagship | ✅ |

## Proxima Centauri d / c / c I — all 11 groups walked (2026-06-23, `proxima_cen.yaml`)
- **Proxima d** (hot airless Mercury-analog, Faria 2022 candidate) — ✅ 11/11. Highlights: e~0.05 synthetic; airless (below shoreline); Teq~317K/substellar~450K; **SPI-inferred B ~16G (Zapatero Osorio 2026, arXiv:2605.22925) — first terrestrial-exoplanet field estimate, phase-locked flares**; field cascade → reduced space-weathering + dark flare-weathered magnetic polar caps; biome hybrid 7 (RSS-Mercury geology + 1:1 thermal).
- **Proxima c** (cold mini-Neptune, Damasso 2020 candidate) — ✅ 11/11. 8 M⊕/~2.7 R⊕; H/He envelope, Teq~40K; pale grey-white (colder-than-Neptune → less blue); ice-giant analog field; **double red/white ice rings (Gratton 2020 hook, anti-Saturn)**; satellite Proxima c I; biomes 5 latitude bands (no ring-shadow).
- **Proxima c I** (Pluto-analog ice moon, fiction) — ✅ 11/11. ~950 km Triton/Titania-class (ratio 0.055); just outside the rings (shepherds outer edge); tenuous Pluto-like N2 + blue haze; bimodal terrain (equatorial tholin belt + polar N2 caps) + **sub-c ring-ice eyeball** (buries tholin, signature); no field/ocean; lowest-hazard (GCR-driven tholin); RB FFFF; biomes 4.

---
**TODO summary (fill systematically):** Polyphemus → ✅ FULL MENU WALKED (identity/orbit/bulk/atmosphere/magnetism/environment/rings/satellites/gameplay gated; surface N/A). Dante/Hades → bulk mass/radius/rotation rows,
magnetism=none, albedo/surface_temp, identity. Pandora → nearly everything (bulk, atmosphere,
surface/biosphere, appearance, environment, gameplay). **Proxima system → ✅ FULL: star + b + d + c + c I all 11-group walked (2026-06-23, methodology-grounded, 51 decisions).**
