# Planet Curation Reference

How to populate `db/planets_curated.json` for a host star, by depth tier.
Default is Phase 1; only escalate to Phase 2 on explicit user request.

---

## Phase 1 — Default (every new planet host)

Goal: one solid published source per planet, overriding NASA Archive
where the published paper is more precise or recent.

### Procedure per planet

1. **Identify the canonical paper.**
   - Discovery paper if the system is well-characterized (no major
     follow-up reanalyses).
   - Most recent re-analysis if mass/radius/orbital parameters were
     refined after discovery.
   - Quick check: search NASA ADS for `<planet name>` AND `RV` (or
     `transit`/`TTV`), sort by date, scan abstracts of top 3-5 results.

2. **Cross-check NASA Archive `pl_refname`.** If Archive cites the same
   paper you found, the auto-fetch is already using the best source —
   you can still add a curated entry to make the provenance explicit and
   to pin down orbital elements (ω, M₀, T_peri) that Archive composites
   sometimes mix from different solutions.

3. **For RV-detected planets, check DACE if NASA Archive lacks `omega_deg`
   or `tperi_bjd`.** DACE typically has the full orbital element set
   including uncertainties. URL pattern:
   `https://dace.unige.ch/exoplanets/?planet=<name>`

4. **For transiting planets, TEPCat is already auto-matched.** No extra
   action needed unless you want to override TEPCat with a more recent
   transit-light-curve fit.

5. **Compose the `planets_curated.json` entry.** Schema is in
   [file-edits.md §6](file-edits.md#6-dbplanets_curatedjson--phase-1-default-for-planet-hosts).

### What to record vs leave null

| Field | When to fill | Source |
|---|---|---|
| `semi_major_axis_au` | Always | Discovery paper |
| `eccentricity` | Always | Discovery paper; null only if explicitly unconstrained |
| `inclination_deg` | If transit OR astrometric fit | Transit fits give 88-90°; RV-only is null |
| `omega_deg` | RV systems usually have this | DACE or discovery paper |
| `mean_anomaly_at_epoch_deg` + `epoch_jd` | If T_peri is published | Convert T_peri to M₀ at chosen epoch |
| `true_mass_mearth` | If astrometry/transit gives it | Otherwise `mass_mearth` with `mass_type: "Msini"` |
| `radius_rearth` | Only if transiting | Null otherwise |
| `mass_type` | Always | `"Msini"`, `"true mass"`, `"transit"`, etc. |

### ADS access

Use the `WebFetch` tool against `https://ui.adsabs.harvard.edu/search/q=<query>`.
ADS does not require an API key for browse-style queries. Example:

```
WebFetch URL: https://ui.adsabs.harvard.edu/search/q=object:%22Wolf+359%22+AND+(RV+OR+%22radial+velocity%22)&sort=date+desc
Prompt: "Return the top 5 papers' bibcode, title, year, and first author. Highlight which has the most recent mass or orbital parameter measurement."
```

For direct paper text/abstract, fetch `https://ui.adsabs.harvard.edu/abs/<bibcode>`.

### ADS query patterns that work well

| Want | Query |
|---|---|
| Latest paper on planet X | `bibcode:(2023* OR 2024* OR 2025* OR 2026*) AND object:"<star>" AND ("planet" OR "companion")` |
| Mass measurement specifically | `<star name> AND (RV OR "radial velocity" OR TTV OR astrometric)` |
| Orbital reanalysis | `<star name> AND (orbital OR eccentricity OR "Keplerian fit")` |

ADS web UI for manual browsing: [ui.adsabs.harvard.edu](https://ui.adsabs.harvard.edu)

### When to skip Phase 1

- Planet was just announced (within 1-2 weeks) and not yet in NASA
  Archive — but discovery paper is available: add it manually with
  `retrieval_date: today`.
- Planet has been retracted: don't add a curated entry, and note in
  `meta.notes` of the host star file.
- All Archive values match the discovery paper exactly: curated entry
  still useful for explicit provenance, but optional.

---

## Phase 2 — Explicit escalation (in-game implementation)

Triggered by user phrases like:
- "Phase 2로 격상해줘"
- "이 시스템 인게임에 구현하자"
- "정밀 큐레이션 부탁해"
- "X 시스템 풀 큐레이션"

Goal: comprehensive measurement collection per the methodology's
five-priority order, with one explicitly chosen `recommended: true`
based on method tier.

### Procedure per planet

1. **Run Phase 1 first** if not already done (gets the baseline curated
   entry).

2. **Survey all five priority sources:**
   - Priority 1 — Individual paper (ADS): the discovery paper *and* any
     subsequent reanalysis. Add each as a separate measurement object.
   - Priority 2 — DACE: pull current orbital fit, especially for RV systems.
   - Priority 3 — TEPCat: for transiting planets, get all published
     transit-derived values, not just the latest.
   - Priority 4 — exoplanet.eu: usually a mirror; only add if it has
     something Archive doesn't.
   - Priority 5 — NASA Archive: already auto-fetched; no action.

3. **Accumulate measurements in arrays.** For Phase 2, expand the
   single-entry physical and orbital sections into arrays.
   
   **⚠ Prerequisite — code change first:** As of 2026-05-18,
   `build_planet_derived` in `scripts/pipeline/build_systems.py` reads
   `curated["physical"]` and `curated["orbital"]` as single dicts (via
   `(curated or {}).get("orbital") or {}`). Array-form curated entries
   will be silently ignored. Before any Phase 2 work:
   
   - Extend `build_planet_derived` to accept either dict or list-of-dict
     for `physical`/`orbital`. When list, pick the entry with
     `recommended: true` (parallel to `mass_measurements` logic).
   - Add a schema check in `schema.py` to enforce exactly-one
     `recommended: true` per array.
   - Update this skill's `references/planet-curation.md` to remove this
     warning.
   
   After the code change, the array form looks like this:

```json
"physical": [
  {
    "true_mass_mearth": 1.27,
    "uncertainty_mearth": 0.18,
    "mass_type": "Msini",
    "method": "RV",
    "source": "Anglada-Escudé 2016",
    "doi": "10.1038/nature19106",
    "recommended": false
  },
  {
    "true_mass_mearth": 1.07,
    "uncertainty_mearth": 0.06,
    "mass_type": "true mass",
    "method": "astrometric",
    "source": "Anglada-Escudé 2022 reanalysis",
    "doi": "10.1051/0004-6361/202242750",
    "recommended": true
  }
]
```

Note: this is an *extension* of the schema in
[file-edits.md](file-edits.md). `build_systems.py` needs an update to
handle array-form physical/orbital — verify before committing Phase 2
work. (As of 2026-05-18 the build script reads single-object form only.)

4. **Apply method hierarchy to set `recommended`:**

   | Tier | Method (decreasing priority) |
   |---|---|
   | 1 | astrometric / direct (true mass) |
   | 2 | TTV / dynamical |
   | 3 | RV (Msini) |
   | 4 | transit-only (radius only) |
   | 5 | predicted / theoretical |

   Tie within tier → smaller fractional uncertainty wins. Record the
   choice and tiebreaker reasoning in the host star file's `meta.notes`
   after the build runs.

5. **Conflict handling:**
   - If two measurements at the same tier disagree by ≥ 30%, surface to
     user — that's not a tiebreaker case.
   - If a measurement uses a method not in the hierarchy (e.g.
     "phase-curve thermal mapping" for radius), surface and ask user
     where to place it in priority order.

### TRAPPIST-1 as the canonical Phase 2 target

Likely first in-game implementation. Phase 2 should produce:
- 7 planet entries, each with discovery paper + Agol 2021 TTV + JWST
  atmospheric papers where relevant
- Mass measurements: Agol 2021 (dynamical, recommended) + Gillon 2017
  (discovery, non-recommended)
- Radius measurements: Agol 2021 (TTV-constrained) + JWST follow-ups

Estimated time: 1-2 hours.

---

## Quality checks

After editing `planets_curated.json`, verify:

```bash
python3 -c "import json; d=json.load(open('db/planets_curated.json')); 
print(f'Hosts: {len(d)}'); 
print(f'Planets: {sum(len(v) for v in d.values())}'); 
[print(f'  {h}: {[p[\"pl_name\"] for p in pls]}') for h, pls in d.items()]"
```

Then re-run the pipeline. Check that each new planet's
`derived` block in the system file has the curated values flowing through:

```bash
python3 -c "import json; d=json.load(open('db/systems/<host>.json'));
for p in d['planets']: print(p['name'], p['derived'])"
```

If curated values aren't appearing, check that `pl_name` exactly matches
between `planets_curated.json` and `planets_raw.json` (whitespace counts).
