<!-- HD 69830 Phase 2 + Phase 3 reconciliation checklist -->
# HD 69830 — Phase 2 full curation + Phase 3 reconciliation

Tier-1 disk-host upgrade following the Delta Pavonis template
(commit 4d26495).

## Phase 2 — db/stellar_props_curated.json

Replace the existing 2-category entry (mass + radius only,
both `unverified`) with full 8/8 categories.

- [x] Identify anchor paper.  Tanner et al. 2019 ApJ 873, 91
      (2019ApJ...873...91T) — dedicated HD 69830 study, full
      Teff/logg/[Fe/H]/L + CHARA-allowed-region stellar
      parameters. Use as primary anchor where possible.
- [x] mass_measurements (Tanner 2019 recommended; Brewer 2016,
      Lovis 2006 alternates)
- [x] radius_measurements (Tanner 2019 recommended; Rosenthal
      2021 alternate; Stassun 2018 TIC-8 SED alternate)
- [x] teff_measurements (Tanner 2019 recommended; Brewer 2016,
      Tsantaki 2013, Casagrande 2011 alternates)
- [x] luminosity_measurements (Tanner 2019 bolometric;
      Beichman 2005 alternate from SED)
- [x] age_measurements (Lovis 2006 isochrone recommended;
      Mamajek 2008 gyrochronology, Tanner 2019 isochrone
      alternates — significant literature spread 4-12 Gyr)
- [x] metallicity_measurements (Tanner 2019 recommended;
      Brewer 2016, Tsantaki 2013, Lovis 2006 alternates)
- [x] rotation_measurements (Suarez Mascareño 2015
      photometric P_rot recommended; Mamajek & Hillenbrand
      2008 gyrochronology alternate)
- [x] activity_measurements (Gomes da Silva 2021 HARPS
      weighted log R'HK recommended; Boro Saikia 2018,
      Henry 1996 alternates)
- [x] meta_notes — flag (a) no asteroseismology / interferometry
      for HD 69830, (b) age literature spread, (c) Phase 3
      currently quotes log R'HK = -5.0 from Henry 1996 — should
      track Gomes 2021 value -4.95 ± 0.04 weighted-mean

## Phase 3 — docs/phase3/hd-69830.md + planet pages + ko mirror

- [x] Stellar rows in hd-69830.md Decisions table updated to
      cite Phase 2 picks.
- [x] Identify divergent rows and add reconciliation notes.
  - radius: current Phase 3 quotes Rosenthal 2021 0.887 R☉
    "unverified"; Phase 2 anchor Tanner 2019 gives 0.905 ± 0.019
  - Teff: current 5385 K (Beichman 2005); Phase 2 anchor
    Tanner 2019 gives 5402 ± 11 K
  - [Fe/H]: current -0.05 (Beichman 2005); Phase 2 Tanner
    2019 gives -0.04 ± 0.02, Brewer 2016 -0.03, both within
    errors
  - log R'HK: current -5.0 (Henry 1996); Phase 2 anchor Gomes
    da Silva 2021 weighted mean -4.95 ± 0.04
- [x] Bibliography expanded to add Tanner 2019, Brewer 2016,
      Gomes da Silva 2021, Boro Saikia 2018, Tsantaki 2013,
      Casagrande 2011, Sousa 2008.
- [x] Korean mirror (ko/docs/phase3/hd-69830.md) updated in
      parallel — block parity preserved.
- [x] Planet pages (b/c/d) updated stellar parameter cross-refs
      to match new picks (mass, radius, L, age, Teff).
- [x] Korean mirror for planet pages updated in parallel.

## Build + verify

- [x] python3 scripts/pipeline/build_systems.py
- [x] python3 scripts/pipeline/build_site.py
- [x] python3 scripts/pipeline/build_phase2_html.py
- [x] python3 scripts/pipeline/build_reports_index.py
- [x] python3 scripts/phase3/check_block_parity.py hd-69830
- [x] python3 scripts/phase3/check_block_parity.py hd-69830-b
- [x] python3 scripts/phase3/check_block_parity.py hd-69830-c
- [x] python3 scripts/phase3/check_block_parity.py hd-69830-d
- [x] python3 scripts/phase3/build_html.py hd-69830 (and -b, -c, -d)
- [x] python3 scripts/pipeline/validate.py — FAIL=0
- [x] ./scripts/check.sh — all 6 checks pass
- [x] Commit with subject `feat(hd-69830): Phase 2 full curation
      + Phase 3 reconciliation`
