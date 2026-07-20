<!-- 40 Eridani C Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 40 Eridani C — Phase 3 Synthesis

40 Eridani C (GJ 166 C, HIP 19849 C, the variable star DY Eri) is the
M4.5 Ve flare-star member of the 40 Eri triple system. It lies 5.01 pc
from the Sun and orbits the DA2.9 white dwarf 40 Eri B with a 230.09-yr
visual-spectroscopic period (Mason, Hartkopf & Miles 2017, e = 0.4300,
a = 6.93″, mean separation ≈ 33 AU). The inner BC pair in turn moves
around the K0.5 V primary 40 Eri A at roughly 83″ angular separation —
an unresolved ~8000-yr outer orbit (Tokovinin MSC 2018). With V = 11.17
and visual variability of a few tenths of a magnitude, C is one of the
nearest optically active M dwarfs and a classic flare-star target. Its
DY Eri variable-star designation reflects sustained Hα emission and
photometric flaring rather than a single-epoch eruption.

The Phase 2 anchors verified 2026-05-29 fix C tightly: a binary-orbit
dynamical mass M = 0.198 ± 0.0042 M☉ (Mason 2021), Mann et al. 2015
spectroscopic Table 5 radius R = 0.274 ± 0.011 R☉ and effective
temperature T_eff = 3167 ± 61 K, Cifuentes 2020 CARMENES bolometric
luminosity L = (6.51 ± 0.13) × 10⁻³ L☉, Mann 2015 [Fe/H] = -0.21 ± 0.08,
and a system-coeval age 1.8 ± 0.5 Gyr from Bond et al. 2017's IFMR
analysis of the WD progenitor. Two activity-related quantities cited
in older literature — Shan et al. 2024's P_rot = 8.56 d and the
multi-survey Hα equivalent-width range pEW ≈ -2 to -4 Å — are recorded
in the DB `meta_notes` but **not** as recommended measurements. Shan
2024 itself flags the 8.56 d period with quality D (debated; 27 of 166
CARMENES periods in that paper are debated). Hα has no single-paper
anchor.

**Scenario choice for NearStars: an active red M4.5 V flare star,
illuminating a hypothetical nearby observer with deep red light and
animated by H-alpha flaring at the cfg cadence appropriate for a
DY Eri-class variable.** No planets are curated (HD 26965 b around the
primary A was refuted by Burrows 2024 and never extended to C in any
case). 13 cfg picks track the canonical parameter set; 4 tie-break
picks involve the visual hex tint and binary-event geometry as seen
from a hypothetical C-orbiting observer.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M4.5 Ve | high | Gray & Garrison community canonical; SIMBAD M4.5Ve. Mann 2015 Table 5 lists M4.7 (within MK scatter); the e suffix marks chromospheric emission consistent with DY Eri flare activity |
| `mass_msun` | 0.198 ± 0.0042 | high | Mason et al. 2021 (`2021AJ....162...53M`) — dynamical mass from the Izmailov 2019 BC orbit (P = 233.20 yr, e = 0.4141) + Gaia eDR3 parallax; supersedes the prior Mason 2017 value (0.2041, tied to the old 230.09-yr orbit and a Heintz 1974 mass-ratio split). Mason 2021 now gives M_C directly, so the Heintz ratio is no longer needed |
| `radius_rsun` | 0.274 ± 0.011 | high | Mann et al. 2015 Table 5 'Gl 166 C' row — M_K-band radius relation calibrated against interferometric M-dwarf sample + BT-Settl atmosphere model fit |
| `teff_k` | 3167 ± 61 | high | Mann et al. 2015 Table 5 — low-resolution SNIFS optical + SpeX NIR spectra fit to BT-Settl atmosphere grid |
| `luminosity_lsun` | 6.51e-3 ± 0.13e-3 | high | Cifuentes et al. 2020 CARMENES catalog row Karmn J04153-076 (VizieR J/A+A/642/A115); multi-band SED integration with Gaia DR2 distance |
| `metallicity_fe_h_dex` | -0.21 ± 0.08 | high | Mann et al. 2015 Table 5 — Mann 2013a low-resolution spectroscopic [Fe/H] calibration vs solar-type companions |
| `age_gyr` | 1.8 ± 0.5 | medium | Bond et al. 2017 §6.2 — system-coeval; B progenitor IFMR yields M_initial ≈ 1.8 M☉ and pre-WD lifetime 1.7 Gyr + 0.12 Gyr WD cooling ≈ 1.8 Gyr total. Uncertainty curator-estimated |
| `rotation_period_days` | n/a (Shan 2024 8.56 d flagged "debated") | low | Shan et al. 2024 (CARMENES VII) lists P_rot = 8.56 d with quality flag D; recorded in DB meta_notes only, not as recommended measurement. Open item |
| `activity_log_rhk` | n/a (M-dwarf regime; H-alpha used instead) | low | Ca II H&K log R'HK is not a clean activity tracer for fully-convective M4–M5 dwarfs (saturated chromospheric flux); Hα equivalent width is the appropriate proxy |
| `activity_h_alpha_pew_a` | -2 to -4 (range across surveys) | medium | Multi-survey: CARMENES (Schöfer 2019), Newton 2017, Reiners 2018 sample H-alpha pEW for GJ 166 C in this range; no single-paper anchor. Variable star DY Eri — value fluctuates with activity cycle |
| `activity_cycle_years` | n/a | low | No documented chromospheric cycle for 40 Eri C; multi-decade ASAS-SN / TESS time series have not yet been published with cycle constraints |
| `x_ray_log_lx_cgs_qualitative` | bright per active M4.5 V expectation | low | ROSAT All-Sky Survey detects the BC pair but blends with B's photospheric soft X-ray contribution; no isolated 40 Eri C log L_X published. Open item |
| `flare_rate_per_day` | n/a (variable star DY Eri designation; rate not quantified) | low | Optical photometric variability and Hα emission confirm flare activity; survey-derived quantitative rate not yet published in our bibliography. Open item |
| `agb_mass_transfer_spinup_narrative` | true | medium | Bond et al. 2017 §6.2 explicitly cites Fuhrmann et al. 2014 — C may have been spun up by accretion during the AGB phase of B's progenitor. Narrative point, not a single cfg field |
| `visual_surface_tint_hex_primary` | `#d97f4a` (warm red-orange) | low | Tie-break: interesting-first. Planck-locus blackbody at 3167 K + Hα emission tinting pushes the perceived color toward saturated red-orange over generic dull-red. Documented in Visual styling |
| `stellar_color_temp_k` | 3167 | high | Derived from Teff |
| `visual_companion_event_b_visible_as_blue_point` | true | medium | BC orbit mean separation ≈ 33 AU (Mason 2017). B at apparent V ≈ -13 from C (M_V ≈ 11.0 + distance modulus −24), comparable to full-Moon brightness, distinctly blue-white given B's T_eff ≈ 17,200 K. Tie-break for the rendering threshold |
| `visual_companion_event_a_visible_as_orange_distant_point` | true | medium | A-BC mean separation ≈ 2000 AU. A at apparent V ≈ -9 from C (M_V ≈ 5.9 + distance modulus −15), orange tint from A's K0.5 V T_eff ≈ 5126 K. Tie-break for the rendering threshold |
| `habitable_zone_inner_au` | 0.067 (derived, conservative) | medium | Kopparapu et al. 2014 M-dwarf HZ inner boundary scaled by √(L / L☉) = √(6.51e-3) for the runaway-greenhouse edge. No curated planets; context value |
| `habitable_zone_outer_au` | 0.21 (derived) | medium | Kopparapu et al. 2014 M-dwarf HZ outer boundary (maximum greenhouse) scaled by the same factor. Context value |

## Surface synthesis

The photosphere of 40 Eridani C is the cool red surface of a late-M
main-sequence dwarf — T_eff = 3167 K places it firmly in the partially
convective transition regime where the radiative core is small or
vanishing. At M = 0.2041 M☉ the star sits just above the fully-
convective limit (≈ 0.35 M☉ for hydrogen-burning main-sequence stars);
modern stellar-interior models (Chabrier & Baraffe 1997, Baraffe 2015)
predict that a thin radiative core may persist but most of the
envelope's heat transport is convective. This convective regime is
the proximate driver of the strong magnetic dynamo and the persistent
H-alpha emission that gives C its DY Eri variable designation.

The visible disk shows the canonical late-M molecular-band spectrum:
strong TiO bands in the optical (heaviest near 705 nm, the γ-band
heads dominating C's red-orange appearance), VO absorption in the
yellow, and FeH features in the near-IR. Continuum opacity from H⁻
peaks in the H-band region. The integrated Planck-locus color at
3167 K is in the warm red-orange region of CIE chromaticity (xy ≈
0.55, 0.40); H-alpha emission contributes a narrow red boost at 656 nm.

Mann et al. 2015 specifically flag Gl 166 C as one of three stars
where the BT-Settl model atmosphere disagrees with their empirical
T_eff / R determination by more than the typical floor (Mann 2015
§5.4, around the discussion of Figure 16). The other two are PM
I10430-0912 and EQ Peg B (Gl 896 B). Why this matters for Phase 3:
the radius and T_eff we adopt are paper-measured (M_K relation +
F_bol integration), not model-fit; the Mann 2015 Table 7 Dartmouth
model fit would give R = 0.242 R☉ and T_eff = 3362 K — both ≈ 11–13%
discrepant from the empirical row, which is exactly the M-dwarf
model bias the Mann paper documents. The DB Phase 2 recommended
entries are the empirical Table 5 row.

Spot coverage is large and animated, as expected for an active M4.5
V. Mann 2015 measures Hα equivalent-width emission across the 178-star
sample but reports the GJ 166 C value as a single epoch only; the
multi-survey scatter is pEW ≈ -2 to -4 Å (Schöfer 2019, Newton 2017,
Reiners 2018) — implying tens of percent variability between epochs.
A hypothetical observer near C's habitable zone would see large
starspots covering 10-30% of the disk during activity maxima, with
plage-bright active regions and the occasional kilo-Gauss-scale
flare flux outburst visible as a localized brightening of a few
percent at optical wavelengths (canonical for M4.5 V flare stars,
e.g. EV Lac, AD Leo).

The slight metal-poor [Fe/H] = -0.21 has only a modest effect on the
SED — the BT-Settl grid at [Fe/H] = -0.2 vs solar predicts a Teff
shift of ~30 K equivalent reddening, well within the curated 61 K
uncertainty. C's [Fe/H] is consistent within 1.5 sigma with the 40
Eri A value (-0.31, Sousa 2008), supporting system-coeval origin.

## Atmosphere synthesis

40 Eri C hosts a fully chromospherically active M-dwarf atmosphere
typical of late-M flare stars. The chromosphere is filled with Hα,
Ca II H&K, Hβ, He I D3, and a wide range of UV emission lines (Mg II
h&k visible in the GALEX FUV, Lyα accessible to HST/STIS). The DY
Eri variable designation reflects multi-decade ground-based monitoring
showing photometric flares and persistent Hα emission across the
chromospheric activity cycle.

X-ray emission is bright but quantitatively under-constrained for
this synthesis. The ROSAT All-Sky Survey detected the BC pair but
the 0.1–2.4 keV soft component blends contributions from C's
chromospheric corona and B's photospheric thermal X-rays. A
quantitative log L_X / L_bol for 40 Eri C alone is not currently in
our bibliography; the qualitative expectation for an M4.5 V at this
age is log L_X / L_bol ≈ -3 to -4 (typical M-dwarf activity sequence,
e.g. Wright et al. 2011, Schmitt & Liefke 2004), with cycle amplitude
factor ~few. Flare X-ray peaks an order of magnitude above the
quiescent level. The Open items list flags isolated-component X-ray
measurement as a follow-up target.

The transition region produces a Lyman-α continuum + Lyα line typical
of M4–M5 active stars; surface flux is several × 10⁵ erg s⁻¹ cm⁻²
quiescent, with flare enhancement up to two orders of magnitude.
Integrated XUV (10–100 nm) luminosity over Gyr timescales is
significant for any potential planet — France et al. 2016 (MUSCLES)
finds that active M4–M5 dwarfs deliver Earth-comparable cumulative
XUV doses despite their lower bolometric luminosity, because their
quiescent XUV / L_bol ratio is ~10⁴ × the solar value. No planets are
curated around C; this regime informs only the system-level activity
context.

C has no surface to constrain via atmosphere-photochemistry coupling
(it's a star). The "atmosphere" here refers to the chromosphere –
transition region – corona structure, animated by the magnetic
dynamo. The cfg implication: any future planet candidate around C
would inherit a strong XUV environment from the chromospheric model,
and reentry-effect renderers should saturate red wavelengths to
reflect the Hα-dominated optical spectrum.

## Rotation & spin synthesis

The rotation period is genuinely uncertain. Shan et al. 2024 (CARMENES
VII) report a CARMENES activity-indicator time-series period of 8.56 d
for Karmn J04153-076 = GJ 166 C, but classify the detection with
quality flag D ("debated"; per Sect. 4 of the paper, 27 of 166
detected periods are debated and 68 are provisional). The Phase 2
DB records this in `meta_notes` only — there is no `rotation_measurements`
recommended:true entry. An earlier 2026-05-27 working-note
attribution to "Kemmer 2025 ~137 d" was retracted on cross-check:
Y. Shan is first author of the actual paper (Kemmer is the 22nd
of 47 co-authors), the year is 2024 not 2025, and the period differs
by ~16×.

For NearStars purposes, the **cfg rotation period field for C is
N/A**. Downstream cfg writers should leave the period unset and
mark it as an explicit gap, or use an interesting-first placeholder
(e.g. 9 d) with a clear cfg-level note that this is a tie-break
within Shan 2024's allowed window. Independent verification — via
TESS short-cadence photometry, RV modulation phase-folding, or
ZDI spectropolarimetry — would convert the entry from `n/a` to
`recommended:false` then to `recommended:true` in a future pass.

A separate Phase 3 narrative point: 40 Eri C's rotation state may
preserve a fossil signature of mass transfer from B's progenitor.
Bond et al. 2017 §6.2 explicitly cites Fuhrmann et al. 2014 — the
suggestion that C "may have been spun up to a higher rotational
velocity by accretion during the AGB phase of [40 Eri] B". The
40 Eri B progenitor had M_initial ≈ 1.8 M☉ and ascended the AGB
before losing its envelope; some fraction of the lost envelope
likely missed the WD remnant and could have been captured by C
sitting at ≈ 33 AU. If a debated short-period rotation (8.56 d or
similar) is eventually confirmed, this would qualitatively support
the AGB-spin-up scenario. The cfg should encode this as a narrative
hint rather than a quantitative rotation-rate prediction.

Obliquity is unconstrained; for visual rendering NearStars adopts a
randomly-oriented spin axis, plausibly tilted ~30° to the BC orbital
plane (analogous to other long-lived MS+WD binaries where tidal
synchronization at 33 AU separation is negligible).

## Visual styling

In the NearStars renderer, 40 Eridani C is portrayed as a small,
warm red-orange M4.5 V flare star — Planck-locus blackbody at 3167 K
gives a base color near `#d97f4a` (warm red-orange, CIE xy ≈ 0.55,
0.40); the Hα 656 nm emission pushes the perceived tint slightly
further toward saturated red. The tie-break Confidence: low call is
*interesting-first*: a range of reasonable hex values lie within the
3167 K Planck locus envelope, and the saturated red-orange option
makes C visually distinct from the K0.5 V primary A (warm yellow-
orange) and the blue-white WD B in mixed system renders.

At 5.01 pc viewed from Earth, V = 11.17 places 40 Eri C below the
naked-eye limit but well within reach of small telescopes. From a
hypothetical observer at C's habitable-zone distance (≈ 0.1 AU based
on L = 6.51e-3 L☉), the star fills an angular diameter of ~1.5°
(2 R★ / a) — about three times the Sun's apparent size from Earth.
Disk features include large starspots (10–30% coverage during
activity maxima), occasional flare brightenings at the few-percent
optical level, and a strong red-orange limb darkening characteristic
of the molecular-band atmosphere.

The companion B at 33 AU mean separation (BC orbit Mason 2017, e =
0.4300 → periastron ~19 AU, apastron ~47 AU) appears as a brilliant
blue-white point of extraordinary brightness. With B's M_V ≈ 11.0
(DA WD, T_eff ≈ 17,200 K), from a C-orbiting observer at 33 AU
B's apparent magnitude is roughly V ≈ -13 (mag = M_V + 5·log₁₀(33 AU
/ 10 pc) ≈ 11.0 − 24). Comparable to the full Moon at Earth in
brightness — a small, intense blue-white point overwhelmingly
dominant against C's red illumination at conjunctions and still
prominent at apastron (V ≈ -12). The orbital motion swings B
visibly across the C-sky over decade-to-century timescales.

The primary A at ~2000 AU mean separation appears as a much fainter
but still naked-eye orange "distant sun" — A's M_V ≈ 5.9 with the
distance modulus to 2000 AU gives apparent V ≈ -9 (mag = 5.9 − 15),
still vastly brighter than any planet seen from Earth but on a
strikingly different scale from B. The K0.5 V T_eff ≈ 5126 K
provides a clear orange tint. The triple appears in C's sky as:
nearby C-disk illumination (the dominant red light source), a
near-stellar blue-white searchlight (B), and a more distant orange
point-source A — three light sources on widely different intensity
and time scales (B moves visibly over decades, A is effectively
fixed on human timescales given the ~8000-yr A-BC orbit).

Flare events drive Firefly-cfg-side plasma color choices: an active
M4.5 V flare-star produces optical flare spectra dominated by Hα +
Hβ + Ca II emission, biasing reentry plasma toward saturated red/
pink palettes during peak flare flux. The exact palette assembly
is firefly-cfg-skill territory (see the periodic table of plasma
colors in `firefly-cfg/`) but the Phase 3 hint here is: **prefer
strong red over generic white plasma effects in C's vicinity**, with
optional Hα-red flare-event accent triggered on a DY Eri-class
variability cadence (sub-hour rise, hours-decay flare profile).

Starspots, faculae, and prominences are rendered at active-M-dwarf
scale during the (uncertain) activity cycle, with the cycle phase
deferred until a paper-confirmed cycle period exists.

## Bibliography

### Read (decision-driving)

- **Mason B. D., Hartkopf W. I., Miles K. N. 2017** — *Binary Star
  Orbits. V. The Nearby White Dwarf/Red Dwarf Pair 40 Eri BC*,
  AJ 154, 200 (`2017AJ....154..200M`, [arXiv:1707.03635](https://arxiv.org/abs/1707.03635),
  DOI 10.3847/1538-3881/aa803e). Updated 230.09-yr BC visual-
  spectroscopic orbit; mass sum 0.776 ± 0.024 M☉, e = 0.4300,
  a = 6.93″. With Heintz 1974 mass ratio gives M_C = 0.2041 ±
  0.0064 M☉. **Primary anchor for the C dynamical mass.**
- **Mann A. W., Feiden G. A., Gaidos E., Boyajian T., von Braun K.
  2015** — *How to Constrain Your M Dwarf: Measuring Effective
  Temperature, Bolometric Luminosity, Mass, and Radius*, ApJ 804, 64
  (`2015ApJ...804...64M`, [arXiv:1501.01635](https://arxiv.org/abs/1501.01635), DOI 10.1088/0004-637X/804/1/64).
  Empirical M-dwarf calibration; Table 5 'Gl 166 C' row gives
  R = 0.274 ± 0.011 R☉, T_eff = 3167 ± 61 K, [Fe/H] = -0.21 ± 0.08,
  and Hα EW. **Primary anchor for radius / T_eff / [Fe/H].** Table 7
  Dartmouth model fit (R = 0.242, T_eff = 3362) is preserved as a
  documented sample-level model bias datapoint (§5.4 + Figure 16).
- **Cifuentes C., Caballero J. A., Cortés-Contreras M. et al. 2020** —
  *CARMENES input catalogue of M dwarfs. V. Luminosities, colours,
  and spectral energy distributions*, A&A 642, A115 (`2020A&A...642A.115C`,
  [arXiv:2007.15077](https://arxiv.org/abs/2007.15077), DOI 10.1051/0004-6361/202038295). Multi-band SED
  integration for the CARMENES M-dwarf sample; Karmn J04153-076 =
  GJ 166 C entry (VizieR J/A+A/642/A115) gives L = (6.51 ± 0.13) ×
  10⁻³ L☉. **Primary anchor for luminosity.**
- **Bond H. E., Bergeron P., Bédard A. 2017** — *The aged
  Astrophysical Implications of a New Dynamical Mass for the Nearby
  White Dwarf 40 Eridani B*, ApJ 848, 16
  (`2017ApJ...848...16B`, [arXiv:1709.00478](https://arxiv.org/abs/1709.00478), DOI 10.3847/1538-4357/aa8a63).
  HST/COS UV spectroscopy of 40 Eri B; full system reanalysis. §6.2
  IFMR (Salaris et al. 2009, M_final = 0.134 M_initial + 0.331) implies M_progenitor ≈ 1.8 M☉ for B, giving
  system-coeval total age ≈ 1.8 Gyr. Same section cites Fuhrmann
  et al. 2014 on the AGB-mass-transfer spin-up scenario for C.
  **Primary anchor for age + AGB-spin-up narrative.**
- **Shan Y., Reiners A., Fabbian D. et al. 2024** — *The CARMENES
  search for exoplanets around M dwarfs. VII. Photospheric rotation
  periods from the activity time series of 166 M dwarfs*, A&A 684, A9
  (`2024A&A...684A...9S`, [arXiv:2401.09550](https://arxiv.org/abs/2401.09550),
  DOI 10.1051/0004-6361/202346794). CARMENES activity-indicator
  time-series; Karmn J04153-076 P_rot = 8.56 d, quality flag D
  ("debated"). 27 of 166 periods are debated, 68 are provisional.
  **Recorded in DB meta_notes only — not a recommended measurement.**

### Read (context / methodology)

- **Heintz W. D. 1974** — *Astrometric study of four visual binaries*,
  AJ 79, 819 (`1974AJ.....79..819H`). Provides the historic BC mass
  ratio used by Mason 2017 to split the mass sum.
- **van Leeuwen F. 2007** — *Validation of the new Hipparcos
  reduction*, A&A 474, 653 (`2007A&A...474..653V`). Parallax used by
  Mason 2017 dynamical mass derivation.
- **Cummings J. D., Kalirai J. S., Tremblay P.-E. et al. 2018** —
  *The white dwarf initial–final mass relation for progenitor masses
  up to 7.5 M☉*, ApJ 866, 21. IFMR used by Bond 2017 for the
  progenitor mass inversion of 40 Eri B.
- **Fuhrmann K., Chini R., Buda L.-S. & Pozo Nuñez F. 2014** —
  *On the Age of Gliese 86*, ApJ 785, 68 (`2014ApJ...785...68F`,
  DOI 10.1088/0004-637X/785/1/68). Primarily an age determination
  of the Gl 86 K+WD binary, with 40 Eri C cited as an analog case
  where the M-dwarf companion's "considerable projected rotational
  velocity" is attributed to mass loss from a degenerate companion's
  prior AGB phase. Cited by Bond 2017 §6.2 for the same spin-up
  hypothesis applied to 40 Eri C.
- **Tokovinin A. 2018** — *The updated multiple-star catalog*,
  ApJS 235, 6 (`2018ApJS..235....6T`). Lists the A-BC pair as
  unfitted with ~8000-yr outer orbit.
- **Burrows A. et al. 2024** — *The Death of Vulcan: NEID Reveals
  That the Planet Candidate Orbiting HD 26965 Is Stellar Activity*,
  AJ 167, 243 (`2024AJ....167..243B`, DOI 10.3847/1538-3881/ad34d5).
  NEID precision RV monitoring of HD 26965 (= 40 Eri A); refutes
  the Ma 2018 "Vulcan" planet candidate, attributing the ~42-day
  signal to rotationally modulated stellar activity (spots +
  convective blueshift suppression). Not directly about C but
  establishes the planet-free status of the system.
- **Kopparapu R. K., Ramirez R. M., SchottelKotte J. et al. 2014** —
  *Habitable zones around main-sequence stars: dependence on planetary
  mass*, ApJ 787, L29 (`2014ApJ...787L..29K`, [arXiv:1404.5292](https://arxiv.org/abs/1404.5292)). HZ
  boundary scaling used to derive 40 Eri C's HZ context values.

### Read (instrument / non-cfg-decisive)

- **Schöfer P., Jeffers S. V., Reiners A. et al. 2019** —
  *The CARMENES search for exoplanets around M dwarfs.
  Activity indicators at visible and near-infrared wavelengths*,
  A&A 623, A44 (`2019A&A...623A..44S`, [arXiv:1903.06803](https://arxiv.org/abs/1903.06803)).
  CARMENES Hα EW time series; GJ 166 C is in the sample. Used
  for the Hα pEW range -2 to -4 Å (DB meta_notes).
- **Newton E. R., Mondrik N., Irwin J. et al. 2017** — *New rotation
  period measurements for M dwarfs in the southern hemisphere*,
  AJ 154, 224 (`2017AJ....154..224N`, [arXiv:1611.04857](https://arxiv.org/abs/1611.04857)). MEarth-
  South photometric rotation periods; one of several survey Hα
  cross-references.
- **Reiners A., Zechmeister M., Caballero J. A. et al. 2018** —
  *The CARMENES search for exoplanets around M dwarfs. High-
  resolution optical and near-infrared spectroscopy of 324 survey
  stars*, A&A 612, A49 (`2018A&A...612A..49R`, [arXiv:1711.06576](https://arxiv.org/abs/1711.06576)).
  CARMENES instrument paper; GJ 166 C parameter row.
- **Wright N. J., Drake J. J., Mamajek E. E., Henry G. W. 2011** —
  *The stellar-activity-rotation relationship and the evolution of
  stellar dynamos*, ApJ 743, 48 (`2011ApJ...743...48W`). M-dwarf
  log L_X / L_bol calibration used qualitatively.
- **France K., Loyd R. O. P., Youngblood A. et al. 2016** —
  *The MUSCLES treasury survey. I. Motivation and overview*,
  ApJ 820, 89 (`2016ApJ...820...89F`, [arXiv:1602.09142](https://arxiv.org/abs/1602.09142)). Context
  for XUV environment around active M dwarfs.

### Not read — no arXiv preprint or low-priority (~12 papers)

The full filtered bib (not regenerated for this stellar-only
synthesis since no Phase 3 driver/system.yaml exists for 40 Eri yet)
would include older multi-decade ground-based photometry of DY Eri
(Hertzsprung 1922 et seq.), historic spectrum classifications
(Joy 1947, Gliese 1957), and various activity-context M-dwarf
catalog papers. None drive cfg-relevant Decisions rows beyond
what the read set above already covers.

## Open items for follow-up

- **Independent rotation-period verification.** Shan 2024 8.56 d is
  flagged quality D. Independent confirmation via TESS short-cadence
  photometry (40 Eri C is in TESS pointing 32 / 33), RV phase-folded
  modulation, or ZDI spectropolarimetric mapping would convert the
  Decisions row from `n/a` to a recommended:false-then-true entry.
- **Single-paper Hα activity anchor.** The multi-survey scatter
  pEW = -2 to -4 Å covers the variable nature of an active flare
  star, but a dedicated long-baseline time-series measurement (e.g.
  CARMENES re-visit, HARPS-N follow-up) would let us record a
  paper-anchored mean + cycle amplitude rather than a range.
- **Isolated 40 Eri C X-ray measurement.** ROSAT All-Sky Survey
  blends the BC pair. A Chandra or XMM-Newton dedicated pointing
  separating C from B's photospheric thermal X-rays would give a
  paper-anchored log L_X / L_bol value. Currently qualitative only.
- **Flare rate quantification.** DY Eri variability is well-known
  qualitatively but no survey-derived quantitative flare frequency
  (flares per day above an energy threshold) is in our current
  bibliography. A TESS Sector-by-Sector analysis or Evryscope
  flare-survey result for GJ 166 C would close this gap.
- **AGB-spin-up scenario confirmation.** Fuhrmann 2014's suggestion
  that C was spun up by B's AGB-phase mass-transfer is consistent
  with (but not confirmed by) a debated short P_rot. A confirmed
  short rotation period plus a chemical-abundance signature (s-process
  enhancement, helium enrichment) in C's atmosphere would be the
  decisive test. No Phase 3 cfg action; logged for narrative
  completeness.
- **Spectral type M4.5 vs M4.7.** Mann 2015 Table 5 lists M4.7,
  community canonical is M4.5 Ve. Both are within MK classification
  scatter; no Phase 3 action required, but worth noting in any future
  schema-tier upgrade that records spectral type with explicit
  reference attribution.

## Related

- [40-eridani-a](40-eridani-a.md) — K0.5 V primary, refuted Vulcan planet, ~83″ unresolved from BC
- [40-eridani-b](40-eridani-b.md) — DA2.9 white dwarf companion at 230.09-yr binary orbit with C
- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — applies to the BC visual-spectroscopic orbit Kepler→ICRS construction
