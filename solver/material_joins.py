# 출처 잇기 계산 — 교차 확인의 띠(선언 격자의 최대 |Δρ|/ρ)와 노드별 r = |Δρ|/σ_allow, σ 전파 (phase-2 impl notes 3–4)
"""Joining two sources inside one phase (rewrite/phase2-impl.frozen.md notes 3 A1–A3, A7 and 4).

`cross_check(view, phase_index, join)` walks the join's declared sampling grid inside its overlap box (the data-range
intersection, A1) and returns, per node, ρ of the preferred and the other source, |Δρ|/ρ, σ_allow and
r = |Δρ|/σ_allow (A3). The band is max |Δρ|/ρ over the grid (A2: «its mismatch goes into the band at every node»);
nodes with r > k are the ones the record must disclose by name and value.

σ of a source at a state (A3, c8's edits 3–4, note 4 item 4):
- propagated: ρ recomputed with each listed parameter moved by its σ, combined in quadrature (correlation not
  printed: independent, which the record discloses as overstating for K0–K′ fits);
- constant: the stated relative σ;
- not_printed: 0, never a stand-in.
sigma_kind converts to 1σ: ci90 ÷ 1.645, ci95 ÷ 1.960, ci68 and 1sigma ÷ 1. σ_allow = max(σ1, σ2) with shared data,
else √(σ1² + σ2²).
"""
from __future__ import annotations

import copy
import math
from types import MappingProxyType

from solver import stepper as st

TO_1SIGMA = MappingProxyType({"1sigma": 1.0, "ci68": 1.0, "ci90": 1.645, "ci95": 1.960, "not_applicable": 1.0})


def _src(view, pi, sid):
    return next(s for s in view.record["phases"][pi]["sources"] if s["id"] == sid)


def source_sigma(view, pi, sid, p, t) -> float:
    """Relative 1σ of ρ for source `sid` at (P, T)."""
    src = _src(view, pi, sid)
    sg = src["sigma"]
    if sg["kind"] == "not_printed":
        return 0.0
    if sg["kind"] == "constant":
        return float(sg["value"]) / TO_1SIGMA[src["sigma_kind"]]
    from solver import material_view as mv
    base = view.source_density(pi, sid, p, t)
    if isinstance(base, st.Stop):
        return math.nan
    var = 0.0
    for name, s in sg["from"].items():
        rec = mv.thaw_plain(view.record)
        tgt = next(x for x in rec["phases"][pi]["sources"] if x["id"] == sid)
        block = tgt["eos"]["params"] if name in tgt.get("eos", {}).get("params", {}) else tgt.get("thermal_model", {})
        block[name]["value"] = float(block[name]["value"]) + float(s)
        moved = mv.RecordView(rec, view.t_pot).source_density(pi, sid, p, t)
        if isinstance(moved, st.Stop):
            return math.nan
        var += ((moved - base) / base) ** 2
    return math.sqrt(var) / TO_1SIGMA[src["sigma_kind"]]


def cross_check(view, pi, join) -> dict:
    """Walk the join's sampling grid; per node ρ_pref, ρ_other, |Δρ|/ρ, σ_allow, r. Returns {nodes, band, max_r, k}."""
    a, b = join["between"]
    smp = join["sampling"]
    box, dp, dt = smp["box"], float(smp["dp"]), float(smp["dt"])
    k = float(join.get("k", 2.0))
    shared = "shared_data" in join
    nodes = []
    p = float(box["p_min"])
    while p <= float(box["p_max"]) + 1e-9 * dp:
        t = float(box["t_min"])
        while t <= float(box["t_max"]) + 1e-9 * dt:
            ra, rb = view.source_density(pi, a, p, t), view.source_density(pi, b, p, t)
            if isinstance(ra, st.Stop) or isinstance(rb, st.Stop):
                nodes.append({"p": p, "t": t, "stop": True})
            else:
                rel = abs(rb - ra) / ra
                sa, sb = source_sigma(view, pi, a, p, t), source_sigma(view, pi, b, p, t)
                allow = max(sa, sb) if shared else math.sqrt(sa * sa + sb * sb)
                nodes.append({"p": p, "t": t, "rho_a": ra, "rho_b": rb, "rel": rel, "sigma_allow": allow,
                              "r": math.inf if allow == 0.0 else rel / allow})
            t += dt
        p += dp
    good = [n for n in nodes if "rel" in n]
    return {"nodes": nodes, "band": max((n["rel"] for n in good), default=math.nan),
            "max_r": max((n["r"] for n in good), default=math.nan), "k": k,
            "over_k": [(n["p"], n["t"], n["r"]) for n in good if n["r"] > k]}
