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

## Per-body values (after doc is gated)
- [ ] Compute J2 (+reference_radius) per body; C22 for synchronous bodies.
- [ ] Write into curated source layer (NOT db/systems directly) → build_systems.
- [ ] Validate: hydrostatic self-consistency + check.sh gate.

## Verify
- [ ] Bibliography ADS-verified (delegated agent).
- [ ] Calibration reproduces Jupiter/Saturn/Earth/Io within stated tolerance.
- [ ] `./scripts/check.sh` green (schema/mirror/dead-link/convention/hangul).
