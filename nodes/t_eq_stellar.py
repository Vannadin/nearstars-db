# 평형온도 노드 계산 — 호스트 광도·장반경·이심률·본드 반사율에서 궤도 평균 입사량과 평형온도 (교과서 항등식, 밴드는 입력 모서리 평가)
"""`t_eq_stellar` (spec nodes/t_eq_stellar.yaml; registration prereg-t-eq-stellar.frozen.md §1 C3).

    S    = Σ_hosts L / (4 π a² √(1 − e²))          orbit-averaged instellation
    T_eq = (S (1 − A) / (4 σ))^¼                   full redistribution, emissivity 1

Both are exact identities, so the method adds no degradation (method_grade measured) and the band is the inputs'
printed bands carried through: S and T_eq are monotone in each input (up in L and e, down in a and A), so the
extremes sit at the corners. The host list holds the body's own host only in this registration; companions in the
system are named in a `companion_hosts_not_combined` note by the caller, not summed.
"""
from __future__ import annotations

import math

SIGMA = 5.670374419e-8   # W m^-2 K^-4, CODATA 2018 (exact in SI)


def s_inst(l, a, e):
    return l / (4.0 * math.pi * a * a * math.sqrt(1.0 - e * e))


def t_eq(s, albedo):
    return (s * (1.0 - albedo) / (4.0 * SIGMA)) ** 0.25


def _lims(q):
    if q.band is None:
        return q.point, q.point
    return q.band.lo, q.band.hi


def compute(ctx):
    hosts = ctx.read("l_host")
    a, e, alb = ctx.read("a"), ctx.read("e"), ctx.read("albedo")
    l_pt = sum(q.point for q in hosts)
    l_lo = sum(_lims(q)[0] for q in hosts)
    l_hi = sum(_lims(q)[1] for q in hosts)
    a_lo, a_hi = _lims(a)
    e_lo, e_hi = _lims(e)
    e_lo, e_hi = max(e_lo, 0.0), min(e_hi, math.nextafter(1.0, 0.0))
    al_lo, al_hi = _lims(alb)
    al_lo, al_hi = max(al_lo, 0.0), min(al_hi, 1.0)
    s = s_inst(l_pt, a.point, e.point)
    s_lo, s_hi = s_inst(l_lo, a_hi, e_lo), s_inst(l_hi, a_lo, e_hi)
    t = t_eq(s, alb.point)
    t_lo, t_hi = t_eq(s_lo, al_hi), t_eq(s_hi, al_lo)
    return {"s_inst": (s, s_lo, s_hi), "t_eq": (t, t_lo, t_hi)}, []
