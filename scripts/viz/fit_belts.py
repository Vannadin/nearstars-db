# 쌍극자 L-셸 타깃 영역에 Kerbalism 벨트 SDF 파라미터를 수치 피팅(IoU 최대화)하는 도구
# SDF 알고리즘 출처: Kerbalism (github.com/Kerbalism/Kerbalism), src/Kerbalism/Radiation/Radiation.cs (Unlicense).
import json
import os
import sys

import numpy as np
from scipy.optimize import minimize

# ---------------- Kerbalism SDF (meridian half-plane, comp/ext = 1) ----------------
# Coordinates: rho = sqrt(x^2+z^2) >= 0 (equatorial distance), y = magnetic axis.
# Region is the revolve of this half-plane section; day-night comp/ext is applied
# later at render time and is not fitted (the target is axisymmetric).

def belt_sdf(rho, y, dist, rad, dxy, bdist, brad, bdxy):
    q1 = np.sqrt(rho * rho * dxy) - dist
    d1 = np.sqrt(q1 * q1 + y * y) - rad
    q2 = np.sqrt(rho * rho * bdxy) - bdist
    d2 = np.sqrt(q2 * q2 + y * y) - brad
    return np.maximum(d1, -d2)

# ---------------- target regions ----------------

def shell_mask(rho, y, L1, L2, rcut):
    """Dipole drift shell between field lines L1..L2, loss-cone cut at r=rcut.
    Field line: r = L cos^2(lambda)  ->  L = r^3 / rho^2."""
    r = np.sqrt(rho * rho + y * y)
    with np.errstate(divide='ignore', invalid='ignore'):
        L = np.where(rho > 1e-9, r ** 3 / (rho * rho), np.inf)
    return (L >= L1) & (L <= L2) & (r >= rcut)

def slab_mask(rho, y, r1, r2, h):
    """Equatorial current-sheet slab (magnetodisc): rho in [r1,r2], |y| <= h."""
    return (rho >= r1) & (rho <= r2) & (np.abs(y) <= h)

def make_target(spec, rho, y):
    if 'L' in spec:
        return shell_mask(rho, y, spec['L'][0], spec['L'][1], spec.get('rcut', 1.0))
    return slab_mask(rho, y, *spec['slab'])

# ---------------- fitting ----------------

def iou(a, b):
    inter = np.count_nonzero(a & b)
    union = np.count_nonzero(a | b)
    return inter / union if union else 0.0

def fit_belt(spec, extent=None, grid=360, verbose=True):
    """Fit (dist, rad, dxy, bdist, brad, bdxy) to the target region. Returns (params, iou)."""
    if extent is None:
        extent = (spec['L'][1] if 'L' in spec else spec['slab'][1]) * 1.25
    ax = np.linspace(0, extent, grid)
    rho, y = np.meshgrid(ax, ax)          # quarter plane (y>=0; both are y-symmetric)
    target = make_target(spec, rho, y)

    def loss(p):
        dist, rad, dxy, bdist, brad, bdxy = p
        if dist <= 0 or rad <= 0 or not (0.02 <= dxy <= 2.0) or not (0.02 <= bdxy <= 2.0) \
           or bdist < 0 or brad < 0:
            return 1.0
        return 1.0 - iou(belt_sdf(rho, y, *p) < 0, target)

    # analytic init from the target's equatorial span + height
    eq = target[0]; heights = target.any(axis=1)
    if not eq.any():                      # hollow at equator? (shouldn't happen)
        eq = target.any(axis=0)
    lo, hi = ax[eq][0], ax[eq][-1]
    ymax = ax[heights][-1] if heights.any() else (hi - lo) / 2
    starts = []
    for dxy0 in (0.15, 0.35, 0.6, 0.9):
        s = np.sqrt(dxy0)
        dist0 = (lo + hi) / 2 * s
        rad0 = max((hi - lo) / 2 * s, ymax * 0.7)
        # border init A: origin-centred sphere cut at the inner edge (D-cut)
        starts.append([dist0, rad0, dxy0, 1e-4, lo * 0.9, 1.0])
        # border init B: torus carve on the concave side (stock-Earth-outer style)
        starts.append([dist0, rad0, dxy0, lo * 0.8 * s, rad0 * 0.8, dxy0])
    best, best_l = None, 1.0
    for s0 in starts:
        r = minimize(loss, s0, method='Nelder-Mead',
                     options={'maxiter': 4000, 'xatol': 1e-4, 'fatol': 1e-5})
        # polish once from the winner of the first pass
        if r.fun < best_l:
            best, best_l = r.x, r.fun
    r = minimize(loss, best, method='Nelder-Mead',
                 options={'maxiter': 6000, 'xatol': 1e-5, 'fatol': 1e-6})
    if r.fun < best_l:
        best, best_l = r.x, r.fun
    fit_iou = 1.0 - best_l
    if verbose:
        d, ra, dx, bd, br, bx = best
        s = np.sqrt(dx)
        print(f"  IoU {fit_iou:.3f} | dist {d:.3f} rad {ra:.3f} dxy {dx:.3f} "
              f"bdist {bd:.4f} brad {br:.3f} bdxy {bx:.3f} "
              f"| equator {(max(d - ra, 0)) / s:.2f}..{(d + ra) / s:.2f} R")
    return best, fit_iou

# ---------------- diagnostics render (target outline vs fitted region) ----------------

def diag_png(spec, params, path, extent=None, size=480):
    from PIL import Image
    if extent is None:
        extent = (spec['L'][1] if 'L' in spec else spec['slab'][1]) * 1.25
    ax_x = np.linspace(0, extent, size)
    ax_y = np.linspace(extent, -extent, 2 * size)
    rho, y = np.meshgrid(ax_x, ax_y)
    target = make_target(spec, rho, y)
    fitted = belt_sdf(rho, y, *params) < 0
    img = np.zeros((2 * size, size, 3), np.uint8)
    img[fitted] = (200, 90, 30)                     # fitted SDF region
    img[target & ~fitted] = (60, 60, 200)           # target missed by fit
    img[target & fitted] = (240, 220, 120)          # overlap
    r = np.sqrt(rho * rho + y * y)
    img[r < 1.0] = (70, 80, 95)                     # body
    Image.fromarray(img, 'RGB').save(path)

# ---------------- per-body physical belt targets ----------------
# L-ranges/cuts from the ADS anchors in docs/reference/solar-system-radiation-belts.md.

TARGETS = {
    # Earth: inner proton belt L~1.1-2 (peak 1.5), outer electron belt L~3-7 (heart 4-5)
    # inner rcut = 1000 km altitude (r~1.16): the inner-belt lower boundary, not the
    # atmosphere top -- trapped flux below ~1000 km is loss-cone-depleted (AP9 picture;
    # the offset dipole dips it to ~200 km only in the SAA, which geomagnetic_offset carries)
    'earth_inner':   {'L': (1.1, 2.0), 'rcut': 1.157},
    'earth_outer':   {'L': (3.0, 7.0), 'rcut': 1.05},
    # Jupiter: dipolar inner belt peak ~1.5-2 R_J; outer = flat magnetodisc.
    # Disc half-thickness 3.0 (Khurana 1989 canonical ~3-3.5); radial 3-16 is a
    # frame truncation -- the physical disc extends past 50 R_J.
    'jupiter_inner': {'L': (1.2, 3.0), 'rcut': 1.03},
    'jupiter_disc':  {'slab': (3.0, 16.0, 3.0)},
    # Saturn: rings absorb inside ~2.3 R_S; weak CRAND belt out to ~6 (Dione filter)
    'saturn_outer':  {'L': (2.3, 6.0), 'rcut': 1.05},
    # Uranus: structural boundaries are the moon L-shells (Krimigis 1986 "except
    # inside the orbit of Miranda"; Cheng 1987 electron minima at Miranda/Ariel/
    # Umbriel L = 5.1/7.5/10.4, broad maxima between): inner = inside Miranda,
    # outer = Miranda..Umbriel. Detectable trapping reaches Titania (~L 17).
    'uranus_inner':  {'L': (1.5, 5.0), 'rcut': 1.05},
    'uranus_outer':  {'L': (5.0, 10.0), 'rcut': 1.05},
    # Neptune: peak L~7, hard Triton cut ~14
    'neptune_inner': {'L': (1.5, 5.0), 'rcut': 1.05},
    'neptune_outer': {'L': (5.0, 14.0), 'rcut': 1.05},
    # Ganymede: single weak belt on closed lines inside ~2 R_G standoff.
    # rcut = 1.0: no atmosphere -- particles absorb at the surface itself.
    'ganymede_belt': {'L': (1.1, 1.9), 'rcut': 1.0},
}

if __name__ == '__main__':
    only = sys.argv[1:] or None
    outdir = os.environ.get('BELT_FIT_DIAG', '')
    results = {}
    for name, spec in TARGETS.items():
        if only and name not in only:
            continue
        print(name)
        params, fiou = fit_belt(spec)
        results[name] = {'params': dict(zip(
            ['dist', 'rad', 'dxy', 'bdist', 'brad', 'bdxy'],
            [round(float(v), 4) for v in params])), 'iou': round(fiou, 3)}
        if outdir:
            diag_png(spec, params, os.path.join(outdir, name + '.png'))
    print(json.dumps(results, indent=1))
