# Phase-2 measurement-floor backfill — plan

Closes the gate 10d worklist: every curated host within 50 ly reaches its
class floor (`phase2/curation-data-contract/SPEC.md` §A0). Owner scope decision
(2026-07-20): **all ≤50 ly curated hosts**, not just the roster.

## Shape of the problem

129 hosts below floor at program start, but they are not one uniform pile —
the distribution is bimodal:

| Tier | Hosts | Gap | Cost per host |
|---|---|---|---|
| A — roster (implementation set) | 2 | 1–2 categories | low, high value |
| B — near-complete non-roster | 9 | 1–2 categories | low |
| C — partial | 6 | 3–4 categories | medium |
| D — never Phase-2 curated | 112 | 5–6 categories | full curation pass each |

Tiers A+B are 11 hosts holding ~15 missing determinations total; Tier D is
essentially "Phase 2 for 112 field stars" and is the real bulk of the program.

## Order

1. **Tier A first** — roster hosts feed Phase 3/4 and emit; a floor gap there
   is a gap in the shipping set.
2. **Tier B** — cheap completions, several are planet hosts already used
   elsewhere in the repo.
3. **Tier C** — medium passes.
4. **Tier D** — batched by spectral class (the same query patterns and the same
   catalog papers cover many M dwarfs at once). Expect this to run across many
   sessions; it is the standing background program, not a sprint.

## Method (per host)

Same discipline as `nearstars-add-star` Phase 2, no shortcuts:

- Literature discovery through the **ADS API** with the registered token, sorted
  by citation count. **Never WebSearch** ([[feedback_ads_paper_discipline]]).
- Every value carries `method` + `reference` + `bibcode` (+ `doi` where
  available). `method` describes what the paper actually did — it is a curation
  judgment, never guessed.
- Conflicting determinations are curated as multiple entries with exactly one
  `recommended: true` and the tie-break recorded.
- Honest negatives: "no measurement found" is a valid outcome and must name the
  queries run. Silence in a search is not proof of absence.
- Asymmetric/one-sided constraints stay asymmetric; do not collapse a
  "2–8 Gyr" range into a fake central value.
- Writes go through `scripts/pipeline/apply_phase2.py <slug>` from a
  `phase2/<slug>/measurements.yaml` — never a direct `json.dump` into the
  curated DB ([[project_curated_whole_file_rewrite]]).
- Legacy dict-form planet blocks encountered on the way get upgraded to
  list+method (SPEC §A1 upgrade-on-touch) — this is how the 402-block census
  drains without a mechanical migration.

## Division of labor

Literature research fans out to subagents (independent discovery, structured
return: value + bibcode + method + justification). **The main thread does the DB
write and the verification** — citation integrity is not delegated
([[feedback_agent_token_saving]]).

## Verification

- `python3 scripts/pipeline/apply_phase2.py <slug> --check` before applying.
- `./scripts/check.sh` green (gate 10d count must fall by exactly the number of
  hosts completed — if it doesn't, the write didn't land where expected).
- Class floor satisfied per `star_class()` in `check_pipeline_flow.py`.

## Success criterion

Gate 10d reports zero hosts below floor. Interim progress needs no separate
tracking: the gate's per-class counts are the dashboard.
