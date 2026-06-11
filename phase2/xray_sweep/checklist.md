<!-- X-ray/플레어 sweep 작업 체크리스트 — radiation_surface confidence 상향 -->
# X-ray / flare sweep checklist

Goal: measured quiescent X-ray luminosity (+ flare context) for the 7
stellar-wind hosts so Phase 3 `stellar_radiation_surface_relative_sun`
stops being activity-vibes (confidence low) and becomes L_X-anchored.

## ① Schema (xray_measurements category)
- [ ] schema.py: `xray_measurements` (value_log_lx_ergs / value_log_rx; methods x_ray_photometry / unverified; extra limit / notes)
- [ ] build_systems.py: conditional-emit raw + derived (mass-loss pattern)
- [ ] validate.py green on no-data build (0 files churned)
- [ ] commit (schema only, b04fc8a pattern)

## ② Per-host curation (cache-verified values only)
- [ ] alpha Cen A — Ayres 2014 cache (cycle-resolved L_X)
- [ ] alpha Cen B — Ayres 2014 cache
- [ ] Proxima — Wargelin 2017 cache (+ flare context in notes)
- [ ] Barnard — Wood 2021 cache; else discovery (France 2020?) → pin + fetch
- [ ] tau Cet — cache sweep; else discovery (NEXXUS / pointed obs) → pin + fetch
- [ ] 40 Eri A — Wood 2005 cache; else discovery → pin + fetch
- [ ] eps Ind A — Chen 2022 / Wood 2005 cache (R_X −5.62 trail)
- [ ] new pins appended to docs/phase3/_bib/stellar-wind.yaml + fetched
- [ ] curated written via canonical writer; build_systems + validate FAIL 0
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
