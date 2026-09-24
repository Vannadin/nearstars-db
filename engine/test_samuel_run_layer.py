# 판 4 배선 시험 — B1(D_d = 0 비트 동일) · 식 (1) 질량 수지 · ΔT′_b · 두 V′_m · 층 한 번 평가
"""Checks for plate 4's wiring in `samuel_run` (pre-registration v2-23 · v2-24). One evaluation each, no
integration — the A verdict is `tools/samuel_a_report.py`'s.

    python3 engine/test_samuel_run_layer.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import samuel_run as sr                # noqa: E402
import samuel_structure as ss          # noqa: E402
import samuel_thermal as st            # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


prof = ss.mars_profile(Path(__file__).resolve().parent / "bodies" / "mars.yaml")
G = prof.gravity(prof.radius_m)
LAYER = dict(d_d=st.D_D_M, k_d=4.0, lambda_d=14.373, fe_mean=96.97, fe_top=94.1306, nodes=41, melting=True,
             source="test")
STATE = (2158.1024424461625, 1815.5593199821958, 80e3, 20e3, 1.0)   # T_c, T_m, D_l, D_cr, t


def terms(**kw):
    s = sr.Setup(lam=10.0, profile=prof, g=G, g_c=0.0, **kw)
    return s, sr.state_terms(s, *STATE, -0.02)


# B1 — D_d = 0 is no layer: every value of one evaluation is bit-identical to the run without `layer`.
for model in ("no_bml", "bml"):
    _, a = terms(model=model)
    _, b = terms(model=model, layer={**LAYER, "d_d": 0.0})
    check(f"B1 ({model}) — D_d = 0 ≡ no layer, bit for bit", a == b and a["layer"] is None,
          f"{len(a)} keys · T_c rate {a['dtc']!r}")

# With the layer.
s, f = terms(model="bml", layer=LAYER)
L = f["layer"]
check("ΔT′_b = T_i − T′_b = 1.43 R T_m² / E*",
      abs((L["t_i"] - f["t_b"]) - 1.43 * st.R_GAS_J_PER_MOL_K * STATE[1] ** 2 / st.E_STAR_J_PER_MOL) < 1e-9,
      f"T′_b {f['t_b']:.2f} · T_i {L['t_i']:.2f} K · printed-form T′_b {L['t_b_printed']:.2f} K (compared, not used)")
r_p, r_c, r_base = st.R_PLANET_M, st.R_CORE_M, st.R_CORE_M + st.D_D_M
v_sil = 4 / 3 * math.pi * (r_p ** 3 - r_c ** 3)
h_pm = L["h_d"] / LAYER["lambda_d"]
check("eq. (1) mass balance — H′_m V_sil′ + H_d V_d = H_pm V_sil",
      abs(L["h_m_prime"] * L["v_sil_p"] + L["h_d"] * L["v_d"] - h_pm * v_sil) < 1e-12 * h_pm * v_sil,
      f"H′_m/H_pm {L['h_m_prime'] / h_pm:.6f} · H_d/H_pm {L['h_d'] / h_pm:.3f}")
check("two V′_m — V_sil′ (to R_p) > V_conv′ (to R_l), both from R_c + D_d",
      abs(L["v_sil_p"] - 4 / 3 * math.pi * (r_p ** 3 - r_base ** 3)) < 1e-6 * L["v_sil_p"]
      and abs(L["v_conv_p"] - 4 / 3 * math.pi * ((r_p - STATE[2]) ** 3 - r_base ** 3)) < 1e-6 * L["v_conv_p"],
      f"V_sil′ {L['v_sil_p']:.4e} · V_conv′ {L['v_conv_p']:.4e} m³")
g = s.layer_grid
check("the layer grid starts linear between T_c and T_i and feeds q_c, q_d",
      g is not None and g.t[0] == STATE[0] and abs(g.t[-1] - L["t_i"]) < 1e-9 and (L["q_c_layer"], L["q_d"]) == s.layer_q,
      f"q_c {L['q_c_layer'] * 1e3:.3f} · q_d {L['q_d'] * 1e3:.3f} mW/m²")
print(f"  [J] {g.describe()}")

print(f"  test_samuel_run_layer — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
