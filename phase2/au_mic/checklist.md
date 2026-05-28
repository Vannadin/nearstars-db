# Checklist — AU Mic Phase 2 full curation + Phase 3 reconciliation

Mirrors Delta Pavonis 4d26495 deliverable shape.

## Phase 2 — db/stellar_props_curated.json

- [ ] Append `"AU Mic": {...}` entry (alphabetical/group placement: end of file, after `Delta Pavonis`)
- [ ] top-level: spectype, spectype_bibcode, spectype_reference, teff_k, teff_bibcode
- [ ] 8 measurement arrays, each ≥1 entry with recommended=true (or empty + meta_notes reason):
  - [ ] mass_measurements — Wittrock 2023 TTV/N-body recommended
  - [ ] radius_measurements — Donati 2023 ZDI recommended
  - [ ] teff_measurements — Plavchan 2020 recommended
  - [ ] luminosity_measurements — Plavchan 2020 recommended (0.09 L☉)
  - [ ] age_measurements — Mamajek & Bell 2014 (β Pic MG, 22 ± 3 Myr) recommended
  - [ ] metallicity_measurements — Shkolnik 2017 / β Pic MG mean (calibration tier)
  - [ ] rotation_measurements — Plavchan 2020 (TESS 4.863 d) recommended
  - [ ] activity_measurements — Hα or Stelzer 2013 X-ray for young saturated dwarf
- [ ] meta_notes describing: young saturated activity regime, no direct CHARA radius, Phase 3 used different metallicity (+0.12 calibration vs MG mean), choice of Hα over log R'HK

## Phase 3 reconciliation — docs

- [ ] docs/phase3/au-mic.md — update Decisions table rows: mass/radius/Teff/L/[Fe/H]/age/rotation/log_rhk/stellar_color_temp to track Phase 2 picks (where they differ); add reconciliation language
- [ ] docs/phase3/au-mic-b.md — stellar value references (M=0.51, R=0.82, L=0.092, age=22 Myr) — light touch, only where they cite specific Phase 2 numbers
- [ ] docs/phase3/au-mic-c.md — same
- [ ] docs/phase3/au-mic-d.md — same
- [ ] docs/phase3/au-mic-e.md — same
- [ ] Bibliography section: add Wittrock 2023 + Plavchan 2020 + Donati 2023 explicitly as Phase 2 primary anchors

## Korean mirrors

- [ ] ko/docs/phase3/au-mic.md — match every English block; natural Korean prose
- [ ] ko/docs/phase3/au-mic-b.md, -c, -d, -e — match
- [ ] block parity check passes

## Build + verify

- [ ] python3 scripts/pipeline/build_systems.py
- [ ] python3 scripts/pipeline/build_site.py
- [ ] python3 scripts/pipeline/build_phase2_html.py
- [ ] python3 scripts/pipeline/build_reports_index.py
- [ ] python3 scripts/phase3/check_block_parity.py au-mic (+ b/c/d/e)
- [ ] python3 scripts/phase3/build_html.py au-mic (+ b/c/d/e)
- [ ] python3 scripts/pipeline/validate.py — FAIL=0
- [ ] ./scripts/check.sh — exit 0

## Commit

- [ ] semantic commit with English subject + body
