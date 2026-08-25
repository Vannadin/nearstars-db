<!-- 질량·반지름·핵질량분율에서 핵 경계와 관성모멘트를 도출하는 방법(논문 근거) — J₂·다이나모의 입력 -->
# Interior structure grounding: where the core boundary sits and what moment of inertia follows

Method reference for the question underneath the figure and the field: **how centrally
condensed is this body?** The answer is one number, the normalised moment of inertia
C/MR², and it is not measurable for anything outside the Solar System — so it has to be
derived from a layer model, and the model has to say where it stops being trustworthy.

The consumers are the [body figure](body-figure-methodology.md) recipe, which turns C/MR²
into J₂ through Radau–Darwin, and the [rocky-planet dynamo](rocky-planet-dynamo-methodology.md),
which needs the core radius. A class-table constant in this slot propagates into J₂, into
the Cassini precession constant, into obliquity, and from there into tidal dissipation —
which is why it is worth deriving rather than looking up.

This doc covers the **static** half of an interior: geometry and moment of inertia.
Whether the core is a conducting liquid is a thermal question (`core_state`), and what k₂
and Q are is a viscoelastic one (`tidal_response`). Different inputs, different literature,
separate recipes.

## Contract — `interior_layers`

**Returns** — `nmoi` [—] · `core_radius_fraction` [—] · `core_radius` [R_earth]
**Needs** — `mass_earth` [M_earth] · `radius_earth` [R_earth] · `core_mass_fraction` [—] ·
`composition` [—] · `core_density` [kg/m3] · `mantle_density` [kg/m3]
**Discriminating keys** — mean density (the two-layer / three-layer split) and core mass
fraction. Regimes and their numeric conditions are in
[Domain of validity](#domain-of-validity) below.
**Grade** — analog. The layers are uniform, which is not what a real interior does.

## The relation

A body of two uniform layers — a core of radius R_c and density ρ_c inside a mantle of
density ρ_m — has mass and moment of inertia given by two integrals over the same profile:

    M = (4/3)π [ ρ_c R_c³ + ρ_m (R³ − R_c³) ]
    I = (8/15)π [ ρ_c R_c⁵ + ρ_m (R⁵ − R_c⁵) ]

Write **f = R_c / R** for the core radius fraction and **x = M_c / M** for the core *mass*
fraction. The first integral then inverts in closed form,

    f³ = x ρ_m / [ ρ_c (1 − x) + x ρ_m ]

and the second becomes the normalised moment of inertia,

    C / MR²  =  (2/5) [ x f² + (1 − x) (1 − f⁵) / (1 − f³) ]

Both are textbook integrations of a piecewise-constant density profile, so the algebra
owes no citation. What it does owe is the **layer densities** — and those are the part
that does not travel, for the reason in the recipe below.

Two limits are worth holding onto as sanity checks. At x → 0 the expression collapses to
2/5, the uniform sphere, because there is no core to concentrate mass. As x → 1 it
collapses to 2/5 again, for the same reason from the other side. Everything interesting
happens in between, and the deeper the value sits below 0.4, the more mass is hiding in
the middle.

## Practical recipe

1. **Mean density from mass and radius.** Below ~3000 kg/m³, stop: the body carries an ice
   shell and needs three layers, not two.
2. **Core mass fraction** from `composition_intent`. Earth's is 0.325.
3. **Layer densities.** Pass them in when they are known. The composition table below is a
   default that holds only near Earth mass, because layer density is a function of the
   pressure that layer sits under — Mercury's core runs near 7800 kg/m³ where Earth's runs
   near 10900, the same iron differently squeezed. Fitting a power law in mass gives an
   exponent that scatters from 0.10 to 0.23 across bodies, so there is no single scaling to
   hide behind. Outside 0.5–2 M⊕ with no densities supplied, the recipe declines.

   | composition | core ρ | mantle ρ | reading |
   |---|---|---|---|
   | `earth_like` | 10900 | 4500 | iron core, silicate mantle (PREM means) |
   | `iron_rich` | 10500 | 3300 | Mercury-like, large core under a thin mantle |
   | `silicate` | 7000 | 3300 | iron-poor, Moon- and Mars-like |

4. **Solve** `f³ = x ρ_m / [ρ_c(1 − x) + x ρ_m]` for the core radius fraction.
5. **Evaluate** `C/MR² = (2/5)[x f² + (1 − x)(1 − f⁵)/(1 − f³)]`.
6. **Report** the fraction, the absolute core radius, and the moment of inertia, with the
   uniform-layer caveat attached — it is not a small one.

## Validation

Reproduced against four measured moments of inertia. All four come from gravity fields or
precession, not from models, and all four pass their layer densities in explicitly:

| body | C/MR² derived | published | error | f derived | f published |
|---|---|---|---|---|---|
| Earth | 0.3467 | 0.3307 | 4.8 % | 0.549 | 0.546 |
| Mars | 0.3679 | 0.3644 | 1.0 % | 0.526 | 0.540 |
| Mercury | 0.3398 | 0.3460 | 1.8 % | 0.792 | 0.828 |
| Moon | 0.3962 | 0.3931 | 0.8 % | 0.208 | 0.201 |

**The error tends one way, for a physical reason.** Uniform layers ignore
self-compression, and a real interior concentrates mass inward, so the derived C/MR² tends
to come out the larger. Earth is the worst case at 4.8 % because Earth is the most
compressed of the four; the Moon, barely compressed at all, lands within 0.8 %. Read the
output as *this value or a little less*, never as a two-decimal number.

It is a tendency and not an invariant. Mercury lands 1.8 % **low**, which is what happens
when the assumed densities are slightly off — the sign flips well before the magnitude
does, so a test on the sign would really be testing that the densities were right.

**These anchors test the geometry, not the density table**, which is why the densities are
supplied rather than looked up: three of the four sit outside the range where the table
applies. Mixing the two questions makes a failure unattributable, and did — Mercury first
came back 8.6 % out and the cause was the table, not the algebra.

## Domain of validity

| regime | condition | what this recipe does | grade |
|---|---|---|---|
| rock + metal | ρ̄ ≳ 3000 kg/m³, 0 < CMF < 1 | solves the geometry and integrates C/MR² | analog |
| ice-rich | ρ̄ < 3000 kg/m³ | declines — three layers, and two puts the boundary in the wrong place | — |
| undifferentiated | CMF = 0 | declines — no core to place; C/MR² is 2/5 by inspection | — |
| outside the table | 0.5 > M or M > 2 M⊕, densities not supplied | declines — layer density is pressure-dependent and the table does not travel | — |
| gas / ice giant | no solid surface | declines — polytrope regime, not this one | — |

Out of domain is a **returned value**, not an error: each row above comes back with its
reason attached, so a body that cannot be derived says why instead of being extrapolated.

**Where it breaks, and how that was found.** Ganymede comes out at 0.346 against a measured
0.3115 — 11 % — with the core boundary at 0.46 against a measured 0.27. Ganymede is metal
under rock under several hundred kilometres of ice, and forcing two layers *misplaces* the
boundary rather than misestimating it. That failure set the mean-density gate at
3000 kg/m³, which also excludes Callisto at 1834 kg/m³ — whose apparent 2.5 % agreement is
a coincidence of partial differentiation, not evidence that the model applies.

## Worked example: Pandora (Alpha Centauri A b III)

The board fixes 0.6447 M⊕ and 5724 km (0.8984 R⊕), which is a mean density of
4890 kg/m³ — comfortably rock-and-metal, and inside the mass range where the default
`earth_like` table applies. At CMF 0.325:

    f³ = 0.325 × 4500 / (10900 × 0.675 + 0.325 × 4500) = 0.1658
    f   = 0.549                    → core radius 3145 km
    C/MR² = (2/5)[0.325 × 0.301 + 0.675 × 0.950 / 0.835] = 0.3467

So Pandora is Earth-like in its degree of central condensation, which is the expected
answer for an Earth-like composition and no surprise — the value of running it is that the
number now carries its inputs, its regime and its 5 % caveat instead of arriving as a
class constant.

## Citations

- **Dziewonski, A. M. & Anderson, D. L. 1981**, PEPI 25, 297
  ([`1981PEPI...25..297D`](https://ui.adsabs.harvard.edu/abs/1981PEPI...25..297D)).
  The Preliminary Reference Earth Model. Source of the Earth layer densities, and of the
  measured C/MR² = 0.3307 the recipe is anchored against.
- **Zeng, L., Sasselov, D. D. & Jacobsen, S. B. 2016**, ApJ 819, 127
  ([`2016ApJ...819..127Z`](https://ui.adsabs.harvard.edu/abs/2016ApJ...819..127Z)).
  Two-layer iron-core/silicate-mantle grids parameterised by core mass fraction — the
  parameterisation this recipe adopts.
- Moment-of-inertia anchors: Mars from Konopliv+ 2011 and InSight; Mercury from Margot+
  2012 (MESSENGER radar); Moon from Williams+ 2014 (lunar laser ranging); Ganymede and
  Callisto from Anderson+ 1996 and 2001 (Galileo gravity).

## Related

- [Mass–radius relation](mass-radius-relation-methodology.md) — supplies the radius, and
  carries a composition lookup this recipe should eventually replace
- [Body figure](body-figure-methodology.md) — turns C/MR² into J₂ via Radau–Darwin
- [Principia geopotential data](principia-geopotential-data.md) — the J₂ worked example
- [Rocky-planet dynamo](rocky-planet-dynamo-methodology.md) — consumes the core radius
- [Derivation discipline](derivation-discipline.md) — why the contract block is checked
  against the code

<!-- Validation table regenerated by `python3 engine/test_interior.py --table`. -->
