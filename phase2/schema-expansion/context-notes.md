---
type: workspace
title: "Phase 2 Schema Expansion — Context Notes"
slug: schema-expansion-context-notes
cluster: methodology
cluster_role: member
status: active
related: [[schema-expansion-checklist]]
created: 2026-05-21
updated: 2026-05-25
tier: public
---
# Phase 2 Schema Expansion — Context Notes

Append-only log of decisions made during the work. Subsequent sessions
should be able to resume by reading this file.

## 2026-05-21 — Why this expansion

User observed that the Phase 2 TRAPPIST-1 visualization showed only mass
and diameter, and asked whether Phase 2 should cover more (orbital,
temperature, etc.) or if that belongs to Phase 3.

**Answer settled in conversation:** orbital / temperature / atmospheric
retrievals are observed facts (paper directly reports the number), so
they belong to Phase 2, not Phase 3. Phase 3 is reserved for synthesized
art-direction decisions that no single paper can be cited for (PQS
terrain color, visual tinting, ocean state inferred from analog, etc.).

**Why Phase 2 expansion is a prerequisite for Phase 3:** Phase 3 synthesis
takes Phase 2 measurements as `inputs:`. If Teff / Teq / atmospheric
retrieval aren't in the DB as measurements, Phase 3 reasoning would
build on nothing.

## 2026-05-21 — Discovery: prior work already partially done

While inspecting `build_systems.py` and `schema.py`:

- The array-form Phase 2 upgrade (mentioned as in-progress in the
  earlier session and warned about in `nearstars-add-star/references/planet-curation.md`)
  is already complete. `_pick_recommended` handles both single-dict and
  list-of-dict at lines 422-423. `validate_planets_curated` enforces
  ≤1 `recommended: true` per array.
- The build code already references `environment` and `atmosphere` as
  curated-section names at line 722 (for source dedup). These are
  anticipatory hooks — no schema validation exists yet, and no field
  set has been defined. This expansion makes them real.
- `PLANET_ALLOWED_METHODS` whitelist exists (astrometric/direct_imaging,
  ttv/dynamical, rv, transit/transit_timing, predicted/theoretical,
  discovery, unverified). We need analogous whitelists for the new
  stellar and planet categories.

The `references/planet-curation.md` warning about "build script reads
single-object form only" is stale and will be removed once this work
is done.

## 2026-05-21 — Stellar measurement categories — proposed

Six new arrays inside `stellar_props_curated[host]`. Each follows the
existing `mass_measurements` / `radius_measurements` pattern:
`value_<unit>`, `uncertainty_<unit>`, `method`, `reference`, `bibcode`,
`doi`, `recommended`.

| Array | Value key | Unit | Method whitelist (tier ↓) |
|---|---|---|---|
| `teff_measurements` | `value_k` | K | `high_res_spectroscopy` > `low_res_spectroscopy` > `sed_fitting` > `photometric_color` |
| `luminosity_measurements` | `value_lsun` | L☉ | `bolometric_flux` > `sed_fitting` > `photometric` |
| `age_measurements` | `value_gyr` | Gyr | `asteroseismology` > `isochrone` > `gyrochronology` > `activity_age` > `kinematic` |
| `metallicity_measurements` | `value_dex` | dex ([Fe/H]) | `high_res_spectroscopy` > `low_res_spectroscopy` > `photometric_calibration` |
| `rotation_measurements` | `value_days` | days (P_rot) | `photometric_variability` > `v_sin_i` > `zeeman_doppler` > `asteroseismology` |
| `activity_measurements` | `value_log_rhk` | log R'HK (or H_alpha eq. width) | `log_rhk` > `h_alpha` > `x_ray` > `ca_ii_h_k` |

**Open issues / judgment calls:**
- For `activity_measurements`, log R'HK and H-alpha use different scales.
  Decision: store the value with its specific key (`value_log_rhk` vs
  `value_h_alpha_ew_angstrom`) — measurement-object schema permits multiple
  value_* keys but at least one is required (see `MEASUREMENT_VALUE_PREFIXES`).
  Method label disambiguates downstream consumers.
- For `metallicity_measurements`, only [Fe/H] in dex is in MVP. [α/Fe],
  individual elemental abundances are out of scope (Phase 3 wouldn't need
  them — visual rendering doesn't care).
- `kinematic` age is included for completeness (UVW dispersion → age via
  AVR) but is the weakest tier; reserve for halo / thick-disk stars where
  asteroseismology / isochrone fail.

## 2026-05-21 — Planet measurement categories — proposed

Two new sections inside each `planets_curated[host][i]`:

### `environment` — thermal + bulk physical observables

| Key | Unit | Notes |
|---|---|---|
| `equilibrium_temperature_k` | K | Bond albedo assumption typically baked into paper's value |
| `bond_albedo` | — | When paper assumes it explicitly |
| `irradiation_flux_sun` | S☉ | Stellar flux at planet, relative to Earth's solar flux |
| `density_g_cc` | g/cm³ | Either directly reported or recomputed; either is fine to record |
| `dayside_brightness_temperature_k` | K | JWST emission spectrum-derived |
| `nightside_brightness_temperature_k` | K | Phase curve-derived |
| `method` | — | `derived_from_a_l_albedo` / `phase_curve` / `emission_spectrum` / `transit_radiometry` |

### `atmosphere` — spectroscopic atmosphere observables

| Key | Unit | Notes |
|---|---|---|
| `detection` | bool | True if any atmospheric signal detected |
| `species_detected` | list[str] | e.g. `["H2O", "CO2"]` |
| `species_excluded` | list[str] | Non-detections at specified significance |
| `pressure_pa` | Pa | Retrieval-derived surface or reference pressure |
| `scale_height_km` | km | Retrieved or inferred |
| `temperature_profile_k` | dict | optional: pressure-temperature points |
| `method` | — | `transmission_spectrum` / `emission_spectrum` / `phase_curve` / `high_res_cross_correlation` |

**Why split into two sections instead of one big `atmosphere`?**
- `equilibrium_temperature` is reported for *every* planet (derived from
  orbital + stellar params), even ones without atmospheres.
- Spectroscopic detection is sparse — only ~30 planets have any.
- Phase 3 visual rendering will care about Teq for *all* planets but
  atmosphere details only for the spectroscopically observed ones.
- Different paper sources, different reliability tiers.

### Orbital extension keys

Add to `PLANET_ORBITAL_ALLOWED`:
- `period_days` — currently only in `raw`, not curated
- `tperi_bjd` — periastron time (RV-detected planets)
- `tranmid_bjd` — transit mid-time (transit-detected planets)

These are sometimes the *primary* observable a paper reports (instead of
M₀ at epoch). Allowing them avoids forcing a conversion at curation time.

## 2026-05-21 — Decisions deferred to implementation

- Whether to require `method` on Phase 1 (dict) entries. Current code only
  requires it on array entries. Decision: keep that asymmetry — Phase 1
  is "single canonical source", method is optional context. Phase 2 array
  *requires* method since tier-based recommended selection depends on it.
- Whether `environment` should default to `derived_from_a_l_albedo` if
  not specified. Decision: no — require explicit method for traceability,
  even though most papers report Teq under the same a+L+A assumption.
- TRAPPIST-1 backfill scope: minimal verification only (1-2 papers per
  category for one planet — TRAPPIST-1 b, c). Comprehensive backfill is
  out of scope for this expansion task.

## 2026-05-21 — schema.py refactor results

- Old `STELLAR_ALLOWED_METHODS` was a single union applied to both mass
  and radius. Refactored to `STELLAR_MEASUREMENT_KINDS` dict with
  per-category method whitelists. Backward-compat union retained as
  `STELLAR_ALLOWED_METHODS` (derived) — only `docs/reference/methodology.md`
  cites it externally.
- Tightened mass methods to methodology.md set
  (`binary_orbit / asteroseismology / evolutionary_model /
  spectroscopic / spectroscopic_calibration / unverified`).
  Old union also implicitly accepted `interferometry / sed_fitting /
  eclipsing_binary` for mass — those are scientifically valid only for
  radius and aren't in actual use for mass anywhere in the DB.
- Found methodology.md gap: `spectroscopic_calibration` is used for
  radius measurements (Wolf 359, Eta Cas B, Kapteyn — M-dwarf
  radius-color calibrations) but not documented in methodology.md
  Radius tier. Added to whitelist to match practice; documenting in
  methodology.md is a separate doc task (out of scope here).
- Planet validation refactored from hardcoded `("orbital", "physical")`
  tuple to `PLANET_BLOCKS` dict with 4 entries — each block carries its
  own `allowed` field set and `methods` whitelist.
- `validate.py` FAIL: 0 confirmed across 152 systems after refactor.

## Related

- [checklist](checklist.md) — sibling workspace doc in `schema-expansion/`
- [methodology hub](../../docs/reference/methodology.md) — parent topic this workspace contributes to
