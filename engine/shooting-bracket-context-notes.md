# Shooting bracket — context notes

Decisions taken while making the bracketing search stop reporting its own trial pressures
as physics.

## The bug is that a discarded value escaped wearing a refusal's clothes

`_shoot_pressure` multiplies a trial central pressure by four until the enclosed mass
reaches the target. Every one of those trials except the last is wrong by construction —
that is what a bracketing search is. The defect was that an exception raised inside one of
them left the function.

What makes it hard to see is that the refusal is well-formed. It names a real material, a
real ceiling from a real paper, and a pressure that really was computed. Nothing about the
message looks wrong. Only comparing it against the converged solution shows the gap: the
water preset's refusal cited an ice column base of 3479 GPa where the answer's is 240.6.

The engine already has the rule this violates. Out-of-domain is a returned value carrying
the regime, a machine-written reason, and a grade, generated at the branch that decided it.
A `PhaseGap` from a trial has none of that provenance and inherits the authority of the
ones that do.

## Narrowing is sound because the outer base rises with the centre

Raising the central pressure raises the whole profile, so an outer layer's base rises with
it. That monotonicity is what makes the fix safe: if a layer breaks at trial pressure P,
every pressure above P breaks it worse, so the answer — if there is one — is below P. The
bracket's upper end can be pulled down to the largest pressure that still integrates
without any risk of stepping over a solution.

It also means the refusal is still reachable and still correct. If the narrowed upper end
does not reach the target mass, more pressure is genuinely required and it genuinely breaks
the layer. That case now reports the narrowed state's pressure rather than a trial's, and
names the outer layer rather than borrowing the inner material's ceiling message.

## Why the geometric midpoint

Pressures here span four orders of magnitude between the first trial and the ceiling, so
the arithmetic midpoint would spend most of its iterations in the top decade. The
refinement loop below already works in log space for the same reason. Narrowing stops as
soon as it finds a pressure that both integrates and brackets the target, which is usually
three or four integrations — it is looking for a bracket, not for precision, and the secant
loop that follows does the precision.

## Only the outer layers were ever wrong

`p_ceiling` is the innermost material's `p_max`, and that check stays exactly as it was.
The centre genuinely sits in that material, so a mass whose centre exceeds it genuinely
cannot be solved. The three ceilings measured by `--ceiling` before this change —
`earth_like` 22.78, pure silicate 53.38, pure iron 24.92 — did not move by a digit, which
is the evidence that the inner check was never the problem.

`water` moved from 5.884 to 21.49 M⊕, and it is the only declared composition whose
limiting material is not at the centre. That is why it alone was reported wrongly, and the
ceiling table now carries it beside the other three so the contrast is visible rather than
remembered.

## The regression test targets the mechanism, not the number

This defect surfaced twice — 6.84 M⊕ for silicate in August 2026 and 5.884 M⊕ for water a
day later — and both times it was diagnosed as a wrong number rather than a wrong mechanism.
The first was recorded in a commit message and the ceiling later moved for an unrelated
reason, so nothing was left behind that would catch the second.

So the test asserts that bodies whose *trial* pressures cross an outer ceiling while their
*converged* pressure does not come back solved, and separately that a body which really
does cross it still declines and still names the layer. A test pinned to "water solves at
8 M⊕" would pass again for the wrong reason the next time a ceiling moves.

The old refusal test was doing exactly that in reverse: it asserted 8.0 M⊕ of `water`
declines, which pinned the artifact in place. It now runs at 30 M⊕, where the converged ice
column really does pass 1 TPa.
