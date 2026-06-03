# Checklist — Solar System as an external observer (Phase 2/3 benchmark)

Scenario (confirmed with user 2026-06-03): **hybrid** — realistic
detectability census as framing + counterfactual synthesis on
characterized bodies. Deliverable: **calibration document** (no DB
mutation; Sol is not a ≤50 ly catalog target).

Fiducial observer: 10 pc, near-future instrument suite
(RV ~0.1 m/s + decadal baseline, Gaia-class astrometry ~20 µas,
PLATO/JWST transit, Roman/HWO/ELT reflected-light imaging ~1e-9 contrast).

## Stage 1 — Detectability census (deterministic) ✅
- [x] `detectability.py` — per body: K_RV, astrometric α, transit depth+prob,
      imaging contrast+separation, Teq(assumed A=0.3) vs Teq(true A) vs Tsurf
- [x] Run at 10 pc → census table; verdict per channel vs fiducial floors
- [x] Sanity check: Jupiter K≈12.5 m/s, Earth K≈0.09 m/s, Jup α≈497 µas

## Stage 2 — Ground truth ✅
- [x] Ground-truth table folded into census (M, R, a, e, A_B, Tsurf) +
      per-body benchmark prose — NASA fact-sheet values

## Stage 3 — Reconstructed observer inputs ✅
- [x] Per benchmark body: "Observer has" line (M sin i / true M,
      R if transiting, Teq under albedo assumption, spectral hints)

## Stage 4 — Blind synthesis (methodology trace) ✅
- [x] Jupiter, Saturn (detected set)
- [x] Earth, Venus, Mars, Titan (counterfactual / if-characterized)

## Stage 5 — Benchmark scoring ✅
- [x] Per body: ✓ recovered / ~ partial / ✗ missed + lesson
- [x] Aggregate failure-mode table (7 modes) + Phase 3 takeaways (5)

## Stage 6 — Deliverable ✅
- [x] `docs/reference/solar-system-external-observer.md` (en)
- [x] `ko/docs/reference/solar-system-external-observer.md` (natural prose mirror)
- [ ] (optional, skipped) wiki nav entry — reference docs have no single nav slot;
      cross-linkable like rex-data-comparison.md

## Stage 7 — Verify + commit ✅
- [x] `bash scripts/check-mirrors.sh` — 92/92 OK
- [x] `bash scripts/check.sh` — my-scope gates PASS (gate-5 FAIL is other
      session's plan files + known build_docs.py false positive, not mine)
- [ ] Semantic commit (VaNnadin identity) — pending
