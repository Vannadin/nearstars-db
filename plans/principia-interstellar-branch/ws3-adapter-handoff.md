# WS3 adapter handoff — thrust under timewarp, C# side (Windows/Opus session)

Status: the C++ core is DONE and gate-tested on the Mac (branch `nearstars-interstellar`;
see `.nearstars/context-notes.md` in the Principia clone for commit hashes). This file
specifies the remaining `ksp_plugin_adapter` (C#) work. Read `research/R4-thrust-under-warp.md`
(esp. §6 and the §9 addendum — design decisions, verified APIs, citations) before coding.

## What the C++ core already provides

- `PileUp` on-rails burn: constant thrust / specific-impulse(by mass) / inertially fixed
  direction / max duration, applied by the catch-up integration with Tsiolkovsky mass
  depletion, exact mid-step cutoff when the propellant window ends, and pile-up mass
  bookkeeping. The burn is **ONE-SHOT**: consumed by each catch-up; the adapter must set it
  again before every catch-up during which the engines burn on rails.
- Predictions anticipate the burn applied by the last catch-up (self-maintaining copy;
  a catch-up without a burn clears it).
- C ABI (already in `interface.generated.cs` after the generator runs on Windows too):
  ```csharp
  void plugin.VesselSetOnRailsBurn(string vessel_guid,
                                   double thrust_in_kilonewtons,
                                   double specific_impulse_in_seconds_g0,  // Isp by WEIGHT, s
                                   XYZ direction,          // World axes; needs not be unit
                                   double max_duration);   // s of propellant available
  void plugin.VesselClearOnRailsBurn(string vessel_guid);
  ```
  The C++ side converts s·g₀ → exhaust velocity and World → Barycentric (rotation only),
  normalizes the direction, and finds the pile up (no-op with a warning if there is none).

## Adapter work items (MVP = packed ACTIVE vessel; feature-flag gated)

1. **Packed harvest branch** parallel to the `!v.packed` force census
   (`ksp_plugin_adapter.cs` ~1797-1894): when the active vessel is packed under warp,
   throttle > 0 and the GATE (item 3) passes, compute
   - total thrust (kN) = Σ engine `finalThrust`-equivalent at current throttle (engines
     ignited & operational; use `thrustTransforms` sum semantics),
   - Isp by mass → pass as seconds-g₀ (the interchange unit): total thrust ÷ Σ(thrustᵢ/Ispᵢ),
   - direction: the commanded axis in World (see item 5),
   - `max_duration` = min over involved propellants of (available amount ÷ per-second
     drain), the resource-limited burn time,
   and call `VesselSetOnRailsBurn` BEFORE the catch-up call for that frame.
2. **Resource drain**: each such frame, drain per-propellant
   `ṁᵢ/ρᵢ · TimeWarp.fixedDeltaTime` (already warp-stretched) via `part.RequestResource`
   (works while packed — verified, R4 §9) + EC for the control condition. Guard against
   double-drain when unpacked: only drain in the packed branch (stock handles unpacked;
   cf. PersistentThrust's `simulate`-flag inversion, PersistentEngine.cs:1181 @sswelm 8f2fbb4).
3. **GATE, every warp frame** (all APIs packed-valid; R4 §9):
   - net thrust torque Σ (rᵢ − CoM) × Fᵢ over engine `thrustTransforms` (RCS Build Aid
     algorithm; MechJeb2 VesselState.cs is the flight-time reference),
   - attitude-control authority: Σ `ITorqueProvider.GetPotentialTorque(out pos, out neg)`
     over ModuleGimbal / ModuleReactionWheel / ModuleControlSurface, per-axis envelope,
   - condition: |net torque| ≤ authority × margin (margin TBD, start 0.5), AND EC present.
4. **Violation / depletion reaction**: cut the burn (`VesselClearOnRailsBurn` — or simply
   don't re-set it), post a LATCHED on-screen message (once per crossing, Kerbalism
   `SupplyData.message` pattern) and halt warp:
   `TimeWarp.fetch.CancelAutoWarp(); TimeWarp.SetRate(0, true);`
   (KAC + PersistentThrust production pattern). C++ cuts thrust exactly at propellant
   exhaustion mid-step regardless, so the physics is safe even if the adapter reacts a
   frame late.
5. **Direction sources** (MVP): hold-current-attitude (engine axis in World at this frame),
   plus adapter-computed inertial vectors for prograde/retrograde/target-relative modes —
   all reduce to a per-frame World vector; no C++ change. A true Frenet-following mode is
   a later C++ extension (generalized RHS; R4 §8).
6. **Feature flag**: gate the whole branch behind a Principia settings flag (default off
   until in-game validated).
7. **In-game smoke test** (the part the Mac cannot do): stock system, probe + ion/chemical
   stage, burn at 100×–10⁶× warp; verify trajectory bends, tanks drain, warp stops on
   depletion, prediction shows the burn, save/load mid-burn continues cleanly, and the
   vessel behaves when unpacking mid-burn (KSP re-asserts part masses; stock takes over
   thrust).

## Phase 2 (explicitly out of MVP): unloaded background burns

Requires a from-scratch background pass (stock simulates nothing for unloaded vessels):
enumerate `protoPartSnapshots`, read engine state from `moduleValues` ConfigNodes, write
`ProtoPartResourceSnapshot.amount` directly, one stalest vessel per tick + clamp (Kerbalism
scheduler discipline, Unlicense; PersistentThrust `BackgroundProcessing/` is the only
engine prior art — it also ships `Helpers/DetectPrincipia.cs`, read it for interop
expectations). Owner requirement: gate violations on background vessels must ALSO stop
warp (Kerbalism's Message.Post choke-point pattern).

## Kerbalism stance

No dependency — everything above is stock-API only. If Kerbalism is installed its own EC
alarms coexist harmlessly (same stock TimeWarp API). Do NOT rely on Kerbalism for
detection; our adapter owns the burn-condition monitoring.
