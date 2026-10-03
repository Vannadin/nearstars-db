# 암석체의 뚜껑 체제를 한 규칙으로 정한다 — 선언이 이기고, 열 파이프 판정과 Korenaga 판구조 판정, 이름 댄 거절 (C158)
"""One rule decides a rocky body's lid regime (prereg-c158-lid-regime, frozen a4310e84).

    resolve(declared, h_min_w_m2, t_p_k, t_s_k, g, h_m, lid_friction, variant) -> dict

- R1 declared wins: a `tectonic_regime` declaration is the regime; the computed tests below only add a
  named note where they disagree («declaration vs physics»). Pandora's note is the owner's setting override.
- R3 heat-pipe test: H_min (radiogenic + tidal surface flux, a LOWER bound) against the largest
  stagnant-lid convective capacity q_SL,max over T_p ∈ [declared T_p, the 1-bar silicate liquidus].
  H_min > q_SL,max ⇒ heat pipe; otherwise this test says nothing (a lower bound below a threshold proves nothing).
- R4 Korenaga 2010 test, as O'Rourke & Korenaga 2012 eqs (14)–(18) print it:
  Δη_L = exp(0.327 γ^0.647 θ_tot), γ = μ/(α(T_u − T_s)), θ_tot = E(T_u − T_s)/(R T_u²);
  plate tectonics possible if Δη_L ≤ 0.25 Ra_i,tot^½, Ra_i,tot = α ρ g (T_u − T_s) h³ / (κ η(T_u)).
  μ is the declared `lid_friction` {low, high, basis: dry | water-weakened, grade, source}; Δη_L rises with μ,
  so a μ range gives «plate favoured» / «stagnant favoured» / «undetermined — μ_crit = X».
- R5 order for an undeclared body: R3, then R4, then the named refusal.
Constants (α, ρ, κ, E, η(T)) are `mantle_budget`'s (Foley 2018 Table 1 / Korenaga 2009), Earth-calibrated.
"""
from __future__ import annotations

import math

import eos
import mantle_budget as mb

#: O'Rourke & Korenaga 2012 eqs (15), (17) — the printed coefficients.
A_GAMMA, B_GAMMA, CRIT_COEFF = 0.327, 0.647, 0.25
#: Korenaga 2010's own run range (307 runs): γ 0.1–1, θ up to ~20 — printed beside a verdict outside it.
GAMMA_RUN, THETA_RUN_MAX = (0.1, 1.0), 20.0
#: the hot-surface caveat (Foley & Bercovici 2014 give the opposite sign of T_s).
HOT_SURFACE_K = 600.0
BASES = ("dry", "water-weakened")

UNDECLARED_REFUSAL = ("lid regime undetermined — declare `lid_friction` (μ, with its dry / water-weakened basis) "
                      "or `tectonic_regime` (C158)")
NO_MU_NOTE = "R4 not run — no `lid_friction` (μ) declared; the regime is declared (C158 R1)"
NO_TS_REFUSAL = "lid regime undetermined — declare `surface_temperature_k` (R4 reads it; C158)"
MAGMA_OCEAN_REFUSAL = "above the 1-bar liquidus — no subsolidus lid (C158 R3)"
#: Pandora — the owner's wording (2026-10-03), as a template with computed fields (prereg §3 Q2).
OVERRIDE_NOTE = ("physics says heat pipe (tidal {h:.0f} W/m², {ratio:.0f}× the max stagnant-lid capacity); "
                 "owner setting override: mobile lid")


def q_sl(t_p_k: float, t_s_k: float, h_m: float, g: float) -> float:
    """Stagnant-lid convective flux [W/m²] at T_p — `mantle_budget.f_man_w_m2` (Korenaga 2009 eq. 3)."""
    return mb.f_man_w_m2(t_p_k, t_s_k, h_m, g)


def heat_pipe_test(h_min: float, t_p_k: float, t_s_k: float, g: float, h_m: float,
                   variant: str = "peridotitic") -> dict:
    """R3. q_SL is taken at the top of [T_p, liquidus(1 bar)]; `mono` reports whether q_SL rose on a 20 K scan."""
    t_liq = eos.silicate_liquidus(1e5, variant)
    if t_liq is None:
        return {"verdict": None, "refusal": "no 1-bar liquidus for this composition (C158 R3)"}
    if t_p_k > t_liq:
        return {"verdict": None, "refusal": MAGMA_OCEAN_REFUSAL, "t_liq_k": t_liq}
    grid = [t_p_k + 20.0 * i for i in range(int((t_liq - t_p_k) // 20.0) + 1)] + [t_liq]
    qs = [q_sl(t, t_s_k, h_m, g) for t in grid]
    mono = all(b > a for a, b in zip(qs, qs[1:]))
    q_max = qs[-1] if mono else max(qs)
    out = {"t_liq_k": t_liq, "q_sl_max": q_max, "mono": mono, "ratio": h_min / q_max, "refusal": None}
    out["verdict"] = "heat pipe" if h_min > q_max else None
    return out


def korenaga(mu: float, t_u: float, t_s: float, g: float, h_m: float) -> tuple[float, float]:
    """(Δη_L, Δη_L,crit) at one μ — O'Rourke & Korenaga 2012 eqs (14)–(18)."""
    d_t = t_u - t_s
    gamma = mu / (mb.ALPHA_1_K * d_t)
    theta = mb.E_V_J_MOL * d_t / (mb.R_GAS_J_MOL_K * t_u ** 2)
    ra = mb.ALPHA_1_K * mb.RHO_KG_M3 * g * d_t * h_m ** 3 / (mb.KAPPA_M2_S * mb.viscosity_pa_s(t_u))
    return math.exp(A_GAMMA * gamma ** B_GAMMA * theta), CRIT_COEFF * math.sqrt(ra)


def mu_crit(t_u: float, t_s: float, g: float, h_m: float) -> float:
    """μ at which Δη_L = Δη_L,crit (closed form of eqs 14–18)."""
    d_t = t_u - t_s
    theta = mb.E_V_J_MOL * d_t / (mb.R_GAS_J_MOL_K * t_u ** 2)
    _dl, crit = korenaga(1.0, t_u, t_s, g, h_m)
    if crit <= 1.0:
        return 0.0
    gamma_c = (math.log(crit) / (A_GAMMA * theta)) ** (1.0 / B_GAMMA)
    return gamma_c * mb.ALPHA_1_K * d_t


def korenaga_test(lid_friction: dict | None, t_u: float, t_s: float, g: float, h_m: float) -> dict:
    """R4 over the declared μ range. Without `lid_friction` the verdict is the named refusal; μ_crit is still given."""
    mc = mu_crit(t_u, t_s, g, h_m)
    d_t = t_u - t_s
    theta = mb.E_V_J_MOL * d_t / (mb.R_GAS_J_MOL_K * t_u ** 2)
    out = {"mu_crit": mc, "verdict": None, "refusal": None, "notes": []}
    if t_s >= HOT_SURFACE_K:
        out["notes"].append(f"hot surface (T_s {t_s:.0f} K): Foley & Bercovici 2014 give the opposite sign of T_s "
                            "to Korenaga's form")
    if theta > THETA_RUN_MAX:
        out["notes"].append(f"θ_tot {theta:.1f} is above Korenaga 2010's run range (≲ {THETA_RUN_MAX:g})")
    if not lid_friction:
        out["refusal"] = UNDECLARED_REFUSAL
        return out
    lo, hi = float(lid_friction["low"]), float(lid_friction["high"])
    basis = lid_friction.get("basis")
    if basis not in BASES:
        out["refusal"] = (f"`lid_friction` must state its basis as one of {BASES} (owner Q3, C158); "
                          f"got {basis!r}")
        return out
    for mu in (lo, hi):
        g_ = mu / (mb.ALPHA_1_K * d_t)
        if not GAMMA_RUN[0] <= g_ <= GAMMA_RUN[1]:
            out["notes"].append(f"γ {g_:.3g} at μ {mu:g} is outside Korenaga 2010's run range "
                                f"{GAMMA_RUN[0]:g}–{GAMMA_RUN[1]:g}")
    dl_hi, crit = korenaga(hi, t_u, t_s, g, h_m)
    dl_lo, _ = korenaga(lo, t_u, t_s, g, h_m)
    if dl_hi <= crit:
        out["verdict"] = "plate tectonics favoured (Korenaga 2010; bistability possible — Lenardic 2018)"
    elif dl_lo > crit:
        out["verdict"] = "stagnant lid favoured (Korenaga 2010)"
    else:
        out["verdict"] = f"undetermined across the declared μ range {lo:g}–{hi:g} — μ_crit = {mc:.3f}"
    out["verdict"] += f" [μ basis: {basis}]"
    return out


def resolve(declared: str | None, h_min: float | None, t_p_k: float | None, t_s_k: float | None,
            g: float | None, h_m: float | None, lid_friction: dict | None, override: bool = False,
            variant: str = "peridotitic") -> dict:
    """R1–R5. Returns {value, source, why, heat_pipe, korenaga, notes}."""
    notes: list[str] = []
    pipe = kor = None
    if None not in (h_min, t_p_k, g, h_m):
        # ⚠ q_SL does not depend on T_s: in k ΔT/h · θ^(−4/3) Ra^(1/3) both θ and Ra are ∝ ΔT and the powers cancel
        #   (ΔT^(1 − 4/3 + 1/3) = ΔT⁰). So R3 runs without a declared surface temperature; R4 needs one.
        pipe = heat_pipe_test(h_min, t_p_k, mb.T_S_K if t_s_k is None else t_s_k, g, h_m, variant)
        if t_s_k is None:
            kor = {"mu_crit": None, "verdict": None, "refusal": NO_TS_REFUSAL, "notes": []}
        else:
            kor = korenaga_test(lid_friction, t_p_k, t_s_k, g, h_m)
            notes += kor["notes"]
    if declared:
        if pipe and pipe.get("verdict") == "heat pipe" and declared != "heat_pipe":
            if override:
                notes.append(OVERRIDE_NOTE.format(h=h_min, ratio=pipe["ratio"]))
            else:
                notes.append(f"declaration vs physics: R3 says heat pipe (H {h_min:.3g} W/m², "
                             f"{pipe['ratio']:.0f}× the max stagnant-lid capacity); declared {declared}")
        if kor and kor.get("verdict") and not kor["verdict"].startswith("undetermined"):
            fav = "mobile" if kor["verdict"].startswith("plate") else "stagnant"
            if fav != declared:
                notes.append(f"declaration vs physics: R4 says {kor['verdict']}; declared {declared}")
        if kor and kor.get("refusal") == UNDECLARED_REFUSAL:
            kor = {**kor, "refusal": NO_MU_NOTE}      # 선언된 몸에 «선언하라» 는 틀린 말이다 — R4 가 안 돌았을 뿐
        src = "declared (owner setting override)" if override else "declared"
        return {"value": declared, "source": src, "why": f"declared tectonic_regime «{declared}» (C158 R1)",
                "heat_pipe": pipe, "korenaga": kor, "notes": notes}
    if pipe and pipe.get("refusal"):
        return {"value": None, "source": "undetermined", "why": pipe["refusal"], "heat_pipe": pipe,
                "korenaga": kor, "notes": notes}
    if pipe and pipe.get("verdict") == "heat pipe":
        return {"value": "heat_pipe", "source": "derived",
                "why": f"R3: H {h_min:.3g} W/m² > max stagnant-lid capacity {pipe['q_sl_max']:.3g} W/m² "
                       f"({pipe['ratio']:.0f}×, T_p up to the 1-bar liquidus {pipe['t_liq_k']:.0f} K)",
                "heat_pipe": pipe, "korenaga": kor, "notes": notes}
    if kor and kor.get("verdict") and not kor["verdict"].startswith("undetermined"):
        value = "mobile" if kor["verdict"].startswith("plate") else "stagnant"
        return {"value": value, "source": "derived", "why": f"R4: {kor['verdict']}", "heat_pipe": pipe,
                "korenaga": kor, "notes": notes}
    why = (kor or {}).get("refusal") or (kor or {}).get("verdict") or UNDECLARED_REFUSAL
    return {"value": None, "source": "undetermined", "why": why, "heat_pipe": pipe, "korenaga": kor,
            "notes": notes}
