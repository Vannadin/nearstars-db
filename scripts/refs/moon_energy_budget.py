# 위성의 4항 에너지 예산(별빛−식+행성열복사+행성반사+조석)으로 T_eq를 구하는 계산기
"""Satellite equilibrium temperature from the four-term energy budget.

Method + citations: docs/reference/moon-energy-budget-methodology.md

A moon is not a planet with a different orbit. Four terms that vanish for a
planet are first-order for a close-in satellite:

  - eclipses by the parent remove stellar flux every orbit
  - the parent's thermal emission heats the moon continuously
  - starlight reflected off the parent adds to the moon's illumination
  - tidal dissipation heats the moon from inside

Grounding: Heller & Barnes 2013 (arXiv 1209.5323) for the illumination +
eclipse + tidal budget and the circumplanetary "habitable edge"; Dobos, Heller
& Turner 2017 (arXiv 1703.02447) for the same four sources as a habitable-zone
calculation; Barnes 2013 (arXiv 1203.5104) for tidal heating driving a runaway
greenhouse ("Tidal Venus"); Peale, Cassen & Reynolds 1979 via
docs/reference/tidal-heating-methodology.md for the tidal term.

Usage:
  python3 scripts/refs/moon_energy_budget.py              # validation + Polyphemus moons
  python3 scripts/refs/moon_energy_budget.py --pandora-27h-vs-32h
"""
from __future__ import annotations

import argparse
import math

SIGMA = 5.670374419e-8
S0 = 1361.0                     # solar constant at 1 AU [W/m2]
AU = 1.495978707e11
R_SUN = 6.957e8
R_JUP = 71492e3
M_EARTH = 5.972e24
G = 6.674e-11
IO_SURFACE_FLUX = 2.4           # W/m2, observed global tidal flux

# Long-wave albedo of a rocky/icy surface is much lower than its optical albedo;
# the parent's thermal emission is absorbed almost completely.
ALBEDO_IR = 0.05


def teq_from_flux(absorbed_flux: float) -> float:
    """Equilibrium temperature [K] from globally averaged absorbed flux."""
    return (absorbed_flux / SIGMA) ** 0.25


def umbra_length(r_parent_m: float, a_star_au: float, r_star_m: float) -> float:
    """Distance behind the parent that the full (umbral) shadow reaches [m]."""
    return r_parent_m * a_star_au * AU / (r_star_m - r_parent_m)


def eclipse_fraction(a_m: float, r_parent_m: float, r_moon_m: float, inc_deg: float,
                     a_star_au: float, r_star_m: float) -> float:
    """Orbit-averaged fraction of stellar flux lost to eclipses by the parent.

    A moon is eclipsed on every orbit when its excursion out of the parent's
    orbital plane, a*sin(i), stays inside the shadow radius; otherwise eclipses
    are seasonal and this returns 0 (a deliberate under-estimate -- see the doc's
    domain-of-validity note).
    """
    if a_m > umbra_length(r_parent_m, a_star_au, r_star_m):
        return 0.0
    r_shadow = r_parent_m - a_m * (r_star_m - r_parent_m) / (a_star_au * AU)
    if r_shadow <= 0:
        return 0.0
    excursion = a_m * math.sin(math.radians(inc_deg))
    if excursion >= r_shadow:
        return 0.0
    chord = 2.0 * math.sqrt(r_shadow ** 2 - excursion ** 2) + 2.0 * r_moon_m
    return min(chord / (2.0 * math.pi * a_m), 1.0)


def tidal_flux(m_parent_kg: float, r_moon_m: float, a_m: float, ecc: float,
               k2_over_q: float) -> float:
    """Solid-body tidal heat flux [W/m2] (Peale/Cassen/Reynolds fixed-Q, synchronous)."""
    n = math.sqrt(G * m_parent_kg / a_m ** 3)
    power = 10.5 * k2_over_q * G * m_parent_kg ** 2 * r_moon_m ** 5 * n * ecc ** 2 / a_m ** 6
    return power / (4.0 * math.pi * r_moon_m ** 2)


def moon_budget(s_star_rel: float, albedo: float, a_rp: float, r_parent_m: float,
                t_parent_k: float, albedo_parent: float, r_moon_m: float,
                inc_deg: float, a_star_au: float, r_star_m: float,
                f_tidal: float = 0.0) -> dict:
    """Globally averaged absorbed flux and T_eq for a satellite."""
    s_inc = s_star_rel * S0
    a_m = a_rp * r_parent_m
    geom = (1.0 / a_rp) ** 2

    stellar_planetlike = s_inc * (1 - albedo) / 4.0
    f_ecl = eclipse_fraction(a_m, r_parent_m, r_moon_m, inc_deg, a_star_au, r_star_m)
    stellar = stellar_planetlike * (1 - f_ecl)

    at_moon_thermal = SIGMA * t_parent_k ** 4 * geom
    at_moon_reflected = albedo_parent * s_inc * geom / 4.0
    thermal = at_moon_thermal * (1 - ALBEDO_IR) / 4.0
    reflected = at_moon_reflected * (1 - albedo) / 4.0

    absorbed = stellar + thermal + reflected + f_tidal
    return {
        "eclipse_fraction": f_ecl,
        "stellar_lost": stellar_planetlike - stellar,
        "at_moon_thermal": at_moon_thermal,
        "at_moon_reflected": at_moon_reflected,
        "absorbed": absorbed,
        "teq_planetlike": teq_from_flux(stellar_planetlike),
        "teq": teq_from_flux(absorbed),
    }


# ── The Polyphemus system (phase4/alpha_centauri.yaml) ────────────────────────
STAR = {"l_sun": 1.521, "teff_k": 5847.0, "r_star_m": 1.2234 * R_SUN}
PARENT = {"r_m": 1.0 * R_JUP, "m_kg": 120 * M_EARTH, "t_k": 225.0, "albedo": 0.30}
A_ORBIT_AU = 1.6
S_REL = STAR["l_sun"] / A_ORBIT_AU ** 2

MOONS = [   # name, a[R_p], R_moon[km], albedo, inclination to the parent's orbital plane
    ("Dante", 1.54, 900, 0.30, 9.0),
    ("Hades", 2.07, 750, 0.30, 11.0),
    ("Pandora", 3.53, 5724, 0.30, 10.0),
    ("Cassandra", 8.40, 3400, 0.35, 4.0),
    ("Chaos", 21.00, 400, 0.70, 1.0),
]


def _budget(a_rp, r_km, albedo, inc, f_tidal=0.0):
    return moon_budget(S_REL, albedo, a_rp, PARENT["r_m"], PARENT["t_k"],
                       PARENT["albedo"], r_km * 1e3, inc, A_ORBIT_AU,
                       STAR["r_star_m"], f_tidal)


def validation():
    print("== Validation ==")
    # Tidal term against Io.
    f_io = tidal_flux(1.898e27, 1.8216e6, 4.217e8, 0.0041, 0.015)
    print("Io tidal flux: formula %.2f W/m2 vs observed ~%.1f  (k2/Q = 0.015)"
          % (f_io, IO_SURFACE_FLUX))
    # Eclipse geometry against Io's familiar ~2.2 h eclipses.
    f_ecl = eclipse_fraction(4.217e8, R_JUP, 1.8216e6, 0.04, 5.2038, R_SUN)
    period_h = 2 * math.pi / math.sqrt(G * 1.898e27 / 4.217e8 ** 3) / 3600.0
    print("Io eclipse: formula %.1f%% of a %.1f h orbit = %.1f h vs the familiar ~2.2 h"
          % (f_ecl * 100, period_h, f_ecl * period_h))
    print()


def polyphemus_table():
    print("== Polyphemus moons: what the four terms do to T_eq ==")
    print("S/S0 = %.4f;  umbra reaches %.2e km, all five moons inside"
          % (S_REL, umbra_length(PARENT["r_m"], A_ORBIT_AU, STAR["r_star_m"]) / 1e3))
    print("%-10s %7s %6s %9s %8s %8s %9s %9s %7s"
          % ("moon", "a[R_p]", "ecl%", "lost", "F_th", "F_refl", "Teq_star", "Teq_4term", "dT"))
    for name, a_rp, r_km, albedo, inc in MOONS:
        b = _budget(a_rp, r_km, albedo, inc)
        print("%-10s %7.2f %6.1f %9.1f %8.2f %8.2f %9.1f %9.1f %+7.2f"
              % (name, a_rp, b["eclipse_fraction"] * 100, -b["stellar_lost"],
                 b["at_moon_thermal"], b["at_moon_reflected"],
                 b["teq_planetlike"], b["teq"], b["teq"] - b["teq_planetlike"]))
    print("lost = stellar flux removed by eclipses; F_th/F_refl = flux AT the moon")
    print("from the parent (thermal / reflected), before the moon's own albedo.")
    print()


def pandora_orbit_choice():
    """The 27 h canon orbit vs the adopted 32 h lock, in tidal-flux terms."""
    print("== Pandora: why the 32 h lock and not the canon 27 h ==")
    name, a_rp, r_km, albedo, inc = MOONS[2]
    r_moon = r_km * 1e3
    b = _budget(a_rp, r_km, albedo, inc)
    print("four-term T_eq (no tidal): %.1f K   absorbed %.1f W/m2"
          % (b["teq"], b["absorbed"]))

    # Kopparapu moist-greenhouse ceiling, converted to an extra-surface-flux budget.
    import sys
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    from greenhouse_dt import kopparapu_seff
    ceiling = (kopparapu_seff(STAR["teff_k"], "moist_greenhouse") * S0
               - S_REL * S0) * (1 - albedo) / 4.0
    print("runaway ceiling (moist greenhouse, first order): %.0f W/m2 = %.0fx Io"
          % (ceiling, ceiling / IO_SURFACE_FLUX))
    print()

    print("%-8s %10s %12s %12s %10s"
          % ("period", "a [km]", "k2/Q 0.0016", "k2/Q 0.003", "ratio"))
    fluxes = {}
    for p_h in (27.0, 32.0):
        n = 2 * math.pi / (p_h * 3600.0)
        a_m = (G * PARENT["m_kg"] / n ** 2) ** (1 / 3)
        f16 = tidal_flux(PARENT["m_kg"], r_moon, a_m, 0.005, 0.0016)
        f30 = tidal_flux(PARENT["m_kg"], r_moon, a_m, 0.005, 0.003)
        fluxes[p_h] = (a_m, f16, f30)
        print("%-8s %10.0f %12.1f %12.1f %10s"
              % ("%.0f h" % p_h, a_m / 1e3, f16, f30, ""))
    ratio = fluxes[27.0][1] / fluxes[32.0][1]
    print("27h/32h tidal flux ratio = %.2f  (a^-15/2 on a %.1f%% smaller orbit)"
          % (ratio, 100 * (1 - fluxes[27.0][0] / fluxes[32.0][0])))
    print()
    for p_h in (27.0, 32.0):
        a_m, f16, _ = fluxes[p_h]
        verdict = "OVER the ceiling -> Tidal Venus" if f16 > ceiling else "under the ceiling"
        print("  %.0f h, e=0.005, k2/Q=0.0016: %6.1f W/m2  %s" % (p_h, f16, verdict))
    print()
    a32, f16_32, _ = fluxes[32.0]
    from greenhouse_dt import greenhouse_increment
    dt_gh = greenhouse_increment(S_REL, 0.198, albedo, ch4_bar=5e-3, hazy=False,
                                 p_total_bar=1.1, teff_k=STAR["teff_k"])
    print("Pandora's greenhouse increment (CO2 18%% + CH4, 1.1 bar) = %+.1f K" % dt_gh)
    print("At 32 h the surface temperature follows the tidal term:")
    for k2q in (0.0000, 0.0010, 0.0016, 0.0030, 0.0060, 0.0150):
        f = tidal_flux(PARENT["m_kg"], r_moon, a32, 0.005, k2q) if k2q else 0.0
        bb = _budget(a_rp, r_km, albedo, inc, f_tidal=f)
        flag = "  <- canon 290 K" if abs(bb["teq"] + dt_gh - 290.0) < 2.0 else ""
        print("  k2/Q %.4f -> tidal %7.1f W/m2 -> T_eq %6.1f K -> Ts %6.1f K%s"
              % (k2q, f, bb["teq"], bb["teq"] + dt_gh, flag))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pandora-27h-vs-32h", action="store_true",
                    help="only the Pandora orbit-choice comparison")
    args = ap.parse_args()
    if args.pandora_27h_vs_32h:
        pandora_orbit_choice()
        return
    validation()
    polyphemus_table()
    pandora_orbit_choice()


if __name__ == "__main__":
    main()
