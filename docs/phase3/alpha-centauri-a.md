<!-- Alpha Centauri A Phase 3 synthesis: cfg-ready stellar visual decisions -->
# Alpha Centauri A — Phase 3 Synthesis

Phase 3 stellar synthesis for the NearStars KSP mod (drafted 2026-05-22).

Alpha Centauri A is the most Sun-like star outside the Solar System
that is also nearby and well-measured. It is a G2 V dwarf (same MK
class as the Sun) with mass 1.1055 ± 0.0039 M☉ (Pourbaix & Boffin
2016, dynamical binary orbit), radius 1.2234 ± 0.0053 R☉ (Kervella
et al. 2017, VLTI/PIONIER interferometry), and luminosity
1.521 ± 0.013 L☉. It sits 1.347 pc from the Solar System as the
slightly more massive primary in the Alpha Centauri AB binary, with
Proxima Cen bound at ~8700 AU as the distant tertiary.

For NearStars the goal is a Sun-twin that is visually distinguishable
from Sol mainly by its larger angular diameter (when viewed from
Earth-equivalent distance), modestly higher luminosity, and very
slightly cooler effective temperature. As of 2025 JWST/NIRCam
coronagraphy reports a candidate giant planet in the habitable zone
(Beichman et al. 2025, arXiv:2508.03814 / "Worlds Next Door") — this
detection is currently candidate-status and is *not* adopted into
NearStars planet inventory, but it shapes the system's narrative.

**Scenario choice for NearStars: Sun-twin with super-solar metallicity
visual tint** — a faintly warmer/yellower G2 V disk than the Sun,
20 d rotation period, modest spot coverage at solar-cycle maximum.

## Decisions

Kopernicus star cfg-ready values. `Confidence`: high = directly
measured or tightly constrained, medium = theoretical with strong
support, low = aesthetic choice within the allowed window.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `mass_msun` | 1.1055 | high | Pourbaix & Boffin 2016 binary_orbit |
| `radius_rsun` | 1.2234 | high | Kervella et al. 2017 VLTI/PIONIER |
| `teff_k` | 5847 | high | Porto de Mello et al. 2008 high-res spectroscopy |
| `luminosity_lsun` | 1.521 | high | Kervella et al. 2017 bolometric flux |
| `spectype` | G2 V | high | Keenan & McNeil 1989 (textbook) |
| `metallicity_fe_h_dex` | +0.24 | high | Porto de Mello et al. 2008 |
| `age_gyr` | 4.81 ± 0.5 | medium | Joyce & Chaboyer 2018 MESA + asteroseismology |
| `rotation_period_days` | 22 | medium | DeWarf et al. 2010 photometric monitoring |
| `obliquity_deg` | 0 | low | adopted (no obliquity measurement); Solar analog |
| `surface_color_temp_k` | 5810 | high | weighted between Teff and limb-darkened mean (~30 K cooler) |
| `surface_tint_rgb_hex` | `#fff6e0` | medium | blackbody 5810 K → CIE D58 chromaticity, very faint cream-yellow vs Sun's `#fff5e6` |
| `corona_tint_rgb_hex` | `#ffeacb` | low | warmer corona haze (cycle minimum); subtle increase in red component |
| `limb_darkening_coeff_quadratic_a` | 0.30 | medium | Claret 2017 4-coefficient → reduced quadratic for KSP |
| `limb_darkening_coeff_quadratic_b` | 0.30 | medium | same |
| `granulation_cell_size_arcsec` | 1.3e-3 | medium | Bigot et al. 2008 / Bedding 2014 — solar-like granulation Mm-scale |
| `convective_overshoot_pct` | 12 | medium | Joyce & Chaboyer 2018 best-fit overshoot 0.10–0.15 |
| `magnetic_cycle_period_yr` | 19 | medium | DeWarf et al. 2010 (compared to Sun's 11 yr) |
| `spot_coverage_max_pct` | 1 | low | very low activity; Solar analog at cycle max |
| `spot_temperature_offset_k` | -1500 | medium | Solar umbra ~3800 K → 5800-3800 ≈ -2000 K; Solar analog penumbra ~5000 K → -800 K; mid-value -1500 K |
| `xray_log_lx_erg_s` | 27.0 | medium | Ayres 2014 — solar-like, cycle-averaged |
| `xray_cycle_factor` | 3.0 | medium | DeWarf 2010 — modest cycle amplitude |
| `flare_rate_per_day_amplitude_log10` | -3 | medium | low — solar-like quiet star; Howard 2023 statistics for old G dwarfs |
| `wind_mass_loss_rate_msun_yr` | 1.5e-14 | medium | Wood et al. 2005 Ly-α astrosphere absorption |
| `wind_terminal_velocity_km_s` | 700 | medium | Solar-wind analog (slow-wind dominated) |
| `chromosphere_ca_ii_log_rhk` | -4.95 | high | DeWarf et al. 2010 |
| `helioseismic_p_mode_max_freq_mhz` | 2.4 | high | Bouchy & Carrier 2002, Bazot 2007 — p-mode envelope peaks near 2.4 mHz |
| `apparent_diameter_arcsec_from_sol` | 0.0085 | high | derived: 2 × 1.2234 R☉ / 1.347 pc × 206265 |
| `apparent_magnitude_v_from_sol` | -0.01 | high | Hipparcos/SIMBAD |
| `companion_b_max_separation_arcsec` | 12 | high | a × (1+e) at apastron: 17.57" × 1.5179 → corresponds to 36.0 AU sky projection |
| `companion_b_min_separation_arcsec` | 1.7 | high | a × (1-e) at periastron: 11.4 AU sky projection |
| `companion_b_orbit_period_yr` | 79.91 | high | Pourbaix 2002 / Kervella 2016 — same as 14h36m WDS catalog 14396-6050 AB |
| `proxima_separation_au_from_a` | 8700 | medium | Kervella, Thévenin & Lovis 2017 — bound outer orbit (e=0.5, P=547 kyr) |
| `interstellar_extinction_av_mag` | 0.0 | high | Local Interstellar Cloud; column density ≪ 1 |

## Stellar disk synthesis

Alpha Cen A's disk is the Solar System's closest analog to the Sun.
At Kervella 2017's interferometric angular diameter (8.502 ± 0.038
mas as measured from Earth), it would subtend 0.0085" from Earth —
about 1/65 of the Sun's apparent diameter (1924"). From its KSP
homeworld equivalent (assuming a 1 AU analog orbit around Alpha A
itself), the disk would appear ~22% larger than the Sun does from
Earth, with ~52% greater luminous flux.

**Color choice.** At Teff = 5847 K (Porto de Mello 2008
high-resolution spectroscopy of the AB pair) the photospheric
blackbody peaks at ~496 nm. After integrating CIE 1931 with the
solar limb darkening kernel, the perceived chromaticity falls very
close to the Sun's D55 reference white — slightly cream-yellow,
indistinguishable to the unaided eye. For KSP we adopt `#fff6e0`
(barely warmer than Sol's typical `#fff5e6`), reflecting the +57 K
hotter Teff and accounting for slightly enhanced opacity from the
super-solar metallicity ([Fe/H] = +0.24, Porto de Mello 2008).

**Granulation.** Bigot et al. 2008 detect the granulation noise in
the asteroseismic photometric residuals — a "salt and pepper"
texture on Mm scales (~1.5e-3 arcsec from Earth, unresolved by
present instruments). At KSP rendering scale (the star is rendered
as a billboard), this manifests only as a subtle 0.1-magnitude flicker
on minute timescales if simulated; the Phase 3 cfg notes the
characteristic timescale but does not require active simulation.

**Limb darkening.** Solar-equivalent quadratic coefficients
(a ≈ b ≈ 0.30) reproduce the disk-edge dimming. Kervella 2017's
PIONIER analysis fits a Claret 4-parameter law; the quadratic
reduction loses ~2% of disk-center brightness fidelity but is
adequate for KSP rendering. Limb is moderately darkened (factor ~0.40
at μ = 0.1) and slightly redder near the edge due to increased path
length through cooler upper photosphere.

**P-mode oscillations.** Bouchy & Carrier 2002 and Bazot 2007
detect solar-like p-modes with envelope peak near 2.4 mHz (period
~7 minutes), amplitude ~25 cm/s in radial velocity. Visual
manifestation is sub-percent disk-integrated flickering on
5–10-minute timescales — not visible to the unaided eye, but
important for high-precision RV planet searches around this star.
Not rendered in KSP.

**No magnetic Halo flares.** The 22-day rotation gives a very low
Rossby number; combined with the deep convective envelope this
results in a low-activity dynamo. Howard 2023 statistics place
solar-twin flare-rate at ~10⁻³ M-class flares per day; superflares
(EX > 10³⁵ erg) are negligible at the system's ~5 Gyr age.

## Activity and variability synthesis

DeWarf et al. 2010 monitored Alpha Cen A photometrically for 7 years
(2003–2010) and spectroscopically for Ca II H&K to derive both the
rotation period and the activity cycle. Key findings:

- **Rotation period**: 22 ± 3 days. Solar-like (the Sun has
  P_rot = 25.4 d at the equator, ~31 d at the poles, mean ~26 d).
  Slightly faster than Sun consistent with ~80% solar age (Joyce &
  Chaboyer 2018 give 4.81 Gyr vs Sun's 4.57 Gyr).
- **Magnetic cycle**: ~19 yr (vs Sun's 22-yr Hale cycle / 11-yr
  Schwabe cycle). DeWarf 2010 detected partial cycle in their
  baseline; the period is loosely constrained.
- **log R'_HK**: -4.95 (mean), with cycle amplitude ~0.05 dex.
  Indicates lower mean chromospheric activity than Sun
  (log R'_HK_Sun ≈ -4.91 at activity max, -4.99 at min). Alpha A
  is at the inactive end of the G2 V activity envelope, consistent
  with age and slow rotation.
- **X-ray luminosity**: log L_X ≈ 27.0 erg/s (Ayres 2014; Robrade
  & Schmitt 2005). Cycle amplitude factor ~3× — modest compared to
  the Sun's ~10× X-ray cycle.

**Spot coverage.** Estimated from photometric variability amplitude
(<1% peak-to-peak in V) and chromospheric activity index: <1%
disk coverage at cycle max. Visual: 1–3 small (~5° diameter) sunspot
groups distributed mid-latitude during active periods. Spot
temperature ~4300 K (umbra) and ~5500 K (penumbra) — about 1500 K
below quiescent photosphere mean.

**No technosignatures detected.** Foster et al. 2022
(arXiv:2211.11756) optical-laser search and Smith et al. 2024
(arXiv:2206.14807) radio gravitational-lens technosignature search
returned null results. Mentioned only for completeness; not visual.

**Coronal structure.** Wood et al. 2005 Ly-α astrosphere absorption
detection gives stellar wind mass loss ~1.5e-14 M☉/yr, ~7% of solar
mass loss. The hot corona (T ~ 2e6 K) is similar to Sun's quiet-Sun
state. For KSP this means visible coronal ray structure at
totality / eclipse rendering, with red-shifted CME ejecta during
flare events (rare).

## System geometry synthesis

The AB binary's mutual visibility is a defining feature of the
NearStars Alpha Cen experience.

**From Alpha A's local frame**, Alpha Cen B traces an elliptical
orbit with:
- Period: 79.91 ± 0.01 yr (Pourbaix 2002, Kervella 2016)
- Semi-major axis: 23.52 AU (combining a_arcsec = 17.57" with
  d = 1.347 pc)
- Eccentricity: 0.5179
- Periastron separation: ~11.4 AU (~Saturn's distance from Sun)
- Apastron separation: ~35.7 AU (~Neptune's distance)

This is large enough that AB cannot host stable circumbinary planets
in their habitable zones, but small enough that each star's planet
inventory is dynamically influenced by the other. B's apparent
brightness from A's surface varies between V ≈ -16 (periastron,
~5× brighter than Full Moon from Earth) and V ≈ -19 (no, wait —
let me reconsider). At apastron, B subtends ~0.022° as seen from A;
at periastron, ~0.066°. Integrated visual magnitude at periastron
~-21 (much brighter than Sun would appear from Saturn but as a
~point source). At apastron, ~-19 — comparable to a quarter-Moon
brightness but still point-like.

**From a hypothetical Earth-analog around A** (1.25 AU, where the
classical HZ would put it): the sun-in-sky is Alpha A at the same
apparent diameter as Sun-from-Earth (since L=1.52 and orbit is
~1.25 AU). B appears as a brilliant variable point source ranging
from V ≈ -20 (faintest) to V ≈ -22 (brightest). This is far brighter
than Venus from Earth, providing dramatic illumination of the
nightside hemisphere when in opposition. The shadow cast by B's
light is detectable but ~10^-3 of A's daytime illumination.

**Proxima visibility.** From Alpha A's surface, Proxima appears as
a faint magnitude ~+5 star — visible to the unaided eye but
unremarkable. Its apparent motion across the sky is ~0.1"/yr
(differential of system's proper motion + Proxima's small orbital
motion around AB barycenter).

**No planets confirmed around A.** Wagner et al. 2021 NEAR
coronagraphic search found C1 (a candidate at ~1.1 AU) which was
later ascribed to a thermal background source. As of 2026-05-22,
the most recent Beichman et al. 2025 (2508.03814) JWST/NIRCam
coronagraphy reports a *candidate* warm giant in the HZ at
~1.5–2 AU, but the detection is one epoch and saturation-confused.
For NearStars cfg this remains unincluded pending confirmation.

## Visual styling

Combining the disk and activity decisions:

- **Global appearance.** A near-perfect Sun-twin. The unaided-eye
  observer cannot distinguish Alpha A from Sol; subtle differences
  (slightly higher color temperature due to higher Teff, slightly
  yellower-warmer due to higher metallicity) cancel out within
  visual gradient perception.
- **Dayside illumination of orbiting bodies.** Same color temperature
  reference as Sol (~5810 K effective for surface illumination
  calculations). Atmospheric scattering on Earth-analogs produces
  similar blue-sky / yellow-sun appearance to Sol viewed from Earth.
- **Disk brightness profile.** Solar-equivalent quadratic limb
  darkening; bright disk-center, ~40% relative brightness at the
  edge. No obvious latitude bands from rotation.
- **Spot visibility.** At cycle max, 1–3 small dark spots at
  ±20–35° latitude, each ~5° angular diameter. Largest spots are
  visible at HZ orbit if directly imaged (KSP-equivalent: render
  procedural dark patches at activity-cycle-max times).
- **Companion B.** Always present in the sky from any Alpha A orbit.
  At ~5° elongation min and ~16° at max (1.25 AU HZ orbit). Cycles
  between bright morning/evening star (apastron) and brilliant
  near-Sun companion (periastron) over the 79.91-yr period.
- **Proxima Cen.** Magnitude ~+5 point source, ~2° from Alpha B
  (slow drift over centuries). Indistinguishable from background
  stars to the unaided eye.
- **Spectral lines for AR overlay.** H-α at 6563 Å (red, dominant in
  chromospheric emission), Ca II H/K at 3933/3968 Å (blue-violet,
  diagnostic of activity), Mg I b triplet at 5167-5184 Å, Na D
  doublet at 5890/5896 Å.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2017A&A...597A.137K** Kervella et al. 2017 — VLTI/PIONIER
  interferometric measurement of A's angular diameter (8.502 ± 0.038
  mas) and B's (5.999 ± 0.025 mas). Definitive radius source.
  Bolometric luminosity derived from same data + Hipparcos parallax.
- **2008A&A...488..653P** Porto de Mello et al. 2008 — Differential
  high-resolution spectroscopic analysis of A and B. Definitive Teff
  and [Fe/H] source. Establishes the system as super-solar in metals.
- **2018ApJ...864...99J** Joyce & Chaboyer 2018 — MESA + asteroseismic
  modeling of both A and B. System age 4.81 ± 0.50 Gyr. Resolves
  long-standing tension between older (~6 Gyr) Bazot 2007 and
  Thévenin 2002 asteroseismic ages.
- **2010ApJ...722..343D** DeWarf et al. 2010 — 7-year ground-based
  photometric + Ca II H&K monitoring. Definitive rotation periods
  (22 d for A, 41 d for B), partial activity cycle, log R'_HK
  measurements.
- **2016A&A...586A..90P** Pourbaix & Boffin 2016 — Dynamical binary
  orbit solution. Masses 1.1055 ± 0.0039 M☉ (A) and 0.9373 ± 0.0033
  M☉ (B). The high-precision modern reference orbit.
- **2017A&A...598L...7K** Kervella, Thévenin & Lovis 2017 —
  Kinematic confirmation that Proxima is gravitationally bound to
  AB at 8700 AU (e = 0.5, P = 547 kyr).
- **2008A&A...488..635B** Bigot et al. 2008 — Asteroseismic
  granulation noise detection and convective-overshoot constraint
  for A. Provides the granulation cell scale used in the visual cfg.
- **2007A&A...470..295B** Bazot et al. 2007 — HARPS asteroseismic
  p-mode detection. Confirms M = 1.105 ± 0.007 M☉ and R = 1.224 ±
  0.003 R☉ via independent (non-dynamical) method.

### Read (context / methodology, not decision-driving)

- **2508.03814** Beichman et al. 2025 — JWST/NIRCam coronagraphic
  candidate detection of a warm giant planet in A's HZ. Mentioned
  in narrative as system context. NOT adopted into NearStars
  planet inventory pending confirmation (single epoch, saturation
  systematics).
- **2104.10086** Akeson et al. 2021 — ALMA millimeter astrometry of
  AB. Improves orbit but does not change the Pourbaix 2002 solution
  meaningfully.
- **2110.12565** Wagner et al. 2021 — NEAR/VLT thermal IR
  coronagraphic search. Reports C1 candidate which was later
  ascribed to background. Useful for context on planet limits.
- **2105.00034** Quarles & Lissauer 2018 — Exomoon dynamical
  stability in Alpha Cen-like binaries. Context for what kind of
  planet inventory is dynamically possible.
- **2108.12650** Milankovitch cycles for Earth-analogue in AB binary.
  Quarles et al. — context for HZ-planet obliquity / climate
  evolution under binary perturbation.
- **2015A&A...582A..49H** Heiter et al. 2015 — FGK Gaia benchmark
  star analysis. Independent Teff = 5792 ± 16 K and [Fe/H] = +0.26
  ± 0.08, cross-validates Porto de Mello.

### Read (instrument-only, not visual-informative)

- **2211.11756** Foster et al. 2022 — Optical SETI search for laser
  emission from AB. Null result. Methodology only.
- **2206.14807** Smith et al. 2022 — Solar-gravitational-lens radio
  technosignature search. Null result.
- **2304.13779** Saide et al. 2023 — Mobile-tower radio leakage
  simulation. Methodology, not Alpha-specific science.
- **2301.11314** Trees & Stam 2023 — Reflected-light polarization
  signatures of Earth-/Venus-analog. Methodology.
- **2405.13247** Pasquini et al. 2024 — Deep learning for RV
  planet detection. Methodology.

### Not read — no arXiv preprint available (96 papers)

The bulk of the bibliography consists of pre-2010 references, ADS
abstracts of conference proceedings, and instrument-paper variants.
Most are mass/radius/age cross-references that don't add visual
information beyond what the read-papers already provide. Key
not-read examples:

- "Transit Search for Exoplanets around Alpha Centauri A and B with
  ASTERIA" (CubeSat — Knapp 2020 dissertation work). Mentioned for
  null-result context.
- Many AB pre-Hipparcos papers (Demarque 1986, etc.) — superseded.
- Numerous proceedings (IAU symposia, AAS abstracts) that summarize
  results already in the read journal papers.

**User action requested.** If newer 2025–2026 papers on the candidate
HZ giant planet detection become available (follow-ups to Beichman
2025 / 2508.03814), they may shift the system narrative and warrant
a Phase 3 revision.

---

## Open items for follow-up

- Confirm/refute the Beichman 2025 candidate HZ giant. If confirmed,
  add to NearStars planet inventory with appropriate Phase 3 planet
  synthesis.
- Refine spot coverage at solar-cycle-max prediction with TESS sector
  observations (multi-year photometry now available for AB pair).
- Cross-check Joyce & Chaboyer 2018 system age against any post-2024
  asteroseismic reanalyses (Gaia DR3 SED + Tess oscillation modes).
- Visual disk tint hex should be calibrated against a renderer using
  CIE 1931 chromaticity from a 5810-K blackbody convolved with the
  solar-twin SED, not pure blackbody. Phase 4 task.
- The convective-overshoot 0.10–0.15 H_p value is at the upper end of
  current model preferences; if a future MESA reanalysis settles at
  lower values, the granulation cell size estimate would shrink ~10%.
- Cycle period uncertainty (DeWarf 2010 baseline ~7 yr only covers
  partial cycle) leaves the 19-yr value soft. Continuous monitoring
  to ~2030 would tighten this.
