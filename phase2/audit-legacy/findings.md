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
all verified OK against cache (Grimm 1802.01377 Tables 2/3 direct; Agol 2021 via
secondary caches 2504.16201, 2101.08172). Stellar L (Van Grootel 2018 1712.01911)
OK. ~49 rows confirmed.

**Real issues to fix (fixes deferred to a later pass):**
- HIGH — `docs/phase3/trappist-1-d.md` density_g_cc = 5.43 is planet b's density
  copied; Agol 2021 M/R → ~4.37.
- HIGH — `docs/phase3/trappist-1-c.md` density_g_cc = 6.36 wrong (doc self-flags
  "~5.7"); Agol 2021 → ~5.46 (2204.04243:235 = 5.4±0.1).
- HIGH — `db/planets_curated.json` TRAPPIST-1 b `environment.equilibrium_temperature_k`
  = 391; Agol 2021 → 398±4 (2509.02128:101). Phase 3-b says 397 (≈correct) → DB↔doc desync.
- MED — Phase 3 T_eq f/g/h = 215/194/169 vs secondary-confirmed 218/197/172 (3 K low).
- MED — Phase 3-f density 4.92 vs computed 5.02.
- MED — stellar metallicity 0.04±0.08 attributed to Gillon 2017; 1712.01911 credits
  Gillon **2016** → possible misattribution.

**UNCACHED (need fetch to finish): Agol 2021 full text (2010.01074, abstract-only),
Gillon 2017 (1703.01424, stub), Burgasser & Mamajek 2017 (age+activity), Vida 2017
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
- **WRONG arXiv**: Plavchan 2020 cited 2006.13428 (correct 2006.13248) in all 4 docs.
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
- **FABRICATED arXiv pairings**: Bolmont 2020 arXiv 2002.02015 = wrong paper (TTV, not the cited
  obliquity-evolution title); Howe 2014 given Lopez&Fortney's arXiv 1311.0329 (duplicate).
- **MISATTRIBUTION**: Vinson&Hansen 2017 (M-dwarf resonance) cited for G-dwarf tidal locking.
- ghost: Makarov 2012 inline, no bib entry. 17 theory papers uncached.

## Batch 6 — HD 69830 planets b/c/d  (DONE)
- **FABRICATED co-author**: "Atri & Mogan 2019" — Atri 2019 (1910.09871) is single-author. All 3.
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
  (PRIMARY, 1708.02051), Feng 2018, Cretignier 2021, Figueira 2025.

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
