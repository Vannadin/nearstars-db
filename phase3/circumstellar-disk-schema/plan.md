# Circumstellar disk synthesis schema — plan

## Goal

Extend Phase 3 synthesis schema so that:

1. **Stellar Phase 3 markdown** (existing pattern, canonical = `alpha-centauri-a.md`) explicitly supports circumstellar debris-disk fields.
2. **Planetary Phase 3 markdown** supports planetary-ring and circumplanetary-disk fields.
3. The cfg-writer side (Kopernicus Ring node, attached either to star body or planet body) gets explicit field mappings.

Then retroactively synthesize the 8 disk-host stars currently in the NS catalog so the new schema has concrete inputs for the downstream cfg writers.

## Why

- NS catalog has 8 known disk-host stars (Vega, Fomalhaut, AU Mic, ε Eri, τ Cet, 61 Vir, HD 69830, δ Pav) but no disk metadata anywhere — neither in `db/systems/<star>.json` nor in any Phase 3 markdown.
- Downstream visual cfg writers (kopernicus-cfg now, Scatterer/Parallax later) have no Phase 3 field to read disk parameters from.
- Stellar Phase 3 has been done before (α Cen A/B) but its field set was never formalized in `synthesis-template.md`; only the planetary field groups are documented there. This work formalizes both.
- Planetary rings (Saturn-like) share the same Kopernicus Ring rendering primitive as stellar debris disks, just at a different parent body. The two fields groups belong in the same schema update for coherence.

## Scope

### In scope

**Schema docs (3 files in `.claude/skills/nearstars-phase3/`):**

- `references/synthesis-template.md` — add Stellar Decisions field groups (Physical / Activity / Visual / Binary-event) + Circumstellar disk subsection + Planetary ring + Circumplanetary disk subsection. Update Decision-table field map with disk + ring rows.
- `references/mod-grounded-fields.md` — add Circumstellar-disk → Kopernicus-Ring (star body) mapping + Planetary-ring → Kopernicus-Ring (planet body) mapping. Match sidecar yaml field names from existing `kopernicus-emit-workspace`.
- `SKILL.md` — Step 9.1 reference `alpha-centauri-a.md` as stellar canonical alongside `trappist-1-e.md`. Step 0 time-estimate row for stellar-only. Step 1 pre-flight note for Phase 2 `disk_measurements` escalation.

**Backward compatibility:** every Decisions row in current `alpha-centauri-a.md` and `trappist-1-e.md` maps cleanly to the new schema. No silent break.

**Per-star synthesis (8 stars):** Vega, Fomalhaut, AU Mic, ε Eri, τ Cet, 61 Vir, HD 69830, δ Pav. Each gets its own `phase3/<star>/` workspace + `docs/phase3/<star>.md` + Korean mirror + HTML build + reports index chip + per-star commit.

### Out of scope

- `kopernicus-cfg` skill updates (the cfg emitter side). The schema makes disk fields machine-readable; emitter changes follow in a subsequent workspace.
- `db/systems/<star>.json` `disk_measurements` blocks. That is Phase 2 measurement curation — `nearstars-add-star` skill. Required as Phase 3 input; if absent for a given star, escalate via Phase 2 first.
- Scatterer / EVE / Parallax cfg mapping. Those skills are gitignored (Patreon-EA per memory). `mod-grounded-fields.md` covers Kopernicus Ring only.
- Disk texture / mesh / shader asset authoring.

## Approach — two stages, agent team in Stage 2

### Stage 1 — Schema docs (main session, sequential)

Main session edits the 3 schema files. Reasons to keep this serial:

- The 3 files cross-reference each other (e.g. `synthesis-template.md` lists field names that `mod-grounded-fields.md` maps to Kopernicus). Drafting them in one head ensures consistency.
- Total scope is small enough (~400 lines added across 3 files) that parallelism would cost more in coordination than it saves.

**Verification gate:** alpha-centauri-a.md and trappist-1-e.md still pass `check_block_parity.py`. `check-mirrors.sh` exits 0. Then single commit.

### Stage 2 — Per-star synthesis (8 parallel sub-agents)

Eight stars, each a SKILL.md Steps 1–14 workflow. Pure-stellar synthesis (no planets to per-planet-bib-build) is lighter than TRAPPIST-1 scale — estimate ~1–2 h model time per star, but all eight run concurrently.

**Team structure:**

- **Main session** — coordinator. Before dispatch: schema commit, Phase 2 status pre-flight, prepare sub-agent prompts. During dispatch: 8 sub-agents fired in a single message. After receipt: per-star Step 10 VERIFY, Korean mirror, HTML build, mirrors check, commit.
- **Sub-agents (general-purpose, ×8)** — one per star, fired simultaneously. Each receives:
  - The new schema (synthesis-template.md content) inline in the prompt
  - The star's `db/systems/<star>.json` Phase 2 inputs
  - SKILL.md Steps 7–9 (deep-read, triage, English synthesis drafting)
  - Output contract: English Phase 3 markdown text + Decisions-row classification + Open items + bibliography list
- **Korean mirror + Step 10 VERIFY + HTML + commit stay with main** — style consistency (per `feedback-ko-mirror-style`), audit-trail rigor (per SKILL.md Step 10), and atomic commits matter more than further parallelism.

**Concurrency considerations:**

- arXiv `build_bibliography.py` enforces 3 s rate per IP. 8 concurrent sub-agents hitting arXiv will stall briefly (each request waits for previous to clear); not fatal, just adds a few minutes to bibliography stage. Acceptable.
- Token cost: 8 × deep-read budget runs simultaneously. User has accepted the 10–20 h total budget; concurrent execution shifts the cost into a shorter wall-clock window.
- Post-receipt processing in main is serial (Korean mirror writing can't easily parallelize while keeping style consistent). Expect main session to be busy ~30 min per star × 8 = ~4 h post-receipt work.

**Per-star commit granularity** (SKILL.md Step 14 default): one commit per star. Eight commits in Stage 2 + one schema commit in Stage 1 = nine total.

## Success criteria

- [ ] `synthesis-template.md`, `mod-grounded-fields.md`, `SKILL.md` updated; every new field has unit + typical range + source priority + Decision-table-map row + mod-mapping row
- [ ] `alpha-centauri-a.md` `check_block_parity.py` passes (no schema regression)
- [ ] `check-mirrors.sh` exits 0 after each per-star commit
- [ ] 8 disk-host stars each have Phase 3 markdown + Korean mirror + HTML + `reports.html` chip
- [ ] Every Decisions row sources to a specific paper line (SKILL.md Step 10 VERIFY)
- [ ] Every stellar `disk_present` Decision row has Confidence label and Basis cite

## Risks

| Risk | Mitigation |
|---|---|
| Schema bloat (template already long) | Group disk fields as single subsection per group; one source-priority block per group |
| Alpha Cen A backward compat break | Explicit "include only if disk_present=true" guard; backward compat validation gate |
| Phase 2 `disk_measurements` missing for some stars | Pre-flight check before each star; escalate via `nearstars-add-star` if absent. Vega/Fomalhaut/AU Mic likely have Spitzer measurements in literature; Phase 2 may need to ingest them |
| Sub-agent variance in synthesis quality | Main-session Step 10 VERIFY (paper-by-row re-check) catches issues per star before commit; one bad sub-agent doesn't cascade |
| Korean-mirror style drift (sub-agent fluent enough?) | Korean mirror stays with main session per `feedback-ko-mirror-style` |
| Time (10–20 h model time) | Per-star commits = clean checkpoints; user can pause/resume between stars |

## Related

- [checklist](checklist.md) — concrete tasks
- [context-notes](context-notes.md) — decision log
- [nearstars-phase3 SKILL](../../.claude/skills/nearstars-phase3/SKILL.md) — workflow this work extends
- canonical structural example for stellar: [`alpha-centauri-a.md`](../../docs/phase3/alpha-centauri-a.md)
- canonical structural example for planetary: [`trappist-1-e.md`](../../docs/phase3/trappist-1-e.md)
- existing planetary-ring sidecar yaml work: [`kopernicus-emit-workspace`](../kopernicus-emit-workspace/context-notes.md)
