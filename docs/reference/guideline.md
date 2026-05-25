# Nearby Star Systems KSP Mod — Project Guideline

**Goal:** Add nearby star systems to KSP 1.12.x on top of Sol-Configs (real solar system). RSS compatibility is a planned future target.

---

## 1. Project Overview

| Item | Detail |
|------|--------|
| Mod name | NearStars |
| KSP version | 1.12.x |
| License | CC-BY-NC-SA-4.0 (matching Sol) |
| Type | Sol-based addon. RSS compatibility deferred. |

The mod adds new star systems; it does not touch or replace existing Sol bodies. RSS compatibility is planned but not currently shipped.

---

## 2. Dependencies

**Required:**

| Mod | Role |
|-----|------|
| Sol-Configs (ballisticfox) | Real solar system base (`FOR[SolSystem]`) |
| Kopernicus (ballisticfox fork) | Body definition framework |
| Module Manager | Conditional patching (`NEEDS[]`) |
| Parallax Continued | Terrain shaders and scatters |
| EVE Volumetrics V5 | Cloud layers (atmospheric bodies only) |
| BurstPQS | Terrain generation optimization |

**Future target (not currently supported):**

| Mod | Tag |
|-----|-----|
| RealSolarSystem | `FOR[RSSConfig]` |

Note: [RSS-Origin 2](https://github.com/CharonSSS/RSS-Origin-2) (CharonSSS, v1.0.0 released 2026-05-21) is the Sol-compatible successor of RSS-Origin v1.x and is now the canonical asteroid/comet/dwarf-planet add-on for Sol-based installs. It is a separate repository from `CharonSSS/RSS-Origin` (v1.x, no Sol support). The patch templates in §5.1 are designed to extend cleanly to RSS once RSS support is implemented.

---

## 3. Target Star Systems

### 3.1 Distance limits

| Engine | Max range | Source |
|--------|-----------|--------|
| Kopernicus (rendering + SOI) | ~50 ly | REX developer |
| Principia (gravitational perturber) | ~80 ly | RSS-Origin 2 developer |

Kopernicus bodies beyond ~50 ly risk map-view failures, floating-point glitches in the renderer, or engine crashes. This is a hard constraint — all Kopernicus bodies must be within 50 ly.

Principia registers stars as gravitational perturbers through a separate mechanism that is not subject to KSP's rendering limits. Stars in the 50–80 ly range are therefore candidates for **Principia-only entries** (no Kopernicus body, no visual presence, gravity effect only).

### 3.2 Scope

The current data pipeline covers all confirmed planetary systems and noteworthy stellar systems within 50 ly. This fully covers the Kopernicus range. See the [live DB viewer](https://vannadin.github.io/nearstars-db/) for the current system list and count. A separate Principia-only pass for the 50–80 ly band can be added later if desired.

### 3.3 Development order

**Build one complete system first, then expand.** The first system serves as the template and reference implementation for all subsequent systems. Do not start a second system until the first is fully playable (Phase 1 + Phase 2 complete for that system).

The final mod ships **~10 stellar systems** selected from the research database in this repo. Selection list and order are still being decided — candidates include Proxima Centauri (nearest, single-star, 2 planets), Barnard's Star (5.96 ly), Alpha Centauri (hierarchical triple, 3 components), and others.

---

## 4. Mod-release repo conventions

The mod release lives in a **separate repo** (`NearStars-Configs/` + `NearStars-Textures/`), not in `nearstars-db`. Its directory layout, cfg conventions, and texture conventions are documented in [`mod-release-layout.md`](mod-release-layout.md):

- §1 Repository structure
- §2 Config conventions (patch tags, body identifier, star/planet templates, file separation)
- §3 Texture conventions

This document keeps project-level scope (targets, data sources, phases, index allocation) below.

---

## 7. flightGlobalsIndex Allocation

Must not collide with Sol-Configs (NAIF SPK-style IDs, see table below)
or RSS-Origin v1.x. NearStars uses 1000+ with 100 indices per system,
which sits in the empty band between Sol-Configs' planetary IDs (≤916)
and its asteroid IDs (≥9000).

| Range | Owner |
|-------|-------|
| 0–99 | Stock KSP / RealSolarSystem (KSP-RO/RealSolarSystem occupies 1–25, 50, 60, 91–95) |
| `10`, `100`–`916` | Sol-Configs planets and moons — NAIF SPK-style IDs (Sol=`10`; Mercury=`100`; Venus=`200`; Earth=`300`, Luna=`301`; Mars=`400`, Phobos=`401`, Deimos=`402`; Jupiter=`500`, Galileans=`501–504`, Amalthea=`505`, Himalia=`514`; Saturn=`600`, major moons=`601–609`, Phoebe=`615`; Uranus=`700`, major moons=`701–705`, Sycorax=`715`; Neptune=`800`, Triton=`801`, Nereid=`802`, Proteus=`808`; Pluto system=`901–916`) |
| `9xxx`–`9xxxxxx` | Sol-Configs asteroids — `9` + asteroid number (Ida=`9243`, Dactyl=`92431`, Pallas=`902`, Ryugu=`9162173`) |
| `10xxxxxx`+ | Sol-Configs TNOs / dwarf planets (Eris=`10134340`, Arrokoth=`10486958`) |
| 1000–1099 | NearStars — first star system (TBD). Sits in the empty `1000–8999` band between Sol-Configs planet IDs (`≤916`) and asteroid IDs (`≥9000`). |
| 1100–1199 | NearStars — second star system (TBD) |
| 1200–1299 | NearStars — third star system (TBD) |
| 1300+ | NearStars — further systems (+100 per system) |

Note: RSS-Origin 2 itself does not assign explicit `flightGlobalsIndex`
values — it relies on Kopernicus auto-assignment. The NearStars 1000+
block is therefore a buffer against future explicit assignments by any
add-on, not a collision with v2 as shipped today.

Within each 100-index block, increment by 1 per body. Stars, planets,
moons, and barycenters share the block.

---

## 8. Astronomical Data Sources

All orbital parameters and physical constants must come from real observational data.

- **Orbital data:** NASA JPL Horizons, SIMBAD
- **Exoplanets:** NASA Exoplanet Archive
- **Stellar physics:** SIMBAD Astronomical Database
- Texture sources must be documented in `Credits-License.md`

---

## 9. Development Phases

**Rule: complete one system end-to-end before starting the next.**

### Phase 1 — First system: star skeleton (MVP)
- [ ] Choose pilot system (recommendation: Proxima Centauri)
- [ ] Repository structure setup
- [ ] Star body definition: orbit, ScaledVersion, Properties
- [ ] Icon and localization key skeleton
- [ ] Verify load in Kopernicus (Sol + RSS)

### Phase 2 — First system: planets
- [ ] Planet definitions (atmosphere, PQS, biomes)
- [ ] Verify all bodies load and orbit correctly

### Phase 3 — First system: visuals
- [ ] Texture production (heightmaps, color maps)
- [ ] Parallax terrain and scatters
- [ ] EVE cloud layers for atmospheric bodies
- [ ] Scatterer atmosphere configs

### Phase 4 — First system: polish + expand
- [ ] Science experiment text for all bodies
- [ ] Compatibility patches (Principia, Kerbalism if applicable)
- [ ] Performance pass
- [ ] Begin second system using Phase 1–3 as template

---

## 10. Open Decisions

- [x] Final mod name — settled as `NearStars`
- [ ] Pilot system selection (Proxima Centauri recommended)
- [ ] Inter-stellar distance scaling strategy — real distances are physically impossible in KSP; symbolic compression required. Must be consistent across Sol stock, Sol quarter, and RSS 1:1 scales. Kopernicus hard limit: ~50 ly (see §3.1).
- [x] macOS texture format compatibility strategy — Windows-only mod; BC5/BC7/BC4 DDS usable without restriction
- [ ] RSS EVE version: V3 (free) vs V5 (Patreon) — whether to support both or V5 only like Sol
- [ ] Principia compatibility: requires separate gravity model cfgs per scale variant; Principia-only entries for 50–80 ly stars are possible (no Kopernicus body needed)
- [ ] Sol Quarter scale support — planned, lower priority. `principia-cfg` skill MVP ships Sol Real scale only; Quarter coords are deferred (different `solar_system_epoch` ⇒ separate cfg files).

## Related

- [methodology](methodology.md) — cluster hub; DB-side workflow
- [mod-reference](mod-reference.md) — downstream mods and dependency tiers
- [mod-release-layout](mod-release-layout.md) — repo layout for the mod-release side
- [data-sources](data-sources.md) — citation requirements for external data
- [rex-data-comparison](rex-data-comparison.md) — REX is cited as the spiritual predecessor in §1
