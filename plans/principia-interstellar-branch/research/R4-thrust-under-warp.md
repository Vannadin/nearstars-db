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
