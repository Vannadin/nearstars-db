---
name: nearstars-phase4
description: >
  Run NearStars Phase 4 — gate owner art-direction and engine/gameplay
  choices against the Phase 2/3 window, and record them as cfg-ready
  overrides in phase4/<system>.yaml (schema v2). Trigger this skill whenever
  the user wants to art-direct, gate, or board a decision — phrases like
  "Phase 4 진행", "Phase 4 돌리자", "<body> 아트 디렉션", "<body> 색/외형
  정하자", "이 궤도값으로 확정", "이 축 gated로", "고증 게이트 통과시켜줘",
  "phase4 board 갱신/만들자", "silent passthrough 확정", "art-direct <body>",
  "gate this decision", "de-perfect the orbit" — or any time the conversation
  is choosing a final value within (or, documented, beyond) the Phase 3 window
  and freezing it for emit. Output is per-(body×axis) rows in
  phase4/<system>.yaml plus the per-body board HTML. Do NOT use for Phase 3
  synthesis (nearstars-phase3), Phase 1/2 DB curation or adding a star
  (nearstars-add-star), or writing the final cfg — those are the downstream
  writer skills (kopernicus-cfg / principia-cfg / firefly-cfg /
  researchbodies-cfg). Phase 4 produces the gated override layer they consume
  last; it does not itself emit cfg.
---

# NearStars Phase 4 — Art-Direction Gate

Phase 4 is the layer where **owner art-direction and engine/gameplay-driven
choices** are validated against the **고증 (canonical-consistency) gate** and
frozen as the **final, cfg-bound values**. Phase 3 *presents* a physically
defensible window and an interesting-first default; Phase 4 *chooses* within
(or, with a documented divergence, beyond) that window.

**Automation gathers and Phase 3 proposes; in Phase 4 the owner decides and you
gate.** Your job is to turn a stated intent into a schema-valid, validator-clean
decision row — never to invent the art-direction, and never to let an
un-chosen axis silently take an engine default.

> **Scope.** The authoritative data contract is [`phase4/SPEC.md`](../../../phase4/SPEC.md):
> the fixed axis menu (§0), the decision taxonomy A–E (§1), the two gate verdicts
> (§2), and the **schema v2** record shape (§3.1). This skill assumes that contract
> is known and focuses on the *when* and *how* of running one decision. Do not
> restate the axis menu or the record schema here — link to SPEC.

## Current state (read this first — do not overclaim)

Phase 4 is **partially built**, not fully wired:

- ✅ Contract (`phase4/SPEC.md`), validator (`scripts/check_phase4_gate.py` =
  check.sh gate 8), per-body viewer (`scripts/phase4/build_phase4_html.py`).
- ✅ Boards exist for 6 confirmed systems; **only `alpha_centauri.yaml` is
  schema v2** — the other five are legacy v1 and must be migrated before they
  are emit-parseable. `trappist_1` and `luhman_16` have **no board yet**.
- ⚠️ **Emit wiring is aspirational for 3 of 4 writers.** SPEC §4/§6 say the cfg
  writers read the Phase 4 layer, but today only `researchbodies-cfg` reads
  `phase4/<system>.yaml` (and via a *mismatched* contract — it reads a top-level
  `discoverability:` list; the boards store `decisions[].discoverability_cfg`).
  `kopernicus`/`principia`/`firefly` do not read Phase 4 at all yet.
- So **Phase 4 today = authoring gated boards.** Actual cfg emit is deferred to
  project-end (owner decision). The known defects + remediation order are in
  [`phase4/_audit/emit-readiness-review.md`](../../../phase4/_audit/emit-readiness-review.md).

## Out of scope

- **Phase 3 synthesis** (windows, alternatives, confidence) → `nearstars-phase3`.
- **DB curation / adding a star / Phase 2 measurements** → `nearstars-add-star`.
- **Writing final cfg** → `kopernicus-cfg`, `principia-cfg`, `firefly-cfg`,
  `researchbodies-cfg`. Phase 4 sits **between** Phase 3 and those writers.

## Workflow Overview — per-decision, not sequential

The unit is **one decision = (body × axis)**. There is no project-wide "4a is
done" moment; each cell flows on its own clock:

```
pick (body × axis) from the fixed §0 menu
   │
   ├─ 4a  owner states intent (or "no art-direction" → passthrough)
   │
   ├─ 4b  gate against Phase 2 (DB) + Phase 3 (window / alternatives)
   │        → pass-in-window   (inside the defensible window)
   │        → documented-divergence (departs a paper; + note + refs[])
   │        → owner-override   (departs an art choice / AI default / canon; rationale in narrative)
   │
   ├─ write the schema-v2 row into phase4/<system>.yaml
   │
   ├─ validate:  python3 scripts/check_phase4_gate.py   (must be 0 errors)
   │
   └─ build:     python3 scripts/phase4/build_phase4_html.py <system>
```

Most axes on most bodies are `passthrough` (Phase 3 default emits unchanged);
Phase 4 records **only the deltas** — plus explicit `passthrough`-confirm rows
where a measurement-less axis would otherwise take a silent engine default.

## Step 1 — Pre-flight: pick the decision, open the board

- Confirm Phase 3 is done for the body (there is a `docs/phase3/<slug>.html`
  report to read the window/alternatives from). If not, route to `nearstars-phase3`.
- Open or create `phase4/<system>.yaml`. **The board filename is the db system
  slug** — `to_file_slug(system_name)` from `scripts/pipeline/_naming.py`, always
  identical to the db filename (`tau_cet.yaml` ↔ `tau_cet.json`). Never slug from
  a display name (the old `tau_ceti.yaml` divergence was unified 2026-07-20).
  `body:` row keys must equal db `stars[].name` / `planets[].name` exactly —
  that string is the emit join key (SPEC §3 naming contract).
- New board? Start it with `schema_version: 2`, `system:`, `status: staged`.
- Per CLAUDE.md §7, if this is a non-trivial session keep a `checklist.md` +
  `context-notes.md` (see `phase4/emit-hardening/` for the pattern).

## Step 2 — 4a: state the art-direction (owner)

- Present **every** axis of the group as a choice — never silently pass an axis
  through. Give 2–4 options with the 고증 (canonical) reading flagged, and let the
  owner pick at least once per facet. (Convention: `CONVENTIONS.md §4.6`,
  `[[feedback_phase4_facet_choices]]`.)
- Accumulate mood/palette/feature scratch in a `phase4/<body>-art-direction.md`
  draft (like `polyphemus-art-direction.md`) — that is the owner's creative
  domain and is **not** the gated record; its conclusions land in the board.
- An axis may legitimately be "no art-direction" → it becomes a `passthrough`
  row (or stays unwritten if it already carries a measured Phase 2 value).

## Step 3 — 4b: run the 고증 gate

Resolve every decision to one of three verdicts (SPEC §2). Distinguish divergence
**from a paper** vs **from a non-paper baseline** — never collapse them:

- **`pass-in-window`** — the value lies inside the Phase 3 window (an error bar,
  a `## Canonical alternatives` reading, or a physical bound). A choice among
  Phase 3's alternatives is pass-in-window by construction.
- **`documented-divergence`** — departs from a **paper-cited value/model** (the
  science). **Requires** both a non-null `divergence_note` (literature value,
  magnitude, why) **and** a non-empty `refs[]` (the paper diverged from).
- **`methodology-derived`** — computed by one of our ADS-grounded methodology
  recipes (`docs/reference/methodology-index.md`: figure J2/C22, dynamo, Cassini
  obliquity, locked temperature, mass–radius, tidal heating, colors, …). `refs[]`
  = **the methodology doc itself** (`docs/reference/<topic>-methodology.md`), **not**
  the individual papers inside it — the provenance of a derived value is our recipe,
  and the recipe already cites its own grounding. Recipe / assumed inputs in
  `narrative`. (If the recipe doesn't exist yet, build it first via the
  `nearstars-methodology` skill, then cite it.)
- **`owner-override`** — departs from a **non-paper baseline**: a prior art choice,
  an AI-synthesized Phase 3 default, canon ([GAME]/[FILM]/wiki), or an analogy.
  Rationale goes in `narrative`; **no** `divergence_note` (paper-divergence-only).

The gate is **hybrid** — quantifiable axes are checked automatically, perceptual
axes by checklist. See [`references/gate-criteria.md`](references/gate-criteria.md)
for the axis → criterion table. Notably:

- **Orbital (a / e / i)** — dynamical stability via the stability sim
  (`phase3/stability-sim/scripts/run.py --set/--scale`), **and** within Phase 2
  error bars. The **conclusion** is the board row; the process + numbers stay in
  `phase3/stability-sim/STABILITY_REPORT.md`. The transient `run.py` flags are
  experiments, not the source of truth.
- **Mass** — within the M·sin i → true-mass envelope, below the dynamical ceiling.
- **Fiction body (class D)** — Hill + HZ stability + composition plausibility
  (**not** `culture`/`classification`; see the class-D recipe below).

## Step 4 — Record the decision (schema v2)

Write one row per (body × axis group). The full row shape, enums, and authoring
rules are in [`references/board-schema.md`](references/board-schema.md) and
`phase4/SPEC.md §3.1`. The rules the validator enforces, in short:

- Prose reasoning → `narrative:`. **Every emit number → a typed `fields[]`
  entry** (`name`, `value`, `unit`, `op`) — never buried in prose.
- **Prose readability contract** (SPEC §3.1; owner feedback 2026-07-24, hardened
  that day): `narrative` = reader-facing story (what the body *is*, why the value
  holds, conclusion first), ≤6 sentences, and it **excludes** bibcodes / file paths
  / equations / parameter dumps, **owner-decision history** (dates, "owner
  chose/declined", facet-walk logs — that lives in checklist/context-notes), and
  **engine mechanics** (biome maps, flight science, discovery mod: author knowledge,
  not story). The gate `evidence` = verification + grounding trail (tool, fit
  quality, formulas, checks, the mechanics the narrative omits); no storytelling, no
  dated decision-logs. A qualitative/non-scalar value (dose ladder, grade) stays in
  prose, not a fake typed field. **No em-dashes** (CONVENTIONS §1.10) and **natural
  Korean, no calques** (거대 가스행성 not 거인, 구름층 not 구름덱) in every rendered
  field. Simulation-derived values (stability windows, gap-clearing, phase-match) cite
  the sim report (`phase3/stability-sim/*.md`) in `refs[]`, not just a paper.
- Gate block keys are exactly `criterion` / `verdict` / `evidence` /
  `divergence_note`. Source citations → a machine-readable `refs:` list (bibcodes
  / arXiv ids only). Do **not** use `note`/`paper`/`rationale`.
- **`refs` must reveal provenance** — what kind of basis a value stands on:
  - **`passthrough` (a measured value flowing straight to emit)** → cite **all**
    the Phase 2/3 measurement papers behind it (every bibcode/arXiv id), not one
    representative pick. A passthrough row carries no gate block, so its `refs`
    live at row level.
  - **derived value** → cite the **methodology doc** (`docs/reference/<topic>-methodology.md`),
    not the papers inside it (see `methodology-derived` above).
  Never drop a single paper lifted from inside a methodology doc onto a derived
  value — the reader can't then tell a direct measurement from a recipe output.
- `verdict: partial` is **illegal** → split into a `pass-in-window` field and a
  `documented-divergence` field, each with its own note.
- `documented-divergence` (at row **or** field level) **requires** a non-null
  `divergence_note`.
- Status ∈ `passthrough | open | art-directed | gated | emitted | superseded`.
  A `passthrough` row carries **no** gate block. A replaced decision becomes
  `superseded` (kept for provenance, never emitted) and the replacement is a
  separate live row.
- The **v2 authoring exemplar is `phase4/alpha_centauri.yaml`** (the migrated
  many-axis v2 board) — model every new row's shape on it. `phase4/barnards_star.yaml`
  is **legacy v1** (uses gate keys like `rationale:` that are illegal in v2); cite it
  only for decision hygiene (the `reproduce:` pointer idea), never copy its row shape.

## Step 5 — Validate

```
python3 scripts/check_phase4_gate.py
```

- `schema_version: 2` boards are **hard-checked** (0 errors required); legacy v1
  boards are **soft-warned** so migration proceeds file-by-file. It also runs as
  **check.sh gate 8**.
- Fix every `✗` before considering a row `gated`. Warnings (missing `refs` on
  canon/no-bibcode rows) are acceptable but minimize them.

## Step 6 — Build the board HTML

```
python3 scripts/phase4/build_phase4_html.py <system>
```

Writes `docs/phase4/<system-slug>/index.html` + one **per-body** page each
(never the whole system on one page — it is too much to read at once). Each
decision renders as: axis + status/verdict pills → narrative prose → the typed
`fields` spec table → evidence / divergence / refs.

## Special procedures

- **Silent-passthrough confirmation.** A measurement-less axis that would take an
  engine default (obliquity 0, inclination 0/90, Ω/ω/M null, e=0, unforced
  rotation) must be **explicitly confirmed**, not assumed (`silent-passthrough-audit.md`).
  For tidal-locked bodies these are trivial (obliquity ≈ 0, spin = orbit normal,
  rotation = orbital period) → one `passthrough`-status row each (no gate). For
  free rotators they are real owner choices → gated rows.
- **Class-D fiction body.** A body with no Phase 2 (Pandora, Erid) carries its
  **full body definition as structured fields** (mass, radius, parent, orbit) —
  never a prose blob — and gates on **Hill + HZ stability + composition
  plausibility**, not on canon-existence. Its orbit still runs the stability sim.
- **Synthetic orbit noise.** De-perfecting default 0/90/e=0 elements uses the
  named policy in [`phase4/policies/synthetic-orbit-noise.md`](../../../phase4/policies/synthetic-orbit-noise.md):
  seeded, physically bounded, DB-invariant, **applied at the emit stage, not
  baked into the board**. Record the *intent* (flag the axis `de-perfect-at-emit`
  with the bound), never a concrete noised number. The transit-preserving
  inclination bound is the headline guardrail.
- **Emit-value pitfalls.** Kopernicus emits many facets as curves/maps, not
  scalars, with real traps (the `temperatureEccentricityBiasCurve` divide-by-zero
  on e≈0; tidal-lock-to-planet-not-star; `hazardousBody.ambientTemp`; gas-giant
  biome maps; A+B flux summing). These bite the *gate* (an e≈0 choice silently
  kills the atmosphere). See
  [`references/kopernicus-emit-pitfalls.md`](references/kopernicus-emit-pitfalls.md).

## Agent-team delegation (when Phase 3 is frozen)

Safe to parallelize **only** when Phase 3 for the body is frozen and its report
exists — parallel, no live network, narrow per-body scope. Draft agents propose
`(axis, value, window-ref)`; the **main thread runs the gate and writes the row**;
always re-run `check_phase4_gate.py` and eyeball board parity yourself — never
trust an agent's self-report. (`[[feedback_agent_token_saving]]`,
`[[feedback_audit_cost_discipline]]`.)

## Autonomy guards

- Read the board before overwriting a `gated`/`superseded` row — know what you
  are replacing. Confirm before deleting a decision (prefer `superseded`).
- Never mutate the DB (`db/systems/*.json`) or Phase 3 reports — Phase 4 is an
  override layer only (SPEC HARD RULE 1).
- Emitting cfg is out of scope — stop at the gated board.

## Common pitfalls

| Pitfall | Rule |
|---|---|
| Axis pruned by body type | Menu is uniform; a rocky moon still has `rings`/`magnetism` (default passthrough). |
| Number in prose | Every emit value in a typed `fields[]` entry, or a writer can't read it. |
| Paper vs non-paper divergence conflated | Departing a **paper** value = `documented-divergence` (+ note + `refs[]`). Departing an **art choice / AI default / canon / analogy** = `owner-override` (rationale in `narrative`, no note). Never label the latter `documented-divergence`. |
| Silent departure gated as pass | A value that leaves the Phase 3 default is never a bare `pass-in-window` — classify it as `documented-divergence` or `owner-override`. |
| `divergence_note` in `note`/`rationale`/`evidence` | Must be the `divergence_note` field, or the validator's guard is blind. |
| Silent engine default | A measurement-less axis needs an explicit `passthrough`/gated row, not assumption. |
| e ≈ 0 emitted | Trips the Kopernicus eccentricity-curve divide-by-zero → emit e ≳ 0.02 or flag suppression. |

## Related documents

- [`phase4/SPEC.md`](../../../phase4/SPEC.md) — the data contract (axis menu, taxonomy, verdicts, schema v2)
- [`phase4/README.md`](../../../phase4/README.md) — staging overview
- [`phase4/policies/synthetic-orbit-noise.md`](../../../phase4/policies/synthetic-orbit-noise.md) — de-perfecting policy
- [`phase4/_audit/emit-readiness-review.md`](../../../phase4/_audit/emit-readiness-review.md) — current defect catalog + remediation order
- [`phase4/_audit/phase4-coverage-audit.md`](../../../phase4/_audit/phase4-coverage-audit.md) · [`silent-passthrough-audit.md`](../../../phase4/_audit/silent-passthrough-audit.md) — worked coverage/silent-default sweeps
- `phase2/curation-data-contract/SPEC.md` — the parent Phase 2/3 contract this extends
- Upstream `nearstars-phase3`; downstream `kopernicus-cfg` / `principia-cfg` / `firefly-cfg` / `researchbodies-cfg`
- [`references/board-schema.md`](references/board-schema.md) · [`references/gate-criteria.md`](references/gate-criteria.md) · [`references/kopernicus-emit-pitfalls.md`](references/kopernicus-emit-pitfalls.md)
