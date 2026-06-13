# 3D Star Map Viewer — Context Notes

Decisions made during the work and the reasoning behind them. Append continuously.

## Coordinate handling
- Source: `derived.icrs_x/y/z_km` (ICRS Cartesian, origin = Solar System Barycenter, so Sol ≈ origin). Frame is ICRS, **not** galactic — grid is labeled "ICRS" to avoid the galactic-plane misread.
- Convert km → ly with `9.460730472580800e12 km/ly` and **bake ly** into the payload. km values (~1e13) would lose precision as float32 on the GPU; ly values are O(1–800) → safe.

## Clustering
- Union-find @ 0.4 ly threshold. Empirically: 157 files → 142 DB clusters; largest intra-cluster gap 0.2205 ly (α Cen↔Proxima), smallest inter-system gap 1.0778 ly (GJ 273↔Procyon). Threshold sits in the empty 0.22–1.08 ly gap → no over/under-merge.
- `binary_orbit_ref` (13 files) + full `binary_orbit` (10 files) give an authoritative grouping signal; builder asserts every ref target shares its spatial cluster (guards future wide systems).

## Color / size
- Teff → RGB: Helland piecewise blackbody-chromaticity approx. Perceptual, **not** a calibrated SED. Slight white-blend at the core for render friendliness. Documented in payload `meta.color_model`.
- Pulsar `psr_j0108_1431` is the only null-Teff star (782 ly) → neutral grey, flagged.
- Marker size: luminosity^0.2 when present (24/157), else spectral-class MS proxy, else min. Markers are billboard proxies, NOT physical radii — noted in legend.

## Solar System
- DB has no Sol entry (it's an external-star DB). Sun + 8 planets hardcoded in the builder from canonical textbook elements (a, e, i, period, radius). Tagged `is_sol` + `sol_data` in meta so it's clearly a reference inject, not DB-derived. This keeps the DB-as-strictly-derived invariant intact (Sol never enters db/systems).

## Multi-scale (planets visible) — user requirement
- ly and AU can't coexist in one float32 scene. Two-mode + origin-rebasing: map view (ly) ↔ system view (AU, host re-centered at origin). Camera fly-in transition.
- Planet orbital coverage: a 222/227, e 204/227, period 224/227, radius 220/227, i only 72/227 → assume coplanar (system local plane) when i is null. Orbit ellipse from a+e analytically.
- Prefer `curated` recommended orbital row when present, else `raw`.

## Output / hosting
- `docs/starmap.html`, committed like other `docs/*.html`. GitHub-Pages hostable (CDN importmap works over https). Serve locally via `python3 -m http.server` for file:// CORS avoidance.

## Reuse
- v2 design tokens inlined from `~/Desktop/NearStars Design System/colors_and_type.v2.css` (glass surfaces, spectral palette O/B/A/F/G/K/M/X, Geist fonts). Spectral palette maps to the legend chips.

## Out of scope (v1)
- search box, travel-time readout, proper-motion animation, HZ rings, moons.

## v2 — continuous zoom + real-size + correct orbits (user follow-ups)
Three follow-up requests reshaped the viewer:
1. **No mode switch — continuous zoom to planets.** Dropped the map/system two-mode split. Single scene with a **floating origin** (`originLy`, rebased to `controls.target` once it drifts > 4000 AU) + `logarithmicDepthBuffer` + tiny near plane (1e-5 AU) + `zoomToCursor`. Scene unit = 1 AU; ly coords × 63241. This spans the ~9-order ly→Earth-radius range without float32 jitter, because the focused system's local coords stay tiny after rebase. Star glow sprites are constant screen size and fade out as you approach (`t` from sysScale-relative distance), revealing the real bodies.
2. **Real sizes.** Stars = `radius_rsun × R_SUN_AU` (0.00465 AU), planets = `radius_rearth × R_EARTH_AU` (4.26e-5 AU). Sub-pixel by design → hence crosshairs.
3. **Crosshairs.** HTML `.xhair` pool, drawn for every body of the active (zoomed-in) cluster, coloured by the body, with a name label. Pooled + only the active cluster's bodies → cheap.
4. **Correct orbits (all elements).** `orbitPoint(a,e,i,Ω,ω,ν)` builds the ellipse with the star at the focus and the perifocal→ICRS 3-1-3 rotation `Rz(Ω)Rx(i)Rz(ω)`; planet placed at true anomaly from M (Kepler-solved) or golden-angle index when M absent. Verified: circular→r=a in-plane, e=0.5→peri 0.5/apo 1.5, i=90°→edge-on ±1. Builder now emits a/e/i/Ω/ω/M per planet (coverage: a 222, e 202, ω 140, i 72, M 96, **Ω only 2/227** → defaults to 0, documented).
5. **Multi-star placement is REAL.** The per-component ICRS coords already encode the epoch separation (α Cen B sits 14.4 AU from A, Proxima 13942 AU) — NOT barycentric-identical as first feared (earlier %.3e print hid it). So components are placed at their measured `offset_au`; planets orbit their actual `host_star`. `placement` counts: 143 primary + 15 astrometric, 0 schematic. The `orbit` field (binary_orbit elements) is emitted as a fallback but currently unused.
Solar System uses real J2000 elements (incl. Ω/ω/M) as a calibration showcase.

## v3 — keyboard movement, phase filter, gravitational binary orbits
1. **WASD / arrow fly.** `applyKeys()` in the loop moves camera+target together along the camera basis (W/S forward, A/D strafe, R/F or Space/Shift up/down, arrows mirror WASD). Speed = `controls.getDistance()*0.03` so it works at every zoom scale; a keypress cancels an in-progress fly. Guarded against typing in inputs; arrows/space `preventDefault` to stop page scroll.
2. **Phase 1–3 filter.** Builder reads `docs/reports-manifest.json` → each component's curation phase (3 if a phase3 report exists, 2 if phase2, else 1); cluster `max_phase` = max over components. Current data: 23 clusters P3, 120 P1, 0 P2-only (every phase2 system is also phase3 — future P2-only systems will appear automatically). Viewer shows P1/P2/P3 toggle chips (with counts) in the legend; `clusterVisible` ANDs `phaseOn[max_phase]`. Sol is `max_phase 3` but always shown (is_sol).
3. **Gravitational binary orbits + past trail.** First cut drew the Keplerian relative ellipse from `binary_orbit` elements (kept as a fallback).

## v4 — real N-body trajectories + calmer movement
- **N-body, not Kepler (user clarified).** The DB stores *distinct* per-component ICRS velocities + masses (α Cen A/B differ by ~9 km/s = the orbital velocity; Sirius, 61 Cyg, etc. likewise) — i.e. a full 6D initial state per star. `nbody_trajectories()` (builder) integrates the system **backward** in time with velocity-Verlet (G=4π² in AU/M☉/yr), in the barycentric frame, and bakes each body's past path (relative to the rep's *current* position, so the trail's index-0 point = the measured offset; verified α Cen B = 14.44 AU both ways). Span ≈ 1.4× the Kepler period of the tightest pair (15–4000 yr); ~150 points/body. No time acceleration — current state + past trajectory only.
- **Honesty guard.** Catalog space-velocities aren't always clean orbital states: 40 Eri A vs the BC pair come out at ~30 km/s relative → unbound, integrating to a 1253 AU runaway. If any body wanders > 5× the tightest separation, `nbody_trajectories` returns None and the viewer falls back to the Keplerian element ellipse, or (no elements) a static measured point. Result: 8 systems get real N-body trails (α Cen, Sirius, Procyon, 61 Cyg, Luhman 16, 70 Oph, η Cas, 55 Cnc); 40 Eri / eps Ind / 36 Oph fall back.
- Viewer draws the trail as a vertex-coloured line fading from near-background (oldest) to the body colour (now); body sits at trail[0]. Lives in `orbitsLines` (zoom-in + Orbits toggle).
- **Movement sensitivity** cut ~6× (keyboard speed 0.03 → 0.005 × distance) per "한참 둔감하게".

## v5 — stellar space-motion trails
User: of the "applies to all bodies?" options, the **bulk space motion** is what they wanted. Added a "공간 운동 / Space motion" toggle: every star draws its **heliocentric linear drift** trail — where it came from, over a look-back time (slider, 5–500 kyr, default 50). Builder emits each cluster's rep velocity (`vel`, km/s ICRS); viewer extrapolates `P0 − V·t` (straight line — galactic-potential curvature is negligible at ≤50 ly over ≤1 Myr). This is bulk galactic drift, **not** an orbit (the icrs velocities are relative to the SSB/Sun rest frame, so the Sun stays at origin and stars stream past). Trail is a colour-fade line (old→now) in a per-node child, map-scale, toggled independently of the orbit trails. Distinct from the N-body orbit trails so the two don't read as the same thing. Barnard's Star (fastest, ~140 km/s) shows the longest trail — a good sanity cue.
