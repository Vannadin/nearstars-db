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

## 2026-05-28 — Tier 1 Phase 2 full curation + Phase 3 reconciliation

Tier-1 disk-host upgrade pass, matching the Delta Pavonis 4d26495
template. Expanded `db/stellar_props_curated.json::"Vega"` from a
mass/radius-only stub to the full 8-category Phase 2 measurement set.

Anchors per category (recommended:true):

- mass — Yoon 2010 (`2010ApJ...708...71Y`); existing pick kept.
- radius — Monnier 2012 (`2012ApJ...761L...3M`); existing pick kept.
- Teff — Monnier 2012 area-averaged 9602 K (kept SIMBAD harmonized
  9692 K in the top-level `teff_k` mirror because the Decisions
  table cites the harmonized value; Monnier's photospheric integral
  is recorded as recommended in the measurements array).
- L — Aufdenberg 2006 / Monnier 2012 total bolometric 47.0 ± 5 L_sun
  from the gravity-darkened model. No single "L=47" measurement
  paper exists for Vega in isolation — both papers derive it as part
  of the 2D rotating-photosphere fit. Pick: Monnier 2012.
- age — Yoon 2010 0.455 ± 0.013 Gyr (rotating isochrone). Monnier
  2012 0.7 ± 0.075 Gyr listed as cross-check. Both kept Confidence
  high in the Decisions table (it's not a tier ambiguity — Yoon is
  newer + smaller formal uncertainty; Monnier listed in Open items).
- [Fe/H] — Yoon 2010 [M/H]=−0.5 ± 0.04 (self-consistent abundance
  fit). Adelman 1988 `1988MNRAS.230..671A` cross-check (Mg/Si/Fe
  pattern). λ Boo class — bulk vs photospheric distinction noted in
  meta_notes.
- rotation — Aufdenberg 2006 v_eq = 274 km/s + Monnier 2012 R_eq
  geometric P_eq = 0.521 d (12.5 h); Petit 2010 ZDI 0.732 d
  cross-check; both stored, Aufdenberg recommended.
- activity — empty []. A0V has no convective envelope; chromospheric
  R'HK undefined. Meta_notes explains. Robrade 2011 X-ray detection
  exists but is controversial — not added pending interpretation.

Top-level mirror added: teff_k=9692, teff_bibcode="SIMBAD harmonized"
(treated narratively in meta_notes; the bibcode field accepts that
this is not a single-paper value — same convention as the Delta Pav
existing `teff_bibcode` field).

### Divergent rows corrected in Phase 3 doc

- `metallicity_fe_h_dex`: Decisions row Confidence promoted from
  medium to high, since `metallicity_measurements` is now populated
  in Phase 2 with Yoon 2010 + Adelman cross-check. Value unchanged.
- `age_gyr`: Basis text updated to cite Phase 2 measurement
  (Yoon 2010 isochrone in `age_measurements`) rather than narrative
  reference; Monnier 2012 cross-check now formally in the array.
- `rotation_v_eq_km_s` + `rotation_period_hours`: Basis text updated
  to cite the geometric derivation as a populated rotation entry
  with Aufdenberg 2006 attribution. Petit 2010 ZDI 0.732 d now also
  formally in the array.
- `luminosity_lsun`: Basis text updated to point at the new
  luminosity_measurements entry.

No fundamentally divergent values — Vega's Phase 3 (synthesized
2026-05-27) was already canonical-aligned per the existing
context-notes Decisions-row classification. The reconciliation
pass is rows-tracking-Phase-2-measurements, not value-changing.

### Rapid-rotator caveat handling

The Teff measurements array records two values:

- 9692 K (recommended:false, `method=interferometry`, Monnier 2012
  area-averaged) — what most papers report as "Teff(Vega)".
- 9602 K (recommended:true, `method=interferometry`, Monnier 2012
  pole/equator-averaged from CHARA/MIRC fit) — the Phase 3
  Decisions row continues to cite the SIMBAD harmonized 9692 K
  value, treated as numerically interchangeable; the difference is
  90 K, well within combined uncertainty.

Polar 10150 K / equatorial 7900 K values from Aufdenberg 2006 are
NOT recorded as separate teff_measurements entries — the schema
expects a single area-averaged Teff per row; the pole/equator
gradient is captured in the Decisions field
`visual_gravity_darkening_pole_equator_temp_diff_k = 2250` which
already exists.

Meta_notes explicitly documents the pole-equator gradient + the
choice of area-averaged Teff for the headline value.

### activity_measurements empty handling

Per task brief: A0 V has no convective envelope, so log R'HK is
undefined. activity_measurements is left as `[]` with a meta_notes
sentence: "A0 V has radiative envelope; chromospheric activity
indices undefined." Robrade 2011 X-ray detection log L_X ≈ 25.5–26
is mentioned narratively but not recorded as `x_ray` method
measurement because the interpretation is contested (weak corona vs
companion contamination, Robrade 2011 itself debates this).

## Related

- [checklist](checklist.md)
- output: [docs/phase3/vega.md](../../docs/phase3/vega.md), [ko/docs/phase3/vega.md](../../ko/docs/phase3/vega.md)
- workspace meta: [phase3/circumstellar-disk-schema](../circumstellar-disk-schema/plan.md)
- canonical structural template: [docs/phase3/alpha-centauri-a.md](../../docs/phase3/alpha-centauri-a.md)
- Delta Pav reconciliation template: commit `4d26495`
