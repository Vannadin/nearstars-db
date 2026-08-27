# Checklist: opening `body_class`, the branch key nobody checks

Plan in one line: eight `selects` edges leave this node and every one of them picks which
physics applies, yet the value they read is a hand-written string in `bodies/*.yaml` that
nothing verifies. Derive the class from mass and radius against published boundaries, hold
the answer as a **set** rather than a pick, and contrast it against the declaration instead
of replacing it.

## Structure question — answer before any code
- [x] (A) / (B) / (C): what is `body_class`'s relation to the radius-valley gate → **(C)**
- [x] does the valley gate move out of `mass_radius_relation` → **no**, it guards that
      recipe's own domain; branch (B) would touch a file another session holds
- [x] `composition_intent` is a gap: can this node classify without it → **mostly yes**;
      it is load-bearing on exactly one boundary (ice giant / gas giant)
- [x] moons (trap 4): is class "what it is made of" or "what it orbits" → **made of**;
      `BodyState.kind` already carries the orbital role, so this recipe never reads it
- [x] vocabulary: `giant` and `gas_giant` are one class with two spellings

## Research (ADS, per `nearstars-methodology`)
- [x] the radius valley: where it is, how wide, what moves it
- [x] a mass-side reading of the same transition, for bodies with no radius
- [x] the deuterium-burning limit and its published spread
- [x] the hydrogen-burning minimum mass and its metallicity dependence
- [x] gas giant vs ice giant: is there any quantitative criterion, or only convention
- [x] sub-Neptune vs ice giant: same question
- [x] the lower edge: below what size does "class" stop meaning anything
- [x] which published boundaries are **not** ours, and why (Chen & Kipping T(2))

## Code
- [x] `body_class.py`: the ladder, one band per boundary, narrowing not choosing
- [x] every constant carries source, validity limit, and why that value
- [x] the valley band is **imported** from `mass_radius.py`, never re-typed
- [x] declaration vs derivation contrasted, declaration never overwritten
- [x] below the hydrostatic floor: decline, naming the consumer that breaks
- [x] `chain.yaml`: `body_class` gains a recipe and its real output list
- [x] `registry.py`: one import line
- [x] `## Contract` block (`check_contracts.py` compares it against the code)

## Verification
- [x] the eight solar-system anchors classify correctly — this is the decision line
- [x] the three declared bodies are reproduced (Earth, Pandora, Alpha Centauri A b)
- [x] boundary-adjacent bodies come back ambiguous, not forced into one box
- [x] a deliberately wrong declaration is caught and reported
- [x] grades split: measured boundaries `calibrated`, conventional ones `judgment`
- [x] `scripts/check.sh` green

## Documentation
- [x] `docs/reference/body-class-methodology.md` (new; the interior doc is another session's)
- [x] `ko/docs/reference/body-class-methodology.md`
- [x] both `methodology-index.md` rows
- [x] `scripts/check.sh` runs the new test
- [x] `python3 scripts/build_docs.py`

## Out of scope — reported, not done
- [x] the eight consumers still read the declared string; wiring them needs `interior.py`
- [x] `GAS_GIANT_CLASSES` / `FLUID_CLASSES` stay where they are (same file)
