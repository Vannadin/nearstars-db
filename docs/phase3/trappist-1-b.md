# TRAPPIST-1 b — Phase 3 Synthesis

TRAPPIST-1 b is a 1.12 R⊕, 1.37 M⊕ rocky planet on a 1.51-day orbit
around an M8V ultra-cool dwarf. It is the innermost of the seven
TRAPPIST-1 worlds and receives 4.3× Earth's insolation. JWST MIRI
secondary-eclipse measurements at 12.8 μm and 15 μm (Greene 2023,
Ducrot 2024) and a full thermal phase curve (Ducrot 2025) give the
cleanest "bare-rock" answer in the system: dayside brightness
temperature ≈ 490–503 K, no detectable nightside emission, no thermal
phase offset. Plausible atmospheres thicker than ~0.3 bar (with any
realistic CO₂ content) are ruled out at 3σ.

**Scenario choice for NearStars: airless ultramafic rocky surface
with localized fresh magma features near the substellar point.** This
matches the favored Ducrot 2024 interpretation (an unweathered
ultramafic surface implies recent / ongoing geological resurfacing)
and incorporates the induction-heating "exo-Io" hint from Grayver
2022 / Bolmont 2020. The alternative — a pure-CO₂ atmosphere with
photochemical haze and stratospheric inversion — is also formally
allowed by the data but disfavored on cosmochemical grounds (no
CO₂ would survive on TRAPPIST-1 c, two doors out, if b retained
one).

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 1.51 d orbit, tidal damping; Agol 2021 |
| `obliquity_deg` | 0 | high | tidal damping; Agol 2021 |
| `eccentricity` | 0.00622 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 337 | medium | Agol 2021 (low ecc → weak constraint) |
| `sidereal_period_days` | 1.5109 | high | Agol 2021 |
| `semi_major_axis_au` | 0.01154 | high | Agol 2021 |
| `mass_mearth` | 1.374 | high | Agol 2021 TTV |
| `radius_rearth` | 1.116 | high | Agol 2021; Greene 2023 transit fit |
| `surface_gravity_g_earth` | 1.103 | high | derived = 1.374 / 1.116² |
| `density_g_cc` | 5.43 | high | Agol 2021 |
| `insolation_s_earth` | 4.25 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 397 | high | Agol 2021 |
| `dayside_brightness_temp_k_15um` | 503 | high | Greene 2023 F1500W eclipse |
| `dayside_brightness_temp_k_phase_curve` | 490 | high | Ducrot 2025 MIRI 15 μm phase curve |
| `bond_albedo` | 0.0 | high | Greene 2023; Ducrot 2025 — dayside-only re-radiation |
| `atmosphere_present` | false | high | Ducrot 2025 phase curve excludes ≳1 bar greenhouse |
| `atmosphere_surface_pressure_pa` | 0 | high | Ih 2023 rules out plausible atmospheres > 0.3 bar |
| `atmosphere_composition` | n/a (airless) | high | Greene 2023; Zieba 2023 (sister-planet constraint) |
| `atmosphere_scale_height_km` | n/a | high | airless |
| `atmosphere_tint_rgb_hex` | n/a | high | airless |
| `dayside_surface_temp_k` | 503 | high | matches measured brightness temp; Ducrot 2025 |
| `substellar_peak_temp_k` | 620 | medium | derived bare-rock subsolar (A=0, ε=1, no advection) |
| `nightside_surface_temp_k` | 80 | medium | airless + no redistribution; passive radiative limit |
| `surface_tint_rgb_hex_primary` | `#1a1612` (dark ultramafic basalt) | medium | Ducrot 2024 "fresh ultramafic" + Moon mare analog |
| `surface_tint_rgb_hex_accent` | `#7a2a10` (cooling lava + iron oxide near substellar) | low | induction heating + fresh-melt patches; Grayver 2022 |
| `surface_morphology` | basaltic plains with fresh lava flows and dark magma ponds near substellar point | medium | Ducrot 2024 unweathered-surface inference; Grayver 2022 induction heating |
| `induction_heating_w_m2` | 0.4–4 | medium | Grayver 2022 (2211.06140) — non-magnetized layered-conductivity case; magnetized Earth-dynamo branch gives up to ~200 W/m² (139 TW over surface area) but no observational confirmation of b having a dynamo |
| `surface_ice_caps` | none (sublimation/photolysis on nightside) | high | dayside 500 K, no atmosphere to trap volatiles |
| `magnetic_field_strength_microtesla_equator` | 3 | low | RM22 (2203.01065) scaling + tidal-locking penalty; Garraffo 2017 tests 0.1–0.5 G bracket |
| `magnetic_dipole_moment_normalized_earth` | 0.08 | low | RM22 TESS tidally-locked rocky planet population 0.01–0.1 M_Earth |
| `magnetic_dipole_tilt_deg` | 10 | low | Tie-break (interesting-first per the interesting-first rule) — 10° gives offset auroral cap rather than uniform polar oval |
| `magnetosphere_standoff_planet_radii` | 1.5 | medium | Garraffo 2017 (1706.04617) Fig. 4 — innermost planet heavily compressed; field often opens to surface |
| `radiation_belt_present` | false | medium | Garraffo 2017 — open field lines, no stable trapped region |
| `surface_radiation_dose_msv_yr` | 80000 | low | Atri 2019 (1910.09871) scaled from e; vacuum-surface (no column shielding); Earth = 2.4 mSv/yr |
| `atmospheric_shielding_g_cm2` | 0 | high | Airless per Greene 2023 / Ducrot 2025 |
| `aurora_present` | false | high | No atmosphere → no auroral emission target |
| `induction_heating_magma_ocean_fraction` | 0.17 | medium | Kislyakova 2018 (1710.08761) — induction reaches 17% of radiogenic flux; magma ocean plausible |
| `star_apparent_angular_diameter_deg` | 5.51 | high | derived: 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |
| `tidal_heating_w_m2` | 0.5–1 (low-e) up to ~400 (max-e, JWST-capped) | medium | Bolmont 2026 (2601.03408) — internal-structure dependent; JWST nightside non-detection caps Φ at ~407 W/m² (Φ_2σ) |

## Surface synthesis

Ducrot 2024 finds two atmosphere-or-surface models that pass the
combined 12.8 / 15 μm eclipse fit: a thick pure-CO₂ atmosphere with
photochemical haze (creating a stratospheric inversion and the CO₂
feature in emission), and — preferred — an airless planet with an
**unweathered ultramafic surface**. The ultramafic interpretation
matters: weathered basalts on the Moon (regolith-aged) have low
broadband albedo but specific 15 μm emissivity that does not match
the data, whereas a fresh (geologically young) ultramafic surface
does. This implies ongoing or recent geological resurfacing.

The Ducrot 2025 phase curve consolidates this: no detected nightside
emission (≲39 ppm at 15 μm), no phase offset, and the dayside flux
matches a bare-rock model with low Bond albedo and inefficient heat
redistribution. The conclusion across the b literature is consistent:
**b is a bare, fresh, dark, hot rock.**

**Resurfacing mechanism.** Two physically plausible drivers:
(1) Tidal heating from the resonant chain. Bolmont 2026 (2601.03408)
revises older estimates substantially upward: for b's measured
core-mass-fraction range (Agol 2021: ~21 wt%) and the smallest plausible
eccentricity, surface flux is **~0.5–1 W/m² (nominal)**, comparable to
Io's ~2 W/m². Higher-eccentricity solutions reach 10²–10³ W/m² but are
ruled out by the JWST nightside constraint (Gillon 2025; T_2σ ≤ 291 K
→ Φ_2σ ≤ 407 W/m²). Even at the conservative ~0.5 W/m² value, tidal
heating dominates Mars's radiogenic ~0.04 W/m² by an order of magnitude.
(2) Magnetic induction heating (Grayver 2022, Cohen 2024) adds another
0.4–4 W/m² from the planet's motion through the stellar wind. The
combined heat budget easily sustains partial-melt volcanism. Given
the system's 7.6 Gyr age, the surface is continuously refreshed by
lava flows in regions of crustal weakness, biased toward the
substellar hemisphere where insolation pushes the upper crust closest
to solidus.

**Color choice.** The host star is a 2566 K M8V dwarf with SED peak
near 1.1 μm — surface reflectance perceived by a human observer is
strongly red-shifted regardless of intrinsic mineral color
(Domagal-Goldman 2010 for the general M-dwarf surface illumination
treatment). For a fresh ultramafic surface (komatiite / olivine-pyroxene
analogue, broadband visible albedo ≈ 0.03–0.08), the closest Solar
System reference is the dark dorsa of Mercury or the unweathered floor
of a young lunar crater. We pick `#1a1612` (very dark ultramafic)
primary, `#7a2a10` (cooling-lava red) accent biased toward the
substellar quadrant.

**Iron oxide.** Less prominent than on d. The "fresh" ultramafic
inference of Ducrot 2024 actively argues against significant
weathering, so we minimize iron-oxide patches relative to d. What
oxide there is should be biased to the terminator and antistellar
hemisphere, where surface material is exposed to stellar UV but not
recently resurfaced.

**Morphology.** Three contributing processes: (1) Continuous
resurfacing by partial-melt volcanism driven by tidal + induction
heating (Bolmont 2020, Grayver 2022), producing fresh lava flows and
shield-volcano features predominantly in the substellar hemisphere.
(2) ~8 Gyr of accumulated impacts, biased toward the leading
hemisphere in the locked frame, but partially erased by ongoing
volcanism. (3) Magma ocean relict features from the initial ~500 Myr
post-accretion phase (extensible to b from Piaulet 2025 §8's argument
for d, since b experienced an even more intense initial energy flux
and would have retained a magma ocean longer). Default texture: dark,
glassy basaltic plains with visible lava-flow channels radiating from
the substellar point and impact craters concentrating toward the
trailing-hemisphere highlands.

## Atmosphere synthesis

JWST MIRI 15 μm photometric eclipses (Greene 2023, five visits,
8.7σ detection) yield Fp/F★ = 861 ± 99 ppm, corresponding to a
dayside brightness temperature of ≈ 503 +26/-27 K. Ih 2023 used this
to bound atmospheric mass: any plausible atmosphere containing ≥100
ppm CO₂ is excluded above 0.3 bar at 3σ, and a Mars-like 6.5 mbar
pure-CO₂ atmosphere is also excluded at 3σ.

Ducrot 2024 added 12.8 μm eclipses (in-band for CO₂'s 15 μm feature)
and found Fp/F★ = 452 ± 86 ppm at 12.8 μm and 775 ± 90 ppm at 15 μm
(combined re-analysis). Two models survive at 2σ: an airless
ultramafic surface (preferred) and a thick pure-CO₂ atmosphere with
photochemical hazes producing a stratospheric inversion (caveat:
requires specific haze chemistry).

Ducrot 2025 closed the case: the MIRI 15 μm phase curve shows a
dayside brightness temperature of 490 ± 17 K, no nightside flux
detected (F_night,max = 39 +55/−27 ppm), and no measurable phase
offset. Atmosphere models with surface pressure ≥1 bar and any
significant greenhouse effect are excluded; b is "unlikely to possess
any substantial atmosphere."

Two theoretical papers reinforce the airless interpretation on
independent grounds. **2412.05188** (Chatterjee & Pierrehumbert 2024)
places b firmly inside the "catastrophic escape" regime of the
revised cosmic shoreline — even continuous volcanic outgassing cannot
rebuild a secondary atmosphere against b's current XUV flux (~10³ ×
F⊕,XUV; ~10⁴–10⁵ during the superluminous pre-main-sequence phase).
**1911.08878** (Turbet 2020) shows that b's maximum retained water
mass fraction is ≤ 2% for a terrestrial-core composition with the
measured loss rate of 0.19%/Gyr, implying b is "likely completely
dry today" — consistent with the airless surface.

**Initial-water inversion.** Gialluca 2024 (2405.02401) performs an MCMC fit using the joint constraint "b airless + c retains thin O₂" and finds initial surface water 8.2 +1.5/-1.0 Earth oceans (1σ). Mechanistically, ~3 TO sequestered in magma ocean, ~4 TO oxygen lost to hydrodynamic drag, ~385 bars dry crustal oxidation post-desiccation. The historical baseline of Bolmont 2017 (1605.00616) gave up to 13.5 EO H lost from b alone over the system's lifetime, producing up to ~422 bars of abiotic O₂ that could have built up if oxygen sinks were ineffective. The Gialluca refinement constrains both upper and lower bounds.

One methodological caveat: **2601.12556** (Wirth, Powell & Wordsworth
2026) finds that b has Λ ≤ 1 (Weak Temperature Gradient assumption
fails), so heat-redistribution-only bounds on b's atmosphere are
weaker than usually assumed. However, Ih 2023's 0.3-bar bound uses
direct 15 μm CO₂ molecular absorption (not redistribution) and still
holds. Ducrot 2025's phase curve also measures redistribution
directly, so this caveat does not change the airless decision.

For NearStars we adopt the **fully airless** interpretation:

- **Pressure.** 0 Pa exactly. The 12.8/15 μm-consistent "CO₂ + haze"
  scenario is dropped because it conflicts with the absence of CO₂
  on the neighboring planet c (Zieba 2023). If c — at lower
  insolation, closer to the cosmic shoreline — does not retain CO₂,
  b cannot plausibly hold a thicker one.
- **No surface volatiles.** Dayside temperatures of ~500 K
  immediately photolyse and thermally desorb any surface H₂O, CO₂,
  or SO₂. The nightside, while cold (~80 K), has no atmospheric
  transport so volatiles cannot cold-trap there.

**Sky appearance.** No atmosphere means no Rayleigh scattering and
no sky-color. The sky is uniformly black at every elevation.
TRAPPIST-1 dominates the sky at angular size 5.51° (over ten times
the Sun's angular size from Earth) — by far the largest single object
in the sky. Its color is deeply red-orange (≈2566 K blackbody → CIE
chromaticity near `#ff7a1a`). The other six TRAPPIST-1 planets
appear as bright stars in conjunction, with c (next planet out)
reaching ~0.7° at inferior conjunction.

**Radiation environment without an atmosphere.** With no atmospheric column to absorb energetic particles, b's surface receives the full M-dwarf wind and flare flux directly. Garraffo 2017 (1706.04617) and Cohen 2014 (1405.7707) simulations show the planetary magnetic field — even at Earth-like strength — is compressed to ~1.5 R_p by the stellar wind, and frequently opens directly to the surface during the planet's sub-Alfvénic crossings (≈50% of each orbit). Atri 2019 (1910.09871) gives a surface dose of ~80 Sv/yr under these conditions during typical flare activity, with single-flare spikes reaching 1–10 Gy. For Kerbalism cfg purposes this places b in the "lethal without active shielding" radiation bracket — crews on the surface accumulate lethal dose in minutes to hours, not days.

## Rotation & spin synthesis

The TRAPPIST-1 b system parameters force a strongly synchronous
configuration. Orbital eccentricity is small (0.00622; Agol 2021),
obliquity is damped to zero by tidal forces over the ≳7.6 Gyr system
age (Agol 2021 §6.2), and the spin-orbit resonance is most plausibly
1:1. Vinson 2017 and Makarov 2018 explored 3:2 alternatives for the
inner TRAPPIST-1 planets and concluded 1:1 is overwhelmingly favored
at b's eccentricity (3:2 is stable only for e ≳ 0.01).

**KSP implementation note.** Rotation period = orbital period =
1.5109 days (130 540 s). In Kopernicus the body's `rotationPeriod`
should equal the orbital `period` in seconds.

**No seasons.** With obliquity = 0 and essentially zero
eccentricity-driven libration, the substellar point is fixed in the
surface frame.

**Spin-orbit drift.** Lustig-Yaeger 2024 (2409.12065) computes a
small secular drift of the substellar point due to the chain's
n-body precession — at b's distance, the drift is ~0.6° per Myr,
negligible on KSP gameplay timescales but worth noting in the cfg
that the "substellar point" is a long-term mean. Revol 2024 (cited
in Bolmont 2026 / 2601.03408) finds an even longer "sidereal day"
of 69 yr for b under the full chain dynamics — again, irrelevant
to gameplay but a faithful annotation.

**Tidal Love number signature.** Bolmont 2020 (2002.02015) shows that the TRAPPIST-1 b TTVs hint at an anomalously high planetary Love number (k₂ ≳ 1.5, well above Earth's 0.299). If real, this is **direct dynamical evidence** for a liquid layer — likely the substellar magma reservoir already adopted in the surface synthesis. The signal is at the noise floor of current TTV fits, so the inference is tentative, but it independently supports the resurfacing interpretation.

**Magnetic dynamo expectation.** With 7.6 Gyr of system age and a tidally-locked 1.51-day rotation (slow compared to Earth's 1 day), b's internal dynamo is expected to be either weak-multipolar (RM22 / 2203.01065 scaling gives ~0.08 × Earth dipole moment) or absent. The induction heating from the stellar wind (Kislyakova 2018 / 1710.08761: 17% of radiogenic flux) keeps the deep interior warm enough that a frozen core is unlikely, so some residual dynamo activity is plausible. The cfg adopts ~3 μT surface field at the equator as a low-confidence estimate. This is enough field to produce a small magnetospheric "bubble" but not enough to deflect stellar wind from the surface during the system's frequent sub-Alfvénic phases.

## Visual styling

Combining the surface and atmosphere decisions:

- **Global color palette.** Dark ultramafic body (`#1a1612` primary,
  `#7a2a10` lava-red accent) seen under intense red-orange stellar
  light appears as a glowing-charcoal world. The substellar
  hemisphere has visible cooling-lava patches catching the stellar
  light; the antistellar hemisphere is near-black.
- **Dayside.** Bright substellar region (~503 K, ~230 °C) with
  textured low-relief lava plains. Substellar peak brightness in the
  cfg's PQS should reach `#a04020` (lava red-orange) within ~15° of
  substellar point.
- **Terminator band.** Narrow due to direct, low-redistribution
  illumination. High topographic contrast — basaltic ridges and
  impact crater rims throw long shadows in the grazing 2566 K light.
- **Nightside.** Cold (~80 K) and entirely dark; only thermal IR
  emission, no visible-band features. KSP nightside lighting should
  be near-zero ambient. The only visible sources are reflected light
  from neighboring planets (c reaches mv ≈ −13 at conjunction, like
  Earth's Moon).
- **No atmosphere haze.** Limb is sharp — no scattering, no
  refraction, no glow. The transition from disk to space is a clean
  edge.
- **Star in sky.** TRAPPIST-1 subtends 5.51° in b's sky (about 11×
  the Sun's angular size from Earth). Its color is deeply red-orange
  (≈2566 K → `#ff7a1a`), and the surface brightness is comparable to
  Mercury-from-Mercury solar brightness (~4.25 S⊕). At wavelengths
  beyond 1 μm the star is bright enough to show prominent solar
  flares (Howard 2023 in the d bibliography; Glazier 2020 for direct
  TRAPPIST-1 flare statistics) — for KSP, occasional flare lighting
  flickers would be a faithful but optional touch.
- **Sister planets in sky.** When in inferior conjunction with b,
  TRAPPIST-1 c (next out) appears at angular size ~0.7° (1.5× Earth's
  Moon). Near-coplanar geometry; these conjunctions occur every ~4
  days (b-c synodic period).
- **Magma ocean glow (optional).** If the substellar surface is
  truly close to solidus, very faint thermal red-orange emission at
  λ ≳ 2 μm might be visible at the substellar point during deep
  nightside flyovers in KSP — a low-priority visual easter egg.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2303.14849** Greene 2023 — JWST/MIRI F1500W secondary eclipse.
  Five visits, 8.7σ detection, Fp/F★ = 861 ± 99 ppm. Dayside
  brightness temperature ≈ 503 K. The discovery paper establishing b
  as a bare-rock candidate.
- **2412.11627** Ducrot 2024 — Combined 12.8 + 15 μm MIRI eclipse
  analysis. Identifies two surviving models: unweathered ultramafic
  airless surface (preferred) vs. thick CO₂ + photochemical haze
  with stratospheric inversion. Drives the surface composition
  decision and the "fresh / geologically active" interpretation.
- **2509.02128** Ducrot 2025 — JWST MIRI 15 μm thermal phase curve
  of b and c. Dayside T = 490 ± 17 K, no nightside emission, no
  phase offset. Definitively excludes ≳1 bar atmospheres. Closes the
  airless interpretation.
- **2305.10414** Ih 2023 — Self-consistent radiative-convective model
  bounding b's atmospheric thickness. Rules out plausible CO₂
  atmospheres > 0.3 bar at 3σ from the Greene 2023 data alone.
- **2509.02120** Constraints from 3D GCM (anonymized — see YAML for
  authors). Explores the family of atmospheres compatible with
  eclipses but ruled out by the phase curve. Reinforces the airless
  conclusion.
- **2412.05188** Chatterjee & Pierrehumbert 2024 — Cosmic shoreline
  with hydrodynamic escape physics. Places b firmly in the
  "catastrophic escape" regime; even outgassing cannot rebuild a
  secondary atmosphere. Theoretical justification for airlessness
  independent of JWST data.
- **2601.03408** Bolmont 2026 — Tidal-heating refinement using full
  interior structure + JWST nightside cap. Drives the upward revision
  of `tidal_heating_w_m2` from 0.04–0.2 to ~0.5–1 W/m² (nominal),
  with the JWST hard cap at 407 W/m² (Φ_2σ). Confirms that high-e,
  low-viscosity interior models for b are observationally excluded.
- **1911.08878** Turbet 2020 — Water mass-radius relationships for
  irradiated rocky planets. Caps b's retained water at ≤2% for an
  Earth-like core, supporting the "dry today" inference.
- **2405.02401** Gialluca 2024 — MCMC initial-water inversion from b/c JWST constraints. Initial water 8.2 +1.5/-1.0 TO. Strengthens b's airless interpretation and ties it to c's thin O₂ atmosphere.
- **2002.02015** Bolmont 2020 — TTV-derived tidal Love number for b. High k₂ ≳ 1.5 would dynamically signal a liquid magma layer; current TTV fits are at noise floor.
- **1605.00616** Bolmont 2017 — Historical baseline for water loss from terrestrial planets orbiting ultracool dwarfs. Up to 13.5 EO H lost from b over system age; up to ~422 bars abiotic O₂ possible. Foundational citation for the airless interpretation.
- **1706.04617** Garraffo 2017 — Threatening Magnetic and Plasma Environment of TRAPPIST-1. MHD simulations of planetary magnetospheres in the stellar wind. Sub-Alfvénic regime opens planetary field to surface for ~50% of each orbit.
- **2203.01065** RM22 (Internal Structures and Magnetic Moments) — Dynamo scaling for tidally-locked rocky planets gives 0.01–0.1 × Earth dipole moment.
- **1910.09871** Atri 2019 — Stellar Proton Event surface-dose calculations. Gives the per-event dose tables used for the radiation cfg.
- **1710.08761** Kislyakova 2018 — Induction heating drives magma-ocean possibility on b/c/d via stellar-wind-induced electromagnetic dissipation.
- **1405.7707** Cohen 2014 — Magnetospheric structure and atmospheric Joule heating for habitable-zone planets.

### Read (context / methodology, not decision-driving)

- **2309.07047** Lim 2023 — NIRISS transmission of b. Strong stellar
  contamination (spots in visit 1, faculae in visit 2). Cloud-free
  hydrogen-rich atmospheres rejected; cannot constrain secondary
  atmospheres. Important context that transmission spectroscopy on
  TRAPPIST-1 b is fundamentally limited by stellar variability.
- **2412.16541** Stellar contamination correction using back-to-back
  b/c transits. Methodology paper relevant to all TRAPPIST-1
  transmission work; not directly visual-informative.
- **2507.02052** Uniform reanalysis of JWST MIRI 15 μm eclipses
  (frame-normalized PCA). Cross-check on Greene 2023 / Zieba 2023
  reductions; consistent results.
- **1905.00512** Bolmont 2019 — Tidal parameters of b and c.
  Estimates tidal heating flux of 0.04–0.2 W/m² for b depending on
  interior Q. Used in the "resurfacing mechanism" discussion.
- **2502.00132** Way 2025 — TRAPPIST-1 d focus, but reviews b's
  status as an exo-Venus / exo-Dead candidate in its introduction.
  Already read for d Phase 3.
- **2601.12556** Wirth, Powell & Wordsworth 2026 — Analytic modeling
  of tidally-locked rocky planet atmospheres. Notes b has Λ ≤ 1
  (WTG assumption fails) so heat-redistribution-only bounds are weak;
  cited as a methodological caveat in the atmosphere synthesis. Does
  not change the airless decision because the molecular-absorption
  bounds (Ih 2023) and phase-curve heat-redistribution measurement
  (Ducrot 2025) are independent of WTG.
- **2512.07695** Allen 2025 — JWST TRAPPIST-1 e/b Program: First
  Observations. Uses b as airless stellar-contamination proxy for e.
  Reaffirms airless interpretation; no new b-specific constraints.
- **1806.10084** Unterborn 2018 — Updated compositional models for
  b/c. Interior degeneracy: small core consistent with no water,
  larger core would require volatile envelope. Superseded by Agol
  2021 + Turbet 2020 for the water-content question.

### Read (instrument-only, not visual-informative)

- **2203.04173** Rustamkulov 2022 — JWST NIRSpec lab time-series
  performance. Methodology only.

### Not read — no arXiv preprint or non-visual content (~30 papers)

The b bibliography includes ~30 papers without arXiv preprints, plus
~5 with arXiv but not visual-informative (instrument-only, biosignature
biosphere modeling, etc.). The most likely visual-informative items
in the not-read set:

- **2026NatAs.tmp...88** "The innermost planets in the TRAPPIST-1
  system do not have thick atmospheres" — likely Lustig-Yaeger-led
  recent Nature Astronomy summary. The arXiv preprint is on the way
  but not yet indexed at retrieval time (2026-05-21). **Flagged for
  re-fetch in a few weeks.**
- **2026NatAs.tmp...65G** "No thick atmosphere around TRAPPIST-1 b
  and c from JWST thermal phase curves" — likely the Nature
  Astronomy publication of Ducrot 2025 (already covered via the
  arXiv preprint 2509.02128). Skip.
- **2306.10150** Zieba 2023 — c's eclipse paper. Read in detail for
  c synthesis; mentioned here because b is the comparison planet
  throughout.

---

## Open items for follow-up

- Re-fetch the 2026 Nature Astronomy papers once arXiv preprints
  appear, in case the published versions tighten the atmosphere
  upper limits below the Ducrot 2025 / Greene 2023 values.
- Validate the "fresh ultramafic" surface decision against any
  future high-resolution JWST spectroscopy (e.g., MIRI MRS) that
  could resolve specific mineralogical features.
- Cross-check the `induction_heating_w_m2` range against more recent
  TRAPPIST-1 stellar-wind models if available — Cohen 2024 onward.
- Cfg variant: a "magma ocean residual" interpretation with a
  visible substellar lava lake. Lower probability but visually
  distinctive; could be implemented as a Phase 3.5 alternative.
- The magnetic field estimates are low-confidence scaling-relation values. If a direct measurement (radio non-detection upper limit) appears for b, the cfg field strength may need adjustment.
- Interesting-first tie-break: the magnetic dipole tilt of 10° was chosen to give a visually distinctive offset auroral cap rather than a uniform polar oval; both are physically plausible.

## Related

- [trappist-1-c](trappist-1-c.md) — adjacent sibling, also a JWST-tested bare-rock candidate (different surface weathering interpretation)
- [trappist-1-d](trappist-1-d.md) — next-but-one sibling; thin-atmo scenario contrasts with b's airless
- [trappist-1-e](trappist-1-e.md) — system's habitable-zone reference point; uses the same M8V host illumination
- [methodology](../reference/methodology.md) — schema for the Decisions table and confidence tags
- [mod-reference](../reference/mod-reference.md) — downstream KSP mods that consume these Phase 3 values
- [rex-data-comparison](../reference/rex-data-comparison.md) — §10 quantifies the Phase 3 → REX delta for the whole TRAPPIST-1 system; b's mass changed +62% post-Agol 2021
