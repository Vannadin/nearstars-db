# Context notes — floor-backfill

Append-only. Started 2026-07-20.

## 2026-07-20 — program start

- Scope is the owner's: **all curated hosts ≤50 ly**, not roster-only.
- **Tiering was the useful move.** The raw "129 hosts below floor" reads as one
  huge program; the actual distribution is bimodal — 11 hosts need 1–2
  determinations (Tier A/B) while 112 have never had a Phase-2 pass at all
  (Tier D, 5–6 categories each). Sequencing A→D means the roster and the
  already-used planet hosts stop being the weak link early, and the long tail
  becomes a batched background program instead of a blocker.
- Tier A is only 2 hosts (40 Eridani C: activity + rotation; Fomalhaut:
  rotation) — the roster was in better shape than the headline number implied.
- **Checked before assuming a curation gap**: Sirius B / Procyon B / Van
  Maanen's Star each hold mass + radius only, while the WD floor also wants
  teff + age. These are famous, well-measured white dwarfs, so this is a
  curation gap and not a measurement gap — worth stating because the opposite
  case (floor asking for something nobody has measured) is a real possibility
  elsewhere in the list and should be recorded as an honest N/A rather than
  chased forever.
- First batch delegated: WD trio (teff + cooling age), rotation trio (Fomalhaut,
  40 Eri C, Delta Pavonis), age quintet (55 Cnc, GJ 9066, HD 219134, YZ Cet,
  eps Ind A). Agents research and return structured blocks; the main thread
  applies via `apply_phase2.py` and verifies.
- 40 Eri C carries prior history the agent was told to respect rather than
  rediscover blind: Shan 2024 P_rot 8.56 d was examined before and deliberately
  left uncurated as a quality-D value (it is nevertheless the input the stellar
  J₂ row uses, as a documented divergence). The agent was asked for a verdict on
  whether that exclusion still holds.

## 2026-07-20 — batch 1 applied (age quartet + WD trio; 129 → 122)

- All 14 bibcodes re-verified against ADS on the main thread before applying
  (first author + year + title match). Writes went through `apply_phase2.py`
  with the whole-entry pattern (current JSON entry + new block), `--check`
  first; 55 Cnc `meta_notes` confirmed preserved.
- **HD 219134 upgrade of note**: Li 2025 asteroseismic age (10.15 ± 1.72 Gyr,
  KPF RV oscillations) — the prior curation deliberately omitted age because
  models spanned 0.2–13.8 Gyr; the new measurement is the first asteroseismic
  age for a main-sequence star cooler than 5000 K.
- **Van Maanen textbook trap**: the ~7000–7500 K Teff in older references is
  superseded (Wolff 2002 UV line-blanketing); all 2009–2024 determinations
  cluster at 6100–6220 K. Recorded in the entry note.
- **Agent hallucination caught by the agent itself**: an ar5iv grab of
  Giammichele 2012 returned Teff 8250 K / 5.94 Gyr for vMa 2 — physically
  inconsistent (a 0.62 M⊙ WD at 8250 K cannot be ~6 Gyr cooled); rejected,
  noted in the DB entry so it doesn't come back.
- **GJ 9066 = the honest-null case the plan predicted**: no published age
  determination exists (queries: full:"GJ 9066" + age/gyrochronology/isochrone/
  kinematic/moving-group → 0 relevant results; 8-paper general sweep all
  non-age). Left null per the DB principle; worklist annotated. If more of
  these accumulate, consider a floor-N/A marker so gate 10d can distinguish
  "not yet curated" from "not measurable" — deferred until there are ≥3 cases.
- Cooling ages recorded explicitly as COOLING age in every WD note (total ages
  quoted where the paper gives them; Procyon total age contested 1.87 vs 2.7
  Gyr — affects total only).
- **Schema gate earned its keep on this very batch**: `wd_cooling_model` wasn't
  in the age-method whitelist and `notes` wasn't an allowed measurement key —
  gate 4d red. Resolution split correctly: wd_cooling_model is a genuinely
  distinct method → schema extension (documented in schema.py comment);
  `activity_age_relation`/`spectroscopic`/`photometric_fitting` were my
  vocabulary drift → corrected to the existing enums (activity_age,
  low_res_spectroscopy, sed_fitting). teff/age now allow `notes` (same
  precedent as rotation/radius). Phase-2 HTML rebuilt for the three new WD
  host pages (gate 7).

## 2026-07-20 — batch 2 applied (rotation/activity trio; 122 → 119, Tier A CLEARED)

- **40 Eri C: prior exclusion reversed on new evidence.** Shan 2024 8.56 d was
  left uncurated in May as an isolated grade-D photometric value. The agent's
  cross-check changed the picture: Pass 2023 v sin i = 1.7 ± 0.2 km/s with the
  curated Mann 2015 radius gives P/sin i = 8.2 d — independent spectroscopic
  corroboration. Curated with the quality caveat in the note; the J₂
  documented-divergence flag in body-figure-methodology (en+ko) is retired
  (the J₂ value itself is unchanged — same period, now curated).
- **Cross-paper computed values stay out of Phase 2**: the proposed
  log Lx/Lbol ≈ −3.2 for 40 Eri C combined NEXXUS Lx with Cifuentes Lbol —
  that is synthesis, not measurement. Dropped; the Lx is preserved as context
  inside the Hα entry's note.
- **Fomalhaut and Delta Pav both have NO published rotation period** (A-type
  with no spots to modulate; near-basal-activity subgiant likewise). Both are
  curated as v_sin_i-method entries with the derivation in the note — Fomalhaut
  is a true period (i★ measured = 90°), Delta Pav an upper limit (i unknown).
  This makes the previously project-internal Fomalhaut P ≈ 24 h derivation
  paper-anchored (Hadjara 2014 numbers re-verified against
  phase4/figure/fomalhaut-j2-research.md).
- All three implied periods re-derived on the main thread (0.979 d / 8.15 d /
  40.2 d & 25.7 d) — agent arithmetic confirmed.
- Schema: activity_measurements gains `notes` (same pattern as teff/age this
  morning). Gate 4d caught it again — three-for-three on this batch pair.
- **Tier A is now empty; Tier B has only GJ 9066 left (honest null).** Floor
  count 119, all remaining = Tier C/D long tail.

## 2026-07-20 — floor-N/A mechanism + Tier C/D wave 1 launched

- **floor_na marker implemented** (the ≥3-cases threshold was clearly about to
  be crossed by the D-wave age hunts): `stellar_props_curated[host].floor_na =
  {category: reason+query-pointer}`. Gate 10d counts these as "N/A (no
  published measurement)" instead of missing; schema allows the key;
  apply_phase2 preserves it if absent from YAML (same as meta_notes).
  Anti-fabrication rule in the schema comment: only with a query log, remove
  when a paper appears. GJ 9066 age = first marked case (118 below floor + 1 N/A).
- **Wave 1 fanned out** (3 agents): Tier C six (Altair, Sirius A, GJ 896 A,
  CWISEP BD, eps Ind Ba/Bb), Tier D M-dwarf 15 (famous planet hosts,
  catalog-first: Cifuentes 2020 / Schweitzer 2019 / Diez Alonso 2019 /
  Astudillo-Defru 2017 / Schöfer 2019), Tier D FGK 15 (bright stars,
  interferometric-first: Boyajian, Torres 2015 Capella, Mount Wilson
  rotation/activity, Mamajek & Hillenbrand 2008 ages). Schema enums embedded
  in the prompts this time — batch 1/2 lost a round-trip to enum drift.

## 2026-07-20 — wave 1 applied (Tier C 6 + M-dwarf 15; 118 → 97, a/bd classes cleared)

- 30 bibcodes re-verified against ADS on the main thread (Tier C 14 + M-dwarf
  16); Engle 2024 log-age conversions spot-recomputed (Kapteyn 10^1.061 =
  11.5 Gyr matches its independent kinematic halo age — good cross-check).
- **Null-entry convention enforced at the merge step**: the M-dwarf agent
  proposed "honest null" placeholder ENTRIES (value: null, method: unverified)
  — converted to floor_na markers instead (the DB principle is null-is-absent,
  and gate 10d now has a proper N/A channel). Also stripped a non-schema
  `l_value: ">"` key; lower/upper limits live in notes (GJ 667 C >100 d,
  LHS 1140 >5 Gyr, GJ 1061 >7 Gyr).
- floor_na added this wave: GJ 896 A teff (active close binary, absent from
  every catalog); CWISEP luminosity+radius; GJ 887 rotation (undetectable,
  240 ppm semi-amplitude); GJ 667 C radius (no primary measurement — S-B from
  its own L+Teff would be derived, not measured) + activity (S-index 0.48
  published but schema has no S-index key); GJ 1214 activity+age; GJ 1002 age;
  LHS 1140 activity; L 98-59 activity; Ross 128 age; Wolf 359 age. Total N/A
  now 14 categories.
- **Contested rotations recorded in notes, not resolved**: GJ 436 (44.6 vs
  Engle 71.4 d), GJ 273 (93.5 vs 160.8 d), Ross 128 (112.8 vs non-significant
  163 d), Kapteyn (83.7 vs 153/176 d). Where an Engle gyro age rests on the
  longer period, the age note says so (GJ 436, GJ 273) — Phase 3 consumers
  should read those notes before leaning on the age.
- CWISEP age is De Furio 2025's ASSUMED 1-10 Gyr field prior (midpoint 5.5,
  method=unverified) — a published adopted value, honestly flagged; not a
  measurement.
- Schema: luminosity gains `notes` (4th category this program; the whole
  *_measurements family now allows it consistently).

## 2026-07-20 — FGK batch 1 applied (97 → 93; 15 more N/A markers, total 29)

- **The tooling-limit vs N/A distinction did real work here.** The agent could
  not reach the rotation-period catalogs (Suárez Mascareño 2015/2016, Donahue
  1996 — not in TAPVizieR; ASU timeouts; digits absent from abstracts) for 9
  bright dwarfs. Those rotations stay MISSING on the worklist (data exists,
  we couldn't reach it), NOT floor_na. A main-thread attempt also failed
  (mesRot is v-sin-i-only; my catalog-code guesses hit the wrong tables).
  Follow-up: pull the CDS ftp ReadMe tables directly next session.
- **Dropped an unverifiable digit**: 61 Cyg A "35.4 d (Boro Saikia 2016)" —
  the abstract confirms the ZDI monitoring but not the number. Widely-quoted
  ≠ sourced; left missing rather than curating folklore.
- floor_na added: unresolved companions (70 Oph B teff/L/activity/rotation;
  eta Cas B all five — coeval-age inheritance deliberately NOT curated as a
  measurement) + giant-star index gaps (Capella/Arcturus/gam Cep activity —
  R'HK is uncalibrated for giants; Capella/Arcturus/gam Cep rotation).
- Arcturus luminosity stays missing (not N/A): ~170-200 Lsun is derivable but
  cross-computed; a direct-L paper certainly exists for one of the
  best-studied giants — follow-up item.
- 55 Cnc B fully missing still: Moutou 2026 abstract carries no Teff
  (main-thread checked); a paper-table read is the lead.
- **DB audit flag from the agent (recorded, out of scope here)**: the curated
  70 Oph A/B radius cites Boyajian 2008 (2008ApJ...683..424B) but that paper
  is "mu Cas A, sigma Dra, HR 511" — likely mis-citation in the mass/radius
  layer. Needs a dedicated audit pass.
- Capella note: DB "Capella" host = Aa clump-giant primary values (Torres
  2015); the Hertzsprung-gap Ab is not separately curated.

## 2026-07-20 — wave 2 applied (M-dwarf 15; 93 → 78, N/A 29 → 45)

- The solo-agent (no sub-branching) run worked cleanly — same coverage
  quality as wave 1, and FLOOR_NA declarations arrived pre-formatted per the
  updated prompt (no null-entry conversion round-trip this time).
- **Cross-ID work was the load-bearing part**: G 261-6 = GJ 1238 = J19242+755
  (Kaminski 2025 explicit — its catalog rows hide under GJ 1238); GJ 1148 =
  J11417+427 vs GJ 1151 = J11509+483 disambiguated; GJ 229 = J06105-218.
- Age reality for field M dwarfs confirmed: only 3/15 have a published age
  (GJ 15 A 4.12, GJ 229 A 2.82, GJ 1132 7.82 Gyr — all Engle 2024 gyro,
  log-dex converted, asymmetric errors kept in notes with uncertainty =
  larger side per the eps Ind A precedent). 12 age floor_na.
- GJ 251 rotation: 122 d (Stock 2020) recommended; the SuperWASP 18.1 d kept
  as a non-recommended alias entry so the disagreement stays visible.
- GJ 1132 discovery-paper radius (0.207, Berta-Thompson) deliberately NOT
  appended — the DB already carries the newer Weisserman 2026 radius and
  adding a stale non-recommended variant adds noise, not information.
- Radius filled for the 5 hosts that lacked it (Cifuentes S-B within-catalog
  values + Schweitzer seconds).
