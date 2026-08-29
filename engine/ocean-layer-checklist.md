# Checklist: the ocean layer, and the inversion it forces open

Plan in one line: the melting curve already says *which* part of an ice column is liquid,
but the integrator never hears it. Give liquid water an equation of state, let the ice
column switch to it wherever the local (P, T) sits above the melting curve (interpolated
inside the step, never quantised to it), and let the inversion take the extra unknown a
three-layer body brings: return the band, narrow it when C/MR² is supplied.

## Structure questions — answered before any code (`ocean-layer-context-notes.md`)
- [x] where the liquid-water EOS comes from (SeaFreeze `water1`, Bollengier+ 2019)
- [x] how the phase fraction enters the integrator (inside the `h2o` material, as a
      step-pinned sub-phase with the crossing located inside the step)
- [x] what the inversion's extra unknown is (a returned band; C/MR² narrows it; the
      ocean thickness itself is not an unknown but follows the declaration)

## Code
- [x] `eos.py`: liquid water material, baked from SeaFreeze `water1` (table, not three
      constants: measured, the three-constant reading is 5–10 % off — see notes)
- [x] `tools/make_water_table.py` + `water_table.py`, same discipline as the H/He table
- [x] `interior.py`: `integrate()` pins the ice column's phase per step, locates the
      solid/liquid crossing inside the step, commits the partial step, switches
- [x] `interior.py`: ocean thickness and ice-shell thickness reach the output
- [x] `interior.py`: the "density is not touched" note becomes the truth of what is now done
- [x] `interior.py`: three-layer inversion (`infer_three_layer`) — band, then C/MR² narrowing
- [x] the grade drops as far as the answer leans on the declaration
- [x] `chain.yaml`: outputs list; the cycle inside the node declared
- [x] `## Contract` block (`check_contracts.py` compares it)

## Verification
- [x] step 1 — condensed anchors bit-identical (Earth · Mars · Mercury · Moon)
- [x] step 2 — the ocean actually moves density (radius and C/MR² change with an ocean)
- [x] step 3 — grid phase at the new boundary: 1499 ↔ 1501 within 1e-5
- [x] step 4 — the five icy moons: how many now reach the published C/MR², and why not
- [x] step 5 — the inversion handles a three-layer body and narrows without picking
- [x] step 6 — the cycle is declared and convergence reported
- [x] step 7 — cost: the four engine tests, before → after
- [x] step 8 — `bash scripts/check.sh` green

## Documentation
- [x] `interior-structure-methodology.md`: the melting section's "verdict only" sentences
      become the ocean section; the Validation icy table regenerated; no net growth
- [x] Korean mirror, same blocks
