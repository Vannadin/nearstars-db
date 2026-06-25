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

## Fluidity factor φ (added 2026-06-25, owner)
- A synchronous body reaches the full hydrostatic (fluid) figure only if it relaxes like
  a fluid (warm/molten). A rigid/cool body attains less. Knob: **φ = fraction of the
  hydrostatic figure attained** (φ=1 fluid/Io-like; φ<1 partial rigidity). φ scales BOTH
  the visual shape (a−c) AND J₂/C₂₂ together (consistent — less deformed = smaller anomaly).
- Owner art-direction per body. **TODO (batch at end of αCen pass): add φ to methodology
  doc §3 + ko mirror** — currently only in this log + values.md.

## Per-body decisions (roster order)
- **Polyphemus** — gas giant, J₂≈0.023 (settled, = geopotential-data.md). No Kaula (smooth).
- **Dante (A b I)** — locked a=110,000 km (1.54 R_p, just outside fluid Roche), hydrostatic
  J₂ 0.049 (very triaxial, a−c 177 km / 20 %). **Owner φ=0.80** (volcanic, partially molten)
  → J₂ 0.039, C₂₂ 0.0118, visual a−c 141 km (~16 % prolate). Kaula airless_rocky K=2.5e-5.
  Terrain pass: sculpt mesh ~16 % prolate (C₂₂ carries gravity; mesh carries the look).
- **Hades (A b II)** — locked a=148,000 km (2.07 R_p), hydrostatic J₂ 0.0187. **Owner φ=0.70**
  (rigid/tectonic surface but ~400× Io internal heat warms interior → partial relax) → J₂ 0.013,
  C₂₂ 0.0039, a−c ~39 km (5.2 %). Kaula airless_rocky K=2.5e-5. Mesh ~5 % prolate at terrain pass.
- Pandora/Cassandra/Chaos hydrostatic figures computed (J₂ 1.94e-3 / 1.45e-4 / 2.52e-5);
  φ + Kaula pending per-body.

## Visual oblate emit — VertexHeightOblateAdvanced (owner-requested 2026-06-25)
- The Kopernicus PQS Mod **VertexHeightOblateAdvanced** renders
  a body as an oblate/triaxial ellipsoid (James Glaze, MIT, KSP 1.12.x). `oblateMode`: PointEquipotential / UniformEquipotential
  (Maclaurin oblate or Jacobi triaxial from period+density) / Blend / **CustomEllipsoid** (a:b:c).
- Our figure → BOTH gravity (Principia J₂/C₂₂) AND visual (CustomEllipsoid a:b:c). Same source,
  consistent. Tool: `body_figure.py::ellipsoid_ratios()`. a:b:c table in values.md.
- ⚠️ NOT the same as the skill's PQS `deformity` (that is terrain height amplitude).
- **Dependency** — added only when a body has a visible figure (a/c ≳ 1.02). **License = MIT**
  (repo `jamespglaze/VertexHeightOblateAdvanced`, source-verified 2026-06-25) → bundle or
  hard-depend permitted, CC-BY-NC-SA-compatible. It is a HARD dependency for any body using the
  node (no cfg fallback; needs ModuleManager + Kopernicus). kopernicus-cfg skill node added
  (references/oblate-figure.md). **Emit writer deferred to project end**; values + mapping locked now.
- Schema (source-verified): `oblateMode` (PointEquipotential/UniformEquipotential/Blend/
  CustomEllipsoid/ContactBinary) · `energyMode` (Low/High) · mass/geeASL/period · **a/b/c = ratios
  of reference radius, ≥1, c=1 smallest**. Our `ellipsoid_ratios()` output IS this form. Use
  **CustomEllipsoid** for all (deterministic, matches our J₂/C₂₂); UniformEquipotential is the
  physics alternative for fluids. **Volume resolved (2026-06-25), two separate radii (Jupiter/Saturn
  precedent in principia-geopotential-data.md):**
  - Principia gravity: `mean_radius` (volumetric, sets volume) + `reference_radius` (equatorial,
    only scales J₂). Jupiter 69911/71492, Saturn 58232/60330. No inflation — oblateness is in J₂.
  - VertexHeightOblateAdvanced visual: a:b:c all ≥1 inflate by a·b·c (Dante ×1.22) → set the
    **Kopernicus PQS `radius` = polar** (= mean × c_physical). Distinct field from Principia's ref.
    (Real giants don't render oblate, so no precedent for the visual case.)

## Open / to confirm
- Per-body NMoI assumptions (especially gas giants and the locked rockies' rigidity).
- Whether to emit C22 for low-q locked bodies where it's < ~1e-6 (likely omit, record).
