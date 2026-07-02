# Principia interstellar-precision custom branch — checklist

Goal: produce a **design draft** for a custom Principia branch that lets one
simulation span Sol AND a remote star (e.g. Alpha Centauri, 4e16 m) with full
per-star orbital precision — solving the flat-frame / single-`double` position
storage limit identified in `principia-docs/interstellar-audit.md §7`.

Deliverable form (assumption, adjustable): rigorous design doc + code-level
sketches (files/templates/signatures to change), NOT a compiling fork by the 7th.

## Ground truth (fable agents, against current master 440310a9)
- [x] Geometry/frame layer — Frame tag, Position storage, rigid transforms
- [x] Dynamic reference frames — ReferenceFrame<Inertial,This>, RigidMotion, reuse potential
- [x] Ephemeris + trajectories + integrator state — cancellation site, DoublePrecision API
- [x] KSP plugin plumbing — single Ephemeris<Barycentric>, World re-centring, P/Invoke precision

## Synthesis (Opus)
- [x] Reconcile 4 reports; confirm audit §7 claims on current master (line drift)
- [x] Decide architecture: per-star SUBSYSTEM ephemeris (local storage + DoublePrecision inter-origin offset), reusing dynamic-reference-frame machinery
- [x] Write design draft: problem, architecture, changed files/signatures, migration, risks, prototype plan → design-draft.md
- [x] ko mirror (reader-facing → CONVENTIONS) → ko/plans/principia-interstellar-branch/design-draft.md

## Open decisions for owner / 슐츠
- [ ] Deliverable depth (design doc only vs skeleton fork)
- [ ] Scope: perturber-only (data, no code) vs full per-star play precision
- [ ] Whether to contribute back to schultz-dev0/principia-docs

## 2026-07-02 — deep research (3 workstreams) + hand-off spec
- [x] R1 FP precision (opus) → research/R1-fp-precision.md
- [x] R2 SOI code map (opus) → research/R2-soi-code-map.md
- [x] R3 SOI numerics/correctness (opus) → research/R3-soi-numerics.md
- [x] R4 thrust under warp (opus+web) → research/R4-thrust-under-warp.md
- [x] Synthesis → impl-spec.md (WS1→WS2→WS3, unified partition, taper-not-hard-zero)
- [x] ko mirror of impl-spec.md → ko/plans/principia-interstellar-branch/impl-spec.md
- [ ] hand off to fable (owner drives in separate session)
