<!-- TRAPPIST-1 7-planet Phase 3 audit pass — policy-fit review against the post-retrofit skill -->
# TRAPPIST-1 Phase 3 — Audit pass 2026-05-22

External audit of all seven TRAPPIST-1 Phase 3 syntheses against the
current `nearstars-phase3` skill, with focus on the post-retrofit
policies introduced in PR #2 (mod-grounded-fields.md, conflict-resolution.md
§ "Documented divergence"). Diagnostic question applied to every
Confidence=low / Confidence=medium row that involves a judgment call:

> Does the canonical reading have a clear weight advantage from the
> literature?
> - **Yes** → divergence — `## Canonical alternatives` row required.
> - **No** (data silent within the window) → tie-break — Basis note
>   sufficient.

No prose was rewritten; this report only flags label / classification /
field-completeness issues. Actual edits to the seven `docs/phase3/*.md`
files (and Korean mirrors) await user confirmation per the audit brief.

---

## Summary of findings

| Planet | Verdict | Reclassifications? | Missing fields? | Terminology fixes? |
|---|---|---|---|---|
| b | clean (minor) | none | minor (n/a placeholders) | minor |
| c | **inconsistent** | **canonical-vs-cfg implementation conflict** | none critical | minor |
| d | clean (minor) | none | minor | minor |
| e | clean | none (recent retrofit good) | belt radii | minor |
| f | clean | none (recent retrofit good) | belt radii | minor |
| g | clean (label only) | none — tie-break holds | prose "canonical" terminology | minor |
| h | **possible upgrade** | **0.005 bar atm pick may be a divergence vs Dong 2018 / K-T 2022 retention literature** | none | minor |

**System-wide issues:**
1. Inconsistent capitalization / phrasing of "Tie-break (interesting-first)" across rows.
2. `magnetic_dipole_tilt_deg` Basis omits the `interesting-first` reference in b/d/e/f/g/h while c has it — minor terminology drift.
3. `radiation_inner_belt_radius_planet_radii` and `radiation_outer_belt_radius_planet_radii` (from `mod-grounded-fields.md`) are missing on every planet that has `radiation_belt_present = true` (e, f, g).
4. `aurora_visibility_fraction_year` (mod-grounded standard) is missing on all 7.
5. `sunset_color_hex` and `mie_scattering_aerosol_anisotropy_g` (Scatterer optional) are missing on the 4 atmosphere-bearing planets (d, e, f, g) but Scatterer §2 documents them as optional, so this is low priority.
6. Field naming inconsistency: `substellar_peak_temp_k` (b, c) vs `surface_temp_substellar_k` (e, f, g, h). Both refer to the same quantity. The standard template (`synthesis-template.md`) doesn't enumerate either — pick one.

---

## Per-planet findings

### TRAPPIST-1 b

**Tie-break rows identified:**
- `magnetic_dipole_tilt_deg = 10` — Basis cites `the interesting-first rule`.

**Diagnostic re-check:** observation silent, theory silent within
5–15° window. Tie-break confirmed. No action.

**Other Confidence=low rows without explicit tie-break label:**
- `surface_tint_rgb_hex_accent = #7a2a10` — exactly the worked
  example in `conflict-resolution.md` § "Documenting the choice"
  (line 158). Should carry the same `Tie-break: interesting-first.
  Photolytic oxidation patches OR cooling-lava red both fit the
  airless ultramafic surface; cfg picks lava for visual distinctiveness.`
  Basis it has now is a mechanism citation, not a tie-break note.
- `surface_radiation_dose_msv_yr = 80000` — derived scaling from
  Atri 2019; not a tie-break, just a low-confidence extrapolation.
  Current Basis is fine.

**Missing mod-grounded fields:** b is airless, so the EVE aurora
fields are all implicitly n/a but not explicitly marked. Adding
explicit `n/a (airless)` rows for `aurora_color_primary_hex`,
`aurora_color_secondary_hex`, `aurora_emission_species_primary`,
`aurora_oval_magnetic_latitude_deg`, `aurora_intensity_kR_typical`,
`aurora_visibility_fraction_year`, `sunset_color_hex`,
`mie_scattering_aerosol_anisotropy_g` would make field-completeness
auditable mechanically.

**Verdict:** clean. Minor terminology cleanup recommended for
`surface_tint_rgb_hex_accent`.

---

### TRAPPIST-1 c — **inconsistent**

User flagged this case as borderline. After re-reading:

**Canonical reading from literature** for surface activity:
- Barr 2018 (1712.05641): Maxwell viscoelastic interior, Io-class
  tidal heating 1.32 W/m², mantle T_eq 1666 K above rock solidus.
- Dobos 2019 (1902.03867): refined Maxwell model with Grimm 2018
  masses, F_int(c) = 0.62 W/m², partial melt confirmed.
- Kislyakova 2018 (1710.08761): c receives 68% of radiogenic flux
  from induction heating — highest in the system.

These are three independent modeling papers converging on the same
conclusion: **c hosts Io-class active volcanism**. By the conflict-
resolution diagnostic this is a *real* canonical weight advantage,
not a tie-break.

**cfg implementation actually picks a mixed reading:**
- `surface_tint_rgb_hex_primary = #2c2218 (weathered basalt)`
- `surface_morphology = "weathered basaltic plains; aged impact
  craters; subdued relief"` — prose then adds "fresh basaltic
  resurfacing in localized hot spots"
- Basis on `surface_morphology` row: "no fresh resurfacing inferred
  (unlike b); cumulative ~8 Gyr impacts" — this Basis directly
  *contradicts* the prose admitting Io-class activity, and contradicts
  Barr/Dobos/Kislyakova.

**This is a latent divergence.** The cfg is implicitly diverging from
the canonical Io-class reading (3 modeling papers) toward a
conservative mostly-weathered surface — but without flagging the
divergence per the new policy.

**Sub-options:**

- **A. Embrace canonical Io-class fully.** Change
  `surface_tint_rgb_hex_primary` from weathered `#2c2218` toward a
  fresh-basalt tone, expand the "hot spots" prominence in
  `surface_morphology`. No Canonical alternatives section needed
  because cfg matches canonical.
- **B. Keep mixed reading but document the divergence.** Add a
  `## Canonical alternatives` section with row:
  `surface_morphology | mostly weathered + localized hot spots | active Io-class global resurfacing | Barr/Dobos/Kislyakova converge on Io-class; cfg picks mixed reading to preserve the b-c "bare-rock siblings" aesthetic pairing in the inner-pair palette.`
  Update the `surface_morphology` Basis to say
  `Documented divergence: see Canonical alternatives.`
  Remove the misleading "no fresh resurfacing inferred (unlike b)"
  from the Basis — it directly contradicts the cited papers.
- **C. Treat as tie-break.** Argue Hu 2025 atmosphere upper-limit
  weakens the canonical claim because mineralogy is observation-silent.
  Add an explicit `Tie-break: interesting-first` style note. **Weakest
  defense** — the canonical here is modeling-based, not observation-
  based, so observation silence does not down-weight it.

**Recommendation: B.** The literature weight clearly favors active.
The cfg diverged conservatively, probably to keep b/c visual pairing.
That decision is fine — but it should be documented per the new
policy, not hidden in a self-contradicting Basis.

**Terminology fixes:**
- `aurora_color_primary_hex`: "tie-break: interesting-first chose
  green over UV-dominant alternative" — inconsistent capitalization
  vs `magnetic_dipole_tilt_deg`'s "Tie-break (interesting-first)".
  Pick one style.
- `aurora_color_secondary_hex`: same.

**User-flagged challenge ("Is Io-class really canonical-weight?")
answered:** Yes. Three independent modeling papers (Barr/Dobos/
Kislyakova) converging on the same conclusion is exactly the
"specific papers, modeling consensus" criterion in
`conflict-resolution.md` § "Documented divergence". Hu 2025
atmosphere upper-limit doesn't change this because Hu 2025
constrains the *atmosphere*, not the *surface mineralogy*.

---

### TRAPPIST-1 d

**Tie-break rows identified:**
- `magnetic_dipole_tilt_deg = 10` — Basis says "Tie-break: 10° gives
  offset auroral cap; aesthetic window 5–15°". `interesting-first`
  reference missing.
- `aurora_color_primary_hex = #B0E0E6` — Basis says "Tie-break
  (interesting-first): pale cyan-white from H₂O cloud aerosol
  excitation + OH band emission boosted to visible by Mie scattering".
  ✅
- `aurora_color_secondary_hex = #4DFF4D` — "tie-break: interesting-first
  picks visible secondary over UV-only". ✅

**Diagnostic re-check on cloud-resonant cyan aurora:** UV emission
(OH-A-X) is well-grounded chemistry; the Mie-scattered visible
rendering is a perception/aesthetic choice. No paper rules in or out
specific visible coloration. Genuine tie-break confirmed.

**No structural reclassifications needed.**

**Verdict:** clean. Add `interesting-first` reference to
`magnetic_dipole_tilt_deg` Basis for terminology consistency.

---

### TRAPPIST-1 e — Canonical alternatives retrofit confirms

Recent retrofit (commit c9e7c81) added the `## Canonical alternatives`
section. Re-verified against the diagnostic:

**Documented divergence (current):**
- `magnetic_field_strength_microtesla_equator = 30 μT (Wang 2025)`
  vs canonical `~2 μT (RM22)`.

**Diagnostic check:** Wang 2025 *assumes* Earth-analog 0.32 G for
habitability-scenario MHD modeling (an in-paper assumption, not a
derived measurement). RM22 (2203.01065) *derives* the dipole moment
from physical scaling laws applied to tidally-locked low-mass planets.
The cfg picks the assumed-Earth-analog value for visual recognizability.

This is a real divergence — RM22's derivation has a clear weight
advantage as canonical because it's the physics-based prediction.
Wang 2025 is one paper using one assumption. ✅ correctly classified.

**Other tie-break rows:**
- `magnetic_dipole_tilt_deg = 11` — Basis: "Earth-analog 11°
  (Wang 2025 uses 23.5° but reports tilt sensitivity); tie-break:
  Earth-like 11° gives recognizable auroral geometry for player". 
  Wang 2025's 23.5° was simulation-default Earth axial tilt, not a
  recommended value for tidally-locked e. Tilt sensitivity reported
  → genuinely silent at 11° vs 23.5° level. Tie-break OK.
- `aurora_color_primary_hex = #4DFF4D` — "interesting-first tie-break:
  green over UV-only alternative". OK.
- `aurora_color_secondary_hex = #FF4D4D` — "tie-break: enhances
  visible palette diversity". OK.

**Cloud morphology row:**
- `cloud_morphology = "double mid-latitude bands + quasi-stationary
  substellar cluster"` with Basis citing THAI II.

Worth noting: THAI II shows 3 of 4 GCMs (ExoCAM / LMD-G / UM Hab 1)
give equatorial-jet superrotation, only ROCKE-3D (and UM under
Cohen 2022 setup) give the double mid-latitude jet. By raw paper
count canonical would lean equatorial. cfg picks mid-latitude.

This is a possible documented divergence — but the synthesis already
flags the tipping-point status explicitly in both the Basis (`"The
double-band cfg pick is one of two equally-supported outcomes."`)
and the Rotation section. Given that Wolf 2017 + Cohen 2022 also
support mid-latitude and that the planet is "at the tipping point",
calling this a divergence is borderline. **Leave as tie-break,
preserve as Open item** (already done).

**Missing mod-grounded fields:**
- `radiation_belt_present = true` but no `radiation_inner_belt_radius_planet_radii`
  or `radiation_outer_belt_radius_planet_radii`. Should be added.
- `aurora_visibility_fraction_year` missing.

**Verdict:** clean structurally. Field completeness needs minor work.

---

### TRAPPIST-1 f — Canonical alternatives retrofit confirms

**Documented divergence (current):**
- `atmosphere_surface_pressure_pa = 100000 (1 bar Wolf 2017 eye-ball)`
  vs canonical `10000 (0.1 bar Turbet 2018 snowball)`.
- `ocean_extent_substellar_radius_deg = 40` (downstream of pressure).

**Diagnostic check:** Turbet 2018 explicitly GCM-converges on
0.1 bar snowball as the more theoretically supported steady state.
Wolf 2017 demonstrates 1 bar produces the lens. Lim 2024 NIRISS
permits both. Canonical = Turbet 2018 (modeling consensus); cfg =
Wolf 2017 eye-ball (visually defining). ✅ correctly classified —
exactly the worked example in `conflict-resolution.md` § "Documented
divergence" § "Worked example — TRAPPIST-1 f atmosphere pressure".

**Other rows:**
- `magnetic_dipole_tilt_deg = 12` — `Tie-break: 12° offset gives
  distinctive auroral cap`. `interesting-first` reference missing.
- `aurora_color_primary_hex`: "tie-break: red over UV-only since
  visible" — Mars-analog CO₂⁺ chemistry is specific, but visible
  vs UV-only is the perception-window choice. Tie-break OK.

**Missing fields:** same as e (`radiation_belt_present = true` →
belt radii missing; aurora_visibility_fraction_year missing).

**Verdict:** clean. Canonical example for the policy.

---

### TRAPPIST-1 g — **tie-break confirmed; prose terminology only**

User flagged cryovolcanic warm spots as borderline ("promoted on
Europa/Ganymede analog alone").

**Diagnostic re-check:**
- Observation: no JWST data on g exists. Silent.
- Theory of cryovolcanism on g specifically: **silent**. The
  bibliography contains no paper that models g's ice-shell-thinning
  or cryovolcanic plume mechanics. The promotion rests on
  Europa-Ganymede analog reasoning.
- Theory of "smooth uniform snowball": also silent on surface
  morphology. Wolf 2017 / Lincowski 2018 / Fauchez 2019 only assert
  *atmospheric* snowball state. No paper says g's ice is
  morphologically featureless.

Both readings are paper-silent. This is genuinely a tie-break, not a
divergence. **The user's challenge does not promote it to divergence.**

**But the prose terminology is off.** The current synthesis says:

> "Per the interesting-first rule, the cfg promotes
> cryovolcanic plumes from 'possible' to **canonical**: visible
> plumes near 2–4 substellar warm spots..."

The word "canonical" here is being used in the casual sense ("the
default cfg pick") not in the policy sense ("the literature-supported
reading"). Under the new policy "canonical" refers specifically to the
*literature-supported* reading — using it to mean "default cfg pick"
will confuse future sessions and could mis-trigger the divergence
machinery (a future audit could read "promoted to canonical" and ask
where the Canonical alternatives row is).

**Recommended terminology fix:** rewrite the sentence to use
tie-break vocabulary:

> "Per the interesting-first rule, the cfg adopts visible
> cryovolcanic plumes near 2–4 substellar warm spots as the default
> visual feature (tie-break: literature silent on surface morphology
> at this resolution)."

Also update the `surface_morphology` row Basis to add the explicit
`Tie-break: interesting-first` note alongside the Europa-Ganymede
analog mention — currently the Basis says "Wolf 2017 + Europa-Ganymede
analog reasoning" with no tie-break label. Without the label, a
future reader can't tell whether this row was a deliberate
interesting-first pick or a confident derivation.

**Other rows:**
- `magnetic_dipole_tilt_deg = 12` — `Tie-break: 12° offset for
  distinctive auroral cap`. `interesting-first` reference missing.

**Missing fields:** same belt-radii + aurora_visibility_fraction_year.

**Verdict:** tie-break holds. Two terminology fixes (prose
"canonical" → tie-break wording; `surface_morphology` Basis label).

---

### TRAPPIST-1 h — **possible documented-divergence upgrade**

User flagged: "어느 쪽이 진짜 canonical 인지 논문 weight 비교 필요"
(Dong 2018 vs Lincowski 2018).

**Three competing readings in the literature:**

1. **Thick atmosphere retention (10–100 bar CO₂/O₂).** Lincowski 2018
   "desiccated habitable" scenario. Single paper; cfg correctly
   treats this as an alternative scenario in Open items.

2. **Moderate retention (~0.1 bar N₂/CO₂).** Supported by:
   - Dong 2018 (1705.05535): "h ought to be the most stable planet
     from the perspective of atmospheric ion loss"; lowest ion escape
     rate in the system; retention timescale ~10¹⁰ yr.
   - Krissansen-Totton 2022 (2207.04164): "outer planets retain
     significant surface volatiles in virtually all model simulations"
     with "CO₂-dominated or CO₂-O₂ atmospheres for all planets that
     retain substantial atmospheres".
   - Bourrier 2017 (1708.09484): h has the smallest mass-loss in the
     system; brief HZ-runaway preserves most accreted water.

3. **Thin / near-airless (~0.005 bar).** Supported by:
   - Castan-Lopez 2025 (2504.19872): cosmic shoreline places h close
     to or below retention threshold.
   - Zahnle 2017 (cosmic shoreline framework).

**cfg picks #3 (0.005 bar)**, with both Confidence=low rows for
`atmosphere_present` and `atmosphere_surface_pressure_pa`.

**Diagnostic check on weight balance:**

The pro-retention side has **3 specific physical-mechanism papers**
(Dong / K-T / Bourrier) directly addressing h's escape, retention,
and water history. The pro-thin side has **2 empirical-scaling
papers** (Castan-Lopez / Zahnle) applying system-level cosmic
shoreline statistics. The physical-mechanism papers more specifically
address h's particular situation; the cosmic shoreline papers are
population-statistical.

**By the conflict-resolution diagnostic, the canonical reading is
arguably #2 (moderate retention).** cfg picks #3 (thin), which is
defensible but conservatively below the literature's typical
prediction.

**Current audit-trail state:**

- Open items mentions "a thicker (~0.1 bar) atmosphere is also
  defensible." ✅ acknowledges alternative.
- Open items says "0.1 bar variant might be more realistic than the
  canonical 0.005 bar." Note the word "canonical" used here for the
  cfg pick — same terminology drift as g.
- No `## Canonical alternatives` section present.

**Recommendation: upgrade to documented divergence.** Add a
`## Canonical alternatives` section with row:

```
| `atmosphere_surface_pressure_pa` | 500 (0.005 bar, cosmic-shoreline-conservative; Castan-Lopez 2025 / Zahnle 2017) | 10000 (0.1 bar Mars-thin N₂+CO₂; Dong 2018 / Krissansen-Totton 2022 retention literature) | Pro-retention literature (Dong 2018 lowest ion escape rate; Krissansen-Totton 2022 outer-planet retention in all simulations; Bourrier 2017 smallest mass-loss in system) favors a thicker atmosphere; cfg picks the cosmic-shoreline-thin reading to preserve the Mars-Pluto hybrid visual character that distinguishes h from g (also a snowball). Conservative 0.1 bar reading preserved as cfg variant in Open items. |
```

Also update the `atmosphere_surface_pressure_pa` row Basis from the
current `"0.005 bar — minimal residual; Mars-thin"` to
`"Documented divergence: see Canonical alternatives. 0.005 bar
cosmic-shoreline-conservative."`.

Same applies to `atmosphere_present` and `atmosphere_composition`
which are downstream of the pressure choice — note the divergence in
their Basis.

The Lincowski 2018 thick (10–100 bar) reading stays an Open-items
alternative scenario (single paper, no Canonical alternatives row
needed since it's not the canonical weight winner).

**This is the strongest upgrade case among all 7 planets.** Acting on
it lifts h's audit trail to the same standard as e and f.

**Other rows:**
- `magnetic_dipole_tilt_deg = 10` — `Tie-break: 10° offset;
  potentially crustal anomaly-dominated like Mars (no clear dipole
  axis)`. The Mars-analog crustal-only field is well-motivated by
  Mars-MAG/ER analog. tie-break is OK but `interesting-first`
  reference missing.
- `aurora_oval_magnetic_latitude_deg = 15` — Confidence=low,
  Basis: "No organized dipole → patchy crustal aurora at random
  latitudes; representative value". This is a representative-pick
  for a system that's fundamentally patchy. Tie-break-equivalent.
  Consider adding `Tie-break: representative` or similar.

**Open items mention "tidal heating may be underestimated by 1–2
orders of magnitude per Makarov 2018":** this is a flagged errata,
not a tie-break or divergence. Action: fix the
`tidal_heating_w_m2` row value, don't leave it as a Confidence note.
(Per CLAUDE.md §10 — read errors; per Step 10 VERIFY
fix don't note.)

---

## System-wide findings

### A. Terminology drift across the seven files

The `Tie-break (interesting-first)` label appears in many forms:

| Phrasing observed | Planet/row |
|---|---|
| `Tie-break (interesting-first per the interesting-first rule)` | b (mag tilt), c (mag tilt) |
| `Tie-break: 10° gives offset auroral cap` (no interesting-first) | d (mag tilt) |
| `tie-break: interesting-first chose green over...` | c (aurora primary) |
| `interesting-first tie-break: green over UV-only alternative` | e (aurora primary) |
| `tie-break: red over UV-only since visible` | f (aurora primary) |
| `Tie-break (interesting-first):` (formal) | d (aurora primary) |
| `Tie-break: 12° offset for distinctive auroral cap` | f, g (mag tilt) |
| `Tie-break: 10° offset; potentially crustal...` | h (mag tilt) |

Recommended single canonical form:
```
Tie-break (interesting-first): <one-clause reason>
```

Capitalization, parenthesization, and word order should be uniform
across all 7 planets. The reference to `the interesting-first rule`
can appear once in the file or be implicit if the synthesis includes
the canonical link section.

### B. Missing mod-grounded fields

Per `references/mod-grounded-fields.md`:

| Field | Mod | Currently missing where |
|---|---|---|
| `radiation_inner_belt_radius_planet_radii` | Kerbalism | e, f, g (belt true) |
| `radiation_outer_belt_radius_planet_radii` | Kerbalism | e, f, g (belt true) |
| `aurora_visibility_fraction_year` | EVE | all 7 |
| `sunset_color_hex` | Scatterer (optional) | d, e, f, g (atmosphere planets) |
| `mie_scattering_aerosol_anisotropy_g` | Scatterer (optional) | d, e, f, g (atmosphere planets) |

For airless / aurora-absent planets (b, h-arguably), missing rows
should be present as `n/a (airless)` so future field-completeness
checks can mechanically verify them.

### C. Field-name inconsistency

`substellar_peak_temp_k` (b, c) ↔ `surface_temp_substellar_k` (e, f, g, h).

The standard template (`synthesis-template.md`) doesn't explicitly
enumerate either. Pick one (recommend `surface_temp_substellar_k`
since it matches the `surface_temp_*` family already used for
nightside / global mean in e–h) and rename b and c for uniformity.

### D. Non-standard fields introduced ad-hoc

These appear in some planets but not the standard template — not
necessarily wrong, but cfg writer must handle them or skip them:

| Field | Where | Worth promoting? |
|---|---|---|
| `iron_mass_fraction_pct` | c only | Add to Physical block in template (rare but visual-relevant for iron-rich planets) |
| `core_mass_fraction` | c only | Possibly add to Physical |
| `subsurface_ocean_probability` | e only | Boldog 2023 metric — better as prose annotation |
| `tidal_k2_over_Q` | c only | Dynamics; let principia-cfg handle |
| `moment_of_inertia_C` | c only | Dynamics; let principia-cfg handle |
| `xuv_flux_at_planet_F_earth` | g only | Worth standardizing across system |
| `stellar_microflare_cadence_min` | g only | Worth standardizing (stellar context) |
| `magnetic_field_present` | e, f, g, h (bool) | Redundant with `magnetic_field_strength_microtesla_equator > 0`; can be derived |
| `induction_heating_magma_ocean_fraction` | b, c, d | Useful — consider promoting |

No edits to the template are proposed here; this is a forward-looking
inventory.

---

## Recommended actions, prioritized

### Priority 1 — substantive policy fixes (require user decision)

| # | Planet | Action |
|---|---|---|
| 1 | c | Decide between sub-option A (embrace canonical Io-class), B (add `## Canonical alternatives` row documenting the divergence), or C (defend as tie-break). **Recommended: B.** Update `surface_morphology` row Basis to drop "no fresh resurfacing inferred" line which contradicts the cited Barr/Dobos papers. |
| 2 | h | Add `## Canonical alternatives` section for `atmosphere_surface_pressure_pa` (0.005 bar gameplay vs 0.1 bar Dong 2018 / K-T 2022 canonical). Update the row Basis to `Documented divergence: see Canonical alternatives.` Korean mirror updated in same commit (block-parity). |
| 3 | h | Fix `tidal_heating_w_m2` row value per Makarov 2018 finding (1–2 orders of magnitude higher than current cfg). Don't keep this as an unresolved Open item — it's a validation-pass finding. |

### Priority 2 — terminology consistency (mechanical fix)

| # | Scope | Action |
|---|---|---|
| 4 | b, d, e, f, g, h | Standardize `magnetic_dipole_tilt_deg` Basis to `Tie-break (interesting-first): <reason>`. Add the `interesting-first` reference where missing. |
| 5 | g | Rewrite the "promotes cryovolcanic plumes from 'possible' to canonical" prose sentence to use tie-break vocabulary; update `surface_morphology` row Basis to add explicit `Tie-break: interesting-first` note. |
| 6 | h | Remove the word "canonical" from the Open items line "0.1 bar variant might be more realistic than the canonical 0.005 bar" — `canonical` carries policy meaning now. Use `default` or `current cfg pick`. |
| 7 | b | Update `surface_tint_rgb_hex_accent` Basis to match the worked example in `conflict-resolution.md` § "Documenting the choice" (currently just cites mechanism; should explicitly say `Tie-break (interesting-first)`). |
| 8 | all 7 | Sweep capitalization of `Tie-break` vs `tie-break` and parenthesization across all `aurora_color_*` rows. |

### Priority 3 — mod-grounded field completeness (low-risk additive edits)

| # | Scope | Action |
|---|---|---|
| 9 | e, f, g | Add `radiation_inner_belt_radius_planet_radii` and `radiation_outer_belt_radius_planet_radii` rows. Use the typical-range defaults from `mod-grounded-fields.md` (inner 1.2–2.0, outer 3–8) with Confidence=low + `Tie-break: airless-default` style note unless a specific paper constrains them. |
| 10 | all 7 | Add `aurora_visibility_fraction_year` row. Use the Earth ≈ 0.05 baseline for d/e/f/g/h scaled by flare frequency; n/a for b. |
| 11 | b | Add explicit `n/a (airless)` rows for missing aurora and Scatterer fields so audit can mechanically verify field-set completeness. |

### Priority 4 — field-naming standardization (one-time cleanup)

| # | Scope | Action |
|---|---|---|
| 12 | b, c | Rename `substellar_peak_temp_k` → `surface_temp_substellar_k` to match e/f/g/h. (Or vice versa — pick one.) Korean mirrors updated in same commit. |

### Priority 5 — beyond-audit follow-ups (no action required)

- Skill template enhancement: consider whether `induction_heating_magma_ocean_fraction`, `xuv_flux_at_planet_F_earth`, `core_mass_fraction` should be added to the standard field list in `synthesis-template.md`. Doing so would standardize current ad-hoc usage across e/f/g/h.

---

## What this audit deliberately did not check

- **Numerical re-verification of Decisions values against papers.**
  This is the `nearstars-phase3` Step 10 validation pass — already
  done in prior commits per the b/c/e/g/h errata in
  `feedback-phase3-validation`. This audit assumes those values are
  correct; it only re-classifies their *labels* and *Basis text*.
- **Korean mirror block-parity verification.** Any edits performed
  in response to this audit must run `bash scripts/check-mirrors.sh`
  and `python3 scripts/phase3/build_html.py` before commit.
- **Bibliography completeness.** Not in scope.
- **Other-planet (non-TRAPPIST-1) synthesis files.** Not in scope.

---

## Time spent

Approximately 1.5 hours of audit time (within the 1-2h cap). Findings
above are the complete output; no truncation.

## Suggested commit granularity

If the user approves edits:

1. **Commit 1** — c: option B (Canonical alternatives row + Basis fix); both en + ko.
2. **Commit 2** — h: Canonical alternatives row + Basis fix + tidal_heating value fix; both en + ko.
3. **Commit 3** — terminology sweep across all 7 planets; both en + ko.
4. **Commit 4** — mod-grounded field additions; both en + ko.
5. **Commit 5** — field-name rename if approved; both en + ko.

Per-stage commits make each policy change reversible individually.
