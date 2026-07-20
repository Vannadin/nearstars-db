# Plan — pipeline-flow-program (phase contract, boundary gates, data-shape normalization, resolver)

Greenlit 2026-07-20 (owner): WP0–WP3 now; WP4 (phase3 gap-fill) and WP5 (phase4
completion) scheduled separately. Phase-2 measurement-floor backfill scope:
**all curated hosts within 50 ly** (owner decision; beyond-implementation-range
flagged bodies excluded).

## Problem (from the two 2026-07-20 audits)

1. **The value spine is prose.** kopernicus/firefly emitters regex-scrape the
   `## Decisions` table in `docs/phase3/<slug>.md`; principia reads db only;
   only researchbodies reads `phase4/*.yaml`. The gated phase4 layer reaches
   1 of 4 emitters. db JSON and phase4 YAML never join in code; the body-name
   join (SPEC §3) has no gate.
2. **Stale contracts.** `guideline.md` §9 still carries the pre-rebuild
   Phase 1–4 definitions; `principia-cfg/references/planet-contract.md` claims
   `planets[]` is empty (123 files now have planets).
3. **Per-system authoring variance.** phase2: 3 authoring generations, 8 roster
   hosts without per-host dirs, planets_curated has two block shapes (list vs
   dict) even within one system; phase4: refs[] sparsity (140 warnings), boards
   missing (trappist_1, luhman_16), tau_cet board star-only.

## Work packages (this program = WP0–WP3)

- **WP0 — Pipeline contract doc**: `docs/reference/pipeline-contract.md` (+ko).
  Current phase definitions, per-boundary artifact/key/gate table, per-class
  done criteria, value-resolution order, write-only-artifact register,
  historical phase2 layout index. guideline.md §9 replaced with a pointer.
- **WP2 — Boundary gates**: `scripts/check_pipeline_flow.py` (check.sh gate 10):
  (a) phase4 `body:` keys ↔ db names (fiction bodies via explicit marker),
  (b) roster completeness matrix (confirmed set × required artifacts per class),
  (c) Decisions-table parse check via the shared parser.
  Shared parser `scripts/pipeline/phase3_decisions.py` lands here (WP1 builds on it).
- **WP3 — Phase 2 data-shape normalization**: migrate planets_curated dict-form
  blocks to the canonical multi-variant list form + validate.py regression rule;
  measurement-floor policy per star class written into
  `phase2/curation-data-contract/SPEC.md`. Floor **backfill** (all ≤50 ly hosts)
  is a separate content program driven by that floor gate's report.
- **WP1 — Emit-value resolver**: `scripts/pipeline/resolve_emit_values.py` —
  the single merge point db.derived → phase3 decisions (parsed) → phase4
  fields[] producing per-body effective values (dry-run JSON under dist/ or
  stdout; cfg writing stays deferred). Emitters are NOT rewired now (emit
  wiring stays a project-end task per standing policy); the resolver + contract
  define what they will read.

## Out of scope (separately scheduled)

- WP4: TRAPPIST-1 star report, 40 Eri c/d reports (phase3 sessions).
- WP5: trappist_1/luhman_16 boards, tau_cet board planets+disk, refs[] backfill.
- Floor backfill curation sessions (ADS discipline, per-host).
