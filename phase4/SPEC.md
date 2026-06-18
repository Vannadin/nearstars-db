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

## 1. Decision taxonomy — what Phase 4 decides

| Class | Driver | Example |
|---|---|---|
| **A. Window selection** | choose within Phase 3 error bars / Canonical alternatives | Barnard *e* = 0.015 (within Basant favored < 0.02) |
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

The persisted, gated decisions for one system. Emitters read this layer; the DB stays
untouched.

```yaml
system: barnards_star
decisions:
  - body: Barnard b           # or "<system>" for a system-wide choice
    field: eccentricity       # eccentricity | semi_major_axis_au | inclination_deg
                              #  | mass_* | atmosphere_* | visual_* | ...
    phase4_value: 0.015
    driver: engine+window-selection      # taxonomy class(es)
    phase3_default: 0.03                 # what Phase 3 presented
    phase2_measured: 0.03                # the measurement (for the divergence audit); DB keeps this
    gate:
      criterion: [stability, error-bar]
      verdict: pass-in-window            # | documented-divergence
      evidence: >
        WHFast 1 Myr at e=0.015 stays bounded (|dE/E| small, e calm); Basant et al.
        2025 favour e<0.02; the system has survived ~10 Gyr (dynamical-survival argument).
      divergence_note: null              # required iff verdict == documented-divergence
    refs: ["2025ApJ...982L...1B"]
    status: staged                       # staged → gated → emitted
```

- **`status`** lifecycle: `staged` (drafted, gate not yet run) → `gated` (gate passed,
  recorded) → `emitted` (a cfg writer has consumed it).
- A **fiction body (class D)** record additionally carries the full body definition
  (mass, radius, parent, orbit) since there is no DB entry to inherit from.
- Orbit-optimization conclusions are cross-referenced to `phase4/orbit-optimizations.md`
  (process + numbers) and the Phase 3 report (cfg-ready a/e/i + Canonical alternatives).

---

## 4. cfg connection

```
db/systems/<slug>.json   (Phase 2 measured + Phase 3 synthesised, derived)  ─┐
docs/phase3/<body>.html  (Phase 3 decisions, confidence, alternatives)       ├─► cfg writer ─► final cfg
phase4/<system>.yaml     (Phase 4 gated overrides + fiction bodies)         ─┘   (kopernicus / principia / firefly)
```

- Writers apply Phase 4 overrides **last**, on top of the DB/Phase-3 values; absent a
  Phase 4 record, the Phase 3 value passes through unchanged.
- The transient stability-sim flags (`run.py --ecc`, `--mass-incl-deg`) are
  **experiments**, not the source of truth — the chosen value is persisted into
  `phase4/<system>.yaml`, which the writers read.
- **check.sh gate (to add):** every `field` a writer emits from Phase 4 must be
  `gated`/`emitted` with `verdict ∈ {pass-in-window, documented-divergence}`, and a
  `documented-divergence` must have a non-null `divergence_note`. Fails the build
  otherwise — the anti-silent-departure guard.

---

## 5. Worked anchors (already analysed)

- **Barnard eccentricity** — class A+B, field `eccentricity`, value 0.015, gate
  `pass-in-window` (within Basant favoured <0.02; stability-sim low-e 1 Myr bounded;
  10 Gyr survival). DB keeps the β-prior 0.03–0.08.
- **Barnard true mass** — class A, field `mass`, value = isotropic-prior median
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

Until then, `phase4/` stays a **staging area** — drafts + the orbit-optimization log,
nothing gated into the DB or emitted.

## Related
- `phase4/README.md` — staging overview
- `phase4/orbit-optimizations.md` — orbit-optimization running log
- `phase4/synthetic-orbit-noise.md` — de-perfecting policy
- `phase2/curation-data-contract/SPEC.md` — Phase 2/3 contract this extends
