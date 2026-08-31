<!-- 2026-08-31 병렬 세션 서베이 세 건의 결과와 그것이 바꾼 판단 — 지휘석 기록 -->
# The three surveys of 2026-08-31 — what was asked, and what came back

Dispatched to the parallel session by the previous directing seat, in the order the owner
approved: AQUA (water's ceiling), the radiative–convective boundary (hot sub-Neptunes), and
a third melting-curve candidate. All three landed the same day; all three were reproduced by
the directing seat and audited independently.

**Each was asked the wrong question, and each answered a better one.** That is the finding
worth carrying forward: the briefs' premises came from our own notes, and in all three cases
the notes were describing something the source did not contain.

The reports themselves live in the parallel session's scratchpad (`H1-aqua-grid-and-ceiling.md`,
`H2-radiative-convective-boundary.md`, `H3-melting-curve-third-candidate.md`) and are not in
the repository. What survives here is what changed.

## ① AQUA — the ceiling was not where the brief put it

**Asked**: does AQUA raise water's pressure ceiling above the ladder's 1 TPa?

**Answer: there is no wall to raise.** 1 TPa is the *cold* ladder's ceiling. `eos.H2O_HOT.p_max`
is **407,517.73 GPa** — 407.5× further — and the 21.29 M⊕ water ceiling everyone quoted comes
from `CEILING_CASES`' water row running `composition="water"` with **no potential temperature**
(`test_interior.py:455`), so it was the cold path's number all along. On the warm path the
wall does not exist, and `h2o` moves from lowest of the four material ceilings to highest.

**The grid is clean** — 328,993 rows = 1093 pressures × 301 temperatures exactly, no missing
nodes, log spacing uniform to eight decimals. Six of AQUA's seven regions are sources we
already carry; the seventh is low-density vapour an interior column never enters.

**What adopting it would actually buy**: the high-pressure 300–1000 K corner (our `h2o_hot`
starts at 1000 K and the ladder ends at 1 TPa, so a cold dense column has no road), and the
stitched entropy/energy zero points. Cost: a 13.6 MB table dependency and AQUA's own Method 2
interpolation seam at 300–700 GPa. **Not urgent** — decide it when a body needing that corner
enters the roster.

**A second reason for that corner appeared later the same day** — see C6: our own ladder is
extrapolated above ~355 GPa, so the corner is not merely untabulated, it is where the table we
do have stops being data.

**The 12–20.6 GPa empty band is not AQUA's to fill.** Measured three ways at once: at 20.0 GPa
our melt is 704.9 K, `water2`'s floor is 870.0 K, and the band is **165 K**; against AQUA's own
executed melt boundary (read from the distributed phase-ID column, not a fit) the band is 48 K.
**Two thirds of the band is our melting curve being cold, not a missing equation of state** —
and AQUA does not fill that space, it disagrees that the space is liquid. That hands the band
to the melting-curve question, ③.

## ② The radiative–convective boundary — the prescription is one layer down

**Asked**: transcribe Nettelmann+ 2011's 80–800 bar radiative–convective boundary.

**Answer: it is not a prescription.** Their §II: *"The transition pressure of the atmosphere
from radiative to adiabatic, at the current time, P_ad(t₀), is a quantity we aim to constrain
with our evolution model."* A fitted output of a cooling-age calculation — and the machinery
behind it (a model-atmosphere grid, thermal evolution with contraction, radiogenic luminosity,
and **the star's age**) is not ours.

**One layer down is transcribable**: Guillot 2010 eq. (27) with Valencia+ 2013's opacity fit
(Table 1, eleven coefficients, verified against the original by the audit). Transcribed and
run, it gives **1012 K at 1 bar** for γ = 0.032 at 50× solar — the number Valencia's own text
quotes — and the deep isothermal layer emerges rather than being imposed.

**But it needs three inputs the recipe cannot supply**, and this is the survey's real product:

- **T_int** — an output of a cooling track. Literature brackets it (Nettelmann 31.8–42.7 K for
  GJ 1214 b; Valencia 24–80 K over 0.1–10 Gyr), and across 30–60 K the boundary moves ~6×. So
  it can be *declared with a citable bracket*, like the recipe's other declarations.
- **γ** — **no published value for the hot sub-Neptunes this work was meant to open.** Valencia
  warns explicitly: *"for hotter planets, not considered in this study, the value of gamma
  could change significantly."*
- **∇_ad** — 2/7 for H₂ with rotational modes live, retreating toward 4/3 for a metal-rich
  envelope. Composition enters twice, through κ and again here; the choice moves the boundary
  by ~16–24 % depending on the driver.

**So the purpose and the available inputs do not meet.** Opening hot sub-Neptunes by this route
means carrying two or three new declarations, at least one of which has no literature to
declare from. That is an owner decision, not a defect.

**A methodological note kept because it cost an hour.** The directing seat's "independent"
reproduction imported the parallel session's own `T_guillot` and `kappa_safe`, so the
transcription was shared from the start and only the driver was independent. A 14–17 %
disagreement was chased through ∇_ad (wrong — the two runs agreed *because* two different
parameters compensated) before landing on the real pair: **T_irr 600 vs 778 K and g 11.056 vs
8.9683 m/s²**. Matching both put all eight rows on top of each other. Two lessons, both already
in the rules and both re-earned: *numbers agreeing is not causes agreeing*, and *a leg that
imports the other leg's code is not a leg*. Verification of a transcription is comparison
against the source, which is what the audit did.

**Both labels the table owed are paid** (regenerated 2026-08-31, same day). Its gravity now
comes from the curated geometry — 8.41(0.36) M⊕ · 2.733(0.033) R⊕ from
`db/planets_curated.json`, sourced to Mahajan+ 2024 (`2024ApJ...963L..37M`) — giving
g = 11.056 m/s² **± 4.9 %** propagated from the printed errors, and the driver prints that
provenance in its own header rather than leaving it to prose. T_irr stays **unchosen**: the
header carries it as `**UNSOURCED DECLARATION**` and prints what 600 / 700 / 778 K do to
every row, so the gap warns the reader from inside the output. **No verdict moved** — T_int's
dominance is still ~120× (3,156 → 27 bar at 50× solar), the 30–60 K bracket still ~6×, the
four deep rows still extrapolation past Valencia's printed 300 bar; the geometry change made
the absolute values ~14 % deeper, and against Nettelmann's own two T_int values the shallow
end now sits 9× rather than 8× below their 80–800 bar.

*A closure worth keeping*: `2024ApJ...963L..37M` **is** arXiv:2402.05991 — the same Mahajan+
2024 the surveyor had discounted as "a stellar-radius paper, nothing for the
radiative–convective question". It was nothing for that question and it is the source of the
planet's mass and radius, which is what the notes' grouping had said all along. Discounting
it half-closed the loop; opening the DB entry closed it the other way.

## ③ The melting curve — there is a third candidate, and the debate is not the one we asked about

**Asked**: is there a third melting-curve candidate, and is the 100–150 K disagreement settled?

**The third candidate exists**: AQUA's melting boundary — a genuinely different lineage
(Gibbs-energy crossing of Journaux+ 2020's ice and Brown 2018's liquid potentials), and it
needs no transcription, being readable from the distributed phase-ID column. A fourth,
Datchi+ 2000, cannot reach the band (its own experimental ceiling of 750 K arrives at
12.75 GPa) but matters below. **No newer curve exists** — the only post-Queyroux measurement
in this band is Prakapenka+ 2021, paywalled.

**Our curve is not uniformly cold. The ordering inverts near 30 GPa.**

| P (GPa) | ours | AQUA | Queyroux | Queyroux − ours |
|---|---|---|---|---|
| 8.2 | 588.1 | 595.7 | 659.4 | +71 |
| 15.4 | 665.9 | 732.8 | 892.1 | **+226** |
| 20.0 | 704.9 | 822.3 | 1057.0 | **+352** |
| 30.7 | 1262.2 | 966.1 | 1269.5 | +7 |
| 40.0 | 1581.3 | 1109.3 | 1388.9 | **−192** |
| 52.0 | 1941.7 | 1333.6 | 1505.1 | **−437** |

Below the seam our IAPWS piece is the coldest of the four. Above it our Reinhardt piece was the
hottest **of those four** — and that half of the sentence did not survive the day: with
Prakapenka+ 2021 measured onto the same grid (Brief 24, 2026-08-31), **we are nowhere the
hottest above 30 GPa** (ours 1262 / 1581 / 1942 K against Prakapenka's 1605 / 2210 / 2739 K at
30.7 / 40 / 52 GPa). What stands is the shape of the claim, not its superlative: **the ordering
is band-dependent, so "our curve is cold" was never one statement.** The sentence is corrected
here rather than rewritten silently, because a fifth voice would move it again.
(The 7 K meeting at 30.7 GPa is a coincidence of two unrelated curves, labelled as such by the
surveyor before anyone asked — and by the fit's own convention: interpolating Queyroux's
Table S1 points there gives 38 K instead.)

**The 100–150 K question is closed, by the paper we were considering adopting.** Queyroux+ 2020
states it themselves: their resistive- and laser-heated experiments, run in one laboratory,
*"increasingly deviate from all previous RH experiments and better match the LH experiments of
Refs. [19,20]; the agreement is within mutual uncertainties, although our melting temperatures
are systematically 100–150 K lower."* One laboratory running both techniques is the strongest
available refutation of a technique artefact; the older resistive-heated series is the outlier;
and the offset is declared to sit inside mutual uncertainty. The "RH vs LH, unresolved" framing
does not survive contact with the source.

**The live question is the curve's shape, and it is live in 2025.** Rescigno+ 2025 (Nature 640,
662, open access): *"the **continuous** slope of the ice VII melting curve (determined through
direct visualization of sample melting³¹) **disagrees with** classical molecular dynamics
simulations that have found **discontinuous** melting due to the emergence of the plastic
phase."* Their ref. 31 is **Datchi+ 2000** (confirmed in the reference block) — the paper
Queyroux pins their own lower branch to, via its VI–VII–fluid triple point. And F. Datchi is
Queyroux+ 2020's corresponding author, so the tension runs through one author's own record:
this is a real methodological debate, not a laboratory rivalry.

**Therefore adopting Queyroux is choosing a side in a live debate.** Defensible — but it must
be a **named** choice, and it changes what "our curve is cold" means: below 20.6 GPa our IAPWS
piece sits near the *continuous* lineage, and adopting Queyroux moves us to the *discontinuous*
one. What Queyroux buys is exactly the kink — the 14.6 GPa triple point, the two branches, and
the VII′/VII″ structure the dispatch would inherit.

**Two costs that come with it.** The upper branch's Simon–Glatzel coefficients carry ±63 % and
±46 % at 90 %, and **the obvious way to turn that into a band is wrong**: a and b are strongly
correlated, so running the four corners (782 K at 20 GPa, 2188 K at 44 GPa) gives *an upper
bound on the band, not the band*. Those corner numbers must never be quoted as Queyroux's
uncertainty. And the upper branch reaches only 44 GPa, so it moves the wall from 20.6 to
44 GPa — not to 52.4, not to 70 — while the lower branch, being a Datchi refit, replaces the
IAPWS piece too.

**Millot+ 2019 is not a fourth curve.** Now cached, and read: *"Our XRD data up to 320 GPa and
3,800 K provide unambiguous lower bounds for the melting line."* A floor test, useful for
refusing candidates that melt below it, not a curve to compare against. It says nothing about
the 14.6 GPa kink — its range starts far above.

## What this moves

- **Owner decision ② (adopt Queyroux or not) is reframed.** Its cost table lost one item: the
  trial-path hardening it needed is ① (landed 2026-08-31). What remains is not a correctness
  repair but a **choice of lineage**, and it should be recorded with that name.
- **Owner decision on AQUA is new and not urgent**, with the gain named (the cold high-pressure
  corner, now doubly motivated) and the cost named.
- **Hot sub-Neptunes stay closed for now**, and the reason is written: not a missing equation,
  but two or three declarations, one of which has no literature.
- **Paper request, first priority: Prakapenka+ 2021** (Nat. Phys. 17, 1233) — the only
  post-Queyroux measurement in the band, and the only way to know whether that curve was
  confirmed, revised or superseded. ② should not be decided without it. **Obtained the same
  day** (`docs/phase3/_papers/2021NatPh..17.1233P.pdf`): the publisher paywall held against
  the owner's institutional access, and an Unpaywall lookup found the author's final version
  in the GFZ Potsdam institutional repository, deposited there by a co-author. A first pass
  reports that published melting lines diverge by up to **700 K near 50 GPa**, that this
  measurement finds a **slope increase above 29 GPa**, and that its own line sits at higher
  temperatures than the previous ones. **Not yet read against our curve or Queyroux's** —
  that comparison is the next piece of work on ②, and nothing above should be treated as
  its result.

## What no leg has checked

Datchi's 750 K / 12.75 GPa ceiling (surveyor's label: **from the abstract**), Prakapenka's
abstract, the ADS three-way search behind "no newer curve exists", AQUA's phase-ID column
readout, AQUA-vs-`h2o_hot` density agreement (0.07–0.29 %), and Nettelmann+ 2011 §II's quote
(the paper is not in the parallel session's folder; the directing seat's leg). Labelled, not
absorbed.
