# Checklist — sprawl-lifecycle-gate

## Bundle 0 — promotion
- [x] Trio created (plan / checklist / context-notes)
- [ ] `plans/doc-tool-sprawl-audit.md` status → promoted (+ko mirror)

## Bundle 1 — rules (AGENTS.md §2)
- [ ] Register phase4/ as a documentation home (root taxonomy: boards + SPEC/README only)
- [ ] §2.1 mirror scope generalized (F7)
- [ ] §2.4 artifact lifecycle rule added
- [ ] plans/ subdir form legalized

## Bundle 2 — mechanical relocation
- [ ] phase4: audits/trackers → `phase4/_audit/` (coverage, silent-passthrough, emit-readiness, facet-checklist)
- [ ] phase4: `polyphemus-art-direction.md` → `phase4/art-direction/`
- [ ] phase4: `synthetic-orbit-noise.md` → `phase4/policies/`
- [ ] phase4: 4 viewer HTML → `phase4/viewers/`
- [ ] References fixed (phase4 README/SPEC, nearstars-phase4 skill, tools.md+ko, animate_orbits.py, alpha_centauri.yaml art_direction path)
- [ ] phase2 session logs → `phase2/tier1-stellar/` (+check_language.py paths)
- [ ] `phase3/_audit/` scratch JSON → gitignored `_audit/_scratch/`
- [ ] .gitignore: `phase3/stability-sim/**/*.log`; untrack 6 committed logs

## Bundle 3 — guardrail
- [ ] check.sh gate 9: phase-root layout / empty dirs / tracked *.log / refs-script index coverage
- [ ] `bash scripts/check.sh` exits 0

## Bundle 4 — index backfill
- [ ] tools.md +8 `scripts/refs/*.py` entries (+ko mirror)
- [ ] one-shot / regenerable header markers on the 8 scripts

## Deferred
- [ ] Slug unification (tau_ceti→tau_cet, α Cen boards) — separate session, before emit
- [ ] docs/ root versioned duplicates — owner confirmation needed
