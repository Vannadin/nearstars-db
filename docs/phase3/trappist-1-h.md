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
| `atmosphere_composition` | N₂ ~90%, trace CO₂ ≲1000 ppm, Ar / H₂O trace | low | Bolmont 2018 review caps p_CO₂ partial pressure at 100–1000 ppm regardless of background; surface CO₂ cold-trap dominates |
| `atmosphere_scale_height_km` | 6.0 | medium | derived: kT/μg with T≈140 K, μ=40, g=5.6 m/s² |
| `atmosphere_tint_rgb_hex` | `#302820` (essentially imperceptible Rayleigh) | low | very thin atmo, M-dwarf SED → negligible scattering |
| `cloud_cover_fraction` | 0.02 | low | minimal — sporadic CO₂ ice cirrus only |
| `cloud_tint_rgb_hex` | n/a | high | clouds too sparse for cfg-relevant tint |
| `ocean_present` | uncertain (sub-glacial possible if wmf at upper bound) | low | low mass + low temp → less basal melt than g; ocean if any is thin and Europa-like |
| `surface_ice_caps` | global CO₂/N₂ frost in cold zones, bedrock outcrop near substellar | medium | Mars-Pluto hybrid analog at lower insolation |
| `surface_tint_rgb_hex_primary` | `#3a2c20` (weathered iron-rich bedrock, dust + Mars analog) | medium | low-density rocky surface + photolytic oxidation over 7.6 Gyr |
| `surface_tint_rgb_hex_accent` | `#c8b8a0` (CO₂/N₂ frost patches + bright ice) | low | volatile-frost deposition in cold regions; Mars polar analog |
| `surface_morphology` | cratered ancient bedrock near substellar, patchy CO₂/N₂ ice frost toward terminator and nightside | medium | Mars/Mercury analog; very low resurfacing rate |
| `magnetic_field_present` | false (low mass + cold + slow rotation) | low | likely no active dynamo; small fossil field possible |
| `induction_heating_w_m2` | 0.001–0.01 | medium | Grayver 2022 — lowest in system due to distance + small mass |
| `tidal_heating_w_m2` | 0.00001–0.0001 | medium | Bolmont 2020 — negligible at h |
| `radiogenic_heat_w_m2` | 0.025 | medium | scaled by mass; slightly less than Earth-analog |
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

**Color choice.** Weathered iron-rich bedrock under M-dwarf
illumination: dark red-brown primary `#3a2c20` (Mars rust + lower
albedo from M-dwarf shift). Frost accents are cream-white
`#c8b8a0`.

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

For NearStars we adopt **0.005 bar (Mars-thin) N₂-dominated
atmosphere with trace CO₂**:

- **Pressure** 0.005 bar (500 Pa) — comparable to Mars (~600 Pa,
  variable). Above zero because some outgassing should accumulate
  on a 0.3 M⊕ planet; below 0.01 bar because cosmic-shoreline /
  Jeans-escape constraints suggest h cannot retain much more.
- **Composition** N₂-dominated (~90%), trace CO₂ (~0.1% = 1000 ppm).
  This is a revision from an earlier draft that had 70% CO₂. The
  driver is **Bolmont 2018 (1810.11255)** review, which finds that
  GCMs of h cannot accumulate more than 100–1000 ppm CO₂ regardless
  of N₂ background — surface cold-trapping removes CO₂ to nightside
  ice deposits faster than outgassing can replenish it. The
  remaining 10% is split among Ar, frost-cycle H₂O vapor, and
  fossil O₂.
- **Clouds.** Minimal (~2% global): rare CO₂ ice cirrus only,
  similar to Mars's mesospheric clouds.

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
