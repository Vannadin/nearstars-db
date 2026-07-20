# 40 Eridani — Phase 3 Context Notes

Append-only decision log. 2026-05-29.

## System overview

- Triple: A (K0.5 V, V=4.43) + B (DA2.9 WD, V=9.53) + C (M4.5 Ve, V=11.17 flare star DY Eri)
- Distance: 5.01 pc (Gaia DR3 + Hipparcos van Leeuwen 2007)
- BC pair: 230.29 yr orbit (Mason, Hartkopf & Miles 2017 `2017AJ....154..200M`, e=0.4294, a=6.93")
- A-BC: ~83" separation, ~8000 yr outer orbit (Tokovinin MSC 2018, unfitted)
- Planet: HD 26965 b ("Vulcan", Ma 2018) refuted (Burrows 2024 `2024AJ....167..243B` — 42 d signal is stellar rotation/activity, multi-instrument 16-yr RV)
- Disk: none known
- System age: ~1.8 Gyr total (Bond 2017 §6.2 IFMR-derived; cooling age 122 Myr for B)

## Per-component handoff to agents

### Agent A — 40 Eri A (K0.5 V) — needs Phase 2 first

Phase 2 missing in DB. Tier 1-style workflow needed before Phase 3.

Known starting paper-actual values from 2026-05-27 prep notes (UNVERIFIED — agent must re-confirm at paper-body level):

| Property | 2026-05-27 candidate | Reference | Verify? |
|---|---|---|---|
| Mass | 0.78 ± 0.08 Msun | Ma 2018 `2018MNRAS.480.2411M` (evolutionary_model) | Re-fetch Ma 2018; this is the refuted planet paper |
| Radius | 0.804 ± 0.006 Rsun | Rains 2020 `2020MNRAS.493.2377R` (interferometry VLTI/PIONIER) | Verify 40 Eri A is in Rains 2020 sample — Rains 2020 is 16 *southern* stars, 40 Eri A dec is -7° |
| Teff | 5126 ± 30 K | Rains 2020 (interferometric θ_LD + F_bol) | Same — verify presence in sample |
| Luminosity | 0.400 ± 0.010 Lsun | Rains 2020 (bolometric_flux) | Same |
| Age | 6.9 ± 4.7 Gyr | Ma 2018 (isochrone Y-Y) | Verify; system-coeval ~1.8 Gyr from B WD conflicts strongly — this is one of the key Phase 3 decisions |
| [Fe/H] | -0.29 ± 0.12 dex | Diaz 2018 `2018AJ....155..126D` (SPECIES high-res) | Verify |
| P_rot | 42.0 ± 2.5 d | Burrows 2024 `2024AJ....167..243B` (photometric + activity, multi-instrument) | Verify in paper Table |
| log R'HK | -4.99 | Jenkins 2011 `2011A&A...531A...8J` (log_rhk) | Verify |

Critical cross-checks:
1. **Rains 2020 sample membership**: paper is "16 southern stars VLTI/PIONIER" — 40 Eri A dec -7°39' is *just barely* southern. Verify by fetching Table 1 of Rains 2020.
2. **Age inconsistency**: Ma 2018 isochrone 6.9 Gyr vs Bond 2017 system-coeval 1.8 Gyr from WD progenitor IFMR. This is a documented divergence — Phase 3 narrative must address.
3. **Burrows 2024 P_rot vs activity**: same paper that refuted the Vulcan planet derives P_rot from the spurious signal — extract carefully.
4. **Other interferometric candidates**: Boyajian et al. 2012 CHARA `2012ApJ...757..112B` — verify if 40 Eri A is in that sample (Northern hemisphere CHARA so likely yes).

After Phase 2 done, agent A continues to Phase 3 synthesis (Decisions table + Surface/Atmosphere/Rotation/Visual sections, stellar template `docs/phase3/alpha-centauri-a.md`).

### Agent B — 40 Eri B (DA2.9 WD)

Phase 2 ✅ already done (Bond 2017 paper-verified, all values + meta_notes recorded).
Agent B drafts `docs/phase3/40-eridani-b.md` directly.

Stellar-Phase 3 specific fields for a WD:
- No surface tint / habitable zone / atmosphere sections (radiative DA atmosphere, no convective envelope, no chromospheric activity)
- Cooling sequence: Bond 2017 `2017ApJ...848...16B` cooling age 122 Myr (thin H layer q_H ≈ 10⁻¹⁰)
- Total age: Bond 2017 IFMR-derived ~1.8 Gyr (progenitor M_initial ~1.8 Msun, pre-WD lifetime 1.7 Gyr)
- Magnetic field: Landstreet & Bagnulo 2015 `2015A&A...580A.120L` upper limit <250 G
- Spectral evolution: Bond 2017 §6 — currently DA, will mix into DC at lower Teff in distant future
- Mass-radius: anchor for white-dwarf MRR (CO core thin H envelope) per Bond 2017 §6.3
- Companion: paired with A at 83" (no binary_orbit cfg entry, A-BC unresolved) + with C at ~33 AU mean orbital separation (BC orbit Mason 2017)

Visual styling: WD in KSP — Sirius B-style very small bright blue-white point. Phase 3 cfg-ready decisions for the Kopernicus-side body include log_g, M-R curve point, IFMR-derived total age, magnetic field upper limit.

### Agent C — 40 Eri C (M4.5 Ve, flare star DY Eri)

Phase 2 ✅ already done (Mason 2017 mass + Mann 2015 R/Teff/[Fe/H] + Cifuentes 2020 L + Bond 2017 system-coeval age + meta_notes including Shan 2024 P_rot 'debated' status).
Agent C drafts `docs/phase3/40-eridani-c.md`.

Specific items to address:
- Active M dwarf (flare star variable DY Eri) — H-alpha emission, X-ray bright
- Rotation: Shan 2024 P_rot 8.56 d (quality D, debated; recorded in meta_notes, not as recommended entry)
- vsini and activity history likely affected by AGB-mass-transfer spin-up from B's progenitor (Fuhrmann 2014 cited in Bond 2017 §6.2)
- AGB accretion: Bond 2017 mentions C "may be due to it having been spun up to a higher rotational velocity by accretion during the AGB phase of B" — Phase 3 narrative point
- Habitable-zone N/A from cfg perspective (no curated planets), but stellar luminosity 6.51e-3 Lsun → HZ ~0.07–0.2 AU (boilerplate)
- Visual styling: Active M4.5 V → red point with strong Hα variability; Firefly cfg downstream for flare aurora colors.

## Pre-existing artifacts to NOT duplicate

- `phase2/40_eridani/checklist.md` + `context-notes.md` — Phase 2 prep workspace (now verification target). Agents should READ these for context but treat any unverified value as candidate, not approved. The Mason 2017 mass / Mann 2015 [Fe/H] / Cifuentes 2020 L / Shan 2024 P_rot findings from today's follow-up commit (8509de9) are the authoritative state.
- `docs/phase2/40-eridani-{a,b,c}.html` — Phase 2 viewer output. Built from current DB. Don't edit.

## Cross-component consistency

After all 3 agents return:
- System age should agree across A/B/C narratives (Bond 2017 ~1.8 Gyr Tot total).
- BC orbit details (P=230.29 yr, e=0.4294) appear consistently in both B and C documents.
- A-BC unresolved status appears in A document.
- Distance 5.01 pc consistent everywhere.
- HD 26965 b refuted status mentioned in A document (with Burrows 2024 cite).

## Verification policy (per 2026-05-28 postmortem)

Each agent must:
- Pre-curation lit search for each measurement category (silence ≠ none)
- Citation value-check at paper Table level (not just abstract)
- DOI + bibcode verification at Crossref or ADS
- Multi-layer commit: DB + meta_notes + Phase 3 narrative + bibliography in same commit
- Launch its own verification subagent at the end of synthesis (Step 7 of postmortem procedure)
- Document in `context-notes.md` (this file) every Decisions-row classification

## Decisions log

- 2026-05-29: System workspace created. Agent A/B/C plan finalized. Working concurrently after this checkpoint.

## Agent A — 40 Eri A Decisions classification

Per Phase 3 skill Step 9.0. Every Decisions row planned for `docs/phase3/40-eridani-a.md` is labeled below.

### Phase 2 verification log (2026-05-29)

- **Mass 0.78 ± 0.08 Msun (Ma 2018)** — VERIFIED at paper Table 2. Method: M-R relation (Torres 2010) + spectroscopic params, labeled `evolutionary_model` in schema.
- **Mass alt 0.76 ± 0.03 Msun (Diaz 2018)** — VERIFIED at paper Table 1 SPECIES.
- **Radius 0.8061 ± 0.0036 Rsun (Boyajian 2012)** — VERIFIED at paper Table 6 (CHARA Classic interferometry, θ_LD = 1.504 ± 0.006 mas, listed as GJ 166A). REPLACES Rains 2020 as recommended because Boyajian has tighter fractional σ (0.45% vs 0.75%); both are interferometry-tier; tie-break by uncertainty per add-star skill.
- **Radius alt 0.804 ± 0.006 Rsun (Rains 2020)** — VERIFIED at paper Table 4 (VLTI/PIONIER, 40 Eri A is star #7 of 16 in Table 1 sample).
- **Teff 5143 ± 14 K (Boyajian 2012)** — VERIFIED at paper Table 6. REPLACES Rains 2020 5126 ± 30 K as recommended. Top-level `teff_k` updated.
- **Teff alt 5126 ± 30 K (Rains 2020)** — VERIFIED.
- **Teff alt 5151 ± 55 K (Diaz 2018)** — VERIFIED at SPECIES Table 1.
- **Luminosity 0.4078 ± 0.0032 Lsun (Boyajian 2012)** — VERIFIED at paper Table 6 (bolometric flux integration). REPLACES Rains 2020.
- **Luminosity alt 0.40 ± 0.01 Lsun (Rains 2020)** — VERIFIED at paper Table 4.
- **Age 6.9 ± 4.7 Gyr (Ma 2018)** — VERIFIED at paper Table 2 (PARSEC isochrone via SED fitting; NOT Y-Y as 2026-05-27 prep notes claimed). KEPT as recommended for the K-dwarf measurement category, but documented-divergence with Bond 2017 below.
- **Age alt 9.23 ± 4.84 Gyr (Diaz 2018)** — VERIFIED at SPECIES Table 1.
- **Age alt 1.8 Gyr (Bond 2017 IFMR-derived)** — VERIFIED at §6.2 (initial mass ~1.8 Msun, MS lifetime 1.7 Gyr + cooling age 122 Myr). Paper states "earlier concerns about an excessive age...appear to be resolved". No formal uncertainty in section text.
- **[Fe/H] -0.29 ± 0.12 (Diaz 2018)** — VERIFIED at SPECIES Table 1. KEPT recommended.
- **[Fe/H] alt -0.42 ± 0.04 (Ma 2018)** — VERIFIED at Ma 2018 Table 2; CORRECTS the prep notes which conflated -0.29 with Ma 2018.
- **[Fe/H] alt -0.31 ± 0.10 (Bensby 2014)** — paper-stated value retained (paper-level verification deferred due to no direct table access; bibcode 2014A&A...562A..71B confirmed correct title).
- **P_rot 42 d (Burrows 2024)** — VERIFIED at paper abstract + multiple section quotes ("~42 days", "stellar rotation period of ∼42 days"). REMOVED fabricated ±2.5 d uncertainty (paper does not quote a formal σ). Method `photometric_variability` retained because Burrows' inference is from line-RV + activity-correlation periodograms.
- **log R'HK -4.99 (Jenkins 2011)** — bibcode 2011A&A...531A...8J VERIFIED (paper title "Chromospheric activities and kinematics for solar type dwarfs and subgiants"). Specific HD 26965 row not table-verified (CDS table access limited in this session); value matches prep notes and well-known literature usage. Caveat in meta_notes.
- **log R'HK alt -4.94 (Henry 1996)** — bibcode 1996AJ....111..439H confirmed correct title ("A Survey of Ca II H and K Chromospheric Emission in Southern Solar-Type Stars"). Same paper-table caveat.

### Phase 3 Decisions row classification (16 rows)

- `spectral_type` = K0.5 V → **canonical-aligned** (Gray 2006 / Keenan & McNeil 1989)
- `mass_msun` = 0.78 ± 0.08 → **canonical-aligned** (Ma 2018; no dynamical alternative available because A-BC orbit is unfitted)
- `radius_rsun` = 0.8061 ± 0.0036 → **canonical-aligned** (Boyajian 2012 CHARA)
- `teff_k` = 5143 ± 14 → **canonical-aligned** (Boyajian 2012)
- `luminosity_lsun` = 0.4078 ± 0.0032 → **canonical-aligned** (Boyajian 2012)
- `metallicity_fe_h_dex` = −0.29 ± 0.12 → **canonical-aligned** (Diaz 2018; Bensby 2014 within 1σ)
- `age_gyr` = 1.8 → **documented-divergence** (Bond 2017 IFMR system-coeval vs Ma 2018 6.9 Gyr K-dwarf isochrone). cfg picks Bond because system-coeval anchored by the WD progenitor is more physically constraining than a single K-dwarf isochrone with 4.7 Gyr error.
- `rotation_period_days` = 42 → **canonical-aligned** (Burrows 2024 NEID activity); pre-Burrows Saar & Osten 1997 ~37 d is documented in Open items as a historical alternative reading
- `activity_log_rhk` = −4.99 → **canonical-aligned** (Jenkins 2011)
- `x_ray_log_lx_cgs` ~ 27.0 → **canonical-aligned** (ROSAT all-sky survey baseline; Schmitt 1985)
- `vulcan_disposition` = "Refuted (Burrows 2024)" → **canonical-aligned**
- `visual_surface_tint_hex_primary` = `#ffd5a8` (orange-tinted warm-white for K0.5 V) → **tie-break** (interesting-first vs sun-like)
- `stellar_color_temp_k` = 5143 → **canonical-aligned** (derived from Teff)
- `star_in_planet_sky_apparent_diameter_arcmin` (from B-C barycenter at ~400 AU) → **canonical-aligned** (derived geometry)
- `visual_companion_event_b_c_pair_visible_arcsec` = ~83 → **canonical-aligned** (WDS J04153−0739)
- `apparent_magnitude_v_from_earth` = 4.43 → **canonical-aligned** (Hipparcos)

Row counts: **14 canonical-aligned**, **1 tie-break**, **1 documented-divergence** (age).

## Agent B — 40 Eri B Decisions classification

Step 9.0 pre-draft classification per nearstars-phase3 skill. Every
Decisions row labelled before prose drafting. 40 Eri B is a stellar
synthesis on a DA white dwarf: most rows are direct paper-anchored
numbers from Bond et al. 2017, so canonical-aligned dominates.

| Decisions row | Value | Class | Note |
|---|---|---|---|
| `spectral_type` | DA2.9 | canonical-aligned | GBR11 (Gianninas, Bergeron & Ruiz 2011) is the canonical DA temperature-index source; Bond 2017 §2 adopts. |
| `mass_msun` | 0.573 ± 0.018 | canonical-aligned | Bond 2017 dynamical mass via HST/FGS astrometry + Mason 2017 BC orbit. Mason 2017 reports a virtually identical 0.575 ± 0.018 from the same orbital fit; the small difference is the parallax adoption. |
| `radius_rsun` | 0.01308 ± 0.00020 | canonical-aligned | Bond 2017 SED-fit (BVRI + ubvy + JHK + Hipparcos π + Teff_atm). |
| `teff_k` | 17200 ± 110 | canonical-aligned | Bond 2017 Balmer-line atmosphere fit (Tremblay & Bergeron 2009 grid). |
| `luminosity_lsun` | 0.01349 ± 0.00054 | canonical-aligned | Bond 2017 bolometric flux integration. |
| `log_g_cgs` | 7.957 ± 0.020 | canonical-aligned | Bond 2017 atmosphere fit. |
| `gravitational_redshift_km_s` | 27.82 ± 0.97 | canonical-aligned | Bond 2017 derived from R, M (GR consistency check). |
| `cooling_age_myr` | ~122 | canonical-aligned | Bond 2017 §6.2 thin-H cooling track. No formal σ stated by paper. |
| `progenitor_initial_mass_msun` | ~1.8 | canonical-aligned | Bond 2017 §6.2 IFMR (Salaris+2009) inversion. |
| `pre_wd_lifetime_gyr` | ~1.7 | canonical-aligned | Bond 2017 §6.2 main-sequence + post-MS lifetime for 1.8 M☉ progenitor. |
| `total_age_gyr` | 1.8 ± 0.5 | canonical-aligned | Bond 2017 §6.2 sum (122 Myr + 1.7 Gyr). DB σ=0.5 is a curator estimate (Phase 2 meta_notes confirms no paper-stated σ); kept consistent with DB. |
| `h_envelope_mass_fraction_log_qh` | ≈ −10 | canonical-aligned | Bond 2017 §6.1 — thin H layer; canonical thick-H value (q_H ≈ 10⁻⁴) does not fit cooling track. |
| `magnetic_field_upper_limit_gauss` | <250 | canonical-aligned | Landstreet & Bagnulo 2015 ESPaDOnS limit, σ⟨Bz⟩ ≈ 85 G. |
| `core_composition` | CO | canonical-aligned | Bond 2017 §6.3 — CO-core MRR fits 40 Eri B to within errors; standard for M_init ~ 1.8 M☉ progenitor. |
| `metal_pollution_dazness` | none (clean DA) | canonical-aligned | Bond 2017 implicit (Balmer-only atmosphere fit); Fabrika 2003 ultra-weak metal lines attributed to circumstellar/ISM gas, not photospheric. |
| `convective_envelope` | none (purely radiative atmosphere) | canonical-aligned | Bond 2017 §6.1 explicit; Teff 17,200 K is well above the H-convection-zone onset (~13,000 K for DA). |
| `companion_a_separation_arcsec` | ~83 (no fitted orbit) | canonical-aligned | Tokovinin MSC 2018 wide-binary geometry. |
| `companion_c_orbit_period_yr` | 230.09 ± 0.68 | canonical-aligned | Mason, Hartkopf & Miles 2017 — Binary Star Orbits V, grade 1. |
| `companion_c_orbit_eccentricity` | 0.4300 ± 0.0027 | canonical-aligned | Mason 2017 Table 4. |
| `companion_c_orbit_a_arcsec` | 6.9310 ± 0.0500 | canonical-aligned | Mason 2017 Table 4. |
| `visual_surface_tint_hex_primary` | `#cfd9ff` (bright blue-white) | tie-break | Planck-locus at 17,200 K → blue-white tint; cfg picks a saturated blue-white for visual distinctiveness from solar-white companions. Documented as tie-break in Basis. |
| `stellar_color_temp_k` | 17200 | canonical-aligned | Identical to Teff for a clean DA radiative atmosphere. |
| `visual_apparent_diameter_arcsec_at_1au` | 25.09 | canonical-aligned | Derived geometric (2 R★ / a × (180·3600/π)). |

Row count summary: **20 canonical-aligned, 1 tie-break, 0 documented-divergence.**
No `## Canonical alternatives` section required.

Mason BC orbit verification note: the Phase 2 working-notes recorded
`P = 230.30 ± 0.68 yr` and `e = 0.4294 ± 0.0027`; the actual Mason 2017
Table 4 values are P = 230.09 ± 0.68 and e = 0.4300 ± 0.0027 (verified
2026-05-29 via ar5iv [1707.03635](https://arxiv.org/abs/1707.03635)). The Phase 3 synthesis uses the
paper-actual numbers. The Phase 2 DB does not contain any BC orbit
entries (orbit lives outside `stellar_props_curated.json`), so no DB
patch is needed from Phase 3 — flag only.

Mason 2021 update note: a newer orbit fit (Mason et al. 2021,
`2021AJ....162...53M`, P = 233.20 ± 0.65 yr, e = 0.4141 ± 0.0072,
a = 6.88788 ± 0.03488″) supersedes Mason 2017 in the Sixth Orbit
Catalog and on Wikipedia. The Phase 3 synthesis uses Mason 2017
because (1) the task brief and Phase 2 prep both refer to Mason 2017,
(2) Bond 2017's mass measurement explicitly uses the Mason 2017 orbit,
so citing the 2017 orbit keeps the mass/orbit chain self-consistent.
Mason 2021 is listed in Open items for follow-up so a future
reconciliation pass can adopt it together with a re-derived dynamical
mass.

## Agent C — 40 Eri C Decisions classification

Per Step 9.0 of `nearstars-phase3` SKILL.md. Diagnostic question per
`references/conflict-resolution.md` § "Tie-break vs. divergence" applied
to each row of the 40 Eri C Decisions table before drafting prose.

Row counts: **9 canonical-aligned, 4 tie-break, 0 documented-divergence.**

| Row | Label | Justification |
|---|---|---|
| `spectral_type` = M4.5 Ve | canonical-aligned | Gray & Garrison 1989 reclassification adopted by IAU; SIMBAD lists M4.5Ve. Mann 2015 Table 5 lists M4.7 (paper-level variation); diff is within MK classification scatter, M4.5 Ve is the broader-community canonical. Documented in prose. |
| `mass_msun` = 0.2041 ± 0.0064 | canonical-aligned | Mason, Hartkopf & Miles 2017 §3 binary_orbit dynamical fit (page 6). DB Phase 2 recommended:true. |
| `radius_rsun` = 0.274 ± 0.011 | canonical-aligned | Mann et al. 2015 Table 5 'Gl 166 C' row (M_K relation + BT-Settl). DB Phase 2 recommended:true. |
| `teff_k` = 3167 ± 61 | canonical-aligned | Mann et al. 2015 Table 5. DB Phase 2 recommended:true. |
| `luminosity_lsun` = 6.51e-3 ± 0.13e-3 | canonical-aligned | Cifuentes et al. 2020 CARMENES catalog VizieR J/A+A/642/A115. DB Phase 2 recommended:true. |
| `metallicity_fe_h_dex` = -0.21 ± 0.08 | canonical-aligned | Mann et al. 2015 Table 5 (low_res_spectroscopy + Mann 2013a calibration). DB Phase 2 recommended:true. |
| `age_gyr` = 1.8 ± 0.5 | canonical-aligned | Bond et al. 2017 §6.2 system-coeval IFMR-derived. Uncertainty curator-estimated (paper reports only ~1.8 Gyr). |
| `rotation_period_days` = N/A | canonical-aligned | Shan 2024 8.56 d is quality flag D (debated, 27 of 166 periods). No conflicting paper-confirmed value. Recording N/A here matches Phase 2 decision (no recommended:true entry; meta_notes only). |
| `activity_h_alpha_pew_a` = N/A (range -2 to -4 reported) | canonical-aligned | Multi-survey scatter (CARMENES / Schoefer / Newton); no single-paper anchor curated. Range matches each survey within its own error budget. |
| `flare_rate_per_day` = N/A | canonical-aligned | DY Eri variable designation confirms flare activity, but no quantitative survey-derived rate in current bibliography. Open item. |
| `x_ray_log_lx_lbol` = qualitatively "bright" | canonical-aligned | No paper anchor for 40 Eri C specifically; ROSAT All-Sky Survey detection is system-blended with B WD. Qualitative only. |
| `visual_surface_tint_hex_primary` = `#d97f4a` (warm red-orange, M4.5 V Planck + Hα tint) | tie-break | Planck-locus blackbody at 3167 K + Hα emission boost in red wavelengths. No paper specifies a hex; tie-break: interesting-first toward saturated red-orange over generic dull-red. |
| `stellar_color_temp_k` = 3167 | canonical-aligned | Derived from Teff. |
| `flare_aurora_color_hint` (downstream Firefly) | tie-break | Active M dwarf → strong Hα 656 nm tint in plasma effects; specific palette deferred to firefly-cfg skill. Tie-break: documented as a Phase 3 hint, exact palette downstream. |
| `visual_companion_event_b_visible_as_blue_point` | tie-break | BC 33 AU mean separation → B WD at apparent V ~ 5-7 from C, distinctly blue. No paper studied this view; interesting-first. |
| `visual_companion_event_a_visible_as_orange_distant_point` | tie-break | A-BC ~2050 AU mean separation → A at V ~ 5 from C, distinctly orange (K0.5 V). Interesting-first; tie-break. |
| `agb_spin_up_narrative` (prose, not a cfg field) | canonical-aligned | Bond 2017 §6.2 explicitly cites Fuhrmann et al. 2014 suggestion that C "may have been spun up to higher rotational velocity by accretion during the AGB phase of B". Documented in Rotation section narrative; not a Decisions row. |

Notes:
- No `## Canonical alternatives` section needed — 0 documented-divergences.
- Hex tint #d97f4a is a tie-break under Confidence: low. Document the
  Planck calc + Hα reasoning in the Visual styling section.
- AGB-spin-up is paper-cited (Bond 2017 + Fuhrmann 2014), so it's
  canonical-aligned even though it's narrative-only.

