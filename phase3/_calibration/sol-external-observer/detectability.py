# 태양계를 외부 관측자(기본 10 pc) 시점에서 채널별 검출 가능성을 계산하는 일회성 캘리브레이션 스크립트
"""Solar System detectability from an external observer's vantage.

For each body, compute the signal an exoplanet astronomer would measure
through each channel (radial velocity, astrometry, transit, reflected-light
imaging) plus the equilibrium temperature they would derive under an
albedo assumption, and return a per-channel detection verdict against a
fiducial near-future instrument suite.

Run:  python3 detectability.py [--distance PC]
"""

import argparse
import math

# --- constants ---
M_JUP_IN_M_EARTH = 317.8
M_SUN_IN_M_JUP = 1047.3            # Sun / Jupiter mass ratio
M_SUN_IN_M_EARTH = M_SUN_IN_M_JUP * M_JUP_IN_M_EARTH
R_SUN_IN_R_EARTH = 109.2
R_SUN_IN_AU = 0.004652             # solar radius in AU (transit geometry)
TEQ_CONST_K = 278.3               # T_eq at 1 AU, A=0, L=L_sun

# Fiducial near-future detection floors (at the working distance)
RV_FLOOR_MS = 0.1                 # ESPRESSO-class; ~stellar jitter for the Sun
RV_MAX_BASELINE_YR = 30           # need ~1 full orbit for a clean detection
ASTROM_FLOOR_UAS = 20             # Gaia-class per-mission signal
TRANSIT_FLOOR_PPM = 20            # PLATO / JWST
IMAGING_CONTRAST_FLOOR = 1.0e-9   # Roman CGI / HWO / ELT reflected light
IMAGING_SEP_FLOOR_ARCSEC = 0.10   # inner working angle

# body: name, mass (M_earth), a (AU), period (yr), radius (R_earth),
#       eccentricity, Bond albedo, geometric albedo, mean surface/1-bar T (K)
BODIES = [
    ("Mercury", 0.0553, 0.387,  0.241,  0.383, 0.206, 0.068, 0.142, 440),
    ("Venus",   0.815,  0.723,  0.615,  0.949, 0.007, 0.770, 0.689, 737),
    ("Earth",   1.000,  1.000,  1.000,  1.000, 0.017, 0.306, 0.434, 288),
    ("Mars",    0.107,  1.524,  1.881,  0.532, 0.093, 0.250, 0.170, 210),
    ("Jupiter", 317.8,  5.204, 11.862, 11.21, 0.049, 0.503, 0.538, 165),
    ("Saturn",  95.16,  9.583, 29.457,  9.45, 0.057, 0.342, 0.499, 134),
    ("Uranus",  14.54, 19.191, 84.02,   4.01, 0.046, 0.300, 0.488,  76),
    ("Neptune", 17.15, 30.07, 164.79,   3.88, 0.011, 0.290, 0.442,  72),
    # Titan orbits Saturn; from outside it sits at Saturn's 9.58 AU and
    # cannot be isolated by stellar RV/transit. Listed for the synthesis
    # benchmark only (its star-channel signals are meaningless → shown "—").
    ("Titan",   0.0225, 9.583, 29.457,  0.404, 0.000, 0.265, 0.22,  94),
]


def rv_semi_amplitude(mass_me, period_yr, ecc, mstar_msun=1.0):
    """RV semi-amplitude K [m/s], assuming sin i = 1 (edge-on)."""
    mp_mjup = mass_me / M_JUP_IN_M_EARTH
    total_msun = mstar_msun + mass_me / M_SUN_IN_M_EARTH
    return (28.4329 / math.sqrt(1 - ecc**2)
            * mp_mjup
            * total_msun**(-2.0 / 3.0)
            * period_yr**(-1.0 / 3.0))


def astrometric_signal_uas(mass_me, a_au, dist_pc, mstar_msun=1.0):
    """Stellar reflex semi-major axis projected on sky [micro-arcsec]."""
    a_star_au = (mass_me / M_SUN_IN_M_EARTH) / mstar_msun * a_au
    return a_star_au / dist_pc * 1.0e6


def transit_depth_ppm(radius_re):
    return (radius_re / R_SUN_IN_R_EARTH)**2 * 1.0e6


def transit_probability(a_au):
    return R_SUN_IN_AU / a_au


def imaging_contrast(radius_re, a_au, geom_albedo):
    rp_au = radius_re / R_SUN_IN_R_EARTH * R_SUN_IN_AU
    return geom_albedo * (rp_au / a_au)**2


def imaging_separation_arcsec(a_au, dist_pc):
    return a_au / dist_pc


def t_eq(a_au, albedo, lstar_lsun=1.0):
    return TEQ_CONST_K * (1 - albedo)**0.25 * a_au**-0.5 * lstar_lsun**0.25


def verdict(detected, marginal=False):
    return "marginal" if marginal else ("YES" if detected else "no")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--distance", type=float, default=10.0,
                    help="observer distance in parsecs (default 10)")
    args = ap.parse_args()
    d = args.distance

    print(f"# Solar System detectability @ {d:.0f} pc "
          f"(Sun = G2V, L=1 L_sun)\n")
    hdr = (f"{'body':8} {'K(m/s)':>8} {'RV':>9} {'astro(µas)':>11} {'astro':>9} "
           f"{'tr(ppm)':>8} {'tr.prob':>8} {'img.C':>9} {'img.sep':>8} {'img':>9} "
           f"{'Teq@.3':>7} {'Teq@A':>7} {'Tsurf':>6}")
    print(hdr)
    print("-" * len(hdr))

    for (name, mass, a, p, r, e, bond, geom, tsurf) in BODIES:
        is_moon = (name == "Titan")
        k = rv_semi_amplitude(mass, p, e)
        astro = astrometric_signal_uas(mass, a, d)
        depth = transit_depth_ppm(r)
        prob = transit_probability(a)
        contrast = imaging_contrast(r, a, geom)
        sep = imaging_separation_arcsec(a, d)
        teq_assumed = t_eq(a, 0.30)
        teq_true = t_eq(a, bond)

        # verdicts (moons can't be isolated by star channels)
        if is_moon:
            rv_v = astro_v = tr_v = "—"
        else:
            rv_v = verdict(k >= RV_FLOOR_MS and p <= RV_MAX_BASELINE_YR,
                           marginal=(k >= RV_FLOOR_MS and p > RV_MAX_BASELINE_YR))
            astro_v = verdict(astro >= ASTROM_FLOOR_UAS and p <= RV_MAX_BASELINE_YR,
                              marginal=(astro >= ASTROM_FLOOR_UAS and p > RV_MAX_BASELINE_YR))
        # transit: depth is always >20 ppm here, so the real gate is the
        # geometric alignment lottery — carried by the tr.prob column below.
        img_v = "—" if is_moon else verdict(
            contrast >= IMAGING_CONTRAST_FLOOR and sep >= IMAGING_SEP_FLOOR_ARCSEC)

        print(f"{name:8} {k:8.3f} {rv_v:>9} {astro:11.1f} {astro_v:>9} "
              f"{depth:8.0f} {prob*100:7.3f}% {contrast:9.1e} {sep:8.2f} {img_v:>9} "
              f"{teq_assumed:7.0f} {teq_true:7.0f} {tsurf:6.0f}")

    print(f"\nFloors @ {d:.0f} pc: RV≥{RV_FLOOR_MS} m/s & P≤{RV_MAX_BASELINE_YR} yr | "
          f"astro≥{ASTROM_FLOOR_UAS} µas | transit≥{TRANSIT_FLOOR_PPM} ppm (+alignment) | "
          f"imaging C≥{IMAGING_CONTRAST_FLOOR:.0e} & sep≥{IMAGING_SEP_FLOOR_ARCSEC}\"")
    print("Teq@.3 = equilibrium T assuming Bond albedo 0.30; "
          "Teq@A = with the body's true Bond albedo; Tsurf = actual mean/1-bar T.")


if __name__ == "__main__":
    main()
