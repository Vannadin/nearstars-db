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

---

## 2026-08-27, later: the two blockers are gone

The owner chose the quadrature route and corrected one thing I had wrong. Both are recorded
here because they change what the earlier sections said.

### The Padé problem dissolved rather than being solved

I had framed 270 hand-typed coefficients as the blocker. The owner's correction: **Antia's
Padé is not the canonical object.** It is a 1993 approximation to a function whose definition
is a closed definite integral, written for Fortran. The definition is the canonical form, and
evaluating it needs no table.

`fermi.py` does that. Three branches, and two of them are not tables at all:

| branch | how | measured error |
|---|---|---|
| η ≤ −1 | the polylog series, converged | ~1e-16 |
| −1 < η < 20 | baked table, Hermite in ln F with exact slopes | **4.5e-7** |
| η ≥ 20 | Sommerfeld degenerate expansion | 1.1e-8 |

The middle is 85 grid points evaluated with `scipy.integrate.quad` in the dev venv and baked,
exactly as ices III, V and VI were. Two things had to be measured rather than assumed:

**The interpolation error is a new error dimension, and it took two tries.** The owner flagged
this: the ice III/V/VI precedent baked three constants, so "is the constant right" was the
whole question. Here the baked object is a function's table, so the gaps between grid points
are a separate error. Measuring it caught a real mistake — interpolating F directly gives
3.9e-6, and the worst point sat in the first cell. Interpolating **ln F** with the exact slope
identity d(ln F_j)/dη = j·F_{j−1}/F_j gives 4.5e-7, an eightfold improvement for free, since
the slopes come from the table itself rather than from a new constant.

**The seam had to move.** With the Sommerfeld branch starting at η = 15 its own error is
1.3e-7, and that jump dominated the inverse's round-trip: 8.6e-8, worst exactly at η = 15.
Moving the seam to η = 20 drops the branch error to 1.1e-8 and the round-trip to 4.2e-14.
Twenty extra grid points bought four orders of magnitude.

**Two oracles, not one**, as instructed: `quad` on the definition, and mpmath at 40 digits on
the polylog identity F_j(η) = −Γ(j+1)·Li_{j+1}(−e^η). They agree to 8.5e-16 over the sweep
the test runs. Different methods do not make the same mistake in the same direction.

**No inverse table.** F_{1/2} is monotone and its derivative is closed (½F_{−1/2}), so Newton
on the forward interpolant converges in two or three steps.

### The water EOS is ported, and the transcription is checked three ways

`water_hot.py` carries Mazevet+ 2019's pressure and internal energy, transcribed from the
authors' `eoswater21.f` rather than from the paper, because the paper omits the explicit form
of the moderate-density term and the reference carries a 2021 correction that postdates it.
About twenty constants.

No Fortran compiler, so no oracle by execution. Three independent checks instead, and the
first is the one that matters:

1. **The paper prints a check value of its own fit**: it puts the liquid-vapour critical point
   at 683 K and 0.331 g/cc (against measured 647 K and 0.322). This port gives **683.1 K and
   0.3305 g/cc**. That single number exercises the van der Waals term, the blending function
   and the ideal term together, and it compares against *their fit* rather than against
   physics, which is the right target when what is being tested is a transcription.
2. **The low-density limit** goes to the molecular ideal gas, approaching 1.000 as density
   drops. Physics fixes that, so a wrong constant would show.
3. **Two sources for the same constants.** The effective charge Z\* is printed in the paper as
   eq. (9) and implemented in the reference; coding both paths independently and comparing
   gives 0.0 difference on its six constants. The blending function is the same story: the
   paper's printed "3509 K" and the reference's 90·T_au agree to the printed rounding
   (3508.6 K), and the paper's 2.5 g/cc is exactly the reference's Q1 = 0.4 inverted.

Internal energy came along because the alternative was an isothermal envelope, and that is not
available: at fixed pressure, moving from 2000 K to 5700 K changes water's density by 14 % at
30 GPa and 5 % at 800 GPa. The Grüneisen parameter falls out by finite differences rather than
by transcribing the reference's analytic derivative chains, which would have been long code
with nothing to check it against; the truncation error is ~1e-4 against an equation of state
good to percents.

### The correction: water-only's cost is not Bethkenhagen's 4 %

I wrote in the previous commit that standing water in for all three ices costs the 4 % /
2.1 % from Bethkenhagen+ 2017. **That is wrong and it is now fixed in the code, both docs and
both mirrors.**

Those numbers bound a different step: mixing three *complete* pure equations of state by
additive volume. The water-only shortcut never takes that step. Its cost is the difference
between a water EOS and a mixture EOS, which the cited literature does not measure — and the
same paper's conclusion proposing that all three pure potentials be built is itself the
statement that water alone is not sufficient. So it is recorded the way the rock–metal case
already was: field practice, unquantified. When methane and ammonia arrive, comparing an
additive-volume mixture against water-only is the work that produces the number.

### Where this leaves the node

Still refused, but for one remaining reason rather than three. What is built and tested is the
whole physics stack an ice-giant envelope needs: Fermi integrals, the hot-water equation of
state, its energy and its Grüneisen parameter. What is left is wiring — a material in
`eos.py`, `ice_giant` out of `FLUID_CLASSES`, the layer stack picking hot water above 1800 K,
and Uranus and Neptune as anchors. That is mechanical work against a tested foundation rather
than a research question, and it is deliberately a separate commit so that a wiring mistake
cannot be confused with a transcription mistake.

---

## The wiring: the node is open, and the error moved to the layer above

`ice_giant` is out of `FLUID_CLASSES`. A body declared with an ice fraction and a potential
temperature now integrates: rock, then an ice mantle on `h2o_hot`, then the H/He envelope.

### The result, and what it names

| planet | R derived | R published | Δ |
|---|---|---|---|
| Uranus | 4.930 R⊕ | 3.981 R⊕ | **+23.8 %** |
| Neptune | 4.992 R⊕ | 3.865 R⊕ | **+29.2 %** |
| Uranus, H/He removed | 3.092 R⊕ | 3.981 R⊕ | **−22.3 %** |

Compositions come from Scheibe+ 2019's Table 1 rows built on this same water EOS, so the
structure is borrowed rather than fitted.

The third row is the finding. Both planets come out too large; removing the envelope
overshoots the other way; the measured radius sits between them. So the error is **the H/He
envelope, not the ices**: 13.8 % of Uranus's mass adds 1.84 R⊕ on the n = 1 polytrope where
the real envelope adds about 0.9. Running the same body with only 5 % H/He gives 4.01 R⊕,
essentially Uranus — the polytrope needs 2.8× less gas than the planet has.

That is the objection the old refusal already carried: "n = 1 폴리트로프는 H/He 압축성에
맞춰진 것이라 여기 쓸 수 없다". Bringing in the ices did not remove it, it **relocated** it.
Fixing it needs an H/He equation of state, which is a different literature and a separate
piece of work. The domain row says so, and the grade is analog.

Central temperatures land unevenly — Uranus 5978 K against a published 5700, Neptune 10017
against 5500. Uranus is close; Neptune is not, and the reason is not diagnosed. Recorded as
an open number rather than explained away.

### What the declaration means on this branch, and why

`potential_temperature` is defined as the surface value, but the H/He polytrope carries no
thermal constants, so temperature does not flow through the envelope: T is constant across it
and the declaration lands at the **top of the ice mantle**. That is a real semantic shift for
this branch and it is stated in the refusal and the domain rows. The alternative is an H/He
thermal treatment, which is the same missing piece as above.

### Two mistakes the tests caught

**A speed optimisation broke an identity.** Passing the previous temperature pass's central
pressure as the next pass's bracket is worth 27 %, and it changes the secant's path, so the
converged value moves in its last bits. That breaks "at the reference potential temperature
the answer does not move, bit for bit" — an identity this file treats as load-bearing rather
than as a tolerance. Reverted, with the reason in the code so it is not re-attempted.

**The density inversion was 200-step bisection.** The first ice giant ran past ten minutes.
`P(ρ)` is nearly a straight line in log-log, so a secant with the bracket kept as a fallback
does the same job in about eight evaluations; warm-starting both that and the Fermi inverse
from the previous call cut a single integration from 1.31 s to 0.58 s, and the two tests
confirmed the answers did not move.

### The cost that remains

One ice giant is 24 to 500 seconds. The density inversion sits in the integrator's inner loop
and each call evaluates Fermi integrals, so this branch is two orders slower than the rocky
one. It is therefore **not in `check.sh`**: the anchors are behind
`test_interior.py --icegiant`, and what `check.sh` runs is the wiring and the material's
temperature fences, which need no integration. That is a real gap — the anchors are not
routinely checked — and it is named here rather than hidden by a smaller test case.
