# Checklist — Curation data contract → cleanup → A/B/C

Recovery + relaunch after the 2026-05-28 rollback and a session crash.
Order agreed with user: **define the data contract → clean ad-hoc code against
it → run A/B/C**.

## Step 0 — Recovery assessment (DONE 2026-05-29)
- [x] git/worktree/dangling-commit forensics — nothing valuable lost
- [x] 40 Eri citation verification (19 recommended entries, 9 papers) — clean,
      0 refuted, 1 metadata SUSPECT (40 Eri A mass method label)
- [x] check.sh run — disk schema migration landed clean; 3 cosmetic FAILs
- [x] root-cause confirmed: phase-order inversion + ad-hoc scaffolding +
      subagent whack-a-mole + non-deterministic paper reading

## Step 1 — Define the contract  ← CURRENT
- [x] Extract Phase 2 schema from `scripts/pipeline/schema.py`
- [x] Extract Phase 3 workflow from `nearstars-phase3` SKILL
- [x] Write `SPEC.md` (this dir)
- [x] Add full Phase 3 cfg field inventory (15 axes; caught 8 groups I'd missed)
- [x] Correct magnetic/aurora: Phase 3-synth, not a gap (truncated-grep error)
- [x] **User confirmed SPEC.md origin (created this session 13:05, untracked, derived from schema.py + skill)**

## Step 2 — Clean ad-hoc code against the contract  ← DONE (commit 7d6a855)
- [x] Killed orphan pid 72561 (crashed recovery session holding worktree locks)
- [x] Pruned 3 stale agent worktrees + deleted their branches (commits already in main)
- [x] `circumstellar-disk-schema/` → NOT renamed (6 referrers); added to check.sh allowlist instead
- [x] Fixed 3 dead links (relative path off-by-one; target files existed)
- [x] `_tag_categories.py` / `_tag_triage.py`: PRESERVED (triage decisions, no Barnard/Teegarden bib yet)
- [x] `disks-meta-migration/golden/` (154, no test dep) removed; kept checklist.md + extracted.json record
- [x] Korean recovery notes exempted in check_language.py (Korean by intent)
- [x] check.sh → all pass, 0 FAIL (only 2 pre-existing stale-mirror WARN, unrelated)

## Step 3 — A/B/C
- [ ] **A** — retrofit 40 Eri `_bib` (pin the 9 verified papers by arxiv_id +
      cache) → lock the clean host as canonical template, demonstrate convergence
- [ ] **B** — surface cleanup folded into Step 2; confirm check.sh green
- [ ] **C** — Tier 1: delta-pavonis Phase 2 from Rains 2020 anchor, full SPEC
      discipline, single host, check.sh gate, then decide expansion

## Discipline (non-negotiable, from root-cause)
- One host at a time. No parallel subagent batch until a verified template exists.
- Read the cached `_papers/<arxiv_id>.md`, never live web, for value-check.
- Multi-layer edits (DB + narrative + ko mirror) in one commit.
- check.sh is the gate after every host.
