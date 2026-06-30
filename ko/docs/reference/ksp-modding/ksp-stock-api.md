---
title: KSP 스톡 C# API 레퍼런스 (플래너 우선 슬라이스)
status: draft
created: 2026-06-30
---

# KSP 스톡 C# API 레퍼런스

**이 문서의 정체.** NearStars 플러그인(전이 플래너, 상대론, 워프, 플럭스 튜브)이 건드리는
스톡 KSP 1.12.x C# API 표면에 대한 *근거화된* 레퍼런스다. 이 문서가 존재하는 이유는,
스톡 API 지식이 이전까지 근거 없는 학습 기억에 의존했고 — 그 기억이 최소 한 번은 틀렸기
때문이다(`ScaledSpace.Factor` → 실제로는 **`ScaleFactor`**, §3). 이 DB는 단언을 인용으로
대체한다.

**근거화 정책(반드시 읽을 것).** KSP는 **클로즈드 소스**다 — 모드 스킬이 Kopernicus/Firefly를
`file:line`으로 인용하는 방식대로 인용할 수 있는 공개 KSP 소스 저장소가 없다. 그래서 여기
실린 모든 항목은 **스톡 API를 호출하는 오픈소스 모드로 확인된다**. `FlightGlobals.fetch.SetVesselTarget(...)`
호출을 컴파일하는 모드가 있다는 사실 자체가, 그 멤버가 그 형태로 존재한다는 증거다. 인용은
`repo path:line`(+퍼머링크)이며, 원본 파일을 직접 받아서 확인했다(검색 스니펫이 아니라).
최상의 기준 — `Assembly-CSharp.dll` 디컴파일(ILSpy/dnSpy) — 은 **보류**다(이 개발 머신에 KSP
설치가 없다. [[project_ksp_stock_api_grounding]] 참고).

- **신뢰도:** **H** = 오픈소스 코드로 직접 확인 · **M** = 디컴파일 XML 문서 미러
  (anatid.github.io / kerbalspaceprogram.com/ksp/api) 또는 간접 · **L** = 미확인 / 추론.
- **라이선스:** 여기에는 *상호운용 사실*(오픈 생태계가 공개적으로 사용하는 시그니처)만
  기록한다 — 디컴파일된 KSP 소스 본문이나 DLL은 일절 커밋하지 않는다. 그런 것을 입수하게
  되더라도 로컬/gitignore로만 둔다.
- **브랜치 주의:** 퍼머링크는 브랜치 팁(MechJeb `dev`, kOS `develop`,
  Kopernicus/Scatterer/Principia `master`)이며 2026-06-30에 확인했다. 줄 번호는 밀릴 수
  있으니 불변 링크가 필요하면 커밋 SHA로 핀을 박을 것.

---

## 1. 타깃 지정 & 천체 열거

| Symbol | 확인된 시그니처/용례 | 근거 | Conf |
|--------|----------------------------|---------|:---:|
| `FlightGlobals.fetch` | 정적 싱글턴 접근자 | Kerbalism `GotoVessel.cs:24` | H |
| `FlightGlobals.ActiveVessel` | 정적 → `Vessel` | Kerbalism `GotoVessel.cs:24` | H |
| `FlightGlobals.Bodies` | `List<CelestialBody>` — `.Find(b=>b.bodyName==…)`, `[i]`, `foreach` | MechJeb2 `MechJebModuleLandingGuidance.cs:273,294`; Telemachus `NavigationHandlers.cs` (index) | H |
| `FlightGlobals.fetch.SetVesselTarget(…)` | `void SetVesselTarget(ITargetable)` + 오버로드 `(ITargetable, bool overrideInputLock)` | kOS `VesselUtils.cs:166,171`; Principia `main_window.cs:44,51` | H |
| `FlightGlobals.fetch.VesselTarget` | `ITargetable` (활성 함선의 타깃) | kOS `MissionSettings.cs`; Firespitter `FScameraToTV.cs` | H |
| `Vessel.targetObject` | 읽기/쓰기 `ITargetable` (함선별 타깃) | MechJeb2 `MechJebModuleTargetController.cs`; RemoteTech `RoverFragment.cs` | H |
| 타깃 해제 | `SetVesselTarget(null)` | kOS `VesselUtils.cs:171`; Principia `main_window.cs:303,322` | H |

### `ITargetable`
- **스톡 구현체:** `CelestialBody`, `Vessel` (둘 다 H — Principia가
  `map_object.celestialBody`와 `map_object.vessel`을 `SetVesselTarget(ITargetable)`
  슬롯에 넘긴다, `main_window.cs:44,51`); `ModuleDockingNode`, `PositionTarget` (M — API 문서 미러).
- **멤버(호출에서 확인됨):** `Vessel GetVessel()` (kOS `VesselUtils.cs:147`),
  `Orbit GetOrbit()` (KSP-IE `VesselExtension.cs`), `Transform GetTransform()` /
  `string GetName()` / `OrbitDriver GetOrbitDriver()` / `Vector3 GetFwdVector()`
  (krpc `TargetableExtensions.cs`; 전체 집합은 문서 미러, M).

**플래너 입장에서:** 타깃 천체 선택 = `FlightGlobals.fetch.SetVesselTarget(body)`이며,
여기서 `body`는 `CelestialBody`(즉 `ITargetable`)다. 천체는
`FlightGlobals.Bodies.Find(b => b.bodyName == name)`으로 해석한다.

---

## 2. 맵뷰 카메라 & 포커스

| Symbol | 확인된 시그니처/용례 | 근거 | Conf |
|--------|----------------------------|---------|:---:|
| `PlanetariumCamera.fetch` | 정적 싱글턴 | Principia `main_window.cs:47,55` | H |
| `PlanetariumCamera.fetch.SetTarget(…)` | `SetTarget(MapObject)` / `(string)` / `(int)` | Principia `main_window.cs:47,55`; RemoteTech `FocusFragment.cs` | H |
| `PlanetariumCamera.fetch.targets` | `List<MapObject>` — `.Find(…)`, `.Clear()`, `.AddRange(…)`, `AddTarget(…)` | Astrogator `KerbalTools.cs:162`; Sigma-Binary `KerbinFixer.cs`; RemoteTech | H |
| `MapObject` | `.celestialBody`, `.vessel`, `.maneuverNode`, `.name` | Principia; Astrogator; krpc `Camera.cs` | H |
| `MapView.MapIsEnabled` | 정적 `bool` | MechJeb2 `MechJebModuleTargetController.cs`; kOS `BindingsUniverse.cs` | H |
| `MapView.MapCamera` | 맵 카메라 (`.SetTarget` 보유) | Astrogator `KerbalTools.cs:161` | H |

**근거 — 천체 선택 + 포커스 메커니즘**(플래너의 타깃 단계가 *사용할* 것. 단 플래너의 타깃은
스톡 천체가 아니라 계산된 리드 포인트이고, LY 스케일에서는 §6이 미검증으로 둠),
Principia `main_window.cs:44–47`(듀얼모드 select/focus UI).
```csharp
FlightGlobals.fetch.SetVesselTarget(map_object.celestialBody);   // select
PlanetariumCamera.fetch.SetTarget(map_object);                   // focus camera
```
Astrogator `KerbalTools.cs:159–162` (`FocusMap(ITargetable center, …)`)는
`MapView.MapCamera.SetTarget(...)` + `PlanetariumCamera.fetch.targets.Find(mapObj =>
mapObj.celestialBody != null && mapObj.celestialBody.Equals(center))`로 같은 일을 한다.

---

## 3. 맵뷰 커스텀 렌더링 (리드 마커 + 헤딩 라인)

> **정정(근거화됨):** 스톡 멤버는 **`ScaledSpace.ScaleFactor`**이지
> `ScaledSpace.Factor`가 아니다. `Factor`는 컴파일되지 않는다. Kopernicus + Scatterer
> 소스와 API 문서로 확인했다.

| Symbol | 확인된 시그니처/용례 | 근거 | Conf |
|--------|----------------------------|---------|:---:|
| `ScaledSpace.ScaleFactor` | `static float` (스케일드 스페이스에서 크기를 맞추는 배율); 추가로 `InverseScaleFactor`, `SceneTransform` | Kopernicus `KopernicusStar.cs` (~L527); Scatterer `SkyNode.cs`; API doc | H |
| `ScaledSpace.LocalToScaledSpace(Vector3d)` | `→ Vector3d` (월드 → 스케일드) | MechJeb2 `GLUtils.cs:56–57`; Kopernicus `KopernicusStar.cs` | H |
| `ScaledSpace.ScaledToLocalSpace(Vector3d)` | `→ Vector3d` (스케일드 → 월드) | MechJeb2 `GLUtils.cs:34,67` | H |
| `PlanetariumCamera.Camera` | 맵뷰 `Camera` (월드 점 투영용) | MechJeb2 `GLUtils.cs:34,47,56,67` | H |
| ScaledScenery 레이어 | `gameObject.layer = 10` (// Layer 10 is ScaledScenery) | ScaledDecorator `AssetLoader.cs` (~L100–109, GPL-3.0) | H |

**모드가 실제로 맵뷰 선/마커를 그리는 방법 — GL 즉시 모드(주요 경로, 확인됨).**
MechJeb은 `LineRenderer` 게임오브젝트를 **쓰지 않는다**. 매 프레임 GL 즉시 모드로 그리며,
월드 점을 `PlanetariumCamera.Camera`로 투영한다. MechJeb2 `GLUtils.cs`의 메서드들.
- `DrawMapViewGroundMarker(CelestialBody, double lat, double lon, Color, …)` — **L12**
- `DrawGroundMarker(CelestialBody, double lat, double lon, Color, bool map, …)` — **L15**
- `DrawPath(CelestialBody, List<Vector3d> points, Color, bool map, bool dashed=false)` — **L79** (`GL.Begin(GL.LINES)`)
- `DrawOrbit(…)` — **L154**; 원시 호출: `GL.PushMatrix(); _material.SetPass(0); GL.LoadOrtho(); GL.Begin(...); GL.Color(c); GL.Vertex3(...); GL.End()`

받아온 소스에서 `LineRenderer`를 맵 레이어에 얹는 방식은 **확인되지 않는다**(L) — 근거화된
경로는 GL 즉시 모드다(*모델*의 경우라면 ScaledDecorator처럼 레이어 10의 게임오브젝트).

---

## 4. 궤도 / 천체 위치 데이터

별도 표기가 없으면 전부 H(직접 확인).

| Symbol | 확인된 시그니처/용례 | 근거 |
|--------|----------------------------|---------|
| `Orbit.getPositionAtUT(double)` | `→ Vector3d` (절대) | kOS `VesselTarget.cs:~129`, `OrbitInfo.cs:~107` |
| `Orbit.getRelativePositionAtUT(double)` | `→ Vector3d` (천체 중심 기준) | MechJeb2 `OrbitExtensions.cs:26` |
| `Orbit.getOrbitalVelocityAtUT(double)` | `→ Vector3d` | MechJeb2 `OrbitExtensions.cs:16`; kOS |
| `Orbit.pos` / `.vel` / `.referenceBody` | `Vector3d` / `Vector3d` / `CelestialBody` | kOS `OrbitInfo.cs:~60,127`; MechJeb2 `OrbitExtensions.cs:33` |
| `CelestialBody.position` | `Vector3d` (월드) | kOS `BodyTarget.cs:~161`; MechJeb2 |
| `CelestialBody.orbit` | `Orbit` (**루트 천체 / 태양에서는 null** — null 체크 필요) | kOS `BodyTarget.cs:~23` |
| `CelestialBody.getPositionAtUT(double)` | `→ Vector3d` (천체에서 직접) | kOS `VesselTarget.cs:~135`, `BodyTarget.cs:~168` |
| `CelestialBody.GetWorldSurfacePosition(lat, lon, alt)` | `→ Vector3d` | kOS `GeoCoordinates.cs:~246,267` |
| `Planetarium.GetUniversalTime()` | `static → double` (현재 UT) | kOS `kOSProcessor.cs:~1247` |

*(마크다운 변환으로 받아온 kOS 줄 번호는 ±몇 줄 오차가 있다. 인용한 호출 텍스트는
정확하며 grep 가능하다. MechJeb `OrbitExtensions.cs` L16/26/33은 정확하다.)*

---

## 5. 근거화된 레시피 — 리드 마커 / 플래너 오버레이

위 근거들로부터 합성했다(모든 *그리기* 원시 동작은 H이며, 인터스텔라 스케일에서의 *정확성*만
미해결이다, §6).

1. **도착 시점 항성 위치** — `CelestialBody.getPositionAtUT(UT)` (또는
   `body.orbit.getPositionAtUT(UT)`; 쌍성 항은 궤도를 경유), 시계는
   `Planetarium.GetUniversalTime()`. 리드 점은 플래너가 계산한 `target`이다(실제 천체가
   아니다).
2. **선택 / 포커스**(계 내부, 정상 스케일) — `SetVesselTarget(body)` +
   `PlanetariumCamera.fetch.SetTarget(mapObject)` (Principia 패턴, §2).
3. **리드 마커 + 헤딩 라인 그리기** — 매 프레임 GL 즉시 모드.
   `ScaledSpace.LocalToScaledSpace(worldPoint)`를 `PlanetariumCamera.Camera`로
   투영하고(MechJeb `GLUtils` 패턴), `ScaledSpace.ScaleFactor`로 크기를 맞춘다. 지속되는
   모델이라면 게임오브젝트를 **레이어 10 (ScaledScenery)**에 부모로 붙인다.

이로써 드래프트 플러그인들의 `// VERIFY:` ScaledSpace 접점이 해소된다
(`FluxTubeRenderer.cs`, 그리고 플래너 오버레이류) — **`Factor`가 아니라 `ScaleFactor`를
쓸 것.**

---

## 6. 미해결 — 인터스텔라 스케일 맵뷰 (DLL / 인게임 테스트 필요)

**공개 모드 소스로는 답할 수 없다.** 광년 스케일에서 천체를 선택하거나 렌더링하는 오픈소스
모드는 없다. 위의 모든 근거는 Kerbin/Sol 스케일에서 동작한다. 막힌 부분은 소스가 아니라
클로즈드 DLL / 런타임에 있다.

1. **선택** — 스톡 맵뷰가 1광년 밖 타깃을 프레임에 잡을 수 있는가? 다성계 팩(Sigma-Binary,
   Galactic-Neighborhood)은 *`targets` 리스트를 큐레이션*할 뿐이며(`Clear()` +
   `AddRange()`), 이는 **스톡 맵뷰가 스케일을 벗어난 천체를 우아하게 처리하지 못함을
   시사한다** — 작동한다는 증거는 아니다.
2. **렌더링 정밀도** — ~10¹⁶ m에서 `Vector3d`→`Vector3` 정밀도 손실,
   `PlanetariumCamera` 파-클립 컬링, 맵 줌이 인터스텔라까지 도달하는지 여부.

→ **경험적 TODO:** 천체를 LY 스케일 `ScaledSpace` 거리에 놓고 맵뷰를 관찰하거나, 스톡
DLL을 들여다본다. **작동한다고 가정하지 말 것.** 이것이 플래너의 유력한 타깃 선택 UX가
**커스텀 시스템 피커**(맵뷰 클릭이 아니라)인 *이유*다 — planner-spec §5 참고.

---

## 출처

2026-06-30에 원본 파일을 직접 받아 확인했다. 핵심 퍼머링크.
- Principia `main_window.cs` — https://github.com/mockingbirdnest/Principia/blob/master/ksp_plugin_adapter/main_window.cs#L44
- kOS `VesselUtils.cs` — https://github.com/KSP-KOS/KOS/blob/develop/src/kOS/Utilities/VesselUtils.cs#L166
- Astrogator `KerbalTools.cs` — https://github.com/HebaruSan/Astrogator/blob/master/Source/KerbalTools.cs#L159
- MechJeb2 `GLUtils.cs` — https://github.com/MuMech/MechJeb2/blob/dev/MechJeb2/GLUtils.cs#L12
- MechJeb2 `OrbitExtensions.cs` — https://github.com/MuMech/MechJeb2/blob/dev/MechJeb2/OrbitExtensions.cs#L16
- Kerbalism `GotoVessel.cs` — https://github.com/Kerbalism/Kerbalism/blob/master/src/Kerbalism/Utility/GotoVessel.cs#L24
- API 문서 미러 (ScaledSpace) — https://anatid.github.io/XML-Documentation-for-the-KSP-API/class_scaled_space.html

최상의 근거화(DLL 디컴파일, KSP 1.12.x `Assembly-CSharp.dll`)는 보류 상태다. 입수되면
M-신뢰도 문서 미러 행들을 대체한다. [[project_ksp_stock_api_grounding]] 참고.

## Related

- [`gameplay/interstellar-expansion/planner-spec.md`](../../../gameplay/interstellar-expansion/planner-spec.md) — 이 문서가 근거화하는 §5 인게임 UI 표면(타깃 선택)
- [`plugins/NearStarsRelativity/`](../../../../plugins/NearStarsRelativity/), [`plugins/NearStarsWarp/`](../../../../plugins/NearStarsWarp/), [`plugins/NearStarsFluxTube/`](../../../../plugins/NearStarsFluxTube/) — 이 문서가 해소하는 `// VERIFY:` 마커들
- [principia-cfg-reference](../principia-cfg-reference.md) — 오픈소스(MIT) 사촌 격, `file:line`으로 직접 인용됨
