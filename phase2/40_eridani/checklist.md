# 40 Eridani — Phase 2 Curation Checklist

System: triple star — A (K0.5V) + B (DA white dwarf) + C (M4.5Ve flare star)

> **2026-05-29 status — Tier 2 warm-up rescope.** Original Tier 3 prep was done
> 2026-05-27, BEFORE the 2026-05-28 fabrication patterns were identified.
> All citations and decisions in this file are now **verification candidates**,
> not approved entries. Re-run each row through the new 7-step procedure:
> pre-curation lit search → citation value-check → DOI/abstract fetch →
> multi-layer commit → Phase 2→3 reconciliation → no false-negative claims →
> verification subagent. Tier 2 scope is 40 Eri B + C only; A stays Tier 1
> for later.

## Pre-research

- [ ] Confirm Gaia DR3 IDs (already in target_list — verify still valid)
- [ ] Check NASA Archive for 40 Eri / HD 26965 planets (DONE: not present, refuted)
- [ ] Decide planet treatment (Tau Ceti e precedent: refuted markdown, no curated entry)
- [ ] Identify candidate papers for each measurement category per component

## 40 Eri A — stellar properties (8 categories)

- [ ] Mass — interferometry / asteroseismology / spectroscopic best
- [ ] Radius — interferometry (Boyajian 2012, Rains 2020 priority)
- [ ] Teff — interferometric IRFM > spectroscopic
- [ ] Luminosity — bolometric flux from interferometric SED
- [ ] Age — gyrochronology + isochrone bounds
- [ ] Metallicity [Fe/H] — high-res spectroscopy
- [ ] Rotation period (P_rot) — photometric / activity-derived
- [ ] Activity log R'HK — modern survey value

## 40 Eri B — white dwarf

- [ ] Mass — Bond et al. 2017 HST trigonometric (gravitational redshift / dynamical)
- [ ] Radius — Bond 2017 (HST, asterometric mass-radius)
- [ ] Teff — Holberg 1998 / Bond 2017 UV
- [ ] Luminosity — bolometric
- [ ] Age (cooling age) — Holberg or Bond
- [ ] Metallicity — N/A for DA WD (note exclusion in meta)
- [ ] Rotation — typically not measured for old DA WDs
- [ ] Activity — N/A

## 40 Eri C — M dwarf flare star (DY Eri)

- [ ] Mass — Mann 2019 spectroscopic_calibration / dynamical from BC orbit
- [ ] Radius — Mann 2015 or Boyajian 2012 (interferometric if available)
- [ ] Teff — Mann 2015 photometric or recent spectroscopic
- [ ] Luminosity — Mann 2015 SED fitting
- [ ] Age — inherited from system (~6 Gyr by Bond 2017 from WD cooling)
- [ ] Metallicity — Mann 2015 photometric or recent M-dwarf survey
- [ ] Rotation — photometric P_rot if measured (flare star, fast rotator likely)
- [ ] Activity — log R'HK / H-alpha EW (DY Eri = flare star, very active)

## Binary orbit refresh

- [ ] B-C orbit — check for updates beyond Heintz 1974 (Howard 2023? Mason 2023 WDS?)
- [ ] A-BC outer orbit — confirm still undetermined (legacy not modeled)

## Planet — 40 Eri A b (Vulcan / HD 26965 b)

- [ ] Document refutation: Lubin et al. 2024 — RV signal = stellar activity (P_rot)
- [ ] Create `phase3/tau_cet_planets`-style refuted markdown if applicable
- [ ] Confirm no entry in planets_curated.json

## Pipeline + verify

- [ ] Edit `db/stellar_props_curated.json` with all measurements
- [ ] Update `db/binary_orbits.json` if newer B-C orbit available
- [ ] Run `python3 scripts/pipeline/build_systems.py`
- [ ] Run `python3 scripts/pipeline/validate.py` — confirm FAIL=0
- [ ] Inspect `db/systems/40_eridani_{a,b,c}.json` derived values
- [ ] Verify principia.gravitational_parameter_km3_s2 + mean_radius_km populated

## Commit

- [ ] Single semantic commit: `feat(40-eri): Phase 2 stellar curation (A/B/C) + planet refutation note`
