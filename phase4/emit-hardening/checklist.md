<!-- Phase 4 emit-hardening 작업 체크리스트 — emit-readiness-review.md 권장 순서 1→5 이행 추적 -->
# Phase 4 Emit-Hardening — Checklist

Driven by `phase4/_audit/emit-readiness-review.md`. Order = the review's remediation path.

## 1. Validator (BK1) — highest leverage
- [x] Define schema **v2** in `phase4/SPEC.md` (typed `fields:` map + `narrative:`, normalized `gate` block, `superseded` status, `discoverability` promotion)
- [x] `scripts/check_phase4_gate.py` — parse every row; `gated/emitted ⟹ verdict ∈ enum`; `documented-divergence ⟹ divergence_note`; axis-group valid; status enum
- [x] `schema_version` gating: v2 = hard-fail, legacy(v1) = soft-warn (so un-migrated boards don't turn check.sh red)
- [x] Wire into `check.sh` as gate 8
- [ ] Extend `check_dead_links.py` to glob `phase4/**/*.yaml` (deferred — separate low-risk change)

## 2. Schema normalization (MJ1–MJ4, MN1–MN4) — pilot on α Cen first
- [x] `alpha_centauri.yaml` → v2 (viewer sample): 75→75 rows lossless; group rows → typed `fields`; prose → `narrative`; gate keys → `evidence`/`divergence_note`; fixed `verdict: partial` (banding split), `status: superseded` (legal now), empty j2 gate, invented axes (orbit/bulk residual), Beichman ref → `["2508.03812","2508.03814"]`. **validator v2: 0 errors, 62 warns (canon/no-bibcode rows)**
- [ ] `proxima_cen.yaml` → v2 (part of the α Cen system view)
- [ ] Roll out to `40_eridani`, `fomalhaut`, `tau_cet`, `barnards_star`

## 3. Verdict fixes (MJ5, MJ6) — done inline during normalization
- [x] α Cen: banding morphology + aurora + A/B stellar_wind + rings → `documented-divergence` + note (verified: 0 divergences without note)
- [ ] 40 Eri: film-over-physical + below-threshold departures → `documented-divergence` + note
- [ ] Re-gate Erid (40 Eri) as class D (stability + composition), not `culture/classification`

## 4. Emitter-contract reconcile (BK2, BK3, BK6, BK7, MJ7)
- [ ] RB emitter: consume `decisions[].discoverability_cfg` (or promote to flat list) + add `message`/bibcode `ref`
- [ ] Recompute Pandora figure on gated 0.645 M⊕ (BK6, `figure/values.md`)
- [ ] Decide writer scope for planet/figure layer (BK3) — extend vs hand-write
- [ ] Per-body color/variant selector field (MJ7)

## 5. Coverage (MJ8)
- [ ] `phase4/trappist_1.yaml`, `phase4/luhman_16.yaml`
- [ ] Tau Ceti planets + cold debris disk board rows
- [ ] Barnard / Tau Ceti passthrough-confirm rows
- [ ] Fix stale prose (Pandora 225k/27h; silent-passthrough-audit line 72)

## Viewer deliverable (owner request)
- [x] `scripts/phase4/build_phase4_html.py` — renders a v2 board → bilingual HTML (status/verdict badges, typed fields, hex chips, expandable narrative+evidence, light/dark + KR/EN toggle)
- [x] `docs/phase4/alpha-centauri.html` — 8 bodies, 75 decisions, generated from the normalized board
- [ ] EN narrative cells (currently chrome is bilingual, prose is KR-only — needs per-row `narrative_en` later)

## Resolver adoption (pipeline-flow-program, 2026-07-20)
- [ ] **Field-alignment map**: phase4 SPEC §0 menu name ↔ phase3 Decisions key ↔ cfg key.
      Prerequisite for any real phase4-over-phase3 override — the two vocabularies are
      currently disjoint (resolver dry-run: 0 natural collisions across the roster).
      Raw material: curation-data-contract SPEC "full cfg field inventory (by axis)".
- [ ] Rewire all 4 emitters to read `scripts/pipeline/resolve_emit_values.py` output
      (kopernicus/firefly drop their local Decisions regex → shared parser comes free);
      ring/disk inputs move from the never-created kopernicus_extras.yaml to phase4 fields.
