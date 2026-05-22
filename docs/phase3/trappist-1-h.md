<!-- TRAPPIST-1 h Phase 3 synthesis: cfg-ready decisions and reasoning -->
# TRAPPIST-1 h — Phase 3 Synthesis

TRAPPIST-1 h is a 0.76 R⊕, 0.33 M⊕ sub-Mars-mass rocky planet on a
18.77-day orbit around an M8V ultra-cool dwarf. Outermost of the
seven, receiving only 0.16× Earth's insolation. Its orbital period
and resonant-chain placement were confirmed by Luger 2017
(1703.04166) using K2 mission data. Gressier 2022 (2112.05510)
obtained the first HST WFC3/G141 near-infrared transmission spectrum
and excluded cloud-free hydrogen-rich atmospheres; no JWST follow-up
has been published as of 2026-05-21. The interesting twist for h:
Lincowski 2018 (1809.07498) notes that a **desiccated** h could
support habitable surface temperatures beyond the maximum-greenhouse
distance under specific 10–100 bar O₂ + CO₂ post-runaway scenarios —
making h the system's most counterintuitive habitability candidate.

**Scenario choice for NearStars: frozen sub-Mars rocky world with
patchy CO₂ + N₂ ice frost over weathered bedrock; very thin
(~0.005 bar) residual atmosphere from late outgassing.** This adopts
the more conservative reading of the cosmic-shoreline literature
(Castan-Lopez 2025, Zahnle 2017) for a low-mass planet at low
insolation, where most volatiles have either been lost or frozen to
the surface. The alternative — Lincowski 2018's "desiccated
habitable" scenario — is preserved as a cfg variant but is less
visually distinctive (a thick CO₂/O₂ atmosphere over a warm dry
rocky surface).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 18.77 d orbit, tidal damping; Agol 2021 |
| `obliquity_deg` | 0 | high | tidal damping; Agol 2021 |
| `eccentricity` | 0.00567 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 339 | medium | Agol 2021 (low ecc → weak constraint) |
| `sidereal_period_days` | 18.7729 | high | Agol 2021; Luger 2017 K2 confirmation |
| `semi_major_axis_au` | 0.06189 | high | Agol 2021 |
| `mass_mearth` | 0.326 | high | Agol 2021 TTV — sub-Mars (Mars 0.107, Mercury 0.055) |
| `radius_rearth` | 0.755 | high | Agol 2021; Gressier 2022 transit fit |
| `surface_gravity_g_earth` | 0.572 | high | derived = 0.326 / 0.755² |
| `density_g_cc` | 4.20 | high | Agol 2021 (water-rich) |
| `water_mass_fraction` | 0.03–0.10 | medium | tightened from earlier 0.05–0.15 — Lichtenberg 2019 ²⁶Al desiccation argues for low end; Bourrier 2017 brief runaway phase (33–67 Myr) preserves most accreted water |
| `insolation_s_earth` | 0.144 | high | Agol 2021 / Gillon 2024 (2401.11815) — corrected from previous round 0.16 |
| `equilibrium_temp_k` (A=0)   | 169 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.5, frosted) | 142 | high | derived; frosted-surface case |
| `bond_albedo` | 0.40 | medium | mixed bedrock + CO₂/N₂ frost; less reflective than full snowball |
| `surface_temp_substellar_k` | 175 | medium | passive radiative balance, slight greenhouse from trace atmo |
| `surface_temp_nightside_k` | 60 | medium | very cold; N₂ ice frost point reached |
| `surface_temp_global_mean_k` | 140 | medium | weak redistribution from thin atmo |
| `atmosphere_present` | true (very tenuous) | low | Gressier 2022 rejects H₂-rich; trace outgassed CO₂ + N₂ plausible |
| `atmosphere_surface_pressure_pa` | 500 | low | 0.005 bar — minimal residual; Mars-thin |
| `atmosphere_composition` | N₂ ~90%, trace CO₂ 10–100 ppm, Ar / H₂O trace | low | Bolmont 2018 review caps p_CO₂ partial pressure at 100–1000 ppm regardless of background; Turbet 2017 tightens to "a few tens of ppm" at 1 bar N₂ for h's surface temperature regime (pure-CO₂ equilibrium = 4 mbar at 145 K, but with N₂ background the effective trace CO₂ is much lower). |
| `atmosphere_scale_height_km` | 6.0 | medium | derived: kT/μg with T≈140 K, μ=40, g=5.6 m/s² |
| `atmosphere_tint_rgb_hex` | `#302820` (essentially imperceptible Rayleigh) | low | very thin atmo, M-dwarf SED → negligible scattering |
| `cloud_cover_fraction` | 0.02 | low | minimal — sporadic CO₂ ice cirrus only |
| `cloud_tint_rgb_hex` | n/a | high | clouds too sparse for cfg-relevant tint |
| `ocean_present` | uncertain (sub-glacial possible if wmf at upper bound) | low | low mass + low temp → less basal melt than g; ocean if any is thin and Europa-like |
| `surface_ice_caps` | H₂O ice cover globally, with buried CO₂ ice underneath; minor bedrock outcrop near substellar | medium | Turbet 2017 (1707.06927) shows surface CO₂ ice is gravitationally unstable on h and gets buried beneath the H₂O ice shell over geological timescales. Surface frost is therefore predominantly H₂O ice with CO₂ ice as a deeper layer. |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (H₂O ice / snow under M-dwarf light) | medium | Surface is predominantly H₂O ice (Turbet 2017 burial argument); the iron-rich bedrock is exposed only in localized substellar regions. Color palette inverts relative to the Mars-Pluto hybrid framing — cream-white dominant, dark bedrock as minor accent. |
| `surface_tint_rgb_hex_accent` | `#3a2c20` (weathered iron-rich bedrock — minor, only at substellar) | low | Surface is predominantly H₂O ice (Turbet 2017 burial argument); the iron-rich bedrock is exposed only in localized substellar regions. Color palette inverts relative to the Mars-Pluto hybrid framing — cream-white dominant, dark bedrock as minor accent. |
| `surface_morphology` | cratered ancient bedrock near substellar, patchy CO₂/N₂ ice frost toward terminator and nightside | medium | Mars/Mercury analog; very low resurfacing rate |
| `magnetic_field_present` | false (low mass + cold + slow rotation) | low | likely no active dynamo; small fossil field possible |
| `induction_heating_w_m2` | 0.001–0.01 | medium | Grayver 2022 — lowest in system due to distance + small mass |
| `tidal_heating_w_m2` | 0.00001–0.0001 | medium | Bolmont 2020 — negligible at h |
| `radiogenic_heat_w_m2` | 0.025 | medium | scaled by mass; slightly less than Earth-analog |
| `magnetic_field_strength_microtesla_equator` | 0.5 | low | Sub-Mars mass (0.33 M⊕) → dynamo likely shut off; Mars-analog crustal remnant field |
| `magnetic_dipole_moment_normalized_earth` | 0.005 | medium | 2208.06523 thermal evolution + RM22 — low-mass planets reach dynamo shutoff early (<1 Gyr) |
| `magnetic_dipole_tilt_deg` | 10 | low | Tie-break: 10° offset; potentially crustal anomaly-dominated like Mars (no clear dipole axis) |
| `magnetosphere_standoff_planet_radii` | 1.2 | medium | Essentially no global magnetosphere; induced magnetosphere only (Venus/Mars-analog); standoff at ionopause ≈ R_planet |
| `radiation_belt_present` | false | high | B-field <0.1 Earth → no Van-Allen-like trapped regions |
| `surface_radiation_dose_msv_yr` | 4000 | medium | Atri 2019 (1910.09871) scaling for h at 0.062 AU; GCR background dominates with weak shielding |
| `atmospheric_shielding_g_cm2` | 5 | medium | Phase 3 cfg pressure 0.005 bar → ~5 g/cm² column |
| `aurora_present` | true | medium | Atm + crustal/induced magnetic field → patchy Mars-like discrete aurora |
| `aurora_color_primary_hex` | `#4DFF4D` | low | N₂ Vegard-Kaplan bands + [NI] 520 nm green if trace O; tie-break: visible green over UV-only |
| `aurora_color_secondary_hex` | `#B19CD9` | low | N₂ Lyman-Birge-Hopfield bands UV-perceived violet |
| `aurora_emission_species_primary` | `N₂ Vegard-Kaplan bands 200–300 nm + N₂⁺ 391.4 nm + N₂ Lyman-Birge-Hopfield` | low | Thin N₂-dominated atm |
| `aurora_oval_magnetic_latitude_deg` | 15 | low | No organized dipole → patchy crustal aurora at random latitudes; representative value |
| `aurora_intensity_kR_typical` | 30 | low | Thinnest atm + weakest field; bright per particle but few collisional targets |
| `star_apparent_angular_diameter_deg` | 1.03 | high | derived: 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## Surface synthesis

TRAPPIST-1 h is the system's smallest planet (0.326 M⊕, sub-Mars
mass) and lies at 0.16 S⊕ insolation. The combination — small mass,
low gravity (0.572 g), and low insolation — makes h a difficult case
for atmospheric retention. The cosmic shoreline literature
(Castan-Lopez 2025 — 2504.19872 — , Zahnle 2017) places h close to
or below the empirical retention threshold for hydrogen-bearing and
even nitrogen-bearing atmospheres. Some volatile retention is
plausible (CO₂ has high enough molecular weight to survive Jeans
escape at h's temperatures) but the atmospheric mass is likely
small.

Despite the low mass, h's bulk density (4.20 g/cc from Agol 2021)
is low enough to imply a non-trivial water mass fraction (~5–15%),
similar to f and g but with much less mass to work with. Most of
this water is likely frozen at the surface (CO₂ and H₂O ice) or
sequestered as a thin sub-glacial layer over a small rocky core.

The Lincowski 2018 (1809.07498) "desiccated h" scenario — habitable
surface temperatures from a thick (10–100 bar) CO₂/O₂ post-runaway
atmosphere — is preserved as a cfg variant but is not the canonical
choice. The post-runaway atmospheric retention timescale at h's
escape velocity is short (≲ 1 Gyr); over 7.6 Gyr of system age,
most of any initial thick atmosphere has been lost.

For the surface morphology, we adopt a Mars-Pluto hybrid analog:

- **Substellar region** (~0–60° from substellar): bedrock-dominated,
  weathered iron-rich surface analogous to Mars's southern
  highlands. Some patchy CO₂ frost in shadowed craters.
- **Mid-zone** (60–120°): increasing frost cover with distance from
  substellar.
- **Terminator** (~90°): high frost-vs-bedrock contrast; long
  topographic shadows under grazing 2566 K light.
- **Nightside** (>120°): predominantly CO₂ + N₂ frost cover at
  ~60 K, with occasional dark bedrock patches at ridge tops.

**Color choice — H₂O ice dominant.** Turbet 2017 shows that even though h's atmosphere is dominated by trace CO₂ at low pressures, the surface frost composition is **predominantly H₂O ice** (not CO₂/N₂ frost as in earlier framings). CO₂ ice deposits form transiently but are gravitationally unstable — they get buried beneath the H₂O ice shell over geological timescales. The visible surface is therefore cream-white (`#d8d0c4`) from clean H₂O ice under M-dwarf illumination, with minor weathered iron-rich bedrock patches (`#3a2c20`) exposed only in localized substellar regions where ice has sublimated. The Mars-Pluto hybrid framing inverts: cream-white dominant globally, with dark bedrock as the minor accent rather than the primary surface tone.

**Interior structure.** Barr 2018 (1712.05641) finds h has a 1030 km rock core (mean-density case), with a maximum-density configuration allowing only ~100 km H₂O shell over the rock. The current cfg WMF 0.03–0.10 sits between these extremes. h's CMF is at the lower end of the system (~0.23), consistent with a relatively iron-poor rocky body.

**Mars-analog patchy aurora geometry.** With no organized global dynamo (sub-Mars mass, frozen core after 7.6 Gyr), h's magnetic field is dominated by **crustal remnants** in localized patches — directly analogous to Mars (Acuña 1999 MAG/ER discovery). Combined with the thin N₂ atmosphere, this produces a *patchy* aurora geometry rather than the regular auroral oval seen on Earth or g. Each crustal magnetic anomaly funnels stellar-wind particles into a localized aurora spot above its location, producing scattered green N₂ Vegard-Kaplan + N₂⁺ violet emissions. The aurora geometry is essentially random — wherever crustal magnetization survived — and the result is dramatically different from the inner planets' organized auroral bands. Cfg renders this as scattered `#4DFF4D` green patches with `#B19CD9` violet accent, distributed at low-to-mid magnetic latitudes rather than concentrated at the poles. Interesting-first tie-break chose this Mars-analog rendering over the alternative "uniform faint global glow" approach.

**Bedrock / iron oxide.** Prominent on h compared to g/f — the
exposed substellar bedrock has had 7.6 Gyr of photolytic oxidation
under direct stellar UV. The primary tint already incorporates
this; specific bright iron-oxide patches near impact crater rims
would be a fine-grained PQS detail.

**Morphology under tidal lock.** Almost no resurfacing — h's tidal
heating is negligible (Bolmont 2020), induction heating minimal
(Grayver 2022 distance scaling), and radiogenic heat too low (small
mass) to drive volcanism. The surface preserves a maximal impact
record across the system's 7.6 Gyr age, biased toward the leading
hemisphere in the locked frame.

## Atmosphere synthesis

Gressier 2022 (2112.05510) presented the first HST WFC3/G141
transmission spectrum of h, the planet's only published atmospheric
observation. The data are consistent with either no atmosphere or
a flat-spectrum secondary atmosphere; cloud-free hydrogen-rich
atmospheres are excluded.

Theoretical modeling:

- **Lincowski 2018:** considers desiccated post-runaway 10–100 bar
  CO₂/O₂ atmospheres for h, finding some give habitable surface
  temperatures. However, the retention probability of such thick
  atmospheres over 7.6 Gyr at h's escape velocity is low.
- **Bourgeois 2024:** magma ocean evolution gives an initial
  outgassed atmosphere of ~1 bar (CO₂ + H₂O); most lost over time.
- **Castan-Lopez 2025:** cosmic shoreline analysis suggests h is
  near or below the retention threshold for typical secondary
  atmospheres.

For NearStars we adopt **0.005 bar (Mars-thin) N₂-dominated atmosphere with trace CO₂**:

- **Pressure** 0.005 bar (500 Pa) — comparable to Mars. Above zero because some outgassing should accumulate on a 0.3 M⊕ planet; below 0.01 bar because cosmic-shoreline / Jeans-escape constraints suggest h cannot retain much more.
- **Composition** N₂-dominated (~90%), trace CO₂ (10–100 ppm, NOT 1000). The driver is Bolmont 2018 review's cold-trap argument plus Turbet 2017 specific calculation showing pure-CO₂ equilibrium is just 4 mbar at 145 K for h, and N₂-background scenarios give only "a few tens of ppm" CO₂ in the gas phase. The remaining ~10% is split among Ar, frost-cycle H₂O vapor, and fossil O₂.
- **Clouds.** Minimal (~2% global): rare CO₂ ice cirrus only.

**Atmospheric retention favored by ion-escape arguments.** Despite the cosmic-shoreline-threshold framing, Dong 2018 (1705.05535) finds h has the LOWEST ion escape rate in the system (1.29×10²⁶ s⁻¹) and the highest atmospheric retention timescale (~10¹⁰ yr) — "h ought to be the most stable planet from the perspective of atmospheric ion loss." Stellar wind dynamic pressure at h is "only" 100–300× Earth's vs. 10³–10⁴× at b. Krissansen-Totton 2022 (2207.04164) similarly concludes that outer planets "retain significant surface volatiles in virtually all model simulations" with "CO₂-dominated or CO₂-O₂ atmospheres for all planets that retain substantial atmospheres." The cfg's thin N₂+trace-CO₂ choice is conservative compared to this; a thicker (~0.1 bar) atmosphere is also defensible.

**Auroral chemistry.** The thin N₂-dominated atmosphere (≲100 ppm CO₂) produces a clean nitrogen-aurora chemistry: N₂ Vegard-Kaplan bands at 200–300 nm (UV, with some scattered to visible cyan-violet), N₂⁺ 391.4 nm First Negative blue, and Lyman-Birge-Hopfield bands. Trace O₂ (if present from photolysis) contributes [OI] 557.7 nm green. Per the crustal-anomaly geometry above, these emissions are concentrated in small spots rather than continuous bands. Intensity ~30 kR is the lowest in the system due to the very thin atmosphere — but each individual aurora spot is bright per unit area because precipitating particles deposit deeply into the thin air. For cfg rendering: faint green/violet patches with no organized polar geometry.

**Sky appearance.** The 0.005 bar atmosphere is essentially
invisible from orbit. From the surface, the sky is black except for
the host star (1.03° angular diameter, red-orange disk). Surface
illumination of 0.16 S⊕ is similar to outer Mars at perihelion.

## Rotation & spin synthesis

Tidal damping at 18.77 days over 7.6 Gyr → synchronous (1:1)
configuration. Obliquity damped to zero. Eccentricity is 0.00567 —
in the 1:1 dominance regime.

**KSP implementation note.** Rotation period = orbital period =
18.7729 days (1 621 977 s).

**No seasons.** Obliquity = 0; libration-induced insolation
variation < 0.5%.

**Resonant chain dynamics.** Luger 2017 (1703.04166) established
h's place in the 7-planet Laplace-resonance chain (8:5 mean-motion
resonance with g). The chain provides ongoing small-amplitude
perturbations of the orbital elements, but for visual / cfg
purposes the configuration is stable.

**Magnetic dynamo expectation.** h's small mass (0.33 M⊕, sub-Mars), advanced age (7.6 Gyr), and very slow tidally-locked rotation (18.8 d) make a sustained global dynamo essentially impossible. 2208.06523 (Thermal Evolution and Magnetic History of Rocky Planets) finds that bodies below ~0.5 M⊕ typically shut down their dynamos within 1–2 Gyr; h is well past that timescale. The remaining magnetic structure is crustal — fossilized magnetization from when h had a younger dynamo, now patchy after billions of years of impact gardening and thermal alteration. This is exactly the Mars situation today: ~1 μT crustal patches with no global dipole. Auroras therefore form not in organized polar ovals but in localized spots above magnetized terrain. RM22 (2203.01065) scaling returns a dipole moment of ~0.005 × Earth, effectively a residual signature rather than an active dynamo.

**Tidal heating note.** Makarov 2018 finds h capture probability into 3:2 spin-orbit = 0.017 (effectively zero); 1:1 lock is confirmed. The tidal dissipation peak is at Maxwell time ~0.20 d (close to the orbital period), giving 5.3×10¹³ W total — about 7×10⁻³ W/m² normalized. This is 1–2 orders of magnitude higher than the cfg's current 0.00001–0.0001 W/m², which may understate the actual flux.

## Visual styling

- **Global appearance.** Dark red-brown rocky world (`#3a2c20`)
  with patchy cream-white frost (`#c8b8a0`) increasing toward the
  terminator and nightside. Visual character somewhere between
  Mars (red-brown rocky) and a smaller Pluto (frost-dominated).
- **Substellar region.** Mostly bedrock; weathered iron-oxide
  brown. Impact craters visible at the cfg PQS resolution. Some
  frost in shadowed crater interiors.
- **Mid-zone.** Mixed bedrock and frost — fractal pattern of
  exposed dark brown over cream frost. Photogenic for KSP
  flyovers.
- **Terminator.** High contrast under grazing 2566 K light;
  topographic shadows reveal cratering and possible tectonic
  features. The frost-bedrock boundary is sharpest here.
- **Nightside.** Cream-white frost cover (`#c8b8a0`) with dark
  bedrock patches at ridge tops. KSP nightside ambient ≈ 1%
  dayside.
- **Atmosphere haze.** Imperceptible — the 0.005 bar atmosphere
  does not produce visible Rayleigh scattering. Limb is sharp.
- **Patchy Mars-style aurora.** Scattered `#4DFF4D` green and `#B19CD9` violet spots at low-to-mid magnetic latitudes — concentrated above magnetized crustal terrain rather than at the poles. Intensity ~30 kR, visible only against the dark nightside. The spotty pattern is the visual signature of h's frozen-core, crustal-anomaly-only magnetic environment.
- **Star in sky.** TRAPPIST-1 subtends 1.03° in h's sky (2× the
  Sun from Earth). Surface illumination 0.144 S⊕ — comparable to
  early-morning twilight on Earth. The red-orange star against the
  ochre-and-cream surface gives h a particularly atmospheric look
  despite the lack of actual atmosphere.
- **Sister planets in sky.** g (next inward) at angular size ~0.3°
  in inner conjunction. Conjunctions less frequent than for inner
  planets due to h's long period.

## Bibliography

### Read (visual-informative, drove decisions above)

- **1703.04166** Luger 2017 — Discovery / confirmation of h's
  orbital period via K2. Establishes h as the seventh planet in
  the resonant chain. Source for orbital parameters.
- **2112.05510** Gressier 2022 — HST WFC3/G141 transmission
  spectrum of h. Rejects cloud-free H₂-rich atmospheres. Only
  direct atmospheric observation of h to date.
- **1809.07498** Lincowski 2018 — Evolved climates of TRAPPIST-1
  worlds. h discussed as both snowball and as the "desiccated
  habitable" outlier. Drives the canonical-vs-variant scenario
  split. Already read for d/e/f/g.
- **2510.12794** Pearce 2025 — Born Dry or Born Wet? Compact
  multiplanet volatile accretion. Considers h's water budget under
  impact + escape evolution.
- **2504.19872** Castan-Lopez 2025 — Cosmic Shoreline Revisited.
  Places h close to the retention threshold; supports thin-atmo
  cfg choice.
- **1707.06927** Turbet 2017 — Climate diversity, tidal dynamics, volatile fate for TRAPPIST-1 planets. Specifies CO₂ equilibrium pressure (4 mbar at 145 K for h pure-CO₂) and demonstrates surface CO₂ ice burial under H₂O ice. **Drives the major surface composition revision (H₂O ice dominant, not CO₂ frost).**
- **1712.05641** Barr 2018 — Interior structures and tidal heating. h rock core 1030 km, maximum 100 km H₂O shell. Lowest density / CMF in the system after the inner trio.
- **1705.05535** Dong 2018 — Atmospheric escape from TRAPPIST-1 planets. h has lowest ion escape rate, atmospheric retention ~10¹⁰ yr. **Argues against the cosmic-shoreline-threshold framing**: ion-escape physics favors h retaining an atmosphere.
- **2207.04164** Krissansen-Totton 2022 — Coupled atmosphere-interior model. Predicts CO₂-dominated or CO₂-O₂ atmospheres for outer planets in virtually all simulations. Supports keeping a non-trivial atmosphere on h.
- **1803.07453** Makarov 2018 — Spin-orbital tidal dynamics. h capture probability into 3:2 = 0.017 → 1:1 lock confirmed.
- **1706.04617** Garraffo 2017 — Threatening Magnetic and Plasma Environment of TRAPPIST-1. Outer-planet magnetosphere context.
- **2203.01065** RM22 — Rocky-planet dynamo scaling; supports h's near-zero dipole moment.
- **2208.06523** Thermal Evolution and Magnetic History of Rocky Planets — confirms sub-Mars-mass planets shut down their dynamos within 1–2 Gyr.
- **1910.09871** Atri 2019 — Surface-dose tables for h.

### Read (context / methodology, not decision-driving)

- **2008.09599** Bourgeois 2024 — Magma ocean evolution for e/f/g
  (not h directly, but provides framework). Already read.
- **2508.12865** Empirical cosmic shoreline. Context.
- **2507.02136** 3D Cosmic Shoreline for Nurturing Atmospheres.
  Context.
- **2603.29743** New M Dwarf Cosmic Shoreline Constraints. Context.
- **1810.05210** Moran 2018 — HST haze limits, includes h.
  Already read.
- **1810.11255** Bolmont 2018 review — Constraining the environment
  and habitability of TRAPPIST-1. Direct quote: "TRAPPIST-1 h is
  unable to maintain surface liquid water. It cannot build up more
  than 10²–10³ ppm of CO₂, whatever the amount of background gas."
  Drives the revised N₂-dominated atmosphere composition with
  trace CO₂.
- **1708.09484** Bourrier 2017 — Temporal evolution of XUV and water
  content. h has the **smallest mass-loss** in the system: only
  0.37–0.43 EO_H over 8 Gyr with realistic photolysis-limited escape
  (ε_α = 0.2). The brief HZ-runaway phase (33–67 Myr) preserves
  most accreted water — but the 26Al desiccation argument
  (Lichtenberg 2019) puts the initial accretion budget low.
- **1902.04026** Lichtenberg 2019 — ²⁶Al desiccation of TRAPPIST-1
  precursor planetesimals. Argues the whole system formed with
  f_H₂O ≪ 15 wt%, possibly ≲ 1 wt%. Tightens h's water mass
  fraction toward the low end.
- **1909.13859** Gonzales 2019 — Reanalysis of TRAPPIST-1 fundamental
  parameters. Confirms field age (0.5–10 Gyr), consistent with
  Burgasser & Mamajek 2017's 7.6 ± 2.2 Gyr. No cfg change required.
- **2401.11815** Gillon 2024 — Comprehensive TRAPPIST-1 system review.
  Confirms h parameters; **corrects insolation from 0.16 to 0.144 ±
  0.006 S⊕**. Cites Childs 2023 formation modeling: outer five
  planets "required significant volatile content" while inner two
  are "nearly totally desiccated" — supports keeping non-trivial
  water content for h.
- **1702.07004** Bourrier 2017a — Lyman-α reconnaissance of
  TRAPPIST-1. XUV fluxes at h: F_X ≈ 34 erg/s/cm², F_EUV ≈ 12
  erg/s/cm², F_Lyα ≈ 13 erg/s/cm². Photoionization lifetime of
  neutral H at h's orbit: ~25 days (longer than h's orbital period
  — relevant to exosphere modeling, not visual).

### Read (instrument-only, not visual-informative)

(None specific to h.)

### Not read — no arXiv preprint or low-priority (~10 papers)

The h bibliography is moderately sized (53 papers, 43 with arXiv).
Most non-arXiv papers are catalog summaries or works that mention
h only in passing.

- **"Simulating Hydrospheres of TRAPPIST-1 h in Search of Liquid
  Water Layer"** (no arXiv) — *potentially important for the
  sub-glacial ocean question*. **Flagged for paste if accessible.**
- **"VizieR Online Data Catalog: TRAPPIST-1 h NIR spectrum
  (Gressier+, 2022)"** — data catalog, content already in 2112.05510.
  Skip.
- **"Characterizing Stellar Activity and Planetary Atmospheres in
  the TRAPPIST-1 System"** (no arXiv) — possibly relevant but skip
  unless atmosphere decision needs review.
- Various SETI / technosignature / catalog papers — irrelevant.

---

## Open items for follow-up

- The Lincowski 2018 "desiccated habitable h" scenario could be
  implemented as an alternative cfg variant — a thick CO₂/O₂
  atmosphere with a warm (~280 K) bare-rock surface. Visually
  distinctive: drier, dustier, with hazy yellow-cream skies.
- The "Simulating Hydrospheres of TRAPPIST-1 h" paper (no arXiv)
  could refine the sub-glacial ocean cfg if accessible.
- No JWST follow-up has been published for h as of 2026-05-21;
  any future emission or transmission spectrum should trigger a
  Phase 3 revisit.
- Cfg variant for "Pluto-like full frost" — minimal bedrock
  exposure, dominantly cream-white surface. Use if a cleaner
  outer-solar-system analog is desired.
- The water mass fraction (0.05–0.15) is poorly constrained;
  could be 0 (rocky-dry analogue) or up to 0.25 (Europa analog).
  Phase 2 should add more interior-structure measurements.
- The "desiccated habitable h" alternative scenario (Lincowski 2018) still stands as a cfg variant; the Dong 2018 / Krissansen-Totton 2022 retention-favoring arguments raise its prior somewhat. A 0.1 bar variant might be more realistic than the canonical 0.005 bar.
- Tidal heating `tidal_heating_w_m2` may be underestimated by 1–2 orders of magnitude per Makarov 2018 (~7×10⁻³ W/m² peak vs cfg's 0.00001–0.0001). Re-check against more recent Bolmont successors.
- The Mars-style patchy aurora geometry is a deliberate interesting-first choice. The alternative "uniform faint global glow" is preserved as cfg variant.
- Surface radiation dose ~4 Sv/yr places h in Kerbalism's "moderate" radiation bracket — better than e or f despite the thinner atmosphere, because h's distance reduces the stellar particle flux.
