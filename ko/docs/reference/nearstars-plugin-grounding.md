# NearStars — 플러그인 근거화 지도

> 출처: [`ksp-modding-sources.md`](ksp-modding-sources.md)(범용 색인) + `plugins/`의 플러그인 드래프트에서 파생
> 목적: NearStars C# 플러그인 드래프트를 근거화하는 시작점 — 각 미해결 질문이 어떤 스톡 API에 대응하는지, 그리고 누가 무엇을 맡는지.

> **이건 편의 자료이지 경계가 아니다.** 아래 표는 *현재* 드래프트의 시작점만 담는다. 표에 없는 API,
> 새 플러그인, 혹은 "KSP 모딩이 대체 어떻게 돌아가나"류는 **항상** 범용 색인
> [`ksp-modding-sources.md`](ksp-modding-sources.md)과 KSPDocsSite로 갈 것. 이 페이지를 확인 범위의
> 한계로 여기지 말 것 — 여기 마커가 없다는 건 "찾아봐라"이지 "안 중요하다"가 아니다. 헷갈리면 이 지도가
> 아니라 범용 색인에서 출발한다.

---

## 소유권

이 플러그인들은 본인이 **로컬에서** 빌드·반복하고(개발자 맥에서 컴파일 — 범용 색인 §7 *Build & deploy*
참조) 나중에 슐츠에게 넘긴다. 이 페이지는 핸드오프 자료이기도 하다. 깊은 런타임 작업 — **Principia
포크**와 **Windows 인게임 테스트** — 만 슐츠 lane으로 남긴다(`project_nearstars_mod_plugins_schultz`).

## 개발자 맥에서 빌드 (로컬 KSP 없음)

KSP 설치본의 `Managed/`에 있는 managed `.dll`들(Assembly-CSharp, UnityEngine* 등)은 플랫폼·아키텍처
무관 .NET IL이다. 즉 *컴파일*만이라면 맥에 KSP를 깔 필요가 **아마 없다** — 같은 버전(1.12.x) 설치본의
`Managed/` 폴더만 확보하면 됨(예: 슐츠의 Windows 복사본). macOS 기대 경로에 배치(또는
`_KSPBT_ManagedRelativePath`/`KSPBT_GameRoot` 오버라이드) 후 macOS arm64에서 `dotnet build`. 최소
`.csproj`와 설치 필수 메커니즘은 범용 색인 §7에 있다. *주의:* 크로스플랫폼 `Managed/` 복사는 **미확인**
(일부 어셈블리의 네이티브 interop 글루) — 폴더를 확보해 플러그인 하나로 실제 빌드해 확인할 것. 안 되면
Plan B는 맥에 실제 KSP 설치. **실행/인게임 테스트**는 어느 경우든 실제 KSP 설치가 필요하다(macOS 사본
또는 슐츠 Windows 머신).

## API 표면 (현재 드래프트)

`plugins/NearStars{Relativity,Warp,FluxTube}/`가 쓰는 것: `Vessel`(11회), `KSPAddon`(9회),
`ScaledSpace`(7회), `GUILayout`(7회), `TimingManager`(6회), `PartModule`(6회), `KSPField`(6회),
`Orbit`(5회), `MonoBehaviour`(4회), `CelestialBody`(4회), `Part`(3회), `LineRenderer`(3회),
`FlightGlobals`(3회), `ModuleEngines`(2회), `KSPEvent`(2회), `GUI`(2회), `VesselModule`(1회). 전부
KSPDocsSite에 있음(범용 색인 §3). 이 목록은 현재 핫스팟일 뿐 상한이 아니다.

## `// VERIFY:` 마커 → 어디서 해소하나

플러그인 드래프트에 `VERIFY` 마커가 ~31개 있다. 믿기 전에 각각을 근거에 연결할 것. **표에 없는 마커도
여전히 해소 대상이다 — KSPDocsSite / 위키에서 찾아볼 것.**

| VERIFY 접점 (파일) | 해소처 |
|---|---|
| `Part.AddForce` 단위(kN) + 힘 채널 · `part.RequestResource(...)` (`ThrustCorrector`, `WarpDriveModule`) | KSPDocsSite `class_part.html` |
| `ModuleEngines.finalThrust`(kN) + 추력 방향 (`ThrustCorrector`) | `class_module_engines.html` |
| `vessel.obt_velocity` 단위/프레임 · `vessel.totalMass`(t) · `vessel.SetPosition`/`GetWorldPos3D`(floating-origin) · `FindPartModuleImplementing<T>` (`WarpDriveModule`, `WarpFlagBridge`, `RelativityState`) | `class_vessel.html` |
| `PartModule` 라이프사이클 + part-move 호출 (`WarpDriveModule`) | 위키 *Core Concepts* + `class_part_module.html` |
| 보정 **타이밍** — 엔진 추력 deposit 이후, Principia stage-7 이전 (`ThrustCorrector`) | 위키 *Execution order*(`TimingManager`/`TimingStage`) |
| IMGUI id 유일성 (`RelativityDashboard`) | Unity 2019.4 Scripting Reference(범용 색인 §5) |
| Principia detach/re-seed + flag 채널 (`PrincipiaInterop`, `WarpFlag`) | **슐츠 lane** — `mockingbirdnest/Principia` + `gameplay/interstellar-expansion/warp/warp-patch-draft.md` §5.2 (포크 필요) |
| Kerbalism/ROKerbalism 자원명 + per-vessel 배선 (`ResourceScaler`) | **슐츠 lane** — Kerbalism 소스 |

---

관련: [`ksp-modding-sources.md`](ksp-modding-sources.md)(범용 색인 — 1차 레퍼런스) · `project_nearstars_mod_plugins_schultz` · `project_nearstars_flux_tube_plugin`.
