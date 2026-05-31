<!-- 행성/위성 색을 실제 물질·메커니즘으로 정당화하는 큐레이션 카탈로그 + 관측 veto 게이트 -->
# 색 물질과 개연성 게이트

관측된 색을 그대로 옮겨 적는 표가 아니라, 색 선택을 정당화하는 도구입니다. 이 모드는 **시각적으로 흥미로운** 세계 쪽으로 기웁니다(게임플레이 다양성 우선 방침). 이 레퍼런스는 그런 *흥미로운* 색 선택을 실재하는 물질이나 메커니즘으로 뒷받침하고, 알맞은 레이어로 보내고, 한 줄짜리 인게임 훅까지 붙일 수 있게 해 줍니다 — **관측이 그것을 직접 금지하지 않는 한.**

이 모드의 행성 색은 거의 다 **측정값이 아니라 합성값**입니다 — 표면·바다·오로라 색이 측정된 외계행성은 없고, 반사광 색이 측정된 건 뜨거운 목성형 행성 몇 개뿐입니다. 그래서 색은 물리로 게이트하고 데이터로 거부하는 Phase 3 합성 판단의 영역입니다.

---

## 게이트 (이 순서대로 진행)

**1. 관측 veto — 실제 측정값이 제안을 *직접 반박*하는가?** 그렇다면 아무리 흥미로워도 **거부**합니다. 이게 절대 하한선입니다. 아래 veto 표를 참고하세요. 데이터 상태는 세 가지로 구분합니다.

- **반박됨(Contradicted)** — 측정값이 그것을 배제하는 경우(맨바위로 확인된 행성에 두꺼운 대기를 얹는 것, *측정된* CO₂ 대기를 가진 행성에 CH₄ 청록 외관을 주는 것, 밀도가 가스 외피를 가리키는 천체에 암석 표면 색조를 입히는 것). → 거부하고, 반박되지 않는 가장 가까운 대안을 제시합니다.
- **제약 없음(Unconstrained)** — 비통과(non-transiting)이거나 대기·알베도가 측정된 적이 없는 경우. 그러면 *반박할 대상 자체가 없으므로* 제안은 자유롭고, 2단계만 통과하면 됩니다. (NearStars 행성 대부분은 RV 전용이라 이게 일반적인 경우입니다.)
- **부합함(Consistent)** — 측정값이 제안을 지지하거나 적어도 양립하는 경우. → 근거 있음.

**2. 개연성 / 지속성 — *이 천체의* 조건(T, 압력, 조성, 항성 SED)에서 이 색을 만들어 내는 실재 물질이나 메커니즘이 있는가, 그리고 그것이 얼마나 안정적이고 예상 가능한가?**

- **흔한 화학**(Rayleigh 청색, CH₄ 청록, 산화철 적색, 황 황색, tholin 주황, 물얼음 백색) → **lane 1: Phase 3 근거 있음**, 정상 신뢰도.
- **이색적이지만 실재함**(할로젠 기체 녹색, 아이오딘 증기 보라색, 존재는 하지만 형성 결과로는 예상되지 않는 chromophore) → **lane 2: cfg-artistic 오버라이드**, 위성이나 합성 이심률과 같은 플래그된 다운스트림 레이어. 신뢰도=낮음, documented divergence, **하지만 진짜 화학 훅을 동반함** — 조작이 아닙니다.
- **생명 의존**(엽록소 녹색, retinal "Purple Earth") → lane 2, 추정성으로 플래그.

**3. 실재하는 물질·메커니즘이 없거나 측정 데이터와 모순되면 → 거부.** chromophore 를 지어내는 건 delta-Pav 디스크 실패 모드입니다.

> 베끼지 말고 다시 계산하세요. 큐레이션된 L 과 a 로부터 T_eq = 278.3·L^0.25/√a, S = L/a² 를 구합니다(SKILL physical-plausibility 게이트 참고). 백열/흑체 색은 표면 T 를 따르고, 산란/반사 색은 조성 + 입자 크기 + 항성 SED 를 따릅니다.

---

## 선명한 색 플레이북 (색 기준 인덱스, 주된 진입점)

"녹색 세계가 갖고 싶다" → 여러 도메인에 걸친 개연성 있는 실현 방법과 각각이 어느 lane 에 안착하는지 정리합니다. 세부 행은 아래 도메인별 표에 있습니다.

### 선명한 청색  *(근거 잡기 가장 쉬움)*
- **대기** — 강한 Rayleigh(맑고 깊은 N₂/CO₂; 단파장이 밝은 항성) · 차가운 H₂/He 거대행성의 CH₄ 흡수(Neptune). lane 1.
- **뜨거운 목성형** — 규산염 구름 반사 + Na 흡수 → 코발트 블루; HD 189733 b 에서 *측정됨*(Evans 2013). lane 1.
- **바다** — 깊고 순수한 액체 물. lane 1.

### 녹색  *(가장 어려움; 대부분 lane 2)*
- **대기** — Cl₂ / 할로젠 기체는 실제로 황록색이고, 황 동소체 증기도 마찬가지. 이색적이고 표준 탈가스 산물이 아님 → lane 2 + 훅.
- **표면** — 감람석/휘석의 신선한 초고철질 노출(은은한 올리브색); 엽록소 식생(생명 → lane 2 추정성).
- **바다** — 식물플랑크톤/엽록소(생명); 무산소 환경에서 녹은 Fe(II)의 "ferrous sea"(가설) → lane 2.

### 자주색 / 보라색
- **대기** — I₂(아이오딘) 증기가 보라색. lane 2 + 훅.
- **표면 / 생물권** — retinal 광영양생물이 보라색을 반사("Purple Earth", DasSarma & Schwieterman). lane 2 추정성.

### 황색 → 주황 → 갈색 → 적색  *(근거가 탄탄한 그라디언트)*
- 황산 / 황 에어로졸(Venus 의 옅은 황색) → 원소 황 표면(Io) → tholin 광화학 안개(Titan/Pluto 의 주황-갈색) → 산화철 표면(Mars 의 적색). 모두 lane 1.

### 백색 / 회색 / 흑색
- 백색 ← 두껍고 흡수 없는 구름, 물/CO₂/N₂ 얼음, 회장암. 회색 ← 에어로졸/규산염 안개, 광물 구름(뜨거움). 흑색 ← 탄소/유기물, 현무암, 알베도가 극히 낮은 뜨거운 목성형(Na/K + TiO/VO; 예 TrES-2 b). lane 1.

---

## 도메인별 표

열 구성: **색 · 물질/메커니즘 · 조건 · 지속성 → lane · 실제 예 · 인게임 훅**. 지속성이 라우팅 결정을 한데 압축합니다(흔함→Phase 3 / 드묾→cfg-artistic / 불가능→거부).

### 대기 (기체 산란 + 흡수 + 에어로졸)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| blue | Rayleigh 산란 | 맑은 분자 기체, 강한 흡수체 없음, 단파장 밝은 항성 | common → P3 | Earth | 분자 대기가 청색을 산란하는 하늘 |
| muted cyan-grey | 차가운 항성 아래 Rayleigh | 같은 조건이나 M 왜성 SED 가 적색 쪽으로 어둡게 밀어냄 | common → P3 | TRAPPIST-1 e (synth) | 붉은 태양에 흐려진 푸른 하늘 |
| cyan / blue | CH₄ 가 적색을 흡수 | 차가운 H₂/He 거대행성 + CH₄ | common → P3 | Uranus, Neptune | 메테인이 적색광을 삼킨 하늘 |
| orange / brown | tholin 광화학 안개 | CH₄+N₂ + UV 플럭스 | common → P3 | Titan, Pluto | UV 로 익은 유기물 스모그 |
| pale yellow | H₂SO₄ / 황 에어로졸 | S 화산활동, 두껍고 뜨거움 | common → P3 | Venus | 황산 구름이 드리운 베일 |
| **yellow-green** | **Cl₂ / 할로젠 기체** | 할로젠이 풍부한 이색적 화학 | **rare → artistic** | (자연 사례 없음) | 염소 기운이 도는 하늘 |
| **violet** | **I₂(아이오딘) 증기** | 아이오딘이 휘발하는 따뜻한 환경 | **rare → artistic** | (자연 사례 없음) | 아이오딘 증기가 보라로 물들인 하늘 |
| white | 흡수가 없는 광학적으로 두꺼운 구름층 | 높은 구름 알베도 | common → P3 | Venus 상층 | 끊김 없이 밝은 구름층 |
| grey / hazy | 일반 에어로졸; 규산염 안개(뜨거움) | 먼지 부하; 뜨거운 광물 증기 | common → P3 | 안개 낀 sub-Neptune, 뜨거운 목성형 | 광물 안개가 잿빛으로 흐린 하늘 |
| cobalt blue | 규산염 구름 반사 + Na | 뜨거운 목성형, 반사성 구름 | measured (few) → P3 | HD 189733 b (Evans 2013) | 나트륨 + 유리 구름의 코발트빛 |

### 표면 (레골리스 / 암석 / 얼음; 확산 반사율)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| red / orange | 산화철(헤마타이트, 침철석) | 산화된 Fe + 풍화 | common → P3 | Mars | 녹슨 산화철 먼지 |
| dark grey / black | 현무암, 고철질/초고철질 규산염 | 화산성, 미풍화 | common → P3 | Moon 의 바다(maria), Mercury | 갓 식은 현무암 평원 |
| very dark | 탄소 / 흑연 / 유기물 | C 가 풍부한 원시 조성 | common → P3 | C 형 소행성 | 탄소로 검게 그을린 지각 |
| light grey / white | 회장암 / 장석 | 장석질 고지대 지각 | common → P3 | 달 고지대 | 밝은 장석질 암석 |
| bright white | 물얼음 | 차가운 표면, H₂O | common → P3 | Europa, Enceladus | 깨끗한 물얼음 껍질 |
| white | CO₂ / N₂ 얼음 서리 | 매우 차가움 | common → P3 | Mars 극관, Triton | 얼어붙은 휘발성 서리 |
| yellow | 원소 황 / SO₂ 서리 | 활발한 S 화산활동 | common → P3 | Io | 황으로 포장된 화산 평원 |
| reddish-brown ice | tholin 으로 물든 얼음 | 얼음 + 조사된 유기물 | common → P3 | Charon 극관, KBO | 방사선에 그을린 얼음 |
| olive green | 신선한 감람석 / 휘석 | 초고철질의 신선한 노출 | uncommon → P3/artistic | 감람석 해변 | 올리브빛 화산 모래 |
| glowing orange | 백열하는 규산염 용융물(흑체) | T_sub ≳ ~1300 K (T_eq ≳ ~1000 K) **또는** 인용된 내부 가열 | conditional → T 가 solidus 를 넘으면 P3 | 55 Cnc e | 가시광으로 빛나는 녹은 암석 |
| green (bio) | 엽록소 식생 | 생명 | speculative → artistic | Earth | 광합성하는 지표 식생 |
| purple (bio) | retinal 광영양생물 | 생명, "Purple Earth" | speculative → artistic | (가설) | retinal 색소 생물권 |

### 바다 / 표면 액체

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| blue | 순수한 액체 물 | 물 바다 | common → P3 | Earth | 적색을 흡수하고 청색을 산란하는 물 |
| green / teal (bio) | 식물플랑크톤 / 엽록소 | 생명 | speculative → artistic | Earth 연안 | 번식으로 물든 얕은 바다 |
| green | 녹은 Fe(II) ferrous | 무산소, Archean 형 | uncommon → artistic | 초기 Earth (가설) | 철이 풍부한 원시 바다 |
| brown / tea | 녹은 유기물(CDOM, 타닌) | 유기물 풍부, 늪지 | uncommon → artistic | 블랙워터 하천 | 타닌으로 물든 물 |
| dark / black | 액체 탄화수소(CH₄/C₂H₆) | Titan 만큼 차가움 | common (cold) → P3 | Titan 호수 | 메테인-에테인 호수 |

### 구름

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| white | 물 / NH₃ / CH₄ 얼음 | 응결 | common → P3 | Earth, Jupiter 의 zone, Neptune | 밝은 얼음결정 구름 |
| yellowish-white | 황산 | S, 뜨거움 | common → P3 | Venus | 황산 안개 |
| brown / tan | NH₄SH(황화수소암모늄), tholin | 거대행성 띠 화학 | common → P3 | Jupiter 의 belt | 황화암모늄의 갈색 띠 |
| red | P / S chromophore(논쟁 중) | 광화학 | uncertain → P3 low-conf | Jupiter 대적반 | 광화학으로 붉어진 폭풍 |
| grey / varied | 규산염 / 철 구름 | 뜨거운 거대행성 / 갈색왜성 | measured → P3 | 뜨거운 목성형, BD | 녹은 광물 구름 |

### 오로라
반사가 아니라 방출 색이며, 이미 별도로 카탈로그화되어 있습니다. [`element-plasma-colors.md`](./element-plasma-colors.md) 와 firefly 의 `composition-color.md` 를 사용하세요. 핵심 방출선은 다음과 같습니다 — O I 557.7 nm 녹색 · O I 630.0 nm 적색(높고 희박한 층) · N₂⁺ 427.8 nm 보라-청색 · N₂ 밴드 적색(하단 가장자리) · 거대행성에서 H Balmer 적색. **조건:** 방출 종을 포함하는 대기 + 자기권 입자 강하(+ 가능하면 자기장). 비통과 행성에서는 자기장/오로라가 tie-break 이므로 → 낮은 신뢰도로 플래그를 유지합니다.

---

## 관측 veto (게이트의 1단계)

실제 측정값이 제안을 직접 반박하면 그 제안은 **거부**됩니다. NearStars 행성 대부분은 RV 전용이라 이 중 *어느 것에도* 걸리지 않습니다(→ 제약 없음 → 자유). veto 는 관련 측정값이 실제로 존재할 때만 작동합니다.

| proposal | vetoed by | example bodies |
|---|---|---|
| 두꺼운 대기 | 맨바위 낮면을 보여 주는 열 위상곡선 / 방출 스펙트럼(열 재분배 없음; 밝기 T ≈ 항성 직하점) | TRAPPIST-1 b (Greene 2023), TRAPPIST-1 c (Zieba 2023), LHS 3844 b (Kreidberg 2019) |
| 조성 X 의 대기 | 조성 Y 의 대기가 *측정됨*(색은 실제 종에 맞아야 함) | 55 Cnc e — JWST CO₂/CO 이차 대기 (Hu 2024) |
| 고체/암석 표면 색조, 용암 표면 | 평균 밀도(질량+반지름) → mini-Neptune / 가스 외피 → 보이는 표면 없음 | H/He 외피를 가진 모든 sub-Neptune |
| 반사광 색 | *측정된* 기하 알베도 / 반사 색 | HD 189733 b 의 짙은 청색 (Evans 2013); TrES-2 b 의 거의 흑색(낮은 알베도) |
| 액체 물 바다 | T_eq 가 물의 임계점을 한참 넘거나 온실효과 없이 빙점을 한참 밑돎 → 안정된 액체 물 없음 | 뜨겁거나 차가운 극단 |

veto 에 걸리면 반박되지 않는 가장 가까운 대안을 제시합니다(예: TRAPPIST-1 b 의 두꺼운 대기가 veto 됨 → 어두운 현무암질 맨바위 표면, 얇은/없는 하늘).

---

## 적용 예시

**Tau Ceti e — 선명한 녹색 대기(PHM 컨셉).** Tau Ceti e 는 RV 전용(비통과)이라 반지름·대기·알베도가 측정된 적이 없습니다 → **제약 없음**, veto 불가능. 녹색 대기 ← 할로젠(Cl₂ 황록) 또는 황 동소체 증기. 실재하는 화학이지만 표준 탈가스 산물은 아님 → **lane 2(cfg-artistic, 플래그, 낮은 신뢰도)**, 진짜 훅 동반. **판정: 녹색 유지.** 인게임: *"Tau Ceti e 의 황록색 하늘은 미량의 할로젠 기체가 적색과 청색을 걸러 낸 결과다 — 형성되기는 드물지만 화학적으로 불가능하지는 않다."* (엔트리를 확정하기 전에 Cl₂/황 색 주장은 출처로 값 검증하세요.)

**"TRAPPIST-1 b 의 두꺼운 대기" — 거부.** JWST 방출(Greene 2023)이 맨바위 낮면을 보여 줍니다 → 두꺼운 대기는 매력과 무관하게 **1단계에서 veto**. 제시한 대안은 어두운 현무암질/초고철질 맨바위 표면 색조, 하늘 없음.

---

## 사용 시 주의

- 이 v1 은 교과서적이고 확립된 색 화학을 사용합니다. **rare / artistic / speculative / debated** 로 표시된 행은 신뢰도가 낮으며, 실제 천체의 Phase 3 문서나 cfg 에 적어 넣을 때는 **사용 시점에 출처를 핀으로 고정**해야 합니다(값 검증 규율).
- 반사율 대 별빛 컨벤션은 `disk-color.md` 를 따릅니다 — 물질 고유 색을 두고, 렌더러/항성이 조명을 입히는 방식입니다. 디스크 도메인은 이 표가 아니라 Mie 엔진(`scripts/phase3/disk_color_mie.py`)을 사용하세요.
- 합성 흐름에 결선하는 작업(SKILL.md 의 정식 색 게이트 + `## Color` 제안 섹션)은 idea-#2 아키텍처 결정(Phase 3 확장 vs Phase 4)이 정해질 때까지 보류입니다. 이 문서는 두 방향 모두가 쓸 수 있는 아키텍처 중립적 토대입니다.
