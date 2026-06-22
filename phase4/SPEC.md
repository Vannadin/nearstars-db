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
| `bulk` | `mass`, `radius`, `geopotential_j2` (oblateness; Principia `j2` + `reference_radius`), `rotation_period`, `obliquity`, `spin_axis_orientation` (pole RA/Dec), `internal_heat`/intrinsic_luminosity (self-luminous giants/BDs), `age`/cooling_age (stars/WDs), `tidal_heating` (Io-type moons) |
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

> **Menu history.** 2026-06-22 (coverage audit `phase4/phase4-coverage-audit.md`): added
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
| **C. Synthetic de-perfecting** | seeded, bounded noise on default 0 / 90° / e=0 | `synthetic-orbit-noise.md` |
| **D. Measurement-less / fiction** | art-directed body with no Phase 2 | Pandora (Avatar), around Polyphemus |
| **E. Visual art-direction** | appearance within Phase 3 physical bounds | Polyphemus banded-ivory look |

Classes A–C/E modify an existing Phase 2/3 body; class D introduces a body the
Phase 1–3 pipeline cannot carry (no measurement).

---

## 2. The 고증 gate — two verdicts

Every decision resolves to one of:

- **`pass-in-window`** — the value lies inside the Phase 3 defensible window (an error
  bar, a Canonical-alternative, or a physical bound). Emits directly; the record names
  the window it sits in.
- **`documented-divergence`** — the value lies outside the window but is justified
  (gameplay / engine). Emits **with** a divergence record: the canonical value, why we
  depart, and the magnitude of the departure.

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
layer; the DB stays untouched. A row exists for every axis the owner has touched or
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
- **check.sh gate (to add):** every `axis` a writer emits from Phase 4 must be
  `gated`/`emitted` with `verdict ∈ {pass-in-window, documented-divergence}`, and a
  `documented-divergence` must have a non-null `divergence_note`. Fails the build
  otherwise — the anti-silent-departure guard.

---

## 5. Worked anchors (already analysed)

- **Barnard eccentricity** — class A+B, axis `orbit.eccentricity`, value β-prior × 0.8
  (c ≈ 0.064), gate `pass-in-window` (closest-to-observed value verified fixed-step
  stable at the adopted median mass; below the measured β-prior; ~10 Gyr survival). DB
  keeps the β-prior 0.03–0.08.
- **Barnard true mass** — class A, axis `bulk.mass`, value = isotropic-prior median
  (i=60°, ×1.155), gate `pass-in-window` (the statistical central true mass, far below
  the ×3 dynamical ceiling). DB keeps M·sin i.
- **Polyphemus / Pandora** — class D+E (`polyphemus-art-direction.md`), gate = stability
  (Pandora Hill-bound at 0.02 R_Hill; Polyphemus HZ-stable a=1.6/e=0.1/i_mut=16°) +
  composition checklist.
- **Synthetic orbit noise** — class C (`synthetic-orbit-noise.md`), gate = transit-
  preserving inclination bound + stability.

---

## 6. Activation criteria — what "building Phase 4" means

Phase 4 is *built* when:
1. `phase4/<system>.yaml` files exist for the confirmed roster (mostly pass-through of
   Phase 3, plus the staged decisions above).
2. A validator enforces the schema + the check.sh emit gate (§4).
3. The cfg writers (kopernicus / principia / firefly) read the Phase 4 layer.

Until then, `phase4/` stays a **staging area** — `<system>.yaml` decision boards +
`*-art-direction.md` 4a drafts + the `synthetic-orbit-noise.md` policy, nothing gated
into the DB or emitted.

## Related
- `phase4/README.md` — staging overview
- `phase4/<system>.yaml` — per-system decision boards (the progress record)
- `phase4/synthetic-orbit-noise.md` — de-perfecting policy
- `phase2/curation-data-contract/SPEC.md` — Phase 2/3 contract this extends
