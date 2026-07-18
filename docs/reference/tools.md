# Tools — NearStars

The project has grown to roughly thirty scripts plus several agent skills spread across multiple directories. This document indexes them **by purpose**, not by location. Each section is one logical unit of work — fetch data, build a viewer, generate mod cfg — and lists every file that participates.

## At a glance

| # | Group | What it does | Entry point |
|---|-------|--------------|-------------|
| 1 | Data engine | Fetch raw → assemble per-system JSON → validate | `./run_pipeline.sh` |
| 2 | DB → HTML viewer | Render `db/systems/` into the static site | `scripts/pipeline/build_site.py` |
| 3 | Phase 3 synthesis | ADS+arXiv triage → cfg-ready Decisions + bilingual viewer | `nearstars-phase3` skill |
| 4 | Stability sandbox | REBOUND N-body for hypothetical moons / extra planets | `phase3/stability-sim/scripts/run.py` |
| 5 | External cross-check | Compare DB positions against Stellarium | `scripts/verification/stellarium_crosscheck.py` |
| 6 | Kopernicus cfg | DB → Kopernicus `.cfg` patches | `kopernicus-cfg` skill |
| 7 | Principia cfg | DB → Principia n-body patches | `principia-cfg` skill |
| 8 | Firefly cfg | Phase 3 atmosphere → Firefly reentry-effect cfg | `firefly-cfg` skill |
| 9 | ResearchBodies cfg | Phase 4 discoverability → ResearchBodies hide/discover patch | `researchbodies-cfg` skill |
| 10 | Add star / Phase 2 curation | New-star DB entry procedure | `nearstars-add-star` skill |
| 11 | Dev helpers | Markdown preview, ko/ mirror parity, repo-wide health | `scripts/preview-md.sh`, `scripts/check-mirrors.sh`, `scripts/check.sh` |
| 12 | 3D star map | `db/systems/` → interactive 3D map (ly scale + per-system AU view) | `scripts/viz/build_starmap.py` |
| 13 | Phase 4 board tools | Validate decision boards (emit gate) + render per-body board HTML | `scripts/check_phase4_gate.py`, `scripts/phase4/build_phase4_html.py` |

## Verification & QA — index

Correctness checks live across several functional groups. This index gathers them in one place for visibility — each tool is also documented in its parent group.

| Verifies | Tool / Activity | Group | Run when |
|----------|-----------------|:-----:|----------|
| Schema integrity of `db/systems/*.json` | `scripts/pipeline/validate.py` | [1](#1-data-engine) | After every build (auto-invoked by `run_pipeline.sh`) |
| Hierarchical binary structure | `scripts/pipeline/test_hierarchical.py` | [1](#1-data-engine) | Smoke test after binary-orbit edits |
| DB positions vs Stellarium | `scripts/verification/stellarium_crosscheck.py` | [5](#5-external-cross-check) | Spot-check before publishing |
| Dynamical stability of curated + hypothetical bodies | `phase3/stability-sim/scripts/run.py` | [4](#4-stability-sandbox) | Before shipping a moon / extra-body cfg, or as a baseline-DB sanity check |
| `ko/` mirror file parity | `scripts/check-mirrors.sh` | [11](#11-dev-helpers) | Before commit / release |
| Phase 3 synthesis policy fit | `nearstars-phase3` audit-pass procedure | [3](#3-phase-3-synthesis-pipeline) | After a synthesis batch — manual, output at `phase3/<system>/audit-pass-<YYYY-MM-DD>.md` |
| Build artifact freshness + manifest coverage | `scripts/check_build_freshness.py` | [11](#11-dev-helpers) | Before push — invoked by `scripts/check.sh` section 7 |
| Phase 4 board schema-v2 / emit-gate conformance | `scripts/check_phase4_gate.py` | [13](#13-phase-4-decision-board-tools) | After every board edit — invoked by `scripts/check.sh` gate 8 |

## 1. Data engine

**Purpose.** Pull astrometry / photometry / stellar-property / planet measurements from public catalogs, assemble them into per-system JSON, and validate.

**Trigger.** New star added to target list, catalog refresh, schema change.

**Files.**
- `scripts/pipeline/fetch_astrometry.py` — Gaia DR3 TAP, SIMBAD fallback (RA, Dec, parallax, proper motion, RV)
- `scripts/pipeline/fetch_photometry.py` — Gaia G + Hipparcos V-mag
- `scripts/pipeline/fetch_stellar_props.py` — Teff, spectype, mass, radius via SIMBAD
- `scripts/pipeline/fetch_planets.py` — NASA Exoplanet Archive TAP
- `scripts/pipeline/fetch_planets_ps.py` — Planetary Systems default-param table
- `scripts/pipeline/fetch_stellarium_ids.py` — Stellarium Web skysource ID lookup
- `scripts/pipeline/build_systems.py` — raw + curated → `db/systems/*.json`
- `scripts/pipeline/build_curated_from_ps.py` — seed `planets_curated.json` from PS defaults
- `scripts/pipeline/generate_target_list.py` — rebuild `target_list.json` from `db/systems/`
- `scripts/pipeline/validate.py` — schema validation; exits non-zero on failure
- `scripts/pipeline/schema.py` — shared schema + validators
- `scripts/pipeline/_naming.py` — canonical host/planet name → slug / filename conversion (single source of truth; all builders import from here)
- `scripts/pipeline/test_hierarchical.py` — hierarchical binary structure test

**Orchestrator.** `./run_pipeline.sh` runs fetch → build → validate → site build in order.

**I/O.** `db/target_list.json` → `db/*_raw.json` → `db/systems/*.json`.

## 2. DB → HTML viewer

**Purpose.** Render `db/systems/` + Phase 2 measurements into the static HTML viewer at `docs/`.

**Files.**
- `scripts/pipeline/build_site.py` — generates `docs/data.json` + main `index.html`
- `scripts/pipeline/build_phase2_html.py` — per-system Phase 2 paper-by-paper viewer
- `scripts/pipeline/build_reports_index.py` — Phase 2/3 reports landing index

**Output.** `docs/{data.json, index.html, phase2/*.html, reports.html}`.

## 3. Phase 3 synthesis pipeline

**Purpose.** Convert Phase 2 measurements into cfg-ready synthesis decisions with a bilingual per-planet HTML viewer.

**Trigger.** Phrases like "Phase 3 진행", "<planet> 합성", "이 행성 Phase 3 까지 올려줘".

**Files.**
- `scripts/phase3/run_phase3.py` — driver for Steps 2–6 (bib build → system bib → expand → score → inject → fetch) from `phase3/<system>/system.yaml`
- `scripts/phase3/build_bibliography.py` — ADS + arXiv per-planet (or `--system`) bibliography
- `scripts/phase3/expand_citations.py` — 1-hop citation-graph walk
- `scripts/phase3/score_papers.py` — authority + relevance scoring, filter
- `scripts/phase3/inject_papers.py` — inject ADS-missed papers from `system.yaml` (replaces per-system `add_missing_papers.py`)
- `scripts/phase3/fetch_arxiv_texts.py` — pull full-text via ar5iv for pending papers
- `scripts/phase3/build_manual_fetch.py` — manual-followup HTML index
- `scripts/phase3/verify_triage.py` — gate: every score≥14 paper triaged
- `scripts/phase3/check_block_parity.py` — preflight: en/ko block structure match
- `scripts/phase3/field_tooltips.py` — tooltip glossary for the viewer
- `scripts/phase3/build_html.py` — per-planet HTML (en + ko mirror, toggle)
- `scripts/phase3/disk_color_mie.py` — synthesize a debris belt's scattered-light reflectance color (Bohren-Huffman Mie over grain-size dist + composition n,k, white-balanced to equal-energy → sRGB hex). Inputs: a_min/a_max/slope/composition/Teff. Validated vs the 2 measured colors (AU Mic blue, Fomalhaut grey). numpy-only.
- `phase3/<system>/system.yaml` — planets, score thresholds, paper injections

**Driver.** `nearstars-phase3` skill — defines the procedure (triage → deep-read → synthesize → validate → ko mirror → visual check).

**Audit pass.** After a synthesis batch the skill prescribes an external audit — each Decisions row reviewed against post-retrofit policies (mod-grounded fields, documented divergence). Output is a manual report at `phase3/<system>/audit-pass-<YYYY-MM-DD>.md`. See `phase3/trappist_1/audit-pass-2026-05-22.md` for the canonical example.

**Output.** `docs/phase3/*.html`, `phase3/<system>/manual-paper-followup.md`, `phase3/<system>/audit-pass-*.md`.

## 4. Stability sandbox

**Purpose.** Verify that hypothetical moons or extra planets stay dynamically stable before they get committed to a Kopernicus / Principia cfg. Doubles as a baseline-stability check for the curated systems themselves.

**Trigger.** Adding a moon or extra body, or sanity-checking the curated DB before shipping.

**Files.**
- `phase3/stability-sim/scripts/load.py` — DB JSON → REBOUND `Simulation`
- `phase3/stability-sim/scripts/run.py` — WHFast + MEGNO main entry
- `phase3/stability-sim/scripts/ring_clearing.py` — test-particle ring-clearing / gap measurement around a moon: seed a disk of massless particles bracketing a feeder moon's semi-major axis, integrate, and report which radii survive (does the moon open a gap or stay embedded?). Used to confirm Polyphemus's Chaos-fed E-ring is continuous (Chaos μ≈7.5e-7 too small to clear a gap — `results/_ring_clearing.log`).
- `phase3/stability-sim/scripts/plot_moons.py` — **canonical orbit-analysis visualization** (static 4-panel PNG: top-down orbits / eccentricity(t) / semi-major-axis drift Δa/a₀(t) / inclination(t)), with a supertitle carrying verdict + integrator + dt + |ΔE/E| + per-moon max Hill-fraction. Works for BOTH hierarchy levels from sim output alone — planet-center (moons, R_p) or star-center (planets, AU), chosen by `--center` (default: moon parent if the run has moons, else the star). Writes `<label>_orbits.png`. Tolerates leapfrog/trace runs (megno=None), unlike planet-only `plot_orbits.py`. `--dir <results-dir> [--label <system>] [--center <body>]`.
- `phase3/stability-sim/scripts/plot_interactive.py` — **interactive** 4-panel viewer (Plotly, self-contained HTML): same panels/data as plot_moons.py but click-legend to toggle a body across all panels, hover for exact values, box-zoom/pan to separate packed inner bodies. Light/dark toggle; plasma palette (matches the other viewers). `--dir <results-dir> [--label <system>] [--center <body>]`.
- `phase3/stability-sim/viewer-manifest.yaml` — single source of per-system viewer sim params (Principia-equivalent leapfrog dt=10min, years, snapshots, hypotheticals, overrides).
- `phase3/stability-sim/scripts/build_viewers.py` — batch driver: reads the manifest, re-runs each system the Principia way (skip-if-fresh), renders the static PNG + 3D animation, and writes the bilingual gallery `docs/phase4/orbit-viewers/index.html`. `--systems`, `--force`, `--quick`, `--gallery-only`.
- `phase3/stability-sim/hypotheticals/<system>.json` — extra-body spec

**Stack.** REBOUND 5.0 in `.venv/`, AU / yr / Msun units, 10⁴ yr default horizon. A Principia-equivalent run uses `--integrator leapfrog --dt-minutes 10` (mimics Principia's fixed 10-min ephemeris step).

**Output.** `phase3/stability-sim/results/{system}_summary.json` + `_timeseries.csv`, `phase3/stability-sim/STABILITY_REPORT.md`.

## 5. External cross-check

**Purpose.** Validate DB-computed positions against an independent source.

**Files.**
- `scripts/verification/stellarium_crosscheck.py` — compare DB RA/Dec to Stellarium Web

**Output.** Console diff report.

## 6. Kopernicus cfg generation

**Purpose.** Turn `db/systems/` + Phase 3 synthesis into Kopernicus `.cfg` patches.

**Range.** ~50 ly (Kopernicus terrain budget cap).

**Driver.** `kopernicus-cfg` skill.

**Files.**
- `.claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py` — bulk emitter (v1.1, 2026-05-27). Scope: circumstellar-disk Rings (star body) + planetary-ring Rings (planet body). Reads `stars[0].raw.disk_measurements` + Phase 3 `disk_tint_rgb_hex` + `disk_opacity`, converts AU → body-radius multipliers, multi-paper merge for null backfill. Full Properties / Orbit / PQS / Atmosphere still hand-written per `.claude/skills/kopernicus-cfg/references/*.md` templates.
- `scripts/make_placeholder_textures.py` — writes stand-in `<Body>_Sunspots.dds` / `<Body>_Corona.dds` (uncompressed 64×64 A8R8G8B8) at the texture paths the emitted star bodies reference, so a test build loads before real art exists. Reads the body list from the emitted `stars.cfg`; run it after the emitter.

**Output.** `dist/NearStars-Configs/Patches/Kopernicus/`, `dist/NearStars-Textures/PluginData/`.

## 7. Principia cfg generation

**Purpose.** Turn `db/systems/` into Principia `gravity_model` + `initial_state` patches for n-body gravity.

**Range.** ~80 ly (further than Kopernicus — no terrain mesh required).

**Driver.** `principia-cfg` skill.

**Output.** `dist/NearStars-Configs/Patches/Principia/`.

## 8. Firefly cfg generation

**Purpose.** Convert each Phase 3 atmosphere synthesis into a Firefly `ATMOFX_BODY` cfg — reentry plasma colors, multipliers, particle thresholds — plus a pack-level `ATMOFX_PLANET_PACK` covering every NearStars body with atmosphere.

**Trigger.** "Firefly cfg 만들어줘", "이 행성 재진입 색", "ATMOFX_BODY", reentry plasma / shockwave / streak chemistry questions.

**Driver.** `firefly-cfg` skill. Pinned to Firefly `mod_version: 1.0.6` (M1rageDev/Firefly, GPL-3.0). Schema claims cite `ConfigManager.cs:line`.

**Files.**
- `.claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py` — generic emitter: Phase 3 Decisions → ATMOFX_BODY + planet pack. Bulk-gas palettes hardcoded (composition-color.md §3); streak species from element DB.
- `db/refs/element_plasma_colors.yaml` — per-element flame/plasma hex DB (118 entries). Replaces pixel-sampling of the Helmenstine 2017 chart.
- `scripts/refs/validate_element_colors.py` — schema check for the DB.
- `scripts/refs/render_element_colors_doc.py` — re-render the companion doc (en + ko mirror).
- `docs/reference/element-plasma-colors.md` — companion view (generated, do not hand-edit).
- `scripts/refs/migrate_element_db_v2.py` — **one-shot migration, do not re-run** (v1 → v2 multi-regime schema for `element_plasma_colors.yaml`, output committed). Wraps each element's flat hex in a `regimes.atomic_flame` block, tagging `hex_basis` as cie_computed (from curated NIST lines) / canonical_descriptor (named flame color) / chart_approx (Helmenstine-chart fallback). Post-migration, edits go straight into the v2 YAML.
- `scripts/refs/populate_reentry_aurora.py` — **one-shot populate (idempotent), output committed**: adds the `reentry_plasma` (~8000–15000K, X I + X II ions + continuum) and `aurora` (forbidden O I green/red + N2+ band) regimes to the atmospherically-relevant species; polyatomics get `not_emitter` + a dissociation note. Ran after the v2 migration.
- `scripts/refs/populate_phosphor_emission.py` — **one-shot populate, output committed**: adds a `phosphor_emission` regime for the lanthanides (Ln3+ in a solid host — the display-industry rare-earth phosphor colors), keeping `atomic_flame` honest about the mostly-faint gas-phase Ln chemistry. Sources: Phosphor Handbook (2007), Blasse & Grabmaier (1994).
- `scripts/refs/populate_tier_c_upgrades.py` — **one-shot re-categorize (idempotent), output committed**: promotes/demotes `chart_approx` element entries after spectroscopic review — canonical_descriptor (named flame color), cie_computed (clear NIST visible lines), or not_visible_to_humans (UV/IR-dominant). Ran after the v2 migration.
- `scripts/refs/populate_spectro_refinements.py` — **one-shot refinement, output committed**: applies a 2026-05-26 subagent NIST + phosphor literature review to `chart_approx` entries — six material re-classifications (e.g. Zr→brilliant white, Gd/Yb→not-visible, Tm→cie_computed blue) plus basis-only honesty fixes for ~13 lanthanide / refractory-metal entries. Sources: NIST ASD, Phosphor Handbook, Conkling *Pyrotechnics*.
- `scripts/refs/build_molecular_db.py` + `db/refs/molecular_plasma_colors.yaml` — regenerable builder for the molecular analog of the element color DB: per-molecule `reentry_plasma` + `aurora` CIE-computed colors (or `not_emitter` with `dissociation_products` for photo-dissociating polyatomics like CO2/NH3/CH4). Captures the molecular-band signature the atomic element DB misses. Uses `wavelength_to_rgb.py`.
- `scripts/refs/cie_color.py` — shared colorimetry: Planck blackbody + CIE 1931 CMF (Wyman 2013) + XYZ→sRGB hue + spectrum→hex. Used by the engine and the temperature-color builder.
- `scripts/refs/wavelength_to_rgb.py` — regenerable **library module**: Bruton 1996 piecewise wavelength → sRGB (`wavelength_to_rgb`), additive intensity-weighted line mixing (`mix_lines`), and `rgb_to_hex`. The "what does a spectral line look like on a display" path (distinct from cie_color.py's colorimetric CIE 1931). Imported by cie_color.py, build_molecular_db.py, the element-DB migrate/populate scripts, and phase3/build_html.py.
- `scripts/refs/body_figure.py` — body figure calculator (grounding: `docs/reference/body-figure-methodology.md`): rotational `J2` via Radau–Darwin, synchronous tidal `C22`, a per-body seeded Kaula-spectrum high-degree geoid, and `ellipsoid_ratios()` → the VertexHeightOblateAdvanced `CustomEllipsoid` a:b:c visual emit. Calibration self-test reproduces Earth/Jupiter/Callisto (`python scripts/refs/body_figure.py`).
- `scripts/refs/build_atomic_lines.py` + `db/refs/atomic_lines.yaml` — atomic line/level/ionization data (H I, He I, C I/II, N I/II, O I/II, S I/II, Mg I/II, Ti I/II, V I/II, Fe I/II — 18 species) from the NIST ASD (lines1.pl + energy1.pl). H/He/C/N/O/S cover realistic atmosphere chemistry (N2/O2/CO2/SO2/H2O/H2/He/CH4/NH3); Mg/Ti/V/Fe feed the metal-oxide bands + their dissociation→atomic march. Add more with the same 2-line recipe. Cache-first (`/tmp/nist`); `--refresh` re-fetches live. Input to the LTE engine.
- `db/refs/molecular_bands.yaml` — molecular band systems (N2 1P/2P, N2+ 1NG, C2 Swan, CH/NH/OH, CN violet, CO Ångström, metal oxides TiO/VO/FeO/MgO) + Huber-Herzberg constants for dissociation equilibrium. Band heads + term values from Pearse & Gaydon / ExoMol / airglow literature. Input to the LTE engine.
- `scripts/refs/saha_boltzmann.py` — first-principles LTE plasma-emission color engine: thermal continuum + atomic lines + molecular bands, with Saha ionization, Boltzmann excitation, and dissociation all computed. Run directly for the self-test + color march. Note the documented LTE caveat (air's reentry blue-violet is non-LTE; not reproduced).
- `scripts/refs/build_plasma_temperature_colors.py` — drives the engine to emit the temperature-resolved plasma color table per composition (500K steps). `_blackbody` continuum is exact (Planck→CIE 1931); compositions are LTE-engine colors. Reference/physics tool, not a cfg input. Run `--sanity` for a color march.
- `db/refs/plasma_temperature_colors.yaml` — generated output: `_blackbody` color-temperature table (1000–20000K) + per-composition color vs T (1000–15000K) with ionization/molecular/emission fractions + dominant regime.
- `scripts/refs/reentry_color.py` — per-planet reentry color from **entry velocity** + atmosphere: maps velocity → representative shock-layer temperature (empirical, anchored to air reentry), runs the engine, **non-LTE on by default** (faster entry → hotter electron temp → N2-family blue-violet). E.g. `--velocity 11 "N2:0.78,O2:0.21"` → vivid reentry blue; `--velocity 5.5 "CO2:0.95,N2:0.05"` → Mars green. The intended per-planet color picker.
- `scripts/refs/emit_atmosphere_color.py` — arbitrary atmosphere composition (molecular mole fractions, e.g. `"CO2:0.95,N2:0.05"`) → LTE plasma color vs temperature. `--t-elec K` enables the 2-temperature non-LTE mode (N2-family blue). Converts to atomic fractions, auto-selects molecular band systems, runs the engine (spectrum-level mix, then CIE). The correct way to get a mixed-atmosphere color (mix spectra, never colors). Emitting elements H/He/C/N/O/S/Mg/Ti/V/Fe; others dropped + renormalized. `--html` for a swatch.
- `scripts/refs/build_aurora_colors.py` + `db/refs/aurora_lines.yaml` + `db/refs/aurora_colors.yaml` — NON-LTE aurora color vs density/altitude per atmosphere. Forbidden-line quenching `φ=A/(A+Σk·n)` (O ¹D red / ¹S green) + N₂ bands → CIE; axis is density (not temperature — aurora is non-thermal). Reproduces Earth's red(high)→green(mid)→pink(low) stratification. Feeds aurora/EVE, NOT Firefly reentry.
- `scripts/refs/build_element_temperature_colors.py` + `db/refs/element_temperature_colors.yaml` — per-element plasma color vs temperature (500K steps), the single-element analog of the per-composition table. Incandescence stand-in + neutral AND first-ion (X II) atomic line emission (Boltzmann), weighted by Saha neutral/ion fractions. Atomic-only; 75 elements with NIST A-values (others omitted). Drives the viewer's periodic table. `validate_plasma_temp.py` structure-checks it.
- `scripts/refs/build_molecular_temperature_colors.py` + `db/refs/molecular_temperature_colors.yaml` — per-molecule plasma color vs temperature (500K steps), the molecular analog of the element table. Each of the 30 panel molecules run as a single-species composition through the engine: low-T bands → dissociation → atomic → ionic. Molecules with atoms outside the engine set (Cl/F/Si) drop them (flagged in `dropped`). Drives the viewer's molecular panel. `validate_plasma_temp.py` enforces reproducibility (offline build).
- `scripts/refs/build_lte_plasma_colors.py` + `db/refs/lte_plasma_colors.yaml` — computed atomic emission color per element (periodic table's `lte_plasma` regime). Boltzmann at 3500K from NIST A-values where available (~73 elements; Na yellow, Cu green), top-N NIST observed intensities as fallback for A-less spectra (Zr/Nb/lanthanides/actinides, flagged low confidence). 98/118 filled; At + superheavies have no measured spectra (null). Curl cache-first; **fetch sequentially/low-concurrency — NIST truncates under load**. This is the ATOMIC color; molecular flame colors (CaOH, SrOH) differ — see curated flame regime.
- `scripts/refs/render_color_visualizer.py` — render `docs/firefly-colors.html`. The periodic table + molecular panel are colored by a **temperature slider** (1000–15000K) reading `element_temperature_colors` + `molecular_temperature_colors`; drag it to see the molecular→atomic→ionic march. Lower sections: composition/element temperature grids; the bulk/streak Firefly palettes; a Sol-planet **engine-vs-Firefly-stock comparison**; emitted bodies; and an aurora **density slider** + emitter catalog (non-LTE).
- `scripts/refs/stellar_photospheric_color.py` — regenerable tool backing `docs/reference/stellar-photospheric-color-methodology.md`: Teff / spectral-type → visible sRGB photosphere tint through the shared `cie_color.py` engine. FGK / white dwarfs use a Planck blackbody at Teff; M dwarfs use a real observed Pickles 1998 SED (TiO/VO/H2O bands → a pale warm orange, not brick-red). Pickles spectra are fetched from VizieR + cached under `scripts/refs/.cache/pickles/` (gitignored). Pipeline self-check: G2V → ~#fff4f2.

**References (in skill).** Five node-type files (`atmofx-body`, `atmofx-planet-pack`, `atmofx-part`, `atmofx-particles`, `atmofx-settings`), `color-format` (HDR), `composition-color` (atmosphere → reentry palette via bulk-gas plasma table), `phase3-mapping` (Phase 3 row → Firefly field), `pitfalls`.

**Output.** `dist/NearStars-Configs/Patches/Firefly/<Body>.cfg` per atmospheric body + `NearStarsPlanetPack.cfg`.

## 9. ResearchBodies cfg generation

**Purpose.** Emit the optional **discoverability** layer — a `RESEARCHBODIES { loadAs = mod ... }` ModuleManager patch that hides each NearStars body until the player discovers it via an observatory/telescope. Maps each body's real detection status (Phase 4 `identity > discoverability`) to an `IGNORELEVELS` start-visibility tuple + an `ONDISCOVERY` message (candidates cite the real detection paper).

**Trigger.** "ResearchBodies cfg 만들어줘", "discoverability 패치", "IGNORELEVELS / ONDISCOVERY", "이 바디 숨김 처리".

**Driver.** `researchbodies-cfg` skill. Pinned to RB `mod_version: 1.13.0.0` (JPLRepo/ResearchBodies). Schema claims cite `<file>.cs:line`. Difficulty grading = Scheme A; emit deferred to project end. Targets non-RP-1 (Sandbox/Science on RSS); RP-1 integration deferred (`references/rp1-compat.md`).

**Files.**
- `.claude/skills/researchbodies-cfg/scripts/emit_researchbodies_cfg.py` — reads Phase 4 `discoverability:` blocks, maps category → IGNORELEVELS tuple (Scheme A), writes one combined patch. `--dry-run` / `--input` supported.

**Output.** `dist/NearStars-Configs/Patches/ResearchBodies/NearStars.cfg`.

## 10. Add star / Phase 2 curation

**Purpose.** Procedure for adding a new star (target list → fetch → curate → validate) and for upgrading an existing star's Phase 2 curation depth.

**Driver.** `nearstars-add-star` skill.

**Files.**
- `scripts/pipeline/apply_phase2.py` — generic applier; reads `phase2/<system>/measurements.yaml` and writes to `stellar_props_curated.json` + `planets_curated.json`. Use `--check` to diff without writing.
- `phase2/<system>/measurements.yaml` — declarative Phase 2 measurement arrays (paper-by-paper, recommended-flagged). One file per system; replaces the old per-system `apply_phase2.py`.

**Workflow.** Edit `target_list.json` → `./run_pipeline.sh` → for Phase 2: write `phase2/<system>/measurements.yaml`, then `python3 scripts/pipeline/apply_phase2.py <system>` → re-validate.

## 11. Dev helpers

**Purpose.** Day-to-day workflow utilities.

**Files.**
- `scripts/preview-md.sh <md-file>` — render markdown to HTML and open in the browser
- `scripts/check-mirrors.sh` — verify `ko/` mirror parity (missing or stale files)
- `scripts/check_dead_links.py` — scan all tracked .md files for broken relative links
- `scripts/check_language.py` — detect Korean-dominant content in English-source-of-truth .md files (threshold 25% hangul; `phase3/_audit/*` allowlisted)
- `scripts/check_build_freshness.py` — verify `docs/data.json` is no older than newest `db/systems/*.json`, `docs/reports.html` / `reports-manifest.json` are no older than newest `docs/phase{2,3}/*.html`, and the manifest has zero orphan keys / dangling html (catches build_site.py skip + slug-convention drift)
- `scripts/check.sh` — pre-release umbrella: schema validation + mirror status (stale = warn, missing = fail) + dead-link scan + convention check + path-migration leftover scan + language check + build freshness + Phase 4 emit-gate (gate 8, tool 13). Manual invocation only.

## 12. 3D star map viewer

**Purpose.** Turn `db/systems/*.json` into an interactive 3D star map for the browser — see *where* the catalog sits in space, then zoom into any system to see its planets.

**Trigger.** "Visualize the DB in 3D", "성도 만들어줘", after a batch of new stars/planets.

**Files.**
- `scripts/viz/build_starmap.py` — reads `db/systems/`, clusters components into one marker per gravitationally-distinct location (union-find @ 0.4 ly, guarded by `binary_orbit_ref`), bakes blackbody RGB from Teff + light-year ICRS coordinates + luminosity-proxy marker sizes, injects the Solar System (canonical hardcoded elements) at the origin, and emits the self-contained viewer. `--self-check` validates counts without writing.
- `scripts/viz/starmap_template.html` — the Three.js viewer template (CDN importmap); builder substitutes the embedded JSON payload.

**Output.** `docs/starmap.html` — single self-contained file, GitHub-Pages hostable. Map view in light-years (Sol at origin, ICRS range rings, spectral legend, distance filter, beyond-50 ly toggle); click for an info panel, double-click to enter an AU-scale per-system view with planet orbits. KO/EN UI toggle.

**Serve.** `cd docs && python3 -m http.server` then open `http://localhost:8000/starmap.html` (CDN modules need http, not `file://`).

**Note.** Colour = perceptual blackbody approximation (not a calibrated SED); marker size = luminosity proxy (billboard, not physical radius). Independent of the `docs/index.html` DB browser (tool 2) — that one is the tabular viewer, this is the spatial one.

**Related — Polyphemus moon-system viewer.** `phase4/viewers/polyphemus-moon-viewer.html` is a standalone interactive 3D viewer for the α Cen A b (Polyphemus) moon system + ring design — the 5 named moons (Dante / Hades / Pandora / Cassandra / Chaos), their inclinations / nodes, and the faint Chaos-fed E-ring. A Phase 4 art-direction aid, separate from the catalog-wide star map; it visualizes the gated roster recorded in `phase4/alpha_centauri.yaml`. **FROZEN (2026-06-22):** its design-exploration job is done (roster / ring / obliquity locked), so it is kept as a captured artifact and later decisions are NOT synced into it. Its only feature the star map lacks is the Pandora surface POV + eclipse view; the canonical, maintained visualization is `docs/starmap.html`.

## 13. Phase 4 decision-board tools

**Purpose.** Keep the Phase 4 art-direction boards (`phase4/<system>.yaml`, schema v2) emit-safe and reviewable — validate every board against the SPEC contract, and render each board as per-body HTML pages for gate review.

**Trigger.** After any board edit (validator runs automatically as `check.sh` gate 8); "Phase 4 진행/돌리자" goes through the `nearstars-phase4` skill, which invokes both.

**Files.**
- `scripts/check_phase4_gate.py` — board validator. `schema_version: 2` boards are hard-checked (status/verdict/op enums, axis menu, typed `fields[]` shape incl. prose-only-number rejection, `(body, axis)` uniqueness, `refs` list type, `colors` hex format, divergence-note requirement, passthrough-carries-no-gate); legacy v1 boards get a soft one-line summary so migration proceeds file-by-file. Contract: `phase4/SPEC.md` §0/§3.1.
- `scripts/phase4/build_phase4_html.py <system>` — renders a v2 board into `docs/phase4/<system-slug>/` (index + one page per body): narrative prose + typed spec table (hex chips, windows, biome color swatches, per-field notes), gate evidence/divergence, KO/EN toggle. Slugs via `scripts/pipeline/_naming.py`. Deterministic (rerun → no diff).

**Output.** Validator: exit 0/1 + per-row diagnostics. Builder: `docs/phase4/<system-slug>/*.html`.

## Skills directory layout

Live skills live under `.claude/skills/<name>/`. `.agents/skills/` is reserved for `<name>-workspace/` build environments and for gitignored Patreon-EA skills (scatterer, eve, volumetrics).

| Skill | Location |
|-------|----------|
| `kopernicus-cfg` | `.claude/skills/kopernicus-cfg/` |
| `principia-cfg` | `.claude/skills/principia-cfg/` |
| `firefly-cfg` | `.claude/skills/firefly-cfg/` |
| `nearstars-add-star` | `.claude/skills/nearstars-add-star/` |
| `nearstars-phase3` | `.claude/skills/nearstars-phase3/` |
| `find-skills` (generic) | `.claude/skills/find-skills/` |

`.agents/skills/firefly-cfg-workspace/` and `nearstars-phase3-workspace/` are build environments for the corresponding live skills, not separate skills.

## Dependency graph

```
target_list.json
     ↓
[1] Data engine ──→ db/systems/*.json
                          │
                          ├──→ [2] HTML viewer ─────→ docs/
                          │
                          ├──→ [3] Phase 3 synth ───→ docs/phase3/
                          │
                          ├──→ [4] Stability sim ───→ phase3/stability-sim/results/
                          │
                          ├──→ [5] Stellarium x-check
                          │
                          ├──→ [6] kopernicus-cfg ──→ dist/.../Kopernicus/
                          │
                          ├──→ [7] principia-cfg ──→ dist/.../Principia/
                          │
                          └──→ [8] firefly-cfg (atmo bodies only) ──→ dist/.../Firefly/

[9] nearstars-add-star — procedure that drives the whole chain for a new star
[10] Dev helpers — orthogonal to the chain
```

## Related

- [methodology](methodology.md) — cluster hub; the data engine and validation tools document this methodology
- [adding_stars](adding_stars.md) — operational sequence using the script index here
- [mod-reference](mod-reference.md) — downstream mod-side tools
- [guideline](guideline.md) — project-level context (phases, distance limits) for the tools
