# Checklist: making the interior solver carry a temperature

Plan in one line: the integration carries P, m and I but not T, so `ρ(P)` has Earth's
thermal structure folded into it via the PREM fits and nothing else's. Carry T alongside,
make `ρ` a function of both, and get a core temperature out so `core_state` can be wired.

## Structure question — answer before any code
- [x] read `internal-heat-luminosity-methodology.md` and say what its `geotherm` is
- [x] `chain.py affects internal_heat_nontidal` — what an edge would drag in
- [x] pick A / B / C, write the reason down before touching `eos.py`

## Research
- [x] how temperature enters a Birch-Murnaghan / Vinet fit, and its validity range
- [x] the constants, per material, from the literature — **and which materials have none**
- [x] where the temperature profile's anchor comes from, and what sets its shape
- [x] convecting vs conducting layers: one treatment or several

## Code
- [x] `eos.py`: thermal term, every constant with source + table + validity
- [x] `eos.py`: materials with no published constant say so and stay isothermal
- [x] `interior.py`: T integrated alongside P, declared anchor, no derived surface T
- [x] core temperature in `values`, next to `core_pressure`
- [x] grade drops when the answer leans on the declaration
- [x] `## Contract` block updated (check_contracts.py compares it)

## Verification
- [x] step 1 — **Earth no worse**: C/MR² 0.3297, radius +0.3 %. Say how double counting was avoided
- [x] step 2 — Mars 2.7 % · Mercury 2.1 % · Moon 0.3 % · Ganymede 2.1 %, plus the roster six
- [x] step 3 — changing T moves ρ, and by the size the literature expects (ice VI 1.3 %)
- [x] step 4 — core temperature reaches the output
- [x] step 5 — grade drops when temperature is declared
- [x] step 6 — the A/B/C answer is written down
- [x] step 7 — `bash scripts/check.sh` green

## Documentation
- [x] `interior-structure-methodology.md`: relation, constants, validity rows, citations
- [x] ko mirror, same blocks
- [~] doc did not grow — 1279 → 1384 lines (+105). Every addition is one of the four the
      brief allows (relation, constants, validity rows, one line of source each) plus the
      generated validation table; the research itself went to `eos.py` and the context
      notes. Reported rather than paid for by cutting sourced prose. See the note below
- [x] `build_docs.py`

## The size problem is now structural

Two sessions running, the additions have been trimmed to the brief's own list and the
document still grew. It is 1384 lines against a 190-line standard, and the reason is
that it carries both the recipe and every validation section for five mechanisms.

The repository has a precedent for exactly this: `solar-system-radiation-belts.md` was
split out of the magnetosphere methodology on 2026-08-16 "so the recipe carries
conclusions only". The same split here — the five `### ... checked on ...` sections into
a companion validation document — removes roughly 290 lines and loses nothing.

Not done here. It is a new reference document plus its Korean mirror plus an index
registration, which is a scope call for the owner rather than something to do quietly
inside a temperature task.
