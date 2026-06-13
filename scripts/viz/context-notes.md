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
- per-component sub-markers, search box, travel-time readout, proper-motion animation, HZ rings, moons. Planet orbits ARE in v1 (user requested).
