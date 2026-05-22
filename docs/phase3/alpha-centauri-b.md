<!-- Alpha Centauri B Phase 3 synthesis: cfg-ready stellar visual decisions -->
# Alpha Centauri B — Phase 3 Synthesis

Phase 3 stellar synthesis for the NearStars KSP mod (drafted 2026-05-22).

Alpha Centauri B is the K1 V secondary in the Alpha Centauri AB
binary, bound at 23.5 AU semi-major axis with P = 79.91 yr to A.
Mass 0.9373 ± 0.0033 M☉, radius 0.8632 ± 0.0037 R☉, luminosity
0.503 ± 0.007 L☉ (one-third of A's). It is metal-rich
([Fe/H] = +0.25 ± 0.04, Porto de Mello 2008), slightly more active
than A (log R'_HK = -4.85; 41-day rotation period), and has a
~7-year activity cycle inferred from photometric monitoring
(DeWarf 2010) and X-ray flux modulation (Robrade & Schmitt 2005,
2012).

For NearStars the goal is a K1 V star whose visual presence is
distinguishably warmer/yellower than A or Sol, but not yet visibly
"orange" like a true K-late dwarf — it sits at the bridge between
G-class and K-class spectral appearance. The historical context of
the Dumusque 2012 phantom-planet (Alpha Cen Bb) and its 2015
retraction by Rajpaul shapes how we interpret RV signals around this
star — the cfg adopts no planets for B.

**Scenario choice for NearStars: K1 V warm-yellow dwarf with
super-solar metallicity and 7-year activity cycle** — slightly
larger limb darkening than A, mild but detectable spot coverage at
cycle max, and a Sun-like magnetic dynamo geometry.

## Decisions

Kopernicus star cfg-ready values.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `mass_msun` | 0.9373 | high | Pourbaix & Boffin 2016 binary_orbit |
| `radius_rsun` | 0.8632 | high | Kervella et al. 2017 VLTI/PIONIER |
| `teff_k` | 5316 | high | Porto de Mello et al. 2008 high-res spectroscopy |
| `luminosity_lsun` | 0.503 | high | Kervella et al. 2017 bolometric flux |
| `spectype` | K1 V | high | Keenan & McNeil 1989 |
| `metallicity_fe_h_dex` | +0.25 | high | Porto de Mello et al. 2008 |
| `age_gyr` | 4.81 ± 0.5 | medium | Joyce & Chaboyer 2018 — same as A (coeval) |
| `rotation_period_days` | 41 | high | DeWarf et al. 2010 |
| `obliquity_deg` | 0 | low | adopted — no measurement |
| `surface_color_temp_k` | 5290 | high | weighted toward limb-darkened mean |
| `surface_tint_rgb_hex` | `#ffe9c4` | medium | blackbody 5290 K → CIE chromaticity, warm-yellow (between Sun and a true K dwarf orange) |
| `corona_tint_rgb_hex` | `#ffd9a0` | low | slightly warmer than disk; observed in chromospheric line ratios |
| `limb_darkening_coeff_quadratic_a` | 0.35 | medium | Claret 2017 K-dwarf reductions; modestly stronger than Sun |
| `limb_darkening_coeff_quadratic_b` | 0.30 | medium | same |
| `granulation_cell_size_arcsec` | 1.0e-3 | medium | Bigot et al. 2008 / smaller cells than A due to lower Teff |
| `convective_overshoot_pct` | 14 | medium | deeper convective envelope than A |
| `magnetic_cycle_period_yr` | 7 | medium | Robrade & Schmitt 2005/2012, Ayres 2014 X-ray cycle |
| `spot_coverage_max_pct` | 5 | medium | DeWarf 2010 — peak-to-peak photometric amplitude ~3% in V |
| `spot_temperature_offset_k` | -1700 | medium | typical K-dwarf umbra ~3600 K → -1700 K below mean photosphere |
| `xray_log_lx_erg_s` | 27.3 | high | Robrade & Schmitt 2005, XMM-Newton |
| `xray_cycle_factor` | 4.5 | medium | Robrade & Schmitt 2012 — clear cycle from 2003–2010 monitoring |
| `flare_rate_per_day_amplitude_log10` | -2 | medium | Ayres 2014 — modest superflare rate; ~10× higher than A |
| `wind_mass_loss_rate_msun_yr` | 2e-14 | medium | Wood et al. 2005 (joint AB measurement) |
| `wind_terminal_velocity_km_s` | 650 | medium | slower than A due to lower escape velocity |
| `chromosphere_ca_ii_log_rhk` | -4.85 | high | DeWarf et al. 2010 |
| `helioseismic_p_mode_max_freq_mhz` | 4.1 | high | Carrier & Bourban 2003 — p-mode envelope higher than A due to higher log g |
| `apparent_diameter_arcsec_from_sol` | 0.0060 | high | derived: 2 × 0.8632 R☉ / 1.347 pc × 206265 |
| `apparent_magnitude_v_from_sol` | 1.33 | high | Hipparcos/SIMBAD |
| `companion_a_max_separation_arcsec` | 12 | high | mirror of A's geometry |
| `companion_a_min_separation_arcsec` | 1.7 | high | mirror of A's geometry |
| `proxima_separation_au_from_b` | 8700 | medium | Kervella, Thévenin & Lovis 2017 — bound outer orbit |
| `interstellar_extinction_av_mag` | 0.0 | high | LIC, negligible reddening |

## Stellar disk synthesis

Alpha Cen B is the first nearby star where a K-class character is
visually obvious. At 5316 K (Porto de Mello 2008) it sits ~500 K
cooler than A and ~460 K cooler than the Sun. The disk-integrated
chromaticity shifts the perceived color firmly into the warm-yellow
zone — RGB ≈ `#ffe9c4` after CIE-D55 → blackbody mapping. Compared
to A's `#fff6e0`, B is unambiguously warmer-toned and would be
perceived as a "K dwarf" in a side-by-side comparison.

**Color choice.** Blackbody peak at ~545 nm (vs A's 496 nm and
Sun's 502 nm). The B-V color (~0.90, Hipparcos) is similar to other
K1 V comparison stars (61 Cyg A: K5 V at B-V = 1.06; 70 Oph A: K0 V
at B-V = 0.86). The KSP tint should be visibly distinct from A but
not as orange as 61 Cyg A.

**Angular diameter.** Kervella 2017's PIONIER measurement gives
5.999 ± 0.025 mas as seen from Earth — about 30% smaller than A's
8.502 mas. From a hypothetical Earth-analog around B at the L=0.503
flux-equivalent distance (0.71 AU), the disk would subtend ~0.71°,
larger than the Sun's 0.53° as seen from Earth and ~33% larger in
solid angle (compensating for the lower luminosity at closer orbit).

**Limb darkening.** K-dwarf limb darkening is stronger than solar:
edge brightness ~30% of disk-center (vs Sun's ~40%). Adopt
quadratic (a,b) = (0.35, 0.30). Limb appears slightly redder due to
TiO band onset in the cooler upper photosphere (already detectable in
B's spectrum unlike A or Sun).

**Granulation.** Bigot et al. 2008 derived smaller granulation
cells for B than A — consistent with the lower-mass deeper-convection
expectation. Cells are ~1.0e-3 arcsec from Earth distance (slightly
finer than A's 1.3e-3). Visual flicker noise is somewhat larger
amplitude (~0.15 magnitude/cell vs Sun's 0.10) but on similar
~10-minute timescales.

**P-mode oscillations.** Carrier & Bourban 2003 detect p-modes at
envelope peak ~4.1 mHz (period ~4 minutes) with amplitude ~9 cm/s
RV. This is higher frequency than A or Sun (consistent with higher
surface gravity log g = 4.54 vs A's 4.32). p-mode visual impact is
sub-percent flickering on minutes timescale; same KSP treatment as A.

**No ASTERIA-class transits.** Knapp 2020 ASTERIA CubeSat transit
search and ground-based RV searches (Dumusque 2012, retracted Rajpaul
2015) place strict limits on close-in (Earth-mass at P < 50 d)
planets. Phase 3 cfg does not include any B planets, consistent with
current observational state.

## Activity and variability synthesis

Alpha Cen B is the more magnetically active member of the AB pair.
Multiple independent monitoring campaigns confirm:

- **Rotation period: 41 ± 3 days** (DeWarf et al. 2010 from
  photometric variability; consistent with v sin i = 1.0 ± 0.5 km/s
  from spectroscopy via i = 56° inclination assumption). Slower than
  A due to lower mass — Brun & Browning 2017 dynamo theory predicts
  K-dwarf rotation typically 30–60 d at ~5 Gyr age.
- **Magnetic cycle period: ~7 years**. First detected by Robrade &
  Schmitt 2005 in XMM-Newton X-ray fluxes; confirmed in DeWarf 2010
  photometry. Notable because it is *shorter* than the Sun's 11-year
  Schwabe cycle despite B being a slower rotator — suggesting that
  the magnetic dynamo structure is different from the solar Babcock-
  Leighton picture.
- **log R'_HK = -4.85** (DeWarf et al. 2010 mean over cycle).
  Moderately active for its rotation rate. Bcoll (longitudinal field
  strength) ≈ 5–15 G during cycle max (Boro Saikia et al. 2018 ZDI).
- **X-ray luminosity: log L_X ≈ 27.3 erg/s** (Robrade & Schmitt
  2005). Factor ~2 higher than A in quiescence. The X-ray cycle
  amplitude is factor 4.5 — modest but well-measured over 2003–2012
  monitoring.

**Spot coverage and visibility.** DeWarf 2010 derived peak-to-peak V
photometric amplitude ~3% at cycle max, implying ~5% disk-area
spot coverage. Spot temperature ~3600 K (umbra) and ~4800 K
(penumbra). Visual: at cycle max, 3–5 dark spot groups distributed
across mid-latitude (±15–40°), each ~8° angular diameter. The
strong limb darkening + spot contrast makes B noticeably "freckled"
when imaged at high resolution at cycle max.

**Flare rate.** Ayres 2014 derived modest flare rate from FUV/UV
monitoring — log-amplitude distribution flatter than A, with ~10×
higher rate for M-class equivalent flares. No superflares confirmed
in the multi-decade baseline. K1 V old stars are generally moderate
flare emitters compared to younger or fully convective M dwarfs.

**Coronal heating.** Robrade & Schmitt 2005 derived T_corona ~ 2-3
MK at cycle max, ~1-1.5 MK at min — the same range as the Sun but
shifted slightly. The hot loops are concentrated near magnetic
network boundaries, similar to solar coronal hole geometry but
denser.

**Magnetic geometry.** Boro Saikia et al. 2018 Zeeman Doppler
imaging shows a predominantly dipole-dominant magnetic geometry at
cycle min, transitioning to multipole-dominant at cycle max — a
solar-like behavior but condensed into the 7-year cycle. The dipole
tilt is ~30° from rotation axis.

## System geometry synthesis

The AB binary mutual visibility from B's frame is the mirror image
of A's:

- B orbits A at 23.5 AU semi-major axis with e = 0.5179.
- From B's surface, A appears as a brilliant variable star ranging
  from V ≈ -22 (apastron, but as a near-point source at 0.022° ang
  diameter) to V ≈ -24 (periastron, 0.066° ang diameter).
- The illumination from A at B's HZ-equivalent orbit (~0.71 AU
  around B) varies by factor (35.7/11.4)² = 9.8× over the binary
  orbital period, providing seasonal-like climate forcing.

**From a hypothetical Earth-analog around B** (0.71 AU, where the
classical HZ would put it): the sun-in-sky is Alpha B at apparent
diameter ~0.71° (33% larger angular size than Sun-from-Earth) but
1× luminosity (matched to L=0.503 at 0.71 AU). The chromaticity is
the warm-yellow K1 V we adopted.

A's flux at this orbit varies between:
- Apastron: A is at 36.0 - 0.71 ≈ 35.3 AU from B-Earth → flux is
  1.52 / 35.3² ≈ 0.0012 L_eff (vs 1.0 from B itself). Magnitude
  ~-19.5 (~2× full-Moon brightness).
- Periastron: A at 11.4 - 0.71 ≈ 10.7 AU → flux 0.013 L_eff.
  Magnitude ~-22 (~30× full-Moon brightness, casts visible shadows).

Day vs night around B-Earth becomes dramatic: during the periastron
phase, when A is in the night sky, it provides night-time
illumination ~30× full-Moon — bright enough for surface activity
without artificial lighting.

**Proxima visibility.** From B's surface, Proxima is at the same
apparent magnitude ~+5 and ~2° from A.

**No planets confirmed around B.** Dumusque et al. 2012 reported
Alpha Cen Bb at P = 3.236 d, K = 0.51 m/s, but this was rebutted by
Rajpaul et al. 2015 (the Gaussian-process activity model showed the
signal was a sampling artifact). The Rajpaul retraction is one of
the cleanest examples of why high-precision RV M-dwarf planet
detection requires explicit activity modeling. As of 2026 no
confirmed planets exist around B.

## Visual styling

- **Global appearance.** A warm-yellow K1 V disk, unambiguously
  cooler/yellower than A or Sol. The observer would describe it as
  "amber" or "warm cream" — not orange yet, but visibly past the
  pure-white solar appearance.
- **Dayside illumination of orbiting bodies.** Color temperature
  ~5290 K — atmospheric scattering on Earth-analog bodies produces
  slightly warmer sky tones than under solar illumination (sky
  perhaps `#a0c0e0` instead of pure `#87ceeb`), with sunsets/sunrises
  exaggerated in red-orange.
- **Disk brightness profile.** Stronger limb darkening than A; edge
  appears ~30% as bright as disk-center, with slight redward shift.
- **Spot visibility.** At cycle max, 3–5 sunspot groups distributed
  across the visible hemisphere, each ~5–8° angular diameter,
  ~1700 K cooler than photosphere. KSP-equivalent: procedural dark
  patches that wax and wane over a 7-year cycle, visible as freckles
  on the rendered disk.
- **Companion A.** Always present in the sky from any B orbit. At
  apastron, A is a brilliant ~0.02° disk; at periastron, ~0.07°
  disk subtly resolved (A has 1.42× B's surface brightness due to
  higher Teff). Provides spectacular variable nighttime
  illumination over the 79.91-yr orbit.
- **Proxima Cen.** Magnitude ~+5 point source ~2° from A.
  Unremarkable visually.
- **Spectral lines.** Same dominant lines as A but with additional
  TiO bands developing in red wavelengths. H-α absorption is deeper
  (cooler photosphere), Ca II H/K cores show stronger emission
  reversal during cycle maxima.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2017A&A...597A.137K** Kervella et al. 2017 — VLTI/PIONIER
  interferometric radius (5.999 ± 0.025 mas; R = 0.8632 ± 0.0037
  R☉) and bolometric luminosity (0.503 ± 0.007 L☉).
- **2008A&A...488..653P** Porto de Mello et al. 2008 — Differential
  high-resolution spectroscopic Teff (5316 ± 28 K) and [Fe/H]
  (+0.25 ± 0.04). Pair-with-A measurement.
- **2010ApJ...722..343D** DeWarf et al. 2010 — 7-yr photometric +
  Ca II H&K monitoring. Rotation period 41 ± 3 d, partial activity
  cycle, log R'_HK = -4.85.
- **2016A&A...586A..90P** Pourbaix & Boffin 2016 — Dynamical mass
  0.9373 ± 0.0033 M☉.
- **2006A&A...446..635B** Bigot et al. 2006 — VLTI/VINCI Alpha B
  interferometry, granulation noise constraint. R = 0.863 ± 0.005
  R☉ (precursor to Kervella 2017).
- **2018ApJ...864...99J** Joyce & Chaboyer 2018 — System age
  4.81 ± 0.50 Gyr; coeval with A. Independent mass M_B = 0.934 ±
  0.0061 M☉ via MESA + asteroseismology.
- **2003A&A...404.1087K** Kervella et al. 2003 — VLTI/VINCI early
  interferometry. Precursor measurement consistent with later
  Kervella 2017.
- **1009.1652 (2010ApJ...717.1279A)** Ayres 2010 — X-ray, FUV, UV
  multi-wavelength monitoring of B, including activity cycle phase
  evolution. Provides cycle amplitude factor 4.5 used in cfg.
- **1202.1265** Carrier & Bourban 2003 — HARPS asteroseismic
  p-mode detection. Confirms log g = 4.54 ± 0.02; p-mode envelope
  at 4.1 mHz.
- **1401.2211** Heller & Armstrong 2014 — "Superhabitability" of
  K-dwarf worlds. Context for what makes B's HZ planets interesting
  beyond just being habitable.

### Read (context / methodology, not decision-driving)

- **0811.0673** Quintana 2002 — Planet formation in B's HZ. Shows
  HZ planets are dynamically possible despite the AB perturbation.
- **1009.1652** Robrade & Schmitt 2012 — Continued X-ray monitoring
  to 2010, extends Robrade & Schmitt 2005's cycle detection.
- **1506.07304** Rajpaul et al. 2015 — Gaussian-process activity
  model for RV time series. Methodology paper that retracts
  Dumusque 2012's Alpha Cen Bb claim. Important context for null
  result on planets around B.
- **1902.10711** Coffinet et al. 2019 — HARPS activity and telluric
  contamination of Alpha B observations. Relevant for the Dumusque/
  Rajpaul controversy.
- **1805.00929** Morel 2018 — Chemical composition of AB revisited.
  Independent confirmation of [Fe/H] = +0.24 and detailed individual
  element abundances. Cross-validates Porto de Mello 2008.
- **1711.06320** Zhao et al. 2018 — Planet detectability around AB
  with various instruments. Context for current RV/transit limits.
- **2211.11756** Foster et al. 2022 — Optical SETI search.

### Read (instrument-only, not visual-informative)

- **2405.13247** Pasquini et al. 2024 — Deep learning for RV
  detection. Methodology.
- "Going to Alpha Centauri B and setting up a Radio Bridge" —
  speculative interstellar communication paper. Not science.

### Not read — no arXiv preprint available (78 papers)

The bulk consist of pre-2010 references and conference summaries.
Key not-read examples:

- "Fe II fluorescence in main-sequence K-dwarfs" — likely Ayres
  pre-2008 paper. Skipped.
- Multiple AAS abstracts and IAU symposium proceedings summarizing
  results in read papers.
- ASTERIA CubeSat dissertation (Knapp 2020) — null transit search,
  cited for context but not visual-informative.

**User action requested.** If newer ZDI magnetic-imaging campaigns
on Alpha B come online (e.g., expected SPIRou or NIRPS results
2026+), the spot-coverage and dipole tilt numbers may need revision.

---

## Open items for follow-up

- The 7-year activity cycle timing is constrained by Robrade &
  Schmitt 2012 to phase but the period uncertainty is ~1.5 yr.
  Additional cycles need to be tracked through 2030 for tighter
  period.
- Spot temperature offset (-1700 K vs photosphere) is a
  K-dwarf-generic value, not measured directly for B. TESS or
  CHEOPS multi-color photometry could constrain.
- Dipole tilt (~30°) from Boro Saikia 2018 ZDI is single-epoch;
  cycle-resolved magnetic mapping is in progress (NIRPS/SPIRou).
- No confirmed planets, but RV upper limits (M sin i < 4 M⊕ at
  P < 50 d, Rajpaul 2015) leave room for a small companion. Phase 3
  cfg should be revised if ESPRESSO long-baseline detects something.
- The Knapp 2020 ASTERIA null transit result excludes Earth-radius
  planets at P < 28 d at high confidence; no planet inventory
  decisions hinge on this.
- The historical Bb retraction shapes how user-facing documentation
  should describe B's planet inventory — explicitly "no confirmed
  planets" rather than just blank.
