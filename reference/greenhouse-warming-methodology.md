<!-- 임의 기체 조합의 온실 상승폭(T_surf − T_eq)을 4개 층으로 도출하는 방법(논문 근거) -->
# Greenhouse warming grounding: four layers from any gas mixture to a surface temperature

Method reference for the **greenhouse temperature increment**

    ΔT_gh  =  T_surface  −  T_eq

of a body with an atmosphere, for an arbitrary gas mixture. Equilibrium temperature is a
closed-form textbook quantity; the *increment* is not. It is the output of a radiative
transfer calculation, and quoting one without a grounded recipe is exactly the
back-of-envelope move the [derived-value grounding rule](methodology-index.md) bans.

Scope split: `T_eq` and the day-night structure of a synchronously-rotating body belong to
[`tidally-locked-temperature-methodology.md`](tidally-locked-temperature-methodology.md);
whether the atmosphere survives at all belongs to
[`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md). This doc
takes the composition as given and returns the warming.

Calculator: [`scripts/refs/greenhouse_dt.py`](../../scripts/refs/greenhouse_dt.py)
(implements Layer 3 and the host-star correction).

## The idea

**Step 1 — the no-atmosphere temperature is free.** `T_eq` follows from the starlight a
body receives and the fraction it reflects. One closed-form line, no model needed.

**Step 2 — what the atmosphere adds is not free.** The increment is set by how opaque the
atmosphere is to outgoing thermal infrared, which depends on *which* gases are present,
at what partial pressures, and on which *pairs* of molecules collide. There is no closed
form. Every honest number comes from a radiative calculation somebody ran.

**Step 3 — so pick the cheapest layer that covers your case.** The four layers below run
from "fully general, needs work" to "one line, narrow validity". Read the routing table,
use the shallowest layer whose conditions you satisfy, and record which layer produced
the number.

## Which layer applies

| | Layer | Covers | Cost | Use when |
|---|---|---|---|---|
| **1** | [Analytic radiative-convective model](#layer-1--the-analytic-model-any-composition) | Any composition, any pressure, thin to thick | Fit two opacity parameters | Thick atmospheres, exotic mixtures, or you need the whole P-T profile |
| **2** | [Per-gas and per-pair opacity data](#layer-2--per-gas-and-per-pair-opacity-the-gas-combination-answer) | Any mixture, from the molecular data up | Assemble opacities, then feed Layer 1 or a model | The mixture has no published analog: unusual gases, unusual CIA pairs |
| **3** | [Anchored iso-Ts contours](#layer-3--anchored-iso-ts-contours-the-shortcut) | N₂ background + CO₂ (+CH₄), ~1 bar, near-solar host | One line | The common rocky-planet case, and you accept ±5–10 K |
| **4** | [Borrow or run a real model](#layer-4--when-to-borrow-or-run-a-real-model) | Anything | Hours to days | The answer is load-bearing and Layers 1–3 disagree or do not apply |

Layer 3 is what most NearStars bodies use, so it carries the worked examples. It is also
the narrowest, and `layer_check()` in the calculator prints the reasons it does not apply.

## Layer 1 — the analytic model (any composition)

[Robinson & Catling 2012](https://arxiv.org/abs/1209.1833) give a **fully analytic 1-D
radiative-convective model** of atmospheric thermal structure. Thermal radiative transfer
is treated as gray in the two-stream approximation, the atmosphere is hydrostatic, and
the key modelling choice is a **power-law scaling between pressure and gray thermal
optical depth**. Convective regions follow adiabats with a scaling parameter that accounts
for condensation of volatiles. The result is closed-form expressions for the P-T profile
and for the radiative and convective flux profiles.

This is the general layer because **composition enters through only two knobs**: the
optical-depth-versus-pressure scaling (how strongly your gas mixture absorbs thermal IR,
and how that grows with pressure) and the adiabat parameter (which condensable dominates).
Fix those two and you get a surface temperature for any mixture, at any pressure.

Its authors validate it against the observed thermal structure of **Venus, Jupiter and
Titan** — three atmospheres that share no composition — plus flux comparisons against more
complex models. That validation range is why this is the layer to reach for when a body
falls outside the Archean-Earth-like box.

Two companions:

- [Robinson & Catling 2014](https://arxiv.org/abs/1312.6859) show that the pressure
  dependence of infrared transparency puts the tropopause near **0.1 bar in essentially
  any thick atmosphere**. Useful as a free structural constraint: if a model or an
  art-directed profile puts the tropopause somewhere else, that is a red flag.
- [Pierrehumbert 2010](https://ui.adsabs.harvard.edu/abs/2010ppc..book.....P),
  *Principles of Planetary Climate*, is the textbook derivation of the underlying gray
  and band-model greenhouse relations. Textbook status means it needs no further
  grounding.

The equations and their coefficients are in the paper; ar5iv has no machine-readable full
text for it, so this doc deliberately does not restate them. Read the paper before using
this layer.

## Layer 2 — per-gas and per-pair opacity (the gas-combination answer)

To build a mixture's opacity from scratch you need two kinds of data, and it is worth
being clear that they are different physics.

**Single-gas absorption lines.** [Gordon 2017](https://ui.adsabs.harvard.edu/abs/2017JQSRT.203....3G),
the HITRAN2016 database, is the standard line list. For already-integrated answers,
[Byrne & Goldblatt 2014b](https://arxiv.org/abs/1409.1880) publish **radiative forcings
for 28 candidate Archean greenhouse gases**, which is the fastest way to rank which trace
species in an invented atmosphere could matter at all, and
[2014a](https://ui.adsabs.harvard.edu/abs/2014GeoRL..41..152B) covers CO₂, CH₄ and N₂O at
very high concentrations (CO₂ to 50,000 ppmv, maximum forcing 38.1 W/m²) where the usual
logarithmic expressions break.

**Collision-induced absorption (CIA).** Pairs of colliding molecules absorb where neither
molecule has a line. In thick or reducing atmospheres this often dominates the warming, so
the available *pairs* constrain which mixtures can be warm at all.
[Karman 2019](https://ui.adsabs.harvard.edu/abs/2019Icar..328..160K) is the current HITRAN
CIA section and lists exactly what exists:

| Atmosphere type | CIA pairs that matter | In HITRAN CIA |
|---|---|---|
| N₂-dominated, reducing (Archean Earth, Titan) | N₂–N₂, N₂–H₂, N₂–CH₄ | yes |
| N₂-dominated, oxic (modern Earth) | N₂–O₂, O₂–O₂, N₂–H₂O | yes |
| CO₂-dominated (Mars-like, Venus-lite) | CO₂–CO₂, CH₄–CO₂, O₂–CO₂ | yes |
| CO₂ + H₂ (reducing thick) | CO₂–H₂ | **no — see below** |
| H₂/He-rich | H₂–H₂, H₂–He, H₂–CH₄, H₂–H, H–He | yes |
| Noble-buffered | CH₄–He, CH₄–Ar, CH₄–CH₄ | yes |

The CO₂–H₂ gap is a real limitation of the literature, not an oversight in this doc. As
the cached [Hayworth 2020](https://arxiv.org/abs/2004.09076) text records, Ramirez and
co-workers "assumed CO₂ is as efficient as N₂ at CIA excitation and applied the N₂–H₂ CIA
coefficients to early Mars-like conditions." Every published CO₂–H₂ warming estimate,
including the ones this doc cites, rests on that proxy. If a NearStars body's warmth
depends on CO₂–H₂, say so explicitly.

For habitable-zone limits under non-classical mixtures — CO₂+CH₄, CO₂+H₂ rather than the
classical CO₂+H₂O — [Ramirez 2018](https://arxiv.org/abs/1807.09504) reviews the newer HZ
formulations and is the right entry point before assembling opacities by hand.

## Layer 3 — anchored iso-Ts contours (the shortcut)

For the common case (N₂ background, CO₂ as the main greenhouse gas, optionally CH₄, around
1 bar, near-solar host) the published model runs can be reused directly, with no opacity
work at all.

Climate papers keep asking one question: *at this starlight level, how much CO₂ does the
surface need to sit at 273 K?* Each answer is a point on a (starlight, CO₂) plane, and the
points trace a contour. Read a body against the contour: more CO₂ than the contour means
warmer than 273 K, less means colder. **How much** comes from a second contour, for 288 K
— the horizontal gap between the two is worth 15 K, which converts "distance from the
contour" into kelvin.

Two facts about the contour's shape carry the physics:

- **It rises steeply as starlight falls.** Dropping `S/S₀` from 0.80 to 0.75 multiplies the
  CO₂ needed for 273 K by six.
- **It ends.** Past roughly 8 bar of CO₂, Rayleigh scattering brightens the planet faster
  than the greenhouse deepens, so **more CO₂ stops helping**. That end point is the outer
  edge of the habitable zone, so the contour carries the habitable zone inside it rather
  than needing a separate rule.

### The anchor points

Published 1-D radiative-convective runs, 1 bar background, cloud-free. Three points pin
the **Ts = 273 K** contour:

| S/S₀ | pCO₂ for Ts = 273 K | Source |
|---|---|---|
| 0.80 | 0.01 bar | [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1, late Archean |
| 0.75 | 0.06 bar | [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1, early Archean |
| `Seff_maxgh(Teff)` | ~8 bar | [Kopparapu 2013](https://arxiv.org/abs/1301.6674), maximum-greenhouse limit |

and two pin the **Ts = 288 K** contour ([Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1):
0.1 bar at `S/S₀` = 0.80, and 0.3 bar at `S/S₀` = 0.75.

### Host-star generalization

The third anchor is not a fixed number: the maximum-greenhouse limit moves with the host
star's spectrum, because a redder star's light is absorbed rather than Rayleigh-scattered.
[Kopparapu 2013](https://arxiv.org/abs/1301.6674) publish it in parametric form (their
Table 3), valid for `2600 ≤ Teff ≤ 7200 K`:

    Seff  =  Seff⊙  +  a·T★  +  b·T★²  +  c·T★³  +  d·T★⁴,      T★ = Teff − 5780 K

| Limit | Seff⊙ | a | b | c | d |
|---|---|---|---|---|---|
| Recent Venus | 1.7753 | 1.4316e-4 | 2.9875e-9 | −7.5702e-12 | −1.1635e-15 |
| Runaway greenhouse | 1.0512 | 1.3242e-4 | 1.5418e-8 | −7.9895e-12 | −1.8328e-15 |
| Moist greenhouse | 1.0140 | 8.1774e-5 | 1.7063e-9 | −4.3241e-12 | −6.6462e-16 |
| **Maximum greenhouse** | **0.3438** | **5.8942e-5** | **1.6558e-9** | **−3.0045e-12** | **−5.2983e-16** |
| Early Mars | 0.3179 | 5.4513e-5 | 1.5313e-9 | −2.7786e-12 | −4.8997e-16 |

So the contour's end point sits at `Seff` = 0.344 for the Sun, 0.348 for α Cen A (5847 K),
0.272 for a 4400 K K dwarf and 0.227 for a Proxima-like 3050 K M dwarf.
`greenhouse_dt.py --seff-table` prints the curve.

**But the two Archean anchors do not move**, because they are solar-spectrum calculations.
Layer 3 therefore stays valid only for host stars near solar `Teff`; the calculator warns
above ±800 K. For an M dwarf, either re-anchor on M-dwarf model runs or drop to Layer 1/2.
Getting this wrong is the classic error: an M dwarf's redder output changes both the
albedo and the absorption, and the CO₂ requirement with it.

### The formula

Between anchors, interpolate `log₁₀ pCO₂` linearly in `S/S₀` along each contour:

    pCO₂_eff  =  pCO₂ · 3            (if CH₄ is present at ≳ 1e-4 mixing ratio)

    Ts  =  273 K  +  m(S) · log₁₀(pCO₂_eff / pCO₂_273(S))  −  ΔT_haze  +  ΔT_N2

    m(S)  =  15 K / log₁₀( pCO₂_288(S) / pCO₂_273(S) )      [K per decade of CO₂]

    ΔT_gh  =  Ts  −  T_eq,        T_eq = 278.6 K · (S/S₀)^¼ · (1 − A)^¼

In words: `pCO₂_eff / pCO₂_273` is how far the body sits from the 273 K contour, as a
ratio; `m(S)` is the kelvin value of one factor-of-ten in that ratio, taken from the gap
between the two contours; the last two terms are corrections for haze and total pressure.
Below `S/S₀` = 0.75 the 288 K contour is shifted by the same amount as the 273 K contour,
which freezes the two-contour spacing — and therefore `m` — at its 0.75 value of
21.5 K per decade. Each correction is grounded:

- **CH₄ credit, factor 3.** [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.3, after
  Kiehl & Dickinson 1987: a CH₄ mixing ratio of 1e-4 lowers the CO₂ needed for a given Ts
  by "about a factor of ~3". Do not scale this credit up with a larger CH₄ inventory —
  [Byrne & Goldblatt 2015](https://ui.adsabs.harvard.edu/abs/2015CliPa..11..559B) show
  Archean CH₄ warming is *diminished* by solar absorption lines, and
  [Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H) revised the CH₄
  greenhouse downward after correcting its absorption coefficients.
- **ΔT_haze = 20 K** when the atmosphere is hazy.
  [Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A) finds fractal organic
  haze cools the surface "by about 20 K", but that the cooling is **self-limiting** (thick
  haze self-shields), so 20 K is a cap rather than a slope. Haze forms once CH₄/CO₂ exceeds
  roughly 0.1 ([Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H);
  [Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A)), which is the test
  the calculator applies by default.
- **ΔT_N2 = 4.4 K per doubling of total pressure.**
  [Goldblatt 2009](https://ui.adsabs.harvard.edu/abs/2009NatGe...2..891G): at Archean
  CO₂/CH₄ levels, doubling the present N₂ inventory warms by 4.4 °C by pressure-broadening
  the existing absorption lines. This is the term that makes total pressure matter
  independently of composition.

### Validation

`python3 scripts/refs/greenhouse_dt.py`

| Case | S/S₀ | pCO₂ | CH₄ | formula Ts | published Ts | diff |
|---|---|---|---|---|---|---|
| Earth today (observed) | 1.00 | 280 ppm | 1.7 ppm | 286.9 K | 288 K | −1.1 |
| Feulner late Archean, 273 K | 0.80 | 0.01 bar | — | 273.0 K | 273 K | anchor |
| Feulner late Archean, 288 K | 0.80 | 0.10 bar | — | 288.0 K | 288 K | anchor |
| Feulner early Archean, 273 K | 0.75 | 0.06 bar | — | 273.0 K | 273 K | anchor |
| Feulner early Archean, 288 K | 0.75 | 0.30 bar | — | 288.0 K | 288 K | anchor |
| Kiehl & Dickinson 1987, +CH₄ | 0.75 | 0.10 bar | 1e-4 | 288.0 K | 288 K | 0.0 |
| Charnay 2013 3-D GCM, comp. C | 0.75 | 0.10 bar | 2 mbar | 288.0 K | 290 K | −2.0 |
| Kopparapu 2013 max greenhouse | 0.344 | 8 bar | — | 273.0 K | 273 K | anchor |

Two rows are real tests rather than anchors: **Earth today lands 1.1 K low** and
**Charnay's 3-D GCM 2.0 K low**, both without tuning. The Kiehl & Dickinson row tests the
CH₄ credit independently and reproduces 288 K exactly.

The strongest check is one the formula was never fitted to. Extrapolating the contour to
early Mars, `S/S₀ = 0.32`, demands **pCO₂ ≈ 10.7 bar** — above the ~8 bar maximum-greenhouse
column, i.e. unreachable. That is precisely the published conclusion that CO₂ + H₂O alone
cannot warm early Mars to 273 K
([Kasting 1991](https://ui.adsabs.harvard.edu/abs/1991Icar...94....1K);
[Ramirez 2014](https://arxiv.org/abs/1405.6701);
[Hayworth 2020](https://arxiv.org/abs/2004.09076)), recovered from Archean-Earth anchors
alone.

## Layer 4 — when to borrow or run a real model

Drop to a full line-by-line or correlated-k radiative-convective model when the number is
load-bearing and the layers above disagree or do not apply. In practice "borrow" is almost
always the right verb: find a published run whose composition, pressure and host spectrum
bracket the body, and interpolate between published cases the way Layer 3 does.

For reducing thick atmospheres the published grid is already good:
[Ramirez 2014](https://arxiv.org/abs/1405.6701) reaches >273 K on early Mars with
1.3–4 bar CO₂ **plus 5–20 % H₂**, and
[Wordsworth & Pierrehumbert 2013](https://ui.adsabs.harvard.edu/abs/2013Sci...339...64W)
warm the early Earth above 0 °C at 75 % solar flux with 2–3× the present N₂ mass and a H₂
mixing ratio of 0.1, needing CO₂ only 2–25× present. Note what those numbers require:
**percent-level H₂, not traces.** Trace H₂ buys nothing, and sustaining percent-level H₂
needs a strongly reducing mantle plus outgassing that outruns escape.

## Domain of validity, by body class

1. **Layer 3 calibrated box: `0.75 ≤ S/S₀ ≤ 1.0`, `pCO₂ ≤ 0.3 bar`, ~1 bar total, N₂
   background, host near solar Teff.** Expect ±5 K.
2. **Layer 3 extrapolated band: `Seff_maxgh ≲ S/S₀ < 0.75`.** The contour here is a straight
   line between the early-Archean anchor and the maximum-greenhouse anchor: bounded at both
   ends by published points, unconstrained between. Expect **±10 K** and say so. The
   Alpha Centauri A b (Polyphemus) moons live here.
3. **Below the maximum-greenhouse limit**: the CO₂ route is closed, no matter the
   inventory. Reducing CIA is the only way to be warm — Layer 4's grid, with the CO₂–H₂
   proxy caveat from Layer 2.
4. **Thick atmospheres (≳ 2 bar) and Venus-like states**: Layer 1. Layer 3 will be wildly
   wrong; Venus's real increment is ~+510 K, far outside anything the contours cover.
5. **Non-solar hosts**: Layer 3's Archean anchors are solar-spectrum. K dwarfs are
   marginal, M dwarfs are out.
6. **Clouds are excluded everywhere in Layers 2–3.** Every anchor is cloud-free, and
   Kopparapu explicitly calls the resulting outer edge conservative because CO₂ cloud
   warming is neglected. A body a few K short of a target can be argued warm by invoking
   cloud warming, but that is an added assumption and must be recorded as one.
7. **Not for runaway/steam atmospheres, and not for H₂/He envelopes** (those are Layer 1
   with H₂–H₂ and H₂–He CIA, and the "surface" is a definition choice).

## Worked examples: the A b moons

α Cen A has `L = 1.521 L☉` and `Teff = 5847 K` (curated,
`db/systems/alpha_centauri_a.json`), and A b orbits at 1.6 AU, so every moon
receives `S/S₀ = 1.521 / 1.6² = 0.594` — **fainter than the early Archean Earth (0.75)**,
though still well inside this star's maximum-greenhouse limit (0.348). Liquid water is
possible in principle, but only with a CO₂ column far above Earth's. Near-solar host and a
~1 bar N₂/CO₂/CH₄ mixture put both bodies in Layer 3, extrapolated band, ±10 K.

At this insolation the 273 K contour sits at **pCO₂ ≈ 0.39 bar** (CO₂ only), or
**≈ 0.13 bar** with a few mbar of CH₄, and the CO₂ sensitivity is 21.5 K per decade.

| Body | atmosphere as recorded | T_eq | Layer 3 Ts | ΔT_gh | recorded ΔT |
|---|---|---|---|---|---|
| Alpha Centauri A b IV (Cassandra) | 1 bar N₂, 3 % CO₂, 3 mbar CH₄, thin haze, A 0.35 | 220 K | **239 K** hazy / **259 K** haze-free | +20 / +40 K | +45–50 K |
| Alpha Centauri A b III (Pandora) | 1.1 bar, 18 % CO₂ + CH₄ + H₂S, A 0.30 | 224 K | **277 K** | +54 K | +70 K |

- **A b IV** sits exactly at the haze threshold: CH₄/CO₂ = 0.1. That makes the haze term
  the whole argument. With haze it is a 239 K ice world; with no haze at all it reaches
  259 K. Since the body is *designed* with a visible amber haze, the defensible window is
  **240–260 K** — a partially frozen world whose water opens only near the warm equator or
  seasonally, which is what its surface description already says. Holding a global mean of
  270–275 K instead requires CO₂ at ~0.13 bar (13 % of a 1 bar atmosphere, four times the
  recorded value) or percent-level H₂.
- **A b III** lands at 277 K on the canon composition: habitable and above freezing, but
  ~13 K cooler than the recorded 290 K. Reaching 290 K at this insolation needs
  pCO₂ ≈ 0.8 bar, i.e. an atmosphere that is ~70 % CO₂ rather than 18 %, which contradicts
  the canon composition. The consistent choices are to lower the mean surface temperature to
  ~277 K, or to invoke CO₂ cloud warming explicitly (validity item 6).
  Note that H₂S, a canon constituent, has no CIA pair in HITRAN CIA and would need Layer 2
  line data to credit at all; it is not carrying any of this warming.

Both recorded increments were assigned without a recipe and both come out optimistic —
A b IV by 15–35 K depending on how much the haze is credited, A b III by ~13 K, against
a ±10 K band. Confidence in the method is medium; in the inputs (CO₂ fraction, haze optical
depth, albedo) low.

### The same body around a different star

`greenhouse_dt.py` closes with the same 1 bar / 3 % CO₂ / 3 mbar CH₄ world at
`S/S₀` = 0.594 around three hosts, to show the host-star axis and its limit:

| Host | Seff at max greenhouse | pCO₂ for 273 K | Layer 3 Ts | verdict |
|---|---|---|---|---|
| α Cen A, 5847 K | 0.348 | 0.40 bar | 259 K | in domain |
| K dwarf, 4400 K | 0.272 | 0.30 bar | 262 K | marginal |
| Proxima-like, 3050 K | 0.227 | 0.26 bar | 263 K | **out of domain** |

The trend is physical — a cooler star's maximum-greenhouse limit sits at lower flux, so the
same body needs less CO₂ — but only the first row is quotable. The other two inherit
solar-spectrum Archean anchors, so for the M dwarf this is Layer 1/2 territory.

## Why not radiative forcing times a climate sensitivity

The textbook-looking alternative is to add up the forcing in W/m² and multiply by a
sensitivity in K per W/m². Both halves exist (Layer 2's forcing tables are exactly the
first half). The product is the problem: the sensitivity is not a constant, because water
vapor and ice albedo make it depend on the temperature you are solving for, so one λ cannot
cover a frozen world and a temperate one. NearStars bodies sit in exactly that transition.
If this recipe is ever rebuilt on forcing, Byrne & Goldblatt are the place to start, and
the sensitivity has to become a function of the state rather than a number.

## Citations

**Layer 1 — general theory**

- **[Robinson & Catling 2012](https://arxiv.org/abs/1209.1833)**, ApJ 757, 104
  ([`2012ApJ...757..104R`](https://ui.adsabs.harvard.edu/abs/2012ApJ...757..104R)). The analytic gray two-stream radiative-convective model;
  composition enters as the optical-depth/pressure power law plus an adiabat scaling.
  Validated by its authors on Venus, Jupiter and Titan. *ar5iv has no usable full text*;
  this doc cites its structure and validation set from the ADS abstract and does not
  restate its equations.
- **[Robinson & Catling 2014](https://arxiv.org/abs/1312.6859)**, Nature Geoscience 7, 12
  ([`2014NatGe...7...12R`](https://ui.adsabs.harvard.edu/abs/2014NatGe...7...12R)). The ~0.1 bar tropopause common to thick atmospheres, from
  pressure-dependent IR transparency. Used as a structural sanity check.
- **[Pierrehumbert 2010](https://ui.adsabs.harvard.edu/abs/2010ppc..book.....P)**,
  *Principles of Planetary Climate* ([`2010ppc..book.....P`](https://ui.adsabs.harvard.edu/abs/2010ppc..book.....P)). Textbook derivation of the
  gray and band-model greenhouse relations; the allowed textbook exception.

**Layer 2 — opacity data**

- **[Karman 2019](https://ui.adsabs.harvard.edu/abs/2019Icar..328..160K)**, Icarus 328, 160
  ([`2019Icar..328..160K`](https://ui.adsabs.harvard.edu/abs/2019Icar..328..160K)). The HITRAN collision-induced absorption section; source of the
  CIA pair table above, including the absence of CO₂–H₂. No preprint; bibcode only.
- **[Gordon 2017](https://ui.adsabs.harvard.edu/abs/2017JQSRT.203....3G)**, JQSRT 203, 3
  ([`2017JQSRT.203....3G`](https://ui.adsabs.harvard.edu/abs/2017JQSRT.203....3G)). HITRAN2016 line list. Cited as the standard data source.
- **[Byrne & Goldblatt 2014a](https://ui.adsabs.harvard.edu/abs/2014GeoRL..41..152B)**,
  GRL 41, 152, and **[2014b](https://arxiv.org/abs/1409.1880)**, Clim. Past 10, 1779
  ([`2014CliPa..10.1779B`](https://ui.adsabs.harvard.edu/abs/2014CliPa..10.1779B)). High-concentration forcings (CO₂ to 50,000 ppmv, max 38.1 W/m²)
  and forcings for 28 candidate Archean gases.
- **[Ramirez 2018](https://arxiv.org/abs/1807.09504)**, Geosciences 8, 280
  ([`2018Geosc...8..280R`](https://ui.adsabs.harvard.edu/abs/2018Geosc...8..280R)). Review of habitable-zone formulations beyond classical CO₂+H₂O;
  the entry point for non-classical mixtures. Numbers here are from the ADS abstract only
  (ar5iv extraction failed); it is cited as a routing reference, not for a value.

**Layer 3 — contour anchors**

- **[Feulner 2012](https://arxiv.org/abs/1204.4449)**, Rev. Geophys. 50, 2006
  ([`2012RvGeo..50.2006F`](https://ui.adsabs.harvard.edu/abs/2012RvGeo..50.2006F)). Faint-young-Sun review; §5.1 supplies four of the five contour
  anchors and §5.3 the CH₄ factor-3 credit. **Cached** at `docs/phase3/_papers/1204.4449.md`.
- **[Kopparapu 2013](https://arxiv.org/abs/1301.6674)**, ApJ 765, 131
  ([`2013ApJ...765..131K`](https://ui.adsabs.harvard.edu/abs/2013ApJ...765..131K)). Habitable-zone limits; the maximum-greenhouse anchor (pCO₂ ~8 bar
  at 1.70 AU for the Sun, Ts fixed at 273 K, CO₂ varied 1–37.8 bar) and the Table 3
  parametric coefficients reproduced above. **Cached** at `docs/phase3/_papers/1301.6674.md`.
- **[Charnay 2013](https://arxiv.org/abs/1310.4286)**, JGR-Atmospheres 118, 10414
  ([`2013JGRD..11810414C`](https://ui.adsabs.harvard.edu/abs/2013JGRD..11810414C)). 3-D Archean GCM; composition C (0.1 bar CO₂ + 2 mbar CH₄ at
  3.8 Ga → ~17 °C) is the independent validation row. **Cached** at
  `docs/phase3/_papers/1310.4286.md`.
- **[Goldblatt 2009](https://ui.adsabs.harvard.edu/abs/2009NatGe...2..891G)**,
  Nature Geoscience 2, 891 ([`2009NatGe...2..891G`](https://ui.adsabs.harvard.edu/abs/2009NatGe...2..891G)). N₂ pressure-broadening term
  (+4.4 °C per doubling of the N₂ inventory). No preprint; bibcode only.
- **[Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H)**,
  Astrobiology 8, 1127 ([`2008AsBio...8.1127H`](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H)). Revised, hazy CH₄ greenhouse: corrected CH₄
  coefficients, pCO₂ ≥ 0.03 bar required, haze onset is climatically cooling. No preprint.
- **[Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A)**, Astrobiology 16,
  873 ([`2016AsBio..16..873A`](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A), arXiv [1610.04515](https://arxiv.org/abs/1610.04515)).
  Coupled climate-photochemical-microphysical hazy Archean: ~20 K cooling, self-limiting,
  τ ~5 at 200 nm, surface UV down ~97 %. *ar5iv extraction failed*; numbers from the ADS
  abstract.
- **[Byrne & Goldblatt 2015](https://ui.adsabs.harvard.edu/abs/2015CliPa..11..559B)**,
  Clim. Past 11, 559. Archean CH₄ warming diminished by solar absorption lines; the reason
  the CH₄ credit is capped rather than scaled.
- **[Wolf & Toon 2013](https://ui.adsabs.harvard.edu/abs/2013AsBio..13..656W)**,
  Astrobiology 13, 656 ([`2013AsBio..13..656W`](https://ui.adsabs.harvard.edu/abs/2013AsBio..13..656W)). Archean GCM corroborating temperate Archean
  climates. Listed for completeness only — ADS carries no abstract and there is no preprint,
  so **no number in this doc comes from it**.

**Layer 4 — borrowed model runs**

- **[Ramirez 2014](https://arxiv.org/abs/1405.6701)**, Nature Geoscience 7, 59
  ([`2014NatGe...7...59R`](https://ui.adsabs.harvard.edu/abs/2014NatGe...7...59R)). 1.3–4 bar CO₂ + 5–20 % H₂ raises early Mars above freezing.
  *ar5iv has no usable full text*; figures from the paper's own ADS abstract, cross-checked
  against Hayworth 2020's cached description.
- **[Hayworth 2020](https://arxiv.org/abs/2004.09076)**, Icarus 345, 113770
  ([`2020Icar..34513770H`](https://ui.adsabs.harvard.edu/abs/2020Icar..34513770H)). CO₂–H₂ CIA on early Mars; source for the 32 %-of-modern-Earth
  flux figure, for Ramirez's H₂ thresholds, and for the N₂–H₂-as-CO₂–H₂ proxy statement.
  **Cached** at `docs/phase3/_papers/2004.09076.md`.
- **[Wordsworth & Pierrehumbert 2013](https://ui.adsabs.harvard.edu/abs/2013Sci...339...64W)**,
  Science 339, 64 ([`2013Sci...339...64W`](https://ui.adsabs.harvard.edu/abs/2013Sci...339...64W)). H₂–N₂ CIA warming of the early Earth. *Science
  report, no preprint*: bibcode, numbers from the ADS abstract.
- **[Kasting 1991](https://ui.adsabs.harvard.edu/abs/1991Icar...94....1K)**, Icarus 94, 1
  ([`1991Icar...94....1K`](https://ui.adsabs.harvard.edu/abs/1991Icar...94....1K)), "CO₂ condensation and the climate of early Mars". The
  CO₂-cloud/albedo argument behind the maximum-greenhouse limit, cited through Kopparapu
  2013 and Hayworth 2020.

## Related

- [`tidally-locked-temperature-methodology.md`](tidally-locked-temperature-methodology.md)
  — supplies `T_eq` and the day-night structure this recipe adds an increment to.
- [`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md) — for a
  satellite, `T_eq` is not the stellar value: eclipses, the parent's thermal and reflected
  light, and tidal heating all enter. Compose that `T_eq` with `greenhouse_increment()`
  rather than using this doc's `Ts` directly, and mind its validity item 4.
- [`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md) — decides
  whether the atmosphere assumed here is retained at all, and owns composition/pressure.
- [`atmosphere-reflected-color-methodology.md`](atmosphere-reflected-color-methodology.md)
  — the same haze that cools the surface here sets the body's reflected color.
- [methodology-index](methodology-index.md) — the living index of all derived-value recipes.
