# Context Notes — AU Mic Phase 2 + Phase 3 reconciliation

## Pattern source

Mirrors Delta Pavonis (commit 4d26495). Append-only edit to
`db/stellar_props_curated.json` (no overwrite of any other host).

## Anchor paper picks

| Category | Recommended | Method tier | Rationale |
|---|---|---|---|
| mass | Wittrock 2023 (2023AJ....166..232W) | evolutionary_model (TTV+N-body dynamical) | M = 0.51 ± 0.028 Msun; tightest formal uncertainty, model-independent (orbital dynamics) |
| radius | Donati 2023 (2023MNRAS.525..455D) | spectroscopic_calibration | R = 0.82 ± 0.02 Rsun (ZDI v sin i + P_rot = 4.86 d, sin i ≈ 1); AU Mic at dec −31 is within CHARA reach but no published interferometric diameter exists; Donati ZDI is the tightest available radius |
| Teff | Plavchan 2020 (2020Natur.582..497P) | high_res_spectroscopy | 3700 ± 100 K from spectroscopic anchor in the discovery paper; Gaia DR3 GSP-Phot gives 3518 K (cross-check, lower because BP/RP is poorly calibrated below 3800 K for young M dwarfs) |
| luminosity | Plavchan 2020 (2020Natur.582..497P) | bolometric_flux | L = 0.09 ± 0.02 Lsun from SED bolometric integration |
| age | Mamajek & Bell 2014 (2014MNRAS.445.2169M) | isochrone (+LDB) | 22 ± 3 Myr for β Pic MG; AU Mic canonical member; LDB-anchored isochronal age |
| [Fe/H] | Shkolnik 2017 (2017ApJ...838...87S) | spectroscopic_calibration | β Pic MG mean +0.12 ± 0.05; no direct AU Mic high-res Fe/H measurement is canonical (M-dwarf [Fe/H] difficult). Method = spectroscopic_calibration (group-mean calibration) |
| rotation | Plavchan 2020 (2020Natur.582..497P) | photometric_variability | P_rot = 4.863 d from TESS Sectors 1 photometric modulation (multi-spot); definitive |
| activity | Houdebine 2010 (2010MNRAS.407.1657H) Hα | h_alpha | M1Ve flare star in saturated regime; log R'HK doesn't translate cleanly. Hα EW ~ −2 to −3 Å is the canonical young-M-dwarf saturated regime metric. Stelzer 2013 X-ray (log L_X ≈ 29.7) as cross-check on X-ray |

## Cross-check papers (recommended:false)

- **Donati 2025** (2025A&A...700A.227D) — recent ESPRESSO+SPIRou; reports M=0.50, R=0.75
  consistent with earlier values
- **Mallorquin 2024** (2024A&A...689A.132M) — ESPRESSO confirmation, planet b/c masses
- **Cale 2021** (2021AJ....162..295C) — RV with GP detrending
- **Stelzer 2013** (2013MNRAS.431.2063S) — X-ray for activity cross-check
- **Binks & Jeffries 2014** (2014MNRAS.438L..11B) — LDB age for β Pic MG (independent anchor)
- **Gaia DR3** (2023A&A...674A...1G) — astrometry already in raw; Teff = 3518 K as cross-check

## Divergent rows to correct in Phase 3 markdown

Comparing current `docs/phase3/au-mic.md` Decisions table values vs Phase 2 picks:

1. **mass_msun**: currently `0.51 ± 0.028` → Wittrock 2023. Matches Phase 2. No change.
2. **radius_rsun**: currently `0.82 ± 0.02` → Donati 2023. Matches Phase 2. No change.
3. **teff_k**: currently `3518` (Gaia DR3) → Phase 2 picks Plavchan 2020 `3700 ± 100`.
   This is a divergence in numeric value. The Phase 3 file should be updated to
   reflect Plavchan 2020 as recommended (high-res spectroscopy > BP/RP GSP-Phot
   per methodology). Note that 3700 ± 100 vs 3518 K reconciles at 1.8σ; both
   values are within combined uncertainties. Many of the derived values in the
   Phase 3 file (luminosity 0.092 from Stefan-Boltzmann at 3518 K; stellar_color_temp_k
   = 3518) need either an update or a documented divergence note.
   Choice: Update `teff_k` row to 3700 ± 100 (Plavchan 2020) as recommended,
   add reconciliation note in basis. Update `luminosity_lsun` to track Plavchan
   2020 direct bolometric measurement (0.09 ± 0.02 L☉) rather than the
   Stefan-Boltzmann derivation. Update `stellar_color_temp_k` to 3700 with a
   note that the visual rendering still uses ~3500 K because the photometric
   color is anchored on observed BP-RP which integrates over molecular bands.
   (Two paths: pick 3700 as the spectroscopic anchor OR keep 3518 as the
   color-temperature anchor. The cleanest fix: separate "teff_k" from
   "stellar_color_temp_k" — Phase 2 anchors Teff at 3700, but the in-game
   blackbody for SED illumination uses the color-equivalent 3518 K. Document.)
4. **metallicity_fe_h_dex**: currently `+0.12 medium` (β Pic MG mean, Shkolnik 2017)
   → Phase 2 picks Shkolnik 2017 calibration `+0.12 ± 0.05`. Already matches.
   The Phase 3 entry was correct in attribution; just add the explicit Phase 2
   anchor to the basis.
5. **age_gyr**: currently `0.022 ± 0.003 high` (Mamajek 2014). Matches Phase 2.
6. **rotation_period_days**: currently `4.86 high` (Plavchan 2020). Matches Phase 2.
7. **activity_log_rhk**: currently `−3.9 high` with basis "Saturated M-dwarf
   activity regime; Stelzer 2013 X-ray + Hα index". This is a documented
   divergence. log R'HK = −3.9 is the saturated regime upper bound but is NOT a
   single paper-cited value for AU Mic. Phase 2 picks Hα EW from Houdebine 2010
   as the recommended activity metric (more directly measured). Need to either
   (a) keep log R'HK = −3.9 as a derived saturated-regime estimate with low
   confidence and add Hα row, OR (b) replace with Hα value as primary.
   Choice: Add explicit Hα EW row as the Phase-2-anchored value, keep
   log R'HK = −3.9 as low-confidence derivation, document.
8. **stellar_color_temp_k**: currently `3518` — see (3) above.

## Things to add (Bibliography)

- **Plavchan 2020** — already in bibliography; mark as Phase 2 primary anchor
  for Teff/L/rotation
- **Wittrock 2023** — already in bibliography; mark as Phase 2 primary anchor for mass
- **Donati 2023** — already in bibliography; mark as Phase 2 primary anchor for radius
- **Mamajek & Bell 2014** — already in bibliography; mark as Phase 2 primary anchor for age
- **Shkolnik 2017** — already in bibliography; mark as Phase 2 primary anchor for [Fe/H]
- **Houdebine 2010** — NEW, add as Phase 2 anchor for activity (Hα)
- **Stelzer 2013** — already in bibliography; mark as cross-check for X-ray activity
- **Donati 2025** — already in bibliography; mark as cross-check for mass/radius
- **Mallorquin 2024** — already in bibliography; mark as cross-check
- **Cale 2021** — currently not in bibliography; add as cross-check for mass

## Open items

- AU Mic [Fe/H] is a known weakness. No direct high-res spectroscopic Fe/H exists
  in the literature; all values come from MG-membership inference or IR-band
  M-dwarf calibration. The +0.12 ± 0.05 Shkolnik 2017 value is the best
  available but is a group-mean, not a single-star measurement. Future ESPRESSO
  / SPIRou-anchored Fe/H from Donati 2025 follow-ups may supersede.

## Constraints honored

- No fabricated values
- No edits outside the deliverable list
- Append-only to `db/stellar_props_curated.json`
- Korean mirrors in parallel; block parity required
- Bibliography expanded
