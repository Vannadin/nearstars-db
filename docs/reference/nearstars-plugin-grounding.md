# NearStars — Plugin Grounding Map

> Source: derived from [`ksp-modding-sources.md`](ksp-modding-sources.md) (the general index) + the plugin drafts in `plugins/`
> Purpose: starting points for grounding the NearStars C# plugin drafts — which stock API each open question maps to, and who owns what.

> **This is a convenience, NOT a boundary.** It lists starting points for the *current* drafts only.
> For any API not in the tables below, any new plugin, or general "how does KSP modding work," go to
> the general index [`ksp-modding-sources.md`](ksp-modding-sources.md) and KSPDocsSite — always. Do
> **not** treat this page as the limit of what to check; a marker missing here means "look it up," not
> "it doesn't matter." When in doubt, start from the general index, not from this map.

---

## Ownership

The dev builds and iterates these plugins **locally** (compile on the dev's Mac — see the general
index §7 *Build & deploy*) and hands the result to Schultz later; this page is also the handoff
artifact. Deep runtime work — the **Principia fork** and **in-game testing on Windows** — stays
Schultz's lane (`project_nearstars_mod_plugins_schultz`).

## Building on the dev Mac (no local KSP)

The managed `.dll`s in a KSP install's `Managed/` (Assembly-CSharp, UnityEngine*, …) are
platform-/arch-agnostic .NET IL. So we likely do **not** need to install KSP on the Mac to *compile*:
obtain the `Managed/` folder from any same-version (1.12.x) install — e.g. Schultz's Windows copy —
lay it out in the macOS-expected path (or override `_KSPBT_ManagedRelativePath`/`KSPBT_GameRoot`), then
`dotnet build` on macOS arm64. A minimal `.csproj` and the mandatory-install mechanics are in the
general index §7. *Caveat:* the cross-platform `Managed/`-copy is **unconfirmed** (native-interop glue
in some assemblies) — verify by building one plugin once we have the folder; Plan B is a real macOS KSP
install. **Running / in-game testing** needs an actual KSP install regardless (a macOS copy, or
Schultz's Windows machine).

## API surface (current drafts)

`plugins/NearStars{Relativity,Warp,FluxTube}/` touch: `Vessel`(11×), `KSPAddon`(9×), `ScaledSpace`(7×),
`GUILayout`(7×), `TimingManager`(6×), `PartModule`(6×), `KSPField`(6×), `Orbit`(5×), `MonoBehaviour`(4×),
`CelestialBody`(4×), `Part`(3×), `LineRenderer`(3×), `FlightGlobals`(3×), `ModuleEngines`(2×),
`KSPEvent`(2×), `GUI`(2×), `VesselModule`(1×). Every one is in KSPDocsSite (general index §3) — this list
is just the current hot-spots, not the ceiling.

## `// VERIFY:` markers → where to resolve them

The plugin drafts carry ~31 `VERIFY` markers. Route each to its grounding before trusting it. **If a
marker isn't listed here, it still needs resolving — look it up in KSPDocsSite / the wiki.**

| VERIFY touchpoint (file) | Resolve at |
|---|---|
| `Part.AddForce` units (kN) + force channel · `part.RequestResource(...)` (`ThrustCorrector`, `WarpDriveModule`) | KSPDocsSite `class_part.html` |
| `ModuleEngines.finalThrust` (kN) + thrust direction (`ThrustCorrector`) | `class_module_engines.html` |
| `vessel.obt_velocity` units/frame · `vessel.totalMass` (t) · `vessel.SetPosition`/`GetWorldPos3D` (floating-origin) · `FindPartModuleImplementing<T>` (`WarpDriveModule`, `WarpFlagBridge`, `RelativityState`) | `class_vessel.html` |
| `PartModule` lifecycle + the part-move call (`WarpDriveModule`) | Wiki *Core Concepts* + `class_part_module.html` |
| Correction **timing** — after engine thrust deposit, before Principia stage-7 (`ThrustCorrector`) | Wiki *Execution order* (`TimingManager`/`TimingStage`) |
| IMGUI id uniqueness (`RelativityDashboard`) | Unity 2019.4 Scripting Reference (general index §5) |
| Principia detach/re-seed + flag channel (`PrincipiaInterop`, `WarpFlag`) | **Schultz lane** — `mockingbirdnest/Principia` + `gameplay/interstellar-expansion/warp/warp-patch-draft.md` §5.2 (needs the fork) |
| Kerbalism/ROKerbalism resource names + per-vessel wiring (`ResourceScaler`) | **Schultz lane** — Kerbalism source |

---

Related: [`ksp-modding-sources.md`](ksp-modding-sources.md) (general index — primary reference) · `project_nearstars_mod_plugins_schultz` · `project_nearstars_flux_tube_plugin`.
