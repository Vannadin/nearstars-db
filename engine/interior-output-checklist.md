# Interior output — checklist

`interior_layers` integrates the layers and returns C/MR², a radius, a core fraction and a
central pressure. Two of those outputs are not reaching the places that need them.

- **NMoI is computed but not consumed.** `body_figure` still takes `nmoi` from
  `nmoi_class_table`, a per-class lookup constant, even though the integration produces a
  per-body value. The class table is the root of J₂, tidal locking and tidal heating, so
  the lookup is load-bearing while a better number sits unused beside it.
- **The verdict is computed but not returned.** For a low-density body with ice excluded,
  the recipe solves an initial porosity and reports `solved`. Whether voids are *expected
  to survive* in that regime is decided inside the same function — from the mass against
  the compaction limit, the central pressure against the grain-fracture threshold, and
  whether tidal heating is declared — and then written into `notes` as prose. A judgement
  that exists only in prose cannot be tabulated, cannot be tested, and drifts.

Both are the same defect: a value the engine already knows, living somewhere the engine
cannot read.

## Why now

The verdict promotion is what makes the later documentation edit honest rather than lossy.
`docs/reference/interior-structure-methodology.md` currently carries the Dante / Hades
judgement in prose because that is the only place it can live. Shortening the document
would delete the reasoning with the words. If the roster table states it from returned
values, the prose can go and nothing is lost.

## Scope

- `chain.yaml` — edge rewiring, and the class table's remaining live rows named.
- `interior.py` — regime indicators promoted from `notes` into `values`.
- `test_interior.py` — the roster table prints the verdict; the indicators are asserted.
- No board edits. The Dante / Hades mass–radius question stays open and is the owner's.

## Tasks

- [x] Confirm which consumers of `nmoi_class_table` the integration can actually serve.
      → verify: the giant row is still required (no polytrope yet), so the table survives
      with a named, narrower domain rather than being deleted. Two consumers, not one —
      `cassini_state` takes the same `nmoi`, and moving only `body_figure` would have left
      one quantity with two suppliers.
- [x] `chain.yaml` — `interior_layers → body_figure (requires, via: nmoi)`; the class-table
      edge demoted to the domain the integration does not cover.
      → verify: `python3 engine/chain.py check` green, and the cycle membership change is
      the one predicted, not a new undeclared cycle.
- [x] `interior.py` — return the regime indicators as values with units:
      mass against the compaction limit, central pressure against grain fracture, and a
      `voids_expected` verdict derived from them.
      → verify: Dante and Hades return the verdict the document argues in prose, computed
      rather than asserted.
- [x] Tidal heating enters as a declared input, not an inference.
      → verify: a body with tidal heating declared and one without differ in the verdict
      and in nothing else.
- [x] `test_interior.py` — roster table gains the verdict column; assertions cover both
      sides of each threshold.
      → verify: `python3 engine/test_interior.py` and `--roster` both green.
- [x] `check_contracts.py` green — the contract block in the methodology document lists the
      new outputs.
      → verify: `./scripts/check.sh`.

## Out of scope

- Deciding the Dante / Hades radii. The verdict makes the finding legible; the choice
  between "the declared radius is too large" and "the rock is lighter than enstatite" is
  the owner's, and neither is taken here.
- The giant polytrope. It is what finally kills the class table, and it has its own prompt.
- Shortening the methodology document. That is the next task, and this one is its
  precondition.

## What it found

- **The core did not grow.** Adding two `requires` edges and dropping one `influences`
  left the coupled core at sixteen nodes and raised the edge count 164 → 165. The
  prediction was that `interior_layers` and `body_figure` are already in the same strongly
  connected component, so no new cycle could appear; `chain.py check` confirms it.
- **The verdict fires on exactly two roster bodies, and for three reasons, not one.**
  Dante and Hades both clear the observed transition mass, both sit far above the
  grain-fracture threshold at the centre (32× and 74×), and both have a declared
  `tidal_heating` row on the board. The roster table now prints `voids? **no**` beside a
  porous solution for each, which is the sentence the methodology document was carrying
  by hand.
- **The other four are unaffected**, which is the check that this is an indicator and not
  a constant: bodies solved on the core or ice axis make no claim about pore space, so the
  column reads `n/a` rather than a verdict about a solution nobody offered.
