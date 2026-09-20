# C55 의 판정 칸 넷을 잰다 — Fe–S 두 재질 × (핵 반지름, 핵 밀도), 화성 질량으로.
"""C55 verdict cells, measured rather than argued.

    python3 tools/c55_cells.py            # 화성의 핵질량비 — 선언이 있으면 그 값, 없으면 역산이 푼 값
    python3 tools/c55_cells.py 0.24 0.20  # 핵질량비를 직접 주며 훑는다

⚠ **이 도구는 화성을 배선하지 않는다.** `engine/bodies/mars.yaml` 은 여전히
`core_material` 을 선언하지 않고, 그 칸은 오너 대기다. 여기서 나오는 수는 «그 재질을
선언하면 무엇이 나오는가» 이고, 그것이 C55 가 재기로 한 것이다.

창(Durán+ 2022 한 논문의 두 축, 균질 맨틀 계열): 핵 반지름 1820–1870 km · 핵 밀도
6.0–6.2 g cm⁻³ (오너 결정 2026-09-20). Khan/Samuel 의 층상 계열은 1650–1675 km · 6.5–6.65 로 **다른 창**이고,
어느 계열을 택하는지는 오너 결정이다 — 여기서는 균질 계열 창만 표시한다.
"""
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import eos                                                   # noqa: E402
import interior                                              # noqa: E402

M_EARTH = 5.97219e24
MARS_MASS_EARTH = 0.1074          # engine/bodies/mars.yaml 의 선언
T_POT = 1600.0                    # 맨틀 포텐셜 온도 — 사격의 온도 괄호가 받는 값
MATERIALS = ("fe_s_13wt_19gpa", "fe_s_19wt_19gpa")
R_WINDOW_KM = (1820.0, 1870.0)
#: 선언된 cmf 에서 창을 벗어나는 **사격층** 칸의 수, 2026-09-17 측정. ⚠ 이 수는 허용치가 아니라
#: **기록**이다 — 늘면 FAIL, 줄면 사람이 내린다. C55 가 연 항목이 닫히면 0 이 된다.
RECORDED_OUTSIDE = 2
RHO_WINDOW = (6.0, 6.2)
def _mars_cmf() -> tuple[float, str]:
    """⚠ **화성이 실제로 푸는 핵질량비는 프리셋의 것이 아니다** (브리프 182 A).

    `mars.yaml` 이 `core_mass_fraction` 을 직접 선언하고 `interior.solve` 는 선언을 프리셋보다
    앞세운다. 프리셋 값(earth_like 0.325)을 «선언된 조성» 이라 부르면 이 표가 **화성이 안 푸는
    조성**을 화성의 것으로 인쇄한다 — 그 라벨이 실제로 틀린 채 하루를 돌았다."""
    import yaml
    doc = yaml.safe_load((Path(__file__).resolve().parent.parent
                          / "bodies" / "mars.yaml").read_text(encoding="utf-8"))
    got = (doc.get("inputs") or {}).get("core_mass_fraction")
    if got is not None:
        return float(got), "mars.yaml 이 선언한 핵질량비"
    # ⚠ **선언이 없으면 프리셋이 아니라 «엔진이 푸는 값»이 답이다** (C57 (c), 2026-09-20).
    #   여기 있던 폴백은 `earth_like` 의 0.325 를 돌려줬는데, 화성이 실제로 푸는 값은
    #   0.2396 이다 — 위 독스트링이 경고한 «화성이 안 푸는 조성을 화성의 것으로 인쇄» 가
    #   선언을 지운 날 그대로 발화했다. 그래서 역산을 불러 **푼 값**을 받고, 라벨도 그렇게 적는다.
    res = interior.infer_composition(
        float((doc.get("inputs") or {})["mass_earth"]),
        float((doc.get("inputs") or {})["radius_earth"]),
        ice_allowed=False, potential_temperature=T_POT)
    cmf = res.values.get("core_mass_fraction", res.inputs.get("core_mass_fraction"))
    if cmf is None:
        raise SystemExit(
            "화성의 핵질량비를 못 얻었다 — mars.yaml 에 선언이 없고 역산도 값을 안 냈다. "
            "이 표는 그 수 없이는 «선언된 행» 을 못 고르므로 인쇄하지 않는다.")
    return float(cmf), "역산이 푼 핵질량비 (mars.yaml 에 선언 없음)"


DECLARED_CMF, CMF_SOURCE = _mars_cmf()


PROBE = "_c55_probe"          # 아래 `consumer_cell` 이 잠깐 등록했다 지우는 조성 이름


def cell(material: str, cmf: float) -> str:
    """사격 층(`shoot`)의 한 칸. 풀리면 두 수와 창 판정, 안 풀리면 거절의 첫 문장."""
    try:
        # ⚠ `shoot` 로 부른다. `_shoot_pressure` 를 직접 부르면 «답이 적합 밖이면 거절» 하는
        # 자리(C60 (c))를 건너뛰어, 엔진이 안 내놓을 수를 이 표만 인쇄하게 된다.
        st, ok = interior.shoot(
            MARS_MASS_EARTH * M_EARTH, cmf, 0.0, material,
            potential_temperature=T_POT)
    except eos.PhaseGap as gap:
        return (f"거절 @ {gap.pressure_pa / 1e9:.4f} GPa · "
                f"{gap.reason.splitlines()[0][:76]}")
    if not st.core_radius_m:
        return "핵 없음 (cmf = 0)"
    r_km = st.core_radius_m / 1e3
    rho = (cmf * MARS_MASS_EARTH * M_EARTH
           / (4.0 / 3.0 * math.pi * st.core_radius_m ** 3) / 1e3)
    r_in = R_WINDOW_KM[0] <= r_km <= R_WINDOW_KM[1]
    rho_in = RHO_WINDOW[0] <= rho <= RHO_WINDOW[1]
    return (f"R_core {r_km:7.1f} km [{'창 안' if r_in else '창 밖'}] · "
            f"rho_core {rho:5.3f} g/cm3 [{'창 안' if rho_in else '창 밖'}] · "
            f"p_cmb {st.p_cmb / 1e9:8.5f} GPa · 수렴 {ok}")


def consumer_cell(material: str, cmf: float) -> str:
    """**소비 경로**(`interior.solve`)의 같은 칸 — 노드가 실제로 받는 층이다.

    ⚠ 두 층의 수가 같지 않다. 기록되는 핵-맨틀 경계가 약 **0.5 kPa** 어긋나고, 그 폭이
    19 GPa 바닥 바로 위에서 판정을 가른다 (감사석 2026-09-10, 브리프 181 B). 그래서 이 표는
    두 층을 **나란히** 인쇄한다 — 어느 층의 수인지 안 적으면 다음 사람이 둘을 섞는다.

    `solve` 는 `core_material` 을 인자로 받지 않고 조성 프리셋에서 읽으므로, 여기서 이름 하나를
    잠깐 등록했다 지운다. 프리셋 표 자체는 안 바뀐다."""
    interior.COMPOSITIONS[PROBE] = (cmf, 0.0, 0.0, material)
    try:
        res = interior.solve(MARS_MASS_EARTH, composition=PROBE,
                             potential_temperature=T_POT, body_class="rocky")
    finally:
        interior.COMPOSITIONS.pop(PROBE, None)
    if not res.applicable:
        return f"거절 · {res.reason.splitlines()[0][:76]}"
    return f"p_cmb {res.values['cmb_pressure']:8.5f} GPa · 수렴 {res.converged}"


def main(argv: list[str]) -> int:
    cmfs = [float(a) for a in argv[1:]] or [DECLARED_CMF]
    print(f"C55 판정 칸 — 화성 질량 {MARS_MASS_EARTH} M⊕ · T_pot {T_POT:.0f} K")
    print(f"창: 핵 반지름 {R_WINDOW_KM[0]:.0f}–{R_WINDOW_KM[1]:.0f} km · "
          f"핵 밀도 {RHO_WINDOW[0]}–{RHO_WINDOW[1]} g/cm3 (균질 맨틀 계열)")
    # ⚠ **앞서 여기 「창은 보드의 수이고 1820–1870 은 Stähler 의 두 구간을 섞은 것」이라 적었다 —
    #   틀렸다** (미결 24, 2026-09-20). Durán+ 2022 초록이 1820–1870 km 를 **직접 인쇄**하고,
    #   1790–1870 을 **«previously»** 라 부른다. 섞여 있던 것은 반지름이 아니라 **축 사이**였다 —
    #   반지름은 Durán, 밀도 5.7–6.3 은 Durán 이 previously 라 부르는 Stähler 값이었다.
    #   오너 결정으로 **두 축을 Durán 하나로** 맞춘다. 반지름은 무접촉, 밀도가 6.0–6.2 로 좁아진다.
    print("  ⚠ 창은 Durán+ 2022 한 논문의 두 축이다 — 반지름 1820–1870 km · 밀도 6.0–6.2 g/cm3. "
          "예전에는 밀도만 Stähler+ 2021 의 5.7–6.3 이었고, 그것은 Durán 이 «previously» 라 부르는 값이다")
    # ⚠ **창 밖을 셀 수 있게 한다** (작업 규율 곁가지, 2026-09-17). 예전에는 이 도구가 «창 안 /
    #   창 밖» 을 인쇄하고도 **언제나 0 을 돌려줬다** — 창을 벗어나도 게이트가 초록이었다.
    #   비교를 인쇄하는 도구는 그 비교에 실패할 수 있어야 한다.
    #   ⚠ **판정은 선언된 핵질량비의 행에만 건다.** 나머지 cmf 는 탐침이고, 탐침이 창을
    #   벗어나는 것은 이 도구가 찾으라고 있는 것이지 결함이 아니다.
    outside = 0
    for cmf in cmfs:
        declared = cmf == DECLARED_CMF
        tag = f" ← {CMF_SOURCE}" if declared else ""
        print(f"\ncmf = {cmf:.3f}{tag}")
        for m in MATERIALS:
            shoot = cell(m, cmf)
            print(f"  {m:18} 사격층 {shoot}")
            print(f"  {'':18} 소비층 {consumer_cell(m, cmf)}")
            if declared and "창 밖" in shoot:
                outside += 1
    # ⚠ **오늘의 창 밖 둘은 기록된 어긋남이다** (C55 자신이 연 항목). 그 둘을 FAIL 로 올리면
    #   이미 아는 사실로 게이트가 빨개지고, 아무도 안 고치는 붉은 줄은 곧 무시된다.
    #   그래서 **래칫**으로 둔다 — 기록된 수를 넘으면 그때 FAIL 이다. mars.yaml 의
    #   `recorded_disagreement` 와 같은 형식이고, 닫는 것은 사람이지 이 줄이 아니다.
    print(f"\n  창 밖 칸 {outside} 개 · 기록된 수 {RECORDED_OUTSIDE} 개 — 창은 "
          f"R_core {R_WINDOW_KM[0]:.0f}–{R_WINDOW_KM[1]:.0f} km · "
          f"rho_core {RHO_WINDOW[0]}–{RHO_WINDOW[1]} g/cm3")
    if outside > RECORDED_OUTSIDE:
        print(f"  [FAIL] 화성의 cmf {DECLARED_CMF:.3f} ({CMF_SOURCE}) 에서 창 밖 칸이 기록된 수보다 많다 "
              f"({outside} > {RECORDED_OUTSIDE})")
        return 1
    if outside < RECORDED_OUTSIDE:
        print(f"  [기록·해소?] 창 밖 칸이 기록된 수보다 적다 ({outside} < {RECORDED_OUTSIDE}) — "
              f"기록을 사람이 내려라")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
