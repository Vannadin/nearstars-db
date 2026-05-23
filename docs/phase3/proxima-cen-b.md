<!-- Proxima Centauri b Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Proxima Centauri b — Phase 3 Synthesis

Proxima Centauri b is a 1.055-Earth-mass terrestrial planet on an
11.18-day, near-circular orbit around the closest star to the Sun
(0.04848 AU semi-major axis, 0.65× Earth's insolation). Discovered
by Anglada-Escudé et al. 2016 (Nature 536, 437; arXiv:1609.03449)
from a decade of HARPS, UVES, and follow-up RV monitoring, the
planet has been refined through successive ESPRESSO + HARPS + NIRPS
campaigns culminating in the Suárez Mascareño et al. 2025 (SM25)
joint analysis. SM25 reports the current best orbital fit:
P = 11.18465 ± 0.00053 d, a = 0.04848 AU, e ≈ 0 (consistent with
circular at the precision of the fit), Msini = 1.055 ± 0.055 M⊕,
mean anomaly at JD 2 460 548.59 of 0°. Both Faria 2022 and SM25
favor a circular orbit; the original Anglada-Escudé 2016 fit reported
an upper limit e < 0.35 rather than a best-fit non-zero eccentricity,
and the later ESPRESSO + NIRPS data tighten this to e < 0.1 (95% CL).

The planet does not transit (Jenkins et al. 2019, arXiv:1905.01336;
Gilbert et al. 2021, arXiv:2110.10702 — multiple Spitzer + TESS
campaigns rule out transits at the discovery period), so the radius,
density, and atmospheric properties are inferred rather than measured.
Climate modeling of Proxima b is now mature: Turbet et al. 2016 first
mapped the 1D parameter space; Boutle et al. 2017 ran the Met Office
Unified Model (UM) for Earth-like and simplified-N₂ scenarios; Del
Genio et al. 2019 added an active ocean component; Sergeev et al.
2020 emphasized substellar convection; Salazar et al. 2020 and
Lewis et al. 2018 explored substellar continent geometry; Galuzzo
2021 produced 3D detectability simulations; and Braam et al.
(2022 / 2023 / 2024 / 2026) built the photochemistry framework for
the trace-species spectra. Meadows et al. 2018 enumerated the
environmental states and observational discriminants.

The atmospheric retention question — whether Proxima b has retained
any significant atmosphere given Proxima's flare environment — remains
genuinely open. Atri 2020 (1910.09871) computes surface radiation
doses lethal to multicellular life under no-atmosphere conditions;
Lee 2021 (2109.06963) models Venus-analog photochemical escape of
oxygen at ~10⁹ atoms cm⁻² s⁻¹; Garraffo 2022 (2211.15697) finds
stellar-wind ram-pressure spikes of 10⁴–10⁶ × the solar value during
super-Alfvénic transits. On the other hand, Zuluaga 2018
(1609.00707) shows that a modest intrinsic magnetic field (~0.1 M⊕
dipole moment) can provide partial shielding, and Meadows 2018 §3
notes that all the escape calculations rely on assumptions about
the early-Proxima XUV history that are themselves uncertain at the
factor-of-10 level. The cfg treats the atmosphere-present decision
as a **tie-break** rather than a divergence: literature gives both
"retained" and "stripped" scenarios with comparable plausibility, and
NearStars selects the visually distinctive atmosphere-present case
per the interesting-first rule.

**Scenario choice for NearStars: a 1.055 M⊕ tidally-locked terrestrial
planet with a 1-bar N₂ + CO₂ atmosphere, a substellar open-water
ocean lens extending to ~60° from the substellar point, surrounded
by extensive glacial ice elsewhere. Cloud cover 55%, including a
substellar convective cluster and Rossby-wave-driven extratropical
variability. Weak intrinsic magnetic field (~0.1 M⊕ dipole moment),
heavily compressed magnetosphere, frequent aurora during Proxima
superflares.** 42 cfg picks; 31 canonical-aligned, 11 tie-break (hex
colors, cloud morphology detail, magnetic field range, water mass
fraction). No documented divergences — the canonical reading
(Boutle 2017 + Del Genio 2019 + Sergeev 2020 + Salazar 2020) supports
exactly this scenario, with snowball and desiccated variants
preserved in Open items.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 11.18-d orbit; Walterová 2020 tidal-locking timescale ~10⁵ yr |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0.0 | high | SM25 — fit consistent with circular |
| `sidereal_period_days` | 11.18465 ± 0.00053 | high | SM25 |
| `semi_major_axis_au` | 0.04848 ± 0.00029 | high | SM25 |
| `mean_anomaly_at_epoch_deg` (JD 2 460 548.59) | 0 | high | SM25 |
| `mass_mearth` | 1.055 ± 0.055 | high | SM25 Msini |
| `radius_rearth` | 1.07 | medium | Tie-break: non-transiting; mass-radius for Earth-like rocky composition gives 1.04–1.10 R⊕; interesting-first picks 1.07 for visual recognition |
| `surface_gravity_g_earth` | 0.92 | medium | derived = 1.055 / 1.07² |
| `density_g_cc` | 5.36 | medium | derived; consistent with Earth-analog rocky composition |
| `water_mass_fraction` | 0.05–0.10 | medium | Tie-break: Herath 2021 interior models allow 0.001–0.4; Earth-analog window chosen for surface-water visual |
| `insolation_s_earth` | 0.646 | high | derived from L = 0.00157 L☉ and a = 0.04848 AU |
| `equilibrium_temp_k` (A=0) | 226 | high | derived |
| `equilibrium_temp_k` (A=0.3) | 207 | high | derived |
| `bond_albedo` | 0.30 | medium | Boutle 2017 GCM range 0.25–0.35 |
| `surface_temp_substellar_k` | 290 | medium | Boutle 2017 §3 — peak dayside in tidally-locked simplified-N₂ scenario; Del Genio 2019 dynamic ocean compatible |
| `surface_temp_nightside_cold_trap_k` | 150 | medium | Boutle 2017 §3 — minimum nightside cold-trap (Earth-like atmosphere slightly warmer) |
| `surface_temp_global_mean_k` | 250 | medium | Boutle 2017 — mean below freezing at e=0; Del Genio 2019 dynamic ocean adds ~10–20 K nightside redistribution |
| `atmosphere_present` | true | medium | Tie-break: Boutle 2017 + Meadows 2018 + Zuluaga 2018 keep retention viable; Atri 2020 + Garraffo 2022 favor escape; both obs-consistent. Interesting-first picks atmosphere visible per the interesting-first rule |
| `atmosphere_surface_pressure_pa` | 100000 (1 bar) | medium | Boutle 2017 nominal Earth-like / simplified-N₂ scenarios both run at 1 bar |
| `atmosphere_composition` | N₂ 95%, CO₂ 5%, H₂O 0.1–1% (saturated near substellar), trace O₂ | medium | Boutle 2017 simplified N₂+CO₂; Braam 2024 photochemistry for trace species |
| `atmosphere_scale_height_km` | 11 | medium | derived: kT/μg with T = 260 K, μ = 30, g = 9.0 m/s² |
| `atmosphere_tint_rgb_hex` | `#4a3030` (deep red-shifted Rayleigh + Mie under M5.5V) | medium | Tie-break: Rayleigh blue heavily reddened by Proxima SED; specific shade selected for visible contrast in-game |
| `cloud_cover_fraction` | 0.55 | medium | Boutle 2017 + Cohen 2023 wave-driven cloud variability |
| `cloud_morphology` | substellar convective cluster + extra-tropical Rossby wave trains + nightside clearer | medium | Boutle 2017 + Sergeev 2020 substellar convection + Cohen 2023 traveling waves |
| `cloud_tint_rgb_hex` | `#d8a888` (warm cream water clouds under M-dwarf) | medium | Tie-break: water-cloud albedo × M-dwarf SED; warm tone chosen for contrast against the dark ocean |
| `ocean_present` | true (substellar open-water lens) | medium | Boutle 2017 + Del Genio 2019 dynamic ocean |
| `ocean_extent_substellar_radius_deg` | 60 | medium | Boutle 2017 — ice line at ~60° from substellar in the Earth-like scenario |
| `ocean_tint_rgb_hex` | `#0a2238` (very dark navy under faint red star) | medium | low insolation + deep liquid water → dark blue-violet |
| `surface_ice_caps` | wraps from ~60° outward; covers ~75% of surface | medium | Boutle 2017 ice cover; Sergeev 2020 thermal-gradient confirmation |
| `surface_tint_rgb_hex_primary` | `#d4cab8` (water ice + frost under red star) | medium | water-ice albedo 0.5–0.7 × M-dwarf SED |
| `surface_tint_rgb_hex_accent` | `#7a4a30` (exposed bedrock at terminator pressure-ridge tops) | low | Tie-break: ice-flow geometry exposing subglacial rock at high-pressure ridge axes |
| `surface_morphology` | substellar liquid ocean disk, transition annulus of sea-ice and slush, glacial ice over frozen ocean elsewhere, exposed bedrock at terminator ridges | medium | Boutle / Del Genio / Sergeev consensus on eyeball-Earth geometry |
| `magnetic_field_present` | true (modest) | medium | Tie-break: Zuluaga 2018 lower-bound supports dipole; large uncertainty in actual value; interesting-first picks present for aurora visual |
| `magnetic_dipole_moment_normalized_earth` | 0.1 | medium | Tie-break: Zuluaga 2018 plausibility range 0.01–1.0; 0.1 selected for partial-shielding regime |
| `magnetic_dipole_tilt_deg` | 15 | low | Tie-break: distinct aurora-cap geometry; literature silent on dipole tilt for Proxima b |
| `magnetosphere_standoff_planet_radii` | 1.5 | high | Garraffo 2022 — stellar wind pressure compresses standoff to < 2 R_p during super-Alfvénic transits |
| `radiation_belt_present` | false | medium | Garraffo 2022 + Atri 2020 — heavy CME compression precludes stable trapped particle population |
| `surface_radiation_dose_msv_yr` | 5000 | medium | Atri 2020 (1910.09871) for 1 bar atmospheric shielding + weak B-field; spikes to 10⁵ during superflares |
| `atmospheric_shielding_g_cm2` | 1000 | high | 1 bar atmosphere → ~1000 g/cm² column |
| `aurora_present` | true | high | Atm + B-field both present; Garraffo 2022 + Vida 2019 frequent superflare cadence drives intense precipitation |
| `aurora_color_primary_hex` | `#4DFF4D` ([OI] 557.7 nm green) | medium | Tie-break: N₂/CO₂/O₂ trace atmosphere chemistry; green oxygen line dominant per Earth-analog spectroscopy |
| `aurora_color_secondary_hex` | `#FF4D4D` (CO₂⁺ Fox–Duffendack–Barker + N₂⁺ Meinel red bands) | medium | Tie-break: photochemistry of N₂+CO₂ trace atmosphere; visible palette diversity |
| `aurora_emission_species_primary` | `[OI] 557.7 nm + N₂⁺ 391.4 nm First Negative + CO₂⁺ doublet` | medium | Braam 2024 photochemistry framework |
| `aurora_oval_magnetic_latitude_deg` | 60 | medium | weak B-field + super-Alfvénic compression broadens the aurora ring |
| `aurora_intensity_kR_typical` | 500 | medium | 10–50× Earth's typical 10 kR baseline; frequent superflare boosts |
| `star_apparent_angular_diameter_deg` | 1.5 | high | derived: 2 R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2980 | high | Proxima Teff |

## Surface synthesis

Proxima b is the canonical "eyeball Earth" — a tidally-locked rocky
planet with a substellar open-water disk surrounded by glacial ice.
Boutle 2017 §3 demonstrates this geometry persists across both the
Earth-like atmosphere (modern composition) and simplified-N₂ (1 bar
N₂ + 376 ppm CO₂) scenarios; Del Genio 2019 confirms it survives the
addition of a dynamic ocean component (which actually enhances heat
redistribution and slightly widens the open-water disk).

The substellar open-water disk extends to roughly 60° from the
substellar point — beyond this, surface temperatures fall below the
freezing point and stable glacial ice forms. The boundary is not
sharp: a transition annulus of sea-ice, slush, and intermittent
melt-back produces a visually striking ring of color and texture
shifts. The disk itself is dark — `#0a2238` in the cfg — because of
the combination of low M-dwarf insolation (0.65 S⊕) and water's deep
absorption above 700 nm. To an observer in orbit, the ocean lens
reads as a near-black disk against the bright glacial ice that
covers the antistellar hemisphere.

The glacial ice surface (`#d4cab8` cfg tint) covers ~75% of the
planet. Sergeev 2020 (arXiv:2004.03007) finds that the substellar
convective plume drives sustained subduction of warm air down to the
surface beneath the open-water disk, which in turn maintains the ice
boundary against the cold antistellar drag. Surface morphology at
the terminator is dominated by ridges from glacial flow plus exposed
bedrock at high-pressure ridge axes (cfg `surface_tint_rgb_hex_accent
= #7a4a30` for the bedrock exposures).

Shields 2018 (1808.09977) raises the alternative hydrohalite-snowball
scenario: if salinity is sufficient and the climate falls into a
snowball regime, salt deposits on the ice surface enhance albedo and
stabilize the snowball state. This is preserved as an Open-items
variant rather than the canonical cfg choice.

The water mass fraction sets the depth of the open-water disk and
the total subsurface ice reserve. Herath 2021 interior models allow
0.001 to 0.4 by mass, with no direct measurement to distinguish.
The cfg's 5–10% Earth-analog choice is a tie-break — it gives
~3-5 km mean ocean depth and recognizable Earth-like surface
hydrology, but the range is broad. A drier (0.001) variant would
shrink the open-water disk; a wetter (0.4) variant approaches Hycean
geometry.

## Atmosphere synthesis

The cfg adopts the Boutle 2017 simplified-N₂ atmosphere as the
canonical Proxima b scenario: 1 bar surface pressure, 95% N₂, ~5%
CO₂, trace H₂O (saturated near the substellar surface, dropping to
the dew point at higher altitudes and toward the terminator). Trace
O₂ (≪ 1%) is included to support the [OI] 557.7 nm aurora emission;
the source is photochemical (H₂O dissociation + escape of H), not
biological.

This composition reproduces the canonical surface temperature
distribution: T_substellar ≈ 290 K (peak dayside), T_nightside cold-
trap minimum ≈ 150 K, T_global_mean ≈ 250 K (Boutle 2017 §3 + Fig. 2).
Heat transport from substellar to nightside is dominated by atmospheric
circulation under the simplified-N₂ scenario; addition of a dynamic
ocean (Del Genio 2019) enhances the redistribution by ~10–20 K and
raises nightside temperatures above the bare-N₂ cold-trap floor.

Cloud cover is 55% in the cfg — chosen as a midpoint of the Boutle
2017 + Cohen 2023 + Sergeev 2020 range. The cloud morphology is
characteristic of tidally-locked synchronous M-dwarf planets:
a substellar convective cluster (Sergeev 2020) with high cirrus
shield, extra-tropical Rossby wave trains (Cohen 2023, 2211.11887)
that produce traveling cloud bands at ±30–60° latitude, and a
clearer nightside (Joshi 2020 dark-side inversion analog). The
cfg `cloud_morphology` field captures all three components in a
single string.

Photochemistry (Yates 2020, 1912.08743; Braam 2024, 2410.19108) is
dominated by O₃ production around the day-night terminator, with
the canonical M-dwarf "stratospheric ozone ring" producing a UV
signal that may be observable in future transmission spectroscopy
(though Proxima b is non-transiting). Scheucher 2020 (2003.02036)
adds the cosmic-ray-induced chemistry contribution — important
during super-Alfvénic transits when the magnetosphere is heavily
compressed.

The atmosphere is the planet's primary radiation shield: the cfg's
`atmospheric_shielding_g_cm2 = 1000` (1 bar column) reduces the
surface dose to ~5000 mSv/yr in quiet conditions (Atri 2020 Table 6
for analogous scenarios). Superflare events spike the dose to 10⁵
mSv per event, well above any biotic threshold but spatially and
temporally localized.

Water-vapor transit ambiguity (Macdonald 2024, 2402.12253) means
even if Proxima b were transiting, distinguishing a humid 1-bar
atmosphere from a desiccated surface would require very high-
precision retrievals; the cfg's atmospheric H₂O abundance is an
inference rather than a measurement.

## Rotation & spin synthesis

Proxima b is tidally locked, with the substellar point fixed at 0°
in the planetary frame and the sidereal rotation period equal to
the 11.18-day orbital period. Tidal locking timescales for a
1.055-M⊕ rocky planet at 0.04848 AU around a 0.122-M☉ M dwarf are
< 10⁵ years (Walterová 2020 Fig. 4), much shorter than the system
age. Obliquity is similarly damped to 0°.

The spin-orbit resonance is 1:1 (synchronous) because the orbital
eccentricity is zero (SM25). For any non-zero eccentricity Proxima b
would migrate into a higher-order resonance (Makarov 2012 framework),
producing intermittent insolation at the substellar point — Braam
2025 (2410.19108) explored spin-orbit resonance climate effects but
the SM25 zero-eccentricity result rules them out for the cfg.

Libration amplitude is < 1° (negligible). The substellar point's
fixed location creates the eyeball-Earth geometry described in the
Surface synthesis section. The daily diurnal cycle is absent; the
only temporal modulation comes from Proxima's 7-year activity cycle,
which slightly modulates the substellar insolation amplitude.

Magnetic dynamo: Zuluaga 2018 (1609.00707) finds that for a rocky
planet of 1 M⊕ with Earth-like core structure and rotation periods
of 10+ days, a modest intrinsic magnetic dipole is plausible
(~ 0.01–1.0 M⊕ moment). The cfg adopts 0.1 M⊕ as a tie-break
midpoint — sufficient for partial atmospheric shielding and visible
aurora but not strong enough to fully repel Proxima's stellar wind.

## Visual styling

In NearStars, Proxima b is the visual centerpiece of the system —
the most-modeled tidally-locked rocky planet in the catalog, with a
visually distinctive eyeball-Earth geometry. The substellar
open-water disk (`#0a2238`) reads as a near-black eye on a bright
glacial-white ice planet (`#d4cab8`), with the warm-cream cloud
cover (`#d8a888`) breaking up the surface into a distinctive
substellar cluster + extratropical band pattern. The terminator
ridges show exposed bedrock (`#7a4a30`) — a warm earth-tone accent
against the dominant cold palette.

Proxima fills 1.5° angular diameter in b's sky — three times the
apparent diameter of the Sun seen from Earth. The deep red M5.5V
illumination (`stellar_color_temp_k = 2980`) saturates the entire
surface with a warm cast. Aurora rings (`#4DFF4D` primary, `#FF4D4D`
secondary) ripple across the terminator during the frequent
superflares, with the cfg `aurora_intensity_kR_typical = 500`
producing visible-from-orbit glow during peak events.

Cloud-band morphology evolves on the 10-day rotation period of the
substellar Rossby waves (Cohen 2023), giving in-game cloud
animation a visible 1-week cadence. The substellar convective
cluster pulses on a slightly faster ~5-day cycle (Sergeev 2020).

The atmosphere's Rayleigh-scattering color is heavily reddened by
the M-dwarf SED — instead of the blue sky of Earth, Proxima b's
atmosphere produces a dim, deep-red sky during day, transitioning
through warm sunset tones to near-black at the terminator. The cfg
`atmosphere_tint_rgb_hex = #4a3030` captures this red-shifted
atmosphere visible from orbit. During Proxima superflares, the sky
briefly brightens with intense UV + optical scattering, producing
visually dramatic flare-events synchronized with the cfg `aurora_*`
fields.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Anglada-Escudé G. et al. 2016** — *A terrestrial planet candidate
  in a temperate orbit around Proxima Centauri*, Nature 536, 437
  (arXiv:1609.03449). Discovery paper. Best-fit P = 11.186 d, Msini =
  1.27 M⊕, a = 0.0485 AU.
- **Suárez Mascareño A. et al. 2025** — *Diving into the planetary
  system of Proxima with NIRPS* (arXiv:2507.21751). Current best
  orbital fit: P = 11.18465 d, e = 0, Msini = 1.055 M⊕.
- **Suárez Mascareño A. et al. 2020** — *Revisiting Proxima with
  ESPRESSO* (arXiv:2005.12114). Intermediate refinement.
- **Faria J. P. et al. 2022** — *A candidate short-period sub-Earth
  orbiting Proxima Centauri* (arXiv:2202.05188). Refined b mass to
  1.07 M⊕; companion Proxima d.
- **Boutle I. A. et al. 2017** — *Exploring the climate of Proxima B
  with the Met Office Unified Model*, A&A 601, A120
  (arXiv:1702.08463). UK Met Office UM GCM; substellar open-water
  lens, eccentricity sensitivity, Earth-like and simplified-N₂
  scenarios.
- **Turbet M. et al. 2016** — *The habitability of Proxima Centauri b.
  II. Possible climates and observability*, A&A 596, A112
  (arXiv:1608.06827). 1D climate framework; aquaplanet to snowball
  range.
- **Meadows V. S. et al. 2018** — *The Habitability of Proxima
  Centauri b: Environmental States and Observational Discriminants*,
  AsBio 18, 133 (arXiv:1608.08620). Atmospheric retention scenarios
  + observational discriminants.
- **Del Genio A. D. et al. 2019** — *Habitable Climate Scenarios for
  Proxima Centauri b with a Dynamic Ocean*, AsBio 19, 99
  (`2019AsBio..19...99D`; no arXiv preprint — Tier A manual followup,
  cited via Boutle / Sergeev / Salazar). Demonstrates dynamic ocean
  enhances heat redistribution and widens the open-water disk.
- **Sergeev D. E. et al. 2020** — *Atmospheric Convection Plays a
  Key Role in the Climate of Tidally Locked Terrestrial Exoplanets*,
  ApJ 894, 84 (arXiv:2004.03007). Substellar convection plume
  drives heat transport.
- **Salazar A. M. et al. 2020** — *The Effect of Substellar Continent
  Size on Ocean Dynamics of Proxima Centauri b*, ApJL 896, L34
  (arXiv:2005.14185). Substellar continent geometry sensitivity.
- **Lewis N. T. et al. 2018** — *The Influence of a Substellar
  Continent on the Climate of a Tidally Locked Exoplanet*, ApJ 854,
  171 (arXiv:1802.00378). Dry substellar continent stabilizes
  circulation.
- **Joshi M. M. et al. 2020** — *Earth's Polar Night Boundary Layer
  as an Analog for Dark Side Inversions on Synchronously Rotating
  Planets*, ApJ 892, 81 (arXiv:2003.06306). Nightside inversion.
- **Yates J. S. et al. 2020** — *Ozone chemistry on tidally locked
  M dwarf planets*, MNRAS 492, 1691 (arXiv:1912.08743). Terminator
  ozone ring.
- **Cohen M. et al. 2023** — *Traveling Planetary-scale Waves Cause
  Cloud Variability on Tidally Locked Aquaplanets*, ApJ 942, 86
  (arXiv:2211.11887). Rossby-wave cloud variability.
- **Scheucher M. et al. 2020** — *Proxima Centauri b: A Strong Case
  for Including Cosmic-Ray-induced Chemistry in Atmospheric
  Biosignature Studies*, ApJ 893, 12 (arXiv:2003.02036). Cosmic-ray
  driven photochemistry.
- **Shields A. L. et al. 2018** — *Hydrohalite Salt-albedo Feedback
  Could Cool M-dwarf Planets*, ApJL 866, L18 (arXiv:1808.09977).
  Snowball variant context.
- **Zuluaga J. I. et al. 2018** — *Magnetic properties of Proxima
  Centauri b analogues*, MNRAS 480, 4225 (arXiv:1609.00707).
  Plausible dipole moment range.
- **Atri D. et al. 2020** — *Stellar Proton Event-induced surface
  radiation dose* (arXiv:1910.09871). Surface dose calculation.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets* (arXiv:2007.12459). Tidal lock
  timescale.
- **Garraffo C. et al. 2022** — *Revisiting the Space Weather
  Environment of Proxima Centauri b*, ApJL 941, L8 (arXiv:2211.15697).
  Stellar wind ram pressure spikes; magnetosphere compression.
- **Lee Y. et al. 2021** — *Exosphere Modeling of Proxima b: A Case
  Study of Photochemical Escape* (arXiv:2109.06963). Venus-analog
  oxygen escape rate.
- **Macdonald E. et al. 2024** — *Water vapour transit ambiguities
  for habitable M-Earths* (arXiv:2402.12253). Atmospheric humidity
  retrieval ambiguity.
- **Galuzzo D. et al. 2021** — *Three-dimensional Climate Simulations
  for the Detectability of Proxima Centauri b*, ApJ 909, 191
  (arXiv:2102.03255). 3D detectability framework.
- **Braam M. et al. 2024** — *Earth-like Exoplanets in Spin–Orbit
  Resonances*, MNRAS 528, 3098 (arXiv:2410.19108). Climate dynamics
  + 3D photochemistry.

### Read (context / methodology, not decision-driving)

- **Bonfils X. et al. 2018** — *A temperate exo-Earth around a quiet
  M dwarf at 3.4 parsec* (arXiv:1711.06177). Sister-system context.
- **Jenkins J. S. et al. 2019** — *Proxima Centauri b is not a
  transiting exoplanet* (arXiv:1905.01336). Ruled out transit.
- **Gilbert E. A. et al. 2021** — *No Transits of Proxima Centauri
  planets in high cadence TESS data* (arXiv:2110.10702). Reinforces
  Jenkins.
- **Hammond T. et al. 2025** — Thermal emission spectra of nearby
  rocky exoplanets (arXiv:2504.00978). Multiple-planet spectra.
- **De Luca P. et al. 2024** — Ozone-climate dynamics
  (arXiv:2404.17972).
- **Boldog Á. et al. 2024** — Interior water content
  (arXiv:2312.01893).
- **Noack L. et al. 2021** — *Interior heating and outgassing of
  Proxima Centauri b* (`2021A&A...651A.103N`, no arXiv). Tier A
  manual followup; cited via abstract.
- **Herath M. et al. 2021** — *Interior structures of Proxima b and
  Ross 128 b* (`2021MNRAS.500..333H`, no arXiv). Tier A manual
  followup; cited via abstract.
- **Reiners A. et al. 2018** — Proxima magnetic field (arXiv:1711.06576).
- **Vida K. et al. 2019** — Proxima flare statistics (arXiv:1907.12580).
- **Fuhrmeister B. et al. 2022** — Proxima X-ray + FUV simultaneous
  flare (arXiv:2204.09270).

### Read (instrument / non-cfg-decisive)

- **Hardegree-Ullman K. et al. 2025** — Bioverse direct-imaging
  prospects (arXiv:2405.11423). Future-observability framework.
- **Singla M. et al. 2023** — Reflection spectra of terrestrial
  exoplanets (arXiv:2303.00540). High-contrast imaging.
- **Pearce L. A. et al. 2025** — Direct-detection sky position
  predictions (arXiv:2509.06747). Mission planning.

### Not read — no arXiv preprint or low-priority (~85 papers)

Conference proceedings, biosignature speculations, technosignature
searches, and gravitational-lens propulsion proposals; preserved in
`docs/phase3/_bib/proxima-cen-b.yaml` with `status: skipped`. Three
notable Tier A no-arXiv items captured in
`phase3/alpha-cen-proxima-system/manual-paper-followup.md`:
**Del Genio 2019** (dynamic ocean), **Noack 2021** (interior
outgassing), **Herath 2021** (interior structure).

## Open items for follow-up

- **Atmosphere-stripped variant**: Atri 2020 + Garraffo 2022 + Lee
  2021 all permit a stripped Proxima b under aggressive XUV /
  stellar-wind erosion scenarios. The cfg `atmosphere_present: true`
  is a tie-break; the alternative cfg variant has
  `atmosphere_present: false` and the surface becomes a hot-rocky
  desert with full Proxima irradiation. The downstream `kopernicus-cfg`
  writer can support both variants.
- **Snowball variant**: Shields 2018 hydrohalite-snowball + Turbet
  2016 low-CO₂ snowball give a fully ice-covered Proxima b with
  no substellar open-water disk. The cfg adopts the Boutle 2017
  eyeball-Earth canonical, but the snowball is observationally
  consistent.
- **Higher-water-content variant**: Herath 2021 interior models
  allow up to ~40 wt% water. A Hycean-style variant with much
  deeper substellar ocean and possible water-cloud opacity is
  another future cfg branch.
- **Spin-orbit resonance climate**: Braam 2024 (2410.19108)
  explored non-synchronous spin-orbit resonance climates. SM25's
  zero-eccentricity orbit makes the synchronous case canonical,
  but a re-analysis with weak eccentricity could change this.
- **Direct imaging**: Sanghi 2025 + Beichman 2025 JWST programs
  may eventually constrain Proxima b's reflected-light spectrum.
  If atmospheric features are detected, the cfg should be
  re-validated against the new constraints.
- **Magnetic field measurement**: Zuluaga 2018 provides only a
  plausibility range. A future direct measurement via radio emission
  during a Proxima-wind transit could constrain the dipole moment.
