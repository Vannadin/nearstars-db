<!-- Phase 3 디스크색 합성 — Mie 산란광 reflectance로 disk_tint_rgb_hex 도출, 고증/vivid 변종 + B/I 검증 -->
# Debris-disk color synthesis (Mie reflectance)

How to derive a circumstellar debris-disk's `disk_tint_rgb_hex` decision when
no resolved scattered-light color exists. Tool:
`scripts/phase3/disk_color_mie.py`.

## Principle

A debris disk's visible color is **scattered starlight**, not thermal
emission. The grains have an intrinsic wavelength-dependent scattering
efficiency `Q_sca(λ)`; the disk we see is `Q_sca(λ) × (stellar SED)`.

We store the **reflectance** color convention: the cfg tint encodes the
*intrinsic dust color* (grey-balanced, star removed), and the renderer applies
the host star's light. This keeps an icy blue disk blue instead of being
swamped by a red M-dwarf's light. White-balance: a flat-`Q_sca` grain must map
to neutral grey.

## Method (what the script does)

1. **Mie scattering** — Bohren-Huffman `bhmie` gives `Q_sca(x, m)` for size
   parameter `x = 2πa/λ` and complex index `m = n − ik`.
2. **Grain-size integral** — integrate over a collisional size distribution
   (`dn/da ∝ a^−q`, q≈3.5) from a blowout floor to a max size. Blowout grain
   size `a_blow ≈ 0.5 µm × (L/L☉)/(M/M☉)` sets the small-end cutoff — luminous
   hosts blow out bigger grains, shifting color.
3. **Wavelength-dependent optical constants** — `n,k` dispersion sampled at
   [400,500,600,700,800] nm per composition: astrosilicate (Draine 2003),
   amorphous carbon (Rouleau & Martin 1991), water ice (Warren & Brandt 2008),
   crystalline olivine (Jäger 2003), tholin (Khare 1984). Composition is the
   biggest lever on hue.
4. **CIE 1931 → sRGB** — `Q_sca(λ)` (reflectance) or `Q_sca(λ)×SED` (absolute)
   integrated against CIE color-matching functions (Wyman 2013 gaussian fit),
   white-balanced, gamma-encoded to sRGB hex.

## Two cfg variants (Sol-Configs model)

Emit BOTH, distinguished by saturation:
- **faithful** — `SAT_FAITHFUL = 0.82`: muted, physically honest.
- **vivid** — `SAT_VIVID = 2.6`: saturation-boosted for visual appeal.

Same hue, different chroma. The cfg writer offers both packs; the user picks.

## Validation (don't skip)

The synthesis is only trustworthy because the blowout/composition physics
reproduces the two disks that DO have measured scattered-light colors:
- **AU Mic** — measured blue (Krist 2005); synthesis B/I ≈ 1.74 vs measured
  ~1.6. ✓
- **Fomalhaut** main ring — measured ~neutral/grey (Kalas 2005); synthesis
  B/I ≈ 0.87 vs ~1.0. ✓

Use `band_ratio()` (B/I) to sanity-check any new belt against a measured
analog before committing the tint.

## When to measure vs synthesize

- **Belt imaged in scattered light** (Fomalhaut main = Kalas 2005, AU Mic =
  Krist 2005) → use the MEASURED color; do not overwrite with synthesis.
- **Thermal / mm-only belt** (no optical scattered-light image) → synthesize.
  Flag `confidence: low` and note it in the host's Phase 3 Open items.

## Provenance

Per-belt grain size / composition / source citations live as comments in
`scripts/phase3/disk_color_mie.py` (`BELTS` table). `db/disks_curated.json`
stores geometry only — the tint provenance is in the script, not meta_notes
(JSON round-trip was not clean). See [[project-nearstars-ring-fabrication]].
