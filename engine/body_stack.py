# 몸 파일의 선언에서 층 적분기 Stack 을 짓는 곳 — 없는 칸은 이름 대고 거절, 판 이동 몸은 밖 (ⓐ1)
"""Build a `thermal_stack.Stack` from a body file (pre-registration `prereg-a1-body-stack.md`, frozen ea6000e1).

    import body_stack
    s = body_stack.body_stack(Path("bodies/mars.yaml"), crust_lambda=10.0)

Where each slot comes from (§1 of the pre-registration):
  structure  — pressure profile, surface gravity, core and planet radii, and the core density (derived: the
               core's mass over its volume, grade derived);
  body file  — age, surface temperature, radiogenic concentrations, initial temperatures, and the new
               `thermal_evolution:` block (each field value · grade · source · counter_evidence_searched);
  the model  — Samuel's constants (a_rh, Ra_c, β_u, u₀, the δ_b law, R, the viscosity reference state, the
               start time), the same for every body;
  run choice — the source-form main plate (decision ⑥): P_m at the upper end, the convective volume, the lid's
               heat split like the mantle's; the rest as `samuel_stack`'s defaults.

A body whose `tectonic_regime` is not `stagnant` is refused by name (decision ①): the layer integrator is a
stagnant-lid model. A missing field is refused by name; nothing is filled silently.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import payload                         # noqa: E402
import samuel_structure as sst         # noqa: E402
import samuel_thermal as st            # noqa: E402
from thermal_stack import Layer, Stack  # noqa: E402

MOBILE_REFUSAL = ("the layer integrator is a stagnant-lid model — a body with moving plates stays outside it "
                  "until the crust-type stage (ⓧ)")

#: every field `thermal_evolution:` must carry, and the three provenance keys each needs (ⓔ1)
FIELDS = {
    "mantle": ("rho", "cp", "k", "alpha", "latent", "eta0", "e_star", "v_star"),
    "crust": ("rho", "cp", "k"),
    "core": ("cp", "epsilon"),
    "melting": ("solidus_seam_gpa", "solidus_low", "solidus_high", "liquidus", "melt_extraction_below_pa",
                "delta_t_sol", "crust_reference_fraction"),
}

#: Samuel's model constants — the model's, not a body's (§2); every body gets the same
MODEL = dict(a_rh=st.A_RH, ra_critical=st.RA_CRITICAL, beta_u=st.BETA_U, u0=st.U0_M_PER_S,
             ra_delta_b=(st.RA_DELTA_B_COEFF, st.RA_DELTA_B_EXP), t_ref=st.T_REF_K, p_ref=st.P_REF_PA,
             r_gas=st.R_GAS_J_PER_MOL_K)
T_INITIAL_GYR = st.T_INITIAL_ROW_GYR

#: the source-form main plate (decision ⑥)
RUN_CHOICE = dict(eps_mode="derived", p_m_mode="top", melt_pressure="engine", stefan_mode="printed",
                  lid_mode="grid", melt_shells=1920, delta_b_cap_fraction=0.5, root_branch="nearest",
                  path_check_every=0, hydrostatic_rho=st.RHO_MANTLE_KG_M3, hydrostatic_g=3.7)
LID_NODES = 41


class Refused(Exception):
    """The body file cannot build a stack — the message names what is missing or why."""


def _val(d, key: str, where: str):
    if key not in d:
        raise Refused(f"`{where}.{key}` is not declared")
    v = d[key]
    return v["value"] if isinstance(v, dict) and "value" in v else v


def _field(block: dict, group: str, key: str):
    g = block.get(group)
    if not isinstance(g, dict) or key not in g:
        raise Refused(f"`thermal_evolution.{group}.{key}` is not declared")
    f = g[key]
    if not isinstance(f, dict) or "value" not in f:
        raise Refused(f"`thermal_evolution.{group}.{key}` has no `value`")
    try:
        payload.check_provenance(f"thermal_evolution.{group}.{key}", f)    # the one grade vocabulary (ⓔ1)
    except ValueError as e:
        raise Refused(str(e)) from None
    v = f["value"]
    num = (int, float)
    if isinstance(v, bool) or not (isinstance(v, num) or (isinstance(v, list) and v and
                                                       all(isinstance(x, num) and not isinstance(x, bool) for x in v))):
        # ⚠ PyYAML reads `6.0e21` (no exponent sign) as a string — refuse rather than carry text into the model
        raise Refused(f"`thermal_evolution.{group}.{key}` value «{v!r}» is not a number")
    return tuple(v) if isinstance(v, list) else v


def _concentration(rc: dict) -> dict:
    return {"U": rc["U_ppb"] * 1e-9, "Th": rc["Th_ppb"] * 1e-9, "K": rc["K_ppm"] * 1e-6}


def read(body_path: Path) -> dict:
    """The body file's slot values, or `Refused` naming the first thing missing. No structure is solved here."""
    doc = yaml.safe_load(Path(body_path).read_text(encoding="utf-8"))
    inp = doc.get("inputs") or {}
    regime = _val(inp, "tectonic_regime", "inputs")
    if regime != "stagnant":
        raise Refused(f"tectonic_regime «{regime}»: {MOBILE_REFUSAL}")
    te = inp.get("thermal_evolution")
    if not isinstance(te, dict):
        raise Refused("`inputs.thermal_evolution` is not declared")
    out = {g: {k: _field(te, g, k) for k in keys} for g, keys in FIELDS.items()}
    # Λ is optional in the file (it is inverted, not fixed, in Samuel's framework): read it only if declared
    crust = te.get("crust") or {}
    out["crust"]["enrichment"] = _field(te, "crust", "enrichment") if "enrichment" in crust else None
    rc = inp.get("radiogenic_concentration")
    if not isinstance(rc, dict):
        raise Refused("`inputs.radiogenic_concentration` is not declared")
    out["body"] = dict(age_gyr=_val(inp, "age_gyr", "inputs"), t_surface=_val(inp, "surface_temperature_k", "inputs"),
                       concentration=_concentration(rc))
    out["t0"] = dict(core=_val(inp, "core_initial_temperature", "inputs"),
                     mantle=_val(inp, "mantle_initial_potential_temperature", "inputs"))
    return out


def body_stack(body_path: Path, *, crust_lambda: float | None = None, profile=None) -> Stack:
    """The stack for `body_path`. The crustal enrichment Λ is the caller's `crust_lambda` if given, else the body
    file's `thermal_evolution.crust.enrichment`, else refused by name (directing, 09-26: an optional body field
    that a run argument overrides). `profile` may be passed to skip re-solving the structure (it must be this
    body's)."""
    v = read(body_path)
    lam = crust_lambda if crust_lambda is not None else v["crust"]["enrichment"]
    if lam is None:
        raise Refused("`thermal_evolution.crust.enrichment` is not declared and no `crust_lambda` was given")
    prof = profile if profile is not None else sst.mars_profile(Path(body_path))   # name only — any body file
    r_p, r_c = prof.radius_m, prof.core_radius_m
    m_core = prof._interp(prof.m, r_c)
    rho_core = m_core / (4.0 / 3.0 * math.pi * r_c ** 3)    # derived: the core's mass over its volume (decision ③)
    M, C, K, L = v["mantle"], v["crust"], v["core"], v["melting"]
    layers = [
        Layer("core", "lumped", 0.0, r_c, {"t0": v["t0"]["core"], "inner_core": None, "rho": rho_core,
                                            "cp": K["cp"], "epsilon": K["epsilon"]}),
        Layer("mantle", "convective", None, None,
              {"t0": v["t0"]["mantle"], "eta0": M["eta0"], "e_star": M["e_star"], "v_star": M["v_star"],
               "volume": "convective", "bottom": "tbl", "rho": M["rho"], "cp": M["cp"], "k": M["k"],
               "alpha": M["alpha"], "latent": M["latent"]}),
        Layer("lid", "conductive", None, r_p,
              {"nodes": LID_NODES, "fixed_m": None, "crust_lambda": lam, "source_heat": True,
               "rho_crust": C["rho"], "cp_crust": C["cp"], "k_crust": C["k"]}),
    ]
    body = dict(v["body"], t_initial_gyr=T_INITIAL_GYR,
                curves={"seam_gpa": L["solidus_seam_gpa"], "low": L["solidus_low"], "high": L["solidus_high"],
                        "liquidus": L["liquidus"]},
                melt_extraction_below_pa=L["melt_extraction_below_pa"], delta_t_sol=L["delta_t_sol"],
                crust_reference_fraction=L["crust_reference_fraction"])
    return Stack(layers, profile=prof, g=prof.gravity(r_p), options=dict(RUN_CHOICE, **MODEL), body=body)
