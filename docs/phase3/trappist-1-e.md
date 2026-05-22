<!-- TRAPPIST-1 e Phase 3 synthesis: cfg-ready decisions and reasoning -->
# TRAPPIST-1 e — Phase 3 Synthesis

TRAPPIST-1 e is a 0.92 R⊕, 0.69 M⊕ rocky planet on a 6.10-day orbit
around an M8V ultra-cool dwarf. Fourth planet out, receiving 0.66×
Earth's insolation — squarely in the conservative habitable zone and
the **single most likely habitable world** in the TRAPPIST-1 system
(Wolf 2017, Turbet 2018, Lincowski 2018, Way 2025). Recent JWST NIRSpec
PRISM transmission spectra (Glidden et al. 2025 DREAMS, 4 visits)
suffer from significant stellar contamination but exclude H₂-rich
atmospheres and weakly disfavor Venus-analog CO₂-rich atmospheres at
2σ. N₂-rich atmospheres with trace CO₂ and CH₄ are fully permitted;
bare-rock interpretation is also consistent.

**Scenario choice for NearStars: temperate aqua-planet with a 1 bar
N₂/CO₂/H₂O atmosphere, ocean-bearing, tidally-locked "eyeball"
geometry with open water near the substellar point and ice at the
terminator and nightside.** This is the canonical "best habitable
candidate" cfg variant. It picks the Wolf 2017 / Turbet 2018 / Way
2025 aquaplanet scenario from among the (still observation-consistent)
options. The alternative bare-rock interpretation is preserved as
a backup cfg variant.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 6.10 d orbit, tidal damping; Agol 2021 |
| `obliquity_deg` | 0 | high | tidal damping; Agol 2021 |
| `eccentricity` | 0.00510 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 108 | medium | Agol 2021 (low ecc → weak constraint) |
| `sidereal_period_days` | 6.1010 | high | Agol 2021 |
| `semi_major_axis_au` | 0.02925 | high | Agol 2021 |
| `mass_mearth` | 0.692 | high | Agol 2021 TTV |
| `radius_rearth` | 0.920 | high | Agol 2021 |
| `surface_gravity_g_earth` | 0.818 | high | derived = 0.692 / 0.920² |
| `density_g_cc` | 4.92 | high | Agol 2021 (lower than Earth — water-rich interior) |
| `water_mass_fraction` | 0.05–0.10 | medium | Agol 2021 + Acuña 2021 — low-mass + lower-density consistent with several wt% H₂O |
| `insolation_s_earth` | 0.66 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 251 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.3) | 230 | high | derived; Earth-analog albedo |
| `bond_albedo` | 0.30 | medium | Earth + Hapi 2024 aqua-planet GCM range 0.25–0.35 |
| `surface_temp_substellar_k` | 290 | medium | Wolf 2017 GCM Aquaplanet; Turbet 2018 §4 |
| `surface_temp_nightside_k` | 230 | medium | Wolf 2017 GCM; ice-covered nightside |
| `surface_temp_global_mean_k` | 270 | medium | Wolf 2017 GCM Aquaplanet |
| `atmosphere_present` | true | high | adopted scenario; consistent with Glidden 2025 |
| `atmosphere_surface_pressure_pa` | 100 000 | medium | 1 bar canonical Earth-like; Glidden 2025 permits N₂-rich with trace CO₂ |
| `atmosphere_composition` | N₂ 78%, O₂ ~5% (low; abiotic), CO₂ ~1%, H₂O 0.1–1%, Ar 0.5% | medium | Wolf 2017, Lincowski 2018 aquaplanet equilibrium; CO₂ elevated vs. Earth for outer-HZ warming |
| `atmosphere_scale_height_km` | 9.5 | medium | derived: kT/μg with T≈270 K, μ=29, g=8.0 m/s² |
| `atmosphere_tint_rgb_hex` | `#5a7090` (muted blue with M-dwarf red shift) | medium | Rayleigh-blue under 2566 K illumination — heavily red-shifted toward dim cyan-gray |
| `cloud_cover_fraction` | 0.55 | medium | Wolf 2017 GCM Aquaplanet stratocumulus + cirrus (60% in Cohen 2022 UM); THAI II 4-GCM intercomparison (Sergeev 2022) gives 10–77% spread across LMD-G / ExoCAM / UM / ROCKE-3D — 0.55 sits in mid-range; confidence dropped from high |
| `subsurface_ocean_probability` | 0.876 | medium | Boldog 2023 (2312.01893) — top-target ranking for HZ |
| `cloud_morphology` | double mid-latitude bands + quasi-stationary substellar cluster | medium | Cohen 2022 UM and Wolf 2017 ROCKE-3D find double mid-latitude jet regime; THAI II shows e sits at the tipping point between equatorial-superrotation (3 of 4 GCMs in Hab 1) and mid-latitude (ROCKE-3D and UM with certain settings). The double-band cfg pick is one of two equally-supported outcomes. |
| `cloud_tint_rgb_hex` | `#c0a890` (warm cream — red-shifted water clouds) | medium | water cloud + 2566 K illumination → warm cream-orange |
| `ocean_present` | true (substellar open-water disk; ice elsewhere) | medium | Turbet 2018 aquaplanet; Pierrehumbert 2011 "eyeball Earth" morphology |
| `ocean_extent_substellar_radius_deg` | 35 | medium | Wolf 2017 Aquaplanet — open ocean within ~35° of substellar point |
| `ocean_tint_rgb_hex` | `#1a2540` (dark navy under low M-dwarf insolation) | low | deep ocean + faint red star → dark blue-violet |
| `surface_ice_caps` | full coverage outside substellar open-water disk; ~60% of surface | medium | Wolf 2017 Aquaplanet ice line at ~35° from substellar |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (snow / sea ice under M-dwarf light) | medium | water ice albedo 0.6–0.8 + red-shifted illumination |
| `surface_tint_rgb_hex_accent` | `#7a6a58` (exposed bedrock at ridge tops on terminator) | low | thin atmosphere + ice flow geometry |
| `surface_morphology` | ocean within ~35° of substellar; sea-ice + glacial terrain elsewhere; submerged + emerged terrain at ice boundary | medium | Hu 2014 / Pierrehumbert 2011 tidally-locked aquaplanet templates |
| `magnetic_field_present` | true (modest, ~0.1× Earth) | low | small mass + slow rotation → weak intrinsic field; not directly constrained |
| `induction_heating_w_m2` | 0.01–0.1 | medium | Grayver 2022 — much lower at e than at b/c |
| `tidal_heating_w_m2` | 0.001–0.01 | medium | Bolmont 2020 — minimal at e |
| `magnetic_field_strength_microtesla_equator` | 30 | medium | Wang 2025 (2504.16662) MHD simulations of e adopt 0.32 G ≈ Earth-strength; Garraffo 2017 test case 0.3 G. Documented divergence: see Canonical alternatives. RM22 dynamo scaling for tidally-locked low-mass planets gives ~2 μT; cfg picks Wang's Earth-analog assumption for visually distinctive magnetosphere. |
| `magnetic_dipole_moment_normalized_earth` | 0.3 | medium | Wang 2025 Earth-analog assumption; conservative for habitable-scenario rendering |
| `magnetic_dipole_tilt_deg` | 11 | medium | Earth-analog 11° (Wang 2025 uses 23.5° but reports tilt sensitivity); tie-break: Earth-like 11° gives recognizable auroral geometry for player |
| `magnetosphere_standoff_planet_radii` | 5 | high | Wang 2025 Fig. 5 for 0.32 G field — calm regime 5–9 R_e; CME-disrupted ~3 R_e |
| `radiation_belt_present` | true | medium | B-field ≥ 0.1 Earth + closed magnetosphere in calm regimes — Van-Allen-like belts possible, though heavily disturbed during sub-Alfvénic transits |
| `surface_radiation_dose_msv_yr` | 12000 | high | Atri 2019 (1910.09871) Table 6 for e at 0.028 AU + 1 bar column + Earth-like B-field; 5000× Earth's 2.4; spikes 10⁶ during hard-spectrum flares |
| `atmospheric_shielding_g_cm2` | 1000 | high | Phase 3 cfg pressure 1 bar Earth-like → ~1000 g/cm² column |
| `aurora_present` | true | high | Atm + magnetic field both substantial; Fraschetti 2019 (1902.03732) proton flux 10⁶× Earth → intense precipitation |
| `aurora_color_primary_hex` | `#4DFF4D` | medium | [OI] 557.7 nm green dominant in N₂/CO₂/O₂ atm — Earth-analog auroral color; interesting-first tie-break: green over UV-only alternative |
| `aurora_color_secondary_hex` | `#FF4D4D` | medium | CO₂⁺ Fox–Duffendack–Barker bands (580–700 nm red/orange) + N₂⁺ Meinel bands; tie-break: enhances visible palette diversity |
| `aurora_emission_species_primary` | `[OI] 557.7 nm + N₂⁺ 391.4 nm First Negative + CO₂⁺ doublet` | medium | Atm composition + standard aurora chemistry |
| `aurora_oval_magnetic_latitude_deg` | 50 | medium | Wang 2025 standoff 5 R_p; Vidotto 2013 Eq. 7 → α ≈ 27°, oval lat ~63°; allow expansion to ~50° during sub-Alfvénic transits |
| `aurora_intensity_kR_typical` | 150 | medium | Fraschetti 2019 proton flux up to 6 orders over Earth → aurora 15× Earth's typical 10 kR (conservative midrange) |
| `star_apparent_angular_diameter_deg` | 2.17 | high | derived: 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## Surface synthesis

TRAPPIST-1 e is the system's most likely habitable world. Three lines
of evidence converge:

1. **Insolation** (0.66 S⊕) places it inside the conservative
   habitable zone (Kopparapu 2013 / 2014) for any reasonable
   atmosphere with greenhouse warming. Without an atmosphere, e
   freezes; with 1 bar N₂/CO₂, it supports surface liquid water
   (Wolf 2017, Turbet 2018 §4).

2. **Density** (4.92 g/cc from Agol 2021) is lower than Earth's
   5.51 g/cc, consistent with a non-trivial water mass fraction.
   Magma-Ocean modeling (Bourgeois et al. 2024 — 2008.09599) gives
   a water mass fraction of 0–0.23 for e, with central estimates
   around 0.05–0.10 (several percent by mass = several Earth oceans
   worth of water).

3. **Observational consistency.** Glidden 2025 (DREAMS) rules out
   H₂-rich and weakly disfavors Venus-analog atmospheres, but
   explicitly permits N₂-rich atmospheres with trace CO₂ and CH₄ —
   exactly the canonical Earth-analog secondary atmosphere.

For the surface morphology, the tidally-locked aquaplanet template
(Pierrehumbert 2011, Hu & Yang 2014, Wolf 2017) gives a distinctive
"eyeball Earth" pattern:

- **Substellar disk** (≲35° from substellar point): open ocean, warm
  enough for liquid water (substellar surface temperature ~290 K in
  Wolf 2017 Aquaplanet scenario), possible cirrus clouds.
- **Mid-latitudes / mid-longitudes** (35–90° from substellar): sea
  ice with thickness varying from a few meters at the ice line to
  hundreds of meters near the terminator.
- **Terminator and nightside** (>90° from substellar): thick glacial
  ice (>1 km) over a frozen ocean; possible emerged terrain at ridge
  tops where ice has fractured around tectonic features.

**Color choice.** Two competing effects: (a) intrinsic ice/snow
albedo is high (0.6–0.8) and bluish-white, (b) the 2566 K M-dwarf
illumination shifts perceived hue strongly to red-orange. The
combination produces a warm cream-white for ice cover (`#d8d0c4`) and
a dark navy-violet for deep ocean (`#1a2540`). Hu 2014 explicitly
notes that aquaplanets around M-dwarfs appear "less blue" than Earth
because the stellar SED has minimal short-wavelength flux to
Rayleigh-scatter.

**Iron oxide / bedrock.** Limited exposure — most surface area is
ice-covered. Bedrock appearance limited to ridge tops near the
terminator where glacial flow has thinned ice. The accent `#7a6a58`
is a muted weathered-basalt tone under M-dwarf light.

**Morphology under tidal lock.** The substellar disk hosts active
hydrological circulation — surface heating drives evaporation,
condensation in the polar / nightside cold-traps creates persistent
glaciers, glacial flow returns water toward the substellar disk.
This pattern is stable on geological timescales (Wolf 2017 §6),
producing a planet with permanent climatic zones rather than
seasonal cycles.

## Atmosphere synthesis

Glidden 2025 (DREAMS NIRSpec PRISM, 4 transits) presents the first
JWST transmission spectra of e. Significant stellar contamination
across 0.6–5 μm complicates the inference, but after marginalizing
over stellar features with Gaussian processes they find:

- H₂-rich (≳80% by volume) cloudy atmospheres excluded at >3σ
- Venus-analog CO₂-rich atmospheres weakly disfavored at 2σ
- N₂-rich atmospheres with trace CO₂ and CH₄ are **fully permitted**
- Bare-rock interpretation also adequate but with unexplained features

This is consistent with — and rather supports — the Earth-analog
secondary atmosphere expected from Wolf 2017 / Lincowski 2018 / Way
2025 modeling.

For NearStars we adopt the **1 bar N₂-rich aquaplanet atmosphere**:

- **Pressure** 1 bar (100 kPa) — Earth-analog, comfortably within the Glidden 2025 N₂-rich consistency window.
- **Composition** N₂ 78%, Ar 0.5%, CO₂ 1% (elevated vs. Earth's 0.04% for outer-HZ greenhouse warming — Wolf 2017 finds 1–10× CO₂ enhancement needed for habitable surface; THAI II Hab 1 with only 400 ppm CO₂ gives global mean 232–246 K, ~25 K cooler than the warmer Hab 2 1-bar-CO₂ scenario; cfg's 1% CO₂ choice sits between Hab 1 and Hab 2), H₂O 0.1–1% (saturated near substellar surface), O₂ ~5% (abiotic photolysis).
- **Clouds.** THAI II 4-GCM intercomparison gives 10–77% cloud cover for Hab 1; the cfg's 0.55 fraction is the mid-range. ROCKE-3D high-cloud end may better match the warm temperate scenario; LMD-G low-cloud end is consistent with a colder, drier variant.

**Sky appearance.** The 1 bar N₂ atmosphere has Earth-like Rayleigh
scattering at short wavelengths, but the 2566 K stellar SED has
minimal flux below 0.5 μm — so the scattered sky color is much
dimmer and shifted toward orange compared to Earth's blue. The
zenith sky is a dim red-blue mix (~`#3a4060`), transitioning to a
warm orange near the horizon (`#a07050`). Water cloud features
appear as warm cream patches (`#c0a890`) catching the red stellar
light.

The host star dominates the daytime sky at angular size 2.17° (about
4× the Sun's angular size from Earth). Surface illumination at the
substellar point is about 0.66 × Earth's, similar to a heavily
overcast Earth day — but with the spectral peak shifted firmly into
the red/near-IR.

**Nightside.** No direct stellar illumination; the only light sources
are (a) scattered light from the dayside transported via atmospheric
circulation (negligible), (b) reflected light from sister planets
(f and d at conjunction, ~0.4–0.5° angular diameter, mv ≈ −10 to
−13), and (c) starlight from distant stars (visible because there
is no atmospheric scattering from the absent sun). Nightside sky
is dramatically dark — KSP nightside ambient should be ~1% of
dayside.

**Auroras as a defining visual feature.** With both a 1 bar atmosphere and the Earth-analog magnetic field adopted here (Wang 2025), e is the strongest aurora candidate in the system. The proton flux at e's orbit is ~10⁶× Earth's (Fraschetti 2019, 1902.03732), driving auroral intensities ~150 kR (15× Earth's typical 10 kR). The dominant emission is [OI] 557.7 nm green (Earth-aurora-analog), with secondary CO₂⁺ Fox–Duffendack–Barker bands giving a red-orange accent. Crucially, during the sub-Alfvénic transits that occupy 50–80% of each orbit (Garraffo 2017), the auroral oval expands from its calm-state magnetic latitude of ~60° down toward ~50° — visible from much of the nightside hemisphere, not just polar regions. For cfg rendering: a primary `#4DFF4D` green auroral band with a secondary `#FF4D4D` red-orange overlay, intensifying during flare events. Interesting-first tie-break: chose Earth-analog magnetic field strength (Wang 2025) over weaker-field alternatives, giving a recognizable auroral structure rather than disorganized polar precipitation.

## Rotation & spin synthesis

Tidal damping for e at 6.10-day period over 7.6 Gyr establishes the
synchronous (1:1) configuration unambiguously. Obliquity damped to
zero (Agol 2021 §6.2). Eccentricity is 0.00510 (Agol 2021), too low
for 3:2 spin-orbit (Vinson 2017).

**KSP implementation note.** Rotation period = orbital period =
6.1010 days (527 127 s). Kopernicus `rotationPeriod` should match the
orbital `period` in seconds.

**Slow rotation effects.** With a 6.1-day rotation period, Coriolis effects are weaker than on Earth. The THAI II 4-GCM intercomparison (Sergeev 2022, 2109.11459) shows e sits at the **tipping point** between two atmospheric circulation regimes: equatorial-jet ("Gill–Matsuno" superrotation, found in ExoCAM / LMD-G / UM Hab 1) and mid-latitude jet ("fast rotator", found in ROCKE-3D and in UM under Cohen 2022 setup). Both regimes produce different cloud morphologies — for NearStars we adopt the double-band mid-latitude jet visual (mean zonal wind ~18 m/s, Rossby gyres at 60–70°N/S, substellar cloud disk reaching ±30° in latitude), but the alternative equatorial-jet morphology (zonal cloud belt at low latitudes with mid-latitude clearer zones) is equally physically valid. The 20-day quasi-stationary cycle in cloud variability (Cohen 2022) is too slow to matter at KSP gameplay speeds.

**No seasons.** Obliquity = 0; libration-induced insolation variation
< 0.4%. The substellar point and its open-water disk are fixed in
the surface frame.

**Magnetic dynamo expectation.** e's mass (0.69 M⊕) and active interior (Bourgeois 2024 magma-ocean evolution; substantial water mass fraction) support a sustained dynamo despite the 6.1-day tidally-locked rotation. Wang 2025 (2504.16662) MHD simulations explicitly adopt 0.32 G Earth-analog surface field for habitability scenarios on e and find magnetopause standoff of 5–9 R_p in calm regimes (compressed to ~3 R_p during CMEs). The interesting-first tie-break favors this Earth-analog field over the alternative weak-field scenario (which would leave e effectively without magnetospheric protection during the system's frequent sub-Alfvénic episodes). For Kerbalism radiation modeling, a closed magnetosphere is assumed; the cfg places trapped-particle belts at 1.5–4 R_p in calm regimes, with significant variability tied to stellar wind state.

## Visual styling

Combining surface and atmosphere decisions:

- **Global appearance.** From orbit, e looks like a snowball with a
  warm-cream open-water "pupil" near the substellar point, ringed
  by a fractal sea-ice transition zone, and entirely white-cream
  glacial ice beyond. Persistent cloud cover (~55% global) softens
  the appearance, with stratocumulus over the substellar ocean and
  high cirrus over the ice zones.
- **Substellar disk (open water).** Dark navy ocean (`#1a2540`)
  under intense red-orange illumination, dotted with warm cream
  clouds (`#c0a890`). Most visually striking feature of the planet.
- **Ice transition band.** Fractal pattern of warm cream
  (`#d8d0c4`) ice and dark ocean (`#1a2540`) — broken sea ice with
  open leads. The transition radius is about 35° from substellar
  (Wolf 2017); KSP terrain should show this as a roughly circular
  ice line.
- **Glacial ice zone.** Smooth warm cream (`#d8d0c4`) with subtle
  topographic relief where glacial flow encounters bedrock. The
  terminator is the brightest zone in oblique illumination — long
  shadows reveal pressure ridges and crevasses.
- **Nightside.** Dark with a faint cyan-white sheen from
  starlight-reflecting ice. Visible features: pressure ridges,
  fractures, and the occasional refrozen lead. KSP nightside ambient
  ≈ 1% dayside; rendering should show ice-features only.
- **Atmosphere haze.** Pale gray-blue limb glow (`#5a7090`) about
  15–25 km thick — Rayleigh-scattered M-dwarf light. Significantly
  fainter than Earth's blue limb because of the M-dwarf SED.
- **Star in sky.** TRAPPIST-1 subtends 2.17° in e's sky (4× the Sun
  from Earth) — appears as a deep red-orange disk (`#ff7a1a`) about
  the size of a large dinner plate held at arm's length. The
  illumination on the surface feels like "perpetual sunset" at the
  substellar point, fading to dusk and full night moving away.
- **Sister planets in sky.** d (next inward) at angular size ~0.3°
  in conjunction; f (next outward) at ~0.4°. Conjunctions every few
  days due to the resonant chain. The full system is near-coplanar.

## Canonical alternatives

### Diverged cfg picks

| Field | Gameplay (in cfg) | Canonical alternative | Why diverged |
|---|---|---|---|
| `magnetic_field_strength_microtesla_equator` | 30 μT (Earth-analog; Wang 2025 0.32 G MHD scenario) | ~2 μT (RM22 dynamo scaling for tidally-locked low-mass planets; Reiners & Christensen 2010) | Wang 2025 *assumes* Earth-analog 0.32 G for habitability-scenario MHD; RM22 *derives* a weaker field from rotation-period dependence and core size. The cfg picks Wang's assumption because a strong magnetosphere + Earth-style auroral oval is recognizable to the player; a weak-field e would have disorganized polar precipitation with no clear visual hook. Weak-field reading preserved as cfg variant in Open items. |
| `magnetic_dipole_moment_normalized_earth` | 0.3 × Earth (downstream of field-strength choice) | <0.1 × Earth (downstream of RM22) | Follows from the field-strength choice; not an independent decision. |

## Bibliography

### Read (visual-informative, drove decisions above)

- **2509.05414** Glidden 2025 (DREAMS NIRSpec PRISM) — first JWST
  transmission spectra of e (4 visits). Excludes cloudy H₂-rich
  atmospheres at >3σ; constrains stellar contamination methods.
  Cornerstone observational paper.
- **2509.05407** Glidden 2025 (DREAMS Secondary Atmospheres) —
  companion paper. **N₂-rich atmospheres with trace CO₂ and CH₄
  fully permitted; weak disfavor of Venus-analog at 2σ.** Drives the
  scenario choice.
- **2510.18704** Bourgeois 2025 — Multimodel ensemble (photochemistry
  + 3D climate + transmission spectra) for e. Explores N₂/CO₂/CH₄/H₂O
  composition space, water clouds, and photochemical hazes. Informs
  the cloud cover fraction and atmospheric composition mix.
- **2502.00132** Way 2025 — ROCKE-3D GCM suite for TRAPPIST-1 d but
  with extensive comparison to e. Locates e in the habitable parameter
  space and discusses the Earth/Venus/Dead trichotomy. Already read
  for d Phase 3.
- **1809.07498** Lincowski 2018 — Evolved climates of all TRAPPIST-1
  planets. "Aqua planet e could maintain a temperate surface given
  Earth-like geological outgassing and CO₂." Directly motivates the
  aquaplanet cfg choice.
- **2006.11349** Wunderlich 2020 — Wet vs. dry atmospheres of e and
  f. Confirms e can be temperate with E-like geology + CO₂. Supports
  cfg composition decisions.
- **2008.09599** Bourgeois 2024 — Magma ocean evolution of e/f/g.
  Gives water mass fraction range 0–0.23 for e; sets the bedrock
  water budget. Used in surface synthesis.
- **2109.11457** Sergeev 2022 (THAI I) — Dry-case 4-GCM intercomparison for TRAPPIST-1 e. Baseline reference for the wet/dry comparison.
- **2109.11459** Sergeev 2022 (THAI II) — Moist-case 4-GCM intercomparison. Provides the 10–77% cloud cover spread and the equatorial-vs-mid-latitude jet regime tipping-point analysis. **Major refinement to the cfg's cloud morphology confidence.**
- **2109.11460** Fauchez 2022 (THAI III) — Simulated transmission spectra for e from the THAI suite. Constrains JWST detectability needs (Hab 1: 23–38 transits, Hab 2: 7–12 transits).
- **1902.03732** Fraschetti 2019 — Stellar Energetic Particle flux in TRAPPIST-1 HZ. Predicts proton flux ~10⁶× Earth's at e, but with two mitigating mechanisms (containment by stellar B-field, CME suppression). Supports keeping a magnetic field in the cfg without forcing a specific value. Also supports the auroral intensity estimate (10⁶× Earth proton flux → ~150 kR).
- **1706.04617** Garraffo 2017 — Threatening Magnetic and Plasma Environment of TRAPPIST-1. Sub-Alfvénic transits 50–80% of orbit; auroral oval geometry implications.
- **2504.16662** Wang 2025 — MHD simulations of TRAPPIST-1 e habitability with Earth-analog magnetic field. Drives the cfg's `magnetic_field_strength` value.
- **1910.09871** Atri 2019 — Stellar proton event surface dose; gives e's 12 Sv/yr baseline + 10⁶× Earth spike during flares.

### Read (context / methodology, not decision-driving)

- **2403.03403** How habitable are M dwarf exoplanets? Modeling
  surface conditions. General M-dwarf HZ context; not e-specific.
- **2412.10192** From CO₂- to H₂O-dominated atmospheres. Background
  on volatile cycling in habitable-zone planets; informs the CO₂
  fraction choice (1% rather than 0.04% for outer-HZ warming).
- **2206.00028** Felton 2022 — Atmospheric exchange biosignature
  false positives (O₂ from d transported to e). Already read for d
  Phase 3. Constrains the abiotic O₂ background but doesn't change
  the visual cfg.
- **2310.15992** New 2D Energy Balance Model for slowly-rotating
  tidally-locked planets. Methodology context for the substellar
  disk modeling.
- **2211.11887** Cohen 2022 — Traveling planetary-scale waves on
  tidally-locked aquaplanets, Met Office UM GCM. Drives the
  **cloud morphology** decision: e sits in the double mid-latitude
  jet regime (~18 m/s mean zonal wind), with substellar cloud disk
  reaching only ±30° in latitude. Two stationary Rossby gyres at
  60–70°N/S; eastern gyre oscillates on a ~20-day cycle. Mean
  cloud fraction 60%, confirming Wolf 2017.
- **2312.01893** Boldog 2023 — Water content of HZ rocky planets.
  e has subsurface ocean probability 87.56% (highest tier in their
  catalog). Rock-ice-boundary tidal heat 0.21 W/m² (range 0.18–0.24,
  much larger than surface flux). Supports the water-rich aquaplanet
  cfg choice.
- **1906.06797** Yamashiki 2019 — Stellar superflare habitability
  impact. TRAPPIST-1's Spot Maximum Flare = 9.09×10³² erg. With a
  1 bar N₂/O₂ atmosphere + Earth-level magnetic field, ground-level
  dose stays non-lethal even under Spot Maximum (≤1.18×10⁴ Sv at
  top-of-atmosphere → manageable at surface). Critical atmospheric
  column for complex life: ~2.04×10² g/cm² (20% Earth). Supports
  keeping the 1 bar atmosphere cfg.
- **2309.15239** + **2405.20167** Cooke 2023 / 2024 — WACCM6
  Earth-like-continents simulations for e. Global mean surface T
  219–231 K (cooler than Wolf 2017 aquaplanet's 270 K) because of
  realistic land-ocean partitioning. O₃ column 50–1310 DU
  depending on stellar UV scenario. The aquaplanet cfg chooses the
  warmer Wolf 2017 baseline; WACCM6 is a colder alternative for
  the "less habitable" cfg variant.
- **2601.18324** Bourgeois 2026 — Early Great Oxidation Event on
  TRAPPIST-1 e (~700 Myr earlier than Earth, K_oxy ~0.83 vs 1.0).
  M-dwarf UV distribution favors O₃ over O₂ photolysis, producing
  a thick O₃ layer at lower atmospheric O₂. Reinforces the cfg's
  inclusion of trace O₃ in atmospheric composition.
- **2305.08813** *(in d bibliography, not e)* Various contamination /
  characterization works — context only.

### Read (instrument-only, not visual-informative)

- **2203.04173** Rustamkulov 2022 — JWST NIRSpec lab time-series.
  Methodology only.
- **2407.19167** Machine-assisted biosignature classification. Not
  e-specific.

### Not read — no arXiv preprint or low-priority (~34 papers)

The e bibliography is the second-largest (64 papers, 30 with arXiv).
Most non-arXiv papers are conference abstracts on biosignatures or
ELT-specific characterization plans, not visual-informative.
Notable items skipped:

- **2024–2025 various** — biosignature feasibility studies and JWST
  proposal abstracts. Skip unless updating the cfg-relevant
  atmospheric composition.
- **Photochemistry program proposals** — methodology only.

---

## Open items for follow-up

- The Glidden 2025 DREAMS papers acknowledge "features which may be
  due to either uncorrected stellar contamination or planetary
  signal." If a future re-reduction or a new instrument (NIRISS,
  MIRI MRS) on e finds molecular features, the atmospheric
  composition table may need updating.
- The water mass fraction range (0.05–0.10 adopted) is the median
  of Bourgeois 2024's 0–0.23 — could narrow if Acuña 2025 or later
  interior fits improve.
- Cfg variant for the "Venus-analog" interpretation (1 bar CO₂ +
  H₂SO₄ clouds): visually distinctive yellow-cream world with no
  ocean. Weakly disfavored at 2σ by Glidden 2025 but not excluded.
- Cfg variant for the "bare-rock airless" interpretation: similar
  visuals to b/c but at e's much colder dayside temperatures (T_eq
  ≈ 250 K → mostly ice-coated bare rock).
- Cross-check the 5% abiotic O₂ choice — could be 10–20% in some
  Lincowski 2018 scenarios. Lower bound matches "minimum
  photolytic" expectation; upper bound is more "post-runaway".
- The cloud morphology between double-mid-latitude-jet and equatorial-superrotation is essentially a GCM-dependent prediction. If a future intercomparison resolves the tipping point, the cfg's `cloud_morphology` value (and possibly the visual rendering of cloud bands) may need updating.
- Interesting-first tie-break: chose Wang 2025's Earth-analog magnetic field (0.32 G) over the RM22 scaling estimate (~0.08 M_Earth, much weaker). The Earth-analog case produces a more visually distinctive magnetosphere + auroral oval; the weaker-field alternative is preserved as a cfg variant for users who prefer the conservative reading.
- The radiation dose figure (12 Sv/yr) places e in Kerbalism's "high-radiation" bracket. Aurora rendering at 150 kR will be dramatic; the user may want a brightness slider for gameplay.
