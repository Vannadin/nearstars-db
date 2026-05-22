<!-- TRAPPIST-1 f Phase 3 synthesis: cfg-ready decisions and reasoning -->
# TRAPPIST-1 f — Phase 3 Synthesis

TRAPPIST-1 f is a 1.04 R⊕, 1.04 M⊕ rocky planet on a 9.21-day orbit
around an M8V ultra-cool dwarf. Fifth planet out, receiving 0.38×
Earth's insolation — outside the conservative habitable zone, near
the maximum-greenhouse limit (Kopparapu 2013). Mass and radius are
the closest to Earth's in the entire system, but its bulk density
(4.92 g/cc from Agol 2021) is low enough that f is most likely a
significant water world: Acuña 2025 (2504.16201) infers a water mass
fraction of 16.2% ± 9.9%. The first NIRISS atmospheric reconnaissance
of f (Lim 2024, ADS bibcode 2024ESS.....510106L; no arXiv preprint
available) rejected cloud-free hydrogen-rich atmospheres but did
not strongly constrain secondary atmospheres.

**Scenario choice for NearStars: eye-ball aquaplanet with a 1 bar
CO₂-rich atmosphere and a substellar open-water lens extending to
~40° from the substellar point, surrounded by extensive glacial ice
elsewhere.** Per [[feedback-phase3-interesting-first]] the cfg
canonicalizes the more visually distinctive scenario among the
observation-consistent options. Wolf 2017 and Turbet 2018 both show
that f at 1 bar CO₂ sustains a substellar open-water disk — a
striking "eye-ball Earth" geometry — while at 0.1 bar CO₂ f collapses
to a complete snowball. The full-snowball reading remains
observation-consistent (Lim 2024 NIRISS only rejects H₂-rich
atmospheres) and is preserved as the conservative cfg variant.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 9.21 d orbit, tidal damping; Agol 2021 |
| `obliquity_deg` | 0 | high | tidal damping; Agol 2021 |
| `eccentricity` | 0.01007 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 8.81 | medium | Agol 2021 |
| `sidereal_period_days` | 9.2075 | high | Agol 2021 |
| `semi_major_axis_au` | 0.03849 | high | Agol 2021 |
| `mass_mearth` | 1.039 | high | Agol 2021 TTV |
| `radius_rearth` | 1.045 | high | Agol 2021 |
| `surface_gravity_g_earth` | 0.952 | high | derived = 1.039 / 1.045² |
| `density_g_cc` | 4.92 | high | Agol 2021 |
| `water_mass_fraction` | 0.04–0.16 | high | Acuña 2025 (2504.16201) reports 7-16% via MAGRATHEA; Acuña 2021 (2101.08172) Fe/Si-constrained scenario 2 gives 3.7 ± 2.6% — union of recent estimates broadens lower bound |
| `insolation_s_earth` | 0.38 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 215 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.5, snowball) | 188 | high | derived; high-albedo snowball case |
| `bond_albedo` | 0.30 | medium | eye-ball geometry: dark substellar ocean lowers global albedo vs. full snowball; Wolf 2017 1 bar branch |
| `surface_temp_substellar_k` | 260 | medium | Wolf 2017 + 0.1 bar CO₂ greenhouse → narrow open-water disk |
| `surface_temp_nightside_k` | 165 | medium | Wolf 2017 GCM; ice-covered cold nightside |
| `surface_temp_global_mean_k` | 220 | medium | Wolf 2017 GCM cold-snowball range |
| `atmosphere_present` | true (thin CO₂-rich) | medium | Lim 2024 rejects H₂-rich, permits thin CO₂; Wolf 2017 outer-HZ snowball case |
| `atmosphere_surface_pressure_pa` | 100 000 | medium | Tie-break (interesting-first): 1 bar CO₂ enables a substellar open-water lens (Wolf 2017); 0.1 bar conservative-snowball reading preserved as cfg variant |
| `atmosphere_composition` | CO₂ 95%, N₂ 4%, trace H₂O | medium | outgassing-driven; Wolf 2017 1 bar branch with saturated H₂O near substellar surface |
| `atmosphere_scale_height_km` | 5 | medium | derived: kT/μg with T≈230 K, μ=43 (CO₂-rich), g=9.3 m/s² |
| `atmosphere_tint_rgb_hex` | `#604040` (very thin CO₂ Rayleigh + dust haze) | low | minimal scattering at 0.1 bar; some CO₂ ice haze possible |
| `cloud_cover_fraction` | 0.25 | medium | Wolf 2017 — limited cloud formation in cold thin atmo |
| `cloud_tint_rgb_hex` | `#d8c8b8` (CO₂ ice + water ice mix, M-dwarf shifted) | medium | terminator + substellar cirrus |
| `ocean_present` | true (sub-glacial; small substellar open-water lens) | medium | Acuña 2025 wmf 16%; basal melting + greenhouse → marginal open water |
| `ocean_extent_substellar_radius_deg` | 40 | medium | Tie-break (interesting-first): 1 bar CO₂ variant chosen as canonical; Wolf 2017 / Turbet 2018 substellar eye-ball morphology with open-water disk to ~40° |
| `ocean_tint_rgb_hex` | `#1a1c30` (deep dark navy, mostly hidden under ice) | low | sub-glacial / small lens; minimally visible from orbit |
| `surface_ice_caps` | full coverage outside ~40° substellar open-water disk; ~60% of surface, with sea-ice transition ring at the disk boundary | medium | Wolf 2017 1 bar CO₂ branch; ice line at ~40° from substellar |
| `surface_tint_rgb_hex_primary` | `#e0d8d0` (clean snow / glacial ice) | medium | snow albedo + M-dwarf illumination |
| `surface_tint_rgb_hex_accent` | `#888070` (CO₂ frost stained with dust + exposed bedrock at ridge tops) | low | nightside CO₂ frost over ice; thin sublimation lag |
| `surface_morphology` | global glacial ice over frozen ocean; pressure-ridge terrain; visible bedrock at terminator ridges | medium | tidally-locked snowball; Wolf 2017 |
| `magnetic_field_present` | true (weak, ~0.05× Earth) | low | small mass + cold interior + slow rotation |
| `induction_heating_w_m2` | 0.001–0.005 | medium | Kislyakova 2017 (1710.08761) — total induction heating 1.1×10¹⁸ W ≈ 0.0012 W/m² normalized to f's surface; below molten-mantle threshold |
| `tidal_heating_w_m2` | 0.0–0.19 | medium | Barr 2018 (1712.05641) — Maxwell viscoelastic; F_tidal,f = 0.14 +0.05/-0.14 W/m², mantle T_eq 1621 K. Lower bound is 0 (uncertainty spans to zero). Current value is 30× higher than the previous Bolmont 2020-scaled estimate |
| `radiogenic_heat_w_m2` | 0.04 | medium | Earth-analog mantle radiogenics × 1 |
| `magnetic_field_strength_microtesla_equator` | 9 | low | RM22 (2203.01065) scaling; 1.04 M⊕ supports active dynamo but slow rotation (9.2 d) → multipolar regime, ~0.3× Earth |
| `magnetic_dipole_moment_normalized_earth` | 0.3 | medium | Garraffo 2017 (1706.04617) test case for f at 0.3 G; supports active dynamo |
| `magnetic_dipole_tilt_deg` | 12 | low | Tie-break: 12° offset gives distinctive auroral cap |
| `magnetosphere_standoff_planet_radii` | 3.5 | high | Garraffo 2017 Fig. 4 bottom panel — 3–4 R_p for f under super-Alfvénic conditions |
| `radiation_belt_present` | true | medium | B-field marginally sufficient; outer-planet stellar wind less crushing than for b/c |
| `surface_radiation_dose_msv_yr` | 7000 | high | Atri 2019 (1910.09871) for f at 0.037 AU + 1 bar shielding + B-field |
| `atmospheric_shielding_g_cm2` | 1000 | medium | Phase 3 cfg pressure 1 bar CO₂ → ~1000 g/cm² column |
| `aurora_present` | true | high | Atm + B-field; thinner-than-Earth CO₂-rich atmosphere gives Mars-analog aurora |
| `aurora_color_primary_hex` | `#FF6B6B` | medium | CO₂⁺ Fox–Duffendack–Barker bands red ~580–620 nm (Mars-analog); tie-break: red over UV-only since visible |
| `aurora_color_secondary_hex` | `#B19CD9` | medium | CO Cameron bands + CO₂⁺ ultraviolet doublet ~289 nm scattered to visible violet |
| `aurora_emission_species_primary` | `CO₂⁺ UV doublet 289 nm + CO Cameron bands + O 297.2 nm` | medium | MAVEN Mars-aurora analog |
| `aurora_oval_magnetic_latitude_deg` | 55 | medium | Vidotto 2013 with R_mp ~3.5 R_p → α ≈ 32°, oval lat ~58° |
| `aurora_intensity_kR_typical` | 80 | low | Fraschetti 2019 proton flux at f's distance |
| `star_apparent_angular_diameter_deg` | 1.65 | high | derived: 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## Surface synthesis

TRAPPIST-1 f sits at the outer edge of the conservative habitable
zone (Kopparapu 2014) and receives 38% of Earth's insolation. Without
significant greenhouse warming, the surface freezes globally (Wolf
2017 §5). With 0.1 bar CO₂, Wolf 2017 finds a tightly-confined
substellar open-water disk can be sustained — but the geometry is
fragile and depends on initial state (Pierrehumbert 2011 bifurcation
between aquaplanet and snowball states).

Acuña 2025 (2504.16201) provides the best current interior fit:
water mass fraction is 16.2% ± 9.9% if all interior parameters are
allowed to vary, or 6.9% ± 2.0% if the mantle-to-core ratio is fixed
at Earth-like. Either way, f is significantly more hydrated than
Earth — likely a true "ocean world" with a global liquid-water layer
underneath the global ice cover.

The Bourgeois 2024 (2008.09599) magma-ocean evolution work suggests
f experienced an extended (>100 Myr) magma ocean phase that produced
substantial atmospheric water and oxygen. Most water has since either
re-equilibrated into the mantle, been lost to space via photolytic
escape, or condensed onto the surface as the planet cooled. The
remaining ocean (now sub-glacial) and the thin CO₂ atmosphere are
the long-lived endpoint.

For the surface morphology, the tidally-locked snowball template
gives:

- **Substellar disk** (≲8° from substellar point): possible open
  water lens; otherwise thin ice with localized fractures. Surface
  T ≈ 260 K is the marginal case for ice/water equilibrium.
- **Glacial ice zone** (8–180° from substellar): thick (>1 km)
  glacial ice over a sub-glacial liquid-water ocean. Surface T
  drops monotonically from ~250 K at the ice line to ~170 K at the
  antistellar point.
- **Terminator** (~90° from substellar): cold (~190 K) and dark; the
  most photogenic zone, where pressure ridges throw long shadows
  under grazing 2566 K light. Possible bedrock exposure where
  glacial flow has thinned ice over crustal highs.

**Color choice.** Snow / glacial ice albedo is 0.6–0.8 (clean, fresh)
or 0.4–0.6 (dust-stained, aged). Under M-dwarf illumination the
perceived hue is warm cream (`#e0d8d0`) rather than blue-white.
CO₂ frost on the nightside contributes a slightly tan tint to dark
patches (`#888070`).

**Eye-ball aquaplanet by interesting-first.** Wolf 2017 explicitly
shows that f at 1 bar CO₂ supports a substellar open-water disk
extending to ~40° from the substellar point — a striking "eye-ball
Earth" morphology with a dark open-ocean pupil ringed by sea-ice
transition and glacial ice elsewhere. Turbet 2018 confirms f cannot
sustain open water below ~1 bar CO₂; the 0.1 bar reading gives a
complete snowball. Both are observation-consistent (Lim 2024 NIRISS
only rejects H₂-rich atmospheres). Per [[feedback-phase3-interesting-first]],
the cfg adopts the 1 bar lens variant as canonical — the eye-ball
morphology is dramatically more interesting visually than a uniform
ice ball, and is genuinely supported by Wolf 2017 and Turbet 2018
GCMs. The full-snowball variant is preserved in Open items for users
who want the conservative reading.

**Sub-glacial ocean architecture.** Acuña 2021 (2101.08172) details
the hydrosphere layering: surface ice Ih, then high-pressure ice
phases (II/III/V/VI) at increasing depth, transitioning to ice VII
at the base (~100 GPa). A thin liquid-water lens can exist between
ice Ih and the high-pressure ices, depending on geothermal flux —
this is the sub-glacial ocean that the cfg already adopts. Europa-like
layered hydrosphere is the closest Solar System analog.

**Photochemical haze / tholin layer.** Turbet 2018 §6 finds that f
sustains photochemical haze formation at its altitude. Over geological
timescales these settle as a faint tan/brown surface overlay biased
toward UV-exposed regions. The cfg's iron-oxide accent already captures
something similar, but the mechanism (UV photochemistry → tholin
deposition) is distinct from oxide formation — both can contribute
to the surface color.

**Iron oxide / bedrock.** Limited exposure — only at ridge tops near
the terminator where glacial flow has thinned ice. Iron oxide tint
is faint compared to the inner planets (b, c) due to limited stellar
UV at f's distance and the persistent ice cover protecting most of
the bedrock from photolytic oxidation.

**Morphology under tidal lock.** Ice circulation: surface heating at
the substellar point sublimates ice (low rate due to thin atmo); CO₂
+ trace H₂O are transported via atmospheric circulation to colder
zones (terminator, nightside) where they condense. Glacial flow then
returns ice toward the substellar disk. The result is a stable
ice circulation with a persistent thin open-water lens at the
substellar point.

## Atmosphere synthesis

The Lim 2024 NIRISS reconnaissance of f (no arXiv preprint, conference
abstract ADS bibcode 2024ESS.....510106L) reports the first JWST
transmission observation of f. The result: H₂-rich atmospheres are
rejected, consistent with Moran 2018 (1810.05210) HST limits, but
secondary atmospheres (CO₂, N₂, H₂O-rich) cannot be constrained from
the available transit baseline. This means the observational picture
for f is more open than for b, c, d, or e.

Theoretical modeling (Wolf 2017 §5, Lincowski 2018, Wunderlich 2020)
agrees that for f to be at all habitable / temperate, it needs
significant CO₂ greenhouse — Wolf 2017 finds 1 bar CO₂ is needed for
a fully open ocean, 0.1 bar gives a tight substellar disk, less
gives a complete snowball.

For NearStars we adopt **1 bar CO₂-rich atmosphere with substellar
open-water lens**:

- **Pressure** 1 bar (100 kPa). Wolf 2017 finds this is the threshold
  for sustained substellar open water; the conservative 0.1 bar
  choice produces full snowball.
- **Composition** CO₂-dominated (95%), N₂ (4%), trace H₂O (saturated
  near substellar surface). Outgassing-driven, with limited
  carbonate-silicate weathering due to mostly ice-covered surface.
- **Clouds.** Moderate (~30% global): water clouds over the
  substellar disk, occasional cirrus + CO₂ ice at terminator and
  high latitudes.

**Mars-analog aurora.** With both a 1 bar CO₂ atmosphere and a
non-trivial magnetic field (~0.3 × Earth, Garraffo 2017 test case),
f hosts Mars-analog auroras driven by stellar-wind precipitation.
The dominant emission is CO₂⁺ Fox–Duffendack–Barker bands at
580–620 nm (red-orange — the same chemistry that gives Mars's
discrete UV+visible aurora as seen by MAVEN), with secondary CO₂⁺
UV doublet and CO Cameron bands scattered into perceived violet.
The auroral oval centers at ~55° magnetic latitude under typical
stellar wind conditions; intensity ~80 kR (~8× Earth's typical).
For cfg rendering: primary `#FF6B6B` red along the auroral oval,
`#B19CD9` violet accent. Interesting-first tie-break: chose
red+violet visible palette over UV-dominant rendering (which would
not show in player view).

**CO₂ cold-trap geometry.** Turbet 2018 finds that f's CO₂ ice deposits
form preferentially in two symmetric cold traps at longitude -120°,
latitude ±80°, at 30–50 km altitude. This is a visual annotation for
the cfg: nightside CO₂ ice clouds (the small fraction predicted at
0.1 bar pressure) are concentrated in these polar cold-trap regions,
not uniformly distributed.

**Sky appearance.** The 0.1 bar CO₂ atmosphere has Rayleigh
scattering ~5% of Earth's, with the M-dwarf SED further depressing
short-wavelength contribution. The sky near substellar is faintly
dark-rust (`#604040`) with the star dominant; near terminator the
sky is dark with faint cyan-white at the limb from CO₂ ice cloud
forward-scattering.

## Rotation & spin synthesis

Tidal damping for f at 9.21-day period over 7.6 Gyr establishes the
synchronous (1:1) configuration. Obliquity damped to zero.
Eccentricity is 0.01007 — at the upper edge where 3:2 spin-orbit
becomes marginally stable (Vinson 2017), but 1:1 remains the
overwhelming-probability state.

**KSP implementation note.** Rotation period = orbital period =
9.2075 days (795 528 s).

**No seasons.** Obliquity = 0; libration-induced insolation variation
~ 1% (slightly higher than inner planets due to higher e). The
substellar point is essentially fixed.

**Magnetic dynamo expectation.** f's Earth-mass core supports an
active dynamo (Driscoll & Olson scaling in 2208.06523 finds
Earth-mass dynamos extend lifetime via core solidification timing).
The 9.2-day tidally-locked rotation reduces dipole strength via
slow-rotation Reiners scaling (~0.3 × Earth dipole), but a coherent
dipole remains supportable. Garraffo 2017 explicitly adopts f as
the representative habitable-zone case with 0.3 G surface field;
the cfg matches this assumption.

## Visual styling

- **Global appearance.** From orbit, f looks like a dark navy "pupil"
  (substellar open ocean, `#1a1c30`) within a fractal sea-ice
  transition zone, ringed by extensive glacial ice cover (`#e0d8d0`)
  over the rest of the planet. Persistent water clouds over the
  substellar disk give a warm cream "cataract" around the pupil.
  The auroral oval `#FF6B6B` red band crosses the nightside near
  magnetic latitude ~55°, visible in shadow against the dark ice.
- **Substellar disk (open water).** Small dark patch ~16° wide
  (8° radius). Contrast against the surrounding warm-cream ice is
  dramatic.
- **Glacial ice.** Vast majority of visible surface. Smooth at large
  scale, with pressure ridges and crevasses visible at the
  terminator under grazing light. Subtle color variations between
  fresh snow (`#e0d8d0`) and dust-stained / refrozen ice (`#c8c0b0`).
- **Terminator band.** High topographic contrast in oblique light.
  Possible bedrock exposure at ridge tops (`#888070` accent).
- **Nightside.** Dark cream-tan from CO₂ frost. KSP nightside ambient
  ≈ 2–5% dayside.
- **Atmosphere haze.** Very thin warm gray-red limb glow (`#604040`),
  5–10 km thick, only visible against space at the planet's limb.
- **Star in sky.** TRAPPIST-1 subtends 1.65° in f's sky (3× the Sun
  from Earth) — appears as a deep red-orange disk. Surface
  illumination is 0.38 S⊕, similar to deep-Earth twilight; the
  star's dim red light gives the snowscape a permanent dawn-tint.
- **Sister planets in sky.** e (next inward) at angular size ~0.3°
  in inferior conjunction; g (next outward) at ~0.3° during outer
  conjunctions. Conjunctions every ~25 days (f-g synodic period).

## Bibliography

### Read (visual-informative, drove decisions above)

- **2504.16201** Acuña 2025 — Internal structure of f via
  MAGRATHEA. wmf 16.2% ± 9.9% (free CMF) or 6.9% ± 2.0% (Earth-like
  mantle-to-core). Establishes f as an ocean world. Drives the
  sub-glacial ocean cfg.
- **2008.09599** Bourgeois 2024 — Magma ocean evolution for e/f/g.
  Predicts f has retained substantial water through evolution.
- **2006.11349** Wunderlich 2020 — Wet vs. dry e and f atmospheres.
  Constrains f's atmosphere to CO₂-rich (snowball branch) or to a
  dry desiccated post-runaway state.
- **1809.07498** Lincowski 2018 — Evolved climates of TRAPPIST-1
  worlds. f is one of the planets where Lincowski's modeling shows
  cold, CO₂-rich atmospheres are the equilibrium. Already read for
  d Phase 3 / e Phase 3.
- **1712.05641** Barr 2018 — Interior structures and tidal heating
  in TRAPPIST-1 planets. Drives the upward revision of f's tidal
  heat flux to 0.14 W/m² (30× higher than previous estimate).
  Maxwell viscoelastic; mantle T_eq 1621 K.
- **2101.08172** Acuña 2021 — Hydrosphere characterization. Details
  f's sub-glacial ocean architecture (ice Ih / high-pressure ices /
  ice VII). WMF 3.7 ± 2.6% scenario 2, broadening the lower bound
  on water content.
- **1707.06927** Turbet 2018 — Modeling climate diversity for
  TRAPPIST-1. **Drives the snowball default**: at 0.1 bar CO₂, f is
  fully ice-covered (no substellar lens). Open ocean emerges only at
  ≥1 bar CO₂. Also identifies the polar CO₂ cold-trap geometry.
- **1710.08761** Kislyakova 2017 — Induction heating estimates. f
  total ~1.1×10¹⁸ W; revises the cfg's induction heating downward.
- **1911.08596** Fauchez 2019 — Cloud and haze modeling for HZ
  TRAPPIST-1 planets. Confirms f's snowball state at all plausible
  CO₂ pressures ≤10 bar.
- **1706.04617** Garraffo 2017 — Threatening Magnetic and Plasma
  Environment of TRAPPIST-1. Adopts f as habitable-zone
  representative; 0.3 G test case drives the cfg's dipole moment.
- **2203.01065** RM22 — Rocky planet magnetic moment scaling.
- **1910.09871** Atri 2019 — Surface-dose tables for f.

### Read (context / methodology, not decision-driving)

- **2605.06964** Energy balance model for TRAPPIST-1 climates.
  Methodology paper; supports the snowball state for f.
- **2506.21351** SEPHI 2.0 habitability index. Catalog context only.
- **2502.00132** Way 2025 — d-focused but useful methodology
  reference for tidally-locked GCMs that apply to f.
- **1810.05210** Moran 2018 — HST haze limits. Already read for d
  Phase 3.

### Read (instrument-only, not visual-informative)

(None specific to f at this depth.)

### Not read — no arXiv preprint or low-priority (~9 papers)

The f bibliography is very small (15 papers, 6 with arXiv).

- **2024ESS.....510106L** Lim 2024 — TRAPPIST-1 f NIRISS atmospheric
  reconnaissance. **Key observational paper for f, but no arXiv
  preprint available.** ADS abstract only. The atmosphere
  inference (H₂-rich rejected, secondary atmospheres unconstrained)
  is sourced from the abstract. **Flagged for fetch when arXiv
  preprint appears.**
- **2025arXiv...** various conference summaries on biosignature
  feasibility and ELT characterization. Skip.

---

## Open items for follow-up

- Re-fetch the Lim 2024 NIRISS f paper when an arXiv preprint
  becomes available; the formal published version may tighten the
  secondary-atmosphere constraints.
- The 0.1 bar CO₂ choice is bracketed by Wolf 2017's modeling but is
  not directly constrained by f-specific observations. If future
  JWST emission spectroscopy of f reveals a colder dayside than
  current models predict, the CO₂ pressure should be reduced (or
  set to zero — full snowball).
- Cfg variant for the "complete snowball" (no substellar open water)
  interpretation — visually simpler, fully white-cream world. Use
  if the substellar lens is found to be too marginal to render
  meaningfully in KSP.
- Cfg variant for the "1 bar CO₂ + full ocean" interpretation
  (Wolf 2017 §5 best-case): visually similar to e but cooler and
  more ice-banded. Use if a deeper habitable-zone alternative is
  desired.
- The water mass fraction (7–16%) is high enough that f could
  plausibly host a sub-glacial liquid-water layer comparable to
  Europa's — possibly with hydrothermal activity if any tidal /
  radiogenic heating reaches the seafloor. Not directly visual
  but worth a Principia annotation.
- The choice between snowball default (0.1 bar CO₂) and 1 bar CO₂ +
  substellar open-water lens variant is a cfg gameplay-vs-fidelity
  trade. Default snowball matches Turbet 2018 most directly; the
  warmer variant preserves the more visually distinctive "eyeball"
  rendering.
- **Cfg variant: full snowball at 0.1 bar CO₂.** Preserved per the
  interesting-first tie-break rule. Users who want the conservative
  observational reading (no substellar open water) can render this
  variant. All Decisions-table values change appropriately (pressure
  → 10 kPa, surface temperature → 220 K global mean, ocean →
  sub-glacial only).
- Magnetic field strength is scaling-based; could be refined if a
  TRAPPIST-1-specific dynamo model becomes available.
