<!-- Principia가 싣고 있는 태양계 천체별 지오포텐셜(J2·구면조화) 실제 값 — 우리 천체 작성용 레퍼런스 -->
# Principia 지오포텐셜 데이터 — 태양계 천체 (원본 그대로)

**Principia**가 태양계용으로 싣고 있는 실제 편평도 / 구면조화 중력 데이터입니다. 우리 천체(예: Polyphemus)를 같은 방식으로 작성할 수 있도록 원본을 그대로 옮겨 두었습니다. 이 문서는 [`principia-cfg-reference.md`](principia-cfg-reference.md)가 다루는 cfg *스키마*에 대응하는 *데이터* 짝입니다.

## 출처

- 저장소: **`mockingbirdnest/Principia`**, 파일 **`astronomy/sol_gravity_model.proto.txt`** (`master`).
- 이 파일을 마지막으로 건드린 커밋: `55f4f93` (2019-08-10).
- 파일 헤더의 컨벤션(원문 그대로): 축 방향 / 반경 / 기준 각도 / 각진동수는 *IAU WGCCRE 2009* (Archinal et al.)에서 JD 2451545.0 (2000-01-01 12:00 TDB) 기준으로 가져왔고, 중력 매개변수는 DE431 SPICE 커널(`gm_de431.tpc`)에서 가져왔습니다. **"Degree 2 order 1 is systematically omitted in the geopotentials."**(지오포텐셜에서 차수 2·order 1 항은 일괄적으로 생략됨)

## 형식 — 세 가지 표현, 그리고 proto↔cfg 매핑

Principia가 번들로 싣는 데이터는 **protobuf 텍스트**(`field : value`, 중첩된 `geopotential { row { column {…} } }`)입니다. KSP 쪽 모드 cfg([`principia-cfg-reference.md`](principia-cfg-reference.md))는 동일한 숫자를 KSP 노드 문법(`field = value`, `geopotential_row { geopotential_column {…} }`)으로 씁니다. 편평도는 **세 가지** 형태로 나타납니다.

| 형태 | 사용처 | proto.txt | KSP cfg 대응 |
|---|---|---|---|
| **스칼라 J2** | 태양 | `j2 : 2.11e-07` | `j2 = 2.11e-07` |
| **존(zonal) `j:` row** | 거대행성 4개 | `geopotential { row { degree: N, column { order: 0, j: …, sin: 0 } } }` | `geopotential_row { degree = N, geopotential_column { order = 0, cos = … } }` |
| **전체 cos/sin row** | 지구, 화성, 달 | `column { order: M, cos: …, sin: … }` | `geopotential_column { order = M, cos = …, sin = … }` |

**정규화(중요).** 두 계수 스타일은 정규화 방식이 서로 **다릅니다**.
- **`j2`와 존 `j:` 필드는 정규화되지 않은(UNNORMALIZED)** 존 조화계수 Jₙ입니다(교과서에 나오는 목성 J2 = 0.0147 같은 값).
- **`cos` / `sin`은 정규화된(NORMALIZED)** Stokes 계수 C̄ₙₘ / S̄ₙₘ입니다(지구 C̄₂₀ = −4.84e‑04).
- 차수 2 존 항의 변환식은 **J₂ = −√5 · C̄₂₀** 입니다. 검산하면 지구의 경우 −√5 × (−4.84169e‑04) = **1.0826e‑03** = 알려진 지구 J₂ ✓.

`reference_radius`는 지오포텐셜/J2가 하나라도 존재하면 반드시 있어야 합니다(계수들이 스케일링된 기준 반경이며, 반드시 평균 반경일 필요는 **없습니다**).

---

## 태양 — 스칼라 J2만

```
  body {
    # J2 coefficient and reference radius from http://ilrs.gsfc.nasa.gov/docs/2014/196C.pdf
    name                    : "Sun"
    gravitational_parameter : "1.3271244004193938e+11 km^3/s^2"
    reference_instant       : "JD2451545.000000000"
    mean_radius             : "696000.0 km"
    axis_right_ascension    : "286.13 deg"
    axis_declination        : "63.87 deg"
    reference_angle         : "84.176 deg"
    angular_frequency       : "14.1844000 deg / d"
    j2                      : 2.1106088532726840e-07
    reference_radius        : "696000.0 km"
  }
```
J₂가 아주 작습니다(~2e‑07). 그리고 이것은 인게임 단순화가 아니라 **실측값**입니다. 태양의 실제 편평도는 ≈ 9×10⁻⁶로(적도가 극보다 696,000 km 중 고작 ~6–10 km 더 클 뿐), 자연계에서 가장 둥근 천체 중 하나입니다. 태양은 거대한 자기중력에 비해 느리게(~25일) 자전하므로 원심 편평이 무시할 만합니다. ~10시간으로 도는 가스 거대행성과 정반대인 셈입니다. (태양 J₂가 이렇게 작은 덕분에 수성 근일점 세차가 깔끔한 일반상대성 검증으로 남기도 합니다.)

---

## 목성 — 존 `j:`, 차수 2–12

```
    # Geopotential and reference radius from Iess et al. (2018).
    name : "Jupiter"
    gravitational_parameter : "1.266865349218008e+08 km^3/s^2"
    mean_radius : "69911 km"   reference_radius : "71492 km"
    axis_right_ascension : "268.056595 deg"   axis_declination : "64.495303 deg"
    reference_angle : "284.95 deg"   angular_frequency : "870.5360000 deg / d"
    geopotential {
      row { degree: 2,  column {order: 0, j: 14696.572e-06, sin: 0}},
      row { degree: 3,  column {order: 0, j:    -0.042e-06, sin: 0}},
      row { degree: 4,  column {order: 0, j:  -586.609e-06, sin: 0}},
      row { degree: 5,  column {order: 0, j:    -0.069e-06, sin: 0}},
      row { degree: 6,  column {order: 0, j:    34.198e-06, sin: 0}},
      row { degree: 7,  column {order: 0, j:     0.124e-06, sin: 0}},
      row { degree: 8,  column {order: 0, j:    -2.426e-06, sin: 0}},
      row { degree: 9,  column {order: 0, j:    -0.106e-06, sin: 0}},
      row { degree: 10, column {order: 0, j:     0.172e-06, sin: 0}},
      row { degree: 11, column {order: 0, j:     0.033e-06, sin: 0}},
      row { degree: 12, column {order: 0, j:     0.047e-06, sin: 0}},
    }
```
J₂ = 14696.572e‑06 = **0.014696572**.

## 토성 — 존 `j:`, 차수 2–12

```
    # Geopotential and reference radius from Durante (2017).
    name : "Saturn"
    gravitational_parameter : "3.793120749865224e+07 km^3/s^2"
    mean_radius : "58232 km"   reference_radius : "60330 km"
    axis_right_ascension : "40.589 deg"   axis_declination : "83.537 deg"
    reference_angle : "38.90 deg"   angular_frequency : "810.7939024 deg / d"
    geopotential {
      row { degree: 2,  column {order: 0, j: 16290.564e-06, sin: 0}},
      row { degree: 3,  column {order: 0, j:     0.079e-06, sin: 0}},
      row { degree: 4,  column {order: 0, j:  -935.281e-06, sin: 0}},
      row { degree: 5,  column {order: 0, j:    -0.261e-06, sin: 0}},
      row { degree: 6,  column {order: 0, j:    86.395e-06, sin: 0}},
      row { degree: 7,  column {order: 0, j:     0.018e-06, sin: 0}},
      row { degree: 8,  column {order: 0, j:   -14.533e-06, sin: 0}},
      row { degree: 9,  column {order: 0, j:     0.190e-06, sin: 0}},
      row { degree: 10, column {order: 0, j:     4.746e-06, sin: 0}},
      row { degree: 11, column {order: 0, j:    -0.555e-06, sin: 0}},
      row { degree: 12, column {order: 0, j:    -0.960e-06, sin: 0}},
    }
```
J₂ = 16290.564e‑06 = **0.016290564**.

## 천왕성 — 존 `j:`, 차수 2와 4만

```
    # Spherical harmonic coefficients and reference radius from Jacobson (2014).
    name : "Uranus"
    gravitational_parameter : "5.793951322279009e+06 km^3/s^2"
    mean_radius : "25362 km"   reference_radius : "25559 km"
    axis_right_ascension : "257.311 deg"   axis_declination : "-15.175 deg"
    reference_angle : "203.81 deg"   angular_frequency : "-501.1600928 deg / d"
    geopotential {
      row { degree: 2, column {order: 0, j: 3510.7e-06, sin: 0}},
      row { degree: 4, column {order: 0, j:  -34.2e-06, sin: 0}},
    }
```
J₂ = **0.0035107**. (각진동수가 **음수**입니다 — 천왕성은 역행 자전이기 때문입니다.)

## 해왕성 — 존 `j:`, 차수 2와 4만

```
    # Spherical harmonic coefficients and reference radius from Jacobson (2009).
    name : "Neptune"
    gravitational_parameter : "6.835099502439672e+06 km^3/s^2"
    mean_radius : "24622 km"   reference_radius : "25225 km"
    axis_right_ascension : "299.36 deg"   axis_declination : "43.46 deg"
    reference_angle : "253.18 deg"   angular_frequency : "536.3128492 deg / d"
    geopotential {
      row { degree: 2, column {order: 0, j: 3408.428530717952e-06, sin: 0}},
      row { degree: 4, column {order: 0, j:  -33.398917590066e-06, sin: 0}},
    }
```
J₂ = **0.003408428530717952**.

> **거대행성들의 패턴에 주목.** 짝수 존 항이 강하고(J₂ ≫ J₄ ≫ J₆), 홀수 존 항은 무시할 만하며, tesseral(order > 0) 항은 없습니다 — 빠르게 도는 유체 천체는 매끄럽고 축대칭이기 때문입니다. J₄는 음수입니다(불룩한 부분이 순수 J₂보다 더 빨리 줄어듭니다). 이것이 바로 Polyphemus 같은 가스 거대행성이 따라야 할 형태입니다.

---

## 지구 — 전체 정규화 cos/sin, 차수 2–10

출처 주석: GRACE/GEOS 결합 모델 **GGM05C**(`ftp://ftp.csr.utexas.edu/pub/grace/GGM05/`).

```
    name                    : "Earth"
    gravitational_parameter : "3.9860043543609598e+05 km^3/s^2"
    mean_radius             : "6371.0084 km"
    axis_right_ascension    : "0.0 deg"
    axis_declination        : "90.0 deg"
    reference_angle         : "190.147 deg"
    angular_frequency       : "360.9856235 deg / d"
    reference_radius        : "6378.1363 km"
    geopotential {
      row { degree: 2,
        column {order:  0, cos: -4.8416945732000e-04, sin:  0},
        column {order:  2, cos:  2.4393734159398e-06, sin: -1.4002940118364e-06}},
      row { degree: 3,
        column {order:  0, cos:  9.5716475834116e-07, sin:  0},
        column {order:  1, cos:  2.0304466371688e-06, sin:  2.4824063468478e-07},
        column {order:  2, cos:  9.0476467441002e-07, sin: -6.1900662463325e-07},
        column {order:  3, cos:  7.2128525517036e-07, sin:  1.4144000651650e-06}},
      row { degree: 4,
        column {order:  0, cos:  5.3998153921365e-07, sin:  0},
        column {order:  1, cos: -5.3618081337028e-07, sin: -4.7357697696907e-07},
        column {order:  2, cos:  3.5049214427031e-07, sin:  6.6250516574391e-07},
        column {order:  3, cos:  9.9086103111508e-07, sin: -2.0095089980582e-07},
        column {order:  4, cos: -1.8849242252755e-07, sin:  3.0881857855702e-07}},
      row { degree: 5,
        column {order:  0, cos:  6.8650323458391e-08, sin:  0},
        column {order:  1, cos: -6.2914579409678e-08, sin: -9.4342598600045e-08},
        column {order:  2, cos:  6.5205860316915e-07, sin: -3.2334307981429e-07},
        column {order:  3, cos: -4.5183137844644e-07, sin: -2.1494236736021e-07},
        column {order:  4, cos: -2.9532340917041e-07, sin:  4.9810578844048e-08},
        column {order:  5, cos:  1.7481435046942e-07, sin: -6.6935467701596e-07}},
      row { degree: 6,
        column {order:  0, cos: -1.4997605610883e-07, sin:  0},
        column {order:  1, cos: -7.5943265879397e-08, sin:  2.6525683249700e-08},
        column {order:  2, cos:  4.8635603179946e-08, sin: -3.7376947326560e-07},
        column {order:  3, cos:  5.7251326495652e-08, sin:  8.9731654074799e-09},
        column {order:  4, cos: -8.5996937469007e-08, sin: -4.7142652438675e-07},
        column {order:  5, cos: -2.6716319362048e-07, sin: -5.3649603802896e-07},
        column {order:  6, cos:  9.4799107163032e-09, sin: -2.3738360514414e-07}},
      row { degree: 7,
        column {order:  0, cos:  9.0500819789642e-08, sin:  0},
        column {order:  1, cos:  2.8088622262423e-07, sin:  9.5159759814302e-08},
        column {order:  2, cos:  3.3039550420017e-07, sin:  9.3020287728326e-08},
        column {order:  3, cos:  2.5046335396041e-07, sin: -2.1709707579017e-07},
        column {order:  4, cos: -2.7498638931989e-07, sin: -1.2405070527179e-07},
        column {order:  5, cos:  1.6469638664557e-09, sin:  1.7930957773652e-08},
        column {order:  6, cos: -3.5879864059130e-07, sin:  1.5179288962731e-07},
        column {order:  7, cos:  1.5230586682001e-09, sin:  2.4103042687242e-08}},
      row { degree: 8,
        column {order:  0, cos:  4.9478326949545e-08, sin:  0},
        column {order:  1, cos:  2.3140759375679e-08, sin:  5.8905000941228e-08},
        column {order:  2, cos:  8.0020451775005e-08, sin:  6.5300088951785e-08},
        column {order:  3, cos: -1.9359078476200e-08, sin: -8.5941592936614e-08},
        column {order:  4, cos: -2.4434458705958e-07, sin:  6.9812156090700e-08},
        column {order:  5, cos: -2.5701616796151e-08, sin:  8.9205635687968e-08},
        column {order:  6, cos: -6.5971100477032e-08, sin:  3.0894511043496e-07},
        column {order:  7, cos:  6.7256526485194e-08, sin:  7.4864353638378e-08},
        column {order:  8, cos: -1.2403256812475e-07, sin:  1.2054023904735e-07}},
      row { degree: 9,
        column {order:  0, cos:  2.8022721711668e-08, sin:  0},
        column {order:  1, cos:  1.4214925632662e-07, sin:  2.1415689169158e-08},
        column {order:  2, cos:  2.1411871093739e-08, sin: -3.1680177946272e-08},
        column {order:  3, cos: -1.6060220449404e-07, sin: -7.4250161337509e-08},
        column {order:  4, cos: -9.3492553818025e-09, sin:  1.9898624014305e-08},
        column {order:  5, cos: -1.6315077786051e-08, sin: -5.4043600040799e-08},
        column {order:  6, cos:  6.2784132964798e-08, sin:  2.2296366358079e-07},
        column {order:  7, cos: -1.1798115451725e-07, sin: -9.6920684034663e-08},
        column {order:  8, cos:  1.8813248989960e-07, sin: -3.0019794719453e-09},
        column {order:  9, cos: -4.7558362699944e-08, sin:  9.6876870006845e-08}},
      row { degree: 10,
        column {order:  0, cos:  5.3345275002101e-08, sin:  0},
        column {order:  1, cos:  8.3753701278788e-08, sin: -1.3109438169724e-07},
        column {order:  2, cos: -9.3977781512067e-08, sin: -5.1264999905428e-08},
        column {order:  3, cos: -6.9910538916696e-09, sin: -1.5412815968052e-07},
        column {order:  4, cos: -8.4459158980573e-08, sin: -7.9023911359757e-08},
        column {order:  5, cos: -4.9285509081565e-08, sin: -5.0617431292160e-08},
        column {order:  6, cos: -3.7586959404344e-08, sin: -7.9771481050624e-08},
        column {order:  7, cos:  8.2571270822778e-09, sin: -3.0490009250716e-09},
        column {order:  8, cos:  4.0589757557591e-08, sin: -9.1710645675513e-08},
        column {order:  9, cos:  1.2538547435906e-07, sin: -3.7942358311393e-08},
        column {order: 10, cos:  1.0042327725658e-07, sin: -2.3863826960514e-08}},
    }
```

## 그 외 지구형 천체 (형식 샘플)

암석질/불규칙 천체는 **전체 cos/sin** 형태를 씁니다(고체 맨틀은 울퉁불퉁하고 축대칭이 아니라서 tesseral 항이 존재합니다).
- **화성** — Konopliv et al. (2016) MRO 중력장, 차수 2–10, 전체 order. `reference_radius = 3396 km`, GM `4.282837362069909e+04 km^3/s^2`. 차수 2: `order 0 cos −0.8750220924537e‑03`, `order 2 cos −0.8463302655983e‑04 / sin 0.4893941832167e‑04`.
- **달** — GRAIL GRGM1200A, 차수 2–39(약 38개 row), 전체 cos/sin. `reference_radius = 1738.0 km`.

---

## NearStars 천체에 적용하기

### 왜 중요한가 — 인공위성 (가장 큰 동기)

J₂는 **낮은 인공위성에 작용하는 가장 지배적인 비케플러 섭동**입니다. 승교점 후퇴와 근점 세차를 일으키죠(∝ (R/a)²·cos i). Principia는 비행체(질량 없는 시험 입자)를 **전체 지오포텐셜** 안에서 적분하므로, 플레이어가 띄운 위성은 인게임에서 현실적으로 세차합니다 — 태양 동기 궤도, 동결 궤도, 몰니야 궤도가 모두 정확히 이 효과를 활용합니다. 따라서 지오포텐셜은 천연 위성을 가진 천체뿐 아니라 **플레이어가 주위에 비행체를 띄우는 모든 천체**(사실상 전부)에 대해 **1차 게임플레이 효과**입니다. (천체 자신의 태양 중심 궤도에는 무시할 만하며, 영향을 받는 것은 **그것**을 도는 물체입니다.)

### J₂ — 파생 emit (넓게 설정하면 되고 수작업 비용은 거의 0)

J₂는 자전 + 밀도 + 질량 + 반경으로부터 결정론적으로 따라 나오므로(**Darwin–Radau** 관계), 단위 변환과 마찬가지로 천체별로 자동 계산되는 *파생* emit 필드입니다 — 아트 디렉션 결정이 **아닙니다**. 천체 유형별로 정리하면 다음과 같습니다.

- **가스 거대행성 / 빠르게 자유 자전하는 천체**(Polyphemus) → 존 **J₂**(선택적으로 **J₄** ≈ J₂의 −4 %, **J₆**), tesseral 없음. 값이 큽니다. 목성 0.0147, 토성 0.0163. Polyphemus(~10시간 자전, 0.47 g/cc, 토성의 0.69보다 낮음) → **J₂ ≈ 0.018–0.025**. 형식: 스칼라 `j2`(선택적으로 `geopotential_row`로 J₄/J₆ 추가), `reference_radius` = 적도 반경.
- **자유 자전하는 암석질**(드묾 — 빠르고 비고정) → 작은 존 **J₂**(느린 자전 → 아주 작음). tesseral(경도 방향 덩어리)은 외계행성에서 측정 불가능하므로 생략하거나(J₂만) 합성합니다(class C). 형식: 스칼라 `j2`.
- **조석 고정된 암석질**(로스터의 상당수 — TRAPPIST-1, Proxima b …) → **축대칭이 아님**. 항성을 향한 영구적 조석 팽대부 때문에 삼축이 되어, 차수 2가 **J₂ (C̄₂₀) 그리고 실재하는 C̄₂₂ ≈ 0.3·J₂를 함께** 갖습니다(정수압 비율 J₂ = 10/3·C₂₂, Io/Europa/Ganymede에서 검증됨) — 측정 불가가 아니라 예측 가능합니다. 자전 = 공전 주기(알려진 값). 형식: 차수 2의 전체 cos/sin(`geopotential_row` degree 2: order 0 = C̄₂₀, order 2 = C̄₂₂).

### 추가하는 거대행성의 J₂ 유도 — Radau–Darwin 방법 (문헌 기반)

가상의 거대행성에는 측정된 J₂가 없으므로, 파생값 규칙에 따라 우리가 근거로 삼는 것은 가짜 측정값이 아니라 **방법**입니다. 1차 **Radau–Darwin 관계**를 사용합니다(Helled, Anderson, Schubert & Stevenson 2011, eq. 3, [arXiv:1109.1627](https://arxiv.org/abs/1109.1627); 원전 Zharkov & Trubitsyn 1978 / Murray & Dermott 1999 §4.4).

```
NMoI = C/(M R²) = (2/3)·[1 − (2/5)·√(5m/(m + 3·J₂) − 1)]      m = ω²·R̄³/(G·M)  (MEAN radius)
inverted →  J₂ = (m/3)·[5/(s²+1) − 1],   s = (5/2)·(1 − (3/2)·NMoI)
```

자유 입력값은 단 하나, **정규화된 관성 모멘트** NMoI = C/MR²(중심 집중도)입니다. 이 값은 측정된 거대행성들로 범위를 정합니다 — 목성 ≈ 0.264, 토성 ≈ 0.21, 얼음 거대행성 ≈ 0.22–0.24 (Helled+2011/2020 [[arXiv:2007.10783](https://arxiv.org/abs/2007.10783)]; Fortney+2018 [[arXiv:1609.06324](https://arxiv.org/abs/1609.06324)]; 균질 구체 = 0.40). 질량이 더 작고 밀도가 더 낮은 거대행성은 토성보다 중심 집중이 *덜* 되어 NMoI가 약간 더 높습니다.

**구현은 항상 실제 거대행성으로 먼저 보정합니다**(이 규칙의 검증 단계). 같은 관계식으로 목성 J₂는 **−0.0 %**(m 0.0834, NMoI 0.2648), 토성 J₂는 **−10 %**(m 0.140, NMoI 0.220) 오차로 재현됩니다. 토성의 잔차는 **1차 절단 오차**로, m이 커질수록 함께 커집니다 — 그래서 빠르게 도는 천체(큰 m)에서는 RD 값이 실제 J₂를 약간 *과소*평가합니다.

**계산 예 — Polyphemus** (M = 120 M⊕, R_eq = 1.0 R_Jup, P_rot ≈ 10.1–10.6 h, NMoI ≈ 0.23 [0.21–0.26]). 형상을 반복 계산하면(f = 3⁄2·J₂ + 1⁄2·m → 평균 반경 → m) m ≈ 0.19, 편평도 ≈ 0.13, 그리고 **J₂ ≈ 0.023**(중심값)이 나옵니다. m ≈ 0.19는 토성의 0.14보다 크므로 1차 절단이 ~10–20 % 과소예측합니다 → 실제 ≈ **0.025–0.026**. 범위는 **0.017–0.033**(NMoI 가정이 지배). 거대행성 보정용 J₂는 Iess et al. 2018(목성) / Durante et al. 2017(토성)에서 가져옵니다. 이 값을 쓸 때는 언제나 NMoI 가정과 범위를 함께 명시하세요.

### 고차항은 높이맵에서 (선택, 지형 단계)

울퉁불퉁한 **degree 3+** 중력장은 지형이 생긴 뒤(Kopernicus PQS / Parallax) 천체의 **높이맵**에서 유도할 수 있습니다. 지형을 지각 밀도 질량층으로 보고 등압(Airy) 보상을 적용한 뒤 구면조화 변환을 취하면 → **눈에 보이는 산맥/분지와 정합하는** C̄ₙₘ/S̄ₙₘ가 나옵니다(중력 ↔ 지형의 자기정합). 단서가 있습니다. 가정된 지각 밀도 + 보상 계수가 필요하며(원시 지형은 중력을 *과대평가*합니다 — 큰 지형은 저밀도 뿌리 위에 떠 있으니까요), 가상 천체에서는 이것들이 합성 수준의 선택입니다. **영향은 미미합니다** — J₂가 위성 세차를 2–3 자릿수 차이로 지배하고, 지형 항(~10⁻⁵ 이하)은 아주 낮은 궤도나 표면 중력 측정에서만 의미가 있습니다. 그래서 이건 지형 작업 **이후**로 미루는, 우선순위 낮은 자기정합 마감 작업입니다. **유의할 점은 높이맵이 J₂를 주지 않는다는 것입니다** — J₂는 자전에 의한 형상(Darwin–Radau)이고, 높이맵은 그 기준면에 대해 측정되므로 J₂에 대한 정보를 담고 있지 않습니다.

## 관련 문서
- [`principia-cfg-reference.md`](principia-cfg-reference.md) — cfg *스키마*(노드 문법, 단위, J2/지오포텐셜 필드)
- `phase3/stability-sim/context-notes.md` — 위성 시뮬레이션의 J2 충실도 격차(우리 REBOUND 런은 J2를 생략하지만 Principia는 포함함)
