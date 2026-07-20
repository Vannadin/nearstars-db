# Luhman 16 AB — Phase 2 context notes

Escalation of the nearest brown-dwarf binary to full literature curation, as the
chosen in-game implementation BD slot. eps Ind B stays Phase 1. Append continuously.

## Source decisions
- **Mass (binary_orbit):** primary = Lazorenko & Sahlmann 2018 (arXiv [1808.07835](https://arxiv.org/abs/1808.07835),
  cache-verified). Reason: longer astrometric baseline (incl. 1984 ESO-R plate),
  and verifiable against the frozen cache — Bedin 2024 ([2403.08865](https://arxiv.org/abs/2403.08865)) is more recent
  but its ar5iv extract is EMPTY (Astron. Nachr., not cacheable). Garcia 2017
  ([1708.02714](https://arxiv.org/abs/1708.02714)) third. Per-component M☉ via /1047.57 (IAU nominal M_Jup).
  L&S 33.51/28.55 MJup; Bedin 35.4/29.4; Garcia 34.2±1.2 / 27.9±1.0. They differ
  ~5% (>error bars) — recorded as alternates, not averaged.
- **Radius:** Phase 1 left null (no measured radius exists). Phase 2 adds the
  evolutionary/assumed 0.9 R_Jup = 0.090 R☉ that Faherty 2014 explicitly adopts
  (Vrba 2004 prescription, line 137 of [1406.1518](https://arxiv.org/abs/1406.1518).md). Labeled evolutionary_model
  with a note that it is the standard field-BD radius assumption, not a measurement.
  Consistent with eps Ind B's King-2010 model radii (~0.08 R☉; Luhman 16 slightly
  larger, consistent with its younger 0.1-3 Gyr age vs eps Ind B's 3.5 Gyr).
- **Teff + luminosity:** Faherty 2014 Table ([1406.1518](https://arxiv.org/abs/1406.1518).md:193). log L/L☉ = -4.67±0.04
  (A), -4.71±0.10 (B); Teff 1310±30 / 1280±75 K (derived from Lbol assuming 0.9 RJup).
- **Age:** 0.1-3 Gyr from Li I detection (both components) + no low-gravity features
  (older than ~120 Myr), Faherty 2014. A genuine constraint but a RANGE, not a point;
  recorded method=unverified with the range in notes (Li-depletion is outside the
  schema age-method whitelist). Low priority per impact order.
- **Activity:** left empty — brown dwarfs at ~1300 K have no chromospheric Ca II H&K
  dynamo, so log R'HK is undefined (same rationale as A-type stars).
- **Rotation:** the key Phase 2 datum for these objects (first BD weather map).
  Delegated to a research agent (Gillon 2013 / Crossfield 2014 / Apai 2021); values
  to be cache-verified before commit. B ~5 hr expected; A weaker constraint.

## Discipline
- Committed `recommended` values value-checked against the frozen _papers cache
  (never agent self-report). New rotation papers pinned in docs/phase3/_bib/luhman-16.yaml.
- Written via apply_phase2.py (canonical writer), never hand json.dump.
