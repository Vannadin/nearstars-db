# NearStars — Relativity layer (Tier 0 mechanic, DRAFT)

Status: **draft, not compiled or tested** (no KSP/Unity/Principia DLLs in this
repo). Authored Opus-side per the spec; Schultz integrates, verifies the API
touchpoints, compiles, and tests in-game (Sonnet-side). Spec of record:
[`gameplay/interstellar-expansion/relativity-mod.md`](../../gameplay/interstellar-expansion/relativity-mod.md)
(§2.6 guards, §3 hand-off).

## What it is

The sub-light special-relativity **gameplay** layer, Tier 0 only (no visuals):
near `c`, effective thrust falls as 1/γ³ (light becomes a natural wall) and
proper-time resource burn slows as 1/γ (fast crews last longer). It modulates
force and consumption rate — it never touches the integrator, so it is
Principia-safe and rides on the stock profile identically.

## Files

- `RelativityState.cs` — **the correctness core (pure logic).** β/γ and the three
  §2.6 guards (activation gate / warp exemption / kraken fail-safe). The only KSP
  touchpoints are velocity + SOI in `BarycentricSpeed`, marked `VERIFY`.
- `ThrustCorrector.cs` — the force hook. Adds `−(1 − 1/γ³)·F_engine` into the
  part-force channel before Principia's stage-7 sample, so net force = `F/γ³`
  while propellant stays at its nominal coordinate-time rate.
- `WarpFlag.cs` — shared "under warp/jump" flag (the warp plugin fills it; safe
  default = not warping).
- `ResourceScaler.cs` — the reward side. Pure decision logic: which resources are
  proper-time (scale ×1/γ) vs coordinate-time (untouched), and the rate multiplier.
  The Kerbalism wiring point is marked `VERIFY`.
- `RelativityDashboard.cs` — IMGUI readout (β, γ, effective thrust %, supply-rate
  %), shown only while the mechanic is active.

## Done in this draft

- Pure β/γ math + all three §2.6 guards, ordered and fail-safe.
- Barycentric-speed derivation (SOI==Sun fast path + parent-chain fallback).
- Corrective-force strategy (preserves fuel; works on both profiles); engine
  thrust summation; longitudinal 1/γ³ model.
- Resource classification (§4 Q4 proper-time set) + rate multiplier.
- Dashboard window (auto-hides when inactive).

## TODO before it ships (Schultz / keyboard)

- **VERIFY the correction timing** — the one real risk. Confirm the engine thrust
  is deposited before our callback and our callback runs before Principia's
  `FashionablyLate` (stage 7). If `Normal` is too early, use strategy (B): a
  Harmony postfix on the engine thrust step calling `ThrustCorrector.ApplyCorrection`.
- **VERIFY KSP API**: `Part.AddForce` units (kN) + that it feeds the channel
  Principia samples; `ModuleEngines.finalThrust` / `thrustTransforms`;
  `Orbit.GetFrameVel()` / `obt_velocity` units.
- **Wire `WarpFlag.Provider`** to the warp plugin (shared static or VesselModule).
- **Principia profile**: source barycentric velocity from Principia (read-only)
  when present.
- **Wire `ResourceScaler` into Kerbalism** — the decision logic is done; the
  remaining work is the Harmony hook that calls `RateMultiplier` at the right point
  in Kerbalism's per-vessel sim step (most API-fragile piece — see its VERIFY block).
- **Verify `ResourceScaler.ProperTimeResources`** names against live Kerbalism/RP-1.
- Unloaded-vessel handling (background thrust under Principia) — MVP does the
  loaded vessel only.
- Dashboard polish — optional ApplicationLauncher toggle; confirm GUI id.
- `.csproj` with refs (Assembly-CSharp, UnityEngine.*; Principia/Kerbalism as
  optional/soft deps); output to `GameData/NearStars/Plugins/`.
- Move tunables (`BetaMin`, `BetaSane`) into a `.cfg` read via GameDatabase.
