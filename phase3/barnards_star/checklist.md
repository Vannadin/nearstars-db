# Barnard's Star Phase 3 — Checklist

## Stage 1 — bibliography builds (driver)
- [x] run_phase3.py barnards_star stages 2, 3, 5, 5b, 6 (stage 4 skipped — no seed)
- [x] verify_triage.py barnards_star — all 20 must-read papers categorized

## Stage 2 — Step 9.0 row classification (per file)
- [x] context-notes: classification log for barnards-star (12 canonical / 5 tie-break)
- [x] context-notes: classification log for barnards-star-b (16 canonical / 16 tie-break)
- [x] context-notes: classification log for barnards-star-c (16 canonical / 16 tie-break)
- [x] context-notes: classification log for barnards-star-d (16 canonical / 16 tie-break)
- [x] context-notes: classification log for barnards-star-e (16 canonical / 18 tie-break)

## Stage 3 — English synthesis (5 .md files)
- [x] docs/phase3/barnards-star.md (17 picks)
- [x] docs/phase3/barnards-star-b.md (32 picks)
- [x] docs/phase3/barnards-star-c.md (32 picks)
- [x] docs/phase3/barnards-star-d.md (32 picks)
- [x] docs/phase3/barnards-star-e.md (34 picks; includes thin-atmosphere tie-break)

## Stage 4 — VERIFY pass
- [x] every Decisions row author/year/number traces to fetched paper or marked tie-break
  - Basant 2025 (2503.08095): orbital + masses + T_eq table verified
  - González Hernández 2024 (2410.00569): b orbital + activity verified
  - Toledo-Padrón 2019 (1812.06712): P_rot + cycle + log R'HK verified
  - France 2020 (2009.01259): 25% duty cycle + 87 Earth-atm/Gyr verified
  - Duvvuri 2021 (2102.08493): EUV flux verified
  - Cristofari 2024 (2310.12125): T_eff + log g verified
  - Mann 2015 / Rains 2021 / Boyajian 2012 / Marfil 2021: DB recommended

## Stage 5 — Korean mirrors
- [x] ko/docs/phase3/barnards-star.md (40 blocks paired)
- [x] ko/docs/phase3/barnards-star-b.md (37 blocks paired)
- [x] ko/docs/phase3/barnards-star-c.md (38 blocks paired)
- [x] ko/docs/phase3/barnards-star-d.md (38 blocks paired)
- [x] ko/docs/phase3/barnards-star-e.md (40 blocks paired)

## Stage 6 — HTML + parity
- [x] check_block_parity.py for all 5 slugs (all OK)
- [x] build_html.py for all 5 slugs (all OK, 53-65 KB)
- [ ] coordinator handles reports-index.html refresh (out of scope)
