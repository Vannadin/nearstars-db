# Checklist: the middle rung (C11)

- [x] the row says what it is and is not: a declared front plus a never-melted crust — **C7 stays closed and C11 is not its repair**
- [x] two declarations, not one: `differentiation_front` (how deep melting reached, cumulative mass fraction) and `crust_rock_fraction` (F3's finding that Malamud's outer mantle is not primordial); `crust_porosity` optional and bounded
- [x] `porosity.py` functions committed first (8786d857), so no intermediate commit is broken
- [x] `_stack` gains the crust as a fourth layer; ice-giant bounds bit-identical to the old formulas (gmf case checked after a negative-crust bug)
- [x] crust = ice ladder + silicate grains by additive volume (Malamud & Prialnik 2015 §3.1.3 / Yasui & Arakawa 2009); a crust step above the melting curve is refused as a self-contradictory declaration
- [x] `PorousCrust` applies eqs. (4)–(6) with Γ = 1 to density only; eq. (7) note carried; refused together with `initial_porosity`
- [x] `solve` validates the partition with numbers; `infer_three_layer` / `_solve_ice_for_radius` bound the ice search by the crust's demand (the first sweep declined every point for want of this)
- [x] directions pre-registered and tested: crust rock raises C/MR², porosity lowers it; front 1.0 bit-identical to the default path
- [x] sweep on a declared grid (200 K; front 1.0/0.9/0.8/0.7/0.6 × X_d 0.3/0.6; one porous point; 270 K refusal recorded) — Titan inside the front 0.8 · X_d 0.6 band, Callisto between two pairs; not tuned
- [x] `test_ice_giant.py --refresh` (integrate/_stack/shoot changed) — values identical (after the negative-crust bug was fixed)
- [x] domain rows EN/KO, contract block, chain.yaml
- [x] C11 row opened and closed in the landing commit; gate FAIL 0; report to nearstars-cb
- [x] reproduction failure (Titan core-0.15 member) traced to an over-broad refusal written after the table; refusal narrowed to `crust_blocked`, both guards checked, grid regenerated on the shipping code — identical; post-mortem and the relay rule recorded
