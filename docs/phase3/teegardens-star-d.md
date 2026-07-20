<!-- Teegarden's Star d Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Teegarden's Star d — Phase 3 Synthesis

Teegarden's Star d is a 0.82 M⊕ minimum-mass sub-Earth-mass rocky
planet on a 26.13-day orbit, with semi-major axis 0.0791 AU. It is
the most recently discovered planet in the system — added by Dreizler
2024 ([arXiv:2402.00923](https://arxiv.org/abs/2402.00923)) using the combined CARMENES + ESPRESSO +
MAROON-X + HPF radial-velocity dataset. The K = 0.86 ± 0.17 m/s
detection lies near the noise floor of the multi-instrument fit, but
the Bayesian evidence improves by more than 5 (Dreizler 2024 Table 10:
model E with d vs the no-d model) — the paper's own significance
threshold for accepting the more complex model — so the detection is
robust. d is the only planet in this system discovered after the 2019
Zechmeister CARMENES discovery paper.

At S = 0.12 S⊕ (Dreizler 2024) — about 1/8 of Earth's insolation —
and equilibrium temperature 159 K (Bond albedo 0.3) or ~165 K (zero
albedo), d sits well beyond the conservative habitable zone. Dreizler
2024 §5.2 explicitly compares its surface temperatures to "Jupiter or
its icy moon Ganymede." Without a thick greenhouse atmosphere, d is
a frozen rock. The cfg renders it as such, with comparison to Mercury
(for the bare-rock surface) and Ganymede (for the cold frozen-ocean
analog).

No GCM modelling has yet been published specifically for d — it is
too cold and outside the standard HZ catalogue to feature in
Boukrouche 2025 (b only), Hammond 2025 (b, c, and other inner-HZ
targets), or Fujii 2026 (b benchmark). The cfg synthesis therefore
relies on analytic scaling from Dreizler 2024's stated equilibrium
temperatures and from Solar System analogs (Mercury, Ganymede, cold
Mars).

**Scenario choice for NearStars: cold sub-Earth bare-rock world with
trace CO₂-N₂ atmosphere (much like cold Mars) or possibly atmosphere-
less (Mercury-analog at this insolation). The cfg picks a thin-
atmosphere variant: ~5 mbar CO₂-N₂ remnant with seasonal CO₂ frost
deposition on the nightside; bedrock primary surface with frost
mottling and rare ice patches in polar/cold-trap regions.** This is
the cfg's "cold rocky" archetype, contrasting with b's habitable
aquaplanet and c's global snowball.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true (pseudo-synchronous, not pure 1:1) | medium | P_orb = 26 d is inside the Griessmeier 2009 tidal-lock timescale for M = 0.089 M☉ host over 8 Gyr; but e = 0.07 is above the Vinson 2017 / Makarov 2018 1:1 threshold (e ≳ 0.01), so the spin settles into a pseudo-synchronous state rather than exact 1:1 |
| `obliquity_deg` | 0 | medium | tidal damping at this period over 8 Gyr |
| `eccentricity` | 0.07 | high | Dreizler 2024 (poorly constrained: +0.10/−0.05) |
| `argument_of_periastron_deg` | 345 | low | Dreizler 2024 (poorly constrained: +129/−93) |
| `sidereal_period_days` | 26.13 | high | Dreizler 2024 |
| `semi_major_axis_au` | 0.0791 | high | Dreizler 2024 |
| `mass_mearth` | 0.82 (msini) | high | Dreizler 2024 — discovery K = 0.86 m/s |
| `radius_rearth` | 0.954 | medium | DB mass-radius-relation derived for 0.82 M⊕ (Zeng 2016 Earth-like MR); non-transiting, no measured radius |
| `surface_gravity_g_earth` | 0.90 | medium | derived = 0.82 / 0.954² |
| `density_g_cc` | 5.2 | low | derived = 5.513 × 0.82 / 0.954³; no transit so M sin i only — Earth-like rocky assumed |
| `insolation_s_earth` | 0.12 | high | Dreizler 2024 |
| `equilibrium_temp_k` (A=0) | 165 | high | derived from S=0.12 and Earth A=0 baseline T = 279 K (279 × 0.12^¼ = 164) |
| `equilibrium_temp_k` (A=0.3) | 159 | high | Dreizler 2024 |
| `bond_albedo` | 0.30 | low | Tie-break: bare-rock with patchy frost; intermediate between Mercury (0.07) and ice-covered (0.5) |
| `surface_temp_substellar_k` | 200 | low | Tie-break: thin-atmosphere case; substellar warmed by direct illumination, no greenhouse |
| `surface_temp_nightside_k` | 60 | low | Tie-break: Mercury-style cold trap; CO₂ frost deposition lowers it below CO₂ condensation point at 5 mbar |
| `surface_temp_global_mean_k` | 130 | low | Tie-break: averaged across day-night; matches Ganymede surface mean (~110 K) and cold Mars (~210 K) range |
| `atmosphere_present` | true (trace) | low | Tie-break: thin CO₂-N₂ remnant; not Mercury-airless because some volatile delivery expected for 0.95 R⊕ rocky |
| `atmosphere_surface_pressure_pa` | 500 | low | Tie-break: ~5 mbar — comparable to current Mars pressure; below CO₂ frost point on nightside so atmospheric collapse cycle plausible |
| `atmosphere_composition` | CO₂ 70%, N₂ 28%, Ar 1%, H₂O trace | low | Tie-break: Mars-analog composition for a cold rocky outgassed atmosphere |
| `atmosphere_scale_height_km` | 2.8 | medium | derived: kT/μg with T=130 K, μ=44 (CO₂-dominated), g=8.84 m/s² |
| `atmosphere_tint_rgb_hex` | `#2a2a30` (almost negligible) | low | Tie-break: trace atmosphere produces minimal Rayleigh; sky is nearly black with star and sister planets visible |
| `cloud_cover_fraction` | 0.02 | low | Tie-break: rare CO₂-ice clouds near nightside terminator only |
| `cloud_morphology` | Occasional CO₂-ice clouds in terminator twilight zone where temperature crosses CO₂ frost point | low | Mars-analog seasonal CO₂ frost cycle |
| `cloud_tint_rgb_hex` | `#a8a090` (very dim white-pink under M7 V) | low | Tie-break |
| `ocean_present` | false | high | T << 273 K; no liquid water possible |
| `subsurface_water_ice_probable` | true | medium | Like Mars / Ganymede — cold dry rocky planet should have subsurface water-ice or possibly buried ocean; not observable |
| `surface_morphology` | Bare basaltic / silicate bedrock with extensive frost mottling at polar / cold-trap regions; impact-cratered like Mercury or Callisto; sparse exposed ice at perpetually-cold cold-trap zones | medium | Mercury / cold Mars / Ganymede analog physics; no Teegarden-d-specific paper |
| `surface_tint_rgb_hex_primary` | `#6a5a4a` (basalt under M-dwarf light; Mercury-like) | medium | Tie-break: dark rocky surface + red-shifted illumination — looks reddish-brown rather than gray |
| `surface_tint_rgb_hex_accent` | `#e8e0d4` (CO₂ frost / water ice in polar cold traps and at terminator) | medium | Tie-break: bright frost contrasts dramatically against dark bedrock |
| `magnetic_field_present` | false (or very weak) | low | Tie-break: small body, slow rotation, old age — dynamo may have shut down |
| `magnetic_field_strength_microtesla_equator` | 5 | low | Tie-break: weak crustal-remnant field only |
| `aurora_present` | false (or extremely weak) | low | Tie-break: no/trace atmosphere + weak B-field — no significant aurora |
| `surface_radiation_dose_msv_yr` | 500 | low | Tie-break: thin atmosphere + weak B-field gives Mars-like surface dose; quiet M7 V keeps it modest |
| `star_apparent_angular_diameter_deg` | 0.72 | high | derived: 2 × 0.107×0.00465 / 0.0791 × 57.3 = 0.72° (1.3× the Sun from Earth) |
| `stellar_illumination_color_temp_k` | 2904 | high | Schweitzer 2019 |

## Surface synthesis

Teegarden d is the system's cold outer rocky world — sub-Earth in
mass, beyond the conservative habitable zone, and lacking the
insolation needed to maintain liquid water under any plausible
atmospheric composition. Dreizler 2024 §5.2 frames it explicitly:
"the newly discovered planet d is cold, residing on an orbit of about
a month, resulting in temperatures akin to Jupiter or its icy moon
Ganymede."

The Solar System analogs that bracket d's parameter space are:

- **Ganymede** (radius 2634 km, T_surface 110 K, no atmosphere):
  d would have higher T_surface (~130 K mean) due to its rocky
  composition and the modest direct M-dwarf flux, but the
  ice-covered surface analogy partially holds.
- **Mercury** (radius 2440 km, T_surface 100-700 K, no atmosphere,
  thermal extremes from tidal lock partially synchronous, weak B-
  field): d's tidally-locked surface extremes would resemble Mercury
  but at lower mean temperature.
- **Cold Mars** (radius 3389 km, T_surface 130-280 K, 6 mbar CO₂
  atmosphere, polar CO₂ frost cycle): the closest direct analog for
  d's atmospheric state if a residual CO₂ atmosphere is present.

The cfg picks a hybrid scenario: **bare basaltic bedrock with extensive
frost mottling**, a **trace ~5 mbar CO₂-N₂ atmosphere**, and a
**seasonal CO₂ frost deposition cycle** on the nightside cold-trap.

Surface morphology:

- **Substellar dayside (~200 K)**: Bare bedrock, primarily dark basalt
  / silicate. Frost patches in shadowed crater interiors but not
  general surface cover. Mercury-style impact crater morphology.
- **Mid-latitudes / terminator (~130 K)**: Mixed bedrock and frost
  cover; CO₂ frost deposition cycles diurnally — but with a 26-day
  synchronous rotation, "diurnal" is actually orbital.
- **Nightside (~60 K)**: Permanent CO₂-frost cold trap. Atmospheric
  pressure locally drops as CO₂ condenses out. Water ice may also be
  permanently stable here.

**Colour choice.** The bedrock under M7 V illumination reads as
reddish-brown `#6a5a4a` rather than the gray of an Earth-Sun
illuminated basalt — the red-shifted SED of the host star saturates
the dark mafic minerals into a warm tone. The bright accent `#e8e0d4`
(CO₂ frost and water ice) provides dramatic visual contrast against
the dark bedrock background.

**Exposed ice patches.** Where present, water ice in cold traps would
appear under M7 V illumination as bright cream-orange — distinct from
CO₂ frost (also bright, slightly more bluish-pink). Player-visible
ice deposits would be the most striking surface features.

## Atmosphere synthesis

No published GCM exists for d. The cfg picks a **trace ~5 mbar CO₂-N₂
atmosphere** as a "cold Mars" analog. Justification:

1. **Volatile delivery**: A 0.82-M⊕ rocky body in the cold zone
   should accrete enough volatiles during planet formation to
   outgas a thin atmosphere over Gyr timescales.
2. **Retention**: The 8-Gyr-old quiet star + d's cold equilibrium
   temperature give modest atmospheric escape rates. A primordial
   atmosphere is more likely to have survived than at b's hotter
   inner-HZ position.
3. **Surface freezing**: Mean T = 130 K is below the CO₂ frost point
   at 5 mbar (~150 K), so the nightside cold-trap would deposit CO₂
   as ice, reducing atmospheric pressure. Earth-Mars-style seasonal
   cycle physics applies on the orbital timescale.

Composition assumed:

- **Pressure** 5 mbar (500 Pa) — Mars-analog.
- **Composition** CO₂ 70%, N₂ 28%, Ar 1%, H₂O trace.
- **Clouds** Rare CO₂-ice clouds in the terminator twilight zone
  where surface T crosses CO₂ frost point seasonally.

**Sky appearance.** Almost negligible — only ~5 mbar of atmosphere
produces minimal Rayleigh scattering. Sky is nearly black with the
host star and sister planets prominently visible. The host appears
as a dim red disk of 0.72° angular diameter (about 1.3× the Sun's
angular size from Earth) — much smaller than from b or c.

**Auroras** are essentially absent — no/trace atmosphere + likely
weak magnetic field mean any incoming SEP particles deposit energy
directly into the surface rather than producing emission.

The alternative cfg scenario is **fully airless Mercury-analog** — no
atmosphere at all. This is consistent with d's parameters if (a)
volatile accretion was minimal during formation or (b) all primordial
atmosphere was stripped during the pre-MS phase. The cfg picks the
thin-atmosphere variant because it produces more interesting visuals
(frost cycling, occasional CO₂-ice clouds) and because Mars-analog
retention is at least as likely as Mercury-analog stripping for a
0.82 M⊕ rocky body at this distance.

## Rotation & spin synthesis

P_orb = 26.13 d is firmly inside the Griessmeier 2009 tidal-lock
timescale for an M = 0.089 M☉ host over 8 Gyr, so d is tidally evolved.
But eccentricity 0.07 sits **above** the Vinson 2017 / Makarov 2018
threshold (3:2 stable only for e ≳ 0.01, exact 1:1 favoured below), so
the spin settles into a **pseudo-synchronous** state — rotating
slightly faster than the orbital mean motion, tracking the angular
velocity at periastron — rather than a strict 1:1 lock. The substellar
point therefore librates and slowly migrates rather than staying
exactly fixed. Obliquity is damped to zero. The eccentricity is too
small for a stable 3:2 capture, but large enough to forbid an exact
synchronous rotation.

**KSP implementation note.** Pseudo-synchronous rotation period is
within ~7% of the orbital period (set by the e=0.07 periastron angular
velocity); the cfg uses rotation period ≈ orbital period = 26.13 days
(2 257 632 s), the same value to Kopernicus precision, with the
libration captured as slow substellar drift rather than a distinct
period.

**Atmospheric circulation.** With only ~5 mbar of atmosphere there is
minimal advection, but a weak superrotating jet might still exist.
The atmospheric column is too thin to homogenize temperatures
significantly — substellar (~200 K) and nightside (~60 K) differ by
~140 K. The temperature gradient drives the CO₂-frost cycle: CO₂
sublimates on the dayside as the local surface T crosses the frost
point at the morning terminator, and deposits at the evening
terminator. This is the orbital-period analog of Mars's seasonal
polar CO₂ cycle.

**No seasons.** Obliquity = 0.

**Magnetic dynamo.** Likely absent or extremely weak. d's sub-Earth
mass (0.82 M⊕) and slow pseudo-synchronous rotation give a small,
slowly-rotating core that probably cannot sustain a self-organized
dynamo over 8 Gyr. The cfg picks 5 μT equatorial as a
crustal-remnant-only field — much weaker than b's 25 μT.

## Visual styling

Combining surface and atmosphere decisions:

- **Global appearance from orbit.** A small dark rocky world with
  bright frost mottling. The contrast between dark `#6a5a4a` bedrock
  and bright `#e8e0d4` frost gives a Mercury-like cratered look but
  with the frost coverage of a cold Mars. The thin atmosphere
  produces no limb haze.
- **Dayside (substellar)**: Predominantly dark basalt. Impact craters
  punctuate the smooth basaltic plains; some craters have bright frost
  centers where ejecta exposed sub-surface ice.
- **Terminator zone**: Mixed bedrock and frost. The most visually
  active region — the morning terminator shows CO₂ sublimation
  signatures as faint cloud puffs; the evening terminator shows
  CO₂ frost deposition. Color transitions from `#6a5a4a` bare rock
  to `#e8e0d4` frost across a few hundred km width.
- **Nightside**: Permanent CO₂-frost cold trap. Surface is uniformly
  bright (very high frost albedo) but barely illuminated — frost
  visibility requires reflected light from the star (only at the
  edges of the trap), reflected light from sister planets b and c
  at conjunction, or starlight from background stars.
- **Atmosphere haze**: Essentially absent. No discernible limb glow.
- **Star in sky.** Teegarden's Star subtends 0.72° (about 1.3× the
  Sun from Earth). Smallest apparent star in the system view.
- **Sister planets in sky.** b at inferior conjunction (~0.15°,
  m_v ≈ −3); c at inferior conjunction (~0.1°, m_v ≈ −2). Both
  much smaller than from each other's perspective. Conjunctions
  every 6 days for b and 20 days for c at the beat periods.

The overall visual impression should evoke Mercury crossed with cold
Mars — a small, dark, frosted rocky body that is visually quiet but
geologically detailed. From a player's perspective, d is the system's
"explore the rocks" world, contrasting with b's "explore the ocean"
and c's "explore the ice".

## Bibliography

### Read (visual-informative, drove decisions above)

- **Dreizler S. et al. 2024** — *Teegarden's Star revisited. A nearby
  planetary system with at least three planets*, A&A 684, A117
  (`2024A&A...684A.117D`, [arXiv:2402.00923](https://arxiv.org/abs/2402.00923)). The discovery paper for
  d. Provides P = 26.13 d, msini = 0.82 M⊕, a = 0.0791 AU, e = 0.07,
  T_eq = 159 K (A=0.3), S = 0.12 S⊕. The §5.2 comparison to "Jupiter
  or Ganymede temperatures" is the cfg's primary qualitative anchor.

### Read (context / methodology, not decision-driving)

- **Zechmeister M. et al. 2019** — Context for the host star (b and c
  discovery; planet d was not yet detected). [arXiv:1906.07196](https://arxiv.org/abs/1906.07196).
- **Schweitzer A. et al. 2019** — Stellar parameters (Teff 2904 K,
  L, R, M). [arXiv:1904.03231](https://arxiv.org/abs/1904.03231).
- **Wandel A. & Tal-Or L. 2019** — Habitability framework (b and c
  only). [arXiv:1906.07704](https://arxiv.org/abs/1906.07704). d falls outside their habitability zone.

### Read (instrument / non-cfg-decisive)

- General Solar System cold-world references (Mercury, Mars, Ganymede
  analog physics) — not in the bib but used as reference frame.

### Not read — no arXiv preprint or low-priority

d's bibliography is essentially empty by design — only Dreizler 2024
contains the discovery and the entire body of measurements. The cfg
synthesis is therefore unusually dependent on a single paper plus
Solar System analog reasoning.

## Open items for follow-up

- **Atmospheric presence (CRITICAL UNKNOWN)**: No direct constraint
  exists for d. The cfg picks a thin Mars-analog atmosphere as a
  reasonable default. If a future occultation or thermal-emission
  observation finds the surface to be Mercury-airless, the cfg
  should remove the atmosphere and switch surface temperatures to
  pure radiative-equilibrium (substellar T might rise toward 270 K,
  nightside drops below 30 K). This airless Mercury-analog is the
  preserved tie-break variant.
- **Truly Ganymede-analog ice-covered scenario**: Dreizler 2024
  compares d to "Ganymede temperatures" — Ganymede is fully ice-
  covered (water-ice crust over a putative subsurface ocean), not
  bare rock. The cfg's bedrock-primary choice is partly visual
  diversification (b is ocean, c is ice, d is rock) and partly
  reflects d's higher density (~5 g/cc rocky vs Ganymede's 1.9 g/cc).
  An ice-shell variant cfg with global water-ice crust is preserved
  here as an alternative.
- **Frost cycle period**: With P_orb = 26 d the CO₂ frost cycle is
  fast. No paper has modeled this for d. A future thermal IR
  observation could detect the seasonal modulation directly.
- **True mass and inclination**: Like b and c, d's true mass at typical
  i = 60° geometric inclination would be ~0.95 M⊕ (still sub-Earth).
  Astrometric follow-up could constrain inclination.
- **Subsurface ocean**: d's cold surface could overlie a buried liquid
  water layer if heated by radiogenic decay + tidal dissipation — but
  with a 26-d orbit and modest eccentricity, tidal heating is small.
  Not currently rendered in cfg.
- **No GCM specific to d**: All recent climate-modelling work on
  Teegarden's system focused on b (Boukrouche 2025, 2024, 2026; Fujii
  2026) or c (Hammond 2025). A dedicated cold-rocky GCM for d would
  significantly tighten the synthesis but does not exist.

## Related

- [teegardens-star](teegardens-star.md) — M7 V host
- [teegardens-star-b](teegardens-star-b.md) — inner sibling, temperate aquaplanet
- [teegardens-star-c](teegardens-star-c.md) — middle sibling, global snowball
- [trappist-1-h](trappist-1-h.md) — sister-system cold outer planet (TRAPPIST-1 h is in fact warmer at S = 0.144 S⊕ — d is colder)
- [methodology](../reference/methodology.md) — Decisions schema
