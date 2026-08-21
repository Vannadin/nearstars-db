# Binary orbit fix — checklist

Principia-session finding (2026-08-21): shipped initial states give wrong binary orbits.
Root cause confirmed: perifocal velocity formula uses eccentric anomaly E in the
true-anomaly (nu) formula → relative speed wrong by (1-e·cosE)/sqrt(1-e²).

- [x] 1. Fix velocity formula in `scripts/pipeline/build_systems.py` (solve_orbit_relative)
- [x] 2. Fix same formula in `docs/reference/binary-epoch-pipeline.md` §2 step 4 + recompute §10 worked examples (+ ko mirror)
- [x] 3. Rebuild `db/systems/`; verify osculating P/e vs catalog for all 10 flat pairs
- [x] 4. Add third-law consistency gate to `validate.py` (a³/P² implied mass vs Σ mass_msun; binary mass vs principia GM cross-check)
- [x] 5. α Cen: B mass 0.9092→0.9373 (Pourbaix & Boffin 2016, matches phase2), parallax 742.12→747.17 mas (Kervella et al. 2016 orbital parallax) via partial-override mechanism
- [x] 6. eps Ind Ba/Bb: share A's Gaia parallax (LOS 8× gap was parallax-error amplification)
- [x] 7. 36 Oph AB: replace orbit with Irwin et al. 1996 Table 4 Orbit 4 (a=14.7", P=568.9, e=0.92237, i=99.555, w=276.412, W=255.083, T=JD2365125.2); current entry is corrupted (a=4.74 transposition + wrong i/w/W/T)
- [x] 8. Regenerate `dist/NearStars-Configs/Patches/Principia/` cfgs
- [x] 9. Residual-error analysis (why P_osc still deviates from catalog P after fix) → context-notes
- [x] 10. Run scripts/check.sh + pipeline tests
