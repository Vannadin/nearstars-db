# 녹는 곡선 이음매 완결성 시험 — 고상선 · 액상선 · 창 안 dT/dP 를 훑어 찾은 값/기울기 이음매가 eos.melt_curve_seams(와 상 경계)뿐인가
"""python3 engine/test_melt_seams.py — window-edge registration (frozen 59bee405) §4 E6.

Scans silicate_solidus and silicate_liquidus (peridotitic, chondritic) and the in-window adiabatic dT/dP at φ 0.02 / 0.5
/ 0.98 from 1 bar to 500 GPa on a log grid (2e5 points for the curves; 2e4 for the dT/dP scan, whose
measured floor — a relative step of 0.27–0.29 % — is that grid's: note 1 §5b, amendment declared with the code). A cell is a candidate when its |second difference| exceeds 20× the median of
its 50 neighbouring cells (and a round-off floor of 1e-12·|y|); each candidate is bisected to 1e-9·P and classified as a
value seam (|Δy| at ±1e-9·P > 1e-6 K, or 1e-6 relative for dT/dP), a slope seam (one-sided slopes over 1e-6·P differ by
> 1e-3 relative), or dropped. Every seam found must lie within 1e-6 relative of eos.melt_curve_seams() (the curves) or of
that set ∪ the material's own phase bounds (the dT/dP scan, which reads the solid part too), and every listed seam must
be found. Positive controls: the known seams (20 slope, 140 value both variants, the Deng crossing ≈ 173.6 slope;
23.83 GPa in the dT/dP scan) and a planted 1 K step and 1 % kink; negative controls: a smooth curve, and 200 GPa (no
longer a seam: Deng ppv runs to 500 GPa, owner 2026-10-19 — a seam found there is an «extra»).
"""
from __future__ import annotations

import math
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eos  # noqa: E402
import interior  # noqa: E402

P_LO, P_HI = 1.0e5, 500e9
N_GRID = int(sys.argv[1]) if len(sys.argv) > 1 else 200_000
fails: list[str] = []


def ok(cond: bool, msg: str) -> None:
    print(f"  [{'PASS' if cond else 'FAIL'}] {msg}")
    if not cond:
        fails.append(msg)


def grid(n: int) -> list[float]:
    a, b = math.log(P_LO), math.log(P_HI * (1 - 1e-12))
    return [math.exp(a + (b - a) * i / (n - 1)) for i in range(n)]


def find_seams(f, n: int = N_GRID, value_tol: float = 1e-6, relative: bool = False) -> list[tuple[float, str]]:
    """The seams of f over the log grid: (P, 'value' | 'slope')."""
    ps = grid(n)
    ys = [f(p) for p in ps]
    d2 = [abs(ys[i + 1] - 2.0 * ys[i] + ys[i - 1]) for i in range(1, n - 1)]
    found: list[tuple[float, str]] = []
    i = 0
    while i < len(d2):
        lo, hi = max(0, i - 25), min(len(d2), i + 26)
        med = statistics.median(d2[lo:hi])
        if d2[i] > 20.0 * med and d2[i] > 1e-12 * max(1.0, abs(ys[i + 1])):
            a, b = ps[i], ps[i + 2]                    # the cell around grid point i+1
            x = _locate(f, a, b)
            kind = _classify(f, x, value_tol, relative)
            if kind and not any(abs(x - y) <= 1e-6 * y for y, _k in found):
                found.append((x, kind))
            i += 3
        else:
            i += 1
    return found


def _defect(f, a: float, b: float) -> float:
    """|f(m) − chord(m)| at the geometric midpoint m of [a, b]: O(width·Δslope) over a kink, O(Δy) over a step, O(width²)
    over smooth curvature."""
    m = math.sqrt(a * b)
    w = (m - a) / (b - a)
    return abs(f(m) - (f(a) + w * (f(b) - f(a))))


def _locate(f, a: float, b: float) -> float:
    """Bisect [a, b] toward the seam: keep the half with the larger chord defect, down to 1e-9·P."""
    for _ in range(200):
        if b - a <= 1e-9 * a:
            break
        m = math.sqrt(a * b)
        a, b = (a, m) if _defect(f, a, m) >= _defect(f, m, b) else (m, b)
    return math.sqrt(a * b)


def _classify(f, x: float, value_tol: float, relative: bool) -> str | None:
    e, d = 1e-9 * x, 1e-6 * x
    lo, hi = f(x - e), f(x + e)
    sl = (f(x - e) - f(x - d)) / (d - e)
    sr = (f(x + d) - f(x + e)) / (d - e)
    # the jump net of the curve's own slope over ±e (a smooth dT/dP of 1e-8 K/Pa moves 2e-6 K over ±1e-9·100 GPa)
    jump = abs(hi - lo - 0.5 * (sl + sr) * 2.0 * e)
    if jump > (value_tol * max(1e-300, abs(lo)) if relative else value_tol):
        return "value"
    if abs(sr - sl) > 1e-3 * max(abs(sl), abs(sr), 1e-300):
        return "slope"
    return None


def near(x: float, ys) -> bool:
    return any(abs(x - y) <= 1e-6 * y for y in ys)


def check(name: str, found, allowed, required) -> None:
    extra = [(round(x / 1e9, 6), k) for x, k in found if not near(x, allowed)]
    missing = [round(y / 1e9, 6) for y in required if not near(y, [x for x, _k in found])]
    ok(not extra and not missing,
       f"{name}: found {[(round(x / 1e9, 4), k) for x, k in found]} GPa — extra {extra}, missing {missing}")


def main() -> int:
    seams = eos.melt_curve_seams()
    print(f"melt_curve_seams: {[round(s / 1e9, 6) for s in seams]} GPa; end {eos.SILICATE_MELT_MAX_PA / 1e9:g} GPa")

    # ── controls ──────────────────────────────────────────────────────────────
    step = lambda p: 1000.0 * math.log(p) + (1.0 if p >= 50e9 else 0.0)            # noqa: E731
    kink = lambda p: 1000.0 * math.log(p) + (0.01 * 1000.0 * math.log(p / 50e9) if p >= 50e9 else 0.0)   # noqa: E731
    smooth = lambda p: 1000.0 * math.log(p) + 3e-9 * p                               # noqa: E731
    check("control: planted 1 K step at 50 GPa", find_seams(step), [50e9], [50e9])
    check("control: planted 1 % kink at 50 GPa", find_seams(kink), [50e9], [50e9])
    check("control: smooth curve", find_seams(smooth), [], [])

    # ── the curves: only melt_curve_seams, and all of them ────────────────────
    old = (eos.MONTEUX_JOIN_PA, eos.SILICATE_ROCK_MAX_PA)          # the hand list at 33a6ac21 (with 500 GPa as an end)
    got = [x for x, _k in find_seams(lambda p: eos.silicate_solidus(p))]
    ok(any(not near(x, old) for x in got), "control: the 33a6ac21 hand list {20, 140} misses a seam the scan finds")
    for v in ("peridotitic", "chondritic"):
        check(f"solidus ({v})", find_seams(lambda p, v=v: eos.silicate_solidus(p, v)), seams, seams)
        check(f"liquidus ({v})", find_seams(lambda p, v=v: eos.silicate_liquidus(p, v)), seams, seams)

    # ── the in-window dT/dP: melt_curve_seams ∪ the material's phase bounds (it reads the solid part too) ─────
    n_dt = max(2000, N_GRID // 10)
    for mat in (eos.SILICATE, eos.SILICATE_CHONDRITIC):
        bounds = sorted({b for ph in mat.phases for b in (ph.p_min, ph.p_max) if 0.0 < b < P_HI})
        allowed = list(seams) + bounds
        for phi in (0.02, 0.5, 0.98):
            v = mat.phases[0].melt_variant

            def dtdp(p, phi=phi, v=v, mat=mat):
                ts, tl = eos.silicate_solidus(p, v), eos.silicate_liquidus(p, v)
                t = ts + phi * (tl - ts)
                return interior._adiabatic_dtdp(mat, p, mat.density(p, t, t), t, t)
            found = find_seams(dtdp, n=n_dt, value_tol=1e-6, relative=True)
            # every seam found is allowed; the 20 GPa join and 23.83 GPa bound must be seen (positive controls)
            # at φ 0.98 the solid part's share is 2 %, so its 23.83 GPa bound sits below the detector (required at φ ≤ 0.5)
            check(f"in-window dT/dP {mat.name} φ {phi}", found, allowed,
                  [eos.MONTEUX_JOIN_PA] + ([eos.SILICATE_EN_TO_PREM] if phi <= 0.5 else []))
    print(f"test_melt_seams: {'OK' if not fails else f'FAIL {len(fails)}'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
