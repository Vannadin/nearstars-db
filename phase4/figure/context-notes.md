<!-- Body-figure 작업 결정·근거 누적 — 다음 세션이 재도출 없이 이어가도록 -->
# Body Figure (J2 / C22) — Context Notes

Append-only decision log. Why each choice, not just what.

## Scope / timing (owner, 2026-06-25)
- Scope = **Phase 4 active set first** (not whole DB roster). Confirmed v1 set:
  αCen (A·B·Proxima + Polyphemus moons)·Barnard·Tau Ceti·40 Eri (A·B·C + b·c·d)·
  Fomalhaut·TRAPPIST-1 + Luhman 16.
- Timing = after the 40 Eri walk wrapped (c/Twoworld walk committed 857fd39).
- Start with the **methodology doc** (owner: "방법론 문서부터").

## Prior art already in the repo (do not duplicate)
- `principia-geopotential-data.md` already carries: the Radau–Darwin NMoI inversion
  (Helled+2011, arXiv:1109.1627), giant J2 calibration (Jupiter −0%, Saturn −10%
  truncation), the worked **Polyphemus** J2 ≈ 0.023–0.026, the normalization rules
  (J2 = −√5·C̄₂₀; J2 = 10/3·C₂₂), and the body-type cfg forms. → New doc is the
  **method** home; geopotential-data.md stays the **data + cfg-form** companion.
  Cross-reference, don't restate the cfg tables.

## Physics decisions
- **Rotational small parameter** q = ω²R³/GM (mean radius for the NMoI/RD form,
  per Helled+2011). For non-locked bodies ω = 2π/P_rot.
- **Maclaurin (homogeneous)**: f = (5/4)q, J2 = q/2, NMoI = 0.4 — the uniform-density
  *upper bound* on flattening. Real fluid bodies are centrally condensed (NMoI < 0.4)
  → less flattened → use Radau–Darwin with the measured/estimated NMoI.
- **Calibration anchors (rotation-only)**: Earth J2/q ≈ 0.31 (NMoI 0.331), Mars ≈ 0.43
  (NMoI 0.364, +Tharsis non-hydrostatic excess). Rocky free rotators land J2 ≈ 0.3–0.4·q.
- **Synchronous (tidally-locked) bodies**: q_s = n²R³/GM (n = orbital mean motion).
  Both rotation and the static tide load degree-2 → triaxial. Hydrostatic ratio
  **J2 = (10/3)·C22** (Io C22/J2 = 0.304, Titan 0.30 — confirmed). Magnitude calibrated
  on measured synchronous moons: J2 ≈ (0.9–1.1)·q_s for differentiated rocky/icy
  (Io J2/q_s ≈ 1.08, Europa ≈ 0.88). C22 ≈ 0.30·J2.
- **Fossil-bulge caveat**: the Moon (J2/C22 ≈ 9, not 3.33) and Mercury are frozen-in,
  NOT hydrostatic — their bulges record an earlier, faster/closer state. For our
  synchronous bodies assume hydrostatic unless there's a reason not to; flag the option.
- **Stars**: extreme central condensation (NMoI ~0.05–0.08) + usually slow rotation →
  J2 tiny (Sun 2.1e-7). Fast rotator **Fomalhaut A** (A-type, vsini high) is the one
  roster star with non-negligible oblateness → RD with a stellar (low) NMoI.
- **Erid (40 Eri A b)**: fast free rotation (P_rot ~5.1 h) + non-locked → the largest
  *rocky* J2 in the roster. Flagged in the figure memory as the headline case.

## Open / to confirm
- Per-body NMoI assumptions (especially gas giants and the locked rockies' rigidity).
- Whether to emit C22 for low-q locked bodies where it's < ~1e-6 (likely omit, record).
