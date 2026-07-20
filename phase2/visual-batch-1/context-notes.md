<!-- 시각 다양성 배치 1 — 결정·근거 기록 (선정 사유, richness 정책, 시스템별 메모) -->
# Visual-richness batch 1 — context notes

## Why this batch
User wants visually-interesting systems for KSP, chosen from the Phase-1
(already-in-DB, NASA-archive auto-fill) layer, ranked by *visual* interest,
not academic importance. Escalating 6 of them to Phase 2 + Phase 3.

## Curation policy in force (2026-05-31)
`[[feedback-gameplay-variety]]`: bias toward gameplay variety. Include a body
unless the truth is genuinely "nothing there" (fabrication / full retraction /
superseded). So:
- **Disputed/tentative bodies are IN** unless severe — e.g. GJ 9066 c is an
  M sin i RV signal (Feng 2020), kept.
- **Moons: add several** for gameplay — but moons are NOT real (no confirmed
  exomoons), so they live in the **cfg/Kopernicus layer (downstream), flagged
  artistic**, NOT in the measurement DB (db/systems stays reality). Validate
  dynamics with `[[project-nearstars-stability-sim]]`. Tracked here, handled
  when the cfg writer runs (out of add-star scope).
- Excluded only: fully-retracted (Barnard b style) or fabricated-source
  (delta Pav disk style). `[[project-nearstars-ring-fabrication]]` search-and-
  verify still applies; the threshold is just lower.
- Value/recommended selection unchanged: method-priority + cache value-check
  (`[[project-nearstars-curation-contract]]`).

## Suggested order (near→complex blend)
1. **YZ Cet** — simplest (single M, 3 small rocky); establishes Phase2→3 pattern.
2. **eps Ind A** — nearest; scope call on brown-dwarf pair eps Ind B.
3. **GJ 9066** — verify RV signal robustness first.
4. **GJ 896 A** — binary (A+B) mutual orbit needed.
5. **HD 219134** — 6 planets, transiting rocky.
6. **55 Cnc** — most planets (5) + binary + the lava/ring showcase.

## Per-system open decisions (fill during pre-research)
- **eps Ind A**: include the brown-dwarf pair eps Ind B (Ba+Bb, ~1460 AU from A)
  as separate component(s)? Adds exotic bodies (richness ✔) but ~1460 AU is far.
  Decision pending pre-research.
- **GJ 896 A**: model A+B mutual orbit (binary_orbits.json). Is B a planet host too?
- **55 Cnc**: A (K0IV-V) + B (M4.5V companion, ~1065 AU). Binary block.
- **GJ 9066**: confirm Feng 2020 signal is a planet (not stellar-activity alias);
  M sin i only → true mass unknown, note in meta.
- **HD 219134**: confirm 6-planet count + which transit (b, c) vs RV-only.

## Gas-giant gap note
This batch finally adds visually-synthesized gas giants (eps Ind A b cold
super-Jupiter, GJ 896 A b, GJ 9066 c, 55 Cnc b/d). Before this, only eps Eri b
existed and its planet Phase 3 was deferred.

## Pre-research done (2026-05-31) — findings + decisions

All 6 are already in the DB at Phase 1 with `method: "unverified"` stellar
mass/radius and EMPTY teff/L/age/rotation/activity. So Phase 2 = re-anchor the
unverified M/R to proper method tiers + fill the empty high-impact categories
(rotation > activity > teff/R/L) + re-pin planet params per-paper.

**YZ Cet** (yz_cet, Gaia 2358524597030794112, single M4.0Ve, 12.1 ly)
- Planets b,c,d confirmed RV (Msini), no measured radius (non-transiting → radius is estimate only).
- DECIDE: EXCLUDE tentative "e" (1-day signal, superseded by Stock 2020 +229 RVs — not mild dispute, it's not-recovered). 
- Anchors: Stock 2020 ([2002.01772](https://arxiv.org/abs/2002.01772), params+rotation 68.4d), Astudillo-Defru 2017 ([1708.03336](https://arxiv.org/abs/1708.03336), discovery+alt), Cifuentes 2020 (VizieR J/A+A/642/A115, teff/L), Schweitzer 2019 (1904.06025, M/R). Aurora: Pineda&Villadsen 2023 ([2304.00031](https://arxiv.org/abs/2304.00031)) + Trigilio 2023 ([2305.00809](https://arxiv.org/abs/2305.00809), planet b B-field). No moons.

**eps Ind A** (eps_ind_a, Gaia 6412595290592307840, K5V, 11.9 ly)
- ⚠ DB has MALFORMED bibcode `2026arXiv260308780M` (Matthews 2026 = arXiv [2603.08780](https://arxiv.org/abs/2603.08780)) → fix on escalation.
- Planet b: cold super-Jupiter, mass migrated 3→6.3→7.6 MJ across RV→JWST. Anchors: Feng 2018 ([1803.08163](https://arxiv.org/abs/1803.08163)), Feng 2019 ([1910.06804](https://arxiv.org/abs/1910.06804)), Matthews 2024 ([2503.01599](https://arxiv.org/abs/2503.01599) Nature), Matthews 2026 ([2603.08780](https://arxiv.org/abs/2603.08780) best params). Atmosphere: NH3 + water-ice clouds (cold giant palette).
- DECIDE (richness): ADD the brown-dwarf pair eps Ind B (Ba T1 67 MJ + Bb T6 53 MJ, Gaia 6412596012146801152), Chen 2022 mutual orbit P=11.02yr a=2.406AU modeled; the A–B wide pair (~1460 AU) left UNMODELED per existing wide-binary convention. Needs B in astrometry_raw → full pipeline run.

**GJ 9066 = TZ Arietis** (gj_9066, Gaia 76868614540049408, M4.5V, 14.6 ly)
- IDENTITY: = TZ Ari = GJ 83.1 = LHS 11 = Karmn J02002+130. NO HIP (Wikipedia's HIP 14810 is WRONG). May need SIMBAD_ALIASES "GJ 9066"→"TZ Ari".
- Planet c (771d, Msini 0.21 MJ) CONFIRMED — Quirrenbach 2022 (CARMENES) independently recovered it. Sibling "b" (242d) = FALSE POSITIVE (refuted); 2-day signal = rotation artifact. KEEP c (mild dispute only). P_rot≈1.96d (fast active rotator).
- Anchors: Quirrenbach 2022 ([2203.16504](https://arxiv.org/abs/2203.16504)), Feng 2020 ([2008.07998](https://arxiv.org/abs/2008.07998)), rotation [2401.09550](https://arxiv.org/abs/2401.09550), Cifuentes/Schweitzer VizieR (Karmn J02002+130).

**GJ 896 A** (gj_896_a, Gaia 2824770686019003904, M3.5Ve, 20.4 ly)
- M+M binary WDS J23317+1956. DECIDE (richness): ADD companion B (Gaia 2824770686019004032, M4.5, 0.165 Msun) + model A–B orbit (Curiel 2022: P=229yr, a=31.6AU, e=0.108 [NOT circular — value-check], retrograde). B not in astrometry_raw → full pipeline. B may itself be unresolved binary (Winters 2021) — flag.
- Planet b: astrometric 2.3 MJ, P 284d (Curiel 2022, [2208.14553](https://arxiv.org/abs/2208.14553)). BACKFILL planet Ω=45.62° (null in DB).

**HD 219134** (hd_219134, Gaia 2009481748875806976 = HIP 114622 = HR 8832 = GJ 892, K3V, 21.3 ly)
- 6 planets b,c,d,f,g,h (NO "e" — lettering skips it; do not invent). b,c TRANSIT (rocky). DECIDE (richness): KEEP contested f,g (controv_flag=1 but NOT retracted; still in Harada 2025/Rosenthal 2021). h = cold Saturn ~3 AU → ring/moon candidate.
- ⚠ Radius will CHANGE: Ligi 2019 ([1909.10058](https://arxiv.org/abs/1909.10058)) interferometric R=0.726±0.014 vs DB 0.778 unverified → interferometry tier wins. Mass tiebreak (Ligi direct 0.696 vs evol 0.81) — surface.
- Anchors: Ligi 2019 (stellar/R), Gillon 2017 ([1703.01430](https://arxiv.org/abs/1703.01430), b/c), Motalebi 2015 ([1507.08532](https://arxiv.org/abs/1507.08532)), Vogt 2015 ([1509.07912](https://arxiv.org/abs/1509.07912), g/h), Johnson 2016 ([1602.05200](https://arxiv.org/abs/1602.05200), activity cycle 11.7yr). Fix g/h provenance bug (source says Gillon, bibcode Vogt). Wide M-dwarf companion ~700 AU = meta.notes only.

**55 Cnc** (55_cnc + 55_cnc_b BOTH already built; = rho1 Cnc = HD 75732 = HIP 43587)
- A (K0IV-V) 5 planets: e (lava USP), b (hot Jup), c, f, d (cold giant). B (M4.5V, ~1065 AU) ALREADY in DB AND now has 2 planets (Moutou 2026).
- ⚠ Moutou 2026 ([2510.11523](https://arxiv.org/abs/2510.11523), postdates cutoff) drives most planet masses + B's planets — value-check from cache before promoting unverified.
- Anchors: von Braun 2011 ([1107.1936](https://arxiv.org/abs/1107.1936), interferometric R=0.943/Teff=5196 — radius tier; DB's 0.943 is actually von Braun's, mis-attributed to Bourrier/unverified), Bourrier 2018 ([1807.04301](https://arxiv.org/abs/1807.04301), system+rotation+activity cycle), Moutou 2026 ([2510.11523](https://arxiv.org/abs/2510.11523)). e atmosphere: Hu 2024 (2405...), Demory 2016 ([1505.00269](https://arxiv.org/abs/1505.00269)). A–B orbit: separation-only (~1065 AU), leave UNMODELED.

**Moons (all systems):** downstream cfg/Kopernicus, artistic, stability-sim-vetted — NOT in measurement DB. Tracked, handled when cfg writer runs (out of add-star scope).

## Log
- 2026-05-31: pre-research complete (6 parallel agents). Starting Phase 2 with YZ Cet (simplest).
- 2026-05-31: YZ Cet DONE (Phase 2 commit 542cea8 + Phase 3 docs). Caught a 3rd arXiv collision (Schweitzer 1904.06025 was an ML paper → [1904.06860](https://arxiv.org/abs/1904.06860)). Branch hygiene: a parallel session had switched the shared checkout to docs/planet-pack-techniques; my YZ Cet commit landed there by accident → cherry-picked to new branch feat/visual-batch-1, restored docs/planet-pack-techniques to its PR tip (81a2cfa). All visual-batch work now lives on feat/visual-batch-1.
- NEXT: eps Ind A (Phase 2 + brown-dwarf pair decision) → GJ 9066 → GJ 896 A (binary) → HD 219134 → 55 Cnc.
- 2026-05-31: ALL 6 systems Phase 2 DONE (YZ Cet 542cea8; eps Ind A/GJ 9066/GJ 896 A/HD 219134/55 Cnc 6fc87aa — parallel-drafted, value-checked, FAIL=0). Caught: Lundkvist 2024≠Campante, Schweitzer arXiv collision 1904.06025→[1904.06860](https://arxiv.org/abs/1904.06860), HD 219134 d/f Gillon→Vogt re-source, GJ 896 binary e=0.108 (HTML table) not circular, von Braun/Ligi interferometric radius re-anchors. Phase 3 synthesis DONE for all (19 slugs, en+ko+html, parity OK).
- DEFERRED (richness follow-on, needs pipeline run): eps Ind B brown-dwarf pair (Ba+Bb, Chen 2022 orbit) + GJ 896 B companion + A–B orbit (Curiel 2022) — new components → target_list + run_pipeline + binary_orbits. Drafts/proposals captured in the draft-agent reports.
- Pre-existing (NOT this batch): proxima-cen-b en/ko block-parity drift (12 vs 11 headings, from old wiki commits b52e5db/1d1c43b) — flag for a separate fix.
