<!-- TRAPPIST-1 d Phase 3 synthesis: cfg-ready decisions and reasoning -->
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
| `density_g_cc` | 5.43 | high | Agol 2021 |
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

- **2502.00132** Way 2025 — "TRAPPIST-1 d: Exo-Venus, Exo-Earth or
  Exo-Dead?" ROCKE-3D 3D GCM suite under 17 boundary-condition
  variants. Provides the climate-scenario envelope (Arid-Venus through
  Aquaplanet), surface temperature ranges, and an explicit comparison
  to Wolf 2017 / Turbet 2018 / Rushby 2020.
- **2508.08416** Piaulet-Ghorayeb 2025 — JWST NIRSpec/PRISM transmission
  spectrum. Definitive observational constraint. Drives the atmosphere
  scenario choice and the bare-rock surface interpretation.
- **2511.10801** Salman 2024 — Atmosphere-interior model with carbon
  cycle. Constrains outgassing composition as a function of mantle
  oxygen fugacity and initial water mass fraction. Supports trace-CO₂
  + H₂O composition over H₂-rich.

### Read (context / methodology, not decision-driving)

- **1802.02250** de Wit 2018 — HST WFC3 atmospheric reconnaissance.
  Initial constraint on H₂-rich atmospheres (8σ for d). Superseded by
  Piaulet 2025 but historically the first non-detection.
- **1810.05210** Moran 2018 — HST haze/cloud limits with updated
  masses. Showed metallicity > 60× solar with tropospheric clouds
  consistent with HST. Superseded by JWST.
- **2103.08600** Welbanks 2021 — Aurora retrieval framework. Predicted
  10-transit JWST NIRSpec detection feasibility for CO₂-rich or N₂-rich
  d atmospheres. The Piaulet 2025 observation is the experimental
  realization of this prediction (with 2 transits, achieving the
  predicted sensitivity).
- **2206.00028** Meadows 2022 — Atmospheric exchange biosignature
  false-positive (O₂ from d transported to e). Constrains plausible
  volatile transport mechanisms but not directly visual.
- **2210.02484** Hill 2022 — Habitable-zone exoplanet catalog. Lists
  d as one of three transiting ≤2 R⊕ HZ planets favorable for follow-up
  alongside LHS 1140 b and K2-3 d. Context only.
- **2304.12490** Hardegree-Ullman 2023 — ELT O₂ detectability survey.
  Estimates 16–55 years of integration to detect Earth-like O₂ on
  d–g with future ground-based ELTs. Not visual-informative but
  contextualizes the long-timescale observational future.

### Read (instrument-only, not visual-informative)

- **2203.04173** Rustamkulov 2022 — JWST NIRSpec lab time-series
  characterization. Methodology reference for the Piaulet 2025
  observation. Used `inject-recovery` simulations on TRAPPIST-1 d
  spectra but the planet appears only as a test case.

### Not read — no arXiv preprint available (22 papers)

These were surfaced by the ADS query but lack arXiv preprints; would
require institutional library access or PDF paste. For Phase 3 d, the
key papers in this set are:

- **2025epsc.conf..178P** Piaulet-Ghorayeb 2025 EPSC abstract — likely
  a conference summary of the JWST paper already read (2508.08416).
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
