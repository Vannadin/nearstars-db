#!/usr/bin/env python3
# 페트로바선 3D 형상 렌더 — 기하는 petrova_line_geometry.py 도출값, 튜브 렌더는 알펜 윙과 공유
"""Sphere-trace the Petrova line.

Shares the tube machinery with `render_alfven_wing` — the swept-sphere
polyline field, the camera, the marcher — and swaps the two things that are
actually different: the path law (one continuous curve leaving along the spin
axis and peaking at the maximum-clearance height) and the radius law (a beam
opening to the target's diameter).
That split is the whole point: one renderer, many line physics.

    python3 scripts/viz/render_petrova_line.py -o out.png

The beam is a thread next to a star — 0.002 stellar radii at the pole — so any
panel that contains the star has to draw it thickened, and the factor is in
the caption. The two true-scale panels are the ones that do not contain it.
"""

import argparse
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'refs'))
import petrova_line_geometry as pg                      # noqa: E402
from render_alfven_wing import (downsample_path, _camera,  # noqa: E402
                                _march, _normal)


# 물리 입력만. 형상은 전부 petrova_line_geometry 가 도출한다.
SYSTEMS = {
    'sol-venus': dict(
        title='Sol → Venus', R_star_m=6.957e8, a_m=1.0821e11,
        R_target_m=6.0518e6, v_orbit_m_s=35.02e3, target='Venus'),
}


def sweep_profile_sdf_np(P, pts, rads, chunk=16000):
    """Distance to a radius profile swept along a curve — not a swept sphere.

    Swept spheres were the whole trouble. Where the radius changes faster than
    the curve advances, each sphere swallows the next and the surface becomes
    the hull of a few big balls instead of the profile that was written down;
    the funnel drops from 0.87 to 0.06 stellar radii over one stellar radius,
    so it was never going to survive that. Here the *nearest point on the
    curve* is found first, purely geometrically, and only then is the radius
    read off at that arc length. The surface is then exactly rho = r(s),
    whatever the taper does.
    """
    a, b = pts[:-1], pts[1:]
    ab = b - a
    seg = np.sqrt((ab * ab).sum(-1))
    den = np.maximum((ab * ab).sum(-1), 1e-30)
    s0 = np.concatenate([[0.0], np.cumsum(seg)])
    s_at = np.concatenate([[0.0], np.cumsum(seg)])

    flat = P.reshape(-1, 3)
    out = np.empty(len(flat))
    for i in range(0, len(flat), chunk):
        q = flat[i:i + chunk][:, None, :]
        ap = q - a[None]
        t = np.clip((ap * ab[None]).sum(-1) / den[None], 0.0, 1.0)
        perp = ap - t[..., None] * ab[None]
        dist = np.sqrt((perp * perp).sum(-1))
        k = np.argmin(dist, axis=1)
        rows = np.arange(len(k))
        rho = dist[rows, k]
        s = s0[k] + t[rows, k] * seg[k]
        out[i:i + chunk] = rho - np.interp(s, s_at, rads)
    return out.reshape(P.shape[:-1])


def build(name, gap_deg, start_frac, tangent_deg=60.0):
    s = dict(SYSTEMS[name])
    start_radius = start_frac * s['R_target_m']
    path, H = pg.petrova_path(s['R_star_m'], s['a_m'], s['R_target_m'],
                              gap_deg=gap_deg, start_radius_m=start_radius,
                              funnel_tangent_deg=tangent_deg)
    d = pg.describe(s['R_star_m'], s['a_m'], s['R_target_m'], s['v_orbit_m_s'],
                    gap_deg=gap_deg, start_radius_m=start_radius)
    # 렌더 단위 = 항성 반경. 별·행성·빔이 한 좌표계에 들어와야 한다.
    u = s['R_star_m']
    d.update(s)
    d['unit_m'] = u
    d['path'] = [(tuple(c / u for c in p), r / u, fn / u, bm / u)
                 for p, r, fn, bm in path]
    d['star_radius'] = 1.0
    d['target_centre'] = np.array([s['a_m'] / u, 0.0, 0.0])
    d['target_radius'] = s['R_target_m'] / u
    d['tangent_deg'] = tangent_deg
    return d


def beam_radii(thin, fatten):
    """Thicken the thread, leave the star-sized funnel alone."""
    return np.array([pg.combine_radius(fn, bm * fatten) for _, _, fn, bm in thin])


def make_sdf(spec, fatten=1.0, samples=240, joint_fillet=0.0):
    thin = downsample_path(spec['path'], samples)
    pts = np.array([p for p, _, _, _ in thin])
    rads = beam_radii(thin, fatten)
    tc, tr = spec['target_centre'], spec['target_radius']

    # 항성과 깔때기 이음매를 필렛한다. 구면은 극에서 수평으로 끝나는데 유한한
    # 굵기의 관이 거기서 솟으므로, 단순 합집합이면 반드시 모서리가 남는다.
    fillet = spec['star_radius'] * joint_fillet

    def sdf(P):
        star = np.linalg.norm(P, axis=-1) - spec['star_radius']
        tube = sweep_profile_sdf_np(P, pts, rads)
        if fillet > 0:
            h = np.clip(0.5 + 0.5 * (star - tube) / fillet, 0.0, 1.0)
            d = star * (1 - h) + tube * h - fillet * h * (1 - h)
        else:
            d = np.minimum(star, tube)
        return np.minimum(d, np.linalg.norm(P - tc, axis=-1) - tr)
    return sdf


def _classify(P, spec, fatten, samples=240):
    """Which primitive owns each surface point — nearest wins.

    Testing "within the target's radius" instead fails exactly where it
    matters: the beam's end cap wraps the target, so every beam pixel there
    sits at the target's radius and gets painted as target.
    """
    thin = downsample_path(spec['path'], samples)
    pts = np.array([p for p, _, _, _ in thin])
    rads = beam_radii(thin, fatten)
    d_star = np.linalg.norm(P, axis=-1) - spec['star_radius']
    d_targ = np.linalg.norm(P - spec['target_centre'], axis=-1) - spec['target_radius']
    d_beam = sweep_profile_sdf_np(P, pts, rads)
    # 도착점이 목표 중심이라 관의 끝 캡과 목표 구면이 정확히 겹친다. 동률은
    # 목표에 준다 — 그래야 원반이 보이고, 그 원반을 정확히 채우는 관이 읽힌다.
    # 두 면이 정확히 겹치므로 부동소수 잡음만으로 픽셀이 갈려 줄무늬가 생긴다.
    # 목표 반경의 1e-3 만큼 여유를 주어 동률을 목표 쪽으로 확실히 넘긴다.
    eps = spec['target_radius'] * 1e-3
    star = (d_star <= d_beam + eps) & (d_star <= d_targ)
    targ = (d_targ <= d_beam + eps) & (d_targ < d_star)
    return ~(star | targ), star, targ


def render_view(spec, view, span, size, centre, fatten=1.0, steps=260,
                joint_fillet=0.0):
    sdf = make_sdf(spec, fatten, joint_fillet=joint_fillet)
    origin, direction, right, up = _camera(view, span, size)
    origin = origin + np.asarray(centre, dtype=float)
    # 빔이 화면에서 몇 픽셀밖에 안 되므로 마칭 허용오차를 픽셀 크기에 맞춘다 —
    # 기본값으로 두면 광선이 관을 통과해 버려 선이 점선으로 끊긴다.
    t, hit = _march(origin, direction, sdf, steps=steps, far=span * 9,
                    tol=span / size * 0.35)

    img = np.tile(np.array([0.026, 0.028, 0.042]), (size, size, 1))
    idx = np.nonzero(hit)
    if not len(idx[0]):
        return img, right, up
    P = origin[idx] + t[idx][:, None] * direction[idx]
    n = _normal(P, sdf)

    key = 0.45 * right + 0.62 * up - 0.75 * direction[0, 0]
    key /= np.linalg.norm(key)
    lam = np.clip(n @ key, 0, 1)
    rim = np.clip(1.0 - np.abs(n @ (-direction[0, 0])), 0, 1) ** 2.0

    beam, star, targ = _classify(P, spec, fatten)
    body = np.where(beam[:, None], np.array([0.94, 0.36, 0.22]),
                    np.array([0.42, 0.44, 0.50]))
    body = np.where(star[:, None], np.array([1.0, 0.86, 0.55]), body)

    shade = body * (0.30 + 0.78 * lam[:, None] ** 0.8)
    shade = shade + np.where(beam[:, None], np.array([1.0, 0.62, 0.34]),
                             np.array([0.5, 0.6, 0.8])) * rim[:, None] * 0.5
    img[idx] = np.clip(shade, 0, 1)
    return img, right, up


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--system', default='sol-venus', choices=sorted(SYSTEMS))
    ap.add_argument('-o', '--out', default='dist/_scratch/petrova-line.png')
    ap.add_argument('--size', type=int, default=440)
    ap.add_argument('--gap-deg', type=float, default=None,
                    help='force a limb gap instead of using the height of '
                         'maximum clearance (the derived default)')
    ap.add_argument('--gain', type=float, default=9.0,
                    help='emission gain for the aurora fill')
    ap.add_argument('--aurora', action='store_true',
                    help='emission-only volumetric fill instead of a surface')
    ap.add_argument('--tangent-deg', type=float, default=60.0,
                    help='latitude from the pole at which the funnel is '
                         'tangent to the star; sets the mouth and the flare')
    ap.add_argument('--start-frac', type=float, default=0.25,
                    help='beam radius at the pole, in target radii')
    a = ap.parse_args()

    if a.aurora:
        spec = build(a.system, a.gap_deg, a.start_frac, a.tangent_deg)
        ext = render_aurora(spec, 'flow', spec['star_radius'] * 4.6, a.size,
                            np.array([0.0, spec['star_radius'] * 2.4, 0.0]),
                            gain=a.gain)
        ins = render_aurora(spec, 'flow', spec['star_radius'] * 1.9, a.size,
                            np.array([0.35, spec['star_radius'] * 1.55, 0.0]),
                            gain=a.gain * 1.25)
        pad = 10
        sheet = Image.new('RGB', (a.size * 2 + pad * 3, a.size + pad * 2 + 34),
                          (8, 9, 14))
        from PIL import ImageDraw, ImageFont
        try:
            fnt = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 12)
        except OSError:                                   # pragma: no cover
            fnt = ImageFont.load_default()
        dr = ImageDraw.Draw(sheet)
        for i, (img, lab) in enumerate(((ext, 'the curtain off the pole, with the star'),
                                        (ins, 'closer on the funnel'))):
            x = pad + i * (a.size + pad)
            sheet.paste(Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)),
                        (x, pad + 26))
            dr.text((x, pad + 8), lab, fill=(214, 186, 186), font=fnt)
        os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
        sheet.save(a.out)
        print(a.out)
        return

    spec = build(a.system, a.gap_deg, a.start_frac, a.tangent_deg)
    tx = float(spec['target_centre'][0])
    waist = min(r for _, r, _, _ in spec['path'])

    # 별이 든 패널은 빔을 굵게 그릴 수밖에 없다 — 빔/별 = 0.002. 배율은 패널
    # 스팬 기준으로 잡아 어느 축척에서도 같은 굵기로 읽히게 한다.
    span_wide = tx * 0.60
    span_knee = spec['apex_in_R_star'] * 2.4
    fat_wide = (spec['star_radius'] * 0.55) / waist
    fat_knee = (spec['star_radius'] * 0.22) / waist
    panels = [
        ('flow', span_wide, np.array([span_wide * 0.86, spec['apex_in_R_star'] * 0.5, 0.0]),
         fat_wide, '1. the whole line',
         f'star to {spec["target"]}; beam x{fat_wide:.0f}'),
        ('flow', span_knee, np.array([span_knee * 0.62, spec['apex_in_R_star'] * 0.42, 0.0]),
         fat_knee, f'2. the apex at {spec["apex_in_R_star"]:.1f} R_star',
         f'curvature is continuous everywhere; beam x{fat_knee:.0f}'),
        ('flow', spec['star_radius'] * 3.4, np.array([0.0, spec['star_radius'] * 1.5, 0.0]),
         1.0, '3. the funnel, true scale',
         f'tangent to the star at {spec["tangent_deg"]:.0f} deg from the pole'),
        ('flow', spec['target_radius'] * 3.2,
         spec['target_centre'] - np.array([spec['target_radius'] * 1.3, 0.0, 0.0]),
         1.0, '4. arrival, true scale',
         f'axis runs to the centre, so the mouth fills the disc exactly'),
    ]

    pad, head = 12, 78
    W = a.size * 4 + pad * 5
    H = a.size + head + pad * 2
    sheet = Image.new('RGB', (W, H), (8, 9, 14))
    dr = ImageDraw.Draw(sheet)
    try:
        fnt = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 11)
        fmid = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 13)
        fbig = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', 16)
    except OSError:                                       # pragma: no cover
        fnt = fmid = fbig = ImageFont.load_default()

    dr.text((pad, 10), f"Petrova line — {spec['title']}", fill=(240, 232, 226), font=fbig)
    dr.text((pad, 32),
            f"one continuous curve, {spec['run_m'] / 1.496e11:.3f} AU: leaves along the spin axis, "
            f"peaks at {spec['apex_in_R_star']:.1f} R_star = sqrt(R_star a) where the target stands "
            f"furthest from the limb ({spec['best_gap_deg']:.0f} deg of dark sky), arrives on its bearing. "
            f"No free coefficient — the control height {spec['control_in_R_star']:.1f} R_star is solved to put "
            f"the apex there",
            fill=(186, 166, 158), font=fnt)
    dr.text((pad, 48),
            f"wide at both ends: a funnel tangent to the star at "
            f"{spec['tangent_deg']:.0f} deg from the pole (a cfg field), a "
            f"{spec['start_radius_m'] / 1e3:,.0f} km waist, then open again to "
            f"{spec['end_radius_m'] / 1e3:,.0f} km = the target's disc   |   "
            f"transit {spec['transit_s'] / 60:.1f} min at c, so the aim leads the *apparent* "
            f"{spec['target']} by {spec['aim_lead_target_diameters']:.2f} diameters "
            f"({spec['aim_lead_deg'] * 3600:.0f} arcsec) — aiming only, the line stays straight",
            fill=(150, 140, 158), font=fnt)

    for i, (view, span, ctr, fat, title, sub) in enumerate(panels):
        img, _, _ = render_view(spec, view, span, a.size, ctr, fat)
        sheet.paste(Image.fromarray((img * 255).astype(np.uint8)),
                    (pad + i * (a.size + pad), head + pad))
        x, y = pad + i * (a.size + pad), head + pad
        dr.text((x, y - 32), title, fill=(238, 226, 220), font=fmid)
        dr.text((x, y - 15), sub, fill=(150, 134, 128), font=fnt)

    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    sheet.save(a.out)
    print(a.out)




# ---------------------------------------------------------------- aurora fill
#
# 참조 이미지(영화 스틸)의 룩: 겹겹의 반투명 커튼, 모서리로 볼 때 밝아지는 필라멘트,
# 심홍 바탕에 흰 코어, 얇은 데로는 별이 비친다. 불투명 표면 트레이서로는 원리적으로
# 안 나오므로 방출 적분(emission-only volumetric)으로 따로 그린다.
CRIMSON = np.array([0.627, 0.106, 0.157])      # 참조 이미지 p50
MID = np.array([0.867, 0.290, 0.373])          # p80
# 참조 이미지의 흰 코어(p99.9, #fefefc)는 램프에서 뺐다 — 오너 지시로 피크가
# 흰색까지 가지 않고 MID 에서 포화한다.


def _axis_frames(pts):
    """Tangent and in-plane normal per vertex. The line lies in x-y, so the
    out-of-plane axis is z everywhere and the frame never twists."""
    t = np.gradient(pts, axis=0)
    t /= np.maximum(np.linalg.norm(t, axis=-1, keepdims=True), 1e-30)
    u = np.zeros_like(t)
    u[:, 2] = 1.0
    v = np.cross(t, u)
    v /= np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-30)
    return t, u, v


def _hash01(n, k):
    """Cheap deterministic hash in [0,1). Sine-based on purpose — a shader can
    evaluate the same thing per step, and a texture cannot travel with a
    formula."""
    return (math.sin(n * 127.1 + k * 311.7) * 43758.5453) % 1.0


def sheet_params(j):
    """Everything that makes one curtain unlike its neighbours.

    Evenly spaced sheets with a phase that ramps linearly in j read as a comb:
    the eye finds the period immediately. So azimuth, radius, fold frequencies,
    fold amplitudes, width and brightness are each jittered from a hash of j,
    and the fold frequencies are deliberately incommensurate so the drapery
    never comes back into step along the line.
    """
    h = [_hash01(j + 1, k) for k in range(9)]
    return {
        'theta': 2 * math.pi * (j + 0.62 * (h[0] - 0.5)) / SHEETS,
        'q': 0.30 + 0.62 * h[1],                    # 반경 방향 위치 → 층이 생긴다
        'f': (0.21 + 0.9 * h[2], 0.53 + 1.7 * h[3], 1.31 + 3.1 * h[4]),
        'a': (0.30 + 0.55 * h[5], 0.18 + 0.30 * h[6], 0.06 + 0.14 * h[7]),
        'w': 0.13 + 0.16 * h[8],
        'gain': 0.55 + 0.9 * h[(j + 3) % 9],
    }


SHEETS = 13
SHEET_SET = None


def _sheets():
    global SHEET_SET
    if SHEET_SET is None:
        SHEET_SET = [sheet_params(j) for j in range(SHEETS)]
    return SHEET_SET


def reduced_arc(arc, rads):
    """Arc length measured in local tube radii — the scale the structure lives on."""
    ds = np.diff(arc)
    rm = 0.5 * (rads[1:] + rads[:-1])
    return np.concatenate([[0.0], np.cumsum(ds / np.maximum(rm, 1e-30))])


def aurora_density(P, pts, rads, arc, frames, reduced, radial_width=0.26):
    """Emissivity of the curtain at a set of points.

    Sheets, not a filled tube: the emission sits on folded surfaces running
    along the line, which is what makes a real aurora read as drapery. Seeing
    one edge-on lengthens the path through it, so the integral along the ray
    brightens by itself — the white filaments are that, not a separate
    highlight.
    """
    t_ax, u_ax, v_ax = frames
    a, b = pts[:-1], pts[1:]
    ab = b - a
    seg = np.sqrt((ab * ab).sum(-1))
    den = np.maximum((ab * ab).sum(-1), 1e-30)

    flat = P.reshape(-1, 3)
    ap = flat[:, None, :] - a[None]
    tt = np.clip((ap * ab[None]).sum(-1) / den[None], 0.0, 1.0)
    perp = ap - tt[..., None] * ab[None]
    dist = np.sqrt((perp * perp).sum(-1))
    k = np.argmin(dist, axis=1)
    rows = np.arange(len(k))

    off = perp[rows, k]
    s = arc[k] + tt[rows, k] * seg[k]
    r = np.interp(s, arc, rads)
    # 접힘 파장을 절대 호길이에 걸면 관이 가는 구간에서 반경 수천 개에 걸쳐
    # 균일해져 구조가 사라진다. 국소 반경으로 잰 축길이 sigma = int ds/r 를 쓰면
    # 어느 배율에서 봐도 같은 결이 나온다 — 난류 매질이 실제로 그렇다.
    sigma = np.interp(s, arc, reduced)
    q = np.sqrt((off * off).sum(-1)) / np.maximum(r, 1e-30)
    theta = np.arctan2((off * u_ax[k]).sum(-1), (off * v_ax[k]).sum(-1))

    dens = np.zeros_like(q)
    for sh in _sheets():
        f, amp = sh['f'], sh['a']
        centre = (sh['theta']
                  + amp[0] * np.sin(f[0] * sigma + 2.1 * sh['q'])
                  + amp[1] * np.sin(f[1] * sigma - 1.3)
                  + amp[2] * np.sin(f[2] * sigma + 0.7))
        dth = np.arctan2(np.sin(theta - centre), np.cos(theta - centre))
        radial = np.exp(-((q - sh['q']) / radial_width) ** 2)
        along = 0.55 + 0.45 * np.sin(f[1] * 0.8 * sigma + 3.0 * sh['q'])
        dens = dens + sh['gain'] * along * radial * np.exp(-(dth / sh['w']) ** 2)

    envelope = np.clip(1.0 - q * q, 0.0, 1.0) ** 0.8
    return (envelope * (0.06 + dens)).reshape(P.shape[:-1])


def sheet_centreline(s, j):
    """Azimuth and radius of curtain j at arc length s — the ribbon route."""
    sh = _sheets()[j]
    f, amp = sh['f'], sh['a']
    return (sh['theta']
            + amp[0] * np.sin(f[0] * s + 2.1 * sh['q'])
            + amp[1] * np.sin(f[1] * s - 1.3)
            + amp[2] * np.sin(f[2] * s + 0.7)), sh['q']


def sheet_ribbons(spec, window=9.0, segments=64, n_sheets=SHEETS):
    """The curtains as ribbon centrelines — the in-game payload.

    Each entry is one strip: (point, radius) along the line at that curtain's
    folded azimuth. Raymarching the density is the primary in-game route and is
    known to work in KSP, so this is the cheaper alternative rather than the
    fallback of necessity: a plugin can build a two-triangle-wide mesh per
    curtain, blend additively and write no depth. Both come out of the same
    expression, which is the point.
    """
    keep = [e for e in spec['path'] if np.hypot(e[0][0], e[0][1]) <= window]
    keep = keep[:: max(1, len(keep) // segments)] or spec['path'][:2]
    pts = np.array([p for p, _, _, _ in keep])
    rads = np.array([r for _, r, _, _ in keep])
    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    _, u_ax, v_ax = _axis_frames(pts)

    out = []
    for j in range(n_sheets):
        th, qf = sheet_centreline(arc, j)
        rad = rads * qf
        centre = pts + rad[:, None] * (np.cos(th)[:, None] * v_ax
                                       + np.sin(th)[:, None] * u_ax)
        out.append((centre, rad))
    return out


def interior_camera(spec, at_arc, size, fov=1.15, tilt_deg=26.0,
                    offset_frac=0.55):
    """A perspective camera sitting *inside* the line, looking along it.

    The reference frame is shot from in there, and it is the view that tells
    you whether the fill reads as drapery or as fog — from outside, a thin tube
    looks like a plume whatever is inside it.
    """
    pts = np.array([p for p, _, _, _ in spec['path']])
    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    i = int(np.argmin(np.abs(arc - at_arc)))
    axis = pts[min(i + 4, len(pts) - 1)] - pts[max(i - 4, 0)]
    axis = axis / np.linalg.norm(axis)
    up0 = np.array([0.0, 0.0, 1.0])
    side = np.cross(axis, up0)
    side /= np.linalg.norm(side)

    # 축을 정면으로 보면 커튼이 전부 소실점으로 모여 바퀴살처럼 읽힌다. 참조
    # 프레임처럼 드레이프가 화면을 가로지르게 하려면 시선을 기울이고 눈을 축에서
    # 띄워야 한다 — 배가 관 한복판에 정지해 있는 그림이 아니다.
    rad = float(np.interp(arc[i], arc, [r for _, r, _, _ in spec['path']][:len(arc)]))
    eye = pts[i] + offset_frac * rad * np.cross(axis, side)
    tilt = math.radians(tilt_deg)
    fwd = math.cos(tilt) * axis + math.sin(tilt) * side
    fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, up0)
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)

    j, k = np.meshgrid(np.arange(size), np.arange(size), indexing='xy')
    sx = (j / (size - 1) - 0.5) * 2 * fov
    sy = (0.5 - k / (size - 1)) * 2 * fov
    d = fwd + sx[..., None] * right + sy[..., None] * up
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    return np.broadcast_to(eye, d.shape).copy(), d


def render_aurora_interior(spec, at_arc, size, depth, steps=170, gain=9.0,
                           segments=110, window=None, tilt_deg=26.0,
                           offset_frac=0.55):
    """Emission march from inside the line, looking down its length."""
    win = window if window is not None else at_arc + depth * 1.2
    keep = [e for e in spec['path']
            if np.hypot(e[0][0], e[0][1]) <= win]
    keep = keep[:: max(1, len(keep) // segments)] or spec['path'][:2]
    pts = np.array([p for p, _, _, _ in keep])
    rads = np.array([r for _, r, _, _ in keep])
    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    frames = _axis_frames(pts)
    reduced = reduced_arc(arc, rads)

    origin, direction = interior_camera(spec, at_arc, size,
                                        tilt_deg=tilt_deg,
                                        offset_frac=offset_frac)
    dt = depth / steps
    acc = np.zeros((size, size))
    for i in range(steps):
        Q = origin + (0.02 * depth + i * dt) * direction
        acc += aurora_density(Q, pts, rads, arc, frames, reduced) * dt
    e = np.clip(acc * gain / max(rads.max(), 1e-9), 0.0, None)
    a1 = 1.0 - np.exp(-e)
    a2 = np.clip((e - 0.55) / 1.9, 0.0, 1.0) ** 1.3
    col = CRIMSON * a1[..., None] + (MID - CRIMSON) * a2[..., None]
    return np.clip(col + np.array([0.012, 0.012, 0.02]), 0, 1)


def render_aurora(spec, view, span, size, centre, window=9.0, steps=150,
                  gain=9.0, segments=48):
    """Emission-only march. No surfaces, no lighting: the picture is the
    integral of the curtain's own glow along each ray, so thin parts stay
    translucent and stars would show through."""
    keep = [e for e in spec['path'] if np.hypot(e[0][0], e[0][1]) <= window]
    keep = keep[:: max(1, len(keep) // segments)] or spec['path'][:2]
    pts = np.array([p for p, _, _, _ in keep])
    rads = np.array([r for _, r, _, _ in keep])
    arc = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))])
    frames = _axis_frames(pts)
    reduced = reduced_arc(arc, rads)

    origin, direction, right, up = _camera(view, span, size)
    origin = origin + np.asarray(centre, dtype=float)
    t0, t1 = span * 2.4, span * 5.6

    # 광구는 불투명하다 — 광선을 거기서 멈춘다. 안 그러면 별 뒤쪽 커튼까지
    # 더해져서 별이 커튼 안에 잠긴 것처럼 보인다.
    oc = origin
    b = (oc * direction).sum(-1)
    c = (oc * oc).sum(-1) - spec['star_radius'] ** 2
    disc = b * b - c
    hit_star = disc > 0
    t_star = np.where(hit_star, -b - np.sqrt(np.maximum(disc, 0.0)), np.inf)
    t_star = np.where(t_star > 0, t_star, np.inf)
    t_end = np.minimum(t1, t_star)

    dt = (t1 - t0) / steps
    acc = np.zeros((size, size))
    for i in range(steps):
        t = t0 + i * dt
        Q = origin + t * direction
        live = t < t_end
        if not live.any():
            break
        acc += np.where(live, aurora_density(Q, pts, rads, arc, frames, reduced), 0.0) * dt
    e = np.clip(acc * gain / max(rads.max(), 1e-9), 0.0, None)

    # 밝기 → 색: 심홍에서 시작해 두꺼운 곳이 흰 코어로 간다(참조 이미지의 램프).
    # 흰색 피크는 뺀다(오너 지시). 두꺼운 곳이 흰 코어로 가는 대신 심홍에서
    # 밝은 장미빛까지만 오르고 거기서 포화한다.
    a1 = 1.0 - np.exp(-e)
    a2 = np.clip((e - 0.55) / 1.9, 0.0, 1.0) ** 1.3
    col = CRIMSON * a1[..., None] + (MID - CRIMSON) * a2[..., None]

    # 광구는 배경으로 깔고 커튼을 그 위에 가산한다.
    star_face = np.where(np.isfinite(t_star)[..., None],
                         np.array([1.0, 0.87, 0.60]), 0.0)
    return np.clip(col + star_face + np.array([0.012, 0.012, 0.02]), 0, 1)


if __name__ == '__main__':
    main()
