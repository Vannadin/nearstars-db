<!-- X-ray/플레어 sweep 작업 체크리스트 — radiation_surface confidence 상향 -->
# X-ray / flare sweep checklist

Goal: measured quiescent X-ray luminosity (+ flare context) for the 7
stellar-wind hosts so Phase 3 `stellar_radiation_surface_relative_sun`
stops being activity-vibes (confidence low) and becomes L_X-anchored.

## ① Schema (xray_measurements category)
- [x] schema.py: `xray_measurements` (value_log_lx_ergs / value_log_rx; methods x_ray_photometry / unverified; extra limit / notes)
- [x] build_systems.py: conditional-emit raw + derived (mass-loss pattern)
- [x] validate.py green on no-data build (0 files churned)
- [x] commit (schema only, b04fc8a pattern) — 32694cb

## ② Per-host curation (cache-verified values only)
- [x] alpha Cen A — Robrade & Schmitt 2016 cache (Ayres 2014 md lost its tables; R&S16 is the L_X anchor)
- [x] alpha Cen B — DeWarf 2010 (rec, ROSAT-96 cycle mean) + R&S16 2012-max alt
- [x] Proxima — Wargelin 2017 R_X (rec) + NEXXUS RASS alt (+ flare context in notes)
- [x] Barnard — France 2020 discovered + pinned + fetched (primary) + NEXXUS / Engle & Guinan alts
- [x] tau Cet — Wood 2021 Table 3 + NEXXUS VizieR row (S&L 2004 rec)
- [x] 40 Eri A — NEXXUS VizieR (rec); Boyajian 2012 ratio DIVERGENT (~5×) → non-rec do-not-use entry
- [x] eps Ind A — Wood 2005 Table 1 (rec) + Chen 2022 R_X alt
- [x] new pins appended to docs/phase3/_bib/stellar-wind.yaml + fetched (France 2020; R&S16 already cached, pinned for traceability)
- [x] curated written via canonical writer; build_systems + validate FAIL 0
- [ ] commit (curation, one axis × all hosts, 8ed58a1 pattern)

## ③ Phase 3 update (7 hosts)
- [ ] radiation_surface rows: value re-checked vs measured L_X ratio, confidence raised, basis cites measurement
- [ ] narrative sentence updated where the picture changes
- [ ] mod-grounded-fields.md derivation row updated (L_X anchor formula)
- [ ] ko mirrors + rebuilt HTML + reports index
- [ ] check.sh all green
- [ ] commit (phase3)

## Gates
- [ ] every committed value greps in docs/phase3/_papers/ cache (no live cite)
- [ ] agent drafts value-checked in main thread before write
