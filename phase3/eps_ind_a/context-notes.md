# eps Ind A — Phase 3 context notes

Append-only decision log. Synthesis from frozen Phase 2 (db/systems/eps_ind_a.json)
+ cached papers in docs/phase3/_papers/. NO live network. NO db edits.

## Verified Phase 2 inputs (db/systems/eps_ind_a.json)

### Stellar (eps Ind A)
- spectype: K5 V (raw.spectype "K5 V"); Lundkvist 2024 title "K5 V star eps Indi A"
- mass_msun: 0.782 ± 0.023 (Lundkvist 2024 asteroseismology, recommended); alt 0.762 ± 0.038 (Demory 2009)
- radius_rsun: 0.713 ± 0.006 (Lundkvist 2024, theta_LD 1.817 mas Rains 2020 + Gaia d=3.648 pc)
- teff_k: 4700 ± 65 (Lundkvist 2024 high-res spectroscopy, UVES)
- luminosity_lsun: 0.239 ± 0.001 (Feng 2019 bolometric flux)
- age: NO Phase 2 age array (age_measurements empty); derived.age_gyr = null
  - literature (context only): 3.48 (+0.78/-1.03) Gyr Chen 2022 (activity, log R'HK -4.72 Pace 2013 + ROSAT R_X -5.62);
    ~4 Gyr Feng 2019; Cardoso 2012 3.7-4.3 Gyr; Lundkvist intro range 0.39-5 Gyr unresolved
- metallicity: NO Phase 2 array; literature [Fe/H] = -0.17 (Lundkvist 2024 UVES), -0.06 Santos 2004 (via Matthews 2026). Skipped per project policy.
- rotation_period_days: 35.0 (Feng 2018, "unverified" method — RV + activity-index periodograms;
  17.8 d is half-rotation alias; supersedes 22 d Saar&Osten 1997, ~20 d Lachaume 1999). No formal sigma.
- activity_log_rhk: -4.72 (Chen 2022 adopting Pace 2013). recommended.
- activity cycle: ~2600 d ≈ 7.1 yr (Lundkvist 2024 §4.3, HARPS archival log R'HK phase-fold). Context.
- distance: Gaia DR3 parallax 274.84 mas -> 3.638 pc (derived) = 11.87 ly. vmag V=4.66 (Gaia converted) — naked-eye.

### Planet b (eps Ind A b) — Matthews 2026 anchor (arXiv 2603.08780, ApJL doi 10.3847/2041-8213/ae5823)
- true_mass: 7.63 (+0.73/-0.70) MJup = 2425 ± 232 M_earth (curated recommended); alt 1033 M_earth Feng 2019 (~3.25 MJup astrometric), 861 Msini Feng 2018
- a: 20.9 (+5.8/-3.3) AU (Matthews 2026); alt 11.55 Feng 2019, 12.82 Feng 2018
- e: 0.244 (+0.11/-0.083) (Matthews 2026); curated uncertainty 0.11
- i: 102.3 (+1.9/-1.7) deg (Matthews 2026)
- Omega (lon asc node): 44.6 ± 1.3 deg (Matthews 2026)
- omega (arg peri): 62 (+48/-27) deg (Matthews 2026)
- P: 108 (+49/-25) yr (derived; curated period_days 39447 ± 17897 ≈ 108 yr). Brief says "~200 yr"; paper MAP best-fit ~110 yr, median 108 yr. Use ~108 yr (paper), note historical 45 yr Feng 2019.
- radius: 12.6 R_earth (DB raw/derived) = 1.12 RJup. mass_type true mass.
- atmosphere (Matthews 2026): ammonia NH3 CONFIRMED (F1065C-F1140C = 0.88 ± 0.08 mag, 11 sigma);
  feature SHALLOWER than cloud-free solar-metallicity models -> preferred explanation THICK WATER-ICE CLOUDS
  (best-fit PICASO/Virga: 275 K, log g 4.5, 3x solar [M/H], 2.5x solar C/O, Kzz 1e9, fsed 6;
  H2O cloud column optical depth 416, tau=1 near 0.7 bar). Faint at 3-5 um (NaCo non-detection).
  Alt explanations: low metallicity (rejected — conflicts L' non-detection) or N-depletion 85-95% (possible but extreme).

### Effective temp vs equilibrium temp — CRITICAL distinction
- Matthews 2026 abstract: "cold (~200-300 K), solar-age giant"; Eps Ind Ab "~275 K planet first imaged by Matthews 2024".
  275 K is the EFFECTIVE / atmosphere temperature — dominated by INTERNAL HEAT (gravitational contraction of a 7.6 MJup
  self-luminous young-ish giant), NOT stellar insolation.
- Radiative-equilibrium temp from starlight alone (derived): T_eq(A=0) = 278.3 * 0.239^0.25 / sqrt(20.9) = 42.6 K;
  T_eq(A=0.3) = 38.9 K. At peri (15.8 AU) 49 K, at apo (26.0 AU) 38 K.
- So: insolation S = L/a^2 = 0.239/20.9^2 = 5.5e-4 S_earth (~0.55 mS_earth) — negligible.
  The planet's observed ~275 K is set by self-luminosity. This is why "T_eq ~0-275 K" in the brief: equilibrium ~40 K,
  but the body radiates at ~275 K from internal heat. Both reported; do NOT introduce un-sourced numbers.

### Derived planet b quantities (shown derivations, not new sourced numbers)
- surface gravity: log g = 4.18 cgs (g = G*7.63MJup / (12.6 Rearth)^2 = 1.50e3 cm/s^2 = 15.3 g_earth).
  Matthews best-fit log g 4.5 is for a smaller-radius model fit; the DB radius 12.6 Rearth gives log g 4.18. Report derived from DB R.
- insolation_s_earth = 0.00055 (L/a^2)
- equilibrium_temp_k_a0 = 43; _a03 = 39 (derived)
- star angular diameter from b = 1.09 arcmin = 0.018 deg (2 R*/a) ≈ 0.034x Sun-from-Earth
- radius 1.12 RJup (12.6/11.21)

### Related bodies (mention only — NO doc/db created)
- eps Ind B = brown-dwarf binary at ~1459 AU (Scholz 2003 / Feng 2019) from A:
  - Ba: T1-1.5, 66.92 ± 0.36 MJup (Chen 2022 dynamical)
  - Bb: T6, 53.25 ± 0.29 MJup (Chen 2022 dynamical)
  - system total ~121 MJup; benchmark L/T-transition brown dwarfs (slowed cooling)

### NO debris disk — eps Ind A has none reported. disk_present=false. Do NOT fabricate.

## Step 9.0 Decisions-row classification

### Stellar (eps-ind-a.md)
- spectral_type K5V — canonical-aligned (DB / Lundkvist 2024)
- mass/radius/teff/luminosity — canonical-aligned (Phase 2 recommended)
- metallicity null — canonical-aligned (skip policy; literature -0.17/-0.06 context)
- age_gyr ~3.5 — canonical-aligned (Chen 2022 activity; no Phase 2 array so Confidence medium/low, literature-direct)
- rotation_period_days 35 — canonical-aligned (Feng 2018, medium: unverified method, no sigma)
- activity_log_rhk -4.72 — canonical-aligned (Chen/Pace)
- activity_cycle_years ~7.1 — canonical-aligned (Lundkvist 2024, medium)
- visual_surface_tint_hex — tie-break (K5V 4700 K blackbody render)
- stellar_color_temp_k 4700 — canonical-aligned (= Teff)
- disk_present false — canonical-aligned (no disk reported)
- companion_brown_dwarf_pair — canonical-aligned (Chen 2022)
Count: 11 canonical-aligned, 1 tie-break, 0 divergence. NO Canonical alternatives section.

### Planet b (eps-ind-a-b.md)
- orbital (a/e/i/Omega/omega/P/mass/radius) — canonical-aligned (Matthews 2026 / DB)
- tidally_locked false — canonical-aligned (20.9 AU, tidal timescale >> age)
- effective_temp_k ~275 — canonical-aligned (Matthews 2024/2026)
- equilibrium_temp_k_a0 ~43 — canonical-aligned (derived; shows insolation is negligible)
- internal-heat-dominated — canonical-aligned (Matthews; self-luminous)
- atmosphere ammonia confirmed — canonical-aligned (Matthews 2026, 11 sigma)
- water-ice clouds present — canonical-aligned (Matthews 2026 preferred explanation; Confidence medium — "suggested"/preferred not proven)
- atmosphere_composition (H2/He + NH3 + H2O clouds, elevated C/O + [M/H]) — canonical-aligned (Matthews best-fit) / partly tie-break for exact mixing ratios
- cloud/atmosphere tint hex (cold pale methane/ammonia-class palette) — tie-break (interesting-first within cold-giant window)
- ring_present false (default) — canonical-aligned (not observed)
- ring artistic OPTION — tie-break, preserved in Open items + flagged "not observed"; cfg default false
- rotation_period_hours — tie-break (no measurement)
- obliquity/magnetic — tie-break
Count: most canonical-aligned (the orbit + atmosphere are MEASURED, unlike eps-eri-b), several tie-break (palette, rotation, ring option). 0 documented-divergence. NO Canonical alternatives section.

## Completion (2026-05-31)
- Wrote 4 files: docs/phase3/eps-ind-a.md (+ko), docs/phase3/eps-ind-a-b.md (+ko)
- Block parity: project check_block_parity.py reports [OK] both (eps-ind-a 37, eps-ind-a-b 39 paired)
- Korean: no closing-colon leaks (trailing or mid-sentence Hangul+colon)
- No build/check.sh/git/db edits run (per hard constraints)
- NO fabricated disk; disk_present=false everywhere; brown-dwarf pair mentioned only (no doc/db created)
