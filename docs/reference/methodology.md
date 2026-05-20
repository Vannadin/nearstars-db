# Stellar System Data Research Methodology

This document defines the workflow for building a structured JSON database of
stellar and planetary data, sourced from public astronomical catalogues.
The database feeds two downstream consumers: Principia proto files and
Kopernicus cfg files, written in separate sessions or agents.

---

## Goal

One JSON file per star system. Each file contains:
- Raw observational values, exactly as received from the source catalogue
- Derived/converted values ready for Principia and Kopernicus
- Full provenance: source name, catalogue ID, retrieval date, epoch

The database is the single source of truth. No downstream agent should need
to query an external catalogue or perform unit conversions independently.

---

## Output Structure

```
db/
  target_list.json            # 파이프라인 입력
  astrometry_raw.json         # 자동 fetch — Gaia DR3 + SIMBAD
  photometry_raw.json         # 자동 fetch — Gaia DR3
  stellar_props_raw.json      # 자동 fetch — SIMBAD (Teff, 스펙형, mesDiameter)
  stellar_props_curated.json  # 수동 입력 — 질량/반지름 정밀 문헌값
  planets_raw.json            # 자동 fetch — NASA Exoplanet Archive
  planets_curated.json        # 수동 입력 — 궤도/환경/대기 상세 문헌값
  binary_orbits.json          # 수동 입력 — 쌍성 궤도
  systems/
    alpha_centauri_a.json
    barnards_star.json
    tau_cet.json
    ...                       # 항성 컴포넌트별 1파일
  backups/                    # 이전 스냅샷 보관 (수동 백업 시점)
```

파이프라인 실행 순서, 스크립트 설명, 새 별 추가 절차는 [`adding_stars.md`](adding_stars.md) 참조.

---

## JSON Schema

### Top-level

```json
{
  "system_name": "Alpha Centauri A",
  "stars": [ ... ],
  "planets": [ ... ],
  "sources": [ ... ],
  "meta": { ... }
}
```

One JSON file per **stellar component**, not per system. `system_name`
matches the component name (e.g. `Alpha Centauri A`, `Alpha Centauri B`,
`Proxima Centauri` are three separate files). The `stars` array always
holds exactly one entry — the component the file describes. Mutual
orbit data for binary/multiple systems lives in `binary_orbits.json`
and is embedded into the representative component file (typically `A`);
sibling components reference it via `binary_orbit_ref`.

This choice reflects how downstream Kopernicus/Principia cfg writers
consume the data: each `CelestialBody` (a single star) maps 1:1 to a
cfg `Body { }` node, so a one-component-per-file layout removes any
indexing during cfg generation.

### `meta`

```json
{
  "retrieval_date": "2026-05-16",
  "solar_system_epoch_jd": 2433282.5,
  "solar_system_epoch_label": "B1950.0",
  "game_epoch_jd_sol": 2433647.5,
  "game_epoch_jd_rss": 2433647.5,
  "coordinate_origin": "SSB",
  "coordinate_frame": "ICRF",
  "coordinate_units": "km, km/s",
  "notes": ""
}
```

`solar_system_epoch_jd` is the epoch at which all state vectors are expressed.
Both Sol and RSS use **JD2433282.5** (nominally B1950.0, 1950-01-01 TDB) as the
`solar_system_epoch`. This is the value to match when querying JPL Horizons.

Note: strictly, Besselian epoch B1950.0 = JD2433282.423. JD2433282.5 is
1950-01-01.0 TT midnight, differing by ~1.85 hours. Both Sol and RSS use
2433282.5 by convention, and JPL Horizons accepts this date directly.
The difference is negligible for KSP purposes but worth knowing if
cross-checking against software that computes B1950.0 precisely.

`game_epoch_jd` does not affect the state vectors. Sol and RSS share the same value:
- Sol: `JD2433647.5`
- RSS: `JD2433647.5`

The coordinate origin is the **Solar System Barycentre (SSB)**, not the Sun.
The Sun itself has a non-zero position in these files (on the order of 10⁵ km
from the SSB). All state vectors must be expressed in this same SSB-ICRF frame.

---

### `stars[]`

The `stars` array always has length 1 — the single component this file
describes. (Binary/multiple systems use one file per component; see
"Top-level" above.)

```json
{
  "name": "Alpha Centauri A",
  "component": "A",

  "raw": {
    "source": "Gaia DR3",
    "source_id": "5853498713160606720",
    "epoch_jd": 2457389.0,
    "epoch_label": "J2016.0",
    "ra_deg": 219.90085,
    "dec_deg": -60.83562,
    "parallax_mas": 742.12,
    "parallax_error_mas": 1.40,
    "pmra_mas_yr": -3678.19,
    "pmdec_mas_yr": 481.84,
    "radial_velocity_km_s": -22.4,
    "radial_velocity_source": "Gaia DR3",

    "vmag_v": -0.01,
    "vmag_source": "hipparcos_hardcoded",

    "teff_k": 5790,
    "spectype": "G2 V",

    "mass_measurements": [
      {
        "value_msun": 1.1055,
        "uncertainty_msun": 0.0039,
        "method": "binary_orbit",
        "reference": "Pourbaix et al. 2002",
        "doi": "10.1051/0004-6361:20021249",
        "recommended": true
      },
      {
        "value_msun": 1.100,
        "uncertainty_msun": 0.006,
        "method": "evolutionary_model",
        "reference": "Thevenin et al. 2002",
        "doi": "10.1051/0004-6361:20021791",
        "recommended": false
      }
    ],

    "radius_measurements": [
      {
        "value_rsun": 1.2234,
        "uncertainty_rsun": 0.0053,
        "method": "interferometry",
        "reference": "Kervella et al. 2017",
        "doi": "10.1051/0004-6361/201629505",
        "recommended": true
      },
      {
        "value_rsun": 1.227,
        "uncertainty_rsun": 0.005,
        "method": "evolutionary_model",
        "reference": "Thevenin et al. 2002",
        "doi": "10.1051/0004-6361:20021791",
        "recommended": false
      }
    ]
  },

  "derived": {
    "epoch_jd": 2433282.5,
    "epoch_label": "B1950.0",
    "propagation_method": "linear",
    "distance_pc": 1.3475,
    "distance_km": 4.153e+13,
    "icrs_x_km":  2.634e+13,
    "icrs_y_km": -3.197e+13,
    "icrs_z_km": -1.272e+13,
    "icrs_vx_km_s": 1.3204,
    "icrs_vy_km_s": -4.4012,
    "icrs_vz_km_s":  0.8913,
    "position_ulp_km": 5.9e-3,
    "icrs_x_j2000_km":  2.557e+13,
    "icrs_y_j2000_km": -3.127e+13,
    "icrs_z_j2000_km": -1.255e+13,
    "icrs_vx_j2000_km_s": 1.3204,
    "icrs_vy_j2000_km_s": -4.4012,
    "icrs_vz_j2000_km_s":  0.8913
  },

  "principia": {
    "gravitational_parameter_km3_s2": 146713602439.899,
    "mean_radius_km": 851119.4
  }
}
```

Notes on `derived`:
- All units follow Principia/Sol convention: **km** and **km/s**.
- `propagation_method: "linear"` means positions were propagated using
  constant space velocity (proper motion + radial velocity). Adequate for
  stellar perturbers over KSP timescales (decades to centuries).
- `position_ulp_km` is `abs(largest_coordinate_km) * 2^-52`. For Alpha
  Centauri (~4e13 km), this is ~0.009 km (9 m) -- acceptable for a
  gravitational perturber, not for close-range orbital mechanics around
  the star.
- The coordinate origin is the **SSB**, not the Sun. The Sun itself sits
  ~10⁵ km from the SSB in these files.

Notes on `mass_measurements` and `radius_measurements`:
- Every available published value goes in the array, regardless of how many.
- `recommended: true` marks the value used in the `principia` block.
  Exactly one entry per array must have `recommended: true`.
- Priority for `recommended` is determined by measurement method, not
  publication date or journal prestige. Method hierarchy:

  Mass:
  1. `binary_orbit` -- direct dynamical measurement, most reliable
  2. `asteroseismology` -- model-dependent but well-constrained
  3. `evolutionary_model` -- indirect; use only when nothing better exists
  4. `spectroscopic` / `spectroscopic_calibration` -- spectral fitting based
  99. `unverified` -- Curation Phase 1 batch에서 method 검증 안 함; 항상 최하위로 처리. 출처(bibcode)는 정확하나 paper가 실제 어떤 방법을 썼는지는 미검증.

  Radius:
  1. `interferometry` -- direct angular diameter measurement
  2. `eclipsing_binary` -- direct geometric measurement
  3. `sed_fitting` -- bolometric flux + Teff + distance (semi-direct)
  4. `evolutionary_model` -- indirect; use only when nothing better exists
  99. `unverified` -- Curation Phase 1 batch 동일 의미.

  The full whitelist of permitted method labels lives in
  `scripts/pipeline/schema.py STELLAR_ALLOWED_METHODS`; the hierarchy
  above only ranks the ones used in practice. Any new method must be
  added to both places.

- If two entries share the same method tier, prefer the one with smaller
  fractional uncertainty. Document the choice in `meta.notes`.

---

### `planets[]`

Each confirmed planet is a separate entry.

```json
{
  "name": "Proxima Centauri b",
  "host_star": "Proxima Centauri",

  "raw": {
    "pl_name": "Proxima Cen b",
    "reference": "Anglada-Escude et al. 2016",
    "retrieval_date": "2026-05-16",
    "period_days": 11.1868,
    "period_err_days": 0.0002,
    "semi_major_axis_au": 0.04856,
    "semi_major_axis_err_au": 0.00030,
    "eccentricity": 0.0,
    "inclination_deg": null,
    "inclination_err_deg": null,
    "omega_deg": null,
    "tperi_bjd": null,
    "tperi_err_bjd": null,
    "tranmid_bjd": null,
    "tranmid_err_bjd": null,
    "mass_mearth": 1.27,
    "mass_err_mearth": 0.18,
    "mass_type": "Msini",
    "radius_rearth": null,
    "radius_err_rearth": null,
    "discoverymethod": "Radial Velocity",
    "pl_controv_flag": 0,
    "pubdate": "2016-08",
    "tepcat": null
  },

  "derived": {
    "semi_major_axis_m": 7.265e+09,
    "eccentricity": 0.0,
    "inclination_deg": null,
    "longitude_of_ascending_node_deg": null,
    "argument_of_periapsis_deg": null,
    "mean_anomaly_at_epoch_deg": null,
    "orbital_epoch_jd": null,
    "mass_kg": 7.548e+24,
    "mass_type": "minimum (M sin i)",
    "radius_m": null
  }
}
```

The `raw` block mirrors `fetch_planets.py` output one-for-one:
- Orbital fields use NASA Exoplanet Archive's `pscomppars` column names
  (`tperi_bjd`, `tranmid_bjd`, `omega_deg`, etc.). Periastron passage time
  (`tperi_bjd`) and transit midpoint (`tranmid_bjd`) are both stored; the
  one to use as the mean-anomaly reference depends on detection method.
- `tepcat` is a nested object populated when TEPCat has independently
  derived mass/radius for a transiting planet. May be `null`.

The `derived` block is unit conversion only (AU → m, M⊕ → kg, R⊕ → m)
with a priority chain `curated > tepcat > nasa_archive`. Missing
measurements remain `null` — default-value assumptions (edge-on
inclination, circular eccentricity, mean anomaly at game start) belong
in the Kopernicus cfg generation stage, not in the DB. Downstream agents
writing the cfg are responsible for choosing and documenting these
defaults.

### `sources[]`

All papers and catalogues consulted during research go here. This is the
complete bibliography for the file.

```json
[
  {
    "title": "Constraining the difference in convective blueshift between the components of alpha Centauri with precise radial velocities",
    "doi": "10.1051/0004-6361:20021249",
    "bibcode": "2002A&A...394..151P",
    "accessed": "2026-05-16",
    "used_for": ["Alpha Centauri A mass", "Alpha Centauri B mass"]
  },
  {
    "title": "Gaia Data Release 3",
    "doi": null,
    "bibcode": "2023A&A...674A...1G",
    "accessed": "2026-05-16",
    "used_for": ["Alpha Centauri A astrometry", "Alpha Centauri B astrometry"]
  }
]
```

- `doi` and `bibcode`: provide both when available. If one is absent, set it to `null`.
- `used_for`: note what was taken from the source. Consulted-but-unused entries
  are fine -- write `"used_for": ["consulted; superseded by Pourbaix et al. 2002"]`.

---

Notes on `null` fields:
- Null means data is missing, not zero. The DB never substitutes a default
  for a missing measurement — that is the Kopernicus cfg writer's job.
- Downstream agents must check for nulls and document any assumed default
  (e.g. `inclination = 90 deg` for RV-only detections) in the cfg itself.

---

## Epoch Handling

### Target epoch

Both Sol and RSS use **JD2433282.5** (B1950.0, 1950-01-01 TDB) as the
`solar_system_epoch`. All state vectors in `derived` must be expressed at
this epoch in SSB-ICRF coordinates.

The `game_epoch` is separate and does not affect state vectors. Sol and RSS share the same value:
- Sol: `JD2433647.5`
- RSS: `JD2433647.5`

When writing MM patches, Sol and RSS variants only differ by NEEDS tag
(`SolSystem` vs `RSSConfig`), not by epoch values.

### Why propagation is needed

Gaia DR3 positions are referenced to **J2016.0** (JD2457389.0).
The target epoch is JD2433282.5. The delta is ~24,000 days (~66 years).

For Alpha Centauri (space velocity ~25 km/s), the positional shift over
66 years is ~5.2e10 km (~350 AU). Propagation is always required.

### Linear propagation

Constant-velocity (uniform rectilinear) propagation in SSB-ICRF is the
standard model used by Gaia and Hipparcos. It is sufficient for stellar
perturbers over KSP-relevant timescales.

The dominant higher-order effect omitted by linear propagation is
**perspective acceleration** — the apparent change in proper motion rate
as a star's distance changes. For most target stars this is negligible
at the perturber accuracy level.

**Edge case: Barnard's Star** (μ ≈ 10,300 mas/yr, ϖ ≈ 548 mas,
RV ≈ −110 km/s) accumulates ~0.5 AU of position error over 66 years
from perspective acceleration alone. This is still within the
perturber-accuracy tolerance for KSP gravitational effects, so the
pipeline applies linear propagation like every other star. The known
discrepancy is recorded in `meta.notes` for the `barnards_star.json`
file. If future requirements demand sub-AU accuracy for Barnard's Star,
fetch a JPL Horizons state vector at JD2433282.5 and override the
`derived` block manually.

References:
- Butkevich & Lindegren (2014), A&A 570, A62 — `doi:10.1051/0004-6361/201424483`, `arXiv:1407.4664`
  Canonical paper for epoch propagation in the Gaia era. Derives rigorous
  closed-form expressions for uniform rectilinear motion; used directly
  in the Gaia pipeline.
- ESA SP-1200 (1997), Vol. 1, Sec. 1.2 (Hipparcos Catalogue, Lindegren et al.)
  Explicitly states that uniform space motion is valid for most stars
  over timescales under a century, even at Hipparcos precision.

```python
def propagate_icrs(x0, y0, z0, vx, vy, vz, jd_from, jd_to):
    """
    Linear propagation from jd_from to jd_to.
    Units: km and km/s (matching Principia/Sol convention).
    See Butkevich & Lindegren (2014) Eq. 4-7 for the full derivation.
    """
    dt_s = (jd_to - jd_from) * 86400.0
    return (
        x0 + vx * dt_s,
        y0 + vy * dt_s,
        z0 + vz * dt_s
    )
```

### `propagation_method` values

| Value | Meaning | Source epoch |
|---|---|---|
| `"linear"` (Gaia) | Gaia DR3 → constant space velocity → target epoch | J2016.0 (JD2457389.0) |
| `"linear"` (SIMBAD) | SIMBAD fallback for Gaia-saturated bright stars → linear propagation | J2000.0 (JD2451545.0) |
| `"kepler_thiele_innes"` | Orbit-bound binary/multiple component → Markley Kepler + Thiele-Innes rotation (Hilditch convention) → ICRS Cartesian | Catalog epoch of the orbit fit, propagated to target epoch via `build_systems.py:solve_orbit_relative` |
| `"horizons_direct"` | JPL Horizons state vectors imported directly at JD2433282.5 — bypasses any propagation | JD2433282.5 (target epoch) |

The SIMBAD fallback path applies to stars without a Gaia DR3 ID — typically
bright stars saturated in Gaia (V < ~6) such as Alpha Centauri A and B,
Sirius, Procyon, Pollux. `fetch_astrometry.py` queries SIMBAD's `basic`
table, whose astrometry is referenced to J2000.0 (~16 years earlier than
Gaia's J2016.0). The `raw.epoch_jd` field records the actual source epoch,
so `build_systems.py` propagates correctly regardless of source.

Currently `"horizons_direct"` applies only to Barnard's Star. Any future
star available in Horizons should be evaluated for the same treatment.

### Epoch fields summary

| Field | Location | Content |
|---|---|---|
| `raw.epoch_jd` | star | Source epoch — J2016.0 for Gaia, J2000.0 for SIMBAD fallback |
| `derived.epoch_jd` | star | Target epoch (JD2433282.5) |
| `meta.solar_system_epoch_jd` | system | JD2433282.5 (same for Sol and RSS) |
| `meta.game_epoch_jd_sol` | system | JD2433647.5 |
| `meta.game_epoch_jd_rss` | system | JD2433647.5 |
| `raw.tperi_bjd` / `raw.tranmid_bjd` | planet | Archive reference epoch (periastron or transit midpoint) |
| `derived.orbital_epoch_jd` | planet | Epoch from curated source if available; else null |

---

## Multiple-System Epoch

> Full mathematical pipeline + worked examples (α Cen, Sirius):
> [`docs/reference/binary-epoch-pipeline.md`](binary-epoch-pipeline.md).
> This section captures only the decisions and schema that affect the DB.

### Why linear back-propagation fails for multi-star systems

For single stars, linear extrapolation of Gaia/SIMBAD astrometry to JD2433282.5
is sufficient (see "Linear propagation" above). For multi-star systems it is
**wrong**, because the components are in mutual orbit — their relative position
rotates, not translates.

Example: Alpha Centauri AB has orbital period 79.762 yr. JD2433282.5 is ~66 yr
before Gaia's J2016 epoch — almost a full orbit. Linear propagation rotates
the A–B vector by 0°, while the real geometry has rotated by ~300°. The
resulting cfg has wrong gravitational geometry, which causes Principia's
N-body integrator to start with spurious eccentricity and energy.

The fix: each multi-star system stores a fitted Kepler solution; at build time
we propagate the components' shared **barycenter** linearly, then apply the
Kepler-derived (B−A) offset evaluated at JD2433282.5 to place individual
components.

### Pipeline outline

```
barycenter_astrometry  → linear propagation (J2016 / J2000 → JD2433282.5)
                          → R_bary, V_bary at target epoch
                                  +
orbits[].(P,T,e,a,i,ω,Ω)  → Kepler solver (M → E → ν)
                          → Thiele-Innes rotation → (B−A) in ICRS (N,E,W)
                                  +
mass ratio q             → r_A = R_bary − q_B · r_AB
                          → r_B = R_bary + q_A · r_AB
```

For triples, the same pipeline runs in nested form (inner orbit on AB, outer
orbit on (AB)–C). See binary-epoch-pipeline.md §6.

### `binary_orbits.json` schema (new)

The legacy schema embedded a single `raw` block with Kepler elements per
system. The new schema separates **per-component** facts (mass, astrometry
source) from **per-orbit** facts (which two bodies it relates, the Kepler
elements, the source paper, grade, phase reliability) by exposing both as
arrays. Multiple orbits per system (triples) become natural.

```json
{
  "Alpha Centauri": {
    "system_id": "alpha_centauri",
    "hierarchy": "triple",
    "components": [
      {
        "name": "Alpha Centauri A",
        "mass_msun": 1.0788,
        "mass_source": "pourbaix_correia_2017",
        "astrometry_source": "mass_weighted_average",
        "astrometry_quality": "barycentric"
      },
      { "name": "Alpha Centauri B", "mass_msun": 0.9092, ... },
      { "name": "Proxima Cen",     "mass_msun": 0.1221, ... }
    ],
    "orbits": [
      {
        "orbit_id": "AB",
        "relates": ["Alpha Centauri A", "Alpha Centauri B"],
        "primary":   "Alpha Centauri A",
        "secondary": "Alpha Centauri B",
        "source":    "akeson_2021",
        "doi":       "10.3847/1538-3881/abfaff",
        "equinox":   "J2000",
        "P_yr":      79.762,
        "T_jd_tt":   2435291.6,
        "e":         0.51947,
        "a_arcsec":  17.4930,
        "i_deg":     79.2430,
        "omega_deg": 231.519,
        "Omega_deg": 205.073,
        "grade":           1,
        "node_resolved":   true,
        "phase_reliable":  true
      }
    ]
  }
}
```

Triple systems list two orbits and use `primary_is_barycenter_of` on the
outer one — see binary-epoch-pipeline.md §6 for the full triple example.

### Schema field reference

| Field | Required | Notes |
|---|---|---|
| `system_id` | yes | Slug used as filename stem. Lowercase, underscores. |
| `hierarchy` | yes | `"binary"`, `"triple"`, `"binary+cpm"` (CPM = common proper motion companion). |
| `components[].name` | yes | Must match `target_list.json` component names exactly. |
| `components[].mass_msun` | yes | With `mass_source` (paper bibcode or `gaia_dr3_nss`). |
| `components[].astrometry_source` | yes | One of `gaia_dr3` / `simbad` / `mass_weighted_average` / `gaia_dr3_nss_barycenter` / `hipparcos_barycenter` / `single_component:<Name>`. Drives where the build pulls the barycenter astrometry from — see "Hybrid storage" note below. |
| `components[].astrometry_quality` | yes | `barycentric` / `photocenter_contaminated` / `single_component`. Informational; validate.py uses it for warnings. |
| `barycenter_astrometry` (system-level) | conditional | Block with `ra_deg`/`dec_deg`/`parallax_mas`/`pm_ra_masyr`/`pm_dec_masyr`/`radial_velocity_km_s`/`epoch_jd`. **Required** when any `astrometry_source` is `gaia_dr3_nss_barycenter` or `hipparcos_barycenter` (the published catalog barycenter values that aren't derivable from component astrometry). Omitted otherwise — the build computes the barycenter on the fly from `astrometry_raw.json`. |
| `orbits[].orbit_id` | yes | `"AB"`, `"inner"`, `"outer"`. Unique within entry. |
| `orbits[].relates` | yes | Components or barycenters this orbit governs. |
| `orbits[].primary` / `secondary` | yes | One must be a component or `primary_is_barycenter_of`. |
| `orbits[].primary_is_barycenter_of` | conditional | For triples' outer orbit; list of component names forming the inner system. |
| `orbits[].source` | yes | `"akeson_2021"` (paper key) or `"orb6:grade=1"` or `"gaia_dr3_nss:OrbitalAlternative"`. |
| `orbits[].P_yr` / `T_jd_tt` / `e` | yes | Kepler core. `T` is time of periastron in JD (TT). |
| `orbits[].a_arcsec` or `a_au` | yes | Relative semi-major axis. Catalog convention is `arcsec`; convert via parallax. |
| `orbits[].i_deg`/`omega_deg`/`Omega_deg` | yes | Inclination, arg of periastron, longitude of ascending node. |
| `orbits[].A`/`B`/`F`/`G` (`C`/`H` optional) | optional | Thiele-Innes constants (in arcsec) if directly published (Gaia NSS). Substitutes for `a`/`i`/`omega`/`Omega`. |
| `orbits[].grade` | yes | Orb6 quality grade 1–9. ≤3 means publication-quality. |
| `orbits[].node_resolved` | yes | `true` if (i,ω,Ω) reflects the physically correct line of nodes (RV data available); `false` if catalog presents the mirror-degenerate solution. |
| `orbits[].phase_reliable` | yes | `false` if `grade ≥ 4` OR extrapolation > 0.5×P from observed coverage. When false, build still runs but `meta.notes` records the warning. |

#### `_principia_notes` meta block

`binary_orbits.json` has a top-level `_principia_notes` key (underscore
prefix, skipped by validators). It records the epoch constants used by
the build (`solar_system_epoch_jd`, `game_epoch_sol_jd`) plus a
`schema_version` string ("YYYY-MM-DD-components-orbits") that's bumped
whenever the component/orbit shape changes. Downstream tools (e.g.
`scripts/pipeline/build_systems.py`) can read it for sanity checks but
the values are not authoritative — they duplicate constants that live
in code.

#### Hybrid astrometry storage

The DB does not store derived/computed astrometry values per component.
Only published barycentric solutions (Gaia DR3 NSS, Hipparcos multi-star
annex) live in a system-level `barycenter_astrometry` block; the build
computes mass-weighted averages on the fly from `astrometry_raw.json`
when `astrometry_source = "mass_weighted_average"`. See
[[project-nearstars-db-principle]].

#### Thiele-Innes convention (Hilditch / Pourbaix)

`build_systems.py` applies the Hilditch / Pourbaix convention:

```
ΔN = A · x_p + F · y_p     (North)
ΔE = B · x_p + G · y_p     (East)
ΔW = C · x_p + H · y_p     (away from observer)
```

This convention is the canonical one across all NearStars docs and
code; `binary-epoch-pipeline.md` §2 step 5 and §10 worked example use
the same formulas. The form above reproduces the legacy
`individual_states.b1950` values for α Cen and Sirius within < 0.05 %.

### Barycenter astrometry decision tree (summary)

For each multi-star system, the `components[].astrometry_source` field is
selected by the following decision tree. The build refuses to run if any
component has `astrometry_source: "unset"`.

```
Gaia DR3 NSS row exists for this system?
├── YES → astrometry_source = gaia_dr3_nss_barycenter
│         astrometry_quality = barycentric
│
└── NO  → resolved pair (separation > ~1″, both have Gaia 5-param)?
          ├── YES → astrometry_source = mass_weighted_average
          │         astrometry_quality = barycentric
          │         (PM averaging cancels orbital tangent velocity)
          │
          └── NO  → Hipparcos multi-star annex (DMSA flag C/O/V/X)?
                    ├── YES → astrometry_source = hipparcos_barycenter
                    │         astrometry_quality = barycentric
                    │
                    └── NO  → astrometry_source = gaia_dr3 (or simbad if saturated)
                              astrometry_quality = photocenter_contaminated
                              (flag, allow but warn)
```

See binary-epoch-pipeline.md §8 for the photocenter-wobble error model.

### Per-system option assessment (best estimate; verify in implementation)

| System | Hierarchy | Recommended option | Source paper override |
|---|---|---|---|
| Alpha Centauri AB | binary | gaia_dr3_nss_barycenter | Akeson et al. 2021 |
| Sirius AB | binary | hipparcos_barycenter (A saturated; B is WD) | Bond et al. 2017 |
| 61 Cygni AB | binary | mass_weighted_average (wide, both in Gaia) | Malkov et al. 2012 — `phase_reliable: false` (P~679 yr, grade ≥3) |
| 40 Eridani ABC | triple | A: gaia_dr3 / B+C close pair: NSS or mass-weighted | needs research |
| Eta Cassiopeiae AB | binary | mass_weighted_average | Tokovinin 2021 — P=480 yr, `phase_reliable: false` likely |
| 36 Ophiuchi ABC | triple | A,B: mass-weighted on close pair / C: static CPM at fixed offset | needs research |

The actual `astrometry_source` value is locked in by the implementation
session — the table above is a starting point, not a commitment.

### Phase reliability semantics

Set `phase_reliable: false` when:
- Orb6 grade ≥ 4, OR
- Observed coverage is less than half the period (extrapolation > 0.5 P), OR
- Time of periastron error exceeds 5% of the period

When `phase_reliable: false`, the build still runs (output is the best estimate
from the available solution) but writes a warning to `meta.notes` of the affected
component files. Downstream Kopernicus cfg can still use the values; users
running long Principia simulations should not trust the relative geometry past
~0.5 P.

For phase-unreliable wide CPM companions (P > 1000 yr, no fitted orbit), use
`orbit_type: "static_cpm"` — see binary-epoch-pipeline.md §6 — which freezes
the relative position at the catalog reference epoch.

---

## Source Recording Protocol

Log every paper and catalogue consulted, even if its values were not used
(record why in `used_for`).

A SIMBAD bibcode is not a source. Resolve it to the original paper via
`https://ui.adsabs.harvard.edu/abs/<bibcode>` and record the DOI there.

If two papers at the same method tier conflict, add both to `sources[]` and
to the measurement array, and document the choice in `meta.notes`.

---

## Data Sources

All sources below are freely accessible. astroquery covers most of them
with a unified Python interface; raw TAP endpoints are listed for direct
access or fallback.

---

### Nearby Star Systems

**RECONS (Research Consortium on Nearby Stars)**
Authoritative list of all stellar systems within 10 parsecs (~32.6 ly).
Primary reference for confirming a star is within the project's 50 ly scope
and for catching newly measured distances that update a star's status.

- URL: `https://www.recons.org`
- Updated regularly as new parallaxes are measured
- Use when: verifying a candidate star is truly within 50 ly; finding
  newly discovered nearby systems not yet prominent in other databases

---

### Astrometry and Stellar Position

**Gaia DR3**
The primary source for position, proper motion, parallax, and radial
velocity of nearby stars.

- TAP endpoint: `https://gea.esac.esa.int/tap-server/tap`
- astroquery: `from astroquery.gaia import Gaia`
- Table: `gaiadr3.gaia_source`
- Key columns: `source_id`, `ra`, `dec`, `parallax`, `parallax_error`,
  `pmra`, `pmdec`, `radial_velocity`
- Epoch: J2016.0 (JD2457389.0)
- Caveat: `radial_velocity` is null for faint red dwarfs.

**Hipparcos**
Pre-Gaia catalogue. Superseded by Gaia DR3 for all nearby stars, but
useful as a cross-check or for stars missing from Gaia due to brightness
saturation (V < ~6 mag).

- Access via VizieR: catalogue `I/311`
- TAP endpoint: `https://tapvizier.cds.unistra.fr/TAPVizieR/tap`

**JPL Horizons**
Direct state vectors (position + velocity) in SSB-ICRF for solar system
bodies and some nearby stars. Outputs match Principia/Sol units (km, km/s)
and epoch (B1950.0 = JD2433282.5) directly.

- Web: `https://ssd.jpl.nasa.gov/horizons/`
- Batch API: `https://ssd.jpl.nasa.gov/horizons_batch.cgi`
- astroquery: `from astroquery.jplhorizons import Horizons`
- Settings: `VECTORS`, frame `ICRF`, center `@SSB`, epoch `1950-Jan-01`
- Coverage: Alpha Centauri, Barnard's Star confirmed available.
  Coverage of other target systems may vary.

---

### Stellar Physical Parameters (Mass, Radius, Teff)

**SIMBAD**
Literature aggregator. Does not store mass/radius as direct columns;
queries the `mesMass` and `mesDiameter` measurement tables via TAP.

- TAP endpoint: `https://simbad.u-strasbg.fr/simbad/sim-tap/sync`
- astroquery: `from astroquery.simbad import Simbad`
- Use for: mass, radius, spectral type, cross-IDs, RV fallback,
  bibcode → paper tracing

**VizieR**
Library of published astronomical catalogues. Hosts thousands of
stellar parameter tables from individual papers -- the most complete
aggregator of literature values.

- TAP endpoint: `https://tapvizier.cds.unistra.fr/TAPVizieR/tap`
- astroquery: `from astroquery.vizier import Vizier`
- Notable hosted catalogues relevant to this project:
  - `I/355` -- Gaia DR3
  - `I/311` -- Hipparcos
  - `B/pastel/pastel` -- PASTEL (see below)
  - `J/A+A/556/A150` -- SWEET-Cat (see below)
  - Individual interferometry papers (CHARA, VLTI/GRAVITY results)

**PASTEL**
Compilation of spectroscopically-derived stellar atmospheric parameters
(Teff, log g, [Fe/H]) from the literature. Useful for finding published
Teff values to cross-check evolutionary model mass estimates.

- URL: `https://pastel.obs.u-bordeaux1.fr/`
- Access via VizieR: `B/pastel/pastel`
- Note: does not directly provide mass or radius; provides the
  spectroscopic parameters used to derive them.

**SWEET-Cat**
Catalogue of atmospheric parameters and masses for planet host stars.
Covers most stars with confirmed planets; uniformly derived where possible.

- URL: `https://sweetcat.iastro.pt/`
- Access via VizieR: `J/A+A/556/A150`
- Provides: Teff, log g, [Fe/H], stellar mass
- Caveat: mass from calibration formulae, not direct measurement.
  Lower priority than binary orbit or interferometry values.

---

### Planetary Orbital Elements and Physical Parameters

#### Investigation Priority Order

When researching a planet system, check all sources below in order and
use the most precise value available. Do not stop at NASA Archive alone.

| Priority | Source | Best for |
|---|---|---|
| 1 | Individual paper (ADS) | Most recent / definitive orbital solution |
| 2 | DACE | RV orbital elements (T₀, ω, eccentricity detail) |
| 3 | TEPCat | Transiting systems — mass + radius from same fit |
| 4 | exoplanet.eu | Cross-check; catches recent discoveries before NASA Archive |
| 5 | NASA Exoplanet Archive | Baseline; used by pipeline auto-fetch |

Record all sources consulted, even if their values were not used.
For each planet, the `planets_curated.json` entry should reflect
the best available value with its source DOI.

---

**NASA Exoplanet Archive**
Most comprehensive planetary database with TAP support. Primary source
for orbital elements.

- TAP endpoint: `https://exoplanetarchive.ipac.caltech.edu/TAP/sync`
- astroquery: `from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive`
- Table: `ps` (Planetary Systems); filter `default_flag = 1`
- Table: `pscomppars` (composite best parameters per planet)
- Key columns: `pl_orbper`, `pl_orbsmax`, `pl_orbeccen`, `pl_orbincl`,
  `pl_orblper`, `pl_bmasse`, `pl_rade`, `pl_tranmid`, `pl_refname`
- Caveat: `default_flag = 1` is the archive's choice of best parameters,
  not always the most recent. Check `pl_refname` and verify against
  the source paper.

**DACE (Data & Analysis Center for Exoplanets)**
Geneva Observatory's RV planet database. More detailed orbital solutions
than NASA Archive for RV-detected planets — includes T₀, ω, eccentricity
confidence intervals, and full RV time series.

- URL: `https://dace.unige.ch/exoplanets/`
- Particularly strong for: nearby M-dwarf planets, HARPS/ESPRESSO targets
- Use when: NASA Archive orbital elements are sparse or outdated

**Extrasolar Planets Encyclopaedia (exoplanet.eu)**
European catalogue. Often updated faster than NASA Archive for newly
announced planets. Useful as a cross-check and for catching recent
discoveries not yet in the NASA Archive.

- URL: `https://exoplanet.eu`
- TAP endpoint: `http://voparis-tap-planeto.obspm.fr/tap`
- astroquery: `import pyvo; pyvo.dal.TAPService("http://voparis-tap-planeto.obspm.fr/tap")`
- Table: `exoplanet.epn_core`
- Bulk CSV download also available from the website.

**TEPCat (Transiting Extrasolar Planet Catalogue)**
Critical compilation of physical and orbital properties for transiting
systems. Independently derived -- not just a mirror of NASA Archive.
Particularly useful for transit-measured radii and masses where the
derivation methodology is documented.

- URL: `https://www.astro.keele.ac.uk/jkt/tepcat/`
- Machine-readable tables available for bulk download.
- Monthly snapshots archived for reproducibility.
- Provides: stellar mass/radius, planet mass/radius, orbital elements,
  obliquity, equilibrium temperature.

**Open Exoplanet Catalogue**
Community-maintained GitHub repository. JSON/XML format. Useful as a
quick lookup and for systems that may be underrepresented in the larger
archives.

- URL: `https://github.com/openexoplanetcatalogue/open_exoplanet_catalogue`
- Access: direct download or `git clone`.

---

### Transit Timing and Ephemeris Data

**NASA Exoplanet Archive Transit and Ephemeris Service**
Computes transit times for confirmed planets from the archive.
Critical for TTV-dominated systems like TRAPPIST-1.

- URL: `https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TransitView/nph-visibletbls`

**Exoplanet Transit Database (ETD)**
Amateur and professional transit observations. Lower precision than
peer-reviewed TTV analyses but broad coverage and useful for
epoch refinement.

- URL: `http://var2.astro.cz/ETD/`

---

### Literature and Paper Access

**NASA ADS (Astrophysics Data System)**
The authoritative literature database for astronomy. Use for:
- Tracing bibcodes from SIMBAD to full papers
- Finding the most recent orbital analyses for a given system
- Retrieving DOIs for all measurement entries

- URL: `https://ui.adsabs.harvard.edu`
- API: `https://api.adsabs.harvard.edu/v1/`

**arXiv (astro-ph.EP, astro-ph.SR)**
Preprint server. Many orbital analyses and stellar parameter papers
appear here before journal publication.

- URL: `https://arxiv.org/list/astro-ph.EP/recent`

---

### Archive and Space Mission Data

**MAST (Mikulski Archive for Space Telescopes)**
Hosts Kepler, K2, TESS, and HST data. Relevant if raw light curves
or transit photometry are needed for a specific system.

- URL: `https://mast.stsci.edu`
- astroquery: `from astroquery.mast import Observations`

---

### Access Priority Summary

| Data type | Primary | Secondary | Cross-check |
|---|---|---|---|
| Position, PM, parallax | Gaia DR3 | Hipparcos (bright stars) | JPL Horizons |
| Radial velocity | Gaia DR3 | SIMBAD | Discovery paper |
| State vectors (km, km/s) | Gaia DR3 → convert | JPL Horizons (direct) | -- |
| Stellar mass | SIMBAD `mesMass` | SWEET-Cat | VizieR (paper-specific) |
| Stellar radius | SIMBAD `mesDiameter` | TEPCat | VizieR (interferometry papers) |
| Orbital elements | NASA Exoplanet Archive | exoplanet.eu | TEPCat |
| Planet mass | NASA Exoplanet Archive | TEPCat | Discovery paper |
| Planet radius | NASA Exoplanet Archive | TEPCat | Discovery paper |
| Transit timing | NASA Archive ephemeris | ETD | Source paper (TTV analysis) |
| Paper lookup | ADS | arXiv | -- |

---

## Known Issues and Open Decisions

### KSP rendering engine limits at interstellar distances

Principia will correctly register a distant star as a gravitational perturber
regardless of distance. The double-precision position ULP at Alpha Centauri
(~4e13 km) is ~9 m -- acceptable for force calculations.

However, KSP's rendering engine is a separate concern. At interstellar
distances, floating-point precision in the renderer (not Principia) may cause
visual glitches, SOI/map view failures, or engine crashes. This has not been
tested at these scales.

**This trade-off must be decided before cfg generation begins:**
- Use real distances -> Principia physics correct, KSP renderer behaviour unknown
- Scale distances down -> KSP renderer stable, Principia physics incorrect

Record the decision and its rationale in `meta.notes` for each system file.

---

## Out of Scope

The following are handled in separate sessions or agents, not here:

- Kopernicus cfg generation
- Principia patch writing (Sol Real variant, Sol Quarter variant, RSS variant)
- Visual and art parameters (atmosphere, terrain, Scatterer, EVE)
- Community vote on which systems to include
- Decision on interstellar distance scaling (see Known Issues above)
