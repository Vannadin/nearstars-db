<!-- 천체의 구-대비 변형(자전 편평 J2 + 조석고정 triaxial C22)을 근거화 계산해 Principia 중력모델에 채우는 방법 -->
# Body figure grounding — rotational oblateness (J₂) and tidal triaxiality (C₂₂)

모든 NearStars 천체의 2차(degree-2) **형상**을 다루는 방법론 레퍼런스입니다. 천체가 완전한 구에서 얼마나
벗어나는지, 그리고 그 변형을 어떤 중력 계수가 포착하는지를 설명합니다. 물리적 원인은 둘, 계수도 둘입니다.

- **자전**은 천체를 편평한 회전타원체로 누릅니다 → zonal **J₂** (= −√5·C̄₂₀).
- **조석고정 천체의 영구 조석 팽대부**는 천체를 *triaxial*(긴 축이 주성을 향함)로 만듭니다
  → sectoral **C̄₂₂**가 추가됩니다.

여기는 **방법** 자체의 canonical 본거지입니다. *데이터 + cfg 형식* 짝 문서는
[`principia-geopotential-data.md`](principia-geopotential-data.md)이며, 태양계 계수의 verbatim 값,
정규화 규칙(J₂ = −√5·C̄₂₀, J₂ = 10⁄3·C̄₂₂), proto↔KSP-cfg 매핑을 담고 있습니다. 그 문서는 이미
**Polyphemus** 자이언트의 J₂를 완전히 풀어 두었고, 이 문서는 그 레시피를 천체 종류 전반으로 일반화하고
조석 C₂₂를 근거화합니다. J₂/C₂₂는 아트디렉션 선택이 아니라 **도출된 emit**입니다. 자전 + 질량 + 반경 +
중심 응집도로부터 결정론적으로 따라 나오므로, 단위 변환처럼 천체마다 계산됩니다. 인게임에서 왜 중요하냐면,
J₂는 **인공위성**에 작용하는 가장 지배적인 비-Keplerian 섭동(승교점 이동 + 근점 세차 ∝ (R/a)²·cos i)이고,
Principia는 비행체를 완전한 지오포텐셜 안에서 적분하기 때문입니다 — 즉 플레이어가 천체 주위를 도는 모든
궤도의 형태를 좌우합니다.

> 규율. 형상은 **정유체역학 평형** 관계식(Radau–Darwin, Maclaurin, 동기위성 형상)에서 따라 나옵니다 —
> 교과서 결과이므로 "도출값은 논문 근거화" 원칙의 허용된 예외입니다. 그럼에도 인용이 필요한 것은
> **캘리브레이션 앵커**(측정된 태양계 J₂/C₂₂)와 관성모멘트 경계이며, 이들은 NASA ADS로 해소합니다.

## 1. The figure parameter

두 효과 모두 표면에서의 원심(또는 조석) 가속도 대 자체중력 가속도의 무차원 비로 지배됩니다.

    q  =  ω²·R³ / (G·M)            (rotational, ω = 2π/P_rot)

**고정되지 않은** 천체에서 ω는 항성시 기준 자전 각속도입니다. **동기 고정된** 천체에서는 ω = n(궤도 평균
운동)이고, 주성으로부터의 *정적 조석*이 같은 차수의 항을 추가합니다 — 동기 원궤도에서는 leading order로
n²R³/(GM_body) = (M_primary/M_body)(R/a)³가 성립하여 자전 파라미터와 조석 파라미터가 비슷한 크기이기
때문입니다. 고정된 경우는 q_s = n²R³/(GM)로 씁니다.

## 2. Rotational figure — Maclaurin vs Radau–Darwin

q에 대한 1차 근사에서, 편평도 f = (R_eq − R_pol)/R_eq와 J₂는 다음 정유체 관계를 따릅니다.

    J₂  =  (2/3)·f  −  (1/3)·q

남은 자유도는 **중심 응집도**이며, 정규화 관성모멘트 NMoI = C/(M R²)로 표현합니다(0.4 = 균질 구,
작을수록 더 응집).

- **균질(Maclaurin) 극한**, NMoI = 0.4: f = (5/4)q, 따라서 **J₂ = q/2**. 이것이 편평도의
  *균일밀도 상한*입니다.
- **중심 응집 천체**(모든 실제 행성/항성), NMoI < 0.4: **Radau–Darwin** 관계를 사용합니다. 이 관계는
  J₂, q, NMoI를 묶습니다(Helled et al. 2011, `principia-geopotential-data.md`에 재현된 형태입니다).

      NMoI = (2/3)·[1 − (2/5)·√(5q/(q + 3J₂) − 1)]
      inverted →  J₂ = (q/3)·[5/(s²+1) − 1],   s = (5/2)·(1 − (3/2)·NMoI)

  같은 q에서 더 응집된 천체는 편평이 **덜** 일어나므로, J₂/q는 ½ 아래로 떨어집니다.

### Calibration (always verify on the real bodies first)

| 천체 | 종류 | q | NMoI | J₂/q | measured J₂ |
|---|---|---|---|---|---|
| Earth | rocky | 3.45e-3 | 0.331 | 0.31 | 1.083e-3 |
| Mars | rocky | 4.6e-3 | 0.364 | ~0.43* | 1.96e-3 |
| Jupiter | giant | 0.083 | 0.265 | 0.177 | 1.470e-2 |
| Saturn | giant | 0.140 | 0.220 | 0.116 | 1.629e-2 |
| Sun | star | ~2e-5 | ~0.06 | ~0.01 | 2.1e-7 |

\*Mars는 Tharsis에 의한 비-정유체 초과량을 가지므로, 그 *정유체* J₂는 더 낮습니다. 자이언트 캘리브레이션은
Jupiter를 −0 %, Saturn을 −10 %로 재현합니다(1차 절단, q가 커질수록 오차 증가) — 따라서 **빠른 자전체(큰 q)에서는
1차 값이** 참 J₂를 약 10–20 % 과소예측합니다. 항성은 응집의 극단에 위치하여, 느린 자전의 태양조차 J₂ ≈ 2×10⁻⁷를
가집니다(알려진 가장 둥근 천체 중 하나입니다). **위 표의 Sun 행은 *측정값*입니다** — Radau–Darwin 역산은 NMoI ≳ 0.13에서만
유효하고 항성의 중심응집(NMoI ~0.05–0.08)에선 음수 J₂를 뱉으므로, 항성은 이 공식에 넣지 않습니다. 대신 항성에는
**태양앵커 q-스케일링**을 씁니다.

    J₂(항성) = (J₂☉ / q☉) · q  ≈  0.0105 · q

앵커는 헬리오사이즈몰로지 측정값 J₂☉ = (2.18 ± 0.06)×10⁻⁷ (Pijpers 1998)입니다. 태양 유사 응집도의 FGK
왜성에 유효합니다. **완전 대류 M 왜성은 예외적으로 Radau–Darwin으로 되돌아갑니다** — n = 3/2 폴리트로프의
NMoI ≈ 0.205(Chandrasekhar 1939)는 이 관계식의 유효범위 안이라, 그 NMoI에서 J₂/q ≈ 0.084가 나옵니다
(태양 비율의 ≈8배 — 응집이 덜해 단위 q당 더 많이 편평해짐). **백색왜성도 같은 분기를 탑니다** — 비상대론
축퇴성은 n = 3/2 폴리트로프에 가까워 NMoI ≈ 0.205로 Radau–Darwin이 적용됩니다(상대론 보정이 중심을 조금
더 응집시키므로 J₂는 소폭 과대 추정). WD 자전은 대개 미측정입니다 — ZZ Ceti 띠 밖이면 성진동이 불가하므로,
Kepler 점근파 표본 중앙값 P ≈ 35 h(Hermes et al. 2017)를 문서화된 통계 입력으로 씁니다(보드에는
documented-divergence). **조기형 항성은 근점이동상수 경로를 직접 씁니다** — 이 모든 분기의 배후에 있는
일반 관계식은 다음과 같습니다.

    J₂(항성) = (2/3) · k₂ · q        (k₂ = 근점이동상수, Sterne 1939)

FGK 앵커는 이 식의 경험적-태양 인스턴스(헬리오사이즈모 J₂/q 역산 k₂☉ = 0.0158)이고, 폴리트로프 분기는
NMoI 0.205 인스턴스입니다. A형은 Claret 2004 그리드(Claret 2019와 정합)에서 k₂를 취하되, 그리드 자체의
태양 오프셋(이론 k₂☉ ≈ 0.020 vs 경험 0.0158)으로 정량화된 ~±25% 모델 계통을 함께 싣습니다. Fomalhaut A
워크드 근거화는 `phase4/figure/fomalhaut-j2-research.md`에 있습니다.
**오너 정책(2026-07-12): 항성 J₂는 크기와 무관하게 항상 계산해서 emit하며, "무시가능" 기록으로 끝내는 처리는
금지합니다** — Principia가 이 항을 적분하므로 오너가 상시 반영을 원합니다.

## 3. Tidal triaxiality — synchronously locked bodies

(거의) 원궤도에 고정된 천체는 주성을 향하는 **영구** 조석 팽대부를 일으킵니다. 그 2차 형상은
**triaxial**(반축 a > b > c, a는 주성을 향하고 c는 자전축)이 되어, J₂ **와** 실제 sectoral C̄₂₂를 함께
가집니다. 정유체 평형에서 둘은 고정된 비율로 묶입니다.

    J₂  =  (10/3)·C̄₂₂        (equivalently  C₂₂ = 0.3·J₂)

그리고 천체는 축 차이가 (a−c):(b−c) = 4:1인 triaxial 타원체가 됩니다. 이 비율은 **측정된 동기위성들**(Io,
Europa, Ganymede, Titan 모두 J₂/C₂₂ ≈ 10/3)에서 **확인**되며, 그래서 고정된 경우는 측정 불가능한 것이
아니라 *예측 가능*합니다. 크기 또한 같은 천체들로 캘리브레이션됩니다.

    J₂  ≈  (0.9–1.1)·q_s     for differentiated rocky/icy synchronous bodies
    C̄₂₂ ≈ 0.30·J₂

(Io J₂/q_s ≈ 1.08, Europa ≈ 0.88 — 이 폭은 내부 구조 차이입니다.) 따라서 느린 *자유* 회전체와 달리,
가까이 고정된 천체는 자전과 조석이 더해지기 때문에 q_s 자체에 필적하는 J₂를 가집니다.

> **화석 팽대부 주의.** Moon(J₂/C₂₂ ≈ 9, 10/3에서 크게 벗어남)과 Mercury는 정유체가 **아닙니다** —
> 그 팽대부는 더 빠르고/가까웠던 과거 상태가 얼어붙은 기록입니다. 우리 동기 천체들은 별도의 형상을
> 화석화할 역사가 없으므로, 천체의 lore가 그것을 암시하지 않는 한 **정유체**로 가정합니다. 문제가 될 수
> 있는 곳에는 그 선택지를 표시해 둡니다.

**근–원 비대칭 (octupole / 물방울).** 두 조석 팽대가 똑같은 것은 degree 2(C̄₂₂, 짝함수 P₂ 변형)
까지입니다. 다음 조석 항은 **홀함수 P₃ octupole**입니다 — 모행성의 당김이 가까운 쪽에서 더 세므로
**모행성 쪽 팽대가 반대쪽보다 살짝 큽니다**(모행성 방향으로 더 뾰족한 물방울/배 형상). 비대칭의 크기는
대략 **R/a**(천체 반경 / 궤도 거리)에 사분극 팽대를 곱한 정도로, 여기선 sub-percent입니다(Dante R/a ≈ 0.8%,
Hades ≈ 0.5%). 그래서 **기록만 하고 기본 emit은 하지 않습니다**. 두 가지 단서. (1) 중력 쪽으론 **degree-3**
항이라 동역학적으로 무시급입니다. (2) 대칭인 `CustomEllipsoid` 메시로는 **표현되지 않습니다** — 시각적
물방울은 terrain pass에서 작은 degree-3 **heightmap** bump로 넣어야 합니다. 실제 사례로 달의 형상 중심이
지구 쪽으로 치우쳐 있습니다.

## 4. Regimes by body type

| body class | spin | figure | coefficients |
|---|---|---|---|
| **가스 자이언트 / 빠른 자유 회전체** | fast, free | large oblate | scalar **J₂** (+ J₄ ≈ −4 % J₂, J₆), no tesseral |
| **자유 암석체** (드묾; 빠르고 비고정) | P_rot | oblate, J₂ ∝ q | scalar **J₂** (tesseral unmeasurable → omit) |
| **동기 암석/얼음체** (로스터 대부분) | ω = n | **triaxial** | degree-2 full: **C̄₂₀ + C̄₂₂** (J₂ = 10⁄3·C₂₂) |
| **항성** | 대개 느림 | nearly round | scalar **J₂** — 항상 emit (태양앵커 0.0105·q, 오너 정책 2026-07-12) |

`reference_radius`(계수가 스케일링되는 기준 반경 — 자전 형상의 경우 **적도** 반경)는 J₂/지오포텐셜을
emit할 때마다 필수입니다. cfg 형식(scalar `j2`, zonal `geopotential_row`, full cos/sin)은
[`principia-geopotential-data.md`](principia-geopotential-data.md)에 정리되어 있습니다.

## 5. High-degree geoid for rocky bodies — synthetic now, heightmap later

§2–§3은 **2차(degree-2)** 형상(자전 + 조석)을 결정론적으로 고정합니다. 실제 암석체는 그 위에 *울퉁불퉁한*
3차 이상의 장을 함께 가집니다 — 천체 고유의 내부 밀도 이상(anomaly)과 지형이 남기는 중력 지문입니다(지구,
달의 mascon, 화성의 Tharsis). 가상의 천체에는 이런 측정된 지문이 없고, 흉내 낼 만큼 풍부한 고차 장을 가진
태양계 천체는 **네 개**뿐입니다(Earth deg 2159, Moon 900, Mars 120, Venus 180; Galilean 위성·Titan·
Enceladus는 사실상 degree-2뿐). 따라서 복잡한 지오이드는 조회하는 것이 아니라 **합성**해야 합니다. 두 단계로
나뉩니다.

**Stage A — Kaula 스펙트럼 합성 장 (지금).** 실제 행성 중력 스펙트럼은 **Kaula의 법칙**(Kaula 1966)을
따릅니다. 완전 정규화된 조화함수의 계수별 RMS가 거듭제곱 법칙으로 감소합니다.

    s_n  =  rms(C̄ₙₘ, S̄ₙₘ)  ≈  K / n²        (Earth: K ≈ 1×10⁻⁵)

→ degree variance σ²ₙ = (2n+1)·s²ₙ ∝ 1/n³. 천체의 지오이드를 합성하는 절차는 이렇습니다.

1. **§2–§3의 2차 항은 유지** — J̄₂₀ = −J₂/√5(고정 천체는 C̄₂₂도)는 근거화된 자전/조석 값으로 그대로
   두고, degree ≥ 3만 합성합니다.
2. 각 n = 3…N_max, m = 0…n에 대해 C̄ₙₘ, S̄ₙₘ ~ Gaussian(0, s_n), s_n = K/n²로 뽑습니다.
3. **RNG는 천체마다 결정론적으로 시딩**(이름 해시) — 같은 천체는 같은 장을 내므로 재현성 invariant가
   보존됩니다. 큐레이션 레이어에서 `synthetic`으로 표시합니다.
4. **K는 천체 종류에 맞춰 캘리브레이션.** 지구(활발한 판구조) ≈ 1×10⁻⁵; 대기 없고 침식되지 않은
   mascon-rich 천체(달/수성형)는 *더 거칠어* K가 큽니다(GRAIL 팀은 달에 달 고유의 Kaula 제약을 적용).
   작고 분화된/얼음 천체는 더 빨리 감소합니다. K가 유일한 조정값이니 명시합니다.
5. **N_max ≈ 8–10** — 현실적인 저궤도 섭동에 충분합니다(Principia 번들 지구는 degree 10에서 절단). 더 높은
   차수는 표면을 제외하면 동역학적으로 무의미합니다. full cos/sin `geopotential_row`로 emit하고
   `reference_radius` = R_eq.

이렇게 하면 통계적으로 지구 같은 울퉁불퉁함 — 그리고 굳이 할 만한 가치를 주는, mascon 같은 저궤도
동역학(대기 없는 천체 위에서 불안정한/frozen 저궤도)이 — 나오면서도, 보이는 무언가에 묶이지 않은 정직한
**합성 등급(synthesis-grade)**임을 유지합니다.

**Stage B — heightmap 기반 장 (지형 패스 단계).** 천체의 지형(PQS/Parallax heightmap)이 일단 존재하면,
degree-3+ 장을 Airy/Pratt 지각 평형 보정 아래 지형으로부터 *재계산*합니다(중력-지형 admittance — Wieczorek의
Treatise 방법, 표준 관행입니다. EGM2008 자체도 데이터가 부족한 영역을 이 방식으로 채웁니다). 그 결과는
**눈에 보이는 산/분지와 자기일관적**이고 Kaula 임시값을 **대체**합니다. 2차 항(자전/조석)은 두 단계에서
변하지 않습니다. 로드맵은 이렇습니다. **degree 2 영구 · degree 3+ Kaula-지금 → heightmap-나중.**

**Visual shape emit (Kopernicus).** J₂/C₂₂는 *중력* 형상(Principia)이고, *눈에 보이는* 형상은
별개의 메시입니다. **VertexHeightOblateAdvanced** PQS Mod(James Glaze, MIT)는 `oblateMode = CustomEllipsoid`와
a:b:c 비율로 천체를 편평/triaxial 타원체로 렌더링합니다. 2차 형상에서 극축으로 정규화(c = 1)하면 이렇게 나옵니다.
triaxial(동기, 정유체 4:1) 천체 → a/R = 1 + 7J₂/3, b/R = 1 − 2J₂/3, c/R = 1 − 5J₂/3 (이후 ÷c); 자유 편평 회전체 →
a = b, c = R(1 − f). `scripts/refs/body_figure.py`의 `ellipsoid_ratios()`가 이를 emit하므로, 하나의 형상이
중력과 시각 양쪽을 구동해 자동으로 일관됩니다. **부피는 보존돼야 합니다** — 물리 형상은 한 축이 부풀면 나머지가
수축합니다(편차 합 ≈ 0). 반경이 둘 따로인데, Principia의 자이언트가 그대로 보여줍니다(Jupiter `mean_radius` 69911 km vs
`reference_radius` 71492 km; Saturn 58232 vs 60330). (1) **Principia 중력**은 `mean_radius`(체적 — 부피 결정) +
`reference_radius`(적도 — J₂ 스케일용)를 씁니다. 편평은 무차원 J₂에만 있어 **인플레이션이 없습니다**. (2) **VertexHeightOblateAdvanced
시각**은 베이스 구를 a:b:c(전부 ≥ 1)로 키우므로, **Kopernicus PQS `radius`(베이스 구)를 극반경**(= 평균반경 × c_physical)으로
두지 않으면 a·b·c배 부풀어 버립니다(Dante ×1.22). 극반경으로 두면 ≥ 1 비율이 부피 보존 형상을 재현합니다. (실제 자이언트는
구로 렌더해 이 시각 문제를 비껴갑니다 — 편평은 J₂에만.)
**하드 의존성**(노드를 쓰는 천체는 플러그인 없이는 형상이 안 나옴)이고
눈에 보이는 임계값(a/c ≳ 1.02) 위의 천체만 이를 끌어옵니다. cfg 노드 + 스키마는 `kopernicus-cfg` 스킬에 있습니다(emit 단계에서 채움).

## 6. Worked examples (NearStars roster, Phase 4 active set)

입력값은 큐레이션된 질량 / 반경 / 자전이며, 고정 상태는
[조석고정 타임스케일 방법](tidal-locking-timescale-methodology.md)에서 가져옵니다.

| body | class | ω source | q (or q_s) | J₂ | C̄₂₂ | note |
|---|---|---|---|---|---|---|
| **Erid** (40 Eri A b) | free rocky | P_rot 5.1 h | **0.056** | **~0.017–0.019** | — | 로스터에서 가장 편평한 암석체 — f ≈ 5 %, 인게임에서 보이는 적도 팽대부; 1차 값은 과소예측(큰 q) |
| **Polyphemus** (α Cen A b) | gas giant | P_rot ~10 h | 0.19 | **~0.023–0.026** | — | geopotential-data.md에서 완전히 풀어 둠 (NMoI ~0.23) |
| **TRAPPIST-1 b** | sync. rocky | n (P 1.51 d) | 1.5e-3 | ~1.5e-3 | **~4.6e-4** | 가까운 고정 → 실제 영구 조석 팽대부, J₂ ≈ 지구 수준 |
| **Proxima b** | sync. rocky | n (P 11.2 d) | 2.8e-5 | ~2.8e-5 | ~8e-6 | 충분히 멀어 형상이 미미함(기록만; C₂₂는 emit 임계 아래로 추정) |
| **α Cen A** | star (G2V) | P_rot 22 d | 4.6e-5 | **4.8e-7** | — | 태양앵커 스케일링(0.0105·q); P_rot ±3 d에서 ±~30 % — 상시-emit 정책 아래 처음 emit된 항성 행 |
| **α Cen B** | star (K1V) | P_rot 41 d | 5.5e-6 | **5.7e-8** | — | 같은 방법, ±~15 % |
| **Proxima** | star (M5.5V) | P_rot 83.5 d | 4.4e-8 | **3.7e-9** | — | 완전 대류 → 폴리트로프 NMoI 0.205로 Radau–Darwin (J₂/q 0.084); ±~25 % (반지름 지배) |
| **40 Eri C** | star (M4.5Ve) | P_rot 8.56 d (품질 D 문헌값) | 1.9e-5 | **1.6e-6** | — | 로스터 항성 최대 J₂ — 빠르게 도는 플레어별; 입력이 큐레이션 기각 문헌값이라 documented-divergence로 채택 |
| **40 Eri B** | star (DA WD) | P ≈ 35 h (통계) | 2.5e-8 | **2.1e-9** | — | 백색왜성도 같은 n = 3/2 폴리트로프 분기; 자전 = Kepler 표본 중앙값(Hermes 2017), documented-divergence |
| **Fomalhaut A** | star (A4V) | P_rot ≈ 24 h (도출: v sin i 93 + 측정 i★ 90°) | 0.044 | **1.0e-4** (밴드 0.8–1.3e-4) | — | 로스터 항성 J₂ 압도적 최대 — 근점이동 경로, k₂ = 0.0036 (Claret 2004, 계통 ±25 %); f ≈ 0.022는 보드의 시각 편평과 자기일관; 자전축은 로스터 유일 완전 3D 실측 (Hadjara 2014 i★ 90°±9°, PA 65.6° ⊥ 디스크) |

핵심 대비는 이렇습니다. **Erid**(빠르고 자유로운 뜨거운 슈퍼지구)는 실제로 편평하지만, 고정된 거주가능
영역 암석체들은 고정이 가까울수록 가파르게 커지는 작은 영구 조석 C₂₂를 제외하면 거의 둥글다는 것입니다
(TRAPPIST-1 b ≫ Proxima b). 항성 형상은 의미 있는 궤도 거리에서 동역학적으로 미미하지만, 2026-07-12 오너
정책에 따라 J₂를 계산해 항상 emit합니다 — Principia가 이 항을 싣고 갑니다.

## 7. Procedure (per body)

1. 고정 상태 결정(조석고정 타임스케일 방법) → 자유 또는 동기.
2. q(자유: P_rot) 또는 q_s(고정: 궤도 n)를 **평균** 반경을 써서 계산(Helled+2011 컨벤션; emit하는
   `reference_radius`는 적도 반경).
3. 천체 종류로부터 NMoI 선택(giant 0.20–0.26; rocky 0.30–0.36; star 0.05–0.08) — 가정 + 범위를 명시.
4. 자유 회전체 → Radau–Darwin로 J₂(균질 경계로는 Maclaurin q/2). 동기 → J₂ ≈ (0.9–1.1)·q_s,
   C̄₂₂ = 0.3·J₂(정유체).
5. **복잡한 지오이드를 원하는 암석체** → Kaula(§5)로 degree 3+를 합성하고, 천체마다 시딩 + `synthetic`으로
   표시. 4단계의 2차 항은 그대로 유지. 지형 패스에서 교체.
6. Emit 임계: ~1×10⁻⁶ 아래의 C₂₂는 건너뜀(값은 기록하되 행은 omit). **J₂는 예외 — 크기와 무관하게 계산값을
   항상 emit합니다(오너 정책 2026-07-12, Principia가 이 항을 싣고 감).** `reference_radius` = 적도 반경으로 설정.
7. `db/systems/*`를 직접 건드리지 말고 **큐레이션된 source layer**를 통해 작성한 뒤 rebuild.

## 8. Citations

모든 bibcode는 NASA ADS로 검증했습니다.

- **Helled, Anderson, Schubert & Stevenson 2011**, Icarus 216, 440 (`2011Icar..216..440H`,
  arXiv **[1109.1627](https://arxiv.org/abs/1109.1627)**) — 자이언트에 사용한 Radau–Darwin NMoI ↔ J₂ 관계; §2의 inversion 형태.
  `principia-geopotential-data.md`에 핀.
- **Murray & Dermott 1999**, *Solar System Dynamics* (`1999ssd..book.....M`) §4 — 자전 및
  동기 천체의 정유체 형상; 이 연쇄식의 교과서 본거지.
- **Tricarico 2014**, ApJ 782, 99 (`2014ApJ...782...99T`) — 동기 형상을 현대적으로 엄밀하게 진술,
  곧 J₂/C₂₂ ≈ 10⁄3, (b−c)/(a−c) ≈ 1⁄4, 그리고 고차 Ω²/(πGρ) 보정입니다. **Dermott 1979**,
  Icarus 37, 575 (`1979Icar...37..575D`)와 짝지어 사용 — 위성 형상과 중력 모멘트의 고전적 유도.
- **Pijpers 1998**, MNRAS 297, L76 (`1998MNRAS.297L..76P`) — 헬리오사이즈몰로지 태양
  J₂ = (2.18 ± 0.06)×10⁻⁷. 항성 태양앵커 q-스케일링의 측정 앵커입니다(FGK 항성은 Radau–Darwin을 우회, §2).
- **Chandrasekhar 1939**, *An Introduction to the Study of Stellar Structure*
  (`1939isss.book.....C`) — 폴리트로프 관성모멘트. n = 3/2(완전 대류 M 왜성·비상대론 백색왜성)의
  NMoI ≈ 0.205로, 둘 다 Radau–Darwin 유효범위 안으로 되돌립니다(§2).
- **Hermes et al. 2017**, ApJS 232, 23 (`2017ApJS..232...23H`) — 점근파 백색왜성 자전 분포.
  표본 중앙값 P ≈ 35 h가 자전 미측정 WD의 문서화된 통계 입력입니다(§2).
- **Sterne 1939**, MNRAS 99, 451 (`1939MNRAS..99..451S`) — 근점이동/내부구조 상수.
  J₂ = (2/3)k₂q의 원류입니다(§2). 현대 러브수 형태는 **Ragozzine & Wolf 2009** (`2009ApJ...698.1778R`).
- **Claret 2004**, A&A 424, 919 (`2004A&A...424..919C`; 최신 그리드 Claret 2019
  `2019A&A...628A..29C`) — 이론 k₂ 그리드. A형 계수의 출처이며, 태양 이론-경험 오프셋(~1.27×)이
  정량화된 계통 오차입니다.
- **Hadjara et al. 2014**, A&A 569, A45 (`2014A&A...569A..45H`) — Fomalhaut 최초의 완전 3D 자전 해
  (i★ = 90°±9°, V_eq sin i = 93±16 km/s, PA 65.6°). Le Bouquin 2009(PA ⊥ 디스크)와 함께 로스터에서
  유일하게 완전히 실측된 항성 극입니다.
- **Chandrasekhar 1969**, *Ellipsoidal Figures of Equilibrium* (`1969efe..book.....C`) —
  Maclaurin spheroid(균질 자전 극한, f = 5q/4).
- **Zharkov & Trubitsyn 1978**, *Physics of Planetary Interiors* (`1978ppi..book.....Z`);
  **Hubbard 1984**, *Planetary Interiors* (`1984plin.book.....H`) — 형상 이론, q–f–J₂–NMoI 연쇄식.
- **측정된 동기 형상 앵커**(J₂ = 10⁄3·C₂₂ 캘리브레이션): Io — Anderson
  et al. 2001 (`2001JGR...10632963A`; 형상 축 a−c = 14.4 km, b−c = 3.6 km → 4:1,
  C/MR² = 0.3769); Europa — Anderson et al. 1998 *Science* 4회 근접
  (`1998Sci...281.2019A`); Ganymede — Anderson et al. 1996 (`1996Natur.384..541A`, J₂ & C₂₂
  직접 보고); Titan — Iess et al. 2010 *Science* (`2010Sci...327.1367I`; a−c = 410 m,
  b−c = 103 m → 비율 3.98 ≈ 4:1, C/MR² ≈ 0.34). 모두 J₂/C₂₂ ≈ 10⁄3을 줍니다.
- **Moon — 비-정유체 / 화석 팽대부**: GRAIL 중력장, Zuber et al. 2013 *Science*
  (`2013Sci...339..668Z`); J₂/C₂₂에서 도출한 관성모멘트 + 내부 해석, Williams et al. 2014
  (`2014JGRE..119.1546W`, I_s/MR² = 0.392728). J₂/C₂₂ ≈ 9 ≠ 10⁄3.
- **Fomalhaut A 자전축** — Le Bouquin et al. 2009, A&A 498, L41 (`2009A&A...498L..41L`,
  VLTI/AMBER): A4V, 자전축 PA 65°로 디스크에 ⊥ — 측정된 극을 가진 빠른 자전체임을 확인하지만,
  편평도 수치는 발표되지 않았습니다(§6 주석 참조).
- **합성 고차 장 (§5)**: Kaula 1966, *Theory of Satellite Geodesy*
  (`1966tsga.book.....K`) — degree-variance 거듭제곱 법칙(Earth RMS ≈ 1×10⁻⁵/n²); GRAIL은
  달에 달 고유의 Kaula 제약을 적용하며(Lemoine et al. 2013, `2013JGRE..118.1676L`),
  천체별 재캘리브레이션을 확인합니다. Heightmap→중력(Stage B): Wieczorek, *Gravity and
  Topography of the Terrestrial Planets*, Treatise on Geophysics (`2015trge.book..153W`;
  orig. `2007plmo.book..165W`) — Airy/Pratt isostasy + 중력-지형 admittance.

## Appendix — measured Solar-System gravity fields (analogs)

형상 레시피와 Kaula 캘리브레이션을 위한 레퍼런스 앵커입니다. "deg"는 복원된 최대 구면조화 차수이며,
Earth/Moon/Mars/Venus만이 진정으로 *풍부한* 고차 장을 가집니다(나머지는 모두 degree-2에서 저차까지로,
플라이바이로 복원).

| body | model | deg | J₂ / C₂₂ (×10⁻⁶) | bibcode | dominant signal |
|---|---|---|---|---|---|
| Earth | EGM2008 | 2159 | 1082.6 / 1.57 | `2012JGRB..117.4406P` | 풍부한 지오이드 앵커 (K ≈ 1e-5) |
| Moon | GL0900 / GRGM900 | 900 | (in model) | `2014GeoRL..41.1452K`, `2013JGRE..118.1676L` | **mascon** → 불안정한 저궤도; 고유 Kaula 상수 |
| Mars | MRO120D / GMM-3 | 120 | (in model) | `2016Icar..274..253K`, `2016Icar..272..228G` | Tharsis; 높은 중력-지형 상관 |
| Venus | MGNP180U | 180 | (in model) | `1999Icar..139....3K` | 매우 높은 중력-지형 상관(두꺼운 리소스피어) |
| Mercury | HgM005 | 50 | (in model) | `2014JGRE..119.2417M`, `2019GeoRL..46.3625G` | 저차; k₂ = 0.451 |
| Io | Galileo | 2 | hydrostatic | `1996Sci...272..709A` | degree-2뿐 |
| Europa | Galileo | 2 | hydrostatic | `1998Sci...281.2019A` | degree-2뿐 |
| Ganymede | Galileo / +Juno | 2 | (1996 model) | `1996Natur.384..541A`, `2022GeoRL..4999475G` | degree-2; Juno가 국지적 이상을 시사 |
| Callisto | Galileo | 2 | **32.7 / 10.2** | `2001Icar..153..157A` | degree-2; C/MR² = 0.355, 부분 분화 |
| Titan | Cassini | 3 | k₂ ≈ 0.6 | `2012Sci...337..457I` | 조석 → 지하 바다 |
| Enceladus | Cassini | 3 | **5435 / 1550** | `2014Sci...344...78I` | J₂/C₂₂ = 3.51, 약하게 비-정유체(남극 바다) |
| Vesta | Dawn | 20 | (in model) | `2014Icar..240..103K` | 비-정유체(Rheasilvia) |
| Ceres | Dawn | ~16 | hydrostatic | `2016Natur.537..515P` | 지각 평형 보정; MoI 0.37 |

## Related

- [`principia-geopotential-data.md`](principia-geopotential-data.md) — verbatim
  태양계 계수, 정규화, cfg 형식, Polyphemus 자이언트 워크드 예시.
- [`principia-cfg-reference.md`](principia-cfg-reference.md) — cfg 스키마(노드 문법, 단위).
- [`tidal-locking-timescale-methodology.md`](tidal-locking-timescale-methodology.md) — 고정 상태(형상의 자전 입력).
- [`mass-radius-relation-methodology.md`](mass-radius-relation-methodology.md) — 반경 입력.
- [`methodology-index.md`](methodology-index.md) — 전체 방법론 인덱스.
