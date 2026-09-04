# 맨틀·핵 결합 열진화 적분기 (C20) — Nimmo+ 2004 식 30·32 를 시간 앞으로 적분해 T_c(t)·T_m(t)·ΔE(t) 를 낸다
"""Core thermal history — the C20 integrator.

Grounding: `docs/reference/internal-heat-luminosity-methodology.md` and Nimmo+ 2004
(`2004GeoJI.156..363N`). Pre-registration and the fixed design: `engine/core-thermal-history-context-notes.md`.

    core   (eq. 30)   Q_R − Q_C = (Q̃_s + Q̃_L + Q̃_g) · dT_c/dt
    mantle (eq. 32)   H_m M_m − Q_M + Q_C = M_m C_pm · dT_h/dt
    Q_C = 4π R_c² F_b  (eqs 37–39, `cmb_flux.bottom_layer`)     Q_M = 4π R_p² F_t  (eqs 34–36, `mantle_flux.implied_flux`)
    T̃_m = r_b · T_m   T_h = r_b^½ · T_m   (eq. 29's form; r_b read from the interior solve at the reference T_pot)

State (T_c, T_m); classical RK4 in time; Nimmo's own 4 Myr step. The Q̃ coefficients come from
`core_energy.core_terms` at unit rate (they are linear in dT_c/dt); the inner core at each step is whatever
`core_energy.inner_core` finds on that step's profile. Entropy production at each step from
`core_entropy.entropy_terms` with the COMPUTED rate, on the four (k × H) corners — the declared-rate axis of
C15's eight corners is what this module computes, so its band is not comparable to C15's.

What this module does not claim: any body's "actual" value (the model is Earth-calibrated: outputs read
"consistent with an Earth-calibrated model"); the short-lived radiogenic pulse (C21, needs t_form); t_form
for anyone. Radiogenic heating here is the long-lived half (K · Th · U) through `radiogenic.history_factor`.

Convergence is pre-registered as the discriminating check: the quantity that must converge is ΔE_min over
the last 3.1 Gyr — not the endpoint T_c — at h, h/2, h/4, with |ΔE_min(h/4) − ΔE_min(h/2)| < 10 % of
|ΔE_min(h/2)| and the same inner-core case at all three steps. A run that fails it reports the step as the
result, not the physics.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cmb_flux as cf            # noqa: E402
import core_energy as ce         # noqa: E402
import core_entropy as cent      # noqa: E402
import mantle_flux as mf         # noqa: E402
import radiogenic as rg          # noqa: E402
from eos import PhaseGap         # noqa: E402
from payload import Result, out_of_domain  # noqa: E402

RECIPE = "internal-heat-luminosity-methodology"
VERSION = "1"
REFS = (
    "docs/reference/internal-heat-luminosity-methodology.md",
    "2004GeoJI.156..363N",      # Nimmo+ 2004 — eqs 29–39 (thermal evolution), §3.2, Tables 2, 4; 4 Myr step (line 419)
    "engine/core-thermal-history-context-notes.md",
)

GYR_S = ce.GYR_S
STEP_MYR = 4.0                      # Nimmo's constant timestep ("a constant timestep of 4 Myr", their line 419)
WINDOW_GYR = 3.1                    # Nimmo's entropy-criteria window: mean and minimum over the last 3.1 Gyr
CONVERGENCE_TOL = 0.10              # pre-registered: |ΔE_min(h/4) − ΔE_min(h/2)| / |ΔE_min(h/2)| < 10 %
K_CORNERS = cf.K_CORE_RANGE         # (30, 70) W/(m K)
H_CORNERS = ce.H_CORE_RANGE         # (0, 1.5e-12) W/kg
ROCKY_ONLY = ("giant", "gas_giant", "ice_giant", "sub_neptune", "brown_dwarf", "star")

NO_INITIAL = ("cannot-say (no initial temperatures declared — core_initial_temperature and "
              "mantle_initial_potential_temperature are the two declarations this integrator adds)")
NO_STRUCTURE = "cannot-say (no interior solution — needs core_radius, cmb_pressure, cmb_temperature, potential_temperature)"
NOT_CONVERGED = "step-not-converged (the step is the result, not the physics — pre-registered branch ⑤ fail)"
CANNOT_SAY_HISTORY = "cannot-say (the four-corner band straddles zero inside the last 3.1 Gyr — C20 built, C15 still cannot say)"
SUSTAINED = "sustained (ΔE_min > 0 over the last 3.1 Gyr on all four k × H corners)"
FAILS = "fails (ΔE_min < 0 somewhere in the last 3.1 Gyr on all four corners)"
CONDITION = ("Earth-calibrated model: Nimmo+ 2004 eqs 30 and 32 integrated with RK4 at Nimmo's 4 Myr step on the state "
             "(T_c, T_m); the mantle base temperature by the interior solve's own adiabat ratio (eq. 29's form); "
             "long-lived radiogenic heat only (K·Th·U, history factor); two new declarations (initial T_c, T_m); "
             "the result stands on ≈24 declarations in all — outputs read 'consistent with an Earth-calibrated model'")


def _core_side(material: str, p_cmb: float, t_c: float, r_cmb: float, m_core: float) -> dict:
    """Profile and rate coefficients at T_c. Q̃ = Q(dT_c/dt = −1 K/s) since Q_s, Q_L, Q_g are linear in the rate."""
    prof = ce.core_profile(material, p_cmb, t_c, r_cmb, m_core)
    unit = ce.core_terms(prof, dtc_dt=-1.0, h=ce.H_CORE)
    # Heat released per unit cooling rate, positive: Q_s + Q_L + Q_g evaluated at dT_c/dt = −1 K/s.
    # (Nimmo's Q̃ carries the opposite sign; the physics is Q_C − Q_R = −Q̃_abs · dT_c/dt, cooling when Q_C > Q_R.)
    q_tilde = unit["q_s"] + unit["q_l"] + unit["q_g"]
    return {"prof": prof, "q_tilde": q_tilde, "inner_core": unit["inner_core"], "m_core": prof["m"][0],
            "core_status": unit.get("core_status", "inner_core")}


def rates(t_c: float, t_m: float, p: dict, t_gyr_from_present: float) -> dict:
    """dT_c/dt and dT_m/dt [K/s] at state (T_c, T_m) and epoch t (Gyr, negative = past)."""
    t_m_base = p["r_b"] * t_m
    side = _core_side(p["material"], p["p_cmb"], t_c, p["r_cmb"], p["m_core"])
    # Nimmo starts both at 4800 K (Fig. 2 caption): zero jump at t = 0. F_b ∝ ΔT^(4/3) → 0 continuously (eqs 37–38),
    # so Q_C = 0 for ΔT ≤ 0 is the continuous limit, not a patch. The mantle cools first; the core follows.
    q_c = cf.bottom_layer(t_c, t_m_base, p["r_cmb"])["q_c_w"] if t_c > t_m_base else 0.0
    q_r = side["m_core"] * p["h_core"]
    dtc = -(q_c - q_r) / side["q_tilde"]          # K/s; negative = cooling
    q_m = mf.implied_flux(t_m, p["g"], p["r_p"])["q_m_w"]
    h_m = p["h_m_present_w"] * rg.history_factor(t_gyr_from_present)
    dtm = (h_m - q_m + q_c) / (p["m_mantle"] * mf.C_PM * math.sqrt(p["r_b"]))
    return {"dtc": dtc, "dtm": dtm, "q_c": q_c, "q_m": q_m, "h_m": h_m, "q_r": q_r, "side": side}


def integrate(params: dict, t_c0: float, t_m0: float, age_gyr: float, step_myr: float = STEP_MYR) -> dict:
    """RK4 from t = −age to 0. Returns the sampled history (one row per step) and the entropy corners per row."""
    n = max(1, int(round(age_gyr * 1000.0 / step_myr)))
    h = age_gyr * GYR_S / n
    t_c, t_m = float(t_c0), float(t_m0)
    rows = []
    for i in range(n + 1):
        t_now = -age_gyr + i * age_gyr / n            # Gyr from present (≤ 0)
        r1 = rates(t_c, t_m, params, t_now)
        side = r1["side"]
        corners = {}
        for k in K_CORNERS:
            for hh in H_CORNERS:
                unit = ce.core_terms(side["prof"], dtc_dt=r1["dtc"], h=hh)
                corners[(k, hh)] = cent.entropy_terms(side["prof"], unit, r1["dtc"], hh, k)["delta_e"]
        ic = side["inner_core"]
        rows.append({"t_gyr": t_now, "t_c": t_c, "t_m": t_m, "dtc_dt_k_gyr": r1["dtc"] * GYR_S,
                     "q_c_w": r1["q_c"], "q_m_w": r1["q_m"], "h_m_w": r1["h_m"],
                     "r_i_km": (ic["r_i"] / 1e3) if ic else 0.0, "core_status": side["core_status"],
                     "delta_e_corners": corners,
                     "delta_e_min_corner": min(corners.values()), "delta_e_max_corner": max(corners.values())})
        if i == n:
            break
        # classical RK4 on (T_c, T_m)
        k1 = (r1["dtc"], r1["dtm"])
        r2 = rates(t_c + 0.5 * h * k1[0], t_m + 0.5 * h * k1[1], params, t_now + 0.5 * h / GYR_S)
        k2 = (r2["dtc"], r2["dtm"])
        r3 = rates(t_c + 0.5 * h * k2[0], t_m + 0.5 * h * k2[1], params, t_now + 0.5 * h / GYR_S)
        k3 = (r3["dtc"], r3["dtm"])
        r4 = rates(t_c + h * k3[0], t_m + h * k3[1], params, t_now + h / GYR_S)
        k4 = (r4["dtc"], r4["dtm"])
        t_c += h * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
        t_m += h * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
    return {"rows": rows, "n_steps": n, "step_myr": age_gyr * 1000.0 / n}


def window_summary(rows: list[dict], window_gyr: float = WINDOW_GYR) -> dict:
    """ΔE statistics over the last `window_gyr` on each corner, and the nucleation epoch."""
    win = [r for r in rows if r["t_gyr"] >= -window_gyr - 1e-9]
    corners = list(win[0]["delta_e_corners"].keys())
    per_corner = {}
    for c in corners:
        vals = [r["delta_e_corners"][c] for r in win]
        per_corner[c] = {"min": min(vals), "mean": sum(vals) / len(vals), "present": vals[-1],
                         "t_min_gyr": win[min(range(len(vals)), key=lambda i: vals[i])]["t_gyr"]}
    mins = [v["min"] for v in per_corner.values()]
    if all(m > 0.0 for m in mins):
        verdict = SUSTAINED
    elif all(m < 0.0 for m in mins):
        verdict = FAILS
    else:
        verdict = CANNOT_SAY_HISTORY
    nucleation = next((r["t_gyr"] for r in rows if r["r_i_km"] > 0.0), None)
    always = rows[0]["r_i_km"] > 0.0
    return {"per_corner": per_corner, "delta_e_min_band": (min(mins), max(mins)), "verdict": verdict,
            "nucleation_t_gyr": nucleation, "inner_core_from_start": always,
            "inner_core_case": ("always" if always else "never" if nucleation is None else "nucleates")}


def sweep(params: dict, t_c0: float, t_m0: float, age_gyr: float, step_myr: float = STEP_MYR) -> dict:
    """h, h/2, h/4 — the pre-registered convergence test on ΔE_min (nominal corner) and the inner-core case."""
    out = {}
    for label, s in (("h", step_myr), ("h/2", step_myr / 2.0), ("h/4", step_myr / 4.0)):
        hist = integrate(params, t_c0, t_m0, age_gyr, s)
        ws = window_summary(hist["rows"])
        nominal = (cf.K_CORE, ce.H_CORE)
        vals = [r["delta_e_corners"][nominal] if nominal in r["delta_e_corners"] else None for r in hist["rows"]]
        # the nominal (k 50, H 1.5) point is not a corner; use the k=70,H=1.5 corner's ΔE_min as the convergence quantity
        # and the band ends, all three must move together
        out[label] = {"hist": hist, "summary": ws,
                      "delta_e_min_lo": ws["delta_e_min_band"][0], "delta_e_min_hi": ws["delta_e_min_band"][1],
                      "t_c_present": hist["rows"][-1]["t_c"], "t_m_present": hist["rows"][-1]["t_m"],
                      "case": ws["inner_core_case"]}
    a, b = out["h/2"], out["h/4"]
    widths = []
    for key in ("delta_e_min_lo", "delta_e_min_hi"):
        ref = abs(b[key]) if abs(b[key]) > 0 else 1.0
        widths.append(abs(b[key] - a[key]) / ref)
    same_case = out["h"]["case"] == out["h/2"]["case"] == out["h/4"]["case"]
    out["converged"] = max(widths) < CONVERGENCE_TOL and same_case
    out["convergence_width"] = max(widths)
    out["same_inner_core_case"] = same_case
    return out


def solve(mass_earth: float, core_mass_fraction: float | None, core_radius_earth: float | None,
          cmb_pressure_gpa: float | None, cmb_temperature: float | None, potential_temperature: float | None,
          radius_earth: float | None, age_gyr: float | None, core_initial_temperature: float | None,
          mantle_initial_potential_temperature: float | None, core_material: str = "fe_prem",
          body_class: str | None = None, run_sweep: bool = False) -> Result:
    inputs = {"mass_earth": mass_earth, "core_mass_fraction": core_mass_fraction, "core_radius": core_radius_earth,
              "cmb_pressure": cmb_pressure_gpa, "cmb_temperature": cmb_temperature,
              "potential_temperature": potential_temperature, "radius_earth": radius_earth, "age_gyr": age_gyr,
              "core_initial_temperature": core_initial_temperature,
              "mantle_initial_potential_temperature": mantle_initial_potential_temperature,
              "core_material": core_material, "body_class": body_class,
              "step_myr": STEP_MYR, "core_h_w_per_kg": ce.H_CORE}
    if body_class in ROCKY_ONLY:
        return out_of_domain(RECIPE, VERSION, f"'{body_class}' 에는 규산염 맨틀·금속 핵의 결합 열진화가 뜻이 없다 — 암석체의 것이다.",
                             inputs=inputs, refs=REFS)
    if not core_radius_earth or not core_mass_fraction or core_mass_fraction <= 0.0:
        return out_of_domain(RECIPE, VERSION, cf.NO_CORE, inputs=inputs, refs=REFS)
    if None in (cmb_pressure_gpa, cmb_temperature, potential_temperature, radius_earth, age_gyr):
        return out_of_domain(RECIPE, VERSION, NO_STRUCTURE, inputs=inputs, refs=REFS)
    if core_initial_temperature is None or mantle_initial_potential_temperature is None:
        return out_of_domain(RECIPE, VERSION, NO_INITIAL, inputs=inputs, refs=REFS)

    m_kg = mass_earth * cf.M_EARTH_KG
    r_p = radius_earth * cf.R_EARTH_M
    params = {"material": core_material, "p_cmb": cmb_pressure_gpa * 1e9, "r_cmb": core_radius_earth * cf.R_EARTH_M,
              "m_core": m_kg * core_mass_fraction, "m_mantle": m_kg * (1.0 - core_mass_fraction),
              "r_b": cmb_temperature / potential_temperature,
              "g": cf.G_NEWTON * m_kg / r_p ** 2, "r_p": r_p, "h_core": ce.H_CORE,
              "h_m_present_w": rg.budget(m_kg * (1.0 - core_mass_fraction))["mantle_w"]}
    try:
        if run_sweep:
            sw = sweep(params, core_initial_temperature, mantle_initial_potential_temperature, age_gyr)
            best = sw["h/4"]
            converged, width = sw["converged"], sw["convergence_width"]
        else:
            hist = integrate(params, core_initial_temperature, mantle_initial_potential_temperature, age_gyr)
            ws = window_summary(hist["rows"])
            best = {"hist": hist, "summary": ws, "t_c_present": hist["rows"][-1]["t_c"],
                    "t_m_present": hist["rows"][-1]["t_m"], "case": ws["inner_core_case"]}
            converged, width = None, None
    except (PhaseGap, ValueError) as e:
        return out_of_domain(RECIPE, VERSION, f"적분이 물리 범위를 벗어났다 — {e}", inputs=inputs, refs=REFS)

    rows = best["hist"]["rows"]
    ws = best["summary"]
    last = rows[-1]
    values = {
        "core_cmb_temperature_present": last["t_c"],
        "mantle_potential_temperature_present": last["t_m"],
        "dtc_dt_present_k_per_gyr": last["dtc_dt_k_gyr"],
        "q_cmb_present": last["q_c_w"],
        "q_mantle_present": last["q_m_w"],
        "inner_core_radius_present_km": last["r_i_km"],
        "inner_core_case": ws["inner_core_case"],
        "inner_core_nucleation_gyr_ago": (-ws["nucleation_t_gyr"]) if ws["nucleation_t_gyr"] is not None else None,
        "delta_e_min_3gyr_lo": ws["delta_e_min_band"][0],
        "delta_e_min_3gyr_hi": ws["delta_e_min_band"][1],
        "delta_e_present_lo": min(last["delta_e_corners"].values()),
        "delta_e_present_hi": max(last["delta_e_corners"].values()),
        "entropy_history_verdict": (ws["verdict"] if converged in (True, None) else NOT_CONVERGED),
        "history_converged": converged,
        "history_convergence_width": width,
        "history_steps": best["hist"]["n_steps"],
    }
    units = {"core_cmb_temperature_present": "K", "mantle_potential_temperature_present": "K",
             "dtc_dt_present_k_per_gyr": "K/Gyr", "q_cmb_present": "W", "q_mantle_present": "W",
             "inner_core_radius_present_km": "km", "inner_core_case": "", "inner_core_nucleation_gyr_ago": "Gyr",
             "delta_e_min_3gyr_lo": "W/K", "delta_e_min_3gyr_hi": "W/K", "delta_e_present_lo": "W/K",
             "delta_e_present_hi": "W/K", "entropy_history_verdict": "", "history_converged": "",
             "history_convergence_width": "", "history_steps": ""}
    if converged is None:
        values["history_converged"] = None   # the sweep is on demand (test_core_history.py --sweep); record: 2026-09-04 width 0.001 %
    mw = 1e6
    nuc = "" if ws["nucleation_t_gyr"] is None else f" ({-ws['nucleation_t_gyr']:.2f} Gyr 전)"
    reason = (f"Nimmo 식 30·32 를 {age_gyr:.2f} Gyr 동안 RK4 로 적분 (h = {best['hist']['step_myr']:.2f} Myr, "
              f"{best['hist']['n_steps']} 걸음{'' if converged is None else ', 수렴 폭 ' + format(width, '.1%')}). "
              f"현재 T_c {last['t_c']:.0f} K · T_m {last['t_m']:.0f} K · dT_c/dt {last['dtc_dt_k_gyr']:+.0f} K/Gyr · "
              f"Q_C {last['q_c_w']/1e12:.2f} TW · Q_M {last['q_m_w']/1e12:.1f} TW · 내핵 {ws['inner_core_case']}"
              f"{nuc} · "
              f"ΔE_min(3.1 Gyr) 네 모서리 {ws['delta_e_min_band'][0]/mw:+.0f}…{ws['delta_e_min_band'][1]/mw:+.0f} MW/K → "
              f"{values['entropy_history_verdict']}. 지구 보정 모형과의 일관성이지 이 천체의 실제 값이 아니다")
    return Result(recipe=RECIPE, version=VERSION, regime="thermal-history", reason=reason, grade="analog",
                  inputs=inputs, values=values, units=units, refs=REFS, notes=(CONDITION,))


from registry import recipe  # noqa: E402


@recipe("core_thermal_history")
def _from_state(state):
    return solve(mass_earth=state["mass_earth"], core_mass_fraction=state.get("core_mass_fraction"),
                 core_radius_earth=state.get("core_radius"), cmb_pressure_gpa=state.get("cmb_pressure"),
                 cmb_temperature=state.get("cmb_temperature"), potential_temperature=state.get("potential_temperature"),
                 radius_earth=state.get("radius") or state.get("radius_earth"), age_gyr=state.get("age_gyr"),
                 core_initial_temperature=state.get("core_initial_temperature"),
                 mantle_initial_potential_temperature=state.get("mantle_initial_potential_temperature"),
                 core_material=state.get("core_material", "fe_prem"), body_class=state.get("body_class"))
