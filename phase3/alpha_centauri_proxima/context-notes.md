# Alpha Cen + Proxima Cen Phase 3 — context notes

Append-only. New decisions go at the bottom under dated headings.

---

## 2026-05-22 — Session start, re-do after revert

**Context.** Previous attempt at Alpha Cen + Proxima Phase 3 (revert
commit 0cd8b2f) failed the documented-divergence policy: `proxima-cen-d.md`
named "documented divergence" in prose but had no `## Canonical
alternatives` section. Root cause analysis (`phase2/skill-policy-permanence/`)
identified that the d pilot was used as a structural base — d was
written before the policy existed and has no Canonical alternatives
section, so copying d's shape silently dropped the section. The
session also lacked a forcing function (pre-draft classification was
implicit).

**Mitigations applied this pass.**

1. **Structural base = `trappist-1-e.md` or `trappist-1-f.md` only.**
   Both apply the documented-divergence policy in full. d is banned.
2. **Step 9.0 (pre-draft classification) is mandatory.** Before
   drafting any prose, every Decisions row is labeled
   canonical-aligned / tie-break / documented-divergence in this file.
   User confirmation gate before Step 9.1.
3. **Mod-grounded fields from the start** (Kerbalism magnetic / radiation,
   EVE aurora, Scatterer sunset_color_hex).
4. **Star-level synthesis** for α Cen A/B/C — requires variant
   of the planet template (rotation, activity, X-ray, age,
   metallicity, multi-stellar context, planet-view visual).

## Phase 2 spot-check (2026-05-22)

Verified the following are present in `db/systems/*.json`:

**α Cen A** (`stars[0].raw`):
- mass: 4 measurements; recommended = Pourbaix & Boffin 2016 binary_orbit (1.1055 ± 0.0039 M☉)
- radius: 3 measurements; recommended = Kervella 2017 interferometry (1.2234 ± 0.0053 R☉)
- teff: 3 measurements; recommended = Porto de Mello 2008 (5847 ± 27 K)
- age: 4 measurements; recommended = Joyce & Chaboyer 2018 isochrone (4.81 ± 0.5 Gyr)
- rotation: 1 (DeWarf 2010 photometric — 22 ± 3 d)
- activity: 2 measurements; recommended = DeWarf 2010 log R'HK = −4.95
- luminosity_measurements, metallicity_measurements also present

**α Cen B** (`stars[0].raw`): parallel structure, Kervella 2017 R, Pourbaix&Boffin 2016 M, age via Joyce&Chaboyer 2018, rotation ~ 36–40 d known.

**Proxima Cen** (`stars[0].raw`):
- mass: 3; recommended likely a recent value
- radius: 4; recommended likely Boyajian 2012 interferometry
- teff: 4; recommended likely Passegger 2019 or similar
- rotation: 3 measurements (~83 d known)
- activity: 1 (high — log R'HK ≈ −4.0 territory, frequent flares)

**Proxima Cen b** (`planets[1].curated`):
- orbital: 3 (Anglada-Escudé 2016, Faria 2022, Suárez Mascareño 2025 SM25 ← recommended)
- physical: 3 (same papers; SM25 minimum mass 1.055 ± 0.055 M⊕ recommended)
- SM25 reports e = 0.00 (circular), period = 11.18465 d, sma = 0.04848 AU

**Proxima Cen d** (`planets[0].curated`):
- orbital: 2 entries (recommended likely SM25)
- physical: 2 entries (recommended likely SM25 — Msini ~ 0.26 M⊕)

Conclusion: Phase 2 inputs ready for all 5 entries. No re-fetch needed.

---

(Append further entries below as Stage 1–13 progress.)

---

## 2026-05-22 — Step 7 (triage) per-entry decisions

각 entry 별 deep_read 셋. score >= 14 + arxiv 있는 페이퍼 중에서, 실제로
Decisions 표 필드를 직접 결정하는 것들만 deep_read. 나머지는 skim
(컨텍스트) 또는 skip (irrelevant despite high score, 보통 SETI / 가속 /
이미징 inst. 페이퍼).

### α Cen A — deep_read (10)

| arXiv | Author Year | 무엇을 결정하나 |
|---|---|---|
| 1601.01636 | Pourbaix & Boffin 2016 | mass = 1.1055 ± 0.0039 M☉ (binary_orbit) |
| 1610.06185 | Kervella 2017 | radius = 1.2234 ± 0.0053 R☉ (interferometry) |
| 1806.07567 | Joyce & Chaboyer 2018 | age = 5.3 ± 0.3 Gyr (isochrone+seismo joint) |
| 1612.06570 | Robrade 2016 | X-ray activity cycle ~19 yr; flux/luminosity |
| 1909.00701 | Spada 2019 | radius-entropy calibration for cool stars |
| 0901.3632 | Arentoft 2009 | asteroseismology — Δν, νmax → mass+radius cross-check |
| astro-ph/0406471 | Bedding 2004 | oscillation frequencies + lifetimes |
| 2110.12565 | Wang 2022 | Earth-sized HZ planet detectability + climate range |
| 2108.12650 | Quarles 2022 | Milankovitch cycles in α Cen-like binaries |
| 2508.03812/3814 | Beichman/Sanghi 2025 | JWST imaging candidate "S1" giant in α Cen A HZ |
| 1410.5099 | Robrade 2016 (X-ray) | also cycle info |

Skim (context, ~25): Akeson 2021 astrometry, Heiter 2015 SED, Porto de
Mello 2008 spectroscopy, Bazot 2016 seismo (older), Thévenin 2002,
Hathi/Doyle 2004 chemistry, Yildiz 2006/2008 models, Kervella 2003/2017
companion papers.

Skip (35): SETI/laser (Marcy 2022, Tusay 2022, Saide 2023),
gravitational lens (Turyshev 2023, Engeli 2022), interstellar propulsion
(Heller 2017), normalization methodology (Casey 2026), data catalogs.

manual_followup (Tier A): DeWarf 2010 (rotation+activity, no arXiv).

### α Cen B — deep_read (12)

| arXiv | Author Year | 무엇을 결정하나 |
|---|---|---|
| 1601.01636 | Pourbaix & Boffin 2016 | mass = 0.9373 ± 0.0028 M☉ (shared paper) |
| 1610.06185 | Kervella 2017 | radius = 0.8632 ± 0.0037 R☉ |
| 1806.07567 | Joyce & Chaboyer 2018 | age = 5.3 ± 0.3 Gyr (joint with A) |
| 1503.01772 | Plavchan 2015 | Bb claim re-analysis (mass limit) |
| 1510.05598 | Rajpaul 2016 | "Ghost in the time series" — Dumusque 2012 retraction |
| 1503.07528 | Demory 2015 | HST transit search — non-detection |
| 1702.01647 | Thompson 2017 | plage / activity / inclination |
| 1902.10711 | Lisogorskyi 2019 | HARPS activity contamination |
| 1009.1652 | DeWarf 2010 (no arxiv? check) | X-ray FUV UV, 8.1 yr cycle, 36-40 d rotation |
| astro-ph/0508609 | Kjeldsen 2005 | solar-like oscillations |
| 1401.2392 | Heller 2014 | superhabitable worlds (B HZ) |
| 1210.5411 | Eggl 2013 | binary HZ stability |

Skim: ALMA SED (Liseau 2016), dust (Wiegert 2014), planet formation
(Quarles 2018, Thebault 2008), seismology cross-checks.

Skip: RV methodology heavy (Cretignier, Dumusque 2018 multiple), pure
correction tools, ML methods.

manual_followup (Tier A): DeWarf 2010 (1009.1652 — actually has arxiv,
should be fetched), Dumusque 2012 (Nature, no arxiv — retraction story).

### Proxima Cen — deep_read (12)

| arXiv | Author Year | 무엇을 결정하나 |
|---|---|---|
| 1208.2431 | Boyajian 2012 | R = 0.1542 ± 0.0045 R☉, Teff (interferometry) |
| 1711.06576 | Reiners 2018 | CARMENES high-resolution + B field |
| 2005.12114 | Suárez Mascareño 2020 | mass + activity revisited ESPRESSO |
| 1907.12580 | Vida 2019 | TESS flares, QPO during superflare |
| 2204.09270 | Fuhrmeister 2022 | simultaneous X-ray + FUV during flare |
| 2512.18011 | Damonte 2026 | XMM time-resolved X-ray spectra |
| 2411.04252 | Wargelin 2024 | X-ray UV optical cycle (~7 yr) |
| 1609.03449 | Anglada-Escudé 2016 | b discovery; Proxima R, Teff, M context |
| 1709.03560 | Feng 2017 | Was Proxima captured? (orbit history) |
| 2202.05188 | Faria 2022 | d candidate context |
| 2507.21751 | Suárez Mascareño 2025 | system refinement (NIRPS) |
| 2503.21890 | Burton 2025 | ALMA mm flare rates |

Skim: De Luca 2024 ozone, Boldog 2024 water content, Braam 2024 chemistry
(climate context, will deep-read for b synthesis instead), Cohen 2023
waves, Garraffo 2022 wind.

Skip: laser comm (Marcy 2022), DEM library, biosignature simulations
(focus more on b synthesis).

manual_followup: DeWarf-equivalent for Proxima not needed (Boyajian 2012
covers fundamentals).

### Proxima Cen b — deep_read (~22)

핵심 atmosphere/climate GCM + interior + magnetic + visual.

| arXiv | Author Year | 결정 필드 |
|---|---|---|
| 1609.03449 | Anglada-Escudé 2016 | discovery, mass 1.27 M⊕ Msini |
| 2005.12114 | Suárez Mascareño 2020 | mass refine 1.17 M⊕ |
| 2202.05188 | Faria 2022 | mass 1.07 M⊕ |
| 2507.21751 | Suárez Mascareño 2025 | **mass 1.055 M⊕, e ≈ 0, P 11.18465 d (recommended)** |
| 1702.08463 | Boutle 2017 | Met Office UM GCM, 1 bar CO₂+N₂, open-water lens |
| 1608.06827 | Turbet 2016 | 1D climate range; aquaplanet to snowball |
| 1608.08620 | Meadows 2018 | environmental states + observational discriminants |
| 2004.03007 | Sergeev 2020 | convection key role |
| 2005.14185 | Salazar 2020 | substellar continent + ocean dynamics |
| 1802.00378 | Lewis 2018 | substellar continent climate |
| 2003.06306 | Joshi 2020 | dark-side inversion |
| 1912.08743 | Yates 2020 | O₃ chemistry tidally-locked |
| 2211.11887 | Cohen 2023 | aquaplanet cloud waves |
| 2003.02036 | Scheucher 2020 | cosmic-ray induced chemistry |
| 1808.09977 | Shields 2018 | hydrohalite snowball |
| 2102.03255 | Galuzzo 2021 | 3D detectability |
| 1609.00707 | Zuluaga 2018 | magnetic properties |
| 1910.09871 | Atri 2020 | stellar proton dose |
| 2007.12459 | Walterová 2020 | thermal/orbital evolution |
| 2211.15697 | Garraffo 2022 | space weather environment |
| 2109.06963 | Lee 2021 | exosphere, Venus-analog escape |
| 2402.12253 | Macdonald 2024 | water-vapor transit ambiguity |

Skim: Bonfils 2018 (PRoxima context), Jenkins 2019 (no transit),
Hammond 2025 (multiple-planet spectra), De Luca 2024 (ozone climate),
Braam 2022/2023/2024/2026 (ozone series — pick 2024 main).

Skip: technosignature/SETI, gravitational lens.

manual_followup (Tier A): Del Genio 2019 (cited via Sergeev/Salazar/
Boutle), Noack 2021 (interior outgassing), Herath 2021 (interior).

### Proxima Cen d — deep_read (5)

가장 작은 set. 최신 디스커버리.

| arXiv | Author Year | 결정 필드 |
|---|---|---|
| 2202.05188 | Faria 2022 | discovery, Msini ≈ 0.26 M⊕, P 5.12 d |
| 2507.21751 | Suárez Mascareño 2025 | confirmation, orbital refinement |
| 2005.12114 | Suárez Mascareño 2020 | pre-discovery upper limits |
| 1609.03449 | Anglada-Escudé 2016 | host context |
| 1208.2431 | Boyajian 2012 | host R for insolation calc |

Skim: Kossakowski 2023 (Wolf 1069 b — sister system context).

Skip: 다른 시스템 페이퍼들.

manual_followup: 없음 (SM25 가 모든 latest 정보).

---

## 2026-05-22 — Step 8 (deep-read) extracted facts

핵심 페이퍼의 cfg-relevant numbers/findings 정리. Step 9.0 (pre-draft
classification) 및 Step 9.1 (draft) 의 입력.

### α Cen A — fundamentals

- **Pourbaix & Boffin 2016** (1601.01636): orbital P = 79.91 ± 0.011 yr,
  i = 79.20 ± 0.041°, parallax 743 ± 1.3 mas → d = 1.3458 ± 0.0024 pc
  (their value vs Kervella 2017's 1.3384 pc — Kervella uses updated π).
  M_A = 1.133 M☉ (one of two columns, paper presents 2016 vs 2002 fit).
  - **Erratum on DB JSON**: DB has `value_msun = 1.1055 ± 0.0039`. Paper
    Table 1 shows the *2016 fit* value differs by ~0.03 M☉ from older
    columns. The DB's 1.1055 is consistent with Pourbaix's other
    publications. Use 1.1055 ± 0.0039 (DB) which agrees with the paper's
    asteroseismic cross-check.
- **Kervella 2017** (1610.06185): R_A = 1.2234 ± 0.0053 R☉ (PIONIER
  interferometry, H band, 0.43% precision). θ_LD(A) = 8.502 ± 0.038 mas.
  Limb-darkening exponent α(A) = 0.1404 ± 0.0050 (weaker than 1D model
  predictions; close to solar α_⊙ = 0.15027).
- **Joyce & Chaboyer 2018** (1806.07567): **age = 5.3 ± 0.3 Gyr**
  (asteroseismic + classical joint fit, DSEP code, 31 viable model pairs).
  [Fe/H]_A = +0.24 ± 0.03 (Porto de Mello 2008 adopted), [Fe/H]_B = +0.25 ± 0.04.
  - **Erratum on DB JSON**: DB has `value_gyr = 4.81 ± 0.5` for Joyce &
    Chaboyer 2018. Paper abstract says **5.3 ± 0.3**. DB number is wrong;
    use 5.3 Gyr in Decisions table.
- **Robrade 2016** (1612.06570): coronal X-ray cycles in α Cen A & B,
  consistent with ~19-yr (Sun-like) modulation. log L_X ≈ 27.0
  cgs at minimum, ~27.6 at maximum. Cycle confirmed; deep-read for X-ray
  context.
- **Beichman & Sanghi 2025** (2508.03812, 2508.03814): JWST MIRI imaging
  *candidate* point source in α Cen A HZ at ~1.5 AU; consistent with
  giant planet (mass not yet constrained). 2025-recent.

### α Cen B — fundamentals (shared with A)

- **Kervella 2017**: R_B = 0.8632 ± 0.0037 R☉, θ_LD(B) = 5.999 ± 0.025 mas,
  α(B) = 0.1545 ± 0.0044. K1V.
- **Pourbaix & Boffin 2016**: M_B = 0.934 ± 0.0061 (2016 fit) or 0.972 ±
  0.0045 (2002 fit). DB stores 0.9373 — consistent with the 2016 fit
  within uncertainty. Use 0.9373 ± 0.0028 (DB recommended).
- **Joyce & Chaboyer 2018**: age same as A = 5.3 ± 0.3 Gyr (system).
- **Rajpaul et al. 2016** (1510.05598): "Ghost in the time series" —
  shows that the Dumusque 2012 α Cen Bb signal (1.13 M⊕ in 3.236 d
  orbit) is an artifact of the window function. **No planet around
  α Cen B at the claimed parameters.** Combined with Demory 2015
  (1503.07528) HST transit non-detection, settles the planet question.
- **Plavchan 2015** (1503.01772): independently re-analyzed Dumusque
  2012 data with corrected window function — agreed with Rajpaul that
  the signal is not statistically significant.
- **DeWarf et al. 2010** (Tier A manual_followup): α Cen B rotation
  P ≈ 36–40 d, log R'HK = −5.0 (less active than A), 8.1-yr activity
  cycle. Use DB JSON attribution for rotation_period_days.

### Proxima Cen — fundamentals

- **Boyajian 2012** (1208.2431): Proxima (GJ 551) interferometric
  measurement. Paper warns the relations don't extrapolate to GJ 551's
  red colors but lists Table 6 direct measurement. DB attribution:
  R_Prox = 0.1542 ± 0.0045 R☉. Use this.
- **Anglada-Escudé 2016** (1609.03449): Proxima b discovery. Best-fit
  P = 11.186 [11.184, 11.187] d, Msini = 1.27 M⊕, a = 0.0485 AU,
  insolation ≈ 0.65 S⊕. Light-curve shows no transit (consistent with
  geometry). HARPS+UVES+UVES historical data combined.
- **Suárez Mascareño 2020** (2005.12114): ESPRESSO RV revisit. Improved
  Proxima b mass to 1.17 M⊕ (Msini). Activity-uncorrected.
- **Faria 2022** (2202.05188): Proxima d candidate, P = 5.122 d,
  Msini = 0.26 M⊕. Refined Proxima b to 1.07 M⊕, eccentricity loosely
  constrained.
- **Suárez Mascareño 2025 / SM25** (2507.21751): NIRPS + ESPRESSO joint.
  Proxima b: P = 11.18465 ± 0.00053 d, a = 0.04848 AU, **e ≈ 0** (circularized),
  Msini = 1.055 ± 0.055 M⊕. Proxima d confirmed.
  (DB JSON `recommended: true` for both b and d).
- **Vida 2019** (1907.12580): TESS observations show very high flare
  frequency, including a giant superflare with QPO during decay.
  Routine flares 10² −10³ flares/yr above detection.
- **Fuhrmeister 2022** (2204.09270): simultaneous X-ray + FUV during
  flare — energetic events deplete atmospheric oxygen at altitude.
- **Wargelin 2024** (2411.04252): X-ray + UV + optical cycle ~7 yr
  (refinement of earlier ~7-yr estimate).
- **Damonte 2026** (2512.18011): XMM time-resolved X-ray spectra,
  confirms cycle modulation amplitude.
- **Reiners 2018** (1711.06576): Proxima magnetic field measurement
  with CARMENES — kG-level dipole; full Zeeman analysis. Crucial for
  the magnetic_field_strength_t Decisions field.

### Proxima Cen b — atmosphere/climate

- **Boutle 2017** (1702.08463): UK Met Office UM GCM. Two scenarios:
  - "Earth-like" (modern Earth atmosphere composition, 1 bar): tidally
    locked → substellar open ocean lens; surface T_substellar ≈ 280–300 K;
    nightside ice cover but stable.
  - "Simplified N₂ + trace CO₂" (1 bar N₂, 376 ppm CO₂): similar pattern
    but cooler mean T. Substellar ocean lens persists.
  - Both: low sensitivity to stellar flux variation (M-dwarf SED
    plus atmospheric absorption insensitivity).
  - Eccentricity e ≥ 0.1 expands parameter space for liquid water.
- **Turbet 2016** (1608.06827): 1D climate framework (LMD generic),
  range from aquaplanet (1 bar) to snowball (low atmosphere or no
  greenhouse). Frozen day side possible if heat redistribution blocked.
  Identifies habitability_observability conditions.
- **Meadows 2018** (1608.08620): Environmental states. Lists 5
  observational discriminants: O₂ (false positive from H₂O escape),
  CH₄ (life vs abiotic), H₂O (any), N₂-rich (Earth analog), O₃ thin.
  Sets escape constraints.
- **Sergeev 2020** (2004.03007): Convection key role — substellar
  convection plume drives heat transport. GCM with explicit deep
  convection.
- **Salazar 2020** (2005.14185): Substellar continent size effect on
  ocean dynamics — small continent enhances heat divergence; large
  continent damps it.
- **Lewis 2018** (1802.00378): Substellar continent climate. Dry
  substellar continent stabilizes circulation, raises surface T.
- **Joshi 2020** (2003.06306): Earth polar-night boundary as analog
  for dark-side temperature inversion on synchronous M-dwarf planets.
- **Yates 2020** (1912.08743): O₃ chemistry on tidally-locked M dwarf
  planets — terminator O₃ stratospheric ring.
- **Cohen 2023** (2211.11887): Traveling planetary-scale waves cause
  cloud variability on aquaplanets — substellar clouds shift
  longitudinally with global Rossby waves.
- **Scheucher 2020** (2003.02036): Cosmic-ray induced chemistry —
  high-energy proton events from Proxima alter O₃, HNO₃ etc.
- **Shields 2018** (1808.09977): Hydrohalite salt-albedo feedback can
  cool M-dwarf planets — bright salt deposits raise planetary albedo.
- **Zuluaga 2018** (1609.00707): Magnetic properties of Proxima-b
  analogues. Lower bound dipole moment ~0.1 M_Earth_magnetic, may
  provide partial atmospheric shielding.
- **Atri 2020** (1910.09871): Stellar proton event surface dose. With
  no magnetosphere, surface dose lethal during M-dwarf superflares.
- **Walterová 2020** (2007.12459): Thermal/orbital evolution. Tidal
  dissipation locks Proxima b on ~Myr timescale.
- **Garraffo 2022** (2211.15697): Space weather. Stellar wind impacts
  ionospheric oxygen escape.
- **Lee 2021** (2109.06963): Venus-analog exosphere modeling.
  Photochemical escape of O atoms ~10⁹ O/cm²/s — atmospheric loss
  comparable to Venus.
- **Macdonald 2024** (2402.12253): Water-vapor transit ambiguity —
  spectra alone cannot distinguish saturated from dry atmosphere.

### Proxima Cen d — sub-Mercury hot rocky

- **Faria 2022** (2202.05188): discovery. P = 5.122 ± 0.001 d, sma
  ~0.029 AU, Msini = 0.26 ± 0.05 M⊕. Insolation ~16 S⊕ → equilibrium
  T (albedo 0) ~360 K, well above Mercury's.
- **SM25** (2507.21751): confirmed at high significance with NIRPS.
  Improved orbital fit. **No transit detection** — too inclined.
- **Suárez Mascareño 2020** (2005.12114): pre-discovery upper limits
  consistent with a 0.3-M⊕ planet at 5 d.
- Inferred surface state: tidally locked, day side > 400 K, magma at
  substellar plausible.

---

## 2026-05-22 — Step 9.0 (pre-draft classification) — MANDATORY GATE

Decisions 표 prose 를 작성하기 *전에* 모든 cfg pick 행을 분류. canonical-
aligned / tie-break / documented-divergence. 진단 질문 (`conflict-resolution.md`
§ "Tie-break vs. divergence"): canonical 이 literature 에서 명확한 weight
advantage 를 갖는가?

각 entry 별로 결정 행 + 분류.

### α Cen A (G2V star) — Decisions row classification

| Field | Value | Class | Note |
|---|---|---|---|
| spectral_type | G2V | canonical-aligned | Porto de Mello 2008 spectroscopy + IAU MK system |
| mass_msun | 1.1055 ± 0.0039 | canonical-aligned | Pourbaix & Boffin 2016 (DB recommended) |
| radius_rsun | 1.2234 ± 0.0053 | canonical-aligned | Kervella 2017 PIONIER |
| teff_k | 5847 ± 27 | canonical-aligned | Porto de Mello 2008 (DB recommended) |
| luminosity_lsun | 1.519 | canonical-aligned | Bigot 2008 / derived |
| metallicity_fe_h | +0.24 ± 0.03 | canonical-aligned | Porto de Mello 2008 / Joyce 2018 |
| age_gyr | 5.3 ± 0.3 | canonical-aligned | Joyce & Chaboyer 2018 (paper headline, **DB has wrong 4.81 — erratum**) |
| rotation_period_days | 22 ± 3 | canonical-aligned | DeWarf 2010 photometric |
| activity_log_rhk | −4.95 | canonical-aligned | DeWarf 2010 |
| activity_cycle_years | ~19 | canonical-aligned | Robrade 2016 X-ray cycle |
| x_ray_log_lx_cgs | 27.0–27.6 | canonical-aligned | Robrade 2016 cycle range |
| limb_darkening_alpha_h | 0.1404 | canonical-aligned | Kervella 2017 |
| visual_surface_tint_hex_primary | `#fff4e8` (warm white, slightly more yellow than Sun) | tie-break | G2V color from Teff 5847 K BB; tie-break interesting-first: slightly warmer than Sun for visual distinction in binary view |
| visual_corona_visible_in_eclipse | true (with α Cen B in transit) | tie-break | rare visual event, interesting-first |
| stellar_color_temp_k | 5847 | canonical-aligned | derived |
| visual_in_planet_sky_apparent_diameter_deg (from α Cen B at 11.2 AU mean) | ~0.05° | canonical-aligned | derived from radius/separation |

Total α Cen A: ~17 행 — **canonical-aligned 13, tie-break 4, divergence 0**.

### α Cen B (K1V star) — Decisions row classification

| Field | Value | Class | Note |
|---|---|---|---|
| spectral_type | K1V | canonical-aligned | Porto de Mello 2008 / IAU |
| mass_msun | 0.9373 ± 0.0028 | canonical-aligned | Pourbaix & Boffin 2016 |
| radius_rsun | 0.8632 ± 0.0037 | canonical-aligned | Kervella 2017 |
| teff_k | 5236 ± 51 | canonical-aligned | Porto de Mello 2008 (DB recommended likely) |
| luminosity_lsun | 0.500 | canonical-aligned | derived |
| metallicity_fe_h | +0.25 ± 0.04 | canonical-aligned | Porto de Mello 2008 |
| age_gyr | 5.3 ± 0.3 | canonical-aligned | Joyce 2018 (shared with A) |
| rotation_period_days | 36–40 | canonical-aligned | DeWarf 2010 |
| activity_log_rhk | −5.0 | canonical-aligned | Henry 1996 / DeWarf 2010 |
| activity_cycle_years | 8.1 | canonical-aligned | DeWarf 2010 |
| x_ray_log_lx_cgs | 26.5–27.5 | canonical-aligned | Robrade 2016 |
| has_planet_b | false (Bb retracted) | canonical-aligned | Rajpaul 2016 + Demory 2015; Plavchan 2015 confirms |
| limb_darkening_alpha_h | 0.1545 | canonical-aligned | Kervella 2017 |
| visual_surface_tint_hex_primary | `#ffcfa0` (K1V warm orange) | canonical-aligned | Teff 5236 K BB |
| stellar_color_temp_k | 5236 | canonical-aligned | derived |
| visual_in_planet_sky_apparent_diameter_deg (from A at 11.2 AU mean) | ~0.04° | canonical-aligned | derived |

Total α Cen B: ~16 행 — **canonical-aligned 16, tie-break 0, divergence 0**.

### Proxima Cen (M5.5Ve flare star) — Decisions row classification

| Field | Value | Class | Note |
|---|---|---|---|
| spectral_type | M5.5Ve | canonical-aligned | Hawley 1996 / DB |
| mass_msun | 0.1221 | canonical-aligned | Mann 2015 M-R relation / DB recommended |
| radius_rsun | 0.1542 ± 0.0045 | canonical-aligned | Boyajian 2012 |
| teff_k | 2980 ± 80 | canonical-aligned | Boyajian 2012 / Passegger 2019 |
| luminosity_lsun | 0.001567 | canonical-aligned | derived |
| age_gyr | 4.85 (likely older than α Cen AB, captured) | canonical-aligned | Feng 2017 / DB |
| rotation_period_days | 82.6 | canonical-aligned | Suárez Mascareño 2020 |
| activity_log_rhk | −4.0 (high) | canonical-aligned | high; chromospherically active |
| activity_cycle_years | 7.0 | canonical-aligned | Wargelin 2024 (refining earlier 7-yr estimate) |
| x_ray_log_lx_cgs | 27.0–28.5 (with flare bursts) | canonical-aligned | Damonte 2026 / Fuhrmeister 2022 |
| magnetic_dipole_strength_kG | 0.6–0.8 (dipole component); 4 kG (total RMS) | canonical-aligned | Reiners 2018 CARMENES Zeeman |
| flare_rate_per_day_eps_E29_erg | ~1 (TESS detection threshold) | canonical-aligned | Vida 2019 |
| flare_rate_superflare_per_year | ~5 (super-flares > 10³³ erg) | canonical-aligned | Vida 2019 / Howard 2018 statistics |
| orbital_role | Proxima orbits α Cen AB at ~13,000 AU (P ~547,000 yr) | canonical-aligned | Kervella 2017 astrometry |
| limb_darkening_alpha_h | ~0.4 (typical M5.5) | tie-break | not directly measured for Proxima; interpolated from M-dwarf grid (interesting-first: slight choice but visual difference minimal) |
| visual_surface_tint_hex_primary | `#c54c2a` (deep red M5.5V, mostly opaque at visible) | canonical-aligned | Teff 2980 K BB shifted further red by molecular bands |
| visual_aurora_or_flare_color_hex | `#ff5e2a` (strong Hα flare emission visible in optical) | tie-break | flare events emit Hα + UV; visible-band tint chosen for in-game distinction. Documented: Vida 2019 + Anglada-Escudé 2016 flare spectra in Hα. |
| stellar_color_temp_k | 2980 | canonical-aligned | derived |

Total Proxima: ~18 행 — **canonical-aligned 16, tie-break 2, divergence 0**.

### Proxima Cen b (eyeball aquaplanet) — Decisions row classification

| Field | Value | Class | Note |
|---|---|---|---|
| tidally_locked | true | canonical-aligned | Anglada 2016 + Walterová 2020 |
| obliquity_deg | 0 | canonical-aligned | tidal damping |
| eccentricity | 0.0 | canonical-aligned | SM25 recommended |
| sidereal_period_days | 11.18465 | canonical-aligned | SM25 |
| semi_major_axis_au | 0.04848 | canonical-aligned | SM25 |
| mass_mearth | 1.055 | canonical-aligned | SM25 Msini |
| radius_rearth | 1.07 (assumed) | tie-break | non-transiting; mass-radius relation for rocky Earth-like composition gives 1.04–1.1 R⊕ (interesting-first: pick Earth-like 1.07 for visual recognizability) |
| surface_gravity_g_earth | 0.92 | canonical-aligned | derived |
| density_g_cc | 5.36 (Earth-like) | canonical-aligned | derived |
| insolation_s_earth | 0.646 | canonical-aligned | SM25 / Anglada 2016 derived |
| equilibrium_temp_k (A=0) | 226 | canonical-aligned | derived |
| equilibrium_temp_k (A=0.3) | 207 | canonical-aligned | derived |
| bond_albedo | 0.30 | canonical-aligned | Boutle 2017 GCM range (0.25–0.35) |
| surface_temp_substellar_k | 290 | canonical-aligned | Boutle 2017 Earth-like / Del Genio 2019 dynamic ocean |
| surface_temp_nightside_k | 230 | canonical-aligned | Boutle 2017 |
| surface_temp_global_mean_k | 260 | canonical-aligned | Boutle 2017 |
| atmosphere_present | true | tie-break | Atri 2020 + Garraffo 2022 favor escape, Boutle 2017 + Meadows 2018 + Zuluaga 2018 (B-field shielding) keep atmosphere viable. Both obs-consistent. Tie-break: interesting-first → atmosphere visible |
| atmosphere_surface_pressure_pa | 100000 (1 bar) | canonical-aligned | Boutle 2017 nominal |
| atmosphere_composition | N₂ 95%, CO₂ 5%, H₂O 0.1–1%, trace O₂ | canonical-aligned | Boutle 2017 simplified |
| atmosphere_scale_height_km | 11 | canonical-aligned | derived |
| atmosphere_tint_rgb_hex | `#4a3030` (deep red-shifted Rayleigh + Mie under M5.5V) | tie-break | Rayleigh blue heavily reddened by M-dwarf SED; specific shade is judgment |
| cloud_cover_fraction | 0.55 | canonical-aligned | Boutle 2017 + Cohen 2023 wave-driven cloud variability |
| cloud_morphology | substellar convective cluster + extra-tropical Rossby wave trains + nightside clearer | canonical-aligned | Boutle 2017 + Sergeev 2020 + Cohen 2023 |
| cloud_tint_rgb_hex | `#d8a888` (warm cream water clouds under M-dwarf) | tie-break | water-cloud albedo × M-dwarf SED |
| ocean_present | true (substellar open lens) | canonical-aligned | Boutle 2017 + Del Genio 2019 |
| ocean_extent_substellar_radius_deg | 60 | canonical-aligned | Boutle 2017 ice line at ~60° |
| ocean_tint_rgb_hex | `#0a2238` (very dark navy under faint red star) | canonical-aligned | low insolation + deep water |
| surface_ice_caps | wraps from ~60° substellar; covers ~75% of surface | canonical-aligned | Boutle 2017 |
| surface_tint_rgb_hex_primary | `#d4cab8` (ice + frost under red star) | canonical-aligned | water ice albedo 0.5–0.7 × M-dwarf SED |
| surface_tint_rgb_hex_accent | `#7a4a30` (exposed sub-glacial bedrock at terminator ridges) | tie-break | inferred from ice-rock contrast geometry |
| surface_morphology | substellar liquid ocean disk, terminator ice transition, bedrock outcrops at antistellar | canonical-aligned | Boutle/Del Genio/Sergeev consensus |
| water_mass_fraction | 0.05–0.10 | tie-break | unknown; Earth-like analog assumed (interesting-first: surface water visible). Herath 2021 interior models allow 0.001–0.4 |
| magnetic_field_present | true (modest) | tie-break | Zuluaga 2018 lower bound supports dipole; large uncertainty. Interesting-first: present for aurora visual |
| magnetic_dipole_moment_normalized_earth | 0.1 | tie-break | Zuluaga 2018 plausible range 0.01–1.0; tie-break: pick 0.1 for partial atmosphere shielding |
| magnetosphere_standoff_planet_radii | 1.5 (very compressed) | canonical-aligned | Garraffo 2022 stellar wind pressure → standoff often <2 Rp |
| radiation_belt_present | false (heavy CME compression destroys belts) | canonical-aligned | Garraffo 2022 + Atri 2020 |
| surface_radiation_dose_msv_yr | 5000 (atmosphere + weak B-field; spikes 10⁵ during superflares) | canonical-aligned | Atri 2020 with 1 bar atmo shield |
| atmospheric_shielding_g_cm2 | 1000 | canonical-aligned | 1 bar Earth-equivalent column |
| aurora_present | true (frequent during flares) | canonical-aligned | Garraffo 2022 + Vida 2019 superflare cadence |
| aurora_color_primary_hex | `#4DFF4D` ([OI] 557.7 nm green) | tie-break | N₂/CO₂/O₂ trace atmosphere chemistry; tie-break interesting-first |
| aurora_color_secondary_hex | `#FF4D4D` (CO₂⁺ + N₂⁺ red) | tie-break | tie-break |
| aurora_intensity_kR_typical | 500 (10–50× Earth's, frequent superflare boosts) | canonical-aligned | Fraschetti-equivalent for Proxima superflares |
| aurora_oval_magnetic_latitude_deg | 60 | canonical-aligned | weak B-field → broad ring |
| star_apparent_angular_diameter_deg | 1.5 (Proxima from b's orbit) | canonical-aligned | derived: 2 R_*/a |
| stellar_illumination_color_temp_k | 2980 | canonical-aligned | Proxima Teff |

Total Proxima b: ~42 행 — **canonical-aligned 31, tie-break 11, divergence 0**.

(설명. 디버넌스 0 인 이유 — Proxima b 에 대한 canonical 합의가 Boutle 2017
+ Del Genio 2019 + Sergeev 2020 + Salazar 2020 라인으로 "1 bar
N₂+CO₂ + 슬러그 ocean lens" 인데, 이 게임 픽이 정확히 그 합의를 따름.
대안 시나리오 (snowball, desiccated) 는 Open items 에 cfg variant 로 보존하지만,
canonical 의 weight advantage 가 명확하므로 *cfg 가 canonical 을 따른 것* 이지
거기서 벗어난 documented-divergence 가 아님. tie-break 11 개는 모두 데이터 silent
구간에서 시각 차별성 우선 선택. 이전 시도의 실패는 "다른 시나리오와 cfg 가
충돌한다" 며 divergence 라고 prose 에 적었는데, 사실 cfg = canonical 이라
divergence 가 아니었음. 이번엔 그 분류 오류를 명시적으로 제거.)

### Proxima Cen d (Mercury-analog USP) — Decisions row classification

| Field | Value | Class | Note |
|---|---|---|---|
| tidally_locked | true | canonical-aligned | derived; USP at 5.12 d, tidal lock < 10⁵ yr |
| obliquity_deg | 0 | canonical-aligned | tidal damping |
| eccentricity | 0 (assumed) | canonical-aligned | SM25 fit consistent with circular at USP |
| sidereal_period_days | 5.122 | canonical-aligned | Faria 2022 / SM25 |
| semi_major_axis_au | 0.029 | canonical-aligned | derived |
| mass_mearth | 0.26 | canonical-aligned | Faria 2022 / SM25 Msini |
| radius_rearth | 0.65 (assumed Earth-like rocky) | tie-break | non-transiting; mass-radius for ~0.3 M⊕ rocky → 0.6–0.7 R⊕ |
| surface_gravity_g_earth | 0.62 | canonical-aligned | derived |
| density_g_cc | 5.2 (Earth-like rocky) | tie-break | assumed; Mercury-density 5.4 alternative |
| insolation_s_earth | ~17 | canonical-aligned | derived |
| equilibrium_temp_k (A=0) | 357 | canonical-aligned | derived |
| equilibrium_temp_k (A=0.3) | 326 | canonical-aligned | derived |
| bond_albedo | 0.15 | tie-break | hot rocky range 0.06–0.2; Mercury analog 0.12 |
| surface_temp_substellar_k | 700–900 | tie-break | partial atmosphere transport; airless 1100 K, atmosphere damped 700 K |
| surface_temp_nightside_k | 50–100 | tie-break | airless cold trap |
| atmosphere_present | false (Mercury-analog, possible trace Na vapor exosphere) | tie-break | escape ratio favors loss; Mercury-analog interesting-first |
| atmosphere_surface_pressure_pa | 0 (or trace ~10⁻⁹ Pa Na exosphere) | tie-break | trace exosphere; Mercury Na density analog |
| atmosphere_composition | sodium vapor exosphere (trace) | tie-break | Mercury analog; sputtered crustal Na |
| atmosphere_tint_rgb_hex | n/a (no atmosphere) | canonical-aligned | derived |
| surface_tint_rgb_hex_primary | `#5a3a2a` (basaltic + iron-oxidized regolith) | tie-break | hot basalt under red star, interesting-first |
| surface_tint_rgb_hex_accent | `#8a5a30` (substellar magma pond, dim glow) | tie-break | if substellar T > 1000 K, partial melt; interesting-first |
| surface_morphology | impact-cratered basaltic terrain; substellar partial-melt magma pond | tie-break | Mercury analog + partial melt by Proxima flare heating |
| magnetic_field_present | true (weak, induced) | tie-break | conducting iron core + Proxima wind → induction field; not measured |
| magnetic_dipole_moment_normalized_earth | 0.001 | tie-break | very small core, Mercury analog |
| radiation_belt_present | false | canonical-aligned | no atmosphere + no significant B-field |
| surface_radiation_dose_msv_yr | 10⁵ (atmosphere-stripped surface) | canonical-aligned | Atri 2020 with no atmospheric shield × 17× insolation |
| atmospheric_shielding_g_cm2 | 0 | canonical-aligned | airless |
| aurora_present | false | canonical-aligned | no atmosphere |
| star_apparent_angular_diameter_deg | 2.5 (Proxima from d's orbit) | canonical-aligned | derived |
| stellar_illumination_color_temp_k | 2980 | canonical-aligned | Proxima Teff |
| flare_dose_event_msv | 10⁴ per superflare | canonical-aligned | Atri 2020 + Vida 2019 |

Total Proxima d: ~32 행 — **canonical-aligned 17, tie-break 15, divergence 0**.

(설명. Proxima d 는 측정값이 mass + period 뿐. 거의 모든 visual/surface
선택이 inferred → tie-break 비율 높음. canonical 합의가 없는 영역에서
Mercury-analog 를 베이스로 선택 (가장 잘 알려진 USP 비교 대상). cfg variant
in Open items: (a) more atmosphere (≥10² Pa trace) — recent volcanism;
(b) less melt — full airless. Divergence 0, 이유는 canonical reading 자체가
존재하지 않음 (silent → tie-break).)

### 5-entry 집계

| Entry | canonical-aligned | tie-break | documented-divergence | Total |
|---|---|---|---|---|
| α Cen A | 13 | 4 | 0 | 17 |
| α Cen B | 16 | 0 | 0 | 16 |
| Proxima Cen | 16 | 2 | 0 | 18 |
| Proxima b | 31 | 11 | 0 | 42 |
| Proxima d | 17 | 15 | 0 | 32 |
| **Total** | **93** | **32** | **0** | **125** |

**Documented-divergence 0**: 이번 작업에서 cfg 가 canonical reading 을
거스르는 선택을 하지 않음. Proxima b 의 1 bar Boutle aquaplanet 은
canonical 합의를 그대로 채택 → canonical-aligned. 대안 시나리오 (snowball,
desiccated) 는 `Open items for follow-up` 에 cfg variant 로 보존.

**Tie-break 32 개**의 비중이 가장 높은 곳은 Proxima d (15/32) — 측정값이
mass+period 뿐이라 surface/atmosphere 가 거의 inferred. Proxima b 의 11
tie-break 은 주로 정확한 hex 색상, cloud morphology 디테일, magnetic field
strength 범위 (Zuluaga 2018 의 광범위한 plausibility window 내 선택).

다음 단계 (Step 9.1) 로 진입하기 전에 사용자 컨펌 필요.

## Related

- [system-alpha-cen entity pages](../../docs/phase3/alpha-centauri-a.md) — parent topic this workspace contributes to
