# 표면 암석권 층(lithosphere_thickness_km) 시험 — 거절 · 층 없는 판 비트 · 층 판의 자리
"""`interior.solve(..., lithosphere_thickness_km=..., surface_temperature_k=...)` (prereg-surface-lithosphere).

    python3 engine/test_lithosphere.py

① 거절 — 두께 ≤ 0 · 포텐셜 온도 없음 · 표면 온도 없음 · 두께 ≥ 맨틀 · 역산 갈래에 선언. 전부 칸 이름 대고.
② 층 없는 판 — 칸을 안 준 풀이와 `lithosphere_thickness_km=None` 풀이가 비트 같다.
③ 층 판 — 바닥 반지름 = R − D(1 m 안), 바닥 온도 = 그 자리 단열 온도(연속), 쏘기 조건(표면 = T_pot)은 그대로.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interior                        # noqa: E402
import run                             # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}{' — ' + detail if detail else ''}")
    fails += 0 if ok else 1


EARTH = dict(core_mass_fraction=0.325, composition="earth_like", potential_temperature=1600.0)

print("① 거절")
for name, kw, word in (
        ("두께 0", dict(lithosphere_thickness_km=0.0, surface_temperature_k=293.0, **EARTH), "0 보다"),
        ("두께 음수", dict(lithosphere_thickness_km=-5.0, surface_temperature_k=293.0, **EARTH), "0 보다"),
        ("포텐셜 온도 없음", dict(lithosphere_thickness_km=100.0, surface_temperature_k=293.0,
                             core_mass_fraction=0.325, composition="earth_like"), "potential_temperature"),
        ("표면 온도 없음", dict(lithosphere_thickness_km=100.0, **EARTH), "surface_temperature_k"),
        ("두께 ≥ 맨틀", dict(lithosphere_thickness_km=4000.0, surface_temperature_k=293.0, **EARTH), "맨틀 두께")):
    r = interior.solve(1.0, **kw)
    check(f"{name} → 이름 대고 거절", (not r.applicable) and word in (r.reason or ""), (r.reason or "")[:90])
r = interior.solve(1.0, interface_temperature_jumps={"rock/lithosphere": 10.0}, **EARTH)
check("암석권 경계 점프 → 이름 대고 거절(조용한 무시 없음)", (not r.applicable) and "암석권" in (r.reason or ""),
      (r.reason or "")[:90])
mars, _ = run.load_body(Path(__file__).resolve().parent / "bodies" / "mars.yaml")
mars.inputs["lithosphere_thickness_km"] = {"value": 300.0, "grade": "analog", "source": "test",
                                            "counter_evidence_searched": "test"}
r = interior._solve_from_state(mars)
check("역산 갈래(화성)에 선언 → 이름 대고 거절", (not r.applicable) and "역산" in (r.reason or ""), (r.reason or "")[:90])

print("\n② 층 없는 판 — 비트")
base = interior.solve(1.0, **EARTH)
none = interior.solve(1.0, lithosphere_thickness_km=None, surface_temperature_k=None, **EARTH)
check("칸 없음 = None (값 전부 비트)", base.applicable and dict(base.values) == dict(none.values),
      f"값 {len(base.values)} 칸")

print("\n③ 층 판 — 자리 · 연속 · 쏘기 조건")
D_KM, T_S = 135.0, 293.0
lit = interior.solve(1.0, lithosphere_thickness_km=D_KM, surface_temperature_k=T_S, **EARTH)
note = next((n for n in lit.notes if "표면 암석권" in n), "")
check("층 판이 풀린다 · 안내 한 줄", lit.applicable and bool(note), note[:120])
r_m = lit.values["radius"] * interior.EARTH_RADIUS_M
base_km = float(note.split("바닥 r ")[1].split(" km")[0]) if "바닥 r " in note else math.nan
check("바닥 반지름 = R − D (1 m + 인쇄 반올림 안)", abs(base_km * 1e3 - (r_m - D_KM * 1e3)) <= 1.0 + 0.5,
      f"바닥 {base_km:.3f} km · R − D {(r_m - D_KM * 1e3) / 1e3:.3f} km")
check("쏘기 조건 그대로 — 층 판도 converged", bool(lit.converged))
print(f"  [보고] 반지름 {base.values['radius']:.9f} → {lit.values['radius']:.9f} R⊕ · nmoi {base.values['nmoi']:.9f} → "
      f"{lit.values['nmoi']:.9f} · CMB T {base.values['cmb_temperature']:.4f} → {lit.values['cmb_temperature']:.4f} K")

print(f"  test_lithosphere — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
