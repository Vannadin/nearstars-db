# Barnard's Star — Phase 3 Synthesis

Barnard's Star (GJ 699, HIP 87937) is the second-closest stellar system
to the Sun at 1.828 pc (Gaia DR3 parallax 547.0 ± 0.04 mas), trailing
only the α Centauri triple. An isolated M4.0 V dwarf with a mass of
0.161 ± 0.006 M☉ (Mann 2015 M–K calibration), a radius of 0.1868 ±
0.0011 R☉ (Rains 2021 CHARA interferometry), and an effective
temperature of 3195 ± 28 K (González Hernández 2024 SED + bolometric
flux), it has the largest known proper motion of any star (10.3 arcsec
yr⁻¹) and a heliocentric radial velocity of −110 km s⁻¹ — kinematics
that place it firmly in the Galactic halo population. Toledo-Padrón
et al. 2019 estimate a kinematic age of 10 ± 2 Gyr, making Barnard
one of the oldest stars within 10 pc.

The system has a long and complicated planet-search history. Van de
Kamp's 1960s–1980s astrometric campaign claimed Jupiter-mass companions
that were never confirmed; Ribas et al. 2018 reported a super-Earth
"b" at 0.4 AU with a 233-day period from a HARPS RV ensemble, which
Lubin et al. 2021 subsequently refuted as a stellar-activity alias.
The current planet inventory rests on the ESPRESSO discovery of
González Hernández et al. 2024 — a sub-Earth-mass planet at P = 3.15 d
that reuses the "b" letter for a wholly different object — and the
MAROON-X confirmation of Basant et al. 2025 that promotes three
additional candidates (c, d, e) to confirmed status. All four planets
are short-period (P < 7 d), sub-Earth Msini, and lie well inside the
inner edge of the conservative habitable zone (Kopparapu 2014 inner
HZ ≈ 0.1 AU, corresponding to P ≈ 10 d for this stellar mass).

Activity is the defining stellar feature for Barnard. Among M4 dwarfs
it is exceptionally quiet: log R'HK = −5.69 (Toledo-Padrón 2019), more
inactive than the Sun at minimum, with a slow 145 ± 15 d rotation
period and a long-term magnetic cycle of 10 ± 2 yr that González
Hernández 2024 independently recovers at 3200 d. The Mega-MUSCLES
program (France et al. 2020) nonetheless detected two FUV and one
X-ray flare in a single HST + Chandra campaign, implying a flare duty
cycle of ~25% — high for a star this old, but with individual flare
energies (~10²⁹·² – 10²⁹·⁵ erg) orders of magnitude below the Proxima
superflare regime. France 2020 conclude that the *quiescent* XUV
output is comparable to modern-Earth solar maximum (atmospheric
heating rates not catastrophic), but the *flaring* duty cycle drives
a thermal escape rate equivalent to ~87 Earth atmospheres Gyr⁻¹ plus
~3 Earth-atm Gyr⁻¹ from ion-loss processes. Their headline framing —
"habitable at last?" — captures the genuine tension: Barnard is the
benchmark old, quiet M dwarf, but the cumulative flare environment
over 10 Gyr is still atmospherically erosive.

**Scenario choice for NearStars: a deep red, halo-old M4 V dwarf with
a 145-day rotation, modest ~200-G surface magnetic field, a benign
quiescent XUV environment, and a ~10-year activity cycle that
modulates a low (~25%) flare duty cycle. Visual styling emphasizes
the cool 3195-K continuum, sub-solar metallicity slightly bluing
the molecular bands relative to a metal-rich M4, and the dim
illumination that all four hot rocky planets experience close-in.**
17 cfg picks; 12 canonical-aligned, 5 tie-break (X-ray quiescent
level, magnetic field RMS, visual hex tints, flare-rate normalization,
limb-darkening exponent). No documented divergences.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M4.0 V | high | DB curated; halo old + low activity argues "V" not "Ve" despite legacy classifications |
| `mass_msun` | 0.161 ± 0.006 | high | Mann 2015 M–K relation; DB recommended |
| `radius_rsun` | 0.1868 ± 0.0011 | high | Rains 2021 CHARA interferometry |
| `teff_k` | 3195 ± 28 | high | González Hernández 2024 SED fitting; Cristofari 2024 NIR 3231 ± 21 K agrees within ~1.5σ |
| `luminosity_lsun` | 0.003558 ± 0.00007 | high | González Hernández 2024 bolometric flux |
| `metallicity_fe_h_dex` | −0.15 ± 0.16 | medium | Marfil 2021 high-res optical spectroscopy; Cristofari 2024 prefers ~−0.5 dex as model input; broad consensus is sub-solar |
| `age_gyr` | 10 ± 2 | high | Toledo-Padrón 2019 kinematic age from halo membership |
| `rotation_period_days` | 145 ± 15 | high | Toledo-Padrón 2019 chromospheric + photometric |
| `activity_log_rhk` | −5.69 | high | Toledo-Padrón 2019; among quietest M dwarfs known |
| `activity_cycle_years` | 10 ± 2 | high | Toledo-Padrón 2019 (10 yr); González Hernández 2024 recovers 3200 d ≈ 8.8 yr |
| `x_ray_log_lx_cgs_quiescent` | 25.5 | medium | Tie-break: France 2020 Chandra single-epoch detection at low S/N; magnitude consistent with old-M-dwarf saturated locus |
| `x_ray_log_lx_cgs_flare_peak` | 27.5 | medium | Tie-break: France 2020 individual events ~10²⁹·² erg over ~5000 s integration → peak rate consistent |
| `flare_duty_cycle` | 0.25 | high | France 2020 Mega-MUSCLES — fraction of time in flaring state from HST + Chandra simultaneous detections |
| `flare_rate_per_day_total` | 0.1 | medium | Tie-break: 3 flares in ~50 ks (HST + Chandra) → ~5/day if extrapolated to FUV-only; conservative 0.1 white-light flare/day matches photometric upper limits |
| `magnetic_total_field_G_mean` | 200 | medium | Tie-break: Reiners 2022 CARMENES Zeeman analysis estimates few-hundred-G surface field; SPIRou polarimetry (Cristofari 2024) implies ordered component much weaker |
| `xuv_quiescent_flux_at_1au_erg_cm2_s` | 0.018 | medium | Duvvuri 2021 DEM reconstruction of EUV 100–912 Å, quiescent |
| `xuv_flare_flux_at_1au_erg_cm2_s` | 0.146 | medium | Duvvuri 2021 DEM reconstruction, flaring state (~8× quiescent) |
| `limb_darkening_alpha_h` | ~0.4 | low | Tie-break: not directly measured; M4 V interpolation from Claret 2018 grid |
| `visual_surface_tint_hex_primary` | `#bd4a2c` (deep red M4 V, slightly bluer than M5.5 owing to sub-solar [Fe/H]) | medium | Tie-break: Teff 3195 K blackbody × molecular-band suppression; [Fe/H] = −0.15 slightly weakens TiO depth |
| `visual_flare_color_hex` | `#ff5e36` (Hα + blue continuum brightening during weak FUV flares) | medium | Tie-break: France 2020 FUV flare spectra; specific hex chosen for in-game visibility |
| `stellar_color_temp_k` | 3195 | high | derived |

## Surface synthesis

Barnard's photosphere is among the dimmest in the NearStars catalog —
0.003558 L☉, 0.187 R☉, Teff 3195 K — making it about 1/280 of the Sun
in bolometric power. At M4 V it sits two subtypes hotter than Proxima
(M5.5V, 2980 K) and two cooler than HD 69830 / 61 Vir analogs, with a
visible-band SED still dominated by TiO and VO molecular bands but
already showing a more "open" pseudocontinuum than the deeper-red
M5–M7 regime. The sub-solar [Fe/H] = −0.15 marginally weakens the
TiO band depth versus a solar-metallicity M4, contributing to a
slightly bluer continuum tint — the cfg's `#bd4a2c` is offset toward
brighter red-orange rather than the deeper red-brown of metal-rich
M4 V references.

CHARA interferometric limb darkening (Rains 2021) constrains the
radius to 0.5% precision but does not directly resolve the
limb-darkening exponent in H band. The cfg adopts α ≈ 0.4 as a
tie-break from the Claret 2018 PHOENIX grid interpolation; the actual
profile depends on chromospheric filling that is poorly modeled in
1D atmospheres at this Teff. Cristofari 2024's SPIRou NIR spectrum
identifies > 18 000 absorption features in the observed data but only
~6 800 in the matching PHOENIX-ACES model, a 2.7× discrepancy that
underlines persistent M-dwarf atmosphere-model incompleteness.

Granulation simulations have not been performed at the resolution
needed for in-game close-up rendering; M-dwarf granulation cells
should scale to ~20–30 km across at this pressure scale height,
slightly larger than Proxima's but smaller than mid-M solar-analog
references. Spot coverage during the activity cycle has not been
directly TiO-band-modeled for Barnard owing to the low activity
level; in-game spot fraction should remain at the 1–2% upper bound
consistent with the Toledo-Padrón 2019 rotational modulation
amplitude.

## Atmosphere synthesis

Barnard's chromosphere and corona are the quietest among all
well-studied M4 dwarfs. log R'HK = −5.69 (Toledo-Padrón 2019) places
it more inactive than the modern Sun (log R'HK ≈ −4.9), and the
chromospheric activity-induced RV signal at the 145-d rotation period
has an upper limit of just 1 m s⁻¹ — small enough that the same paper
recovered the rotation only through joint multi-spectrograph analysis
of 14.5 years of data. The chromospheric Hα profile sits in mild
absorption rather than emission, contradicting the legacy "Ve"
classification adopted in some catalogs; the cfg uses "M4.0 V"
accordingly.

The corona is faint. France et al. 2020 (Mega-MUSCLES) obtained
contemporaneous HST STIS/COS and Chandra ACIS-S spectra and detected
three discrete flares (two in FUV, one in X-ray) in a combined
exposure of ~50 ks — yielding the headline 25% flare duty cycle. The
quiescent X-ray luminosity is at the lower end of the M-dwarf locus
(log L_X ~ 25.5 cgs, conservatively); during the flaring state it
rises to log L_X ~ 27.5 with individual event energies of ~10²⁹·²
erg over decay timescales of order 5000 s. The cfg encodes both the
quiescent and flare-peak rates, plus the duty cycle, so downstream
Kerbalism radiation-environment routines can sample the time-averaged
exposure.

The XUV environment is more demanding for hypothetical habitable-zone
planets than the optical activity suggests. Duvvuri 2021 reconstructed
the EUV (100–912 Å) spectrum via differential emission measure
modeling, finding a quiescent integrated flux of 0.018 erg cm⁻² s⁻¹
at 1 AU and a flaring flux of 0.146 erg cm⁻² s⁻¹ (~8× boost). France
2020 propagated these fluxes through a thermal + ion-loss escape model
for a hypothetical unmagnetized terrestrial planet at the HZ
(0.1 AU), finding that the quiescent XUV alone produces atmospheric
heating rates comparable to modern-Earth solar maximum — *not*
catastrophic. But integrated over the 25% flare duty cycle, the
cumulative loss is ~87 Earth atmospheres Gyr⁻¹ (thermal hydrodynamic
escape) + ~3 Earth-atm Gyr⁻¹ (ion-pickup escape). For the inner-system
planets at a = 0.019–0.038 AU, these rates scale up by another 7–28× —
a strong constraint against any retained primary atmosphere.

The magnetic field has been characterized in Stokes V (circular
polarization) by the SPIRou Legacy Survey since 2018. Cristofari 2024
notes the existence of detailed magnetic measurements but does not
itself extract the dipole strength; Reiners 2022 CARMENES
Zeeman-broadening estimates point to a mean surface field of order
200 G — modest by M-dwarf standards (Proxima reaches ~4 kG; younger
mid-M's like AU Mic exceed 1 kG). The ordered dipole component
inferred from spectropolarimetry is even smaller, consistent with the
old age and slow rotation.

## Rotation & spin synthesis

The 145 ± 15-d rotation period (Toledo-Padrón 2019) is among the
longest measured for any field M dwarf and is the dynamical signature
of 10 Gyr of magnetic braking. González Hernández 2024 independently
recovers the period at 140 d in ESPRESSO chromospheric indicators
plus its second harmonic at 71 d, in good agreement. The slow
rotation reinforces the kinematic age estimate via the standard
Newton 2018 / Engle 2018 gyrochronology relations for old M dwarfs.

The activity cycle of 10 ± 2 yr (Toledo-Padrón 2019) or 3200 d ≈ 8.8 yr
(González Hernández 2024) modulates both the chromospheric activity
indices and the long-term mean RV by a few m s⁻¹. The cycle is
Sun-like in duration but driven by a much weaker dynamo, and its
amplitude is consistent with the slow-rotator regime predicted by
Reiners & Mohanty 2012.

No asteroseismic oscillations have been detected in Barnard — the
surface gravity is too high and the convective amplitudes too low,
as for all M dwarfs. Differential rotation has not been resolved;
inclination of the rotation axis is unconstrained.

## Visual styling

Barnard renders as a deep red M4 V in NearStars — the photospheric
tint `#bd4a2c` sits between Proxima's `#c54c2a` deeper red and the
warmer red-orange of mid-M references like the GJ 1214 / AU Mic
analogs. The sub-solar [Fe/H] = −0.15 nudges the visible continuum
slightly toward orange relative to a solar-metallicity M4 by
weakening the TiO and VO molecular-band absorption that would
otherwise dominate the 5500–7000 Å region.

The star is small in absolute angular size but large from each of
its close-in planets: at d's 0.0188 AU it subtends 5.3°, at b's
0.0229 AU 4.3°, at c's 0.0274 AU 3.6°, at e's 0.0381 AU 2.6°. From
all four, the star fills 5–10× the apparent angular diameter of the
Sun seen from Earth — a constant dim red disk dominating the daylight
sky.

Flares are visible but infrequent compared to Proxima. The France
2020 25% duty cycle implies ~1 detectable flare per 4 days of
continuous observation in HST/Chandra-sensitive bands, but the
individual flare energies are below the threshold that would produce
a strong visible-band brightening at the star. The cfg's
`visual_flare_color_hex = #ff5e36` shifts color slightly toward
orange during peak emission, mimicking the modest Hα + blue
continuum brightening; intensity is markedly lower than the Proxima
analog. Superflares (≥ 10³³ erg) have not been documented for
Barnard, and the cfg does not include a separate superflare entry —
the existing flare cfg covers the observed energy distribution.

The corona is rendered as a very faint blue-white halo, brightening
slightly during the X-ray-bright phases of the 10-year cycle. The
extended FUV flux dominates the high-energy SED but is invisible to
unaided observation; in-game effects are limited to ambient
illumination color shifts during flares and visible Hα brightening
on the stellar disk.

## Bibliography

### Read (visual-informative, drove decisions above)

- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star* (`2024A&A...690A..79G`, arXiv:2410.00569).
  ESPRESSO discovery of current Barnard b; rotation period 140 d;
  long-term cycle 3200 d; refutation of Ribas 2018.
- **Basant R. et al. 2025** — *Four Sub-Earth Planets Orbiting
  Barnard's Star from MAROON-X and ESPRESSO* (`2025ApJ...982L...1B`,
  arXiv:2503.08095). MAROON-X confirmation of b, c, d, e at 30 cm/s
  precision; full 4-planet orbital + mass table.
- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star: very slow rotation and evidence for long-term
  activity cycle* (`2019MNRAS.488.5145T`, arXiv:1812.06712). P_rot
  = 145 ± 15 d; 10-yr cycle; log R'HK; age estimate.
- **Cristofari P. et al. 2024** — *Comprehensive High-resolution
  Chemical Spectroscopy of Barnard's Star with SPIRou* (arXiv:2310.12125).
  T_eff = 3231 ± 21 K alt fit; 15-element abundances; SPIRou
  spectropolarimetry baseline for B-field.
- **Duvvuri G. et al. 2021** — *Reconstructing the Extreme Ultraviolet
  Emission of Cool Dwarfs Using Differential Emission Measure
  Polynomials* (arXiv:2102.08493). DEM EUV reconstruction; Barnard
  quiescent and flare EUV fluxes.
- **France K. et al. 2020** — *The High-Energy Radiation Environment
  Around a 10 Gyr M Dwarf: Habitable at Last?* (arXiv:2009.01259).
  Mega-MUSCLES HST + Chandra; 25% flare duty cycle; atmospheric loss
  rates at HZ.
- **Mann A. W. et al. 2015** — *How to Constrain Your M Dwarf*
  (`2015ApJ...804...64M`, arXiv:1501.01635). M–K mass relation; DB
  recommended mass.
- **Rains A. D. et al. 2021** — *Characterization of 92 southern TESS
  candidate planet hosts* (`2021MNRAS.504.5788R`, arXiv:2102.08133).
  CHARA interferometric radius for Barnard.
- **Boyajian T. S. et al. 2012** — *Stellar Diameters and Temperatures
  II* (`2012ApJ...757..112B`, arXiv:1208.2431). Independent
  interferometric R + Teff confirmation.
- **Marfil E. et al. 2021** — *The CARMENES search for exoplanets
  around M dwarfs: Stellar atmospheric parameters* (`2021A&A...656A.162M`,
  arXiv:2110.07329). [Fe/H] = −0.15.

### Read (context / methodology, not decision-driving)

- **Lubin J. et al. 2021** — *Stellar Activity Manifesting at a
  One-year Alias Explains Barnard b as a False Positive*
  (`2021AJ....162...61L`; no arXiv). Refutes Ribas 2018 super-Earth.
  Cited via abstract.
- **Ribas I. et al. 2018** — *A candidate super-Earth planet orbiting
  near the snow line of Barnard's star* (`2018Natur.563..365R`,
  arXiv:1811.05955). Historical claim, refuted; preserved for
  literature continuity.
- **Stefanov A. K. et al. 2024** — *A sub-Earth-mass planet orbiting
  Barnard's star: No evidence of transits in TESS photometry*
  (arXiv:2410.00577). Companion to González Hernández 2024 ruling
  out transits.
- **Choi J. et al. 2013** — *Precise Doppler Monitoring of Barnard's
  Star* (arXiv:1208.2273). Long-baseline RV constraints; pre-discovery
  upper limits.
- **Paulson D. B. et al. 2006** — *Optical Spectroscopy of a Flare on
  Barnard's Star* (arXiv:astro-ph/0511281). Single flare event
  characterization.
- **Kürster M. et al. 2003** — *Low-level RV variability in Barnard's
  Star* (arXiv:astro-ph/0303528). Secular acceleration + activity
  signatures.
- **Reiners A. et al. 2022** — CARMENES Zeeman analysis for M dwarfs;
  Barnard mean field constraint (no specific Phase 3 arXiv fetched —
  inferred from sample work).

### Read (instrument-only, not visual-informative)

- **Liebert J. et al. 2005** — *Barnard's Star and the M Dwarf
  Temperature Scale*. Calibration methodology only.
- **Benedict G. F. et al. 1998** — *HST Fine Guidance Sensor
  photometry of Proxima and Barnard*. Astrometric methodology only.

### Not read — no arXiv preprint or low-priority (~130 papers)

The Barnard bibliography is large because of the star's long history
as a planet-search benchmark and its proximity. The skipped pool
includes:

- Pre-2000 spectral-type confirmations and proper-motion measurements
- Historical Van de Kamp astrometric claims (1960s–1980s)
- Instrumentation-development papers using Barnard as RV standard
- Mid-IR direct imaging upper limits (CanariCam 1507.01254 etc.)
- SETI / interstellar-mission targeting proposals

Preserved in `docs/phase3/_bib/barnards-star.yaml` with
`status: skipped`.

## Open items for follow-up

- **Magnetic-field dipole strength via Stokes V**: Cristofari 2024
  uses SPIRou polarimetric data but does not extract the longitudinal
  field. A targeted ZDI (Zeeman Doppler Imaging) analysis on the same
  data set would tighten the cfg `magnetic_total_field_G_mean` entry,
  currently a tie-break at 200 G.
- **Lubin 2021 not fetched**: The canonical refutation of Ribas 2018
  has no arXiv preprint. A user-pasted abstract or full text would
  let us upgrade the discussion of Ribas 2018 from "abstract-cited"
  to "deep-read."
- **Flare-rate calibration**: France 2020 reports a 25% duty cycle
  from one HST + Chandra epoch — a single observation snapshot. The
  cfg `flare_rate_per_day_total = 0.1` is a tie-break. TESS sector
  monitoring of Barnard could refine this if photometric sensitivity
  reaches the ~10²⁹-erg flare regime.
- **Phase 3 metallicity range**: Marfil 2021 reports −0.15 ± 0.16
  dex; Cristofari 2024 prefers ~ −0.5 dex as PHOENIX model input;
  Duvvuri 2021 adopts Ribas −0.32. A homogenized re-derivation across
  optical + NIR with consistent assumptions could narrow the range.
- **Spot covering fraction**: in-game spot rendering currently uses
  the 1–2% photometric upper bound. A direct TiO-band-depth
  modulation analysis (Berdyugina 2017 framework) would refine the
  cycle-modulated coverage.
- **DB spectral-type "M4.0 Ve"**: the legacy classification with the
  emission qualifier conflicts with the deeply inactive log R'HK and
  Hα-in-absorption profile. Recommend updating the DB to "M4.0 V";
  the cfg drops the "e" already.

## Related

- [barnards-star-b](barnards-star-b.md), [barnards-star-c](barnards-star-c.md), [barnards-star-d](barnards-star-d.md), [barnards-star-e](barnards-star-e.md) — confirmed sub-Earth planet family inside the HZ inner edge
- [proxima-cen](proxima-cen.md) — comparable distance + spectral subtype; activity contrast (Barnard quiet, Proxima active)
- [methodology](../reference/methodology.md) — Decisions schema source
- [data-sources](../reference/data-sources.md) — paper citation policy
- [mod-reference](../reference/mod-reference.md) — downstream cfg writers consuming these stellar fields
- [rex-data-comparison](../reference/rex-data-comparison.md) — Barnard appears in REX with the retracted Ribas 2018 planet; NS reflects the 2024–2025 ESPRESSO/MAROON-X system
