# 표 보간의 한 자리 — 적분기가 읽는 표 값을 단조 3 차 에르미트(PCHIP)로 C¹ 보간(쌍선형의 격자점 꺾임 = C157 규칙 1 이음매 부류를 없앰)
"""Shared C¹ table interpolation (prereg-c157 post-freeze note 10).

Monotone piecewise-cubic Hermite (Fritsch & Carlson 1980; the PCHIP slope rule) on non-uniform 1-D grids, and its
tensor product on 2-D grids:

- node slopes: weighted harmonic mean of the neighbouring secants, zero where they differ in sign; at an end or a
  missing neighbour, PCHIP's one-sided three-point form; with two usable nodes only, linear;
- reproduces node values exactly, stays within the bracketing node values on monotone data, C¹ along each axis;
- 2-D: interpolate along the second axis on each row of the 4 x 4 stencil, then along the first axis through those
  values. A missing (None) node *outside* the query cell is replaced, for slope estimation only, by linear
  extrapolation from its own row's nearest real node along that row's PCHIP end slope (audit e2: a stencil that
  shrinks per query would make the slopes, and so the value, jump where a neighbouring row ends). The stencil shape
  therefore never changes and C¹ holds next to ragged edges. A missing corner of the query cell raises `CellMissing`
  so callers keep today's refusal.

`MODE` = "pchip" (default) or "linear" (today's bilinear / linear, for comparison fixtures only).
"""
from __future__ import annotations

import math

MODE = "pchip"
#: 노트 10 (감사 e2 HOLD 1) — 2 차원 읽기에서 빈 이웃 격자점을 그 열의 끝 기울기로 외삽해 쓴 횟수(값 밖 셈). 0 이 아니면 그
#   읽기가 들쭉날쭉한 표 가장자리 옆이었다는 뜻 — 외삽은 기울기 추정에만 쓰고, 묻는 칸의 네 모서리는 늘 실제 값이다.
EXTRAPOLATED_READS = [0]


class CellMissing(Exception):
    """A corner of the query cell has no value."""


def _end_slope(h0: float, h1: float, d0: float, d1: float) -> float:
    """PCHIP one-sided three-point slope at an end node (d0 the adjacent secant, d1 the next)."""
    s = ((2.0 * h0 + h1) * d0 - h0 * d1) / (h0 + h1)
    if s * d0 <= 0.0:
        return 0.0
    if d0 * d1 < 0.0 and abs(s) > 3.0 * abs(d0):
        return 3.0 * d0
    return s


def _inner_slope(h0: float, h1: float, d0: float, d1: float) -> float:
    """PCHIP interior slope from the left secant d0 (width h0) and the right secant d1 (width h1)."""
    if d0 * d1 <= 0.0:
        return 0.0
    w1, w2 = 2.0 * h1 + h0, h1 + 2.0 * h0
    return (w1 + w2) / (w1 / d0 + w2 / d1)


def _coeffs(xs, ys, i: int):
    """(x0, h, y0, y1, m0, m1) of cell i — node values and PCHIP node slopes. Raises CellMissing if a corner is missing."""
    y0, y1 = ys[i], ys[i + 1]
    if y0 is None or y1 is None:
        raise CellMissing(i)
    x0, x1 = xs[i], xs[i + 1]
    h = x1 - x0
    d = (y1 - y0) / h
    has_l = i - 1 >= 0 and ys[i - 1] is not None
    has_r = i + 2 < len(xs) and ys[i + 2] is not None
    if has_l:
        hl = x0 - xs[i - 1]
        m0 = _inner_slope(hl, h, (y0 - ys[i - 1]) / hl, d)
    elif has_r:
        hr = xs[i + 2] - x1
        m0 = _end_slope(h, hr, d, (ys[i + 2] - y1) / hr)
    else:
        m0 = d
    if has_r:
        hr = xs[i + 2] - x1
        m1 = _inner_slope(h, hr, d, (ys[i + 2] - y1) / hr)
    elif has_l:
        hl = x0 - xs[i - 1]
        m1 = _end_slope(h, hl, d, (y0 - ys[i - 1]) / hl)
    else:
        m1 = d
    return x0, h, y0, y1, m0, m1


def _hermite(x: float, c) -> float:
    x0, h, y0, y1, m0, m1 = c
    t = (x - x0) / h
    t2, t3 = t * t, t * t * t
    return ((2.0 * t3 - 3.0 * t2 + 1.0) * y0 + (t3 - 2.0 * t2 + t) * h * m0
            + (-2.0 * t3 + 3.0 * t2) * y1 + (t3 - t2) * h * m1)


def cubic1(x: float, xs, ys, i: int) -> float:
    """Value at x in [xs[i], xs[i+1]]. `ys` is indexable with None for missing nodes; xs strictly increasing."""
    y0, y1 = ys[i], ys[i + 1]
    x0, x1 = xs[i], xs[i + 1]
    t = (x - x0) / (x1 - x0)
    # 무게 0 인 끝은 안 본다 — 격자선 위의 물음이 옆 빈 칸 때문에 거절되지 않게(오늘의 쌍선형과 같은 규칙)
    if t == 0.0 and y0 is not None:
        return y0
    if t == 1.0 and y1 is not None:
        return y1
    if y0 is None or y1 is None:
        raise CellMissing(i)
    if MODE == "linear":
        return y0 + (y1 - y0) * t
    return _hermite(x, _coeffs(xs, ys, i))


def cubic2(xa: float, xb: float, xs_a, xs_b, val, ia: int, ib: int, cache: dict | None = None) -> float:
    """Value at (xa, xb) in cell [ia, ia+1] x [ib, ib+1]. `val(ka, kb)` returns the node value or None.
    `cache` (optional, per static table and field): the second-axis Hermite coefficients of a stencil row depend only on
    the table, so they are kept by (row, cell, required) — the same arithmetic, so the same values, read once."""
    if MODE == "linear":
        q = (val(ia, ib), val(ia + 1, ib), val(ia, ib + 1), val(ia + 1, ib + 1))
        u = (xa - xs_a[ia]) / (xs_a[ia + 1] - xs_a[ia])
        v = (xb - xs_b[ib]) / (xs_b[ib + 1] - xs_b[ib])
        w = ((1 - u) * (1 - v), u * (1 - v), (1 - u) * v, u * v)
        if any(x is None and wx > 0.0 for x, wx in zip(q, w)):
            raise CellMissing((ia, ib))
        return math.fsum(wx * x for x, wx in zip(q, w) if wx > 0.0)
    na = len(xs_a)
    rows = {}
    for ka in range(ia - 1, ia + 3):
        if 0 <= ka < na:
            req = ka in (ia, ia + 1)
            key = (ka, ib, req)
            hit = cache.get(key) if cache is not None else None
            if hit is not None:
                c, nx = hit
                EXTRAPOLATED_READS[0] += nx         # 읽기마다 센다(캐시 채움마다가 아니라) — 셈의 뜻 그대로
            else:
                nx0 = EXTRAPOLATED_READS[0]
                col = _Col(val, ka, len(xs_b), ib, req)
                x0, x1 = xs_b[ib], xs_b[ib + 1]
                tb = (xb - x0) / (x1 - x0)
                if tb in (0.0, 1.0) and col[ib + (tb == 1.0)] is not None:
                    rows[ka] = col[ib + (tb == 1.0)]       # 격자선 위 — 오늘의 «무게 0 끝» 규칙(캐시 안 함)
                    continue
                try:
                    c = _coeffs(xs_b, col, ib)
                except CellMissing:
                    c = False                  # 빈 행 — 바깥 보간이 그 행이 필요하면(무게 > 0) 거기서 CellMissing
                if cache is not None:
                    cache[key] = (c, EXTRAPOLATED_READS[0] - nx0)
            if c:
                rows[ka] = _hermite(xb, c)
    return cubic1(xa, xs_a, _Sparse(rows, na), ia)


class _Col:
    """Lazy view of node values along the second axis on one first-axis row (only ib-1 .. ib+2 are read)."""
    __slots__ = ("val", "ka", "n", "ib", "required")

    def __init__(self, val, ka, n, ib, required):
        self.val, self.ka, self.n, self.ib, self.required = val, ka, n, ib, required

    def __len__(self):
        return self.n

    def __getitem__(self, kb):
        if not 0 <= kb < self.n:
            return None
        v = self.val(self.ka, kb)
        if v is not None or (self.required and kb in (self.ib, self.ib + 1)):
            return v                            # 묻는 칸의 모서리(필요한 두 행)는 늘 실제 값 — 없으면 None → CellMissing
        return _extrapolate(self.val, self.ka, kb, self.ib, self.n)


def _extrapolate(val, ka, kb, ib, n):
    """Missing outer stencil node (ka, kb): extend row ka from its real node nearest the query cell (toward ib) along
    that row's PCHIP end slope. Grid spacing is taken as uniform in index for the slope (callers pass the axis)."""
    # 가장 가까운 실제 격자점(양쪽에서 찾고, 같은 거리면 묻는 칸 쪽) — 묻는 자리와 무관하게 정해져야 C¹ 이 선다(감사 e2)
    k = None
    for dist in range(1, n):
        cands = [kb + dist, kb - dist] if kb <= ib else [kb - dist, kb + dist]
        for c in cands:
            if 0 <= c < n and val(ka, c) is not None:
                k = c
                break
        if k is not None:
            break
    if k is None:
        return None
    step = 1 if k > kb else -1                  # kb 에서 실제 점 쪽으로
    y0 = val(ka, k)
    y1 = val(ka, k + step) if 0 <= k + step < n else None
    y2 = val(ka, k + 2 * step) if 0 <= k + 2 * step < n else None
    if y1 is None:
        return y0                               # 한 점뿐 — 평평하게
    d0 = (y1 - y0) / step                       # 바깥(kb) 쪽을 향한 색인당 기울기: 끝 기울기 공식은 안쪽 두 할선에서
    d1 = (y2 - y1) / step if y2 is not None else d0
    m = -_end_slope(1.0, 1.0, -d0, -d1) if step > 0 else _end_slope(1.0, 1.0, d0, d1)
    EXTRAPOLATED_READS[0] += 1
    return y0 + m * (kb - k)


class _Sparse:
    """Row results keyed by first-axis index; absent rows read as None."""
    __slots__ = ("d", "n")

    def __init__(self, d, n):
        self.d, self.n = d, n

    def __len__(self):
        return self.n

    def __getitem__(self, k):
        return self.d.get(k)


def end_slope(xs, ys, right: bool) -> float:
    """PCHIP slope at the first (right=False) or last (right=True) node — for a C¹ linear extension past the table."""
    if len(xs) < 2:
        return 0.0
    if right:
        h0, h1 = xs[-1] - xs[-2], (xs[-2] - xs[-3]) if len(xs) > 2 else None
        d0 = (ys[-1] - ys[-2]) / h0
        if h1 is None:
            return d0
        return _end_slope(h0, h1, d0, (ys[-2] - ys[-3]) / h1)
    h0, h1 = xs[1] - xs[0], (xs[2] - xs[1]) if len(xs) > 2 else None
    d0 = (ys[1] - ys[0]) / h0
    if h1 is None:
        return d0
    return _end_slope(h0, h1, d0, (ys[2] - ys[1]) / h1)


def finite(x) -> bool:
    return x is not None and math.isfinite(x)
