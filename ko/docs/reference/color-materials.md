<!-- 행성/위성 색을 실제 물질·메커니즘으로 정당화하는 큐레이션 카탈로그 + 관측 veto 게이트 -->
# Color materials & the plausibility gate

관측된 색을 그대로 옮겨 적는 표가 아니라, 색 선택을 정당화하는 도구입니다. 이 모드는 **시각적으로 흥미로운** 세계 쪽으로 기웁니다(게임플레이 다양성 우선 방침). 이 레퍼런스는 그런 *흥미로운* 색 선택을 실재하는 물질이나 메커니즘으로 뒷받침하고, 알맞은 레이어로 보내고, 한 줄짜리 인게임 훅까지 붙일 수 있게 해 줍니다 — **관측이 그것을 직접 금지하지 않는 한.**

이 모드의 행성 색은 거의 다 **측정값이 아니라 합성값**입니다 — 표면·바다·오로라 색이 측정된 외계행성은 없고, 반사광 색이 측정된 건 뜨거운 목성형 행성 몇 개뿐입니다. 그래서 색은 물리로 게이트하고 데이터로 거부하는 Phase 3 합성 판단의 영역입니다.

---

## The gate (run in this order)

**1. 관측 veto — 실제 측정값이 제안을 *직접 반박*하는가?** 그렇다면 아무리 흥미로워도 **거부(REJECT)** 합니다. 이게 절대 하한선입니다. 아래 veto 표를 참고하세요. 데이터 상태는 세 가지로 구분합니다.

- **반박됨(Contradicted)** — 측정값이 그것을 배제하는 경우(맨바위로 확인된 행성에 두꺼운 대기를 얹는 것, *측정된* CO₂ 대기를 가진 행성에 CH₄ 청록 외관을 주는 것, 밀도가 가스 외피를 가리키는 천체에 암석 표면 색조를 입히는 것). → 거부하고, 반박되지 않는 가장 가까운 대안을 제시합니다.
- **제약 없음(Unconstrained)** — 비통과(non-transiting)이거나 대기·알베도가 측정된 적이 없는 경우. 그러면 *반박할 대상 자체가 없으므로* 제안은 자유롭고, 2단계만 통과하면 됩니다. (NearStars 행성 대부분은 RV 전용이라 이게 일반적인 경우입니다.)
- **부합함(Consistent)** — 측정값이 제안을 지지하거나 적어도 양립하는 경우. → 근거 있음.

**2. 개연성 / 지속성 — *이 천체의* 조건(T, 압력, 조성, 항성 SED)에서 이 색을 만들어 내는 실재 물질이나 메커니즘이 있는가, 그리고 그것이 얼마나 안정적이고 예상 가능한가?**

- **흔한 화학**(Rayleigh 청색, CH₄ 청록, 산화철 적색, 황 황색, tholin 주황, 물얼음 백색) → **lane 1: Phase 3 근거 있음**, 정상 신뢰도.
- **이색적이지만 실재함**(할로젠 기체 색조, 아이오딘 증기 보라색, 전이금속 chromophore 광물, 존재는 하지만 형성 결과로는 예상되지 않는 chromophore) → **lane 2: cfg-artistic 오버라이드**, 위성이나 합성 이심률과 같은 플래그된 다운스트림 레이어. 신뢰도=낮음, documented divergence, **하지만 진짜 화학 훅을 동반함** — 조작이 아닙니다.
- **생명 의존**(엽록소 녹색, retinal "Purple Earth", 호염성 분홍) → lane 2, 추정성으로 플래그.

**3. 실재하는 물질·메커니즘이 없거나 측정 데이터와 모순되면 → 거부(REJECT).** chromophore 를 지어내는 건 delta-Pav 디스크 실패 모드입니다.

> 베끼지 말고 다시 계산하세요. 큐레이션된 L 과 a 로부터 T_eq = 278.3·L^0.25/√a, S = L/a² 를 구합니다(SKILL physical-plausibility 게이트 참고). 백열/흑체 색은 표면 T 를 따르고, 산란/반사 색은 조성 + 입자 크기 + 항성 SED 를 따릅니다.

---

## Color physics — why some colors are easy and some are hard

색을 고르기 전에 이 절을 먼저 읽으세요. 왜 순수한 녹색 대신 자꾸 황록색에 안착하게 되는지, 선명한 색이 실제로 어디에 사는지를 설명합니다.

- **밴드패스 규칙 (왜 순수한 녹색이 어려운가).** 녹색으로 보이려면 적색과 청색을 *둘 다* 흡수하면서 녹색만 통과시켜야 합니다 — 밴드패스입니다. 흔한 대기 기체는 한쪽만 흡수합니다. CH₄ 는 적색을 먹어 치워 결과가 청색/청록으로 읽히지 녹색으로 읽히지 않습니다. 단일 흡수체 대기는 청색 쪽이나 적색/갈색 쪽으로 미끄러질 뿐 깔끔한 녹색에는 닿지 못합니다. 순수한 녹색에는 상보적인 흡수체 두 개(엽록소)나 본질적으로 녹색인 기체(Cl₂/ClO₂)가 필요합니다 → 그래서 대기성 녹색은 거의 언제나 lane 2 입니다.
- **방출은 반사로는 불가능한 선명함을 낼 수 있다.** 반사/산란은 광대역이라 연속체를 거르는 일이고, 그래서 옅거나 탁해지기 쉽습니다. 방출선은 좁고 단색이라 대기광/오로라는 어떤 반사 대기도 흉내 낼 수 없는 *순수하고 채도 높은* 색조(O I 557.7 nm 녹색, N₂⁺ 427.8 nm 보라-청색)를 보일 수 있습니다. **선명하고 순수한 색을 원하면 색조가 아니라 광휘에 손을 뻗으세요.**
- **전이금속 d-오비탈(결정장) 흡수가 가장 중요한 *무기* 선명색이다.** Fe, Cr, Cu, Mn 이 무거운 일을 도맡습니다 — 생명이 필요 없습니다. 선명하면서도 근거 있는 표면을 만드는 지렛대입니다.
- **산화 상태와 신선/풍화 여부가 색조를 결정한다.** Fe²⁺ → 녹색(감람석, 사문석, 녹점토); Fe³⁺ → 적색/황갈색(헤마타이트, 침철석). 같은 원소가 산화환원에 따라 정반대 색을 냅니다. 신선/환원성 = 녹색; 풍화/산화성 = 적황색. Mn-산화물 바니시는 노출된 암석을 시간이 지나며 검게 만듭니다.
- **생물이 가장 선명한 색을 만든다.** 색소가 좁은 대역에 맞춰진 흡수체이기 때문입니다(엽록소는 적색+청색에 노치를 냄; phycoerythrin ~530–570 nm; retinal ~568 nm). 반사되는 보색은 채도가 높습니다. 다만 생명 의존이라 → 추정 lane 입니다. (멜라닌은 예외 — *광대역* 흡수체라 진한 갈색/검정일 뿐 선명하지 않습니다.)
- **차가운 항성은 하늘을 적색 쪽으로 민다.** Rayleigh ∝ λ⁻⁴ 이지만, 산란할 수 있는 청색은 항성이 내보내는 만큼뿐입니다. M 왜성의 적색/IR 편향 SED 는 단파장 플럭스를 거의 남기지 않아 → 같은 맑은 대기가 선명한 청색이 아니라 창백한 회청색으로 읽힙니다. 변수는 산란이 아니라 광원입니다.
- **백열은 조성이 아니라 온도가 결정한다** — 흑체이며, Draper 점(~800 K)에서 처음으로 흐릿한 적색 광휘가 보이기 시작해 주황/황색을 거쳐 백열(≳1500 K)에 이릅니다. 표면 T 가 실제로 문턱을 넘을 때만 라우팅하세요.
- **구름 색은 응결 온도 사다리를 따른다.** 차가움→뜨거움. CH₄/N₂/H₂O/NH₃ 얼음(백색) → NH₄SH + tholin(갈색/황갈색) → H₂SO₄(황백색) → 저온 염/황화물 KCl, ZnS, Na₂S, MnS, Cr(~600–1400 K) → 규산염/철/강옥(~1300–2000 K, 회색 광물 먼지). 구름층 T 에서 화학종을 고르세요.
- **뜨거운 목성형은 기본이 어둡고, 밝은 쪽이 예외다.** 넓은 Na/K D-선 날개(가장 뜨거운 경우 TiO/VO 까지)가 가시광을 들이켜 → 측정된 뜨거운 목성형 대부분은 저알베도입니다(TrES-2 b ≈ 검정). 높은 알베도는 알칼리 흡수를 압도하며 산란하는 반사성 규산염/금속 구름을 필요로 합니다(HD 189733 b, LTT 9779 b).

---

## Vivid color playbook (color-indexed; the primary entry point)

"녹색 세계가 갖고 싶다" → 여러 도메인에 걸친 개연성 있는 실현 방법과 각각이 어느 lane 에 안착하는지 정리합니다. 세부 행은 아래 도메인별 표에 있습니다.

### Vivid blue  *(근거 잡기 가장 쉬움)*
- **대기** — 강한 Rayleigh(맑고 깊은 N₂/CO₂; 단파장이 밝은 항성) · 차가운 H₂/He 거대행성의 CH₄ 흡수(Neptune). lane 1.
- **뜨거운 목성형** — 규산염 구름 반사 + Na 흡수 → 코발트 블루; HD 189733 b 에서 *측정됨*(Evans 2013). lane 1.
- **표면** — Cu²⁺ azurite, 청금석/라피스(S₃⁻ 라디칼) 울트라마린, 빙하 청색 얼음(두껍고 맑은 얼음). lane 1–2.
- **바다** — 깊고 순수한 액체 물. lane 1.

### Cyan / teal
- **대기** — CH₄ + 얇은 고층 안개(Uranus 의 옅음 vs Neptune 의 진함). lane 1.
- **표면** — Cu²⁺ 터키석 / 규공작석(chrysocolla) / atacamite(건조하거나 염분 있는 Cu 풍화). lane 1–2.
- **바다** — 빙하 암분(rock flour) 부유물이 청록색을 산란. lane 1.

### Green  *(대기로는 어렵고; 표면으로는 쉬움)*
- **방출(선명하고 실재함)** — O I 557.7 nm 대기광/오로라가 존재하는 가장 순수한 녹색입니다. 대기광/오로라가 강한 세계는 가장자리(limb)에서 선명한 녹색으로 *빛납니다*. tie-break, low-conf.
- **표면, 생명 없음(최고의 무기 선명 녹색)** — **Cr³⁺ 에메랄드 녹색**(uvarovite, 크롬 투휘석, fuchsite)이 가장 채도 높은 무기 녹색; **Cu²⁺ 공작석(malachite)** 녹색; 감람석/페리도트 + 사문석 + 녹점토는 더 은은한 올리브/병녹색을 냄(신선한 초고철질). lane 1–2.
- **생물(가장 상징적)** — 엽록소 식생(표면) / 식물플랑크톤(바다). lane 2 추정성.
- **바다** — 녹은 Fe(II) "ferrous sea"(Archean 가설). lane 2.
- **대기(기체)** — 황록색만 가능. Cl₂ / ClO₂. 깔끔한 순수 녹색 기체는 존재하지 않음 → 대기성 녹색은 본질적으로 예술적 선택입니다. lane 2 + 약한 훅.

### Purple / violet
- **대기** — I₂(아이오딘) 증기가 보라색. lane 2 + 훅.
- **표면 / 생물권** — retinal 광영양생물이 보라색을 반사("Purple Earth", DasSarma & Schwieterman). lane 2 추정성. 안토시아닌 식물상(pH 가변).
- **표면 광물** — 형석 / 일부 Mn 또는 Fe 인산염(은은함). lane 2.

### Yellow → orange → brown → red  *(근거가 탄탄한 그라디언트)*
- 황산 / 황 에어로졸(Venus 의 옅은 황색) → 원소 황 표면(Io 의 황색, 뜨거워지면 붉어짐) → 계관석 황색(orpiment) / 웅황 적색(realgar)(As-S) → tholin 광화학 안개(Titan/Pluto 의 주황-갈색) → 침철석 황갈색 → 헤마타이트 산화철 적색(Mars) → 진사 주홍(HgS). lane 1, As/Hg 계열은 lane 2.

### Pink / rose / magenta
- **표면 광물** — Mn²⁺ 능망간석(rhodochrosite) / 장미휘석(rhodonite) 장미색. lane 1–2.
- **바다 / 생물권** — 호염성 대증식(Dunaliella + Halobacterium 카로티노이드)이 염호 전체를 분홍-적색으로 물들임. lane 2 추정성.
- **얼음** — N₂/CH₄ 얼음 위의 얇은 tholin 막(Triton/Pluto 의 분홍). lane 1.

### White / grey / black
- 백색 ← 두껍고 흡수 없는 구름, 물/CO₂/N₂ 얼음, 회장암, 증발잔류 암염(석고/암염), Ceres 의 탄산나트륨 faculae. 회색 ← 에어로졸/규산염 안개, 광물 구름(뜨거움), 현무암. 흑색 ← 탄소/유기물, 현무암, 흑요석 유리, Mn-산화물 사막 바니시, 알베도가 극히 낮은 뜨거운 목성형(Na/K + TiO/VO; 예 TrES-2 b). lane 1.

---

## Per-domain tables

열 구성: **색 · 물질/메커니즘 · 조건 · 지속성 → lane · 실제 예 · 인게임 훅**. 지속성이 라우팅 결정을 한데 압축합니다(흔함→Phase 3 / 드묾→cfg-artistic / 불가능→거부).

### Atmosphere — scattering & absorption

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| blue | Rayleigh 산란 | 맑은 분자 기체, 강한 흡수체 없음, 단파장 밝은 항성 | common → P3 | Earth | 분자 대기가 청색을 산란하는 하늘 |
| deep blue | 강한 Rayleigh, 크고 맑은 기체 기둥 | 두껍고 맑은 N₂/CO₂, 에어로졸 없음, 뜨겁고 밝은(F/G) 항성 | common → P3 | Earth at depth | 깊고 맑은 공기의 바다 |
| wan grey-blue | 적색 SED 아래의 Rayleigh | M 왜성은 적색/IR 에서 정점 → 산란할 청색이 거의 없음 | common → P3 | TRAPPIST-1 worlds (synth) | 청색이 너무 모자라 청색이 못 되는 하늘 |
| cyan / blue | CH₄ 가 적색을 흡수 | 차가운 H₂/He 거대행성 + CH₄ | common → P3 | Uranus, Neptune | 메테인이 적색광을 삼킨 하늘 |
| teal / aquamarine | CH₄ + 얇은 고층 안개가 누그러뜨림 | 차가운 거대행성, CH₄ + 고층 안개(Uranus vs Neptune) | common → P3 | Uranus (pale) vs Neptune (deep) | 안개가 부드럽게 누그러뜨린 메테인 청색 |
| white | 흡수가 없는 광학적으로 두꺼운 구름층 | 높은 구름 알베도 | common → P3 | Venus top | 끊김 없이 밝은 구름층 |
| grey / hazy | 일반 에어로졸; 규산염 안개(뜨거움) | 먼지 부하; 뜨거운 광물 증기 | common → P3 | 안개 낀 sub-Neptune, 뜨거운 목성형 | 광물 안개가 잿빛으로 흐린 하늘 |

### Atmosphere — colored gases (intrinsic gas color; exotic)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| yellow-green | Cl₂(염소) 기체 | 할로젠이 풍부한 이색적 탈가스 | rare → artistic | (자연 사례 없음) | 염소 녹색이 드리운 대기 |
| yellow-green (more saturated) | ClO₂(이산화염소) 기체 | 이색적 Cl-O 화학, > 11 °C | rare → artistic | (자연 사례 없음) | 병든 듯한 이산화염소 녹색 |
| violet | I₂(아이오딘) 증기 | 아이오딘이 휘발하는 따뜻한 환경 | rare → artistic | (자연 사례 없음) | 아이오딘 증기가 보라로 물들인 하늘 |
| red-brown | Br₂(브로민) 증기 | 따뜻하고 브로민이 휘발 | rare → artistic | (자연 사례 없음) | 브로민 증기, 적갈색 |
| red-brown | NO₂ / N₂O₄ | 따뜻한 산화-질소 화학(T 가 오르면 짙어짐) | rare → artistic | (스모그 유사) | 갈색의 매캐한 이산화질소 안개 |
| pale yellow | F₂(플루오린) 기체 | 극단적으로 반응성 높은 할로젠 화학 | rare → artistic (pale) | (자연 사례 없음) | 희미한 플루오린 황색 색조 |
| pale blue | O₃(오존) 기체 | 매우 두꺼운 O₃ 기둥(행성 규모에서는 흐릿함) | rare → artistic (pale) | (Earth O₃ 는 너무 얇아 안 보임) | 희미한 오존 청색 기운 |
| cherry red | S₃(삼황) 증기 | 뜨거운 황 증기(~440 °C) | rare → artistic | 화산성 황 증기 | 삼황이 뜨거운 대기에서 체리빛으로 빛남 |

### Atmosphere — photochemical haze

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| orange / brown | tholin(CH₄+N₂ → UV 로 쪼개진 유기물) | 환원성 대기 + UV/우주선 플럭스 | common → P3 | Titan, Pluto, Triton | UV 로 익은 유기물 스모그 |
| pale yellow-tan | 황 / 폴리설퍼 광화학 안개 | S 함유 화산 기체 + 광분해 | common → P3 | Venus 상층 안개, Io 분출구 상단 | 황으로 물든 광화학 베일 |
| upper-sky tint | 일반화된 성층권 흡수체(층을 이룬 어떤 흡수 종이든) | 상공의 UV 흡수층(O₃, CH₄, SO₂, tholin, NO₂…) | common → P3 | Scatterer useOzone 슬롯(일반) | 고층 흡수층이 상층 하늘을 칠함 |

### Atmosphere — *measured* exoplanet reflected color (strongest anchors)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| deep cobalt blue | 반사성 규산염("유리 비") 구름이 청색을 산란 + Na 가 > 450 nm 를 흡수 | 뜨거운 목성형, 중층 규산염 구름 | measured → P3 | HD 189733 b (Evans 2013, Ag≈0.4 blue) | 나트륨과 유리 비 구름의 코발트 블루 |
| near-black | 구름 없음 + Na/K + TiO/VO 가 거의 모든 빛을 삼킴 | 매우 뜨거운 목성형, 구름이 적은 낮면 | measured → P3 | TrES-2 b (Ag < ~0.01) | 석탄보다 어두운 — 빛을 먹는 세계 |
| bright mirror-white | 두껍고 반사성 높은 규산염/금속 구름, 매우 높은 알베도 | 금속이 풍부한 초고온 Neptune/Jupiter | measured → P3 | LTT 9779 b (Ag≈0.8), Kepler-7 b (≈0.38) | 어둠 속 거대한 금속 구름 거울 |
| grey / muddy | Na + K 넓은 D-선 날개가 가시광을 지배 | 뜨거운 목성형, 구름 적음 | measured (typical) → P3 | 대부분의 뜨거운 목성형 | 알칼리 증기가 햇빛을 들이켜는 세계 |

### Emission / airglow / aurora (a glow, not reflectance — vivid pure colors)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| vivid green | O I 557.7 nm(원자 산소 금지선) | O 함유 대기 + 입자 강하, ~90–100 km | tie-break → artistic low-conf | Earth aurora/airglow | 오로라의 전형적인 산소 녹색 |
| deep red | O I 630.0 nm(높고 희박한 O) | 얇고 높은 O, > 200 km, 저밀도 열권 | tie-break → artistic low-conf | Earth high red aurora | 높고 희박한 산소가 붉게 타오름 |
| yellow | Na D 589 nm(나트륨 방출/대기광) | 들뜬 Na 층(운석/화산 기원) | tie-break → artistic low-conf | Earth Na airglow, Io Na cloud | 나트륨 황색 광휘의 띠 |
| violet-blue | N₂⁺ 427.8 nm(제1 음성대) | 강한 강하로 이온화된 N₂, < 100 km | tie-break → artistic low-conf | Earth low aurora fringe | 커튼 아래쪽의 보랏빛 가장자리 |
| crimson (low edge) | N₂ 제1 양성대 | 조밀한 저층 오로라, 고에너지 전자 | tie-break → artistic low-conf | Earth red-bottomed aurora | 질소의 진홍빛 자락 |
| faint red shimmer | H Balmer (H-alpha 656 nm) | H 풍부(거대행성) 대기 + 들뜸 | tie-break → artistic low-conf | gas-giant H₂ aurora | 희미한 수소-적색 일렁임 |

> 오로라/대기광에는 세 가지가 필요합니다 — 방출 종, 입자 들뜸원, 그리고 (조직된 오로라라면) 자기장. 비통과 행성에서는 자기장이 측정되지 않으므로 → 기본값이 아니라 플래그된 낮은 신뢰도 tie-break 로 유지하세요. Jupiter 의 오로라는 태양계에서 가장 *강력*하지만 대부분 UV/IR 입니다 — 출력은 가시성이 아닙니다.

### Surface — transition-metal chromophores (the vivid-inorganic core)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| vivid emerald green | Cr³⁺ 결정장(uvarovite, 크롬 투휘석, fuchsite) | Ca/Al/Mg 규산염 속 미량 Cr³⁺, 초고철질/크로마이트 모암 | uncommon → P3/artistic | uvarovite, 크롬 투휘석 | 크롬이 물들인 에메랄드 암석 |
| rust red / ochre | Fe³⁺ 산화물 — 헤마타이트(α-Fe₂O₃) | 산화된 철 + 풍화/UV | common → P3 | Mars | 산화철이 붉게 번진 지표 |
| yellow-brown / ochre | Fe³⁺ 옥시수산화물 — 침철석/갈철석 | 수화된 산화철, 축축한 풍화 | common → P3 | bog iron, Mars dust | 수화된 녹, 황갈색 |
| olive / bottle green | 감람석/페리도트·휘석 속 Fe²⁺ | 신선하고 미산화된 초고철질/고철질 | common (fresh) → P3 | 감람석 모래(Papakōlea), peridot | 풍화되지 않은 철녹색 맨틀 암석 |
| green | 사문석 속 Fe²⁺/Fe³⁺ | 수화된(사문암화된) 초고철질 | common → P3 | serpentinite | 물에 변질된 맨틀 녹색 |
| grey-green (muted) | 녹점토(glauconite, celadonite, chlorite) | 해성/변질 현무암 점토, 혼합가 Fe | common → P3 | greensand, celadonite | 철-점토 녹색 토양 |
| malachite green | Cu²⁺ 탄산염(공작석) | 이차 Cu, CO₂ 풍부한 산화 풍화 | uncommon → P3/artistic | malachite | 구리-탄산염 녹색 피막 |
| azure / deep blue | Cu²⁺ 탄산염(azurite) | Cu 산화대, 높은 탄산염 | uncommon → P3/artistic | azurite | 구리 청색, azurite |
| bright turquoise / cyan | Cu²⁺(turquoise, chrysocolla, atacamite) | 건조한 Cu 풍화; atacamite 는 Cl 풍부/염분 필요 | rare → artistic | turquoise, chrysocolla | 사막의 구리 터키석 |
| rose / pink | Mn²⁺ 탄산염/규산염(rhodochrosite, rhodonite) | Mn 풍부한 탄산염/변성, 환원성 | uncommon → P3/artistic | rhodochrosite | 망간-분홍 암석 |
| sooty black veneer | Mn³⁺/⁴⁺ 산화물(사막 바니시) | 건조한 표면, 시간이 흐르며 Mn-산화물 피복 | common → P3 | desert varnish | 망간으로 검어진 바니시 |

### Surface — non-metal vivid chromophores (rare but genuine inorganic)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| ultramarine blue | 알루미노규산염 격자 속 S₃⁻ 삼황 라디칼(lazurite) | S 함유 알칼리성 변성, 환원 후 갇힘 | rare → artistic | lapis lazuli | 갇힌 황 라디칼이 청색으로 빛남 |
| ruby red / orange | As–S 전하이동(realgar α-As₄S₄) | 저온 열수/화산성 As+S, 분기공 | rare → artistic | realgar | 비소-황화물 루비빛 피막 |
| golden yellow | As–S(orpiment As₂S₃) | 고온 As+S, 온천/분기공 | rare → artistic | orpiment | 금황색 비소 유리 |
| scarlet / vermilion | HgS 전하이동(cinnabar) | 저온 Hg 풍부 열수/화산 분출구 | rare → artistic | cinnabar | 수은-황화물 주홍 |

### Surface — common rock, ice, sulfur, carbon, melt

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| dark grey / black | 현무암, 고철질/초고철질 규산염 | 화산성, 미풍화 | common → P3 | Moon 의 바다(maria), Mercury | 갓 식은 현무암 평원 |
| light grey / white | 회장암 / 사장석 | 장석질 고지대 지각 | common → P3 | 달 고지대 | 밝은 장석질 암석 |
| pinkish grey | 화강암(K-장석 + 석영) | 규장질 대륙 지각 | common → P3 | granite shields | 분홍-회색 화강암 |
| bright white | 황산염/증발잔류암(석고, 암염, 경석고) | 증발한 염수, 건조한 분지 | common → P3 | White Sands, salt flats | 눈부신 백색 염원 |
| brilliant white spot | 탄산나트륨 염수 증발잔류물 | 표면에 도달한 빙화산성 염수 | common → P3 | Ceres / Occator faculae | 밝은 소금 분수 잔류물 |
| bright yellow | 원소 황(S₈, 저온) | S 화산활동/분기공, 급랭 | common → P3 | Io plains | 황으로 포장된 화산 평원 |
| orange → red → black | 뜨거운 황 동소체(열에 따라 이동) | 분출구 근처의 용융/뜨거운 황 | common → P3 | Io hot flows | 분출구로 갈수록 검어지는 뜨거운 황 |
| bright white | 깨끗한 물얼음 / 서리 | 차가운 표면, 신선한 H₂O 입자 | common → P3 | Europa, Enceladus | 깨끗한 물얼음 껍질 |
| white | CO₂ / N₂ / CH₄ 휘발성 서리 | 매우 차갑고 휘발성이 응결 | common → P3 | Mars caps, Triton, Pluto | 얼어붙은 휘발성 서리 |
| glacial blue / cyan | 두껍고 맑은 얼음 — O–H 배음이 긴 경로에서 적색을 흡수 | 조밀하고 기포 없는, 압축된/깊은 얼음 | common (needs depth) → P3 | glacial blue ice | 깊은 얼음이 적색을 삼킴 |
| red-brown / salmon | 얼음 위 tholin 착색(조사된 CH₄+N₂) | 차가운 얼음 위 UV/우주선이 가공한 메테인 | common → P3 | Pluto, Charon pole, Triton | 방사선에 그을린 유기물 얼음 |
| very dark / black | 흑연 / 검댕 / 내화성 유기물 | C 가 풍부한 원시 물질 | common → P3 | C-type asteroids, comet crust | 탄소로 검게 그을린 지각 |
| jet black (glassy) | 흑요석 / 규산염 화산 유리 | 급랭된 규장-중성 용융물 | common → P3 | obsidian flows | 급랭으로 유리처럼 검어진 용암 |
| dull red glow | 흑체 백열 시작(Draper ~800 K) | 표면 T ≳ 800 K | conditional → P3 if T clears | hot lava skin | 처음 어리는 흐릿한 적색 열광 |
| orange → white-hot glow | 더 뜨거운 흑체 | T ≈ 1000–1500+ K | conditional → P3 | active lava, 55 Cnc e dayside | 가시광으로 빛나는 녹은 암석 |

> "질소 얼음 분홍"은 N₂ 고유 색이 **아닙니다** — N₂/CH₄ 얼음 위에서 조사된 메테인이 만든 얇은 tholin 층입니다. 질소가 아니라 tholin 의 공으로 돌리세요.

### Ocean / surface liquid

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| deep blue | 순수한 물 — 배음 적색 흡수 + 청색 산란 | 맑고 깊은 물기둥 | common → P3 | Earth open ocean | 적색을 먹고 청색을 산란하는 물 |
| turquoise / milky cyan | 부유한 빙하 암분(청록색을 산란) | 침식으로 생긴 미세 광물 부유물 | common → P3 | Lake Louise, meltwater lakes | 암석 가루가 물을 빙하빛으로 바꿈 |
| green | 녹은 Fe(II)가 녹색 창을 엶(청색 + 적색을 흡수) | 무산소, 철 풍부(Archean 형) | uncommon → P3/artistic | 초기 Earth "green ocean" 가설 | 산소 없는 하늘 아래 철의 바다 |
| rusty red | 부유한 제2철 산화물 | 산화철이 실린 물, 강 플룸 | uncommon → P3/artistic | 철로 물든 하구 | 얕은 물을 흐리게 하는 철녹 |
| brown / tea | CDOM(녹은 유기물, 타닌)이 청색+UV 흡수 | 유기물 풍부, 늪지 유역 | common → P3 | Rio Negro, blackwater rivers | 타닌으로 물든 차색 물 |
| dark / near-black | 액체 탄화수소(CH₄/C₂H₆), 낮은 알베도 | 매우 차가운(~90 K) 탄화수소 순환 | common (cold) → P3 | Titan, Kraken Mare | 검고 고요한 메테인-에테인 바다 |
| pale / colorless | 액체 황산 / 농축 염수 | 뜨겁고 S 풍부한(산성) 또는 증발잔류 염수 | uncommon → P3/artistic | Venus-droplet analog | 부식성의 유리 같은 표면 액체 |
| glowing orange-red | 백열하는 용융 규산염(용암호) | T_surf ≳ ~1000–1300 K, 활발한 화산활동 | conditional → P3 if T clears | Io paterae, 55 Cnc e | 잉걸불처럼 빛나는 녹은 암석 |
| pink / red | 호염성 카로티노이드(Dunaliella + Halobacterium) | 초염분 염수, 강한 UV | speculative → artistic | Lake Hillier, saltern ponds | 소금을 좋아하는 미생물이 물들인 염호 |
| green / teal | 식물플랑크톤 / 엽록소 대증식 | 생명, 영양 풍부한 얕은 물 | speculative → artistic | Earth coastal blooms | 대증식으로 물든 살아 있는 얕은 바다 |

### Biological pigments (life-dependent → speculative, but the most vivid)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| vivid green | 엽록소 a/b — 맞춰진 밴드패스(적색 ~660 + 청색 ~430 흡수) | 산소 발생 광합성, 태양 같은 가시광 플럭스 | speculative → artistic | Earth vegetation | 빛을 먹는 생명의 녹색 |
| deep red / maroon | 원적색 엽록소 f / 박테리오엽록소(창이 ~700–1000 nm 로 이동) | 적색/M 왜성 SED 아래의 광합성 | speculative → artistic | far-red cyanobacteria | 붉은 태양 빛에 맞춰진 잎 |
| orange / yellow | 카로티노이드(β-카로틴, 박테리오루베린) | 보조/광보호 색소 | speculative → artistic | autumn foliage, Dunaliella | 카로티노이드 주황의 지표 식물 |
| deep red | phycoerythrin(녹색 ~530–570 nm 흡수) | 홍조류 / 시아노박테리아, 깊은 물 | speculative → artistic | red algae | 깊은 녹색을 잡으려 붉어진 조류 |
| blue / blue-green | phycocyanin(주황-적색 ~610–660 nm 흡수) | 시아노박테리아, 표면 막 | speculative → artistic | cyanobacterial mats | 청색 색소를 띤 미생물 매트 |
| purple / magenta | retinal(bacteriorhodopsin) — 녹색 ~568 nm 흡수 | "Purple Earth" retinal 광영양 | speculative → artistic | hypothesis (DasSarma & Schwieterman) | retinal 색소 생물권, 보라색 |
| red→purple→blue | 안토시아닌 — pH 의존 액포 색소 | 식물 조직, 스트레스/저온 반응 | speculative → artistic | autumn / blue flowers | pH 로 가변하며 식물상을 칠하는 색소 |
| brown / black | 멜라닌 — 광대역 흡수체(선명하지 않음) | 광보호, 강한 UV 표면 | speculative → artistic | dark biological crusts | UV 를 막으며 표면을 어둡게 하는 색소 |

### Cloud (condensate + chromophore; cold → hot ladder)

| color | mechanism | conditions | persistence → lane | example | hook |
|---|---|---|---|---|---|
| white | 물얼음 구름(흡수 없음, 높은 산란) | T 가 H₂O 응결을 허용 | common → P3 | Earth | 밝은 물얼음 구름층 |
| white | 암모니아(NH₃) 얼음 구름 | 차가운 거대행성, NH₃ 응결(~150 K) | common → P3 | Jupiter/Saturn zones | 얼어붙은 암모니아 구름 상단 |
| bright white | 메테인/에테인 얼음 구름 | 매우 차가운 얼음 거대행성 대기 | common → P3 | Neptune bright clouds, Titan | 고층의 메테인 얼음 권운 |
| brown / tan | NH₄SH — 신선할 땐 무색, 방사분해/UV 산물이 청색을 흡수 | 거대행성 띠 화학, 따뜻한 층 | common → P3 | Jupiter belts | 황화암모늄의 갈색 띠 |
| yellowish-white | 황산(H₂SO₄) 에어로졸 방울 | S 화산활동, 뜨겁고 두꺼운 대기 | common → P3 | Venus | 황산 구름 베일 |
| red (uncertain) | 미상의 chromophore — 방사분해된 NH₄SH / S-P 광화학 / Carlson NH₃+아세틸렌 | 상승류가 S/P 기체를 UV 가 비추는 구름 상단으로 올림 | uncertain → P3 low-conf | Jupiter Great Red Spot | 폭풍 상단의 광화학 적색 |
| grey / muddy (hot) | 규산염 + 철 + 강옥 광물 구름 | 뜨거움(L 왜성 / 뜨거운 목성형), ~1300–2000 K | measured (BDs) → P3 | L dwarfs, hot Jupiters | 녹은 암석과 철 먼지의 구름 |
| salt-and-sulfide haze | 저온 광물 구름 — KCl, ZnS, Na₂S, MnS, Cr | ~600–1400 K(T 왜성 / 따뜻한 거대행성) | measured → P3 | T dwarfs | 따뜻한 하늘의 소금-황화물 안개 |
| very red (NIR) | 두꺼운 광물 먼지 구름이 젊은/먼지 많은 대기를 붉게 만듦 | 먼지 많은 L 왜성 / 저중력 거대행성 | measured → P3 | HR 8799 b/c/d, ULAS J2227 | 먼지가 너무 두꺼워 세계 전체가 붉게 빛남 |

---

## Observational vetoes (step 1 of the gate)

실제 측정값이 제안을 직접 반박하면 그 제안은 **거부(REJECT)** 됩니다. NearStars 행성 대부분은 RV 전용이라 이 중 *어느 것에도* 걸리지 않습니다(→ 제약 없음 → 자유). veto 는 관련 측정값이 실제로 존재할 때만 작동합니다.

| proposal | vetoed by | example bodies |
|---|---|---|
| thick atmosphere | 맨바위 낮면을 보여 주는 열 위상곡선 / 방출 스펙트럼(열 재분배 없음; 밝기 T ≈ 항성 직하점) | TRAPPIST-1 b (Greene 2023), TRAPPIST-1 c (Zieba 2023), LHS 3844 b (Kreidberg 2019) |
| atmosphere of composition X | 조성 Y 의 대기가 *측정됨*(색은 실제 종에 맞아야 함) | 55 Cnc e — JWST CO₂/CO secondary atmosphere (Hu 2024) |
| solid/rocky surface tint, lava surface | 평균 밀도(질량+반지름) → mini-Neptune / 가스 외피 → 보이는 표면 없음 | H/He 외피를 가진 모든 sub-Neptune |
| reflected-light color | *측정된* 기하 알베도 / 반사 색 | HD 189733 b deep blue (Evans 2013); TrES-2 b near-black (low albedo) |
| liquid-water ocean | T_eq 가 물의 임계점을 한참 넘거나 온실효과 없이 빙점을 한참 밑돎 → 안정된 액체 물 없음 | 뜨겁거나 차가운 극단 |

veto 에 걸리면 반박되지 않는 가장 가까운 대안을 제시합니다(예: TRAPPIST-1 b 의 두꺼운 대기가 veto 됨 → 어두운 현무암질 맨바위 표면, 얇은/없는 하늘).

---

## Worked examples

**Tau Ceti e — 선명한 녹색 대기(PHM 컨셉).** Tau Ceti e 는 RV 전용(비통과)이라 반지름·대기·알베도가 측정된 적이 없습니다 → **제약 없음**, veto 불가능. 녹색 *대기*(기체 색조)에는 깔끔한 메커니즘이 없습니다 — Cl₂/ClO₂ 는 황록색까지밖에 못 갑니다 → lane 2, 약한 훅. 하지만 녹색 *세계*는 쉽습니다. 녹색을 **표면**(Cr³⁺ 에메랄드 / 사문석 / 감람석 — 무기, 생명 불필요)이나 **식생**(엽록소, lane 2 추정성)으로 보내고, 선택적으로 가장자리에 **O I 557.7 nm 녹색 대기광**을 더하세요. **판정: 녹색 유지** — 녹색 가스 색조가 아니라 녹색 표면(근거가 가장 탄탄함) ± 녹색 대기광으로. 인게임: *"Tau Ceti e 는 희미한 산소 녹색 대기광 아래 크롬과 사문석의 녹색 지각을 두르고 있다."* (엔트리를 확정하기 전에 광물 색 주장은 출처로 값 검증하세요.)

**선명한 녹색, 생명 없음 — 무기 경로.** 생물을 끌어들이지 않고 채도 높은 녹색을 원할 때. Cr³⁺ 광물(uvarovite/크롬 투휘석/fuchsite)이 가장 순수한 무기 에메랄드; Cu²⁺ 공작석(malachite)이 강한 녹색; 사문석/감람석이 더 넓은 올리브 지각을 냄. 모두 lane 1–2, 비통과 세계에서는 veto 없음.

**"TRAPPIST-1 b 의 두꺼운 대기" — 거부.** JWST 방출(Greene 2023)이 맨바위 낮면을 보여 줍니다 → 두꺼운 대기는 매력과 무관하게 **1단계에서 veto**. 제시한 대안은 어두운 현무암질/초고철질 맨바위 표면 색조, 하늘 없음.

---

## Notes on use
- 이 카탈로그는 교과서적이고 확립된 색 화학을 사용합니다. **rare / artistic / speculative / uncertain** 으로 표시된 행은 신뢰도가 낮으며, 실제 천체의 Phase 3 문서나 cfg 에 적어 넣을 때는 **사용 시점에 출처를 핀으로 고정**해야 합니다(값 검증 규율).
- 가장 순수하고 채도 높은 색을 원하면 기체 색조나 일반 산란보다 **방출** 메커니즘(대기광/오로라)이나 **전이금속/생물** chromophore 를 택하세요 — 광대역 산란은 옅어지는 경향이 있습니다.
- 반사율 대 별빛 컨벤션은 `disk-color.md` 를 따릅니다 — 물질 고유 색을 두고, 렌더러/항성이 조명을 입히는 방식입니다. 디스크 도메인은 이 표가 아니라 Mie 엔진(`scripts/phase3/disk_color_mie.py`)을 사용하세요.
- 오로라 *방출선* 색(정확한 파장)은 [`element-plasma-colors.md`](./element-plasma-colors.md) 에 카탈로그화되어 있습니다. firefly 의 `composition-color.md` 는 재진입 플라즈마 bulk-gas 색을 다룹니다.
- 합성 흐름에 결선하는 작업(SKILL.md 의 정식 색 게이트 + `## Color` 제안 섹션)은 idea-#2 아키텍처 결정(Phase 3 확장 vs Phase 4)이 정해질 때까지 보류입니다. 이 문서는 두 방향 모두가 쓸 수 있는 아키텍처 중립적 토대입니다.
