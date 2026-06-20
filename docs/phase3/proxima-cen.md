# Proxima Centauri — Phase 3 Synthesis

Proxima Centauri (α Cen C, GJ 551) is the closest star to the Sun at
1.301 ± 0.001 pc — gravitationally bound to the α Cen AB pair at a
projected separation of ~13 000 AU and an inferred orbital period of
roughly 547 000 years (Kervella 2017 astrometry). An M5.5Ve flare
star with a mass of just 0.122 M☉, radius 0.141 ± 0.011 R☉
(Demory et al. 2009 VLTI/VINCI interferometry), and an effective
temperature of 2904 ± 51 K, it lies at the deep red end of the main sequence and
hosts two confirmed planets (Proxima b — Anglada-Escudé 2016; Proxima
d — Faria 2022, confirmed by Suárez Mascareño et al. 2025) plus a
candidate Proxima c (sub-Neptune at 5.2 AU; not yet confirmed at the
3σ level).

Compared to the quiet α Cen AB pair only 0.27 pc away, Proxima is a
dramatically more energetic and variable star. Its rotation period
of 83.5 ± 0.5 days (Benedict et al. 1998 HST photometry; modern
Suárez Mascareño work corroborates ~83 d — SM2020 adopts 83.2, SM2025
GP fit gives 83.2 ± 1.6) is slow for an M dwarf, consistent with old
age. As an old, slow rotator it is only moderately-to-weakly active by
the quiescent chromospheric measure — log R'HK ≈ −5.65 ± 0.17
(Suárez Mascareño et al. 2016 Ca II H&K) — yet it still flares
frequently, with Hα often in emission and a moderate ~0.6 kG mean
surface field (Reiners & Basri 2008; Reiners 2022 CARMENES) plus a
~0.2 kG mostly-poloidal large-scale field (Klein 2021 SPIRou ZDI).
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
star with a ~83-day rotation, moderate ~0.6 kG mean surface field (sub-kG large-scale dipole), 7-year
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
| `radius_rsun` | 0.141 ± 0.011 | high | Demory et al. 2009 (VLTI/VINCI interferometry) |
| `teff_k` | 2904 ± 51 | high | Passegger et al. 2019 high-res spectroscopy (consistent with SM2020/2025 adopted 2900 ± 100) |
| `luminosity_lsun` | 0.001567 | high | derived from R, Teff |
| `metallicity_fe_h_dex` | +0.21 | medium | Passegger 2019 H-band |
| `age_gyr` | 4.85 | medium | dynamics + activity proxy; Feng & Jones 2018 capture vs. coeval ambiguity |
| `rotation_period_days` | 83.5 ± 0.5 | high | Benedict et al. 1998 (HST photometric); modern SM corroborates ~83 d (SM2020 adopts 83.2; SM2025 GP 83.2 ± 1.6); Zapatero Osorio 2026 (`2605.22925`) ESPRESSO photospheric 84.9 ± 0.6 d, consistent within ~2σ. Value retained |
| `activity_log_rhk` | −5.65 ± 0.17 | high | Suárez Mascareño et al. 2016 (Ca II H&K; SM2020 recalibrates to −4.98) — old slow rotator, low/moderate quiescent activity |
| `activity_cycle_years` | 7 | medium | Wargelin 2024 X-ray + UV + optical cycle |
| `x_ray_log_lx_cgs_quiescent` | 27.0 | medium | Damonte 2026 XMM time-resolved spectra |
| `x_ray_log_lx_cgs_flare_peak` | 28.5 | medium | Fuhrmeister 2022 simultaneous X-ray + FUV peak |
| `magnetic_dipole_strength_kG` | 0.135 | high | Klein et al. 2021 — SPIRou ZDI large-scale dipole component (135 G; large-scale field ~200 G, mostly poloidal) |
| `magnetic_total_field_kG_rms` | 0.6 | high | Reiners & Basri 2008 / Reiners 2022 — mean (small-scale) surface field Bf ≈ 0.6 kG; "moderate", consistent with the long ~83 d rotation |
| `flare_rate_per_day_total` | 1.49 | high | Vida 2019 TESS — 72 events in ≈ 50 d (energy range 10²⁹–10³² erg) |
| `flare_rate_superflare_per_year` | 3 (≥ 10³³ erg); 0.5 (≥ 10³⁴ erg) | high | Vida 2019 TESS — explicit numbers in §4 from cumulative flare frequency distribution |
| `orbital_role_around_acen_ab` | bound at ~13 000 AU; P ≈ 547 000 yr | medium | Kervella 2017 astrometric tracking; Feng & Jones 2018 capture analysis |
| `limb_darkening_alpha_h` | ~0.4 | low | Tie-break: not directly measured for Proxima; interpolated from M-dwarf model grid (Claret 2018); interesting-first per the interesting-first rule for slight visual variation |
| `visual_surface_tint_hex_primary` | `#c54c2a` (deep red M5.5V) | high | Teff 2904 K blackbody + molecular band suppression below 6500 Å |
| `visual_flare_color_hex` | `#ff5e2a` (Hα-dominated optical flare with broadband continuum brightening) | medium | Tie-break: Vida 2019 + Anglada-Escudé 2016 supplement flare spectra; specific hex chosen for in-game visibility against the dim red quiescent continuum |
| `stellar_color_temp_k` | 2904 | high | derived |

## Surface synthesis

Proxima Centauri's photosphere is one of the dimmest and reddest in
the NearStars catalog. At 2904 K Teff and 0.141 R☉, its total
luminosity is just 0.00157 L☉ — about 1/640 of the Sun. The visible
continuum below 6500 Å is heavily depressed by TiO, VO, and water
bands, with most of the radiated flux emerging in the near- and
mid-infrared. The H-band photospheric structure is poorly modeled by
1D atmospheres (M-dwarf model atmospheres extrapolate the deep red
molecular bands beyond their validated range), so the
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
output. Reiners & Basri 2008 and Reiners 2022 (CARMENES) measured a
moderate mean surface field Bf ≈ 0.6 kG, and Klein 2021 (SPIRou ZDI)
recovered a ~0.2 kG mostly-poloidal large-scale field with a ~0.135 kG
dipole component, providing the magnetic forcing that drives
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

The ~83.5-day rotation period (Benedict et al. 1998 HST photometry)
is corroborated by modern optical photometry and chromospheric activity
tracers — SM2020 adopts 83.2 d and the SM2025 GP fit gives 83.2 ± 1.6 d.
It is long for an M5.5V — implying old age (≥ 4 Gyr based
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

- **Demory B.-O. et al. 2009** — *Mass-radius relation of low and very
  low-mass stars revisited with the VLTI*, A&A 505, 205
  (`2009A&A...505..205D`, arXiv:0906.0602). VLTI/VINCI interferometric
  R = 0.141 ± 0.011 R☉ — the recommended Proxima radius.
- **Passegger V. M. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Photospheric parameters of target stars from
  high-resolution spectroscopy* (`2019A&A...627A.161P`,
  arXiv:1907.00807). High-res spectroscopic Teff = 2904 ± 51 K and
  H-band metallicity.
- **Suárez Mascareño A. et al. 2016** — *Characterization of the radial
  velocity signal induced by rotation in late-type dwarfs*
  (`2016A&A...595A..12S`, arXiv:1506.08039). Ca II H&K activity index
  log R'HK = −5.65 ± 0.17 for GJ 551 (recalibrated to −4.98 in SM2020).
- **Suárez Mascareño A. et al. 2020** — *Revisiting Proxima with
  ESPRESSO* (`2020A&A...639A..77S`, arXiv:2005.12114). ESPRESSO RV
  monitoring; adopts rotation period ~83.2 d (87 ± 12 d measured);
  recalibrated activity index timeseries.
- **Suárez Mascareño A. et al. 2025** — *Diving into the planetary
  system of Proxima with NIRPS: Breaking the m/s barrier*
  (`2025A&A...700A..11S`, arXiv:2507.21751). The current best orbital
  fit for Proxima b (e ≈ 0, P = 11.18465 d, Msini = 1.055 M⊕) and
  confirmation of Proxima d; GP rotation period 83.2 ± 1.6 d.
- **Benedict G. F. et al. 1998** — *Photometry of Proxima Centauri and
  Barnard's Star Using Hubble Space Telescope Fine Guidance Sensor 3*,
  AJ 116, 429 (`1998AJ....116..429B`). HST/FGS3 photometric rotation
  period 83.5 ± 0.5 d — the recommended Proxima rotation period.
- **Anglada-Escudé G. et al. 2016** — *A terrestrial planet candidate
  in a temperate orbit around Proxima Centauri*, Nature 536, 437
  (`2016Natur.536..437A`, arXiv:1609.03449). Original discovery of
  Proxima b; supplementary Hα flare-frequency measurements.
- **Faria J. P. et al. 2022** — *A candidate short-period sub-Earth
  orbiting Proxima Centauri*, A&A 658, A115 (`2022A&A...658A.115F`,
  arXiv:2202.05188). Proxima d candidate at P = 5.122 d, Msini =
  0.26 M⊕.
- **Reiners & Basri 2008 / Reiners et al. 2022 / Klein et al. 2021** —
  Proxima magnetic field. Reiners & Basri 2008 (`2008A&A...489L..45R`,
  arXiv:0808.2986) and Reiners 2022 (`2022A&A...662A..41R`,
  arXiv:2204.00342, CARMENES) give a moderate mean surface field
  Bf ≈ 0.6 kG; Klein 2021 (`2021MNRAS.500.1844K`, arXiv:2010.14311,
  SPIRou ZDI) recovers a ~0.2 kG mostly-poloidal large-scale field with
  a ~0.135 kG dipole. (Supersedes the earlier mis-citation to the
  Reiners 2018 CARMENES spectral atlas `1711.06576`, which carries no
  Proxima field measurement.)
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

## Stellar wind / astrosphere

Proxima has a **compact astrosphere** — its weak wind (Ṁ ≤ 0.2 Ṁ⊙ upper limit,
Wood 2001) stands off the local ISM at only **≲55 AU**. The crucial point for a
radiation layer: although Proxima looks quiescent by the chromospheric measure
(log R'HK underrepresents M-dwarf activity), it is a violent **flare star**, so
its crew-relevant particle radiation is far HARSHER than the Sun's —
flare-dominated, not wind-dominated. Its activity cycles on ~7 yr (Wargelin
2017). It shares the same local interstellar flow as α Cen (V_ISM ≈ 25 km/s).

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `solar_cycle_yr` | 7 | medium | Wargelin 2017 (ASAS V-band + X-ray/UV) |
| `stellar_wind_mass_loss_solar` | ≤ 0.2 (upper limit) | medium | Wood 2001 astrospheric Lyα |
| `local_ism_inflow_speed_kms` | ~25 | medium | Wood 2005 (LIC; same flow as α Cen) |
| `astrosphere_standoff_au` | ≲ 55 (upper bound) | medium | 120·√(Ṁ_rel)·(V_⊙/V_ISM) from the Ṁ upper limit. Assumes a Sun-like wind speed (V_⊙ ≈ 400 km/s, fixed-velocity assumption of Wood et al. 2002/2005); only Ṁ and V_ISM vary per star |
| `stellar_radiation_surface_relative_sun` | ~5 | medium | quiescent L_X now measured at 0.3–2× solar (Wargelin R_X −4.4; NEXXUS 27.22); flare-weighted boost on top (5-mmag flares ~63/day, U-band ~1.4/hr). Quiescent-only canonical alternative: ~0.3 |
| `astrosphere_apex_ra_deg` / `_dec_deg` | ~185 / +42 | low | 6D astrometry vs LIC; **plugin-only** |

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

## Related

- [alpha-centauri-a](alpha-centauri-a.md), [alpha-centauri-b](alpha-centauri-b.md) — wide CPM companions at ~13,000 AU (P ≈ 547 kyr; Kervella 2017). Capture-vs-coeval origin remains unresolved (Feng & Jones 2018).
- [proxima-cen-b](proxima-cen-b.md), [proxima-cen-d](proxima-cen-d.md) — confirmed planetary system; b is the HZ rocky world, d the USP sub-Earth
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — Proxima's outer orbit around AB barycenter is the canonical hierarchical/static-CPM example (§6)
- [methodology](../reference/methodology.md) — DB schema source
- [rex-data-comparison](../reference/rex-data-comparison.md) — §3 Proxima T_eff is the notable Phase 3 → REX disagreement (3498 K vs 3042 K, NS uses Suárez Mascareño 2025)
