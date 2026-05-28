<!-- eps Eri Phase 2 + Phase 3 reconciliation checklist -->
# eps Eri — Phase 2 + Phase 3 reconciliation checklist

Mirroring delta-pavonis (commit 4d26495) for Tier 1 host eps Eri.

## Phase 2 entry in `db/stellar_props_curated.json`

- [x] Replace existing barebones eps Eri entry (mass+radius only, method=unverified) with full 8/8 categories
- [x] Top-level `teff_k`, `teff_bibcode`, `spectype`, `spectype_bibcode`, `spectype_reference`
- [x] `mass_measurements` — Llop-Sayson 2021 recommended (joint RV + Hipparcos/Gaia astrometry)
- [x] `radius_measurements` — Baines 2008 CHARA interferometric recommended (method: direct_interferometry); Di Folco 2007 VLTI/VINCI second; Rosenthal 2021 CLS SED third
- [x] `teff_measurements` — Valenti & Fischer 2005 SME recommended; Brewer 2016 cross-check; Baines 2012 interferometric
- [x] `luminosity_measurements` — Baines 2012 bolometric flux recommended
- [x] `age_measurements` — Mamajek & Hillenbrand 2008 (440 Myr) recommended; Barnes 2007 gyrochrone cross-check
- [x] `metallicity_measurements` — Valenti & Fischer 2005 SME recommended; Brewer 2016 cross-check
- [x] `rotation_measurements` — Donahue 1996 (11.2 d Ca II HK) recommended; Croll 2006 MOST cross-check
- [x] `activity_measurements` — log R'HK Zechmeister 2013 recommended; Henry 1996 cross-check
- [x] `meta_notes` with caveats (Metcalfe 2013 dual 2.95+12.7 yr cycle, Coffaro 2020 X-ray cycle, no asteroseismology)

## Phase 3 reconciliation

- [x] `docs/phase3/eps-eri.md` Decisions table — update stellar rows to match new Phase 2 recommended picks
- [x] Add new bibliography entries for Phase 2 anchors (move existing entries from "context" to "primary" tier as needed)
- [x] `docs/phase3/eps-eri-b.md` — update host-star context if mass/radius diverge from new Phase 2 recommended
- [x] `ko/docs/phase3/eps-eri.md` mirror — block parity
- [x] `ko/docs/phase3/eps-eri-b.md` mirror — block parity

## Rebuild + verify

- [x] `python3 scripts/pipeline/build_systems.py`
- [x] `python3 scripts/pipeline/build_site.py`
- [x] `python3 scripts/pipeline/build_phase2_html.py`
- [x] `python3 scripts/pipeline/build_reports_index.py`
- [x] `python3 scripts/phase3/check_block_parity.py eps-eri`
- [x] `python3 scripts/phase3/check_block_parity.py eps-eri-b`
- [x] `python3 scripts/phase3/build_html.py eps-eri`
- [x] `python3 scripts/phase3/build_html.py eps-eri-b`
- [x] `python3 scripts/pipeline/validate.py` (FAIL=0)
- [x] `./scripts/check.sh` (passes)
- [x] semantic commit
