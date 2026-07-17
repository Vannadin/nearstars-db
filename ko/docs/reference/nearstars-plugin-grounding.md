# NearStars — 플러그인 근거화 지도

> 출처: [`ksp-modding-sources.md`](ksp-modding-sources.md)(범용 색인) + `plugins/`의 플러그인 드래프트에서 파생
> 목적: NearStars C# 플러그인 드래프트를 근거화하는 시작점 — 각 미해결 질문이 어떤 스톡 API에 대응하는지, 그리고 누가 무엇을 맡는지.

> **이건 편의 자료이지 경계가 아니다.** 아래 표는 *현재* 드래프트의 시작점만 담는다. 표에 없는 API,
> 새 플러그인, 혹은 "KSP 모딩이 대체 어떻게 돌아가나"류는 **항상** 범용 색인
> [`ksp-modding-sources.md`](ksp-modding-sources.md)과 KSPDocsSite로 갈 것. 이 페이지를 확인 범위의
> 한계로 여기지 말 것 — 여기 마커가 없다는 건 "찾아봐라"이지 "안 중요하다"가 아니다. 헷갈리면 이 지도가
> 아니라 범용 색인에서 출발한다.

---

## 범위 & 소유권

**NearStars 종속 플러그인 = Warp + FluxTube 를 다룬다.** (상대성 레이어는 2026-07-01 자체 독립 레포로
승격됨 — `~/Desktop/ksp-relativity/` — 이제 NearStars 플러그인이 아니고, 근거화는 거기서 산다.)

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

`plugins/NearStars{Warp,FluxTube}/`가 쓰는 것: `ScaledSpace`(7회), `PartModule`(6회), `KSPField`(6회),
`KSPAddon`(5회), `Vessel`(4회), `Orbit`(3회), `LineRenderer`(3회), `CelestialBody`(3회),
`MonoBehaviour`(2회), `KSPEvent`(2회), `FlightGlobals`(1회), 그리고 `part.RequestResource` / `vessel.*`
인스턴스 호출. 전부 KSPDocsSite에 있음(범용 색인 §3). 이 목록은 현재 핫스팟일 뿐 상한이 아니다.

## `// VERIFY:` 마커 → 어디서 해소하나

Warp 드래프트에 `VERIFY` 마커가 ~15개 있다(FluxTube는 아직 없음). 믿기 전에 각각을 근거에 연결할 것.
**표에 없는 마커도 여전히 해소 대상이다 — KSPDocsSite / 위키에서 찾아볼 것.**

| VERIFY 접점 (파일) | 해소처 |
|---|---|
| `part.RequestResource(...)` — ExoticMatter / Megajoules 소모 (`WarpDriveModule`) | KSPDocsSite `class_part.html` |
| `vessel.obt_velocity` 단위/프레임 · `vessel.totalMass`(t) · `vessel.SetPosition`/`GetWorldPos3D`(floating-origin) · `FindPartModuleImplementing<T>` (`WarpDriveModule`, `WarpFlagBridge`) | `class_vessel.html` |
| `PartModule` 라이프사이클 + part-move 호출 (`WarpDriveModule`) | 위키 *Core Concepts* + `class_part_module.html` |
| Principia detach/re-seed + 포크 flag 채널 (`PrincipiaInterop`) | **슐츠 lane** — `mockingbirdnest/Principia` + `gameplay/interstellar-expansion/warp/warp-patch-draft.md` §5.2 (포크 필요) |
| 워프 ↔ 상대성 suppress flag — `WarpFlagBridge`가 이제 **외부 `ksp-relativity` mod** 소유의 `WarpFlag`를 읽음 | 그 mod의 공개 API로 배선(cross-repo 통합점) |

## 백로그 — 후보 플러그인 (아직 초안 없음)

떠올랐지만 아직 초안을 안 잡은 장기 NearStars 결합 플러그인 아이디어. 소유 규칙 동일 — cfg로 안 되는 런타임 거동은 C# 플러그인, 딥 런타임·인게임 테스트는 슐츠 담당.

| 플러그인 | 하는 일 | cfg로 안 되는 이유 | 근거화 출발점 |
|---|---|---|---|
| **고리면 추종기**(Polyphemus E-고리) | Principia 하에서 Kopernicus 고리를 매 프레임 특정 천체의 *실시간* 궤도면으로 재정렬 — 공급/양치기 위성이 세차해도 고리가 그 위성과 공면 유지. | Kopernicus 고리는 행성에 고정된 정적 디스크라 n-body에 반응 못 함. Principia에선 공급원 Chaos가 세차·libration(~56년, ±~6°, 2천년에 secular ~18°까지 — `results/_principia2000_dense`)해서 고정 고리가 벌어짐. | Kopernicus `Ring` 컴포넌트와 그 transform(KSPDocsSite / Kopernicus 소스), 천체의 실시간 `Orbit` 법선 읽기(`class_orbit.html`), `KSPAddon`/`MonoBehaviour`에서 프레임마다 갱신. **임시(플러그인 전):** 정적 고리를 Chaos 평균면(Laplace)에 앵커 — `phase4/alpha_centauri.yaml` rings 축 참조. |

---

관련: [`ksp-modding-sources.md`](ksp-modding-sources.md)(범용 색인 — 1차 레퍼런스) · 분리된 상대성 mod(`~/Desktop/ksp-relativity/`) · `project_nearstars_mod_plugins_schultz` · `project_nearstars_flux_tube_plugin`.
