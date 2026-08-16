#!/usr/bin/env python3
# 알펜 날개 경계면의 3D 형상을 스피어 트레이싱으로 렌더 — 기하는 magnetopause_geometry.py 도출값 그대로
"""Sphere-trace the Alfven-wing boundary in 3D.

The 2D slice renders in `render_belts.py` cut the x-y (meridional) plane, which
is exactly the plane an Alfven wing does *not* live in: the wings lean out of
the flow direction z. So this tool ray-marches the real signed distance field
instead of slicing it, and prints four views:

    parent-view (down +x)  — the B-v plane, where the wings are widest apart
    flow-view (down +z)    — what the plasma runs into
    field-view (down +y)   — down the wing axis pair
    three-quarter          — the shape as an object

The SDF is `magnetopause_geometry.alfven_wing_sdf`, re-implemented here over
numpy arrays for speed; `--selftest` asserts the two agree to 1e-9.

    python3 scripts/viz/render_alfven_wing.py --body ganymede -o out.png
"""

import argparse
import math
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'refs'))
import magnetopause_geometry as mg  # noqa: E402
from render_outputs import save_versioned  # noqa: E402


# 물리 입력만 적는다 — 형상 수치(기울기·관 반경·직선 길이)는 전부 여기서 도출된다.
PARENTS = {
    'jupiter': dict(parent_mass_kg=1.898e27, parent_radius_m=71_492e3,
                    parent_spin_s=9.925 * 3600, parent_B_eq_uT=428.0),
    # 보드값: Polyphemus 120 M⊕, R_J, 자전 10.35 h, B_eq 170 uT
    'polyphemus': dict(parent_mass_kg=120 * mg.M_EARTH, parent_radius_m=mg.R_JUP,
                       parent_spin_s=10.35 * 3600, parent_B_eq_uT=170.0),
}

BODIES = {
    'ganymede': dict(
        title='Ganymede', sub='Jovian plasma, L 15 R_J', parent='jupiter',
        L_shell=15.0, moon_radius_m=2634e3, moon_B_eq_uT=0.719,
        plasma_cm3=4.0, ion_amu=14.0),
    'pandora': dict(
        title='Pandora (A b III)', sub='Polyphemus plasma, L 3.53 R_p',
        parent='polyphemus', L_shell=3.53, moon_radius_m=5724e3,
        moon_B_eq_uT=75.0),
    'dante': dict(
        title='Dante (A b I)', sub='unmagnetized, Io-like ionospheric obstacle',
        parent='polyphemus', L_shell=1.54, moon_radius_m=1821e3,
        moon_B_eq_uT=0.0, ionosphere_radii=1.1),
}


def geometry_for(name):
    spec = dict(BODIES[name])
    spec.update(PARENTS[spec.pop('parent')])
    title, sub = spec.pop('title'), spec.pop('sub')
    g = mg.derive_wing_geometry(**spec)
    g['title'], g['sub'] = title, sub

    rho = (spec.get('plasma_cm3', mg.IO_TORUS_PEAK_CM3 * 0.02) * 1e6
           * spec.get('ion_amu', mg.IO_TORUS_ION_AMU) * mg.AMU)
    g['paths'] = [
        mg.dipole_wing_path(spec['L_shell'], spec['parent_radius_m'],
                            spec['moon_radius_m'], g['M_A'],
                            spec['parent_mass_kg'], spec['parent_spin_s'],
                            spec['parent_B_eq_uT'], rho, g['R_tube'],
                            hemisphere=h, flow_sign=g['flow_sign'], steps=520,
                            min_radius=g['landing_floor'])
        for h in (1.0, -1.0)]
    g['parent_radius'] = spec['parent_radius_m'] / spec['moon_radius_m']
    g['parent_centre'] = np.array(
        [spec['L_shell'] * spec['parent_radius_m'] / spec['moon_radius_m'], 0.0, 0.0])
    g['straightness'] = straightness_profile(g['paths'][0], g['R_tube'])
    pr = wing_profile(g)
    # 바닥값이 물리기 직전 구간에서 테이퍼 각을 잰다 — 바닥에 걸린 뒤로는 원통이라 0이다.
    free = np.nonzero(pr['R_abs'] > g['landing_floor'] * 1.001)[0]
    j = free[-1] if len(free) > 2 else len(pr['R_abs']) - 1
    i = max(0, j - 5)
    ds = pr['s'][j] - pr['s'][i]
    g['contact_half_angle_deg'] = math.degrees(math.atan(
        -(pr['R_abs'][j] - pr['R_abs'][i]) / ds)) if ds > 0 else 0.0
    g['floor_starts_at'] = float(pr['f'][j]) if len(free) else 1.0
    g['floor_binds'] = bool(len(free) and free[-1] < len(pr['R_abs']) - 2)
    return g


def straightness_profile(path, R_tube):
    """Where the wing stops being straight, measured on the real curved path.

    Departure of the path from its own initial tangent, against arc length.
    Reported at the thresholds that matter: one tube radius (the analytic
    estimate sqrt(2 R_tube R_curv) targets this), and a quarter / half turn.
    """
    pts = np.array([p for p, _ in path])
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    tang = pts[1] - pts[0]
    tang = tang / np.linalg.norm(tang)
    dev = np.linalg.norm(pts - s[:, None] * tang, axis=1)

    def crossing(level):
        hit = np.nonzero(dev > level)[0]
        return float(s[hit[0]]) if len(hit) else float('nan')

    return {'s': s, 'dev': dev, 'total': float(s[-1]),
            'one_radius': crossing(R_tube),
            'quarter': crossing(0.25 * s[-1]),
            'ten_pct': crossing(0.10 * s[-1])}


def downsample_path(path, samples, radius_tol=0.03, angle_tol=0.035):
    """Thin a path for rendering, keeping detail where the shape actually moves.

    Two failures this avoids, both learned the hard way. `path[::step]` drops
    the endpoint whenever the length is not a multiple of the step, which cost
    the Petrova beam its last 112 target radii — invisible in the numbers,
    glaring in the picture. And uniform thinning spends its budget evenly along
    a path whose interesting parts are not evenly spread: the Petrova funnel
    collapses by a factor of 500 within two stellar radii, and four straight
    frusta across that stretch render as a stack of rings.

    So keep a vertex when the radius has moved by `radius_tol` or the direction
    has turned by `angle_tol` radians since the last one kept, and thin the
    quiet stretches by however much is left of the budget.
    """
    if len(path) <= samples:
        return list(path)
    step = max(1, len(path) // samples)
    out = [path[0]]
    ref_r = path[0][1]
    ref_dir = None
    for i in range(1, len(path) - 1):
        p, r = path[i][0], path[i][1]
        prev = out[-1][0]
        d = math.dist(p, prev) or 1e-12
        direction = tuple((p[k] - prev[k]) / d for k in range(3))
        turned = (ref_dir is not None
                  and sum(direction[k] * ref_dir[k] for k in range(3)) < math.cos(angle_tol))
        moved = abs(r - ref_r) > radius_tol * max(r, ref_r, 1e-12)
        if turned or moved or i % step == 0:
            out.append(path[i])
            ref_r, ref_dir = r, direction
    out.append(path[-1])
    return out


def path_sdf_np(P, pts, rads, chunk=24000):
    """Swept-sphere polyline distance, vectorized over both points and segments.

    Twin of mg.wing_path_sdf. Chunked over points so the (N, S) intermediates
    stay bounded no matter how long the path is.
    """
    a, b = pts[:-1], pts[1:]
    ra, rb = rads[:-1], rads[1:]
    ab = b - a
    den = np.maximum((ab * ab).sum(-1), 1e-12)
    flat = P.reshape(-1, 3)
    out = np.empty(len(flat), dtype=P.dtype)
    for i in range(0, len(flat), chunk):
        q = flat[i:i + chunk][:, None, :]                    # (n,1,3)
        ap = q - a[None]                                     # (n,S,3)
        t = np.clip((ap * ab[None]).sum(-1) / den[None], 0.0, 1.0)
        perp = ap - t[..., None] * ab[None]
        seg = np.sqrt((perp * perp).sum(-1)) - (ra[None] + (rb - ra)[None] * t)
        out[i:i + chunk] = seg.min(axis=1)
    return out.reshape(P.shape[:-1])


def wing_sdf_np(P, R_obst, R_wing, M_A, length, flow_sign, field_sign, blend):
    """Vectorized twin of mg.alfven_wing_sdf. P is (..., 3) in body radii."""
    wp, wm = mg.alfven_wing_axes(M_A, flow_sign, field_sign)
    d = np.linalg.norm(P, axis=-1) - R_obst
    for axis in (wp, wm):
        a = np.asarray(axis)
        t = np.clip(P @ a, 0.0, length)
        cap = np.linalg.norm(P - t[..., None] * a, axis=-1) - R_wing
        if blend > 0:
            h = np.clip(0.5 + 0.5 * (cap - d) / blend, 0.0, 1.0)
            d = cap * (1 - h) + d * h - blend * h * (1 - h)
        else:
            d = np.minimum(d, cap)
    return d


def _selftest():
    rng = np.random.default_rng(7)
    args = dict(R_obst=2.0, R_wing=2.0, M_A=0.48, length=23.3,
                flow_sign=1.0, field_sign=-1.0, blend=1.0)
    P = rng.uniform(-40, 40, size=(400, 3))
    fast = wing_sdf_np(P, **args)
    slow = np.array([mg.alfven_wing_sdf(tuple(p), **args) for p in P])
    err = np.abs(fast - slow).max()
    assert err < 1e-9, f'numpy SDF disagrees with the scalar one by {err}'
    print(f'selftest ok — max |numpy - scalar| = {err:.2e} over 400 points')


def _camera(view, span, size):
    """Orthographic basis (right, up, forward) plus the ray origin grid."""
    bases = {
        'parent': ((0, 0, 1), (0, 1, 0), (-1, 0, 0)),   # looking down +x
        'flow':   ((1, 0, 0), (0, 1, 0), (0, 0, -1)),   # looking down +z
        'field':  ((0, 0, 1), (1, 0, 0), (0, -1, 0)),   # looking down +y
    }
    if view == 'threequarter':
        f = np.array([-0.55, -0.42, -0.72])
        f /= np.linalg.norm(f)
        r = np.cross(np.array([0.0, 1.0, 0.0]), -f)
        r /= np.linalg.norm(r)
        u = np.cross(-f, r)
    else:
        r, u, f = (np.array(v, dtype=float) for v in bases[view])
    j, i = np.meshgrid(np.arange(size), np.arange(size), indexing='xy')
    sx = (j / (size - 1) - 0.5) * 2 * span
    sy = (0.5 - i / (size - 1)) * 2 * span
    origin = sx[..., None] * r + sy[..., None] * u - f * (span * 4)
    return origin, np.broadcast_to(f, origin.shape).copy(), r, u


def _march(origin, direction, sdf, steps=130, far=None, tol=1e-3):
    """Sphere-tracing, evaluating the field only on rays still in flight.

    Masking matters here: the full-run views are mostly background, and marching
    dead rays through a 70-segment polyline field is what made this unusably
    slow before.
    """
    shape = origin.shape[:2]
    t = np.zeros(shape)
    hit = np.zeros(shape, dtype=bool)
    live = np.ones(shape, dtype=bool)
    far = far if far is not None else origin.shape[0]
    for _ in range(steps):
        idx = np.nonzero(live)
        if not len(idx[0]):
            break
        P = origin[idx] + t[idx][:, None] * direction[idx]
        d = sdf(P)
        struck = d < tol
        hit[idx[0][struck], idx[1][struck]] = True
        step = np.maximum(d * 0.9, tol)
        t[idx] = t[idx] + np.where(struck, 0.0, step)
        live[idx] = (~struck) & (t[idx] < far)
    return t, hit


def _normal(P, sdf, h=2e-3):
    """Central-difference gradient. P is a flat (N,3) list of surface hits."""
    o = np.zeros_like(P)
    g = []
    for ax in range(3):
        e = o.copy()
        e[..., ax] = h
        g.append(sdf(P + e) - sdf(P - e))
    n = np.stack(g, axis=-1)
    return n / np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-9)


def wing_profile(spec):
    """Thickness and lead angle against fraction of the run — the two things the
    3D views cannot show, because both vary by orders of magnitude."""
    path = spec['paths'][0]
    P = np.array([p for p, _ in path])
    R = np.array([r for _, r in path])
    s = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    # 위성 gsm 좌표에서 모천체 방위각을 되돌린다.
    Xp = spec['parent_centre'][0] - P[:, 0]
    Zp = P[:, 2] * spec['flow_sign']
    phi = np.degrees(np.arctan2(Zp, Xp))
    return {'f': s / s[-1], 's': s, 'R': R / R[0], 'phi': phi,
            'R_abs': R, 'lag': P[:, 2]}


def render_profile(names, out, size=(880, 470)):
    from PIL import ImageDraw, ImageFont
    W, H = size
    img = Image.new('RGB', (W, H), (8, 9, 14))
    dr = ImageDraw.Draw(img)
    try:
        fnt = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 11)
        fbig = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 14)
    except OSError:                                   # pragma: no cover
        fnt = fbig = ImageFont.load_default()
    colours = [(122, 168, 255), (255, 154, 82), (126, 214, 160)]

    specs = [(n, geometry_for(n)) for n in names]
    profs = [(n, g, wing_profile(g)) for n, g in specs]
    phimax = max(max(abs(p['phi'])) for _, _, p in profs) or 1.0

    panels = [('tube diameter / diameter at the moon', 'R', 1.0),
              ('lead angle from the moon meridian (deg)', 'phi', phimax)]
    pw, ph = (W - 90) // 2, H - 150
    for k, (title, key, top) in enumerate(panels):
        ox, oy = 52 + k * (pw + 38), 106
        dr.rectangle([ox, oy, ox + pw, oy + ph], outline=(46, 54, 72))
        dr.text((ox, oy - 18), title, fill=(196, 210, 232), font=fnt)
        for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
            y = oy + ph - frac * ph
            dr.line([ox, y, ox + pw, y], fill=(26, 31, 43))
            dr.text((ox - 46, y - 6), f'{frac * top:6.2f}', fill=(112, 126, 148), font=fnt)
            x = ox + frac * pw
            dr.line([x, oy, x, oy + ph], fill=(26, 31, 43))
            dr.text((x - 10, oy + ph + 5), f'{frac:.2f}', fill=(112, 126, 148), font=fnt)
        dr.text((ox + pw // 2 - 60, oy + ph + 20),
                'fraction of the run to the parent', fill=(140, 158, 186), font=fnt)
        for i, (_, g, p) in enumerate(profs):
            pts = [(ox + f * pw, oy + ph - min(v / top, 1.0) * ph)
                   for f, v in zip(p['f'], p[key])]
            dr.line(pts, fill=colours[i % len(colours)], width=2)

    dr.text((14, 10), 'Alfven wing — how the tube changes along its run',
            fill=(232, 238, 248), font=fbig)
    for i, (_, g, p) in enumerate(profs):
        dr.text((14, 30 + i * 15),
                f"{g['title']:22s} tilt {g['theta_A_deg']:4.1f} deg   "
                f"lands at {p['R'][-1] * 100:5.1f}% of its starting diameter   "
                f"lead {p['phi'][-1]:5.2f} deg",
                fill=colours[i % len(colours)], font=fnt)
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    img.save(out)
    save_versioned(img, 'alfven-profile')
    return out


def _project(world, centre, right, up, span, size):
    """World point → panel pixel, for drawing annotations over a rendered view."""
    d = np.asarray(world, dtype=float) - centre
    return (size / 2 + (d @ right) / span * size / 2,
            size / 2 - (d @ up) / span * size / 2)


def render_anatomy(name, out, size=380, fatten=None, fillet_scale=None):
    """One sheet answering the three shape questions, each in its own panel."""
    from PIL import ImageDraw, ImageFont
    spec = geometry_for(name)
    st = spec['straightness']
    prof = wing_profile(spec)
    fs = mg.FILLET_SCALE_DEFAULT if fillet_scale is None else fillet_scale
    fillet_km = fs * spec['scale_height_m'] / 1e3

    near = 2.35 * st['one_radius']
    nc = np.array([near * 0.22, 0.0, 0.0])
    far = 0.60 * float(spec['parent_centre'][0]) + spec['parent_radius']
    mid = np.array([far * 0.66, 0.0, 0.0])
    # 굵기 배율은 천체마다 다르게 잡는다 — 고정 x8 은 이미 모천체의 27% 를 차지하는
    # 판도라의 관을 행성보다 굵게 그려서, 비율을 물어보게 만든다.
    fat = fatten if fatten is not None else max(
        1.0, min(8.0, 0.45 * spec['parent_radius'] / spec['R_tube']))

    panels = [
        ('parent', near, nc, 1.0,
         f"1. tilt — theta_A = arctan M_A = {spec['theta_A_deg']:.1f} deg",
         'the B-v plane, seen down the parent direction'),
        ('flow', far, mid, fat,
         '2. thickness — a horn in the middle of the run',
         f'full run; tube drawn x{fat:.1f}, so the taper is relative'),
        ('field', far, mid, fat,
         f"3. lead — {prof['phi'][-1]:+.1f} deg of azimuth",
         'from over the parent pole; flow to the right'),
        ('flow', max(4.5 * (prof['R_abs'][-1] + fs * spec['landing_floor']), 1e-3),
         np.array(spec['paths'][0][-1][0]), 1.0,
         f"4. contact — lands {prof['R_abs'][-1]:.3g} R wide, true scale",
         (f"floor {spec['scale_height_m'] / 1e3:.0f} km (1 H) from "
          f"f={spec['floor_starts_at']:.2f}; fillet {fs:g} H = {fillet_km:.0f} km"
          if spec['floor_binds'] else
          f"flux-limited to the surface, half-angle "
          f"{spec['contact_half_angle_deg']:.2f} deg; fillet {fs:g} H "
          f"= {fillet_km:.0f} km")),
    ]

    pad, head = 12, 84
    W = size * 4 + pad * 5
    H = size + head + pad * 2 + 268
    sheet = Image.new('RGB', (W, H), (8, 9, 14))
    dr = ImageDraw.Draw(sheet)
    try:
        fnt = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 11)
        fmid = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 13)
        fbig = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 16)
    except OSError:                                   # pragma: no cover
        fnt = fmid = fbig = ImageFont.load_default()

    dr.text((pad, 10), f"{spec['title']} — Alfven wing anatomy",
            fill=(232, 238, 248), font=fbig)
    dr.text((pad, 32),
            f"M_A {spec['M_A']:.2f}   obstacle {spec['R_obst']:.2f} R   "
            f"straight for {st['one_radius']:.0f} R of a {st['total']:.0f} R run   "
            f"lands at {prof['R'][-1] * 100:.1f}% diameter, {prof['phi'][-1]:+.1f} deg of lead   "
            f"|  blue = straight, orange = bent, grey = parent",
            fill=(140, 158, 186), font=fnt)

    for idx, (view, span, ctr, fat, title, sub) in enumerate(panels):
        img, right, up = render_view(spec, view, span, size, full=True,
                                     centre=ctr, fatten=fat,
                                     fillet_scale=fillet_scale)
        tile = Image.fromarray((img * 255).astype(np.uint8))
        x, y = pad + idx * (size + pad), head + pad
        sheet.paste(tile, (x, y))
        dr.text((x, y - 34), title, fill=(226, 234, 248), font=fmid)
        dr.text((x, y - 17), sub, fill=(130, 148, 176), font=fnt)

        od = ImageDraw.Draw(sheet)
        if view == 'parent':                       # 자기장 축과 끼인각을 겹쳐 그린다
            for s in (1, -1):
                a = _project((0, 0, 0), ctr, right, up, span, size)
                b = _project((0, s * span * 0.9, 0), ctr, right, up, span, size)
                for k in range(0, 30, 2):          # 점선
                    t0, t1 = k / 30, (k + 1) / 30
                    od.line([x + a[0] + (b[0] - a[0]) * t0, y + a[1] + (b[1] - a[1]) * t0,
                             x + a[0] + (b[0] - a[0]) * t1, y + a[1] + (b[1] - a[1]) * t1],
                            fill=(96, 108, 132), width=1)
            lab = _project((0, span * 0.62, 0), ctr, right, up, span, size)
            od.text((x + lab[0] + 6, y + lab[1]), 'B (field axis)',
                    fill=(120, 134, 160), font=fnt)
            ar = _project((0, -span * 0.55, spec['flow_sign'] * span * 0.30),
                          ctr, right, up, span, size)
            od.text((x + ar[0], y + ar[1]), '→ flow', fill=(150, 168, 200), font=fnt)
        if view == 'field':
            pc = _project(spec['parent_centre'], ctr, right, up, span, size)
            od.text((x + pc[0] - 22, y + pc[1] - 30), 'parent',
                    fill=(160, 168, 184), font=fnt)
            mo = _project((0, 0, 0), ctr, right, up, span, size)
            od.text((x + mo[0] - 10, y + mo[1] + 12), 'moon',
                    fill=(160, 168, 184), font=fnt)

    chart = render_profile([name], out + '.tmp.png', size=(W - pad * 2, 250))
    sheet.paste(Image.open(chart), (pad, head + pad + size + 14))
    os.remove(chart)
    os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
    sheet.save(out)
    save_versioned(sheet, f'alfven-anatomy-{name}')
    return out


def path_arclength_np(P, paths):
    """Arc length of the nearest sample over *both* wings — the tint has to be
    per-wing, or the southern wing gets coloured by the northern one's run."""
    flat = P.reshape(-1, 3)
    best_d = np.full(len(flat), np.inf)
    best_s = np.zeros(len(flat))
    for path in paths:
        pts = np.array([q for q, _ in path])
        acc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
        for i in range(0, len(flat), 24000):
            q = flat[i:i + 24000][:, None, :]
            d2 = ((q - pts[None]) ** 2).sum(-1)
            k = np.argmin(d2, axis=1)
            dmin = np.take_along_axis(d2, k[:, None], 1)[:, 0]
            sl = slice(i, i + 24000)
            closer = dmin < best_d[sl]
            best_d[sl] = np.where(closer, dmin, best_d[sl])
            best_s[sl] = np.where(closer, acc[k], best_s[sl])
    return best_s.reshape(P.shape[:-1])


def make_sdf(spec, full, fatten=1.0, fillet_scale=None):
    """Near-field uses the straight-tube approximation; `full` marches the real
    curved flux tubes all the way to the parent, parent body included."""
    blend = 0.5 * spec['R_obst']
    if not full:
        def sdf(P):
            return wing_sdf_np(P, spec['R_obst'], spec['R_tube'], spec['M_A'],
                               spec['length'], spec['flow_sign'],
                               spec['field_sign'], blend)
        return sdf

    # 렌더용 다운샘플: 520 세그먼트는 형상에 필요 없고 마칭만 몇 배 느려진다.
    arrs = []
    for path in spec['paths']:
        thin = downsample_path(path, 90)
        arrs.append((np.array([p for p, _ in thin], dtype=np.float64),
                     np.array([r * fatten for _, r in thin], dtype=np.float64)))
    pr, pc = spec['parent_radius'], spec['parent_centre']

    # 착지 필렛: 관과 모천체가 만나는 모서리를 스케일 높이만큼 부드럽게 잇는다.
    # 임의 스무딩이 아니라 관이 녹아드는 층의 두께 그 자체다.
    if fillet_scale is None:
        fillet_scale = mg.FILLET_SCALE_DEFAULT
    fillet = spec['landing_floor'] * fillet_scale * fatten

    def sdf(P):
        d = np.linalg.norm(P, axis=-1) - spec['R_obst']
        for pts, rads in arrs:
            d = np.minimum(d, path_sdf_np(P, pts, rads))
        body = np.linalg.norm(P - pc, axis=-1) - pr
        if fillet <= 0:
            return np.minimum(d, body)
        h = np.clip(0.5 + 0.5 * (body - d) / fillet, 0.0, 1.0)
        return body * (1 - h) + d * h - fillet * h * (1 - h)
    return sdf


def render_view(spec, view, span, size, full=False, centre=None, fatten=1.0,
                fillet_scale=None):
    sdf = make_sdf(spec, full, fatten, fillet_scale)
    if centre is None:
        theta = math.radians(spec['theta_A_deg'])
        centre = np.array([0.0, 0.0,
                           spec['flow_sign'] * spec['length'] * math.sin(theta) / 2])
    origin, direction, right, up = _camera(view, span, size)
    origin = origin + centre
    t, hit = _march(origin, direction, sdf, far=span * 9)

    # 셰이딩은 맞은 픽셀에만. 배경까지 법선 6회 + 최근접 경로 탐색을 돌리면
    # 고해상도에서 시간의 대부분이 빈 하늘에 쓰인다.
    img = np.tile(np.array([0.031, 0.036, 0.055]), (size, size, 1))
    idx = np.nonzero(hit)
    if not len(idx[0]):
        return img, right, up
    P = origin[idx] + t[idx][:, None] * direction[idx]
    n = _normal(P, sdf)

    # 광원은 카메라에 물린다 — 뷰마다 조명을 새로 잡으면 형상 비교가 안 된다.
    key = 0.45 * right + 0.62 * up - 0.75 * direction[0, 0]
    key /= np.linalg.norm(key)
    lam = np.clip(n @ key, 0, 1)
    rim = np.clip(1.0 - np.abs(n @ (-direction[0, 0])), 0, 1) ** 2.2

    # 직선 구간과 꺾인 구간을 색으로 가른다 — 전이점이 결론이라 캡션보다 그림이 낫다.
    ess = path_arclength_np(P, spec['paths'])
    on_parent = (np.linalg.norm(P - spec['parent_centre'], axis=-1)
                 <= spec['parent_radius'] * 1.004)
    straight = (ess <= spec['straightness']['one_radius']) & ~on_parent
    body = np.where(straight[:, None],
                    np.array([0.34, 0.52, 0.80]), np.array([0.74, 0.46, 0.30]))
    body = np.where(on_parent[:, None], np.array([0.40, 0.40, 0.44]), body)

    shade = (body * lam[:, None] ** 0.85) * 0.92
    shade = shade + np.where(straight[:, None], np.array([0.42, 0.62, 1.0]),
                             np.array([1.0, 0.66, 0.42])) * rim[:, None] * 0.55
    img[idx] = np.clip(shade + np.array([0.05, 0.07, 0.13]), 0, 1)
    return img, right, up


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--body', default='ganymede', choices=sorted(BODIES))
    ap.add_argument('-o', '--out', default='dist/_scratch/alfven-wing.png')
    ap.add_argument('--size', type=int, default=460)
    ap.add_argument('--span', type=float, default=None)
    ap.add_argument('--fatten', type=float, default=0.0,
                    help='tube radius multiplier in the full-run panels; '
                         '1 = true scale, 0 = pick one per body so the tube '
                         'never outgrows the parent')
    ap.add_argument('--fillet-scale', type=float, default=None,
                    help='landing fillet in ionospheric scale heights; the '
                         'defensible window is 1-3, default 3')
    ap.add_argument('--anatomy', action='store_true',
                    help='one sheet: tilt, thickness, lead, plus the profiles')
    ap.add_argument('--profile', action='store_true',
                    help='thickness and lead-angle profiles instead of the 3D views')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()

    if a.selftest:
        _selftest()
        return

    if a.profile:
        print(render_profile(sorted(BODIES), a.out))
        return

    if a.anatomy:
        print(render_anatomy(a.body, a.out, size=a.size,
                             fatten=a.fatten if a.fatten > 0 else None,
                             fillet_scale=a.fillet_scale))
        return

    spec = geometry_for(a.body)
    far = 0.62 * float(spec['parent_centre'][0]) + spec['parent_radius']
    mid = np.array([far * 0.62, 0.0, 0.0])
    fat = a.fatten or 8.0
    st = spec['straightness']
    near = a.span or 1.9 * st['one_radius']
    nc = np.array([near * 0.30, 0.0, 0.0])
    views = [('parent',
              f"near field, down +x — straight to {st['one_radius']:.0f} R, then bends",
              near, True, nc, 1.0),
             ('threequarter', 'near field, three-quarter', near, True, nc, 1.0),
             ('flow', f'full run to the parent, down +z  (tube x{fat:g})',
              far, True, mid, fat),
             ('threequarter', f'full run, three-quarter  (tube x{fat:g})',
              far, True, mid, fat)]

    pad, head = 12, 34
    W = max(a.size * 2 + pad * 3, 900)
    H = a.size * 2 + pad * 3 + head
    sheet = Image.new('RGB', (W, H), (8, 9, 14))
    from PIL import ImageDraw, ImageFont
    try:
        fnt = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 12)
        fbig = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 15)
    except OSError:                                   # pragma: no cover
        fnt = fbig = ImageFont.load_default()
    dr = ImageDraw.Draw(sheet)

    dr.text((pad, 8), f"{spec['title']} — Alfven wing, 3D", fill=(232, 238, 248), font=fbig)
    dr.text((pad, 24),
            f"{spec['sub']}  |  M_A {spec['M_A']:.2f}  tilt {spec['theta_A_deg']:.1f} deg"
            f"  |  R_obst {spec['R_obst']:.3g}  R_tube {spec['R_tube']:.3g}"
            f"  |  straight {spec['length']:.0f} R, bends onto the field line, "
            f"lands on the parent at {spec['straightness']['total']:.0f} R",
            fill=(140, 158, 186), font=fnt)

    for idx, (view, label, span, full, ctr, fatten) in enumerate(views):
        img, _, _ = render_view(spec, view, span, a.size, full=full,
                                centre=ctr, fatten=fatten)
        tile = Image.fromarray((img * 255).astype(np.uint8))
        x = pad + (idx % 2) * (a.size + pad)
        y = head + pad + (idx // 2) * (a.size + pad)
        sheet.paste(tile, (x, y))
        dr.text((x + 8, y + 6), label, fill=(196, 210, 232), font=fnt)

    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    sheet.save(a.out)
    save_versioned(sheet, f'alfven-wing-{a.body}')
    print(a.out)


if __name__ == '__main__':
    main()
