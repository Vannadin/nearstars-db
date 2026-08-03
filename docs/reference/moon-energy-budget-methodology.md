<!-- 위성의 T_eq를 4항 에너지 예산(별빛−식+행성열복사+행성반사+조석)으로 도출하는 방법(논문 근거) -->
# Satellite energy budget: the four terms a planet does not have

Method reference for the **equilibrium temperature of a moon**. A satellite is not a
planet on a slightly different orbit. Four terms that are zero or negligible for a planet
are first-order for a close-in moon, and three of them are easy to forget:

    absorbed  =  stellar·(1 − f_eclipse)  +  parent thermal  +  parent reflected  +  tidal

    T_eq  =  (absorbed / σ)^¼

For a body with an atmosphere, the greenhouse increment from
[`greenhouse-warming-methodology.md`](greenhouse-warming-methodology.md) is then added on
top of *this* `T_eq`, not the stellar-only one.

Calculator: [`scripts/refs/moon_energy_budget.py`](../../scripts/refs/moon_energy_budget.py).

The framing is [Heller & Barnes 2013](https://arxiv.org/abs/1209.5323), who assemble
exactly these terms for exomoons and note that satellites "can receive more illumination
per area than their host planets, as the planet reflects stellar light and emits thermal
photons," that "eclipses can significantly alter local climates on exomoons by reducing
stellar illumination," and that "tidal heating can be very large on exomoons, possibly
even large enough for sterilization."
[Dobos, Heller & Turner 2017](https://arxiv.org/abs/1703.02447) run the same four sources
as a habitable-zone calculation.

## The terms

### Eclipses — a cooling term, usually the biggest surprise

The parent casts an umbra of length `L = R_p · d_star / (R_star − R_p)`. Every NearStars
moon sits far inside its parent's umbra, so eclipses are total, not annular.

Whether they happen *every* orbit is a geometry question with a clean answer: the moon's
excursion out of the parent's orbital plane is `a · sin(i)`, and if that stays smaller
than the shadow radius, the moon cannot avoid the shadow no matter where its line of nodes
points. Compact moon systems therefore eclipse continuously rather than seasonally.

The orbit-averaged fraction of stellar flux lost is the shadow chord over the orbit
circumference:

    f_eclipse  =  [ 2·√(r_shadow² − (a·sin i)²)  +  2·R_moon ]  /  2πa

This is a first-order treatment: it ignores penumbra, and it returns 0 for moons whose
inclination lifts them clear of the shadow, which under-counts seasonal eclipses. Both
errors are small next to the term itself.

### Parent thermal emission — a heating term, continuous

The parent radiates as a body of temperature `T_p` (its own equilibrium temperature plus
whatever internal heat it still carries), so at the moon:

    F_thermal  =  σ T_p⁴ · (R_p / a)²

Unlike starlight this never switches off, and it peaks exactly when the moon is eclipsed.
Long-wave albedo is low, so the moon absorbs nearly all of it; the calculator uses 0.05.

### Parent reflected starlight — a heating term, in phase with the eclipse

    F_reflected  =  A_p · S · (R_p / a)² / 4

Reflected light is maximal at superior conjunction, when the moon sees the parent's fully
lit face — which is also when it is in shadow. Orbit-averaging both terms separately gets
the total energy right, which is what a global `T_eq` needs.

### Tidal heating — a heating term, and the one with the widest range

The solid-body term is owned by
[`tidal-heating-methodology.md`](tidal-heating-methodology.md); this doc only consumes it:

    Ė  =  (21/2) · (k₂/Q) · G M_p² R⁵ n e² / a⁶,      F_tidal = Ė / 4πR²

The `a^(−15/2)` dependence is what makes this term dangerous. `k₂/Q` spans more than a
decade across plausible interiors, so the tidal flux spans more than a decade too, and it
is usually the dominant uncertainty in a close-in moon's budget.

### The ceiling: the circumplanetary habitable edge

Enough total flux triggers a runaway greenhouse, and tidal heating counts.
[Barnes 2013](https://arxiv.org/abs/1203.5104) named the outcome a **"Tidal Venus"**: a
world tidally heated "at high enough levels to induce a runaway greenhouse for a long
enough duration for all the hydrogen to escape," after which it cannot support life even
if the orbit later circularizes. [Heller & Barnes 2013](https://arxiv.org/abs/1209.5323)
turn the same idea into a **circumplanetary "habitable edge"**: the locus where radiative
plus tidal heating trigger runaway.

The calculator's ceiling is a first-order stand-in: take
[Kopparapu 2013](https://arxiv.org/abs/1301.6674)'s moist-greenhouse limit for the host
star, subtract the stellar flux the moon already receives, and convert the remainder into
an allowable extra surface flux. That treats internal heat as interchangeable with
absorbed starlight, which it is not in detail — Barnes 2013 is the proper calculation. Use
it as a red line, not as a precise boundary.

Worth keeping in view: Heller & Barnes's own illustration is that a satellite "at a
distance greater than 10 planetary radii" is the configuration that could indicate a
habitable moon. Close-in canon moons start out on the wrong side of that.

## Validation

`python3 scripts/refs/moon_energy_budget.py`

| Check | Formula | Observed | |
|---|---|---|---|
| Io tidal flux (`k₂/Q` = 0.015) | 2.24 W/m² | ~2.4 W/m² | ✓ |
| Io eclipse duration | 5.5 % of a 42.5 h orbit = 2.3 h | the familiar ~2.2 h | ✓ |

The two checks are independent: the first is the tidal formula against a measured heat
flow, the second is pure shadow geometry against a duration anyone can watch through a
telescope. Neither was tuned.

## Domain of validity

1. **Total umbral eclipses only.** Penumbra and annular geometry are ignored. Fine while
   the moon sits deep inside the umbra, which holds for any moon of a giant at a
   Sun-like distance.
2. **Global averages.** The four-term `T_eq` is an energy-balance mean. A close-in moon
   also has strong local structure — sub-parent hemisphere, eclipse cycle, day-night — that
   this does not resolve. With a thick atmosphere or an ocean, thermal inertia smooths the
   eclipse cycle anyway.
3. **Constant parent temperature.** `T_p` is taken as one number. A young giant's internal
   heat makes it much hotter, and [Heller 2015](https://arxiv.org/abs/1311.0292) shows
   irradiation from hot, young giant planets can drive a runaway greenhouse on their moons
   by itself. For an old system the cloud-top equilibrium value is adequate.
4. **The composition with a greenhouse increment is an extrapolation once tidal flux is
   large.** The greenhouse contours were calibrated on bodies whose internal heat is
   negligible; adding a contour-derived `ΔT_gh` on top of a tidally inflated `T_eq`
   assumes the increment is unchanged, when in reality the water-vapour feedback responds
   to the actual temperature. Barnes 2013 treats stellar and tidal flux together.
5. **Ocean tidal dissipation is NOT in this budget.** See the second channel below. For a
   moon with a liquid ocean it is a separate term, set by the eccentricity tide and the
   ocean's depth rather than by `k₂/Q`.

## Worked example: the Alpha Centauri A b (Polyphemus) moons

α Cen A (`L = 1.521 L☉`, `Teff = 5847 K`), A b at 1.6 AU (`S/S₀ = 0.594`), parent
radius 1.0 R_Jup, mass 120 M⊕, cloud-top 225 K, `A_p` = 0.30. The umbra reaches
2.19 × 10⁷ km and **all five moons are inside it, eclipsed on every orbit** — for each of
them `a·sin(i)` is smaller than the shadow radius.

| Moon | a [R_p] | eclipse | stellar lost | parent thermal | parent reflected | T_eq stellar | T_eq 4-term | ΔT |
|---|---|---|---|---|---|---|---|---|
| Alpha Centauri A b I (Dante) | 1.54 | 20.2 % | −28.6 W/m² | 61.3 | 25.6 | 223.5 K | 219.6 K | **−3.9 K** |
| Alpha Centauri A b II (Hades) | 2.07 | 14.2 % | −20.1 | 33.9 | 14.2 | 223.5 K | 219.6 K | **−3.9 K** |
| Alpha Centauri A b III (Pandora) | 3.53 | 7.7 % | −10.9 | 11.7 | 4.9 | 223.5 K | 220.6 K | **−2.9 K** |
| Alpha Centauri A b IV (Cassandra) | 8.40 | 3.1 % | −4.1 | 2.1 | 0.9 | 219.4 K | 217.9 K | −1.5 K |
| Alpha Centauri A b V (Chaos) | 21.0 | 1.3 % | −0.8 | 0.3 | 0.1 | 180.8 K | 180.3 K | −0.5 K |

The parent's illumination is large at the moon — 61 W/m² of thermal flux reaching A b I —
but it enters the global average divided by four and after albedo, while the eclipse
removes stellar flux that was already divided by four. **Eclipse loss wins at every
distance**, so the net effect of "being a moon" is cooling, not warming. Intuition points
the other way, which is precisely why the term is worth computing.

### Why A b III's lock is 32 h and not the canon 27 h

The board chose a 32 h tidal lock over the film's 27 h, recorded as keeping the ocean's
tidal budget sub-runaway. That decision holds up quantitatively, and the margin is thin:

| Period | a | tidal flux at `e` = 0.005, `k₂/Q` = 0.0016 | vs the 101 W/m² ceiling |
|---|---|---|---|
| 27 h (canon) | 225,365 km | **106 W/m²** | over — Tidal Venus |
| 32 h (adopted) | 252,393 km | **45 W/m²** | under, factor 2.2 margin |

A 10.7 % smaller orbit raises the tidal flux by 2.34×, purely from `a^(−15/2)`. The canon
orbit lands just past the runaway ceiling; the adopted one sits comfortably inside it.

The same calculation then explains A b III's canon surface temperature without touching its
canon composition. With the four-term `T_eq` and the greenhouse increment of +53.6 K from
its 18 % CO₂ + CH₄ atmosphere:

| `k₂/Q` | tidal flux | T_eq | T_surface |
|---|---|---|---|
| 0 (no tidal term) | 0 | 220.6 K | 274.1 K |
| 0.0010 | 28.3 W/m² | 231.4 K | 285.0 K |
| **0.0016** | **45.3 W/m²** | **237.2 K** | **290.8 K** ← canon 290 K |
| 0.0030 | 85.0 W/m² | 249.4 K | 302.9 K |
| 0.0060 | 170 W/m² | 270.6 K | 324.2 K |
| 0.0150 (Io-like) | 425 W/m² | 315.1 K | 368.7 K |

Read this as a constraint, not a prediction: `k₂/Q` ≈ 0.0016 is *fitted* to land on 290 K.
What the table earns is the consistency statement — a single `k₂/Q` exists that puts the
canon 27 h orbit past the runaway ceiling *and* reproduces the canon 290 K at 32 h. The
sensitivity is brutal in the other direction: an Io-like interior would make A b III a
369 K steam world.

The lesson generalizes past this system. For a close-in moon the tidal term, not the
greenhouse, is usually the knob that decides habitability, and it is the knob with the
worst-constrained input.

## The second channel: ocean tidal dissipation

Everything above uses **solid-body** tidal dissipation. A moon with a liquid ocean
dissipates tidal energy in the water too, and that channel obeys different rules. Two
forcings drive it, and telling them apart is the whole game.

**Obliquity forcing is efficient but starved.**
[Tyler 2008](https://ui.adsabs.harvard.edu/abs/2008Natur.456..770T) showed that the
obliquity tide — usually dismissed as subdominant — has the right form and frequency to
resonantly excite large-amplitude Rossby waves in a moon's ocean; for Europa the kinetic
energy of that resonant flow is "two thousand times larger than that of the flow excited by
the dominant tidal forces." [Hay & Matsuyama 2019](https://ui.adsabs.harvard.edu/abs/2019Icar..319...68H)
conclude that "obliquity tides are likely to dominate the tidal heating budget of icy
satellite oceans."

The catch is the forcing angle. **What drives an obliquity tide is the angle between the
spin axis and the moon's own orbit normal, not the tilt of that orbit relative to anything
else.** A tidally damped moon settles into a Cassini state, and per
[`cassini-state-obliquity-methodology.md`](cassini-state-obliquity-methodology.md) a
close-in moon of a giant is expected at **sub-degree** obliquity — 10⁻³–10⁻² degrees like
the Galileans, reaching Titan-like 0.1–0.3° only if an ocean amplifies it.
[Matsuyama 2014](https://ui.adsabs.harvard.edu/abs/2014Icar..242...11M) puts a number on
what that starvation costs: at Cassini-state obliquity, Enceladus's obliquity-tide flux is
"smaller than the observed value by many orders of magnitude."

**Eccentricity forcing is the live channel, and it is resonant.** Matsuyama 2014 finds the
resonant response to the *eccentricity* tide "can be large enough to explain Enceladus'
observed heat flow", and that ocean loading, self-attraction and solid-region deformation
shift which ocean thicknesses resonate, "potentially resulting in orders of magnitude
changes in the dissipated energy flux."

For NearStars this is good news, because it turns a threat into a knob:

- The channel that could run away needs an obliquity we do not have. A b III's recorded
  `obliquity: 10°` is the **orbital inclination** (the board's own note: canon 29° reread
  as the orbital-plane tilt, `spin_axis_orientation: orbit normal`), so the tide-driving
  angle is the Cassini-state value, sub-degree, comparable to or smaller than Europa's.
- The channel that remains is set by **ocean thickness**, which for an invented world is an
  art parameter. Pick a depth away from resonance and the flux is small; land on resonance
  and it moves by orders of magnitude.
- A b III's ocean is at the surface, so the ice-shell effects
  ([Beuthe 2016](https://arxiv.org/abs/1608.08488)'s crustal suppression,
  [Hay & Matsuyama 2019](https://ui.adsabs.harvard.edu/abs/2019Icar..319...68H)'s
  shell-mediated enhancement) do not apply; the free-surface treatment is the right one,
  and Hay & Matsuyama extend free-surface scaling laws to shells "benchmarked to within
  10 %", so the free-surface laws are the validated baseline rather than an approximation.

**Status: bounded, not quantified.** No number is assigned here because the eccentricity
resonance depends on an ocean depth nobody has chosen yet. What this section buys is the
knowledge that the ocean channel is a depth choice rather than an uncontrolled risk, and
that "the ocean's tidal budget" in the board's wording is the solid-body budget above plus
this depth-dependent term. Fixing A b III's ocean depth is the trigger to compute it, with
[Matsuyama 2018](https://arxiv.org/abs/1804.07727) as the method.

## Citations

- **[Heller & Barnes 2013](https://arxiv.org/abs/1209.5323)**, Astrobiology 13, 18
  ([`2013AsBio..13...18H`](https://ui.adsabs.harvard.edu/abs/2013AsBio..13...18H)). The four-term exomoon budget (planetary reflection, thermal
  emission, eclipses, tidal heating) and the circumplanetary habitable edge; also the
  >10 planetary-radii illustration. *ar5iv extraction failed*; the statements used here
  are from the paper's own ADS abstract.
- **[Dobos, Heller & Turner 2017](https://arxiv.org/abs/1703.02447)**, A&A 601, A91
  ([`2017A&A...601A..91D`](https://ui.adsabs.harvard.edu/abs/2017A%26A...601A..91D)). The same four energy sources as an exomoon habitable-zone
  calculation, following Heller et al. 2014 Eq. 4; also the ~100 W/m² tidal marker used in
  their habitability shading. **Cached** at `docs/phase3/_papers/1703.02447.md`.
- **[Barnes 2013](https://arxiv.org/abs/1203.5104)**, Astrobiology 13, 225
  ([`2013AsBio..13..225B`](https://ui.adsabs.harvard.edu/abs/2013AsBio..13..225B)). "Tidal Venuses": tidal heating driving a runaway greenhouse long
  enough to desiccate a world, and the resulting revision to the habitable zone for
  non-circular orbits. Numbers from the ADS abstract.
- **[Heller 2015](https://arxiv.org/abs/1311.0292)**, Int. J. Astrobiology 14, 335
  ([`2015IJAsB..14..335H`](https://ui.adsabs.harvard.edu/abs/2015IJAsB..14..335H)). Runaway greenhouse on exomoons from irradiation by hot, young
  giant planets — the reason a constant parent temperature is a validity limit here.
- **[Kopparapu 2013](https://arxiv.org/abs/1301.6674)**, ApJ 765, 131
  ([`2013ApJ...765..131K`](https://ui.adsabs.harvard.edu/abs/2013ApJ...765..131K)). Supplies the moist-greenhouse limit used as the first-order
  runaway ceiling. **Cached** at `docs/phase3/_papers/1301.6674.md`.
- **[Tyler 2008](https://ui.adsabs.harvard.edu/abs/2008Natur.456..770T)**, Nature 456, 770
  ([`2008Natur.456..770T`](https://ui.adsabs.harvard.edu/abs/2008Natur.456..770T)). Obliquity-driven Rossby-wave resonance in moon oceans; the
  2000× flow-energy result for Europa. *Nature letter, no preprint*: bibcode, numbers from
  the ADS abstract.
- **[Matsuyama 2014](https://ui.adsabs.harvard.edu/abs/2014Icar..242...11M)**, Icarus 242,
  11 ([`2014Icar..242...11M`](https://ui.adsabs.harvard.edu/abs/2014Icar..242...11M)). Ocean loading, self-attraction and solid-region deformation
  shift the resonant ocean thicknesses by orders of magnitude; at Cassini-state obliquity
  Enceladus's obliquity-tide flux falls "many orders of magnitude" below observed, while the
  resonant eccentricity tide can explain the observed heat flow. This is the paper that
  decides which ocean forcing matters. No preprint; numbers from the ADS abstract.
- **[Matsuyama 2018](https://arxiv.org/abs/1804.07727)**, Icarus 312, 208
  ([`2018Icar..312..208M`](https://ui.adsabs.harvard.edu/abs/2018Icar..312..208M)). Ocean tidal heating with solid shells; thin-shell approximation
  accurate to a few percent for eccentricity tides. The method to use once an ocean depth is
  chosen. **Cached** at `docs/phase3/_papers/1804.07727.md`.
- **[Beuthe 2016](https://arxiv.org/abs/1608.08488)**, Icarus 280, 278
  ([`2016Icar..280..278B`](https://ui.adsabs.harvard.edu/abs/2016Icar..280..278B)). Crustal control of dissipative ocean tides; subsurface-to-surface
  ocean scaling rules. Numbers from the ADS abstract.
- **[Hay & Matsuyama 2019](https://ui.adsabs.harvard.edu/abs/2019Icar..319...68H)**,
  Icarus 319, 68 ([`2019Icar..319...68H`](https://ui.adsabs.harvard.edu/abs/2019Icar..319...68H)). Non-linear bottom drag with an ice shell;
  free-surface dissipation scaling laws extended to shells and benchmarked to within 10 %;
  concludes obliquity tides dominate icy-satellite ocean heating *where the obliquity
  exists*. No preprint; numbers from the ADS abstract.
- **[Hay & Matsuyama 2017](https://ui.adsabs.harvard.edu/abs/2017Icar..281..342H)**,
  Icarus 281, 342 ([`2017Icar..281..342H`](https://ui.adsabs.harvard.edu/abs/2017Icar..281..342H)). Numerical Laplace-tidal-equation modelling with
  bottom drag; obliquity Rossby resonance independent of ocean thickness for thick oceans.
  No preprint; bibcode only.
- **Peale, Cassen & Reynolds 1979** — the tidal term itself, via
  [`tidal-heating-methodology.md`](tidal-heating-methodology.md), which carries the full
  citation and the `k₂/Q` calibration table.

## Related

- [`ice-stability-methodology.md`](ice-stability-methodology.md) — consumes this doc's
  `F_abs` to decide whether exposed ice survives; the sublimation term makes the surface
  colder than the `T_eq` computed here whenever a volatile is exposed.
- [`tidal-heating-methodology.md`](tidal-heating-methodology.md) — owns the tidal power
  formula and the `k₂/Q` regimes this doc consumes as one of its four terms.
- [`greenhouse-warming-methodology.md`](greenhouse-warming-methodology.md) — adds the
  atmospheric increment on top of the `T_eq` computed here; see its Layer-3 domain limits
  before composing the two.
- [`tidally-locked-temperature-methodology.md`](tidally-locked-temperature-methodology.md)
  — the planet-side `T_eq` and day-night structure; a moon replaces its Layer 1 with this
  doc's four terms.
- [`cassini-state-obliquity-methodology.md`](cassini-state-obliquity-methodology.md) —
  supplies the spin-axis obliquity that decides whether the obliquity ocean tide is live.
  Do not substitute an orbital inclination for it.
- [methodology-index](methodology-index.md) — the living index of all derived-value recipes.
