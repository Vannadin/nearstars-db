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

## AU Mic (DONE 2026-05-30)
- First M-dwarf host. Radius = the contested category. The famous 0.75 Rsun is
  White et al. 2019 -- an UNREFEREED AAS conference abstract (no journal, no
  arXiv). Only refereed interferometric radius is Gallenne 2022 VLTI/PIONIER
  (cache-verified: theta_LD 0.825 +/- 0.033stat +/- 0.038sys -> R 0.862 +/- 0.052).
  Recommended Gallenne per contract; kept White 0.75 + Donati 0.82 as alts so the
  divergence is on the record. Fame-trap avoided (cf. Boyajian/eps Eri).
- Mass divergence: Plavchan 2020 0.50 (community standard, Klein 2021 Table
  cache-verified "M_S 0.50+/-0.03 P20") recommended over Donati 2023 0.60.
- Teff/[M/H] = Cristofari 2023 SPIRou (cache: Teff 3665+/-31, [M/H] +0.12+/-0.10,
  [alpha/Fe] 0 -> [M/H]~[Fe/H]). L = Donati 2023 logL -0.99 (cache, Table) -> 0.102.
- Age = Mamajek & Bell 2014 BPMG 23+/-3 Myr (cache: isochrone 22+/-3 + LDB; 12 Myr
  kinematic explicitly rejected). Association-membership age, the right anchor type.
- Rotation = Plavchan 2020 TESS 4.86 d (Klein Table cache-verified). Activity =
  Tsikoudi & Kellett 2000 ROSAT Lx 2.24e29 -> log(Lx/Lbol)~-3.2 (near saturation).
  Magnetic <B> 2.61 kG (Donati 2023) noted in meta_notes for the Phase 3 magnetic
  axis (not a stellar_props category).
- Plavchan 2020 .md extracted as 1 line (Nature arXiv abstract-only) -> verified
  its values via the Klein 2021 Table cache instead (which attributes them to P20).

## BUILD GOTCHA (2026-05-30): date-stamp churn
- build_systems.py line 25 stamps RETRIEVAL_DATE = date.today() into EVERY system
  file. When the calendar day rolls over, a rebuild rewrites all 151 files with
  only the new "accessed"/"retrieval_date" -- NOT a content change. Confirmed via
  `git diff -- db/systems ':(exclude)...au_mic.json'` filtered of date lines = empty.
- Per-host discipline: stage ONLY the target host's system file, then
  `git restore --worktree -- db/systems/ ':(exclude)db/systems/<host>.json'` to
  drop the date churn. Do NOT git-add the 150 date-only files.

## HD 69830 (DONE 2026-05-30)
- Cleanest host yet: ONE dedicated paper (Tanner et al. 2015, cached 1412.5251)
  anchors 6 of 7 categories, all cache-text-verified from its Table 2 + abstract:
  theta_LD 0.674 -> R 0.9058, L 0.622 (SED), Teff 5394 (CHARA+SED) / 5385 (SME),
  M 0.863 (Y2), [Fe/H] -0.04 (SME), v sin i 0.8, age 10.6 (HRD) / 7.5 (SME).
- No asteroseismology exists (verified). Recommended mass = Tanner isochrone (no
  better method available for this star).
- Age: recommended Tanner's SME-isochrone 7.5+/-3 (the more precise of their two)
  + Mamajek activity-age 5.9 alt; 10.6 HRD in meta_notes. Tanner explicitly says
  all methods (incl. Mamajek 5.7-6.1 activity/gyro) agree it is OLD, ruling out
  the old Song 2000 "young" claim -> relevant to the asteroid belt being
  non-primordial. Unlike eps Eri/tau Cet the age methods broadly AGREE (~6-10 Gyr).
- Activity = GdS 2021 logR'HK -4.999 wmean (VizieR recno 1388, 711 obs; -5.013 med).
- ROTATION: no measured period (same as tau Cet pattern) -> 7 categories not 8.
  v sin i 0.8 + CHES empirical 41.7 d noted in meta_notes only.
- This is the model case for "interferometry + SED + SME single-paper anchor".

## 61 Vir (DONE 2026-05-30)
- Twin of the HD 69830 pattern: single dedicated interferometric paper (von Braun
  et al. 2014, cached 1312.1792) anchors R/Teff/L/mass/age, all cache-verified
  from its Tables 2/3/4: theta_LD 1.073 -> R 0.9867, F_bol 36.06e-8 -> Teff 5538 +
  L 0.8222, Y2 -> mass 0.93 / age 8.6.
- No asteroseismology (verified). Boyajian 2012/2013 do NOT contain 61 Vir
  (verified) -- von Braun is the sole interferometric source.
- [Fe/H] = Santos/Sousa 2013 -0.01 (GdS VizieR recno 21, near-solar); activity =
  GdS 2021 logR'HK -5.013 (1251 obs, cache-verified row) + Mamajek -5.001.
- Rotation = Baliunas 1996 29 d (Ca II HK, no arXiv; Wright 2011 compiles, Vogt
  2010 adopts) -> recorded photometric_variability. UNLIKE HD 69830/tau Cet, this
  host HAS a measured period -> full 8 categories.
- Age divergence (all old ~6-9 Gyr): recommended GdS 7.69+/-1.44 (clean error,
  brackets the spread) over von Braun isochrone 8.6 / Mamajek activity 6.4.
- GIT GOTCHA repeat: after build_systems, `git add` then the date-churn
  `git restore` -- but verify staging with `git status --porcelain` before commit;
  the restore step can leave the target file unstaged (' M' = worktree-only). Just
  re-add before committing.

## Vega (DONE 2026-05-30)
- First A-star. Gravity-darkened pole-on rapid rotator -> polar/equatorial Teff/R
  differ; a single value is an approximation. Anchored on Monnier 2012 (cached
  1211.6055), chosen over the research-suggested Yoon 2010 BECAUSE Yoon has no
  arXiv (IOP only, uncacheable) and Monnier is the most recent revision + fully
  cache-verifiable. Discipline > recency-of-the-headline-number.
- Monnier Table 2 cache-verified (body for mass/age/Z/rotation; HTML for the
  Table 2 R/Teff/L numbers, same ar5iv-table-not-in-text issue as Baines/von
  Braun): R_pol 2.418 / R_eq 2.726, T_pol 10070 / T_eq 8910 / mean 9360, L_bol
  47.2 (apparent 58.4), mass 2.15, age 700 Myr, P 0.71 d, beta 0.231.
- Recorded: radius = equatorial 2.726 (rec) + polar 2.418 (alt, emit_source false);
  Teff = mean 9360 (rec, polar/eq in meta_notes); L = bolometric 47.2 (rec) +
  Aufdenberg 37 (alt); age = Monnier 0.70 (rec) + Yoon 0.455 (alt, DIVERGENCE
  455-700 Myr); [Fe/H] -0.5 (lambda Boo, Yoon); rotation 0.71 d (Petit 2010 ZDI).
- ACTIVITY left EMPTY by design: log R'HK is not defined for A0 V (no convective
  dynamo). X-ray non-detection (Pease 2006) noted in meta_notes only. So Vega has
  7 categories -- the missing one is physically correct, not a gap.
- SCHEMA GOTCHA: age method 'evolutionary_model' is NOT in the age whitelist
  (only activity_age/asteroseismology/gyrochronology/isochrone/kinematic/
  unverified). Rotating evolutionary tracks (Geneva/BASTI) -> use method
  'isochrone'. Caught by validate.py (FAIL 2), fixed.

## Fomalhaut (DONE 2026-05-30)
- Single-anchor Mamajek 2012 (cached 1206.6353) for mass/R/Teff/L/age, all
  cache-verified (text + Table 2): mass 1.92, R 1.842, Teff 8590, L 16.63, age
  440 Myr. Radius/Teff use Absil 2009 (cached 0908.3133) excess-corrected theta_LD
  2.223 mas -> fixed the existing DB radius attribution (was wrongly credited to
  Di Folco 2004; the 1.842 value is Mamajek's derived R).
- Radius/Teff DIVERGENCE: Davis 2005 (no arXiv) R 1.744 / Teff 8819 (uncorrected
  for circumstellar excess) -- documented, Absil/Mamajek preferred.
- [Fe/H] = Dunkin 1997 -0.03 (near-solar; A-star spectroscopic [Fe/H] scattered,
  Mamajek assumes protosolar). Rotation: only v sin i ~93 km/s -> not recorded
  (the 10.3 d is the K-dwarf companion). Activity: none (A star). 6 categories.
- Unlike Vega, Fomalhaut is a NORMAL A-rotator (mild gravity darkening) so single
  Teff/R are fine.

## CAMPAIGN COMPLETE (2026-05-30) -- all 7 Tier 1 hosts done
- Pattern that worked: per host, one research subagent gathers candidate anchors
  (bibcode+arxiv_id+value+location) -> main thread pins bib, fetches to cache,
  value-checks every recommended number against the cached text or the named
  VizieR catalog row -> writes the 8-category entry with documented divergences
  -> schema gate -> build_systems (revert date-churn) -> one commit.
- Recurring science patterns: (1) interferometry+SED single-paper anchors are the
  cleanest (HD 69830/Tanner, 61 Vir/von Braun, Fomalhaut/Mamajek). (2) Age is the
  usual divergence -> pick the method consistent with activity+rotation (young for
  active eps Eri/AU Mic, old for inactive tau Cet/HD 69830/61 Vir). (3) A-stars
  (Vega, Fomalhaut) have NO log R'HK by physics -> activity left empty, correct.
  (4) Catalog/survey papers carry per-star values in VizieR, not the ar5iv body.
  (5) Fame-traps avoided: Boyajian 2012 lacks eps Eri & 61 Vir; Suarez Mascareno
  lacks tau Cet; NEXXUS lacks AU Mic; White 2019 (AU Mic R) is an unrefereed AAS
  abstract. (6) build_systems date-stamp churns all 151 files on a day rollover --
  stage only the target, restore the rest.
- Schema reminders learned: age method has NO 'evolutionary_model' (use isochrone);
  rotation has no km/s value key (v sin i only -> don't record a period).
