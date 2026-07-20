# 40 Eridani — Phase 2 Context Notes

## System identity

- **Distance**: 5.01 pc (Gaia DR3) — well within Kopernicus 50 ly range
- **HD 26965 / HR 1325 / GJ 166 A** (K0.5V primary)
- **HD 26976 / GJ 166 B** (DA4 white dwarf)
- **GJ 166 C / DY Eri** (M4.5Ve flare star)
- Gaia DR3 IDs already in target_list — verified during earlier Phase 1 add.
- WDS 04153-0739; BC pair binds tightly (~200 AU), A is ~400 AU away (sep ~83").

## Planet status (HD 26965 b — "Vulcan")

- Discovery: Ma et al. 2018 (Dharma Planet Survey, AJ 156:90). RV ~10.6 d signal,
  m sin i ≈ 8.5 M⊕, claimed terrestrial habitable-zone planet.
- Refutation: **Lubin et al. 2024 AJ 167:114** — combined NEID/HARPS/HIRES RV
  + stellar activity indicators (Halpha, Ca II) show the ~42-day signal
  (later analysis re-derived) is rotational, not Keplerian. Activity-induced.
- NASA Archive: empty (table `ps` returns 0 rows for HD 26965). Already removed.
- **Decision**: do NOT add to `planets_curated.json`. Document as refuted in
  a Phase 3-style markdown if user requests, mirroring Tau Cet e precedent.

## Phase 2 method-tier policy

Per memory `[[reference-rex-comparison]]` and skill instructions, set
exactly one `recommended: true` per measurement array using:

- **Mass**: binary_orbit > asteroseismology > evolutionary_model > spectroscopic > spectroscopic_calibration
- **Radius**: interferometry > eclipsing_binary > evolutionary_model
- **Teff**: interferometry (IRFM bolometric) > spectroscopic > photometric
- **Luminosity**: bolometric_flux_integration > evolutionary_model > photometric
- **Age**: asteroseismology > isochrone > gyrochronology > activity (R'HK)
- **Metallicity**: spectroscopic > photometric
- **Rotation**: photometric_period > spectroscopic_vsini (with sin i degenerate)
- **Activity**: log R'HK from Mt. Wilson HK or modern survey

## Component-specific notes

### 40 Eri A (K0.5V)
- Bright enough for interferometric measurements
  (Boyajian et al. 2012, ApJ 757:112 — CHARA θ_LD baseline).
- Rains et al. 2020 (MNRAS 493:2377) gives radius update?
- Tsantaki 2013, Ramirez 2013 high-res spectra for [Fe/H].
- Rotation period from Donahue 1996 Mt Wilson archive or recent TESS?
- Active K-dwarf; activity is exactly what spoiled the planet signal.

### 40 Eri B (DA white dwarf)
- **Bond et al. 2017 ApJ 840:70** is the definitive modern reference:
  HST FGS astrometric mass = 0.573 ± 0.018 M_sun, R = 0.0136 ± 0.0002 R_sun.
- Teff ≈ 16,500 K. Cooling age ~120 Myr (but total age much older).
- Metallicity not applicable (atmosphere stripped); record in notes only.
- No mass_radius_curated entry — schema applies to it but we treat WD
  carefully.

### 40 Eri C (M4.5Ve / DY Eri)
- Flare star, optical variable DY Eri.
- Mann et al. 2015 ApJ 804:64 — M-dwarf calibrations (mass, radius, Teff, [Fe/H])
- Newton et al. 2018, Reiners 2022 for rotation/activity if specific entry.
- v sin i high (rapid rotator), strong Halpha emission, X-ray bright.

## Binary orbit notes

- Inner B-C: Heintz 1974 P=247.9 yr, e=0.41. ORB6 grade 4.
- A-BC outer: ~8000 yr orbit, very poorly determined; legacy entries treated
  as undetermined. **Keep current decision**: A as independent single,
  binary_orbits.json holds only B-C.
- Check Howard et al. 2023, Mason WDS 2024 update for B-C — Gaia DR3 epoch
  data may have tightened parameters.

## Consolidated literature findings

### 40 Eri A (K0.5V) — recommended set

| Property | Value | Method | Reference | Bibcode |
|---|---|---|---|---|
| Mass | 0.78 ± 0.08 M☉ | evolutionary_model (Y-Y isochrone) | Ma et al. 2018 | 2018MNRAS.480.2411M |
| Radius | 0.804 ± 0.006 R☉ | interferometry (VLTI/PIONIER) | Rains et al. 2020 | 2020MNRAS.493.2377R |
| Teff | 5126 ± 30 K | interferometry (θ_LD + Fbol) | Rains et al. 2020 | 2020MNRAS.493.2377R |
| Luminosity | 0.400 ± 0.010 L☉ | bolometric_flux | Rains et al. 2020 | 2020MNRAS.493.2377R |
| Age | 6.9 ± 4.7 Gyr | isochrone (Y-Y) | Ma et al. 2018 | 2018MNRAS.480.2411M |
| [Fe/H] | −0.29 ± 0.12 dex | high_res_spectroscopy (SPECIES) | Diaz et al. 2018 | 2018AJ....155..126D |
| P_rot | 42.0 ± 2.5 d | photometric_variability (NEID+activity) | Burrows et al. 2024 | 2024AJ....167..243B |
| log R'HK | −4.99 | log_rhk | Jenkins et al. 2011 | 2011A&A...531A...8J |

Alternates kept for cross-check:
- Mass: Diaz 2018 0.76 ± 0.03 M☉ (SPECIES isochrone)
- Age: Diaz 2018 9.23 ± 4.84 Gyr (SPECIES isochrone)
- [Fe/H]: Bensby 2014 −0.31 ± 0.10 (high-res spectroscopy thick/thin disk survey)
- log R'HK: Henry et al. 1996 −4.94

### 40 Eri B (DA2.9 white dwarf) — recommended set

| Property | Value | Method | Reference | Bibcode |
|---|---|---|---|---|
| Mass | 0.573 ± 0.018 M☉ | binary_orbit (MHM17 BC orbit + HST FGS) | Bond et al. 2017 | 2017ApJ...848...16B |
| Radius | 0.01308 ± 0.00020 R☉ | sed_fitting (BVRI + ubvy + JHK + π_Hip + Teff_atm) | Bond et al. 2017 | 2017ApJ...848...16B |
| Teff | 17 200 ± 110 K | high_res_spectroscopy (DA Balmer-line atmosphere fit) | Bond et al. 2017 | 2017ApJ...848...16B |
| Luminosity | 0.01349 ± 0.00054 L☉ | bolometric_flux | Bond et al. 2017 | 2017ApJ...848...16B |
| Total age | ~1.8 Gyr (Mfinal→IFMR→Mfinit→tMS) | isochrone (IFMR-derived progenitor lifetime) | Bond et al. 2017 | 2017ApJ...848...16B |
| [Fe/H] | N/A (clean DA, no metal pollution) | — | — | — |

Spectral type updated DA4 → DA2.9 (Gianninas, Bergeron & Ruiz 2011, 2011ApJ...743..138G).
Magnetic: non-magnetic, σ⟨Bz⟩ ≈ 85 G, no detection above ~250 G (Landstreet et al. 2015, 2015A&A...580A.120L).
Cooling age 122 Myr is the model-dependent thin-H envelope value, not a σ-quoted measurement — record in notes only.

### 40 Eri C (M4.5Ve / DY Eri) — recommended set

| Property | Value | Method | Reference | Bibcode |
|---|---|---|---|---|
| Mass | 0.2036 ± 0.0064 M☉ | binary_orbit (BC dynamical) | Mason, Hartkopf & Miles 2017 | 2017AJ....154..200M |
| Radius | 0.274 ± 0.011 R☉ | spectroscopic_calibration (M_K → R, Mann 2015) | Mann et al. 2015 | 2015ApJ...804...64M |
| Teff | 3167 ± 60 K | low_res_spectroscopy (BT-Settl synth-spec fit to optical+NIR) | Mann et al. 2015 | 2015ApJ...804...64M |
| Luminosity | (6.51 ± 0.13) × 10⁻³ L☉ | bolometric_flux (SED integration 0.4–24 μm) | Cifuentes et al. 2020 | 2020A&A...642A.115C |
| Age | ~1.8 Gyr (system-coeval, from WD progenitor) | isochrone | Bond et al. 2017 | 2017ApJ...848...16B |
| [Fe/H] | not directly measured — inherit from A | — | — | — |
| P_rot | (Kemmer 2025 ≈137 d — flagged provisional, not curated) | — | — | — |
| Hα | active (pEW ≈ −2 to −4 Å, ranges across surveys) | h_alpha | (skipped pending single-paper value) | — |

For Phase 2 curation, omit C's P_rot and activity unless a single verified value can be pinned. Conservative: leave empty arrays.

### Binary orbit B-C — Mason et al. 2017 (replaces Heintz 1974)

| Element | Heintz 1974 (current) | Mason 2017 (replace with) |
|---|---|---|
| P (yr) | 247.9 | 230.30 ± 0.68 |
| T (Bessel yr) | 1849.0 | 1847.7 ± 1.1 |
| e | 0.41 ± 0.02 | 0.4294 ± 0.0027 |
| a (arcsec) | 6.93 ± 0.2 | 6.930 ± 0.050 |
| i (°) | 107.6 ± 2.0 | 107.56 ± 0.29 |
| ω (°) | 329 ± 10 | 318.4 ± 1.1 |
| Ω (°) | 151.3 ± 5.0 | 151.44 ± 0.12 |
| equinox | B1950 | J2000 |
| grade | 4 | 1 (definitive) |
| phase_reliable | false | true |

Bibcode: 2017AJ....154..200M, DOI: 10.3847/1538-3881/aa803e, [arXiv:1707.03635](https://arxiv.org/abs/1707.03635)

T_jd_tt conversion: J1847.7 = JD 2395929.775 (Julian year convention; Mason 2017 uses equinox J2000).

The outer A-BC orbit remains undetermined (Tokovinin MSC 2018 lists ~8000 yr, ~83″ separation; no fitted Keplerian solution). Keep current "A as single component" treatment.

### Planet — HD 26965 b / 40 Eri A b ("Vulcan")

- Discovery: Ma et al. 2018 MNRAS 480:2411 (Dharma Planet Survey, RV).
- Refutation: Burrows et al. 2024 AJ 167:243 ("The death of Vulcan") — 42-day signal is stellar rotation/activity, not Keplerian. Multi-instrument (HIRES + PFS + CHIRON + HARPS + NEID, 16 yr).
- NASA Archive `ps` table: empty for HD 26965 → already removed.
- **Decision**: no entry in planets_curated.json. No Phase 3 markdown required (system has no other planet candidates; Tau Cet e style refuted note would be optional, defer until user requests).

## Decisions log

- 2026-05-27: Phase 2 started. Planet HD 26965 b excluded from curated DB (refuted Burrows 2024; absent from NASA Archive).
- 2026-05-27: B-C orbit upgraded Heintz 1974 → Mason 2017 (grade 1, phase_reliable=true). Equinox B1950 → J2000.
- 2026-05-27: Spectral type 40 Eri B updated DA4 → DA2.9 (GBR11). Magnetic null result recorded in meta.notes.
- 2026-05-27: 40 Eri C rotation period (Kemmer 2025 ≈137 d) deferred — paper not independently verified by survey agent.
- 2026-06-03: **OVERRIDE — HD 26965 b (40 Eri A b) RE-INCLUDED in planets_curated per user decision** (gameplay/cultural variety: Star Trek Vulcan + PHM Erid). Uses pre-retraction Ma 2018 RV values (8.47 M⊕ m sin i, P 42.245 d, a 0.224 AU, e 0.04). Refutation (Burrows/Lubin 2024 — signal is stellar rotation) is documented in Phase 3 (docs/phase3/40-eridani-a.md, "Refuted planet" section + documented-divergence framing) and flagged in the curated reference note. The earlier "do NOT add" decision (2026-05-27) is superseded. NOTE: the PHM 2026 film's deep-blue atmosphere + rings are FICTION — not added to the DB (real Ma 2018 mass/orbit only); recorded in cultural-context.md only.

## 2026-05-29 — Tier 2 warm-up restart

Following the 2026-05-28 Tier 1 rollback (`a2ef49c`, 27 commits reverted for
citation integrity), this workspace is **re-opened as a verification target**
rather than an approved plan. Every recommended-set row above was decided
2026-05-27, the day before the fabrication patterns were named. Status of
each by category:

- All bibcodes in this file (Bond 2017 `2017ApJ...848...16B`, Mason 2017
  `2017AJ....154..200M`, Mann 2015 `2015ApJ...804...64M`, Cifuentes 2020
  `2020A&A...642A.115C`, Gianninas 2011 `2011ApJ...743..138G`,
  Landstreet 2015 `2015A&A...580A.120L`) → fetch abstract+Table, value-check.
- "N/A" claims (40 Eri B metallicity, rotation, activity; 40 Eri C
  metallicity-inherit-from-A) → re-run lit search to confirm silence,
  not assume it. Same pattern as HD 69830 false-negative on interferometry.
- 40 Eri C P_rot (Kemmer 2025 ≈137 d, currently deferred) → fetch the paper
  to confirm value + uncertainty; decide curate/skip based on what's in the
  body, not on the 2026-05-27 deferral memo.
- 40 Eri C Hα pEW "−2 to −4 Å" claim → resolve to a single survey paper or
  drop with explicit "multi-survey scatter exceeds tier-3 ambiguity" note.

Scope for this warm-up: **40 Eri B + C only**. 40 Eri A stays Tier 1
(Phase 3 ← Phase 1 reversal) for a later pass once the new procedure is
template-validated.
