# Barnard's Star Phase 3 — Context Notes

Append-only decision log. Source of truth for every Decisions-row pick.

## Phase 2 inputs (committed e72ba99)

Stellar (db/systems/barnards_star.json + db/stellar_props_curated.json):
- Teff = 3195 ± 28 K (González Hernández 2024 SED fitting, recommended)
- R = 0.1868 ± 0.0011 R☉ (Rains 2021 CHARA interferometry)
- M = 0.161 ± 0.006 M☉ (Mann 2015 M-K)
- L = 0.003558 ± 7.2e-5 L☉ (González Hernández 2024 bolometric flux)
- [Fe/H] = −0.15 ± 0.16 dex (Marfil 2021)
- Age = 10 ± 2 Gyr (Toledo-Padrón 2019 kinematic, halo membership)
- P_rot = 145 ± 15 d (Toledo-Padrón 2019 photometric)
- log R'HK = −5.69 (Toledo-Padrón 2019; deeply inactive)
- SpType = M4.0 Ve (M-class; "Ve" = emission-line variable M dwarf)

Planets (all RV non-transiting, Msini only):
- d: 0.263 ± 0.024 M⊕, a = 0.0188 AU, P = 2.3402 d, e = 0.04 (hottest)
- b: 0.299 ± 0.026 M⊕, a = 0.0229 AU, P = 3.1542 d, e = 0.03
- c: 0.335 ± 0.030 M⊕, a = 0.0274 AU, P = 4.1244 d, e = 0.08 (most massive)
- e: 0.193 ± 0.033 M⊕, a = 0.0381 AU, P = 6.7392 d, e = 0.04 (coolest, least massive)

Historical: Ribas 2018 reported a super-Earth "b" at 0.4 AU (P = 233 d), refuted by Lubin 2021 (2021AJ....162...61L). The current Barnard b is a different planet that reuses the b letter.

## Derived equilibrium temperatures (Bond albedo A varied)

T_eq = [(L × (1−A)) / (16 π σ a²)]^0.25

With L = 0.003558 L☉ = 1.362e24 W, a in m, σ = 5.67e−8 SI:

- d at 0.0188 AU: S = 10.07 S⊕ → T_eq(A=0) = 496 K, T_eq(A=0.1) = 483 K, T_eq(A=0.3) = 453 K
- b at 0.0229 AU: S = 6.79 S⊕  → T_eq(A=0) = 449 K, T_eq(A=0.1) = 438 K, T_eq(A=0.3) = 411 K
- c at 0.0274 AU: S = 4.74 S⊕  → T_eq(A=0) = 411 K, T_eq(A=0.1) = 400 K, T_eq(A=0.3) = 376 K
- e at 0.0381 AU: S = 2.45 S⊕  → T_eq(A=0) = 348 K, T_eq(A=0.1) = 339 K, T_eq(A=0.3) = 319 K

All four are hot rocky planets, well inside any conservative HZ for a 3195 K M4 (Kopparapu 2014 inner HZ at ~0.1 AU). e at 2.45 S⊕ sits close to Venus's 1.9 S⊕ — borderline Venus-analog territory, NOT habitable. Note: planet d is hotter than b despite the task spec's reversed labeling — verified against db/systems/barnards_star.json (d at 0.0188 AU is closer than b at 0.0229 AU).

## Angular diameters from each planet

Star angular = 2 × R★/a × (180/π)
- d: 2 × 0.1868 R☉ × 6.96e8 m / 2.812e9 m × (180/π) = 5.30°
- b: 4.34°
- c: 3.63°
- e: 2.61°

## Bond albedo policy

Rocky no-atmosphere: Mercury 0.12; lunar 0.11; the cfg uses 0.10–0.15 range.
Partial-melt magma surface: 0.05–0.08 (Stamenković ApJ).
Fully airless dark basalt: 0.06–0.08.

## Magnetic environment

Barnard is exceptionally quiet for an M4: log R'HK = −5.69, more inactive than the Sun. Reiners 2022 (CARMENES) measured B ~ 200 G mean field for Barnard's Star. Toledo-Padrón 2019 found no significant rotational modulation peak in optical activity tracers within their dataset baseline (rotation showed up only weakly at 145 d).

This contrasts sharply with Proxima Cen (log R'HK = −4.0, B ~ 4 kG, frequent superflares). Barnard's atmosphere retention prospects are much better than Proxima's per Bourrier 2017 / France 2020 XUV scaling.

## Ribas 2018 retraction handling

Per task spec: cite Ribas 2018 historically/contextually, NOT as a current measurement. Lubin 2021 is the canonical refutation. The current "b" designation refers to González Hernández 2024 P=3.15 d planet (different planet).

## Tie-break vs divergence framework reminders

- canonical-aligned: cfg pick matches paper consensus
- tie-break: literature is silent / multiple valid values within window → pick visually interesting
- documented-divergence: paper has clear weight but cfg picks differently → requires `## Canonical alternatives` section

For Barnard b/c/d/e, the radius/composition/atmosphere/surface decisions are nearly all tie-break (no transits, no JWST yet, all post-2024 discoveries with no follow-up GCM modeling). The Mercury-analog template applies broadly.

## Deep-read findings

### González Hernández 2024 (2410.00569) — ESPRESSO discovery of Barnard b
- 156 ESPRESSO observations over 4 years; GP modeling of stellar activity
- Confirms b at P=3.1533±0.0006 d, a=0.0229±0.0003 AU, Msini=0.37±0.05 M⊕ (later refined to 0.299 by Basant 2025)
- T_eq(b) = 400 K assuming zero albedo and full heat redistribution
- Refutes Ribas 2018 233-d super-Earth (no signal in ESPRESSO data)
- Activity: long-term cycle ~3200 d (~9 yr), rotation 140 d, second harmonic 71 d

### Basant 2025 (2503.08095) — MAROON-X confirmation of 4-planet system
- 112 MAROON-X RVs at 30 cm/s precision, contemporaneous with ESPRESSO
- Confirms b independently; promotes c, d, e to confirmed/strong candidate
- Table 3 (recommended values): all from β[1.52, 29] prior eccentricity distribution
  - b: P=3.1542 d, a=0.0229 AU, Msini=0.299 M⊕, T_eq=438 K (A=0, full redistribution)
  - c: P=4.1244 d, a=0.0274 AU, Msini=0.335 M⊕, T_eq=400 K
  - d: P=2.3402 d, a=0.0188 AU, Msini=0.263 M⊕, T_eq=483 K
  - e: P=6.7392 d, a=0.0381 AU, Msini=0.193 M⊕, T_eq=340 K
- Stability: 10⁹ orbits of inner planet at zero ecc; e<0.02 favored for long-term stability
- HZ inner edge at P=10 d (a ≈ 0.115 AU per Kopparapu 2014)
- Rules out planets > 0.37-0.57 M⊕ in HZ (P=10-42 d)

### Toledo-Padrón 2019 (1812.06712)
- P_rot = 145 ± 15 d from chromospheric indicators (Hα, Ca II HK, Na I D, CCF FWHM)
- 14.5-year RV baseline (HARPS, HARPS-N, CARMENES, HIRES, UVES, APF, PFS)
- Long-term magnetic cycle 10 ± 2 yr
- log R'HK = −5.69 (extremely inactive; lower than the Sun at minimum)
- Predicted activity-induced RV signal at P_rot ≈ 1 m/s upper limit

### Cristofari 2024 (2310.12125) — SPIRou NIR spectroscopy
- 846 visits, S/N > 2500 in H band, 2018–2023
- T_eff = 3231 ± 21 K (NIR line-group method)
- T_eff = 3238 ± 11 K (interferometric, Boyajian 2012 + Rains 2021 R)
- log g = 5.08 ± 0.15 (NIR spectroscopy)
- 15 element abundances incl. K, O, Y, Th (4 new vs prior literature)
- Many lines in observed spectrum not in PHOENIX-ACES models — model incompleteness

### Duvvuri 2021 (2102.08493) — DEM EUV reconstruction
- Mega-MUSCLES sample includes Barnard
- Quiescent EUV (100–912 Å) integrated flux = 0.018 erg/cm²/s at 1 AU
- Flaring EUV = 0.146 erg/cm²/s at 1 AU (~10× increase)
- Adopted [Fe/H] = −0.32 (Ribas 2018), spectype M4
- Quiescent S/N very low; large uncertainties

### France 2020 (2009.01259) — Mega-MUSCLES "Habitable at Last?"
- HST + Chandra observations
- Detected 2 FUV flares (~10²⁹·⁵ erg each, δ_130 ≈ 5000 s) and 1 X-ray flare (~10²⁹·² erg)
- Flare duty cycle ≈ 25% (high for an old M dwarf)
- Quiescent XUV does NOT drive strong atmospheric escape — comparable to modern-Earth solar-max
- Flare environment DOES drive hydrodynamic loss: ~87 Earth-atm/Gyr (thermal) + ~3 Earth-atm/Gyr (ion loss)
- HZ at ~0.1 AU; old-M-dwarf secondary atmosphere retention is feasible IF planet survived initial 5 Gyr
- "Habitable at last" framing: contrast with young flaring M-dwarfs

## Step 9.0 Pre-draft classification

### Barnard's Star (stellar)
- spectral_type M4.0 V (variable, not always Ve given log R'HK = −5.69) → canonical-aligned
- mass 0.161 ± 0.006 M☉ → canonical-aligned (Mann 2015 DB recommended)
- radius 0.1868 ± 0.0011 R☉ → canonical-aligned (Rains 2021 CHARA)
- teff 3195 ± 28 K → canonical-aligned (González Hernández 2024; lower than Cristofari 2024's 3231 K — within 1.5σ; DB recommended)
- luminosity 0.003558 L☉ → canonical-aligned (González Hernández 2024)
- metallicity −0.15 ± 0.16 → canonical-aligned (Marfil 2021; Cristofari uses −0.5 dex as model input, Duvvuri uses Ribas −0.32; broad range)
- age 10 ± 2 Gyr → canonical-aligned (Toledo-Padrón 2019 halo kinematic)
- rotation 145 ± 15 d → canonical-aligned (Toledo-Padrón 2019)
- activity log R'HK = −5.69 → canonical-aligned (Toledo-Padrón 2019)
- activity cycle 10 ± 2 yr → canonical-aligned (Toledo-Padrón 2019; González Hernández 2024 finds 3200 d ≈ 8.8 yr — within window)
- x_ray quiescent log L_X = 25.5 → tie-break (France 2020 single Chandra detection; uncertainty large)
- x_ray flare peak log L_X = 27.5 → tie-break (France 2020 ~10²⁹·² erg per event, ~5000 s duration)
- flare_duty_cycle = 0.25 → canonical-aligned (France 2020)
- magnetic_total_field_G = 200 → tie-break (Reiners 2022 CARMENES ~ 200 G; SPIRou polarimetry available but specific Stokes V dipole strength not extracted to abstract level)
- flare rate ~ low — tie-break (no large dataset; ~few flares per month from France 2020 implies)
- visual surface tint hex — tie-break (M4.0V deep red, sub-solar [Fe/H] slight blue shift)
- limb_darkening — tie-break (M-dwarf grid interpolation)

### Barnard b/c/d/e (planets)
Most planet-level decisions are tie-break because:
- No transits → radius, density, composition unmeasured
- Mass is Msini only (true mass can be larger if low inclination)
- No atmospheric observations (JWST hasn't observed any of these yet)
- Post-2024 discoveries → no follow-up GCM modeling published
- The Mercury-analog template (used for Proxima d) applies broadly

Per planet, the canonical-aligned decisions are: orbital params from Basant 2025; Msini; T_eq (full redistribution); insolation; tidally_locked (high confidence given P<7d, tidal damping); obliquity (damped).

Surface/atmosphere/visual decisions are tie-break given the literature silence. None require divergence section since there's no canonical contradiction — just absence of canonical predictions.

Specific picks summary:
- All 4 planets: bare-rock dominant surface, vestigial atmospheres at most, tidally locked
- d (hottest at T_eq=483 K, S=10 S⊕): substellar partial-melt visible; iron-oxidized basalt
- b (T_eq=438 K, S=6.8 S⊕): bare basaltic rocky; possible sodium exosphere
- c (T_eq=400 K, S=4.7 S⊕): bare rocky; minimal volatile retention
- e (T_eq=340 K, S=2.45 S⊕, closest to HZ inner edge): borderline Venus-analog; thicker exosphere plausible; only one of 4 to potentially retain modest atmosphere

Reporting row counts after drafting in synthesis-output.
