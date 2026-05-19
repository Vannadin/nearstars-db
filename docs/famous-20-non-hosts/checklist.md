# Checklist — Famous 20 Non-Host Stars

## Setup
- [x] Sub-target list defined (20 components, 12 existing + 8 new)
- [x] Gaia DR3 IDs found for new additions (where they exist)
- [x] Capella treated as 1 component (Aa+Ab merged for KSP scale)

## New additions (8)
- [ ] Append 5 system entries to `target_list.json`
- [ ] HIPPARCOS_V: Arcturus (-0.05), Capella (0.08), Procyon B (10.92)
- [ ] SIMBAD_ALIASES: Van Maanen's Star → Wolf 28
- [ ] Mass/radius lookup from literature (Boyajian, Kervella, Mann, Holberg WDs)
- [ ] `stellar_props_curated.json` per-component entries
- [ ] `binary_orbits.json`: Procyon (Bond 2017), 70 Oph (orb6)
- [ ] Run `./run_pipeline.sh`
- [ ] Verify 5 new `db/systems/*.json` files exist
- [ ] All 8 new components have principia.mu and mean_radius_km populated

## Existing re-investigation (12)
- [ ] Sirius A: replace unverified → interferometry / asteroseismology
- [ ] Sirius B: WD literature (Holberg 2013)
- [ ] α Cen A/B: preserved Pourbaix 2016 — no change needed (verify)
- [ ] Vega: interferometric radius, evolutionary mass
- [ ] Altair: Monnier 2007 interferometry
- [ ] Fomalhaut: Mamajek 2012 or similar
- [ ] 61 Cyg A/B: Kervella 2008
- [ ] Kapteyn: keep Anglada-Escude 2014 or look for newer
- [ ] Eta Cas A/B: Boyajian or similar

## Verification
- [ ] `validate.py` FAIL 0
- [ ] target_list.json: 136 → 141 systems
- [ ] db/systems/: 144 → 149 files (4 new system files + 1 binary becomes 2 = 5 actually)

(Counting: 5 systems × 1 file per component → Arcturus 1, Capella 1, Procyon 2, Wolf 359 1, 70 Oph 2, Van Maanen 1 = 8 new files)

- [ ] commit + report
