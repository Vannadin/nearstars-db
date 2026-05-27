# Phase 2 disk_measurements ingest — context notes

Append-only decision log.

## 2026-05-27 — Step 1 of the 3-step disk-followup plan

User confirmed sequence: (1) Phase 2 disk_measurements ingest → (2) kopernicus-cfg disk emitter → (3) 14 planet Phase 3 syntheses across 5 stars. Agent team usage approved.

## Decision: entry granularity = per (paper × belt)

Alternative considered: per paper, with multi-belt structure represented as a nested array inside the entry.

Selected: per (paper × belt) with a `belt` enum field. Reasons:

- Each belt has its own geometry (inner/outer radius, dust temperature). A nested array would duplicate the bibcode/doi/reference fields per belt; a flat array with `belt` field is more normalized.
- Filtering "recommended cold belt" becomes a simple `belt == "main_cold" && recommended == true` filter rather than nested traversal.
- Matches the existing NS pattern of one row per (value × source). `mass_measurements` already has one row per (mass-estimate × paper); `disk_measurements` extends this to (belt × paper) since "disk" is multi-property by nature.

Cost: a paper that fits N-belt structure produces N rows with shared bibcode. Acceptable.

## Decision: belt enum is open-ended (no pre-frozen list)

Initial enum: `inner_warm | intermediate | main_cold | single | asteroid_analog | warm | cold`.

But ε Eri has explicit "three belts" (Backman 2009): asteroid (3 AU) + intermediate (20 AU) + Kuiper analog (64 AU). HD 69830 has a single warm asteroid-belt analog at 1 AU. Vega is two-belt warm (14 AU) + cold (62-200 AU). δ Pav is single cold belt at 30-80 AU. Fomalhaut is three-belt with inner asteroid analog + intermediate + main ring at 140 AU.

Different papers use different naming conventions for the same belt. Pre-freezing the enum forces translation work. Better: schema allows any string, document the *recommended* values in methodology, let sub-agents add new strings if the paper uses one (e.g. "outer_halo" if a paper describes it that way). Normalization can happen later if values diverge wildly.

## Decision: sub-agent writes db json directly

Previous batch retrofit (ea775f3) had mixed sub-agent behavior — some returned markdown text for main to write, some wrote files directly. For Step 1.2 we standardize: each sub-agent writes its own star's db json directly. Reasons:

- Each star has independent json (no inter-star race condition)
- main is freed from re-serializing 8 large json blobs
- Sub-agent has direct read access to `db/systems/<slug>.json` to preserve existing fields when adding the new `disk_measurements` array
- Main's job is Step 10 VERIFY post-receipt, not transcription

Risk: sub-agent could break unrelated fields. Mitigation: validate.py runs on every star post-receipt; main spot-checks a returned diff.

## Decision: commit granularity = single batch

Per-star commits would produce 8 commits. The work is mechanical (restructuring Phase 3 cite content into DB form) and homogeneous, so a batch is cleaner — and matches SKILL.md Step 14 "per-system batching for shared context" precedent.

If validate.py fails for any star, that star is fixed before commit; no partial commit.

## Risks

| Risk | Notes |
|---|---|
| methodology.md schema also needs `ko` mirror? | Likely yes per `scripts/check-mirrors.sh` discipline — check after Step 1.1 |
| Some Phase 3 markdown disk rows lack bibcodes (the deferred "Phase 2 disk_measurements absent" note effectively masks specific paper cites) | Sub-agent should re-extract from Bibliography section, where bibcodes ARE listed |
| HD 69830 documented divergence (`disk_opacity` amplified for visibility) — should DB record the unamplified physical value? | Yes — DB stores observation-faithful values. The Phase 3 cfg-pick is preserved in the Decisions table, with the DB as the source for the "physical" alternative |
| τ Cet's 4th planet (e) curation question — does Phase 2 ingest also handle the planet_controv_flag? | Out of scope for this workspace. Mention in Open items as a downstream task |

## Open items (deferred to follow-up workspaces)

- Schema for non-disk Phase 2 measurements that are still null for the 8 stars (mass_measurements, radius_measurements, teff_measurements) — separate `nearstars-add-star` runs
- τ Ceti e curation question (separate from disk_measurements)
- kopernicus-cfg emitter to read this new array (Step 2)

## Related

- [plan](plan.md)
- [checklist](checklist.md)
- upstream: [phase3/circumstellar-disk-schema](../../phase3/circumstellar-disk-schema/plan.md)
- methodology: [`docs/reference/methodology.md`](../../docs/reference/methodology.md)
