# 구조 기저층의 시험 — 선언 없으면 예전과 같음(S-B1 · S-B2) · 층 질량 · 경계 반지름 · 상태 인쇄 · 거절 둘
"""Checks for the basal layer in the structure solve (pre-registration `prereg-structure-basal-layer.md` §3).
Mars at a fixed core mass fraction (0.24) and T_pot 1600 K — test inputs, not a fit.

    python3 engine/test_basal_layer.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interior as I                   # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


M, CMF, TP = 0.1074, 0.24, 1600.0
D_KM, RHO = 150.0, 4050.0


def solve(**kw):
    return I.solve(M, core_mass_fraction=CMF, potential_temperature=TP, **kw)


# S-B1 / S-B2 — no declaration, or thickness 0, is the path without a layer: every value the same.
base = solve()
zero = solve(basal_layer_thickness_km=0.0, basal_layer_density=RHO)
check("S-B1 — no declaration: the layer keys do not change the answer", base.values == solve(basal_layer_thickness_km=None).values)
check("S-B2 — thickness 0 is no layer, bit-identical", zero.values == base.values and zero.applicable == base.applicable)

# S-경계 · S-질량 — the layer as the integrator walks it (the record carries each step's start state).
lay = solve(basal_layer_thickness_km=D_KM, basal_layer_density=RHO)
v = lay.values
check("S-경계 — the solved thickness is the declared one (1e-6)",
      abs(v["basal_layer_thickness_km"] - D_KM) < 1e-6 * D_KM,
      f"{v['basal_layer_thickness_km']!r} km · top {v['core_plus_layer_radius_solved_km']:.3f} km")
rec: list = []
p_c = v["core_pressure"] * 1e9
t_c = v["core_temperature"]
st = I.integrate(p_c, M * I.EARTH_MASS_KG, CMF, 0.0, "fe_prem", t_center=t_c, t_pot=TP, record=rec,
                 basal_layer={"thickness_m": D_KM * 1e3, "density": RHO})
info = I._BASAL_INFO.get(id(st))
r_lo, r_hi = info["r_base"], info["r_top"]
inside = [row for row in rec if r_lo <= row[0] < r_hi]     # the record names the stack material at a step start
m_lo = next(row[2] for row in rec if row[0] >= r_lo - 1e-6)
m_hi = next(row[2] for row in rec if row[0] >= r_hi - 1e-6)
want = RHO * 4.0 / 3.0 * math.pi * (r_hi ** 3 - r_lo ** 3)
check("S-질량 — the layer's mass is 4050 × its volume (1e-6)", abs((m_hi - m_lo) / want - 1.0) < 1e-6,
      f"{(m_hi - m_lo):.6e} kg against {want:.6e} kg · {len(inside)} steps inside")
check("S-경계 — the layer starts at the core radius and ends at core + D_d (1e-6)",
      abs(r_lo - st.core_radius_m) < 1e-6 * r_lo and abs(r_hi - r_lo - D_KM * 1e3) < 1e-6 * D_KM * 1e3,
      f"base {r_lo / 1e3:.3f} km · top {r_hi / 1e3:.3f} km")
check("S-상태 — the layer base state is printed", isinstance(v["basal_silicate_state"], str),
      f"{v['basal_silicate_state']} · base P {info['p_base'] / 1e9:.2f} GPa · T {info['t_base']:.0f} K")

# Refusals by name.
r1 = solve(basal_layer_thickness_km=D_KM)
check("a thickness without a density is refused by name", not r1.applicable and "밀도" in str(r1.reason))
r2 = solve(basal_layer_thickness_km=D_KM, basal_layer_density=RHO, interface_temperature_jumps={"core/rock": 10.0})
check("a layer with interface jumps is refused by name (no `basal` in the jump vocabulary yet)",
      not r2.applicable and "basal" in str(r2.reason))

print(f"  test_basal_layer — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
