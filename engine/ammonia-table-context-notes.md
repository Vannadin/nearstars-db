# The ammonia table — context notes (C4, reopened for ammonia)

C4 closed on 2026-08-30 *unbuilt*: the ammonia source was behind a paywall and an author
request looked like the only route. The registered overturn condition fired the same day —
the owner obtained the paper and **the table is printed inside it**. C4 reopened for the
ammonia half only; this is its build. The methane half was then re-stated from its own
full text at the owner's direction (below), still unbuilt.

## Provenance

Bethkenhagen, French & Redmer 2013, *Equation of state and phase diagram of ammonia at high
pressures from ab initio simulations*, J. Chem. Phys. 138, 234504
([`2013JChPh.138w4504B`](https://ui.adsabs.harvard.edu/abs/2013JChPh.138w4504B), doi
[10.1063/1.4810883](https://doi.org/10.1063/1.4810883)); cached at
`docs/phase3/_papers/2013JChPh.138w4504B.pdf`, first page "J. Chem. Phys. 138, 234504
(2013)" with the title above; bibcode checked by title. The repository now carries two
Bethkenhagen papers — every label below says which.

**Appendix B, Table I** is the distribution. Grep of the full text finds no repository, no
data-availability statement and no analytic fit. The table is 93 rows of (ρ g/cm³, T K, p GPa,
u kJ/g) across two pages; `pdftotext -layout` recovers all 93 with no duplicates and no
misses (plain `pdftotext` scatters the columns). The parser in
`engine/tools/make_ammonia_table.py` requires exactly 93 rows, eleven temperatures, nine
densities, the six absent cells absent, and ten asterisks; `test_ammonia.py` compares eight
rows read from the rendered page by eye — a second path, independent of the text layer —
plus the flagged set, the counts and the ragged edge.

The grid, from the printed table (not the parallel session's parse, which agreed):

```
T (K)      500  700  1000 2000 3000 4000 5000 6000 7000 8000 10000
ρ (g/cm³)  0.5 · 0.75 · 1.0 · 1.3 · 1.5 · 1.8 · 2.0 · 2.5 · 3.0
500 K   ρ ≤ 1.5 (5 points) · 700 K   ρ ≤ 2.0 (7) · 1000 K and above   all 9
p  0.309 – 333.2 GPa
```

**Uncertainty, in the paper's words** (Appendix B): *"In general, the pressure is converged
within an error bar of 2%, except for the data points marked with asterisk, which have an
uncertainty of up to 5%. The caloric EOS is of the same quality as the pressure."* Five rows
carry the asterisk, on p and u both — (0.5, 4000), (0.75, 4000), (1.0, 4000), (0.5, 5000),
(0.75, 5000) — the hot, rarefied corner. The flag rides on each row of `ISOTHERMS` and
`ammonia_table.uncertainty(ρ, T)` returns 5 % whenever the interpolation touches a flagged
point, 2 % otherwise; the material exposes it as `NH3.uncertainty(P, T)`. None of the eight
ice-giant-mantle check points below touches a flagged row.

## The convention — chosen, stated, testable

The two Bethkenhagen papers publish this ammonia under different conventions:

- 2013, Appendix B: *"The latter one [the caloric EOS] includes the vibrational correction
  u^vc_vv(ρ, T) based on the power spectra that were computed self-consistently from the
  simulations"*; Fig. 7 caption: *"The presented data already include the vibrational
  correction"*; eq. (1) u = u* + u_vc.
- 2017, §II.4 (`docs/phase3/_papers/1709.04133.md`): *"the correction due to nuclear quantum
  effects was removed from the published data set (Bethkenhagen et al. 2013)"*.

**Chosen: the printed values, correction included.** They are the only values printed, and
they are the physically corrected ones (the paper's Hugoniot comparison, §IV B, finds *"the
vibrational correction leads to a substantial improvement of the caloric EOS"*). What was
rejected: reconstructing the 2017 uncorrected set by subtracting a u_vc read off Fig. 8 —
that would be reading numbers off a figure. The consequence is bounded by where the
correction enters:

- **Density mixing does not see it.** Additive volume reads p(ρ, T) only. The paper neglected
  the pressure correction p_vc for this data set because u_vc was *"only weakly dependent on
  the density"* — and adds *"However, this should not be understood as a general result since
  there are known examples where ionic quantum effects play a role also for the thermal EOS,
  e.g., in cold solids."* Quoted, not dropped.
- **c_P and ∇_ad do see it**, through ∂u/∂T. That is the one place where mixing this table
  with a partner of the other convention would be inconsistent. The partner here is Mazevet+
  2019's water fit, whose own convention on nuclear quantum effects this repository has not
  established; so the thermal columns of the check below are reported with that caveat and
  no sign is asserted from them.

Testable: `ammonia_table.U_INCLUDES_VIBRATIONAL_CORRECTION = True` is a constant the module
carries and `test_ammonia.py` asserts; the module docstring and `eos.py`'s block above
`Ammonia` say the same in words.

## What was built

- `engine/tools/make_ammonia_table.py` — parses the cached PDF's text layer, validates the
  counts, measures the interpolation error, writes the module. Dev-only (`pdftotext`); not a
  runtime dependency. The generated module has no imports beyond `math`.
- `engine/ammonia_table.py` — generated. Per-isotherm tuples of (ρ, p, u, flag) in the
  paper's units; SI accessors `pressure(ρ, T)`, `internal_energy(ρ, T)`, `density(P, T)` (by
  bisection), `uncertainty`, `rho_bounds(T)`, `p_bounds(T)`, `in_domain`. The grid is
  ragged and **nothing is interpolated across the absent cells**: the domain at T is the
  intersection of the two bracketing isotherms' density ranges (on an isotherm exactly, that
  isotherm alone). Above 10 000 K, below 500 K, or past the ragged pressure edge, a
  `ValueError` names the table; `eos.Ammonia` turns it into a `PhaseGap` that also names it.
- `eos.Ammonia` (`nh3`, registered in `MATERIALS`) in the `HotWater` shape: density from the
  table, c_P / ∇_ad / γ from finite differences of the table's p and u (1 % steps, folded
  inward at the edges), `p_max` = 333.2 GPa (the table's edge), `uncertainty(P, T)`.
- `engine/test_ammonia.py`, added to `scripts/check.sh` after `test_water_hot.py`.

**Interpolation.** Along an isotherm log p is linear in log ρ and u linear in log ρ; between
isotherms both linear in T. Measured leave-one-out (drop a grid point, predict it from its
neighbours — the number at *doubled* spacing; for linear interpolation the true inter-grid
error is about a quarter of it):

| region | p, worst | where | u, worst |
|---|---|---|---|
| whole grid | 17.3 % | ρ 0.5, 3000 K, along T | 2.45 kJ/g |
| ice-giant mantle region (ρ ≥ 1.0 g/cm³, T ≥ 2000 K — the solved mantles run 2550–6070 K) | 8.7 % | ρ 1.0, 3000 K, along T | 2.45 kJ/g |

The whole-grid worst sits in the low-density dissociation corner — *adjacent to* the 5 %
flags, not in their corner (corrected 2026-09-03, C22: the five flags are at 4000 K (0.5 · 0.75 · 1.0 g/cm³)
and 5000 K (0.5 · 0.75), none at 3000 K; and the asterisk marks a **convergence error** — Appendix,
*"uncertainty of up to 5%"* — not dissociation) — and 3000 K is where the paper reports its first-order transition (§IV A,
between 1.8 and 2.0 g/cm³ on the 3000 K isotherm; the table does not mark it and the
interpolation crosses it). Log-log in T was tried (15.2 % whole-grid) and not adopted: the gain
is marginal and one rule for p and u is simpler. The generator writes both numbers into the
module; the test re-measures the temperature-direction one.

## The check — water and ammonia, both from tables, mixed by additive volume

Eight (P, T) points: four read off the engine's own solved Uranus profile (50–250 GPa,
2830–3950 K, from `tools/methane_thresholds.py`) and four bracketing the central
temperatures (5500–6300 K sits between the 5000 and 7000 K isotherms — **interpolation, not
extrapolation**, which is why this was worth building), all under the table's ceiling at
their temperature. The solved mantles reach 820–1016 GPa at their base; the table ends at
270–333 GPa, so the deep mantle is outside it. Water is Mazevet+ 2019 (`h2o_hot`),
ammonia is this table; the pair is mixed at the solar-ratio mass fractions renormalised to
two components, w_NH₃ = 0.08/(0.08 + 0.61) = 0.1159 (Bethkenhagen+ 2017 §V).

| P (GPa) | T (K) | ρ_H₂O | ρ_NH₃ | NH₃/H₂O | μ-ratio | mix/H₂O | flag |
|---|---|---|---|---|---|---|---|
| 50 | 2830 | 2241 | 1713 | 0.764 | 0.945 | 0.9654 | 2 % |
| 100 | 3190 | 2782 | 2171 | 0.781 | 0.945 | 0.9684 | 2 % |
| 200 | 3730 | 3474 | 2713 | 0.781 | 0.945 | 0.9685 | 2 % |
| 250 | 3950 | 3738 | 2924 | 0.782 | 0.945 | 0.9687 | 2 % |
| 50 | 5000 | 2076 | 1609 | 0.775 | 0.945 | 0.9674 | 2 % |
| 100 | 5500 | 2611 | 2045 | 0.783 | 0.945 | 0.9689 | 2 % |
| 200 | 6000 | 3308 | 2612 | 0.790 | 0.945 | 0.9700 | 2 % |
| 250 | 6300 | 3566 | 2826 | 0.792 | 0.945 | 0.9705 | 2 % |

**Result, composition tier, ammonia share only.** At the same (P, T) ammonia is **21–24 %
less dense** than water (ρ_NH₃/ρ_H₂O = 0.764–0.792) — far more than the 5.5 % the equal-number-density argument
(μ_NH₃/μ_H₂O = 0.945) predicted; that argument was a floor, and it is now superseded for
this share by a measured ratio. Water standing in for the water–ammonia pair **overestimates
its density by 2.9–3.5 %**, direction **+** (it widens the residual), as the tier said. The
number is above its noise: the ammonia density's 2 % + ~2.2 % (interpolation, the mantle-region
leave-one-out over four) propagates into the mixture as w·(ρ_mix/ρ_NH₃) ≈ 0.6 %. The water side's error (an analytic fit, not a
table) is not quantified here; the comparison takes it as the reference.

**Thermal tier, ammonia share — reported, no sign asserted.** At the same points ammonia's
c_P is 1.3–2.1× water's. Its ∇_ad is 19–45 % *below* water's at seven of the eight points
(0.108–0.228 against 0.176–0.289), so the pair's c_P-weighted ∇_ad is 3–10 % shallower
there — the direction the tier's mechanism named (more atoms per unit mass → higher heat
capacity → shallower adiabat → colder interior). **At the mantle top it is the other way**:
at 50 GPa, 2830 K ammonia's ∇_ad is 0.172 against water's 0.152 and the pair's adiabat is
2.6 % steeper. The columns rest on ∂u/∂T of a coarse table (the 2000–3000–4000 K isotherms,
where the paper's first-order transition sits) under the convention caveat above, so the
row keeps "mechanism named, sign ungrounded"; this is the first table-derived indication,
and it is not uniform along the profile.

**Net tier.** Still needs the tables — **methane is still missing**, and it is the largest
share (0.31). Nothing here softens the three-tier statement; it fills in numbers for one
third of one tier.

## Grounds for the next decision (not taken)

Whether ammonia enters the ice-giant mantle as a declared fraction is a separate decision.
Grounds for: the material exists at grade *table* with its uncertainty carried; the mixing
rule is already in `Mixture`; `SOLAR_ICE_MASS_FRACTIONS` gives a published default ratio; the
mantle's (P, T) is inside the table (interpolation). Grounds against, or for waiting: a
water–ammonia mantle is *not* the ternary the field models — methane's share is larger than
ammonia's, and a two-component mantle would fix the composition term for the ammonia share
while leaving the larger one out; the convention caveat touches the adiabat; and the table's
ceiling (≈ 290–333 GPa at mantle temperatures) is **below the ice giants' central pressures**,
so a declared fraction would need a stated fallback in the deep mantle. Wiring it changes
`interior._stack` (a path function) and would need `test_ice_giant.py --refresh` in the same
commit. Decision left to the owner.

## The methane half — re-stated from Sherman+ 2012, not baked

Sherman, Wilson, Weeraratne & Militzer 2012, *Ab initio simulations of hot, dense methane
during shock experiments*, Phys. Rev. B 86, 224113
([`2012PhRvB..86v4113S`](https://ui.adsabs.harvard.edu/abs/2012PhRvB..86v4113S), doi
[10.1103/PhysRevB.86.224113](https://doi.org/10.1103/PhysRevB.86.224113), arXiv
[1207.2948](https://arxiv.org/abs/1207.2948)); both files in the cache
(`docs/phase3/_papers/2012PhRvB..86v4113S.pdf`, `.tex`); title checked against the bibcode.
The EOS table is in the LaTeX source's appendix ("to be published as online supplementary
information", 1σ in brackets); the published PDF says *"different initial densities are
given in the online supplemental information"* and does not print it. Counted from the
source: 79 rows, 13 densities, 13 temperatures (300, 1000, 2000, 3000, 4000, 5000, 6000,
7000, 10 000, 20 000, 30 000, 40 000, 75 000 K) — the coverage table is in the C4 row.

**Why it is not baked** (the owner's decision, with the grounds read here):

1. The paper's own result is that methane stops being methane in the region: *"Up to 3000 K
   … the methane molecules remained intact. At a temperature of approximately 4000–5000 K,
   a plateau is reached … the system entering into a polymeric regime where the methane
   molecules spontaneously dissociate to form long hydrocarbon chains that dissociate and
   reform rapidly. We will demonstrate this regime to be metallic"*; abstract: *"At 6000 K,
   the sample transforms into a plasma composed of many, short-lived chemical species."* And
   they flag that even the molecular states *"may not necessarily be the thermodynamic
   ground state"*, citing Spanu+ that the polymeric state is favoured above 4 GPa.
   Bethkenhagen+ 2017 §III: *"Pure methane does not become superionic but instead
   decomposes into long-chained molecules in our simulations."* Additive volume evaluates
   each component at (P, T) as itself; for a component that has become hydrocarbon chains
   and hydrogen, the published binary/ternary deviations (Bethkenhagen+ 2017's 4 % / 2.1 %)
   are measured on *their* simulations and no error for treating such a component as a
   linear-mixing member exists in the literature read here.
2. Coverage: the low-density lines (0.8, 1.0 g/cm³) stop at 4000 K, below the adiabat; only
   1.201 and 1.498 g/cm³ run the whole temperature range; four densities are single points.
   Bethkenhagen+ 2017 §II.3 says it of the existing methane sets by name: *"none of them
   covers the entire pressure-temperature region required for Uranus and Neptune interior
   models."* A material built on it would be inventing coverage.

So the row's methane reason is upgraded from *paywalled* to *a distributed table that does
not license the mixing rule, on a grid that does not cover the region.*

## Measured: the engine's mantles against the dissociation thresholds

`engine/tools/methane_thresholds.py` (a measurement, not a gate) reads the frozen
convergence points from `ice_giant_anchor.json`, runs the one standalone integration
`test_ice_giant.py` uses, and samples the ice layer. Thresholds as Sherman's introduction
collects them: C–C bond formation above 1100 K and 10 GPa and diamond above 3000 K (Hirai+,
laser-heated DAC), the polymeric regime at 4000–5000 K (Sherman's DFT-MD).

```
Uranus:  ice mantle 34.5–819.8 GPa, 2663–5948 K (78 samples); centre 1220 GPa, 6160 K
  C–C (> 1100 K & > 10 GPa): crossed at 34.5 GPa, 2663 K — 78/78 samples, the whole mantle
  diamond (> 3000 K):        crossed at 80.2 GPa, 3037 K — 71/78
  polymeric (> 4000 K):      crossed at 261.5 GPa, 4010 K — 51/78;  > 5000 K at 525.3 GPa — 27/78
    ~50 GPa 2829 K · ~100 GPa 3188 K · ~200 GPa 3726 K · ~300 GPa 4194 K
Neptune: ice mantle 39.2–1015.6 GPa, 2553–6066 K (76 samples); centre 1533 GPa, 6296 K
  C–C: crossed at 39.2 GPa, 2553 K — 76/76
  diamond: crossed at 113.8 GPa, 3049 K — 67/76
  polymeric: 333.8 GPa, 4039 K — 48/76;  > 5000 K at 625.8 GPa — 27/76
    ~50 GPa 2669 K · ~100 GPa 2996 K · ~200 GPa 3471 K · ~300 GPa 3886 K
```

The mantles pass all three thresholds: the whole mantle above the C–C line, nine tenths of
the pressure span above the diamond line, the deeper half in or beyond the polymeric
regime. Recorded as numbers; not judged. Two things the measurement does not say: these are
*this recipe's* profiles (a water mantle under an H/He envelope, the C5 attribution
standing), and a threshold crossed in (P, T) is not a statement about how much carbon
separates or where it goes — that would be the item the owner may or may not open.

## What did not move

No anchor: `nh3` is a new material with no consumer; the fingerprint hashes `interior.py`
path functions, none of which changed. `test_ice_giant.py --fast` and the full anchor set are
in the gate log. Gate time: `test_ammonia.py` adds under a second.
