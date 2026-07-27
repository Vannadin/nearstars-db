# 기체 종별 대기 보유 판정: Jeans 파라미터 λ와 탈출 체제 (exoplanet-atmosphere-methodology §5)
"""Species-by-species atmospheric retention from the Jeans parameter.

Method + citations: docs/reference/exoplanet-atmosphere-methodology.md

The cosmic shoreline (Gate 1) answers "any atmosphere at all". It does not say
WHICH gases survive, and that is a different competition: gravity against the
thermal energy of one molecular species at the exobase.

    lambda  =  G M m / (k T_exo r_exo)

Regimes, from Volkov 2011 (arXiv 1009.5110), who mapped the transition with direct
simulation Monte Carlo:

  lambda <~ 2.1        isentropic supersonic outflow limit
  lambda ~ 2-3         hydrodynamic <-> Jeans transition (atomic gas)
  lambda ~ 2.4-3.6     the same transition for a diatomic gas
  lambda > 3           escape proceeds molecule-by-molecule
  lambda >~ 6          the rate matches the classical Jeans rate

For a light gas inside a heavier background the Jeans rate is not the whole story:
Hunten 1973 showed the flux can instead be capped by diffusion of the light species
up through the background, set by its mixing ratio, and that the heavy gases are
not dragged along.

Usage:
  python3 scripts/refs/jeans_escape.py                 # validation + NearStars bodies
  python3 scripts/refs/jeans_escape.py --mass 9.0e23 --radius 3400 --texo 500
"""
from __future__ import annotations

import argparse

G = 6.674e-11
K_B = 1.380649e-23
AMU = 1.66053906660e-27

# molar masses [amu] of the species a rocky secondary atmosphere can plausibly hold
SPECIES = {"H": 1.008, "H2": 2.016, "He": 4.003, "CH4": 16.04, "H2O": 18.02,
           "N2": 28.01, "O2": 32.00, "CO2": 44.01, "H2S": 34.08, "Xe": 131.3}

# Volkov 2011 thresholds
LAMBDA_BLOWOFF = 2.1        # upper limit for isentropic supersonic outflow
LAMBDA_TRANSITION = 3.0     # above this, molecule-by-molecule
LAMBDA_JEANS_CLEAN = 6.0    # above this, the classical Jeans rate applies
# Practical retention marker: well above the clean-Jeans boundary the Jeans flux
# becomes negligible on Gyr timescales. This is a convention of this doc, not a
# published threshold -- see the doc's domain-of-validity note.
LAMBDA_RETAINED = 30.0


def jeans_lambda(mass_kg: float, r_exo_m: float, molar_amu: float, t_exo_k: float) -> float:
    """Jeans parameter: gravitational over thermal energy for one species."""
    return G * mass_kg * molar_amu * AMU / (K_B * t_exo_k * r_exo_m)


def v_escape(mass_kg: float, radius_m: float) -> float:
    return (2.0 * G * mass_kg / radius_m) ** 0.5


def regime(lam: float) -> str:
    if lam <= LAMBDA_BLOWOFF:
        return "hydrodynamic blow-off"
    if lam < LAMBDA_TRANSITION:
        return "blow-off/Jeans transition"
    if lam < LAMBDA_JEANS_CLEAN:
        return "molecule-by-molecule, above Jeans rate"
    if lam < LAMBDA_RETAINED:
        return "classical Jeans escape"
    return "retained"


def table(label: str, mass_kg: float, radius_km: float, t_exo_k: float,
          exobase_alt_km: float = 0.0, species=None) -> None:
    r = (radius_km + exobase_alt_km) * 1e3
    print("%s  M=%.3g kg  R=%.0f km  T_exo=%.0f K  v_esc=%.0f m/s"
          % (label, mass_kg, radius_km, t_exo_k, v_escape(mass_kg, radius_km * 1e3)))
    for name in (species or ("H", "H2", "He", "CH4", "N2", "CO2")):
        lam = jeans_lambda(mass_kg, r, SPECIES[name], t_exo_k)
        print("    %-4s lambda %8.1f   %s" % (name, lam, regime(lam)))


def validation() -> None:
    print("== Validation: three bodies whose retention we know, three different regimes ==")
    print()
    table("Earth   ", 5.972e24, 6371, 1000, exobase_alt_km=500, species=("H", "H2", "N2", "O2"))
    print("    expected: H escapes (Jeans/diffusion-limited), N2 and O2 retained")
    print()
    table("Titan   ", 1.345e23, 2575, 175, exobase_alt_km=1500, species=("H2", "CH4", "N2"))
    print("    expected: N2 retained despite weak gravity because it is cold;")
    print("              H2 sits in the transition regime and is lost")
    print()
    table("Mars    ", 6.417e23, 3390, 250, exobase_alt_km=200, species=("H", "H2", "CO2"))
    print("    expected: H escapes, CO2 bound against thermal escape (its loss is")
    print("              ion/sputtering-driven, not Jeans -- see Ramstad 2021)")
    print()


def nearstars() -> None:
    print("== NearStars: the Polyphemus moons that have an atmosphere ==")
    print()
    # Cassandra: 9.0e23 kg, 3400 km, surface ~250 K. Exobase temperature is the weak
    # input; bracket it rather than pick one.
    for t in (300, 500, 800):
        table("Cassandra", 9.0e23, 3400, t, exobase_alt_km=200,
              species=("H2", "CH4", "N2", "CO2"))
        print()
    table("Pandora  ", 3.85e24, 5724, 800, exobase_alt_km=300,
          species=("H2", "CH4", "H2S", "N2", "O2", "CO2", "Xe"))
    print()
    print("== And the bare-rock check: Gate 1 already excludes these ==")
    for label, m, rad in (("Hades    ", 5.0e21, 750), ("Dante    ", 8.0e21, 900)):
        print("%s v_esc = %.0f m/s (Moon 2380, Titan 2640) -> below the shoreline"
              % (label, v_escape(m, rad * 1e3)))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--mass", type=float, help="body mass [kg]")
    ap.add_argument("--radius", type=float, help="body radius [km]")
    ap.add_argument("--texo", type=float, default=500.0, help="exobase temperature [K]")
    ap.add_argument("--alt", type=float, default=0.0, help="exobase altitude [km]")
    args = ap.parse_args()
    if args.mass and args.radius:
        table("query   ", args.mass, args.radius, args.texo, exobase_alt_km=args.alt,
              species=tuple(SPECIES))
        return
    validation()
    nearstars()


if __name__ == "__main__":
    main()
