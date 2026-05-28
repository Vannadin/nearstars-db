# 61 Vir Phase 2 + Phase 3 reconciliation — context notes

Append-only log. 2026-05-28.

## Phase 2 anchor selection

Sources discovered via NASA Exoplanet Archive `stellarhosts` TAP query
(2026-05-28). Verified bibcodes/DOIs via Wikipedia article on 61 Virginis
which carries the modern parameter set (Rathsam 2023 + Yu 2024).

### Tier hierarchy applied (per methodology.md)

Mass:
1. binary_orbit > asteroseismology > evolutionary_model >
   spectroscopic. 61 Vir has none of the first two. So
   evolutionary_model wins.
2. Pick Rathsam 2023 (Mvalu = 0.93 +/- 0.01) over Vogt 2010 (0.942
   +/- 0.034) — smaller uncertainty + newer paper using Yale-Potsdam
   stellar isochrones with Gaia DR3 parallax + high-res spectroscopy
   Teff/[Fe/H].

Radius:
1. interferometry > eclipsing_binary > sed_fitting >
   evolutionary_model.
2. von Braun 2014 CHARA: theta_LD measurement -> R = 0.9867 +/-
   0.0048 R_sun. Real interferometric measurement, supersedes Vogt
   2010 evolutionary R = 0.963 +/- 0.011.
3. CRITICAL: existing 61-vir.md cites Vogt 2010 R as "interferometric
   angular diameter combined with parallax" — same misattribution
   pattern as Delta Pav's Bruntt 2010 claim. Vogt 2010 derives R from
   isochrone (cites Takeda 2007). The actual CHARA measurement is
   von Braun 2014.

Teff:
1. interferometry > high_res_spec > sed_fitting > photometric.
2. Rathsam 2023 (5568 +/- 4 K) is high-res differential spectroscopy
   relative to the Sun (solar analog Li-depletion study). Smallest
   formal uncertainty.
3. von Braun 2014 (5538 +/- 13 K) is sed_fitting using interferometric
   theta_LD + bolometric flux — technically more direct but ~30 K
   cooler. Within 2 sigma.
4. Phase 3 was using Gaia DR3 photometric 5552 K, which is fine but
   not paper-citable; replace with Rathsam 2023.

Luminosity: von Braun 2014 0.8222 +/- 0.0033 (bolometric_flux from
SED + Hipparcos parallax). Vogt 2010 says 0.82 (consistent).

Age: tier is asteroseismology > isochrone > activity > gyrochronology
> kinematic. 61 Vir lacks asteroseismic detection.
1. Rathsam 2023 (7.70 +0.28/-0.26 Gyr) — isochrone, smallest unc
2. Vogt 2010 / Takeda 2007 (8.96 +2.76/-3.08) — isochrone, older
3. von Braun 2014 (8.6) — isochrone with interferometric R
4. Mamajek 2008 (6.1 +/- 1.7) — activity_age, the chromospheric pick
5. Sanz-Forcada 2010 (7.96) — X-ray inferred

Recommended: Rathsam 2023 7.70 Gyr (newest, isochrone, tight unc).
Confidence MEDIUM because the activity-age (Mamajek 6.1) diverges by
~1 sigma; documented divergence. Phase 3 docs were citing 6.1 which
is now demoted.

[Fe/H]: tier is high_res > low_res > photometric.
1. Rathsam 2023 (+0.006 +/- 0.004) — solar-analog differential, the
   smallest formal uncertainty
2. Vogt 2010 (-0.01) — high-res spec
3. Sousa 2008 (-0.02 +/- 0.01) — high-res spec
4. Maldonado 2015 (-0.02 +/- 0.01) — high-res spec
5. Rosenthal 2021 (+0.0275 +/- 0.06) — high-res
Recommended: Rathsam 2023.

Rotation: tier is photometric_variability > v_sin_i >
asteroseismology.
1. Yu 2024 (32.1 +/- 0.2 d) — GP modeling of 18-year HARPS
   spectroscopic activity time series. This IS a photometric_variability
   equivalent (chromospheric activity tracer over rotation period),
   directly detected.
2. Wright 2004 (~29 d from S_HK) — earlier inference, less direct
3. Vogt 2010 §4 (~28-30 d from RV jitter) — informal

Recommended: Yu 2024.

Note: 32.1 d direct supersedes Wright's 29 d, which was an inferred
rotation period from chromospheric S-index variation. This is a real
~10% upward revision worth noting.

Activity: log R'HK.
1. Isaacson & Fischer 2010 (-5.0) — California HK catalog, long-term
   monitoring; recommended.
2. Henry et al. 1996 (-5.0 also) — Mt. Wilson cross-check
3. Gomes da Silva 2021 — likely included but not verified; skipped
   for this commit (would refine to ~-5.0 +/- 0.01 if confirmed).

## Phase 3 reconciliation rows

In `docs/phase3/61-vir.md` Decisions table:

| Field | Current | New (Phase 2-cited) | Status |
|---|---|---|---|
| `mass_msun` | 0.942 ± 0.034 (Vogt 2010) | 0.93 ± 0.01 (Rathsam 2023) | within 1 sigma; updated |
| `radius_rsun` | 0.963 ± 0.011 (Vogt 2010, mislabeled interferometric) | 0.9867 ± 0.0048 (von Braun 2014, real CHARA) | **divergent — attribution corrected** |
| `teff_k` | 5552 (Gaia DR3 photometric) | 5568 ± 4 (Rathsam 2023 high-res) | updated, both within err |
| `luminosity_lsun` | 0.82 (Vogt 2010) | 0.8222 ± 0.0033 (von Braun 2014 bolometric) | same value, tighter |
| `metallicity_fe_h_dex` | +0.00 ± 0.05 | +0.006 ± 0.004 (Rathsam 2023) | same value, tighter |
| `age_gyr` | 6.1 ± 1.7 (Mamajek 2008 activity_age) | 7.70 +0.28/-0.26 (Rathsam 2023 isochrone) | **divergent — methodology change** |
| `rotation_period_days` | 29 (Wright 2004 inferred) | 32.1 ± 0.2 (Yu 2024 direct) | **updated — direct measurement** |
| `activity_log_rhk` | -5.0 (Isaacson 2010) | unchanged | |

## Open items

- Gomes da Silva 2021 may have 61 Vir log R'HK refit; not confirmed
  for this commit. Would add as cross-check if verified.
- Boyajian 2013 CHARA stellar diameters IV: 61 Vir may or may not be
  in this earlier CHARA campaign; could not verify from public abstract.
  von Braun 2014 is the confirmed CHARA reference.
- Planet pages may need light edits to update insolation derivations
  using the new L = 0.8222 L_sun (rounding within Phase 3 precision
  floor — no material change).
