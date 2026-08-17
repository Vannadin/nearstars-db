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
K_B = 1.380649e-23
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


def wing_tail_ratio(M_A, base=150.0):
    """Tail length ratio for a sub-Alfvenic body, in nose radii.

    Owner decision 2026-08-17: an Alfven wing enters the game as nothing more
    than **a shorter Shue tail**. The wing's own geometry — the tube, the
    landing on the parent's ionosphere, the reflected fan — is visualisation
    material and does not reach a cfg.

    The ratio interpolates geometrically between a sphere and the ordinary
    `base`, which costs no new coefficient and lands exactly on both ends:

        ratio = base ** M_A          ratio(0) = 1 (sphere), ratio(1) = base

    Scaling `base` *linearly* by M_A was the first attempt and is wrong at the
    small end: at A b III's M_A 0.0096 it asks for a tail 44% longer than the
    nose, where the physical day-night asymmetry is 0.01%. The geometric form
    gives 5% there, and 11 nose radii at Ganymede's M_A 0.48 against the usual
    150 — short, as intended, and reached continuously rather than by a switch.
    """
    return float(base) ** float(M_A)


def sphere_fields(standoff):
    """A true sphere at the measured standoff — the M_A -> 0 limit.

    Kept for the degenerate case and for boards written before the tail-ratio
    rule above; `cfg_fields(nose, alpha, wing_tail_ratio(M_A))` reaches the same
    place continuously and is what new work should use.
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


# ------------------------------------------------- Alfven wings (3D geometry)
#
# A sub-Alfvenic obstacle raises no bow shock and no swept tail. What it raises
# instead is a pair of standing Alfven waves — the wings — and their geometry is
# fully determined by three numbers we already compute per body: the Alfven Mach
# number (tilt), the obstacle size (cross-section), and the parent's field-line
# curvature (how far the straight-tube description survives).
#
# Sources, all read in full:
#   Neubauer 1980, 1980JGR....85.1171N — the wing model; currents follow the
#     Alfven characteristics.
#   Saur review 1908.06446 §4.2 — "The wings are inclined with respect to the
#     background magnetic field by an angle tan^-1 M_A (Neubauer, 1980)", the
#     Elsasser characteristics z+- = v +- B/sqrt(mu0 rho), and (their Figure 3)
#     "the purple tube characterizes the boundary of the main wing which
#     corresponds to the size of the source, i.e. the moon".
#   Saur 2013 eq. 57, quoted by Fischer & Saur 2019 (1901.02747) — the effective
#     obstacle radius R_eff = k R_obst, with k = sqrt(3) when the body's dipole
#     is parallel to the ambient field.


def alfven_mach_number(v_rel, B_T, rho):
    """M_A = |v_rel| / v_A — the number the whole regime call turns on."""
    return v_rel / alfven_speed(B_T, rho)


def alfven_wing_angle(M_A):
    """Tilt of each wing away from the background field, in radians.

    tan(theta_A) = M_A: the wave travels along B0 at v_A while the flow carries
    it downstream at v_0, so the standing structure leans by the ratio.
    """
    return math.atan(M_A)


def wing_tube_radius(R_obst):
    """Geometric radius of the wing tube — equal to the obstacle radius.

    Two independent statements give the same answer. Flux conservation: an
    obstacle of radius R_obst excludes B0 pi R_obst^2 of ambient flux, and the
    ambient field is uniform outside, so the tube carrying that flux has the
    same radius. And the Saur review's Figure 3 caption, describing the drawn
    wing boundary: "The purple tube characterizes the boundary of the main wing
    which corresponds to the size of the source, i.e., the moon."

    Do **not** use `alfven_effective_radius` for the shape; that is a different
    quantity (see its docstring).
    """
    return R_obst


def alfven_effective_radius(R_obst, k=math.sqrt(3.0)):
    """Flux-equivalent obstacle radius for the *Poynting flux*, Saur 2013 eq. 57.

    R_eff = k R_obst is defined so that the wing's energy flux comes out right;
    it is larger than the tube the wing actually occupies because the ambient
    field lines are focused toward a magnetized obstacle. It sizes the power,
    not the surface — `wing_tube_radius` sizes the surface.

    k = sqrt(3) is the parallel-dipole maximum. An unmagnetized conducting
    obstacle (Io-like) takes k = 1 with R_obst the ionospheric radius. The
    anti-parallel case — Ganymede's, where the moon's moment opposes the
    ambient field — is measured *larger* than the aligned one in the MHD fits
    (Strugarek 2016, 1610.05705 §3.3), so sqrt(3) is a floor there, not a cap.
    """
    return k * R_obst


def dipole_curvature_radius(L_shell_m):
    """Radius of curvature of a dipole field line at its equatorial crossing.

    r = r_eq cos^2(lat) has curvature radius r_eq / 3 at the equator. This is
    what bends the wing away from a straight tube.
    """
    return L_shell_m / 3.0


def wing_straight_length(R_wing_m, R_curv_m):
    """How far the straight-tube description holds, in metres.

    The wing follows the parent's field line, which departs from its own
    tangent by ~l^2 / (2 R_curv). Setting that departure equal to the wing's
    own radius gives the length at which the tube has visibly bent:

        l = sqrt(2 R_wing R_curv)

    Past it the wing continues — undamped, all the way to the parent's
    ionosphere — but as a curved flux tube, not as this cylinder.
    """
    return math.sqrt(2.0 * R_wing_m * R_curv_m)


def alfven_wing_axes(M_A, flow_sign=1.0, field_sign=1.0):
    """Unit vectors of the two wings in the Kerbalism gsm frame.

    Frame, for a moon whose RadiationBody sets `reference` to its parent:
    x = toward the parent, y = spin axis (= the parent's field direction at the
    moon, up to sign), z = x cross y = the orbital direction. The corotating
    plasma overtakes a moon outside synchronous orbit, so the flow runs along
    +z there and -z inside it — that is `flow_sign`. `field_sign` is +1 when
    the ambient field points along +y (Earth-like parent) and -1 when it points
    along -y (Jupiter-like, whose dipole is reversed).

    Returns (w_plus, w_minus) as (x, y, z) tuples, from the characteristics
    c+- = v0 +- v_A Bhat normalized: direction ∝ M_A vhat +- Bhat. Both carry
    the same downstream component, so both wings lean downstream.
    """
    v = (0.0, 0.0, flow_sign)
    b = (0.0, field_sign, 0.0)
    out = []
    for s in (1.0, -1.0):
        w = tuple(M_A * v[i] + s * b[i] for i in range(3))
        n = math.sqrt(sum(c * c for c in w))
        out.append(tuple(c / n for c in w))
    return out[0], out[1]


def sub_alfvenic_compression(M_A):
    """Day-night standoff asymmetry of a sub-Alfvenic obstacle.

    The confinement is magnetic pressure B0^2/2mu0 everywhere plus ram
    rho v^2 on the upstream side only; their ratio is 2 M_A^2, and the standoff
    goes as p^(-1/6), so the upstream side is closer in by (1 + 2 M_A^2)^(1/6).
    This is the number that licenses drawing the obstacle as a sphere: at
    M_A 0.5 it is 8%, and it falls to nothing as the flow slows.
    """
    return (1.0 + 2.0 * M_A * M_A) ** (1.0 / 6.0)


def derive_wing_geometry(parent_mass_kg, parent_radius_m, parent_spin_s,
                         parent_B_eq_uT, L_shell, moon_radius_m,
                         moon_B_eq_uT=0.0, plasma_cm3=IO_TORUS_PEAK_CM3 * 0.02,
                         ion_amu=IO_TORUS_ION_AMU, ionosphere_radii=1.0,
                         parent_field_sign=-1.0, parent_exo_T_K=1000.0,
                         parent_exo_mu=1.0):
    """Every number the 3D wing shape needs, from physical inputs only.

    Nothing here is authored: the tilt comes from the Mach number, the tube
    radius from the obstacle, the straight length from the parent's field-line
    curvature. Lengths in the returned dict are in *moon radii*, which is the
    unit Kerbalism's SDF works in.

    `ionosphere_radii` is the obstacle size for an unmagnetized moon (Io-like);
    it is ignored when the moon has a field of its own, where the obstacle is
    the Chapman-Ferraro standoff against the total confining pressure.
    """
    r = L_shell * parent_radius_m
    v_rel, v_corot, v_kep = corotation_relative_speed(
        parent_mass_kg, parent_spin_s, r)
    B_local = parent_field_T(parent_B_eq_uT, L_shell)
    rho = plasma_cm3 * 1e6 * ion_amu * AMU
    v_A = alfven_speed(B_local, rho)
    M_A = v_rel / v_A

    if moon_B_eq_uT > 0:
        p_tot, _, _ = confining_pressure_Pa(B_local, rho, v_rel)
        R_obst = nose_radii(moon_B_eq_uT, p_tot)
    else:
        R_obst = ionosphere_radii

    R_tube = wing_tube_radius(R_obst)
    R_curv = dipole_curvature_radius(r)
    length = wing_straight_length(R_tube * moon_radius_m, R_curv) / moon_radius_m
    # 동기궤도 밖이면 플라스마가 위성을 추월한다 → 흐름은 +z(공전 방향).
    flow_sign = 1.0 if r > synchronous_radius_m(parent_mass_kg, parent_spin_s) else -1.0

    g_parent = surface_gravity(parent_mass_kg, parent_radius_m)
    H = ionospheric_scale_height_m(parent_exo_T_K, parent_exo_mu, g_parent)

    return {
        'v_rel_km_s': v_rel / 1e3,
        'v_corot_km_s': v_corot / 1e3,
        'v_kep_km_s': v_kep / 1e3,
        'B_local_nT': B_local * 1e9,
        'v_A_km_s': v_A / 1e3,
        'M_A': M_A,
        'sub_alfvenic': M_A < 1.0,
        'theta_A_deg': math.degrees(alfven_wing_angle(M_A)),
        'R_obst': R_obst,
        'R_tube': R_tube,
        'R_eff_flux': alfven_effective_radius(R_obst),
        'compression': sub_alfvenic_compression(M_A),
        'R_curv_parent_radii': R_curv / parent_radius_m,
        'length': length,
        'flow_sign': flow_sign,
        'field_sign': parent_field_sign,
        'parent_gravity': g_parent,
        'scale_height_m': H,
        'landing_floor': H / moon_radius_m,
        'axes': alfven_wing_axes(M_A, flow_sign, parent_field_sign),
    }


def ionospheric_scale_height_m(T_K, mu_amu, g_m_s2):
    """H = kT / (mu m_u g) — the thickness of the layer the wing lands in.

    This is the one length that keeps the landing honest. Flux conservation
    alone would have the tube meet a mathematical surface at a mathematical
    edge, but the conductor it actually terminates on is a shell hundreds of
    kilometres deep, and the wing dissolves into it rather than striking it.
    So H does two jobs: it is the fillet radius at the junction, and it is the
    floor on the tube radius, because a tube cannot stay thinner than the layer
    it is diffusing into.

    Take the *upper* ionosphere's composition — atomic H at Jupiter, not H2.
    That is the deeper layer and therefore the generous end of the estimate,
    which is the right side to err on for a boundary we are drawing rather than
    measuring.
    """
    return K_B * T_K / (mu_amu * AMU * g_m_s2)


def surface_gravity(mass_kg, radius_m):
    return G * mass_kg / radius_m ** 2


# 착지 필렛은 H 의 몇 배인가. 바닥값(관이 그보다 가늘 수 없는 두께)은 H 한 장이지만,
# 전류가 닫히는 전도층 자체는 한 장이 아니라 여러 장에 걸쳐 있다 — 전도도 프로파일은
# 스케일 높이 규모의 폭을 가진 봉우리이고, 그 봉우리의 어깨까지가 관이 풀리는 구간이다.
# 그래서 물리적으로 방어되는 창은 1~3 H 이고, 그 안에서 어디를 쓸지는 아트 선택이다.
FILLET_SCALE_WINDOW = (1.0, 3.0)
FILLET_SCALE_DEFAULT = 3.0


def dipole_wing_path(L_shell, parent_radius_m, moon_radius_m, M_A_local,
                     parent_mass_kg, parent_spin_s, parent_B_eq_uT,
                     rho, R_tube, hemisphere=1.0, flow_sign=1.0, steps=260,
                     min_radius=0.0):
    """The wing as it actually runs: a curved, narrowing flux tube to the parent.

    A wing does not end in space. It follows the parent's field line through the
    moon, and that line lands on the parent's ionosphere — the auroral footprint
    the wing paints there is the observable end of the structure (Neubauer 1980;
    the review 1908.06446 §3.3 for the reflection that follows). Two things
    happen along the way, both derivable:

    * **It bends.** The dipole line curves, r = r_eq cos^2(lat), and the local
      Alfven tilt rides on top of it. The tilt is not constant: v_A rises steeply
      as the field strengthens toward the parent, so M_A falls and the wing
      straightens onto the field line. We integrate the local tilt rather than
      assume the one measured at the moon, holding rho fixed along the tube (the
      one assumption here, and the reason the far end is the rough part).

    * **It narrows.** Magnetic flux is conserved, so the tube radius goes as
      1/sqrt(B). By the ionosphere the field is orders of magnitude stronger and
      the tube has closed to a spot — which is why the footprint is a spot.

    `min_radius` is the floor from `ionospheric_scale_height_m` (in moon radii);
    below it the tube is thinner than the layer it lands in, which the flux
    argument has no way to know.

    Returns a list of (point, radius) with the point in moon radii in the gsm
    frame and the radius in moon radii too. `hemisphere` +1 runs to the parent's
    north, -1 to its south; those are the two wings. The path is a geometric
    curve, so it does not depend on which way the parent's field points — only
    the Elsasser label (which wing is z+) does.
    """
    r_eq = L_shell * parent_radius_m
    B_moon = parent_field_T(parent_B_eq_uT, L_shell)
    lat_max = math.acos(math.sqrt(min(1.0, parent_radius_m / r_eq)))

    path, s, phi = [], 0.0, 0.0
    prev = None
    for i in range(steps + 1):
        lat = hemisphere * lat_max * i / steps
        r = r_eq * math.cos(lat) ** 2
        rho_cyl, Y = r * math.cos(lat), r * math.sin(lat)   # 자전축까지 거리, 축방향
        B = parent_B_eq_uT * 1e-6 * math.sqrt(1 + 3 * math.sin(lat) ** 2) \
            / (r / parent_radius_m) ** 3

        # 하류 변위는 자전축 둘레의 **방위각 회전**이다. 평행이동으로 넣으면
        # 끝이 전리층을 벗어나 허공에 뜬다 — 실제로는 자전축 대칭이므로 회전된
        # 동일 자기력선 위에 남고, 착지점만 경도로 밀린다(Io 발자국의 lead angle).
        if prev is not None:
            ds = math.dist((rho_cyl, Y), prev)
            v_rel, _, _ = corotation_relative_speed(parent_mass_kg, parent_spin_s, r)
            M = v_rel / alfven_speed(B, rho)
            s += ds
            phi += ds * math.sin(alfven_wing_angle(M)) / max(rho_cyl, 1e-9)
        prev = (rho_cyl, Y)

        X_p, Z_p = rho_cyl * math.cos(phi), rho_cyl * math.sin(phi)
        p = (-(X_p - r_eq) / moon_radius_m,
             Y / moon_radius_m,
             flow_sign * Z_p / moon_radius_m)

        # 플럭스 보존: 관 반경 ∝ 1/sqrt(B). 다만 착지층 두께 아래로는 못 내려간다.
        path.append((p, max(R_tube * math.sqrt(B_moon / B), min_radius)))
    return _resample_by_arclength(path, steps)


def _resample_by_arclength(path, count):
    """Even spacing along the curve.

    Sampling uniformly in latitude puts the long segments right at the moon,
    where the shape needs the resolution, and wastes them near the pole. The
    renderer's polyline shows that as a crease at the joint.
    """
    pts = [p for p, _ in path]
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    total = acc[-1]
    if total <= 0:
        return path

    out, j = [], 0
    for i in range(count + 1):
        target = total * i / count
        while j < len(acc) - 2 and acc[j + 1] < target:
            j += 1
        span = acc[j + 1] - acc[j]
        f = 0.0 if span <= 0 else (target - acc[j]) / span
        (pa, ra), (pb, rb) = path[j], path[j + 1]
        out.append((tuple(pa[k] + (pb[k] - pa[k]) * f for k in range(3)),
                    ra + (rb - ra) * f))
    return out


def wing_path_sdf(p, path, cap_index=None):
    """Distance to a swept-sphere polyline — the curved tube `dipole_wing_path`
    describes. `cap_index` truncates the path, for near-field renders."""
    pts = path if cap_index is None else path[:cap_index]
    best = float('inf')
    for (a, ra), (b, rb) in zip(pts, pts[1:]):
        ab = tuple(b[i] - a[i] for i in range(3))
        ap = tuple(p[i] - a[i] for i in range(3))
        den = sum(c * c for c in ab) or 1e-12
        t = max(0.0, min(1.0, sum(ap[i] * ab[i] for i in range(3)) / den))
        d = math.sqrt(sum((ap[i] - t * ab[i]) ** 2 for i in range(3)))
        best = min(best, d - (ra + (rb - ra) * t))
    return best


def _capsule_sdf(p, axis, length, radius):
    """Signed distance to a capsule from the origin along `axis` for `length`."""
    t = sum(p[i] * axis[i] for i in range(3))
    t = 0.0 if t < 0.0 else (length if t > length else t)
    d = math.sqrt(sum((p[i] - t * axis[i]) ** 2 for i in range(3)))
    return d - radius


def _smin(a, b, k):
    """Polynomial smooth minimum — the wings join the obstacle, they do not
    intersect it with a crease."""
    if k <= 0.0:
        return min(a, b)
    h = max(0.0, min(1.0, 0.5 + 0.5 * (b - a) / k))
    return b * (1 - h) + a * h - k * h * (1 - h)


def alfven_wing_sdf(p, R_obst, R_wing, M_A, length,
                    flow_sign=1.0, field_sign=1.0, blend=None):
    """The exact 3D signed distance of an Alfven-wing boundary.

    Union of the obstacle — a sphere, because a sub-Alfvenic obstacle is not
    compressed on any side — with the two wing tubes, blended so the surface is
    smooth where they meet. `p` is in body radii in the gsm frame; every length
    argument is in body radii too.

    `blend` defaults to half the obstacle radius. It is a convention, not a
    derived value: the wing attaches to the interaction region continuously,
    but no published fit gives the fillet.
    """
    if blend is None:
        blend = 0.5 * R_obst
    wp, wm = alfven_wing_axes(M_A, flow_sign, field_sign)
    d = math.sqrt(p[0] ** 2 + p[1] ** 2 + p[2] ** 2) - R_obst
    for axis in (wp, wm):
        d = _smin(d, _capsule_sdf(p, axis, length, R_wing), blend)
    return d


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
    print('BROWN DWARFS — isolated pair, ISM ram, astrosphere-style Shue branch')
    print('=' * 78)
    # Luhman 16: no stellar wind — the obstacle pressure is the pair's own motion
    # through the LISM. v_rel from db/refs/lism_kinematics.yaml cloud vectors
    # (G/LIC/Blue span 24-28 km/s); n from the warm-cloud range, 0.2 cm-3 nominal.
    # B_eq = equatorial dipole = B_dyn / (2 sqrt 2) with B_dyn from the
    # planetary-dynamo-scaling BD branch (dynamo at the surface).
    LIC_B_T = 3e-10          # ~3 uG local-cloud field (IBEX-ribbon scale)
    n_ism_cm3 = 0.2
    v_rel_ms = 26e3
    rho_ism = n_ism_cm3 * 1e6 * AMU   # H-dominated
    p_ism_Pa = rho_ism * v_rel_ms ** 2
    v_A_ism = alfven_speed(LIC_B_T, rho_ism)
    bds = [
        # name, B_dyn G (dynamo BD branch), R_body m
        ('Luhman 16 A', 1246.0, 62_613e3),
        ('Luhman 16 B', 1177.0, 62_613e3),
    ]
    print(f'\nISM: n {n_ism_cm3} cm-3, v_rel {v_rel_ms/1e3:.0f} km/s -> '
          f'p_ram {p_ism_Pa*1e9:.4g} nPa | v_A(LIC) {v_A_ism/1e3:.1f} km/s '
          f'-> M_A {v_rel_ms/v_A_ism:.2f} (super-Alfvenic: real tail, Shue branch)')
    for name, B_dyn_G, R_bd in bds:
        B_eq_uT = B_dyn_G * 100.0 / (2.0 * math.sqrt(2.0))
        nose = nose_radii(B_eq_uT, p_ism_Pa)
        alpha = 0.42   # rotation-dominated magnetosphere -> Jupiter's fitted
                       # ceiling, clamped (same owner call as Polyphemus)
        f = cfg_fields(nose, alpha)
        au = nose * R_bd / 1.495978707e11
        print(f'\n{name}')
        print(f'  B_dyn {B_dyn_G:.0f} G -> B_eq {B_eq_uT:.0f} uT')
        print(f'  Chapman-Ferraro nose = {nose:.0f} R_body = {au:.3f} AU')
        print(f'  alpha = {alpha} (Jupiter fitted ceiling by analogy, '
              'rotation-dominated)')
        print(f"  radius {f['pause_radius']:.1f}  comp {f['pause_compression']:.4f}  "
              f"ext {f['pause_extension']:.7f}  hs 1.0  | L = {f['tail_L']:.0f} R_body"
              f" = {f['tail_L']*R_bd/1.495978707e11:.1f} AU")

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


# ---------------------------------------------------- Shue → 스톡 인코딩 변환

def _px_gen(x, comp, ext, waist, smooth):
    u = x - waist
    if smooth <= 0:
        return u * (ext if u < 0 else comp)
    return 0.5 * (comp + ext) * u + 0.5 * (comp - ext) * math.sqrt(u * u + smooth * smooth)


def _width_gen(x, rad, comp, ext, waist, smooth):
    q = rad * rad - _px_gen(x, comp, ext, waist, smooth) ** 2
    return math.sqrt(q) if q > 0 else 0.0


def _constrain(r0, L, rad, smooth, comp=1.0):
    """노즈 px(r0)=rad 와 꼬리 px(-L)=-rad 를 waist·ext 에 대해 교대 수렴."""
    waist, ext = -0.5 * r0, rad / L
    for _ in range(60):
        lo, hi = -40 * r0, r0 - 1e-12
        for _ in range(100):
            m = (lo + hi) / 2
            if _px_gen(r0, comp, ext, m, smooth) < rad:
                hi = m
            else:
                lo = m
        waist = (lo + hi) / 2
        elo, ehi = 1e-14, comp
        for _ in range(100):
            m = (elo + ehi) / 2
            if _px_gen(-L, comp, m, waist, smooth) > -rad:
                elo = m
            else:
                ehi = m
        ext = (elo + ehi) / 2
    return waist, ext


def shue_to_stock(r0, alpha, tail_ratio=150.0, samples=500, grid=(101, 61), span=4.0):
    """Fit the generalised stock pause to a softened Shue surface.

    This *is* how the project implements Shue. Rather than evaluate `r(θ)` in the
    engine — which would need a polar form converted to a Cartesian signed
    distance, plus new domain and offset formulas, plus a re-check of the
    particle-mesh shell — the four stock fields are fitted to the Shue surface
    once, offline. `compression` is retired to 1.0 and `waist` carries the
    asymmetry, because compression pins the widest cross-section to the body
    plane while Shue puts it behind the planet.

    The result depends only on alpha: normalise by `r0` and bodies sharing an
    alpha get identical `rad/r0`, `waist/r0`, `ext` and `smooth/rad`.

    Residual against the target is a few percent, smaller than the physical
    spread in alpha itself — Shue 1998 has alpha = (0.58 − 0.007·Bz)(1 + 0.024·ln Dp),
    so a ±5 nT swing in IMF Bz moves the tail width by about ±20%.
    """
    L = tail_ratio * r0
    target = []
    for i in range(1, samples):
        th = math.pi * i / samples
        r = softened_shue_r(th, r0, alpha, L)
        target.append((r * math.cos(th), r * math.sin(th)))

    nr, ns = grid
    best = None
    for ri in range(nr):
        rad = r0 * (1 + ri * 0.05)
        for si in range(ns):
            smooth = rad * (si / (ns - 1.0) * span)
            waist, ext = _constrain(r0, L, rad, smooth)
            if abs(_width_gen(r0, rad, 1.0, ext, waist, smooth)) > 1e-4:
                continue
            err = math.sqrt(sum((_width_gen(x, rad, 1.0, ext, waist, smooth) - y) ** 2
                                for x, y in target) / len(target))
            if best is None or err < best[0]:
                best = (err, rad, ext, waist, smooth)
    err, rad, ext, waist, smooth = best
    return {'pause_radius': rad, 'pause_compression': 1.0, 'pause_extension': ext,
            'pause_waist': waist, 'pause_smooth': smooth,
            'pause_height_scale': 1.0, 'tail_L': L, 'rms': err}
