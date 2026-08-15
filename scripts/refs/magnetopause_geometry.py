#!/usr/bin/env python3
# 자기권계면 형상 계산기 — Chapman-Ferraro 노즈 + 레짐 판정 + Kerbalism cfg 4필드 도출
"""Magnetopause geometry from the field, per
`docs/reference/planetary-magnetosphere-geometry-methodology.md`.

Three things this computes, in the order the methodology asks them:

1. **Nose** — Chapman-Ferraro balance against whatever flows past the body.
   For a planet that is the stellar wind; for a moon inside a parent's
   magnetosphere it is the *total* confining pressure, which is dominated by
   the parent's magnetic pressure, not by ram.

2. **Regime** — which shape family the boundary belongs to. The Alfven Mach
   number decides it for an embedded moon: sub-Alfvenic flow raises Alfven
   wings instead of a bow shock and a swept tail (Neubauer 1980; Kivelson 2013
   for Ganymede), so the boundary is a sphere, not a Shue surface.

3. **The four cfg fields** — pause_radius / pause_compression /
   pause_extension / pause_height_scale, from alpha and the L = 150 x nose
   tail convention.

Run with no arguments to print the full NearStars + Sol table.
"""

import math

MU0 = 4 * math.pi * 1e-7
AMU = 1.66053907e-27
G = 6.674e-11
M_EARTH = 5.972e24
R_JUP = 71_492e3

# 보드 관행: 태양 1 AU 램압 = 2.0 nPa (Proxima b/c 기존 도출값이 이 값으로 정확히 재현된다)
P_SOLAR_1AU_NPA = 2.0

# Io 토러스 피크 이온밀도와 평균 이온질량 — 위성 레짐의 밀도 기준점
IO_TORUS_PEAK_CM3 = 2000.0
IO_TORUS_ION_AMU = 20.0


def ram_pressure_nPa(mdot_sun, a_au):
    """Stellar-wind ram pressure, scaled from the solar value at 1 AU.

    p ∝ Mdot / r² at fixed wind speed — the speed cancels between the mass
    flux and the v² factor only if it is held equal to the solar value, which
    is what every board in this repo assumes.
    """
    return P_SOLAR_1AU_NPA * mdot_sun / a_au ** 2


def nose_radii(B_eq_uT, p_Pa, f=2.0):
    """R_mp / R_body from Chapman-Ferraro balance (methodology Part A)."""
    B = B_eq_uT * 1e-6
    return (f * f * B * B / (2 * MU0 * p_Pa)) ** (1 / 6)


# Rutala 2025 (2025JGRA..13033842R / arXiv 2502.09186), fitted to observed Jovian
# magnetopause crossings. Both the standoff and the flaring exponent come from it.
def rutala_jupiter_rss(p_nPa):
    return 38.0 * p_nPa ** -0.25


def rutala_jupiter_alpha(p_nPa):
    return 0.28 + 1.08 * p_nPa


def magnetodisc_inflation(p_nPa, B_jup_uT=428.0):
    """How much a Jupiter-class magnetodisc inflates the boundary past vacuum dipole.

    Chapman-Ferraro assumes a vacuum dipole out to the boundary; a rotating,
    plasma-loaded disc pushes it further out. Measured at Jupiter as the ratio
    of the Rutala fit to the Chapman-Ferraro prediction for the same wind.

    The factor is not constant — Chapman-Ferraro goes as p^-1/6 and the fit as
    p^-1/4, so it falls as p^-1/12: a harder wind squeezes the disc out and
    drives the boundary back toward the vacuum answer.
    """
    return rutala_jupiter_rss(p_nPa) / nose_radii(B_jup_uT, p_nPa * 1e-9)


def cfg_fields(nose, alpha, tail_ratio=150.0):
    """The Kerbalism pause fields alpha implies.

    pause_compression = 2^alpha reproduces the Shue flank/nose ratio in the
    stock SDF; the tail closes at L = tail_ratio x nose, so extension is
    pause_radius / L = 2^alpha / tail_ratio. height_scale is 1.0 because Shue
    is axisymmetric — stock's 1.1 squeezes the meridional width by 1/1.1.
    """
    comp = 2.0 ** alpha
    return {
        'pause_radius': nose * comp,
        'pause_compression': comp,
        'pause_extension': comp / tail_ratio,
        'pause_height_scale': 1.0,
        'tail_L': nose * tail_ratio,
    }


def sphere_fields(standoff):
    """The Alfven-wing case: a true sphere at the measured standoff.

    Ganymede precedent — sub-Alfvenic flow means no bow shock and no swept
    tail, so compression, extension and height_scale are all unity.
    """
    return {
        'pause_radius': standoff,
        'pause_compression': 1.0,
        'pause_extension': 1.0,
        'pause_height_scale': 1.0,
        'tail_L': None,
    }


# ---------------------------------------------------------------- moon regime

def corotation_relative_speed(parent_mass_kg, parent_spin_s, r_m):
    """|v_corotation - v_Kepler| at radius r — the flow the moon actually sees.

    Inside the synchronous orbit the moon overtakes the plasma, so the sign
    flips; only the magnitude matters for the Mach number.
    """
    v_corot = 2 * math.pi * r_m / parent_spin_s
    v_kep = math.sqrt(G * parent_mass_kg / r_m)
    return abs(v_corot - v_kep), v_corot, v_kep


def synchronous_radius_m(parent_mass_kg, parent_spin_s):
    return (G * parent_mass_kg * parent_spin_s ** 2 / (4 * math.pi ** 2)) ** (1 / 3)


def alfven_speed(B_T, rho_kg_m3):
    return B_T / math.sqrt(MU0 * rho_kg_m3)


def critical_density_kg_m3(B_T, v_rel):
    """The density at which M_A reaches 1 — the number the regime call turns on."""
    return B_T * B_T / (MU0 * v_rel * v_rel)


def parent_field_T(B_eq_uT, L):
    """Dipole equatorial field at L shells out."""
    return B_eq_uT * 1e-6 / L ** 3


def confining_pressure_Pa(B_parent_T, rho, v_rel):
    """What holds an embedded moon's magnetosphere in.

    Magnetic + ram. At every NearStars moon the magnetic term dominates by an
    order of magnitude, which is why an embedded standoff must not be computed
    from ram alone.
    """
    p_mag = B_parent_T ** 2 / (2 * MU0)
    p_ram = rho * v_rel ** 2
    return p_mag + p_ram, p_mag, p_ram


def softened_shue_r(theta, r0, alpha, L):
    """r(theta) of the closed Shue variant the project adopted.

    eps -> 0 recovers exact Shue; eps > 0 closes the tail at r(180 deg) = L
    with zero slope and no join anywhere.
    """
    eps = 1.0 / ((L / r0) ** (1.0 / alpha) - 1.0)
    c = math.cos(theta / 2.0) ** 2
    return r0 * ((1.0 + eps) / (eps + c)) ** alpha


def _stock_pause_radius_at(x, radius, comp, ext, offset=0.0):
    """Solve the stock pause SDF for the cylindrical radius at a given x.

    SDF = sqrt(px^2 + (y*hs)^2 + z^2) - radius, with px = (x+offset) scaled by
    ext behind the (shifted) origin and comp in front of it.
    """
    px = (x + offset)
    px *= ext if px < 0 else comp
    q = radius * radius - px * px
    return math.sqrt(q) if q > 0 else 0.0


def fit_offset_emulation(r0, alpha, L, samples=400):
    """Least-squares fit of the offset-sphere emulation to the softened Shue curve.

    The stock SDF pins the widest cross-section to the body plane and so cannot
    express the Shue tail flare; shifting the sphere centre tailward before the
    scaling lifts that limit. Returns the four fields plus the worst residual.
    """
    xs, rs = [], []
    for i in range(1, samples):
        th = math.pi * i / samples
        r = softened_shue_r(th, r0, alpha, L)
        xs.append(r * math.cos(th))
        rs.append(r * math.sin(th))

    best = None
    for off in [r0 * k / 40.0 for k in range(0, 121)]:
        for rad in [r0 * k / 40.0 for k in range(20, 201)]:
            # comp is pinned by the nose: at x = r0 the surface must close.
            px_nose = r0 + off
            if px_nose <= 0 or rad <= 0:
                continue
            comp = rad / px_nose
            # extension is pinned by the tail cut at x = -L.
            px_tail = -L + off
            if px_tail >= 0:
                continue
            ext = rad / -px_tail
            err = 0.0
            for x, rr in zip(xs, rs):
                err += (_stock_pause_radius_at(x, rad, comp, ext, off) - rr) ** 2
            if best is None or err < best[0]:
                best = (err, off, rad, comp, ext)
    err, off, rad, comp, ext = best
    worst = max(abs(_stock_pause_radius_at(x, rad, comp, ext, off) - rr)
                for x, rr in zip(xs, rs))
    return {'pause_offset': off, 'pause_offset_radius': rad,
            'pause_offset_compression': comp, 'pause_offset_extension': ext,
            'rms': math.sqrt(err / len(xs)), 'worst': worst}


def _report():
    print('=' * 78)
    print('PLANETS — stellar wind, Shue branch')
    print('=' * 78)
    planets = [
        # name, B_eq uT, Mdot/Mdot_sun, a_AU, alpha, alpha source, magnetodisc?
        ('Polyphemus (A b)', 170.0, 0.5, 1.60, 0.42,
         "Jupiter's fitted ceiling, clamped (owner call 2026-08-16)", True),
        ('Proxima Cen b', 1.2, 0.2, 0.04848, 0.50,
         'Mercury fit (Winslow 2013)', False),
        ('Proxima Cen c', 18.0, 0.2, 1.50, 0.58,
         'Earth by analogy (ice giant)', False),
    ]
    for name, B, mdot, au, alpha, src, disc in planets:
        p_nPa = ram_pressure_nPa(mdot, au)
        nose = nose_radii(B, p_nPa * 1e-9)
        print(f'\n{name}')
        print(f'  B_eq {B} uT | wind {mdot} Mdot_sun @ {au} AU -> p_ram {p_nPa:.4g} nPa')
        print(f'  Chapman-Ferraro nose = {nose:.3f} R_body')
        if disc:
            k = magnetodisc_inflation(p_nPa)
            nose *= k
            print(f'  magnetodisc inflation x{k:.3f} -> nose = {nose:.3f} R_body')
            print(f'  (Rutala alpha evaluated at this pressure would be '
                  f'{rutala_jupiter_alpha(p_nPa):.3f}, 3x beyond calibration)')
        f = cfg_fields(nose, alpha)
        print(f'  alpha = {alpha} ({src})')
        print(f"  radius {f['pause_radius']:.4f}  comp {f['pause_compression']:.4f}  "
              f"ext {f['pause_extension']:.7f}  hs 1.0  | L = {f['tail_L']:.1f} R_body")

    print()
    print('=' * 78)
    print('MOONS — embedded in Polyphemus, Alfven-wing test')
    print('=' * 78)
    M_par = 120 * M_EARTH
    R_par = R_JUP
    spin = 10.35 * 3600
    B_par_eq = 170.0
    r_sync = synchronous_radius_m(M_par, spin)
    print(f'\nPolyphemus: M {M_par:.4g} kg, R {R_par/1e3:.0f} km, spin {spin/3600:.2f} h')
    print(f'  synchronous orbit = {r_sync/R_par:.3f} R_p '
          '(moons inside it overtake the plasma)')

    moons = [
        # name, L (R_p), own B_eq uT
        ('Dante (A b I)', 1.54, 0.0),
        ('Hades (A b II)', 2.07, 0.0),
        ('Pandora (A b III)', 3.53, 75.0),
        ('Cassandra (A b IV)', 8.4, 0.4),
        ('Chaos (A b V)', 21.0, 0.0),
    ]
    rho_io = IO_TORUS_PEAK_CM3 * 1e6 * IO_TORUS_ION_AMU * AMU
    for name, L, B_own in moons:
        r = L * R_par
        v_rel, v_c, v_k = corotation_relative_speed(M_par, spin, r)
        B_par = parent_field_T(B_par_eq, L)
        rho_crit = critical_density_kg_m3(B_par, v_rel)
        n_crit = rho_crit / (IO_TORUS_ION_AMU * AMU) / 1e6
        print(f'\n{name}  L = {L} R_p')
        print(f'  v_corot {v_c/1e3:6.2f}  v_kep {v_k/1e3:6.2f}  -> v_rel {v_rel/1e3:6.2f} km/s')
        print(f'  parent B at L = {B_par*1e6:.3f} uT')
        print(f'  M_A = 1 needs n = {n_crit:.3g} ions/cm3 '
              f'= {n_crit/IO_TORUS_PEAK_CM3:.4g} x the Io torus PEAK')
        if B_own > 0:
            p_tot, p_mag, p_ram = confining_pressure_Pa(B_par, rho_io * 0.02, v_rel)
            standoff = nose_radii(B_own, p_tot)
            print(f'  confining p = {p_tot*1e6:.3f} uPa '
                  f'(magnetic {p_mag*1e6:.3f} + ram {p_ram*1e6:.3f})')
            print(f'  own standoff = {standoff:.3f} R_moon')


if __name__ == '__main__':
    _report()
