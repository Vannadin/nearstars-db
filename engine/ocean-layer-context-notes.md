# The ocean layer — context notes

Decisions taken while letting liquid water into the integration, and the reasoning behind
them. Appended as the work goes.

## The three structure questions, answered before any code

### 1. Where the liquid-water equation of state comes from: **SeaFreeze, `water1`**

The brief's suspicion was right. SeaFreeze v1.1.0, the library the ices III · V · VI and
VII/X were already read from, ships **three** liquid-water representations, and the one
this work needs was on the shelf all along:

| key | source | knot domain | use |
|---|---|---|---|
| `water1` | Bollengier, Brown & Shaw 2019 ([2019JChPh.151e4501B](https://ui.adsabs.harvard.edu/abs/2019JChPh.151e4501B)) | 0 – 2300 MPa · 239 – 501 K | **this work**: the ocean under an ice shell, up to the ice VI ceiling |
| `water2` | Brown 2018 ([2018FlPEq.463...18B](https://ui.adsabs.harvard.edu/abs/2018FlPEq.463...18B)) | 0 – 100 GPa · 240 – 10 000 K | not used: it is the shelf for a liquid column above 2.3 GPa (named in the refusal) |
| `water_IAPWS95` | Wagner & Pruß 2002 | 0.1 – 3×10⁵ MPa · 180 – 20 000 K | not used: same domain as the two above and the ices were read from SeaFreeze, one library for the whole ladder |

`water1` is the natural match. Its 2.3 GPa ceiling is 4 % above the ice VI → VII transition
(2.216 GPa), so it covers exactly the pressure range where the IAPWS melting curve this
recipe already carries (equations 1–4) says liquid and ice exchange, and Bollengier's own
sound-speed measurements go to 700 MPa, which is where the Ganymede-class ocean sits. Both
bibcodes were confirmed on ADS on 2026-08-29; the Journaux+ 2020 SeaFreeze citation is
already in `REFS`. IAPWS-95 would have been the second candidate; it lost only because the
whole water ladder is now read from one library and the cross-checks in
`test_interior.py` run against that same library.

**Three constants are not enough this time, and that was measured before deciding.**
Ices III · V · VI went in as (ρ₀, K₀, K₀′) read at one reference state plus (αK_T, c_V) for
the thermal term, and reproduced SeaFreeze to 0.006–0.118 %. Doing the same for `water1`
(read at 0.1 MPa · 273.15 K, BME3, Anderson–Goto thermal pressure) is **5.3 % off at
2.2 GPa on the 273 K isotherm and 10.6 % at 400 K**; read at 300 K instead it is 3.7 % and
7.1 %. The reason is water's own thermodynamics, not the reading: αK_T runs from −1.3×10⁵
Pa/K at 273 K (the density maximum is at 277 K) to +5.3×10⁶ Pa/K at 2 GPa · 330 K, a change
of sign and forty-fold in magnitude across the ocean regime, and the "αK_T independent of
volume" approximation every other thermal term in `eos.py` rests on is simply false for a
liquid at these pressures. The γ identity the ices satisfy still holds (checked at four
states to five decimals), so the *method* is not the issue, only its inputs' constancy.

So the liquid goes in the way the H/He envelope did: a **baked table** of ρ(P, T) and the
adiabatic gradient (∂lnT/∂lnP)_S from `water1`, generated once by a tool script in the
development venv, with SeaFreeze staying a non-runtime dependency exactly as before. That
is the repository's existing precedent for an equation of state with no closed form
(`hhe_table.py` / `tools/make_hhe_table.py`), and the test that regenerates the table when
SeaFreeze is present and prints SKIP when it is not comes with it.

### 2. Where the phase fraction enters the integrator: **inside the `h2o` material, pinned per step**

`_stack` builds layers by cumulative mass fraction, one material per layer. The ocean is
not a new layer in that sense: it is the same substance as the shell above it and the
high-pressure ice below it, and which of the three a given depth is depends on the local
(P, T) against the melting curve — the decision `_ice_verdict` already makes, after the
fact, from samples. So the answer to "material-internal or layer structure" is
**material-internal**, and the stack is untouched: a body with an ocean still declares
`ice_mass_fraction` and nothing else.

What changes is *when* the decision is made. `phase_at(P)` picks the solid rung at every
Runge–Kutta sub-stage from pressure alone; letting it also look at temperature would flip
the phase between sub-stages of one step, which is the staircase this repository just paid
21× to remove. So the integrator does what it does for layer boundaries and the table floor:

- at the start of each step in the ice column it decides **once** whether the column is
  liquid here (T > T_melt(P), using the material's own melting curve) and pins the
  effective material for the whole step — `H2O` (the solid ladder) or `H2O_LIQUID`;
- it predicts the state at the end of the step and, if the phase would differ there,
  bisects the fraction of the step at which the linearly interpolated (P, T) crosses the
  melting curve, re-takes the RK4 step to that fraction, commits it, and switches for the
  next step. Same code shape as the table-floor stop in `speed-context-notes.md` §11.

The melting curve below 20.6 GPa is the IAPWS one already on the phases; above it there is
no curve and the column stays on the solid ladder with the verdict `undecided`, exactly as
before. A liquid demanded above `water1`'s 2.3 GPa ceiling (a warm column whose ice VII
would melt) is a **refusal by name**: the shelf is `water2` and the refusal says so.

**The existing ladder already has a small staircase of the same kind, and it is recorded,
not fixed.** Measured on Ganymede at the converged central pressure, isothermal, 1499 /
1500 / 1501 steps: surface mass moves by 1.5×10⁻⁵ and radius by 3.4×10⁻⁵ — the Ih → III →
V → VI density jumps sit at whatever RK sub-stage they fall on. The full solve is much
quieter (radius 6×10⁻⁶ across the three grids with a temperature declared) because the
shoot absorbs the mass riser into the central pressure. It is below the 1e-5 line the brief
sets for the *new* boundary and it is out of this task's scope; it is named here so the
next person does not rediscover it as the ocean's fault.

### 3. What the inversion's extra unknown is: **there are two, and neither is the ocean**

The ocean's thickness is **not a free composition parameter**. Once `potential_temperature`
is declared, the melting curve and the adiabat fix where the column is liquid; the caller
does not choose an ocean depth, the physics does, from the declaration. That is the same
place `core_state` stands with `core_cmb_temperature`: the thermal history that sets the
declared number is not in this recipe, so the grade drops to analog whenever the answer
uses it, and every result with an ocean says which declaration it leans on. No new
declaration is added; the existing one now moves density.

What a three-layer body does bring is a **second composition unknown**: an iron core mass
fraction *and* an ice mass fraction, with rock as the remainder. Two observations (mass,
radius) cannot fix two fractions, and the brief's three roads were weighed as follows.

- **Declare one** — the repository's convention, and it stays available: `solve()` with
  both fractions given is the forward problem and nothing changes there. But making the
  inversion *require* a declared core fraction would hide the degeneracy behind a number
  the caller has no basis for.
- **Use C/MR² as a third observation** — right where it exists (every Solar-System moon in
  the anchor table), absent for every exoplanet and every NearStars moon.
- **Return the band and do not narrow** — the standing rule.

The answer is the last two together, because they are one mechanism: `infer_three_layer`
scans the core-fraction axis, solves the ice fraction that reproduces the radius at each
point, and **returns the band** — the family of (core fraction, ice fraction, C/MR²) that all
reproduce mass and radius. That is the whole answer when only mass and radius are known,
and it is what "the engine narrows, it does not pick" means here. When a measured C/MR² is
supplied it is used to **narrow the band to the one member that reproduces it**, and the
result says that it did so on a third observation. The engine never selects a core fraction
on its own.

The published moment of inertia is therefore consumed in two different ways by the two
different tests, and the distinction matters for what the validation claims:

- the **five-moon table** asks whether the published C/MR² lies *inside* the band the model
  can reach from mass and radius — that is the touchstone the brief names ("does it start
  to match"), and it is a fair test because the band is computed without the number;
- the **narrowed inversion** then reads back the composition that C/MR² selects, which is a
  read-back and not a prediction, and is graded accordingly.

## Cost, decided before measuring

A moon solve with a temperature declared costs 3–5 s against 0.3 s isothermal, because the
surface-temperature loop wraps the pressure shoot. A band of seven core-fraction points,
each an ice-fraction bisection of ~12 solves, is therefore 5–7 minutes per moon, which the
default gate cannot carry five times over. The plan: the default `test_interior.py` run
asserts Europa (the one genuinely three-layer body in the table) on a coarse band, and the
five-moon table stays behind `--icy` as it already is. The growth is measured in §"How it
came out", not paid.

Baseline, measured 2026-08-29 before any change (`python3 engine/test_*.py`, wall clock,
run one after another on an otherwise idle machine): `test_interior` 186 s · `test_mixture`
263 s · `test_giant` 223 s · `test_ice_giant` 93 s, 765 s together (the brief's 827 s was a
different day's machine). The after-figures are in §"How it came out".

## What was built, in the order it was found

**The liquid is a table, not three constants** — measured first (above), then baked:
`tools/make_water_table.py` writes `water_table.py` (66 × 93 points, ρ and dT/dP|_S) and
reports its own interpolation error: 1.9×10⁻⁴ in density where an ocean sits (252–360 K),
5.8×10⁻⁴ at the low-pressure, high-temperature corner near the vapour curve where no ocean
is. `eos.py` wraps it as `LiquidWater` (`h2o_liquid`), the same duck-typed shape as the H/He
and hot-water materials: no `p_floor` (the ocean has a P = 0 surface), an own `dtdp_adiabat`
so the integrator reads the published slope instead of assembling one, and three named
refusals (isothermal path, above 2.3 GPa, outside 240–500 K).

**The liquid ceiling is thrown as a temperature refusal.** The first attempt at a warm moon
declined: `shoot()` opens the temperature bracket at twice the declared potential
temperature, and 540 K at the bracket's high trial pressure put the ice VII base above its
melting curve, which demanded liquid at 4.8 GPa. That is not physics, it is the trial
value, and the pressure-narrowing path cannot fix it because lowering the central pressure
does not lower the temperature. Raising it with `temperature_k` set (`too_cold=False`) lets
the existing temperature bracket lower the trial by 1.6× and carry on, which is what the
H/He table's upper wall already did. A body that still hits it at the converged point (a warm
water world) comes back `converged=False` with the surface temperature unmet, and the note
names `water2` as the shelf.

**The per-step decision is closed-form, not an inversion.** Pinning the phase once per step
means one melting-curve question per step of the column, and the first profile put a third
of a warm solve into `water_t_melt`'s 80-iteration bisection (154 000 calls). The decision
does not need the melting temperature, only which side of the curve the point is on, and
within a branch `p_melt(T)` is monotone: `water_liquid_at(p, t)` compares the pressure with
the curve's pressure directly (the retrograde ice Ih branch flips the sign) and answers
outside a branch's temperature range without evaluating anything. Checked against
`t > water_t_melt(p)` at 20 000 random (P, T): zero mismatches. `water_t_melt` itself is
untouched, so every verdict note prints the same numbers as before.

**Anchors, checked rather than asserted.** With the wiring in and the ocean switch on, Earth,
Mars, Mercury and the Moon (isothermal and at 1600 K) and the Ganymede two-layer inversion
are bit-identical to the pre-change dump (`anchors_before.json` / `anchors_after1.json` in the
session scratchpad, every field compared with `==`). The isothermal path never evaluates the
melting curve, and a rock body with a temperature has no `h2o` layer to pin.

## How it came out

**The touchstone.** Five icy moons, the two-layer inversion beside the three-layer band at a
270 K declaration (`test_interior.py --icy`, ~20 min; the same numbers came out of
`scratchpad/bands.py` first):

| moon | two-layer | band (core 0 → 0.45) | published | verdict |
|---|---|---|---|---|
| Ganymede | 0.3179 (+2.1 %) | 0.2836 – 0.3128 | 0.3115 | inside; narrows to core 0.008 · ice 0.421 · ocean 500 km / shell 24 km |
| Europa | 0.3793 (+9.6 %) | 0.2774 – 0.3655 | 0.3460 | inside; narrows to core 0.070 · ice 0.078 · ocean 104 km / shell 26 km |
| Callisto | 0.3158 (−11 %) | 0.2856 – 0.3119 | 0.3549 | above the band |
| Titan | 0.3172 (−7.1 %) | 0.2853 – 0.3126 | 0.3414 | above the band |
| Enceladus | 0.3051 (−8.9 %) | 0.2682 – 0.3008 | 0.3350 | above the band, and no ocean at 270 K (10 MPa column) |

Two of five, up from one, and the sentence for the other three changed: every band's C/MR²
falls as the core grows, so a published value above the zero-core end is unreachable by any
layering — the rock must be lighter than this silicate (hydrated, porous) or partially
differentiated. **"Not enough layers" is gone; "the wrong rock" is what remains**, and the
refusal note in `infer_three_layer` says so. Ganymede is the cleanest demonstration of the
ocean doing the work: at zero core the residual went 2.1 % → 0.4 % because 500 km of liquid
replaced ices III·V·VI, which are denser than the liquid. Europa moved the other way (its
column is ice Ih and liquid, and there the liquid is the denser); what put it inside was the
iron core the single-axis inversion could not express.

**The declaration's leverage, measured on Ganymede.** The band's shape does not depend on the
270 K choice, but its level does: the shell is 24 km at 270 K, and the Ih melting point of
251–273 K bounds what any declaration can do. That is the sentence the grade carries.

**Grid phase at the new boundary** (fixed converged P_c, T_c; 1499 · 1500 · 1501 steps):
Europa-like surface mass 8×10⁻⁷ and radius 8×10⁻⁷; Ganymede-like 1×10⁻⁷. Full solves agree
to 1×10⁻⁷ in radius. With `INTERPOLATE_LAYERS = False` the same three grids scatter by
1.8×10⁻³ in mass and 2×10⁻³ in radius, which is the staircase the brief warned about, and it
is now a gate assertion (< 1e-5).

**The cycle, and its convergence.** Declared as cycle 7 in `chain.yaml` (one node, inside
`interior_layers`) and in the result note: phase → density → temperature → phase. One
integration is causal from the centre out, so the loop closes in the existing surface-
temperature iteration; `converged` already required both the mass shoot (1e-8) and the
surface temperature (1e-3), and every ocean solve above reports `converged=True`.

**Grade.** Any body with an ocean has `potential_temperature` away from 1600 K, so the
existing `thermal_moves` rule already returns analog; the ocean note names the declaration
it leans on, and the three-layer inversion is analog by construction (a read-back).

**What was cut from the methodology doc to keep it at 1595 lines** (it is exactly 1595, from
1595): the two "verdict only" paragraphs became the ocean section; the 2026-08-27 temperature
paragraph and the water-row bracketing story (both revision narrative, on the skill's
do-not-write list); the stale ice VII domain row (it said `eos.py` has no thermal constants
for ice VII, untrue since ice X went in); the porosity-is-not-ice paragraph shortened to its
claim; recipe step 2, which still said the undifferentiated case is refused. The Korean
mirror went 1441 → 1441 after the same cuts plus its own (it had lagged the English by
150 lines before this work and still does).

**Cost, measured** (wall clock, same machine, the after-run partly overlapping other jobs):

| test | before | after | Δ |
|---|---|---|---|
| test_interior | 186 s | 396 s | +210 s: the Europa-like ocean solves (2 × ~8 s), the grid-phase triple, and the two-point Europa band with C/MR² narrowing (~3 min) |
| test_mixture | 263 s | 265 s | +2 s (noise; no ocean path) |
| test_giant | 223 s | 233 s | +10 s (noise; no ocean path) |
| test_ice_giant | 93 s | 99 s | +6 s (noise; bit-identical anchors) |

A warm moon solve itself went from 3–5 s to 6–7 s: the closed-form phase decision pays for
the per-step question, and what remains is the temperature bracket taking one extra bounce
off the liquid ceiling at its 2× first guess. The `--icy` table is ~20 minutes and stays off
the gate. Not repaid, as asked.

**The gate.** `bash scripts/check.sh` all green, 17 min 44 s against the brief's ~14 min
(the +210 s of `test_interior` above; the other three tests are within noise). Recorded, not
repaid.
