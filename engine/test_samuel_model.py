# Samuel 층 없는 모형 우변 조각의 시험 — 인쇄식 값 · Ra<Ra_c 분기 · 식 20 부호 · 우리 유도(v2-7)
"""Checks for `samuel_model`, plate 2 first cut. No integration yet: the refused slots stop it.

    python3 engine/test_samuel_model.py

Each check is a property a wrong wiring would break, not a stored number: the lid-base temperature against
a hand evaluation of 2019 SI eq. (4), the `Ra < Ra_c` branch (v2-2 ②), the sign of the lid-base term in
2019 SI eq. (20) (the v2 interpretation, `−`), the energy balance's signs, and the named refusals.
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

# 2019 SI eq. (22) with Λ as H_cr/H_pm (v2-4): total heat is conserved, H_m hits 0 at the ceiling,
# and a Λ above it refuses rather than clipping. The volumes are a 50 km crust on the a–f mantle.
import math                            # noqa: E402
v_sil = 4 / 3 * math.pi * (st.R_PLANET_M ** 3 - st.R_CORE_NO_BML_M ** 3)
v_cr = 4 / 3 * math.pi * (st.R_PLANET_M ** 3 - (st.R_PLANET_M - 50e3) ** 3)
v_m = v_sil - v_cr
h_m, h_cr = sm.heat_split(1e-8, v_cr, v_m, 10.0)
check("2019 SI eq. (22) — H_m V_m + H_cr V_cr = H_pm V_sil", abs((h_m * v_m + h_cr * v_cr) / (1e-8 * v_sil) - 1) < 1e-12,
      f"H_m {h_m:.4g}, H_cr {h_cr:.4g} W/m³")
ceil = sm.crust_enrichment_ceiling(v_cr, v_m)
check("v2-4 ③ — the ceiling is V_sil/V_cr and H_m = 0 there",
      abs(ceil - v_sil / v_cr) < 1e-9 * ceil and abs(sm.heat_split(1e-8, v_cr, v_m, ceil)[0]) < 1e-20,
      f"ceiling {ceil:.2f} for a 50 km crust")
try:
    sm.heat_split(1e-8, v_cr, v_m, ceil * 1.01)
    check("v2-4 ③ — above the ceiling refuses", False, "returned a value")
except sm.Refused as e:
    check("v2-4 ③ — above the ceiling refuses", "ceiling" in str(e), str(e)[:70])
check("2019 SI eq. (15) — no crust, no shift; D_cr = D_ref shifts by ΔT_sol",
      sm.depleted_solidus(1400.0, 0.0, 1e5, st.DELTA_T_SOL_K) == 1400.0
      and sm.depleted_solidus(1400.0, 1e5, 1e5, st.DELTA_T_SOL_K) == 1550.0)

# The two slots still unbuilt refuse by name, with no value.
# Th and K back in time: at t = 0 the present rate; one half-life back, ⁴⁰K's part doubles.
now = sm.primitive_heat_th_k(0.0, 1.0)
hand = 54e-9 * 2.6368e-5 + 284e-6 * 3.4302e-9
check("Ruedas 2017 — Th + K today by hand", abs(now / hand - 1) < 1e-12, f"{now:.5g} W/kg")
back = sm.primitive_heat_th_k(1248.0, 1.0)
hand_back = 54e-9 * 2.6368e-5 * 2 ** (1248 / 14000) + 284e-6 * 3.4302e-9 * 2
check("Ruedas 2017 — one ⁴⁰K half-life back", abs(back / hand_back - 1) < 1e-12)
# U split by nuclide reproduces the table's element rate today (v2-6 ① 검산), and each nuclide decays alone.
u_now = (sm.primitive_heat(0.0, 1.0) - sm.primitive_heat_th_k(0.0, 1.0)) / 14e-9
check("v2-6 ① — ²³⁵U + ²³⁸U today = U element 9.8314e-5 W/kg", abs(u_now / st.H_U_W_PER_KG - 1) < 5e-5,
      f"{u_now:.6e} W/kg")
u_back = (sm.primitive_heat(704.0, 1.0) - sm.primitive_heat_th_k(704.0, 1.0)) / 14e-9
f235 = 0.0072045 * 235.043928190 / 238.02891 * 5.68402e-4
f238 = 0.9927955 * 238.050786996 / 238.02891 * 9.4946e-5
# The same mass-weighted sum for K, from the ⁴⁰K row of Ruedas 2017 Table 2 (PDF p6, rendered): the atomic
# masses 39.963998166 and 39.0983 and H(⁴⁰K) 2.8761e-5 W/kg are test-only literals, not model inputs.
k_elem = st.X_ISO_K40 * 39.963998166 / 39.0983 * 2.8761e-5
check("v2-6 ① — ⁴⁰K mass-weighted = K element 3.4302e-9 W/kg", abs(k_elem / st.H_K_W_PER_KG - 1) < 5e-5,
      f"{k_elem:.6e} W/kg")
atomic_only = sum(n["x_iso"] * n["h_w_per_kg"] for n in (st.U235, st.U238))
check("v2-6 ① — atomic fractions alone miss by ~0.04 % (why the mass weight is there)",
      3e-4 < atomic_only / st.H_U_W_PER_KG - 1 < 6e-4, f"{atomic_only:.6e} W/kg")
check("v2-6 ① — one ²³⁵U half-life back, by hand", abs(u_back / (2 * f235 + f238 * 2 ** (704 / 4468)) - 1) < 1e-12)

# 2023 SI eq. (9): the seam goes to the first line, the gap there is 0.3 K (v2-5 ②), and T_liq > T_sol.
check("2023 SI eq. (9) — solidus at 10 GPa is the first line, 2075.3 K", abs(sm.solidus(10.0) - 2075.3) < 1e-9)
check("2023 SI eq. (9) — just above the seam, the second line (≈ 2075 K)", abs(sm.solidus(10.0 + 1e-9) - 2075.0) < 1e-6)
check("2023 SI eq. (9) — liquidus above solidus from 0 to 25 GPa",
      all(sm.liquidus(p / 2) > sm.solidus(p / 2) for p in range(0, 51)),
      f"at 0 GPa {sm.solidus(0):.1f} / {sm.liquidus(0):.1f} K")
check("2021 eq. (9) — melt fraction clamps to [0, 1]",
      sm.melt_fraction(1000, 1400, 2000) == 0.0 and sm.melt_fraction(2500, 1400, 2000) == 1.0
      and sm.melt_fraction(1700, 1400, 2000) == 0.5)

# v2-7 ① — ϵ_m of an isothermal mantle is 1, and a mantle hotter at depth gives ϵ_m > 1, below T_b/T_m.
r_top, r_bot = st.R_PLANET_M - 300e3, st.R_CORE_NO_BML_M + 100e3
check("v2-7 ① — ϵ_m = 1 when T_b = T_m", abs(sm.mantle_mean_ratio(1700, 1700, r_top, r_bot) - 1) < 1e-12)
eps = sm.mantle_mean_ratio(1700, 1900, r_top, r_bot)
check("v2-7 ① — 1 < ϵ_m < T_b/T_m, and below the radial mean (the shell weights the top)",
      1 < eps < 1900 / 1700 and eps < (1700 + 1900) / 2 / 1700, f"ϵ_m {eps:.5f}")

# v2-7 ④ with the supplement's hydrostatic profile — melting only where the adiabat crosses the solidus,
# and the Stefan number is ≥ 0 and grows with a hotter mantle.
def hydro(r):
    return sm.hydrostatic_pressure(r, rho_m=3500.0, g=3.7, r_p=st.R_PLANET_M)
kw = dict(d_cr=0.0, d_ref=sm.crust_reference_thickness(st.R_PLANET_M, st.R_CORE_NO_BML_M),
          delta_t_sol=st.DELTA_T_SOL_K, extraction_below_pa=st.MELT_EXTRACTION_BELOW_PA, shells=400)
cold = sm.melt_integrals(1300, 1400, r_top, r_bot, hydro, **kw)
hot = sm.melt_integrals(1900, 2000, r_top, r_bot, hydro, **kw)
check("v2-7 ④ — a 1300 K mantle does not melt; a 1900 K one melts in the shallow zone",
      cold["shallow_phi_v"] == cold["deep_phi_v"] == 0.0 and hot["shallow_phi_v"] > 0,
      f"hot shallow ∫φdV {hot['shallow_phi_v']:.3g} m³")
v_m = 4 / 3 * math.pi * (r_top ** 3 - r_bot ** 3)
stk = dict(v_m=v_m, l_m=st.L_MANTLE_J_PER_KG, c_m=st.CP_MANTLE_J_PER_KG_K, dt_k=1.0, **kw)
s_cold = sm.stefan_number(1300, 1400, r_top, r_bot, hydro, **stk)
s_hot = sm.stefan_number(1900, 2000, r_top, r_bot, hydro, **stk)
s_tot = sm.stefan_number_total(1900, 2000, r_top, r_bot, hydro, **stk)
check("2019 SI PDF p6 printed St — 0 without melt; at T_m 1900 (hydrostatic) 0.09369 (v2-8)",
      s_cold == 0.0 and abs(s_hot - 0.09369) < 5e-6, f"St {s_hot:.5f}")
check("comparison St, total derivative — 0.2004 at the same input (v2-8)", abs(s_tot - 0.2004) < 5e-5,
      f"St {s_tot:.5f}")
kw_dep = dict(kw, d_cr=kw["d_ref"])
dep = sm.melt_integrals(1900, 2000, r_top, r_bot, hydro, **kw_dep)
check("2019 SI eq. (15) — a depleted solidus melts less in the shallow zone, deep unchanged",
      dep["shallow_phi_v"] < hot["shallow_phi_v"] and dep["deep_phi_v"] == hot["deep_phi_v"])

print(f"  test_samuel_model — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
