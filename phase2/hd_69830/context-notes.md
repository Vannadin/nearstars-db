<!-- HD 69830 Phase 2 + Phase 3 reconciliation decisions log -->
# HD 69830 — Curation decisions

## Anchor paper choice — Tanner et al. 2019 ApJ 873, 91

`2019ApJ...873...91T`, doi:10.3847/1538-4357/aafe73. Dedicated
HD 69830 study delivering homogeneous Teff, log g, [Fe/H], L_bol,
isochrone mass/radius, and habitable-zone geometry. Tightest
formal uncertainties among the modern dedicated HD 69830 papers
and the only paper to combine FEROS / HARPS high-res spectroscopy
with Spitzer FIR + Hipparcos parallax for a self-consistent
SED-anchored bolometric L.

- Teff = 5402 ± 11 K
- log g = 4.49 ± 0.03
- [Fe/H] = -0.04 ± 0.02
- L = 0.622 ± 0.012 L☉ (bolometric flux + Hipparcos parallax)
- mass M = 0.863 ± 0.043 M☉ (isochrone from Teff/L/[Fe/H])
- radius R = 0.905 ± 0.019 R☉ (Stefan-Boltzmann from L + Teff)
- HZ inner/outer (Kopparapu 2013 conservative): 0.72 / 1.20 AU

Note: Tanner 2019 specifically discusses HD 69830 in the context
of the warm dust belt + Lovis 2006 planets, making it the obvious
anchor for cfg-ready synthesis.

## Why not Lovis 2006 mass

Lovis 2006 quotes M = 0.86 ± 0.03 M☉ from isochrone fitting using
ground-based optical / IR colors and Hipparcos parallax with a
Yi 2001 isochrone grid. Tanner 2019 redid the same isochrone
analysis with updated atmosphere models (MARCS) + measured L_bol
and gets 0.863 ± 0.043 — central value identical, slightly larger
uncertainty due to careful error propagation. Picking Tanner 2019
for tier consistency across all stellar quantities (Lovis 2006
remains as alternate).

## Why not Brewer 2016 for Teff

Brewer et al. 2016 ApJS 225, 32 (`2016ApJS..225...32B`) gives
Teff = 5410 ± 25 K, [Fe/H] = -0.03 ± 0.04 from the SPOCS
(Spectroscopic Properties Of Cool Stars) homogeneous KECK/HIRES
pipeline. Slightly larger formal uncertainty than Tanner 2019,
and Tanner 2019 is dedicated rather than survey-pipeline. Kept
as a strong cross-check.

## Rotation period — Suarez Mascareño 2015

Suarez Mascareño et al. 2015 MNRAS 452, 2745
(`2015MNRAS.452.2745S`, doi:10.1093/mnras/stv1441) — long-term
HARPS Ca II H&K monitoring of HD 69830 detects a 35.5 ± 0.5 day
rotation period from chromospheric activity rotational modulation
(NOT photometric — HD 69830 is too quiet for photometric P_rot
from MOST / HARPS continuum precision). This is the only direct
P_rot measurement; Mamajek & Hillenbrand 2008 gyrochronology
gives ~34 d from log R'HK calibration — within 1σ. Suarez
Mascareño 2015 recommended.

## Activity — Gomes da Silva 2021 supersedes Henry 1996

Henry 1996 quoted log R'HK ≈ -5.00 from Mt Wilson single-snapshot
measurement; Gomes da Silva 2021 (`2021A&A...646A..77G`) weighted
mean of 240 HARPS spectra over 2003-2018 gives log R'HK = -4.95 ±
0.04, slightly more active than Henry 1996 but still firmly in
the inactive locus. Boro Saikia 2018 (`2018A&A...616A.108B`)
multi-survey median gives -4.99, consistent with both. Phase 3
text quoted -5.0 colloquially; reconcile to -4.95 (Gomes 2021).

## Age — kept Lovis 2006 / Mamajek 2008 spread

HD 69830 age literature is wide:
- Lovis 2006 isochrone: 4-10 Gyr (broad)
- Mamajek & Hillenbrand 2008 activity-rotation: 5.7 ± 1 Gyr
- Tanner 2019 isochrone: 10.6 ± 2.0 Gyr (newer isochrones,
  refined log g → older HR-diagram crossing)
- Beichman 2005 used 4-10 Gyr in disk evolution context

The literature is split between ~5-6 Gyr (activity-driven) and
~10 Gyr (isochrone). Picking Mamajek 2008 5.7 Gyr as
recommended since (a) activity-rotation is the more reliable
diagnostic at this metallicity and Teff (Tanner 2019 isochrone
hits the subgiant turnoff degeneracy where the upper-MS
isochrone tracks pile up), (b) the Phase 3 docs already use this
value. Confidence: medium. Phase 3 reconciliation flags the
divergence in age row.

## Phase 3 reconciliation summary

Stellar rows in the Decisions table to be reconciled from the
old "unverified" basis to Phase 2 anchors:

| Row | Old | New | Method |
|-----|-----|-----|--------|
| mass_msun | 0.86 ± 0.03 (Lovis 2006) | 0.863 ± 0.043 (Tanner 2019) | isochrone, recommended Tanner 2019 |
| radius_rsun | 0.887 ± 0.019 (Rosenthal 2021) | 0.905 ± 0.019 (Tanner 2019) | Stefan-Boltzmann from L + Teff |
| teff_k | 5385 ± 20 (Beichman 2005) | 5402 ± 11 (Tanner 2019) | high-res spectroscopy |
| luminosity_lsun | 0.60 ± 0.03 (derived) | 0.622 ± 0.012 (Tanner 2019) | bolometric flux |
| metallicity_fe_h_dex | -0.05 ± 0.02 (Beichman 2005) | -0.04 ± 0.02 (Tanner 2019) | high-res spectroscopy |
| age_gyr | 5.7 ± 1.0 (Mamajek 2008) | 5.7 ± 1.0 (Mamajek 2008) — unchanged, Phase 3 flags Tanner 2019 10.6 Gyr divergence in basis |
| rotation_period_days | 34 ± 3 (Mamajek 2008) | 35.5 ± 0.5 (Suarez Mascareño 2015) | photometric_variability (Ca II H&K) |
| activity_log_rhk | -5.0 (Henry 1996) | -4.95 ± 0.04 (Gomes da Silva 2021) | log_rhk weighted mean |
| stellar_color_temp_k | 5385 (derived) | 5402 (derived from Tanner 2019 Teff) | derived |

All changes within 1-2σ of old values; reconciliation is about
attribution consistency + tighter formal uncertainties, not about
revising the cfg picks materially.

## Planet pages — minimal stellar-cross-ref updates

The planet pages reference host parameters (L = 0.60, P_rot = 34 d,
age = 5.7 Gyr, Teff = 5385 K). Update to:
- L = 0.622 (Tanner 2019)
- Teff = 5402 K (Tanner 2019)
- age = 5.7 ± 1 (unchanged)
- P_rot = 35.5 d (Suarez Mascareño 2015)
- R★ = 0.905 R☉ → recompute angular diameters

Derived insolations / equilibrium temperatures stay within 5% so
no material cfg-value change required; only the citation strings
need updating.
