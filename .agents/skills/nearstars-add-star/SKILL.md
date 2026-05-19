---
name: nearstars-add-star
description: >
  Add a star (or binary/multiple system) to the NearStars KSP mod database
  pipeline. Trigger this skill whenever the user wants to add any stellar
  system to the project — phrases like "X 별 추가해줘", "add Y star", "GJ
  XXX 추가", "(별 이름) 데이터 만들어줘", "이 시스템도 데이터베이스에
  넣자", or any time the conversation involves expanding the target_list to
  include a new star. The DB layer is distance-agnostic; downstream cfg
  writers (Kopernicus ~50 ly, Principia ~80 ly) handle their own range
  limits. Also use this skill when the user says "이거 Phase 2로 격상" or
  "정밀 큐레이션 해줘" for an existing star — the same procedure applies to
  the curation upgrade. Do NOT use this skill for writing Kopernicus or
  Principia cfg files (those are downstream of the DB); use kopernicus-cfg
  for that.
---

# NearStars — Add Star to DB

This skill executes the full pipeline-driven workflow for adding one or more
stellar components to `db/systems/`. The user has delegated the small
decisions (Gaia ID lookup, recommended-measurement selection, default
planet-curation depth); follow the policies in user memory rather than
asking each time.

---

## Trigger Recap

You are running this skill if any of these hold:
- The user explicitly named a star and asked to add it to the database.
- The user asked to expand the project to cover a new system.
- The user requested Phase 2 (full literature) curation for a system that
  already exists in the DB.

If the request is about generating a Kopernicus or Principia cfg, stop —
that's the `kopernicus-cfg` skill and runs downstream of this DB.

---

## Workflow Overview

```
1. Pre-research            ← look up Gaia DR3 ID, distance, structure, planets
2. File edits              ← target_list, stellar_props_curated, conditional files
3. Planet curation         ← Phase 1 default (Phase 2 if user requested)
4. Pipeline run            ← ./run_pipeline.sh (or just build_systems if no fetch needed)
5. Verify                  ← inspect output JSON, validate.py FAIL=0
6. Report                  ← summary to user
```

Each step is detailed below. For full templates, decision trees, and edge
cases, see the `references/` files when you reach the relevant step.

---

## Step 1 — Pre-research

Goal: gather everything you need so the rest is mechanical edits.

For each component of the system, you need:

| Required | How to find |
|---|---|
| Common name (e.g. "GJ 412 A") | User-provided |
| Distance | SIMBAD or RECONS — record it. No hard limit at the DB layer; note >50 ly in `meta.notes` since downstream Kopernicus cfg ignores it |
| Gaia DR3 `source_id` | SIMBAD `ident` table — see `scripts/lookup_gaia.py` |
| Component structure (single/binary/triple) | SIMBAD or discovery paper |
| V magnitude (only if Gaia-saturated, V<~6) | Hipparcos / SIMBAD |
| Mass/radius literature values | NASA ADS — method-priority |
| Planets (auto-fetched, but check if recent) | NASA Exoplanet Archive |
| Mutual orbit if binary/multiple | Pourbaix, WDS, Sixth Orbit Catalog |

Run the helper script when you have a candidate name:

```bash
python3 .agents/skills/nearstars-add-star/scripts/lookup_gaia.py "GJ 412 A"
```

It returns Gaia DR3 source_id (if any), SIMBAD canonical name, distance, V
magnitude, and component flags. If SIMBAD returns nothing, the name is
ambiguous — try alternate names or escalate to user.

---

## Step 2 — File edits

Edit only the files needed for the case. The pipeline merges raw + curated
on next run.

| File | When to edit | What to add |
|---|---|---|
| `target_list.json` | **Always** | One new entry — system/components/gaia_source_ids/binary |
| `db/stellar_props_curated.json` | **Almost always** | Mass + radius measurements per component |
| `scripts/pipeline/fetch_photometry.py` `HIPPARCOS_V` | If Gaia-saturated bright star (V<~6) | Hardcoded V magnitude with comment |
| `scripts/pipeline/fetch_stellar_props.py` `SIMBAD_ALIASES` | If SIMBAD canonical name differs from `target_list` name | `"our name": "SIMBAD name"` |
| `db/binary_orbits.json` | If multiple star system | Mutual orbit block |
| `db/planets_curated.json` | If host star has confirmed planets (Phase 1) | Per-planet orbital + physical literature values |

**Exact schemas and examples are in [references/file-edits.md](references/file-edits.md). Read it before editing any file.**

---

## Step 3 — Planet curation depth

Default = **Phase 1** (memory: `feedback-planet-curation`):

- For each confirmed planet, find one published source — usually the
  discovery paper or most recent reanalysis — and add an entry to
  `db/planets_curated.json`.
- For RV-detected planets, check if NASA Archive has `omega_deg` and
  `tperi_bjd`. If missing, consult DACE for the orbital solution.
- Transiting planets fall back to TEPCat automatically — no extra work.
- exoplanet.eu only as cross-check if NASA Archive is sparse or stale.

Escalate to **Phase 2** only if the user explicitly says so ("정밀 큐레이션",
"Phase 2", "이 시스템 인게임 구현하자"). Phase 2 walks all five priority
sources from the methodology and accumulates every published measurement.

Details, ADS search patterns, and the curated.json schema:
[references/planet-curation.md](references/planet-curation.md)

---

## Step 4 — Pipeline run

If you only added/changed curated files and `target_list.json`, **and** the
star is already in `astrometry_raw.json` from a previous run:

```bash
python3 scripts/pipeline/build_systems.py
python3 scripts/pipeline/validate.py
```

Otherwise (new star — no raw data yet):

```bash
./run_pipeline.sh
```

This runs all four fetches (Gaia, SIMBAD, NASA Archive, photometry) plus
build + validate + site build. ~5 minutes for full run, dominated by
SIMBAD OID lookups (~2s/star).

---

## Step 5 — Verify

After the pipeline finishes, inspect the new file:

```bash
python3 -c "import json; d=json.load(open('db/systems/<filename>.json')); print(json.dumps({k:v for k,v in d.items() if k!='planets'}, indent=2)[:1500])"
```

Checklist for each new component:

- [ ] File exists at `db/systems/<filename>.json`
- [ ] `stars[0].raw`: ra/dec/parallax/proper motion not null
- [ ] `stars[0].derived.position_ulp_km` is reasonable (~1e-2 to 1e-3 km for 10-50 ly)
- [ ] `stars[0].principia.gravitational_parameter_km3_s2` not null (else curated mass missing)
- [ ] `stars[0].principia.mean_radius_km` not null (else curated radius missing)
- [ ] If binary: `binary_orbit` block present (primary) or `binary_orbit_ref` (sibling)
- [ ] If planets: each planet has `derived.semi_major_axis_m` and `mass_kg`
- [ ] `validate.py` reports `FAIL: 0` (WARN is OK for known-missing data)

If any item fails, see [references/troubleshooting.md](references/troubleshooting.md).

---

## Step 6 — Report

Summarize back to the user:

```
<star name> 추가 완료.
- Gaia DR3 ID: 12345...  (or "없음, Hipparcos 폴백")
- Distance: 8.2 ly
- Components: 1  (or "binary: A+B")
- Planets: 2 confirmed (b, c)
- Mass source: <Author Year>, <method>
- 파일: db/systems/<filename>.json
- validate.py: FAIL 0, WARN N
```

If any value was assumed or estimated (e.g. inclination unknown → null in
DB), note it explicitly so the user knows what the Kopernicus writer will
have to fill in later.

---

## Key Policies (from user memory)

These are the user-confirmed defaults. Do NOT ask the user about them.
Memory references use `[[memory-name]]` — the LLM loads memory by name
from the user's memory store, not by file path.

- **Gaia ID lookup**: search SIMBAD `ident` yourself, don't ask user.
  See `[[feedback-star-addition]]`.
- **Recommended measurement selection**: when authoring a curated entry,
  *you* set exactly one `recommended: true` per `mass_measurements` /
  `radius_measurements` array. The pipeline reads that flag literally —
  it does NOT auto-apply method tiers. Use the hierarchy below to pick:
  - Mass: `binary_orbit` > `asteroseismology` > `evolutionary_model` >
    `spectroscopic` > `spectroscopic_calibration`
  - Radius: `interferometry` > `eclipsing_binary` > `evolutionary_model`
  
  Ties within a tier → pick smaller fractional uncertainty. Record
  the choice and tiebreaker in the host's `meta.notes` after the build
  runs (manual edit; build doesn't propagate notes).
- **Planet curation depth**: Phase 1 default. Don't escalate to Phase 2
  without explicit user request. See `[[feedback-planet-curation]]`.
- **DB design**: derived blocks store unit-converted measurements only;
  null is null, never substitute defaults. See
  `[[project-nearstars-db-principle]]`.
- **Binary file layout**: one file per component; mutual orbit embeds
  in the representative (first) component; siblings store
  `binary_orbit_ref`. See `[[project-nearstars-binary-layout]]`.

If a policy conflict arises (e.g. two binary_orbit measurements 30%+
apart, or a new method tier not in the hierarchy), surface it to the
user rather than silently picking.

---

## Common edge cases

Quick handling reference. Full details in
[references/decision-tree.md](references/decision-tree.md) and
[references/troubleshooting.md](references/troubleshooting.md).

| Symptom | Likely cause | Fix |
|---|---|---|
| `astrometry_raw에 없음 — 건너뜀` | Gaia DR3 has no entry and SIMBAD fallback failed | Verify name in SIMBAD, add to `SIMBAD_ALIASES` |
| `principia.gravitational_parameter_km3_s2: null` | No recommended mass in curated | Add mass measurement with `recommended: true` |
| `vmag_v: null` | No Gaia photometry and not in `HIPPARCOS_V` | Add to `HIPPARCOS_V` if V mag exists; leave null for Y dwarfs |
| Star is V<6 (Vega, Sirius, etc.) | Gaia saturation — astrometry from SIMBAD, photometry needs Hipparcos | Hardcode V in `HIPPARCOS_V`; epoch becomes J2000.0 instead of J2016.0 |
| Brown/sub-stellar dwarf with `value_msun < 0.08` | Sub-stellar mass measurement | Use SED/evolutionary model paper; record method correctly |
| Distance > 50 ly | Outside Kopernicus rendering range | Proceed with DB collection — distance is a downstream concern, not a DB-layer one. Note the distance in `meta.notes`. Whoever writes the Kopernicus cfg will skip this star (out of their range); Principia cfg writer may include it as a perturber if within their ~80 ly range. The DB itself stores any distance. |

---

## Related documents

For human-oriented reference (not used by the skill, but useful when
debugging discrepancies):

- `docs/reference/methodology.md` — DB schema and design intent
- `docs/reference/adding_stars.md` — original operational manual; this
  skill supersedes it for automated work but the manual stays
  authoritative for human edits
- `docs/reference/guideline.md` — project-level scope, dependencies,
  distance limits
- `docs/reference/principia-cfg-reference.md` — for the downstream
  cfg writer (out of scope here)
