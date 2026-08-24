# KSP Modding — Authoritative Source Index

> Source: KSPModdingLibs org (wiki + repos), verified 2026-07-01 via `gh`/raw (not WebFetch summaries)
> Purpose: A routing index — "I want to make *this kind* of mod → here is every authoritative resource I need, where it lives, and how to read it." This is a **pointer**, not a content mirror; it deliberately does not copy the sources (they are living and would go stale).

> **How this index came to be.** A hand-authored KSP-modding KB once lived at
> `docs/reference/ksp-modding/`. It reconstructed modding knowledge by witnessing
> open-source mods, and it was wrong at least once (`ScaledSpace.Factor` → actually
> `ScaleFactor`). It was deleted (commit 57c3d1a) once the community's own
> authoritative material was found: the **KSPModdingLibs** org documents and tools
> the whole mod-making process. This index points at that, grounded.

---

## 0. Access discipline (read before citing anything)

These rules exist because we got burned. Follow them.

1. **WebFetch summaries are NOT a citation source.** WebFetch summarizes pages with a
   small model; it dropped/garbled core classes from `KSPDocsSite/annotated.html`
   **twice**. Use it only for "does this page roughly exist / what's on it"
   reconnaissance.
2. **For any grounded claim, read raw.** `gh api` / `git clone` / `curl` the raw file
   and read the actual line. GitHub wiki raw markdown:
   `https://raw.githubusercontent.com/wiki/KSPModdingLibs/KSPModdingWiki/<Page>.md`.
3. **Pin citations to a commit SHA.** Line numbers drift. Cite `repo path:line @ sha`.
4. **Stock API is closed-source.** There is no KSP repo to cite. The authoritative
   stand-ins are `KSPDocsSite` (Doxygen of the real game assemblies) and, for *witness*,
   any open-source mod that compiles a call to the member. DLL decompile is the
   gold standard, deferred (no KSP install on this Mac).
5. **Building requires KSP's stock assemblies.** `KSPBuildTools` needs `KSPBT_GameRoot`
   pointed at a real KSP install; `KSPLibs` only documents *how to strip* those DLLs from
   an install you already have. With no local KSP, the stock `Managed/` DLLs are a hard
   prerequisite — obtain them from any same-version install before compiling (see §7).
6. **Patreon boundary holds.** Scatterer/EVE/Volumetrics EA material stays local-only;
   never commit EA-gated schema facts. See `feedback_patreon_assets`.

---

## 1. By mod intent → where to look

Find the row that matches "what I want to build," then follow its sources.

| I want to make… | Primary authoritative sources | Notes / where it gets hard |
|---|---|---|
| **A code/plugin mod (C#)** — new behavior, HUD, physics | Wiki *Creating a Plugin* (Win/Linux) · `KSPBuildTools` · `KSPDocsSite` (API) · Wiki *Core Concepts* + *Execution order* | The hard part is **deployment + lifecycle**, not C# (see row below). Build needs stock DLLs (§0 rule 5). |
| **…and get it actually running in KSP** | Wiki *Creating a new Plugin Mod on Windows / Linux* (build → symlink into `GameData` → scene) | This is what newcomers get stuck on (confirmed by JonnyOThan). The setup guides are the answer. |
| **React to game state** (vessel change, launch, part explode, pause) | Wiki *Core Concepts* (`GameEvents`) · KSPDocsSite `class_game_events.html` | Pattern: `GameEvents.onVesselChange.Add(cb)` — and **remove the handler** to avoid leaks (Core Concepts warns). |
| **A ModuleManager cfg patch** (tweak existing content) | MM *Handbook* (official) · MM *Field Guide* (al2me6, unofficial, covers caveats) · `Mutiny` (cfg-driven Delete/Modify of *game objects*, no code) | No compile needed. Field Guide documents gotchas the official docs miss; Mutiny reaches object/prefab tweaks MM can't. |
| **A planet pack / star system** | Kopernicus Wiki · **our skills**: `kopernicus-cfg`, `principia-cfg`, `firefly-cfg`, `researchbodies-cfg` | NearStars' home turf — already grounded in skills + `docs/reference/principia-cfg-reference.md`. |
| **A part mod (models, engines, IVA)** | *KSP1 Modding Bible* · `PartTools` (Unity 2019.4.18f1) · `io_object_mu` (Blender) · Kurgut IVA guide · Kavaeric engines guide · `KSPCommunityPartModules` (reuse shared part modules) | Asset pipeline, not code. Unity version is exact: **2019.4.18f1 LTS**. Depend on KSPCommunityPartModules before writing a common behavior yourself. |
| **A visual mod (shaders/materials)** | `Shabby` (shader asset-bundle loader) · Scatterer/EVE (**local-only**, Patreon) | Custom shaders ship via Shabby + cfg. EA visual mods stay off-repo (§0 rule 6). |
| **Runtime patching of stock behavior** | `HarmonyKSP` · Wiki *Execution order* (`TimingManager`/`TimingStage`) | Harmony is the standard. Persistence/scenario hooks → Core Concepts. |
| **Performance-critical code** | `KSPBurst` (Unity Burst → native) · `KSPProfiler` / `dotTrace` / `UnityHeapExplorer` (profile first) | Profile before optimizing. |
| **Distribution / release** | CKAN *Spec* · Addon Version Checker *Spec* (MiniAVC) · `spacedock-upload` (GitHub Action) | Version file + CKAN metadata + SpaceDock upload. |
| **Debugging a mod** | gotmachine *Debugging & profiling* gist · `UnityExplorerKSP` (in-game inspector) · `TextAnalysisTool.NET` (logs) · `KSPBugReport` (bundle a user's logs/save/screenshots for a repro) | Rider enables real debugging on Linux/Mac. Setup in §7. |
| **NullRef on scene load / object missing** | Wiki *Execution order* + *Core Concepts* · `Player.log` | Usually a **timing** bug: you touched an object before it existed. Check `KSPAddon` startup scene + lifecycle order, not the object. |
| **Reverse-engineer stock behavior** | Wiki *Decompiling KSP* · then `KSPDocsSite` · DLL decompile (ILSpy/dnSpy, deferred) | Last resort when API ref + witnesses are insufficient. |

---

## 2. KSPModdingLibs org — repo map (verified roles)

The org's `.github` profile README is the canonical "for Modders / for Players" split. Verified characterizations:

**Process tooling & docs**
- **KSPBuildTools** (MIT, active, **v1.1.1** 2025-12-01) — MSBuild/NuGet build chain; CKAN dep resolution, version-file gen, CI. Every setup guide uses it. **Requires `KSPBT_GameRoot` → a KSP install.** **Self-documented in-repo**: `docs/msbuild/{getting-started,configuration,dependencies,ksp-install,generating-version-files}.md`, `docs/workflows/`, `docs/actions/` — the authoritative build reference (read raw via `gh`). See §7.
- **KSPModTemplate** (MIT) — starter scaffold for a new mod project.
- **KSPLibs** (README only, no release) — *documents the method* to strip KSP/Unity DLLs to signatures (`assembly-publicizer *.dll --strip-only`, BepInEx/Krafs publicizer) **from a KSP install's `KSP_x64_Data/Managed`**. Not pre-built DLLs.
- **KSPDocsSite** (GitHub Pages) — full Doxygen dump of the real game assemblies. See §3.
- **KSPModdingWiki** — the wiki indexed in §4.
- **.github** — org profile / canonical entry point.

**Runtime libraries (depend as needed)**
- **HarmonyKSP** (MIT) — KSP-packaged Harmony v2 for runtime patching.
- **KSPCommunityPartModules** (MIT, active) — shared part modules to avoid duplication.
- **Shabby** (GPL-3.0, active) — custom shader/material loader.
- **KSPBurst** (active) — Unity Burst compiler package for native-compiled hot paths.
- **Mutiny** (GPL-3.0) — cfg-driven object patching (Delete/Modify) without code.

**Debug / profiling (dev-only, not shipped)**
- **UnityExplorerKSP** (GPL-3.0) — in-game Unity object inspector/editor.
- **UnityHeapExplorer** (MIT) — memory profiler / leak finder.
- **KSPProfiler** (MIT) — in-game gameloop frame-time profiler.

**Misc / CI / end-user**
- **spacedock-upload** (MIT) — GitHub Action: automate SpaceDock releases.
- **KSPBugReport** — end-user log/save bundler.
- **KSPCommunityFixes** — end-user stock bugfix mod, **NOT a modding tutorial** (don't mine it for methodology).

---

## 3. KSPDocsSite — the stock C# API reference

- URL root: `https://kspmoddinglibs.github.io/KSPDocsSite/`
- It is a **complete Doxygen dump** (12,994 HTML files, KSP 1.12.4 assemblies). "Currently just a copy of the last available one."
- **Class page URL pattern:** `class_<snake_case>.html`, where CamelCase → lowercase with an underscore before each capital; acronym letters split (e.g. `FX` → `_f_x`).
  - `ModuleEnginesFX` → `class_module_engines_f_x.html`
- **Member list** for a class: append `-members` (e.g. `class_vessel-members.html`).
- Commonly-referenced classes, all confirmed present: `flight_globals`, `vessel`, `part`,
  `part_module`, `vessel_module`, `scaled_space`, `celestial_body`, `timing_manager`,
  `game_events`, `module_engines`(`_f_x`), `orbit`, `map_view`, `planetarium_camera`,
  `high_logic`.
- **Read raw** (`gh api repos/KSPModdingLibs/KSPDocsSite/contents/<file>` or clone) — WebFetch
  mis-summarized this site twice (§0.1).

---

## 4. The wiki — page directory

Raw markdown: `https://raw.githubusercontent.com/wiki/KSPModdingLibs/KSPModdingWiki/<Page>.md`

- **Guides and Resources** — the master external-link index (mirrored into §5 below).
- **Tools** — 9 dev tools (PartTools, NightStar, VSCode, VS Community, Rider, io_object_mu, TextAnalysisTool, UnityExplorerKSP, dotTrace).
- **Communities** — Discord servers (KSP Modding Society, CKAN, SpaceDock, JonnyODiscord/IVA, Kopernicus).
- **Creating a new Plugin Mod on Windows** / **…on Linux in 2026** — end-to-end setup, build, deploy.
- **Execution order of plugins code** — `TimingManager` + `TimingStage` enum (ObscenelyEarly…BetterLateThanNever), `[DefaultExecutionOrder]`.
- **KSP Core Concepts** — 16 foundational types (KSPAddon, ConfigNode, GameEvents, Vessel, Part, AttachNode, PartModule, VesselModule, ScenarioModule, Scene, InternalModel/Prop/Module, CelestialBody, GameDatabase, KSPField/Event).
- **Speeding up KSP loading for faster iteration** — pruning + QuickStart/HotReload/KSPCommunityFixes.
- **Decompiling KSP** — de4dot (deobfuscate `Assembly-CSharp.dll`) → ILSpy 8.2 (C# 7.3 for KSP 1.12.5). EULA-gray; decompiled output stays local/gitignored.
- **Template Page** — wiki contribution template.

---

## 5. External authoritative resources (exact URLs from the wiki master index)

**General / distribution**
- CKAN Spec — https://github.com/KSP-CKAN/CKAN/blob/master/Spec.md
- Addon Version Checker (MiniAVC) Spec — https://github.com/linuxgurugamer/KSPAddonVersionChecker/blob/master/Documents/MiniAVC/README.md

**Plugins / code**
- KSP API Reference (KSPDocsSite) — https://kspmoddinglibs.github.io/KSPDocsSite/
- Debugging & profiling KSP plugins (gotmachine gist) — https://gist.github.com/gotmachine/d973adcb9ae413386291170fa346d043
- Patched Conics modding journey (YouTube) — https://www.youtube.com/watch?v=maQjOMWcZho
- Plugin modding guide (KSP forum, outdated) — https://forum.kerbalspaceprogram.com/topic/153765-getting-started-the-basics-of-writing-a-plug-in/
- MSBuild/.csproj — https://learn.microsoft.com/en-us/visualstudio/msbuild/msbuild?view=vs-2022
- .NET 4.8 API — https://learn.microsoft.com/en-us/dotnet/api/?view=netframework-4.8.1
- .NET numeric format strings — https://learn.microsoft.com/en-us/dotnet/standard/base-types/standard-numeric-format-strings
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

**Tools** (see §4 Tools page for the full annotated list)
- PartTools (Unity 2019.4.18f1 — .mu/IVA authoring) — https://web.archive.org/web/20240927111307/https://forum.kerbalspaceprogram.com/applications/core/interface/file/attachment.php?id=372
- ksp-cfg-support (VSCode ext) — https://marketplace.visualstudio.com/items?itemName=al2me6.ksp-cfg-support
- io_object_mu (Blender) — https://github.com/taniwha/io_object_mu
- TextAnalysisTool.NET — https://textanalysistool.github.io/

---

## 6. Project-specific bindings → separate doc

This index is **general and reusable** — it deliberately holds no single mod's specifics, so it never
becomes a per-project lookup table. NearStars' own plugin bindings (which stock API each draft's
`// VERIFY:` marker maps to, the ownership split, the dev-Mac build specifics) live in a companion:

→ [`nearstars-plugin-grounding.md`](nearstars-plugin-grounding.md) (+ `ko/` mirror)

That companion is explicit that it is a *convenience, not a boundary* — for anything not in it, you
come back here and to KSPDocsSite. Other projects can ignore it entirely.

---

## 7. Build & deploy a plugin (verified 2026-07-01)

Grounded in **KSPBuildTools @ v1.1.1** + the two wiki setup guides + the Decompiling-KSP page.
KSPBuildTools is self-documented in-repo (§2) — `docs/msbuild/*` is the authoritative build reference.

> **Anti-rot.** The snippets and line numbers below are a *verified snapshot* (2026-07-01,
> KSPBuildTools v1.1.1), not a living mirror. KSPBuildTools rebases — before trusting the XML,
> re-check it against the live source-of-truth: `KSPModdingLibs/KSPModTemplate` and
> `KSPBuildTools/tests/plugin-mod/plugin-mod.csproj`, and re-confirm `KSPCommon.props` line numbers.

**Minimal plugin `.csproj`** (modern SDK-style, KSPBuildTools via NuGet — verified against
`getting-started.md` + `tests/plugin-mod/plugin-mod.csproj`):

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net48</TargetFramework>      <!-- KSP Mono 4.x -->
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
The NuGet package imports `KSPCommon.targets` implicitly; build output copies to `KSPBT_ModRoot`.
Variants: the test project uses a **git-submodule** form (explicit `<Import …/KSPCommon.targets>`,
plus MinVer/JsonPoke); the Decompiling guide shows the **legacy non-SDK** form (`OutputType=Library`,
`TargetFrameworkVersion=v4.0`, `$(ManagedPath)` references). All three work; NuGet SDK-style is simplest.

**Dependencies & version file** (don't hand-roll — KSPBuildTools generates these):
- Declare a dependency with `<ModReference Include="0Harmony"><DLLPath>GameData/000_Harmony/0Harmony.dll</DLLPath><CKANIdentifier>Harmony2</CKANIdentifier></ModReference>` — resolves the compile reference *and* (with `CKANIdentifier`) CKAN-installs it at build time; also auto-emits `[assembly: KSPAssemblyDependency(...)]`. `<CKANDependency Include="X"/>` for data-only deps. (`dependencies.md`)
- Emit the AVC `.version` file with a `<KSPVersionFile>` item (`Name`/`Version`/`KSP_Version{,_Min,_Max}`/`URL`/`Download`). (`generating-version-files.md`)

**A local KSP install is mandatory.** KSPBuildTools resolves stock/Unity assemblies from
`$(KSPBT_GameRoot)/<managed-path>`; it does **not** bundle or download them — unset/invalid
`KSPBT_GameRoot` fails the build with an explicit error. Per-platform managed paths
(`KSPCommon.props:72–74`):
- Windows `KSP_x64_Data/Managed` · macOS `KSP.app/Contents/Resources/Data/Managed` · Linux `KSP_Data/Managed`
- **Do NOT set `KSPBT_GameRoot` in `.csproj`** (`configuration.md` warns). Set it per-machine in
  `.csproj.user` (gitignored), or `KSP_ROOT` env var for CI. Discovery order (`ksp-install.md`):
  `KSPBT_GameRoot` prop → `KSP_ROOT` env → a `KSP/` subdir in the solution → `ReferencePath` → Steam default.

**No local KSP install?** The managed `.dll`s in `Managed/` (Assembly-CSharp, UnityEngine*, …) are
platform-/arch-agnostic .NET IL, so *compiling* likely doesn't require installing KSP on your dev
machine: get the `Managed/` folder from any same-version (1.12.x) install — even one on another OS —
lay it out in the OS-expected path (or override `_KSPBT_ManagedRelativePath`/`KSPBT_GameRoot`), then
`dotnet build`. *Caveat:* the cross-platform `Managed/` copy is **unconfirmed** (KSPBuildTools docs
don't endorse it; some assemblies carry native-interop glue) — compile-reference *should* be fine (IL
only), but verify by building once. (NearStars' concrete Mac setup lives in the companion doc, §6.)

**Deploy & iterate:** `dotnet build` → DLL in `GameData/<ModName>/Plugins/` → symlink that into a
KSP install's GameData (`ln -s` macOS/Linux, `mklink /j` Windows) → relaunch KSP (or F5 from VS/Rider).
Compiling is OS-agnostic; **running / in-game testing** needs an actual KSP install.

**Debugging & profiling** (gotmachine gist — mostly Windows-tested, Rider better on Mac/Linux):
- **Make KSP debuggable**: add `player-connection-debug=1` to `<KSP>/…Data/boot.config` (macOS:
  `KSP.app/Contents/Resources/Data/boot.config`), and drop the *development* `UnityPlayer`
  from the matching Unity 2019.4.18f1 `PlaybackEngines/…development_mono/` into the KSP folder.
- **Build with symbols**: `<DebugType>portable</DebugType>` (Debug config) → ship the `.pdb`
  next to the DLL in GameData.
- **Attach**: VS (Visual Studio Tools for Unity) *Attach Unity Debugger*, or Rider *Attach to Unity
  Process* → pick the KSP instance. Common gotcha: firewall blocks the connection; KSP's
  *Simulate In Background* must be on. Manual IP/port is in `Player.log`.
- **Profile**: compile with `ENABLE_PROFILER`, wrap hot code in `Profiler.BeginSample(...)`/`EndSample()`,
  connect Unity editor *Profiler*. Profile a Release+`ENABLE_PROFILER` build, not Debug (Debug timings
  are meaningless).

**Distribution:** KSPBuildTools also generates the AVC `.version` file and ships GitHub Actions for
CKAN + SpaceDock publish (`docs/workflows/publish-to-spacedock.md`, `docs/actions/`).

---

## 8. Coverage & to-deepen (honest gaps)

Grounded so far: org repo roles (§2), KSPDocsSite usage (§3), wiki page map (§4), master link
index (§5), build/deploy + dependencies + version file + debugging/profiling (§7, from KSPBuildTools
`docs/msbuild/*` + gotmachine gist), Decompiling-KSP (de4dot → ILSpy 8.2, C# 7.3; EULA-gray, DLL/dump
gitignored). The full code-mod lifecycle (build → deploy → debug → distribute) is covered.
Project-specific bindings are split out (§6 → companion). Not yet deepened:
- **Core Concepts / Execution order** — summarized (§4), not yet cited at member level.
- **Part / IVA / visual** branches — link-level only; deepen if a project needs parts or custom shaders.
- **CKAN / SpaceDock release workflow** — `docs/workflows/*` located, not walked through end-to-end.
- **`Managed/` cross-platform compile** — reasoned (§7), not yet executed against a real folder.

Related memory: `project_ksp_stock_api_grounding` · `project_nearstars_mod_plugins_schultz` · `feedback_reference_doc_location` · `feedback_patreon_assets`.
