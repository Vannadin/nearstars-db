---
title: KSP 플러그인 스캐폴딩 & 빌드 (기둥 ②)
status: draft
created: 2026-06-30
---

# 플러그인 스캐폴딩 & 빌드

KSP 1.12.x C# 플러그인을 *세우는* 데 필요한 근거화된 표면이다. 진입점,
PartModule/VesselModule 생명주기, 어셈블리 탐색, 빌드 레퍼런스, 그리고 툴바 버튼을 다룬다.
근거화 정책과 신뢰도 범례는 [`README`](README.md) 참조. 따로 표기하지 않으면 모든 행은
**H**(공개 소스 코드 직접 witness)다. 인용은 `repo path:line` 형식이며, 핀 박힌 커밋은
[Provenance](#provenance)에 있다.

---

## 1. `[KSPAddon(KSPAddon.Startup.X, bool once)]`

비-part 플러그인의 진입점으로, KSP가 특정 씬에서 인스턴스화하는 `MonoBehaviour`다.
`once = true` → 한 번 인스턴스화하고 유지한다. `false` → 매칭되는 씬마다 새로 생성한다.

| Startup 값 | witnessed | 인용 |
|---|---|---|
| `Flight` | ✓ | KSPCommunityFixes `BugFixes/TimeWarpOrbitShift.cs:51` |
| `EditorAny` | ✓ | KerbalEngineer `Editor/BuildAdvanced.cs:31` |
| `MainMenu` | ✓ | MechJeb2 `InstallChecker.cs:12`; Kerbalism `System/Kerbalism.cs:14` |
| `SpaceCentre` | ✓ | kOS `Module/kOSSettingsChecker.cs:8` |
| `EveryScene` | ✓ | Kerbalism `Utility/Profiler.cs:18` |
| `Instantly` | ✓ | KSPCommunityFixes `KSPCommunityFixes.cs:10`; Kerbalism `System/Loader.cs:30` |
| `FlightAndEditor` | ✓ | kOS `Module/KOSNameTag.cs:86` |
| `TrackingStation` | ✓ | KerbalEngineer `TrackingStation/DisplayStackTS.cs:41` |
| `PSystemSpawn` | ✓ | KSPCommunityFixes `Performance/FastLoader.cs:110` |
| `AllGameScenes` | ✓ | kOS `Module/SceneChangeCleaner.cs:6` |
| `FlightAndKSC` | ✓ | KerbalEngineer `Flight/FlightEngineerCore.cs:43` |

> **미확인(실재하는 enum 멤버이나 이 레포들에서 안 쓰일 뿐):** `EditorVAB`,
> `EditorSPH`, `SpaceCentreAndFlight`. 필요하면 쓰되 witness 전까지는 M으로 다룬다.

## 2. `PartModule` 생명주기 + 속성 (H)

`class X : PartModule` — 오버라이드(파라미터 *타입*이 핵심이고 이름은 임의다).

| 멤버 | 인용 |
|---|---|
| `public override void OnAwake()` | kOS `Module/kOSProcessor.cs:1001` |
| `public override void OnStart(StartState state)` | kOS `kOSProcessor.cs:397` |
| `public override void OnUpdate()` | Kerbalism `Deploy.cs:57` (또는 Unity `Update()` 사용) |
| `public override void OnFixedUpdate()` | kOS `kOSProcessor.cs:925` |
| `public override void OnLoad(ConfigNode node)` | kOS `kOSProcessor.cs:964`; MechJeb2 `MechJebCore.cs:781` |
| `public override void OnSave(ConfigNode node)` | kOS `kOSProcessor.cs:993`; MechJeb2 `MechJebCore.cs:926` |
| `[KSPField]` / `[KSPField(isPersistant=true)]` / `(guiActive=true, guiName=…)` | Kerbalism `Sensor.cs:16/15/19`; kOS `kOSProcessor.cs:90` |
| `[KSPEvent(guiActive=true, guiName="…")] void M()` | kOS `kOSProcessor.cs:152` |
| `[KSPAction("…", actionGroup=KSPActionGroup.None)] void M(KSPActionParam p)` | kOS `kOSProcessor.cs:177` |

## 3. `VesselModule` (H, 갭 하나)

`class X : VesselModule` — `Vessel`당 인스턴스 하나로, 함선 로드 시 자동 인스턴스화된다.
kOS `Module/kOSVesselModule.cs:19`에서 확인된다.

| 멤버 | 인용 |
|---|---|
| `protected override void OnAwake()` | `kOSVesselModule.cs:47` |
| `protected override void OnStart()` | `:71` |
| `protected override void OnLoad(ConfigNode node)` | `:115` |
| 함선별 훅 `OnLoadVessel()` / `OnUnloadVessel()` / `OnGoOffRails()` / `OnGoOnRails()` | `:76 / :91 / :101 / :109` |

> **갭 (M):** `VesselModule.OnSave(ConfigNode)` 오버라이드는 **확인되지 않았다**
> (kOSVesselModule은 `OnLoad`만 오버라이드한다). 스톡 베이스는 대칭짝인
> `OnSave(ConfigNode)`를 노출하므로, witness를 확보하기 전까지는 M으로 다룬다(확인된
> `OnLoad`와 대칭). 상대론 두-시계 누산기 + 워프 상태 persistence와 직결되니, 의존하기
> 전에 반드시 확인한다.

## 4. `[KSPAddon]` 클래스 안의 `MonoBehaviour` (H)

`[KSPAddon(Startup.FlightAndKSC, false)] public sealed class X : MonoBehaviour` —
KerbalEngineer `Flight/FlightEngineerCore.cs:43`. Unity 생명주기는 같은 파일에서
확인된다. `Awake()` :242, `Start()` :312, `Update()` :325, `FixedUpdate()` :261,
`OnDestroy()` :276. `OnGUI()` — KerbalEngineer `Editor/BuildOverlay.cs:159`.

## 5. 어셈블리 탐색 (H)

| API | witnessed | 인용 |
|---|---|---|
| `AssemblyLoader.loadedAssemblies` (`LoadedAssembly`의 enumerable) | `foreach (var a in AssemblyLoader.loadedAssemblies)` | KSPCommunityFixes `Modding/ModUpgradePipeline.cs:76`; Kerbalism `Kerbalism.cs:501` |
| `GameDatabase.Instance.GetConfigNodes("NODE_NAME") → ConfigNode[]` | `GetConfigNodes("RESOURCE_DEFINITION")` | Kerbalism `Lib.cs:864`; `ScienceDB.cs:210` |

## 6. 어셈블리 버전 관리 (H)

- `[assembly: KSPAssembly("kOS", 1, 5)]` — kOS `Properties/AssemblyInfo.cs:23`.
  시그니처는 `KSPAssembly(string name, int major, int minor)`.
- `[assembly: KSPAssemblyDependency("KerbalEngineer.Unity", 1, 0)]` — KerbalEngineer
  `Properties/AssemblyInfo.cs:36`.

## 7. `.csproj` 레퍼런스 + 배포 경로 (H)

MechJeb2 `MechJeb2.csproj` 기준.
- `<Reference Include="Assembly-CSharp">` :188과 `Assembly-CSharp-firstpass` :192 —
  둘 다 `SpecificVersion=False`, `Private=False`, HintPath 없음(빌드 시
  `KSP_x64_Data/Managed`에서 해석된다).
- 참조하는 UnityEngine 모듈: `UnityEngine` :206, 그리고 `CoreModule` :218,
  `IMGUIModule` :226, `PhysicsModule` :234, `InputLegacyModule` :230,
  `TextRenderingModule` :238, `UI` :242, `ImageConversionModule` :222,
  `AnimationModule` :210, `AssetBundleModule` :214 (:206–246).
- **배포:** 빌드 후 `xcopy /Y /I %TargetPath% "%KSPDIR%\GameData\MechJeb2\Plugins\"`
  (`copy_build.bat:32`) → **`GameData/<Mod>/Plugins/*.dll`** 컨벤션을 확인해 준다.

## 8. `ApplicationLauncher` 툴바 버튼 (H)

8-인자 `AddModApplication(Callback onTrue, onFalse, onHover, onHoverOut, onEnable,
onDisable, ApplicationLauncher.AppScenes visibleInScenes, Texture texture)`.
- 8개 모두 명명 — KerbalEngineer `AppLauncherButton.cs:200`.
- nullable 콜백 — MechJeb2 `MechJebModuleMenu.cs:254` (`null,null,null,null, AppScenes.ALWAYS, tex`).
- `AppScenes`는 `[Flags]`(OR 결합) — kOS `KOSToolbarWindow.cs:26-30,157`
  (`FLIGHT | SPH | VAB | MAPVIEW`). 확인된 값: `ALWAYS, FLIGHT, SPH, VAB, MAPVIEW`.

---

## Gaps / not witnessed (do not fabricate)
- `VesselModule.OnSave(ConfigNode)` 오버라이드 (§3) — M.
- KSPAddon `EditorVAB` / `EditorSPH` / `SpaceCentreAndFlight` — 실재하나 여기서 안 쓰임 (M).

## Provenance
2026-06-30에 워킹 트리를 클론 + `grep -n`으로 확인했다(웹 코드 검색은 적중률에 한계가
있다). 핀: MechJeb2 `4c38069` (csproj `0f8903a`), kOS `8f281a4` / tag
`v1.4.0.0` `73c93e6`, Kerbalism `660a802`, KSPCommunityFixes `676e049`, KerbalEngineer
`54b8b73`. 예시 퍼머링크.
https://github.com/KSPModdingLibs/KSPCommunityFixes/blob/676e049829b082ec4462efb80bf2594d511ac652/KSPCommunityFixes/BugFixes/TimeWarpOrbitShift.cs#L51

## Related
- [`README`](README.md) — KB 인덱스 + 근거화 정책
- [`ksp-stock-api.md`](ksp-stock-api.md) — 이 스캐폴딩이 호스팅하는 런타임 API
- [`persistence-harmony.md`](persistence-harmony.md) — OnSave/OnLoad + Harmony 부트스트랩
- [`unity-for-ksp.md`](unity-for-ksp.md) — MonoBehaviour 본문을 위한 Unity 쪽 패턴
