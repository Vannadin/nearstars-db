---
title: WS4 minimal-fork warp — C#/adapter implementation handoff (Windows session)
status: READY — C++ side verified done (no fork needed); C#/cruise side to implement
owner decision: minimal-fork chosen (2026-07-04); see R7 for the alternative rejected
grounds: R7 §4/§9, gameplay/interstellar-expansion/warp/warp-patch-draft.md, plugins/NearStarsWarp/
target base: fork head 1727a86fa, gate 184
---

# WS4 minimal-fork warp — implementation handoff

The owner chose the **minimal-fork** path (R7). This doc is the go-list for the Windows/C# session
(Schultz's lane). It consolidates what is already verified vs. what remains, so the implementation
does not re-derive it. Read alongside `gameplay/interstellar-expansion/warp/warp-patch-draft.md`
(the patch sketch + cruise-plugin skeleton) and R7 (`research/R7-warp-support.md`).

## What the minimal-fork warp is (one paragraph)

A vessel under NearStars warp is **released by Principia** (dropped from the managed set) for the
duration of the cruise; a custom cruise layer moves it with stock KSP calls; on dropout the flag
clears and Principia **re-adopts** it from its new stock orbit around the destination star. The
C++ trajectory/flight-plan are destroyed on release and rebuilt fresh on arrival (flight-plan loss
on warp is accepted). No new C++ API, no `VesselSetState` ABI.

## C++ side — VERIFIED DONE, nothing to fork

This session verified the two load-bearing C++ assumptions with headless tests on the fork
(no code change was needed — the existing machinery already does the right thing):

- **Subsystem assignment is automatic.** `PluginIntegrationTest.WarpReadoptionLandsInDestination‑
  Subsystem` (commit `1727a86fa`): a vessel re-adopted around a star in another subsystem is
  constructed with that subsystem (from its parent celestial, `vessel.cpp:93`) and its trajectory
  is anchored at that subsystem's local origin — NOT offset by the interstellar distance. So a
  warp across the void needs **no C++ re-seed fork**; just re-adopt with the destination star as
  the parent.
- **Save/load + reanimation preserve the vessel state.** `OnRailsBurnHistorySurvivesReanimation`
  (commit `280cf4d9b`): a re-adopted vessel round-trips through save/load intact. (The
  reanimation-across-thrust coast approximation is a rare, mid-session-drop-only path — R7 finding,
  accepted.)

⇒ **The Windows session touches only C# (adapter + cruise plugins). The C++ core is ready.**

## C# work — the go-list

### 1. The one fork line (adapter)
In the fork's `ksp_plugin_adapter/ksp_plugin_adapter.cs`, `UnmanageabilityReasons(Vessel)`
(the patch draft cites ~620–660 on 2026-06 master — **reconfirm the signature + line on the fork
head**, it has diverged): add ONE OR-term so a vessel flying the NearStars warp flag is reported
unmanageable (thus released). Read the flag from a stock channel (`KSPField`/GUID-map by name) to
avoid a Principia↔NearStars compile dependency. This is the entire Principia-side change.

### 2. Cruise layer (no fork — `plugins/NearStarsWarp/`)
Per `warp-patch-draft.md` §2: `WarpCruise.cs` state machine (Idle→Spooling→Cruising→Dropout),
capture v0 in the Sol-barycentric frame at engage, move continuously while released,
`WarpDriveModule.cs` (PartModule + ExoticMatter fuel, `warp_exotic_matter.py`),
`WarpFlagBridge.cs` (fills the relativity layer's `WarpFlag.Provider`).

### 3. Velocity on dropout — the one thing to get right (cruise-side, no fork)
Principia re-adopts from the stock orbit, setting barycentric velocity = `v_deststar + v_orbit`
(R7 §9.2). So the cruise layer must write the drop-out stock orbit's **relative velocity** to
achieve the intended arrival:
- **Realistic (default):** `v_orbit = v0 − v_deststar` → barycentric velocity = v0 preserved →
  a hyperbolic arrival carrying the true interstellar closing velocity (the braking leg bleeds it
  off). The navigation planner already computes this arrival velocity.
- **Casual (difficulty toggle, owner's idea):** write a bound parking orbit → the vessel arrives
  co-moving with the destination star (interstellar Δv waived). Same code path, different chosen
  `v_orbit` — a free game-setting toggle, NOT a bug (R7 §7.4).
Confirm v0 capture is in the same barycentric frame Principia re-adopts into (World→Barycentric of
a velocity needs the full RigidMotion, R7 §9.2).

### 4. Re-adoption mechanics (confirm in-game)
On dropout: clear the flag, set the destination stock orbit around the destination star
(so `vessel.mainBody` = destination star), and let the next Principia tick re-adopt via
`CreateTrajectoryIfNeeded` — which, verified above, assigns the destination subsystem and anchors
at the right origin. No further action.

### 5. Stock teleport artifacts the arrival must handle (s25 instrumented findings, 2026-07-18)

Both were root-caused in-game on the fork's WS5 test rig (a live cheat teleport is
mechanically the same thing as a warp arrival — a large single-step state write with a
mainBody switch); records in the Principia clone, `.nearstars/checklist.md` WS5-C2 section.

- **Phantom geeForce blocks saves and KSC exit (WS5-C2-R2).** A live teleport out of a
  rotating-frame situation (departure below the home body's inverse-rotation threshold)
  can leave the world-frame rotation state uncleared: `obt_velocity` keeps rotating at the
  departure body's ω, stock's `Δobt_velocity/Δt − graviticAcceleration` accounting then
  reads a PERMANENT phantom acceleration ω×v (measured: |pert| = ω_Kerbin × v to 6
  significant digits, constant for minutes), and `FlightGlobals.ClearToSave` refuses at
  `geeForce > 0.1` — the player cannot quicksave or leave for KSC after arrival. The
  cruise layer must (a) avoid engaging from an inverse-rotation state, or explicitly
  ensure the frame state is rebuilt on arrival, and (b) wrap the arrival write in
  `vessel.IgnoreGForces(frames)` (public stock API; stock itself uses it after its own
  teleport-scale moves, Vessel:6257) so the acceleration smoothing never captures the
  jump. Symptom signature if it slips through: "under acceleration" exit refusal with a
  CONSTANT G readout; heals on KSP restart + load.
- **Stale landed state NREs on the PQS-less destination (checkLanded family).** Any
  stale `GroundContact`/`PermanentGroundContact` or `landed=True` arriving at a star hits
  four unguarded `pqsController` dereferences (decouple abort → per-frame NREs → part
  explosions; poisoned saves NRE on every load). Fixed ecosystem-side by
  **InterstellarFluxFix v1.1.0** (invariant enforcement: PQS-less ⇒ not landed, stale
  flags cleared at source) — which is therefore a REQUIRED companion of the NearStars
  release, not just a thermal fix. The cruise layer itself needs no code for this, but
  do not strip FluxFix from the install.

## Acceptance (in-game, Windows)
- A vessel warps Sol→destination system, is released mid-cruise, and re-adopts around the
  destination star in the correct subsystem (confirm no NaN/precision blowup — the C++ test covers
  the headless case; confirm in-game).
- Realistic mode: the vessel arrives with the interstellar closing velocity (hyperbolic), brakeable.
- Casual mode: arrives in the written parking orbit.
- Flight-plan loss on warp is expected (accepted).
- Save/load mid-cruise (vessel released, purely stock-side) and post-arrival both survive.
- **Post-arrival hygiene (§5):** quicksave AND flight→KSC exit succeed after arrival; the
  geeForce readout is ~0 on a coast (a constant nonzero G = the §5 phantom, fail).

## Related
- `research/R7-warp-support.md` — full feasibility/failure-catalog/decision; §9 the C++ deep dives.
- `gameplay/interstellar-expansion/warp/warp-patch-draft.md` — the patch sketch + cruise skeleton.
- `ws4-warp-support-backlog.md` — the workstream stub.
- `ws3-adapter-handoff.md` — the sibling WS3 adapter handoff (same Windows session lane).
