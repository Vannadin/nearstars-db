# File Edits Reference

Exact schemas and edit patterns for each file touched during star addition.
Edit only the files relevant to your case (see SKILL.md Step 2 table).

---

## 1. `target_list.json` — always edit

Append one entry to the JSON array. Order: place new entries at the end;
the pipeline doesn't care about order.

### Single-star system

```json
{
  "system": "GJ 412 A",
  "components": ["GJ 412 A"],
  "gaia_source_ids": ["762815470562110464"],
  "hip_ids": [54211],
  "binary": false
}
```

### Binary/multiple system

```json
{
  "system": "Luhman 16",
  "components": ["Luhman 16 A", "Luhman 16 B"],
  "gaia_source_ids": ["5353626573562355584", "5353626573562355456"],
  "hip_ids": [],
  "binary": true
}
```

### Bright star with no Gaia DR3 entry (saturation)

```json
{
  "system": "Vega",
  "components": ["Vega"],
  "gaia_source_ids": [],
  "hip_ids": [91262],
  "binary": false
}
```

Empty `gaia_source_ids` → pipeline falls back to SIMBAD astrometry path.
`hip_ids` is informational only; the pipeline doesn't use it.

### Field reference

| Field | Type | Notes |
|---|---|---|
| `system` | string | Canonical system name. Same as component name for single stars. |
| `components` | string array | Hostname per component, in catalogue order (A, B, C, ...). |
| `gaia_source_ids` | string array | Gaia DR3 source_id per component, same order. Use `null` or empty for components without Gaia entry. |
| `hip_ids` | int array | Optional Hipparcos IDs. Pipeline doesn't use. |
| `binary` | bool | True if this system has an entry in `binary_orbits.json`. |

---

## 2. `db/stellar_props_curated.json` — almost always edit

The pipeline auto-fetches spectype/Teff/mesDiameter from SIMBAD but
**never auto-fetches mass**. Without a recommended mass entry,
`principia.gravitational_parameter_km3_s2` is null and Kopernicus
generation is blocked.

### Schema

Object keyed by component name (must match `target_list.components`).

```json
"GJ 412 A": {
  "teff_k": 3537,
  "spectype": "M1.0 V",
  "mass_measurements": [
    {
      "value_msun": 0.39,
      "uncertainty_msun": 0.02,
      "method": "spectroscopic",
      "reference": "Mann et al. 2015",
      "bibcode": "2015ApJ...804...64M",
      "doi": "10.1088/0004-637X/804/1/64",
      "recommended": true
    }
  ],
  "radius_measurements": [
    {
      "value_rsun": 0.40,
      "uncertainty_rsun": 0.01,
      "method": "interferometry",
      "reference": "Boyajian et al. 2012",
      "bibcode": "2012ApJ...757..112B",
      "doi": "10.1088/0004-637X/757/1/112",
      "recommended": true
    }
  ]
}
```

### Field reference

| Field | Required | Notes |
|---|---|---|
| `teff_k` | Optional | Omit to use SIMBAD value. Provide if literature has a more precise number. |
| `spectype` | Optional | Omit to use SIMBAD value. |
| `mass_measurements` | **Required** | Array. Each entry needs `value_msun`, `method`, `reference`, `recommended`. |
| `radius_measurements` | Optional but recommended | Same shape with `value_rsun`. |

### `method` values (governs `recommended` selection)

| Order (best first) | Mass methods | Radius methods |
|---|---|---|
| 1 | `binary_orbit` | `interferometry` |
| 2 | `asteroseismology` | `eclipsing_binary` |
| 3 | `evolutionary_model` | `evolutionary_model` |
| 4 | `spectroscopic` | — |
| 5 | `spectroscopic_calibration` | — |

If you add multiple measurements (Phase 2), set exactly one
`recommended: true` per array — the highest-priority method. Tie-break by
smaller fractional uncertainty. Record the choice in the system file's
`meta.notes` after the build runs.

### Field name discipline

Use `uncertainty_msun` and `uncertainty_rsun`. The `error_*` prefix is
deliberately forbidden by `scripts/pipeline/schema.py`; using it will
fail validation. Other forbidden patterns can be added there as needed.

---

## 3. `scripts/pipeline/fetch_photometry.py` `HIPPARCOS_V` — conditional

Edit only if Gaia DR3 photometry will be missing or unreliable. Typical
triggers:

- Bright star saturating Gaia (`G < ~6` mag) — e.g. Vega, Sirius, Altair
- Cool red dwarf not in Gaia DR3 — e.g. GJ 411, GJ 273
- Component of a close binary where Gaia couldn't deblend

Add a single line under the existing entries:

```python
HIPPARCOS_V = {
    "Sirius A":      -1.46,
    "Alpha Centauri A": -0.01,
    # ...
    "Vega":           0.03,        # source: Hipparcos HIP 91262
}
```

Comment with the source (Hipparcos catalogue, discovery paper, etc.) so
future maintainers can verify. The exact key must match `components`.

---

## 4. `scripts/pipeline/fetch_stellar_props.py` `SIMBAD_ALIASES` — conditional

Edit if SIMBAD's canonical name differs from the form used in
`target_list.json`. Symptoms in the next pipeline run:

- `SIMBAD에 없음 (N개)` list includes the new star
- `stellar_props_raw.json` entry has all-null fields for the star

Typical examples:

```python
SIMBAD_ALIASES = {
    "40 Eridani A":               "GJ 166 A",
    "Chi-1 Orionis A":            "chi01 Ori",
    "Kapteyn":                    "Kapteyn's Star",
    "Mu Herculis A":              "mu Her A",
}
```

To find the right SIMBAD name, query the helper script's output or browse
[simbad.u-strasbg.fr](https://simbad.u-strasbg.fr/simbad/sim-fid).

---

## 5. `db/binary_orbits.json` — only for multi-star systems

**⚠ Schema is in transition (2026-05-18).** The new schema is specified
in `docs/reference/methodology.md` §"Multiple-System Epoch" and the math
pipeline is in `docs/reference/binary-epoch-pipeline.md`. Implementation
(migrating existing 6 entries to the new schema and updating
`build_systems.py` to consume it) is **scheduled for a follow-up session**
— see memory `project-binary-epoch-pending`. Until that lands:

- **Do not add new multi-star systems via this skill** — the existing
  `build_systems.py` does not correctly handle binary orbital motion yet
  (it linearly propagates each component independently, which is wrong
  for any period less than ~few hundred years). New additions would have
  the same bug.
- **If a new multi-star system is genuinely needed before implementation
  is done**, you can add the system as separate single-star entries in
  `target_list.json` (without `binary: true`), accept the wrong relative
  geometry as a known issue, and document in `meta.notes` of the affected
  component files. Then re-process when the binary pipeline ships.

### New schema (target state)

Top-level key matches `target_list.system`. Two arrays — `components` and
`orbits` — replace the legacy single `raw` block.

```json
"Alpha Centauri": {
  "system_id": "alpha_centauri",
  "hierarchy": "binary",
  "components": [
    {
      "name": "Alpha Centauri A",
      "mass_msun": 1.0788,
      "mass_source": "akeson_2021",
      "astrometry_source": "gaia_dr3_nss_barycenter",
      "astrometry_quality": "barycentric",
      "ra_deg":  219.9020833,
      "dec_deg": -60.8339722,
      "parallax_mas": 750.81,
      "pm_ra_masyr":  -3679.25,
      "pm_dec_masyr":   473.67,
      "radial_velocity_km_s": -22.4,
      "epoch_jd": 2457389.0
    },
    { "name": "Alpha Centauri B", ... }
  ],
  "orbits": [
    {
      "orbit_id": "AB",
      "relates":  ["Alpha Centauri A", "Alpha Centauri B"],
      "primary":  "Alpha Centauri A",
      "secondary":"Alpha Centauri B",
      "source":   "akeson_2021",
      "doi":      "10.3847/1538-3881/abfaff",
      "equinox":  "J2000",
      "P_yr":     79.762,
      "T_jd_tt":  2435291.6,
      "e":        0.51947,
      "a_arcsec": 17.4930,
      "i_deg":    79.2430,
      "omega_deg":     231.519,
      "Omega_deg":     205.073,
      "grade":           1,
      "node_resolved":   true,
      "phase_reliable":  true
    }
  ]
}
```

For triples (40 Eridani, 36 Ophiuchi), `orbits[]` carries two entries —
the inner pair, and an outer orbit that uses `primary_is_barycenter_of`
to refer to the inner pair's center of mass. See methodology §"Multiple-
System Epoch" for the full schema field reference and per-system option
table, and `binary-epoch-pipeline.md` §6 for the triple example.

### Legacy entries (current state)

The 6 systems already in `binary_orbits.json` (Alpha Centauri, Sirius,
61 Cygni, 40 Eridani, Eta Cassiopeiae, 36 Ophiuchi) still use the
**legacy** single-`raw` schema. They will be migrated in the
implementation session, not edited piecemeal here. Leave them alone.

### Where to find orbital elements

| Source | Use for |
|---|---|
| [Sixth Catalog of Visual Orbits (USNO)](https://www.astro.gsu.edu/wds/orb6.html) | Visual binary orbits. Has grade (1=best, 9=indeterminate). |
| Pourbaix & collaborators papers | Spectroscopic+visual combined solutions. Highest precision for nearby stars. |
| WDS catalogue | Cross-validation only; not full orbital solutions. |

`orb_grade` ≤ 4 is publication-quality. Higher means lower confidence;
note it in `meta.notes` when building.

---

## 6. `db/planets_curated.json` — Phase 1 default for planet hosts

One key per host star, with an array of curated planet entries.

### Schema

```json
"GJ 412 A": [
  {
    "pl_name": "GJ 412 A b",
    "orbital": {
      "epoch_jd": 2459000.0,
      "semi_major_axis_au": 0.0245,
      "eccentricity": 0.18,
      "inclination_deg": 88.5,
      "longitude_of_ascending_node_deg": null,
      "argument_of_periapsis_deg": 217.0,
      "mean_anomaly_at_epoch_deg": 142.0,
      "source": "Stefansson et al. 2023",
      "doi": "10.3847/1538-3881/ac9a52"
    },
    "physical": {
      "true_mass_mearth": 2.42,
      "uncertainty_mearth": 0.33,
      "mass_type": "true mass",
      "radius_rearth": null,
      "source": "Stefansson et al. 2023",
      "doi": "10.3847/1538-3881/ac9a52"
    }
  }
]
```

### Field reference

| Section | Field | Notes |
|---|---|---|
| `orbital` | `semi_major_axis_au` | AU. Overrides NASA Archive. |
| `orbital` | `eccentricity` | Dimensionless. |
| `orbital` | `inclination_deg` | Degrees. Leave null if not constrained. |
| `orbital` | `longitude_of_ascending_node_deg` | Usually null — only constrained by astrometric fits. |
| `orbital` | `argument_of_periapsis_deg` | Critical for RV systems; check DACE if missing in NASA Archive. |
| `orbital` | `mean_anomaly_at_epoch_deg` | Together with `epoch_jd`, fixes phase. |
| `orbital` | `epoch_jd` | Reference epoch (BJD) for the mean anomaly. |
| `physical` | `true_mass_mearth` | Use if astrometric or transit-derived true mass available. |
| `physical` | `mass_mearth` | Use if only `M sin i` available (RV-only). |
| `physical` | `radius_rearth` | Transit-derived. Null for RV-only detections. |
| `physical` | `mass_type` | e.g. `"Msini"`, `"true mass"`, `"transit"`. |
| `orbital`/`physical` | `source`, `doi` | Always provide. Auto-added to system file's `sources[]`. |

Missing fields stay null — never substitute defaults. The Kopernicus
writer fills these in with documented assumptions later.

Phase 2 escalation: accumulate multiple `physical` and `orbital` entries
in arrays following the same schema and let downstream logic pick the
recommended.
