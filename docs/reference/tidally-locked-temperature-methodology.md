<!-- 조석고정 외계행성 표면온도 추정 방법론 레퍼런스 -->
# Tidally-Locked Exoplanet Surface-Temperature Methodology

> Source: synthesis of the tidally-locked-planet climate literature (Joshi 1997,
> Pierrehumbert 2011, Kite+ 2011, Yang+ 2013, Hu & Yang 2014, Wordsworth 2015,
> Koll & Abbot 2016, Kopparapu+ 2013/2016, Checlair+ 2017, Haqq-Misra+ 2018,
> Yang+ 2019, Koll 2022, Hammond+ 2022, Turbet+ 2016, Boutle+ 2017, Abe+ 2011).
> Citations resolved against NASA ADS (the registered ADS_API_TOKEN), not ad-hoc
> web search; arXiv id where one exists, otherwise the authoritative ADS bibcode.
> Purpose: a reusable three-layer recipe for estimating substellar / nightside /
> global-mean surface temperatures of synchronously-rotating rocky planets in the
> NearStars roster (Proxima b, the seven TRAPPIST-1 planets, etc.), and for
> mapping the result onto KSP/Kopernicus temperature curves at emit.
> This is a working reference, not a textbook. See §7 for the verified citations.

## Table of Contents

1. [Why Tidally-Locked Planets Need Special Treatment](#1-why-tidally-locked-planets-need-special-treatment)
2. [Layer 1: Equilibrium Temperature (Closed-Form)](#2-layer-1-equilibrium-temperature-closed-form)
3. [Layer 2: Substellar Ceiling & Day-Night Contrast (Analytic Scaling)](#3-layer-2-substellar-ceiling-day-night-contrast-analytic-scaling)
4. [Layer 3: Body-Specific GCMs (Anchor Values)](#4-layer-3-body-specific-gcms-anchor-values)
5. [Climate-State Taxonomy](#5-climate-state-taxonomy)
6. [How NearStars Applies This](#6-how-nearstars-applies-this)
7. [Annotated Bibliography](#7-annotated-bibliography)
8. [Related](#related)

---

## 1. Why Tidally-Locked Planets Need Special Treatment

A synchronously-rotating planet keeps one hemisphere facing its star forever. The
substellar point receives steady, perpendicular insolation while the antistellar
hemisphere sees no starlight at all: a permanent day side and a permanent night
side, with a fixed terminator ring between them. This is the generic state for
rocky planets in the habitable zones of M dwarfs (the orbits are close enough
that tidal locking happens within the system age), which is exactly the regime
of most NearStars terrestrial targets.

Two consequences follow that make the usual one-number "temperature" misleading:

- **Equilibrium temperature (Teq) is NOT the surface temperature.** Teq is a
  globally-averaged radiative-balance number that assumes the absorbed flux is
  spread evenly over the whole planet. A locked planet does not heat evenly. The
  real surface field is a steep gradient from a hot substellar point to a cold
  antistellar point. Teq lands somewhere in between and describes neither.

- **The day-night contrast is set by the atmosphere, not the orbit.** With no
  atmosphere (or a very thin one) the day side bakes and the night side
  radiates to near the cosmic background; the contrast is enormous and the night
  side can be cold enough to freeze out the atmosphere itself. A thick atmosphere
  (or an ocean) transports heat to the night side and flattens the gradient. So
  the same orbit can yield wildly different surface temperatures depending on the
  atmospheric inventory.

The recipe below therefore produces **three** numbers (substellar, nightside,
global mean) and treats the spread between them as the quantity that depends on
atmosphere thickness and heat transport.

---

## 2. Layer 1: Equilibrium Temperature (Closed-Form)

The cheap, always-available anchor. From global radiative balance with stellar
flux `S` (incident at the planet's orbit), Bond albedo `A`, and the factor of 4
for the day-side-disk-absorbs / whole-sphere-emits geometry:

```
Teq = [ S (1 − A) / (4 σ) ]^(1/4)
```

Equivalently in terms of the host's effective temperature `Teff`, radius `R*`,
and orbital distance `a`:

```
Teq = Teff · sqrt(R* / 2a) · (1 − A)^(1/4)
```

(the two forms are identical once `S = σ Teff⁴ · (R*/a)²` is substituted).

**Worked example: Proxima b.** With `S ≈ 0.66 S⊕` and `A ≈ 0.2`,

```
Teq ≈ 230 K   (literature range 226–251 K depending on the exact S, albedo,
               and whether a moist/greenhouse correction is folded in)
```

**Caveat that motivates Layer 2:** the factor of 4 bakes in **efficient global
redistribution**. It assumes the absorbed energy is shared over the entire
sphere before re-emission. That is an idealization. For a locked planet it is the
*best-case* (thick-atmosphere) limit, not the actual surface temperature. Teq is
the right anchor for "how much energy is in the system," but on its own it
silently assumes the most heat-transport-efficient atmosphere possible.

---

## 3. Layer 2: Substellar Ceiling & Day-Night Contrast (Analytic Scaling)

Layer 2 brackets the problem: an upper bound on the day side, plus an estimate of
how much the atmosphere closes the day-night gap.

### Substellar ceiling (zero redistribution)

The opposite idealization from Teq: a bare rock with no heat transport, where each
surface element is in instantaneous local radiative balance. At the substellar
point the star is overhead, so the geometry factor is 1 (not 1/4):

```
T_ss = [ S (1 − A) / σ ]^(1/4)   =   Teq · 4^(1/4)   ≈   1.19 · Teq
```

**Proxima b (A = 0.2): T_ss ≈ 336 K.** This is the **ceiling**: no atmosphere can
make the substellar point hotter than the airless local-balance value (greenhouse
warming aside, which a thin atmosphere supplies only modestly). The real
substellar temperature sits *below* this once any redistribution carries heat
away.

### What sets the contrast: advection vs radiation

Between the Teq floor (perfect redistribution) and the T_ss ceiling (zero
redistribution), the controlling balance is **how fast the atmosphere moves heat
from day to night (advection) versus how fast it radiates that heat to space
(radiative cooling)**, a competition of timescales. Thicker atmospheres have
more mass and more momentum to advect heat and a longer radiative timescale, so
they redistribute more efficiently and the day-night contrast shrinks.

Key results, in order of how to use them:

- **Joshi, Haberle & Reynolds 1997**: the foundational GCM result that a modest
  atmosphere (≳ 0.1–0.3 bar of a CO₂-rich gas) transports enough heat to keep the
  night side from collapsing (i.e. from freezing out the atmosphere). Below that,
  the night side cools until the atmosphere condenses and the gas pressure runs
  away to collapse.

- **Wordsworth 2015**: develops the redistribution-vs-collapse theory and gives
  scaling expressions for the day-night temperature difference and the surface
  wind speeds. Identifies the atmospheric boundary layer as the key control on
  energy balance, and maps the parameter regime where atmospheric collapse occurs.

- **Koll & Abbot 2016**: treats the circulation as a planetary heat engine under
  the weak-temperature-gradient (WTG) approximation, yielding the day-night
  temperature structure and an upper bound on large-scale wind speeds for dry,
  tidally-locked rocky atmospheres.

- **Koll 2022**: the practical one. A **pressure-dependent day-night contrast
  scaling** that interpolates smoothly between the thin-atmosphere (large contrast)
  and thick-atmosphere (small contrast) limits, usable **without running a full
  GCM**. This is the tool that turns "0.7–1 bar" into an actual contrast estimate
  for a body that has no published GCM.

- **Haqq-Misra+ 2018**: demarcates the **circulation regime** (slow-rotator /
  Rhines-rotator / fast-rotator) from the planet's rotation rate and size. The
  regime governs *how* heat is carried (a single substellar cell vs. banded jets),
  so it sets the shape of the day-night field, not just its amplitude. Fix the
  regime before reading the contrast off Koll 2022.

- **Hammond+ 2022**: an **energy-balance model** for rapidly/synchronously
  rotating planets: a lightweight analytic alternative to a GCM that returns the
  full surface temperature field, useful as an independent cross-check on the
  Koll scaling.

- **Kite, Gaidos & Manga 2011**: maps the **instability/collapse** feedbacks; a
  reminder that the thin end of the pressure range is not just "more contrast" but
  can tip into runaway atmospheric collapse (the hard floor on Layer 2).

### Qualitative read for the NearStars-typical case

For a ~0.7–1 bar atmosphere (the order of magnitude assumed for several roster
terrestrials) the planet sits in the **partial-redistribution** regime: the
substellar region is warm but below the airless ceiling, the night side is cold
but **not** collapsed, and the global mean lands a little above the Teq anchor
once any greenhouse contribution is included. Thicker → flatter (toward Teq);
thinner → steeper (toward the T_ss ceiling on the day side, toward freeze-out on
the night side).

---

## 4. Layer 3: Body-Specific GCMs (Anchor Values)

When a target has a **published 3-D general circulation model**, adopt those
numbers: they supersede Layers 1 and 2 for that body, and they calibrate the
Layer-2 scaling for neighbours.

**Proxima b** is the best-anchored roster target:

| Source | Model | Substellar | Nightside | Global mean | Case |
|---|---|---|---|---|---|
| Turbet+ 2016 | LMD GCM | ~290 K | ~150 K | ~250 K | ~1 bar N₂ + CO₂ |
| Boutle+ 2017 | UK Met Office UM | ~290 K | ~150 K | ~250 K | ~1 bar N₂ + trace CO₂ |

Both independent GCMs converge on roughly **substellar ~290 K / nightside
~150 K / global mean ~250 K** for a ~1-bar nitrogen atmosphere with a CO₂ trace
and enough surface water for a substellar liquid pool. Note how this sits between
the Layer-1 anchor (Teq ≈ 230 K) and the Layer-2 ceiling (T_ss ≈ 336 K), exactly
as the partial-redistribution picture predicts.

For **other pressures**, scale qualitatively from these anchors using the Koll
2022 contrast scaling: a thicker atmosphere pulls substellar and nightside toward
the ~250 K mean (smaller amplitude); a thinner one pushes substellar up toward the
336 K ceiling and the night side down toward collapse. For roster planets with no
GCM (e.g. most TRAPPIST-1 worlds), the workflow is Layer 1 + Layer 2 anchored to
the nearest analogous GCM case rather than an invented number.

---

## 5. Climate-State Taxonomy

For water-bearing tidally-locked planets, the surface climate falls into a small
set of named states. The two controlling axes are **(a) atmospheric thickness /
heat-transport efficiency** and **(b) the surface water inventory**. Pick the
state on the Phase 4 board; it determines the albedo, the contrast, and where
liquid (if any) sits.

| Climate state | What produces it | Key ref |
|---|---|---|
| **Eyeball Earth** | Moderate water + weak transport: a circular open-ocean pool at the substellar point, ice everywhere else. The canonical locked-ocean state. | Pierrehumbert 2011 |
| **Lobster / asymmetric eyeball** | As eyeball, but **ocean** heat transport drags the warm pool downwind (eastward), distorting the circle into a lobster shape. | Hu & Yang 2014 |
| **Waterbelt / ice-covered ocean** | Stronger cooling: the substellar pool shrinks; open water survives only as a thin equatorial/terminator belt over an otherwise ice-covered ocean. | Yang+ 2013 (adjacent) |
| **Snowball** | Transport + albedo feedback freeze the whole surface, including the substellar point; globally ice-covered. **Caveat: a fully-locked *ocean* planet resists this**: the substellar melt pool persists (Checlair+ 2017), so true global snowball needs land at the substellar point or a very thin atmosphere. | Pierrehumbert 2011; Checlair+ 2017 |
| **Thick-atmosphere global ocean** | Massive atmosphere (or deep ocean) redistributes heat so efficiently that liquid water covers the planet day and night; small day-night contrast. | Yang+ 2013 |
| **Dune / land planet** | **Low water inventory** (arid, desert world): little water to freeze out or run away, so the habitable zone widens and the surface stays warm and dry rather than icing over. | Abe+ 2011 |
| **Terminator-ring habitability** | Day side too hot, night side frozen, but the ring at the day-night boundary holds moderate, potentially habitable temperatures. | Wordsworth 2015 (adjacent) |
| **Subsurface ocean under ice** | Surface frozen, but geothermal/tidal heat (or a thin insulating ice shell) sustains liquid water *beneath* the ice, a Europa-like reading. | Pierrehumbert 2011 (Super-Europa) |

---

## 6. How NearStars Applies This

The three-layer output maps directly onto the KSP/Kopernicus thermal model:

- **Teq + the substellar/night/mean split feed the temperature CURVES.** Kopernicus
  represents surface temperature as a base `temperatureCurve` plus latitude- and
  longitude-offset curves. The global-mean number sets the base level; the
  **substellar/nightside split sets the longitude-offset amplitude** (the
  day-night swing on a locked body shows up as a longitude dependence, since the
  substellar point is fixed). The amplitude itself comes from the lock plus the
  atmosphere, i.e. from the Layer-2/Layer-3 contrast, not from anything KSP
  computes on its own.

- **Record the chosen climate state and its parameters in the Phase 4 board.**
  The board entry must name the climate state (§5) and pin its controlling
  parameters: **albedo `A`, surface pressure, CO₂ fraction**, water inventory.
  These are art-direction choices gated by the literature, per the Phase 4 facet
  policy.

- **The temperature numbers are then `Teq` (computed, Layer 1) + `contrast`
  (Koll 2022 scaling, Layer 2), anchored to any body-specific GCM (Layer 3).**
  Where a GCM exists (Proxima b), the emit values are the GCM's substellar /
  nightside / mean. Where none exists, they are Layer 1 + Layer 2 with the chosen
  parameters, and the divergence from any analogous GCM is documented rather than
  silently assumed.

This keeps the emit deterministic and reproducible: every temperature on a locked
body traces back to a stated albedo/pressure/CO₂ choice and a cited scaling or GCM.

---

## 7. Annotated Bibliography

Each entry: authors, year, journal, **verified** arXiv id (or a flag where none
exists), and one line on what it contributes.

- **Joshi, M. M., Haberle, R. M. & Reynolds, R. T. (1997)**: *Icarus* 129, 450.
  **No arXiv (pre-arXiv-astro-ph-era planetary paper).** Foundational GCM result:
  a modest atmosphere prevents nightside atmospheric collapse on a locked planet.

- **Pierrehumbert, R. T. (2011)**: *ApJ Letters* 726, L8. No arXiv preprint;
  cite by ADS bibcode **2011ApJ...726L...8P** (the previously-circulated id
  1010.5052 is an unrelated mathematics paper: do not use it). "A Palette of
  Climates for Gliese 581g": defines the eyeball / snowball / Super-Europa
  climate states for a tidally-locked world.

- **Yang, J., Cowan, N. B. & Abbot, D. S. (2013)**: *ApJ Letters* 771, L45.
  **[arXiv:1307.0515](https://arxiv.org/abs/1307.0515).** Stabilizing substellar cloud feedback expands the inner
  habitable zone; supports the thick-atmosphere / waterbelt readings.

- **Hu, Y. & Yang, J. (2014)**: *PNAS* 111, 629. No arXiv preprint; cite by ADS
  bibcode **2014PNAS..111..629H** (the previously-circulated id [1312.3337](https://arxiv.org/abs/1312.3337) is
  Leconte+ 2013 on runaway greenhouse: do not use it). Ocean heat transport
  shifts the eyeball pool downwind: the "lobster" / asymmetric-eyeball state.

- **Kite, E. S., Gaidos, E. & Manga, M. (2011)**: *ApJ* 743, 41.
  **[arXiv:1109.2668](https://arxiv.org/abs/1109.2668).** Climate instability on tidally-locked planets: the
  feedbacks that can tip a locked atmosphere toward collapse (Layer-2 context).

- **Kopparapu, R. K. et al. (2016)**: *ApJ* 819, 84. **[arXiv:1602.05176](https://arxiv.org/abs/1602.05176).** Inner
  edge of the habitable zone for *synchronously rotating* planets: the
  locked-specific flux/HZ framing (more on-topic than the 2013 general HZ paper).

- **Haqq-Misra, J. et al. (2018)**: *ApJ* 852, 67. **[arXiv:1710.00435](https://arxiv.org/abs/1710.00435).**
  Demarcates the circulation regimes (slow-rotator / Rhines-rotator / fast-rotator)
  of synchronously rotating planets: the regime sets the day-night contrast
  structure, a direct Layer-2 input.

- **Checlair, J., Menou, K. & Abbot, D. S. (2017)**: *ApJ* 845, 132.
  **[arXiv:1705.08904](https://arxiv.org/abs/1705.08904).** "No Snowball on Habitable Tidally Locked Planets": the
  substellar melt region persists, so a fully-locked ocean planet resists global
  glaciation. This nuances the Snowball row in §5.

- **Yang, J. et al. (2019)**: *ApJ* 871, 29. **[arXiv:1902.02103](https://arxiv.org/abs/1902.02103).** Ocean dynamics
  and the inner edge of the habitable zone: ocean heat transport's role in the
  eyeball/lobster surface temperature field.

- **Hammond, M. et al. (2022)**: *PSJ* 3, 32. **[arXiv:2201.02685](https://arxiv.org/abs/2201.02685).** An energy
  balance model for rapidly and synchronously rotating planets, a lightweight
  analytic alternative to a full GCM for the day-night temperature field.

- **Abe, Y., Abe-Ouchi, A., Sleep, N. H. & Zahnle, K. J. (2011)**: *Astrobiology*
  11, 443. **No arXiv preprint found.** "Habitable zone limits for dry planets":
  low-water-inventory land/dune worlds have a wider habitable zone than aqua
  planets.

- **Wordsworth, R. (2015)**: *ApJ* 806, 180. **[arXiv:1412.5575](https://arxiv.org/abs/1412.5575)** (the
  previously-circulated id 1505.07087 is incorrect). Atmospheric heat
  redistribution and collapse theory; scaling for day-night ΔT and surface winds.

- **Koll, D. D. B. & Abbot, D. S. (2016)**: *ApJ* 825, 99. **[arXiv:1605.01066](https://arxiv.org/abs/1605.01066)**
  (the previously-circulated id 1603.05229 is incorrect). WTG + heat-engine model
  of the day-night temperature structure and wind speeds for dry locked rocky
  atmospheres.

- **Koll, D. D. B. (2022)**: *ApJ* 924, 134. **[arXiv:1907.13145](https://arxiv.org/abs/1907.13145).** Pressure-
  dependent day-night contrast scaling usable without a full GCM (thicker
  atmosphere → smaller contrast). The Layer-2 workhorse.

- **Turbet, M. et al. (2016)**: *A&A* 596, A112. **[arXiv:1608.06827](https://arxiv.org/abs/1608.06827).** LMD GCM
  of Proxima b; substellar ~290 K / nightside ~150 K / mean ~250 K for ~1 bar
  N₂+CO₂. Layer-3 anchor.

- **Boutle, I. A. et al. (2017)**: *A&A* 601, A120. **[arXiv:1702.08463](https://arxiv.org/abs/1702.08463).** UK Met
  Office Unified Model of Proxima b; independent confirmation of the Turbet+ 2016
  temperature structure. Layer-3 anchor.

- **Kopparapu, R. K. et al. (2013)**: *ApJ* 765, 131 (erratum *ApJ* 770, 82).
  **[arXiv:1301.6674](https://arxiv.org/abs/1301.6674).** Habitable-zone boundary estimates; sets the flux context
  (`S`) and inner/outer-edge framing used in Layer 1.

- **Ho, S. & Turner, E. L. (2011)**: *ApJ* 739, 26. **[arXiv:1007.0245](https://arxiv.org/abs/1007.0245).** Related
  (not climate): the statistical RV minimum-mass → true-mass deprojection method,
  used elsewhere in the pipeline to turn `m sin i` into a mass for these planets.

---

## Related

- [exoplanet-atmosphere-methodology](exoplanet-atmosphere-methodology.md): the sibling recipe for
  the surface pressure, mean molecular weight (μ) and scale height of the same
  rocky atmospheres; the temperature `T` from here feeds its scale-height formula.
- [binary-epoch-pipeline](binary-epoch-pipeline.md): epoch/state-vector handling for
  multiple-star hosts (Proxima orbits α Cen AB).
- [solar-system-external-observer](solar-system-external-observer.md): the Teq-blind-to-greenhouse
  calibration benchmark (Venus: Teq 227–299 K vs actual 737 K) that motivates the
  "Teq ≠ surface T" warning in §1.
- Phase 3 synthesis skill (`nearstars-phase3`): where the chosen albedo /
  pressure / CO₂ fraction and the emit temperature numbers are recorded per planet.
- [methodology-index](methodology-index.md) — the index of all derived-value methodology recipes.
