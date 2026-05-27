# Phase 2 disk_measurements ingest — checklist

## Step 1.1 — Schema definition (main)

- [ ] Read `docs/reference/methodology.md` § JSON Schema → `stars[]` for existing `*_measurements` documentation pattern
- [ ] Add `### disk_measurements` subsection with the schema documented in `plan.md`
- [ ] Add a worked example (Vega-style two-belt entries) so sub-agents have a reference template
- [ ] Check `scripts/pipeline/validate.py` — does it enforce per-measurement schema? If yes, update to accept `disk_measurements` array
- [ ] Run `python3 scripts/pipeline/validate.py` against existing 8 db files — confirm baseline passes (no disk arrays = no schema failures)
- [ ] `check.sh` baseline run — record any failing checks unrelated to this work
- [ ] Schema commit gate: single commit `refs(methodology): disk_measurements schema for raw stars[] block`

## Step 1.2 — 8 parallel sub-agents

- [ ] Dispatch Vega disk_measurements sub-agent
- [ ] Dispatch Fomalhaut disk_measurements sub-agent (multi-belt + companion context)
- [ ] Dispatch AU Mic disk_measurements sub-agent (resolved edge-on)
- [ ] Dispatch ε Eri disk_measurements sub-agent (three-belt structure)
- [ ] Dispatch τ Cet disk_measurements sub-agent (single broad belt)
- [ ] Dispatch 61 Vir disk_measurements sub-agent (single cold belt)
- [ ] Dispatch HD 69830 disk_measurements sub-agent (warm asteroid-belt analog)
- [ ] Dispatch δ Pav disk_measurements sub-agent (single cold belt, SED-only)

Each sub-agent's input contract:
- Star slug + display name
- Path to its Phase 3 markdown (`docs/phase3/<slug>.md`)
- Path to its workspace context-notes (`phase3/<slug>/context-notes.md` where present, or skip if absent — main provides what's available)
- The committed disk_measurements schema (inline)
- Output: direct write to `db/systems/<slug>.json` with `raw.disk_measurements` array populated

Each sub-agent's output contract:
- Modified `db/systems/<slug>.json` with `disk_measurements` array
- A short report listing: number of entries written, which paper got `recommended: true`, any field that had to be left null with reason

## Step 1.3 — Post-receipt validation + commit (main)

- [ ] For each returned db json: spot-check 1 entry's bibcode + values against the source Phase 3 markdown (Step 10 VERIFY analog)
- [ ] Run `python3 scripts/pipeline/validate.py` — exits 0
- [ ] Run `bash scripts/check.sh` — no new failures vs baseline
- [ ] Update each Phase 3 markdown's `## Open items for follow-up` — mark `disk_measurements ingest` item as resolved with commit hash (8 small edits, batched into the same commit)
- [ ] Update each `ko/docs/phase3/<slug>.md` Open items section to match (block-parity check after)
- [ ] Run `bash scripts/check-mirrors.sh` — all 37+ pairs OK
- [ ] Batch commit: `feat(db): disk_measurements ingest for 8 disk-host stars`

## Out of scope (subsequent workspaces)

- Step 2: kopernicus-cfg disk emitter (reads the disk_measurements from DB and emits Kopernicus Ring nodes)
- Step 3: 14 planet Phase 3 syntheses across 5 stars
- Phase 2 ingest for non-disk fields (mass/radius/teff measurements arrays that are currently empty for some of the 8 stars — separate `nearstars-add-star` invocation if curation depth requires it)

## Related

- [plan](plan.md)
- [context-notes](context-notes.md)
