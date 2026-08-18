# 연화 Shue 곡면에 '일반화 스톡 pause'(waist·smooth)를 적합하는 도구 — ⚗ KerbalismShuePause 대기 세트
"""Fit the generalized stock magnetopause to a softened-Shue surface.

Stock Kerbalism scales x by one factor on the dayside and another on the nightside,
`px = x * (x<0 ? extension : compression)`, which kinks at x=0 and pins the widest
cross-section to the body plane. The KerbalismShuePause plugin generalizes that to

    u  = x - pause_waist
    px = (comp+ext)/2 * u  +  (comp-ext)/2 * sqrt(u^2 + pause_smooth^2)

which is C-infinity and lets the widest section sit downstream. `waist = smooth = 0`
reproduces stock exactly (methodology Part C, the ⚗ section).

This module answers the question that set produces: given a body whose boundary we
want to be a **softened Shue** surface, what five values render it best?

    r(theta) = r0 * ((1+eps)/(eps + cos^2(theta/2)))^alpha,
    eps      = 1/((L/r0)^(1/alpha) - 1)

Two conventions are baked in, both inherited from the sets already gated (Mercury,
Ganymede, Alpha Centauri A b III):

  * **compression retires to 1.0.** In the generalized form it would only pin the
    widest cross-section back to the body plane, which is the very thing `waist`
    exists to move, so the asymmetry is carried by `waist` alone.
  * **nose and tail are preserved exactly.** They are the two numbers the Shue fit
    itself is anchored on, so they are constraints rather than fit targets: given
    (waist, smooth) the radius and extension are solved from them, and only the
    two shape knobs are searched.

The search therefore runs over (waist, smooth) and minimizes the rms *relative*
radial deviation from the Shue curve, sampled uniformly in theta.

Usage:
    python3 scripts/refs/fit_generalized_pause.py                 # self-test
    python3 scripts/refs/fit_generalized_pause.py NOSE TAIL ALPHA # one body
"""
import math
import sys

import numpy as np
from scipy.optimize import brentq, minimize


def softened_shue_r(theta, r0, L, alpha):
    """Radius of the softened-Shue closed curve at angle theta from the star direction."""
    eps = 1.0 / ((L / r0) ** (1.0 / alpha) - 1.0)
    c2 = np.cos(theta / 2.0) ** 2
    return r0 * ((1.0 + eps) / (eps + c2)) ** alpha


def nose_tail(rad, comp, ext, waist, smooth):
    """Closed-form nose and tail of the generalized pause (see the belt viewer's
    pauseNoseTail; the discriminant collapses to B^2*(rad^2 + comp*ext*smooth^2))."""
    A, B, ce = 0.5 * (comp + ext), abs(0.5 * (comp - ext)), comp * ext
    s = B * math.sqrt(rad * rad + ce * smooth * smooth)
    return (A * rad - s) / ce + waist, (A * rad + s) / ce - waist


def solve_rad_ext(nose, tail, waist, smooth, comp=1.0):
    """Radius and extension that put the nose and tail exactly where asked."""
    def err(ext):
        # rad from the nose equation, then check the tail
        def f(rad):
            return nose_tail(rad, comp, ext, waist, smooth)[0] - nose
        try:
            rad = brentq(f, 1e-6, 1e4, xtol=1e-12)
        except ValueError:
            return 1e6, None
        return nose_tail(rad, comp, ext, waist, smooth)[1] - tail, rad
    lo, hi = 1e-6, comp - 1e-9
    flo = err(lo)[0]
    for _ in range(200):                     # bisection on ext (tail is monotone in it)
        mid = 0.5 * (lo + hi)
        fmid, rad = err(mid)
        if fmid == 1e6:
            hi = mid
            continue
        if (flo < 0) == (fmid < 0):
            lo, flo = mid, fmid
        else:
            hi = mid
    ext = 0.5 * (lo + hi)
    _, rad = err(ext)
    return rad, ext


def _model_r(theta, rad, comp, ext, waist, smooth):
    """Radius of the generalized-pause surface at angle theta (meridian plane)."""
    out = np.empty_like(theta)
    for i, th in enumerate(np.atleast_1d(theta)):
        ct, st = math.cos(th), math.sin(th)

        def g(r):
            u = r * ct - waist
            px = 0.5 * (comp + ext) * u + 0.5 * (comp - ext) * math.sqrt(u * u + smooth * smooth)
            return math.hypot(px, r * st) - rad
        hi = 1.0
        while g(hi) < 0 and hi < 1e6:
            hi *= 2.0
        out[i] = brentq(g, 1e-9, hi, xtol=1e-12)
    return out


def exact_alpha_half(nose, tail):
    """Closed-form generalized-pause set for alpha = 0.5. Exact, not a fit.

    At alpha = 0.5 the softened Shue surface and the generalized stock surface are the
    **same surface**, with `pause_waist` = 0. Writing c = cos^2(theta/2), the alpha=0.5
    Shue curve satisfies

        r^2 (2eps+1) + r x = 2 r0^2 (1+eps)

    and the generalized form with compression 1 and waist 0 satisfies

        r^2 + (1-e^2)/2 * x (S - x) + k^2 w^2 = rad^2,   S = sqrt(x^2+w^2), k = (1-e)/2.

    Requiring the second to reduce to the first forces S - x = lambda r on the surface,
    and consistency then pins lambda = 2/sqrt(1-e^2), which closes the system:

        eps = 1/((L/r0)^2 - 1),  q = 2 eps + 1
        extension = sqrt(1 - 1/q^2)
        C         = 2 r0^2 (1+eps) / q
        smooth    = 2 q sqrt(C)
        radius    = sqrt(C + ((1-extension)/2)^2 smooth^2)

    This is why the sub-Alfvenic branch is the one the two extra fields were built for:
    at any other alpha the generalized form can only approximate Shue (0.4 -> 9.6% rms,
    0.58 -> 3.3% at Mercury's nose and tail), and at 0.5 it is exact to machine
    precision. `pause_waist` is 0 for every body on this branch; the nonzero waists in
    the sets gated before 2026-08-18 are hand-fit artefacts sitting ~0.35% off.
    """
    eps = 1.0 / ((tail / nose) ** 2 - 1.0)
    q = 2.0 * eps + 1.0
    ext = math.sqrt(1.0 - 1.0 / (q * q))
    C = 2.0 * nose * nose * (1.0 + eps) / q
    smooth = 2.0 * q * math.sqrt(C)
    rad = math.sqrt(C + ((1.0 - ext) / 2.0) ** 2 * smooth * smooth)
    return {'pause_waist': 0.0, 'pause_smooth': round(smooth, 4),
            'pause_radius_smoothed': round(rad, 4), 'pause_compression_smoothed': 1.0,
            'pause_extension_smoothed': round(ext, 6)}


def fit(nose, tail, alpha, n=181, verbose=True):
    """Fit (waist, smooth) -> the five-value set. Returns (params dict, rms)."""
    theta = np.linspace(0.0, math.pi * 0.995, n)
    target = softened_shue_r(theta, nose, tail, alpha)

    def loss(p):
        waist, smooth = p
        if smooth < 0 or abs(waist) > 5 * nose:
            return 1e3
        try:
            rad, ext = solve_rad_ext(nose, tail, waist, smooth)
            if not (0 < ext < 1) or rad <= 0:
                return 1e3
            r = _model_r(theta, rad, 1.0, ext, waist, smooth)
        except Exception:
            return 1e3
        return float(np.sqrt(np.mean(((r - target) / target) ** 2)))

    best = None
    for w0 in (0.05 * nose, 0.2 * nose):          # 두 출발점 — 국소최소 방지
        for s0 in (0.5 * nose, 2.0 * nose, 4.0 * nose):
            r = minimize(loss, [w0, s0], method='Nelder-Mead',
                         options={'xatol': 1e-6, 'fatol': 1e-10, 'maxiter': 4000})
            if best is None or r.fun < best.fun:
                best = r
    waist, smooth = best.x
    rad, ext = solve_rad_ext(nose, tail, waist, smooth)
    p = {'pause_waist': round(waist, 4), 'pause_smooth': round(smooth, 4),
         'pause_radius_smoothed': round(rad, 4), 'pause_compression_smoothed': 1.0,
         'pause_extension_smoothed': round(ext, 6)}
    if verbose:
        n_, t_ = nose_tail(rad, 1.0, ext, waist, smooth)
        print(f"  nose {n_:.4f} (asked {nose})   tail {t_:.2f} (asked {tail})   "
              f"rms {best.fun*100:.2f}%   smooth/rad {smooth/rad:.2f}x")
        for k, v in p.items():
            print(f"    {k:30s} {v}")
    return p, best.fun


if __name__ == '__main__':
    if len(sys.argv) == 4:
        nose, tail, alpha = (float(x) for x in sys.argv[1:])
        print(f"nose {nose}  tail {tail}  alpha {alpha}")
        if abs(alpha - 0.5) < 1e-9:
            p = exact_alpha_half(nose, tail)
            print("  alpha = 0.5 -> exact closed form (no fit needed), pause_waist = 0")
            for k, v in p.items():
                print(f"    {k:30s} {v}")
        else:
            print("  alpha != 0.5 -> the generalized form can only approximate Shue here")
            fit(nose, tail, alpha)
    else:
        # 자기검증 두 가지. (1) 닫힌 해가 실제로 Shue 곡면 위에 있는가.
        # (2) 2026-08-18 이전에 손으로 맞춘 세트들이 그 곡면에서 얼마나 떨어져 있는가.
        def rms_against_shue(nose, tail, rad, ext, waist, smooth):
            th = np.linspace(0.001, math.pi * 0.995, 400)
            tgt = softened_shue_r(th, nose, tail, 0.5)
            mod = _model_r(th, rad, 1.0, ext, waist, smooth)
            return float(np.sqrt(np.mean(((mod - tgt) / tgt) ** 2)))

        CASES = [
            ('Mercury', 1.45, 217.5, (2.9, 0.01342, 0.0777, 4.2533)),
            ('Ganymede', 2.1096, 23.256, (3.9026, 0.18183, 0.0558, 6.2441)),
            ('Alpha Centauri A b III', 3.3857, 3.553, (3.3857, 0.95304, 0.2528, 13.5428)),
        ]
        print("alpha = 0.5: closed form vs the hand-fitted sets gated before 2026-08-18\n")
        for name, nose, tail, hand in CASES:
            p = exact_alpha_half(nose, tail)
            r_exact = rms_against_shue(nose, tail, p['pause_radius_smoothed'],
                                       p['pause_extension_smoothed'], 0.0, p['pause_smooth'])
            r_hand = rms_against_shue(nose, tail, hand[0], hand[1], hand[2], hand[3])
            ok = r_exact < 1e-5
            print(f"{name}  (nose {nose}, tail {tail})")
            print(f"   [{'PASS' if ok else 'FAIL'}] closed form   rms {r_exact:.2e}   "
                  f"waist 0  smooth {p['pause_smooth']}  radius {p['pause_radius_smoothed']}  "
                  f"extension {p['pause_extension_smoothed']}")
            print(f"          gated set     rms {r_hand:.2e}   "
                  f"waist {hand[2]}  smooth {hand[3]}  radius {hand[0]}  extension {hand[1]}")
