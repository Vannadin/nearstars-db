# Adding Stars to the NearStars Database

How to add a new star (or star component) to the pipeline.

---

## Overview

The pipeline is driven by a single input file: `db/target_list.json`.
Adding a star means adding one entry there, then re-running the pipeline.

```
db/target_list.json
       │
       ├─ fetch_astrometry.py    → db/astrometry_raw.json
       ├─ fetch_photometry.py    → db/photometry_raw.json
       ├─ fetch_stellar_props.py → db/stellar_props_raw.json
       └─ fetch_planets.py       → db/planets_raw.json
                    │
               build_systems.py  → db/systems/<name>.json
                    │
              build_site.py      → docs/data.json
```

---

## Hostname convention

- One entry per **stellar component** that appears as a body in the mod.
- Multi-component systems share one entry with multiple components:
  `"Alpha Centauri A"`, `"Alpha Centauri B"` → single entry, `binary: true`.
- Single stars: `"Vega"`, `"Altair"`.
- `to_filename()` in `build_systems.py` converts name → filename:
  lowercase, apostrophes stripped, non-alphanumeric → `_`, trim edges.
  Example: `"Chi-1 Orionis A"` → `chi_1_orionis_a.json`.

---

## Step 1 — Add to `db/target_list.json`

Append an entry at the end of the array:

```json
{
  "system": "New Star",
  "components": ["New Star"],
  "gaia_source_ids": ["1234567890123456789"],
  "hip_ids": [],
  "binary": false
}
```

Fields:

| Field | How to get it |
|---|---|
| `system` | Canonical system name (same as hostname for single stars) |
| `components` | List of component hostnames in the system |
| `gaia_source_ids` | Gaia DR3 `source_id` — look up at [Gaia Archive](https://gea.esac.esa.int/archive/) or SIMBAD. One ID per component, same order as `components`. Use `null` if unavailable. |
| `hip_ids` | Hipparcos ID if known — optional, not used by pipeline |
| `binary` | `true` if this system has a mutual orbit in `db/binary_orbits.json` |
| `stellarium_ids` | _Auto-populated_ by `fetch_stellarium_ids.py`. `{component_name → Stellarium Web skysource_id}`. Don't edit manually. |

For binary systems, list both (or all) components:

```json
{
  "system": "New Binary",
  "components": ["New Binary A", "New Binary B"],
  "gaia_source_ids": ["111...", "222..."],
  "hip_ids": [12345, 12346],
  "binary": true
}
```

---

## Step 2 — Add stellar properties to `db/stellar_props_curated.json`

`fetch_stellar_props.py` auto-fetches spectype, Teff, and interferometric radii
from SIMBAD into `stellar_props_raw.json` (overwritten on each run).
Mass measurements and precise literature radii must be added manually to
`stellar_props_curated.json` — these take priority over the raw values in
`build_systems.py`.

Add an entry keyed by the component hostname:

```json
"New Star": {
  "teff_k": 5500,        ← optional; omit to use SIMBAD value
  "spectype": "G5 V",    ← optional; omit to use SIMBAD value
  "mass_measurements": [
    {
      "value_msun": 0.92,
      "uncertainty_msun": 0.03,
      "method": "spectroscopic",
      "reference": "Author et al. (2020)",
      "bibcode": "2020ApJ...000..000A",
      "doi": "10.xxxx/...",
      "recommended": true
    }
  ],
  "radius_measurements": [
    {
      "value_rsun": 0.88,
      "uncertainty_rsun": 0.02,
      "method": "interferometry",
      "reference": "Author et al. (2020)",
      "bibcode": "2020ApJ...000..000A",
      "doi": "10.xxxx/...",
      "recommended": true
    }
  ]
}
```

At minimum, set `recommended: true` on one mass and one radius measurement —
these are used to compute the `principia.gravitational_parameter_km3_s2` and
`principia.mean_radius_km` fields in the output JSON.

---

## Step 3 — Handle vmag_v if Gaia is unavailable

`fetch_photometry.py` computes V magnitude from Gaia G + BP-RP automatically.
If the star has no Gaia ID (e.g. brown dwarf, Gaia-saturated bright star),
add the V magnitude to `HIPPARCOS_V` in `fetch_photometry.py`:

```python
HIPPARCOS_V = {
    ...
    "New Star": 5.23,  # source: Hipparcos HIP 12345
}
```

If no optical V magnitude exists (infrared-only objects like Y dwarfs),
leave it out — `vmag_v: null` in the output is acceptable.

---

## Step 4 — Handle binary orbits (if applicable)

If the new system is a gravitationally bound pair, add its mutual orbit
to `db/binary_orbits.json` and set `binary: true` in `db/target_list.json`.

See existing entries (e.g. Alpha Centauri, Sirius) for the schema.
There is no automated fetch — `binary_orbits.json` is maintained manually
since published orbital solutions vary widely in form (visual orbit
elements, ephemeris files, RV fits) and require case-by-case curation.
`build_systems.py` embeds the relevant entry into the representative
component file automatically.

---

## Step 5 — Re-run the pipeline

```bash
cd /path/to/project
python3 scripts/pipeline/fetch_astrometry.py
python3 scripts/pipeline/fetch_photometry.py
python3 scripts/pipeline/fetch_stellar_props.py
python3 scripts/pipeline/fetch_planets.py
python3 scripts/pipeline/fetch_stellarium_ids.py
python3 scripts/pipeline/build_systems.py
python3 scripts/pipeline/validate.py
python3 scripts/pipeline/build_site.py
```

Or use the convenience script:

```bash
./run_pipeline.sh
```

The five fetch scripts (steps 1–5 in the block above) are independent and can run in any order or in parallel.

---

## Verification

After `build_systems.py`:
- Check that `db/systems/<new_name>.json` was created.
- Inspect `stars[0].raw` for astrometry, `stars[0].principia` for mass/radius.

After `validate.py`:
- Should show 0 FAIL. WARN for missing vmag_v is acceptable for non-Gaia stars.

After `build_site.py`:
- Open `docs/index.html` in a browser and search for the new star.

---

## Known exceptions

| Star | Issue |
|---|---|
| WISEP J121756.91+162640.2 A | SIMBAD name mismatch — actual SIMBAD ID is `WISE J121756.90+162640.8`. Astrometry fetch fails; file was manually patched. |
| CWISEP J193518.59-154620.3 | Y dwarf — no Gaia ID, no optical V mag. principia radius missing (expected). |
| GJ 273, GJ 411, HD 62509 | No Gaia ID — V magnitudes hardcoded in `HIPPARCOS_V`. |

---

## Pipeline scripts

| Script | Role |
|---|---|
| `fetch_astrometry.py` | Gaia DR3 TAP batch query + SIMBAD fallback for bright saturated stars |
| `fetch_photometry.py` | Gaia G+BP-RP → V mag conversion; bright stars use hardcoded Hipparcos V |
| `fetch_stellar_props.py` | SIMBAD: spectype, Teff, mesDiameter → R☉; mass from `stellar_props_curated.json` |
| `fetch_planets.py` | NASA Exoplanet Archive TAP → planet orbits and physical properties |
| `fetch_stellarium_ids.py` | Stellarium Web API → per-component skysource ID lookup (idempotent; skips populated entries) |
| `build_systems.py` | Merges all raw + curated files → B1950 + J2000 epoch propagation → systems/*.json |
| `validate.py` | Checks required fields, epoch consistency, vmag_v presence |
| `build_site.py` | systems/*.json → docs/data.json |

## External APIs

| API | Endpoint | Used for |
|---|---|---|
| Gaia DR3 TAP | gea.esac.esa.int/tap-server | Astrometry, photometry |
| SIMBAD TAP | simbad.u-strasbg.fr/simbad/sim-tap | Bright-star fallback, mesDiameter, spectype, Teff |
| NASA Exoplanet Archive | exoplanetarchive.ipac.caltech.edu/TAP | Planet data |
| VizieR WDS TAP | tapvizier.cds.unistra.fr | Binary cross-validation (binary_orbits only) |
