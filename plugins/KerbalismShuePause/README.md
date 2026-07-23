# Kerbalism — Shue-model magnetopause (DEFERRED / future feature)

Status: **planned, not implemented.** Locked in as a future candidate on 2026-07-23
(same backlog tier as `NearStarsFluxTube`). No prototype yet — this is the brief.
Delivery route is an open decision: **(a)** NearStars-local Harmony patch, or
**(b)** upstream pull request to `Kerbalism/Kerbalism`.

## What it is

Replace (or extend) Kerbalism's magnetopause shape with the **Shue et al. 1997/98
empirical model** — the standard spacecraft-crossing-fit magnetopause surface:

    r(θ) = r0 · ( 2 / (1 + cos θ) )^α

where `θ` is the angle from the sunward axis, `r0` the subsolar (nose) standoff,
and `α` the tail-flaring parameter (θ=90° flank = `r0·2^α`; `α ≥ 0.5` → open,
ever-flaring tail). Refs: `1997JGR...102.9497S`, `1998JGR...10317691S` (see
`docs/reference/planetary-magnetosphere-geometry-methodology.md`).

## Why (current Kerbalism geometry falls short)

Kerbalism's pause is a **sphere with piecewise x-scaling** (`pause_radius` +
`pause_compression`/`pause_extension`, `Radiation.cs Pause_func`). Compared against
Shue (analysis 2026-07-23, see the belt-viewer artifact):

- nose curvature too blunt (squashed hemisphere ≈ 22.5 R_E vs Shue ~14 R_E, Earth);
- max cross-section pinned at the body plane — real magnetopause is widest tailward;
- tail is a closed spindle, not an open flaring cylinder;
- three coupled fields to fake what Shue does with **two physical ones** (`r0`, `α`).

Bonus: Shue 98 parametrizes `r0`, `α` by solar-wind pressure and IMF Bz — hooking
that to Kerbalism's `solar_cycle`/storm state gives a magnetopause that visibly
**compresses during storms**. That dynamic response is the PR selling point.

## Implementation sketch

- New `RadiationModel` fields: `pause_shue = true`, `pause_nose` (r0), `pause_alpha`
  (default 0.58). Backward compatible: absent → legacy sphere path.
- `Pause_func`: radial difference `D = |p| − r0·(2/(1+cosθ))^α`, `θ = acos(p.x/|p|)`.
  Not a true Euclidean SDF, but Kerbalism only uses D for the mesh isosurface and
  the thin boundary band (`Lib.Clamp(D / −0.1332f, …)`) — radial difference suffices.
  Clamp θ (~150°) or cap r to bound the open tail. `pause_height_scale` still composes.
- Rendering is free: `ParticleMesh` accepts any `dist_func`.
- Storm hook (stretch goal): drive `r0`, `α` from the Shue 98 Dp/Bz fits mapped onto
  storm/CME state.

## TODO before it ships

- Decide route (local Harmony postfix on `Pause_func` vs upstream PR with cfg parsing).
- Prototype the radial-difference isosurface in the belt-viewer first (cheap parity check).
- Upstream PR: match Kerbalism code style, add cfg docs, test stock+RSS configs unchanged.
- NearStars emit: if adopted, Polyphemus/Pandora pause rows gain `pause_nose`/`pause_alpha`
  directly from the methodology's Chapman–Ferraro nose values (no comp-ratio encoding).

Interactive geometry comparison (compression vs translation vs Shue): the
belt-viewer artifact built 2026-07-23 (`pause_offset` ⚗ slider + Shue overlay).
Pairs with `NearStarsFluxTube` as C#/plugin-tier work (in-house).
