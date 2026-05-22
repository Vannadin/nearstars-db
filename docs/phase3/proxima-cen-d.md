<!-- Proxima Cen d Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Proxima Cen d — Phase 3 Synthesis

Phase 3 planet synthesis for the NearStars KSP mod (drafted 2026-05-22).

Proxima Cen d is the closest sub-Earth-mass planet to the Solar
System. Discovered by Faria et al. 2022 via ESPRESSO RV at the
0.4 m/s amplitude level, and refined by Suárez Mascareño et al.
2025 (Msini = 0.26 ± 0.038 M⊕, P = 5.12 d, a = 0.0288 AU). The
minimum mass is ~2.4× Mars, making d the smallest confirmed planet
known beyond the Solar System as of the 2025 publication. It sits
deep inside Proxima's habitable zone — receiving ~3× Earth's flux —
where any volatile inventory faces extreme XUV exposure and tidal
heating.

No transits have been detected; no atmospheric data exist. The
planet's character must be inferred entirely from theoretical
considerations: thermal escape (Tian 2015 sub-Earth scaling),
silicate vaporization at high insolation (Way 2024 hot-Mercury
analogs), and tidal heating from eccentric orbits (Bolmont 2017
Proxima d not yet published since discovery in 2022).

**Scenario choice for NearStars: Mercury-analog hot bare-rock with
thin night-side volatile frost on poles**, anchored by basaltic /
ultramafic surface composition with relict magma-ocean morphology
on the leading dayside hemisphere. This is the "documented
divergence" cfg — gameplay-relevant frost cap on the night side
gives visual variety beyond a uniform hot rock; the canonical
"fully desiccated bare rock" is preserved as a cfg variant.

## Decisions

Kopernicus / atmosphere cfg-ready values.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 5.12 d orbit, tidal damping; Barnes 2017 |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0.0 | medium | Suárez Mascareño 2025; Faria 2022 0.04 less trusted |
| `sidereal_period_days` | 5.12338 | high | Suárez Mascareño 2025 |
| `semi_major_axis_au` | 0.02881 | high | Suárez Mascareño 2025 |
| `mass_mearth_msini` | 0.26 | high | Suárez Mascareño 2025 RV |
| `mass_mearth_true_adopted` | 0.32 | medium | adopted: 23% upward for inclination (sin i ≈ 0.81 prior; Mendillo 2018) |
| `radius_rearth` | 0.66 | medium | derived from M_true × Earth-like rock-iron MR relation (Zeng 2016) |
| `surface_gravity_g_earth` | 0.74 | medium | derived |
| `density_g_cc` | 5.5 | medium | rocky composition; less compressed than larger bodies |
| `equilibrium_temp_k` (A=0.1) | 363 | high | derived from a/R★, T★=2904 K |
| `equilibrium_temp_k` (A=0) | 379 | high | derived |
| `bond_albedo` | 0.10 | medium | bare-rock analog from TRAPPIST-1 b/c JWST emission |
| `atmosphere_present` | false (or thin trace) | low | adopted: bare rock; thin CO₂ <100 Pa as variant |
| `atmosphere_surface_pressure_pa` | 0 (canonical) / 50 (variant) | low | Mercury analog; trace at most |
| `atmosphere_composition` | none / trace CO₂ + Na vapor | low | photolytic Na exosphere if any rock-vapor |
| `atmosphere_scale_height_km` | - | - | not applicable for canonical case |
| `atmosphere_tint_rgb_hex` | none | - | no atmosphere visible |
| `dayside_substellar_temp_k` | 540 | medium | bare-rock subsolar at 3 S⊕, A=0.1 |
| `dayside_average_temp_k` | 380 | medium | bare-rock hemispherical average |
| `nightside_average_temp_k` | 90 | low | radiative cooling without atmospheric transport; Mercury analog |
| `surface_volatile_frost_present_on_pole` | true | low | Mercury polar volatile analog; tidally locked anti-stellar cold trap |
| `surface_volatile_composition` | H₂O + CO₂ + Na | low | photolytic delivery + cold trap accumulation |
| `surface_tint_rgb_hex_primary` | `#3a2818` (dark gray-brown basalt) | low | bare-rock low albedo + M-dwarf red illumination |
| `surface_tint_rgb_hex_accent` | `#7a4020` (relict magma flow tubes) | low | hotter magma ocean residual; cooler than TRAPPIST-1 d |
| `surface_tint_rgb_hex_frost_cap` | `#fff8e0` (warm cream frost) | low | H₂O frost under deep-red M-dwarf reflection |
| `surface_morphology` | cratered basaltic plains + leading-hemisphere magma relicts | low | bare rock with TRAPPIST-1 b/c analog overprint |
| `magnetic_field_strength_microtesla_equator` | 0.5 | low | sub-Earth-mass core shrinks; RM22 scaling + tidal-locking penalty |
| `magnetic_dipole_moment_normalized_earth` | 0.01 | low | RM22 (2203.01065) for sub-Mars-mass tidally-locked |
| `magnetic_dipole_tilt_deg` | 5 | low | tie-break: nearly aligned with rotation axis |
| `magnetosphere_standoff_planet_radii` | 1.1 | medium | very weak field → magnetopause near surface |
| `radiation_belt_present` | false | high | field too weak for trapped-particle regime |
| `surface_radiation_dose_msv_yr_quiet` | 60000 | medium | Atri 2019 scaled to d's orbit + no shielding |
| `surface_radiation_dose_msv_yr_flare_event` | 1e7 | medium | Proxima flares + no atmosphere = direct stellar irradiation |
| `aurora_present` | false | medium | no atmosphere → no auroral emission |
| `induction_heating_w_per_m2` | 0.2 | medium | Kislyakova 2018 — moderate contribution for d's mass + B-field combination |
| `tidal_heating_w_per_m2` | 0.05 | low | low eccentricity; minimal contribution; Bolmont 2017 |
| `star_apparent_angular_diameter_deg` | 2.6 | high | derived: 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2904 | high | Passegger 2019 SED fit |

## Surface synthesis

Proxima d's surface state is set by three competing processes:
- (1) Stellar XUV erosion of any atmosphere over 5 Gyr — Tian 2015
  scaling for sub-Earth-mass planets at high insolation predicts
  complete loss of N₂/CO₂ atmosphere within ~100 Myr.
- (2) Tidal heating from any remaining eccentricity — Bolmont
  2017 estimates F_int ≈ 0.05 W/m² for e ≈ 0.01 (the
  Suárez Mascareño 2025 upper limit), which is sub-runaway.
- (3) Surface-vapor cycle from photoevaporation of any volatiles
  delivered by impact or outgassing — produces a transient Na
  exosphere similar to Mercury but on a smaller scale.

The dominant outcome is **bare rock with permanent night-side cold
trap volatile deposit** — a Mercury analog scaled down by ~2.5× in
radius. The dayside surface is at 540 K substellar (well below
basalt solidus ~1400 K but warm enough for active surface
chemistry: photolytic oxidation, alkali volatilization, slow
weathering).

**Color choice.** Bare basalt + iron oxide overlay under M-dwarf
red illumination. Same dark gray-brown palette as TRAPPIST-1 d
(`#3a2818` primary), with brown-red iron-oxide accent (`#7a4020`).
The accent is slightly warmer than TRAPPIST-1 d's `#5a3220` because
d (Proxima) is at higher insolation and the cumulative photo-
oxidation is more complete.

**Magma-ocean relicts.** d's lower mass means a magma ocean phase
of ~100 Myr (vs ~500 Myr for TRAPPIST-1 d). Relict morphology is
present but more eroded than TRAPPIST-1 d's. Visible as smoothed
basaltic plains on the leading hemisphere, with occasional
fracture systems where the cooling magma contracted.

**Night-side cold trap.** Mercury hosts H₂O ice in permanently
shadowed polar craters (Lawrence 2013, Neumann 2013 MESSENGER
data). Proxima d, being tidally locked rather than rotating, has
a fixed anti-stellar point that is permanently dark and cold (~90 K
without atmospheric heat transport). Any volatiles delivered by
impact or photolytic transport from the dayside accumulate in
this region — H₂O ice, CO₂ ice, and possibly Na/K alkali frost.
Estimated coverage: ~5% of the anti-stellar hemisphere within
~30° of the cold pole.

**Crater morphology.** d's smaller mass + smaller gravity gives
larger crater diameters per impactor mass — typical crater
diameters might be 2× larger than equivalent Earth craters per
impactor. The leading hemisphere accumulates impacts preferentially.
Surface age: ~5 Gyr, mostly heavily cratered to lunar-highlands
density.

**Surface chemistry.** At 540 K substellar T:
- Active alkali volatilization (Na, K)
- Photolytic oxidation of basalt surface to hematite/ilmenite
- Possible aluminum/calcium silicate vapor transport in transient
  flare-driven heating events
- No carbonate-silicate cycle (no atmosphere)

The Na exosphere from alkali volatilization would be visible
through ground-based spectroscopy (Na D doublet absorption) if it
ever transits — but with no transit detected, this remains
unobserved.

## Atmosphere synthesis

**Canonical case: no atmosphere.** The combination of:
- (1) High XUV flux at 0.029 AU (~5× Earth-orbit values)
- (2) Low planet mass (0.32 M⊕) and surface gravity (0.74 g_E)
- (3) 5 Gyr cumulative escape history
- (4) Frequent flare events providing acute escape episodes

drives the dominant outcome: complete loss of any primary or
secondary atmosphere down to the bare-rock surface, with only
transient (~hours) exospheric features during outgassing or
volatile-impact events.

**Variant: thin CO₂ envelope.** If d outgassed CO₂ at a rate
similar to current Mars and the escape rate is at the lower end
of Tian 2015 predictions, a residual ~50 Pa CO₂ atmosphere could
persist. This is consistent with the JWST upper limit on similar
hot rocky exoplanets (Greene 2023 for TRAPPIST-1 b: < 0.5 bar
CO₂ at 99%). For NearStars cfg variant: ~50 Pa CO₂ + trace Na +
trace water vapor, with a barely detectable Rayleigh limb haze.

**No oceans, no clouds.** Even if water was delivered post-magma-
ocean phase, the dayside is too hot for liquid water (and too dry
without an atmosphere); the night-side cold-trap volatiles are
locked as frost, not free.

**Surface chemistry from flare impacts.** Each Proxima flare
(~10⁴/yr at d's orbit) deposits a UV+X-ray pulse that drives
surface photochemistry — slow oxidation of basalt to hematite,
chemical weathering of feldspars, and transient generation of
sodium and potassium vapor that condense back to the surface
within hours.

## Rotation & spin synthesis

Tidal locking is essentially certain (5.12 d period >> sync
timescale; Barnes 2017). Spin-orbit state:
- **1:1** (default, eccentricity ≈ 0). Adopted.
- 3:2 not possible at e = 0.

**Obliquity = 0.** Tidal damping over Gyr.

**No day-night cycle.** Substellar point fixed; only motion is
slow stellar rotation (83 d) of Proxima's disk in d's sky.

**Tidal heating.** With e ≈ 0 (Suárez Mascareño 2025), the tidal
heating contribution is negligible — Bolmont 2017 scaling gives
F_int ≈ 0.05 W/m², well below runaway threshold. The slight
upward eccentricity envelope from Faria 2022 (e ≤ 0.04) gives
upper limit F_int < 0.5 W/m², still sub-runaway.

**No seasons.** Same as TRAPPIST-1 d: constant insolation,
no diurnal cycle, no seasonal cycle.

## Visual styling

- **Global appearance.** Dark gray-brown bare-rock world under
  deep-red M-dwarf illumination. Visually similar to TRAPPIST-1 d
  but warmer/dimmer accent due to higher insolation and longer
  photolytic oxidation history.
- **Dayside.** Hot substellar zone (540 K) appears slightly
  blackbody-glowing if rendered at high dynamic range — the
  surface emits thermal IR strongly but visible-band emission
  is dim (kT ≈ 0.05 eV vs visible-band 1.5 eV). For KSP rendering,
  treat as reflective-only.
- **Terminator.** No atmospheric optical features. Sharp shadow
  transition at the terminator (no haze, no glow).
- **Nightside.** Very dark (~90 K). Tiny frost-cap region around
  anti-stellar point appears warm-cream (`#fff8e0`) if directly
  illuminated by Alpha AB starlight (rare geometry). Otherwise
  invisible.
- **Frost cap.** ~5% coverage centered on anti-stellar point.
  Visible from space when viewed from a Proxima b position with
  d in opposition — appears as a small bright spot on an
  otherwise dark hemisphere.
- **Atmosphere.** None canonical. If variant 50 Pa CO₂ enabled,
  add a thin pale-grey limb haze (~2 km thick) barely detectable.
- **Star in sky.** Proxima subtends ~2.6° (~5× Sun-from-Earth's
  apparent diameter). The largest stellar disk in any NearStars
  planet's sky. Deep red-orange with prominent visible starspot
  complexes.
- **Sister planet b in sky.** Proxima b at 0.0485 AU is further
  from Proxima than d (0.0288 AU). In conjunction, b passes at
  closest distance ~0.02 AU (~3 million km) — appears as bright
  ~mV -2 disk-resolved (~3') for several hours, then recedes.
- **Alpha AB in sky.** Brilliant point V ≈ -7, cream-yellow,
  ~2° from a slowly-drifting position. Bright enough to cast
  visible shadows; provides notable night-side illumination on
  the anti-stellar hemisphere.
- **Flare events.** Each Proxima flare delivers intense UV+visible
  brightening for minutes. d's dayside is briefly heated by
  10–100×; transient surface-volatile vaporization produces
  short-lived "auroral" emission from the resulting Na vapor cloud
  (though no actual aurora — no atmosphere). Looks like a brief
  red glow around the leading hemisphere.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2022A&A...658A.115F** Faria et al. 2022 — Proxima d discovery
  via ESPRESSO RV (Msini = 0.26 M⊕, P = 5.12 d). Definitive
  discovery characterization.
- **2025A&A...700A..11M** Suárez Mascareño et al. 2025 — Combined
  HARPS + ESPRESSO + NIRPS analysis. Refined parameters used as
  Phase 2 recommended.
- **2405.05013** Lobo & Bouchy 2024 — Potential surface ice
  distribution on close-in terrestrial exoplanets around M dwarfs.
  Directly addresses cold-trap ice deposits on M-dwarf planets in
  d's parameter regime. Drives the night-side frost cap visual.
- **2102.06318** Howard et al. 2018 — Proxima flare distribution.
  Scaled to d's orbit (0.029 AU) gives ~10⁴ flares/yr.

### Read (context / methodology, not decision-driving)

- **2204.09270** Diamond-Lowe et al. 2022 — Simultaneous X-ray +
  FUV monitoring of Proxima. Radiation environment.
- **MacGregor et al. 2018 (1803.07581)** — March 2016 ALMA
  superflare. Drives flare-event-rate envelope at d's orbit.
- **2402.00115** Yaptangco et al. 2025 — Short-timescale activity
  effects on transit detection. Context for non-detection of d
  transits.
- **2409.06637** Wanderley et al. 2024 — Magnetic fields in M
  dwarf planet hosts. Context for B-field environment.
- **2301.02477** Kossakowski et al. 2023 — Wolf 1069 b
  characterization. Comparable HZ-edge M-dwarf rocky planet;
  cross-reference for parameter envelope.
- **2304.09220** TOI-2095 paper — comparable system, methodology.
- **2207.13727** MIRECLE mission concept — future-instrument
  context for hot-rocky-planet characterization.

### Read (instrument-only, not visual-informative)

- **2504.18485** ESPRESSO iodine cell calibration. Methodology.
- **2102.01910** Optical SETI search of Proxima. Null result.
- **2311.04316** Planetary perturbers paper. Different system.
- **2209.11346** Multiple-star planet host catalog. Context.

### Not read — no arXiv preprint available (2 papers)

- "MOST Observations of Proxima Centauri" abstract — superseded
  by published Davenport 2016 paper which is already in the
  read set for Proxima Cen synthesis.

**User action requested.** None at this time. d is observationally
poorly constrained, so theoretical predictions dominate. If
post-2026 transit attempts succeed or direct imaging produces
phase-curve photometry, the surface temperature distribution
could be measured directly.

---

## Open items for follow-up

- The inclination of d's orbit is unconstrained. Adopted Msini →
  M_true factor 1.23 is statistical; direct mass measurement
  would tighten.
- The cold-trap volatile deposit (Lobo & Bouchy 2024 framework)
  is highly model-dependent. The 5% coverage estimate could be
  off by an order of magnitude in either direction.
- Magnetic field strength (0.5 μT) for a sub-Mars-mass body is
  poorly constrained by terrestrial scaling laws. RM22's
  framework was developed for Earth-mass bodies and may not
  extrapolate accurately to 0.32 M⊕.
- The variant 50 Pa CO₂ atmosphere is allowed by current limits
  but unobserved. Phase 4 cfg should explicitly support both
  bare-rock and thin-CO₂ variants.
- The Mercury polar volatile analog assumes similar impact-
  delivery rates and photolytic transport efficiency. These
  could differ for a tidally locked body around an M dwarf.
- Surface chemistry under M-dwarf XUV (alkali volatilization,
  hematite formation) needs laboratory validation under realistic
  flux conditions — current model assumes Earth-equivalent.
- The Suárez Mascareño 2025 eccentricity e = 0 is consistent
  with no tidal heating; if future RV data find non-zero e,
  the surface heat flux could approach habitable temperatures.
