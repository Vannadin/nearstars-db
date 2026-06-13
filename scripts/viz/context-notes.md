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

## v7 — stability animation, selected-body highlight, label-toggle fix
- **Stability orbit animation (REBOUND time-series).** Builder embeds each planet's `[t,a,e]` series from `phase3/stability-sim/results/*_timeseries.csv` (46 planets; body names match DB planet names directly). Info panel gains a "Stability sim ▶" button when the selected cluster has any; it flies in (framing the host + orbit, *not* the wide cluster) and opens a play/scrub panel that **morphs the orbit ellipse over sim time** (a,e interpolated; orientation fixed since the series only stores a,e), with a readout (t / e / periastron) that flags `disruption risk` when q<0.08 AU. Alpha Cen A b is the dramatic one — the *observed* orbit (e=0.4, i_mut=50°) Kozai-pumps e 0.08↔0.998. The morph overrides the normal orbit render while playing (done at the end of `updateScene`).
- **Selected-body highlight.** `selBody` set on click (zoomed-in → nearest crosshair; map → cluster's primary star) and on double-click focus; rendered with a larger accent crosshair (`.xhair.sel`).
- **Bug fix — "all labels" toggle wouldn't turn off.** The per-frame label projection re-showed any existing `labelEl` regardless of intent, overriding `ensureLabels`. Added `cl.labelWanted` (= showAllLabels || sol || confirmed) as the single source of truth; the per-frame block only displays a label when `labelWanted`.

## v8 — precise 3D stability animation (real positions)
The first stability animation morphed an ellipse from a/e with **fixed orientation** (the sim only saved a/e). User wanted the *real* 3D evolution. Extended `phase3/stability-sim/scripts/run.py` to also record `x_au,y_au,z_au` (host-relative) per snapshot, re-ran all 12 systems (REBOUND reinstalled in `.venv`; **keep it — user instruction, don't delete**). The builder now embeds `[t,a,e,x,y,z]` and the viewer draws the **actual 3D path** (growing colour-fade trail + marker at the scrubbed time), so precession + inclination + e-pumping all show. Stable systems re-ran identically (a/e 0/1000 diff, just +xyz). **α Cen needed IAS15**: trace under-estimates the secular EKL instability (e_max only 0.71 even at 100 kyr), so α Cen's viz data is the IAS15 50 kyr observed-orbit run (e_max→1.0, unstable) — matching the dynamics study. Also fixed: "Fly here" was closing the info panel (so the Stability-sim button vanished) — it now stays open.

## v9 — orbit-variant toggle (real data vs game-adjusted) + parallel 1 Myr runs
- **α Cen A b two orbits, toggleable.** The adopted/stable orbit (a=1.6,e=0.1,i16°, IAS15 1 Myr → e_max 0.16, the orbit the game uses) is the default; the observed orbit (e=0.4,i50°, the real JWST-candidate data → Kozai-unstable) is a second variant preserved in `results/_observed/`. Builder emits `stability` as a list of `{id,data}` variants (id ∈ adopted/observed/sim); the viewer's stability panel gets a variant button + an explanatory note (`VAR_INFO`): "adopted = stabilised for the game build" vs "observed = based on real measured data (pre-adjustment)". Single-variant planets (everyone else) show no toggle.
## v10 — hover names + debris-disk rings
- **Hover shows a star's name** even when its persistent label is off: `pointermove` sets `hoverCl`, and a single `#hoverLabel` projects its name at the marker (skipped if the cluster is already labelled). Map-scale only (pick ignores faded glows when zoomed in).
- **Debris disks visualised** for the 7 disk hosts (Fomalhaut, AU Mic, eps Eri, Vega, tau Cet, 61 Vir, HD 69830). Builder reads `db/disks_curated.json` → recommended belts {inner_au, outer_au, inc_deg}; viewer draws an inclined translucent `RingGeometry` per belt around the primary (inc 0 = face-on, 90 = edge-on; AU Mic 89.5° → edge-on, Fomalhaut 65.6° tilted). Colour = star light greyed (no Mie colour in the data). Visible when zoomed into the system; disk outer radius feeds `sysScale`. Fomalhaut (planet retracted) finally has something to see.
- Moon/satellite visualisation (Pandora etc.) deferred — separate task later.

## (sim infra) 1 Myr runs are parallel + resumable (`run_1myr.sh [MAX]`, default now 11): independent systems + single-threaded REBOUND → run concurrently, wall-clock ≈ slowest single (55 Cnc) not the serial sum; re-running skips systems already at 1 Myr. **Keep `.venv`** (rebound) for re-runs. Launch detached with `caffeinate -i` so the Mac doesn't idle-sleep. α Cen excluded (observed ejects; adopted already 1 Myr).

## v6 — N-body for ALL multi-star systems (bound subgroups + element fallback)
User: "모든 다중성계는 nbody 기반으로". Reworked `nbody_trajectories` to split components into **gravitationally bound subgroups** (pairwise specific energy E<0) and integrate each ≥2 group in its *own* barycentric frame. This stops a loosely-attached member whose catalog velocity is unbound (40 Eri A at ~30 km/s vs the B–C pair, which is itself bound at 3.7 km/s) from contaminating the bound pair — previously the whole system was rejected. Result: the bound pairs of 40 Eri (B–C) and eps Ind (Ba–Bb) now integrate as real N-body, where before both fell back entirely.
- **Element fallback** (`kepler_trajectory`): when the catalog state gives no bound pair but a published `binary_orbit` solution exists, the secondary's past path is sampled from the elements (2-body = N-body for N=2). This brings in 36 Oph A–B (e=0.92).
- **Data-limited remainder (honest, not fabricated):** 55 Cnc B is a wide common-proper-motion companion with *no* orbital solution → static. Loose outer members with neither a bound catalog velocity nor an outer-orbit solution stay static: Proxima (marginally bound, P≈547 kyr), 40 Eri A↔BC, eps Ind A↔B, 36 Oph C. These need orbital data the DB intentionally doesn't have (would be fabrication). Every other multi-star component is now N-body/gravitational. Coverage logged in the build.
