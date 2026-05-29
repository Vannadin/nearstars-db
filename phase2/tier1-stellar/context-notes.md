# Context notes — Tier 1 stellar Phase 2 campaign

Decisions + reasoning, appended continuously. Newest at the bottom of each host
section.

## Campaign-level decisions (2026-05-29)
- Scope = Phase 2 stellar DB layer (8 categories) per host. NOT a full Phase 3
  md re-synthesis (that is the downstream step, tracked separately). Rationale:
  the checklist REMAINING block defines Tier 1 as "build Phase 2 STELLAR
  measurements"; the inversion is fixed once the measured layer exists.
- Research division of labor: a single research subagent per host gathers
  candidate anchors (bibcode + arxiv_id + reported value + table/section), then
  the main thread fetches to cache and value-checks each recommended number
  against the cached text. The subagent never writes DB values directly — this
  keeps the value-check gate in one deterministic place (the cache), avoiding the
  "different subagents, different papers/values" divergence that caused the
  rollback.
- Method-priority for recommended pick (per category):
  - radius/teff: direct interferometry (theta_LD + Fbol) > asteroseismology > SED
  - mass: binary_orbit > asteroseismology > evolutionary_model > empirical_relation
  - luminosity: bolometric_flux > SED > photometric
  - [Fe/H]: high_res_spectroscopy
  - age: prefer the method consistent with activity+rotation; document divergence
  - rotation: photometric_variability (measured period) > v sin i (upper bound only)
  - activity: log R'HK primary; X-ray as secondary entry

## eps Eri (DONE 2026-05-29)
- Anchor = Baines & Armstrong 2012 (2012ApJ...744..138B; arXiv 1112.0447 is the
  full ar5iv text). Cache-verified in body/Table 3: theta_LD 2.153+/-0.028 mas,
  R 0.74+/-0.01, Teff 5039+/-126 (theta_LD + Fbol), L 0.32+/-0.03, M 0.82+/-0.05
  (Y^2 isochrone), age ~1 Gyr (isochrone, authors disclaim). 4 categories from
  one bulletproof source.
- [Fe/H] = Santos 2004 -0.13+/-0.04 — TEXT-confirmed (the paper body has the
  HD 22049 table row, not just VizieR). Recommended over Sousa 2008 (-0.11,
  VizieR-only) precisely because it is cache-text-verifiable.
- Activity = Gomes da Silva 2021 logR'HK -4.4960 — VizieR row J/A+A/646/A77 (eps
  Eri recno 52, 553 spectra). The paper body is methodology only; per-star value
  lives in the catalog. X-ray = Coffaro 2020 Lx ~2e28 erg/s (body-confirmed);
  log(Lx/Lbol) ~ -4.8 derived with Baines L (documented in meta_notes).
- Rotation = Croll 2006 MOST (no arXiv); Froehlich 2007 (cached, arXiv 0711.0806)
  reanalysis TABLE-confirms P1=11.348, P2=11.553 d, k~0.09, P_eq~11.2. Recorded
  11.45+/-0.2 bracketing the two spots.
- AGE = documented divergence. Recommended the YOUNG branch (Barnes 2007 gyro
  0.44 Gyr, adopted by cache-verified Coffaro 2020) over isochrone (~1-4.8 Gyr),
  applying the delta-Pav principle: pick the age method consistent with the
  measured activity + rotation. For an active 11 d K dwarf that is the young age.
- METHOD LESSON: catalog/survey papers (Sousa, Gomes da Silva, Mamajek, VF2005)
  carry per-star values in VizieR, NOT in the ar5iv body — value-check those
  against the named VizieR catalog by object id (deterministic), as delta Pav did
  for Henry/Huensch. Single-object papers (Baines, Coffaro, Froehlich) and Santos
  2004 (has the row in-text) are body-verifiable. Boyajian 2012 does NOT contain
  eps Eri (verified) -- a fame trap avoided.
- build_systems.py rebuilt; only eps_eri.json changed (deterministic). The 6
  empty Phase-1 categories are now populated -> inversion fixed.

## tau Cet (DONE 2026-05-29)
- Radius was already settled (Korolik 2023 CHARA/MIRC-X, kept). Filled the other
  7; replaced the Phase-1 "unverified" Feng 2017 mass label.
- Mass + L = Teixeira 2009 (cached 0811.3989, TEXT-verified): "the mean density
  gives a mass of 0.783 +/- 0.012 Msun", "derive a luminosity of 0.488 +/- 0.010
  Lsun". Mass method = asteroseismology (mean density + interferometric R). L
  method = photometric (M_V + BC), the cleanest cited L since Korolik reports none.
- Teff: Korolik 2023 (cached 2307.10394) gives BOTH — interferometric 5370 +/- 20
  (theta_LD + Boyajian Fbol, text §3.2) and spectroscopic 5320 +/- 40 (their
  Table 1 adopted). Recommended the interferometric per contract method-priority;
  documented the split. Santos 2013 5310 +/- 17 (GdS VizieR row) as 3rd alt.
- [Fe/H] = Santos 2013 -0.52 +/- 0.01 (GdS VizieR row r_Teff=2013A&A...556A.150S,
  confirmed). Bruntt 2010 -0.18 (cached 1002.4268, table-verified) kept as the
  alpha-enhanced outlier alt.
- Activity = Gomes da Silva 2021 logR'HK -4.977 (VizieR row recno 101); Mamajek
  2008 -4.958 (VizieR table13 recno 15, confirmed) corroborates.
- AGE divergence: recommended the OLD isochrone (Di Folco 2004 ~10 Gyr, adopted by
  Korolik Table 1) over Mamajek activity-age 5.8 Gyr -- same delta-Pav principle,
  opposite direction from eps Eri: tau Cet is very inactive + slow, so the old
  age is the activity-consistent one. Range 4.4-12.4 Gyr noted.
- ROTATION: no direct photometric period exists (pole-on, inactive). Korolik
  gyrochronology 46 +/- 4 d recorded with method=unverified (honest; gyro is not
  in the rotation method whitelist). Baliunas 1996 ~34 d noted. Suarez Mascareno
  2015/2016 do NOT contain tau Cet (fame-trap avoided, like Boyajian/eps Eri).
- GdS isochrone age 0.028 Gyr is a metal-poor-star fit failure -> rejected (same
  catalog-isochrone-unreliable pattern seen for eps Eri's 4.8 Gyr).

## AU Mic
(next -- M1 Ve, young ~22 Myr Beta Pic MG, flare star; expect rotation + flares
well-measured, age from moving-group membership, very different regime from FGK)
