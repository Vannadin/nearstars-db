# 40 Eridani — Phase 3 Context Notes

Append-only decision log. 2026-05-29.

## System overview

- Triple: A (K0.5 V, V=4.43) + B (DA2.9 WD, V=9.53) + C (M4.5 Ve, V=11.17 flare star DY Eri)
- Distance: 5.01 pc (Gaia DR3 + Hipparcos van Leeuwen 2007)
- BC pair: 230.29 yr orbit (Mason, Hartkopf & Miles 2017 `2017AJ....154..200M`, e=0.4294, a=6.93")
- A-BC: ~83" separation, ~8000 yr outer orbit (Tokovinin MSC 2018, unfitted)
- Planet: HD 26965 b ("Vulcan", Ma 2018) refuted (Burrows 2024 `2024AJ....167..243B` — 42 d signal is stellar rotation/activity, multi-instrument 16-yr RV)
- Disk: none known
- System age: ~1.8 Gyr total (Bond 2017 §6.2 IFMR-derived; cooling age 122 Myr for B)

## Per-component handoff to agents

### Agent A — 40 Eri A (K0.5 V) — needs Phase 2 first

Phase 2 missing in DB. Tier 1-style workflow needed before Phase 3.

Known starting paper-actual values from 2026-05-27 prep notes (UNVERIFIED — agent must re-confirm at paper-body level):

| Property | 2026-05-27 candidate | Reference | Verify? |
|---|---|---|---|
| Mass | 0.78 ± 0.08 Msun | Ma 2018 `2018MNRAS.480.2411M` (evolutionary_model) | Re-fetch Ma 2018; this is the refuted planet paper |
| Radius | 0.804 ± 0.006 Rsun | Rains 2020 `2020MNRAS.493.2377R` (interferometry VLTI/PIONIER) | Verify 40 Eri A is in Rains 2020 sample — Rains 2020 is 16 *southern* stars, 40 Eri A dec is -7° |
| Teff | 5126 ± 30 K | Rains 2020 (interferometric θ_LD + F_bol) | Same — verify presence in sample |
| Luminosity | 0.400 ± 0.010 Lsun | Rains 2020 (bolometric_flux) | Same |
| Age | 6.9 ± 4.7 Gyr | Ma 2018 (isochrone Y-Y) | Verify; system-coeval ~1.8 Gyr from B WD conflicts strongly — this is one of the key Phase 3 decisions |
| [Fe/H] | -0.29 ± 0.12 dex | Diaz 2018 `2018AJ....155..126D` (SPECIES high-res) | Verify |
| P_rot | 42.0 ± 2.5 d | Burrows 2024 `2024AJ....167..243B` (photometric + activity, multi-instrument) | Verify in paper Table |
| log R'HK | -4.99 | Jenkins 2011 `2011A&A...531A...8J` (log_rhk) | Verify |

Critical cross-checks:
1. **Rains 2020 sample membership**: paper is "16 southern stars VLTI/PIONIER" — 40 Eri A dec -7°39' is *just barely* southern. Verify by fetching Table 1 of Rains 2020.
2. **Age inconsistency**: Ma 2018 isochrone 6.9 Gyr vs Bond 2017 system-coeval 1.8 Gyr from WD progenitor IFMR. This is a documented divergence — Phase 3 narrative must address.
3. **Burrows 2024 P_rot vs activity**: same paper that refuted the Vulcan planet derives P_rot from the spurious signal — extract carefully.
4. **Other interferometric candidates**: Boyajian et al. 2012 CHARA `2012ApJ...757..112B` — verify if 40 Eri A is in that sample (Northern hemisphere CHARA so likely yes).

After Phase 2 done, agent A continues to Phase 3 synthesis (Decisions table + Surface/Atmosphere/Rotation/Visual sections, stellar template `docs/phase3/alpha-centauri-a.md`).

### Agent B — 40 Eri B (DA2.9 WD)

Phase 2 ✅ already done (Bond 2017 paper-verified, all values + meta_notes recorded).
Agent B drafts `docs/phase3/40-eridani-b.md` directly.

Stellar-Phase 3 specific fields for a WD:
- No surface tint / habitable zone / atmosphere sections (radiative DA atmosphere, no convective envelope, no chromospheric activity)
- Cooling sequence: Bond 2017 `2017ApJ...848...16B` cooling age 122 Myr (thin H layer q_H ≈ 10⁻¹⁰)
- Total age: Bond 2017 IFMR-derived ~1.8 Gyr (progenitor M_initial ~1.8 Msun, pre-WD lifetime 1.7 Gyr)
- Magnetic field: Landstreet & Bagnulo 2015 `2015A&A...580A.120L` upper limit <250 G
- Spectral evolution: Bond 2017 §6 — currently DA, will mix into DC at lower Teff in distant future
- Mass-radius: anchor for white-dwarf MRR (CO core thin H envelope) per Bond 2017 §6.3
- Companion: paired with A at 83" (no binary_orbit cfg entry, A-BC unresolved) + with C at ~33 AU mean orbital separation (BC orbit Mason 2017)

Visual styling: WD in KSP — Sirius B-style very small bright blue-white point. Phase 3 cfg-ready decisions for the Kopernicus-side body include log_g, M-R curve point, IFMR-derived total age, magnetic field upper limit.

### Agent C — 40 Eri C (M4.5 Ve, flare star DY Eri)

Phase 2 ✅ already done (Mason 2017 mass + Mann 2015 R/Teff/[Fe/H] + Cifuentes 2020 L + Bond 2017 system-coeval age + meta_notes including Shan 2024 P_rot 'debated' status).
Agent C drafts `docs/phase3/40-eridani-c.md`.

Specific items to address:
- Active M dwarf (flare star variable DY Eri) — H-alpha emission, X-ray bright
- Rotation: Shan 2024 P_rot 8.56 d (quality D, debated; recorded in meta_notes, not as recommended entry)
- vsini and activity history likely affected by AGB-mass-transfer spin-up from B's progenitor (Fuhrmann 2014 cited in Bond 2017 §6.2)
- AGB accretion: Bond 2017 mentions C "may be due to it having been spun up to a higher rotational velocity by accretion during the AGB phase of B" — Phase 3 narrative point
- Habitable-zone N/A from cfg perspective (no curated planets), but stellar luminosity 6.51e-3 Lsun → HZ ~0.07–0.2 AU (boilerplate)
- Visual styling: Active M4.5 V → red point with strong Hα variability; Firefly cfg downstream for flare aurora colors.

## Pre-existing artifacts to NOT duplicate

- `phase2/40_eridani/checklist.md` + `context-notes.md` — Phase 2 prep workspace (now verification target). Agents should READ these for context but treat any unverified value as candidate, not approved. The Mason 2017 mass / Mann 2015 [Fe/H] / Cifuentes 2020 L / Shan 2024 P_rot findings from today's follow-up commit (8509de9) are the authoritative state.
- `docs/phase2/40-eridani-{a,b,c}.html` — Phase 2 viewer output. Built from current DB. Don't edit.

## Cross-component consistency

After all 3 agents return:
- System age should agree across A/B/C narratives (Bond 2017 ~1.8 Gyr Tot total).
- BC orbit details (P=230.29 yr, e=0.4294) appear consistently in both B and C documents.
- A-BC unresolved status appears in A document.
- Distance 5.01 pc consistent everywhere.
- HD 26965 b refuted status mentioned in A document (with Burrows 2024 cite).

## Verification policy (per 2026-05-28 postmortem)

Each agent must:
- Pre-curation lit search for each measurement category (silence ≠ none)
- Citation value-check at paper Table level (not just abstract)
- DOI + bibcode verification at Crossref or ADS
- Multi-layer commit: DB + meta_notes + Phase 3 narrative + bibliography in same commit
- Launch its own verification subagent at the end of synthesis (Step 7 of postmortem procedure)
- Document in `context-notes.md` (this file) every Decisions-row classification

## Decisions log

- 2026-05-29: System workspace created. Agent A/B/C plan finalized. Working concurrently after this checkpoint.
