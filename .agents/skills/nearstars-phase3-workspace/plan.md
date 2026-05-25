# nearstars-phase3 SKILL.md slim-down
# Plan

Date: 2026-05-22
Workspace: `.agents/skills/nearstars-phase3-workspace/`
Live skill: `.claude/skills/nearstars-phase3/` (other sessions may be reading it — work on the draft, swap after they finish)

## Problem

`SKILL.md` is 609 lines, over the skill-creator recommended ceiling of 500. The body has accumulated inline templates / tables that duplicate `references/`, a Trigger Recap that duplicates the frontmatter description, and a Phase 3-specific policies section that duplicates Step bodies. Readability of the main procedure (Step 0–14) suffers, and mandatory gates like Step 9.0 risk getting buried.

## Goal

- Body keeps *procedure + judgment triggers* only; deep references move to `references/`.
- 605 lines → under 500.
- Behaviorally equivalent (every Step preserved, every policy branch preserved).
- Live skill untouched during editing — other sessions are running.

## Approach (9 candidates)

### Trim (body → references, or compress)

1. `## Trigger Recap` (15 lines) → 3 lines. Duplicates the frontmatter description.
2. Step 5 scoring table (7 lines) → 1 line. `scoring-reference.md` is the canonical source.
3. Step 9.1 inline markdown template (~26 lines) → heading list only. `synthesis-template.md` is canonical.
4. Step 9 Dual-track paragraph (~23 lines) → triage questions + branch only. `conflict-resolution.md` is canonical.
5. Step 10 failure-mode list (~10 lines) → moved to `conflict-resolution.md`.
6. `## Phase 3-specific policies` (25 lines) → 4-line memory-slug list.
7. `## Related documents` (19 lines) → 5 lines.

### Compress (small paragraph cleanup)

8. Step 0 body (3 paragraphs) → table + 1 paragraph.
9. Intro + Scope box duplication → keep Scope box only.

## Out of scope

- Editing other `references/*.md` files. The only exception is adding failure modes to `conflict-resolution.md` (candidate 5).
- Editing the live skill directory. Swap happens in a separate step after user approval.
- Behavior changes (adding/removing Steps, adding policy branches). This pass is shape-only.

## Verify

1. `draft/SKILL.md` line count ≤ 500.
2. All 14 Steps (0–14) still present.
3. Step 9.0 mandatory-classification gate still visually prominent after compression.
4. All four `references/` pointers in the body survive.
5. (Optional) Load the draft into a fresh session, prompt with "make a TRAPPIST-1 e classification table" and confirm Step 9.0 fires.

## Out of this session

Other-session shutdown + `mv draft/* live/` swap — separate step.
