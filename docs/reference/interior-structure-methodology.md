<!-- 질량·반지름·핵질량분율에서 층 기하와 관성모멘트를 푸는 방법 -->
# Interior structure: layer geometry and moment of inertia

Four recipes were each privately assuming an interior — a core radius for the rocky
dynamo, a normalised moment of inertia for the figure, a k₂/Q for tidal heating, a
conducting phase for the field. None of them said so, and the assumptions did not have to
agree. This document derives the part of that which is a **static structure problem**:
where the core/mantle boundary sits, and what moment of inertia follows.

The thermal question (is the core a conducting liquid?) and the viscoelastic question
(what are k₂ and Q?) are different calculations with different inputs and different
literature. They are separate nodes — `core_state` and `tidal_response` — and neither is
written yet.

## Contract — `interior_layers`

**Returns** — `nmoi` [—] · `core_radius_fraction` [—] · `core_radius` [R_earth]
**Needs** — `mass_earth` [M_earth] · `radius_earth` [R_earth] · `core_mass_fraction` [—] ·
`composition` [—] · `core_density` [kg/m3] · `mantle_density` [kg/m3]
**Discriminating keys** — mean density (≳ 3000 kg/m³ two-layer rock+metal; below that an
ice shell makes it a three-layer body), and core mass fraction (0 < CMF < 1).
**Grade** — analog. The layers are uniform, which is not what a real interior does.

| regime | condition | what this recipe does | grade |
|---|---|---|---|
| rock + metal | ρ̄ ≳ 3000 kg/m³, 0 < CMF < 1 | solves the two-layer geometry and integrates the moment of inertia | analog |
| ice-rich | ρ̄ < 3000 kg/m³ | declines — a thick ice shell over a rock mantle over a metal core is three layers, and a two-layer fit puts the boundary in the wrong place (Ganymede: 0.46 against the measured 0.27) | — |
| undifferentiated | CMF = 0 | declines — no core to place; NMoI is the uniform-sphere 0.4 by inspection | — |
| outside the default table | M < 0.5 or > 2 M⊕ with no densities given | declines — layer densities are pressure-dependent, so the table does not travel; pass `core_density` and `mantle_density` instead | — |
| gas / ice giant | no solid surface | declines — the polytrope regime, not this one | — |

**Out of domain is a returned value.** Each declining row comes back with its reason.

## The law

For a sphere of two uniform layers — a core of radius R_c and density ρ_c inside a mantle
of density ρ_m — mass and moment of inertia are the two integrals

    M = (4/3)π [ ρ_c R_c³ + ρ_m (R³ − R_c³) ]
    I = (8/15)π [ ρ_c R_c⁵ + ρ_m (R⁵ − R_c⁵) ]

Writing f = R_c / R for the core radius fraction and x = M_c / M for the core **mass**
fraction, the first integral inverts in closed form,

    f³ = x ρ_m / [ ρ_c (1 − x) + x ρ_m ]

and the second becomes the normalised moment of inertia

    C / MR²  =  (2/5) [ x f² + (1 − x) (1 − f⁵) / (1 − f³) ]

Both are textbook integrations of a piecewise-constant density profile; no citation is
owed for the algebra. What is owed is the **layer densities**, and those come from the
Preliminary Reference Earth Model (Dziewonski & Anderson 1981,
[`1981PEPI...25..297D`](https://ui.adsabs.harvard.edu/abs/1981PEPI...25..297D)) for
Earth, and from the two-layer iron-core/silicate-mantle grids of Zeng+ 2016
([`2016ApJ...819..127Z`](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z)) for the
parameterisation by core mass fraction.

**Why the moment of inertia is the quantity worth deriving.** It is the one number that
says how centrally condensed a body is, and it is what the figure recipe needs: J₂ follows
from C/MR² through the Radau–Darwin relation, which is why the
[J₂ worked example](principia-geopotential-data.md) starts there. A class-table constant
in that slot propagates into J₂, into the Cassini precession constant, into the obliquity,
and from there into tidal dissipation.

## The recipe

1. Compute the mean density from mass and radius. Below ~3000 kg/m³, stop — the body has
   an ice shell and needs three layers.
2. Take the core mass fraction from `composition_intent`. Earth's is 0.325.
3. Take the layer densities. Pass them in when they are known; the composition table is a
   default that holds only near Earth mass, because layer density is a function of the
   pressure that layer sits under. Mercury's core runs near 7800 kg/m³ where Earth's runs
   near 10900 — the same iron, differently squeezed. Fitting a power law in mass gives an
   exponent that scatters from 0.10 to 0.23 across bodies, so there is no single scaling to
   hide behind: outside 0.5–2 M⊕ the recipe declines rather than guess.
4. Solve `f³ = x ρ_m / [ρ_c(1 − x) + x ρ_m]` for the core radius fraction.
5. Evaluate `C/MR² = (2/5)[x f² + (1 − x)(1 − f⁵)/(1 − f³)]`.
6. Report the fraction, the absolute core radius, and the moment of inertia — with the
   uniform-layer caveat attached, because it is not a small one.

## Validation

Reproduced against published moments of inertia, all of them measured rather than modelled:

| body | C/MR² derived | published | error | f derived | f published |
|---|---|---|---|---|---|
| Earth | 0.3467 | 0.3307 | 4.8 % | 0.549 | 0.546 |
| Mars | 0.3679 | 0.3644 | 1.0 % | 0.526 | 0.540 |
| Mercury | 0.3398 | 0.3460 | 1.8 % | 0.792 | 0.828 |
| Moon | 0.3962 | 0.3931 | 0.8 % | 0.208 | 0.201 |

Sources: Earth from PREM; Mars from Konopliv+ 2011 and InSight; Mercury from Margot+ 2012
(MESSENGER); Moon from Williams+ 2014 (lunar laser ranging).

**The error runs one way, for a physical reason.** Uniform layers ignore self-compression,
and a real interior concentrates mass inward, so the derived C/MR² tends to come out the
larger. Earth is the worst case at 4.8 % because Earth is the most compressed of the four;
the Moon, barely compressed at all, lands within 0.8 %. Read the output as *this value or a
little less*, never as a two-decimal number.

This is a tendency, not an invariant, and the code does not test it as one. Mercury lands
1.8 % **low**, which is what happens when the assumed layer densities are slightly off: the
sign flips before the magnitude does. Anything the sign is asked to prove would really be
proving that the densities were right.

**These anchors test the geometry, not the density table.** All four pass their layer
densities in explicitly, because three of them sit outside the range where the default
table applies. Mixing the two questions would mean never knowing which one failed — and
that is exactly what happened on the first run, where Mercury came back 8.6 % out and the
cause was the table, not the algebra.

**Where it breaks, and how it was found.** Ganymede comes out at 0.346 against a measured
0.3115 — 11 % — and the core fraction at 0.46 against a measured 0.27. Ganymede is not a
two-layer body: it is a metal core under a rock mantle under several hundred kilometres of
ice, and forcing two layers puts the boundary in the wrong place entirely. That failure is
what set the mean-density gate at 3000 kg/m³, which also excludes Callisto (1834 kg/m³) —
whose apparent 2.5 % agreement is a coincidence of partial differentiation, not evidence
the model applies.

## Worked examples

Generated by `engine/test_interior.py`; the table above is regenerated from the same code
that implements the recipe, so it fails if the two drift.

## Related

- [Mass–radius relation](mass-radius-relation-methodology.md) — supplies the radius, and
  currently carries a composition lookup this recipe should eventually replace
- [Body figure](body-figure-methodology.md) — consumes C/MR² for J₂ via Radau–Darwin
- [Principia geopotential data](principia-geopotential-data.md) — the J₂ worked example
- [Rocky-planet dynamo](rocky-planet-dynamo-methodology.md) — consumes the core radius
- [Derivation discipline](derivation-discipline.md) — why the contract block is checked
  against the code
