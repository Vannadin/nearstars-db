# 층 목록 열진화(T2)의 시험 — 판 2 · 4 한 번 평가가 samuel_run 과 비트 같음 · B1′ · 판 2 회귀 여섯
"""Checks for `thermal_stack` (pre-registration `prereg-T2-layer-list.md` §7). The box sweeps (R4 · R4P)
are `tools/samuel_a_report.py --engine stack`'s; here one evaluation each and one full plate-2 run.

    python3 engine/test_thermal_stack.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import samuel_run as sr                # noqa: E402
import samuel_structure as ss          # noqa: E402
import samuel_thermal as st            # noqa: E402
import thermal_stack as ts             # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


prof = ss.mars_profile(Path(__file__).resolve().parent / "bodies" / "mars.yaml")
G = prof.gravity(prof.radius_m)
LAYER = dict(d_d=st.D_D_M, k_d=4.0, lambda_d=14.373, fe_mean=96.97, fe_top=94.1306, nodes=41, melting=True)
STATE = (2158.1024424461625, 1815.5593199821958, 80e3, 20e3, 1.0)

# One evaluation, stack against the frozen `samuel_run` — plate 2 (no layer), plate 4 and 4P (layer).
for name, lam, kw in (("plate 2", 20.0, {}), ("plate 4", 10.0, {"model": "bml", "layer": LAYER}),
                      ("plate 4P", 10.0, {"model": "bml", "layer": LAYER, "p_m_mode": "top"})):
    a = sr.state_terms(sr.Setup(lam=lam, profile=prof, g=G, g_c=0.0, **kw), *STATE, -0.02)
    b = ts.state_terms(ts.samuel_stack(lam=lam, profile=prof, g=G, **kw), *STATE, -0.02)
    check(f"{name} — one evaluation bit-identical to samuel_run", a == b, f"{len(a)} keys · dT_m/dt {b['dtm']!r}")

# B1′ — D_d = 0 is no layer: the stack has no basal layer and evaluates as plate 2's bundle does.
s0 = ts.samuel_stack(lam=10.0, profile=prof, g=G, model="bml", layer={**LAYER, "d_d": 0.0})
s1 = ts.samuel_stack(lam=10.0, profile=prof, g=G, model="bml")
check("B1′ — D_d = 0 builds no basal layer, bit-identical to no layer",
      s0.basal is None and [x.role for x in s0.layers] == ["core", "mantle", "lid"]
      and ts.state_terms(s0, *STATE, -0.02) == ts.state_terms(s1, *STATE, -0.02))
check("the mantle names its volume — silicate without a layer, convective with one (C113)",
      s1.mantle.params["volume"] == "silicate"
      and ts.samuel_stack(lam=10.0, profile=prof, g=G, model="bml", layer=LAYER).mantle.params["volume"] == "convective")
check("the inner-core slot is empty in every reproduction stack (T2 §6)", s1.core.params["inner_core"] is None)

# Source-form switches (prereg-source-form-plates d9d5af99). SF-B1: off is T2 — every check above ran with
# them off. SF-에너지: in a layered stack every heating term adds back to the whole silicate's (1e-12).
import math                            # noqa: E402
sf = ts.samuel_stack(lam=10.0, profile=prof, g=G, model="bml", layer=LAYER, source_volume=True, source_lid_heat=True)
L = ts.state_terms(sf, *STATE, -0.02)["layer"]
r_p, d_l, d_cr = st.R_PLANET_M, STATE[2], STATE[3]
shell = lambda a, b: 4 / 3 * math.pi * (a ** 3 - b ** 3)
v_lid, v_cr, v_sil = shell(r_p, r_p - d_l), shell(r_p, r_p - d_cr), shell(r_p, st.R_CORE_M)
h_pm = L["h_d"] / LAYER["lambda_d"]
total = L["h_m"] * (v_lid - v_cr) + L["h_cr"] * v_cr + L["h_m"] * L["v_conv_p"] + L["h_d"] * L["v_d"]
check("SF-에너지 — h_m (V_lid − V_cr) + h_cr V_cr + h_m V_conv′ + H_d V_d = H_pm V_sil (1e-12)",
      abs(total / (h_pm * v_sil) - 1.0) < 1e-12, f"ratio {total / (h_pm * v_sil) - 1.0:+.2e}")
p2 = ts.state_terms(ts.samuel_stack(lam=20.0, profile=prof, g=G), *STATE, -0.02)
p2s_stack = ts.samuel_stack(lam=20.0, profile=prof, g=G, source_volume=True)
p2s = ts.state_terms(p2s_stack, *STATE, -0.02)
check("C113 switch — plate 2's mantle volume becomes the convective one and dT_m/dt moves",
      p2s_stack.mantle.params["volume"] == "convective" and p2s["dtm"] != p2["dtm"],
      f"dT_m/dt {p2['dtm']:.4e} → {p2s['dtm']:.4e} K/s")

# R2 — plate 2's six regression pins, through the stack.
out = ts.run(ts.samuel_stack(lam=20.0, profile=prof, g=G), 10.0)
v = sr.curve_values(out["rows"])
# the same pins and widths as test_samuel_run.FROZEN_L20 / FROZEN_TOL (K to the frozen decimal; peak time 0.0005 Gyr)
for key, want, tol in (("T_c today", 2101.44, 0.005), ("T_m today", 1942.15, 0.005), ("T_c(1) − T_c0", -49.32, 0.005),
                       ("T_m(1) − T_m0", 285.91, 0.005), ("T_m peak", 2043.85, 0.005), ("T_m peak time", 1.2726, 0.0005)):
    check(f"R2 — {key} = {want}", abs(v[key] - want) <= tol, f"{v[key]:.6f}")

print(f"  test_thermal_stack — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
