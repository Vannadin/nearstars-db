<!-- Alpha Cen A/B + Proxima Cen Phase 2 curation — decisions and rationale -->
# Alpha Centauri (A, B) + Proxima Cen — Phase 2 Curation Context Notes

Append-only log. 2026-05-22.

## Scope

Three stars + two planets. The system is the closest stellar system to
Sol; existing curated entries had only mass/radius single-point values
(plus Suárez Mascareño 2025 for Proxima, with a garbled-encoded
reference string from raw ingest). Phase 2 escalates to:

- Mass / radius / Teff / luminosity / age / metallicity / rotation / activity
  arrays for each of the three stars.
- Multi-paper orbital + physical arrays for Proxima b, d.

## Why now

Phase 3 synthesis is about to write 5 visual-cfg synthesis documents
(Alpha A, Alpha B, Proxima, Proxima b, Proxima d). Those should read
from Phase 2 measurement arrays, not Phase 1 single dicts.

## Paper selection — Alpha Cen A

Alpha Cen A is the best-studied G2V star outside the Sun. Mass is
overdetermined: a direct binary-orbit dynamical solution (Pourbaix &
Boffin 2016, refined by Kervella et al. 2016) plus asteroseismic
modeling (Bazot 2007/2016; Thévenin 2002; Joyce & Chaboyer 2018).

Recommended choice:
- **Mass**: Pourbaix & Boffin 2016 (binary_orbit, 0.35% uncertainty).
  Direct dynamical measurement supersedes model-dependent
  asteroseismic results.
- **Radius**: Kervella 2017 (interferometry, 0.43% uncertainty). VLTI/
  PIONIER definitive 2017 update over the 2003 VINCI result.
- **Teff**: Porto de Mello 2008 (high_res_spectroscopy, 0.46%). Best
  spectroscopic determination; Heiter 2015 benchmark uses similar
  methodology but slightly different reduction.
- **Luminosity**: Kervella 2017 — derived from bolometric flux +
  Hipparcos parallax. Other older bolometric estimates supersede.
- **Age**: Joyce & Chaboyer 2018 (MESA + asteroseismology) — most
  recent comprehensive modeling. Significant tension with Bazot 2007
  (6.52 Gyr) and Thévenin 2002 (6.41 Gyr); resolved partially by Bazot
  2016 (4.4 Gyr). Field consensus has been migrating toward the
  younger value (~5 Gyr).
- **Metallicity**: Porto de Mello 2008 — high-precision differential
  abundance analysis specifically optimized for the Alpha Cen system.
- **Rotation/Activity**: DeWarf et al. 2010 — only paper with both
  rotation period and activity cycle for Alpha Cen A from ground-based
  photometric monitoring.

## Paper selection — Alpha Cen B

Symmetric treatment with Alpha Cen A. Same papers contribute:
- Pourbaix & Boffin 2016 (binary_orbit mass)
- Kervella 2017 (interferometric radius)
- Bigot 2006 (independent VLTI VINCI Alpha B paper)
- Joyce & Chaboyer 2018 (system age — same value for A and B since
  they're coeval)
- DeWarf 2010 (rotation period, ~41 d; longer than A due to lower
  mass and higher Rossby number)

## Paper selection — Proxima Cen

Proxima is bound to Alpha AB (Kervella, Thévenin, Lovis 2017) so the
age is constrained to be the same as the system age. M-dwarf mass /
radius are hardest to measure directly; key papers:

- **Mass**: Mann et al. 2019 K-band-magnitude empirical relation gives
  M=0.1221 ± 0.0035 M_sun. This matches the Suárez Mascareño 2025
  value (which itself derives from similar methodology). Anglada
  Escudé 2016 discovery paper used 0.120 ± 0.015 (less precise).
- **Radius**: Boyajian 2012 CHARA interferometry definitive
  measurement R=0.1410 ± 0.0070 R_sun. Demory 2009 VLTI value
  agrees but with larger error.
- **Teff**: Passegger 2019 CARMENES analysis — 2904 ± 51 K. Pineda
  2021 and Cifuentes 2020 also overlap. The Suárez Mascareño 2025
  value of 3498 K (in raw entry) appears anomalous — most M5.5Ve
  determinations are in the 2850–3050 K range. Will reconcile with
  recommended=Passegger 2019.

  **NOTE**: The existing raw value teff_k=3498 K comes from a
  CARMENES recipe paper (Cifuentes 2021), but most spectroscopic
  determinations place Proxima Teff in the 2850–3050 K range. The
  value 3498 K is high. The recommended teff_measurements entry
  should use the more conventional value. The derived block will
  pick from the recommended array entry, overriding the raw.

- **Rotation**: Suárez Mascareño 2016 — definitive 83-day period from
  long-baseline ASAS+HARPS data. Klein 2021 ZDI gives a slightly
  longer value but consistent within errors.
- **Activity**: Same paper, log R'HK = -5.55 (very inactive; old M
  dwarf consistent with system age).

## Paper selection — Proxima b and d

- **Anglada-Escudé 2016** — discovery of b. Cited values: P=11.186,
  Msini=1.27.
- **Faria 2022** — ESPRESSO discovery of d (5.12 d) + refined b
  parameters. Msini(d) = 0.26 ± 0.05.
- **Suárez Mascareño 2025** — most recent comprehensive RV analysis
  combining HARPS + ESPRESSO + ESPRESSO-NIR. Refined parameters for
  both planets. **Recommended for both.**

## Method label decisions

### Stellar

- `binary_orbit` for Pourbaix & Boffin, Kervella 2016 (binary
  parallax + RV → mass).
- `asteroseismology` for Bazot 2007/2016, Thévenin 2002 (p-mode
  modeling).
- `evolutionary_model` for Joyce & Chaboyer 2018 (MESA + seismic
  constraint, but the mass is the model output).
- `interferometry` for Kervella 2003/2017, Bigot 2006/2008, Boyajian
  2012, Demory 2009 — direct angular diameter measurement.
- `sed_fitting` for Schweitzer 2019, Cifuentes 2020 — broadband
  photometry to fit synthetic spectra.
- `spectroscopic_calibration` for Mann 2019 — K-band absolute
  magnitude → mass.
- `high_res_spectroscopy` for Porto de Mello 2008, Heiter 2015,
  Passegger 2019, Pineda 2021 — line-by-line abundance / Teff fit.
- `bolometric_flux` for luminosity (Kervella 2017, Boyajian 2012,
  Demory 2009) — integrated SED flux.
- `photometric_variability` for rotation (DeWarf 2010, Suárez
  Mascareño 2016, Benedict 1998) — long-term photometric monitoring.
- `zeeman_doppler` for rotation (Klein 2021) — magnetic-imaging
  derived rotation.
- `ca_ii_h_k` for activity (Henry 1996, DeWarf 2010, Suárez
  Mascareño 2016) — Ca II H&K line emission index.
- `isochrone` for Joyce & Chaboyer 2018 age (uses MESA isochrone
  fits to seismic frequencies).
- `kinematic` for Kervella 2017 Proxima age (bound-companion
  inference rather than direct dating).

### Planet

- `rv` for all Proxima b/d measurements (no transits, no astrometry,
  no TTV).

## Tier ordering and recommendation rules

For each measurement category, pick the entry with:
1. Most direct method (dynamical > model > calibration)
2. Smallest fractional uncertainty
3. Most recent publication (for ties)

This was applied to mark recommended=true for each entry.

## Edge case: Proxima teff disagreement

The raw entry has Teff=3498 K (Cifuentes 2020 reanalysis), but
Anglada Escudé 2016 reports 3050 K, Passegger 2019 reports 2904 K,
Pineda 2021 reports 2900 K. The 3498 K value is anomalous for an
M5.5Ve dwarf.

Recommended choice: Passegger 2019 (2904 ± 51 K) based on
high-resolution CARMENES infrared spectroscopy with a temperature
scale calibrated against asteroseismic benchmark M dwarfs. This will
update the derived block's teff_k.

Phase 3 synthesis should use ~2900 K for surface visual color
temperature, not 3498 K.
