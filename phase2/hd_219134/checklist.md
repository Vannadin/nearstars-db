# HD 219134 — Phase 2 checklist (DRAFT step)

Host: HD 219134 (HR 8832 = GJ 892 = HIP 114622), K3V, 21.3 ly,
Gaia DR3 2009481748875806976. Effectively single. 6 planets: b, c, d, f, g, h
(no planet e — lettering legitimately skips it).

## Bibliography (pin + fetch)
- [x] Ligi et al. 2019 (1909.10058, 2019A&A...631A..92L) — fetched (full ar5iv)
- [x] Gillon et al. 2017 (1703.01430, 2017NatAs...1E..56G) — fetched (ABSTRACT ONLY;
      ar5iv has no LaTeX render -> arXiv landing page; abstract carries b/c m+R verbatim)
- [x] Motalebi et al. 2015 (1507.08532, 2015A&A...584A..72M) — fetched (full ar5iv)
- [x] Vogt et al. 2015 (1509.07912, 2015ApJ...814...12V) — fetched (full ar5iv)
- [x] Johnson et al. 2016 (1602.05200, 2016ApJ...821...74J) — fetched (full ar5iv)

## Stellar measurements
- [x] radius — Ligi 2019 interferometry 0.726 +/- 0.014 Rsun (recommended; replaces DB 0.778)
- [x] radius alt — Vogt/Takeda 0.77 +/- 0.02 (evolutionary_model)
- [x] mass — Ligi 2019 direct 0.696 +/- 0.078 (recommended, method=unverified)
- [x] mass alt — Motalebi SYCLIST 0.78 +/- 0.02 (evolutionary_model)
- [x] teff — Ligi 2019 interferometric 4858 +/- 50 K (recommended); Motalebi SPC 4941 alt
- [x] luminosity — Ligi 2019 bolometric_flux 0.264 +/- 0.004 Lsun (recommended)
- [x] rotation — Johnson 2016 22.83 +/- 0.03 d (recommended, unverified); Motalebi 42.3 d alt
- [x] activity — Johnson 2016 <log R'HK> = -4.89 (recommended); 11.7 yr cycle in notes
- [x] age — OMITTED (models 0.2-13.8 Gyr; activity 3-9 Gyr; unconstrained)
- [x] metallicity — SKIPPED per policy

## Planets (period is the unambiguous letter key; Vogt uses a different scheme)
- [x] b (3.09d) transit — Gillon 2017 m=4.74+/-0.19, R=1.602+/-0.055 (rec); Ligi R=1.500 alt
- [x] c (6.76d) transit — Gillon 2017 m=4.36+/-0.22, R=1.511+/-0.047 (rec); Ligi R=1.415 alt
- [x] f (22.8d) CONTESTED — Vogt 2015 (=Vogt "d") Msini=8.9 Mearth (rec)
- [x] d (46.7d) — Vogt 2015 (=Vogt "e") Msini=21.3 Mearth (rec); Motalebi 8.67 alt
- [x] g (94.2d) CONTESTED — Vogt 2015 (=Vogt "f") Msini=10.8 Mearth (rec)
- [x] h (2247d) cold Saturn — Vogt 2015 (=Vogt "g") Msini=108 Mearth, 0.34 MJup (rec)

## Deliverables (DRAFT only — MAIN applies/builds)
- [x] docs/phase3/_bib/hd-219134.yaml (5 papers, all fetched)
- [x] phase2/hd_219134/measurements.yaml (validated, apply --check clean)
- [x] checklist.md + context-notes.md
- [ ] apply_phase2.py + build_systems.py + validate.py  <- MAIN/human, NOT this step
