<!-- 내부구조 솔버 코어 목록 중 닫힌 항목의 기록 절을 옮겨 둔 보관 파일 -->
# Interior solver — the core list, closed entries

The evidence sections of entries whose row in [`interior-core.md`](interior-core.md)'s table reads **closed**,
moved here byte for byte on 2026-09-23 so that the working ledger holds the open ones. Nothing below was
rewritten; the table rows stay in the working ledger, which is still the one place to ask "what is open".
One exception, inside C47 (i): its sub-section *The C21 premise, re-measured* stays in the working ledger,
because C21 is open.

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
solver item, so it is not on this list. *(It became C18 under the owner's notation and closed on
2026-09-04 as a named refusal — see C18.)*

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

**Parked at the gate 2026-08-30 (F4, Queyroux at the seam).** The band 16.5–20.6 GPa has
one measurement, Queyroux+ 2020 (2020PhRvL.125s5501Q, the arbiter's seat, independent of
Kimura 2023), and this repository holds its six-page Letter but not the Supplemental Material
that carries the individual melting points (Table S1). The values printed in the band —
15.6(2) GPa at 905 K and **18.4(9) GPa at 944 K** — are the ice VII″ → VII′ **isostructural
solid transition** on two isotherms (§*Isostructural transition*; Fig. 1 keeps "melting line"
and "isostructural solid transition" as separate symbols), not melting points; the triple
point is 14.6(5) GPa · 850(20) K. F1's criterion, reused, has nothing to put a residual inside
of, and a fit cannot reopen a row, so the fourth branch fires and nothing moves. What the
Letter does give is a **bound**: liquid at 15.4 GPa · 944 K (Fig. 2a) and solid at 18.4(9) GPa
· 944 K put T_m(18.4 GPa) above 944 K — above IAPWS's 690 K by 254 K and Reinhardt's 801 K by
143 K, the direction and size of Kimura's out-of-band point. Recorded as orientation, not a
verdict. Table S1 (free from APS, requested from the owner) is what would run the item.
`engine/queyroux-seam-context-notes.md`.

**Revisited 2026-08-31 (F4 resumed): Table S1 arrived, and the measurement sits with
neither curve — it is hotter than both.** Twelve measured melting points (Queyroux+ 2020
Supplemental Material Table S1, read from the PDF), three inside the band: 16.6 ± 0.5 GPa ·
930 ± 10 K, 16.6 ± 0.2 · 944 ± 10, 17.3 ± 1.1 · 978 ± 10. Against them IAPWS eq. (5) is
255–297 K cold (25–30 σ) and Reinhardt's line 213–228 K cold (21–23 σ); at every point from
8.4 to 17.3 GPa both curves are on the cold side, IAPWS already 69–79 K (14–16 σ) cold at
8.4–8.8 GPa. So of the three registered outcomes none fires as written: not "with Reinhardt",
not "with IAPWS" — **C3 does not reopen** — and not "between" but *above both*. The band is
redrawn to what the data support: **both curves too cold by 210–300 K at 16.6–17.3 GPa**,
Reinhardt the less wrong by 40–70 K; the +26 % step is in the measured direction and not
large enough; the dispatch is unchanged because the recipe has no third curve, and adopting
Queyroux's points as a melting-curve source is an owner decision with this table as its
grounds. Above 27 GPa (σ_T = 100 K) Reinhardt is inside at 27 GPa and hotter than Queyroux by
160 and 239 K at 36.7 and 44.7 GPa — while F1 found it inside Kimura & Murakami's ±130–150 K
at six of seven points; the two experiments differ by the 100–150 K Queyroux themselves
report against the laser-heated family, and this recipe does not adjudicate between them.
Grade: the measurement clears the 5 % bar (σ_T/T_m 0.7–1.3 % to 17.3 GPa) and the curves do
not clear the measurement, so analog stands with a new reason — the one measurement in the
band sits 210–300 K above both lines. Table S1 is a check table in `test_interior.py`.
Two ways a check can fail to raise a grade, now both on record: F1's — the check's own error
(8–11 %) is larger than the scale, so it cannot see; F4's — the check is precise enough
(0.7–1.3 %) and **the thing checked is wrong**. The grade word is the same; the reasons are
opposites, and the second is the one that names what would have to change.

**Revisited 2026-09-01 (Brief 33) — the owner adopted, and the adopted thing is not
"Queyroux".** F4's park closed the way it registered: the reopening condition (a
melting-curve source decision by the owner, with the S1 table as grounds) fired. Below the
kink (14.6 GPa) the dispatch now carries **the unweighted mean of the two post-2020
measurements** — Queyroux+ 2020's lower Simon–Glatzel and Prakapenka+ 2021's ice-VII
segment — a stretch where the continuous-vs-discontinuous lineage debate (Rescigno+ 2025
defends continuous; Datchi stands on both sides) does not exist and the two agree
(|Q−P| ≤ 54 K vs 71–348 K to the old curve). Our own IAPWS piece is excluded from the mean
(a three-way mean let our curve vote on its own trial, 111–120 K below both measurements).
Label conditions carried in `eos.py` at the constants: the two papers share Datchi's anchor
(2.17 GPa · 354.8 K printed in both), so the 1.0 K agreement at 8.2 GPa is never independent
confirmation — the independent number is 8.7 K at 20.0 GPa; the mean's uncertainty is the
curves' separation alongside each σ, never σ/√2; below 8.4 GPa the span is anchored
interpolation, not measurement support. **14.6–20.6 GPa is now a named disputed refusal**
(the sources agree numerically but assign different phases — VII′ vs VII — and the dispatch
consumes the phase; verdicts are still given outside the candidates' envelope, and no roster
body reaches the band: ice-giant column tops 34.5/39.2 GPa, moon calls all below 8.4 GPa).
Above 20.6 GPa nothing changed. **The grade's reason moves accordingly**: below the kink the
curve is no longer simulation but the mean of two mutually consistent measurements (grade
question now hangs on the mean's declared uncertainty, not on "the lines are simulation");
in the band the honest state is refusal, not a graded curve. Handover step at our VI–VII
triple point: +4.1 K, recorded not smoothed. Anchors bit-identical (measured); the old seam
sentence ("+26 % at 20.6 GPa, both curves cold against S1") stays above as the record of
what the dispatch was when C3 closed.

### C5 — Where the giants' leftovers belong — **closed 2026-08-30**

Two residuals; both now have an owner, and one has two declarations it can be read against.

**Jupiter, and the diluted core — reached, no consumer.** The mixture rule carries one
homogeneous Z through the envelope. Post-Juno structure is not "graded inward": Debras &
Chabrier 2019 §4.1 (2019ApJ...872..100D, text in the cache) is titled *Inward decreasing
abundance of heavy elements in some part of the outer envelope* — locally ∇Z > 0 — and the
structure needs four regions: an outer convective envelope, a composition-and-entropy
gradient, an inner convective envelope and an extended dilute core. Not implemented: Alpha
Centauri A b's radius is a declaration, so nothing in the roster would read a graded-Z
envelope today. The earlier compact-core attempt and its silicate ceiling stay in the domain
row.

**Corrected 2026-08-31 (survey ⑥) — this row claimed "two transcribable forms exist" and one
of them is not one.** *Helled & Stevenson 2017's* Z(m) is a Gaussian the paper prints and
then disowns twice: the sentence introducing it says *"In such a case (**which is merely
chosen to aid the explanation**)"*, and §I says the validity of their suggestion
*"**doesn't automatically lead to a prediction for the final Z-profile** which depends on the
specific conditions under which the giant planet has formed."* What the paper gives is a
**formation-history relation** plus an illustrative profile computed from a specific Jupiter
formation model — not a form to transcribe. The accurate label is *"a formation-history
relation, and an example Gaussian chosen to aid an argument."* **`Howard, Guillot & Bazot
2023` is a real closed form** and stands: an erf profile whose width parameter δm_dil the
paper *"set[s] to 0.075"*, with no derivation or sensitivity test in the text.

*The consequence for C13*: its registered fourth branch — Helled & Stevenson's ice-envelope
applicability — **closes here, and not for the registered reason.** Not "Jupiter-only, cannot
be transferred" but **there is no function to transfer**; the mechanism's own conditions are
composition-independent, and the profile only ever arrives through a formation model our
bodies do not have.

*And the row was missing the paper that matters most for the ice giants.* **Vazan & Helled
2020** ([`2020A&A...633A..50V`](https://ui.adsabs.harvard.edu/abs/2020A%26A...633A..50V),
arXiv 1908.10682, cached) is about **Uranus**, fits **the moment of inertia directly**
(*"we fit MoI instead of the gravitational moments"*, target **0.222–0.230 MR²**), tests
whether a gradient survives on Gyr timescales with the Ledoux criterion, and tabulates four
adopted models. Its conclusion lands on this list's own open question: *"an interior with a
**mixture of ice and rock, rather than separated ice and rock shells**, is consistent with
measurements, suggesting that **Uranus might not be 'differentiated'**."* It has no closed
Z(r) either — it sweeps *"composition gradients of various slopes"* and selects on R, L and
MoI.

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

*Revisited 2026-08-31 (C13)* — (a)'s *"reached, no consumer"* was true when written and is
**superseded on the consumer half**: the ice giants' measured C/MR² deficit (−15.8 % /
−11.4 % after the radius is stripped, the gate's 2026-08-31 comparison) is a consumer. The
blocker moved, it did not vanish — not "nothing would read a graded-Z envelope" but "the
recipe cannot yet hold the arrangement it would grade toward": see C13, where the rock-free
extreme refuses at stack build. (b) is untouched.

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

*Revisited 2026-08-31* — **a time axis was considered and rejected** (owner's decision; the
planned C13 was not opened). Not because the recipe lacks an axis, but because **the axis is
a different one**. The Neumann & Kruse relation does not take an age in Gyr. What it takes is
**t₀ — the accretion time after CAI formation, in Ma** (their §2.3), and the outcome turns
on that value at the megayear level: for the wet olivine rheology successful models live in
t₀ ≈ 1.3–1.9 Ma (§3.3), and for the antigorite rheology **no differentiation occurs at all
for t₀ ≥ 5.5 Ma (at ϕ₀ = 0.6)** (§3.4) — because the short-lived isotopes (²⁶Al, ⁵³Mn, ⁶⁰Fe) release their
heat "within the first few millions of years after CAIs" (§2.3; all read from the cached
text this session). The structure is decided within ~5 Ma; the remaining 4.5 Gyr is
bookkeeping. **Feeding `body_age` (Gyr) into this node would give it the number it is least
sensitive to while the number it is most sensitive to stays undefined.** The six consumers
in sight (Uranus, Neptune, Callisto, Titan, Europa, Enceladus) are all solar-system anchors
whose ages are CAI-anchored directly, so inheriting an age from a star does not even arise
for them. For invented bodies neither t₀ nor the initial ²⁶Al abundance derives from the
star's age (Lichtenberg+ 2019 — reported by the directing session as 0–10× solar ²⁶Al₀
across systems, not re-read here — *corrected 2026-09-03 from the cached preprint, C21 (a): the paper's
scanned range is **[0.1, 10] × ²⁶Al_⊙**, floor 0.1 not 0, and it is a model scan, not an observed
distribution*): both are **declarations**, not derived values, and
whether to introduce them is a Phase 4 owner decision. Since ²⁶Al matters only for bodies
small enough to be shaped by it, the node never applies to the ice giants. **Do not draw a
`body_age → porosity` edge in the chain**: the edge is real but the payload would be wrong —
it must carry `t_form` (Ma after CAI), not `t_body` (Gyr); a Gyr endpoint is at most an
`influences`. Two papers considered for the request list are dropped with the time axis —
**Kruijer+ 2017** (Jupiter's Hf-W age) and **Castillo-Rogez+ 2009** (Iapetus): both served
only the Gyr-age inheritance question, which no longer exists.

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

### C11 — The middle rung: a declared differentiation front and a never-melted crust — **opened 2026-08-30 on F3's grounds; closed 2026-08-30; the declared pair settled 2026-09-01 — the grid is the answer, and no pair is elected**

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
X_d 0.3, core 0.30).

**Owner's decision 2026-09-01: the grid stands as the answer and no pair is elected.** The
question this row left open — *which declared pair should Callisto and Titan actually use* —
is resolved by declining it. **Titan's published value falls inside one pair's band and
Callisto's falls between two**, and refining the grid to capture Callisto's remaining 0.0012
is the fitting C5 and C10 refused and Brief 26 refused again. So the published statement is
the band, not a point: **the recipe says what each declaration implies, and does not claim to
know which one these moons are.** Anything downstream that needs a single number — a cfg
value, a board row — declares its own choice and carries that label, rather than borrowing
authority from a measurement that was never made. The table is the regeneration on the code that
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

### C12 — A ternary anchor from a diffusion table? — **opened 2026-08-31 on the owner's grounds; closed 2026-08-31, recorded**

**A check, not a material — and not a reopening of C4.** Opened when the owner doubted the
report that Bethkenhagen+ 2017's typeset version (`2017ApJ...848...67B.pdf`, in the cache)
carried no usable data — a report made from the text layer twice — and read it as images:
the EOS grid is indeed absent (Figures 1–3 only, no table, no supplement; **C4's methane half
stays on its author-request route**), but **Table 1** prints R · ρ · T · p at thirty state
points along three Uranus profiles beside the real 2:1:4 mixture's self-diffusion
coefficients. If ρ were the mixture's, water-alone could be measured against the real ternary
— the number C4 said needed the tables.

**Settled from the text first**: §4 introduces the table as *"the diffusion coefficients of
each species in the real ternary mixture, as well as radius, density, temperature, and
pressure along the three profiles"* — profile quantities; §2.7 matches the profile's
*pressure* within 2 % and says nothing of tabulating the box's density; the mixture's own
density appears as Figure 4. The text's reading is (나), the profile's density. **The
registered discriminating check then failed on its own premise**: this recipe's water
(Mazevet+ 2019 at all thirty rows) is 18–32 % denser than *every* printed ρ, including the
water-only profile's (29 % at 6.9 GPa · 1775 K → 18 % at 510 GPa · 5750 K), so the column is
not pure water's density anywhere — and both readings can explain that size (an H/He-bearing
inner envelope under (나); a mixture 15–25 % lighter than water under (가), which C4's own
ammonia result makes plausible). **Closed on the conservative branch**: no ternary anchor can
be read from the column with the evidence held; C4's composition tier keeps its water +
ammonia number. What would settle it: Redmer+ 2011's own ρ(R) for the water-only model, or the
authors. **The failed test was the audit session's proposal, fixed into the brief by the
directing session — the responsibility is joint**, recorded the way this project keeps every
error named. *Observation, derived, not a verdict*: the residual shrinks with depth
(+29 % → +16–19 %), which is qualitatively what reading (나) with a small H/He admixture in
the inner envelope would do; Redmer+ 2011's ρ(R) would most likely settle it that way.
**Redmer+ 2011** (Icarus 211, 798, the water-only Uranus model) goes on the owner's
paper-request list; if it prints 1.00 g cm⁻³ at 0.839 R_U, (나) is settled and C12 reopens as
*revisited*. *(Superseded by the revisit below, written later the same day: the paper was obtained,
printed no ρ(R), and came **off** the list because a shell-boundary sentence replaced the need — the
later paragraph is the current state, kept here as the record of what was asked; Brief 64 labelled it.)* No code, no anchor, no gate change. `engine/ternary-anchor-context-notes.md`.

*Revisited 2026-08-31* — the owner obtained **Redmer+ 2011**
([2011Icar..211..798R](https://ui.adsabs.harvard.edu/abs/2011Icar..211..798R), cached as
`docs/phase3/_papers/2011Icar..211..798R.pdf`), and the expected settle path does not exist
in it: **no ρ(R) table** (Figures 1–3 only, no supplement; the structure models are taken
from Fortney & Nettelmann 2010). **(나) is settled anyway, by a shorter path** — one
sentence of shell geometry instead of a number. Bethkenhagen+ 2017's Figure 3 caption names
the model (*"water-only (Redmer et al. 2011)"*), their §2(i) states what the name means
(*"ices are represented solely by a water EOS"* — the ice component's representation, not
the planet's composition; the model is three-layer with an H/He-rich outer envelope), and
Redmer+ 2011 prints the shell boundaries: *"the ionic water shell extending from 0.6 to
0.8 R_p"*. Table 1's shallowest row sits at **0.839 R_U — above the water shell, inside the
H/He-bearing outer envelope**, where ρ = 1.00 g cm⁻³ is the profile's density and could not
be pure water's; our water being +29 % against it is thereby explained. The verdict does not
move (closed, conservative branch; no ternary anchor; C4's tier keeps water + ammonia — that
Table 1 gives no mixture density is now confirmed, not assumed). What moves is the closure's
quality, from *"could not confirm — the anchor cannot be read under either reading"* to
*"confirmed — reading (나)"*, and the failed test's wrong assumption gets its final name: **a
misreading of the profile's name** — "water-only" states the ice component's composition,
not the body's. Redmer+ 2011 comes **off the request list**: not because it yielded the
number, but because the shell-boundary sentence replaced the need for it. All three quotes
verified against the cached PDFs in this session.

### C13 — Does the fuzzy core account for the moment-of-inertia deficit? — **opened 2026-08-31; closed 2026-09-01 as a named refusal: the deficit is real, three axes were measured, and each stops at a boundary this recipe can name**

**Not C5's repair.** C5(a) recorded a graded-Z envelope as *reached, no consumer* — true
when written. What opened this row is a **measurement**: the ice giants' C/MR² sits
−24.3 % / −25.3 % under Nettelmann+ 2013 (P_Voy, R_mean), and **−15.8 % / −11.4 % remains
after the radius is stripped**. A fuzzy core is the candidate whose sign matches — and sign
is not size (C5(b) taught that: the boundary layer had the plausible direction and widened
the residual).

**The target is a derived value, said plainly**: λ is J₂, J₄ and an assumed rotation period
passed through an interior model — matching 0.230 is agreeing with what the gravity field
permits, not matching nature. And N13's own models are three-layer with **rocks confined to
the core**, so the number this row would chase was produced by a model that does not contain
the thing this row would add; λ being gravity-constrained softens that, but any future
"matched by adding what they did not have" needs its own justification, written here in
advance.

**The non-core terms, bounded first** (each ruled out as the owner of the remainder): the
rotation term — our λ is a non-rotating sphere's — is order 1 % by the axial-vs-mean
identity (2/3)J₂ = 0.00234 / 0.00236, with m_rot = ω²R_eq³/GM = 2.95 % / 2.61 % as the
restructuring scale; the rotation-period spread is a **target-side** spread of −3.3 % /
+6.0 % (attribution measured against P_Voy: IAU baseline, normalization-matched, both
papers' default). Together ≲ 7 % against 11.4–15.8 %: a remainder survives.

**The bracket, and why it could not be held.** As briefed: end A = the anchor's compact
central silicate; end B = the same rock mass (5.43 % / 6.07 % of the planet) spread
uniformly through the envelope (`envelope_z` = 0.283 / 0.321, no silicate layer). **End B
refuses at stack build, at any temperature**: with no silicate at the centre the water
column reaches P_c (1220 / 1533 GPa) and the cold-phase pre-check demands the solid
ladder's coverage, whose French & Redmer 2015 evidence span ends at **1000 GPa** — even
though the answer's deep column is fluid (Mazevet) and never touches the ladder there.
Branch 2's registered assumption ("nothing in the recipe caps the outer extreme") is
**false, with the cap named**. Third member of one family in two days (C11's over-broad
refusal, the Queyroux–Neptune route death): **the trial corridor's cold flank demands
evidence the answer never uses.** The analytic ceiling, computed since the engine could not
(all rock at the surface, structure held fixed — assumptions written): Δλ/λ ≤ f_rock/λ =
+31.2 % / +33.7 %, above the required +18.7 % / +12.9 % — so the fuzzy core **cannot be
excluded**, and is not confirmed: the solvable span was never measured.

**Open, with the settling path named**: the cold-flank representability work (route the
over-depth ladder refusal so the temperature loop stays on the fluid side, or teach the
pre-check that a column can be fluid-only where the answer is), after which end B is two
solves. It is the same prerequisite the Queyroux adoption would need — the two owner
decisions share it. **The registered fourth branch — Helled & Stevenson 2017's
ice-envelope applicability — is closed as of survey ⑥ (see C5's correction): there is no
closed form to apply, because that paper disowns its own Gaussian as illustrative and
delivers a formation-history relation instead.**
Both refusals reproduce in ≤ 1 s. No code, no anchor, no gate change.
`engine/fuzzy-core-context-notes.md`.

*Revisited 2026-08-31, same day — the audit overturned "could not be held": end B was
**1 ULP away**, and the bracket is now measured.* The audit's independent construction
(`imf = 1 − (rock+hhe)/m`) leaves a floating-point residual of +5.6e-17 for Neptune — a
ghost silicate stub that occupies the centre, keeps the water column off the 1000 GPa
ladder cap, and lets the cold flank survive: **1 s refusal vs 112 s convergence on one
ULP.** The directing session pre-registered the reading (λ stable across ε → the ε→0
limit; λ moving with ε → artifact) and ran ε = 1e-7 / 1e-9; this session's runner
reproduced every digit (triple complete), added the float-residual point, and retired the
caveats: **λ is stable across nine orders of ε** (Neptune 0.219683 at 1e-9 vs 0.219617 at
5.6e-17, a 3e-4 relative move; Uranus 0.209756 / 0.209749 at 1e-9 / 1e-7 — its
float-residual point does not exist, because 1 − (0.79+2.0)/14.536 leaves a residual of
exactly 0.0 and dies: **the same expression revives Neptune and leaves Uranus dead**,
which is the cold-flank family's strongest exhibit); the ladder wall does **not** press
Neptune's P_c 984 GPa (a probe at 1010 GPa integrates; mass closure 1.000000); grid
1500 → 6000 moves the radius 3.7–3.9e-4, the anchors' own order. **The measured bracket:**

| | I/(M·R_pub²), end A | end B | target (N13, P_Voy) | gap covered |
|---|---|---|---|---|
| Uranus | 0.1937 | 0.2032 (λ 0.2098, R −1.57 %) | 0.2300 | **26 %** |
| Neptune | 0.2135 | 0.2248 (λ 0.2197, R +1.15 %) | 0.2410 | **41 %** |

**The answer this axis gives: rearranging the declared rock mass — any grading between
compact core and uniform envelope Z — buys at most 26 % / 41 % of the gap. This axis
cannot close the deficit.**

> ⚠ **Condition attached 2026-09-01 (Brief 31): these two percentages were measured on the
> clamped table, and they do not survive its repair.** With the 66 repairable clamped nodes
> assembled instead of read, **both ends of this bracket stop converging** (λ −6.9 % / −5.5 %,
> boundary condition missed) — so the bracket **is not measurable at all** on that path. The
> same holds for Brief 26's gradient span: 39.7 % / 60.0 % collapses to ≈3.6 % / ≈1.5 %, the
> wide half refusing. **These are measurements of a table choice, not of the planet.** A number
> that exists on one grounded route and will not converge on the other was never robust to
> that choice. Which route is nearer the truth this experiment does not say — the truth is in
> the original authors' unpublished calculation. Default path unchanged: the repair is an
> opt-in instrument (`engine/hhe_repair.py`), nothing imports it, the baked table still carries
> its 72 clamped cells, the anchors were not refreshed, and both readings are kept side by
> side wherever the numbers appear. **Owner's decision 2026-09-01: the default stays the
> published table** — not because that route is judged nearer the truth, but because there is
> no ground to elect either as truth, and this list's practice when it cannot choose is to
> record the divergence rather than pick (the move C11 made when it published a grid of
> declared pairs and declined to select one).

What this is *not*: a ceiling on the fuzzy core as the
literature means it, which spreads **ice** as well as rock; the recipe's end B moves only
the declared rock. The remaining owners on the table are that difference (graded ice) and
the ice mantle's own density profile — the ice axis stays open, unmeasured. The stub is an
apparatus, not a repair: that the corridor's boundary sits one floating-point digit from
the answer's path strengthens the structural diagnosis (`f3f3a3fd`), and the general fix
remains the shared prerequisite of both pending owner decisions. Bonus, measured on the
way: end B also **shrinks the radius residual** (Uranus +5.48 % → −1.57 %, Neptune
+8.94 % → +1.15 %) and cools the centre (T_c 4953 / 4901 K) — recorded, not attributed.

*Revisited 2026-08-31, later the same day (Brief 22)* — **the stub is retired: end B
solves with no stub at all.** The cold-flank corridor repair (the rules paragraph;
`engine/cold-flank-context-notes.md`) removed the three static spots, and the
pre-registered acceptance passed: both planets solve under **both** `imf` expressions —
Uranus (residual exactly 0.0, the configuration that died) λ 0.209729 · renorm 0.2032;
Neptune (±5.6e-17) λ 0.219577 / 0.219617 · renorm 0.2248 both ways. 1 ULP no longer gates
solvability, only nudging λ by 1.8e-4 relative, inside the ε-ladder envelope. **The
measured bracket stands stub-free: 26 % / 41 % were not stub-dependent** (branch 4 did
not fire). The ice axis (③) is now measurable without any phantom device — which was the
reason ① was ordered before it.

*Revisited 2026-08-31, Brief 23 — **the ice axis, attempted: representable except one
named wall, and no bracket end converges through it.*** The mixing question was answered
from sources first (Soubiran & Militzer 2015: additive volume for H₂O–H₂ measured good to
a few %, ≤10 % locally, over 2–70 GPa × 1000–6000 K; and N13's own envelopes are LM-REOS
*linear-mixed* water — matching like with like), so branch 4 did not fire. The
representation was built (`envelope_z_rock_fraction`, a dispatching `_EnvelopeWater`
part, and **water1's c_P baked** — the source's own Gibbs quantity, closing the hole that
confined C5(b)'s rock mixing to ≥ 2.3 GPa). All four end-B states (ice / ice+rock × two
planets) close mass exactly and **none converges**: a refusal spy shows 1102 of 1202
trial deaths on one wall — **liquid envelope water at p ≲ 0.1 GPa × 500–1000 K**, the
tri-corner of water1's 500 K top, water2's 0.1 GPa floor and Mazevet's 1000 K floor,
which every path cold enough to reach the 76 / 72 K boundary must cross carrying 85 %
dissolved water. Branch 3, refined: blocker named, with a published filler (IAPWS-95 /
IF97 steam covers it) whose baking is an owner decision. **No gap-covered percentage is
reported** — a bracket end that misses the boundary condition by ~1200 K is not a
measured end. Recorded, not judged: all four states sit *above* the targets (renorm
0.2531–0.3061 vs 0.2300 / 0.2410), and the wedge-crossing is partly the uniform-Z
bracket's own artifact — a graded profile tapers the water toward 1 bar and is not
blocked to the same degree. `engine/ice-axis-context-notes.md`.

**The ice axis, attempted twice and measured as a wall both times — 2026-09-01 (Briefs 23, 25).**
Brief 23 put the declared ice into the envelope as a uniform Z; every bracket end refused, and
**1102 of 1202 refusals sat at one water wall** (p ≲ 0.1 GPa × 500–1000 K — the junction of
water1's 500 K ceiling, water2's 0.1 GPa floor and Mazevet's 1000 K floor). Brief 25 baked
IAPWS-IF97 regions 1–3 to fill exactly that window.

**The steam bake did what it was for: the water wall is retired.** In the same solve the spy
now counts **100 refusals, 100 % of them `h_he`, water 0.** But no end converges, so **no
gap-covered percentage exists** and the registered product is the next wall's coordinates.

**Where it moved, and why the target is unreachable.** The surface pins at **355–363 K
regardless of central temperature, against a declared 76 K.** Every trial adiabat cold enough
to head for 76 K dies on the **H/He table's low-temperature floor**, measured here directly
rather than inferred from the refusals:

| pressure | lowest temperature the `h_he` table will evaluate |
|---|---|
| 130 GPa | **1830 K** |
| 150 GPa | 1900 K |
| 164 GPa | 1945 K |
| 1050 GPa | 3130 K |

The refusal samples sit at 131–1121 K in the first band (130–164 GPa) and 1929–3096 K in the
second (~1046–1062 GPa) — **below the floor in both.** So a cold envelope at those depths has
no representation at all, and the 76 K surface is not reachable from below by any central
temperature.

*Corrected 2026-09-01 (survey ⑦) — this was first written as "a material ceiling of the kind
C6 lists". It is not one.* The floor is **our own declared line**, not the source's evidence
limit: `hhe_table.py` carries `REACH_A = 2.7198`, `REACH_B = 0.2567` and the rule
`log T ≥ REACH_A + REACH_B · log P`, whose comment says *"below that a **convecting** envelope
does not reach, and the distributed table's defects (7 sentinel cells in the density slot,
grad_ad clamped to 0.1/0.5) are all down there. We refuse rather than repair — stating the
domain beats touching published numbers."* Evaluated at the five pressures probed above, the
line gives 1830.0 / 1898.5 / 1942.5 / 3128.5 / 3132.3 K — **reproducing every measured floor
point**, residuals 0 to +2.7 K in the direction a 5 K probe step would give. The underlying
table (Chabrier, Mazevet & Soubiran 2019, cached) advertises **10² to 10⁸ K** and our own
baked subset starts at 100 K. **Nothing is missing. We declined to enter.**

*The four ends, recorded and not judged* (λ, then the radius residual, then
`I/(M·R_pub²)`): Uranus B_ice 0.294150 / −10.51 % / 0.2356; Uranus B_both 0.313228 /
−12.81 % / 0.2381; Neptune B_ice 0.299345 / −7.81 % / 0.2544; Neptune B_both 0.305116 /
−5.30 % / 0.2736. All four sit **above** the targets (0.2300 / 0.2410), the same direction as
the earlier attempt with values moved by the surface coming down from ~1275 K to ~360 K.
**None of this is a measurement** — an end that misses its boundary condition is not an end,
and these numbers must not be quoted as the ice axis's coverage.

**The label steam does not buy still rides**: trial paths now *cross* the old wedge on IF97,
and that crossing happens over an unverified additive mixture, outside Soubiran & Militzer's
validated band on both axes (`7769be6e`).

Two defects were found on the way and are registered in the rules above — the re-armed
sentinel that let the temperature loop run 51 attempts against a ceiling of 29, and the
climb that hid the wall from the controller. Both were invisible while every trial died in
the steam wedge first.

**The composition gradient, measured — and the widths that work are the ones that are not
allowed (2026-09-01, Brief 26).** Z(x) as Howard+ 2023's erf, discretised by shell mass. The
implementation's own check came first and passed twice: **width → 0 reproduces the layer stack
bit-identically**, both against the anchor and against a rock-free toy, so the gradient is
continuous with what it replaces rather than a second recipe. It also **clears the wall that
stopped the ice axis** — the uniform-Z end carried heavy material to the surface and dragged
the adiabat under `h_he`'s floor, while a gradient's upper envelope converges to clean H/He
and stays inside the window. That was predicted in Brief 23's landing note and tested here.

**Then the cap excluded the result — and the cap is weaker than "stability".** What route A
actually transcribes is **a description of Vazan & Helled 2020's successful models, not a
stability calculation.** Their sentence, read at its place in the cached text: models matching
radius, luminosity and moment of inertia *"have some **common properties**: in these models the
outer 20% of the planetary radius develop a large-scale convection on top of a stratified inner
region. This convective layer is metal rich for all models except for the two-layer model
(U-1) … heavy-element enrichment of 0.6-0.7."* So the criterion is **"does this look like the
profiles that worked for them"**, not **"is this convectively stable"** — Ledoux is what
*they* used to test survival; the 0.8 R figure is an outcome they observed. The row says so
because the two readings license very different next moves.

Under that criterion, the gradient's span sits below 0.8 R **only at δm_dil = 0.01 and 0.025 —
the two widths that sit on the layer limit and move nothing.** w ≥ 0.05 crosses
0.8 R and w ≥ 0.075 reaches the surface. **Taking route A as transcribed, the reachable
coverage is ~0 %, and the span below is a set of unreachable points.** Route B (deriving our
own ∇X) refuses by name: no radiative gradient exists in this recipe, and the check does not
invent one.

| δm_dil | Uranus renorm | ΔR | Neptune renorm | ΔR |
|---|---|---|---|---|
| 0.01 · 0.025 *(within the cap)* | 0.1937 · 0.1937 | +5.44 % · +5.32 % | 0.2135 · 0.2136 | +8.90 % · +8.78 % |
| 0.05 | 0.1938 | +4.97 % | 0.2137 | +8.37 % |
| 0.075 *(Howard's value)* | 0.1941 | +4.27 % | 0.2140 | +7.58 % |
| 0.125 | 0.1951 | +2.19 % | 0.2153 | +5.50 % |
| 0.20 | 0.1991 | +0.33 % | 0.2200 | **+3.98 %** |
| 0.30 | 0.2081 | **+0.12 %** | 0.2300 | +4.14 % |
| target (N13, P_Voy) | 0.2300 | | 0.2410 | |

All fourteen converged; **no width was adopted** and the observables are reported beside the
grid, never fitted to. The span, if the cap were not there: **39.7 % (Uranus) / 60.0 %
(Neptune)** of the deficit, monotonic in width with no plateau inside the registered grid.
(Neptune's 0.2300 at w = 0.30 equals *Uranus's* target — a coincidence of digits, not a
result.) Shell count is not a knob: 32 → 64 leaves renorm at 0.1941.

**The exclusion's own scope, stated because it bounds the verdict.** The declared family here
is a two-end erf with `z_shallow = 0`; Vazan's stable models put a **metal-rich homogeneous
convective top (Z ≈ 0.6–0.7) above the gradient** — a shape this family cannot express. So the
finding is *"widths that move the answer are outside the cap **for this family**"*, not
*"gradients are unstable."*

**A second product, unasked for: the radius residual collapses.** Uranus **+5.44 % → +0.12 %**,
monotonic. Neptune **+8.90 % → 3.98 % at w = 0.20, then back to 4.14 %** — **non-monotonic,
with its optimum inside the grid**, while renorm rises monotonically for both. So the radius
axis behaves differently from the moment-of-inertia axis, and the two planets behave
differently from each other. Recorded, not judged.

**And the wall the two gradient families died on is one assumption answering two questions
(survey ⑦, 2026-09-01).** The reach line's justification is *"below that a **convecting**
envelope does not reach"*, and it was derived by integrating **adiabats**. Both halves are
statements about a convective, adiabatic envelope.

**A composition gradient is, by definition, stably stratified** — that is what makes it a
gradient rather than a mixed layer — and Vazan & Helled say what follows: *"The heat in a
stable (steep) composition gradient region is transported by **conduction**"*, the layer
*"acts as a thermal boundary to suppress convection and slow down the internal cooling."* A
sub-adiabatic profile is **colder than an adiabat at the same pressure**, so a gradient model
descends below the reach line **on purpose**. That both families died on the same line is not
coincidence: **we asked a question outside the premise of a domain we had drawn from that
premise.**

*This does not make the refusal wrong.* The distributed values below the line really are
damaged — 7 sentinel cells, 887 clamped — and the source calls part of that region
*"unphysical"*, naming solid hydrogen and helium and the breakdown of the Wigner–Kirkwood
expansion, *"identified in Fig. 1 and 16"*. **What changes is the reason attached to the
refusal**: "a convecting envelope does not reach here" stops applying the moment the layer
being carried is stratified. One line is answering two questions, and only one of them is
still its own.

**Settled 2026-09-01 (survey ⑦ addendum): both bands are inside the forbidden region, and
what puts them there is helium, not hydrogen.** The figures arrived (the owner fetched the
paper; the earlier cached copy was an ar5iv conversion whose only two `<img>` tags were the
converter's own logo, which is why the text was readable and the figures were not).

**Fig. 1 and Fig. 16 are not two cuts of one diagram — they are the two pure components.**
Caption 1: *"Temperature-density domain of the present EOS for **hydrogen**."* Caption 16:
*"…for **helium**."* Both end with the same sentence, verified twice in the cached text:
**"The EOS must not be used beyond these limits."** Our table is the Y = 0.275 additive
mixture of those two.

| band | hydrogen's melting line | helium's | verdict |
|---|---|---|---|
| 130–164 GPa · 131–1121 K | ≈870 K at 130, ≈740 K at 164 — the band **straddles**, 81–88 % of its log-T width solid | ≈1180 K at 130, ≈1400 K at 164 — **the whole band sits below** | **solid** |
| ~1055 GPa · 2309–2340 K | Γ_m = 175 line ≈1520 K — band is 1.5× hotter, so **fluid by hydrogen** | ≈4100 K — band is **1.85× colder**, 0.27 dex, several times the error | **solid** |

**Read Fig. 1 alone and the second band answers "fluid".** It is helium that binds it, and
helium is 27.5 % of the mixture. Method, because the numbers are figure reads: vector PDF
rendered at 2400 dpi, measured against tick marks inside the same crop, **± 1 % in pressure
and ± 3.5–5 % in temperature**, with the calibration checked against a printed number — the
surveyor's H₂ melting maximum at ≈80 GPa · ≈1000 K against the text's *"determined
experimentally up to T ≃ 1000 K, P ≃ 100 GPa"*. One corner is left undecided rather than
claimed: band 1's top at 130 GPa (1121 vs 1180 K, inside the error), and band 2's crossing of
the f_WK = 0.7 validity limit (5 % ± 4 %).

**So §5's finding stands and does not open the region.** The reach line's stated reason —
*"a convecting envelope does not reach"* — genuinely stops applying to a stratified layer.
**But a second limit sits in the same place and does not care whether the layer convects:**
the source forbids its own EOS there. **The gradient path is wrong at those cells, and that
reason survives dropping the convective assumption.** Two limits happened to lie close
together and we had been citing the one that does not apply.

*What would settle the remaining corners, and it is arithmetic rather than a search*: the
melting and validity curves are printed as **eqs. (1), (2), (3), (7)**. Evaluating them turns
every ± 4 % above into an exact number. Not yet done.

**Tightened by the printed equations, and one of them has a wrong unit note.** The melting
and validity curves are printed, so the figure reads could be replaced by arithmetic —
reproduced independently by the directing seat.

**Helium, eq. (7): `T_m = 61.0 P^0.639`, followed by *"where the pressure P is in kbar
(= 0.1 GPa)"*. Read that way it gives 5959 K at 130 GPa against a figure read of ≈1180 K —
5× off.** The upstream source settles it, and it was already in our cache from the water
survey: Chabrier cites **Datchi+ 2000**, whose Simon law is `P = 1.6067 × 10⁻³ T^1.565`.
Inverting: **1/1.6067e-3 = 622.394, and 622.394^0.639 = 61.011**, while **1/1.565 = 0.6390** —
the printed coefficient *and* exponent are that inversion to the decimal. Round trip, checked
here: 300 K → 12.096 GPa → 300.01 K; 1000 K → 79.604 GPa → 1000.06 K. And 12.1 GPa at 300 K
is helium's known room-temperature solidification pressure, so it holds physically as well as
algebraically. **The coefficient is right and the unit note is wrong — P is in GPa.** A kbar
reading would require the printed coefficient to be 14.0. The paper is quoted as printed, the
discrepancy is named, and anyone transcribing eq. (7) uses GPa and cites Datchi alongside.
(Second odd printed unit in this paper; no common cause claimed.)

**Hydrogen, eq. (1)** confirms the figure reads to better than 1 % (988.4 K at the 76.3 GPa
maximum; **869.8 K at 130 GPa, 741.6 K at 164** against ≈870 and ≈740 read). **Helium's
equation replaces them**: 1368.2 K at 130 GPa and 1587.1 K at 164, where the figure had been
read as 1180 and 1400 — **12–14 % low against a stated ± 5–7 %.** The surveyor named their own
error bar as optimistic and identified the cause they had already flagged: Fig. 16's axis
labels had to be read from a different crop than the region of interest.

**Effect on the verdict — it strengthens.** Band 1's top corner, previously "5 % below the
line, inside the error", is **18 % below at 130 GPa and 29 % below at 164**. The whole band,
corner included, is solid with room. Band 2's helium margin goes from 1.85× to **2.25×**.

**One limit cannot be closed, and the reason is worth more than the answer.** Eqs. (2) and (3)
— the OCP melting line and the f_WK = 0.7 validity limit — are functions of **density**, not
pressure. Our bands are given in (P, T). Converting needs ρ(P, T), **which is the very table
whose usability at those cells is the open question.** The check requires the object it is
checking. That is the cleanest statement of why this question and the baked-cell count are
two different questions, and it is left undecided rather than forced.

**And counting the baked table turned the second reason false as stated (Brief 29,
2026-09-01).** The reach line's comment gives two grounds; the first was shown not to apply
to a stratified layer, and the second — *"the distributed table's defects are **all** down
there"* — was checked against **our own baked product** rather than the distributed original.

*The two bands were never baked at all.* `KEEP` trims columns per isotherm, and for band A the
kept range stops far short of it; for band B the four isotherms of the fatal point's bicubic
stencil end at 224–794 GPa while evaluation needs 1259 GPa. **The fatal cell is neither
damaged nor sound — it is unbaked**, so the refusal there is the reach line itself, not data.
Sentinels in the baked table: **zero** — all seven sit in trimmed columns. That is registered
branch ④, and it makes *"the table is damaged there"* the wrong sentence: **we did not bake
those cells.**

*But 72 clamped cells survive the bake, and 70 of them sit **above** the line* — inside the
region we use. Reproduced by the directing seat over the baked arrays: 5495 cells kept, 72
with `grad_ad` pinned, **70 above the reach line, 2 below**, every one of them at the **0.1**
clamp end and none at 0.5. The block runs **≈18–112 GPa × 1585–3981 K** — the molecular-to-
atomic transition band, near where Gupta+ 2025 place the fluid structural transition. So the
second reason holds for the sentinels and for the cold pinned mass, and **fails for one block
that lives in the used domain**.

**Tested, and the answer is the uncomfortable middle (Brief 30, 2026-09-01).**

**Contact is universal.** A stencil hook reproducing the baked bicubic's clamped 4×4 was run
over 22 converged points: **every published number in this row reads clamped stencils.**
Anchors **12.1 % (Uranus) / 18.5 % (Neptune)** of envelope `grad_ad` lookups, contact zone
22–37 GPa · 2359–2624 K — the middle of the block. **The rock-axis end B behind C13's
26 % / 41 % : 20.7 % / 26.2 %.** Ice ends 13.2–20.2 %, the whole gradient grid 13.6–20.1 % — **the grid figures reproduced by
the directing seat on the preserved runner, all fourteen points, range identical**.
Branch ① is out. (The first attempt returned zero lookups from a declaration slip in the
runner's own setup; it was discarded and re-run rather than reported.)

**Propagation says the answers hold — with one quantity at the edge.** All 72 cells were
replaced by in-isotherm linear interpolation behind a non-committed hook and **both anchors
were re-solved** — the propagation test that Brief 28's point measurement could not stand in
for.

| | Δλ | ΔR | ΔT_c |
|---|---|---|---|
| Uranus | +9.3e-6 | +9.0e-6 | **+3.41e-4** |
| Neptune | −4.3e-5 | +2.9e-5 | +1.43e-4 |

Against the anchors' own reproducibility (3.7–3.9e-4): λ and R sit 10–40× below it, and
**T_c sits at 0.87–0.92× — inside, but against the wall.** Branch ③ did not fire and
**`--refresh` was not run anywhere**, which is the right instinct: re-freezing on a
substituted table would make the substitution the reference.

**What this does and does not establish, kept together.** It establishes that our published
numbers do not move under *this* substitution. It does **not** establish distance from the
unpublished true values — **the replacement is our own interpolation, not truth**, so this is
a sensitivity to one substitution and not an error bar. And **we are reading clamped values**,
which the answers surviving does not undo: a colder-starting or higher-Z body sits deeper in
the block, and the same test could come out differently. The two runners
(`clamp_contact`, `clamp_propagate`, ~3 min together) are preserved for exactly that re-check.

**Still open, and it belongs to the figures rather than the code**: whether the original clamp
is conservative or violent at those conditions — the block sits in the molecular-to-atomic
transition band, near where Gupta+ 2025 place the fluid structural transition.

*The follow-up as first opened*: the notes' own table has a 60 K-start adiabat passing 100 GPa
at ≈2371 K, which puts a cold-start ice-giant profile **inside the stencil reach of those
pinned rows**. **Whether our anchor integrations read stencils containing a clamped node is
not known and is checkable.** If they do, the adiabatic gradient at those steps is a clamp end
rather than a published value. Verdict-changing if true; opened as its own item rather than
folded in here.

*What was named and not guessed*: **Chabrier's Fig. 1 and Fig. 16**, read as
(log T, log P) coordinates. If the cells we hit lie inside the solid-H/He region, the wall is
physics and the gradient path is wrong there; if they lie merely below our adiabatic cut, the
numbers exist and the question becomes whether the sentinel and clamped cells actually touch
them. The surveyor **did not guess** — the figures are not in the cached text, and the
hydrogen melting curve was not recalled from memory to decide it. Second candidate, unmeasured
because this survey was scoped to literature: whether the damaged cells overlap the two bands
at all (the notes put sentinels at 500–710 K · 8–225 GPa and the clamp at T ≤ 3550 K — the
latter covers both bands).

*And the target passes by a different trade, not a wider table.* Vazan & Helled use **SCvH
(Saumon+ 1995)** — a semi-analytic free-energy model that returns a number everywhere by
construction — while ours is a simulation-assembled table with declared holes. Chabrier 2019
contains SCvH as its own low-temperature component and then spends several sections on where
SCvH disagrees with QMD. **Not a better table: a different bargain.**

**What this leaves the owner.** A gradient that reaches the numbers exists; a gradient that
reaches them *and* resembles the profiles Vazan found workable does not. Two ways forward,
both declarations of their own: **(a)** find or derive an actual stability cap — this recipe
has never had one, and route A turned out to be a family resemblance rather than a criterion —
or **(b)** widen the declared family to `z_shallow > 0`, which **is Vazan's own successful
shape**, and measure again. (b) is the cheaper honesty: it tests our recipe against the
literature's geometry instead of re-drawing a line around our own answer. Fitting the width
to the observables would have produced 39.7 % / 60.0 % and no way to know this — which is
what the method was chosen to prevent.

**Closed 2026-09-01 as a named refusal — the ending the audit proposed and the owner chose.**
`conv=False` reads as *"the solver could not"*; the measurements say something stronger and
addressable, so this row ends the way C6's ceilings do: **with a mechanism and a citation, not
a shrug.**

*The deficit is real and stands*: −15.8 % / −11.4 % after the radius is stripped, against
N13's gravity-constrained λ.

*Three axes were measured, and each stops somewhere this recipe can point at.*

| axis | where it stops |
|---|---|
| **declared rock, redistributed** | Reaches 26 % / 41 % of the gap on the published table — **and that bracket does not exist on the repaired one** (Brief 31). The axis's own ceiling is real; its size is a table choice. |
| **declared ice, uniform envelope Z** | Not measurable. Every bracket end refuses — first at the water wedge (1102 of 1202), then, once IF97 filled it, at `h_he`'s declared reach line. |
| **composition gradient Z(x)** | Built, general, continuous with the layer stack to the bit. Clears the wall the uniform end died on. **The widths that move λ lie outside the geometry Vazan's successful models share**, and the family that does share it (`z_shallow > 0`) cannot reach a 76 K surface at all. |

*And the wall the last two share is now identified to the cell.* It is **our own declared
reach line**, not a source limit — `log T ≥ 2.7198 + 0.2567 log P`, reproducing every measured
floor point. Its stated reason (*"a convecting envelope does not reach"*) **stops applying to
a stratified gradient**, which transports by conduction and is sub-adiabatic by construction.
**But a second limit sits in the same place and does not care whether the layer convects**:
Chabrier's Fig. 1 and Fig. 16 put both bands inside the forbidden region, **helium binding
where hydrogen would have allowed it**, under captions that read *"The EOS must not be used
beyond these limits."* Confirmed by arithmetic on the printed equations, once eq. (7)'s unit
note was shown wrong against Datchi+ 2000.

**So the refusal is chosen, named and cited** — which is this list's definition of finished.
What is *not* claimed: that a fuzzy core cannot account for the deficit. What is claimed is
that **this recipe cannot decide it**, and exactly why.

*Left on the table for whoever reopens it*: the ice mantle's own density profile — the one
named candidate never measured; the unpublished `grad_ad` behind the 66 repairable clamps,
which only the original authors hold; and whether the clamp is conservative or violent in the
molecular-to-atomic band.

### C37 — `rotation_period` under three spellings, and a `None` nobody noticed — **listed 2026-09-06**

`dynamo_rocky` asks `state.get("rotation_period")`; bodies declare `rotation_period_h`;
`chain.yaml` names the node's output `rotation_period`. Measured on Luhman 16 A: the declared key is
`rotation_period_h` = 6.94, and `state.get("rotation_period")` returns **None**. So every body has been
handing the rocky ladder a rotation period of `None`.

**It is a one-line bug, not a schema decision.** The sibling `dynamo.py` already reads
`state.get("rotation_period_h")` and works — the answer exists in a module that runs. What is left over
is the graph label, a third spelling of the same field.

⚠ **Nothing has been wrong in any verdict, and that is the uncomfortable part.** `rotation_period_h`
has no consumer inside `dynamo_rocky` — it appears in the signature, in the recorded inputs, and in the
call, and no branch reads it. So the engine has been writing `"rotation_period": None` into its own
evidence record for every body and **emitting no signal at all**, because nothing depended on it. The
first person to be misled would be someone auditing that record later.

**Not fixed here, deliberately.** It landed in the middle of Brief 121, and folding a schema repair
into the placeholder commit would have meant the wiring and a value changed together — exactly what the
A/B for C36 exists to avoid.

### C39 — one tidal quality, two ways of getting it — **closed 2026-09-06**

`tidal_heating` takes `k2_over_q` as a **per-body declaration** and the boards carry values;
`tidal_locking` uses the **class band** `Q/k₂` 10²–10³ that its document prints. Same physical
quantity, two sources, so **two nodes can look at one body and see different numbers**.

The values make the point. Hades declares `k₂/Q = 1e-3`, i.e. `Q/k₂ = 1000` — the top of the class
band. **Dante declares 0.0155, i.e. `Q/k₂ = 64.5` — below the band's floor.** ⚠ And it misses on the
same side as Venus: both want a body that dissipates *more* than the class allows. For a tidally
molten moon that is physically reasonable, which is the uncomfortable part — **the class band does not
describe our own roster**, and Venus is then not an isolated failure of that band but the second
instance.

**The shape it took**: whatever was declared wins, and the class band is the fallback — the same
pattern `ω₀` acquired in C36/brief 124. The inversion lives at one named function so the direction
cannot be lost between the two nodes, and the output carries `q_over_k2_source`, which says in words
which of the two the verdict stood on.

**Why it was worth doing, which is not tidiness.** The class band's *ceiling* is the uncertain end,
and it was deciding a verdict on its own. Holding everything else fixed and moving only that ceiling:

| `Q/k₂` ceiling | consistency-window floor | this code's 5 h default |
|---|---|---|
| 500 | 2.30 h | passes |
| **1000** (the document's) | **4.60 h** | **passes, by 8.8 %** |
| 1500 | 6.89 h | ⚠ excluded |
| 2000 | 9.18 h | ⚠ excluded |

**The 5 h default is excluded if the ceiling is under 10 % higher than the printed one** — and the
document prints `~10³`, with the tilde, so no tighter statement is available. A number nobody has
measured for our bodies decides the answer, and it decides it within its own printing error. Every
body that declares its own `k₂/Q` is one body that no longer rests on it.

**What moved on the boards: nothing.** Measured before and after on the two roster bodies that
declare a tidal quality, at the board's own mass and radius:

| body | declared `k₂/Q` | `Q/k₂` | τ before (class band) | τ after (declaration) | verdict |
|---|---|---|---|---|---|
| Dante | 0.0155 | 64.5 | 0.0315–0.315 yr | 0.0203 yr | 1:1 → 1:1 |
| Hades | 1e-3 | 1000 | 0.288–2.88 yr | 2.88 yr | 1:1 → 1:1 |

Against a 5.3 Gyr age, both are decided by the `a⁶` gate with nine orders of magnitude to spare, so
the declaration moves `τ` and moves no verdict. **That is the finding, not a null result** — the
before-and-after was run precisely because a flip would have moved a board value the owner has already
approved, and it is recorded so the next person does not have to re-run it to find out.

⚠ **What the same table shows and the verdict column hides.** Read the two `τ` columns again:

    Dante   0.0315 – 0.315 yr   →   0.0203 yr
    Hades   0.288  – 2.88  yr   →   2.88   yr

**Wiring the declaration turned `τ` from a band into a point, and that point's uncertainty is now
carried nowhere.** Physically it follows — a declaration is one number, so the result is one number —
but Dante's 0.0155 is not a measurement: the board says in its own words that it is *"fitted rather
than predicted"*. While the class band ran, not knowing showed up as a width. It no longer does. **That
is not a cost of this change so much as a thing this change made visible**, and it is C40.

⚠ **Wiring `k₂` from the interior solver is only half a route.** `k₂` follows from structure, but `Q`
is rheology, and Barnes writes that the *"tidal dissipation rate is poorly constrained"*. And the
solver computes neither rigidity nor `k₂` today. A separate item, not this one.

### C43 — a disc criterion on a moon, fed by a silent default — **listed 2026-09-07, not started**

Brief 127 asked for something that sounded mechanical: `bindings.yaml` names `semi_major_axis_au` and
the bodies declare `semi_major_axis_km`, so unify them at one named conversion, the way C39 unified
the tidal quality. **The conversion does not exist**, and finding out why turned up something larger.

**The two names are not one quantity in two units.** `bodies/pandora.yaml` declares `kind: moon` with
`parent: Alpha Centauri A b`, so its `semi_major_axis_km` is the orbit **around its planet** — the same
file's `perturber_mass_earth: 120.0` (Polyphemus) confirms which body it orbits.
`body_class`'s `semi_major_axis_au` is the distance **from the star**: its only consumer is
`pebble_isolation_mass`, `body_class.py@«Lambrechts & Johansen 2014 의 페블 고립질량»`, which asks where
in the **protoplanetary disc** a core grew. One key, two frames — and a moon's planetocentric axis
cannot produce a heliocentric distance, because that number belongs to the parent and is not in this
file.

⚠ **What the attempted conversion would have done**, measured before anything was edited:

| `semi_major_axis_au` | pebble isolation mass | boundary verdict for Pandora at 0.6447 M⊕ |
|---|---|---|
| absent → 5 AU default | 20.000 M⊕ | `BELOW` [analog] |
| 252 393 km → 0.001687 AU | 0.00215 M⊕ | ⚠ `INSIDE` [judgment] — stops narrowing |
| moon, boundary skipped (the fix) | — | `INSIDE` [judgment], and it says why |

⚠ **Correction to this row, made after the fix was written.** An earlier draft of this section, and the
message that reported it, called the converted case `ABOVE`. **It is `INSIDE`.** The mass does clear
the isolation mass, but the next gate asks whether it also exceeds twice the maximum core mass
(50 M⊕), and 0.6447 does not — so the boundary returns "no published criterion separates this range"
rather than the opposite verdict. **The error was computing `m_iso` by hand and inferring the branch
from it instead of calling the function**, which is the same defect this file records elsewhere under
a different name. The direction of the finding is unchanged and its size is smaller: the boundary stops
narrowing and its grade drops from `analog` to `judgment`.

**The emitted class does not move** in any of the three — all give `rocky`, `decided_by=radius valley`,
`grade=calibrated`, because that boundary settles Pandora first. **That is luck, not safety**: a
slightly larger moon surfaces it, and even here the wrong reading would sit underneath a correct
answer.

⚠ **The bigger finding is not the naming.** Strip the conversion away and the code still applies a
disc-formation criterion to a moon — and, lacking the distance, fills it in:
`body_class.py@«a = semi_major_axis_au or PEBBLE_ISO_REF_AU»`. **A moon did not grow by accreting
pebbles in the protoplanetary disc**, so the question is not merely being asked with a wrong number;
it is the wrong question for this body, answered from a quiet 5 AU that nobody wrote.

**Three routes, all the owner's**:
1. A moon inherits its parent's `semi_major_axis_au` — the chain already has `scope: parent` edges for
   exactly this shape.
2. `body_class` does not evaluate the pebble-isolation boundary for a moon at all, which may be the
   physically right answer rather than a workaround.
3. Split the names, so the frame is in the name: planetocentric axis versus stellar distance. The most
   honest, and a rename, which is why it was not started at night.

### Resolved 2026-09-07 — route 2, and the naming question dissolves with it

**Owner decision: a satellite does not take the pebble-isolation branch.** Inheriting the parent's
distance was rejected because it still applies a *stellar*-disc criterion to a body that did not form
in the stellar disc.

**What the literature gives, and neither path uses a distance from the star.** Earth's Moon comes from
a giant impact — Canup & Asphaug 2001,
[`2001Natur.412..708C`](https://ui.adsabs.harvard.edu/abs/2001Natur.412..708C) — and the Galilean and
Saturnian systems accrete in a **circumplanetary** disc fed during the giant's own gas accretion —
Canup & Ward 2002, [`2002AJ....124.3404C`](https://ui.adsabs.harvard.edu/abs/2002AJ....124.3404C),
now held. **The disc that matters is the planet's, not the star's.**

`_ice_giant_vs_gas_giant` now returns `INSIDE` with that reason for a satellite, and the recipe passes
`is_satellite=(state.kind == "moon")`. A declared `gas_mass_fraction` still answers the boundary, since
that is a statement about composition and carries no frame.

⚠ **And the `semi_major_axis_au` / `_km` question closes with it.** If a moon never consumes a stellar
distance, there is nothing to fill that key with, and the "which spelling is canonical" question has
no subject. It was never an independent decision.

### The satellite mass budget — recorded, nothing changed

Canup & Ward 2006, [`2006Natur.441..834C`](https://ui.adsabs.harvard.edu/abs/2006Natur.441..834C):
a gas planet's satellite system holds *"a similar fraction of their respective planet's mass
(~10⁻⁴)"*. ⚠ **Read from the ADS abstract, not the paper** — it is not held.

Against Polyphemus at 120 M⊕, from the board's own masses:

| body | board mass | M⊕ | fraction of planet | vs 10⁻⁴ |
|---|---|---|---|---|
| Pandora | 3.850×10²⁴ kg | 0.6447 | 5.37×10⁻³ | **53.7×** |
| Cassandra | 9.000×10²³ kg | 0.1507 | 1.26×10⁻³ | **12.6×** |
| Hades | 5.000×10²¹ kg | 0.0008 | 6.98×10⁻⁶ | 0.1× |
| Dante | 1.552×10²¹ kg | 0.0003 | 2.17×10⁻⁶ | 0.02× |
| Chaos | 5.400×10²⁰ kg | 0.0001 | 7.53×10⁻⁷ | 0.008× |
| **system** | 4.757×10²⁴ kg | 0.7965 | 6.64×10⁻³ | **66.4×** |

**All five are exempt and no value changes**, and the reasons are not the same for all five:

- **Pandora** — the source material fixes it. *"아바타는 설정이 그러니 그대로 두고 기록만"* (owner).
- **Cassandra** — **owner decision, 2026-09-07**: *"카산드라도 면제 및 기록."* A 13× reduction would
  falsify already-approved prose about its surface gravity and density.
- **Hades, Dante, Chaos** — already inside the convention. **There was never anything to exempt.**

⚠ **Two things this table must not be read as saying.**

1. **10⁻⁴ is a budget for the whole system, not a cap per moon.** Singling Pandora out as the body
   that breaks it is **our construction** and appears nowhere in the paper; what the paper constrains
   is the 66.4× on the bottom row.
2. **The scaling is stated for gaseous planets**, and the same abstract says the fraction is *"two to
   three orders of magnitude smaller than that of the largest satellites of the solid planets (such as
   the Earth's Moon)"*. It applies here because Polyphemus is a gas giant — which the engine derives
   independently — and would not apply around a rocky primary.

⚠ **The abstract also names our case directly**: the mechanism *"could limit the largest moons of
extrasolar Jupiter-mass planets to Moon-to-Mars size."* Pandora at 0.6447 M⊕ is well past Mars. **The
exemption is a decision made against a stated expectation, not in the absence of one**, and that is
why it is recorded rather than quietly allowed.

**Going forward**: newly invented moons follow the scaling. The existing five are not revisited.

**Nothing was changed.** The measurement above is the whole of the work.

### C37 — one lookup, four names, and a contract check that could not see it — **closed 2026-09-07**

⚠ **First, a correction: there were two spellings, not three.** This file previously counted
`rotation_period_days` among them. It is not a declaration — `bodies/luhman_16_a.yaml` reads
`rotation_period_h: 6.94    # DB rotation_period_days 0.2892`, a comment preserving the source value
next to the converted one, and **no code reads it**. The 24× hazard that name implied never existed.

**The real defect was one lookup.** `dynamo_rocky` read `state.get("rotation_period")`; every supplier
writes `rotation_period_h` — three body files, the sibling `dynamo.py`, and `tidal_locking`'s own
output. So the recipe received `None` **on every body, always**, and wrote that `None` into its
evidence record.

⚠ **Why nothing noticed, which is the part worth keeping.** `check_contracts` compares the document's
`Needs` against `set(result.inputs)` — **the labels a recipe attaches to its evidence, not the keys it
looked up.** `dynamo_rocky` labelled the value `"rotation_period"`, the contract said
`rotation_period`, they matched, and the lookup string was never examined. **A recipe can read a key
nobody supplies and stay green indefinitely, as long as it files the resulting `None` under a name the
contract knows.** That is the mechanism, and it is not specific to this node.

**So the repair is four sites, not one** — otherwise the same trap stays open for whoever reads the
contract next:

| site | was | now |
|---|---|---|
| `dynamo_rocky` lookup | `state.get("rotation_period")` | `state.get("rotation_period_h")` |
| its evidence label | `"rotation_period"` | `"rotation_period_h"` |
| contract Needs (en + ko) | `rotation_period` [h] | `rotation_period_h` [h] |
| `chain.yaml` outputs label | `rotation_period` | `rotation_period_h` |

With label and lookup now one string, `check_contracts` actually covers this node.

**What changed in the answers: nothing.** Measured on Pandora, the only roster body that both reaches
the rocky ladder and has a rotation period to give (32 h, from `tidal_locking`): every emitted value is
identical — `b_eq` 41.3725 µT, `ladder_regime` 1, `dynamo_alive` alive, the same `rossby_verdict`.
Only `inputs` moves, from `None` to 31.999 h.

⚠ **That is not a reason to call the repair empty.** The engine wrote `"rotation_period": None` into its
own evidence for every body it ever judged, and the first person to reconstruct a verdict from that
record would have been reading a lie. **A test now fails if the lookup regresses**, since nothing else
would notice: verified by reverting the key and watching it go red.

### C63 2026-09-10 — the cold φ(P) slot stays empty, and that is the answer — **a named refusal, no code changed**

⚠ **Nothing moved.** `engine/porosity.py` keeps every constant it had, `voids_expected` keeps its three
indicators, and the Dante fixture keeps `φ₀ = 0.3890625` bit for bit. **The output of this stage is a
refusal with a name**, and the name is: *the seven compaction papers held on 2026-09-10 do not print a
cold, unsintered φ(P) law over our slot's range — 1 MPa to 764 MPa — so there is no basis in this set for
moving `P_LAB_MAX` or the rock law.* Source: `P29-porosity-compaction-prereg.md` (parallel seat), sha256
`8884e29ae2832870…`, **16563 B**, in `~/Desktop/NearStars-artifacts/2026-09-09-c20-entropy-band/`, hashed
here. ⚠ *The relay quoted this file as `c999b544…`. The file on disk hashes to the value above, its mtime
is 16:37, and the directing seat confirmed (2026-09-10) that `c999b544…` is the version **before** the
parallel seat replaced its roster sentence this evening. The disk version is what this line is written
against, and it is the one cited.*

**Why it is a refusal and not a gap.** The seven do carry compaction laws, and each one is a law about a
different thing:

- **Four cover a pressure range that ends below our floor.** Weidling+ 2009, Güttler+ 2010, Henke+ 2012
  eq. 15 and Kataoka+ 2013 are dust- and fluffy-aggregate laws that are already **saturated at 1 MPa** —
  Henke 0.420 and Güttler 0.423 at 10⁶ Pa, flat above; Kataoka's form reaches ρ = ρ₀ at **0.47 MPa**. Our
  rock law's floor *begins* where theirs end.
- **Two are rate laws, not φ(P).** Gail+ 2015 and Henke+ 2016 close pore space by **temperature and
  time** — hot pressing validated at 16.6–29.1 MPa and 1433–1624 K — so they need a thermal history and
  return φ(P, T, t). ⚠ **That is a different quantity from the one the slot holds**, and substituting it
  would be C58 (a)'s mismatch again: the right form asked at the wrong state.
- **One is shock, not lithostatic.** Bland+ 2014 prints 16 iSALE runs at 0.75–3 km s⁻¹ and no φ(P) law at
  all. Its one usable line is a **citation**, not a measurement: *"~1 MPa at the centre of a 100-km radius
  asteroid"*.
- **The law the code already uses is not in the seven.** Bierson+ 2019 is held as text only, its
  b-coefficients are fitted over **30–80 MPa** (Yasui & Arakawa) and Durham+ 2005's 150 MPa is where
  `P_LAB_MAX` comes from — and **Dante's centre is 317 MPa**, above every cold law in the held set and
  above the lab range of the one we ship.

⚠ **And five of the seven name the mechanism our three indicators do not have.** Henke 2012/2016, Gail
2015 and Bland close the pore space of a 100–170 km body by **²⁶Al radiogenic heating above ≈ 700 K**, not
by lithostatic pressure. Our `voids_expected` fires on mass, grain-fracture pressure and a declared tidal
bool — *"tidal" appears 0 times in all seven papers*. So the indicator set is not merely coarse; **it is
indexed on a different cause than the one the literature uses at this body scale.** That is a finding, and
it is recorded as owner-pending candidate (d), not built.

**Owner-pending, none taken** (P29's own table, relabelled): (a) a second cold rock law as an option or as
documented contrast · (b) `P_LAB_MAX` one scalar or per-law (150 / 30–80 / 1 / 764 MPa) · (c) which φ₀
family the rock inversion axis may land in (0.60 · 0.36–0.44 · 0.248 · free, today 0.389) · (d) ²⁶Al
sintering as a fourth declared-bool indicator · (e) the Dante/Hades radius question, **already pending and
unchanged**. ⚠ **None is urgent**, and (d) is a candidate only — no printed body-independent form for it
exists in the held set.

**What this refusal costs, stated plainly.** The inferred-porosity axis keeps running on one law whose
fitted range covers **a quarter of Dante's pressure column** (34.0 % of that body's mass sits above the
150 MPa cap). ⚠ *That is not a defect this stage may repair* — repairing it means electing a law, and
every candidate in the held set is either saturated three decades too low or needs a thermal history the
node does not receive. **Carry 2012 and Consolmagno+ 2008 stay unheld**, so indicator 1 stays
second-hand. The next move belongs to the owner, or to a paper we do not have.

### C47 — the table is fed radiogenic production, and its thresholds are defined on surface heat flow — **measured 2026-09-07, not fixed**

**The question this answers is not "which end", it is "why half".** The low feed gives Earth
41.80 mW/m² where the measurement is 92.1. A factor of two does not look like an inaccuracy, and if a
term is missing then it is not something to choose between — it is something to fill.

**What the code is actually fed, read from `chain.yaml` rather than assumed.** `heat_transport_mode`
has exactly **two** incoming `requires` edges: `tidal_heating` → `surface_flux` and
`internal_heat_nontidal` → `radiogenic_power`. The second edge's own note says the judgement is made
on *"the whole radiogenic output (l_int = radiogenic_power) plus the tidal flux"*. **There is no
secular-cooling edge, and no node in the chain emits such a value.**

**What the thresholds are defined on, from both papers.** Reese+ 1998: *"the critical **heat flux**
which can be removed without widespread melting"*. Lourenço+ 2020 §4.3: *"the **total surface heat
flow** (i.e., the sum of magmatic and conductive heat flows)"*. Both are surface heat flow. So the fed
quantity and the threshold quantity are not the same physical quantity.

**Two bodies, measured.** Earth alone cannot settle this, because Earth is the only body with a
measured surface flux sitting beside our number.

| body | our low feed | that body's **radiogenic production** | ours ÷ radiogenic | that body's **surface heat flow** | ours ÷ surface |
|---|---|---|---|---|---|
| Earth | 41.80 mW/m² = **21.32 TW** | Korenaga 2008 §41: BSE **16 ± 3 TW**; §2's sketch says *"about 20 TW"* | **1.33×** (1.12–1.64 across 13–19 TW); **1.07×** against the sketch | Davies & Davies 2010: **47 ± 2 TW** = 92.1 mW/m² | **0.45×** |
| Mars | 15.87 mW/m² | Parro+ 2017: **14.3 mW/m²**, Wänke & Dreibus composition | **1.11×** | Parro+ 2017's own model: **19 mW/m²** (range 14–25) | **0.84×** |

⚠ **Corrected 2026-09-24 (prereg-radiogenic, `12afb7f8`) — the table stays as written:** the engine now feeds Earth 21.75 TW (0.04263 W/m²) and Mars 12.14 mW/m², so Earth ÷ Korenaga 2008's 16 TW is 1.36× (not 1.33×) and Mars ÷ Parro+ 2017 is **0.85×**, not 1.11× (1.19× on the 09-23 tree). The other cells that divide by the engine's radiogenic production move with it: Earth «1.12–1.64 across 13–19 TW» → **1.14–1.67**, «1.07× against the sketch» → **1.09×**, surface «0.45×» (÷ 47 TW) → **0.46×**; Mars surface «0.84×» (÷ 19 mW/m²) → **0.64×**. The row this correction belongs to is C47 in `interior-core.md`.

⚠ **Verdict: (b) — a different quantity, not an inaccurate one.** It agrees with radiogenic production
on both bodies to within 11–33 % and misses surface heat flow by factors that differ *between* the
bodies. An inaccurate surface flux would miss by a similar factor on both.

**⚠ Which is why no multiplier is allowed here, and the reason is quantitative.** The gap between the
two quantities is the **Urey ratio**, and it is a property of the body:

| body | Urey ratio, and whose | `1/Ur` |
|---|---|---|
| Earth | **0.35**, Korenaga 2008's bulk-Earth value (= 16/46 TW, which this seat reproduced by arithmetic); our own 21.32/47 gives 0.454; his **convective** Urey ratio is 0.23 ± 0.15 and is a different quantity again | **2.2–2.9** |
| Mars | **0.68–0.75**, Parro+ 2017 (0.715 at 20 mW/m²); convective-history models give 0.52–0.62 and 0.594 ± 0.024 | **1.3–1.5** |

**A single constant cannot serve both**, and the two bodies we can check are the two that disagree most.
Multiplying Earth by ~2 to seat it at 90 mW/m² is the exact defect class this ledger spent 2026-09-07
removing.

**What the missing term is, in the source's words.** Korenaga 2008 §2: *"Loss of internal energy is
balanced primarily by (1) heat production from radiogenic elements and (2) a decrease in the primordial
heat content of Earth (i.e., secular cooling)… Other energy sources such as tidal dissipation are
negligible compared to these two processes"*, and *"the present-day internal heat production is about
20 TW …, so the rest of the surface heat flux must be from secular cooling."* Parro+ 2017 says the same
of Mars in the other direction — Ur near 0.7 means *"a relatively small difference between the total
radioactive heat production and heat loss through the surface, and therefore a **moderate** contribution
from secular cooling."*

⚠ **Our own document already names the term.** §6 of `tidal-heating-methodology.md`: *"Note that tidal
heating is one heat source among several (radiogenic, **accretional, primordial**)."* Four sources are
named in our text and the chain feeds two of them. This is not an undiscovered gap; it is an unfilled
one.

⚠ **And that same sentence carries a second defect.** It continues: *"For an Earth-mass body radiogenic
heating alone is ~0.08 W/m²; tidal heating matters when it exceeds that."* The figure is **uncited**,
and it is **2.1× both held estimates** of Earth's radiogenic production (Korenaga's 16–20 TW =
0.031–0.039 W/m²; our own engine 0.0418) while being **87 % of Earth's measured total** (0.0921). It
sits with the totals, not with the components. ⚠ **It is also one of C34's four candidates** — listed
there as *"0.08 §6.1"* — so one of the four values that decision was choosing between is a figure whose
own label is in doubt. Not repaired here; its source has to be found first.

**⚠ What this does to C34's score, and it is not a small correction.** At the low feed Mars passed and
Earth failed. That difference is **not** evidence about the fed quantity — it is a measure of how close
each body's Urey ratio is to 1. Mars's 0.68–0.75 means a radiogenic number fed into a surface threshold
still lands in the right cell; Earth's 0.35–0.45 means it does not. **The 3-of-4 was scoring the Urey
ratio.** Mercury and Venus have no measured surface heat flow, so they cannot even be checked this way.

**⚠ Not fixed, and wider than C34.** The same shortfall applies to **every body this engine feeds**; it
is visible only on Earth and Mars because only they have an independent number beside ours. Filling it
needs a grounded secular-cooling recipe — a cooling rate times a heat capacity times a mass, of the
shape Korenaga's own eq. (8) uses (`C dTi/dt = H(t) − Q(t)`, with `C = 7×10²⁷ J K⁻¹` for the whole
Earth) — not a factor. ⚠ *The `eq. (8)` pointer itself is confirmed, not stale: C47 (b) item 1 shows
C20's mantle equation **is** that equation (`C dT/dt = H − Q` with `C = M_m C_pm`). What was stale here
is the number beside it.* C20 (`core_thermal_history`) already emits `q_cmb_present` **3.745 TW** for
Earth (⚠ **5.07 TW until 2026-09-09** — that was the `H` = 1.5 pW/kg value, and owner decision ⑤ moved
it twice in one day; Briefs 166 D/E),
but that is the core's contribution across the CMB, not the planet's secular cooling, so it does not
close this on its own. **The low/high choice in C34 stays the owner's, and this section exists so that
it is made knowing the low candidate is a different quantity rather than a smaller one.**

### C47 (b) 2026-09-07 — the integrator was opened first, and the two-body condition fails on the ordering

**The instruction was to look before building, and looking changed the answer twice.**

**Answer to the three-way question: (ii) for the cooling rate, and *already an output* for the thing
C47 actually needs.**

1. **C20's mantle equation *is* Korenaga eq. (8).** `engine/core_history.py` line 8 prints it:
   `mantle (eq. 32)   H_m M_m − Q_M + Q_C = M_m C_pm · dT_h/dt`. That is `C dT/dt = H − Q` with
   `C = M_m C_pm`. The integrator has been solving this equation since 2026-09-04.
2. **`dT_h/dt` is computed and not emitted** — the output list carries `dtc_dt_present_k_per_gyr`,
   which is the **core**'s rate. So the mantle rate is case (ii), inside and unpromoted.
3. ⚠ **But promoting it is not needed, because the surface flow is already an output.**
   `q_mantle_present` **is** `Q_M = 4π R_p² F_t`, from `mantle_flux.implied_flux` (Nimmo+ 2004 eqs
   34–36). The quantity C47 was going to build already exists and is already emitted. **Guardrail ①
   (fix `C` from the paper) is therefore moot for this route** — no `C` is used.
4. **Guardrail ③ holds.** `implied_flux(t_m_k, g, r_m)` takes a mantle potential temperature, gravity
   and radius. **No measured surface heat flux enters anywhere**, which is what the guardrail asked.

⚠ **And our own module diagnosed C47 sixteen days ago.** `engine/mantle_flux.py`'s header, written at
Brief 46: *"The implied flow and the radiogenic budget are not required to match; **secular cooling is
the expected difference** (the paper: Earth 'loses heat roughly twice as fast as it is being generated
by radioactive decay')."* That is C47's whole finding, in our own code, citing Nimmo for it — the
**third** independent place this was already written down, after §6's *"accretional, primordial"* and
Korenaga's own §2. The consumer never read any of them.

**The pass condition, measured.** One recipe, `Ur = radiogenic / implied_flux`, no per-body adjustment,
default concentration set:

| common `T_m` | Earth `Ur` | Mars `Ur` |
|---|---|---|
| 1603 K (Nimmo's own printed present-day Earth value) | 0.537 | 0.317 |
| 1700 K | **0.353** — Korenaga's 0.35 almost exactly | **0.209** |
| **published** | **0.35** (Korenaga, 16/46) | **0.68–0.75** (Parro+ 2017) |

**Earth can be landed. Mars misses by 3.4×.** ⚠ **And the failure is in the ordering, which no choice
of `T_m` repairs.** Earth → Mars under this law:

| quantity | Earth | Mars | factor |
|---|---|---|---|
| `δ_t` top boundary layer | 41.1 km | 56.8 km | **×1.38 thicker** (`δ ∝ g^−1/3`) |
| `F_t` | 118.3 mW/m² | 85.7 mW/m² | ×0.72 |
| `Q_M` | 60.4 TW | 12.4 TW | ÷4.88 |
| `H` radiogenic | 21.3 TW | 2.58 TW | ÷8.27 |
| **`Ur = H/Q_M`** | | | **falls ×1.69** |

The literature has `Ur` **rise** ×2.0 from Earth to Mars. **A recipe that reverses the direction is not
off by a constant, and the two bodies we can check are the only two we can check.** To pass, Mars would
need `T_m = 1419 K` against Earth's 1702 K — **283 K colder, chosen because it makes `Ur` come out.**
That is per-body tuning wearing a physical name.

⚠ **Why it inverts, in our own docstring's words.** `mantle_flux.py`: the parameterisation was tuned on
four simultaneous **present-day Earth** constraints — *"the present-day mantle temperature, viscosity
and heat flux"* — plus densities adopted to match PREM. Eight Earth constants ride along (`ρ_m`,
`α_m`, `κ_t`, `k_t`, `η₀`, `T₀`, `ζ`, `Ra_c`), and `T_s = 293 K` is *"the one constant here that is
obviously not the roster's."* **It is a mobile-lid boundary-layer law, and Mars is the archetypal
stagnant lid.**

⚠ **A source already on our own ladder falsifies it outright.** `implied_flux` gives Mars
**85.7 mW/m²** at `T_m = 1700 K`. Reese+ 1998's ceiling for Mars is **15–30 mW/m²** — the very number
that is the bottom of the C46 ladder. So **our own ladder says this law hands Mars 2.9–5.7× more heat
than its lid can conduct without widespread melting.** Meanwhile Parro's measured-model 19 mW/m² =
2.74 TW sits **inside** Reese's 2.17–4.33 TW. The stagnant-lid law and the measurement agree with each
other; the mobile-lid law agrees with neither.

⚠ **A hard blocker on the (i)/(ii) route independent of all of the above.** Only
`engine/bodies/earth.yaml` declares `core_initial_temperature` and
`mantle_initial_potential_temperature`. **C20 cannot run on Mars at all**, so the two-body condition
cannot be scored through the integrator even if the physics were right.

**⚠ And the loop closes on C46.** The right surface flow needs the **regime** — mobile-lid bodies take
Nimmo eqs 34–36, stagnant-lid bodies need a stagnant-lid law — while C46 needs the surface flow to
place the cell. C46 already recorded that flux cannot supply the regime, and that Lourenço's
discriminants are mobility and plateness, both outputs of a 4.5 Gyr simulation. **So C47 is not
blocked on writing code. It is blocked on the same circularity C46 named, and closing one closes the
other.**

**What would actually unblock it, stated as a request rather than a build.** The stagnant-lid
scaling is Reese, Solomatov & Moresi 1998's own subject — *"thermal boundary layer analyses as well as
finite element simulations of stagnant lid convection with non-Newtonian viscosity"* — and ⚠ **we hold
only its abstract; every AGU and ADS scan returns 403.** The abstract prints the two ceilings and not
the scaling law. **Nothing is built here because the half of the physics that Mars needs is in a paper
we do not have.**

**Nothing was changed in the engine by this section.** No node, no edge, no value. Item B of the
brief — no regime name is emitted while this stands — is already the state of the code: `solve_mode`
emits `regime_candidates` and refuses a single regime whenever more than one stands.

### C47 (c) 2026-09-07 — the stagnant-lid law was read, and the mobile/stagnant distinction is not what was breaking C47

**A paper was found on an open route and read from source. It changes the diagnosis, and it does not
close the item.** Korenaga 2009 ([`2009GeoJI.179..154K`](https://ui.adsabs.harvard.edu/abs/2009GeoJI.179..154K)),
*"Scaling of stagnant-lid convection with Arrhenius rheology and the effects of mantle melting"* — same
author as the Urey-ratio review this project already cites for C47's Earth numbers, adjacent year.

**⚠ First correction: the law is not eq. 30.** The brief identified eq. 30 as the scaling law. The
paper's §4 says the opposite in its own voice — *"The boundary-layer stability criterion (**eq. 43**)
is used to calculate `Nu`"* — and describes eq. 30 as *"**the conventional scaling** of `Ra_i^{1/3}`"*
that its results *"deviate considerably from"*. **Eq. 30 is the law this paper argues against.** Its
contribution is that mantle melting *"may reduce the conventional prediction of surface heat flux by up
to a factor of ∼5–10"* (Summary, read in full).

**⚠ Second, and this is the finding: the conventional stagnant-lid law fails the direction test, and
fails it *identically* to the mobile-lid law we already had.** Eq. 30 is
`Nu ≈ a θ^(−1−β) Ra_i^β` with `a ≈ 0.30 + 0.25n` and `β = n/(n+2)`, `Ra_i` from eq. 21 (Arrhenius),
`q = Nu k ΔT / D` from eq. 19. Evaluated with the paper's own constants and **one shared `b`**, at a
common `ΔT` and `T_i`:

| law | Mars/Earth surface flux | `Ur` Earth → Mars | needed |
|---|---|---|---|
| Nimmo eqs 34–36, **mobile lid** (what we had) | **0.724** | falls ×0.59 | — |
| Korenaga eq. 30, **stagnant lid**, `n = 1` | **0.723** | falls ×0.59 | rises ×2.0 |
| Korenaga eq. 30, **stagnant lid**, `n = 3` | 0.557 | falls ×0.77 | rises ×2.0 |

⚠ **0.724 and 0.723 are the same number, and it is not a coincidence.** Both laws put the flux at
`q ∝ g^{1/3} ΔT^{4/3}` for `n = 1`: the boundary layer thickens as `g^{−1/3}`, and **`D` cancels
analytically** out of `q = Nu k ΔT/D` for every `n`, because `Ra_i ∝ g ΔT D^{(n+2)/n}` raised to
`β = n/(n+2)` returns exactly one factor of `D`. **So swapping a mobile-lid law for a conventional
stagnant-lid law changes the Earth→Mars ordering not at all.** The mobile/stagnant distinction was the
wrong suspect — C47 (b) named it as the cause and that was too quick.

**What does carry the direction is the melting correction**, and the paper says so in its own §4.2:
mantle melting *"starts to affect heat-flow scaling at **lower temperatures for Mars than Earth**
because the **low gravity of Mars results in the formation of thicker depleted mantle** for a given
potential temperature."* Suppressing Mars's flux harder than Earth's is exactly the direction `Ur`
needs. ⚠ But that is eqs 41–56 solved iteratively with `z*_D = Nu^{−1}`, not a formula to transcribe —
**it is a build, and nothing was built here.**

**⚠ Third, and it is a harder stop than the direction: this law cannot give an absolute Urey ratio
either, by the author's own statement.** From p. 163, verified on the page image rather than the text
layer:

> *"the pre-exponential factor `b` in eq. (1) is determined so that the surface heat flux is
> **50 mW m⁻²** at the present-day Earth condition … **different planets may take different
> pre-exponential factors** … The purpose of this **(arbitrary) normalization** for mantle rheology is
> to provide a simple reference point and highlight differences caused by mantle melting and the size
> of a planet."*

And the Earth it normalizes to is **counterfactual**: *"Earth does not presently exhibit stagnant-lid
convection … it is convenient to use this familiar planet first to derive a **hypothetical** heat-flow
scaling law, **against which results for other planets may be compared**."* The 50 mW/m² is not
Earth's measured 92.1. **So the absolute scale is free per planet, declared arbitrary, and anchored to
an Earth that does not exist.** Choosing `b` per body to land the two Urey ratios is the per-body
tuning guardrail ④ forbids — with a citation attached, which makes it worse rather than better.

**⚠ The pass condition is therefore not obtainable from this paper.** Not because its physics is wrong,
but because it is built as a **relative** comparison instrument and says so.

**The reserve law was given a qualification check only — not a fit.** Foley & Bercovici 2014
([`2014GeoJI.199..580F`](https://ui.adsabs.harvard.edu/abs/2014GeoJI.199..580F), ⚠ **arXiv eprint; its
page and equation numbers are not the journal's**) was opened for one question: does it carry a
constant fixed by calibrating to Earth? **It does not** — its exponents come from least-squares fits to
its own numerical experiments. And its abstract claims the shape C47 actually needs: scalings
*"across the stagnant lid and plate-tectonic regimes"*, i.e. **a law that does not require the regime
as an input.** ⚠ It has freedom of its own kind (grain-damage material parameters, and it *"treat[s]
the plate length as an unknown"*), and evaluating it is a build. **It was not fitted, and no number was
taken from it**, because brief 145's own warning applies: trying two laws and keeping the one that
lands is per-body tuning wearing two citations.

**The knot, written in both places it binds:** *a correct surface heat flow needs the regime, and placing the regime needs the surface heat flow.* ⚠ **And the stagnant-lid
law does not cut it** — that was the hope this section tested and removed. A law that spans both
regimes would, which is why Foley & Bercovici is the one worth a build if the owner spends one.

**Nothing was changed in the engine.** No node, no edge, no value, no constant transcribed.

### C47 (d) 2026-09-08 — the declared-regime path already exists, runs the other way, and the law contradicts the declaration it would serve

**Guardrail ① asked for a sweep of the grade names before a fifth one was coined. The sweep found the
word already in use, and then found the module that uses it.**

**The vocabulary, swept.** Four axes, and they do not collide:

| axis | words | where |
|---|---|---|
| `Result.grade` | `measured` · `calibrated` · `analog` · `judgment` · `authored` | `payload.GRADES` |
| `Band.value_origin` | `printed` · `chosen` | `bands.py` |
| `Band.pick` | `printed` · `chosen` · `unchosen`, plus `provisional` as a fourth pick word | `bands.py`, `provisional.py` |
| ladder rung origin | `analogy-rung` · `abstract-level` · `held body text` | `tidal_heating.py` |

⚠ **A fifth word is not needed, because `declared` already exists.** `engine/tidal_transport.py` has
carried `mode=dict(value=mode, provenance="declared")` since **Brief 35, 2026-09-01**, on a `provenance`
axis of its own. Coining a grade for declared regimes would duplicate a word this engine has been using
for a week.

⚠ **And the sweep turned up an inconsistency this seat made yesterday**: `REGIME_LADDER`'s third rung
origin is the bare literal `"held body text"` while its two siblings are named constants
(`ANALOGY_RUNG`, `ABSTRACT_LEVEL`). Three origins, two of them named. Not repaired in this section —
recorded so it is repaired deliberately rather than noticed again.

**⚠ The bigger find: D is already built, and it runs the other way.** `engine/tidal_transport.py`,
Brief 35, opens with *"Ė → (internal temperature, lithosphere thickness) under a **DECLARED** transport
mode"* and argues D's exact case — *"수송 모드는 **선언**이고 도출이 아니다"*, citing Kankanamge & Moore
2019 §6 doing the same thing (*"the internal heating rate is chosen to satisfy the observed thermal
emission"*). Its `TRANSPORT_MODES` are `heat-pipe`, `stagnant-lid`, `plate-tectonics`.

But three things separate it from what D needs:

1. ⚠ **The flux is an INPUT, not an output.** It takes `surface_flux_wm2`, sets `H = F_s / D`, and
   returns internal temperature, lithosphere thickness, and the melt/conductive **split** of the flux it
   was given. **Flux in, state out.** D asks for regime in, flux out — the opposite direction.
2. ⚠ **Only `heat-pipe` is solved at all.** `stagnant-lid` and `plate-tectonics` return
   `internal_temperature=None` with the module's own note that other modes are *"§6.2의 용량 사다리로
   판정만 한다"* — judged by the ladder, not converted. **The two regimes C47 needs are the two it does
   not solve.**
3. ⚠ **Its verification status is `failed-io-reproduction`, and its numbers are marked 채택 금지.** The
   transcription is verbatim and solves to ~10⁻¹⁴ residual, but Kankanamge & Moore 2019 cannot reproduce
   its own printed Io result (1471 K, 12.6 km) from its own printed constants; back-solving the constants
   that make it a root gives `α = 8.71×10⁻⁷ K⁻¹` — **1/34 of rock's** — and `ΔT_rh = 354 K` against a
   rheological scale of 40–100 K.

**The `b` question, answered — and the answer is what stops D.** Guardrail: an absolute flux from the
declared path needs `b` fixed, or the regime refuses flux. **It can be fixed**: take Korenaga 2009's own
`b`, re-fitted on the paper's own printed Earth condition using the paper's own printed constant list
(including its `α`, self-consistently — see paper defect #24), as **one global declaration** for every
body. That is not per-body tuning; it is the same shape as `mantle_flux`'s `T_s = 293 K` or
`radiogenic`'s `MANTLE_SHARE = 0.70`, both of which are Earth's numbers declared for every rocky body.
⚠ Its width is **unquantified by the paper** — *"different planets may take different pre-exponential
factors … grain size and mantle composition"*, with no range printed — and `q ∝ b^{−β/n}`, so a decade
of grain size is **2.15×** in flux at `n = 1`.

**⚠ But at that normalization the law contradicts the declaration it is being asked to serve.**

| body declared **stagnant-lid** | eq. 30 flux | against Reese's stagnant ceiling 10–30 mW/m² |
|---|---|---|
| Earth-size | **50 mW/m²** (by construction) | **1.7× the top, 5.0× the bottom** |
| Mars-size | **36 mW/m²** | **1.2× the top, 3.6× the bottom** |

**Declare "stagnant lid", compute the flux, and C46 answers that the body cannot be a stagnant lid.**
The declaration and the law disagree, so D's flux path would emit a value that its own consumer
rejects. That is not a number worth emitting.

**⚠ And the repair is in Korenaga, not in Foley & Bercovici — which is the reason to stop and report.**
The paper's advertised contribution is that mantle melting *"may reduce the conventional prediction of
surface heat flux by up to a factor of ∼5–10"*. Apply that:

⚠ **Corrected 2026-09-08, same seat, a few hours later — the table below originally read the ÷5–10 as
a two-sided interval and it is an upper bound.** The paper's words, in both places it says this
(Summary and §5), are *"could reduce the conventional prediction of surface heat flux **by up to** a
factor of ∼5–10"*, and it is prose summarising Figs 12–13, not a printed range of computed values. **A
reduction of *at most* 5–10× means the reduced flux lies somewhere in `[q/10, q]`** — it does not mean
the flux is `q/10` or `q/5`. Reading "up to X" as an interval and then taking its ends is the same
error class as C46's ceiling-used-as-floor, made by this seat hours after repairing that one.

| body | eq. 30 | what the paper's *"up to ∼5–10"* actually licenses | ceiling 10–30 |
|---|---|---|---|
| Earth-size | 50 | somewhere in **5.0 – 50 mW/m²** | **may** reach it; not delivered |
| Mars-size | 36 | somewhere in **3.6 – 36 mW/m²** | **may** reach it; not delivered |

**So the melting correction permits the ceiling to be satisfied and does not deliver it.** The
conclusion below survives — Korenaga is the remaining candidate and C47 (c) tested the wrong equation —
but it survives as *the only unexhausted route inside this paper*, not as a route already shown to
land. ⚠ **Korenaga 2009 is not exhausted: C47 (c) tested only the law the paper argues *against*.**
Eq. 43 with
the melting correction (eqs 41–56, solved iteratively with `z*_D = Nu^{−1}`) is the paper's actual law,
and it is the single build that serves **both** open paths — D's flux output, and the direction test
that C47 (c) ran on the wrong equation.

**Nothing was built, and nothing in the engine changed.** Per brief 146's own instruction: a reason
appeared to change the order, so this stops here. **The proposed order is: Korenaga eq. 43 + melting
first** (it serves D and re-runs A's test on the right equation), with Foley & Bercovici held as the
genuinely independent third family for the pre-registered "three families, same direction" verdict.

⚠ **Closed 2026-09-08 by a fourth family, not a third.** Korenaga eq. 43 with melting was built (C47 (e)
→ (k)) and it fails in the same direction as the other three: `q_E/q_M` reaches **1.5114** against the
**3.68 / 4.78** the Urey ratios need. **So the verdict this note was waiting for is in, and Foley &
Bercovici was never needed to reach it** — four families, one direction. *(C47 (g)'s cell calls this
"the note in C47 (c)"; it is this paragraph, in C47 (d).)*

### C47 (e) 2026-09-08 — the law was read before building, and the build is C20-sized

**Brief 147 put one step in front of the build: read, size it, then decide. This is the size.**

**The chain, counted.** Korenaga 2009's actual law is not one equation:

| what | equations | note |
|---|---|---|
| Arrhenius correction to `θ` | 39, 40, **41** | `θ_eff = (c₁c₂)^{1/2}`, a geometric mean of two correction factors, *"c₁ tends to be too low for higher n whereas c₂ too high"* |
| local Rayleigh number | **42** | `Ra_l(δ) = Ra_i · max[ δ_eff^{(n+2)/n} T*_eff / η*_eff ]` — a **maximum over sublayers**, with `η*_eff` a **logarithmic average** |
| stability criterion | **43**, 44 | `Ra_l(δ) = Ra_crit(n)`, `Ra_crit(n) ≈ exp(3.84 + 2.25/n)`; `Nu = δ^{−1}` |
| dry solidus | **45** | `P₀ = (T_p − 1150)/100`, Takahashi & Kushiro 1983 |
| depth-dependent viscosity | 46, **47** | a step: `1` below `z*_D`, `Δη` above |
| density stratification | **48**, 52 | and eq. 52 is a **second branch** for when `Nu > 1/z*_D` |
| compositional buoyancy | **50**, 51 | `dρ/dF ≈ −1.2 kg m⁻³ per per cent` (Korenaga 2006), and a mean degree of melting |
| equivalent temperature contrast | 53, **54** | `T*_ρ`, how the density contrast enters as a temperature |
| the outer solve | **56** | `Nu = F_Nu(n, E, T_s, ΔT, Ra_i, Δη, Δρ, z*_D)`, iterated by setting `z*_D = Nu^{−1}` when `Nu > 1/z*_D` |

**Fourteen equations, and three nested numerical levels** — a maximization over `δ_eff` inside a
root-find for `δ` inside a fixed-point iteration on `z*_D`. ⚠ **That is C20-sized**, not a
transcription: `core_history.py` is the closest thing this engine already has to it.

**⚠ Two declared inputs we would have to supply, and one of them comes from a figure.**

- `Δη`, the dehydration viscosity contrast: §4 **sets it to 10²**, while §3 reports experiments
  suggesting *"a factor of ∼10³ increase in viscosity due to dehydration"* for diffusion creep. Printed
  ends, different values, no election — **a C32 band, not a constant.**
- `Δρ`: §4 says *"compositional buoyancy is calculated based on **Fig. 11**"*. ⚠ **An input read off a
  graph.** Everything else here is a formula; this one is not.
- Also declared and ours to carry: melt productivity `(dF/dP)_S = 15 %/GPa` (Korenaga 2006) and
  `P_f = 0`, *"for simplicity"*.

**⚠ What we already hold — and the honest answer is nothing that fits.** Brief 147 asked this first
because two builds today turned out to exist already. This one does not.

| candidate | what it is | verdict |
|---|---|---|
| `eos.py`'s `silicate_solidus(p, variant)` | melting **temperature as a function of pressure**, Andrault+ 2011 A-chondritic/peridotitic | ✗ **the inverse quantity from a different source.** Eq. 45 gives the **pressure at which a mantle of potential temperature `T_p` begins to melt**. Substituting ours moves the paper's own depleted-layer depth |
| `mantle_flux.py`'s `viscosity()` | `η₀ exp(−ζ(T − T₀))`, **linear-exponential**, Nimmo eq. 35 | ✗ **this is the rheology the paper argues against.** Korenaga 2009's subject *is* Arrhenius versus linear-exponential, and its eq. 21 carries `exp[E/(nRT_i)]` |

⚠ One thing does come free from the comparison: Nimmo's `ζ = 10⁻² K⁻¹` gives `θ = ζΔT = 13.5` at
`ΔT = 1350 K`, and Korenaga's Table 2 lists `θ` from **7.93 to 15.11** across `Δη = 3–30000`. **The two
papers' `θ` mean the same thing and sit in the same range** — a free consistency check between two
independently transcribed modules.

**⚠ Reproduction anchors — and this is where it is stronger than the last transcription this engine
tried.** `tidal_transport.py` carries `failed-io-reproduction` because Kankanamge & Moore 2019 cannot
reproduce its own printed result. Korenaga 2009 offers three checks, and two already pass:

| anchor | status |
|---|---|
| §4.1's printed *"`Ra_i` varies from ∼10⁹ to ∼10¹³"* over `T_i` 1200–1800 °C | ✅ **passes** — this seat's transcription gives **1.26 × 10⁹ → 2.27 × 10¹²**. ⚠ Note `Ra_i` at the Earth condition is pinned by `q = 50 mW/m²` alone, so this tests the `θ`/`Ra_i`/`Nu` chain and says nothing about `α` |
| eq. 44's `Ra_crit(n)` against the text's *"∼450 (n = 1), ∼134 (n = 2), ∼104 (n = 3)"* | ✅ **passes at n = 1 and 3** — `exp(3.84 + 2.25/n)` gives 440 and 98.5. ⚠ `n = 2` gives 143 against ∼134, **7 % off** |
| **Table 2**, which prints per-row `θ`, `Ra`, `Nu`, `δ` for `Δη = 3 … 30000` | **the real anchor, unused so far** — row-by-row numbers for exactly the stability analysis eq. 43 performs |
| §4's dimensional planetary results | ⚠ **Figs 12–14 only.** No printed dimensional flux to check against, so the absolute scale has no anchor — consistent with C47 (c)'s finding that the absolute scale is declared arbitrary |

**Size verdict: a multi-session build with a good row-level anchor and no absolute-scale anchor.** The
stability analysis can be verified against Table 2 row by row; the dimensionalized planetary flux
cannot be verified against anything the paper prints.

**⚠ And the guardrail check found an error in this seat's own C47 (d), corrected there.** The
*"÷5–10"* is **prose, appearing twice** (Summary and §5) and reading *"could reduce … **by up to** a
factor of ∼5–10"* — a summary of Figs 12–13, not a printed range of computed values, and an **upper
bound on the reduction**. C47 (d) put ÷5 and ÷10 at the ends of an interval and observed that both
landed under the ceiling. **An "up to" is one-sided**: the reduced flux lies in `[q/10, q]`, so the
melting correction **permits** the ceiling and does not deliver it. Reading a bound as an interval and
taking its ends is the same error class as C46's ceiling-used-as-floor, repeated by the same seat a few
hours after repairing it. **The conclusion that Korenaga is the remaining unexhausted route stands; the
claim that it already lands does not.**

### C47 (f) 2026-09-08 — step 1 passes: the transcription reproduces the only row-level anchor this engine has

**Built: `engine/stagnant_lid.py` + `engine/test_stagnant_lid.py`, wired into the gate.** Brief 148's
step 1 was to match eq. 43's stability analysis against Table 2's printed rows and **stop if it does
not match**. It matches.

**⚠ First, the directing seat corrected this seat's stopping line, and the correction is right.** C47
(e) recommended abandoning the build because the absolute flux has no anchor. But the pass condition is
a **ratio**:

    Ur_Mars / Ur_Earth  =  (H_Mars/H_Earth) × (q_Earth/q_Mars)

`H` is known absolutely for both bodies, and if `b` is **one global declaration** then `q ∝ b^{−β/n}`
appears on both sides of `q_Earth/q_Mars` and cancels. **So the direction test does not need the
absolute scale, and the missing anchor does not block it.** My stopping line was drawn around the wrong
quantity. ⚠ It survives in one narrowed place — the *absolute* flux still has no anchor and must not be
emitted — which is now the recorded reason for a refusal rather than a reason to stop.

**⚠ Second, two things this seat had told the directing seat turned out wrong on reading.**

1. **The equation to test is eq. 29, not eq. 30.** The paper introduces eq. 30 with *"In the limit of
   `Nu ≫ 1`, it approaches the following asymptotic formula"*, and Table 2's `Nu` is **3.1–7.2**. Read
   from the page image of p. 158, eq. 29 is
   `Nu[1 − 2Nu⁻¹(1 − a_rh θ⁻¹)]^{1−β(n+2)/(2n)} = a θ^{−1−β} Ra_i^β` — and `a ≈ 0.30 + 0.25n` was
   **fitted to eq. 29, not eq. 30**. ⚠ So **C47 (c)'s direction test ran the asymptotic form outside
   its own stated limit.** At Table 2's scale the two forms differ by **27 %**; they converge to 0.1 %
   only when `Ra_i` is raised 10⁸×. That does not overturn C47 (c)'s finding — `D` still cancels and
   both laws still go as `g^{1/3}` — but the test has to be re-run on eq. 29 in step 4.
2. **Table 1 cannot be an anchor.** C47 (e) listed it as one. Its linear-exponential block prints `Nu`
   but its `θ` and `Ra_i` sit in the **Arrhenius** columns, so no `(θ, Ra_i, Nu)` triple exists there.
   **Table 2's Δη = 1 block is the only row-level anchor in this paper**, ten rows of it.

**Step 1's result.**

| check | result |
|---|---|
| eq. 29 against Table 2's ten `Δη = 1` rows | **rms 2.27 %**, bias **−0.44 %p**, worst row **4.63 %** |
| the paper's own stated fit quality | *"The rms error of the fit is ∼1.2 per cent"* — ⚠ **on Table 1**, the set the fit was made to. 2.27 % on a held-out set is the expected degradation |
| eq. 44's `Ra_crit(n)` against the text's ∼450 / ∼134 / ∼104 | 441 · **143** · 98 — n = 1 and 3 pass, ⚠ **n = 2 off by 7 %**, now pinned by a test that fires if it ever changes |
| eq. 30 as the `Nu ≫ 1` limit of eq. 29 | ratio **1.270** at Table 2's scale → **1.001** at 10⁸× `Ra_i` |
| free cross-check: Nimmo's `ζ = 10⁻²` at `ΔT = 1350` gives `θ = 13.50` | inside Table 2's `θ` range 7.93–16.05. **Two independently transcribed modules agree on a quantity that means the same thing in both papers** |

**⚠ And the residual was tested for tunability, then left alone.** Refitting `a_rh` from the text's
2.5 gives 2.256 and buys **0.08 percentage points** of rms. A residual that refitting cannot move is
not a knob, so the text's single value stands and `Δη`-free `a_rh` is not read off Fig. 3. **A test
pins that**: if refitting ever buys more than 0.5 %p, it fires, because that would mean the residual
*is* adjustable and the single value would need re-arguing.

**What is not built, and stays not built until later steps:** any flux, dimensional or not. This module
emits nothing into the chain. The melting correction (eqs 41–56), the `b` sensitivity measurement, and
the Earth-vs-Mars direction test are steps 2–4.

### C47 (f2) 2026-09-08 — step 3's dehydration half passes 30 rows with zero tuned parameters

**Built into `engine/stagnant_lid.py`: eq. 42's local Rayleigh number, eq. 43's stability criterion,
eqs 45/50/51/53/54's melting parameters.** ⚠ **n = 1 only** — eq. 46's stress term `(τ*)^{1−n}` is
exactly 1 there and the derivation below drops it. The paper's own §4.1 and Table 2 are both n = 1.

**⚠ The geometry was derived, not guessed, and the derivation reproduces the paper's own fitted
coefficient.** Sublayers are measured **upward from the boundary layer's base**, and `η*` is relative
to `η(T_i)` because `Ra_i` already carries `exp[E/(nRT_i)]`, so `⟨1−T*⟩ = u/2` and
`η*_eff = exp(θu/2)`. The maximum in eq. 42 then falls at an interior point `u* = 4(n+1)/(nθ)`, and
eliminating `δ` gives `Nu ∝ θ^{−(2n+2)/(n+2)} Ra_i^β` — where **`(2n+2)/(n+2) = 1+β` exactly**, which
is eq. 30's form. The coefficient that falls out is

    a = [4(n+1)/n]^{1+β} exp(−2(n+1)β/n) / Ra_crit^β  =  **0.5539**  at n = 1

against the paper's regression result **`a = 0.55`** — **0.7 %.** ⚠ **That is not a transcription
check; it is an independent reproduction of the paper's own claim** that *"the boundary-layer stability
approach reproduces exactly the asymptotic heat-flow scaling"*. Confirmed numerically too: eq. 43's
numerics sit at **1.0071×** eq. 30 on every row, and 1.0071 is exactly 0.5539/0.55.

⚠ **And the same derivation fails at n ≥ 2** (0.274 and 0.187 against 0.80 and 1.05), which is the
dropped stress term showing itself. Diagnosed rather than patched, and the scope is recorded as n = 1.

⚠ **Labelled 2026-09-09 (Brief 167 A) — "the paper's regression result" is one of five numbers for this
one quantity, and Korenaga states the reason for the spread himself.** Read verbatim from the held paper:
*"Solomatov & Moresi (2000) ([`2000JGR...10521795S`](https://ui.adsabs.harvard.edu/abs/2000JGR...10521795S)) fit eq. (29) to their
numerical results and obtained **a ≈ 0.31 + 0.22n** by assuming a_rh = 1.2(n + 1). As **my definition of
T̄_i (eq. 20) results in slightly different values of Nu, Ra_i and a_rh**, I repeated their regression
analysis and obtained that **a ≈ 0.30 + 0.25n**. The rms error of the fit is ∼1.2 per cent."*

| value at `n = 1` | where it comes from |
|---|---|
| **0.528 ± 0.002** | S&M 2000 Table 5's one-parameter fit (`a_rh` 2.4, `β` fixed at the theoretical 0.333, χ²ᵥ 0.3) |
| **0.53** | the same paper as Korenaga summarises it, `a ≈ 0.31 + 0.22n` under `a_rh = 1.2(n+1)` |
| **0.55** | **Korenaga's own re-regression**, `a ≈ 0.30 + 0.25n` — *this is the 0.55 above, and the comparison stands* |
| **0.57** | Korenaga's Fig. 6 caption, a separate per-`n` subgroup fit in the same paper |
| **0.5** | Foley 2018's printed `c₁`, citing Reese, S&M and Korenaga together |

**So the 0.7 % is a correct statement about the number it names**, and it is a better one than it looked:
Korenaga's own fit carries an **rms of ∼1.2 per cent**, so our closed form lands **inside the paper's own
fit error**. ⚠ **What the 0.7 % must not be read as is agreement with the primary fit** — against S&M's
0.528 ± 0.002 our 0.5539 is **+4.91 %**, thirteen times that fit's stated precision. **And the cause is
printed, not mysterious: a different definition of the internal temperature `T̄_i`.** ⚠ *Which also means
that "+4.91 %, thirteen times" is a **comparison across a definition boundary and not evidence of an
implementation error** — the within-definition check is the 0.7 % against Korenaga's own refit, and it
passes inside his fit's rms. The three definitions are laid out verbatim in C51's first-anchor section.* That same
difference is the one candidate explanation for the 3.65× absolute-flux gap between the two papers
(C51's first anchor), which is why this is labelled here rather than repaired.

**Table 2, all three blocks, `nu_full` = eq. 43 + eq. 29's pre-asymptotic bracket:**

| `Δη` | rms | bias | worst | rows used in the paper's fit? |
|---|---|---|---|---|
| 1 | **2.16 %** | −0.01 %p | 4.22 % | no — the fit was to Table 1 |
| 3 | **2.84 %** | +1.68 %p | 6.10 % | ⚠ **no. independent anchor** |
| 10 | **3.35 %** | +1.95 %p | 8.24 % | ⚠ **no. independent anchor** |
| **all 30** | **2.83 %** | +1.21 %p | | |

**Zero free parameters**: `Ra_crit` from eq. 44, `a_rh` = 2.5 from §2.2's text, `z*_D` = 0.75 from
Table 2's footnote, `Δη` from the table's own column. **So the twenty `Δη = 3` and `Δη = 10` rows are
an independent anchor for the dehydration-stiffening mechanism**, and a test comment says so, so that
nobody later reads all thirty as fitted.

⚠ **One construction here is ours and is labelled in the code.** The stability analysis returns the
**asymptotic** `Nu`; Table 2's `Nu` of 3–7 is not asymptotic. So eq. 43's result is fed as the
right-hand side of eq. 29 and `Nu` re-solved. At `Δη = 1` that is exactly eq. 29; extending it to
`Δη ≠ 1` is our step, not the paper's.

**Two claims this seat made to the directing seat were wrong, and reading fixed both — in the
favourable direction this time.**

1. ⚠ **`Δρ` needs no figure read.** C47 (e) called it *"an input read off a graph"*. Eqs 51 and 53
   with §5's printed `(dF/dP)_S = 15 %/GPa` and `P_f = 0`, eq. 50's `dρ/dF`, §4's `ρ₀ = 3300` and
   eq. 45's solidus compute it outright. **Fig. 11 is a plot of the result.**
2. ⚠ **The paper contradicts its own `α`, and the contradiction is load-bearing.** §4's constant list
   prints `α = 2 × 10⁻³ K⁻¹`; §3.2's worked example says *"The factor αΔT is ∼0.05, so Δρ of 0.99
   corresponds to ΔT*_ρ of ∼0.2"*. At the paper's own `ΔT = 1350 K`, §4's value gives `αΔT = 2.70` and
   `ΔT*_ρ = 0.0037` — **missing both numbers** — while `3.7 × 10⁻⁵` gives `0.0499` and `0.2002`,
   **hitting both inside 0.2 %.** And ⚠ **this seat's earlier "harmless inside the paper" verdict on
   defect #24 was wrong**: `b` absorbs `α` inside `Ra_i`, but `α` **also** sets `ΔT*_ρ` in eq. 54,
   where nothing absorbs it. Using the printed value switches compositional buoyancy **off** rather
   than weakening it.


### C47 (g) 2026-09-08 — pre-registration for step 4, written before the test was run

⚠ **This section was written and committed BEFORE the direction test was computed.** That is the
point of it. The `α` choice below feeds the one mechanism that could produce the Earth-vs-Mars
asymmetry step 4 measures, and the two candidate values differ by **54×**, so the choice has to be
justified on grounds that cannot know the answer.

**The choice: `α = 3.7 × 10⁻⁵ K⁻¹`, from Korenaga 2009 §3.2, not the `2 × 10⁻³ K⁻¹` printed in §4.**

**The grounds, which are independent of step 4's outcome.** §3.2 states its own worked example:

> *"The factor **αΔT is ∼0.05**, so Δρ of 0.99 corresponds to `ΔT*_ρ` of ∼0.2."*

With the paper's own `ΔT = 1350 K`:

| `α` | `αΔT` | `ΔT*_ρ` at `Δρ = 0.99` | reproduces §3.2? |
|---|---|---|---|
| **2 × 10⁻³** — printed in §4's constant list | 2.700 | 0.0037 | ✗ off by 54× |
| **3.7 × 10⁻⁵** | **0.0499** | **0.2002** | ✅ both numbers, to 0.2 % |

**The paper contradicts itself, and only one of the two readings reproduces the paper's own worked
example.** That is the whole argument, and it is settled by arithmetic on two printed sentences —
nothing in it looks at Earth, Mars, or a Urey ratio.

⚠ **Why this is a place where a reader should be suspicious, stated by us rather than left to be
found.** `α` sets `ΔT*_ρ` (eq. 54), `ΔT*_ρ` enters `ΔT*_eff` in eq. 42, and compositional buoyancy is
**the candidate mechanism for the very asymmetry step 4 is about to measure**. Choosing the value that
makes that mechanism 54× stronger, immediately before measuring whether the mechanism is strong
enough, is a sequence that looks like knob-turning from the outside however sound the argument is.

**So step 4 is run BOTH ways and both lines are reported, side by side, whichever passes.** The
dependence is published, not resolved: a reader must be able to see at a glance that the conclusion
rests on which half of the paper's self-contradiction is taken.

**What is already fixed and cannot move**, so that step 4 has nothing left to tune:

| quantity | value | source |
|---|---|---|
| `Ra_crit(n)` | `exp(3.84 + 2.25/n)` | eq. 44 |
| `a_rh` (n = 1, linear-exponential) | 2.5 | §2.2 text, and refitting buys 0.08 %p — C47 (f) |
| `(dF/dP)_S` | 15 %/GPa | §5, printed (Korenaga 2006) |
| `P_f` | 0 | §5, *"for simplicity"* |
| `dρ/dF` | −1.2 kg m⁻³ per per cent | eq. 50 |
| `ρ₀` for melting parameters | 3300 kg m⁻³ | §4 |
| `b` | re-fitted on the paper's own printed Earth condition, one global declaration | C47 (d), and C47 (f) measured the ratio's sensitivity at 3.7 % per decade against the absolute flux's 115 %, bounded above at 1.384 |
| `Δη` | **a band, 10² (§4) and ∼10³ (§3)** — not elected | §3, §4 |

**The target step 4 must hit, fixed in C47 (f) before this section:** `q_Earth/q_Mars` must reach
**3.68** (against our own 0.454 denominator) or **4.78** (against Korenaga's 0.35), from the
no-melting value of **1.372**. So the melting correction must suppress Mars's flux **2.7–3.5× more
than Earth's**.

**⚠ Pre-registered verdict rule — all four cells, written before the run.** The fourth was missing
from the first draft of this section and was filled on the directing seat's catch, still before the
computation. A rule invented after seeing which cell you landed in is not a rule.

| outcome | verdict |
|---|---|
| **neither `α` reaches the target** | the **fourth** law family to fail in the same direction. C47 closes as *named, not filled* — the recorded answer becomes "no single untuned law in this literature reproduces both Urey ratios", and the three-families-same-direction note in C47 (c) closes with it |
| **both reach it** | the choice did not matter; the result stands on its own and `α` is recorded as a non-issue for this test |
| **only §3.2's `α = 3.7 × 10⁻⁵` reaches it** | reported as **conditional on the paper's self-contradiction**, and **not** presented as a pass. The arithmetic favours §3.2, but a result that exists only under one half of a contradiction is a result with a footnote, not a closed item |
| **only §4's printed `α = 2 × 10⁻³` reaches it** | ⚠ **also not a pass, and for a sharper reason than "wrong for the right reason".** At `αΔT = 2.7` the equivalent temperature contrast is `ΔT*_ρ ≈ 0.004` — compositional buoyancy is *switched off*, not merely weakened. So this cell would mean **the asymmetry is carried by dehydration stiffening alone, and adding compositional buoyancy destroys it** — i.e. the paper's two melting mechanisms push in opposite directions on the very quantity being tested. That is a finding about the mechanisms and it gets its own item; it is not evidence that the law reproduces the Urey ratios, because the `α` producing it fails the paper's own worked example |

**⚠ The point of the eight fixed values above is that step 4 has nothing left to tune.** That sentence
matters more than the table: every quantity the direction test touches was pinned by a printed source
before the test ran, so a failure cannot be argued away and a pass cannot be manufactured.

**⚠ Registered decomposition — the test is run three ways per `α`, six runs in all.** The insight
behind the fourth cell is that **dehydration stiffening and compositional buoyancy push in opposite
directions on the asymmetry.** If that is true it is true whichever cell lands, so it must be measured
in the main test rather than invoked only where it becomes extreme:

| run | mechanisms on | what it answers |
|---|---|---|
| **(a)** | dehydration stiffening only (`Δη`, `z*_D`) | how much of the asymmetry the stiff dehydrated lid carries alone |
| **(b)** | compositional buoyancy only (`ΔT*_ρ`) | how much the density contrast carries alone, and **with what sign** |
| **(c)** | both — **this is the test** | whether the target 3.68 / 4.78 is reached |

⚠ **Registered before the computation, and the reason matters:** with a single number the result is
uninterpretable either way — reaching the target would not say what carried it, and missing it would
not say what was short. A decomposition added *after* seeing where (c) landed would be a
decomposition built to explain the answer. Registered now, it also puts the opposite-directions claim
at risk: if (a) and (b) turn out to push the **same** way, the fourth cell's reasoning is wrong and
that gets recorded as this seat's error.

**Sign convention fixed now, so it cannot be reinterpreted later:** the asymmetry is `q_Earth/q_Mars`,
and a mechanism *helps* if turning it on **raises** that ratio above the no-melting 1.372. A mechanism
that lowers it pushes against the test.

### C47 (h) 2026-09-08 — step 4's verdict is held, and step 0's threshold is written before the measurement

**Step 4 ran, its numbers are final, and its verdict is held.** The numbers are in C47 (g)'s
pre-registration and are not revised here. ⚠ *Corrected 2026-09-08 (Brief 160): **that run's outputs are
not in this repo.** (g) holds the pre-registration — the four cells, the eight fixed values, the target
3.68 / 4.78 and the no-melting 1.372 — and no `q_Earth/q_Mars` from a run appears in any document,
module, test or scratch directory. The run lived in the 09-07/08 seats' transcripts and its numbers went
with them. Step 4 is therefore a **build**, not a re-run — counted in C47 (j).* ⚠ *And that marker is
itself superseded within the day: the run **was recovered** from the 09-07 transcript at `f3f068ea`, so
"in no scratch directory", "went with them" and "a build, not a re-run" are each no longer true as
written — see C47 (j) and (k).* What is recorded here is why the verdict cannot be read off
them yet.

**⚠ The pre-registration had a hole, and the directing seat found it, not this seat.** The eight
quantities pinned before step 4 do not include `T_p`. The direction test was run at a **common
potential temperature** for Earth and Mars — a decision made while implementing, on the mistaken
ground that C47 (c) had already settled it. **C47 (c) settled something else**: it forbade *choosing*
Mars's `T_m` so that `Ur` comes out. **Reading `T_p` off a thermal history is not choosing.** Those two
were collapsed into one, and the collapse is this seat's.

⚠ **The omission is shared and is recorded as shared.** This seat pinned eight values and published
the table; the directing seat approved it. Neither noticed the ninth. It is not the work seat's alone.

**Why it matters, in one sentence:** Mars's higher Urey ratio is explained in the literature by Mars
having *cooled more* — so running the test at a common `T_p` may have removed the very physics being
tested, in which case the failure is the setup's and not Korenaga's.

**And route (ii) is not hypothetical.** `core_history` already emits
`mantle_potential_temperature_present`, and on Earth it returns **1525 K** against the 1623 K this
seat fed step 4 from Korenaga's own §4 condition — a 98 K difference between two non-arbitrary
sources. ⚠ **Corrected later the same night by C48: that 1525 K comes out of a call made far outside
the flux law's expansion point.** The blast radius of C48 is small — one consuming edge, no board row,
no `db/` entry — **but a small blast radius does not exempt this citation**, which is inside it. The
argument above stands only as far as C48 leaves it standing. It cannot run on Mars because `earth.yaml` is the only body declaring the two initial
temperatures.

**⚠ Route (i) is closed, and not for want of looking.** Monders, Médard & Grove 2007
([`2007M&PS...42..131M`](https://ui.adsabs.harvard.edu/abs/2007M%26PS...42..131M)) states
*"the persistence of high mantle potential temperatures on Mars, **similar to those on the modern
Earth**, until at least the very latest Noachian (**3.7 Ga**)"*. **Mars has no present volcanism, so
no erupted melt records a present `T_p`** — every "present Martian potential temperature" in the
literature is a thermal-model output, not a measurement. ⚠ And the paper's `1320 °C` is the multiple
saturation temperature of **one Gusev basalt at 1.0 GPa**, not a mantle potential temperature; it is
not transcribed. Baratoux+ 2011 ([`2011Natur.472..338B`](https://ui.adsabs.harvard.edu/abs/2011Natur.472..338B))
is the canonical `T_p`-versus-time curve and was **not held** (Nature) — ⚠ *held since 2026-09-08
(owner-supplied PDF). Reading it closed the hole and narrowed the claim: the paper prints the epoch
**difference** (80 ± 20 °C) but no absolute `T_p` anywhere in its text — the levels everyone re-cites are
contour labels on its Fig. 3/4. See C47 (i).*
⚠ **2026-09-08 — re-cited present-day values found, the original still unheld.** Yoshizaki & McDonough
2020 (~1500 K) and Dong+ 2022 (1600 K "today") both print present-day Martian `T_p` **as model inputs**,
100 K apart, both tracing to Baratoux+ 2011 — held since 2026-09-08, and its absolute levels are
figure-read, not printed (C47 (i)). **So "closed" above is wrong as written** — what
survives is that no Mars `T_p` is *measured*. Corrected in full in C47 (i).

**What Mars needs, which is more than the brief supposed.** ⚠ *Stale since Brief 149 (`2d1bb397`), which
created it: `engine/bodies/mars.yaml` exists, with the two declarations below written into it.* There is no `mars.yaml` at all; the five
body files are Earth, Alpha Centauri A b, Pandora and the two Luhman 16 components. So this is a new
control body, on `earth.yaml`'s own stated footing — *"a specimen for checking the engine against
published values, not a board body"* — and **it does not go on the board.** Of its inputs, mass,
radius, age and core mass fraction are published and `stagnant_lid: true` is a fact, but **three
declarations have no Martian source**: `potential_temperature` and the two initial temperatures.

**Two of the three cost nothing, and one is the whole question.**

- **The initial temperatures transfer unchanged from Nimmo+ 2004's printed starting condition** —
  Fig. 2's caption, *"starting temperature of both mantle and core was 4800 K"*, which is where
  Earth's own 4800 K / 3040 K come from. That is this engine's established pattern for an Earth number
  declared on every rocky body (`MANTLE_SHARE = 0.70`, `T_s = 293 K`), and its value here is precisely
  that **it leaves nothing for this seat to pick.** The 3.7 Ga checkpoint then validates or refutes the
  transfer.
- ⚠ **`potential_temperature` is different, and transferring Earth's 1600 K would re-introduce the
  defect this section exists to fix — with a citation attached.** It also steers the trajectory:
  `core_history` sets `r_b = cmb_temperature / potential_temperature` and divides the mantle cooling
  rate by `√r_b`.

**So step 0's question, stated the way the directing seat put it, which is sharper than this seat's
first framing:** not *"is route (ii) circular"* but **"may Earth's `potential_temperature` be
transferred to Mars at all?"**

**⚠ Threshold and sweep width, fixed here before the measurement.** Naming "weak" and "strong" after
seeing the numbers would be inventing a rule to fit the cell it landed in — the error this seat
blocked in C47 (g)'s fourth cell and would otherwise repeat one section later.

| item | value | ground |
|---|---|---|
| **sweep** | declared Mars `potential_temperature` over **1400–1800 K** | Earth's declared value is 1600 K (Unterborn+ 2019) and Monders has Mars *"similar to modern Earth"* until 3.7 Ga, so ±200 K brackets it without being chosen for an outcome |
| **criterion A** | `abs(d output T_p / d declared T_pot) < 0.5` | at a slope of 1 the declaration **is** the output; at 0 the trajectory has forgotten it. Half is the point where the body's own mass, radius and age stop dominating |
| **criterion B** | the 3.7 Ga checkpoint verdict must be **the same at both sweep ends** | if sweeping our declaration flips the checkpoint, the checkpoint is testing the declaration and not the trajectory |
| **rule** | **both** must hold to proceed. Either failing stops step 0 and the transfer is refused | — |

⚠ **Criterion A measures the declaration's effect on the *output `T_p`*, not on `q_E/q_M`, and that
is deliberate.** The end-to-end sensitivity looks like the more relevant one and it is the one that
must not gate this decision: **fixing a threshold on the final answer means letting the answer decide
whether the input was legitimate.** A is on the intermediate quantity because the question is whether
Earth's number propagates into Mars's state — which is answerable without knowing what that state then
implies. **Not an omission; the placement is the point**, and it is written here because the obvious
"improvement" is to move it.

**The end-to-end sensitivity is measured afterwards and kept as a record.** Once the verdict is fixed
it can no longer influence it, and what the result depends on, and by how much, still gets written
down. Order buys both.

⚠ **And the checkpoint's own limit, recorded beside it so a pass is not over-read:** Monders gives a
**qualitative** statement, not a number. The checkpoint can only catch a badly wrong trajectory. **A
pass is not a precision validation of the Martian thermal history**, and nothing downstream may cite
it as one.

### C47 (i) 2026-09-08 — step 0's numbers, the criterion-B rule fixed before the unblinding, and four corrections

**Step 0 asked one question — `engine/interior-core-closed.md@«be transferred to Mars at all?»` — and this section carries its numbers.** Criterion A's are below and
final, and criterion B's are below. ⚠ **The rule that decides criterion B was committed at `2fb2bba4`
with the 3.7 Ga column still unread** — including the verdict-line paper, which was the owner's to pick.
The table was computed afterwards and added in the commit that follows it, so **git testifies to the
order** rather than this sentence doing it.

⚠ **Every number in this section is at the core heating H = 1.5 pW/kg** (`core_energy.H_CORE` as it stood on
2026-09-08). Owner decision ⑤ lowered the declared H to 0.14 on 2026-09-09, and at the declared H the same
trajectory ends at **T_p 1377.23 K** with **T_p@3.7 Ga 1668.05 K** — criterion B still passes, with the upper-end
headroom **5.1 K** instead of 4.0–4.7 K. Criterion A's 1400–1800 K sweep has **not** been re-run at the declared H.
The numbers below are left exactly as measured; the label is what Brief 166 D adds.

⚠ **And 180 C spent some of that headroom** (2026-09-11). The pressure split gives Mars's core γ **2.8718**
instead of 1.5 at its core-mantle boundary, and `core_history` reads that through `cmb_flux` and
`core_energy` — so the declared-H trajectory's 3.7 Ga checkpoint moved **1668.00 → 1668.79 K** and the
distance to Herzberg's upper edge **1673.15 K** went **5.15 → 4.36 K**. Criterion B still passes.
*It is named here because the direction matters more than the size:* this section's own sentence is that
**a 5 K error anywhere in the trajectory flips this checkpoint**, and 180 C moved it 0.79 K toward the
edge for a reason that is a **measured liquid thermal set**, not a modelling choice.

#### The criterion-B rule, fixed before the numbers were read

C47 (h) pre-registered criterion B as one sentence — *the 3.7 Ga checkpoint verdict must be the same
at both sweep ends*. That sentence plus a paper band did not compose into one window, and the work
seat refused to unblind until the directing seat closed the four gaps. ⚠ **The refusal is the reason
this subsection exists: the rule below was fixed while the answer was still unread, and the commit
carrying it is dated before the commit carrying the table.**

| # | question the sentence did not answer | decided 2026-09-08 | why this and not the other reading |
|---|---|---|---|
| ① | is the window the paper's **absolute** band, or the paper's width **centred on** Earth's declared 1600 K? | **absolute band.** Pass = `T_p@3.7 Ga ∈ [band]`. The declared 1600 K does **not** enter the arithmetic; it stays as the guard that the window is never built from the engine's own 1525 K output | centring would invent a `±` no paper prints (Herzberg 2007's band is not symmetric about 1600 K), which is `docs/reference/derivation-discipline.md@«A band is the opposite of a knob only when its width comes from the physics»`. ⚠ The two readings differ by 13.15 K at each edge, so this is not cosmetic |
| ② | one of the four candidate papers prints a **point** (Herzberg+ 2010, 1350 °C = 1623 K, no `±` in the abstract) — what is its in/out? | **excluded from the agreement test**, kept as a record column reporting the distance in K | a zero-width window admits nothing, so its cell is undefined under either reading of ①. The agreement test runs on the three candidates that print a band |
| ③ | "the same verdict at both ends" — is **both ends out** "the same"? | **failure.** Both ends out means no declared value passes the checkpoint, which is a refutation, not stability. Step 0 fails and the transfer is refused | the checkpoint asks whether the declaration puts Mars near modern Earth at 3.7 Ga; "stable and wrong at every point" answers that with no |
| ④ | which variant, and do the interior sweep points count? | **verdict on `T_m0-fixed`** (the variant that uses `engine/bodies/mars.yaml@«mantle_initial_potential_temperature: 4021.0»`, the file's printed value), **at the two ends only**. `r_b-point` and the three interior points are record columns | (h) says *both sweep ends*, and the variants are an implementation choice that (h) never registered, so the file's own printed state is the one under test |

**The verdict line is the owner's, and it is chosen: Herzberg+ 2007, `[1553.15, 1673.15]` K
(2026-09-08 17:35, from the four candidates below).** ⚠ The rank order that would have picked it
— rank 1 Monders+ 2007, rank 2 Herzberg+ 2007 — **was a seat's, is in no commit, and collided with
the parallel seat's own finding** that *the choice of paper is the choice of width, so it is an
owner-facing choice*. So the rank order is chronicle only; the four candidates went to the owner and
the owner picked the first:

| candidate | window, K | grade | note |
|---|---|---|---|
| **Herzberg+ 2007** [`2007GGG.....8.2006H`](https://ui.adsabs.harvard.edu/abs/2007GGG.....8.2006H) — ✅ **owner's choice, the verdict line** | **[1553.15, 1673.15]** | ⚠ **held** since 2026-09-08 (owner-supplied PDF, cache) — upgraded from *abstract only*, and the label re-read in the body: *"Our preferred `T_P` range for ambient mantle is 1280–1400 °C (Figure 5)"*, computed by the **McKenzie & Bickle 1988** potential-temperature method for *"MORB magmas with 10–13 % MgO"*, and again where the paper states its result — *"Our work shows that ambient mantle temperatures at normal oceanic ridges are 1280–1400°C"*, `ΔT_P` = 120 °C — the sentence pinning the location rather than a paragraph number | a potential temperature of the ambient mantle, so it does not repeat the Monders defect below. The body also warns its Iceland values *"should not be used as a high `T_P` anchor for ambient mantle"* — we do not |
| Katsura+ 2010 [`2010PEPI..183..212K`](https://ui.adsabs.harvard.edu/abs/2010PEPI..183..212K) — record column | [1575, 1645] from the abstract; **[1560, 1640] from the body** | ⚠ **held** since 2026-09-08 | mineral-physics route (410-km discontinuity + adiabat), no solidus anywhere in it. ⚠ **The abstract and the body disagree**: abstract *"the mantle potential temperature is found to be 1610 ± 35 K"*, body §4 *"1600 ± 40 K"* — and the divergence is systematic, not only in `T_p` (transition-zone base 2010 ± 40 vs 1990 ± 50 K, 2700 km 2730 ± 50 vs 2630 ± 60 K). **Neither is elected**, both are recorded, and **Mars's 1668 K is outside both**, so the record column's verdict does not move |
| Putirka 2016 [`2016AmMin.101..819P`](https://ui.adsabs.harvard.edu/abs/2016AmMin.101..819P) — record column | [1603.15, 1723.15] | abstract only | 1330–1450 °C, modern ambient MORB, olivine–liquid Fe–Mg re-calibration |
| union of the four | [1553.15, 1723.15] | — | widest reading, **unchanged** by Herzberg+ 2010's band, which lies inside it |
| ⚠ **Monders+ 2007 cannot supply one** | — | held | its 1280–1475 °C is Earth's **basaltic magmatism** range (Kinzler & Grove 1992, McKenzie & Bickle 1988), not a potential temperature. Using it would put a magmatism range in a `T_p` slot — the same class of error C47 was opened for |
| record only | Herzberg+ 2010 [`2010E&PSL.292...79H`](https://ui.adsabs.harvard.edu/abs/2010E%26PSL.292...79H) 1623 K (the point of rule ②) — ⚠ **held** since 2026-09-08, and the body §3 does print a **band**: *"a mantle potential temperature (i.e., `T_P`) of **1350 ± 50 °C** is required to produce primary basaltic magmas having 10–13 % MgO"* = **[1573.15, 1673.15] K**, which Mars's 1668 K is **inside**. ⚠ **Rule ②'s "point candidate, excluded" was a decision taken on the abstract**, which prints no ±; recorded here as an after-the-fact column, and **the agreement test is not recomputed** — re-running a test on evidence that arrived after its verdict is the thing pre-registration exists to prevent. Also record-only: Sarafian+ 2017's **+60 °C** | — | so the apparent agreement of the two routes is not independent of whether that correction is applied |

#### Criterion A — passes, and by three orders of magnitude

**Sweep: Mars's declared `potential_temperature` over 1400–1800 K, five points, both variants.
Threshold `|d T_p,out / d T_pot,declared| < 0.5`, pre-registered in C47 (h).**

| declared `T_pot` | `r_b` | `T_m0` (`r_b`-point) | steps | output `T_p` | output `T_c` | `h_min` Myr | max `h/τ` |
|---|---|---|---|---|---|---|---|
| 1400 | 1.1882 | 4039.58 | 1197 | **1382.74** | 3897.09 | 0.0049 | 0.100 |
| 1500 | 1.1909 | 4030.44 | 1197 | **1382.82** | 3895.08 | 0.0051 | 0.100 |
| 1600 | 1.1937 | 4021.05 | 1197 | **1382.90** | 3893.01 | 0.0053 | 0.100 |
| 1700 | 1.1868 | 4044.41 | 1198 | **1382.73** | 3897.84 | 0.0048 | 0.100 |
| 1800 | 1.1799 | 4067.99 | 1199 | **1382.56** | 3902.68 | 0.0044 | 0.100 |

| variant | end-to-end slope | adjacent slopes | max \|slope\| | verdict |
|---|---|---|---|---|
| `r_b`-point | −0.0004 | +0.0008 +0.0008 −0.0017 −0.0017 | **0.0017** | ✅ ≪ 0.5 |
| `T_m0`-fixed | −0.0004 | +0.0008 +0.0008 −0.0017 −0.0017 | **0.0017** | ✅ ≪ 0.5 |

**Three things the table says beyond the threshold.**

- **The two variants agree to the printed digit at every point.** So ④'s choice of verdict variant
  moves nothing in the output; it is a provenance choice, not an accuracy one.
- ⚠ **The slope changes sign at 1600 K**, because `r_b` is itself non-monotonic in the declaration
  (1.1882 · 1.1909 · **1.1937** · 1.1868 · 1.1799 — a 1.2 % spread with its maximum at 1600 K). The
  400 K sweep moves the answer by **0.34 K**: the trajectory has all but forgotten the declaration.
- **Liveness, both parts, before any slope was read.** Earth's anchor reproduced inside the same run
  (`T_p` 1525.46 K against the anchor 1525.46, 1152 steps, `r_b` 1.5789) and the five outputs are five
  distinct values in both variants, so the sweep is not a constant — `engine/test_interior.py@«늘 발화하면 상수다»`
  applied to a scratch script whose numbers get reported.

#### Criterion B — passes, and ⚠ by 4 K

**Unblinded at 17:44:58 under the rule at `2fb2bba4`, from the values the 16:40 run wrote blind
(`C47 STAGE0 END rc=0 16:40:01`).** Verdict line **Herzberg+ 2007 `[1553.15, 1673.15]` K** (owner, 17:35 —
before the unblinding), verdict variant `T_m0`-fixed, verdict points the two ends.

⚠ **The seal held for nine of the ten columns, not ten.** The `1600 K` point's `T_p@3.7 Ga` was **already
public**: `engine/test_core_history.py` prints it as test ⑥'s third value (`T_p@3.7Ga`, the nearest adaptive
row) and `engine/interior-core.md@«within 0.1 K of the 0.25 Myr sweep»`'s C48 cell has carried **1669.22 K**
since `20ed09d7`. **What was public was the value, not the verdict** — 1600 K is an interior point and the
verdict is read at the two ends, so no cell could be anticipated from it. *(The same label, run two ways, is
0.10 K apart: 1669.22 adaptive against the 0.25 Myr sweep's 1669.12, which is test ⑥'s ±5 K comparand.)*

⚠ **And the pre-registered hold branch never fired, which is different from being skipped.** The rule said
*if the candidates disagree the verdict is held and the owner picks the paper* — and they do disagree. But
the owner picked at **17:35**, before the disagreement was visible at 17:44:58, so the branch was
**pre-empted by an earlier choice** rather than passed over. Its purpose — that a seat must not elect the
width — was served by the route the choice actually took.

| declared `T_pot` | variant | `T_p@3.7 Ga` | row's actual t, Gyr | `q_M`, TW | `q_C`, TW | **Herzberg 07** | Katsura 10 | Putirka 16 | union | − 1623 K |
|---|---|---|---|---|---|---|---|---|---|---|
| **1400** | **`T_m0`-fixed** | **1668.86** | −3.7007 | 3.057 | 0.405 | **in** | out | in | in | +45.86 |
| 1400 | `r_b`-point | 1668.65 | −3.6995 | 3.057 | 0.405 | in | out | in | in | +45.65 |
| 1500 | `T_m0`-fixed | 1669.04 | −3.7006 | 3.058 | 0.405 | in | out | in | in | +46.04 |
| 1500 | `r_b`-point | 1668.57 | −3.6981 | 3.058 | 0.405 | in | out | in | in | +45.57 |
| 1600 | `T_m0`-fixed | 1669.22 | −3.7006 | 3.059 | 0.405 | in | out | in | in | +46.22 |
| 1600 | `r_b`-point | 1669.22 | −3.7006 | 3.059 | 0.405 | in | out | in | in | +46.22 |
| 1700 | `T_m0`-fixed | 1668.81 | −3.7007 | 3.056 | 0.405 | in | out | in | in | +45.81 |
| 1700 | `r_b`-point | 1668.74 | −3.7003 | 3.056 | 0.405 | in | out | in | in | +45.74 |
| **1800** | **`T_m0`-fixed** | **1668.41** | −3.7008 | 3.054 | 0.406 | **in** | out | in | in | +45.41 |
| 1800 | `r_b`-point | 1668.27 | −3.7000 | 3.054 | 0.406 | in | out | in | in | +45.27 |

**Verdict: 1400 K → 1668.86 K in · 1800 K → 1668.41 K in — the same verdict at both ends, and the
verdict is *in*. Criterion B passes.** With criterion A, **step 0 passes: Earth's declared
`potential_temperature` may be transferred to Mars**, and `engine/bodies/mars.yaml`'s `validated:
pending` becomes a validation.

**Four things that must be read with it.**

- ⚠ **The margin is 4 K on a 120 K band.** The band's top edge is 1673.15 K and the trajectory lands at
  1668.4–1669.2 K, so the headroom is **4.0–4.7 K**. **A 5 K error anywhere in the trajectory flips this
  cell**, so the pass may not be cited as a comfortable one — and C48 has already shown this integrator
  calling its flux law far outside the law's expansion point.
- ⚠ **The four banded candidates do not agree, and the verdict rests on which one the owner picked.**
  *(Four, not three: Herzberg+ 2010's body band arrived after the verdict and is recorded above — the
  count moves, the verdict is not recomputed.)* Herzberg+ 2007, Putirka 2016, Herzberg+ 2010's
  `[1573.15, 1673.15]` and the union all say *in*; **Katsura+ 2010 `[1575, 1645]` puts both ends OUT** —
  because 1668 K is above its top edge. So under the mineral-physics reading of modern Earth this checkpoint
  fails. **The dependence is published, not resolved**, exactly as C47 (g) published step 4's dependence
  on `α`: the owner chose the paper before the column was opened, which is why this is recorded rather
  than re-litigated.
- **The declaration barely moves the checkpoint**: 0.81 K of spread in `T_p@3.7 Ga` across the whole
  400 K sweep, and the two variants agree to ~0.5 K. That is criterion A's 0.0017 slope seen at the
  checkpoint instead of at the present.
- **Earth, in the same run, is at 1824.70 K at 3.7 Ga** (present 1525.46 K, 1152 steps). So Mars at
  3.7 Ga sits ~156 K **below Earth-at-3.7-Ga** while inside **modern** Earth's band. ⚠ That is what
  Monders' sentence says — *similar to those on the **modern** Earth* — and it is what the rule
  implemented; a checkpoint against Earth's own 3.7 Ga state would be a different test and would fail.

**Sampling:** the checkpoint reads the nearest adaptive row. ⚠ *Corrected on the audit seat's
reproduction: the row lands within **0.79 Myr** of −3.7 Ga on the **verdict variant** (`T_m0`-fixed, all five
points), which is what the verdict rests on — but the widest **record** row, `1500 | r_b`-point, is
**1.91 Myr** away (−3.6981 Gyr). "Within 0.8 Myr at every point" was wrong as written; the table's own t
column carried the counter-example.* The sampling gap does not move a cell here — the sweep's whole spread
in `T_p@3.7 Ga` is 0.81 K — but the claim had a scope it did not state.

⚠ **And the ceiling, restated because the pass is thin:** Monders+ 2007's statement is **qualitative**.
It can catch a badly wrong trajectory and nothing finer. **A pass is not a precision validation of the
Martian thermal history**, and at 4 K of headroom it is not even a comfortable qualitative one.

⚠ **And the checkpoint's ceiling, restated so a pass is not over-read** (C47 (h) put it first):
Monders+ 2007's statement is **qualitative** — high `T_p`, *"similar to those on the modern Earth"*,
until 3.7 Ga. It can catch a badly wrong trajectory and nothing finer. **A pass is not a precision
validation of the Martian thermal history.**

#### Four corrections carried by this section

**1. Where 1623 K comes from — the C47 (h) attribution was wrong, and the chain is one link longer.**
⚠ *Settled 2026-09-08 with both papers held:* **1623 K is Herzberg+ 2010's `1350 ± 50 °C`** — itself a
consensus value, carrying seven citations in that sentence (McKenzie & Bickle 1988, Langmuir+ 1992, Kinzler
1997, Herzberg+ 2007, Courtier+ 2007, Lee+ 2009, Gregg+) — **and the range under it is Herzberg+ 2007's
1280–1400 °C**. So Korenaga 2010 §5's attribution to *2007* skips a step: the digits are 2010's, the
supporting range is 2007's. The paragraph below is the trace as it stood before the papers were held. (h) called it *"Korenaga's own
§4 condition"*. Traced: Korenaga 2010 §5 prints *"The reference temperature is set to 1623 K (1350 °C),
which corresponds to the present-day potential temperature of the ambient mantle"* and attributes it to
**Herzberg et al. 2007** — but Herzberg+ 2007's own abstract prints **1280–1400 °C**, and the **1350 °C
at the present** is printed by Herzberg+ **2010**. Korenaga **2009** §4's `ΔT` = 1350 K with `T_s` = 273 K
is a **third** path to the same digits and is a different quantity (a contrast, not a potential
temperature). ⚠ **So three readings in two papers land on 1623 K, and which one step 4 used is not
decidable from the number** — which is exactly `docs/reference/derivation-discipline.md@«A number cannot enter without its label»`.

**2. `h_min_myr` mixes the landing step into the minimum — measured, not argued.**
`engine/core_history.py@«# land exactly on the present»` truncates the final step so the history ends on
t = 0, and that truncated value competes for the minimum. `max_h_over_tau` does not have the defect (the
ratio is taken before the truncation). **On Earth the reported minimum IS the landing step:**

| what | value | where |
|---|---|---|
| `h_min_myr` as `integrate` reports it | **0.249252 Myr** | step **#1152 of 1152**, 1-based — the last one |
| the four steps before it | 4.0000 Myr each | the cap, binding — and **1125 of the 1152** steps run at the cap |
| the actual stiffest step | **0.3929 Myr** | step 0, the first |

⚠ **And that closes an open label.** `engine/tools/adaptive-step-prereg.md@«first steps shrink from 4 Myr to ≈ 0.39 Myr»`
predicted 0.39 Myr and the audit measured a minimum of 0.249 Myr — **two different quantities, not a wrong
prediction.** The prediction is right to three digits (0.3929 Myr); the 0.249 is the landing step. The
pre-registration stays verbatim; the comparison lives here. So Mars's `h_min` 0.0044–0.0053 Myr in the
criterion-A table is read with the same caveat, and nothing downstream uses `h_min` as a physical quantity.

**3. "Mars's 75" is a truncation of 75.8.** The fixed 4 Myr step was `h/τ` = **75.8** on Mars's first
step (τ = 0.0528 Myr at the start), not 75. The three places that print it carry `≈`, so the label is
sound and only the digit is corrected here.

**4. Route (i) is not closed the way (h) says.** (h) states *"Route (i) is closed, and not for want of
looking"* on the ground that no present Martian `T_p` is published. **Re-cited present-day values do
exist** — Yoshizaki & McDonough 2020 ([`2020GeCoA.273..137Y`](https://ui.adsabs.harvard.edu/abs/2020GeCoA.273..137Y), §5.1, held) assumes **~1500 K** as a
present-day areotherm input; Dong+ 2022 ([`2022Icar..38515113D`](https://ui.adsabs.harvard.edu/abs/2022Icar..38515113D), held) uses **1600 K** for *"the average
Martian mantle today"* and the Baratoux curve by epoch (Amazonian ~1600–1650 K, Hesperian ~1650–1700 K).
Both are **model inputs, 100 K apart, and both trace to Baratoux+ 2011**, which Parro+ 2017 warns are
*"volcanic (non-average) regions"*. ⚠ **Baratoux+ 2011 is held since 2026-09-08** (owner-supplied PDF) and
it changes the grade of everything downstream of it:

| what Baratoux+ 2011 gives | value | grade |
|---|---|---|
| epoch-to-epoch **difference** — printed in the text and Methods | *"a total spread of ~80 K"*, and *"a temperature decrease of **80 ± 20 °C**"* | **printed** |
| absolute `T_p` by epoch — **only as contour labels on Fig. 3/4**, never in the text | Amazonian **1611–1678 K**, Hesperian **1649–1673 K**, read off the figures by eye (±10 °C) | ⚠ **figure-read — not a printed value, and it may not enter a board row** |

So the paper's own numeric claim is a **difference**, not a level, and the levels every re-citation quotes
are figure readings. Against those figures **Yoshizaki & McDonough's ~1500 K is more than 100 K below any
contour**, while **Dong+ 2022's 1600 K is an Amazonian volcanic-province value**. ⚠ Baratoux's own
corrigendum (*Nature* **475**, 254) touches only the heat-flow numbers, and this repo cites none of them —
checked. ⚠ **The original claim's core survives — no
Mars `T_p` is measured, because Mars has no present volcanism to record one — but "does not exist in
the literature" is wrong as written**, and the sentence is marked rather than replaced.

#### Recorded only — the convergence branch ⑤ had stopped testing what it registered

**Found while correcting the stale step strings, and it is not a step string.** Pre-registered branch ⑤ is a
**step**-halving convergence test (`engine/core-thermal-history-context-notes.md@«Run the full history at **h, h/2, h/4**»`,
recorded 2026-09-04 as width 0.001 % at **1135 / 2270 / 4540** steps). ⚠ *Two widths appear in these
documents and they are the same test on two days: **0.001 % is the 2026-09-04 record** (the figure the
code and the test carry) and **0.0006 % is the 2026-09-08 re-run** after the restoration, on the same
three step counts. Both are far inside the pre-registered 10 % pass line, so the branch's verdict never
moved.* After Brief 157 `core_history.sweep`
went on passing only `step_myr`, which is now the **cap** in `h = min(cap, 0.1·τ)` — so halving it changed
only the steps where the cap binds, and the recorded counts could not be reproduced. ⚠ **A pre-registered
branch had quietly become a different test, and nothing failed**: the gate does not run `--sweep`, and the
docstring still described the old one.

**Brief 161 restored the registered meaning** — `sweep` runs `adaptive=False` — rather than re-writing ⑤ to
match the code, because *"a branch registered before the adaptive step exists is not re-written afterwards"*.
An adaptive-**cap** sweep is a real question and is **deliberately not built**; it would need its own
registration.

#### The audit seat's independent run, at the same tree

**`test_core_history.py` re-run by a third seat, `rc=0`, digit-for-digit against the C48 row:** Earth
adaptive **1152** steps, max `h/τ` **0.100**, reported minimum `h` **0.249** Myr (the landing step, above);
Earth fixed-step **1135** steps, `T_p` **1525.46** K; Mars adaptive **1382.90 / 3893.01 / 1669.22** K,
**1197** steps, `h_min` **0.0053** Myr. **Runtime 223.66 s** against the ~235 s stated in the commit
message — **−4.8 %**, inside load variation, and reported because
`docs/reference/derivation-discipline.md@«say what your work adds to the gate's time»` asks for it.

#### Waiting on the owner, recorded so neither is decided by a seat

| decision | the two candidates | what turns on it |
|---|---|---|
| ~~criterion B's verdict line~~ | **answered 2026-09-08 17:35: Herzberg+ 2007 [1553.15, 1673.15] K**, the other three record-only | the 3.7 Ga in/out, hence whether the transfer is allowed |
| ~~Mars's declared `potential_temperature`~~ | **answered 2026-09-08 17:52: Earth's 1600 K, transferred (Unterborn+ 2019), in Brief 153's transfer-record form.** The two re-citations (Yoshizaki & McDonough 2020 ~1500 K; Dong+ 2022 1600 K, which agrees) are record columns | ⚠ **nothing in the Mars result** — criterion A's 0.0017 slope means the whole 400 K sweep moves the answer 0.34 K. It was a provenance choice, not an accuracy one |

### C47 (j) 2026-09-08 — step 4 is a build, not a re-run, and this is the head written before anything is computed

**Written at 18:44 KST, before any step-4 quantity was computed.** Brief 160 asked for step 4 to be
re-run with the ninth fixed value (`T_p`) supplied. ⚠ **There is nothing to re-run.** The search was
`step 4` / `단계 4` and `q_Earth/q_Mars` across `engine/` and `docs/reference/`, plus every earlier
seat's scratch directory for a runner or a log:

| what exists | where |
|---|---|
| the pre-registration — four verdict cells, eight fixed values, the target **3.68 / 4.78** from the no-melting **1.372**, the sign convention, the (a)(b)(c) decomposition | C47 (g), committed before the run |
| **step 1** — eq. 29/30/42/43/44 transcribed and checked row by row against Table 2's three `Δη` blocks | `engine/stagnant_lid.py`, `engine/test_stagnant_lid.py` (in the gate) |
| **step 3's dehydration half** — eqs 45/50/51/53/54, 30 rows, no tuned parameter | C47 (f2), same module |
| **step 4's outputs** | ⚠ **not in this repo** — and ⚠ *recovered 2026-09-08 ~21:00 from the 09-07 work seat's transcript (`a0402cc0`) by the directing seat, verbatim with per-block timestamps and tool ids, into `/Users/vana/Desktop/NearStars-artifacts/2026-09-08-c47-step4/c47_step4_recovered.md` (md5 `ce35dc0ad7d084a475b7242af75605d5`) — a durable path, since a scratch directory belongs to one session.* The runner was **two inline `python3 -c` blocks** (16:39:22, which raised `OverflowError`, and 16:39:56, which ran), so nothing of it was ever committed |

⚠ **So C47 (h)'s opening — *"Step 4 ran, its numbers are final"* — points at an artifact this repo does
not hold.** It ran inside the 09-07 seat's transcript, and that transcript — not the repo — is where the
numbers were. That sentence is marked in (h) rather than deleted, and this section exists so the next run
has a head that predates it.

⚠ **What the recovery changes, and what it does not.** The 09-07 outputs now exist as a recovered
artifact, so Brief 162 is *promote the inline runner and reproduce those numbers bit-for-bit*, not
*build from nothing*. ⚠ **And reproducing them proves only that the same code gives the same numbers — it is not a physical
anchor.** The independent legs are the four anchors below, and the load-bearing one is `b` reproducing
50 mW/m² at the paper's Earth condition. **But this seat has now read them**, so they are a
**reproduction anchor, not a blind target** — the head's ordering claim above covers this seat's own computation, which has not
happened, and it may not be read as a claim that the re-run was blind to the recovered values. The
verdict cells in (g) are what they always were: written before any of it.

**What the build must add, counted before it is started** (`engine/stagnant_lid.py`'s own docstring
already says *"차원화는 단계 3–4"* — the module deliberately stops short of a flux):

| # | missing piece | what pins it |
|---|---|---|
| 1 | the fixed-point iteration **`z*_D = Nu⁻¹`** (eq. 56) — `nu_full` today takes `z_d` as an argument and does not iterate it | Korenaga 2009 eq. 56, *"iterated by setting `z*_D = Nu⁻¹` when `Nu > 1/z*_D`"* (C47 (e)) |
| 2 | per-body **`θ`** and **`Ra_i`** from `E`, `T_s`, `ΔT`, `g`, `D`, `κ`, `ρ`, `C_p` | the paper's §4 constant list; ⚠ and the `α` in it is the one the paper contradicts itself on (C47 (g)) |
| 3 | the **`b` normalization** — one global declaration, re-fitted on the paper's own printed Earth condition | C47 (d): *"take Korenaga 2009's own `b`, re-fitted on the paper's own printed Earth condition … as one global declaration for every body"*. ⚠ Width unquantified by the paper, and `q ∝ b^{−β/n}` — a decade of grain size is 2.15× in flux |
| 4 | **`Nu → q`** dimensionalization | `q = Nu · k ΔT / D`, with the absolute scale carried by 3 |

**⚠ The pre-registration is not touched.** (g)'s four cells, eight fixed values, target, sign
convention and decomposition stand **verbatim** — no re-registration, no widening, and **whichever cell
the result lands in, that cell's sentence is the verdict.** If it lands outside all four, the table is
recorded and the verdict is left to the owner rather than invented here.

**The ninth fixed value, which is why (h) held the verdict — both bodies, with their labels:**

| body | `T_p` | provenance |
|---|---|---|
| Earth | **1600 K** | declared, Unterborn+ 2019 §2 (`engine/eos.py@«EARTH_POTENTIAL_T = 1600.0»`) |
| Mars | **1600 K** | Earth's value **transferred**, `engine/bodies/mars.yaml` at `4ad07b07`; step 0 passed (criterion A max \|slope\| 0.0017, criterion B in at both ends) and the owner chose the transfer over the ~1500 K re-citation at **17:52** |

⚠ **The two being equal is the thing (h) warned about, and it is now a measured choice rather than an
implementation accident.** Criterion A measured that Mars's trajectory forgets this declaration —
0.0017 K of output per K of declaration — so a common `T_p` is no longer removing the physics the test
measures **by assumption**; it is doing so, if at all, at a rate step 0 bounded.

**How the build gets verified before it is run.** Four anchors, three of them named in C47 (e) before
any of this:

| anchor | what it checks |
|---|---|
| `Ra_i` over `T_i` = 1200–1800 °C against §4.1's printed *"∼10⁹ to ∼10¹³"* | the `θ`/`Ra_i` chain |
| `Ra_crit(n)` against the text's *"∼450 (n = 1), ∼134 (n = 2), ∼104 (n = 3)"* | eq. 44, already passing at n = 1 and 3 |
| Table 2's three `Δη` blocks, row by row | the stability solve, already in the gate |
| **`b` reproducing 50 mW/m² at the Earth condition** — by construction, so a miss means the dimensionalization is wrong | the new piece, and the only anchor the absolute scale has. ⚠ *Sharpened in (k) commit 3: the paper defines this on **eq. 30 without melting**, so the anchor reads `q_E` = 50.000 ± 10⁻³ **evaluated that way** — not on the eq. 29 path the runs use, which sits 3.98 % higher by construction* |

**⚠ And there is no absolute-scale anchor beyond that one, by the paper's own doing:** §4's planetary
results are **Figs 12–14 only**, with no printed dimensional flux. That was C47 (e)'s size verdict and
it has not changed.

**Carried in the same commit, because they touch the same file: the audit seat's three findings on
C47 (i).** Three bibcodes that carried no clickable link now have one (Putirka 2016, Yoshizaki &
McDonough 2020, Dong+ 2022); the banded-candidate count moves from three to **four**, since Herzberg+
2010's body band is now recorded — ⚠ *the count moves, the agreement test is still not recomputed*; and
Herzberg+ 2007's citation is pinned by its own sentence rather than by the words *"concluding
paragraph"*. ⚠ **One count is worth keeping beside them: the audit seat counted twelve distinct edits in
`8d83b03d` where this seat's report grouped them as seven.** Same work, but the smaller number is the
one that would leave a reader thinking less had changed — a report's grouping is not a count.

**This section is the head. The build is Brief 162**, and the recovery settles how it starts: the
inline runner is promoted to engine code, re-verified against the four anchors above rather than
trusted, and re-run at the two `T_p` labels. ⚠ **Three things in the recovered runner are questions for
that brief, named here before it starts** — it fits `b` with eq. 30 (`nu_asymptotic`) while every run
uses eq. 29 with the stability solve (`nu_full`), which is why its Earth flux comes out at 52 rather
than the 50 mW/m² it was fitted to — ⚠ *withdrawn in (k) commit 3: that fit is the paper's own printed
definition, and the 52 is the eq. 29 − eq. 30 difference*; it hardcodes `α = 2 × 10⁻³` inside `Ra_i` while sweeping `α` only
in the buoyancy term, so the paper's self-contradiction is resolved *two ways at once inside one run*;
and it sets `z*_D` from the melting-onset depth instead of iterating eq. 56's `z*_D = Nu⁻¹`, which is
missing piece 1 above. **None of these is a reason to discard it** — it is the fastest route to a
reproducible step 4 — but each must be decided in the open rather than inherited.

### C47 (k) 2026-09-08 — step 4's runner is promoted with its defects, and the 09-07 numbers reproduce

**Brief 162 commit 1. What is promoted is the 09-07 work seat's second inline block, arithmetic
unchanged**, from the recovery in C47 (j)
(`/Users/vana/Desktop/NearStars-artifacts/2026-09-08-c47-step4/c47_step4_recovered.md`, md5
`ce35dc0ad7d084a475b7242af75605d5`). It now lives in `engine/stagnant_lid.py` as four functions and
six constants plus `engine/tools/c47_step4.py`, and the tool checks every printed number of that run.

⚠ **What this reproduction is, and what it is not.** *It confirms that the same code produces the same
numbers — that promotion did not damage anything.* **It is not a physical anchor.** The independent
legs are the four anchors C47 (j) named, and the load-bearing one is **`b` reproducing 50 mW/m² at the
paper's own Earth condition** — ⚠ *which the promoted code passes exactly, once the anchor is read the
way §4 defines it (eq. 30, no melting): 50.0000 mW/m². The 52.02 in the runs is the eq. 29 − eq. 30
difference, not a missed fit — commit 3 below.* Commits 2–5 repair one defect each; the physics is
tested there, not here.

⚠ **And the blinding scope, stated as in (j):** this seat read the recovered numbers before writing the
runner, so they are a **reproduction anchor, not a blind target.** (g)'s four verdict cells predate all
of it, and the verdict is not written in this section.

#### The 09-07 numbers, reproduced

`b` = **4.1921 × 10¹⁰** (one global declaration, re-fit on the paper's Earth condition). Target
`q_Earth/q_Mars` = **3.68** (against our 0.454) or **4.78** (against Korenaga's 0.35), from the
no-melting baseline **1.372** — all three fixed in C47 (f)/(g) before any of this.

| `T_p` | body | depleted layer | as % of mantle | `z*_D` |
|---|---|---|---|---|
| 1350 °C | Earth | 61.8 km | 2.13 % | 0.9787 |
| 1350 °C | Mars | 163.8 km | 9.10 % | 0.9090 |
| 1500 °C | Earth | 108.2 km | 3.73 % | 0.9627 |
| 1500 °C | Mars | 286.7 km | 15.93 % | 0.8407 |

| `T_p` | `α` | run | `q_E` | `q_M` | **`q_E/q_M`** | `Ur_E` | `Ur_M` | `Ur_M/Ur_E` |
|---|---|---|---|---|---|---|---|---|
| 1350 °C | §3.2 `3.7e-5` | (a) dehydration only | 52.02 | 29.17 | **1.7832** | 0.803 | 0.612 | 0.762 |
| 1350 °C | §3.2 | (b) buoyancy only | 52.02 | 35.90 | **1.4492** | 0.803 | 0.498 | 0.619 |
| 1350 °C | §3.2 | **(c) both** | 52.02 | 29.17 | **1.7832** | 0.803 | 0.612 | 0.762 |
| 1350 °C | §4 `2.0e-3` | (a) | 52.02 | 29.17 | **1.7832** | 0.803 | 0.612 | 0.762 |
| 1350 °C | §4 | (b) | 52.04 | 39.06 | **1.3323** | 0.803 | 0.457 | 0.569 |
| 1350 °C | §4 | **(c)** | 52.02 | 29.17 | **1.7832** | 0.803 | 0.612 | 0.762 |
| 1500 °C | §3.2 | (a) | 51.04 | 23.42 | **2.1791** | 0.819 | 0.763 | 0.931 |
| 1500 °C | §3.2 | (b) | 105.33 | 77.74 | **1.3549** | 0.397 | 0.230 | 0.579 |
| 1500 °C | §3.2 | **(c) both** | 51.04 | 22.79 | **2.2396** | 0.819 | 0.784 | 0.957 |
| 1500 °C | §4 | (a) | 51.04 | 23.42 | **2.1791** | 0.819 | 0.763 | 0.931 |
| 1500 °C | §4 | (b) | 120.93 | 89.01 | **1.3586** | 0.346 | 0.201 | 0.581 |
| 1500 °C | §4 | **(c)** | 51.04 | 23.41 | **2.1800** | 0.819 | 0.763 | 0.932 |

**Seventeen anchors — twelve run cells, four depleted layers and `b` — all reproduce at the printed
precision** (`✅ 09-07 앵커 17/17 일치`, `rc=0`), and `engine/tools/c47_step4.py` exits `rc=1` if any of them moves. ⚠ **No verdict is read
off this table**, because four defects sit between it and the physics.

#### ⚠ The (g) fourth cell's premise is falsified, and (g) registered how to record that

C47 (g) reasoned that dehydration stiffening and compositional buoyancy *"push in opposite directions
on the asymmetry"*, and registered the consequence in advance: *"if (a) and (b) turn out to push the
**same** way, the fourth cell's reasoning is wrong and that gets recorded as this seat's error."*

**They push the same way.** Against the no-melting **1.372**, dehydration alone gives **1.7832** and
buoyancy alone **1.4492** — both **above** it, so by (g)'s own sign convention both mechanisms *help*.
**So the reasoning behind the fourth cell was wrong, and it is recorded here as the 09-07 seat's error,
in the form that seat registered for it.**

⚠ **What is true instead is stranger, and it is visible in the same rows.** At 1350 °C, **(c) equals
(a) to four decimals** (1.7832): with dehydration on, buoyancy adds *nothing at all*. At 1500 °C it
adds a little (2.2396 against 2.1791) under §3.2's `α` and almost nothing (2.1800) under §4's. And
(b)'s own absolute fluxes are the loudest thing in the table — 105.33 and 120.93 mW/m² on Earth, twice
the other rows — because with `Δη = 1` the dehydrated lid is not stiff and the flux is not suppressed.
**So the mechanisms do not oppose; the stiff lid dominates, and once it is on the density contrast is
nearly invisible.** That is a finding about the mechanisms, and it is not a verdict on the target.

#### Commit 2 — defect ④ repaired: one surface temperature, and the prediction held

**Registered before the run: Earth's flux moves by ≪ 1 %.** With `T_s` unified to a single 273.15 K —
so `ΔT` = `T_p` exactly and the `b` fit sits on the same condition the runs do — the twelve runs move
like this.

⚠ **Why 273.15 and not the paper's printed 273, stated because the paper is the source of the
ambiguity.** §4 prints the Earth condition as `T_s` = **273 K**, `ΔT` = **1350 K**, `T_i` = **1350 °C** —
mutually inconsistent by 0.15 K (1623.15 − 273 = 1350.15). Two resolutions exist: `T_s` = 273.15 makes
`ΔT` = `T_p` exactly and so reproduces **the paper's `ΔT` = 1350 K** exactly, while `T_s` = 273.0
reproduces the paper's printed `T_s` and leaves `ΔT` at 1350.15. **We take the first**, because `ΔT` is
the quantity the equations evaluate. Either way the fit and the runs now share one condition, which is
what defect ④ was about.

| what | before (09-07) | after | move |
|---|---|---|---|
| `b` | 4.1921 × 10¹⁰ | **4.2038 × 10¹⁰** | +0.28 % |
| `q_E` at 1350 °C | 52.02 | **51.98** | −0.04 mW/m² = **−0.08 %** |
| `q_E` at 1500 °C | 51.04 | **51.03** | −0.01 mW/m² = **−0.02 %** |
| `q_E/q_M` (c), 1350 °C | 1.7832 | **1.7823** | −0.0009 |
| `q_E/q_M` (c), 1500 °C | 2.2396 | **2.2398** | +0.0002 |
| depleted layers, all four | 61.8 / 163.8 / 108.2 / 286.7 km | **unchanged** | `z*_D` does not read `T_s` |

**The prediction held**, and the largest move anywhere in the table is `q_E` in the buoyancy-only rows
(105.33 → 105.23 and 120.93 → 120.81 mW/m², −0.1 %). ⚠ **No verdict is read here either** — this
subsection reports one change's size and nothing else.

⚠ **And the runner proved it can fail as well as pass**: `--anchors` returned `rc=0` at `aea75984` and
`rc=1` here, which is `docs/reference/derivation-discipline.md@«A check must prove it can pass and can fail before its result is written down»`
applied to the tool that guards the rest of this brief.

#### Commit 3 — defect ① is withdrawn: the eq. 30 fit is what the paper prints

**Read before repairing, and the repair turned out to be the mistake.** §4, printed:

> *"the pre-exponential factor `b` in eq. (1) is determined so that the surface heat flux is
> **50 mW m⁻²** at the present-day Earth condition (`D` = 2900 × 10³ m, `g` = 9.8 m s⁻², `T_s` = 273 K,
> and `ΔT` = 1350 K) **without the effects of mantle melting (i.e. Δη = 1 and Δρ = 1)**"*

and Fig. 12's caption — *"Reference viscosity is chosen so that **conventional scaling** predicts
surface heat flux of 50 mW m⁻² at `T_i` = 1350 °C"* — with the body naming *"the conventional scaling of
`Ra_i` (**eq. 30**)"*. **So fitting `b` on eq. 30 with melting off is the paper's own definition, and the
09-07 runner did what the paper says.**

| what | value |
|---|---|
| `q_E` at the paper's Earth condition **evaluated on eq. 30** (the definition) | **50.0000 mW/m²** — by construction |
| `q_E` on **eq. 29 + the stability solve**, melting off, same `b` | **51.9919 mW/m²** — **+3.98 %** |
| `b` if it were re-fitted on the eq. 29 path instead | 4.7452 × 10¹⁰ (**×1.1288** of 4.2038 × 10¹⁰) |
| what eq. 30 would then read — the departure from the paper's normalization | **48.0211 mW/m²** |
| effect on the verdict quantity (`q_E/q_M`, 1350 °C, (c), §3.2) | 1.7823 → **1.7311**, −2.9 %, **away from the 3.68 / 4.78 target** |

**So the choice is about faithfulness, not about the verdict**: `b` is one global declaration entering
both bodies, so the ratio barely moves — C47 (f) had already measured that at 3.7 % per decade of `b`
against 115 % for the absolute flux. **The paper's definition is kept, the alternative is recorded, and
nothing is re-fitted.**

⚠ **Whose error this was, recorded where the others are.** The pass line *"`b` reproduces 50 mW/m²"* was
set as an anchor in C47 (j) without checking which equation the paper normalizes on; **that was the
directing seat's — and the audit seat approved the same pass line, so two of the three legs were wrong
together**, which is the failure mode three separate legs exist to prevent. It is written here rather
than left in a message. The anchor is not deleted but sharpened: **`q_E` = 50.000 ± 10⁻³ evaluated on
eq. 30**, which the code passes.

⚠ **And the reclassification costs us an anchor, which has to be said plainly.** If `b` is *defined* by
"eq. 30, no melting, Earth = 50 mW/m²", then reproducing 50.000 at that condition is **a definition, not
a verification** — C47 (e)'s fourth anchor was never an anchor. **So the absolute scale has no
independent check at all**, exactly as (e) said when it noted that §4's planetary results are Figs 12–14
with no printed dimensional flux. The independent legs are **three**: `Ra_i`'s printed range over
`T_i` = 1200–1800 °C, `Ra_crit`'s ∼450 / 134 / 104, and Table 2's three `Δη` blocks row by row.

**That weakness does not reach the verdict, and the reason is structural.** The verdict cells read
`q_Earth/q_Mars` and `Ur_M/Ur_E` — **ratios** — and `b` is one global constant entering both bodies
identically, so it cancels to first order: C47 (f) measured the ratio's sensitivity at **3.7 % per decade
of `b`** against **115 %** for the absolute flux. **An unanchored absolute scale is a real limit on any
flux we would emit, and not a limit on the direction test.**

⚠ **And this is the ninth time today that reading the thing before building it changed the build** —
after existing code four times, a declared limit, a paper's own sentence, our own rule, and the recovery
that turned "build from nothing" into "promote and reproduce". **None of the nine was caught by the
gate.**

#### Commit 4 — defect ② repaired, and the repair proves the defect could not have mattered

**`α` now enters `Ra_i` as an argument, and `b` is fitted with the same `α`** — self-consistently, which
is the only way a normalization and the constant it normalizes can be read together. **The result is
that nothing moves, and that is the finding:**

| `α` | `b`, fitted with that `α` | `Ra_i` at the Earth condition | `q_E` (c), 1350 °C | `q_E/q_M` |
|---|---|---|---|---|
| §4's `2.0 × 10⁻³` | 4.203785 × 10¹⁰ | 1.360020 × 10¹⁰ | 51.9758 | 1.782288 |
| §3.2's `3.7 × 10⁻⁵` | **7.777002 × 10⁸** | **1.360020 × 10¹⁰** | **51.9758** | **1.782288** |
| ratio | **1.850000 × 10⁻²** | identical to every digit | identical | identical |

⚠ **`Ra_i ∝ α/b`, and `b` is fitted at the Earth condition, so `α` is absorbed by `b` exactly.** ⚠ *And
the claim holds only under that condition: **`α` is invisible through `Ra_i` while `b` is obtained by
fitting a fixed Earth condition.** Take `b` any other way — a literature value, a per-body grain size —
and the `Ra_i` path opens again silently. The sentence must never be written without that clause.* The `b`
ratio equals the `α` ratio to six digits (1.85 × 10⁻²), `Ra_i` is unchanged to every printed digit, and
all twelve runs are bit-identical to commit 3's. **So the paper's `α` self-contradiction cannot act
through `Ra_i` at all — it can only act through `ΔT*_ρ`**, which is where C47 (g) put it. `α` and `b` are
not separately identifiable, and the paper itself calls its normalization *"(arbitrary)"*.

⚠ **This means the split the audit seat proposed as commit 4's pass line — §3.2 and §4 giving different
`q_E` in the (a) rows — cannot happen, and its absence is not evidence that the argument was left
unwired.** The wiring is visible in the `b` column instead: two `α` values now produce two `b` values in
the ratio 1.85 × 10⁻², where before commit 4 there was one `b` for both.

**The counterfactual, recorded because it is the only way `α` in `Ra_i` bites.** ⚠ *Label first, because
"the paper's `b`" would be false: `b` is **not** printed anywhere in Korenaga 2009 — it is **our** global
declaration, fitted to the paper's Earth condition (C47 (d)). What is held fixed below is therefore
`b` = 4.203785 × 10¹⁰, the value fitted with §4's `α`. And the two rows were measured in scratch: **the
shipped code has no `b`-freeze mode**, by design, since freezing it is the mixing commit 4 exists to
prevent.* With that `b` held and `α` in `Ra_i` moved to §3.2's, `Ra_i` falls 54×:

| case, `α` in `Ra_i` only | `q_E` 1350 °C | `q_M` | `q_E/q_M` | `Ra_i` (Earth) |
|---|---|---|---|---|
| 2.0 × 10⁻³ (paper's `b` and `α` together) | 51.9758 | 29.1624 | 1.7823 | 1.360 × 10¹⁰ |
| 3.7 × 10⁻⁵ with the paper's `b` kept | **15.0253** | 12.5636 | **1.1959** | 2.516 × 10⁸ |

⚠ **And that case falls *below* the no-melting 1.372**, so even the mixed reading moves away from the
target. It is recorded, not adopted: mixing a `b` fitted at one `α` with runs at another is the thing
commit 4 exists to stop.

**One thing this settles in the good direction.** The `α` ambiguity's blast radius is now bounded: with
`b` fitted per `α` and eq. 56 solved, the two `α` values give **identical `q_E`, `q_M` and ratios in the
(a) and (c) rows to four decimals**, and differ **only in the buoyancy-alone (b) rows**. **So C47 (g) was
right, after the fact, to put `α` on the buoyancy axis** — the axis it registered as the one `α` could
move is the only axis `α` moves.

#### Commit 5 — defect ③ repaired: eq. 56's fixed point, and it takes the 1500 °C asymmetry away

**The recursion, as the paper states it.** §3.1: *"when the dehydrated layer becomes dynamically
unstable, that is, `Nu > 1/z*_D`, we can modify the depth-dependent viscosity"*, solved
*"recursively … until `Nu` converges. The convergence is usually achieved within a few iterations"*; §4:
*"eq. (56) is solved iteratively by setting `z*_D = Nu⁻¹` when `Nu > 1/z*_D`, to have a self-consistent
pair of the surface heat flux and the assumed viscosity and density structure."*

⚠ **The paper uses `z*_D` in two senses, and its own numbers say which sense the trigger takes.** This
was first written up as *our* reading justified by the alternative being implausible. Korenaga 2009 is
**held**, so it was read, and the grade improves: **the prose defines a coordinate, the numbers require a
thickness.**

**The chain, four printed steps and one confirmation.**

1. ⚠ **`δ` is a thickness, and `z*` increases upward — printed under eq. 20.** *"`T_i − T_s` =
   `1/(1−δ) ∫₀^{1−δ} T dz*`"*, and then: *"where **δ = Nu⁻¹** = (T_i − T_s)/ΔT_H. **The
   non-dimensionalized thickness of the top thermal boundary layer is the reciprocal of the Nusselt
   number**, and the internal temperature is defined as the average of temperature below the boundary
   layer."* The integral runs **0 → 1−δ** with prefactor `1/(1−δ)`, so the interior is `z* ∈ [0, 1−δ]`
   and **the boundary layer is the top slab `z* ∈ [1−δ, 1]`**.
2. **Eq. 47 puts the dehydrated layer at `z* > z*_D`** — `Z(z*)` is 1 below and `Δη` above — so there
   `z*_D` is a **coordinate** and the layer's **thickness is `1 − z*_D`** (Table 2's 0.75 → a lid 0.25
   thick).
3. **Eq. 49 substitutes a length into that slot**: *"self-consistent and solve the following equation
   recursively: `Nu = F_Nu(n, θ, Ra_i, Δη, Nu⁻¹)`, until `Nu` converges."* Eq. 48's fifth argument is
   `z*_D`; eq. 49's is `Nu⁻¹` = `δ`.
4. **So the trigger's `z*_D` is a thickness, by arithmetic on 1–3.** *"Is the dehydrated layer thicker
   than the boundary layer?"* is `1 − z*_D > δ`, i.e. `Nu > 1/(1 − z*_D)` — and the paper writes that
   condition as **`Nu > 1/z*_D`**. ⚠ **The symbol carries both senses in the paper's own text**, which
   is why the overload is the paper's and not our reading.
5. **Table 2 confirms which sense discriminates.** On our 30 transcribed rows (`Δη` = 1, 3, 10; `Nu`
   **3.09–7.22**): the coordinate threshold `1/0.75` = **1.333** has **0 rows below, 30 above** — the
   trigger would be permanently true and §3.1's two regimes, *"reduces surface heat flux even when the
   dehydrated lid is thinner"* versus *"eventually destabilized"*, could not both exist. The thickness
   threshold `1/(1 − 0.75)` = **4.0** has **15 below, 15 above**, and `δ = 1/Nu` (**0.1385–0.3236**)
   straddles the lid thickness 0.25 **15/15**. Fig. 8(a)'s caption puts its horizontal line
   `Nu = 1/z*_D` in the middle of the figure, not off its bottom edge.

**And the code already carries step 1's geometry:** `engine/stagnant_lid.py@«above = max(0.0, min(top, 1.0) - max(1.0 - delta, z_d))»`
measures the stiff share of a sublayer as the part above `z_d`, with the boundary layer occupying the
top `δ` — the same convention, written before any of this was read.

**So the overload is the paper's**, and it belongs beside its `α` self-contradiction (defect #24) rather
than in our list of reading choices. The implementation uses the thickness sense for the trigger and the
update, and the boundary-coordinate sense for `nu_full`'s geometry, which is what Table 2 fixes;
`nu_eq56` converts (`1 − thickness`).

**The third possibility, checked and closed:** the `Nu` in the trigger could have been a different
normalization from the one `nu_full` returns, which would dissolve the "always fires" objection. It is
not — the paper defines `Nu` as `δ⁻¹`, and `nu_stability` solves eq. 43 for `δ` and returns `δ⁻¹`.

**Under the thickness sense the trigger fires in 10 of the 24 body-cells** — two at 1350 °C (Mars's
buoyancy-only rows) and eight at 1500 °C (all three Mars runs plus Earth's buoyancy-only, both `α`).
⚠ *Corrected on the audit's count: "four of twelve" had mixed this up with the number of **cells that hit
the 50-iteration cap**, which was also four.*

| where it fires | initial `d/D` | `1/(d/D)` | `Nu` before | fires? |
|---|---|---|---|---|
| Earth, 1350 °C, (a)/(c) | 0.0213 | 46.89 | 27.91 | no |
| Mars, 1350 °C, (a)/(c) | 0.0910 | 10.99 | 9.72 | no |
| Mars, 1350 °C, (b) | 0.0910 | 10.99 | — | **yes** |
| Earth, 1500 °C, (a)/(c) | 0.0373 | 26.80 | 24.66 | no |
| **Mars, 1500 °C, all three** | 0.1593 | 6.28 | 6.83–7.02 | **yes** |
| Earth, 1500 °C, (b) | 0.0373 | 26.80 | — | **yes** |

**What it does to the twelve runs:**

| `T_p` | run | `q_E/q_M` before | after | move |
|---|---|---|---|---|
| 1350 °C | (a), (c), both `α` | 1.7823 | **1.7823** | unchanged — does not fire |
| 1350 °C | (b) §3.2 | 1.4492 | **1.4276** | −0.0216 |
| 1350 °C | (b) §4 | 1.3323 | **1.3319** | −0.0004 |
| **1500 °C** | **(a), both `α`** | 2.1791 | **1.5838** | **−0.5953** |
| **1500 °C** | **(c) §3.2** | 2.2396 | **1.5838** | **−0.6558** |
| **1500 °C** | **(c) §4** | 2.1800 | **1.5838** | −0.5962 |
| 1500 °C | (b) §3.2 / §4 | 1.3549 / 1.3586 | 1.3467 / 1.3584 | −0.0082 / −0.0002 |

⚠ **And at the verdict temperature eq. 56 never fires — so commit 5 moved the exploratory column and
left the verdict cells untouched.** At the declared 1600 K (1326.85 °C) the dehydrated layer is thinner
than the boundary layer on both bodies: Earth `1/(d/D)` = **53.03** against `Nu` = **24.67**, Mars
**12.43** against **10.13**, and the recursion exits at zero iterations in all 24 declared-`T_p` cells.
**Commit 6's 1.5114 is the same number before and after this repair**, which is worth knowing before
anyone reads the verdict as resting on eq. 56.

⚠ **The self-consistent lid is thinner, so Mars leaks more**: at 1500 °C Mars's dehydrated layer falls
from 15.93 % of the mantle to **10.35 %** and its flux rises **22.79 → 32.22 mW/m²**, while Earth's is
untouched at (a)/(c). **The 1500 °C column, which had been the best case for the test, loses most of its
asymmetry.** The largest `q_E/q_M` anywhere in the table is now **1.7823**, at 1350 °C — **48 % of the
3.68 target and 37 % of the 4.78 one.**

⚠ **And the paper's "a few iterations" is not our experience, which is worth recording as a limit of the
transcription rather than of the paper.** The `(b)` rows converge in **4–14** iterations, as advertised.
The `Δη = 100` rows at 1500 °C take **117–129**, and the rate is linear with a ratio that **drifts
upward**: `Nu·z*_D − 1` falls by **0.66–0.73× over the first four steps, 0.8194× at the fifth — one step, not a
stretch — and 0.8466× from the sixth to the end** (measured on Mars 1500 °C (a): residuals
1.187 × 10⁻¹ → 7.892 × 10⁻² → 5.404 × 10⁻² …). ⚠ *"≈ 0.82 through the middle" was a single point written
as an interval; corrected on the audit's trace.* At the tail rate 10⁻¹⁰ needs **~125** steps, which is what the observed 117–129
are. ⚠ *Corrected on the audit's measurement: "≈ 0.7× and ~60 steps" read the early rate as if it were
the asymptotic one.* **The cap was 50 and four cells hit it**; it was raised to **400** after the rate was measured, and `nu_eq56` reports `converged: False`
rather than returning a number if it is ever hit. **The runner now takes ~61 s.**

⚠ **And the reason the paper's "few iterations" does not describe our runs is that the recursion is
running outside the region the paper exercised** — the same shape of finding as C48, where two of one
paper's numbers failed to compose on a second body. The paper's claim of *"trivial differences (< 0.1 per
cent)"* is made for `Δη` ≤ 10 with Table 2's `Nu` of **3.09–7.22** (our 30 transcribed rows). **We run
`Δη` = 100 at `Nu` = 9.67–27.9** — **10× outside in `Δη`, 1.3–3.9× outside in `Nu`** — and there the recursion is not trivial: Mars at 1500 °C moves its
dehydrated layer from **15.93 % to 10.35 %** of the mantle and its flux by **+41 %**. **That is an
extrapolation, and it is a limit on the 1500 °C exploration rather than on the verdict** — at the
declared 1600 K the trigger never fires (above), so the verdict cells contain no extrapolated
recursion.

#### Commit 6 — the verdict: neither `α` reaches the target, which is C47 (g)'s first cell

**Run at the declared potential temperatures, read from the body files rather than typed in: Earth
1600 K (Unterborn+ 2019, `engine/eos.py@«EARTH_POTENTIAL_T = 1600.0»`) and Mars 1600 K (transferred,
step 0 passed, owner 2026-09-08 17:52).** ⚠ *Both declarations are the same number today, so this set
coincides with a common-`T_p` case — **because Mars carries Earth's value, which is a provenance fact,
not a physical coincidence.** The moment Mars gets a Martian `T_p`, this set separates from the common
one.* In °C, which is what eq. 45 takes: **1326.85 °C** for both.

| body | depleted layer | as % of mantle | `z*_D` |
|---|---|---|---|
| Earth | 54.7 km | 1.89 % | 0.9811 |
| Mars | 144.8 km | 8.05 % | 0.9195 |

| `α` | run | `q_E` | `q_M` | **`q_E/q_M`** | of 3.68 | of 4.78 | `Ur_E` | `Ur_M` | `Ur_M/Ur_E` |
|---|---|---|---|---|---|---|---|---|---|
| §3.2 `3.7e-5` | (a) dehydration only | 45.15 | 29.87 | **1.5114** | 41.1 % | 31.6 % | 0.926 | 0.598 | 0.646 |
| §3.2 | (b) buoyancy only | 45.15 | 32.67 | **1.3818** | 37.5 % | 28.9 % | 0.926 | 0.547 | 0.591 |
| §3.2 | **(c) both — the test** | 45.15 | 29.87 | **1.5114** | **41.1 %** | **31.6 %** | 0.926 | 0.598 | 0.646 |
| §4 `2.0e-3` | (a) | 45.15 | 29.87 | **1.5114** | 41.1 % | 31.6 % | 0.926 | 0.598 | 0.646 |
| §4 | (b) | 45.15 | 34.09 | **1.3243** | 36.0 % | 27.7 % | 0.926 | 0.524 | 0.566 |
| §4 | **(c) both** | 45.15 | 29.87 | **1.5114** | **41.1 %** | **31.6 %** | 0.926 | 0.598 | 0.646 |

**The verdict, read off C47 (g)'s pre-registered table and not composed here.** The target was
`q_E/q_M` ≥ **3.68** (against our own `Ur_Earth` 0.454) or **4.78** (against Korenaga's 0.35), from the
no-melting **1.372**. The best cell is **1.5114**, both `α`, so:

> **neither `α` reaches the target** → the **fourth** law family to fail in the same direction. C47
> closes as *named, not filled* — the recorded answer becomes "no single untuned law in this literature
> reproduces both Urey ratios", and the three-families-same-direction note in C47 (c) closes with it

*(quoted in C47 (g)'s own formatting; the words are unchanged from that cell.)*

**Said in Urey terms, which is where the failure is legible.** The law hands Earth `Ur` = **0.926**
against a literature 0.35–0.454, and Mars **0.598** against 0.68–0.75 — so it makes **Earth** look like
the body that retains its heat and **Mars** the one that has cooled, `Ur_M/Ur_E` = **0.646** where the
literature wants roughly 1.5–2.1. ⚠ **The melting correction moved the ratio the right way** (1.372 →
1.5114, +10 %) **and by nowhere near enough**, and eq. 56's self-consistency took back most of what the
1500 °C case had appeared to offer.

**What this closes and what it does not.** It closes step 4, and with it C47 as *named, not filled*.
⚠ **C34 and C46 are not touched here** — the candidate set C34 waits on is re-drawn by this result, and
that is the next brief's work, not this section's. **Nothing in `db/`, no board row and no emitted value
depends on any number above**; the step-4 path has never had a consumer.

⚠ **And the honest limit on all of it, restated because a closing section is where it would be
dropped:** the absolute scale has **no independent anchor** (commit 3), so these fluxes are not a
prediction of anyone's heat flow — the verdict rests on the **ratio**, which is what the pre-registration
put the threshold on.

#### Commit 7 — the gate now checks step 4, and the two references are kept apart

**Two reference tables, and the distinction is the point.** `ANCHORS` holds the 09-07 run's printed
numbers and is **frozen** — it passes only at `aea75984`, because commits 2–6 repaired defects and the
numbers were *supposed* to move. `EXPECTED` holds **this commit's** numbers and is updated whenever a
change is justified. **`--anchors` demands the first; the default mode demands the second, and the gate
runs the default.**

⚠ **Why both are needed, stated as the failure each one prevents.** Keeping only the frozen anchors
means every commit after the first reports a red herring, so the check gets ignored. Updating the
anchors each commit means they stop being anchors — there is then nothing that says the promotion was
faithful. And having no current table at all is the hole this commit closes: **a regression in
`stagnant_lid.py` would have passed the gate silently**, since nothing in the gate evaluated step 4.

| mode | reference | cells | verdict at this commit |
|---|---|---|---|
| default (in the gate) | `EXPECTED` + `DEPLETED_EXPECTED`, current | **26** | **`rc=0`** |
| `--anchors` | `ANCHORS` + `DEPLETED_ANCHORS`, 09-07, frozen | **17** | **`rc=1`** — 13 cells moved, as commits 2–6 intended |

⚠ **Two holes in the first version of this check, found by the audit seat.** The depleted-layer
comparison sat **inside the `if not quiet:` block**, so the gate — which runs `--quiet` — never evaluated
it: printing and checking were one statement, and silencing one silenced the other. And the
**declared-`T_p` depleted layers were in no table at all** (Earth 54.7 km / 1.89 %, Mars 144.8 km /
8.05 %), so the verdict set's geometry was unguarded. Both are now checked in both modes, which is why
the default count is **26** and not the 24 first reported here.

**Cost, stated because the discipline asks for it: ~62 s added to the gate**, which is eq. 56's fixed
point iterating 117–129 times in the four `Δη = 100` rows at 1500 °C. `scripts/check.sh@«C47 4단계 방향 시험 (브리프 162)»`
carries the same number beside the call.

#### Where the checks were wrong, recorded because two of three legs failed together

**Four pass lines set by other seats were withdrawn on evidence during this brief**, and they are worth
listing beside this seat's own errors:

| pass line | withdrawn because |
|---|---|
| *"`b` must reproduce 50 mW/m²"* on the eq. 29 path — **directing seat, approved by the audit seat** | §4 defines the normalization on eq. 30 without melting; the 52 is the two equations' difference (commit 3) |
| *"the (a) rows must split between the two `α`"* — audit seat | `Ra_i ∝ α/b` and `b` is fitted, so `α` is absorbed exactly; the split cannot occur (commit 4) |
| *"Table 2's `Nu` is 2.76–6.03"* — audit seat | that is Table **3**; Table 2's 30 rows are 3.09–7.22 |
| *"our runs are at `Nu` 24–45"* — audit seat | a flux converted as if it were a `Nu`; the `Δη` = 100 cells are 9.67–27.9 |

⚠ **The first line is the one to keep: the directing seat set it and the audit seat approved it, so two of
the three legs were wrong at once** — and what caught it was neither leg but **reading the paper before
repairing the code**. Three legs are not three checks when two of them share a reading.

#### The four defects, named before any of them is repaired

| # | defect | why it matters | repaired in |
|---|---|---|---|
| ~~①~~ | `b` is fitted with **eq. 30** (`nu_asymptotic`) while every run uses **eq. 29 + the stability solve** (`nu_full`) | ⚠ **withdrawn — not a defect.** §4 defines the normalization exactly this way, and the 52 is the two equations' difference. Commit 3 records it instead of repairing it | ⚠ **no repair** |
| ② | `Ra_i` hardcodes **`α = 2 × 10⁻³`** (§4's printed value) while `α` is swept only in the buoyancy term | one run then takes **both halves of the paper's self-contradiction at once**, which is not what (g) registered — (g) asked for the two `α` read side by side, not mixed inside one run | commit **4** — repaired, and ⚠ *it moved nothing: `α` is absorbed by `b`* |
| ③ | `z*_D` is set from the **melting-onset depth**, not iterated as **eq. 56**'s `z*_D = Nu⁻¹` | the paper's outer solve is a fixed point; ours is a single geometric guess | commit **5** — repaired, and ⚠ *it removed most of the 1500 °C asymmetry: (c) 2.2396 → 1.5838* |
| ④ | `T_s` is **mixed inside one run**: `T_i = T_p + 273.15` but `ΔT = T_i − 273.0`, so `ΔT` = 1350.15 K at `T_p` = 1350 °C — while the `b` fit line uses the literals **1350.0 / 1623.0** | the fit condition and the run condition differ by **0.15 K** | commit **2**, and it goes first |

⚠ **④ was repaired first, and the reasoning that put it there survives its neighbour's withdrawal.** A
fit's fixed point is exact only at the condition it was fitted on, so a `T_s` mixed between the fit line
and the runs would have contaminated any statement about the normalization. It was unified first (one
273.15 K), and the normalization then turned out to need **no repair at all**. **Each commit reports how
far its own change moved the twelve runs, and no commit reports two changes at once.**

**⚠ What is promoted is the second block (16:39:56), and the difference from the first is `θ`'s
definition — this matters enough to state where a reader will trip over it.** The first block (16:39:22)
used `θ = E ΔT / (R T_i)` and died with `OverflowError` inside `_ra_local_max`'s
`d_eta ** frac * exp(θu/2)`; the second uses **`θ = E ΔT / (R T_i²)`**, the Frank-Kamenetskii form, and
runs. **Run the `T_i` form and `b` comes out at `6.0416 × 10⁻³` — a factor `6.94 × 10¹²`, 12.8 orders
of magnitude, from `4.1921 × 10¹⁰` — and none of the twelve rows reproduces.** Both figures were
re-derived at this tree before this section was written, and both match what the recovered blocks
printed. ⚠ **The overflow has a one-line cause:** at `ΔT` = 1350 K and `T_i` = 1623 K the `T_i` form
gives `θ` = **30 014** against the Frank-Kamenetskii **18.49**, and `_ra_local_max` evaluates
`exp(θu/2)` — `exp(15 007)` is not a float. ⚠ **The promoted code is the `T_i²` form**, and
`engine/stagnant_lid.py@«실행된 것은 이 정의다»` says so where a reader will look.

⚠ **`b` is re-fitted rather than pinned to the printed digits.** The 09-07 run printed `4.1921e+10` to
four significant figures and used the bisection's full precision; declaring the printed value as the
constant would not reproduce the run. So `fit_b_eq30()` solves the same bisection and
`B_GRAIN_RECORDED` carries the printed value **for comparison only**.

### C48 — the integrator was validated on Earth, and Earth survived by not blowing up rather than by being right — **closed 2026-09-08: domain (Brief 155) + step (Briefs 156–157)**

**This one number is the whole item:**

> ⚠ **`2.3 × 10¹⁰ Pa·s`** — the mantle viscosity `core_history` asks Nimmo's law for, at the
> temperature it starts Mars from. **That is not a mantle.** Solid rock near its solidus is
> `10¹⁸–10²¹`; this is eight orders below the bottom of that, in the neighbourhood of a warm lava
> rather than of a convecting mantle. Earth's own start asks for `4.3 × 10¹⁴` — still four orders
> under solid rock.

**C20 ran on a second body for the first time today and diverged.** Mars's mantle integrates to
`T_m = −6244 K` at the declared potential temperature of 1600 K, and to −6977 … −8208 K across the
whole pre-registered 1400–1800 K sweep. Every point. ⚠ **The divergence is not the interesting part** —
a body that survives the same call is not thereby getting a right answer.

**What the flux law returns at the temperatures the integrator actually feeds it:**

| body | `T_m` | `F_t` | `Q_M` | measured, for scale |
|---|---|---|---|---|
| Mars | **4021 K** (its initial condition) | **719,546 mW/m²** | **103,882 TW** | Parro+ 2017: **19 mW/m²** |
| Mars | 1600 K | 55.6 | 8.03 TW | Reese ceiling 15–30 mW/m² |
| **Earth** | **3040 K** (its initial condition) | **25,144 mW/m²** | **12,825 TW** | Davies & Davies 2010: **92.1 mW/m², 47 TW** |
| Earth | 1600 K | 76.9 | 39.2 TW | — |

**Earth is called at 273× its own measured flux and Mars at ~38,000× Parro's.** ⚠ **Earth's numbers
come out of the same out-of-range call; Earth simply has the mantle heat capacity to survive it.**
That is the finding, and it is about C20 rather than about Mars.

**Why, precisely — and the answer is not the one this seat first reached for.** `mantle_flux.py`
declares `BRACKET_K = (1000, 2500)` and its `consistency` path refuses outside it by name. `core_history`
calls `implied_flux` directly with no such check. But ⚠ **that bracket is ours, not Nimmo's**: its own
comment calls it *"the bisection bracket"*, and `invert_for_flow`'s docstring dates it to Brief 57,
where a bisection on the **inverse** problem was returning an endpoint as a value. **Nimmo+ 2004 prints
no validity range for eq. 35 at all.**

**The real constraint is in the equation's form.** Eq. 35 is a linear-exponential expansion about a
reference temperature, and Nimmo's Table 2 fixes it: *"We adopt this value for `T₁` and **1573 K for
`T₀`**"*, with `η₀ = 10²¹ Pa·s` there. Evaluated away from that point:

| `T_m` | distance from `T₀` | viscosity | as a fraction of `η₀` |
|---|---|---|---|
| 1600 K — Nimmo's own present-day Earth | +27 K | 7.6 × 10²⁰ Pa·s | ÷ 1 |
| 2500 K — our bracket ceiling | +927 K | 9.4 × 10¹⁶ | ÷ 10,615 |
| **3040 K — C20's Earth initial** | **+1467 K** | 4.3 × 10¹⁴ | **÷ 2,350,174** |
| **4021 K — C20's Mars initial** | **+2448 K** | 2.3 × 10¹⁰ | **÷ 42,808,392,211** |

So no published range was violated — **none is printed** — and **a linearisation was evaluated 1467
and 2448 K from its expansion point.**

⚠ **The obvious repair does not exist, and it is the first thing the next reader will reach for.**
`BRACKET_K` looks like the guard that failed, so widening it — or adding it to `core_history`'s call —
looks like the fix. **It is not.** That constant is ours and it is about a different problem (a
bisection on the inverse map, Brief 57). Enforcing it would turn a wrong number into a refusal, which
is better, but it would not give the integrator a flux at 3000 K. **There is no value of `BRACKET_K`
that makes eq. 35 usable 1500 K from its expansion point.**

**⚠ And the sharpest way to say it: two numbers from the same paper do not compose on a second body.**
The 4800 K initial condition is what Nimmo prints **for Earth**, and the flux law's blow-up point moves
with gravity and radius, so it sits **somewhere different on every body**. A starting temperature that
Earth barely survives is outside the usable region on Mars. **Not our arithmetic error — a
composition failure between two of one paper's own values**, found only by running a second body.

⚠ **That generalises past C20, and it is the reason to record it somewhere wider.** This engine
declares Earth's numbers on every rocky body by design — `MANTLE_SHARE = 0.70`, `T_s = 293 K`,
Korenaga's `b`, and now Nimmo's 4800 K. **The pattern is sound and this is its failure mode: a transfer
that is safe on the body it came from can be outside the usable region on another, and only running the
second body shows it.** Transfers need a per-body check, not just a label.

**Blast radius, counted rather than estimated.** `core_thermal_history` has **one** consuming edge —
`core_entropy_production` (`chain.yaml`, `kind: influences`) — plus `core_entropy.py` and its test.
**No board row and no `db/` entry stands on any C20 output.** Nine markdown records mention
`entropy_history_verdict`. ⚠ **And one C20 output was used in argument today**: C47 (h) cited Earth's
`mantle_potential_temperature_present = 1525 K` as evidence that route (ii) already produces a value.
**It does — from an out-of-range call.**

**⚠ Not repaired tonight, and the two directions are named rather than taken.**

1. **A flux law the integrator can use at early high temperatures.** Not this one, outside ~1573 ± a
   few hundred K.
2. **Starting the integration inside the usable region, on grounds.** ⚠ **This is not "lower the
   initial temperature until it runs."** Choosing a starting value because it integrates is the defect
   this whole item exists to name. A grounded starting *epoch* is a different thing from a working
   starting *value*.

**⚠ And C47's verdict does not move.** Inside the usable region — Mars at 1600 K — the flux is
**55.6 mW/m²**, about **2× Reese's own ceiling** for Mars. The original defect stands exactly where
C47 (b) put it. **The divergence is a separate cause, and repairing it would not make the direction
test pass.**
