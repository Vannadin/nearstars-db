<!-- nearstars-phase3 스킬 최적화 체크리스트 - 심각도별 commit 단위로 분할 -->
# Checklist — nearstars-phase3 optimization

## 🔴 Critical (this session — single commit)

- [x] [I1] Compress "Key Policies (from user memory)" — keep only the
      3 Phase 3-specific links (`feedback-phase3-validation`,
      `feedback-phase3-interesting-first`,
      `project-nearstars-phase-distinction`); drop the 5 that are
      already in MEMORY.md auto-load
- [x] [I2] Add `--mark-skipped-below N` flag to
      `scripts/phase3/score_papers.py`; replace SKILL.md Step 5
      inline-Python block with a one-line invocation
- [x] [I3] Step 5 prose: explicitly name two thresholds —
      `--keep-threshold` (bib retention) and must-read threshold
      (fetch in Step 6). Add a one-line note distinguishing them.
- [x] [I4] Move the 9-row "Looking for / Why" table from Step 8 in
      SKILL.md into `references/synthesis-template.md` under a new
      "Decision-table field map" subsection; leave a one-line pointer
      in Step 8.
- [x] SKILL.md line count: 543 → 509 = **-34 lines** (target was
      ≥50; missed because [I3] added 5 lines of intentional prose
      explaining the two-threshold split. Net removals: -39 lines.)
- [x] Smoke test: `score_papers.py --help` shows the new flag;
      dry-run on `docs/phase3/_bib/trappist-1-b.yaml` shows
      "marked-skipped-below 14: 0 papers" (idempotent on already-
      processed yaml)
- [x] Commit with VaNnadin identity, single commit (9a12ade)

## 🟡 Medium (this session — single commit)

- [x] [I5] AGENTS.md §2 — add `phase3/<system>/` block + decision-rule
      bullet (user chose: keep phase3/, document it)
- [x] [I6] Step 1.2 — embed canonical checklist.md stages from
      `phase3/trappist-1-system/checklist.md`
- [x] [I7] Frontmatter description — compress 3 sentences into one
      ("Do NOT use for X / Y / Z / W")

## 🟢 Minor (this session — single commit)

- [x] [I8] Absorb manual-paper-followup into Step 7 (Triage) as a
      new `manual_followup` classification; renumber Steps 15→14
      (Commit) and update Workflow Overview accordingly
- [x] [I9] Remove dead `references/troubleshooting.md` link from
      Common pitfalls section
- [x] [I10] Add "verify:" line to Steps 5, 7, 8, 10, 12 — each one
      names a concrete check before proceeding (CLAUDE.md §4)
- [x] [I11] Promote "Time and scope warning" to Step 0 with explicit
      "quote the matching row to the user upfront and confirm" prose
- [x] Final SKILL.md line count: 515 → 527 (+12 net; the verify
      lines and Step 7 manual_followup body add prose intentionally)
      Total vs original 543: **-16 lines** across three commits.
- [x] Commit with VaNnadin identity (ef6a504)
