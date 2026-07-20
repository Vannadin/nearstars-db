<!-- AU Mic c Phase 3 synthesis: cfg-ready decisions and reasoning -->
# AU Mic c — Phase 3 Synthesis

AU Microscopii c is a 2.79 ± 0.18 R⊕, 14.46 ± 3.24 M⊕ warm sub-Neptune
on an 18.86-day orbit around the 22-Myr-old M1Ve flare star AU Mic.
Martioli et al. 2021 (A&A 649, A177; `2021A&A...649A.177M`,
[arXiv:2102.05288](https://arxiv.org/abs/2102.05288)) discovered the planet in TESS Sector 27 transits
that had been missed in the original Sector 1 search because of the
longer period; Mallorquin et al. 2024 (A&A 689, A132;
`2024A&A...689A.132M`) refined both mass and radius with combined
ESPRESSO + TESS reanalysis. Bulk density is ≈ 3.7 g/cc — about
two-thirds Earth's, lower than typical rocky super-Earths but
substantially higher than b's 0.45 g/cc puffy regime. c sits in the
mass–radius "valley" between gas-dominated sub-Neptunes and water-rich
rocky planets — its bulk composition is consistent with either a
~5% H/He envelope over a rocky/iron core, or a substantial water-rich
mantle with minimal hydrogen envelope. No atmospheric detection has
been reported as of this writing.

**Scenario choice for NearStars: a tidally-locked warm sub-Neptune
with a thin H/He envelope (~5% by mass) over a water-rich rocky/iron
core, surface pressure at the cloud deck ~10⁶ Pa, modest cloud
morphology with banded structure under M-dwarf illumination, hot
dayside, and a less-pronounced atmospheric escape signature than b
because of c's deeper gravitational well and lower insolation.**
All 26 cfg picks are canonical-aligned within the sub-Neptune
literature window; two are tie-breaks (atmosphere tint hex, cloud
tint hex). No documented divergences.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false (pseudo-synchronous; 3:2 candidate) | high | 18.86 d orbit; tidal damping ≪ 22 Myr age for sub-Neptune at 0.119 AU around 0.51 M☉, but e = 0.18 drives pseudo-synchronous rotation (Hut 1981 ω/n ≈ 1.24) — 3:2-capture regime, not pure 1:1 |
| `obliquity_deg` | 5 | high | tidal damping toward zero; small residual retained for the eccentric, pseudo-synchronous spin state |
| `eccentricity` | 0.18 | medium | Mallorquin 2024 ESPRESSO + TESS joint fit |
| `argument_of_periastron_deg` | 72.8 | medium | Mallorquin 2024 |
| `sidereal_period_days` | 18.859023 | high | Martioli 2021 TESS Sector 27 + Sector 1 |
| `semi_major_axis_au` | 0.119 | high | Mallorquin 2024 (Kepler's third from M☉ + P) |
| `inclination_deg` | 89.46 | high | Martioli 2021 transit fit; refined Mallorquin 2024 |
| `mass_mearth` | 14.46 ± 3.24 | high | Mallorquin 2024 ESPRESSO RV with GP detrending |
| `radius_rearth` | 2.79 ± 0.18 | high | Mallorquin 2024 TESS reanalysis |
| `surface_gravity_g_earth` | 1.86 | high | derived = 14.46 / 2.79² |
| `density_g_cc` | 3.7 | high | derived; ≈ 0.67 ρ_Earth — consistent with thin H/He + rocky core OR water-rich mantle |
| `insolation_s_earth` | 7.2 | high | derived from L = 0.102 L☉ (Donati 2023, recommended) and a = 0.119 AU |
| `equilibrium_temp_k` (A=0) | 454 | high | derived; consistent with TEPCat 428 K reported with non-zero albedo |
| `equilibrium_temp_k` (A=0.1) | 442 | high | derived; modest sub-Neptune albedo |
| `bond_albedo` | 0.10 | medium | sub-Neptune analog low albedo; cloud-deck reflectance |
| `dayside_surface_temp_k` | 500 | medium | thinner envelope than b → less day-night redistribution; dayside slightly above T_eq. Estimated from the day-night heat-recirculation (+ internal-heat) parameterization of Cowan & Agol 2011 (`1001.0012`) in the weak-recirculation limit |
| `nightside_surface_temp_k` | 380 | medium | modest redistribution with thin H/He envelope. Estimated from the Cowan & Agol 2011 (`1001.0012`) heat-recirculation (+ internal-heat) parameterization |
| `atmosphere_present` | true (thin H/He envelope) | medium | density consistent with envelope mass ~5%; Lopez & Fortney 2014 scaling; no direct atmospheric detection yet |
| `atmosphere_surface_pressure_pa` | 1.0e6 | medium | cloud-deck pressure for thin envelope; sub-Neptune analog; Owen & Wu 2017 photoevaporation valley framework |
| `atmosphere_composition` | H₂ ~80%, He ~15%, H₂O ~2%, CH₄ + NH₃ + CO trace; potential photochemical haze | medium | sub-Neptune analog; if water-world variant, H₂O could be higher (5–10%) |
| `atmosphere_scale_height_km` | 82 | high | derived: kT/μg with T = 450 K, μ = 2.5 (H/He + heavier admixture), g = 18.2 m/s² |
| `atmosphere_tint_rgb_hex` | `#8a6a4c` | low | Tie-break: interesting-first. Sub-Neptune photochemical haze under M-dwarf SED → muted red-brown, similar to b but less pronounced because of less inflation |
| `cloud_cover_fraction` | 0.65 | medium | sub-Neptune analog with banded structure but more variable than puffy Neptunes |
| `cloud_morphology` | banded zonal cloud structure with equatorial superrotation, less pronounced than b; potential H₂O/NH₃ ice cloud condensation at terminator | medium | Showman 2009 scaled to sub-Neptune temperature + rotation; canonical for warm sub-Neptunes |
| `cloud_tint_rgb_hex` | `#b0987a` | low | Tie-break: muted cream under M1V red light; chosen for visual differentiation from b's brighter clouds |
| `surface_morphology` | n/a — no solid surface visible at cloud-deck radius; deeper interior likely water-rich mantle + rocky/iron core | medium | density and mass-radius position place c just inside the sub-Neptune envelope regime |
| `magnetic_field_present` | true | medium | Sub-Neptune H-rich envelope sustains a modest dynamo (ice-giant analog) |
| `magnetic_field_strength_microtesla_equator` | 50 | low | Order-of-magnitude **ice-giant analog** (Neptune/Uranus ~0.1–0.5 G; Connerney 1991), scaled below b for the smaller envelope. The energy-flux scaling (Christensen 2009; applied to inflated exoplanets by Yadav & Thorngren 2017 `1709.05676`) is hot-Jupiter-validated; AU Mic c (0.046 M_Jup) is below that regime, where He separation makes the surface field unquantifiable (Stevenson 1980) → estimate, not measured. See docs/reference/planetary-dynamo-scaling.md |
| `atmospheric_escape_rate_g_s` | 1e8 | medium | Energy-limited escape after Lecavelier des Etangs 2007 (`astro-ph/0609744`), scaled down from b's Allart-2023-anchored ~1e10 g/s by c's deeper gravity well and lower insolation |
| `aurora_present` | true | low | H-rich upper atmosphere + AU Mic stellar wind → H Balmer-α expected, but weaker than b due to smaller atmospheric mass |
| `aurora_color_primary_hex` | `#ff6e8c` | low | Tie-break: H-α 656.3 nm dominant; same color family as b but fainter |
| `star_apparent_angular_diameter_deg` | 3.9 | high | derived: 2 × 0.862 R☉ / 0.119 AU × (180/π) ≈ 3.9° |
| `stellar_illumination_color_temp_k` | 3665 | high | from host star Teff |

## Surface synthesis

AU Mic c sits at the lower edge of the sub-Neptune regime. Mass
14.46 M⊕ and radius 2.79 R⊕ give density 3.7 g/cc — consistent
with either:

1. **Thin H/He envelope** (~5% by mass) over a rocky/iron core. Lopez
   & Fortney 2014 mass-radius diagrams place 2.79 R⊕ / 14.46 M⊕ in
   the regime where ≤ 10% H/He envelope inflates a rocky core to the
   observed size. This is the canonical sub-Neptune interpretation
   and is the cfg's default reading.

2. **Water-world variant** with a significant H₂O mantle (perhaps
   30–40% by mass) and minimal hydrogen envelope. This is also
   consistent with the bulk density (Zeng 2019 mass-radius for
   water worlds) and would be a meaningful alternative — but the
   sub-Neptune valley (Fulton 2017, Owen & Wu 2017) statistically
   favors the H/He-envelope interpretation for planets in c's regime,
   and AU Mic's youth (22 Myr) makes a primordial H/He envelope more
   likely retained than in older systems.

For NearStars purposes, the "visible surface" the player sees is the
top of the H/He cloud deck at ~10⁶ Pa, rendered as a banded gaseous
body with a less pronounced banding pattern than b (because of the
smaller envelope mass + slower rotation). There is no rocky terrain
to render. The interior structure — rocky/iron core, H₂O/silicate
mantle, H/He envelope — affects density inversions but not the
visible appearance.

The youth of the system continues to matter here. At 22 Myr, c is
still contracting; its current density of 3.7 g/cc will increase to
perhaps 4.5 g/cc at Gyr ages as the envelope cools and the planet
shrinks by ~10–15% in radius. This is too subtle to render in a
single cfg, but justifies treating the present-day inflated state as
the default rather than an old-system equivalent.

## Atmosphere synthesis

The atmosphere of c is not directly detected, but its existence and
properties are constrained indirectly.

**Pressure.** The transit-derived radius pins the cloud-deck pressure
to roughly 10⁶ Pa for a thin H/He envelope. If c is the water-world
variant, the dominant gas at this pressure would be supercritical
steam rather than H₂, but the visible cloud deck location would be
similar. The cfg adopts the thin-envelope interpretation as the
headline reading.

**Composition.** No direct atmospheric measurement exists for c at
this writing. The composition is inferred from the bulk density +
sub-Neptune mass-radius valley: H₂ ~80%, He ~15%, with trace H₂O,
CH₄, NH₃, CO at near-solar abundance. Photochemical hazes from CH₄
photolysis under AU Mic's intense XUV are expected; whether these
condense into a haze layer comparable to Titan's depends on the
upper-atmosphere C/O ratio (not measured for c). The cfg adopts a
moderate haze layer with cloud cover fraction 0.65 — slightly less
than b's 0.70 because of c's reduced inflation and the lack of
direct cloud-detection evidence.

**Sky appearance.** From low orbit, c looks like a smaller, less
inflated version of b: muted red-brown bands under deep red M1V
illumination, with the equatorial superrotation jet visible but less
pronounced than b's. The cloud-top color (`#b0987a`) is more muted
than b's (`#c0a880`) because of the higher gravity and reduced
atmospheric scale height — less haze accumulation in the visible
column. The star fills 3.9° in c's sky (about 7× the Sun from Earth)
and is the dominant illumination source; surface insolation is 7.2×
Earth's at the substellar cloud top, but red-shifted.

**Atmospheric escape.** With c at 0.119 AU receiving 7.2× Earth's
insolation, the XUV-driven escape rate is roughly an order of
magnitude lower than b's: ~10⁸ g/s under energy-limited assumptions
with AU Mic's saturated-regime XUV flux. This is sufficient to lose
a few percent of the H/He envelope over the system's projected
lifetime — significant for the long-term evolution but minor for
the present-day visual appearance. No He I 10830 Å detection has
been attempted at c-equivalent precision; if attempted with current
instruments, an escape-tail comparable to b's is possible but at
lower significance.

## Rotation & spin synthesis

Tidal damping of an 18.86-day sub-Neptune at 0.119 AU around
0.51 M☉ proceeds on a timescale of ~10⁶–10⁷ years (Goldreich & Soter
1966 with Neptune-like Q ≈ 10⁴); over the 22-Myr system age, c is
tidally evolved (damping ≪ age, though closer to the age than for b).
At eccentricity 0.18 (Mallorquin 2024) the spin does not settle into
pure 1:1 but into a pseudo-synchronous (super-synchronous) state, with
a Mercury-like 3:2 resonance a real possibility; the cfg adopts the
pseudo-synchronous state (`tidally_locked = false`), and the 3:2
variant is preserved in Open items. No spin–orbit angle
measurement (Rossiter–McLaughlin) has been published for c at this
writing.

**KSP implementation note.** Rotation period = orbital period =
18.859023 days (1 629 419.6 s). Kopernicus `rotationPeriod` should
match the orbital `period`.

**Mild seasonal modulation.** Obliquity damped to zero, but
eccentricity 0.18 drives substantial insolation variation (1 +/- 36%)
along the orbit. Periapsis insolation is ~11 S⊕, apoapsis ~5 S⊕ — a
factor-of-2 variation. The thick atmosphere smooths this to ~30 K
cloud-top temperature variation across the orbit, visible as a
modest brightening of the dayside near periapsis.

**Day-night redistribution.** With a thinner H/He envelope than b's,
c's atmosphere is less efficient at redistributing heat to the
nightside. Expected day-night contrast: ~120 K (dayside 500 K,
nightside 380 K). No phase-curve observation has been attempted; the
host-star spot signal would dominate at AU Mic c's transit depth.

## Visual styling

The visual presentation of AU Mic c is a softer, smaller cousin to b:

- **Global appearance.** A warm sub-Neptune disk with muted zonal
  banding, lit by AU Mic at 3.9° angular diameter (7× the Sun from
  Earth — still dominant but no longer overwhelming). The disk shows
  muted red-brown bands (`#8a6a4c` for primary haze, `#b0987a` for
  zone clouds) — slightly more muted than b because of less
  atmospheric mass to render.
- **Banded structure.** Equatorial superrotation jet produces a
  faint equatorial zone with darker mid-latitude belts. Polar
  regions show subtle hood-like darkening. Bands are narrower than
  b's because of the smaller atmospheric scale height (82 km vs.
  567 km) — they appear as fine stripes rather than broad zones.
  Tie-break: chose banded over uniform haze for visual interest.
- **Cloud-top texture.** Less turbulent than b — c's smaller scale
  height + slower rotation means eddies and Rossby waves develop
  more slowly. The cloud top reads as a relatively smooth banded
  surface with fine-scale perturbations.
- **No prominent escape tail.** Unlike b, c's atmospheric escape is
  estimated at ~10⁸ g/s — visible only as a faint extended halo
  rather than a comet-like tail. Cfg renders this as a subtle
  upper-atmosphere glow at the day-night terminator during super-flare
  events, not as a discrete trailing structure.
- **Star in sky.** AU Mic subtends 3.9° in c's sky (7× the Sun from
  Earth) — a moderate-sized deep-red disk dominating the daytime sky.
  Surface insolation 7.2× Earth's at substellar cloud top.
  Super-flares brighten illumination by 1–3 magnitudes for tens of
  minutes — slightly less dramatic than at b because of greater
  distance.

The edge-on debris disk at 35–210 AU appears as a thin bright streak
on either side of AU Mic, similar to the view from b but the disk's
inner edge is now angularly closer because c is itself farther out
(disk inner edge at ~3.3° from AU Mic as seen from c, vs. ~5° from b).
Sister planets b (inward) and d (inward) are visible as small dots
at conjunction; e (outward, if confirmed) is also visible. Transits
of b across AU Mic's disk are visible from c (b's orbital plane is
within the same edge-on geometry); these would appear as small dark
spots crossing the stellar disk lasting ~3 hours.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Martioli E. et al. 2021** — *AU Mic c: a second planet transiting the young M dwarf AU Mic*, A&A 649, A177 (`2021A&A...649A.177M`, [arXiv:2102.05288](https://arxiv.org/abs/2102.05288)). TESS Sector 27 + ground-based confirmation of c at 18.86 d; transit-derived radius 2.79 R⊕. Cornerstone discovery paper.
- **Mallorquin M. et al. 2024** — *AU Mic system characterized with ESPRESSO*, A&A 689, A132 (`2024A&A...689A.132M`). ESPRESSO + TESS joint analysis; refines c's mass to 14.46 ± 3.24 M⊕ and radius to 2.79 ± 0.18 R⊕. **Adopted as headline source for mass and density.**
- **Lopez E. D. & Fortney J. J. 2014** — *Understanding the Mass-Radius Relation for Sub-Neptunes*, ApJ 792, 1 (`2014ApJ...792....1L`, [arXiv:1311.0329](https://arxiv.org/abs/1311.0329)). Mass-radius envelope-mass-fraction calibration. c's parameters give ~5% H/He envelope; drives the cfg surface pressure pick.
- **Fulton B. J. et al. 2017** — *The California-Kepler Survey III: Gap in the Radius Distribution of Small Planets*, AJ 154, 109 (`2017AJ....154..109F`, [arXiv:1703.10375](https://arxiv.org/abs/1703.10375)). The sub-Neptune / super-Earth radius valley at ~1.8 R⊕; c sits on the sub-Neptune side of the valley, statistically favoring the H/He envelope interpretation over the water-world variant.
- **Owen J. E. & Wu Y. 2017** — *The Evaporation Valley in the Kepler Planets*, ApJ 847, 29 (`2017ApJ...847...29O`, [arXiv:1705.10810](https://arxiv.org/abs/1705.10810)). Photoevaporation framework for the sub-Neptune valley; c at 6.5 S⊕ + AU Mic XUV is moderately above the threshold for envelope retention over Gyr timescales but well below it at 22 Myr.

### Read (context / methodology, not decision-driving)

- **Plavchan P. et al. 2020** — *A planet within the debris disk around the pre-main-sequence star AU Microscopii*, Nature 582, 497 (`2020Natur.582..497P`, [arXiv:2006.13248](https://arxiv.org/abs/2006.13248)). TESS discovery of b; provides context for the system's overall stellar-activity environment and the multi-spot complexity of AU Mic's lightcurve.
- **Cale B. L. et al. 2021** — *Diving Beneath the Sea of Stellar Activity: Chromatic Radial Velocities of AU Mic b*, AJ 162, 295 (`2021AJ....162..295C`, [arXiv:2109.13996](https://arxiv.org/abs/2109.13996)). First robust RV mass for b with GP detrending; methodology applied to c.
- **Wittrock J. M. et al. 2023** — *Transit Timing Variation Measurements and Dynamical Mass Determination of the AU Mic System*, AJ 166, 232 (`2023AJ....166..232W`, [arXiv:2310.10719](https://arxiv.org/abs/2310.10719)). TTV-based dynamical mass for b and c; introduces d candidate. Confirms c's mass within Mallorquin 2024 uncertainty.
- **Zeng L. et al. 2019** — *Growth model interpretation of planet size distribution*, PNAS 116, 9723 (`2019PNAS..116.9723Z`, [arXiv:1906.04253](https://arxiv.org/abs/1906.04253)). Water-world mass-radius models used for the c water-world variant interpretation.
- **Showman A. P. et al. 2009** — *Atmospheric Circulation of Hot Jupiters*, ApJ 699, 564 (`2009ApJ...699..564S`, [arXiv:0809.2089](https://arxiv.org/abs/0809.2089)). Equatorial-superrotation GCM framework, scaled to sub-Neptune temperature and rotation for the banded morphology pick.

### Read (instrument / non-decisive)

- **Szabó Gy. M. et al. 2021** — *Spi-Ops campaign on AU Mic c* (`2021A&A...654A.159S`, [arXiv:2108.07984](https://arxiv.org/abs/2108.07984)). CHEOPS transit timing for c; refines period and inclination but doesn't drive visual cfg.

### Not read — no arXiv preprint or low-priority (~20 papers)

Conference abstracts and proposal summaries for c-specific
characterization (NIRSpec proposals, ground-based RM attempts) without
published results don't contribute cfg-decisive content. He I 10830 Å
observations of c — if attempted — would meaningfully constrain the
atmospheric escape rate; no such observation has been published as of
this writing.

## Open items for follow-up

- **Atmospheric detection.** No JWST or ground-based transmission
  spectrum has been published for c. NIRSpec/NIRISS observations
  could constrain composition and reveal whether the headline
  thin-H/He interpretation or the water-world variant is correct.
  If H₂O features are detected at high significance and H₂ features
  absent, switch the cfg to a water-world variant with
  `atmosphere_composition` dominated by H₂O/CH₄/CO₂.
- **He I 10830 Å observation.** A non-detection of He I escape from c
  would corroborate the smaller-escape-tail picture; a detection
  would imply the H/He envelope is being more rapidly stripped than
  estimated and the cfg's atmospheric_escape_rate should be revised
  upward.
- **Phase curve.** Spitzer/JWST phase curve of c would constrain the
  day-night temperature contrast and the cloud-top distribution.
  Until measured, the 500 K / 380 K picks remain at medium confidence.
- **3:2 spin-orbit-resonance cfg variant.** At e = 0.18 the pseudo-
  synchronous equilibrium (Hut 1981 ω/n ≈ 1.24) sits in the 3:2
  spin-orbit-capture regime rather than pure 1:1. A 3:2 cfg variant
  (rotation period = (2/3) × 18.859023 d ≈ 12.57 d) would produce a
  slowly migrating substellar point and eccentricity-driven insolation
  seasons rather than a fixed dayside.
- **Cfg variant: water world.** The water-rich interpretation
  (Zeng 2019 mass-radius branch) is a meaningful alternative to the
  thin-H/He envelope. A "c water world" cfg variant could ship a
  steam-dominated atmosphere with H₂O ice clouds and a slightly
  different visual appearance (bluer-tinted clouds, less haze). Listed
  as a follow-up cfg variant.
- **Mature-system variant.** At 1 Gyr, c would shrink to ~2.5 R⊕ as
  the envelope cools; a "mature AU Mic c" cfg variant could ship the
  deflated state for comparison.

## Related

- [au-mic](au-mic.md) — host star synthesis with disk geometry
- [au-mic-b](au-mic-b.md) — sister planet, puffy hot Neptune at 8.5 d
- [au-mic-d](au-mic-d.md) — sister planet, Earth-mass TTV candidate at 12.7 d
- [au-mic-e](au-mic-e.md) — sister planet, ESPRESSO RV candidate at 33.1 d
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream cfg writers
