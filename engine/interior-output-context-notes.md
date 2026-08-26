# Interior output — context notes

Decisions taken while wiring `interior_layers`' outputs to their consumers, and the
reasoning behind them. Appended as the work goes.

## The class table does not die yet, and saying so is the point

The obvious move is to delete `nmoi_class_table` now that the integration produces a
per-body C/MR². It would be wrong. The integration covers condensed-phase bodies — iron,
silicate, the water ices — and refuses gas giants outright, because an H/He envelope needs
a polytrope the equation-of-state module does not have. Alpha Centauri A b is a giant, and
its NMoI 0.23 comes from the table.

So the table survives with a *narrower declared domain* rather than a deleted edge. That is
a better outcome than deletion anyway: an edge that says "lookup, for the class the
integration cannot reach" states where the remaining debt is, and the debt disappears on
its own when the polytrope lands.

## A judgement that only prose can hold is a judgement that will drift

`_porous_rock_verdict` already computes everything the verdict needs. The mass is compared
against the compaction limit, the central pressure against the grain-fracture threshold,
and both comparisons are formatted into a sentence and appended to `notes`. The numbers are
in the function; only the conclusion leaves as prose.

The cost of that shows up three ways. The roster table prints `solved` for bodies the same
function believes should hold no voids. A test cannot assert on a sentence. And the
methodology document had to restate the argument by hand, which is how it grew — the
document was carrying a value because the return contract was not.

`payload.Result` was built for exactly this: values with units, a regime, a machine-written
reason. The fix is to use it rather than to write better prose.

## Tidal heating is an input, not something to infer

Bierson+ 2019 §2.2 lists what its compaction model does not include, and tidal heating is
on that list — it removes porosity. For Dante the board declares roughly 1200× Io, which is
the single strongest reason to disbelieve a porous solution there.

The interior solver cannot compute that; tidal heating is a different node, and it is not
implemented. The honest wiring is a declared boolean input, the same shape as
`ice_allowed`, which is already a declaration rather than physics. Inferring it from the
body's mass or orbit inside the interior solver would put a second, worse copy of
`tidal_heating` inside a recipe that has no business owning it.

## The verdict narrows; it does not choose

The engine's standing rule is that it narrows the field and the owner picks. The verdict
here says "the published relation's envelope admits this radius, but three regime
indicators say voids should not survive at this mass, this pressure, and this heating".
That is a narrowing. It deliberately does not say which of the two readings — the declared
radius is too large, or the rock is lighter than the silicate this recipe carries — is
correct, because that is a composition question and the answer is not in this recipe.

## `cassini_state` moved too, and that was not scope creep

The task named `body_figure`. But `cassini_state` reads the same `nmoi` from the same class
table, and moving one consumer while leaving the other would have produced a single
quantity with two suppliers — the exact shape of the alias defect the backflow layer exists
to detect (`magnetosphere` / `magnetopause_standoff_rp` / `pause_nose` are three names for
one R_mp, and that is how the Proxima update missed two dependants).

Moving one and not the other is not the smaller change; it is the change that creates the
defect. Both edges moved.

## Two values, not four

The verdict rests on three indicators, and the first draft returned all three as values
alongside the verdict. That was wrong for a reason worth recording: `Result.evidence()`
renders every value into the one line a board row carries, so each added key lengthens
every evidence line for every body forever.

`payload` already has the right home for the indicators — `reason` is written at the branch
that made the decision and therefore cannot describe a different calculation than the one
that ran. So the *verdict* is a value, and the indicators that produced it are in the
reason and the note. Two new keys, `bulk_porosity` and `voids_expected`.

## The verdict is returned on every path, not only the porous one

`voids_expected` is computed in `solve()` and therefore comes back for Earth as readily as
for Dante. That looks like noise on a body nobody was asking about pore space, and it is
deliberate: `check_contracts.py` compares the documented `Returns` against the key set the
code actually produced, so a key that appears only on some paths is a contract that is true
only on some paths. Sometimes-present keys rot.

The roster table absorbs the cost by reading the verdict only where the solution was found
on the porosity axis, and printing `n/a` elsewhere. The value is always available; the
column only speaks where a claim about voids was actually made.

## What the verdict says about Dante and Hades, and what it does not

All three indicators fire for both bodies. That is now computed and asserted rather than
argued in prose, and the roster table prints it. It does not resolve the open question —
the choice between "the declared radius is too large for the declared mass" and "the rock
is lighter than the enstatite this recipe carries" is a composition question this recipe
cannot answer, and the boards were not touched.
