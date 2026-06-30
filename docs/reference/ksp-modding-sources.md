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
   an install you already have. On this Mac (no KSP), the stock `Managed/` DLLs are a
   hard prerequisite — obtain from a KSP install (Schultz's) before any compile.
6. **Patreon boundary holds.** Scatterer/EVE/Volumetrics EA material stays local-only;
   never commit EA-gated schema facts. See `feedback_patreon_assets`.

---

## 1. By mod intent → where to look

Find the row that matches "what I want to build," then follow its sources.

| I want to make… | Primary authoritative sources | Notes / where it gets hard |
|---|---|---|
| **A code/plugin mod (C#)** — new behavior, HUD, physics | Wiki *Creating a Plugin* (Win/Linux) · `KSPBuildTools` · `KSPDocsSite` (API) · Wiki *Core Concepts* + *Execution order* | The hard part is **deployment + lifecycle**, not C# (see row below). Build needs stock DLLs (§0.5). |
| **…and get it actually running in KSP** | Wiki *Creating a new Plugin Mod on Windows / Linux* (build → symlink into `GameData` → scene) | This is what newcomers get stuck on (confirmed by JonnyOThan). The setup guides are the answer. |
| **A ModuleManager cfg patch** (tweak existing content) | MM *Handbook* (official) · MM *Field Guide* (al2me6, unofficial, covers caveats) | No compile needed. Field Guide documents gotchas the official docs miss. |
| **A planet pack / star system** | Kopernicus Wiki · **our skills**: `kopernicus-cfg`, `principia-cfg`, `firefly-cfg`, `researchbodies-cfg` | NearStars' home turf — already grounded in skills + `docs/reference/principia-cfg-reference.md`. |
| **A part mod (models, engines, IVA)** | *KSP1 Modding Bible* · `PartTools` (Unity 2019.4.18f1) · `io_object_mu` (Blender) · Kurgut IVA guide · Kavaeric engines guide | Asset pipeline, not code. Unity version is exact: **2019.4.18f1 LTS**. |
| **A visual mod (shaders/materials)** | `Shabby` (shader asset-bundle loader) · Scatterer/EVE (**local-only**, Patreon) | Custom shaders ship via Shabby + cfg. EA visual mods stay off-repo (§0.6). |
| **Runtime patching of stock behavior** | `HarmonyKSP` · Wiki *Execution order* (`TimingManager`/`TimingStage`) | Harmony is the standard. Persistence/scenario hooks → Core Concepts. |
| **Performance-critical code** | `KSPBurst` (Unity Burst → native) · `KSPProfiler` / `dotTrace` / `UnityHeapExplorer` (profile first) | Profile before optimizing. |
| **Distribution / release** | CKAN *Spec* · Addon Version Checker *Spec* (MiniAVC) · `spacedock-upload` (GitHub Action) | Version file + CKAN metadata + SpaceDock upload. |
| **Debugging a mod** | gotmachine *Debugging & profiling* gist · `UnityExplorerKSP` (in-game inspector) · `TextAnalysisTool.NET` (logs) | Rider enables real debugging on Linux/Mac. |
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
- Confirmed present (the classes our plugins touch): `flight_globals`, `vessel`, `part`,
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
- **Decompiling KSP** — *(not yet read; grounding row for §1)*.
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
- ksp-cfg-support (VSCode ext) — https://marketplace.visualstudio.com/items?itemName=al2me6.ksp-cfg-support
- io_object_mu (Blender) — https://github.com/taniwha/io_object_mu
- TextAnalysisTool.NET — https://textanalysistool.github.io/

---

## 6. NearStars-specific bindings

What *our* work pulls from where.

- **Our plugin drafts** (`plugins/NearStars{Relativity,Warp,FluxTube}/`) touch: `Vessel`(11×),
  `KSPAddon`(9×), `ScaledSpace`(7×), `GUILayout`(7×), `TimingManager`(6×), `PartModule`(6×),
  `KSPField`(6×), `Orbit`(5×), `MonoBehaviour`(4×), `CelestialBody`(4×), `Part`(3×),
  `LineRenderer`(3×), `FlightGlobals`(3×), `ModuleEngines`(2×), `KSPEvent`(2×), `GUI`(2×),
  `VesselModule`(1×). Every one is in KSPDocsSite (§3).
- **Principia interop** (`PrincipiaInterop.Detach/ReseedAt`) is **not** in KSPModdingLibs →
  `mockingbirdnest/Principia` + our `gameplay/interstellar-expansion/warp/warp-patch-draft.md`.
  Schultz's lane (requires a Principia fork).
- **Build blocker:** stock `Managed/` DLLs needed (§0.5) — Schultz's KSP install.
- **C#/C++ in-game work** is Schultz's lane (`project_nearstars_mod_plugins_schultz`); this side
  does design/spec/cfg + grounding.

---

## 7. Build & deploy a plugin (verified 2026-07-01)

Grounded in **KSPBuildTools @ v1.1.1** + the two wiki setup guides + the Decompiling-KSP page.
KSPBuildTools is self-documented in-repo (§2) — `docs/msbuild/*` is the authoritative build reference.

**Minimal plugin `.csproj`** (modern SDK-style, KSPBuildTools as a NuGet PackageReference):
- `TargetFramework` = `net48` (KSP runs Mono 4.x; net48 is the compile target)
- `LangVersion` = `7.3` (Unity 2019.4 / C# 7.3 ceiling)
- `<PackageReference Include="KSPBuildTools" Version="1.1.1" />`
- Build output auto-copies to `GameData/<ModName>/Plugins/`.
- (The Decompiling guide shows the *legacy* non-SDK form: `<Import …/KSPCommon.targets>` +
  `$(ManagedPath)` references, `OutputType=Library`, `TargetFrameworkVersion=v4.0`. Either works;
  SDK-style is the modern path.)

**A local KSP install is mandatory.** KSPBuildTools resolves stock/Unity assemblies from
`$(KSPBT_GameRoot)/<managed-path>`; it does **not** bundle or download them — unset/invalid
`KSPBT_GameRoot` fails the build with an explicit error. Per-platform managed paths
(`KSPCommon.props:72–74`):
- Windows `KSP_x64_Data/Managed` · macOS `KSP.app/Contents/Resources/Data/Managed` · Linux `KSP_Data/Managed`
- Steam auto-detect per platform (`KSPCommon.props:81–82`).

**This Mac has no KSP — the practical unblock.** The `Managed/` assemblies (Assembly-CSharp,
UnityEngine*, …) are platform-agnostic .NET IL. So we do **not** need to install KSP on the Mac:
obtain the `Managed/` folder from any same-version (1.12.x) install — e.g. Schultz's Windows copy —
lay it out in the macOS-expected path (or override `_KSPBT_ManagedRelativePath`/`KSPBT_GameRoot`),
then `dotnet build` compiles on macOS arm64 (arm64 dotnet SDK; IL is arch-agnostic).
*[Reasoned from the props layout — confirm once we actually have the folder.]*

**Deploy & iterate:** `dotnet build` → DLL in `GameData/<ModName>/Plugins/` → symlink that into the
KSP install's GameData (`ln -s` macOS/Linux, `mklink /j` Windows) → relaunch KSP (or F5 from VS/Rider).
**Running** the game still needs Windows/Mac KSP = Schultz's lane; this Mac is **compile-only**.

**Distribution:** KSPBuildTools also generates the AVC `.version` file and ships GitHub Actions for
CKAN + SpaceDock publish (`docs/workflows/publish-to-spacedock.md`, `docs/actions/`).

---

## 8. Coverage & to-deepen (honest gaps)

Grounded so far: org repo roles (§2), KSPDocsSite usage (§3), wiki page map (§4), master link
index (§5), build & deploy (§7), Decompiling-KSP (de4dot → ILSpy 8.2, C# 7.3; EULA-gray, DLL/dump
gitignored). Not yet deepened:
- **gotmachine debugging gist** — not read; debugging workflow.
- **KSPBuildTools `docs/msbuild/*`** — located, not yet read line-by-line (config knobs, dep resolution).
- **Core Concepts / Execution order** — summarized, not yet cited at member level.
- **Part / IVA / visual** branches — link-level only; deepen if NearStars adds parts or custom shaders.

Related memory: `project_ksp_stock_api_grounding` · `project_nearstars_mod_plugins_schultz` · `feedback_reference_doc_location` · `feedback_patreon_assets`.
