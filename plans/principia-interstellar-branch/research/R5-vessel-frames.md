# R5 — Vessel coordinate representation (WS1 commit 4, promoted to a design)

Author: fable (after implementing WS1 commits 1-3). Source head: fork branch
`nearstars-interstellar` @ 6c21c5563 (= master 440310a9 + WS1). Status: IMPLEMENTED
through 4d + hardening (see §7 post-implementation addendum, 2026-07-03); §6 B
(commit 4e) is under re-decision — see §8.

## 0. Problem (the gap R1 left open)

WS1 localized the **backbone**: massive-body positions are stored relative to per-subsystem
origins. Vessels are untouched: `Vessel` holds `DiscreteTrajectory<Barycentric>` with absolute
positions (`vessel.hpp:436`), so a vessel at a 4e16 m star still has ULP = 8 m — orbit/landing
precision at the destination is broken, which is the core gameplay scenario. Worse, the massless
kernels now MIX representations: `ComputeGravitationalAccelerationByMassiveBodyOnMasslessBodies`
evaluates body positions LOCAL (`trajectories_[b1]->EvaluatePositionLocked(t)`) but receives
vessel positions from the caller — wrong as soon as subsystems are active. R1 §4's "route only
rendering through the globalizing accessor" under-scopes all of this.

## 1. Architectural facts the design leans on (verified in code)

1. **Vessel state I/O at the plugin boundary is parent-relative, never absolute**:
   `VesselFromParent`/`CelestialFromParent` return `RelativeDegreesOfFreedom<AliceSun>`
   (`plugin.hpp:334,344`); unloaded parts enter as `from_parent` offsets (`:209-213`); loaded
   parts enter in `World`, anchored to `main_body` (`:222-233`); `InsertOrKeepVessel` carries the
   KSP reference-body index (`:199-204`). ⇒ If the parent's stored DoF is subsystem-local, the
   absolutized vessel DoF lands in the SAME subsystem-local representation automatically.
2. **The ephemeris is built in one place** — `Plugin::EndInitialization` (`plugin.cpp:184-230`)
   from the accumulated `gravity_model_`/`initial_state_` protos, with the full parent hierarchy
   at hand (`parents_` map). ⇒ the partition can be computed there and passed to the Ephemeris
   ctor (WS1's `subsystems` param); no per-insertion threading needed.
3. Reference frames / renderer read ephemeris trajectories directly
   (`plugin.cpp:263-269`, `physics/rigid_reference_frame*`), and are applied to vessel DoFs.
   ⇒ the only consumers that need care are those mixing objects from DIFFERENT subsystems.

## 2. Design principle

**Barycentric stays the sole semantic frame.** "Subsystem-local" is a *storage representation*:
every stored `Position<Barycentric>` (body or vessel) is implicitly tagged with a subsystem id;
mixing two representations requires reconstituting the inter-origin offset in DoublePrecision
(the WS1 kernel machinery, reused verbatim). A vessel carries ONE id; all its trajectories
(history, psychohistory, prediction, flight plan) share that representation.

## 3. Components

1. **Ephemeris (headless)** — public accessors `subsystem_of_body(body)` and
   `InterSubsystemOffset(s1, s2)` (DoublePrecision). Massless kernels get the WS1 split:
   `...OnMasslessBodies` (`ephemeris_body.hpp:1478+`), potential (`:1529+`), jerk-on-massless,
   and the single-position queries. API: `FlowWithAdaptiveStep` (both overloads) and
   `ComputeGravitationalAcceleration/PotentialOnMasslessBody` take `int subsystem = 0`;
   `NewInstance`/fixed-step takes `std::vector<int> subsystems = {}` parallel to its
   trajectories (it accepts several). Defaults ⇒ byte-identical legacy.
2. **Partition source (plugin)** — AS IMPLEMENTED (4b, simplification of the signed-off
   heuristic): the hierarchy is not needed at all — the clustering pass alone IS the rule.
   `ClusterSubsystems(positions, threshold)` (free function, `physics/ephemeris.hpp`) does
   single-linkage clustering with `R_subsystem` = 1e14 m; bodies chained within the threshold
   share a subsystem (bound binaries handled natively), and a single-cluster result returns the
   empty partition so that stock/RSS systems stay on the byte-identical legacy path.
   `SolarSystem::MakeEphemeris` takes an `optional<Length> subsystem_clustering_threshold` and
   computes the partition internally; `Plugin::EndInitialization` passes the constant and logs
   the resulting partition. No cfg/proto change. [§6 decision A]
3. **Vessel** — `subsystem_` int, set at insertion to the parent celestial's subsystem
   (`InsertOrKeepVessel` already has `parent_index`); PileUp inherits it from its vessels
   (co-located ⇒ equal). Invariant: all the vessel's trajectories are stored in that
   representation; the massless-flow calls pass it down.
4. **Cross-subsystem consumers (audit list, fix = globalize via the offset, collapsed to
   double — these paths need km-not-mm precision):** `VesselFromParent`/`CelestialFromParent`
   when the parent is in another subsystem (interstellar cruise: KSP parent = Sun);
   `RigidReferenceFrame`s whose centre body is in another subsystem than the vessel (map view
   across systems); targeting a vessel in another subsystem; apsides vessel↔body;
   `geometric_potential_plotter_`. Same-subsystem cases — the precision-critical ones — never
   touch the offset and stay exact.
5. **Rebase (the one new mechanism)** — trigger: vessel unloaded ∧ nearest subsystem anchor ≠
   current ∧ distance to both anchors > `R_void` (default 1e15 m). Action: translate ALL the
   vessel's trajectories by −(offset_new − offset_old) (DoublePrecision collapsed to double),
   set `subsystem_`. Correctness: at >1e15 m from every anchor the translation error is
   ≤ ULP(~2e16) ≈ 4 m where ambient gravity is ≲1e-10 m/s² — dynamically negligible, invisible
   at rendering scale; with WS2's taper the force there is exactly zero and the rebase is
   rigorously glitch-free. One-shot O(points), once per interstellar transfer. Predictions and
   flight plans are rebuilt routinely anyway.
6. **Serialization** — `optional int32 subsystem` on the Vessel (and PileUp) messages
   (`serialization/ksp_plugin.proto:164,114`); absent ⇒ 0 ⇒ legacy saves unchanged.

## 4. What deliberately does NOT change

The C interface QP structs and the C# adapter (parent-relative I/O hides everything);
stock-KSP/World handling; `Barycentric` as the type everywhere; WS1's backbone machinery.

## 5. Commit order (each headless-testable on the Mac up to 4c)

- **4a** Ephemeris accessors + massless split + params. Test: extend
  `interstellar_precision_test` with a massless probe orbiting the remote planet —
  probe-planet separation error, control (subsystem 0 representation at 4e16 m, meters)
  vs probe flowed with `subsystem = 1` (sub-mm). Same structure as the WS1 gate.
- **4b** Partition in `EndInitialization` + `MakeEphemeris` threading (+ `ksp_plugin_test`).
- **4c** `Vessel::subsystem_` + threading through vessel/pile-up flows + rebase + serialization
  (+ vessel_test / pile_up_test).
- **4d** Cross-subsystem consumer audit (§3.4) + fixes. KSP-facing; the part that genuinely
  needs an in-game smoke test on Windows later.
- **4e** Rebase-aware flight plans + predictions (§6 B): per-segment subsystem tags, coast-split
  at the void boundary, per-segment globalization in consumers. Headless-testable via
  `flight_plan_test` / a cross-system plan scenario in the precision test.

## 6. Owner decisions needed

- **A. Partition rule — DECIDED (owner, 2026-07-02): hierarchy+distance heuristic with the
  clustering pass** (§3.2). An explicit cfg override key remains a later escape hatch if a real
  pack structure defeats the heuristic. Constants `R_subsystem` = 1e14 m, `R_void` = 1e15 m.
- **B. Flight-plan precision across subsystems — DECIDED (owner, 2026-07-02): precise from the
  start.** Mechanism: per-segment subsystem tags. A coast segment that crosses the void boundary
  (same trigger rule as the vessel rebase) is split at the crossing; the next sub-segment
  continues in the destination representation. Prognostication/prediction get the same
  treatment (same `FlowWithAdaptiveStep` seam). Consumers of plan/prediction trajectories
  globalize per segment. This adds `flight_plan.cpp` (segment chain) and `vessel.cpp`
  (prognosticator) to the scope — tracked as commit 4e below.
  **[RE-DECIDED (owner, 2026-07-03): Option 1 of §8 — keep the whole-plan rebase, defer
  per-segment tags. Commit 4e is dropped from the MVP path; revisit only if in-game use
  shows a case where the origin-side 8 m display quantization matters. ACCEPTED TRADEOFF:
  after a vessel crosses to another subsystem, the DISPLAY accuracy of its own past
  trajectory (the history flown in the origin system, as plotted in map view) and of the
  origin-side segments of its flight plan degrades to the ~8 m ULP grid. Integration
  accuracy, other vessels, and the origin system's backbone are unaffected.]**

## 7. Post-implementation addendum (2026-07-03, after 4a–4d + review + hardening)

What held, and what this design under-modelled — recorded so that WS2/WS3 inherit the lesson.

- **Held:** the storage-representation principle (§2), the parent-relative boundary argument
  (§1.1), the partition-at-EndInitialization simplification (§3.2), back-compat via defaults
  (byte-identical legacy verified by the full upstream suite + a stock benchmark), and the
  rebase trigger geometry (§3.5's error analysis). A dedicated sign-convention audit found all
  ~40 conversion sites directionally correct.
- **Under-modelled: state lifecycle.** §3.5 called the rebase "one new mechanism … predictions
  and flight plans are rebuilt routinely anyway". In reality FIVE holders of *stale copies* of
  vessel state exist and none were notified by the rebase: the checkpointer (absent from this
  document entirely), the reanimator thread, the prognosticator thread, lazily-serialized
  flight plans, and optimization-driver copies. All 10 CONFIRMED findings of the 12-angle
  review (2026-07-03) were in these five paths; all are fixed by making every stored
  trajectory *self-describing* (per-checkpoint / per-plan / per-prognostication subsystem
  tags) instead of patching with a cumulative offset. **Rule for future mechanisms: for any
  mutation of vessel/plan state, enumerate the asynchronous and serialized holders of copies
  of that state before coding.**
- **§3.4 audit list was categorically right but numerically half-complete**: the real 4d audit
  found ~2× the sites (renderer World/sun anchoring, planetarium occlusion spheres, part
  loading via the main-body frame, navball, orbit-analyser internals, optimizer distances).
- §4's "the C interface hides everything" had exactly one leak
  (`FlightPlanGetManoeuvreInitialPlottedVelocity`), fixed.

## 8. 4e options (for the owner's re-decision of §6 B)

Context change since the 2026-07-02 decision: (a) whole-plan `FlightPlan::Rebase` — broken at
decision time, unknowingly — is now fixed and tested; (b) 4d threaded a ONE-REP-PER-TRAJECTORY
`int subsystem` through ~15 consumer signatures, which per-segment representation would
re-open.

**Residual error of Option 1 (keep whole-plan rebase, skip/defer 4e):**
- One-time seed translation error at rebase: ≤ 4 m (half-ULP of the collapsed 4×10¹⁶ m
  offset). Ambient gravity there ≤ ~1.3×10⁻¹⁰ m/s² (μ ≈ 1.3×10²⁰ m³/s² at 10¹⁵ m), so the
  dynamical effect of 4 m is ~10⁻²⁴ m/s² — nil; with WS2's taper the force there is exactly
  zero.
- After the rebase the whole plan is re-integrated in the destination rep, so segments still
  near the ORIGIN star sit at ~4×10¹⁶ m from the representation origin: their positions are on
  an 8 m ULP grid (pre-WS1 precision) — but those are *past* (already-flown or
  departure-adjacent) segments; the remaining/future segments near the destination are exact.
  A manœuvre still parameterized in the origin system keeps its exact time and Δv; only its
  displayed geometry quantizes at ~8 m.
- Net: no discontinuity, no drift; a one-time metre-scale step at the rebase event and 8 m
  display quantization for origin-side history. Invisible at render scale.

**Cost of Option 2 (per-segment tags, the original 4e):**
- FlightPlan: per-segment subsystem tags + coast split at the void boundary (trigger = §3.5
  rule) + serialization of the tags (proto change) + manœuvre bookkeeping across the split.
- Prognostication/prediction: same split treatment.
- Consumers: the ~15 signatures threaded in 4d assume one rep per trajectory
  (`Plugin::ComputeAndRender*`, `Renderer::Render*`, `Planetarium::PlotMethod4`, interface
  callers) — each must become per-segment-aware, or FlightPlan must expose a normalized
  single-rep view for consumption (which reintroduces the collapse it tries to avoid).
- A further lifecycle audit (per-§7 rule) for the new per-segment state.
- Estimated effort: comparable to 4c-1+4c-2 combined (~2–3 commits + review), vs ~0 for
  Option 1.

**What Option 2 buys over Option 1:** sub-mm (instead of 8 m) *display* precision for
origin-side plan segments after a mid-void rebase, and mm-exact cross-void plan geometry while
still un-rebased. It does NOT change integration accuracy of the flown trajectory (the vessel
itself always integrates in its own rep, exactly).

**Recommendation (fable):** Option 1 now (proceed to activation + end-to-end test); revisit
Option 2 only if in-game use shows a case where origin-side 8 m display quantization matters.

**DECIDED (owner, 2026-07-03): Option 1**, explicitly accepting the tradeoff that a rebased
vessel's past-trajectory display (its origin-system history in map view) and the origin-side
portion of its flight plan are quantized at ~8 m after the crossing.
