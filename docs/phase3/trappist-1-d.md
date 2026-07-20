# TRAPPIST-1 d — Phase 3 Synthesis

Pilot Phase 3 document for the NearStars KSP mod (drafted 2026-05-21).

TRAPPIST-1 d is a 0.79 R⊕ rocky planet on a 4.05-day orbit around an
M8V ultra-cool dwarf, at the inner edge of the classical habitable
zone. Recent JWST/NIRSpec observations (Piaulet-Ghorayeb et al. 2025)
place strict limits on its atmosphere: most Solar System analog
compositions are excluded at >95% confidence. The remaining
observation-consistent scenarios are (A) airless bare rock, or (B) an
extremely thin atmosphere with potential high-altitude water aerosols
at the terminator.

**Scenario choice for NearStars: thin atmosphere with terminator
water-ice clouds**, leaning close to (A) on pressure (~0.01 bar, the
JWST 3σ ceiling) but keeping the terminator cloud feature predicted by
Turbet 2023 GCM. This balances JWST fidelity with sufficient visual
distinction from a Mercury-clone bare rock.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high = directly
measured or tightly constrained, medium = theoretical with strong
support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 4.05 d orbit, tidal damping; Agol 2021 |
| `obliquity_deg` | 0 | high | tidal damping; Agol 2021 |
| `eccentricity` | 0.00638 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 234 | medium | Agol 2021 (low ecc → weak constraint) |
| `sidereal_period_days` | 4.0508 | high | Agol 2021 |
| `semi_major_axis_au` | 0.02227 | high | Agol 2021 |
| `mass_mearth` | 0.388 | high | Agol 2021 TTV; Piaulet 2025 reconfirms |
| `radius_rearth` | 0.788 | high | Agol 2021; Piaulet 2025 transit fit |
| `surface_gravity_g_earth` | 0.624 | high | derived = 0.388 / 0.788² |
| `density_g_cc` | 4.35 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.3) | 262 | high | Piaulet 2025 |
| `equilibrium_temp_k` (A=0)   | 287 | high | derived from a/R★, T★ = 2566 K |
| `bond_albedo` | 0.10 | medium | bare-rock analog from T-1 b/c JWST emission; uncertainty 0.05–0.20 |
| `atmosphere_present` | true (very thin) | low | adopted scenario (B); (A) airless also defensible |
| `atmosphere_surface_pressure_pa` | 1 000 | medium | upper limit ~0.01 bar at 3σ for H₂-rich; consistent with thin CO₂ at <2σ; Piaulet 2025 §7.1–7.2 |
| `atmosphere_composition` | trace CO₂ + H₂O vapor on N₂ | low | CH₄, NH₃, H₂-rich excluded; CO₂ marginal at 2σ; H₂O survives via terminator cloud GCM |
| `atmosphere_scale_height_km` | 12 | medium | derived: kT/μg with T≈280 K, μ≈30 g/mol (CO₂/N₂ mix), g=6.1 m/s² |
| `atmosphere_tint_rgb_hex` | `#a8b0c0` (pale silver-blue, weak) | low | terminator H₂O ice + Rayleigh remnant under 2566 K red illumination |
| `dayside_surface_temp_k` | 390 | medium | bare-rock subsolar with A=0.1; cf. Way 2025 Arid-Venus 1-bar Sim 01 dayside max 364 K (their case has more redistribution) |
| `nightside_surface_temp_k` | 150 | low | weak redistribution in thin-atmo regime; analog T-1 b/c |
| `terminator_water_ice_clouds` | scattered, high-altitude (~mbar level) | low | Turbet 2023 GCM, Piaulet 2025 §7.3 — water-rich tail forms mbar stratospheric clouds at terminator |
| `ocean_present` | false | high | interior to water condensation limit (0.772 S⊕ for T-1 star; Turbet 2023); any H₂O resides in atmosphere |
| `surface_ice_caps` | none on dayside; possible nightside cold-trap frost | low | extreme day/night contrast; minimal volatile budget |
| `surface_tint_rgb_hex_primary` | `#2a2018` (dark gray-brown basalt) | low | bare-rock low albedo + M-dwarf red illumination shifts perceived hue; Mercury/Moon analog |
| `surface_tint_rgb_hex_accent` | `#5a3220` (iron oxide patches) | low | photolytic oxide formation on long-tidally-locked dayside (Turbet 2018 mechanism) |
| `surface_morphology` | cratered basaltic plains; relict magma-flow features near dayside-terminator | low | bare-rock interpretation; magma ocean retained ≲500 Myr (Piaulet 2025 §8); subsequent impacts |
| `magnetic_field_strength_microtesla_equator` | 1 | low | Sub-Earth mass (0.39 M⊕) shrinks core; RM22 scaling + tidal-locking penalty |
| `magnetic_dipole_moment_normalized_earth` | 0.02 | low | RM22 ([2203.01065](https://arxiv.org/abs/2203.01065)) for sub-Earth-mass tidally-locked; Driscoll & Olson dynamo shutoff favored |
| `magnetic_dipole_tilt_deg` | 10 | low | Tie-break: 10° gives offset auroral cap; aesthetic window 5–15° |
| `magnetosphere_standoff_planet_radii` | 1.5 | medium | Weaker dipole → smaller magnetopause; Garraffo 2017 interpolated |
| `radiation_belt_present` | false | medium | Field <0.1 Earth, no trapped-particle regime |
| `surface_radiation_dose_msv_yr` | 25000 | low | Atri 2019 ([1910.09871](https://arxiv.org/abs/1910.09871)) interpolated for d at 0.022 AU + thin atm (~10 g/cm²) |
| `atmospheric_shielding_g_cm2` | 10 | medium | Phase 3 cfg pressure 0.01 bar → ~10 g/cm² column |
| `aurora_present` | true | low | Thin atm + weak B-field → visible auroral activity, novel chemistry from H₂O-rich tail |
| `aurora_color_primary_hex` | `#B0E0E6` | low | Tie-break (interesting-first): pale cyan-white from H₂O cloud aerosol excitation + OH band emission boosted to visible by Mie scattering |
| `aurora_color_secondary_hex` | `#4DFF4D` | low | Trace [OI] green if oxygen present; tie-break: interesting-first picks visible secondary over UV-only |
| `aurora_emission_species_primary` | `OH(A-X) 308 nm + H Lyman-α + scattering on terminator H₂O ice` | low | Derived from atm composition (water-rich tail per Turbet 2023 → unique cloud-resonant emission) |
| `aurora_oval_magnetic_latitude_deg` | 30 | medium | Weaker B-field → larger oval aperture (Vidotto 2013) |
| `aurora_intensity_kR_typical` | 200 | low | Thin atm means deeper precipitation, brighter per particle; flare-driven |
| `induction_heating_magma_ocean_fraction` | 0.56 | medium | Kislyakova 2018 ([1710.08761](https://arxiv.org/abs/1710.08761)) — 56% of radiogenic; magma-ocean plausibility supports d's existing magma-relict morphology notes |
| `star_apparent_angular_diameter_deg` | 2.85 | high | derived: 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## Surface synthesis

The two innermost TRAPPIST-1 planets, b and c, have JWST emission and
transmission data consistent with bare, dark, low-albedo rocky surfaces
(Greene 2023, Zieba 2023, referenced extensively in Piaulet 2025). For d,
direct emission constraints are not yet published, but the JWST
transmission analysis treats a bare-rock scenario as fully consistent
with the flat spectrum after stellar contamination is removed (Piaulet
2025 §8). We therefore extend the bare-rock interpretation to d, with
the caveat that d sits at a cooler equilibrium temperature than b or c
and could plausibly host condensed surface volatiles on its nightside.

**Color choice.** The host star is a 2566 K M8V dwarf — its SED peaks
near 1.1 μm with a steep red continuum. Surface reflectance perceived
by a human observer is shifted toward red-brown regardless of intrinsic
mineral color (Domagal-Goldman 2010 for general M-dwarf surface
illumination; not specifically d). For a fresh basaltic surface, the
Mercury / Moon mare analog (broadband visible albedo ≈ 0.05–0.12,
Hapke-corrected) is the closest Solar System reference. We pick
`#2a2018` (dark gray-brown) with `#5a3220` iron-oxide patch tint.

**Tidal heating refinement.** Dobos 2019 ([1902.03867](https://arxiv.org/abs/1902.03867)) gives F_int(d) = 0.26 +0.14/-0.21 W/m² with mantle T_eq ≈ 1645 K (above rock solidus, supporting up to 35% melt by volume). The newer re-derivation of Bolmont et al. 2026 (`2601.03408`, Table 3 — k₂ + internal-structure + Agol 2021 eccentricities) raises this to 0.39–2.60 W/m² (core-size dependent) and finds d tidal-DOMINATED, consistent with d's magma-relict morphology. The flux is just below the runaway-greenhouse critical value (273 W/m², per the same paper); with Bond albedo ≥ 0.3, d sits in the safe (non-runaway) regime. The cfg's current A_B = 0.10 would technically put d into runaway if a substantial volatile reservoir existed — but the JWST-constrained near-airless interpretation (Piaulet 2025) resolves this tension by leaving essentially no water to run away.

**Iron oxide patches.** Photochemistry on long-tidally-locked terrestrial
worlds tends to produce surface oxidation in regions accessible to
stellar UV, even with extremely thin atmospheres (Turbet 2018 photolysis
discussion in the context of dayside surface chemistry). We expect a
patchy iron-oxide overlay biased toward the substellar quadrant. This
is a low-confidence aesthetic call — no direct reflectance measurement
exists.

**Morphology.** Three contributing processes inform the surface
texture: (1) the ≲500 Myr magma ocean phase (Piaulet 2025 §8) leaves
relict flow / fracture structures, (2) ~8 Gyr of impact accumulation
on a tidally-locked surface (cratering biased toward leading hemisphere
in the locked frame), and (3) potential induction heating from
star-planet magnetic coupling (Grayver 2022, cited in Way 2025) could
sustain limited volcanism — but no direct evidence forces this for
d specifically. We default to lunar-highlands-density cratering with
visible magma-ocean relict features near the dayside terminator (where
freeze-front textures might be expected as the magma cooled
non-uniformly under tidally-locked irradiation).

## Atmosphere synthesis

JWST NIRSpec/PRISM transmission spectroscopy over two transits
(Piaulet-Ghorayeb 2025) yields a flat spectrum within ±100–150 ppm
after stellar contamination correction. This excludes:

- H₂-rich atmospheres thicker than ~0.01 bar at >3σ (any metallicity
  ≲100× solar)
- Cloud-free Titan-like (1.6% CH₄ in N₂), >3σ
- Archean Earth analogs at 1 bar, >3σ (CH₄ partial pressure)
- Cloud-free Venus (~92 bar CO₂), >95%
- Early Mars (1 bar CO₂), >95%
- Cloud-free modern Earth, >95%

The remaining marginally-consistent scenarios (within 2σ):

- Extremely thin (<0.01 bar) Mars-like CO₂
- Venus-like with high-altitude sulfuric acid clouds
- Modern Earth-like with water clouds masking CO₂
- Water-rich atmosphere where mbar-level stratospheric H₂O ice clouds
  form at the terminator (Turbet 2023 GCM predicts this for d
  specifically due to its position interior to the water condensation
  limit at 0.772 S⊕ — Piaulet 2025 §7.3)
- Fully airless bare rock

For NearStars we adopt a synthesis of the "very thin atmosphere +
terminator water-ice clouds" scenario:

- **Pressure** at the 3σ JWST ceiling (~1000 Pa = 0.01 bar) rather than
  the airless extreme. This is the highest atmosphere mass still
  consistent with JWST data.
- **Composition** dominated by N₂ with trace CO₂ and H₂O. CH₄ and NH₃
  are excluded by photodissociation (Turbet 2018). H₂ is excluded by
  formation + escape arguments (Hori & Ogihara 2020 cited in Piaulet
  2025 §7.1). CO₂ at trace levels is marginally allowed and supported
  by outgassing models (Liggins 2021, Salman 2024). H₂O is required
  for the terminator cloud feature.
- **Terminator clouds** as discrete high-altitude water-ice patches,
  not a full overcast. This matches the GCM prediction (Turbet 2023,
  Piaulet 2025 §7.3) and provides visual interest distinct from a fully
  bare planet.

**Interior-atmosphere coupling.** Acuña 2021 ([2101.08172](https://arxiv.org/abs/2101.08172)) characterizes d's hydrosphere as not in global radiative balance (absorbed flux ≈ 33 W/m² below OLR), implying d is gradually cooling. With WMF in the 0.036–0.084 range and Earth-analog radiogenic flux, d's volatile inventory could plausibly exist in condensed phases (liquid water or ice Ih) at the surface or in a subsurface layer. This is an alternative scenario to the chosen "thin atmosphere + terminator water-ice clouds" cfg — for the canonical NearStars output, we keep the JWST-constrained interpretation, but the cooling-and-condensing scenario is preserved as a cfg variant.

**Cloud-resonant aurora.** d's adopted scenario — terminator H₂O ice clouds at mbar altitudes (Turbet 2023) — gives a unique auroral signature. Stellar-wind precipitation into the thin water-rich atmosphere dissociates H₂O into H and OH radicals, producing OH(A-X) UV emission at 308 nm. Crucially, the high-altitude ice clouds scatter this UV light back to visible wavelengths through Mie scattering, producing a pale cyan-white auroral glow concentrated at the terminator — distinct from Earth's polar-cap aurora geometry. The intensity reaches ~200 kR (20× Earth), driven by the M-dwarf's high stellar wind flux. For cfg rendering: primary `#B0E0E6` (pale cyan-white) along the terminator, secondary `#4DFF4D` (green) if local [OI] enhancement; interesting-first tie-break preferred the cloud-resonant visible rendering over the pure-UV alternative, which would be invisible.

**Sky appearance.** With 0.01 bar surface pressure, Rayleigh scattering
is essentially absent on the dayside — the sky is near-black at the
zenith even at midday, with the M8 star providing intense localized
red-orange illumination (~2566 K color temperature). Toward the
terminator, the high-altitude water-ice clouds catch oblique stellar
light and appear as faint cyan-white streaks against the red-tinted
horizon. The nightside sky is uncontaminated and shows the rest of the
TRAPPIST-1 planet chain in conjunction (the seven planets are
near-coplanar; Agol 2021).

## Rotation & spin synthesis

The TRAPPIST-1 d system parameters force a strongly synchronous
configuration. The orbital eccentricity is small (0.00638; Agol 2021),
the obliquity is damped to zero by tidal forces over the system's
≳7 Gyr age (Agol 2021 §6.2), and the spin-orbit resonance is most
plausibly 1:1 — though Way 2025 notes that 3:2 spin-orbit states are
not formally excluded (Correia 2014, Makarov 2018, Revol 2024) and
runs two of his GCM simulations under that assumption. For NearStars
we adopt the 1:1 case as the default; the 3:2 alternative would be
a follow-up cfg variant.

**KSP implementation note.** True 1:1 tidal lock means rotation period
= orbital period = 4.0508 days. In Kopernicus the body's `rotationPeriod`
should equal the orbital `period` in seconds (349 989 s).

**No seasons.** With obliquity = 0 and effectively no
eccentricity-driven libration (insolation variation < 0.4% over an
orbit), the substellar point is fixed in the surface frame. Visual
ramifications: no day-night cycle for any surface location, no
seasonal cap migration, no terminator drift.

**Magnetic dynamo expectation.** d's small mass (0.39 M⊕) and slow tidally-locked rotation (4.05 d) make a strong dynamo difficult. RM22 ([2203.01065](https://arxiv.org/abs/2203.01065)) places sub-Earth-mass tidally-locked planets at ~0.02 × Earth dipole moment, giving ~1 μT surface field at the equator. The 56% induction-heating fraction (Kislyakova 2018) suggests an active liquid layer in d's interior, so a weak residual dynamo is plausible. The cfg adopts a low-but-nonzero field — enough to support a faint cloud-resonant aurora at the terminator but not to deflect stellar wind from the bulk of the dayside.

## Visual styling

Combining the surface and atmosphere decisions:

- **Global color palette.** Dark basalt body (`#2a2018` primary,
  `#5a3220` accent) seen under intense red-orange stellar light
  appears as a deep ochre-charcoal world with no green or blue
  channel. Highest visual contrast is at the terminator where the
  near-grazing light reveals topographic relief.
- **Dayside.** Bright substellar region (~390 K, ~118 °C) with subdued
  features due to high near-zenith illumination flattening shadows.
  Iron-oxide patches strongest within ~30° of substellar point.
- **Terminator band.** The most photogenic zone. High-altitude water
  ice clouds catch stellar light and appear as faint cyan-white wisps
  against the red surface. Substantial topographic shadow contrast.
- **Nightside.** Cold (~150 K) and dark; only thermal IR emission, no
  visible-band features. KSP nightside lighting should be very low
  ambient — the only light source is starlight reflected from
  TRAPPIST-1 b, c (rare close conjunctions) or the outer planets.
- **Atmosphere haze.** The 0.01 bar atmosphere is barely visible. Add
  a thin pale silver-blue limb haze (`#a8b0c0`) maybe 3–5 km thick,
  only visible against the dark space background at the planet's limb.
- **Star in sky.** TRAPPIST-1 subtends ~2.85° in d's sky (about 5.7×
  the Sun's angular size from Earth). Its color is deeply red-orange
  (≈2566 K blackbody → CIE chromaticity near `#ff7a1a`), and the
  surface brightness is comparable to Mars-from-Mars solar brightness
  (~1.12 S⊕). At wavelengths beyond 1 μm the star is bright enough to
  show prominent solar flares (Howard 2023, cited in Piaulet 2025 §1)
  — for KSP, occasional flare lighting flickers would be a faithful
  but optional touch.
- **Sister planets in sky.** When in inferior conjunction, TRAPPIST-1
  c appears at angular size ~0.5° (similar to Earth's Moon from
  Earth's surface), TRAPPIST-1 e at ~0.3°. The near-coplanar
  geometry means these conjunctions are frequent (every few days).

## Bibliography

### Read (visual-informative, drove decisions above)

- **[2502.00132](https://arxiv.org/abs/2502.00132)** Way 2025 — "TRAPPIST-1 d: Exo-Venus, Exo-Earth or
  Exo-Dead?" ROCKE-3D 3D GCM suite under 17 boundary-condition
  variants. Provides the climate-scenario envelope (Arid-Venus through
  Aquaplanet), surface temperature ranges, and an explicit comparison
  to Wolf 2017 / Turbet 2018 / Rushby 2020.
- **[2508.08416](https://arxiv.org/abs/2508.08416)** Piaulet-Ghorayeb 2025 — JWST NIRSpec/PRISM transmission
  spectrum. Definitive observational constraint. Drives the atmosphere
  scenario choice and the bare-rock surface interpretation.
- **[2511.10801](https://arxiv.org/abs/2511.10801)** Salman 2024 — Atmosphere-interior model with carbon
  cycle. Constrains outgassing composition as a function of mantle
  oxygen fugacity and initial water mass fraction. Supports trace-CO₂
  + H₂O composition over H₂-rich.
- **[1902.03867](https://arxiv.org/abs/1902.03867)** Dobos 2019 — Maxwell viscoelastic tidal heating model.
  F_int(d) = 0.26 W/m², mantle T 1645 K (up to 35% melt by volume).
  Identifies the runaway-greenhouse threshold for d's albedo (A_B ≥ 0.3
  needed if volatile reservoir present).
- **[2101.08172](https://arxiv.org/abs/2101.08172)** Acuña 2021 — Hydrosphere characterization for the 7
  planets. d's WMF 3.6–8.4%, atmosphere not in radiative balance
  (cooling phase). Supports an alternative condensed-volatile scenario.
- **[1706.04617](https://arxiv.org/abs/1706.04617)** Garraffo 2017 — Threatening Magnetic and Plasma
  Environment of TRAPPIST-1. MHD simulations placing the inner-planet
  magnetopauses near surface.
- **[2203.01065](https://arxiv.org/abs/2203.01065)** RM22 — Magnetic moments of rocky planets. Sub-Earth-mass
  tidally-locked dynamo scaling.
- **[1910.09871](https://arxiv.org/abs/1910.09871)** Atri 2019 — Surface-dose tables for stellar proton
  events.
- **[1710.08761](https://arxiv.org/abs/1710.08761)** Kislyakova 2018 — Induction heating: d receives 56% of
  radiogenic flux from stellar-wind electromagnetic coupling; supports
  magma-ocean alternative scenario in d's interior.

### Read (context / methodology, not decision-driving)

- **[1802.02250](https://arxiv.org/abs/1802.02250)** de Wit 2018 — HST WFC3 atmospheric reconnaissance.
  Initial constraint on H₂-rich atmospheres (8σ for d). Superseded by
  Piaulet 2025 but historically the first non-detection.
- **[1810.05210](https://arxiv.org/abs/1810.05210)** Moran 2018 — HST haze/cloud limits with updated
  masses. Showed metallicity > 60× solar with tropospheric clouds
  consistent with HST. Superseded by JWST.
- **[2103.08600](https://arxiv.org/abs/2103.08600)** Welbanks 2021 — Aurora retrieval framework. Predicted
  10-transit JWST NIRSpec detection feasibility for CO₂-rich or N₂-rich
  d atmospheres. The Piaulet 2025 observation is the experimental
  realization of this prediction (with 2 transits, achieving the
  predicted sensitivity).
- **[2206.00028](https://arxiv.org/abs/2206.00028)** Meadows 2022 — Atmospheric exchange biosignature
  false-positive (O₂ from d transported to e). Constrains plausible
  volatile transport mechanisms but not directly visual.
- **[2210.02484](https://arxiv.org/abs/2210.02484)** Hill 2022 — Habitable-zone exoplanet catalog. Lists
  d as one of three transiting ≤2 R⊕ HZ planets favorable for follow-up
  alongside LHS 1140 b and K2-3 d. Context only.
- **[2304.12490](https://arxiv.org/abs/2304.12490)** Hardegree-Ullman 2023 — ELT O₂ detectability survey.
  Estimates 16–55 years of integration to detect Earth-like O₂ on
  d–g with future ground-based ELTs. Not visual-informative but
  contextualizes the long-timescale observational future.

### Read (instrument-only, not visual-informative)

- **[2203.04173](https://arxiv.org/abs/2203.04173)** Rustamkulov 2022 — JWST NIRSpec lab time-series
  characterization. Methodology reference for the Piaulet 2025
  observation. Used `inject-recovery` simulations on TRAPPIST-1 d
  spectra but the planet appears only as a test case.

### Not read — no arXiv preprint available (22 papers)

These were surfaced by the ADS query but lack arXiv preprints; would
require institutional library access or PDF paste. For Phase 3 d, the
key papers in this set are:

- **2025epsc.conf..178P** Piaulet-Ghorayeb 2025 EPSC abstract — likely
  a conference summary of the JWST paper already read ([2508.08416](https://arxiv.org/abs/2508.08416)).
  Skip.
- **2024absc.conf00561M / 2024ESS.....550004M / 2023PSJ.....4..192M**
  Mullens et al. 2023–2024 — "Feasibility of Detecting Biosignatures
  in the TRAPPIST-1 System." Three appearances of the same study at
  different venues. Likely not visual-informative (biosignature focus).
  Skip unless atmosphere decision needs review.
- **Confirmation of a Dynamical Model for the TRAPPIST-1 Exoplanetary
  System** (no arXiv) — *potentially important for orbital parameters*.
  If this updates Agol 2021's dynamics, the orbital decisions above
  may need revision. **Flagged for user paste if accessible.**
- **ExoCAM: A Community Climate Modeling Tool** (no arXiv) — tool paper,
  not science. Skip.
- **NIRISS Exploration of the Atmospheric diversity of Transiting
  exoplanets (NEAT)** — GTO program description, no science content.
  Skip.
- **VizieR Online Data Catalog: NIR transmission spectra of TRAPPIST-1
  planets (Zhang 2018)** — data catalog, content already in Zhang 2018
  paper. Skip.
- **Limits on Clouds and Hazes in the TRAPPIST-1 Planets: insights from
  the laboratory** — likely Moran 2020 lab follow-up to the 2018
  paper. **Mild interest** for haze parameters; not decision-critical
  given JWST data.
- **Insights into the atmospheres of the TRAPPIST-1 planets from the
  laboratory and modeling** — similar to above. Skip.
- **Characterizing JWST NIRSpec's Noise Performance with a Lab-Measured
  Time Series** — instrument, not science. Skip.
- **Prospects for Biosignature Detection with JWST** (x2) — predates
  JWST data. Skip.
- **Experimental Constraints for Improving Terrestrial Exoplanet
  Photochemical Models** — methodology, no specific d constraint. Skip.
- Remaining ~10 entries: NEAT program / conference summaries.

**User action requested:** If the "Confirmation of a Dynamical Model for
the TRAPPIST-1 Exoplanetary System" paper is accessible, please paste —
it could refine the orbital parameters table above.

---

## Open items for follow-up

- Validate the Bond albedo choice (0.10) against any future emission
  spectroscopy of d. T-1 b is at 0.0 ± 0.1 (Greene 2023), c is
  similar; d may differ if it retains any volatile/cloud component.
- Refine surface tint hex codes when a renderer is available for visual
  testing under M8V illumination.
- Cfg variant for 3:2 spin-orbit case (Way 2025 alt scenario) if any
  KSP/Principia gameplay distinction merits it.
- Cross-check 0.01 bar atmosphere choice against the Kopernicus
  PQS+atmosphere interaction model — at this pressure the atmosphere
  is essentially decorative.
- The Dobos 2019 albedo tension (A_B ≥ 0.3 needed to avoid runaway if
  any liquid water present) deserves explicit cfg attention if a future
  renderer wants to support a "wet d" variant. The canonical cfg sits
  at A_B = 0.10 under the airless / near-airless interpretation; the
  wet variant would need A_B ≥ 0.3.
- The cloud-resonant aurora at the terminator is a unique cfg signature
  for d. It depends on the H₂O ice cloud altitude being above the
  auroral precipitation deposition layer — if future observations push
  the cloud altitude down, the cyan-white glow may need revision.
- The 25 Sv/yr surface dose places d in Kerbalism's "high-radiation"
  bracket; crew habitation would need shielding equivalent to ~2 m of
  regolith.

## Related

- [trappist-1-c](trappist-1-c.md) — adjacent inner sibling; both have low-confidence atmosphere scenarios
- [trappist-1-e](trappist-1-e.md) — habitable-zone reference; d sits at the inner HZ edge
- [trappist-1-f](trappist-1-f.md) — outer sibling; both rely on Wolf 2017 / Turbet GCMs
- [methodology](../reference/methodology.md) — Decisions schema and confidence rubric
- [mod-reference](../reference/mod-reference.md) — downstream mods
- [rex-data-comparison](../reference/rex-data-comparison.md) — §10 shows d's mass −5% vs REX (close agreement)
