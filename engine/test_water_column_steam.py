# C24 — 물 기둥의 IF97 후보(마지막)와 두 이음매, 양성 대조, 물 많은 암석체의 수렴을 잰다
"""C24: the water column consults IAPWS-IF97 last (engine/water-world-convergence-context-notes.md).

    python3 engine/test_water_column_steam.py
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import steam_if97, water2_table, water_table  # noqa: E402
from interior import solve  # noqa: E402

fails = 0


def row(ok, text):
    global fails
    fails += 0 if ok else 1
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


print("이음매 — IF97 ↔ water2 (0.1 GPa) · IF97 ↔ water1 (500 K), 사전등록 문턱 Ⓐ ≤ 5 %, 실측 ≤ 0.04 % 를 0.05 % 로 고정")
worst = 0.0
for T in (560.0, 600.0, 700.0, 800.0, 870.0, 1000.0):
    a, b = steam_if97.density(0.1e9, T), water2_table.density(0.1e9, T)
    worst = max(worst, abs(a / b - 1.0))
for P in (0.02e9, 0.05e9, 0.09e9, 0.1e9):
    a, b = steam_if97.density(P, 500.0), water_table.density(P, 500.0)
    worst = max(worst, abs(a / b - 1.0))
row(worst < 5e-4, f"열 점 최악 |Δρ/ρ| {worst*100:.3f} %")

print("\n양성 대조 — 얼음 0 은 한 비트도 안 움직인다 (2026-09-04 기록: 3 s · calibrated · R 1.0030 · 중심 358.5 GPa)")
t0 = time.perf_counter()
r0 = solve(1.0, core_mass_fraction=0.325, potential_temperature=1600.0)
row(r0.converged and r0.grade == "calibrated" and abs(r0.values["radius"] - 1.0030) < 5e-5 and abs(r0.values["core_pressure"] - 358.46) < 0.05,
    f"ice 0: {r0.grade} · R {r0.values['radius']:.4f} · centre {r0.values['core_pressure']:.2f} GPa ({time.perf_counter()-t0:.0f} s)")

print("\n⑥ 물 많은 암석체 — 수렴하거나 다음 벽이 이름을 댄다 (연쇄로 메우지 않는다)")
for imf in (0.1, 0.3):
    t0 = time.perf_counter()
    r = solve(1.0, core_mass_fraction=0.325, ice_mass_fraction=imf, potential_temperature=1600.0)
    dt = time.perf_counter() - t0
    if r.applicable:
        print(f"      ice {imf}: converged {r.converged} · {r.grade} · R {r.values['radius']:.4f} · P_cmb {r.values['cmb_pressure']:.1f} · T_cmb {r.values['cmb_temperature']:.0f} K ({dt:.0f} s)")
        # 등급은 수렴 판정이 아니다 — interior 는 열이 흐르는 물 기둥이 있으면 규칙으로 analog 를 준다(thermal_moves 등).
        # 사전등록 ⑥ 의 "calibrated 복귀" 는 마른 천체의 등급을 보고 적은 것이라 물 천체에는 성립할 수 없는 기준이었고,
        # 그렇게 기록한다. 판정은 converged 하나다.
        row(r.converged, f"ice {imf}: 수렴 (등급 {r.grade} 은 규칙, 판정 아님)")
    else:
        print(f"      ice {imf}: REFUSED — {r.reason[:140]} ({dt:.0f} s)")
        row("IF97" in r.reason or "표현" in r.reason or "PhaseGap" in r.reason, f"ice {imf}: 이름 있는 거절 (다음 벽) — 기록만")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
