# NearStars Pipeline Contract — Phases, Interfaces, Gates

**Status:** canonical (2026-07-20). This document is the single current definition
of the Phase 1–4 pipeline: what each phase is, what machine artifact crosses each
boundary, which key joins it, and which gate guards it. It supersedes the legacy
per-system development phases that `guideline.md` §9 carried from the original
project sketch (star skeleton / planets / visuals / polish — a different, obsolete
numbering).

Grounded in the two 2026-07-20 audits (per-system consistency + data-flow trace);
working notes in `phase2/pipeline-flow-program/`.

## 0. Phase definitions (current)

| Phase | What it is | Canonical store | Driven by |
|---|---|---|---|
| **1** | Baseline curation from public catalogs (Gaia DR3, SIMBAD, NASA EA, ORB6): identity, astrometry, binary orbits | `db/*.json` raw layers → `db/systems/*.json` (strictly derived) | `scripts/pipeline/` |
| **2** | Paper-cited measurements (per-paper `bibcode` attribution) appended to the curated layers | `db/stellar_props_curated.json`, `db/planets_curated.json`, `db/disks_curated.json` | `nearstars-add-star` skill, `apply_phase2.py` |
| **3** | cfg-ready synthesis: measurements → per-body decisions (window + interesting-first default) | `docs/phase3/<slug>.md` — the `## Decisions` table is the machine interface (§2) | `nearstars-phase3` skill |
| **4** | Owner art-direction gated against the Phase 2/3 window; frozen overrides | `phase4/<system>.yaml` (schema v2, SPEC.md) | `nearstars-phase4` skill |
| **emit** | Deterministic cfg writing, `cfg = f(db, phase3, phase4)` — deferred to project end | `dist/` | writer skills (kopernicus/principia/firefly/researchbodies-cfg) |

Phase 2 vs 3 invariant: Phase 3 inputs must be Phase 2 measurements; Phase 4 never
mutates Phase 2/3 (see `phase4/SPEC.md` "Phase distinction").

## 1. Boundary table — what crosses, on what key, guarded by what

| Boundary | Machine artifact crossing | Join key | Gate |
|---|---|---|---|
| 1→2 | `phase2/<host>/measurements.yaml` → curated JSON via `apply_phase2.py` | `system_name` + body `name` | `validate.py` (check.sh 1) |
| 2→db | curated JSON → `db/systems/*.json` via `build_systems.py` (strictly derived, never hand-edited) | `system_name`; file stem = `to_file_slug(system_name)` | `validate.py`; snake_case guard (check.sh 4b); freshness (7) |
| 2→3 | curated measurements (read by the synthesis author) + `phase3/<system>/system.yaml` (**bibliography pipeline input only** — see §5) | db names / `system_slug` | — (human judgment; bib scripts validate their own schema) |
| 3→4, 3→emit | `## Decisions` table in `docs/phase3/<slug>.md` — columns `Field / Value / Confidence / Basis`, parsed by `scripts/pipeline/phase3_decisions.py` | report slug = `to_url_slug(body name)`; row key = `Field` label | Decisions parse check (check.sh 10c) |
| 4→emit | `phase4/<system>.yaml` `decisions[].fields[]` (+ `discoverability_cfg`) | board filename = `to_file_slug(system_name)`; `body:` = db `name` **exactly** (SPEC §3 naming contract); fiction bodies marked `discoverability: fictional` | schema gate (check.sh 8); body↔db + roster gates (10a/10b) |
| all→emit | resolver output (§3) | body name | dry-run (WP1) |

## 2. Join-key registry

One body has exactly these spellings; never invent others:

- **`system_name` / body `name`** (db JSON) — display-form exact string
  (`tau Cet`, `Proxima Cen b`, `Alpha Centauri A`). The master key. phase4
  `body:` must equal it exactly.
- **file slug** = `to_file_slug(name)` — snake_case, working tree + db filenames
  (`tau_cet.json`, `phase4/tau_cet.yaml`, `phase3/tau_cet/`).
- **url slug** = `to_url_slug(name)` — kebab-case, docs tree only
  (`docs/phase3/tau-cet.md`, `docs/phase4/tau-cet/`). Planet **report** slugs
  are `to_url_slug(host name) + "-" + planet letter` — identical to the planet
  name's own slug everywhere except hosts whose db planet names omit the host
  suffix (`Barnard b` → `barnards-star-b.md`, not `barnard-b.md`).
- **`kopernicus_name`** (optional, phase4 row field) — the in-game cfg body name
  (`Polyphemus`); the only place a cultural name becomes a key.

Both slugs derive from the same `name` via `scripts/pipeline/_naming.py` — never
slug from a display variant (the 2026-07-20 `tau_ceti` incident).

## 3. Value-resolution order (target architecture)

Effective per-body value = layered merge, later wins:

```
db/systems derived  <  phase3 Decisions (parsed)  <  phase4 fields[] (gated)
```

- The merge lives in **one module**: `scripts/pipeline/resolve_emit_values.py`
  (WP1). Emitters format cfg syntax from resolver output; they do not choose
  sources themselves.
- **Current state (pre-rewiring):** principia reads db only; kopernicus/firefly
  scrape the Decisions md directly; researchbodies reads phase4 directly. The
  rewiring of all four onto the resolver is an emit-time task tracked in
  `phase4/emit-hardening/checklist.md`. Until then a phase4-only edit does NOT
  reach principia/kopernicus/firefly output — do not assume otherwise.
- A value must live in exactly one authoritative layer; restating it in prose
  (board `narrative:`) is display, never a source.
- **Field alignment (closed 2026-07-20).** phase3 Decision names and phase4
  `fields[]` names are disjoint vocabularies by design: a board records the
  owner's menu choice without units (`mass`, `radius`, `rotation_period`),
  while a Decisions row bakes the unit into the key (`mass_msun` /
  `mass_mearth` / `mass_mjup`). Left alone they never collide, so the layered
  merge silently never overrode anything. The bridge is
  **`scripts/pipeline/field_alignment.yaml`** — for each board menu name, the
  candidate phase3 keys in priority order, the implied unit per body class, and
  the downstream cfg target. The resolver picks the first candidate that the
  body's own report actually used, which is how a unit-less board value lands on
  the right unit variant per class. Coverage is enforced, not assumed: gate 10f
  warns on any board field name missing from the map (currently 93/93 mapped).
  Fields with an empty `phase3:` list are board-authoritative by design
  (gameplay axes, ring textures, fiction bodies) and emit unopposed.

## 4. Per-class done criteria (what "complete" means per phase)

Phase-2 measurement floor (categories in `stellar_props_curated.json`; [Fe/H]
optional everywhere per the standing skip-metallicity decision):

| Star class | Floor categories |
|---|---|
| FGK / M host | teff, radius, luminosity, mass, age, rotation, activity (7) |
| A-type | teff, radius, luminosity, mass, age, rotation (activity N/A — no chromospheric index; record the N/A) |
| White dwarf | teff, radius, mass, age |
| Brown dwarf | teff, radius, luminosity, mass, age |

Unresolved companions follow their own spectral class (eps Ind Ba/Bb → the BD
floor). Floor scope (owner, 2026-07-20): **all curated hosts within 50 ly**;
`beyond-implementation-range` bodies exempt. Gate 10d reports the worklist
(`check_pipeline_flow.py --floor-detail`); backfill is a scheduled curation
program. Full floor definition: `phase2/curation-data-contract/SPEC.md` §A0;
planet block shape rule (list+method canonical): §A1.

Phase 3: every db planet of an implemented host gets a report; the host star gets
a star-level report (disk content folds into it — no separate disk reports).
Phase 4: confirmed-roster systems get a board covering every db body (stars +
planets) plus gated fiction bodies; non-roster hosts need no board.

## 5. Write-only / special-role artifacts (so nobody "fixes" them wrongly)

- `phase3/<system>/system.yaml` — input to the **bibliography** scripts only
  (`run_phase3.py` etc.). Not a synthesis-value store; nothing downstream reads
  it. Absent for hand-triaged systems; that is fine.
- `docs/phase3/*.html`, `docs/phase4/**/*.html` — renders for humans; no
  machine consumer.
- `phase3/<system>/kopernicus_extras.yaml` — **deprecated before first use**:
  the kopernicus emitter references it but no instance exists. Ring/disk emit
  values resolve via phase4 `fields[]` through the resolver instead (WP1).
- `gameplay/`, `phase3/stellar_wind_synthesis/`, `phase4/figure/values.md`,
  `phase4/viewers/` — design/reference layers, consumed at authoring time, not
  by emit. (`figure/values.md` carries a known stale mass — see board notes.)

## 6. Historical phase2 layout index (authoring generations — do not restructure)

Phase 2 was authored in three generations; the notes for a host live where its
generation put them. This index is the lookup; history is not rewritten:

- **Per-host dir + measurements.yaml**: alpha_centauri_proxima (A/B/Proxima),
  trappist_1, luhman_16, hd_219134, eps_ind_a, yz_cet, gj_896_a, gj_9066, 55_cnc.
- **Per-host dir, notes only** (data applied straight to db): 40_eridani,
  delta_pavonis.
- **Batch dirs** (no per-host dir): `tier1-stellar/` → eps Eri, tau Cet, AU Mic,
  HD 69830, 61 Vir, Vega, Fomalhaut (+delta Pav follow-ups); `tier1-batch2/` →
  Barnard's star, Teegarden's star; `xray_sweep/`, `visual-batch-1/`,
  `disk-measurements-ingest/` → cross-host sweeps.
- **Going forward**: new hosts always get the per-host dir + measurements.yaml
  form (`nearstars-add-star` skill).

## Related

- [guideline.md](guideline.md) — project overview; its §9 now points here.
- [methodology.md](methodology.md) — schema and layer semantics.
- `phase2/curation-data-contract/SPEC.md` — Phase 2/3 required-data contract.
- `phase4/SPEC.md` — Phase 4 board schema + naming contract (§3).
- [tools.md](tools.md) — tool index (parsers, gates, resolver).
