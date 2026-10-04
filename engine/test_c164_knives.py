# C164 메모 5 판정 행 — 남긴 고침 둘(착지 걸음 옛 상 밀도 · 뜨거운 표면 반 걸음)을 끄면 되살아나고 켜면 사라지는 것으로 지킴
"""python3 engine/test_c164_knives.py — prereg-c164 post-freeze notes 1 and 5 (thresholds fixed before the test ran;
(b′) set from C164 §0.3's measured scan, post-result)."""
from __future__ import annotations

import contextlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import interior  # noqa: E402

fails = 0


def check(name: str, ok: bool, detail: str = "") -> None:
    global fails
    fails += not ok
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def _last_integrate(solve):
    """한 풀이의 마지막 적분 인자(고정 p_c · T_c)."""
    calls = []
    oi = interior.integrate

    def itr(*a, **k):
        calls.append((a, dict(k)))
        return oi(*a, **k)
    interior.integrate = itr
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            solve()
    finally:
        interior.integrate = oi
    return calls[-1]


def _radius(args, steps: int, **switches) -> float:
    a, k = args
    saved = {n: getattr(interior, n) for n in ("STEPS", "MAX_STEPS", *switches)}
    try:
        interior.MAX_STEPS = int(interior.MAX_STEPS * steps / interior.STEPS)
        interior.STEPS = steps
        for n, v in switches.items():
            setattr(interior, n, v)
        with contextlib.redirect_stdout(io.StringIO()):
            return interior.integrate(*a, **k).radius_m
    finally:
        for n, v in saved.items():
            setattr(interior, n, v)


print("C164 메모 1 (a) — 상 경계 착지 걸음의 단계 밀도(등온 지구, 고정 p_c): |R(1500) − R(1501)|")
earth = _last_integrate(lambda: interior.solve(1.0, core_mass_fraction=0.325))
d_off = abs(_radius(earth, 1500, CUT_STAGE_OLD_SIDE=False) - _radius(earth, 1501, CUT_STAGE_OLD_SIDE=False))
d_on = abs(_radius(earth, 1500, CUT_STAGE_OLD_SIDE=True) - _radius(earth, 1501, CUT_STAGE_OLD_SIDE=True))
check("끄면 새 상 밀도를 읽는 착지 걸음의 톱니가 되살아난다(> 20 m)", d_off > 20.0, f"{d_off:.2f} m")
check("켜면 톱니가 사라진다(≤ 2 m)", d_on <= 2.0, f"{d_on:.3f} m")

print("C164 메모 5 (b′) — 표면 반 걸음의 밀도(슈퍼지구 5 M⊕, 고정 p_c · T_c): STEPS 1495–1505 의 R 퍼짐")
se = _last_integrate(lambda: interior.solve(5.0, core_mass_fraction=0.325, potential_temperature=2300.0))


def _spread(args, lo, hi, **sw) -> float:
    rs = [_radius(args, n, **sw) for n in range(lo, hi + 1)]
    return (max(rs) - min(rs)) / 1e3


s_off = _spread(se, 1495, 1505, SURF_RHO=False)
f0 = interior.SURF_RHO_FALLBACKS[0]
s_on = _spread(se, 1495, 1505, SURF_RHO=True)
check("끄면 차가운 rho0 의 표면 톱니가 되살아난다(> 0.2 km)", s_off > 0.2, f"{s_off:.3f} km")
check("켜면 톱니가 사라진다(≤ 0.05 km)", s_on <= 0.05,
      f"{s_on:.4f} km · rho0 물러남 {interior.SURF_RHO_FALLBACKS[0] - f0} 번")

print("C164 메모 2 · 4 — 상수 밀도 층(화성 기저층 4050 kg/m³)을 이름 없는 실패 없이 걷는다")
_M, _CMF, _TP = 0.1074, 0.24, 1600.0
with contextlib.redirect_stdout(io.StringIO()):
    lay = interior.solve(_M, core_mass_fraction=_CMF, potential_temperature=_TP,
                         basal_layer_thickness_km=150.0, basal_layer_density=4050.0)
rec: list = []
try:
    with contextlib.redirect_stdout(io.StringIO()):
        st = interior.integrate(lay.values["core_pressure"] * 1e9, _M * interior.EARTH_MASS_KG, _CMF, 0.0, "fe_prem",
                                t_center=lay.values["core_temperature"], t_pot=_TP, record=rec,
                                basal_layer={"thickness_m": 150e3, "density": 4050.0})
    info = interior._BASAL_INFO.get(id(st))
    inside = sum(1 for row in rec if info["r_base"] <= row[0] < info["r_top"])
    err = None
except Exception as e:  # noqa: BLE001 — 이 줄이 지키는 것이 «이름 없는 실패가 없다» 이다
    inside, err = 0, f"{type(e).__name__}: {e}"
check("상수 밀도 층을 걸어도 예외가 없다(층 안 걸음 ≥ 2)", err is None and inside >= 2, err or f"층 안 {inside} 걸음")

print(f"  test_c164_knives — {'모두 통과' if not fails else f'실패 {fails}'}")
sys.exit(1 if fails else 0)
