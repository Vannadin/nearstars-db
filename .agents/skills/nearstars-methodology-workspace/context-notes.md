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

**2026-07-11 — iteration 2 (regression feedback from real use)**

- **Owner report: the skill performed worse than the pre-skill practice.**
  Symptoms from the first real run (a warpfx session): whole-prompt
  delegation to a single agent → nested sub-agent fan-out with no
  main-thread verification, plus generally shallower output.
- **Root cause: the skill is a summary, and the summary dropped the
  exemplars.** Pre-skill, authoring always happened next to the live
  artifacts (R6 open in context, dynamo doc as the model, NearStars repo
  assets at hand). The skill compressed those into structure descriptions;
  sessions followed the rules but lost the craft — and in warpfx the
  relative exemplar paths didn't even resolve.
- **Fix chosen: mandatory-read pointers, not embedding.** Owner asked why
  not put the uncompressed originals into the skill; decided against
  physical copies (originals keep evolving — R6 was mid-execution during
  this discussion; embedding creates a second stale copy and another sync
  axis on top of the two-repo skill copies). Instead: a mandatory "read the
  exemplars first" step with absolute paths (resolve from any repo), per
  mode — dynamo doc for Mode A, R6 prompt + gravity-significance-floor
  methodology for Mode B, index discipline note for both. Token cost
  measured at ~3–5k once per authoring session (vs 57k for authoring,
  100k+ per research agent) — negligible insurance.
- **Exemplar audit:** R3/R4/R5 turned out to be *code*-research reports
  (zero ADS citations) — not literature exemplars. The citation-craft
  exemplar is `gravity-significance-floor-methodology.md` (angle-by-angle,
  ~46 pinned citations), R6's graduated Mode A form.
- Earlier same-day amendments (also fallout from the warpfx run): Mode B
  execution rules (run in the session main loop, no whole-prompt delegation;
  absolute paths for the _papers cache and sanity-check data cross-repo)
  and the non-ADS source fallback ladder.
