---
title: Warp mechanics under Principia + interstellar navigation — brainstorm
status: active
created: 2026-06-28
---

# Warp under Principia + interstellar navigation — brainstorm

**Stage: brainstorm / exploratory — not committed.** Captures the warp-mechanics
and navigation ideas from the 2026-06-28 session. Extends
[`feasibility.md`](feasibility.md) (gate 0). Source-grounded findings are marked
**[src]** (Principia `mockingbirdnest/Principia` @ master); the rest are design
ideas to validate. In-game C#/C++ is Schultz's lane
([[project-nearstars-mod-plugins-schultz]], [[project-principia-custom-branch]]);
this side does design/spec/cfg + math prototypes.

---

## 1. Requirements (owner)

- **Continuous cruise**, not a discrete jump — steerable, takes in-game time,
  abortable/redirectable mid-flight, "see the stars go by."
- **Velocity continuity at warp start** — carry the entry relative velocity v₀
  through and drop out at it (Alcubierre "no momentum change" property).
- **Must coexist WITH Principia.** The non-Principia profile is trivial (just
  don't install Principia) and is *not* the goal. The whole exercise is
  warp + Principia together.

## 2. Why warp is hard under Principia  [src]

- Authoritative vessel state is a C++ `DiscreteTrajectory` (`vessel.cpp`); KSP's
  transform is overwritten every frame from Principia's integration
  (`ksp_plugin_adapter.cs` `UpdateVessel` ~516–525, the `part_rb.position = …`
  write). Comment: *"nobody will know that they're not the ones obtained by Unity."*
- The apparent-motion channel **discards CoM translation** — `DeformPileUpIfNeeded`
  (`pile_up.cpp` ~445–578) keeps only attitude (Davenport q-method); `NudgeParts`
  re-anchors to the integrated CoM. *"We cannot use the apparent motion of the
  centre of mass, because the game does not conserve momentum."* → an external
  `SetPosition` is read in, its translation thrown away, integrated position
  written back the same frame. This is why HyperEdit/Blueshift "have no effect"
  (issue #1420, wontfix).
- Principia **governs ALL managed vessels** — loaded AND unloaded/packed
  (`adapter.cs` vessel loop ~1311–1327; background catch-up ~1700–1768). There is
  **no vessel state where stock OrbitDriver governs** a managed vessel; on-rails
  is also overwritten (`vessel.orbit.UpdateFromStateVectors` ~522). Stock orbit
  set ⇒ doesn't stick.
- Authoritative DoF is **seeded from KSP stock orbit exactly once** — first
  insertion of an unknown GUID (`CreateTrajectoryIfNeeded` guarded by
  `trajectory_.empty()`, `vessel.cpp` ~232–256). Never re-seeds while the Vessel
  object lives. **No in-place re-seed / `ResetVessel`.**
- `ExternalInterface` is **read-only and being removed** (Landau last → Laplace
  unimplemented → Laurent removed, late 2025). So no future "set state" hook is
  coming upstream; CONTRIBUTING: "unsolicited contributions seldom welcome."
- **"Just disable the revert" is the wrong layer** — the write-back is a symptom;
  authority is the integrated trajectory. Suppressing it → craft snaps back next
  frame + pile-up/prediction/save-load break.
- **Jump fits, cruise fights.** A discrete jump = one new initial condition,
  integrated forward — fits cleanly. Continuous cruise = overriding the
  integrated CoM ~50×/s, exactly what `DeformPileUpIfNeeded`/`NudgeParts` reject.

## 3. The options ladder (how to get cruise anyway)

| Path | Cruise? | Flight plan | Fork | Rebase burden |
|------|:------:|------------|------|---------------|
| **No-fork (crude free + re-seed)** | ✗ jump only | lost | none | none |
| **Minimal fork — `UnmanageabilityReasons` flag** | ✓ | lost (acceptable) | small, stable area | light |
| Big fork — `VesselSetState` C ABI | ✓ | can preserve | large, integrator internals | heavy |

- **No-fork crude  [src]** — make Principia free the vessel's C++ `Vessel` for ≥1
  frame (it drops from the kept-set → `FreeVesselsAndPartsAndCollectPileUps`
  erases it, `plugin.cpp` ~688–704), move the stock vessel, let it re-insert →
  re-seeds from the new stock orbit. **Loses Principia trajectory history +
  flight plan** (they live in the destroyed C++ object; the "zombie" map carries
  only prediction adaptive-step params). **KSP GUID/parts/crew survive.**
  Inherently a discrete JUMP. No deep-space-compatible "unmanaged situation"
  exists to hold a vessel detached through a whole cruise (LANDED/PRELAUNCH are
  surface-only) — so no-fork = jump only.
- **Minimal fork (the sweet spot)** — the only Principia detach gate is the
  `UnmanageabilityReasons` filter (`adapter.cs` ~620–660; excludes non-
  ORBITING/FLYING/etc., DEAD, pos==0, hack-gravity; **no VesselType check**).
  Add **one per-vessel exclusion condition** ("flag X ⇒ unmanaged"). Then:
  engage → flag → Principia releases the vessel → custom continuous cruise
  (carry v₀) → dropout sets stock orbit at destination + clears flag → Principia
  re-seeds via the existing first-insertion path. **Cruise works; flight plan
  lost; GUID kept.** Lives in a *stable filter*, not the integrator → far lighter
  monthly-rebase risk than a `VesselSetState`. *(Design inference from confirmed
  mechanism — verify with Schultz.)*
- **Big fork** — add a `VesselSetState(guid, barycentric DoF)` C ABI that clears
  & re-seeds the trajectory in place. Could preserve identity/flight-plan, but
  touches integrator internals (heavy rebase) and is unnecessary if flight-plan
  loss is acceptable.

**Working assumption: flight-plan loss on warp is acceptable** — you replan at
the destination system anyway.

## 4. Cruise architecture (ⓑ2)

Continuous cruise lives in a **custom interstellar travel layer above Principia's
physics scene**, not inside its tick integration:

1. **Engage** → mark vessel unmanaged (minimal-fork flag) → Principia releases it.
2. **Cruise** → custom propagator moves it continuously & steerably, carrying v₀.
   Other vessels/bodies keep their Principia trajectories; time passes normally.
3. **Dropout** → set destination stock orbit + clear flag → Principia re-adopts
   from that state.

Principia only touches the two endpoints (detach / re-seed), so there is no
per-tick fight.

## 5. Fork reality  [src]

- **License: MIT** (`LICENSE.txt`, Robin/Pascal Leroy = eggrobin). Fork, modify,
  redistribute a modified `principia.dll` freely; keep notices (Principia's +
  bundled deps abseil/protobuf/zfp/…). Our data-sources "MIT" is correct.
- **Build: heavy** — pinned MSVC 2022 (VS 2026 incompatible) / Clang 20, many
  `deps` submodules + real KSP assemblies, OOM pitfalls. macOS build is
  "best-effort/untested" and the *shipping* artifact must be a Windows DLL
  (NearStars is Windows-only).
- **Upstream won't take it** — mod API is being deleted; "unsolicited
  contributions seldom welcome." ⇒ **permanent divergent fork.**
- **Distribution** — single DLL at `GameData/Principia/x64/principia.dll` ⇒
  **mutually exclusive with official Principia**, breaks CKAN; Principia releases
  monthly (KSP-version-locked) ⇒ rebase treadmill. The minimal-fork flag
  mitigates this (stable code area), but the fork burden is real.

## 6. Velocity continuity + the inter-stellar frame decision

- **Mechanical carry** — capture v₀ at engage, carry through cruise, restore at
  dropout. KSPIE/Blueshift already do "drop out at entry velocity."
- **Open decision — which frame's velocity is preserved across the gap?** Stars
  move (Barnard ~140 km/s proper motion), so carrying origin-frame v₀ means you
  arrive at the destination with the inter-stellar relative velocity added.
  - (a) **barycentric preserve** — arrive carrying the real relative velocity
    (realistic; arrival is a challenge).
  - (b) **destination-rest** — arrive at rest vs the target star (convenient; gamey).
  - (c) middle.
  Novel to NearStars (existing warp mods are stock-scale fake binaries).

## 7. Interstellar navigation planner

Principia moves the stars (perturbers with real space velocities; binaries also
orbit), so interstellar nav is a **lead-intercept** — aim where the star will be
at arrival, not where it is now. Principia's own flight planner can't do the warp
leg (detached, non-gravitational, flight-plan dropped) ⇒ **custom planner needed.**

- **Key simplification** — at interstellar separation mutual gravity ≈ 0, so a
  single star moves ~**linearly**: `P(T) = P₀ + v_star·T`, computed from the DB's
  ICRF position + velocity. Binary: add the known orbital term (elements in DB).
  ⇒ **no dependence on Principia's read API** (which is being removed). Big win.
- **Solver** — fixed-point lead-intercept: guess transit time T → star position
  P(T) → distance → warp time for that distance → update T → converge. Output:
  **heading + transit time + arrival relative velocity** (the last tied to the
  §6 frame decision).
- **Profiles** — Principia profile *needs* lead-intercept (stars drift); stock
  profile likely near-static ⇒ simpler direct-aim.

## 8. Open decisions / next

- Velocity-frame decision (§6: a / b / c).
- Verify the minimal-fork `UnmanageabilityReasons` flag actually detaches cleanly
  & re-seeds (with Schultz).
- Prototype the lead-intercept math (validate convergence + show how the frame
  decision changes arrival), like the Δv map.
- Confirm flight-plan-loss-on-warp is acceptable.

## Source anchors

- `ksp_plugin_adapter.cs`: vessel loop ~1311–1327; `UnmanageabilityReasons`
  ~620–660; one-time seed 1396/1432; `UpdateVessel` ~516–525; on-rails ~1772;
  warp catch-up ~1700–1768.
- `plugin.cpp`: `InsertOrKeepVessel` ~573–604; free/zombie ~688–704.
- `vessel.cpp`: `CreateTrajectoryIfNeeded` ~232–256. `pile_up.cpp`:
  `DeformPileUpIfNeeded` ~445–578, `NudgeParts` ~404.
- FAQ + issues #1420 (HyperEdit no-effect, wontfix), #1659 (read-only
  `FlowBodyCentric` musing), #2457 (zombies); Interface wiki (read-only, removed);
  `LICENSE.txt` (MIT); `Setup.md`; `CONTRIBUTING.md`.

## Related

- [feasibility](feasibility.md) — gate 0 (Δv map, light floor, relativity, warp-mod survey, two-profile)
