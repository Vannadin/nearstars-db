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

## 2026-07-24 — owner challenge: replace the B² interpolation with the exact recipe

Owner: "단순 보간으로 계산한거야? 방법론 규율대로 정확한 값을 구하는 법을 조사해줘."
Mode A methodology upgrade, three research legs (solo Opus agents):

1. **K–P formula recovered exactly** — not from the paywalled papers but from
   Mauk & Fox's own open Zenodo software (2021zndo...4782323M, doi
   10.5281/zenodo.4782323): the flexible spectral shape, Summers 2009 A4–A8
   relativistic resonance, A1/A2 growth integrals, and the marginal-stability
   condition CmCk = L·Rp·wi/(3·vg) with wave gain 3 (independently confirmed by
   Mourenas 2024, 2024JGRA..12932193M). Cached: mauk_fox_KP.nb + rendered run
   (validation targets: wi=0.658455, CmCk peak 0.608 for Earth L=5) +
   kennel_petschek_recipe.md. Key scaling finding: the limit's controlling
   variable is We/wpe ∝ B/√n_cold + spectral/pitch indices — **NOT B²**.
2. **Flux→dose leg (the reframing)** — no single quotable per-intensity factor
   exists in ADS abstracts; the standard method is SHIELDOSE-2 (Seltzer
   1979ITNS...26.4896S, 1992STIN...9315580S). Load-bearing physics: Mauk & Fox
   show Earth/Jupiter/Uranus sit at COMPARABLE differential K–P caps near
   1 MeV, yet doses differ by orders — **dose contrast is driven by spectral
   hardness (the tail above the ~2 mm-Al transmission cutoff; 1 MeV e⁻ CSDA
   range ≈ 2.0 mm Al) and belt size, not the 1 MeV value**. Textbook free-field
   factor 2.3e-8 rad(Si)/(e·cm⁻²) at 1 MeV, de-rated ~10× behind ~2.5 mm Al.
   Recommendation adopted: anchor-ratio calibration (game Earth 10.4 rad/h)
   with the hardness factor made explicit, not a naked 1-MeV ratio.
3. **Python port** of the Zenodo notebook → scripts/refs/kp_limit.py
   (agent running; validates against the notebook's printed intermediates).

Implication for the methodology: the B² two-anchor interpolation empirically
bundled (KP plateau ratio ≈ O(1)) × (hardness factor) × (shield transport);
the upgrade decomposes it into stated factors with the KP plateau computed
exactly. The Polyphemus rad/h remains a calibrated regime call, but each
factor is now mechanistic and pinned.
