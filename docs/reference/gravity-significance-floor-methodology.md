<!-- Principia far-field gravity 절단(a_floor·shell ratio)을 문헌으로 근거화한 방법론 문서 -->
# Gravity Significance Floor: Methodology & Literature Grounding

This note grounds **two numerical parameters** of a per-pair far-field gravity-truncation
scheme built into a Principia (KSP n-body) fork:

1. the **acceleration floor** `a_floor` (provisionally `1e-12 m/s²`), and
2. the **switching-shell width ratio** outer/inner (provisionally `3`).

Both were placeholders. This document collects the literature that either justifies them
or supplies a defensible replacement, so the parameters can be set from the evidence alone.

> Discipline: every load-bearing number is pinned to an ADS bibcode (+ arXiv id where one
> exists) and, where it fixes a number, a short verbatim quote. Textbook relations
> (Newtonian two-body acceleration, the Jacobi radius) are the allowed exception to
> "derived values must be paper-grounded." Standard for the [methodology index](methodology-index.md).

## The mechanism being grounded (context)

Each body gets a cutoff radius **`r_c = √(μ / a_floor)`**: the distance where its
point-mass acceleration `μ/r²` falls to the floor `a_floor`. The **potential** (not the
force) is multiplied by a C² quintic sigmoid σ: untouched below `r_c/3`, smoothly ramped on
`[r_c/3, r_c]`, **exactly zero** beyond `r_c`. For massive–massive pairs one σ is applied
symmetrically to both members (Newton's third law → momentum exact), with the pair cutoff at
`max(r_c_a, r_c_b)`. Consequences: an asteroid never stops feeling its star (the star's `r_c`
dominates); asteroid↔asteroid and star↔star-across-lightyears pairs vanish; asteroid↔planet
pairs survive (planet `r_c ≈ 133 AU`), so a belt's collective effect on planets is retained.

Design goals: (a) make vessels in the interstellar void **exactly** force-free, and (b) stop
spending computation on physically meaningless pairs (hundreds of RSS-Origin asteroids all
perturbing each other and a 40-ly-distant system).

Profile to weigh against: gameplay up to ~centuries of timewarp; **player-measurable
quantities are relative** in-simulation quantities (orbits, encounters, maneuver planning),
not absolute coordinates; worst identified drift ≈ **500 m/yr** (coherent worst case at the
cutoff boundary, at `a_floor = 1e-12`).

Reference scales (all derived from `r_c = √(μ/a_floor)`, `μ_☉ = 1.327e20 m³/s²`):

| `a_floor` (m/s²) | `r_c(1 M☉)` | `r_c(2.01 M☉)` | `r_c(asteroid, μ=1e9)` |
|---|---|---|---|
| `1e-11` | 0.385 ly (0.118 pc) | 0.546 ly | 0.067 AU |
| `1e-12` (provisional) | 1.218 ly (0.373 pc) | 1.726 ly | 0.211 AU |
| `1e-13` | 3.850 ly (1.180 pc) | 5.459 ly | 0.668 AU |

---

## A. Planetary-ephemeris perturber selection (the strongest precedent)

The strongest precedent, JPL's DE series, selects perturbers by their **positional effect
on a specific observed baseline (the Mars orbit / Earth–Mars range), not by a mass threshold
or an acceleration cutoff**, and then simply **drops** the sub-threshold remainder. DE430/431
and DE440/441 integrate the same 343 asteroids individually: *"Perturbations from 343
asteroids have been included… The set… represents 90 percent of the total mass of the main
belt and contains the asteroids with the most significant effects on the orbit of Mars in
terms of perturbation amplitude and frequency"* (Folkner et al. 2014, `2014IPNPR.196C...1F`).
Park et al. carry the set forward unchanged: *"The 343 asteroids were the same set… which
consist of ∼90% of the total asteroid-belt mass"* (Park, Folkner, Williams & Boggs 2021,
`2021AJ....161..105P`). DE uses **no main-belt ring**: the remaining ~10% of belt mass is
neglected outright; DE440 adds only a *Kuiper* aggregate (30 individual KBOs + a 36-point ring
at 44 AU).

The quantitative threshold is stated most explicitly in the ring literature underlying DE and
INPOP. Kuchynka et al. 2010 (`2010A&A...514A..96K`) fix a main-belt ring at 2.8 AU of mass
`Mring = 0.6±0.2×10⁻¹⁰ M☉`, and quantify the residual: modeling the top asteroids plus one ring
captures *"more than 99% of the global perturbation"* on the inner planets, reducing the
neglected-asteroid signal on the Earth–Mars range *"to 38 m"* (amplitude selection, N=300) or
*"4 m for N=300"* (MIQP selection), i.e. of order **1 metre over a decade**. Individual
objects dominate that budget: Ceres alone reaches ~1199 m on the Earth–Mars distance over
1970–2010 (Fienga et al. 2011, `2011CeMDA.111..363F`). So the *operative* threshold is a
**~1–40 m positional effect over the multi-decade data span**, applied per body.

INPOP applies the same position-effect logic with an explicit metre floor: *"approximately 240
asteroids… should represent the perturbations induced by the main belt on planetary orbits
down to an order of a meter"* (`2011CeMDA.111..363F`), with the sub-threshold remainder
aggregated via the Kuchynka ring; by INPOP19a the individual set grew to 343 plus a Kuiper ring
of `(0.061 ± 0.001) M⊕` (Di Ruscio et al. 2020, `2020A&A...640A...7D`). EPM likewise splits
individual + aggregate: 301 large asteroids plus a rotating ring at 2.67 AU of mass
`(0.507 ± 0.051)×10⁻¹⁰ M☉`, against a total belt mass `(12.038 ± 0.087)×10⁻¹⁰ M☉` (Pitjeva &
Pitjev 2018, `2018AstL...44..554P`).

**Relevance to our fidelity.** Two points transfer directly. First, the ephemeris precedent
selects by *positional effect on the measured relative baseline over the integration span*,
exactly the quantity our profile cares about (relative in-sim orbits/encounters), not by an
acceleration floor; our `a_floor`/`r_c` scheme is a coarser proxy for the same intent. Second,
the drop-vs-aggregate choice only becomes load-bearing at the **~1–40 m** level these teams
target: JPL judges dropping ~10% of belt mass acceptable at metre fidelity, and the ring
recovers the last ">99%" precisely because sub-metre absolute accuracy demands it. At our
tolerance (~500 m/yr, relative), we sit **2–3 orders of magnitude looser** than the regime
where aggregation earns its keep, so **dropping the sub-cutoff far-field tail entirely is well
within precedent**, a ring exists only to chase metre-level *absolute* accuracy we do not need.

> **Numbers extracted**
> - **343**: asteroids integrated individually in DE430/431 & DE440/441 (≈90% of belt mass) (`2014IPNPR.196C...1F`; `2021AJ....161..105P`)
> - selection = "most significant effects on the orbit of Mars…"; remaining ~10% **dropped**, no main-belt ring in DE (`2014IPNPR.196C...1F`)
> - **4–38 m**: residual Earth–Mars range effect after one ring absorbs the sub-threshold tail (N=300); ">99% of global perturbation" captured (`2010A&A...514A..96K`)
> - ~1199 m: largest single-asteroid (Ceres) effect on Earth–Mars distance, 1970–2010 (`2011CeMDA.111..363F`)
> - ~240 asteroids "down to an order of a meter": INPOP metre-level individual-perturber threshold (`2011CeMDA.111..363F`)
> - 301 individual + ring at 2.67 AU `(0.507±0.051)×10⁻¹⁰ M☉`; total belt `(12.038±0.087)×10⁻¹⁰ M☉`, EPM (`2018AstL...44..554P`)

---

## B. Detectability bound: the smallest coherent acceleration ever measured

The most sensitive coherent acceleration ever extracted from a natural body is the Yarkovsky
drift on asteroid (101955) Bennu, and it lands almost exactly at our proposed floor. Chesley
et al. measure *"da/dt=(-19.0±0.1)×10⁻⁴ au/Myr or 284±1.5 m/year"* from optical astrometry
spanning 1999–2013 plus radar delay at three apparitions (`2014Icar..235....5C`). The
underlying transverse nongravitational acceleration (JPL parameter A2) is
`−4.618(24)×10⁻¹⁴ au/day²` ≈ **9.3×10⁻¹³ m/s²**: the best-determined Yarkovsky detection in
the literature, at signal-to-noise ~200 (Farnocchia et al. 2013, `2013Icar..224....1F`: *"The
best determination is for asteroid (101955) 1999 RQ₃₆, with an SNR ∼ 200"*). Reaching it
required decade-scale radar ranging at ~75–300 m delay precision per apparition.

The first-ever direct detection set the same regime a decade earlier: Chesley et al. detected
Yarkovsky on the 0.5-km asteroid 6489 Golevka via *"Radar ranging from Arecibo… [which]
unambiguously reveals a small nongravitational acceleration"* (`2003Sci...302.1739C`), again
only via radar over a ~12-year, three-apparition baseline. Catalog surveys confirm this is the
sensitivity *edge*, not a typical value: only *"21 NEAs whose orbital fits show a measurable
orbital drift with a signal to noise ratio (SNR) greater than 3"* (`2013Icar..224....1F`), and
Nugent et al. report *"observed drifts (~10⁻³ AU Myr⁻¹)"* across 54 NEAs, order ~10⁻¹³ m/s²
transverse (`2012AJ....144...60N`). So the natural-body detectability floor spans roughly
**10⁻¹³–10⁻¹² m/s²**, reached only via multi-decade radar ranging to specifically-tracked
objects whose absolute positions are externally known to tens of metres.

The classic spacecraft-tracking datum sits nearly three orders higher: the Pioneer anomaly
*"a_P=(8.74±1.33)×10⁻⁸ cm/s²"* = **8.74×10⁻¹⁰ m/s²** from Doppler + ranging over ~11.5 yr
(Anderson et al. 2002, `2002PhRvD..65h2004A`), and even that proved an artifact: *"once the
thermal recoil force is properly accounted for, no anomalous acceleration remains"* (Turyshev
et al. 2012, `2012PhRvL.108x1101T`). That a 8.7×10⁻¹⁰ m/s² signal turned out to be spacecraft
self-heating shows how hard genuine coherent accelerations at that level are to establish.

**Placement of our floor.** `a_floor = 1×10⁻¹² m/s²` is essentially at the magnitude of the
single most sensitive acceleration ever measured (Bennu, ~9×10⁻¹³) and ~880× below the Pioneer
anomaly. Raw-magnitude-wise it is therefore *not comfortably below* detectability: it
coincides with the observational frontier. **But that frontier was purchased by ~12 years of
external radar ranging to one tracked body at ~75 m precision, against an independently known
heliocentric ephemeris.** The game exposes none of that apparatus: player measurables are
relative, self-referential in-sim orbits/encounters (worst drift ~500 m/yr), with no external
absolute-position anchor and no decade-long radar baseline. The floor is thus **operationally
undetectable in the game's measurement regime** even though its magnitude equals the state of
the art, and the damping only bites *below* `r_c`, where per-pair accelerations are ≤ `a_floor`
by construction.

> **Numbers extracted**
> - **9.3×10⁻¹³ m/s²**: Bennu transverse Yarkovsky accel (A2 = −4.618×10⁻¹⁴ au/day²), best natural-body detection, SNR~200 (`2014Icar..235....5C`)
> - 284 ± 1.5 m/yr: Bennu semimajor-axis drift, 1999–2013 optical + 3-apparition radar (`2014Icar..235....5C`)
> - ~75–300 m: radar delay precision per apparition enabling the Bennu detection (`2014Icar..235....5C`)
> - ~10⁻³ AU/Myr (~10⁻¹³ m/s²): typical measured Yarkovsky drift across 54 NEAs (`2012AJ....144...60N`)
> - SNR > 3 for only 21 NEAs: statistical detection threshold for Yarkovsky in orbital fits (`2013Icar..224....1F`)
> - first direct Yarkovsky detection, Arecibo radar, 0.5-km Golevka (`2003Sci...302.1739C`)
> - **8.74×10⁻¹⁰ m/s²**: Pioneer anomaly, Doppler+ranging over ~11.5 yr; later resolved as thermal recoil (`2002PhRvD..65h2004A`; `2012PhRvL.108x1101T`)

---

## C. Stellar dynamics: where star–star gravity stops being meaningful physics

The relevant physical scale is the **Jacobi (tidal) radius**, the separation at which the
Galactic tidal acceleration across a pair matches the pair's mutual gravity. Jiang & Tremaine
(2010, `2010MNRAS.401..977J`) define `r_J ≡ [G(M₁+M₂)/(4 Ω_g A_g)]^(1/3)` and evaluate it for
the solar neighborhood: it *"equals 1.7 pc = 3.5×10⁵ AU for solar-mass stars"*, i.e. for a
total mass `M₁+M₂ = 2 M☉`, using `Ω_g ≈ 27`, `A_g ≈ 15 km/s/kpc` at `R_g = 8 kpc`. Their
simulations find the population *"exhibits a minimum at a few times the Jacobi radius r_J"*,
so the observable bound-pair population is effectively truncated at ≈ `r_J`.

**Crossover for a 1+1 M☉ pair: `r_J = 1.7 pc = 5.5 ly`**, where both the mutual and tidal
accelerations are ≈ **1×10⁻¹³ m/s²**. This crossover acceleration is the physically motivated
floor. The *observed* wide-binary cutoff sits somewhat inside it, at ~0.1–1 pc: common-proper-
motion pairs follow a single power law `dN/dΔθ ∝ Δθ^(−α)` with *"α = 1.67 ± 0.07 for the disk"*
out to ~1 pc (Chanamé & Gould 2004, `2004ApJ...601..289C`); El-Badry's Gaia review
(`2024NewAR..9801694E`, [arXiv:2403.12146](https://arxiv.org/abs/2403.12146)) reports the same slope and notes bound pairs are
cleanly identifiable only to `s ≈ 5×10⁴ AU (≈0.24 pc)`, with pairs *"≳10⁵ au … mostly chance
alignments, not gravitationally bound."* Encounters plus the tide grind down the widest pairs
over Gyr (Weinberg, Shapiro & Wasserman 1987, `1987ApJ...312..367W`), so the observed widest
bound binaries (~1 pc) lie a factor of a few below the formal `r_J` (1.7 pc).

**Where `r_c` lands.** `a_floor = 1×10⁻¹²` gives `r_c(1 M☉) = 0.37 pc = 1.2 ly`
(`≈0.53 pc = 1.7 ly` for a 2 M☉ pair). Either way `r_c` sits **well *inside* the tidal-crossover
radius** (0.37–0.53 pc vs 1.7 pc), a factor ~3–5 too small to be "matched" to the tide. At the
provisional `r_c` the bare two-body term (~10⁻¹² m/s²) still exceeds the Galactic tide there
(~3×10⁻¹⁴ m/s², `a_tide/a_mut ≈ 0.03`) by more than an order of magnitude, so the Newtonian
two-body term is still the dominant physics at 1.2 ly. **The tidal argument therefore does not
uniquely justify 1e-12; it justifies a floor closer to ~1×10⁻¹³ m/s²**, which pushes `r_c(1 M☉)`
to ≈1.2 pc (~4 ly) and `r_c(2 M☉)` to ≈1.7 pc, aligning the cutoff with the Jacobi radius. As
set, the mod truncates *earlier* than the tide would, conservative (it never keeps a far-field
term the tide should have dominated), but not matched to the tidal scale.

> **Numbers extracted**
> - **1.7 pc = 5.5 ly**: Jacobi (tidal) radius for a 2 M☉ (1+1) pair in the solar neighborhood (`2010MNRAS.401..977J`)
> - `r_J = [G(M₁+M₂)/(4 Ω_g A_g)]^(1/3)`, `Ω_g ≈ 27`, `A_g ≈ 15 km/s/kpc`: formula + Oort inputs (`2010MNRAS.401..977J`)
> - **~1×10⁻¹³ m/s²**: mutual = tidal acceleration at the crossover (physically motivated floor) (derived from `2010MNRAS.401..977J`)
> - α = 1.67 ± 0.07 (disk), single power law to ~1 pc: observed wide-binary separation distribution (`2004ApJ...601..289C`)
> - bound to ~5×10⁴ AU (~0.24 pc); ≳10⁵ AU mostly chance alignments: observed max bound separation (`2024NewAR..9801694E`)
> - `r_c(1 M☉) = 0.37 pc` vs `r_J = 1.7 pc`: `r_c` is ~4.6× *inside* the tidal crossover (two-body term still dominant there) (comparison vs `2010MNRAS.401..977J`)

---

## D. N-body force-error tolerances and outer-truncation precedent

**Long-term integration error budgets sit between machine precision and ~10⁻⁹.** IAS15 keeps
*"systematic errors…well below machine precision"* and follows Brouwer's law, with an internal
convergence tolerance ε ≡ 10⁻¹⁶ but a deliberately relaxed *"default value of ε_b = 10⁻⁹"*
(Rein & Spiegel 2015, `2015MNRAS.446.1424R`). WHFast is engineered so *"E_bias is absent… its
implementation is completely unbiased"* and conserves relative energy *"better by two to three
orders of magnitude"* than the classic Wisdom–Holman map (Rein & Tamayo 2015,
`2015MNRAS.452..376R`; foundational method: Wisdom & Holman 1991, `1991AJ....102.1528W`). So the
community *target* relative energy/force error for conservative long-term work is ~10⁻⁹, with the
achievable floor at 10⁻¹⁵–10⁻¹⁶.

**Collisionless force-accuracy standards are far looser: a few ×10⁻³.** Dehnen 2002
(`2002JCoPh.179...27D`) states *"in collisionless stellar dynamics a relative force error of few
10⁻³ is often sufficient,"* achieved at opening angle `θ ≃ 0.5–0.65`; Barnes & Hut 1986
(`1986Natur.324..446B`) and its error analyses established that galaxy/cluster codes routinely
run at ~0.1–1% per-particle force error. The accepted tolerance band thus spans ~10⁻³
(collisionless) down to ~10⁻⁹ (planetary target) and ~10⁻¹⁵ (integrator roundoff floor).

**Where the `a_floor` bias sits.** As a relative force error at 1 AU from a solar mass:
`GM_☉/r² = 5.93×10⁻³ m/s²`, so `a_floor / (GM/r²) = 1e-12 / 5.93e-3 =` **1.7×10⁻¹⁰**. This static
bias is ~7 orders *below* the tree-code collisionless tolerance, comfortably below the
WHFast/IAS15 default accuracy parameter (10⁻⁹), and only ~5 orders above the double-precision
roundoff floor. It is largest at 1 AU and shrinks as 1/r² inward (≈1.7×10⁻¹² at 0.1 AU,
effectively at roundoff), and it appears only near the per-pair cutoff shell, not globally. By
any published standard a 1.7×10⁻¹⁰ relative bias is negligible against the errors production
integrations already tolerate.

**Verdict on the shell-width ratio: no literature basis.** There is a rich literature on
*splitting* gravity into short- and long-range parts (Ewald summation, P³M/TreePM handovers,
MOND interpolating functions), but these tune a split scale for speed/accuracy of the *full*
force; **none define, or offer guidance on, the width of a smooth C² shell that drives gravity to
*exactly zero* beyond an outer radius.** No paper prescribing an outer/inner shell-width ratio
for a smooth gravity cutoff was found. The 3× ratio (`r_c/3 → r_c`) is a HarmonicDamping
convention with no astrophysical or numerical-analysis precedent; **it should remain justified
solely by the fork's internal energy-conservation / drift tests, not by any claimed literature
standard.**

> **Numbers extracted**
> - **1.7×10⁻¹⁰**: `a_floor(1e-12)` as relative force error at 1 AU / 1 M☉ (`GM/r²=5.93×10⁻³ m/s²`) (derived)
> - 10⁻⁹: WHFast/IAS15 default user accuracy parameter `ε_b` (`2015MNRAS.446.1424R`)
> - 10⁻¹⁶: IAS15 internal convergence tolerance ≈ double-precision machine ε (roundoff floor) (`2015MNRAS.446.1424R`)
> - 2–3 orders: WHFast relative-energy improvement over classic WH map; unbiased, Brouwer scaling (`2015MNRAS.452..376R`)
> - few×10⁻³: accepted relative *force* error for collisionless tree codes at `θ ≃ 0.5–0.65` (`2002JCoPh.179...27D`; `1986Natur.324..446B`)
> - **(empty)**: no literature basis for the smooth outer-truncation shell-width ratio; keep 3× justified by internal tests only

---

## E. Operational spacecraft-navigation force models (secondary)

Real navigation force models draw a hard line at a small, fixed set of perturbers rather than
"all bodies." JPL's deep-space orbit-determination formulation (Moyer, DESCANSO Monograph 2)
integrates spacecraft and planetary trajectories under the Sun, eight planets, Moon, Pluto, and
exactly **16 massive asteroids** (the "Big-16": Ceres, Pallas, Vesta, Iris, Bamberga, …),
selected as the only asteroids large enough to measurably bias inner-solar-system / Mars-mission
arcs; everything smaller is dropped. That is deliberately far coarser than the *ephemeris* it
rides on: DE440 carries **343 asteroids + 30 KBOs + a KBO ring** (`2021AJ....161..105P`), ~20×
more perturbers than the navigation model bothers to include. Community tools mirror the "add
only what you need" discipline: NASA GMAT's `ForceModel` ships an **empty `PointMasses` list by
default** (analyst enumerates third bodies, typically `{Sun, Luna, Jupiter}`, no asteroids), and
Orekit's `CelestialBodyFactory` predefines only Sun, Moon, eight planets and Pluto as point
masses, with asteroids added only by hand.

> **Numbers extracted**
> - **16**: "Big-16" massive asteroids in the JPL DSN deep-space OD force model (+ Sun, 8 planets, Moon, Pluto) (Moyer, DESCANSO Monograph 2)
> - **343 + 30 KBOs + ring**: perturbers in the underlying DE440 ephemeris (~20× the nav model) (`2021AJ....161..105P`)
> - `PointMasses = {}` default, no default asteroids: GMAT `ForceModel` (GMAT R2020a User's Guide)
> - Sun + Moon + 8 planets + Pluto as point masses, no built-in asteroids: Orekit `CelestialBodyFactory` (Orekit architecture docs)

---

## Synthesis: the design answer

### Criterion type

The gold-standard practice (angle A) selects perturbers by their **positional effect on the
measured relative baseline over the integration span** (an *observable-effect* criterion) and
**drops** whatever falls below it. That is exactly the quantity our profile cares about (relative
in-sim orbits/encounters, not absolute coordinates). But the ephemeris criterion presumes a
concrete measurable (Earth–Mars range) and a data span; a sandbox game has no single such
baseline, and needs the void to be **exactly** force-free, which only a hard cutoff delivers.

**Recommendation: keep the absolute acceleration floor as the primary criterion**, understood as
a roster-independent, O(1)-cheap *proxy* for the observable-effect rule. It is the only one of the
three options that makes the interstellar void exactly force-free (goal a). The relative-
significance rule (option 2, R3's `a_pair/a_dominant < ε` vessel-path rule) remains the right tool
for the *integration/vessel* side and composes with (does not replace) the floor. The
observable-effect rule (option 3) is the conceptual justification for the floor's *value*, not a
separate runtime mechanism.

### Value: `a_floor = 1×10⁻¹² m/s²` (keep the provisional), acceptable range `[1×10⁻¹³, 1×10⁻¹¹]`

The provisional value turns out to be well-placed, sitting at the confluence of three independent
bounds:

- **Below detectability in-game (B).** 1e-12 coincides with the *observational* frontier (Bennu,
  ~9×10⁻¹³ m/s²), but that frontier required 12 yr of external radar ranging against a known
  ephemeris, apparatus the game has no analogue for. Nothing the player can measure (relative
  orbits/encounters) is affected.
- **Conservative w.r.t. the Galactic tide (C).** `r_c(1 M☉) = 1.2 ly` sits *inside* the 5.5-ly
  Jacobi radius, so the fork never keeps a far-field term in the regime the (unmodeled) tide
  should dominate.
- **Negligible as a force bias (D).** 1.7×10⁻¹⁰ relative error at 1 AU, 7 orders below tree-code
  tolerance.
- **Achieves the compute win (A/E).** `r_c(asteroid, μ≈1e9) = 0.21 AU`, well below typical belt
  spacing, so asteroid↔asteroid pairs die; asteroid↔planet survive. Dropping the sub-cutoff tail
  (no ring) is within ephemeris precedent, since we are 2–3 orders looser than the ~1–40 m regime
  where aggregation earns its keep.

**What each end of the range trades:**

| `a_floor` | `r_c(1 M☉)` | Character | Trade |
|---|---|---|---|
| `1e-13` | 3.85 ly | **Physically matched**: `r_c(2 M☉)=5.5 ly` aligns with the Jacobi radius; cut exactly where the tide overtakes the two-body term (C). | Larger `r_c` ⇒ more surviving pairs. `r_c(asteroid)=0.67 AU` ≈ belt spacing, so the asteroid↔asteroid decoupling weakens (more pairs survive), erodes the compute win. Boundary drift ~10× smaller (~50 m/yr). |
| `1e-12` | 1.2 ly | **Recommended**: detectability-floor-aligned, conservative vs tide, kills asteroid↔asteroid, roster clears 8×. | Truncates ~4.6× inside the tidal radius (cuts a two-body-dominant but game-irrelevant, sub-detectable regime). |
| `1e-11` | 0.39 ly | **Max-compute**: smallest `r_c`, fewest surviving pairs, still below in-game detectability and still roster-safe. | Boundary drift ~10× larger (~5 km/yr); roster margin thins to 2.6× on AB–Proxima; nearing the `<7×10⁻¹¹` hard roster limit. |

The lower bound of the range (1e-13) is the *most physically principled* choice (matches the
tidal scale); the recommended 1e-12 trades ~1.5 dex of "physical matching" for a materially better
asteroid↔asteroid compute win and an 8× roster margin, while remaining sub-detectable. Do **not**
exceed ~1e-11: at `a_floor = 7×10⁻¹¹` the cutoff `r_c(2.01 M☉)` drops to the AB–Proxima apoapsis
and would unbind the roster's widest real pair.

### Roster sanity check (verified against `db/binary_orbits.json`)

Requirement: no bound binary wider than the `r_c` of its (more massive) primary. **Verified** for
`a_floor = 1e-12`. The binding case is the Alpha Centauri outer orbit; every other pair clears by
750–8000×.

| System | Pair | Separation | Primary | `r_c` | Margin |
|---|---|---|---|---|---|
| Alpha Centauri | **AB–Proxima** | a = 8700 AU = **0.138 ly**; e = 0.5 ⇒ apoapsis ≈ 13,050 AU ≈ **0.206 ly** | AB (2.01 M☉) | 1.73 ly | **8.4×** (at apoapsis) |
| Sirius | AB | 19.8 AU | 2.06 M☉ | 1.75 ly | ~5600× |
| Procyon | AB | 15.1 AU | 1.50 M☉ | 1.49 ly | ~6200× |
| 61 Cygni | AB | 85 AU | 0.71 M☉ | 1.02 ly | ~760× |
| Eta Cassiopeiae | AB | 90 AU | 0.97 M☉ | 1.20 ly | ~850× |
| (all others: 40 Eri BC, 36 Oph AB, 70 Oph AB, Luhman 16, ε Ind B) | – | ≤ 35 AU | – | – | > 1600× |

The tightest margin (AB–Proxima, 8.4×) is the constraint that caps `a_floor` from above at ~1e-11
if a ≥3× margin is required.

### Shell-width ratio

**No literature basis exists** (angle D) for the width of a smooth outer-truncation shell: the
gravity-splitting literature (Ewald, P³M/TreePM, MOND) concerns accuracy-preserving reformulations
of the full force, not a physical outer cutoff. **Recommendation: keep the outer/inner = 3
HarmonicDamping convention, and justify it explicitly by the fork's internal energy-conservation
and boundary-drift tests, not by any claimed external standard.** This absence is itself a
finding: we own the choice, backed by our own tests.

## Related

- [methodology-index](methodology-index.md): index of paper-grounded derived-value recipes.
- [principia-cfg-reference](principia-cfg-reference.md) / [principia-geopotential-data](principia-geopotential-data.md): the n-body gravity-model cfg conventions this truncation scheme extends.
- [binary-epoch-pipeline](binary-epoch-pipeline.md): the source of the `db/binary_orbits.json` roster used in the sanity check.

## Addendum (2026-07-04): roster also caps the floor from BELOW; 1e-13 rejected

Owner considered adopting the "physically matched" lower end (`1e-13`, r_c aligned with the
Jacobi radius). Rejected on roster geometry:

- At `1e-13`, `r_c(1 M☉) = 3.85 ly` and `r_c(α Cen AB, 2.01 M☉) = 5.46 ly` **exceeds the
  Sol–α Cen separation (4.37 ly)**, Sol itself sits inside α Cen's cutoff, and no point of
  the flagship route is exactly force-free (the two shells jointly cover the whole void).
  This defeats design goal (a). It also erodes goal (b): `r_c(asteroid) = 0.67 AU` is at
  belt-neighbor spacing, so asteroid↔asteroid pairs survive *inside the σ shell* (costlier
  than no cutoff).
- **Void-zero existence condition**: a force-free segment on a route requires
  `r_c(A) + r_c(B) < d(A,B)`. For Sol–α Cen (4.37 ly, 1 + 2.01 M☉) this demands
  **`a_floor ≥ ~5e-13 m/s²`** (at 5e-13 the sum is 4.16 ly, zero-segment width ~0.2 ly;
  at 1e-12 it is 2.95 ly, width ~1.4 ly).
- Combined with the upper cap from AB–Proxima binding (~1e-11, §Roster sanity check), the
  **roster-admissible window is `[≈5e-13, ≈1e-11]`**; `1e-13` lies outside it, `1e-12`
  sits comfortably inside. Decision (owner, 2026-07-04): **keep `a_floor = 1e-12 m/s²`.**
