# NearStars Curation Data Contract

**Status:** DRAFT — awaiting user confirmation (2026-05-29)
**Purpose:** The single authoritative definition of *what data Phase 2 and Phase 3
require*. Everything else (helper scripts, audits, working dirs) is judged
against this contract. When a tool or value does not serve this contract, it is
scaffolding and is removed or pinned.

Derived verbatim from the committed sources of truth — not reconstructed:
- Phase 2 schema → `scripts/pipeline/schema.py` (enforced by `check.sh`)
- Phase 3 workflow → `.claude/skills/nearstars-phase3/SKILL.md`
- Convergence mechanism → `docs/phase3/_bib/*.yaml` + `scripts/phase3/fetch_arxiv_texts.py`

---

## Phase distinction (invariant)

- **Phase 2 = paper-cited measurements.** Each value traces to a real paper.
- **Phase 3 = cfg-ready synthesis.** Values *no single paper provides*,
  synthesized from Phase 2 inputs.
- **HARD RULE: Phase 3 inputs must be Phase 2 measurements**, never Phase 1
  auto-fill. Running Phase 3 on Phase 1 is the "workflow inversion" that must
  not recur. (`nearstars-phase3` SKILL Step 1 pre-flight enforces this.)

---

## Phase 2 — required data, per body type

### A. Stellar — `db/stellar_props_curated.json`
Keyed by canonical host name. Partial override allowed (no top-level required key).

**Top-level allowed keys:** `teff_k`, `teff_bibcode`, `spectype`,
`spectype_bibcode`, `spectype_reference`, `meta_notes`, `sources_extra`,
+ the 8 measurement-category arrays below.

**8 measurement categories** (each an array of entries):

| category | value key | uncertainty key | allowed `method` |
|---|---|---|---|
| `mass_measurements` | `value_msun` | `uncertainty_msun` | binary_orbit, asteroseismology, evolutionary_model, spectroscopic, spectroscopic_calibration, empirical_relation, unverified |
| `radius_measurements` | `value_rsun` | `uncertainty_rsun` | interferometry, eclipsing_binary, sed_fitting, evolutionary_model, spectroscopic_calibration, asteroseismology, unverified |
| `teff_measurements` | `value_k` | `uncertainty_k` | high_res_spectroscopy, low_res_spectroscopy, sed_fitting, photometric_color, interferometry, unverified |
| `luminosity_measurements` | `value_lsun` | `uncertainty_lsun` | bolometric_flux, sed_fitting, photometric, unverified |
| `age_measurements` | `value_gyr` | `uncertainty_gyr` | asteroseismology, isochrone, gyrochronology, activity_age, kinematic, unverified |
| `metallicity_measurements` | `value_dex` | `uncertainty_dex` | high_res_spectroscopy, low_res_spectroscopy, photometric_calibration, unverified |
| `rotation_measurements` | `value_days` | `uncertainty_days` | photometric_variability, v_sin_i, zeeman_doppler, asteroseismology, unverified |
| `activity_measurements` | one of `value_log_rhk` / `value_h_alpha_ew_angstrom` / `value_x_ray_log_lx_lbol` / `value_ca_ii_log_lhk` | `uncertainty_*` | log_rhk, h_alpha, x_ray, ca_ii_h_k, unverified |

**Per-entry rules:**
- Required: `method`, `recommended`.
- Common optional: `reference`, `bibcode`, `doi`.
- Forbidden prefix: `error_*` (use `uncertainty_*`).
- At least one `value_*` key must be present.
- **Exactly 0 or 1 `recommended: true` per category.**
- `recommended: true` is incompatible with `emit_source: false` (a recommended
  value is the source of a derived field and must keep attribution).
- `radius_measurements` extra keys: `instrument`, `angular_diameter_mas`,
  `angular_diameter_uncertainty_mas`, `arxiv`, `notes`.
- `mass`/`radius` extra keys: `source_title`, `source_used_for`, `emit_source`
  (build-control for the auto `sources[]` loop; stripped before raw block).
- `rotation_measurements` extra key: `notes` (grade / technique caveat, e.g. a
  chromospheric Ca II H&K period recorded with `method=unverified`).

**Category completeness is impact-ordered, not all-mandatory.** Priority for the
cfg / visual layer: rotation > activity > teff / R / L / mass > age > metallicity.
- **[Fe/H] is skipped for new hosts** — metallicity only weakly tints the SED
  (line blanketing, below perception), does not drive magnetic field or stellar
  wind (rotation + activity dynamo do), and Kopernicus does not ingest it.
- **A-type stars** leave `activity_measurements` empty (no chromospheric dynamo).
- Never fabricate a rotation period from v sin i / pole-on geometry — record
  `method=unverified` or omit. `method=unverified` flags a real measurement whose
  technique is outside the whitelist, not a dubious value.

### B. Disk — `db/disks_curated.json`
Keyed by component name (must exist in `target_list.json` components — orphan/typo
guard). One entry = (paper × belt).

- Top-level allowed: `disk_measurements`, `meta_notes`.
- Value keys (≥1 key must be *present*; the value itself may be `null` for
  detection-only papers like IRAS): `inner_radius_au`, `outer_radius_au`,
  `dust_temperature_k`, `dust_mass_mearth`, `inclination_deg`, `aspect_ratio`
  (vertical h = H/r, dimensionless; resolved/edge-on disks only) (+ `uncertainty_*`).
- Required: `method`, `recommended`. Optional: `reference`, `bibcode`, `doi`.
- Allowed `method`: sed_fit, resolved_imaging, photometric_excess, unverified.
- Extra keys: `belt`, `morphology`, `resolved`, `observatory`, `notes`.

### C. Planet — `db/planets_curated.json`
Keyed by host → list of planet dicts. Each planet: required `pl_name`; optional
blocks `orbital` / `physical` / `environment` / `atmosphere`.

- Each block is a **dict (Phase 1)** or **list-of-dict (Phase 2 multi-paper)**.
- Every block element requires ≥1 provenance key: `source` / `reference` /
  `bibcode` / `doi`.
- Array (Phase 2) form: `method` required + per-block whitelist; **0 or 1
  `recommended: true`** per block.
- Block field sets + method whitelists: see `schema.py` `PLANET_*_ALLOWED` /
  `PLANET_*_METHODS` (orbital+physical share `PLANET_ALLOWED_METHODS`;
  environment + atmosphere have their own).

---

## Provenance pinning — the convergence rule (anti-divergence)

The failure mode "every audit found a different paper / wrong value" was caused
by **non-deterministic live web search**. The fix is already-built infrastructure:

1. Every recommended Phase 2 value cites a paper by `bibcode` and — where an
   arXiv version exists — pins its `arxiv_id` in the per-host bibliography
   `docs/phase3/_bib/<slug>.yaml`.
2. `scripts/phase3/fetch_arxiv_texts.py` downloads the ar5iv text once into
   `docs/phase3/_papers/<arxiv_id>.md` (idempotent, git-ignored, regenerable).
3. **Value-check reads the cached text, never the live web.** Two audits of the
   same value read the identical bytes → results converge instead of diverging.

A value whose source is not pinned + cached is not "verified" — it is
"re-discoverable", which is the divergent state to avoid.

**Catalog / survey papers carry per-star values in VizieR, not the ar5iv body.**
Large catalogs (Cifuentes 2020, Mann 2015, Schweitzer 2019, Gomes da Silva,
Sousa / Santos) publish per-object measurements in their VizieR table, not in
the cached paper text. Value-check those against the named VizieR catalog (e.g.
`J/A+A/642/A115`) by object ID — a named-catalog lookup is deterministic too.

**Writing curated is canonical-writer-only.** Persist
`db/stellar_props_curated.json` / `db/planets_curated.json` through
`scripts/pipeline/apply_phase2.py` (from `phase2/<slug>/measurements.yaml`) or
`schema.write_canonical` — never a hand-rolled `json.dump`. A divergent indent
or key order re-serializes the whole file (a thousands-line diff that can mask
other entries). `validate.py` (check.sh gate 1) hard-fails any non-canonical
curated file, so the gate catches it before commit.

---

## Derived astrophysical values — method-grounding rule

Some cfg-bound values are not *measured* but *derived* (computed from curated
inputs). For any **non-trivial astrophysical derivation — one where a naive
estimate can be materially wrong because a model or structural assumption drives
the result** — ground the derivation in the literature, do not ship a
back-of-envelope as if authoritative. Examples: oblateness / J2, tidal heating
rate, atmospheric escape, greenhouse-inclusive equilibrium temperature, interior
structure / Love numbers, spin evolution.

- **Ground the *method*, not a fake measurement.** A fictional body (e.g.
  Polyphemus) has no measured value to cite. The grounding is (1) the derivation
  **relation / method paper** (e.g. Darwin–Radau / theory of figures, or an
  interior-model J2 paper) applied to our inputs, plus (2) citing the **input and
  calibration sources** (e.g. the giants' real J2 from Iess 2018 / Durante 2017).
- **Textbook closed-form is its own grounding.** Roche limit, Hill radius, Kepler,
  angular size, unit conversions — the standard formula *is* the citation; do not
  demand a paper per arithmetic. The rule targets model-dependent derivations, not
  every calculation.
- **Use the existing machinery.** Pin the method/calibration paper by `bibcode` +
  `arxiv_id`, cache via `fetch_arxiv_texts.py`, read the cached text (never live
  re-search) — the same convergence discipline as for measured values.
- **State the assumption + uncertainty.** Record which model/assumption was used
  and the resulting spread (a single number with no stated structural assumption
  is a back-of-envelope, not a grounded derivation).

Anchor: **Polyphemus J2** has been re-grounded — the giant-calibrated `q = ω²R³/GM`
estimate was replaced by a Radau–Darwin / theory-of-figures derivation (Helled et al.
2011, NMoI 0.23) giving J2 ≈ 0.023 (range 0.017–0.033), gated in the board and confirmed
by the 2026-06-25 figure pass + `docs/reference/body-figure-methodology.md` (methodology
index #13); treated as final (`phase4/alpha_centauri.yaml` bulk.geopotential_j2).

---

## Phase 3 — required output + workflow

**Precondition:** Phase 2 done for every body (SKILL Step 1 pre-flight). If only
Phase 1 exists, stop and escalate via `nearstars-add-star`, or proceed with
explicitly degraded confidence.

**Driver:** `scripts/phase3/run_phase3.py <slug>` runs stages 2–6 from
`phase3/<system>/system.yaml` (per-planet bib → system bib → citation expand →
score+filter → inject → arXiv fetch).

**Judgment steps (do not parallelize blindly):**
- Step 7 Triage — every `combined_score ≥ 14` paper classified
  deep_read/skim/skip/manual_followup; recorded in `category:` on the bib YAML,
  reasoning in `context-notes.md`. Gate: `verify_triage.py` exits 0.
- Step 8 Deep-read — extract cfg numbers from `_papers/<arxiv_id>.md`, log with
  arxiv_id beside each number.
- Step 9 Draft — pre-draft per-row classification
  (canonical-aligned / tie-break / documented-divergence) BEFORE prose.
- **Step 10 VERIFY — every Decisions row re-checked against the cached paper.**
  Single most important step. No unverified row is committed.
- Step 11 Korean mirror — natural prose, exact block parity.
- Step 12 Build — `check_block_parity.py` → `build_html.py` → reports index →
  `check-mirrors.sh`.
- Step 13 Browser check. Step 14 Commit (per-planet default).

**Output artifacts:** `docs/phase3/<slug>.md` + `.html` + `ko/docs/phase3/<slug>.md`.
The Decisions-table cfg-ready field set (stellar vs planetary) is defined in
`.claude/skills/nearstars-phase3/references/synthesis-template.md`
§ "Decision-table field map" — that reference is canonical; this contract does
not duplicate it.

**4 gates:** (1) Phase 2 inputs, (2) every Decisions row re-checked against
source, (3) tie-break defaults to visually distinctive, (4) canonical-vs-cfg
divergence requires a `## Canonical alternatives` section.

---

## Phase 3 — full cfg field inventory (by axis)

Enumerated from `synthesis-template.md` + `mod-grounded-fields.md` (both read
end-to-end 2026-05-29). This is the no-truncation checklist: a synthesis is
incomplete if an applicable axis below is unaddressed. P2 = has a Phase 2
measured input; P3-synth = synthesized (no measurement possible for exoplanets).

| Axis | cfg fields | Phase 2 input | Mod target |
|---|---|---|---|
| Orbit & spin | tidally_locked, obliquity_deg, eccentricity, argument_of_periastron_deg, sidereal_period_days, semi_major_axis_au, inclination_deg | planet `orbital` / `binary_orbits` | Kopernicus / Principia |
| Physical (planet) | mass_mearth, radius_rearth, surface_gravity_g_earth, density_g_cc, insolation_s_earth, equilibrium_temp_k (A=0 / A=0.3), bond_albedo, water_mass_fraction | planet `physical`+`environment` | Kopernicus |
| Surface | day/nightside_surface_temp_k, dayside_brightness_temp_k_*, surface_tint_rgb_hex_primary/accent, surface_morphology, surface_ice_caps, ocean_present/extent/tint | P3-synth | Kopernicus/PQS |
| Atmosphere | atmosphere_present, surface_pressure_pa (or reference_pressure_pa for gas giants — no solid surface, 1 bar cloud-deck reference), composition, scale_height_km, tint_rgb_hex, cloud_cover_fraction/morphology/tint | planet `atmosphere` | Kopernicus |
| Atmosphere optics | sunset_color_hex, mie_scattering_aerosol_anisotropy_g | P3-synth | Scatterer (local emitter) |
| Interior heating | tidal_heating_w_m2, induction_heating_w_m2, radiogenic_heat_w_m2 | paper/synth | Kopernicus |
| Magnetic field | magnetic_field_strength_microtesla_equator, magnetic_dipole_moment_normalized_earth, magnetic_dipole_tilt_deg | P3-synth (dynamo scaling) | Kerbalism |
| Radiation / belts | radiation_belt_present, radiation_inner/outer_belt_radius_planet_radii, surface_radiation_dose_msv_yr, atmospheric_shielding_g_cm2 | P3-synth | Kerbalism |
| Aurora | aurora_present (← atmosphere AND non-zero B), aurora_color_primary/secondary_hex, aurora_emission_species_primary, aurora_oval_magnetic_latitude_deg, aurora_intensity_kR_typical, aurora_visibility_fraction_year | P3-synth | EVE (local emitter) |
| Rings & disks | (a) planetary ring `ring_*` (7) (b) circumplanetary disk `circumplanetary_disk_*` (5) (c) circumstellar disk `disk_*` (12); multi-belt hosts use per-belt `disk_<belt>_*` → one Kopernicus `Ring` per belt | only (c) → `disks_curated` (per-belt) | Kopernicus Ring(s) |
| Sky from surface | star_apparent_angular_diameter_deg, stellar_illumination_color_temp_k | star+orbit synth | Kopernicus/Scatterer |
| Stellar physical | spectral_type, mass_msun, radius_rsun, teff_k, luminosity_lsun, metallicity_fe_h_dex, age_gyr | stellar 7 of 8 | Kopernicus |
| Stellar activity | rotation_period_days, activity_log_rhk, activity_cycle_years, x_ray_log_lx_cgs_min/max, limb_darkening_alpha_h, flare_rate_per_day, flare_energy_log_erg_max | stellar rotation+activity | Firefly/EVE |
| Stellar visual | visual_surface_tint_hex_primary, stellar_color_temp_k, visual_corona_extent_radii, visual_spot_coverage_max | blackbody+synth | Firefly/Scatterer |
| Binary visual event | visual_companion_event_<descriptor> (open naming) | orbit geometry | Firefly/Kopernicus |

**Dependency chain (do not break):** magnetic_field_strength →
`radiation_belt_present` + `aurora_present` (also needs atmosphere) +
`surface_radiation_dose`. Aurora color comes from atmosphere composition
(emission species), not the field.

**Mod gate:** EVE / Scatterer cfg *emitters* are local-only (Patreon policy), but
these Phase 3 *data fields* live in the public `nearstars-phase3` skill and may
be synthesized + committed. Kopernicus / Kerbalism / Firefly emitters are public.

The per-field "what to look for in the paper" extraction map is
`synthesis-template.md` § "Decision-table field map" (planetary/stellar) and
`mod-grounded-fields.md` (Kerbalism/EVE/Scatterer) — those remain canonical for
extraction detail; this table is the completeness checklist.

---

## What this contract implies for tooling

- Canonical Phase 2 curation + schema = `scripts/pipeline/` (`apply_phase2.py`,
  `build_systems.py`, `schema.py`, `validate.py`, `_naming.py`).
- Canonical Phase 3 pipeline = `scripts/phase3/` (driver + bib + fetch + score +
  triage-verify + html).
- Canonical gate = `scripts/check.sh`.
- **Any per-host one-shot script that mutates a `_bib` YAML or a curated JSON is
  scaffolding.** Its *decisions* (e.g. which papers are deep_read) are data and
  belong in the bib YAML's `category:` field; the script itself is disposable
  once those decisions are baked in.
