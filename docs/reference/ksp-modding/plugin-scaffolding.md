---
title: KSP plugin scaffolding & build (pillar ②)
status: draft
created: 2026-06-30
---

# Plugin scaffolding & build

Grounded surface for *standing up* a KSP 1.12.x C# plugin: entry points, the
PartModule/VesselModule lifecycle, assembly discovery, build references, and the
toolbar button. Grounding policy + confidence legend: see
[`README`](README.md). All rows are **H** (direct open-source code witness) unless
marked. Citations are `repo path:line`; pinned commits in [Provenance](#provenance).

---

## 1. `[KSPAddon(KSPAddon.Startup.X, bool once)]`

Entry point for a non-part plugin: a `MonoBehaviour` KSP instantiates on a scene.
`once = true` → instantiate once and persist; `false` → recreate each matching scene.

| Startup value | witnessed | citation |
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

> **Not witnessed (real enum members, just unused in these repos):** `EditorVAB`,
> `EditorSPH`, `SpaceCentreAndFlight`. Use if needed but treat as M until witnessed.

## 2. `PartModule` lifecycle + attributes (H)

`class X : PartModule` — overrides (param *type* is load-bearing; name is arbitrary):

| Member | citation |
|---|---|
| `public override void OnAwake()` | kOS `Module/kOSProcessor.cs:1001` |
| `public override void OnStart(StartState state)` | kOS `kOSProcessor.cs:397` |
| `public override void OnUpdate()` | Kerbalism `Deploy.cs:57` (or use Unity `Update()`) |
| `public override void OnFixedUpdate()` | kOS `kOSProcessor.cs:925` |
| `public override void OnLoad(ConfigNode node)` | kOS `kOSProcessor.cs:964`; MechJeb2 `MechJebCore.cs:781` |
| `public override void OnSave(ConfigNode node)` | kOS `kOSProcessor.cs:993`; MechJeb2 `MechJebCore.cs:926` |
| `[KSPField]` / `[KSPField(isPersistant=true)]` / `(guiActive=true, guiName=…)` | Kerbalism `Sensor.cs:16/15/19`; kOS `kOSProcessor.cs:90` |
| `[KSPEvent(guiActive=true, guiName="…")] void M()` | kOS `kOSProcessor.cs:152` |
| `[KSPAction("…", actionGroup=KSPActionGroup.None)] void M(KSPActionParam p)` | kOS `kOSProcessor.cs:177` |

## 3. `VesselModule` (H, one gap)

`class X : VesselModule` — one instance per `Vessel`, auto-instantiated on vessel
load. Witnessed in kOS `Module/kOSVesselModule.cs:19`:

| Member | citation |
|---|---|
| `protected override void OnAwake()` | `kOSVesselModule.cs:47` |
| `protected override void OnStart()` | `:71` |
| `protected override void OnLoad(ConfigNode node)` | `:115` |
| per-vessel hooks `OnLoadVessel()` / `OnUnloadVessel()` / `OnGoOffRails()` / `OnGoOnRails()` | `:76 / :91 / :101 / :109` |

> **Gap (M):** a `VesselModule.OnSave(ConfigNode)` override was **not witnessed**
> (kOSVesselModule overrides `OnLoad` only). The stock base exposes the symmetric
> `OnSave(ConfigNode)`; treat as M (symmetric to the witnessed `OnLoad`) until a
> witness is pulled. Relevant to the relativity two-clock accumulator + warp state
> persistence — confirm before relying.

## 4. `MonoBehaviour` in a `[KSPAddon]` class (H)

`[KSPAddon(Startup.FlightAndKSC, false)] public sealed class X : MonoBehaviour` —
KerbalEngineer `Flight/FlightEngineerCore.cs:43`. Unity lifecycle witnessed in the
same file: `Awake()` :242, `Start()` :312, `Update()` :325, `FixedUpdate()` :261,
`OnDestroy()` :276. `OnGUI()` — KerbalEngineer `Editor/BuildOverlay.cs:159`.

## 5. Assembly discovery (H)

| API | witnessed | citation |
|---|---|---|
| `AssemblyLoader.loadedAssemblies` (enumerable of `LoadedAssembly`) | `foreach (var a in AssemblyLoader.loadedAssemblies)` | KSPCommunityFixes `Modding/ModUpgradePipeline.cs:76`; Kerbalism `Kerbalism.cs:501` |
| `GameDatabase.Instance.GetConfigNodes("NODE_NAME") → ConfigNode[]` | `GetConfigNodes("RESOURCE_DEFINITION")` | Kerbalism `Lib.cs:864`; `ScienceDB.cs:210` |

## 6. Assembly versioning (H)

- `[assembly: KSPAssembly("kOS", 1, 5)]` — kOS `Properties/AssemblyInfo.cs:23`.
  Signature `KSPAssembly(string name, int major, int minor)`.
- `[assembly: KSPAssemblyDependency("KerbalEngineer.Unity", 1, 0)]` — KerbalEngineer
  `Properties/AssemblyInfo.cs:36`.

## 7. `.csproj` references + deploy path (H)

From MechJeb2 `MechJeb2.csproj`:
- `<Reference Include="Assembly-CSharp">` :188 and `Assembly-CSharp-firstpass` :192 —
  both `SpecificVersion=False`, `Private=False`, no HintPath (resolved at build from
  `KSP_x64_Data/Managed`).
- UnityEngine modules referenced: `UnityEngine` :206, plus `CoreModule` :218,
  `IMGUIModule` :226, `PhysicsModule` :234, `InputLegacyModule` :230,
  `TextRenderingModule` :238, `UI` :242, `ImageConversionModule` :222,
  `AnimationModule` :210, `AssetBundleModule` :214 (:206–246).
- **Deploy:** post-build `xcopy /Y /I %TargetPath% "%KSPDIR%\GameData\MechJeb2\Plugins\"`
  (`copy_build.bat:32`) → confirms the **`GameData/<Mod>/Plugins/*.dll`** convention.

## 8. `ApplicationLauncher` toolbar button (H)

8-arg `AddModApplication(Callback onTrue, onFalse, onHover, onHoverOut, onEnable,
onDisable, ApplicationLauncher.AppScenes visibleInScenes, Texture texture)`:
- all 8 named — KerbalEngineer `AppLauncherButton.cs:200`.
- nullable callbacks — MechJeb2 `MechJebModuleMenu.cs:254` (`null,null,null,null, AppScenes.ALWAYS, tex`).
- `AppScenes` is `[Flags]` (OR-combine) — kOS `KOSToolbarWindow.cs:26-30,157`
  (`FLIGHT | SPH | VAB | MAPVIEW`). Values witnessed: `ALWAYS, FLIGHT, SPH, VAB, MAPVIEW`.

---

## Gaps / not witnessed (do not fabricate)
- `VesselModule.OnSave(ConfigNode)` override (§3) — M.
- KSPAddon `EditorVAB` / `EditorSPH` / `SpaceCentreAndFlight` — real but unused here (M).

## Provenance
Verified 2026-06-30 by cloning + `grep -n` on working trees (web code-search hit rate
limits). Pinned: MechJeb2 `4c38069` (csproj `0f8903a`), kOS `8f281a4` / tag
`v1.4.0.0` `73c93e6`, Kerbalism `660a802`, KSPCommunityFixes `676e049`, KerbalEngineer
`54b8b73`. Example permalink:
https://github.com/KSPModdingLibs/KSPCommunityFixes/blob/676e049829b082ec4462efb80bf2594d511ac652/KSPCommunityFixes/BugFixes/TimeWarpOrbitShift.cs#L51

## Related
- [`README`](README.md) — KB index + grounding policy
- [`ksp-stock-api.md`](ksp-stock-api.md) — the runtime API this scaffolding hosts
- [`persistence-harmony.md`](persistence-harmony.md) — OnSave/OnLoad + Harmony bootstrap
- [`unity-for-ksp.md`](unity-for-ksp.md) — Unity-side patterns for the MonoBehaviour body
