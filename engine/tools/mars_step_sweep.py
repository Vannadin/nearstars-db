# C48 진단용 — C20 의 적분 스텝을 실제로 바꿔 가며 화성 발산이 스텝 탓인지 가르는 일회성 측정 스크립트
"""Does C20's fixed 4 Myr step cause the Mars divergence, or is the step innocent?

    python3 engine/tools/mars_step_sweep.py

**C48, 2026-09-08. 이름이 이 스크립트의 출력에 달려 있다.**

    스텝 줄여 살아남  →  C48 = "고정 스텝이 맨틀 시간상수를 못 따라간다"
    스텝 줄여도 발산  →  C48 = "미시연 영역" (논문은 화성을 안 돌린다). 스텝은 무죄

⚠ **왜 `integrate.__defaults__` 를 직접 바꾸는가 — 이 한 줄이 이 파일의 존재 이유다.**
`core_history.integrate` 의 시그니처가 `step_myr: float = STEP_MYR` 이고, **파이썬의 기본
인자는 정의 시점에 묶인다.** 그래서 `core_history.STEP_MYR = 0.1` 로 모듈 전역을 바꿔도
기본값은 4.0 그대로이고, `solve` 는 :217 에서 인자 없이 부른다. 2026-09-08 에 이 좌석이
정확히 그 함정에 빠져 **스텝 넷을 돌리고 넷 다 4 Myr 로 돌았다** — 출력 네 줄이 전부
"발산" 이라 그럴듯했고, "스텝 탓이 아니다" 라고 적을 뻔했다.

⚠ **그래서 이 스크립트는 먼저 자기가 살아 있음을 증명한다** (`prove_live`). 우리 규율에
이미 있는 것이다 — `engine/test_interior.py`:*"문턱 위에서 발화하고 아래에서 침묵해야
지표이지, **늘 발화하면 상수다**"*. 죽은 스윕은 스텝을 상수로 만든다.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import core_history as ch          # noqa: E402
from interior import solve as isolve  # noqa: E402

MARS = dict(mass_earth=0.1074, core_mass_fraction=0.24, radius_earth=0.5320, age_gyr=4.54)
EARTH = dict(mass_earth=1.0, core_mass_fraction=0.325, radius_earth=1.0, age_gyr=4.54)


def _params(body: dict, t_pot: float, core_init: float):
    ii = isolve(mass_earth=body["mass_earth"], core_mass_fraction=body["core_mass_fraction"],
                composition="earth_like", body_class="rocky", potential_temperature=t_pot)
    v = ii.values if hasattr(ii, "values") else ii
    r_b = v["cmb_temperature"] / t_pot
    return dict(core_radius_earth=v.get("core_radius"), cmb_pressure_gpa=v.get("cmb_pressure"),
                cmb_temperature=v["cmb_temperature"], potential_temperature=t_pot,
                core_initial_temperature=core_init,
                mantle_initial_potential_temperature=core_init / r_b,
                body_class="rocky", **body)


def run(body: dict, t_pot: float, core_init: float, step_myr: float):
    """한 번 적분한다. (출력 T_p, 걸음 수) — 발산이면 (None, None)."""
    saved = ch.integrate.__defaults__
    try:
        ch.integrate.__defaults__ = (step_myr,)
        r = ch.solve(**_params(body, t_pot, core_init))
        if not r.values:
            return None, None
        return r.values.get("mantle_potential_temperature_present"), r.values.get("history_steps")
    finally:
        ch.integrate.__defaults__ = saved


def prove_live() -> bool:
    """⚠ 스윕을 믿기 전에 스윕이 걸리는지 증명한다. 지구로, 스텝을 터무니없이 바꿔서."""
    _, n_small = run(EARTH, 1600.0, 4800.0, 4.0)
    _, n_big = run(EARTH, 1600.0, 4800.0, 200.0)
    print(f"살아있음 증명 — 지구, 스텝 4 Myr: {n_small} 걸음 · 200 Myr: {n_big}")
    ok = n_small is not None and n_small != n_big
    print("  " + ("✓ 스텝이 실제로 걸린다" if ok else "✗ 스윕이 죽었다 — 아래 수는 전부 무의미"))
    return ok


def main() -> int:
    if not prove_live():
        return 1
    print("\n화성 — 선언 T_pot 1600 K, 전이한 핵 초기 4800 K, 스텝만 바꾼다")
    print(f"{'스텝 Myr':>10} {'h/tau':>7}  결과      (tau ≈ 0.717 Myr, 지구는 36.3)")
    for step in (4.0, 1.0, 0.25, 0.05):
        t_p, n = run(MARS, 1600.0, 4800.0, step)
        got = f"T_p {t_p:.1f} K, {n} 걸음" if t_p else "발산"
        print(f"{step:10.2f} {step / 0.717:7.2f}  {got}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
