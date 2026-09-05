# The silicate melting chain — context notes (Brief 36)

2026-09-02. Registration 9a41aba0 (with item 0 held open); the directing seat answered
(B) with the corrected regime table — the amendment on the checklist preserves the
original registration. Surveys ⑫/⑬ are the literature record; this file records what
was BUILT and the conditions carried.

## 1. What was built

`eos.py`: `silicate_solidus/liquidus/melt_fraction(p, variant)` — the regime-switched
chain (rock to 140 GPa: Monteux+ 2016 eqs (10)–(13) read in the cached primary, the
solidus scale 1.336×10⁹ Pa confirmed at its own line; pure MgSiO₃ above: Deng+ 2023
bdg to the printed 180 GPa triple point, ppv to Deng's own 200 GPa caveat line, Fei+
2021 upper bound to 500 GPa; named refusal above). `Phase.melt = "silicate"` on the
three mgsio3 phases; `Phase.melt_variant` carries the composition branch;
`SILICATE_CHONDRITIC` is the never-melted variant and `interior._stack` seeds it from
`differentiated` (undifferentiated rock+metal layer, and the C11 primitive crust —
both "never melted"). **What the composition actually changes**: not where melting
*starts* (the solidus is shared — HZ96 below 20 GPa, and Monteux's own printed choice
of the A-chondritic eq. (12) for both above), but **how fast the rock finishes
melting** — the liquidus alone splits (+879 K at 140 GPa), so A and F differ in the
window's width and φ's temperature gradient, never in the onset. `t_melt` (solidus)
is therefore variant-blind at every pressure; call `silicate_liquidus` or
`silicate_melt_fraction` to see the branch. φ = (T−T_sol)/(T_liq−T_sol) is Monteux eq. (6), printed — the
single source of truth; C′_p = C_p + ΔH/(T_liq−T_sol) is eq. (17) (ΔH = 4×10⁵ J/kg,
Table 1, Ghosh & McSween 1998), hooked into `Material.c_p` and damping `grad_ad` by
C_p/C′_p in-window. `interior.solve` returns `silicate_melt_state` /
`silicate_melt_fraction_max` from a post-hoc verdict over new `rock_samples`
(same discipline as the ice column: curves consulted after integration).

## 2. Conditions and non-adoptions, recorded

- **Eq. (16) (α′) is printed and NOT adopted.** Adopting the melt expansivity without
  eq. (15)'s melt density (which we also do not adopt — density stays the solid EOS
  everywhere) would mix a melt-expansion gradient into a solid-density column. The
  verdict note says plainly that "molten" names a state and has not moved the radius;
  Δρ/ρ = 1.5 % (Table 1, Tosi et al.) is recorded for the day a melt density is
  grounded.
- **The 20 GPa liquidus construction.** Monteux's three separately-cited liquidus
  branches meet at 20 GPa within 0.040 K (1.6 parts in 10⁵) and the solidus pair
  within 1.002 K — someone constructed that agreement and the paper does not say who
  (Andrault is both a co-author and the 2011 fit's author, so it may be upstream).
  Party unnamed. Andrault+ 2011 [`2011E&PSL.304..251A`](https://ui.adsabs.harvard.edu/abs/2011E&PSL.304..251A) is **held since 2026-09-05**;
  Herzberg & Zhang 1996 [`1996JGR...101.8271H`](https://ui.adsabs.harvard.edu/abs/1996JGR...101.8271H) is **still unobtained** — the owner
  could not get it, and it is one of the only two papers this engine still wants. Whether the one we
  now hold closes this on its own, or the pair was needed, is a verdict the audit seat is forming;
  **this note claims neither**. Pinned in the gate as transcription checks.
- **The 140 GPa seam boundary: the range half is closed, the composition half is not.**
  Monteux prints no number for Andrault's fitted range ("up to … Earth's lowermost mantle
  conditions") and 140 GPa was chosen because Monteux's own model exercises the curves there
  ("melt fraction ≈ 40 % at P = 140 GPa"); the alternative was Earth-CMB 136 GPa.
  **Closed 2026-09-05 by reading Andrault directly** [`2011E&PSL.304..251A`](https://ui.adsabs.harvard.edu/abs/2011E&PSL.304..251A): the paper
  prints its melting curves *"at 30 to 140 GPa"*, so our seam is not outside the measured range —
  it is exactly its top edge. This half needed only Andrault, and Herzberg & Zhang 1996 was never
  required for it.
  ⚠ **What stays open is the 20 GPa junction**, and that one does need the paper we do not hold:
  the low-pressure branch is Herzberg & Zhang's, so "who constructed the agreement at the junction"
  cannot be answered from one side. See also the registered 20–24 GPa window in `eos.py` — Andrault
  calls his own T₀ *"virtual"* because that mineral assemblage is only stable above 24 GPa.
- **The pure-mineral chain above 140 GPa is an upper bound on the rock solidus**
  (refractory pure MgSiO₃ melts above multi-component rock): above it — definitely at
  least partially molten; below it — indeterminate, and the verdict labels the
  region's φ = 0 as "below an upper bound", never "definitely solid". (The corrected
  brief's phrasing had this direction inverted; the labels carry the physical one.)
- **Considered and not done** (the brief's list, recorded): liquidus as a constant
  offset from the solidus (unnecessary — Monteux prints it as an independent fit); an
  unmarked seam (every step measured and pinned); silent extension past validity
  (named refusals at 500 GPa and at Deng bdg's 11.89 GPa arithmetic floor — the range
  limit that lives in coefficients, survey ⑬'s new kind).
- **Nominal width for single-point melters** (140–500 GPa): 150 K, declared,
  filled-in (mid of the brief's 100–200 K band) — unlike the rock window, whose width
  is measured (solidus and liquidus printed separately: 244 K at 1 GPa → 1485 K at
  140 GPa on the F branch). `melt_scale` stays 1.0.
- **Antigorite's empty `melt` is a verdict** (dehydration/breakdown, not congruent
  melting) — written at the phase definition.

## 3. Seams and checks, measured (pinned in test_silicate_melt.py)

Transcription: Deng Table I residuals ≤ ±50 K (the paper's own class), printed
500 GPa extrapolation 9376.6 vs 9376; Fei anchor exact at 140 GPa; Monteux joins
0.040 K / 1.002 K, and the 1336×10⁹ trap scale pinned at 745.6 K. Seams: 140 GPa
rock→implemented curves **+1275.7 K (A) / +396.7 K (F)** on the liquidus and
**+1732.1 K** on the solidus — one basis for both lines: the step between the curves
this code actually returns (rock branch → tm ± 75). *Corrected 2026-09-02 (audit): the
first record quoted the liquidus steps against Deng's bare tm (+1200.7/+321.7), a
different basis than the solidus line beside it. The three candidate bases sit exactly
75 K apart because the nominal width is a declaration — the step numbers depend on
that declaration, which is why the basis must be named.* (A material-kind declaration,
not smoothed);
180 GPa bdg→ppv **+17.98 K** (printed triple point; the fits' own crossing at
173.6 GPa carried as the paper's internal inconsistency); 200 GPa ppv→Fei
**+296.7 K**; 500 GPa closure comparison +47.6 K.

## 4. The motivating question, measured (NOT adopted)

Dante forward (1.5519×10²¹ kg, silicate, no core): cold declaration → `undecided`
(the label says declaring a temperature turns it into a verdict); at Brief 35's
**unvalidated** 2122 K → **`molten`, φ = 1.0** — the tool can now say "magma ocean",
with the limitation labels riding along (solid-EOS density; the 2122 K carries
`failed-io-reproduction`). R stays ~486 km either way. Nothing on any board changed.

Anchors: Earth at the reference 1600 K stays `solid` (61 K margin at the surface,
guarded in the test); U/N bit-identical (test_ice_giant full run, pre-gate).
