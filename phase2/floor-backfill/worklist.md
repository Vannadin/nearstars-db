# Phase-2 measurement-floor backfill — worklist

Generated from `check_pipeline_flow.py --floor-detail` (gate 10d) on 2026-07-20.
Scope per owner decision: **all curated hosts within 50 ly**. Floor definition:
`phase2/curation-data-contract/SPEC.md` §A0. [Fe/H] is optional everywhere.

Tiers are by cost/value, not by importance: Tier A/B are hosts that already have
most of their floor and need 1–2 targeted determinations; Tier D are field stars
that were never Phase-2 curated at all and each need a full pass.

Regenerate this list any time with:
```
python3 scripts/check_pipeline_flow.py --floor-detail
```
Progress is also visible without this file — gate 10d's per-class counts fall as
hosts are completed.

### Tier A — roster hosts (implementation set; highest value) — 2 hosts

- [x] `[a]` **Fomalhaut** — DONE 2026-07-20: rotation (Hadjara 2014 VLTI 3-D spin: v sin i 93 + i★ 90° → P 0.98 d; no published period exists, derivation now paper-anchored)
- [x] `[fgkm]` **40 Eridani C** — DONE 2026-07-20: rotation (Shan 2024 8.56 d, grade D — CURATED on Pass 2023 v sin i corroboration, prior exclusion reversed) + activity (Pass 2023 Hα −4.42 Å)

### Tier B — near-complete non-roster (1–2 categories short) — 9 hosts

- [x] `[fgkm]` **55 Cnc** — DONE 2026-07-20: age (von Braun 2011 isochrone 10.2 Gyr + Maxted 2015 gyro)
- [x] `[fgkm]` **Delta Pavonis** — DONE 2026-07-20: rotation (Costa Silva 2020 v sin i → P/sin i 41 d upper limit; no period measurable for this quiet subgiant)
- [x] `[fgkm]` **GJ 9066** — N/A 2026-07-20: age has no published determination (floor_na marker; gate 10d counts it as N/A, not missing)
- [x] `[fgkm]` **HD 219134** — DONE 2026-07-20: age (Li 2025 asteroseismology 10.15 Gyr — first asteroseismic age below 5000 K)
- [x] `[fgkm]` **YZ Cet** — DONE 2026-07-20: age (Engle & Guinan 2017 gyro 4.0 Gyr)
- [x] `[fgkm]` **eps Ind A** — DONE 2026-07-20: age (Chen 2022 activity 3.5 +0.8/-1.0 Gyr)
- [x] `[wd]` **Procyon B** — DONE 2026-07-20: teff (Provencal 2002) + cooling age (Liebert 2013)
- [x] `[wd]` **Sirius B** — DONE 2026-07-20: teff (Barstow 2005) + cooling age (Bond 2017)
- [x] `[wd]` **Van Maanen's Star** — DONE 2026-07-20: teff (Coutu 2019; textbook 7000-7500 K superseded) + cooling age (Sion 2009)

### Tier C — partial (3–4 categories short) — 6 hosts

- [x] `[a]` **Altair** — DONE 2026-07-20: teff 7550 (Erspamer 2003, GD-노트) + L 12.1 + rot 0.324 d (Bouchaud 2020 ESTER) + age ~0.1 Gyr
- [x] `[a]` **Sirius A** — DONE 2026-07-20: teff 9800 (Gebran 2016) + L 25.84 (XHIP) + rot 5.2 d 상한 + age 0.242 Gyr (Bond 2017 자체 트랙, WD 계 나이와 정합)
- [x] `[bd]` **CWISEP J193518.59-154620.3** — DONE 2026-07-20: teff 482 K (Faherty 2024 JWST; Marocco 315 K supersede) + age = De Furio 2025 채택 prior(unverified); L·radius = floor_na
- [x] `[bd]` **eps Ind Ba** — DONE 2026-07-20: teff 1320 + L 2.0e-5 (King 2010) + age 3.5 Gyr (Chen 2022 채택)
- [x] `[bd]` **eps Ind Bb** — DONE 2026-07-20: teff 910 + L 5.86e-6 (King 2010) + age 3.5 Gyr (Chen 2022 채택)
- [x] `[fgkm]` **GJ 896 A** — DONE 2026-07-20: activity Lx/Lbol −3.02 (Morin 2008) + L 0.018 + age ≤0.1 Gyr (Zuckerman 2013 Octans-Near); teff = floor_na (인용가능 측정 부재)

### Tier D — never Phase-2 curated (5–6 short; the long tail) — 112 hosts

- [ ] `[fgkm]` **47 UMa** — teff/L/activity/age DONE 2026-07-20 (Luck 2017 + MH08); rotation 잔여(Suárez Mascareño/Donahue 표 미접근 — 도구 한계, N/A 아님)
- [ ] `[fgkm]` **55 Cnc B** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **61 Cygni A** — teff/L/activity/age DONE 2026-07-20 (Kervella 2008 계 나이 6.0); rotation 잔여(35.4 d 통설이나 초록 미기재 — 미조작 원칙으로 보류)
- [ ] `[fgkm]` **61 Cygni B** — teff/L/activity/age DONE 2026-07-20; rotation 잔여
- [ ] `[fgkm]` **70 Ophiuchi A** — teff/L/activity/age DONE 2026-07-20 (Eggenberger 2008 성진학 6.2 Gyr); rotation 잔여
- [ ] `[fgkm]` **70 Ophiuchi B** — age DONE (계 나이) + teff/L/activity/rotation = floor_na(미분해 동반성) 2026-07-20
- [ ] `[fgkm]` **Arcturus** — teff/age DONE (Ramirez 2011); activity/rotation = floor_na; luminosity 잔여(직접 L 출처 후속)
- [ ] `[fgkm]` **CD Cet** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **COCONUTS-2 A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Capella** — teff/L/age DONE (Torres 2015 Aa 주성); activity/rotation = floor_na(거성 지표 부재) 2026-07-20
- [ ] `[fgkm]` **Eta Cassiopeiae A** — teff/L/activity/age DONE 2026-07-20; rotation 잔여
- [ ] `[fgkm]` **Eta Cassiopeiae B** — 전 카테고리 floor_na(미분해 희미한 동반성) 2026-07-20
- [ ] `[fgkm]` **G 192-15** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **G 261-6** — activity, age, luminosity, radius, rotation, teff
- [x] `[fgkm]` **GJ 1002** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [x] `[fgkm]` **GJ 1061** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **GJ 1132** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 1148** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 1151** — activity, age, luminosity, rotation, teff
- [x] `[fgkm]` **GJ 1214** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **GJ 1265** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 1289** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 15 A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 179** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 180** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 229** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 238** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 251** — activity, age, luminosity, rotation, teff
- [x] `[fgkm]` **GJ 273** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **GJ 317** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 3323** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 338 B** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 341** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 3512** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 357** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 367** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 3779** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 393** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 3988** — activity, age, luminosity, rotation, teff
- [x] `[fgkm]` **GJ 411** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **GJ 414 A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 422** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 4274** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 433** — activity, age, luminosity, rotation, teff
- [x] `[fgkm]` **GJ 436** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **GJ 480** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 486** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 514** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 536** — activity, age, luminosity, rotation, teff
- [x] `[fgkm]` **GJ 581** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **GJ 625** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 649** — activity, age, luminosity, rotation, teff
- [x] `[fgkm]` **GJ 667 C** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **GJ 674** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 680** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 682** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 685** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 687** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 740** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 806** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 832** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 849** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 86** — activity, age, luminosity, rotation, teff
- [x] `[fgkm]` **GJ 876** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [x] `[fgkm]` **GJ 887** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **GJ 96** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **Gl 378** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Gl 410** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Gl 49** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Gl 686** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Gl 725 A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Gliese 12** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 115404 A** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **HD 136352** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 140901** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **HD 141004** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 147379** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 147513** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **HD 180617** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 190007** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 192310** — teff/L/activity/age DONE 2026-07-20; rotation 잔여(~47 d 문헌 언급, bibcode 미확보)
- [ ] `[fgkm]` **HD 20794** — teff/L/activity/age DONE 2026-07-20 (SPOCS+MH08, 매우 늙음 13.5 Gyr 천장값); rotation 잔여
- [ ] `[fgkm]` **HD 211970** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **HD 222237** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 22496** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 238090** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 260655** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 285968** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 3651** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 40307** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 62509** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 86728** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HIP 48714** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **HIP 56998** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HIP 79431** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **HN Lib** — activity, age, luminosity, rotation, teff
- [x] `[fgkm]` **Kapteyn** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **L 363-38** — activity, age, luminosity, rotation, teff
- [x] `[fgkm]` **L 98-59** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [x] `[fgkm]` **LHS 1140** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **LHS 3844** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **LHS 475** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **LTT 1445 A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Procyon A** — teff/L/activity/age DONE (Kervella 2004 성진학 2.3 Gyr); rotation 잔여
- [x] `[fgkm]` **Ross 128** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **Ross 508** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **TOI-540** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Wolf 1061** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Wolf 1069** — activity, age, luminosity, rotation, teff
- [x] `[fgkm]` **Wolf 359** — DONE 2026-07-20 (wave 1, catalog-first; floor_na where no measurement exists)
- [ ] `[fgkm]` **gam Cep** — teff/L/age DONE (Knudstrup 2023 성진학 5.7); activity/rotation = floor_na(아거성) 2026-07-20
- [ ] `[fgkm]` **ups And** — teff/L/activity/age DONE 2026-07-20; rotation 잔여(도구 한계)
