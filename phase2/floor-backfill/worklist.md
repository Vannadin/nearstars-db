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

- [ ] `[a]` **Altair** — age, luminosity, rotation, teff
- [ ] `[a]` **Sirius A** — age, luminosity, rotation, teff
- [ ] `[bd]` **CWISEP J193518.59-154620.3** — age, luminosity, radius, teff
- [ ] `[bd]` **eps Ind Ba** — age, luminosity, teff
- [ ] `[bd]` **eps Ind Bb** — age, luminosity, teff
- [ ] `[fgkm]` **GJ 896 A** — activity, age, luminosity, teff

### Tier D — never Phase-2 curated (5–6 short; the long tail) — 112 hosts

- [ ] `[fgkm]` **47 UMa** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **55 Cnc B** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **61 Cygni A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **61 Cygni B** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **70 Ophiuchi A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **70 Ophiuchi B** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Arcturus** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **CD Cet** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **COCONUTS-2 A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Capella** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Eta Cassiopeiae A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Eta Cassiopeiae B** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **G 192-15** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **G 261-6** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 1002** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 1061** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 1132** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 1148** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 1151** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 1214** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 1265** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 1289** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 15 A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 179** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 180** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 229** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 238** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 251** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 273** — activity, age, luminosity, rotation, teff
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
- [ ] `[fgkm]` **GJ 411** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 414 A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 422** — activity, age, luminosity, radius, rotation, teff
- [ ] `[fgkm]` **GJ 4274** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 433** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 436** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 480** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 486** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 514** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 536** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 581** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 625** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 649** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 667 C** — activity, age, luminosity, radius, rotation, teff
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
- [ ] `[fgkm]` **GJ 876** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **GJ 887** — activity, age, luminosity, rotation, teff
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
- [ ] `[fgkm]` **HD 192310** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **HD 20794** — activity, age, luminosity, rotation, teff
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
- [ ] `[fgkm]` **Kapteyn** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **L 363-38** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **L 98-59** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **LHS 1140** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **LHS 3844** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **LHS 475** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **LTT 1445 A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Procyon A** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Ross 128** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Ross 508** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **TOI-540** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Wolf 1061** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Wolf 1069** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **Wolf 359** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **gam Cep** — activity, age, luminosity, rotation, teff
- [ ] `[fgkm]` **ups And** — activity, age, luminosity, rotation, teff
