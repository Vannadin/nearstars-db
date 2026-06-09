# Luhman 16 AB — Phase 2 checklist

System-level escalation to full literature curation (both components, no planets).
Impact order: rotation > activity > teff/R/L/mass > age > metallicity(skip).

## Luhman 16 A (L7.5)
- [x] mass — multi-source: L&S2018 33.51 MJup (rec) / Bedin2024 35.4 / Garcia2017 34.2 → M☉
- [x] radius — 0.090 R☉ (0.9 R_Jup, Vrba-2004 prescription, Faherty2014); evolutionary_model
- [x] teff — 1310±30 K (Faherty2014, Lbol-derived)
- [x] luminosity — log L/L☉ = -4.67±0.04 (Faherty2014, bolometric)
- [x] age — 0.1-3 Gyr (Faherty2014, Li + no low-gravity); method=unverified, range in notes
- [ ] rotation — P_rot (hr) from variability (Gillon/Crossfield/Apai) — research agent pending
- [n/a] activity — BD too cool for Ca II H&K dynamo; leave empty
- [skip] metallicity

## Luhman 16 B (T0.5)
- [x] mass — L&S2018 28.55 MJup (rec) / Bedin2024 29.4 / Garcia2017 27.9 → M☉
- [x] radius — 0.090 R☉ (0.9 R_Jup, Faherty2014); evolutionary_model
- [x] teff — 1280±75 K (Faherty2014)
- [x] luminosity — log L/L☉ = -4.71±0.10 (Faherty2014)
- [x] age — 0.1-3 Gyr (shared system age)
- [ ] rotation — P_rot (hr); B is the famous cloud-weather variable (~5 hr) — agent pending
- [n/a] activity
- [skip] metallicity

## Apply
- [ ] write measurements.yaml
- [ ] apply_phase2.py luhman_16
- [ ] build_systems + validate (FAIL 0)
- [ ] check.sh green
