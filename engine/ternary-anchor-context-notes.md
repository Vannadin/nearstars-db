# A ternary anchor from a diffusion table? (C12) — context notes

**Opened by the owner on 2026-08-31**, on grounds the owner found: the report that
Bethkenhagen+ 2017's published version carried no usable data had been made from the text
layer twice; the owner doubted it and read the typeset PDF as images, and Table 1 carries
state points. **A check, not a material.** Closed the same day on the conservative branch:
the table's density column cannot be read as the ternary's density from the text, and the
check designed to confirm the reading turned out to rest on a false premise.

## Provenance

Bethkenhagen, M., Meyer, E. R., Hamel, S., Nettelmann, N., French, M., Scheibe, L., Ticknor,
C., Collins, L. A., Kress, J. D., Fortney, J. J. & Redmer, R. 2017, *Planetary Ices and the
Linear Mixing Approximation*, ApJ 848, 67
([`2017ApJ...848...67B`](https://ui.adsabs.harvard.edu/abs/2017ApJ...848...67B), doi
[10.3847/1538-4357/aa8b14](https://doi.org/10.3847/1538-4357/aa8b14)) — the typeset ApJ
version, `docs/phase3/_papers/2017ApJ...848...67B.pdf`, nine pages, first page checked
("The Astrophysical Journal, 848:67 (9pp), 2017 October 10"). Everything quoted below is from
this PDF (text layer, with page 7 rendered for Table 1), not from the ar5iv text.

**The EOS grid is genuinely absent from the typeset version too**: the methane and mixture
equations of state appear only as Figures 1–3; no numeric table, no data-availability
statement, no supplement. **C4's methane half does not move; its route is still an author
request.** This item is not a reopening of C4 in any branch.

## What Table 1 is (p. 7)

Caption: *"Self-diffusion Coefficients of the Real Ternary Mixture along the Considered
Planetary Profiles."* Columns R (R_U) · ρ (g cm⁻³) · T (K) · p (GPa) · D_H · D_C · D_N · D_O,
in three blocks: *Icy Planetary Profile* (9 rows, 4.3–558 GPa, 1500–3850 K), *Water-only
Planetary Profile* (11 rows, 6.9–510 GPa, 1775–5750 K), *TBL Planetary Profile* (10 rows,
4.8–559 GPa, 1500–14 000 K). Thirty rows.

## The question, settled from the text first

**What is ρ?** Two readings were registered: (가) the simulated 2:1:4 mixture's own density at
that (T, p); (나) the profile model's density at that radius.

The sentences that bear on it, quoted:

- §2.7: *"We simulated mixtures containing 24 methane, 12 ammonia, and 48 water molecules.
  This was performed along three planetary P–T profiles of Uranus (see Section 2.1). …
  Each simulation run was started from a density derived using the EOSs of the pure compounds
  and the LMA. Every 1000 timesteps, the pressure was checked and the volume of the
  simulation box was adapted until the desired pressure was matched up to a deviation of 2%.
  Since this procedure is computationally expensive, especially for low pressures, we
  typically chose two different volumes and interpolated linearly between the results in
  order to match target pressures below 40 GPa."*
- §4, introducing the table: *"Additionally, the diffusion coefficients of each species in
  the real ternary mixture, as well as radius, density, temperature, and pressure along the
  three profiles, are given in Table 1."*

**Reading from the text: (나).** The table sentence lists *"radius, density, temperature, and
pressure along the three profiles"* as one group of profile quantities beside the mixture's
diffusion coefficients; §2.7 describes the simulation matching the profile's *pressure* and
says nothing about tabulating the box's resulting density. The mixture's own density enters
the paper as Figure 4 (its deviation from the LMA along the profiles), not as a column. This
reading is what the text supports; it is not stated in so many words, so it is recorded as
the text's reading, not a certainty.

## The discriminating check — run after the reading, and what it actually showed

As registered: evaluate this recipe's water at a water-only-profile row; (나) was to land on
the printed ρ, (가) about 4 % above it. Run at every row, with the material the recipe would
use (all thirty are on Mazevet+ 2019's hot-water fit, `h2o_hot`; none refused):

| profile | rows | ρ_water / ρ_printed − 1 |
|---|---|---|
| water-only | 6.9 GPa · 1775 K … 510 GPa · 5750 K | **+29.2 % → +18.4 %**, monotone in p |
| icy | 4.3 GPa · 1500 K … 558 GPa · 3850 K | +32.2 % → +19.2 % |
| TBL | 4.8 GPa · 1500 K … 559 GPa · 14 000 K | +32.1 % → +15.8 % (the R = 0.785 pair at 13 GPa, 2175 and 6875 K: printed 1.20 → 0.91, ours 1.515 → 1.168 — the same ratio, 0.76 vs 0.77) |

**Neither registered prediction holds.** Our water is 18–29 % above the printed ρ on the
*water-only* profile — so the printed column is not pure water's density at that (p, T)
(Mazevet's fit reproduces the French+ 2009 QMD water the Redmer+ 2011 model was built on to
a few percent, not to 20–30 %). Two explanations remain, and **both fit the size**:

- under (나), the water-only model's inner envelope is not pure water but ices with H/He
  admixed (three-layer Uranus models carry a heavy-element fraction below 1 in the inner
  envelope); 10–15 % H/He by mass at these pressures lowers the density by about that much
  — *not verified here*, because Redmer+ 2011 / Nettelmann+ 2013 were not read for this;
- under (가), the 2:1:4 mixture is lighter than water by more than the 4 % the
  mean-molecular-weight argument gave — this repository's own C4 check found ammonia 21–24 %
  less dense than water at equal (p, T), and methane is lighter still, so a mixture 15–25 %
  lighter than water is plausible; the smooth decrease of the offset with pressure across
  all three profiles is what a fixed mixture's compressibility would do.

The check therefore **cannot discriminate** — its (나) prediction assumed the profile's
material was pure water, and that assumption was the thing it disproved. What it does
establish: **the printed ρ is not pure water's density anywhere in the table**, and the
"4 % heavier" figure registered for (가) was a floor (C4's ammonia result already said so).

## Verdict — the conservative branch

The text supports (나); the check could not confirm it, and under (나) the column is a model
profile's density, not a mixture's. Under either reading **no ternary anchor can be read
from this column with the evidence held** — under (나) it is not the mixture, under (가) the
text does not say so. So the registered *"ambiguous in the text"* branch is taken: **C12
closes as recorded — Table 1 does not give a mixture density this recipe can anchor on**, and
C4's composition tier keeps its water + ammonia number (2.9–3.5 %) as the only measured
piece.

**What would settle it**, named: (i) the Redmer+ 2011 water-only Uranus profile's own ρ(R)
(their Table or figure) — if it prints the same 1.00 g cm⁻³ at R = 0.839 R_U and 6.9 GPa,
Table 1's ρ is the profile's, (나) is settled, and the column carries the model's H/He
admixture; (ii) failing that, Bethkenhagen+ 2017's Figure 4 read for the mixture's density
deviation from the LMA, which would let the mixture density be reconstructed from the pure
EOSs — but the pure methane EOS is the thing C4 lacks, so (ii) does not close; (iii) the
authors.

## What did not move

No code, no anchor, no test (a check whose meaning is unsettled does not enter the gate).
C4 untouched; the 2017 citation's base moved from the ar5iv text to the typeset PDF.
