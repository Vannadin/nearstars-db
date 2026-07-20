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
