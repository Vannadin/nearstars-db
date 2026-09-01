# The superionic boundary against the 1800 K ceiling — context notes (surveys ⑩·⑩b)

Landed 2026-09-01 from the parallel seat's reports (`H10-millot-fig4-vs-1800K.md`,
`H10b-french2016-fig4.md`, pre-registrations `H10-PREREGISTER.md`/`H10b-PREREGISTER.md`
— read directly, not via relay). Docs only: **no code or constant moved here** — the
constant/gate repairs are Brief 34's. `interior-core.md`'s C6 row is the directing
seat's edit, not this file's.

## §1 The finding, in one sentence each

- **Millot+ 2019 Fig. 4** (2019Natur.569..251M, p. 4): the predicted solid/superionic
  boundary (dashed grey, caption's own word "predicted", from its ref. 15) **peaks near
  204 GPa · ≈2138 K and descends through 1800 K at ≈358 ± 15 GPa** — so between there
  and `ICE_X_P_MAX` = 1000 GPa a column between the boundary and 1800 K would sit on
  `ice_x`, which is what the code's comment says cannot happen. The live check
  (`MILLOT_SUPERIONIC = (100 GPa, 2000 K)` vs a flat line) tests a false premise: the
  boundary is not flat.
- **French, Desjarlais & Redmer 2016 Fig. 4** (2016PhRvE..93b2140F, p. 8 — the paper
  the dashed line comes from; cached, owner-fetched): the same boundary in the source's
  own rendering **peaks at 193 GPa · ≈2124 K, crosses 1800 K at ≈329 ± 25 GPa (solid) /
  ≈335 (dashed)** — and, because its axis runs to 100 Mbar, it shows what Millot's
  cannot: **the ices field is a closed lens that exits the plotted range at
  ≈523 GPa · ≈801 K. Above ~520 GPa there is no ice region at all in this
  calculation, at any plotted temperature.**

## §2 What must be said carefully (the register's four rules)

1. **The crossing's position is not adjudicated.** The two renderings disagree by
   29 GPa and their error bars barely touch (⑩ 343–373; ⑩b 304–354). The honest
   statement: **the 1800 K incursion begins somewhere in 305–375 GPa.** The PEAK is the
   strong confirmation — 0.7 % in T, 5 % in P, across two figures with different axis
   schemes (linear 10–500 GPa vs log 0.1–100 Mbar).
2. **Reading precision rides beside every number.** ⑩: x calibrated on five tick
   intervals (345–350 px/100 GPa, ±1 GPa), y on two intervals (±17 K), dominated by
   dash-centre eyeballing ±58 K → ±9 GPa on the crossing (quoted ±15 to be generous).
   ⑩b: log-axis calibration in exponent space, 508 px/decade ×3 intervals (±1 %),
   y checked against two labels not used in calibration (Δ +1/+3 px), dominated by
   line-centre ±15 px → ±7 % in P. No curve was transcribed in either — inequalities
   and feature positions only.
3. **`ice_x` now has three ceilings, all different, in one place:**
   | ceiling | value | what it is |
   |---|---|---|
   | data | **≈355 GPa** | French & Redmer 2015's own highest simulated density (4.25 g/cc at 300 K) — C6 |
   | stability | **≈520 GPa** (new, ⑩b) | where the ices field closes in French+ 2016 Fig. 4 |
   | printed | **1000 GPa** | SeaFreeze's knot box — **the one the code carries** |
   The smallest is the data ceiling; the one we use is the largest.
4. **Today's answers are not wrong.** The U/N converged mantles sit at ≥2553 K —
   well above the boundary everywhere. **Trial paths are unmeasured**, and that is
   what separates a labeling defect from a convergence defect — Brief 34's first item.

## §3 The attribution finding (its own kind, recorded)

`SUPERIONIC_MIN_T = 2000 K` / `SUPERIONIC_MIN_P = 100 GPa` (and the live copy
`MILLOT_SUPERIONIC`) carry, under Millot's name, **a number Millot's abstract
attributes to refs 6–12** — "Particularly intriguing is the prediction⁶⁻¹² …
exceeding 100 gigapascals and … above 2,000 kelvin" (directing-seat verified in the
cached PDF, as are the quotes below). Millot's own bcc-phase data near the boundary
are "**better interpreted as insulating solid ice**" — the paper does not itself claim
superionic ice below 1800 K; the predicted line it replots does. Kind of result, for
the classification: *a constant sourced from an abstract turned out to be that
abstract's summary of somebody else's prediction* — previous instances were our notes
over-reading a source; this one is a source quoting third parties.

## §4 Why this boundary cannot be waved off — and its own stated limits

The boundary's ice-side potential is **ref. [30] = French & Redmer 2015 (PRB 91,
014308) — the very potential SeaFreeze's `VII_X_French` implements and our `ice_x` is
fitted to.** This is not an external line intruding on our table; it is the authors of
our ice potential computing where their own ice stops being stable. Their own
qualifications (§IV, directing-seat verified): the boundary "lies somewhat low in
temperature", and adding nuclear quantum effects to the MD "would very likely result
in a **lower** melting temperature" — **the stated bias direction starts the incursion
at LOWER pressure, not higher**; the ±0.1 kJ/g sensitivity worry belongs to the
bcc–fcc line, while the SIW–ices line's shifts are "one order of magnitude smaller" —
ours is the robust one. And beyond the ice field they decline to compute: post-ice-X
crystalline predictions exist [69–75] but "the derivation of accurate thermodynamic
potentials for them is not an easy task" — **the field closes; nothing published here
replaces it.** No printed boundary equation or table exists in French+ 2016 (§IV gives
the method only — a legitimate "not found"; the boundary lives as Fig. 4's lines).
