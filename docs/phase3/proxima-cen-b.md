<!-- Proxima Cen b Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Proxima Cen b — Phase 3 Synthesis

Phase 3 planet synthesis for the NearStars KSP mod (drafted 2026-05-22).

Proxima Cen b is the nearest known potentially habitable planet at
1.302 pc. Discovered by Anglada-Escudé et al. 2016 via radial
velocity (HARPS), refined by Faria et al. 2022 (ESPRESSO) and
Suárez Mascareño et al. 2025 (HARPS+ESPRESSO+NIRPS combined). It
is a terrestrial-mass world (Msini = 1.055 ± 0.055 M⊕,
Suárez Mascareño 2025) on a 11.18-day orbit at 0.0485 AU, receiving
~0.65× Earth's flux — inside the inner edge of the optimistic
habitable zone for a 2904 K M5.5 host. No transits have been
detected (multi-year searches by ASTERIA, TESS, MEarth-South, ATCA
follow-ups have all returned null), implying orbital inclination
< ~87° relative to Earth's line of sight.

Because no transmission spectroscopy exists, the atmospheric state
is unconstrained by direct observations and must be reasoned from
theoretical considerations: XUV-driven escape over ~5 Gyr
(Ribas et al. 2016, Zahnle & Catling 2017), N₂/CO₂ outgassing
balance (Tian 2015, Lichtenberg 2024), and GCM climate modeling
under tidally locked conditions (Turbet et al. 2016, Boutle et al.
2017, Way et al. 2024 spin-orbit resonance suite).

**Scenario choice for NearStars: temperate eyeball-Earth aquaplanet
with persistent substellar ocean and frozen poles**, with thin
N₂/CO₂ atmosphere (~0.5 bar) and scattered substellar clouds. This
balances JWST-equivalent observational defensibility with the
visually distinctive "blue dot at Proxima" motif that has shaped
public perception since the 2016 discovery announcement. The
desiccated bare-rock alternative (Ribas 2016 escape-dominated case)
is preserved as a cfg variant.

## Decisions

Kopernicus / atmosphere cfg-ready values.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 11.2 d orbit, tidal damping; Barnes 2017 |
| `obliquity_deg` | 0 | medium | tidal damping with binary perturbation negligible at this orbit |
| `eccentricity` | 0.02 | medium | Suárez Mascareño 2025; consistent with Faria 2022; A16 had higher 0.35 less trusted |
| `sidereal_period_days` | 11.18465 | high | Suárez Mascareño 2025 |
| `semi_major_axis_au` | 0.04848 | high | Suárez Mascareño 2025 |
| `mass_mearth_msini` | 1.055 | high | Suárez Mascareño 2025 RV |
| `mass_mearth_true_adopted` | 1.30 | medium | adopted: 23% upward for inclination (sin i ≈ 0.81 prior; Mendillo et al. 2018 statistical) |
| `radius_rearth` | 1.07 | medium | derived from M_true × Earth-like rock-iron MR relation (Zeng 2016) |
| `surface_gravity_g_earth` | 1.14 | medium | derived |
| `density_g_cc` | 6.0 | medium | Earth-like rocky composition |
| `equilibrium_temp_k` (A=0.3) | 234 | high | derived from a/R★, T★=2904 K |
| `equilibrium_temp_k` (A=0) | 254 | high | derived |
| `bond_albedo` | 0.20 | medium | substellar cloud feedback (Boutle 2017) ~30%; partial cloud cover gives ~20% net |
| `atmosphere_present` | true | low | adopted scenario; Tian 2015 N₂ retention possible |
| `atmosphere_surface_pressure_pa` | 50000 | low | ~0.5 bar; intermediate between Mars (~600 Pa) and Earth (~10⁵ Pa) given partial atmospheric escape |
| `atmosphere_composition` | N₂ (70%) + CO₂ (28%) + H₂O (2%) | low | Tian 2015 outgassing balance; H₂O variable |
| `atmosphere_scale_height_km` | 6 | medium | derived from T~250 K, μ~36 g/mol (N₂+CO₂ mix), g=11.2 m/s² |
| `atmosphere_tint_rgb_hex` | `#f0c8a8` (pale tan-blue limb) | medium | Rayleigh + thin Mie scattering under deep-red M-dwarf illumination produces washed-out sky tint |
| `dayside_substellar_temp_k` | 282 | medium | Turbet 2016 GCM: open-ocean substellar warm pool with ~50% cloud cover |
| `dayside_average_temp_k` | 220 | medium | atmospheric circulation + albedo feedback |
| `nightside_average_temp_k` | 175 | medium | weak day-night heat transport in moderate atmosphere; ice cap on antistellar point |
| `substellar_ocean_present` | true | low | Pierrehumbert 2011 + Boutle 2017 GCM — substellar pool is dynamically stable under M-dwarf illumination |
| `surface_ice_fraction_pct` | 70 | low | global ice coverage ex-substellar circle (eyeball Earth scenario) |
| `surface_ocean_fraction_pct` | 20 | low | substellar ice-free zone |
| `surface_continent_fraction_pct` | 10 | low | composition-derived; some land plausible |
| `surface_tint_rgb_hex_ocean` | `#1a4060` (deep blue under red illumination) | low | ocean H₂O absorption + M-dwarf red preferential reflection |
| `surface_tint_rgb_hex_ice` | `#e0d8c0` (warm-tint ice under M-dwarf) | low | ice scatter under red illumination |
| `surface_tint_rgb_hex_continent` | `#604020` (dark basalt + iron oxide weathering) | low | dim red-tinted terrain |
| `magnetic_field_strength_microtesla_equator` | 35 | medium | Earth-mass dipole scaling (Olson & Christensen 2006); Garraffo 2016 MHD context for compression |
| `magnetic_dipole_moment_normalized_earth` | 0.55 | medium | from 1.07 R⊕ and tidally-locked rotation (10× slower than Earth) |
| `magnetosphere_standoff_planet_radii` | 1.5 | medium | Garraffo 2016 — strong Proxima wind compresses magnetopause |
| `radiation_belt_present` | true | low | wider trapping region than Earth due to weaker dipole + harder stellar wind |
| `surface_radiation_dose_msv_yr_quiet` | 50 | medium | normal background; atmosphere shielding ~5 g/cm² |
| `surface_radiation_dose_msv_yr_superflare_event` | 1e6 | medium | MacGregor 2018 + Atri 2019 — superflare proton storm |
| `flare_event_rate_per_yr_observable_at_planet` | 100 | high | Howard 2018 scaled to b's orbit |
| `aurora_present` | true | medium | strong stellar wind + B-field gives strong auroral activity |
| `aurora_color_primary_hex` | `#A0E0B0` | low | tie-break: visible green from [OI] 5577 Å excitation under thick N₂+CO₂ atmosphere |
| `aurora_color_secondary_hex` | `#E090A0` | low | proton-driven Hα 6563 Å emission (red); MacGregor superflare events make this dominant during flares |
| `aurora_oval_magnetic_latitude_deg` | 50 | medium | weaker dipole gives larger oval; Vidotto 2013 scaling |
| `aurora_intensity_kR_quiet` | 80 | medium | quiet Proxima wind gives modest aurora |
| `aurora_intensity_kR_flare` | 5000 | medium | flare/superflare brightness |
| `induction_heating_w_per_m2` | 0.05 | medium | Kislyakova 2018 sub-Earth scaling, weak contribution |
| `star_apparent_angular_diameter_deg` | 1.5 | high | derived: 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2904 | high | Passegger 2019 SED fit |

## Surface synthesis

Proxima b is the canonical M-dwarf eyeball planet candidate.
Pierrehumbert 2011 first articulated the "eyeball Earth" climate
state for tidally locked aquaplanets: under deep-red M-dwarf
illumination, ice-albedo feedback combined with concentrated
substellar heating produces a globally frozen world with a small
liquid water region directly under the host star. The ratio of
substellar liquid to global ice depends on insolation, atmospheric
heat transport efficiency, and rotational state.

Boutle et al. 2017 GCM simulations specifically for Proxima b under
1-bar N₂+H₂O atmosphere show that the eyeball state is dynamically
stable — convective updrafts at the substellar point efficiently
remove the sea ice that would otherwise propagate inward from the
poles, and the resulting cloud cover at the substellar zone
provides a stabilizing albedo feedback (the "M-dwarf cloud
suppression" mechanism is *not* a runaway-greenhouse pathway).

Turbet et al. 2016 considered three scenarios:
- (A) Earth-twin 1-bar N₂+H₂O: eyeball with ~30% surface ice-free.
  Adopted.
- (B) Snowball state with 1-bar CO₂ + ice: stable only at much
  lower CO₂ partial pressure.
- (C) Hot greenhouse with thick CO₂ atmosphere: dynamically
  unstable; collapses to (A) over Myr timescales.

For NearStars cfg we adopt (A) as the canonical case.

**Color choice.** Ocean: very deep blue under M-dwarf illumination
because water has very strong long-wavelength absorption — the
preferential reflection at short wavelengths is fed by very little
incident flux (M dwarf SED is dominated by IR), so the visible-band
reflection is *bluer* than Earth's ocean per surface, but
*dimmer* in absolute brightness. RGB ≈ `#1a4060`.

**Surface ice.** M-dwarf illumination on H₂O ice produces a warm-
tinted reflection (ice is bright across visible, so it accepts the
red SED). RGB ≈ `#e0d8c0`. Polar caps appear as a warm cream-white
fringe to a deep red-illuminated dark world.

**Continents.** Bare basalt + iron oxide weathering on M-dwarf
worlds tends to produce surface oxidation as on TRAPPIST-1 d.
Continents (if present) appear as dark brown-red patches between
ice cap and substellar ocean.

**Substellar zone morphology.** Open ocean with persistent
convective clouds; cloud cover ~50% (Boutle 2017). Cloud-decked
ocean appears as a bright cream-white circle of ~30° angular
diameter on the substellar point, embedded in surrounding ice.
This is the "eye" of the eyeball Earth — the iconic visual feature.

**Cratering.** ~5 Gyr age + tidally locked → leading-hemisphere
crater asymmetry (similar to Mercury's old surface), but partly
erased by ice resurfacing on the night/polar regions and by
sediment burial in the substellar ocean.

**Habitability context.** Heller & Armstrong 2014 "Superhabitable
worlds" emphasizes that K-dwarf and earlier M-dwarf temperate
worlds have stable long-baseline climates due to the host's longer
main-sequence lifetime. Proxima b at 5 Gyr is mid-life and could
have hosted stable temperate conditions for the duration if (A)
was its initial state.

## Atmosphere synthesis

No direct atmospheric observations exist for Proxima b. Theoretical
inferences from XUV history, tidal locking, and equilibrium
chemistry:

**XUV escape history.** Ribas et al. 2016 modeled cumulative XUV
flux on b over 5 Gyr: ~10× current Earth value time-integrated.
Sufficient to drive 1–10 Earth-ocean masses of water loss via
hydrodynamic escape. *If* the initial water inventory was Earth-
like, the residual water budget is uncertain — between fully
desiccated (Zahnle & Catling 2017 wet case) and ~Earth-equivalent
(if the planet had significantly more initial water).

**Atmospheric retention.** Tian 2015 N₂ retention model predicts
that a 1-bar N₂ atmosphere is stable against thermal escape for an
Earth-mass planet at b's orbit. Non-thermal escape (sputtering,
ion pickup by stellar wind) is more aggressive — Garraffo et al.
2016 MHD models show partial atmospheric stripping during stellar
wind enhancements. Net: ~0.1–1 bar N₂ atmosphere is plausible at
present.

**Composition.** Outgassing balance from a mantle with Earth-like
fO₂ produces dominant N₂ + CO₂ (~70:28) with trace H₂O. CH₄ and
NH₃ are photolyzed by M-dwarf XUV faster than they can be
replenished by volcanic outgassing. O₂ build-up from H₂O
photolysis is possible but the inventory is sensitive to escape
rates (Meadows 2017 false-positive biosignature analysis).

**Atmospheric circulation.** Standard tidally-locked GCM produces
a single hemispheric convective cell with strong substellar
updrafts, equatorial superrotating jet, and terminator-zone
descending air. Day-night heat redistribution efficiency depends
on surface pressure — at 0.5 bar, the night-side temperature is
moderated to ~175 K (above CO₂ condensation, so no CO₂ ice cap).

**Lightning.** Braam et al. 2023 modeled lightning chemistry on
tidally locked Earth-like worlds. Lightning-driven NO production
in the substellar updraft is ~30% of Earth's rate, producing
detectable atmospheric chemistry signatures. For NearStars visual:
occasional lightning flashes visible during the night-side passage
under the substellar cloud deck.

**Cloud structure.** Cohen et al. 2022 show that "traveling
planetary-scale waves" produce cloud variability on tidally locked
aquaplanets — patches of stratus rotate with the planetary wave
speed (~few day timescale). Visual: subglacial cloud bands at
terminator zone, fragmenting and reforming on ~3-day timescale.

**Ozone.** Chen et al. 2023 model stratospheric ozone on
synchronously rotating exoplanets: ozone is concentrated at the
day-night terminator due to photolytic transport. Visual: faint
UV-blue ozone layer at terminator only (not global).

**Flare atmosphere chemistry.** Howard 2023 flare statistics
scaled to b's orbit (0.0485 AU) give ~100 flares/yr at planet
location. Each event temporarily dissociates the atmosphere by
30–80%, producing a "flare smog" of reactive nitrogen species
that condense to NO₂/NO during the post-flare relaxation phase.

## Rotation & spin synthesis

Tidal locking is essentially certain at b's orbit: tidal
synchronization timescale << 5 Gyr (Barnes 2017 for moderate
viscosity). Spin-orbit state could be:

- **1:1** (default) — orbital eccentricity ≈ 0 favors this state.
  Adopted.
- **3:2** — possible if orbit had been more eccentric in the past
  (Way et al. 2024 considers this for similar planets).

**Obliquity = 0.** Tidal damping over Gyr timescales drives
obliquity to zero for tidally locked worlds without strong
companion perturbation. Proxima's wide AB hierarchical orbit
provides negligible perturbation on b's spin axis at present
epoch.

**No day-night cycle.** With 1:1 lock and zero obliquity, the
substellar point is fixed in surface coordinates. Visual: no
diurnal lighting variation, no terminator drift. The only timescale
is the stellar rotation period (83 d) producing slow stellar disk
rotation, and the orbital period (11.2 d) producing eclipses /
occultations of Alpha AB during conjunction.

**Day-night heat transport.** Despite the steady-state insolation
geometry, large-scale atmospheric circulation produces strong
day-night heat transport. The substellar warm pool (282 K) is
balanced against the anti-stellar cold spot (~150 K with full
atmospheric heat transport; ~120 K if atmosphere is thin/stripped).

## Visual styling

Combining surface and atmosphere decisions:

- **Global color palette.** Deep-red ambient illumination from
  Proxima dominates. The substellar zone glows warm cream (cloud
  + ice + ocean blend); the polar zone is dim warm-cream ice;
  continents (if any) are dark brown-red basalt.
- **Substellar view.** The "iconic" Proxima b appearance: looking
  down at the substellar point from above, the world resembles
  Pierrehumbert's eyeball Earth — bright central cloud-decked
  ocean ringed by ice. The cloud center has detectable
  morphology (storms, convective cells).
- **Terminator band.** The most dynamic region. Cloud bands
  fragment and reform; thin ozone layer creates a faint UV-blue
  glow visible from space at the day-night boundary; auroral
  emission from incoming stellar wind protons concentrated at
  ±50° magnetic latitude.
- **Nightside.** Very dark and cold (~175 K). No insolation; only
  reflected light from Alpha AB (cream-yellow), aurora glow
  (greenish-red), and occasional lightning flashes during the
  substellar cloud convection. The Milky Way and Alpha AB
  dominate the night sky.
- **Atmospheric haze.** The 0.5 bar atmosphere produces a faint
  pale tan-blue limb haze (~10 km thick), only visible against
  black-space limb illumination.
- **Star in sky.** Proxima subtends ~1.5° (3× Sun-from-Earth's
  apparent diameter). Deep red-orange (`~#ff6028`), visibly
  freckled with starspot complexes that drift on the 83-day
  rotation period. Solar-mass equivalent illumination (~0.65 S⊕)
  at orbit.
- **Sister planet d in sky.** Proxima d at 0.0288 AU is closer to
  the star than b is. When in inferior conjunction with b, d
  passes within ~0.02 AU (~3 million km) of b — appears as a
  bright ~mV -2 star for several hours, then recedes. Not a
  full transit since orbits are not perfectly coplanar.
- **Alpha AB in sky.** Brilliant point at V ≈ -7, cream-yellow,
  ~2° from a position that drifts very slowly over centuries.
  Bright enough to cast detectable shadows.
- **Flare event visuals.** Once per ~4 days, a flare brightens
  Proxima by 5–50× for minutes. The substellar zone receives a
  brief intense UV-blue light pulse, washing out the normal red
  illumination. Aurora intensifies dramatically. The illuminating
  effect would be jarring for any KSP gameplay around b — a key
  feature of "living near an active M dwarf."
- **Superflare events.** Every ~1 yr at b's orbit position, a
  ~10³³ erg flare brightens Proxima 100–1000×. Lasting 30 min,
  the planet briefly receives multi-solar-equivalent flux,
  triggering atmosphere chemistry and aurora storms.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2016Natur.536..437A** Anglada-Escudé et al. 2016 — Proxima b
  discovery paper. Definitive RV characterization at discovery.
- **2022A&A...658A.115F** Faria et al. 2022 — ESPRESSO refinement +
  Proxima d discovery. Better mass constraint for b (Msini 1.07 ±
  0.06).
- **2025A&A...700A..11M** Suárez Mascareño et al. 2025 — HARPS +
  ESPRESSO + NIRPS combined analysis. Refined parameters used as
  Phase 2 recommended for both b and d.
- **2016A&A...596A.111T** Turbet et al. 2016 — GCM simulations for
  Proxima b under three atmospheric scenarios (snowball, eyeball,
  greenhouse). Drives the (A) eyeball scenario choice.
- **2017MNRAS.471.4628B** Boutle et al. 2017 — Cloud-resistant
  ocean GCM showing eyeball stability under M-dwarf illumination.
- **2016ApJ...823L..14R** Ribas et al. 2016 — XUV escape history
  for Proxima b. Time-integrated atmosphere loss estimate.
- **1607.06677** Zahnle & Catling 2017 — Atmospheric escape
  outcome envelope. Bare-rock case as cfg alternative.
- **1802.00141** Hu et al. 2018 — Biohabitability of M-dwarf
  planets. UV-flare context.
- **2204.09270** Diamond-Lowe et al. 2022 — Simultaneous X-ray +
  FUV monitoring of Proxima. Quantifies the radiation environment
  at b's orbit.
- **2306.03004** Chen et al. 2023 — Stratospheric ozone on
  synchronously rotating exoplanets. Drives terminator-zone
  ozone visual.
- **2209.12502** Braam et al. 2023 — Lightning chemistry on
  tidally locked Earth-likes. Drives lightning visual.
- **2211.11887** Cohen et al. 2022 — Cloud variability from
  planetary waves. Drives terminator-zone cloud dynamics.
- **2410.19108** Way et al. 2024 — Spin-orbit resonance climate
  variants. Provides 3:2 alternative cfg.
- **2402.12253** Schreyer et al. 2024 — Water vapor transit
  retrieval ambiguities. Context for atmosphere retrieval
  expectations.
- **2204.03501** Quick et al. 2023 — Tidal-driven tectonic
  activity. Argues b could have plate tectonics.

### Read (context / methodology, not decision-driving)

- **2312.01893** Lichtenberg et al. 2024 — Water content of HZ
  rocky exoplanets. Context for initial water budget.
- **MacGregor et al. 2018 (1803.07581)** — March 2016 ALMA
  superflare. Drives superflare rate envelope at b's orbit.
- **2102.06318** Howard et al. 2018 — ASAS-SN flare cumulative
  distribution.
- **1706.04617** Garraffo et al. 2016 — MHD simulations of
  star-planet magnetic interaction at Proxima b. Drives
  magnetosphere standoff.
- **1909.13740** Garraffo et al. 2020 — Updated wind models.
- **1805.00929** Morel 2018 — Chemical composition of AB pair;
  context for system age and metallicity.
- **2410.01621** Garraffo et al. 2024 — Magnetized winds.
- **1802.00141** Mullan & MacDonald 2018 — Habitability physics.

### Read (instrument-only, not visual-informative)

- **2503.18538** PIAA/nuller coronagraph paper.
- **2311.18117** Detecting biosignatures with high-contrast
  imaging. Future-instrument context.

### Not read — no arXiv preprint available (84 papers)

Key not-read examples:
- "A Catalog of Habitable Zone Exoplanets" — context only.
- "Prospects for Cryovolcanic Activity on Cold Ocean Planets" —
  intriguing but outside b's parameter space (b is not cold-ocean
  per our cfg, it's eyeball with substellar warm pool).
- Multiple SETI search papers around Alpha + Proxima — null
  results, methodology only.

**User action requested.** If JWST or any future direct-imaging
mission (HabEx, LUVOIR successor) produces actual atmospheric
spectroscopy of b, the entire atmosphere section would need
revision. The 2025–2026 ELT direct-imaging campaigns (Carlomagno
2023 framework) may produce first reflected-light constraints.

---

## Open items for follow-up

- The inclination of b's orbit is unconstrained (no transit
  detection). Adopted Msini → M_true factor 1.23 is a Mendillo
  2018 statistical prior; a true direct measurement would tighten
  the mass.
- The Pierrehumbert eyeball state assumption is robust per Boutle
  2017 but depends on initial water inventory; if b is genuinely
  desiccated (Ribas 2016 worst case), the visual is closer to a
  baked Mars (cfg variant required).
- The Earth-equivalent magnetic field assumption (35 μT equator)
  is based on terrestrial dipole scaling; if b has weaker dynamo
  due to tidal locking, the field could be < 10 μT and aurora
  would be much brighter and lower-latitude.
- The 3:2 spin-orbit resonance variant (Way 2024) would produce
  daylight migration cycles — a strikingly different cfg.
- Lightning rate (Braam 2023) and visual flash frequency need
  better visual rendering — should appear as subtle subglacial
  flashes during the substellar cloud-deck pass.
- The flare schedule (100/yr at b's orbit) makes b's "living
  conditions" notably hostile for any KSP crew operations —
  worth highlighting in cfg comments for radiation gameplay.
- Direct-imaging follow-ups by 2030 (NEAR, ELT, KPIC) should
  refine the surface and atmosphere visual to the point where
  Phase 4 cfg revision is warranted.
