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
from render_alfven_wing import (path_sdf_np, downsample_path, _camera,  # noqa: E402
                                _march, _normal)


# 물리 입력만. 형상은 전부 petrova_line_geometry 가 도출한다.
SYSTEMS = {
    'sol-venus': dict(
        title='Sol → Venus', R_star_m=6.957e8, a_m=1.0821e11,
        R_target_m=6.0518e6, v_orbit_m_s=35.02e3, target='Venus'),
}


def build(name, gap_deg, start_frac, funnel_scale=0.7, funnel_power=1.5):
    s = dict(SYSTEMS[name])
    start_radius = start_frac * s['R_target_m']
    path, H = pg.petrova_path(s['R_star_m'], s['a_m'], s['R_target_m'],
                              gap_deg=gap_deg, start_radius_m=start_radius,
                              funnel_scale=funnel_scale, funnel_power=funnel_power)
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
        tube = path_sdf_np(P, pts, rads)
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
    d_beam = path_sdf_np(P, pts, rads)
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
    ap.add_argument('--funnel-scale', type=float, default=0.7,
                    help='funnel decay length in stellar radii')
    ap.add_argument('--funnel-power', type=float, default=1.5,
                    help='0 = exponential tail; p > 0 uses 1/(1+u^p), which '
                         'pinches as fast but leaves a thicker neck')
    ap.add_argument('--start-frac', type=float, default=0.25,
                    help='beam radius at the pole, in target radii')
    a = ap.parse_args()

    spec = build(a.system, a.gap_deg, a.start_frac,
                 a.funnel_scale, a.funnel_power)
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
         1.0, '3. the funnel off the pole, true scale',
         'amplitude derived, so it clears the pole with no collar'),
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
            f"wide at both ends: a funnel off the pole, widest it can be without breaking the "
            f"star's surface, a "
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


if __name__ == '__main__':
    main()
