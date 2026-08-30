<!-- 내부구조 솔버를 "끝났다" 고 말하려면 남은 것 — 코어 작업 목록 -->
# Interior solver — the core list

What remains before the interior solver can be called finished. Not a wish list: every
entry here is something **this recipe can close by itself**, and closing all of them is the
definition of done for this tool.

The information was scattered across the methodology document's domain table, six sets of
context notes, and a review file that is now half stale. Asking "what is left" meant
re-reading all three and getting a slightly different answer each time. This is the one
place.

**Order, set by the owner 2026-08-29: C1 first, then down the list in number.** No entry
depends on another, so the numbers are a queue rather than a chain; an entry that closes as
*"recorded, not found"* still closes.

**Keeping this file alive.** C2 was stale within a day of being written. So each brief's
Landing section carries one checkbox — *update the matching row in `interior-core.md`* — and
a row is not closed by the work being done but by that line being written here.

**Prose that carries a number carries the duty to update it.** Notes, domain rows, tables —
wherever a number sits, when the code moves that number the same commit either fixes it or
dates it *interim, superseded <date>*. Three times a note fell behind the code (C2 within a
day; the domain row that stated Neptune's "1797 K, three kelvin under the floor" as fact; the
H/He note's Saturn +2.09 % after the gas-layer temperature carry moved it to +7.06 %), and
the rule above only covered core rows.

**Labels are re-checked at their place in the text, not only the constants.** When a
transcription is verified against a source, the equation number itself is confirmed to sit
where the text puts it. Constants that are right hide a wrong label, and the next reader who
follows the label opens the wrong equation — the same failure as a fabricated DOI that
resolves to a real, unrelated paper: the form is plausible, so it passes. (C8 wrote Noack &
Lasbleis's R_p scaling as their eq. (8); it is their eq. (5), and (8) is X_CMF. The constants
were right, eight labels were not.) **And when one file carries two papers, the same number
can exist twice, so a label is written with the paper's name** — `Noack & Lasbleis eq. 5`,
never a bare `eq. 8` — which is how `test_interior.py` came to hold Unterborn's real eq. 8
beside a mislabelled Noack & Lasbleis eq. 8 without either looking wrong. That is the fourth
kind of plausible-because-well-formed failure this list has met, after the fabricated
identifier, the stale number and the label slip: the same number from a different paper.

**When a source is baked, its claimed range is swept against physical criteria registered
in advance, and the effective ceiling is measured and recorded with the table.** A label can
be verified faithfully at its place in the source and the source's own claim can still
break in execution — the fifth kind of plausible-because-well-formed failure. SeaFreeze's
`water2` (water2 item, 2026-08-30) carries knots to 100 GPa and AQUA quotes that as its
range, and the spline returns negative densities inside it; the effective ceiling (2.3 GPa
at 360 K rising to 30 GPa at 1000 K) was found by a sweep whose criteria — ρ finite and
rising with P, 1000 < c_P < 15 000 J/kg/K, dT/dP|_S > 0, no runaway in successive density
increments, two cells of margin — were fixed *before* the sweep, so the ceiling could not
drift to wherever the results looked odd. **Pre-registration is the point**: without it,
"as far as it looks fine" is an impression, not a verdict. `fermi.py`, `hhe_table.py` and
`ammonia_table.py` already meet this in their own ways; it is stated here so the next baked
table does too.

**Relays without verification, in both directions.** *Downward*: a number without its label
does not enter a brief. *Upward*: **a number that changes a verdict is reproduced by the
directing session before it goes to the audit.** Verdict-changing, specified in advance so
it is not judged by impression: (a) a number that opens, closes or reopens a row; (b) **a
first claim that a published value is contained or reproduced**; (c) a number that moves an
anchor; (d) a number that changes a grade. The directing session's reproduction does **not**
replace the audit's: a verdict-changing number is computed by the working session,
reproduced by the directing session, and reproduced again by the audit. The five failures
that produced these two sentences are one disease in two directions — four unlabelled
numbers travelling down into briefs, and one headline (C11's "Titan is inside a declared
band", 2026-08-30) travelling up without reproduction; the rule above stops the first and
this one the second.

**A table is regenerated on the code that ships, in the commit that ships it — and when the
regeneration differs, which side is right is settled by a separate trace.** The sub-kind's
name ("the table ran ahead of the code inside one commit") invites doubting the table first;
in the case that named it (C11, 2026-08-30) the table was right and the code had regressed —
an over-broad refusal written after the table removed a converged member. Regenerate, diff,
then trace; do not correct the table to the code, or the code to the table, on the name alone.

## Where the line is

Not by body class — by **what is missing**.

**In:** the missing thing is a material, a structure, a declaration, or a wire. The recipe
can reach it.

**Out:** the missing thing is physics the hydrostatic integration does not contain, or a
node that already exists elsewhere.

| out of scope | why |
|---|---|
| brown dwarf | deuterium burning above ~13 M_J puts an energy source inside the body. Not an input this recipe lacks — a term the equations do not have |
| star | the stellar C/MR² is the n = 3/2 polytrope value 0.205 (Chandrasekhar 1939), already on a separate `body_figure` branch |
| evolution and cooling tracks | age-dependent envelope thickness and luminosity belong to `internal_heat_nontidal` and to nodes not yet written |
| gate economics | the gate ran 14:12 → 14:22 → 17:44 and the cost was twice *recorded, not repaid*. Not solver physics — but it belongs on **a maintenance list of its own**, written down here only so it cannot fall between the two. Two small fixes ride with it: the conditional `_LAST_INVERSE` line, and a double-cut test for a thin layer |

**Sub-Neptunes are in.** What they lack is a gas mass fraction, which age and irradiation
set — an *input*, not physics. This recipe already takes six such inputs by declaration and
drops its grade for each: `ice_allowed`, `tidal_heating`, `initial_porosity`, `envelope_z`,
`potential_temperature`, `core_cmb_temperature`. A seventh is the same move, not a new
standard.

## The list

### C1 — Sub-Neptunes, and the defect hiding behind them — **closed 2026-08-30**

The sweep (5 M⊕ · CMF 0.20 · 500 K at 1 bar) now solves at 2, 5, 10, 20 and 30 % gas and
declines at 50, 80 and 100 % citing the hottest bound solution and the wall above it —
neither sentence mentions a ceiling. `sub_neptune` is off `FLUID_CLASSES`; `gas_mass_fraction`
is the seventh declaration. GJ 1214 b (8.41 M⊕, 2.733 R⊕) is reproduced by 1.5–2.4 % H/He for
1-bar temperatures of 350–250 K, inside Valencia+ 2013's < 7 % and beside their ~3 % for a
solar-metallicity envelope.

Both measurements were wrong: the 17.7 M⊕ row was the polytrope era's, the "0 M⊕ since the
table" of 2026-08-28 was the same defect as the sweep's refusal (the envelope base cut off as a
surface), and the cap re-measured with the defect fixed was 11.46 M⊕ (interim, superseded
2026-08-30 F2: 16.69 M⊕ once the bulk-modulus finite difference stopped poking past the
silicate ceiling on the shooting's ceiling trial). Under it were three defects, none a ceiling: the
integrator took the envelope base leaving the H/He table's reach line for the 1-bar surface,
so the envelope had no mass; the temperature loop's proportional update diverges when the
1-bar temperature scales faster than the central one (thin envelopes on heavy cores); and a
ladder seed already over the target fell onto the inflated branch of the U-shaped surface-mass
curve. Each fix is gated so that no anchor path enters it, and the bit lines say so.
`engine/sub-neptune-context-notes.md` has the measurements.

Left open, named: a sub-Neptune now integrates but has **no dynamo path** — `core_state`
declines by class, `dynamo_giant` excludes it by mass, `dynamo_rocky` does not take the class.
Recorded as a gap edge in `chain.yaml` (`body_class → dynamo_rocky, via: sub_neptune`); not a
solver item, so it is not on this list.

### C2 — The ocean layer, and multi-axis inversion — **closed 2026-08-29**

Liquid water came from SeaFreeze's `water1`, the phase switch is pinned inside the
integration step the same way layer boundaries are, and `infer_three_layer` returns a band
over the core axis, narrowing only when a measured C/MR² is supplied. Grid phase 2e-3 → 8e-7,
asserted at the gate. Condensed anchors bit-identical; `chain.yaml` cycle 7 declares the
phase → density → temperature loop.

Two of the five icy anchors came inside — Ganymede 2.1 % → 0.4 %, Europa narrowed to a 7 %
core under a 104 km ocean. **The other three moved the question rather than answering it,
which is C10.**

Reasoning: `engine/ocean-layer-context-notes.md`.

### C3 — The melting-curve gap, and dispatch by class — **closed 2026-08-30**

The ice material is now chosen by the local (P, T) against two published lines, never by
`body_class`: IAPWS's melting curve to 20.6 GPa, then Reinhardt+ 2022's liquid–solid line
(to 52.4 GPa) and its ice VII′–VII″ line (to 70 GPa), baked from the paper's public data by
`tools/make_ice_melt_table.py`. Below the VII′–VII″ line the column is the condensed ladder;
above it, VII″ and the liquid alike go to Mazevet's fit, whose floor is now the paper's own
1000 K rather than the ladder's 1800 K ceiling. Every result names the phase at both ends of
the column and the line it was measured against. Neptune's envelope base at convergence is
39 GPa · 2 555 K, 999 K above the liquid line — fluid for a stated reason. The seam at
20.6 GPa is +26 % in melting temperature, measured and stated; the grade is analog because
the lines are simulation.

Two things came out from under it. The "1797 K, three kelvin under the floor" was a trial
path, not the converged point; and Neptune's old convergence was luck — the 1-bar
temperature was jagged in the central temperature by ±0.4 K because the closing
extrapolation read its adiabatic gradient at a grid-bound step start. The gradient is now read
at the exit point and the temperature loop keeps its best pass; Uranus moved +3.8 × 10⁻⁵ in
radius, Neptune −2.8 × 10⁻⁴ (6 308 → 6 296 K at the centre), both reported in
`engine/melting-curve-context-notes.md`. Above 70 GPa no line reaches and none is invented:
the verdict says "fluid or superionic" with Millot+ 2018's one point.

**The seam is itself under review.** Kimura 2023
([`2023JChPh.158m4504K`](https://ui.adsabs.harvard.edu/abs/2023JChPh.158m4504K), *Revisiting
the melting curve of H₂O by Brillouin spectroscopy to 54 GPa* — a measurement across the whole
Reinhardt range, on the owner's paper-request list; bibcode checked by title, this session and
the audit session) becomes the arbiter of the disputed band when it arrives: its product is
not only a possible grade upgrade but a **re-verdict of the band (16.5–20.6 GPa / 715–902 K)
and a possible narrowing of the seam's width.**

**Revisited 2026-08-30 (F1), with the criterion fixed before the comparison.** Kimura &
Murakami measure melting only from 25.9 to 53.6 GPa (their lower rows are liquid runs at a
temperature *estimated from Queyroux's curve*). Against Reinhardt's line, six of their seven
melting points sit inside their own stated ±130–150 K, and the one outside (25.9 GPa) is the
measurement *hotter* than the simulation by 171 K — away from IAPWS, not toward it. At the
seam their Simon–Glatzel fit (eq. (2), anchored on Queyroux's 14.6 GPa · 850 K triple point)
gives 1028 K (968–1155 at 1σ): +14 % above Reinhardt and +44 % above IAPWS's 715 K.
**Kimura sits with Reinhardt; the step is not an artefact of the simulation.** C3 stays
closed, the seam number stands, the dispatch is unchanged, and the grade stays analog
because the check's own error is 8–11 % and it does not reach the seam. The band is not
narrowed: the measurement gives no support to IAPWS's end. Table I enters the gate as a check
table. What would still move this is a measured point between 15 and 26 GPa — Queyroux+ 2020,
now in the cache. `engine/seam-retrial-context-notes.md` has the tables.

**Revisited 2026-08-30 (water2): the open defect this row named is filled, not overturned.**
The band with no equation of state — liquid water above the ocean table's 2.3 GPa (or above
its 500 K) and below the hot-water fit's 1000 K floor, the one F2's Callisto and Titan at
f = 0.75 walked into — is now carried by SeaFreeze `water2` (Brown 2018,
2018FlPEq.463...18B; range as AQUA §2.3.5 states it, *"liquid and supercritical H₂O from
1 GPa to 100 GPa and up to 10⁴ K"*), baked ragged to the spline's **real** ceiling, which is
not its knot box: SeaFreeze's `water2` returns negative densities inside 100 GPa — valid to
2.3 GPa at 360 K, 10 GPa at 600 K, 13 GPa at 700 K, 30 GPa at 1000 K, hugging the liquid
side of this row's melting curve. Two seams measured: water1 ↔ water2 in their overlap ρ
0.13 % / dT/dP|_S 9 %; water2 ↔ Mazevet at 1000 K, Mazevet 2.5–3.3 % less dense over
2.3–26 GPa. Still uncovered by name: 12–20.6 GPa between the melting curve and the ceiling
(≲ 170 K wide), and hot water below 0.1 GPa. `engine/water2-context-notes.md`. C3 stays
closed; the dispatch by (P, T) is unchanged, one more material answers it.

### C4 — Ammonia and methane — **closed 2026-08-30, unbuilt; reopened 2026-08-30 for ammonia and closed again for that half, built**

The ice-giant envelope is water alone, standing in for a water–ammonia–methane mixture. That
is the field's own convention, but it is a stated substitution and **its price is not
quantified** — not bounded, not estimated. Bethkenhagen+ 2017's 2.1 % is the deviation from
*mixing three components you already have*, not the cost of replacing two of them with the
third; `eos.py` states the distinction correctly. The number only comes into existence when
the tables do, and the tables cannot be reached from here. Three routes, checked on
2026-08-27 and again on 2026-08-30:

| route | why it fails |
|---|---|
| Bethkenhagen+ 2017 (2017ApJ...848...67B, full text in the cache) | describes the grid exactly — 1000 GPa · 20 000 K, thirteen isotherms — and publishes no data-availability statement and no URL |
| Bethkenhagen+ 2013 (2013JChPh.138w4504B, doi 10.1063/1.4810883), the ammonia source | AIP paywall; 330 GPa · 500–10 000 K, the set 2017 extended |
| FPEOS, Militzer+ 2021 (2021PhRvE.103a3203M) | distributes tables and code, and carries CH₄ — but **no NH₃**, and its range 10⁴–10⁹ K begins above the ice-giant adiabat (5500–6300 K) |

**An author request is the only remaining route.** Bethkenhagen+ 2013 goes on the owner's
paper-request list; the 2017 tables would come from the same authors.

What can be said about the sign, in three tiers, only the first carrying a number:

- **composition** — direction **+**, it *widens* the residual. The solar-ratio mixture
  (0.31 : 0.08 : 0.61 CH₄ : NH₃ : H₂O by mass, Bethkenhagen+ 2017 §V) has a mean molecular
  weight of 17.28 against water's 18.02, so water overestimates the ice density by 4.27 % at
  equal number density (*derived*); electrons per unit mass agree in direction (H₂O 0.555,
  NH₃ 0.587, CH₄ 0.623 e/amu, *derived*). Correcting it lowers the density and enlarges a
  planet the model already makes too large, on a ~1.5 % radius scale (*derived*).
- **thermal** — mechanism named, **sign ungrounded**. Atoms per unit mass run H₂O 3/18 <
  NH₃ 4/17 < CH₄ 5/16, so the ideal-gas intuition is a higher heat capacity, a shallower
  adiabat, a colder and denser interior (Bethkenhagen+ 2017's icy Uranus is cold, T_core ~
  4000 K), pulling the radius back. Dissociation at high pressure shrinks that difference
  and with it the sign; no direction is defended.
- **net** — needs the tables.

Writing "1.5 % worse" would quote the first tier as the third.

C5 was attributed on 2026-08-30: the ice giants' residual belongs to a thermal boundary
layer at the transition between the ice/rock interior and the H/He envelope and to the
inner mantle's ice:rock ratio (Nettelmann+ 2016), with non-adiabatic interiors the review's
own open question (Helled+ 2020). **C4 is not a candidate for that residual in either
direction**, so closing it unbuilt costs the recipe nothing it was counting on.
`engine/ammonia-methane-context-notes.md` has the search.

**Reopened 2026-08-30 for the ammonia half** — the registered overturn condition fired: the
owner obtained Bethkenhagen, French & Redmer 2013 and **the table is printed inside it**
(Appendix B, Table I; no repository, no fit — the printed table is the distribution). The
closure above assumed it was out of reach; it was not. The methane half stays closed as
written — nothing new bears on it.

**Closed again for ammonia, built.** `engine/ammonia_table.py`, baked by
`tools/make_ammonia_table.py` from the cached PDF's text layer and checked against the
printed page: 93 points on a **ragged** grid (500 K to 1.5 g/cm³, 700 K to 2.0, 1000 K and
above to 3.0; 0.309–333.2 GPa), the five asterisked points carried as a 5 % flag against the
paper's 2 %, nothing interpolated across the six absent cells. The material `nh3`
(`eos.Ammonia`) refuses outside the table by name. **The convention is stated and tested**:
the caloric column includes the vibrational correction (2013 Appendix B) — the correction
Bethkenhagen+ 2017 §II.4 removed from this set — and the exposure is c_P / ∇_ad only, never
the density mixing. The ice-giant adiabat (5500–6300 K) lies between the 5000 and 7000 K
isotherms: **interpolation, not extrapolation.** Interpolation error, leave-one-out at
doubled spacing: 8.7 % in the mantle region (ρ ≥ 1 g/cm³, T ≥ 2000 K), 17.3 % in the low-density dissociation corner.

**What the table settles, and only that.** Water (Mazevet+ 2019) and ammonia (this table)
read at the same (P, T) at eight points — four on the engine's own solved Uranus profile
(50–250 GPa, 2830–3950 K) and four bracketing the central temperatures — mixed by additive
volume at the solar-ratio pair fraction w_NH₃ = 0.1159: ammonia is 21–24 % less dense than water at
equal (P, T) — the equal-number-density μ argument (5.5 %) was a floor — and **water
standing in for the water–ammonia pair overestimates its density by 2.9–3.5 %**, direction
+, above the propagated noise (0.6 %). That is the composition tier's number for the
**ammonia share**; the tier's direction stands. The thermal tier gets a first table-derived
indication that is **not uniform**: ammonia's ∇_ad is 19–45 % below water's at seven points
(the pair's adiabat 3–10 % shallower) and above it at the mantle top (50 GPa, 2830 K: 2.6 %
steeper), under the convention caveat — so it **keeps "sign ungrounded"**. The net tier still needs the tables,
**because methane — the largest share, 0.31 — is still missing.** Ammonia is not wired
into any body; whether it enters the mantle as a declared fraction is the owner's decision,
with the grounds (for, against, and the ceiling below the ice giants' centres) in
`engine/ammonia-table-context-notes.md`. Anchors bit-identical — no path function moved.

**The methane half, re-stated from the full text (2026-08-30, not built).** Sherman, Wilson,
Weeraratne & Militzer 2012, *Ab initio simulations of hot, dense methane during shock
experiments*, Phys. Rev. B 86, 224113 (2012PhRvB..86v4113S, arXiv 1207.2948) is in the
cache as the published PDF and the arXiv LaTeX source. **A table exists and is distributed**:
the source's appendix carries 79 DFT-MD (T, P, E) points with 1σ error bars, marked *"to be
published as online supplementary information"* — the published PDF refers to the
supplement and does not print it. The row's old reason, *not obtained because paywalled*, is
replaced by two that hold with the table in hand:

- **Methane does not persist as a species in the region.** Sherman: *"At a temperature of
  approximately 4000–5000 K, a plateau is reached … the system entering into a polymeric
  regime where the methane molecules spontaneously dissociate to form long hydrocarbon
  chains"*, a regime they show to be metallic; at 6000 K a plasma. Bethkenhagen+ 2017 §III on
  their own runs: *"Pure methane does not become superionic but instead decomposes into
  long-chained molecules in our simulations."* Additive volume assumes each component keeps
  its identity at (P, T); **no mixing error for a dissociating component has been measured
  or published**, so a methane table would not make a linear-mixing mantle grounded.
- **The grid does not cover the region.** Counted from the source (13 densities × 13
  temperatures, 79 cells filled): the low densities stop at 4000 K, only two density lines
  (1.201 and 1.498 g/cm³) run the full 300–75 000 K, and single points sit at 0.600, 1.353,
  2.129 and 2.376 g/cm³. Bethkenhagen+ 2017 §II.3, naming Sherman: *"none of them covers the
  entire pressure-temperature region required for Uranus and Neptune interior models."*

| ρ (g/cm³) | 0.600 | 0.800 | 1.000 | 1.201 | 1.353 | 1.498 | 1.600 | 1.775 | 2.010 | 2.129 | 2.257 | 2.376 | 2.502 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| points | 1 | 5 | 5 | 13 | 1 | 13 | 9 | 9 | 9 | 1 | 6 | 1 | 6 |
| T (K) | 300 | 300–4000 | 300–4000 | 300–75 000 | 2000 | 300–75 000 | 2000–75 000 | 2000–75 000 | 2000–75 000 | 10 000 | 5000–75 000 | 10 000 | 5000–75 000 |

**Measured: the solved mantles do pass the published dissociation thresholds.**
`tools/methane_thresholds.py` reads the frozen convergence point and samples the ice layer:

| | Uranus | Neptune |
|---|---|---|
| ice mantle span | 34.5–820 GPa, 2663–5948 K | 39.2–1016 GPa, 2553–6066 K |
| C–C bonds (> 1100 K and > 10 GPa, Hirai+ via Sherman) | the whole mantle, from its top | the whole mantle, from its top |
| diamond (> 3000 K) | from 80 GPa (3037 K) to the base — 71 of 78 samples | from 114 GPa (3049 K) — 67 of 76 |
| polymeric 4000 K / 5000 K | 262 GPa / 525 GPa | 334 GPa / 626 GPa |

So in this recipe's own profiles the entire ice mantle sits above the carbon–carbon bond
threshold, nine tenths of its pressure span above the diamond threshold, and its deeper
half inside or beyond the polymeric regime. That is a measurement, recorded here as grounds
either way; whether carbon separation becomes an item (carbon as its own phase rather than
methane in a mixture) is the owner's decision. **The three-tier sign statement does not
move**: methane's absence is now more precisely stated, and the net still needs tables that
would have to carry a dissociating component — which none published does.

### C5 — Where the giants' leftovers belong — **closed 2026-08-30**

Two residuals; both now have an owner, and one has two declarations it can be read against.

**Jupiter, and the diluted core — reached, no consumer.** The mixture rule carries one
homogeneous Z through the envelope. Post-Juno structure is not "graded inward": Debras &
Chabrier 2019 §4.1 (2019ApJ...872..100D, text in the cache) is titled *Inward decreasing
abundance of heavy elements in some part of the outer envelope* — locally ∇Z > 0 — and the
structure needs four regions: an outer convective envelope, a composition-and-entropy
gradient, an inner convective envelope and an extended dilute core. Two transcribable forms
exist: Helled & Stevenson 2017's closed Z(m) (2017ApJ...840L...4H) and Howard, Guillot &
Bazot 2023's Juno-constrained models (2023A&A...672A..33H). Not implemented: Alpha Centauri
A b's radius is a declaration, so nothing in the roster would read a graded-Z envelope
today. The earlier compact-core attempt and its silicate ceiling stay in the domain row.

**The ice giants — the residual has an owner, and the question was wrong.** Helled,
Nettelmann & Guillot 2020 (2020SSRv..216...38H, text in the cache): "even a very small (in
mass) H-He atmosphere can imply high interior temperatures, if an adiabatic temperature
profile is assumed" — the +8 % / +14.7 % central-temperature excess is the signature of an
adiabatic H/He envelope, not a missing material, and whether layer transitions are sharp or
gradual is open (their Fig. 4). Nettelmann, Wang & Fortney 2016 (2016Icar..275..107N, text
in the cache) put the mechanism at the **boundary**: a stably stratified thermal boundary
layer at the H/He–ice/rock transition near 0.1 Mbar (their Table 1), whose class II and III
models "yield by a factor of up to about 2 to 3 warmer core temperatures than the class I
models. As a result, the presence of rocks is required in the inner mantle in order to
match the gravity data" (§7); their U15-II has ΔT = 2500 K and U15-III 4700 K (Fig. 9),
≈ 5000 K (≈ 9000 K) higher central temperatures (§6), and their favoured models carry 1× solar
I:R with "the mixing behavior of rocks with … ices … not well-understood". Their negative
result is narrower than it was quoted: the I:R ratio "does not provide a solution to the
**low luminosity**" (§3) — a cooling-time statement, not a gravity-fit one. C4 is not a
candidate for this residual either way.

**Two declarations, integrated without tuning.** `boundary_temperature_jump` (the TBL step at
this recipe's mantle/envelope boundary, 30–40 GPa for the anchors) and
`mantle_rock_fraction` (silicate mixed into the water phases above 2.3 GPa). Published values
for the first (2500 K, 4700 K); no published mass fraction for the second, so a declared grid:

| declaration | Uranus ΔR (T_c) | Neptune ΔR (T_c) |
|---|---|---|
| none (anchor) | +5.48 % (6 160 K) | +8.94 % (6 296 K) |
| ΔT 2500 K | +7.99 % (11 493 K) | +11.50 % (11 886 K) |
| ΔT 4700 K | +10.04 % (15 661 K) | +13.58 % (16 241 K) |
| rock 0.10 | +3.64 % (6 275 K) | +7.02 % (6 401 K) |
| rock 0.20 | +1.83 % (6 369 K) | +5.13 % (6 486 K) |
| ΔT 2500 K + rock 0.10 | +5.61 % (11 630 K) | +9.00 % (11 994 K) |
| ΔT 2500 K + rock 0.20 | +3.26 % (11 718 K) | +6.56 % (12 053 K) |

Read, not fitted: the boundary layer **widens** the radius residual (+2.5 %p per 2500 K) and
raises the centre by ≈ 5 300 K per 2500 K — the same ≈ 5 000 K Nettelmann report for class II;
rock **narrows** it by ≈ 1.8 %p per 0.10. Neither published value closes either planet on its
own; the two together are the chain the paper describes (warmer → less dense → rock), and the
rock fraction that would close it is not a number this recipe has a source for, so it is not
declared. Anchors keep both at 0 and are bit-identical. `engine/giant-residual-context-notes.md`
has the runs and the provenance of every number.

### C6 — Material ceilings

Each material stops where its evidence stops, and each ceiling is a row that declines by
name. They are listed together because they are one kind of work.

| material | ceiling | what is above it |
|---|---|---|
| `h2o` | 1 TPa · 1800 K | ice X above the knot domain; superionic above the temperature |
| `silicate` | 13.5 TPa | Thomas–Fermi–Dirac (electron degeneracy) |
| `fe_prem` · `fe_eps` | 12 · 20.9 TPa | the same |
| `h_he` | 10⁴ GPa in the giant branch | the table's own edge |

Needs: nothing, unless a body the roster wants is refused by one of them. **Each is a
correctly stated limit, not a defect** — the work here is to keep them honest, not to remove
them. Listed so that a future refusal can be traced to its row rather than re-diagnosed.

Depends on: a body that actually hits one.

### C7 — Partial differentiation — **closed 2026-08-30: the intermediate state is not a mixture**

`differentiated: false` integrates rock and metal mixed in one layer and declines when ice
or gas is present. The refusal stays; its reason is raised. It used to say the mixture rule
handles rock and metal only — true of the code, and an invitation to go looking for the
missing rule. Searched 2026-08-30 (additive-volume / ideal / linear mixing for rock + ice,
interior models of undifferentiated icy bodies): **no mixing rule for an ice-bearing layer
exists, and no published bound on the error of using one.** Two reasons, and they are the
content of this closure.

**It is a reaction, not a mixture.** Water and silicate combine into hydrated minerals with
their own density, volume change and heat; that is why hydrated-rock density in the
literature comes from Gibbs-energy minimisation over a mineral database rather than from
mixing two end-member densities. C10 hit the same wall from the other side — no closed-form
hydrated-rock EOS and no ice–rock mixing rule are two faces of one fact.

**It is a process, not a state.** What makes a body neither fully mixed nor fully layered is
how far the water got. Malamud & Prialnik 2015 (2015Icar..246...21M) start from a
homogeneous ice–rock body and follow the multiphase flow of water through porous rock, the
differentiation that results and the aqueous alteration of the rock, with the density profile
from hydrostatic equilibrium maintained through changing composition, pressure and
temperature; Malamud & Prialnik 2013 (2013Icar..225..763M) treat serpentinisation
explicitly, exothermy included; Prialnik & Merk 2008 (2008Icar..197..211P) is the porous
icy-body evolution code both stand on. **Provenance, plainly: all three are Elsevier, no
preprint, and only the abstracts were read.** This closure can say a treatment exists and
what kind it is; it cannot say whether it is transcribable. Malamud & Prialnik 2015 goes on
the owner's paper-request list serving **C7 and C9 at once** — its heat sources include
compaction's gravitational potential energy and serpentinisation, two of the five
exclusions C9 is about.

**This does not touch C10.** C7 forbids mixing water *into* silicate — a reaction. C10 mixes
antigorite with enstatite/PREM: two solids coexisting as grains, each with its own measured
equation of state, which is what a partially serpentinised rock physically is. Volume
additivity between them is standard and is the same shape as the rock–metal rule this
recipe already carries, so C10's interpolation is one declared axis — how serpentinised —
and not the forbidden mixture.

**Revisited 2026-08-30 (F3), from the full text now in the cache.** The stated limit is
removed in the transcribable direction: the paper's EOS (§3.3, eqs. (1)–(7)) is an
**equilibrium closed form in (P, T, X_d) with every coefficient printed** — porosity of ice
ψ_w = 0.45 exp(−β_w(T/T_m)√P) and of rock ψ_d = 0.4 exp(−β_d P) Γ(T_max), volumes added by
the two-layer model — and its only history variable is T_max, one number per shell. It fits
laboratory compaction to 764 MPa, ice I only, no rock melt; at Callisto's and Titan's core
pressures it is out of range and gives ~1 % void, so **it does not reach the deciding region
of C10's three moons; it reaches their crusts.** Both reasons above are confirmed from the
text: serpentinisation is a reaction *"only so long as there is available liquid water"*, and
the front is an output of a 4.6 Gyr multiphase-flow run with no input parameter for how far
melting reached. **One sentence above was too broad and is corrected here in words:** a
mixing rule for an ice-bearing layer *does* exist for the never-wet state — cold ice and rock
grains, each compacted on its own curve, volumes additive (Yasui & Arakawa 2009's two-layer
model, adopted as eq. (1) and reported to reproduce the mixture's compaction curve) — which is
C10's shape; what still has no rule is the reacted, partially differentiated body, and the
refusal stays on that. "No consumer" is therefore a **choice** about the missing front, not an
absence of a treatment. The full text names the declared-front shortcut (*"assuming that
differentiation somehow occurred, without actually computing how"*) and does not take it;
grounds for a middle rung — a declared front plus a cold mixed crust, Callisto and Titan as
consumers — are written as a proposal, not an item, in
`engine/malamud-readthrough-context-notes.md`. C7 stays closed.

### C8 — The temperature branch's validated window — **closed 2026-08-30**

The adiabat had one published check, Unterborn+ 2019 eq. 7 — 4.4 % at 1 R⊕, −17 % at
1.46 R⊕ — and one anchor is a coincidence with an error bar. The second is Noack & Lasbleis
2020 (2020A&A...638A.129N, PDF in the cache): their eq. (22) carries the mantle adiabat to the
CMB with every term printed, valid 0.8–2 M⊕ for Earth-like composition, and all constants
were re-read from the PDF. Their eqs. (20)–(21) are initial post-magma-ocean temperatures and
were not used. Engine against both, Earth-like CMF 0.325 at 1600 K
(`test_interior.py --adiabat`, and the section *Temperature, checked against a published
core-mantle boundary* carries the full table):

| M (M⊕) | R (R⊕) | engine | vs eq. (22) | vs eq. 7 | anchors vs each other |
|---|---|---|---|---|---|
| 0.8 | 0.942 | 2430 K | −2.2 % | −2.9 % | +0.7 % |
| 1.0 | 1.003 | 2526 K | −1.4 % | −4.4 % | +3.1 % |
| 1.5 | 1.123 | 2724 K | −0.7 % | −7.2 % | +7.1 % |
| 2.0 | 1.216 | 2884 K | −0.8 % | −9.5 % | +9.6 % |

The Earth point reproduces the 2562 K an independent reading reported (2563 K) — the
transcription check. So the grade above 1.05 R⊕ rests on a measured spread: the engine is
within 2.2 % of one published estimate and within 9.5 % of the other, and **the two published
estimates disagree with each other by up to 9.7 %**, with the engine between them. The
agreement in absolute temperature is partly two differences cancelling (the paper's 2000 K at
250 km against the engine's 1736 K there; the engine's rise to the CMB 12–14 % steeper than
the paper's damped exponent), and the test pins both. **2 M⊕ (1.22 R⊕) is the paper's own
ceiling**; above it the recipe is back to one anchor, to Unterborn's 1.5 R⊕. Anchors
bit-identical: this added a comparison, not a change to the adiabat.
`engine/adiabat-window-context-notes.md` has the transcription and the runs.

### C9 — Porosity on a heated body — **closed 2026-08-30: a relation exists, and it depends on rheology**

**This row's own prediction was wrong, and is corrected here rather than quietly.** It said
*"this one may close as 'the bound is the answer', which is a legitimate ending."* The
2026-08-30 survey found otherwise, and a row that carries a guess carries the duty to correct
it — left standing, it tells the next reader to skip the search.

The compaction relation (Bierson+ 2019) returns an upper bound on void space, never an
estimate, because melt, differentiation, convection, impacts and tidal heating all remove
porosity and its §2.2 excludes all five. **Three of the five are carried, with
coefficients, by Neumann & Kruse 2019** (2019ApJ...882...47N, open access, full text fetched
through the ADS gateway into the cache and read): Enceladus heated by radionuclides and tidal
dissipation, differentiating through a melting front, its core compacted by creep — their
§2.5, "compaction is a change of the density and volume of a porous material that is being
heated and applied pressure to … facilitated by creep processes on a geologic timescale" —
with the olivine creep laws of Mei & Kohlstedt 2000 and the antigorite law of Amiguet+ 2012,
coefficients for dry olivine (A1–A4), wet olivine (B1–B4) and antigorite (C1–C2) in their
Table 3. Results: core radius 185–205 km, **porous core layer 4–70 km**, ocean ≈10–27 km, ice
shell ≈30–40 km. Convection and impacts: ✗ — still carried by nobody, and said so.

**How it closes.** Not "the bound is the answer" and not "the bound is replaced":

- Bierson's bound stays the **general case**, validated over 123–2326 km diameter; Neumann is
  one body at one size (252 km) and cannot replace a general bound.
- Neumann & Kruse enter as the **branch** for a tidally heated, differentiating body, grade
  analog — **reached and specified, not wired.** The relation is a creep law integrated over
  a thermal history (porosity as a function of time, stress, grain size, water and
  temperature), and this recipe integrates hydrostatics, not time. Wiring it means a thermal
  evolution the recipe does not have; the specification (which creep laws, which table) is
  written so that whoever brings the history finds the branch ready. Consumers, when it is
  wired: the icy anchors that are heated and differentiating — Enceladus first (the paper's
  own body; on the icy roster, solved today with no porosity declared), Europa, and the roster's
  tidally heated moons that declare `tidal_heating`.
- **The path on the day it is wired:** parse Table 3 from the cached publisher HTML
  (`docs/phase3/_papers/2019ApJ...882...47N.html`, whose `<table>` keeps the columns the text
  extraction flattened) or from the publisher PDF (`PUB_PDF` on ADS), bake the creep
  coefficients the way the other tables are baked, and integrate the creep law over a declared
  thermal history — the history being the thing the recipe does not yet have.
- Malamud & Prialnik 2015 (2015Icar..246...21M, on the request list from C7) serves this item
  too: its abstract carries compaction's gravitational potential energy and serpentinisation
  heat as heat sources — two more of the five.

**The discriminator it hands C10, kept on its own layer.** "No porosity is retained for an
antigorite rheology, implying that the core of Enceladus is not dominated by this mineral."
Vance+ 2018 gave two routes to Enceladus's ~2700 kg/m³ — hydrous rock, or anhydrous rock plus
pores — and density alone cannot tell them apart; retained porosity can, because antigorite
is weak and creep closes its pores. **That is a rheology statement, not a density
statement**: Hilairet's antigorite ρ₀ still stands and still lands on Vance's target. What
Neumann adds is that a body *made* of it would not keep its pores. The two live on different
layers; a later session must not read this as a density refutation.

**Revisited 2026-08-30 (F3), from the full text.** The abstract-derived sentence holds and
gets its weights: serpentinisation heat is the second source after radioactivity (an order of
magnitude below it over the run, twice it in the first 200–235 Myr); compaction's
gravitational energy is *"marginal"*, two orders below serpentinisation. Tidal heating,
impacts and convection are still carried by nobody — satellites are excluded from the
paper's sample for the first two. What the text adds is a **third relation of its own kind**:
rock porosity as a closed form in (P, T_max), eq. (5) with a step Γ centred at 675 K that the
authors call *"hypothetical"*, valid to ~0.8 GPa, ice I, no rock melt. It does not replace
Bierson (general) or Neumann (rheology over a history); but its history is one declared
number per shell, T_max ≥ T, and the present T gives the maximum porosity — a bound. For
this relation "reached, no consumer" is a choice about a declaration, not about a thermal
evolution. Transcription note when it is ever wired: the printed eq. (7) exponent
15(T_max/675) − 1 contradicts the text's stated behaviour; 15(T_max/675 − 1) is the form the
text describes. `engine/malamud-readthrough-context-notes.md`. C9 stays closed.

### C10 — Lighter rock — **closed 2026-08-30: the axis exists, and it does not reach**

Callisto, Titan and Enceladus sit **above** every three-layer band: every member of a band
lowers C/MR² as the core grows, so a published value above the zero-core end cannot be reached
by any layering, and the reason was read as the material — rock lighter than the
enstatite-plus-PREM silicate, hydrated or porous. Set aside on 2026-08-26 for want of a
grounded lighter rock; the evidence arrived and was used.

**The material.** Hilairet, Daniel & Reynard 2006 (2006GeoRL..33.2302H, open access, PDF in
the cache): antigorite compressed to 10 GPa with no amorphisation, transition or hysteresis;
their adopted second-order Birch–Murnaghan **V₀ = 2926.23(50) Å³, K₀ = 67.27(123) GPa,
K₀′ = 4**, confirmed by an F–f plot (§3 [13]). The paper prints no ρ₀; it prints the structural
formula (Mg₂.₆₂Fe₀.₁₆Al₀.₁₅)(Si₁.₉₆Al₀.₀₄)O₅(OH)₃.₅₇ (§2 [6]) and "the V₀ value corresponding to
m = 1 … is 172 Å³" (§4 [15]), and from those **ρ₀ = 273.50 u / 172 Å³ = 2640.5 kg/m³** — derived
here from the PDF, matching two earlier independent readings (2638–2640), and checked twice:
2926.23 / 172 = 17.01 is the m = 17 polysome the paper indexes with (Capitani & Mellini 2004),
and the paper's one printed density, 2765 kg/m³ at 5.7 GPa and 470 °C, comes back as 2841 at
room temperature on this curve — +2.7 %, the size and sign of 450 K of expansion.
**Room temperature only**: the paper measures no thermal term and borrows Holland & Powell
1998 where it needs one; that paper is on the request list, and the grade is set by this
deficiency, not by the fit. `test_interior.py` re-derives ρ₀ and re-runs both checks.

**The axis.** `serpentinisation`, a declared fraction of antigorite in the rock layer, mixed
by additive volume with the silicate — **two solids coexisting as grains**, the rock–metal
rule's own shape and not the reaction C7 declined (water *into* silicate). Where the water
went is history, so it is a declaration and drops the grade. Temperature passes through the
antigorite component the way it passes through any phase without thermal constants.

**Bracketing, and the result.** Antigorite sits under the Vance+ 2018 targets (2641 kg/m³ at
Enceladus's 0.023 GPa, 2742 at Callisto's 2.73, 2761 at Titan's 3.28, against ~2700 and
~3100) and the existing silicate sits over them, so the three-layer band was re-run at
fractions 0, 0.25, 0.5, 0.75, 1 — declared, not fitted:

| moon | published | band top f = 0 → 1 | fraction in [0, 1] that closes it |
|---|---|---|---|
| Callisto | 0.3549 | 0.3119 → 0.3321 | **none** — 0.023 short at pure antigorite |
| Titan | 0.3414 | 0.3126 → 0.3334 | **none** — 0.008 short |
| Enceladus | 0.3350 | 0.3008 → 0.3216 | **none** — 0.013 short |

Lightening the rock to pure antigorite closes 40–75 % of each gap and no more. That is the
strong result the brief allowed for: **the answer on these three is not serpentinisation but
void space** — C9's branch, porosity retained on a heated body — or the partial
differentiation C7 declined to model. Two items now answer one question from two sides, and
C9's discriminator keeps its own layer: a body whose core is antigorite-dominated would not
keep its pores (rheology), while Hilairet's density stands (density) — on Enceladus the two
statements together say the pores are in rock that is *not* mostly antigorite, which is
consistent with this table.

**Dante / Hades.** One of the two readings of that open radius question is that the rock is
lighter than this silicate; C10 gives it a tool and does not run it. The judgment is the
owner's.

**Revisited 2026-08-30 (F2), with the overturn condition registered first.** Holland & Powell
1998 is in the cache and antigorite **is** in its Table 5 (atg, a° = 4.70×10⁻⁵ K⁻¹ in
α(T) = a°(1 − 10/√T), κ₂₉₈ = 525 kbar, the C_p polynomial), and Hilairet's §4 borrows from
exactly that paper — the chain holds. The term is carried flattened at 298 K
(αK_T = 1.33 MPa/K with Hilairet's K₀; c_V 966 J/kg/K), from a pure-Mg end-member onto a
natural Fe/Al sample. Re-run on the same grid, the bands are unchanged to four decimals at
every finished point (Enceladus −0.0001 at f ≥ 0.75; Callisto and Titan at f = 0.75 ran past
the sweep's budget, a C3 band defect traced in the notes, not a change in the answer): the
moons' rock sits within ~100 K of the reference and the thermal pressure is ≲ 0.1 GPa
against 2–3 GPa. **No moon reaches its
published C/MR² at any fraction in [0, 1]; C10 stays closed.** The grade stays analog, and
its reason is now the borrowing and flattening, not the term's absence — the sentence that
said otherwise is rewritten here and in the docs. Two ceiling-poking finite differences were
fixed on the way (`eos.Material.k_t`, `interior._adiabatic_dtdp`); no anchor touched.
`engine/antigorite-thermal-context-notes.md` has the transcription and the runs.

### C11 — The middle rung: a declared differentiation front and a never-melted crust — **opened 2026-08-30 on F3's grounds; closed 2026-08-30**

**What it is, and what it is not.** C7 refuses a body that is neither fully mixed nor fully
layered, because ice mixed through rock *where liquid water reached it* is a reaction and a
transport history. **C7 stays closed, and C11 is not its repair.** C11 is the other case F3
found in Malamud & Prialnik 2015's full text: the depth the melting reached is taken as a
**declaration**, and the body is static — metal core, rock, water/ice mantle, and above the
front a crust that never melted, cold ice and rock grains never in contact with liquid water.
Hydration is a story about places liquid water reached, so C7's argument does not apply
there; and for that state a mixing rule exists — Yasui & Arakawa 2009's two-layer model,
adopted as Malamud & Prialnik's eq. (1) and reported to do *"a very good job of reproducing
the compaction curve of the mixture"* (§3.1.3) — the shape C10 already uses for antigorite
plus enstatite. The first row added after the list closed.

**Two declarations, not one.** `differentiation_front` (cumulative mass fraction from the
centre that melted; 1.0 is today's body) and `crust_rock_fraction` — the second because the
source's outer mantle is *not* primordial: it is ice-enriched by water that rose and refroze
(§5.1), so the front alone does not fix the crust's composition; the primordial fraction is
an upper bound. Optional `crust_porosity`: the same paper's eqs. (4)–(6) with Γ = 1 (never
melted), laboratory compaction curves, an **upper bound** on void. Directions registered
before the sweep: crust rock **raises** C/MR², porosity **lowers** it. `_stack` gains the
crust as a fourth layer (ice ladder + silicate as grains, additive volume, no
serpentinisation — water never reached it); a crust step above the melting curve is refused
as a self-contradictory declaration. Grade analog whenever a crust is declared; the
Malamud porosity functions landed first (8786d857) so no intermediate commit is broken.

**The sweep, on a declared grid, not tuned.** Potential temperature 200 K — at the roster's
270 K the crust is refused, because ice Ih/III/V melt at 251–273 K between 0.02 and 0.6 GPa
and a never-melted crust cannot sit there; the reference (front 1.0) is re-run at the same
200 K. `infer_three_layer` over core fractions 0/0.15/0.30/0.45; `test_interior.py
--middle-rung` regenerates it. Band = C/MR² over the core-fraction members that reproduce
the radius:

| moon (published) | front | X_d 0.3 | X_d 0.6 |
|---|---|---|---|
| Callisto (0.3549) | 1.0 | 0.2881–0.3127 (no crust) | — |
| | 0.9 | 0.3010–0.3077 | 0.3155–0.3203 |
| | 0.8 | 0.3107–0.3158 | 0.3393 |
| | 0.7 | 0.3220–0.3348 | **0.3561–0.3643** |
| | 0.6 | 0.3275–0.3390 | 0.3714–0.3768 |
| Titan (0.3414) | 1.0 | 0.2883–0.3138 (no crust) | — |
| | 0.9 | 0.3011–0.3081 | 0.3158–0.3207 |
| | 0.8 | 0.3103–0.3300 | **0.3384–0.3498** |
| | 0.7 | 0.3218–0.3350 | 0.3547–0.3633 |
| | 0.6 | 0.3270–0.3390 | 0.3695–0.3757 |

**Where they land.** C10's grid lay entirely below both published values; C11's grid
**brackets them**. Titan's 0.3414 falls **inside** the band of one declared pair — front
0.8, X_d 0.6 (0.3384 at core 0.15 to 0.3498 at core 0) — closed along the core axis the way
Europa's is, with the declarations untouched. Callisto's 0.3549 falls **between** two
declared pairs: above the front 0.8 · X_d 0.6 band (0.3393) and just below the front 0.7 ·
X_d 0.6 band (0.3561–0.3643), 0.0012 under its low end; no grid point's band contains it,
and the grid is not refined to make one — that would be the fitting C5 and C10 declined.
Porosity on the front 0.7 · X_d 0.6 pair moves the band down as registered: Callisto
0.3561–0.3643 → 0.3390–0.3494, Titan 0.3547–0.3633 → 0.3386–0.3496 (about −0.015, the
laboratory upper bound on crust void). One member did not converge (Callisto, front 0.9 ·
X_d 0.3, core 0.30). The table is the regeneration on the code that
ships (2026-08-30, after the crust-refusal fix was narrowed — see the notes' post-mortem),
identical at all twenty points to the first pass; run times 2–7 min per point; the 270 K
refusal through the inversion route did not finish in 17–24 CPU-minutes and was stopped — the temperature bracket is
exhausted on every solve of the regula falsi — where the direct `solve` refuses in about 12 s.
Recorded as a cost, not fixed here.

**What moves and what does not.** Anchors bit-identical: Uranus and Neptune (the stack's
bounds for a body with a gas envelope reproduce the old expressions to the bit — checked
after a negative-crust bug in the first pass had frozen both as refusals, which is exactly
the failure the anchor exists to catch), Europa's inversion, the rock and giant anchors;
`--refresh` for the fingerprint (`_stack`, `integrate`, `shoot` changed). The Callisto and
Titan question C10 left — *void space or partial differentiation* — now has its second half
measured: a declared front with a rock-bearing crust reaches the published values, a
serpentinisation fraction does not. Which pair, if any, a body should declare is the owner's
call; this row supplies the grid. `engine/middle-rung-context-notes.md`.

## What closing all of these does not do

It does not make the solver answer every body. Brown dwarfs and stars stay out by the line
above, and each material ceiling stays where its evidence stops. What it does is make every
remaining refusal **one this recipe chose**, with a named mechanism and a citation, rather
than one it fell into.

That is the standard the rest of the engine is held to, and it is what "finished" means
here.

## Related

- [`interior-structure-methodology.md`](../docs/reference/interior-structure-methodology.md)
  — the domain table these entries index
- `engine/*-context-notes.md` — the reasoning behind each closed item
- `engine/coverage-review.md` — a 2026-08-27 snapshot, superseded by this file
