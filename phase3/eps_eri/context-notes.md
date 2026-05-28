<!-- eps Eri Phase 2 + Phase 3 reconciliation context notes -->
# eps Eri — context notes

## Why this curation

Tier 1 disk-host upgrade option-B (Phase 2 + immediate Phase 3 re-audit),
following the delta-pavonis template in commit `4d26495`. eps Eri is the
second-nearest planet host (after Proxima); existing Phase 3 had several
stellar rows cited only against the legacy DB or Gaia DR3 pipeline values
rather than paper-anchored measurements with bibcodes.

## Recommended-pick reasoning by category

Tier hierarchy applied: **most-direct method > smaller fractional
uncertainty > more recent for ties**.

- **mass = 0.82 ± 0.02 Msun (Llop-Sayson 2021, `2021AJ....162..181L`).**
  Joint RV + Hipparcos IAD + Gaia DR2 astrometry + multi-epoch vortex
  coronagraphy fit. Fully constrained, modern, tightest published
  uncertainty. The earlier Valenti & Fischer 2005 SME mass (0.85, no
  formal uncertainty) and Takeda 2007 mass (0.83 ± 0.04 from evol model)
  are kept as cross-checks.
- **radius = 0.735 ± 0.005 Rsun (Baines & Armstrong 2012,
  `2012ApJ...761...57B`, PAVO@CHARA limb-darkened angular diameter
  2.126 ± 0.014 mas + Hipparcos parallax).** This is a **direct
  interferometric** measurement — the most-direct method available for
  any stellar radius. Di Folco 2007 VLTI/VINCI gave θ_LD = 2.148 ± 0.029
  mas → R = 0.74 ± 0.01 Rsun (`2007A&A...475..243D`) — independent
  interferometric cross-check. Rosenthal 2021 CLS table gives R = 0.759
  Rsun from SED fitting (`2021ApJS..255....8R`); slightly higher
  because SED+parallax method has different systematics than direct
  angular-diameter resolution.
- **Teff = 5039 ± 126 K (Baines & Armstrong 2012, interferometric:
  L_bol + θ_LD via Stefan-Boltzmann inversion).** Most-direct method.
  Spectroscopic alternates: Valenti & Fischer 2005 SME 5146 ± 44 K
  (`2005ApJS..159..141V`), Brewer 2016 5076 ± 25 K
  (`2016ApJS..225...32B`), Tsantaki 2013 5077 ± 31 K
  (`2013A&A...555A.150T`) all bracket the interferometric value
  within combined uncertainty.
- **L = 0.32 ± 0.01 Lsun (Baines & Armstrong 2012,
  `2012ApJ...761...57B`, bolometric flux from spectrum +
  interferometric distance).** Most-direct method. Older Eiroa 2013
  DUNES bolometric L = 0.34 Lsun is consistent at ~1σ.
- **age = 0.44 ± 0.10 Gyr (Mamajek & Hillenbrand 2008,
  `2008ApJ...687.1264M`).** Activity + rotation + isochrone joint fit
  for nearby solar-type dwarfs; this is the canonical published
  modern eps Eri age. Barnes 2007 gyrochrone gives ~820 Myr from
  P_rot=11.2 d alone (`2007ApJ...669.1167B`) but is superseded by
  the activity-rotation joint fit in the same age window. Note: the
  full age uncertainty is dominated by gyrochrone systematics for a
  young K dwarf and is in practice ~factor-2 (200–900 Myr).
- **[Fe/H] = −0.13 ± 0.04 (Valenti & Fischer 2005 SPOCS,
  `2005ApJS..159..141V`).** SME spectroscopic; widely cited solar-type
  reference. Brewer 2016 confirms at −0.10 ± 0.03
  (`2016ApJS..225...32B`); both with same SME pipeline so kept as
  separate measurements. eps Eri is slightly sub-solar — a known
  characteristic of the local young K dwarf population.
- **P_rot = 11.20 ± 0.05 d (Donahue 1996 Mt Wilson Ca II HK
  14-year timeseries, `1996ApJ...466..384D`).** Canonical rotation
  measurement, very well-determined. Croll 2006 MOST photometric
  variability period 11.45 ± 0.05 d (`2006ApJ...648..607C`)
  independent confirmation. Roettenbacher 2016 Doppler imaging
  derives ~11.5 d but is a model-dependent indirect measurement
  (`2016Natur.533..217R`).
- **log R'HK = −4.39 ± 0.07 (Zechmeister 2013 HARPS modern epoch,
  `2013A&A...552A..78Z`).** Best modern instrumental snapshot from a
  homogeneous pipeline. Henry 1996 Mt Wilson gives log R'HK = −4.46
  (`1996AJ....111..439H`), older but historically canonical.
  Differences (~0.07 dex) reflect both the activity cycle phase
  (Metcalfe 2013 shows 2.95 + 12.7 yr cycles) and instrumental
  calibration scatter, not real long-term change.

## Phase 3 reconciliation — divergent rows

Existing eps-eri.md / eps-eri-b.md stellar rows mostly used the right
papers already; the substantive changes are:

1. **`radius_rsun` row.** Phase 3 had `0.759 ± 0.012 R☉ (Rosenthal 2021
   CLS table; consistent with Di Folco 2007 VLTI/VINCI interferometry)`.
   The new Phase 2 picks Baines 2012 CHARA `0.735 ± 0.005 R☉` (most-
   direct method, smaller uncertainty). The Phase 3 cited the indirect
   SED-fit value as primary and the direct interferometric value as
   "consistent" cross-check — that ordering is inverted relative to
   tier hierarchy. Phase 3 Decision row updated and basis text rewritten;
   ~3% offset between 0.735 and 0.759 documented as different methods.
2. **`teff_k` row.** Phase 3 had `5180 K (DB; agrees with Valenti &
   Fischer 2005 SME and Brewer 2016)`. The DB value 5180 K comes from
   the Gaia-DR3-derived raw teff_k field, which is a photometric proxy
   rather than a published spectroscopic measurement. The new Phase 2
   picks Baines 2012 interferometric 5039 ± 126 K with VF05 5146 ± 44 K
   as spectroscopic cross-check. Decision row updated. 100 K offset (5180
   vs 5039) documented as photometric vs interferometric method choice.
3. **`luminosity_lsun` row.** Phase 3 had `0.34 (derived from R, Teff via
   Stefan-Boltzmann)`. Replacing with `0.320 ± 0.011 Lsun (Baines 2012
   bolometric flux)` — direct measurement supersedes the derived value.
4. **`stellar_color_temp_k` row.** Updated 5180 → 5039 to track new
   Phase 2 Teff pick.
5. **`metallicity_fe_h_dex` row.** Unchanged value but basis now cites
   the Phase 2 entry directly rather than "DB".

eps-eri-b.md inherits L_star = 0.32 (was 0.34) and M_star = 0.82 (no
change) and R_star = 0.735 (was 0.759). Insolation `S_earth = L/a^2 =
0.32 / 3.53^2 = 0.0257` slightly lower than the previous 0.027 (no
material change to equilibrium-temperature picks in the planet doc).
Angular diameter of star from planet `2*R/a = 2*0.735*Rsun/3.53*AU =
0.108°` (was 0.115°) updated.

## Bibcode + DOI verification

Verified during this session:
- `2021AJ....162..181L` Llop-Sayson 2021 DOI `10.3847/1538-3881/ac134a`
- `2008ApJ...687.1264M` Mamajek & Hillenbrand 2008 (arXiv 0807.1686)
- `2013ApJ...763L..26M` Metcalfe 2013 DOI `10.1088/2041-8205/763/2/L26`
  (note: dual cycles 2.95 yr + 12.7 yr, not single 2.95 yr; corrected
  in narrative if needed)

Bibcodes for remaining papers (Baines 2012, Di Folco 2007, VF05,
Brewer 2016, Tsantaki 2013, Donahue 1996, Croll 2006, Zechmeister 2013,
Henry 1996, Roettenbacher 2016, Backman 2009, MacGregor 2015, Booth 2017,
Mawet 2019, Su 2017) follow ADS canonical encoding and match the
published forms used in the existing Phase 3 doc, which was reviewed
in the prior `feat(stellar): fill TRAPPIST-1 activity + 40 Eri B/C N/A
notes` review window.

## Open items

- Baines 2012 vs Rosenthal 2021 radius offset (~3%) — not surprising given
  different methodologies. Once a JWST/CHARA-update PAVO measurement comes
  out we'd revise.
- Metcalfe 2013 dual-cycle (2.95 yr short + 12.7 yr long) — the existing
  Phase 3 only mentions 2.95 yr. Adding 12.7 yr would be a substantive
  visual-cycle revision and is flagged in Open items for follow-up rather
  than implemented in this curation (scope discipline).
- Stellar mass remains Llop-Sayson 2021 0.82 ± 0.02 — the same value used
  in the existing Phase 3, so the mass row only gets a basis-text refresh.
