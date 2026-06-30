# NearStars — Warp-under-Principia (cruise layer, DRAFT)

Status: **draft, not compiled or tested** (no KSP/Unity/Principia DLLs in this
repo). Authored Opus-side per the spec; Schultz forks Principia, integrates,
verifies the API touchpoints, compiles, and tests in-game. Spec of record:
[`gameplay/interstellar-expansion/warp-patch-draft.md`](../../gameplay/interstellar-expansion/warp/warp-patch-draft.md).

## What it is

The continuous, steerable warp cruise from the brainstorm's **minimal-fork** path:
one `UnmanageabilityReasons` exclusion in Principia releases the vessel; a custom
propagator moves it (carrying its barycentric `v0`, frame (a)); on dropout it
re-seeds a stock orbit at the destination and Principia re-adopts it. Flight plan
is lost on warp (accepted — replan at destination).

**This plugin is inert without the §1 Principia fork** — `PrincipiaInterop.Detach`
raises a flag a patched `principia.dll` must read. On the non-Principia profile
the interop is a no-op and the cruise core runs on SigmaBinary + stock conics.

## Files

- `WarpCruise.cs` — **correctness core (pure logic).** Engage/cruise/dropout state
  machine, smoothstep spool ramps (no teleport pop), v0 carry, FTL step. No KSP calls.
- `WarpDriveModule.cs` — `PartModule`: engage/disengage UI, ExoticMatter gate +
  drive-energy drain (gameplay model), applies the cruise step each FixedUpdate.
- `PrincipiaInterop.cs` — **the fork seam.** Detach (raise flag) / re-seed (set stock
  orbit, clear flag). `REQUIRES FORK`; no-op without Principia.
- `WarpFlagBridge.cs` — fills `NearStars.Relativity.WarpFlag.Provider` so the
  relativity layer exempts a warping vessel (§2.6(ii)).

## Done in this draft

- Pure cruise state machine + velocity-continuity (frame (a)) + FTL propagator step.
- The minimal-fork detach/re-seed strategy expressed as an interop seam.
- Gameplay energy model wired (ExoticMatter standing load + MJ drive drain), matching
  `prototypes/warp_exotic_matter.py`.
- Cross-plugin warp-flag bridge to the relativity layer.

## TODO before it ships (Schultz / keyboard)

- **The fork itself** — add the one `UnmanageabilityReasons` OR-term to a Principia
  fork; confirm it drops the vessel from the kept-set and that dropout re-seeds from
  the new stock orbit (warp-patch-draft.md §1, §5.1). The one load-bearing assumption.
- **Flag channel** — KSPField/GUID-map vs compile dependency (§1.2, §5.2). Prefer the
  stock-field channel so Principia↔NearStars stay decoupled.
- **VERIFY KSP API**: `vessel.SetPosition` / `GetWorldPos3D` (floating-origin + Kraken
  safe) while detached; `vessel.SetOrbit` / `UpdateFromOrbitAtUT` on re-seed;
  `RequestResource` for ExoticMatter/Megajoules; `obt_velocity` units/frame;
  `FindPartModuleImplementing`.
- **Barycentric v0 as a vector** — reuse the relativity layer's `BarycentricSpeed`
  derivation; source from Principia (read-only) on the Principia profile.
- **Planner wiring** — `PlotCourse(dest, arrivalVel)` is fed by the lead-intercept
  planner (`prototypes/planner_*.py` → in-game UI); confirm the destination-orbit
  representation.
- **Re-seed continuity** — confirm no part loss / pop / save-load break across
  detach→cruise→re-adopt.
- **`.csproj`** with refs (Assembly-CSharp, UnityEngine.*; Principia optional/soft;
  NearStarsRelativity for the flag bridge); output to `GameData/NearStars/Plugins/`.
- Move tunables (`warpBeta`, `exoticPerTonne`, `mjPerTonneLy`, `SpoolDur`) into `.cfg`.
