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
