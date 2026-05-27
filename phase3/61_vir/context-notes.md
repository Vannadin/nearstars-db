# 61 Virginis Phase 3 — context notes

Append-only decision log. Started 2026-05-27.

## Source inventory (Phase 2 from DB + literature-direct per task)

DB `db/systems/61_vir.json` carries:

- Gaia DR3 astrometry — RA/Dec/parallax/PM/RV all attributed
- Vmag 4.7105 (gaia_dr3_converted)
- Teff 5552 K (Gaia DR3)
- Spectype G6.5V (Gaia label)
- Mass 0.942 ± 0.034 M☉ (Vogt 2010, recommended, "unverified" method tag)
- Radius 0.963 ± 0.011 R☉ (Vogt 2010, recommended, "unverified" method tag)
- distance_pc 8.5344 (Gaia parallax)

DB **does not** carry:

- `age_measurements` — literature-direct: Mamajek & Hillenbrand 2008
  isochrone+activity-age, ~6 Gyr
- `metallicity_measurements` — literature-direct: Bensby 2014 / Brewer
  2016 / Pavlenko 2012: [Fe/H] ≈ −0.02 to +0.00 (solar within errors)
- `rotation_measurements` — literature-direct: Vogt 2010 §4 inferred
  P_rot ≈ 29 d from RV jitter modeling; Wright 2004 chromospheric
  P_rot
- `activity_measurements` — literature-direct: Wright 2004 / Isaacson
  & Fischer 2010 log R'HK ≈ −5.0 (quiet)
- `luminosity_measurements` — derived from R²·(T/5772)⁴ =
  0.963² · (5552/5772)⁴ = 0.794 L☉. Vogt 2010 quotes 0.82 L☉.
  Cite Vogt 2010 directly to match the literature value.
- `disk_measurements` — **absent in DB**. Literature-direct per task
  spec: Wyatt 2012 Herschel-PACS resolved cold ring; Lawler 2014
  ALMA/Herschel SED follow-up; Su 2017 Spitzer+Herschel context.

## Phase 2 escalation note

The task explicitly requests stellar-only synthesis with disk
literature-direct (Wyatt 2012, Lawler 2014, Su 2017). Confidence=low
for disk-tint synth flagged in Decisions Basis column. Open items
section flags Phase 2 disk_measurements ingest as the natural follow-up.

## Step 9.0 — Decisions-row classification

Per SKILL.md Step 9.0 mandatory gate. Each Decisions row labeled as:

- **canonical-aligned** — cfg pick matches canonical reading
- **tie-break** — obs/theory silent within window; cfg picks interesting
- **documented-divergence** — canonical has weight advantage, cfg picks differently

### Stellar Physical (7)

- `spectral_type` = G6.5V → canonical-aligned (Gaia DR3 label; Gray
  2003 G7V also seen — taking the more recent + finer subtype as primary)
- `mass_msun` = 0.942 ± 0.034 → canonical-aligned (Vogt 2010)
- `radius_rsun` = 0.963 ± 0.011 → canonical-aligned (Vogt 2010)
- `teff_k` = 5552 → canonical-aligned (Gaia DR3); Pavlenko 2012 5538
  is consistent within 14 K — well below the Phase 3 precision floor
- `luminosity_lsun` = 0.82 → canonical-aligned (Vogt 2010; my derived
  0.794 is consistent)
- `metallicity_fe_h_dex` = +0.00 ± 0.05 → canonical-aligned (solar twin
  consensus: Pavlenko 2012, Bensby 2014, Brewer 2016)
- `age_gyr` = 6.1 ± 1.7 → canonical-aligned (Mamajek & Hillenbrand 2008
  chromospheric+isochrone combo, the standard solar-twin age for 61 Vir)

### Stellar Activity

- `rotation_period_days` = 29 → canonical-aligned (Wright 2004
  chromospheric P_rot; Vogt 2010 §4 confirms via RV jitter)
- `activity_log_rhk` = −5.0 → canonical-aligned (Isaacson & Fischer 2010
  S_HK catalog; Henry 1996 longer monitoring also ≈−5.0)
- `x_ray_log_lx_cgs_min/max` = 26.7 / 27.0 → canonical-aligned (Schmitt
  & Liefke 2004 NEXXUS-2 catalog: log L_X ≈ 26.7–27.0 cgs)

### Stellar Visual

- `visual_surface_tint_hex_primary` = `#fff2dc` → tie-break (near-solar
  blackbody at 5552 K; cfg picks a slightly creamier tone than Sun's
  `#fff8f0` to give the player a clue this is a slightly cooler G-dwarf)
- `stellar_color_temp_k` = 5552 → canonical-aligned (= Teff)

### Circumstellar disk (Phase 2 absent — literature-direct, marked low)

- `disk_present` = true → canonical-aligned (Wyatt 2012 Herschel-PACS
  resolved excess; confirmed by Tanner et al. 2014 / Lawler context)
- `disk_inner_radius_au` = ~30 AU → canonical-aligned (Wyatt 2012
  Herschel resolved ring); some papers cite ~14–96 AU as the dust
  belt's radial extent at 70/100/160 μm
- `disk_outer_radius_au` = ~96 AU → canonical-aligned (Wyatt 2012
  outer cutoff from SED fit + resolved geometry)
- `disk_dust_temperature_k` = ~50 K → canonical-aligned (Wyatt 2012
  Herschel modified blackbody fit, ~30–60 K range)
- `disk_tint_rgb_hex` = `#9ca4b5` → tie-break (50 K thermal emission
  invisible in optical; cfg picks a cool steel-blue scattering tint
  for visual recognition; Confidence=low documented)
- `disk_opacity` = 0.10 → tie-break (Herschel optical depth τ ~ 10⁻⁵
  in IR; cfg picks a player-visible value scaled for KSP renderer;
  Confidence=low)
- `disk_morphology` = "single cold belt, KBO analog" → canonical-aligned
  (Wyatt 2012)
- `disk_resolved_imaging` = true → canonical-aligned (Wyatt 2012
  Herschel/PACS resolved)
- `disk_imaging_observatory` = "Herschel/PACS (Wyatt 2012)" →
  canonical-aligned
- `disk_mass_mearth` = ~0.07 M⊕ dust mass → canonical-aligned (Wyatt
  2012 quotes ~10× scaled Sun's KBO inventory; later Lawler 2014 / Su
  2017 ~6–8×; task spec gives the 6–8× range — adopt the midpoint)
- `disk_planetesimal_belt_inferred` = true → canonical-aligned (dust
  replenishment requires parent body belt against PR-drag/collisional
  losses; Wyatt 2012 §5)

### Row counts

- canonical-aligned: 17
- tie-break: 3 (visual tint + disk tint + disk opacity)
- documented-divergence: 0

No `## Canonical alternatives` section needed — all divergences are
either canonical-aligned or tie-breaks. Per template policy, **omit**
the section (don't leave an empty placeholder).

## Visual scenario for the renderer

- Solar-yellow G6.5V (slightly cooler/cremier than Sol)
- Cold debris ring visible in orbit view, ~30–96 AU radius, KBO analog
- 3 RV-detected sub-Neptune planets shown as point-of-light foreground

## Bibliography plan

### Read (visual-informative)

- Wyatt et al. 2012 — Herschel resolved cold ring (the primary disk
  paper, the user's "Cold Dust around Nearby Stars" anchor)
- Vogt et al. 2010 — discovery of b/c/d + stellar parameters (mass,
  radius, L, age) — the foundational paper for both the planet and
  star sides
- Mamajek & Hillenbrand 2008 — chromospheric activity-age relation,
  the standard 61 Vir age citation
- Wright et al. 2004 — chromospheric rotation period, S_HK catalog
- Pavlenko et al. 2012 — high-resolution spectroscopy, confirms
  solar-twin status

### Read (context / instrument)

- Tanner et al. 2014 — disk SED+imaging context
- Schmitt & Liefke 2004 — NEXXUS-2 ROSAT X-ray catalog
- Isaacson & Fischer 2010 — California HK catalog refit of log R'HK
- Su et al. 2017 — Spitzer + Herschel cold disk survey (context)
- Bensby et al. 2014 — thin/thick disk kinematics + metallicity sample
- Brewer et al. 2016 — Spectral Properties of Cool Stars (SPOCS), [Fe/H] refit

### Not read

- ~30+ catalog / SETI / interstellar-mission proposal papers (typical
  Phase 3 "not-read" backlog for a Vmag 4.7 naked-eye star with high
  bibcode count)

## Open items snapshot

- Phase 2 `disk_measurements` ingest (Wyatt 2012 + Lawler 2014 + Su
  2017) — currently literature-direct; would upgrade Confidence on
  disk geometry rows from high to high (already high) but documents
  the chain.
- Planets b/c/d Phase 3 follow-up — separate workspace; b is a
  super-Earth (5.1 M⊕, 4.2 d), c/d are warm Neptune-mass (18/23 M⊕,
  38/124 d).
