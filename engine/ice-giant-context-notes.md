# Ice-giant envelope — context notes

Decisions taken while trying to open `ice_giant`, and the reasoning behind them. Appended
as the work goes.

## The temperature-domain question, answered before any code: **(3), not at all**

The brief offered three readings and the answer is the third one: an ice-giant interior does
not overlap the water ladder's temperature domain **anywhere**.

The ladder runs 20–1800 K, a ceiling set on 2026-08-27 by the knot domain of French &
Redmer's ices VII/X potential and kept there because Millot+ 2019 put superionic water above
2000 K. An ice giant's ice mantle starts *above* that ceiling and goes up:

| where | condition | source |
|---|---|---|
| outer/inner envelope boundary | ~30 GPa | Scheibe+ 2019 §3 |
| deep interior | ~100 GPa, 5000–7000 K | Scheibe+ 2019 §3.2 |
| centre | 5700 K (Uranus), 5500 K (Neptune) | Scheibe+ 2019 §3.2 |
| icy Uranus model core | ~3800 ± 500 K | Bethkenhagen+ 2017 §V |

So the coldest number anyone publishes for the deep interior of these planets is about
**twice** our ceiling, and the ice mantle is fluid or superionic throughout. Bethkenhagen+
2017 §I says it plainly: "water is predicted to become superionic along the adiabat of
Uranus and Neptune ... whereas ammonia remains fluid".

That settles the size of the job. This is **not** "add two components to the water ladder".
Every rung of that ladder is a condensed solid phase, and none of them exists at these
conditions. Opening `ice_giant` means bringing in the fluid/superionic branch — the phase
this recipe deliberately declined three days ago — for three substances at once.

## What the research found

### 1. The mixing rule now has a measured limit for planetary ices

This is the one gap that closed. `eos.py` records that the additive volume law's only
quantified bound is Vorberger+ 2007's 8 % for H-He, and that nothing comparable exists for
other mixtures, so nothing was claimed. For ices it does exist:

**Bethkenhagen+ 2017** ([arXiv:1709.04133](https://arxiv.org/abs/1709.04133)) tested the
linear mixing approximation against real mixtures with DFT-MD, on data "ranging up to
1000 GPa and 20 000 K", for all three 1:1 binaries and for the 2:1:4 ternary along three
Uranus profiles:

- binaries: "deviations ... are generally small; for the thermal EOS they amount to 4 % or
  less", and they call 4 % an **upper limit** rather than a typical value
- ternary along Uranus profiles: "maximum deviations in density amount to up to 2.1 %",
  falling below 0.5 % above 10 000 K
- the deviation has a **sign**: "the LMA overestimates the density, while the internal energy
  is underestimated"
- where it degrades is named: when one component becomes superionic and another does not, or
  where carbon chemistry sets in

So planetary ices are *better behaved* under additive volume than H-He is (4 % against 8 %),
which is worth recording whether or not the envelope is ever built.

### 2. The composition ratio is a declaration, and it has a published default

Bethkenhagen+ 2017 §V take a solar H:C:N:O abundance and get
`Z_CH4 : Z_NH3 : Z_H2O = 0.31 : 0.08 : 0.61` by mass; the 2:1:4 molecular mixture they
simulate is chosen for "resemblance to the solar abundances of about 4:1:7 of C:N:O
(Asplund+ 2009)". Nothing observational pins it for a given planet — it comes from the
star's abundances and the formation history, neither of which this recipe carries. So it
would enter the same way `envelope_z` does: declared, and the grade drops when the answer
leans on it.

### 3. Only one of the three components has a transcribable equation of state

- **Water.** Mazevet, Licari, Chabrier & Potekhin 2019
  ([arXiv:1810.05658](https://arxiv.org/abs/1810.05658)) is exactly the object needed: an
  analytic Helmholtz free-energy fit covering liquid, plasma and superionic water, "valid for
  the entire density range relevant to planetary modeling ... for temperatures below
  50,000 K". Scheibe+ 2019 build their Uranus and Neptune models on it.
- **Ammonia** (Bethkenhagen+ 2013) and **methane** (Bethkenhagen+ 2017's own new EOS) exist
  as tabulated DFT-MD data. Neither paper prints a closed form, and neither has an
  open-access table this session could read. There is nothing to transcribe.

So even the maximal version of this work could only build the envelope out of **water alone**
— which is, to be fair, what the field does: Bethkenhagen+ 2017 §V notes that "planet models
where HCNO-bearing molecules are represented by a water EOS" is the standard three-layer
practice (Redmer+ 2011; Helled+ 2011; Nettelmann+ 2013), and their whole paper exists to
quantify what that costs.

### 4. What stopped the water import, concretely

Mazevet+ 2019's fit is not a three-constant curve. The published paper drops the explicit
form of its moderate-density term, so the authoritative source is their reference
implementation, `eoswater21.f`, fetched from the URL the paper gives
(http://www.ioffe.ru/astro/H2O/) — 465 lines of Fortran 77 carrying a correction dated
2021-08-18 that post-dates the paper.

Reading it, the pressure path decomposes cleanly: an ideal-molecule term, a van der Waals
molecular term with four constants, an effective-charge function with eight, a Fermi-function
blend with three, and the free energy of an ideal electron Fermi gas. The first four are a
day's careful work. **The fifth is the blocker.** It needs the Fermi integrals `I(1/2)` and
`I(3/2)` and the inverse `X(1/2)`, which the reference implements as Antia 1993's Padé
approximations: four coefficient tables of 8, 8, 12 and 12 entries for the forward integrals
and four more for the inverse, roughly **270 high-precision constants**, none of which is
about water at all.

There is no Fortran compiler on this machine (`gfortran` is absent), so the reference cannot
be run as an oracle. Hand-transcribing 270 coefficients of a numerical-library table with no
way to execute the original, into a repository whose stated discipline is that hand-keyed
tables drift and that has been 54× wrong once already, is the wrong trade — and it would be
invisible if wrong, because a bad Padé coefficient produces a plausible number rather than an
error.

The alternative is to evaluate the Fermi integrals from their definition by quadrature, which
needs no table at all. That is honest and it is slower: the integrator asks for a density
roughly a million times per body, and `scripts/check.sh` has to run on the system interpreter
with no scientific stack. It would have to be a tabulate-at-import-and-interpolate scheme with
its own stated error. That is a real piece of work, not a blocker — but it is a piece of work
about numerical methods, not about planets, and it should be chosen deliberately rather than
smuggled in at the end of an EOS task.

### 5. And the equation of state would not be sufficient anyway

The brief's decision line is that one recipe must reproduce Uranus **and** Neptune, or name
whose fault the miss is. The literature answers that in advance, and the answer is not the
equation of state.

Scheibe+ 2019 built adiabatic Uranus and Neptune models on the Mazevet water EOS, tuned to
each planet's measured radius, and got cooling times of 5.1 Gyr for Uranus and 3.7 Gyr for
Neptune against an actual age of 4.56 Gyr — "too short for Neptune and too long for Uranus".
Their conclusion is the title of the problem: "neither planet is fully adiabatic in the deeper
interior". Nettelmann+ 2016 could only fix Uranus by putting a thermal boundary layer into it.

That is the same mechanism `core_state` ran into: a boundary layer whose size is set by a heat
flux, in a recipe with no heat flux and no thermal history. So a perfect ices EOS would let
this solver integrate an ice giant, and the two planets would still not both come out — the
difference between them is thermal history, and naming that is the honest result rather than a
consolation.

## What landed, and what did not

**Landed.** The mixing rule's measured limit for planetary ices (4 % / 2.1 %, with its sign
and its failure mode), the composition ratio with its source, and an `ice_giant` refusal that
names the actual distance to be covered instead of gesturing at "a Redmer+ 2011-family
water-ammonia EOS" — which was also slightly wrong, since what is needed is the fluid branch
rather than a high-pressure solid one.

**Not landed: the envelope equation of state, so the node is still refused.** The reason is
§4 above, and it is a cost-and-risk judgement rather than a missing citation. The decision
belongs to the owner because it is a choice about how much numerical-methods work to take on:

- **Port Mazevet+ 2019 with the Padé tables.** Fastest at run time, ~270 hand-typed constants,
  no oracle on this machine. Not recommended in that form.
- **Port it with quadrature plus an import-time table.** No transcription risk on the special
  functions, needs its own accuracy statement and a speed check against `check.sh`'s budget.
  This is the recommended route if the node is to open.
- **Ask for a compiler.** With `gfortran` available the reference becomes an oracle and the
  first option stops being reckless. This is the cheapest way to de-risk the other two.

Whichever is chosen, the envelope would be water-only at first, with ammonia and methane
recorded as absent and their cost bounded by §1.
