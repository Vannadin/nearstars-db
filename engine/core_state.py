# 핵이 다이나모를 돌릴 수 있는 상태인가 — 핵의 압력·온도를 철의 융해곡선에 대서 상을 판정한다
"""Decide whether a rocky body's core is a conducting **liquid**.

    from core_state import solve

    solve(core_pressure=358.6, cmb_pressure=135.2, cmb_temperature=2526,
          core_temperature=2671, core_cmb_temperature=3760)
        → conductor_phase 'liquid_outer_solid_inner', 내핵 경계 ~3.5×10² GPa

`interior_layers` 는 핵의 **기하** 를 푼다. 그 핵이 다이나모를 돌릴 수 있느냐는 별개의
질문이고, rocky-planet-dynamo-methodology 가 "convective buoyancy flux through a
conducting liquid-iron core" 라고 적는 그 '액체' 가 이 노드의 출력이다. chain.yaml 이
2026-08-27 부터 그렇게 배선돼 있고, 그때 빠져 있던 조각이 융해곡선이었다.

**융해곡선만으로는 열리지 않았다.** 이 레시피를 짜면서 나온 것이 그 사실이다. 저쪽이
내는 `core_temperature` 는 표면에서 중심까지 이어 그린 단열선 하나 위의 값이라 핵이
맨틀의 단열선 위에 앉아 있고, 사이의 D″ 열경계층(지구에서 1200 K 이상)과 철의 진짜
단열 기울기가 둘 다 빠져 있다. 두 편향이 같은 방향이라 그 값은 **하한** 이고, 이 레시피는
하한을 하한으로 쓴다.

그래서 갈래가 둘이다.

* **선언이 없을 때** — 저쪽 지오섬을 하한으로 읽는다. 어느 깊이의 융해온도가 그 하한보다
  **낮으면** 거기는 액체다. 경계층은 핵을 데우기만 하므로 어떤 열류를 넣어도 그 판정은
  안 뒤집힌다. 반대쪽은 말할 수 없다 — 하한이 한쪽만 묶기 때문이다. 그래서 이 갈래는
  `liquid` 아니면 `undecided` 만 낸다. **`solid` 는 절대 내지 않는다.**
* **`core_cmb_temperature` 가 선언되면** — 핵 쪽 핵-맨틀 경계 온도에서 핵 자신의 단열선을
  올린다. 그러면 `solid` 도 말할 수 있고 내핵 경계도 찍힌다. 그 선언은 강착과 냉각 이력이
  정하는 값이고 이 레시피에 그 둘이 없다 — `potential_temperature` · `initial_porosity` ·
  `envelope_z` 와 같은 종류이고, 답이 거기 기대는 만큼 등급이 내려간다.
"""
from __future__ import annotations

import math
from dataclasses import replace as _dc_replace

import eos
from eos import (IRON_LIGHT_ELEMENT_FACTOR, IRON_MELT_MAX, IRON_MELT_SPLICE,
                 MATERIALS, PhaseGap, iron_t_melt)
from payload import Result, out_of_domain
from registry import recipe

RECIPE = "core-state-methodology"
VERSION = "1"

REFS = (
    "2015PEPI..244...69Z",      # Zhang+ 2015 — 순철 융해곡선 Simon 적합, 365 GPa 까지
    "2023PhRvR...5c3194G",      # González-Cataldo & Militzer 2023 — 300–5000 GPa 융해선
    "2022Sci...375..202K",      # Kraus+ 2022 — 1 TPa 까지의 융해 실측, 위 계산의 대조상대
    "2013Sci...340..464A",      # Anzellini+ 2013 — 내핵 경계 6230 ± 500 K
    "2019E&PSL.510...45S",      # Sinmyo+ 2019 — 같은 자리 5500 ± 220 K, 핵 온도 앵커
    "2002PhRvB..65p5118A",      # Alfè+ 2002 — 핵 조건의 그뤼나이젠 계수 ~1.5
    "2022ApJ...938..131Z",      # Zhang & Rogers 2022 — 20 % 내림 관례와 경계층 크기
    "1981PEPI...25..297D",      # PREM — 핵-맨틀 경계와 내핵 경계의 압력
)

# ── 핵의 단열선 ─────────────────────────────────────────────────────────
#
# 그뤼나이젠 계수가 상수면 단열선이 밀도의 거듭제곱으로 닫힌다.
#
#     T(P) = T_cmb · (ρ(P) / ρ_cmb)^γ
#
# **γ 는 새로 고른 값이 아니라 발표된 값이다.** Alfè, Price & Gillan 2002
# (arXiv:cond-mat/0107307) 이 h.c.p. 고체에 대해 "γ varies little with pressure or
# temperature for 100 < p < 300 GPa and 4000 < T < 6000 K, and has a value of ca. 1.5"
# 라고 적고, 액체 Hugoniot 에서도 "almost exactly constant, varying in the narrow range
# from 1.51 to 1.52 as p goes from 280 to 340 GPa" 라고 적는다. 그래서 상수로 두는 것이
# 근사가 아니라 그 논문의 결과다.
#
# eos.py 의 `gruneisen()` 항등식을 쓰지 않는 이유가 여기 있다. 그 항등식은 얼음에서
# SeaFreeze 의 γ 와 소수 넷째 자리까지 맞지만, 철에서는 Seager+ 2007 의 αK₀ 를 받는다 —
# 그건 밀도를 맞추려고 고른 **열압력** 상수이지 γ 의 출처가 아니고, 핵 압력대에서 0.22 를
# 낸다. 한 재료에 두 개의 γ 가 있는 셈이라 표류의 씨앗이고, 그래서 어느 쪽이 어느 질문에
# 쓰이는지를 여기와 eos.py 양쪽에 적어 둔다: 밀도는 αK₀, 핵의 단열선은 이 γ 다.
GAMMA_CORE = 1.5
GAMMA_RANGE_PA = (100e9, 340e9)     # 그 논문이 γ 를 확인한 압력 구간
# 같은 논문의 **액체** 값 (위 주석의 두 번째 인용, 새 출처 없음): 액체 Hugoniot 에서
# "1.51 to 1.52 as p goes from 280 to 340 GPa". GAMMA_CORE = 1.5 는 h.c.p. **고체** 의
# 값이고, fe_prem 은 PREM 외핵의 **액체** 밀도 적합이다 (eos.Phase.fit_state, 브리프 41).
# 그러므로 이 단열선은 액체 적합 위에 고체의 지수를 올린 것이다 — 브리프 41 이 밀도에서
# 잡는 병을 지수에서 한 층 위로 앓는 셈이다. 지구 기둥에서 중심 판정은 γ = 1.5145 에서
# 뒤집히는데, 그 값이 이 액체 범위 **안** 에 있다 (1.51 → −5.5 K 고체, 1.52 → +6.7 K 액체).
# GAMMA_CORE 는 바꾸지 않는다 — 판정이 맞게 나오도록 상수를 옮기는 일은 하지 않는다.
# 대신 뒤집힘점이 이 범위 안에 드는지를 내보내고, 그것이 "얇다" 의 기준이다 (아래).
GAMMA_LIQUID_RANGE = (1.51, 1.52)
GAMMA_LIQUID_RANGE_PA = (280e9, 340e9)

# ── 판정의 여유 (브리프 42) ──────────────────────────────────────────────
# 단열선에서 밀도는 비(ρ/ρ_cmb)로만 들어와 **정확히 상쇄** 된다 — ρ₀ 를 ±10 % 해도 중심
# 온도가 소수 열째 자리까지 안 움직인다. 상쇄되지 않는 것은 압축률(K₀)과 γ 이고, 지구
# 기둥에서 중심 판정은 K₀ = 194 GPa 에서 갈리는데 fe_prem 은 201 GPa 라 17.6 K (0.33 %)
# 지나 앉아 있으며, γ 는 1.5145 에서 뒤집히는데 선언이 1.5 다 (0.97 %). 답은 틀리지 않았다
# (지구는 외핵 액체·내핵 고체가 맞다) — 문제는 −17 K 판정과 −500 K 판정이 똑같이 보였다는
# 것이다. 그래서 여유와 두 뒤집힘점을 판정 옆에 내보낸다. **γ 도 K₀ 도 움직이지 않는다.**
#
# "얇다" 의 기준 (브리프 42 후속, 감사 ①): 중심 판정이 뒤집히는 γ 가 Alfè+ 2002 가 인쇄한
# γ 값들의 폭 — 고체 1.5 에서 액체 1.52 까지 — **안** 에 있으면 얇다. 여유는 단열선 쪽 양이므로
# 그 불확도도 단열선 쪽에서 잰다. 첫 판(d133ad41)은 융해곡선의 이음매 불일치 6.8 % 를
# 기준으로 썼는데, 그 수는 겹침 구간의 한 압력(≈312 GPa)에서 읽은 값이었고 실제 폭은
# 4.0–7.5 % (300 → 365 GPa, high/low − 1) 라 어느 압력에서 읽었는지가 빠져 있었다 — 이제
# 이음매 불일치는 **중심압에서의 국소값** 으로 정보로만 내보낸다 (melt_splice_disagreement).
# 거절이 아니다 — 답은 서 있고, 칼날 위라는 것을 독자가 안다.
# Alfè 의 고체·액체 두 인쇄값을 감싸는 **포락선** 이지 측정된 범위가 아니다. 액체 범위만 쓰면 thin 이
# 물리 진술로 읽히는데 GAMMA_CORE 는 여전히 고체값이라, 같은 혼합을 반대 방향으로 저지르는 셈이다.
GAMMA_SPAN = (min(GAMMA_CORE, GAMMA_LIQUID_RANGE[0]), GAMMA_LIQUID_RANGE[1])
MARGIN_THIN = "thin"
MARGIN_COMFORTABLE = "comfortable"
MARGIN_NOT_COMPUTABLE = "not-computable (lower bound, no core adiabat)"
K0_FLIP_SPAN = (0.5, 2.0)           # K₀ 뒤집힘점을 찾는 이분법의 배율 범위


def melt_splice_disagreement(p_pa: float) -> float | None:
    """철 융해곡선 두 조각의 국소 불일치 (high/low − 1), 겹침 구간 300 GPa–이음매(365 GPa)
    안에서만. 밖이면 None. 7.51 % (300) → 3.98 % (365), 단조."""
    lo_c, hi_c = eos.IRON_MELT_LOW, eos.IRON_MELT_HIGH
    if p_pa < hi_c[1] or p_pa > IRON_MELT_SPLICE:
        return None
    def simon(c):
        t0, p0, a, cc = c
        return t0 * (1.0 + (p_pa - p0) / a) ** cc
    return simon(hi_c) / simon(lo_c) - 1.0


def _center_temperature(material, p_c: float, p_cmb: float, t_cmb: float) -> float:
    rho_cmb = material.density(p_cmb, t_cmb, 0.0)
    return _adiabat(material, p_c, p_cmb, t_cmb, rho_cmb)


def gamma_flip(material, p_c: float, p_cmb: float, t_cmb: float) -> float:
    """중심 판정이 뒤집히는 γ. 닫힌 꼴: T_cmb·(ρ_c/ρ_cmb)^γ = T_melt,c."""
    rho_cmb = material.density(p_cmb, t_cmb, 0.0)
    rho_c = material.density(p_c, t_cmb, 0.0)
    return math.log(material.t_melt(p_c) / t_cmb) / math.log(rho_c / rho_cmb)


def k0_flip_gpa(material, p_c: float, p_cmb: float, t_cmb: float) -> float | None:
    """중심 판정이 뒤집히는 K₀ [GPa] — 첫 상의 K₀ 만 바꾼 사본으로 이분법. 상이 둘
    이상이거나 배율 범위 안에서 부호가 안 바뀌면 None (계산 못 한다고 말한다)."""
    if len(material.phases) != 1:
        return None
    ph = material.phases[0]
    t_melt_c = material.t_melt(p_c)

    def margin_at(k0: float) -> float:
        mat = _dc_replace(material, phases=(_dc_replace(ph, k0=k0),))
        return _center_temperature(mat, p_c, p_cmb, t_cmb) - t_melt_c

    lo, hi = ph.k0 * K0_FLIP_SPAN[0], ph.k0 * K0_FLIP_SPAN[1]
    if (margin_at(lo) > 0.0) == (margin_at(hi) > 0.0):
        return None
    return _cross(margin_at, lo, hi) / 1e9

# 발표된 지구 앵커. **우리 출력이 아니다** — 검증이 여기 기대고, 이 레시피는 읽지 않는다.
SINMYO_EARTH_CMB_K = (3760.0, 290.0)    # Sinmyo+ 2019 초록, 핵 쪽 핵-맨틀 경계 온도
SINMYO_EARTH_ICB_K = (5120.0, 390.0)    # 같은 초록, 내핵 경계 온도
PREM_ICB_GPA = 328.85                   # PREM 의 내핵 경계 압력

CONDUCTOR_LIQUID = "liquid"
CONDUCTOR_SOLID = "solid"
CONDUCTOR_MIXED = "liquid_outer_solid_inner"
CONDUCTOR_UNDECIDED = "undecided"

# 핵이 없는 천체, 그리고 고체 핵 이야기가 아닌 천체.
CORELESS_CLASSES = ("giant", "gas_giant", "ice_giant", "sub_neptune",
                    "brown_dwarf", "star")

# 거절문은 클래스마다 다르다 — 무엇이 다이나모를 돌리는지가 다르고, 서브넵튠은
# 돌릴 갈래가 아직 없기 때문이다. 한 문장으로 덮으면 서브넵튠에 금속수소를 말하게 된다.
_METALLIC_H = ("다이나모는 금속수소가 돌린다 — 그쪽은 dynamo_giant 의 갈래이고 "
               "철의 융해곡선과 무관하다.")
_CORELESS_WHY = {
    "giant": "거대행성의 " + _METALLIC_H,
    "gas_giant": "거대행성의 " + _METALLIC_H,
    "brown_dwarf": "갈색왜성의 " + _METALLIC_H,
    "ice_giant": "얼음거대행성의 다이나모는 이온성·초이온성 물이 돌린다 — 그쪽은 "
                 "dynamo_giant 의 아날로그 갈래이고 철의 융해곡선과 무관하다.",
    "sub_neptune": "서브넵튠의 철핵은 가스 외피 아래 앉아 있지만 그 핵을 받는 다이나모 "
                   "갈래가 아직 없다 — dynamo_giant 는 질량으로 배제하고 dynamo_rocky 는 "
                   "이 클래스를 받지 않는다. chain.yaml 의 gap 이다. 여기서 철의 "
                   "융해곡선을 대도 그 답을 읽을 소비처가 없다.",
    "star": "항성에는 금속 핵이 없다. 자기장은 대류층의 다이나모이고 이 엔진의 몫이 아니다.",
}


def _adiabat(material, p_pa: float, p_cmb: float, t_cmb: float,
             rho_cmb: float) -> float:
    """핵 쪽 경계 온도에서 올린 단열선의 온도 [K]. T ∝ ρ^γ 다."""
    rho = material.density(p_pa, t_cmb, 0.0)
    return t_cmb * (rho / rho_cmb) ** GAMMA_CORE


def _cross(f, lo: float, hi: float) -> float:
    """f 의 부호가 바뀌는 자리를 이분법으로 찾는다. 단조라 뿌리가 하나다."""
    f_lo = f(lo)
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if (f(mid) > 0.0) == (f_lo > 0.0):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def solve(core_pressure: float,
          cmb_pressure: float,
          core_temperature: float,
          cmb_temperature: float,
          core_material: str = "fe_prem",
          core_cmb_temperature: float | None = None,
          body_class: str | None = None) -> Result:
    """핵의 상을 판정한다. 압력은 GPa, 온도는 K.

    `core_pressure` 는 중심압, `cmb_pressure` 는 핵-맨틀 경계의 압력이고 둘 다
    `interior_layers` 의 출력이다. `core_temperature` · `cmb_temperature` 도 그쪽에서
    오는데, **핵의 온도가 아니라 하한** 이다 (모듈 주석을 보라).

    `core_cmb_temperature` 는 **선언** 이다. 핵 쪽 핵-맨틀 경계 온도이고, 그 값은 D″
    열경계층을 가로지르는 열류가 정한다 — `internal_heat_nontidal` 의 몫이라 여기서
    도출하지 않는다. 주지 않으면 하한 갈래로 간다."""
    inputs = {"core_pressure": core_pressure, "cmb_pressure": cmb_pressure,
              "core_temperature": core_temperature,
              "cmb_temperature": cmb_temperature,
              "core_material": core_material,
              "core_cmb_temperature": core_cmb_temperature,
              "body_class": body_class}

    if body_class in CORELESS_CLASSES:
        return out_of_domain(
            RECIPE, VERSION,
            f"'{body_class}' 에는 이 판정이 뜻이 없다. 이 노드가 묻는 것은 **금속 핵이 "
            f"액체인가** 이고, {_CORELESS_WHY[body_class]}",
            inputs=inputs, refs=REFS)

    if cmb_pressure <= 0.0 or core_pressure <= cmb_pressure:
        return out_of_domain(
            RECIPE, VERSION,
            f"핵이 없다 — 핵-맨틀 경계 압력 {cmb_pressure:.3g} GPa, 중심압 "
            f"{core_pressure:.3g} GPa. 핵질량분율이 0 이거나 미분화 천체다. "
            "미분화는 금속이 규산염에 섞여 있는 상태라 녹는점이 하나가 아니고, "
            "고상선과 액상선 두 곡선이 필요하다 — 이 파일에 그 둘이 없다.",
            inputs=inputs, refs=REFS)

    if core_temperature <= 0.0 or cmb_temperature <= 0.0:
        return out_of_domain(
            RECIPE, VERSION,
            "온도가 없다. interior_layers 에 포텐셜 온도를 선언하지 않으면 그 해는 "
            "등온이라 지오섬이 아예 없고, 융해곡선에 댈 것이 없다. 포텐셜 온도를 "
            "선언하면 하한 갈래가 열린다.",
            inputs=inputs, refs=REFS)

    material = MATERIALS.get(core_material)
    if material is None or material.melt_free_phases():
        return out_of_domain(
            RECIPE, VERSION,
            f"핵 재료 '{core_material}' 에 발표된 융해곡선이 없다. 곡선이 있는 것은 "
            "철(fe_prem · fe_eps)과 규산염(브리프 36 사슬)이고, antigorite 는 고온 "
            "운명이 융해가 아니라 탈수·분해라 비어 있는 것 자체가 판정이다.",
            inputs=inputs, refs=REFS)

    p_cmb, p_c = cmb_pressure * 1e9, core_pressure * 1e9
    if p_c > IRON_MELT_MAX:
        return out_of_domain(
            RECIPE, VERSION,
            f"중심압 {core_pressure / 1e3:.2f} TPa 가 철 융해곡선의 상한"
            f"({IRON_MELT_MAX / 1e12:.0f} TPa) 위다. 그 위는 González-Cataldo & "
            "Militzer 2023 의 계산 구간 밖이고, 이 레시피에는 그 압력의 융해선이 없다 — "
            "상태방정식은 12 TPa 까지 가지만 융해곡선은 5 TPa 에서 끝난다.",
            inputs=inputs, refs=REFS)

    try:
        t_melt_cmb = material.t_melt(p_cmb)
        t_melt_c = material.t_melt(p_c)
        rho_cmb = material.density(p_cmb, cmb_temperature, 0.0)
    except PhaseGap as gap:
        return out_of_domain(RECIPE, VERSION, gap.reason, inputs=inputs, refs=REFS)

    depressed = abs(material.phases[0].melt_scale - 1.0) > 1e-12
    notes = [
        f"융해곡선: {material.phases[0].melt_ref}. 핵-맨틀 경계 "
        f"{cmb_pressure:.1f} GPa 에서 {t_melt_cmb:.0f} K, 중심 {core_pressure:.1f} GPa "
        f"에서 {t_melt_c:.0f} K."]
    if depressed:
        notes.append(
            f"**가벼운 원소의 내림 {(1 - IRON_LIGHT_ELEMENT_FACTOR) * 100:.0f} % 는 "
            f"선언이다.** '{core_material}' 는 PREM 외핵 적합이라 가벼운 원소를 이미 품고 "
            "있고, 순철 곡선을 그대로 대면 녹는점을 너무 높게 잡는다. 내림폭은 발표된 "
            "열진화 모형들의 관례이고 (Stevenson+ 1983 → Zhang & Rogers 2022), 독립 "
            "검산이 같은 자리에 떨어진다 — Sinmyo+ 2019 의 지구 내핵 경계 온도 "
            f"{SINMYO_EARTH_ICB_K[0]:.0f} ± {SINMYO_EARTH_ICB_K[1]:.0f} K 를 순철 곡선의 "
            # 브리프 38 E: 이 백분율은 리터럴이었고(19.1), iron_t_melt 가 움직이면 조용히
            # 낡을 수였다. 이제 PREM ICB 압력(328.85 GPa)에서 계산한다 — 검산의 압력이
            # 어디였는지도 이 한 줄이 말한다. test_core_state 가 ~19 % 를 고정한다.
            f"같은 압력(PREM ICB {PREM_ICB_GPA:.2f} GPa) 값에 대면 "
            f"{(1.0 - SINMYO_EARTH_ICB_K[0] / iron_t_melt(PREM_ICB_GPA * 1e9)) * 100:.1f} % 다. "
            "두 수는 같은 주장이 아니라서 이 일치는 "
            "도출이 아니라 검산이고, 핵의 조성은 이 레시피가 도출하지 않는다.")
    if p_c > IRON_MELT_SPLICE:
        notes.append(
            f"중심압이 {IRON_MELT_SPLICE / 1e9:.0f} GPa 를 넘어 융해곡선이 두 번째 "
            "조각으로 넘어간다 (González-Cataldo & Militzer 2023). 겹치는 구간(300–365 GPa)에서 두 "
            "적합이 7.5 % (300 GPa) → 4.0 % (365 GPa, high/low − 1) 어긋나고, 그 폭은 같은 압력의 두 실험이 어긋나는 폭"
            "(Anzellini+ 2013 의 6230 ± 500 K 대 Sinmyo+ 2019 의 5500 ± 220 K, 13 %)보다 "
            "좁다. 이음매 근처의 판정은 그 폭만큼 흔들린다.")

    # ── 갈래 1: 선언이 없다. 저쪽 지오섬을 하한으로 읽는다 ────────────────
    if not core_cmb_temperature:
        liquid_cmb = cmb_temperature > t_melt_cmb
        liquid_c = core_temperature > t_melt_c
        notes.append(
            "**핵 쪽 경계 온도가 선언되지 않았다.** interior_layers 의 지오섬을 하한으로 "
            "읽는다 — 그 값은 맨틀 단열선을 핵까지 이어 그린 것이고 D″ 열경계층과 철의 "
            "진짜 단열 기울기가 둘 다 빠져 있어서, 두 편향이 같은 방향(아래)이다. 그래서 "
            f"'액체' 는 말할 수 있고 '고체' 는 말할 수 없다. 하한: 경계 "
            f"{cmb_temperature:.0f} K · 중심 {core_temperature:.0f} K.")
        if liquid_cmb and liquid_c:
            phase, reason = CONDUCTOR_LIQUID, (
                f"핵 전체가 액체다. 하한만으로도 융해온도를 넘는다 — 경계에서 "
                f"{cmb_temperature - t_melt_cmb:+.0f} K, 중심에서 "
                f"{core_temperature - t_melt_c:+.0f} K. 열경계층은 핵을 데우기만 하므로 "
                "어떤 열류를 넣어도 이 판정은 안 뒤집힌다.")
            grade = "analog"
        else:
            phase, reason = CONDUCTOR_UNDECIDED, (
                "판정하지 않는다. 하한이 융해온도 아래라 액체라고 말할 수 없고, 하한은 "
                "한쪽만 묶으므로 고체라고도 말할 수 없다 — 빠진 열이 얼마인지를 "
                "`core_cmb_temperature` 로 선언하면 이 노드가 답한다. 지구에서 그 값은 "
                f"{SINMYO_EARTH_CMB_K[0]:.0f} ± {SINMYO_EARTH_CMB_K[1]:.0f} K 이고 "
                "(Sinmyo+ 2019), 이 적분이 내는 맨틀 쪽 값보다 1200 K 넘게 높다.")
            grade = "judgment"
        return Result(
            recipe=RECIPE, version=VERSION, regime="lower_bound", reason=reason,
            grade=grade, inputs=inputs, refs=REFS,
            values={"conductor_phase": phase,
                    "cmb_melt_temperature": t_melt_cmb,
                    "center_melt_temperature": t_melt_c,
                    "core_cmb_temperature_used": cmb_temperature,
                    "core_center_temperature_used": core_temperature,
                    "icb_pressure": 0.0,
                    # 브리프 42 ④: 하한 갈래에는 단열선이 없어 뒤집힘점을 계산할 수 없다.
                    # 여유는 **하한 대비** 로만 적고, 조건은 못 한다고 이름 붙인다.
                    "center_margin": core_temperature - t_melt_c,
                    "cmb_margin": cmb_temperature - t_melt_cmb,
                    "center_margin_fraction": (core_temperature - t_melt_c) / t_melt_c,
                    "gamma_flip": None,
                    "gamma_flip_in_alfe_range": None,
                    "k0_flip": None,
                    "melt_splice_disagreement": melt_splice_disagreement(p_c),
                    "margin_condition": MARGIN_NOT_COMPUTABLE},
            units={"conductor_phase": "", "cmb_melt_temperature": "K",
                   "center_melt_temperature": "K",
                   "core_cmb_temperature_used": "K",
                   "core_center_temperature_used": "K",
                   "icb_pressure": "GPa",
                   "center_margin": "K", "cmb_margin": "K",
                   "center_margin_fraction": "dimensionless",
                   "gamma_flip": "dimensionless", "gamma_flip_in_alfe_range": "",
                   "k0_flip": "GPa", "melt_splice_disagreement": "dimensionless",
                   "margin_condition": ""},
            notes=tuple(notes))

    # ── 갈래 2: 핵 자신의 단열선 ──────────────────────────────────────────
    t_cmb_core = float(core_cmb_temperature)
    t_center = _adiabat(material, p_c, p_cmb, t_cmb_core, rho_cmb)

    def margin(p_pa: float) -> float:
        return _adiabat(material, p_pa, p_cmb, t_cmb_core, rho_cmb) - material.t_melt(p_pa)

    m_cmb, m_c = t_cmb_core - t_melt_cmb, t_center - t_melt_c
    icb = 0.0
    if m_cmb > 0.0 and m_c > 0.0:
        phase = CONDUCTOR_LIQUID
    elif m_cmb <= 0.0 and m_c <= 0.0:
        phase = CONDUCTOR_SOLID
    elif m_cmb > 0.0 >= m_c:
        phase = CONDUCTOR_MIXED
        icb = _cross(margin, p_cmb, p_c) / 1e9
    else:
        # 경계가 고체인데 중심이 액체다. 융해곡선이 단열선보다 가파르다는
        # González-Cataldo & Militzer 2023 의 결과와 어긋나므로, 값이 아니라 사실을 낸다.
        phase = CONDUCTOR_UNDECIDED
        notes.append(
            "**단열선과 융해곡선이 거꾸로 만난다** — 경계가 고체인데 중심이 액체다. "
            "González-Cataldo & Militzer 2023 은 융해선이 단열선보다 늘 가파르다고 "
            "적으므로(그래서 결정화가 늘 중심에서 시작한다) 이 배치는 물리가 아니라 "
            "입력이 어긋났다는 뜻이다. 판정하지 않는다.")

    notes.append(
        f"**핵 쪽 경계 온도 {t_cmb_core:.0f} K 는 선언이다.** D″ 열경계층을 가로지르는 "
        "열류가 정하는 값이고, 그 열류는 `internal_heat_nontidal` 의 출력이라 이 레시피가 "
        f"도출하지 않는다. 이 적분이 낸 맨틀 쪽 값은 {cmb_temperature:.0f} K 이고 차이가 "
        f"{t_cmb_core - cmb_temperature:+.0f} K 다. Zhang & Rogers 2022 는 자기 모형에서 "
        "그 차이를 1 M⊕ 에서 ~240 K, 3 M⊕ 에서 ~1880 K 로 내는데, 그 폭 자체가 이 값이 "
        "모형에 달렸다는 뜻이다. 등급을 analog 로 내린다.")
    lo, hi = GAMMA_RANGE_PA
    gamma_out_of_range = p_c > hi
    if gamma_out_of_range:
        notes.append(
            f"핵 단열선의 γ = {GAMMA_CORE} 는 Alfè+ 2002 가 {lo / 1e9:.0f}–{hi / 1e9:.0f} GPa "
            f"에서 확인한 값이고, 이 천체의 중심압 {core_pressure:.0f} GPa 는 그 위다. "
            "그 위에서 γ 가 어떻게 흐르는지를 이 레시피는 모른다 — 상수로 끌고 간다.")
    # 액체 범위는 자기 구간(280–340 GPa)으로 따로 판정한다 (감사, 브리프 42 후속). 두 상한이
    # 340 으로 같은 것은 우연이고, 100–280 GPa 의 중심은 고체 구간 안·액체 구간 밖이다.
    liq_lo, liq_hi = GAMMA_LIQUID_RANGE_PA
    liquid_gamma_out_of_range = not (liq_lo <= p_c <= liq_hi)
    if liquid_gamma_out_of_range:
        notes.append(
            f"같은 논문의 액체 γ {GAMMA_LIQUID_RANGE[0]}–{GAMMA_LIQUID_RANGE[1]} 은 "
            f"{liq_lo / 1e9:.0f}–{liq_hi / 1e9:.0f} GPa 에서 확인된 값이고, 이 천체의 중심압 "
            f"{core_pressure:.0f} GPa 는 그 {'위' if p_c > liq_hi else '아래'}다 — 아래의 뒤집힘 "
            "비교는 그 값도 외삽해서 쓴다.")

    # ── 브리프 42: 판정의 여유와 두 뒤집힘점 ─────────────────────────────
    frac_c = m_c / t_melt_c
    g_flip = gamma_flip(material, p_c, p_cmb, t_cmb_core)
    k_flip = k0_flip_gpa(material, p_c, p_cmb, t_cmb_core)
    k0_now = material.phases[0].k0 / 1e9
    in_span = GAMMA_SPAN[0] <= g_flip <= GAMMA_SPAN[1]
    splice = melt_splice_disagreement(p_c)
    liquid_fit = material.phases[0].fit_state == "liquid"
    thin = in_span
    condition = MARGIN_THIN if thin else MARGIN_COMFORTABLE
    notes.append(
        f"**판정의 여유 ({condition}).** 중심에서 단열선 − 융해온도 = {m_c:+.1f} K "
        f"({frac_c * 100:+.2f} % of T_melt), 경계에서 {m_cmb:+.1f} K. 중심 판정은 γ = "
        f"{g_flip:.4f} 에서 뒤집힌다 (선언 {GAMMA_CORE}, {(g_flip / GAMMA_CORE - 1) * 100:+.2f} %)"
        + (f", K₀ = {k_flip:.1f} GPa 에서 뒤집힌다 (이 재료 {k0_now:.1f} GPa)"
           if k_flip is not None else
           f"; K₀ 뒤집힘점은 계산하지 않았다 (상이 {len(material.phases)}개이거나 "
           f"배율 {K0_FLIP_SPAN} 안에 없다)")
        + ". 밀도 자체는 비로만 들어와 상쇄된다 — 갈리는 것은 압축률과 γ 다. "
        + (f"**얇다**: 뒤집히는 γ {g_flip:.4f} 가 Alfè+ 2002 가 인쇄한 γ 의 폭 "
           f"{GAMMA_SPAN[0]}–{GAMMA_SPAN[1]} (고체 {GAMMA_CORE}, 액체 {GAMMA_LIQUID_RANGE[0]}–"
           f"{GAMMA_LIQUID_RANGE[1]} @ {GAMMA_LIQUID_RANGE_PA[0] / 1e9:.0f}–{GAMMA_LIQUID_RANGE_PA[1] / 1e9:.0f} GPa) "
           "안에 있다 — 같은 논문의 액체 값을 쓰면 판정이 모호해진다"
           + ("; 그리고 이 천체의 중심압은 "
              + " · ".join(s for s, on in (
                    (f"고체 검증 구간({lo / 1e9:.0f}–{hi / 1e9:.0f} GPa)", gamma_out_of_range),
                    (f"액체 구간({liq_lo / 1e9:.0f}–{liq_hi / 1e9:.0f} GPa)", liquid_gamma_out_of_range)) if on)
              + " 밖이라 그 γ 는 외삽이다"
              if (gamma_out_of_range or liquid_gamma_out_of_range) else "")
           + (f". 액체 γ 의 위끝({GAMMA_LIQUID_RANGE[1]})에서는 중심 판정이 액체로 넘어간다 — "
              f"**선언된 {GAMMA_CORE} 가 이 레시피에서 내핵의 존재 자체를 떠받치고 있다.** 상수는 "
              "옮기지 않는다(답이 맞게 나오도록 상수를 옮기는 일은 금지다); 그 금지의 비용이 이것이다"
              if liquid_fit and (m_c < 0.0) else "")
           + ". 답은 서 있다 — 칼날 위라는 것을 라벨이 말한다."
           if thin else
           f"뒤집히는 γ {g_flip:.4f} 가 Alfè+ 2002 의 γ 폭 {GAMMA_SPAN[0]}–{GAMMA_SPAN[1]} 밖이다.")
        + (f" **고체의 γ {GAMMA_CORE} 를 액체 밀도 적합({core_material}, fit_state liquid) 위에 "
           "올렸다** — 브리프 41 이 밀도에서 잡는 병을 지수에서 앓는 자리다; 상수는 옮기지 않았다."
           if liquid_fit else "")
        + (f" 철 융해곡선 이음매의 국소 불일치는 중심압에서 {splice * 100:.2f} % (high/low − 1, 정보)."
           if splice is not None else "")
        + " γ 와 K₀ 는 움직이지 않았다 (core-margin-context-notes.md).")

    reason = (f"핵-맨틀 경계 {cmb_pressure:.1f} GPa / {t_cmb_core:.0f} K 에서 γ = "
              f"{GAMMA_CORE} 의 단열선을 올리면 중심 {core_pressure:.1f} GPa 에서 "
              f"{t_center:.0f} K 다. 융해온도가 경계 {t_melt_cmb:.0f} K · 중심 "
              f"{t_melt_c:.0f} K 이므로 "
              + {CONDUCTOR_LIQUID: "핵 전체가 액체다.",
                 CONDUCTOR_SOLID: "핵 전체가 고체다 — 다이나모를 돌릴 액체가 없다.",
                 CONDUCTOR_MIXED: f"외핵이 액체이고 내핵이 고체다 (경계 {icb:.0f} GPa).",
                 CONDUCTOR_UNDECIDED: "판정하지 않는다."}[phase])

    return Result(
        recipe=RECIPE, version=VERSION, regime="declared_core_adiabat", reason=reason,
        grade="judgment" if phase == CONDUCTOR_UNDECIDED else "analog",
        inputs=inputs, refs=REFS,
        values={"conductor_phase": phase,
                "cmb_melt_temperature": t_melt_cmb,
                "center_melt_temperature": t_melt_c,
                "core_cmb_temperature_used": t_cmb_core,
                "core_center_temperature_used": t_center,
                "icb_pressure": icb,
                "center_margin": m_c,
                "cmb_margin": m_cmb,
                "center_margin_fraction": frac_c,
                "gamma_flip": g_flip,
                "gamma_flip_in_alfe_range": in_span,
                "k0_flip": k_flip,
                "melt_splice_disagreement": splice,
                "margin_condition": condition},
        units={"conductor_phase": "", "cmb_melt_temperature": "K",
               "center_melt_temperature": "K",
               "core_cmb_temperature_used": "K",
               "core_center_temperature_used": "K",
               "icb_pressure": "GPa",
               "center_margin": "K", "cmb_margin": "K",
               "center_margin_fraction": "dimensionless",
               "gamma_flip": "dimensionless", "gamma_flip_in_alfe_range": "",
               "k0_flip": "GPa", "melt_splice_disagreement": "dimensionless",
               "margin_condition": ""},
        notes=tuple(notes))


@recipe("core_state")
def _from_state(state):
    from interior import COMPOSITIONS
    composition = state.get("composition_intent", "earth_like")
    core_material = COMPOSITIONS.get(composition, (0, 0, 0, "fe_prem"))[3]
    return solve(
        core_pressure=state["core_pressure"],
        cmb_pressure=state["cmb_pressure"],
        core_temperature=state["core_temperature"],
        cmb_temperature=state["cmb_temperature"],
        core_material=core_material,
        # 핵 쪽 경계 온도는 **선언** 이다. 없으면 하한 갈래로 간다.
        core_cmb_temperature=state.get("core_cmb_temperature"),
        body_class=state.get("body_class"),
    )
