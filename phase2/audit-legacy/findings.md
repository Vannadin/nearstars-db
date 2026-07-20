# Legacy Phase 2/3 audit — findings log

Auditing pre-discipline Phase 2/3 work (built before the 2026-05-28 postmortem +
curation-data-contract). This-session work (Tier 1 batch 2, Tier 1 stellar
re-synth, Tier 2, 40 Eri, disks) is already value-checked and excluded.

Method per host: value-check every `recommended` Phase 2 value + every Phase 3
Decisions row against the cached `_papers/<arxiv_id>.md` (or named VizieR
catalog). Flag the postmortem failure modes:
- fabricated bibcode (no ADS hit / wrong arXiv id)
- secondary-source misattribution (value actually from a different paper)
- false-negative ("no measurement exists" not lit-searched)
- Phase2↔Phase3 desync (doc cites a value not matching the recommended DB value)
- uncertainty drift / value drift from the cited paper

Batches (small, one at a time): TRAPPIST-1 · α Cen A/B · Proxima · inversion-host
planet docs (au-mic / 61-vir / hd-69830 / tau-cet / eps-eri planets).

---

## Batch 1 — TRAPPIST-1  (DONE 2026-05-30)

Planet masses/radii (Agol 2021 recommended + Grimm 2018 alts) + eccentricities:
all verified OK against cache (Grimm [1802.01377](https://arxiv.org/abs/1802.01377) Tables 2/3 direct; Agol 2021 via
secondary caches [2504.16201](https://arxiv.org/abs/2504.16201), [2101.08172](https://arxiv.org/abs/2101.08172)). Stellar L (Van Grootel 2018 [1712.01911](https://arxiv.org/abs/1712.01911))
OK. ~49 rows confirmed.

**Real issues to fix (fixes deferred to a later pass):**
- HIGH — `docs/phase3/trappist-1-d.md` density_g_cc = 5.43 is planet b's density
  copied; Agol 2021 M/R → ~4.37.
- HIGH — `docs/phase3/trappist-1-c.md` density_g_cc = 6.36 wrong (doc self-flags
  "~5.7"); Agol 2021 → ~5.46 ([2204.04243](https://arxiv.org/abs/2204.04243):235 = 5.4±0.1).
- HIGH — `db/planets_curated.json` TRAPPIST-1 b `environment.equilibrium_temperature_k`
  = 391; Agol 2021 → 398±4 ([2509.02128](https://arxiv.org/abs/2509.02128):101). Phase 3-b says 397 (≈correct) → DB↔doc desync.
- MED — Phase 3 T_eq f/g/h = 215/194/169 vs secondary-confirmed 218/197/172 (3 K low).
- MED — Phase 3-f density 4.92 vs computed 5.02.
- MED — stellar metallicity 0.04±0.08 attributed to Gillon 2017; [1712.01911](https://arxiv.org/abs/1712.01911) credits
  Gillon **2016** → possible misattribution.

**UNCACHED (need fetch to finish): Agol 2021 full text ([2010.01074](https://arxiv.org/abs/2010.01074), abstract-only),
Gillon 2017 ([1703.01424](https://arxiv.org/abs/1703.01424), stub), Burgasser & Mamajek 2017 (age+activity), Vida 2017
(rotation). Stellar radius/age/rotation/activity unverified until fetched.**

---

## Batch 2 — Alpha Centauri A/B  (DONE)
- **MISATTRIBUTION**: M_A 1.1055±0.0039 / M_B 0.9373±0.0033 cited Pourbaix 2016 but are
  actually Kervella 2016 (2016A&A...594A.107K, UNCACHED). Pourbaix gives 1.105±0.007 /
  0.934±0.006. (DB + both Phase 3 docs.)
- **FABRICATED attribution**: α Cen B Phase 3 teff_k = 5236±51 "Porto de Mello 2008" — actual
  PdM value 5316±28; 5236 is Kervella's interferometric Teff. Wrong value+unc+method.
- **DRIFT (DB age)**: A & B age DB 4.81±0.5 vs Joyce&Chaboyer 2018 headline 5.3±0.3 (Phase 3
  already uses 5.3 → DB↔doc desync, DB wrong).
- **DESYNC**: B Teff (doc 5236/DB 5316), B logR'HK (doc -5.0/DB -4.85), B rotation (doc 38±2/
  DB 41±3), A lum (DB unc 0.013 vs paper 0.015), A X-ray range 27.0-27.6 unsupported, parallax
  747.17 attributed Pourbaix but is Kervella 2016.
- UNCACHED: Kervella 2016, DeWarf 2010, Henry 1996, Porto de Mello 2008.

## Batch 3 — Proxima Cen (star + b + d)  (DONE)
- **BIBCODE ERROR**: SM25 ...11M → ...11S (6 DB entries; doc Open-items already flags).
- **DESYNC (stellar)**: radius doc 0.1542 / DB 0.141; Teff doc 2980 / DB 2904 (Passegger);
  rotation doc SM2020 82.6 / DB SM2016 83.0; [Fe/H] doc +0.21 / DB +0.05.
- **HUGE DRIFT**: activity logR'HK doc **-4.0** / DB **-5.55** (1.55 dex — doc likely confused).
- mass attribution doc "Mann 2015" but DB = Mann 2019 + SM25 recommended.
- planet b/d SM25+Faria values CACHE-CONFIRMED OK; Proxima c correctly absent. SMA d precision
  loss (doc 0.029 / DB 0.02881).
- UNCACHED: Anglada 2016, Passegger 2019, Kervella 2017, SM2016, Klein 2021, Mann 2019.

## Batch 4 — AU Mic planets b/c/d/e  (DONE)
- **WRONG arXiv**: Plavchan 2020 cited 2006.13428 (correct [2006.13248](https://arxiv.org/abs/2006.13248)) in all 4 docs.
- **SYSTEMATIC stellar desync** (all 4 planet docs use non-recommended/superseded host values):
  L=0.092 (rec 0.102), Teff=3518 (rec 3665, host doc explicitly supersedes), R=0.82 (rec 0.862)
  → insolation/color-temp/angular-diameter all off.
- **arithmetic**: scale heights b 290(→560)/c 60(→82)/d 13(→8.7); planet d SMA 0.105 "Kepler-
  derived" but Kepler gives 0.085.
- ghost: Cohen 2024 cited, absent from bib; Donati 2025 title = copy of Mallorquin 2024 title.
- Phase2↔3 orbital sync OK for b/c/d. UNCACHED: Mallorquin 2024, Donati 2025, Wittrock 2023,
  Allart 2023, Cale 2021, Tristan 2023.

## Batch 5 — 61 Vir planets b/c/d  (DONE) — Phase 2 CLEAN
- Phase 2 (Vogt 2010) all match; Phase2↔3 sync clean.
- **FABRICATED arXiv pairings**: Bolmont 2020 arXiv [2002.02015](https://arxiv.org/abs/2002.02015) = wrong paper (TTV, not the cited
  obliquity-evolution title); Howe 2014 given Lopez&Fortney's arXiv [1311.0329](https://arxiv.org/abs/1311.0329) (duplicate).
- **MISATTRIBUTION**: Vinson&Hansen 2017 (M-dwarf resonance) cited for G-dwarf tidal locking.
- ghost: Makarov 2012 inline, no bib entry. 17 theory papers uncached.

## Batch 6 — HD 69830 planets b/c/d  (DONE)
- **FABRICATED co-author**: "Atri & Mogan 2019" — Atri 2019 ([1910.09871](https://arxiv.org/abs/1910.09871)) is single-author. All 3.
- **MISATTRIBUTION**: Atri 2019 (SPE terrestrial dose) used for "G8V quiet wind" Neptune dose; all 3.
- **YEAR+SCOPE error**: "Madhusudhan 2016" = 2012 paper on 55 Cnc e rocky interior (planet c).
- **CALC error**: Hut 1981 pseudo-sync 0.84 should be 0.908 (planet c).
- **UNCACHED source driving desync**: "Tanner 2019" (1812.08964) not in bib; c mass 11.8→12.1,
  d 18.1→18.4. phantom "DB-stored 3.17 R⊕" (b — no radius in DB). L=0.60 vs 0.622 (4%). Lamy
  2017/2018 inconsistency. Lovis 2006 permanently UNCACHED (2006 Nature, no ar5iv).

## Batch 7 — tau Cet planets f/g/h + eps Eri b  (DONE)
tau Cet (DB has f/g/h only; e correctly absent as FP — clean):
- **DESYNC (stale stellar)**: planet docs L=0.457 / DB 0.488 (Teixeira); Teff 5344 / DB 5370
  (Korolik). Same not-updated-after-re-synth pattern.
- **MISATTRIBUTION**: disk incl 35° → MacGregor 2016, actually Lawler 2014 (MacGregor assumed it).
- **FABRICATED**: Tomasko 2008 "Venus albedo" = actually Titan/Huygens paper; "Güdel 2014 A&A 571
  A85" HZ = A&A 571 is the Planck issue (no such paper); "Wordsworth&Pierrehumbert 2015" title
  mismatch.
- **ARITHMETIC**: scale heights e/f/h; spin-orbit KSP rotation g & h used (3/2)·P instead of
  (2/3)·P; tidal-timescale ratio (49.41/20)^(13/3)≈250 should be 50.
- SUSPICIOUS: g arg_periapsis 395.341° (>360°, likely +360 artifact). UNCACHED: Feng 2017
  (PRIMARY, [1708.02051](https://arxiv.org/abs/1708.02051)), Feng 2018, Cretignier 2021, Figueira 2025.

eps Eri b (worst — ALL 10 cornerstone papers UNCACHED):
- **mass label error + 18% desync**: DB true_mass_mearth 209.77 (=0.66 MJup) labeled "true mass"
  but is M sin i; doc says 0.78 MJup (248 M⊕).
- **deprojection arithmetic**: doc "0.66/sin34°=0.78" — actually 1.18 MJup.
- **surface gravity unit error**: doc 22 g_earth; actual 1.79 g_earth (factor ~12).
- **STALE host values**: L 0.34/0.32, R 0.759/0.74, Teff 5180/5039 (Baines 2012 recommended).
- Hill sphere 0.36/0.237 AU; magnetic dipole 17000 vs 15600; ghost cites (Metcalfe 2013,
  Canup 2002, Coffaro 2020); false "papers in host bib" claim. Fetch priority: Llop-Sayson 2021
  (2108.05552).

---

# SYSTEMATIC PATTERNS (fix strategy)

1. **Stale stellar values in inversion-host PLANET docs** — au-mic / tau-cet / eps-eri planet
   docs use pre-re-synthesis L/Teff/R (the session updated host stellar docs + DB but NOT the
   planet sub-docs). Mechanical, widespread, low-risk to fix (recompute insolation/Teq/angular
   diameter/color-temp from the recommended host values). 61-vir/hd-69830 planets less affected.
2. **Fabricated / misattributed citations** — Bolmont 2020 (61 Vir, wrong arXiv), Howe 2014
   (dup arXiv), Atri+Mogan co-author (HD 69830 ×3), Tomasko 2008 / Güdel 2014 / W&P 2015 (tau
   Cet), Madhusudhan year (HD 69830 c), Vinson 2017 scope (61 Vir), MacGregor→Lawler (tau Cet),
   α Cen masses→Kervella2016-not-Pourbaix, Plavchan wrong arXiv (AU Mic ×4). NEEDS citation fix
   (+ fetch to confirm correct source).
3. **Arithmetic errors in derived cfg fields** — scale heights (AU Mic, tau Cet, eps Eri b),
   surface gravity (eps Eri b), Hill sphere (eps Eri b), spin-orbit resonance (tau Cet g/h),
   tidal timescales, mass deprojection (eps Eri b). Deterministic recompute fixes.
4. **Phase2↔3 desync** — HD 69830 c/d mass (Tanner2019 uncached), eps Eri b mass label,
   Proxima (Teff/radius/rotation/activity), α Cen B Teff.
5. **Bibcode errors** — Proxima SM25 ...11M → ...11S (6 entries).
6. **UNCACHED primaries needing fetch before commit** — Feng 2017 (tau Cet), Llop-Sayson 2021 +
   9 others (eps Eri b), Lovis 2006 (HD 69830, no ar5iv — permanent), Kervella 2016 (α Cen),
   Anglada 2016 / Passegger 2019 / SM2016 (Proxima), Mallorquin 2024 / Wittrock 2023 (AU Mic).

**HIGH-severity / cfg-visible to fix first:** eps Eri b mass+gravity+stale-stellar; α Cen B
fabricated Teff + DB age; Proxima activity logR'HK -4.0 (1.55 dex); TRAPPIST-1 d/c densities;
the fabricated citations (no fetch needed to DELETE/correct obvious ones like Atri+Mogan,
Tomasko, Güdel).

---

# FIXES APPLIED (2026-05-30)

**Batch 1 (7a8c38c)** — Proxima SM25 bibcode ...11M→...11S (6 entries); stale-stellar recompute
in au-mic/tau-cet/eps-eri planet docs (insolation/Teq/color-temp/angular-diameter onto
recommended host L/Teff/R); arithmetic (scale heights, tau Cet g/h spin-orbit (2/3)·P + tidal
50×, eps Eri b gravity 1.8 g_E / Hill 0.237 AU / dipole 15600); AU Mic Plavchan arXiv
2006.13428→[2006.13248](https://arxiv.org/abs/2006.13248); AU Mic d Kepler-claim→Wittrock.

**Batch 2 (e91a791)** — citation fixes: HD 69830 drop "& Mogan" (single-author) + Atri dose
demoted + Madhusudhan 2016→drop + phantom radius; tau Cet MacGregor→Lawler 2014, drop
Tomasko/Güdel/W&P fabrications, solar-day prose (g 40 d, h 98.8 d); 61 Vir drop wrong/dup
arXiv (Bolmont [2002.02015](https://arxiv.org/abs/2002.02015), Howe [1311.0329](https://arxiv.org/abs/1311.0329)) + Vinson→Hut 1981 + Makarov ghost; eps Eri b
ghost-cite bib entries + false "papers in host bib" claim; α Cen A/B DB age 4.81→5.3±0.3
(Joyce & Chaboyer 2018 1σ, cache [1806.07567](https://arxiv.org/abs/1806.07567):300).

**Batch 3 (this commit)** — fetch-verified: tau Cet g ω 395.341→35.341 (Feng 2017 reported
6.90 rad raw, normalized; DB+doc); HD 69830 c/d revert to Lovis 2006 (11.8/18.1) — "Tanner
2019 (1812.08964)" was an arXiv COLLISION (resolves to a controls paper), source removed;
eps Eri b wrong Llop-Sayson arXiv 2108.05552 removed (COLLISION → ML paper).

## DEFERRED — needs careful dedicated pass (not rushed)   [ALL RESOLVED 2026-05-30 — see "RESOLVED" below]
1. **eps Eri b mass/inclination** — DB 0.66 MJup "true mass" (likely M sin i mislabeled) vs doc
   0.78 (Mawet 2019 joint-fit at i≈89°) vs 1.19 (coplanar i=34°). cfg uses i=34° but mass 0.78
   (the i≈89° value) → internally inconsistent. Needs the CORRECT Llop-Sayson 2021 arXiv id
   (2108.05552 was a collision) + a synthesis decision on cfg inclination, then recompute
   gravity/density. Mawet 2019 ([1810.03794](https://arxiv.org/abs/1810.03794)) IS correctly cached for cross-check.
2. **α Cen A/B masses** — values 1.1055/0.9373 correct but attributed to Pourbaix 2016; the
   tight uncertainties are from Kervella et al. 2016 (arXiv [1610.06079](https://arxiv.org/abs/1610.06079), not yet fetched).
   Re-attribute after fetch. Also α Cen B Phase 3 Teff 5236±51 "Porto de Mello 2008" is wrong
   (PdM = 5316±28; 5236 is Kervella interferometric) — fix attribution/value after fetch.
3. **Proxima** stellar desyncs (doc radius 0.1542/DB 0.141; Teff 2980/DB 2904; rotation SM2020
   82.6/DB SM2016 83.0; activity doc -4.0/DB -5.55) — legacy DB itself unverified (SM2016 etc.
   uncached); needs fetch round.
4. **TRAPPIST-1** densities (d 5.43→~4.37, c 6.36→~5.46), b T_eq 391→398, metallicity
   Gillon 2016/2017 — needs Agol 2021 full text (cache abstract-only) + Gillon fetch.
5. Systematic: legacy docs have several arXiv-id COLLISIONS (wrong id → unrelated paper) —
   worth a dedicated arXiv-id integrity sweep across all legacy bibs.

## RESOLVED — careful dedicated pass (2026-05-30)
All five deferred items fixed. DB edits via `schema.write_canonical`; Phase 3 docs (en+ko)
+ HTML rebuilt; `check.sh` green except one unrelated parallel-session file (a missing ko
mirror for `plans/universe-sandbox-nbody-comparison.md`, not ours). Every value was
re-verified against the frozen `_papers` cache on the main thread — agent reports were NOT
trusted blind. Research/fetch + doc-edits were delegated to subagents; value-check stayed on main.

1. **α Cen A/B masses — attributions were SWAPPED.** cache `1610.06079.md:86-87` Table 1: the
   P16 column (Pourbaix & Boffin 2016) = 1.133 / 0.972; the K16 column (Kervella et al. 2016) =
   1.1055 ± 0.0039 / 0.9373 ± 0.0033 (the DB-recommended values). Swapped reference/bibcode/doi so
   1.1055/0.9373 → Kervella 2016 and 1.133/0.972 → Pourbaix & Boffin 2016. Docs reattributed
   (intro + Decisions + Bibliography), M_B uncert 0.0028→0.0033, A parallax 747.17 reattributed
   Pourbaix→Kervella, luminosity A 1.519→1.521 / B 0.500→0.503.
   - α Cen B Teff: DB already correct (5316 ± 28, Porto de Mello 2008). The DOC was wrong
     (5236 ± 51, an untraceable digit-swap) → corrected to 5316 ± 28 (value + uncertainty);
     stellar_color_temp_k → 5316; tint hex left unchanged (80 K shift sub-perceptual, noted in
     Open items).
2. **TRAPPIST-1** — the wrong densities lived ONLY in the Phase 3 docs (DB c–h density = null).
   cache `2010.01074.md:25` Agol Table 6: c = 5.447, d = 4.354 (b = 5.425, so DB b 5.43 is correct).
   Doc c 6.36→5.45 (+ the "Agol reports ~5.7" fabrication → 5.447, open item closed), d 5.43→4.35.
   b T_eq DB 391→398 (A=0, derived from Agol insolation S_b = 4.153 S⊕; Agol has NO T_eq column —
   Gillon 2017 gives 400 K). [Fe/H] attribution Gillon 2017 → Gillon 2016 (the originating NIR
   measurement; value +0.04 ± 0.08 unchanged, per the existing-host metallicity policy).
3. **Proxima** — radius: Boyajian 2012 EXCLUDES GJ 551 (cache `1208.2431.md:107,117`, no Proxima
   radius) → removed that mis-cited entry, promoted Demory 2009 (0.141 ± 0.011) to recommended;
   doc 0.1542→0.141. Teff: DB Passegger 2019 (2904 ± 51) kept (correct); doc 2980/Boyajian →
   2904/Passegger. Rotation: SM2016 gives 116.6 d / 82.5 ± 8.25 d, not 83.0 ± 0.8 (cache
   `1506.08039.md:184`) → removed the SM2016 entry, promoted Benedict 1998 (83.5 ± 0.5); doc
   82.6/SM2020 → 83.5/Benedict (SM2020 adopts 83.2, SM2025 GP 83.2 ± 1.6 corroborate). Activity:
   SM2016's real value = −5.65 ± 0.17 (cache `1506.08039.md:184`), not −5.55; doc −4.0 was
   implausible → DB −5.55→−5.65 + uncertainty 0.17; doc −4.0→−5.65 + prose rewrite (old slow
   rotator, low/moderate quiescent activity, still flares). Stale SM25-bibcode open item removed
   (DB already stores 2025A&A...700A..11S).
4. **eps Eri b** — the DB was ALREADY CORRECT (true mass 0.66 M_Jup @ i = 78.81°, Llop-Sayson 2021,
   2021AJ....162..181L; cache `2108.02305.md:170` — astrometry-deprojected, NOT M sin i). The DOC
   was the inconsistent artifact: it used Mawet's 0.78 mislabeled "M sin i" and cited the COLLISION
   arXiv 2108.05552 (an unrelated ML paper) with a wrong title. Fixed doc to 0.66 @ 78.81°,
   corrected the citation to arXiv [2108.02305](https://arxiv.org/abs/2108.02305), documented the Mawet mass history (M sin i 0.72;
   0.78 @ i≈89°; 1.19 @ i=34° coplanar), and softened the coplanar claim (Llop-Sayson: planet ~2σ
   off the 34° ring; Roettenbacher 2022 unverified). Correct pin added to `_bib/eps-eri.yaml`.
   NO DB change.
5. **arXiv-id integrity sweep** — read-only sweep of all audited legacy bibs: 0 NEW collisions; the
   two known historical collisions (2108.05552, 1812.08964) are no longer live anchors; all
   load-bearing curated citations resolve correctly. (Large auto-harvested bib lists have many
   uncached entries, not verifiable in a read-only pass.)

Minor follow-ups left (NOT blocking, flagged by agents): α Cen B `limb_darkening_alpha_h` ±0.0044
vs cache ±0.0055; α Cen Related-line phrasing now imprecise after re-attribution; `binary_orbits.json`
α Cen mass provenance (`pourbaix_correia_2017`, B = 0.9092) differs from the stellar_props layer.
