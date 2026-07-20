<!-- Phase 4 데이터 계약 — art-direction을 고증 게이트로 검증해 게임용 최종 cfg 값을 확정하는 레이어의 정의 -->
# NearStars Phase 4 — Art-Direction Gate Data Contract

Phase 4 is the layer where **user art-direction and engine/gameplay-driven choices**
are validated against a **고증 (canonical-consistency) gate** and persisted as the
**final, cfg-bound values**. Phase 3 *presents* a physically defensible window and an
interesting-first default; Phase 4 *chooses* within (or, with documentation, beyond)
that window and freezes the choice for emission.

This contract formalizes the three pieces the Phase 4 backlog left open: the **gate
format**, the **decision record schema**, and the **cfg connection**.

## Phase distinction (invariant)

- **Phase 2 = paper-cited measurements** — the curated DB (`db/*_curated.json`).
- **Phase 3 = cfg-ready synthesis** — values synthesized from Phase 2, presented with
  confidence + `## Canonical alternatives`.
- **Phase 4 = art-direction-gated final cfg values** — a selection/override layer on
  top of Phase 2 + Phase 3.

**HARD RULES (never violated by Phase 4):**
1. Phase 2 (the curated DB) and Phase 3 reports are **never mutated** by Phase 4.
2. Emission stays deterministic: `cfg = f(db/systems, phase3, phase4)`.
3. Every emitted Phase 4 value is either **inside the Phase 3 window** or carries a
   **documented divergence** record. No silent departures from canonical.

---

## 0. How Phase 4 actually runs — per-decision, not sequential

Phase 4 is **not** "finish all the art-direction, then gate it all." Work arrives
ragged and per-axis: the orbit is settled while the colour is still a sketch and the
aurora is untouched. So the unit of Phase 4 is **one decision = (body × axis)**, and
each decision flows on its own clock through two **roles**:

- **4a — art-direction (owner).** State the intent for that one axis. May be empty
  ("no art-direction") — then the axis just rides the Phase 3 default.
- **4b — gate (agent).** Check that one 4a target against Phase 2 + Phase 3 →
  `pass-in-window` / `documented-divergence` (§2), and write the cfg-ready value.

There is no project-wide "4a is done" moment. The only meaningful question is
per-row: *what state is this (body, axis) in?* So 4a says *what we want* for a cell;
4b says *whether it's defensible and how to emit it*. The gate criteria, record
schema, and cfg wiring below are all the **4b** machinery.

### Decision axes — fixed menu, uniform across all body types

Every body draws from the **same** axis menu — the menu is **never pruned by body
type**. A rocky planet still carries `appearance.rings` (a rocky world *can* have a
ring); it simply defaults to none. This removes the "how do I decompose the visual"
problem: the decomposition is fixed up front.

| group | axes |
|---|---|
| `identity` | `body_type`/spectral_class, `designation` (e.g. Roman-numeral moons), `cultural_name` (in-game blurb text), `discoverability` (notability / discovery difficulty) |
| `orbit` | `semi_major_axis_au`, `eccentricity`, `inclination_deg`, `longitude_ascending_node`, `argument_periapsis`, `mean_anomaly`/epoch, `spin_orbit_resonance`/tidal-lock, `lagrange_placement` (trojans / co-orbitals) |
| `bulk` | `mass`, `radius`, `gravity` (derived echo of GM/R² — Kopernicus geeASL slot), `geopotential_j2` + `reference_radius` (oblateness; Principia `j2` — always emitted as a pair), `flattening` (derived echo of the figure — visual oblate-mesh slot), `geopotential_c22` (tidal triaxiality — locked bodies), `j4` (fast rotators, optional), `rotation_period`, `obliquity`, `spin_axis_orientation` (pole RA/Dec), `internal_heat`/intrinsic_luminosity (self-luminous giants/BDs), `age`/cooling_age (stars/WDs), `tidal_heating` + `tidal_surface_flux` (Io-type moons) |
| `atmosphere` | `composition`, `pressure`, `temperature`, `scale_height`, `breathability`/oxygen (stock O₂ flag), `greenhouse` (surface vs equilibrium T), `escape`/loss |
| `surface` | `surface_type` (rock/ice/lava/ocean), `hydrosphere`/ocean, `ice_caps`/glaciation, `tectonics`/volcanism, `terrain` (Parallax heightmap / biomes), `surface_temperature`, `albedo`, `biosphere` |
| `appearance` | `banding`/base-colour, `clouds`, `haze`, `aurora`, `rings`, `surface`, `emission_glow` (lava / self-luminous / night-side), `specular` (ocean glint), `artificial`/city-lights, **[stars]** `granulation`, `limb_darkening`, `spots_faculae`, `corona`, `flares`, **[pulsar]** `beam` |
| `magnetism` | `magnetic_field` (dynamo surface field), `magnetosphere` (standoff / belt extent), `radiation_belts` |
| `environment` | `radiation` (Kerbalism dose zones), `stellar_wind` (mass-loss), `activity` (rotation/cycle/X-ray — stars), `heliosphere` (astrosphere extent), `flares`/space-weather (CME / storms), `uv_xray_flux`, `habitable_zone` (stars) |
| `rings` | `ring_structure` (radii / gaps), `ring_composition`/color/opacity, `ring_plane` (inclination), `circumstellar_disk` (debris belt), `asteroid_belt` |
| `satellites` | art-directed / fiction moons (class D) as a list, `co_orbitals`/trojans, `dust_sources` (ring feeders) |
| `gameplay` | `sphere_of_influence_tuning`, `science_biomes`, `timewarp_limits`, `difficulty` — *KSP-specific; almost always passthrough* |

The menu is the **union of decision axes any body type could need** — never pruned by type
(a rocky moon still carries `rings` and `magnetism`; they just default to passthrough). Most
axes on most bodies are `passthrough`; Phase 4 only records the deltas. `identity` and
`gameplay` are meta groups that are passthrough for nearly every body.

> **Menu history.** 2026-06-22 (coverage audit `phase4/_audit/phase4-coverage-audit.md`): added
> `magnetism`, `environment`, `surface`, `rings`, `identity`, `gameplay` groups and expanded
> `orbit`/`bulk`/`atmosphere`/`appearance`/`satellites` to the full union above — the α Cen
> audit found the planet's dynamo field (drives aurora + moon radiation), the stars'
> wind/activity (drive the heliosphere), surfaces, and ring/disk structure all lacked axes.

### Per-row status — this is the progress board

Each decision carries a status; a system's `decisions[]` list (§3) **is** the Phase 4
progress board for that system:

- `passthrough` — no art-direction; the Phase 3 default emits unchanged. **Most rows
  are this** — Phase 4 is only the *deltas* from Phase 3, never a blank to fill in.
- `open` — a decision is required but not yet made (a blocking TODO: a cfg-frame
  conversion still owed, or an axis the owner hasn't art-directed yet).
- `art-directed` — a 4a target is stated; the 4b gate has not run.
- `gated` — 4b passed; value + verdict frozen.
- `emitted` — a cfg writer has consumed it.
- `superseded` — the decision was replaced by a later one (kept for provenance; carries no
  live gate and is never emitted). The row that supersedes it is the live one.

"What is left in Phase 4" = the `open` + `art-directed` rows (`grep status:`).

### Soft coupling — gate inputs, not scheduling

A 4b gate for an `appearance` axis reads the `orbit` / `bulk` / `atmosphere` values
as **fixed context** (you need the temperature to gate a band colour). So there is a
soft "physical axes inform appearance gates" ordering — but it is a *gate-input*
dependency, not a blocker: an `appearance` 4a can start against the current best
physical value before that value is itself `gated`.

---

## 1. Decision taxonomy — what Phase 4 decides

| Class | Driver | Example |
|---|---|---|
| **A. Window selection** | choose within Phase 3 error bars / Canonical alternatives | Barnard *e* × 0.8 (closest-to-observed stable; within the RV eccentricity band) |
| **B. Engine-driven optimization** | the game engine forces a choice | low-*e* for Principia fixed-step stability; body culling for perf |
| **C. Synthetic de-perfecting** | seeded, bounded noise on default 0 / 90° / e=0 | `policies/synthetic-orbit-noise.md` |
| **D. Measurement-less / fiction** | art-directed body with no Phase 2 | Pandora (Avatar), around Polyphemus |
| **E. Visual art-direction** | appearance within Phase 3 physical bounds | Polyphemus banded-ivory look |

Classes A–C/E modify an existing Phase 2/3 body; class D introduces a body the
Phase 1–3 pipeline cannot carry (no measurement).

---

## 2. The 고증 gate — four verdicts

Every decision resolves to one of:

- **`pass-in-window`** — the value lies inside the Phase 3 defensible window (an error
  bar, a Canonical-alternative, or a physical bound). Emits directly; the record names
  the window it sits in.
- **`documented-divergence`** — the value departs from a **paper-cited value or model**
  (a measurement / published model in the literature). Reserved for divergence *from the
  science*. Emits **with** a `divergence_note` (the literature value, why we depart, the
  magnitude) and **requires** `refs[]` naming the paper(s) diverged from.
- **`methodology-derived`** — the value was **computed by one of our own ADS-grounded
  methodology recipes** (`docs/reference/methodology-index.md`: figure J2/C22, dynamo
  B-field, Cassini obliquity, tidally-locked temperature, mass–radius, tidal heating,
  internal-heat luminosity, surface / atmosphere / stellar / disk color, …). Not a
  departure and not an art pick — a grounded derivation. `refs[]` names the methodology's
  grounding paper(s); the recipe / any assumed inputs go in `narrative`. No
  `divergence_note`.
- **`owner-override`** — the value departs from a **non-paper baseline**: a prior
  art-direction choice, an AI-synthesized Phase 3 default, canon ([GAME]/[FILM]/wiki), or
  an analogy / heuristic tie-break. The rationale lives in the **`narrative`**, not in a
  `divergence_note`. `refs[]` optional.

**Distinguish the two divergence kinds.** Departing from a paper (`documented-divergence`)
and departing from a prior art choice / AI default (`owner-override`) are separate
categories — never collapse them. The test: *is there a paper whose value/model we are
contradicting?* If yes → `documented-divergence` (cite it in `refs[]`). If the baseline is
an earlier art pick, an AI-generated default, canon, or an analogy → `owner-override`.

**`divergence_note` is paper-divergence-only.** It may appear **iff** the verdict is
`documented-divergence`. Non-paper rationale goes in `narrative`.

A choice among Phase 3's `## Canonical alternatives` is `pass-in-window` by
construction (Phase 3 already vetted those readings).

### Gate criteria by axis

| Axis | Criterion | Automated? |
|---|---|---|
| Orbital (a / e / i) | dynamical stability (stability-sim: survives the play window **and** Principia fixed-step fidelity) **and** within Phase 2 error bars | **yes** (stability-sim verdict + numeric bound check) |
| Mass | within Msini → true-mass envelope; not past the dynamical ceiling | **yes** |
| Atmosphere / composition | physical & chemical consistency with Phase 3 synthesis bounds | checklist |
| Visual | blackbody / SED plausibility, Phase 3 colour window | checklist |
| Fiction body (D) | Hill + HZ stability (host stays HZ-stable, moon stays Hill-bound) + composition plausibility | **yes** (stability) + checklist (composition) |

The gate is **hybrid**: quantifiable axes (stability, error bars) are checked
automatically; perceptual axes (visual, composition) are a human checklist staged in a
`phase4/` draft.

---

## 3. Decision record schema — `phase4/<system>.yaml`

One file per system; one `decisions[]` row per **(body, axis)**. Emitters read this
layer; the DB stays untouched.

**Naming contract (2026-07-20, owner-confirmed — the emit join).**

- **Board filename** = `to_file_slug(system_name)` of the host component's db file
  (`scripts/pipeline/_naming.py`), and the in-file `system:` field equals the
  filename stem. Precedent: `tau_cet.yaml` ↔ db `system_name: "tau Cet"` (the
  earlier `tau_ceti.yaml`, slugged from the display name "tau Ceti", was renamed —
  never slug from a display form).
- **Board granularity** = one board per dynamical host group: a tight pair gated
  as one unit shares a board (`alpha_centauri.yaml` = A + B + A b system); a
  gravitationally distinct host with its own planetary system gets its own board
  (`proxima_cen.yaml`). Working dirs in phase2/3 may scope wider
  (`phase2/alpha_centauri_proxima/`) — that is a topic scope, not a slug.
- **`body:` keys** must equal the db `name` **exactly** (stars: `stars[].name`,
  planets: `planets[].name` — e.g. `Proxima Cen b`, not `Proxima Centauri b`).
  The emitter joins board rows to db bodies by exact string; there is no alias
  table. Invented bodies (class D satellites) have no db row — for them the board
  is the naming authority and every later reference reuses the board's string
  verbatim (`Proxima Cen c I`, `Pandora`). Display/prose names inside `narrative`
  are free. A row exists for every axis the owner has touched or
that carries an `open` TODO; untouched axes need no row (they are `passthrough` by
default), though a board may list them explicitly to show coverage.

```yaml
system: barnards_star
decisions:
  - body: "*"                    # a single body name, or "*" for all planets
    axis: orbit.eccentricity     # group.name from the fixed menu (§0) — never free-form
    status: gated                # passthrough | open | art-directed | gated | emitted
    op: scale                    # set | scale (how value applies over the Phase 3 default)
    value: 0.8
    driver: engine+window-selection        # taxonomy class(es), §1
    phase3_default: "β-prior (c≈0.08)"      # what Phase 3 presented
    gate:
      criterion: [stability, error-bar]
      verdict: pass-in-window               # | documented-divergence
      evidence: >
        median-mass WHFast 1 Myr clean (|dE/E|=6.5e-9, e_max≤0.085); below the
        measured β-prior; ~10 Gyr dynamical survival.
      divergence_note: null                 # required iff verdict == documented-divergence
    refs: ["2025ApJ...982L...1B"]
```

- **`axis`** is `group.name` from the fixed menu (§0) — never a free-form field name.
- **`status`** lifecycle as in §0; a `passthrough` row carries no `gate` block.
- A **fiction body (class D)** row under `satellites` additionally carries the full
  body definition (mass, radius, parent, orbit) — there is no DB entry to inherit from.
- For an optimized orbit, the **process + numbers** live in
  `phase3/stability-sim/STABILITY_REPORT.md`; the **conclusion** is the row here. (The
  former cross-system `orbit-optimizations.md` running log is retired into these rows.)

### 3.1 Schema v2 — typed `fields` + `narrative` (the emit-parseable form)

The v1 shape above assumes **one row = one `group.name` field**. In practice a curated
decision bundles many quantities and a paragraph of reasoning (a `bulk` decision fixes
mass *and* radius *and* J2, with prose). Exploding those into dozens of atomic rows loses
the reasoning and bloats the board. **Schema v2** keeps **one row per (body, axis group)**
but makes it machine-readable: a typed `fields:` list (one entry per emit field) plus the
human `narrative:`. A file opts in with a top-level `schema_version: 2`; without it the
file is legacy v1 (soft-checked, not emit-ready).

```yaml
schema_version: 2
system: alpha_centauri
status: staged
decisions:
  - body: "Alpha Centauri A b"      # exact display name
    kopernicus_name: Polyphemus     # optional — the cfg-internal name emitters/RB need
    axis: bulk                      # a §0 group (or group.name for a single-field decision)
    status: gated                   # passthrough|open|art-directed|gated|emitted|superseded
    driver: [window-selection, art-direction]   # taxonomy class(es), §1
    narrative: >                    # human prose — reasoning, context (KR ok)
      1.0 R_Jup 저신뢰 반경, J2는 자전+조석 figure에서 도출 …
    fields:                         # one typed entry per emit field — the machine layer
      - name: radius                # → bulk.radius
        value: 1.0
        unit: R_jup
        op: set                     # set | scale | passthrough
        phase3_default: "1.0 R_Jup (low)"
      - name: geopotential_j2       # → bulk.geopotential_j2 (Principia j2 + reference_radius)
        value: 0.023
        reference_radius_km: 71492
        op: set
        verdict: pass-in-window     # optional per-field; else inherits gate.verdict below
        divergence_note: null       # required iff THIS field's verdict == documented-divergence
    gate:
      criterion: [observation]
      verdict: pass-in-window       # row-level default verdict
      evidence: >
        …reproducible pointer / error bar / window…
      divergence_note: null         # required iff row verdict == documented-divergence
    refs: ["2508.03814"]            # bibcodes / arXiv ids as a machine-readable list
    discoverability_cfg:            # promoted structured block (identity axis)
      category: naked_eye
      ignorelevels: "T T T T"
      message: null                 # ONDISCOVERY text (required for candidate/disputed)
      ref: "2018AJ....155..117M"    # detection bibcode (not prose)
```

**Rules v2 adds over v1:**
- `axis` is a §0 **group** (with a `fields:` list) *or* a `group.name` (with a single
  top-level `value`). The group must be in the §0 menu; each `fields[].name` should be a
  §0 axis name.
- Every emit number lives in a typed field (`value` + `unit`/`op`), never only in prose.
- The gate block uses the schema keys **`evidence`** and **`divergence_note`** — not
  `note`/`paper`/`rationale`. Source citations go in `refs` (machine-readable), not prose.
- `verdict: partial` is **illegal** — split into a `pass-in-window` field and a
  `documented-divergence` field (each with its own note).
- `divergence_note` is required (non-null) wherever a verdict is `documented-divergence`,
  and is **allowed only there** — never on `owner-override` / `pass-in-window` rows (their
  rationale goes in `narrative`). `documented-divergence` additionally **requires** a
  non-empty `refs[]` (the paper diverged from). These are check.sh guards.

### 3.2 Bulk template convention — fixed per-class fieldsets (2026-07-12)

The pre-skill era bundled un-chosen elements into ad-hoc `bulk` rows with whatever
fields were at hand, so the fieldset drifted per body. To make "absent" distinguishable
from "forgotten", every body's bulk coverage now follows a **class template**:

- Every real body (not the `*` wildcard) with any live row carries **exactly one live
  `axis: bulk` group row** — the anchor — tagged with a `body_class`:
  `star | tidally_locked | free_rotator`.
- **Core fields (all classes):** `mass`, `radius`, `gravity`, `rotation_period`,
  `spin_axis_orientation`, `geopotential_j2`, `reference_radius`, `flattening`, `age`.
- **star** = core. (`cooling_age` satisfies the age slot for WDs; no obliquity —
  the spin axis itself is the decision — and no c22/internal_heat slots.)
- **tidally_locked** = core + `obliquity` (≈0 confirm) + `geopotential_c22` +
  `internal_heat` (+ optional `tidal_heating`/`tidal_surface_flux` for Io-types).
- **free_rotator** = core + `obliquity` (a real choice) + `internal_heat`;
  `geopotential_c22` is physically absent → recorded as n/a (below), never omitted.
- **Union rule:** a template slot is satisfied by an entry in the anchor row's
  `fields[]` **or** by a live dedicated `bulk.<name>` row for the same body (the
  post-skill style for heavy-narrative decisions — J2, spin axis). Never duplicate a
  value in both places; the per-body HTML page renders them adjacent anyway.
  `intrinsic_luminosity` satisfies the internal_heat slot, `cooling_age` the age slot.
- **n/a representation:** the field entry stays present with `value: null` plus a
  non-empty `na_reason` (e.g. `"free rotator — no tidal triaxiality"`). A field with
  neither value nor na_reason is a validator error.
- **Severity split:** template *structure* is hard (missing anchor row, missing/invalid
  `body_class`, a value-less field without na_reason → validator errors); template
  *coverage* is soft (a slot not yet walked → validator warning). Phase 4 is
  per-decision — an un-walked slot is open work made visible, not a schema failure,
  and the warning list is exactly the "forgotten vs omitted" detector.
- **gravity guard:** `gravity` is a derived echo (GM/R², the Kopernicus geeASL slot),
  kept for emit convenience by owner decision. The validator warns when it drifts
  from the row's own mass/radius by more than ~2%.
- **flattening:** derived echo of the figure decision, kept as a direct visualization
  slot (VertexHeightOblateAdvanced / oblate mesh) by owner decision (2026-07-13), like
  gravity. Definition: f = (R_eq − R_pol)/R_eq. Derivation (body-figure-methodology.md):
  stars/free rotators f = (3·J₂ + q)/2 (first-order hydrostatic, inverted §2 relation);
  tidally-locked triaxial bodies f = (5/2)·J₂ (mean-equatorial spheroid — the full
  a−c egg axis ≈ 4·J₂·R stays in the J2/C22 row notes). Undecided figure → the slot
  stays open (coverage warning), same as J₂.

---

## 4. cfg connection

```
db/systems/<slug>.json   (Phase 2 measured + Phase 3 synthesised, derived)  ─┐
docs/phase3/<body>.html  (Phase 3 decisions, confidence, alternatives)       ├─► cfg writer ─► final cfg
phase4/<system>.yaml     (Phase 4 gated overrides + fiction bodies)         ─┘   (kopernicus / principia / firefly)
```

- Writers apply Phase 4 overrides **last**, on top of the DB/Phase-3 values; absent a
  Phase 4 record, the Phase 3 value passes through unchanged.
- The transient stability-sim flags (`run.py --set/--scale`, `--mass-incl-deg`) are
  **experiments**, not the source of truth — the chosen value is persisted into
  `phase4/<system>.yaml`, which the writers read.
- **check.sh gate (implemented):** `scripts/check_phase4_gate.py` (check.sh gate 8)
  enforces, on every `schema_version: 2` board, that a `gated`/`emitted` row has
  `verdict ∈ {pass-in-window, documented-divergence, owner-override, methodology-derived}`, that any
  `documented-divergence` carries a non-null `divergence_note` **and** a non-empty `refs[]`
  (the paper diverged from), and that `divergence_note` appears **only** on
  `documented-divergence` rows (non-paper rationale belongs in `narrative`). Legacy (v1)
  boards are soft-warned, not failed, so migration can proceed file-by-file. This is the
  anti-silent-departure guard.

---

## 5. Worked anchors (already analysed)

- **Barnard eccentricity** — class A+B, axis `orbit.eccentricity`, value β-prior × 0.8
  (c ≈ 0.064), gate `pass-in-window` (closest-to-observed value verified fixed-step
  stable at the adopted median mass; below the measured β-prior; ~10 Gyr survival). DB
  keeps the β-prior 0.03–0.08.
- **Barnard true mass** — class A, axis `bulk.mass`, value = isotropic-prior median
  (i=60°, ×1.155), gate `pass-in-window` (the statistical central true mass, far below
  the ×3 dynamical ceiling). DB keeps M·sin i.
- **Polyphemus / Pandora** — class D+E (`art-direction/polyphemus-art-direction.md`), gate = stability
  (Pandora Hill-bound at 0.02 R_Hill; Polyphemus HZ-stable a=1.6/e=0.1/i_mut=16°) +
  composition checklist.
- **Synthetic orbit noise** — class C (`policies/synthetic-orbit-noise.md`), gate = transit-
  preserving inclination bound + stability.

---

## 6. Activation criteria — what "building Phase 4" means

Phase 4 is *built* when:
1. `phase4/<system>.yaml` files exist for the confirmed roster (mostly pass-through of
   Phase 3, plus the staged decisions above).
2. A validator enforces the schema + the check.sh emit gate (§4).
3. The cfg writers (kopernicus / principia / firefly) read the Phase 4 layer.

Until then, `phase4/` stays a **staging area** — `<system>.yaml` decision boards +
`*-art-direction.md` 4a drafts + the `policies/synthetic-orbit-noise.md` policy, nothing gated
into the DB or emitted.

## Related
- `phase4/README.md` — staging overview
- `phase4/<system>.yaml` — per-system decision boards (the progress record)
- `phase4/policies/synthetic-orbit-noise.md` — de-perfecting policy
- `phase2/curation-data-contract/SPEC.md` — Phase 2/3 contract this extends
