<!-- Phase 3 항성풍/astrosphere 합성 설계 노트 — 결정 사항과 물리 근거 -->
# Stellar-wind / astrosphere Phase 3 synthesis — context notes

Scope: synthesize cfg-ready stellar-wind fields from the Phase 2 measurements
(`mass_loss`, `magnetic_field`, `activity_cycle`) + L + 6D astrometry, for the
Kerbalism radiation layer. Two write targets:
- ② field spec → `nearstars-phase3/references/mod-grounded-fields.md` (new
  "Kerbalism stellar wind / astrosphere" section).
- ① per-star values → `docs/phase3/<host>.md` Decisions table (+ ko + HTML).

See `[[project-nearstars-stellar-wind-kerbalism]]` for the reverse-engineered
Kerbalism mechanism and the heliotail-plugin decision.

## Kerbalism stellar model (grounded in Radiation.cs, prior session)
A star is a `RadiationBody` with:
- `radiation_surface` (rad/h) — inverse-square wind/cosmic dose. Sun (ROKerbalism) = 46.5.
- `solar_cycle` (s) — Sun = 11 yr.
- a heliopause pause: large `pause_radius` (Sun = 1000 R☉), negative `radiation_pause`
  = a SHIELD (the heliosphere blocks galactic cosmic rays).
- NO belts on stars (belts are planetary).
- Heliotail aim = `gsm.x_axis` = body→reference vector. Self-referencing star →
  fixed world (1,0,0). Stock cfg CANNOT aim a per-star tail → Harmony plugin only.

## Synthesis fields + derivations
1. **solar_cycle_yr** = `activity_cycle_yr` (Phase 2) directly. flat star (τ Cet) →
   no modulation (omit / set very long). High confidence (measured).
2. **astrosphere_standoff_au** (heliopause-analog nose distance, the GCR-shield radius):
   ram-pressure balance r_ap ∝ sqrt(Ṁ·v_w / (n_ISM·V_ISM²)). With v_w = 400 km/s
   (Wood's universal assumption) and LIC n_ISM common to all nearby stars, this reduces to
   **r_ap,star = 120 AU · sqrt(Ṁ_rel) · (V_ISM,⊙ / V_ISM,star)**, anchored on the
   Sun's ~120 AU heliopause and V_ISM,⊙ ≈ 26 km/s.
   - V_ISM per star: Wood 2005 Table 1 where measured (αCen 25, ε Ind 68, Proxima 25
     km/s); else = |v_star − v_LIC| from 6D astrometry (same calc as the apex below).
   - Worked checks: αCen √2·(26/25)=1.47 → ~176 AU; ε Ind √0.5·(26/68)=0.27 → ~32 AU
     (Wood explicitly calls ε Ind a "compact astrosphere" → formula validated);
     Proxima √0.2·1.04=0.47 → <56 AU (upper bound, Ṁ is a limit).
   - Ṁ upper limits → standoff is an upper bound (note `limit`).
3. **stellar_radiation_surface_relative_sun** (×Sun, 1.0 ≡ 46.5 rad/h): the SOFTEST
   field. Crew dose is driven by SEP/flares (not steady wind), which correlate with
   activity. Anchor on Sun=1.0; scale by activity. CAVEAT: log R'HK is FGK-calibrated
   and badly underrepresents M-dwarf flares — Proxima looks "inactive" in R'HK (−5.65)
   but is a violent flare star → its radiation_surface is HIGH, not low. Use flare/X-ray
   reasoning for M dwarfs, R'HK for FGK. Confidence = low–medium (interesting-first,
   anchored). Per-host: αCen ~1 (solar-like), τ Cet/Barnard/40 Eri/ε Ind ≲1 (inactive
   old dwarfs), Proxima ≫1 (flares).
4. **astrosphere_apex_ra_deg / _dec_deg** (upwind/nose direction): from 6D astrometry,
   apex = direction of −(v_star − v_LIC) (the ISM inflow the star sees). LIC flow
   ≈ 26 km/s from (l,b) per Lallement & Bertin 1992. The downwind (tail) = opposite.
   **PLUGIN-ONLY** — stock cfg renders only a sphere; the Harmony plugin patches
   `Radiation.Gsm_space` gsm.x_axis to this vector. Beyond the LIC (~>5 pc) → fall back
   to LSR-relative velocity (approximate).
5. **local_ism_inflow_speed_kms** (V_ISM) = |v_star − v_LIC|; feeds (2) and is the apex speed.
6. **stellar_wind_speed_kms** = 400 (assumed, Wood) unless measured.

## Source priority
1. Wood astrospheric Lyα (gives Ṁ + V_ISM + θ directly): αCen/Proxima (Wood 2001/2005),
   ε Ind (Wood 2005), Barnard/τ Cet (Wood 2021 limits).
2. Compute V_ISM + apex from the star's 6D astrometry vs the LIC vector.
3. Ṁ from Phase 2 mass_loss; solar_cycle from Phase 2 activity_cycle.
4. radiation_surface from activity level (interesting-first, Sun-anchored).

## Open / deferred
- radiation_surface absolute calibration is weak (no curated L_X). Treat as
  confidence=low until an X-ray/flare-rate sweep is done.
- Stars without Ṁ (40 Eri A, Fomalhaut): astrosphere size unconstrained → either
  estimate from activity-wind scaling or omit standoff (note as such).
- emit (kerbalism-cfg writer skill) converts these physical fields to cfg units
  (pause_radius in star-radii, solar_cycle in s); NOT this step.
