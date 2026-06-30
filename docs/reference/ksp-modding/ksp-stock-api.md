---
title: KSP stock C# API reference (planner-first slice)
status: draft
created: 2026-06-30
---

# KSP stock C# API reference

**What this is.** A *grounded* reference for the stock KSP 1.12.x C# API surface the
NearStars plugins touch (transfer planner, relativity, warp, flux-tube). It exists
because stock-API knowledge was previously ungrounded training memory — and that
memory was wrong at least once (`ScaledSpace.Factor` → it is actually
**`ScaleFactor`**, §3). This DB replaces assertion with citation.

**Grounding policy (read this).** KSP is **closed-source** — there is no public KSP
source repo to cite by `file:line` the way the mod skills cite Kopernicus/Firefly.
So every entry here is **witnessed by an open-source mod that calls the stock API**:
a mod compiling a call to `FlightGlobals.fetch.SetVesselTarget(...)` is proof that
that member exists with that shape. Citations are `repo path:line` (+ permalink),
verified by fetching the raw file (not search snippets). The gold-standard —
decompiling `Assembly-CSharp.dll` (ILSpy/dnSpy) — is **deferred** (no KSP install on
this dev machine; see [[project_ksp_stock_api_grounding]]).

- **Confidence:** **H** = direct open-source code witness · **M** = decompiled-XML doc
  mirror (anatid.github.io / kerbalspaceprogram.com/ksp/api) or indirect · **L** =
  not witnessed / inferred.
- **License:** only *interop facts* (signatures the open ecosystem uses publicly) are
  recorded here — no decompiled KSP source body, no DLL, is committed. Those stay
  local/gitignored if ever obtained.
- **Branch note:** permalinks are branch-tip (MechJeb `dev`, kOS `develop`,
  Kopernicus/Scatterer/Principia `master`) verified 2026-06-30; line numbers may
  drift — pin to a commit SHA if you need immutable links.

---

## 1. Targeting & body enumeration

| Symbol | Witnessed signature / usage | Witness | Conf |
|--------|----------------------------|---------|:---:|
| `FlightGlobals.fetch` | static singleton accessor | Kerbalism `GotoVessel.cs:24` | H |
| `FlightGlobals.ActiveVessel` | static → `Vessel` | Kerbalism `GotoVessel.cs:24` | H |
| `FlightGlobals.Bodies` | `List<CelestialBody>` — `.Find(b=>b.bodyName==…)`, `[i]`, `foreach` | MechJeb2 `MechJebModuleLandingGuidance.cs:273,294`; Telemachus `NavigationHandlers.cs` (index) | H |
| `FlightGlobals.fetch.SetVesselTarget(…)` | `void SetVesselTarget(ITargetable)` + overload `(ITargetable, bool overrideInputLock)` | kOS `VesselUtils.cs:166,171`; Principia `main_window.cs:44,51` | H |
| `FlightGlobals.fetch.VesselTarget` | `ITargetable` (active vessel's target) | kOS `MissionSettings.cs`; Firespitter `FScameraToTV.cs` | H |
| `Vessel.targetObject` | r/w `ITargetable` (per-vessel target) | MechJeb2 `MechJebModuleTargetController.cs`; RemoteTech `RoverFragment.cs` | H |
| clear target | `SetVesselTarget(null)` | kOS `VesselUtils.cs:171`; Principia `main_window.cs:303,322` | H |

### `ITargetable`
- **Stock implementers:** `CelestialBody`, `Vessel` (both H — Principia passes
  `map_object.celestialBody` and `map_object.vessel` into the `SetVesselTarget(ITargetable)`
  slot, `main_window.cs:44,51`); `ModuleDockingNode`, `PositionTarget` (M — API doc mirror).
- **Members (witnessed in calls):** `Vessel GetVessel()` (kOS `VesselUtils.cs:147`),
  `Orbit GetOrbit()` (KSP-IE `VesselExtension.cs`), `Transform GetTransform()` /
  `string GetName()` / `OrbitDriver GetOrbitDriver()` / `Vector3 GetFwdVector()`
  (krpc `TargetableExtensions.cs`; doc mirror for the full set, M).

**For the planner:** selecting a target body = `FlightGlobals.fetch.SetVesselTarget(body)`
where `body` is a `CelestialBody` (an `ITargetable`). Resolve the body via
`FlightGlobals.Bodies.Find(b => b.bodyName == name)`.

---

## 2. Map-view camera & focus

| Symbol | Witnessed signature / usage | Witness | Conf |
|--------|----------------------------|---------|:---:|
| `PlanetariumCamera.fetch` | static singleton | Principia `main_window.cs:47,55` | H |
| `PlanetariumCamera.fetch.SetTarget(…)` | `SetTarget(MapObject)` / `(string)` / `(int)` | Principia `main_window.cs:47,55`; RemoteTech `FocusFragment.cs` | H |
| `PlanetariumCamera.fetch.targets` | `List<MapObject>` — `.Find(…)`, `.Clear()`, `.AddRange(…)`, `AddTarget(…)` | Astrogator `KerbalTools.cs:162`; Sigma-Binary `KerbinFixer.cs`; RemoteTech | H |
| `MapObject` | `.celestialBody`, `.vessel`, `.maneuverNode`, `.name` | Principia; Astrogator; krpc `Camera.cs` | H |
| `MapView.MapIsEnabled` | static `bool` | MechJeb2 `MechJebModuleTargetController.cs`; kOS `BindingsUniverse.cs` | H |
| `MapView.MapCamera` | the map camera (has `.SetTarget`) | Astrogator `KerbalTools.cs:161` | H |

**Killer witness — select + focus a body in map view** (exactly the planner's target
step), Principia `main_window.cs:44–47`:
```csharp
FlightGlobals.fetch.SetVesselTarget(map_object.celestialBody);   // select
PlanetariumCamera.fetch.SetTarget(map_object);                   // focus camera
```
Astrogator `KerbalTools.cs:159–162` (`FocusMap(ITargetable center, …)`) does the same
via `MapView.MapCamera.SetTarget(...)` + `PlanetariumCamera.fetch.targets.Find(mapObj =>
mapObj.celestialBody != null && mapObj.celestialBody.Equals(center))`.

---

## 3. Map-view custom rendering (lead-marker + heading line)

> **Correction (grounded):** the stock member is **`ScaledSpace.ScaleFactor`**, not
> `ScaledSpace.Factor`. `Factor` does not compile. Witnessed in Kopernicus + Scatterer
> source and the API doc.

| Symbol | Witnessed signature / usage | Witness | Conf |
|--------|----------------------------|---------|:---:|
| `ScaledSpace.ScaleFactor` | `static float` (× to size things in scaled space); also `InverseScaleFactor`, `SceneTransform` | Kopernicus `KopernicusStar.cs` (~L527); Scatterer `SkyNode.cs`; API doc | H |
| `ScaledSpace.LocalToScaledSpace(Vector3d)` | `→ Vector3d` (world → scaled) | MechJeb2 `GLUtils.cs:56–57`; Kopernicus `KopernicusStar.cs` | H |
| `ScaledSpace.ScaledToLocalSpace(Vector3d)` | `→ Vector3d` (scaled → world) | MechJeb2 `GLUtils.cs:34,67` | H |
| `PlanetariumCamera.Camera` | the map-view `Camera` (project world pts) | MechJeb2 `GLUtils.cs:34,47,56,67` | H |
| ScaledScenery layer | `gameObject.layer = 10` (// Layer 10 is ScaledScenery) | ScaledDecorator `AssetLoader.cs` (~L100–109, GPL-3.0) | H |

**How mods actually draw map-view lines/markers — GL immediate mode (primary, witnessed).**
MechJeb does **not** use a `LineRenderer` GameObject; it draws each frame in GL
immediate mode, projecting world points through `PlanetariumCamera.Camera`. Methods in
MechJeb2 `GLUtils.cs`:
- `DrawMapViewGroundMarker(CelestialBody, double lat, double lon, Color, …)` — **L12**
- `DrawGroundMarker(CelestialBody, double lat, double lon, Color, bool map, …)` — **L15**
- `DrawPath(CelestialBody, List<Vector3d> points, Color, bool map, bool dashed=false)` — **L79** (`GL.Begin(GL.LINES)`)
- `DrawOrbit(…)` — **L154**; primitive: `GL.PushMatrix(); _material.SetPass(0); GL.LoadOrtho(); GL.Begin(...); GL.Color(c); GL.Vertex3(...); GL.End()`

A `LineRenderer`-on-map-layer approach is **not witnessed** in fetched source (L) — the
grounded path is GL immediate mode (or a GameObject on layer 10 for *models*, per
ScaledDecorator).

---

## 4. Orbit / body position data

All H (direct witnesses) unless noted.

| Symbol | Witnessed signature / usage | Witness |
|--------|----------------------------|---------|
| `Orbit.getPositionAtUT(double)` | `→ Vector3d` (absolute) | kOS `VesselTarget.cs:~129`, `OrbitInfo.cs:~107` |
| `Orbit.getRelativePositionAtUT(double)` | `→ Vector3d` (body-centered) | MechJeb2 `OrbitExtensions.cs:26` |
| `Orbit.getOrbitalVelocityAtUT(double)` | `→ Vector3d` | MechJeb2 `OrbitExtensions.cs:16`; kOS |
| `Orbit.pos` / `.vel` / `.referenceBody` | `Vector3d` / `Vector3d` / `CelestialBody` | kOS `OrbitInfo.cs:~60,127`; MechJeb2 `OrbitExtensions.cs:33` |
| `CelestialBody.position` | `Vector3d` (world) | kOS `BodyTarget.cs:~161`; MechJeb2 |
| `CelestialBody.orbit` | `Orbit` (**null for root body / Sun** — null-check) | kOS `BodyTarget.cs:~23` |
| `CelestialBody.getPositionAtUT(double)` | `→ Vector3d` (directly on the body) | kOS `VesselTarget.cs:~135`, `BodyTarget.cs:~168` |
| `CelestialBody.GetWorldSurfacePosition(lat, lon, alt)` | `→ Vector3d` | kOS `GeoCoordinates.cs:~246,267` |
| `Planetarium.GetUniversalTime()` | `static → double` (current UT) | kOS `kOSProcessor.cs:~1247` |

*(kOS line numbers from markdown-conversion fetches are ±a few lines; the quoted call
text is exact/greppable. MechJeb `OrbitExtensions.cs` L16/26/33 are exact.)*

---

## 5. Grounded recipe — the lead-marker / planner overlay

Synthesized from the witnesses above (all the *drawing* primitives are H; only the
interstellar-scale *correctness* is unresolved, §6):

1. **Star position at arrival** — `CelestialBody.getPositionAtUT(UT)` (or
   `body.orbit.getPositionAtUT(UT)`; binary term via the orbit), with
   `Planetarium.GetUniversalTime()` as the clock. The lead point is the planner's
   computed `target` (not a real body).
2. **Select / focus** (in-system, normal scale) — `SetVesselTarget(body)` +
   `PlanetariumCamera.fetch.SetTarget(mapObject)` (Principia pattern, §2).
3. **Draw the lead marker + heading line** — GL immediate mode each frame: project
   `ScaledSpace.LocalToScaledSpace(worldPoint)` through `PlanetariumCamera.Camera`
   (MechJeb `GLUtils` pattern), sizing by `ScaledSpace.ScaleFactor`. For a persistent
   model, parent a GameObject on **layer 10 (ScaledScenery)**.

This resolves the `// VERIFY:` ScaledSpace touchpoints in the draft plugins
(`FluxTubeRenderer.cs`, and any planner overlay) — **use `ScaleFactor`, not `Factor`**.

---

## 6. UNRESOLVED — interstellar-scale map view (DLL / in-game test needed)

**Public mod source cannot answer these.** No open-source mod selects or renders a body
at light-year scale; every witness above runs at Kerbin/Sol scale. The blockers live in
the closed DLL / runtime, not in any source:

1. **Selection** — can stock map view frame a target a light-year out? Multi-star packs
   (Sigma-Binary, Galactic-Neighborhood) only *curate the `targets` list* (`Clear()` +
   `AddRange()`), which **hints stock map view does not gracefully handle off-scale
   bodies** — not proof it works.
2. **Rendering precision** — `Vector3d`→`Vector3` precision loss at ~10¹⁶ m;
   `PlanetariumCamera` far-clip culling; whether map zoom even ranges to interstellar.

→ **Empirical TODO:** place a body at LY-scale `ScaledSpace` distance and observe map
view, or inspect the stock DLL. **Do not assume it works.** This is *why* the planner's
likely target-selection UX is a **custom system picker** (not map-view clicking) — see
planner-spec §5.

---

## Provenance

Verified 2026-06-30 by fetching raw files. Key permalinks:
- Principia `main_window.cs` — https://github.com/mockingbirdnest/Principia/blob/master/ksp_plugin_adapter/main_window.cs#L44
- kOS `VesselUtils.cs` — https://github.com/KSP-KOS/KOS/blob/develop/src/kOS/Utilities/VesselUtils.cs#L166
- Astrogator `KerbalTools.cs` — https://github.com/HebaruSan/Astrogator/blob/master/Source/KerbalTools.cs#L159
- MechJeb2 `GLUtils.cs` — https://github.com/MuMech/MechJeb2/blob/dev/MechJeb2/GLUtils.cs#L12
- MechJeb2 `OrbitExtensions.cs` — https://github.com/MuMech/MechJeb2/blob/dev/MechJeb2/OrbitExtensions.cs#L16
- Kerbalism `GotoVessel.cs` — https://github.com/Kerbalism/Kerbalism/blob/master/src/Kerbalism/Utility/GotoVessel.cs#L24
- API doc mirror (ScaledSpace) — https://anatid.github.io/XML-Documentation-for-the-KSP-API/class_scaled_space.html

Gold-standard grounding (DLL decompile, KSP 1.12.x `Assembly-CSharp.dll`) is deferred;
when available it supersedes the M-confidence doc-mirror rows. See
[[project_ksp_stock_api_grounding]].

## Related

- [`gameplay/interstellar-expansion/planner-spec.md`](../../../gameplay/interstellar-expansion/planner-spec.md) — §5 in-game UI surface this grounds (target selection)
- [`plugins/NearStarsRelativity/`](../../../plugins/NearStarsRelativity/), [`plugins/NearStarsWarp/`](../../../plugins/NearStarsWarp/), [`plugins/NearStarsFluxTube/`](../../../plugins/NearStarsFluxTube/) — the `// VERIFY:` markers this resolves
- [principia-cfg-reference](../principia-cfg-reference.md) — the open-source (MIT) cousin, cited by `file:line` directly
