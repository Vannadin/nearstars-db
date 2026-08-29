# Where the giants' leftovers belong — context notes

Decisions taken while closing C5 of `interior-core.md`, and the runs behind them.

## Provenance, done before anything was written

Neither Nettelmann+ 2016 nor Helled+ 2020 was in the cache; both preprints
(1605.00171, 1909.04891) were fetched with `fetch_arxiv_texts.py` before any number was
used. What the brief carried and what the text says:

| brief | in the text? |
|---|---|
| boundary near **0.1 Mbar** | yes — Table 1 (P^(LB) ≈ 0.1 Mbar), §4 opening, Fig. 8 and §6 |
| "**2 to 3 warmer core temperatures**" / "**presence of rocks is required**" | yes — §7 conclusions, verbatim |
| ΔT = **2500 K** (U15-II), **4700 K** (U15-III); ≈ 5000 K / 9000 K hotter centres | yes — Fig. 9 caption, §6 |
| "**1× solar I:R**" favoured | yes — §6; but no mass fraction is printed, so the rock declaration has **no pinned value** |
| "even when uncertainties in the ice:rock ratio are taken into account" | the abstract's wording; §3's own sentence is that the I:R uncertainty "does not provide a solution to the **low luminosity** of Uranus" — a cooling-time result, not a gravity-fit one. Quoted as such |
| Helled 2020's lapse-rate sentence | **not in the markdown** — `grep lapse` finds nothing — but it is in the ar5iv HTML, which the markdown extraction dropped. Verified there, quoted verbatim |

The two-number lesson is now three: "2–200 GPa" (C3) and "0.1 Mbar" (C4) were relayed by
the directing session from a parallel report without a text check, and the lapse-rate
sentence would have been the third had the HTML not been searched. **A number handed down
by the directing session is checked like any other** — that is this loop's discipline, and
it caught the directing session twice today.

## The two declarations, and how they were wired

`boundary_temperature_jump`: when the outward integration leaves the ice mantle for the
H/He envelope, the temperature drops by the declared step — the interior is that much
warmer than an adiabat continued through the boundary, which is what a stably stratified
TBL does. If the step exceeds the temperature at the mantle top the refusal is thrown as
too cold, so the temperature bracket raises the centre and tries again. Applied at both
layer-switch sites (the in-step boundary cut and the loop-top threshold).

`mantle_rock_fraction`: silicate mixed by additive volume into whatever water phase the
melting-curve dispatch chose, above the ocean table's 2.3 GPa only (the inner envelope of
Nettelmann's three layers; an ocean does not carry rock, and the ocean table has no c_P to
weight a mixture's ∇_ad). A water–rock `Mixture` needs the water phase's c_P and ∇_ad;
`HotWater` had neither, so both were added from `water_hot`'s own P(ρ,T) and U(ρ,T) by the
same identities `Material` uses. `dtdp_adiabat` was deliberately **not** added to
`HotWater`: the integrator prefers it when present, and that would have moved every ice
giant off its anchor. Pure-water paths are bit-identical by construction — `--fast` PASS on
the frozen convergence points.

Rejected: mixing rock into the ocean/shallow ice as well (first attempt). Neptune's cold
trial paths reach the liquid-water table and its `LiquidWater` carries only a published
dT/dP|_S, not c_P, so the mixture could not weight ∇_ad there — and a rock-bearing ocean
is not the physics anyway.

## The runs (declared, not tuned)

Full solves, `body_class="ice_giant"`, Scheibe+ 2019 compositions as in the gate, 1-bar
temperatures 76 / 72 K. Each 35–70 s.

| body | ΔT (K) | rock | radius (R⊕) | ΔR | T_c (K) | P_c (GPa) | converged |
|---|---|---|---|---|---|---|---|
| Uranus | 0 | 0 | 4.198853 | +5.48 % | 6160 | 1220 | yes (anchor) |
| Uranus | 2500 | 0 | 4.298818 | +7.99 % | 11493 | 1198 | yes |
| Uranus | 4700 | 0 | 4.380494 | +10.04 % | 15661 | 1181 | yes |
| Uranus | 0 | 0.10 | 4.125818 | +3.64 % | 6275 | 1324 | yes |
| Uranus | 0 | 0.20 | 4.053761 | +1.83 % | 6369 | 1442 | yes |
| Uranus | 2500 | 0.10 | 4.203932 | +5.61 % | 11630 | 1314 | yes |
| Uranus | 2500 | 0.20 | 4.110664 | +3.26 % | 11718 | 1449 | yes |
| Neptune | 0 | 0 | 4.210086 | +8.94 % | 6296 | 1533 | yes (anchor) |
| Neptune | 2500 | 0 | 4.309122 | +11.50 % | 11886 | 1513 | yes |
| Neptune | 4700 | 0 | 4.389406 | +13.58 % | 16241 | 1498 | yes |
| Neptune | 0 | 0.10 | 4.135931 | +7.02 % | 6401 | 1659 | yes |
| Neptune | 0 | 0.20 | 4.062888 | +5.13 % | 6486 | 1800 | yes |
| Neptune | 2500 | 0.10 | 4.212589 | +9.00 % | 11994 | 1655 | yes |
| Neptune | 2500 | 0.20 | 4.117950 | +6.56 % | 12053 | 1819 | yes |

What the table says, in the order the paper says it:

- **The boundary layer widens the residual.** +2.5 %p per 2500 K on both planets. A warmer
  interior is less dense at the same pressure, exactly Nettelmann's §6 premise. It also
  raises the centre by ≈ 5 300 K per 2500 K of step, against their "≈ 5000 K higher" for
  class II — a check the recipe did not aim at.
- **Rock narrows it.** ≈ 1.8 %p per 0.10 of mantle rock on Uranus, ≈ 1.9 on Neptune, with
  the centre warming ~100 K per 0.10 (denser mantle, deeper adiabat).
- **Neither published value closes either planet alone**, and the two together restate the
  paper's chain rather than solving it: at ΔT = 2500 K, Uranus would need roughly 0.3 of
  rock and Neptune roughly 0.6 to reach zero. Those are extrapolations of this table, not
  declarations — no source prints a mass fraction, "1× solar I:R" is not converted here, and
  a fraction chosen to land on zero would be a fit wearing a declaration's clothes. So the
  row carries the grid and the slopes, and no closing value.
- **The Neptune/Uranus asymmetry survives every column**: Neptune's residual is ~3.4 %p
  larger than Uranus's at every declaration, so whatever closes it is not the same
  declaration for both — consistent with the review's point that the two are not the same
  planet twice.

## (a) Jupiter — reached, no consumer

Two transcribable forms: Helled & Stevenson 2017's closed Z(m) (in the cache, line 61 of
1704.01299) and Howard+ 2023's Juno-constrained dilute-core models. Not implemented,
because nothing would read it: Alpha Centauri A b's radius is a declaration. The core list's
"graded inward" is corrected to Debras & Chabrier 2019's four-region shape, whose §4.1
title states the local ∇Z > 0.

## What else moved

- `test_giant.py --table` prints a T_c column; the giant anchor table in the methodology
  (EN and KO) carries it: Jupiter 14 314 K, Saturn 6 930 K, Uranus 6 160 K, Neptune 6 296 K,
  Alpha Centauri A b 8 930 K. The Alpha Centauri A b row had also drifted (59 962 km /
  0.2875 / 790 GPa in the prose against the generator's 64 934 km / 0.2697 / 659 GPa); the
  generator's numbers are the ones in the table now.
- `chain.yaml`: the two declarations recorded beside `gas_mass_fraction`.
- Path functions touched (`solve`, `shoot`, `_shoot_pressure`, `integrate` signatures);
  `--refresh` in the landing commit, values bit-identical.

## Gate cost

No new work on the anchor path; the declaration branches are skipped at 0. `HotWater.c_p`
is only called inside a mixture.
