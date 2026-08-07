<!-- Proxima d 비주얼 art-direction Phase 4 스크래치 — 사용자 창작 영역, 미게이팅 -->
# Phase 4 Draft — Proxima Cen d Visual Art Direction

**Status:** DRAFT · **Phase 4a creative input** · NOT gated, NOT in the DB. The gated
conclusions (surface / appearance / gameplay) live in the decision board
[`../proxima_cen.yaml`](../proxima_cen.yaml) — this `.md` is the 4a scratch that feeds
them and the emit-end texture art pass, not the record of record.

This is the **user's creative domain**. Science below is quoted only as the window
the art choices are checked against.

---

## The body

Ultra-short-period sub-Earth (0.30 M⊕, R 0.72 R⊕ = twice Mercury's size), tidally
locked at 0.029 AU, airless dark basalt, age 4.85 Gyr. Substellar ~450 K, night
hemisphere ~30 K (geothermal floor). Polar magnetic field ~16 G (SPI estimate,
Zapatero Osorio 2026), star's flares phase-locked to the orbit.

## Palette (gated on the board — reference only)

Two-tone space-weathered basalt: fresh shielded mid-latitudes intrinsic `#3c3833`
(Proxima-lit ~`#3c2d17`), flare-weathered magnetic polar caps ~`#2a2622`
(Proxima-lit ~`#2a1e10`), Bond albedo 0.11. The caps are an optical overlay —
they recolor terrain, never reshape it.

**Working-palette rule (owner, 2026-08-07): any hex actually used in graphics
work is the INTRINSIC color (no starlight baked in).** The engine multiplies
the star's light at render time, so lit values would double-apply it. The
Proxima-lit hexes above are preview-only.

Color mechanism map (size-dependent npFe⁰ optics, methodology §4):

- Micrometeorite gardening (planet-wide, field-blind): coarse mpFe → darkens,
  hue stays near-neutral. The baseline "dark basalt everywhere".
- Stellar-wind sputtering (blocked at mid-latitudes by the 16 G field): fine
  npFe⁰ → reddens more than darkens. Mercury takes this unshielded (albedo
  ~0.088); d's shielded belts stay fresher, paler, less red (0.11).
- Cusp-channeled flare ions (concentrated at the magnetic poles): saturated
  dose, npFe⁰ accumulating + coarsening → darkening dominates, red slope
  saturates → near-black brown caps. Brown-black, not pure black, because the
  fine-npFe⁰ red slope survives.

## Terrain / crater density (2026-08-07 owner Q&A)

Grounded lightly against `docs/reference/crater-degradation-methodology.md`
(accumulation vs erasure-channel race). On d the only live eraser is impact
gardening — no fluid erosion, no warm ice, no tectonic repaving — so the surface
runs to saturation:

- **Overall density: Mercury-highlands class, at saturation.** 4.85 Gyr airless
  with the slowest eraser only → crater-on-crater is the physical default.
- **Plains: a subdued lunar-maria miniature is plausible.** 0.30 M⊕ (vs Mercury
  0.055, Moon 0.012) keeps the interior warm longer → early volcanic plains in
  the first ~1–2 Gyr, then ~3 Gyr more bombardment: visibly smoother than the
  highlands yet still densely pocked. IMPORTANT: all-basalt crust → almost no
  compositional albedo contrast (unlike the Moon's bright highlands / dark
  maria). Plains should read through **crater-density contrast only**, not tone.
- **No icy-moon fracture networks.** Europa/Ganymede grooves need an ice shell
  plus tidal flexing (eccentricity); d is dry rock on a circular orbit. Neither
  condition exists.
- **Instead: Mercury-style lobate scarps.** A small iron-cored rock that cooled
  and contracted folds its surface into 100s-km thrust scarps that cut across
  craters — the signature of an old shrunken world. A few ancient despinning
  faults optional.
- **Small craters sharper than Mercury's.** No day-night cycle (locked: 450 K /
  30 K are static) → no thermal-fatigue breakdown of small crater rims. Fine
  craters keep crisp edges.
- **Polar caps are color, not relief.** Crater topography reads through the
  dark weathered caps unchanged.

One line: *Mercury's bones, a faint lunar-maria quiet in the lowlands, no
cracks, small craters crisper than Mercury's, contraction scarps to mark the
age.* Meshes with the gameplay biomes (Day Plains / Craters / Magnetic Polar
Caps).

## Alfvén wing (future in-game visual)

Concept figure `docs/img/proxima-d-alfven-wing.png` (wiki-ready; script
`scripts/viz/render_alfven_wing.py`). Not expressible in Kerbalism's radiation
SDF — if implemented in-game it rides the in-house flux-tube plugin
(`plugins/NearStarsFluxTube/`, YZ Cet SPI arc prototype): a second tube pair,
starward 12° / anti-starward 7°, leaning toward the orbit's trailing side.

## Related

- Board rows: `../proxima_cen.yaml` (d surface / appearance / gameplay)
- `docs/reference/surface-color-albedo-methodology.md` §4 (space weathering)
- `docs/reference/crater-degradation-methodology.md`
- `docs/reference/tidally-locked-temperature-methodology.md` (450 K / 30 K split)
