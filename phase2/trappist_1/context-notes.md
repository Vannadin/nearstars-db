# TRAPPIST-1 — Phase 2 Curation Context Notes

Append-only log of decisions made while curating TRAPPIST-1 to Phase 2 depth.
2026-05-20.

## Why TRAPPIST-1 first

User requested a sample run to validate the Phase 2 schema and pipeline
before scaling to all 33 systems. TRAPPIST-1 was chosen because:
- 7 planets — exercises the array-form schema with high cardinality.
- Clear paper hierarchy: Gillon 2017 discovery → Grimm 2018 TTV
  refinement → Agol 2021 best TTV.
- All measurements have NASA Archive `ps` table provenance with
  bibcodes — no need for external ADS fetch.

## Paper selection

NASA Archive `ps` returned 40 planet rows + 9 stellar rows. Filtered to
papers that provide non-null mass or radius:

### Stellar (host TRAPPIST-1)

Sorted by `st_masserr / st_mass` (fractional uncertainty):

| Year | Paper | M (M_sun) | M frac err | R (R_sun) | R frac err |
|------|-------|-----------|-----------|-----------|-----------|
| 2021 | Agol et al. | 0.0898 ± 0.0023 | 2.6% | 0.1192 ± 0.0013 | 1.1% |
| 2018 | Van Grootel et al. | 0.089 ± 0.006 | 6.7% | — | — |
| 2018 | Grimm et al. | 0.089 ± 0.007 | 7.9% | — | — |
| 2017 | Gillon et al. (Nature 542) | 0.0802 ± 0.0073 | 9.1% | 0.117 ± 0.0036 | 3.1% |
| 2016 | Gillon et al. (Nature 533) | 0.08 ± 0.009 | 11% | 0.117 ± 0.004 | 3.4% |
| 2019 | Stassun et al. | 0.0908 ± 0.020 | 22% | 0.1148 ± 0.0034 | 3.0% |
| 2020 | Ducrot et al. | 0.0898 (cited V.G.) | — | 0.1234 ± 0.0033 | 2.7% |

Recommended: **Agol 2021** for both mass and radius — lowest fractional
uncertainty in both. Note Agol 2021 uses Van Grootel 2018 evolutionary
priors with TTV cross-validation, so the actual underlying mass model
is still evolutionary.

### Planetary

Of the 40 ps rows, only papers with `pl_bmasse IS NOT NULL` provide TTV
masses (Gillon 2017, Grimm 2018, Agol 2021). Other papers (Gillon 2016,
Ducrot 2020, Hirano 2020, Luger 2017, Rajpaul 2025, Piaulet 2025) give
radius-only or are atmospheric follow-ups outside the mass/radius scope.

Kept: Gillon 2017, Grimm 2018, Agol 2021 for all 7 planets.
Added Luger 2017 separately for h (planet identification paper).

## Method label decisions

### Planet `method` field

- **Gillon 2017 (Nature 542)**: 7-planet announcement. Mass values
  given are TTV-derived from early TRAPPIST telescope monitoring.
  → label = `ttv`
- **Grimm 2018**: Explicit TTV refinement paper. → `ttv`
- **Agol 2021**: Best TTV (added Spitzer + ground campaigns). → `ttv`
- **Luger 2017**: Identification of planet h via expected resonance.
  Provides radius only. → `discovery`

### Stellar `method` field

`STELLAR_ALLOWED_METHODS` lacks `dynamical` (TTV-constrained stellar
mass). All Gillon/Grimm/Agol stellar values cite Van Grootel 2018
evolutionary models as the underlying mass prior with TTV as a
cross-check, not an independent measurement. Therefore labeled
`evolutionary_model` for those, `sed_fitting` for radii.

Ducrot 2020 stellar radius (0.1234) uses Spitzer's transit-derived a/R*
combined with the evolutionary mass — `sed_fitting` is the closest
match in the whitelist (the spectral-energy-distribution + transit
geometry approach).

Stassun 2019 stellar radius (0.1148) uses Gaia DR2 distance + isochrone
SED fit. → `interferometry` is incorrect (no interferometer used);
labeled `sed_fitting` instead. Original entry in checklist mislabeled
this; corrected here.

## Recommendation choices

- **Stellar mass — Agol 2021**: lowest fractional uncertainty (2.6%
  vs Van Grootel 6.7%), and the TTV cross-check provides independent
  validation of the evolutionary prior.
- **Stellar radius — Agol 2021**: lowest fractional uncertainty (1.1%
  vs Stassun 3.0%). Ducrot 2020 (0.1234) is 3.4% larger than Agol —
  within tier-3 ambiguity but not flagged as 30%+ conflict.
- **Planet mass/radius — Agol 2021** for all 7: explicit upgrade over
  Grimm 2018 with longer baseline and more transit observations.

## Schema notes

`physical` array per planet has 3 entries (Gillon 2017, Grimm 2018,
Agol 2021), except h which has 4 (adds Luger 2017 for discovery
context, no mass).

`orbital` kept as Phase 1 dict (Agol 2021) — paper-to-paper variation
in semi-major axis, eccentricity, and inclination is < 5% and would not
materially change the derived block. Phase 2 array can be added later
if needed for orbital element provenance.

`mass_type` = "true mass" for all TTV entries (planets perturb each
other dynamically — no sin i ambiguity).

## Pipeline run prep

Before running the pipeline, check that:
- `PLANET_ALLOWED_METHODS` (schema.py) contains `ttv`, `discovery`,
  `transit` — confirmed.
- `STELLAR_ALLOWED_METHODS` (schema.py) contains `evolutionary_model`,
  `sed_fitting`, `interferometry`, `spectroscopic_calibration` —
  confirmed (interferometry not used in final Phase 2, but
  spectroscopic_calibration is for Stassun 2019).
- `_pick_recommended` in build_systems.py handles list `orbital`
  fallback to first entry — yes, returns `block[0]` when no
  `recommended: true`.

## Related

- [system-trappist-1 entity pages](../../docs/phase3/trappist-1-e.md) — parent topic this workspace contributes to
