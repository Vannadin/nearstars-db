# Phase 2 — stellar spin-axis inclination (i★) + position angle curation (2026-06-15)

Add measured stellar spin-axis orientation (i★ = axis tilt to line of sight; PA = sky
position angle of the projected axis) as a Phase 2 measurement category, then show it in
the 3D viewer (replacing the spin-orbit-alignment assumption where a measurement exists).

Source: literature survey (subagent, 2026-06-15). Tiers: direct = interferometry/
asteroseismology/Doppler-imaging; derived = vsini+P+R / ZDI / activity modeling.

## Schema
- [ ] Add `inclination_measurements` to STELLAR_MEASUREMENT_KINDS (value_keys {value_deg};
      methods interferometry/spectro_astrometry/asteroseismology/zeeman_doppler/
      vsini_inversion/activity_modeling/lightcurve_modeling/disk_proxy/unverified;
      extra_keys position_angle_deg, position_angle_uncertainty_deg, notes).

## Curate (12 stars)
With existing measurements.yaml (edit YAML → apply_phase2):
- [ ] α Cen B  i★ 45 (+9/−19)  activity_modeling  Dumusque 2014 (2014ApJ...796..133D)
- [ ] Proxima  i★ 47±7  zeeman_doppler  Klein/Donati 2021 (2020MNRAS.500.1844K)
- [ ] HD 219134  i★ 77±8  zeeman_doppler  Folsom 2018 (2018A&A...619A.130F)
- [ ] YZ Cet  i★ 60±5  zeeman_doppler  (arXiv:2511.21853, 2025)
- [ ] GJ 896 A  i★ 60  zeeman_doppler  Morin 2008 via Curiel 2022 (2008MNRAS.390..567M)
Without YAML (direct write_canonical injection — build_curated_from_ps preserves):
- [ ] Vega  i★ 6.2±0.4, PA −58±6  interferometry  Monnier 2012 (2012ApJ...761L...3M)
- [ ] Fomalhaut  i★ null, PA 65±3  spectro_astrometry  Le Bouquin 2009 (2009A&A...498L..41L)
- [ ] AU Mic  i★ 90 (+0/−20)  vsini_inversion  Watson 2011 (2011MNRAS.413L..71W)
- [ ] ε Eri  i★ 30±3  lightcurve_modeling  Croll 2006 (2006ApJ...648..607C)  [NOT 79°]
- [ ] τ Cet  i★ 7±7  interferometry  Korolik 2023 (2023AJ....166..123K)
- [ ] HD 69830  i★ 13 (+27/−13)  vsini_inversion  Simpson 2010 (2010MNRAS.408.1666S)
- [ ] V1400 Cen  i★ 68±10  vsini_inversion  Mamajek 2012 (2012AJ....143...72M)
Skipped: Luhman 16 A/B (literature value disputed); α Cen A, 55 Cnc, ε Ind A, TRAPPIST-1,
Barnard, 40 Eri A, Teegarden, GJ 9066, 61 Vir (no axis constraint → keep alignment default).

## Viewer
- [ ] build_starmap: emit i★ + PA per component (from stellar_props inclination_measurements).
- [ ] starmap_template: spin axis uses measured i★ (+PA where present) via skyBasis; else the
      spin-orbit-alignment default. Tooltip/legend distinguishes measured vs assumed.

## Verify
- [ ] validate.py green; check.sh green; reproducible build; JS syntax OK.
