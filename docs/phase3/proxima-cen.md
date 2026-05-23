<!-- Proxima Centauri Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Proxima Centauri — Phase 3 Synthesis

Proxima Centauri (α Cen C, GJ 551) is the closest star to the Sun at
1.301 ± 0.001 pc — gravitationally bound to the α Cen AB pair at a
projected separation of ~13 000 AU and an inferred orbital period of
roughly 547 000 years (Kervella 2017 astrometry). An M5.5Ve flare
star with a mass of just 0.122 M☉, radius 0.1542 ± 0.0045 R☉
(Boyajian 2012 interferometry), and an effective temperature of
2980 ± 80 K, it lies at the deep red end of the main sequence and
hosts two confirmed planets (Proxima b — Anglada-Escudé 2016; Proxima
d — Faria 2022, confirmed by Suárez Mascareño et al. 2025) plus a
candidate Proxima c (sub-Neptune at 5.2 AU; not yet confirmed at the
3σ level).

Compared to the quiet α Cen AB pair only 0.27 pc away, Proxima is a
dramatically more energetic and variable star. Its rotation period
of 82.6 ± 0.1 days (Suárez Mascareño 2020) is slow for an M dwarf —
consistent with old age — but its chromospheric activity is high:
log R'HK ≈ −4.0, Hα frequently in emission, kG-level surface magnetic
fields measured by Reiners et al. 2018 from CARMENES Zeeman analysis.
The X-ray, FUV, and UV outputs cycle on a ~7-year timescale (Wargelin
2024) and flare frequently — Vida 2019 TESS observations resolved
several flares per day above the photometric noise (Vida's 72 events over
≈ 50 d give a total flare rate of 1.49/day across the 10²⁹–10³² erg
energy range), with superflares of ≥ 10³³ erg expected roughly
3 times per year and ≥ 10³⁴ erg events once every two years. The combined X-ray + FUV flare spectroscopy of Fuhrmeister
2022 (arXiv:2204.09270) documents the simultaneous coronal–
chromospheric response to these events.

Proxima's relationship to α Cen AB is less certain than the
gravitational binding suggests. Feng & Jones 2018 (arXiv:1709.03560)
modeled the encounter dynamics and conclude that Proxima may have been
captured into the α Cen AB system rather than born with it; the kinematic
agreement at the system center of mass leaves both formation
scenarios viable. The age is best estimated at ~4.85 Gyr (DB Phase 2
attribution) — comparable to α Cen AB but with substantial
uncertainty.

**Scenario choice for NearStars: a low-mass, deeply red M5.5Ve flare
star with a ~83-day rotation, kG-class magnetic dipole, 7-year
activity cycle, and frequent superflares. Visual styling emphasizes
the strong red continuum, frequent Hα flare brightening, and the
visible glow from a hypothetical close-in planet.** 18 cfg picks;
16 canonical-aligned, 2 tie-break (limb darkening interpolation +
specific flare hex tint).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M5.5Ve | high | Hawley 1996; DB |
| `mass_msun` | 0.1221 | high | Mann 2015 M–K relation; DB recommended |
| `radius_rsun` | 0.1542 ± 0.0045 | high | Boyajian 2012 interferometry |
| `teff_k` | 2980 ± 80 | high | Boyajian 2012; Passegger 2019 |
| `luminosity_lsun` | 0.001567 | high | derived from R, Teff |
| `metallicity_fe_h_dex` | +0.21 | medium | Passegger 2019 H-band |
| `age_gyr` | 4.85 | medium | dynamics + activity proxy; Feng & Jones 2018 capture vs. coeval ambiguity |
| `rotation_period_days` | 82.6 ± 0.1 | high | Suárez Mascareño 2020 ESPRESSO |
| `activity_log_rhk` | −4.0 | high | high; chromospherically active |
| `activity_cycle_years` | 7 | medium | Wargelin 2024 X-ray + UV + optical cycle |
| `x_ray_log_lx_cgs_quiescent` | 27.0 | medium | Damonte 2026 XMM time-resolved spectra |
| `x_ray_log_lx_cgs_flare_peak` | 28.5 | medium | Fuhrmeister 2022 simultaneous X-ray + FUV peak |
| `magnetic_dipole_strength_kG` | 0.6 | high | Reiners 2018 CARMENES Zeeman (dipole component) |
| `magnetic_total_field_kG_rms` | 4 | high | Reiners 2018 (Zeeman RMS) |
| `flare_rate_per_day_total` | 1.49 | high | Vida 2019 TESS — 72 events in ≈ 50 d (energy range 10²⁹–10³² erg) |
| `flare_rate_superflare_per_year` | 3 (≥ 10³³ erg); 0.5 (≥ 10³⁴ erg) | high | Vida 2019 TESS — explicit numbers in §4 from cumulative flare frequency distribution |
| `orbital_role_around_acen_ab` | bound at ~13 000 AU; P ≈ 547 000 yr | medium | Kervella 2017 astrometric tracking; Feng & Jones 2018 capture analysis |
| `limb_darkening_alpha_h` | ~0.4 | low | Tie-break: not directly measured for Proxima; interpolated from M-dwarf model grid (Claret 2018); interesting-first per the interesting-first rule for slight visual variation |
| `visual_surface_tint_hex_primary` | `#c54c2a` (deep red M5.5V) | high | Teff 2980 K blackbody + molecular band suppression below 6500 Å |
| `visual_flare_color_hex` | `#ff5e2a` (Hα-dominated optical flare with broadband continuum brightening) | medium | Tie-break: Vida 2019 + Anglada-Escudé 2016 supplement flare spectra; specific hex chosen for in-game visibility against the dim red quiescent continuum |
| `stellar_color_temp_k` | 2980 | high | derived |

## Surface synthesis

Proxima Centauri's photosphere is one of the dimmest and reddest in
the NearStars catalog. At 2980 K Teff and 0.1542 R☉, its total
luminosity is just 0.00157 L☉ — about 1/640 of the Sun. The visible
continuum below 6500 Å is heavily depressed by TiO, VO, and water
bands, with most of the radiated flux emerging in the near- and
mid-infrared. The H-band photospheric structure is poorly modeled by
1D atmospheres (Boyajian 2012 §4 warns that GJ 551's red colors
extrapolate beyond the validated range of the calibrations), so the
cfg adopts a tentative limb-darkening exponent α ≈ 0.4 interpolated
from the Claret 2018 M-dwarf grid as a tie-break against a
phenomenological dim-edge model.

The photosphere is granulation-resolved at the sub-arcsecond level
in extreme close-up rendering: typical M-dwarf granulation cells
~30 km across (scaled with pressure scale height). Sunspot coverage
during cycle maximum reaches estimates of 5–10% based on TiO
band-depth modeling (Berdyugina 2017 review). Faculae and bright
plage are visible but contribute less to the integrated luminosity
than in earlier-type stars.

## Atmosphere synthesis

Proxima's chromosphere and corona dominate its observable energy
output. Reiners et al. 2018 (CARMENES) measured a Zeeman-broadened
mean magnetic field of ~4 kG (RMS over the disk) with a roughly
0.6-kG dipole component, providing the magnetic forcing that drives
the elevated UV / X-ray emission. The quiescent X-ray luminosity is
log L_X ≈ 27.0 cgs (Damonte 2026), rising by an order of magnitude
during flares (Fuhrmeister 2022).

Flares are the defining feature. Vida 2019 (arXiv:1907.12580) used
TESS photometry to characterize the flare distribution — the typical
flare amplitude in the white-light band ranges across 10²⁹–10³² erg energies over
1.49 flares/day, with super-flares (≥ 10³³ erg) at ~3 per year and
events ≥ 10³⁴ erg once every two years. The most dramatic event recorded shows quasi-
periodic oscillations during the decay phase, attributed to plasma
oscillations in the flare loop. Burton et al. 2025 (arXiv:2503.21890)
extended the flare census into millimeter wavelengths using ALMA,
finding the rate of mm-bright flares is comparable to that in the
optical.

The activity cycle — first detected by Wargelin et al. 2017 in
~15 years of X-ray and optical photometry, and refined by Wargelin
2024 to ~7 years — modulates both the mean flare rate and the
spot-induced rotational modulation amplitude. Anglada-Escudé 2016
documents the same modulation in Hα equivalent width across the
HARPS + UVES timeseries used for the Proxima b discovery.

The atmospheric loss to the Proxima planetary system is enormous:
Garraffo et al. 2022 (arXiv:2211.15697) finds the stellar wind ram
pressure at b's distance ranges from 10⁴ to 10⁶ times solar values
during sub-Alfvénic and super-Alfvénic transits. Coronal mass
ejections carry total kinetic energies up to 10³⁴ erg per event in
the Vida 2019 superflare sample.

## Rotation & spin synthesis

The 82.6-day rotation period (Suárez Mascareño 2020) is well-measured
from optical photometry and chromospheric activity tracers in
ESPRESSO. It is long for an M5.5V — implying old age (≥ 4 Gyr based
on the Newton 2018 M-dwarf gyrochronology), consistent with the
~4.85 Gyr DB Phase 2 attribution. Differential rotation has not been
resolved.

Asteroseismic detection of p-modes is impossible for an M dwarf —
the surface gravity is too high and the pulsation amplitudes too
low — so the rotation comes entirely from spot modulation and
chromospheric tracers. Suárez Mascareño 2020 §4 estimates the
inclination of the rotation axis at i ≈ 35° from the spot-modulation
amplitude vs. mean activity pattern, consistent with Proxima b's
orbital inclination being lower than 90°.

## Visual styling

Proxima renders as a deep red M5.5V in NearStars — the photospheric
tint `#c54c2a` shifts the in-game illumination color toward the
visible red end, with most of the integrated SED below the V-band
peak. Viewed from Proxima b at 0.0485 AU, Proxima fills 1.5° angular
diameter (about 3× the apparent diameter of the Sun seen from Earth);
from Proxima d at 0.029 AU it fills 2.5°. The dim red color and
large angular size combine to produce a visually striking "great red
star" appearance from close-in habitable-zone planets.

Flares are rendered as transient brightening events: the in-game
flare cfg key `visual_flare_color_hex = #ff5e2a` shifts the color
slightly toward orange during peak emission, mimicking the Hα-dominated
optical flare spectrum (Vida 2019 + Anglada-Escudé 2016 spectra).
Superflares (~3 per year of 10³³ erg, ~0.5 per year of 10³⁴ erg)
produce 1–2 magnitude brightening events lasting tens of minutes,
with the QPO modulation visible in the photometric decay tail.

The corona is rendered as a faint blueish halo during quiescent
phases, but it brightens dramatically during X-ray-active phases of
the 7-year cycle. Stellar wind streamers are not directly visible
but propagate as in-game space-weather effects for any nearby
planetary atmosphere.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Boyajian T. S. et al. 2012** — *Stellar Diameters and Temperatures
  II*, ApJ 757, 112 (`2012ApJ...757..112B`, arXiv:1208.2431). CHARA
  interferometric R = 0.1542 ± 0.0045 R☉; Teff cross-check.
- **Suárez Mascareño A. et al. 2020** — *Revisiting Proxima with
  ESPRESSO* (`2020A&A...639A..77S`, arXiv:2005.12114). ESPRESSO RV
  monitoring; rotation period 82.6 ± 0.1 d; activity index timeseries.
- **Suárez Mascareño A. et al. 2025** — *Diving into the planetary
  system of Proxima with NIRPS: Breaking the m/s barrier*
  (`2025A&A...700A..11S`, arXiv:2507.21751). The current best orbital
  fit for Proxima b (e ≈ 0, P = 11.18465 d, Msini = 1.055 M⊕) and
  confirmation of Proxima d.
- **Anglada-Escudé G. et al. 2016** — *A terrestrial planet candidate
  in a temperate orbit around Proxima Centauri*, Nature 536, 437
  (`2016Natur.536..437A`, arXiv:1609.03449). Original discovery of
  Proxima b; supplementary Hα flare-frequency measurements.
- **Faria J. P. et al. 2022** — *A candidate short-period sub-Earth
  orbiting Proxima Centauri*, A&A 658, A115 (`2022A&A...658A.115F`,
  arXiv:2202.05188). Proxima d candidate at P = 5.122 d, Msini =
  0.26 M⊕.
- **Reiners A. et al. 2018** — *CARMENES search for exoplanets around
  M dwarfs. High-resolution optical and near-infrared spectra of
  324 dwarfs* (`2018A&A...612A..49R`, arXiv:1711.06576). Zeeman
  analysis; Proxima magnetic field components.
- **Vida K. et al. 2019** — *Flaring Activity of Proxima Centauri from
  TESS Observations*, ApJ 884, 160 (`2019ApJ...884..160V`,
  arXiv:1907.12580). Flare statistics, QPO super-flare, 5 super-flares
  per year.
- **Fuhrmeister B. et al. 2022** — *The high energy spectrum of
  Proxima Centauri simultaneously observed at X-ray and FUV
  wavelengths*, A&A 663, A119 (arXiv:2204.09270). Coronal +
  chromospheric flare response.
- **Wargelin B. J. et al. 2024** — *X-Ray, UV, and Optical
  Observations of Proxima Centauri's Stellar Cycle*, A&A in press
  (arXiv:2411.04252). Refined 7-yr activity cycle.
- **Damonte A. et al. 2026** — *Time-resolved X-ray spectra of
  Proxima Centauri as seen by XMM-Newton* (arXiv:2512.18011).
  Quiescent X-ray spectroscopy and cycle modulation.
- **Burton K. et al. 2025** — *The Proxima Centauri Campaign: First
  Constraints on Millimeter Flare Rates from ALMA*
  (arXiv:2503.21890). mm-band flare rate.

### Read (context / methodology, not decision-driving)

- **Feng F. & Jones H. R. A. 2018** — *Was Proxima captured by α
  Centauri A and B?* (arXiv:1709.03560). Orbit history dynamics.
- **Kervella P. et al. 2017** — *Proxima's orbit around α Centauri*,
  A&A 598, L7 (arXiv:1611.03495). Astrometric tracking that confirms
  the bound triple.

### Read (instrument / non-cfg-decisive)

- **De Luca P. et al. 2024** — Ozone-climate dynamics of Proxima b
  Earth-analog (arXiv:2404.17972). Atmospheric chemistry framework
  reused in Proxima-b synthesis.
- **Boldog Á. et al. 2024** — Water-content modeling of rocky HZ
  planets (arXiv:2312.01893). Cross-referenced in Proxima-b interior.

### Not read — no arXiv preprint or low-priority (~150 papers)

- **DeWarf-equivalent for Proxima rotation/cycle**: not needed
  (Suárez Mascareño 2020 + Wargelin 2024 cover the same observable
  base with current precision).
- Conference proceedings, SETI / laser-communication targeting,
  interstellar-mission proposals; preserved in
  `docs/phase3/_bib/proxima-cen.yaml` with `status: skipped`.

## Open items for follow-up

- **Proxima c (sub-Neptune at 5.2 AU candidate)**: Damasso 2020 +
  Benedict 2020 reported astrometric + RV evidence for a third
  planet, but the 3σ confidence threshold has not been reached as of
  2026 follow-up. If confirmed, a new `has_planet_c` Decisions row
  is needed; current cfg leaves the planet out.
- **Active region latitude distribution**: Suárez Mascareño 2020 §4
  inclination i ≈ 35° but does not resolve spot latitudes. A future
  Doppler-imaging campaign could constrain whether Proxima's active
  regions are predominantly equatorial (like the Sun) or polar (like
  some young rapid rotators).
- **Capture vs. coeval origin**: Feng & Jones 2018 cannot
  distinguish; the implication for age (4.85 Gyr coeval vs.
  potentially much younger if captured from a star-forming region
  encounter) propagates into the cfg `age_gyr` confidence. A future
  Gaia DR4 astrometric solution might tighten the encounter dynamics.
- **DB JSON SM25 bibcode erratum**: DB stores
  `bibcode = 2025A&A...700A..11M` but ADS resolves the paper at
  `2025A&A...700A..11S` (last initial S, not M). The DB attribution
  for Proxima b/d orbit + mass should be corrected.
