# 연속 용융 적분(ALE 방식의 "exact" 규칙) — 껍질마다 추출 반지름과 고상선 이음매 반지름에서 정확히 나누고, 조각마다 {T > T_sol} 의 정확한 부분 구간을 찾아 φ 를 3점 Gauss–Legendre 로 적분해 V_melt·Σφ dV 를 상태에 연속이게 함(samuel_model.melt_integrals 와 같은 호출 꼴)
"""The ALE mode's melt integrals (D2 note §7.5; f4 rounds 1–8). Same signature and return keys as
samuel_model.melt_integrals, which stays T2's rule.

On the same radial shells (`shells`), each shell [r_a, r_b] is split exactly where it contains the extraction radius
(P = extraction_below_pa) and the solidus seam (P = curves["seam_gpa"]); each piece is then on one solidus branch
(shallow/deep by its midpoint's pressure; low/high line by its midpoint's pressure, the printed lines jump 0.3 K at the
seam). On each piece the melting set {T(r) > T_sol(r)} is found from the sign of g = T − T_sol at the piece's ends, a
sign change bisected (60 steps) to its radius. V_melt adds the exact volume of the melting sub-interval and Σφ dV adds
∫ φ 4π r² dr over it by 3-point Gauss–Legendre, so both are continuous in the state (T_m, T_b, the layer radii,
D_cr). A melting interval lying wholly inside one piece, with both piece ends below the solidus, is not seen (f4
round 7 found none that is not pinned at r_x or the seam)."""
import math

import samuel_model as sm

_GL_X = (-math.sqrt(3.0 / 5.0), 0.0, math.sqrt(3.0 / 5.0))
_GL_W = (5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0)


def solidus_branch(p_gpa: float, shallow: bool, high: bool, *, d_cr: float, d_ref: float, delta_t_sol: float,
                   curves: dict | None = None) -> float:
    """The solidus this rule uses on one piece: the low or high printed line (by the piece's side of the seam), depleted
    when the piece is shallower than the extraction pressure. thermal_ale's event thresholds read the same function
    (r2 S2), so the events sit where this rule's melting set changes."""
    cv = sm._curves(curves)
    if high:
        a_, b_, c_ = cv["high"]
        x_ = p_gpa - cv["seam_gpa"]
        t_sol = a_ + b_ * x_ + c_ * x_ ** 2
    else:
        a_, b_, c_ = cv["low"]
        t_sol = a_ + b_ * p_gpa + c_ * p_gpa ** 2
    if shallow:
        t_sol = sm.depleted_solidus(t_sol, d_cr, d_ref, delta_t_sol)
    return t_sol


def melt_integrals(t_m: float, t_b: float, r_top: float, r_bot: float, pressure_pa, *, d_cr: float, d_ref: float,
                   delta_t_sol: float, extraction_below_pa: float, shells: int, curves: dict | None = None) -> dict:
    out = {"shallow_phi_v": 0.0, "shallow_v": 0.0, "deep_phi_v": 0.0, "deep_v": 0.0}
    span = r_top - r_bot
    cv = sm._curves(curves)
    seam = cv["seam_gpa"]

    def temp(r):
        return t_b + (t_m - t_b) * (r - r_bot) / span

    def sol_liq(r, shallow, high):
        p_gpa = pressure_pa(r) / 1e9
        return (solidus_branch(p_gpa, shallow, high, d_cr=d_cr, d_ref=d_ref, delta_t_sol=delta_t_sol, curves=curves),
                sm.liquidus(p_gpa, curves))

    def bisect_root(f, a, b, fa):
        for _ in range(60):
            m = 0.5 * (a + b)
            fm = f(m)
            if (fm > 0) == (fa > 0):
                a, fa = m, fm
            else:
                b = m
        return 0.5 * (a + b)

    def add(a, b, shallow, high):
        if b <= a:
            return
        g = lambda r: temp(r) - sol_liq(r, shallow, high)[0]  # noqa: E731
        ga, gb = g(a), g(b)
        if ga > 0 and gb > 0:
            lo, hi = a, b
        elif ga <= 0 and gb <= 0:
            return
        else:
            x = bisect_root(g, a, b, ga)
            lo, hi = (a, x) if ga > 0 else (x, b)
        if hi <= lo:
            return
        c, hw = 0.5 * (lo + hi), 0.5 * (hi - lo)
        pv = 0.0
        for xx, w in zip(_GL_X, _GL_W):
            r = c + hw * xx
            t_sol, t_liq = sol_liq(r, shallow, high)
            pv += w * sm.melt_fraction(temp(r), t_sol, t_liq) * 4.0 * math.pi * r ** 2
        key = "shallow" if shallow else "deep"
        out[key + "_v"] += 4.0 * math.pi / 3.0 * (hi ** 3 - lo ** 3)
        out[key + "_phi_v"] += pv * hw

    dr = span / shells
    for k in range(shells):
        a, b = r_bot + k * dr, r_bot + (k + 1) * dr
        cuts = [a, b]
        for p_cut in (extraction_below_pa, seam * 1e9):
            pa_, pb_ = pressure_pa(a) - p_cut, pressure_pa(b) - p_cut
            if (pa_ > 0) != (pb_ > 0):
                cuts.append(bisect_root(lambda r, pc=p_cut: pressure_pa(r) - pc, a, b, pa_))
        cuts.sort()
        for lo_, hi_ in zip(cuts, cuts[1:]):
            mid = 0.5 * (lo_ + hi_)
            p_mid = pressure_pa(mid)
            add(lo_, hi_, p_mid < extraction_below_pa, p_mid / 1e9 > seam)
    return out
