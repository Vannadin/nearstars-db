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

**Closed-tail requirement (owner, 2026-07-23).** In KSP the pause volume is a
*radiation* region, not a field region: inside it Kerbalism applies a uniform
benefit (GCR shield saturates 0.133 R inside the boundary via
`Lib.Clamp(D / −0.1332f, …)`, plus storm protection and the `Magnetosphere`
virtual biome). An open Shue tail would be an infinite safe corridor. And Shue
is *intrinsically* open — for any `α > 0`, `r` diverges as θ→180° (α < 0.5 only
pinches the radius at infinite distance), so closure must be explicit, not an
α choice. Closing the surface at a finite tail length encodes "influence fades
tailward" with zero extra dose logic — physically defensible too (Earth lobe
field ~10 nT by ~100 R_E, GCR-irrelevant).

**How to close — adopted: the softened Shue (owner iteration, 2026-07-23).**
Two rejected attempts first: a naive CSG cap `max(D_shue, |p−c|−L)` leaves a
crease ring + dome (*amputated*); a teardrop hybrid (Shue dayside + ellipsoid
tail joined at the terminator) is C0 only — a visible slope kink at the join.
The owner required a natural gradient with **no joins anywhere**, which the
softened form delivers as a single analytic C∞ closed curve:

    r(θ) = r0 · [ (1+ε) / (ε + cos^{2m}(θ/2)) ]^{α/m}
    ε    = 1 / ( (L/r0)^{m/α} − 1 )

- `ε → 0` recovers exact Shue (since `2/(1+cosθ) = 1/cos²(θ/2)`).
- `ε > 0` closes the tail at exactly `r(180°) = L`, with `dr/dθ = 0` there
  (rounded tip); smooth everywhere, no crease, no join.
- `m` concentrates the softening tailward. **Fixed in code at m = 2** (dayside
  within ~1% of true Shue on Earth-like numbers: θ=45° −0.1%, flank −1.1%) —
  a shape-tuning constant, not a physics parameter; do NOT expose it in cfg
  (owner, 2026-07-23). Verified numerically 2026-07-23 (viewer + node check).

**Field set (owner-confirmed): `(r0, α, L)` — three orthogonal fields.** α alone
cannot replace `pause_radius`: it is a dimensionless flank/nose ratio (`2^α`) and
needs the scale anchor r0. Legacy mapping (free backward-compat conversion):

| legacy | Shue-native | relation |
|---|---|---|
| `pause_compression` | `pause_alpha` | `α = log₂(comp)` (ROK Earth 1.5 → 0.585 ✓) |
| `pause_radius` | *(derived)* | flank = `r0·2^α`; `r0 = radius/comp` |
| `pause_extension` | `pause_tail` (L) | `L = radius/ext` (ROK Earth → 200 R_E) |
| `pause_height_scale`, `pause_deform` | kept (optional) | compose unchanged |

Caveat: the conversion is shape-faithful for earth-style configs; RSS Jupiter
(comp 1.05 → α 0.07, unphysically spherical dayside) shows giants never used
the comp trick — re-tune α per giant after conversion.

- New `RadiationModel` fields: `pause_shue = true`, `pause_nose` (r0),
  `pause_alpha` (default 0.58), `pause_tail` (L, body radii). Backward
  compatible: absent → legacy sphere path.
- `Pause_func`: radial difference `D = |p| − r(θ)` with the softened form,
  `θ = acos(p.x/|p|)`. Not a true Euclidean SDF, but Kerbalism only uses D for
  the mesh isosurface and the thin boundary band — radial difference suffices.
  `pause_height_scale` still composes.
- Rendering is free: `ParticleMesh` accepts any `dist_func`.
- Storm hook (stretch goal): drive `r0`, `α` from the Shue 98 Dp/Bz fits mapped onto
  storm/CME state.
- Giant-planet variant (stretch goal): plasma-loaded magnetospheres compress
  differently (Joy 2002 Jupiter / Kanani 2010 Saturn) — relevant to Polyphemus
  (Dante mass-loading). Cusp indentation (Lin 2010) only if aurora funnels ship.

## TODO before it ships

- Decide route (local Harmony postfix on `Pause_func` vs upstream PR with cfg parsing).
- Prototype the radial-difference isosurface in the belt-viewer first (cheap parity check).
- Upstream PR: match Kerbalism code style, add cfg docs, test stock+RSS configs unchanged.
- NearStars emit: if adopted, Polyphemus/Pandora pause rows gain `pause_nose`/`pause_alpha`
  directly from the methodology's Chapman–Ferraro nose values (no comp-ratio encoding).

Interactive geometry comparison (compression vs translation vs Shue): the
belt-viewer artifact built 2026-07-23 (`pause_offset` ⚗ slider + Shue overlay).
Pairs with `NearStarsFluxTube` as C#/plugin-tier work (in-house).
