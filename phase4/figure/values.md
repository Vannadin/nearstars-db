<!-- Per-body figure 값 원장 (J2 + C22 + Kaula 3+) — emit 시 curated 레이어로 이주 -->
# Body Figure Values — per-body ledger

Confirmed degree-2 (J₂, C̄₂₂) + high-degree (Kaula) figure per body, in roster order.
Feeds the curated source layer at the cfg-emit stage. Method:
`docs/reference/body-figure-methodology.md`; tool: `scripts/refs/body_figure.py`.

**Fluidity factor φ** — fraction of the hydrostatic (fluid) figure a body actually
attains; φ < 1 for a partially-rigid / not-fully-molten body. φ scales BOTH the visual
shape (a−c) AND the gravity coefficients J₂/C₂₂ together. Owner art-direction per body.

Kaula K by class: earth_like 1.0e-5 · airless_rocky 2.5e-5 · icy 1.5e-5.
Emit threshold: omit J₂/C₂₂ below ~1×10⁻⁶ (record only).

## α Centauri system

### Polyphemus (α Cen A b) — gas giant ✅
J₂ ≈ **0.023** (NMoI 0.23; range 0.0175–0.0318) + J₄ ≈ −4 %·J₂ + J₆. Zonal only, no
tesseral, no Kaula (smooth fluid). reference_radius 71,492 km. (= geopotential-data.md.)

### Dante (α Cen A b I) — volcanic moonlet, synchronous ✅
Locked to Polyphemus, a 110,000 km (1.54 R_p, just outside fluid Roche), P 9.2 h.
Hydrostatic J₂ 0.049. **Owner φ = 0.80** (volcanic, partially molten, not a full magma
ocean). → **J₂ ≈ 0.039 · C̄₂₂ ≈ 0.0118** (J₂ = 10⁄3·C₂₂). Visual: prolate toward
Polyphemus, **a−c ≈ 141 km (~16 %)** — visibly egg-shaped. Kaula degree 3–8,
airless_rocky K = 2.5e-5, seed "Dante". reference_radius 900 km. **Terrain pass: sculpt
the mesh ~16 % prolate** (gravity C₂₂ already carries it; visual needs the mesh).

### Hades (α Cen A b II) — gray Ganymede-like rocky moon, synchronous ✅
Locked, a 148,000 km (2.07 R_p), P 14.4 h. Hydrostatic J₂ 0.0187. **Owner φ = 0.70**
(compromise: surface reads rigid/tectonic, but big internal tidal heat ~400× Io keeps
the interior warm → partial relaxation). → **J₂ ≈ 0.013 · C̄₂₂ ≈ 0.0039**. Visual: a−c
≈ 39 km (~5.2 % prolate) — mildly egg-shaped, less than Dante. Kaula degree 3–8,
airless_rocky K = 2.5e-5, seed "Hades". reference_radius 750 km. Terrain pass: mesh ~5 % prolate.
### Pandora (α Cen A b III) — Na'vi homeworld, synchronous ✅
Locked, a 252,393 km (3.53 R_p), P 32 h, large (0.72 M⊕, R 5724 km). Hydrostatic J₂
1.94e-3. **Owner φ = 0.95** (large, warm, active → essentially relaxed). → **J₂ ≈
1.84e-3 · C̄₂₂ ≈ 5.5e-4**. Visual a−c ≈ 42 km (**0.74 %** — not visibly egg, reads as a
sphere; C̄₂₂ real for orbits only). **Kaula EARTH_LIKE K = 1e-5** (active tectonics +
ocean) degree 3–8, seed "Pandora" — the first body with a full Earth-like complex geoid
(matters: players orbit low + land → realistic low-orbit perturbation). reference_radius 5724 km.
### Cassandra (α Cen A b IV) — outer retrograde Archean-life moon, FREE rotator ✅
**Free rotation P_rot ~39 h** (3:1-ish, NOT locked) → rotational figure only.
q 1.31e-3, NMoI 0.33 (iron core) → **J₂ ≈ 4.1e-4** (oblate, f ~0.13 %). **No C̄₂₂**
(no fixed tidal axis). Warm (seas, ~270 K) → relaxed, φ≈1. Kaula **earth_like K = 1e-5**
(atmosphere + seas + tectonics → erosion) degree 3–8, seed "Cassandra". reference_radius 3400 km.
### Chaos (α Cen A b V) — outermost retrograde icy moonlet, FREE rotator ✅
**Free fast rotation P_rot 9.5 h** → rotational figure only. q 0.060 (small + fast → large)
→ **J₂ ≈ 0.026** (range 0.021–0.030, NMoI 0.35–0.40), **f ~7 % (1/14)** — visibly oblate
(flattened poles, not egg). **No C̄₂₂** (free rotator). ✅ matches the facet board's
independent f ~0.06–0.075. Warm plumes → relaxed, φ≈1. Kaula **icy K = 1.5e-5**, seed
"Chaos". reference_radius 400 km. Terrain pass: oblate mesh ~7 % (polar flattening).

### α Cen stars — A / B / Proxima C ✅ (all OMIT)
Slow rotators (P_rot 22 d / 41 d / 83.5 d). J₂ negligible (|J₂| ≲ 3e-6, below threshold)
and the Radau–Darwin inversion is out of range at stellar NMoI (~0.06) anyway → **record as
negligible, never emit**. Sun analog J₂ ≈ 2.1e-7.

### Proxima planets (α Cen C) ✅ — all gravity-only, no visible figure
- **Proxima b** — locked, P 11.19 d, 1.07 M⊕/1.02 R⊕. q_s 2.7e-5 → J₂ 2.7e-5, **C̄₂₂ 8.2e-6**
  (>threshold → emit gravity). Visual a−c 0.01 % → skip. φ≈0.95.
- **Proxima d** — locked, P 5.12 d, 0.26 M⊕/0.692 R⊕. J₂ 1.7e-4, **C̄₂₂ 5.0e-5** (emit gravity).
  Visual 0.07 % → skip.
- **Proxima c** — mini-Neptune, FREE, **P_rot 27 h (owner board value)**, 8 M⊕/2.7 R⊕, NMoI 0.23.
  q 6.7e-3 → **J₂ ≈ 8.0e-4** (range 5e-4–1e-3), f 0.45 % → a/c 1.005 **< 1.02 → skip visual**
  (emit gravity J₂). (NOT visibly oblate — earlier 16 h guess was wrong; 27 h is our set value.)
- **Proxima c I** — ice moon ~950 km, locked to c. Small; figure pending exact c-orbit, expected
  below visible threshold → gravity C₂₂ only if above ~1e-6.

---
**α Centauri system figure pass complete.** Visible oblate bodies: Polyphemus, Dante, Chaos,
Hades (4). Everyone else gravity-only or omit. Next system (roster order): Barnard's Star.

## Visual oblate emit — VertexHeightOblateAdvanced (Kopernicus PQS Mod, James Glaze, MIT)

The figure produces TWO independent emits from one calculation: the **gravity** figure
(Principia J₂/C₂₂, above) and the **visual** shape (a Kopernicus mesh via the
VertexHeightOblateAdvanced PQS Mod, `oblateMode = CustomEllipsoid`, a:b:c ratios). Same
figure → consistent. `scripts/refs/body_figure.py` → `ellipsoid_ratios()` outputs a:b:c.
Hard dependency (a body using the node won't render without the plugin), pulled in only by
the bodies that emit a visible figure (a/c ≳ 1.02). **Emit wiring + the kopernicus-cfg skill node are deferred
to the emit stage; values + mapping locked here.** Schema source-verified (repo
`jamespglaze/VertexHeightOblateAdvanced`); **license MIT** (bundle/hard-depend OK,
CC-BY-NC-SA-compatible). a/b/c are ratios of reference radius (c=1 smallest); CustomEllipsoid mode.

| body | mode | a : b : c (c=1) | visual emit |
|---|---|---|---|
| Polyphemus | oblate (giant, f~13%) | 1.149 : 1.149 : 1.0 | yes (Saturn-like) |
| Dante | triaxial (φ0.8) | 1.167 : 1.042 : 1.0 | yes (clear egg) |
| Chaos | oblate (f~7%) | 1.075 : 1.075 : 1.0 | yes (flattened) |
| Hades | triaxial (φ0.7) | 1.053 : 1.013 : 1.0 | yes (mild egg) |
| Pandora | triaxial (φ0.95) | 1.007 : 1.002 : 1.0 | no — sphere to eye (gravity C₂₂ only) |
| Cassandra | oblate (f~0.13%) | 1.001 : 1.001 : 1.0 | no — skip |
