# Context notes: `body_class`

Why the node looks like this, what was rejected, and what it found. The manual is
[`docs/reference/body-class-methodology.md`](../docs/reference/body-class-methodology.md);
this file is the reasoning that did not belong in a manual.

## The structure question, answered first

`chain.yaml` already declares `mass_radius_relation → body_class (requires, via:
radius_valley)`, and `mass_radius_relation` already runs a valley gate. Three readings were
on the table. The answer is **(C): they are different questions**, and the mechanics of (A)
follow from it.

The valley gate asks *"can I read a radius off the rocky grid here?"* It guards
`mass_radius_relation`'s own domain, which is why it **declines** above the valley rather
than returning a class. A decline is not a classification: "statistically not rocky" does
not say whether the body is a sub-Neptune, an ice giant or a gas giant.

`body_class` asks *"what is this body?"*, and it has to answer for bodies where the valley
gate never runs at all. Alpha Centauri A b is the case in the repository right now: at
0.38 M_J both `mass_radius_relation` and `interior_layers` decline, so the node produces no
values, and an edge declared `via: radius_valley` has nothing to carry. The class still has
to come out, because eight `selects` edges are waiting on it.

So the valley constants stay in `mass_radius.py`, `body_class` **imports** them rather than
holding a second copy, and the edge is honoured in substance: the same band, read for a
different purpose. Branch (B) — moving classification out of `mass_radius_relation` — was
rejected on its own merits before the file-ownership question arose: it would leave that
recipe unable to guard itself.

This is the same shape as the previous node. `internal_heat_nontidal`'s geotherm and
`interior_layers`' T(P) were one word over two quantities; here two questions were about to
be collapsed into one because they share a number.

## `composition_intent` is a gap, and exactly one boundary needs it

Five of the six boundaries are drawn in mass or radius and do not need it. One does.

Gas giant and ice giant are not separated by size — they are separated by **whether most of
the mass is H/He or heavy elements**. Lambrechts & Johansen 2014 make that the definition:
a core that reaches the pebble isolation mass gets a runaway envelope and becomes a gas
giant, one that does not stays core-dominated. Their Fig. 4 caption states it in one line.
So without a declared envelope composition, that boundary is convention, and the recipe says
so rather than picking.

The recipe therefore reads `composition_intent` in one place, and its absence has a visible
cost rather than a silent one.

## Chen & Kipping's three transitions: two are ours, one is not

[1603.08614](https://arxiv.org/abs/1603.08614) fits a broken power law to 316 objects and
infers three transition masses without assuming any of them. Two are boundaries this node
wants:

- T(1) = 2.04 (+0.66/−0.59) M⊕, solid → volatile-enveloped
- T(3) = 0.0800 ± 0.0081 M_sun, the onset of hydrogen burning

T(2) = 0.414 (+0.057/−0.065) M_J is **not** our gas/ice giant line, and their own paper says
why: "Saturn is close to being the largest occurring Neptunian world." Their Neptunian class
runs from Uranus to Saturn. Adopting T(2) would put Saturn — and Alpha Centauri A b at
120 M⊕ — on the ice-giant side, which is the opposite of what every consumer needs. The
transition is real; it is the mass at which self-compression starts flattening the M–R
relation, not a compositional divide.

The same paper carries a second negative result worth keeping. Brown dwarfs show **no**
transition at 13 M_J: "brown dwarfs are merely high-mass members of a continuum of Jovians."
So the deuterium limit is invisible in mass and radius. It is still a boundary here, because
the consumers that branch on it — `interior.py` declining brown dwarfs, `dynamo.py` doing
the same — branch on **thermal history**, not on structure. Two criteria, two consumers.
That is why the ladder reads radius at the bottom and mass at the top.

## Why the two halves of the ladder read different quantities

Below the giants the discriminant is **radius**: the valley is a radius feature, and Rogers
2015's whole argument is that at a given radius you can tell whether there is an envelope.
Above the giants the discriminant is **mass**: fusion thresholds are mass thresholds, and
radius is nearly degenerate there (Chen & Kipping's Jovian power index is −0.04 ± 0.02).

The mass fallback for the rocky boundary exists because half the DB's rocky planets have no
measured radius — `rocky_roster.py` already documents that an "estimated" radius is some
other mass-radius relation's output and feeding it back is circular. So when radius is
absent the node falls to Chen & Kipping's mass break and drops a grade, because a mass alone
does not say whether there is an envelope.

## Rejected

- **A `moon` class.** `BodyState.kind` already carries star / planet / moon, and every one
  of the eight `selects` consumers branches on material physics, not on what the body
  orbits. The recipe deliberately never reads `kind`; that omission *is* the answer to the
  question of whether class means composition or orbit.
- **A `water_world` class.** No consumer names it. `interior.COMPOSITIONS` has a `water`
  entry, but that is a composition, and composition is a separate declared input.
- **A `small_body` class for sub-hydrostatic objects.** Same test: no consumer. Below the
  potato radius the node declines instead, naming `body_figure` — whose J₂ comes from
  Radau–Darwin, which assumes a hydrostatic figure.
- **A `super_earth` class.** It is a region of the rocky class, not a different physics.
  Chen & Kipping put the point sharply: with the solid/volatile break at 2.04 M⊕, "rocky
  Super-Earths can be argued to be a fictional category."
- **Solar-system anchors as boundary values.** The gas/ice giant band was first drawn from
  Uranus and Saturn, then thrown out: validating against the eight anchors while fitting the
  boundary to two of them proves nothing. The published criteria are used instead, and the
  anchors only check them.

## `giant` and `gas_giant` are one class with two spellings

`interior.py` holds `GAS_GIANT_CLASSES = ("giant", "gas_giant")` and `core_state.py` lists
both in `CORELESS_CLASSES`; `dynamo.py` defaults to `"giant"`; `bodies/alpha_centauri_a_b.yaml`
declares `"giant"`. Nothing distinguishes them anywhere.

This is the `base_color` / `base_colour` failure recorded in
[derivation-discipline](../docs/reference/derivation-discipline.md) §7, one file earlier in
its life: a spelling variant admitted to the menu makes the drift legal. The vocabulary
here is six names and `gas_giant` is the canonical one, because it is the spelling that is
unambiguous standing next to `ice_giant`. `giant` is normalised on input, recorded as a
single-entry alias with its reason, and **never emitted**.

The declaration in `bodies/alpha_centauri_a_b.yaml` was left alone. It is an owner decision
and the trap in this work is replacing declarations with derivations.

The cleanup — one spelling in the yaml, and `GAS_GIANT_CLASSES` / `FLUID_CLASSES` moved out
of `interior.py` to sit beside the vocabulary — belongs to whoever closes the ice-giant work,
because it is that file.

## What the anchors found

All eight solar-system bodies classify correctly and none of the boundaries was fitted to
them. Two results came out of running them:

- **Saturn is the discriminating anchor.** It is the only body where a plausible boundary
  choice (Chen & Kipping T(2)) gives the wrong answer, and it is what forced the gas/ice
  giant boundary onto composition and radius instead of mass.
- **Alpha Centauri A b is a Saturn.** At 120 M⊕ and 1.0 R_J it sits in the same place, so
  the declared `giant` is reproduced only because T(2) was rejected.

## Observations, not changed

- `mass_radius.py` sets `VALLEY_HI = 1.8`, and its methodology doc §5 calls ~1.8 R⊕ the
  valley centre. Van Eylen+ 2018's abstract puts the centre at ≈2 R⊕ and Fulton+ 2017's
  measured deficit runs to 2.0 R⊕. The engine's ambiguous band is therefore narrower than
  the measured one, on the confident side. That constant belongs to `mass_radius_relation`,
  so this node imports it and reports rather than edits.
- Ho & Van Eylen 2023 measure the valley's location moving with orbital period
  (∂log R/∂log P = −0.096) and with host mass (+0.231). The band here is fixed, which is
  another reason it is the right place to say "ambiguous" rather than draw a line.
- `dynamo.py` declines above `BD_M_MAX = 70` M_J as "stellar". The hydrogen-burning minimum
  mass is 0.070–0.083 M_sun, i.e. 73–87 M_J, so 70 M_J is a little low. It only affects a
  decline message.
