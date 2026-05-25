# Famous 20 Non-Host Stars within 50 ly — Plan

## Scope

Objective top-20 most famous non-planet-host stars within 50 ly. Re-investigate where already in DB, add fresh where not.

## The 20 (objective by fame: brightness + history + culture + scientific significance)

### Already in DB → re-investigate (12 components)

| # | Star | Why famous | Current curation |
|---|---|---|---|
| 1 | Sirius A | Brightest in night sky | unverified — bulk fill |
| 2 | Sirius B | First WD discovered | unverified |
| 3 | α Cen A | Closest system (Proxima sibling) | binary_orbit Pourbaix 2016 (PRESERVED) |
| 4 | α Cen B | same | binary_orbit Pourbaix 2016 (PRESERVED) |
| 5 | Vega | Photometric standard | unverified |
| 6 | Altair | Summer Triangle | unverified |
| 7 | Fomalhaut | α PsA, debris disk | unverified |
| 8 | 61 Cygni A | Bessel's first parallax (1838) | unverified |
| 9 | 61 Cygni B | same | unverified |
| 10 | Kapteyn | Halo subdwarf, fast PM | unverified Anglada-Escude 2014 |
| 11 | Eta Cassiopeiae A | Achird, naked-eye binary | unverified |
| 12 | Eta Cassiopeiae B | same | unverified |

### New additions (8 components)

| # | Star | Why famous | Approach |
|---|---|---|---|
| 13 | Arcturus | 4th brightest, K-giant | Single, SIMBAD astrometry, HIPPARCOS_V |
| 14 | Capella | 6th brightest, close binary | Single entry (Aa+Ab dynamically merged) |
| 15 | Procyon A | 8th brightest, α CMi | Binary with B, SIMBAD astrometry |
| 16 | Procyon B | Classic WD secondary | same binary |
| 17 | Wolf 359 | Star Trek/sci-fi fame | Single, Gaia ✓ |
| 18 | 70 Ophiuchi A | Bessel's binary, historic | Binary with B, Gaia ✓ |
| 19 | 70 Ophiuchi B | same | same binary |
| 20 | Van Maanen's Star | First isolated WD (1917) | Single, Gaia ✓, SIMBAD alias to "Wolf 28" |

## Approach

### For 8 new additions

1. `target_list.json` — append 5 system entries: Arcturus, Capella, Procyon (A+B), Wolf 359, 70 Ophiuchi (A+B), Van Maanen's Star
2. `fetch_photometry.py HIPPARCOS_V` — add Arcturus (-0.05), Capella (0.08), Procyon B (10.92)
3. `fetch_stellar_props.py SIMBAD_ALIASES` — Van Maanen's Star → "Wolf 28"
4. `stellar_props_curated.json` — mass + radius + spectype with paper attribution per component
5. `binary_orbits.json` — Procyon (Bond et al. 2017), 70 Ophiuchi (Pourbaix orb6 grade 2)
6. Run `./run_pipeline.sh` (need fresh fetches for new stars)

### For 12 existing re-investigations

Lighter pass since pipeline already has data:
- Check current curated `method` and `bibcode`
- Where method="unverified", attempt to find authoritative paper (interferometric radius from Boyajian 2012/2013, mass from Stassun TICv8 2019 for FGK, Mann 2015 for M)
- Update entry with proper method label + bibcode + DOI
- Preserve α Cen A/B (Pourbaix 2016 already optimal)

## Success criteria

- 20 components all have:
  - `principia.gravitational_parameter_km3_s2` != null
  - `principia.mean_radius_km` != null
  - At least one mass measurement with proper `method` (not "unverified") and bibcode
- `validate.py` FAIL 0
- 8 new system files exist in `db/systems/`
- target_list.json grows from 136 → 141 systems

## Related

- [methodology hub](../../docs/reference/methodology.md) — parent topic this workspace contributes to
