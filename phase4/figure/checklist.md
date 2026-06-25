<!-- Body-figure (J2/C22) 작업 체크리스트 — 방법론 문서 + 로스터별 값 -->
# Body Figure (J2 / C22) — Checklist

Owner-directed roster-wide oblateness pass. Scope = **Phase 4 active set first**
(αCen·Barnard·Tau Ceti·40 Eri·Fomalhaut·TRAPPIST-1 + Luhman 16); timing = after
the 40 Eri walk (done). Two deliverables: a methodology doc (#13) + per-body values
into the Principia gravity model via the curated source layer.

## Methodology doc (#13) — ✅ DONE (commit 7be62ef, 2026-06-25)
- [x] Draft `docs/reference/body-figure-methodology.md` (English).
  - [x] Rotational figure: q = ω²R³/GM; Maclaurin (homogeneous) vs Radau–Darwin (NMoI).
  - [x] J2 = (2/3)f − (1/3)q; calibrate on Solar-System giants + Earth/Mars.
  - [x] Tidal triaxiality: synchronous q_s = n²R³/GM; J2 = (10/3)·C22 hydrostatic ratio.
  - [x] Body-type regimes: gas giant / free rocky / synchronous rocky / star.
  - [x] Fossil-bulge caveat (Moon, Mercury super-hydrostatic).
  - [x] Worked examples for the active-set roster.
  - [x] Annotated bibliography (ADS-verified bibcodes + anchor values).
- [x] ko mirror `ko/docs/reference/body-figure-methodology.md` (natural Korean).
- [x] Cross-link: methodology-index.md "Pending" → live (EN + ko).

## Per-body values — ✅ DONE (2026-06-25)
- [x] Compute J2 (+reference_radius) per body; C22 for synchronous bodies — full roster, ledger `values.md`.
- [x] Record into the **Phase 4 boards** (the figure source-of-record per SPEC = `phase4/<system>.yaml`,
      NOT the curated DB — J2/C22 are emit-derived from DB mass/radius/rotation; only the art-direction
      (φ, visual a:b:c, NMoI) is persisted). αCen moons' tidal C̄₂₂ corrected (were wrongly "j2~0");
      40 Eri Erid/c/d figure deferrals resolved; Polyphemus confirmed; SPEC stale note fixed.
- [x] Validate: hydrostatic self-consistency + calibration.
- Note: pushing J2/C22 into emitted cfg (Principia geopotential / VertexHeightOblateAdvanced) stays
  at the project-end emit stage; rest-of-DB roster (beyond active set) deferred.

## Verify — ✅
- [x] Bibliography ADS-verified (delegated agent).
- [x] Calibration reproduces Jupiter/Saturn/Earth/Io within stated tolerance.
- [x] Board edits parse + values match ledger + no residual figure-deferral pointers + ko mirror parity.
