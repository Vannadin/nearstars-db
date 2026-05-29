# Context notes — curation data contract

Append-only decision log. Newest at bottom.

## 2026-05-29 — why this dir exists
Two events compounded: (1) a deliberate 2026-05-28 rollback of a 27-commit Tier 1
batch for systematic citation-integrity failures, and (2) a session crash that
lost the *conversation* context (not disk artifacts). User feared a from-scratch
redo. Forensics showed otherwise:
- postmortem + next-session-prompt preserve the methodology and verified citations
- 40 Eri work is committed (10 unpushed commits) and passed independent citation
  verification — keep, do not redo
- the disk/ring schema "format-incompatibility" catastrophe is already RESOLVED
  (`disks_curated.json` passes schema)

## Root-cause synthesis (user-reported failure modes)
1. Phase-order inversion — Phase 3 run on Phase 1 inputs (skipping Phase 2).
2. Ring/disk data broke document format — RESOLVED via separate source layer.
3. Subagent whack-a-mole — agents lacked the global schema invariant, each
   reshaped its file differently → new parity breaks → more fixes → more breaks.
4. Non-deterministic paper reading — agents skim + live-search, so each audit
   found different papers / wrong values; audits diverged instead of converging.

## Design decision: contract-first
The death spiral's root is the *absence of a fixed definition* of what each phase
needs. So: pin the contract (SPEC.md) from the committed sources of truth, then
judge every ad-hoc artifact against it. The contract is the anti-drift jig.

## Convergence mechanism (kills failure mode #4)
The repo already has it: `_bib/<slug>.yaml` pins `arxiv_id`; `fetch_arxiv_texts.py`
caches `_papers/<arxiv_id>.md`; value-check reads the CACHE, not the web. 40 Eri
was curated without a `_bib` (live search), which is why its verification had to
go live — Step 3A retrofits the bib to lock it convergent.

## 40 Eri verification result (2026-05-29)
19 recommended entries / 9 distinct papers. 0 REFUTED. 1 SUSPECT: 40 Eri A mass
method label `evolutionary_model` should be `empirical_relation` (Ma 2018 used the
Torres+2010 relation, not tracks; value 0.78±0.08 and citation are correct).
Minor: 40 Eri B/C age ±0.5 Gyr is a curator estimate, not in Bond 2017 ("~1.8 Gyr").
