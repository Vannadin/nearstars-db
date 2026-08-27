# Checklist: opening the ice-giant envelope

Plan in one line: `ice_giant` sits in `FLUID_CLASSES` and refuses the Uranus/Neptune class
outright. Find out whether the water ladder reaches those conditions, and work to whatever
range that answer allows.

## Temperature-domain question — answer before any code
- [x] where an ice-giant interior sits in P and T, from published models
- [x] compare against the ladder's 20–1800 K ceiling
- [x] pick (1) inside / (2) partly / (3) not at all, and write the answer down first

## Research (ADS, per `nearstars-methodology`)
- [x] ammonia and methane equations of state at these conditions
- [x] the mixing rule's validity for water-ammonia-methane, or its absence
- [x] the ice composition ratio: observationally bound, or a declaration
- [x] what a hot dense-water EOS would cost to bring in

## Code
- [x] the mixing rule's measured limit for planetary ices, with its source
- [x] the composition ratio as a named, cited constant
- [x] `ice_giant` refusal rewritten to name what is missing and how far away it is
- [ ] **not done — the envelope EOS itself.** Reason recorded in the context notes

## Verification
- [x] every existing anchor bit-identical
- [x] the refusal still declines by name, and now names the right thing
- [x] `bash scripts/check.sh` green

## Documentation
- [x] domain row, mixing limit, composition, sources → methodology doc, without growing it
- [x] Korean mirror
