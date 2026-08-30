# The melting curve above 20.6 GPa — context notes

Decisions taken while closing C3 of `interior-core.md`, and the reasoning behind them.
Appended as the work goes.

## What the ice giants actually reach, measured before deciding anything

The brief's "Neptune's envelope base landed at 1797 K, three kelvin under the floor" is a
**trial path**, not the converged point. Integrating once at the frozen convergence point
(`test_ice_giant.py`'s `_standalone`, with `water_hot.density` instrumented):

| body | ice layer top | ice layer base | Reinhardt liquid line at the top |
|---|---|---|---|
| Uranus | 30.6 GPa · 2624 K | 820 GPa · 5947 K | 1258 K → fluid by +1366 K |
| Neptune | 36.6 GPa · 2538 K | 1016 GPa · 6078 K | 1467 K → fluid by +1071 K |

So at convergence both are fluid at the base of the envelope by a kilokelvin, and the
class-based dispatch was giving the right material for the wrong reason. Deeper, the
adiabat climbs ~8 K/GPa while the liquid line climbs ~34 K/GPa; the line ends at
52.4 GPa · 1953 K where Neptune is at 2667 K, so the two never meet inside the data. At
190 GPa Neptune is at 3440 K and Uranus at 3670 K, both under Millot+ 2018's "melts near
5,000 K at 190 GPa" — the deep mantle is superionic, and Mazevet's single fit is what
covers it.

## What the published data are, and are not

`figs-1-and-S1/coex-line-liquid.dat` is the blue line of Fig. 1a: eleven liquid–solid
coexistence points from thermodynamic integration, **10 to 52.4 GPa**, three of them
(20, 26, 47 GPa) starred as benchmarked by direct coexistence, and the direct-coexistence
set (`coex-direct-coexistence.dat`) agrees with the line to within 4 K at 20, 26 and 47 GPa
and 7 K at 15 GPa. The brief's "2–200 GPa" is the paper's *range of bcc ices*, not the
range of the liquid line: the liquid line the data carry is 10–52.4 GPa.

`coex-line-superionic-ice.dat` is the brown line: the **VII′–VII″ coexistence** from TI
along isobars, 20 to 70 GPa, first order by the chemical-potential slope (Fig. 1e). The
paper's triple point liquid–VII′–VII″ is at ~20 GPa · 875 K, and the two files agree
there (875 K on the liquid line, 856 K on the solid–solid line at 20 GPa — the 19 K is the
paper's own scatter at the triple point). `discontinuity-kink.dat` is the cyan dashed
line, the brute-force density/enthalpy discontinuity locus, 20–80 GPa; above ~40 GPa the
paper says it coincides with the proton-diffusivity proxy for the superionic transition.
It is the same transition seen a cruder way, and it is **not** baked — the coexistence
line is the thermodynamic one.

The grade is **analog**: a machine-learned potential fitted to PBE DFT, checked against
experiment only through the location of the triple point (Queyroux+ 2020: 14.6 GPa · 850 K
against the simulation's ~20 GPa · 875 K). Every experiment that would check the line
itself is paywalled (Schwager 2004, Frank 2004, Lin 2005, Kimura 2014/2023, Queyroux 2020,
Weck 2022, Bezacier 2014, Journaux 2020, Millot 2018/2019). Not worked around.

## The seam at 20.6 GPa — measured, and it is large

IAPWS equation (5) gives **715 K** at 20.6 GPa (its own end). Reinhardt's line interpolated
to 20.6 GPa gives **~902 K**. That is a **+26 % step in melting temperature** at the seam,
and in pressure the same statement is that Reinhardt reaches 715 K at ~16.5 GPa, 20 %
below IAPWS.

The two curves cross near 15–16 GPa (IAPWS 663 K at 15 GPa against Reinhardt's 643 K), so
splicing at the crossing was tried on paper and **rejected**: it would trade IAPWS's last
five gigapascals of measured curve for a simulation where both exist, and the splice
pressure would be ours rather than either source's. The silicate precedent — splice where
the source stops, measure the seam, state it — is what this follows. Frank+ 2004 was
rejected in the ice X work for a 17 % pressure step at the same seam; this one is worse in
temperature and is accepted because it buys 32 GPa of curve and the phase boundaries
above it, not one third of a rung. A column sitting in the disputed band (715–902 K near
20.6 GPa) is named as such by the verdict rather than silently assigned.

Below the seam the slope disagreement is the real content: IAPWS ends at ~10 K/GPa,
Reinhardt runs at ~46 K/GPa through the same pressures. The paper itself lists the
experimental triple points at 14.6, 35 and 43 GPa from three groups, so the disagreement
is the literature's, not ours.

## The fluid's floor is Mazevet's, not the ladder's ceiling

`water_hot.T_MIN` was 1800 K "at the same place as `ICE_VII_X_T_MAX`" — exactly the
conflation C3 exists to remove. Mazevet+ 2019 §3.1 states its own domain: liquid at
ρ ≲ 1 g/cc and T ≲ 2000 K, plasma at 1 ≲ ρ ≲ 10² g/cc and **10³ K ≲ T** ≲ 10⁵ K,
superionic covered "satisfactorily" by the single-phase fit, and limited applicability
for ice VII and X at T ≲ 2000 K over 2–300 GPa. The last clause is about the *solid*: the
fit "extends the liquid throughout the solid phases" (their §4). So when the melting
curve says liquid, the fit is being used as what it is — a liquid fit — and its floor at
planetary densities is the paper's **1000 K**. The floor moves from 1800 to 1000 K, and
the test that asserted `T_MIN == ICE_VII_X_T_MAX` is replaced by one that asserts they
are different objects with different provenance.

Between the melting line and 1000 K above 2.3 GPa (the liquid-water table's ceiling)
there is a band with no liquid EOS in this repository. The shelf is named: SeaFreeze's
`water2` (Brown 2018, 0–100 GPa · 240–10 000 K). Not brought in — it is the C2 note's
shelf, and this item is the curve.

## Dispatch, and what "carries" above 52.4 GPa

The ice layer's stack material is always the ladder (`h2o`). Per step, the local (P, T)
against the curve picks: liquid → `h2o_liquid` up to the liquid table's 2.3 GPa, `h2o_hot`
above it if at or above Mazevet's floor; solid → the ladder. `ice_material` and the
`ICE_GIANT_CLASSES` decision are gone from `solve`/`_stack`/`integrate`/`shoot`.

Above 52.4 GPa no liquid line is carried. The recipe does **not** invent one: there the
solid is integrated on the ladder to its fit ceiling (1800 K, a fit's number) and above
that only Mazevet's fit exists (fluid and superionic as one), so the EOS is chosen by
availability and the verdict says "fluid or superionic — the liquid line ends at
52.4 GPa" rather than naming a phase it cannot locate. Millot+ 2018's single point
(190 GPa · ~5000 K) is quoted in the note as the one measurement that would place a body's
deep mantle on one side, and both ice giants sit ~1500 K under it.

Ice VII″ (between the VII′–VII″ line and the liquid line) has no equation of state of
its own here. It is integrated on the same French & Redmer potential as VII′/X — Reinhardt
describes the density discontinuity across that first-order line as small — and the phase
is **named** VII″ in the verdict with the grade already analog. That is the honest
version of "closing the ice_x hole": the curve now reaches 52.4 GPa, so `ice_x` carries a
melting curve over 37.4–52.4 GPa and the verdict states the pressure above which it does
not.

## Superionic onset against Millot+ 2019 (condition b)

Attempted from what is accessible: the abstract (ADS, 2019Natur.569..251M) places
superionic water at "pressures exceeding 100 gigapascals and high temperatures above
2,000 kelvin". Reinhardt's VII′–VII″ line reaches 1921 K at 70 GPa with a slope of
~17 K/GPa over 50–70 GPa; a straight continuation puts it at ~2400 K at 100 GPa, above
the abstract's 2000 K floor. That is consistent in direction (superionic above ~2000 K
past 100 GPa) but it is a comparison of a simulated line's extrapolation against an
abstract's round numbers. **It cannot be checked properly**: what would check it is the
paper's Fig. 3 phase diagram (the measured melting line of superionic ice XVIII between
~160 and 400 GPa and the ice VII–XVIII boundary), and the paper is paywalled. Recorded as
unverified; the constants `SUPERIONIC_MIN_T`/`SUPERIONIC_MIN_P` that already sit in
`eos.py` remain abstract-sourced and say so.

## What the first implementation hit, in order

**The ladder above 1 TPa on a cold trial.** With the ladder as the stack material, an ice
giant's first trials (central temperature 2 × 72 K) put the whole ice column solid and the
ladder's 1 TPa pressure ceiling threw a *pressure* refusal, which the shooting cannot fix by
raising the temperature. The old class dispatch had hidden this behind `h2o_hot`'s too-cold
refusal. Resolved by the availability rule: above the ladder's fit (1 TPa or 1800 K) the
only representation is Mazevet's, and if the state is under its 1000 K floor too the refusal
is thrown as too cold — honestly, since the state is reachable hotter.

**The VII′/X sliver above 1800 K.** Between ~65 and 70 GPa the VII′–VII″ line sits above
1800 K, so a solid decided by the line could not be integrated on the ladder. The same
availability rule covers it: a phase the lines call solid but the ladder cannot represent is
integrated on Mazevet and the verdict says so ("사다리의 적합 밖이라 밀도는 Mazevet 이 냈다").

**Ice VII″ is superionic, so it belongs to Mazevet, not the ladder.** The first cut sent
everything the liquid line called solid to the ladder, and Neptune's trials then hit the
1800 K ceiling in the 47–52.4 GPa band (VII″ under the melting line, above 1800 K). Queyroux+
2020 identify VII″ with the predicted superionic phase and Mazevet's fit covers the superionic
regime; French & Redmer's potential is the insulating VII/X. So the VII′–VII″ line, not the
liquid line, is the ladder/Mazevet boundary, and the liquid line only names liquid vs VII″
inside Mazevet's field. This is the physically right dispatch and it is what shipped.

**The 500–1000 K liquid band.** A trial with the envelope base at 0.7 GPa · 986 K is liquid
by IAPWS but above the ocean table's 500 K and below Mazevet's 1000 K. Thrown as too cold
(the fluid opens above), which is the direction the old `h2o_hot` floor threw it. For a warm
water world this flips the old direction (the ocean table's ceiling used to lower the
temperature); no anchor visits the band, and a body whose answer sits inside it declines by
name either way.

## The second finding: Neptune's convergence was luck

With the dispatch in place Neptune solved but `converged=False`, and the trace showed why.
The 1-bar temperature is a **jagged** function of the central temperature: scanning
6300–6340 K gave 71.64, 71.46, 71.97, 71.88, 71.71, 72.19, 72.10, 71.97, 72.42 K on the
*old* code too (old and new agree to the last digit at every point — the dispatch did not
cause it). The 1-bar level of an ice giant lies under the H/He table's 100 K floor, so the
integration exits the table a few bar above 1 bar and closes the gap with T ∝ P^∇_ad; the
exponent was `last_grad`, the gradient at the **start of the step** that crossed the floor,
and step starts sit on the radius grid, so which step crosses changes discretely with the
central temperature. The old trial path happened to land in a trough (71.9965 K at
6308.5 K, inside the 1e-3 tolerance); the new path did not.

Two changes, both in the temperature loop's territory:

- the exponent is now `_grad_ad_at(mat, p, t)` **at the exit point**, which the bisection
  locates independently of the grid. The scan becomes 72.09, 72.07, 72.14, 72.27, 72.28,
  72.30, 72.42, 72.48, 72.48 K — a residual ripple of ~0.02 K remains (the temperature is
  carried with one ∇_ad per step, a first-order scheme, so the accumulated error still
  depends on grid phase), but the ±0.4 K teeth are gone;
- the loop **keeps its best pass**. Even with the ripple, the proportional update rides the
  ripple's local slope (n ≈ 2.5) and diverges after touching 3.5 × 10⁻⁵, and the old code
  returned the last pass. Anchors that contract every pass end on their best pass and are
  untouched by construction; a body whose last pass drifted out returns the pass that met
  the tolerance.

Jupiter and Saturn never exit through the floor (165 K and 135 K at 1 bar), so the giant
anchors are bit-identical; `test_giant.py` passed unchanged. The ice giants moved:

| body | radius | central temperature | converged |
|---|---|---|---|
| Uranus | 4.198693 → 4.198853 R⊕ (+3.8 × 10⁻⁵) | 6 158.6 → 6 160.1 K | True → True |
| Neptune | 4.211250 → 4.210086 R⊕ (−2.8 × 10⁻⁴) | 6 308.5 → 6 295.5 K | True (luck) → True |

The mechanism in one sentence: the exit-point gradient closes the last extrapolation about
0.4 K hotter, so the loop settles the centre 13 K cooler on Neptune and 1.5 K warmer on
Uranus (whose 76 K exit is nearer the floor). Re-frozen with `--refresh` in the landing
commit; the grid-phase asserts hold (Uranus 7.2 × 10⁻⁷, Neptune 8.6 × 10⁻⁶ across 1499 ↔ 1501
steps).

## Gate cost

`test_ice_giant.py` full solves: Uranus 49 → 51 s, Neptune 44 → 55 s at the refresh. The
state dispatch adds one line lookup per step in the ice layer; the rest is the different
trial path. About +13 s on a 22-minute gate.

## What is left, named

- The liquid line above 52.4 GPa and the superionic melting line (Millot+ 2018/2019) are
  not carried; the verdict says "fluid or superionic" there. What would carry them is the
  paywalled Millot+ 2019 Fig. 3, or French & Redmer 2016's superionic potentials.
- The 500–1000 K dense-liquid band has no equation of state; the shelf is SeaFreeze `water2`. *(Filled 2026-08-30: `water2` baked to its real ceiling, `engine/water2-context-notes.md`.)*
- The residual 0.02 K ripple in the 1-bar temperature is the first-order temperature carry,
  not this item's.
