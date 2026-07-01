# NearStars — Plugin Grounding Map

> Source: derived from [`ksp-modding-sources.md`](ksp-modding-sources.md) (the general index) + the plugin drafts in `plugins/`
> Purpose: starting points for grounding the NearStars C# plugin drafts — which stock API each open question maps to, and who owns what.

> **This is a convenience, NOT a boundary.** It lists starting points for the *current* drafts only.
> For any API not in the tables below, any new plugin, or general "how does KSP modding work," go to
> the general index [`ksp-modding-sources.md`](ksp-modding-sources.md) and KSPDocsSite — always. Do
> **not** treat this page as the limit of what to check; a marker missing here means "look it up," not
> "it doesn't matter." When in doubt, start from the general index, not from this map.

---

## Scope & ownership

**Covers the NearStars-coupled plugins: Warp + FluxTube.** (The relativity layer was promoted to its
own standalone repo on 2026-07-01 — `~/Desktop/ksp-relativity/` — and is no longer a NearStars
plugin; its grounding lives there now.)

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

`plugins/NearStars{Warp,FluxTube}/` touch: `ScaledSpace`(7×), `PartModule`(6×), `KSPField`(6×),
`KSPAddon`(5×), `Vessel`(4×), `Orbit`(3×), `LineRenderer`(3×), `CelestialBody`(3×), `MonoBehaviour`(2×),
`KSPEvent`(2×), `FlightGlobals`(1×), plus `part.RequestResource` / `vessel.*` instance calls. Every
type is in KSPDocsSite (general index §3) — this list is just the current hot-spots, not the ceiling.

## `// VERIFY:` markers → where to resolve them

The Warp draft carries ~15 `VERIFY` markers (FluxTube has none yet). Route each to its grounding
before trusting it. **If a marker isn't listed here, it still needs resolving — look it up in
KSPDocsSite / the wiki.**

| VERIFY touchpoint (file) | Resolve at |
|---|---|
| `part.RequestResource(...)` — ExoticMatter / Megajoules draw (`WarpDriveModule`) | KSPDocsSite `class_part.html` |
| `vessel.obt_velocity` units/frame · `vessel.totalMass` (t) · `vessel.SetPosition`/`GetWorldPos3D` (floating-origin) · `FindPartModuleImplementing<T>` (`WarpDriveModule`, `WarpFlagBridge`) | `class_vessel.html` |
| `PartModule` lifecycle + the part-move call (`WarpDriveModule`) | Wiki *Core Concepts* + `class_part_module.html` |
| Principia detach/re-seed + the fork flag channel (`PrincipiaInterop`) | **Schultz lane** — `mockingbirdnest/Principia` + `gameplay/interstellar-expansion/warp/warp-patch-draft.md` §5.2 (needs the fork) |
| Warp ↔ relativity suppress flag — `WarpFlagBridge` reads the `WarpFlag` now owned by the **external `ksp-relativity` mod** | wire via that mod's public API (cross-repo integration point) |

---

Related: [`ksp-modding-sources.md`](ksp-modding-sources.md) (general index — primary reference) · the extracted relativity mod (`~/Desktop/ksp-relativity/`) · `project_nearstars_mod_plugins_schultz` · `project_nearstars_flux_tube_plugin`.
