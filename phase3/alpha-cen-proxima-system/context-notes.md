<!-- Alpha Cen + Proxima Phase 3 — decisions and rationale -->
# Alpha Centauri + Proxima — Phase 3 Context Notes

Append-only log. 2026-05-22.

## Scope difference vs TRAPPIST-1 d

TRAPPIST-1 d was a single rocky planet with rich atmosphere/surface
data. Alpha Cen A/B/Proxima is a **stars + planets** synthesis:
- 3 stellar disk syntheses (no planet content)
- 2 planet syntheses (Proxima b, d)

Stellar syntheses focus on:
- Color temperature → SED → KSP star tint
- Limb darkening, granulation cell scale (visual disk)
- Activity (spots, plages, flares for Proxima)
- Apparent disk size from companion stars' frames
- For Proxima: flare frequency, X-ray/EUV environment for habitability

## Decision philosophy

Per memory `feedback_phase3_interesting_first`:
- When observation/theory tie, default to visually more interesting
- Conservative interpretation → cfg variant

Per memory `feedback_phase3_documented_divergence`:
- Gameplay can outrank canonical within observation-fit range
- Documented in Canonical alternatives section
- Canonical preserved as cfg variant

## Decision philosophy — stars specifically

For star tint, accuracy matters more than "interesting" because:
- Stars are the primary light source for all planets
- Wrong stellar tint propagates to all planet visuals
- KSP renders stars as a billboard + light source, so the tint
  affects atmospheric scattering, surface illumination, etc.

So for stellar tint, lean canonical (blackbody from Teff) rather
than "interesting". But for proper motion / aurora / flare visuals,
"interesting first" still applies.

## Per-star expected scenarios

### Alpha Cen A (G2V, 5790 K)

Sun-like with slightly higher mass (1.10 M_sun), radius (1.22 R_sun),
luminosity (1.52 L_sun), and metallicity ([Fe/H] = +0.24). Apparent
color is essentially the Sun's:
- Spectral peak ~500 nm (B-V ≈ 0.71)
- Visual tint very close to white/cream-white

Visual differences vs Sun:
- Slightly larger angular diameter from same distance
- ~50% brighter integrated flux
- Higher metallicity → slightly cooler-looking limb due to deeper
  convective overshoot (very subtle, hard to render)
- Activity: low (~22 d rotation; log R'HK ≈ -4.95, slightly less
  active than Sun's solar-min)

### Alpha Cen B (K1V, 5260 K)

K1V mid-orange dwarf. Lower mass (0.94 M_sun), smaller radius
(0.86 R_sun), about 1/3 luminosity (0.50 L_sun). Same metallicity
as A.

Visual:
- Spectral peak ~570 nm (B-V ≈ 0.90)
- Visible tint: warm-yellow to pale-orange (RGB ≈ #ffd9b3)
- Larger limb darkening than A
- More active surface (log R'HK ≈ -4.85, ~7 yr cycle)
- Modest spot coverage (~5–10% at cycle max, DeWarf 2010)

### Proxima Cen (M5.5Ve, 2904 K)

M5.5 fully-convective dwarf with strong magnetic activity. Mass
0.12 M_sun, radius 0.14 R_sun, luminosity 0.00155 L_sun (~640× less
than the Sun). Extremely active despite its old age (~5 Gyr):
- Rotation: 83 d (slow for an M dwarf — long Rossby number, so the
  dynamo is in the supersaturated regime where activity decouples
  from rotation rate)
- Frequent superflares (Howard 2018, MacGregor 2018, Vida 2019,
  ASAS-SN long-term photometry)
- X-ray luminosity ~1e27 erg/s, similar to active Sun
- Magnetic field ~600 G (Reiners & Basri 2008)
- Coronal mass ejections: indirect detection (MacGregor 2018) of
  rare superflares affecting Proxima b habitability

Visual:
- Spectral peak ~1.0 μm (deep red), B-V ≈ 1.97
- Visible tint: deep red-orange (RGB ≈ #ff6633 or similar)
- ~1° angular diameter from Proxima b (compared to Sun ≈ 0.5° from
  Earth)
- Massive starspot complexes visible directly (Tregloan-Reed 2024
  spectropolarimetric mapping)
- Flares produce factor 10–100 brightness spikes lasting minutes;
  superflares (factor ~1000) every ~10 yr (Howard 2018)
- Auroral activity on the star itself from M-dwarf chromospheric
  Lyman-α
- TiO band absorption in the spectrum gives a very red appearance
  with strong CO/H2O bands in the near-IR

## Per-planet expected scenarios

### Proxima Cen b (HZ-edge terrestrial, 1.07 M⊕ Msini, ~0.05 AU, 11.2 d)

The classic "nearest potentially habitable planet". Discovered by
Anglada-Escudé et al. 2016 via RV, no transit detected. Receives
~0.65× Earth's flux (well within Sun-equivalent HZ inner edge but
the M-dwarf SED shifts the effective HZ). Likely tidally locked.

Scenarios (mostly modeling-based, no JWST atmospheric data published
in same depth as TRAPPIST-1):

- **A: Habitable** — 1 bar atmosphere, surface ocean possible, 
  Turbet et al. 2016 GCM, Boutle et al. 2017 cloud-resistant ocean.
- **B: Desiccated** — heavy XUV-driven escape over 5 Gyr leaves 
  scorched bare rock (Ribas et al. 2016, Zahnle & Catling 2017).
- **C: Eyeball Earth** — frozen most of the surface but liquid 
  ocean under the substellar point (Pierrehumbert 2011, applied to
  many M-dwarf temperate worlds).
- **D: Mini-Neptune residual** — H/He envelope survives even after
  stripping (less favored given low mass).

For NearStars cfg: **Scenario A (Habitable Eyeball Earth hybrid)** —
1 bar N2+CO2 atmosphere, substellar ocean, frozen poles, scattered
clouds. The "interesting first" tie-break since this is the most
visually distinctive and the iconic Proxima b motif.

Conservative variant (Scenario B desiccated): cfg variant preserved.

### Proxima Cen d (sub-Earth-mass hot rock, 0.26 M⊕ Msini, ~0.029 AU, 5.12 d)

Discovered by Faria et al. 2022, confirmed by Suárez Mascareño 2025.
Very low minimum mass (~Mars × 2.4), receiving ~3× Earth's flux.
Likely tidally locked. No atmospheric data.

Scenarios:
- **A: Bare rock** — Mercury analog, no atmosphere, dayside ~600 K.
- **B: Thin CO2 atmosphere** — outgassed CO2 down to mbar level.
- **C: Volatile-rich residual** — small bodies retain volatiles in
  permanent night-side cold traps.

For NearStars cfg: **Scenario A with C accent** — Mercury-like bare
rock body with thin night-side frost deposit (Iridis-like glacial
hints in polar shadows). Hot dayside, cratered surface, possible
relict magma flows like TRAPPIST-1 d's choice.

## Methodology reuse (system constants)

Triple-system parameters constant across all 5 docs:
- Distance: ~1.35 pc (Alpha AB), ~1.30 pc (Proxima)
- Age: ~5 Gyr (Joyce & Chaboyer 2018)
- Metallicity: super-solar ([Fe/H] ~ +0.24 for AB; +0.05 for Proxima)
- Galactic kinematics: thin disk, low U/V/W
- AB orbit: 79.91 yr P=0.518e, a=23.5 AU
- Proxima orbit around AB: P~547000 yr, a=8700 AU, e=0.5

Geometry from each frame:
- From Alpha A: B subtends 0.5–8" depending on phase; angular size
  variable. At max sep (~36 AU), B subtends ~0.02° (1.2 arcmin); at
  min sep (~11 AU), ~0.06° (3.4 arcmin). Variable apparent magnitude.
- From Alpha B: same orbit (mirrored). A is brighter.
- From Proxima b: Proxima fills ~1.5° of sky; AB pair visible as a
  single bright star (~mV -7) — brighter than Venus from Earth, but
  point-like since separation is < arcsec at 1.5 pc.
- From Proxima d: same as b but closer to Proxima (subtends ~2.4°).

## Heading structure (frozen for ko mirror parity)

Star docs (Alpha A, B, Proxima):
- (intro paragraphs, no H2)
- ## Decisions
- ## Stellar disk synthesis
- ## Activity and variability synthesis
- ## System geometry synthesis
- ## Visual styling
- ## Bibliography
- ### Read (visual-informative, drove decisions above)
- ### Read (context / methodology, not decision-driving)
- ### Read (instrument-only, not visual-informative)
- ### Not read — no arXiv preprint available (N papers)
- ## Open items for follow-up

Planet docs (Proxima b, d):
- (intro paragraphs, no H2)
- ## Decisions
- ## Surface synthesis
- ## Atmosphere synthesis
- ## Rotation & spin synthesis
- ## Visual styling
- ## Bibliography (same 4 sub-sections)
- ## Open items for follow-up

## Triage rules

For each bibliography:
- **Read (visual-informative)**: papers with surface/atmo/disk content
  directly relevant to KSP visual choice
- **Read (context)**: methodology, important for understanding
  but not direct visual driver
- **Read (instrument)**: observatory description, calibration
- **Not read — no arXiv**: defer to manual-followup file

Total per doc: 10–30 papers actually read out of typical 50–150
returned by ADS.
