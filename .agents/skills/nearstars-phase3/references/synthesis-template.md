<!-- Phase 3 합성 마크다운 표준 템플릿 — 6개 섹션 + 각 필드 설명 -->
# Phase 3 synthesis — markdown template

Canonical example: `docs/phase3/trappist-1-d.md` (the pilot file).

Every Phase 3 markdown must have this exact section structure to keep
the Korean mirror and HTML build deterministic. Don't add or skip
sections — leave a section empty with a "(none for this planet)" note
if it doesn't apply.

## Header (HTML comment, then H1)

```markdown
<!-- <Planet> Phase 3 synthesis: cfg-ready decisions and reasoning -->
# <Planet> — Phase 3 Synthesis
```

Korean version uses `<!-- <Planet> Phase 3 합성. cfg-ready 결정과 근거 -->`.

## Intro paragraphs (no heading)

Two short paragraphs:

1. **Observational state.** Mass / radius / period / a / insolation,
   plus the cleanest constraint (JWST eclipse depth, transmission
   non-detection, etc.).
2. **Adopted scenario.** One sentence summarizing the cfg choice and
   the alternative scenario it rules out.

## ## Decisions

A single markdown table with these columns exactly:

```markdown
| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | <orbital-period> orbit, tidal damping; Agol 2021 |
```

Confidence values:

- **high** — directly measured or tightly constrained by multiple
  independent observations
- **medium** — theoretical with strong support, OR derived from
  measured quantities with assumed physics
- **low** — aesthetic choice within an allowed observational window;
  could be different and still match data

Standard field list (use these field names so the cfg writers can
match by exact key):

### Orbital
- `tidally_locked`
- `obliquity_deg`
- `eccentricity`
- `argument_of_periastron_deg`
- `sidereal_period_days`
- `semi_major_axis_au`
- `inclination_deg` (optional; usually in Phase 2 already)

### Physical
- `mass_mearth`
- `radius_rearth`
- `surface_gravity_g_earth` (derived)
- `density_g_cc`
- `insolation_s_earth`
- `equilibrium_temp_k` (A=0)
- `equilibrium_temp_k` (A=0.3) — Earth-analog albedo
- `bond_albedo`
- `water_mass_fraction` (range)

### Atmosphere
- `atmosphere_present` (bool)
- `atmosphere_surface_pressure_pa`
- `atmosphere_composition` (prose)
- `atmosphere_scale_height_km` (derived)
- `atmosphere_tint_rgb_hex` (hex string for limb haze)
- `cloud_cover_fraction`
- `cloud_morphology` (prose)
- `cloud_tint_rgb_hex`

### Surface
- `dayside_surface_temp_k`
- `nightside_surface_temp_k`
- `dayside_brightness_temp_k_*` (per JWST filter band, if measured)
- `surface_tint_rgb_hex_primary`
- `surface_tint_rgb_hex_accent`
- `surface_morphology` (prose)
- `surface_ice_caps` (prose)
- `ocean_present` (bool or prose)
- `ocean_extent_substellar_radius_deg`
- `ocean_tint_rgb_hex`

### Interior heating (optional but recommended for cfg-faithful renders)
- `tidal_heating_w_m2`
- `induction_heating_w_m2`
- `radiogenic_heat_w_m2`

### Sky / star
- `star_apparent_angular_diameter_deg`
- `stellar_illumination_color_temp_k`

## ## Surface synthesis

Prose section, 3–6 paragraphs:

1. Observational anchor (what the JWST / HST / theoretical paper
   actually shows)
2. Color choice with M-dwarf-illumination reasoning
3. Iron oxide / mineralogy notes
4. Morphology under tidal lock (cratering, magma relics, ice flow,
   etc.)

## ## Atmosphere synthesis

Prose section. Three required points to cover:

1. **Pressure choice** with σ bound from the cited paper
2. **Composition** with photochemistry / outgassing / escape reasoning
3. **Sky appearance** — what an observer on the surface sees

If atmosphere is absent (e.g. b), explicitly say so and write a brief
"airless sky" paragraph instead.

## ## Rotation & spin synthesis

Prose section. Required points:

1. **Tidal damping argument** for 1:1 vs 3:2 spin-orbit (per Vinson
   2017 / Makarov 2018: 1:1 below e ≈ 0.01, 3:2 above)
2. **KSP implementation note** — rotation period in seconds
3. **Obliquity / seasons** — usually obliquity = 0, no seasons
4. **Optional secular drift** — Lustig-Yaeger 2024 substellar drift
   numbers if cited

## ## Visual styling

Prose section. Bulleted list covering:

- Global appearance (orbit-view)
- Dayside detail
- Terminator band detail
- Nightside appearance
- Atmosphere haze (or absence)
- Star in sky (angular diameter, color temp, brightness analogy)
- Sister planets in sky (angular diameters at conjunction)
- Optional: special features (cryovolcanism, magma glow, etc.)

## ## Bibliography

Four required sub-sections:

```markdown
### Read (visual-informative, drove decisions above)
- **<arxiv_id>** <First-author> <year> — <one-sentence description of
  what the paper contributes to the cfg>
- ...

### Read (context / methodology, not decision-driving)
- ...

### Read (instrument-only, not visual-informative)
- ...

### Not read — no arXiv preprint or low-priority (~N papers)
- **<bibcode>** <title> — <reason for not reading / when to revisit>
- ...
```

The "Not read" section is **intentional** — leaving it empty hides the
audit trail. Always include a count and at least the most prominent
3–5 skipped entries.

## ## Open items for follow-up

Bulleted list. Examples:
- Re-fetch the 2026 Nature Astronomy papers once arXiv preprints appear
- Refine surface tint hex codes when a renderer is available
- Cfg variant for the alternative scenario (preserved as backup)

This section is where the synthesis admits uncertainty. Include
specific numbers / paper IDs that would trigger a revisit.

---

## Block-parity rule (critical for ko mirror)

`build_html.py` pairs the English and Korean files by block order.
Every paragraph, every table, every list, every fenced code block must
have a corresponding block in the Korean file at the same position.

What counts as one block:
- A heading (any level) → 1 block
- A paragraph (one or more consecutive non-empty lines) → 1 block
- A table (header + separator + data rows) → 1 block (column count
  must match across en/ko; row count must match)
- A bulleted list → 1 block (item count must match)
- A fenced code block (```…```) → 1 block
- An HTML comment → 1 block (counts! don't drop them in the mirror)

If you add a new paragraph to en, add a corresponding paragraph to ko
in the same position before running build_html.py.
