<!-- AU Mic e Phase 3 synthesis: cfg-ready decisions and reasoning -->
# AU Mic e — Phase 3 Synthesis

AU Microscopii e is a controversial radial-velocity candidate planet
around the 22-Myr-old M1Ve flare star AU Mic, reported by Donati et al.
2025 (A&A 700, A227; `2025A&A...700A.227D`, doi:10.1051/0004-6361/202555371)
from a multi-year SPIRou + ESPRESSO RV campaign. The reported orbital
period is 33.11 ± 0.06 d and the minimum mass is 21.1 ± 5.4 M⊕; the
planet does not transit and no other independent observational
constraint (TTV, direct imaging, astrometry) exists. The candidate
carries `pl_controv_flag = 1` in the NASA Exoplanet Archive because
the RV signal sits in a region of period space where AU Mic's
stellar-activity rotational harmonics (multiples of the 4.86-d
rotation period) can plausibly contribute systematic power; the
33.11-d period is not a clean harmonic of 4.86 d (≈ 6.81 × rotation),
which is part of why Donati 2025 argues for a planetary
interpretation, but the host star's super-saturated activity makes
RV-only candidates intrinsically harder to confirm.

Because every cfg parameter for e is downstream of an unconfirmed
detection, this synthesis is **cfg-conservative throughout** —
every confidence value is `low`, and the cfg-ready section is
explicitly gated on independent confirmation. If e is retracted in a
future analysis, the AU Mic system should ship with only b/c/d in
the NearStars cfg, and this Phase 3 synthesis should be archived
rather than promoted to the cfg writer.

**Scenario choice for NearStars: a candidate ~21 M⊕ warm sub-Neptune
on a 33.1-d orbit at ~0.16 AU around AU Mic, modeled by analogy with
AU Mic c (the system's only well-characterized sub-Neptune) as a
tidally-locked warm sub-Neptune with a thin H/He envelope over a
rocky/iron interior. Cfg shipping is gated on independent
confirmation — until a transit search succeeds, a TTV signal is
detected in extended monitoring, or a second-instrument RV recovery
appears, the cfg writer should treat AU Mic e as an optional fourth
planet variant rather than a default member.** 27 cfg picks; all are
low confidence; no documented divergences (every choice here is
either a tie-break within the unconstrained window, or a direct
inheritance from AU Mic c's better-constrained parameters).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true (conditional on planet being real) | low | 33.1 d orbit; tidal damping ≪ 22 Myr age for sub-Neptune-class planet at 0.16 AU around 0.51 M☉; same argument as AU Mic c |
| `obliquity_deg` | 0 | low | tidal damping assumption; conditional on confirmation |
| `eccentricity` | null | low | Donati 2025 does not publish e (low-S/N RV-only fit); cfg adopts circular as default |
| `argument_of_periastron_deg` | null | low | not published; null retained |
| `sidereal_period_days` | 33.11 ± 0.06 | low | Donati 2025 ESPRESSO + SPIRou RV; signal contested as activity-induced |
| `semi_major_axis_au` | 0.161 | low | derived: a³ = M☉ · P²(yr) gives 0.161 AU from M = 0.51 M☉, P = 33.11 d; Donati 2025 does not publish a directly |
| `inclination_deg` | null (assume ~89.5° if coplanar with b/c/d) | low | no transit; if e is real and coplanar with the system's edge-on architecture (b/c/d all i ≈ 88–89°, debris disk i = 89.5°), e should also be near-edge-on, but this is an inference |
| `mass_mearth` | 21.1 ± 5.4 (minimum mass; sin i = 1 if coplanar) | low | Donati 2025; mass quoted is M (not M sin i) under the coplanar-system assumption — if e is misaligned, true mass is larger |
| `radius_rearth` | 2.9 | low | Tie-break: no transit; estimated from Chen & Kipping 2017 mass-radius relation for a sub-Neptune at 21 M⊕ (≈ 2.6–3.2 R⊕ window). cfg picks 2.9 for visual parallel with AU Mic c at 2.79 R⊕ |
| `surface_gravity_g_earth` | 2.5 | low | derived = 21.1 / 2.9² (assuming the placeholder radius); strongly dependent on the radius assumption |
| `density_g_cc` | 4.7 | low | derived; slightly higher than AU Mic c's 3.7 g/cc — consistent with smaller envelope mass fraction at greater distance |
| `insolation_s_earth` | 3.6 | low | derived from L = 0.092 L☉ and a = 0.161 AU |
| `equilibrium_temp_k` (A=0) | 381 | low | derived; substantially cooler than b/c/d because of greater distance |
| `equilibrium_temp_k` (A=0.1) | 371 | low | derived; modest sub-Neptune albedo |
| `bond_albedo` | 0.10 | low | sub-Neptune analog low albedo; no measurement |
| `dayside_surface_temp_k` | 410 | low | thin envelope inheriting AU Mic c's day-night redistribution pattern; dayside slightly above T_eq |
| `nightside_surface_temp_k` | 320 | low | modest redistribution; nightside marginally below T_eq |
| `atmosphere_present` | true (assumed thin H/He envelope) | low | mass 21 M⊕ at 0.16 AU under M-dwarf XUV is in the regime where a small H/He envelope can survive over 22 Myr (Owen & Wu 2017); no direct detection |
| `atmosphere_surface_pressure_pa` | 1.0e6 | low | cloud-deck pressure for a thin H/He envelope; same analog as AU Mic c |
| `atmosphere_composition` | H₂ ~80%, He ~15%, H₂O ~2%, CH₄ + NH₃ + CO trace; potential photochemical haze | low | inherited from AU Mic c sub-Neptune analog; no direct measurement |
| `atmosphere_scale_height_km` | 50 | low | derived: kT/μg with T = 380 K, μ = 2.5, g = 24.5 m/s² |
| `atmosphere_tint_rgb_hex` | `#8a6a4c` | low | Tie-break: same family as AU Mic c — sub-Neptune photochemical haze under M-dwarf SED. Cooler than c (380 K vs 450 K) but cfg keeps the same hex for visual consistency across the AU Mic sub-Neptune pair |
| `cloud_cover_fraction` | 0.60 | low | sub-Neptune analog; slightly less than c because of cooler temperature and reduced photochemical haze generation |
| `cloud_morphology` | banded zonal cloud structure with equatorial superrotation; weaker than c's banding because of cooler temperature and slower rotation; potential H₂O/NH₃ ice cloud condensation at low latitudes | low | Showman 2009 scaled to cooler sub-Neptune; canonical reading for warm sub-Neptunes; specific morphology uncertain without observations |
| `cloud_tint_rgb_hex` | `#a08868` | low | Tie-break: slightly darker than c's `#b0987a` because of cooler temperature reducing high-cloud brightness; chosen for visual differentiation from c |
| `surface_morphology` | n/a — no solid surface visible at cloud-deck radius; interior likely water-rich mantle + rocky/iron core (or rocky world if envelope is absent) | low | density placeholder; conditional on the radius assumption |
| `magnetic_field_present` | true | low | sub-Neptune with H-rich envelope sustains modest dynamo; Yadav & Thorngren 2017 scaling — but the slow 33-d rotation would weaken the dynamo |
| `magnetic_field_strength_microtesla_equator` | 30 | low | Tie-break: weaker than c (50 μT) because of slower rotation in 1:1 lock; not measured |
| `atmospheric_escape_rate_g_s` | 1e7 | low | lower than c because of greater distance from AU Mic; energy-limited estimate with AU Mic XUV at 0.16 AU |
| `aurora_present` | true | low | H-rich upper atmosphere + AU Mic stellar wind → H Balmer-α expected, but weaker than b/c because of greater distance and smaller atmospheric mass |
| `aurora_color_primary_hex` | `#ff6e8c` | low | Tie-break: H-α 656.3 nm dominant; same color family as b/c but fainter |
| `star_apparent_angular_diameter_deg` | 2.7 | low | derived: 2 × 0.82 R☉ / 0.161 AU × (180/π) ≈ 2.7° (R from Phase 2 anchor Donati 2023 ZDI) |
| `stellar_illumination_color_temp_k` | 3518 | high | host star photometric color-equivalent blackbody (Gaia DR3 BP/RP); distinct from Phase 2 spectroscopic Teff = 3700 ± 100 K (Plavchan 2020) which drives the SED — see au-mic.md `stellar_color_temp_k` (one parameter that doesn't depend on e being confirmed) |

## Surface synthesis

AU Mic e's "surface" is the most speculative element in this Phase 3
synthesis because no observation constrains its bulk properties.
Donati 2025's RV signal gives a minimum mass of 21.1 ± 5.4 M⊕ under
the coplanar-system assumption (which the cfg adopts because the
debris disk and b/c/d are all consistently near-edge-on), but no
transit has been observed and no radius is measured. The cfg's
placeholder radius of 2.9 R⊕ comes from the Chen & Kipping 2017
probabilistic mass-radius relation applied at 21 M⊕; this places e
in the sub-Neptune regime, broadly parallel to AU Mic c (2.79 R⊕,
14.46 M⊕) but at higher mass and density.

For NearStars purposes, e is therefore modeled as a sub-Neptune
analog of c, scaled up in mass and out in distance. The "visible
surface" the player would see — if and when e is confirmed and
shipped in cfg — is the top of a thin H/He cloud deck at ~10⁶ Pa,
rendered as a banded gaseous body. Whether a rocky/iron core exists
below or whether e is instead a water-rich mantle with minimal
envelope is unresolved; the cfg adopts the thin-envelope
interpretation as the headline reading by parallel construction
with c.

**Why the radius is so uncertain.** The mass-radius diagram at
21 M⊕ admits at least three distinct compositional families. A
super-Earth with a substantial water mantle could have radius
~2.3 R⊕ at density ~9 g/cc — denser than Earth, the densest member
of the sub-Neptune valley. A sub-Neptune with ~3% H/He envelope over
a rocky core matches the Chen & Kipping 2017 placeholder at ~2.9 R⊕,
density ~4.7 g/cc — the cfg's headline reading. A more inflated
sub-Neptune with ~10% H/He could reach ~3.5 R⊕ at density ~2.7 g/cc,
similar to a small Neptune. Without a transit, the cfg cannot
distinguish these, and the placeholder value is a midrange guess.

**If e is rocky rather than envelope-bearing.** A 21 M⊕ super-Earth
at 0.16 AU around AU Mic would be subject to severe XUV-driven
atmosphere erosion over 22 Myr but not enough to strip a thick
envelope (Owen & Wu 2017 photoevaporation valley places the
envelope-stripping threshold at higher insolation than e
experiences). The rocky-without-envelope variant is therefore
plausible but not strongly favored by the photoevaporation
framework. Listed as a cfg variant in Open items.

**Surface morphology under tidal lock.** If e is a rocky variant
rather than a sub-Neptune, the surface morphology at 380 K dayside,
320 K nightside under tidal lock would produce a regime intermediate
between AU Mic d's (substellar lava province + nightside frost cap)
and Earth's (mild day-night contrast). The cfg does not commit to
specific surface features for e because the rocky-variant scenario
is itself secondary.

## Atmosphere synthesis

The atmosphere of e is, by construction, undetectable from current
observations. The candidate has no transit and no direct imaging;
the only constraint is the RV-derived mass, which says nothing
directly about atmospheric composition or pressure.

**Pressure.** The cfg adopts ~10⁶ Pa cloud-deck pressure as the
analog to AU Mic c's thin H/He envelope reading. This is a
midrange estimate; the true value could plausibly span 10⁵ Pa
(very thin envelope, near-airless rocky variant) to 10⁷ Pa
(thicker H/He envelope, mini-Neptune variant). The cfg picks the
midrange c-analog as the default.

**Composition.** By parallel construction with AU Mic c (H₂ ~80%,
He ~15%, trace H₂O/CH₄/NH₃/CO with photochemical hazes), the cfg
adopts the same composition for e. This is unprincipled but
internally consistent. The actual composition at 21 M⊕, 0.16 AU
around a flare-saturated M1V is not measurable from current data.

**Sky appearance.** Under the assumed thin H/He envelope, the
daytime sky on e (if descending toward the cloud deck) would
appear as a deeper-cream-toned banded surface lit by AU Mic at
2.7° angular diameter. Surface insolation 3.6× Earth's — substantial,
but lower than at b (18.8×) or c (6.5×). The visual presentation
would be a smaller, cooler cousin to c.

**Atmospheric escape.** The XUV-driven escape rate at 0.16 AU
under AU Mic's saturated regime is roughly an order of magnitude
lower than at c's 0.119 AU, giving ~10⁷ g/s under energy-limited
assumptions. This is small enough that the envelope, if present,
is largely retained over the system's 22-Myr age.

## Rotation & spin synthesis

Tidal damping of a 33.1-d sub-Neptune at 0.161 AU around 0.51 M☉
proceeds on a timescale of ~10⁷ years (Goldreich & Soter 1966 with
Neptune-like Q ≈ 10⁴), comparable to or marginally less than the
22-Myr system age. Whether e is fully locked at 1:1 spin-orbit
depends sensitively on the planet's tidal Q and on the
eccentricity (not measured); the cfg adopts 1:1 lock as the
default scenario consistent with the sub-Neptune analog
interpretation.

**KSP implementation note (conditional on confirmation).** Rotation
period = orbital period = 33.11 days (2 860 704 s). Kopernicus
`rotationPeriod` should match the orbital `period`. If the cfg
ships e as an optional fourth planet, this rotation period
applies; if e is omitted, the cfg writer should not synthesize a
rotation cfg for an unshipped body.

**No seasons.** Obliquity damped to zero (under the locked
assumption). Eccentricity is not measured — circular assumption is
adopted.

**Day-night redistribution.** With a thin H/He envelope, e's
atmosphere transports heat from day to night moderately well, but
less than b's thicker envelope. Expected day-night contrast:
~90 K (dayside 410 K, nightside 320 K). The contrast is smaller
than at b/c because e's lower insolation reduces the thermal
forcing.

**Slow rotation effects.** With a 33-day rotation period, Coriolis
effects are an order of magnitude weaker than at b/c. Atmospheric
circulation is dominated by direct day-to-night thermal forcing
(Sergeev 2020 substellar convection framework) rather than zonal
jets. Banded structure may be less developed than at c.

## Visual styling

The visual presentation of AU Mic e (conditional on confirmation)
is a smaller, cooler, more weakly-banded cousin to AU Mic c:

- **Global appearance.** A warm sub-Neptune disk with faint zonal
  banding, lit by AU Mic at 2.7° angular diameter (5× the Sun from
  Earth — still dominant but reduced compared to the inner three
  planets). The disk shows muted red-brown bands (`#8a6a4c` for
  primary haze, `#a08868` for zone clouds) — slightly cooler-toned
  than c because of the lower temperature reducing high-cloud
  brightness.
- **Banded structure.** Equatorial superrotation jet produces a
  faint equatorial zone with darker mid-latitude belts, but less
  pronounced than at c because of the slower rotation period and
  cooler temperature. Bands appear as fine stripes rather than
  broad zones. Tie-break: chose banded over uniform haze for
  visual continuity with the other AU Mic sub-Neptunes.
- **Cloud-top texture.** Even less turbulent than c — e's smaller
  scale height + much slower rotation means eddies and Rossby
  waves are minimal. The cloud top reads as a relatively smooth
  banded surface with subtle perturbations.
- **No prominent escape tail.** Unlike b, e's atmospheric escape
  is estimated at ~10⁷ g/s — invisible at any practical observation
  geometry. Cfg renders no extended halo or escape tail for e.
- **Star in sky.** AU Mic subtends 2.7° in e's sky (5× the Sun
  from Earth) — a moderate red disk dominating the daytime sky.
  Surface insolation 3.6× Earth's at substellar cloud top.
  Super-flares brighten illumination by 1–3 magnitudes for tens of
  minutes — least dramatic among the four planets because of
  greatest distance, but still substantial because of AU Mic's
  intrinsic flare luminosity.
- **Sister planets.** b (innermost, puffy Neptune) at conjunction
  appears as a small dot ~0.2° in diameter; c (next inward,
  sub-Neptune) similar; d (innermost rocky) faint at ~0.05°.
  The edge-on debris disk at 35–210 AU is visible as a thin
  bright streak on either side of AU Mic, with the inner edge
  at ~3° from the star as seen from e.

The debris disk's inner edge at 35 AU is angularly closer from e
(~2.6° away on the sky) than from the inner planets, but the
visual difference is subtle — the disk's brightness and geometry
dominate the appearance from any AU Mic vantage point.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Donati J.-F. et al. 2025** — *AU Mic system characterized with ESPRESSO*, A&A 700, A227 (`2025A&A...700A.227D`, doi:10.1051/0004-6361/202555371). Discovery paper for the AU Mic e candidate; SPIRou + ESPRESSO RV at 33.11-d period with minimum mass 21.1 ± 5.4 M⊕. **Cornerstone (and currently only) detection.** Signal flagged as `pl_controv_flag = 1` in NEA because of AU Mic's super-saturated activity making RV-only detections difficult to confirm.
- **Mallorquin M. et al. 2024** — *AU Mic system characterized with ESPRESSO*, A&A 689, A132 (`2024A&A...689A.132M`). ESPRESSO + TESS joint analysis that refined b/c parameters but did not detect e — sets the context for the activity-modeling sensitivity at AU Mic. The non-detection in Mallorquin 2024 is one source of the controversy: Donati 2025's later analysis with extended SPIRou data recovers a signal that Mallorquin 2024's pipeline did not pick up.
- **Mallorquin M. et al. 2024b (non-confirmation)** — *Revisiting the dynamical masses of the transiting planets in the young AU Mic system*, A&A accepted (arXiv:2407.16461). Explicit non-confirmation: "we do not confirm the recently proposed existence of the planet candidate AU Mic 'e' with an orbital period of 33.4 days." Sets 3σ upper limit K_e < 10 m/s in optical RV using the earlier Donati 2023 period. Donati 2025 responds: the revised lower amplitude (5.9 m/s, 4.9σ) sits below Mallorquin's optical sensitivity floor and is detectable mainly in SPIRou near-IR — wavelength-dependent SNR, not refutation.
- **Wittrock J. M. et al. 2023** — *Transit Timing Variation Measurements and Dynamical Mass Determination of the AU Mic System*, AJ 166, 232 (`2023AJ....166..232W`, arXiv:2310.10719). TTV-based dynamical mass for the inner planets; introduces d. Wittrock's N-body fit does not require an additional perturber at 33 d (any d-c TTV residuals can be explained by their dynamical model without e), which is part of the e-controversy chain.
- **Owen J. E. & Wu Y. 2017** — *The Evaporation Valley in the Kepler Planets*, ApJ 847, 29 (`2017ApJ...847...29O`, arXiv:1705.10810). Photoevaporation framework; e at 3.6 S⊕ + AU Mic XUV is well above the envelope-retention threshold at 22 Myr, supporting the thin-H/He-envelope cfg pick over the rocky-without-envelope variant.
- **Chen J. & Kipping D. 2017** — *Probabilistic Forecasting of the Masses and Radii of Other Worlds*, ApJ 834, 17 (`2017ApJ...834...17C`, arXiv:1603.08614). Mass-radius relation used to estimate the placeholder radius of 2.9 R⊕ from the RV-derived mass.

### Read (context / methodology, not decision-driving)

- **Plavchan P. et al. 2020** — *A planet within the debris disk around the pre-main-sequence star AU Microscopii*, Nature 582, 497 (`2020Natur.582..497P`, arXiv:2006.13428). TESS discovery of b; defines the system's stellar-activity context relevant to the e-controversy.
- **Martioli E. et al. 2021** — *AU Mic c: a second planet transiting the young M dwarf AU Mic*, A&A 649, A177 (`2021A&A...649A.177M`, arXiv:2102.05288). Discovery of c; the sub-Neptune analog from which most of e's cfg parameters are inherited.
- **Tristan I. I. et al. 2023** — *Catching the Flares of the AU Mic System with TESS*, ApJ 951, 33 (`2023ApJ...951...33T`, arXiv:2306.00077). TESS flare census; rate 5.6/day above 10³¹ erg. Drives the activity-contamination concern for the e RV signal.
- **Klein B. et al. 2021** — *Investigating the young AU Mic system with SPIRou: stellar magnetic field and close-in planet mass*, MNRAS 502, 188 (`2021MNRAS.502..188K`, arXiv:2012.04970). SPIRou near-IR ZDI + RV of AU Mic; methodology that fed into the Donati 2025 SPIRou + ESPRESSO joint analysis.
- **Boldog Z. et al. 2025** — *Transit-timing variations in the AU Mic system observed with CHEOPS*, A&A 694, A137 (`2025A&A...694A.137B`, arXiv:2501.13575). CHEOPS TTV refinement of b/c orbits with d as inner perturber. Does NOT address e at the 33 d period — Boldog's TTV fit does not require an outer 33-d perturber. Neither confirms nor refutes e; most recent TTV study with no signature at e's period.
- **Donati J.-F. et al. 2023** — *The magnetic field topology and filling of the very active M dwarf AU Mic*, MNRAS 525, 2015 (`2023MNRAS.525.2015D`). ZDI of host star; provides stellar magnetic-field context for any close-in candidate.
- **Goldreich P. & Soter S. 1966** — *Q in the Solar System*, Icarus 5, 375 (`1966Icar....5..375G`). Tidal damping timescale framework used for the conditional 1:1 spin-orbit conclusion.
- **Sergeev D. E. et al. 2020** — *Atmospheric Convection Plays a Key Role in the Climate of Tidally Locked Terrestrial Exoplanets: Insights from High-Resolution Simulations*, ApJ 894, 84 (`2020ApJ...894...84S`, arXiv:2004.03007). Substellar-convection framework applied to the day-night redistribution discussion.

### Read (instrument / non-decisive)

- **Cale B. L. et al. 2021** — *Diving Beneath the Sea of Stellar Activity: Chromatic Radial Velocities of AU Mic b*, AJ 162, 295 (`2021AJ....162..295C`, arXiv:2109.13996). GP-detrending methodology applied (indirectly) to the Donati 2025 e detection; not e-decisive.

### Not read — no arXiv preprint or low-priority (~15 papers)

The AU Mic e literature is sparse because the candidate is very
recent (Donati 2025) and has not yet been the subject of
independent follow-up observations. Several upcoming papers
(extended SPIRou monitoring, possible TESS extended-mission
detection attempts, JWST atmospheric characterization proposals)
are in progress but were not deep-read because they don't
contribute cfg-decisive content at this time. The full filtered
bibliography is preserved in the planet's `_bib/au-mic-e.yaml`
(to be created) with `status: skipped` annotations.

## Open items for follow-up

- **Independent confirmation (highest priority).** The cfg's
  inclusion of AU Mic e is gated on independent confirmation. A
  second-instrument RV detection (e.g., from extended HARPS-N or
  MAROON-X monitoring), a TTV signal in extended b/c transit
  monitoring with TESS or PLATO, or a successful transit search
  would each promote e from candidate to confirmed. If e is
  retracted instead (the activity-contamination explanation winning
  out over a planetary one), the cfg should ship AU Mic with only
  b/c/d and the e Phase 3 should be archived as
  `docs/phase3/_archived/au-mic-e.md` rather than promoted to the
  cfg writer.
- **Transit search.** If e's inclination is favorable (probably
  near-edge-on if coplanar with the rest of the system), a
  transit could be detectable in extended TESS sectors or future
  PLATO observations. A transit detection would collapse the
  radius uncertainty (currently ±~10% from the Chen & Kipping
  placeholder) and the density uncertainty from low to high
  confidence, and would also independently confirm the planet's
  existence.
- **Atmospheric detection.** Conditional on confirmation, any
  JWST transmission spectrum of e would constrain the assumed
  thin-H/He composition. A non-detection at high SNR would favor
  the rocky-without-envelope variant; a detection of H₂O, CH₄,
  or CO would support the cfg's sub-Neptune-analog reading.
- **Cfg variant: e omitted.** If e is retracted, the cfg ships
  AU Mic with only b/c/d. This is the default conservative
  variant: ship only confirmed planets, preserve the e Phase 3
  in archive, and revisit if independent confirmation appears.
  This variant is the **conservative default** until confirmation
  arrives.
- **Cfg variant: e confirmed as sub-Neptune.** If e is confirmed
  and transits are detected, ship as the cfg synthesizes here —
  a c-analog sub-Neptune at 0.16 AU, 33-d period, 21 M⊕ with
  thin H/He envelope and banded zonal cloud structure.
- **Cfg variant: e confirmed as rocky super-Earth.** If e is
  confirmed but no transits are detected and the mass-radius
  inference points to a rocky composition (density > 6 g/cc),
  ship as a heavy super-Earth analog of AU Mic d rather than as
  a sub-Neptune. Surface morphology would shift toward d's
  tidally-locked-rocky pattern (substellar lava province
  attenuated by lower insolation; nightside cold trap; thin or
  absent atmosphere). The visual styling would diverge
  meaningfully from the headline reading.
- **Cfg variant: e at higher mass.** If extended RV monitoring
  finds the true mass is higher (e.g., if the system is not
  perfectly coplanar and the RV gives only M sin i), e could
  approach Neptune mass (~30–40 M⊕). This would push the cfg
  toward a b-analog puffy Neptune reading. Listed as a possible
  variant pending higher-quality data.

## Related

- [au-mic](au-mic.md) — host star synthesis with disk geometry
- [au-mic-b](au-mic-b.md) — sister planet, puffy hot Neptune at 8.5 d
- [au-mic-c](au-mic-c.md) — sister planet, sub-Neptune at 18.9 d (the closest analog used to inherit e's parameters)
- [au-mic-d](au-mic-d.md) — sister planet, Earth-mass TTV candidate at 12.7 d
- [methodology](../reference/methodology.md) — Decisions schema
- [mod-reference](../reference/mod-reference.md) — downstream cfg writers
