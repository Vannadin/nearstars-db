# 재료 경계 온도 점프 선언(interface_temperature_jumps) 시험 — 옛 얼음→외피 점프 흡수 · 거절 · 방향
"""`interior.solve(..., interface_temperature_jumps={...})` (prereg-interface-jumps, 덧붙임 3).

    python3 engine/test_interface_jumps.py

① 옛 선언 `boundary_temperature_jump=x` 와 새 이름 `{"ice/envelope": x}` 가 같은 답을 낸다(비트).
② 거절 — 두 이름 동시 · 모르는 경계 · 음수 · 온도 없음 · 층에 없는 경계 · 역산 갈래에 선언.
③ 방향 — 지구에 `core/rock` 500 K: 핵 쪽이 맨틀 쪽보다 정확히 500 K 뜨겁고, 점프 없는 판은 세 온도가 같다.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interior                        # noqa: E402
import run                             # noqa: E402
from test_ice_giant import _body, _fractions   # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


def same(a, b) -> bool:
    if isinstance(a, float) and isinstance(b, float):
        return a == b or (math.isnan(a) and math.isnan(b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if isinstance(a, (tuple, list)) and isinstance(b, (tuple, list)):
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


print("① 옛 선언 흡수 — boundary_temperature_jump 대 interface_temperature_jumps 의 ice/envelope")
_n, m, _r, m_core, m_hhe, t1bar = _body("Neptune")
imf, gmf = _fractions(m, m_core, m_hhe)
ICE = dict(body_class="ice_giant", core_mass_fraction=0.0, ice_mass_fraction=imf, gas_mass_fraction=gmf,
           potential_temperature=t1bar)
# ⚠ **먼저 한 번 데운다.** 같은 인수로 두 번 풀면 `bracket_invalid` 가 첫 호출에만 찍힌다(2026-09-24 측정:
#   `['ice_fr2015.density_at']` → `[]`) — 이 변경 전부터 있던 호출 순서 의존이다. 두 이름의 비교가 그것을 재지 않게
#   둘 다 데운 뒤에 푼다.
interior.solve(m, boundary_temperature_jump=100.0, **ICE)
old = interior.solve(m, boundary_temperature_jump=100.0, **ICE)
new = interior.solve(m, interface_temperature_jumps={"ice/envelope": 100.0}, **ICE)
check("해왕성 점프 100 K — 두 이름이 같은 적용 여부·등급·값(비트)",
      old.applicable == new.applicable and old.grade == new.grade and same(dict(old.values), dict(new.values))
      and (old.applicable or old.reason == new.reason),
      f"applicable {old.applicable} · grade {old.grade} · 값 {len(old.values)} 칸")

print("\n② 거절")
EARTH = dict(core_mass_fraction=0.325, composition="earth_like", potential_temperature=1600.0)
cases = [
    ("두 이름 동시", dict(boundary_temperature_jump=100.0, interface_temperature_jumps={"ice/envelope": 100.0}, **ICE),
     "같은 선언"),
    ("모르는 경계", dict(interface_temperature_jumps={"core/mantle": 10.0}, **EARTH), "모르는 경계"),
    ("음수", dict(interface_temperature_jumps={"core/rock": -1.0}, **EARTH), "0 이상"),
    ("온도 없음", dict(interface_temperature_jumps={"core/rock": 10.0}, core_mass_fraction=0.325,
                   composition="earth_like"), "potential_temperature"),
    ("층에 없는 경계", dict(interface_temperature_jumps={"ice/envelope": 10.0}, **EARTH), "층에 없다"),
]
for name, kw, word in cases:
    mass = m if kw.get("body_class") == "ice_giant" else 1.0
    r = interior.solve(mass, **kw)
    check(f"{name} → 이름 대고 거절", (not r.applicable) and word in (r.reason or ""), (r.reason or "")[:90])
mars, _ = run.load_body(Path(__file__).resolve().parent / "bodies" / "mars.yaml")
mars.inputs["interface_temperature_jumps"] = {"core/rock": {"value": 100.0, "grade": "declared", "source": "test"}}
r = interior._solve_from_state(mars)
check("역산 갈래(화성)에 선언 → 이름 대고 거절", (not r.applicable) and "역산" in (r.reason or ""), (r.reason or "")[:90])

print("\n③ 방향 — 지구 core/rock 500 K")
base = interior.solve(1.0, **EARTH)
hot = interior.solve(1.0, interface_temperature_jumps={"core/rock": 500.0}, **EARTH)
bv, hv = base.values, hot.values
check("점프 없는 판 — cmb_temperature = _core = _mantle (비트)",
      bv["cmb_temperature"] == bv["cmb_temperature_core"] == bv["cmb_temperature_mantle"],
      f"{bv['cmb_temperature']!r}")
check("점프 판 — 핵 쪽 − 맨틀 쪽 = 500 K (비트)",
      hot.applicable and hv["cmb_temperature_core"] - hv["cmb_temperature_mantle"] == 500.0
      and hv["cmb_temperature"] == hv["cmb_temperature_core"],
      f"핵 쪽 {hv.get('cmb_temperature_core')!r} · 맨틀 쪽 {hv.get('cmb_temperature_mantle')!r}")
check("점프 판 — 핵 쪽이 점프 없는 판보다 400 K 넘게 뜨겁다(맨틀 쪽은 같은 T_pot 에 묶임)",
      hot.applicable and hv["cmb_temperature_core"] > bv["cmb_temperature"] + 400.0,
      f"{hv['cmb_temperature_core'] - bv['cmb_temperature']:+.2f} K · 맨틀 쪽 차 "
      f"{hv['cmb_temperature_mantle'] - bv['cmb_temperature']:+.2f} K")
print(f"  [보고] 반지름 {bv['radius']:.6f} → {hv['radius']:.6f} R⊕ · nmoi {bv['nmoi']:.6f} → {hv['nmoi']:.6f} · "
      f"등급 {base.grade} → {hot.grade}")

print(f"  test_interface_jumps — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
