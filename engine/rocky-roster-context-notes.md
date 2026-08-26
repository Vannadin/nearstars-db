# Rocky roster — context notes

The handoff listed "run the rocky roster" as work that needed no new recipe: 40 Eridani,
Barnard's Star, TRAPPIST-1 and Proxima have rocky planets in `db/systems`, and the solver
had never been pointed at them. This records what running it found and the decisions the
survey needed.

## The first run's headline was true and misleading

Feeding all seventeen planets to `infer_composition` gives sixteen solved and one declined.
That reads as "the recipe covers the rocky roster", and it is wrong.

Eight of those sixteen were inverted against a radius nobody measured. Barnard's four
planets and Proxima b and d are radial-velocity detections; they do not transit, so no
radius is observable, and the value in the database came from somebody's mass–radius
relation. Inverting composition from a mass and an estimated radius returns the composition
that relation assumed. The signature is visible in the output: Barnard's four planets land
at core mass fractions 0.229, 0.251, 0.255 and 0.260 — a tight cluster, which is what one
curve evaluated four times looks like, not what four independent planets look like.

So the survey's first job is not to compute anything. It is to refuse to compute the eight
answers that would look derived without being derived.

## The error bar decides, not the detection method

The obvious test is `discoverymethod`, and it does not work: the database carries `rv`,
`Radial Velocity` and `theoretical` for what is the same situation, because the rows came
from different upstream sources.

`radius_err_rearth` works. Every measured radius in these files carries an uncertainty and
every estimated one carries `None`. That is not a quirk of this database — it is what
publishing a measurement means — so the rule holds independently of how any particular row
spells its provenance.

Three tiers come out of it:

| tier | what is known | what the survey asks |
|---|---|---|
| measured | transit radius with an error bar, true mass | invert for composition |
| estimated | radius present, no error bar | **nothing** — inverting is circular |
| mass-only | no radius | forward-solve from a declared composition |

## `Msini` is a lower bound, and the forward tier has to say so

Two planets have neither a radius nor a true mass. A forward solve still says something
useful — what this mass would look like under a declared composition — but the mass itself
is `M sin i`, so the true mass is larger. The outcome string carries that, because a
number printed without it invites being read as the planet's mass.

That flag needed reading from two places. `Proxima Cen c` has no `mass_type` in its `raw`
block and `msini` only in `derived`; checking one block silently dropped the caveat for
exactly the planet that most needed it.

## The only decline is not a rock-composition problem

`40 Eridani A b` at 8.47 M⊕ declines because its central pressure reaches 3827 GPa and the
silicate fit stops at 3500 GPa. Bisecting the mass axis puts the Earth-like ceiling at
**6.84 M⊕**, the start of the super-Earth range.

This matters for what happens next. The standing plan was to research *lighter* rock once
the roster produced declines, on the theory that low-density bodies would need it. The
roster produced the opposite: nothing solved on the ice axis, every measured planet solved
on the core axis, and the single decline is a body too *heavy* for the silicate fit's
pressure range. The rock work the roster actually justifies is the high-pressure end.

And that ceiling is the same 3.5 TPa that stops Jupiter's dissolved heavy elements and a
compact rock core inside a giant. Three mechanisms, one limit.

## Reading the database rather than transcribing it

The moon roster in `test_interior.py` is a hand-written table because it carries what the
board declared alongside each body, and that declaration lives nowhere else. This survey is
the opposite case: these are measured exoplanets whose values are already in
`db/systems/*.json`, so transcribing them would create a second copy that drifts.

`db/systems` is build output and must not be edited, but reading it is what it is for.
`derived` is the right block — `mass_kg` and `radius_m` are already unit-normalised, and
the alternative is re-deriving unit conversions the pipeline already did.

## Why the gate runs one inversion and the table runs seven

One inversion scans an axis and then bisects, which costs six to seven seconds. Seven of
them would add forty seconds to a check that already takes two minutes, for a 40 % increase
from one survey.

What the gate needs to protect is the *classification* — that estimated radii stay out of
the inverter, that no planet silently drops from the database, that the caveats still
print. Those are nearly free. The accuracy of the inversion itself is already exercised six
times over by the moon roster in the same run.

So the default checks the wiring with one representative body and `--full` sweeps all
seven; the table regenerates all seven every time it is printed. The decline scan had to be
taught the same discipline — it originally evaluated every row and undid the saving.
