# Checklist: the liquid-water gap, closed with water2

- [x] Brown 2018 bibcode/title checked; SeaFreeze `water2` knots read from the .mat (0–100 GPa × 240–10 000 K); AQUA fetched into the cache and §2.3.5 quoted at its place
- [x] the spline's real validity mapped per isotherm (negative ρ / c_P 10⁶ inside the knot box) — a finding about the library, table in the notes
- [x] `tools/make_water2_table.py` bakes ρ, dT/dP|_S, c_P on a ragged log-P × T grid (0.1 GPa–ceiling × 360–1100 K); interpolation error measured and written into the module
- [x] `eos.DenseLiquidWater` (`h2o_liquid_dense`), refusals by name at the ceiling (too_cold), below 0.1 GPa, outside 360–1100 K; registered
- [x] `integrate.liquid_material` dispatches into the band; water1 box and the ≥ 1000 K Mazevet path untouched; `_ice_verdict` names the representation
- [x] seam water1 ↔ water2 measured (splines and baked tables): ρ 0.13 %, dT/dP 9 % in the baked overlap; unphysical water2 in the ocean region recorded
- [x] seam water2 ↔ Mazevet at 1000 K measured: −2.5 … −3.3 % over 2.3–26 GPa
- [x] `LIQUID_WATER_SHELF` ("not baked") removed; refusal texts in `eos.py`/`interior.py` rewritten; `test_water2.py` in the gate
- [x] Callisto and Titan at f = 0.75: finish in 54 s and 58 s (F2: > 70 CPU-min unfinished) — band tops 0.3265 / 0.3276, the values F2 had traced; F2's open thread closed
- [x] anchors: Uranus/Neptune bit-identical (their converged paths never sit in the band; trial-path refusals keep the too_cold direction); `--refresh` for the fingerprint only (integrate's nested dispatch changed); Europa's gate inversion unchanged (0.2979–0.3655, core 0.071 · ice 0.078); rock/giant anchors untouched — nothing moved
- [x] C3 revisited line; domain rows; materials row; citation (Brown 2018, AQUA); KO mirror; F2/melting notes pointers
- [ ] gate FAIL 0, time added; report to nearstars-cb
