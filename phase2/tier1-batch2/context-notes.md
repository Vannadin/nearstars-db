# Context notes — Tier 1 Batch 2 (Barnard + Teegarden)

Fresh build. Prep dirs quarantined (blind oracle, diff at end). All values below are
CACHE-VERIFIED on the main thread (line citations into docs/phase3/_papers/<id>.md).

## Barnard's Star — VERIFIED Phase 2 spec (key "Barnard's star", slug barnards-star)

Anchors (all CACHED): ESPRESSO 2024 = 2410.00569 (A&A 690 A79, González Hernández;
doi 10.1051/0004-6361/202451311) · Schweitzer 2019 = 1904.03231 (A&A 625 A68;
doi 10.1051/0004-6361/201834965) · Marfil 2021 = 2110.07329 (A&A 656 A162;
doi 10.1051/0004-6361/202141980) · Jahandar 2023 = 2310.12125 (ApJ; SPIRou) ·
Toledo-Padrón 2019 = 1812.06712 (MNRAS 488 5145; doi 10.1093/mnras/stz1647) ·
Mann 2015 = 1501.01635 (ApJ 804 64) · Boyajian 2012b = 1208.2431 (ApJ 757 112) ·
Ribas 2018 = Nature 563 365 (arXiv 1811.05955; cache is a 1-line stub).

| category | recommended value | method | reference | bibcode | cache evidence |
|---|---|---|---|---|---|
| mass | 0.162 ± 0.007 Msun | spectroscopic_calibration | Schweitzer et al. 2019 | 2019A&A...625A..68S | ESPRESSO 2410.00569 line 86 (=Schweitzer weighted mean of 3 dets) |
| mass (alt) | 0.161 ± 0.006 | empirical_relation | Mann et al. 2015 | 2015ApJ...804...64M | DB anchor; M_K relation |
| radius | 0.187 ± 0.001 Rsun | interferometry | Schweitzer et al. 2019 | 2019A&A...625A..68S | Schweitzer 1904.03231 line 75 (R_interf via Boyajian 2012b θ_LD=0.952 mas + Gaia DR2 d=1.8267 pc); ESPRESSO line 88. angular_diameter_mas=0.952, note Boyajian 2012b θ_LD |
| teff | 3195 ± 28 K | high_res_spectroscopy | González Hernández et al. 2024 | 2024A&A...690A..79G | ESPRESSO 2410.00569 line 81 (SteParSyn on ESPRESSO master) |
| teff (alt) | 3273±51 Schweitzer / 3254±32 Marfil / 3231±21 Jahandar | high_res_spectroscopy | (resp.) | | ESPRESSO line 116 |
| luminosity | 0.003558 ± 0.000072 Lsun | bolometric_flux | Schweitzer et al. 2019 | 2019A&A...625A..68S | ESPRESSO line 80, 118 (L*=3.558±0.072 ×10⁻³ Lsun) |
| metallicity | -0.39 ± 0.03 dex | high_res_spectroscopy | Jahandar et al. 2023 | 2023ApJ...... | ESPRESSO line 116 (SPIRou, NIR, most precise) — DIVERGENT |
| metallicity (alt) | -0.15±0.16 Schweitzer / -0.57±0.10 Marfil | high_res_spectroscopy | (resp.) | | ESPRESSO line 116 — documented divergence (~0.4 dex spread) |
| rotation | 145 ± 15 d | photometric_variability | Toledo-Padrón et al. 2019 | 2019MNRAS.488.5145T | 1812.06712 line 35 (Table 1) + abstract (photometry supports) |
| rotation (alt) | 152₋₁₄⁺¹⁷ (ESPRESSO GP) / 136±16 (Donati 2023 ZDI) | | | | ESPRESSO line 263 |
| activity | log R'HK = -5.82 ± 0.08 | log_rhk | Toledo-Padrón et al. 2019 | 2019MNRAS.488.5145T | 1812.06712 line 339 (own Smw measurement) + line 34. cycle ~3226 d / 10±2 yr |
| age | 8.5 ± 1.5 Gyr (range 7–10) | kinematic | Ribas et al. 2018 | 2018Natur.563..365R | value-checked via Toledo-Padrón 1812.06712 line 13 ("age 7–10 Gyr (Ribas 2018)"); old intermediate-Pop-II, high space velocity |

teff_k top-level: keep but update? Currently 3278. Recommended teff is now 3195 (ESPRESSO).
spectype: M4.0 Ve (keep; ESPRESSO says M3.5–M4).

### Divergences to flag in Phase 3 (## Canonical alternatives)
- metallicity: -0.15 (Schweitzer/Passegger VIS) vs -0.39 (Jahandar SPIRou NIR) vs -0.57
  (Marfil VIS+NIR). NIR favored for cool M dwarfs → recommended -0.39. cfg [Fe/H] sensitive.
- teff: 3195–3273 spread (~80 K) across spectroscopic determinations.

### ⚠ Prep-diff flag (caught during verification, BEFORE reading prep)
Current committed DB radius = 0.1868 ± 0.0011, method=interferometry, "Rains et al. 2021,
2021MNRAS.504.5788R". That bibcode = "Characterization of 92 southern TESS candidate planet
hosts" (Rains 2021, southern + spectroscopic/photometric, NOT interferometry, NOT Barnard).
MISATTRIBUTION. Correct interferometric source = Schweitzer 2019 R_interf 0.187±0.001
(Boyajian 2012b θ_LD). Replaced in fresh build. Mann 2015 mass anchor is fine.

## Teegarden's Star — TODO (agent value-check pending)
Current DB: mass 0.097±0.01, radius 0.12±0.012, both Dreizler 2024 method=unverified.
