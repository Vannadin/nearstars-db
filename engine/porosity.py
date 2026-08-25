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


REFS = (
    "2019Icar..326...10B",      # Bierson+ 2019 — 식 (1)(2) 와 계수 표, KBO 검증
    "2009JGRE..114.9004Y",      # Yasui & Arakawa 2009 — 압밀 실험, 순수 실리카 지수
    "2005GeoRL..3218202D",      # Durham+ 2005 — 얼음 냉압밀, 강도가 버티는 공극
    "2012P&SS...73...98C",      # Carry 2012 — 10 MPa 문턱과 관측된 전이질량
    "2002aste.book..485B",      # Britt+ 2002 — 입자 파쇄 문턱의 원 출처
)
