# Phase 3 generic driver — context notes

## Design decisions

### `system.yaml` is the only system-specific file

Everything else (which planets, which thresholds, which injected papers)
lives there. Stage scripts under `scripts/phase3/` remain generic.

### Driver covers Steps 2–6 only

Steps 0–1 (estimate + pre-flight) and Steps 7+ (triage, deep-read,
synthesis prose, ko mirror, build, commit) stay under the SKILL.md
runbook — they need judgment, not automation. The driver is a
mechanical-loop wrapper.

### Inject as a separate stage

`inject_papers.py` runs AFTER `score_papers.py` (per the existing
`add_missing_papers.py` ordering — "Run once after build_bibliography.py
+ score_papers.py"). Injected papers enter as `status: pending` and are
caught by `fetch_arxiv_texts.py` in Step 6.

The driver wires it in as Stage 5b (between score and fetch).

### Bib slug convention

Match what `build_bibliography.py:46-50` already produces via
`slugify()`: lowercase, non-alphanumeric → `-`. So `Proxima Cen b` →
`proxima-cen-b`, `TRAPPIST-1 d` → `trappist-1-d`. System bibs prefix
with `_system-`.

### Block-parity check is pre-flight for build_html.py

`build_html.py` already enforces block parity, but failure happens
mid-build with a confusing trace. `check_block_parity.py` extracts the
same parser logic into a standalone preflight, so Step 11→12 can fail
fast with a clear message.

## Open questions / deferred

- Should `run_phase3.py` parallelize per-planet bib builds? Currently
  the SKILL says "sequential because arXiv 3 s rate is per-IP". Keep
  sequential. arXiv etiquette > speed.
- `verify_decisions.py` was prototyped and dropped — the Basis cell
  uses author-year shorthand ("Faria 2022", "SM25") not bibcodes, so a
  naïve check generates a warning per row. A useful version needs a
  Bibliography-section cross-reference parser, which is bigger than the
  current refactor's scope. The `check_block_parity` + `verify_triage`
  gates catch the most common failure modes already.

## Related

- [checklist](checklist.md)
- [scoring-reference (nearstars-phase3 skill)](../../.claude/skills/nearstars-phase3/references/scoring-reference.md) — score thresholds context
