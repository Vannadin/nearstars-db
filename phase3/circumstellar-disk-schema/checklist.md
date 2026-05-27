# Circumstellar disk schema — checklist

Concrete tasks. Tick as you go. Each unchecked block = roughly one commit unit.

## Stage 1 — Schema docs (main session)

### synthesis-template.md

- [ ] Add `### Stellar Physical` field group: `spectral_type`, `mass_msun`, `radius_rsun`, `teff_k`, `luminosity_lsun`, `metallicity_fe_h_dex`, `age_gyr`
- [ ] Add `### Stellar Activity` field group: `rotation_period_days`, `activity_log_rhk`, `activity_cycle_years`, `x_ray_log_lx_cgs_min`, `x_ray_log_lx_cgs_max`, `limb_darkening_alpha_h`
- [ ] Add `### Stellar Visual` field group: `visual_surface_tint_hex_primary`, `stellar_color_temp_k`
- [ ] Add `### Multi-star binary event` field group: `visual_companion_event_*` (open-ended naming; document the pattern)
- [ ] Add `### Circumstellar disk (stellar)` field group:
  - `disk_present` (bool)
  - `disk_inner_radius_au`, `disk_outer_radius_au` (float, AU)
  - `disk_dust_temperature_k` (float, K)
  - `disk_tint_rgb_hex` (hex string, cfg-ready synth)
  - `disk_opacity` (float 0–1, cfg-ready synth)
  - `disk_morphology` (prose — single-ring / multi-ring / asymmetric / two-belt)
  - `disk_resolved_imaging` (bool)
  - `disk_imaging_observatory` (prose — Herschel / ALMA / HST-STIS / VLT-SPHERE)
  - `disk_imaging_inclination_deg` (float, if resolved)
- [ ] Add `### Planetary ring` field group (extends Surface):
  - `ring_present` (bool)
  - `ring_inner_au`, `ring_outer_au` (float)
  - `ring_color_hex` (hex)
  - `ring_opacity` (float 0–1)
- [ ] Add `### Circumplanetary disk` field group (young / PDS-70-class):
  - `circumplanetary_disk_present` (bool)
  - `circumplanetary_disk_radius_planet_radii` (float)
  - `circumplanetary_disk_tint_rgb_hex` (hex)
- [ ] Update `### Decision-table field map`: add row for "Disk inner/outer radius, dust temp" → disk_inner_radius_au, disk_outer_radius_au, disk_dust_temperature_k
- [ ] Update `### Decision-table field map`: add row for "Disk resolved imaging morphology" → disk_morphology, disk_resolved_imaging, disk_imaging_observatory
- [ ] Update `### Decision-table field map`: add row for "Planetary ring extent" → ring_present, ring_inner_au, ring_outer_au
- [ ] Add canonical-example reference for stellar synthesis: `alpha-centauri-a.md`

### mod-grounded-fields.md

- [ ] Add `## Circumstellar disk (Kopernicus Ring on star body)` section:
  - Table: Phase 3 field → Kopernicus Ring field → unit conversion → notes
  - Source-priority block: ALMA / Herschel resolved imaging > Spitzer SED-fit > photometric IR excess > theory
  - Texture path convention deferred to texture pipeline (per kopernicus-emit-workspace open question)
- [ ] Add `## Planetary ring (Kopernicus Ring on planet body)` section with same table structure
- [ ] Cross-link to `synthesis-template.md` field-group anchors

### SKILL.md

- [ ] Step 0 — add time-estimate row: `Stellar-only (no planets) | 1–2 h` between "Single-planet" and "2–3 planet" rows
- [ ] Step 1 pre-flight — add bullet: "For stellar synthesis, confirm Phase 2 `disk_measurements` if disk is suspected. If absent, escalate via `nearstars-add-star` before Phase 3."
- [ ] Step 9.1 standard structure — add `alpha-centauri-a.md` to the canonical-template list (alongside `trappist-1-e.md`, with note that planetary uses TRAPPIST-1 examples and stellar uses Alpha Cen A)
- [ ] Step 9.1 — note stellar synthesis uses Stellar Decisions field groups (link to `synthesis-template.md` anchor)
- [ ] Step 14 — no change needed (per-star commit already the default)

### Backward compatibility validation

- [ ] Read `docs/phase3/alpha-centauri-a.md` Decisions table; confirm every existing field name appears in new schema
- [ ] Read `docs/phase3/trappist-1-e.md` Decisions table; confirm new ring fields slot in without breaking existing rows
- [ ] Run `python3 scripts/phase3/check_block_parity.py alpha-centauri-a` — exits 0
- [ ] Run `python3 scripts/phase3/check_block_parity.py trappist-1-e` — exits 0
- [ ] Run `bash scripts/check-mirrors.sh` — exits 0

### Stage 1 commit

- [ ] `git status --short` review
- [ ] Stage only the 3 schema files + workspace artifacts (`phase3/circumstellar-disk-schema/*.md`)
- [ ] Single commit: `refs(phase3): stellar Decisions field groups + circumstellar disk + planetary ring schema`

## Stage 2 — Per-star synthesis (8 parallel sub-agents)

### Pre-flight (main session, before dispatch)

- [ ] For each of 8 stars, read `db/systems/<star>.json` and record whether Phase 2 `disk_measurements` exists. Output: `phase3/circumstellar-disk-schema/phase2-status.md`
- [ ] For stars missing Phase 2 disk data, decide per-star: escalate via `nearstars-add-star` now (blocking) vs proceed with literature-direct Phase 1-grade inputs and mark `Confidence=low`. Log decision in context-notes
- [ ] For each star, create `phase3/<star>/` with `system.yaml` + light `checklist.md` + `context-notes.md` stub
- [ ] For each star, check `docs/phase3/<star>.md` — if existing partial Phase 3 (e.g. AU Mic with its planets), the sub-agent prompt must say "extend, do not overwrite"

### Sub-agent dispatch (single message, 8 parallel Agent tool calls)

- [ ] Vega
- [ ] Fomalhaut
- [ ] AU Mic (extend if existing)
- [ ] ε Eri
- [ ] τ Cet (note: 5 planets — sub-agent prompt scopes to stellar + disk only; planet-by-planet synthesis is a follow-up workspace)
- [ ] 61 Vir
- [ ] HD 69830
- [ ] δ Pav

Each sub-agent prompt contains:
- New schema (synthesis-template.md stellar field groups + disk subsection content, inlined)
- Star's `db/systems/<star>.json` content
- SKILL.md Steps 7–9 (triage + deep-read + English synthesis drafting)
- Pre-flight escalation decision (Phase 2 status)
- Output contract: English Phase 3 markdown + Decisions-row classification log + Open-items list + bibliography YAML stub

### Per-star post-receipt (main session, serial as each sub-agent returns)

For each returned synthesis:

- [ ] **Step 10 VERIFY** — re-read each Decisions row against the cited paper in `docs/phase3/_papers/<arxiv_id>.md`; fix any row that doesn't trace
- [ ] Write Korean mirror `ko/docs/phase3/<star>.md` (natural-prose Korean per `feedback-ko-mirror-style`)
- [ ] `python3 scripts/phase3/check_block_parity.py <star>` — exits 0
- [ ] `python3 scripts/phase3/build_html.py <star>`
- [ ] `bash scripts/check-mirrors.sh` — exits 0
- [ ] Browser visual check (lang toggle + Decisions table renders new disk fields)
- [ ] Per-star commit

### Stage 2 final (after all 8 stars committed)

- [ ] `python3 scripts/pipeline/build_reports_index.py`
- [ ] `bash scripts/check-mirrors.sh` final pass
- [ ] `docs/reports.html` shows all 8 new chips
- [ ] All 8 stars' `disk_present=true` Decisions rows traceable to cited paper

## Out of scope (subsequent workspaces)

- kopernicus-cfg emitter updates to consume disk fields
- Scatterer/EVE/Parallax disk shader cfg (gitignored skills)
- Disk texture / colormap PNG asset authoring
- Phase 2 `disk_measurements` ingestion for stars missing them (`nearstars-add-star` workspace)

## Related

- [plan](plan.md)
- [context-notes](context-notes.md)
