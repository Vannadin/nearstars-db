#!/usr/bin/env python3
# 페트로바선 기하 — 극에서 수직 상승 → 림 이탈 고도에서 꺾임 → 목표를 덮으며 종단
"""Petrova-line geometry, built the same way the Alfven wing was: physical
inputs in, a path plus a radius profile out.

This is *not* a magnetic arc. The shape the owner specified has four parts:

1. leave the star at the top of its spin axis,
2. climb straight along the axis,
3. curve over continuously — never a corner, and never a localised arc
   either, because the clearance it steers by improves all the way,
4. reach the target with the cross-section widened to cover its whole disc.

Only (3) needs an argument, and it turns out to be geometric. From directly
over the pole the target sits *on the star's limb* — the sight line to it
grazes the photosphere — so at the surface it is not separable at all. Climb,
and the target rises off the limb. The sight line from height H to a target at
orbital radius `a` passes the star's centre at an impact parameter

    b(H) = H a / sqrt(H^2 + a^2)

and setting b = R_star shows the sight line clears the photosphere almost
immediately, only 14 km above Sol's pole. But clearing it
is not the same as reading it: a star's surface brightness does not fall with
distance, so a target one degree off the limb is still against a wall of
light. The criterion that decides the knee is therefore the **angular gap**
between the target and the limb,

    gap(H) = arccos(H / sqrt(a^2 + H^2)) - arcsin(R_star / H)   ->   H = R_star / cos(gap)

for a target well outside the star — and that gap is **not monotonic**: climbing lifts the target off the limb, but
it also swings the target toward the downward axis, and the second effect wins
in the end. So there is a height of maximum clearance, and it is the geometric
mean of the star's radius and the orbit,

    H_best = sqrt(R_star * a)

which for Sol and Venus is 12.5 R_sun at a gap of 81 degrees. The knee
therefore needs no threshold at all — it sits where the target is easiest to
read. That removes the last free coefficient from the path; only the beam's
starting radius is still a choice.

Aiming is a separate matter from shape. Astrophage cross at light speed, so
the target moves about one of its own diameters during transit and the path
curves by 24 arcsec — invisible. But the light the traveller sees is equally
delayed, so the aim point leads the *apparent* position by twice the transit
displacement. That offset is returned for the record; it does not bend the
drawn line.
"""

import math

C = 2.99792458e8


def limb_grazing_height(R_star_m, a_m):
    """Height at which the sight line to the target just grazes the limb.

    The sight line from (0, H) to (a, 0) passes the star's centre at
    b = H a / sqrt(H^2 + a^2); setting b = R_star gives this. It is the
    *lower* bound and nothing more: clearing the limb geometrically still
    leaves the target pressed against a wall of photosphere.
    """
    return R_star_m * a_m / math.sqrt(a_m * a_m - R_star_m * R_star_m)


def limb_gap_deg(H_m, R_star_m, a_m):
    """Angle between the target and the star's limb, seen from height H.

    Two angles measured at the traveller: the target sits
    arccos(H / sqrt(a^2+H^2)) from straight down, and the limb sits
    arcsin(R_star / H) from the same axis. The difference is how much dark sky
    separates them.
    """
    if H_m <= R_star_m:
        return -math.degrees(math.asin(min(1.0, R_star_m / max(H_m, 1e-9))))
    theta_t = math.acos(H_m / math.hypot(a_m, H_m))
    alpha = math.asin(min(1.0, R_star_m / H_m))
    return math.degrees(theta_t - alpha)


def best_gap_height(R_star_m, a_m, samples=20000):
    """The height at which the target stands *maximally* clear of the limb.

    The gap is not monotonic, and that is the useful fact. Climbing lifts the
    target off the limb, but it also swings the target toward the downward
    axis, and past a point the second effect wins. Setting d(gap)/dH = 0,

        R / (H sqrt(H^2 - R^2))  =  a / (a^2 + H^2)

    and taking H >> R_star, H << a gives the whole answer at once:

        H_best = sqrt(R_star * a)

    the geometric mean of the star's radius and the orbit. So the knee needs no
    threshold at all — it sits where the target is easiest to see, which is a
    derived height, not a chosen one. For Sol and Venus that is 12.5 R_sun,
    with a maximum gap of 81 degrees.

    Solved numerically here (the closed form is the large-ratio limit), which
    also keeps it honest for a target close in, where the two effects trade off
    at a different place.
    """
    lo = limb_grazing_height(R_star_m, a_m)
    hi = a_m * 0.9
    best_H, best_g = lo, limb_gap_deg(lo, R_star_m, a_m)
    for i in range(1, samples + 1):
        # 기하평균 근처가 답이므로 로그 격자로 훑는다.
        H = lo * (hi / lo) ** (i / samples)
        g = limb_gap_deg(H, R_star_m, a_m)
        if g > best_g:
            best_H, best_g = H, g
    return best_H, best_g


def glare_clearance_height(R_star_m, a_m, gap_deg=60.0):
    """Height at which the target stands `gap_deg` clear of the star's limb.

    This is the criterion that matters, not bare limb clearance. A star's
    surface brightness does not fall with distance, so what decides whether the
    target is readable is how far it sits from the bright edge — and that gap
    is a function of height alone. For a target well outside the star it
    reduces to

        H = R_star / cos(gap)

    so 30 deg of dark sky costs a 1.15 R_star climb, 60 deg costs 2.0, and
    75 deg costs 3.9. The gap itself is the ungrounded knob: it stands in for
    the navigator's tolerance to scattered light, which we have no model for.
    Solved numerically here so the finite orbit is included rather than assumed
    away.
    """
    lo, hi = limb_grazing_height(R_star_m, a_m) * (1 + 1e-12), a_m * 0.5
    if limb_gap_deg(hi, R_star_m, a_m) < gap_deg:
        raise ValueError('that gap is unreachable below half the orbit')
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if limb_gap_deg(mid, R_star_m, a_m) < gap_deg:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def gap_band(R_star_m, a_m, frac=0.99, samples=40000):
    """Height range over which the target is within `frac` of its best clearance.

    The knee is not a corner, and this is why. The gap curve is broad around
    its maximum — for Sol and Venus it stays within 1% of the peak from
    8.3 to 19.1 stellar radii — so there is no single height at which turning
    suddenly becomes right. The turn is spread across the band, which makes it
    an arc, and the band's width sets the arc's radius. `frac` is the only
    coefficient and a weak one: the band moves slowly with it.
    """
    H_best, g_best = best_gap_height(R_star_m, a_m)
    target = g_best * frac
    lo = hi = None
    base = limb_grazing_height(R_star_m, a_m)
    for i in range(1, samples + 1):
        H = base * (a_m * 0.9 / base) ** (i / samples)
        if limb_gap_deg(H, R_star_m, a_m) >= target:
            lo = H if lo is None else lo
            hi = H
    return lo, hi, H_best, g_best


def aim_lead_m(a_m, v_orbit_m_s, speed_frac_c=1.0):
    """How far ahead of the *apparent* target position the beam must aim.

    One transit time of target motion to lead it, plus one more because the
    light the traveller navigates by is that same transit time stale.
    """
    transit = a_m / (speed_frac_c * C)
    return 2.0 * v_orbit_m_s * transit, transit


def _bezier_apex(P0, P1y, P2, samples=4000):
    """Highest point of the quadratic Bezier, and where along it that falls."""
    best = (-1e300, 0.0)
    for i in range(samples + 1):
        t = i / samples
        y = (1 - t) ** 2 * P0[1] + 2 * t * (1 - t) * P1y + t * t * P2[1]
        if y > best[0]:
            best = (y, t)
    return best


def _solve_control(P0, P2, apex_target, lo=None, hi=None):  # noqa: D401
    """Control height whose curve peaks exactly at the derived clearance height."""
    lo = P0[1] if lo is None else lo
    hi = apex_target * 6 if hi is None else hi
    for _ in range(160):
        mid = 0.5 * (lo + hi)
        if _bezier_apex(P0, mid, P2)[0] < apex_target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def petrova_path(R_star_m, a_m, R_target_m, gap_deg=None,
                 start_radius_m=None, steps=1400, funnel_tangent_deg=60.0):
    """The line as (point, radius) samples, in metres, star-centred.

    Frame: y is the spin axis, the target sits at x = a in the equatorial
    plane, so the whole line lies in the x-y plane.

    **One curve, not three segments.** An earlier build had a straight climb, a
    tangent arc and a straight run, which is defensible but wrong in spirit:
    the clearance the traveller steers by improves continuously, so the turn is
    spread over the whole trip rather than banked into one corner. The curve is
    therefore a quadratic Bezier from the pole to the target, and it needs no
    coefficient of its own — the control height is solved so that the curve's
    apex sits exactly at the maximum-clearance height sqrt(R_star a). That
    fixes everything at once: it leaves the pole along the spin axis, it peaks
    where the target is easiest to read, it arrives on the target's bearing,
    and its curvature is continuous end to end.

    `funnel_tangent_deg` is the latitude, measured from the pole, at which the
    funnel touches the star. It is the shape's one free coefficient and is
    meant to be set per system from cfg. Everything else about the funnel
    follows from it: the mouth is R sin(phi), the touch height R cos(phi), and
    the decay rate cos(phi) / (R sin^2(phi)) is whatever makes the curve leave
    the surface tangentially rather than cutting across it.

    The cross-section is wide at **both** ends and narrow between. At the star
    it opens into a funnel a stellar radius across — the stream gathers off the
    whole body, not out of a point — and pinches in fast, over a fraction of a
    stellar radius, so that it reads as a funnel rather than a long horn.
    `funnel_scale` is that decay length in stellar radii and is a shape
    coefficient, not a derived one: the gathering region has no scale to hang
    it on but the star's own size. At the far end it opens again to cover the
    target's disc.
    `start_radius_m` is the waist between them, and must be smaller than the
    target's radius for that second opening to happen; it defaults to a quarter
    of it.
    """
    if start_radius_m is None:
        start_radius_m = 0.25 * R_target_m
    H_best = (best_gap_height(R_star_m, a_m)[0] if gap_deg is None
              else glare_clearance_height(R_star_m, a_m, gap_deg))

    # 경로는 항성 표면이 아니라 **중심**에서 시작한다. 표면에서 시작하면 깔때기
    # 입이 극점 위에 지름 2 R_star 짜리 원반으로 떠서 테두리가 링으로 보인다.
    # 중심에서 시작하면 넓은 구간이 항성 안에 묻히고, 표면 위로 나오는 부분만
    # 깔때기로 읽힌다.
    phi = math.radians(funnel_tangent_deg)
    s_t, r_t = R_star_m * math.cos(phi), R_star_m * math.sin(phi)
    rate = math.cos(phi) / (R_star_m * math.sin(phi) ** 2)

    P0 = (0.0, 0.0)
    # 도착점은 표면이 아니라 목표 중심 — 빔이 원반 전체를 덮는다는 서술과
    # 맞으려면 관의 축이 중심까지 가야 하고, 그래야 끝 반경 R_target 이 정확히
    # 원반을 채운다.
    P2 = (a_m, 0.0)
    P1y = _solve_control(P0, P2, H_best)


    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * P0[0] + 2 * t * (1 - t) * 0.0 + t * t * P2[0]
        y = (1 - t) ** 2 * P0[1] + 2 * t * (1 - t) * P1y + t * t * P2[1]
        pts.append((x, y))

    total = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    path, run = [], 0.0
    for i, (x, y) in enumerate(pts):
        if i:
            run += math.dist(pts[i - 1], pts[i])
        f = run / total

        # 도착부: 목표 지름을 덮을 때까지 벌어진다.
        w = f * f * (3 - 2 * f)
        beam = start_radius_m + (R_target_m - start_radius_m) * w

        # 출발부: 항성 표면에 **접하는** 깔때기.
        #
        # 앞선 시도들은 전부 이음매가 안 매끄러웠다. 관을 별 안에 넣어 극에서만
        # 내보내면 그 지점에서 벽이 표면과 90 도로 만나고, 넓게 내보내면 옆구리를
        # 뚫고 나와 칼라가 생긴다. 어느 쪽이든 접선이 안 맞는다.
        #
        # 깔때기: 항성 표면에 접하는 지수. 호길이로 재므로 경로가 휘면 같이 휜다.
        # 별 근처에서는 경로가 사실상 수직이라 s ~= y 이고, 접선 조건이 그대로
        # 성립한다. 접점 아래(s < s_t)는 별 자신이 채우므로 그리지 않는다.
        if run >= s_t:
            funnel = r_t * math.exp(-(run - s_t) * rate)
        else:
            funnel = 0.0

        path.append(((x, y, 0.0), combine_radius(funnel, beam), funnel, beam))
    return path, H_best


def combine_radius(funnel, beam, n=4.0):
    """Soft maximum of the two mouths — a plain max would crease at the join."""
    return (funnel ** n + beam ** n) ** (1.0 / n)


def describe(R_star_m, a_m, R_target_m, v_orbit_m_s, gap_deg=None,
             speed_frac_c=1.0, start_radius_m=None):
    """Every number the shape and the aiming need, from physical inputs."""
    H_lo, H_hi, H_best, g_best = gap_band(R_star_m, a_m)
    P1y = _solve_control((0.0, 0.0), (a_m, 0.0), H_best)
    apex_y, apex_t = _bezier_apex((0.0, 0.0), P1y, (a_m, 0.0))
    H = H_best if gap_deg is None else glare_clearance_height(R_star_m, a_m, gap_deg)
    lead, transit = aim_lead_m(a_m, v_orbit_m_s, speed_frac_c)
    run = math.hypot(a_m, H)
    return {
        'gap_deg': limb_gap_deg(H, R_star_m, a_m),
        'best_gap_deg': g_best,
        'best_height_in_R_star': H_best / R_star_m,
        'band_lo_in_R_star': H_lo / R_star_m,
        'band_hi_in_R_star': H_hi / R_star_m,
        'arc_radius_in_R_star': (H_hi - H_lo) / R_star_m,
        'control_in_R_star': P1y / R_star_m,
        'apex_in_R_star': apex_y / R_star_m,
        'apex_at_fraction': apex_t,
        'geometric_mean_in_R_star': math.sqrt(R_star_m * a_m) / R_star_m,
        'grazing_height_in_R_star': limb_grazing_height(R_star_m, a_m) / R_star_m,
        'climb_height_m': H,
        'climb_above_surface_m': H - R_star_m,
        'climb_in_R_star': H / R_star_m,
        'knee_angle_deg': math.degrees(math.atan2(a_m, H)),
        'run_m': run,
        'transit_s': transit,
        'aim_lead_m': lead,
        'aim_lead_target_diameters': lead / (2 * R_target_m),
        'aim_lead_deg': math.degrees(lead / a_m),
        'start_radius_m': (0.25 * R_target_m if start_radius_m is None
                           else start_radius_m),
        'end_radius_m': R_target_m,
        'opening_half_angle_deg': math.degrees(math.atan(R_target_m / run)),
    }
