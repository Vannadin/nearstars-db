<!-- 내부구조 솔버를 "끝났다" 고 말하려면 남은 것 — 코어 작업 목록 -->
# Interior solver — the core list

What remains before the interior solver can be called finished. Not a wish list: every
entry here is something **this recipe can close by itself**, and closing all of them is the
definition of done for this tool.

The information was scattered across the methodology document's domain table, six sets of
context notes, and a review file that is now half stale. Asking "what is left" meant
re-reading all three and getting a slightly different answer each time. This is the one
place.

**Order, set by the owner 2026-08-29: C1 first, then down the list in number.** No entry
depends on another, so the numbers are a queue rather than a chain; an entry that closes as
*"recorded, not found"* still closes.

**Keeping this file alive.** C2 was stale within a day of being written. So each brief's
Landing section carries one checkbox — *update the matching row in `interior-core.md`* — and
a row is not closed by the work being done but by that line being written here.

## Where the line is

Not by body class — by **what is missing**.

**In:** the missing thing is a material, a structure, a declaration, or a wire. The recipe
can reach it.

**Out:** the missing thing is physics the hydrostatic integration does not contain, or a
node that already exists elsewhere.

| out of scope | why |
|---|---|
| brown dwarf | deuterium burning above ~13 M_J puts an energy source inside the body. Not an input this recipe lacks — a term the equations do not have |
| star | the stellar C/MR² is the n = 3/2 polytrope value 0.205 (Chandrasekhar 1939), already on a separate `body_figure` branch |
| evolution and cooling tracks | age-dependent envelope thickness and luminosity belong to `internal_heat_nontidal` and to nodes not yet written |
| gate economics | the gate ran 14:12 → 14:22 → 17:44 and the cost was twice *recorded, not repaid*. Not solver physics — but it belongs on **a maintenance list of its own**, written down here only so it cannot fall between the two. Two small fixes ride with it: the conditional `_LAST_INVERSE` line, and a double-cut test for a thin layer |

**Sub-Neptunes are in.** What they lack is a gas mass fraction, which age and irradiation
set — an *input*, not physics. This recipe already takes six such inputs by declaration and
drops its grade for each: `ice_allowed`, `tidal_heating`, `initial_porosity`, `envelope_z`,
`potential_temperature`, `core_cmb_temperature`. A seventh is the same move, not a new
standard.

## The list

### C1 — Sub-Neptunes, and the defect hiding behind them — **closed 2026-08-30**

The sweep (5 M⊕ · CMF 0.20 · 500 K at 1 bar) now solves at 2, 5, 10, 20 and 30 % gas and
declines at 50, 80 and 100 % citing the hottest bound solution and the wall above it —
neither sentence mentions a ceiling. `sub_neptune` is off `FLUID_CLASSES`; `gas_mass_fraction`
is the seventh declaration. GJ 1214 b (8.41 M⊕, 2.733 R⊕) is reproduced by 1.5–2.4 % H/He for
1-bar temperatures of 350–250 K, inside Valencia+ 2013's < 7 % and beside their ~3 % for a
solar-metallicity envelope.

Both measurements were wrong: the 17.7 M⊕ row was the polytrope era's, the "0 M⊕ since the
table" of 2026-08-28 was the same defect as the sweep's refusal (the envelope base cut off as a
surface), and the cap re-measured with the defect fixed is 11.46 M⊕. Under it were three defects, none a ceiling: the
integrator took the envelope base leaving the H/He table's reach line for the 1-bar surface,
so the envelope had no mass; the temperature loop's proportional update diverges when the
1-bar temperature scales faster than the central one (thin envelopes on heavy cores); and a
ladder seed already over the target fell onto the inflated branch of the U-shaped surface-mass
curve. Each fix is gated so that no anchor path enters it, and the bit lines say so.
`engine/sub-neptune-context-notes.md` has the measurements.

Left open, named: a sub-Neptune now integrates but has **no dynamo path** — `core_state`
declines by class, `dynamo_giant` excludes it by mass, `dynamo_rocky` does not take the class.
Recorded as a gap edge in `chain.yaml` (`body_class → dynamo_rocky, via: sub_neptune`); not a
solver item, so it is not on this list.

### C2 — The ocean layer, and multi-axis inversion — **closed 2026-08-29**

Liquid water came from SeaFreeze's `water1`, the phase switch is pinned inside the
integration step the same way layer boundaries are, and `infer_three_layer` returns a band
over the core axis, narrowing only when a measured C/MR² is supplied. Grid phase 2e-3 → 8e-7,
asserted at the gate. Condensed anchors bit-identical; `chain.yaml` cycle 7 declares the
phase → density → temperature loop.

Two of the five icy anchors came inside — Ganymede 2.1 % → 0.4 %, Europa narrowed to a 7 %
core under a 104 km ocean. **The other three moved the question rather than answering it,
which is C10.**

Reasoning: `engine/ocean-layer-context-notes.md`.

### C3 — The melting-curve gap, and dispatch by class

The ice material is chosen by `body_class`, never by the local (P, T) —
`interior.py:960`. Neptune's envelope base landed 3 K under the hot-water fit's floor and
declined until the boundary interpolation moved it above; the dispatch itself is unchanged
and the next body at that boundary will hit it again.

Dispatching by state is right in principle but **1800 K cannot be the switch**: it is the
knot ceiling of a fit, not a phase boundary, and water at those pressures is fluid. IAPWS
equation (5) ends at 715 K (20.6 GPa) and `melt_free_phases()` already names `ice_x` as
carrying no curve at all.

Needs: a melting curve between 20.6 GPa and the superionic field. Then the dispatch can read
the state.

Depends on: nothing. Closing it also settles two domain rows that currently defer to it.

### C4 — Ammonia and methane

The ice-giant envelope is water alone, standing in for a water–ammonia–methane mixture. That
is the field's own convention, but it is a stated substitution and **its price is not
quantified**. Bethkenhagen+ 2017's 2.1 % is the deviation from *mixing three components that
you already have*, not the cost of replacing two of them with the third; the distinction was
corrected once already, in the H/He work, and `eos.py` states it correctly. The number only
comes into existence when C4's tables do.

The 2026-08-27 survey found the blocker: of the three, only water has a form that can be
transcribed; ammonia and methane exist as tables.

Needs: their tables located and baked, the way Chabrier's H/He table was in C6's sibling
work. Or a recorded finding that they are not reachable.

Depends on: nothing.

### C5 — Where the giants' leftovers belong

Two residuals, one question: after the model is run, some radius and some heat are left
over, and **nothing in this recipe owns them.**

**Jupiter, and the diluted core.** The mixture rule carries one homogeneous Z through the
envelope. Post-Juno models favour heavy elements graded inward instead, and the residual
after the homogeneous rule is what that grading would explain. An earlier attempt to place Z
as a compact core failed in the wrong direction and ran into the silicate ceiling; the domain
row records it.

**The ice giants, and a residual that has been ownerless three times.** Uranus comes out
**+5.47 %** with a central temperature of 6 159 K against Scheibe+ 2019's 5 700 K — an 8 %
overshoot in the same direction — and Neptune **+8.97 %**. The ice-giant notes opened the
question *"ice or envelope?"* and left it open; the review of that work marked it ownerless;
this list omitted it. It is written here so that stops. C4 cannot absorb it — an ammonia and
methane mixture is a percent-scale correction and this is nine — and the diluted core above
is a Jupiter frame.

Needs: the residual attributed — a graded-Z envelope for the one, ice-versus-envelope
resolved for the other — or a recorded finding that neither can be attributed with what this
recipe carries.

Depends on: nothing, but only worth reading against C6.

### C6 — Material ceilings

Each material stops where its evidence stops, and each ceiling is a row that declines by
name. They are listed together because they are one kind of work.

| material | ceiling | what is above it |
|---|---|---|
| `h2o` | 1 TPa · 1800 K | ice X above the knot domain; superionic above the temperature |
| `silicate` | 13.5 TPa | Thomas–Fermi–Dirac (electron degeneracy) |
| `fe_prem` · `fe_eps` | 12 · 20.9 TPa | the same |
| `h_he` | 10⁴ GPa in the giant branch | the table's own edge |

Needs: nothing, unless a body the roster wants is refused by one of them. **Each is a
correctly stated limit, not a defect** — the work here is to keep them honest, not to remove
them. Listed so that a future refusal can be traced to its row rather than re-diagnosed.

Depends on: a body that actually hits one.

### C7 — Partial differentiation

`differentiated: false` integrates for rock and metal mixed in one layer, and declines when
ice or gas is present. Ice mixed through rock is neither fully mixed nor fully layered, and
the mixture rule this file carries handles rock and metal only.

Needs: a mixing rule for the ice-bearing case, or a recorded finding that the intermediate
state needs a different treatment than a mixture.

Depends on: nothing.

### C8 — The temperature branch's validated window

The only published check on the adiabat (Unterborn+ 2019 eq. 7) is matched to 4.4 % at
1 R⊕ and drifts to −17 % at 1.46 R⊕, so the grade drops above 1.05 R⊕ even where density
did not move. `core_state` consumes that number, so the drift propagates into a verdict.

Needs: a second published anchor above 1.05 R⊕, or a recorded finding that none exists.

Depends on: nothing.

### C9 — Porosity on a heated body

The compaction relation returns an upper bound on void space, never an estimate, because
melt, differentiation, convection, impacts and tidal heating all remove porosity and
Bierson+ 2019 §2.2 excludes all five. The recipe says so and declines to decide.

Needs: a relation that carries at least one of the five, or a recorded finding that the
bound is the best available answer.

Depends on: nothing. **This one may close as "the bound is the answer"**, which is a
legitimate ending.

### C10 — Lighter rock

Callisto, Titan and Enceladus sit **above** every three-layer band. Every member of a band
lowers C/MR² as the core grows, so a published value above the zero-core end cannot be
reached by any layering at all: the mass is less centrally concentrated than rock over water
allows. The reason is the material, not the structure — the rock must be lighter than the
enstatite-plus-PREM silicate this recipe carries. Hydrated or porous is the published reading
for all three.

**This was investigated and set aside on 2026-08-26 for want of evidence, and the evidence
now exists.** The rocky-planet roster produced no body needing lighter rock — every measured
planet solved on the core axis — so the conclusion then was that a search had no direction.
That survey was of rocky planets; the icy moons say the opposite, three of five, in the same
direction, agreeing with their published readings.

It is also the axis the open Dante / Hades question turns on: one of the two readings there
is that the rock is lighter than this silicate.

Needs: a lighter silicate, grounded — which rock, over which pressure and temperature range,
against what. The direction the 2026-08-26 note said was missing.

Depends on: nothing.

## What closing all of these does not do

It does not make the solver answer every body. Brown dwarfs and stars stay out by the line
above, and each material ceiling stays where its evidence stops. What it does is make every
remaining refusal **one this recipe chose**, with a named mechanism and a citation, rather
than one it fell into.

That is the standard the rest of the engine is held to, and it is what "finished" means
here.

## Related

- [`interior-structure-methodology.md`](../docs/reference/interior-structure-methodology.md)
  — the domain table these entries index
- `engine/*-context-notes.md` — the reasoning behind each closed item
- `engine/coverage-review.md` — a 2026-08-27 snapshot, superseded by this file
