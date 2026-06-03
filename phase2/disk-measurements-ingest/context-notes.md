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

## 2026-06-03 — vertical thickness (`aspect_ratio`) extension

Resumed the stalled 2026-06-02 thickness session. Pending decision (field design
for vertical structure) resolved with the user: **Option A — `aspect_ratio`
(h = H/r, dimensionless)**, chosen over absolute `scale_height_au` + ref radius (B)
and `opening_angle_deg` (C). Reasons: literature reports h directly (verbatim, zero
derivation surface), scale-free → cross-host comparable, single field, render
opening angle = arctan(h) is trivial.

Schema: added `aspect_ratio` to `schema.py` `disk_measurements.value_keys` (enables
`uncertainty_aspect_ratio`). Documented in `methodology.md` (+ ko). **SPEC §B not
touched** — another session has an uncommitted atmosphere-row diff in SPEC.md, so a
`git add` would capture it; SPEC §B value-key list is a follow-up.

Verified values (paper-read, not memory — the MacGregor-2017 memory was WRONG):
- **Fomalhaut** h ≈ 0.0175 ± 0.004 — Boley 2012 (`1204.0007`, `2012ApJ...750L..21B`)
  reports a 1.0° ± 0.25 midplane opening angle (exponential vertical profile);
  h = tan θ. MacGregor 2017 (`1705.05867`) does NOT measure vertical structure (2D
  model, only cites Boley) — corrected a false attribution.
- **AU Mic** h = 0.031 (+0.005/−0.004) — Daley 2019 (`1904.00027`,
  `2019ApJ...875...87D`, DOI 10.3847/1538-4357/ab1074), edge-on ALMA i=88.5°, Gaussian
  H(r)=hr constant over r~23-41 AU; new entry (inclination left null so Schneider 2014
  stays recommended geometry). Cached at `docs/phase3/_papers/1904.00027.md`.

Only these two of the 8 disk hosts have a measured vertical structure (the rest are
face-on or unresolved → `aspect_ratio` absent, never synthesized). Propagated via
build_systems → build_site (single-writer disk zone; serialized in one session).

## Related

- [plan](plan.md)
- [checklist](checklist.md)
- upstream: [phase3/circumstellar-disk-schema](../../phase3/circumstellar-disk-schema/plan.md)
- methodology: [`docs/reference/methodology.md`](../../docs/reference/methodology.md)
