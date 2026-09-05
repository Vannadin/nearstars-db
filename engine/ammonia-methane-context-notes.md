# Ammonia and methane — context notes

C4 closes **without code**, so these notes are the deliverable besides the row itself.

## The three routes, and why each fails

The ice-giant envelope is water alone for a water–ammonia–methane mixture. The tables that
would replace it were looked for on 2026-08-27 (the coverage review) and again on
2026-08-30 with the paper cache and ADS.

1. **Bethkenhagen+ 2017** (2017ApJ...848...67B, open access, full text in
   `docs/phase3/_papers/1709.04133.md`). The paper describes its grid precisely — pressure
   and internal energy on a ρ–T grid to 1000 GPa and 20 000 K, thirteen isotherms
   (1000–8000 K in 1000 K steps, 10 000–16 000 K in 2000 K steps, 20 000 K), at least ten
   densities per isotherm — and its Table 1 gives diffusion coefficients and profile
   quantities, not the equation of state. The text carries **no data-availability
   statement and no URL** (grep for "availab", "github", "http" finds only the diffusion
   sentence about literature values). The grid is described; the numbers are not published.
2. **Bethkenhagen+ 2013** (2013JChPh.138w4504B, doi 10.1063/1.4810883), the ammonia source
   the 2017 paper extends — 330 GPa, 500–10 000 K, with nuclear-quantum corrections the
   2017 work removes for consistency. Written here as an AIP paywall, and **that is out of date**:
   the owner obtained it on 2026-08-30 and `ammonia_table.py` was baked from it (the ledger in
   `interior-core.md` has said so since). What the abstract alone could not give, the paper did.
3. **FPEOS**, Militzer+ 2021 (2021PhRvE.103a3203M, open access). It genuinely distributes
   tables and interpolation code for H, He, B, C, N, O, Ne, Na, Mg, Al, Si and eleven
   compounds including **CH₄** — but **no NH₃**, and its range is "∼10⁴ to 10⁹ K", which
   begins above the ice-giant adiabat this recipe integrates (5500–6300 K at the centre).
   Two independent reasons, either sufficient.

So an author request is the only remaining route. Bethkenhagen+ 2013 is added to the
owner's paper-request list by the row; the 2017 tables live with the same group.

**Not tried and not worked around**: reading tables off figures, or reconstructing the
mixture from a different ab initio set. Both are the fabrication the audit checks for.

## The two sentences the list got wrong

**"Its price is bounded."** It is not. Bethkenhagen+ 2017's 2.1 % (ternary, along Uranus
profiles) and 4 % (binaries, an upper limit) measure the linear mixing approximation —
mixing three complete equations of state by additive volume — against the real mixture. The
substitution this recipe makes never takes that step: it is the difference between a water
EOS and a mixture EOS, a different quantity the cited literature does not measure. `eos.py`
already says this at `AVL_ICES_DEVIATION`; the methodology's "what that number does not
cover" paragraph says it; the C4 row now says "not bounded, not estimated" rather than
"not quantified" alone.

**The sign, in three tiers.** Only the first tier carries a number, and it is marked derived:

| tier | statement | status |
|---|---|---|
| composition | water **overestimates** the ice density: solar-ratio mixture (0.31 : 0.08 : 0.61 CH₄ : NH₃ : H₂O by mass, Bethkenhagen+ 2017 §V) has mean molecular weight 17.28 vs 18.02 → 4.27 % at equal number density; electrons per unit mass H₂O 0.555 < NH₃ 0.587 < CH₄ 0.623 e/amu agree in direction. Correcting it lowers the density and **enlarges** a planet already too large — about 1.5 % in radius for a one-third-density-perturbation scaling | derived, direction + |
| thermal | atoms per unit mass H₂O 3/18 < NH₃ 4/17 < CH₄ 5/16 → higher heat capacity, shallower adiabat, colder and denser interior, radius pulled back (Bethkenhagen+ 2017's icy Uranus: T_core ~ 4000 K). But that is an ideal-gas intuition; dissociation at high pressure shrinks the difference and with it the sign | mechanism named, sign ungrounded |
| net | — | needs the tables |

Writing "1.5 % worse" would quote the first tier as if it were the third.

Derivations, so the audit can re-do them: μ = 1 / (0.61/18.015 + 0.08/17.031 + 0.31/16.043)
= 17.277; 18.015 / 17.277 − 1 = 4.27 %. Electrons per amu: 10/18.015, 10/17.031, 10/16.043.

## Why closing it unbuilt costs nothing the recipe was counting on

C5 was attributed on 2026-08-30 (the directing session's finding, from Nettelmann+ 2016 and
Helled+ 2020): the ice giants' residual belongs to a thermal boundary layer at the
ice/rock–H/He transition and to the inner mantle's ice:rock ratio, and the
central-temperature excess is what an adiabatic H/He envelope produces. C4 is therefore not
a candidate for that residual in either direction — the composition term would widen it and
the thermal term has no sign — and the row that used to point at C4 for it no longer needs
to. The domain prose in the methodology (the ice-giant anchor table's closing sentence, EN
and KO) now carries the three tiers instead of "not quantified" alone.

## What would reopen it

The tables. If Bethkenhagen's group answers, the shape is `make_hhe_table.py`'s: bake the
grid, mix by additive volume with `AVL_ICES_DEVIATION` as the stated width, and re-solve
Uranus and Neptune with `SOLAR_ICE_MASS_FRACTIONS` as the declared ratio. The
`ice_giant_anchor.json` gate would then measure the net tier directly.
