<!-- 40 Eridani B Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 40 Eridani B — Phase 3 Synthesis

40 Eridani B (HD 26976, WD 0413−077, EG 11) is the brighter of the
two non-host components of the 40 Eri triple system at 5.01 pc — the
second-nearest white dwarf to the Sun after Sirius B and visually the
**closest** white dwarf to a naked-eye-bright companion (V = 9.53 at
83″ from the K0.5 V primary 40 Eri A). With M dwarf 40 Eri C it forms
a 230.09-year visual binary (Mason, Hartkopf & Miles 2017) whose
HST/FGS-anchored dynamical solution gives the cleanest precision-mass
measurement for any nearby field white dwarf: **M = 0.573 ± 0.018 M☉**
(Bond et al. 2017). Combined with SED-fit R = 0.01308 ± 0.00020 R☉,
log g = 7.957 ± 0.020, and Teff = 17,200 ± 110 K, 40 Eri B sits on
the CO-core, mass-radius relation almost exactly where standard
theory predicts.

The headline finding of Bond 2017 is **not** the mass, however —
it is the **thin** hydrogen envelope: the cooling track only fits
the observed (M, R, Teff, L) point if the surface H layer mass
fraction is q_H ≈ 10⁻¹⁰, four orders of magnitude below the
canonical "thick" value q_H ≈ 10⁻⁴. Bond 2017 reads this as
direct evidence that a significant fraction of DA white dwarfs
were born (or have evolved) with thin H layers, supporting the
DA → DC evolutionary scenario in which the bottom of the H
convection zone eventually meets the underlying He layer and the
star mixes into a helium-dominated atmosphere. 40 Eri B is too
hot for that mixing event today — its atmosphere is **purely
radiative** at 17,200 K — but the thin-H result fixes its
long-term fate.

**Scenario choice for NearStars: a brilliant blue-white pinpoint
white dwarf orbiting the M-dwarf 40 Eri C at a mean separation of
~33 AU, rendered with the canonical Bond 2017 parameter set.** All
20 measurement rows track the canonical literature; the only
tie-break is the chosen visual hex code for the surface tint
(`#cfd9ff`), a saturated blue-white selected for in-game visual
distinctiveness from solar-white companions. No documented
divergences, so no `## Canonical alternatives` section.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | DA2.9 | high | Gianninas, Bergeron & Ruiz 2011 (GBR11) — DA spectral-temperature subclass survey |
| `mass_msun` | 0.573 ± 0.018 | high | Bond et al. 2017 — HST/FGS astrometry of BC pair + Mason 2017 visual orbit |
| `radius_rsun` | 0.01308 ± 0.00020 | high | Bond et al. 2017 — SED-fit from BVRI + ubvy + JHK + Hipparcos parallax + atmosphere Teff |
| `teff_k` | 17200 ± 110 | high | Bond et al. 2017 — Balmer-line atmosphere fit (Tremblay & Bergeron 2009 grid) |
| `luminosity_lsun` | 0.01349 ± 0.00054 | high | Bond et al. 2017 — bolometric flux integration |
| `log_g_cgs` | 7.957 ± 0.020 | high | Bond et al. 2017 — surface gravity from atmosphere fit |
| `gravitational_redshift_km_s` | 27.82 ± 0.97 | high | Bond et al. 2017 — derived from M, R; serves as the GR-consistency cross-check on the dynamical mass |
| `cooling_age_myr` | ~122 | medium | Bond et al. 2017 §6.2 — thin-H cooling track; no formal σ stated |
| `progenitor_initial_mass_msun` | ~1.8 | medium | Bond et al. 2017 §6.2 — IFMR inversion via Salaris et al. 2009 |
| `pre_wd_lifetime_gyr` | ~1.7 | medium | Bond et al. 2017 §6.2 — main-sequence + post-MS lifetime for a 1.8 M☉ progenitor |
| `total_age_gyr` | 1.8 ± 0.5 | medium | Bond et al. 2017 §6.2 (cooling age + pre-WD lifetime); σ is a curator estimate, no paper-stated value |
| `h_envelope_mass_fraction_log_qh` | ≈ −10 | high | Bond et al. 2017 §6.1 — thin-H finding; canonical thick-H (q_H ≈ 10⁻⁴) excluded by cooling-track fit |
| `magnetic_field_upper_limit_gauss` | <250 | high | Landstreet & Bagnulo 2015 — ESPaDOnS spectropolarimetry, σ⟨Bz⟩ ≈ 85 G, no detection |
| `core_composition` | CO | high | Bond et al. 2017 §6.3 — CO-core mass-radius relation fits within errors; standard for M_init ~ 1.8 M☉ |
| `metal_pollution_dazness` | none (clean DA, no photospheric metals) | high | Bond et al. 2017 — Balmer-only atmosphere fit; Fabrika 2003 ultra-weak metal absorption attributed to circumstellar/ISM gas, not photosphere |
| `convective_envelope` | none (purely radiative) | high | Bond et al. 2017 §6.1 — atmosphere purely radiative at 17,200 K, well above the DA H-convection onset (~13,000 K) |
| `companion_a_separation_arcsec` | ~83 | high | Tokovinin MSC 2018 — wide-binary 40 Eri A↔BC geometry, no fitted Keplerian solution |
| `companion_c_orbit_period_yr` | 230.09 ± 0.68 | high | Mason, Hartkopf & Miles 2017 Table 4 — grade-1 visual orbit |
| `companion_c_orbit_eccentricity` | 0.4300 ± 0.0027 | high | Mason, Hartkopf & Miles 2017 Table 4 |
| `companion_c_orbit_a_arcsec` | 6.9310 ± 0.0500 | high | Mason, Hartkopf & Miles 2017 Table 4 — projected semi-major axis; ≈ 34.7 AU at 5.01 pc |
| `visual_surface_tint_hex_primary` | `#cfd9ff` (saturated blue-white) | medium | Tie-break: Planck-locus at 17,200 K → blue-white; cfg picks a saturated tint over a near-white reference for visual distinctiveness from solar-white companions |
| `stellar_color_temp_k` | 17200 | high | Equal to Teff for a clean radiative DA photosphere |
| `visual_apparent_diameter_arcsec_at_1au` | 25.09 | high | Derived geometric: 2 R★ / a × (180·3600/π) with R★ = 0.01308 R☉ = 9.10×10⁶ m (~1.43 R⊕) |

## Surface synthesis

The photosphere of 40 Eri B is a **purely radiative** layer at
Teff = 17,200 K. There is no convection zone in the visible
atmosphere — Bond 2017 §6.1 makes this explicit, and the value
sits well above the canonical DA H-convection onset near
13,000 K. Granulation, supergranulation, sunspots, plages, and
all of the classical FGK-stellar surface features are
**absent**. The visible disk is a featureless, nearly uniform
black-body emitter modulated only by surface gravity broadening
of the H Balmer lines.

Even spectropolarimetric searches for surface magnetic structure
have come up empty: Landstreet & Bagnulo 2015 used ESPaDOnS at
the CFHT with a novel broad-band circular-polarimetry technique
to push the upper limit on any organized field to roughly 250 G,
with mean noise σ⟨Bz⟩ ≈ 85 G — "the smallest standard error of
field measurement ever obtained for a white dwarf" at the time
of publication. An earlier Fabrika et al. 2003 BSAO programme
had reported tentative variability with semi-amplitude
~4–5 kG and two candidate rotation periods (2h 25m and 5h 17m),
but Fabrika himself noted the periods could not be "firmly"
determined; the more sensitive Landstreet & Bagnulo 2015
non-detection effectively refutes the kilogauss-level claim.
For NearStars rendering this means **no animated magnetic
features** — no Zeeman tomography map, no spot pattern, no
aurorae.

The surface gravity log g = 7.957 ± 0.020 (cgs) translates to a
photon-escape velocity v_esc ≈ 4,250 km/s and a gravitational
redshift contribution to the radial velocity of 27.82 ± 0.97 km/s
(Bond 2017). This redshift serves as a precision GR
cross-check: an independent ESPaDOnS-derived spectroscopic
gravitational redshift is consistent within 1σ, confirming
that the dynamical mass and the SED radius are mutually
self-consistent. For the KSP cfg this means the body's gravity
and its visual size faithfully scale with the canonical
mass-radius relation for a CO-core WD with a thin H envelope.

## Atmosphere synthesis

40 Eri B has a **pure-hydrogen** photosphere with no detectable
metal pollution. The Balmer-only spectroscopic fit of Bond 2017
adopts the Tremblay & Bergeron 2009 LTE pure-H model grid; the
clean Balmer profiles set Teff and log g with high precision and
leave no residual evidence of metal absorption beyond
Fabrika 2003's ultra-weak features, which Fabrika attributed to
circumstellar or interstellar gas accreting from the ISM and
from a putative ~10⁻¹⁹ M☉/yr inflow from the dM4e companion
40 Eri C — not to photospheric pollution. 40 Eri B is therefore
not a DAZ; it is a clean DA. No metal absorption layer is
needed in the KSP cfg.

Spectral evolution is the defining long-term story. Bond 2017
§6.1 notes that the H layer is so thin (q_H ≈ 10⁻¹⁰) that as
the star continues to cool, the bottom of the H convection zone
that develops at lower Teff will eventually reach the underlying
helium envelope. The two layers will mix and 40 Eri B will
**transition from a DA into a helium-atmosphere DC** white dwarf.
This is not imminent — 40 Eri B is presently DA2.9 at 17,200 K
and cooling slowly; the DA → DC mixing event happens at much
lower Teff (typically below 6,000 K for thin-H DAs). On the
canonical NearStars temporal scale (in-game years) this
transition is irrelevant; the cfg renders 40 Eri B in its
current DA2.9 state.

There is no chromosphere, no transition region, no corona. The
indicators that calibrate activity on FGK and M dwarfs —
log R'HK, Hα emission, X-ray L_X cycles — have no physical
meaning for a radiative-atmosphere white dwarf. The Phase 2
DB correctly records these fields as N/A. The XUV emission is
limited to the thermal Wien tail of the 17,200 K black-body, and
even that is below the threshold for chemical effects on any
hypothetical orbiting body, since the bolometric luminosity
itself is only 0.0135 L☉.

## Rotation & spin synthesis

40 Eri B's rotation is **not well constrained**. There is no
photometric variability that survives modern monitoring; there
is no detectable Zeeman polarization that would let
spectropolarimetric Doppler imaging recover a period (Landstreet
& Bagnulo 2015 effectively refute the kilogauss field that
Fabrika 2003's variability claim would have required); and
sub-projected v sin i upper limits from broadened Balmer
profiles are model-degenerate with the pressure broadening at
17,200 K. The Phase 2 DB records **no rotation entry** for
40 Eri B; the Phase 3 synthesis carries that null forward.

For KSP cfg purposes this is not a missing field — it is an
explicit absence. The body cfg can pick any rotation rate
consistent with white-dwarf physics; the conventional choice is
a slow rotation (P_rot of order hours to days) inherited from
the AGB progenitor's spun-down core, with the proviso that the
AGB common-envelope or wind-loss phase may have transferred
angular momentum to the M-dwarf companion 40 Eri C (Bond 2017
§6.2 cites Fuhrmann 2014 for the AGB-spin-up scenario on C).
For visual rendering at NearStars scale, the rotation rate is
imperceptible — the body is a point source even at high zoom.

40 Eri B is **outside** the DAV ZZ-Ceti instability strip. The
empirical strip for DA white dwarfs lies between roughly
10,500 K and 12,500 K (Gianninas et al. 2011 and references
therein); 17,200 K places 40 Eri B well above the blue edge.
There are no observed pulsations and none are expected; the
renderer therefore does not animate any surface brightness
oscillation.

## Visual styling

In the NearStars renderer, 40 Eri B is portrayed as a brilliant
**blue-white pinpoint** — saturated cyan-tinged white encoded
as `#cfd9ff` against the canonical solar-white. At 17,200 K the
Planck-locus chromaticity sits in the blue-white region of the
Kelvin scale (between Vega's ~9,600 K and the hottest O-stars'
~30,000+ K); rendering it as pure white would lose the visual
distinction from the K-dwarf 40 Eri A and the M-dwarf 40 Eri C
when the three components are framed together. The tie-break
defaults to the saturated tint per the interesting-first rule.

At 5.01 pc viewed from Earth the apparent magnitude is V = 9.53 —
naked-eye-invisible without a telescope despite the proximity,
because the white dwarf's tiny radius (0.013 R☉, ~1.4 R⊕) caps
the bolometric output at 0.0135 L☉. The body cfg renders the
star at its physical scale; at 1 AU separation the apparent
angular diameter is ~25″ — well below the ~30′ disk that the
Sun subtends from Earth, so even at close in-system fly-by
distances 40 Eri B presents as a small bright disk rather than
a resolved sphere.

The binary partner 40 Eri C orbits at a mean separation of
~34.7 AU (Mason 2017 a = 6.93″ × 5.01 pc), ranging from
~19.8 AU at periastron (e = 0.43) to ~49.6 AU at apastron over
the 230-year orbit. From the cfg viewpoint of a body orbiting
40 Eri B, the M-dwarf companion 40 Eri C appears as a dim red
point of variable brightness (DY Eri is a flare star) at
arcminute-scale separation. The wider companion 40 Eri A
sits at ~83″ (~415 AU at 5.01 pc), unbound on Kopernicus orbit
timescales but visible as a bright orange K-dwarf "second
sun" — V = 4.43, comparable to a magnitude-1 star in the night
sky when seen from a hypothetical 40 Eri B planet.

The triple is best appreciated in a system-wide view: A as a
bright orange disk, B as a blue-white pinpoint, C as a dimmer
red flare star — three different stellar evolutionary endpoints
arranged in a single 5-pc field. The Visual styling cfg should
preserve this colour triad rather than blending B toward
neutral white.

## Bibliography

### Read (decision-driving)

- **Bond H. E., Bergeron P. & Bédard A. 2017** — *Astrophysical
  Implications of a New Dynamical Mass for the Nearby White Dwarf 40
  Eridani B*, ApJ 848, 16 (`2017ApJ...848...16B`,
  arXiv:1709.00478, DOI 10.3847/1538-4357/aa8a63). HST/FGS
  astrometry of the BC pair anchored on the Mason 2017 visual
  orbit; pure-H model atmosphere Balmer-line fit; SED fit to
  BVRI + ubvy + JHK + Hipparcos parallax. Headline parameters:
  M = 0.573 ± 0.018 M☉, R = 0.01308 ± 0.00020 R☉,
  Teff = 17,200 ± 110 K, log g = 7.957 ± 0.020,
  L = 0.01349 ± 0.00054 L☉, gravitational redshift
  27.82 ± 0.97 km/s. §6.1 thin-H envelope (q_H ≈ 10⁻¹⁰)
  with purely radiative atmosphere; §6.2 IFMR-derived
  progenitor M_init ≈ 1.8 M☉, pre-WD lifetime 1.7 Gyr,
  total age 1.8 Gyr; §6.3 CO-core MRR consistency check
  across four nearby WDs; §6.4 conclusion that thin-H DAs
  are common.

- **Landstreet J. D. & Bagnulo S. 2015** — *A novel and
  sensitive method for measuring very weak magnetic fields
  of DA white dwarfs — A search for a magnetic field at the
  250 G level in 40 Eridani B*, A&A 580, A120
  (`2015A&A...580A.120L`, DOI 10.1051/0004-6361/201526434).
  ESPaDOnS broad-band circular polarimetry at CFHT;
  individual ⟨Bz⟩ measurements consistent with zero within
  σ ≈ 80–90 G; concludes a probable upper limit ⟨Bz⟩ ≲ 250 G,
  noting the noise is "the smallest standard error of field
  measurement ever obtained for a white dwarf". This refutes
  the Fabrika 2003 kilogauss-variability claim.

- **Mason B. D., Hartkopf W. I. & Miles K. N. 2017** —
  *Binary Star Orbits V. The Nearby White Dwarf — Red Dwarf
  Pair 40 Eri BC*, AJ 154, 200 (`2017AJ....154..200M`,
  arXiv:1707.03635, DOI 10.3847/1538-3881/aa803e). Re-derived
  visual orbit incorporating speckle interferometry through
  2016; grade-1 definitive solution Table 4: P = 230.09 ±
  0.68 yr, T = 1847.60 ± 1.10, e = 0.4300 ± 0.0027,
  a = 6.9310 ± 0.0500″, i = 107.53° ± 0.29°, ω = 318.20° ±
  1.10°, Ω = 151.44° ± 0.12°. Dynamical masses M_B = 0.575 ±
  0.018 M☉, M_C = 0.2041 ± 0.0064 M☉ — consistent with
  Bond 2017 within errors.

- **Gianninas A., Bergeron P. & Ruiz M. T. 2011** —
  *A Spectroscopic Survey and Analysis of Bright,
  Hydrogen-Rich White Dwarfs*, ApJ 743, 138
  (`2011ApJ...743..138G`, arXiv:1109.3171). Definitive DA
  spectral-temperature index survey adopting the DA1–DA9
  Sion classification; 40 Eri B (WD 0413−077) carries the
  DA2.9 subtype in this work, the canonical post-2011 value
  used by Bond 2017 and subsequent literature.

### Read (context / methodology)

- **Tremblay P.-E. & Bergeron P. 2009** — *Spectroscopic
  Analysis of DA White Dwarfs: Stark Broadening of Hydrogen
  Lines Including Nonideal Effects*, ApJ 696, 1755
  (`2009ApJ...696.1755T`). The pure-H model-atmosphere grid
  Bond 2017 adopts for the Balmer-line Teff and log g fit.

- **Salaris M. et al. 2009** — *Semi-empirical White Dwarf
  Initial–Final Mass Relations: A Thorough Analysis of
  Systematic Uncertainties due to Stellar Evolution Models*,
  ApJ 692, 1013 (`2009ApJ...692.1013S`). The IFMR relation
  M_final = 0.134 M_init + 0.331 that Bond 2017 §6.2 inverts
  to recover M_init ≈ 1.8 M☉ from the measured M_final =
  0.573 M☉.

- **Fabrika S. N. et al. 2003** — *Looking for magnetic
  fields in white dwarfs. The B and M components of 40 Eri*,
  BSAO 55, 17 (arXiv:astro-ph/0006050). Earlier kilogauss
  variability claim (B_max ~ 4–5 kG; candidate periods 2h25m
  and 5h17m); the authors note no firm single period could
  be determined. Effectively superseded by Landstreet &
  Bagnulo 2015's null detection.

- **Tokovinin A. 2018** — *The Updated Multiple Star Catalog*,
  ApJS 235, 6 (`2018ApJS..235....6T`). MSC entry for 40 Eri
  records the A↔BC outer pair at ~83″ separation, ~8,000-yr
  approximate period, no fitted Keplerian solution.

### Read (instrument-only / context)

- **Mason B. D. et al. 2021** — *Speckle Interferometry at
  the US Naval Observatory. XXIV*, AJ 162, 53
  (`2021AJ....162...53M`, DOI 10.3847/1538-3881/abfaa2).
  Newer BC orbit fit: P = 233.20 ± 0.65 yr, e = 0.4141 ±
  0.0072, a = 6.88788 ± 0.03488″. Listed as the current
  Sixth Orbit Catalog entry; Phase 3 cfg keeps Mason 2017
  for self-consistency with Bond 2017's mass derivation, and
  the 2021 update is logged as a follow-up item below.

- **Holberg J. B. et al. 2013** — *Where are all the
  Sirius-like binary systems?*, MNRAS 435, 2077
  (`2013MNRAS.435.2077H`). Sets 40 Eri BC in the broader
  population of nearby Sirius-like (FGK + WD) systems for
  context, but does not re-measure 40 Eri B parameters.

### Not read — no decision impact (~12 papers)

Pre-Bond legacy parallax / orbit notes (Heintz 1974, Wegner 1974
spectroscopic redshift, McCook & Sion 1999 WD catalogue
classifications), DA spectropolarimetric surveys that include
40 Eri B as a non-detection without separate measurement
(Kawka & Vennes 2007, Aznar Cuadrado 2004), and recent
catalogue / Gaia DR3 cross-match papers that quote Bond 2017
without independent measurement. The full filtered list is
captured implicitly via the Phase 2 meta_notes citation chain;
none would change the Decisions table.

## Open items for follow-up

- **Mason 2021 orbit update.** Mason et al. 2021
  (`2021AJ....162...53M`) supersedes the Mason 2017 visual
  orbit with P = 233.20 ± 0.65 yr, e = 0.4141 ± 0.0072,
  a = 6.88788 ± 0.03488″. A future reconciliation pass should
  adopt the 2021 elements and re-derive the dynamical mass
  with the same Bond 2017 HST/FGS astrometry; the resulting
  mass should differ from 0.573 M☉ by less than the current
  ±0.018 M☉ uncertainty, but the orbit period in particular
  matters for Principia long-period n-body integrations.

- **DA → DC transition Teff threshold.** Bond 2017 §6.1
  predicts mixing of the thin H layer into the He envelope at
  some Teff well below 17,200 K but does not quote a specific
  transition temperature for q_H ≈ 10⁻¹⁰. A future cfg variant
  could render the future DC state by interpolating between
  Bergeron-Wesemael cooling tracks; the present cfg uses only
  the current DA2.9 state.

- **ZZ Ceti pulsation status.** 40 Eri B is well outside the
  DAV instability strip (10,500–12,500 K versus 17,200 K) and
  no oscillations are observed. If future TESS or CHEOPS
  long-baseline monitoring detected sub-mmag photometric
  variability, the cfg might gain a low-amplitude pulsation
  effect; presently none is recorded.

- **Astrometric Gaia DR4 mass refinement.** Gaia DR4 (expected
  late-decade release) will deliver multi-epoch astrometry of
  the BC pair with sub-microarcsecond per-epoch precision;
  the 0.573 ± 0.018 M☉ dynamical mass may be tightened by an
  order of magnitude.

- **Per-Phase-2-DB σ on total age.** Bond 2017 reports
  "~1.8 Gyr" without a paper-stated uncertainty; the Phase 2
  DB carries σ = 0.5 Gyr as a curator estimate. The Phase 3
  Decisions row mirrors that estimate; a reconciliation pass
  could either retain (as documented) or replace with a
  paper-cited σ if a follow-up cooling-track + IFMR
  Monte-Carlo analysis is published.

## Related

- [40-eridani-a](40-eridani-a.md) — K0.5 V primary at ~83″ (~415 AU); host of the refuted "Vulcan" planet (Burrows et al. 2024)
- [40-eridani-c](40-eridani-c.md) — M4.5 Ve flare star DY Eri; bound to 40 Eri B with 230-yr orbit
- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — Kepler→ICRS conversion for the BC visual orbit
