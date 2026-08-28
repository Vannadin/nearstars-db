# Checklist: bringing the ice-giant anchor back into the routine gate

Plan in one line: one Uranus solve costs 1038 s, so the Uranus and Neptune anchors sit
behind `test_interior.py --icegiant` and `scripts/check.sh` does not protect them. Find
where the time goes, take back what can be taken back **without moving a single bit of any
anchor**, and if that is not enough, put the anchor under the gate another way and make the
gate say what it skips.

## Before any code
- [x] gate budget decided and the per-body target derived from it (context notes §1)
- [x] `hhe-eos-context-notes.md` §Cost corrected to the final numbers (5.4 s / 1038 s)
- [x] the bit-identity harness written, and a baseline captured for every anchor
      (condensed five, moons six, icy five, Jupiter, Saturn Z = 0 and 0.0825, Earth core, Uranus)
- [x] baseline timings: one ice giant (1038 s quiet · 1257–1360 s under load), the whole gate (14 min 12 s)

## Measure before touching
- [x] cProfile of one Uranus solve: which function owns what share
- [x] `integrate()` call count for one Uranus solve, and the per-integrate cost
- [x] the outer-loop structure counted: temperature passes × bracket tries × pressure shots

## Optimisations (each one: bit-identical on every anchor, or reverted and recorded)
- [x] Python-level work that changes no floating-point operation (recorded per item)
- [x] anything that changes an evaluation path: tried, measured, and either kept with the
      bit check passing or rejected with the reason in the context notes

## Verification
- [x] every anchor bit-identical against the baseline, with every cache switched on
- [x] "at the reference potential temperature nothing moves" still holds (test_interior)
- [x] one ice giant timed before and after
- [x] the whole gate timed before and after
- [x] budget reached, or the shortfall stated — **not reached**: 729 s against 90 s; §6 of the notes says why and what it costs to close

## Landing
- [x] the anchor is in `check.sh`, or one of the three alternatives is chosen and the reason written — route 3, `test_ice_giant.py` + `ice_giant_anchor.json` (notes §7)
- [x] whatever the gate skips, the gate's output says so
- [x] `engine/README.md` cost line, if it changes
- [x] `bash scripts/check.sh` green
