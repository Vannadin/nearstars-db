<!-- HD 219134 Phase 3 작업 노트 — 결정 분류 + 유도값 감사 추적 -->
# HD 219134 — Phase 3 context notes

## Scope

Visual synthesis only (no live network). All numbers trace to the frozen
Phase 2 layer in `db/systems/hd_219134.json` or to shown derivations.
No disk fabricated (none reported for HD 219134). Deliverables: stellar
K3V + 6 planets (b, c, d, f, g, h), en + ko mirror each (14 files).

## Phase 2 anchors (from db/systems/hd_219134.json)

### Star (Ligi et al. 2019, VEGA/CHARA interferometry; Johnson 2016 activity/rotation)
- spectral_type = K3 V (Gaia DR3 spectype)
- Teff = 4858 ± 50 K (Ligi 2019, interferometric F_bol + theta_LD; alt Motalebi 4941)
- R = 0.726 ± 0.014 R☉ (Ligi 2019, theta_LD = 1.035 ± 0.021 mas)
- L = 0.264 ± 0.004 L☉ (Ligi 2019, bolometric flux)
- M = 0.696 ± 0.078 M☉ (Ligi 2019, direct from R + transit density; method=unverified; alt Motalebi 0.78)
- rotation: 22.83 ± 0.03 d (Johnson 2016 S_HK; CONTESTED — Motalebi 42.3 d, Vogt ~20 d) — method=unverified
- activity: log R'HK = -4.89 (Johnson 2016); 11.7 yr (4230 d) S-index magnetic cycle (Johnson 2016)
- age omitted (poorly constrained, 0.2–13.8 Gyr); [Fe/H] skipped per policy
- distance: 6.5418 pc = 21.33 ly (Gaia DR3 parallax 152.864 mas); V = 5.53
- Effectively single (V~9.4 M dwarf at ~700 AU projected; meta-note only, not a binary)

### Planets (curated recommended entries)
- b: P=3.0937 d, a=0.0382 AU, e=0.0, true mass 4.74±0.19 M⊕, R=1.602±0.055 R⊕ (Gillon 2017 transit). TEPCat T_eq=1015 K. TRANSITING (i=85.05). Motalebi 2015 orbit.
- c: P=6.765 d, a=0.064 AU, e=0.062, true mass 4.36±0.22 M⊕, R=1.511±0.047 R⊕ (Gillon 2017 transit). TEPCat T_eq=782 K. TRANSITING (i=87.28).
- d: P=46.71 d, a=0.23508 AU, e=0.0 (curated), Msini 21.3±1.27 M⊕ (Vogt 2015). RV-only, no radius. (alt Motalebi 8.67)
- f: P=22.805 d, a=0.14574 AU, e=0.0 (curated), Msini 8.9±0.95 M⊕ (Vogt 2015). controv_flag=1. RV-only.
- g: P=94.2 d, a=0.3753 AU, e=0.0 (curated), Msini 10.8±1.27 M⊕ (Vogt 2015). controv_flag=1. RV-only.
- h: P=2247 d, a=3.11 AU, e=0.06, Msini 108.0±6.36 M⊕ = 0.340 M_Jup (Vogt 2015). RV-only cold giant.

NOTE on d/f mass: DB curated `recommended:true` uses Vogt 2015 values
(d Msini 21.3 M⊕; f Msini 8.9 M⊕). The brief mentioned d "super-Earth /
mini-Nep" and f "~9 M⊕". The frozen DB recommended values are the
canonical source — use d = 21.3 M⊕ (Vogt 2015 recommended), f = 8.9 M⊕.
Brief's "~9 M⊕" for f matches the curated 8.9; brief's d "super-Earth"
description is looser but the curated Msini is 21.3 (mini-Neptune scale).
Synthesize from the DB recommended numbers, flag the Motalebi alt for d.

## Derived values (shown derivations)

T_eq = 278.3 · L^0.25 / √a, with L = 0.264 (L^0.25 = 0.71663):
- b (a=0.0382): A=0 → 1021 K; A=0.3 → 934 K. [TEPCat published 1015 K — cite as primary]
- c (a=0.064):  A=0 → 789 K;  A=0.3 → 721 K. [TEPCat published 782 K — cite as primary]
- d (a=0.23508):A=0 → 411 K;  A=0.3 → 376 K.
- f (a=0.14574):A=0 → 523 K;  A=0.3 → 478 K.
- g (a=0.3753): A=0 → 326 K;  A=0.3 → 298 K.
- h (a=3.11):   A=0 → 113 K;  A=0.3 → 104 K.

Insolation S = L / a²  (L=0.264):
- b 180.9, c 64.5, d 4.78, f 12.4, g 1.87, h 0.027 S⊕

Surface gravity g_earth = M/R² (transiting b,c only):
- b: 4.74 / 1.602² = 1.85 g⊕
- c: 4.36 / 1.511² = 1.91 g⊕

Bulk density ρ = 5.513 · M/R³ g/cc (transiting b,c):
- b: 5.513 · 4.74/1.602³ = 6.36 g/cc
- c: 5.513 · 4.36/1.511³ = 6.97 g/cc
(Both denser than Earth's 5.51 → rocky/iron-rich, consistent with Gillon 2017
"the highest-density known transiting super-Earths.")

Star apparent angular diameter from planet = 2·R★/a (deg), R★=0.726 R☉=0.003376 AU:
- b 10.13°, c 6.05°, d 1.65°, f 2.66°, g 1.03°, h 0.124°

Mass conversions for RV-only (radius is estimate-only, LOW confidence):
- d Msini 21.3 M⊕ → mini-Neptune; Zeng 2016 rocky R would be ~2.5 R⊕ but at
  21 M⊕ a volatile envelope likely → R estimate ~2.5–3.5 R⊕ (low conf).
  DB raw NASA value R=1.61 is auto-fill (not curated); treat as unconstrained.
- f Msini 8.9 M⊕ → super-Earth/mini-Nep boundary; R estimate ~1.8–2.5 R⊕ (low conf).
- g Msini 10.8 M⊕ → mini-Neptune; R estimate ~2.0–3.0 R⊕ (low conf).
- h Msini 108 M⊕ = 0.340 M_Jup → cold Saturn-class gas giant; R ~0.9–1.0 R_Jup (low conf).

## Decisions-row classification (Step 9.0)

All rows are either canonical-aligned (DB/derivation) or tie-break
(interesting-first visual within allowed window). NO documented divergence
on any planet or the star — every value either traces to a Phase 2
recommended measurement, a shown derivation, or is an aesthetic tie-break
flagged in Basis. Therefore NO `## Canonical alternatives` section on any
of the 14 files (omit it entirely, per template — no empty placeholder).

Rotation is genuinely contested (22.83 vs 42.3 d) but the DB already picks
22.83 as recommended; this is a Phase 2 tie already resolved in the DB —
documented in the star's Basis + Open items, not a Phase-3 divergence.

### Star (hd-219134) — ~5 canonical-aligned (R/Teff/L/spectral_type/distance),
rotation+activity canonical-aligned-with-caveat, visual tint tie-break,
spot/corona tie-break, disk_present=false canonical (none reported).

### b — hot rocky super-Earth. transiting (mass+radius measured = high).
T_eq, g, density derived. surface tints + atmosphere airless reading = tie-break.
### c — hot rocky super-Earth, same template, cooler (789 K).
### d — RV-only mini-Neptune (radius low-conf). warm.
### f — RV-only super-Earth, contested (controv_flag=1, kept per gameplay policy). warm.
### g — RV-only mini-Neptune, contested (controv_flag=1, kept). temperate.
### h — RV-only cold Saturn-class gas giant. Ring = ARTISTIC tie-break
(ring_observed=false; cold giant makes icy rings plausible per disk-color policy).

## Tie-break log (interesting-first, all flagged in Basis)
- Star visual tint #f0a868 (warm orange K3V, 4858 K blackbody after TiO onset)
- Star visual_spot_coverage_max ~0.02 (moderately quiet, log R'HK -4.89)
- b surface #2a2422 dark basalt primary + #b84a1e partial-melt/lava accent (1015 K airless)
- c surface #3a3026 dark basalt + #8a3a1a oxidized accent (789 K, below melt but hot)
- d/f/g atmosphere/cloud tints under K3V orange illumination (warm)
- h gas-giant cloud bands warm cream (NH₃/H₂O cloud deck at 113 K),
  Saturn-like ring (artistic) icy ring tint near-neutral grey-white
