<!-- 61 Vir c Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 61 Vir c — Phase 3 Synthesis

61 Vir c is the middle of three RV-detected planets around the G6.5V
solar twin 61 Virginis, reported by Vogt et al. 2010 (HIRES + AAT joint
solution). The detection is radial-velocity-only; the planet does not
transit, so the directly measured quantities are limited to orbital
period P = 38.021 ± 0.034 d, semi-major axis a = 0.2175 AU, eccentricity
e = 0.14, argument of periastron ω = 341°, and minimum mass Msini =
18.2 ± 1.1 M⊕. The true mass is at least 18.2 M⊕ and most plausibly in
the 18–25 M⊕ range under the system's likely near-edge-on inclination
posterior. No radius has been measured; reflected-light direct
imaging is a future-class observation (HabEx / LUVOIR era), so the
ground-state atmosphere is currently unconstrained.

**Scenario choice for NearStars: a warm sub-Neptune with a retained
H/He primary envelope (~3–5% by mass), hazy stratosphere from
photochemical absorbers, and an essentially featureless cloud-covered
disk under solar-twin illumination.** This is the GJ 1214 b /
HD 97658 b cosmochemical archetype applied to c's slightly warmer
insolation (S ≈ 17 S⊕, T_eq(A=0) ≈ 525 K, T_eq(A=0.3) ≈ 478 K). The
alternative — a rocky / iron-rich super-Neptune with no H/He envelope
— is preserved as a cfg variant in Open items, because the photoevaporation
calculation for an 18 M⊕ core at 0.22 AU around a G-dwarf
unambiguously favors envelope retention but the bulk-composition
mass–radius branch is observationally degenerate without a transit.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false (pseudo-synchronous) | medium | Tidal-locking timescale at 38 d / 0.22 AU is ~1–3 Gyr for an 18 M⊕ planet; comparable to age but with e=0.14 the spin state is most likely pseudo-synchronous (Hut 1981; Henning & Hurford 2014), not strictly 1:1 |
| `obliquity_deg` | 5 | low | Tie-break: tidal damping reduces obliquity but does not zero it for a pseudo-synchronous case; cfg picks 5° for visual seasonality without violating dynamics |
| `eccentricity` | 0.14 | high | Vogt 2010 RV fit |
| `argument_of_periastron_deg` | 341 | high | Vogt 2010 |
| `sidereal_period_days` | 38.021 | high | Vogt 2010 orbital period; rotation may differ if not locked |
| `semi_major_axis_au` | 0.2175 | high | Vogt 2010 |
| `mass_mearth` | 18.2 | high | Vogt 2010 Msini; lower bound only (RV-only) |
| `radius_rearth` | 4.5 | medium | Tie-break: no transit; mass–radius for 18 M⊕ with retained H/He envelope (Lopez & Fortney 2014, Howe 2014) gives R = 3.5–6 R⊕; cfg picks 4.5 R⊕ as the canonical sub-Neptune mid-range |
| `surface_gravity_g_earth` | 0.90 | medium | derived = 18.2 / 4.5² (at the H/He envelope nominal cloud-top reference radius) |
| `density_g_cc` | 1.10 | medium | derived; consistent with a ~3–5% H/He envelope on a rocky core |
| `insolation_s_earth` | 17.4 | high | derived from L = 0.822 L☉ (von Braun 2014) and a = 0.2175 AU |
| `equilibrium_temp_k` (A=0) | 525 | high | derived |
| `equilibrium_temp_k` (A=0.3) | 478 | high | derived |
| `bond_albedo` | 0.3 | medium | Tie-break: range 0.2–0.5 for hazy sub-Neptune; cfg picks 0.3 (GJ 1214 b / HD 97658 b analog) |
| `dayside_brightness_temp_k_at_clouds` | 460 | medium | Derived from T_eq with mild redistribution and 1-bar cloud-top reference |
| `nightside_brightness_temp_k_at_clouds` | 380 | medium | Pseudo-synchronous heat redistribution gives moderate day–night contrast (Showman 2009 GCM regime for warm sub-Neptunes) |
| `atmosphere_present` | true | high | H/He envelope retention at 18 M⊕ × 0.22 AU around a G-dwarf is well-established (Owen & Wu 2017 photoevaporation valley: c sits well to the right of the loss boundary) |
| `atmosphere_surface_pressure_pa` | (no surface; envelope continuous) | high | gas planet — no surface; cloud-top reference at ~1 bar = 10⁵ Pa |
| `atmosphere_composition` | H₂ ~75%, He ~24%, H₂O ~0.3%, CH₄ ~0.1%, NH₃ ~0.05%, traces of CO, CO₂, photochemical hazes | medium | Standard sub-Neptune primordial composition (Madhusudhan 2012; Moses 2013); H/He primary with trace volatiles |
| `atmosphere_scale_height_km` | 220 | medium | derived: kT/μg with T≈478 K, μ=2.4 (H/He dominated), g=0.90 g⊕ = 8.8 m/s² |
| `atmosphere_tint_rgb_hex` | `#a8b8cc` (pale steel-blue limb haze) | low | Tie-break: H/He Rayleigh scattering peaks in blue under solar-yellow illumination, but photochemical hazes (Morley 2015) attenuate the blue and add an orange-brown undertone; cfg picks a muted steel-blue as the canonical hazy-sub-Neptune limb tint |
| `cloud_cover_fraction` | 1.0 | high | Hazy sub-Neptune archetype (GJ 1214 b: Kreidberg 2014 featureless transmission spectrum; HD 97658 b similar); complete cloud cover from KCl/Na₂S deep clouds and photochemical haze blanket |
| `cloud_morphology` | global haze deck + faint zonal banding from eastward equatorial jet | medium | Showman 2009 / Lewis 2014 GCM for warm sub-Neptunes: super-rotating equatorial jet (~1 km/s) drives faint zonal banding; deep KCl/Na₂S clouds at ~1 bar provide the optical layer |
| `cloud_tint_rgb_hex` | `#d8c8a8` (warm cream haze, GJ 1214 b analog) | low | Tie-break: photochemical haze tint from Morley 2015 sub-Neptune retrieval; cfg picks the warm-cream haze tone over a featureless gray to give c a distinct visual identity from d |
| `surface_tint_rgb_hex_primary` | n/a (no surface) | high | gas planet |
| `surface_tint_rgb_hex_accent` | n/a | high | gas planet |
| `surface_morphology` | n/a — gas planet | high | no rocky surface |
| `ocean_present` | false | high | no surface; deep envelope possibly transitions to supercritical H₂O / ionic H₂O at >10⁴ bar but not a discrete ocean layer |
| `tidal_heating_w_m2` | 0.001–0.01 | medium | Bolmont 2020 / Henning & Hurford 2014 scaling for e=0.14 at 38 d; negligible vs. insolation budget |
| `radiogenic_heat_w_m2` | 0.01 | low | Rocky-core radiogenic contribution; small fraction of total heat flux for a gas planet |
| `star_apparent_angular_diameter_deg` | 0.241 | high | derived: 2 × R★ / a × (180/π); 0.9867 R☉ (von Braun 2014 CHARA) at 0.2175 AU |
| `stellar_illumination_color_temp_k` | 5568 | high | host Teff (Rathsam 2023) |

## Surface synthesis

61 Vir c has **no rocky surface** in the cfg-rendering sense — the
planet is a sub-Neptune with a continuous H/He envelope wrapped over a
rocky/icy core. The visible "surface" the cfg renders is the cloud-deck
at the ~1 bar reference level, where photochemical haze and deep KCl /
Na₂S clouds combine to produce a featureless globally cloud-covered
appearance under solar-twin illumination.

The deep interior structure is inferred from mass–radius scaling for
sub-Neptunes (Lopez & Fortney 2014, Howe 2014). For Msini = 18.2 M⊕ at
0.22 AU around a G-dwarf, three mass–radius branches are
observationally consistent:

1. **H/He envelope branch (canonical)** — 3–5% envelope mass over a
   rocky core, giving R = 4.0–5.0 R⊕. Density ~1.1 g/cc. This is the
   warm sub-Neptune archetype, indistinguishable in mass-only
   measurements from GJ 1214 b, HD 97658 b, or K2-18 b.

2. **Water-rich envelope branch** — ~20% water mass fraction over a
   rocky core with no H/He, giving R ≈ 3.5–4.0 R⊕. Density ~1.7 g/cc.
   Visually slightly bluer and less hazy than the H/He case (Madhusudhan
   2021 Hycean class but smaller mass).

3. **Iron-rich rocky branch** — pure rock+iron giving R ≈ 2.4 R⊕,
   density ≈ 6.5 g/cc. Excluded by Owen & Wu 2017 photoevaporation
   physics: a 2.4 R⊕ rocky planet at 18 M⊕ would be at the
   photoevaporation valley center, but at 0.22 AU around a G-dwarf the
   loss rate is far below the threshold for stripping a 3–5% H/He
   envelope. Loss-driven evolution does not produce this branch at c's
   parameters.

The cfg adopts **branch 1 (H/He envelope)** as canonical. This is a
tie-break against branch 2 (water-rich); both are observationally
consistent at the RV level, but branch 1 is more common in the
sub-Neptune population (Fulton 2017 radius valley, sub-Neptunes
dominate at ~2.5 R⊕ peak). The water-rich branch is preserved as a cfg
variant in Open items.

**Color choice.** Under solar-twin illumination, the dominant visible
features are the photochemical haze layer in the upper stratosphere
(producing the warm cream cloud-top tint `#d8c8a8`) and the deep
KCl/Na₂S cloud deck at the ~1 bar reference level. The Rayleigh
scattering signature of the H/He primary atmosphere contributes a
faint blue tint at the limb (`#a8b8cc`), but the photochemical haze
overlay damps it considerably — GJ 1214 b's transmission spectrum
(Kreidberg 2014) shows essentially no Rayleigh feature visible because
the haze blocks short wavelengths.

**Morphology under pseudo-synchronous rotation.** With a 38 d orbital
period and e=0.14, the spin state is most likely **pseudo-synchronous**
(Hut 1981, Henning & Hurford 2014) — rotation rate matching the
orbital angular velocity at pericenter, ~30 d sidereal period rather
than locked 38 d. Showman 2009 and Lewis 2014 GCMs for warm
sub-Neptunes in this rotation regime predict a strong eastward
super-rotating equatorial jet (~1 km/s) driving a thin zonal banding
structure under the global haze deck. The bands are faint —
order-unity-contrast clouds + haze blend them into a soft global
gradient rather than a Jupiter-style sharp zonal stripes.

## Atmosphere synthesis

c's atmosphere is canonical sub-Neptune territory: a retained H/He
primary envelope of 3–5% by mass over a rocky/icy core, with trace
condensable volatiles (H₂O, CH₄, NH₃) and photochemical hazes that
dominate the optical appearance.

**Retention argument.** Owen & Wu 2017's photoevaporation valley
analysis places c well to the right of the loss boundary. For an
18 M⊕ core at 0.22 AU around a 0.822 L☉ G-dwarf, the XUV-driven mass
loss rate scales to ~10⁷ g/s — about 0.1% of the envelope mass lost
per Gyr. Over the 5.5 Gyr system age the total loss is ~0.8% of the
envelope, well below the 3–5% nominal envelope mass. c retains its
primary atmosphere comfortably.

**Pressure profile.** No surface — the envelope is hydrostatically
continuous from low-density gas at the top to multi-kbar supercritical
H/He at the rocky-core boundary. The cfg adopts a 1-bar reference
level for the "cloud-top" surface that the renderer treats as the
visible disk. Scale height 220 km at this level is consistent with
sub-Neptune scale-height estimates (Lewis 2014). Atmospheric
composition follows the standard primordial-envelope model
(Madhusudhan 2012, Moses 2013): H₂ ~75%, He ~24%, H₂O ~0.3%, CH₄
~0.1%, NH₃ ~0.05%, with traces of CO, CO₂, HCN, and photochemical
hazes that dominate the optical appearance.

**Clouds.** At T_eq ~ 480 K and pressures of 0.1–10 bar, the
condensable species in equilibrium are KCl (condensing at ~600 K),
Na₂S (~700 K), and water ice (condensing at upper altitudes where T
drops below 273 K). KCl/Na₂S clouds form the deep cloud deck;
water-ice clouds form an upper-altitude condensate veil where the
temperature inverts above the haze layer. Above all of this,
photochemical haze (Morley 2015, Lavvas 2017) builds up from
methane + HCN photolysis under solar-twin UV — producing the
optically thick blanket that makes warm sub-Neptunes featureless in
transmission spectroscopy.

**Sky appearance from a hypothetical aerostat at 1 bar.** The sky
above is hazy cream-orange (`#d8c8a8`) with the disk of 61 Vir
visible through the haze as a diffuse warm-yellow patch at angular
diameter ~0.23° — about half the Sun's apparent diameter from Earth.
Surface brightness through the haze is significantly reduced from
the direct insolation level (S = 17.4 S⊕ at top of atmosphere becomes
~3 S⊕ at the 1-bar level after haze attenuation). Day-night contrast
is moderate: ~80 K temperature difference between the substellar
cloud-top (~460 K) and antistellar cloud-top (~380 K) drives a
pseudo-zonal circulation that smooths out sharp terminator features.

**Photochemical haze chemistry.** The 5568 K solar-twin SED gives a
near-Earth-Sun UV-to-visible ratio. Methane photolysis at λ ≲ 200 nm
produces HCN, C₂H₂, and higher-mass haze precursors that nucleate
into the optically thick haze layer (Lavvas 2017). The haze is
distributed across the stratosphere from ~0.01 to ~0.1 bar, with
optical depth τ ≫ 1 at visible wavelengths — making c essentially
opaque to direct surface viewing.

## Rotation & spin synthesis

c's spin state is determined by the balance of tidal-damping and
eccentricity-pumping timescales. At a 38-day orbital period, 0.22 AU
separation, and 18 M⊕ mass, the tidal locking timescale for an
Earth-analog interior Q is ~1–3 Gyr (Henning & Hurford 2014 scaling).
This is comparable to but shorter than the 5.5 Gyr system age — c
has had time to damp obliquity and spin angular velocity but not
necessarily to reach strict 1:1 lock.

With eccentricity 0.14 (Vogt 2010), Hut 1981's pseudo-synchronous
state is the most likely outcome: rotation rate matching the orbital
angular velocity at pericenter, giving a sidereal period of ~30 d
(vs. the orbital 38 d). This produces a slowly drifting substellar
point in the rotating frame, with the substellar longitude completing
a full rotation in ~150 days.

**KSP implementation note.** The cfg adopts `rotation_period_days` =
30 (pseudo-synchronous, ~2 590 000 s in Kopernicus units). This is
distinct from the orbital period and produces a non-locked but slow
rotation that gives c a faint diurnal cycle for any orbital observer.

**Obliquity.** Tidal damping has reduced obliquity but the
pseudo-synchronous state allows non-zero residual obliquity. The cfg
picks 5° as a tie-break — small enough to be dynamically plausible,
large enough to give a faint seasonal modulation of the cloud bands.

**Tidal heating.** Bolmont 2020 / Henning & Hurford 2014 scaling for
e=0.14 at 38 d period and 18 M⊕ mass gives a tidal heating
contribution of 0.001–0.01 W/m². This is negligible relative to the
~250 W/m² absorbed insolation at the cloud-top, so c is firmly
**insolation-dominated** in its thermal budget. The deep interior may
host modest residual heat from formation + radiogenic decay (~0.01
W/m²), again small relative to insolation.

**No seasons in the rocky-planet sense.** Eccentricity 0.14 drives a
±30% modulation of insolation over the orbit, but with pseudo-synchronous
rotation and a deep gaseous envelope the thermal response is heavily
damped — diurnal cycles average out at depth, and the visible cloud
deck shifts by only a few Kelvin between peri and apo passages.

## Visual styling

Combining the surface and atmosphere decisions:

- **Global appearance (orbit view).** A pale, hazy disk with a warm
  cream-orange overall tint (`#d8c8a8`) under solar-twin illumination.
  Faint zonal banding visible at high contrast settings; otherwise a
  featureless soft-edged sphere. Limb haze adds a steel-blue
  Rayleigh-scattered glow (`#a8b8cc`) at the day-night terminator.
- **Cloud-top morphology.** Pseudo-zonal banding from the
  super-rotating equatorial jet (~3–5 bands across the disk, with
  faint contrast). Substellar region slightly brighter (~460 K
  warmer haze + thicker condensate veil); antistellar slightly
  darker.
- **Photochemical haze layer.** Stratospheric haze ~10⁵ km altitude
  produces the dominant warm-cream visible color. Optical depth ≫ 1
  blocks any view of deeper cloud structure — c is featureless at
  near-infrared and visible wavelengths.
- **Limb haze.** Pale steel-blue Rayleigh scattering at λ ≲ 0.5 μm
  from the H/He upper atmosphere, attenuated but visible at the
  terminator and in transmission. Adds a soft cyan ring around the
  disk in oblique sunlight.
- **Nightside.** Reflected sister-planet light from b (very dim,
  small disk) and d (similar magnitude, larger phase). Nightside
  cloud-top temperature 380 K — too cool to be visible in optical
  thermal emission but bright in mid-IR (~10 μm).
- **Star in sky.** 61 Vir subtends 0.235° at c — about half the Sun's
  angular size from Earth. Through the haze it appears as a diffuse
  warm-yellow patch (`#fff2dc` cfg-encoded host tint), not a sharp
  disk. Surface illumination ~17× Earth's at top of atmosphere, ~3×
  Earth's at the 1-bar cloud-top after haze attenuation.
- **Sister planets in sky.** b (next inward at 0.05 AU) appears at
  angular size ~0.04° at inferior conjunction (every ~5 days); d
  (next outward at 0.48 AU) appears at ~0.1° at conjunction (every
  ~55 days). Near-coplanar geometry; conjunctions are sky events for
  any in-system observer.
- **Optional banding animation.** A slow zonal drift of the cloud
  bands (timescale ~30 d, matching the pseudo-synchronous rotation
  period) would add subtle dynamism to the otherwise static-looking
  disk. Low-priority Phase 3.5 visual detail.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Vogt S. S. et al. 2010** — *A Super-Earth and Two Neptunes
  Orbiting the Nearby Sun-Like Star 61 Virginis*, ApJ 708, 1366
  (`2010ApJ...708.1366V`). The discovery paper. Reports c's orbit
  (P=38.021 d, a=0.2175 AU, e=0.14, ω=341°) and minimum mass
  (Msini = 18.2 ± 1.1 M⊕). HIRES + AAT joint RV solution. All
  Decisions table orbital + mass values anchor here.
- **Owen J. E. & Wu Y. 2017** — *The evaporation valley in the
  Kepler planets*, ApJ 847, 29 (`2017ApJ...847...29O`, arXiv:1705.10810).
  Photoevaporation-valley physics. Places c well to the right of the
  loss boundary (XUV-driven loss ~0.6% of envelope over 6 Gyr).
  Anchors `atmosphere_present = true` with high confidence.
- **Lopez E. D. & Fortney J. J. 2014** — *Understanding the
  mass-radius relation for sub-Neptunes*, ApJ 792, 1
  (`2014ApJ...792....1L`, arXiv:1311.0329). Sub-Neptune envelope
  mass-radius scaling. For 18 M⊕ with 3–5% H/He envelope, R = 4.0–5.0
  R⊕; cfg picks 4.5 R⊕. Anchors the `radius_rearth` tie-break.
- **Howe A. R. et al. 2014** — *Mass-radius relations and core-envelope
  decompositions of super-Earths and sub-Neptunes*, ApJ 787, 173
  (`2014ApJ...787..173H`, arXiv:1311.0329). Sub-Neptune mass-radius
  diversity; supports the H/He envelope canonical reading and bounds
  the water-rich alternative.
- **Madhusudhan N. 2012** — *C/O ratio as a dimension for
  characterizing exoplanetary atmospheres*, ApJ 758, 36
  (`2012ApJ...758...36M`, arXiv:1209.2412). Sub-Neptune
  primordial-envelope composition baseline; drives the H/He primary
  + trace condensable composition.
- **Moses J. I. et al. 2013** — *Compositional diversity in the
  atmospheres of hot Neptunes*, ApJ 777, 34 (`2013ApJ...777...34M`,
  arXiv:1306.5178). Photochemistry of sub-Neptunes; informs the
  CH₄/HCN/photochemical-haze chain.
- **Morley C. V. et al. 2015** — *Thermal emission and reflected
  light spectra of super Earths with flat transmission spectra*, ApJ
  815, 110 (`2015ApJ...815..110M`, arXiv:1511.01492). Hazy
  sub-Neptune retrieval framework; drives the `atmosphere_tint` and
  `cloud_tint` tie-break (warm cream haze under solar illumination).
- **Lavvas P. & Koskinen T. 2017** — *Aerosol properties of the
  atmospheres of extrasolar giant planets*, ApJ 847, 32
  (`2017ApJ...847...32L`, arXiv:1707.08077). Sub-Neptune photochemical
  haze formation mechanism; informs the global cloud cover and haze
  optical depth.
- **Kreidberg L. et al. 2014** — *Clouds in the atmosphere of the
  super-Earth exoplanet GJ 1214 b*, Nature 505, 69
  (`2014Natur.505...69K`, arXiv:1401.0022). The canonical "featureless
  transmission spectrum" sub-Neptune; c is the warmer analog with
  similar expected visual.
- **Showman A. P. et al. 2009** — *Atmospheric circulation of hot
  Jupiters: coupled radiative-dynamical GCM*, ApJ 699, 564
  (`2009ApJ...699..564S`, arXiv:0809.2089). Establishes the
  super-rotating equatorial jet in tidally-influenced gas planets;
  informs c's `cloud_morphology` (zonal banding).
- **Lewis N. K. et al. 2014** — *GCMs of warm sub-Neptunes*, ApJ 795,
  150 (`2014ApJ...795..150L`, arXiv:1410.0008). GCM scaling for the
  ~38 d period sub-Neptune regime; supports the pseudo-synchronous
  spin and equatorial-jet circulation.
- **Hut P. 1981** — *Tidal evolution in close binary systems*, A&A
  99, 126 (`1981A&A....99..126H`). Pseudo-synchronous spin equilibrium
  for eccentric orbits; foundational citation for c's spin state.
- **Henning W. G. & Hurford T. 2014** — *Tidal heating in multilayered
  terrestrial exoplanets*, ApJ 789, 30 (`2014ApJ...789...30H`,
  arXiv:1311.5904). Sub-Neptune tidal heating + spin-locking
  timescales; gives ~1–3 Gyr for c's parameters.
- **Bolmont E. et al. 2020** — *Tidal dissipation and obliquity
  evolution* (`2020A&A...644A.165B`, arXiv:2002.02015). Provides the
  tidal-heating flux scaling for c (0.001–0.01 W/m²).

### Read (context / methodology, not decision-driving)

- **Rathsam A. et al. 2023** — *Lithium depletion in solar analogs*,
  MNRAS 525, 4642 (`2023MNRAS.525.4642R`, doi:10.1093/mnras/stad2589).
  Inherited from host-star synthesis. Phase 2 anchor for 61 Vir age
  (5.50 +0.78/-0.74 Gyr); sets the photoevaporation-evolution
  timescale.
- **von Braun K. et al. 2014** — *Stellar diameters V*, MNRAS 438,
  2413 (`2014MNRAS.438.2413V`, doi:10.1093/mnras/stt2360). Inherited
  from host-star synthesis. L = 0.8222 ± 0.0033 L☉ anchors the
  insolation derivation.
- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age
  Estimation for Solar-Type Dwarfs* (`2008ApJ...687.1264M`,
  arXiv:0807.1686). Inherited from host-star synthesis. Activity-age
  6.1 ± 1.7 Gyr — demoted to cross-check vs Rathsam 2023 isochrone
  (documented divergence in host-star reconciliation).
- **Fulton B. J. et al. 2017** — *The California-Kepler Survey III.
  A Gap in the Radius Distribution of Small Planets*, AJ 154, 109
  (`2017AJ....154..109F`, arXiv:1703.10375). Radius valley
  demographics; supports the H/He envelope canonical reading for c's
  18 M⊕ population.
- **Wyatt M. C. et al. 2012** — *Herschel imaging of 61 Vir*
  (`2012MNRAS.424.1206W`, arXiv:1206.2370). Inherited from host-star
  synthesis. Cited briefly; the cold debris ring at 30 AU does not
  interact dynamically with c at 0.22 AU.
- **Madhusudhan N. et al. 2021** — *Habitability and biosignatures of
  Hycean worlds*, ApJ 918, 1 (`2021ApJ...918....1M`, arXiv:2108.10888).
  Hycean alternative scenario for sub-Neptunes; relevant to d's
  Open-items variant. Less applicable to c at its warmer T_eq but
  cited as the broader sub-Neptune classification framework.

### Read (instrument-only, not visual-informative)

- **Marcy G. W. et al. 2014** — Kepler super-Earth statistics
  context.

### Not read — no arXiv preprint or low-priority (~10 papers)

The c-specific arXiv record is small. The not-read set is
predominantly:

- **Dynamical-stability follow-ups** of the Vogt 2010 system.
- **Transit search non-detections** confirming c does not transit;
  Geometric transit probability for c at e=0.14, a=0.22 AU is ~1.5%,
  so the non-detection is consistent with random inclination.
- **Generic photoevaporation-rate calculations** without 61 Vir-specific
  stellar wind models.

## Open items for follow-up

- **True mass and radius from direct imaging.** c's mass is Msini-only
  and its radius is a mass–radius scaling estimate. A future
  direct-imaging campaign would yield true mass + radius from a
  reflected-light detection; HabEx / LUVOIR era observation.
- **Cfg variant: water-rich Hycean-style envelope.** At c's
  insolation (T_eq ~ 480 K), a water-rich envelope with H₂ atmosphere
  is observationally consistent with the H/He primary envelope. Cfg
  variant would render c as a denser, less hazy, deeper-blue disk.
  Document as Phase 3.5 alternative.
- **Cfg variant: rocky no-envelope alternative.** Photoevaporation
  physics strongly favors envelope retention but a small residual
  probability remains for a pure-rocky 18 M⊕ planet (R ≈ 2.4 R⊕,
  density ~6.5 g/cc). Render would be a hot rocky world similar to b
  but cooler — visually distinct from the haze-covered canonical
  reading. Preserve as cfg variant.
- **Future JWST or HabEx transmission spectroscopy.** Although c does
  not transit, future direct-imaging spectroscopy could resolve the
  cloud-top composition. Refinement opportunities: H₂O/CH₄/NH₃
  abundances, haze optical depth, deeper cloud composition (KCl vs
  Na₂S vs ZnS).
- **GCM-driven cloud morphology.** Lewis 2014 GCMs for warm sub-Neptunes
  predict zonal banding but the band contrast at c's specific
  parameters has not been simulated. A targeted GCM run would
  constrain the `cloud_morphology` choice between "global haze deck"
  and "haze + visible Jupiter-style bands."
- **Atmospheric escape rate cross-check.** Owen & Wu 2017 generic
  scaling supports envelope retention; a 61 Vir-specific stellar wind
  + XUV model (Vidotto-style) would refine the loss-rate estimate.

## Related

- [61-vir](61-vir.md) — host star Phase 3 synthesis
- [61-vir-b](61-vir-b.md) — next-inward sibling hot super-Earth at 0.05 AU
- [61-vir-d](61-vir-d.md) — next-outward sibling sub-Neptune at 0.48 AU (cooler analog)
- [methodology](../reference/methodology.md) — Decisions schema
