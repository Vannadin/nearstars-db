# Tau Ceti Phase 3 — context notes

Stellar-only synthesis. Planets f/g/h Phase 3 deferred to a follow-up
workspace. Tau Ceti e is not in NS DB (see rex-data-comparison §6) and
its curation revisit is logged as an Open item.

## Decisions-row classification

Total: 22 rows.

### Stellar Physical (7)
- spectral_type = G8V                  → canonical-aligned (Gray 2006 + SIMBAD)
- mass_msun = 0.783 ± 0.012            → canonical-aligned (Feng 2017 from MK relation; Teixeira 2009 asteroseismic 0.783 agrees)
- radius_rsun = 0.793 ± 0.004          → canonical-aligned (Teixeira 2009 asteroseismic + Di Folco 2007 interferometry)
- teff_k = 5344 ± 50                   → canonical-aligned (Pavlenko 2012; Santos 2013 agrees within 1σ)
- luminosity_lsun = 0.457              → canonical-aligned (derived R + Teff via Stefan–Boltzmann)
- metallicity_fe_h_dex = -0.55 ± 0.05  → canonical-aligned (Pavlenko 2012; Santos 2013 = -0.49 within 1σ)
- age_gyr = 7.0 ± 1.5                  → canonical-aligned (Pavlenko 2012 super-population kinematics + Mamajek 2008 gyrochronology agree on 6–8 Gyr)

### Stellar Activity (3)
- rotation_period_days = 34            → canonical-aligned (Baliunas 1996 Ca II H&K timeseries, refined by Pavlenko 2012)
- activity_log_rhk = -4.95             → canonical-aligned (Pavlenko 2012; one of the most inactive G dwarfs in HK survey)
- x_ray_log_lx_cgs ≤ 26.5              → canonical-aligned (Schmitt 1985 EXOSAT non-detection upper limit; Judge 2004 confirms quiescent)

### Stellar Visual (2)
- visual_surface_tint_hex_primary = #ffe9c8 (cream-yellow, slightly less yellow than Sol due to metal-poor SED)  → tie-break (metal-poor → bluer continuum at fixed Teff; interesting-first per skill rules)
- stellar_color_temp_k = 5344          → canonical-aligned (= Teff)

### Circumstellar disk (10)
- disk_present = true                  → canonical-aligned (Greaves 2004 SCUBA + MacGregor 2016 ALMA)
- disk_inner_radius_au ≈ 6             → canonical-aligned (MacGregor 2016 ALMA fit)
- disk_outer_radius_au ≈ 55            → canonical-aligned (MacGregor 2016 ALMA fit)
- disk_dust_temperature_k ≈ 60         → canonical-aligned (MacGregor 2016 SED + Greaves 2004 60–80 K)
- disk_tint_rgb_hex = #b8aa9c (warm grey-brown, metal-poor analog of Kuiper Belt)  → tie-break (composition not directly measured; KBO analog with metal-poor parent star → slightly less reddened than Sol KBO)
- disk_opacity = 0.15                  → tie-break (optical depth ~ 10⁻³ inferred from dust mass + geometry; in-game visibility cfg uses 0.15 for visual register)
- disk_morphology = "broad single ring, metal-poor analog of Kuiper Belt"  → canonical-aligned (MacGregor 2016 explicitly favors single broad ring over multi-belt)
- disk_resolved_imaging = true         → canonical-aligned (MacGregor 2016 ALMA)
- disk_imaging_observatory = "ALMA"    → canonical-aligned
- disk_mass_mearth ≈ 1.2               → canonical-aligned (MacGregor 2016 fit; ~10–20× Sol KBO dust mass)
- disk_planetesimal_belt_inferred = true  → canonical-aligned (MacGregor 2016 §5 collisional cascade requires parent body belt)

### Counts
- canonical-aligned: 18
- tie-break: 4 (visual surface tint, disk tint, disk opacity, disk morphology label is partly inferred)
- documented-divergence: 0

No `## Canonical alternatives` section needed.

## Key decisions

1. **age_gyr = 7.0 ± 1.5**. Pavlenko 2012 cites Eggen 1971 super-population kinematics (member of an old disk population) + chromospheric activity proxy → 6–8 Gyr. Mamajek 2008 gyrochronology agrees on the lower end (~6.5 Gyr from 34 d period). Pick midpoint 7.0 with ±1.5 to span the range.

2. **metallicity_fe_h_dex = -0.55**. Pavlenko 2012 is the headline value. Santos 2013 = -0.49 ± 0.05 is within 1σ but uses a different model atmosphere; Pavlenko's is preferred because the differential analysis to the Sun is cleaner. Either value puts τ Cet at the metal-poor extreme of nearby G dwarfs.

3. **rotation_period_days = 34**. Baliunas 1996 Mt Wilson HK survey originally measured 34 d. Pavlenko 2012 confirms it via combined HK and photometric data. Some recent papers cite 46 d (Boro Saikia 2018 from ZDI), but the 34 d HK-traced value is canonical and matches the period implied by activity level + age via Skumanich braking.

4. **Visual tint**. Metal-poor stars at fixed Teff have slightly more H-rich SED (less line blanketing in the blue) → continuum looks marginally bluer than a solar-metallicity G8V. Interesting-first rule says pick `#ffe9c8` (cream-yellow, less yellow than Sol `#fff4e8`) and document in Basis. This is the same tie-break shape as alpha-centauri-a but in the opposite direction (alpha Cen A is metal-rich → warmer cream; tau Cet is metal-poor → cooler cream).

5. **Disk geometry**. MacGregor 2016 ALMA Band 6 image shows a broad single ring from ~6 to ~55 AU peaked around 30 AU. Greaves 2004 SCUBA detection was the discovery but resolved as a fuzzy excess; ALMA pins the geometry. Single-ring morphology (no inner gap below the noise floor) → planet roster (f at 1.33 AU, g at 0.13 AU, h at 0.24 AU) all interior to the disk; no planetesimal-clearing planet at intermediate radii is inferred.

6. **Disk tint**. Composition not directly measured. Default assumption is silicate + ice grains (KBO analog), but the metal-poor parent star likely formed a disk with slightly less iron-rich (less reddened) grains than the Sun's KBO. Pick `#b8aa9c` (warm grey-brown, between Sol-KBO `#a08470` reference and a more achromatic grey) as tie-break. Document in Basis as "metal-poor KBO analog".

## Notes for downstream Kopernicus cfg writer

- Disk Kopernicus Ring: inner = 6 AU, outer = 55 AU, mid-color `#b8aa9c`, opacity 0.15, no opacity gradient (single broad ring). Attach to tau Cet body.
- Star color: `#ffe9c8` for renderer; color temp 5344 K for illumination.
- No flare animation needed (quiet star, log L_X ≤ 26.5).
- Planet roster (f/g/h) cfg from a follow-up Phase 3 — not in this synthesis.
