# SKILL.md slim-down
# Checklist

## Setup

- [x] Create workspace directory.
- [x] Copy live → `live-snapshot/` (frozen baseline).
- [x] Copy live → `draft/` (edit target).
- [x] Write plan.md / checklist.md / context-notes.md.

## Body slim-down (draft/SKILL.md)

- [x] Candidate 1 — Trigger Recap compressed (15 → 3 lines).
- [x] Candidate 2 — Step 5 scoring table compressed (7 → 1 line).
- [x] Candidate 3 — Step 9.1 inline template compressed (26 → 8 lines).
- [x] Candidate 4 — Step 9 Dual-track paragraph compressed (23 → 8 lines).
- [x] Candidate 5 — Step 10 failure-mode list moved out (-10 lines).
- [x] Candidate 6 — Phase 3-specific policies compressed (25 → 5 lines).
- [x] Candidate 7 — Related documents trimmed (19 → 5 lines).
- [x] Candidate 8 — Step 0 body tightened (-5 lines).
- [x] Candidate 9 — Intro + Scope duplication removed (-8 lines).

## references/ updates (one file only)

- [x] `conflict-resolution.md` — receive the 4 failure modes from candidate 5 (319 → 333 lines).

## Verify

- [~] `draft/SKILL.md` line count: 609 → **511** (target 500, +11-line margin).
- [x] All 14 Steps (0–14) preserved (15 headings including 9.0 + 9.1).
- [x] Step 9.0 mandatory gate preserved (line 276).
- [x] `references/` pointers (5 spots) + intro box (4 spots) all survive.
- [ ] User reviews the diff.

## Apply (separate step, after user approval)

- [ ] Confirm other sessions are shut down.
- [ ] Swap `draft/` → live skill dir.
- [ ] Commit (one-sentence message).
