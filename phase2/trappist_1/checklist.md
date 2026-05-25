# TRAPPIST-1 — Phase 2 Curation Checklist

Sample run for the 33-system Phase 2 escalation (started 2026-05-20).
Verifies that the array-form schema, build extension, and validate
pipeline all work end-to-end before extending to other systems.

## Host star (M7.5 V)

NASA Archive `ps` table gave 9 distinct stellar papers for TRAPPIST-1.
Curate them into `db/stellar_props_curated.json` arrays.

### mass_measurements

- [x] Gillon 2016  — 2016Natur.533..221G — M = 0.08 ± 0.009 — evolutionary_model
- [x] Gillon 2017  — 2017Natur.542..456G — M = 0.0802 ± 0.0073 — evolutionary_model
- [x] Grimm 2018   — 2018A&A...613A..68G — M = 0.089 ± 0.007 — evolutionary_model (TTV-constrained)
- [x] Van Grootel 2018 — 2018ApJ...853...30V — M = 0.089 ± 0.006 — evolutionary_model
- [x] Stassun 2019 — 2019AJ....158..138S — M = 0.0908 ± 0.020 — spectroscopic_calibration
- [x] Agol 2021    — 2021PSJ.....2....1A — M = 0.0898 ± 0.0023 — evolutionary_model **(recommended)**

### radius_measurements

- [x] Gillon 2016  — 2016Natur.533..221G — R = 0.117 ± 0.004 — sed_fitting
- [x] Gillon 2017  — 2017Natur.542..456G — R = 0.117 ± 0.0036 — sed_fitting
- [x] Stassun 2019 — 2019AJ....158..138S — R = 0.1148 ± 0.0034 — interferometry (Gaia distance + SED)
- [x] Ducrot 2020  — 2020A&A...640A.112D — R = 0.1234 ± 0.0033 — sed_fitting (Spitzer)
- [x] Agol 2021    — 2021PSJ.....2....1A — R = 0.1192 ± 0.0013 — sed_fitting **(recommended)**

## Planets (7) — Phase 2 array form

Each planet gets `physical` array of mass/radius measurements (paper-attributed),
with `recommended: true` for the best TTV (Agol 2021). `orbital` stays single-dict
(Phase 1) since orbital elements have minor inter-paper variation and the Agol 2021
fit is canonical.

Method labels:
- `ttv`     — TTV-derived dynamical mass (Gillon 2017, Grimm 2018, Agol 2021)
- `transit` — transit-only radius (no mass)
- `discovery` — initial detection with rough estimates

### TRAPPIST-1 b
- [x] Gillon 2017  — 2017Natur.542..456G — M=0.85, R=1.086 — ttv
- [x] Grimm 2018   — 2018A&A...613A..68G — M=1.017, R=1.121 — ttv
- [x] Agol 2021    — 2021PSJ.....2....1A — M=1.374 ± 0.069, R=1.116 ± 0.014 — ttv **(recommended)**

### TRAPPIST-1 c
- [x] Gillon 2017  — M=1.38, R=1.056 — ttv
- [x] Grimm 2018   — M=1.156, R=1.095 — ttv
- [x] Agol 2021    — M=1.308 ± 0.056, R=1.097 ± 0.014 — ttv **(recommended)**

### TRAPPIST-1 d
- [x] Gillon 2017  — M=0.41, R=0.772 — ttv
- [x] Grimm 2018   — M=0.297, R=0.784 — ttv
- [x] Agol 2021    — M=0.388 ± 0.012, R=0.788 ± 0.011 — ttv **(recommended)**

### TRAPPIST-1 e
- [x] Gillon 2017  — M=0.62, R=0.918 — ttv
- [x] Grimm 2018   — M=0.772, R=0.910 — ttv
- [x] Agol 2021    — M=0.692 ± 0.022, R=0.920 ± 0.013 — ttv **(recommended)**

### TRAPPIST-1 f
- [x] Gillon 2017  — M=0.68, R=1.045 — ttv
- [x] Grimm 2018   — M=0.934, R=1.046 — ttv
- [x] Agol 2021    — M=1.039 ± 0.031, R=1.045 ± 0.013 — ttv **(recommended)**

### TRAPPIST-1 g
- [x] Gillon 2017  — M=1.34, R=1.127 — ttv
- [x] Grimm 2018   — M=1.148, R=1.148 — ttv
- [x] Agol 2021    — M=1.321 ± 0.038, R=1.129 ± 0.015 — ttv **(recommended)**

### TRAPPIST-1 h
- [x] Gillon 2017  — R=0.755 only — discovery
- [x] Luger 2017   — 2017NatAs...1E.129L — R=0.752 — discovery (confirmed h)
- [x] Grimm 2018   — M=0.331, R=0.773 — ttv
- [x] Agol 2021    — M=0.326 ± 0.020, R=0.755 ± 0.014 — ttv **(recommended)**

## Pipeline

- [x] Extend `build_planet_derived` for array form (completed 2026-05-20)
- [x] Extend `schema.py:validate_planets_curated` for array form (completed 2026-05-20)
- [ ] Edit `db/stellar_props_curated.json` — TRAPPIST-1 mass/radius arrays
- [ ] Edit `db/planets_curated.json` — 7 planets, `physical` → array form
- [ ] Run `python3 scripts/pipeline/build_systems.py`
- [ ] Run `python3 scripts/pipeline/validate.py` — FAIL=0 expected
- [ ] Verify `db/systems/trappist_1.json` derived values match Agol 2021
- [ ] Commit: "Phase 2: TRAPPIST-1 — 11 stellar / 24 planetary measurements"

## Open questions

- Stellar mass method for Grimm 2018 / Agol 2021: TTV-constrained but not in
  STELLAR_ALLOWED_METHODS (whitelist lacks `dynamical`). Decided to label
  `evolutionary_model` since both papers cite Van Grootel 2018 evolutionary
  models as their stellar prior, with TTV providing only cross-check.

## Related

- [system-trappist-1 entity pages](../../docs/phase3/trappist-1-e.md) — parent topic this workspace contributes to
