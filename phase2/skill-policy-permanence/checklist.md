---
type: workspace
title: "스킬에 정책 형식 강제 — 체크리스트"
slug: skill-policy-permanence-checklist
cluster: methodology
cluster_role: member
status: active
related: [[skill-policy-permanence-context-notes]], [[skill-policy-permanence-plan]]
created: 2026-05-21
updated: 2026-05-25
tier: public
---
# 스킬에 정책 형식 강제 — 체크리스트
# Skill policy permanence — checklist

## Edits (all in commit 37c16d4)

- [x] `synthesis-template.md` — canonical example reference changed:
      `trappist-1-d.md` → `trappist-1-e.md` + `trappist-1-f.md`.
      d demoted to "pilot — pre-policy" with Alpha Cen incident note.
- [x] `conflict-resolution.md` — two anti-patterns added under
      § Documented divergence § Anti-patterns. Both cite the
      2026-05-22 Alpha Cen incident.
- [x] `SKILL.md` Step 9 — split into 9.0 (mandatory pre-draft
      classification, gates 9.1) + 9.1 (structure, e/f baseline,
      d-as-base prohibited).

## Verify

- [x] Each edited file re-Read post-Edit for structural integrity.
- [x] Step 9 block: 9.0 + 9.1 visible, ``` template ``` block follows
      9.1 correctly, no stray fenced-code issues.
- [x] Anti-patterns subsection bounds clean (next H2 unchanged).
- [x] Canonical examples list renders as a bullet list (not a heading).

## Commit + push

- [x] Single commit `37c16d4` — one-sentence description per CLAUDE.md §9.
- [x] Pushed to `origin/main`.

## Handoff prompt update

- [ ] Add Step 9.0 reminder line to the Alpha Cen redo handoff prompt
      so the next session sees the mandatory gate even if it skims
      the skill body.

## Retrospective artifacts (this directory)

- [x] `plan.md` — what was done and why.
- [x] `checklist.md` — this file.
- [x] `context-notes.md` — decision log + CLAUDE.md conformance note.

## Related

- [context-notes](context-notes.md) — sibling workspace doc in `skill-policy-permanence/`
- [plan](plan.md) — sibling workspace doc in `skill-policy-permanence/`
- [methodology hub](../../docs/reference/methodology.md) — parent topic this workspace contributes to
