# Checklist — sprawl-lifecycle-gate

## Bundle 0 — promotion
- [x] Trio created (plan / checklist / context-notes)
- [x] `plans/doc-tool-sprawl-audit.md` status → promoted (+ko mirror) — b97def3

## Bundle 1 — rules (AGENTS.md §2)
- [x] Register phase4/ as a documentation home (root taxonomy: boards + SPEC/README only) — a77a3a6
- [x] §2.1 mirror scope generalized (F7) — a77a3a6
- [x] §2.4 artifact lifecycle rule added — a77a3a6 (+evidence-log exception, gate-9 commit)
- [x] plans/ subdir form legalized — a77a3a6

## Bundle 2 — mechanical relocation
- [x] phase4: audits/trackers → `phase4/_audit/` (coverage, silent-passthrough, emit-readiness, facet-checklist) — 97e1238
- [x] phase4: `polyphemus-art-direction.md` → `phase4/art-direction/` — 97e1238
- [x] phase4: `synthetic-orbit-noise.md` → `phase4/policies/` — 97e1238
- [x] phase4: 4 viewer HTML → `phase4/viewers/` — 97e1238
- [x] References fixed; dead-link scan 545 files / 0 broken — 97e1238
- [x] phase2 session logs → `phase2/tier1-stellar/` (+check_language.py paths) — f0681c5
- [x] `phase3/_audit/` scratch JSON → gitignored `_audit/_scratch/` — c665284
- [x] .gitignore: `phase3/stability-sim/**/*.log`; 4 uncited logs untracked, 2 evidence logs kept (elements.log, _ring_clearing.log) — c665284

## Bundle 3 — guardrail
- [x] check.sh gate 9: phase-root layout / empty dirs / tracked *.log / refs-script index coverage — 8822200
- [x] `bash scripts/check.sh` exits 0 — all 9 gates green (2026-07-19)

## Bundle 4 — index backfill
- [x] tools.md +8 `scripts/refs/*.py` entries (+ko mirror) — e3345de
- [x] one-shot / regenerable header markers on the 8 scripts — e3345de
- [x] 7 pre-existing missing ko mirrors (principia-interstellar-branch) backfilled — 75d6080

## Deferred
- [ ] Slug unification (tau_ceti→tau_cet, α Cen boards) — separate session, before emit
- [ ] docs/ root versioned duplicates — owner confirmation needed
