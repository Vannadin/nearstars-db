<!-- Vega Phase 3 synthesis: cfg-ready decisions and reasoning -->
# Vega — Phase 3 Synthesis

Vega (α Lyrae, HD 172167, HIP 91262) is the fifth-brightest star in the night sky and the prototype A0Va dwarf, sitting at 7.679 pc (parallax 130.23 mas; SIMBAD). It is the historical zero-point of the Johnson photometric system and, since IRAS scanned it in 1983, the archetype debris-disk star — the term "Vega-like" excess was coined here (Aumann et al. 1984, `1984ApJ...278L..23A`). The stellar parameters the NearStars DB carries are anchored on Monnier et al. 2012 (`2012ApJ...761L...3M`), the most recent CHARA/MIRC imaging revision: M = 2.15 (+0.10/−0.15) M☉, equatorial R = 2.726 ± 0.006 R☉ (polar 2.418), surface-area-averaged Teff = 9360 ± 90 K (polar 10070 K vs. equatorial 8910 K), and bolometric L = 47.2 ± 2.0 L☉ — all products of the modern picture of Vega as a near-pole-on rapid rotator rather than a slowly-rotating photometric standard. Monnier found weaker gravity darkening and slower rotation (ω/ω_crit = 0.774) than the earlier Aufdenberg et al. 2006 / Yoon et al. 2010 work.

Vega has no confirmed planets. The deepest RV searches (Hunsch & Schmitt 2019 and references therein; Hurt et al. 2021, `2021AJ....161..157H`) rule out > 0.3 M_Jup companions inside ~7 AU and place ~Saturn-mass upper limits across the inner asteroid-belt analog region. A candidate ~0.6-day signal at 0.04 AU has been discussed (Hurt 2021) but is not regarded as confirmed at synthesis date. The system that *does* dominate Vega's visual identity is its two-belt circumstellar disk: a warm inner zone at ~14 AU consistent with an asteroid-belt-like population, and a cold outer ring resolved from ~70 AU to ~200 AU, separated by a cleared gap that almost certainly implies one or more unseen planetesimal-belt-stirring planets between ~14 and ~70 AU (Su et al. 2013, `2013ApJ...763..118S`; Sibthorpe et al. 2010, `2010A&A...518L.130S`; Hughes et al. 2012, `2012ApJ...750...82H`).

**Scenario choice for NearStars: a near-pole-on A0 Va rapid rotator (i ≈ 6.5°), gravity-darkened from ~10070 K polar to ~8910 K equatorial, sitting at the center of a luminous two-belt debris disk viewed face-on.** The pole-on geometry is the visually defining feature — most A-star illustrations show a uniform white-blue disk, but the cfg portrays Vega's bright hot pole staring straight at the player while the cooler equator forms a darker limb-band. The disk is rendered as a luminous IRAS-discovery-era face-on dust ring. Every Decisions row with Confidence=high tracks observation; the disk geometry rows are Confidence=medium because resolved imaging exists but the model parameterizations differ (Su 2013 vs. Sibthorpe 2010 inner-radius disagreement of ~3 AU); the synth-only fields (tint hex, opacity) are Confidence=low tie-breaks documented in the Basis column.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | A0 Va | high | Keenan & McNeil 1989; SIMBAD harmonized MK |
| `mass_msun` | 2.15 (+0.10/−0.15) | high | Monnier et al. 2012 (`2012ApJ...761L...3M`) — rotation-aware Geneva-track fit (Phase 2 recommended; Yoon 2010 2.135 agrees) |
| `radius_rsun` (equatorial) | 2.726 ± 0.006 | high | Monnier et al. 2012 — CHARA/MIRC imaging; equatorial radius of the oblate rapid rotator (R_pole = 2.418 ± 0.012 R☉, R_eq/R_pole ≈ 1.13) |
| `teff_k` (effective) | 9360 ± 90 | high | Monnier et al. 2012 — surface-area-averaged Teff (Phase 2 recommended; T_pole 10070 / T_eq 8910; supersedes the SIMBAD 9692) |
| `luminosity_lsun` | 47.2 ± 2.0 | high | Monnier et al. 2012 — bolometric (Phase 2 recommended; apparent pole-on-inflated value is 58.4 ± 2.2) |
| `metallicity_fe_h_dex` | −0.5 | medium | Yoon 2010 — metal-weak λ Boo surface abundance (Z = 0.006–0.008); Vega is a known λ Boo-class A-star (Adelman & Gulliver 1990) |
| `age_gyr` | 0.7 (+0.15/−0.075) | high | Monnier et al. 2012 — rotation-aware evolutionary tracks (Phase 2 recommended). DOCUMENTED DIVERGENCE vs Yoon 2010 non-rotating isochrone 0.455 ± 0.013 Gyr (see Canonical alternatives) |
| `rotation_v_eq_km_s` | ~195 | high | Monnier et al. 2012 — the revised (slower) rotation; ω/ω_crit = 0.774 ± 0.012 (Aufdenberg/Peterson's earlier 274 km/s assumed a faster ω ≈ 0.91) |
| `rotation_period_days` | 0.71 ± 0.03 | high | Petit et al. 2010 (`2010A&A...523A..41P`) — spectropolarimetric magnetic rotation period (≈17.0 h; Alina 2012 confirms; Phase 2 recommended) |
| `limb_darkening_alpha_h` | n/a (replaced by gravity-darkening model) | high | Vega is not well-fit by a single-α limb-darkening law; the 2D von Zeipel gravity-darkening β = 0.231 ± 0.028 (Monnier 2012) is the cfg-relevant parameter |
| `visual_gravity_darkening_pole_equator_temp_diff_k` | 1160 (T_pole 10070 K, T_eq 8910 K) | high | Monnier 2012 — CHARA/MIRC; the modern revision found WEAKER gravity darkening than Aufdenberg 2006's 2250 K (10150/7900) |
| `visual_surface_tint_hex_primary` | `#cfe0ff` (pole-on hot-white-blue with cooler equatorial limb) | low | Tie-break: blackbody at area-averaged 9360 K is a near-pure white-blue; cfg shifts marginally bluer to emphasize the hot polar face that dominates the pole-on view, the limb darkening toward `#e8eef8` (~8910 K) in the equatorial band. Interesting-first per `conflict-resolution.md`. |
| `stellar_color_temp_k` | 9360 | high | derived from area-averaged Teff for in-game illumination |
| `radius_rsun_polar` | 2.418 ± 0.012 | high | Monnier et al. 2012 — polar radius of the oblate rotator (the cfg should render the star oblate; mean ~2.6 R☉) |
| `rotation_omega_crit_ratio` | 0.774 ± 0.012 | high | Monnier et al. 2012 — fraction of critical (break-up) angular velocity (the revised, slower value vs Aufdenberg's 0.91) |
| `visual_pole_on_inclination_deg` | ~6.5 | high | Monnier et al. 2012 (i = 6.2 ± 0.4°); stellar spin axis very nearly along the line of sight to Earth |
| `activity_log_rhk` | n/a (A0 V has no convective dynamo/chromosphere — intentionally not recorded) | high | A0 V radiative envelope — no log R'HK is defined. Vega itself is an X-ray NON-detection, L_X < 2 × 10²⁵ erg/s (Pease, Drake & Kashyap 2006); the log L_X ≈ 25.5–26 X-ray that Robrade & Schmitt 2011 detected is attributed to a low-mass COMPANION, not Vega |
| `disk_present` | true | high | Aumann et al. 1984 — IRAS 60/100 μm excess; the *defining* Vega-like disk observation |
| `disk_belts` | warm, cold | high | Su et al. 2013 two-component SED: a warm inner belt + a cold outer belt separated by a cleared gap |
| `disk_warm_inner_radius_au` | 14 ± 2 | medium | Su et al. 2013 — warm asteroid-analog inner belt at ~14 AU (Spitzer-IRS + Herschel-PACS) |
| `disk_warm_dust_temperature_k` | 170 | medium | Su et al. 2013 two-component SED — warm dust population |
| `disk_warm_mass_mearth` | 0.0003 | medium | Su et al. 2013 — warm-belt dust mass |
| `disk_warm_tint_rgb_hex` | `#dde3ed` (pale blue-white) | low | No optical scattered-light color measured (Vega's belts are resolved only in thermal IR/mm); synthesized from Vega's A0V blue-white color + grain albedo. Large debris grains scatter near-neutrally, so the belt reads close to the star color |
| `disk_warm_opacity` | 0.02 | low | Tie-break: τ ~ 10⁻⁴ (Su 2013); boosted to a faint-but-visible value |
| `disk_cold_inner_radius_au` | 110 ± 9 | medium | Su et al. 2013 — cold Kuiper-analog inner edge ~110 AU (audit 2026-05-29: corrected from 62) |
| `disk_cold_outer_radius_au` | 200 ± 20 | medium | Sibthorpe et al. 2010 (`2010A&A...518L.130S`) Herschel-PACS — cold belt extends to ~200 AU |
| `disk_cold_dust_temperature_k` | 50 | medium | Su et al. 2013 — cold dust population |
| `disk_cold_mass_mearth` | 0.013 | medium | Su et al. 2013 — cold-belt dust mass; parent-body mass much larger but unobserved |
| `disk_cold_tint_rgb_hex` | `#d6deec` (faint blue-white) | low | No optical scattered-light color measured (thermal IR/mm only); synthesized from Vega's A0V blue-white color + albedo. The two belts differ by radius/brightness, not hue |
| `disk_cold_opacity` | 0.06 | low | Tie-break: τ ~ 10⁻⁴ (Su 2013); boosted for visibility. Conservative value in Open items |
| `disk_morphology` | two-belt: warm asteroid-analog at ~14 AU + cold Kuiper-analog at ~110–200 AU + a cleared gap (14→110 AU) implying planetesimal-stirring planets | high | Su et al. 2013 two-component SED + Spitzer-MIPS imaging; the cleared gap is the strongest indirect planet evidence at Vega |
| `disk_resolved_imaging` | true | high | Holland 1998 SCUBA 850 μm (`1998Natur.392..788H`); Wilner 2002 OVRO 1.3 mm; Su 2013 Spitzer-MIPS; Sibthorpe 2010 Herschel-PACS; Hughes 2012 ALMA |
| `disk_imaging_observatory` | IRAS (1983) → JCMT-SCUBA (Holland 1998) → Spitzer-MIPS (Su 2013) → Herschel-PACS (Sibthorpe 2010) → ALMA (Hughes 2012) | high | Standard Vega-like heritage chain |
| `disk_imaging_inclination_deg` | 6.2 (face-on, locked to stellar pole-on geometry) | medium | Sibthorpe 2010 / Su 2013 — disk i ≈ 6° consistent with the stellar spin axis (both belts coplanar) |
| `disk_planetesimal_belt_inferred` | true | high | Dust lifetime at 110–200 AU ≪ system age 0.45 Gyr; planetesimal replenishment required (Sibthorpe 2010 §5) |

## Surface synthesis

Vega's "surface" is not a single-temperature photosphere. The CHARA Array interferometric campaigns of Aufdenberg et al. 2006 and Monnier et al. 2012 resolve the star as an oblate rotator viewed nearly pole-on, with its rotation axis tipped just ~6.5° off the line of sight to Earth. Monnier's revised ω/ω_crit = 0.774 — the equator is rotating at ~77% of breakup velocity (the earlier Aufdenberg fit had given 0.91). The classical von Zeipel theorem (1924) predicts flux ∝ g_eff^β with β = 0.25 for radiative envelopes; the empirical fit gives β ≈ 0.231 (Monnier 2012). The visible consequence is a hot bright pole — T_pole ≈ 10070 K — staring directly at the observer, surrounded by a cooler equatorial band at T_eq ≈ 8910 K that forms a slightly darker annulus at the limb. This ~1160 K pole-to-equator temperature gradient (Monnier 2012; weaker than Aufdenberg 2006's 2250 K) is the defining visual property of Vega and the reason every classical "Vega is a hot blue-white A0" textbook illustration is wrong in detail — what an observer sees is closer to a small, intensely bright white-blue dot with a subtle cooler halo.

The pole-on geometry has a second consequence relevant for the NearStars renderer: the equatorial limb darkening is dominated by gravity darkening, not by classical limb darkening. A single-parameter α exponent in the Claret 2011 / Kervella 2017 sense does not fit Vega's H-band interferometric visibilities; the relevant cfg field is the gravity-darkening β coefficient and the inclination, which combine to produce the observed brightness profile. NearStars stores the inclination and pole/equator temperatures explicitly rather than collapsing to a single α.

Vega is also a member of the λ Boötis class of chemically peculiar A-stars (Adelman & Gulliver 1990; Yoon 2010 adopts [M/H] ≈ −0.5 in best-fit models). The photosphere shows depleted heavy-element abundances compared with the bulk stellar composition, attributed to selective accretion of gas-depleted interstellar material or to circumstellar-disk fractionation. The surface metallicity tints the SED marginally toward the blue (less line blanketing in the UV), reinforcing the visual choice of `#cfe0ff` over a more cream blackbody match.

The photosphere is too hot to host significant convective granulation. The outer envelope is radiative; surface structure is dominated by rotation rather than by convective cells, and spot coverage is essentially zero. Petit et al. 2010 (`2010A&A...523A..41P`) detected weak magnetic field (~0.6 G longitudinal) with ZDI suggesting a polar magnetic spot — this is one of the first magnetic detections on a "non-Ap" A-star and may explain the anomalously weak X-ray emission, but it produces no visible photometric variability at typical cfg time scales.

## Atmosphere synthesis

A0V dwarfs do not have a chromosphere in the cool-star sense. The radiative envelope provides no convective dynamo to power Ca II H&K emission, and the standard log R'HK activity index is undefined for Vega. The Mg II h+k and Ca II H&K lines appear purely as photospheric absorption with no chromospheric core emission reversal — a defining feature of the photometric A0V standard.

Vega itself is, in fact, an X-ray NON-detection: Pease, Drake & Kashyap 2006 (`2006ApJ...636..426P`) place a deep upper limit L_X < 2 × 10²⁵ erg/s on the A-star — "the darkest bright star." The weak log L_X ≈ 25.5–26 X-ray that Robrade & Schmitt 2011 (`2011A&A...531A..58R`) detected is attributed to a low-mass COMPANION, not to Vega's radiative envelope (their title is explicit: "X-ray detection of the very low-mass companion of Vega-like α Lyrae"). So the cfg carries no coronal activity for Vega itself. NearStars adopts no in-game flare model for Vega — A0 V radiative envelopes produce none.

The integrated UV output is, however, enormous: at 47 L☉ with a peak SED in the near-UV, Vega delivers ~30× the solar UV flux at equivalent distance. This XUV-driven photoevaporation has been invoked (Wilner 2002; Sibthorpe 2010) as the mechanism that clears small dust grains from the inner disk and may be partially responsible for the gap between the warm and cold belts. Any hypothetical inner planet would experience an extreme UV environment — relevant only as flavor text since no planet has been detected.

The visible "sky" of Vega, in the sense of any extended optical-depth structure, is dominated not by a chromosphere but by the surrounding debris disk seen in scattered light at small angular separations and by the gravity-darkened pole-equator gradient at the photosphere itself. There is no atmospheric haze, no corona-on-the-limb feature analogous to a G-dwarf, and no observable extended outflow.

## Rotation & spin synthesis

Vega rotates at v_eq sin i = 22 ± 2 km/s in classical line-broadening measurements (Gulliver et al. 1994), which historically encouraged the misclassification of Vega as a slow rotator. The CHARA interferometric resolution (Aufdenberg 2006; Peterson 2006, `2006Natur.440..896P`) revealed that this small sin i is not a small v_eq but a small i. Aufdenberg/Peterson inferred v_eq ≈ 274 km/s at ω/ω_crit ≈ 0.91; the later higher-resolution Monnier 2012 CHARA/MIRC imaging revised this DOWNWARD to ω/ω_crit = 0.774 (v_eq ≈ 195 km/s) with weaker gravity darkening — still among the most rapidly rotating bright stars, but less extreme than first thought.

The cfg adopts the Petit et al. 2010 rotation period of 0.71 ± 0.03 d (≈ 17.0 h), measured from spectropolarimetric (ZDI) magnetic-field rotational modulation and confirmed by Alina 2012 — the Phase 2 recommended value. (A naive 2π·R_eq/v_eq estimate gives ~12.5 h at the old 274 km/s v_eq, but Monnier's revised slower rotation, v_eq ≈ 195 km/s and ω/ω_crit = 0.774, is consistent with the longer magnetic period.)

The spin axis is the most-constrained orientation parameter in the entire star: i ≈ 6.2° ± 0.3° (Aufdenberg 2006), which means in the Kerbal frame Vega's pole points almost exactly at Sol. The visual consequence in the NearStars renderer is that from any vantage point near Earth/Kerbin, the player looks down on Vega's hot bright pole; the cooler equatorial band is seen edge-on as a darker rim. This is the geometry the cfg portrays — no need to invent a tilt, the literature gives it directly.

Obliquity of the disk and rotation axis are aligned within errors (Sibthorpe 2010; Su 2013), consistent with a coeval-formation scenario in which the disk and stellar spin share the original protoplanetary angular momentum vector. No precession or secular axis drift is implemented in the cfg.

## Visual styling

- **Global appearance (orbit-view).** A small, intensely bright white-blue stellar disk (face-on pole; T ≈ 10150 K) surrounded by a faint warm-cream halo where the cooler equator forms a darker limb-band. At KSP rendering distances Vega appears as a nearly-point source with the gravity-darkened gradient just barely resolvable at very close fly-by — the visual is dominated by the spectacular surrounding face-on debris disk.
- **Surface detail.** No granulation, no sunspots, no faculae. The dominant visible feature is the ~1160 K pole-to-equator temperature gradient (Monnier 2012): a brilliant `#cfe0ff` near the apparent center fading to `#e8eef8` near the equatorial limb (a subtler gradient than Aufdenberg 2006's 2250 K would have implied). The transition is smooth (no sharp boundary) and roughly axisymmetric for the pole-on viewer.
- **Polar / equatorial features.** A faint ZDI polar magnetic spot (Petit 2010) — not visually rendered in current cfg but listed as an Open items extension.
- **Atmosphere haze.** None. A-stars have no chromosphere; the limb cuts cleanly without a soft haze band.
- **Debris-disk visual (the showpiece feature).** Vega is the IRAS-archetype debris disk and the cfg portrays it as the visually dominant element of the system at distance. The disk renders as one Kopernicus `Ring` per belt (multi-belt): an inner warm belt at ~14 AU as a faint, dim, narrow torus glowing with pale blue-white `#dde3ed` tones (scattered A0V starlight off near-neutral grains), essentially invisible at orbit-view zoom and becoming visible when the player approaches the inner system; a cleared gap from 14 to 110 AU forming an empty annulus that visually identifies where unseen planetesimal-belt-stirring planets must exist — the cfg's strongest visual hint at Vega's "missing planets"; and an outer cold belt from 110 to 200 AU as the main visual element, a face-on bright ring with faint blue-white `#d6deec` tones (scattered A0V starlight; no optical color measured), opacity 0.06, sharper inner edge than outer per Sibthorpe 2010 morphology — the structure IRAS discovered and the cfg's defining "you are at Vega" cue.
- **Star in sky (from a hypothetical inner planet at 1 AU).** Apparent diameter ≈ 2 · R_eq / a · (180·60/π) ≈ 2 · 2.726 · 696000 / 1.496×10⁸ · (60·180/π) ≈ 0.087° (~5.2 arcmin) — about 16% of the Sun's apparent diameter from Earth, but ~7× brighter per unit area (Teff ratio)^4. The illumination color temperature ~9360 K renders as a slightly blue daylight; sunlight has a noticeable extra blue cast vs. solar reference.
- **Disk-in-sky from a hypothetical inner planet.** The outer belt at 110–200 AU subtends ~30° to ~90° in the sky as a face-on ring — a striking nighttime "Vega ring" easily one of the most visually distinctive features in NearStars. The pole-on geometry means the ring is seen as a true ring (full annulus), not as an edge-on streak.
- **Sister planets in sky.** None confirmed; cfg has no planet bodies for Vega. If the Su 2013 gap-clearer planets are added in a future cfg variant, they would appear as inner-system point sources.

## Canonical alternatives

**Age — rotation-aware vs non-rotating isochrone.** The cfg adopts the
Monnier 2012 age 0.7 (+0.15/−0.075) Gyr from rotation-aware Geneva
tracks. The documented alternative is the Yoon 2010 value 0.455 ± 0.013
Gyr from non-rotating-model isochrones; Monnier's explicit treatment of
rapid rotation pushes the age substantially older. Both supersede the
classic ~350 Myr estimates.

**Rotation / gravity darkening — Monnier vs Aufdenberg/Peterson.** The
cfg uses Monnier 2012's revised ω/ω_crit = 0.774 (v_eq ≈ 195 km/s) and
the weaker 1160 K pole-to-equator gradient (T_pole 10070, T_eq 8910).
The earlier Aufdenberg 2006 / Peterson 2006 fits gave a faster ω ≈ 0.91
(v_eq 274 km/s) and a stronger 2250 K gradient (10150/7900); Monnier's
higher-resolution CHARA/MIRC imaging is the modern revision and the cfg
default. The equatorial Teff in particular ranges 7557 K (Peterson) to
8910 K (Monnier) across the gravity-darkened models.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Aumann H. H. et al. 1984** — *Discovery of a Shell Around Alpha Lyrae*, ApJ 278, L23 (`1984ApJ...278L..23A`). The IRAS discovery paper that named the "Vega phenomenon"; 60 and 100 μm excess; first debris disk ever identified.
- **Aufdenberg J. P. et al. 2006** — *First results from the CHARA Array. VII. Long-baseline interferometric measurements of Vega consistent with a pole-on, rapidly rotating star*, ApJ 645, 664 (`2006ApJ...645..664A`, arXiv:astro-ph/0603327). CHARA H-band interferometry; v_eq = 274 km/s, i = 5° ± 2°, T_pole = 10150 K, T_eq = 7900 K, ω/ω_crit = 0.91; defines the modern picture of Vega.
- **Peterson D. M. et al. 2006** — *Vega is a rapidly rotating star*, Nature 440, 896 (`2006Natur.440..896P`). Independent NPOI interferometric confirmation; same conclusion as Aufdenberg.
- **Monnier J. D. et al. 2012** — *Resolving Vega and the Inclination Controversy with CHARA/MIRC*, ApJ 761, L3 (`2012ApJ...761L...3M`, arXiv:1211.6055). **Phase 2 anchor.** Higher-resolution CHARA/MIRC imaging: R_eq 2.726 ± 0.006 / R_pol 2.418 R☉, surface-mean Teff 9360 ± 90 (T_pole 10070 / T_eq 8910), L_bol 47.2 ± 2.0, mass 2.15, age 0.7 (+0.15/−0.075) Gyr, ω/ω_crit 0.774, β 0.231. Found WEAKER gravity darkening and slower rotation than the earlier work.
- **Yoon J. et al. 2010** — *A New View of Vega's Composition, Mass, and Age*, ApJ 708, 71 (`2010ApJ...708...71Y`). Rotating-model isochrone: M 2.135, age 0.455 ± 0.013 Gyr (the documented-divergence alternative to Monnier's rotation-aware 0.7 Gyr — see Canonical alternatives), [M/H] = −0.5 (the cfg metallicity source; resolves the Vega "metallicity problem" as λ Boo surface depletion).
- **Pease D. O., Drake J. J. & Kashyap V. L. 2006** — *The Darkest Bright Star: Chandra X-Ray Observations of Vega*, ApJ 636, 426 (`2006ApJ...636..426P`). Deep Chandra non-detection of Vega, L_X < 2 × 10²⁵ erg/s — the Phase 2 basis for "no coronal activity"; the Robrade 2011 X-ray is a companion, not Vega.
- **Su K. Y. L. et al. 2013** — *Asteroid Belts in Debris Disk Twins: Vega and Fomalhaut*, ApJ 763, 118 (`2013ApJ...763..118S`, arXiv:1211.7298). Spitzer-IRS + Herschel-PACS two-component SED fit; warm 170 K inner belt at 14 AU, cold 50 K outer belt at ~110–200 AU; cleared gap implying planetesimal-stirring planets; defines the two-belt cfg morphology.
- **Sibthorpe B. et al. 2010** — *The Vega debris disc: A view from Herschel*, A&A 518, L130 (`2010A&A...518L.130S`). Herschel-PACS 70/100/160 μm resolved imaging; disk radial profile with sharper inner edge than outer; supports radiation-pressure / PR-drag depletion of small grains; outer-edge radius ~200 AU.
- **Holland W. S. et al. 1998** — *Submillimetre images of dusty debris around nearby stars*, Nature 392, 788 (`1998Natur.392..788H`). JCMT-SCUBA 850 μm; first sub-mm resolved image of Vega's disk; established the cold debris ring structure.
- **Hughes A. M. et al. 2012** — *Confirmation of the Vega Asteroid Belt with Combined Spitzer and Submillimeter Array Observations*, ApJ 750, 82 (`2012ApJ...750...82H`, arXiv:1203.0598). SMA / early-ALMA-era 880 μm observations; confirms cold-belt structure; constrains inner edge.
- **Petit P. et al. 2010** — *A weak magnetic field at the surface of Vega*, A&A 523, A41 (`2010A&A...523A..41P`, arXiv:1006.5868). NARVAL spectropolarimetry; ~0.6 G longitudinal field, possible polar magnetic spot, P_rot ZDI estimate 0.732 d (longer than equatorial 12.5 h due to higher-latitude anchoring).

### Read (context / methodology, not directly decision-driving)

- **Adelman S. J. & Gulliver A. F. 1990** — Abundance analysis of Vega; identifies the λ Boötis spectral peculiarity. Methodology reference for the [M/H] = −0.5 photospheric value.
- **Gulliver A. F. et al. 1994** — *The Spectrum of Vega: A Pole-on View of a Rapidly Rotating Star*, ApJ 429, L81. First spectroscopic suggestion (pre-CHARA) that Vega's small v sin i hides a large v.
- **Robrade J. & Schmitt J. H. M. M. 2011** — *X-ray detection of the very low-mass companion of Vega-like α Lyrae*, A&A 531, A58 (`2011A&A...531A..58R`). XMM-Newton detection at log L_X ≈ 25.5–26 erg/s; controversial interpretation between weak corona and companion contamination.
- **Hurt S. A. et al. 2021** — *A Decade of Radial Velocity Monitoring of Vega*, AJ 161, 157 (`2021AJ....161..157H`). Deepest RV upper limits to date; candidate 0.6-day signal at 0.04 AU, unconfirmed; rules out Saturn-mass companions inside ~7 AU.
- **Wilner D. J. et al. 2002** — *Toward Imaging the Vega Belt*, ApJ 569, L115. OVRO 1.3 mm interferometric imaging; early sub-mm structure mapping.
- **Hunsch M. & Schmitt J. H. M. M. 2019** — Review of radial velocity constraints on A-star planet hosts including Vega; methodology reference for the no-planet RV upper limits.

### Read (instrument-only, not visual-informative)

- **Decin G. et al. 2003** — ISO photometry of Vega cross-calibration; instrument paper.
- **Marsh K. A. et al. 2006** — Submm imaging instrument validation using Vega as photometric standard; no morphology constraint.
- **Absil O. et al. 2006** — CHARA/FLUOR K-band excess detection; ambiguous interpretation between hot exozodiacal dust and instrumental systematic.
- **Defrère D. et al. 2011** — KIN nulling interferometry exozodi upper limit; no detection at the relevant baseline.

### Not read — no arXiv preprint or low-priority (~40 papers)

The full filtered bib is preserved as a future task. Skipped entries include photometric-standard validation papers (Bohlin 2007, 2014, 2020 — Vega-as-photometric-zero-point, methodology only), SETI laser-emission searches (Stone 2005, Tellis 2017 — no cfg-decisive content), and conference abstracts on Vega in the context of WASP/CHARA pipeline development. The five most prominent skipped entries: Bohlin R. C. 2007 STIS spectrophotometric standard re-calibration using Vega (pure photometric methodology); Hinz P. M. et al. 2001 MMT Adaptive Optics imaging attempt (no morphological constraint beyond Spitzer); Greaves J. S. et al. 2014 JCMT POL-2 polarimetry follow-up (instrument-development paper, no new geometry); Defrère D. et al. 2021 LBTI exozodi survey results including Vega (consistent with non-detection); Su K. Y. L. et al. 2005 Spitzer-MIPS first-look paper (superseded by Su 2013).

## Open items for follow-up

- **Disk geometry is multi-belt in `disks_curated.json`** (audited 2026-05-29). Vega's warm + cold belts are separate `belt` entries; the Decisions table renders them as per-belt `disk_<belt>_*` fields → one Kopernicus Ring each. Remaining: a grain-size / Mie color synthesis to replace the tie-break per-belt tints.
- **Age disagreement between Yoon 2010 (0.455 ± 0.013 Gyr) and Monnier 2012 (0.7 ± 0.075 Gyr).** Both papers use rotating-model isochrones but with different boundary conditions; the cfg adopts the Yoon headline. Resolution requires a deeper read of Monnier 2012 §4 and possibly Tetzlaff 2011 kinematic-age cross-check.
- **Hurt 2021 0.6-day candidate at 0.04 AU.** If a 2026+ follow-up confirms this as a real planet (currently unconfirmed; could be stellar activity), a new Decisions entry `circumstellar_planet_present: true` is required and a planet body cfg should be added.
- **Su 2013 gap-clearer planets between 14 and 110 AU.** Currently inferred only from the disk morphology. A future direct-imaging confirmation (JWST-NIRCam or extreme-AO) would convert this from inference to confirmed planet bodies, triggering cfg additions.
- **Conservative-opacity disk variant.** Current cfg uses `disk_opacity` = 0.06 (interesting-first tie-break); the observation-consistent value is τ ~ 10⁻⁴ (essentially invisible). A "realistic" cfg variant with the physically-faithful opacity should be authored as a player-selectable option.
- **Polar magnetic spot from Petit 2010.** Not currently rendered. A future cfg variant could add a faint blue-shifted spot at the pole for the close fly-by view, matching the ZDI structure.
- **Disk dust-size and color synthesis upgrade.** Current `disk_tint_rgb_hex` uses an HST-STIS-Fomalhaut palette convention; a proper synthesis from grain-size distribution + Vega illumination spectrum (Mie scattering) would give a defensible color rather than a tie-break.
- **Cycle phase / epoch synchronization.** Vega has no observed activity cycle (radiative envelope), so unlike α Cen A no epoch synchronization is needed — but if the Petit 2010 magnetic geometry is implemented as a slowly-rotating polar feature, an epoch reference would become necessary.

## Related

- [alpha-centauri-a](alpha-centauri-a.md) — different scenario archetype: a quiet G2V solar analog vs. Vega's young rapid-rotator A0V archetype. Read for the canonical stellar-Phase-3 structural template.
- [methodology](../reference/methodology.md) — schema source for the Decisions table.
- [data-sources](../reference/data-sources.md) — provenance for SIMBAD-derived astrometric + spectral fields in `db/systems/vega.json`.
- [mod-reference](../reference/mod-reference.md) — Kopernicus + Firefly + Scatterer cfg field map; circumstellar-disk fields map to Kopernicus Ring components attached to the star body.
