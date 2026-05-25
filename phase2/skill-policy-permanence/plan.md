# 스킬에 문서화된 정책의 *형식* 까지 영구 반영하는 작업
# Skill policy permanence — plan

Date: 2026-05-22 (retrofit after the work — see context-notes for why)

## Problem

Alpha Cen Phase 3 first pass (committed 2026-05-22 16:16, reverted 16:40
in `0cd8b2f`) named "documented divergence" in prose but did **not**
create the `## Canonical alternatives` H2 section. `proxima-cen-d.md`
inlined `0 (canonical) / 50 (variant)` in a Decisions Value cell —
schema breakage, not the standard appendix format.

The policy *concept* reached the author; the policy *form* did not.

## Root cause hypothesis

Most likely the author used `trappist-1-d.md` (pilot, pre-policy) as
the structural template. d has no `## Canonical alternatives` section
because the documented-divergence policy was added 2026-05-22 14:04
(`a9e5438`), well after d was written. Copying d's shape silently
drops the section even when the new planet has a divergence.

A secondary contributor: SKILL.md Step 9 mentioned the section but
treated the diagnostic question as advisory — there was no gate that
forced the author to *enumerate* each row's classification before
drafting.

## Goal

Make the skill encode policy *form* as strongly as concept, so a
future session can't apply it half-correctly.

Verification: spawn a fresh agent with only the skill in context, ask
it to plan a synthesis with at least one divergence row, and confirm
the planned output has the `## Canonical alternatives` section.

## Approach (three changes, single commit `37c16d4`)

1. **synthesis-template.md** — replace the "Canonical example" pointer
   from `trappist-1-d.md` to `trappist-1-e.md` and `trappist-1-f.md`.
   Demote d to "pilot — pre-policy" with explicit don't-use-as-template
   warning citing the Alpha Cen incident.

2. **conflict-resolution.md** § Documented divergence § Anti-patterns —
   add two anti-patterns:
   - "Naming the divergence in prose without creating the section"
     (the structural-vs-terminology gap that bit Alpha Cen)
   - "Inlining canonical/variant values in a single Decisions cell"
     (the `0 (canonical) / 50 (variant)` schema violation)
   Both anti-patterns cite the 2026-05-22 incident as evidence.

3. **SKILL.md Step 9** — split into 9.0 (mandatory pre-draft
   classification) + 9.1 (structure). 9.0 forces a per-row
   classification log into `phase3/<system>/context-notes.md` with
   labels `canonical-aligned / tie-break / divergence`. The author
   must report the counts to the user before drafting begins.

## Verify (was done implicitly; logging it here per §4)

- [x] Each edit re-read post-Edit for structural integrity.
- [x] SKILL.md Step 9 structure intact (9.0 + 9.1, template block
      follows 9.1 correctly).
- [x] conflict-resolution.md Anti-patterns subsection still ends
      cleanly before `## When the user's prior synthesis was wrong`.
- [x] synthesis-template.md "Canonical examples" plural list renders.

## CLAUDE.md conformance — retrofit acknowledgement

This work was initially executed without creating the `plan.md /
checklist.md / context-notes.md` artifacts that §7 requires for
non-trivial tasks. The user flagged this. These files are being
created retroactively so a future session reviewing why the skill
was changed can find the rationale without re-deriving it from the
commit message alone.

## Related

- [methodology hub](../../docs/reference/methodology.md) — parent topic this workspace contributes to
