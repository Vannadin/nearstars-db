# Phase 3 Integrity Audit — 2026-06-03

Full re-audit of all 63 `docs/phase3/*.md` reports after the user distrusted
Phase 3 representation/analysis accuracy. Method: agent-team per-report audit
(every Decisions row vs cached papers, offline) → **main-thread verification**
(deterministic grep / recompute / DB-compare; targeted paper reads). Two seed
probes (Barnard, Fomalhaut) were manually confirmed first.

**Artifacts:** `_scratch/findings-all-63-2026-06-03.json` (430 raw candidate findings),
`_scratch/triaged-2026-06-03.json` (auto-adjudication), `_scratch/static-flags-2026-06-03.json`
(Phase 0). No repo code/DB modified.

## How to read this
The agent pass produced 430 candidate findings (43 high / 178 med / 209 low),
but it **over-flagged**: deterministic verification **refuted 120 of 230**
cache-presence flags (the cited paper was actually present) and several
high-severity flags on flagship reports were legitimate documented divergences.
Trust the **CONFIRMED** list below; the **REFUTED** list is recorded so the
same false alarms aren't re-raised.

---

## CONFIRMED — real, actionable

### HIGH
1. **Barnard's Star — Phase 2↔3 desync.** DB has 4 confirmed planets (Basant
   2025, `2025ApJ...982L...1B`); Phase 3 has **0 planet reports**. Host narrates
   them as González 2024 "candidates" and doesn't cite Basant 2025. Cause: the
   2026-05-28 revert (`a2ef49c`) → 05-30 host-only rebuild. *[manual]*
2. **Teegarden's Star — same desync.** 3 DB planets, 0 reports. *[Phase 0 / agent]*
3. **Fomalhaut — disk geometry wrong vs source.** Intermediate belt 60–110 AU
   but Gáspár 2023 ([arXiv:2305.03789](https://arxiv.org/abs/2305.03789)) says **83–104 AU**; the ~78 AU gap is
   missing; inner-belt inclination "~67.5°" but paper says **47.8°** (the
   misalignment is the paper's headline result); intro prose "40–80" contradicts
   the table. Root cause: `_bib/fomalhaut.yaml` = 5 stellar-param papers, **0
   disk papers**. *[manual vs paper]*
4. **hd-219134-h — surface_gravity 4× too high.** Report 3.8 g⊕; G·M/R² with the
   report's own 0.34 M_Jup, 0.95 R_Jup = **~0.95 g⊕** (9.34 m/s²; verified
   against Jupiter/Saturn). *[recompute]*
5. **gj-896-a-b — surface_gravity ~12× too high.** Report 58 g⊕ ("570 m/s²");
   G·M/R² with 2.26 M_Jup, 1.1 R_Jup = **46 m/s² ≈ 4.7 g⊕**. *[recompute]*
6. **eps-eri-b — mass double-deprojected.** Report 0.78 M_Jup / 248 M⊕,
   "deprojected from M sin i ≈ 0.66 M_Jup". But DB/Llop-Sayson 2021 0.66 M_Jup
   (**209.77 M⊕**) is already the **true mass**; treating it as M sin i and
   re-deprojecting inflates it ~18%. *[DB + report]*
7. **proxima-cen-b — ko block parity broken.** en=43 / ko=41; HTML build/mirror
   integrity. *[Phase 0]*

### MEDIUM
8. **Systemic: disk-host geometry rows are not offline-verifiable.** The disk
   Decisions block cites disk papers absent from bib+cache for **Fomalhaut, 61
   Vir, Vega, tau Cet, HD 69830** (61 Vir's `disk_present`/radii flagged high).
   Only **Fomalhaut is confirmed wrong** (#3); the others are **UNVERIFIED** —
   values may be correct from `db/disks_curated.json` but can't be checked
   offline. Needs disk-bib backfill, then verify. (eps Eri is clean — audited
   2026-05-29.) *[grep]*
9. **hd-69830 — prose vs table spectral-type inconsistency.** Decisions table +
   DB = **K0 V** (correct cfg value); intro prose calls it "G8V". Internal
   inconsistency only. *[grep]*
10. **proxima-cen-b/d — equilibrium_temp ~10% off recompute.** b: report 226 K
    vs 278.3·L^¼/√a = 251 K; d: report 357 K vs 325 K. Minor; check which L/a
    the report used. *[recompute]*
11. **~78 decision rows cite sources absent from bib+cache** (after removing the
    120 false positives). Mostly `atmosphere_present`/`composition` synthesis
    calls (judgment, not measurement) + orbital params from recent uncached
    papers (au-mic Mallorquin 2024, Hirano 2020). Coverage gap, not proven
    error. See `triaged-2026-06-03.json` UPHELD set. *[grep]*

---

## REFUTED — agent false positives (do NOT act on these)
- **120 / 230 cache-presence flags**: the cited paper IS in `_papers` or the bib;
  the audit agent failed to find it.
- **proxima-cen-b/d angular diameter**: 1.55°/2.61° vs report 1.5°/2.5° — within
  4%, correct.
- **hd-219134-h angular diameter & T_eq**: recompute matches report exactly.
- **au-mic-e mass**: report 21.1 M⊕ = DB (Donati 2025). Source + value match.
- **alpha-centauri-a age**: cfg 5.3 Gyr (Joyce & Chaboyer 2018) is correct and
  the DB-erratum is *intentionally documented* in Open items — not a desync.
- **trappist-1-f "Wolf 2017 1 bar branch"** & **trappist-1-g water_mass_fraction
  0.11–0.50 (Bourgeois 2024 / Unterborn 2018)**: these match the project's own
  canonical examples in `conflict-resolution.md` verbatim. Correct attribution;
  the agent over-classified an UNVERIFIABLE-offline as WRONG_ATTRIBUTION.

---

## Previously-deferred — now VERIFIED (all 7 CONFIRMED real, 2026-06-03)
Checked against cached papers / report lines / DB. **Zero false positives** in
this set (it was the high-severity non-cache residue, higher quality than the
auto-flagged bulk).

- **proxima-cen `magnetic_dipole_strength_kG` (0.6) + `magnetic_total_field_kG_rms`
  (4) — WRONG_ATTRIBUTION (high).** Cited to Reiners 2018 (`1711.06576`), which
  has **0 "kG" mentions** — it is a 324-star RV/spectral-atlas survey, not a
  Proxima magnetography paper. Values must be re-attributed (Reiners & Basri 2008
  / Klein 2021) or marked unverified.
- **proxima-cen-b `atmosphere_composition` — VALUE_MISMATCH + INTERNAL (high).**
  Decisions row "CO₂ 5%"; Boutle 2017 (`1702.08463`) Table = CO₂ MMR 5.941e-4
  (**~376 ppm, trace**), and the report's OWN prose (line 124) says "376 ppm CO₂".
  ~130× overstated.
- **proxima-cen-b `magnetosphere_standoff_planet_radii` (1.5) — VALUE_MISMATCH
  (high).** Garraffo 2022 (`2211.15697`) line 83: standoff "between approximately
  3 R_p and 11 R_p". 1.5 matches nothing.
- **trappist-1-e/f `surface_radiation_dose_msv_yr` (12000 / 7000) — VALUE_MISMATCH
  (high).** Atri 2019 (`1910.09871`) table gives **per-event Gy** (e 3.9e-3, f
  2.25e-3 at ~1 bar) / dimensionless enhancement factors — not Sv/yr. The 12 / 7
  Sv-yr figures are a misderived annualization, wrongly marked "high".
- **trappist-1-f ocean vs surface-temp — INTERNAL_CONTRADICTION (high).**
  `ocean_present`=true + open-water lens, but `surface_temp_substellar_k`=260
  (13 K below freezing). The hottest point can't hold open water at 260 K.
- **au-mic-b/c tidal lock vs eccentricity (medium).** b forces 1:1 at e=0.07; c's
  prose says "fully locked 1:1" while its Decisions row correctly says "3:2 /
  pseudo-sync" at e=0.18. Violates the eccentric-lock gate / self-inconsistent.
- **vega `age_gyr` — INTERNAL_CONTRADICTION (high).** Decisions 0.7 Gyr (Monnier,
  = DB) but Open-items line 148 says "cfg adopts the Yoon headline" (0.455) and
  intro line 48 says "0.45 Gyr"; also mislabels Yoon (non-rotating) as "rotating".
- **hd-69830 `disk_mass_mearth` (4e-4) — INTERNAL + DESYNC (high).** Matches
  neither its own basis (6e-5) nor DB (`disks_curated` 6e-5 Beichman / 1e-3 Lisse).

---

## Fix backlog (SEPARATE approval — not part of audit)
- **F1** Barnard b/c/d/e + Teegarden b/c/d planet Phase 3 reports (new synthesis).
  Update Barnard host to cite Basant 2025, reframe as confirmed.
- **F2** Fomalhaut disk geometry fix (values in hand) + disk-bib backfill.
- **F3** Two surface_gravity arithmetic errors: hd-219134-h (→0.95 g⊕),
  gj-896-a-b (→4.7 g⊕); recheck downstream scale_height/density.
- **F4** eps-eri-b mass → 0.66 M_Jup / 209.77 M⊕ (DB/Llop-Sayson true mass).
- **F5** proxima-cen-b ko block parity (en43/ko41).
- **F6** Disk-bib backfill for 61 Vir / Vega / tau Cet / HD 69830, then verify
  geometry (may be fine from disks_curated).
- **F7** hd-69830 prose G8V→K0V; proxima T_eq recompute.
- **F9** proxima-cen `magnetic_dipole_strength_kG`/`magnetic_total_field_kG_rms`:
  re-source (Reiners 2018 [1711.06576](https://arxiv.org/abs/1711.06576) is wrong) or mark unverified.
- **F10** proxima-cen-b `atmosphere_composition`: CO₂ 5% → ~376 ppm (N₂ + trace CO₂).
- **F11** proxima-cen-b `magnetosphere_standoff_planet_radii`: 1.5 → 3–11 R_p (Garraffo 2022).
- **F12** trappist-1-e/f `surface_radiation_dose_msv_yr`: re-derive from Atri 2019
  (per-event Gy, not Sv/yr); current 12000/7000 + "high" confidence are wrong.
- **F13** trappist-1-f: reconcile open-water lens with 260 K substellar (raise the
  temperature basis or drop the open-water claim).
- **F14** au-mic-b: pseudo-synchronous not 1:1 (e=0.07); au-mic-c: fix prose to
  match the 3:2 Decisions row (e=0.18).
- **F15** vega `age_gyr`: reconcile to the Decisions value 0.7 Gyr (Monnier, = DB);
  fix Open-items/intro contradictions + Yoon "rotating" mislabel.
- **F16** hd-69830 `disk_mass_mearth`: 4e-4 → 6e-5 (DB Beichman recommended) or
  document the 6e-5–1e-3 range.

## Audit-quality note
Confidence in this report comes from main-thread verification, not the raw agent
output. The agent pass was a **finder** (high recall, low precision); the
deterministic + targeted verification was the **filter**. Per-finding verify
agents were abandoned (cost). See `RESUME-2026-06-03.md` and
`feedback_audit_cost_discipline` memory.
