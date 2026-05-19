# Troubleshooting

Common failures encountered when adding a star, and how to fix them.

---

## Pipeline-level errors

### `astrometry_raw에 없음 — 건너뜀`

`build_systems.py` couldn't find astrometry for the star. Causes:

1. **Gaia DR3 source_id wrong**: query Gaia archive directly to verify.
2. **SIMBAD fallback failed**: name doesn't match any SIMBAD identifier.
   Check `SIMBAD_ALIASES` and the helper script output.
3. **Star is in Gaia DR3 but parallax is null** (very faint sources):
   pipeline rejects parallax ≤ 0. May need to inject a manual entry.

Fix:
```bash
# verify Gaia entry exists
python3 -c "
import urllib.request, urllib.parse, json
q = \"SELECT source_id, parallax FROM gaiadr3.gaia_source WHERE source_id = <YOUR_ID>\"
data = urllib.parse.urlencode({'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'json','QUERY':q}).encode()
r = urllib.request.urlopen(urllib.request.Request('https://gea.esac.esa.int/tap-server/tap/sync', data=data, method='POST'))
print(json.loads(r.read())['data'])
"
```

### `parallax ≤ 0 — 건너뜀`

Gaia DR3 returned a negative or zero parallax (rare — means the
five-parameter solution failed). Two options:
- Drop the star (it's not actually nearby — Gaia gave it because the
  star is very faint or has multiple solutions)
- Use SIMBAD parallax as override by clearing the Gaia ID in
  `target_list.json` (forces SIMBAD fallback)

### `principia.gravitational_parameter_km3_s2: null` after build

No mass measurement has `recommended: true` in
`stellar_props_curated.json`. Confirm:
- An entry exists for this star
- At least one measurement has `recommended: true`
- The key in curated matches `target_list.components` exactly
  (whitespace, capitalization)

### `principia.mean_radius_km: null` after build

Same as above but for `radius_measurements`. Also check:
- SIMBAD `mesDiameter` may have returned a measurement automatically;
  the curated `recommended` overrides this. If you want SIMBAD's
  interferometry value, don't add a curated radius.

### `vmag_v: null` warning in validate

Gaia photometry missing AND no `HIPPARCOS_V` entry. Acceptable for:
- Y dwarfs and very late T dwarfs (no optical detection)
- Brown dwarfs in general

Not acceptable for:
- Main-sequence stars with V < 12 (should have Gaia or Hipparcos)
- → Add to `HIPPARCOS_V`

---

## SIMBAD name mismatch

### Symptom

`fetch_stellar_props.py` prints:
```
→ SIMBAD에 없음 (N개): [..., 'Your Star', ...]
```

After build, the star has `teff_k: null`, `spectype: null`, and no
SIMBAD-derived radius.

### Diagnose

Check what SIMBAD actually calls the star:

```bash
python3 -c "
import urllib.request, urllib.parse, json
q = \"SELECT id FROM ident WHERE id LIKE '%Your Star%'\"
data = urllib.parse.urlencode({'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'json','QUERY':q}).encode()
r = urllib.request.urlopen(urllib.request.Request('https://simbad.u-strasbg.fr/simbad/sim-tap/sync', data=data, method='POST'))
print([row[0] for row in json.loads(r.read())['data']])
"
```

### Fix

Add the SIMBAD canonical form to `SIMBAD_ALIASES` in
`scripts/pipeline/fetch_stellar_props.py`. Re-run only `fetch_stellar_props.py`
and then `build_systems.py`.

---

## Binary system edge cases

### "binary=true이나 binary_orbits.json에 항목 없음" warning

`build_systems.py` set `is_binary=True` from `target_list.json` but
couldn't find the corresponding entry in `binary_orbits.json`.

Causes:
- `target_list.system` doesn't match the key in `binary_orbits.json`
  (whitespace, capitalization)
- You set `binary: true` before adding the orbit data

Fix: ensure the system name is identical in both files. The orbit data
must exist before setting `binary: true`.

### Triple system with one unrelated component

If A and B are gravitationally bound but C is a wide companion not in a
fitted orbit:
- Include all three in `target_list.components`
- Only include A and B in `binary_orbits.components`
- The build will embed binary_orbit in A's file, mark B with ref, and
  give C no binary_orbit attribute (since C isn't in binary_orbits)

Document the hierarchy in `binary_orbits.json` field `hierarchy`:
`"binary"`, `"triple"`, `"hierarchical-AB+C"`, etc.

---

## Planet data issues

### Planet missing from `planets_raw.json` after fetch

`fetch_planets.py` queries the full `pscomppars` table and filters
results by `hostname IN target_list`. Possible causes for missing:
- Hostname in `target_list.json` doesn't match NASA Archive `hostname`
  (typos, alternate names) — check exact spelling
- Planet not yet in NASA Archive (very recent discovery)
- Planet retracted — verify on NASA Archive directly

### Phase 1 curated values not flowing through to `derived` block

The merge in `build_planet_derived` keys on `pl_name`. Verify:
- Exact name match (`"Proxima Cen b"` ≠ `"Proxima Centauri b"` ≠ `"Proxima Cen b "`)
- Strip leading/trailing whitespace

The auto-extracted `pl_name` from NASA Archive is the canonical form.
Check the entry in `planets_raw.json` and copy the exact string.

### TEPCat values not appearing for transiting planet

TEPCat name format is finicky (`55_Cnc_e`, `GJ_1214b`, `TRAPPIST-1c`).
The `tepcat_keys()` function in `fetch_planets.py` tries several
variants. If none match:
- Check TEPCat's allplanets-csv.csv for the actual entry name
- Add a new variant to `tepcat_keys()` in `fetch_planets.py`

---

## Schema validation failures

### `금지 prefix 사용 ['error_*']` in `stellar_props_raw 스키마 검증 실패`

Some measurement object uses `error_*` instead of `uncertainty_*`. Most
common cause: copy-paste from an older paper or template.

Fix: change `error_msun` → `uncertainty_msun`, `error_rsun` →
`uncertainty_rsun`.

This is enforced by `schema.py` precisely because field naming has
caused data quality issues in the past.

### `value_* 키 없음`

A measurement object has `method` and `reference` but no `value_msun`
or `value_rsun`. Always provide `value_<unit>`. If unknown, omit the
entire measurement object — don't leave a placeholder.

---

## Pipeline performance

### Pipeline takes > 10 minutes

Typical full run is 5-6 minutes. If longer:
- SIMBAD TAP may be slow (server load) — try again later
- Network issues — check if other queries to gea.esac.esa.int / simbad.u-strasbg.fr work
- Gaia archive may be doing maintenance

Each script can be run independently. To resume after a slow step:
```bash
# only re-run what's needed
python3 scripts/pipeline/build_systems.py
python3 scripts/pipeline/validate.py
```

---

## Network / API failures

### `HTTPError 502` / `503` / `urllib.error.URLError`

External TAP servers (Gaia, SIMBAD, NASA Archive) are not 100% available.
The fetch scripts don't retry by default.

If only one fetch failed, re-run that specific script. If all four fail
simultaneously, your network is the problem — check connectivity to
`gea.esac.esa.int`, `simbad.u-strasbg.fr`, `exoplanetarchive.ipac.caltech.edu`.

### `HTTPError 400` from SIMBAD

Usually a malformed ADQL query — special characters in star names
(apostrophes, brackets) not escaped. Check the affected star name.

### `urllib.error.URLError: [Errno 8] nodename nor servname provided`

DNS resolution failure. The pipeline cannot proceed. Verify internet
connection and DNS settings before retrying.

### TEPCat CSV fetch fails

`fetch_planets.py` continues with empty TEPCat data on failure — you'll
see `→ 0개 행성에 TEPCat 데이터 연결`. Transit-derived mass/radius
overrides won't apply. Re-run the script later when TEPCat is reachable.

### NASA Archive returns 0 planets after query

The query targets the full `pscomppars` table without a distance filter.
If the result is empty:
- NASA Archive TAP service down — try again later
- Network issue — verify `exoplanetarchive.ipac.caltech.edu` reachable
- Target hostnames don't match Archive's `hostname` column — verify
  spelling against the Archive's web interface

### Gaia TAP returns null radial_velocity

Normal for faint red dwarfs and brown dwarfs. The build sets RV=0 with a
note in `radial_velocity_source`. Position propagation still works
(tangential motion dominates for nearby stars).

---

### One specific star takes forever in `fetch_stellar_props.py`

The script does ~1 query/star with 0.1s sleep. Total ~14 seconds of
sleep + ~2s × 144 = ~5 minutes. This is dominated by SIMBAD response
time, not bandwidth.

To investigate per-star slowness, add a `print(time.time())` around the
specific star and see if SIMBAD is the bottleneck.

---

## When to roll back

Backups live in `db/backup_<date>/`. Before destructive operations
(rebuild from scratch, mass edit of curated files):

```bash
cp -r db/systems db/backup_$(date +%Y_%m_%d_%H%M)/systems
cp db/*.json db/backup_$(date +%Y_%m_%d_%H%M)/  # only the curated ones
```

To restore:
```bash
cp -r db/backup_<date>/systems db/systems
```

The pipeline can also be re-run from raw — the raw JSON files are the
"trust boundary" for fetched data. Curated files are the trust boundary
for human-entered data.
