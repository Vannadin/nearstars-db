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

## The pool was the project's roster, which is not a generality test

`SYSTEMS` held four system names and `ROCKY_MAX_ME` a hand-picked 20 M⊕ cut. Both were
boundaries this file invented for itself, and together they meant the survey's population
was "the bodies we intend to implement". The solver is general; its sample was not.

The pool now comes from the whole database — 229 planets across 157 files — and
`body_class` decides what counts as rocky. That replaces both hardcoded boundaries with one
published, cited recipe, and it makes the roster the first consumer of a node that eight
`selects` edges are waiting on.

`rocky` is taken as a **candidate**, not a verdict: a body inside a boundary band comes back
with both neighbours alive, and those ambiguous bodies are precisely what this survey exists
to look at. Filtering to the unambiguous ones would delete the question.

## Widening it found what the narrow pool was hiding

17 planets became 88, and two declines appeared that four systems never produced.

- **GJ 341 b** — 4.0 M⊕ at 0.88 R⊕ is 32 g/cm³, denser than pure iron. Refusing is right;
  the declared pair is not a planet.
- **GJ 367 b** — 0.633 M⊕ at 0.699 R⊕. The target sits *between* an all-`fe_prem` body
  (0.7236 R⊕) and pure `fe_eps` iron (0.6774), so the inversion's axis genuinely cannot
  reach it: it needs a core with fewer light elements than Earth's.

Both refusals are correct and **neither message says so** — they report "reason unknown"
from a generic fallback, which fails the engine's own rule that a refusal names a mechanism.
The information to write both messages already exists, since `fe_eps` is carried precisely
as the "cannot be denser than this" limit. Not fixed here: the message lives in
`interior.py`, which another session holds.

## The mass-only tier is empty, and that is a result

No body in the database can be called rocky from mass alone: `body_class` will not put
anything above Chen & Kipping's 2.04 M⊕ break in the rocky class without a radius, and the
database has no radius-less planet below it. Two former members left the pool for that
reason — `Proxima Cen c` and `40 Eridani A b`, both mass-only.

So the survey prints its funnel: 229 scanned, 88 rocky candidates, and the counts for what
each filter removed. A population that narrows silently reads as "we covered everything".

## The test asserts rules, not a name list

The old test held 17 planet names with their expected grades. That was the hardcoding put
back one file over: the pool would be data-driven and the check would re-pin it to the same
seventeen, and any planet the database gained afterwards would go unchecked.

What it holds now is the rules — the pool is wide and comes from the database, the funnel
counts what it dropped, estimated radii never reach the inverter, measured ones do — plus
two sentinels, one per populated tier, that confirm real database rows still land where they
should. The `Msini` caveat is asserted against a constructed row rather than a database one,
because the tier it applies to is currently empty and a rule that stops being checked when
its tier empties is a rule that leaks the moment the tier refills.
