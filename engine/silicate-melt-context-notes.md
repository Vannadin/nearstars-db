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
both "never melted"). φ = (T−T_sol)/(T_liq−T_sol) is Monteux eq. (6), printed — the
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
  Party unnamed; Andrault+ 2011 / Herzberg & Zhang 1996 (both unobtained) would close
  it. Pinned in the gate as transcription checks.
- **The 140 GPa seam boundary is range-unconfirmed.** Monteux prints no number for
  Andrault's fitted range ("up to … Earth's lowermost mantle conditions"); 140 GPa
  chosen because Monteux's own model exercises the curves there ("melt fraction ≈ 40 %
  at P = 140 GPa"); the alternative was Earth-CMB 136 GPa.
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
rock→bdg **+1200.7 K (A) / +321.7 K (F)** (a material-kind declaration, not smoothed);
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
