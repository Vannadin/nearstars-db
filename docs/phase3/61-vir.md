<!-- 61 Virginis Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 61 Virginis — Phase 3 Synthesis

61 Virginis (HD 115617, HIP 64924, GJ 506) is a naked-eye G6.5V solar
twin at 8.534 ± 0.001 pc (Gaia DR3 parallax 117.17 ± 0.15 mas, or
27.83 light-years) in the constellation Virgo. Spectral type G6.5V
(Gray et al. 2006 NStars) is consistent with the older G7V Gray 2003
classification; effective temperature Teff = 5568 ± 4 K (Rathsam et
al. 2023 solar-analog differential high-resolution spectroscopy)
places it ~200 K cooler than the Sun. The radius is directly measured
by CHARA long-baseline optical interferometry, R = 0.9867 ± 0.0048 R☉
(von Braun et al. 2014), with mass 0.93 ± 0.01 M☉ (Rathsam 2023
Yale-Potsdam isochrone). The bolometric luminosity L = 0.8222 ± 0.0033
L☉ (von Braun 2014 bolometric flux + Hipparcos parallax) is the
canonical direct value. Metallicity sits essentially at solar
([Fe/H] = +0.006 ± 0.004, Rathsam 2023; consistent with Sousa 2008,
Maldonado 2015, Vogt 2010, all within ±0.02 dex), and the modern
isochrone age is 5.50 +0.78/-0.74 Gyr (Rathsam 2023 Table A1 for
HD 115617 / HIP 64924), which overlaps the Mamajek & Hillenbrand 2008
activity-age + isochrone value of 6.1 ± 1.7 Gyr at 1σ; the older
isochrone fits (Vogt 2010 8.96 +2.76/-3.08 Gyr, von Braun 2014 8.6
Gyr, Sanz-Forcada 2010 X-ray 7.96 Gyr — all ~8–9 Gyr) sit at the
upper end of the combined uncertainty. The star is quiet: photospheric rotation P_rot = 32.1 ± 0.2
d (Yu et al. 2024 Gaussian-process modeling of 18-yr HARPS RV+activity
time series, superseding the earlier Wright 2004 inference of ~29 d
from S-index variation), log R'HK ≈ −5.0 (Isaacson & Fischer 2010;
Henry 1996), and a low X-ray luminosity log L_X ≈ 26.7–27.0 cgs
(Schmitt & Liefke 2004 NEXXUS-2).

61 Vir hosts three RV-detected planets (Vogt 2010 — a HIRES + AAT
joint solution): b a super-Earth at 4.215 d / 5.1 M⊕ Msini, c a warm
sub-Neptune at 38.021 d / 18.2 M⊕, and d a sub-Neptune at 123.01 d /
22.9 M⊕. Outside the planet zone, **Herschel/PACS imaging by Wyatt et
al. 2012 resolves a cold debris belt centred near ≈ 30 AU** with
outer extent to ≈ 96 AU and dust temperature ~50 K, a textbook KBO
analogue with a dust mass 6–8× the Sun's Edgeworth–Kuiper belt
inventory.

**Scenario choice for NearStars: a quiet, slightly cool G6.5V solar
twin with a single resolved cold debris ring at ~30 AU and three
inner planets shown as foreground points of light.** Stellar-Physical
decisions are canonical-aligned with the new Phase 2 anchors; the
radius row carries a corrected attribution (the canonical CHARA
interferometric value from von Braun 2014, not the Vogt 2010
evolutionary radius which earlier drafts mislabeled as
interferometric), and the age row is now isochrone-led (Rathsam 2023)
with the Mamajek & Hillenbrand 2008 activity-age + isochrone combo as
a cross-check — the two converge near 5–6 Gyr, while the older Vogt
2010 / von Braun 2014 / Sanz-Forcada 2010 isochrones at ~8–9 Gyr sit
within the combined uncertainty and motivate holding Confidence=medium
pending asteroseismic arbitration. The
three tie-breaks are visual tint, debris-ring scattering tint, and
debris-ring opacity where Herschel's far-IR detection doesn't
constrain the optical appearance.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G6.5V | high | Gray et al. 2006 NStars; consistent with the older G7V Gray 2003 classification at finer subtype resolution |
| `mass_msun` | 0.93 ± 0.01 | high | Rathsam et al. 2023 Yale-Potsdam isochrone fit to solar-analog Li-depletion sample (smallest formal uncertainty); supersedes Vogt 2010 (0.942 ± 0.034) and Rosenthal 2021 (0.914 ± 0.037), all within 1σ |
| `radius_rsun` | 0.9867 ± 0.0048 | high | von Braun et al. 2014 CHARA long-baseline optical interferometry — direct angular diameter combined with Hipparcos parallax. Supersedes the Vogt 2010 evolutionary-model radius (0.963 ± 0.011, ~2.4% smaller) that earlier Phase 3 drafts incorrectly labeled "interferometric"; Vogt 2010 actually derived R from Takeda 2007 isochrone analysis |
| `teff_k` | 5568 ± 4 | high | Rathsam et al. 2023 high-resolution solar-analog differential spectroscopy; von Braun 2014 sed_fitting from interferometric θ_LD gives 5538 ± 13 K and Vogt 2010 spectroscopic 5577 ± 33 K bracket within combined uncertainty; replaces Gaia DR3 photometric 5552 K used in the earlier draft |
| `luminosity_lsun` | 0.8222 ± 0.0033 | high | von Braun et al. 2014 bolometric flux integration + Hipparcos parallax; Vogt 2010's 0.82 (from L = R²·(T/T☉)⁴) agrees within rounding |
| `metallicity_fe_h_dex` | +0.006 ± 0.004 | high | Rathsam et al. 2023 high-res differential spectroscopy (smallest formal uncertainty); Vogt 2010 (-0.01), Sousa 2008 (-0.02 ± 0.01), Maldonado 2015 (-0.02 ± 0.01), Rosenthal 2021 (+0.0275 ± 0.06) all agree within combined errors at near-solar |
| `age_gyr` | 5.50 +0.78/-0.74 | medium | Rathsam et al. 2023 Yale-Yonsei isochrone, Table A1 row for HD 115617 / HIP 64924 (newest paper, tightest formal uncertainty). Mamajek & Hillenbrand 2008 chromospheric activity-age + isochrone gives 6.1 ± 1.7 Gyr — overlaps Rathsam at 1σ, so the older "isochrone-vs-activity" framing no longer applies. **Residual older-isochrone tension:** Vogt 2010 (8.96 +2.76/-3.08), von Braun 2014 (8.6), and Sanz-Forcada 2010 X-ray (7.96 Gyr) all sit at ~8–9 Gyr — within combined uncertainty of Rathsam but at the upper end of the literature spread. Phase 3 holds Confidence=medium pending asteroseismic arbitration |
| `rotation_period_days` | 32.1 ± 0.2 | high | Yu et al. 2024 multidimensional-GP modeling of 18-year HARPS RV + activity-indicator time series; the first direct rotation-period detection. Supersedes the earlier Wright 2004 inference (~29 d from S_HK fluctuation; Vogt 2010 §4 RV-jitter modeling also reported 28–30 d power) — the ~10% upward revision reflects the better cycle-baseline of the HARPS data |
| `activity_log_rhk` | −5.0 | high | Isaacson & Fischer 2010 California HK catalog (long-term monitoring stable at quiet G-dwarf locus); Henry et al. 1996 Mt Wilson cross-check agrees |
| `x_ray_log_lx_cgs_min` | 26.7 | medium | Schmitt & Liefke 2004 — NEXXUS-2 ROSAT survey lower bound |
| `x_ray_log_lx_cgs_max` | 27.0 | medium | Schmitt & Liefke 2004 — NEXXUS-2 ROSAT survey upper bound; no resolved cycle yet |
| `visual_surface_tint_hex_primary` | `#fff2dc` (warm cream, slightly more amber than Sun) | medium | Tie-break: G6.5V blackbody at 5568 K + interesting-first cue that this is a cooler G-dwarf than the player's Sol reference |
| `stellar_color_temp_k` | 5568 | high | derived from Teff (Rathsam 2023) |
| `disk_present` | true | high | Wyatt et al. 2012 — Herschel/PACS resolved cold ring; SED-confirmed by Tanner 2014, Su 2017 |
| `disk_inner_radius_au` | 30 | high | Wyatt 2012 — Herschel/PACS resolved geometry; modified-blackbody SED fit places the temperature-weighted radius near 30 AU |
| `disk_outer_radius_au` | 96 | medium | Wyatt 2012 — resolved outer cutoff at 70/100/160 μm; outer edge slightly less constrained than the inner |
| `disk_dust_temperature_k` | 50 | high | Wyatt 2012 — modified-blackbody SED fit (range 30–60 K) |
| `disk_tint_rgb_hex` | `#9ca4b5` (cool steel-blue scattering tint) | low | Tie-break: 50 K thermal emission peaks in far-IR (invisible to the eye); cfg picks a cool-grey scattering tint so the ring is recognizable in the orbit-view renderer |
| `disk_opacity` | 0.10 | low | Tie-break: Herschel τ ~ 10⁻⁵ (optical depth in far-IR) is far below player visibility; cfg picks a renderer-visible value while keeping the ring obviously faint |
| `disk_morphology` | single cold belt, KBO analog | high | Wyatt 2012 — single broad ring; no warps, gaps, or two-belt structure reported |
| `disk_resolved_imaging` | true | high | Wyatt 2012 — Herschel/PACS resolved at 70/100/160 μm |
| `disk_imaging_observatory` | Herschel/PACS (Wyatt 2012) | high | direct citation |
| `disk_mass_mearth` | 0.07 | medium | Wyatt 2012 — dust mass quoted as ~6–8× Sun's KBO inventory; midpoint adopted, scaled to M⊕ via the standard 5×10⁻³ M⊕ Edgeworth–Kuiper dust reference |
| `disk_planetesimal_belt_inferred` | true | high | Wyatt 2012 §5 — dust lifetime against PR drag + collisional grinding requires a parent body belt to replenish the observed dust |

## Surface synthesis

61 Vir's photosphere sits ~200 K cooler than Sol — Teff 5568 K
(Rathsam 2023) versus the 5772 K solar reference — but at otherwise
solar-twin parameters: mass 0.93 M☉ (Rathsam 2023), radius 0.987 R☉
(von Braun 2014 CHARA), [Fe/H] within 0.01 dex of solar (Rathsam
2023). The luminosity 0.822 L☉ is the natural consequence of the
slightly lower temperature given an essentially solar radius. In the
visible band the spectrum carries the canonical G-dwarf Ca II H&K,
Mg b, Na D, and Hα signature with line depths intermediate between a
Sun-like G2V and a slightly redder K0V; high-resolution differential
spectroscopy by Rathsam et al. 2023 (anchored on solar-analog
lithium depletion) confirms the solar-twin abundance pattern, with no
anomalous lithium depletion or rapid-rotator veiling.

Granulation patterns from 3D radiative-hydrodynamic simulations
(STAGGER/CO5BOLD family, as applied to similar G6/G7V targets in the
Magic 2013 grid) predict cell sizes ~10% larger than solar and
contrast slightly higher than Sol, scaling with the slower convective
turnover at the cooler Teff. Sunspot coverage tracks the chromospheric
log R'HK = −5.0 (Isaacson & Fischer 2010), placing 61 Vir in the
quiet-dwarf locus alongside τ Ceti and α Cen B — peak coverage during
any inferred activity cycle would be ≲ 0.3% of the visible disk,
slightly less than Sol's solar-maximum.

Limb darkening at H band is not directly measured for 61 Vir (no
PIONIER campaign comparable to α Cen A's Kervella 2017), but the
1D-atmosphere prediction places α_H ≈ 0.20 — slightly stronger than
α Cen A's measured 0.14 in line with the cooler Teff. NearStars
adopts the 1D prediction with Confidence=medium pending direct
interferometric follow-up.

The slight amber shift in the visual tint is a tie-break: the
blackbody peak at 5568 K is shifted ~7% redward of solar in λ_max
terms, contributing to the slightly creamier visual cue selected over
a pure solar match.

## Atmosphere synthesis

61 Vir hosts a quiet G-dwarf chromosphere–transition-region–corona
structure characteristic of an old, magnetically inactive solar twin.
The chromospheric S-index (Wilson 1968 Mt Wilson convention)
translates to log R'HK ≈ −5.0 (Isaacson & Fischer 2010), about
0.05 dex quieter than the modern Sun at solar minimum and a full
0.20 dex below typical young G-dwarfs. The transition-region UV
emission and the X-ray luminosity log L_X = 26.7–27.0 cgs (0.1–2 keV,
Schmitt & Liefke 2004 NEXXUS-2 catalog) place 61 Vir squarely in the
inactive G-dwarf locus.

No long-term activity cycle has been resolved for 61 Vir comparable
to α Cen A's 19-yr Robrade 2016 detection — the chromospheric
monitoring record is shorter and the underlying cycle amplitude is
expected to be small. Flares above the photometric noise floor are
not reported; 61 Vir provides a benign space-weather environment for
any inner planet (and the three Vogt 2010 planets all sit inside
a < 0.5 AU envelope).

The integrated XUV luminosity is below 10⁻⁴ L_bol, similar to or
quieter than solar, and would be unable to materially erode an
Earth-mass primary atmosphere on Gyr timescales for any planet at or
beyond ~0.3 AU. The inner planet b (0.050 AU, separate Phase 3
workspace) sits in the photoevaporation-influenced regime, but the
stellar XUV contribution is no more aggressive than Sol's at the
equivalent insolation.

## Rotation & spin synthesis

The 32.1 ± 0.2 day rotation period (Yu et al. 2024 from a
multidimensional Gaussian-process fit to 18 years of HARPS RV and
activity-indicator time series) is the first direct detection,
superseding the older Wright 2004 estimate (~29 d from chromospheric
S_HK fluctuations) and the Vogt 2010 §4 RV-jitter inference (28–30 d
power in the residuals). At ~8 Gyr (Rathsam 2023 isochrone) and via
the Skumanich braking law P_rot ∝ √t scaled from a solar-type ZAMS
spin, the expected rotation period is 30–35 d, which 61 Vir's
measured 32.1 d matches exactly — the new value is in better accord
with the modern isochrone age than the older 29 d figure was with
the Mamajek 2008 activity age, and provides additional support for
the isochrone-led age picture.

Asteroseismic detections are not yet available for 61 Vir — the
star's Vmag = 4.71 makes it observable but no dedicated p-mode
campaign equivalent to Bedding 2004 for α Cen A has been carried out;
HARPS RV time series would in principle support a detection.
Differential rotation is not directly resolved; following the
Skumanich locus solar analog, the equator is expected to rotate ~20%
faster than the poles.

The rotation axis inclination is unconstrained — for visual rendering
NearStars adopts an axis tilted 30° to the ecliptic of the inner
planetary system, consistent with a randomly oriented spin axis. The
Vogt 2010 inclination posterior for b/c/d is consistent with a
co-planar near-edge-on system but cannot be tied directly to the
stellar spin.

## Visual styling

In the NearStars renderer, 61 Vir is portrayed as a warm-cream G6.5V
star — visually close to Sol but tinted slightly amber to encode the
~200 K cooler photosphere. The visual hex `#fff2dc` is a tie-break
choice against a pure solar match: it gives the player an immediate
cue that this is a cooler G-dwarf than their Sol reference, which
helps distinguish 61 Vir from other near-solar Phase 3 targets (α Cen
A's `#fff4e8` cream, 47 UMa, etc.).

- **Orbit view (system entry)**: solar-yellow point source surrounded
  by a faint, near-circular debris ring centred at ~30 AU radius,
  extending out to ~96 AU. The ring is rendered as a thin grey-blue
  scattering band with opacity 0.10 — visible but obviously faint,
  not a Saturn-class ring.
- **Close-in view (within the planet zone, < 1 AU)**: the debris ring
  recedes into the background; the three inner planets (b at 0.05 AU,
  c at 0.22 AU, d at 0.48 AU) appear as foreground points of light
  during planet phase, with b's super-Earth disk and c/d's
  sub-Neptune disks resolved only at very close range.
- **Surface view (from a planet)**: a recognizable solar-type disk
  with mild limb darkening, granulation pattern, and faint sunspots
  during any active phase. The 0.96 R☉ star at 0.48 AU (planet d)
  would span ~0.53° angular diameter, almost exactly the Sun's
  apparent size from Earth — a near-perfect Sol analog for the
  outer-planet observer.
- **Star in sky from Earth**: at Vmag 4.71 the star is naked-eye but
  unremarkable, embedded in the constellation Virgo near the
  ecliptic; in NearStars' real-stars-only mode the star appears at
  its Gaia DR3 J2016.0 sky position propagated linearly to the game
  epoch.
- **Debris ring viewed from a hypothetical outer planet**: at, say,
  10 AU the ring would form a thin diffuse band along the ecliptic,
  brightest in scattered light when illuminated from the back side
  — analogous to how the Sun's Edgeworth–Kuiper belt would appear
  to an observer at Neptune's orbit but 6–8× brighter due to the
  higher dust mass.
- **Quiet-star animation**: spot rendering is muted — peak coverage
  ≲ 0.3% of the disk, much less dramatic than Sol's solar-maximum
  spotting. No prominent flare or CME visual effects.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Rathsam A., Meléndez J. & Carvalho Silva G. 2023** — *Lithium
  depletion in solar analogs: age and mass effects*, MNRAS 525, 4642
  (`2023MNRAS.525.4642R`, doi:10.1093/mnras/stad2589, arXiv:2309.00471).
  Solar-analog differential high-resolution spectroscopy; supplies the
  Phase 2 anchors for Teff (5568 ± 4 K), mass (0.93 ± 0.01 M☉),
  [Fe/H] (+0.006 ± 0.004), age (5.50 +0.78/-0.74 Gyr), and log g
  (4.390 ± 0.012). **Primary Phase 2 anchor for 61 Vir** (newest paper,
  smallest uncertainties); replaces Pavlenko 2012 in the earlier
  draft.
- **von Braun K. et al. 2014** — *Stellar diameters and temperatures
  V — 11 newly characterized exoplanet host stars*, MNRAS 438, 2413
  (`2014MNRAS.438.2413V`, doi:10.1093/mnras/stt2360, arXiv:1312.1792).
  CHARA long-baseline optical interferometry — direct angular diameter
  for 61 Vir combined with Hipparcos parallax. Supplies the **only
  direct radius** (R = 0.9867 ± 0.0048 R☉) and the canonical bolometric
  luminosity (L = 0.8222 ± 0.0033 L☉). Earlier Phase 3 drafts
  incorrectly attributed Vogt 2010 as the interferometric source — that
  attribution was wrong (Vogt 2010 used Takeda 2007 isochrone) and is
  corrected here.
- **Yu H. et al. 2024** — *Modelling stellar variability in archival
  HARPS data: I — Rotation and activity properties with
  multidimensional Gaussian processes*, MNRAS 528, 5511
  (`2024MNRAS.528.5511Y`, doi:10.1093/mnras/stae137, arXiv:2401.05528).
  First direct rotation-period detection for 61 Vir: P_rot = 32.1 ± 0.2
  d from a multidimensional-GP fit to 18 years of HARPS RV + activity
  time series. Supersedes the Wright 2004 / Vogt 2010 §4 inferences
  of ~29 d.
- **Vogt S. S. et al. 2010** — *A Super-Earth and Two Neptunes
  Orbiting the Nearby Sun-Like Star 61 Virginis*, ApJ 708, 1366
  (`2010ApJ...708.1366V`, doi:10.1088/0004-637X/708/2/1366). The
  foundational paper for the three planet detections (b 4.215 d,
  c 38.021 d, d 123.01 d) — HIRES + AAT joint RV solution. Adopts
  Takeda 2007 stellar parameters (M = 0.942 ± 0.034 M☉, R = 0.963 ±
  0.011 R☉, age 8.96 +2.76/-3.08 Gyr from isochrone). Now demoted to
  cross-check for stellar parameters; remains the primary planet
  detection paper.
- **Wyatt M. C. et al. 2012** — *Herschel imaging of 61 Vir: implications
  for the prevalence of debris in low-mass planetary systems*, MNRAS
  424, 1206 (`2012MNRAS.424.1206W`, doi:10.1111/j.1365-2966.2012.21298.x,
  arXiv:1206.2370 — earlier draft cited 1204.6063 in error).
  Herschel/PACS resolved imaging of the cold debris
  belt at 70/100/160 μm; single broad ring centred near ~30 AU extending
  to ~96 AU, dust temperature ~50 K, dust mass 6–8× Sun's KBO
  inventory. Anchors every Circumstellar-disk Decisions row.
- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age Estimation
  for Solar-Type Dwarfs Using Activity-Rotation Diagnostics*, ApJ 687,
  1264 (`2008ApJ...687.1264M`, arXiv:0807.1686). Chromospheric
  activity-age + isochrone combo giving 6.1 ± 1.7 Gyr — overlaps the
  Rathsam 2023 Yale-Yonsei isochrone value (5.50 +0.78/-0.74 Gyr) at
  1σ, so no methodology divergence remains. The older Vogt 2010 /
  von Braun 2014 isochrone fits (~8–9 Gyr) sit at the upper end of
  combined uncertainty; Phase 3 picks Rathsam and holds
  Confidence=medium pending asteroseismic arbitration.
- **Wright J. T. et al. 2004** — *Chromospheric Ca II Emission in
  Nearby F, G, K, and M Stars*, ApJS 152, 261 (`2004ApJS..152..261W`,
  doi:10.1086/386283). Catalog of Mt-Wilson S-indices and inferred
  rotation periods; 61 Vir P_rot ≈ 29 d from S_HK fluctuations — now
  superseded by Yu 2024's direct 32.1 ± 0.2 d. Cross-check.

### Read (context / methodology, not directly decision-driving)

- **Isaacson H. & Fischer D. 2010** — *Chromospheric Activity and Jitter
  Measurements for 2630 Stars on the California Planet Search*, ApJ
  725, 875 (`2010ApJ...725..875I`, arXiv:1009.2301). The California
  HK catalog refit; 61 Vir log R'HK ≈ −5.0 confirmed stable across
  multiple seasons.
- **Schmitt J. H. M. M. & Liefke C. 2004** — *NEXXUS: A Comprehensive
  ROSAT survey of coronal X-ray emission among nearby solar-like
  stars*, A&A 417, 651 (`2004A&A...417..651S`). NEXXUS-2 catalog;
  61 Vir log L_X ≈ 26.7–27.0 cgs, quiet G-dwarf locus.
- **Tanner A. et al. 2014** — context paper for the 61 Vir disk SED +
  imaging follow-up; reinforces the Wyatt 2012 cold-belt geometry.
- **Su K. Y. L. et al. 2017** — *Hot extended Solar System dust and
  cold debris disks in the Spitzer + Herschel surveys*, AJ 153, 226
  (`2017AJ....153..226S`). 61 Vir in the cold-disk sample; consistent
  with Wyatt 2012.
- **Sousa S. G. et al. 2008** — *Spectroscopic parameters for 451
  stars in the HARPS GTO planet search program*, A&A 487, 373
  (`2008A&A...487..373S`, doi:10.1051/0004-6361:200809698). High-res
  spectroscopic parameters for 61 Vir (Teff = 5558 ± 19 K, [Fe/H] =
  -0.02 ± 0.01, log g = 4.36). Cross-check for Teff and [Fe/H].
- **Maldonado J. et al. 2015** — *Stellar parameters of cool dwarfs
  and subgiants*, A&A 579, A20 (`2015A&A...579A..20M`,
  doi:10.1051/0004-6361/201525764). Independent high-res spectroscopic
  refit; Teff = 5579 ± 10 K, [Fe/H] = -0.02 ± 0.01 — agrees with the
  near-solar consensus.
- **Rosenthal L. J. et al. 2021** — *The California Legacy Survey I.*
  ApJS 255, 8 (`2021ApJS..255....8R`, doi:10.3847/1538-4365/abe23c).
  California Planet Search 30-year RV refit including 61 Vir; reports
  Teff = 5585.57 ± 78.88 K, M = 0.914 ± 0.037, R = 1.033 ± 0.023,
  [Fe/H] = +0.0275 ± 0.06. Cross-check; consistent at the 1σ level
  with the Rathsam 2023 / von Braun 2014 picks.
- **Sanz-Forcada J. et al. 2010** — *X-ray ages for nearby stars*,
  A&A 511, L8 (`2010A&A...511L...8S`,
  doi:10.1051/0004-6361/200913670). 61 Vir X-ray-inferred age 7.96
  Gyr, sitting at the older-isochrone end alongside Vogt 2010 / von
  Braun 2014. In tension with the Rathsam 2023 + Mamajek 2008
  convergence at 5–6 Gyr — motivates the medium Confidence on the
  age row.

### Read (instrument-only, not visual-informative)

- **Gray R. O. et al. 2006** — *Contributions to the Nearby Stars
  (NStars) Project: Spectroscopy of Stars Earlier than M0 Within 40 pc
  — The Southern Sample*, AJ 132, 161 (`2006AJ....132..161G`,
  doi:10.1086/504637). G6.5V spectral classification for 61 Vir. Note:
  earlier Phase 3 drafts attributed the G6.5V to "Gaia DR3 label" —
  Gray 2006 NStars is the actual primary classification source.
- **Pavlenko Y. V. et al. 2012** — *Effective temperatures, gravities,
  metallicities, and ages of 18 solar twin candidates*
  (`2012MNRAS.422..542P`, arXiv:1112.0590). High-resolution
  spectroscopy of solar-twin candidates including 61 Vir; consistent
  with near-solar [Fe/H] within 0.05 dex. Demoted to cross-check
  (smaller sample, larger formal uncertainty than Rathsam 2023).
- **Bensby T. et al. 2014** — *Exploring the Milky Way stellar disk: a
  detailed elemental abundance study of 714 F and G dwarfs*, A&A 562,
  A71 (`2014A&A...562A..71B`, arXiv:1309.2631). 61 Vir in the
  thin-disk metallicity sample; [Fe/H] consistent with solar.
- **Brewer J. M. et al. 2016** — *Spectral Properties of Cool Stars
  (SPOCS): extended catalog of 1626 stars*, ApJS 225, 32
  (`2016ApJS..225...32B`, arXiv:1606.07929). SPOCS extended catalog;
  refit of [Fe/H], Teff, log g for 61 Vir consistent with the
  near-solar values.
- **Lawler S. M. et al. 2014** — context paper for the cold-disk
  population around solar-type stars; 61 Vir cited.
- **Magic Z. et al. 2013** — STAGGER 3D RHD grid for cool dwarfs;
  cited via granulation discussion.

### Not read — no arXiv preprint or low-priority (~30 papers)

Conference abstracts (DDA, EPSC), SETI / laser-emission searches,
brown-dwarf companion radial-velocity follow-up at very large
separations, and astrobiology white papers contribute no cfg-decisive
content. The full filtered bib would be preserved in
`docs/phase3/_bib/61-vir.yaml` once the system.yaml-driven Stage 5
filter is run; for this literature-direct stellar synthesis no bib
yaml exists yet.

## Open items for follow-up

- **Phase 2 `disk_measurements` ingest**: this synthesis cites Wyatt
  2012, Tanner 2014, and Su 2017 directly. Adding a structured
  `disk_measurements` array to `db/systems/61_vir.json` (with the
  Wyatt 2012 geometry + dust mass as the recommended entry) would
  formalize the audit trail; Confidence on the disk geometry rows
  would not change (already high), but the literature-direct flag in
  Basis could be replaced with a clean DB reference.
- **Planets b/c/d Phase 3 follow-up**: a separate workspace
  (`phase3/61_vir_planets/`) will synthesize the three Vogt 2010
  planets. b is a 5.1 M⊕ super-Earth at 0.050 AU (likely hot rocky /
  steam-atmosphere category); c is a warm sub-Neptune at 0.22 AU
  (~18 M⊕); d is a cooler sub-Neptune at 0.48 AU (~23 M⊕). None
  transit (RV-only), so atmospheric characterization is in
  reflected-light regime via direct imaging proposals.
- **Asteroseismic campaign**: 61 Vir at Vmag 4.71 is HARPS/ESPRESSO
  reachable; a dedicated p-mode detection would tighten the
  asteroseismic age and arbitrate the residual older-isochrone
  tension (Vogt 2010 / von Braun 2014 / Sanz-Forcada 2010 ~8–9 Gyr vs
  Rathsam 2023 5.50 +0.78/-0.74 Gyr and Mamajek 2008 6.1 ± 1.7 Gyr,
  the latter two converging at 5–6 Gyr within combined uncertainty).
  An age tied to seismic Δν + ν_max would drop the uncertainty by a
  factor of ~3 and likely confirm the younger reading given the Yu
  2024 P_rot = 32.1 d already aligns with the
  ~8 Gyr Skumanich expectation.
- **Direct-imaging follow-up of the debris ring**: ALMA millimetre
  imaging (CO + dust continuum) would refine the ring geometry beyond
  Herschel's spatial resolution; if a sharp inner edge or asymmetry
  is detected, the `disk_morphology` field could be upgraded from
  "single cold belt, KBO analog" to a more detailed shape.
- **Long-term activity cycle**: 61 Vir's chromospheric monitoring
  record is too short to confirm or refute a solar-like cycle; a Mt
  Wilson / California HK follow-up over the next decade would
  populate the `activity_cycle_years` field.

## Related

- [alpha-centauri-a](alpha-centauri-a.md) — solar-twin comparison; 61 Vir is the cooler quieter analog at 8.53 pc vs α Cen A at 1.34 pc
- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [data-sources](../reference/data-sources.md) — paper-citation policy this synthesis inherits
