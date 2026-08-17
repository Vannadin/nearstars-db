<!-- 페트로바선 기하와 룩 — 별도 시각화 모드가 소비할 도출 결과와 렌더 -->
# The Petrova line — geometry and look

*Project Hail Mary*'s Petrova line is not a NearStars body, and nothing here reaches a
Kerbalism cfg. It is here because a **separate visualisation mod** will draw it from this
project's API, and because building it was the first real test of whether the machinery
written for [Alfvén wings](planetary-magnetosphere-geometry-methodology.md) generalises
past magnetic geometry. It does: the swept-profile field, the arc-length resampling and the
renderer carried over untouched, and only the path law and the radius law were swapped.

Everything below comes out of `scripts/refs/petrova_line_geometry.py`; the pictures come
out of `scripts/viz/render_petrova_line.py`.

## The shape

[![Petrova line geometry](../img/petrova/petrova-geometry.png)](../img/petrova/petrova-geometry.png)

*Sol to Venus. One continuous curve, 0.726 AU: it leaves along the spin axis, peaks where
the target is easiest to read, and arrives on its bearing.*

The line is **one curve, not three segments**. Two earlier builds banked the turn into a
corner and then into a tangent arc; both localise a turn that the physics spreads, because
the clearance the traveller steers by improves the whole way.

**The knee needs no threshold.** From directly over the pole the target sits *on* the star's
limb — the sight line grazes the photosphere — so it is not separable at all there. Climbing
lifts it off the limb, but it also swings the target toward the downward axis, so the
angular gap

```
gap(H) = arccos(H / √(a² + H²)) − arcsin(R★ / H)
```

is **not monotonic**. It has a maximum, and for a target well outside the star that maximum
sits at the geometric mean of the star's radius and the orbit:

```
H_best = √(R★ · a)
```

12.5 R☉ for Sol and Venus, with 81° of clear sky. The curve is the quadratic Bézier whose
control height is solved to put its apex exactly there, which fixes everything at once: it
leaves along the spin axis, peaks where the target reads best, arrives on its bearing, and
has continuous curvature end to end. No coefficient of its own.

**Aiming is separate from shape.** At light speed the crossing takes six minutes, which
bends the path by 24 arcsec — invisible at any drawing scale. But the light the traveller
navigates by is equally stale, so the aim point leads the *apparent* target by twice the
transit displacement: 2.09 Venus diameters, 48 arcsec.

**The funnel** is tangent to the star at latitude `funnel_tangent_deg` from the pole, a cfg
field, adopted at 60°. Value and slope both match the sphere at the touch point, so the
silhouette flows out of the star with no join to see, and the curve approaches the axis
without reaching it, so there is no apex either. The decay rate is not chosen — tangency
fixes it at `cos φ / (R★ sin² φ)`.

**Do not draw any of this as swept spheres.** Where the radius changes faster than the curve
advances — the funnel drops from 0.87 to 0.06 stellar radii inside one stellar radius —
consecutive spheres swallow one another and the surface becomes the hull of a few large
balls. A floating rim at the pole, a collar with a crease, a dome, a sharp apex: every
artefact chased through this shape was that one cause, and four rounds of profile tuning
were treating symptoms. `sweep_profile_sdf_np` finds the nearest point on the curve first
and only then reads the radius there, so the surface is exactly `ρ = r(s)` however hard the
taper.

## The waist

[![The waist of the Petrova line](../img/petrova/petrova-waist.png)](../img/petrova/petrova-waist.png)

*The thinnest section, at 10.6 R☉ along the run — 6.5% of it — where the funnel has finished
closing and meets the beam. Radius 1,588 km, a quarter of the target's. Both frames true
scale.*

The cross-section is wide at both ends and narrow between: a funnel over the star, this
waist, then a mouth opening again to cover the target's disc. The axis runs to the target's
**centre**, not its surface, so that mouth fills the disc exactly.

## The fill

[![The Petrova line as an aurora curtain](../img/petrova/petrova-aurora-exterior.png)](../img/petrova/petrova-aurora-exterior.png)

*Emission-only volumetric march. Exposure 70 outside; the closer frame runs 1.25× that.*

Surfacing the line was never going to look right. The reference is layered translucent
drapery with stars showing through the thin parts, so the fill is an **emission integral**
through the medium — no surfaces, no lighting — which makes thin parts translucent and
brightens edge-on sheets by itself. The palette is taken off the reference frame, `#a01b28`
through `#dd4a5f`.

The medium is a **sum of folded sheets** rather than a filled tube, which is what makes it
read as drapery. Three things were needed before it stopped looking synthetic:

- **Sheets jittered per index.** Evenly spaced sheets with a phase ramping linearly in index
  read as a comb — the eye finds the period at once. Azimuth, radius, fold frequencies,
  width and brightness are each hashed per sheet, and the fold frequencies are
  incommensurate so the drapery never comes back into step.
- **Sheets at different radii**, so the drapery layers in depth rather than sitting on one
  shell.
- **Fold wavelengths measured in local tube radii**, not absolute arc length. The tube spans
  four orders of magnitude in width, so anything keyed to arc length goes uniform over
  thousands of radii wherever it is thin.

Brightness is per-channel Reinhard rather than a clamp. Clamping at a stop turns everything
above it into one flat slab of that colour; removing the peak instead flattens the
highlights. Rolling off per channel gives a peak that exists and occupies almost no area,
since red saturates first and green and blue only catch up an order of magnitude later — a
wide white region is exactly what reads as clipped SDR.

Dynamic range, not exposure, is what makes room for that peak: the sheets are thin, so rays
crossing one square-on accumulate little while rays grazing one accumulate the same, and the
ratio between filament and background widens instead of the whole frame brightening.

Everything is analytic — a handful of sines and a sine-hash, no textures — because raymarched
volumes do ship in KSP (EVE Volumetrics) and the expression has to survive the move into a
shader. `sheet_ribbons()` is the additive-mesh route out of the same formula, an alternative
rather than a fallback.

## Related

- [`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md)
  — the Alfvén-wing shape family this borrows its machinery from.
- [`tools.md`](tools.md) §14 — the calculators and renderers.
- [`plugins/NearStarsFluxTube`](../../plugins/NearStarsFluxTube/README.md) — the separate
  visualisation mod that will consume this.
