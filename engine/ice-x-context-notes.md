# Ice X — context notes

Decisions taken while carrying the water ladder above 37.4 GPa, and the reasoning behind
them. Appended as the work goes.

## The structure question, answered before any code

The brief asked whether a temperature-dependent boundary goes beside `p_min`/`p_max`, or
reuses the `melt` slot, or takes some third shape. The answer is **beside `p_min`/`p_max`,
as `t_max`, and it is a different kind of object from `melt`** — and the reason is worth
keeping, because the two look alike from a distance.

`melt` is a **physical transition** that this recipe can locate: `T_melt(P)` is a curve,
it varies with pressure, and its consumer uses it to *label* a state without touching the
density. The superionic boundary is the same kind of thing, and if this work had a curve
for it, it would go in the same slot.

It does not. What the research produced is a **domain ceiling**: the equation of state
below is a Gibbs representation whose knot domain stops at 1800 K, and that is a property
of the fit, not of the material — the same kind of statement as `p_max`. So it is stored
the same way `p_max` is, a flat number on the phase, and crossing it is a refusal that
names what is above rather than a verdict.

The two happen to line up, which is why the ceiling is usable rather than arbitrary:
Millot+ 2019's abstract puts superionic water at "pressures exceeding 100 gigapascals and
high temperatures above 2,000 kelvin", so a ceiling at 1800 K sits **below** the phase this
recipe cannot model. The recipe never silently returns ice X where the material is
superionic; it stops first and says so.

## What the research found, in the order it changed the plan

### 1. Ice VII's thermal constants exist, and they were one directory away

The 2026-08-27 note said the literature was silent. It is not. SeaFreeze v1.1.0 ships a
sixth representation, `VII_X_French`, which the package's own README attributes to **French
& Redmer 2015** ([`2015PhRvB..91a4308F`](https://ui.adsabs.harvard.edu/abs/2015PhRvB..91a4308F),
"Construction of a thermodynamic potential for the water ices VII and X"). Reading its knot
domain out of the shipped spline gives **1.7 GPa to 1000 GPa, 20 K to 1800 K**.

That is the same source and the same construction ices III, V and VI already use in
`eos.py`: evaluate a released Gibbs representation at a stated reference state and read ρ,
K_T, K′, αK_T and c_V off it. The earlier session looked for a *paper* carrying ice VII's
thermal constants as printed numbers and found none, which was true and is still true;
what it missed is that the representation it was already depending on covers ice VII too.

So ice VII stops being isothermal, and the phase above it can be built the same way.

### 2. One phase covers 37.4 GPa to 1 TPa, not several

French & Redmer treat ices VII and X as **one** thermodynamic potential — the VII→X
transition is a continuous symmetrisation of the hydrogen bond, not a first-order jump, so
there is no density discontinuity to put a rung at. Goncharov+ 2005's 47 GPa, which the old
refusal names, is where that symmetrisation completes, not where a new equation of state
starts.

So the ladder gains **one** rung, `ice_x`, running from the existing 37.4 GPa transition to
the representation's 1 TPa ceiling. The silicate work reached the same shape for the same
kind of reason: one phase, spliced where the source stops.

### 3. The fit had to be a fit, and that is a change of kind worth recording

Ices III, V and VI were **read**, not fitted: ρ, K_T and K′ evaluated at P = 0 on the
reference isotherm are exactly what a third-order Birch-Murnaghan takes, and rebuilding the
curve from them reproduced the representation to 0.006 %, 0.014 % and 0.118 %.

That route is closed here. The representation's knot domain starts at 1.7 GPa, so P = 0 is
not evaluable, and reading (ρ, K_T, K′) at 37.4 GPa and solving the three-parameter
Birch-Murnaghan backwards gives a curve **15.5 % out** by 1 TPa — a local reading cannot
span a 27× pressure range.

So `ice_x` is a least-squares fit to the representation's 300 K isotherm over exactly the
range it is used on. Three functional forms were tried on the same data:

| form | ρ₀ (kg/m³) | K₀ (GPa) | K₀′ | worst density deviation |
|---|---|---|---|---|
| Vinet | 1644.29 | 22.29 | 6.75 | **1.475 %** |
| BME3 | 1855.97 | 58.37 | 4.67 | 1.621 % |
| BME4 | — | — | — | diverges |

Vinet wins, and it is also the form the file's own rule points at: Seager+ 2007 §III.1 says
Vinet extrapolates better than Birch-Murnaghan at high pressure, which is why Fe(ε) uses it.
The residual is worst at the two ends (+1.48 % at 37.4 GPa, −1.02 % at 1 TPa) and around
0.5 % through the middle. Splitting into two Vinet pieces was tried and rejected: it gets
the deviation down to 0.26 % but the lower piece's parameters come out at ρ₀ = 382 kg/m³
and K₀ = 0.4 MPa, which are not constants of anything — they are a curve-fitting artifact
of a narrow range far from zero pressure, and this file does not carry constants that mean
nothing.

**1.475 % is this phase's honest width, and it is larger than any other rung's.** It is
stated in the code, measured by the test, and it is the reason the grade drops.

### 4. The seam is 2.3 %, and it is a disagreement between two sources rather than an error

At 37.4 GPa the existing ice VII curve (Seager+ 2007 Table 1's Birch-Murnaghan of Hemley+
1987's data) gives 2467.7 kg/m³ and the new Vinet gives 2524.0, a **−2.26 %** step. Two
thirds of it is the new fit's own +1.48 % overshoot at the low end of its range; the rest is
that Hemley's 1987 experimental fit, extrapolated to 37.4 GPa, sits 0.82 % below French &
Redmer's 2015 potential there.

It is not closed by adjusting either curve. Pulling the Vinet down to meet ice VII would be
fitting to our own output, which discipline 3 bans, and moving the transition pressure is
not available because everything below 37.4 GPa has to stay bit-identical. Note that
37.4 GPa is not our number either: Zeng & Sasselov 2013 §III.3.2 set it as "the intersection
between FFH2004's EOS and FMNR2009's EOS", which is the same construction applied to the
previous generation of the same two sources.

The silicate ladder's seam at 3.5 TPa is 0.21 % and the doc says so; this one is ten times
that, so it is measured by the test and named in the note rather than left for a reader to
discover.

### 5. The Anderson–Goto thermal form does not fit this material well, and the numbers say so

Every thermal constant in this file rests on αK_T being independent of volume above the
Debye temperature, which is Anderson & Goto 1989's result and Seager+ 2007 §IV.2.2's reason
for using a thermal pressure linear in ΔT. Evaluating the representation across its domain
shows αK_T for ice VII/X roughly **doubling** from 300 K to 1800 K at every pressure
(4.34 → 9.39 MPa/K at 37.4 GPa; 2.25 → 10.04 at 1 TPa), so the linear form is a coarser
approximation here than it is for silicate or iron.

Measured against the representation, the thermal term is good where it matters and poor at
one corner: **within 0.7 % at 100 GPa and above** across 300–1800 K, degrading to 2.0 % at
37.4 GPa / 600 K and 7.7 % at 37.4 GPa / 1800 K. That corner is not physical ice anyway —
ice VII melts near 870 K at 37.4 GPa on Frank+ 2004's Simon equation — but the recipe cannot
prove that for itself, so the number is recorded rather than argued away.

A second, sharper finding: the representation is a **rectangular** knot domain over a phase
field that is not rectangular. Evaluated at 2.216 GPa and 1500 K it returns c_V = 1.5 × 10⁸
J/kg/K, and at 10 GPa and 1800 K it returns c_V = −7.3 × 10⁵ — both far above the melting
curve, where ice VII does not exist and the spline is extrapolating into nonsense. The
1800 K ceiling does not protect against that at low pressure. It is recorded here; what
protects the recipe in practice is that the melting verdict already goes `undecided` there.

### 6. The melting curve runs out first, and that stays a verdict rather than a density

IAPWS R14-08(2011)'s ice VII equation is valid 355–715 K, which in pressure is 2.216 GPa to
**20.6 GPa** — it ends inside ice VII, well below where ice X starts. Above it there is no
melting curve this recipe carries.

Two candidates were found and both were rejected for now:

- **Frank, Fei & Hu 2004** ([`2004GeCoA..68.2781F`](https://ui.adsabs.harvard.edu/abs/2004GeCoA..68.2781F))
  print a Simon equation in their abstract, `(P − 2.17)/0.764 = (T/355)^4.32 − 1`, valid
  3–60 GPa. Splicing it above IAPWS would put a **17 % pressure step** at the seam (17.1 GPa
  against IAPWS's 20.6 GPa at 715 K), and it would buy melting verdicts over one third of
  one rung. Not worth a second water melting compilation.
- **Millot+ 2018** ([`2018NatPh..14..297M`](https://ui.adsabs.harvard.edu/abs/2018NatPh..14..297M))
  measure that ice "melts near 5,000 K at 190 GPa", which is a point, not a curve.

So the answer to the collision is: **the melting curve loses, and says so.** Above 20.6 GPa
`ice_column_state` is `undecided`, exactly as it already was above 2.216 GPa for a different
reason. One thing did have to change: the verdict used to take the best margin over the
samples it could evaluate and ignore the rest, which could return `solid` for a column whose
deep half it never looked at. A column with any sample outside the curve can now only come
back `molten` or `undecided`, never `solid` — the same one-sided-bound rule `core_state`
uses.

## Density: changed on purpose, and where

Unlike the melting-curve work, this one **is** about density, and three things move.

- **Above 37.4 GPa** a body that used to be declined now integrates on ice X. That is the
  whole point.
- **Between 2.216 and 37.4 GPa, only when a temperature is declared.** Ice VII was isothermal
  and now carries thermal pressure. With no declared potential temperature the path is
  unchanged bit for bit, which is what every anchor runs on.
- **Nowhere below 2.216 GPa.** Ices Ih, III, V and VI are untouched.

## What was deliberately not done

**No superionic phase.** French & Redmer 2016
([`2016PhRvE..93b2140F`](https://ui.adsabs.harvard.edu/abs/2016PhRvE..93b2140F)) construct
thermodynamic potentials for both superionic phases and derive their boundary against ices
VII and X, but neither the boundary nor the potentials are in the abstract and the paper has
no preprint, so there is nothing to transcribe. The recipe stops at 1800 K and names that
paper as the one that would open it.

**No TFD.** Above 1 TPa the refusal stands. Zeng & Sasselov 2013 carry French+ 2009's
tabulated equation of state to 8.893 TPa before switching to Thomas-Fermi-Dirac, so there is
about a factor of nine of published headroom between where this recipe stops and where
degeneracy actually takes over; what is missing is a form to read, not physics. The refusal
says which of the two it is.

**No ice-giant envelope.** Everything here is pure H₂O. What it leaves for that branch is
the pressure range: the `ice_giant` refusal asks for a water-ammonia-methane mixture, and the
water half of that now exists to 1 TPa.

## How it came out

**The composition that was closed is open.** The `water` preset solved to 0.0398 M⊕ and now
solves to **5.884 M⊕**, a factor of 148. Measured across the ice axis, with the ice column's
own ceiling doing the limiting in every case:

| composition | mass ceiling |
|---|---|
| `water` preset (ice 0.50, core 0.163) | 5.884 M⊕ |
| ice mass fraction 0.25 | 12.318 M⊕ |
| ice mass fraction 0.75 | 17.646 M⊕ |
| pure ice | 17.247 M⊕ |

**Nothing below 37.4 GPa moved.** C/MR², radius and central pressure for Earth, Mars,
Mercury, the Moon and Ganymede, and C/MR² and radius for the five published icy moons, are
identical to the last digit against the revision before this one. The icy-moon residuals are
unchanged as well (Ganymede 2.1 %, Callisto 11.0 %, Titan 7.1 %, Europa 9.5 %, Enceladus
8.9 %); none of those columns reaches ice VII, let alone ice X.

**The fence moved rather than came down.** Above 1 TPa the recipe still declines, and the
refusal now says which of the two things ended: the representation's knot domain, not the
physics. Above 1800 K it declines by temperature and names the superionic phase and the
paper that would open it. A 40 M⊕ water world is still refused — by the iron core's ceiling
now, not the ice's, which is itself a sign the ice rung is no longer the binding constraint.

**The grade drops where it should.** A `water` body at 0.5 M⊕ keeps its ice column inside
ice VII and stays `calibrated`; at 1.0 M⊕ the column reaches 44 GPa, crosses into ice X and
drops to `analog`, with the note naming the 1.475 % fit width and the −2.26 % seam. That is
the `mgsio3_pv` pattern applied to the ice ladder.

**Documentation.** `interior-structure-methodology.md` went 1451 → 1484 lines (+33). No new
section was opened: the new phase went into the existing constants table and its paragraph,
the domain rows replaced the one refusal row that is now three, and the three sources went
into Citations. The offset that would more than pay for it is still sitting there unspent —
the page's "What changed, and why each change had to" section is a revision history, which
the methodology skill's do-not-write list bans outright, and removing it is a bigger edit
than this task and belongs with the split decision that is already with the owner.
