# Phase 1 Curation Checklist — 50 ly Hosts

## Setup
- [x] Confirm scope with user (PoC → full 121 hosts in one session)
- [x] Read [[feedback-planet-curation]] memory
- [x] Inspect raw data structure (`planets_raw.json` from `pscomppars`)
- [x] Identify root cause of previous attempt failure
- [x] Confirm `ps` table accessible from NASA Archive TAP

## PoC (Task #2)
- [x] Fetch `ps` rows for GJ 179, GJ 581, GJ 1132
- [x] Extract default_flag=1 row + bibcode per planet
- [x] WebFetch ADS abstract pages → ❌ JS-rendered, switched to bibcode-as-truth + Crossref DOI lookup
- [x] Build curated entries (planets + hosts)
- [x] Run `build_systems.py` + `validate.py` on PoC subset
- [x] Inspect output `db/systems/*.json` → confirm `derived` blocks populated
- [x] Document workflow surprises in `context-notes.md`

## Infrastructure (Task #3)
- [x] Decide: in-place modify `fetch_planets.py` or new `fetch_planets_ps.py` → new file (keep legacy)
- [x] Write the query for `ps` table with required fields + `default_flag`
- [x] Output structure: per-planet dict with explicit bibcode/doi/values
- [x] Test on PoC hosts → values match what PoC manually produced
- [x] Cache full `ps` fetch output for the 121 hosts
- [x] Small fix to `build_systems.py` line 643 — bibcode-or-doi dedup, bibcode propagation
- [x] Add stellar-parameter fallback (non-default-flag rows when default lacks `st_mass`/`st_rad`)
- [x] URL-decode bibcodes (NASA encodes `&` → `%26` for A&A papers)

## Bulk curation (Task #4)
- [x] Auto-generate `planets_curated.json` entries from `ps` default-row data
- [x] Auto-generate `stellar_props_curated.json` entries from `st_refname` rows
- [x] Spot-check bibcode validity — Crossref resolves 81 of 115 DOIs (70%, rest are arXiv preprints or rare journals)
- [x] Handle special cases:
  - [x] α Cen A/B, Barnard's star → PRESERVED (no overwrite — verified in build log)
  - [x] Hosts where `ps` default lacks values → fallback to non-default row (35 hosts)
  - [x] Brown dwarf companions — mass_type carries through (e.g. CWISEP, COCONUTS-2)
  - [x] Controversial planets (`pl_controv_flag=1`) — kept; flag is in raw, not curated

## Verification (Task #5)
- [x] `python3 scripts/pipeline/build_systems.py` clean run (143 written, 1 expected skip for WISEP)
- [x] `python3 scripts/pipeline/validate.py` → FAIL 0
- [x] WARN: 74 (down from 282 pre-curation; previous bulk fill was 52 but inflated coverage)
- [x] `principia` blocks populated for 121 / 144 (mass) and 105 / 144 (radius)
- [x] Coverage report (final):
  - **mass**: 121 / 144 — only 2 planet-host gaps (GJ 163, Ross 458) — verified 0 NASA `st_mass` rows
  - **radius**: 105 / 144 — 22 planet-host gaps — verified 0 NASA `st_rad` rows for M-dwarf sample
  - **planets curated**: 223 / 223
  - **DOI resolved**: 81 / 115 unique bibcodes (70%)

## Reporting + commit (Task #6)
- [x] Update `context-notes.md` with final decisions and surprises
- [x] Tick all boxes here
- [ ] Semantic commit
- [ ] Summary back to user

## Related

- [methodology hub](../../docs/reference/methodology.md) — parent topic this workspace contributes to
