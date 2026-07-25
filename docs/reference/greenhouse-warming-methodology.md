<!-- 대기 온실 상승폭(T_surf − T_eq)을 문헌 iso-Ts 격자로 도출하는 방법(논문 근거) -->
# Greenhouse warming grounding: the literature iso-Ts grid

Method reference for deriving the **greenhouse temperature increment**

    ΔT_gh  =  T_surface  −  T_eq

of a rocky body with a real atmosphere. Equilibrium temperature is a closed-form
textbook quantity; the *increment* is not. It is the output of a radiative-convective
or general-circulation model, and quoting one without a grounded recipe is exactly the
back-of-envelope move the [derived-value grounding rule](methodology-index.md) bans.

This doc is the canonical home for the increment. `T_eq` itself, and the day-night
structure of a synchronously-rotating body, belong to
[`tidally-locked-temperature-methodology.md`](tidally-locked-temperature-methodology.md);
whether an atmosphere survives at all belongs to
[`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md).

Calculator: [`scripts/refs/greenhouse_dt.py`](../../scripts/refs/greenhouse_dt.py).

## Why not a forcing-plus-sensitivity formula

The tempting route is radiative forcing (W/m²) times a climate sensitivity (K per
W/m²). Both halves are grounded in the literature —
[Byrne & Goldblatt 2014a](https://ui.adsabs.harvard.edu/abs/2014GeoRL..41..152B)
compute CO₂ forcing from 100 ppmv to 50,000 ppmv (maximum 38.1 W/m²) and publish
simplified expressions that fix the IPCC ones at high concentration, and
[Byrne & Goldblatt 2014b](https://arxiv.org/abs/1409.1880) extend this to 28 Archean
gases — but the product is not: the sensitivity itself depends on temperature through
the water-vapor and ice-albedo feedbacks, so a single λ cannot span a frozen world and
a temperate one. NearStars bodies sit exactly in that transition, so this recipe stays
with the published model output instead.

## The relation: iso-Ts contours in (insolation, CO₂ column)

Published 1-D radiative-convective runs for a 1 bar background atmosphere converge on
a simple statement: for a target surface temperature, the required CO₂ partial pressure
rises steeply as insolation falls. Three points pin the **Ts = 273 K** contour:

| S/S₀ | pCO₂ for Ts = 273 K | Source |
|---|---|---|
| 0.80 | 0.01 bar | [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1, late Archean |
| 0.75 | 0.06 bar | [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1, early Archean |
| 0.346 | ~8 bar | [Kopparapu 2013](https://arxiv.org/abs/1301.6674), maximum-greenhouse limit (1.70 AU) |

and two pin the **Ts = 288 K** contour ([Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1):
0.1 bar at S/S₀ = 0.80, and 0.3 bar at S/S₀ = 0.75.

The Kopparapu anchor is the physically meaningful end of the contour, not just another
grid point: past ~8 bar, Rayleigh scattering by CO₂ raises the albedo faster than the
greenhouse deepens, so **more CO₂ stops helping**. That is the outer edge of the
habitable zone.

## The practical formula

Interpolate `log₁₀ pCO₂` piecewise-linearly in `S/S₀` along each contour, then read the
body's position relative to the 273 K contour:

    pCO₂_eff  =  pCO₂ · 3            (if CH₄ is present at ≳ 1e-4 mixing ratio)

    Ts  =  273 K  +  m(S) · log₁₀(pCO₂_eff / pCO₂_273(S))  −  ΔT_haze  +  ΔT_N2

    m(S)  =  15 K / log₁₀( pCO₂_288(S) / pCO₂_273(S) )      [K per decade of CO₂]

    ΔT_gh  =  Ts  −  T_eq,        T_eq = 278.6 K · (S/S₀)^¼ · (1 − A)^¼

Term by term, each grounded:

- **CH₄ credit, factor 3.** [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.3,
  after Kiehl & Dickinson 1987: a CH₄ mixing ratio of 1e-4 lowers the CO₂ needed for a
  given Ts by "about a factor of ~3". Do not stack this credit with a larger CH₄
  inventory — [Byrne & Goldblatt 2015](https://ui.adsabs.harvard.edu/abs/2015CliPa..11..559B)
  show Archean CH₄ warming is *diminished* by solar absorption lines, and
  [Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H) revised the
  CH₄ greenhouse downward after correcting its absorption coefficients.
- **ΔT_haze = 20 K** when the atmosphere is hazy.
  [Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A) finds fractal
  organic haze cools the surface "by about 20 K", but that the cooling is
  **self-limiting** (thick haze self-shields), so 20 K is a cap rather than a slope.
  Haze forms once CH₄/CO₂ exceeds roughly 0.1
  ([Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H);
  [Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A)), which is the
  test the calculator applies by default.
- **ΔT_N2 = 4.4 K per doubling of total pressure.**
  [Goldblatt 2009](https://ui.adsabs.harvard.edu/abs/2009NatGe...2..891G): at Archean
  CO₂/CH₄ levels, doubling the present atmospheric N₂ inventory warms by 4.4 °C through
  pressure broadening of the existing absorption lines.

### Validation: the formula against published runs

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
| Kopparapu 2013 max greenhouse | 0.346 | 8 bar | — | 273.0 K | 273 K | anchor |

Two of these are real tests rather than anchors: **Earth today lands 1.1 K low** and
**Charnay's 3-D GCM 2.0 K low**, both without tuning. The Kiehl & Dickinson row tests the
CH₄ credit independently and reproduces 288 K exactly.

The strongest independent check is one the formula was never fitted to. Extrapolating
the contour to early Mars, `S/S₀ = 0.32`, demands **pCO₂ ≈ 11 bar** — above the ~8 bar
maximum-greenhouse column, i.e. unreachable. That is precisely the published conclusion
that CO₂ + H₂O alone cannot warm early Mars to 273 K
([Kasting 1991](https://ui.adsabs.harvard.edu/abs/1991Icar...94....1K);
[Ramirez 2014](https://arxiv.org/abs/1405.6701);
[Hayworth 2020](https://arxiv.org/abs/2004.09076)), recovered from Archean-Earth
anchors alone.

## Domain of validity

1. **Calibrated box: `0.75 ≤ S/S₀ ≤ 1.0`, `pCO₂ ≤ 0.3 bar`, ~1 bar total, N₂ background,
   anoxic or Earth-like.** Inside it, expect ±5 K.
2. **Extrapolated band: `0.35 ≲ S/S₀ < 0.75`.** The contour here is a straight line in
   (S, log pCO₂) between the early-Archean anchor and the maximum-greenhouse anchor, so
   it is bounded at both ends by published points but unconstrained in between. Expect
   **±10 K**, and state it. NearStars' Polyphemus moons live in this band.
3. **Below the maximum-greenhouse limit (`S/S₀ ≲ 0.35`)**: the CO₂ route is closed. A
   body there needs reducing collision-induced absorption to be warm at all:
   [Ramirez 2014](https://arxiv.org/abs/1405.6701) reaches >273 K on early Mars with
   1.3–4 bar CO₂ **plus 5–20 % H₂**, and
   [Wordsworth & Pierrehumbert 2013](https://ui.adsabs.harvard.edu/abs/2013Sci...339...64W)
   warm the early Earth above 0 °C at 75 % solar flux with 2–3× the present N₂ mass and
   a H₂ mixing ratio of 0.1, needing CO₂ only 2–25× present. **Trace H₂ does not buy
   this**: the CIA terms need percent-level H₂, which in turn needs a strongly reducing
   mantle and outruns escape only with vigorous outgassing.
4. **Clouds are excluded.** Every anchor is a cloud-free calculation; Kopparapu
   explicitly calls the resulting outer edge conservative because CO₂ cloud warming is
   neglected. A body a few K short of a target can be argued warm by invoking cloud
   warming, but that is an added assumption and must be recorded as one.
5. **Not for runaway or steam atmospheres**, and not for H₂/He envelopes.

## Worked examples: the Polyphemus moons

α Cen A has `L = 1.521 L☉` (curated, `db/systems/alpha_centauri_a.json`) and Polyphemus
orbits at 1.6 AU, so every moon receives `S/S₀ = 1.521 / 1.6² = 0.594` — **fainter than
the early Archean Earth (0.75)**, and well inside the maximum-greenhouse limit
(0.346). Liquid water is therefore possible in principle, but only with a CO₂ column
far above Earth's.

At this insolation the 273 K contour sits at **pCO₂ ≈ 0.40 bar** (CO₂ only), or
**≈ 0.13 bar** with a few mbar of CH₄, and the CO₂ sensitivity is 21.4 K per decade.

| Body | atmosphere as recorded | T_eq | recipe Ts | ΔT_gh | recorded ΔT |
|---|---|---|---|---|---|
| Cassandra | 1 bar N₂, 3 % CO₂, 3 mbar CH₄, thin haze, A 0.35 | 220 K | **246 K** hazy / **266 K** haze-free | +26 / +46 K | +45–50 K |
| Pandora | 1.1 bar, 18 % CO₂ + CH₄ + H₂S, A 0.30 | 224 K | **275 K** | +52 K | +70 K |

- **Cassandra** sits right at the haze threshold: CH₄/CO₂ = 0.1 exactly. That makes the
  haze term the whole argument. With the haze it is a 246 K ice world; with no haze at
  all it reaches 266 K. Since the body is *designed* with a visible amber haze, the
  defensible window is **250–265 K** — a partially frozen world whose water opens only
  near the warm equator or seasonally, which is what its surface description already
  says. Holding a global mean of 270–275 K instead requires raising CO₂ to ~0.13 bar
  (13 % of a 1 bar atmosphere, four times the recorded value) or adding percent-level H₂.
- **Pandora** lands at 275 K on the canon composition: habitable and above freezing, but
  ~15 K cooler than the recorded 290 K. Reaching 290 K at this insolation needs
  pCO₂ ≈ 2 bar, which contradicts the canon ~1.1 atm total pressure. The consistent
  choices are to lower the mean surface temperature to ~275 K, or to invoke CO₂ cloud
  warming explicitly (item 4 above).

Both recorded increments were assigned without a recipe and both come out optimistic —
Cassandra by ~20 K, Pandora by ~15 K, against a ±10 K band. Confidence in the method is
medium; in the inputs (CO₂ fraction, haze optical depth, albedo) low.

## Citations

- **[Feulner 2012](https://arxiv.org/abs/1204.4449)**, Rev. Geophys. 50, 2006
  (`2012RvGeo..50.2006F`). The faint-young-Sun review; §5.1 supplies four of the five
  contour anchors and §5.3 the CH₄ factor-3 credit. **Cached** at
  `docs/phase3/_papers/1204.4449.md`.
- **[Kopparapu 2013](https://arxiv.org/abs/1301.6674)**, ApJ 765, 131
  (`2013ApJ...765..131K`). Updated habitable-zone limits; the maximum-greenhouse anchor
  (pCO₂ ~8 bar at 1.70 AU, Ts fixed at 273 K, CO₂ varied 1–37.8 bar). **Cached** at
  `docs/phase3/_papers/1301.6674.md`.
- **[Charnay 2013](https://arxiv.org/abs/1310.4286)**, JGR-Atmospheres 118, 10414
  (`2013JGRD..11810414C`). 3-D GCM of the Archean; composition C (0.1 bar CO₂ + 2 mbar
  CH₄ at 3.8 Ga → ~17 °C) is the independent validation row. **Cached** at
  `docs/phase3/_papers/1310.4286.md`.
- **[Hayworth 2020](https://arxiv.org/abs/2004.09076)**, Icarus 345, 113770
  (`2020Icar..34513770H`). CO₂–H₂ CIA on early Mars; source for the "32 % of modern
  Earth flux" figure and for Ramirez's H₂ thresholds. **Cached** at
  `docs/phase3/_papers/2004.09076.md`.
- **[Ramirez 2014](https://arxiv.org/abs/1405.6701)**, Nature Geoscience 7, 59
  (`2014NatGe...7...59R`). 1.3–4 bar CO₂ + 5–20 % H₂ raises early Mars above freezing.
  *ar5iv has no usable full text*; the figures used here are from the paper's own ADS
  abstract, cross-checked against Hayworth 2020's cached description of it.
- **[Wordsworth & Pierrehumbert 2013](https://ui.adsabs.harvard.edu/abs/2013Sci...339...64W)**,
  Science 339, 64 (`2013Sci...339...64W`). H₂–N₂ CIA warming of the early Earth.
  *Science report, no preprint*: cited by bibcode, numbers from the ADS abstract.
- **[Goldblatt 2009](https://ui.adsabs.harvard.edu/abs/2009NatGe...2..891G)**,
  Nature Geoscience 2, 891 (`2009NatGe...2..891G`). N₂ pressure-broadening term
  (+4.4 °C per doubling of the N₂ inventory). *Nature Geoscience letter, no preprint*:
  bibcode only.
- **[Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H)**,
  Astrobiology 8, 1127 (`2008AsBio...8.1127H`). Revised, hazy CH₄ greenhouse: corrected
  CH₄ coefficients, pCO₂ ≥ 0.03 bar required, haze onset is climatically cooling.
  No preprint; bibcode only.
- **[Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A)**,
  Astrobiology 16, 873 (`2016AsBio..16..873A`, arXiv
  [1610.04515](https://arxiv.org/abs/1610.04515)). Coupled climate-photochemical-
  microphysical hazy Archean: ~20 K cooling, self-limiting, τ ~5 at 200 nm, surface UV
  down ~97 %. *ar5iv extraction failed*; numbers from the ADS abstract.
- **[Byrne & Goldblatt 2014a](https://ui.adsabs.harvard.edu/abs/2014GeoRL..41..152B)**,
  GRL 41, 152, and **[2014b](https://arxiv.org/abs/1409.1880)**, Clim. Past 10, 1779
  (`2014CliPa..10.1779B`). High-concentration radiative forcings and 28 Archean gases.
  Not used numerically here; cited for why the forcing route was rejected, and the place
  to start if this recipe is ever rebuilt as forcing-plus-sensitivity.
- **[Byrne & Goldblatt 2015](https://ui.adsabs.harvard.edu/abs/2015CliPa..11..559B)**,
  Clim. Past 11, 559. Archean CH₄ warming diminished by solar absorption lines; the
  reason the CH₄ credit is capped rather than scaled.
- **[Wolf & Toon 2013](https://ui.adsabs.harvard.edu/abs/2013AsBio..13..656W)**,
  Astrobiology 13, 656 (`2013AsBio..13..656W`). Archean GCM
  corroborating temperate Archean climates. Listed for completeness only — ADS carries
  no abstract and there is no preprint, so **no number in this doc comes from it**.
- **[Kasting 1991](https://ui.adsabs.harvard.edu/abs/1991Icar...94....1K)**, Icarus 94, 1
  (`1991Icar...94....1K`), "CO₂ condensation and the climate of early Mars". The CO₂-cloud/albedo argument
  behind the maximum-greenhouse limit, cited through Kopparapu 2013 and Hayworth 2020.

## Related

- [`tidally-locked-temperature-methodology.md`](tidally-locked-temperature-methodology.md)
  — supplies `T_eq` and the day-night structure this recipe adds an increment to; use
  that doc's Layer 1 for the closed form and this one for the atmosphere.
- [`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md) — decides
  whether the atmosphere assumed here is retained at all.
- [`atmosphere-reflected-color-methodology.md`](atmosphere-reflected-color-methodology.md)
  — the same haze that cools the surface here sets the body's reflected color.
- [methodology-index](methodology-index.md) — the living index of all derived-value recipes.
