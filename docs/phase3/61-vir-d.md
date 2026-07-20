<!-- 61 Vir d Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 61 Vir d — Phase 3 Synthesis

61 Vir d is the outermost of three RV-detected planets around the G6.5V
solar twin 61 Virginis, reported by Vogt et al. 2010 (HIRES + AAT joint
solution). The detection is radial-velocity-only; the planet does not
transit, so the directly measured quantities are limited to orbital
period P = 123.01 ± 0.55 d, semi-major axis a = 0.476 AU, eccentricity
e = 0.35, argument of periastron ω = 314°, and minimum mass Msini =
22.9 ± 2.6 M⊕. The true mass is at least 22.9 M⊕ and most plausibly in
the 23–32 M⊕ range under the system's likely near-edge-on inclination
posterior. No radius has been measured; reflected-light direct
imaging is a future-class observation (HabEx / LUVOIR era), so the
ground-state atmosphere is currently unconstrained.

**Scenario choice for NearStars: a cool, eccentric sub-Neptune with a
retained H/He primary envelope (~5–8% by mass), a thicker condensate
cloud deck of H₂O and NH₃ ices, faint zonal banding, and a strongly
modulated insolation over the e = 0.35 orbit.** This is the K2-18 b /
Hycean-adjacent archetype applied to d's cooler insolation
(S ≈ 3.6 S⊕, T_eq(A=0) ≈ 383 K, T_eq(A=0.3) ≈ 351 K) and high
eccentricity. The alternative — a fully Hycean water-world with a
shallow H₂ envelope over a liquid-water layer — is preserved as a
cfg variant in Open items because d's mean insolation places it close
to the inner edge of the Hycean window (Madhusudhan 2021) but the
e = 0.35 orbital excursion swings it well inside the runaway-greenhouse
boundary at periastron.

## Decisions

Kopernicus / atmosphere cfg-ready values. `Confidence`: high =
directly measured or tightly constrained, medium = theoretical with
strong support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false (pseudo-synchronous) | medium | Tidal-locking timescale at 123 d / 0.48 AU is ~5–15 Gyr for a 23 M⊕ planet; exceeds 6 Gyr system age. With e=0.35 the spin state is pseudo-synchronous (Hut 1981; Henning & Hurford 2014), not locked |
| `obliquity_deg` | 15 | low | Tie-break: tidal damping is incomplete at d's separation; cfg picks 15° for visible seasonal modulation of the cloud bands, within the dynamically allowed window for a near-coplanar sub-Neptune |
| `eccentricity` | 0.35 | high | Vogt 2010 RV fit; the highest eccentricity of the three 61 Vir planets |
| `argument_of_periastron_deg` | 314 | high | Vogt 2010 |
| `sidereal_period_days` | 123.01 | high | Vogt 2010 orbital period; rotation differs (pseudo-sync) |
| `semi_major_axis_au` | 0.476 | high | Vogt 2010 |
| `mass_mearth` | 22.9 | high | Vogt 2010 Msini; lower bound only (RV-only) |
| `radius_rearth` | 5.0 | medium | Tie-break: no transit; mass–radius for 23 M⊕ with a 5–8% H/He envelope (Lopez & Fortney 2014, Howe 2014) gives R = 4.5–5.5 R⊕; cfg picks 5.0 R⊕ as the cool-sub-Neptune mid-range, slightly larger than c because d's cooler envelope is less compressed |
| `surface_gravity_g_earth` | 0.92 | medium | derived = 22.9 / 5.0² (at the H/He envelope nominal cloud-top reference radius) |
| `density_g_cc` | 1.00 | medium | derived; consistent with a ~5–8% H/He envelope on a rocky core, slightly less dense than c at the cooler equilibrium |
| `insolation_s_earth` | 3.62 | high | derived from L = 0.82 L☉ and a = 0.476 AU |
| `insolation_s_earth_periastron` | 8.57 | high | derived; S × (1 − e)⁻² at e = 0.35 |
| `insolation_s_earth_apoastron` | 1.99 | high | derived; S × (1 + e)⁻² at e = 0.35 |
| `equilibrium_temp_k` (A=0) | 383 | high | derived |
| `equilibrium_temp_k` (A=0.3) | 351 | high | derived |
| `equilibrium_temp_k_periastron` (A=0) | 476 | high | derived; T_eq × (1 − e)⁻⁰·⁵ |
| `equilibrium_temp_k_apoastron` (A=0) | 330 | high | derived; T_eq × (1 + e)⁻⁰·⁵ |
| `bond_albedo` | 0.35 | medium | Tie-break: range 0.2–0.5 for cooler sub-Neptune with thicker H₂O/NH₃ cloud deck; cfg picks 0.35 (slightly higher than c at 0.30 because d's cooler temperature favors more reflective water-ice clouds) |
| `dayside_brightness_temp_k_at_clouds` | 340 | medium | Derived from T_eq with moderate redistribution and 1-bar cloud-top reference |
| `nightside_brightness_temp_k_at_clouds` | 285 | medium | Pseudo-synchronous heat redistribution with deeper envelope gives moderate day-night contrast (Showman 2009 / Lewis 2014 GCM regime for cool sub-Neptunes) |
| `atmosphere_present` | true | high | H/He envelope retention at 23 M⊕ × 0.48 AU around a G-dwarf is unambiguous (Owen & Wu 2017 photoevaporation valley: d is far outside the loss boundary) |
| `atmosphere_reference_pressure_pa` | 100000 | high | gas planet — no solid surface; cloud-top reference at ~1 bar = 10⁵ Pa |
| `atmosphere_composition` | H₂ ~74%, He ~24%, H₂O ~0.5%, CH₄ ~0.2%, NH₃ ~0.1%, traces of CO, CO₂, photochemical hazes | medium | Standard sub-Neptune primordial composition (Madhusudhan 2012; Moses 2013); higher condensable abundances than c because d's cooler temperature allows deeper-mixed volatiles to reach the visible deck |
| `atmosphere_scale_height_km` | 165 | medium | derived: kT/μg with T≈351 K, μ=2.4 (H/He dominated), g=0.92 g⊕ = 9.0 m/s² |
| `atmosphere_tint_rgb_hex` | `#b8c4d4` (pale blue-grey limb haze) | low | Tie-break: H/He Rayleigh scattering peaks in blue under solar-yellow illumination; the cooler T_eq means less photochemical haze attenuation than c, so the limb shows a more pronounced Rayleigh-blue tint |
| `cloud_cover_fraction` | 1.0 | high | Cool sub-Neptune with thick condensate cloud deck (H₂O ice at upper levels, NH₃ ice at deeper levels); near-complete coverage from the combined cloud + photochemical haze blanket |
| `cloud_morphology` | global water-ice + ammonia-ice cloud deck with faint zonal banding from an eastward equatorial jet; modulated cloud thickness over the eccentric orbit | medium | Showman 2009 / Lewis 2014 GCM for cool sub-Neptunes: super-rotating equatorial jet (~0.5 km/s) drives faint zonal banding; H₂O / NH₃ condensates form the optically thick deck; e=0.35 drives periodic thickening near apoastron and partial dissipation near periastron |
| `cloud_tint_rgb_hex` | `#e0e4ec` (pale blue-white cloud deck, water-ice analog) | low | Tie-break: water-ice clouds are intrinsically white-blue; cfg picks the pale blue-white tone over the warm cream of c to give d a distinct "cooler, icier" visual identity |
| `surface_tint_rgb_hex_primary` | n/a (no surface) | high | gas planet |
| `surface_tint_rgb_hex_accent` | n/a | high | gas planet |
| `surface_morphology` | n/a — gas planet | high | no rocky surface |
| `ocean_present` | false | high | no surface; deep envelope may host a supercritical H₂O / ionic H₂O layer at >10⁴ bar but not a discrete ocean |
| `tidal_heating_w_m2` | 0.005–0.05 | medium | Bolmont 2020 / Henning & Hurford 2014 scaling for e=0.35 at 123 d period; higher than c because of larger e but still negligible vs. insolation budget |
| `radiogenic_heat_w_m2` | 0.01 | low | Rocky-core radiogenic contribution; small fraction of total heat flux for a gas planet |
| `seasonal_amplitude_factor` | 4.3 | high | derived: S_peri / S_apo = ((1+e)/(1-e))² = 4.3× at e=0.35; the largest seasonal modulation in the 61 Vir system |
| `star_apparent_angular_diameter_deg` | 0.108 | high | derived: 2 × R★ / a; 0.963 R☉ at 0.476 AU |
| `stellar_illumination_color_temp_k` | 5552 | high | host Teff |

## Surface synthesis

61 Vir d has **no rocky surface** in the cfg-rendering sense — the
planet is a sub-Neptune with a continuous H/He envelope wrapped over a
rocky/icy core. The visible "surface" the cfg renders is the cloud-deck
at the ~1 bar reference level, where water-ice and ammonia-ice
condensates combine with photochemical haze to produce a featureless
globally cloud-covered appearance under solar-twin illumination.

The deep interior structure is inferred from mass–radius scaling for
sub-Neptunes (Lopez & Fortney 2014, Howe 2014). For Msini = 22.9 M⊕ at
0.48 AU around a G-dwarf, three mass–radius branches are
observationally consistent:

1. **H/He envelope branch (canonical)** — 5–8% envelope mass over a
   rocky/icy core, giving R = 4.5–5.5 R⊕. Density ~1.0 g/cc. This is
   the cool sub-Neptune archetype, with a slightly thicker envelope
   than c because the cooler equilibrium temperature reduces
   photoevaporation pressure to negligible levels.

2. **Hycean / water-world branch** — ~30–50% water mass fraction with
   a thin H₂ atmosphere over a liquid-water layer, giving R ≈ 3.5–4.5
   R⊕. Density ~1.8 g/cc. d's mean T_eq ≈ 351 K is close to the inner
   edge of Madhusudhan 2021's Hycean window (T_eq 200–400 K at the
   water-ice surface), making this branch genuinely viable for the
   mean orbit; however e=0.35 drives T_eq to 476 K at periastron, well
   above the liquid-water stability limit at a 1-bar surface pressure.
   The branch is preserved as a cfg variant.

3. **Iron-rich rocky branch** — pure rock+iron giving R ≈ 2.7 R⊕,
   density ≈ 6.5 g/cc. Excluded by Owen & Wu 2017 photoevaporation
   physics: at 0.48 AU around a G-dwarf the loss rate over 6 Gyr is
   ~0.05% of any H/He envelope, far below the threshold for stripping.
   Loss-driven evolution does not produce this branch at d's
   parameters.

The cfg adopts **branch 1 (H/He envelope)** as canonical, parallel to
the c synthesis. d's cooler envelope hosts a richer condensate
chemistry than c (water-ice clouds become optically dominant at T_eq <
400 K, supplementing the NH₃ / KCl / Na₂S population available at c's
warmer 478 K). The water-rich Hycean variant is more compelling for d
than for c on the mean-orbit T_eq alone, but the periastron excursion
disfavors it; the canonical reading remains the H/He sub-Neptune.

**Color choice.** Under solar-twin illumination, the dominant visible
features are the upper-tropospheric water-ice cloud deck (producing
the pale blue-white cloud-top tint `#e0e4ec`) and the underlying
ammonia-ice deck at the deeper ~3-bar level. Photochemical haze
(Lavvas 2017) is thinner than at c's higher T_eq because the cooler
stratosphere reduces methane photolysis efficiency; the Rayleigh-blue
limb haze (`#b8c4d4`) is therefore more visible than at c, where the
haze blanket dominates.

**Morphology under pseudo-synchronous rotation.** With a 123 d
orbital period and e=0.35, the spin state is pseudo-synchronous (Hut
1981, Henning & Hurford 2014) — rotation rate matching the orbital
angular velocity at pericenter, giving a sidereal period of ~84 d
(vs. the orbital 123 d). Showman 2009 and Lewis 2014 GCMs for cool
sub-Neptunes in this rotation regime predict a moderate eastward
super-rotating equatorial jet (~0.5 km/s, slower than at c because
the longer rotation period weakens Coriolis-driven jet acceleration)
driving subtle zonal banding. The bands are visible as soft contrast
variations modulated by the strong eccentricity-driven seasonal cycle:
near periastron the cloud deck thins and bands become slightly more
defined; near apoastron the deck thickens into a near-uniform
gradient.

## Atmosphere synthesis

d's atmosphere is canonical cool sub-Neptune territory: a retained
H/He primary envelope of 5–8% by mass over a rocky/icy core, with
trace condensable volatiles (H₂O, CH₄, NH₃) and photochemical hazes
that combine with deep water-ice and ammonia-ice cloud decks to
produce the featureless visible disk.

**Retention argument.** Owen & Wu 2017's photoevaporation valley
analysis places d far to the right of the loss boundary. For a 23 M⊕
core at 0.48 AU around a 0.82 L☉ G-dwarf, the XUV-driven mass loss
rate scales to ~10⁵ g/s — about 10⁻⁴ of the envelope mass lost per
Gyr. Over the 6.1 Gyr system age the total loss is ~10⁻³ of the
envelope, completely negligible. d retains its primary atmosphere
with the largest margin of any 61 Vir planet.

**Pressure profile.** No surface — the envelope is hydrostatically
continuous from low-density gas at the top to multi-kbar supercritical
H/He at the rocky-core boundary. The cfg adopts a 1-bar reference
level for the "cloud-top" surface that the renderer treats as the
visible disk. Scale height 165 km at this level is consistent with
cool sub-Neptune scale-height estimates (Lewis 2014). Atmospheric
composition follows the standard primordial-envelope model
(Madhusudhan 2012, Moses 2013): H₂ ~74%, He ~24%, H₂O ~0.5%, CH₄
~0.2%, NH₃ ~0.1%, with traces of CO, CO₂, HCN, and photochemical
hazes. The condensable abundances are higher than at c because d's
cooler temperature allows deeper-mixed volatiles (especially H₂O and
NH₃) to reach the visible deck without thermal dissociation.

**Clouds.** At T_eq ~ 351 K (mean) and pressures of 0.1–10 bar, the
condensable species in equilibrium are water-ice (condensing at 273 K
at the upper troposphere reference altitude), NH₃ ice (condensing at
~200 K at deeper altitudes), and NH₄SH (Lewis 1969 thermochemistry,
~5 bar level). Water-ice forms the optically dominant upper cloud
deck; NH₃ ice and NH₄SH form deeper layers. Photochemical haze
(Morley 2015, Lavvas 2017) from methane + HCN photolysis is present
but thinner than at c's warmer T_eq — the cooler stratosphere
reduces the photochemical reaction efficiency.

**Sky appearance from a hypothetical aerostat at 1 bar.** The sky
above is pale blue-white (`#e0e4ec`) with the disk of 61 Vir visible
through the cloud cover as a moderately diffuse warm-yellow patch at
angular diameter ~0.11° — about a fifth of the Sun's apparent
diameter from Earth. Surface brightness through the cloud deck is
significantly reduced from the direct insolation level (S = 3.6 S⊕
at top of atmosphere becomes ~0.5 S⊕ at the 1-bar level after cloud
attenuation). Day-night contrast at the cloud-top is moderate:
~55 K temperature difference between substellar (~340 K) and
antistellar (~285 K) cloud-tops drives a pseudo-zonal circulation
that smooths terminator features.

**Eccentricity-driven seasons.** The e=0.35 orbit drives a 4.3×
modulation of insolation between periastron and apoastron, the
largest of any 61 Vir planet. This is the dominant atmospheric
forcing for d: at periastron the cloud deck thins (water-ice clouds
partially sublimate as T_eq rises to 476 K and the upper troposphere
warms above water-condensation temperature locally), revealing
darker NH₃ and deeper haze layers; at apoastron the deck thickens
and the disk appears more uniformly bright. The seasonal cycle
period is 123 d, and the orbital phase determines a slow brightness
modulation observable in reflected light at the few-percent level.

**Photochemical haze chemistry.** The 5552 K solar-twin SED gives a
near-Earth-Sun UV-to-visible ratio. Methane photolysis at λ ≲ 200 nm
produces HCN, C₂H₂, and higher-mass haze precursors (Lavvas 2017).
The cooler stratosphere at d (compared to c) reduces the photolysis
rate by ~3× at the same UV flux per molecule, giving a thinner haze
layer that does not dominate the optical appearance. The H/He
Rayleigh signature is therefore more visible at d than at c.

## Rotation & spin synthesis

d's spin state is determined by the balance of tidal-damping and
eccentricity-pumping timescales. At a 123-day orbital period, 0.48 AU
separation, and 23 M⊕ mass, the tidal locking timescale for an
Earth-analog interior Q is ~5–15 Gyr (Henning & Hurford 2014
scaling). This exceeds the 6.1 Gyr system age — d has not had time to
reach 1:1 lock. Obliquity damping has been incomplete; the cfg picks
15° as a tie-break for visual seasonal modulation.

With eccentricity 0.35 (Vogt 2010), Hut 1981's pseudo-synchronous
state is the dominant attractor: rotation rate matching the orbital
angular velocity at pericenter, giving a sidereal period of ~84 d
(vs. the orbital 123 d). This produces a slowly drifting substellar
point in the rotating frame, with the substellar longitude completing
a full rotation in ~280 days.

**KSP implementation note.** The cfg adopts `rotation_period_days` =
84 (pseudo-synchronous, ~7 257 600 s in Kopernicus units). This is
distinct from the orbital period and produces a non-locked, slow
rotation that gives d a faint diurnal cycle combined with a strong
seasonal cycle from the e=0.35 orbit.

**Obliquity.** Tidal damping is incomplete at d's distance; the cfg
picks 15° as a tie-break — large enough to give visible seasonal
modulation of the cloud bands (cloud-belt latitudes shift with
sub-solar latitude over the orbit), small enough to keep the
near-coplanar inclination posterior of the 61 Vir system intact. The
b/c inner planets have lower obliquity because of stronger tidal
damping at smaller separations.

**Tidal heating.** Bolmont 2020 / Henning & Hurford 2014 scaling for
e=0.35 at 123 d period and 23 M⊕ mass gives a tidal heating
contribution of 0.005–0.05 W/m². The higher eccentricity boosts the
flux above c's 0.001–0.01 W/m², but the longer period attenuates the
overall budget. This is negligible relative to the ~50 W/m² absorbed
mean insolation at the cloud-top, so d is firmly
**insolation-dominated** in its thermal budget. The deep interior may
host modest residual heat from formation + radiogenic decay (~0.01
W/m²), again small relative to insolation.

**Strong seasons.** Eccentricity 0.35 drives a 4.3× modulation of
insolation over the orbit. Combined with the deep H/He envelope's
slow thermal response, the seasonal cycle manifests as cloud-deck
thickness modulation rather than dramatic temperature swings — but
the visible disk brightness modulates by ~10–15% over the 123 d
orbit, the strongest seasonal photometric signature in the 61 Vir
inner system.

## Visual styling

Combining the surface and atmosphere decisions:

- **Global appearance (orbit view).** A pale blue-white, hazy disk
  with a soft cool overall tint (`#e0e4ec`) under solar-twin
  illumination. Slightly icier-looking than c, distinct enough to
  read as a "cooler outer sub-Neptune" at a glance. Faint zonal
  banding visible at high contrast; otherwise a featureless
  soft-edged sphere with a clearer Rayleigh-blue limb haze
  (`#b8c4d4`) than c.
- **Cloud-top morphology.** Pseudo-zonal banding from the
  super-rotating equatorial jet (~3–4 bands across the disk, with
  faint contrast). Substellar region slightly brighter (~340 K
  warmer cloud + thicker condensate veil); antistellar slightly
  darker. Banding contrast strengthens near periastron (cloud deck
  thins) and weakens near apoastron (deck thickens into a smoother
  gradient).
- **Eccentricity-driven seasonal cycle.** Over the 123 d orbit the
  visible disk modulates by ~10–15% in brightness — brightest near
  periastron (more reflected light from thinner cloud deck plus
  closer geometry) and dimmest near apoastron. The cfg can encode
  this as a slow ~123 d brightness pulsation tied to the
  orbital phase.
- **Limb haze.** Pale blue Rayleigh scattering at λ ≲ 0.5 μm from
  the H/He upper atmosphere is more visible than at c because the
  photochemical haze blanket is thinner. Adds a soft cyan ring
  around the disk at the terminator, particularly noticeable at
  high phase angles.
- **Nightside.** Reflected sister-planet light from c (small disk,
  inferior conjunction every ~55 d) and from b (very dim, distant).
  Nightside cloud-top temperature 285 K — too cool to be visible in
  optical thermal emission but bright in mid-IR (~10 μm).
- **Star in sky.** 61 Vir subtends 0.108° at d — about a fifth of the
  Sun's angular size from Earth at mean distance, swelling to ~0.166°
  at periastron and shrinking to ~0.080° at apoastron. Through the
  cloud deck it appears as a diffuse warm-yellow patch (`#fff2dc`
  cfg-encoded host tint), not a sharp disk. Surface illumination
  ~3.6× Earth's at top of atmosphere (mean), ranging from ~8.6× at
  periastron to ~2.0× at apoastron.
- **Sister planets in sky.** c (next inward at 0.22 AU) appears at
  angular size ~0.05° at superior conjunction and ~0.1° at inferior
  conjunction (every ~55 days); b (at 0.05 AU) is much smaller
  (~0.01° at maximum elongation) and not always visible from d's
  vantage. Near-coplanar geometry; conjunctions are sky events for
  any in-system observer.
- **Optional seasonal animation.** A slow modulation of cloud-deck
  brightness and band contrast over the 123 d orbit, synchronized
  with the orbital phase, would faithfully render the
  eccentricity-driven seasonal cycle. Higher-priority Phase 3.5
  visual detail than for b or c because d's seasonal swing is
  large enough to be visually noticeable.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Vogt S. S. et al. 2010** — *A Super-Earth and Two Neptunes
  Orbiting the Nearby Sun-Like Star 61 Virginis*, ApJ 708, 1366
  (`2010ApJ...708.1366V`). The discovery paper. Reports d's orbit
  (P=123.01 d, a=0.476 AU, e=0.35, ω=314°) and minimum mass
  (Msini = 22.9 ± 2.6 M⊕). HIRES + AAT joint RV solution. All
  Decisions table orbital + mass values anchor here.
- **Owen J. E. & Wu Y. 2017** — *The evaporation valley in the
  Kepler planets*, ApJ 847, 29 (`2017ApJ...847...29O`, [arXiv:1705.10810](https://arxiv.org/abs/1705.10810)).
  Photoevaporation-valley physics. Places d far outside the loss
  boundary (XUV-driven loss ~10⁻³ of envelope over 6 Gyr).
  Anchors `atmosphere_present = true` with high confidence.
- **Lopez E. D. & Fortney J. J. 2014** — *Understanding the
  mass-radius relation for sub-Neptunes*, ApJ 792, 1
  (`2014ApJ...792....1L`, [arXiv:1311.0329](https://arxiv.org/abs/1311.0329)). Sub-Neptune envelope
  mass-radius scaling. For 23 M⊕ with 5–8% H/He envelope, R = 4.5–5.5
  R⊕; cfg picks 5.0 R⊕. Anchors the `radius_rearth` tie-break.
- **Howe A. R. et al. 2014** — *Mass-radius relations and core-envelope
  decompositions of super-Earths and sub-Neptunes*, ApJ 787, 173
  (`2014ApJ...787..173H`). Sub-Neptune mass-radius
  diversity; supports the H/He envelope canonical reading and bounds
  the Hycean / water-rich alternative.
- **Madhusudhan N. 2012** — *C/O ratio as a dimension for
  characterizing exoplanetary atmospheres*, ApJ 758, 36
  (`2012ApJ...758...36M`, [arXiv:1209.2412](https://arxiv.org/abs/1209.2412)). Sub-Neptune
  primordial-envelope composition baseline; drives the H/He primary
  + trace condensable composition.
- **Madhusudhan N. et al. 2021** — *Habitability and biosignatures of
  Hycean worlds*, ApJ 918, 1 (`2021ApJ...918....1M`, [arXiv:2108.10888](https://arxiv.org/abs/2108.10888)).
  Hycean class definition; d's mean T_eq sits near the inner edge of
  the Hycean window. Drives the Open-items Hycean variant.
- **Moses J. I. et al. 2013** — *Compositional diversity in the
  atmospheres of hot Neptunes*, ApJ 777, 34 (`2013ApJ...777...34M`,
  [arXiv:1306.5178](https://arxiv.org/abs/1306.5178)). Photochemistry of sub-Neptunes; informs the
  CH₄/HCN/photochemical-haze chain at d's cooler stratosphere.
- **Morley C. V. et al. 2015** — *Thermal emission and reflected
  light spectra of super Earths with flat transmission spectra*, ApJ
  815, 110 (`2015ApJ...815..110M`, [arXiv:1511.01492](https://arxiv.org/abs/1511.01492)). Hazy
  sub-Neptune retrieval framework; informs the haze-thickness scaling
  between c (warmer) and d (cooler).
- **Lavvas P. & Koskinen T. 2017** — *Aerosol properties of the
  atmospheres of extrasolar giant planets*, ApJ 847, 32
  (`2017ApJ...847...32L`, [arXiv:1707.08077](https://arxiv.org/abs/1707.08077)). Sub-Neptune photochemical
  haze formation mechanism; supports the thinner haze layer at d.
- **Showman A. P. et al. 2009** — *Atmospheric circulation of hot
  Jupiters: coupled radiative-dynamical GCM*, ApJ 699, 564
  (`2009ApJ...699..564S`, [arXiv:0809.2089](https://arxiv.org/abs/0809.2089)). Establishes the
  super-rotating equatorial jet in tidally-influenced gas planets;
  informs d's `cloud_morphology` (zonal banding).
- **Lewis N. K. et al. 2014** — *GCMs of warm sub-Neptunes*, ApJ 795,
  150 (`2014ApJ...795..150L`, [arXiv:1410.0008](https://arxiv.org/abs/1410.0008)). GCM scaling for the
  cool sub-Neptune regime; supports the pseudo-synchronous spin and
  the weaker equatorial-jet circulation at d's longer rotation
  period.
- **Hut P. 1981** — *Tidal evolution in close binary systems*, A&A
  99, 126 (`1981A&A....99..126H`). Pseudo-synchronous spin equilibrium
  for eccentric orbits; foundational citation for d's spin state at
  e=0.35.
- **Henning W. G. & Hurford T. 2014** — *Tidal heating in multilayered
  terrestrial exoplanets*, ApJ 789, 30 (`2014ApJ...789...30H`,
  [arXiv:1311.5904](https://arxiv.org/abs/1311.5904)). Sub-Neptune tidal heating + spin-locking
  timescales; gives ~5–15 Gyr for d's parameters (exceeds system age).
- **Bolmont E. et al. 2020** — *Tidal dissipation and obliquity
  evolution* (`2020A&A...644A.165B`). Provides the
  tidal-heating flux scaling for d (0.005–0.05 W/m²).
- **Lewis J. S. 1969** — *The clouds of Jupiter and the NH₃-H₂O and
  NH₃-H₂S systems*, Icarus 10, 365. Foundational thermochemistry for
  sub-Neptune cloud condensation sequences; gives the H₂O / NH₃ /
  NH₄SH layering at d's T_eq.

### Read (context / methodology, not decision-driving)

- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age
  Estimation for Solar-Type Dwarfs* (`2008ApJ...687.1264M`,
  [arXiv:0807.1686](https://arxiv.org/abs/0807.1686)). Inherited from host-star synthesis. Gives 61 Vir
  age 6.1 ± 1.7 Gyr; sets the photoevaporation evolution timescale.
- **Pavlenko Y. V. et al. 2012** — *Solar twin candidates*
  (`2012MNRAS.422..542P`, [arXiv:1112.0590](https://arxiv.org/abs/1112.0590)). Inherited from host-star
  synthesis. Confirms solar-twin SED for the photochemical-haze model.
- **Fulton B. J. et al. 2017** — *The California-Kepler Survey III.
  A Gap in the Radius Distribution of Small Planets*, AJ 154, 109
  (`2017AJ....154..109F`, [arXiv:1703.10375](https://arxiv.org/abs/1703.10375)). Radius valley
  demographics; supports the H/He envelope canonical reading for d's
  23 M⊕ population.
- **Wyatt M. C. et al. 2012** — *Herschel imaging of 61 Vir*
  (`2012MNRAS.424.1206W`, [arXiv:1204.6063](https://arxiv.org/abs/1204.6063)). Inherited from host-star
  synthesis. Cited briefly; the cold debris ring at 30 AU does not
  interact dynamically with d at 0.48 AU (d sits well inside the
  ring's inner edge).
- **Kreidberg L. et al. 2014** — *Clouds in the atmosphere of the
  super-Earth exoplanet GJ 1214 b*, Nature 505, 69
  (`2014Natur.505...69K`, [arXiv:1401.0022](https://arxiv.org/abs/1401.0022)). Featureless sub-Neptune
  transmission spectrum reference; informs the global cloud cover
  expectation at d's parameters.

### Read (instrument-only, not visual-informative)

- **Marcy G. W. et al. 2014** — Kepler super-Earth statistics
  context.

### Not read — no arXiv preprint or low-priority (~10 papers)

The d-specific arXiv record is small. The not-read set is
predominantly:

- **Dynamical-stability follow-ups** of the Vogt 2010 system; d's
  e=0.35 is the most dynamically active element of the three-planet
  chain, but the system is stable within Vogt 2010's solution.
- **Transit search non-detections** confirming d does not transit;
  geometric transit probability for d at e=0.35, a=0.48 AU is ~0.6%,
  so the non-detection is consistent with random inclination.
- **Generic photoevaporation-rate calculations** without 61 Vir-specific
  stellar wind models.

## Open items for follow-up

- **True mass and radius from direct imaging.** d's mass is Msini-only
  and its radius is a mass–radius scaling estimate. A future
  direct-imaging campaign would yield true mass + radius from a
  reflected-light detection; HabEx / LUVOIR era observation. d is
  the most favorable 61 Vir planet for direct imaging because of its
  largest angular separation from the host (~57 mas at maximum
  elongation).
- **Cfg variant: Hycean / water-world envelope.** At d's mean T_eq
  ~ 351 K (close to the inner edge of Madhusudhan 2021's Hycean
  window), a water-rich envelope with thin H₂ atmosphere is
  observationally consistent with the H/He primary envelope. The
  e=0.35 orbit takes d to T_eq ~ 476 K at periastron, well above the
  liquid-water stability limit at 1 bar, disfavoring but not
  excluding the Hycean reading. Cfg variant would render d as a
  denser, less hazy, deeper-blue ocean-world disk with periodic
  storms triggered at periastron. Document as Phase 3.5 alternative.
- **Cfg variant: rocky no-envelope alternative.** Photoevaporation
  physics strongly favors envelope retention (loss < 0.1% over
  6 Gyr) but a small residual probability remains for a pure-rocky
  23 M⊕ planet (R ≈ 2.7 R⊕, density ~6.5 g/cc). Render would be a
  cooler rocky world — visually distinct from the haze-covered
  canonical reading. Preserve as cfg variant.
- **Cfg variant: stronger seasonal storm system.** d's e=0.35
  drives a 4.3× insolation modulation, the largest in the 61 Vir
  system. GCM simulations targeted at the d-specific eccentricity
  could constrain whether this drives episodic storm features
  (cyclones, equatorial overshooting) that would warrant additional
  visual detail beyond the static cloud-band rendering. Phase 3.5
  refinement.
- **Future direct-imaging spectroscopy.** Although d does not
  transit, future direct-imaging spectroscopy could resolve the
  cloud-top composition. Refinement opportunities: H₂O/CH₄/NH₃
  abundances, haze optical depth, deeper cloud composition (water-ice
  vs NH₃-ice vs NH₄SH).
- **Atmospheric escape rate cross-check.** Owen & Wu 2017 generic
  scaling already places d at negligible loss; a 61 Vir-specific
  stellar wind + XUV model (Vidotto-style) would confirm but not
  change the qualitative envelope-retention conclusion.

## Related

- [61-vir](61-vir.md) — host star Phase 3 synthesis
- [61-vir-b](61-vir-b.md) — innermost sibling hot super-Earth at 0.05 AU
- [61-vir-c](61-vir-c.md) — middle sibling sub-Neptune at 0.22 AU (warmer analog)
- [methodology](../reference/methodology.md) — Decisions schema
