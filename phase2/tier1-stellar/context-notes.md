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

## tau Cet
(next)
