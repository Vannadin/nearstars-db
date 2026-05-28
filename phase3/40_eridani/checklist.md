# 40 Eridani — Phase 3 Synthesis Checklist

Triple system: A (K0.5 V) + B (DA2.9 white dwarf) + C (M4.5 Ve flare star DY Eri).
Stellar-only synthesis (HD 26965 b refuted, no curated planets).
Started 2026-05-29 after Tier 2 warmup. Per Phase 3 skill workflow.

## Stage 0 — Pre-flight

- [x] Time estimate shared: 5–9 h total (3–6 h Phase 3 + 2–3 h A Phase 2 prereq)
- [x] Phase 2 status confirmed
  - 40 Eri A: ❌ Tier 1 prerequisite (8 categories missing)
  - 40 Eri B: ✅ (Bond 2017 paper-verified)
  - 40 Eri C: ✅ (Mason 2017 + Mann 2015 + Cifuentes 2020 + [Fe/H] follow-up)
- [x] Working dir `phase3/40_eridani/` created
- [x] checklist.md + context-notes.md (this file + sibling)

## Stage 1 — Per-component background agents (parallel)

- [ ] **Agent A** — 40 Eri A Phase 2 (mass / radius / Teff / luminosity / age / [Fe/H] / P_rot / activity) → Phase 3 synthesis `docs/phase3/40-eridani-a.md` + ko mirror
- [ ] **Agent B** — 40 Eri B Phase 3 synthesis `docs/phase3/40-eridani-b.md` + ko mirror (DA WD specific Decisions fields)
- [ ] **Agent C** — 40 Eri C Phase 3 synthesis `docs/phase3/40-eridani-c.md` + ko mirror (M dwarf flare star)

Each agent applies the 7-step procedure from 2026-05-28 postmortem:
1. Pre-curation lit search
2. Citation value-check at paper-Table level
3. Crossref DOI + abstract+author verify
4. Multi-layer commit discipline (DB + meta_notes + narrative + bibliography)
5. Phase 2 → Phase 3 reconciliation
6. No false-negative claims (silence ≠ "no measurement exists")
7. Verification subagent spot-check after draft

## Stage 2 — Synthesis + verification (per-agent)

- [ ] Each agent runs Step 9.0 pre-draft classification log (canonical-aligned / tie-break / documented-divergence per Decisions row)
- [ ] Each agent runs Step 10 VERIFY (every Decisions row traced to paper)
- [ ] Each agent launches its own verification subagent (Step 7 of postmortem procedure)

## Stage 3 — Integration in main session

- [ ] Receive agent outputs, review consistency across A/B/C (system-coeval age, hierarchy notes)
- [ ] Korean mirrors (block-parity check)
- [ ] `check_block_parity.py` per slug
- [ ] `build_html.py` per slug
- [ ] `build_reports_index.py`
- [ ] `check-mirrors.sh`
- [ ] Browser visual check (lang toggle, table rendering)

## Stage 4 — Commit

- [ ] Per-component or single-system commit (decide based on size)
- [ ] Multi-layer: DB + Phase 3 markdown + ko + docs build artifacts in same commit per host

## Notes

- 40 Eri B is a WD — stellar synthesis template `docs/phase3/alpha-centauri-a.md` (8-section). Surface tint / atmosphere sections N/A; cooling sequence + IFMR + age narrative emphasized.
- 40 Eri C is a flare star — high activity → Firefly cfg considerations downstream.
- A-BC outer orbit ~8000 yr unresolved → no binary_orbits entry for A-BC.
- Phase 2 follow-up just completed: Mann 2015 [Fe/H] -0.21 for C; Cifuentes 2020 L verified; Shan 2024 P_rot 8.56 d debated (not curated).
