# 경계층 근의 연속 추적과 접힘 사건 — samuel_run · thermal_stack 이 같이 쓰는 한 벌 (C145, prereg-c145-fold-continuation)
"""Root continuation and fold events for the boundary-layer solve (C145, `prereg-c145-fold-continuation.md` 15a66cc8).

Today the solve rescans δ_b on 48 cells at every evaluation and keeps the root nearest the previous one. E0
(`pc/c145/e0.md`) showed that the scan loses a root pair ~20 km apart inside one cell (R2, 0.783 Gyr), and that
which RK4 stage it loses it at decides the path. This module replaces that, on the main ("nearest") branch, with:

- **continuation** (§2.1): the adopted root is refined inside a local bracket around its last accepted value,
  half-width w = min(max(K·|Δx_last|, FLOOR), ½ × distance to the nearest other root on either side);
- a **fold function** (§2.2): g = the signed extremum of h between the adopted root and its neighbour on the side
  of motion; a fold is a sign flip of g;
- **event location** (§2.3): a step over which the adopted root is lost to a fold is bisected in length to
  min(1e-9 Gyr, 1e-6 × step), taken on the old branch, and the branch is switched at the event;
- the **branch after the event** (§2.4): the root nearest δ* by a full scan of ≥ 4096 cells, the larger on a tie.

`samuel_run` and `thermal_stack` must stay bit-identical (T2 §7), so both call this one copy.
"""
from __future__ import annotations

import math

K_BRACKET = 4.0            # §2.1 k
FLOOR_M = 1e3              # §2.1 floor, 1 km
FULL_SCAN = 4096           # §2.4: cells of the event-time scan (E0: 48 lost a 20 km pair; 4096 resolved 0.21 km)
NEIGHBOUR_CELLS = 256      # neighbour search reach, in full-scan cells on each side (inner δ_b: one h per cell)
OUTER_NEIGHBOUR_CELLS = 32  # the outer δ_u search: each cell costs an inner solve, so it looks less far
BISECT_ITERS = 50          # as the solves' own bracket bisection
GOLDEN_ITERS = 60
EVENT_TOL_GYR = 1e-9       # §2.3
EVENT_TOL_STEP = 1e-6      # §2.3: the tolerance is at most this fraction of the current step
MIN_STEP_FRACTION = 2.0 ** -40   # reject-and-halve gives up below this fraction of the step (named refusal)
_PHI = (math.sqrt(5.0) - 1.0) / 2.0


class Lost(Exception):
    """The adopted root was not found in its local bracket. `fold` tells which way: True — the hump between it and
    its neighbour on the side of motion changed sign (a fold, §2.2); False — it left the bracket (§2.1)."""

    def __init__(self, equation: str, fold: bool):
        super().__init__(f"{equation}: {'fold' if fold else 'left the bracket'}")
        self.equation, self.fold = equation, fold


class Root:
    """One tracked root: its value and last accepted change, and its neighbours below and above (None = none
    within reach) with their own last changes — the neighbours are carried by the same continuation (§2.1)."""
    __slots__ = ("x", "dx", "lo", "hi", "dlo", "dhi", "g")

    def __init__(self, x: float, dx: float = 0.0, lo: float | None = None, hi: float | None = None,
                 dlo: float = 0.0, dhi: float = 0.0, g: float = 0.0):
        #: g — the sign (+1/−1) of h on the hump between x and the neighbour ahead, at this accepted state; 0 = none
        self.x, self.dx, self.lo, self.hi, self.dlo, self.dhi, self.g = x, dx, lo, hi, dlo, dhi, g

    def ahead(self):
        """The neighbour on the side of motion, or None when there is none there. Before any motion (Δx = 0,
        the first accepted state after a cold start or an event) the nearer neighbour stands in."""
        if self.dx > 0.0:
            return self.hi
        if self.dx < 0.0:
            return self.lo
        near = [n for n in (self.lo, self.hi) if n is not None]
        return min(near, key=lambda n: abs(n - self.x)) if near else None

    def __repr__(self):
        return f"Root({self.x!r}, dx={self.dx!r}, lo={self.lo!r}, hi={self.hi!r}, g={self.g!r})"


class Track:
    """The continuation state carried from one accepted state to the next: the outer δ_u and inner δ_b roots."""
    __slots__ = ("u", "b")

    def __init__(self, u: Root, b: Root):
        self.u, self.b = u, b


def bisect(f, a: float, b: float, fa: float) -> float:
    """The solves' own bracket bisection (same arithmetic)."""
    for _ in range(BISECT_ITERS):
        m = 0.5 * (a + b)
        fm = f(m)
        if (fm > 0) == (fa > 0):
            a, fa = m, fm
        else:
            b = m
    return 0.5 * (a + b)


def half_width(r: Root) -> float:
    """§2.1: w = min(max(K·|Δx_last|, FLOOR), ½ × distance to the nearest other root on either side)."""
    w = max(K_BRACKET * abs(r.dx), FLOOR_M)
    gaps = [r.x - r.lo] if r.lo is not None else []
    if r.hi is not None:
        gaps.append(r.hi - r.x)
    if gaps:
        w = min(w, 0.5 * min(gaps))
    return w


def local_root(h, r: Root, lo: float, hi: float):
    """The root of h in [x − w, x + w] ∩ [lo, hi], or None when h does not change sign there."""
    w = half_width(r)
    a, b = max(lo, r.x - w), min(hi, r.x + w)
    if not a < b:
        return None
    fa, fb = h(a), h(b)
    if math.isnan(fa) or math.isnan(fb) or (fa > 0) == (fb > 0):
        return None
    return bisect(h, a, b, fa)


def hump(h, a: float, b: float, sign: float) -> tuple[float, float]:
    """(location, value) of the extremum of `sign`·h strictly between a and b, by golden section. Between two
    adjacent roots h keeps one sign; with that sign this is the hump that shrinks to zero when they meet (§2.2).
    The returned value is h itself (signed)."""
    lo, hi = min(a, b), max(a, b)
    c, d = hi - _PHI * (hi - lo), lo + _PHI * (hi - lo)
    fc, fd = sign * h(c), sign * h(d)
    for _ in range(GOLDEN_ITERS):
        if fc > fd:
            hi, d, fd = d, c, fc
            c = hi - _PHI * (hi - lo)
            fc = sign * h(c)
        else:
            lo, c, fc = c, d, fd
            d = lo + _PHI * (hi - lo)
            fd = sign * h(d)
    x = 0.5 * (lo + hi)
    return x, h(x)


def hump_sign(h, r: Root) -> float:
    """The sign of h between the root and its neighbour ahead (0 when there is none) — kept at accepted states."""
    nb = r.ahead()
    if nb is None:
        return 0.0
    return 1.0 if h(0.5 * (r.x + nb)) > 0 else -1.0


def lost(h, r: Root, equation: str) -> Lost:
    """Classify a root that `local_root` did not find (§2.1–§2.2). With a neighbour ahead at the last accepted
    state, search the interval the pair spanned for the hump of the sign it had then (`r.g`): if none is left
    (the extremum of g·h is ≤ 0), the pair met and vanished — a fold. Anything else is the root leaving its
    bracket."""
    nb = r.ahead()
    if nb is None or r.g == 0.0:
        return Lost(equation, False)
    _, g_now = hump(h, r.x, nb, r.g)
    return Lost(equation, r.g * g_now <= 0.0)


def scan(h, lo: float, hi: float, n: int) -> list:
    """Every root of h on [lo, hi] by n cells + bisection (sign changes only)."""
    roots, a, fa = [], lo, h(lo)
    for k in range(1, n + 1):
        b = lo + (hi - lo) * k / n
        fb = h(b)
        if (fa > 0) != (fb > 0):
            roots.append(bisect(h, a, b, fa))
        a, fa = b, fb
    return roots


def neighbours(h, x: float, lo: float, hi: float, reach: int = NEIGHBOUR_CELLS) -> tuple:
    """(nearest root below x, nearest root above x) within `reach` full-scan cells, or None. The search starts half
    a cell away from x so the adopted root itself is not counted — a neighbour closer than that is found only by
    continuation (`accept`), never by this search."""
    cell = (hi - lo) / FULL_SCAN
    out = []
    for step in (-cell, cell):
        found = None
        a = x + 0.5 * step
        if lo <= a <= hi:
            fa = h(a)
            for _ in range(reach):
                b = a + step
                if not lo <= b <= hi:
                    break
                fb = h(b)
                if (fa > 0) != (fb > 0):
                    found = bisect(h, min(a, b), max(a, b), fa if a < b else fb)
                    break
                a, fa = b, fb
        out.append(found)
    return out[0], out[1]


def _continue_neighbour(h, nb, dnb: float, x: float, side: float, lo: float, hi: float):
    """Carry a neighbour of the adopted root (now at x) to this state: its own local bracket, half-width
    min(max(K·|Δ|, FLOOR), ½ × its distance to x), kept on its side of x. None when it is not found there (it met
    another root, or moved away) — the caller then searches for a new one."""
    if nb is None:
        return None
    w = min(max(K_BRACKET * abs(dnb), FLOOR_M), 0.5 * abs(nb - x))
    a, b = nb - w, nb + w
    if side > 0:
        a = max(a, x + 0.5 * abs(nb - x))
    else:
        b = min(b, x - 0.5 * abs(nb - x))
    a, b = max(a, lo), min(b, hi)
    if not a < b:
        return None
    fa, fb = h(a), h(b)
    if math.isnan(fa) or math.isnan(fb) or (fa > 0) == (fb > 0):
        return None
    return bisect(h, a, b, fa)


def accept(h, prev: Root | None, x: float, lo: float, hi: float, reach: int = NEIGHBOUR_CELLS) -> Root:
    """The tracked root at a newly accepted state where the adopted root is x: both neighbours carried from
    `prev` by continuation, a missing one searched for (`neighbours`), and the hump sign toward the neighbour
    ahead. `prev` None (a cold start or an event) searches for both."""
    if prev is None:
        r = Root(x)
        r.lo, r.hi = neighbours(h, x, lo, hi, reach)
    else:
        r = Root(x, x - prev.x)
        r.lo = _continue_neighbour(h, prev.lo, prev.dlo, x, -1.0, lo, hi)
        r.hi = _continue_neighbour(h, prev.hi, prev.dhi, x, 1.0, lo, hi)
        if r.lo is None or r.hi is None:
            nlo, nhi = neighbours(h, x, lo, hi, reach)
            r.lo = r.lo if r.lo is not None else nlo
            r.hi = r.hi if r.hi is not None else nhi
        r.dlo = r.lo - prev.lo if (r.lo is not None and prev.lo is not None) else 0.0
        r.dhi = r.hi - prev.hi if (r.hi is not None and prev.hi is not None) else 0.0
    r.g = hump_sign(h, r)
    return r


def pick_after(roots: list, d_star: float, dead: tuple | None = None):
    """§2.4: the root nearest δ*, the larger on an exact tie. Roots inside the vanished pair's interval `dead`
    (widened by one full-scan cell each side) are the dying pair itself and are excluded."""
    keep = [x for x in roots if dead is None or not (dead[0] <= x <= dead[1])]
    if not keep:
        return None
    return min(keep, key=lambda x: (abs(x - d_star), -x))


def event_tolerance_s(h_s: float, gyr_s: float) -> float:
    """§2.3: min(1e-9 Gyr, 1e-6 × the current step), in seconds."""
    return min(EVENT_TOL_GYR * gyr_s, EVENT_TOL_STEP * h_s)


def advance(step, y: list, t_gyr: float, h_s: float, gyr_s: float):
    """One accepted step from (y, t). `step(y, t_gyr, h_s)` takes a full RK4 step **on the step-start branch** and
    checks the end state; it raises `Lost` when a stage or the end state loses the adopted root.

    Returns (y_end, h_used, event) — `event` is the `Lost` of a located fold, else None.
    - A root that leaves its bracket (§2.1): the step is rejected and halved, never rescanned. Below
      MIN_STEP_FRACTION of the first try the `Lost` is raised to the caller (which refuses by name).
    - A fold (§2.3): the step length is bisected between a step that keeps the root and one that loses it, to
      `event_tolerance_s`; the longest step that keeps it is taken. The caller switches the branch at its end."""
    h = h_s
    while True:
        try:
            return step(y, t_gyr, h), h, None
        except Lost as e:
            if not e.fold:
                h *= 0.5
                if h < MIN_STEP_FRACTION * h_s:
                    raise
                continue
            tol = event_tolerance_s(h, gyr_s)
            lo, hi, y_lo = 0.0, h, y
            while hi - lo > tol:
                mid = 0.5 * (lo + hi)
                try:
                    y_mid = step(y, t_gyr, mid)
                except Lost:
                    hi = mid
                else:
                    lo, y_lo = mid, y_mid
            e.tol_s = tol
            return y_lo, lo, e
