# Checklist: carrying the silicate equation of state above 3.5 TPa

Plan in one line: the silicate material stops at 3.5 TPa because it is built from
Zeng+ 2016's PREM lower-mantle fit, whose author states that ceiling. Find where the
literature actually ends, splice one phase on, and re-measure the three places that
ceiling closed.

## Research
- [x] ADS: what MgSiO3 is above 3.5 TPa, and how it compresses
- [x] ADS: transition pressures with sources — how many phases does the ladder need
- [x] Find where the new fit ends, and what is above *that*
- [x] Reject candidates on the record (context-notes), not silently

## Code
- [x] `eos.py`: the new phase, every constant carrying source + table
- [x] `eos.py`: silicate `over_reason` / `gap_reason` name their mechanism
- [x] `interior.py`: the extrapolated segment shows up in grade or note
- [x] no gap in the silicate ladder

## Verification
- [x] step 1 — five anchors bit-identical below 3.5 TPa (Earth/Mars/Mercury/Moon/Ganymede)
- [x] step 2 — roster six unchanged (Pandora/Cassandra/Hades/Dante/Chaos/Proxima c I)
- [x] step 3 — rocky mass ceiling re-measured, per composition
- [x] step 4 — Jupiter Z retried at 11 / 26 / 42 M(+), reported either way
- [x] step 5 — rock core inside a giant retried
- [x] step 6 — above the new ceiling still declines by naming the mechanism
- [x] step 7 — `bash scripts/check.sh` green

## Documentation
- [x] `interior-structure-methodology.md`: constants row, validity rows, citations
- [x] ko mirror, same blocks
- [~] doc did not grow — 1258 → 1279 lines (+21). Most of the new material went to the
      code comment and the context notes, and the changelog section was compressed into a
      table to absorb the rest; the residual is reported rather than paid for by cutting
      sourced prose
- [x] `build_docs.py`
