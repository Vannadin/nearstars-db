# Phase 2 disk_measurements ingest — plan

## Goal

Add paper-cited `disk_measurements` arrays to `db/systems/<star>.json` for the 8 disk-host stars synthesized in commit `ea775f3`, so that:

1. Phase 3 disk Decisions rows have a DB source-of-truth instead of literature-direct citation.
2. The future kopernicus-cfg disk emitter (Step 2 of the 3-step disk-followup plan) reads from DB rather than parsing Phase 3 markdown.
3. NS's "per-measurement bibcode + recommended flag" provenance policy applies to disk data, exactly as it does for mass / radius / teff.

Eight stars covered: Vega, Fomalhaut, AU Mic, ε Eri, τ Cet, 61 Vir, HD 69830, δ Pav.

## Why

- Every Phase 3 synthesis under `ea775f3` and its precursors flagged "Phase 2 `disk_measurements` ingest needed" in the Open items. This workspace closes that loop.
- The disk fields in current stellar Phase 3 markdown cite Su 2013 / Sibthorpe 2010 / etc. directly in the Basis column. That is acceptable as Phase 1-grade input but degrades auditability versus the rest of NS's per-measurement provenance discipline.
- The kopernicus-cfg disk emitter (Step 2, separate workspace) needs a stable machine-readable disk source. Phase 3 markdown parsing works but adds parser fragility; DB read is cleaner and matches every other emit pattern in the project.

## Approach

### Step 1.1 — Define `disk_measurements` schema (main, sequential)

Add to `docs/reference/methodology.md` § JSON Schema → `stars[]` a new sub-section documenting `raw.disk_measurements[]`. Schema:

```json
{
  "belt": "inner_warm" | "intermediate" | "main_cold" | "single" | "asteroid_analog" | "warm" | "cold",
  "inner_radius_au": <number, nullable>,
  "outer_radius_au": <number, nullable>,
  "dust_temperature_k": <number, nullable>,
  "dust_mass_mearth": <number, nullable>,
  "morphology": "<prose>",
  "resolved": <bool>,
  "observatory": "<Spitzer-MIPS | Herschel-PACS | ALMA | HST-STIS | VLT-SPHERE | JWST-MIRI | IRAS | JCMT-SCUBA | OVRO | SMA | EUVE | ...>",
  "inclination_deg": <number, nullable>,
  "method": "sed_fit" | "resolved_imaging" | "photometric_excess",
  "reference": "<string>",
  "bibcode": "<NASA ADS bibcode>",
  "doi": "<DOI>",
  "recommended": <bool>,
  "notes": "<string, optional>"
}
```

Entry granularity: per (paper × belt). A paper that fits multi-belt structure (e.g. Su 2013 Vega 2-belt) emits multiple entries sharing the same bibcode. A paper that detects only `disk_present` from photometric excess (e.g. Aumann 1984 IRAS) emits one entry with most geometry fields = null.

This step also updates `scripts/pipeline/validate.py` if its schema check parses raw measurement arrays explicitly.

### Step 1.2 — 8 parallel sub-agents (1 per star)

Each sub-agent receives:

- Star slug + display name
- Its `phase3/<star>/context-notes.md` (already has Decisions row Basis citations)
- Its `docs/phase3/<slug>.md` (full synthesis prose with paper-cited disk rows)
- The new `disk_measurements` schema (inlined from Step 1.1)
- Output contract: directly write the updated `db/systems/<slug>.json` with the `disk_measurements` array filled (belt-decomposed, paper-cited, `recommended: true` flagged on the canonical / most-cited fit)

Each sub-agent extracts paper-cited disk values from the Phase 3 synthesis and converts them into structured entries. No new literature work — only restructuring the cite-paper-and-numbers content from Phase 3 into DB form.

### Step 1.3 — Validation + commit (main, serial after sub-agents return)

- `python3 scripts/pipeline/validate.py` exits 0 for all 8 stars
- Spot-check one star's `disk_measurements` against its Phase 3 markdown for value match + bibcode match (Step 10 VERIFY analog for Phase 2)
- Single batch commit: `feat(db): disk_measurements ingest for 8 disk-host stars (Phase 2 follow-up to ea775f3)`
- Update each star's Phase 3 Open items to mark the `disk_measurements ingest` item as resolved (cross-link back)

## Success criteria

- [ ] `methodology.md` documents `disk_measurements` schema with the field list above
- [ ] `validate.py` schema check accepts (and validates) `disk_measurements` arrays
- [ ] 8 `db/systems/<star>.json` files each have a populated `disk_measurements` array (≥ 1 entry with `recommended: true`)
- [ ] Multi-belt stars (Vega, Fomalhaut, ε Eri) have ≥ 2 belt entries
- [ ] Sample paper-cite spot-check passes (random entry's bibcode matches the cited paper in Phase 3 Basis)
- [ ] Phase 3 Open items for these 8 stars get the disk_measurements item updated to "ingested in commit <hash>"

## Risks

| Risk | Mitigation |
|---|---|
| Schema design churn after first sub-agent returns | Define schema fully in Step 1.1 before any sub-agent dispatch; schema commit is gate |
| Sub-agent invented values (no paper cite) | Step 10 VERIFY applied to disk_measurements; main spot-check before commit |
| `validate.py` rejects schema additions | Step 1.1 also updates validate.py if needed; run before sub-agent dispatch |
| Conflict with other session's DB work | Other session works on `docs/index.v2.html` reading from `docs/data.json`, not writing `db/systems/*.json`; safe per the cross-session survey earlier in this conversation |
| Belt enum churn (some discoveries don't fit "warm/cold/main" buckets) | Sub-agent free to add new belt enum strings; schema permits any string at first, normalize after Step 1.3 if needed |

## Agent team structure

Same pattern as the stellar synthesis batch retrofit (the immediate precursor — confirmed working):

- **Main session**: schema definition (Step 1.1), sub-agent dispatch, Step 10 VERIFY analog (Step 1.3), validate.py, commit
- **8 sub-agents (general-purpose)**: 1 per star, parallel dispatch in single message. Each reads its own Phase 3 markdown + workspace context-notes, writes its star's db json directly.

## Related

- [checklist](checklist.md)
- [context-notes](context-notes.md)
- upstream Phase 3 syntheses: `docs/phase3/{vega,fomalhaut,au-mic,eps-eri,tau-cet,61-vir,hd-69830,delta-pavonis}.md`
- schema reference: [`docs/reference/methodology.md`](../../docs/reference/methodology.md) § JSON Schema → stars[]
- schema source workspace: [`phase3/circumstellar-disk-schema`](../../phase3/circumstellar-disk-schema/plan.md)
- downstream Step 2: kopernicus-cfg disk emitter (separate workspace, future)
- downstream Step 3: disk-host planet Phase 3 (separate workspace, future)
