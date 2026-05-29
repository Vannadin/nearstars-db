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
- [x] contract dir committed (542fb6a) — protects the foundation
- [x] 40 Eri A mass label SUSPECT fixed (76c9fc2) — multi-layer, empirical_relation
- [x] **A** (A-lite) — authored 40-eridani-{a,b,c}.yaml pinning cited+anchor papers;
      fetch validated all 20 arxiv_ids resolve (0 failed) + cached to _papers.
      Caught Ma 2018 + Boyajian 2012 (primary anchors) lacking inline arxiv pins.
- [x] **B** — surface cleanup folded into Step 2 (7d6a855); check.sh green
- [x] **C** — Tier 1 host #1: delta-pavonis Phase 2 DONE (8e9b4b7) on Rains 2020
      anchor; full SPEC discipline + check.sh gate. Caught 4 contamination items.

## Step 4 — Disk detour (2026-05-29, triggered by the δ Pav disk fabrication)
- [x] δ Pav disk = fabricated, removed (9c477a2); audited all 7 disk hosts
      (09eb0d1 + cc30ea3) — 61 Vir Tanner fabricated, several mis-cites fixed
- [x] Multi-belt Phase 3 schema (faaaccd) + applied to Vega/Fomalhaut (f8dd360),
      eps Eri (1ef2224); science-faithful tints (cf265c7)
- Valuable but a DETOUR from the original Tier 1 goal.

## REMAINING — original Tier 1 goal (the inversion fix, NOT yet done)
Build Phase 2 STELLAR measurements (8 categories) for the other 7 inversion hosts,
one at a time under the contract. Their DISKS are now clean, but their stellar
Phase 3 still sits on Phase 1:
- eps Eri · AU Mic · HD 69830 · 61 Vir · Vega · Fomalhaut · tau Cet

## Discipline (non-negotiable, from root-cause)
- One host at a time. No parallel subagent batch until a verified template exists.
- Read the cached `_papers/<arxiv_id>.md`, never live web, for value-check.
- Multi-layer edits (DB + narrative + ko mirror) in one commit.
- check.sh is the gate after every host.
