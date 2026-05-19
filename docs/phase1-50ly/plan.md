# Phase 1 Curation — All 50 ly Planet Hosts (Plan)

Skill-validation test triggered 2026-05-19. Reset commit `1f023d0` cleared the prior `pscomppars` bulk-fill because it violated the per-paper attribution policy ([[feedback-planet-curation]]).

## Goal

For every planet host within 50 ly currently in the DB (121 hosts, 223 confirmed planets), produce paper-attributed entries in `db/planets_curated.json` and corresponding host mass/radius entries in `db/stellar_props_curated.json`. Each measurement carries an explicit `bibcode` and (when available) `doi`. Pipeline rebuild yields FAIL 0 in `validate.py`.

## Why the previous attempt was wrong

`fetch_planets.py` queries `pscomppars` (composite parameters) and stores `disc_refname` (discovery reference) per planet. `pscomppars` values are NASA's merged best-effort from multiple papers — the discovery paper rarely matches the actual source of mass/radius/period values. The earlier bulk fill recorded `disc_refname` as if it were the source for every parameter. That is exactly the "Phase 0.5" shortcut the user forbade.

## Correct Phase 1 workflow

1. Query the NASA Exoplanet Archive `ps` table (per-paper rows) for each planet, filtering `default_flag = 1`. NASA marks one row as the default — the paper they currently consider authoritative for that planet.
2. Take the parameter values **and** `pl_refname` from that row. The `pl_refname` is the source of those specific values.
3. Extract bibcode from the `pl_refname` HTML link (already in `<a refstr=... href=https://ui.adsabs.harvard.edu/abs/{bibcode}/abstract>` form).
4. Verify the bibcode resolves on ADS via WebFetch (spot-check sample for the bulk run; full check for PoC).
5. Resolve bibcode → DOI when possible (ADS abstract page contains DOI).
6. Build `planets_curated.json` entries with values + bibcode + doi explicit.
7. For host masses/radii, follow the same pattern from `stellar_props_raw.json` measurement arrays — many already have bibcodes, just need to be promoted to curated.

## Approach

PoC first (2-3 representative hosts), then full bulk.

- **PoC hosts:** GJ 179 (RV, single), GJ 581 (RV, multi-planet), GJ 1132 (transit + RV mix).
- After PoC: extend the fetch script to fetch `ps` table rows so this becomes mechanical for the 223 planets.
- Bulk run, then validate.

## Out of scope

- Phase 2 (full literature) — only triggered per system on user request.
- Re-fetching astrometry / photometry / SIMBAD (already cached and stable).
- Kopernicus / Principia cfg generation (downstream skill).
- Stars without planets (21 hosts in the DB) — they keep their current curation level; Phase 1 is planet-host-only.

## Success criteria

- `db/planets_curated.json`: 223 planet entries, each with `bibcode`.
- `db/stellar_props_curated.json`: ≥121 entries (the 3 high-quality + 118 new minimum).
- `validate.py`: FAIL 0; WARN count comparable to or better than the previous bulk-fill baseline (52).
- Per planet: `derived.semi_major_axis_m`, `mass_kg` populated where source has them.
- Source attribution: no entry pointing to `pscomppars` as the source.
