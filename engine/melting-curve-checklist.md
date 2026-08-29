# Checklist: the melting curve above 20.6 GPa, and dispatch by state (C3)

Plan in one line: the ice layer's material is chosen by `body_class` (`h2o_hot` for ice
giants, the condensed ladder for everyone else) because no melting curve reaches above
IAPWS equation (5)'s 20.6 GPa. Bake Reinhardt+ 2022's liquid–solid coexistence line
(20.6–52.4 GPa) and its VII′–VII″ line from the published data, let the local (P, T)
pick the material, and make every result say which phase it got and why.

## Read first
- [x] `interior-core.md` C3, `sub-neptune-context-notes.md`, the domain row at :1078
- [x] the published data (`BingqingCheng/highP-ice`, `figs-1-and-S1/coex-*.dat`) and the paper text (arXiv 2203.12897, fetched into the cache)
- [x] what the ice giants actually reach at their converged point (Neptune 36.6 GPa · 2538 K at the envelope base — 1071 K above the line; the "1797 K" was a trial path)

## Structure questions — answered before any code
- [x] where the curve lives: a baked module (`ice_melt_table.py`), generated, no runtime dependency
- [x] where the seam is: at IAPWS's end (20.6 GPa), measured, not at the two curves' crossing
- [x] the fluid EOS floor is Mazevet's own stated floor (1000 K at ρ ≳ 1 g/cc), a separate object from `ICE_VII_X_T_MAX`
- [x] what carries the phase above 52.4 GPa: nothing — the note says so, availability picks the EOS

## Bake
- [x] `engine/tools/make_ice_melt_table.py` reads the cloned data, writes `engine/ice_melt_table.py`
- [x] the baked module records the data commit, the file names, and the two benchmark checks (triple point 20 GPa · 875 K; direct-coexistence points)

## Dispatch
- [x] `water_t_melt` / `water_liquid_at` extended to 52.4 GPa; `ice_x` carries the curve to where it ends
- [x] `water_phase_name(p, t)` names the phase and the line it was measured against
- [x] `integrate()` picks liquid → `h2o_liquid` (≤ 2.3 GPa) or `h2o_hot` (above, at or above its floor), solid → the ladder; `ice_material` and the `ICE_GIANT_CLASSES` decision are gone
- [x] `ICE_VII_X_T_MAX` and the phase boundaries stay separate objects (test)

## Four conditions
- [x] (a) the seam at 20.6 GPa measured and stated as a number
- [x] (b) the superionic onset compared with Millot+ 2019 — or recorded as unverifiable, with what would verify it
- [x] (c) the table generated, never transcribed
- [x] (d) fit ceiling ≠ phase boundary, in the code and in the test

## Verify
- [x] Neptune passes for a stated reason (the phase at its envelope base, and why)
- [x] anchors bit-identical (condensed · icy · giant); ice giants moved and are reported with the number (Uranus +3.8e-5, Neptune −2.8e-4 in radius)
- [x] gate FAIL 0, grid-phase asserts unchanged, gate cost stated
- [x] `test_ice_giant.py --refresh` in the landing commit (path functions touched)

## Landing
- [x] domain rows (:1060 superionic, :1078 dispatch, :1080 hot water) + Korean mirror
- [x] `interior-core.md` C3 closed, dated
- [x] report to `nearstars-cb`
