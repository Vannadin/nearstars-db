# C13 — does the fuzzy core account for the moment-of-inertia deficit? — context notes

2026-08-31, Brief 21. The measurement that opened this: the ice giants' C/MR² sits
−24.3 % / −25.3 % under Nettelmann+ 2013's P_Voy values, and −15.8 % / −11.4 % remains
after the radius contribution is stripped (`icegiant-nmoi-context-notes.md`). The fuzzy
core is the candidate whose **sign** matches. Sign is not size (C5(b)'s lesson), so the
brief's order was: bound the non-core terms, bracket with what exists, build only if the
bracket reaches.

## §1 The non-core terms, bounded

1. **Rotation (our sphere does not spin; their planets do).** Two labeled numbers.
   The axial moment of a hydrostatic rotating body exceeds its mean moment by
   (2/3)(C−A)/MR² = (2/3)J₂ (textbook identity, B = A): with NH22 Table 1's measured J₂
   (3510.68 / 3535.94 ×10⁻⁶) that is 0.00234 / 0.00236 in λ, i.e. **1.02 % / 0.98 %** of
   the N13 targets. The overall scale of rotational restructuring is the rotational
   parameter m_rot = ω²R_eq³/GM = **2.95 % / 2.61 %** (derived from NH22 Table 1's mass,
   equatorial radius and period; G, M⊕ textbook). Order percents, not tens of percents.
2. **Rotation period (a spread in the target, not in us).** P_Voy vs P_HAS moves the
   published λ **−3.3 % (Uranus) / +6.0 % (Neptune)** — already recorded in the gate. The
   attribution below is measured against the **P_Voy** target: it is the IAU baseline, the
   normalization-matched N13 value, and the choice both source papers share as their
   default row.
3. **What λ is.** Not a measurement — a value derived from J₂, J₄ and an assumed rotation
   rate through an interior model. Matching 0.230 is agreeing with what the gravity field
   permits, not matching nature; the C13 row says it that way.

Sum of the bounded non-core terms ≲ 7 % against a deficit of 11.4–15.8 %: **a remainder
survives the bounds** and still needs an owner. The bracket was therefore worth running.

## §2 The bracket — and the recipe cannot hold its outer end

Ends as briefed: **A** = the anchor as it is (rock compact at the centre — comparable to
N13's own "rocks confined to the core"); **B** = the same rock mass (0.79 / 1.04 M⊕ =
5.43 % / 6.07 % of the planet) spread uniformly through the H/He envelope as Z
(`envelope_z` = 0.283 / 0.321, no silicate layer), λ computed at both ends.

**End B refuses — not as tuning failure but at stack build.** Full solves die in 1 s
(first refusal: the column's 2416–2550 K sits above the ice-x fit's 1800 K ceiling — the
superionic wedge the recipe declines by name). The decisive diagnostic: a standalone
integration **at the anchors' own convergence points** (P_c 1220 / 1533 GPa, T_c
6160 / 6296 K — hot, fluid) throws PhaseGap at T = 0.0, before any temperature enters:
*"얼음 기둥 바닥이 1220 GPa 로 근거 구간의 상한(1000 GPa) 위다"*. With no silicate layer
the water column extends to the centre, and the **cold-phase pre-check** demands the solid
ladder cover the whole column — French & Redmer 2015's knot span (via SeaFreeze) ends at
1000 GPa. In the anchor configuration the silicate core occupies the deep column and the
ice base stays near/below that line; remove it and the stack cannot be built at ice-giant
central pressures, at any temperature.

So **branch 2's assumption is false, with the cap named**: `envelope_z` exists, but
"nothing in the recipe caps the outer extreme" is wrong — the cap is the solid ladder's
1000 GPa evidence span enforced by the cold-flank pre-check, even though the *answer's*
deep column is fluid (Mazevet) and never touches the ladder there. This is the third
member of one family in two days: C11's over-broad refusal, the Queyroux–Neptune route
death (`queyroux-flip-context-notes.md` §3), and now this — **the trial corridor's cold
flank keeps demanding evidence the answer never uses.**

## §3 The ceiling, computed outside the engine (assumptions labeled)

Since the engine cannot measure end B, the span's ceiling was computed analytically:
moving mass fraction f from the centre to radius R adds at most ΔI = f·MR², so

    Δλ/λ ≤ f_rock/λ_A = 0.0543/0.1741 = **+31.2 %** (Uranus) · 0.0607/0.1799 = **+33.7 %** (Neptune)

against the required **+18.7 % / +12.9 %** (the factors that lift I/(M·R_pub²) = 0.1937 /
0.2135 to the P_Voy targets 0.230 / 0.2410). Assumptions, written per the C12 rule: all
rock at the surface (the envelope actually spans r/R ≈ 0.75–1, so the true end B sits
below this ceiling), and the rest of the structure held fixed (hydrostatic rearrangement
ignored — the real span must be solved, which is what the engine currently cannot do).

Reading: the ceiling **reaches** the requirement, so the fuzzy core **cannot be excluded**
by the bracket — and it is not confirmed either, because the reachable, solvable span was
never measured. Had the ceiling fallen short, the item would have closed negative today.

## §4 How it lands

C13 stays **open**: the bracket did not settle it either way. What settling requires is
now concrete and named — the deep-column representability work (the cold flank must
survive a rock-free centre: e.g. the over-depth ladder refusal routed so the temperature
loop can stay on the fluid side, or the pre-check taught that a column can be fluid-only
where the answer is), after which end B is two solves. Whether that work happens is the
owner's call; it is the same infrastructure the Queyroux adoption would need, so the two
decisions share a prerequisite. Helled & Stevenson 2017's closed form was never reached
(only relevant if building) — its ice-envelope applicability check remains the registered
fourth branch for whoever builds.

C5's revisited line: (a) recorded the graded-Z envelope as *reached, no consumer* — true
when written. **Superseded on the consumer half**: the measured deficit is a consumer now.
The blocker moved: not "nothing would read it" but "the recipe cannot yet hold the
arrangement it would grade toward".

## §5 What did not move

No code, no anchor, no gate change — this item is measurement and documentation only.
Both refusals reproduce in ≤ 1 s (the full solve and the convergence-point integration in
§2; runner preserved at the session scratchpad's `c13_bracket.py`, and the diagnostic is
three lines against the frozen anchor).
