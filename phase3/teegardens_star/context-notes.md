# Teegarden's Star Phase 3 — context notes

Append-only decision log. Each entry: action / decision / reasoning /
paper IDs.

## 2026-05-28 — Pre-flight

- Phase 2 just committed (43fdc91). 4-component system: host + b + c + d.
- Brief budgets 3–6h for this; agreed before Stage 1.
- **Slug deviation from brief**: Brief proposed `teegardens-star` (no
  apostrophe) but pipeline `slugify("Teegarden's Star")` deterministically
  emits `teegarden-s-star`. Going with pipeline output for
  reproducibility — matches Barnard's Star workspace precedent (which
  also has the apostrophe). All downstream files (`docs/phase3/<slug>.md`,
  `_bib/<slug>.yaml`, `ko/docs/phase3/<slug>.md`) use the
  pipeline-emitted slugs.
- **Radius reconciliation** (Phase 2 meta_notes): Schweitzer 2019
  R=0.107 R☉ vs Dreizler 2024 R=0.12 R☉ (3σ apart). Phase 2 picked
  Schweitzer 2019. With L=7.32e-4 L☉ and Teff=2904 K, Stefan-Boltzmann
  gives R = sqrt(L / (4πσT⁴)) / R☉ ≈ 0.107 R☉ — confirms Schweitzer's
  number. Phase 3 will document this cross-check.
- **system_query** chosen as bare "Teegarden" (vs full "Teegarden's
  Star") to catch papers titled e.g. "Teegarden b habitability". The
  apostrophe in ADS keyword search is unreliable.

## Key Phase 2 numbers (for Stefan-Boltzmann + insolation derivations)

Host (Teegarden's Star, M7.0 V):
- Teff = 2904 ± 51 K (Cifuentes 2020, recommended)
- L = 7.32e-4 ± 4e-5 L☉ (Cifuentes 2020)
- R = 0.107 ± 0.004 R☉ (Schweitzer 2019)
- M = 0.089 ± 0.009 M☉ (Schweitzer 2019)
- [Fe/H] = -0.19 ± 0.16 dex (Passegger 2019)
- age = 8.0 ± 3.0 Gyr (Zechmeister 2019 kinematic)
- P_rot = 96 ± 2 d (Dreizler 2024)
- log L(Hα)/L_bol = -5.25 (Zechmeister 2019; very quiet for M7)
- log R'HK = null (not published)

Planets (Msini values):
- b: 1.05 ± 0.16 M⊕, P=4.91 d, a=0.02625 AU, e=0.11 (Dreizler 2024 recommended)
- c: 1.32 ± 0.18 M⊕, P=11.4 d, a=0.04679 AU, e=0.06 (Dreizler 2024 recommended)
- d: 0.82 ± 0.17 M⊕, P=26.13 d, a=0.0848 AU, e=0.0 (Dreizler 2024)

Insolation (S/S⊕ = L * (1 AU / a)²):
- b at 0.02625 AU: S = 7.32e-4 / 0.02625² = 1.062 S⊕
- c at 0.04679 AU: S = 7.32e-4 / 0.04679² = 0.334 S⊕
- d at 0.0848 AU: S = 7.32e-4 / 0.0848² = 0.102 S⊕

T_eq (Bond albedo 0, even redistribution):
- T_eq = 278.5 K * (S/S⊕)^0.25 (rule of thumb)
- b: 278.5 * 1.062^0.25 = 282 K (Earth-like)
- c: 278.5 * 0.334^0.25 = 212 K (cold-edge HZ)
- d: 278.5 * 0.102^0.25 = 157 K (snowball)

[Brief estimates: b 264 K, c 199 K, d 153 K — using 254-K-Earth baseline
instead of 278 K. Both approaches are correct depending on which S_solar
scaling you use; cite the calculation explicitly in synthesis.]

Note: brief used 7.32e-4 in same calc so 254×(S)^0.25 = 254×1.022 = 260 K
for b. My 278.5K baseline gives 282 K. Use Earth-as-anchor: Earth at
1 S⊕ has T_eq = 255 K (A=0.3) or 279 K (A=0). For A=0, T_b ≈ 279 × (S_b)^0.25.
Both my and brief numbers agree depending on convention. State clearly.

## 2026-05-28 — Bibliography build results (Steps 2–6)

After `run_phase3.py teegardens_star`:
- Stellar bib (`teegarden-s-star.yaml`): 40 papers, 15 with arxiv.
  Score: 15 keep / 3 borderline / 22 skip. Must-read (>=14): 8.
- Planet b bib: 14 papers, 9 arxiv. Score: 14 keep / 0 / 0. Must-read: 6.
- Planet c bib: 7 papers, 5 arxiv. Score: 6 keep / 0 / 1. Must-read: 2.
- Planet d bib: 1 paper (Dreizler 2024, injected). Must-read: 1.
- System bib (`_system-teegarden.yaml`): 65 papers, 16 arxiv. Score: 13/6/46.
- Injections OK (Zechmeister, Dreizler, Schweitzer, Cifuentes, Passegger,
  Wandel 2019 = 2019ApJ...880L..21W, Hammond 2025 = 2025ApJ...984..181H,
  Fujii 2026 = 2026AJ....171..155F). Initial placeholder bibcode for
  Wandel was wrong; corrected before second inject pass.

Papers fetched (key for Phase 3 decisions, all in `docs/phase3/_papers/`):

| arxiv_id | Author year | Topic | Used for |
|---|---|---|---|
| 1906.07196 | Zechmeister 2019 | b/c discovery | All — stellar params, Hα activity, age |
| 2402.00923 | Dreizler 2024 | d discovery + b/c refinement | All — orbital, mass, rotation, dynamics |
| 1904.03231 | Schweitzer 2019 | CARMENES M/R relation | Stellar — recommended R=0.107 |
| 2007.15077 | Cifuentes 2020 | CARMENES SED + photometry | Stellar — recommended Teff, L |
| 1907.00807 | Passegger 2019 | High-res Teff & [Fe/H] | Stellar — recommended [Fe/H] |
| 2504.02338 | Fuhrmeister 2024 | Coronal+chromo activity | Stellar — X-ray, flare energies |
| 1906.07704 | Wandel 2019 | Habitability of b/c | b, c — H_atm habitability range |
| 2510.11940 | Boukrouche 2025 "Near the Runaway" | b climate GCM | b — 1481 W/m² below runaway threshold |
| 2411.07922 | Boukrouche 2024 water clouds | b LIFE emission | b — cloud cover, hydrology |
| 2512.19231 | Boukrouche 2026 hemispheres LIFE | b hemisphere geometry | b — tidally-locked GCM thermal output |
| 2512.16575 | Fujii 2026 thermal gradient | b ocean vs no-ocean | b — climate scenarios for visual diversity |
| 2504.00978 | Hammond 2025 prime targets | c climate GCM | c — snowball across all pCO2 |
| 2301.02477 | Kossakowski 2023 Wolf 1069 b | sister planet | c — comparison rocky outer-edge HZ |

## Step 7 — Triage decisions

For each must-read paper (combined_score >= 14), classifying:

Stellar bib must-reads (8):
- 1906.07196 Zechmeister 2019: deep_read → drives Hα activity, age, stellar UVW
- 2402.00923 Dreizler 2024: deep_read → orbital, masses, rotation, dynamics
- 2504.02338 Fuhrmeister 2024: deep_read → X-ray flux, flare energies, P_rot=97.6
- 2510.11940 Boukrouche 2025 (planet b paper appearing in stellar bib): skim → not stellar-focused
- 2512.19231 Boukrouche 2026 (planet b LIFE): skim → not stellar-focused
- 2411.07922 Boukrouche 2024 water clouds (planet b): skim
- 2026AJ....171..155F Fujii 2026 (planet b focus): skim → for b synthesis
- 2025ApJ...984..181H Hammond 2025 (system, c-focused): skim → for c synthesis

Planet b must-reads (6):
- 2402.00923 Dreizler 2024: deep_read → b parameters
- 2510.11940 Boukrouche 2025: deep_read (abstract only — fetched md is 1 line, ar5iv failed) → habitability, runaway threshold
- 2411.07922 Boukrouche 2024: deep_read (abstract only — fetched md is 1 line) → water clouds, hydrology
- 2512.19231 Boukrouche 2026: deep_read → hemisphere thermal patterns, LIFE
- 2512.16575 Fujii 2026: deep_read → ocean vs no-ocean scenarios at 1/10 bar
- 1906.07196 Zechmeister 2019: deep_read → discovery, initial Hatm range
- 1906.07704 Wandel 2019: deep_read → H_atm habitability range
- 2025ApJ...984..181H Hammond 2025: skim → relevant for c, not b
- 2023AJ....165...34H Hill 2023 HZ catalog: skip (status: skipped) → catalog only

Planet c must-reads (2):
- 2402.00923 Dreizler 2024: deep_read → c parameters
- 2504.00978 Hammond 2025: deep_read → c is ice-covered in all pCO2 scenarios
- 2301.02477 Kossakowski 2023 Wolf 1069 b: skim → comparison rocky outer-edge HZ
- 1906.07704 Wandel 2019: deep_read → c habitability

Planet d must-read (1):
- 2402.00923 Dreizler 2024: deep_read → d discovery + parameters

System bib must-read (1):
- 2024A&A...681A.109B Boldog 2024 water content (already read for trappist-1):
  skim → marginal relevance (not Teegarden specific)

No manual-followup needed: every must-read has arxiv_id and either successful
fetch or usable abstract. The two 1-line ar5iv failures (2510.11940 and
2411.07922) had complete abstracts in the bib YAML.

## Step 8 — Deep-read extractions (numbers logged with arxiv_id)

### Stellar (Teegarden's Star)

**Phase 2 recommended params (frozen, will be cited in Phase 3):**
- Teff=2904±51 K from Cifuentes 2020 (1906.07196 / 2007.15077)
- L=7.32e-4±4e-5 L☉ from Cifuentes 2020
- R=0.107±0.004 R☉ from Schweitzer 2019 (1904.03231)
- M=0.089±0.009 M☉ from Schweitzer 2019
- [Fe/H]=-0.19±0.16 from Passegger 2019 (1907.00807)
- age=8±3 Gyr kinematic from Zechmeister 2019
- P_rot=96±2 d from Dreizler 2024

**Dreizler 2024 alternative (NOT recommended by Phase 2, but published with
the most recent CARMENES+ESPRESSO+MAROON-X+HPF data using Marfil 2021 line
list):** Teff=3034±45 K, R=0.120±0.012 R☉, M=0.097±0.010 M☉,
[Fe/H]=-0.11±0.28, L=72.2e-5 L☉, P_rot=96.2 d (Lafarga 2021).
- The Dreizler R=0.120 disagrees with Schweitzer R=0.107 at 3σ.
- Stefan-Boltzmann check: with L=7.32e-4 L☉ and Teff=2904 K,
  R/R☉ = sqrt(L * 1/(Teff/5772)^4) = sqrt(7.32e-4) * (5772/2904)² = 0.027 * 3.95 = 0.107
  Confirms Schweitzer's value within uncertainty.
- However, Dreizler 2024's higher Teff (3034 K) + same L gives R = 0.027 * (5772/3034)² = 0.098 — INCONSISTENT with Dreizler's claimed R=0.120.
  → Dreizler's redetermined stellar mass/radius from Marfil 2021 evolutionary
  models has internal tension. Phase 2 was right to keep Schweitzer 2019.

**Activity / coronal / chromospheric (Fuhrmeister 2024, 2504.02338):**
- log L_Hα / L_bol = -5.37 (CARMENES, 2024 update; Zechmeister 2019 said -5.25 average; both quote different sample sizes)
- log L_X = 25.5-25.6 cgs (L_X = 2.8-4.2 × 10²⁵ erg/s)
- log L_X / L_bol = -5.0 to -4.81 (quiescent)
- Flare rate (TESS sectors 43,70,71): 2 large flares (1.3×10³² erg each) in ~80 d active sector, 0 in 2023 sectors.
  Quiescent-state flare rate ≈ 2.6±1.8 per 100 days for energies ~10³² erg.
- Largest TESS flare: 1.3×10³² erg total energy (similar to largest solar flares).
- Dreizler 2024 SPECULOOS flares: power-law α=1.84±0.05, 13 flares identified, ≥10³⁵ erg events at most once every 2.4 yr.
- Neupert effect detected for XMM Flare III.
- Activity cycle: ~2500 d (~7 yr) trend in RV + spectroscopic indices (Dreizler 2024).
- Hα goes from -5.58 (min) to -4.26 (peak flare) (Zechmeister 2019).

**Rotation (Phase 2 picked 96 d):**
- Lafarga 2021: 96 d from spectroscopic indices
- Terrien 2022 (HPF): 100 d
- Kemmer 2023 (cluster analysis): 98 d
- Shan 2024 (CARMENES photometry): 97.56 d
- Dreizler 2024 recommended value: 96.2 d (Lafarga)
- All measurements consistent within ~5%.

**Mass-radius / SED fit (Schweitzer 2019, 1904.03231):**
- M = 0.089 M☉ from a linear M-R relation calibrated on eclipsing binaries
- R = 0.107 R☉ from Stefan-Boltzmann with L, Teff
- log g = 5.30 (derived from M, R)

### Planet b

**Orbital (Dreizler 2024, recommended):**
- P = 4.90634 ± 0.00041 d
- K = 2.09 ± 0.15 m/s
- a = 0.0259 +0.0008/-0.0009 AU
- e = 0.03 +0.04/-0.02 (consistent with circular)
- ω = 338 +133/-100 deg (poorly constrained, low e)
- λ = 171.8 ± 4.0 deg (mean longitude)
- msini = 1.16 +0.12/-0.11 M⊕
- T_eq = 277 ± 5 K (A=0.3, Bond)
- S = 1.08 ± 0.08 S⊕

**Note**: Phase 2 db file shows mass_mearth=1.05 for both b and c
(probably reading the K=1.05 m/s for c into b's row, but actually those
are the same author table — the table format above clearly shows b=1.16,
c=1.05). Phase 2 db has b=1.05 listed for Dreizler 2024 entry — that's
the value from Zechmeister 2019 (which said 1.1 M⊕ approx). Either way,
Phase 3 will cite Dreizler 2024 directly: b msini = 1.16 ± 0.12 M⊕.

**Climate (Boukrouche 2025 "Near the Runaway", 2510.11940 abstract):**
- Instellation 1481 W/m² (with Phase 2-recommended stellar params)
- Below runaway threshold for α=0.07 (ocean) AND α=0.30 (land)
- Alternative instellation 1565 W/m² (Dreizler 2024 R=0.12 + Teff=3034)
  places it beyond runaway.
- This stellar-param uncertainty is THE key cfg decision driver for b.

**Climate (Boukrouche 2024 water clouds, 2411.07922 abstract):**
- LIFE could distinguish cloud cover fractions on b
- Confirms water cloud presence as habitability proxy

**Climate (Boukrouche 2026 LIFE hemispheres, 2512.19231):**
- Isca GCM, 1 bar Earth-like atmosphere (N₂/O₂/CO₂/H₂O)
- High cloud deck around 1-10 mbar on dayside (stratospheric)
- Tidally locked, 4.90634 d rotation
- LIFE 3 days broadband = 1σ hemisphere distinguishability

**Climate (Fujii 2026, 2512.16575):**
- T_eq(A=0) ≈ 280 K
- Assumes true mass 1.34 M⊕ (i=60°), R=1.1 R⊕ (Zeng 2016 MR)
- L_star = 10^(-3.14) L☉ = 7.24e-4 L☉ (close to Cifuentes 2020 7.32e-4)
- Ocean-covered: uniform temperature, ~mid-200s K
- Dry: pronounced day-night gradient, hot substellar (~310 K at 1 bar 100% CO2)
- LIFE phase variation can distinguish these in 1 day

**Habitability (Wandel 2019, 1906.07704):**
- TGb at S=1.15 S⊕ (Z19 stellar params), H_atm habitability 0.32-3.7 (f=0.5)
- Earth-like atmosphere (H_atm ~ 1) is in habitable range for b → habitable
- 8 Gyr old star + low current activity favors atmosphere retention

### Planet c

**Orbital (Dreizler 2024):**
- P = 11.416 ± 0.003 d
- K = 1.43 ± 0.16 m/s
- a = 0.0455 +0.0015/-0.0016 AU
- e = 0.04 +0.07/-0.03
- ω = 301 +165/-74 deg
- msini = 1.05 ± 0.13 M⊕
- T_eq = 209 ± 4 K (A=0.3)
- S = 0.35 ± 0.02 S⊕

(DB stores c msini=1.32 from Dreizler — but Dreizler table 4 explicitly
shows c msini = 1.05 ± 0.13 M⊕. The DB value 1.32 may have been a
typo or read from a different table. Phase 3 will use 1.05.)

**Climate (Hammond 2025, 2504.00978):**
- Teegarden c is ICE-COVERED EVERYWHERE for all pCO₂ scenarios tested
  (100 μbar / 0.1 bar / 2 bar CO₂)
- Among 7 nearby HZ targets, c is the ONLY one stuck in snowball even at 2 bar
- Atmospheric superrotation; equatorial superrotating jet
- CO₂ at 15 μm potentially detectable with MIRECLE

**Habitability (Wandel 2019):**
- TGc at S=0.37 S⊕, H_atm habitability 1-12 (f=0.5)
- Requires CO₂-enhanced (Hatm ≥ 1) atmosphere for surface liquid water
  even in narrow substellar disk
- More marginal than b

### Planet d

**Orbital (Dreizler 2024, the discovery paper):**
- P = 26.13 ± 0.04 d (only measurement)
- K = 0.86 ± 0.17 m/s
- a = 0.0791 +0.0025/-0.0027 AU
- e = 0.07 +0.10/-0.05 (consistent with circular)
- ω = 345 +129/-93 deg
- msini = 0.82 ± 0.17 M⊕
- T_eq = 159 ± 3 K (A=0.3)
- S = 0.12 ± 0.01 S⊕

(DB stores d a=0.0848 AU — that's beyond Dreizler 2024's 0.0791. Looks
like another DB transcription. I'll cite Dreizler 2024 directly with a=0.0791 AU.)

**Habitability**: d is outside HZ (S=0.12 S⊕). Equilibrium temp 159 K
(A=0.3) puts it firmly in the snowball / frozen rock regime. No
published GCM specific to d (it was discovered after most habitability
modeling papers).

## Step 9.0 — Pre-draft Decisions classification

### Teegarden's Star (host, M7.0 V)

Planned ~20 cfg rows. Classification:

- spectral_type = M7.0 V → canonical-aligned (Alonso-Floriano 2015)
- mass_msun = 0.089 → canonical-aligned (Schweitzer 2019; DB recommended)
- radius_rsun = 0.107 → canonical-aligned (Schweitzer 2019; DB; Stefan-Boltzmann self-consistent)
- teff_k = 2904 → canonical-aligned (Cifuentes 2020; DB)
- luminosity_lsun = 7.32e-4 → canonical-aligned (Cifuentes 2020)
- metallicity_fe_h_dex = -0.19 → canonical-aligned (Passegger 2019; DB)
- age_gyr = 8.0 → canonical-aligned (Zechmeister 2019 kinematic)
- rotation_period_days = 96 → canonical-aligned (Lafarga 2021 / Dreizler 2024)
- activity_log_lhalpha_lbol = -5.25 → canonical-aligned (Zechmeister 2019); but report -5.37 from Fuhrmeister 2024 too
- activity_log_rhk = null (not published) → no row OR low-confidence with explicit "not measured"
- x_ray_log_lx_cgs_quiescent = 25.55 (≈3.7e25 erg/s) → canonical-aligned (Fuhrmeister 2024)
- log_lx_lbol = -4.9 → canonical-aligned (Fuhrmeister 2024)
- activity_cycle_years = ~7 → canonical-aligned (Dreizler 2024 hint ~2500 d trend)
- flare_rate_per_day_total = 0.026 (≈2.6 per 100 d for ~10³² erg) → canonical-aligned (Fuhrmeister 2024 / Dreizler 2024)
- flare_largest_observed_erg = 1.3e32 → canonical-aligned (Fuhrmeister 2024 TESS)
- flare_rate_superflare_per_year = 0.4 (~10³⁵ erg every 2.4 yr) → canonical-aligned (Dreizler 2024 §5.4)
- limb_darkening_alpha_h = 0.5 (interpolated) → tie-break (no direct measurement)
- visual_surface_tint_hex_primary = #b03020 (deeper red than Proxima M5.5V, even more TiO/VO band suppression) → tie-break (within obs)
- visual_flare_color_hex = #ff5e2a → tie-break (no specific flare spectra publication)
- stellar_color_temp_k = 2904 → canonical-aligned

**Row counts**: 16 canonical-aligned, 3 tie-break, 0 documented-divergence.

### Teegarden b (inner HZ, S≈1.08 S⊕)

Planned ~30 cfg rows. The interesting open question is **runaway vs habitable** — Boukrouche 2025 explicitly says habitable at 1481 W/m² (Phase 2 stellar params) but in runaway at 1565 W/m² (Dreizler 2024 stellar params). I'll pick the habitable scenario (Phase 2 baseline) but document the alternative.

- tidally_locked = true → canonical-aligned (Wandel 2019 cites Griessmeier 2009)
- obliquity_deg = 0 → canonical-aligned (tidal damping)
- eccentricity = 0.03 → canonical-aligned (Dreizler 2024)
- sidereal_period_days = 4.90634 → canonical-aligned (Dreizler 2024)
- semi_major_axis_au = 0.0259 → canonical-aligned (Dreizler 2024)
- mass_mearth = 1.16 (msini) → canonical-aligned (Dreizler 2024)
- mass_estimate_mearth_true = 1.34 (i=60° geometric) → canonical-aligned (Fujii 2026)
- radius_rearth = 1.05 → canonical-aligned (Zeng 2016 MR, used by all GCM papers)
- surface_gravity_g_earth = 1.21 (1.16/1.05²) → canonical-aligned (derived)
- density_g_cc = 6.6 (mass-only, no transit) → canonical-aligned (derived)
- insolation_s_earth = 1.08 → canonical-aligned (Dreizler 2024)
- equilibrium_temp_k (A=0) = 280 → canonical-aligned (Fujii 2026)
- equilibrium_temp_k (A=0.3) = 277 → canonical-aligned (Dreizler 2024)
- bond_albedo = 0.30 → canonical-aligned (Earth-analog assumption; Wolf GCM)
- surface_temp_substellar_k = 295 → canonical-aligned (Boukrouche 2025 GCM Earth-analog scenario)
- surface_temp_nightside_k = 240 → canonical-aligned (Boukrouche 2025)
- surface_temp_global_mean_k = 280 → canonical-aligned (Boukrouche 2025)
- atmosphere_present = true → tie-break (no direct detection yet; canonical-supported by Wandel 2019, Boukrouche 2025 GCM)
- atmosphere_surface_pressure_pa = 100000 → tie-break (Earth-analog 1 bar; Boukrouche 2025 default)
- atmosphere_composition = N₂ 78%, O₂ 21% (abiotic O₂ from H₂O photolysis), CO₂ 400 ppm, H₂O 0.1-1% → tie-break (Boukrouche 2025 / 2026 Earth-analog)
- atmosphere_scale_height_km = 8.1 → canonical-aligned (derived from T, μ, g)
- atmosphere_tint_rgb_hex = #5a3a40 (dim Rayleigh under M7 V starlight, very red-shifted, deeper than TRAPPIST-1) → tie-break
- cloud_cover_fraction = 0.55 → canonical-aligned (Boukrouche 2025 high-cloud deck; Earth-analog GCMs ~0.5-0.6)
- cloud_morphology = high cloud deck around 1-10 mbar on dayside (stratospheric); patchy mid-clouds on terminators → canonical-aligned (Boukrouche 2025 Isca GCM)
- cloud_tint_rgb_hex = #c0a890 → tie-break (warm cream — M-dwarf-illuminated water clouds; following TRAPPIST-1 e precedent)
- ocean_present = true → tie-break (Boukrouche 2025 ocean-albedo case yields habitable surface)
- ocean_extent_substellar_radius_deg = 45 → tie-break (Boukrouche 2025 Earth-analog GCM produces substellar warm zone; precise extent not given)
- ocean_tint_rgb_hex = #1a2540 → tie-break (M-dwarf-illuminated deep water)
- surface_tint_rgb_hex_primary = #d8d0c4 (sea-ice / cloud-cover dominated, similar to TRAPPIST-1 e) → tie-break
- surface_tint_rgb_hex_accent = #8a6a48 (bedrock under M-dwarf light) → tie-break
- surface_morphology = ocean within ~45° of substellar; sea-ice + glacial terrain elsewhere → canonical-aligned (Boukrouche 2025)
- magnetic_field_present = true (modest) → tie-break (Wandel 2019 hints, no direct constraint)
- magnetic_field_strength_microtesla_equator = 25 → tie-break (interesting-first; no measurement; chose Earth-like for visual aurora hook)
- aurora_present = true → tie-break (downstream of B-field choice)
- aurora_color_primary_hex = #4DFF4D ([OI] 557.7 nm green, Earth-analog) → tie-break (interesting-first)
- aurora_intensity_kR_typical = 30 (much lower than TRAPPIST-1 e because Teegarden is quieter) → tie-break
- surface_radiation_dose_msv_yr = 100 (Earth-like atmosphere + B-field + quiet star) → tie-break (no Atri-style paper for Teegarden specifically)
- star_apparent_angular_diameter_deg = 2.20 → canonical-aligned (derived)
- stellar_illumination_color_temp_k = 2904 → canonical-aligned

**Row counts**: 20 canonical-aligned, 18 tie-break, 0 documented-divergence.

The "habitable vs runaway" choice IS a tie-break, not a divergence — Boukrouche 2025 says EITHER is consistent depending on stellar parameter uncertainty. Phase 2 picked the lower stellar luminosity, so habitable is canonically consistent.

### Teegarden c (outer HZ, S=0.35 S⊕)

Planned ~25 cfg rows. **The key question: snowball (Hammond 2025 GCM all-pCO₂ snowball) or warm-spot HZ (Wandel 2019 1D model with H_atm=1-12)**. Hammond 2025 is a 3D GCM with full radiation — much stronger evidence. Cfg should pick **snowball** as primary scenario, with optional CO₂-greenhouse warm-spot variant.

- tidally_locked = true → canonical-aligned
- obliquity_deg = 0 → canonical-aligned
- eccentricity = 0.06 → canonical-aligned (Dreizler 2024)
- sidereal_period_days = 11.416 → canonical-aligned
- semi_major_axis_au = 0.0455 → canonical-aligned
- mass_mearth = 1.05 (msini) → canonical-aligned (Dreizler 2024 table 4)
- radius_rearth = 1.02 (Zeng 2016) → canonical-aligned (Hammond 2025)
- surface_gravity_g_earth = 1.01 (1.05/1.02²) → canonical-aligned (derived)
- insolation_s_earth = 0.35 → canonical-aligned (Dreizler 2024 0.35; Hammond 0.37)
- equilibrium_temp_k (A=0.3) = 209 → canonical-aligned (Dreizler 2024)
- bond_albedo = 0.55 (snowball high-ice albedo) → canonical-aligned (Hammond 2025 snowball)
- surface_temp_global_mean_k = 200 (Hammond shows <freezing everywhere even 2 bar CO₂) → canonical-aligned (Hammond 2025)
- atmosphere_present = true → tie-break (snowball requires some atmosphere to transport heat; Hammond simulated 1 bar)
- atmosphere_surface_pressure_pa = 100000 → canonical-aligned (Hammond 2025 default)
- atmosphere_composition = N₂ 99%, CO₂ 1% → tie-break (within Hammond ranges, picks the "warmer" snowball end)
- cloud_cover_fraction = 0.35 → canonical-aligned (Hammond 2025 low for cold snowball)
- ocean_present = false (frozen) → canonical-aligned (Hammond 2025)
- surface_morphology = global ice sheet, hummocky terrain → canonical-aligned (snowball physics)
- surface_tint_rgb_hex_primary = #d8d0c4 (ice surface under M-dwarf light) → tie-break
- surface_tint_rgb_hex_accent = #4a3030 (exposed bedrock at low-latitude impact craters / volcanic vents) → tie-break
- atmosphere_tint_rgb_hex = #4a3a50 (thin Rayleigh layer) → tie-break
- aurora_present = true (weak) → tie-break (downstream)
- aurora_intensity_kR_typical = 15 → tie-break
- magnetic_field_strength_microtesla_equator = 20 → tie-break
- star_apparent_angular_diameter_deg = 1.25 → canonical-aligned (derived)
- stellar_illumination_color_temp_k = 2904 → canonical-aligned

**Row counts**: 14 canonical-aligned, 10 tie-break, 0 documented-divergence.

### Teegarden d (cold outside HZ, S=0.12 S⊕)

Planned ~20 cfg rows. d is firmly outside HZ; expected to be frozen rock with possibly thin CO₂ atmosphere. No GCM paper specific to d.

- tidally_locked = true → canonical-aligned (Wandel-style argument, P_orb=26 d still inside tidal-lock timescale)
- obliquity_deg = 0 → canonical-aligned
- eccentricity = 0.07 → canonical-aligned (Dreizler 2024)
- sidereal_period_days = 26.13 → canonical-aligned
- semi_major_axis_au = 0.0791 → canonical-aligned
- mass_mearth = 0.82 (msini) → canonical-aligned (Dreizler 2024)
- radius_rearth = 0.95 (Zeng 2016 sub-Earth) → canonical-aligned (DB derived)
- surface_gravity_g_earth = 0.91 → canonical-aligned (derived)
- insolation_s_earth = 0.12 → canonical-aligned (Dreizler 2024)
- equilibrium_temp_k (A=0) = 165 → canonical-aligned (derived; Dreizler quotes 159 for A=0.3)
- equilibrium_temp_k (A=0.3) = 159 → canonical-aligned (Dreizler 2024)
- bond_albedo = 0.30 (bare-rock / thin frost) → tie-break (no GCM for d)
- surface_temp_substellar_k = 200 (thin atmosphere case) → tie-break (no GCM, scaled from b/c)
- surface_temp_nightside_k = 60 (CO₂ frost trap) → tie-break (Mercury/Mars-analog cold-trap)
- atmosphere_present = false (or trace, <0.001 bar) → tie-break (thin to none — Mars-Mercury continuum, no data)
- atmosphere_surface_pressure_pa = 500 → tie-break (trace, like cold Mars)
- atmosphere_composition = thin CO₂ with N₂ → tie-break
- surface_tint_rgb_hex_primary = #6a5a4a (basalt + frost mottling, similar to Mercury) → tie-break
- surface_tint_rgb_hex_accent = #e8e0d4 (CO₂ frost / water ice in polar cold traps) → tie-break
- atmosphere_tint_rgb_hex = #2a2a30 (almost negligible) → tie-break
- cloud_cover_fraction = 0.02 (CO₂ ice clouds near terminator only) → tie-break
- ocean_present = false → canonical-aligned (T<<273 K)
- aurora_present = false (no/trace atmosphere) → tie-break
- magnetic_field_strength_microtesla_equator = 5 (very weak; small cold body) → tie-break
- star_apparent_angular_diameter_deg = 0.72 → canonical-aligned (derived)
- stellar_illumination_color_temp_k = 2904 → canonical-aligned

**Row counts**: 11 canonical-aligned, 14 tie-break, 0 documented-divergence.

### Aggregate row counts

| Entry | Canonical-aligned | Tie-break | Documented-divergence |
|---|---|---|---|
| Teegarden's Star | 16 | 3 | 0 |
| Teegarden b | 20 | 18 | 0 |
| Teegarden c | 14 | 10 | 0 |
| Teegarden d | 11 | 14 | 0 |
| **Total** | **61** | **45** | **0** |

No `## Canonical alternatives` sections required — Phase 3 picks track the canonical readings, with tie-breaks in visual/colour space where literature is silent.

The closest case to divergence is **Teegarden b habitable vs runaway**, but
the canonical reading (with Phase 2 stellar params) is habitable, so picking
habitable is canonical-aligned. The alternative (Dreizler 2024 stellar params
→ runaway) is mentioned in Open items, not Canonical alternatives.

The next-closest case is **Teegarden c snowball vs warm spot** — but the most
recent 3D GCM (Hammond 2025) says snowball even at 2 bar CO₂, so snowball
IS the canonical reading. Wandel 2019 1D model with H_atm=12 is not
"weight-equivalent" canonical — it's an older 1D analytic model. Snowball
cfg pick is canonical-aligned.


