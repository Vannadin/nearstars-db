<!-- C22 — 얼음거대행성 맨틀에 암모니아 분율을 선언 인자로 배선한다. step 1 = 기본값 0, 비트 동일. 사전등록 → 실행 기록 -->
# Ammonia wiring — context notes (C22, step 1)

2026-09-03. **§1–§3 are the pre-registration, committed before any code ran.** §4 is filled in after the
run. Owner's decision, verbatim (`4b8e06ba`): *"1로 하되 조심히 접근하자."* The grounds are in
`ammonia-table-context-notes.md` §"Grounds for the next decision" and `interior-core.md` C22; not re-derived
here.

## 1. What the survey settled before code (parallel seat, three sentences reproduced by the work seat from the cache)

- **Methane's precedent does not transfer.** Bethkenhagen+ 2017 (`1709.04133.md`), the paragraph *before* the
  methane sentence that closed C4's methane half: *"pure ammonia becomes superionic as well but only below
  4000 K (Bethkenhagen et al. 2013)"*. ⚠ Extraction note: the PDF's text layer splits the word (*"superi
  onic"*), in this seat's `pdftotext` run with and without `-layout`; grep the ar5iv `.md` or search
  `superi`. The decomposition products also differ — methane polymerises into long chains, ammonia
  elementises into **N₂ + H₂** (2013 §III: *"the formation of H₂ and N₂ molecules, which is a clear sign that
  the ammonia molecules are at least partially dissociated"*).
- **In our bodies it is not even superionic — it is fluid.** 2013 §III A, Redmer+ 2011 isentropes laid on their
  phase diagram: *"Neither of the isentropes crosses the superionic phase albeit the isentrope of Neptune is
  located very close to the superionic region at 3000 K. According to our phase diagram, ammonia is very
  likely to only occur as a fluid under conditions present in the interior of Uranus and Neptune."* ⚠ "Fluid"
  splits into molecular and dissociated fluid and **the sentence does not say which**; 2017's Fig. 6 caption
  marks *"partial dissociation of ammonia into N₂ and H₂"* on the Uranus model **in the figure only, with no
  printed coordinates**. Both go on the emit label when w > 0.
- **The low-pressure / envelope branch is closed, two reasons.** (i) The *"low-density dissociation corner"*
  (ρ 0.5 g/cm³ · 3000 K) sits at a printed **1.906 GPa** but **3000 K** — a hot, dilute supercritical fluid,
  not an envelope state. (ii) The table's lowest isotherm is 500 K, so real envelope conditions are not in it
  at all; and 2017's structure models put the ice-rich layer **below** *"P₁₋₂ = 10–15 GPa between the outer
  H/He-rich and the inner ice-rich envelope"*. **Target layer: the mantle. `ENVELOPE_WATER` is not touched.**
- **A first-order transition the interpolation crosses, at three isotherms** (2013 §IV A): *"continuity
  between 1.8 g/cm³ and 2.0 g/cm³ in the 3000 K isotherm which coincides with the phase transition between the
  superionic and the dissociated phase. This is a strong indication for a first-order phase transition"*;
  *"the same behavior … for the 1000 K and 2000 K isotherms, but it is less pronounced … between 1.3 g/cm³ and
  1.5 g/cm³"*; *"the same effect should occur … at 500 K between 1.0 g/cm³ and 1.3 g/cm³, but it is probably
  too small to be seen"*. The table does not mark any of them. **Pressures are ours, not the paper's**: Table I
  rows at 3000 K give 1.8 g/cm³ → 59.40 GPa and 2.0 g/cm³ → 76.45 GPa; the paper attaches no pressure to the
  transition.
- **Correction to `ammonia-table-context-notes.md`** (line ~106): the 17.3 % worst interpolation point (ρ 0.5 ·
  3000 K) is **not** in *"the same corner the 5 % flags sit in"* — `ammonia_table.py`'s five flags are at
  4000 K (0.5 · 0.75 · 1.0 g/cm³) and 5000 K (0.5 · 0.75); none at 3000 K. *Adjacent (the hotter neighbour)*,
  and the asterisk means **convergence error** (Appendix: *"uncertainty of up to 5%"*), not dissociation.

## 2. Design — the shape of `mantle_rock_fraction` (C5), nothing new

- New declaration **`ammonia_mass_fraction`** (default **0.0**) on `integrate`, `solve_with_temperature`,
  `solve` (and the `inputs` record), threaded exactly where `mantle_rock_fraction` is.
- In `integrate`, at the deep-mantle water wrap (`in_column and p > water_table.P_MAX_PA`, where `with_rock`
  is applied today): `with_ices(water_mat)` = `mix(water_mat, 1 − w; NH3, w)` when w > 0, else **the same
  object**; then `with_rock` as today. Order: ices first, rock second — the rock fraction is of the ice
  mantle, the ammonia fraction is of its ices.
- Validation as for rock: `0 ≤ w < 1`; needs `imf > 0`; needs a potential temperature (the table is (ρ, T)
  and `Mixture.grad_ad` is c_P-weighted). `_stack` untouched.
- Three labels on the emitted note whenever w > 0 (C22 in `interior-core.md`): methane asymmetry (0.31 vs
  0.08, methane not built); table ceiling below the mantle base (≈ 290–333 GPa vs 820–1016 GPa); convention
  caveat on the adiabat (density grounded, thermal not); plus the survey's two: fluid but molecular-vs-
  dissociated unsaid; partial dissociation into N₂ + H₂ marked only in a figure.
- **`integrate` and `solve` are path-fingerprint functions**, so the fingerprint changes and
  `test_ice_giant.py --refresh` rides in the same commit — **and the refreshed values must equal the old
  ones bit for bit.** The two sentences are not a contradiction; together they are this step's test.

## 3. Pre-registered outcomes

- ① **Default 0 is the old path**: after `--refresh`, every frozen value (`radius`, `nmoi`, `core_pressure`,
  `core_temperature`, …) is byte-identical to the previous `ice_giant_anchor.json`; only `path_fingerprint`
  and `frozen_at` change. *Expected: at w = 0 the wrap returns the same material object.*
- ② **Any value moves** → stop, trace, do not absorb into the refresh. *Not expected.*
- ③ **Opt-in point check confirms §113's prediction**: at w = 0.1159 the mixture built by the wrap gives
  ρ_mix/ρ_H₂O on §113's eight (P, T) points inside **0.9654–0.9705** (−2.9 to −3.5 %), the table's own
  numbers. *Expected — it is the same two materials and the same rule.*
- ④ **Opt-in full solve of Uranus at w = 0.1159**: expected to **refuse by name** — the ammonia table refuses
  above its ceiling (`ammonia_table.density` → `PhaseGap`, ceiling 237–333 GPa by isotherm) and the mantle
  reaches 820 GPa. The refusal is the step-2 prerequisite (a deep-mantle rule) made visible. If it
  **converges**, the evidence gate was not consulted on this layer → trace. If the trial corridor **cycles**
  instead of concluding → record with the cold-flank family (Brief 22's steering rule).
- ⑤ Gate FAIL 0, and what the step adds to its time.

## 4. Run record

*(filled in after the run)*
