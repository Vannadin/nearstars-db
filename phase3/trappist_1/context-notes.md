# TRAPPIST-1 system Phase 3 — context notes

Append-only log of decisions made while extending Phase 3 synthesis to
the remaining six TRAPPIST-1 planets (b, c, e, f, g, h). d is the
already-completed pilot.

## 2026-05-21 — Scope and depth

User confirmed: full d-level depth for all 6, parallelized fetches.
Each planet gets ~300 lines of synthesis: decisions table (~30 rows),
Surface / Atmosphere / Rotation / Visual sections, full bibliography
with Read / context / instrument / not-read categories.

## 2026-05-21 — Per-planet observational state going in

This drives how heavily synthesis vs. measurement each planet leans:

- **b** — innermost. JWST MIRI 12.8 μm emission (Greene 2023):
  Tday ≈ 503 K, A_B = 0.0 ± 0.1, atmosphere-free or trace. The
  cleanest "definitely bare rock" case. Lava world potential at
  3.4 S⊕ insolation.
- **c** — JWST MIRI 15 μm emission (Zieba 2023): Tday ≈ 380 K
  consistent with bare rock + low albedo OR very thin (≲10 bar) CO₂.
  Also constrained, slightly more atmosphere room than b.
- **d** — DONE. JWST NIRSpec transmission (Piaulet 2025) flat,
  most-atmospheres-excluded. Adopted thin-atmosphere + terminator
  H₂O ice cloud scenario.
- **e** — habitable zone center. No JWST transmission yet published
  in the same depth. Way 2025 ROCKE-3D GCM explores
  Venus/Earth/Dead variants. Best HZ candidate. Will rely heavily on
  Wolf 2017, Turbet 2018, Way 2025, Lustig-Yaeger 2024 (if available)
  GCM predictions.
- **f** — outer HZ edge. Cooler than e, ~Teq 215 K. Turbet 2018 places
  it in the "Snowball Earth or thin CO₂" branch. Lim 2023 JWST/NIRISS
  transmission excludes H₂-rich (per the d paper's reference list).
- **g** — outer HZ. ~Teq 195 K. Even more snowball-prone than f. Less
  observational follow-up; relies on outgassing/escape models.
- **h** — outermost. ~Teq 169 K. Sub-Mars mass (0.33 M⊕). Permanently
  frozen analog; possible subsurface ocean if internally heated.

## 2026-05-21 — Methodology reuse from d

Constants reused for all 7 (host star is the same):

- Host: TRAPPIST-1 M8V, 2566 K, 0.1192 R☉, 0.0898 M☉, 0.000522 L☉
- Age: 7.6 ± 2.2 Gyr (Burgasser 2017)
- Stellar SED color tint: red-orange `~#ff7a1a` for visual sections
- Tidal lock baseline 1:1, obliquity 0
- Eccentricity: from Agol 2021 TTV (per planet)
- Mass / radius / a / P: Agol 2021 TTV
- "Sister planets in sky" geometry: near-coplanar (Agol 2021)
- ~8 Gyr age implies heavy impact accumulation on all surfaces

## 2026-05-21 — Per-planet expected scenario choices

Working hypothesis before reading papers (will revise as needed):

- **b** — bare hot rock (basaltic/melt-resurfaced). No atmosphere.
  Strong substellar magma-ocean residual? Way 2024 calls it "exo-Io"
  candidate from induction heating. Visual: dark basalt + iron oxide
  patches under fierce red glare, possibly fresh lava in patches.
- **c** — bare warm rock. No detectable CO₂ atmosphere down to thin
  limit. Similar palette to b but cooler, less melt.
- **e** — adopt habitable-temperate scenario: 1 bar N₂+CO₂+H₂O
  atmosphere, ocean-bearing, blue-tint with cloud cover. The classic
  "best habitable candidate" cfg variant.
- **f** — outer HZ, snowball/cold thin-CO₂ branch. Mostly icy
  surface, thin atmosphere. Possible subglacial liquid water but
  surface frozen.
- **g** — fully frozen, slightly thicker CO₂ to stave off complete
  collapse (Wordsworth 2017 cold-trap idea). Snowy surface.
- **h** — Mars/Pluto analog. Either fully frozen N₂/CO₂ ice with bare
  surface in places, or volatile-stripped bedrock. Tend toward icy
  given outer location.

## 2026-05-21 — Heading structure (frozen for ko mirror parity)

All six syntheses use the same H2 structure as d:
- (intro paragraphs, no H2)
- ## Decisions
- ## Surface synthesis
- ## Atmosphere synthesis
- ## Rotation & spin synthesis
- ## Visual styling
- ## Bibliography
- ### Read (visual-informative, drove decisions above)
- ### Read (context / methodology, not decision-driving)
- ### Read (instrument-only, not visual-informative)
- ### Not read — no arXiv preprint available (N papers)
- ## Open items for follow-up

If a category is empty for a given planet, the H3 heading is still
kept (with a brief "none for this planet" note) so the ko mirror
parses cleanly.

## Stellar synthesis pass — 2026-05-28

The seven planets are already complete. This pass adds the host star
itself (`docs/phase3/trappist-1.md`) — an M8 V ultra-cool dwarf with
distinctive activity and magnetic-feature properties.

### Extracted numbers from deep-read papers

**Van Grootel 2018 (1712.01911)** — stellar params:
- Parallax 82.4 ± 0.8 mas (d = 12.14 ± 0.12 pc); pre-Gaia value
- L* = (5.22 ± 0.19) × 10⁻⁴ L☉
- M* = 0.089 ± 0.006 M☉ (combined evolutionary + dynamical-binary)
- R* = 0.121 ± 0.003 R☉
- T_eff = 2516 ± 41 K
- [Fe/H] = 0.04 ± 0.08 (Gillon 2016 NIR spec)
- Notes: density anomaly may indicate either supersolar [Fe/H] (+0.40) or magnetic-activity radius inflation; "low-activity M8" per Luger 2017

**Burgasser & Mamajek 2017 (1706.02018)** — age:
- 7.6 ± 2.2 Gyr (concordance of CMD, density, no Li, no low-gravity features, kinematics, P_rot, magnetic activity)
- log(L_Hα/L_bol) = −4.85 to −4.60 dex (moderate activity)
- log(L_X/L_bol) = −3.52 ± 0.17 dex
- v sin i = 6 ± 2 km/s
- UVW = (−43.8, −66.3, +11.0) km/s; S = 80.0 km/s
- Kinematics: transitional thin/thick disk
- Suggests +0.06 [Fe/H] super-solar; R* anomaly 8–14% over solar-metallicity isochrones

**Vida 2017 (1703.10130)** — rotation + flares (K2 short-cadence 80 d):
- P_rot = 3.295 ± 0.003 d (most prominent K2 peak; matches Luger 2017)
- 42 flares analyzed, E = 1.26 × 10³⁰ – 1.24 × 10³³ erg
- 5 (12%) complex multi-peaked events
- ~0.9 flares/day overall (42/45 d effective)
- No correlation between flare timing and rotational phase
- T_eff = 2550 K assumed; R = 0.117 R☉ assumed

**Wheatley 2017 (1605.01564)** — XMM X-ray, 30 ks 17 Dec 2014:
- L_X / L_bol = (2–4) × 10⁻⁴
- L_XUV / L_bol = (6–9) × 10⁻⁴
- L_X (0.1–2.4 keV) = (3.8–7.9) × 10²⁶ erg/s → log L_X = 26.6 – 26.9 (cgs)
- 2-temperature corona: kT = 0.15 ± 0.02, 0.83 +0.16/−0.10 keV
- Variability factor ~few over 7.8 hr (rotational? flare?)
- L_Hα / L_bol = 2.5–4.0 × 10⁻⁵ (chromospheric; modest)
- Quotes Reiners & Basri 2010: B_mag ~ 600 G

**Bourrier 2017 (1702.07004)** — HST/STIS Ly-α:
- F_Lyα (Earth-equivalent) = 0.05 +0.01/−0.02 erg/s/cm²
- Ly-α much weaker than Proxima Cen (0.30) despite similar X-ray flux → chromosphere less active than corona
- log N(H I) (ISM) = 18.3 ± 0.2
- Ly-α flux at planets b–h: 414, 221, 111, 64, 37, 25, 13 erg/s/cm²
- TRAPPIST-1 = coldest exoplanet host with measured Ly-α as of 2017

**Roettenbacher & Kane 2017 (1711.02676)** — activity / spot evolution:
- K2 P_rot = 3.30 ± 0.08 d; Spitzer epoch (76 d earlier) gives 0.819 ± 0.015 d
- Period inferred from photometry is unreliable — surface evolves on weeks-to-months timescales
- Photospheric T = 2500 K, spot T = 2200 K (dark-spot model; ΔT ≈ 300 K)
- Spot-photosphere flux ratio: 0.31 (Kepler), 0.70 (Spitzer)
- Saturated activity regime (Rossby number << 0.1)
- Argues for atmospheric erosion via cosmic-shoreline argument

**Morris 2018a (1803.04543)** — bright-spot alternative:
- Three bright spots, R_spot/R* ≈ 0.004, T_spot ≳ 5300 ± 200 K
- Spots cover ~0.005% of disk → ≪ 1% total
- Reconciles K2 rotational modulation with Spitzer (no significant signal at 4.5 μm where hot bright spots contrast against 2500 K photosphere reduces)
- Flares correlate with brightest-spot longitude → 3.3 d may be active-region lifetime, not literal rotation
- "Zebra effect" caveat: bright vs dark spot interpretation degenerate

**Wilson 2021 Mega-MUSCLES (2102.11415)** — full SED:
- 5 Å – 100 μm SED, COS+STIS+XMM+models
- Provides DEM model for unobserved EUV
- Quiescent XUV ~ 3.75 × 10²⁷ erg/s integrated
- Confirms moderate chromospheric activity vs corona

**Glazier 2020 (2006.14712)** — superflare rate:
- Cumulative superflare rate (≥10³³ erg) = 4.2 +1.9/−0.2 / yr
- Evryscope+K2 combined, 170 nights over 2 yr
- Conclusion: flare rate insufficient to deplete ozone on HZ planets, but also insufficient for prebiotic UV chemistry
- ≥10³⁴ erg events not observed (extrapolated rate < 1/yr)

**Vasilyev 2025 (2508.04793)** — magnetic features from JWST/NIRISS:
- Post-flare flux enhancement → dark magnetic feature disappearance during flare
- Feature cooler than photosphere "by at most a few hundred K" (so T_feature > 2300 K)
- First inferred spectrum of an M8 magnetic feature
- Flare energy-frequency distribution similar to Sun

**Howard 2025 (2512.04265)** — flare→XUV scaling:
- 6 JWST/NIRISS+NIRSpec flares, 2.2–8.7 × 10³⁰ erg
- RADYN beam-heating: F_e = 10¹² erg/s/cm², E_cutoff ≤ 37 keV (moderate beams, weaker than typical M-dwarf flares)
- Cumulative XUV flare contribution = 1.35 +2.0/−0.15 × quiescent (so flares ~double the XUV at planets)
- TRAPPIST-1 saturated-flaring estimated 4.5 × 10³⁵ erg/yr below 4 Gyr spin-down knee; current rate ~2.8× lower
- Saturated → integrated XUV history dominated by pre-main-sequence + young phase (Fleming 2020 calibration)

**Gonzales 2019 (1909.13859)** — fundamental params reanalysis:
- log(L_bol) = −3.216 ± 0.016 → L = 6.09 × 10⁻⁴ L☉ (15% higher than VG18, consistent with Agol 2021 if Teff ~2566 K)
- T_eff = 2628 ± 42 K
- M = 90 ± 8 M_Jup ≈ 0.0859 ± 0.0076 M☉
- R = 1.16 ± 0.03 R_Jup ≈ 0.119 ± 0.003 R☉
- log g = 5.21 ± 0.06
- Spectype M7.5 (vs M8 in Burgasser; vs M8 V in Liebert & Gizis 2006)
- Classified intermediate-gravity (between field and young low-gravity); kinematics still old-disk
- Two possible explanations for inflation: magnetic activity, or planetary tidal heating of star

### Recommended DB values vs paper sources

DB `derived` block uses Agol 2021 recommended values:
- M* = 0.0898 ± 0.0023 M☉
- R* = 0.1192 ± 0.0013 R☉
- T_eff = 2566 ± 26 K
- L = 0.000522 (Van Grootel 2018)
- Age = 7.6 ± 2.2 Gyr (Burgasser 2017)
- [Fe/H] = 0.04 ± 0.08 (Gillon 2017)
- P_rot = 3.295 ± 0.003 d (Vida 2017)

For the synthesis Decisions table the cfg picks Agol 2021 values for
M, R, T (TTV-anchored) but cites Van Grootel for L and Burgasser for age.

### Decisions-row classification (Step 9.0)

Stellar synthesis is mostly canonical-aligned. Two tie-break choices,
no documented divergences:

- `spectral_type` = M8 V → canonical-aligned (Liebert & Gizis 2006; Gillon 2016; Gonzales 2019 says M7.5 — DB uses M7.5e from Gaia tag, synthesis cites both; M8 is the modal classification)
- `mass_msun` = 0.0898 ± 0.0023 → canonical-aligned (Agol 2021 TTV+evol)
- `radius_rsun` = 0.1192 ± 0.0013 → canonical-aligned (Agol 2021)
- `teff_k` = 2566 ± 26 → canonical-aligned (Agol 2021 SED)
- `luminosity_lsun` = 5.22 × 10⁻⁴ → canonical-aligned (Van Grootel 2018)
- `metallicity_fe_h_dex` = +0.04 ± 0.08 → canonical-aligned (Gillon 2017)
- `age_gyr` = 7.6 ± 2.2 → canonical-aligned (Burgasser 2017)
- `log_g` = 5.21 ± 0.06 → canonical-aligned (Gonzales 2019)
- `rotation_period_days` = 3.295 ± 0.003 → canonical-aligned (Vida 2017, Luger 2017)
- `activity_log_lhalpha_lbol` = −4.7 (midpoint) → canonical-aligned (Burgasser 2017 collated)
- `activity_log_lx_lbol` = −3.52 ± 0.17 → canonical-aligned (Burgasser 2017 / Wheatley 2017)
- `x_ray_log_lx_cgs` = 26.6–26.9 → canonical-aligned (Wheatley 2017)
- `xuv_log_lxuv_lbol` = −3.1 (midpoint 6–9 × 10⁻⁴) → canonical-aligned (Wheatley 2017)
- `magnetic_field_gauss_mean` = 600 +200/−400 → canonical-aligned (Reiners & Basri 2010 via Wheatley)
- `flare_rate_per_day_total` = ~0.9 → canonical-aligned (Vida 2017 — 42 events / 45 d)
- `flare_rate_superflare_per_year` = 4.2 +1.9/−0.2 (≥10³³ erg) → canonical-aligned (Glazier 2020)
- `flare_xuv_contribution_relative_quiescent` = 1.35 +2.0/−0.15 → canonical-aligned (Howard 2025)
- `spot_filling_fraction` = unconstrained → tie-break: "intermediate" 1–5% (Roettenbacher / Morris models conflict, both observation-allowed)
- `spot_temperature_contrast_k` = ~300 (dark) OR ~+2800 (bright) → tie-break: cfg picks the bright/hot spot interpretation per Morris 2018a (visually more distinctive on M8 surface, plus solved Spitzer non-detection puzzle)
- `visual_surface_tint_hex_primary` = `#ff5520` (deep red-orange M8 V at 2566 K → CIE) → canonical-aligned (blackbody at Teff)
- `stellar_color_temp_k` = 2566 → canonical-aligned
- `limb_darkening_alpha_h` = ~0.4 → low confidence (interpolated from M-dwarf model grid like Proxima; no direct measurement for ultracool dwarf)
- `rotation_axis_inclination_deg` = 60 (i_planet ≈ 89° + i_rot disagreement allowed) → canonical-aligned to Hirano 2020 / Brady 2022 obliquity constraints
- `activity_cycle_years` = unknown / no clear cycle → canonical-aligned (Roettenbacher & Kane 2017 cycle non-detection; weak periodicity ~7 yr suggested but inconclusive)

Total: 22 canonical-aligned, 2 tie-break (`spot_filling_fraction`,
`spot_temperature_contrast_k`), 0 documented-divergence.

### Bibliography category assignment

- Deep_read (12): Van Grootel 2018, Burgasser 2017, Vida 2017,
  Wheatley 2017, Bourrier 2017, Roettenbacher & Kane 2017, Morris 2018a,
  Wilson 2021, Glazier 2020, Vasilyev 2025, Howard 2025, Gonzales 2019
- Skim / context (~8): Gillon 2016/2017, Luger 2017, Reiners & Basri 2010,
  Filippazzo 2015, Reiners 2018 CARMENES, Garraffo 2017, Ducrot 2020,
  Paudel 2018, Davoudi 2024, Morris 2018b, Seli 2021
- Skip / sister-planet only: everything ≥14 score that is planet-focused
  (Greene 2023, Ducrot 2024/2025, Lim 2023, etc. — covered in per-planet bibs)
- Manual_followup: Howard 2023 (2310.03792 fetch failed — fallback to abstract)

## Related

- [system-trappist-1 entity pages](../../docs/phase3/trappist-1-e.md) — parent topic this workspace contributes to
