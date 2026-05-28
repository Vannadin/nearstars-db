# Teegarden's Star b — Phase 3 Synthesis

Teegarden's Star b is a 1.16 M⊕ minimum-mass rocky planet (probably
~1.34 M⊕ true mass at typical i = 60° geometric inclination; Fujii
2026) on a 4.91-day orbit around the M7.0 V host. The semi-major axis
of 0.0259 AU and the host bolometric luminosity of 7.32 × 10⁻⁴ L☉
combine to yield an insolation of 1.08 ± 0.08 S⊕ — slightly higher
than Earth's, placing b at the inner edge of the conservative habitable
zone. Equilibrium temperature with Bond albedo 0.3 is 277 ± 5 K
(Dreizler 2024); with zero albedo it is ~280 K (Fujii 2026 benchmark).
Both numbers straddle the freezing-point of water, making b one of the
most genuinely Earth-analog candidates in the NearStars catalog by
mass and insolation alone.

The planet is non-transiting; mass and radius are both derived rather
than measured. Mass comes from a multi-instrument RV fit (CARMENES +
ESPRESSO + MAROON-X + HPF, 355 nightly-binned measurements, Dreizler
2024). The cfg radius of 1.05 R⊕ follows the Zeng 2016 / 2019 Earth-
like-bulk mass-radius relation, as used uniformly by all the recent
GCM modelling papers (Boukrouche 2025, Fujii 2026, Hammond 2025 for
sister planets). The mass is a minimum mass (m sin i), so the true
mass-radius could be substantially higher at lower orbital
inclinations, but the radius prediction at 1.16-1.34 M⊕ is robust to
~5% across the various mass-radius scalings.

The defining cfg-relevant question for b is **runaway vs habitable**.
Boukrouche 2025 (arXiv:2510.11940) uses the Isca GCM at the Phase 2-
recommended stellar luminosity (instellation = 1481 W/m²) and finds b
remains comfortably below the runaway greenhouse threshold for **both**
α = 0.07 (ocean) and α = 0.30 (land) surface albedos — meaning a 1-bar
Earth-like atmosphere with present-day composition is sustainable. With
the Dreizler 2024 alternative stellar parameters (Teff = 3034 K,
R = 0.120 R☉) the instellation rises to 1565 W/m² and the same GCM puts
b past the runaway threshold. Phase 2 picked Schweitzer 2019's R = 0.107
R☉ as recommended; this synthesis adopts the corresponding **habitable**
cfg scenario. The runaway-variant cfg is preserved in Open items.

**Scenario choice for NearStars: temperate aquaplanet with 1-bar
Earth-like N₂/O₂/CO₂ atmosphere, ocean-bearing, tidally-locked
"eyeball" geometry with open water near the substellar point, a
high-altitude (1-10 mbar) stratospheric cloud deck, and sea-ice
elsewhere.** This is the showcase habitable cfg in the Teegarden
system. The alternative runaway-Venus cfg (consistent with the
Dreizler 2024 stellar-parameter side of the uncertainty) is preserved
as a backup variant in Open items.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | Wandel 2019 (Griessmeier 2009 timescale); Boukrouche 2025/26 GCM assumes 1:1 |
| `obliquity_deg` | 0 | high | tidal damping; Wandel 2019 |
| `eccentricity` | 0.03 | high | Dreizler 2024 |
| `argument_of_periastron_deg` | 338 | medium | Dreizler 2024 (poorly constrained at low e: +133/−100) |
| `sidereal_period_days` | 4.90634 | high | Dreizler 2024 |
| `semi_major_axis_au` | 0.0259 | high | Dreizler 2024 |
| `mass_mearth` | 1.16 (msini) | high | Dreizler 2024 — multi-instrument RV |
| `mass_estimate_mearth_true` | 1.34 (geometric i ≈ 60°) | medium | Fujii 2026 — used in 3D GCM |
| `radius_rearth` | 1.05 | medium | Zeng 2016 Earth-like MR; all GCM papers adopt this scaling |
| `surface_gravity_g_earth` | 1.21 | medium | derived = 1.16 / 1.05² |
| `density_g_cc` | 5.5 (Earth-like assumption) | low | no transit; assumed from Zeng 2016 MR |
| `insolation_s_earth` | 1.08 | high | Dreizler 2024 (Phase 2 stellar params) |
| `equilibrium_temp_k` (A=0) | 280 | high | Fujii 2026 benchmark |
| `equilibrium_temp_k` (A=0.3) | 277 | high | Dreizler 2024 table 4 |
| `bond_albedo` | 0.30 | medium | Earth-analog; Boukrouche 2025 α_s=0.30 land case used as cfg surface albedo proxy |
| `surface_temp_substellar_k` | 295 | medium | Boukrouche 2025 Isca GCM Earth-analog scenario substellar warm zone |
| `surface_temp_nightside_k` | 240 | medium | Boukrouche 2025 GCM nightside cold-trap |
| `surface_temp_global_mean_k` | 280 | medium | Boukrouche 2025 — habitable below runaway at 1481 W/m² |
| `atmosphere_present` | true | medium | Tie-break: no direct atmospheric detection (non-transiting); Wandel 2019 + Boukrouche 2025 GCM canonical Earth-analog scenario |
| `atmosphere_surface_pressure_pa` | 100 000 | medium | Tie-break: 1-bar Earth-analog adopted by Boukrouche 2025/26 and Fujii 2026 baseline |
| `atmosphere_composition` | N₂ 78%, O₂ 21% (abiotic photolytic), CO₂ 400 ppm, H₂O 0.1–1% saturated, Ar 0.5% | medium | Tie-break: Earth-analog from Boukrouche 2025/26 explicit composition; abiotic O₂ from H₂O photolysis at high M-dwarf XUV |
| `atmosphere_scale_height_km` | 8.1 | medium | derived: kT/μg with T=280 K, μ=29, g=11.9 m/s² |
| `atmosphere_tint_rgb_hex` | `#5a3a40` (deeper than TRAPPIST-1 e because M7 V SED is even more red-shifted) | medium | Tie-break: Rayleigh under 2904 K illumination — even less short-wavelength flux than M5.5V; dim cyan-gray-violet |
| `cloud_cover_fraction` | 0.55 | medium | Boukrouche 2025/26 Isca GCM — high cloud deck at 1-10 mbar plus mid-altitude clouds on terminators |
| `cloud_morphology` | High stratospheric cloud deck (1-10 mbar) on dayside; mid-altitude (200-500 mbar) ring at terminators where moist air condenses | medium | Boukrouche 2026 Fig. 1-2 — dayside cloud cover; substellar moisture transported to terminator cold-trap |
| `cloud_tint_rgb_hex` | `#c0a890` (warm cream — red-shifted water clouds under M7 V illumination) | medium | Tie-break: water cloud + 2904 K illumination; matches TRAPPIST-1 e convention |
| `ocean_present` | true (substellar open-water disk; ice elsewhere) | medium | Tie-break: Boukrouche 2025 ocean-albedo case (α_s=0.07) — open water sustainable on dayside |
| `ocean_extent_substellar_radius_deg` | 45 | medium | Tie-break: Boukrouche 2025 substellar warm zone radius (not explicitly tabulated but Fig. 1 shows ~40-50° of warm surface); larger than TRAPPIST-1 e's 35° due to higher insolation |
| `ocean_tint_rgb_hex` | `#1a2540` (dark navy — deep water under faint red star) | low | Tie-break: deep ocean + M7 V illumination; follows TRAPPIST-1 e convention |
| `surface_ice_caps` | sea-ice + glacial ice outside substellar open-water disk; ~50% of surface | medium | Boukrouche 2025 — ice line at ~45° from substellar at 1481 W/m² |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (snow / sea ice under M-dwarf light) | medium | water-ice albedo 0.6-0.8 + red-shifted illumination; matches TRAPPIST-1 e convention |
| `surface_tint_rgb_hex_accent` | `#8a6a48` (exposed bedrock at ridge tops on terminator) | low | thin atmosphere + ice flow geometry |
| `surface_morphology` | ocean within ~45° of substellar; sea-ice + glacial terrain at higher latitudes/longitudes; emerged bedrock at terminator pressure ridges | medium | Boukrouche 2025/26 Isca GCM; Pierrehumbert 2011 tidally-locked aquaplanet template |
| `magnetic_field_present` | true (modest) | low | Tie-break: no direct constraint; quiet old M dwarf supports atmospheric retention via Wandel 2019 argument |
| `magnetic_field_strength_microtesla_equator` | 25 | low | Tie-break: interesting-first; Earth-analog field assumed for visual aurora hook; no measurement |
| `magnetic_dipole_tilt_deg` | 11 | low | Tie-break: Earth-analog 11° for recognizable auroral geometry |
| `magnetosphere_standoff_planet_radii` | 6 | low | Tie-break: scaled from TRAPPIST-1 e Wang 2025 (5-9 R_p), adjusted upward because Teegarden's stellar wind ram pressure is much lower than TRAPPIST-1's |
| `aurora_present` | true | medium | Atm + magnetic field both substantial; M-dwarf SEP environment supports aurora |
| `aurora_color_primary_hex` | `#4DFF4D` | medium | Tie-break: [OI] 557.7 nm green in N₂/O₂/CO₂ atm — Earth-analog auroral colour |
| `aurora_intensity_kR_typical` | 30 | medium | Tie-break: 3× Earth's 10 kR (quiet star + modest field) — much lower than TRAPPIST-1 e's 150 kR because Teegarden flare rate is ~25× lower |
| `radiation_belt_present` | true (weak) | low | Tie-break: closed magnetosphere + low stellar wind ram pressure |
| `surface_radiation_dose_msv_yr` | 100 | low | Tie-break: 1-bar atmosphere + Earth-like B-field + quiet M7 V — much lower than TRAPPIST-1 e's 12 000 mSv/yr because stellar XUV and SEP fluxes are far weaker; no Atri-style published number for Teegarden |
| `atmospheric_shielding_g_cm2` | 1000 | high | 1-bar Earth-like → ~1000 g/cm² column |
| `star_apparent_angular_diameter_deg` | 2.20 | high | derived: 2 × R★/a × (180/π) = 2 × 0.107×0.00465 / 0.0259 × 57.3 = 2.20° |
| `stellar_illumination_color_temp_k` | 2904 | high | Cifuentes 2020 |

## Surface synthesis

Teegarden b is the system's most habitable candidate by every standard
metric. Three converging lines of evidence:

1. **Insolation** S = 1.08 ± 0.08 S⊕ (Dreizler 2024) — slightly above
   Earth's. With the recommended Phase 2 stellar parameters this
   corresponds to 1481 W/m² incident flux. Boukrouche 2025 (Isca GCM
   with present-day Earth atmospheric composition) explicitly finds
   that at 1481 W/m² b remains below the runaway greenhouse threshold
   for both ocean (α_s = 0.07) and land (α_s = 0.30) surface albedos.
   The alternative 1565 W/m² scenario (using Dreizler 2024 alternative
   stellar parameters) tips into runaway, but Phase 2 prefers the
   lower-luminosity Schweitzer / Cifuentes solution.

2. **Mass and bulk density.** With m sin i = 1.16 M⊕ and an
   assumed Zeng 2016 Earth-like radius of 1.05 R⊕, the inferred bulk
   density is ~5.5 g/cc — Earth-like, consistent with a silicate-iron
   rocky interior with a non-trivial water reservoir. The true mass at
   typical i = 60° geometric inclination is ~1.34 M⊕ (Fujii 2026); this
   doesn't change the radius prediction by more than ~5%.

3. **Theoretical habitability.** Wandel 2019 (arXiv:1906.07704) applies
   a 1D climate-habitability model and finds the habitable atmospheric
   heating range for b at S = 1.15 S⊕ extends across H_atm = 0.32 to
   3.7 for f = 0.5 (moderate atmospheric circulation) — i.e., from
   sub-Mars greenhouse all the way to substantial CO₂ enhancement.
   The Earth-analog atmosphere (H_atm ≈ 1) is comfortably inside this
   range.

For the surface morphology, the tidally-locked aquaplanet template
(Pierrehumbert 2011, Hu & Yang 2014, applied here via Boukrouche 2025
Isca GCM) gives a distinctive "eyeball Earth" pattern shifted slightly
warmer than the TRAPPIST-1 e analog:

- **Substellar warm zone** (≤ 45° from substellar point): open ocean
  for the α_s = 0.07 case; surface temperature ~295 K at substellar,
  dropping to ~265 K at the ice line. The warm-zone radius is ~10° larger
  than TRAPPIST-1 e's 35° because Teegarden b receives 1.6× more
  insolation.
- **Mid-latitudes / mid-longitudes** (45-90° from substellar): sea
  ice with thickness from a few meters at the ice line to tens of
  meters at the terminator.
- **Terminator and nightside** (>90° from substellar): thick glacial
  ice over a frozen ocean substrate; surface temperature ~240 K
  (Boukrouche 2025 GCM nightside).

**Colour choice.** Same as TRAPPIST-1 e — water-ice albedo is intrinsically
0.6-0.8 and bluish-white, but the 2904 K M7 V illumination shifts
perceived hue heavily toward red-orange. The combination produces a
warm cream-white for ice cover (`#d8d0c4`) and a dark navy-violet for
deep ocean (`#1a2540`). The substellar zone is the most visually
striking feature — a dark "pupil" of open water surrounded by a fractal
sea-ice transition band and uniform glacial ice farther out.

**Exposed bedrock.** Limited (~5-10% of surface area). Bedrock
exposure is concentrated at the terminator where glacial flow has
thinned ice over pressure ridges and where minor tectonic uplift could
expose dark mafic crust under the perpetually red-tinted illumination.
Accent tint `#8a6a48` reads as muted weathered basalt under M7 V
light.

## Atmosphere synthesis

The cfg adopts the **1-bar N₂-rich aquaplanet atmosphere** following
Boukrouche 2025 (Isca GCM) and Boukrouche 2026 (LIFE hemispheres
paper). The explicit composition used in those simulations is
essentially present-day Earth's:

- **Pressure** 1 bar (100 kPa) — Earth-analog, sustainable below
  runaway threshold at 1481 W/m² per Boukrouche 2025.
- **Composition** N₂ 78%, O₂ 21% (abiotic photolytic — the cfg
  assumes no biosphere; Lincowski 2018-style M-dwarf abiotic O₂
  buildup), CO₂ 400 ppm (Earth modern), CH₄ 1 ppm trace, H₂O 0.1-1%
  saturated, Ar 0.5%.
- **Clouds.** The Boukrouche 2026 Isca GCM Fig. 1-2 shows a high
  cloud deck around 1-10 mbar on the dayside (stratospheric for
  Earth) plus mid-altitude water clouds (~500 mbar) near terminators.
  Total cloud cover ~55% globally. The dayside high-cloud deck is
  optically thin enough not to dominate albedo — the outgoing longwave
  radiation pattern is driven primarily by atmospheric temperature
  structure, not cloud opacity. This is a key cfg distinction: unlike
  TRAPPIST-1 e (where mid-altitude stratocumulus dominate), b's
  dayside cloud signature is in the stratosphere.

**Sky appearance.** The 1-bar N₂ atmosphere has Earth-like Rayleigh
scattering at short wavelengths, but the 2904 K stellar SED has almost
no flux below 0.5 μm — so the scattered sky color is dim and
shifted strongly toward red-orange. The zenith sky is a dim red-blue
mix (~`#3a3040`), transitioning to a warm orange near the horizon
(~`#a06040`). Water cloud features appear as warm cream patches
(`#c0a890`) catching the red stellar light.

The host star dominates the daytime sky at angular size 2.20° (about
4× the Sun's angular size from Earth, comparable to TRAPPIST-1 e's
view of TRAPPIST-1). Surface illumination at the substellar point is
about 1.08 × Earth's bolometric flux — but with the spectral peak in
the near-infrared, the visible-light illumination is more like a
heavily overcast Earth afternoon.

**Nightside.** No direct stellar illumination; the only light sources
are (a) scattered light from the dayside transported via atmospheric
circulation (small but non-negligible — Boukrouche 2025 GCM shows
nightside temperatures ~240 K maintained by ~50 W/m² advected heat),
(b) reflected light from sister planets c and d at conjunction (~0.3°
angular diameter, m_v ≈ −8 to −10), and (c) starlight from background
stars. Nightside sky is dim but not completely dark — KSP nightside
ambient should be ~3-5% of dayside.

**Atmospheric escape.** Old age (8 Gyr) + low current XUV flux + quiet
star give Teegarden b far better atmospheric retention prospects than
either Proxima b or TRAPPIST-1 d. Wandel 2019 §3.1 reviews
Lammer-style erosion models and notes that the present-day stellar
wind is too weak to strip an Earth-mass atmosphere; the early pre-main-
sequence phase (which lasted ~1 Gyr for ultra-cool dwarfs of
Teegarden's mass) was hotter and more active and may have stripped any
primordial H/He envelope, but a heavy-element secondary atmosphere
acquired by late accretion / outgassing should survive. The L_X / L_bol
= −4.9 today is high in relative terms but the absolute L_X ≈ 3.7 ×
10²⁵ erg/s gives only 1/10⁵ of the Sun's X-ray flux at Earth — Boukrouche
2025 GCM does not include atmospheric escape but assumes Earth-like
composition holds.

**Auroras** are a present but muted visual feature. With a 1-bar
atmosphere and an Earth-analog magnetic field (tie-break assumption),
b should support polar auroral ovals at the canonical ~60° magnetic
latitude. Because Teegarden produces only ~0.4 large (≥10³⁵ erg) flares
per year and ~2.6 modest (~10³² erg) flares per 100 days (Fuhrmeister
2024 + Dreizler 2024), the auroral intensity is far below TRAPPIST-1
e's 150 kR — the cfg adopts 30 kR (3× Earth's typical 10 kR) for a
recognizable but understated auroral palette. Dominant emission is
[OI] 557.7 nm green (Earth-analog colour `#4DFF4D`), with weaker N₂⁺
391.4 nm violet contribution.

## Rotation & spin synthesis

Tidal damping for b at 4.91-day period over 8 Gyr establishes
synchronous (1:1) rotation unambiguously (Griessmeier 2009 timescale ≪
8 Gyr at this orbital distance and mass). Obliquity damped to zero.
Eccentricity is 0.03 (Dreizler 2024), too low for 3:2 spin-orbit
resonance (Vinson 2017).

**KSP implementation note.** Rotation period = orbital period =
4.90634 days (423 668 s). Kopernicus `rotationPeriod` should match the
orbital `period` in seconds.

**Atmospheric circulation regime.** Boukrouche 2025/26 Isca GCM and
Hammond 2025 ExoCAM GCM (the latter for c, but the dynamical regime
extrapolates) both find equatorial superrotation — a single broad
prograde zonal jet driven by the stationary thermal forcing of the
substellar dayside. The Boukrouche 2026 explicit cloud-fraction Fig. 2
shows the dayside cloud disk centred on the substellar point with a
tail extending eastward, consistent with the Matsuno-Gill pattern of
tidally-locked atmospheric circulation. There is no obvious
mid-latitude jet bifurcation seen at TRAPPIST-1 e — b is fully on the
"superrotation" side of the dynamical phase diagram (Haqq-Misra 2018),
because b is hotter (1.08 vs 0.66 S⊕).

**No seasons.** Obliquity = 0; libration-induced insolation variation
< 0.3%. The substellar point and its open-water disk are fixed in
the surface frame.

**Magnetic dynamo.** b's mass (1.16-1.34 M⊕) and likely active
interior (Earth-analog assumed) should support a sustained dynamo
despite the synchronous 4.91-day rotation — the dynamo is driven by
core convection, not surface rotation, and Earth's 27-day Moon-induced
synchronous-rotation thought experiment retains a dynamo on theoretical
grounds. The cfg therefore picks a modest Earth-analog field (25 μT
equatorial surface) as an interesting-first tie-break, giving a
visible auroral structure for player navigation.

## Visual styling

Combining surface and atmosphere decisions, b renders as a slightly
warmer cousin of TRAPPIST-1 e:

- **Global appearance from orbit.** A snowball with a warm-cream open-
  water "pupil" ~45° from substellar, ringed by a fractal sea-ice
  transition band, and entirely white-cream glacial ice beyond. The
  stratospheric cloud deck (1-10 mbar) creates a high, thin, even
  haze that softens the substellar contrast — the cloud features
  appear more diffuse than TRAPPIST-1 e's mid-altitude stratocumulus.
- **Substellar disk (open water).** Dark navy ocean (`#1a2540`)
  under intense red-orange illumination, dotted with warm cream
  cirrus-equivalent clouds (`#c0a890`). The substellar warm zone is
  the most visually striking feature.
- **Ice transition band.** Fractal pattern of warm cream (`#d8d0c4`)
  ice and dark ocean (`#1a2540`) — broken sea ice with open leads.
  The transition radius is ~45° from substellar.
- **Glacial ice zone.** Smooth warm cream (`#d8d0c4`) with subtle
  topographic relief where glacial flow encounters bedrock. The
  terminator is the brightest zone in oblique illumination — long
  shadows reveal pressure ridges and crevasses; here the accent
  `#8a6a48` exposed bedrock peeks through.
- **Nightside.** Dimly visible (~3-5% of dayside) due to advected
  atmospheric heat-redistribution warmth. Visible features: pressure
  ridges, fractures, refrozen leads, faint auroral ovals at ~60°
  magnetic latitude.
- **Atmosphere haze.** Pale gray-blue-violet limb glow (`#5a3a40`)
  about 12-20 km thick — Rayleigh-scattered M7 V light. Significantly
  fainter than Earth's blue limb because the M-dwarf SED has minimal
  short-wavelength flux to scatter.
- **Star in sky.** Teegarden's Star subtends 2.20° in b's sky (4× the
  Sun from Earth) — appears as a deep red-orange disk (`#b03020`)
  comparable in apparent size to TRAPPIST-1 e's view of TRAPPIST-1.
  Illumination is "perpetual sunset" at substellar, fading to dusk
  and full night moving toward the terminator.
- **Sister planets in sky.** c at conjunction (~0.3° angular diameter,
  m_v ≈ −8); d at conjunction (~0.2°, m_v ≈ −5). Conjunctions every
  6-10 days for c and ~26 days for d, near-coplanar by RV evidence
  (Dreizler 2024 dynamical stability analysis).

## Bibliography

### Read (visual-informative, drove decisions above)

- **Zechmeister M. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Two temperate Earth-mass planet candidates around
  Teegarden's Star*, A&A 627, A49 (`2019A&A...627A..49Z`,
  arXiv:1906.07196). Discovery of b and c. Initial mass and orbit.
- **Dreizler S. et al. 2024** — *Teegarden's Star revisited*, A&A 684,
  A117 (`2024A&A...684A.117D`, arXiv:2402.00923). Refined b orbit
  (P = 4.90634 d, e = 0.03, msini = 1.16 M⊕, T_eq = 277 K, S = 1.08 S⊕).
- **Wandel A. & Tal-Or L. 2019** — *On the Habitability of Teegarden's
  Star planets*, ApJ 880, L21 (`2019ApJ...880L..21W`, arXiv:1906.07704).
  Analytic 1D habitability model — b habitable range H_atm = 0.32-3.7.
- **Boukrouche R., Caballero R., Lewis N. T. 2025** — *Near the
  Runaway: The Climate and Habitability of Teegarden's Star b*, ApJ
  993, L19 (`2025ApJ...993L..19B`, arXiv:2510.11940). Isca GCM at
  1481 W/m² — b habitable for α_s = 0.07 AND 0.30; 1565 W/m² beyond
  runaway. Critical paper for the cfg's habitable-scenario choice.
- **Boukrouche R. et al. 2024** — *The Impact of Water Clouds on the
  Prospective Emission Spectrum of Teegarden's Star b as Observed by
  LIFE*, ApJ 977, 88 (`2024ApJ...977...88B`, arXiv:2411.07922). Water
  cloud cover detectability with LIFE — confirms cloud cover as
  habitability tracer.
- **Boukrouche R. & Janson M. 2026** — *Disentangling the Hemispheres
  of Teegarden's Star b with LIFE*, ApJ 996, L43 (`2026ApJ...996L..43B`,
  arXiv:2512.19231). Isca GCM hemisphere maps; high cloud deck at
  1-10 mbar; LIFE 3-day broadband 1σ hemisphere distinction.
- **Fujii Y. et al. 2026** — *Probing Thermal Gradient of Habitable-
  zone Rocky Planets as an Anti-indicator of a Global Surface Ocean
  Using Mid-infrared Direct Imaging*, AJ 171, 155 (`2026AJ....171..155F`,
  arXiv:2512.16575). ROCKE-3D ocean-vs-no-ocean scenarios for b at 1
  and 10 bar; LIFE can distinguish in 1 day at two phases. Gives
  T_eq(A=0) = 280 K benchmark.

### Read (context / methodology, not decision-driving)

- **Hammond T. et al. 2025** — Climate of nearby temperate rocky
  targets (arXiv:2504.00978). Used directly for Teegarden c; relevant
  for b as context (b not in their snowball list — habitable in their
  ExoCAM grid).
- **Schweitzer A. et al. 2019** — Stellar parameters (arXiv:1904.03231),
  used via host star.
- **Fuhrmeister B. et al. 2024** — Stellar activity context for
  atmospheric retention (arXiv:2504.02338).

### Read (instrument / non-cfg-decisive)

- **Mandell A. et al. 2022** — MIRECLE mission concept; cited as PIE
  context.
- **Hill M. L. et al. 2023** — Catalog of Habitable Zone Exoplanets
  (`2023AJ....165...34H`, arXiv:2304.13417). Catalog-only entry; b
  ranks high but adds no measurement.

### Not read — no arXiv preprint or low-priority

The b bibliography is small (14 papers, 9 with arXiv). Five non-arXiv
papers are catalog entries or short conference proceedings; all are
preserved in `docs/phase3/_bib/teegarden-s-star-b.yaml` with `status:
skipped` where appropriate.

## Open items for follow-up

- **Stellar-parameter ambiguity for runaway threshold** (CRITICAL):
  Boukrouche 2025 explicitly notes that at 1565 W/m² (the Dreizler
  2024 alternative stellar params) b is **beyond** the runaway
  greenhouse threshold. Phase 2 picked the lower-luminosity Schweitzer
  params (1481 W/m²) keeping b habitable. If future stellar parameter
  refinement (interferometry, JWST occultation, asteroseismic-impossible-
  for-M7) favors the Dreizler higher-R, the cfg should switch to a
  **runaway Venus-analog variant**: 1-100 bar CO₂ atmosphere, no
  surface water, hot dayside (~700 K), thick sulfuric acid clouds, no
  ice anywhere. Preserved as backup variant.
- **True mass at low inclination**: If the orbital inclination is
  much less than 60°, the true mass could be 1.5-3 M⊕ and the planet
  could be a mini-Neptune rather than rocky. Fujii 2026 explicitly
  takes i = 60° geometric for the 1.34 M⊕ estimate. Astrometric
  detection by Gaia DR4 or Theia could constrain inclination.
- **Cloud morphology dependence on GCM**: Boukrouche 2026's Isca GCM
  gives a high stratospheric cloud deck dominating the dayside emission
  pattern. Hammond 2025's ExoCAM gives mid-altitude clouds for sister
  planets. The cfg's stratospheric-cloud pick may shift if a future
  GCM intercomparison (THAI-style) for b changes the consensus.
- **No transit confirmation**: All planetary parameters are RV-derived.
  A transit detection from CHEOPS or a focused TESS revisit (low
  probability for non-transiting geometry) would directly measure
  radius and tighten the atmospheric column.
- **Auroral intensity / shielding**: The cfg's 30 kR and 100 mSv/yr
  numbers are scaled from TRAPPIST-1 e by activity ratio. A Teegarden-
  specific SEP+atmosphere model (Atri-style) does not exist yet.
- **Magnetic field strength**: No measurement. The cfg picks Earth-
  analog 25 μT as interesting-first. A weaker scaling (RM22-style for
  tidally-locked low-mass planets) would give ~3 μT and weaker
  auroras.

## Related

- [teegardens-star](teegardens-star.md) — M7 V host
- [teegardens-star-c](teegardens-star-c.md) — outer sibling, snowball candidate
- [teegardens-star-d](teegardens-star-d.md) — outermost, outside HZ
- [trappist-1-e](trappist-1-e.md) — structurally similar (M-dwarf HZ aquaplanet); b is warmer
- [proxima-cen-b](proxima-cen-b.md) — direct comparator; Proxima b is more flare-stressed
- [methodology](../reference/methodology.md) — Decisions schema
- [rex-data-comparison](../reference/rex-data-comparison.md) — Teegarden b is among the highest-ESI planets in the HZ catalogues
