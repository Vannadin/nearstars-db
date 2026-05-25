# Phase 2 — Schema Expansion Checklist

Started 2026-05-21. Expand Phase 2 coverage from mass + radius only to
the broader observed-fact set (stellar Teff/L/age/[Fe/H]/P_rot/activity,
planet Teq/density, atmospheric retrievals). Prerequisite for Phase 3.

## Discovery (already done before this checklist started)

- [x] Array-form upgrade in `build_systems.py` — `_pick_recommended`
      accepts dict (Phase 1) or list (Phase 2). Confirmed at line 422-423.
- [x] `environment` / `atmosphere` section names already iterated in
      build code (line 722) for source dedup. No schema validation yet.
- [x] `validate_planets_curated` already validates Phase 2 array form
      and enforces ≤1 `recommended: true` per array.

## Schema design memo

- [x] Finalize stellar measurement category names + measurement-object schema
- [x] Finalize planet `environment` + `atmosphere` field set
- [x] Define method whitelist per category (tier order matters — picks `recommended`)
- [x] Decide orbital extension keys (`period_days`, `tperi_bjd`, `tranmid_bjd`)

## schema.py edits

- [x] `STELLAR_PROPS_REQUIRED` / `STELLAR_PROPS_OPTIONAL` — add 6 new measurement keys
- [x] Per-category method whitelist constants (`STELLAR_TEFF_METHODS` etc.)
- [x] `validate_stellar_props_curated` (or whatever the entry point is) — extend
- [x] `PLANET_CURATED_OPTIONAL` — add `environment`, `atmosphere`
- [x] `PLANET_ORBITAL_ALLOWED` — add `period_days`, `tperi_bjd`, `tranmid_bjd`
- [x] Define `PLANET_ENVIRONMENT_ALLOWED`, `PLANET_ATMOSPHERE_ALLOWED`
- [x] Method whitelists for environment + atmosphere

## build_systems.py edits

- [x] Star `derived` — add `teff_k`, `luminosity_lsun`, `age_gyr`,
      `metallicity_fe_h`, `rotation_period_d`, `activity_log_rhk`
- [x] Planet `derived` — add `equilibrium_temperature_k`, `density_g_cc`
- [x] `_pick_recommended` reuse for each new array category

## TRAPPIST-1 example data

- [x] `stellar_props_curated[TRAPPIST-1]` — add `teff_measurements`
      (Gillon 2017 / Agol 2021), `luminosity_measurements` (Van Grootel 2018),
      `age_measurements` (Burgasser & Mamajek 2017)
- [x] `planets_curated[TRAPPIST-1]` b–h — add `environment.equilibrium_temperature_k`
      (Agol 2021 reports each planet's Teq)
- [x] At least one planet — add `atmosphere` block (TRAPPIST-1b/c have
      JWST emission spectra; Greene 2023, Zieba 2023)

## Verification

- [x] `python3 scripts/pipeline/validate.py` → FAIL: 0
- [x] `python3 scripts/pipeline/build_systems.py` → no error
- [x] `db/systems/trappist_1.json` — new derived fields present for star + planets
- [x] Existing systems regression check — `git diff db/systems/*.json` 만 새 필드 추가만 변경, 기존 값 변동 없음

## Out of scope (follow-up)

- Visualization (`docs/phase2-trappist-1.html`) update to display new fields
- Populating other Phase 2 systems (33-system list) — separate batch task
- Atmospheric retrieval fields beyond detection presence — keep minimal until Phase 3 needs surface

## Related

- [methodology hub](../../docs/reference/methodology.md) — parent topic this workspace contributes to
