# NearStars — Mod Reference

> **Perspective.** This document is the **KSP mod install reference**:
> which mods to install, what they do, and where to download them, split
> by dependency tier (Required / Graphics / Compatibility / Optional).
>
> For the **attribution / license** side — which external mods NearStars
> reproduces content from, under what license, and how — see
> [`data-sources.md`](data-sources.md). Only Kopernicus, Principia, and
> Sol-Configs are referenced from that file; everything else here is
> install-only and has no attribution obligation.

## Required Dependencies (mod won't load without these)

| Mod | Description | GitHub |
|-----|-------------|--------|
| **Kopernicus** (ballisticfox fork) | Custom planetary system framework. Without it, NearStars bodies don't exist. License: LGPL-3.0 — see [data-sources.md §2](data-sources.md#kopernicus-ballisticfox-fork) | [ballisticfox/Kopernicus](https://github.com/ballisticfox/Kopernicus) |
| **Module Manager** | cfg patch language runtime. Provides `NEEDS[]`, `FOR[]`, `@` patch syntax. Without it, all patches are void | [sarbian/ModuleManager](https://github.com/sarbian/ModuleManager) |
| **BurstPQS** | Burst-compiled terrain generation. ~15× faster than stock, eliminates scene-switch stutter | [Phantomical/BurstPQS](https://github.com/Phantomical/BurstPQS) |
| **Sol** (ballisticfox) | Modern recreation of the real solar system at real, quarter, and stock scale. NearStars attaches new star systems to this base system. License: CC-BY-NC-SA 4.0 — see [data-sources.md §2](data-sources.md#sol-configs-rss-reborn--ballisticfox) | [RSS-Reborn/Sol-Configs](https://github.com/RSS-Reborn/Sol-Configs) |

---

## Graphics Mods

### Direct Dependencies (NearStars cfg files reference these directly)

| Mod | Description | GitHub |
|-----|-------------|--------|
| **Parallax Continued** | PBS terrain shaders + 3D scatter objects. NearStars writes `[Body]-ParallaxTerrain.cfg` and `[Body]-ParallaxScatters.cfg` directly | [Gameslinx/Parallax-Continued](https://github.com/Gameslinx/Parallax-Continued) |
| **EVE-Redux / EVE Volumetrics V5** | Cloud and aurora layers. V5 adds volumetric clouds (Patreon build). NearStars writes `EVE_CLOUDS` cfg directly | [LGhassen/EnvironmentalVisualEnhancements](https://github.com/LGhassen/EnvironmentalVisualEnhancements) |

### Compatibility Patches — Priority 1 (visuals break without these)

| Mod | Description | GitHub |
|-----|-------------|--------|
| **Scatterer** | Rayleigh/Mie atmospheric scattering, ocean reflections, sun flares. Requires `Scatterer_atmosphere` per planet and `Scatterer_sunflare` per star | [LGhassen/Scatterer](https://github.com/LGhassen/Scatterer) |
| **Firefly** | Aerodynamic heating effects during reentry and supersonic flight. Uses `ATMOFX_PLANET_PACK` + `ATMOFX_BODY` nodes to define per-planet colors and intensity | [M1rageDev/Firefly](https://github.com/M1rageDev/Firefly) |
| **Deferred Rendering** | Deferred rendering pipeline for KSP. No cfg patches required, but Scatterer/EVE versions must be verified as Deferred-compatible. Parallax is already compatible | [LGhassen/Deferred](https://github.com/LGhassen/Deferred) |

### Compatibility Patches — Priority 2 (loads without these, quality difference)

| Mod | Description | GitHub |
|-----|-------------|--------|
| **Distant Object Enhancement** | Renders distant planets and stars at realistic apparent size and color. Requires custom flare color registration per new star | [KSPModStewards/DistantObjectEnhancement](https://github.com/KSPModStewards/DistantObjectEnhancement) |
| **PlanetShine** | Planets and moons cast reflected light onto vessels. Requires reflected light color configuration per body | [PapaJoesSoup/ksp-planetshine](https://github.com/PapaJoesSoup/ksp-planetshine) |
| **TUFX** | Unity Post Process Package v2 wrapper. Can provide per-system bloom and color grading profiles | [KSPModStewards/TUFX](https://github.com/KSPModStewards/TUFX) |

### Compatibility Patches — Optional

| Mod | Description | GitHub |
|-----|-------------|--------|
| **Textures Unlimited** | PBR reflection shaders. Enables physically based reflections on metallic or icy body surfaces | [shadowmage45/TexturesUnlimited](https://github.com/shadowmage45/TexturesUnlimited) |
| **True Volumetric Clouds** | Advanced volumetric cloud system by blackrack, separate from EVE. Incompatible with EVE V5 — deferred to long-term scope | Patreon only |

---

## Non-Graphics Compatibility Patches

| Mod | Description | GitHub |
|-----|-------------|--------|
| **Principia** | N-body gravity simulation. Requires gravitational parameter registration per star, with separate configs for Sol, Sol-Quarter, and RSS scales. License: MIT — see [data-sources.md §2](data-sources.md#principia-mockingbirdnest) | [mockingbirdnest/Principia](https://github.com/mockingbirdnest/Principia) |
| **Kerbalism** | Radiation, life support, and science overhaul. Requires radiation environment config per star system. Support TBD | [Kerbalism/Kerbalism](https://github.com/Kerbalism/Kerbalism) |
| **ResearchBodies** | Telescope-based body discovery mechanic. Requires registering new bodies in the discovery list | [JPLRepo/ResearchBodies](https://github.com/JPLRepo/ResearchBodies) |

---

## Time-Warp & Relativity (interstellar-play set) — Principia-fork compatibility (verified 2026-07-18)

Sub-light interstellar play needs warp rates far beyond stock (40 ly at 0.1c ≈ 400 y
= 35 wall-clock HOURS at stock 100,000×), so these two ride along with the Principia
fork. Compatibility assessed against the upstream FAQ's rule — a mod is incompatible
iff it "moves vessels or otherwise changes orbits (1) without using engines or
(2) during time warp" — plus source-level reading of both mods.

| Mod | Verdict | GitHub |
|-----|---------|--------|
| **BetterTimeWarpContinued** | Compatible (rate-table mod, moves no vessels). Upstream-measured: smooth at 100,000×, "janky" at 1,000,000× (CPU, not correctness), 6,000,000× smooth with no vessels. Practical ceiling for sustained ultra-warp is Principia CPU + **RAM growth** (the upstream eviction issue our PR targets) — measure via the in-game kit's long-cruise scenario. Prefer rails warp; its boosted physics warp just multiplies unpacked integration load. The fork's WS4 dead-man switch is warp-rate independent by design; WS3 burn integration takes arbitrary Δt chunks. | [linuxgurugamer/BetterTimeWarpContinued](https://github.com/linuxgurugamer/BetterTimeWarpContinued) |
| **Relativity** (Vannadin) | Compatible in normal (unpacked) flight BY DESIGN: the γ³ thrust suppression is injected as a corrective part-force before Principia's TimingManager read, verified in-game on Principia force profiles; the proper-time ledger ticks every FixedUpdate for loaded AND unloaded vessels (time-warp-valid). Its "warp guard" is an FTL-drive Provider hook, NOT time warp. **KNOWN GAP: the fork's WS3 on-rails burn takes NO γ³ correction** — the burn harvest synthesizes thrust from engine-module data (maxThrust × throttle × vacuum Isp), and the corrective force lives only in the (packed-idle) part-force channel ⇒ warp-burning near c integrates Newtonian thrust and can cross c. Fix shape: the WS3 harvest queries Relativity for a 1/γ³ multiplier (reflection, present-guarded, the same pattern as Relativity's Kerbalism adapter); mass flow stays nominal (matches Relativity's design). Tracked on the Principia-fork side. | [Vannadin/Relativity](https://github.com/Vannadin/Relativity) |

Also relevant: upstream lists **Blueshift** (warp drive) as incompatible; the fork's
WS4 release channel (`PrincipiaWarpStatus.warpEngaged`) exists precisely to lift that
class of incompatibility — warp mods release the vessel from Principia management and
re-adopt on arrival. Non-standard propulsion that edits orbits directly during warp
(Persistent-Thrust-style) remains incompatible by the upstream rule unless routed
through WS3 (standard `ModuleEngines` inheritors are what the WS3 harvest reads).

## Reference Repos (examples from other planet packs)

| Repo | Purpose |
|------|---------|
| [SPACEMAN9813/Firefly-Planet-Pack-Configs](https://github.com/SPACEMAN9813/Firefly-Planet-Pack-Configs) | Firefly cfg examples from various planet packs |
| [OneSaltyPringle/OPM-Parallax](https://github.com/OneSaltyPringle/OPM-Parallax) | Parallax Continued cfg examples from OPM |

## Related

- [methodology](methodology.md) — cluster hub
- [mod-release-layout](mod-release-layout.md) — repo layout that consumes these mods
- [data-sources](data-sources.md) — license/attribution side of the mods referenced here (Kopernicus, Principia, Sol-Configs)
- [guideline](guideline.md) — project-level scope (which mods are required vs optional)
- [principia-cfg-reference](principia-cfg-reference.md) — Principia mod's cfg API
