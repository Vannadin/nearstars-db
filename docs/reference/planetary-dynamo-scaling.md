<!-- 거대행성·아성단 자기장을 에너지플럭스 dynamo 스케일링으로 도출하는 방법(논문 근거) -->
# Planetary / substellar magnetic-field grounding: energy-flux dynamo scaling

Method reference for deriving the dipole magnetic field of **gas-giant and
substellar** bodies, in the same "cite the relation + calibration, not a fake
measurement" spirit as the [J₂ Radau–Darwin worked example](principia-geopotential-data.md).
Giant-planet fields are never measured directly (no in-situ magnetometer, no
resolved Zeeman signal), so the curated value must come from a grounded scaling
law, not from "scale Jupiter by mass", which is physically wrong (see below).

This is the canonical home for the giant/substellar dynamo method; the rocky-planet
field method (RM22 = Rodríguez-Mozos & Moya 2022, `2203.01065`) lives in the
TRAPPIST-1 family decisions and the Phase 3 skill's `mod-grounded-fields.md`.

## The law

Christensen, Holzwarth & Reiners 2009 (Nature 457, 167, `2009Natur.457..167C`)
showed that the dynamo field strength of a rapidly-rotating body is set by the
**energy flux** (luminosity per unit area) threading its convective interior, not
by its rotation rate and not by its mass directly. The mean field at the dynamo
surface scales as

    B_dyn  ∝  (energy flux)^(1/3)  ·  ρ^(1/6)

with a thermodynamic-efficiency factor ≈ 1 for a wide class of objects. Reiners &
Christensen 2010 (A&A 522, A13, `2010A&A...522A..13R`, arXiv **[1007.1514](https://arxiv.org/abs/1007.1514)**, cached)
write it in terms of mass, luminosity and radius (solar units):

    B_dyn  =  4.8 · (M · L² / R⁷)^(1/6)   [kG]

Crucially the field is **independent of rotation rate** as long as the body
rotates above a critical (saturation) limit, which holds for isolated brown
dwarfs, young exoplanets, and giants not tidally locked very close to their star.
The physical consequence that breaks linear-mass scaling: **L is the body's own
internal (cooling) luminosity, which is large when the body is young and decays as
it cools.** A young giant therefore has a *stronger* field than an old one of the
same mass, and a young sub-Jupiter can outshine old Jupiter. "Scale Jupiter's
430 µT down by mass" gets the direction wrong.

### Dipole field at the planet surface

For giant planets (M < 13 M_J) the dynamo sits below the visible surface (≈ 0.83 R
in Jupiter). Reiners & Christensen relate the equatorial surface dipole to the
dynamo-surface field by

    B_dip^eq  =  B_dyn / (2√2)

(factor 2: dipole is half the rms field at the dynamo surface; factor √2: the
equatorial dipole is 1/√2 of the rms dipole), plus a mass-dependent depth
attenuation. The polar dipole is twice the equatorial: B_dip^pol = 2·B_dip^eq.

## The practical interpolation formula (calibrated to the paper's own values)

Rather than re-derive internal cooling luminosities L(M, age) from scratch (which
would itself need grounding in Burrows/Fortney tracks), we anchor on the
**published, depth-corrected dipole values** that Reiners & Christensen 2010
tabulate, and interpolate in (mass, age):

    B_dip^pol(M, age) = 9 G · (age / 4.5 Gyr)^(−0.33) · (M / M_Jup)^0.93
    B_dip^eq = B_dip^pol / 2          (1 G = 100 µT)

- The **0.93 mass exponent** reproduces the paper's "a 5 M_J planet is 4–5× stronger
  than 1 M_J at all ages" (5^0.93 ≈ 4.5).
- The **−0.33 age exponent** reproduces their 1 M_J cooling track (~100 G polar at
  a few Myr → ~9 G at 4.5 Gyr → <10 G at 10 Gyr).

### Validation: the formula reproduces the paper's published bodies

| Body | M (M_J) | age (Gyr) | formula B_pol | paper B_pol | match |
|---|---|---|---|---|---|
| Jupiter | 1.00 | 4.5 | 9.0 G | 9 G (Connerney polar 8.4 G) | ✓ |
| ε Eri b (paper's M sin i) | 1.55 | 1.7 | 18.7 G | 19 G (their Table 4.3) | ✓ |
| 1 M_J young end | 1.00 | 0.003 | 101 G | ~100 G | ✓ |
| 1 M_J old end | 1.00 | 10 | 6.9 G | <10 G | ✓ |

Equatorial Jupiter from the formula = 4.5 G = 450 µT, matching Jupiter's real
~4.3 G equatorial surface field. The interpolation is used **only within the
calibrated giant regime** (0.3 ≲ M ≲ 10 M_J, age ≳ 0.2 Gyr, fast rotation).

## Domain of validity: three regimes

The law is built for, and validated on, **H/He gas giants and brown dwarfs**. The
body class decides which method applies:

1. **True giants, 0.3 ≲ M ≲ 13 M_J**: apply the interpolation formula above.
   (NearStars: ε Eri b, GJ 896 A b, ε Ind A b.)
2. **Brown dwarfs, 13–70 M_J**: use B_dyn directly (dynamo near the surface);
   massive BDs reach a few kG when young, weakening ~10× by 10 Gyr.
3. **Sub-Saturn / sub-Neptune / Neptune-mass (M ≲ 0.3 M_J)**: **out of the
   validated domain.** Reiners & Christensen explicitly exclude Saturn-and-smaller
   because helium separation stratifies the conducting region (Stevenson 1980) and
   the surface-field reduction is "difficult to quantify." Use a Solar-System
   ice-giant analog (Neptune/Uranus ~0.1–0.5 G, highly non-dipolar; Connerney
   1991/Ness 1986), noting that youth/inflation raises the internal flux, and flag
   the value as an order-of-magnitude analog, not a grounded derivation.
   (NearStars: AU Mic b, c, e.)
4. **Rocky planets**: the giant dynamo law does **not** apply. Use the rocky
   scaling RM22 (Rodríguez-Mozos & Moya 2022, `2203.01065`) + tidal-locking penalty
   + Garraffo 2017. (NearStars: AU Mic d.)

Mis-applying a giant/BD paper to a rocky planet, e.g. citing Reiners & Christensen
2010 for an Earth-mass body, is a citation error even when the paper is real.

## Worked examples (NearStars giants)

Inputs are the curated mass/radius/age (Phase 2 anchors). B_eq = B_pol/2;
dipole moment vs Earth = (B_eq / 4.5 G) · (R/R_Jup)³ · 20000 (Jupiter's moment ≈
20000 × Earth at B_eq = 4.5 G).

| Body | M (M_J) | R (R_J) | age (Gyr) | B_eq | dipole (×Earth) | conf |
|---|---|---|---|---|---|---|
| ε Eri b | 0.66 | 1.05 | 0.44 | **660 µT** (540–810) | ~34 000 | low–med |
| GJ 896 A b | 2.26 | 1.10 | 0.1–0.95 | **2000 µT** (1600–3400) | ~120 000 | low |
| ε Ind A b | 7.6 | 1.12 | 3.5 | **3200 µT** (2600–3700) | ~3700 / 2600 → med | low–med |

Notes:
- **ε Eri b**: young (0.44 Gyr gyrochronology, high conf) so despite 0.66 M_J its
  field *exceeds* Jupiter's. The old "scaled jovian, ~7 % below Jupiter" (400 µT)
  had the sign of the youth effect backwards.
- **GJ 896 A b**: host age is genuinely uncertain (≲100 Myr PMS vs ~950 Myr); the
  field spans a factor ~2 across that range. Central 2000 µT, young-end up to 3400.
- **ε Ind A b**: 7.6 M_J is near the brown-dwarf boundary; the 0.93 mass exponent
  is extrapolated above its 1–5 M_J calibration, so the central value carries an
  extra ~25 % systematic. Still firmly in the "much stronger than Jupiter" regime.

Confidence stays **low–medium**: the *method* is grounded and validated, but the
inputs (internal luminosity via age, mass for M sin i cases, radius for non-transit
giants) each carry real uncertainty, and the dipole moment scales as R³.

## Citations

- **Christensen, Holzwarth & Reiners 2009**, Nature 457, 167 (`2009Natur.457..167C`).
  Origin of the energy-flux scaling law. *Nature letter, no arXiv preprint*: cited
  by bibcode (verifiable via ADS/Nature/PubMed; not in the ar5iv `_papers/` cache).
- **Reiners & Christensen 2010**, A&A 522, A13 (`2010A&A...522A..13R`, arXiv
  **[1007.1514](https://arxiv.org/abs/1007.1514)**). Application to giant planets + brown dwarfs; the evolution tracks
  and tabulated dipole values this method is calibrated against. **Cached** in
  `docs/phase3/_papers/1007.1514.md` (pinned in the au-mic / eps-eri / gj-896-a /
  eps-ind-a bibliographies).
- **Yadav & Thorngren 2017**, ApJL 849, L12 (`2017ApJ...849L..12Y`, arXiv
  **[1709.05676](https://arxiv.org/abs/1709.05676)**, cached): applies the Christensen 2009 energy-flux scaling to
  inflated **hot Jupiters** (using Thorngren & Fortney radius-inflation luminosities).
  The most direct exoplanet application of the method; used for the AU Mic planets as
  a downward extrapolation below its hot-Jupiter regime (with the sub-Saturn
  He-separation caveat).
- **Rodríguez-Mozos & Moya 2022** (RM22), `2203.01065`: rocky-planet field scaling
  (cached). Used for AU Mic d, not the giants.
