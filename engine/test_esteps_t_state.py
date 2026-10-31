# E-steps — 고정 걸음 T 상태: 단계 밀도의 한 길(브리지 · 표면 대체 · rho0 · 캐시)과 고정 (p_c, T_c) 표면 T 의 band/10 문턱
"""E-steps (prereg pc/ea-esteps): the fixed step carries T as an RK4 state.

    python3 engine/test_esteps_t_state.py

1. The stage dT reads density through `_stage_density`, the one function `deriv` uses (r2 B1 on bccdb6c9). On the C24
   IF97 bridge (dense water below 0.1 GPa), where the material itself refuses, the stage dT keeps the step-start slope
   and calls no material. The same holds for SURF_RHO's PhaseGap fallback and for rho0.
2. Earth's last thermal integration at fixed (p_c, T_c) with its lithosphere: surface T at STEPS 1500 against 9600 is
   within band/10 with the switch on, and at least 100 × band/10 off (design: 0.20 and 444).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eos  # noqa: E402
import interior  # noqa: E402

fails = 0
BAND10 = 9.63e-7


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


def same(x):
    return x


dense = interior.MATERIALS["h2o_liquid_dense"]
P_BR, T_BR = 0.05e9, 400.0

print("브리지 — 조밀 물 0.05 GPa · 400 K: 재료 자신은 거절, 단계 밀도는 IF97, 단계 dT 는 걸음 시작 기울기")
try:
    dense.density(P_BR, T_BR, 0.0)
    refuses = False
except eos.PhaseGap:
    refuses = True
row(refuses, "전제: h2o_liquid_dense 가 0.05 GPa 에서 PhaseGap (이 길을 건너뛰면 새 거절)")
br, pe, rho = interior._stage_density(dense, P_BR, T_BR, T_BR, 0.0, 0.0, 0.0, same, True, {})
row(br == "bridge" and rho == interior.COLUMN_STEAM.density(P_BR, T_BR), f"_stage_density → {br} · ρ {rho:.3f}")
try:
    got = interior._stage_dtdr(dense, P_BR, T_BR, T_BR, 0.0, 0.0, 0.0, same, True, {}, 7.0e-9, -3.0e4)
    row(got == 7.0e-9 * -3.0e4, f"_stage_dtdr 브리지 → 걸음 시작 기울기 × dP/dr ({got!r})")
except eos.PhaseGap as e:
    row(False, f"_stage_dtdr 브리지가 재료를 불러 거절: {str(e)[:120]}")

print("\n표면 밖 — 1 bar 밀도가 PhaseGap 이면 rho0(dT 는 세지 않는다), SURF_RHO 끔이면 rho0")
n0 = interior.SURF_RHO_FALLBACKS[0]
br, pe, rho = interior._stage_density(dense, -1.0e6, T_BR, T_BR, 0.0, 0.0, 0.0, same, False, {}, count=False)
row(br == "surf_fallback" and rho == dense.rho0 and interior.SURF_RHO_FALLBACKS[0] == n0,
    f"count=False → {br} · ρ {rho} · 셈 그대로")
got = interior._stage_dtdr(dense, -1.0e6, T_BR, T_BR, 0.0, 0.0, 0.0, same, False, {}, 7.0e-9, -3.0e4)
row(got == 7.0e-9 * -3.0e4 and interior.SURF_RHO_FALLBACKS[0] == n0, "_stage_dtdr surf_fallback → 걸음 시작 기울기, 셈 그대로")
interior._stage_density(dense, -1.0e6, T_BR, T_BR, 0.0, 0.0, 0.0, same, False, {})
row(interior.SURF_RHO_FALLBACKS[0] == n0 + 1, "count=True(deriv) 는 센다")
interior.SURF_RHO_FALLBACKS[0] = n0
saved = interior.SURF_RHO
try:
    interior.SURF_RHO = False
    br, pe, rho = interior._stage_density(dense, -1.0e6, T_BR, T_BR, 0.0, 0.0, 0.0, same, False, {})
    row(br == "rho0" and rho == dense.rho0, f"SURF_RHO 끔 → {br}")
finally:
    interior.SURF_RHO = saved

print("\n캐시 — 같은 걸음의 같은 (P, T) 는 재료를 다시 부르지 않는다")
cache = {(2.0e9, 1500.0): 1234.5}
br, pe, rho = interior._stage_density(dense, 2.0e9, 1500.0, 1500.0, 0.0, 0.0, 0.0, same, False, cache)
row(br == "eos" and rho == 1234.5, f"캐시 적중 → {br} · ρ {rho}")

print("\nE6 — 지구 마지막 열 적분(고정 p_c · T_c · 암석권), 표면 T: STEPS 1500 대 9600")
A = (358454193668.33655, 5.972e+24, 0.325, 0.0, "fe_prem", 0.0, None, 0.0, 0.0, 1.0, True, 3172.346057629161, 1600.0,
     0.0, 0.0, 0.0, 1.0, 0.0, False, None)
K = {"ammonia_mass_fraction": 0.0, "interface_jumps": None, "basal_layer": None,
     "lithosphere": {"r_base": 6255008.71315615, "r_top": 6390008.71315615, "t_s": 293.0}}
steps0, sw0 = interior.STEPS, interior.FIXED_T_STATE
try:
    err = {}
    for on in (True, False):
        interior.FIXED_T_STATE = on
        ts = {}
        for n in (1500, 9600):
            interior.STEPS = n
            ts[n] = interior.integrate(*A, **K).t_surface
        err[on] = abs(ts[1500] - ts[9600]) / ts[9600] / BAND10
    row(err[True] <= 1.0, f"켬: |ΔT_s|/T_s = {err[True]:.3g} × band/10 (≤ 1, 설계 0.20)")
    row(err[False] >= 100.0, f"끔: |ΔT_s|/T_s = {err[False]:.3g} × band/10 (≥ 100, 설계 444)")
finally:
    interior.STEPS, interior.FIXED_T_STATE = steps0, sw0

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
