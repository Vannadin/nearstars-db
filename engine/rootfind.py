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


# ── 핵 사격의 접힘: {dm = 0} 위 호 길이 이어 걷기와 그 근 고르기 (core-tc-fold-registration, 동결 fbbce52e) ─────────────
# Pure functions over callables. The caller (interior) supplies F(u, v) → (dm, g) on u = ln P_c, v = ln T_c, with
# dm = m/M − 1 (the shoot's mass residual) and g = ln(T_s/T_pot) (the loop's surface residual); F raises FoldOutside
# outside the declared domain. Nothing here reads the engine.

#: C2 — the tangent's finite-difference step in u and v (log units, so a relative step of P_c and T_c), declared value
FOLD_FD_STEP = 1e-5
#: C2 — an easy step is one whose corrector converges in at most this many iterations (68 n1)
EASY_ITERS = 2
#: C2 — the step rule: start, floor and ceiling of the arc step in (u, v), halve on corrector failure, double after
#: FOLD_EASY_RUN easy steps in a row; the budget counts predictor–corrector attempts over both legs
FOLD_H0 = 2e-3
FOLD_H_MIN = 1e-7
FOLD_H_MAX = 2e-2
FOLD_EASY_RUN = 3
FOLD_CORR_ITERS = 8
FOLD_BUDGET = 600
#: the crossing locator's iteration cap (Illinois on the step fraction)
FOLD_CROSS_ITERS = 40
#: F12 on the core chain — the same values as solver/solve.py's WARM_STEP_K / WARM_STEPS_MAX (a test asserts equality)
WARM_STEP_K = 10.0
WARM_STEPS_MAX = 20


class FoldOutside(Exception):
    """F was asked for a point outside the declared domain (or the integration there refused)."""


class FoldWalk:
    """The walk's record: accepted points (s, u, v, dm, g, t_u, t_v, ∂dm/∂u, ∂dm/∂v), the tangent oriented along increasing s; crossings of g = 0 (s, u, v, g), turning points in
    v (s, u, v, g), evaluations spent, and how it ended ("done" — both legs reached the domain's edge; "budget";
    "seed" — the seed could not be put on {dm = 0})."""

    def __init__(self):
        self.points: list = []
        self.crossings: list = []
        self.turning: list = []
        self.evals = 0
        self.attempts = 0
        self.status = "done"
        self.leg_ends: list = []


def _grad(F, u, v, f0, walk):
    du = F(u + FOLD_FD_STEP, v)[0]
    dv = F(u, v + FOLD_FD_STEP)[0]
    walk.evals += 2
    return (du - f0) / FOLD_FD_STEP, (dv - f0) / FOLD_FD_STEP


def _correct(F, u, v, gu, gv, tol_dm, walk):
    """Chord Newton on dm along the gradient direction from (u, v): returns (u, v, dm, g, iters) or None."""
    n2 = gu * gu + gv * gv
    if not n2 > 0.0:
        return None
    for it in range(FOLD_CORR_ITERS + 1):
        dm, g = F(u, v)
        walk.evals += 1
        if abs(dm) <= tol_dm:
            return u, v, dm, g, it
        if it == FOLD_CORR_ITERS:
            return None
        u, v = u - dm * gu / n2, v - dm * gv / n2
    return None


def fold_walk(F, seed, tol_dm: float, direction: float = -1.0, budget: int = FOLD_BUDGET, h0: float = FOLD_H0):
    """C1/C2 — pure arc-length continuation on {dm = 0} from `seed` = (u, v): first the leg whose tangent has
    du/ds of sign `direction` (−1: toward the shallow end, smaller P_c), to the domain's edge, then back through the seed
    to the other edge (item 8: the walk does not stop at its first crossing). Collects every crossing of g = 0 (located
    to |dm| ≤ tol_dm on the curve, g by Illinois on the step fraction) and every turning point of v(s)."""
    walk = FoldWalk()
    try:
        u0, v0 = seed
        dm0, g0 = F(u0, v0)
        walk.evals += 1
        gu, gv = _grad(F, u0, v0, dm0, walk)
        got = _correct(F, u0, v0, gu, gv, tol_dm, walk)
    except FoldOutside:
        got = None
    if got is None:
        walk.status = "seed"
        return walk
    u0, v0, dm0, g0, _it = got
    gu, gv = _grad(F, u0, v0, dm0, walk)
    legs = []
    for sense in (direction, -direction):
        pts = _leg(F, (u0, v0, dm0, g0, gu, gv), sense, tol_dm, budget, h0, walk)
        legs.append((sense, pts))
        if walk.status == "budget":
            break
    # one arc-length coordinate through the seed: the first leg negative, the second positive
    first = [(-s, u, v, dm, g, -tu, -tv, gu, gv) for s, u, v, dm, g, tu, tv, gu, gv in reversed(legs[0][1])]
    second = legs[1][1][1:] if len(legs) > 1 else []
    walk.points = first + second
    _scan(F, walk, tol_dm)
    return walk


def _leg(F, start, sense, tol_dm, budget, h0, walk):
    u, v, dm, g, gu, gv = start
    tu, tv = -gv, gu
    nt = math.hypot(tu, tv)
    tu, tv = tu / nt, tv / nt
    if (tu < 0.0) != (sense < 0.0):
        tu, tv = -tu, -tv
    pts = [(0.0, u, v, dm, g, tu, tv, gu, gv)]
    s, h, easy = 0.0, h0, 0
    while True:
        if walk.attempts >= budget:
            walk.status = "budget"
            walk.leg_ends.append(("budget", u, v))
            return pts
        walk.attempts += 1
        outside = False
        try:
            got = _correct(F, u + h * tu, v + h * tv, gu, gv, tol_dm, walk)
            if got is not None:
                nu, nv, ndm, ng, it = got
                ngu, ngv = _grad(F, nu, nv, ndm, walk)
        except FoldOutside:
            got, outside = None, True
        if got is None:
            h *= 0.5
            easy = 0
            if h < FOLD_H_MIN:      # the domain's edge (the last failure left the domain) or a corrector that won't close
                walk.leg_ends.append(("edge" if outside else "corrector", u, v))
                return pts
            continue
        ntu, ntv = -ngv, ngu
        nn = math.hypot(ntu, ntv)
        if not nn > 0.0:
            walk.leg_ends.append(("singular", nu, nv))
            return pts
        ntu, ntv = ntu / nn, ntv / nn
        if ntu * tu + ntv * tv < 0.0:      # keep the orientation along the curve
            ntu, ntv = -ntu, -ntv
        s += math.hypot(nu - u, nv - v)
        u, v, dm, g, gu, gv, tu, tv = nu, nv, ndm, ng, ngu, ngv, ntu, ntv
        pts.append((s, u, v, dm, g, tu, tv, gu, gv))
        easy = easy + 1 if it <= EASY_ITERS else 0
        if easy >= FOLD_EASY_RUN:
            h, easy = min(2.0 * h, FOLD_H_MAX), 0


def _scan(F, walk, tol_dm):
    """Crossings of g between neighbouring points (located on the curve) and turning points of v(s)."""
    pts = walk.points
    for a, b in zip(pts, pts[1:]):
        if (a[6] < 0.0) != (b[6] < 0.0):
            walk.turning.append((b[0], b[1], b[2], b[4]))
        if a[4] == 0.0:
            walk.crossings.append((a[0], a[1], a[2], a[4]))
            continue
        if (a[4] < 0.0) == (b[4] < 0.0) or b[4] == 0.0:
            continue
        walk.crossings.append(_locate(F, a, b, tol_dm, walk))
    if pts and pts[-1][4] == 0.0:
        walk.crossings.append((pts[-1][0], pts[-1][1], pts[-1][2], 0.0))


def _locate(F, a, b, tol_dm, walk):
    """g = 0 between accepted points a and b: Illinois on θ ∈ (0, 1), each trial put on the curve from the chord
    point a + θ(b − a) by the corrector along a's gradient direction (the chord is short: one accepted step)."""
    s_a, ua, va, _dma, ga = a[:5]
    s_b, ub, vb, _dmb, gb = b[:5]
    gu, gv = a[7], a[8]            # a's gradient of dm: the corrector's direction and scale
    lo, flo, hi, fhi, side = 0.0, ga, 1.0, gb, 0
    best = (s_a, ua, va, ga) if abs(ga) < abs(gb) else (s_b, ub, vb, gb)
    for _ in range(FOLD_CROSS_ITERS):
        th = lo - flo * (hi - lo) / (fhi - flo)
        try:
            got = _correct(F, ua + th * (ub - ua), va + th * (vb - va), gu, gv, tol_dm, walk)
        except FoldOutside:
            got = None
        if got is None:
            break
        u, v, _dm, g, _it = got
        cand = (s_a + th * (s_b - s_a), u, v, g)
        if abs(g) < abs(best[3]):
            best = cand
        if g == 0.0 or hi - lo < 1e-12:
            break
        if (g < 0.0) == (flo < 0.0):
            lo, flo = th, g
            if side == -1:
                fhi *= 0.5
            side = -1
        else:
            hi, fhi = th, g
            if side == 1:
                flo *= 0.5
            side = 1
    return best


def fold_states(walk, e_g: float):
    """Item 8 — the walk's crossings grouped into states: two consecutive crossings (in s) are one state iff
    max |g| over the walk's points between them is ≤ e_g (the excursion test). Each state is reported at its crossing
    nearest the seed (|s| least), with all its crossings: a list of (crossing_nearest_seed, crossings)."""
    cs = sorted(walk.crossings)
    groups: list = []
    for c in cs:
        if groups:
            prev = groups[-1][-1]
            between = [abs(p[4]) for p in walk.points if prev[0] < p[0] < c[0]]
            if (max(between) if between else 0.0) <= e_g:
                groups[-1].append(c)
                continue
        groups.append([c])
    return [(min(gr, key=lambda c: abs(c[0])), gr) for gr in groups]


def core_warm_choice(states_at, t0: float, states0, step: float = WARM_STEP_K, n_max: int = WARM_STEPS_MAX):
    """Item 10, owner F12 on the core chain: `states_at(t)` gives ("states", (T_c, …)) — one or more — or ("other", id)
    at T_pot t. Steps t0 + k·step for k = 1 … n_max until one state is left, then walks back taking at each T_pot the
    state nearest in T_c to the one chosen at the next warmer T_pot. Returns (T_c or None, trace, why)."""
    trace = [(t0, tuple(states0))]
    for k in range(1, n_max + 1):
        t = t0 + k * step
        kind, val = states_at(t)
        if kind != "states" or not val:
            trace.append((t, ()))
            return None, trace, f"the warm-side sweep met {val} at T_pot {t:g} K before one state was left"
        trace.append((t, tuple(val)))
        if len(val) == 1:
            chosen = val[0]
            for _t, sts in reversed(trace[:-1]):
                chosen = min(sts, key=lambda r: abs(r - chosen))
            return chosen, trace, None
    return None, trace, f"two or more states persist over {n_max} warm steps of {step:g} K"
