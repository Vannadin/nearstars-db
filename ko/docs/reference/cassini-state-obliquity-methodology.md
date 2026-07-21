<!-- 조석으로 감쇠된 천체의 평형 자전축 기울기(Cassini state obliquity)를 근거화 계산해 "고정=obliquity 0" 가정을 실제 평형값으로 대체하는 방법 -->
# Cassini-state obliquity: equilibrium spin-axis tilt of a damped body

자전이 조석으로 감쇠되어 **Cassini state**에 들어앉은 천체의 **평형 obliquity ε**를 다루는 방법론
레퍼런스입니다. "조석고정 ⟹ obliquity = 0" 식의 게으른 가정을 실제 Cassini-state 값으로 대체합니다.
잘 측정된 동기 천체라면 어느 것이든 그 값은 **작지만 0은 아니며**, 세속(secular) 자전–궤도 공명이 끼어들면
*크게* 벌어질 수 있습니다.

짝 문서는 [`body-figure-methodology.md`](body-figure-methodology.md)(형상 계수 J₂, C̄₂₂를 공급)와
[`tidal-locking-timescale-methodology.md`](tidal-locking-timescale-methodology.md)(천체를 Cassini
후보로 만드는 고정 상태를 공급)입니다.

> 규율. Cassini 프레임워크는 교과서 천체역학(Colombo–Peale–Ward)이므로 그렇게 밝히고 표준 레퍼런스로
> 인용합니다. ADS로 근거화하는 것은 **캘리브레이션 앵커**(측정된 Cassini obliquity, Mercury, Titan,
> Galilean 위성들)와 동기 경우의 세차 상수 계수입니다. 계수 두 개는 과잉 주장 대신 명시적 불확실성
> 플래그를 달고 갑니다(§3, §6).

## 1. What a Cassini state is

주성(항성, 위성의 경우 모행성)은 천체의 자전 + 조석 팽대부에 토크를 걸어, **자전축 ŝ가 궤도 법선 n̂
둘레를 세차**하게 만듭니다. 그 세차율은 세차 상수 α가 정합니다. 한편 n̂ 자신은 고정된 경사 I를 유지한 채
**Laplace 극 k̂ 둘레를 궤도 승교점율 g로 세차**합니다. **Cassini state**는 궤도와 함께 세차하는
공전 좌표계에서의 평형입니다. ŝ, n̂, k̂가 **한 평면에 놓인 채 공통 속도 g로 함께 세차**합니다(Colombo 1966
`1966AJ.....71..891C`; Peale 1969 `1969AJ.....74..483P`). 조석 소산은 ŝ를 그 평면에서 살짝 *바깥으로*
밀어냅니다(Su & Lai 2022 `2022MNRAS.509.3301S`).

상태는 최대 **네 개**입니다(Peale 1969).

- **State 1**: 낮은 obliquity, ŝ가 n̂ 근처. 조용히 조석 감쇠된 천체가 도달하는 분기입니다.
  **NearStars에서 고정 천체의 기본값입니다.**
- **State 2**: obliquity가 Laplace 극 반대쪽; **클 수 있습니다**(수십 도); 나머지 하나의 안정
  종착 상태입니다.
- **States 3 & 4**: 불안정합니다.

소산 아래에서는 **state 1과 2만 끌개(attractor)**입니다(Ward 1975 `1975AJ.....80...64W`). ε = 0 근처에서
감쇠된 천체는 **state 1**에 안착하고, 세속 자전–궤도 공명에 걸리거나 그것을 통과하며 이주한 천체는 높은
obliquity의 **state 2**에 포획될 수 있습니다(Millholland & Laughlin 2019 `2019NatAs...3..424M`).

## 2. Equilibrium-obliquity relation

ε = obliquity(∠ ŝ,n̂), I = Laplace 평면에 대한 궤도 경사, g = Ω̇ < 0 승교점 세차율, α > 0 자전 세차
상수라 할 때, Cassini state는 다음을 만족합니다(Peale 1969 `1969AJ.....74..483P`; Ward & Hamilton 2004
`2004AJ....128.2501W`).

    α · cos ε · sin ε  +  g · sin(ε − I)  =  0                    (1)

**근의 개수**는 임계비에 대한 |g|/α로 정해집니다(Henrard 1987 `1987CeMec..40..345H`; Ward & Hamilton 2004).

    (|g|/α)_crit = ( sin^(2/3) I + cos^(2/3) I )^(3/2)            (2)

|g|/α < crit → 근 4개(state 1–4); |g|/α > crit → 근 2개(state 2 & 3), state 1은 state 4와 합쳐져
사라집니다. 작은 I 극한에서 (2)는 |g|/α ≈ 1로 환원됩니다. *((2)의 정확한 지수 묶음은 캐시된 소스에서
이미지였습니다. 공명 플래그에는 작은 I 형태 |g|/α ≈ 1이면 충분하니, 인용하려거든 Ward & Hamilton 2004에서
전체 표현을 먼저 확인하십시오.)*

**작은 각 State-1 해**(ε, I 작음; Ward 1975; Fabrycky+ 2007 `2007ApJ...665..754F`).

    ε₁  ≈  |g| sin I / ( α + |g| cos I )                          (3)
    α ≫ |g|  ⟹  ε₁ ≈ (|g|/α) sin I  →  0                          (4)

**(4)가 고정 천체의 핵심 결과입니다.** 팽대부가 이끄는 자전 세차 α가 궤도 승교점율 |g|를 크게 웃돌 때,
평형 obliquity는 ≈ (|g|/α)·sin I라는 *작지만 0은 아닌* 값으로 억눌립니다. **정확히 0은 아닙니다**. 이 값은
공명 |g|/α ~ 1(state 2) 근처에서만 커집니다.

## 3. The precession constant α

**자유 / 빠른 회전체**(Néron de Surgy & Laskar 1997 `1997A&A...318..975N`; Ward 1975), n² = G M⋆ / a³
및 항등식 (C−A) = J₂·M R²와 함께.

    α = (3/2) · (n²/ω) · [ J₂ / (C/MR²) ] · (1−e²)^(−3/2)         (5)

Sanity check: 지구의 태양 토크 α를 (5)로 구하면(J₂ = 1.08e-3, C/MR² = 0.331, ω = 2π/day, n = 2π/yr)
≈ 17″/yr로, 알려진 태양-달 세차의 태양 기여분 ~16″/yr와 맞아떨어집니다.

**동기 고정된 천체**(ω = n): **NearStars가 필요로 하는 경우**입니다. 천체는 triaxial(A < B < C)이며,
정유체 형상 계수 J₂와 C̄₂₂, 정규화 관성모멘트 C̃ ≡ C/MR²을 써서 위성 문헌(Bills 2005 `2005Icar..175..233B`;
Baland+ 2011 `2011A&A...530A.141B`)은 다음을 씁니다.

    α_syn = (3/2) · n · ( J₂ + C̄₂₂ ) / (C/MR²)                    (6)

> **계수 주의.** 강체 극 조합은 (C−A)/C = (J₂ + 2C̄₂₂)/C̃이지만, 벤치마크된 위성 obliquity 논문들은
> (J₂ + C̄₂₂)/C̃ (6)을 씁니다. 정유체 동기 천체는 C̄₂₂ = 0.3·J₂이므로 둘은 1.3 J₂ 대 1.6 J₂로 갈려
> α에서 ~20 %, 따라서 ε에서 ~20 %의 폭이 생깁니다. **(6)(Baland/Bills)을 채택합니다**. 측정된 위성으로
> 캘리브레이션된 값이기 때문입니다. ±20 %는 모델링 계통 오차로 싣고, 정확한 계수는 사용 시점에
> `2011A&A...530A.141B` / `2005Icar..175..233B`에서 확인하십시오.

ω = n이면 n²/ω = n이 되어 고정 천체의 α는 빠른 회전체보다 훨씬 작고, (J₂ + C̄₂₂)에 비례해 스케일합니다.
고정 천체에서 이 값은 궤도가 조여들수록 *커집니다*(figure 문서 §3: J₂ ≈ q_s, C̄₂₂ ≈ 0.3 J₂). 그래서
**가장 조인 고정일수록 가장 둥글게 도는 → 가장 작은 ε₁**이 됩니다, 공명이 끼어들지 않는 한.

## 4. Getting the orbital nodal rate g

**(a) 다중 행성계의 행성: Laplace–Lagrange 세속 이론**(Murray & Dermott 1999 `1999ssd..book.....M`,
7장). 승교점 진동수 {g_i}는 경사 상호작용 행렬 B의 고유값입니다. 최저차는 이렇습니다.

    B_jk = +(1/4) n_j · [m_k/(M⋆+m_j)] · α_jk · ᾱ_jk · b^(1)_{3/2}(α_jk)
    B_jj = −Σ_{k≠j} B_jk

α_jk = 장반경 비(작은 쪽/큰 쪽), b^(1)_{3/2}는 Laplace 계수입니다. **입력**: 이웃 질량 + 장반경 + 주성
질량. 지배 모드의 {g, I}를 씁니다. **공명 사슬**(예: TRAPPIST-1)에서는 Laplace–Lagrange가 무너지므로 →
직접 **N-body 승교점 진동수 분석**을 씁니다(Millholland+ 2024 `2024ApJ...961..203M`, [arXiv:2311.17908](https://arxiv.org/abs/2311.17908)).

**(b) 근접 위성: 모행성의 편평도 J₂가 이끔**(Murray & Dermott 1999).

    |g| = |Ω̇| ≈ (3/2) · J₂,planet · (R_planet/a)² · n · cos i     (7)

여기에 항성 및 다른 위성/고리 항이 더해집니다. 위성의 Laplace 평면 경사 I는 모행성 적도(가까울 때 지배하는
J₂ 항)와 항성 둘레 궤도 사이의 균형점입니다. **입력**: 모행성 J₂, R_planet, 위성 a와 n, 다른 위성들.

## 5. Calibration anchors (verify the recipe here first)

| body | state | measured obliquity | source | hydrostatic recipe reproduces? |
|---|---|---|---|---|
| **Mercury** (3:2) | 1 | **2.11 ± 0.1 arcmin** (0.035°) | `2007Sci...316..710M` Margot+ 2007 | **예**: Cassini 관계 + 측정된 ε가 *바로* C/MR²을 추론하는 방법이며, J₂, C₂₂와 자기일관적입니다(`2009CeMDA.105..329M`). |
| **Moon** | **2** | 황도에 6.7° (Laplace 평면 기준 ≈1.54°) | `1975Sci...189..377W` Ward 1975 | 프레임워크는 **예**, 형상은 **아니오**: Cassini-state 전이에서 나온 진짜 state-2 값이지만, 달의 **화석 팽대부**(J₂/C₂₂≈9≠10/3)가 정유체 α를 깨뜨립니다. 화석 플래그. |
| **Titan** | 1 | ≈0.3° | `2010AJ....139..311S` Stiles+ 2010 | **아니오**: 강체 Titan은 ~2–3× 과소예측합니다. 이 값은 **지하 바다**(껍질의 Cassini-state 공명)를 요구합니다, Baland+ 2011 `2011A&A...530A.141B`. 비강체 플래그. |
| **Io–Callisto** | 1 | ≈10⁻³–10⁻² deg (작지만 0은 아님) | `2005Icar..175..233B` Bills 2005 | **예**(강체); 액체 층이 이들을 이동시킵니다(`2012Icar..220..435B`). **고정 ≠ 0**을 확증합니다. |
| **Enceladus** | 1 | ≈0.0015° (강체) | `2016Icar..268...12B` Baland+ 2016 | **예**; 바다가 있어도 ≪ 0.05°에 머뭅니다(`2011Icar..214..779C`). |

**핵심**: 잘 측정된 동기 천체는 예외 없이 *0이 아닌* Cassini state 1에 앉아 있습니다(Mercury 0.035°,
Galilean 위성 10⁻³–10⁻² deg, 바다 포함 Titan 0.3°), **"정확히 0"은 결코 옳지 않지만**, 공명(Moon =
state 2)이나 분리된 바다(Titan)가 끼어들지 않는 한 크기는 1도 미만입니다.

## 6. Regime guidance / expected magnitudes

- **M 왜성 둘레 a ≈ 0.03–0.05 AU의 근접 암석 행성**(Proxima b형, TRAPPIST-1형): 조인 고정 → 큰 J₂+C₂₂
  → 큰 α_syn → (4)에 의해 |g|/α ≈ 1 공명에서 멀면 **ε₁은 1도 미만**입니다. Millholland+ 2024는 TRAPPIST-1
  행성 대부분이 ε ≈ 0일 공산이 크고 **행성 d가 가능한 예외**라고 봅니다. 기본값: 0으로 가정하지 말고
  ε ≈ 0.01–1°를 계산합니다.
- **공명으로 증폭된 state 2는 실재합니다.** Guerrero+ 2024 `2024ApJ...975..256G`: 알려진 M 왜성 다중
  행성계 280개 중 **~75 %의 행성이 안정한 고-obliquity state 2에 포획될 *수* 있으며**, 유효 고정을 깨고
  실제 낮밤 주기를 만듭니다. *게임플레이로 흥미로운*(interesting-first) 분기입니다. 천체마다 |g|/α가
  임계 (2) 근처인지 표시하고, 그렇다면 수십 도의 문서화된 ε를 정당하게 채택할 수 있습니다.
- **미니-넵튠(~950 km 천체)에서 a ~ 4 R_p의 근접 얼음 위성**: 모행성 J₂ (7)에서 오는 g가 빠르고 α_syn은
  작습니다. Galilean 위성처럼 **1도 미만 state-1 obliquity**(10⁻³–10⁻² deg)를 예상하며, **단** 지하 바다가
  이를 Titan 같은 ~0.1–0.3°로 증폭할 수 있습니다(documented-divergence 선택지). 공명은 |g|/α로
  확인합니다.

## 7. Inputs needed per body (checklist)

figure 문서 + 큐레이션된 DB에서.
- **J₂**, 고정 천체는 **C̄₂₂** · **C/MR²**(천체 종류) · **자전 ω**(동기이면 = n)와 **평균 운동 n** ·
  **e, a, 주성 질량 M⋆**.

g를 위해.
- 행성 경우: **이웃 행성들의 질량 + 장반경** → Laplace–Lagrange 지배 승교점 모드 {g, I}(공명 사슬은 N-body
  진동수 분석);
- 위성 경우: **모행성 J₂, R_planet, 위성 a, 다른 위성/고리** → (7) + 위성의 Laplace 평면 I.

그다음: α는 자유면 (5), 고정이면 (6) → (1)을 풀어 state-1 근을 구하고((3)/(4)는 작은 각 검증) → ε를
보고합니다. |g|/α를 (2)에 대해 시험해 큰 state-2 해가 존재하는지 표시합니다.

## 8. Caveats (honest)

1. **동기 α 계수**: Baland/Bills의 (6) (J₂+C̄₂₂)/C̃ 대 강체 (J₂+2C̄₂₂)/C̃: ~20 % 폭; Baland/Bills를
   채택하고 계통을 싣습니다.
2. **임계비 (2)의 정확한 형태**: 작은 I 극한 |g|/α ≈ 1은 견고합니다; 인용 전에 Ward & Hamilton 2004에서
   전체 표현을 확인합니다.
3. **화석 팽대부**(Moon, Mercury 형상): 형상이 얼어붙은 경우 정유체 α는 틀립니다; figure 문서의 화석-팽대부
   플래그를 재사용합니다.
4. **비강체 증폭**(Titan): 지하 바다가 ε를 2–3× 곱할 수 있습니다; 기본값이 아니라 문서화된 선택지입니다.
5. **미지의 g**: 동반 천체 집합이 잘 제약되지 않으면 g(따라서 ε)가 불확실합니다; 가정한 이웃을 명시합니다.
   공명 사슬은 N-body 진동수 분석을 *요구*합니다.
6. **State 1 대 2는 역사 의존적**: 소산은 기본적으로 state 1을 선택하지만, M 왜성 행성의 ~75 %에서
   공명/이주에 의한 state 2 포획이 그럴듯합니다(Guerrero 2024), Phase 4에서 제시할 만한 interesting-first
   분기입니다.

## Related

- [`body-figure-methodology.md`](body-figure-methodology.md): §3이 세차 상수 (6)에 들어가는 J₂와 조석
  C̄₂₂를 공급합니다.
- [`tidal-locking-timescale-methodology.md`](tidal-locking-timescale-methodology.md):
  천체가 애초에 고정(Cassini 후보)되었는지 여부.
- [`principia-geopotential-data.md`](principia-geopotential-data.md): J₂/C₂₂의 cfg 형식; 자전축
  방향은 Principia/Kopernicus 극에 들어갑니다.
- [`methodology-index.md`](methodology-index.md): 전체 방법론 인덱스.
