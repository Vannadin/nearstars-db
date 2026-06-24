<!-- YZ Cet Phase 3 synthesis: cfg-ready decisions and reasoning -->
# YZ Cet — Phase 3 Synthesis

YZ Cet (GJ 54.1; Gaia DR3 2358524597030794112) is an M4.5 V red dwarf
at 3.717 pc (Gaia DR3 parallax 269.06 mas) — about 12.1 light-years
away, the 21st-nearest stellar system to the Sun. The fundamental
parameters come from the frozen Phase 2 layer: effective temperature
Teff = 3100 K (Cifuentes et al. 2020, SED fitting; the three
independent determinations span 3056–3151 K), luminosity
L = 0.0022 ± 0.00005 L☉ (Cifuentes 2020, bolometric flux), radius
R = 0.1571 ± 0.0052 R☉ and mass M = 0.1368 ± 0.0033 M☉ (both Schweitzer
et al. 2019, CARMENES). It is an eruptive flare star of the
UV-Ceti / BY-Draconis class, slowly rotating at P_rot = 68.4 d (Stock
et al. 2020, V-band photometry) with a chromospheric activity index
log R'HK = −4.71 ± 0.21 (Astudillo-Defru et al. 2017) — moderately
active for a mid-M dwarf, with frequent optical flares riding on a
slowly-modulated starspot background.

What makes YZ Cet exceptional for NearStars is not its photosphere but
its magnetosphere. YZ Cet is the **first exoplanetary system with a
confirmed radio detection of star-planet magnetic interaction (SPI)**:
Pineda & Villadsen 2023 detected coherent, ~100%-circularly-polarized
2–4 GHz radio bursts with the VLA whose recurrence nearly tracks the
2.02-day orbit of the innermost planet b, and Trigilio et al. 2023
confirmed the SPI at 4.37σ with uGMRT 550–900 MHz observations,
modelling the auroral radio emission (ARE) to infer a stellar polar
field B_p ≈ 2.4 kG and a **planetary magnetic field on b of at least
0.4 G** — the first (indirect) measurement of an exoplanet magnetic
field. The host therefore carries a Jupiter-Io-style flux tube to its
inner planet, an electron-cyclotron-maser radio aurora, and ordinary
flare activity all at once.

**Scenario choice for NearStars: a deep-red, moderately active,
slowly-rotating M4.5 V flare star that anchors a Jupiter-Io-style
star-planet magnetic interaction with its innermost planet.** The
stellar layer is anchored on the frozen Phase 2 sources (Cifuentes
2020 Teff/luminosity, Schweitzer 2019 mass/radius, Stock 2020 rotation,
Astudillo-Defru 2017 activity) and on the two SPI radio papers (Pineda
& Villadsen 2023 detection, Trigilio 2023 confirmation + stellar field
inference). No circumstellar disk is known — searches have not reported
one and none is fabricated here. One tie-break sets the visual surface
tint for the 3100 K M4.5 V SED; the SPI / magnetic-field decisions sit
at medium-to-low confidence because the geometry is model-dependent.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M4.5 V | high | Astudillo-Defru et al. 2017; Pineda & Villadsen 2023 / Trigilio 2023 (eruptive variable; UV-Cet / BY-Dra class) |
| `mass_msun` | 0.1368 ± 0.0033 | high | Schweitzer et al. 2019 — CARMENES spectroscopic calibration (Phase 2 recommended); alternatives 0.1418 (Schweitzer), 0.1475 (Cifuentes 2020), 0.13 (Astudillo-Defru 2017) all within ~1σ |
| `radius_rsun` | 0.1571 ± 0.0052 | high | Schweitzer et al. 2019 — SED fitting (Phase 2 recommended); Cifuentes 2020 gives 0.1626, Astudillo-Defru 2017 gives 0.168 |
| `teff_k` | 3100 | high | Cifuentes et al. 2020 — SED fitting (Phase 2 recommended); the three determinations span 3056 (Astudillo-Defru 2017) to 3151 K (Schweitzer 2019), all consistent with mid-M |
| `luminosity_lsun` | 0.0022 ± 0.00005 | high | Cifuentes et al. 2020 — bolometric flux (Phase 2 recommended); Schweitzer 2019 gives 0.002195, indistinguishable |
| `metallicity_fe_h_dex` | null (not curated) | low | No Phase 2 metallicity measurement; skipped per project policy (sub-perception color effect at fixed Teff) |
| `age_gyr` | ~5 (not Phase-2-curated) | low | No Phase 2 age array; literature places YZ Cet at a few Gyr (Engle & Guinan 2017 give ~3.8 Gyr via the 68 d rotation); the slow rotation and moderate activity are consistent with an intermediate-age disk dwarf. Not a cfg-decisive number |
| `rotation_period_days` | 68.4 ± 0.05 | high | Stock et al. 2020 — combined V-band photometry (ASH2+SNO+ASAS+ASAS-SN), Phase 2 recommended; R+I band gives 68.5 ± 1.0 d; supersedes the 83 d Astudillo-Defru 2017 value |
| `activity_log_rhk` | −4.71 ± 0.21 | high | Astudillo-Defru et al. 2017 — Ca II H&K index (Phase 2 recommended); moderately active for a slow-rotating mid-M dwarf (Rossby number ~0.5; Pineda & Villadsen 2023) |
| `activity_h_alpha_log_lhalpha_lbol` | −4.32 | medium | Reiners 2018 (via Pineda & Villadsen 2023 Table 1); Hα in modest emission, consistent with the eruptive-variable classification |
| `x_ray_log_lx_lbol` | −4.13 | medium | Stelzer 2013 (via Pineda & Villadsen 2023 Table 1); L_X ≈ 10^27.1 erg/s, near the solar value (Trigilio 2023) |
| `flare_state` | frequent optical flares | medium | TESS optical flaring seen in the light curve (Pineda & Villadsen 2023); incoherent gyrosynchrotron radio flares also observed at 2–4 GHz. UV-Cet / BY-Dra eruptive variable |
| `magnetic_field_bf_kg` | ~2.2 | medium | Moutou et al. 2017 — Zeeman-broadening mean field ⟨Bf⟩ ≈ 2.2 kG (via Pineda & Villadsen 2023 / Trigilio 2023); a high outlier for the Rossby number, possibly overestimated (Reiners 2022) |
| `magnetic_field_polar_bp_kg` | ~2.4 | medium | Trigilio et al. 2023 — large-scale polar field B_p ≲ 2.4 kG inferred from the ARE spectrum (s=2 harmonic, ν_min ≈ 500 MHz → B_min ≈ 90 G at r_max); consistent with the Moutou 2017 ⟨Bf⟩ |
| `spi_radio_confirmed` | true | high | Trigilio et al. 2023 — ARE from SPI confirmed at 4.37σ (uGMRT 550–900 MHz, 4/9 detections folding to two orbital-phase sectors of planet b); Pineda & Villadsen 2023 VLA 2–4 GHz candidate detection |
| `spi_driver_planet` | b | high | Pineda & Villadsen 2023; Trigilio 2023 — bursts fold to b's 2.02087 d orbit, not c or d; b is innermost (a/R★ ≈ 21.9) and sits in the sub-Alfvénic regime |
| `spi_emission_frequency_ghz` | 0.5–4 | high | Trigilio 2023 (550–900 MHz uGMRT) + Pineda & Villadsen 2023 (2–4 GHz VLA); ECM at the cyclotron harmonic of the kG coronal field |
| `visual_surface_tint_hex_primary` | `#ffd081` (pale warm orange, M4.5 V) | medium | Real photospheric color: the Pickles 1998 observed M4.5 SED at 3100 K integrated through the shared CIE→sRGB engine (`scripts/refs/stellar_photospheric_color.py`), peak-channel normalized. A pale warm orange; the 3100 K blackbody is a fair first approximation and the TiO/VO bands shift the displayed chromaticity only modestly (the large effect is on the color index, not the visible hue). Nearly identical to the M4 V Barnard `#ffd487` (Teff close), all within the pale-warm-orange family. (Supersedes the earlier render-saturated brick-red estimate `#cf5630`.) |
| `stellar_color_temp_k` | 3100 | high | derived from Teff (Cifuentes 2020) |
| `visual_spot_coverage_max` | 0.1 | low | Tie-break: BY-Dra-class rotational modulation drives the 68.4 d photometric period (Stock 2020); a low-to-moderate cool-spot fraction reproduces it. Not a measured filling factor |
| `apparent_magnitude_v_from_earth` | 12.16 | high | Gaia DR3 V (converted); far below naked-eye visibility despite 3.717 pc, because of the tiny 0.0022 L☉ luminosity |
| `distance_pc` | 3.717 | high | Gaia DR3 parallax 269.06 mas; ≈ 12.1 ly, the 21st-nearest system |
| `disk_present` | false | high | No debris disk reported for YZ Cet in the literature; none fabricated (search-and-verify policy) |

## Surface synthesis

YZ Cet has the deep red photosphere typical of a mid-M dwarf. At
Teff = 3100 K (Cifuentes 2020) the SED peaks in the near-infrared near
~0.93 μm, and the optical continuum is heavily suppressed by TiO and
VO molecular bands — though not as totally strangled as the cooler
M7 V Teegarden's Star (2904 K). The three independent Teff
determinations span only 3056–3151 K, so the temperature is robust and
the rendered color is well constrained. With R = 0.1571 R☉
(Schweitzer 2019) and L = 0.0022 L☉ the star is roughly 1/450 of the
Sun's luminosity, far too faint to see by eye (V = 12.16) despite its
12.1-light-year proximity.

The defining surface property is moderate magnetic activity expressed
as a slowly-rotating, spotted, flaring disk. The Ca II H&K index
log R'HK = −4.71 (Astudillo-Defru 2017) places YZ Cet in the
moderately-active regime; the Hα is in modest emission
(log L_Hα/L_bol = −4.32, Reiners 2018 via Pineda & Villadsen 2023) and
the coronal X-ray luminosity log L_X/L_bol = −4.13 (Stelzer 2013) gives
L_X ≈ 10^27.1 erg/s, comparable to the quiet Sun (Trigilio 2023). The
star is formally an eruptive variable of the UV-Ceti / BY-Draconis
class: it shows frequent optical flares in its TESS light curve
(Pineda & Villadsen 2023) and rotational brightness modulation from
cool starspots, which is what defines the 68.4 d photometric period
(Stock 2020). For cfg rendering this means a deep-red disk carrying a
low-to-moderate cool-spot fraction that drifts on the 68-day rotation,
punctuated by bright flares — a livelier surface than the very quiet
old dwarfs (Barnard, Teegarden) but not the near-continuous flaring of
a young M dwarf like AU Mic.

The magnetic field anchoring all of this is strong. Zeeman-broadening
gives a mean surface field ⟨Bf⟩ ≈ 2.2 kG (Moutou 2017), and the
SPI radio modelling of Trigilio 2023 independently infers a
large-scale polar field B_p ≈ 2.4 kG from the auroral-radio-emission
spectrum. Mid-M dwarfs of this type "tend to have strong, kG,
axisymmetric dipolar field topologies" (Kochukhov & Lavail 2017, via
Trigilio 2023), and YZ Cet fits that picture — the strong, ordered
dipole is precisely what makes the planet-star flux tube efficient
enough to produce detectable radio aurorae. (One caveat: the Moutou
2017 Zeeman-broadening value is a high outlier for YZ Cet's Rossby
number ~0.5 and may be systematically overestimated for slow rotators,
per Reiners 2022.)

No metallicity is curated in the Phase 2 layer and none is synthesized
here; at fixed Teff the metallicity effect on the rendered M-dwarf
color is sub-perceptible, and project policy skips it for new hosts.
There is no debris disk: no infrared-excess detection or resolved
imaging of a disk around YZ Cet has been reported, so the star is
rendered diskless.

## Atmosphere synthesis

A main-sequence star has no "atmosphere" in the planetary cfg sense;
for a stellar synthesis this section covers the chromosphere, corona,
flares, and — uniquely for YZ Cet — the magnetospheric radio
environment that defines the system.

YZ Cet's chromosphere and corona are those of a moderately active mid-M
dwarf. The chromospheric Ca II H&K index log R'HK = −4.71
(Astudillo-Defru 2017) and the Hα emission (log L_Hα/L_bol = −4.32;
Reiners 2018) indicate a persistently warm chromosphere, and the
coronal X-ray output (log L_X/L_bol = −4.13; Stelzer 2013) sits near
the quiet-Sun level in absolute terms (L_X ≈ 10^27.1 erg/s; Trigilio
2023). The 68.4 d rotation gives a Rossby number Ro ≈ 0.5 (Pineda &
Villadsen 2023), placing YZ Cet in the unsaturated, magnetically-braked
regime — active, but not saturated. The wind is modest: mass-loss-rate
estimates cluster at Ṁ ≲ 0.2–5 Ṁ_⊙ depending on the model (Pineda &
Villadsen 2023 use Ṁ ≈ 0.25 Ṁ_⊙ in their realistic Model B;
Trigilio 2023 adopt Ṁ ≈ 0.2 Ṁ_⊙).

The headline feature is the magnetospheric radio aurora. With a kG-scale
ordered dipole, YZ Cet strongly confines its wind: Trigilio 2023
compute a wind magnetic confinement parameter η★ ≈ 10^8 and an Alfvén
radius R_Alf ≈ 100 R★, so **all three planets orbit deep inside the
star's magnetosphere** in the sub-Alfvénic regime. The innermost
planet b (a/R★ ≈ 21.9, orbital velocity ~87.6 km/s) ploughs through the
closed stellar field, and the perturbation propagates back along the
flux tube to the stellar poles, where electron-cyclotron-maser emission
produces highly-circularly-polarized auroral radio bursts — exactly the
Jupiter-Io mechanism, but star-sized. This is detected as ~100%-polarized
2–4 GHz bursts (Pineda & Villadsen 2023, VLA) and 550–900 MHz bursts
folding to two symmetric orbital-phase sectors of planet b (Trigilio
2023, uGMRT; 4.37σ). The ECM spectrum's low-frequency cutoff
ν_min ≈ 500 MHz implies B_min ≈ 90 G at the emission height, and the
inferred polar field is B_p ≈ 2.4 kG.

Flares punctuate all of this. Beyond the coherent SPI bursts, YZ Cet
shows incoherent gyrosynchrotron radio flares (Pineda & Villadsen 2023,
Epoch 2) and optical flares in TESS — the ordinary eruptive-variable
behaviour expected of a UV-Ceti star. For cfg purposes the corona /
chromosphere layer is "moderately active with frequent flares,"
distinct from the quiescent-with-rare-flares old dwarfs and from the
saturated young flare stars.

## Rotation & spin synthesis

YZ Cet rotates slowly, with a photometric period P_rot = 68.4 ± 0.05 d
(Stock 2020, combined V-band photometry; the R+I band gives
68.5 ± 1.0 d). This supersedes the earlier 83 d estimate of
Astudillo-Defru 2017 and the ~68.5 d value Pineda & Villadsen 2023 used
for their synodic-period phase-wrapping. A 68-day period is slow but
not extreme — far faster than the very old dwarfs Teegarden (96 d) or
GJ 1151 (~130 d), and consistent with an intermediate-age,
moderately-active mid-M dwarf. Engle & Guinan 2017 use the rotation to
estimate an age of ~3.8 Gyr; no formal age array is curated in Phase 2,
so the cfg treats age as a low-confidence ~5 Gyr context number rather
than a decision input.

**KSP implementation note.** Stellar rotation period = 68.4 d =
5 909 760 s. In Kopernicus the star body's `rotationPeriod` is set in
seconds; the slow rotation makes spin-related visual foreshortening
negligible.

The rotation matters for the SPI rendering. Because the bursts recur
near the planet's orbital period rather than the stellar rotation
period, the SPI signal is genuinely planet-driven and not a rotational
artefact — but the ~68 d stellar rotation does modulate the geometry:
between the Pineda & Villadsen 2023 epochs (~90 d apart, 1.3 rotation
periods) the tilted stellar dipole rotated significantly, which is why
the bursts did not recur at exactly the same orbital phase. For a
faithful cfg the radio-aurora animation should be keyed primarily to
planet b's 2.02-day orbit with a slower ~68-day modulation of the
visible-pole geometry.

The rotation-axis inclination is unconstrained; Trigilio 2023's
geometric ARE model favours an orbital-plane inclination i ≈ 30°–60°
and assumes the stellar dipole is roughly aligned with the rotation
axis and perpendicular to the orbital plane. For NearStars visual
rendering a generic axis orientation is adopted, since the slow
rotation makes the precise spin axis visually unimportant for the
photosphere (it matters only for the SPI flux-tube geometry).

## Visual styling

In the NearStars renderer, YZ Cet is portrayed as a pale warm orange
M4.5 V flare star whose signature is its magnetic environment rather
than its modest photosphere:

- **Global appearance.** A pale warm orange disk encoded as `#ffd081`,
  the real integrated-SED color close to the 3100 K blackbody; the
  TiO/VO bands shift the displayed chromaticity only modestly. It is
  essentially the same hue as the M4 V Barnard's Star (`#ffd487`,
  near-identical Teff), both within the pale-warm-orange family. The
  illumination color temperature for scene lighting of the three
  planets is driven directly by the 3100 K SED.
- **Spotted surface.** A low-to-moderate cool-spot fraction
  (`visual_spot_coverage_max ≈ 0.1`) drifting on the 68.4-day rotation
  reproduces the BY-Dra-class photometric modulation. Slowly-evolving
  dark spot groups, not a uniform disk.
- **Flares.** Frequent bright optical flares (UV-Cet eruptive variable)
  — more active than Barnard or Teegarden, rendered as recurrent
  transient brightenings, but not the near-continuous flaring of a
  young M dwarf.
- **Radio aurora (the headline).** Although the SPI emission is a radio
  phenomenon and not visible to the eye, it is the system's defining
  feature and should be expressed visually: a Jupiter-Io-style flux
  tube connecting the innermost planet b to the stellar magnetic poles,
  with auroral footpoints brightening at b's 2.02-day orbital cadence
  and the visible pole modulated on the 68-day rotation. From b's point
  of view this is a stellar aurora at the foot of the flux tube — a
  visually distinctive, scientifically grounded effect unique to YZ Cet
  in the catalog.
- **Star in the planets' skies.** From b (a = 0.0163 AU) the star
  subtends ~5.1° — about 10× the Sun's angular size from Earth; from c
  (~3.9°) and d (~2.9°) it is smaller but still dominant. The disk is
  deep red-orange and floods the close-in worlds with infrared-rich
  light at 8.2, 4.7 and 2.7× Earth's insolation respectively.
- **From Earth.** YZ Cet is a V = 12.16 telescopic object, invisible to
  the naked eye despite its 12.1-light-year proximity, because of the
  tiny 0.0022 L☉ luminosity.

## Bibliography

### Read (drove Decisions above)

- **Pineda J.S. & Villadsen J. 2023** — *Coherent radio bursts from
  known M-dwarf planet host YZ Ceti*, Nature Astronomy (arXiv:2304.00031).
  The VLA 2–4 GHz discovery of ~100%-circularly-polarized coherent
  radio bursts whose recurrence nearly tracks planet b's 2.02087 d
  orbit. Source for the SPI-candidate detection, the sub-Alfvénic
  environment (Model A/B winds, Rossby number ~0.5), the Table 1
  stellar parameters (M, R, Teff, log L_X/L_bol = −4.13, log L_Hα/L_bol
  = −4.32, ⟨Bf⟩ ≈ 2.2 kG, P_rot ~68.5 d), and the planet b minimum
  field inference. Establishes YZ Cet as the prime SPI monitoring case.
- **Trigilio C. et al. 2023** — *Star-Planet Interaction at radio
  wavelengths in YZ Ceti: Inferring planetary magnetic field*, ApJL
  (arXiv:2305.00809). uGMRT 550–900 MHz: 4/9 detections folding to two
  symmetric orbital-phase sectors of planet b, confirming ARE from SPI
  at 4.37σ (99.992%). Source for the confirmed-SPI decision, the
  inferred stellar polar field B_p ≈ 2.4 kG (from the ECM spectrum,
  s=2, ν_min ≈ 500 MHz), the η★ ≈ 10^8 / R_Alf ≈ 100 R★ sub-Alfvénic
  geometry, and the **planet b magnetic field lower limit B ≥ 0.4 G** —
  the first indirect exoplanet magnetic-field measurement.
- **Stock S. et al. 2020** — *The CARMENES search for exoplanets around
  M dwarfs. Three temperate to warm super-Earths* (`2020A&A...636A.119S`,
  doi:10.1051/0004-6361/201936732). Phase 2 recommended source for the
  rotation period (68.4 ± 0.05 d, combined V-band photometry) and for
  the planet b/c/d orbits and minimum masses. Supersedes the 83 d
  Astudillo-Defru 2017 rotation period.
- **Cifuentes C. et al. 2020** — *CARMENES input catalogue of M dwarfs.
  Photometric and astrometric properties* (`2020A&A...642A.115C`,
  doi:10.1051/0004-6361/202038295). Phase 2 recommended source for the
  effective temperature (3100 K, SED fitting) and luminosity
  (0.0022 L☉, bolometric flux).
- **Schweitzer A. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Different roads to radii and masses of the target
  stars* (`2019A&A...625A..68S`, doi:10.1051/0004-6361/201834965).
  Phase 2 recommended source for the mass (0.1368 M☉) and radius
  (0.1571 R☉).
- **Astudillo-Defru N. et al. 2017** — *The HARPS search for southern
  extra-solar planets. A compact system of short-period super-Earths
  around YZ Ceti* (`2017A&A...605L..11A`, doi:10.1051/0004-6361/201731581).
  Discovery paper for the three planets; Phase 2 recommended source for
  the activity index (log R'HK = −4.71) and spectral type. Earlier
  Teff/mass/radius alternatives retained as `recommended:false`.

### Read (context / methodology, not decision-driving)

- **Moutou C. et al. 2017** — Zeeman-broadening mean field ⟨Bf⟩ ≈ 2.2 kG
  for YZ Cet (cited via Pineda & Villadsen 2023 / Trigilio 2023). The
  magnetic-field-strength Decisions row traces to this; flagged as a
  possible slow-rotator overestimate by Reiners 2022.
- **Stelzer B. et al. 2013** & **Reiners A. et al. 2018** — coronal
  X-ray (log L_X/L_bol = −4.13) and Hα (log L_Hα/L_bol = −4.32)
  activity indices, both via the Pineda & Villadsen 2023 Table 1
  compilation. Context for the activity rows.
- **Engle S.G. & Guinan E.F. 2017** — rotation-age relation giving the
  ~3.8 Gyr age (cited via Trigilio 2023). Context only; not a Phase 2
  curated value.

### Read (instrument-only, not visual-informative)

- The radio-interferometry methodology in Pineda & Villadsen 2023
  (CASA / VLA self-calibration, Stokes V dynamic spectra) and Trigilio
  2023 (uGMRT band-4 calibration, hollow-cone ARE geometry) is the
  instrument backbone of the SPI claim but contributes no direct visual
  field beyond the burst statistics already used above.

### Not read — no arXiv preprint or low-priority (~handful)

The earlier Astudillo-Defru 2017 stellar-parameter alternatives
(Teff = 3056 K, R = 0.168 R☉) are superseded by the recommended
Cifuentes/Schweitzer values and retained only in the Phase 2 DB audit
trail. Generic slow-rotator-M-dwarf radio-flare-statistics surveys
(Villadsen & Hallinan 2019, Callingham 2021) cited inside the SPI
papers are read for context but contribute no YZ-Cet-specific cfg
number. No debris-disk papers exist to read (none reported).

## Open items for follow-up

- **Planet Phase 3 syntheses.** The three planets (b, c, d) are
  produced as separate Phase 3 docs (`yz-cet-b/c/d.md`). Planet b's
  inferred ≥ 0.4 G magnetic field (Trigilio 2023) is the SPI driver and
  feeds the b synthesis directly.
- **Stellar magnetic-field geometry.** No Zeeman-Doppler-Imaging (ZDI)
  map of YZ Cet's large-scale field exists yet; both SPI papers scale
  from Proxima Cen's topology. A direct ZDI map would pin the dipole
  tilt and inclination and sharpen the radio-aurora flux-tube animation
  in the cfg. The Moutou 2017 ⟨Bf⟩ ≈ 2.2 kG should be revisited if a
  ZDI-based field becomes available (Reiners 2022 suggests it may be a
  slow-rotator overestimate).
- **Age.** No Phase 2 age array. If a future curation adds a
  gyrochronology or kinematic age, the low-confidence ~5 Gyr context
  number should be replaced.
- **Flare-rate quantification.** The eruptive-variable classification is
  qualitative; a TESS flare census would let a future cfg attach a
  quantitative `flare_rate_per_day` to the rendering.
- **SPI radio-aurora visualization fidelity.** The flux-tube footpoint
  brightening keyed to b's 2.02 d orbit with 68 d rotational modulation
  is a tie-break visual choice grounded in the hollow-cone ARE model;
  refine once a renderer can show it.

## Related

- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [yz-cet-b](yz-cet-b.md) — innermost planet; the SPI driver with an inferred ≥ 0.4 G magnetic field
- [yz-cet-c](yz-cet-c.md) — middle planet
- [yz-cet-d](yz-cet-d.md) — outermost planet
- [barnards-star](barnards-star.md) — comparison M dwarf (M4.0 Ve, near-identical Teff); contrast Barnard's old quiet near-floor activity with YZ Cet's moderate activity and SPI radio aurora
- [teegardens-star](teegardens-star.md) — comparison cooler, older, much quieter ultracool dwarf (M7 V, 96 d rotation)
- [proxima-cen](proxima-cen.md) — comparison M dwarf and the SPI analog used by both radio papers to scale YZ Cet's magnetic field
