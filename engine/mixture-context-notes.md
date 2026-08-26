# Mixture rule — context notes

Decisions taken while giving one layer two materials, and the reasoning behind them.
Appended as the work goes.

## The rule was never in doubt; its validity range was the research

Every giant-planet equation of state in the literature mixes species by the additive volume
law, and says so plainly. Saumon+ 1995 build their H/He tables with "the additive volume
rule and an additional ideal entropy-of-mixing term". Chabrier+ 2019 restate it twenty-four
years later: "based on the so-called additive volume law and thus does not take into account
the interactions between the two species". Baraffe+ 2008 §3.3 gives the form this recipe
uses, "the mass-weighted interpolation of each species contribution at constant intensive
variables, P and T", and calls it "exact in the ideal gas limit, without restriction on the
species mass fractions and densities".

So four papers agree on the rule. None of the four quantifies the error, because each is
using it rather than testing it. The paper that tests it is Vorberger+ 2007, which ran
first-principles DFT-MD on H-He mixtures specifically to "investigate the validity of the
widely used linear mixing approximation" and found deviations up to 8 % in volume at
constant pressure, worst in the region of molecular dissociation and near zero in the pure
molecular phase.

That is the number that belongs in the code, and finding it is why the search was for the
validity rather than for the rule.

## The Z carrier is the honest problem, and none of the three materials is right

Guillot's heavy-element budget is ices plus rock. This file has three candidates and each
fails differently:

| material | composition fit | ceiling | verdict |
|---|---|---|---|
| `h2o` | best — Z in giants is ice-dominated | 37.4 GPa | useless; a giant envelope passes that in its first few per cent |
| `silicate` | plausible middle | 3.5 TPa | covers Saturn's 709 GPa centre, not Jupiter's ~4.4 TPa |
| `fe_prem` | too dense; iron is the dense end of Z, not its middle | 12 TPa | covers both, at the cost of misrepresenting what Z is |

Silicate is the choice, and Jupiter-with-Z declines on its ceiling as a result. Picking
`fe_prem` instead would have made Jupiter run, which is exactly why it was not picked: the
ceiling is a real limit and choosing a material to hide it would be choosing the answer.
The iron numbers are measured in the test anyway, so the alternative is on the record rather
than in the model.

This is the second time the PREM lower-mantle ceiling has bitten. The previous session hit
it putting Guillot's Z into a *compact core*; this one hits it putting the same Z into the
*envelope*. Same ceiling, two different mechanisms, and that repetition is itself the
finding: 3.5 TPa is where this repository's rock stops, and Jupiter's centre is past it.

## Saturn landing at −0.1 % is the result, and it is not a fit

Z = 0.200 is not tuned. It is 19 M⊕ / 95.16 M⊕, the **bottom edge** of Guillot's published
Saturn budget, taken as a boundary rather than searched for. It produces −0.1 % against the
IAU mean radius from +20.7 %.

The temptation is to call that a validation of the recipe. It is not, and the grade says so
below. It validates the *mixture rule*: the rule was handed a composition from a paper and
returned a radius that matches a measurement. What it does not show is any ability to
predict Saturn, because the composition was told to it.

## The grade tracks the declaration, not the fit

The giant branch demotes to `analog` below Jupiter because n = 1 responds to neither mass
nor composition, so a body between the anchors gets Jupiter's answer with no way to say
whether its residual is the 0.6 % kind or the 20.7 % kind. Z changes half of that: the
model now responds to composition. It still does not respond to mass — R = √(πK/2G) has no
M in it, and two giants at the same Z still get the same radius.

So the anchor count went from one passing and one failing to two passing, but the second one
passes *given a declared composition*. The rule adopted:

- `envelope_z > 0` demotes to `analog` regardless of mass, because Z is a declaration this
  recipe cannot derive. Same discipline as `initial_porosity`.
- `envelope_z == 0` keeps the existing mass-based demotion, with its note corrected: Saturn
  is no longer evidence that the branch is wrong at that mass, it is evidence that the
  branch needs a composition there.

The alternative considered and rejected was upgrading the span between the two anchors to
`calibrated`. It reads well and it is wrong: the span is anchored at its ends in *mass*
while the model varies in *Z*, so a 200 M⊕ body inside the span is not interpolating
between two checked points. It is being handed a number that depends only on what Z it was
declared with.

## Undifferentiated has no anchor, and the discriminating test is the substitute

There is no measured C/MR² for a fully undifferentiated rock-metal body. The searches
return Ceres (partially differentiated), Callisto (rock and ice, partially differentiated)
and Enceladus, all of which are the partial case this task is explicitly not doing.

What can be tested is the discrimination a real anchor would perform. Mercury's measured
C/MR² is 0.3460. Run undifferentiated at the same mass and metal fraction, the mixture
returns 0.3934, 13.7 % higher, which is the recipe correctly saying Mercury cannot be
undifferentiated. That is a test against a measured number even though it is not an anchor,
and it is what goes in the test file.

A second property worth asserting: C/MR² comes out 0.3714, 0.3721, 0.3720 for metal
fractions 0.0, 0.325, 0.70. Nearly flat, because a homogeneous body's concentration is set
by self-compression alone and not by what it is made of. That flatness is a prediction of
the mixture rule rather than an accident, so the test pins it.

## What was not added

No new output keys. `Result.evidence()` renders every value into the single line a board row
carries, and the previous session already paid for that lesson: indicators belong in
`reason` and `notes`, values belong in `values` only when something downstream consumes
them. Nothing downstream consumes a mixture diagnostic yet.
