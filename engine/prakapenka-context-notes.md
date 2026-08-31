# Prakapenka+ 2021 against our curve, Queyroux and AQUA — context notes

Brief 24, 2026-08-31. Material for owner decision ② — no adoption verdict here, and no
"our curve is right/wrong" frame (survey ③ showed the ordering flips by band).
Pre-registration in `prakapenka-checklist.md`.

## §1 The source, and where the numbers come from

`docs/phase3/_papers/2021NatPh..17.1233P.pdf` — Nature Physics 17, 1233 (GFZ Potsdam OA
author copy), **54 pages, supplementary included** (Notes, Tables 1–4, Figures 1–15+).
The directing session's three quotes verified in the full text (700 K spread at ~50 GPa ·
slope-jump controversy at 20–47 GPa with two competing triple-point assignments · their
own "abrupt increase in slope of the melting line above 29 GPa" and the abstract's "higher
temperatures than previously determined in static compression experiments … in agreement
with theoretical calculations and data from shock wave experiments").

**The melting line is printed as equations — no digitizing.** Supplementary Table 3 gives
Simon–Glatzel parameters per phase line, with asymmetric uncertainties:

| line | P₀ (GPa) | T₀ (K) | a | n |
|---|---|---|---|---|
| Ice VII melt | 2.17(5) | 354.8(5) | 1.25 (−0.2/+0.35) | 2.85 (−0.1/+0.25) |
| bcc-SI melt & bcc–fcc SI | 17.5(5) | 880(10) | 3.4 (−0.3/+0.5) | 3.15 (−0.15/+0.25) |
| fcc-SI melt | 27.5(7) | 1290(15) | 4.4 (−0.8/+1.0) | 2.5 (−0.3/+0.1) |

Form: the supplementary's rendering loses the constant, but **P = P₀ + a[(T/T₀)ⁿ − 1]**
is confirmed by transcription checks, run before use: P(T₀) = P₀ on every segment; the
Ice VII segment evaluated at the next segment's T₀ = 880 K gives 17.56 GPa ≈ its P₀ 17.5
(continuity); the fcc segment at 190 GPa gives 5523 K, beside the Millot+ 2018 shock point
(~5000 K at 190 GPa) the paper itself cites as the only high-P measurement. One printed
non-closure recorded as-is: the bcc-SI segment at T = 1290 K gives 25.4 GPa against the
fcc segment's P₀ = 27.5 — the segments are fits per line, not a spliced single curve, and
the ~2 GPa mismatch sits exactly in their slope-anomaly region. Central values only; the
printed asymmetric uncertainties are carried in the table above, not propagated.

## §2 The four-way table (survey ③'s grid and columns, plus Prakapenka)

| P (GPa) | ours | AQUA | Queyroux | **Prakapenka** | Prak − Queyroux | Prak − ours |
|---|---|---|---|---|---|---|
| 8.2 | 588.1 | 595.7 | 659.4 | **658.4** | −1 | +70 |
| 15.4 | 665.9 | 732.8 | 892.1 | **838.0** | −54 | +172 |
| 20.0 | 704.9 | 822.3 | 1057.0 | **1048.3** | −9 | +343 |
| 30.7 | 1262.2 | 966.1 | 1269.5 | **1605.2** | +336 | +343 |
| 40.0 | 1581.3 | 1109.3 | 1388.9 | **2209.9** | +821 | +629 |
| 52.0 | 1941.7 | 1333.6 | 1505.1 | **2738.8** | +1234 | +797 |

(ours/AQUA/Queyroux columns are survey ③'s, unchanged; the Queyroux column there is the
fit convention its footnote states. Segment used: Ice VII melt at 8.2/15.4, bcc-SI at
20.0, fcc-SI at 30.7/40.0/52.0.)

## §3 Branch judgment — 1 below the anomaly, 2 above it, 3 overall

- **Below ~20 GPa, Prakapenka supports Queyroux against ours (branch 1 for that band)**:
  at 8.2 GPa they are 1 K apart; at 20.0 GPa 9 K apart; both sit 70–350 K above our IAPWS
  piece. At mid-band Prakapenka runs somewhat colder than Queyroux (−54 K at 15.4 GPa,
  −103 K at Queyroux's own 17.3 GPa point) — same side of ours, smaller margin.
- **Above ~30 GPa, Prakapenka disagrees with everyone, on the absolute-temperature axis
  (branch 2)**: +336…+1234 K above Queyroux and +343…+797 K above our Reinhardt piece,
  growing with pressure. This is the paper's own claim in numbers ("higher temperatures
  than previously determined in static compression"), and the disagreement's other axis
  is the anomaly's **location/assignment**: Prakapenka puts the slope jump at ~27.5–29 GPa
  (fluid–bcc-SI–fcc-SI), Queyroux's family reads a fluid–VII–VII′ structure near
  14.6 GPa/850 K — the controversy the paper names stays open.
- **Branch 3 stands and sharpens**: the ordering is band-dependent, and one survey-③
  sentence is **superseded by the new number** (re-opened per today's rule): *"above the
  seam our Reinhardt piece is the hottest"* was true of the four curves surveyed; with
  Prakapenka in the room ours is no longer the hottest anywhere above 30 GPa. The survey
  note is the directing seat's file — flagged to them rather than edited here.

**Re-opened old numbers, checked against the new one**: F4's record "Queyroux sits hotter
than both our curves in the disputed band" — still true, now with a third voice sitting
between (15.4–17.3 GPa) or alongside (8.4, 20 GPa). F4's grade reasoning and C3's
dispatch are untouched — nothing here changes a verdict; the 700 K literature spread the
paper quotes at ~50 GPa sits beside our own table's spreads at 52 GPa — **the four-way
spread is 1405.2 K** (highest Prakapenka 2738.8, lowest AQUA 1333.6), and the
Prakapenka−Queyroux gap alone is 1233.7 K. (An earlier draft printed 1233 K *as* the
four-way spread — a mislabel the directing session's reproduction caught; both numbers
are true, the name was wrong.) Consistent in direction with their sentence; recorded,
not judged.

## §4 What did not move

No code, no anchor, no gate change (docs only; gate delta 0 — nothing new executes).
Reproduction: the transcription checks and grid values are one script
(`scratchpad/prakapenka_grid.py` shape — three Simon–Glatzel tuples and an inversion);
every input number above is printed in Supplementary Table 3 of the cached PDF.
