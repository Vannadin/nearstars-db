<!-- 상(phase) 조인 키 + 물성 곁표 (전도도 · 조석소산 가중). 사전등록 → 실행 기록 -->
# Phase join key and side tables — context notes

2026-09-04 (afternoon). Owner adopted two items from a separate seat's comparison with the predecessor tool
(relayed by the directing seat): **① a phase name as the join key, with per-phase property side tables**
(electrical conductivity now, tidal-dissipation weight next; latent heat and colour when a consumer appears),
and **② class-default tables behind `authored`** (separate item, after ①). **§1–§2 are the pre-registration,
committed before any table is written.**

**Absolute line**: the predecessor's *pattern* is adopted; **none of its values are** (not a citable source —
copyright, the author's stance; and its shipped example carries a 60 % stellar-mass error). Every cell here is
graded (`measured` / `calibrated` / `analog` / `authored`) with its own source; an empty place is `authored`
with the two markers of `AUTHORED-VALUES-POLICY.md` (`gap:`, `consistent-with:`).

## 1. What the engine actually emits today — read, not copied

Phase keys, as `eos.Phase.name` / single-phase material names (the join key must be one of these):

    fe_prem · fe_eps                                   iron (PREM-fitted alloy · laboratory ε-iron)
    mgsio3_en · mgsio3_prem · mgsio3_pv                silicate (enstatite · PREM-fitted · post-perovskite)
    antigorite                                         hydrated silicate
    ice_ih · ice_iii · ice_v · ice_vi · ice_vii · ice_x  water ices
    h2o_liquid · h2o_liquid_dense · h2o_hot            liquid / hot water (single-phase materials)
    h_he · nh3                                         hydrogen–helium · ammonia (single-phase materials)

**Not phase keys** (state labels, emitted by recipes, not materials): `core_state.conductor_phase` ∈ {liquid,
solid, liquid_outer_solid_inner, undecided}; `interior.ice_column_state`, `interior.silicate_melt_state`. A side
table keyed on phases does not replace these labels; a consumer that needs a property of "the core" maps the
label to the iron phase it names.

**Where a property already lives twice — the double-entry the table is meant to prevent (checked, 2026-09-04):**
- **Electrical conductivity: nowhere yet.** The directing seat's brief says `dynamo_rocky` "holds it internally";
  it does not — `dynamo_rocky` consumes only the `conductor_phase` label and holds no σ (grep: no electrical
  conductivity constant in any engine module; the only conductivities are *thermal*: `cmb_flux.K_CORE`,
  `mantle_flux.K_T`). The first consumer of σ will be the Rm criterion of C23 (Tang+ 2025 eq. 46), not yet built.
- **Tidal-dissipation weight: nowhere yet** (`tidal_heating.py` does not exist; no k₂/Q constant in the engine).
So today the table prevents a *future* double entry, not an existing one — recorded as the fact it is.

## 2. Registered outcomes (before any cell is written)

- **①** For every phase key above, both axes get a row. A cell with a held source is graded by that source; a cell
  with none is `authored` with `gap:` (what was searched: the paper cache via `check_paper_held.py`, and the
  methodology docs) and `consistent-with:` (the bound it sits inside). **No cell copies the predecessor.**
- **②** Success criterion, as the brief set it: *what double entry did the table prevent?* Pre-registered answer
  given §1: none existing; it fixes the single home for σ and the tidal weight before C23 and `tidal_heating`
  are written. If, while writing, a hidden second home for either property turns up, it is named here and the
  table replaces it.
- **③** No consumer is rewired tonight (`dynamo_rocky` has nothing to rewire; C23 and `tidal_heating` do not
  exist). The table ships with a lookup and a test that (a) every emitted phase key has a row on both axes,
  (b) every cell carries a grade and a source or the two `authored` markers, (c) the key set equals the set the
  materials actually emit — a phase added to `eos` without a row fails the gate.
- **④** Anchors untouched; no path-fingerprint function changes; no `--refresh`. Gate FAIL 0; time recorded.
- **⑤** Item ② (class defaults + the three devices: strict mode, per-body authored count in the gate,
  class-table-only) is **not** started under this pre-registration.
- **⑥ Empty cells are legal — and the default** (directing seat, added before any cell was written). 16 phases ×
  2 axes = 32 cells, and most have no held source (ice VII's electrical conductivity, antigorite's k₂/Q …).
  Filling them all as `authored` would build an elaborate structure out of invented numbers — worse than an
  empty table. An empty cell means *the consumer refuses for that phase*, the engine's normal behaviour. The
  table starts nearly empty and fills one cell at a time as a source appears; a missing paper is **not** put on
  the request list for this (it becomes needed when a consumer exists).
- **⑦ Only the two axes with a waiting consumer** (σ ← C23's Rm; k₂/Q ← `tidal_heating`). Colour and latent heat
  are not opened.
- **⑧ The gate prints "filled / total" per axis and the number of `authored` cells** — how empty the table is must
  be visible at a glance; that list *is* the next research queue.
- **⑨ Order against item ②, fixed now so the two policies cannot collide later**: ②'s class defaults attach to
  the **body-class axis only**. *The phase side tables' empty cells are not a target of ②* — a phase is not a
  class — so ② can never silently swallow this table's emptiness.

Side note: the directing seat corrected its own count today — 35 computed nodes, 28 with a recipe field, 11
registered in code, **17** documented-but-uncoded (not "two"). This file's author had not written "two" anywhere.

## 3. Run record — 2026-09-04 (① built: two tables, mostly empty on purpose)

`engine/phase_tables.py` + `engine/test_phase_tables.py`, gate row after `test_payload.py`. The key set is
**read from `eos` at import** (17 keys — the pre-registration's list had 16 written out; `h2o_hot` was the one
counted twice in the head and once on paper) and the test fails when either table's key set differs from it.

    axis           filled / total   authored   filled cells
    conductivity      1 / 17          0        fe_prem — 1.36e6 S/m, RM22 (`2203.01065`) core table, mark D; analog (Earth's alloy core
                                               applied to any fe_prem layer). Cross-check: Tang+ 2025 Table "σ 1×10⁶ S m⁻¹" (their ref. 46);
                                               RM22's own printed λ_m 1.32 vs 1/(μ₀σ) = 0.585 (paper-defects row 14) kept, not resolved.
    tidal_kq         10 / 17          0        mgsio3_en/prem/pv — rocky class band 1e-3…1e-2; ice_ih…ice_x — icy+ocean band 1e-4…1e-2;
                                               h_he — giant band 1e-5…1e-3. All `analog`, source: tidal-heating-methodology §5 class table
                                               (Io / Enceladus / giant anchors). A class band on a phase, labelled so.

**Empty on purpose, with the reason each** (the research queue, ⑧): σ — `fe_eps` (laboratory pure iron is not
the alloy core; no held value), the three silicates (Kislyakova+ 2017 `1710.08761` uses an "Earth-like conductivity
profile for a dry and iron-poor silicate mantle" whose numbers live in its figure, not its text — no printed
value to cite), `antigorite`, the six ices, the three waters (Nettelmann+ 2014 `1402.7299` prints only the
ionic → plasma threshold "> 100 Ω⁻¹ cm⁻¹", a transition marker), `h_he`, `nh3`; k₂/Q — the two irons (the core is
not the dissipating layer in the fixed-Q recipe; no band printed), `antigorite`, the three waters (k₂/Q is a
solid-body quantity; the doc's icy band is for a shell + ocean body), `nh3`. Papers not held (Pozzo+ 2012
`2012Natur.485..355P`, Ohta+ 2016 `2016Natur.534...95O`, checked with `check_paper_held.py`) are **not** on the
request list — they become needed when a consumer exists (⑥).

**Two labels added the same hour (directing seat)**: (1) the ten `tidal_kq` cells are the class band replicated per
phase, **not a phase decomposition** — the difference between phases of one class is 0, and that 0 means "not
distinguished", not "equal"; the phase key carries no information on this axis yet, and a per-phase value replaces
a cell when one arrives. (2) The σ cell is **self-contradictory inside RM22**: the printed λ_m 1.32 m²/s implies
6.03e5 S/m, a factor **2.26** below the printed 1.36e6. C23's Rm = μ₀σUD against a threshold of 50 carries that
factor whole, so C23 must compute Rm with both values and report first whether the on/off verdict flips —
pre-registered now so the choice is not made after seeing the result. Tang+ 2025's ~1e6 fixes the order only.

**② outcome (the success criterion)**: no existing double entry was found to remove; the single home for σ
and k₂/Q now exists before C23 and `tidal_heating` are written — a future double entry prevented, as
pre-registered. **③**: no consumer rewired (there was nothing to rewire). **④**: anchors untouched, no
`--refresh`; `check_paper_tables` rc 0. **⑨** is written into the module docstring: item ② attaches to the
body-class axis only. **No value from the predecessor.**
