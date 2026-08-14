# Context notes — belt asymmetry derivation (2026-08-13)

## Why this started

The gradient re-derivation pass produced a comparison figure, and the owner spotted that
Proxima d's belts render symmetric. They do: the board carries `comp 1.01 / ext 1.0`,
copied wholesale from the Earth preset. That is defensible for Earth-like bodies (belts
sit deep inside the standoff) but Proxima d orbits at 0.029 AU, its nose is 7 R_p, and
its outer belt reaches 5 R_p — 70 % of the standoff. Inheriting Earth's numbers there is
inheritance, not grounding.

## Why `(r/R_mp)³` and not something else

The weight has to be the external-to-internal field ratio, and the Chapman–Ferraro
boundary currents contribute a roughly uniform inner field of order the dipole's own
field *at the boundary* — which is the same statement as the `f ≈ 2` doubling Part A
already uses for the standoff. Dipole field falls as r⁻³, so the ratio at radius r is
`(r/R_mp)³`. That makes the recipe consistent with Part A instead of introducing a second,
unrelated assumption. Both limits are then correct by construction: symmetric deep inside,
boundary-shaped at the boundary.

## The evaluation-point decision

Core circle (`dist/√deform_xy`), not the outer edge. Kerbalism applies one x-scale per
shell; the core carries the dose peak and the shell's characteristic L, so it is the
shell average. Using the edge would over-distort the whole shell to match its worst point
(Earth outer: ε 0.35 at the edge vs 0.05 at the core). The edge value is still worth
printing as the upper bound, because it is a readable measure of how much the
one-scale-per-shell design costs.

## What the validation actually proved

Ganymede is the load-bearing one: the recipe returns 1.052 against ROKerbalism's shipped
1.05, and nothing in the derivation knew that number. Earth's inner belt comes out 1.001
against a shipped 1.01 — also right. The disagreements are the informative part: the
giants ship 1.05 / 0.9 where the recipe says 1.000, because their belts sit at a few
percent of the standoff. So those shipped values are art, and we now know it.

## Paper currency (the owner asked)

Mead 1964 looked suspiciously old, so it was checked rather than assumed: `citations()`
sorted by date shows 2024–2026 papers still citing it, and for the *description* of the
CF deformation it is the canonical reference. Its quantitative coefficients, though, were
superseded by the Tsyganenko family; T02 is named in the doc as the escalation route.
Same pass replaced the loose "AP9" mention with Ginet 2013 (AE9/AP9's own paper).
General rule extracted: separate the **mechanism** citation (old is fine, physics does
not rot) from the **numbers** citation (always check for a successor model).

## Not done

The derived values are not in the boards yet — belt geometry's single source of truth is
`render_belts_bodies.py` `*_phys` plus the phase4 rows, and changing either is a visible
change to a gated row. Waiting on the owner, together with the gradient values from the
previous pass.

## Induced-boundary shape function — three wrong answers before the right one (2026-08-14)

Venus and Mars have no dynamo, so their boundary is an induced one, and it needed a shape
function for the overlay. The sequence, recorded because each step looked correct at the time.

1. **Shue with a softened closure.** Rejected: Shue's single α sets the terminator width
   (`r₀·2^α`) *and* the tail behaviour (`ρ ∝ u^(1−2α)`, cylindrical at exactly α = 0.5).
   Venus needs a tight waist plus a widening tail, which no single α provides.
2. **Two-α Shue** (α_day, α_night blended at 90°). Worked visually, but invented a knob, and
   α_night was picked to suppress a mid-tail bulge — a criterion with no measurement behind it.
3. **Conic section.** Adopted on the strength of "this is the form the literature fits".
   True, but for the **bow shock**, not the boundary. Three failures: a conic through nose and
   terminator overshoots the tail (5.05 vs 3.15 R_V at −20); forced closed as an ellipse it
   bulges to 1.5–1.8× the terminator width at the ellipse centre, which is pure geometry
   (max half-width = semi-minor axis `b`) sited where no crossings exist; and at Venus it dips
   to 0.9745 R_V, below the surface. The owner caught both the bulge and the surface breach.
4. **Circle + cone** — what Martinecz 2009 actually published for the IMB, "a circle on the
   dayside and a straight line on the nightside", validated unchanged to ≥20 R_V by Edberg
   2024 (arXiv 2410.21856). No invented parameters, and the circle cannot pierce a nose that
   is above the surface.

The methodological lesson, worth generalising: **step 3 failed because a fitted form was
lifted across boundaries.** "The literature fits conics at Venus" was true of a different
surface. Before adopting a functional form, check which boundary it was fitted to — the
answer was one sentence away in the same paper (Edberg §1: conics for the BS, circle+line
for the IMB).

Second lesson: **an invented constraint is worse than a missing one.** The ellipse only
appeared because a tail closure at 11 R_V was fed in as if measured; that single fabricated
number forced `e` < 1 and produced every downstream defect. The real state of knowledge is
that the boundary does not close within the observed domain, and the engine's closure is
declared as an engine requirement instead.

Currency check that settled Mars: Vignes 2000's own abstract calls the nightside MPB "highly
variable", and Němec 2020 says MAVEN-era models are "unreliable beyond the terminator". So
Mars' nightside is Venus' flare scaled by terminator radius, justified by a Phobos-2 / PVO
comparison finding no structural difference between the two tails — labelled an analogy.
It passes one check nobody designed for: dayside circle slope 0.135 vs cone 0.131 at the
terminator, smooth to 3%.
