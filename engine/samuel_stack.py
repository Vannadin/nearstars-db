# 샘유얼 판(화성) 재현용 층 목록을 samuel_thermal 값으로 짓는 곳 — 층 적분기는 칸만 읽는다 (ⓐ2)
"""The Samuel plates' layer stacks, filled from `samuel_thermal` (pre-registration `prereg-a2-stack-params.md`).

`thermal_stack` reads every value from the stack's slots; this module is the one place those slots are filled
from the Mars papers' constants. Moved here unchanged from `thermal_stack` (ⓐ2) — the values are bit-identical.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import samuel_layer as lay             # noqa: E402
import samuel_model as sm              # noqa: E402
import samuel_thermal as st            # noqa: E402
from thermal_stack import Layer, Stack  # noqa: E402

#: the plates' age, Gyr — was `thermal_stack.AGE_GYR`
AGE_GYR = 4.5


#: the two reproduction targets' constants — the same bundles as `samuel_run.MODELS`
MODELS = {
    "no_bml": dict(eta0=st.ETA0_NO_BML_PA_S, e_star=st.E_STAR_NO_BML_J_PER_MOL, v_star=st.V_STAR_NO_BML_M3_PER_MOL,
                   r_c=st.R_CORE_NO_BML_M, t_c0=st.T_CORE_0_NO_BML_K, t_m0=st.T_MANTLE_0_NO_BML_K),
    "bml": dict(eta0=st.ETA0_PA_S, e_star=st.E_STAR_J_PER_MOL, v_star=st.V_STAR_M3_PER_MOL,
                r_c=st.R_CORE_M, t_c0=st.T_CORE_0_K, t_m0=st.T_MANTLE_0_K),
}


def samuel_stack(*, lam: float, profile, g: float, model: str = "no_bml", layer: dict | None = None,
                 eps_mode: str = "derived", p_m_mode: str = "mid", melt_pressure: str = "engine",
                 stefan_mode: str = "printed", lid_mode: str = "grid", lid_nodes: int = 41,
                 melt_shells: int = 1920, fixed_lid_m: float | None = None, delta_b_cap_fraction: float = 0.5,
                 root_branch: str = "nearest", path_check_every: int = 0, r_c: float | None = None,
                 source_volume: bool = False, source_lid_heat: bool = False) -> Stack:
    """The stacks of plates 2 · 2P (no layer) and 4 · 4P (basal layer) — `samuel_run.Setup`'s arguments,
    as layers. `layer` with D_d = 0 is no layer (B1). `r_c` overrides the bundle's core radius.

    Source-form switches (prereg-source-form-plates, frozen d9d5af99), both off = T2's bit reproduction:
    `source_volume` — the mantle balance over the convective volume as 2021 PDF p. 11 prints it («Vm is
    the volume of the convective mantle»), not plate 2's whole silicate (C113; grade literature);
    `source_lid_heat` — in a layered stack the lid grid's heat is split like the mantle's, eq. (1) first
    and the crust share from V_sil′ (C114; grade our inference — v2-22 ② calls that step our reading)."""
    m = MODELS[model]
    rc = m["r_c"] if r_c is None else r_c
    layer = layer if layer and layer["d_d"] != 0.0 else None
    core = Layer("core", "lumped", 0.0, rc, {"t0": m["t_c0"], "inner_core": None, "rho": st.RHO_CORE_KG_M3,
                                              "cp": st.CP_CORE_J_PER_KG_K, "epsilon": st.EPSILON_CORE})
    layers = [core]
    if layer is not None:
        basal = dict(layer)
        basal.setdefault("rho_d", lay.layer_density(basal["fe_mean"]))
        basal.setdefault("fe_m", lay.FE_M)
        basal.setdefault("shift_k", lay.FE_SHIFT_K)
        layers.append(Layer("basal", "conductive", rc, rc + layer["d_d"], basal))
    mantle = Layer("mantle", "convective", None, None,
                   {"t0": m["t_m0"], "eta0": m["eta0"], "e_star": m["e_star"], "v_star": m["v_star"],
                    "volume": "convective" if (layer is not None or source_volume) else "silicate",
                    "bottom": "tbl" if layer is None else "grid_flux+jump",
                    "rho": st.RHO_MANTLE_KG_M3, "cp": st.CP_MANTLE_J_PER_KG_K, "k": st.K_MANTLE_W_PER_M_K,
                    "alpha": st.ALPHA_SILICATE_PER_K, "latent": st.L_MANTLE_J_PER_KG})
    layers.append(mantle)
    layers.append(Layer("lid", "conductive", None, st.R_PLANET_M,
                        {"nodes": lid_nodes, "fixed_m": fixed_lid_m, "crust_lambda": lam,
                         "source_heat": source_lid_heat, "rho_crust": st.RHO_CRUST_KG_M3,
                         "cp_crust": st.CP_CRUST_J_PER_KG_K, "k_crust": st.K_CRUST_W_PER_M_K}))
    return Stack(layers, profile=profile, g=g,
                 options=dict(eps_mode=eps_mode, p_m_mode=p_m_mode, melt_pressure=melt_pressure,
                              stefan_mode=stefan_mode, lid_mode=lid_mode, melt_shells=melt_shells,
                              delta_b_cap_fraction=delta_b_cap_fraction, root_branch=root_branch,
                              path_check_every=path_check_every,
                              a_rh=st.A_RH, ra_critical=st.RA_CRITICAL, beta_u=st.BETA_U, u0=st.U0_M_PER_S,
                              ra_delta_b=(st.RA_DELTA_B_COEFF, st.RA_DELTA_B_EXP), t_ref=st.T_REF_K,
                              p_ref=st.P_REF_PA, r_gas=st.R_GAS_J_PER_MOL_K,
                              hydrostatic_rho=st.RHO_MANTLE_KG_M3, hydrostatic_g=3.7),
                 body=dict(t_surface=st.T_SURFACE_K, age_gyr=AGE_GYR, t_initial_gyr=st.T_INITIAL_ROW_GYR,
                           concentration=sm.plate_concentration(), curves=sm.plate_curves(),
                           melt_extraction_below_pa=st.MELT_EXTRACTION_BELOW_PA, delta_t_sol=st.DELTA_T_SOL_K,
                           crust_reference_fraction=0.2))
