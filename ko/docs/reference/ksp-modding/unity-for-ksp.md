---
title: Unity-for-KSP 패턴 (기둥 ③)
status: draft
created: 2026-06-30
---

# Unity-for-KSP 패턴

KSP 1.12.x 플러그인이 쓰는 Unity(2019.4) API 표면이다 — GameObject, 코루틴,
LineRenderer, 머티리얼/셰이더, IMGUI 윈도, 카메라 투영. 근거화 정책과 범례는
[`README`](README.md) 참조. ScaledSpace + GL 즉시 모드 맵 그리기는
[`ksp-stock-api.md` §3](ksp-stock-api.md)에 근거화되어 있고 여기서는 교차 참조만 한다.

> **스캐폴딩 witness:** kOS `VectorRenderer.cs`는 라벨이 달린 **직선 2점 벡터**(화살표 +
> 화살촉)를 그린다 — 용도는 kOS 스크립트의 디버그 벡터 시각화이지 곡선 호가 *아니다*.
> 플럭스 튜브 / 리드 마커와 공유하는 것은 **저수준 렌더링 스캐폴딩**뿐이다(한 파일에
> GameObject 생성, `AddComponent<LineRenderer>`, `SetParent`, localScale/localPosition,
> 셰이더 try-both 관용구, 최신 LineRenderer 프로퍼티 API). 플럭스 튜브는 그 스캐폴딩을
> 재사용하되 2점 대신 `positionCount = N`으로 곡선 Bézier 점들을 먹인다 — 즉 모양이 아니라
> *기계장치*의 가장 가까운 witness다.

---

## 1. GameObject + AddComponent + Transform (H)

| 패턴 | 인용 |
|---|---|
| `new GameObject(name)` | MechJeb2 `MechJebModuleWaypointWindow.cs:1305`; kOS `VectorRenderer.cs:334` |
| `new GameObject(name, typeof(A), typeof(B), …)` | kOS `VectorRenderer.cs:409` (`RectTransform, Canvas, CanvasScaler`) |
| `gameObject.AddComponent<T>()` | MechJeb2 `…WaypointWindow.cs:1306`; kOS `VectorRenderer.cs:337` |
| 렌더러 컴포넌트를 **맵 카메라에** 붙이기 | `MapView.MapCamera.gameObject.AddComponent<X>()` — MechJeb2 `…WaypointWindow.cs:1294`; TWP `TWP.cs:105` |
| `transform.parent =` / `= null` (월드로 분리) | MechJeb2 `MechJebModuleDebugArrows.cs:276`; TWP `AngleRenderPhase.cs:171` |
| `transform.SetParent(child, false)` | kOS `VectorRenderer.cs:412`; KerbalEngineer `Window.cs:74` |
| `transform.localScale` / `localPosition` | kOS `VectorRenderer.cs:577 / 319` |

> **갭:** 비-제네릭 `AddComponent(typeof(T))`는 **5개 레포 모두에 없다** — 제네릭
> `AddComponent<T>()`를 쓴다. (M / 사용 금지.)
> `SetParent(x,false)` 대 `transform.parent = x`는 레포별 컨벤션이며 둘 다 유효하다.

## 2. 코루틴 (H, 드묾)

- 애니메이션을 구동하는 `StartCoroutine(IEnumerator)` — KerbalEngineer `Window.cs:134`,
  `CanvasGroupFader.cs:83`. Unity가 `IEnumerator Start()`를 자동 실행 — MechJeb2
  `MechjebBundlesManager.cs:25`.
- `IEnumerator` 본문 + `yield return null`(프레임마다) — KerbalEngineer `Window.cs:140,159`.
- `yield return new WaitForEndOfFrame()` — KerbalEngineer `CanvasGroupFader.cs:92`.

> **갭:** `yield return new WaitForSeconds(…)`와 `WaitForFixedUpdate()`는 5개 레포에서
> **확인되지 않았다**. 표준 Unity API이니, 쓸 경우 Unity ScriptReference를 M으로 인용하거나
> witness 레포를 추가한다.

## 3. LineRenderer (H)

최신 프로퍼티 API(이쪽을 쓴다. 구식 `SetVertexCount`/`SetWidth`/`SetColors`는 죽은/주석
처리된 블록에만 나온다).
```csharp
var line = obj.AddComponent<LineRenderer>();
line.useWorldSpace = …;          // false = follow parent transform; true = world coords
line.material = mat;
line.positionCount = N;          // resize anytime
line.startWidth = line.endWidth = w;
line.startColor = line.endColor = c;
line.SetPosition(i, pt);
```
witness: kOS `VectorRenderer.cs:337,340,356,469-478`; MechJeb2
`MechJebModuleWaypointWindow.cs:1305-1311` (공유 static 머티리얼, `positionCount=N`
리사이즈 :1422,:1457).

**ScaledSpace LineRenderer 템플릿(플럭스 튜브 / 리드 호에 가장 직접 적용 가능)**
— TWP `AngleRenderPhase.cs:162-179`: `gameObject.layer = 9`(scaled-atmosphere) 또는
`10`(scaled-space)으로 설정하고, `useWorldSpace = true`로 두고, `SetPosition(i,
ScaledSpace.LocalToScaledSpace(arcPoint))`(:429)을 넣고, 폭을 카메라 거리로 스케일한다 —
`startWidth = 10f/1000f * cam.Distance` (:432) — 화면상 두께를 일정하게 유지하기 위함이다.
거기 머티리얼은 `Shader.Find`가 아니라 **`MapView.orbitLinesMaterial`**(:132)이다.

## 4. 머티리얼 + `Shader.Find` (H)

| 셰이더 문자열 | 인용 |
|---|---|
| `"Legacy Shaders/Particles/Additive"` | MechJeb2 `GLUtils.cs:12`, `…WaypointWindow.cs:1277`; KerbalEngineer `DebugDrawing.cs:15` |
| `"Particles/Alpha Blended"` → 폴백 `"Legacy Shaders/Particles/Alpha Blended"` | kOS `VectorRenderer.cs:352-356` |
| `"Hidden/Internal-Colored"` (GL colored) | KSPCommunityFixes `ReRootPreserveSurfaceAttach.cs:86` |

**관용구 — try-both** (kOS `VectorRenderer.cs:352-356`): 맨 `"Particles/…"` 이름을 먼저
시도하고, null이면 `"Legacy Shaders/Particles/…"`로 폴백한다(Unity 2019/KSP 1.8+에서 이들이
*Legacy Shaders/* 아래로 이동했다). 1.12.x에서는 `Legacy Shaders/` 접두가 바로 먹히지만,
try-both가 확인된 가장 안전한 형태다. 대안: `MapView.orbitLinesMaterial`을 재사용한다.

## 5. IMGUI 윈도 (H)

`void OnGUI()`(MonoBehaviour 콜백) → `GUILayout.Window(id, rect, drawFunc, title)`,
그리기 함수의 끝은 `GUI.DragWindow()`로 마무리한다.

| 요소 | 인용 |
|---|---|
| `OnGUI()` + `GUI.skin = HighLogic.Skin` | KerbalEngineer `BuildAdvanced.cs:187`; kOS `GUIWindow.cs:96` |
| `GUILayout.Window(id, rect, func, title[,style][,opts])` (`id = GetInstanceID()`) | KerbalEngineer `BuildAdvanced.cs:199`; MechJeb2 `DisplayModule.cs:159` |
| `GUI.DragWindow()` / `GUI.DragWindow(Rect)` | KerbalEngineer `BuildAdvanced.cs:557`; TriggerAu `MonoBehaviourWindow.cs:184` |
| 컨트롤: `BeginHorizontal/Vertical`, `Toggle`, `Button`, `Label`, `GUILayout.Width/ExpandWidth(false)` | MechJeb2 `MechJebModuleMenu.cs:161-294`; KerbalEngineer `BuildAdvanced.cs:264` |

평범한 `OnGUI()` 콜백을 쓴다 — 구식 `RenderingManager.AddToPostDrawQueue`는 죽었다
(TWP에서 주석 처리됨). `GameEvents.onGUIApplicationLauncherReady`는 윈도 그리기가 아니라
툴바 버튼용이다.

## 6. 카메라 투영 + 레이어 (H)

**월드 위치의 라벨 / 마커(정확히 NearStars 패턴)** — WaypointManager
`WaypointFlightRenderer.cs:280`: `ScaledSpace.LocalToScaledSpace(localPos)` →
`PlanetariumCamera.Camera.WorldToScreenPoint(scaledPos)` → `Screen.height`로 Y-flip
(:282); 카메라 뒤쪽 컬링은 `Vector3d.Dot(cam.transform.forward, p.normalized) < 0`
(:274); 컴포넌트는 `MapView.MapCamera.gameObject`에 산다 (:36).

| 필요 | 접근자 | 인용 |
|---|---|---|
| 맵 카메라 | `PlanetariumCamera.Camera` | MechJeb2 `GLUtils.cs:92` |
| 비행 카메라 | `FlightCamera.fetch.mainCamera` | MechJeb2 `GLUtils.cs:97`; KSPTrajectories `FlightOverlay.cs:46` |
| 에디터 카메라 | `EditorLogic.fetch.editorCamera` | kOS `Utils.cs:13` |
| 씬별 선택(셋 다) | `MapView.MapIsEnabled`로 분기 | kOS `Utils.cs:13` |

**KSP 레이어 번호** (Kopernicus `GameLayers.cs:34-37`, H): `SCALED_SPACE_ATMOSPHERE =
9`, `SCALED_SPACE = 10`, `LOCAL_SPACE = 15`. → scaled-space 플럭스 튜브/리드 오브젝트는
**레이어 10**에 둔다.

> **갭:** `Camera.main` / `ScaledCamera.Instance`는 **확인되지 않았다** — 위 접근자를
> 쓴다. KSP 레이어 번호를 깔끔하게 나열한 위키는 없다. 레이어 10은 위키가 아니라
> Kopernicus 소스로 근거화한 것이다. Unity 레이어를 Deferred의 *스텐실* 값과 **혼동하지
> 말 것**(별개 시스템이다).

---

## Provenance
2026-06-30에 확인했다(클론 + raw-fetch + read). 핀: MechJeb2 `4c38069`, kOS
`8f281a4`, KerbalEngineer `54b8b73`, TransferWindowPlanner `7465e99`, KSPTrajectories
`master`, KSPCommunityFixes `676e049`, Kopernicus `master`, WaypointManager `master`.

## Related
- [`README`](README.md) — KB 인덱스 + 근거화 정책
- [`ksp-stock-api.md`](ksp-stock-api.md) — §3 ScaledSpace + GL 즉시 모드(여기서 재유도하지 않음)
- [`plugin-scaffolding.md`](plugin-scaffolding.md) — 이 코드의 KSPAddon/MonoBehaviour 호스트
- [`../../../plugins/NearStarsFluxTube/`](../../../../plugins/NearStarsFluxTube/) — 이 코드가 가장 직접 봉사하는 LineRenderer 호
