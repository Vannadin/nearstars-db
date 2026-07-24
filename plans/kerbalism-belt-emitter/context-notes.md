# Kerbalism radiation cfg emitter — context notes

## 2026-07-24 — opened

- Owner green-lit this emit ahead of the project-end emit batch (their own
  earlier deferral, their call to move now). Scope: radiation belts only.
- Owner decisions this session: intensities = **physical values** (option 1);
  "the main consumers will be the exoplanet bodies later — for the solar-system
  cfg I will propose it to the devs upstream." → the patch doubles as an
  upstream proposal: heavy provenance comments (bibcodes, fit IoU), clean
  standalone RadiationModel definitions + @RadiationBody rebinds.
- Single source of truth: the `*_phys` entries in
  `scripts/viz/render_belts_bodies.py` (fit output already lives there for the
  renders). The emitter imports that dict — no second copy of the numbers.
- Gradients (3.3/2.2) equal Kerbalism defaults (Radiation.cs ctor
  radiation_inner_gradient 3.3 / outer 2.2) → not emitted.
- Geomagnetic pole lat/lon cannot come from the render dict (meridian slices
  don't encode polarity/longitude) → explicit cited table in the emitter:
  Earth 80.37/-72.62 (IGRF, stock), Jupiter -80/0 (JRM33, reversed),
  Saturn 90 (Cao 2020 <0.007 deg), Uranus 31.4 (Ness 1986), Neptune 43
  (Ness 1989), Mercury 90 (Anderson 2012 tilt <0.8 deg; the 0.2 R_M north
  offset carries the asymmetry), Ganymede -86 (Kivelson 2002 tilt ~176 deg).
- MM mechanics: new RadiationModel nodes are plain (Kerbalism reads them all);
  rebinds are `@RadiationBody[Name]:NEEDS[RealSolarSystem]:AFTER[KerbalismConfig]`
  (must run after ROK's own Support/RSS.cfg body renames/copies). `%` used for
  fields absent on some stock bodies (Ganymede geomagnetics, its radiation_pause).
- dist/ is gitignored (repo convention) — the emitter is the committed artifact,
  the cfg is generated output.

## 2026-07-24 — NearStars-body extension

- Owner choices: Polyphemus outer belt = L 4.2–10 (Cassandra 8.4 submerged →
  "intermediate"); intensities re-derived from the methodology rather than
  picked from presets; Pandora = refit shape only (values preserved).
- Methodology upgraded first: Part B gained the **saturated-regime calibration**
  (Mauk & Fox 2010, 2010JGRA..11512220M, verified via ADS + cached) — two-anchor
  B² interpolation between Earth (31 µT → 10.4 rad/h) and Jupiter (428 µT →
  ~1500). Polyphemus 170 µT → 313 → 300 rad/h inner; outer = 0.1× (torus-driven
  Jupiter ratio) = 30. The board row cites the methodology doc per the
  refs-provenance rule, and Mauk & Fox lives in the doc, not the row.
- Board rows (alpha_centauri, validator 0 errors): new Polyphemus
  magnetism.radiation_belts row (gated, methodology-derived; structure pinned by
  canon moon L-shells — inner L 1.3–3.0 with peak at Hades 2.07, slot 3.0–4.2
  around Pandora 3.53, fit IoU .97/.97); Pandora row superseded + refit
  replacement (L 1.15–2.2, IoU .98; pause re-encoded nose 2.6 = 2.99/1.15).
  Both rows carry **individual cfg-named fields** (inner_dist … radiation_inner)
  — the packed radiation_model string format is retired.
- Emitter: `load_nearstars_specs()` parses gated radiation_belts rows from all
  phase4 boards → `dist/.../Kerbalism/NearStars-Radiation.cfg` (RadiationModel +
  RadiationBody per body, NEEDS[NearStarsSystem], refs as comments). Errors out
  loudly on legacy packed rows.
- Viewer builder now imports load_nearstars_specs — the Pandora/Polyphemus
  presets come from the gated board (same single source as the emitter); the
  hand-carried artifact sketch values are gone.
