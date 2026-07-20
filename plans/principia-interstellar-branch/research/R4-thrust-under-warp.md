# R4 — Continuous thrust under timewarp

Research agent: opus + web. Source head 440310a9.

## 0. Summary
Principia already has EVERY physical primitive for continuous, mass-depleting, direction-controlled thrust on a real n-body trajectory. Two machines exist: (1) real-time physical thrust (loaded vessel) — adapter harvests `part.force` each FixedUpdate → `PileUp::AdvanceTime` integrates history with `FlowWithAdaptiveStep` (`pile_up.cpp:596-620`); (2) planned finite burns — `Manœuvre` (constant thrust + Tsiolkovsky mass depletion, `manœuvre_body.hpp:267-278`) via `FlightPlan::BurnSegment` (`flight_plan.cpp:469-495`). **Only gap = the seam under warp: force census gated on `!v.packed` (`ksp_plugin_adapter.cs:1797-1798`)** so under warp `intrinsic_force_`=0 and AdvanceTime takes the coast branch. Engines produce no accel under warp.

## 1. Burns today
- `Manœuvre` (`manœuvre.hpp:38-83`): `Force thrust`, `SpecificImpulse` (thrust÷mass-flow = exhaust velocity), Frenet frame, `is_inertially_fixed`. `mass_flow=thrust/Isp`, `final_mass=m₀−ṁ·dur`. **Key primitive** `ComputeIntrinsicAcceleration` (`manœuvre_body.hpp:267-278`): `direction·thrust/(m₀−(t−t₀)·ṁ)` inside window, 0 outside — time-varying accel with instantaneous mass. Wrapped as `InertialIntrinsicAcceleration`→`Ephemeris::IntrinsicAcceleration` (time-only, `:188-197`) and `FrenetIntrinsicAcceleration`→`GeneralizedIntrinsicAcceleration` (time+state, `:199-210`). **Burns are finite continuous accel, not instantaneous Δv.**
- `FlightPlan` (`flight_plan.hpp:36-269`): coast/burn chain, mass chains across manœuvres (`flight_plan.cpp:169`). `BurnSegment` (`:469-495`) is the integration seam (FlowWithAdaptiveStep with inertial vs Frenet accel). Runs only on the flight-plan trajectory, never vessel history — that's the gap.
- Vessel trajectory (`vessel.hpp`): history → backstory_ → psychohistory_ → prediction_; prediction async (prognosticator `:380-381`), disposable; **history is the real path a burn must modify**.

## 2. RHS hook (where thrust enters the ODE)
`ephemeris.hpp:72-80`: `IntrinsicAcceleration = function<Vector<Acceleration,Frame>(Instant)>`, `GeneralizedIntrinsicAcceleration = function<...(Instant, DegreesOfFreedom)>`. Injection: `FlowWithAdaptiveStep` does `accelerations[0] += intrinsic_acceleration(t)` (`ephemeris_body.hpp:431-433`) / generalized `:464-467`; fixed-step instance sums a vector `:366-381`. Massless integrator = adaptive RKN `DormandElMikkawyPrince1986RKN434FM` (`integrators.cpp:84-92`). **Single clean seam** — any burn as an IntrinsicAcceleration integrates correctly.

## 3. Timewarp mapping
Per frame `Plugin::AdvanceTime` (`plugin.cpp:754-767`) clears loaded intrinsic forces, Prolongs ephemeris; does NOT integrate vessels. Vessel catch-up: `CatchUpLaggingVessels`/`CatchUpVessel` (`:769-826`) → `PileUp::DeformAndAdvanceTime` on thread pool → `vessel->AdvanceTime` extends history. `PileUp::AdvanceTime` (`pile_up.cpp:572-638`): `intrinsic_force_==0` → coast branch (:575); `!=0` → thrust branch integrates HISTORY (:596-620). **Principia DOES integrate vessel history under warp — but always coast, because intrinsic_force_=0 under warp.**

## 4. Exists vs missing
Exists: finite continuous thrust w/ mass depletion; intrinsic-accel RHS injection; history integration with thrust; chained mass + Frenet/inertial direction; real-time thrust into history. **Missing: thrust while packed/under warp (census gated `!v.packed`); resource drain under warp + auto-warp-stop on depletion.** Gap = "real-time physical thrust under warp" vs "planned flight-plan burn". Interstellar cruise wants live throttle for months → flight plan is the reference impl, not the delivery vehicle.

## 5. Prior art & incompatibility
PersistentThrust / BackgroundProcessing / Kerbalism mutate the stock `Orbit` (UpdateFromStateVectors) on rails — cannot change throttle/attitude mid-warp. **Incompatible with Principia**: Principia owns managed-vessel trajectory, writes state OUT to stock orbit (`ApplyToVesselsOnRails`→`UpdateVessel` `ksp_plugin_adapter.cs:1772-1774`), never reads it back — a mod's orbit edits get overwritten. Principia issue #2347 requests a native mechanism. **Must be internal: burn as intrinsic accel on Principia's history, never touch stock Orbit.**

## 6. Mechanism to add
Per-vessel **OnRailsBurn** injecting a Manœuvre-style intrinsic accel into the history integration AdvanceTime already does. Piecewise-constant per frame (const thrust/Isp/direction over [current_time_, t], mass depleting), reproducing a variable-throttle finite burn over many frames.
- **Data** (`pile_up.hpp:196-197`): `std::optional<OnRailsBurn> on_rails_burn_` {Force thrust; SpecificImpulse isp; Vector<double,Barycentric> direction; bool is_inertially_fixed;}. Inertial per frame (adapter hands world→Barycentric XYZ, cf. `:1382`) avoids Frenet on hot path.
- **AdvanceTime branch** (`pile_up.cpp:572-638`): when `on_rails_burn_` set (and intrinsic_force_==0): make psychohistory authoritative, `a(t)=dir·thrust/(m₀−(t−t₀)·ṁ)` (shared helper w/ `manœuvre_body.hpp:273-274`), `FlowWithAdaptiveStep(&trajectory_, accel, t, ...)`, deplete `mass_` by `(t_end−t₀)·ṁ` (use actual reached t_end), dry-mass clamp (integrate to `t_dry`, clear burn, signal warp-stop).
- **Plugin API** (`plugin.hpp/cpp` near `:801-826`): `VesselSetOnRailsBurn(guid, thrust, isp, direction)` / `VesselClearOnRailsBurn` (locate pile-up as CatchUpVessel), run before CatchUpLaggingVessels. C interface `interface_vessel.cpp` (mirror interface_part force fns) + regen P/Invoke.
- **C# adapter** (`ksp_plugin_adapter.cs`): parallel PACKED branch to `:1797-1894`: sum engine thrust + mass-flow → Isp-by-mass; resolve world attitude→Barycentric XYZ; call VesselSetOnRailsBurn when throttle>0 & resources ok; **drain propellant/EC** for warp step (`part.RequestResource`); warp-halt on depletion (`TimeWarp.SetRate(0,true)`, cf. flight_planner.cs:613). Feature-flag gated.
- **Prediction** (`vessel.cpp` FlowPrognostication): feed same intrinsic accel for the burn window so drawn trajectory anticipates thrust.

## 7. Files
1. `manœuvre_body.hpp:267-278` — extract `ThrustAcceleration(dir,thrust,m₀,ṁ,t₀,t)` helper.
2. `pile_up.hpp:196-197` — OnRailsBurn + serialize (mirror intrinsic_force_).
3. `pile_up.cpp:572-638` — new branch + mass bookkeeping + dry clamp.
4. `plugin.hpp/cpp:801-826` — Set/Clear API.
5. `interface_vessel.cpp` (+interface_part pattern) — C entry + P/Invoke.
6. `ksp_plugin_adapter.cs` — packed harvest branch, resource drain, warp-halt, feature flag.
7. `vessel.cpp` FlowPrognostication — prediction consistency.
8. `serialization/ksp_plugin.proto` PileUp — on-rails burn for warp-through-save.

## 8. Mass/Isp/control notes
Law `a=dir·thrust/(m₀−(t−t₀)ṁ)`, ṁ=thrust/Isp; Isp = specific impulse by MASS (exhaust velocity = total thrust ÷ Σ engine mass-flows), not Isp-by-weight. `mass_` (`pile_up.hpp:196`) decremented per frame; tanks drained in C#; on unpack KSP part masses re-assert (`InsertOrKeepLoadedPart :1354`). Throttle+direction re-read every frame ⇒ fully live under warp (the advantage over PersistentThrust). MVP inertial-fixed direction (time-only overload); Frenet-locked later (generalized RHS `:464-467`). Never write stock Orbit.

Sources: PersistentThrust (SpaceDock 2450, bld/PersistentThrust GitHub), Persistent Thrust Extended (KSP forums), Principia issue #2347.

## 9. Addendum (2026-07-03, owner + fable) — attitude, gating, resources: grounded

**Rotation-under-warp problem (owner).** Principia integrates pile-up rotation under warp
(EulerSolver, torque-free); in-game SAS cannot null residual spin perfectly, so over
month-scale burns any attitude-derived thrust direction rotates away (1e-4 °/s ≈ one full
turn per 115 d) and lateral thrust washes out. Decisions:
- **Burn direction is COMMANDED, not attitude-derived** — the flight planner's own guidance
  assumption (`Manœuvre.is_inertially_fixed` / Frenet) extended to on-rails burns. Core takes
  a per-frame direction (inertial MVP; Frenet mode later via the generalized RHS). Adapter
  direction sources: inertial-hold, per-frame prograde/target/etc. (all reduce to a per-frame
  inertial vector; no core change).
- **Spin-following thrust (EulerSolver-evolved direction) REJECTED**: physically exact but
  useless for the target scenario (long cruises with imperfect SAS). Rotational state stays
  untouched — no conservation violation; thrust-vs-display attitude mismatch documented,
  cosmetic display alignment optional later (adapter-side).
- **GATE (adapter, every warp frame)**: net engine thrust torque about CoM within the
  vessel's attitude-control authority (margin TBD), control powered. Σ r×F per
  `thrustTransform` (RCS Build Aid algorithm — editor-only mod, LGPL-3.0, m4v/RCSBuildAid
  @81ee807: Plugin/{EngineForce,MarkerForces}.cs; flight-time reference MechJeb2
  VesselState.cs @4c38069, GPL-3.0 — all APIs packed-valid) vs. per-axis authority summed
  from stock `ITorqueProvider.GetPotentialTorque(out pos, out neg)` (ModuleGimbal,
  ModuleReactionWheel, ModuleControlSurface). This unifies owner conditions (a) torque-free
  thrust and (b) attitude control present into one physical check; (c) EC = presence +
  per-frame drain.
- **On gate violation or depletion**: cut burn + `TimeWarp.fetch.CancelAutoWarp()` +
  `TimeWarp.SetRate(0, /*instant=*/true)` (KAC + PersistentThrust production pattern).

**Resources, verified (sonnet agents, raw-source citations):**
- **PACKED active vessel**: `Part.RequestResource` fully works on rails — stock
  `ModuleCommand.FixedUpdate` drains EC on rails (hibernation ×0.01 exists because of it);
  Kopernicus solar panels charge unconditionally (KopernicusSolarPanel.cs:421,633 @fc66962).
  Drain = ṁ/ρ · `TimeWarp.fixedDeltaTime` (already warp-stretched). Double-drain guard when
  unpacked: PersistentThrust `simulate` flag inversion (sswelm/PersistentThrust
  PersistentEngine.cs:1181 @8f2fbb4).
- **UNLOADED vessel**: stock simulates nothing. State = `ProtoPartResourceSnapshot.amount`
  (public field; direct write persists; `UpdateConfigNodeAmounts()` before Save). Background
  engine prior art: PersistentThrust `BackgroundProcessing/` (the ONLY mod doing engines;
  ships Helpers/DetectPrincipia.cs — read for interop) + Kerbalism scheduler discipline
  (≤1 unloaded vessel per tick, deferred clamped to [0, capacity], no sub-stepping;
  Kerbalism license = Unlicense → borrowable). Kerbalism does NOT sim background engines.
- **SCOPE SPLIT**: MVP = packed active vessel (scenario A; §6-7 stand, now verified).
  Unloaded background burns = phase 2 (proto-snapshot resource pass + own scheduler + flow
  re-implementation; warp-stop on violation applies there too, per owner).

**Monitoring/alert prior art (Kerbalism @660a802, follow-up 2026-07-03) — the
violation→warp-stop pipeline we should mirror:**
- Detection: `ResourceInfo.Sync` computes `Level`, `AverageRate`, `DepletionTime()`
  (Resource.cs:906-975) — identically for unloaded vessels (proto-snapshot sync set,
  round-robin one vessel/tick).
- Thresholds: `Supply.Execute` (Profile/Supply.cs:36-75) — low = 15% (`Severity.warning`),
  empty = epsilon (`Severity.danger`); EC alerts fire even for UNCREWED probes (other supplies require crew), with a SAVE-PERSISTED once-per-crossing latch
  (`SupplyData.message`) so alerts fire once per crossing (anti-spam; copy this).
- **Central choke point**: `Message.Post(severity, …)` itself calls `Lib.StopWarp()` for
  warning-or-worse (UI/Message.cs:145-148) — ANY vessel's emergency (incl. background)
  halts warp. `Lib.StopWarp` (Lib.cs:356-367) = `CancelAutoWarp()` +
  `TimeWarp.SetRate(maxRate_below_cap, /*instant=*/true, /*postScreenMessage=*/false)`;
  default cap 0 = full stop.
- Monitor UI reads the same ResourceCache (`Level`/`DepletionTime`, red ≤0.5%, orange
  ≤15%) — cheap property reads, no proto walk in the UI path.
- EC-death contract: `powered = EC > ε` → CommNet `connection.linked=false` → probe goes
  DARK (uncontrollable, not destroyed) + "signal lost" warning (itself a warp stop).
- **Mapping to our adapter**: gate violation / propellant-or-EC depletion → cut burn (core
  one-shot semantics already coast automatically) + latched popup + CancelAutoWarp +
  SetRate(0, true). Our `max_duration` already encodes time-to-depletion, so the C++ core
  cuts thrust exactly at exhaustion even mid-step; the adapter's job is only detection +
  message + warp stop. If Kerbalism is installed its own EC alarms coexist harmlessly
  (same stock TimeWarp API). Phase-2 background burns adopt the round-robin + choke-point
  pattern wholesale.

## 10. Addendum (2026-07-08, session 19 — R5) — the *powered ⇒ non-collapsible* invariant

**Invariant.** A history segment that carries an on-rails burn is a *powered* thrust
arc, not a gravitational coast, and MUST remain non-collapsible: it is checkpointed and
reconstructed exactly, never collapsed to its endpoints and later re-integrated as a
coast. Collapsing a powered segment would let reanimation replay it force-free, so the
reloaded vessel would drift off the arc it actually flew.

**Why it needs stating.** Reusing the intrinsic-acceleration machinery (§6) was the right
call, but this collapsibility interaction was left implicit and surfaced as a bug: the
powered points appended during a burn could land in a *collapsible* segment, because
`Vessel::AdvanceTime` runs collapsibility detection inside
`FreeVesselsAndPartsAndCollectPileUps` — *before* the catch-up applies the burn, when the
burn is not yet known.

**Enforced.** `Vessel::IsCollapsible` treats a pile-up's live `on_rails_burn` /
`on_rails_burn_for_prediction` as non-collapsible; and `Vessel::AdvanceTime` re-detects
collapsibility in the catch-up (where `on_rails_burn_for_prediction` is live) before
appending the powered points, so they land in a non-collapsible, checkpointed segment.

**Tested.** `VesselTest.IsCollapsible` asserts the predicate (a live burn ⇒ not
collapsible). The *outcome* — a burn survives a save / forced-drop / reanimation
round-trip because it was checkpointed non-collapsibly — is covered end-to-end by
`OnRailsBurnHistorySurvivesReanimation` and the forced-drop golden fixture
`AnchoredBurnSurvivesDropAndReanimation` (the latter lowers the serialize threshold so the
drop actually engages).
