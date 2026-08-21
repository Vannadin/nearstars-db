# Binary orbit fix — context notes

## 2026-08-21 root cause
- `solve_orbit_relative` velocity: `v = n·a/√(1−e²) · (−sinE, √(1−e²)·cosE)` is the
  **nu-form coefficient with E plugged in**. Correct E-form: `v = n·a/(1−e·cosE) · (−sinE, √(1−e²)·cosE)`.
  Verified both correct forms agree numerically; shipped form off by (1−e·cosE)/√(1−e²).
- Same wrong formula in `docs/reference/binary-epoch-pipeline.md` line ~141 AND its §10
  worked examples — doc, code, and validation examples shared the bug (why tests passed).
- After fix, 8/10 flat pairs close to catalog P within ~3% (Luhman16 0.07%, eps Ind BaBb 0.0%).

## Data-layer issues (independent of formula bug)
- α Cen: astrometry_raw parallax 742.12 (SIMBAD/HIP old) vs orbit-paper 747.17 (Kervella
  2016 orbital parallax); binary_orbits B mass 0.9092 mislabeled pourbaix_correia_2017 —
  phase2 measurements.yaml has 0.9373 (Pourbaix & Boffin 2016, 2016A&A...586A..90P).
  With both fixed: implied M=2.037 vs catalog 2.0428 (0.3%).
- 36 Oph AB entry corrupted: a=4.74 (true 14.7 — digit transposition), i=81 (true 99.555),
  omega=143 (true 276.412), Omega=16 (true 255.083), T_jd=2379956 (true 2365125.2).
  Ground truth: Irwin, Yang & Walker 1996 (1996PASP..108..580I,
  https://ui.adsabs.harvard.edu/abs/1996PASP..108..580I) Table 4 Orbit 4 (authors reject
  Orbits 1-3). Known tension: Irwin fixed π=187.4 mas (van Altena 1993) vs Gaia DR3 168.0
  → third law with Gaia distance implies 2.07 M☉ vs ~1.53-1.67 modern masses. Newer
  self-consistent solution (Giovinazzi et al. 2026, AAS iPoster, cited by arXiv:2608.13243:
  P=501 yr, a=74.9 AU, e=0.8999, M=1.67 — third-law-consistent 0.2%) has no published
  i/omega/Omega/T yet → adopt Irwin Orbit 4 now, swap when Giovinazzi publishes.
- eps Ind A↔B: no A–B orbit exists in DB (P ~ tens of kyr, unconstrained) → components
  placed independently; Ba Gaia parallax 270.66 vs A 274.84 (Δ4.19 mas ≫ physical ≤0.5 mas
  at 1460 AU) → LOS gap 11,486 AU (8× catalog sep). Fix: Ba/Bb share A's parallax.
- Proxima: unbound vs AB in shipped state (relv 3.77 vs v_esc 0.52 km/s) — Gaia relative
  velocity at 13,000 AU is error-dominated; hierarchical orbit is phase_reliable=false by
  design. Not fixable from elements; harmless on game timescales (drift ≪ orbit scale).

## 2026-08-21 residual-error analysis (post-fix)

State vectors are built to be *exactly* Keplerian for the geometry
(a = a_arcsec × Gaia distance, catalog P). That geometry implies a total mass
M_geo = a_au³/P_yr². When the state is integrated (or osculating elements are
re-derived) with the adopted component masses M_cat instead, the period shifts by

    ΔP/P ≈ (M_geo/M_cat − 1) · (3a/r − 1)     — r = separation at the 1950 epoch.

Verified numerically on all pairs (prediction matches measured residual to <0.5%p).
The (3a/r − 1) factor means near-periastron epochs amplify small mass mismatches:
Alpha Cen's −0.3% mass mismatch → −1.2% period; a pair caught at apastron (36 Oph,
factor 0.69) *damps* its large +24% mismatch to +16.6%.

Post-fix residual budget (P_osc vs catalog P):
| pair            | resid  | cause |
|-----------------|--------|-------|
| Luhman 16 AB    | +0.08% | — |
| eps Ind Ba-Bb   | −0.02% | — |
| 40 Eri BC       | −0.10% | — |
| Sirius AB       | +0.22% | Bond 2017 orbit vs Gaia/HIP parallax, sub-percent |
| Eta Cas AB      | +0.96% | mass/parallax source mix, sub-percent masses |
| Alpha Cen AB    | −1.21% | Kervella orbital parallax vs P&B2016 masses, δ=0.3% |
| Procyon AB      | −1.83% | Bond 2015 masses vs visual-orbit geometry, δ=1.6% |
| 70 Oph AB       | +2.97% | catalog masses vs geometry, δ=1.3%, amp 2.6 |
| 61 Cyg AB       | +8.82% | Strand 1952 grade-3 orbit (a=24.3″±2, P=659±50) vs Kervella 2008 masses — inside the orbit's own error bars; phase_reliable=false already |
| 36 Oph AB       | +16.6% | Irwin 1996 fixed π=187.4 mas vs Gaia 168.0 — documented, gate warns; swap to Giovinazzi 2026 when published |

Conclusion: no residual is a code artifact; each is the third-law inconsistency
of its own source mix, now surfaced by validate.py gate 4c-2.

## In-game meaning
Principia integrates GM (stellar-props recommended mass) × emitted initial state.
After unifying binary_orbits masses with phase2 (α Cen B, 61 Cyg B), the shipped
confirmed-set cfg gives Alpha Cen AB P=78.94 yr / e=0.515 (catalog 79.91 / 0.5179).
Proxima remains on the linear fallback: Gaia relative velocity at ~12,700 AU is
error-dominated (3.7 vs v_esc 0.55 km/s) → formally hyperbolic, but drift over
centuries of gameplay is ≪ separation; the 547 kyr orbit is invisible either way.
