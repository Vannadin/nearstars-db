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

## §5 Where the 1800 K ceiling comes from — the owner's question (2026-09-04, evening)

**Pre-registered outcomes** (directing seat, before the reading): Ⓟ 1800 K is the source's *printed* validity bound →
our ceiling is right, and a Neptune that needs more is "this model cannot solve Neptune", which changes C26's kind;
Ⓠ 1800 K is a number *we* drew → find why, and an absent reason is itself the finding; Ⓡ the source states no upper
bound → record as unresolved, and do not fill it with AQUA's 2291 K (a seam of someone else's table, not our fit's
range). **In no outcome does the ceiling move**; AQUA is not evidence here (its region is M19, the same source as
`h2o_hot`, and its 2291 K flat line is AQUA's own construction).
*Addendum 2026-09-04 (parallel seat, scratch-only, audited): the M19 identity holds at the refusal point — 923.6 GPa lies above
AQUA's own 700 GPa hand-over to M19 (AQUA §2.3.3); between 100 and ≈722 GPa the AQUA and Mazevet densities differ (+6.33 % at
100 GPa · 1995 K, zero crossing ≈228 GPa, −2.1 % at 317 GPa). Substituting AQUA's region 5 (Brown 2018) into `h2o_hot` over
1–100 GPa perturbs the `h2o_hot` call path (branch at call 1533; 8837 → 8308 calls) yet leaves every `PhaseGap` the solve raises
bit-identical — all seven, including the ceiling refusal at h2o · 923611757256.9896 Pa · 1800.0000005870 K (t − 1800 = 5.9e−7 K,
consistent with the "< 0.5 K" in ② below). Pre-registered outcome Ⓐ; the report and pre-registration live in the parallel seat's
scratch, not the repository.*

**① What the number is.** `ICE_VII_X_T_MAX = 1800.0` (`eos.py`) is the **upper knot of the temperature axis of
SeaFreeze v1.1.0's `VII_X_French` spline**, read out of the shipped `.mat` on 2026-08-27 (`ice-x-context-notes.md`:
*"Reading its knot domain out of the shipped spline gives 1.7 GPa to 1000 GPa, 20 K to 1800 K"*; the same reading
gave `ICE_X_P_MAX` = 1000 GPa). It is stored as a `Phase.t_max` and the refusal fires at `t > t_max` (`eos.py@«if ph.t_max and t > ph.t_max:»`).
⚠ The reading could not be repeated tonight: no `seafreeze` module is importable from `/usr/bin/python3` or
`/opt/homebrew/bin/python3`, and no venv was found under `~/Desktop` (SESSION-HANDOFF names the rebuild,
`pip install SeaFreeze==1.1.0`). The 08-27 record stands as the provenance; it is not re-verified here.

**③ What the source says above 1800 K.** French & Redmer 2015 (`2015PhRvB..91a4308F`, cached PDF; the cache's
`1411.6017.md` is a different paper — HD 209458b — and was not used):
- §III (extraction line 211): *"The densities were varied between 1.6 and 4.25 g/cm³, and the temperatures were chosen
  from 295 up to 2000 K. Additional simulation runs at 2250 K and higher temperatures resulted in either molten or
  superionic structures."* — the **data ceiling in temperature is 2000 K**, 200 K above our knot.
- Abstract (line 38): *"The EOS derived in the present work is valid in the entire stability region of ices VII, VII*,
  and X and is well behaved in extrapolation."* — the validity bound is the **stability region**, not a temperature;
  the same authors draw that region as a curve in French+ 2016 Fig. 4 (peak ≈2124 K at 193 GPa, through 1800 K at
  ≈329 GPa, closing at ≈523 GPa — §1 above).
- No sentence prints 1800 K, and no sentence prints a temperature limit as a number other than the 2000 K of the grid.

**Outcome — none of Ⓟ/Ⓠ/Ⓡ as written; named Ⓢ, "the intermediary's box".** The ceiling is neither the source's printed
bound (Ⓟ: the source's own grid goes to 2000 K and its stated bound is the stability *region*) nor a number we chose
(Ⓠ: we read it, we did not draw it); it is the knot box of the packager's spline, **200 K under the source's data
ceiling and unrelated to the stability boundary** — the same kind of fact as `ICE_X_P_MAX` = 1000 GPa being the knot
box over a 355 GPa data ceiling (C6), only in the other direction: there the box is too wide, here it is too narrow.
Ⓡ's instruction is kept: nothing is filled from AQUA. **The ceiling does not move** (a move is a separate decision
and moves anchors).

Two consistency notes, recorded not repaired: (a) the refusal *message* (`eos.py:2449` ff.) still explains the ceiling
with Millot+ 2019's *"100 GPa · above 2000 K"* sentence, which the constant's own comment (`eos.py@«# 온도 천장. **매듭 구간의 상한이지 상 경계가 아니다.** 1800 K 위에 초이온상이 놓인다는»`) had already
found misattributed (Brief 34) — message and comment disagree; (b) `test_interior.py` (d) guards that the 1800 K
ceiling and the Reinhardt melting line at 47 GPa, equal as numbers, stay different objects — consistent with Ⓢ.
⚠ (a) repaired 2026-09-04 (owner-approved; the commit titled "fix(eos): the ice_x temperature-ceiling refusal now names the knot box"): the message now names the knot box, drops Millot+ 2019, keeps FR2016 — string only, constants and anchors unchanged.

**② Does Neptune need more than 1800 K, and how much?** Measured on a scratch copy of `engine/` with
`column_steam_allowed = True` (the window open under envelopes; worktree untouched, nothing committed):
`test_ice_giant._solve("Neptune")` refuses in 1 s, at first contact —

    막힌 재료: h2o, 압력 923.6118 GPa, 온도 1800 K   (t > 1800 by less than 0.5 K; printed rounded)

so the wall is met at **≈924 GPa**, which is above the *stability* ceiling (≈520 GPa — French+ 2016's ices field is
closed there at every temperature) and far above the data ceiling (≈355 GPa). Reading: what Neptune's open-window
column meets at 1800 K is not a superionic-ice question at all — at 924 GPa the source's own authors have no ice of
any kind — it is the ladder being consulted where only its extrapolation exists (C6's "upper two thirds"). **How much
above 1800 K the converged column would sit cannot be measured**: the solve stops at first contact and there is no
representation to continue on (that is C26). The C24 record "refuses at ice_x's 1 800 K ceiling" is now specific:
924 GPa · 1800 K, first contact.

**What this changes for C26**: its object is a *fluid/superionic water representation at ~500–1000 GPa*, above the
ices field, not "ice above 1800 K" — French & Redmer 2016's two superionic potentials (named in the refusal message)
are the candidate; whether `h2o_hot` (M19) should be consulted there instead is a dispatch question the ladder's
`liquid_material` does not ask today. Listed as the question; not started.
