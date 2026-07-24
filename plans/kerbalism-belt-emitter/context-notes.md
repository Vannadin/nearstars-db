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
