# NearStars

A data pipeline and database for adding real nearby star systems to **Kerbal Space Program 1.12.x**, grounded in actual astronomical measurements.

This repository is the **data engine** of the mod. It fetches observational data from public astronomical catalogs, assembles it into structured per-system JSON files, and validates them for downstream consumption by Kopernicus and Principia config writers.

---

## What it does

- Pulls astrometry, photometry, stellar properties, and exoplanet data from live catalogs (Gaia DR3, SIMBAD, NASA Exoplanet Archive, ORB6)
- Computes SSB-ICRF Cartesian positions and velocities in km / km·s⁻¹ for every star
- Handles binary and multiple star systems — resolves barycentric positions via mass-weighted averaging and Keplerian orbital propagation
- Generates Kopernicus and Principia-ready data (~50 ly and ~80 ly range respectively)
- Validates the entire database against a strict schema before any build step completes
- Publishes a static HTML viewer of the full database (`docs/`)

---

## Repository layout

```
db/
  target_list.json          # master list of 142 target systems
  astrometry_raw.json       # fetched: RA, Dec, parallax, proper motion, RV
  photometry_raw.json       # fetched: V-mag, Gaia G, BP-RP
  stellar_props_raw.json    # fetched: Teff, spectral type, mass, radius measurements
  planets_raw.json          # fetched: exoplanet orbital + physical parameters
  planets_ps_default.json   # NASA Planetary Systems default values (pre-curate)
  binary_orbits.json        # hand-curated Keplerian orbital elements (ORB6-based)
  stellar_props_curated.json # manual overrides for mass/radius/spectype
  planets_curated.json      # manual overrides for planet data
  systems/                  # assembled per-component output (152 files)
    alpha_centauri_a.json
    alpha_centauri_b.json
    sirius_a.json
    ...

scripts/pipeline/
  fetch_astrometry.py       # Gaia DR3 TAP batch → SIMBAD fallback
  fetch_photometry.py       # Gaia G/BP-RP + Hipparcos V-mag
  fetch_stellar_props.py    # Teff, spectype, mass, radius from SIMBAD
  fetch_planets.py          # NASA Exoplanet Archive TAP
  fetch_planets_ps.py       # Planetary Systems default-param table
  fetch_stellarium_ids.py   # Stellarium Web skysource ID lookup
  build_systems.py          # assembles raw + curated → db/systems/*.json
  build_curated_from_ps.py  # seeds planets_curated from PS defaults
  build_site.py             # generates docs/data.json + docs/index.html
  generate_target_list.py   # utility: rebuild target_list from systems/
  validate.py               # schema validation (exits non-zero on failure)
  schema.py                 # shared schema definitions and validators

docs/
  index.html                # static DB viewer (dark theme, filterable)
  data.json                 # viewer data source

run_pipeline.sh             # one-shot full pipeline runner
```

---

## Pipeline

Run the full pipeline with:

```bash
./run_pipeline.sh
```

Stages run in order:

| # | Script | What it does |
|---|--------|--------------|
| 1 | `fetch_astrometry.py` | Queries Gaia DR3 TAP for all `gaia_source_id`s in `target_list.json`; falls back to SIMBAD TAP for any misses |
| 2 | `fetch_photometry.py` | Retrieves V-mag (Hipparcos/hardcoded) and Gaia G, BP-RP |
| 3 | `fetch_stellar_props.py` | Retrieves Teff, spectral type, and all available mass/radius measurements |
| 4 | `fetch_planets.py` | Queries NASA Exoplanet Archive for confirmed planets around each target |
| 5 | `fetch_stellarium_ids.py` | Maps each component to a Stellarium Web skysource ID (idempotent; skips already-mapped entries) |
| 6 | `build_systems.py` | Merges raw + curated data, propagates epochs, computes ICRF positions, resolves binaries |
| 7 | `validate.py` + `build_site.py` | Schema-validates `db/systems/`, then regenerates the static viewer |

All fetch scripts are **idempotent** — they only query missing or null entries on re-run, so incrementally adding new stars is safe.

---

## Data layers

Each file in `db/systems/` has three layers:

### `raw`
Source values as retrieved from catalogs, with provenance attached. Includes:
- Astrometry: RA, Dec, parallax, proper motion (pmra, pmdec), radial velocity, epoch
- Photometry: V-mag, Gaia G, BP-RP
- Stellar properties: Teff, spectral type, all available mass and radius measurements with method labels (`interferometry`, `binary_orbit`, `eclipsing_binary`, `asteroseismology`, etc.) and `recommended` flags
- Planet data: orbital elements, masses, radii (when available)

### `derived`
Computed from `raw`. Never assumes values — if source data is null, derived values stay null.
- ICRF Cartesian position and velocity at B1950 and J2000 epochs (SSB origin, km / km·s⁻¹)
- Distance in pc and km
- For binary components: barycentric offset, orbit role (primary/secondary), mass ratio
- Epoch propagation method: `kepler_thiele_innes` for binaries, standard ICRF kinematics for singles

### `principia`
KSP Principia-ready values:
- Gravitational parameter μ = GM (km³·s⁻²), computed from recommended mass
- Mean radius (km), computed from recommended radius

---

## Binary and multiple system handling

Binary/multiple systems require special treatment because catalog astrometry is typically center-of-light, not barycentric.

For each system in `db/binary_orbits.json`:
- Keplerian orbital elements are stored (period, epoch of periastron, eccentricity, semi-major axis, inclination, ω, Ω) sourced from ORB6 / published solutions
- `build_systems.py` propagates the orbit to the game epoch using the **Kepler + Thiele-Innes** method to compute the true anomaly, then converts to Cartesian separation vectors
- Each component's position is separated from the barycenter using the mass ratio q = M_B / (M_A + M_B)
- The barycenter position itself is computed as a mass-weighted average of component catalog positions

Currently tracked binary/multiple systems (8 systems, 16 components):

| System | Type | Source |
|--------|------|--------|
| Alpha Centauri AB | Binary | Pourbaix & Correia 2017 |
| Sirius AB | Binary | ORB6 |
| 61 Cygni AB | Binary | ORB6 |
| 40 Eridani ABC | Hierarchical triple | ORB6 |
| Eta Cassiopeiae AB | Binary | ORB6 |
| 36 Ophiuchi ABC | Hierarchical triple | ORB6 |
| + 2 more | Binary | ORB6 |

---

## Planet curation

Planet data goes through two phases:

**Phase 1 (default)** — NASA Exoplanet Archive best-available values. Orbital elements are used as-is for basic Kopernicus placement. Most stars are at this level.

**Phase 2 (precision curated)** — Manual override via `planets_curated.json`, adding precise orbital elements with full provenance (DOI, bibcode). Used when the system will be implemented in-game with Principia n-body physics. Each `orbital` and `physical` block in curated data requires at least one provenance field (`source`, `bibcode`, or `doi`).

---

## Schema validation

`scripts/pipeline/schema.py` defines required and optional keys for every data layer. `validate.py` runs all checks at the end of the pipeline and exits non-zero on any failure.

Validated layers:
- `astrometry_raw.json` — required astrometry fields, epoch format
- `photometry_raw.json` — vmag_v required, source required
- `stellar_props_raw.json` — mass/radius measurement structure, `value_*` prefix enforced, `error_*` prefix forbidden (must use `uncertainty_*`)
- `binary_orbits.json` — orbit elements, component cross-references, barycenter block requirements
- `stellar_props_curated.json` — method whitelist, single `recommended: true` per measurement type
- `planets_curated.json` — provenance required on every orbital/physical block

---

## Downstream usage

This repo produces data; it does not write KSP config files directly.

**Kopernicus** (~50 ly range): reads `db/systems/*.json` to generate `.cfg` files that add stars and planets to the KSP solar system. Uses the `derived.icrs_*` coordinates and `principia.*` values.

**Principia** (~80 ly range): reads the same JSON files to generate n-body initial condition blocks in B1950 ICRF. Requires `derived.icrs_x_km`, `derived.icrs_vx_km_s`, and `principia.gravitational_parameter_km3_s2`.

The downstream cfg writers apply their own distance cutoffs independently of this pipeline.

---

## Requirements

- Python 3.10+
- [`PyAstronomy`](https://github.com/sczesla/PyAstronomy) — Markley Kepler equation solver

```bash
pip install PyAstronomy
```

No other external dependencies. All catalog queries use standard `urllib` over TAP/HTTP.

---

## Data sources

| Source | Used for |
|--------|----------|
| [Gaia DR3](https://www.cosmos.esa.int/web/gaia/data-release-3) | Primary astrometry (RA, Dec, parallax, PM, RV) |
| [SIMBAD](https://simbad.u-strasbg.fr/) | Fallback astrometry, Teff, spectral type, mass/radius literature values |
| [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/) | Confirmed planet parameters |
| [ORB6 / WDS](https://www.astro.gsu.edu/wds/orb6.html) | Binary/multiple system orbital elements |
| [Stellarium Web](https://stellarium-web.org/) | Sky-source IDs for in-game skybox integration |
| Published papers | System-specific curated values (cited inline per measurement) |

---

## License

MIT — see [LICENSE](LICENSE).

Third-party data attributions: see [NOTICE](NOTICE).
