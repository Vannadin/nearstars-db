# HD 219134 — Phase 2 context notes (DRAFT step)

## Scope
DRAFT step only: pin/fetch bibliography, draft curator-input
`measurements.yaml` + evidence. MAIN/human value-checks and applies
(`apply_phase2.py` -> `build_systems.py` -> `validate.py`). No db/*,
target_list, binary_orbits edits; no build/git in this step.

## Pre-research (verified before drafting)
- HD 219134 = HR 8832 = GJ 892 = HIP 114622, K3V, 21.3 ly,
  Gaia DR3 2009481748875806976 (V 5.5, Gaia astrometry OK).
- Effectively single. A V~9.4 M dwarf sits at ~106.6" (~700 AU projected,
  P~20 kyr; Eggleton & Tokovinin 2008, cited in Vogt 2015 line 31).
  -> meta.notes only, NOT a binary_orbits entry.
- DB before this work: mass 0.81 + radius 0.778 method=unverified
  (attributed Gillon 2017); EMPTY teff/L/age/rotation/activity.

## Paper-letter scheme conflict (the crux of provenance)
The planet letters are NOT stable across papers. Period is the only
unambiguous key. Mapping (modern DB/NASA convention <- Vogt 2015 Table 3):

| DB letter | Period (d) | Vogt 2015 letter | Motalebi 2015 letter |
|---|---|---|---|
| b | 3.09  | b | b |
| c | 6.76  | c | c |
| f | 22.8  | **d** | (not in M15) |
| d | 46.7  | **e** | **d** |
| g | 94.2  | **f** | (not in M15) |
| h | 2247  | **g** | **e** (P=1190/1842, poorly constrained) |

Johnson 2016 (line 15) settles the convention: "we will refer to the
outer planet as HD 219134 h rather than e ... as the parameters we
measured ... more closely match the V15 values."

## Provenance findings (re-anchoring the DB)
1. **Radius 0.778 -> 0.726**: DB carried Gillon-2017 unverified 0.778 Rsun.
   Ligi 2019 VEGA/CHARA interferometry gives R = 0.726 +/- 0.014 Rsun
   (theta_LD = 1.035 +/- 0.021 mas). This is the better measurement
   (direct angular diameter) -> recommended. Difference is ~7%/~2.5 sigma.
2. **Mass tiebreak 0.696 vs ~0.78**: Ligi direct mass 0.696 +/- 0.078
   (interferometric R + transit density rho=1.82) vs evolutionary
   0.755-0.810 (Ligi C2kSMO) / 0.78 +/- 0.02 (Motalebi SYCLIST) /
   0.794 (Takeda). Picked Ligi 0.696 recommended (measurement > model),
   recorded method=unverified (no clean enum for "interferometry+transit
   density"), evolutionary 0.78 as alt. Agree within ~1.5 sigma. DB's
   prior 0.81 was the high end of the evolutionary range, unverified.
3. **g/h provenance**: DB already attributes g & h to Vogt 2015 with the
   correct bibcode (2015ApJ...814...12V). The task's "g/h say Gillon but
   bibcode Vogt" did not match the actual DB state. The REAL provenance
   issue is **d & f**: DB lists them as mass_type="true mass" attributed
   to Gillon 2017, but Gillon 2017's abstract reports masses+radii for
   b & c ONLY (the transiting pair). The d=16.17 / f=7.3 "true mass"
   values (with implausibly tiny +/-0.02 radius errors) are NOT in the
   cited Gillon source and ar5iv has no Gillon full text to verify them.
   -> Re-pinned d & f to Vogt 2015 RV Msini (verifiable): f Msini=8.9,
   d Msini=21.3 Mearth. Motalebi 8.67 kept as d alt. The old "true mass"
   d/f values are treated as UNVERIFIED and dropped from the draft.

## Cache caveat (Gillon 2017)
ar5iv has no LaTeX-rendered HTML for 1703.01430; the fetcher saved the
arXiv landing page. The abstract (1703.01430.md:7) carries the b/c mass +
radius + host radius verbatim, which is all that is needed for the
recommended b/c physical entries. d/f/h full-table values are NOT in this
cache, which is why those re-pin to Vogt (full ar5iv text available).

## Contested planets f & g (kept per gameplay-variety policy)
- pl_controv_flag=1 for both; NOT retracted (still in Rosenthal 2021 /
  Harada 2025 per task). Kept and annotated.
- f (22.8d): Johnson 2016 finds a stellar S_HK rotation period of
  22.83 +/- 0.03 d, identical to f's orbital period to 1 sigma -> the RV
  signal "might be caused by stellar magnetic activity" (Johnson line 143).
- The rotation period itself is contested (22.83 vs 42.3 vs ~20 d), which
  feeds the f-controversy. Documented in rotation_measurements notes.

## Rotation decision
No photometric period (Vogt APT flat to ~0.0002 mag). Two activity-index
periods: Johnson 22.83 +/- 0.03 d (S_HK, dedicated analysis, most precise)
vs Motalebi 42.3 d (log R'HK + CCF). Johnson notes 22.83 may be the first
harmonic of ~45 d under differential rotation. Recommended = Johnson 22.83
(precision + dedicated study); 42.3 d kept as documented alt. Both
method=unverified (S_HK/activity-index periodogram is outside the rotation
enum), per the eps Ind A precedent.

## Open items for MAIN/human
- Value-check each recommended value against the cache lines in the
  evidence table before apply.
- Consider filing an archive_issues.md note on the NASA/DB d & f
  "true mass" Gillon attribution (likely a default-flag composite
  mislabel) if escalating to the catalog maintainer.
- After build, copy meta_notes reasoning into the host file's meta.notes
  (build does not propagate notes automatically) and add the wide-M-dwarf
  companion note.
