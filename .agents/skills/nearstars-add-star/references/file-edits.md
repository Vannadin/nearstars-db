# File Edits Reference

Edit patterns (case-by-case JSON snippets, judgment notes, gotchas) for
each file touched during star addition. Edit only the files relevant
to your case (see SKILL.md Step 2 table).

> **Field reference** — what each key means and how to obtain its value
> — lives in
> [`docs/reference/adding_stars.md`](../../../../docs/reference/adding_stars.md).
> This document focuses on *which case* applies and the editing pattern
> for it, not on re-defining the schema.

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

> For per-field semantics, see
> [`docs/reference/adding_stars.md`](../../../../docs/reference/adding_stars.md)
> "Add to db/target_list.json".

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

`build_systems.py` solves Kepler + Thiele-Innes per orbit at JD 2433282.5
and distributes components by mass ratio (Hilditch / Pourbaix convention).
See `docs/reference/methodology.md` §"Multiple-System Epoch" for schema
field reference and `docs/reference/binary-epoch-pipeline.md` for the
math pipeline. The 6 existing systems (Alpha Centauri, Sirius, 61 Cygni,
40 Eridani, Eta Cassiopeiae, 36 Ophiuchi) are already in the live schema.

### Schema (live)

Top-level key matches `target_list.system`. Two arrays — `components`
and `orbits` — describe the system.

```json
"Alpha Centauri": {
  "system_id": "alpha_centauri",
  "hierarchy": "binary",
  "wds_id": "14396-6050",
  "components": [
    {
      "name": "Alpha Centauri A",
      "mass_msun": 1.1055,
      "mass_source": "pourbaix_correia_2017",
      "astrometry_source": "mass_weighted_average",
      "astrometry_quality": "barycentric"
    },
    { "name": "Alpha Centauri B", "...": "..." }
  ],
  "orbits": [
    {
      "orbit_id": "AB",
      "relates":  ["Alpha Centauri A", "Alpha Centauri B"],
      "primary":  "Alpha Centauri A",
      "secondary":"Alpha Centauri B",
      "source":   "Pourbaix & Correia (2017) / Kervella et al. (2016)",
      "doi":      "10.1051/0004-6361:20021249",
      "equinox":  "J2000",
      "P_yr":     79.91,
      "T_jd_tt":  2435035.7,
      "e":        0.5179,
      "a_arcsec": 17.57,
      "i_deg":    79.205,
      "omega_deg":     231.65,
      "Omega_deg":     204.85,
      "grade":           1,
      "node_resolved":   true,
      "phase_reliable":  true
    }
  ]
}
```

### `components[].astrometry_source` values

| Value | Build behavior | Required side-data |
|---|---|---|
| `mass_weighted_average` | Build computes barycenter as mass-weighted Cartesian average of all related components' `astrometry_raw.json` entries. All related components must share `epoch_jd`. | none |
| `single_component:<Name>` | Build uses one named component's `astrometry_raw.json` as the barycenter. Use when a published barycentric solution is unavailable but one component is bright/well-measured (e.g. Sirius A as proxy for the AB barycenter). | none |
| `gaia_dr3_nss_barycenter` | Build reads top-level `barycenter_astrometry` block (RA/Dec/parallax/PM/RV at the published epoch) directly. | top-level `"barycenter_astrometry": {...}` |
| `hipparcos_barycenter` | Same as above. | top-level `"barycenter_astrometry": {...}` |
| `gaia_dr3` / `simbad` | Component handled as if it were a single star (linear propagation of its own `astrometry_raw`). Use for components that are not in any fitted `orbits[].relates` (e.g. 40 Eridani A, 36 Ophiuchi C). | none |

`astrometry_quality` is informational: `barycentric` / `photocenter_contaminated`
/ `single_component`. Build does not change behavior on this field, but
validate.py uses it for warnings.

### Triple systems

For 40 Eridani and 36 Ophiuchi, the current entries model only the inner
pair. The outer A-BC (40 Eri) and AB-C (36 Oph) orbits are dropped — both
are observationally underdetermined and Principia's N-body integrator
will correct the relative geometry forward from the per-component initial
state. The outer-component (`40 Eridani A`, `36 Ophiuchi C`) uses
`astrometry_source: "gaia_dr3"` so it falls into the single-star path.

If you need to add a fully resolved hierarchical triple, the schema
reserves `orbits[].primary_is_barycenter_of: ["A", "B"]` for the outer
orbit. `build_systems.py` raises `NotImplementedError` for that field
today — extend `resolve_binary_component_states` before relying on it.

### `phase_reliable: false`

Set when:
- ORB6 grade ≥ 4, OR
- Observed coverage is less than half the period, OR
- Time of periastron error exceeds 5 % of the period

`build_systems.py` still emits per-component Kepler-derived states, but
writes a warning into `meta.notes` so downstream consumers know the
relative geometry at JD 2433282.5 may differ from reality. Principia's
N-body simulation corrects dynamically once gravity takes over.

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
