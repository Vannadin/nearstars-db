# Samuel 층 없는 모형 우변 조각의 시험 — 인쇄식 값 · Ra<Ra_c 분기 · 식 20 부호 · 거절 셋
"""Checks for `samuel_model`, plate 2 first cut. No integration yet: the three refused slots stop it.

    python3 engine/test_samuel_model.py

Each check is a property a wrong wiring would break, not a stored number: the lid-base temperature against
a hand evaluation of 2019 SI eq. (4), the `Ra < Ra_c` branch (v2-2 ②), the sign of the lid-base term in
2019 SI eq. (20) (the v2 interpretation, `−`), the energy balance's signs, and the three named refusals.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import samuel_model as sm              # noqa: E402
import samuel_thermal as st            # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


# 2019 SI eq. (4) at the a–f initial mantle temperature, by hand: 2.54 · 8.31 · T_m² / 300e3.
t_m0 = st.T_MANTLE_0_NO_BML_K
t_l = sm.lid_base_temperature(t_m0, st.E_STAR_NO_BML_J_PER_MOL, st.A_RH, st.R_GAS_J_PER_MOL_K)
hand = t_m0 - 2.54 * 8.31 * t_m0 ** 2 / 300.0e3
check("2019 SI eq. (4) — T_l at the a–f T_m0", abs(t_l - hand) < 1e-9, f"T_l {t_l:.4f} K, drop {t_m0 - t_l:.4f} K")

# The viscosity equals η₀ at the reference state, whatever E* and V* are.
eta_ref = sm.viscosity(st.T_REF_K, st.P_REF_PA, st.ETA0_NO_BML_PA_S, st.E_STAR_NO_BML_J_PER_MOL,
                       st.V_STAR_NO_BML_M3_PER_MOL, st.T_REF_K, st.P_REF_PA, st.R_GAS_J_PER_MOL_K)
check("2019 SI eq. (1) — η(T_ref, P_ref) = η₀", abs(eta_ref / st.ETA0_NO_BML_PA_S - 1.0) < 1e-12)

# Ra < Ra_c zeroes q_m and δ_u; above it, both are positive. The same geometry, two viscosities.
geo = dict(rho_m=st.RHO_MANTLE_KG_M3, alpha=st.ALPHA_SILICATE_PER_K, g=3.7, k_m=st.K_MANTLE_W_PER_M_K,
           c_pm=st.CP_MANTLE_J_PER_KG_K, r_p=st.R_PLANET_M, d_l=100e3, r_c=st.R_CORE_NO_BML_M,
           ra_c=st.RA_CRITICAL, beta_u=st.BETA_U)
t_c0 = st.T_CORE_0_NO_BML_K
low = sm.upper_layer(t_m0, t_l, t_c0, t_m0 + 100.0, 1e40, **geo)
high = sm.upper_layer(t_m0, t_l, t_c0, t_m0 + 100.0, 1e20, **geo)
check("v2-2 ② — Ra < Ra_c sets q_m = δ_u = 0", low["subcritical"] and low["q_m"] == 0.0 and low["delta_u"] == 0.0,
      f"Ra {low['ra']:.3g}")
check("above Ra_c, q_m > 0 and 0 < δ_u < R_l − R_c", not high["subcritical"] and high["q_m"] > 0
      and 0 < high["delta_u"] < st.R_PLANET_M - 100e3 - st.R_CORE_NO_BML_M, f"Ra {high['ra']:.3g}")

# 2019 SI eq. (20): with everything else zero, a positive lid-base gradient must thin the lid (the `−`).
lid = dict(q_m=0.0, d_cr_rate=0.0, t_m=t_m0, t_l=t_l, t_s=st.T_SURFACE_K, rho_m=st.RHO_MANTLE_KG_M3,
           c_m=st.CP_MANTLE_J_PER_KG_K, rho_cr=st.RHO_CRUST_KG_M3, l_m=st.L_MANTLE_J_PER_KG,
           k_m=st.K_MANTLE_W_PER_M_K)
check("2019 SI eq. (20) — last term wired `−` (v2 interpretation)",
      sm.lid_rate(lid_base_gradient=1e-3, **lid) < 0 and sm.lid_rate(lid_base_gradient=-1e-3, **lid) > 0)
check("2019 SI eq. (20) — a larger q_m thins the lid", sm.lid_rate(lid_base_gradient=0.0, **{**lid, "q_m": 0.02}) < 0)

# 2021 eqs (10)–(11): heat leaving the core warms the mantle and cools the core.
core = sm.core_rate(q_c=0.01, rho_c=st.RHO_CORE_KG_M3, c_pc=st.CP_CORE_J_PER_KG_K, v_c=1.0, eps_c=st.EPSILON_CORE, a_c=1.0)
mant = sm.mantle_rate(q_m=0.0, q_c=0.01, h_m=0.0, d_cr_rate=0.0, t_m=t_m0, t_l=t_l, stefan=0.0, eps_m=1.0,
                      rho_m=st.RHO_MANTLE_KG_M3, c_pm=st.CP_MANTLE_J_PER_KG_K, v_m=1.0, a_m=1.0, a_c=1.0,
                      rho_cr=st.RHO_CRUST_KG_M3, l_m=st.L_MANTLE_J_PER_KG, c_pcr=st.CP_CRUST_J_PER_KG_K)
check("2021 eqs (10)–(11) — q_c > 0 cools the core and warms the mantle", core < 0 < mant)

# The three slots refuse by name, with no value.
for fn, word in ((sm.lid_base_gradient, "lid"), (sm.heat_production, "H_m"), (sm.melt_state, "melt")):
    try:
        fn()
        check(f"refusal — {fn.__name__}", False, "returned a value")
    except sm.Refused as e:
        check(f"refusal — {fn.__name__}", word in str(e), str(e)[:70])

print(f"  test_samuel_model — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
