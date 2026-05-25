# SKILL.md slim-down — decision log
# Context notes

## Why now (2026-05-22)

The recent policy-tightening pass (added Step 9.0, two anti-patterns, the e/f canonical example) pushed SKILL.md to 609 lines. That clears the skill-creator "body < 500 lines" guideline, and the side effect is that mandatory gates like Step 9.0 risk getting buried in the surrounding prose. The progressive-disclosure principle says deep definitions belong in `references/` — they're already there, so the right move is to strip the duplication out of the body.

## Why a workspace (not in-place)

Other sessions may be reading the live skill mid-edit. If a session re-reads a half-edited SKILL.md it sees a torn state. So:

- `live-snapshot/` — frozen baseline (explicit copy beats `git stash` for this).
- `draft/` — edit target.
- Swap to live only after edits are done AND the other sessions have finished.

## Invariant

This pass changes shape only — behavior must stay equivalent:

- No new Steps, no deletions.
- No new policy branches.
- All 14 Step headings preserved.
- Step 9.0 + 9.1 split preserved (the point of yesterday's policy tightening).
- All `references/` pointers preserved.

CLAUDE.md §3 (Surgical Changes) still applies: "don't touch nearby code that isn't broken" holds even for cleanup work.

## Priority order for the 9 candidates

Roughly by impact:

- Candidates 3 (Step 9.1 template) + 6 (Phase 3-specific policies) + 4 (Dual-track) — ~60 lines combined. Largest `references/` duplication.
- Candidates 1 (Trigger Recap) + 7 (Related documents) — ~22 lines combined. Duplicate frontmatter / external references.
- Candidates 2 / 5 / 8 / 9 — ~30 lines combined. Small cleanups.

## Out of bounds (not touched this pass)

- Step 11 Korean-mirror style table — a frequently-consulted quick-reference table; keep it inline.
- Step 10 verify body — the highest-stakes Step; keep it thick.
- Autonomy guards / Common pitfalls — already compact.
- Other `references/*.md` (`mod-grounded-fields.md`, `scoring-reference.md`, `synthesis-template.md`) — only *receive* content from the body, never *modified* beyond that. The exception is `conflict-resolution.md`, which gets the 4 failure modes from candidate 5.
