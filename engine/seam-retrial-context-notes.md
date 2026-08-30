# The seam retrial (F1) — context notes

C3's row named Kimura 2023 as the arbiter of the 20.6 GPa seam before the paper was in
hand. The paper is in the cache now. **This is not a defence of C3**: the criterion below was
fixed before any comparison was run, and the row's fate follows from it.

## What the paper actually contains (read from the PDF, `pdftotext -layout`)

Kimura & Murakami 2023, J. Chem. Phys. 158, 134504 (2023JChPh.158m4504K, checked by title).
Brillouin scattering in a CO₂-laser-heated diamond anvil cell; melting identified by the
appearance of the liquid's Brillouin peaks; temperatures by two-colour pyrometry with a
stated total uncertainty of **6–11 %** per run (§II), each Table I point carrying its own
figure in parentheses (±130–150 K). Pressure from the diamond Raman edge before and after
heating, plus a thermal-pressure estimate P_th; the melting pressure is P + P_th.

**Table I** (20 rows) is the data. Twenty rows, but only **fifteen are measured melting
points**: the five rows at P + P_th = 7.8, 9.3, 11.7, 15.6 and 21.3 GPa carry a starred
temperature that the caption defines as *"estimated from the melting curve proposed by
Queyroux et al."* — they are liquid-velocity runs at an assumed T_m, not measurements of T_m.
The measured points run from **25.9 GPa (1300 K) to 53.6 GPa (1970 K)**.

**Equation (2)** (Kimura & Murakami's numbering) is a Simon–Glatzel fit,
T_m = T_ref ((P_m − P_ref)/A + 1)^(1/C), anchored at Queyroux+ 2020's triple point
(P_ref = 14.6 GPa, T_ref = 850 K — *Queyroux's* point, adopted, not measured here), with
**A = 21.0(59)** and **C = 1.32(23)**.

Consequence for the seam: **Kimura measures nothing below 25.9 GPa.** The seam sits at
20.6 GPa, and the band C3 called disputed is 16.5–20.6 GPa. Below 26 GPa the only thing
Kimura offers is eq. (2), which is an extrapolation of a fit whose low-pressure anchor is
Queyroux's triple point, not Kimura's own data. That limits what this retrial can decide,
and the limit is written here before the numbers.

## The criterion, fixed before the comparison

1. **Where Kimura has a measured point (25.9–53.6 GPa)**: Reinhardt's line, interpolated to
   P + P_th, "sits with" Kimura if |T_Reinhardt − T_Kimura| ≤ the uncertainty Kimura prints
   for that point. Reinhardt prints no per-point uncertainty (its `.dat` carries none and the
   paper gives none), so the combined uncertainty is Kimura's alone — the conservative
   direction. Verdict per point: inside / outside.
2. **At the seam and in the disputed band (≤ 21.3 GPa)**, no measured point exists. Eq. (2)
   is compared as what it is — a fit anchored on Queyroux — against IAPWS eq. (5) and against
   Reinhardt, and the residual is reported against the **5 % in melting temperature** this
   project has used as the disqualifying scale (17 % rejected Frank+ 2004; 26 % is the step
   under review), chosen before seeing eq. (2)'s values. This tier can *inform* the band's
   width; it cannot by itself reopen C3, because it is not a measurement at those pressures.
3. **Everything is a table** — per-point residuals, then a summary. The pre-registered
   outcomes (Reinhardt / IAPWS / between) are read off tier 1 for the overlap and tier 2 for
   the band, and the row's fate follows: measured points inside Kimura's error → C3 stays
   closed with a *revisited* line; measured points siding with IAPWS → C3 reopens; between →
   the band is redrawn to what the measurement supports and the dispatch decision is checked.

## The comparison (run after the criterion above was written)

**One reading of Table I had to be settled first.** Several pressures carry more than one
row (31.2 / 31.4 GPa at 1560 and 1693 K; 37.2–37.4 GPa at 1530, 1610, 1690 K; 41.1 / 41.2;
51.5 / 51.6; 53.5 / 53.6). These are liquid-phase velocity runs at increasing laser power at
one pressure; melting is "identified based on the appearance of the Brillouin peaks derived
from the liquid phase", so the melting temperature at a pressure is the **lowest** temperature
at which the liquid was seen there, and the hotter rows are the liquid above its melting
point. Kimura's own eq. (2) confirms the reading: at 31 GPa it gives 1316 K, beside the
1300 K row, not the 1693 K one. So tier 1 is run on the lowest-T row per pressure group
(seven points inside Reinhardt's range), and the all-rows table is kept beneath it so nothing
is hidden.

**Tier 1 — measured points against Reinhardt's line (2022 `coex-line-liquid.dat`, interpolated
to P + P_th).** Criterion: |Reinhardt − Kimura| ≤ Kimura's printed uncertainty.

| P + P_th (GPa) | Kimura T_m (K) | Reinhardt (K) | residual (K) | / σ | inside? |
|---|---|---|---|---|---|
| 25.9 | 1300 ± 140 | 1129 | −171 | −1.22 | **no** — Reinhardt colder |
| 30.7 | 1300 ± 140 | 1262 | −38 | −0.27 | yes |
| 37.2 | 1530 ± 140 | 1487 | −43 | −0.31 | yes |
| 41.1 | 1570 ± 140 | 1618 | +48 | +0.35 | yes |
| 47.3 | 1730 ± 140 | 1808 | +78 | +0.56 | yes |
| 49.6 | 1770 ± 140 | 1874 | +104 | +0.74 | yes |
| 51.5 | 1860 ± 140 | 1928 | +68 | +0.48 | yes |
| 53.5 | 1910 ± 140 | — | beyond Reinhardt's 52.4 GPa | | |

Six of seven inside; the one outside is the lowest measured pressure, where the measurement
is **hotter** than the simulation by 171 K (1.2 σ). Over 30–52 GPa the simulation sits inside
the measurement's error at every point, with no systematic sign (three below, four above).

All rows, for completeness (the hotter rows at a repeated pressure are liquid above T_m and
are not melting points; they read as "outside" only because they are not T_m):

| P + P_th | T (K) | Reinhardt | residual | / σ |
|---|---|---|---|---|
| 31.2 | 1560 ± 140 | 1280 | −280 | −2.0 |
| 31.4 | 1693 ± 150 | 1287 | −406 | −2.7 |
| 37.3 | 1610 ± 140 | 1490 | −120 | −0.9 |
| 37.4 | 1690 ± 150 | 1494 | −196 | −1.3 |
| 41.2 | 1630 ± 140 | 1622 | −8 | −0.1 |
| 51.6 | 1930 ± 130 | 1930 | 0 | 0.0 |
| 53.6 | 1970 ± 130 | — | | |

**Tier 2 — the seam and the disputed band, where Kimura has no measured point.** Eq. (2),
Kimura & Murakami's Simon–Glatzel fit (anchored on Queyroux+ 2020's triple point, 14.6 GPa ·
850 K; A = 21.0(59), C = 1.32(23)), against IAPWS eq. (5) and Reinhardt:

| P (GPa) | eq. (2) (K) | IAPWS eq. (5) | Reinhardt | eq. (2) vs IAPWS | eq. (2) vs Reinhardt |
|---|---|---|---|---|---|
| 14.6 | 850 (anchor) | 659 | 624 | +29 % | +36 % |
| 16.5 | 908 | 675 | 713 | +35 % | +27 % |
| 18.0 | 952 | 686 | 782 | +39 % | +22 % |
| 20.0 | 1011 | 705 | 875 | +43 % | +16 % |
| **20.6** | **1028** (968–1155 at ±1σ in A, C) | **715** | **902** | **+44 %** | **+14 %** |
| 26.0 | 1181 | — | 1133 | | +4 % |
| 30.0 | 1289 | — | 1237 | | +4 % |
| 40.0 | 1550 | — | 1581 | | −2 % |
| 50.0 | 1797 | — | 1885 | | −5 % |

The 5 % scale: within the measured range (26–50 GPa) the fit and Reinhardt agree to 2–5 %,
inside it. At the seam the fit is 14 % above Reinhardt and **44 % above IAPWS** — but that
number is an extrapolation of a fit whose low end is Queyroux's triple point, and the fit's
own 1σ spread at 20.6 GPa is 968–1155 K. It does not measure the seam; it says which side of
the seam the experimental picture is on.

## Verdict, read off the tables by the pre-registered rule

**Kimura sits with Reinhardt.** Over the overlap the simulation is inside the measurement's
stated error at six of seven melting points, and the one miss has the measurement *hotter*
than the simulation — further from IAPWS's 715 K end, not closer. At the seam, where Kimura
does not measure, its Queyroux-anchored fit also lies above Reinhardt. Nothing in the paper
sides with IAPWS's end; the +26 % step is not an artefact of the simulation.

So by the rule written above: **C3 stays closed, with a dated *revisited* line.** The seam
number does not change (the splice and both curves in the code are what they were), so no
"26 %" anywhere needs updating. What the retrial adds:

- the disputed band is **not redrawn narrower**: the measurement does not support IAPWS's end
  at all, and the experimental side at 20.6 GPa is Reinhardt's 902 K or above (the fit's
  968–1155 K). If anything the band's IAPWS edge is the questionable one. The dispatch
  decision (IAPWS to its end, Reinhardt above) is unchanged: replacing IAPWS's last five
  gigapascals with a fit extrapolated from a triple point would be trading a measurement for
  an extrapolation, the same trade C3 refused in the other direction;
- the grade of Reinhardt's line **stays analog**, and the reason is stated: the check is real
  but its own error is 8–11 % per point, larger than the 5 % scale this project treats as
  calibrated, and it covers 26–52 GPa, not the seam. "Analog, with a measured check inside
  its error over 30–52 GPa" is the honest sentence;
- Kimura is **not baked as a source**: its measured range (26–54 GPa) does not reach the
  seam, its points are ±140 K, and its fit is anchored on another paper's triple point.
  Range versus provenance was weighed and provenance did not win where the measurement does
  not exist. Table I's melting points enter `test_interior.py` as a **check table**, with the
  row/column provenance, so the six-of-seven statement is re-run by the gate.

## What would still change this

A measured melting point between 15 and 26 GPa. Queyroux+ 2020 (now in the cache, F-series)
is the paper with the triple point at 14.6 GPa and XRD melting to 45 GPa; its data, if
tabulated, are the ones that would put a measurement on the seam itself.
