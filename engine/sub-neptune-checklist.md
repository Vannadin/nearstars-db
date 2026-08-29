# Checklist: sub-Neptunes, and the false ceiling refusal under them (C1)

Plan in one line: an iron core under a gas envelope declines with "must exceed fe_prem's
ceiling", which a 5 M⊕ body cannot mean. Reproduce both contradicting measurements, find
the mechanism by instrumenting surface mass against central pressure, fix the root finding
(not a ceiling), then take `sub_neptune` off `FLUID_CLASSES` with `gas_mass_fraction` as a
declared input that drops the grade.

## Reproduce
- [x] the sweep (M 5 · CMF 0.20 · 500 K, gas 100 → 2 %): 100 % solves (converged False), all others decline at the iron ceiling
- [x] the "large rock core in a giant, 17.7 M⊕" row: `test_giant.py` measures **0 M⊕** since the H/He table (2026-08-28); the domain row is the stale one

## Diagnose
- [x] instrument `integrate()` over the whole admissible central-pressure range
- [x] name the mechanism in one sentence (context notes) — the U-shape hypothesis is refuted for this case

## Fix
- [x] `integrate()`: a table-domain exit far above 1 bar is a temperature refusal, not the surface
- [x] every anchor trial path stays untouched (max exit ratio measured 9× against a 100× line)
- [x] refusals cite the state actually reached
- [ ] `sub_neptune` off `FLUID_CLASSES`; `gas_mass_fraction` a declaration (grade, note, chain.yaml)

## Verify
- [x] the sweep solves at every gas fraction, or declines with a mechanism that survives reading aloud
- [x] regression: an iron core under a gas envelope solves; the ladder cannot report a ceiling while a root exists below it
- [x] one published sub-Neptune: sweep gas fraction to its radius, compare with its published range
- [ ] anchors bit-identical (condensed · icy · giant · ice giant)
- [ ] `bash scripts/check.sh` FAIL 0

## Landing
- [x] domain rows: sub-Neptune, large rock core
- [x] `interior-core.md` C1 closed
- [x] Korean mirror- [x]ecklist: sub-Neptunes, and the false ceiling refusal under them (C1)

Plan in one line: an iron core under a gas envelope declines with "must exceed fe_prem's
ceiling", which a 5 M⊕ body cannot mean. Reproduce both contradicting measurements, find
the mechanism by instrumenting surface mass against central pressure, fix the root finding
(not a ceiling), then take `sub_neptune` off `FLUID_CLASSES` with `gas_mass_fraction` as a
declared input that drops the grade.

## Reproduce
- [x] the sweep (M 5 · CMF 0.20 · 500 K, gas 100 → 2 %): 100 % solves (converged False), all others decline at the iron ceiling
- [x] the "large rock core in a giant, 17.7 M⊕" row: `test_giant.py` measures **0 M⊕** since the H/He table (2026-08-28); the domain row is the stale one

## Diagnose
- [x] instrument `integrate()` over the whole admissible central-pressure range
- [x] name the mechanism in one sentence (context notes) — the U-shape hypothesis is refuted for this case

## Fix
- [x] `integrate()`: a table-domain exit far above 1 bar is a temperature refusal, not the surface
- [x] every anchor trial path stays untouched (max exit ratio measured 9× against a 100× line)
- [x] refusals cite the state actually reached
- [ ] `sub_neptune` off `FLUID_CLASSES`; `gas_mass_fraction` a declaration (grade, note, chain.yaml)

## Verify
- [ ] the sweep solves at every gas fraction, or declines with a mechanism that survives reading aloud
- [ ] regression: an iron core under a gas envelope solves; the ladder cannot report a ceiling while a root exists below it
- [ ] one published sub-Neptune: sweep gas fraction to its radius, compare with its published range
- [ ] anchors bit-identical (condensed · icy · giant · ice giant)
- [ ] `bash scripts/check.sh` FAIL 0

## Landing
- [ ] domain rows: sub-Neptune, large rock core
- [ ] `interior-core.md` C1 closed
- [ ] Korean mirror
