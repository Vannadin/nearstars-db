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

## Scope addition — a size for the deformation (owner, 2026-08-04)

Kerbalism's `*_deform` adds `sin(x·5)·sin(y·7)·sin(z·6)·A` to the signed distance. Because
it depends on all three coordinates separately it is the engine's **only** non-axisymmetric
knob, and ROKerbalism uses it exactly that way: the `mercury` model and the one literally
named `irregular` both carry `pause_deform = 0.1`, with `metallic` / `solidiron` / `anomaly`
at 0.04-0.1. So the mod already expresses "this field is not a clean dipole" through deform.

**What is missing is a scale.** The wavenumbers 5/7/6 are hardcoded, so the *amplitude* of
the lumpiness is tunable but its *size* is not. At a Mercury-like standoff of 1.54 body radii
those wavenumbers put 8 to 11 lobes around the boundary, which is far finer than the
multipolar fields we actually derive: a dynamo with power out to spherical-harmonic degree
l = 4 wants about 4 lobes, i.e. wavenumbers near 2.6, a scale factor of ~0.52 against stock.

So this plugin should carry a second geometry feature alongside the Shue surface:

- **`pause_deform_scale`** (and the belt equivalents `inner_deform_scale` /
  `outer_deform_scale`), a multiplier on the hardcoded wavenumbers. `1.0` reproduces stock
  exactly, so every shipped cfg is unaffected.
- Derivation of the value belongs with the field geometry, not with art: it follows from the
  dominant harmonic degree, `k = l / R_mp`, scale factor `= k / 5`.
- Composing with Shue: the deformation rides *on* the Shue surface rather than on the sphere,
  so the two features are orthogonal and the scale term keeps its meaning.

**Already prepared on our side** (so the plugin only has to read it):

| Where | State |
|---|---|
| `scripts/viz/belt_viewer_template.html` | `*_deform_scale` sliders + 2D SDF + 3D raymarch all honour it; cfg export writes it as a `⚗` comment, never a cfg line |
| `scripts/viz/build_belt_viewer.py` | passes a board's `pause_deform` and `pause_deform_scale` into the preset |
| `scripts/pipeline/emit_kerbalism_radiation.py` | `pause_deform` is a real emitted key; `pause_deform_scale` sits in `PENDING_MODEL_KEYS` and is deliberately **not** written to cfg |
| Phase 4 boards | may carry the value with an explicit unused marker, so the number is derived once and waits |

Until the plugin lands, a board's scale value is documentation: the geometry is derived and
recorded, and stock renders the stock lumpiness.

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

    r(θ) = r0 · [ (1+ε) / (ε + cos²(θ/2)) ]^α
    ε    = 1 / ( (L/r0)^{1/α} − 1 )

- `ε → 0` recovers exact Shue (since `2/(1+cosθ) = 1/cos²(θ/2)`).
- `ε > 0` closes the tail at exactly `r(180°) = L`, with `dr/dθ = 0` there
  (rounded tip); smooth everywhere, no crease, no join.
- **Taper fixed at m = 1** (owner, 2026-07-23): the generalized form carried a
  tail-concentration exponent `m` (`cos^{2m}`, `α/m`); it is pinned to the base
  form `m = 1` — no extra taper, no knob, not a cfg field. (An initial "zero
  taper" was corrected to 1: `m = 0` degenerates to a sphere, so the base
  no-extra-taper form is `m = 1`.) Cost is nil at game-scale tails: with L
  linked to the Kerbalism tail (Earth L = 200 R_E), dayside deviation from true
  Shue is ≤0.33% at the flank (verified 2026-07-23).

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
