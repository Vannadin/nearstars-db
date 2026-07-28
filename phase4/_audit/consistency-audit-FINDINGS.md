<!-- 2026-07-28 페이즈 4 아웃풋 일관성 감사 결과 — 8축 병합 발견 목록 (읽기 전용 감사, 수정은 오너 선택) -->
# Phase 4 output consistency audit — FINDINGS

Run 2026-07-28 against `phase4/alpha_centauri.yaml` (82 rows) per
`consistency-audit-BRIEF.md`. Eight independent Opus auditors, one axis each
(physics couplings · prose rules · EN↔KO parity · refs/provenance · decision
honesty · fields/DB/viewer · deep style · out-of-scope serious-only), findings
cross-verified by the orchestrator with row-scoped greps and recomputation.
**Read-only: nothing was edited.** `check_phase4_gate.py` 0 errors,
`check_pipeline_flow.py` PASS at time of audit.

**Verdict on the brief's question ("do the rows read as one document written
by one hand?"): not yet — but the gap is small and concentrated.** ~70 of 82
narratives are genuinely uniform (Voice A). The residue: 2 narratives that
never received the prose pass, 1 equation-dump narrative, 13 evidence blocks
still in the pre-07-17 clipped register, a Korean mirror that breaks the
6-sentence cap the English respects (7 rows), and a terminology layer with
~12 concepts spelled 2–4 ways. The numeric backbone is solid — 30+ independent
recomputations all reproduce — and the dominant defect class is **corrected
values that never propagated to neighbouring rows**.

Locations are `line` numbers in `phase4/alpha_centauri.yaml` unless another
file is named. ✓ = independently re-verified by the orchestrator.

---

## 1. CRITICAL — in-scope (alpha_centauri)

**C1. Cassandra's radiation grade never propagated to the parent ladder.** ✓
`A b/environment.radiation` narrative L749 (EN) + L755 (KO): "Cassandra
low/낮음". Cassandra's own row (L2509, re-gated 2026-07-27), the belts row
(L670) and the magnetosphere row (L633) all say intermediate/중간. Found
independently by 4 auditors.

**C2. Cassandra `gameplay` evidence_ko contradicts evidence (EN).** ✓
L2562 EN: intermediate radiation, "shielding is required rather than
optional". L2563 KO: "방사선·열 위협 적어 탐사 우호적" — the retired low-grade
reading. The viewer defaults to Korean, so the owner-facing surface carries
the superseded claim. Highest EN/KO divergence on the board (char ratio 0.18
vs median ~0.42).

**C3. Retired `820× Io` live in 4 rendered spots; owning row says ~1200×.** ✓
Owning row L1406 (`~1200× Io`, note records 구값 820×). Stale: L1358 — the
**emit field** `Dante/bulk.internal_heat`; L762+L769 (`A b/environment.radiation`
evidence EN+KO); L1535+L1541 (`Dante/environment.radiation` evidence EN+KO).
Softened understatement "hundreds of times / 수백 배" at L745/L751.
Recomputation confirms ~1268× Io / ~11,800 W/m², i.e. 1200 is right.

**C4. Ring photometry is calibrated against the wrong observed radius,
undermining the gated 1.0 R_Jup.** `A b/rings` evidence: +0.05 R_Jup
equivalent disk (~23k km, τ≈9e-5) "matching the ~1.05 R_Jup observed flux".
But `bulk.radius` calls 1.05 a mis-transcription and keeps ring-free
1.1–1.15 R_Jup as the flux-required alternative. Cross-sections add as R²:
reaching 1.10–1.15 needs an equivalent disk 0.46–0.57 R_Jup (33–41k km),
τ ≈ 1.8–2.8e-4 — the gated ring is **2–3× too faint** to close the argument
that licenses radius 1.0. Two gated emit values depend on this.

**C5. Dante's 673 K surface cannot retain the sulfur its albedo, palette and
biome map are built on.** Elemental S melts at 388 K, boils ~718 K; at 673 K
ambient with only a tenuous SO₂ exosphere, exposed sulfur deposits evaporate.
The 2026-07-26 regrounding checked only the Draper point (798 K), never
volatile stability. Affects `surface` albedo note (황 반 ~0.5), `appearance`
"sulfur plains #d9c24a", `gameplay` biome "Sulfur Plains". Same defect class
as the already-fixed Chaos ice-stability bug.

**C6. The emitted Chaos orbit does not stay inside the ring gap that exists
for it.** ✓ Gap `1410000–1590000` (L810, designed around the 1.5M mean);
emitted snapshot `a_km: 1576906.3`, r 1.55–1.60M (L2958) — crosses the outer
annulus each orbit. Disclosed only inside the moons-table note; the rings
row's narrative, `ring_gap_km` field and clearance claim do not carry the
caveat.

**C7. Cassandra `magnetism.magnetic_field` asserts a gate that did not run.** ✓
`status: gated`, `criterion: [derived-grounding]`, `verdict: pass-in-window`
(L2441ff) while its own evidence says "The field STRENGTH is not derived, and
that is a gap rather than a value" (L2474) and the field note says 세기 미도출
(L2457). The narrative states the quantitative conclusion the evidence
disclaims ("still enough to hold off the outer belt… surface dose stays
low"), and `refs` cite `rocky-planet-dynamo-methodology.md` for a derivation
never run.

**C8. `Chaos/satellites` narrative is `None.` on the row that owns the
E-ring-supply decision.** ✓ L2769–2770. `A b/rings` evidence forwards the
reader there ("lives in Chaos.satellites, which owns the question"); the
row's fields/evidence carry the full assessment (424 m/s, 134 kg/s torus)
under an owner-override badge whose viewer legend promises an explanation.
Rule 6 (`없음.`) misapplied to a non-empty axis.

**C9. Chaos `surface`/`satellites` cite a methodology doc that does not cover
the load-bearing claim.** The sublimation-lifetime calculation (albedo 0.91 ⇒
134 K ice stable; 0.70 ⇒ gone in 4.5 Myr; 6.7e-11 kg/m²s outflux) comes from
the `docs/ice-stability.html` tool, which neither row cites;
`surface-color-albedo-methodology.md` (cited) contains no sublimation/ice
stability treatment (verified by opening it).

## 2. CRITICAL — out of scope (five other boards), flagged per the owner's "serious only" rule

**X1. Three text corruptions introduced by commit `4b8d73b`, two already
rendered into published viewer pages.**
- `barnards_star.yaml:15-18` — identity narrative mid-sentence deletion
  ("(GJ 699).5로 맨눈 불가…", dangling `.5로`, unbalanced paren). Rendered in
  `docs/phase4/barnards-star/barnards-star.html`.
- `proxima_cen.yaml:592-594` — `difficulty` **emit field** truncated to
  `"임무=항성간 플래그십 · 발견="`. Rendered in the Proxima b page.
- `40_eridani.yaml:544-550` — 40 Eri A b `appearance` gate.evidence cut
  mid-clause, unbalanced `(`, on a documented-divergence row.

**X2. Cross-board superlative contradictions (stale after later boards
landed).** 40 Eri C claims roster-max stellar J2 (1.6e-6) vs Fomalhaut 1.0e-4
which correctly names 40 Eri C as runner-up; Proxima claims roster-min J2
(3.7e-9) vs Barnard 2.2e-9 claiming the same, while 40 Eri B (2.1e-9) beats
both silently; Barnard claims 로스터 최고령 8.5 Gyr vs tau Cet's adopted
10 Gyr.

**X3. 40 Eri A d mean temperature 268 K (bulk/surface) vs 260 K asserted 4×
in the atmosphere row — including the emit-bound `escape` field — with the
atmosphere row citing the bulk row as its source.**

**X4. Proxima Cen d surface color: appearance row + `base_color` emit field
still derive from the retired `#34302c` after surface superseded it with
`#3c3833` (+ polar cap) — and drop the two-tone cap entirely.**

**X5. Discoverability retirement half-applied outside alpha_centauri:**
Proxima b's difficulty gutted (X1) while 40 Eri still carries `발견 TFFF`
tuples in 3 emit fields; narrative/evidence leftovers instructing a
ResearchBodies emit on proxima/40eri/fomalhaut (+`naked_eye=T T T T` in all
five identity evidences). One retired layer, four different states.

Also noted: `docs/phase4/` pages for these boards are stale (built from
`b31ecf7+미커밋`, three commits behind HEAD) — alpha_centauri pages were
verified content-current by byte-diff regeneration.

## 3. MAJOR — stale numbers / cross-row contradictions (in scope)

| # | Where | Says | Owning row says |
|---|---|---|---|
| M1 | `Hades/surface` ev L1733/L1745 | Dante ~650 K, 0.14 m lid | 673 K, ~0.12 m (L1399–1421). Physics note: with 1–5 % hotspots the ambient should itself drop to ~641–667 K — the Dante rows double-count ~5 % of the budget |
| M2 | `Cassandra/atmosphere` ev L2331/L2350 | magnetopause "33 R_p" | 23.5 R_p gated; 33 is the 500 µT counterfactual (L650) |
| M3 | `Pandora/magnetism.magnetosphere` L2075 + `A b/environment.radiation` L766 | "Earth-class" field | `Pandora/magnetism.magnetic_field` L2045 explicitly bans the label ("not 'Earth-class'") |
| M4 | `Hades/bulk.tidal_heating` narrative | "Pandora (860× Hades's mass…)" | gated masses give 770×; 860× is the rejected canon mass |
| M5 | `Chaos/surface` + `Chaos/satellites` ev | "20 R_p" | 21 R_p everywhere else (1.5e6/71492 = 20.98) |
| M6 | `A b/rings` ev | "NOT the epoch 179° snapshot" | 179° is the design value; snapshot is 176.475 |
| M7 | `A b/environment.radiation` | Dante extreme (>4,500 rem/day) > Hades severe | both rows compute identical 7,200 rem/day; Hades ev: "the same grade as Dante"; belt peaks at Hades |
| M8 | `Cassandra/atmosphere` ev | Titan at "a fourteenth of this mass" | 1.345e23/9.0e23 = 1/6.7 |
| M9 | `Cassandra/magnetism` ev L2475 | "core is 0.151 M⊕ vs Pandora's 0.645" | both are **total** masses; no core mass exists on the board (the BRIEF's open item inherited the error) |
| M10 | `A b/bulk.obliquity` ev | moons "keep the design-of-record ~9–11° / ~176/179°" | emitted table: 10.996/17.863/18.041/168.241/176.475 |
| M11 | `A b/appearance.aurora` vs belts/`Pandora/appearance` | aurora faint because the quiet star supplies little plasma | belts are source-dominated by Dante's torus; Pandora gets a "Jupiter Io-torus strong-aurora analog" from the same plasma. Internally-driven channel unaddressed |
| M12 | `Chaos/gameplay` | "Chaos runs against the other moons" | Cassandra is also retrograde (168°, near-coplanar) — and **no Cassandra row states its retrograde orbit** |
| M13 | `Pandora` vs `Cassandra` `environment.radiation` | both now "중간" | ladder rungs collapsed after Cassandra's upgrade; Pandora is gap-shielded, Cassandra belt-submerged — same word, different physics |

Minor same-class: Dante libration ±0.6° should be ±1.15° by the 2e formula
Hades uses; Pandora field "~1.8×/두배 지구" vs 75/31 = 2.42× (1.8 is the
moment ratio); solar J2 2.18e-7 vs 2.1e-7 in one evidence block; Pandora
atmosphere 1.1 atm vs "canon ~20% 빽빽" note (undocumented divergence) and
290 K field vs 291 K chain; A b field 170 µT vs evidence 172 µT; Cassandra
243–263 K range propagates a question `appearance` already closed (haze
gated present ⇒ 243 K); "Cassandra shepherds the inner edge" (3:2 ratio
would justify it; nowhere stated).

## 4. MAJOR — prose rules & EN↔KO parity

- **KO sentence cap:** 7 `narrative_ko` exceed 6 sentences while EN complies —
  `bulk.radius` 8, `atmosphere` 8, `appearance.banding` 9, `appearance.aurora`
  7, `magnetism.radiation_belts` 9, `rings` 8 (all A b), `Pandora/bulk` 9.
  Cause: KO splits EN colon/semicolon clauses; cap was enforced on EN only.
- **Em-dashes: 46 rendered** ✓ (narrative 1 — `Chaos/gameplay` L2817;
  evidence 17; evidence_ko 7; fields notes/values 21 — SPEC §3.1 covers
  rendered fields too). Brief said 26; fields were uncounted.
- **덱 calque ×4** ✓ (L376, L432, L469, L495) — SPEC's named counter-example;
  L376 sits two sentences from the correct 구름층. Polyphemus KO carries
  ~a dozen untranslated English nouns (zone, belt, azure, festoon…); moon
  bodies' KO is naturalised.
- **Pre-pass survivors:** `orbit.semi_major_axis_au` + `orbit.eccentricity`
  narratives (blame 07-10/07-17 vs ≥07-24 for all 80 others) — telegraph
  register, arrows, surname, "Canonical alternative", at rows 2–3 of the
  flagship page. `B/bulk.geopotential_j2` narrative is an equation dump whose
  A twin is prose (not on the brief's sanctioned list); A/B
  `spin_axis_orientation` pair splits telegraph/prose the other way.
- **EN ladder duplicated** in `A b/environment.radiation` (sentences 1 and 4;
  KO has it once — the two languages carry different content).
- **Gameplay shape:** `A b/gameplay` decides 6 biomes but lists none in
  prose (part 2 of the three-part shape missing); `Cassandra/gameplay` lists
  6 with zero descriptors where the other four moons all carry them.
- **없음 policy:** `Hades/magnetism.magnetic_field` and `Hades/atmosphere`
  pad a sentence where the Chaos precedent says `없음.`; C8 is the inverse.
- **Narrative meta/pointer leaks:** "The old split had it exactly backwards"
  (L957, provenance content), "replaces the silent default… with an explicit
  decision" (L1162), "recorded alternative"/"on record" (L179/L429);
  cross-row pointers "the orbit row"(L85, EN only — KO drops it, leaving the
  Korean reader without the referent), "clouds row"(L430/439), "A's matching
  row"(L1092/1096).
- **EN-side regex damage:** `Hades/bulk.tidal_heating` ev L1672 `k2/Q =
  1e-3.1e-2` (KO correctly `1e-3~1e-2`); same block + `radiation_belts` ev
  L712–723 de-Unicoded (`x`, `->`, `>=5e2x`, `--`) while their KO halves keep
  `×→⁴`. Typo `"drama,."` L527 ✓.
- **Identity template split 3/1/1:** fiction disclaimer verbatim on
  Dante/Hades/Pandora, paraphrased on Cassandra, **absent on Chaos** — which
  also never gives its formal designation.
- Stale KO subject: L471 "금색은…오너 조정" vs EN "chromophore set to…" (the
  retired gold-haze reading).

## 5. MAJOR — 임의 값 labelling & verdict semantics (decision honesty)

- **Unlabelled picks** (model: A's 7° = "An arbitrary value / 임의 값"):
  Chaos obliquity 15° (L2620, brief's open item, confirmed), Polyphemus
  obliquity 5° (L260ff — long story on why 27° died, never says 5° is
  picked), Cassandra obliquity 20° (L2276, evidence supports "≠0" not "20"),
  rotation periods Chaos 9.5 h + Cassandra 39 h (evidence justifies
  non-synchronous, never the number; Chaos's gated f and J₂ are computed
  **from** the pick), albedos Cassandra 0.35 (word "albedo" absent from its
  evidence) + Pandora 0.30 (analogy only). Honest counter-examples exist on
  the same board (Dante/Hades/Chaos albedos).
- **Verdict asymmetry:** `orbit.eccentricity` (pass-in-window) vs
  `orbit.inclination_deg` (documented-divergence) for the identical
  Kozai-driven departure from the observed value.
- **Passthrough rows that set:** A/B `bulk` anchors are `passthrough` yet
  carry derived `flattening` with `op: set` (L1285, L1305) ✓.
- **Narrative asserts what evidence labels art:** `A b/rings` narrative
  states the Chaos plume feed as mechanism ("feeds the ring with cryovolcanic
  plumes the way Enceladus feeds…") while its evidence marks the feed ART
  DIRECTION and C8's row says no groundable mechanism supplies that
  brightness; echoed in 4 Chaos narratives. The art label reaches **no**
  narrative on the board.
- **Endpoint pick unexplained in rendered layer:** `Hades/bulk.tidal_heating`
  adopts the low end of a 10× band; only unrendered provenance says the owner
  chose it.
- `difficulty` authored on 3 rows (L2212, L2558, L2830, all ending in a
  dangling `·` ✓) though SPEC §0 defers the axis; absent on the other 3.
- Stale comment `# documented-divergence` on the aurora row whose verdict is
  `owner-override` (L553 vs L571) ✓. `driver:` vocabulary free-form (19
  tokens vs SPEC §1's five classes; `physical`/`physics`, `emit`, …).

## 6. MAJOR — viewer/builder layer ✓

- `na_reason` never rendered (builder reads value/unit/…/op only): the three
  `geopotential_c22: null` rows show blank cells — exactly what §3.2
  introduced the key to prevent.
- Field-level `verdict` renders only `documented-divergence`
  (`build_phase4_html.py:78`): `banding_morphology`'s **owner-override**
  displays unbadged under a "허용 범위 내" pill — the legend's honesty promise
  broken at field level.
- `A b/satellites` is v1-shaped (row-level `value:`, no `fields:`) in a v2
  file ✓ — builder renders nothing for it; its narrative points readers at
  `stability_scans`/decision blocks the builder also drops (~90 lines,
  including the `designations` map). SPEC §3.1's "renderer reads only
  narrative/fields/refs/gate" claim is inaccurate in both directions.
- Build stamp records HEAD-at-build-time (`b31ecf7+미커밋`), not content
  identity — misleading as a staleness signal (alpha_centauri content itself
  verified current by regeneration byte-diff).
- Emit hygiene: `gravity` unit split m/s² (5 bodies) vs g (3); base-colour
  slot named 4 ways (`banding_base`/`color`/`base_colour`/`surface`); 28
  field names unmapped in `field_alignment.yaml` (25 from this board — belt
  geometry set, `cliff_height`, `neutral_torus_supply`…) that can never
  override Phase 3; `cliff_height` parked on Chaos's `identity` axis;
  Cassandra folds `magnetosphere` into `magnetic_field` where
  Polyphemus/Pandora have dedicated rows.
- `40_eridani.yaml`: `fictional: true` on 40 Eri A c/d **which exist in
  `db/systems/40_eridani_a.json`** ✓ — divergent practice vs alpha_centauri
  (invented moons kept out of DB per SPEC §3), and
  `check_pipeline_flow.is_fictional()` is one-directional (only consulted for
  db-missing bodies) + accepts the flag on any row (docstring says identity).

## 7. MAJOR — refs & provenance

- **Sibling parity gaps** (same defect the brief's §G worked example had):
  `surface` refs — Dante ∅, Pandora ∅, Cassandra ∅ vs Hades 3 refs ✓ (Dante
  is the sharpest: same 2026-07-26 pass, same energy-budget logic, zero
  refs); `environment.radiation` — Chaos ∅ vs 4 siblings {RB, MG} ✓;
  `appearance` — Dante/Hades/Chaos ∅ vs Pandora/Cassandra cited, though all
  three commit hex palettes+albedos; A vs B `environment.activity` (4 vs 2)
  and `appearance` (4 vs 2) — the missing ones are pair-covering papers;
  `A b/orbit` cites 1 of the 2 sim docs its three orbit siblings cite.
- **Inline citations not in refs[]:** `bulk.geopotential_j2` evidence carries
  arXiv 1109.1627 (+2007.10783, 1609.06324) inline ✓; `magnetism.magnetic_field`
  carries 1007.1514 ✓; "Kennedy 2011" (rings) has no identifier anywhere.
- **Cited doc ≠ claim:** C9 above; `STABILITY_REPORT.md` contains no
  obliquity (`_obliq5`), PA-match, or ring-clearing sections though three
  rows cite it for exactly those; `rocky-planet-dynamo-methodology.md` cited
  out-of-domain for icy Chaos.
- **Path errors in evidence prose:** `scripts/scan_pa_match.py` etc. — real
  location `phase3/stability-sim/scripts/` ✓; `results/_ring_clearing` is a
  `.log` file, not a directory ✓.
- **All 20 file-path refs[] resolve; all 24 bibcodes/arXiv ids well-formed**
  (note: `docs/phase3/_papers/` is arXiv-keyed — bibcode "resolves in cache"
  is not a usable gate).
- **Provenance:** `A b/rings` block over the 4-line budget and ordered
  06-21 → 07-28 → 07-27 against "newest last"; `Cassandra/atmosphere` carries
  a session detour that belongs in context-notes. Other 17 blocks compliant.
- **22 refs-less gated rows** (= the gate's warnings): 10 are all-gameplay +
  4 moon identities → one policy call (exempt in SPEC or standing refs);
  the rest are physics claims with zero grounding (`Dante/surface`,
  `Pandora/surface`, `Cassandra/surface`, `Chaos/environment.radiation`,
  `A/bulk.spin_axis_orientation`, `A b/appearance.clouds` …).

## 8. Style layer (deep audit; full concordance in the agent report)

- **Terminology with ≥2 renderings (12+ concepts):** 조석고정 15× vs 조석 고정
  4× ✓ (the 4 all in moon-bulk narrative_ko); 가스자이언트/거대 가스행성/
  거대행성/가스행성 (flagship identity disagrees with every other narrative) ✓;
  방사선대/벨트/내대·외대 split across the 5 sibling radiation rows;
  자기권계면/자기권 경계/자기 거품의 코 + bare "standoff" untranslated in KO
  L640 ✓; Polyphemus/폴리페무스 and Pandora/판도라 split across sibling
  evidence_ko; 안쪽/내측 위성들 in consecutive sentences (Cassandra bulk
  L2264–2265); Dante's two temperatures as 400/700 °C in one row and
  673/973 K in the next; Teq vs T_eq; `1e5 yr` vs `1000yr`; EN ALLCAPS (18×)
  vs KO `**bold**` (7×, Cassandra only ✓ — `**` may render literally).
- **Session seams:** narratives span 4 eras but hold voice except the 2
  pre-pass rows; **13 evidence blocks untouched since 07-17** sit in clipped
  fragments beside 07-27 multi-paragraph essays (Dante bulk/magnetism, Hades
  bulk/magnetism, Pandora env.radiation, Cassandra bulk/surface/gameplay-KO,
  Chaos bulk/atmosphere/appearance/gameplay, A spin-axis-EN). A datable
  second hand inside Era 2: the four British spellings (recognisable L878,
  Vapour L2636, colour L2712, neighbour L2817 ✓) + the lone narrative
  em-dash, all blame to 07-27.
- **Sibling-set verdicts:** gameplay 5× = parallel (best set); appearance 5×
  = acceptably varied; identity 5× = incoherent (see §4); bulk 5× =
  incoherent ("invented" opener on 2 of 4 invented-mass moons); A/B
  appearance + magnetic_field = parallel; A/B geopotential_j2 +
  spin_axis_orientation = incoherent.
- **Tone evenness by body (most→least):** Cassandra · Dante · Hades ·
  Pandora · A · B · Chaos · **Polyphemus** — the flagship page is the least
  even (telegraph at rows 2–3, poetry at 6–8, numeral dump at 18:
  `radiation_belts` narrative carries 9 raw numerals while its adjacent
  `magnetosphere` sibling tells the same story with zero).
- **Evidence register outliers:** narrative-flavoured evidence worst 5 =
  Cassandra atmosphere 340w / Hades tidal 288w / Cassandra appearance 241w /
  Chaos satellites 229w / Cassandra magnetism 205w; identity evidences are
  bare assertions ("An Io-type volcanic world.", 26 chars, no check no ref).

## 9. Open items from the brief — status after audit

| Item | Status |
|---|---|
| Rule 4 (workflow-vocab ban) not in SPEC/skill/memory | **Closed 2026-07-28** (same session as this audit): codified into SPEC §3.1, skill Step 4 and the prose memory, together with the owner's clarification that ~6 sentences is a yardstick, not a hard cap. Boards already comply (strict tokens zero board-wide ✓). |
| Cassandra field strength underived | **Worse than briefed:** the gate row now asserts pass-in-window on an unrun derivation (C7), and the brief's own "0.151 M⊕ core" phrasing inherited the total-mass mislabel (M9). |
| Pandora ocean dissipation unquantified | Honestly flagged in `atmosphere` evidence; narrative presents 290 K as settled (one hedging clause would do). |
| Chaos obliquity 15° unlabelled | Confirmed — and the sweep found 4 more unlabelled picks of the same class (§5). |

## 10. Verified clean (what the audit established positively)

- Gate 0 errors; pipeline PASS; YAML parses; zero duplicate (body×axis); no
  illegal status/verdict values; exactly one documented-divergence row,
  properly noted.
- `fictional: true` exact on this board: precisely Dante/Hades/Pandora/
  Cassandra/Chaos, identity rows, none in db; pipeline exemption matches.
- DB parity exact for every A/B/A b passthrough value checked (masses, radii,
  P_rot, ages, Teff, activity indices, cycle lengths, i★, wind total).
- ~30 independent recomputations reproduce: belt SDF geometry decoded from
  `fit_belts.py` matches the stated L-shells and every moon placement; tidal
  heating all four bodies; all Teq/energy-budget chains; Roche/Hill;
  spin-orbit ratios; figure chain (J₂/C₂₂/f/q) all 8 bodies; wind split;
  magnetopause scaling; ring optics internal algebra; orbit rewind 90.05°;
  designations map.
- Strict rule-4 tokens: zero in all narratives, both languages. No bibcodes/
  file paths in narratives. Owner-decision dates: zero in narratives.
  Provenance discipline 17/19 compliant. KO: zero 합니다체, zero
  sentence-ending colons, zero missing `_ko` fields; numeric parity zero
  drift beyond the items reported.
- 8 of 11 override rows pass the honesty bar outright (Chaos surface +
  satellites evidence = reference standard; Pandora bulk; A b clouds/aurora/
  banding-field; A/B stellar_wind); failures are localized to the narrative
  slot, not the evidence.
- alpha_centauri viewer pages byte-identical to a regeneration from current
  YAML (stamp aside). All file refs resolve.

## 11. Suggested sequencing (owner's call — nothing has been edited)

1. **Out-of-scope corruption repairs (X1)** — three surgical row-scoped
   fixes; two are live on published pages. Then rebuild the five stale
   board pages.
2. **Mechanical stale-value sweep (in scope):** C1, C2, C3, M1, M2, M3, M4,
   M5, M6, M8, M9, D-class glyph damage (L1672 `1e-3.1e-2`), typo L527.
   All row-scoped edits with the three post-edit checks from the brief.
3. **Owner decisions needed (not mechanical):** C4 ring brightness vs the
   1.0 R_Jup argument; C5 Dante sulfur vs 673 K (palette/biome/albedo);
   C6 gap geometry vs emitted orbit; C7 Cassandra dynamo (derive a number or
   re-gate honestly as owner-override/open); M7 Dante-vs-Hades ladder
   wording; M11 aurora story vs torus budget; M13 ladder rung naming;
   annotate M10 design-vs-snapshot policy in the prose rows that state it.
4. **Prose/voice pass:** the 2 orbit narratives + B J2 (+ A/B spin-axis
   leveling); 7 over-cap KO narratives; 46 em-dashes; 4 덱 + Polyphemus KO
   noun sweep; identity template unification (Chaos disclaimer/designation);
   `없음.` policy on Hades's two rows + a real narrative for C8; biome list
   into `A b/gameplay`; Cassandra gameplay descriptors; 임의 값 labels (§5);
   art-label clauses into the rings/Chaos narratives; terminology
   concordance picks (§8); evidence-register trim of the worst 5.
5. **Builder/schema:** render `na_reason`; badge field-level overrides;
   v2-ify `A b/satellites` (or render row `value:`); difficulty policy
   (SPEC defers it — remove or un-defer); driver vocabulary; gravity units;
   field_alignment mapping for the 25 unmapped names.
6. **Contract updates (SPEC/skill/memory):** codify rule 4; renderer-keys
   sentence in §3.1; refs policy for gameplay/identity axes; fictional-flag
   direction (40 Eri practice vs SPEC §3); note the arXiv-keyed cache limit.
