# C55 의 판정 칸 넷을 잰다 — Fe–S 두 재질 × (핵 반지름, 핵 밀도), 화성 질량으로.
"""C55 verdict cells, measured rather than argued.

    python3 tools/c55_cells.py            # 선언된 조성(earth_like, cmf 0.325)
    python3 tools/c55_cells.py 0.24 0.20  # 핵질량비를 직접 주며 훑는다

⚠ **이 도구는 화성을 배선하지 않는다.** `engine/bodies/mars.yaml` 은 여전히
`core_material` 을 선언하지 않고, 그 칸은 오너 대기다. 여기서 나오는 수는 «그 재질을
선언하면 무엇이 나오는가» 이고, 그것이 C55 가 재기로 한 것이다.

창(Durán+ 2022 / Stähler+ 2021, 균질 맨틀 계열): 핵 반지름 1820–1870 km · 핵 밀도
5.7–6.3 g cm⁻³. Khan/Samuel 의 층상 계열은 1650–1675 km · 6.5–6.65 로 **다른 창**이고,
어느 계열을 택하는지는 오너 결정이다 — 여기서는 균질 계열 창만 표시한다.
"""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import eos                                                   # noqa: E402
import interior                                              # noqa: E402

M_EARTH = 5.97219e24
MARS_MASS_EARTH = 0.1074          # engine/bodies/mars.yaml 의 선언
T_POT = 1600.0                    # 맨틀 포텐셜 온도 — 사격의 온도 괄호가 받는 값
MATERIALS = ("fe_s_13wt_19gpa", "fe_s_19wt_19gpa")
R_WINDOW_KM = (1820.0, 1870.0)
RHO_WINDOW = (5.7, 6.3)
DECLARED_CMF = interior.COMPOSITIONS["earth_like"][0]


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
    for cmf in cmfs:
        tag = " ← 선언된 composition_intent: earth_like" if cmf == DECLARED_CMF else ""
        print(f"\ncmf = {cmf:.3f}{tag}")
        for m in MATERIALS:
            print(f"  {m:18} 사격층 {cell(m, cmf)}")
            print(f"  {'':18} 소비층 {consumer_cell(m, cmf)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
