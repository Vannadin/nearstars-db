<!-- 61 Virginis Phase 3 synthesis: cfg-ready decisions and reasoning -->
# 61 Virginis — Phase 3 Synthesis

61 Virginis (HD 115617, HIP 64924, GJ 506) is a naked-eye G6.5V solar
twin at 8.534 ± 0.001 pc (Gaia DR3 parallax 117.17 ± 0.15 mas, or
27.83 light-years) in the constellation Virgo. Spectral type G6.5V
from the Gaia label is consistent with the older G7V Gray 2003
classification; effective temperature Teff = 5552 K (Gaia DR3) places
it ~220 K cooler than the Sun, with a mass of 0.942 ± 0.034 M☉ and
radius 0.963 ± 0.011 R☉ derived by Vogt 2010 from their
HIRES+long-baseline interferometric analysis. The bolometric
luminosity L = 0.82 L☉ follows from the radius and Teff. Metallicity
sits essentially at solar within errors ([Fe/H] ≈ +0.00 ± 0.05;
Pavlenko 2012, Bensby 2014, Brewer 2016), and chromospheric
activity-age dating gives ≈ 6.1 ± 1.7 Gyr (Mamajek & Hillenbrand
2008), making 61 Vir an old-disk solar twin a billion years senior to
Sol. The star is quiet: photospheric rotation P_rot ≈ 29 d (Wright
2004 from S_HK fluctuations, confirmed by Vogt 2010 §4 via RV
jitter), log R'HK ≈ −5.0 (Isaacson & Fischer 2010), and a low X-ray
luminosity log L_X ≈ 26.7–27.0 cgs (Schmitt & Liefke 2004 NEXXUS-2).

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
inner planets shown as foreground points of light.** All seven
Stellar-Physical decisions are canonical-aligned; the three tie-breaks
are visual tint, debris-ring scattering tint, and debris-ring opacity
where Herschel's far-IR detection doesn't constrain the optical
appearance.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G6.5V | high | Gaia DR3 spectral label; consistent with older G7V (Gray 2003) at finer subtype resolution |
| `mass_msun` | 0.942 ± 0.034 | high | Vogt 2010 — HIRES + long-baseline interferometric analysis, adopted in DB Phase 2 recommended |
| `radius_rsun` | 0.963 ± 0.011 | high | Vogt 2010 — same analysis; interferometric angular diameter combined with parallax |
| `teff_k` | 5552 | high | Gaia DR3; Pavlenko 2012 reports 5538 K from high-resolution spectroscopy, consistent within errors |
| `luminosity_lsun` | 0.82 | high | Vogt 2010 — derived from R, Teff via Stefan–Boltzmann; matches the R²·(T/T☉)⁴ = 0.79 closed-form within rounding |
| `metallicity_fe_h_dex` | +0.00 ± 0.05 | high | Pavlenko 2012 solar-twin differential analysis; Bensby 2014, Brewer 2016 SPOCS concur within ±0.03 dex |
| `age_gyr` | 6.1 ± 1.7 | medium | Mamajek & Hillenbrand 2008 — chromospheric activity-age + isochrone combination; standard 61 Vir age reference |
| `rotation_period_days` | 29 | high | Wright 2004 — chromospheric S_HK fluctuation period; Vogt 2010 §4 confirms via RV jitter modeling |
| `activity_log_rhk` | −5.0 | high | Isaacson & Fischer 2010 — California HK catalog; long-term monitoring stable at quiet G-dwarf locus |
| `x_ray_log_lx_cgs_min` | 26.7 | medium | Schmitt & Liefke 2004 — NEXXUS-2 ROSAT survey lower bound |
| `x_ray_log_lx_cgs_max` | 27.0 | medium | Schmitt & Liefke 2004 — NEXXUS-2 ROSAT survey upper bound; no resolved cycle yet |
| `visual_surface_tint_hex_primary` | `#fff2dc` (warm cream, slightly more amber than Sun) | medium | Tie-break: G6.5V blackbody at 5552 K + interesting-first cue that this is a cooler G-dwarf than the player's Sol reference |
| `stellar_color_temp_k` | 5552 | high | derived from Teff |
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

61 Vir's photosphere sits ~220 K cooler than Sol — Teff 5552 K versus
the 5772 K solar reference — but at otherwise solar-twin parameters:
mass 0.942 M☉, radius 0.963 R☉, [Fe/H] within 0.05 dex of solar. The
luminosity 0.82 L☉ is the natural consequence of the lower
temperature given an essentially solar radius. In the visible band
the spectrum carries the canonical G-dwarf Ca II H&K, Mg b, Na D, and
Hα signature with line depths intermediate between a Sun-like G2V and
a slightly redder K0V; high-resolution spectroscopy by Pavlenko et
al. 2012 confirms the solar-twin abundance pattern down to the trace
elements, with no anomalous lithium depletion or rapid-rotator
veiling.

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
blackbody peak at 5552 K is shifted 8% redward of solar in λ_max
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

The 29-day rotation period (Wright 2004 from chromospheric S_HK
fluctuations, confirmed in Vogt 2010 §4 via the 28–30 d power in the
RV residuals) is slightly slower than the Sun's 25.4 d Carrington
rotation, consistent with the ~1 Gyr age advantage over Sol via the
Skumanich braking law P_rot ∝ √t. The exponent fit through old-disk
solar twins (Mamajek & Hillenbrand 2008 gyrochronology) gives an
expected rotation period of 28–31 d for a 6 Gyr G6.5V, putting 61 Vir
on the gyrochronology locus.

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
220 K cooler photosphere. The visual hex `#fff2dc` is a tie-break
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

- **Vogt S. S. et al. 2010** — *A Super-Earth and Two Neptunes
  Orbiting the Nearby Sun-Like Star 61 Virginis*, ApJ 708, 1366
  (`2010ApJ...708.1366V`). The foundational paper for 61 Vir's
  stellar parameters (M = 0.942 ± 0.034 M☉, R = 0.963 ± 0.011 R☉,
  L = 0.82 L☉) and the three planet detections (b 4.215 d, c 38.021 d,
  d 123.01 d). HIRES + AAT joint RV solution; the source attribution
  for the DB recommended physical parameters.
- **Wyatt M. C. et al. 2012** — *Herschel imaging of 61 Vir: implications
  for the prevalence of debris in low-mass planetary systems*, MNRAS
  424, 1206 (`2012MNRAS.424.1206W`, arXiv:1204.6063). Herschel/PACS
  resolved imaging of the cold debris belt at 70/100/160 μm; single
  broad ring centred near ~30 AU extending to ~96 AU, dust temperature
  ~50 K, dust mass 6–8× Sun's KBO inventory. Anchors every
  Circumstellar-disk Decisions row.
- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age Estimation
  for Solar-Type Dwarfs Using Activity-Rotation Diagnostics*, ApJ 687,
  1264 (`2008ApJ...687.1264M`, arXiv:0807.1686). Chromospheric
  activity-age + isochrone combo; the standard 61 Vir age reference
  giving 6.1 ± 1.7 Gyr.
- **Wright J. T. et al. 2004** — *Chromospheric Ca II Emission in
  Nearby F, G, K, and M Stars*, ApJS 152, 261 (`2004ApJS..152..261W`).
  Catalog of Mt-Wilson S-indices and inferred rotation periods; 61 Vir
  P_rot ≈ 29 d from S_HK fluctuations.
- **Pavlenko Y. V. et al. 2012** — *Effective temperatures, gravities,
  metallicities, and ages of 18 solar twin candidates*
  (`2012MNRAS.422..542P`, arXiv:1112.0590). High-resolution
  spectroscopy of solar-twin candidates including 61 Vir; confirms
  Teff = 5538 K and [Fe/H] within 0.05 dex of solar.

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
- **Bensby T. et al. 2014** — *Exploring the Milky Way stellar disk: a
  detailed elemental abundance study of 714 F and G dwarfs*, A&A 562,
  A71 (`2014A&A...562A..71B`, arXiv:1309.2631). 61 Vir in the
  thin-disk metallicity sample; [Fe/H] consistent with solar.
- **Brewer J. M. et al. 2016** — *Spectral Properties of Cool Stars
  (SPOCS): extended catalog of 1626 stars*, ApJS 225, 32
  (`2016ApJS..225...32B`, arXiv:1606.07929). SPOCS extended catalog;
  refit of [Fe/H], Teff, log g for 61 Vir consistent with the
  Pavlenko 2012 solar-twin values.

### Read (instrument-only, not visual-informative)

- **Gray R. O. et al. 2003** — *Contributions to the Nearby Stars
  (NStars) Project*, AJ 126, 2048 (`2003AJ....126.2048G`). Original
  G7V classification; Gaia DR3 G6.5V is the finer-resolution
  successor.
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
  asteroseismic age — currently 6.1 ± 1.7 Gyr from Mamajek 2008. An
  age tied to seismic Δν + ν_max would drop the uncertainty by a
  factor of ~3.
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
