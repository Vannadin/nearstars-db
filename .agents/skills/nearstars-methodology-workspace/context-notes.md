<!-- nearstars-methodology 스킬 추출 과정의 결정 기록 -->
# nearstars-methodology skill extraction — context notes

**2026-07-11 — extraction session**

- **Why a skill now.** The methodology-grounding procedure existed as practice
  (13 methodology docs + Principia R1–R7 series) and as scattered records
  (methodology-index.md discipline note, ADS-discipline memory, R6 prompt).
  Owner asked to extract it into a skill so future sessions follow one canonical
  procedure. Skill = thin scaffolding; canonical index stays
  `docs/reference/methodology-index.md` (per reference-doc-location feedback).
- **Two-mode split (A/B).** The practice genuinely has two shapes: durable
  per-body recipes (Mode A, dynamo-doc template) vs one-shot parameter grounding
  consumed by another session (Mode B, R-series). Made the mode choice step 1
  of the skill rather than blending them.
- **Anchors-vs-dictation nuance.** The ADS-discipline memory bans handing agents
  a paper list, but the R-prompts *do* name candidate anchors. Resolved in the
  skill: naming candidate anchors per angle is fine iff framed as
  to-be-ADS-verified and replaceable; dictating a final list is the banned thing
  (2026-06-23 incident).
- **Light test only (owner's call).** Full with/without eval would run real ADS
  research — hundreds of k to millions of tokens. Owner picked a 1-run light
  test: Mode B authoring on the synthetic-eccentricity backlog item, research
  execution forbidden. 57k tokens, 3 min. 8/8 assertions passed; the agent's
  repo-derived counts (204 orbital blocks / 20 e=0 / 35 null / 149 measured)
  reproduced exactly on independent recount.
- **Post-test skill fixes** (from the test agent's own friction report):
  (1) Mode B artifacts live under the consuming track's `plans/<track>/research/`
  — the principia-interstellar-branch path is an instance, not canonical;
  (2) Mode B authoring and executing are separable roles — the deliverable can
  be the prompt alone; (3) a Mode B prompt must carry its own copies of the ADS
  discipline AND the delegation instructions, since the executor gets no other
  context.
- **Workspace location.** Drafted under `.claude/skills/` (skill-creator sibling
  convention) but house convention keeps workspaces in `.agents/skills/`
  (nearstars-phase3-workspace precedent, committed with checklist/context-notes).
  Move deferred until after the owner's viewer review so feedback.json lands in
  the live path.
- **Viewer env note.** `generate_review.py` needs Python ≥3.10; system python3
  is 3.9 → use `/opt/homebrew/bin/python3` (3.14).
