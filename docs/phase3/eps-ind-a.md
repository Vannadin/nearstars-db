<!-- eps Ind A Phase 3 synthesis: cfg-ready decisions and reasoning -->
# ε Indi A — Phase 3 Synthesis

ε Indi A (HD 209100, HIP 108870, GJ 845 A, HR 8387) is a K5 V dwarf at
3.638 pc (Gaia DR3 parallax 274.84 ± 0.10 mas) — about 11.9 light-years
away, the host of one of the nearest known stellar systems to the Sun and
the primary of a remarkable hierarchical triple. The fundamental
parameters come from the frozen Phase 2 layer: effective temperature
Teff = 4700 ± 65 K (Lundkvist et al. 2024, high-resolution UVES
spectroscopy), luminosity L = 0.239 ± 0.001 L☉ (Feng et al. 2019,
bolometric flux), radius R = 0.713 ± 0.006 R☉ (Lundkvist et al. 2024,
from the Rains et al. 2020 limb-darkened angular diameter θ_LD =
1.817 ± 0.013 mas combined with the Gaia DR3 distance), and mass
M = 0.782 ± 0.023 M☉ (Lundkvist et al. 2024). The mass is notable as an
asteroseismic determination: Lundkvist 2024 detected solar-like
oscillations at ν_max = 5265 ± 110 µHz — the highest-frequency
solar-like oscillations ever measured in any star — making ε Indi A the
coolest dwarf with measured oscillations. It is a quiet, slowly-rotating
K dwarf: the chromospheric activity index is log R'HK = −4.72 (Chen et
al. 2022, adopting Pace 2013) and the rotation period is P_rot ≈ 35 d
(Feng et al. 2018), with a chromospheric activity cycle of ≈ 2600 d
(≈ 7.1 yr) detected in the HARPS Ca II H&K archive (Lundkvist 2024).

What makes ε Indi A exceptional for NearStars is its system. ε Indi A
hosts **the closest directly-imaged cold giant exoplanet to the Sun** —
ε Indi A b, a ~7.6 M_Jup super-Jupiter on a ~20.9 AU orbit, the first
solar-age (~3.5 Gyr) giant exoplanet imaged by JWST with a temperature
near ~275 K, confirmed ammonia, and evidence for thick water-ice clouds
(Matthews et al. 2024, 2026). The same star is orbited at ~1459 AU by
**ε Indi B**, a binary brown-dwarf pair (Ba: T1–1.5, 66.9 M_Jup; Bb: T6,
53.3 M_Jup; Chen et al. 2022 dynamical masses) — among the
best-characterized brown dwarfs in the sky. The full ε Indi system thus
spans a K dwarf, a cold super-Jupiter, and two T-dwarf brown dwarfs in
one gravitationally bound hierarchy within 12 light-years.

**Scenario choice for NearStars: a warm orange-amber, quiet,
slowly-rotating K5 V dwarf — the third-nearest naked-eye K dwarf —
hosting the nearest directly-imaged cold super-Jupiter and a distant
brown-dwarf-pair companion.** The stellar layer is anchored on the
frozen Phase 2 sources (Lundkvist 2024 mass/radius/Teff, Feng 2019
luminosity, Feng 2018 rotation, Chen 2022 activity + age) with the
brown-dwarf-pair context from Chen 2022. No circumstellar disk is known —
no infrared-excess or imaging detection has been reported and none is
fabricated here. One tie-break sets the visual surface tint for the
4700 K K5 V SED; the age and rotation sit at medium confidence because
no Phase 2 age array exists and the rotation method is RV-activity-index
rather than photometric.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | K5 V | high | Lundkvist et al. 2024 (title: "the K5 V star ε Indi A"); DB raw.spectype. Older catalogs sometimes list K4.5 V / K2 V (Feng 2019) — K5 V is the recommended modern type |
| `mass_msun` | 0.782 ± 0.023 | high | Lundkvist et al. 2024 — asteroseismic ν_max scaling (HARPS+UVES) with interferometric R (Phase 2 recommended); Demory et al. 2009 0.762 ± 0.038 agrees within 1σ |
| `radius_rsun` | 0.713 ± 0.006 | high | Lundkvist et al. 2024 — Rains 2020 θ_LD = 1.817 ± 0.013 mas + Gaia DR3 d = 3.648 pc (Phase 2 recommended); "in excellent agreement with the value found by Rains et al. 2020" |
| `teff_k` | 4700 ± 65 | high | Lundkvist et al. 2024 — high-resolution UVES spectroscopy (Phase 2 recommended); literature median ≈ 4649 K (Lundkvist §2.3) consistent |
| `luminosity_lsun` | 0.239 ± 0.001 | high | Feng et al. 2019 — bolometric flux (Phase 2 recommended); consistent with R 0.713, Teff 4700 via Stefan–Boltzmann |
| `metallicity_fe_h_dex` | null (not Phase-2-curated) | low | No Phase 2 metallicity array; skipped per project policy (sub-perception color effect at fixed Teff). Literature: −0.17 ± 0.03 (Lundkvist 2024 UVES), −0.06 ± 0.08 (Santos 2004 via Matthews 2026) — slightly sub-solar, not cfg-decisive |
| `age_gyr` | ~3.5 (not Phase-2-curated) | medium | Chen et al. 2022 — Bayesian activity-age (log R'HK = −4.72 Pace 2013 + ROSAT R_X = −5.62) gives 3.48 (+0.78/−1.03) Gyr; Feng 2019 ~4 Gyr, Cardoso 2012 3.7–4.3 Gyr corroborate. No Phase 2 age array; literature spans 0.39–5 Gyr (Lundkvist 2024 intro), the activity branch is adopted |
| `rotation_period_days` | ~35 | medium | Feng et al. 2018 — RV + spectroscopic activity-index (NaD/R'HK/BIS) periodograms; 17.8 d signal is the half-rotation alias of ~35 d. No formal σ; supersedes 22 d (Saar & Osten 1997) and ~20 d (Lachaume 1999). Not photometric (no published photometric period — Chen 2022) |
| `activity_log_rhk` | −4.72 | high | Chen et al. 2022 (adopting Pace 2013) — Ca II H&K chromospheric index (Phase 2 recommended); a quiet, intermediate-age K dwarf, slightly less active than the Sun's mean |
| `activity_cycle_years` | ~7.1 | medium | Lundkvist et al. 2024 §4.3 — ≈ 2600 d sinusoidal cycle phase-folded from 4293 HARPS archival log R'HK points (2003–2016); the asteroseismic amplitude varies inversely with the cycle |
| `visual_surface_tint_hex_primary` | `#ffb870` (warm orange-amber K5 V) | medium | Tie-break: 4700 K blackbody after molecular-band suppression of the blue, rendered deeper-amber than the warmer K-dwarfs (40 Eri A K0.5 V `#ffd5a8`, ε Eri K2 V `#ffd9a8`) and warmer than the M-dwarf reds; K5 V sits between |
| `stellar_color_temp_k` | 4700 | high | derived from Teff (Lundkvist et al. 2024) |
| `visual_spot_coverage_max` | 0.05 | low | Tie-break: a quiet K dwarf (log R'HK = −4.72) with a slow 35 d rotation supports only a low cool-spot fraction modulating the ~7 yr cycle. Not a measured filling factor |
| `disk_present` | false | high | No debris disk reported for ε Indi A in the literature; none fabricated (search-and-verify policy) |
| `companion_planet_present` | true (ε Indi A b, ~7.6 M_Jup cold super-Jupiter at ~20.9 AU) | high | Matthews et al. 2024 JWST/MIRI discovery image; Matthews 2026 second epoch + refined mass. Planet Phase 3 in `docs/phase3/eps-ind-a-b.md` |
| `companion_brown_dwarf_pair_present` | true (ε Indi Ba T1–1.5 66.9 M_Jup + Bb T6 53.3 M_Jup at ~1459 AU) | high | Chen et al. 2022 — VLT/NACO relative + FORS2 absolute astrometry; dynamical masses to <0.5%. Pending DB addition (not yet a NearStars body) |
| `apparent_magnitude_v_from_earth` | 4.66 | high | Gaia DR3 V (converted); a naked-eye star in Indus despite the modest 0.239 L☉ luminosity, thanks to its 11.9-ly proximity |
| `distance_pc` | 3.638 | high | Gaia DR3 parallax 274.84 mas; ≈ 11.87 ly |

## Surface synthesis

ε Indi A has the warm orange-amber photosphere typical of a late-K
dwarf. At Teff = 4700 K (Lundkvist 2024) the SED peaks in the
red-orange near ~620 nm, with the optical continuum shaped by the MgH
and CaH molecular bands and the first TiO heads beginning to bite below
~6300 Å — far less suppressed than a true M dwarf, but distinctly cooler
and more orange than the catalog's earlier K dwarfs (40 Eri A K0.5 V at
5143 K, ε Eri K2 V at 5039 K). With R = 0.713 R☉ and L = 0.239 L☉ the
star is roughly a quarter of the Sun's luminosity; at 11.9 light-years
this still places it well within naked-eye range (V = 4.66), the
brightest star in the southern constellation Indus.

The defining surface property is quietness. The chromospheric Ca II H&K
index log R'HK = −4.72 (Chen 2022, adopting Pace 2013) marks ε Indi A as
a quiet, intermediate-age K dwarf — slightly below the Sun's mean
activity and far below the active K dwarfs like ε Eri (−4.50). The
slow ~35 d rotation (Feng 2018) is consistent with the ~3.5 Gyr activity
age and with the magnetically-braked, unsaturated regime. Lundkvist 2024
recovered a ≈ 2600 d (≈ 7.1 yr) activity cycle by phase-folding 13 years
of HARPS Ca II H&K archive, and showed the asteroseismic mode amplitudes
vary inversely with the cycle (they happened to catch the star near
cycle minimum with HARPS in 2011 and near maximum with UVES in 2021).
For cfg rendering this means a warm orange-amber disk carrying only a
low cool-spot fraction (`visual_spot_coverage_max ≈ 0.05`) modulating
slowly on the multi-year cycle — a calm photosphere, not a flaring one.

The asteroseismic detection is itself a remarkable surface property:
ν_max = 5265 ± 110 µHz is the highest-frequency solar-like oscillation
spectrum ever measured (Lundkvist 2024), surpassing α Cen B and τ Ceti.
The oscillation amplitudes are tiny (~3.4 cm/s) — appropriate for a cool,
quiet, low-luminosity dwarf — and are not a directly visible feature,
but they anchor the asteroseismic mass that the cfg adopts.

No metallicity is curated in the Phase 2 layer and none is synthesized
here; the literature value is slightly sub-solar ([Fe/H] ≈ −0.17,
Lundkvist 2024; −0.06, Santos 2004), but at fixed Teff the effect on the
rendered K-dwarf color is sub-perceptible and project policy skips it.
There is no debris disk: no infrared-excess detection or resolved
imaging of a disk around ε Indi A has been reported, so the star is
rendered diskless.

## Atmosphere synthesis

A main-sequence star has no "atmosphere" in the planetary cfg sense; for
a stellar synthesis this section covers the chromosphere, corona, and
activity cycle.

ε Indi A's chromosphere and corona are those of a quiet, intermediate-age
K dwarf. The chromospheric Ca II H&K index log R'HK = −4.72 (Chen 2022,
adopting Pace 2013) sits below the solar mean, and the coronal X-ray
activity is correspondingly low — the ROSAT all-sky survey gives an
X-ray-to-bolometric ratio R_X = log(L_X/L_bol) ≈ −5.62 (via Chen 2022's
activity-age analysis), at the quiet end for a K dwarf. The slow ~35 d
rotation (Feng 2018) places ε Indi A in the unsaturated,
magnetically-braked regime, and the ~7.1 yr chromospheric cycle
(Lundkvist 2024) is a Sun-like activity cycle — shorter than the Sun's
11 yr but well-behaved and sinusoidal, with the asteroseismic amplitudes
modulating in anti-phase with it.

There is no headline flaring or magnetospheric phenomenon here, unlike
the catalog's active dwarfs. ε Indi A is a calm, quiet star whose
significance is its planetary and substellar companions rather than its
own activity. For cfg purposes the corona / chromosphere layer is
"quiet, with a Sun-like ~7 yr activity cycle" — distinct from both the
near-dead-quiet old M dwarfs and the loud young/active K and M dwarfs.

The one subtlety worth encoding for a faithful render is the activity
cycle: at cycle maximum the chromospheric emission and any cool-spot
modulation strengthen modestly, and the asteroseismic mode amplitudes
weaken — a coupled behavior that could drive a slow ~7 yr brightening /
spot-coverage animation if a future cfg renders it.

## Rotation & spin synthesis

ε Indi A rotates slowly, with a period P_rot ≈ 35 d (Feng 2018). The
value is not a photometric rotation period — the star "lacks a published
photometric rotation period" (Chen 2022) — but was derived from HARPS
radial velocities combined with spectroscopic activity-index periodograms
(NaD1/NaD2, R'HK, BIS), where the prominent 17.8 d signal is the
half-rotation alias of the true ~35 d period (Feng 2018, "The rotation
period of ε Indi is about 35 d, approximately double 17.8 d"). No formal
uncertainty is published. This ~35 d value supersedes the older, shorter
estimates of ~22 d (Saar & Osten 1997) and ~20 d (Lachaume 1999) that
were used in some earlier age determinations, and is corroborated by
Feng 2019. The cfg adopts 35 d at medium confidence because of the
absent σ and the non-photometric method.

**KSP implementation note.** Stellar rotation period ≈ 35 d =
3 024 000 s. In Kopernicus the star body's `rotationPeriod` is set in
seconds; the slow rotation makes spin-related visual foreshortening
negligible.

The rotation feeds the age. ε Indi A's age is one of the system's
long-standing open problems — Lundkvist 2024 notes estimates spanning
0.39–5 Gyr across rotation, activity, kinematic, and evolutionary
methods. The shorter rotation periods (~20 d) used by Lachaume 1999
yielded younger ages (0.8–2.0 Gyr); the modern ~35 d period and the
chromospheric activity push the age older. Chen 2022's Bayesian
activity-age method (log R'HK + X-ray + Tycho photometry) gives
3.48 (+0.78/−1.03) Gyr, consistent with Feng 2019's ~4 Gyr and with the
Cardoso 2012 evolutionary 3.7–4.3 Gyr — and this ~3.5 Gyr is what the
cfg adopts as the system age (also relevant to the brown-dwarf cooling
benchmarks and the "solar-age giant" framing of planet b). Because there
is no Phase 2 age array, the age is carried at medium confidence as a
literature-direct value.

The rotation-axis inclination is unconstrained for the photosphere. For
NearStars visual rendering a generic axis orientation is adopted, since
the slow rotation makes the precise spin axis visually unimportant for
the disk.

## Visual styling

In the NearStars renderer, ε Indi A is portrayed as a warm orange-amber
K5 V dwarf whose significance is its companions rather than its own
modest, quiet photosphere:

- **Global appearance.** A warm orange-amber disk encoded as `#ffb870`,
  the 4700 K blackbody continuum after molecular-band suppression of the
  blue — deeper-amber than the warmer K dwarfs in the catalog (40 Eri A
  K0.5 V `#ffd5a8`, ε Eri K2 V `#ffd9a8`) and clearly warmer (less red)
  than the M-dwarf reds (Barnard `#cf5a30`). K5 V sits between, and the
  tint is picked to read as the distinctly orange one among the nearby
  K dwarfs. The illumination color temperature for scene lighting is
  driven by the 4700 K SED.
- **Quiet spotted surface.** A low cool-spot fraction
  (`visual_spot_coverage_max ≈ 0.05`) modulating slowly on the 35 d
  rotation and the ~7 yr activity cycle. A calm disk — a few small,
  slowly-evolving spot groups, not the busy spotted surface of an active
  K dwarf.
- **Activity cycle (subtle).** A ~7.1 yr Sun-like chromospheric cycle
  (Lundkvist 2024) could be expressed as a slow, modest brightening of
  the chromospheric emission and a small rise in spot coverage at cycle
  maximum — a gentle multi-year animation, far weaker than ε Eri's
  loud 2.9 yr cycle.
- **No flares, no aurora.** Unlike the catalog's active dwarfs, ε Indi A
  has no defining flaring or magnetospheric feature; it renders as a
  steady, calm orange-amber star.
- **Companions in the sky (the headline).** The system's visual interest
  is the companions. The cold super-Jupiter ε Indi A b orbits at
  ~20.9 AU — from the star it is a distant, faint point; from the planet
  the star subtends ~1.1 arcmin (0.018°), about 1/30 the Sun's angular
  size from Earth, a brilliant orange-amber pinpoint. Far beyond, at
  ~1459 AU, the brown-dwarf pair ε Indi B (Ba + Bb) glows as two faint,
  deep-red T-dwarf points — invisibly dim to the eye from Earth but a
  striking pair in any wide-field render of the system.
- **From Earth.** ε Indi A is a V = 4.66 naked-eye star in Indus,
  visible without a telescope despite its modest 0.239 L☉ luminosity
  because of its 11.9-light-year proximity — one of the nearest
  naked-eye stars in the sky.

## Bibliography

### Read (drove Decisions above)

- **Lundkvist M. S. et al. 2024** — *Low-amplitude solar-like
  oscillations in the K5 V star ε Indi A*, ApJ 964, 110
  (`2024ApJ...964..110L`, doi:10.3847/1538-4357/ad25f2,
  arXiv:2403.04509). Detects solar-like oscillations at ν_max =
  5265 ± 110 µHz (highest-frequency ever measured), giving an
  asteroseismic mass M = 0.782 ± 0.023 M☉ via ν_max scaling with the
  interferometric R = 0.713 ± 0.006 R☉ (Rains 2020 θ_LD + Gaia d).
  Teff = 4700 ± 65 K and [Fe/H] = −0.17 from UVES; a ≈ 2600 d activity
  cycle from the HARPS R'HK archive. Phase 2 recommended anchor for
  mass/radius/Teff.
- **Feng F. et al. 2019** — *Detection of the nearest Jupiter analog in
  radial velocity and astrometry data*, MNRAS 490, 5002
  (`2019MNRAS.490.5002F`, doi:10.1093/mnras/stz2912, arXiv:1910.06804).
  RV + Hipparcos/Gaia astrometric detection of ε Indi A b; Phase 2
  recommended source for the luminosity (0.239 L☉) and corroborating
  the ~35 d rotation and ~4 Gyr age. The planet orbit here (a ≈ 11.6 AU,
  ~3 M_Jup) is superseded by Matthews 2026.
- **Feng F. et al. 2018** — *Detection of the closest Jovian exoplanet
  in the ε Indi triple system* (`2018arXiv180308163F`, arXiv:1803.08163).
  arXiv preprint; Phase 2 recommended source for the rotation period
  (~35 d, from RV + activity-index periodograms; the 17.8 d signal is
  the half-rotation alias). No refereed bibcode — superseded for the
  planet orbit by Feng 2019 / Matthews 2026.
- **Chen M. et al. 2022** — *Precise Dynamical Masses of ε Indi Ba and
  Bb: Evidence of Slowed Cooling at the L/T Transition*, AJ 163, 288
  (`2022AJ....163..288C`, doi:10.3847/1538-3881/ac66d2,
  arXiv:2205.08077). VLT/NACO relative + FORS2 absolute astrometry of the
  brown-dwarf pair: Ba (T1–1.5) 66.92 ± 0.36 M_Jup, Bb (T6)
  53.25 ± 0.29 M_Jup. Phase 2 recommended source for ε Indi A's activity
  index (log R'HK = −4.72, Pace 2013) and the adopted system age
  (3.48 +0.78/−1.03 Gyr, Bayesian activity-age) — also the source for the
  brown-dwarf-pair Decisions row.

### Read (context / methodology, not decision-driving)

- **Matthews E. C. et al. 2024** — JWST/MIRI direct-imaging discovery of
  ε Indi A b (`2024Natur.633..789M`, arXiv:2503.01599). Establishes the
  ~275 K cold super-Jupiter and the elevated-metallicity / 3–5 µm
  faintness context. Drives the planet b synthesis
  (`docs/phase3/eps-ind-a-b.md`); cited here for the system framing. The
  ar5iv full text was not available in the cache (HTML-only stub);
  numbers are taken from the abstract and from Matthews 2026's recap.
- **Matthews E. C. et al. 2026** — *A second visit to ε Ind Ab with
  JWST*, ApJL (doi:10.3847/2041-8213/ae5823, arXiv:2603.08780). Second
  JWST/MIRI epoch confirming ammonia + suggesting thick water-ice clouds;
  refined mass 7.6 ± 0.7 M_Jup, a = 20.9 AU, e = 0.244. Drives the planet
  b synthesis; cited here for the system framing.
- **Demory B.-O. et al. 2009** — VLTI/VINCI interferometric radius/Teff/L
  (`2009A&A...505..205D`). Phase 2 alternative mass 0.762 ± 0.038 M☉ (via
  the Xia 2008 M–L relation), agreeing with Lundkvist 2024 within 1σ.
  VizieR-only (no ar5iv body); not table-verified in this session.
- **Santos N. C. et al. 2004** — Spectroscopic metallicities for
  planet-host stars (`2004A&A...415.1153S`). [Fe/H] = −0.06 ± 0.08 for
  ε Indi A (cited via Matthews 2026); context for the skipped-metallicity
  row.

### Read (instrument-only, not visual-informative)

- The asteroseismic methodology of Lundkvist 2024 (HARPS/UVES RV time
  series, weighted power spectra, ν_max envelope fitting) and the
  astrometric methodology of Chen 2022 (NACO relative + FORS2 absolute
  astrometry, orvara-style orbit fits) are the instrument backbone of the
  mass and age determinations but contribute no direct visual field
  beyond the values already used above.

### Not read — no arXiv preprint or low-priority (~handful)

The Demory 2009 VLTI/VINCI per-star interferometric table lives in
VizieR (J/A+A/505/205) rather than an ar5iv body and was marked
manual_followup in the bibliography; its mass value is carried as a
Phase 2 alternative. Older rotation/age estimates (Saar & Osten 1997
~22 d, Lachaume 1999 ~20 d) are superseded by the Feng 2018 ~35 d period
and the Chen 2022 activity age, and are retained only as historical
context. No debris-disk papers exist to read (none reported).

## Stellar wind / astrosphere

ε Ind A is the textbook **compact astrosphere**: a moderate wind (Ṁ = 0.5 Ṁ⊙)
running into a fast ~68 km/s ISM inflow stands off at only **~32 AU** — Wood 2005
explicitly calls it compact, and our 6D-astrometry V_ISM (69 km/s) reproduces
Wood's 68 km/s, validating the method. It cycles on **5.65 yr** (Laliotis 2023;
matching Lovis 2011's 4.71 yr). An active-ish old K dwarf, roughly solar in
particle environment.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `solar_cycle_yr` | 5.65 | high | Laliotis 2023 S-index (matches Lovis 2011 4.71 yr to 1.5σ) |
| `stellar_wind_mass_loss_solar` | 0.5 | high | Wood 2005 astrospheric Lyα (compact astrosphere) |
| `local_ism_inflow_speed_kms` | 68 | high | Wood 2005; 6D-astrometry calc (69) confirms |
| `astrosphere_standoff_au` | ~32 (compact) | high | 120·√0.5·(25.4/68); matches Wood's description |
| `stellar_radiation_surface_relative_sun` | ~1.0 | low | active old K (R'HK −4.72) — interesting-first near solar |
| `astrosphere_apex_ra_deg` / `_dec_deg` | ~110 / +2 | low | 6D astrometry vs LIC; **plugin-only** |

## Open items for follow-up

- **Planet Phase 3 synthesis.** ε Indi A b is produced as a separate
  Phase 3 doc (`eps-ind-a-b.md`), anchored on Matthews 2024/2026. It is
  the nearest directly-imaged cold super-Jupiter and the system's
  headline feature.
- **Brown-dwarf pair ε Indi B (pending DB addition).** Ba (T1–1.5,
  66.9 M_Jup) + Bb (T6, 53.3 M_Jup) at ~1459 AU (Chen 2022) are not yet
  NearStars bodies. Adding them — with the Chen 2022 dynamical masses and
  the Ba–Bb mutual orbit — would let the cfg render the full ε Indi
  hierarchical triple. They are mentioned in this synthesis but no DB or
  Phase 3 doc is created for them here.
- **Age.** No Phase 2 age array. The ~3.5 Gyr Chen 2022 activity age is a
  literature-direct value carried at medium confidence; if a future
  curation adds a gyrochronology, asteroseismic, or kinematic age, the
  cfg age should be replaced. The 0.39–5 Gyr literature spread
  (Lundkvist 2024) is the residual uncertainty.
- **Rotation period uncertainty.** Feng 2018 reports "~35 d" with no
  formal σ and via an RV-activity-index (not photometric) method. A TESS
  or dedicated photometric rotation measurement would tighten the value
  and the gyrochronological age cross-check.
- **Metallicity.** Skipped per project policy; literature ≈ −0.17
  (Lundkvist 2024). If a future cfg needs a metallicity-reddening tweak
  the value is available, but the color effect is sub-perceptible at
  fixed Teff.
- **Activity-cycle visualization fidelity.** The ~7.1 yr Sun-like cycle
  (Lundkvist 2024) is a tie-break visual choice for slow brightening /
  spot-coverage modulation; refine the cycle-phase anchoring to the
  game epoch once a renderer can show it.

## Related

- [methodology](../reference/methodology.md) — schema source for the Decisions table
- [eps-ind-a-b](eps-ind-a-b.md) — the nearest directly-imaged cold super-Jupiter (~7.6 M_Jup, ~20.9 AU); JWST ammonia + water-ice clouds
- [eps-eri](eps-eri.md) — comparison nearby K dwarf (K2 V) with a confirmed jovian and a resolved triple-ring disk; contrast ε Eri's loud activity + disk against ε Indi A's quiet, disk-free photosphere
- [40-eridani-a](40-eridani-a.md) — comparison nearby K dwarf (K0.5 V) in a triple system; warmer and similarly quiet
- [alpha-centauri-b](alpha-centauri-b.md) — comparison K1 V dwarf with measured asteroseismology; ε Indi A's ν_max is the higher of the two
- [rex-data-comparison](../reference/rex-data-comparison.md) — REX has a basic stellar entry for ε Indi A; the cold super-Jupiter and the brown-dwarf-pair hierarchy are NearStars additions
