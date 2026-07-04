---
title: R3 §5B — neighbor-list backbone/vessel optimization — implementation plan
status: PLAN (owner chose variant B + plan-first, 2026-07-04) — not yet implemented
grounds: R3 §5 (soi-numerics), builds on WS2/WS2b (the taper is done; this adds the structure)
target base: fork head 280cf4d9b, gate 183
---

# R3 §5B — neighbor lists for the far-field-damped N-body kernels

## 0. What this is (and what is already done)

WS2/WS2b already **taper** gravity: each pair is visited and multiplied by the C² quintic σ,
becoming exactly zero beyond its cutoff. That is the *potential* fix (reversible, no-drift).
**This plan adds the missing *structural* optimization**: stop *visiting* pairs that are damped
to zero, so the loop cost drops from O(N²) to ~O(N·k). Measured motivation: the WS2b benchmark
`BM_EphemerisMultiSubsystemAsteroids` showed a 2.1× backbone speedup from the taper alone, capped
by the residual ~25%-per-pair cost of visiting-then-skipping every dead pair. This plan removes
that residual.

Owner decisions recorded: **variant B (neighbor lists), not variant A (raw block-diagonal)** —
because block-diagonal alone is a correctness landmine (below); and **plan-first** (implement in a
fresh, budget-rich session because the backbone is the most drift-sensitive kernel and the
acceptance gate is a century-scale energy test).

## 1. The two correctness landmines this plan must respect

### 1a. Block-diagonal is NOT valid on its own
Skipping whole cross-subsystem blocks assumes inter-subsystem separation > max(r_c) of the cross
pairs. But `subsystem_clustering_threshold = 1e14 m` (`ksp_plugin/plugin.cpp:95`) while a
solar-mass star's r_c = √(μ/floor) ≈ **1.14e16 m** (114× larger). So two subsystems clustered as
distinct at, say, 5e14 m apart still have live cross-forces (5e14 < 1.14e16), and a naive
block-diagonal would wrongly drop them. Real rosters put stars light-years apart (4e16 m > r_c),
but the partition does **not guarantee** it. ⇒ Use a **coarse per-subsystem-pair check** ("is
this block pair entirely beyond max(r_c)?"), never an unconditional block skip.

### 1b. Reversibility forbids a stateful (skinned, reused) Verlet list on the backbone
QT12's no-drift comes from **time-reversibility**: the force must be a pure function of the current
positions, f = f(q) (R3 §0.1). A classic Verlet list is built once and **reused for K steps** (to
amortize the rebuild); during those steps the force depends on the *build-time* positions, i.e. on
history, not on current q → reversibility broken → **secular energy drift** — the exact pathology
QT12 exists to prevent. R3's own "(iii) skin + hysteresis" (R3 §2) is an MD idiom for
*non-reversible* integrators and **must not be applied to the reversible backbone.** ⇒ On the
backbone the neighbor structure must be **stateless: rebuilt every force evaluation from the
positions the force uses**, so f stays exactly f(q). (A skinned/reused list is acceptable only on
the *massless/vessel* path — see §5 — which is adaptive and makes no no-drift claim, R3 §3.)

## 2. Design — a two-level, stateless-per-step structure

Per backbone force evaluation (`ComputeGravitationalAccelerationBetweenAllMassiveBodies`, the RHS
called once per QT12 step with the current `positions`):

**Level 1 — subsystem blocks (handles the interstellar void, cheaply):**
- Precompute per subsystem a bounding sphere (centre + radius) of its bodies, and each subsystem's
  max r_c. For a subsystem pair (s1, s2), the block is entirely damped iff
  `dist(centre_s1, centre_s2) − radius_s1 − radius_s2 ≥ maxpair_r_c(s1,s2)` (using the constant
  inter-subsystem offset). If so, **skip the whole block** (all s1×s2 pairs contribute zero) —
  the safe substitute for block-diagonal (§1a). Few subsystems ⇒ negligible cost. Recompute the
  bounding data each evaluation (stateless) or when positions move materially (still a pure
  function of q if recomputed each eval; prefer per-eval for reversibility, it is O(N)).

**Level 2 — within a subsystem (handles the asteroid belt):**
- Split the subsystem's bodies into **large-r_c** (stars, planets — few; their r_c spans the whole
  subsystem) and **small-r_c** (asteroids — many).
- **large × everything**: full loop (few large bodies ⇒ O(N_large · N), cheap). They reach
  everything in the subsystem anyway, so no list helps.
- **small × small**: bucket the small bodies into a **uniform cell grid** sized to the small-body
  cutoff (≈ r_c of the small class) over the subsystem's bounding box, **rebuilt every evaluation**
  (O(N), a pure function of q ⇒ reversible). Each small body visits only its own + adjacent cells
  ⇒ O(N·k). Pairs beyond the cutoff are never visited. This is where the 200-asteroid N² dies.
- The grid is single-scale *within the small class* (asteroids share ~one r_c), so the
  multi-scale problem (star r_c 1e16 vs asteroid r_c 3e10) is handled by the large/small split,
  not by one grid spanning six orders of magnitude.

## 3. Invariants to preserve (regression, not optional)

- **Bit-identical disabled path**: floor = 0 (or single subsystem, no belt) must produce the exact
  same result as today — the whole structure is entered only when damping is active AND there is a
  worthwhile body count. Guard with the existing `has_far_field_damping` template split + a
  runtime body-count threshold; below it, keep the current O(N²) loop verbatim.
- **Momentum exactness**: every visited pair still applies ONE σ symmetrically to both bodies
  (Newton-3), exactly as WS2b (`ephemeris_body.hpp` massive kernel). A pair not visited contributes
  exactly zero to BOTH bodies — momentum stays exact.
- **Subsystem offsets**: cross-subsystem visited pairs still use `inter_subsystem_offset`; the
  block check uses the same constant offsets.
- **Oblateness**: geopotential harmonics self-damp far below r_c, so a body pair skipped by the
  grid (beyond r_c) also has negligible harmonics — safe. But large bodies (oblate stars/planets)
  are in the full-loop tier, so their harmonics are always computed. Never put an oblate body in
  the gridded small tier.
- **Reversibility**: the structure is a pure function of the current `positions` every evaluation
  (no cross-step state). This is the load-bearing property (§1b).

## 4. Backbone implementation steps (ordered, each with a verify)

1. **Bounding + r_c metadata** (`Ephemeris`): per-subsystem bounding sphere + max r_c, and the
   large/small body partition (by r_c threshold, e.g. r_c < subsystem-diameter). Verify: unit test
   of the metadata on a synthetic roster.
2. **Level-1 block check** in `ComputeGravitationalAccelerationBetweenAllMassiveBodies`: before the
   pair loops, skip fully-damped subsystem-pair blocks. Verify: bit-identical to today on all
   gate rosters (blocks that aren't fully damped are NOT skipped); the 3-subsystem test still
   passes; a new test that a genuinely-live near-subsystem block is NOT skipped.
3. **Level-2 cell grid** for small×small within a subsystem. Verify: the damped result equals the
   current per-pair-skip result to bit-exactness (same pairs visited, same σ) on the
   200-asteroid roster.
4. **Benchmark**: extend `BM_EphemerisMultiSubsystemAsteroids` (or add a sparser-belt variant) to
   confirm the speedup exceeds the 2.1× taper-only figure; report best-of-3.
5. **Acceptance gate (the hard one, §6)**: century bounded-energy non-drift.

## 5. Vessel / massless path (R3 §5A — optional second target)

The massless kernel `ComputeGravitationalAccelerationByAllMassiveBodiesOnMasslessBodies`
(`ephemeris_body.hpp`) loops ALL massive bodies per massless body, skipping per-pair beyond
outer². In a belt world this is the bigger real cost (per vessel, per substep). Here a
**skinned, reused per-vessel neighbor list IS acceptable** (this path is adaptive and makes no
no-drift claim — R3 §3), rebuilt every few substeps, skin δ ≈ 0.05–0.1·r_c + hysteresis to kill
chatter. Site r₀ where a_cut/a_dominant = 1e-6 (R3 §5A). This is separable from the backbone work
and can be a follow-up. **Owner to confirm target priority** (backbone-first is recommended: it is
self-contained and the benchmark already quantifies its win; the vessel path is more entangled
with prediction/flight-plan/rebasing).

## 6. Acceptance gate (mandatory — R3 §5C)

- **Bit-identical disabled path**: full 183-test gate byte-identical with floor = 0.
- **Bounded-energy non-drift** (the load-bearing gate): a multi-century QT12 run of a bound system
  WITH the neighbor structure active must show energy that is **bounded and oscillatory** (the
  QT12 signature), not a random walk — matching the SAME run without the structure to ~1e-12
  relative. Extend `astronomy/ksp_system_test` / `ksp_resonance_test` or add an interstellar
  century-energy test. **If energy drifts, the structure broke reversibility → revert.**
- **Momentum exactness**: total momentum conserved to round-off over the run.
- **Benchmark**: measured speedup > 2.1× on the belt roster; disabled path within noise.

## 7. Risks & fallbacks

- **Reversibility regression** (highest risk): mitigated by stateless-per-step (§1b) + the
  century-energy gate. If per-eval rebuild is too costly, do NOT switch to a reused list on the
  backbone — instead narrow the scope (grid only the small tier) or fall back to today's per-pair
  skip (R3's "if in doubt skip B").
- **Cell-grid dynamic range**: mitigated by the large/small split (§2) — the grid only spans the
  small class.
- **Marginal real value**: if profiling on a real roster shows the backbone is not the in-game
  bottleneck (vs the vessel path), do §5 first or instead. Confirm the bottleneck before building.
- **Complexity vs payoff**: this is a large change to the most critical kernel. If the belt sizes
  in the actual NearStars/RSS-Origin roster are modest, the 2.1× taper-only figure may already
  suffice — re-confirm the roster's asteroid count before committing.

## 8. Effort

Backbone (§4): ~1 budget-rich session (metadata + block check + cell grid + the century gate is
the long pole). Vessel (§5): a separate comparable session. Recommend backbone-first, gated, then
reassess whether the vessel path is worth it.

## Related
- `research/R3-soi-numerics.md` — §5 recommendation this implements; §0.1 reversibility (§1b here).
- WS2b commit `e6a0225cd` — the taper this builds on (massive kernel).
- `.nearstars/interstellar-test-sweep.md` — the 2.1× measurement + `BM_EphemerisMultiSubsystemAsteroids`.
