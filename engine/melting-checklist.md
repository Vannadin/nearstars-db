# Checklist: letting the interior solver decide whether a layer is molten

Plan in one line: the solver carries P and T at every depth but never asks whether the
material there is solid or liquid, because no melting curve exists in `eos.py`. Put the
curve next to `phase_at(P)` as a material property, and let its two consumers read it —
the warm ice window in `interior_layers`, and the new `core_state` node.

## Structure question — answer before any code
- [x] where does a melting curve live: material property, or a layer of its own
- [x] does `core_state` reuse `interior_layers`' geotherm, or build its own

## Research (ADS, per `nearstars-methodology`)
- [x] iron melting curve at core pressures, with its validity range
- [x] iron melting curve above 365 GPa (super-Earth cores), and the splice
- [x] the light-element depression for an alloyed core, and its published spread
- [x] water melting curve over 209.5 MPa – 2.216 GPa (ices III / V / VI)
- [x] published check values to test the implementation against
- [x] the core adiabat: is `interior_layers`' core temperature usable as-is
- [x] materials with no published curve — name them

## Code
- [x] `eos.py`: `Phase.t_melt(P)`, every constant with source, table and validity limit
- [x] `eos.py`: phases with no published curve say so and stay undecided
- [x] `interior.py`: the warm ice window decides, and says what it did not do to density
- [x] `core_state.py`: the new recipe, its own core adiabat, its own declaration
- [x] `chain.yaml`: `core_state` gains a recipe and its real output list
- [x] `## Contract` blocks for both nodes (`check_contracts.py` compares them)
- [x] grade drops as far as the answer leans on a declaration

## Verification
- [x] step 1 — anchors bit-identical (density is not touched; say so)
- [x] step 2 — Earth's outer core liquid, inner core solid
- [x] step 3 — the warm ice window row becomes a verdict
- [x] step 4 — `core_state` returns `conductor_phase`
- [x] step 5 — moving the temperature flips the verdict
- [x] step 6 — the grade reflects the declaration
- [x] step 7 — `bash scripts/check.sh` green

## Documentation
- [x] melting curves + constants + validity rows → `interior-structure-methodology.md`,
      without growing it (the ice-window row replaces a refusal row)
- [x] `core-state-methodology.md` — new doc, new node, its own contract
- [x] Korean mirrors for both, and both index registrations
