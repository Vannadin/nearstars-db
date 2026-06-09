# Luhman 16 AB — Phase 3 context notes (substellar synthesis)

Adapted stellar-synthesis for a brown-dwarf binary (no planets). Papers already
cached + deep-read in Phase 2 (5e147b9); Steps 2-7 (bib/score/triage) skipped.
Cached: Faherty 2014 (1406.1518), Gillon 2013 (1304.0481), Apai 2021 (2101.02253),
Crossfield 2014 (1401.8145), L&S 2018 (1808.07835), Chen 2022 (2205.08077).

## Color computation (scripts/refs/cie_color.py, Planck + CIE 1931 Wyman 2013)
- 1310 K (A) blackbody full-brightness hue: rgb (255, 89, 0) = #FF5900; xy (0.6043, 0.3843)
- 1280 K (B) blackbody full-brightness hue: rgb (255, 86, 0) = #FF5600; xy (0.6079, 0.3818)
- Dim-ember tint (x0.40, reflecting L ~ 2e-5 Lsun): A #662400, B #662200
- Both ~identical (30 K apart); A/B visual difference is CLOUDS, not base color.

## Color synthesis reasoning (color-materials.md veto gate)
- Base = blackbody incandescence ~1300 K → deep red-orange ember (line 364). Physically
  solid (incandescence set by T, not composition).
- Modifier = dusty silicate/iron/corundum cloud decks (1300-2000 K grey mineral dust,
  line 117) + broad Na/K alkali absorption in the optical → mutes/reddens to a dark
  dull red, not a clean bright orange.
- MAGENTA REJECTED for T0.5: magenta is non-spectral, needs a green-notch absorber
  (line 62-66, 178). The "brown dwarfs look magenta" result is a late-T/Y phenomenon
  (deep CH4 + Na/K carving the green-yellow); at T0.5 B is only just past the L/T
  transition and stays red. Noted in Open items, not adopted.
- B's drama is the WEATHER (dynamic patchy/banded clouds, ~11% variability), not a
  fabricated tint. B's thinner/patchier clouds (Faherty 2014: B ~50 K warmer in
  grain-scattering regions) let deeper, hotter layers peek through -> brighter warm
  patches over the dark-red base.

## Decisions-row classification
Both components:
- spectral_type, mass_msun, radius_rsun, teff_k, luminosity_lsun, age_gyr,
  rotation_period_days  -> canonical-aligned (Phase 2 measurements, cache-verified)
- visual_surface_tint_hex_primary  -> tie-break (blackbody-computed hue is canonical;
  the dim-ember rendering value is interesting-first within the physics)
- stellar_color_temp_k  -> canonical-aligned (= teff)
- cloud_morphology / variability_amplitude  -> canonical-aligned
  (A near-featureless: Buenzli 2015 <0.4-4.5%; B banded/patchy weather map:
   Crossfield 2014 Doppler map + Gillon 2013 ~11% + Apai 2021 jets)
No documented divergence -> no `## Canonical alternatives` section.
Counts: ~7 canonical-aligned, 1 tie-break, 0 divergence (per component).

## Rotation
- B: 4.87 hr (Gillon 2013, recommended); multi-peaked 4.9-5.3 hr (Apai TESS 5.28 hr).
- A: 6.94 hr TENTATIVE (Apai 2021, unverified); ~5-8 hr disputed. Confidence=low.
