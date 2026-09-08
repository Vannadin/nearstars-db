---
name: ksp-modding-sources
description: >-
  Authoritative source index for modding Kerbal Space Program (KSP 1.12.x). Routes any KSP
  mod-making task to the community's canonical resources — the KSPModdingLibs wiki + repos,
  the KSPDocsSite C# API reference, KSPBuildTools, ModuleManager, Kopernicus. Use this whenever
  the user wants to create, build, debug, or ship a KSP mod or plugin: writing or scaffolding a
  C# plugin (KSPAddon/PartModule/VesselModule), setting up a plugin .csproj / build, finding the
  stock KSP C# API for a class or method, ModuleManager .cfg patching, part / planet / visual /
  IVA mods, Harmony runtime patching, attaching a debugger to KSP, or publishing to CKAN/SpaceDock —
  even if the user doesn't name a specific tool or repo. Prefer this skill for "how do I mod KSP /
  where do I find X for KSP modding" questions. Do NOT trigger for in-game gameplay or
  orbital-mechanics questions that aren't about building a mod.
---

# KSP Modding — Authoritative Source Index

**What this is.** A routing index into the community's canonical KSP-modding resources: given "I want
to make *this kind* of mod," it tells you which authoritative source to consult, where it lives, and
how to read it correctly. It is a **pointer, not a mirror** — it deliberately does not copy upstream
content (which changes), so always fetch the live source rather than trusting a remembered snapshot.

The whole ecosystem is documented and tooled by the **KSPModdingLibs** GitHub org. Its `.github`
profile README is the canonical "for Modders / for Players" entry point.

---

## 0. Access discipline (read before citing anything)

These rules prevent the most common failure modes when grounding KSP-modding claims.

1. **WebFetch summaries are NOT a citation source.** WebFetch summarizes a page with a small model
   and silently drops/garbles detail (it has mangled `KSPDocsSite` class indexes). Use it only for
   rough "does this page exist / what's on it" reconnaissance.
2. **For any grounded claim, read raw.** Use `gh api` / `git clone` / `curl` and read the actual line.
   GitHub wiki raw markdown lives at
   `https://raw.githubusercontent.com/wiki/KSPModdingLibs/KSPModdingWiki/<Page>.md`.
3. **Pin citations to a commit SHA.** Line numbers drift as repos rebase. Cite `repo path:line @ sha`.
4. **Stock KSP is closed-source.** There is no KSP repo to cite. The authoritative stand-in is
   `KSPDocsSite` (a Doxygen dump of the real game assemblies); for a *witness*, any open-source mod
   that compiles a call to a member proves that member exists. DLL decompile is the last resort and
   is against the Take2 EULA — keep any decompiled output local, never redistribute it.
5. **Building requires KSP's stock assemblies.** `KSPBuildTools` needs `KSPBT_GameRoot` pointed at a
   real KSP install; it does not bundle or download the game DLLs. With no local install you must
   obtain the stock `Managed/` folder from some same-version install before compiling (§7).

---

## 1. By mod intent → where to look

Match the row to what the user wants to build, then follow its sources (§5 has exact URLs).

| I want to make… | Primary authoritative sources | Notes |
|---|---|---|
| **A code/plugin mod (C#)** | Wiki *Creating a Plugin* (Win/Linux) · `KSPBuildTools` · `KSPDocsSite` (API) · Wiki *Core Concepts* + *Execution order* | The hard part is deployment + lifecycle, not C# (next row). Build needs stock DLLs (§0.5). |
| **…and get it running in KSP** | Wiki *Creating a new Plugin Mod on Windows / Linux* (build → symlink into `GameData` → scene) | This is where newcomers get stuck. The setup guides are the answer. |
| **React to game state** (vessel change, launch, part explode, pause) | Wiki *Core Concepts* (`GameEvents`) · KSPDocsSite `class_game_events.html` | Pattern: `GameEvents.onVesselChange.Add(cb)` — and **remove the handler** to avoid leaks. |
| **A ModuleManager cfg patch** | MM *Handbook* (official) · MM *Field Guide* (al2me6, unofficial, covers caveats) · `Mutiny` (cfg-driven Delete/Modify of game objects, no code) | No compile needed. |
| **A planet pack / star system** | Kopernicus Wiki | Config-driven; large, well-documented domain. |
| **A part mod (models, engines, IVA)** | *KSP1 Modding Bible* · `PartTools` (Unity 2019.4.18f1) · `io_object_mu` (Blender) · Kurgut IVA guide · Kavaeric engines guide · `KSPCommunityPartModules` | Asset pipeline, not code. Unity version is exact: **2019.4.18f1 LTS**. |
| **A visual mod (shaders/materials)** | `Shabby` (shader asset-bundle loader) | Custom shaders ship via Shabby + cfg. |
| **Runtime patching of stock behavior** | `HarmonyKSP` · Wiki *Execution order* (`TimingManager`/`TimingStage`) | Harmony is the standard for changing behavior with no cfg/API hook. |
| **Performance-critical code** | `KSPBurst` (Unity Burst → native) · `KSPProfiler` / `dotTrace` / `UnityHeapExplorer` (profile first) | Burst only helps opt-in `[BurstCompile]` Jobs; profile before optimizing. |
| **Distribution / release** | CKAN *Spec* · Addon Version Checker (MiniAVC) *Spec* · `spacedock-upload` (GitHub Action) | `.version` file + CKAN metadata + SpaceDock upload. |
| **Debugging a mod** | gotmachine *Debugging & profiling* gist · `UnityExplorerKSP` (in-game inspector) · `TextAnalysisTool.NET` (logs) · `KSPBugReport` (bundle a user's logs/save for a repro) | Rider enables real debugging on Linux/Mac. Setup in §7. |
| **NullRef on scene load / object missing** | Wiki *Execution order* + *Core Concepts* · `Player.log` | Usually a **timing** bug — you touched an object before it existed. Check `KSPAddon` startup scene + lifecycle order. |
| **Reverse-engineer stock behavior** | Wiki *Decompiling KSP* · then `KSPDocsSite` · DLL decompile (ILSpy/dnSpy) | Last resort; EULA-gray, keep output local. |

---

## 2. KSPModdingLibs org — repo map

**Process tooling & docs**
- **KSPBuildTools** (MIT) — MSBuild/NuGet build chain; CKAN dep resolution, `.version` gen, CI. Every setup guide uses it. Requires `KSPBT_GameRoot` → a KSP install. Self-documented in-repo at `docs/msbuild/*`, `docs/workflows/*`, `docs/actions/*`.
- **KSPModTemplate** (MIT) — starter scaffold for a new mod project.
- **KSPLibs** — documents *how* to strip a KSP install's DLLs to signatures (`assembly-publicizer --strip-only`); not pre-built DLLs.
- **KSPDocsSite** — full Doxygen dump of the real game assemblies (§3).
- **KSPModdingWiki** — the wiki (§4).

**Runtime libraries (depend as needed)**
- **HarmonyKSP** (MIT) — KSP-packaged Harmony v2 for runtime patching. Depend on this one shared copy; don't bundle your own (version conflicts).
- **KSPCommunityPartModules** (MIT) — shared part modules to avoid duplication.
- **Shabby** (GPL-3.0) — custom shader/material loader.
- **KSPBurst** — Unity Burst compiler package; native-compiles `[BurstCompile]` Jobs. No benefit unless you use the Job System.
- **Mutiny** (GPL-3.0) — cfg-driven object patching (Delete/Modify) without code.

**Debug / profiling (dev-only)**
- **UnityExplorerKSP** (GPL-3.0) — in-game Unity object inspector/editor.
- **UnityHeapExplorer** (MIT) — memory profiler / leak finder.
- **KSPProfiler** (MIT) — in-game gameloop frame-time profiler.

**Misc / CI / end-user**
- **spacedock-upload** (MIT) — GitHub Action to automate SpaceDock releases.
- **KSPBugReport** — end-user log/save bundler.
- **KSPCommunityFixes** — end-user stock bugfix mod. **NOT a modding tutorial** — don't mine it for methodology; it's Harmony bugfix patches, not pedagogy.

---

## 3. KSPDocsSite — the stock C# API reference

- Root: `https://kspmoddinglibs.github.io/KSPDocsSite/` — a complete Doxygen dump of the KSP 1.12.x assemblies.
- **Class page URL pattern:** `class_<snake_case>.html`, where CamelCase → lowercase with an underscore before each capital, and acronym letters split. Example: `ModuleEnginesFX` → `class_module_engines_f_x.html`.
- **Member list** for a class: append `-members` (e.g. `class_vessel-members.html`).
- Common classes all resolve: `flight_globals`, `vessel`, `part`, `part_module`, `vessel_module`, `scaled_space`, `celestial_body`, `timing_manager`, `game_events`, `module_engines`(`_f_x`), `orbit`, `map_view`, `planetarium_camera`, `high_logic`.
- **Read raw** (`gh api repos/KSPModdingLibs/KSPDocsSite/contents/<file>` or clone). Do NOT rely on a WebFetch summary of this site — it is large and gets mis-summarized.

---

## 4. The wiki — page directory

Raw markdown: `https://raw.githubusercontent.com/wiki/KSPModdingLibs/KSPModdingWiki/<Page>.md`

- **Guides and Resources** — the master external-link index (mirrored into §5).
- **Tools** — dev tools (PartTools, VSCode, VS, Rider, io_object_mu, TextAnalysisTool, UnityExplorerKSP, dotTrace).
- **Communities** — Discord servers (KSP Modding Society, CKAN, SpaceDock, IVA, Kopernicus).
- **Creating a new Plugin Mod on Windows** / **…on Linux in 2026** — end-to-end setup, build, deploy.
- **Execution order of plugins code** — `TimingManager` + `TimingStage` enum, `[DefaultExecutionOrder]`.
- **KSP Core Concepts** — the 16 foundational types (KSPAddon, ConfigNode, GameEvents, Vessel, Part, AttachNode, PartModule, VesselModule, ScenarioModule, Scene, InternalModel/Prop/Module, CelestialBody, GameDatabase, KSPField/Event).
- **Speeding up KSP loading for faster iteration** — pruning + QuickStart/HotReload.
- **Decompiling KSP** — de4dot → ILSpy 8.2 (C# 7.3 for 1.12.5); EULA-gray, keep output local.

---

## 5. External authoritative resources (exact URLs)

**General / distribution**
- CKAN Spec — https://github.com/KSP-CKAN/CKAN/blob/master/Spec.md
- Addon Version Checker (MiniAVC) Spec — https://github.com/linuxgurugamer/KSPAddonVersionChecker/blob/master/Documents/MiniAVC/README.md

**Plugins / code**
- KSP API Reference (KSPDocsSite) — https://kspmoddinglibs.github.io/KSPDocsSite/
- Debugging & profiling KSP plugins (gotmachine gist) — https://gist.github.com/gotmachine/d973adcb9ae413386291170fa346d043
- Patched Conics modding journey (YouTube) — https://www.youtube.com/watch?v=maQjOMWcZho
- MSBuild/.csproj — https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild?view=vs-2022
- .NET 4.8 API — https://learn.microsoft.com/en-us/dotnet/api/?view=netframework-4.8.1
- Unity 2019.4 Scripting Reference — https://docs.unity3d.com/2019.4/Documentation/ScriptReference/index.html
- Unity 2019.4 Event Execution Order — https://docs.unity3d.com/2019.4/Documentation/Manual/ExecutionOrder.html

**ModuleManager**
- Field Guide (al2me6, unofficial) — https://al2me6.notion.site/A-Field-Guide-To-ModuleManager-279b026272314cbfb24ea3a6cc406371
- Handbook (sarbian, official) — https://github.com/sarbian/ModuleManager/wiki/Module-Manager-Handbook

**Planet modding**
- Kopernicus Wiki — https://kopernicuswiki.org/

**Parts / models**
- KSP1 Modding Bible — https://github.com/the-dev-hole/the_ksp_1_modding_bible/wiki
- Kurgut's IVA guide — https://github.com/kurgut/KSP-IVA-modding-Guide/wiki
- Kavaeric's engines guide — https://kavaeric.notion.site/Creating-engines-for-KSP-16f8338f483b473486ca9657674d85e2
- PartTools (Unity 2019.4.18f1) — https://web.archive.org/web/20240927111307/https://forum.kerbalspaceprogram.com/applications/core/interface/file/attachment.php?id=372
- io_object_mu (Blender) — https://github.com/taniwha/io_object_mu

**Tools**
- ksp-cfg-support (VSCode ext) — https://marketplace.visualstudio.com/items?itemName=al2me6.ksp-cfg-support
- TextAnalysisTool.NET — https://textanalysistool.github.io/

---

## 6. Build & deploy a C# plugin

The canonical build reference is KSPBuildTools' own in-repo docs (`docs/msbuild/*`). **Fetch them live** —
the snippets below are a snapshot, and property names / line numbers drift as KSPBuildTools rebases.

**Minimal plugin `.csproj`** (SDK-style, KSPBuildTools via NuGet):

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net48</TargetFramework>      <!-- KSP runs Mono 4.x -->
    <LangVersion>7.3</LangVersion>                <!-- Unity 2019.4 ceiling -->
    <PlatformTarget>x64</PlatformTarget>
    <AssemblyName>MyMod</AssemblyName>
    <KSPBT_ModRoot>$(MSBuildThisFileDirectory)/GameData/$(MSBuildProjectName)</KSPBT_ModRoot>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="KSPBuildTools" Version="1.1.1" />
  </ItemGroup>
</Project>
```

Confirm the current KSPBuildTools version and the exact template against
`KSPModdingLibs/KSPModTemplate` and `KSPBuildTools/tests/plugin-mod/plugin-mod.csproj` before trusting this.

- **KSP install is mandatory.** KSPBuildTools resolves stock/Unity assemblies from
  `$(KSPBT_GameRoot)/<managed-path>` (Windows `KSP_x64_Data/Managed`, macOS
  `KSP.app/Contents/Resources/Data/Managed`, Linux `KSP_Data/Managed`). **Do not** set `KSPBT_GameRoot`
  in the `.csproj` — set it per-machine in `.csproj.user` (gitignored), or the `KSP_ROOT` env var for CI.
- **No local KSP?** The `Managed/` assemblies are platform-agnostic .NET IL, so *compiling* likely
  works with a `Managed/` folder copied from any same-version install (even on another OS) — verify by
  building once; some assemblies carry native glue.
- **Dependencies:** declare with `<ModReference Include="0Harmony"><DLLPath>…</DLLPath><CKANIdentifier>Harmony2</CKANIdentifier></ModReference>` — resolves the compile reference and CKAN-installs it at build time, and emits `[assembly: KSPAssemblyDependency(...)]`. See `dependencies.md`.
- **Version file:** emit the AVC `.version` with a `<KSPVersionFile>` item. See `generating-version-files.md`.
- **Deploy & iterate:** `dotnet build` → DLL lands in `GameData/<ModName>/Plugins/` → symlink that into
  the KSP install's GameData (`ln -s`, or `mklink /j` on Windows) → relaunch KSP (or F5 from VS/Rider).
- **Debugging:** add `player-connection-debug=1` to `<KSP>/…Data/boot.config` + drop the *development*
  `UnityPlayer` from the matching Unity 2019.4.18f1 `PlaybackEngines/…development_mono/`; build with
  `<DebugType>portable</DebugType>` and ship the `.pdb`; then *Attach Unity Debugger* (VS) / *Attach to
  Unity Process* (Rider). See the gotmachine gist (§5).

---

## Note on sources & license

This skill only **points at** upstream resources — it does not redistribute their code. Each is under
its own license (KSPModdingLibs repos are mostly MIT; Shabby / Mutiny / UnityExplorerKSP are GPL-3.0;
the wiki and third-party guides have their own terms). Respect each when depending on or bundling a
tool. The skill text itself is CC-BY-NC-SA 4.0.
