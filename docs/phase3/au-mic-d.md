<!-- AU Mic d Phase 3 synthesis: cfg-ready decisions and reasoning -->
# AU Mic d — Phase 3 Synthesis

AU Microscopii d is a 1.053 ± 0.511 M⊕ Earth-mass planet candidate on
a 12.74-day orbit around the 22-Myr-old M1Ve flare star AU Mic.
Discovered via transit-timing variation analysis by Wittrock et al.
2023 (AJ 166, 232; `2023AJ....166..232W`, arXiv:2310.10719) from a
combined TESS + ground-based transit dataset of the previously known
planets b and c, d does not itself transit (no direct radius
measurement); its orbital period and mass come from the gravitational
perturbations it imprints on b and c's transit times. Independent
ESPRESSO RV reanalysis by Mallorquin et al. 2024
(`2024A&A...689A.132M`) finds the d signal at marginal RV significance,
consistent with the TTV-derived mass. The radius listed in the NASA
Exoplanet Archive (1.02 R⊕) is a placeholder from a mass-radius
relation rather than a measurement.

Because d does not transit, its bulk density, atmosphere, and surface
properties are inferred rather than measured. The mass uncertainty
(± 0.511 M⊕, nearly 50%) is large. Insolation at 0.105 AU around
0.102 L☉ is ~9.3 × Earth's — well inside any reasonable habitable-zone
boundary, with equilibrium temperature ~440 K assuming Earth-analog
albedo. d orbits inside the snow line and inside the resolved debris
disk (35–210 AU); it is one of three small inner planets (with b and c)
bathed in AU Mic's super-flare bombardment.

**Scenario choice for NearStars: a tidally-locked Earth-mass rocky
planet with a thin secondary atmosphere (~10⁴ Pa, CO₂-dominated)
outgassed from active volcanism, basaltic surface with iron-oxide
reddening on the dayside, partial cooling-lava features near the
substellar point, and a globally hot terminator-to-nightside heat
distribution. Scenario chosen as a documented divergence: the
canonical interpretation under AU Mic's XUV bombardment is airless
(rapid atmospheric stripping over 22 Myr); the cfg picks the
volcanically-replenished thin-atmosphere reading because outgassing
in a young, tidally heated, possibly magma-ocean-residual planet
provides a plausible replenishment source — and the atmospheric
visual presence is the cfg's most distinctive feature.** 27 cfg picks;
22 canonical-aligned, 3 tie-break, 2 documented divergences
(atmosphere_present, ocean_present).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 12.74 d orbit; tidal damping ≪ 22 Myr age for Earth-mass planet at 0.105 AU around 0.51 M☉ |
| `obliquity_deg` | 0 | high | tidal damping |
| `eccentricity` | 0.00305 | high | Wittrock 2023 TTV fit |
| `argument_of_periastron_deg` | 160.79 | medium | Wittrock 2023 TTV fit (low-e → weak constraint) |
| `sidereal_period_days` | 12.73596 | high | Wittrock 2023 TTV fit; consistent with Mallorquin 2024 RV |
| `semi_major_axis_au` | 0.105 | medium | Wittrock 2023 reported value |
| `inclination_deg` | 89.32 | medium | Wittrock 2023 TTV fit (consistent with edge-on but no transit observed) |
| `mass_mearth` | 1.053 ± 0.511 | medium | Wittrock 2023 N-body + TTV dynamical fit |
| `radius_rearth` | 1.02 | low | Tie-break: no transit detected; NEA placeholder from mass-radius relation (Chen & Kipping 2017 probabilistic relation); cfg picks 1.02 for visual recognition as an Earth-analog rocky planet |
| `surface_gravity_g_earth` | 1.01 | low | derived = 1.053 / 1.02²; downstream of radius assumption |
| `density_g_cc` | 5.45 | low | derived; consistent with Earth-analog rocky composition |
| `insolation_s_earth` | 9.3 | high | derived from L = 0.102 L☉ (Donati 2023, recommended) and a = 0.105 AU |
| `equilibrium_temp_k` (A=0) | 478 | high | derived |
| `equilibrium_temp_k` (A=0.1) | 466 | high | derived; modest dark-basalt albedo |
| `bond_albedo` | 0.10 | medium | dark basaltic surface with partial dust covering; M-dwarf SED reduces effective albedo |
| `dayside_surface_temp_k` | 530 | medium | thin atmosphere → limited day-night redistribution; dayside slightly above T_eq. Estimated from the day-night heat-recirculation (+ internal-heat) parameterization of Cowan & Agol 2011 (`1001.0012`) in the weak-recirculation limit |
| `nightside_surface_temp_k` | 250 | medium | weak atmosphere transport; thermal inertia of basaltic surface. Estimated from the Cowan & Agol 2011 (`1001.0012`) heat-recirculation (+ internal-heat) parameterization |
| `atmosphere_present` | true (thin secondary CO₂) | medium | Documented divergence: see Canonical alternatives. Outgassing from active interior (Driscoll & Barnes 2015 tidal-heating-driven volcanism scaling for young rocky planets) replenishes a thin secondary atmosphere despite AU Mic XUV bombardment |
| `atmosphere_surface_pressure_pa` | 10000 | medium | Documented divergence: see Canonical alternatives. ~0.1 bar CO₂ from outgassing balance vs. escape; conservative variant is 0 (airless) |
| `atmosphere_composition` | CO₂ ~85%, N₂ ~10%, SO₂ ~3%, H₂O trace; outgassing-replenished | medium | volcanic-outgassing composition under reducing-to-oxidizing transition; trace SO₂ from volcanic plumes |
| `atmosphere_scale_height_km` | 8.7 | medium | derived: kT/μg with T = 450 K, μ = 43 (CO₂), g = 9.9 m/s² |
| `atmosphere_tint_rgb_hex` | `#704030` | low | Tie-break: interesting-first. Thin CO₂ + volcanic dust under M1V red illumination → muted red-brown haze, distinctive from b/c's H/He bands |
| `cloud_cover_fraction` | 0.20 | medium | thin atmosphere → limited cloud formation; sparse SO₂ aerosol haze near volcanic regions |
| `cloud_morphology` | sparse cumulus / SO₂ haze patches near volcanic regions; mostly clear elsewhere | low | Tie-break: distinctive over generic; SO₂ plumes localized to active volcanic provinces |
| `cloud_tint_rgb_hex` | `#a08070` | low | Tie-break: warm cream of SO₂ haze under M-dwarf SED |
| `ocean_present` | false (sub-glacial possible on cold nightside; visible surface is dry) | medium | Documented divergence: see Canonical alternatives. Surface temperature regime (530 K dayside, 250 K nightside) plus thin atmosphere precludes stable surface liquid water; cold-trap ice possible on far-side hemispheres |
| `surface_tint_rgb_hex_primary` | `#5a4030` | medium | dark basaltic surface under M1V illumination; iron-oxide reddening from photochemical alteration |
| `surface_tint_rgb_hex_accent` | `#a04020` | low | Tidal heating on a very young (~22 Myr) close-in planet can drive Io-analog volcanism (Driscoll & Barnes 2015); localized cooling-lava hotspots are a low-confidence possibility, NOT insolation melt (T_eq 478 K is below the silicate solidus) |
| `surface_morphology` | dark basaltic plains with iron-oxide reddening; localized cooling-lava patches at substellar; nightside cold-trap with surface ice + frost lag | medium | tidally-heated young rocky planet (Driscoll & Barnes 2015 framework); volcanic resurfacing on Myr timescales |
| `surface_ice_caps` | nightside frost cap at hemispheric anti-substellar position; sublimation-driven volatile cycle | medium | tidally-locked terminator condensation; thin atmosphere allows volatile transport day to night |
| `magnetic_field_present` | true (weak) | low | Earth-mass rocky planet with active interior; dynamo possible despite slow rotation |
| `magnetic_field_strength_microtesla_equator` | 5 | low | Earth-mass rocky planet → **rocky** dynamo scaling RM22 (Rodríguez-Mozos & Moya 2022, `2203.01065`, cached) + slow-rotation penalty (Garraffo 2017): a weak field despite an active young core. (Replaces a citation to Reiners & Christensen 2010, which is a giant/brown-dwarf dynamo paper inapplicable to a rocky planet.) |
| `surface_radiation_dose_msv_yr` | 5000 | medium | thin atmospheric column (~100 g/cm²) + weak magnetic field → high surface dose under AU Mic super-flares; Atri 2019 framework |
| `aurora_present` | true | medium | thin atmosphere + weak B-field + intense stellar wind → visible aurora; Mars-analog CO₂⁺ emission |
| `aurora_color_primary_hex` | `#ff6b6b` | medium | CO₂⁺ Fox–Duffendack–Barker bands red ~580–620 nm; Mars-analog visible aurora |
| `aurora_emission_species_primary` | CO₂⁺ doublet + CO Cameron bands + O 297.2 nm | medium | thin CO₂ atmosphere chemistry; MAVEN Mars-aurora analog |
| `star_apparent_angular_diameter_deg` | 4.4 | high | derived: 2 × 0.862 R☉ / 0.105 AU × (180/π) ≈ 4.4° |
| `stellar_illumination_color_temp_k` | 3665 | high | from host star Teff |

## Surface synthesis

AU Mic d is the most observationally uncertain of the AU Mic system's
four planets. Without a transit, the radius is not measured; the NASA
Exoplanet Archive's listed 1.02 R⊕ is a placeholder from a mass-radius
relation (Chen & Kipping 2017 probabilistic scaling), not an
independent measurement. The cfg adopts this placeholder because (a)
it is consistent with the Wittrock 2023 N-body-derived mass under an
Earth-analog density assumption, and (b) the alternative (a smaller
rocky planet at higher density, or a slightly larger sub-Neptune at
lower density) would be no better constrained.

For NearStars purposes, d is therefore modeled as an Earth-analog rocky
planet with density 5.45 g/cc and surface gravity 1.01 g_Earth — a
plausible reading within the observational window. The surface is
basaltic with iron-oxide reddening; the dark primary tone (`#5a4030`)
reflects the M1V illumination + ferric mineral reddening common to
weathered basalts under reducing atmospheric chemistry. The accent
tone (`#a04020`) represents localized cooling-lava hotspots near the
substellar point — a low-confidence possibility driven by tidal
heating on this very young (~22 Myr) close-in planet (Driscoll &
Barnes 2015), not by insolation melt (T_eq 478 K sits below the
silicate solidus).

**Surface morphology under tidal lock.** With 1:1 spin-orbit
synchronization, the substellar hemisphere remains permanently
illuminated (530 K equilibrium) and the anti-substellar hemisphere
remains permanently dark (250 K). Atmospheric heat transport is
weak (thin atmosphere), so the temperature gradient across the
terminator is steep — perhaps 50–80 K over ~1000 km. This drives:

- **Substellar lava province.** Tidal heating + radiogenic heating
  + persistent stellar illumination keeps the substellar hemisphere
  warm enough for sustained volcanic activity. Cooling-lava patches
  are visible at 1000–1500 K (red-yellow glow) within active
  provinces; surrounding basaltic plains are at 530 K (dark).
- **Mid-latitude weathered basalt.** The terminator zone (between
  substellar lava province and nightside cold trap) hosts weathered
  basaltic plains with photochemical iron-oxide reddening — the
  primary surface tint at `#5a4030`.
- **Nightside cold trap.** Anti-substellar hemisphere accumulates
  frost from atmospheric transport — CO₂, SO₂, and trace H₂O
  condense. Surface ice caps are localized to the anti-substellar
  point; thin frost extends ~30° outward.

**Mineralogy.** Driven by AU Mic's intense XUV flux, the upper-mm
of the surface undergoes photochemical alteration: Fe²⁺-bearing
silicates oxidize to Fe³⁺ on Gyr timescales, but at 22 Myr the
process is only partially complete. The result is a surface with
fresh dark basalt + partial weathered iron-oxide reddening — exactly
the regolith reading the cfg adopts.

The youth of the system means **active resurfacing is plausible**.
Driscoll & Barnes 2015 framework for tidal-heating-driven volcanism on
young rocky planets gives a tidal heat flux of ~0.1–1 W/m² for d at
e = 0.003 — roughly equal to or slightly above Io's flux of 2 W/m².
This is sufficient to drive episodic volcanism that resurfaces
substantial fractions of the planet on Myr timescales. The cfg's
substellar lava province + atmospheric SO₂ haze are the visible
consequences.

## Atmosphere synthesis

The atmosphere of d is the cfg's most consequential pick — and the
one most exposed to revision. The dominant question is whether AU
Mic's super-flare bombardment over 22 Myr has stripped any primary
H/He envelope (highly likely, given d's small mass and AU Mic's
saturated XUV regime), and whether a thin secondary atmosphere
sustained by outgassing is currently present.

**Documented divergence.** The canonical reading from XUV escape
arguments (Owen & Wu 2017; Cohen 2024 system-level MHD; Tristan
2023 super-flare census; Atri 2019 surface dose calculations) is that
d should be airless: the rate of atmospheric stripping at d's
insolation under AU Mic's XUV exceeds the rate of outgassing
replenishment for Earth-mass volcanically-quiescent planets. The
cfg picks differently — adopting a thin secondary atmosphere at
~10⁴ Pa (0.1 bar) — because (a) AU Mic's young age makes d's
interior thermally active (tidal + radiogenic + residual accretion
heat), (b) Driscoll & Barnes 2015 framework supports active outgassing
on Myr timescales, and (c) the atmosphere-present cfg provides a more
visually distinctive presentation than a bare-rock airless analogue.
The canonical airless reading is preserved as a cfg variant in Open
items and listed in `## Canonical alternatives`.

**Pressure.** The cfg adopts ~10⁴ Pa (0.1 bar). At this pressure,
visual atmospheric effects (Rayleigh scattering near the limb,
sunset color, faint cloud cover) are present but subtle — closer to
Mars's atmosphere than Earth's. The escape rate at this pressure
balances against outgassing on Gyr timescales.

**Composition.** Volcanic outgassing of a relatively young rocky
planet produces CO₂-dominated atmospheres (analog: early Earth, early
Mars). The cfg composition (CO₂ ~85%, N₂ ~10%, SO₂ ~3%) reflects this
canonical volcanic outgassing template, with SO₂ as a marker of active
plume activity. H₂O is at trace levels — most water is either locked
in interior reservoirs or has been photodissociated + lost (H
escapes, O retained or oxidizes surface minerals).

**Sky appearance.** Under a thin CO₂ atmosphere at d, the daytime
sky is a dim red-orange — Rayleigh scattering is minimal at 0.1 bar,
so the sky is mostly dark even on the dayside, with the star's
direct glare and a faint dust-reddened haze. Looking horizontally
through the atmosphere yields a deeper red-brown band — sunset
geometry persists across the whole dayside. SO₂ aerosols from
volcanic plumes give localized atmospheric haze patches with a warm
cream tint (`#a08070`). The nightside sky is dark with no
illumination except for sister-planet conjunctions and starlight.

**Atmospheric retention.** Atri 2019 framework for surface dose
under stellar proton events suggests that d's atmosphere — even at
0.1 bar — provides limited radiation shielding (~100 g/cm² column,
vs. Earth's 1030 g/cm²). Super-flare events (Tristan 2023; Cully
1993) periodically strip the upper atmosphere; outgassing replenishes
on timescales of years to decades. The cfg renders this as a faint
upper-atmosphere glow during super-flare events — visible as a brief
enhancement of the limb haze.

## Rotation & spin synthesis

Tidal damping of an Earth-mass planet at 0.105 AU around 0.51 M☉
proceeds on a timescale of ~10⁵ years for rocky-planet Q ≈ 100
(Goldreich & Soter 1966) — far shorter than the 22-Myr system age.
d is fully locked into 1:1 spin-orbit synchronization. Eccentricity
0.003 (Wittrock 2023) is too low to support 3:2 spin-orbit
(Vinson 2017 threshold ~0.01); 1:1 is unambiguous.

**KSP implementation note.** Rotation period = orbital period =
12.73596 days (1 100 234 s). Kopernicus `rotationPeriod` should
match the orbital `period`.

**No seasons.** Obliquity damped to zero. Eccentricity-induced
insolation variation is ≲ 1% — negligible. Substellar and
anti-substellar hemispheres are stable on geological timescales.

**Day-night thermal contrast.** With thin atmosphere (10⁴ Pa CO₂),
day-night redistribution is weak. Expected contrast: 280 K (dayside
530 K, nightside 250 K). The substellar point is permanently at
~530 K, the terminator at ~390 K, and the anti-substellar point at
~250 K. These temperatures support the cfg's surface morphology:
substellar lava province, weathered terminator basalt, nightside
frost cap.

**Slow rotation effects.** With a 12.74-day rotation period,
Coriolis effects are weaker than Earth's by an order of magnitude.
Atmospheric circulation is dominated by direct day-to-night thermal
forcing (Sergeev 2020 substellar convection framework) rather than
zonal jets. Substellar convective cluster + nightside frost
condensation form the dominant atmospheric pattern.

## Visual styling

The visual presentation of AU Mic d is a tidally-locked rocky world
with a thin atmosphere — distinct from b/c's gas-giant disks:

- **Global appearance.** A dark basaltic disk with iron-oxide
  reddening and a bright substellar lava province, lit by AU Mic
  at 4.4° angular diameter (8× the Sun from Earth). The dayside
  hemisphere shows the characteristic "eyeball" geometry of a
  tidally-locked rocky planet with an active substellar zone; the
  substellar lava province is the brightest feature, glowing
  red-yellow at 1000–1500 K — visible from orbit as a bright
  patch ~30° in diameter.
- **Substellar lava province.** Active cooling-lava patches at
  1000–1500 K (red-yellow glow) within a roughly circular substellar
  region of ~30° radius. Surrounding basaltic plains (530 K) are
  dark (`#5a4030` primary tint). The contrast between glowing lava
  and dark basalt is the cfg's most visually striking surface feature.
- **Terminator weathered basalt.** Between substellar lava and
  nightside frost, the terminator zone shows weathered basaltic
  plains with iron-oxide reddening. Surface tint `#5a4030` primary
  with `#a04020` accent at active volcanic patches. Long shadows at
  oblique illumination reveal subtle topographic relief.
- **Nightside frost cap.** Anti-substellar hemisphere accumulates
  frost (CO₂, SO₂, trace H₂O) as the atmosphere transports volatiles
  to the cold trap. Visible as a localized bright patch (~30°
  diameter) centered on the anti-substellar point, surrounded by
  thin frost extending ~30° outward. Frost reflects starlight,
  making the nightside cold trap dimly visible.
- **Atmospheric haze.** Pale red-brown limb glow (`#704030`) about
  10–15 km thick — Rayleigh-scattered M-dwarf light + volcanic dust
  + SO₂ aerosol. Localized SO₂ plumes near active volcanic regions
  appear as warm cream patches (`#a08070`) drifting on slow zonal
  winds.
- **Auroras during super-flares.** Mars-analog visible aurora
  (`#ff6b6b` primary, CO₂⁺ Fox–Duffendack–Barker bands at 580–620 nm)
  appears during AU Mic super-flare events. Localized to the
  weak-magnetic-field poles; the auroral oval is at low magnetic
  latitude (~40°) because of the weak field. Visible from much of
  the nightside hemisphere during flare events; only at high
  magnetic latitude during quiescence.
- **Star in sky.** AU Mic subtends 4.4° in d's sky (8× the Sun from
  Earth) — a vast deep-red disk dominating the daytime sky. Surface
  illumination 9.3× Earth's at substellar but red-shifted into the
  near-IR; the visible-light brightness is comparable to Earth's
  noon sun. Super-flares brighten by 1–3 magnitudes for tens of
  minutes — visible as transient brightening of the substellar lava
  province.
- **Sister planets.** b (innermost, puffy Neptune) at conjunction
  appears as a moderate dot ~0.3° in diameter; c (middle, sub-Neptune)
  smaller but still visible; e (outermost if confirmed) faint. The
  edge-on debris disk at 35–210 AU is visible as a thin bright
  streak on either side of AU Mic.

## Canonical alternatives

### Diverged cfg picks

| Field | Gameplay (in cfg) | Canonical alternative | Why diverged |
|---|---|---|---|
| `atmosphere_present` | true (thin CO₂ ~0.1 bar; outgassing-replenished) | false (airless under AU Mic XUV bombardment) | Canonical interpretation under Owen & Wu 2017 photoevaporation + Cohen 2024 system-level MHD + Tristan 2023 super-flare census is that Earth-mass d cannot retain a primary H/He envelope or a vapor-thin secondary atmosphere against AU Mic's XUV flux at 0.105 AU. The cfg picks the volcanically-replenished thin-atmosphere reading because (a) d's young age + tidal heating support active outgassing (Driscoll & Barnes 2015), (b) the atmosphere-present visualization is meaningfully more interesting than a bare-rock airless analogue. The canonical airless variant is preserved in Open items as a cfg fallback. |
| `atmosphere_surface_pressure_pa` | 10000 (0.1 bar CO₂) | 0 (vacuum) | Downstream of atmosphere_present choice. Conservative variant ships pressure = 0 with all atmospheric visual layers disabled. |
| `ocean_present` | false (visible surface dry; nightside cold trap accumulates ice/frost) | false (airless variant has no surface volatiles either) | The two variants converge on "no liquid surface water" but differ on whether nightside ice exists. Cfg keeps nightside ice in the atmosphere-present scenario; airless variant has no nightside ice (no atmosphere to transport volatiles). |

## Bibliography

### Read (visual-informative, drove decisions above)

- **Wittrock J. M. et al. 2023** — *Transit Timing Variation Measurements and Dynamical Mass Determination of the AU Mic System*, AJ 166, 232 (`2023AJ....166..232W`, arXiv:2310.10719). N-body + TTV dynamical mass; introduces d as a TTV-only candidate at 12.74 d, mass 1.053 ± 0.511 M⊕. **Cornerstone discovery paper.**
- **Mallorquin M. et al. 2024** — *AU Mic system characterized with ESPRESSO*, A&A 689, A132 (`2024A&A...689A.132M`). ESPRESSO RV reanalysis recovers the d signal at marginal significance; confirms TTV-derived parameters within uncertainty.
- **Driscoll P. E. & Barnes R. 2015** — *Tidal Heating of Earth-like Exoplanets around M Stars*, Astrobiology 15, 739 (`2015AsBio..15..739D`, arXiv:1506.08077). Framework for tidal-heating-driven volcanism on young rocky planets at M-dwarf habitable zones. Adopted for d's surface volcanism + atmosphere-replenishment argument.
- **Owen J. E. & Wu Y. 2017** — *The Evaporation Valley in the Kepler Planets*, ApJ 847, 29 (`2017ApJ...847...29O`, arXiv:1705.10810). Photoevaporation framework; canonical argument that small planets at d's insolation under M-dwarf XUV strip atmospheres on Myr timescales. The cfg's documented divergence is against this reading.
- **Tristan I. I. et al. 2023** — *Catching the Flares of the AU Mic System with TESS*, ApJ 951, 33 (`2023ApJ...951...33T`, arXiv:2306.00077). TESS flare census; rate 5.6/day above 10³¹ erg. Drives the atmospheric stripping argument for the canonical alternative.
- **Atri D. 2019** — *Modelling stellar proton event-induced particle radiation dose on close-in exoplanets*, MNRAS 492, L28 (`2020MNRAS.492L..28A`, arXiv:1910.09871). Surface dose calculations for M-dwarf exoplanets under stellar proton events; informs the radiation environment and aurora intensity.
- **Sergeev D. E. et al. 2020** — *Atmospheric Convection Plays a Key Role in the Climate of Tidally Locked Terrestrial Exoplanets: Insights from High-Resolution Simulations*, ApJ 894, 84 (`2020ApJ...894...84S`, arXiv:2004.03007). Substellar convection framework for tidally-locked thin-atmosphere planets.

### Read (context / methodology, not decision-driving)

- **Plavchan P. et al. 2020** — *A planet within the debris disk around the pre-main-sequence star AU Microscopii*, Nature 582, 497 (`2020Natur.582..497P`, arXiv:2006.13248). TESS discovery of b; provides the stellar-activity context that informs d's atmosphere retention discussion.
- **Martioli E. et al. 2021** — *AU Mic c: a second planet transiting the young M dwarf AU Mic*, A&A 649, A177 (`2021A&A...649A.177M`, arXiv:2102.05288). Discovery of c; defines the inner planetary architecture that allowed TTV detection of d.
- **Chen J. & Kipping D. 2017** — *Probabilistic Forecasting of the Masses and Radii of Other Worlds*, ApJ 834, 17 (`2017ApJ...834...17C`, arXiv:1603.08614). Mass-radius relation used by NASA Exoplanet Archive for the placeholder radius of d (1.02 R⊕).
- **Goldreich P. & Soter S. 1966** — *Q in the Solar System*, Icarus 5, 375 (`1966Icar....5..375G`). Tidal damping timescale framework used for the 1:1 spin-orbit conclusion.
- **Vinson A. M. & Hansen B. M. S. 2017** — *On the spin states of habitable zone exoplanets around M dwarfs: the effect of a near-resonant companion*, MNRAS 472, 3217 (`2017MNRAS.472.3217V`, arXiv:1709.00007). Spin-orbit resonance thresholds; e = 0.003 too low for 3:2.

### Read (instrument / non-decisive)

- **Donati J.-F. et al. 2023** — *The magnetic field topology and filling of the very active M dwarf AU Mic*, MNRAS 525, 455 (`2023MNRAS.525..455D`). ZDI of host star; provides stellar magnetic-field context for the planetary radiation environment.
- **Cale B. L. et al. 2021** — *Diving Beneath the Sea of Stellar Activity: Chromatic Radial Velocities of AU Mic b*, AJ 162, 295 (`2021AJ....162..295C`, arXiv:2109.13996). Methodology for AU Mic RV detrending applied (indirectly) to Mallorquin 2024's recovery of d.

### Not read — no arXiv preprint or low-priority (~20 papers)

Several recent system-level dynamical studies (3-planet vs. 4-planet
stability checks, TTV reanalysis with later TESS sectors) are noted
in the ADS record but were not deep-read for this synthesis because
they don't change the headline mass/period parameters from Wittrock
2023. Proposal abstracts and conference summaries (DPS, EPSC) for
d-specific characterization plans contribute no cfg-decisive content.

## Open items for follow-up

- **Transit search for d.** If d's orbital inclination is favorable
  (Wittrock 2023 TTV fit gives i ≈ 89.3° but with substantial
  uncertainty), a future TESS sector or PLATO observation could
  catch d's transit and measure the radius directly. This would
  collapse the radius uncertainty + density uncertainty from low
  to high confidence.
- **Independent confirmation.** d is currently TTV-only with marginal
  RV recovery. A second TTV epoch or higher-precision RV reduction
  would strengthen the planet's confirmation. If d is retracted
  (unlikely given Mallorquin 2024 recovery but possible), the cfg
  should ship the AU Mic system with only b/c/e.
- **Atmospheric detection / non-detection.** Any future transmission
  spectrum of d (if a transit is detected) would directly constrain
  the atmosphere-present cfg pick. A non-detection at high SNR would
  favor the canonical airless variant; a detection of CO₂/SO₂ would
  support the cfg's outgassing scenario.
- **Cfg variant: airless rocky d.** The canonical interpretation
  (canonical alternatives row) — d as an airless rocky planet stripped
  by AU Mic's super-flare XUV bombardment — is preserved as a cfg
  variant. Surface tints remain similar (basaltic + iron-oxide), but
  atmosphere_present = false, ocean_present = false, no aurora,
  no atmospheric haze. The lava-province substellar feature persists
  in both variants (tidal + radiogenic heating).
- **Cfg variant: massive d.** Wittrock 2023's mass uncertainty
  spans 0.5–1.5 M⊕ (1σ). The high-mass end (1.5 M⊕) at the
  placeholder radius (1.02 R⊕) implies density 7.9 g/cc — a metal-rich
  composition like Mercury. This variant is unlikely to be visually
  distinguishable from the canonical reading but should be noted for
  interior-modeling consistency.
- **Cfg variant: tidal heating extreme.** Driscoll & Barnes 2015
  framework allows for tidal heating up to ~10 W/m² in the high-e
  + high-Q range, sufficient to produce an Io-class globally-active
  d with widespread volcanism. The cfg adopts a moderate 0.1–1 W/m²
  reading; the Io-class variant would extend the substellar lava
  province to global coverage and increase atmospheric SO₂.

## Related

- [au-mic](au-mic.md) — host star synthesis with disk geometry
- [au-mic-b](au-mic-b.md) — sister planet, puffy hot Neptune at 8.5 d
- [au-mic-c](au-mic-c.md) — sister planet, sub-Neptune at 18.9 d
- [au-mic-e](au-mic-e.md) — sister planet, ESPRESSO RV candidate at 33.1 d
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream cfg writers
