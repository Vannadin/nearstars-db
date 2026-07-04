---
title: R7 — Warp/FTL support under Principia — current-code re-grounding, failure catalog, approach decision
status: research complete (2026-07-04)
grounds: WS4 (ws4-warp-support-backlog.md)
---

# R7 — Warp/FTL support: feasibility, approach, and the exhaustive failure catalog

## 0. What this document is — and what it deliberately does NOT re-derive

NearStars **already has a mature warp corpus** (written 2026-06-30, before WS1/WS2/WS3
landed on the interstellar fork). This R7 does **not** duplicate it — read those first:

- `gameplay/interstellar-expansion/warp/warp-and-navigation-brainstorm.md` — the `[src]`
  source analysis + the **options ladder** (no-fork / minimal-fork / big-fork C ABI) + cruise
  architecture + arrival-velocity frame discussion.
- `gameplay/interstellar-expansion/warp/warp-patch-draft.md` — the **chosen minimal-fork
  patch** (one `UnmanageabilityReasons` OR-term) + cruise-plugin skeleton.
- `gameplay/interstellar-expansion/warp/warp-drive-energetics.md` — the ADS-cited Alcubierre
  physics (why a warp is a **state discontinuity**, not an integrable force). `warp_exotic_matter.py`
  = the gameplay fuel model.
- `plugins/NearStarsWarp/` — draft C# (`WarpCruise`, `WarpDriveModule`, `PrincipiaInterop`,
  `WarpFlagBridge`) with `VERIFY`/`REQUIRES FORK` markers.
- `plans/principia-interstellar-branch/ws4-warp-support-backlog.md` — the owner-approved
  backlog stub; it sketched a big-fork `VesselWarpTo` C ABI as the "expected shape (to be
  confirmed by a research pass)" — **this is that research pass.**

**R7's unique contribution** (what the 2026-06-30 corpus could not have): a re-grounding
against the **current** fork code — which now carries subsystems (WS1), the checkpointer/
reanimator + rebase lifecycle (R5), the force-free void (WS2/WS2b), and the WS3 journalled-API
recipe — plus the exhaustive failure catalog and the resolved approach decision. Method: five
parallel source-mapping passes over the live code (DiscreteTrajectory, prediction/flight-plan,
checkpointer/rebase, WS3 API recipe, warp-mod prior art). Line anchors are from the fork at
head `e6a0225cd`; **reconfirm before coding** (Principia rebases monthly).

---

## 1. Feasibility verdict

**Feasible, and materially simpler than WS3** — via the minimal-fork path the KB already
chose. The big-fork `VesselWarpTo` C ABI is *also* feasible but hits a large, fragile surface
(§3.A–B) that the minimal-fork path sidesteps almost entirely. The physics settles the
framing: an Alcubierre warp produces **no proper acceleration and no local momentum change**
(the crew is in free fall inside the bubble), so a warp has **no honest continuous trajectory
representation** — it is a discontinuity in the vessel's degrees of freedom. Every design
below is therefore some form of "terminate the old trajectory, re-seed a new one"; they differ
only in *where* the discontinuity is expressed and *how much machinery* must tolerate it.

---

## 2. The two strategies (reconciling the plan's stub with the KB corpus)

The WS4 stub (plan dir) and the warp corpus (gameplay dir) point at **different**
implementation strategies. This is a genuine fork in the plan that the owner must ratify;
R7 recommends the minimal-fork.

| | **Minimal-fork (KB choice)** | **Big-fork `VesselWarpTo` (stub sketch)** |
|---|---|---|
| Mechanism | Add ONE OR-term to `UnmanageabilityReasons(Vessel)` in `ksp_plugin_adapter.cs`. While the warp flag is up, Principia stops managing the vessel; a NearStars cruise layer moves it with stock KSP calls. On dropout, clear flag → Principia re-seeds a fresh trajectory from the new stock orbit via `CreateTrajectoryIfNeeded` (guarded by `trajectory_.empty()`, `vessel.cpp` ~232–256). | New journalled plugin API (WS3 recipe): terminate the history, append a discontinuity-marked point / open a fresh segment at the destination DoF, trigger subsystem rebase, refresh prediction. |
| Trajectory discontinuity | **None to represent** — the C++ `Vessel` + its `DiscreteTrajectory` are destroyed on detach and rebuilt fresh. | In-place: hits the full DiscreteTrajectory + reanimation minefield (§3.A–B). |
| Fork surface | **1 line, in the adapter** (which NearStars already forks). Lives in a stable filter → light monthly rebase. | journal.proto + generated ×5 + plugin.cpp + interface + trajectory-reseed + reanimation checkpoint forcing + rendering break. Integrator-adjacent. |
| Flight plan on warp | Lost, replan at destination (accepted). | Could in principle survive, but §3.C shows it must be reset on a velocity-changing jump anyway. |
| Works during Principia-managed timewarp | No — warp happens while unmanaged (its own cruise clock). | Yes — but a warp *is* instantaneous, so this buys little. |
| History honesty | A **gap** (Principia has no trajectory for the cruise interval). | A discontinuity-marked continuous-ish record. |
| Save/load | Trajectory is destroyed/recreated → nothing exotic to serialize; GUID/parts/crew survive. | The re-seed changes the serialized trajectory → persists, but a mid-history discontinuity risks the load-time `ConsistencyStatus` CHECK (§3.F). |
| Verdict | **RECOMMENDED.** | Only if a future feature needs in-sim warp-maneuver planning; defer. |

The failure catalog (§3) is the argument: the big-fork path's extra capability costs a large
fragile surface, and the one honest thing it offers (a recorded discontinuity) has no physical
meaning a warp could respect anyway.

---

## 3. Failure-mode catalog (the core deliverable)

Tagged **[big]** = big-fork only, **[both]** = affects either strategy, **[min]** =
minimal-fork specific. Ordered roughly by severity.

### A. DiscreteTrajectory cannot hold a discontinuity at a segment seam **[big]**
- A jump can exist **only inside a single segment**, between two consecutive points — never at
  a segment boundary. `ConsistencyStatus` requires last-point-of-seg-N == first-point-of-seg-N+1
  in both time AND degrees of freedom (`discrete_trajectory_body.hpp:862-904`), and every mutator
  ends in `CHECK_OK(ConsistencyStatus())` (`:181,199,240,265,308,460`) → immediate abort.
  `AttachSegments` hard-`CHECK_EQ`s matching DoF (`:211`). `NewSegment` *forcibly duplicates* the
  previous last point (`:172-174`), so you cannot even manufacture a clean seam.
- An **intra-segment** jump → the Hermite cubic between the two points is built from both
  endpoints' position+velocity (`discrete_trajectory_segment_body.hpp:137-169,646-659`); a large
  Δposition or mismatched velocity makes the interpolant overshoot wildly. Endpoints are exact,
  the interior is garbage — and every consumer that samples intermediate instants (rendering,
  flight-plan seeding, prognostication) reads the garbage.
- Downsampling error accumulation is corrupted around the jump (`:443-475`): the jump term
  dominates `downsampling_error_`, and the baseline is only reset on the retained-point branch
  (`:470`), so nearby legitimate points may be wrongly dropped/kept.
- zfp lossy compression reconstructs non-endpoint, non-`exact` points only to `tolerance`
  (`:725-796`); a km-scale jump among metre-scale points smears neighbors.
- **The whole of A vanishes under minimal-fork** — a destroyed+recreated trajectory has no jump
  to represent.

### B. Reanimation *erases* a discontinuous past **[big]**
- Reanimation **re-integrates** each past segment with the physics integrator and stitches it
  (`ephemeris_body.hpp:1268-1314`; vessel: `FlowWithFixedStep`, `vessel.cpp:1304`). A position
  jump is not reproducible by integration → the reconstructed past is a smooth physical
  trajectory that **contradicts** the saved post-warp points. The discontinuity disappears
  unless a checkpoint is forced **exactly at** the warp instant so the jump lands on a
  checkpoint boundary.
- Stitching then asserts `CHECK_EQ(t_initial, reanimated.back().time)` (`vessel.cpp:1283`) and
  warns/gaps on mismatch (`ephemeris_body.hpp:1302-1305`); `Merge` `LOG(FATAL)`s on overlapping
  ranges (`discrete_trajectory_segment_body.hpp:551-556`). A warp straddling a checkpoint
  interval is a latent crash.
- **Minimal-fork avoids this** — the pre-warp `Vessel` is gone; there is no discontinuous past
  to reanimate.

### C. Prediction, flight plan, and maneuvers **[both, but cheap under minimal-fork]**
- Prediction is anchored to `psychohistory_->back()` (`vessel.cpp:664-669`); a stale prediction
  segment is **reused** if no fresh prognostication exists (`:461-465`). A warp must force-drop
  `prediction_`, stop the prognosticator (`StopPrognosticator`, `:691-693`), and re-predict —
  else an async result seeded from the old state attaches as garbage (`AttachPrognostication`
  only corrects for *subsystem*, not a physical jump, `:1457-1463`).
- The flight plan holds its own frozen `initial_degrees_of_freedom_` (`flight_plan.hpp:254`);
  `FlightPlan::Rebase` only *translates position, keeps velocity* (`flight_plan.cpp:462-464`),
  so a velocity-changing warp **cannot** be expressed by the existing rebase — the plan must be
  reset. A warp landing inside a planned burn window is explicitly rejected
  (`UnavailableError`, `vessel.cpp:618-621`).
- Maneuver thrust/Frenet frames derive from captured initial state (`manœuvre_body.hpp:231-234`),
  refreshed only by a full `ComputeSegments` recompute — a rebase without a valid new anchor
  gives a silently-wrong Δv direction (no crash).
- A running `FlightPlanOptimizationDriver` holds a copy of the pre-warp plan
  (`flight_plan_optimizer.hpp:223`); must be interrupted exactly as `RebaseIfNeeded` does
  (`vessel.cpp:196-198`).
- **Under minimal-fork all of this is free**: the flight plan/prediction die with the destroyed
  Vessel and are rebuilt at the destination. This is the accepted "flight-plan loss on warp."

### D. Subsystem assignment on re-seed — WS1 intersection **[RESOLVED: auto-correct under minimal-fork; big-fork must handle it]**
- A warp destination is in a *different* subsystem (another star), so the re-seeded vessel must
  be tagged with the destination subsystem and have its trajectory expressed relative to that
  subsystem's local origin — else it lands at light-year scale against the wrong origin, the
  FP-precision catastrophe WS1 exists to prevent (`ToRemoteSystem` is 4e16 m in the tests).
- **The lifecycle resolves this for the minimal-fork automatically (see §9.1).** An unmanaged
  vessel is *destroyed*, not persisted: the adapter skips `InsertOrKeepVessel` for it
  (`ksp_plugin_adapter.cs:1314-1321`), so it is dropped from `kept_vessels_` and
  `FreeVesselsAndPartsAndCollectPileUps` does `vessels_.erase(it)` (`plugin.cpp:626`). On
  re-adopt a **brand-new** `Vessel` is constructed with
  `subsystem_ = ephemeris->subsystem_of_body(parent->body())` (`vessel.cpp:93`) — and the parent
  is `vessel.mainBody`, which the cruise layer has set to the destination star. So the fresh
  vessel gets the destination subsystem *for free*, and the parts' DoF are converted into that
  (correct) origin by `InsertUnloadedPart` (`plugin.cpp:446-455`). **No re-seed subsystem fork
  is needed.** (My earlier "needs a subsystem fork" was based on a persist-and-reseed model that
  does not occur — the vessel is destroyed.)
- **Big-fork (in-place re-seed) DOES need it:** the persisted `Vessel` keeps its old
  `subsystem_` (`set_parent` does not change it, `vessel.cpp:206-210`), and `RebaseIfNeeded`
  refuses to fire on a close arrival (`nearest_distance <= 1e15 m` early-return,
  `vessel.cpp:167-169`). The reusable primitive is the body of `RebaseIfNeeded`
  (`vessel.cpp:172-190`: `subsystem_conversion` → `trajectory_.Translate` → `subsystem_ = target`
  → `ForAllParts(set_subsystem)` → `PileUp::Rebase`); factor it into a
  `Rebase(int target_subsystem)` that bypasses the distance gate, and set the subsystem *before*
  the DoF are written (so `subsystem_conversion` collapsing `DoublePrecision` to a single
  `Displacement`, `ephemeris_body.hpp:312-316`, is only used to move *between* origins, never as
  a substitute for anchoring in the right subsystem).

### E. Concurrency / background threads **[both]**
- The rebase translation was deliberately moved under `lock_` because the reanimator reads
  `trajectory_.front()` under it (`vessel.cpp:177-182`, commit `aa557ec4e`). A warp mutating
  `trajectory_`/`subsystem_` off-lock, or while pile-ups are being advanced (invariant at
  `plugin.cpp:845-846`), races the reanimator/prognosticator.
- `PileUp::Rebase` documents "must not be called while the pile-up is being advanced"
  (`pile_up.hpp:139`) — same constraint for any re-seed. Safe invocation points:
  `CatchUpLaggingVessels` (`plugin.cpp:842-851`) and `CatchUpVessel` (`:888-890`).

### F. Save/load **[both, differs by strategy — see §9.3 for the subsystem-partition detail]**
- Minimal-fork: nothing exotic. During the cruise the vessel is purely stock-side (Principia
  destroyed it), so a mid-cruise save simply doesn't serialize it; on load KSP re-creates it and
  Principia adopts it fresh when the warp ends. The re-adopted vessel's `subsystem_` round-trips
  via the existing WS1 field (`vessel.cpp:746`, absent⇒0). GUID/parts/crew survive throughout.
- Big-fork: an intra-segment discontinuity survives a round trip only if re-appended
  consecutively; a seam representation crashes `ReadFromMessage`'s
  `CHECK_OK(ConsistencyStatus())` (`discrete_trajectory_body.hpp:736`). The pre-rebase
  accumulated-offset scheme already failed save/load once (commit `7a21103d3`) — a warp relying
  on any implicit/accumulated offset instead of a per-checkpoint subsystem tag won't round-trip.

### G. Rendering **[big]**
- `RenderBarycentricTrajectoryInPlotting` appends every point with no gap detection
  (`renderer.cpp:104-125`) → a psychohistory→prediction chain spanning the jump draws a
  spurious straight line across the warp. Needs an explicit trajectory break at the warp
  instant. **Minimal-fork:** no rendered path spans the gap (old trajectory is gone).

### H. Warp-mod interop is adversarial by default **[both]**
- Principia's authoritative-state model **overwrites the KSP transform every frame**
  (`ksp_plugin_adapter.cs UpdateVessel` ~516-525); any external `SetPosition`/
  `Orbit.UpdateFromStateVectors` from a stock warp mod is read and its translation discarded
  the same frame. This is the documented reason HyperEdit/Blueshift "have no effect" (Principia
  issue #1420, wontfix) and why the FAQ lists Blueshift as incompatible ("these changes would
  be immediately undone by Principia... Principia would win").
- ⇒ We **cannot** simply install a stock warp mod. Either (min) detach the vessel at the
  authority layer so stock calls take effect for the cruise interval, or (big) do the move
  inside Principia's own model. Foreign warp mods (KSPIE = `Orbit.UpdateFromStateVectors`
  velocity injection; Blueshift = per-frame `Vessel.SetPosition`) would each need to call our
  hook; shipping our own minimal warp part (as `plugins/NearStarsWarp/` drafts) is cleaner than
  patching foreign mods.

### I. Velocity-frame / arrival relative velocity **[RESOLVED: velocity is frame-invariant across subsystems; preserving v0 is cruise-side, not a fork — see §9.2]**
- The KB chose **(a) barycentric preserve**: keep the vessel's Sol-barycentric inertial velocity
  v0 through the warp, so it arrives carrying the true interstellar relative velocity
  `v_rel = v0 − v_deststar` (a *hyperbolic* arrival the braking leg bleeds off — deliberate
  realism, the navigation planner already computes it).
- **Key fact (confirmed):** subsystem local origins differ by a **constant** displacement (zero
  relative velocity: `subsystem_origin_offset_` is a time-independent `Displacement`,
  `ephemeris_body.hpp:194,325`; jerk kernel comment "The velocities are unaffected: the origin
  offsets are constant", `:1524`). So a velocity vector is **identical in every subsystem's
  frame** — a subsystem change is a pure position rebase (`SubsystemConversionMotion` is a
  RigidMotion with identity rotation and unmoving frame velocity, `plugin.cpp:1911-1921`).
- **Consequence per strategy (see §9.2):** a *direct-DoF* re-seed (big-fork) preserves v0
  automatically. The *stock-orbit* re-seed (minimal-fork) sets barycentric velocity to
  `v_deststar + v_orbit` (`plugin.cpp:446-447`), so a naive bound stock orbit would place the
  vessel in a **parking orbit co-moving with the destination star — silently handing the player
  the entire interstellar Δv (tens of km/s) for free.** The fix is **cruise-side, no fork**:
  write the drop-out stock orbit with relative velocity `v_orbit = v0 − v_deststar`, giving
  barycentric `v_deststar + (v0 − v_deststar) = v0` — the realistic hyperbolic arrival. The
  cruise layer already captured v0 and can query `v_deststar`.
- World→Barycentric of a velocity needs the full `RigidMotion` (the ω×r term), not the
  rotation-only `OrthogonalMap` (`renderer.cpp:344-347` vs the hand-assembled motion at
  `plugin.cpp:481-496,762-816`) — relevant only if the warp reads velocities from the game frame.

---

## 4. Recommended implementation plan (minimal-fork)

**The deep dives (§9) confirm the minimal-fork is genuinely ~one adapter line** — subsystem
assignment is automatic (fresh construction from the destination parent) and velocity
preservation is cruise-side (choose the drop-out stock orbit's relative velocity). Follows
`warp-patch-draft.md` §1–5, with these **current-code deltas** from R7:

1. **The one fork:** add one OR-term to `UnmanageabilityReasons` in the fork's
   `ksp_plugin_adapter.cs` (draft's ~620–660 is 2026-06 master; the fork diverged — reconfirm
   line), keyed off a stock-field warp flag (read a `KSPField`/GUID-map by name to avoid a
   Principia↔NearStars compile dependency). Unmanaged ⇒ the vessel is destroyed (§9.1); on
   dropout it is re-adopted fresh from the destination-star stock orbit.
2. **Subsystem: nothing to do (§9.1).** The re-adopted vessel is constructed with
   `subsystem_ = subsystem_of_body(mainBody = destination star)` (`vessel.cpp:93`) → correct
   automatically. No re-seed subsystem fork. (Earlier "§3.D needs a fork" is retracted; it
   applies only to the big-fork in-place path.)
3. **Velocity: cruise-side (§9.2).** The drop-out stock orbit must carry relative velocity
   `v_orbit = v0 − v_deststar` so the barycentric seed is v0 (realistic hyperbolic arrival),
   NOT a bound parking orbit (which would gift the interstellar Δv). Pure C# in `WarpCruise`;
   no fork. Confirm v0 capture frame == the barycentric frame Principia seeds into.
4. **WS2 makes warp entry/exit clean** — a vessel detaching/re-seeding mid-void sees exactly
   zero background force (WS2/WS2b: force-free to machine precision), so no tail forces to
   reconcile. Positive intersection: warp is numerically cleanest exactly where it happens.
5. **Destination must be a partitioned celestial (§9.3)** — always true for the roster (every
   star is a celestial partitioned at initial ephemeris construction). No new subsystem may be
   created at runtime; a warp target that is not an existing subsystem would hard-CHECK-fail.
6. Cruise layer (`plugins/NearStarsWarp/`) is NearStars-side (Schultz's lane): `WarpCruise`
   state machine, ExoticMatter fuel, `WarpFlagBridge`. Verify the patch-draft §5 checklist
   (detach drops from kept-set; dropout re-adopts in the right subsystem/velocity; no part/crew
   loss; save/load across detach→cruise→re-adopt).

If the owner instead wants the **big-fork** path, the WS3 recipe applies verbatim (journal.proto
extension + generator run + plugin.cpp method + interface_vessel.cpp marshalling), plus: an
explicit `Rebase(target_subsystem)` primitive factored from `RebaseIfNeeded` (§3.D), a forced
checkpoint at the warp instant (§3.B), relaxing the one segment seam's `ConsistencyStatus`/
`AttachSegments` CHECK (§3.A), and breaking the rendered path (§3.G). Velocity is preserved
*automatically* here (§9.2). Estimated 3–5× the minimal-fork effort — and it buys only in-sim
managed-timewarp warp + a recorded discontinuity, neither of which a mod feature needs.

---

## 5. Stability plan

- **Golden test (either strategy):** warp a vessel Sol→remote-system, then a 10-year coast, and
  assert the arrival orbit around the destination star is stable and represented in the correct
  subsystem (extends the WS1 `FarFieldDampedCoast`/rebase e2e tests).
- **Reanimation test (big-fork only):** save immediately after a warp, force reanimation past
  the warp instant, assert no `ConsistencyStatus`/`Merge` crash and that the warp instant sits
  on a checkpoint boundary.
- **Concurrency:** exercise a warp while the reanimator/prognosticator is active (the §3.E race);
  assert the lock discipline holds.
- **Interop regression:** confirm a vessel NOT under the warp flag is still fully managed (the
  OR-term must be exactly scoped).
- **Save/load:** round-trip a mid-cruise save (minimal-fork: vessel is unmanaged — confirm it
  re-adopts correctly on load) and a just-warped save.

## 6. Optimization

- A warp is **instantaneous** — no per-step cost, so there is no hot path to optimize. The only
  cost is the one-time re-seed + (big-fork) a forced checkpoint + prediction refresh.
- The relevant efficiency concern is **not** re-triggering full reanimation on every warp: a
  forced checkpoint at the warp instant (big-fork) bounds reanimation to post-warp segments.
  Minimal-fork has none of this — the fresh Vessel starts with an animate-at-birth checkpointer
  (`ephemeris.hpp:698` rationale).

---

## 7. Open questions / owner decisions

1. **Minimal-fork vs big-fork** — R7 recommends **minimal-fork** (the §3 catalog is the
   argument, and §9 shows it is genuinely ~one adapter line). Owner to ratify; this reconciles
   the plan stub (which sketched big-fork) with the KB corpus (which chose minimal-fork).
2. ~~Subsystem assignment on re-seed~~ — **RESOLVED (§9.1)**: automatic under minimal-fork (fresh
   construction from the destination-star parent); a big-fork concern only.
3. ~~Arrival velocity frame~~ — **RESOLVED (§9.2)**: velocity is frame-invariant across
   subsystems; barycentric-preserve is cruise-side (choose the drop-out orbit's relative
   velocity), no fork.
4. **Arrival difficulty as an option (new — owner's idea 2026-07-04):** because v0 preservation
   is entirely the cruise layer's choice of drop-out stock-orbit velocity (§9.2), the arrival
   regime is a **free difficulty toggle** with zero extra code:
   - *Realistic / hard:* `v_orbit = v0 − v_deststar` → hyperbolic arrival, player must brake off
     the true interstellar closing velocity (tens of km/s).
   - *Casual / easy:* a bound parking orbit → vessel arrives co-moving with the destination star
     (the interstellar Δv is waived). This is the "naive" behavior — but as a *chosen* option,
     not a bug. Exposed as a difficulty/game-setting or a per-drive tunable in `WarpCruise`.
5. **Do we ship our own warp part or patch foreign mods (§3.H)?** KB leans ship-our-own
   (`plugins/NearStarsWarp/`); foreign-mod interop is per-mod work.

## 8. Correction to the WS4 stub — issue #2347

The WS4 backlog stub and the brainstorm call warp "the same incompatibility as PersistentThrust
(Principia issue #2347)." **Issue #2347 is actually "Burn in time warp with RO ion engines"** —
a persistent low-thrust-under-timewarp feature request, still **open**, not a teleport issue.
The maintainers' anti-warp position lives in the **FAQ**, not the tracker: "Any mod that tries
to move vessels or otherwise change orbits either (1) without using engines or (2) during time
warp, is incompatible with Principia," which names **Blueshift explicitly**. No dedicated
Alcubierre/warp/teleport issue exists in Principia's tracker (searched: only #2347, #2185 warp-
*to-node*, #4223 surface-teleport bug). The root-cause characterization ("can't move without
engines / during timewarp") is directionally right; the issue number/title is not. → fix the
stub's citation.

## 9. Deep-dive addendum (2026-07-04) — the three findings that simplify the minimal-fork

Three follow-up source passes (subsystem assignment, velocity frame, serialization) plus a
direct read of the unmanaged-vessel lifecycle. Together they show the minimal-fork needs **no
C++ re-seed fork** — only the one adapter line.

### 9.1 Unmanaged ⇒ destroyed ⇒ fresh construction ⇒ correct subsystem (the load-bearing lifecycle)
- The adapter skips `InsertOrKeepVessel` for an unmanageable vessel: `if
  (unmanageability_reasons != null) { … continue; }` (`ksp_plugin_adapter.cs:1314-1321`). A
  vessel is added to `kept_vessels_` only *inside* `InsertOrKeepVessel` (`plugin.cpp:425`), so an
  unmanaged vessel is not kept.
- `FreeVesselsAndPartsAndCollectPileUps` then **destroys** it: kept vessels take the
  `CreateTrajectoryIfNeeded` branch (`plugin.cpp:617-619`); non-kept vessels hit
  `vessels_.erase(it)` (`plugin.cpp:626`) — the owning `unique_ptr<Vessel>` (trajectory, flight
  plan, subsystem) is freed. KSP GUID/parts/crew survive stock-side.
- On re-adopt the GUID reappears, `InsertOrKeepVessel` runs with `inserted=true`, and a
  **brand-new** `Vessel` is constructed: `subsystem_(ephemeris->subsystem_of_body(parent->body()))`
  (`vessel.cpp:93`), where the parent is `main_body_index = vessel.mainBody`
  (`ksp_plugin_adapter.cs:1312,1323-1326`). The cruise layer set the drop-out stock orbit around
  the destination star, so `mainBody` = destination star ⇒ **destination subsystem, automatically.**
- Parts are then inserted with their DoF converted *into* the (now correct) vessel subsystem
  (`InsertUnloadedPart`, `plugin.cpp:446-455`), and `CreateTrajectoryIfNeeded` barycentres them
  (`vessel.cpp:267-285`). So the trajectory is anchored in the destination origin from birth — no
  `Translate`, no rebase, no fork. (Contrast: `set_parent` alone does *not* change `subsystem_`,
  `vessel.cpp:206-210` — which is why the *big-fork* in-place path, where the Vessel persists,
  must reassign it explicitly; see §3.D.)

**State inheritance across the destroy/recreate (NOT "perfect inheritance" — by design).** What
the re-adopted vessel keeps falls into three categories:
- *Survives (stock-side, never in the C++ Vessel):* parts, crew, resources (incl. the warp
  ExoticMatter — a stock resource, so cruise-time drain persists), GUID, name, stock orbit. The
  C++ `Part` objects are owned by the Vessel (`parts_`, `vessel.hpp:461`) and destroyed with it,
  but are faithfully **reconstructed** from the authoritative KSP parts on re-insertion (mass,
  resources, DoF re-read) — same result, not a copy.
- *Preserved by GUID (the "zombie" map):* `prediction_adaptive_step_parameters_` is stashed on
  destruction (`plugin.cpp:624`), restored by GUID on re-create (`plugin.cpp:401-407`), and even
  serialized (`plugin.cpp:1673`). It is the *only* Principia-side per-vessel setting carried
  across.
- *Lost by design (in the freed Vessel):* `trajectory_` (history gap over the cruise),
  `flight_plans_` + maneuvers (replan at destination — the accepted "flight-plan loss"), target
  designation (`ClearTargetVesselIf`, `plugin.cpp:623`); `subsystem_`/orbit-analyser/checkpointer
  are *reconstructed* correctly, not inherited. These losses are exactly the quantities a warp —
  a genuine trajectory discontinuity — cannot carry anyway, so the destroy/recreate discards
  precisely the right set.

### 9.2 Velocity is frame-invariant across subsystems; v0 preservation is cruise-side
- Subsystem local origins differ by a **constant** displacement — `subsystem_origin_offset_[s]`
  is set once at construction (`ephemeris_body.hpp:194`), stored as a time-independent
  `DoublePrecision<Displacement>` (`ephemeris.hpp:680`); inter-subsystem offsets likewise
  (`:325`). The jerk kernel states it: "The velocities are unaffected: the origin offsets are
  constant" (`ephemeris_body.hpp:1524`). So a velocity is identical in every subsystem's frame;
  a subsystem change moves position only (`RebaseIfNeeded` does `trajectory_.Translate(disp)`
  with velocity untouched, `vessel.cpp:172-181`; `SubsystemConversionMotion` = RigidMotion,
  identity rotation, unmoving frame velocity, `plugin.cpp:1911-1921`).
- **Direct-DoF re-seed (big-fork):** keep the Barycentric DoF velocity ⇒ v0 preserved for free.
- **Stock-orbit re-seed (minimal-fork):** `InsertUnloadedPart` sets barycentric DoF =
  `parent->current_degrees_of_freedom(t) + PlanetariumRotation⁻¹(from_parent)`
  (`plugin.cpp:444-447`), i.e. velocity = `v_deststar + v_orbit`. `CreateTrajectoryIfNeeded`
  just barycentres that (`vessel.cpp:267-285`), so the seed velocity is whatever the drop-out
  stock orbit specified. ⇒ To preserve v0, the cruise layer writes `v_orbit = v0 − v_deststar`
  (barycentric result = v0); to give an easy bound arrival, it writes a parking-orbit velocity.
  **Either way it is a cruise-side C# choice, not a fork.**
- Arrival relative velocity therefore = `v0 − v_deststar` (the real interstellar closing speed,
  what the braking leg bleeds off) in the realistic mode.

### 9.3 Subsystem partition is serialized (not recomputed); destination must be a partitioned subsystem
- The partition is written explicitly and restored verbatim: `Ephemeris` gains
  `repeated int32 body_subsystem = 14` and `repeated DoublePrecision subsystem_origin_offset = 15`
  (`serialization/physics.proto:196-200`), written only when `subsystem_origin_offset_.size() > 1`
  (`ephemeris_body.hpp:1017-1024`) and read back directly, overwriting the offsets
  (`:1065-1099`). `ClusterSubsystems` runs **only at initial construction**
  (`solar_system_body.hpp:173`), never in `ReadFromMessage` — so load reproduces the save-time
  partition exactly; **no re-clustering risk**, and the partition is fixed for the game (no new
  subsystem appears at runtime).
- Vessel/checkpoint/flight-plan subsystem tags: `Vessel.subsystem` (`ksp_plugin.proto`,
  written `if != 0` at `vessel.cpp:746`, read absent⇒0 at `:859`), `Checkpoint.subsystem = 4`,
  `FlightPlan.subsystem = 14`. Commit `7a21103d3` added these because the old in-memory
  `rebase_offset_` accumulator "…survives saving and loading, which the accumulated rebase offset
  did not" — reanimation now integrates each checkpoint in the subsystem it was written in and
  converts via `subsystem_conversion(checkpoint_subsystem, subsystem_)`.
- **Warp requirement:** the destination subsystem must already exist in the persisted partition,
  or `subsystem_conversion`/`inter_subsystem_offset`'s `CHECK_LT(subsystem, …size())`
  (`ephemeris_body.hpp:518,585,623`) hard-fails on load/reanimation. This is **automatically
  satisfied** for the NearStars roster: every star is a celestial partitioned at initial
  construction, and a warp target is always such a celestial. Minimal-fork adds **no new
  serialization** — the re-adopted vessel round-trips through the existing WS1 `subsystem` field.
- Backward compat: a pre-subsystem or stock save loads with the fields absent ⇒ single subsystem
  0, unchanged behavior (`has_...()` guards / absent⇒0 defaults).

## Related
- `ws4-warp-support-backlog.md` — the workstream stub this research grounds.
- `research/R4-thrust-under-warp.md` — WS3, whose journalled-API recipe the big-fork path reuses.
- `research/R5-vessel-frames.md` — the checkpointer/reanimator + rebase lifecycle rules (§3.B/D/E).
- `gameplay/interstellar-expansion/warp/*` — the physics + minimal-fork patch draft + plugins.
