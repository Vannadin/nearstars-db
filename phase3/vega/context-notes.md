# Vega Phase 3 — context notes

## 2026-05-27 — Synthesis via batch retrofit

Vega was synthesized as one of 8 disk-host stars in the
`phase3/circumstellar-disk-schema` workspace. A general-purpose
sub-agent drafted the English markdown from cited literature;
main session ran Step 10 VERIFY (paper bibcodes + known values
cross-check), wrote the Korean mirror, and built HTML.

Phase 2 disk_measurements absent from `db/systems/vega.json`.
Per the documented policy, all disk Decisions rows cite literature
directly (paper + year + bibcode) rather than the DB; Confidence
labels capture the precision (high for resolved-imaging geometry,
medium for SED-fit parameters, low for synth-only fields like
tint hex and opacity).

## Decisions-row classification

Per [`conflict-resolution.md`](../../.claude/skills/nearstars-phase3/references/conflict-resolution.md)
§ "Tie-break vs. divergence":

- `spectral_type = A0Va` → canonical-aligned
- `mass_msun = 2.135 ± 0.075` → canonical-aligned
- `radius_rsun (equatorial) = 2.726 ± 0.006` → canonical-aligned
- `teff_k (effective) = 9692` → canonical-aligned
- `luminosity_lsun = 47 ± 5` → canonical-aligned
- `metallicity_fe_h_dex = -0.5` → canonical-aligned (λ Boo photospheric depletion)
- `age_gyr = 0.455 ± 0.013` → tie-break (Yoon 2010 vs Monnier 2012 0.7 Gyr; both within-window; cfg picks Yoon as headline, Monnier preserved in Open items)
- `rotation_v_eq_km_s = 274 ± 14` → canonical-aligned
- `rotation_period_hours (equatorial) = 12.5` → canonical-aligned (derived)
- `limb_darkening_alpha_h = n/a` → canonical-aligned (Vega is not parameterized this way; gravity-darkening β is the relevant cfg field)
- `visual_gravity_darkening_pole_equator_temp_diff_k = 2250` → canonical-aligned
- `visual_surface_tint_hex_primary = #cfe0ff` → tie-break (interesting-first; emphasize hot pole over area-averaged blackbody)
- `stellar_color_temp_k = 9692` → canonical-aligned (derived)
- `visual_pole_on_inclination_deg = 6.2 ± 0.3` → canonical-aligned
- `activity_log_rhk = n/a` → canonical-aligned (A0V has no chromosphere)
- `disk_present = true` → canonical-aligned
- `disk_inner_radius_au = 14 (warm); 62 (cold inner edge)` → canonical-aligned (Su 2013 two-belt fit)
- `disk_outer_radius_au = 200 ± 20` → canonical-aligned (Sibthorpe 2010)
- `disk_dust_temperature_k = 170 (warm); 50 (cold)` → canonical-aligned
- `disk_tint_rgb_hex = #ffd9a8 / #ffe4b8` → tie-break (HST-STIS palette convention for invisible thermal dust)
- `disk_opacity = 0.06 / 0.02` → tie-break (physical τ ~ 10⁻⁴ boosted for in-game visibility; conservative preserved in Open items)
- `disk_morphology = two-belt + cleared gap` → canonical-aligned (Su 2013)
- `disk_resolved_imaging = true` → canonical-aligned
- `disk_imaging_observatory = IRAS→SCUBA→Spitzer→Herschel→ALMA` → canonical-aligned
- `disk_imaging_inclination_deg = 6.2` → canonical-aligned (locked to stellar pole-on)
- `disk_mass_mearth = 0.013 (cold) + 0.0003 (warm)` → canonical-aligned (Su 2013 dust mass)
- `disk_planetesimal_belt_inferred = true` → canonical-aligned (PR-drag lifetime ≪ system age)

Totals: 23 canonical-aligned, 3 tie-break (age, surface tint hex, disk tint+opacity), 0 documented-divergence. No `## Canonical alternatives` section needed.

## Step 10 VERIFY pass

Spot-checks against well-known literature values:

- Aufdenberg 2006 CHARA v_eq=274 km/s, T_pole=10150 K, T_eq=7900 K, i ≈ 5° — confirmed match
- Monnier 2012 CHARA/MIRC R_eq=2.726 R☉ — confirmed match
- Yoon 2010 M=2.135 M☉, age 0.455 Gyr, [M/H]=-0.5 — confirmed match
- Su 2013 two-belt 14 + 62–200 AU — confirmed match
- Sibthorpe 2010 Herschel-PACS outer 200 AU — confirmed match
- Aumann 1984 IRAS discovery — confirmed match
- Petit 2010 ~0.6 G longitudinal field, ZDI 0.732 d — confirmed match
- Hurt 2021 0.6-day RV candidate at 0.04 AU — confirmed match
- Robrade 2011 X-ray log L_X 25.5–26 — confirmed match

All 9 spot-checks pass. No row contradicts a well-known fact.

## Open items

- **Phase 2 `disk_measurements` ingest needed.** `db/systems/vega.json` has no `disk_measurements` block — every disk Decisions row currently cites literature directly rather than the DB. A Phase 2 refresh pass should add `disk_measurements` entries citing Su 2013, Sibthorpe 2010, Hughes 2012, and Holland 1998 with `recommended: true` on the Su 2013 two-component fit.
- **Age disagreement Yoon 2010 (0.455 ± 0.013 Gyr) vs Monnier 2012 (0.7 ± 0.075 Gyr).** Both rotating-model isochrones but with different boundary conditions; cfg adopts Yoon. Resolution requires deeper read of Monnier 2012 §4 and Tetzlaff 2011 kinematic-age cross-check.
- **Hurt 2021 0.6-day candidate at 0.04 AU.** If 2026+ follow-up confirms (currently unconfirmed; could be stellar activity), `circumstellar_planet_present: true` Decisions row required and planet body cfg authored.
- **Su 2013 gap-clearer planets between 14 and 62 AU.** Inferred only from disk morphology. JWST-NIRCam or extreme-AO direct imaging would convert to confirmed planet bodies.
- **Conservative-opacity disk variant.** Current cfg uses `disk_opacity` = 0.06 (interesting-first tie-break); observation-consistent value is τ ~ 10⁻⁴ (essentially invisible). Author a "realistic" cfg variant as player-selectable option.
- **Polar magnetic spot from Petit 2010.** Not currently rendered; future cfg variant could add faint blue-shifted polar spot for close fly-by view.
- **Disk dust-size + Mie-scattering color synthesis.** Replace current HST-STIS-Fomalhaut palette tie-break with physically-derived `disk_tint_rgb_hex` from grain-size distribution + A0V illumination spectrum.
- **Robrade 2011 X-ray interpretation.** Weak corona vs. companion contamination is still debated; affects whether Vega gets any in-game flare model. Currently cfg has no flare model.

## Related

- [checklist](checklist.md)
- output: [docs/phase3/vega.md](../../docs/phase3/vega.md), [ko/docs/phase3/vega.md](../../ko/docs/phase3/vega.md)
- workspace meta: [phase3/circumstellar-disk-schema](../circumstellar-disk-schema/plan.md)
- canonical structural template: [docs/phase3/alpha-centauri-a.md](../../docs/phase3/alpha-centauri-a.md)
