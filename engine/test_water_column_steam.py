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

print("\n⑥ 물 많은 암석체 — 뜨거운 물 괄호 밑을 채운 답은 수렴한 답에서 R1 로 이름 대고 거절한다 (C122 고침)")
# ⚠ 옛 기대(수렴, 2026-09-04 기록 R 1.1313 · 1.2585)는 뜨거운 물 괄호 밑을 500 kg/m³ 로 채운 답이었다 —
#   C122 고침(prereg-c122-fix 3db41d5f, 덧붙임 1 00b9dd4d)이 답에서 거절한다. PASS 는 등록 R1 문장 요소에 댄다:
#   밀도 괄호 구절 · 채웠을 걸음 수 · 질량 몫. 다른 벽의 거절은 FAIL 로 드러난다(옛 이름 목록은 이 두 행에서 뺐다).
import re  # noqa: E402
for imf in (0.1, 0.3):
    t0 = time.perf_counter()
    r = solve(1.0, core_mass_fraction=0.325, ice_mass_fraction=imf, potential_temperature=1600.0)
    dt = time.perf_counter() - t0
    if r.applicable:
        print(f"      ice {imf}: 풀림 R {r.values['radius']:.4f} ({dt:.0f} s)")
        row(False, f"ice {imf}: R1 거절을 기대했는데 풀림")
    else:
        why = r.reason or ""
        print(f"      ice {imf}: REFUSED — {why[:200]} ({dt:.0f} s)")
        ok = ("뜨거운 물 적합(Mazevet+ 2019)의 밀도 괄호" in why
              and re.search(r"채웠을 걸음 \d+ 개", why) is not None
              and re.search(r"질량 몫 [0-9][0-9.e+-]*", why) is not None)
        row(ok, f"ice {imf}: R1 이름 댄 거절(C122 고침)")

print("\n" + ("모두 통과" if not fails else f"{fails}건 실패"))
sys.exit(1 if fails else 0)
