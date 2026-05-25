# nearstars-phase3 skill — optimization plan

> **STATUS: COMPLETE (2026-05-22)** — superseded by
> `.agents/skills/nearstars-phase3-workspace/` (Anthropic skill-creator
> convention). Kept for historical context only; do not extend.

## Goal

Reduce `.claude/skills/nearstars-phase3/SKILL.md` from 543 → ~350 lines
without losing functionality, by removing duplication with user memory,
the synthesis-template reference, and the score_papers.py script.
Improve consistency with CLAUDE.md (§2 simplicity, §4 verifiable goals,
§7 trio artifacts) and AGENTS.md §2 (work-dir convention).

## Why

The skill was newly created in commit `f40da7b` and retrofitted in
`a457867`. Both passes added content; nothing was trimmed. The current
state has:

- Memory links re-stated inside the skill (loaded twice into context)
- Inline Python in Step 5 that should be a script flag
- A 9-row field table duplicated between SKILL.md and synthesis-template
- Two threshold concepts (`keep-threshold` vs must-read) blurred together
- An undocumented `phase3/<system>/` work-dir convention not in AGENTS.md

The 🔴 critical issues all fall under CLAUDE.md §2 "Simplicity First".

## Scope (this session)

Apply the 🔴 critical items only ([I1]~[I4]). 🟡 medium and 🟢 minor
items are deferred to follow-up sessions per the user's chosen split.

## Out of scope

- [I5] AGENTS.md §2 phase3 dir convention — addressed in 🟡 session
- [I6]~[I11] — addressed in 🟡 / 🟢 sessions
- Restructuring the workflow step count (still 15 steps after this pass)
- Adding new tests / CI for the skill

## Success criteria

1. SKILL.md `wc -l` drops by ≥50 lines
2. `score_papers.py --mark-skipped-below N` works idempotently
3. No memory-redundant lines remain in SKILL.md (Phase 3-specific only)
4. `references/synthesis-template.md` is the single source for the
   per-planet field list
5. Step 5 prose makes the two threshold roles explicit
6. Existing TRAPPIST-1 Phase 3 outputs are not regenerated or changed

## Related

- [phase3 procedure (skill)](../../.claude/skills/nearstars-phase3/SKILL.md) — parent topic this workspace contributes to
