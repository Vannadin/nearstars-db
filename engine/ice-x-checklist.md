# Checklist: carrying the water ice ladder above 37.4 GPa

Plan in one line: water stops at 37.4 GPa, which closes one of the four declared
compositions above 0.0398 M⊕. Find what is published above that pressure, put it in as a
phase, and rebuild the fence at whatever new place the evidence actually ends.

## Structure question — answer before any code
- [x] how a T-dependent boundary enters `Phase`: beside `p_min`/`p_max`, or elsewhere
- [x] is it the same kind of object as `melt`, or a different kind
- [x] write the answer down first (`engine/ice-x-context-notes.md`)

## Research (ADS, per `nearstars-methodology`)
- [x] ice VII thermal constants — does the literature really stay silent
- [x] what phases exist above 37.4 GPa, and what equation of state each has
- [x] where the new fit ends, and what is above *that*
- [x] the superionic boundary: is it inside the range we would use
- [x] what happens to the melting curve, which runs out at 715 K

## Code
- [x] `eos.py`: the new phase, every constant with source, reference state and validity
- [x] `eos.py`: ice VII stops being isothermal, or is recorded as staying so
- [x] `eos.py`: the temperature ceiling, and a refusal that names what is above it
- [x] `interior.py`: the ice verdict follows the ladder up
- [x] `## Contract` blocks unchanged or updated (`check_contracts.py` compares them)
- [x] grade drops where the answer rests on a first-principles fit alone

## Verification
- [x] step 1 — below 37.4 GPa bit-identical (five anchors, six moons, five icy moons)
- [x] step 2 — the `water` preset's mass ceiling, measured and reported
- [x] step 3 — the published icy moons do not get worse
- [x] step 4 — no gap in the ladder, including the new rung
- [x] step 5 — temperature changes the verdict
- [x] step 6 — above the new ceiling it still declines by name
- [x] step 7 — `bash scripts/check.sh` green

## Documentation
- [x] new phase, transition condition, domain rows, one line per source →
      `interior-structure-methodology.md`, without growing it
- [x] Korean mirror, and the tables generated rather than typed
