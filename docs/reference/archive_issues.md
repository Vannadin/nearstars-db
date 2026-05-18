# NASA Exoplanet Archive Data Issues

Found during cross-validation against SIMBAD/Gaia DR3 (2026-05-16).
Contact: exoplanetarchive@ipac.caltech.edu

---

## Issue 1: GJ 411 — stale distance, missing Gaia DR3 link

**Table:** pscomppars  
**Field:** sy_dist, gaia_dr3_id

| Field | Archive value | Correct value | Source |
|-------|--------------|---------------|--------|
| sy_dist | 5.676 pc (18.5 ly) | 2.546 pc (8.3 ly) | SIMBAD plx 392.75 mas |
| gaia_dr3_id | NULL | should exist | Lalande 21185 / HD 95735 |

The archive distance appears to be a pre-Gaia measurement that has not been updated.
GJ 411 (Lalande 21185 / HD 95735) is the 5th nearest stellar system and well within Gaia DR3 coverage.

---

## Issue 2: GJ 273 — stale distance, missing Gaia DR3 link

**Table:** pscomppars  
**Field:** sy_dist, gaia_dr3_id

| Field | Archive value | Correct value | Source |
|-------|--------------|---------------|--------|
| sy_dist | 5.922 pc (19.3 ly) | 3.786 pc (12.4 ly) | SIMBAD plx 264.13 mas |
| gaia_dr3_id | NULL | should exist | Luyten's Star / GJ 273 |

Same pattern as GJ 411 — pre-Gaia distance retained, no Gaia DR3 cross-match.

---

## Issue 3: VHS J125601.92-125723.9 — distance conflict between Archive and Gaia DR3

**Table:** pscomppars  
**Field:** sy_dist

| Source | Distance |
|--------|----------|
| Archive sy_dist | 12.7 pc (41.4 ly) — photometric estimate |
| Gaia DR3 parallax | 47.27 mas → 21.15 pc (69.0 ly) |

The discrepancy (8.45 pc) exceeds the 50 ly selection boundary used in this project.
Note: VHS J125601.92-125723.9 is an M7.5 brown dwarf — Gaia optical parallax reliability
may be reduced for this extremely red object (bp_rp = 4.46, G = 15.1).
An independent infrared parallax measurement would resolve this conflict.

---

---

## Issue 4 (TEPCat): TRAPPIST-1 d — mass 10× too large

**Source:** https://www.astro.keele.ac.uk/jkt/tepcat/allplanets-csv.csv  
**Field:** M_b (Mjup), column index 26  
**Found:** 2026-05-18, cross-validation against NASA Exoplanet Archive

| Source | Value | Reference |
|--------|-------|-----------|
| TEPCat allplanets-csv | 0.0122 Mjup = 3.8775 M⊕ | 2021PSJ.....2....1A |
| NASA Exoplanet Archive | 0.00122 Mjup = 0.388 M⊕ | same paper |

All other TRAPPIST-1 planets (b, c, e, f, g, h) agree between the two sources within 1%.
The discrepancy is exactly 10×, consistent with a missing decimal zero in TEPCat's data entry
(`0.0122` instead of `0.00122`). Both sources cite Agol et al. 2021 (2021PSJ.....2....1A).

Contact for TEPCat corrections: https://www.astro.keele.ac.uk/jkt/tepcat/

---

## How these were found

Query: `SELECT hostname, sy_dist, gaia_dr3_id FROM pscomppars WHERE sy_dist <= 15.307`

Cross-validated each returned system against:
- Gaia DR3 TAP (gaiadr3.gaia_source, matched by gaia_dr3_id)
- SIMBAD TAP (basic table, plx_value)

Systems where gaia_dr3_id was NULL fell back to SIMBAD astrometry,
which revealed the distance discrepancies for GJ 411 and GJ 273.
