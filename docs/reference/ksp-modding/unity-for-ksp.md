---
title: Unity-for-KSP patterns (pillar ③)
status: draft
created: 2026-06-30
---

# Unity-for-KSP patterns

The Unity (2019.4) API surface KSP 1.12.x plugins use — GameObjects, coroutines,
LineRenderer, materials/shaders, IMGUI windows, camera projection. Grounding policy +
legend: [`README`](README.md). ScaledSpace + GL immediate-mode map drawing are
grounded in [`ksp-stock-api.md` §3](ksp-stock-api.md) and only cross-referenced here.

> **Scaffolding witness:** kOS `VectorRenderer.cs` draws a **straight 2-point vector**
> (arrow + arrowhead) with a label — its purpose is debug-vector visualization for kOS
> scripts, *not* a curved arc. What it shares with the flux-tube / lead-marker is only
> the **low-level rendering scaffolding** in one file: GameObject creation,
> `AddComponent<LineRenderer>`, `SetParent`, localScale/localPosition, the shader
> try-both idiom, and the modern LineRenderer property API. The flux-tube reuses that
> scaffolding but feeds `positionCount = N` curved Bézier points instead of 2 — so this
> is the closest witnessed analog for the *mechanics*, not the shape.
>
> *Footnote (to avoid a known confusion):* this file is kOS's **`VECDRAW`** feature
> (`[KOSNomenclature("Vecdraw")]`; GameObjects `vecdrawLine`/`vecdrawHat`), an **in-world
> 3D vector overlay** drawn via `ScaledSpace.LocalToScaledSpace` with an `isOnMap` branch
> — **not** the kOS text terminal/GUI. It is exactly that in-world `LineRenderer` +
> `ScaledSpace` path (verified by raw-fetching the file) that makes it a valid
> scaffolding witness; the grounding does not otherwise depend on kOS.

---

## 1. GameObject + AddComponent + Transform (H)

| Pattern | citation |
|---|---|
| `new GameObject(name)` | MechJeb2 `MechJebModuleWaypointWindow.cs:1305`; kOS `VectorRenderer.cs:334` |
| `new GameObject(name, typeof(A), typeof(B), …)` | kOS `VectorRenderer.cs:409` (`RectTransform, Canvas, CanvasScaler`) |
| `gameObject.AddComponent<T>()` | MechJeb2 `…WaypointWindow.cs:1306`; kOS `VectorRenderer.cs:337` |
| attach a renderer component **to the map camera** | `MapView.MapCamera.gameObject.AddComponent<X>()` — MechJeb2 `…WaypointWindow.cs:1294`; TWP `TWP.cs:105` |
| `transform.parent =` / `= null` (detach to world) | MechJeb2 `MechJebModuleDebugArrows.cs:276`; TWP `AngleRenderPhase.cs:171` |
| `transform.SetParent(child, false)` | kOS `VectorRenderer.cs:412`; KerbalEngineer `Window.cs:74` |
| `transform.localScale` / `localPosition` | kOS `VectorRenderer.cs:577 / 319` |

> **Gap:** non-generic `AddComponent(typeof(T))` **absent in all 5 repos** — use the
> generic `AddComponent<T>()`. (M / do-not-use.)
> `SetParent(x,false)` vs `transform.parent = x` is per-repo convention; both valid.

## 2. Coroutines (H, sparse)

- `StartCoroutine(IEnumerator)` driving an animation — KerbalEngineer `Window.cs:134`,
  `CanvasGroupFader.cs:83`. Unity auto-runs `IEnumerator Start()` — MechJeb2
  `MechjebBundlesManager.cs:25`.
- `IEnumerator` body + `yield return null` (per-frame) — KerbalEngineer `Window.cs:140,159`.
- `yield return new WaitForEndOfFrame()` — KerbalEngineer `CanvasGroupFader.cs:92`.

> **Gap:** `yield return new WaitForSeconds(…)` and `WaitForFixedUpdate()` **not
> witnessed** in the 5 repos. Standard Unity APIs — cite Unity ScriptReference as M if
> used, or add a witness repo.

## 3. LineRenderer (H)

Modern property API (use this; the old `SetVertexCount`/`SetWidth`/`SetColors` appears
only in dead/commented blocks):
```csharp
var line = obj.AddComponent<LineRenderer>();
line.useWorldSpace = …;          // false = follow parent transform; true = world coords
line.material = mat;
line.positionCount = N;          // resize anytime
line.startWidth = line.endWidth = w;
line.startColor = line.endColor = c;
line.SetPosition(i, pt);
```
Witnesses: kOS `VectorRenderer.cs:337,340,356,469-478`; MechJeb2
`MechJebModuleWaypointWindow.cs:1305-1311` (shared static material, `positionCount=N`
resize at :1422,:1457).

**ScaledSpace LineRenderer template (most directly applicable to a flux-tube / lead arc)**
— TWP `AngleRenderPhase.cs:162-179`: set `gameObject.layer = 9` (scaled-atmosphere) or
`10` (scaled-space), `useWorldSpace = true`, feed `SetPosition(i,
ScaledSpace.LocalToScaledSpace(arcPoint))` (:429), and scale width by camera distance —
`startWidth = 10f/1000f * cam.Distance` (:432) — to keep constant on-screen thickness.
Material there is **`MapView.orbitLinesMaterial`** (:132) instead of `Shader.Find`.

## 4. Material + `Shader.Find` (H)

| Shader string | citation |
|---|---|
| `"Legacy Shaders/Particles/Additive"` | MechJeb2 `GLUtils.cs:12`, `…WaypointWindow.cs:1277`; KerbalEngineer `DebugDrawing.cs:15` |
| `"Particles/Alpha Blended"` → fallback `"Legacy Shaders/Particles/Alpha Blended"` | kOS `VectorRenderer.cs:352-356` |
| `"Hidden/Internal-Colored"` (GL colored) | KSPCommunityFixes `ReRootPreserveSurfaceAttach.cs:86` |

**Idiom — try-both** (kOS `VectorRenderer.cs:352-356`): try the bare `"Particles/…"`
name, fall back to `"Legacy Shaders/Particles/…"` if null (Unity 2019/KSP 1.8+ moved
these under *Legacy Shaders/*). For 1.12.x the `Legacy Shaders/` prefix works directly;
the try-both is the safest witnessed form. Alternative: reuse `MapView.orbitLinesMaterial`.

## 5. IMGUI windows (H)

`void OnGUI()` (MonoBehaviour callback) → `GUILayout.Window(id, rect, drawFunc, title)`,
ending the draw func with `GUI.DragWindow()`:

| Element | citation |
|---|---|
| `OnGUI()` + `GUI.skin = HighLogic.Skin` | KerbalEngineer `BuildAdvanced.cs:187`; kOS `GUIWindow.cs:96` |
| `GUILayout.Window(id, rect, func, title[,style][,opts])` (`id = GetInstanceID()`) | KerbalEngineer `BuildAdvanced.cs:199`; MechJeb2 `DisplayModule.cs:159` |
| `GUI.DragWindow()` / `GUI.DragWindow(Rect)` | KerbalEngineer `BuildAdvanced.cs:557`; TriggerAu `MonoBehaviourWindow.cs:184` |
| controls: `BeginHorizontal/Vertical`, `Toggle`, `Button`, `Label`, `GUILayout.Width/ExpandWidth(false)` | MechJeb2 `MechJebModuleMenu.cs:161-294`; KerbalEngineer `BuildAdvanced.cs:264` |

Use the plain `OnGUI()` callback — the old `RenderingManager.AddToPostDrawQueue` is dead
(commented out in TWP). `GameEvents.onGUIApplicationLauncherReady` is for the toolbar
button, not window drawing.

## 6. Camera projection + layers (H)

**Label / marker at a world position (the exact NearStars pattern)** — WaypointManager
`WaypointFlightRenderer.cs:280`: `ScaledSpace.LocalToScaledSpace(localPos)` →
`PlanetariumCamera.Camera.WorldToScreenPoint(scaledPos)` → Y-flip with `Screen.height`
(:282); behind-camera cull via `Vector3d.Dot(cam.transform.forward, p.normalized) < 0`
(:274); component lives on `MapView.MapCamera.gameObject` (:36).

| Need | accessor | citation |
|---|---|---|
| map camera | `PlanetariumCamera.Camera` | MechJeb2 `GLUtils.cs:92` |
| flight camera | `FlightCamera.fetch.mainCamera` | MechJeb2 `GLUtils.cs:97`; KSPTrajectories `FlightOverlay.cs:46` |
| editor camera | `EditorLogic.fetch.editorCamera` | kOS `Utils.cs:13` |
| scene-dependent pick (all three) | branch on `MapView.MapIsEnabled` | kOS `Utils.cs:13` |

**KSP layer numbers** (Kopernicus `GameLayers.cs:34-37`, H): `SCALED_SPACE_ATMOSPHERE =
9`, `SCALED_SPACE = 10`, `LOCAL_SPACE = 15`. → a scaled-space flux-tube/lead object goes
on **layer 10**.

> **Gaps:** `Camera.main` / `ScaledCamera.Instance` **not witnessed** — use the
> accessors above. No wiki cleanly lists KSP layer numbers; layer 10 is grounded from
> Kopernicus source, not wiki. Do **not** confuse Unity layers with Deferred's *stencil*
> values (different system).

---

## Provenance
Verified 2026-06-30 (clone + raw-fetch + read). Pinned: MechJeb2 `4c38069`, kOS
`8f281a4`, KerbalEngineer `54b8b73`, TransferWindowPlanner `7465e99`, KSPTrajectories
`master`, KSPCommunityFixes `676e049`, Kopernicus `master`, WaypointManager `master`.

## Related
- [`README`](README.md) — KB index + grounding policy
- [`ksp-stock-api.md`](ksp-stock-api.md) — §3 ScaledSpace + GL immediate-mode (not re-derived here)
- [`plugin-scaffolding.md`](plugin-scaffolding.md) — the KSPAddon/MonoBehaviour host for this code
- [`../../../plugins/NearStarsFluxTube/`](../../../plugins/NearStarsFluxTube/) — the LineRenderer arc this most directly serves
