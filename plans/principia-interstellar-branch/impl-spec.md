---
title: "Principia interstellar branch — implementation spec (hand-off to fable)"
status: ready-for-implementation
created: 2026-07-02
audited_against: mockingbirdnest/Principia master @ 440310a9
research: research/R1-fp-precision.md, R2-soi-code-map.md, R3-soi-numerics.md, R4-thrust-under-warp.md
---

# Principia interstellar branch — implementation spec

This is the master hand-off document. It defines **three workstreams**, their
dependency order, and the key cross-cutting decisions. Each workstream has a
detailed grounded spec in `research/R*.md` (read the matching Rn before coding
that workstream — this file is the map, they are the territory).

**Audience: a coding model (fable) driven in a separate session.** It is
self-contained: setup, order, and the reconciled design are all here.

## 0. Setup (do this first, any session)

```
git clone https://github.com/mockingbirdnest/Principia
cd Principia && git checkout -b nearstars-interstellar   # base = master @ 440310a9
```

All file:line citations in this doc and in `research/R*.md` are against master
head `440310a9`. If the head has moved, re-anchor by symbol name (the functions
are stable; line numbers drift). Principia's build is bespoke (MSVC/clang, large);
building is the practical gate on the KSP-facing commits — expect that to be the
slow part, and validate the headless C++ tests first (they need no KSP install).

## 1. The three workstreams

| # | Feature | Layer | Risk | Depends on |
|---|---|---|---|---|
| **WS1** | Long-distance FP precision (per-star local origin + DoublePrecision offset) | `physics/ephemeris*` | Low (back-compat by default) | — |
| **WS2** | SOI cutoff + grouped interaction (block-diagonal N-body + force-free coasting) | `physics/ephemeris*` | Medium (numerics) | **WS1** (shares the partition) |
| **WS3** | Continuous thrust under timewarp | `ksp_plugin/*` + adapter | Medium (KSP-facing) | independent |

**Build WS1 → WS2 sequentially** (they share one data structure — see §2).
**WS3 is independent** and can proceed in parallel; it touches a disjoint part
of the tree (`ksp_plugin/pile_up`, `manœuvre`, adapter).

## The void regime (cross-cutting)

A vessel that belongs to no subsystem — deep in the interstellar void — is a
first-class regime, not an edge case of any single workstream. Its four faces, and
where each is handled:

- **Precision**: far from every anchor, absolute coordinates carry the full
  interstellar magnitude; the subsystem split (WS1/R5) keeps integration exact and
  the sector/anchor machinery (WS6) keeps *rendering and scene placement* exact.
  A void vessel's own dynamics are trivially smooth (far-field-damped, force-free).
- **Docking / close approach**: two void vessels must share an anchor to interact
  coherently (RT-1, resolved — co-anchoring on approach).
- **Loaded parts**: scene-side coherence for vessels created/split in the void or at
  a star (WS5-C/C2 — adoption-time coherence; landed/ground-contact state is
  impossible at PQS-less bodies, enforced ecosystem-side by InterstellarFluxFix).
- **Rebase policy**: when a void coast approaches a new system, dominance + hysteresis
  (#4, mass-based, k=3 margin) decides the subsystem handoff; the band sits outside
  every reasonable Hill sphere, so no bound orbit flaps.

Anything new that touches a subsystem-less vessel starts by checking this list —
the four faces are load-bearing and already have owners; new void work extends them
rather than re-deriving.

## 2. KEY SYNTHESIS DECISION — WS1's subsystem partition IS WS2's group structure

R1 introduces `subsystem_of_body_` (per-star partition, to localize origins).
R2 independently introduces `group_ids_`/`groups_` (per-star partition, to block
the pair loop). **These are the same object. Build ONE partition that serves
both.** Reconciled structure on `Ephemeris<Frame>` (unify R1 §1.2 + R2 §3):

```cpp
// ONE per-star partition, serves both FP-locality (WS1) and interaction-grouping (WS2).
std::vector<int> subsystem_of_body_;                                   // parallel to bodies_; 0 == Sol
std::vector<DoublePrecision<Displacement<Frame>>> subsystem_origin_offset_;  // WS1: local origin per subsystem
struct BodyGroup { std::vector<std::size_t> oblate_members, spherical_members; };  // WS2: for grouped iteration
std::vector<BodyGroup> subsystem_members_;                             // derived from subsystem_of_body_
std::vector<Square<Length>> soi_cutoff_squared_;                       // WS2: per-body, fixed at ctor
```

Consequence: WS1 commit 1 already creates `subsystem_of_body_`; WS2 reuses it and
adds only `subsystem_members_` (the index-list view) + `soi_cutoff_squared_` +
the taper. Do **not** build two partitions.

Start with a **STATIC partition** (assign at construction, never recompute at
runtime). This is correct for the NearStars roster (stars don't change systems)
and sidesteps the integrator-contract hazard (R2 §6): membership must never
change *within* an integration step. Defer any dynamic re-grouping (R2 §5,
`Prolong:338` hook) unless a real need appears.

## 3. KEY SYNTHESIS DECISION — the SOI cutoff is a smooth C² taper, NOT a hard zero

The owner's stated intent (#2) was "treat gravity as *literally zero* beyond
where it converges to ~0, keep only inertia." R3 shows the intent is right but
the *literal hard-zero* is disqualifying, and gives the correct mechanism that
**still delivers force-free coasting**:

- **Correction of a shared misconception:** Principia's `QUINLAN_TREMAINE_1990_ORDER_12`
  is **not symplectic — it is a symmetric linear multistep method**
  (`integrators/methods.hpp:1041`). Its no-drift property comes from
  **time-reversibility** (force = f(q)) + **smoothness** of f, not symplecticity.
- **A hard cutoff breaks smoothness**: a step of height μ/r_c in the potential at
  the boundary injects energy every crossing → **random-walk secular drift**,
  8–12 orders larger than the bounded ~1e-13 oscillation Principia tolerates, and
  of the wrong *kind* (drift, not oscillation). It forfeits the property that
  makes Principia trustworthy.
- **The fix that keeps the owner's intent:** a **C² quintic taper on the
  POTENTIAL**, `Φ̃(r) = Φ(r)·S(r)`, `S(x)=1−10x³+15x⁴−6x⁵`, `x=(r−r₀)/(r_c−r₀)`,
  S=1 for r≤r₀, 0 for r≥r_c. Compact support ⇒ **exactly zero beyond r_c**
  (genuine force-free inertial coasting — exactly what #2 wanted), but smoothly
  ramped so the truncated system is still a smooth conservative system ⇒ no drift.
  Residual is a *static* modelling bias (physically negligible), not drift.
- **Speed** comes from a **Verlet neighbor list + skin + hysteresis** (orthogonal
  to the taper): O(N²)→O(N·k). Combine both.

**Where to apply (R3 §5):**
- **Vessel path = the primary payoff, low risk** (one-way coupling, already
  adaptive, tail genuinely negligible). Neighbor list per vessel; C² taper on
  each massive body's contribution; exactly 0 beyond r_c; site r₀ at
  a_cut/a_dominant = 1e-6. Delivers clean interstellar coasting + the dominant
  speedup. **Do this first within WS2.**
- **Backbone = secondary, careful.** Full N² *within* each bound star system;
  only *between* systems (light-years apart, below round-off) taper inter-block
  terms to zero → block-diagonal force matrix. Apply the same S(r) **symmetrically
  to both sides** of each pair (`ephemeris_body.hpp:1372-1378`) to keep momentum
  exact. If in doubt, skip the backbone cut — it is not the bottleneck.
- **Non-negotiables (R3 §5C):** taper the potential (derive force from it — never
  truncate the force independently, that makes the field non-conservative);
  symmetric per-pair on the backbone; C² minimum; validate bounded/non-drifting
  energy against `physics/ephemeris_test.cpp` + `astronomy/ksp_system_test.cpp` /
  `ksp_resonance_test.cpp` as the acceptance gate.

R2's per-pair `continue` cutoff (hard skip at `:1368`/`:1435`) is acceptable ONLY
as a Tier-A correctness scaffold placed so far out that μ/Δq² is already
machine-negligible; the shippable form is the smooth taper. Prefer building the
taper directly on the vessel path.

## 4. Per-workstream build order

### WS1 — FP precision (see `research/R1-fp-precision.md`)
1. **Commit 1 (headless precision proof, ~3 files):** add `subsystem_of_body_` +
   `subsystem_origin_offset_` members; defaulted `subsystems = {}` ctor param
   (empty ⇒ byte-identical legacy); ingest global→local in the ctor
   (`ephemeris_body.hpp:122-159`); kernel same/cross-subsystem split at `:1366`;
   thread params through call sites; add `astronomy/interstellar_precision_test.cpp`
   (two star+planet subsystems, one at 4e16 m, vs legacy control → assert remote
   separation error after < 1 mm, control > 1 m).
2. Jacobian (`:1193`) + jerk cross-subsystem split.
3. Serialization (`physics.proto:181-210` additive; empty ⇒ legacy loads unchanged).
4. Global-position accessor + plugin wiring (`plugin.cpp:128-138`); route only
   rendering through the globalizing accessor.

### WS2 — SOI cutoff (see `research/R2-soi-code-map.md` + `research/R3-soi-numerics.md`)
Reuses WS1's `subsystem_of_body_`. Build order:
1. Vessel-path C² taper + per-vessel neighbor list (R3 §5A) in the massless kernel
   (`ephemeris_body.hpp:1412-1462`) — clean coasting + main speedup, lowest risk.
   Validate energy/trajectory has no kink.
2. Backbone block-diagonal: `subsystem_members_` index lists + generalize the
   massive kernel to an index-list `b2` (R2 §2 Tier B); inter-block taper only,
   symmetric per pair. Validate no-drift energy (acceptance gate).
3. (Only if needed) mirror the treatment into Jacobian/jerk/potential kernels for
   consistency; dynamic re-grouping at `Prolong:338`.

### WS3 — thrust under warp (see `research/R4-thrust-under-warp.md`) — independent
1. Extract `ThrustAcceleration` helper from `manœuvre_body.hpp:267-278`.
2. `OnRailsBurn` on `PileUp` (`pile_up.hpp:196-197`) + the new AdvanceTime branch
   (`pile_up.cpp:572-638`) with mass depletion + dry-mass clamp.
3. Plugin API `VesselSetOnRailsBurn`/`Clear` + C interface + P/Invoke.
4. C# adapter packed-branch harvest (throttle/direction/resource drain,
   warp-halt on depletion), feature-flag gated.
5. Prediction consistency (`FlowPrognostication`) + PileUp serialization.
Principle: express the burn as an intrinsic acceleration on Principia's history;
**never write the stock KSP `Orbit`** (why PersistentThrust is incompatible —
Principia issue #2347).

## 5. Global acceptance gates
- **Back-compat:** every existing Principia test passes untouched (WS1/WS2 default
  to single-subsystem, no-cutoff; WS3 feature-flag off).
- **WS1:** `interstellar_precision_test` shows ~9 m → sub-mm at 4e16 m.
- **WS2:** `ephemeris_test` / `ksp_system_test` / `ksp_resonance_test` show
  **bounded, non-drifting** energy with the taper active; measured pair-count /
  cost reduction.
- **WS3:** a headless test of `PileUp::AdvanceTime` with an `OnRailsBurn` matches a
  reference flight-plan `Manœuvre` of the same thrust/Isp/duration (mass + Δv).

## 6. What is deliberately NOT in scope
- Galactic frame / galactic-scale coordinates (owner rejected; `Barycentric`
  stays the sole frame — WS1 uses only per-star local origins + DP offsets).
- Dynamic (runtime-recomputed) subsystem membership (start static).
- Frenet-locked on-rails thrust direction (MVP is inertially-fixed per frame).
- The US²-style integrator/UX borrow (separate note,
  `../universe-sandbox-nbody-comparison.md`).

## 7. References
- `research/R1-fp-precision.md` — WS1 full spec.
- `research/R2-soi-code-map.md` — WS2 code map.
- `research/R3-soi-numerics.md` — WS2 numerics/correctness (the taper argument).
- `research/R4-thrust-under-warp.md` — WS3 full spec.
- `design-draft.md` — the earlier architecture narrative (superseded on the SOI
  question by R3; WS1 matches).
- `schultz-dev0/principia-docs/interstellar-audit.md`, `theoretical_implementation.md`
  — original audit (note: WS1 drops the galactic level the audit proposed).
