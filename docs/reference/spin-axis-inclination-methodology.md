<!-- 미측정 항성/갈색왜성 자전축 시선경사 i★를 v sin i + 자전주기 + 반지름 결합으로 도출하는 방법(논문 근거) -->
# Spin-axis inclination grounding: i★ from v sin i + rotation period + radius

Method reference for deriving the **line-of-sight spin inclination i★** of a
star or brown dwarf that has **no direct i★ measurement**, by combining three
observables: the projected rotation velocity (v sin i, spectroscopic), the
rotation period (P, photometric), and the radius (R). Bodies with a *measured*
i★ (interferometric like tau Cet / Fomalhaut, or Doppler-imaging) passthrough
that measurement instead — this recipe is only for the combination route.

First consumer: the Luhman 16 A/B Phase 4 board (spin-axis rows).

## The relation

Treating the body as a rigid rotating sphere, the true equatorial velocity is

    v_eq = 2π R / P

and the spectroscopic broadening measures its projection, so

    sin i★ = v sin i / v_eq = (v sin i · P) / (2π R)

This is textbook geometry (the allowed exception class), but its *use as an
inclination estimator* is standard practice in the brown-dwarf variability
literature — Vos, Allers & Biller 2017 ([`2017ApJ...842...78V`](https://ui.adsabs.harvard.edu/abs/2017ApJ...842...78V),
arXiv [1705.06045](https://arxiv.org/abs/1705.06045), cached) state the
procedure and its assumptions explicitly (rigid rotation; Jupiter's
core-vs-cloud period difference of ~5 min justifies the rigid-sphere
approximation at photometric-period precision) and apply it to 19 variable
brown dwarfs.

## Practical formula

With R in Jupiter radii (R_Jup = 71 492 km) and P in hours:

    v_eq [km/s] = 124.78 · (R / R_Jup) / P_hr
    sin i★      = v sin i / v_eq

Conventions: i★ = 90° is equator-on, i★ = 0° pole-on. Spectral broadening
cannot distinguish i from 180° − i (north pole vs south pole toward us), so
results are quoted in 0–90° (Masuda & Winn 2020, §II).

## Statistical discipline (Masuda & Winn 2020)

Masuda & Winn 2020 ([`2020AJ....159...81M`](https://ui.adsabs.harvard.edu/abs/2020AJ....159...81M),
arXiv [2001.04973](https://arxiv.org/abs/2001.04973), cached) show that the
naive Monte Carlo — sampling v sin i and v_eq independently from their error
bars and histogramming sin i — is **wrong**, because v sin i and v_eq are not
statistically independent (v sin i ≤ v_eq always). The naive procedure
"severely overestimates the probability density for cos i ≈ 1" (pole-on) and
underestimates equator-on. The correct object is the posterior of **cos i**
(flat for an isotropic axis), computed from the joint likelihood.

NearStars consequences (we do not run their full Bayesian machinery):

1. **Report i★ as a bound or bracket, not a Gaussian.** Propagate the input
   ranges through the formula edge-to-edge (min/max of R and P) and state the
   result as "i★ > X°" or "X°–90°" — the shape our consumers (board rows,
   viewer layers) can actually use.
2. **Nominal sin i★ > 1 is not an error** when v sin i ≈ v_eq within
   uncertainties — it means equator-on (i★ ≈ 90°) with the excess absorbed by
   the input error bars. Never "clip" it into a fake precise 90° ± small.
3. **Low-inclination claims need extra care** (the naive method's bias is
   worst there); an equator-on conclusion is robust, a pole-on one is not.

## Domain of validity / regimes

1. **Direct i★ measurement exists** (interferometric rotation solution,
   Doppler-imaging fit): passthrough the measurement; do not derive.
   (NearStars: tau Cet 7°±7° Korolik 2023; Fomalhaut 90°±9° Hadjara 2014.)
2. **All three inputs measured** (v sin i + P + R): apply the formula with
   the statistical discipline above. Confidence = the weakest input's
   confidence; a disputed period makes i★ conditional on the period choice,
   and the row must say which period it assumed.
3. **Radius not measured** — the universal brown-dwarf case (no L/T dwarf has
   a directly measured radius): use the electron-degeneracy field-BD radius
   0.8–1.2 R_Jup (Burrows et al. 2001,
   [`2001RvMP...73..719B`](https://ui.adsabs.harvard.edu/abs/2001RvMP...73..719B);
   radius nearly mass-independent at field ages), or the object's own
   evolutionary-model radius where curated (Filippazzo et al. 2015,
   [`2015ApJ...810..158F`](https://ui.adsabs.harvard.edu/abs/2015ApJ...810..158F)).
   Propagate the full radius range into the i★ bracket.
4. **Slow rotators, v_eq ≲ 2–2.5 km/s**: the recipe fails *in principle*, not
   just in precision — spectroscopic v sin i is unreliable below ~2–2.5 km/s
   (turbulent/instrumental broadening dominates; Dumusque 2014,
   [`2014ApJ...796..133D`](https://ui.adsabs.harvard.edu/abs/2014ApJ...796..133D)),
   and slow rotators sit entirely under that floor. Use an alternative route:
   activity/RV modeling (SOAP — Dumusque 2014's α Cen B i★ = 45°(+9/−19)) or
   Zeeman-Doppler imaging (Klein 2021's Proxima i★ = 47°±7°). NearStars
   examples: α Cen B (v_eq 1.07 km/s) and Proxima (0.085 km/s) — both keep
   their measured alternative-route values; the combination method cannot
   check them.
5. **No period, or no v sin i**: the recipe does not apply. An isotropic
   prior (flat in cos i★) is the honest state; any adopted orientation is an
   owner art choice (owner-override), not a derivation.

Caveats that stay caveats: differential rotation (bounded by the Jupiter
5-minute argument above); photometric periods from evolving weather can drift
between epochs (Apai 2021's Luhman 16 B period splitting) — use the canonical
period and note the spread; the derived i★ says nothing about the spin-axis
*position angle* on the sky (a separate, usually free, emit orientation).

## Worked example — Luhman 16 A & B (the first consumers)

Inputs: v sin i 17.6 ± 0.1 km/s (A), 26.1 ± 0.2 km/s (B) (Crossfield et al.
2014, cached); P_A = 6.94 hr (Apai et al. 2021, tentative), P_B = 4.87 hr
(Gillon et al. 2013) with the Apai 2021 TESS analysis spanning 4.9–5.3 hr;
R = 0.90–1.10 R_Jup (Burrows 2001 degenerate radius, the bracket Apai 2021
adopt).

| body | P (hr) | v_eq over R 0.90–1.10 R_Jup | sin i★ = v sin i / v_eq | i★ |
|---|---|---|---|---|
| A | 6.94 | 16.2–19.8 km/s | 0.89–1.09 | **> 62°** (equator-ward) |
| B | 5.28 (TESS) | 21.3–26.0 km/s | 1.00–1.23 | **≈ 90°** (equator-on) |

Validation: these reproduce Apai et al. 2021 §6.2's own published numbers —
their v_eq brackets (A 16.3–19.9, B 21.2–25.9 km/s; ours differ only in the
last-digit rounding of R_Jup) and their conclusions "Luhman 16 A is viewed
within 28° of its equatorial plane (i > 62°)" and "B is viewed almost exactly
equatorially (i ≃ 90°)". B's nominal sin i★ reaching 1.23 at the small-radius
edge is the rule-2 case: equator-on, excess absorbed by the radius bracket.

System bonus: the AB orbital inclination is 79.21° ± 0.45° (Bedin et al. 2017,
[`2017MNRAS.470.1140B`](https://ui.adsabs.harvard.edu/abs/2017MNRAS.470.1140B),
arXiv [1706.00657](https://arxiv.org/abs/1706.00657); the curated Lazorenko &
Sahlmann 2018 orbit's 100.26° is the same plane under the opposite
node/direction convention, 180° − 100.26° = 79.74°). Apai 2021 note the two
spin axes and the orbit normal "may be well aligned" — three planes within
~28° of each other, with no evidence for misalignment.

## Worked example — α Centauri A (regime-2 star)

Inputs: v sin i 2.7 ± 0.7 km/s (Saar & Osten 1997), P 22 ± 3 d (DeWarf 2010,
DB recommended), R 1.2234 R☉ (Kervella 2017). v_eq = 2.81 km/s (2.48–3.26
over the period range) → sin i★ = 0.96 nominal → **i★ ≈ 74°, bracket
38°–90°** (edge-to-edge). Consistent with spin-orbit alignment (AB orbital
inclination 79°); Bazot et al. 2007 ran the same relation in reverse —
assuming i = 79° alignment, v sin i predicts P = 22.5 ± 5.9 d, matching the
photometric 22 d. The two directions closing on the same numbers is the
cross-check. Contrast the companions: α Cen B (v_eq 1.07 km/s) and Proxima
(0.085 km/s) are regime-4 slow rotators where this recipe cannot run.

## Citations

- **Vos, Allers & Biller 2017**, ApJ 842, 78 ([`2017ApJ...842...78V`](https://ui.adsabs.harvard.edu/abs/2017ApJ...842...78V),
  arXiv [1705.06045](https://arxiv.org/abs/1705.06045), **cached**). The
  standard BD application of the combination method: procedure, rigid-sphere
  justification, field-BD radius prescription (0.8–1.2 R_Jup), 19-object
  sample.
- **Masuda & Winn 2020**, AJ 159, 81 ([`2020AJ....159...81M`](https://ui.adsabs.harvard.edu/abs/2020AJ....159...81M),
  arXiv [2001.04973](https://arxiv.org/abs/2001.04973), **cached**). The
  statistical treatment: v sin i and v_eq are correlated; naive sampling
  biases toward pole-on; work in cos i. Source of the reporting discipline.
- **Apai et al. 2021**, ApJ 906, 64 ([`2021ApJ...906...64A`](https://ui.adsabs.harvard.edu/abs/2021ApJ...906...64A),
  arXiv [2101.02253](https://arxiv.org/abs/2101.02253), **cached**). Applies
  the method to Luhman 16 A/B (§6.2) — the validation anchor and the values
  the Phase 4 board consumes.
- **Crossfield et al. 2014**, Nature 505, 654 ([`2014Natur.505..654C`](https://ui.adsabs.harvard.edu/abs/2014Natur.505..654C),
  arXiv [1401.8145](https://arxiv.org/abs/1401.8145), **cached**). The
  v sin i measurements for both Luhman 16 components.
- **Burrows et al. 2001**, RvMP 73, 719 ([`2001RvMP...73..719B`](https://ui.adsabs.harvard.edu/abs/2001RvMP...73..719B),
  arXiv [astro-ph/0103383](https://arxiv.org/abs/astro-ph/0103383)). The
  electron-degeneracy radius plateau behind the 0.8–1.2 R_Jup field-BD
  prescription.
- **Filippazzo et al. 2015**, ApJ 810, 158 ([`2015ApJ...810..158F`](https://ui.adsabs.harvard.edu/abs/2015ApJ...810..158F),
  arXiv [1508.01767](https://arxiv.org/abs/1508.01767)). Per-object
  evolutionary-model radii, preferred over the generic bracket when curated.
- **Dumusque 2014**, ApJ 796, 133 ([`2014ApJ...796..133D`](https://ui.adsabs.harvard.edu/abs/2014ApJ...796..133D),
  arXiv [1409.3593](https://arxiv.org/abs/1409.3593)). The slow-rotator floor
  (v sin i unreliable below ~2–2.5 km/s) and the SOAP alternative route
  (α Cen B i★ = 45°).
- **Saar & Osten 1997**, MNRAS 284, 803 ([`1997MNRAS.284..803S`](https://ui.adsabs.harvard.edu/abs/1997MNRAS.284..803S)).
  v sin i for α Cen A (2.7 ± 0.7 km/s; quoted verbatim in the cached Bazot
  2007, arXiv [0706.1682](https://arxiv.org/abs/0706.1682)). *1997 MNRAS, no
  arXiv preprint*: verified by bibcode + the cached secondary quote.
- **Bedin et al. 2017**, MNRAS 470, 1140 ([`2017MNRAS.470.1140B`](https://ui.adsabs.harvard.edu/abs/2017MNRAS.470.1140B),
  arXiv [1706.00657](https://arxiv.org/abs/1706.00657)). Luhman 16 AB orbital
  inclination used in the spin-orbit alignment note.

## Related

- [cassini-state-obliquity-methodology](cassini-state-obliquity-methodology.md) —
  the *equilibrium tilt* counterpart for tidally-damped bodies; this doc is the
  *observed line-of-sight* inclination for free rotators. Do not cross-apply.
- [body-figure-methodology](body-figure-methodology.md) — consumes measured
  i★ (Fomalhaut worked example) for full 3-D rotation solutions and J₂.
- [methodology-index](methodology-index.md) — the living index of all
  derived-value recipes.
