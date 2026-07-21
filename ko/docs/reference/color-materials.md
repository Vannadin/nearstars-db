<!-- 행성/위성 색을 실제 물질·메커니즘으로 정당화하는 큐레이션 카탈로그 + 관측 veto 게이트 -->
# Color materials & the plausibility gate

관측된 색을 그대로 옮겨 적는 표가 아니라, 색 선택을 정당화하는 도구입니다. 이 모드는 **시각적으로 흥미로운** 세계 쪽으로 기웁니다(게임플레이 다양성 우선 방침). 이 레퍼런스는 그런 *흥미로운* 색 선택을 실재하는 물질이나 메커니즘으로 뒷받침하고, 알맞은 레이어로 보내고, 한 줄짜리 인게임 훅까지 붙일 수 있게 해 줍니다, **관측이 그것을 직접 금지하지 않는 한.**

이 모드의 행성 색은 거의 다 **측정값이 아니라 합성값**입니다. 표면·바다·오로라 색이 측정된 외계행성은 없고, 반사광 색이 측정된 건 뜨거운 목성형 행성 몇 개뿐입니다. 그래서 색은 물리로 게이트하고 데이터로 거부하는 Phase 3 합성 판단의 영역입니다.

---

## 게이트 (이 순서대로 실행)

**1. 관측 veto: 실제 측정값이 제안을 *직접 반박*하는가?** 그렇다면 아무리 흥미로워도 **거부(REJECT)** 합니다. 이게 절대 하한선입니다. 아래 veto 표를 참고하세요. 데이터 상태는 세 가지로 구분합니다.

- **반박됨(Contradicted)**: 측정값이 그것을 배제하는 경우(맨바위로 확인된 행성에 두꺼운 대기를 얹는 것, *측정된* CO₂ 대기를 가진 행성에 CH₄ 청록 외관을 주는 것, 밀도가 가스 외피를 가리키는 천체에 암석 표면 색조를 입히는 것). → 거부하고, 반박되지 않는 가장 가까운 대안을 제시합니다.
- **제약 없음(Unconstrained)**: 비통과(non-transiting)이거나 대기·알베도가 측정된 적이 없는 경우. 그러면 *반박할 대상 자체가 없으므로* 제안은 자유롭고, 2단계만 통과하면 됩니다. (NearStars 행성 대부분은 RV 전용이라 이게 일반적인 경우입니다.)
- **부합함(Consistent)**: 측정값이 제안을 지지하거나 적어도 양립하는 경우. → 근거 있음.

**2. 개연성 / 지속성: *이 천체의* 조건(T, 압력, 조성, 항성 SED)에서 이 색을 만들어 내는 실재 물질이나 메커니즘이 있는가, 그리고 그것이 얼마나 안정적이고 예상 가능한가?**

- **흔한 화학**(Rayleigh 청색, CH₄ 청록, 산화철 적색, 황 황색, tholin 주황, 물얼음 백색) → **lane 1: Phase 3 근거 있음**, 정상 신뢰도.
- **이색적이지만 실재함**(할로젠 기체 색조, 아이오딘 증기 보라색, 전이금속 또는 전하이동 chromophore 광물, 구조색 무지개빛) → **lane 2: cfg-artistic 오버라이드**, 위성이나 합성 이심률과 같은 플래그된 다운스트림 레이어. 신뢰도=낮음, documented divergence, **하지만 진짜 화학 훅을 동반함**, 조작이 아닙니다.
- **생명 의존**(엽록소 녹색, retinal "Purple Earth", 호염성 분홍) → lane 2, 추정성으로 플래그.

**3. 실재하는 물질·메커니즘이 없거나 측정 데이터와 모순되면 → 거부(REJECT).** chromophore 를 지어내는 건 delta-Pav 디스크 실패 모드입니다.

> 베끼지 말고 다시 계산하세요. 큐레이션된 L 과 a 로부터 T_eq = 278.3·L^0.25/√a, S = L/a² 를 구합니다(SKILL physical-plausibility 게이트 참고). 백열/흑체 색은 표면 T 를 따르고, 산란/반사 색은 조성 + 입자 크기 + 항성 SED 를 따릅니다.

---

## 색 물리: 왜 어떤 색은 쉽고 어떤 색은 어려운가

색을 고르기 전에 이 절을 먼저 읽으세요. 메커니즘에 이름을 붙이고, 왜 어떤 색조는 값싸고 어떤 색조는 이색적인지 설명합니다.

- **밴드패스 규칙 (왜 순수한 녹색·마젠타가 어려운가).** 녹색으로 보이려면 적색과 청색을 *둘 다* 흡수하면서 녹색만 통과시켜야 하고, 마젠타는 적색과 청색을 *둘 다* 통과시키면서 녹색만 노치로 잘라 내야 합니다. 흔한 단일 흡수체는 한쪽만 죽입니다(CH₄ 는 적색을 먹어 → 청색/청록으로 읽힘). 그래서 청색이나 적색/갈색 쪽으로 미끄러질 뿐 깔끔한 녹색이나 마젠타에는 닿지 못합니다. 그런 색에는 정교하게 좁힌 노치 흡수체(엽록소, retinal)나 본질적으로 색을 띤 화학종이 필요합니다 → 보통 lane 2 입니다.
- **세 가지 무기 색 엔진.** 선명한 광물 색은 다음 셋 중 하나에서 나옵니다. (1) **d-d 결정장**: 전이금속 이온의 d-오비탈 전이(Cu²⁺ 청색/녹색, Cr³⁺ 녹색 *또는* 적색, Mn²⁺ 분홍, Mn³⁺ 보라, Co²⁺ 분홍, V³⁺ 보라). (2) **원자가간 전하이동(IVCT)**: 인접한 두 금속 이온 사이로 전자가 건너뛰는, *매우* 강한 흡수체라 미량으로도 짙은 색을 냄(Fe²⁺→Ti⁴⁺ 사파이어 청색, Fe²⁺→Fe³⁺ vivianite). (3) **방사선 색중심**: 조사 + 미량 도펀트가 결함을 가두는 경우(자수정 보라, 보라 형석, amazonite 청록). 결정장이 대부분의 색조를 내고, IVCT 가 *가장 짙은 청색*을 내며, 색중심은 조사된 보라/청색을 냅니다.
- **밴드갭 자(반도체 난색 계열).** 황화물/산화물 반도체에서는 밴드갭이 색을 정하고 매끄럽게 미끄러집니다. Eg ≳ 3.0 eV → 백색(S₈ 빈약, TiO₂) · ~2.6 eV → **황색**(S₈, orpiment) · ~2.2 eV → **주황-적색**(헤마타이트) · ~2.0 eV → **짙은 적색**(진사) · ≲ 1.7 eV → **흑색**. Eg 를 낮추면 황색→주황→적색→흑색으로 걸어갑니다. S / As–S / Hg–S / Fe-산화물 계열이 네 개의 우연이 아니라 하나의 그라디언트인 이유입니다.
- **방출은 반사로는 불가능한 선명함을 낼 수 있다.** 반사/산란은 광대역이라 옅거나 탁해지기 쉽습니다. 방출선은 좁아서 대기광/오로라는 어떤 반사 표면도 흉내 낼 수 없는 *순수하고 채도 높은* 색조(O I 557.7 nm 녹색, N₂⁺ 427.8 nm 보라-청색)를 보입니다. **선명하고 순수한 색을 원하면 광휘에 손을 뻗으세요.**
- **구조색은 별개의 범주다**(자체 섹션 참고). 흡수가 아니라 파장 규모의 *구조*(박막, 라멜라, 구체 격자)가 빛과 간섭해서 나오는 색입니다. **goniochromic** 이라서, 색조가 보는 각도에 따라 변합니다(단백석의 불꽃, labradorite 의 섬광, 기름막), 평평한 확산 색조로는 흉내 낼 수 없고, 무지개빛/스페큘러 셰이더가 필요합니다.
- **금속 광택은 색조가 아니라 마감이다.** 황철석 금색, 자연 금, M 형 금속 세계(16 Psyche)가 금속처럼 보이는 건 높은 *스페큘러*, 각도 무관 반사 때문입니다. cfg 단서는 확산 알베도 색이 아니라 금속/스페큘러 재질입니다. 그리고 노출된 Fe-Ni 는 밝은 거울이 아니라 *어두운 건메탈*로 읽힙니다(Psyche 가시 알베도 ~0.1–0.3).
- **산화 상태와 신선/풍화 여부가 색조를 결정한다.** Fe²⁺ → 녹색(감람석, 사문석); Fe³⁺ → 적색/황갈색(헤마타이트, 침철석). 같은 원소가 정반대 색을 냅니다. 신선/환원성 = 녹색; 풍화/산화성 = 적황색. Mn-산화물 바니시는 노출된 암석을 시간이 지나며 검게 만듭니다.
- **생물이 가장 선명한 색을 만든다.** 색소가 좁은 대역에 맞춰진 흡수체이기 때문입니다(엽록소는 적색+청색에 노치를 냄; phycoerythrin ~530–570 nm; retinal ~568 nm → 마젠타). 다만 생명 의존이라 → 추정성입니다. (멜라닌은 예외: 광대역이라 진한 갈색/검정일 뿐 선명하지 않습니다.)
- **차가운 항성은 하늘을 적색 쪽으로 민다.** Rayleigh ∝ λ⁻⁴ 이지만, 산란할 수 있는 청색은 항성이 내보내는 만큼뿐입니다. M 왜성의 적색/IR 편향 SED 는 단파장 플럭스를 거의 남기지 않아 → 같은 맑은 대기가 선명한 청색이 아니라 창백한 회청색으로 읽힙니다. *주의:* 태양 같은 항성 아래에서 순수한 보라/라벤더 Rayleigh 하늘은 물리적으로 **불가능**합니다(보라색 고갈 + 눈의 반응). 라벤더를 평범한 Rayleigh 로 라우팅하지 마세요.
- **백열은 조성이 아니라 온도가 결정한다**: 흑체이며, Draper 점(~800 K)에서 처음으로 흐릿한 적색 광휘가 보이기 시작해 주황/황색을 거쳐 백열(≳1500 K)에 이릅니다. 표면 T 가 문턱을 넘을 때만 라우팅하세요.
- **구름 색은 응결 온도 사다리를 따른다.** 차가움→뜨거움. CH₄/N₂/H₂O/NH₃ 얼음(백색) → NH₄SH + tholin(갈색/황갈색) → H₂SO₄(황백색) → 저온 염/황화물 KCl, ZnS, Na₂S, MnS, Cr(~600–1400 K) → 규산염/철/강옥(~1300–2000 K, 회색 광물 먼지). 구름층 T 에서 화학종을 고르세요.
- **뜨거운 목성형은 기본이 어둡고, 밝은 쪽이 예외다.** 넓은 Na/K 날개(가장 뜨거운 경우 TiO/VO 까지)가 가시광을 들이켜 → 측정된 뜨거운 목성형 대부분은 저알베도입니다(TrES-2 b ≈ 검정). 높은 알베도는 반사성 규산염/금속 구름을 필요로 합니다(HD 189733 b 청색, LTT 9779 b 거울).

---

## 선명한 색 플레이북 (색 기준 색인; 주된 진입점)

"*X* 세계가 갖고 싶다" → 여러 도메인에 걸친 개연성 있는 실현 방법과 각각이 어느 lane 에 안착하는지 정리합니다. 세부 행은 아래 도메인별 표에 있습니다.

### 청색
- **대기**: Rayleigh(맑은 분자 기둥; 청색이 풍부한 밝은 항성에서만 선명) · 차가운 거대행성의 CH₄(Neptune) · 뜨거운 목성형 HD 189733 b 에서 측정된 코발트색(규산염 구름 + Na). lane 1.
- **표면(생명 없이 선명)**: IVCT 사파이어(Fe²⁺→Ti⁴⁺, 가장 짙음) · 청금석/라피스 울트라마린(S₃⁻ 라디칼) · Cu²⁺ azurite · 수화 황산구리(젖으면 청색, 마르면 백색) · amazonite(Pb 방사선 색중심). lane 1–2.
- **얼음 / 물**: 빙하 청색 얼음 & 깊은 물(O–H 진동 배음이 적색을 흡수, 깊이/투명도 필요). lane 1.
- **방출**: N₂⁺ 427.8 nm 보라-청색 오로라 가장자리. tie-break.
- *근거 가장 탄탄:* Rayleigh + 깊은 물/얼음 배음(순수 물리). *가장 선명:* 사파이어 IVCT / 청금석.

### 청록
- **대기**: CH₄ + 높은 안개(Uranus 의 옅음 vs Neptune 의 진함). lane 1.
- **표면**: Cu²⁺ 터키석 / chrysocolla / atacamite(건조하거나 염분 있는 Cu 풍화). lane 1–2.
- **바다**: 빙하 암분(rock flour) 부유물 · 밝은 모래 위 얕은 물. lane 1.

### 녹색
- **표면(생명 없이 선명, 헤드라인)**: Cr³⁺ 에메랄드(uvarovite, 크롬 투휘석, fuchsite)가 가장 순수한 무기 녹색; Cu²⁺ 공작석(malachite); 감람석/사문석은 더 은은한 올리브를 냄. lane 1–2.
- **방출**: O I 557.7 nm 대기광/오로라가 존재하는 가장 순수한 녹색입니다(가장자리 광휘). tie-break.
- **생물**: 엽록소 식생 / 식물플랑크톤. lane 2 추정성.
- **바다**: 녹은 Fe(II) "ferrous sea"(Archean 가설). lane 2.
- **대기(기체)**: 황록색만 가능(Cl₂/ClO₂); 깔끔한 순수 녹색 기체는 없음 → 대기성 녹색은 본질적으로 예술적 선택입니다. lane 2 + 약한 훅.

### 보라/자주/남색
- **표면(생명 없이 선명)**: Mn³⁺ 광물(purpurite, sugilite, charoite)이 진짜 보라색 chromophore, Mn³⁺ 은 보라색에 대해 Cr³⁺ 이 녹색에 대한 것과 같습니다 · V³⁺ tanzanite 청보라 · 자수정 & 보라 형석(방사선 색중심). lane 2.
- **대기**: I₂(아이오딘) 증기가 진짜 보라색입니다. lane 2 + 훅.
- **생물**: retinal "Purple Earth"(DasSarma & Schwieterman); 안토시아닌 식물상(pH 가변). lane 2 추정성.
- **방출**: N₂⁺ 427.8 nm 보라색 광휘. tie-break.
- *Veto:* 평범한 Rayleigh 는 태양 같은 항성 아래에서 라벤더 하늘을 **만들지 못합니다**.

### 분홍/장미/마젠타
- **표면(생명 없음)**: Mn²⁺ rhodochrosite/rhodonite 장미색 · Co²⁺ erythrite("코발트 꽃") 진홍-분홍 · 장미 석영(Fe-Ti 함유물 IVCT, 옅음만). lane 1–2.
- **생물**: 호염성 염호 갯벌(카로티노이드/bacterioruberin) · retinal 마젠타 · 안토시아닌. lane 2 추정성.
- **얼음**: N₂/CH₄ 얼음 위의 얇은 tholin(Triton/Pluto). lane 1.
- *마젠타는 비스펙트럼 색*: 녹색 노치 흡수체가 필요함 → retinal(생명), Co²⁺, 또는 IVCT 여야 하며 광대역 산란으로는 절대 안 됨.

### 적색/진홍/적갈
- **표면**: 헤마타이트(Fe³⁺, 어디에나 있는 행성 적색, Mars) · 진사(HgS, 가장 채도 높음) · Cr³⁺ 루비(에메랄드와 같은 이온이 모암 격자에 따라 뒤집힘) · 계관석(As-S). lane 1(헤마타이트) / lane 2(Hg, As, 루비).
- **방출**: O I 630.0 nm 적색 오로라(높고 희박한 O). tie-break.
- **생물**: phycoerythrin 홍조류 · 원적색 엽록소 적갈색(M 왜성 식물). lane 2 추정성.
- **백열**: T ≳ 800 K 에서 흐릿한 적색 광휘. conditional.

### 주황
- **대기/안개**: tholin(저압 → 주황-적색; 고압 → 황색). lane 1.
- **표면**: 뜨거운 황 동소체(Io 분출구) · 계관석 · ~1000 K 백열. lane 1.
- **생물**: 카로티노이드. lane 2 추정성.

### 황색
- **표면(생명 없이 선명)**: 원소 황 S₈(밴드갭 황색; Io 평원)는 근거 있고 *동시에* 선명함 · 웅황(As-S) 금황색 · jarosite/침철석 황갈색. lane 1(S₈) / lane 2(As).
- **구름/안개**: H₂SO₄ + 황 안개(Venus, 옅음) · 고압 tholin. lane 1.
- **방출**: Na D 589 nm 나트륨 광휘. tie-break.

### 금색/금속 *(색조가 아니라 마감)*
- **표면**: 황철석 FeS₂ 황동빛 금색(어디에나 있음, 근거 있음) · 자연 금 / 호박금(진짜 금, 드묾) · 반동석 bornite(무지개빛 변색, 구조색 참고) · 경면 헤마타이트 & Fe-Ni 금속(강철빛). lane 1–2.
- **세계 전체**: M 형 금속 소행성(16 Psyche): 실재하지만 밝은 거울이 아니라 스페큘러 광택을 띤 *어두운 건메탈*로 읽힘. lane 2, 어둡게 플래그.
- *cfg 단서:* 확산 색조가 아니라 높은 스페큘러 + 금속 재질.

### 갈색/황갈 *(현실적 기본값: 본질적으로 탁함)*
- 침철석/갈철석 황토색 · NH₄SH 띠 · tholin 안개 · CDOM 차색 물 · 사막 바니시 · 혼합 레골리스. 모두 lane 1. 선명한 선택지는 없음: 볼거리가 아니라 정직한 기본값으로 사용하세요.

### 백/회/흑/은
- **백색** ← 휘발성 얼음(H₂O/CO₂/N₂/CH₄), SO₂ 서리(Io), 회장암/장석, 증발잔류 암염(석고/암염), Ceres 의 탄산나트륨 faculae, NH₃ 구름, 금속 구름 LTT 9779 b. **회색** ← 현무암, 풍화 레골리스, 에어로졸/규산염 안개, 뜨거운 광물 구름(chromophore 없는 기본값). **흑색** ← 탄소/유기물, 흑요석, Mn 바니시, 초저알베도 뜨거운 목성형(TrES-2 b). **은색** ← Fe-Ni 금속(스페큘러, 중성). lane 1.

### 무지개색/구조색 *(goniochromic: 특수 셰이더 필요)*
- 단백석 색의 유희(실리카 구체 격자) · 진주층(nacre) · labradorite/spectrolite 섬광 · 월장석 구조 청색 · bornite/비스무트 변색막 무지개 · 기름막/서리막. 선명하지만 **보는 각도에 의존** → 렌더링 주의와 함께 lane 2 artistic(평평한 색조가 아님). 구조색 섹션을 참고하세요.

---

## 도메인별 표

열 구성: **색 · 물질/메커니즘 · 조건 · 지속성 → lane · 실제 예 · 인게임 훅**. 지속성이 라우팅 결정을 한데 압축합니다(흔함→Phase 3 / 드묾→cfg-artistic / 불가능→거부).

### 대기: 산란 & 흡수

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 청색 | Rayleigh 산란 | 맑은 분자 기체, 강한 흡수체 없음, 단파장 밝은 항성 | common → P3 | Earth | 분자 대기가 청색을 산란하는 하늘 |
| 짙은 청색 | 강한 Rayleigh, 크고 맑은 기체 기둥 | 두껍고 맑은 N₂/CO₂, 에어로졸 없음, 뜨겁고 밝은(F/G) 항성 | common → P3 | Earth at depth | 깊고 맑은 공기의 바다 |
| 창백한 회청색 | 적색 SED 아래의 Rayleigh | M 왜성은 적색/IR 에서 정점 → 산란할 청색이 거의 없음 | common → P3 | TRAPPIST-1 worlds (synth) | 청색이 너무 모자라 청색이 못 되는 하늘 |
| 청록/청색 | CH₄ 가 적색을 흡수 | 차가운 H₂/He 거대행성 + CH₄ | common → P3 | Uranus, Neptune | 메테인이 적색광을 삼킨 하늘 |
| 청록/아쿠아마린 | CH₄ + 얇은 고층 안개가 누그러뜨림 | 차가운 거대행성, CH₄ + 고층 안개(Uranus vs Neptune) | common → P3 | Uranus (pale) vs Neptune (deep) | 안개가 부드럽게 누그러뜨린 메테인 청색 |
| 백색 | 흡수가 없는 광학적으로 두꺼운 구름층 | 높은 구름 알베도 | common → P3 | Venus top | 끊김 없이 밝은 구름층 |
| 회색/흐림 | 일반 에어로졸; 규산염 안개(뜨거움) | 먼지 부하; 뜨거운 광물 증기 | common → P3 | 안개 낀 sub-Neptune, 뜨거운 목성형 | 광물 안개가 잿빛으로 흐린 하늘 |

### 대기: 색을 띤 기체 (기체 고유 색; 이색적)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 황록색 | Cl₂(염소) 기체 | 할로젠이 풍부한 이색적 탈가스 | rare → artistic | (자연 사례 없음) | 염소 녹색이 드리운 대기 |
| 황록색 (더 짙음) | ClO₂(이산화염소) 기체 | 이색적 Cl-O 화학, > 11 °C | rare → artistic | (자연 사례 없음) | 병든 듯한 이산화염소 녹색 |
| 보라색 | I₂(아이오딘) 증기 | 아이오딘이 휘발하는 따뜻한 환경 | rare → artistic | (자연 사례 없음) | 아이오딘 증기가 보라로 물들인 하늘 |
| 적갈색 | Br₂(브로민) 증기 | 따뜻하고 브로민이 휘발 | rare → artistic | (자연 사례 없음) | 브로민 증기, 적갈색 |
| 적갈색 | NO₂ / N₂O₄ | 따뜻한 산화-질소 화학(T 가 오르면 짙어짐) | rare → artistic | (스모그 유사) | 갈색의 매캐한 이산화질소 안개 |
| 옅은 황색 | F₂(플루오린) 기체 | 극단적으로 반응성 높은 할로젠 화학 | rare → artistic (pale) | (자연 사례 없음) | 희미한 플루오린 황색 색조 |
| 옅은 청색 | O₃(오존) 기체 | 매우 두꺼운 O₃ 기둥(행성 규모에서는 흐릿함) | rare → artistic (pale) | (Earth O₃ 는 너무 얇아 안 보임) | 희미한 오존 청색 기운 |
| 체리 적색 | S₃(삼황) 증기 | 뜨거운 황 증기(~440 °C) | rare → artistic | 화산성 황 증기 | 삼황이 뜨거운 대기에서 체리빛으로 빛남 |

### 대기: 광화학 안개

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 주황/갈색 | tholin(CH₄+N₂ → UV 로 쪼개진 유기물), 저압 | 환원성 대기 + UV/우주선 플럭스 | common → P3 | Titan, Pluto, Triton | UV 로 익은 유기물 스모그 |
| 황갈색 | tholin(고압 막) / 황 광화학 안개 | 더 짙은 유기물 안개; 또는 S 함유 기체 + 광분해 | common → P3 | 깊은 Titan 안개, Venus, Io 상단 | 황과 유기물의 광화학 베일 |
| 상층 하늘 색조 | 일반화된 성층권 흡수체(층을 이룬 어떤 흡수 종이든) | 상공의 UV 흡수층(O₃, CH₄, SO₂, tholin, NO₂…) | common → P3 | Scatterer useOzone 슬롯(일반) | 고층 흡수층이 상층 하늘을 칠함 |

### 대기: *측정된* 외계행성 반사 색 (가장 강한 앵커)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 짙은 코발트 청색 | 반사성 규산염("유리 비") 구름이 청색을 산란 + Na 가 > 450 nm 를 흡수 | 뜨거운 목성형, 중층 규산염 구름 | measured → P3 | HD 189733 b (Evans 2013, Ag≈0.4 blue) | 나트륨과 유리 비 구름의 코발트 블루 |
| 거의 흑색 | 구름 없음 + Na/K + TiO/VO 가 거의 모든 빛을 삼킴 | 매우 뜨거운 목성형, 구름이 적은 낮면 | measured → P3 | TrES-2 b (Ag < ~0.01) | 석탄보다 어두운, 빛을 먹는 세계 |
| 밝은 거울 백색 | 두껍고 반사성 높은 규산염/금속 구름, 매우 높은 알베도 | 금속이 풍부한 초고온 Neptune/Jupiter | measured → P3 | LTT 9779 b (Ag≈0.8), Kepler-7 b (≈0.38) | 어둠 속 거대한 금속 구름 거울 |
| 회색/탁함 | Na + K 넓은 D-선 날개가 가시광을 지배 | 뜨거운 목성형, 구름 적음 | measured (typical) → P3 | 대부분의 뜨거운 목성형 | 알칼리 증기가 햇빛을 들이켜는 세계 |

### 방출 / 대기광 / 오로라 (반사가 아니라 광휘: 선명한 순수 색)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 선명한 녹색 | O I 557.7 nm(원자 산소 금지선) | O 함유 대기 + 입자 강하, ~90–100 km | tie-break → artistic low-conf | Earth aurora/airglow | 오로라의 전형적인 산소 녹색 |
| 짙은 적색 | O I 630.0 nm(높고 희박한 O) | 얇고 높은 O, > 200 km, 저밀도 열권 | tie-break → artistic low-conf | Earth high red aurora | 높고 희박한 산소가 붉게 타오름 |
| 황색 | Na D 589 nm(나트륨 방출/대기광) | 들뜬 Na 층(운석/화산 기원) | tie-break → artistic low-conf | Earth Na airglow, Io Na cloud | 나트륨 황색 광휘의 띠 |
| 보라-청색 | N₂⁺ 427.8 nm(제1 음성대) | 강한 강하로 이온화된 N₂, < 100 km | tie-break → artistic low-conf | Earth low aurora fringe | 커튼 아래쪽의 보랏빛 가장자리 |
| 진홍색 (아래 가장자리) | N₂ 제1 양성대 | 조밀한 저층 오로라, 고에너지 전자 | tie-break → artistic low-conf | Earth red-bottomed aurora | 질소의 진홍빛 자락 |
| 희미한 적색 일렁임 | H Balmer (H-alpha 656 nm) | H 풍부(거대행성) 대기 + 들뜸 | tie-break → artistic low-conf | gas-giant H₂ aurora | 희미한 수소-적색 일렁임 |

> 오로라/대기광에는 세 가지가 필요합니다: 방출 종, 입자 들뜸원, 그리고 (조직된 오로라라면) 자기장. 비통과 행성에서는 자기장이 측정되지 않으므로 → 플래그된 낮은 신뢰도 tie-break 로 유지하세요.

### 표면: 결정장 & 전하이동 chromophore (선명한 무기색의 핵심)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 선명한 에메랄드 녹색 | Cr³⁺ 결정장(uvarovite, 크롬 투휘석, fuchsite) | Ca/Al/Mg 규산염 속 미량 Cr³⁺, 초고철질/크로마이트 모암 | uncommon → P3/artistic | uvarovite | 크롬이 물들인 에메랄드 암석 |
| 핏빛 적색 | 강옥 속 Cr³⁺ 결정장(강한 장이 적색으로 뒤집음) | Al₂O₃ 속 미량 Cr, 짧은 Cr–O 결합 | rare → artistic | ruby | 크롬 루비빛 적색(에메랄드와 같은 이온) |
| 녹슨 적색/황토색 | Fe³⁺ 산화물: 헤마타이트(α-Fe₂O₃) | 산화된 철 + 풍화/UV | common → P3 | Mars | 산화철이 붉게 번진 지표 |
| 황갈색 | Fe³⁺ 옥시수산화물: 침철석/갈철석/jarosite | 수화된 산화철; jarosite = 산성-황산염 | common → P3 | bog iron, Mars dust | 수화된 녹, 황갈색 |
| 올리브/병녹색 | 감람석/페리도트·휘석 속 Fe²⁺ | 신선하고 미산화된 초고철질/고철질 | common (fresh) → P3 | 감람석 모래(Papakōlea) | 풍화되지 않은 철녹색 맨틀 암석 |
| 녹색 | 사문석/녹점토 속 Fe²⁺/Fe³⁺ | 수화된(사문암화된) 초고철질; 또는 해성 점토 | common → P3 | serpentinite, greensand | 물에 변질된 맨틀 녹색 |
| 공작석 녹색 | Cu²⁺ 탄산염(공작석) | 이차 Cu, CO₂ 풍부한 산화 풍화 | uncommon → P3/artistic | malachite | 구리-탄산염 녹색 피막 |
| 하늘색/짙은 청색 | Cu²⁺ 탄산염(azurite) | Cu 산화대, 높은 탄산염 | uncommon → P3/artistic | azurite | 구리 청색, azurite |
| 터키색/청록 | Cu²⁺(turquoise, chrysocolla, atacamite) | 건조한 Cu 풍화; atacamite 는 Cl 풍부/염분 필요 | rare → artistic | turquoise | 사막의 구리 터키석 |
| 선명한 청색(마르면 바램) | 수화된 [Cu(H₂O)₆]²⁺ 속 Cu²⁺ d-d | 수화 황산구리 백화, 건조한 Cu 풍화 | uncommon → P3/artistic | chalcanthite | 구리 염, 젖으면 청색 마르면 백색 |
| 장미색/분홍 | Mn²⁺ 탄산염/규산염(rhodochrosite, rhodonite) | Mn 풍부한 탄산염/변성, 환원성 | uncommon → P3/artistic | rhodochrosite | 망간-분홍 암석 |
| 보라 → 진보라 | Mn³⁺ 결정장(purpurite, sugilite, charoite) | 인산염/알칼리 규산염 속 산화 Mn | rare → artistic | sugilite | 망간 보라(보라색의 Cr³⁺) |
| 진홍 → 분홍 | Co²⁺ 결정장(erythrite, "코발트 꽃") | Co 광체 위 이차 수화 Co-비산염 | rare → artistic | erythrite | 진홍빛 코발트-꽃 피막 |
| 청보라(다색성) | zoisite 속 V³⁺ 결정장 | Ca-Al 규산염 속 미량 바나듐, 변성 | rare → artistic | tanzanite | 바나듐이 물들인 zoisite, 청보라 |
| 짙은 사파이어 청색 | Fe²⁺→Ti⁴⁺ 원자가간 전하이동(IVCT) | Al₂O₃ 속 인접 Al 자리의 미량 Fe+Ti | rare → artistic | sapphire | 철-티타늄 전자 교환이 청색으로 태움 |
| 청색 → 남색(빛 속에서) | Fe²⁺→Fe³⁺ 인산철(II)의 내부 광산화 | 무산소, P 풍부, Fe 풍부 퇴적물; 빛/공기에서 짙어짐 | uncommon → P3/artistic | vivianite | 스스로 산화해 청색이 되는 인산철 |
| 옅은 장미색 | dumortierite 유사 나노섬유 함유물 속 Fe–Ti IVCT | 미량 Ti+Fe 붕규산염 섬유가 든 괴상 석영 | rare → artistic (pale) | rose quartz | 희미한 장미 석영 홍조 |
| 검댕 같은 흑색 표피 | Mn³⁺/⁴⁺ 산화물(사막 바니시) | 건조한 표면, 시간이 흐르며 Mn-산화물 피복 | common → P3 | desert varnish | 망간으로 검어진 바니시 |

### 표면: 밴드갭 반도체, 라디칼 & 색중심 chromophore

> 밴드갭 자: Eg 를 낮추면 **황색 → 주황 → 적색 → 흑색**으로 걸어갑니다(S₈ ~2.6 → 헤마타이트 ~2.2 → 진사 ~2.0 eV). 라디칼과 색중심 경로는 여기 묶인 별개의 메커니즘입니다.

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 레몬 → 황금 황색 | 원소 황 S₈ 밴드갭(~2.6 eV) | 급랭된 S 화산활동/분기공 | common → P3 | Io plains | 황으로 포장된 화산 노면 |
| 황금 황색 | 웅황 As₂S₃ 밴드갭 | 고온 As+S 분기공/온천 | rare → artistic | orpiment | 금황색 비소 유리 |
| 루비 적색/주황 | 계관석 α-As₄S₄ 밴드갭/전하이동 | 저온 열수/화산성 As+S | rare → artistic | realgar | 비소-황화물 루비빛 피막 |
| 주홍/버밀리언 | 진사 HgS 밴드갭(~2.0 eV) | 저온 Hg 풍부 열수/화산 분출구 | rare → artistic | cinnabar | 수은-황화물 주홍 |
| 울트라마린 청색 | 알루미노규산염 격자 속 S₃⁻ 삼황 라디칼(lazurite) | S 함유 알칼리성 변성, 환원 후 갇힘 | rare → artistic | lapis lazuli | 갇힌 황 라디칼이 청색으로 빛남 |
| 보라(가열하면 황색으로 바램) | Fe³⁺ + γ-조사 → 석영 속 정공 색중심 | 석영 속 미량 Fe + U/Th/K-40 선량 | uncommon → P3/artistic | amethyst | 조사된 철-도핑 석영; 가열하면 citrine |
| 녹색→청색→보라 | 형석 속 콜로이드-Ca + F-중심 색중심 | 방사성 모암 근처의 CaF₂, 조사됨 | rare → artistic | purple fluorite | 방사선으로 자란 칼슘 콜로이드 |
| 청록 | microcline 속 Pb + 물 방사선 색중심 | Pb + 결합수를 가진 K-장석, 조사됨 | rare → artistic | amazonite | 조사된 납 함유 장석 |

### 표면: 금속/경면 광택 (뚜렷한 외관, 높은 스페큘러, 각도 무관)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 황동빛 금색(금속광택) | 황철석 FeS₂ 금속 광택 | 황화/열수 Fe-S 광상 | common → P3 | pyrite ("fool's gold") | 황철석의 놋쇠빛 금속 광택 |
| 진짜/옅은 금색 | 자연 금 / 호박금(Au, Ag 합금) | 자연 금속 농집, 열수 | rare → artistic | native gold | 버터빛 자연 금 광택 |
| 강철빛 은회색 | 경면 헤마타이트 + 철-니켈 금속 | 노출된 금속/specularite, 닦인 산화물 | uncommon → P3/artistic | specularite, meteoric Fe-Ni | 닦인 강철 회색 광택 |
| 어두운 건메탈(금속광택) | M 형 소행성 Fe-Ni 금속 레골리스(노출 핵 유사) | 파괴된 분화 천체, 금속 풍부 지각 | rare → artistic (dark, not mirror) | 16 Psyche | 벗겨진 금속 핵, 광택 없는 건메탈 |

### 표면: 흔한 암석, 얼음, 황, 탄소, 용융물

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 어두운 회색/흑색 | 현무암, 고철질/초고철질 규산염 | 화산성, 미풍화 | common → P3 | Moon 의 바다(maria), Mercury | 갓 식은 현무암 평원 |
| 밝은 회색/백색 | 회장암 / 사장석 | 장석질 고지대 지각 | common → P3 | 달 고지대 | 밝은 장석질 암석 |
| 분홍빛 회색 | 화강암(K-장석 + 석영) | 규장질 대륙 지각 | common → P3 | granite shields | 분홍-회색 화강암 |
| 중간 회색(특징 없음) | 우주풍화된 혼합 레골리스 | 무대기 천체, 미소운석 + 태양풍 정원화 | common → P3 | 대부분의 무대기 표면 | 풍화된 레골리스가 기본 회색으로 바램 |
| 밝은 백색 | 황산염/증발잔류암(석고, 암염, 경석고) | 증발한 염수, 건조한 분지 | common → P3 | White Sands, salt flats | 눈부신 백색 염원 |
| 눈부신 백색 점 | 탄산나트륨 염수 증발잔류물 | 표면에 도달한 빙화산성 염수 | common → P3 | Ceres / Occator faculae | 밝은 소금 분수 잔류물 |
| 밝은 황색 | 원소 황(S₈, 저온) | S 화산활동/분기공, 급랭 | common → P3 | Io plains | 황으로 포장된 화산 평원 |
| 백색 서리 | SO₂ 서리(고산란 응결물) | 활발한 S 화산활동 + 콜드트랩; 분출구는 어두움 | common → P3 | Io (Colchis Regio) | 화산성 이산화황 서리가 평원을 희게 만듦 |
| 주황 → 적색 → 흑색 | 뜨거운 황 동소체(열에 따라 이동) | 분출구 근처의 용융/뜨거운 황 | common → P3 | Io hot flows | 분출구로 갈수록 검어지는 뜨거운 황 |
| 밝은 백색 | 깨끗한 물얼음 / 서리 | 차가운 표면, 신선한 H₂O 입자 | common → P3 | Europa, Enceladus | 깨끗한 물얼음 껍질 |
| 백색 | CO₂ / N₂ / CH₄ 휘발성 서리 | 매우 차갑고 휘발성이 응결 | common → P3 | Mars caps, Triton, Pluto | 얼어붙은 휘발성 서리 |
| 빙하 청색/청록 | 두껍고 맑은 얼음: O–H 배음이 긴 경로에서 적색을 흡수 | 조밀하고 기포 없는, 압축된/깊은 얼음 | common (needs depth) → P3 | glacial blue ice | 깊은 얼음이 적색을 삼킴 |
| 적갈색/연어색 | 얼음 위 tholin 착색(조사된 CH₄+N₂) | 차가운 얼음 위 UV/우주선이 가공한 메테인 | common → P3 | Pluto, Charon pole, Triton | 방사선에 그을린 유기물 얼음 |
| 매우 어두움/흑색 | 흑연 / 검댕 / 내화성 유기물 | C 가 풍부한 원시 물질 | common → P3 | C-type asteroids, comet crust | 탄소로 검게 그을린 지각 |
| 칠흑색(유리질) | 흑요석 / 규산염 화산 유리 | 급랭된 규장-중성 용융물 | common → P3 | obsidian flows | 급랭으로 유리처럼 검어진 용암 |
| 흐릿한 적색 → 백열 광휘 | 흑체 백열(Draper ~800 K → ≳1500 K) | 표면 T 가 문턱을 넘음 | conditional → P3 if T clears | active lava, 55 Cnc e dayside | 가시광으로 빛나는 녹은 암석 |

> "질소 얼음 분홍"은 N₂ 고유 색이 **아닙니다**. N₂/CH₄ 얼음 위에서 조사된 메테인이 만든 얇은 tholin 층입니다. 질소가 아니라 tholin 의 공으로 돌리세요.

### 바다 / 표면 액체

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 짙은 청색 | 순수한 물: 배음 적색 흡수 + 청색 산란 | 맑고 깊은 물기둥 | common → P3 | Earth open ocean | 적색을 먹고 청색을 산란하는 물 |
| 터키색/뿌연 청록 | 부유한 빙하 암분(청록색을 산란) | 침식으로 생긴 미세 광물 부유물 | common → P3 | Lake Louise | 암석 가루가 물을 터키색으로 바꿈 |
| 열대 청록 | 밝은 얕은 바닥 위 짧은 경로 산란 | 탄산염/석영 모래 위 얕고 맑은 물 | common → P3 | tropical lagoons | 밝은 모래 위 얕은 물이 청록으로 빛남 |
| 녹색 | 녹은 Fe(II)가 녹색 창을 엶(청색 + 적색을 흡수) | 무산소, 철 풍부(Archean 형) | uncommon → P3/artistic | early-Earth "green ocean" hypothesis | 산소 없는 하늘 아래 철의 바다 |
| 녹슨 적색 | 부유한 제2철 산화물 | 산화철이 실린 물, 강 플룸 | uncommon → P3/artistic | 철로 물든 하구 | 얕은 물을 흐리게 하는 철녹 |
| 갈색/차색 | CDOM(녹은 유기물, 타닌)이 청색+UV 흡수 | 유기물 풍부, 늪지 유역 | common → P3 | Rio Negro, blackwater rivers | 타닌으로 물든 차색 물 |
| 어두움/거의 흑색 | 액체 탄화수소(CH₄/C₂H₆), 낮은 알베도 | 매우 차가운(~90 K) 탄화수소 순환 | common (cold) → P3 | Titan, Kraken Mare | 검고 고요한 메테인-에테인 바다 |
| 옅음/무색 | 액체 황산 / 농축 염수 | 뜨겁고 S 풍부한(산성) 또는 증발잔류 염수 | uncommon → P3/artistic | Venus-droplet analog | 부식성의 유리 같은 표면 액체 |
| 빛나는 주황-적색 | 백열하는 용융 규산염(용암호) | T_surf ≳ ~1000–1300 K, 활발한 화산활동 | conditional → P3 if T clears | Io paterae, 55 Cnc e | 잉걸불처럼 빛나는 녹은 암석 |
| 분홍/적색 | 호염성 카로티노이드(Dunaliella + Halobacterium/Salinibacter) | 초염분 염수, 강한 UV | speculative → artistic | Lake Hillier | 소금을 좋아하는 미생물이 물들인 염호 |
| 녹색/청록 | 식물플랑크톤 / 엽록소 대증식 | 생명, 영양 풍부한 얕은 물 | speculative → artistic | Earth coastal blooms | 대증식으로 물든 살아 있는 얕은 바다 |

### 생물 색소 (생명 의존 → 추정성, 그러나 가장 선명함)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 선명한 녹색 | 엽록소 a/b: 맞춰진 밴드패스(적색 ~660 + 청색 ~430 흡수) | 산소 발생 광합성, 태양 같은 가시광 플럭스 | speculative → artistic | Earth vegetation | 빛을 먹는 생명의 녹색 |
| 짙은 적색/적갈색 | 원적색 엽록소 f / 박테리오엽록소(창이 ~700–1000 nm 로 이동) | 적색/M 왜성 SED 아래의 광합성 | speculative → artistic | far-red cyanobacteria | 붉은 태양 빛에 맞춰진 잎 |
| 주황/황색 | 카로티노이드(β-카로틴, 박테리오루베린) | 보조/광보호 색소 | speculative → artistic | autumn foliage, Dunaliella | 카로티노이드 주황의 지표 식물 |
| 짙은 적색 | phycoerythrin(녹색 ~530–570 nm 흡수) | 홍조류 / 시아노박테리아, 깊은 물 | speculative → artistic | red algae | 깊은 녹색을 잡으려 붉어진 조류 |
| 청색/청록 | phycocyanin(주황-적색 ~610–660 nm 흡수) | 시아노박테리아, 표면 막 | speculative → artistic | cyanobacterial mats | 청색 색소를 띤 미생물 매트 |
| 보라/마젠타 | retinal(bacteriorhodopsin): 녹색 ~568 nm 흡수 | "Purple Earth" retinal 광영양 | speculative → artistic | hypothesis (DasSarma & Schwieterman) | retinal 색소 생물권, 보라색 |
| 적색→보라→청색 | 안토시아닌: pH 의존 액포 색소 | 식물 조직, 스트레스/저온 반응 | speculative → artistic | autumn / blue flowers | pH 로 가변하며 식물상을 칠하는 색소 |
| 갈색/흑색 | 멜라닌: 광대역 흡수체(선명하지 않음) | 광보호, 강한 UV 표면 | speculative → artistic | dark biological crusts | UV 를 막으며 표면을 어둡게 하는 색소 |

### 구름 (응결물 + chromophore; 차가움 → 뜨거움 사다리)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 백색 | 물얼음 구름(흡수 없음, 높은 산란) | T 가 H₂O 응결을 허용 | common → P3 | Earth | 밝은 물얼음 구름층 |
| 백색 | 암모니아(NH₃) 얼음 구름(순수) | 차가운 거대행성, NH₃ 응결(~150 K) | common → P3 | Jupiter pure-NH₃ regions | 얼어붙은 암모니아 구름 상단 |
| 밝은 백색 | 메테인/에테인 얼음 구름 | 매우 차가운 얼음 거대행성 대기 | common → P3 | Neptune bright clouds, Titan | 고층의 메테인 얼음 권운 |
| 갈색/황갈색 | NH₄SH: 신선할 땐 무색, 방사분해/UV 산물이 청색을 흡수 | 거대행성 띠 화학, 따뜻한 층 | common → P3 | Jupiter belts | 황화암모늄의 갈색 띠 |
| 황백색 | 황산(H₂SO₄) 에어로졸 방울 | S 화산활동, 뜨겁고 두꺼운 대기 | common → P3 | Venus | 황산 구름 베일 |
| 적색(불확실) | 미상의 chromophore: 방사분해된 NH₄SH / S-P 광화학 / Carlson NH₃+아세틸렌 | 상승류가 S/P 기체를 UV 가 비추는 구름 상단으로 올림 | uncertain → P3 low-conf | Jupiter Great Red Spot | 폭풍 상단의 광화학 적색 |
| 회색/탁함(뜨거움) | 규산염 + 철 + 강옥 광물 구름 | 뜨거움(L 왜성 / 뜨거운 목성형), ~1300–2000 K | measured (BDs) → P3 | L dwarfs, hot Jupiters | 녹은 암석과 철 먼지의 구름 |
| 소금-황화물 안개 | 저온 광물 구름: KCl, ZnS, Na₂S, MnS, Cr | ~600–1400 K(T 왜성 / 따뜻한 거대행성) | measured → P3 | T dwarfs | 따뜻한 하늘의 소금-황화물 안개 |
| 매우 붉음(NIR) | 두꺼운 광물 먼지 구름이 젊은/먼지 많은 대기를 붉게 만듦 | 먼지 많은 L 왜성 / 저중력 거대행성 | measured → P3 | HR 8799 b/c/d, ULAS J2227 | 먼지가 너무 두꺼워 세계 전체가 붉게 빛남 |

---

## 구조색 & 간섭색 (goniochromic: 별개의 범주)

흡수가 아니라 파장 규모의 **물리적 구조**(박막, 라멜라, 구체 격자)가 빛과 간섭해서 나오는 색입니다. 위의 모든 것과 달리 색조가 **보는/조명 각도에 따라 변하고(goniochromism)**, **평평한 확산 색조로는 재현할 수 없습니다**. 무지개빛/스페큘러 셰이더, 환경 맵, 또는 최소한 강한 스페큘러+프레넬 패스가 필요합니다. **lane 2 / 렌더링 주의를 단 artistic** 으로 보내세요. 실재하고 근거 잡을 수 있지만 평평한 표면 색이 아니라 *재질 마감* 결정입니다(방출이 색조가 아니라 특수 메커니즘인 것과 같습니다). 선명하지만 방향성이 있습니다.

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| 옮겨가는 스펙트럼 조각 | 광결정: 정렬된 ~150–300 nm 실리카 구체에서 Bragg 회절 | 수화 실리카가 규칙적 구체 격자로 침적 | rare → artistic (play-of-color) | precious opal | 묻힌 구체 격자가 돌아갈 때마다 색을 쏨 |
| 청색/녹색/금색 섬광 | ~128–252 nm 분리 라멜라에서 다층 간섭 | 천천히 식은 Ca 풍부 사장석(Bøggild gap) | rare → artistic (directional flash) | labradorite / spectrolite | 장석 라멜라가 labradorite 청색으로 번쩍임 |
| 떠다니는 청백색 광택 | 파장 이하 장석 라멜라에서 Rayleigh 산란(색소가 아니라 구조) | 정장석-조장석 연정, ~120–150 nm 라멜라 | rare → artistic (goniochromic) | moonstone (adularescence) | 파장 이하 라멜라가 달빛 청색을 산란 |
| 파스텔 청록 광택 | 아라고나이트 판상 박막 + 가장자리 회절 | 층상 ~0.5 µm 탄산염 판 + 유기물 시트 | rare → artistic (iridescent) | nacre / mother-of-pearl | 층층이 쌓인 조개 판이 진주층처럼 어른거림 |
| 무지개 청-보라-금 | Cu-Fe 황화물 위 파장 두께 변색막의 박막 간섭 | bornite 표면에 ~λ 두께 산화막이 자람 | rare → artistic (iridescent) | bornite "peacock ore" | 구리 광석 위 변색막 무지개 |
| 전스펙트럼 무지개 | 비스무트 산화막의 박막 간섭 | 비스무트가 공기 중에서 식으며 산화 | rare → artistic (iridescent) | bismuth crystal | 맨 금속 위 산화막 무지개 |
| 움직이는 무지개 | 두께가 변하는 액체/얼음 막의 박막 간섭 | 반사 바탕 위 ~λ 두께의 투명한 막 | conditional → artistic (iridescent) | oil slick, soap bubble, frost film | 두께가 변하는 얇은 막이 무지개를 칠함 |

---

## 관측 veto (게이트 1단계)

실제 측정값이 제안을 직접 반박하면 그 제안은 **거부(REJECT)** 됩니다. NearStars 행성 대부분은 RV 전용이라 이 중 *어느 것에도* 걸리지 않습니다(→ 제약 없음 → 자유). veto 는 관련 측정값이 실제로 존재할 때만 작동합니다.

| proposal | vetoed by | example bodies |
|---|---|---|
| thick atmosphere | 맨바위 낮면을 보여 주는 열 위상곡선 / 방출 스펙트럼(열 재분배 없음; 밝기 T ≈ 항성 직하점) | TRAPPIST-1 b (Greene 2023), TRAPPIST-1 c (Zieba 2023), LHS 3844 b (Kreidberg 2019) |
| atmosphere of composition X | 조성 Y 의 대기가 *측정됨*(색은 실제 종에 맞아야 함) | 55 Cnc e, JWST CO₂/CO secondary atmosphere (Hu 2024) |
| solid/rocky surface tint, lava surface | 평균 밀도(질량+반지름) → mini-Neptune / 가스 외피 → 보이는 표면 없음 | H/He 외피를 가진 모든 sub-Neptune |
| reflected-light color | *측정된* 기하 알베도 / 반사 색 | HD 189733 b deep blue (Evans 2013); TrES-2 b near-black (low albedo) |
| liquid-water ocean | T_eq 가 물의 임계점을 한참 넘거나 온실효과 없이 빙점을 한참 밑돎 → 안정된 액체 물 없음 | 뜨겁거나 차가운 극단 |
| lavender / violet Rayleigh sky | 기초 광학: 보라색 고갈 + 눈의 반응 때문에 맑은 대기 산란은 태양 같은 항성 아래에서 보라가 아니라 청색으로 읽힘 | (보라색은 I₂ 기체 / Mn³⁺ 표면 / 오로라로 대신 라우팅) |

veto 에 걸리면 반박되지 않는 가장 가까운 대안을 제시합니다(예: TRAPPIST-1 b 의 두꺼운 대기가 veto 됨 → 어두운 현무암질 맨바위 표면, 얇은/없는 하늘).

---

## 워크드 예시

**Tau Ceti e: 선명한 녹색(PHM 컨셉).** RV 전용(비통과)이라 반지름·대기·알베도가 측정된 적이 없습니다 → **제약 없음**, veto 없음. 녹색 *기체* 대기에는 깔끔한 메커니즘이 없습니다(Cl₂/ClO₂ 는 황록색까지밖에 못 감 → lane 2, 약함). 하지만 녹색 *세계*는 쉽습니다. 녹색을 **표면**(Cr³⁺ 에메랄드 / 사문석, 무기)이나 **식생**(엽록소, lane 2 추정성)으로 보내고, 선택적으로 **O I 557.7 nm 녹색 대기광**을 더하세요. **판정: 녹색 유지**, 녹색 가스가 아니라 녹색 표면 ± 대기광으로. 인게임: *"희미한 산소 녹색 대기광 아래 크롬과 사문석의 녹색 지각."*

**엔진 골라잡기: 생명 없이 선명한 색.** 무기 팔레트는 넓습니다. **청색**(IVCT 사파이어 / 청금석 / Cu azurite), **녹색**(Cr³⁺ 에메랄드 / Cu 공작석), **보라**(Mn³⁺ sugilite / 자수정), **적색**(진사 / Cr³⁺ 루비 / 헤마타이트), **황색**(S₈ / 웅황), **분홍**(Co²⁺ erythrite / Mn²⁺ rhodochrosite), **금색-금속**(황철석 / 자연 금), **무지개색**(단백석 / labradorite). 어느 것도 생물권이 필요 없습니다. 이제 녹색 섹션만 깊은 게 아닙니다. 각각 진짜 화학 훅과 함께 lane 1–2 에 안착하고, 구조색/금속색은 마감/셰이더 주의를 동반합니다.

**"TRAPPIST-1 b 의 두꺼운 대기": 거부.** JWST 방출(Greene 2023)이 맨바위 낮면을 보여 줍니다 → 두꺼운 대기는 **1단계에서 veto**. 대안: 어두운 현무암질/초고철질 맨바위 표면 색조, 하늘 없음.

---

## 사용 노트
- 이 카탈로그는 교과서적이고 확립된 색 화학을 사용합니다. **rare / artistic / speculative / uncertain** 으로 표시된 행은 신뢰도가 낮으며, 실제 천체의 Phase 3 문서나 cfg 에 적어 넣을 때는 **사용 시점에 출처를 핀으로 고정**해야 합니다(값 검증 규율).
- 가장 순수하고 채도 높은 색을 원하면 기체 색조나 일반 산란보다 **방출**(대기광/오로라)이나 **전이금속 / IVCT / 생물** chromophore 를 택하세요. 광대역 산란은 옅어지는 경향이 있습니다.
- **구조색과 금속색**은 평평한 색조가 아니라 *재질 마감* 결정입니다(스페큘러, 무지개빛, 각도). 렌더링 필요성을 플래그하세요.
- 반사율 대 별빛 컨벤션은 `disk-color.md` 를 따릅니다. 물질 고유 색을 두고, 렌더러/항성이 조명을 입히는 방식입니다. 디스크 도메인은 이 표가 아니라 Mie 엔진(`scripts/phase3/disk_color_mie.py`)을 사용하세요.
- 오로라 *방출선* 색(정확한 파장)은 [`element-plasma-colors.md`](./element-plasma-colors.md) 에 카탈로그화되어 있습니다. firefly 의 `composition-color.md` 는 재진입 플라즈마 bulk-gas 색을 다룹니다.
- 합성 흐름에 결선하는 작업(SKILL.md 의 정식 색 게이트 + `## Color` 제안 섹션)은 idea-#2 아키텍처 결정(Phase 3 확장 vs Phase 4)이 정해질 때까지 보류입니다. 이 문서는 두 방향 모두가 쓸 수 있는 아키텍처 중립적 토대입니다.

## Related

- [surface-color-albedo-methodology](surface-color-albedo-methodology.md) — 이 카탈로그가 뒷받침하는 표면 광물색 + Bond albedo 레시피입니다.
- [atmosphere-reflected-color-methodology](atmosphere-reflected-color-methodology.md) — 하늘/구름 반사색. 공용 CIE 1931 → sRGB 엔진을 소유합니다.
- [debris-disk-color-methodology](debris-disk-color-methodology.md) — 잔해원반 먼지의 Mie 산란색 경로입니다.
- [element-plasma-colors](element-plasma-colors.md) — 발광/플라스마색(오로라·재진입·선)입니다.
- [methodology-index](methodology-index.md) — 모든 도출값 방법론 레시피의 인덱스입니다.
