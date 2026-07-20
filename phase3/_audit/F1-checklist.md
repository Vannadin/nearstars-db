# F1 — Barnard + Teegarden planet Phase 3 re-synthesis (checklist)

Audit finding F1: 7 planets (Barnard b/c/d/e + Teegarden b/c/d) are Phase-2
curated in the DB but have **no Phase 3 planet reports** — the prior reports
(commits 04701d5 / e006ef6) were swept up in the 2026-05-28 blanket "citation
integrity" revert (a2ef49c) and never restored. The revert's named fabrications
were all OTHER hosts (HD 69830 / eps Eri / AU Mic / 61 Vir / tau Cet); the
Barnard/Teegarden planet reports were collateral. Approach: **recover the prior
drafts → re-verify every Decisions citation against cached papers → reconcile
to DB → promote → ko parity → build → reframe Barnard host**. Not from-scratch.

## Stage 0 — recon + ground truth  [DONE]
- [x] Confirm 7 planets in DB, no current planet reports
- [x] Recover 7 en + 7 ko drafts + old per-planet bibs from git (phase3/*/_recovered/)
- [x] Confirm discovery papers cached: Basant 2025 (2503.08095), Stefanov 2024
      (2410.00577), González Hernández 2024 ([2410.00569](https://arxiv.org/abs/2410.00569)), Dreizler 2024
      ([2402.00923](https://arxiv.org/abs/2402.00923)), Zechmeister 2019 ([1906.07196](https://arxiv.org/abs/1906.07196))
- [x] Build F1-ground-truth.md (all 7 planets: P, a, e, M sin i, S, T_eq, R)
- [x] Re-fetch failed GCM caches: Boukrouche "Near the Runaway" (2510.11940) +
      "Water Clouds" (2411.07922) — abstracts verified, real, correctly attributed
- [x] Confirm [2403.01028](https://arxiv.org/abs/2403.01028) (materials-science misfetch) is cite-only, never used

## Stage 1 — per-planet verify + reconcile + promote  [DONE]
For each of barnards-star-{b,c,d,e}, teegardens-star-{b,c,d}:
- [x] Verify load-bearing rows (mass, a, e, P, T_eq, S) vs F1-ground-truth.md
- [x] Recompute derived (T_eq, S, surface_gravity, density, scale_height) from DB
- [x] Verify every cited paper is real + correctly attributed (cache or WebFetch)
- [x] Apply interesting-first cascade + physical-plausibility gates
- [x] Promote final en → docs/phase3/<slug>.md

## Stage 2 — Korean mirrors  [DONE]
- [x] ko/docs/phase3/<slug>.md block-parity to final en (×7)

## Stage 3 — verification + HTML  [DONE]
- [x] check_block_parity.py <slug> → PASS (×7)
- [x] build_html.py <slug> → exit 0 (×7)
- [x] build_reports_index.py + check-mirrors.sh
- [x] Reframe Barnard host report: planets confirmed (Basant 2025), drop
      "out of scope / candidate" framing
- [x] check.sh gates (allow pre-existing build_docs.py gate-5)

## Stage 4 — commit  [DONE — 939b794 Barnard, 6cd8fed Teegarden]
- [x] per-system commits (Barnard 4-planet, Teegarden 3-planet) + host reframe
- [x] errata + memory update
