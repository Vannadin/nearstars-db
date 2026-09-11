<!-- 층 유동학에서 조석 Love 수(k₂·h₂·l₂)와 소산 Q 를 레올로지 밴드로 내는 방법론 레퍼런스 -->
# Tidal-Response Methodology: Love Numbers and Dissipation from a Layered Body

Method reference for deriving the degree-2 tidal **Love numbers** `k₂`, `h₂`, `l₂` and the
dissipation quality factor `Q` of a layered body from its interior structure and the
**rheology of each layer**, by integrating the viscoelastic propagator of
Beuthe 2015 outward through homogeneous layers and applying the correspondence principle
per rheology.

This recipe exists because `k₂/Q` is the dominant uncertainty in
[tidal-heating-methodology](tidal-heating-methodology.md), and because the two NearStars
bodies that need it today carry a value **fitted to our own output** rather than derived.
It does not fix that: this is an **emitter**. It publishes its own number under its own
name and replaces nothing.

> Citations resolved against NASA ADS (the registered `ADS_API_TOKEN`), not ad-hoc web
> search. Every equation below is cited to a held paper by equation number.

**Scope note.** This doc derives the body's *response* to a tidal potential. How much power
that response dissipates is [tidal-heating](tidal-heating-methodology.md); whether the body
rotates synchronously in the first place is
[tidal-locking-timescale](tidal-locking-timescale-methodology.md). The three are separate
questions and this recipe feeds neither of the other two today.

## Table of Contents

1. [The propagator: six ODEs per homogeneous layer](#1-the-propagator-six-odes-per-homogeneous-layer)
2. [From surface values to Love numbers](#2-from-surface-values-to-love-numbers)
3. [Rheology: three complex compliances, emitted as a band](#3-rheology-three-complex-compliances-emitted-as-a-band)
4. [Fluid layers: what this build does, and where it stops](#4-fluid-layers-what-this-build-does-and-where-it-stops)
5. [Where the layers come from, and what this recipe refuses](#5-where-the-layers-come-from-and-what-this-recipe-refuses)
6. [Anchors: what this recipe is checked against](#6-anchors-what-this-recipe-is-checked-against)
7. [Annotated bibliography](#7-annotated-bibliography)
8. [Related](#related)

---

## Contract — `tidal_response`

**Returns** — `k2` [dimensionless] · `h2` [dimensionless] · `l2` [dimensionless] ·
`q` [dimensionless] · `k2_band` [—] · `h2_band` [—] · `l2_band` [—] · `q_band` [—] ·
`k2_over_q_emitted` [—] · `layer_q` [—] · `rheology_members_emitted` [—] ·
`liquid_layer_treatment` [—] · `static_limit` [—] · `tidal_composition_preset_used` [—] ·
`tidal_composition_preset_name` [—] · `g_surface_identity` [dimensionless] ·
`homogeneous_nmoi` [dimensionless]

⚠ **The four `*_band` keys, the two labels and the two self-checks are Returns, not decoration.** An
earlier draft of this contract listed eight keys while the node emitted seventeen, and it passed only
because **no body runs the node** — the first body to declare a block would have met a checker that had
never seen nine of its values (audit seat, 2026-09-11). *A contract that is right only while nothing
exercises it is not right.*

⚠ **Nothing here is written into `k2_over_q`.** That key stays the body's **declaration**,
which is what `tidal_heating` reads through the C39 seam. The emitted number has its own
name, `k2_over_q_emitted`, so the two can be printed side by side and neither is silently
replaced. *A first build that replaced a fitted value with a derived one would move shipped
verdicts before anyone had checked the derivation.*

⚠ **The Love numbers are a band, not a value.** `k2`, `h2`, `l2` and `q` each carry the
three rheologies' answers (`maxwell`, `andrade`, `sundberg_cooper`) plus `band: [min, max]`.
**No rheology is elected** — that is an owner decision and this recipe does not make it.

⚠ **`tidal_composition_preset_used` and `tidal_composition_preset_name` are values, not
notes**, and they carry this node's prefix on purpose: `mass_radius_relation` already emits
`composition_preset_used`, and the two answer different questions — a screening-radius
composition against a tidal layer-model composition. An unprefixed name would put one key
under two producers, which is the C64 shape.

**Needs** — `radius` [R_earth] · `core_radius` [R_earth] · `mass_earth` [M_earth] ·
`tidal_response` [—] (the per-body declaration block; see §5)

**Declared-optional** — inputs this recipe declares a default for; absent is a normal state,
not a hole. `ocean_thickness` [km] (absent → 0, no ocean layer) · `ice_shell_thickness` [km]
(absent → 0) · `crust_thickness` [km] (absent → 0, no separate crust) ·
`core_mass_fraction` [—] (absent → `interior.COMPOSITIONS[composition_intent]` slot 0, and
the run says so: `tidal_composition_preset_used` is 1) · `ice_mass_fraction` [—] (absent →
the same table's slot 1, the C28 rule) · `composition_intent` [—] (absent → no preset is
reachable and the recipe refuses by name).

**Discriminating keys** — the presence of the `tidal_response` declaration (absent → the
node does not run at all), the per-layer shear modulus and viscosity (absent → named
refusal), and the forcing period.

**Grade** — analog. The propagator and the compliances are the papers'; every material
parameter is either the body's declaration or a named printed table, and the answer is a
band across three rheologies rather than a value.

| regime | condition | what this recipe does | grade |
|---|---|---|---|
| declared | a `tidal_response` block with per-layer μ and η, and a forcing period | integrates the propagator and emits the three-rheology band | analog |
| substitute | μ absent but a printed per-material table is named | same, with `mu_source: material_substitute(<table>)` on every layer that used it | analog |
| partial rheology | Andrade or Sundberg–Cooper parameters absent | emits the members it can and **names** the ones it refused; the band narrows and says so | analog |
| no declaration | no `tidal_response` block | **does not run** — not a refusal, an absence; the node produces no result | — |
| no composition | neither a declared mass fraction nor a usable `composition_intent` preset | refuses by name — `cannot-say (no composition preset)` | — |

---

## 1. The propagator: six ODEs per homogeneous layer

The body is a stack of layers, each with **constant** density ρ, shear modulus μ and
Poisson-type parameters. Within a layer the radial functions `y₁…y₆` — radial and tangential
displacement, the two stresses, the potential perturbation and its gradient — satisfy six
first-order ODEs in radius. Beuthe 2015 prints them as **eqs (13)–(18)**
([`2015Icar..258..239B`](https://ui.adsabs.harvard.edu/abs/2015Icar..258..239B)), the
degree-n form of the Takeuchi & Saito 1972 eq. 82 system.

**Where the integration starts.** Beuthe prints the ODEs but **not** the three solutions regular at
the centre — those live in Takeuchi & Saito 1972 eqs I(98)–I(103), which is paywalled and not held, and
the static solid-layer propagator matrix is likewise deferred to a book this project does not hold
(Appendix F). What closes the chain is **Saito 1974** (held; J-STAGE, installed 2026-09-11 for exactly
this gap — equations read from the page images). In a layer with μ = 0 the potential decouples from
displacement, and Saito's eq. (17) introduces `y₇`, continuous even where the density jumps, so that his
eq. (18) is a **two-variable first-order system in (y₅, y₇)** that can be integrated without knowing the
displacement at all. Its starting values at the centre are printed — eq. (19), `y₅ = rⁿ` and
`r y₇ = 2(n−1) rⁿ` — and at the core-mantle boundary his eq. (20) gives **three independent sets** of
solid-layer starting vectors.

So the chain is: a **liquid** core integrates from the centre by Saito (18)–(19); the core-mantle
boundary supplies three start vectors by Saito (20); Beuthe (13)–(18) carries them through the solid
layers; the surface conditions (eq. 5) fix the combination; eq. (7) reads off the Love numbers.

⚠ **A solid core is refused by name.** Declaring μ > 0 for the innermost layer puts the starting
solutions back in Takeuchi & Saito 1972, which is not held — so the recipe says
`solid core start values live in Takeuchi & Saito 1972 I(98)-I(103), not held` rather than inventing
them. *That is a declaration-decided branch, not a hidden limitation.*

⚠ **Layer-homogeneous is the formalism's native input, not our simplification.** The
propagator is derived for constant (ρ, μ) per layer; feeding it a continuous ρ(r) would be a
different method. So the fact that this recipe uses one density per layer is **not** an
approximation added on top of the paper — but the size of the gap between that stack and the
structure the integrator actually solved **is** a number worth printing, and §6's J9 prints
it.

## 2. From surface values to Love numbers

At the surface the three Love numbers read directly off the integrated solution —
Beuthe 2015 **eq. (7)**:

```
h_n = g · y₁(R)      l_n = g · y₃(R)      k_n = y₅(R) − 1
```

with `g` the surface gravity. This recipe emits **n = 2 only**. Higher degrees are a change
of its own, not a parameter.

`Q` follows from the imaginary part of the complex `k̃₂` — Bagheri+ 2022 §4.3
([`2022AdGeo..63..231B`](https://ui.adsabs.harvard.edu/abs/2022AdGeo..63..231B)) — and
`k2_over_q_emitted` is `|k̃₂|/Q`, emitted as a band across the rheologies.

## 3. Rheology: three complex compliances, emitted as a band

The elastic solution becomes viscoelastic by the correspondence principle: replace μ with
the frequency-dependent `μ̃(ω) = 1/J̃(ω)`, where `J̃` is the complex compliance of the chosen
rheology, evaluated at the **forcing frequency** ω = 2π / `forcing_period_s`.

| rheology | where it is printed | parameters it needs |
|---|---|---|
| Maxwell | Bagheri+ 2022 §2.3 | μ, η |
| Andrade | Bagheri+ 2022 §2.5 eq. 18, `J(t) = J_U + β t^α + t/η`; the Im/Re form in Renaud & Henning 2018 eq. (11) | μ, η, α, ζ |
| Sundberg–Cooper | Bagheri+ 2022 §2.6 | μ, η, plus the anelastic pair (Δ_J, τ) |

⚠ **All three are emitted; none is elected.** Which rheology a body *has* is an owner
decision resting on evidence this recipe does not contain. When a body's declaration lacks
the parameters a member needs, that member is **refused by name** and the others still
publish — a narrower band that says why it is narrow.

## 4. Fluid layers: what this build does, and where it stops

A liquid layer has μ → 0, and this build handles **one** of them: the **core**, by Saito's (y₅, y₇)
propagation from the centre (§1). Everything above it must be solid.

⚠ **An ocean under an ice shell is refused by name, and the reason is not "we did not get to it".**
Two printed facts close that door. First, Beuthe's **eq. (27)**, `k°_n + 1 = h°_n`, is the relation that
holds *"if the fluid layer reaches the surface (surface ocean or quasi-fluid crust)"* — the superscript
marks that **the surface layer of the body behaves as a fluid**. It is not a treatment of a subsurface
ocean; that case is the **membrane approach of his section 3**, with its own effective parameters, and
it is not built here. Second, re-entering a solid layer *above* a fluid needs the analogue of Saito's
eq. (20) at the top of the fluid, and Saito prints those start vectors **only at the core-mantle
boundary**.

So the refusal names both: *the equation cited for a subsurface ocean answers a different question, and
the start vectors for climbing back into a solid do not exist in the held set.* **Today's roster has no
body with an ice mass fraction above zero, so nothing is blocked by this.**

⚠ *An earlier draft of this recipe called the liquid-layer treatment "the membrane limit" and said
Saito 1974 was paywalled and unheld. Saito was downloaded on 2026-09-11 for exactly this gap — the
sentence went stale the same day — and "membrane limit" turned out to name an equation that does not do
what the decision said. Both are recorded rather than quietly corrected.*

**The static limit is the whole body's.** Beuthe prints it as eq. (22) and describes it as *"typically
applied to the whole body [e.g. Wahr et al., 2006]"*. Viscoelasticity enters through the complex μ̃(ω),
not through the ω² inertial terms — so there is **no quasi-static join** between a static core and a
dynamic mantle to assume, because neither is dynamic. Every output carries
`static_limit: static limit applied to the whole body (Beuthe 2015 eq. 22)`. The ω² terms are in the
code exactly as printed, behind a single switch, so turning them on is a measurement someone can make.

## 5. Where the layers come from, and what this recipe refuses

**The layer map is built inside this node.** The structure recipe emits no named layer list,
so the declared layer names are matched to boundary radii by one fixed table:

| declared name | inner radius | outer radius |
|---|---|---|
| `core` | 0 | `core_radius` |
| `mantle` | `core_radius` | **the smallest existing upper boundary** among {crust base, ocean base, surface} |
| `crust` | `radius − crust_thickness` | `radius` |
| `ocean` | `radius − ice_shell_thickness − ocean_thickness` | `radius − ice_shell_thickness` |
| `ice_shell` | `radius − ice_shell_thickness` | `radius` |

⚠ **The mantle's top is a minimum, not "crust base or surface".** The crust boundary is the
rocky primordial-crust slot and is absent on ocean bodies, so the simpler rule would let the
mantle run to the surface and **double-cover** the ocean and ice shell — which the propagator
would integrate twice, with no refusal firing, because every declared name would still have
found a boundary. The stacking order (core → rock → ice → crust → envelope) guarantees the
minimum is always the mantle's top.

⚠ **Two of the boundaries arrive as thicknesses, in kilometres, while the radii are in Earth
radii.** The conversion happens in one place and the test pins it.

After the map is built the node checks that the intervals **cover [0, R] with no gap and no
overlap**. That check exists because an overlap is invisible to every name-based refusal.

**Densities come from declared mass fractions**, not from a density profile — the structure
recipe keeps none that a consumer can read. Each layer's density is
`(fraction × M) / (shell volume)`: the core takes `core_mass_fraction`, the ice column takes
`ice_mass_fraction`, and the rock column takes the remainder. ⚠ *The ocean and the ice shell
share one density in this build* (`ice column homogeneous`); splitting them needs per-layer
masses the structure recipe does not emit, which is a change of its own.

Because the layer masses are the declared fractions, `g(R)` reduces to `G·M/R²`
identically. That identity is checked and **named** `g_surface_identity`, with its scope
stated: it catches gaps, overlaps and fractions that do not sum to one. ⚠ *It cannot say
whether this layer stack matches the structure the integrator solved* — that is what J9
measures instead.

**The refusals this recipe owns, each by name.**

| when | what it says |
|---|---|
| a declared layer has no boundary pair on this body | `layer "X" declared but absent from the solve` |
| the solve has a layer nothing declared | `solve has layer "Y" with no tidal declaration` |
| the ice mass fraction is > 0 but no ice boundary radius exists | `ice column present, no radius boundary` |
| neither a declared mass fraction nor a usable preset | `cannot-say (no composition preset)` |
| the body's composition was reached by inversion | `this body's composition was inverse-solved and is not visible in state` |
| a rheology's parameters are missing | that member is named and the band narrows |

⚠ **A missing mass fraction takes the engine's existing path, it does not invent a second
one.** An undeclared ice fraction reads `interior.COMPOSITIONS[composition_intent]` slot 1 —
the rule the rocky-dynamo recipe already follows — and an undeclared core fraction reads slot
0, which is what the structure integrator itself does. *Refusing here while the integrator
presets silently would give the engine two answers to one question.* The preset's use is
counted in this node's own values, so a `k₂` that rests on a preset says so.

## 6. Anchors: what this recipe is checked against

| # | body | what is compared | source |
|---|---|---|---|
| J1 | Earth, elastic limit | `k₂ = 0.302`, `h₂ = 0.609` (M₂ tide, model **PEM-C**, rotation and ellipticity included) — Wahr 1981 [`1981GeoJ...64..677W`](https://ui.adsabs.harvard.edu/abs/1981GeoJ...64..677W). ⚠ The measured semi-diurnal set Bagheri+ 2022 quotes (`k₂ 0.3531`, `h₂ 0.6072`, `l₂ 0.0843`, `Q ≈ 10`) includes oceans and anelasticity and is **not** the elastic comparison. ⚠ The build must name which Earth model its layers declared — PEM-C against PREM differs at the same order as the threshold | held |
| J2 | Moon | `k₂ = 0.02416 ± 0.00022` (GRAIL, via Bagheri+ 2022 §5.3); monthly `Q ≈ 38` from the **lunar-laser-ranging** lineage, not GRAIL | held, second-hand |
| J3 | Mars | `k₂ = 0.169 ± 0.006` (Konopliv, as printed in the held Bagheri papers); `Q = 95 ± 10` (Khan 2018, for Q only) | held |
| J0 | any body | ⚠ **the strongest wiring check, and both sides of it are printed**: with the core shrunk until the stack is one uniform density, the propagator must reproduce Bagheri+ 2022 eqs (56)(57) for `k̄ₙ` **and** Beuthe's Kelvin–Love form for `h₂`, `(5/2)/(1 + (19/2)μ̂)` with `μ̂ = μ/(ρgR)`. Measured worst difference **3.6e-05** at μ = 1e10 · 5e10 · 1.45e11 Pa. All four pieces — Saito's start vectors, Beuthe's six ODEs, the surface conditions and eq. (7) — have to be right for that to come out. ⚠ *A third line, `love_ratio_identity`, checks the two printed forms against each other (`k̄₂/h₂ = 3/5` in this limit, to 1e-12) — that one is **arithmetic**, since both share the denominator, and it is named so nobody reads it as physics* | held (both forms) |
| J4 | Io | **refused by name** — the held set prints no Io `k₂`; Renaud & Henning 2018 cites Bierson & Nimmo 2016, which is not held | — |
| J5 | Beuthe membrane cases | ⚠ **outside this build, and the reason is printed rather than hidden**: `h₂ = 1.27` / `1.35` are values of the **membrane approximation**, which §4 does not build — eq. (27) applies to a fluid layer reaching the surface, not to the subsurface case these numbers describe. Registered as C62 (c) | held |
| J6 | Dante · Hades · Pandora | the declared `k2_over_q` printed **beside** the emitted one — no verdict, no replacement | declaration |
| J7 | the roster | every body's full solve is **bit-identical** before and after, and the contract checker's class ③/④ baselines and lookup count do not move | gate |
| J8 | the chain | duplicate-producer keys **10 → 9** — the two nodes that both emitted `k2_over_q` become one | `chain.py check` |
| J9 | the approximation's size | the layer-homogeneous stack's `nmoi`, analytic, printed **beside** the structure recipe's `nmoi` as a per-body % difference. ⚠ **Not an equality line** — homogeneous layers approximate ρ(r) and a non-zero difference is expected; the number is how far the propagator's stack sits from the solved structure | report only |

⚠ **J1–J5 report; they do not tune.** No parameter in this recipe is adjusted to close a gap
against an anchor.

## 7. Annotated bibliography

- **Beuthe 2015**, [`2015Icar..258..239B`](https://ui.adsabs.harvard.edu/abs/2015Icar..258..239B)
  — the propagator system (eqs 13–18), the surface Love-number map (eq. 7), the membrane
  limit for fluid layers (eq. 27) and the membrane worked cases. The structural source.
- **Bagheri+ 2022**, [`2022AdGeo..63..231B`](https://ui.adsabs.harvard.edu/abs/2022AdGeo..63..231B)
  — the three rheologies (§2.3, §2.5 eq. 18, §2.6), `Q` from the complex `k̃₂` (§4.3), and
  the Earth / Moon / Mars measured sets it quotes. A review: its anchor values are
  second-hand and labelled so.
- **Renaud & Henning 2018** — the Andrade Im/Re form (eq. 11). ⚠ Prints **no** Io `k₂`; it
  cites Bierson & Nimmo 2016 for that, which is not held.
- **Wahr 1981**, [`1981GeoJ...64..677W`](https://ui.adsabs.harvard.edu/abs/1981GeoJ...64..677W)
  — the elastic solid-Earth Love numbers J1 stands on. ⚠ Its Table 4 prints a similar-looking
  pair for the 1066A model that are the deformation scalars, **not** (h, l, k).
- **Takeuchi & Saito 1972** — the eq. 82 form Beuthe's system descends from, and the source of the
  three centre-regular starting solutions (eqs I(98)–I(103)). **Paywalled and not held**, which is why
  a declared solid core is refused by name rather than started from an invented asymptotic form.
- **Saito 1974**, *Some problems of static deformation of the earth*, J. Phys. Earth 22, 123–140 —
  **held** (J-STAGE, free; installed 2026-09-11 for this gap). ⚠ *Image-heavy: the equations are read
  from the page images, not from a text layer.* §2.3 supplies eq. (17)'s continuous `y₇`, eq. (18)'s
  two-variable liquid-layer system, eq. (19)'s centre starting values and eq. (20)'s three sets of
  solid-layer starting vectors at the core-mantle boundary. Carrying the same treatment through an
  ocean is the registered successor to §4.

## Related

- [tidal-heating-methodology](tidal-heating-methodology.md): what a body *does* with the
  response derived here. ⚠ It reads the **declared** `k2_over_q`, not this recipe's emitted
  value — the seam is deliberate and unchanged.
- [tidal-locking-timescale-methodology](tidal-locking-timescale-methodology.md): whether the
  body is synchronous at all, which this recipe assumes rather than decides.
- [interior-structure-methodology](interior-structure-methodology.md): the layer boundaries
  and mass fractions this recipe reads, and the `nmoi` J9 compares against.
- [methodology-index](methodology-index.md) — the index of all derived-value methodology recipes.
