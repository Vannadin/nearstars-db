# Interior temperature — context notes

Decisions taken while making the solver carry a temperature, and the reasoning behind them.
Appended as the work goes.

## The structure question, answered before any code: **C, and A follows from it**

The brief offered three readings of the relationship between this recipe and
`internal_heat_nontidal`'s `geotherm`. The answer is **(C) they are different quantities
sharing one word**, and once the word is split, **(A) the profile belongs here** follows
without a choice being needed.

**What that document's `geotherm` actually is.** `internal-heat-luminosity-methodology.md`
never derives a temperature profile. Searching its full text for *adiabat*, *Grüneisen*,
*potential temperature* and *K per km* returns nothing. What it produces is `l_int` and
`t_int`, and for a rocky body `t_int ≈ 35 K` — a **heat budget**, not a profile. The word
"geotherm" appears in §5 in prose, once, as the thing that budget *sets*: "The same
radiogenic + secular luminosity sets the geotherm, and the geotherm is what drives the
consequences NearStars actually art-directs." It is handed to two consumers, `dynamo_rocky`
and `heat_transport_mode`, both of which want a thermal state rather than a flux.

**What the equation of state needs is a different object.** `ρ(P, T)` is evaluated inside
the integration loop, at a pressure the loop is in the middle of computing. The temperature
it needs is `T(P)` along the hydrostatic profile. No node that does not integrate the
structure can produce that, because it is a function of the structure. So this is not a
value that could be handed over even in principle.

**So one word covers a scalar budget and a profile.** That is the shape of the failure this
repository already had once, with `magnetosphere` / `magnetopause_standoff_rp` /
`pause_nose` all being one R_mp — except mirrored: there it was one quantity under three
names, here it is two quantities under one name.

**Not (B), and the reason is worth keeping.** An edge `internal_heat_nontidal →
interior_layers` of kind `requires` would promise a number that the producing recipe does
not produce. But the coupling it would express **is real**, and it is the load-bearing one:

> Unterborn+ 2019 §2 sets the boundary condition `T(R) = T_Pot`, the mantle potential
> temperature, and says why it is not the surface temperature: "In reality, a colder,
> conductive layer is likely present at the surface of planets, transitioning to an adiabat
> below a surface boundary layer."

The size of that boundary layer is set by the heat flux, which is exactly what
`internal_heat_nontidal` produces. So the honest record is an `influences` edge carrying
`status: gap` — the chain's existing vocabulary for "this matters and is not modelled" —
rather than a `requires` edge nothing can satisfy.

**What was done about the name.** `geotherm` was left alone: it belongs to another recipe
and renaming it would reach into two edges this task does not own. Instead the outputs added
here are named for what they are, `cmb_temperature` and `core_temperature`, and the
distinction is recorded on the node and in the methodology. A rename of `geotherm` to
something like `interior_heat_budget` is worth doing and is left as a recommendation.

## Why the anchor is a declaration and not the declared surface temperature

The brief's trap 2 says surface temperature must be declared rather than derived. That is
right, and the research turned up a stronger version of it: **the surface temperature is not
the anchor of the interior profile at all.**

In a convecting interior the adiabat's intercept is the potential temperature, and the
surface sits below it across a conductive lid. For Earth the gap is roughly 1300 K: a pure
adiabat run down from 288 K reaches about 600 K at the core-mantle boundary, against a real
value of 2500 to 2800 K (Lay+ 2008, quoted by Unterborn+ 2019). Anchoring on the surface
temperature would not be an approximation, it would be wrong by a factor of four.

So the declared input is `potential_temperature`, which is Unterborn's own boundary
condition, and it sits beside `ice_allowed` and `tidal_heating` as a declaration this recipe
does not derive. Its default is `None`, meaning *not declared*, and that path is byte for
byte the old isothermal one.

## The double-counting defence, and why it is an identity rather than a tolerance

The brief called this the real difficulty and it was. The trap has a precise shape: the two
PREM-derived materials are fits to a measurement of the real, hot Earth, so Earth's geotherm
is already inside their effective ρ₀. Add a 300 K-referenced thermal expansion and Earth is
heated twice — the same arithmetic that took Jupiter's radius from +0.6 % to −9.8 % when
heavy elements were added to a polytrope constant Helled+ 2022 had fitted to a Jupiter that
already has them.

Three routes were on the table. Stripping Earth's geotherm back out of the PREM fit needs a
geotherm we do not have and would discard the calibration that makes Earth work. Swapping to
a cold-isotherm fit for rock means replacing `fe_prem` and `mgsio3_prem`, and those two are
why Earth reproduces to 0.3 % at all. What is left is the differential, and it turns out to
be exact rather than approximate:

- Each phase carries the temperature of the reference its fit sits on. For the lab fits that
  is a constant. For the PREM fits it is **Earth's adiabat**, anchored at Unterborn+ 2019's
  1600 K mantle potential temperature.
- The adiabat `dT/dP = γT/K_S` is **linear in T**, so a family of adiabats is one curve
  scaled by its anchor: `T_ref(P) = T(P)·(1600/T_Pot)`. The reference profile therefore never
  has to be integrated separately, and `ΔT(P) = T(P)·(1 − 1600/T_Pot)` in closed form.
- At `T_Pot = 1600 K` that is identically zero, at every pressure, by algebra. So the test
  asserts `==` rather than a tolerance, and all four anchors return bit-for-bit what they
  returned with temperature switched off.

The cost of the rule is worth naming: `mgsio3_en` is a room-temperature laboratory fit, and
this rule references it to Earth's adiabat along with the two PREM phases. The justification
is that in this stack it is not used as a laboratory isotherm — it is the top of a rocky
column whose 0.3 % agreement with Earth was obtained with it in place, and its own residual
is inside that agreement. Referencing it to 300 K instead would apply a +1300 K correction to
the top of Earth's mantle that the same 0.3 % already excludes. The rule is uniform for the
rock-and-metal column and stated as such rather than being silently per-phase.

## Where the adiabat is checked, and where it is not

The anchor is external on purpose. Unterborn+ 2019 fit their own models' CMB temperature to
a cubic in radius (eq. 7) and give its sensitivity to the anchor (eq. 8), and they compare
their 1 R⊕ value against Lay+ 2008's 2500–2800 K for Earth. Ours lands at **2526 K**, inside
that band and 4.4 % under eq. 7.

It drifts with size: −9.5 % at 2 M⊕, −16.9 % at 4 M⊕. The mechanism is identifiable rather
than mysterious. Holding αK_T volume-independent — which is the whole content of the
Anderson–Goto approximation — makes `γ = (∂P/∂T)_V/(ρ c_V)` fall as 1/ρ exactly, while a
Debye treatment of α(P,T) and C_P(P,T) lets it fall more slowly. So the branch is declared
checked only to 1.05 R⊕, the note names the bias above that, and the grade drops there even
when the density did not move, because the consumer of `cmb_temperature` is `core_state`.

Two smaller residuals, recorded rather than tuned: the sensitivity `dT_CMB/dT_Pot` comes out
1.55 against eq. 8's 1.83, and the core's own adiabat is shallow (2671 K centre against
2526 K at the boundary) because iron's αK₀ is small until the electron term takes over at
high ΔT. The second matters for `core_state` and is worth revisiting when the melting-curve
comparison is built.

## What was not done

`core_state` itself: not implemented, as instructed. What did happen is that its two inputs
now exist, so the two `requires` edges could be declared, and `chain.py needs core_state`
answers 34 where it answered 0. The melting curve is a separate paper.

The ice ladder cross-check turned into the nicest result of the session and deserves a note.
`eos.py` already carried "III 0.11 % · V 0.27 % · VI 1.3 %" as the honest error width of
treating those phases isothermally — numbers measured against SeaFreeze. The thermal term
comes from a completely different constant (αK_T rather than a ρ(P,T) comparison) and
returns 0.107 %, 0.267 % and 1.283 %. Nothing was fitted to make that happen.

## Wiring `core_state`'s output, found while verifying this work

Declaring `core_state`'s two `requires` edges took `chain.py needs core_state` from zero to
34, but `affects core_state` stayed at zero: nothing consumed the node. The reason was one
edge away.

`core_state`'s only declared output is `conductor_phase`, and the edge carrying that
quantity to `dynamo_rocky` named `interior_layers` as its source — bundled together with
`core_radius` in a single `via` list. `interior_layers` does not produce `conductor_phase`
and never did. So the node that exists to answer "can this core drive a dynamo" was written
out of the one place that asks.

The source settles the split. RM22 solves the internal structure for the core radius and
density, then feeds that core into a dynamo scaling driven by "the convective buoyancy flux
through a **conducting liquid-iron core**". Geometry and phase are two questions with two
answers: the geometry edge keeps `interior_layers`, and the phase edge now comes from
`core_state`. `affects core_state` is 31.

This is the same defect the temperature work refused to create when it rejected option (B)
— a `requires` edge promising a number nothing produces — except it was already in the file
rather than about to be added. It is also the same shape as the `nmoi` supplier fixed on
2026-08-26: one quantity, two suppliers, and the wrong one wins because nobody re-reads the
edge.

### Three more like it, not touched

Sweeping every `via` against its source's declared `outputs` gives 35 mismatches, but most
are noise — `outputs` lists are sparse, so the named quantity usually has no declared owner
at all. Only where another node **is** the declared owner is there a real conflict, and
after the fix above three remain:

| edge | `via` | declared owner |
|---|---|---|
| `star_physical → body_figure` | `p_rot` | `spin_axis_inclination` |
| `body_figure → cassini_state` | `radius` | four nodes; `body_figure` emits `reference_radius` |
| `crater_state → hapke_shader_values` | `terrain` | `hapke_shader_values` itself |

None is obviously wrong and each needs a decision rather than an edit. The first two bodies
in one name: a star's own rotation feeding its own figure is legitimate, and so is a
planet's — the collision is that one field name serves both. The third looks like a slip,
`reference_radius` written as `radius`. The fourth is a word doing two jobs, terrain as
input information versus terrain as a shader output.

The general lesson is that `via` is unchecked. Nothing compares it against the source's
`outputs`, which is why this survived. Whether it should be checked is a question about how
complete `outputs` lists are meant to be, and that is a larger call than this fix.
