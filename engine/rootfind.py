# 0 을 사이에 둔 두 시행 안에서 근을 좁히는 엔진 공용 도우미 — 한 걸음에 한 번 평가하는 Brent 법 (C152)
"""Bracketed root finding for loops that spend one pass per evaluation (prereg-c152-straddle-root).

`brent(a, fa, b, fb, xtol)` is a generator: ``x = next(g)`` gives the first trial, ``x = g.send(fx)`` the next
one, and ``StopIteration`` ends it when the bracket is narrower than ``xtol``. ``g.bracket`` is not available on a
generator, so the last state is returned as ``StopIteration.value``: ``(x_best, f_best, x_lo, x_hi)``.

The algorithm is Brent (1973) «zeroin» — inverse quadratic interpolation or secant when they stay inside the
bracket and shrink it fast enough, bisection otherwise — so it converges whenever ``fa`` and ``fb`` differ in sign.
A residual that **jumps** across zero (no root) is narrowed to the jump; the caller sees ``|f_best|`` stay large.
"""
from __future__ import annotations

import math


def brent(a: float, fa: float, b: float, fb: float, xtol: float):
    """양 끝을 **곧바로** 검사한다(생성기는 첫 next 까지 몸통을 안 돌리므로, 검사를 밖에 둔다)."""
    if (fa < 0.0) == (fb < 0.0) and fa != 0.0 and fb != 0.0:
        raise ValueError("rootfind.brent: fa and fb do not straddle zero")
    return _brent(a, fa, b, fb, xtol)


def _brent(a: float, fa: float, b: float, fb: float, xtol: float):
    if fa == 0.0:
        return a, fa, a, a
    if fb == 0.0:
        return b, fb, b, b
    c, fc = a, fa
    d = e = b - a
    while True:
        if (fb > 0.0) == (fc > 0.0):
            c, fc = a, fa
            d = e = b - a
        if abs(fc) < abs(fb):
            a, b, c = b, c, b
            fa, fb, fc = fb, fc, fb
        tol = 2.0 * 2.220446049250313e-16 * abs(b) + 0.5 * xtol
        m = 0.5 * (c - b)
        if abs(m) <= tol or fb == 0.0:
            return b, fb, min(b, c), max(b, c)
        if abs(e) >= tol and abs(fa) > abs(fb):
            s = fb / fa
            if a == c:
                p, q = 2.0 * m * s, 1.0 - s
            else:
                q0, r = fa / fc, fb / fc
                p = s * (2.0 * m * q0 * (q0 - r) - (b - a) * (r - 1.0))
                q = (q0 - 1.0) * (r - 1.0) * (s - 1.0)
            if p > 0.0:
                q = -q
            else:
                p = -p
            if 2.0 * p < min(3.0 * m * q - abs(tol * q), abs(e * q)):
                e, d = d, p / q
            else:
                d = e = m
        else:
            d = e = m
        a, fa = b, fb
        b = b + d if abs(d) > tol else b + math.copysign(tol, m)
        fb = yield b
