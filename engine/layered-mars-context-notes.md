# Layered Mars — context notes

Append-only. Decisions taken while building, and why.

## Why the names split the way they do

One name, `core_radius_km`, carries two different quantities today.

| Where | What it holds | Which quantity |
|---|---|---|
| the `core_plus_layer_radius_km` block of `bodies/mars.yaml` | 1845.0 km, Durán+ 2022, seismic/diffracted | **apparent** — iron core plus molten layer |
| `_infer_from_state`, reading the declaration | the same declaration, read out | **apparent** |
| `_infer_from_state` → the anchor's `declared` block | the fit's target | **apparent** |
| `fit_sulphur_to_core_radius`, the bisection target | what the bisection aims at | **apparent** |
| the anchor's `fixings.*.core_radius_km` | what the solve produced | **iron core** |
| `_record` in `test_mars_sulphur.py` | the same, recorded | **iron core** |

Samuel+ 2023 prints the relation the split rests on: the apparent core radius is the radius of the
liquid iron alloy **plus** the thickness of the fully molten silicate layer, and the apparent radii
agree between the layered and the homogeneous inversions while the iron radii do not.

So the declaration is renamed and the solver output keeps the old name:

- **declared input** → `core_plus_layer_radius_km`
- **solver output** → `core_radius_km` (unchanged)

`nl2020_exponent` and `nl2020_tcmb` in `test_interior.py` also use `core_radius_km`, but as a local parameter of the Noack &
Lasbleis formula, not as the board declaration. It is left alone.

### Why not `apparent_core_radius_km`

It does not say *apparent with respect to what*, so the old reading survives the rename. The
chosen name closes its own meaning. The objection that it reads oddly on a body with no layer is
the point: when the layer is zero the two radii are equal, and **printing that they are equal is
what distinguishes "we did not look" from "there is nothing there"**.

## Why the device comes before the physics

Prediction ㉣ says three nodes must not move: `dynamo_rocky`, whose edge is declared but whose
module never reads the boundary, and `body_figure` and `cassini_state`, which have no module at
all. Nothing binds that today. Without it, a boundary quantity could leak into one of those nodes
and no run would notice — and the census this item rests on would be wrong with no signal.

The binding is static: re-derive which modules reference the boundary names and compare the set
against a frozen list. It solves nothing and runs in milliseconds.

## Why removing `recorded_disagreement` is not only "turning a red on"

`compare()` in `engine/run.py` prints `[기록·해소?]` when a recorded disagreement has come back inside its
tolerance. The radius axis is inside today, so that line prints on every run. Removing the key
removes that line too. It is the result of this item, not a regression — recorded here because the
line is described in the gate log's own header as being there by design.

## Sequencing

The removal lands in the same plate as the rest. Alone it would publish a gate that is red with
nothing to fix.

## The existing verdict answers a different question than the layer needs

`_silicate_melt_verdict` reduces the rock column to `max_phi` — the largest melt fraction over all
samples — so its answer is **"is the column molten anywhere"**. The layer is a *basal* one: what
this item needs is **"is the silicate molten where it meets the core"**.

`rock_samples` is a tuple of `(p, t)` pairs (`Structure.__init__` stores it; the integrator fills it). **There is no
radius in it.** So the basal question cannot be asked by position.

Pressure is monotone with depth, so the deepest sample is the highest-pressure one, and that is
the handle this item uses. Three branches, and only the first two have a supplier today:

1. the deepest sample is below the solidus → **no basal layer**; the apparent radius equals the
   iron-core radius, and that equality is printed rather than left silent;
2. the deepest sample is molten → **a basal layer exists**, and its thickness has no supplier, so
   the apparent radius is a named `cannot-say` — it is not filled with Khan+ 2023's 150 ± 15 km,
   which is the number this item compares against;
3. the deepest sample is one the melting curve does not reach (`silicate_melt_fraction` returns
   `None` above its range — `_silicate_melt_verdict` collects those as `blind_p`), or it sits inside the
   partial-melt window → **undecided**, named as such.

⚠ Branch 2 is the one the Martian case lands in, and it returns no number. That is the honest
state: the engine can say a basal layer is there and cannot say how thick it is. Anything else
would install a Martian constant, which §1 of the pre-registration forbids.

## Why the anchor was re-frozen twice

`refresh()` takes the digests of its trigger files — `interior.py`, `eos.py`, `chain.yaml` — at the
top of the run, before any fit. So a re-freeze carries the state of `interior.py` as it was when
the run started.

The rename touched `interior.py`; so does the basal-state work. Folding both into one re-freeze
would have been cheaper, and it was not done. The rename is a change of names only, so the six
frozen numbers must come back identical, and that is a check worth having on its own. Run together
with a change that may legitimately move a number, an identical-values check cannot say which
change moved what.

So the first re-freeze carries the rename alone, and the second carries the basal-state work.

## The prescription for this was already in the code

the out-of-range probe in `test_mars_sulphur.py` asks its out-of-range question with the *declared* pin rather than a
pinned name, and the comment above it says why: writing the pin's name into the test makes the
test measure an old decision instead of the declaration on the day the owner changes it — and it
records that this is not hypothetical, a gate went red on exactly that in 2026-09-20.

The rename walked straight through that line, because the line asks by declaration. **The same
disease had a prescription here already, and this item rediscovered it rather than inventing one.**
Worth saying plainly: the line was not written for the layer work, and it held anyway.
