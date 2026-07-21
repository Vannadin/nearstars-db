# 3D Star-Map Viewer — recap + optimization plan

Hand-off doc for a clean session. Self-contained: it recaps what the viewer does and
lays out a prioritized optimization plan to execute + verify.

## Status (2026-07-21) — cross-surface nav + field payload

- **Cross-surface navigation — DONE.** The four doc surfaces (DB `index.html`,
  3D `starmap.html`, `reports.html`, `firefly-colors.html`) now share one nav bar
  linking each other plus the GitHub Wiki. `firefly-colors.html` was orphaned (nothing
  linked in) and is now reachable. Wiki link is top-bar only (owner choice). Injected per
  surface: `index.html` directly, plus the `build_reports_index` / `render_color_visualizer`
  / `starmap_template` generators.
- **Field-layer payload — DONE (partial).** The 1314-star field layer shipped
  `id`/`is_field`/`distance_pc`/`distance_ly`/`beyond_50ly` on every entry, all derivable
  or constant; dropped in the builder and reconstructed in the viewer at load. Field
  494→373 KB, payload 1241→1120 KB, file 1379→1258 KB.
- **Remaining optimization (flagged, not done — riskier viewer surgery):**
  - **Field `components` (~214 KB).** Each field star carries a full component object
    (name=label, rgb=rep_rgb, is_primary=true, offset_au=[0,0,0], radius_rsun=class proxy,
    plus spectype/spec_class/teff_k/vmag_v). Only spectype/spec_class/teff_k are real
    info (shown in the detail panel, line ~1135) and the AU-scale star mesh reads it
    (line ~779). Slimming needs viewer defaults at BOTH paths — do it carefully with a
    browser smoke. Biggest remaining win.
  - **`planets:[]` per field entry (~18 KB)** — droppable if the viewer defaults `c.planets`.
  - **stability 287 KB** — regrew past the 2026-06-16 215 KB (more systems have runs now);
    audit the per-variant cap + stray-float rounding.
- **Verification done this round:** self-check (157→143 clusters, 237 planets), module
  `node --check`, reproducible build (identical md5), dead-link + freshness gates green.
  **Visual browser smoke still recommended** for the field-derive change (1314 markers +
  detail panel + distance gate).

## Status (2026-06-16)
- **P1 — payload — DONE.** Stability series downsampled to ≤100 snapshots/variant
  (`math.ceil(len/100)`), per-row time column dropped (uniform spacing → viewer rebuilds
  `t` from per-variant `t0`/`t_end` once at load, so all downstream indexing is unchanged),
  rounding tightened (e 3dp, angles 2dp), binary/Kepler trajectories downsampled (~154→~110
  pts). Playback increment 0.5→0.25 to keep loop duration constant at half the snapshots.
  Result: **payload 793.5→436.5 KB (−45%), file 882→526 KB (−40%)**; stability 553.6→215.4,
  trajectory 74.0→53.8. Kept the ≥100-snapshot floor deliberately (secular detail), so
  payload lands ~436 not ~400 — held the guardrail over the approximate target.
- **P2 — per-frame cost — DONE** (prior, commit `4d2fda0`): buffer reuse + dirty-skip when paused.
- **P3 — object hygiene:** assessed — no runtime geometry/material churn (all THREE objects
  created once), no leaks; no action needed.
- **P4 — maintainability:** deferred (optional, no behavior change).

Files: `scripts/viz/build_starmap.py` (builder, reads `db/systems/*.json`) +
`scripts/viz/starmap_template.html` (the viewer; 1377 lines inline JS) →
`docs/starmap.html` (self-contained, GitHub-Pages hosted). Rebuild:
`python3 scripts/viz/build_starmap.py`. JS syntax check: extract the module `<script>`
and `node --check`.

## What the viewer does now (features, incl. this session's work)
- Map view: 143 cluster sprites in ICRS (ly), Sol at origin; continuous floating-origin
  zoom into AU system views (host star + planet orbits + disks).
- Sky-true orbital planes via `skyBasis(pos,i,Ω,ω)` (orbit normal in the Sol→star
  line-of-sight frame). Disks rendered as inclined ribbons.
- **Plane fallback** (`hostPlane`): a planet with unmeasured i/Ω uses its host's
  measured-i planets' mean plane, else the disk plane, else face-on (per-host).
- **Stability sim panel**: REBOUND time-series → morphing orbit animation; play/slider;
  **confirmed ⇄ candidates variant toggle** (id-based; planets absent from a variant are
  hidden); **charts** (📈): periapsis–apoapsis band + eccentricity (right axis) +
  inclination, smooth quadratic lines, line-style key, distinct per-planet palette;
  **expand modal** (⤢) for a large chart; mobile tweaks.
- **Stellar spin axes**: gold = measured i★ (+PA for Vega/Fomalhaut), dim blue =
  spin-orbit-alignment assumption; `spinAxisDir(pos,i★,PA)` + re-tilt-the-disk-normal
  fallback. Toggle in the top bar.
- Planet-row click → fly-to; zoom dock shifts clear of the open detail panel.

## Current state (measured 2026-06-15)
- `docs/starmap.html` 902 KB; embedded JSON payload **813 KB**.
- Payload by key: **planets 629 KB (77%)**, components 132 KB, disks 1.6 KB.
  - planets bulk = **stability data: 58 variants × ~200 snapshots = 11,550 rows** of
    `[t,a,e,inc,Ω,ω,f]`.
  - components bulk = binary N-body **trajectories: 19 arrays, 2923 pts**.
- Per-frame hot paths (`tick`→`updateScene`→`updateStability`, every frame):
  - `updateStability` rebuilds each active orbit's `BufferGeometry` from scratch every
    frame — recomputes a 180-segment ellipse and allocates new `Float32BufferAttribute`
    for position+color per rec, **even when paused**.
  - `drawStabChart` / `drawBigChart` repaint the whole canvas every frame when the chart
    / modal is open, **even when paused** (cursor doesn't move).
  - `updateScene` walks all 143 clusters every frame (glow/visibility/labels).

## Optimization plan (prioritized)

### P1 — Payload size (biggest win; target 813 KB → ≤ ~400 KB)
1. **Stability data** (in `build_starmap.load_stability` / `_load_stab_dir`):
   - Downsample to ~100 points per variant (viewer already lerps between snapshots, so
     fewer is fine for the secular shape). Today `step=max(1,len//110)` leaves 200 at 200.
     Lower the cap to ~100, and verify the morph still reads smooth.
   - Drop the per-row time `t`: snapshots are uniform → store `t_end` + count once per
     variant and reconstruct `t` in the viewer. Saves 1 of 7 columns.
   - Round `a` (4dp), `e` (3dp), `inc/Ω/ω/f` (2dp) — already mostly done; audit for
     stray long floats.
   - Expected: ~629 KB → ~250–300 KB.
2. **Trajectories / epicycle** (`build_starmap`): downsample (e.g. ≤120 pts) + round to
   4–5 dp. ~132 KB → ~60 KB.
3. **Global**: round all emitted coordinates/elements to the minimum dp the viewer needs;
   ensure `json.dumps(separators=(',',':'))`-tight (no spaces). Confirm self-check counts
   unchanged.

### P2 — Per-frame rendering cost
1. `updateStability`: **reuse buffers** — preallocate each rec's position/color
   `Float32BufferArray` once (seg+1 length) at registration; each frame write into the
   existing arrays and set `geometry.attributes.position.needsUpdate=true` instead of
   `new Float32BufferAttribute`. Eliminates per-frame allocation/GC.
2. **Skip work when nothing changed**: when `!stabPlaying` and the slider/variant haven't
   moved, skip the orbit recompute and the chart repaint (track a dirty flag). The chart
   especially: repaint only on `stabIdx`/variant/lang change, not every frame.
3. Confirm hidden recs (wrong variant) early-return before any compute (already partly
   done).
4. (Optional) `updateScene` cluster walk: short-circuit per-cluster work when the cluster
   is far/invisible.

### P3 — Object/material hygiene
- Dispose geometries/materials when meshes are rebuilt or a sim is closed (avoid leaks on
  repeated open/close). Audit `closeStability` / variant switches.
- `frustumCulled` only where geometry is host-local (already set on anim lines).

### P4 — Maintainability (optional, no behavior change)
- The template is 1377 lines of inline JS. Keep it a single self-contained file (GitHub
  Pages constraint) but section it with clear banners, hoist pure helpers together, and
  sweep dead code. Do NOT split into modules (would break the single-file hosting model).

## Verification (run after each P-step)
- `build_starmap.py` self-check passes (157 files, 143 clusters, planet counts unchanged).
- Extract module script → `node --check` (syntax).
- Reproducible build: rebuilding twice yields identical `docs/starmap.html` (diff 0).
- Payload size recorded before/after each step (this doc's numbers are the baseline).
- Manual smoke (http.server): map loads; fly into TRAPPIST-1 / Alpha Cen / Fomalhaut;
  open stability sim + charts + expand modal + variant toggle; spin-axis toggle; mobile
  width. Stability morph still smooth after downsample.
- `./scripts/check.sh` green (gate-5 docs/wiki false positive is pre-existing).

## Risks / guardrails
- Downsampling stability too far loses secular detail (e oscillation, ejection onset).
  Keep ≥ ~100 pts and eyeball Barnard/AU Mic candidate runs (the ones with structure).
- Buffer-reuse refactor can silently break orbit rendering — verify TRAPPIST sim visually
  and that variant-hidden planets stay hidden.
- Dropping per-row `t` assumes uniform snapshot spacing — true for current runs; assert it
  in the builder so a non-uniform run fails loudly instead of mis-rendering.

## Scope / non-goals
- No new viewer features here — optimization + cleanup only.
- Keep the single-file, CDN-importmap, GitHub-Pages model.
- DB / pipeline unchanged except the builder's emit (downsampling/rounding).
