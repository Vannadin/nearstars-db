# 압력이 공극을 닫는 관계 φ(P) — 상수 하나하나가 어느 논문 어느 표에서 왔는지 붙여둔다
"""How much void space survives at a given pressure.

    from porosity import porosity, LAW_FOR
    porosity("rock", 10e6)      → 0.466   (실리카, 10 MPa)
    porosity("ice", 10e6)       → 0.221   (물얼음, 10 MPa)

작은 천체는 자기중력이 약해서 암석을 다 으깨지 못한다. 남은 빈틈이 평균밀도를
낮추고, 그래서 질량과 반지름만 보면 실제보다 가벼운 물질로 이루어진 것처럼 보인다.
이 파일은 **그 빈틈이 압력의 함수라는 물리** 를 담는다. 질량에 맞춘 곡선이 아니다 —
관측 몇 개에 지수함수를 맞추면 값은 나오지만 왜 그 값인지 물을 수 없다.

**기준이 되는 문턱이 하나 있다.** 규산염 입자는 압력이 약 10 MPa 에 닿으면 깨지기
시작한다 (Britt+ 2002; Carry 2012 §5.2 가 "silicate grains start to fracture when the
pressure reaches ∼10⁷ Pa" 로 인용한다). 그래서 내부압이 거기까지 못 가는 천체는
공극을 그대로 들고 있고, 넘는 천체는 잃는다. 관측이 그 문턱을 확인해 준다 — Carry
2012 §5.2 는 "The pressure inside an object with a mass lower than ≈10²⁰ kg never
reaches 10⁷ Pa" 라고 적고, 같은 절에서 10²⁰ kg 위의 천체가 전부 macroporosity ≈ 0
축에 몰려 있고 그 아래는 0에서 70 %까지 흩어져 있다고 보고한다.

**전이질량은 입력이 아니라 결과다.** 이 파일에 10²⁰ kg 은 상수로 들어 있지만 계산에
쓰지 않는다. 솔버가 압력 프로파일을 풀고 그 문턱을 넘는지 보면 전이질량이 저절로
나오는데, test_porosity.py 가 그 값이 발표된 10¹⁹–10²⁰ kg 구간에 떨어지는지 확인한다.

## 관계식

Bierson, Nimmo & McKinnon 2019 (Icarus 326, 10) 의 식 (1)(2) 를 그대로 쓴다. 그들이
KBO 18개의 발표 밀도를 이 식으로 설명했고, 계수는 실험실 압밀 실험에서 왔다.

    얼음   φ(P) = max(φ₀ · exp(b_ice · P),  φ_floor)
    암석   φ(P) = min(φ₀ · P^(b_rock),      φ₀)

P 는 국소 정암압을 **MPa** 로 넣는다. 지수 형태와 거듭제곱 형태가 갈리는 것은 우리가
고른 게 아니라 Yasui & Arakawa 2009 가 두 재료를 그렇게 적합했기 때문이다 — 얼음은
낮은 공극에서 지수, 실리카는 전 구간에서 거듭제곱이 더 잘 맞았다 (그들의 §3.3).

φ_floor 는 **강도가 버티는 공극** 이다. Durham+ 2005 가 granulated 물얼음을 150 MPa
까지 눌러도 공극 ~0.10 이 남는 것을 재고, 77 K 에서는 100 MPa 위에서도 10–20 % 가
버틴다고 보고한다. Bierson+ 2019 은 그 값을 0.20 으로 잡았다.

## 유효 한계 — 이게 없으면 넘어가도 아무도 모른다

* **실험압.** Yasui & Arakawa 2009 는 −10 °C 에서 30 MPa, −55 ~ −67 °C 에서 80 MPa
  까지 눌렀다. Durham+ 2005 가 150 MPa 다. 그 위는 **외삽** 이고, `p_cap` 인자가
  그 구간에서 아무것도 주장하지 않는 보수적 읽기를 준다. 얼마나 심각한가 — 지구
  중심(358 GPa)에 이 식을
  들이대면 암석 공극 15 % 가 나온다. 명백한 헛소리이고, 이 법칙이 차갑고 소결되지
  않은 알갱이 물질에만 쓰인다는 뜻이다.
* **차갑고 소결되지 않았을 것.** Bierson+ 2019 §2.2 가 자기 모형이 다루지 않는 것을
  나열한다 — "melt production, differentiation, convection, impacts, and tidal
  heating". 그 다섯은 전부 공극을 **더** 없애는 방향이라, 이 식은 밀도의 **하한**
  (= 남을 수 있는 최대 공극) 이다. 그들 자신이 "our model runs represent a lower
  bound on the bulk density (the most porosity that can be retained)" 라고 적는다.
* **φ₀ 는 이 레시피가 도출하지 못한다.** 강착이 정하고 가열이 지운다. 둘 다 여기
  없으므로 φ₀ 는 **선언** 으로 들어온다 (`initial_porosity`), 기본값 0 이다.
  0 이 "공극이 없다" 는 주장은 아니다 — "이 레시피는 판정할 수 없다" 는 뜻이다.
* **검증된 크기.** Bierson+ 2019 이 맞춰 본 KBO 는 지름 123–2326 km 이고, Carry
  2012 의 소행성 표본은 질량 10¹⁷–10²⁰ kg 이다.
"""
from __future__ import annotations

import math

# ── 관계식의 상수 ───────────────────────────────────────────────────────
#
# 넷 다 Bierson+ 2019 Table 1 (Icarus 326, 10; PMC7058130) 에서 왔고, 그 표가 각 값의
# 원 출처를 적어 두었다. b_ice·b_rock 은 Yasui & Arakawa 2009, φ_floor 는 Durham+ 2005.
PHI0_NOMINAL = 0.60        # 초기 공극. Bierson+ 2019 Table 1 의 nominal
PHI_FLOOR_ICE = 0.20       # 강도가 버티는 공극. 같은 표, Durham+ 2005 근거
B_ICE = -0.1               # MPa⁻¹. 같은 표 "Empirical compaction parameter (ice)"
B_ROCK = -0.11             # 무차원. 같은 표 "Empirical compaction parameter (silicate)"
#
# b_rock 은 Yasui & Arakawa 2009 Table 1 의 마지막 행에서 직접 확인된다 — 순수 실리카
# (f = 1, −10 °C) 를 거듭제곱으로 적합한 결과가 a₃ = 0.53, b₃ = 0.11 이고, 초기 공극
# 0.64 가 30 MPa 에서 0.38 로 줄었다. 두 논문이 독립적으로 같은 지수를 준다.
YASUI_SILICA_A3 = 0.53     # Yasui & Arakawa 2009 Table 1, run 090210-5
YASUI_SILICA_B3 = 0.11     # 같은 행. Bierson 의 b_rock 과 부호만 다른 같은 수
YASUI_SILICA_PHI_I = 0.64  # 같은 행, 초기 공극
YASUI_SILICA_PHI_F = 0.38  # 같은 행, 30 MPa 에서의 최종 공극

# ── 문턱과 한계 ─────────────────────────────────────────────────────────
P_GRAIN_FRACTURE = 10.0e6  # Pa. 규산염 입자가 깨지기 시작하는 압력.
#                            Britt+ 2002 → Carry 2012 §5.2 ("∼10⁷ Pa")
P_LAB_MAX = 150.0e6        # Pa. 압밀 실험이 도달한 최대 압력 (Durham+ 2005).
#                            Yasui & Arakawa 2009 는 30 MPa (−10 °C) / 80 MPa (저온)
MASS_COMPACT_KG = 1.0e20   # kg. **관측된** 전이질량. Carry 2012 §5.2 가 이 위의
#                            천체는 macroporosity ≈ 0, 아래는 0–70 % 라고 보고한다.
#                            계산에 쓰지 않는다 — 압력 문턱에서 저절로 나와야 하는 값
DIAMETER_VALIDATED_KM = (123.0, 2326.0)   # Bierson+ 2019 Table A.2 의 KBO 지름 범위

# 재료 이름 → 어느 법칙을 쓰는가. eos.py 의 MATERIALS 키와 맞춘다.
#
# 철에는 법칙을 붙이지 않았다. 압밀 곡선을 못 찾은 것이 첫째 이유이고, 둘째 이유가
# 더 크다 — 핵은 금속이 녹아 가라앉아서 생긴다. 그 과정을 거친 물질에 "소결되지 않은
# 알갱이" 법칙을 쓰는 것은 앞뒤가 안 맞는다. 문헌이 침묵하는 게 아니라 이 자리에
# 그 질문이 없다.
LAW_FOR: dict[str, str | None] = {
    "h2o": "ice",
    "silicate": "rock",
    "fe_prem": None,
    "fe_eps": None,
}


def porosity(kind: str, p_pa: float, phi0: float = PHI0_NOMINAL,
             p_cap: float | None = None) -> float:
    """압력 `p_pa` 에서 남는 공극률. `kind` 는 'ice' 또는 'rock'.

    `p_cap` 은 **보수적 읽기** 다. 그 압력 위에서는 공극을 0 으로 둔다 — 측정된 적이
    없는 구간에서 아무것도 주장하지 않는다는 뜻이고, `P_LAB_MAX` 를 넣는 것이 그
    용법이다. 기본값 None 은 발표된 대로 (Bierson+ 2019 이 자기 KBO 내부에 이 식을
    구간 제한 없이 적용한다) 전 구간에 적용한다.

    둘 다 필요하다. 발표된 대로가 출처에 충실한 쪽이고, 자른 쪽이 결론이 외삽에
    기대고 있는지 재는 쪽이다. 거듭제곱 꼬리가 아주 천천히 죽어서 — 지구 중심
    358 GPa 에 들이대면 암석 공극 15 % 가 나온다 — 그 구별이 실제로 필요하다."""
    if phi0 <= 0.0:
        return 0.0
    if p_cap is not None and p_pa > p_cap:
        return 0.0
    p_mpa = max(p_pa, 0.0) / 1.0e6
    if kind == "ice":
        return max(phi0 * math.exp(B_ICE * p_mpa), min(PHI_FLOOR_ICE, phi0))
    if kind == "rock":
        if p_mpa <= 1.0:
            return phi0                      # min(·, φ₀) 이 여기서 걸린다
        return min(phi0 * p_mpa ** B_ROCK, phi0)
    raise ValueError(f"모르는 공극 법칙 '{kind}'")


def bulk_factor(material_name: str, p_pa: float, phi0: float,
                p_cap: float | None = None) -> float:
    """고체 밀도에 곱해 벌크 밀도를 만드는 인자 (1 − φ). 법칙이 없으면 1."""
    if phi0 <= 0.0:
        return 1.0
    kind = LAW_FOR.get(material_name)
    if kind is None:
        return 1.0
    return 1.0 - porosity(kind, p_pa, phi0, p_cap)


def voids_expected(mass_kg: float, p_center_pa: float,
                   tidal_heating: bool = False) -> tuple[bool, str]:
    """이 레짐에서 공극이 남아 있으리라 기대할 수 있는가, 그리고 왜.

    압밀 곡선은 "이 압력에서 φ 가 얼마인가" 를 답하지 "이 천체가 애초에 공극을
    가질 수 있는가" 를 답하지 않는다. 후자는 세 지표가 말하고, 셋 다 이 파일의
    상수에서 나온다 — 그래서 판정도 여기 있다.

    지표 셋은 전부 **공극이 없는 쪽** 으로만 발화한다. 하나라도 걸리면 이 천체의
    공극 해는 예측이 아니라 봉투 상한으로 읽어야 한다.

    1. 관측된 전이질량 (Carry 2012 §5.2). 10²⁰ kg 위의 천체는 관측상 전부
       macroporosity ≈ 0 이다. 압밀 곡선이 검증된 곳은 그 아래다.
    2. 입자 파쇄 문턱 (Britt+ 2002 → Carry 2012). 중심압이 10 MPa 를 넘으면
       규산염 알갱이가 깨지기 시작한다. 1 번의 기작 쪽 진술이지만, 질량이 아니라
       적분이 실제로 낸 압력을 보므로 독립적으로 발화할 수 있다.
    3. 조석가열. Bierson+ 2019 §2.2 가 자기 모형의 제외 목록에 넣은 다섯 중
       하나이고, 다섯 다 공극을 **더** 없애는 방향이다.

    조석가열은 계산하지 않고 **선언으로 받는다.** 그건 다른 노드의 일이고, 여기서
    질량이나 궤도로 추정하면 `tidal_heating` 의 두 번째 사본이 이 레시피 안에
    생긴다.
    """
    hits = []
    if mass_kg > MASS_COMPACT_KG:
        hits.append(f"질량이 관측된 전이질량의 {mass_kg / MASS_COMPACT_KG:.0f} 배"
                    f" (Carry 2012 §5.2)")
    if p_center_pa > P_GRAIN_FRACTURE:
        hits.append(f"중심압이 입자 파쇄 문턱의 "
                    f"{p_center_pa / P_GRAIN_FRACTURE:.0f} 배")
    if tidal_heating:
        hits.append("조석가열이 선언돼 있다 (Bierson+ 2019 §2.2 의 제외 목록)")
    if not hits:
        return True, (f"세 지표 어느 것도 걸리지 않는다 — 질량 "
                      f"{mass_kg / MASS_COMPACT_KG:.2f} × 10²⁰ kg, 중심압 "
                      f"{p_center_pa / 1e6:.1f} MPa, 조석가열 선언 없음. "
                      "압밀 곡선이 검증된 레짐 안이다.")
    return False, "공극이 남을 레짐이 아니다 — " + "; ".join(hits) + "."


REFS = (
    "2019Icar..326...10B",      # Bierson+ 2019 — 식 (1)(2) 와 계수 표, KBO 검증
    "2009JGRE..114.9004Y",      # Yasui & Arakawa 2009 — 압밀 실험, 순수 실리카 지수
    "2005GeoRL..3218202D",      # Durham+ 2005 — 얼음 냉압밀, 강도가 버티는 공극
    "2012P&SS...73...98C",      # Carry 2012 — 10 MPa 문턱과 관측된 전이질량
    "2002aste.book..485B",      # Britt+ 2002 — 입자 파쇄 문턱의 원 출처
)


# ── 원시 지각의 two-layer 공극 (Malamud & Prialnik 2015, C11) ──────────────
#
# Malamud & Prialnik 2015 (2015Icar..246...21M) §3.3 식 (4)–(6), 전문에서 읽음 (F3,
# malamud-readthrough-context-notes.md). 얼음과 암석이 각자의 압밀 곡선을 따르고 부피를 더하는
# two-layer 모형(Yasui & Arakawa 2009)이고, 위 Bierson 법칙과 **같은 실험**(Durham+ 2005,
# Yasui & Arakawa 2009, Leliwa-Kopystyński+ 1994)의 다른 매개화다 — 차이는 얼음의 상동온도
# T/T_m 의존(식 (6))과 암석의 지수 형이다. 지각(C11)에만 쓴다. 논문 단위 cgs: P 는 dyn/cm².
#   ψ_w(T, P) = ψ_w0 exp(−β_w(T/T_m) √P),  β_w = β_w1 + β_w2 / (1 + exp(β_w3 (1 − T/T_m)))
#   ψ_d(P)    = ψ_d0 exp(−β_d P) Γ,        Γ = 1 (지각은 녹은 적이 없다: T_max < T_m)
# 식 (7) 의 Γ 는 인쇄본 지수가 15(T_max/675) − 1 로 본문 서술("675 K 중심")과 어긋나고
# 15(T_max/675 − 1) 이 본문과 맞는다 — 여기서는 Γ = 1 이라 그 형이 값에 안 들어오지만, 옮겨 적는
# 다음 사람을 위해 적어 둔다. 적합 범위: 얼음 150 MPa(Durham)·암석 764 MPa(Leliwa-Kopystyński),
# 얼음 I. 그 위는 외삽이고 공극이 이미 몇 % 라 그 몫이 상한이다.
MALAMUD_PSI_W0 = 0.45
MALAMUD_PSI_D0 = 0.4
MALAMUD_BETA_W1 = 4.7434e-5     # cm dyn^-1/2
MALAMUD_BETA_W2 = 31.7434e-5    # cm dyn^-1/2
MALAMUD_BETA_W3 = 11.0
MALAMUD_BETA_D = 1.28e-10       # cm² dyn⁻¹
MALAMUD_P_FIT_MAX = 764.0e6     # Pa. 암석 압밀 데이터의 끝 (Leliwa-Kopystyński+ 1994)


def malamud_ice_porosity(p_pa: float, t_k: float, t_melt_k: float | None) -> float:
    """얼음 알갱이의 공극 ψ_w(T, P), 식 (4)·(6). 온도가 흐르지 않으면(t ≤ 0) 또는 녹는점을 모르면
    가장 차가운 끝(β_w1) 으로 잰다 — 공극이 가장 많이 남는 쪽, 곧 상한이다."""
    p_cgs = max(p_pa, 0.0) * 10.0
    if t_k > 0.0 and t_melt_k:
        h = min(t_k / t_melt_k, 1.0)
        beta = MALAMUD_BETA_W1 + MALAMUD_BETA_W2 / (1.0 + math.exp(MALAMUD_BETA_W3 * (1.0 - h)))
    else:
        beta = MALAMUD_BETA_W1
    return MALAMUD_PSI_W0 * math.exp(-beta * math.sqrt(p_cgs))


def malamud_rock_porosity(p_pa: float) -> float:
    """암석 알갱이의 공극 ψ_d(P), 식 (5) 에 Γ = 1."""
    return MALAMUD_PSI_D0 * math.exp(-MALAMUD_BETA_D * max(p_pa, 0.0) * 10.0)

