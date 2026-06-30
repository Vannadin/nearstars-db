# KSP 모딩 — 권위 자료 색인

> 출처: KSPModdingLibs 조직(위키 + 레포), 2026-07-01 `gh`/raw로 검증(WebFetch 요약 아님)
> 목적: 라우팅 색인 — "이런 모드를 만들고 싶다 → 그때 필요한 모든 권위 자료가 어디 있고 어떻게 읽는지"를 한 곳에서. 이 문서는 **포인터**이지 내용 미러가 아니다. 원본은 살아있는 자료라 복사하면 곧 stale 되므로 일부러 복사하지 않는다.

> **이 색인이 생긴 경위.** 예전엔 손으로 쓴 KSP 모딩 KB가 `docs/reference/ksp-modding/`에 있었다.
> 오픈소스 모드 호출을 witness 삼아 지식을 재구성하던 방식이었고, 최소 한 번 틀렸다
> (`ScaledSpace.Factor` → 실제는 `ScaleFactor`). 커뮤니티 자신의 권위 자료를 찾은 뒤 삭제했다
> (커밋 57c3d1a). **KSPModdingLibs** 조직이 모드 제작 전 과정을 직접 문서화·도구화해 두었기 때문이다.
> 이 색인은 그곳을 근거 있게 가리킨다.

---

## 0. 접근 규율 (인용 전에 먼저 읽을 것)

데인 적이 있어서 만든 규칙들이다. 지킬 것.

1. **WebFetch 요약은 인용 출처가 아니다.** WebFetch는 작은 모델로 페이지를 요약하는데,
   `KSPDocsSite/annotated.html`에서 핵심 클래스를 **두 번** 누락·왜곡했다. "이 페이지가 대충
   있나/뭐가 실렸나" 정찰용으로만 쓴다.
2. **근거가 필요한 주장은 raw로 읽는다.** `gh api` / `git clone` / `curl`로 raw 파일을 받아
   실제 줄을 읽는다. GitHub 위키 raw 마크다운은
   `https://raw.githubusercontent.com/wiki/KSPModdingLibs/KSPModdingWiki/<Page>.md`.
3. **인용은 commit SHA로 핀한다.** 줄번호는 움직인다. `repo path:line @ sha`로 인용.
4. **스톡 API는 클로즈드소스다.** 인용할 KSP 레포가 없다. 권위 대역은 `KSPDocsSite`(실제 게임
   어셈블리의 Doxygen)이고, *witness*로는 그 멤버 호출을 컴파일하는 오픈소스 모드를 쓴다. DLL
   디컴파일은 gold standard지만 보류(이 맥에 KSP 설치본 없음).
5. **빌드하려면 KSP의 stock 어셈블리가 필요하다.** `KSPBuildTools`는 `KSPBT_GameRoot`가 실제 KSP
   설치를 가리켜야 하고, `KSPLibs`는 *이미 가진 설치본*에서 DLL을 stripped하는 *방법*만 적어 둔다.
   이 맥엔 KSP가 없으니 stock `Managed/` DLL이 컴파일의 선결조건이다 — KSP 설치본(슐츠 것)에서 확보할 것.
6. **Patreon 경계는 유지된다.** Scatterer/EVE/Volumetrics EA 자산은 로컬 전용, EA 한정 스키마
   사실도 커밋 금지. `feedback_patreon_assets` 참조.

---

## 1. 모드 의도별 → 어딜 보나

"무엇을 만들고 싶은가"에 맞는 행을 찾아 그 출처를 따라가면 된다.

| 만들고 싶은 것 | 1차 권위 출처 | 비고 / 어디서 어려워지나 |
|---|---|---|
| **코드/플러그인 모드 (C#)** — 새 거동·HUD·물리 | 위키 *Creating a Plugin*(Win/Linux) · `KSPBuildTools` · `KSPDocsSite`(API) · 위키 *Core Concepts* + *Execution order* | 어려운 건 C#이 아니라 **배포 + 라이프사이클**(아래 행). 빌드는 stock DLL 필요(§0.5). |
| **…그리고 KSP 안에서 실제로 돌리기** | 위키 *Creating a new Plugin Mod on Windows / Linux*(빌드 → `GameData`에 symlink → 씬) | 초심자가 막히는 지점(JonnyOThan이 확인해 줌). 셋업 가이드가 답이다. |
| **ModuleManager cfg 패치** (기존 콘텐츠 손보기) | MM *Handbook*(공식) · MM *Field Guide*(al2me6, 비공식, 캐비엇 풍부) | 컴파일 불필요. Field Guide는 공식 문서가 빠뜨린 함정을 다룬다. |
| **행성 팩 / 항성계** | Kopernicus Wiki · **우리 스킬**: `kopernicus-cfg`, `principia-cfg`, `firefly-cfg`, `researchbodies-cfg` | NearStars 본진 — 스킬 + `docs/reference/principia-cfg-reference.md`로 이미 근거화됨. |
| **부품 모드 (모델·엔진·IVA)** | *KSP1 Modding Bible* · `PartTools`(Unity 2019.4.18f1) · `io_object_mu`(Blender) · Kurgut IVA 가이드 · Kavaeric 엔진 가이드 | 코드가 아니라 에셋 파이프라인. Unity 버전 고정: **2019.4.18f1 LTS**. |
| **비주얼 모드 (셰이더/머티리얼)** | `Shabby`(셰이더 에셋번들 로더) · Scatterer/EVE(**로컬 전용**, Patreon) | 커스텀 셰이더는 Shabby + cfg로 배포. EA 비주얼 모드는 레포 밖(§0.6). |
| **스톡 거동 런타임 패칭** | `HarmonyKSP` · 위키 *Execution order*(`TimingManager`/`TimingStage`) | Harmony가 표준. persistence/scenario 후킹은 Core Concepts. |
| **성능 민감 코드** | `KSPBurst`(Unity Burst → 네이티브) · `KSPProfiler` / `dotTrace` / `UnityHeapExplorer`(먼저 측정) | 최적화 전에 프로파일링부터. |
| **배포 / 릴리스** | CKAN *Spec* · Addon Version Checker *Spec*(MiniAVC) · `spacedock-upload`(GitHub Action) | 버전 파일 + CKAN 메타데이터 + SpaceDock 업로드. |
| **모드 디버깅** | gotmachine *Debugging & profiling* gist · `UnityExplorerKSP`(인게임 인스펙터) · `TextAnalysisTool.NET`(로그) | Rider면 Linux/Mac에서도 실제 디버깅 가능. |
| **스톡 거동 역공학** | 위키 *Decompiling KSP* · 이후 `KSPDocsSite` · DLL 디컴파일(ILSpy/dnSpy, 보류) | API 레퍼런스 + witness로 부족할 때의 최후 수단. |

---

## 2. KSPModdingLibs 조직 — 레포 지도 (검증된 역할)

조직의 `.github` 프로필 README가 "for Modders / for Players" 구분의 정식 기준이다. 검증한 특성화.

**제작 도구 & 문서**
- **KSPBuildTools** (MIT, 활발, **v1.1.1** 2025-12-01) — MSBuild/NuGet 빌드 체인. CKAN 의존성 해소·버전파일 생성·CI. 모든 셋업 가이드가 씀. **`KSPBT_GameRoot` → KSP 설치 필요.** **레포 자체에 문서 있음**: `docs/msbuild/{getting-started,configuration,dependencies,ksp-install,generating-version-files}.md`, `docs/workflows/`, `docs/actions/` — 빌드의 권위 레퍼런스(`gh`로 raw 읽기). §7 참조.
- **KSPModTemplate** (MIT) — 새 모드 프로젝트 스타터 스캐폴드.
- **KSPLibs** (README만, release 없음) — KSP/Unity DLL을 시그니처로 stripped하는 *방법*을 문서화(`assembly-publicizer *.dll --strip-only`, BepInEx/Krafs publicizer). **KSP 설치본의 `KSP_x64_Data/Managed`에서** 만든다. 사전 빌드된 DLL이 아니다.
- **KSPDocsSite** (GitHub Pages) — 실제 게임 어셈블리의 전체 Doxygen 덤프. §3 참조.
- **KSPModdingWiki** — §4에 색인한 위키.
- **.github** — 조직 프로필 / 정식 진입점.

**런타임 라이브러리 (필요할 때 의존)**
- **HarmonyKSP** (MIT) — 런타임 패칭용 KSP 패키지판 Harmony v2.
- **KSPCommunityPartModules** (MIT, 활발) — 중복 방지용 공유 part 모듈.
- **Shabby** (GPL-3.0, 활발) — 커스텀 셰이더/머티리얼 로더.
- **KSPBurst** (활발) — 핫패스 네이티브 컴파일용 Unity Burst 컴파일러 패키지.
- **Mutiny** (GPL-3.0) — 코드 없이 cfg로 오브젝트 패칭(Delete/Modify).

**디버그 / 프로파일링 (dev 전용, 배포 안 함)**
- **UnityExplorerKSP** (GPL-3.0) — 인게임 Unity 오브젝트 인스펙터/에디터.
- **UnityHeapExplorer** (MIT) — 메모리 프로파일러 / 누수 탐지.
- **KSPProfiler** (MIT) — 인게임 게임루프 프레임타임 프로파일러.

**기타 / CI / 엔드유저**
- **spacedock-upload** (MIT) — GitHub Action. SpaceDock 릴리스 자동화.
- **KSPBugReport** — 엔드유저 로그/세이브 번들러.
- **KSPCommunityFixes** — 엔드유저 스톡 버그픽스 모드, **모딩 교본 아님**(방법론 채굴 금지).

---

## 3. KSPDocsSite — 스톡 C# API 레퍼런스

- URL 루트: `https://kspmoddinglibs.github.io/KSPDocsSite/`
- **완전한 Doxygen 덤프**(HTML 12,994개, KSP 1.12.4 어셈블리). "그냥 마지막 가용본 복사."
- **클래스 페이지 URL 패턴:** `class_<snake_case>.html`. CamelCase는 소문자로 바꾸고 대문자마다 앞에 언더스코어, 약어 글자는 분리(예: `FX` → `_f_x`).
  - `ModuleEnginesFX` → `class_module_engines_f_x.html`
- 클래스의 **멤버 목록**: `-members`를 붙임(예: `class_vessel-members.html`).
- 실재 확인(우리 플러그인이 건드리는 클래스): `flight_globals`, `vessel`, `part`,
  `part_module`, `vessel_module`, `scaled_space`, `celestial_body`, `timing_manager`,
  `game_events`, `module_engines`(`_f_x`), `orbit`, `map_view`, `planetarium_camera`,
  `high_logic`.
- **raw로 읽을 것**(`gh api repos/KSPModdingLibs/KSPDocsSite/contents/<file>` 또는 clone) — 이 사이트를
  WebFetch가 두 번 오요약했다(§0.1).

---

## 4. 위키 — 페이지 디렉터리

raw 마크다운: `https://raw.githubusercontent.com/wiki/KSPModdingLibs/KSPModdingWiki/<Page>.md`

- **Guides and Resources** — 마스터 외부 링크 색인(§5에 미러).
- **Tools** — 개발 도구 9종(PartTools, NightStar, VSCode, VS Community, Rider, io_object_mu, TextAnalysisTool, UnityExplorerKSP, dotTrace).
- **Communities** — Discord 서버(KSP Modding Society, CKAN, SpaceDock, JonnyODiscord/IVA, Kopernicus).
- **Creating a new Plugin Mod on Windows** / **…on Linux in 2026** — 셋업·빌드·배포 전 과정.
- **Execution order of plugins code** — `TimingManager` + `TimingStage` enum(ObscenelyEarly…BetterLateThanNever), `[DefaultExecutionOrder]`.
- **KSP Core Concepts** — 코어 타입 16종(KSPAddon, ConfigNode, GameEvents, Vessel, Part, AttachNode, PartModule, VesselModule, ScenarioModule, Scene, InternalModel/Prop/Module, CelestialBody, GameDatabase, KSPField/Event).
- **Speeding up KSP loading for faster iteration** — 프루닝 + QuickStart/HotReload/KSPCommunityFixes.
- **Decompiling KSP** — *(아직 안 읽음. §1의 근거 보강 대상.)*
- **Template Page** — 위키 기여 템플릿.

---

## 5. 외부 권위 자료 (위키 마스터 색인의 정확한 URL)

**일반 / 배포**
- CKAN Spec — https://github.com/KSP-CKAN/CKAN/blob/master/Spec.md
- Addon Version Checker(MiniAVC) Spec — https://github.com/linuxgurugamer/KSPAddonVersionChecker/blob/master/Documents/MiniAVC/README.md

**플러그인 / 코드**
- KSP API Reference(KSPDocsSite) — https://kspmoddinglibs.github.io/KSPDocsSite/
- 디버깅 & 프로파일링 gist(gotmachine) — https://gist.github.com/gotmachine/d973adcb9ae413386291170fa346d043
- Patched Conics 모딩 여정(YouTube) — https://www.youtube.com/watch?v=maQjOMWcZho
- 플러그인 모딩 가이드(KSP 포럼, 구버전) — https://forum.kerbalspaceprogram.com/topic/153765-getting-started-the-basics-of-writing-a-plug-in/
- MSBuild/.csproj — https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild?view=vs-2022
- .NET 4.8 API — https://learn.microsoft.com/en-us/dotnet/api/?view=netframework-4.8.1
- .NET 숫자 포맷 문자열 — https://learn.microsoft.com/en-us/dotnet/standard/base-types/standard-numeric-format-strings
- Unity 2019.4 Scripting Reference — https://docs.unity3d.com/2019.4/Documentation/ScriptReference/index.html
- Unity 2019.4 Event Execution Order — https://docs.unity3d.com/2019.4/Documentation/Manual/ExecutionOrder.html

**ModuleManager**
- Field Guide(al2me6, 비공식) — https://al2me6.notion.site/A-Field-Guide-To-ModuleManager-279b026272314cbfb24ea3a6cc406371
- Handbook(sarbian, 공식) — https://github.com/sarbian/ModuleManager/wiki/Module-Manager-Handbook

**행성 모딩**
- Kopernicus Wiki — https://kopernicuswiki.org/

**부품 / 모델**
- KSP1 Modding Bible — https://github.com/the-dev-hole/the_ksp_1_modding_bible/wiki
- Kurgut IVA 가이드 — https://github.com/kurgut/KSP-IVA-modding-Guide/wiki
- Kavaeric 엔진 가이드 — https://kavaeric.notion.site/Creating-engines-for-KSP-16f8338f483b473486ca9657674d85e2

**도구** (전체 주석 목록은 §4 Tools 페이지)
- ksp-cfg-support(VSCode 확장) — https://marketplace.visualstudio.com/items?itemName=al2me6.ksp-cfg-support
- io_object_mu(Blender) — https://github.com/taniwha/io_object_mu
- TextAnalysisTool.NET — https://textanalysistool.github.io/

---

## 6. NearStars 전용 바인딩

*우리* 작업이 어디서 무엇을 끌어오나.

- **우리 플러그인 드래프트**(`plugins/NearStars{Relativity,Warp,FluxTube}/`)가 쓰는 것: `Vessel`(11회),
  `KSPAddon`(9회), `ScaledSpace`(7회), `GUILayout`(7회), `TimingManager`(6회), `PartModule`(6회),
  `KSPField`(6회), `Orbit`(5회), `MonoBehaviour`(4회), `CelestialBody`(4회), `Part`(3회),
  `LineRenderer`(3회), `FlightGlobals`(3회), `ModuleEngines`(2회), `KSPEvent`(2회), `GUI`(2회),
  `VesselModule`(1회). 전부 KSPDocsSite에 있음(§3).
- **Principia interop**(`PrincipiaInterop.Detach/ReseedAt`)는 KSPModdingLibs에 **없음** →
  `mockingbirdnest/Principia` + 우리 `gameplay/interstellar-expansion/warp/warp-patch-draft.md`.
  슐츠 lane(Principia 포크 필요).
- **빌드 병목:** stock `Managed/` DLL 필요(§0.5) — 슐츠의 KSP 설치본.
- **인게임 C#/C++ 작업**은 슐츠 lane(`project_nearstars_mod_plugins_schultz`). 이쪽은 설계/스펙/cfg + 근거화.

---

## 7. 플러그인 빌드 & 배포 (2026-07-01 검증)

**KSPBuildTools v1.1.1** + 위키 셋업 가이드 둘 + Decompiling-KSP 페이지에 근거. KSPBuildTools는
레포 자체에 문서를 가짐(§2) — `docs/msbuild/*`가 빌드의 권위 레퍼런스.

**최소 플러그인 `.csproj`** (모던 SDK 스타일, KSPBuildTools를 NuGet으로 — `getting-started.md` +
`tests/plugin-mod/plugin-mod.csproj`로 검증):

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net48</TargetFramework>      <!-- KSP Mono 4.x -->
    <LangVersion>7.3</LangVersion>                <!-- Unity 2019.4 상한 -->
    <PlatformTarget>x64</PlatformTarget>
    <AssemblyName>NearStarsRelativity</AssemblyName>
    <KSPBT_ModRoot>$(MSBuildThisFileDirectory)/GameData/$(MSBuildProjectName)</KSPBT_ModRoot>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="KSPBuildTools" Version="1.1.1" />
  </ItemGroup>
</Project>
```
NuGet 패키지가 `KSPCommon.targets`를 암묵적으로 import. 빌드 산출물은 `KSPBT_ModRoot`로 복사.
변형: 테스트 프로젝트는 **git-submodule** 형태(명시적 `<Import …/KSPCommon.targets>` + MinVer/JsonPoke),
Decompiling 가이드는 **레거시 비-SDK** 형태(`OutputType=Library`, `TargetFrameworkVersion=v4.0`,
`$(ManagedPath)` 참조). 셋 다 되지만 NuGet SDK 스타일이 가장 간단.

**의존성 & 버전 파일** (손으로 만들지 말 것 — KSPBuildTools가 생성):
- 의존성은 `<ModReference Include="0Harmony"><DLLPath>GameData/000_Harmony/0Harmony.dll</DLLPath><CKANIdentifier>Harmony2</CKANIdentifier></ModReference>`로 선언 — 컴파일 참조를 해소하고, `CKANIdentifier`가 있으면 빌드 시 CKAN 설치까지. `[assembly: KSPAssemblyDependency(...)]`도 자동 생성. 데이터 전용 의존성은 `<CKANDependency Include="X"/>`. (`dependencies.md`)
- AVC `.version` 파일은 `<KSPVersionFile>` 아이템으로 생성(`Name`/`Version`/`KSP_Version{,_Min,_Max}`/`URL`/`Download`). (`generating-version-files.md`)

**로컬 KSP 설치가 필수다.** KSPBuildTools는 stock/Unity 어셈블리를 `$(KSPBT_GameRoot)/<managed-path>`에서
해소한다. 번들하거나 다운로드하지 **않음** — `KSPBT_GameRoot`가 비었거나 잘못되면 명시적 에러로
빌드 실패. 플랫폼별 managed 경로(`KSPCommon.props:72–74`):
- Windows `KSP_x64_Data/Managed` · macOS `KSP.app/Contents/Resources/Data/Managed` · Linux `KSP_Data/Managed`
- **`KSPBT_GameRoot`를 `.csproj`에 넣지 말 것**(`configuration.md` 경고). 머신별로 `.csproj.user`(gitignore)에
  두거나, CI는 `KSP_ROOT` 환경변수로. 탐색 순서(`ksp-install.md`):
  `KSPBT_GameRoot` 속성 → `KSP_ROOT` 환경변수 → 솔루션의 `KSP/` 하위폴더 → `ReferencePath` → Steam 기본 경로.

**이 맥엔 KSP가 없다 — 현실적 우회.** `Managed/` 어셈블리(Assembly-CSharp, UnityEngine* 등)는
플랫폼 무관 .NET IL이다. 즉 맥에 KSP를 깔 필요 **없이** 같은 버전(1.12.x) 설치본의 `Managed/`
폴더만 확보하면 됨 — 예: 슐츠의 Windows 복사본 — macOS 기대 경로에 배치(또는
`_KSPBT_ManagedRelativePath`/`KSPBT_GameRoot` 오버라이드)하면 `dotnet build`가 macOS arm64에서
컴파일된다(arm64 dotnet SDK, IL은 아키텍처 무관).
*[props 레이아웃에서 추론 — 폴더 확보하면 확인할 것.]*

**배포 & 반복:** `dotnet build` → DLL이 `GameData/<ModName>/Plugins/`에 → 그걸 KSP 설치본의
GameData로 symlink(`ln -s` macOS/Linux, `mklink /j` Windows) → KSP 재실행(또는 VS/Rider에서 F5).
게임 **실행**은 여전히 Windows/Mac KSP 필요 = 슐츠 lane. 이 맥은 **컴파일 전용**.

**디버깅 & 프로파일링** (gotmachine gist — 주로 Windows 검증, 맥/리눅스는 Rider가 나음):
- **KSP를 디버깅 가능하게**: `<KSP>/…Data/boot.config`에 `player-connection-debug=1` 추가(macOS는
  `KSP.app/Contents/Resources/Data/boot.config`), 그리고 같은 Unity 2019.4.18f1의
  `PlaybackEngines/…development_mono/`에서 *개발용* `UnityPlayer`를 KSP 폴더에 넣음.
- **심볼 포함 빌드**: `<DebugType>portable</DebugType>`(Debug 구성) → `.pdb`를 GameData의 DLL 옆에 둠.
- **어태치**: VS(Visual Studio Tools for Unity) *Attach Unity Debugger*, 또는 Rider *Attach to Unity
  Process* → KSP 인스턴스 선택. 흔한 함정: 방화벽이 연결 차단, KSP의 *Simulate In Background* 켜야 함.
  수동 IP/포트는 `Player.log`에 있음.
- **프로파일**: `ENABLE_PROFILER`로 컴파일, 핫코드를 `Profiler.BeginSample(...)`/`EndSample()`로 감싸고
  Unity 에디터 *Profiler* 연결. Debug 말고 Release+`ENABLE_PROFILER` 빌드를 프로파일할 것(Debug 타이밍은
  의미 없음).

**배포(distribution):** KSPBuildTools는 AVC `.version` 파일도 생성하고 CKAN + SpaceDock 퍼블리시용
GitHub Action도 제공(`docs/workflows/publish-to-spacedock.md`, `docs/actions/`).

---

## 8. 커버리지 & 더 팔 곳 (정직한 갭)

여기까지 근거화: 조직 레포 역할(§2), KSPDocsSite 사용법(§3), 위키 페이지 지도(§4), 마스터 링크
색인(§5), 빌드/배포 + 의존성 + 버전 파일 + 디버깅/프로파일링(§7, KSPBuildTools `docs/msbuild/*` +
gotmachine gist), Decompiling-KSP(de4dot → ILSpy 8.2, C# 7.3. EULA-회색, DLL/덤프 gitignore).
코드 모드 라이프사이클 전체(빌드 → 배포 → 디버그 → 릴리스)가 이제 커버됨. 아직 더 안 판 것.
- **Core Concepts / Execution order** — 요약만(§4), 아직 멤버 수준 인용 안 함.
- **부품 / IVA / 비주얼** 갈래 — 링크 수준만. NearStars가 부품·커스텀 셰이더 추가하면 그때 심화.
- **CKAN / SpaceDock 릴리스 워크플로** — `docs/workflows/*` 위치 파악, 끝까지 걸어보진 않음.

관련 메모리: `project_ksp_stock_api_grounding` · `project_nearstars_mod_plugins_schultz` · `feedback_reference_doc_location` · `feedback_patreon_assets`.
