# 61 Vir Phase 2 full curation + Phase 3 reconciliation — checklist

Started 2026-05-28. Worktree branch `worktree-agent-a5a1b84355a4ac1b7`.
Following the Delta Pavonis template (commit `4d26495`).

## Stage 0 — research

- [x] Read CLAUDE.md, `4d26495` diff, schema.py, existing 61-vir docs
- [x] Pre-existing `phase3/61_vir/` notes reviewed (host star + planets)
- [x] NEA stellar-hosts TAP query for 61 Vir paper inventory
- [x] Wikipedia 61 Vir for canonical recent picks (Rathsam 2023, Yu 2024)
- [x] Confirmed von Braun 2014 has CHARA interferometric R for 61 Vir

## Stage 1 — Phase 2 curation (db/stellar_props_curated.json)

- [ ] In-place enrichment of existing "61 Vir" stub (line 2343)
- [ ] 8 categories filled: mass / radius / teff / luminosity / age /
      metallicity / rotation / activity
- [ ] Top-level: spectype, teff_k, teff_bibcode, spectype_bibcode,
      spectype_reference, meta_notes

Picks:
- mass: 0.93 ± 0.01 (Rathsam 2023 evolutionary)
- radius: 0.9867 ± 0.0048 (von Braun 2014 CHARA interferometry)
- teff: 5568 ± 4 K (Rathsam 2023 high-res spec)
- L: 0.8222 ± 0.0033 (von Braun 2014 bolometric)
- age: 7.70 +0.28/-0.26 Gyr (Rathsam 2023 isochrone)
- [Fe/H]: +0.006 ± 0.004 (Rathsam 2023)
- P_rot: 32.1 ± 0.2 d (Yu 2024 GP HARPS)
- log R'HK: -5.0 (Isaacson & Fischer 2010)

## Stage 2 — Phase 3 reconciliation (English docs)

- [ ] `docs/phase3/61-vir.md` — Decisions table stellar rows updated
- [ ] Two divergent rows reconciled:
      * radius 0.963 → 0.9867 (Vogt 2010 evolutionary, mistakenly
        called interferometric, → von Braun 2014 actual CHARA)
      * age 6.1 ± 1.7 → 7.70 +0.28/-0.26
      * Teff 5552 (Gaia DR3 photometric) → 5568 ± 4 (Rathsam high-res)
      * P_rot 29 → 32.1 (Yu 2024 direct)
- [ ] Bibliography expanded: Rathsam 2023, Yu 2024, von Braun 2014
      as primary refs; demote Mamajek 2008 to cross-check
- [ ] Planet pages (b, c, d): update stellar-context rows where they
      cite host parameters (insolation derivations etc.)

## Stage 3 — Korean mirror

- [ ] `ko/docs/phase3/61-vir.md` block parity
- [ ] `ko/docs/phase3/61-vir-b/c/d.md` updated parallel

## Stage 4 — Rebuild artifacts

- [ ] `python3 scripts/pipeline/build_systems.py`
- [ ] `python3 scripts/pipeline/build_site.py`
- [ ] `python3 scripts/pipeline/build_phase2_html.py`
- [ ] `python3 scripts/pipeline/build_reports_index.py`
- [ ] `python3 scripts/phase3/check_block_parity.py 61-vir / -b / -c / -d`
- [ ] `python3 scripts/phase3/build_html.py 61-vir / -b / -c / -d`
- [ ] `python3 scripts/pipeline/validate.py` — FAIL=0
- [ ] `./scripts/check.sh` — pass

## Stage 5 — commit

- [ ] semantic commit, Delta Pav body structure
