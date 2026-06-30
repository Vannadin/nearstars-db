---
title: Warp-under-Principia — minimal-fork patch draft + cruise plugin
status: draft
created: 2026-06-30
---

# Warp under Principia — minimal-fork patch draft

**Stage: draft — not compiled or tested.** Concretizes the *minimal-fork* path
chosen in [`warp-and-navigation-brainstorm.md`](warp-and-navigation-brainstorm.md)
§3 (the `UnmanageabilityReasons` flag) into (a) an actual patch sketch against
Principia's source and (b) a cruise-layer plugin skeleton
([`plugins/NearStarsWarp/`](../../../plugins/NearStarsWarp/)). Source-grounded
claims carry the brainstorm's `[src]` anchors; line numbers are from
`mockingbirdnest/Principia` @ master and **must be re-confirmed before any fork**
(Principia rebases monthly). In-game C#/C++ is Schultz's lane
([[project-nearstars-mod-plugins-schultz]], [[project-principia-custom-branch]]);
this is the brief, not shipping code.

---

## 0. The one decision this draft commits to

The brainstorm left three open items (§6 frame, §8 verify, flight-plan loss).
This draft fixes defaults so there is something concrete to verify:

| Decision | Default chosen here | Why | Reversible? |
|----------|--------------------|-----|-------------|
| Detach mechanism | **Minimal fork** — one `UnmanageabilityReasons` exclusion | sweet spot: cruise works, lives in a stable filter (light rebase) | yes — swap the interop layer |
| Flight plan on warp | **Lost, replan at destination** | the C++ trajectory is destroyed on detach; preserving it = big fork | yes — big fork later |
| Velocity frame across the gap | **(a) barycentric preserve** | project ethos (realistic); arrival relative velocity is a real challenge | yes — one constant in `WarpCruise` |
| Energy / fuel | **Gameplay-tuned ExoticMatter** (see `warp_exotic_matter.py`) | the metric energy is 10⁶⁰× absurd; gameplay model is the only shippable one | yes — tuner cfg |

All four are tunable / swappable; none is load-bearing for the *architecture*.

---

## 1. The patch — Principia side (C++/C# fork)

### 1.1 What we add

Exactly **one** per-vessel exclusion in the detach gate. When a vessel raises the
NearStars warp flag, Principia stops managing it for the duration of the cruise;
on dropout the flag clears and Principia re-adopts the vessel from its (new) stock
orbit via the existing first-insertion seed path.

**Anchor [src]:** `ksp_plugin_adapter.cs`, `UnmanageabilityReasons(Vessel)`
(~620–660). It already excludes non-`ORBITING`/`FLYING`/`SUB_ORBITAL`/`ESCAPING`,
`DEAD`, `position == 0`, and hack-gravity vessels — but has **no `VesselType`
check and no extension point.** We add one OR-term.

### 1.2 Diff sketch (illustrative — confirm signature + line at fork time)

```csharp
// ksp_plugin_adapter.cs — inside UnmanageabilityReasons(Vessel vessel)
// (existing checks build up a `reasons` string/flags; we add one term)

+   // --- NearStars warp hook -------------------------------------------------
+   // A vessel actively under NearStars warp must be released by Principia so the
+   // custom cruise layer can move it continuously (see plugins/NearStarsWarp).
+   // The flag is a stock-side channel (KSPField / static map keyed by GUID) that
+   // the warp PartModule sets on engage and clears on dropout. Reading a stock
+   // field here keeps the fork to ONE stable line — no integrator change.
+   if (NearStarsWarpBridge.IsUnderWarp(vessel)) {
+     reasons += (reasons.Empty() ? "" : ", ") + "under NearStars warp";
+   }
+   // -------------------------------------------------------------------------
```

`NearStarsWarpBridge.IsUnderWarp` is a tiny static the fork ships alongside the
adapter (or, to avoid a Principia↔NearStars compile dependency, read a
conventional `KSPField`/`ProtoVessel` value by name — see §3 VERIFY). The key
property: **the fork is one filter line, not an integrator edit** — the brainstorm's
"sweet spot" (§3) — so the monthly-rebase surface is minimal.

### 1.3 Why this is enough  [src]

- The detach gate is the *only* place Principia decides whether a managed vessel
  is governed; excluding the vessel here drops it from the kept-set.
- On dropout we set a stock orbit and clear the flag; the next tick the vessel is
  no longer excluded, so `CreateTrajectoryIfNeeded` (`vessel.cpp` ~232–256) seeds
  a **fresh** C++ trajectory from that stock orbit (the existing first-insertion
  path — guarded by `trajectory_.empty()`). No new re-seed API needed.
- The C++ `Vessel` and its `DiscreteTrajectory` (history + flight plan) are
  destroyed on detach (they live in the freed object). **KSP GUID / parts / crew
  survive.** ⇒ flight-plan loss, accepted in §0.

### 1.4 What we explicitly do NOT do

- **No `VesselSetState` C ABI** (the "big fork" — touches integrator internals,
  heavy rebase). Unnecessary once flight-plan loss is accepted.
- **No suppressing the write-back** (`UpdateVessel` ~516–525). That fights a
  symptom; the vessel would snap back and pile-up/prediction/save-load break.
  Detaching at the *authority* layer (the kept-set) is the correct layer.

---

## 2. The cruise layer — NearStars side (no fork)

Lives **above** Principia's physics scene; Principia only touches the two
endpoints (detach / re-seed), so there is no per-tick fight (brainstorm §4).

```
ENGAGE                    CRUISE (custom propagator)              DROPOUT
──────                    ──────────────────────────              ───────
capture v0 (barycentric)  vessel detached (flag up):              set stock orbit
raise warp flag        →  move continuously & steerably,       →  at destination,
Principia releases it      carrying v0; FTL β_s; other bodies      restore v0,
                           keep their Principia trajectories;      clear flag →
                           time passes normally                    Principia re-seeds
```

State machine (pure logic, `WarpCruise.cs`): `Idle → Spooling → Cruising →
Dropout → Idle`. `Spooling`/`Dropout` are short ramps so velocity and position
are continuous (no teleport pop). The propagator integrates
`position += (v0 + heading·v_s)·dt` each `FixedUpdate` while `Cruising`.

**Velocity continuity (§6 frame = (a) barycentric preserve):** capture `v0` in
the Sol-barycentric inertial frame at engage; carry it unchanged; on dropout the
vessel arrives carrying the real inter-stellar relative velocity (origin star
motion minus destination star motion). This is the realistic, harder arrival —
the navigation planner (`planner_*.py`) already computes that arrival relative
velocity, and the relativity layer's leg-3 braking handles bleeding it off.

---

## 3. Cross-plugin tie — the relativity layer's warp flag

The relativity layer ([`plugins/NearStarsRelativity/`](../../../plugins/NearStarsRelativity/))
§2.6(ii) must treat a warping vessel as identity (warp β is not physical β, or it
reads FTL → NaN). It already exposes `WarpFlag.Provider`. **This plugin fills it**
— `WarpFlagBridge` registers a provider that returns `true` while a vessel is in
the `Cruising`/`Spooling`/`Dropout` states. One shared flag, both Schultz's lane.

---

## 4. Files in the draft plugin

| File | Role | KSP/Principia touch |
|------|------|---------------------|
| `WarpCruise.cs` | **correctness core (pure logic).** Engage/cruise/dropout state machine; v0 capture + carry; FTL step; frame-(a) policy. | none (pure) |
| `WarpDriveModule.cs` | `PartModule` — engage/disengage UI, ExoticMatter check + drain (gameplay model), drives the state machine. | VERIFY (PartModule API, resource drain) |
| `PrincipiaInterop.cs` | detach / re-seed touchpoints: raise the warp flag, set destination stock orbit, clear flag. **REQUIRES the §1 fork.** | VERIFY + REQUIRES FORK |
| `WarpFlagBridge.cs` | registers `WarpFlag.Provider` for the relativity layer (§3). | none |
| `README.md` | status + hand-off TODO. | — |

`PrincipiaInterop` is the file that **cannot work without the §1 fork** — it is
where "raise the flag Principia reads" lives. On the non-Principia profile the
same interop is a no-op (no Principia to detach from; SigmaBinary + stock conics
already let a custom propagator move the vessel), so the cruise core is profile-agnostic.

---

## 5. Verify before hand-off (Schultz / keyboard)

1. **The fork line** — confirm `UnmanageabilityReasons` signature + that adding
   an OR-term cleanly drops the vessel from the kept-set AND that dropout re-seeds
   from the new stock orbit (the §1.3 claim). This is the one load-bearing
   assumption (brainstorm §8). *Design inference from confirmed mechanism — verify.*
2. **Flag channel** — decide stock `KSPField`/GUID-map vs a compile dependency
   (§1.2). Prefer the stock-field channel to keep Principia↔NearStars decoupled.
3. **Re-seed continuity** — confirm the vessel does not pop / lose parts / break
   save-load across detach→cruise→re-adopt.
4. **Velocity units / frame** — confirm `v0` capture is in the same barycentric
   frame Principia re-seeds into.
5. **Non-Principia profile** — confirm the cruise core runs with `PrincipiaInterop`
   as a no-op under SigmaBinary + stock conics.

---

## Source anchors

Same as the brainstorm (re-confirm at fork time):
`ksp_plugin_adapter.cs` `UnmanageabilityReasons` ~620–660, `UpdateVessel`
~516–525, vessel loop ~1311–1327; `plugin.cpp` free/zombie ~688–704;
`vessel.cpp` `CreateTrajectoryIfNeeded` ~232–256; `LICENSE.txt` (MIT — fork OK,
keep notices); issue #1420 (HyperEdit no-effect, wontfix).

## Related

- [warp-and-navigation-brainstorm](warp-and-navigation-brainstorm.md) — §3 options ladder, §4 cruise arch, §6 frame (this draft picks defaults)
- [feasibility](../feasibility.md) — gate 0 (two-profile decision; this is the "warp + Principia together" path)
- `warp_exotic_matter.py` — the ExoticMatter / energy economics the gameplay fuel model uses
- [relativity-mod](../relativity/relativity-mod.md) — §2.6(ii) warp flag this plugin fills
