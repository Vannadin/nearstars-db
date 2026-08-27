# Melting curves — context notes

Decisions taken while giving the solver a melting curve, and the reasoning behind them.
Appended as the work goes.

## Where the curve lives: **on `Phase`, in `eos.py`**

The brief left this open. The answer is the material, for three reasons that are really
one reason.

`eos.py` already answers "is this phase valid at this pressure" with `p_min` / `p_max`,
and `phase_at(P)` picks the branch. A melting curve is the same kind of object — a
temperature threshold that is a function of pressure — and it needs the same kind of branch
selection, because **`T_melt(P)` is not single-valued for water**: ice Ih's melting curve
runs backwards (273.16 K at 611 Pa down to 251.165 K at 208.566 MPa) while ice III, V and VI
run forwards.

One correction to the first draft of that reasoning, made while implementing it. The curve
does **not** branch on the phase's own `p_min` / `p_max`: it branches on its own break
pressures, because IAPWS's triple points differ from ours by up to 2.3 % (see below) and
selecting by the phase interval would ask ice VI's equation about a pressure below where
that equation starts. So `Phase` declares *which* curve it belongs to (`"water"`, `"iron"`,
or `""` for none) and the curve carries its own breakpoints. That is still a material
property; it is just one curve per material rather than one per phase.

The second reason is that there are two consumers, and two copies drift. `interior_layers`
asks about the ice column; `core_state` asks about the iron core. Both read one object.

The third is that a curve without its equation of state is not checkable. The published
verification values (IAPWS Table 3, and the ICB anchors for iron) are stated as pressures
and temperatures, and the test that reproduces them sits next to the test that reproduces
`ρ(P)` for the same phase.

## What the research found, in the order it changed the plan

### 1. The iron melting curve exists over the whole range this engine reaches, in two pieces

**Zhang, Sun, Wang & Zhang 2015** ([`2015PEPI..244...69Z`](https://ui.adsabs.harvard.edu/abs/2015PEPI..244...69Z))
fit their two-phase molecular-dynamics melting data to a Simon equation and print it in
their own abstract:

    T_m = 1825 K · (1 + P/57.723 GPa)^0.654          fitted to 365 GPa

It gives 1825 K at zero pressure against the measured 1811 K for iron (0.8 %), and 6345 K
at the inner-core boundary, which the same abstract calls "very close to the recent diamond
anvil cell extrapolated value".

**González-Cataldo & Militzer 2023** ([`2023PhRvR...5c3194G`](https://ui.adsabs.harvard.edu/abs/2023PhRvR...5c3194G))
carry it to super-Earth cores, and likewise print the fit in the abstract:

    T_m = 6469 K · (1 + (P − 300 GPa)/434.82 GPa)^0.54369     300 – 5000 GPa

with the sentence that matters for `core_state`: "The slope of our melting line is
consistently steeper than that of our adiabats, which implies that the crystallization of
iron in the cores of terrestrial planets always starts from their centers, like on Earth."

The two overlap on 300–365 GPa and disagree by **6.8 to 7.5 %** there, the higher curve
being González-Cataldo's. That spread is smaller than the spread between the two static
compression experiments at the same pressure (Anzellini+ 2013's 6230 ± 500 K against
Sinmyo+ 2019's 5500 ± 220 K, 13 % apart), so it is not a defect of either fit. It is
recorded rather than averaged away, and the splice sits at 365 GPa where Zhang's fit ends.

### 2. The water melting curve is a standard, and it comes with its own check values

**IAPWS R14-08(2011)**, the *Revised Release on the Pressure along the Melting and
Sublimation Curves of Ordinary Water Substance*, gives closed-form `p_melt(T)` for ice Ih,
III, V, VI and VII with stated validity ranges and stated uncertainties (2 %, 3 %, 3 %,
3 %, 7 %), and its §7 lists one calculated pressure per equation for program verification.
This is the same kind of source, from the same body, as the IAPWS-06 release `eos.py`
already reads ice Ih's ρ₀ and K_T from, and it is a non-ADS citation of the curated-standard
kind the methodology skill allows, pinned by release number.

The window the brief asked about — 209.5 MPa to 2.216 GPa — is covered by equations (2),
(3) and (4), end to end, with no gap.

**Its triple points are not bit-identical to ours, and that is worth writing down.** `eos.py`
takes its phase transitions from Choukroun & Grasset 2007 via Zeng & Sasselov 2013; IAPWS
constrains its melting equations to its own triple-point table. They differ by 0.45 %
(Ih–III), 1.4 % (III–V) and 2.3 % (V–VI) in pressure. The transitions stay where the
equation of state put them and the melting curve keeps its own reducing constants, because
moving either to match the other would break the fit it belongs to. The result is that
within about 2 % of a triple point the two disagree about which phase melts; that is
smaller than IAPWS's own 3 % uncertainty on the curve, and it is named in the note.

### 3. The core temperature `interior_layers` produces is a **lower bound**, not the core temperature

This is the finding that reshaped the work. The brief expected the melting curve to be the
last missing piece for `core_state`. It is not, and running the numbers says so immediately:
Earth at the reference potential temperature comes out with a central temperature of
**2671 K at 358 GPa**, where iron melts near 6600 K. Taken at face value the recipe would
report Earth's core as entirely solid, contradicting the measurement that this whole task
is judged against.

Two named mechanisms, both real, both outside this recipe:

**The core sits on the mantle's adiabat.** `interior.py` integrates one continuous adiabat
from the surface to the centre. Unterborn+ 2019's eq. 7, the published check the temperature
work anchored on, is a **mantle** adiabat and its 2635 K at 1 R⊕ is the mantle-side CMB
temperature — the paper says so, comparing it to Lay+ 2008's 2500–2800 K "as determined
using a similar method to ours". Between that and the core sits the D″ thermal boundary
layer, whose ΔT is set by the CMB heat flux. Sinmyo+ 2019 put Earth's core-side CMB
temperature at **3760 ± 290 K**; the jump is over 1200 K. Zhang & Rogers 2022
([arXiv:2208.06523](https://arxiv.org/abs/2208.06523)) report it as ~240 K for a 1 M⊕
planet and ~1880 K for 3 M⊕ *in their models*, which is the point: it is model-dependent and
flux-driven, and this recipe has no flux.

**The iron branch of the adiabat is too flat.** `Phase.gruneisen` closes γ as an identity
from αK_T and c_V, which is validated for the ices against SeaFreeze's own γ to four decimal
places. For iron it inherits Seager+ 2007 §IV.2.2's αK₀ = 0.00121 GPa/K (from Isaak &
Anderson 2003) — a **thermal-pressure** constant, chosen there to get densities right, not a
Grüneisen source. It yields γ_Fe ≈ 0.22 at core pressures, against the ab-initio value of
**ca. 1.5** that Alfè, Price & Gillan 2002
([arXiv:cond-mat/0107307](https://arxiv.org/abs/cond-mat/0107307)) find "varies little with
pressure or temperature for 100 < p < 300 GPa and 4000 < T < 6000 K", and 1.51–1.52 on the
liquid Hugoniot. The transcription in `eos.py` is faithful to its source; the source was
answering a different question.

Both biases point the same way — down. So the number is not garbage: it is a **lower bound**
on the core temperature, and a lower bound supports a one-sided verdict. That is what
`core_state` is built on.

## The design that follows

`core_state` is a separate calculation, as `chain.yaml` already said it would be, and it has
two branches.

**Without a declaration** it uses `interior_layers`' geotherm as the lower bound it is. If
the melting temperature at a depth is *below* that bound, the material there is liquid and no
boundary layer can change it, because the boundary layer only adds heat. If it is above, the
answer is `undecided` — never `solid`, because the bound is one-sided. This branch needs
nothing declared and can still return a verdict.

**With `core_cmb_temperature` declared** it integrates the core's own adiabat from the
core-side CMB temperature at constant γ = 1.5 (Alfè+ 2002), which is a closed form on the
density profile: `T(P) = T_cmb · (ρ(P)/ρ_cmb)^γ`. Then it can say `solid` as well as
`liquid`, and locate the inner-core boundary where the adiabat crosses the melting curve.
The declaration is the same kind of object as `potential_temperature`, `initial_porosity`,
`envelope_z` and `tidal_heating`: something accretion and thermal history set, which this
recipe does not carry. The grade drops to analog whenever the answer uses it.

**γ = 1.5 is checked, not assumed.** Sinmyo+ 2019 give two points on one Earth core adiabat,
3760 K at the CMB and 5120 K at the ICB. Integrating our core adiabat at γ = 1.5 from the
first reproduces the second to better than 1 %. That is a published pair reproduced, not our
output tested against our output.

## The light-element depression, and why the alloy is already in the material

`fe_prem` is a fit to PREM's outer core, so light elements are inside its effective ρ₀
already — that is the sentence `eos.py` has carried since the beginning. The melting curve
has to follow the same split:

- `fe_eps` — laboratory pure ε-iron. The published curve applies unchanged.
- `fe_prem` — an alloyed core. Its melting point is depressed.

The depression is a declared modelling constant, not a derivation, and the literature spread
is wide. The convention published thermal-evolution models use is **20 %** (Stevenson+ 1983,
carried by Tachinami+ 2011, Stixrude 2014, and Zhang & Rogers 2022, who state it plainly:
"the melting temperature of iron is reduced by 20 % to account for the influence of light
elements in the iron core"). An independent check lands in the same place: Sinmyo+ 2019's
Earth ICB temperature of 5120 ± 390 K against Zhang+ 2015's pure-iron 6331 K at 329 GPa is a
**19.1 %** depression. Those two are not the same statement — Sinmyo applied their own 380 K
depression to their own 5500 K curve, and 5120 K is their estimate of a physical temperature
— so the agreement is a consistency check, not a derivation. Both numbers are recorded and
the 20 % is what ships.

## What was deliberately not done

**No liquid equation of state.** A verdict is returned; density is not touched. Melting
lowers density by a few per cent and modelling that means a second equation of state per
material, a phase fraction inside the integrator, and a new anchor set — larger than this
task. The consequence is stated in every note that carries a molten verdict: the radius and
C/MR² returned alongside it are the **solid-phase** answer. Every anchor is therefore
bit-identical to before, which is checked rather than asserted.

**Ice VII stops where its thermal constants stop.** IAPWS gives a melting curve for ice VII
(355–715 K) and `eos.py` has no thermal constants for that phase, so the temperature does not
flow through it — `dT/dP` is zero there and whatever T entered the layer is carried, unchanged
and meaningless. The verdict declines above 2.216 GPa and names that, rather than comparing a
real curve against a fake temperature.

**No silicate melting curve.** A magma-ocean verdict for the mantle needs a silicate solidus,
which is a different literature (a solidus and a liquidus for a mixture, not one melting point
for a pure compound), and a molten mantle breaks the solid-body premise the rest of this
recipe rests on. `melt_free_phases()` names the silicate phases as having no curve, the way
`cold_phases()` names the phases that have no thermal constants.


## How it came out

**Earth's core is right, and only on the declared branch.** With the core-side CMB
temperature declared at Sinmyo+ 2019's 3760 K, `core_state` returns
`liquid_outer_solid_inner` and puts the inner-core boundary at 352 GPa against PREM's
328.85 GPa. The residual is +7 %, and the reason it is that large in pressure while the
temperatures agree is that the adiabat and the melting curve run nearly parallel near the
centre: a 1 % shift in melting temperature moves the boundary by tens of GPa, and the two
published experiments at that pressure disagree by 13 %. Without the declaration Earth comes
back `undecided`, which is the honest answer for a bound that only closes one side.

**The γ check landed better than expected.** Sinmyo+ 2019 give two points on one Earth core
adiabat; integrating from the first at γ = 1.5 gives 5121 K against their 5120 K. That is a
published pair reproduced, and it is the only reason to believe the adiabat branch at all.

**The anchors did not move — measured, not asserted.** C/MR², radius and central pressure
for Earth, Mars, Mercury, the Moon and Ganymede are identical to the last digit against the
revision before this one. Density was not touched, and nothing in the melting path is
reachable from the density path.

**What grew that was said not to grow.** `interior-structure-methodology.md` went from 1384
to 1439 lines (+4 %): a melting-curve section of ~40 lines, three domain rows replacing one,
two Contract entries and a citation. Every line of it is on the "belongs in the methodology
doc" side of the brief's placement table, and the iron half went to the new doc instead. It
is still growth and it is recorded here rather than glossed. Two sections on that page are on
the methodology skill's do-not-write list already — "What changed, and why each change had
to" (a revision history) and "What the roster asks for" (framed around our bodies) — and
removing either would more than pay for this addition, but that is a separate edit and the
split proposal for this page is still with the owner.

**One thing found and not fixed.** `engine/interior.py`'s `_from_state` was not passing
`potential_temperature` or `tidal_heating` through from the body file, so no body could ever
declare a temperature to the runner even though `solve()` accepted one. That is wired now,
because `core_state` cannot work without it. It also means `engine/bodies/earth.yaml` exists:
`check_contracts.py` could not verify `core_state`'s contract without a sample body that
reaches it, and Earth is the only body whose core-side CMB temperature is published.
`check_contracts.py` now runs the graph before reading the results, because calling one
recipe in isolation can never satisfy a node that eats another node's output.
