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

Note: RSS-Origin v1.x does not support Sol. v2 with Sol support is in development but unreleased. The patch templates in §5.1 are designed to extend cleanly to RSS once RSS support is implemented.

---

## 3. Target Star Systems

### 3.1 Distance limits

| Engine | Max range | Source |
|--------|-----------|--------|
| Kopernicus (rendering + SOI) | ~50 ly | REX developer |
| Principia (gravitational perturber) | ~80 ly | RSS-Origin developer |

Kopernicus bodies beyond ~50 ly risk map-view failures, floating-point glitches in the renderer, or engine crashes. This is a hard constraint — all Kopernicus bodies must be within 50 ly.

Principia registers stars as gravitational perturbers through a separate mechanism that is not subject to KSP's rendering limits. Stars in the 50–80 ly range are therefore candidates for **Principia-only entries** (no Kopernicus body, no visual presence, gravity effect only).

### 3.2 Scope

The current data pipeline covers all confirmed planetary systems and noteworthy stellar systems within 50 ly. This fully covers the Kopernicus range. See the [live DB viewer](https://vannadin.github.io/nearstars-db/) for the current system list and count. A separate Principia-only pass for the 50–80 ly band can be added later if desired.

### 3.3 Development order

**Build one complete system first, then expand.** The first system serves as the template and reference implementation for all subsequent systems. Do not start a second system until the first is fully playable (Phase 1 + Phase 2 complete for that system).

Final system list and selection order are TBD — candidates include Proxima Centauri (nearest, single-star, 2 planets), Barnard's Star (5.96 ly), Alpha Centauri (famous, but triple system complexity), and others.

---

## 4. Mod-release repo conventions

The mod release lives in a **separate repo** (`NearStars-Configs/` + `NearStars-Textures/`), not in `nearstars-db`. Its directory layout, cfg conventions, and texture conventions are documented in [`mod-release-layout.md`](mod-release-layout.md):

- §1 Repository structure
- §2 Config conventions (patch tags, body identifier, star/planet templates, file separation)
- §3 Texture conventions

This document keeps project-level scope (targets, data sources, phases, index allocation) below.

---

## 7. flightGlobalsIndex Allocation

Must not collide with Sol-Configs **or** RSS-Origin. NearStars uses
1000+ with 100 indices per system.

| Range | Owner |
|-------|-------|
| 0–99 | Stock KSP / RealSolarSystem (KSP-RO/RealSolarSystem occupies 1–25, 50, 60, 91–95) |
| 100–199 | Sol-Configs (RSS-Reborn) |
| 1000–1099 | NearStars — first star system (TBD) |
| 1100–1199 | NearStars — second star system (TBD) |
| 1200–1299 | NearStars — third star system (TBD) |
| 1300+ | NearStars — further systems (+100 per system) |

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
