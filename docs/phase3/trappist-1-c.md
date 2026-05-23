---
type: entity
entity_kind: planet
title: "TRAPPIST-1 c"
slug: trappist-1-c
kopernicus_name: Trappist1c
host_star: Trappist1
cluster: system-trappist-1
cluster_role: member
sources: ["Agol 2021", "Zieba 2023", "Ducrot 2025", "Lincowski 2018", "Lincowski 2023", "Luger and Barnes 2015", "Acuña 2021", "Barr 2018", "Dobos 2019"]
related: [[trappist-1-b]], [[trappist-1-d]], [[trappist-1-e]], [[methodology]], [[mod-reference]], [[rex-data-comparison]]
created: 2026-05-21
updated: 2026-05-24
confidence: medium
scenario: thin O₂-dominated atmosphere (~0.1 bar) over dark basaltic surface
tier: public
---

# TRAPPIST-1 c — Phase 3 Synthesis

TRAPPIST-1 c is a 1.10 R⊕, 1.31 M⊕ rocky planet on a 2.42-day orbit
around an M8V ultra-cool dwarf. Second planet out, receiving 2.27×
Earth's insolation. JWST MIRI 15 μm secondary-eclipse (Zieba 2023) and
phase-curve (Ducrot 2025) measurements give a dayside brightness
temperature of 369–380 K — consistent with either a bare rock or a
thin O₂-dominated atmosphere. Cloud-free O₂/CO₂ mixtures from 10 bar
(10 ppm CO₂) down to 0.1 bar (pure CO₂) are ruled out; a Venus-analog
with sulfuric-acid clouds is disfavored at 2.6σ.

**Scenario choice for NearStars: thin O₂-dominated atmosphere
(~0.1 bar) with trace H₂O vapor, no significant CO₂, over a dark
basaltic surface.** This adopts the "fossil oxygen" scenario from
Luger & Barnes 2015 / Lincowski 2018 / Lincowski 2023: an initial
H₂O-rich steam atmosphere underwent hydrodynamic H escape during the
young M-dwarf's high-luminosity pre-main-sequence phase, stripping
hydrogen and leaving photolytic O₂ behind. The remaining surface is
weathered (unlike b's fresh ultramafic), with mature regolith. This
is distinct from b (airless, fresh) and from d (thin atmo with
terminator H₂O ice clouds) while staying observation-consistent.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 2.42 d orbit, tidal damping; Agol 2021 |
| `obliquity_deg` | 0 | high | tidal damping; Agol 2021 |
| `eccentricity` | 0.00654 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 282 | medium | Agol 2021 (low ecc → weak constraint) |
| `sidereal_period_days` | 2.4219 | high | Agol 2021 |
| `semi_major_axis_au` | 0.01580 | high | Agol 2021 |
| `mass_mearth` | 1.308 | high | Agol 2021 TTV |
| `radius_rearth` | 1.097 | high | Agol 2021 |
| `surface_gravity_g_earth` | 1.087 | high | derived = 1.308 / 1.097² |
| `density_g_cc` | 6.36 | high | derived; Agol 2021 reports ~5.7 (uncertainty bars overlap) |
| `insolation_s_earth` | 2.27 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 339 | high | Agol 2021 |
| `dayside_brightness_temp_k_15um` | 380 | high | Zieba 2023 MIRI F1500W eclipse |
| `dayside_brightness_temp_k_phase_curve` | 369 | high | Ducrot 2025 MIRI 15 μm phase curve |
| `bond_albedo` | 0.05 | medium | constrained between 0 (bare rock) and ~0.3 (reflective) by Ducrot 2025 |
| `atmosphere_present` | true (thin) | low | adopted O₂-dominated; (A) airless also defensible |
| `atmosphere_surface_pressure_pa` | 10 000 | medium | 0.1 bar O₂ at the upper edge of Lincowski 2023's 1σ-consistent envelope |
| `atmosphere_composition` | O₂ 98%, trace H₂O / O₃ / CO₂ ≲100 ppm | medium | Lincowski 2018 photolytic-oxygen prediction; Lincowski 2023 fit |
| `atmosphere_scale_height_km` | 10 | medium | derived: kT/μg with T≈370 K, μ=32 (O₂), g=10.7 m/s² |
| `atmosphere_tint_rgb_hex` | `#3a3a40` (very faint O₂ Rayleigh + thin O₃ Chappuis absorption) | low | scattering minimal at 0.1 bar; O₃ adds slight gray-blue tint under M-dwarf illumination |
| `dayside_surface_temp_k` | 369 | high | matches phase-curve measured brightness |
| `substellar_peak_temp_k` | 430 | medium | derived bare-surface subsolar (A=0.05, ε=1, weak advection) |
| `nightside_surface_temp_k` | 140 | medium | weak advection from thin O₂ atmo; Ducrot 2025 nightside < ~150 K |
| `surface_tint_rgb_hex_primary` | `#2c2218` (weathered basalt) | medium | aged basaltic surface, no recent volcanism; Mercury-mature regolith analog |
| `surface_tint_rgb_hex_accent` | `#604030` (iron oxide patches, photolytic) | low | UV photolysis on long-tidally-locked surface; Turbet 2018 mechanism |
| `surface_morphology` | weathered basaltic plains; aged impact craters; subdued relief | medium | no fresh resurfacing inferred (unlike b); cumulative ~8 Gyr impacts |
| `surface_ice_caps` | nightside CO₂ / H₂O frost in a narrow band ≳60° from substellar | medium | thin atmo can transport trace H₂O; nightside T < CO₂ frost point |
| `induction_heating_w_m2` | 0.05–0.5 | medium | Grayver 2022 — lower than b due to greater distance; not enough for active volcanism |
| `tidal_heating_w_m2` | 0.62 (+0.42/-0.53) (Dobos 2019) or 1.32 (+0.30/-0.47) (Barr 2018) | medium | Barr 2018 (1712.05641) and Dobos 2019 (1902.03867) — Maxwell viscoelastic models with Grimm 2018 + Agol 2021 masses. Io-class flux; T_eq mantle 1659–1666 K (above rock solidus → partial melt). |
| `core_mass_fraction` | 0.24 ± 0.08 | medium | Acuña 2021 (2101.08172) — Fe/Si stellar-constrained scenario |
| `iron_mass_fraction_pct` | ~50 | medium | Barr 2018 — highest density of 7 planets (7642 kg/m³ mean), iron-richest |
| `water_mass_fraction` | ≤4 × 10⁻⁶ | medium | Acuña 2021 — scenario 1 best estimate near zero |
| `tidal_k2_over_Q` | (0.4–2) × 10⁻⁴ | medium | Brasser 2019 (1905.00512) interior models; dynamical lower bound k₂/Q ≳ 1×10⁻³ |
| `moment_of_inertia_C` | 0.286 (range 0.235–0.4) | low | Brasser 2019 representative case |
| `magnetic_field_strength_microtesla_equator` | 3 | low | RM22 scaling; iron-richest planet but slow rotation (2.4 d) → multipolar regime, weak dipole |
| `magnetic_dipole_moment_normalized_earth` | 0.08 | low | RM22 (2203.01065) — TESS tidally-locked rocky planets cluster 0.01–0.1 M_Earth |
| `magnetic_dipole_tilt_deg` | 12 | low | Tie-break (interesting-first per the interesting-first rule) — offset polar cap; 5–15° aesthetic window |
| `magnetosphere_standoff_planet_radii` | 1.8 | medium | Garraffo 2017 (1706.04617) Fig. 4 — slightly larger than b due to distance |
| `radiation_belt_present` | false | medium | Field too weak (<0.1 Earth) to sustain stable trapped-particle population |
| `surface_radiation_dose_msv_yr` | 50000 | low | Atri 2019 (1910.09871) Table 6 scaling for c at 0.0158 AU + 100 g/cm² atm shielding; 1 bar O₂ + B-field reduces lethal-flare spikes |
| `atmospheric_shielding_g_cm2` | 100 | medium | Phase 3 cfg pressure 0.1 bar O₂ → ~100 g/cm² column |
| `aurora_present` | true | medium | Thin O₂ atm + weak B-field together produce visible auroral emission |
| `aurora_color_primary_hex` | `#4DFF4D` | medium | [OI] 557.7 nm green from O atomic recombination (Earth-aurora-analog in O-rich thin atm); tie-break: interesting-first chose green over UV-dominant alternative |
| `aurora_color_secondary_hex` | `#A050B0` | low | O₂⁺ Second Negative bands ~330–400 nm violet; tie-break: interesting-first picks visible-wavelength side of UV-blue continuum |
| `aurora_emission_species_primary` | `[OI] 557.7 nm + O₂⁺ Second Negative` | medium | Atm composition + standard aurora chemistry (O-rich thin atm) |
| `aurora_oval_magnetic_latitude_deg` | 35 | medium | Vidotto 2013 Eq. 7 with magnetopause ~2 R_p → α ≈ 45°; weak field expands oval toward equator |
| `aurora_intensity_kR_typical` | 100 | medium | Kislyakova 2018 stellar field 1100 nT at c (vs Earth's 5 nT) → 10–500× Earth auroral driver |
| `induction_heating_magma_ocean_fraction` | 0.68 | medium | Kislyakova 2018 (1710.08761) — c receives **highest induction heating** in system (68% of radiogenic); supports the Io-class tidal heating values already in cfg |
| `star_apparent_angular_diameter_deg` | 4.02 | high | derived: 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## Surface synthesis

The c eclipse + phase-curve data are consistent with either a bare,
dark, low-albedo surface or a thin O₂-dominated atmosphere with
minimal CO₂ (Zieba 2023, Lincowski 2023, Ducrot 2025). Unlike b — where
Ducrot 2024 found a model-consistency argument for fresh ultramafic
surfaces — c's eclipse data do not require an unweathered surface. The
inverse interpretation is also possible: c's surface may be
significantly older than b's because c has less tidal + induction
heating (Bolmont 2020 estimates tidal heating ~10× lower at c, and
Grayver 2022 induction heating ~10× lower for the same reason).

The latest tidal heating estimates (Barr 2018 / 1712.05641 and Dobos
2019 / 1902.03867) revise c's interior heat flux upward to **Io-class
values** of 0.6–1.3 W/m² — an order of magnitude higher than the
original "scaled from b" estimate. This implies c may host **active
or recent volcanism**, possibly with surface eruptions of silicate
magma. The cfg therefore widens its surface interpretation: weathered
basalt remains the most common surface (over ~8 Gyr of impact
accumulation), but **fresh basaltic resurfacing in localized "hot
spots"** is now equally plausible. Visual rendering should show a
mixed character — mature regolith dominant globally with brighter,
less-weathered patches near regions of recent volcanism.

Interior composition is distinctive among the seven planets. Acuña
2021 (2101.08172) finds c's water mass fraction is essentially zero
(≤4×10⁻⁶), with a core-mass fraction of 0.24 ± 0.08. Barr 2018 reports
c has the **highest mean density of any TRAPPIST-1 planet** (7642
kg/m³ — about 50% iron by mass). This iron-richness is independent
of any specific composition model: c sits cleanly outside the
water-rich range of the outer planets.

**Magnetic-induction heating reinforces the Io interpretation.** Kislyakova 2018 (1710.08761) computes induction heating from the stellar magnetic field for all 7 TRAPPIST-1 planets and finds c receives the **highest fraction** — 68% of radiogenic flux (vs. ~17% for b, ~56% for d, less for outer planets). Combined with Barr 2018's Io-class tidal flux (1.32 W/m²), this gives c a total interior heat budget well above the partial-melt threshold. A near-surface magma reservoir, possibly with active surface volcanism, becomes a strong default (rather than a marginal alternative) — consistent with the already-revised Surface tint accent toward fresh-basalt and active resurfacing.

The interior composition is consistent with — but does not require —
substantial water. Unterborn 2018 (1806.10084) finds c can be fit by
either a small-core (≤23 wt% Fe) rocky interior with no volatile
envelope, or a larger-core composition needing 8–34 wt% water; the
two-body degeneracy is not resolvable from mass+radius alone. Grimm
2018 (1802.01377) gives a slightly lower mass (1.156 +0.142/−0.131 M⊕)
than Agol 2021 (1.308 ± 0.056 M⊕), with a volatile probability ≥0.24
— i.e., c is consistent with no extended volatile envelope. The
adopted "weathered basalt" surface is the simplest interpretation
under these constraints.

**Color choice.** Weathered basalt under M8V illumination. The dark
basaltic primary `#2c2218` is slightly lighter than b's `#1a1612`
fresh-ultramafic to reflect the weathered-regolith maturity. The
iron-oxide accent `#604030` is more prominent than on b because:
(1) surface is older and has had more time to oxidize, and (2) the
thin O₂ atmosphere provides a continuous low-level oxidant supply.

**Morphology.** No active resurfacing implies preserved impact
record: well-defined craters at all size ranges, with a saturation
density approaching the lunar highlands. Magma ocean relict features
from the initial 100–500 Myr phase (Krissansen-Totton 2022, Magma
Ocean Evolution paper for TRAPPIST-1 system) should still be partially
visible as broad highland regions distinct from later impact basins.

## Atmosphere synthesis

Zieba 2023 (MIRI F1500W secondary eclipses, 4 visits) measured Fp/F★
= 421 ± 94 ppm at 15 μm. This corresponds to a dayside brightness
temperature of 380 ± 31 K, consistent with a bare rock at low albedo
or a thin, low-greenhouse atmosphere. The data exclude:

- 10 bar cloud-free atmospheres with ≥10 ppm CO₂
- 1 bar cloud-free atmospheres with significant CO₂
- 0.1 bar pure-CO₂ atmospheres
- Venus-analog atmospheres with sulfuric-acid clouds (2.6σ)

Lincowski 2023 expanded the model space to include broader atmosphere
types using a two-column climate-photochemistry coupled model. Within
2σ they find:

- **Thin O₂ atmospheres** with low CO₂ (≲100 ppm) at 0.1 bar are
  consistent with the data
- 1–10 bar O₂ + 100 ppm CO₂ at 2.0–2.2σ
- 1–10 bar O₂ + up to 0.5% CO₂ at 2.9σ
- Thin O₂ with up to 10% H₂O vapor (within 1σ)

Ducrot 2025 phase-curve closes the case further: c's dayside is
369 ± 23 K, nightside undetected (≲ 110 ppm at 15 μm), no significant
phase offset. Either bare-rock or thin O₂ remains consistent.

For NearStars we adopt **0.1 bar O₂-dominated thin atmosphere**:

- **Pressure** at 0.1 bar (10 kPa). Within Lincowski 2023's 1σ
  consistency envelope for O₂-dominated compositions with low CO₂.
- **Composition** dominated by O₂ (~98%) with trace H₂O vapor
  (~1%) and trace O₃ from photolysis (~100 ppm). CO₂ kept very low
  (~100 ppm) to honor the Zieba 2023 / Lincowski 2023 constraints.
  The O₂ origin is hydrodynamic-escape fossil: Luger & Barnes 2015
  show that an initial H₂O steam atmosphere on the early TRAPPIST-1
  worlds would lose H to space and leave behind ~10 bar of O₂; later
  photolysis + surface oxidation reduces this to the observed
  thin-O₂ remnant.
- **No clouds** in the canonical state. The thin O₂ atmosphere has
  insufficient water for cloud formation in steady state, and CO₂
  is too low for CO₂-ice clouds.

**Population-statistics support.** Gialluca 2024 (2405.02401) ran
MCMC simulations of the post-runaway escape epoch for the inner
TRAPPIST-1 planets under the joint constraint "b airless + c thin O₂".
Their result: with initial water ≥1 TO, **>98% of c simulations
retain an O₂-dominated atmosphere**; b/c-joint inversion gives
initial water 8.2 +1.5/-1.0 Earth oceans. The 0.1 bar O₂ choice is
therefore not only observation-consistent but is the dominant
outcome of the post-runaway-greenhouse evolution.

**Auroral signature.** In a thin O₂-dominated atmosphere, the dominant precipitation-driven emission is [OI] 557.7 nm green (the same line that gives Earth its classic green aurora). Stellar wind compression brings the magnetopause to ~2 R_p (Garraffo 2017), which means the auroral oval — normally a high-latitude band on Earth — expands toward magnetic latitude ~35°. The result is a wide aurora band visible from substantial fractions of c's nightside, not just the polar regions. Intensity reaches ~100 kR (≈10× Earth's typical 10 kR) due to the constantly elevated stellar wind. Secondary O₂⁺ Second Negative emission near 330–400 nm contributes a violet edge; for cfg rendering, primary `#4DFF4D` green with `#A050B0` violet accent. The interesting-first tie-break favors this visible-wavelength rendering over the alternative UV-dominant emission palette, which would be invisible to the player.

**Sky appearance.** The 0.1 bar O₂ atmosphere has weak Rayleigh
scattering (about 5% at 0.5 μm vs. Earth's 1 bar of N₂+O₂). The sky
near the substellar point is faintly dark-violet at the zenith,
transitioning to a pale gray-orange near the limb where the stellar
disk is bright. Toward the nightside, the sky is essentially black.
O₃ Chappuis absorption (peaking near 0.6 μm) adds a subtle gray
overtone in the day-side scattered light. The host star dominates
the daytime sky at angular size 4.02° (about 8× the Sun's angular
size from Earth).

## Rotation & spin synthesis

Tidal damping for c at 2.42-day period over 7.6 Gyr establishes the
synchronous (1:1) configuration unambiguously. Obliquity damped to
zero. Eccentricity is 0.00654 (Agol 2021) — too low to support a 3:2
resonance (Vinson 2017 finds 3:2 stable only for e ≳ 0.01).

**Possible magma ocean signature.** Bolmont 2020 (2002.02015) shows
that TRAPPIST-1 b/c TTVs could hint at a high planetary Love number
(k₂ ≳ 1.5), which would dynamically signal a liquid magma layer.
Combined with the Io-class tidal flux (Barr 2018), this raises the
prior on c hosting partial melt. The current TTV fits are
noise-floor-limited, so the inference is tentative.

**Magnetic dynamo expectation.** c's iron-rich interior (Barr 2018: 50% Fe by mass, highest density in the system) is the strongest pro-dynamo case among the inner planets, but the 2.4-day tidally-locked rotation severely limits dipolar field strength via the Rossby-number regime transition (Reiners & Christensen 2010). RM22 (2203.01065) scaling predicts a multipolar/weak field at ~0.08 × Earth dipole moment, giving ~3 μT surface field at the equator. This is enough to deflect part of the stellar wind plasma and channel it into the auroral oval, but not enough to sustain Van-Allen-like radiation belts.

**KSP implementation note.** Rotation period = orbital period =
2.4219 days (209 254 s). Kopernicus `rotationPeriod` should match the
orbital `period` in seconds.

**No seasons.** Obliquity = 0; libration-induced insolation variation
< 0.5%. The substellar point is fixed in the surface frame on
geological timescales (modulo the slow precession noted for b).

**Eccentricity-driven tidal flexure.** With e = 0.00654 and an
ultra-cool dwarf host, the tidal heating rate from forced libration
is modest. Brasser 2019 (1905.00512) gives k₂/Q in the range (0.4–2)
× 10⁻⁴ from interior models, with a dynamical lower bound k₂/Q ≳
1×10⁻³; representative moment-of-inertia C ≈ 0.286 (range 0.235–0.4).
The implied surface tidal flux is ~10× lower than b's (consistent
with c's larger orbital semi-major axis), keeping c in the
"insufficient to drive active volcanism" regime — consistent with
the "weathered surface" inference.

## Visual styling

Combining surface and atmosphere decisions:

- **Global color palette.** Dark weathered basalt body (`#2c2218`
  primary, `#604030` accent) under intense red-orange stellar light
  appears as a deep brown-charcoal world with subtle iron-oxide
  banding biased toward the substellar hemisphere. The thin O₂
  atmosphere is essentially invisible from orbit except as a faint
  limb haze.
- **Dayside.** Substellar region (~430 K subsolar peak, ~370 K
  general dayside) with iron-oxide patches strongest within 30° of
  substellar point. Subdued topographic relief — mature impact
  cratering, no active volcanism. Heat redistribution to nightside
  is weak but nonzero (~140 K nightside floor) due to the thin O₂
  atmosphere.
- **Terminator band.** Moderate topographic shadow contrast under
  grazing 2566 K light. Possible high-altitude pale-gray
  Rayleigh-scattered haze visible as a thin limb glow at low solar
  zenith angles.
- **Nightside.** Cold (~140 K) and dark. Possible CO₂/H₂O frost in
  a narrow band ≳60° from substellar; appears as faint lighter
  patches under reflected light from sister planets. Thermal IR
  emission only in visible bands. KSP nightside ambient ≈ 5–10% of
  dayside.
- **Atmosphere haze.** Thin pale gray-violet limb haze (`#3a3a40`),
  3–8 km thick, visible against space at the planet's limb only.
- **Star in sky.** TRAPPIST-1 subtends 4.02° in c's sky (8× the Sun
  from Earth). Color `#ff7a1a` (2566 K). Surface brightness ~2.27 S⊕
  (similar to Venus's insolation at Earth's orbit). Flare activity
  identical to b — occasional prominent IR flares.
- **Sister planets in sky.** b (next inward) appears at ~0.6° at
  inferior conjunction; d (next outward) at ~0.5° during conjunctions
  every 4–6 days. Near-coplanar geometry from Agol 2021.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2306.10150** Zieba 2023 — JWST/MIRI F1500W secondary eclipse of
  c. Fp/F★ = 421 ± 94 ppm, dayside T ≈ 380 K. Excludes Venus-analog
  and most CO₂-rich atmospheres. The discovery paper for c's
  atmospheric upper limit.
- **2308.05899** Lincowski 2023 — Broader atmosphere exploration for
  c using two-column climate+photochemistry. Finds thin O₂ low-CO₂
  atmospheres consistent within 1σ. Drives the adopted O₂-dominated
  scenario.
- **2509.02128** Ducrot 2025 — MIRI 15 μm phase curve of b and c.
  c dayside 369 ± 23 K, no nightside detection. Closes the
  atmospheric scenario space toward bare-rock / thin-O₂.
- **2305.01250** Acuña 2023 — Interior-atmosphere modeling. Finds c
  most likely has a bare surface but cannot rule out a thin
  atmosphere. Supports the surface-vs-atmosphere degeneracy
  resolved by Lincowski 2023.
- **2412.11987** Nicholls 2024 — Convective shutdown in lava-world
  atmospheres. Uses c as a case study; explores when magma oceans
  can persist under non-convective atmospheres. Informs the
  "weathered surface" vs. "fresh ultramafic" choice (c lands on
  weathered side).
- **1712.05641** Barr 2018 — Interior structures and tidal heating
  in TRAPPIST-1 planets. Drives the upward revision of c's tidal
  heat flux to Io-class (1.32 W/m²). Identifies c as the iron-richest
  planet (highest density, ~50% Fe).
- **1902.03867** Dobos 2019 — Tidal heating and habitability of
  TRAPPIST-1 exoplanets. Refined Maxwell viscoelastic model with
  Grimm 2018 masses. F_int(c) = 0.62 W/m². Confirms partial-melt
  interior.
- **2101.08172** Acuña 2021 — Hydrosphere characterization. c WMF
  ≤ 4×10⁻⁶, CMF 0.24 ± 0.08. Drives the "dry rocky" interior
  choice.
- **2405.02401** Gialluca 2024 — MCMC escape simulation. >98% of
  c outcomes retain O₂ atmosphere. Strongly supports the 0.1 bar
  O₂ scenario.
- **2002.02015** Bolmont 2020 — TTV Love-number constraint hinting
  at possible magma layer.
- **1706.04617** Garraffo 2017 — Threatening Magnetic and Plasma
  Environment of TRAPPIST-1. MHD simulations placing the magnetopause
  at 1.5–2 R_p for inner planets.
- **2203.01065** RM22 — Internal Structures and Magnetic Moments.
  Tidally-locked rocky planet dynamo scaling.
- **1910.09871** Atri 2019 — Stellar Proton Event surface-dose
  tables; the radiation cfg reference.

### Read (context / methodology, not decision-driving)

- **2412.16541** Stellar contamination correction using back-to-back
  b/c transits. Methodology relevant to all TRAPPIST-1 transmission;
  not directly visual-informative.
- **2412.11627** Ducrot 2024 — b's combined 12.8+15 μm eclipse
  analysis. Mentioned here because the bare-rock vs. CO₂-haze
  interpretation parallels c's options.
- **2507.02052** Uniform reanalysis of JWST MIRI 15 μm eclipses
  (frame-normalized PCA). Cross-check; consistent results.
- **2505.03672** Statistical geochemical constraints on water
  outgassing as secondary-atmosphere source for TRAPPIST-1 planets.
  Background context for the "fossil O₂" inference.
- **1802.01377** Grimm 2018 — TTV-derived masses and Bayesian
  interior fit. c's volatile probability ≥0.24 (no extended water
  envelope required). Mass slightly lower than Agol 2021 but within
  uncertainty.
- **1806.10084** Unterborn 2018 — Updated compositional models;
  c's interior is degenerate between small-core rocky (no water)
  and larger-core wet (8–34 wt% water). Both options consistent
  with current cfg.
- **1905.00512** Brasser, Barr & Dobos 2019 — Tidal parameters for
  b and c. Drives the new `tidal_k2_over_Q` and `moment_of_inertia_C`
  entries in the decisions table. Note: the synthesis previously
  cited this paper as "Bolmont 2020" by mistake; corrected.

### Read (instrument-only, not visual-informative)

- **2409.19333** Stellar contamination correction methodology paper.
  Cited for completeness; no direct visual content for c.

### Not read — no arXiv preprint or low-priority (~20 papers)

The c bibliography is smaller than b's (32 vs 66). Most non-arXiv
papers are conference summaries or sister-planet biosignature studies.
Notable items skipped:

- **2026NatAs.tmp...65G** "No thick atmosphere around TRAPPIST-1 b
  and c from JWST thermal phase curves" — likely the Nature Astronomy
  publication of Ducrot 2025 (covered via arXiv 2509.02128). Skip.
- **2025arXiv...** various retraction / re-fit conference summaries.
  Skip unless any updates the c eclipse depth.

---

## Open items for follow-up

- Validate the 0.1 bar O₂ atmosphere choice against any future c
  emission spectroscopy in shorter-wavelength MIRI filters (e.g.,
  F1280W on c) — the airless alternative is statistically as
  consistent and might be preferred if a future renderer needs the
  "bare rock siblings" b+c pairing.
- Cross-check the iron-oxide accent prominence against the c-specific
  predictions in Way 2024 / Cohen 2024 (TRAPPIST-1 surface oxidation
  modeling) if those become available.
- Cfg variant for the "airless bare-rock" interpretation, paired with
  b's airless cfg as a coordinated palette.
- Refine the `density_g_cc` entry: the derived value (6.36) is
  slightly higher than Agol 2021's reported 5.7, reflecting different
  uncertainty propagation. Phase 2 should reconcile.
- Magnetic field strength is low-confidence scaling-based. Direct
  radio-emission upper limits (e.g., Vedantham 2020) could tighten the
  dipole moment range.
- Interesting-first tie-break: aurora color was set to visible-green
  /violet rather than UV-dominant; cfg variant could render the
  UV-dominant emission as a faint glow if a wider rendering palette
  is supported.

## Related

- [trappist-1-b](trappist-1-b.md) — inner sibling, both candidates for the "no significant atmosphere" JWST cohort
- [trappist-1-d](trappist-1-d.md) — adjacent outer sibling; thin-atmosphere scenario shares the cosmic-shoreline reasoning
- [trappist-1-e](trappist-1-e.md) — full habitable-zone reference for the system
- [methodology](../reference/methodology.md) — schema for Decisions table conventions and confidence labels
- [mod-reference](../reference/mod-reference.md) — downstream KSP mods
- [rex-data-comparison](../reference/rex-data-comparison.md) — §10 covers TRAPPIST-1 mass/radius re-fits relative to REX
