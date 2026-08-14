<!-- 쌍극 자기장 세기+항성풍에서 자기권 크기·모양과 방사선대 강도(다요인)를 도출해 Kerbalism 지오메트리로 매핑하는 방법(논문 근거) -->
# 행성 자기권 지오메트리 근거화: standoff·방사선대·Kerbalism 매핑

바디의 **쌍극 자기장 세기**([암석형](rocky-planet-dynamo-methodology.md) 또는
[거대행성](planetary-dynamo-scaling.md) 다이나모 레시피 산출)를 **자기권의 모양과
크기** — 자기권계면 standoff, 방사선대 범위, 벨트 강도 — 로 바꾸고, 이를 Kerbalism이
실제로 소비하는 필드로 매핑하는 방법 문서입니다. Kerbalism은 Tesla 단위 물리 자기장을
들고 있지 않습니다. 방사선 환경을 *지오메트리*(`RadiationModel` 벨트/pause 셸) +
*강도*(`radiation_inner/outer/pause/surface`, rad/h) + 쌍극축 방향
(`geomagnetic_pole_lat/lon`)으로 모델링합니다. 이 문서가 그것들을 물리에서 도출하는
레시피입니다.

**핵심 규율(이 문서가 존재하는 이유).** 자기장 세기는 *그릇*을 정하지 *내용물*을 정하지
않습니다. standoff와 벨트 반경은 자기장으로 스케일되지만, **벨트 강도는 별개 요인** —
입자 공급원과 손실의 균형, 그리고 Kennel–Petschek 안정포획 한계로 상한 — 의 지배를
받으며 자기장 세기만의 함수가 *아닙니다*. 벨트 강도를 B에서 읽어내려는 것이 이 문서가
막는 전형적 실수입니다.

## Part A — 자기장에서 지오메트리(모양 + 크기)

### 자기권계면 standoff (Chapman–Ferraro 균형)

주간측 자기권계면은 행성 자기압이 주변 램압과 평형을 이루는 곳입니다(Chapman & Ferraro
1931, [`1931TeMAE..36...77C`](https://ui.adsabs.harvard.edu/abs/1931TeMAE..36...77C); 경험식 Shue et al. 1997/1998, [`1997JGR...102.9497S`](https://ui.adsabs.harvard.edu/abs/1997JGR...102.9497S) /
[`1998JGR...10317691S`](https://ui.adsabs.harvard.edu/abs/1998JGR...10317691S)). 쌍극장이 `B(r) = B_eq·(R_p/r)³`로 감소하고 Chapman–Ferraro
표면전류가 경계에서 場을 약 2배로 만든다면(계수 `f ≈ 2`).

    R_mp / R_p  =  [ f² · B_eq² / (2 μ₀ · P_ram) ]^(1/6)      (μ₀ = 4π×10⁻⁷)

여기서 `P_ram = ρ v²`는 바디를 스쳐 흐르는 것의 램압입니다 — 행성이면 **항성풍**,
임베디드 위성이면 **모행성의 공회전 자기권 플라스마**(regime 참조). `^(1/6)` 멱은
입력 오차에 매우 강건합니다. B나 P가 8배 틀려도 R_mp는 2배만 움직입니다.

**적도(sub-solar) 자기장**만 개입합니다 — 자기권계면 코는 자기적도에 있습니다. 극
자기장은 여기 등장하지 않습니다. 순수 쌍극이면 그냥 `2·B_eq`라 독립적 지오메트리 정보가
없습니다(다극장에서만 정보값을 가짐 — regime 참조).

### 벨트 범위

포획 입자는 닫힌 쌍극 자기력선(L-shell)을 타므로, 벨트는 바깥으로 **자기권계면에
갇히고**(`R_outer ≲ 0.6–0.8 R_mp`) 안으로는 대기/표면(`R_inner ≈ 1.1–2 R_p`)에
갇힙니다. 강한 場 → 큰 standoff → 벨트가 더 멀리 놓일 여지. 자기장 세기가 벨트를 직접
크기 정하는 유일한 지점입니다.

### 유도 자기권 — 다이나모가 없는 갈래

위의 모든 이야기는 고유 쌍극자를 전제합니다. **다이나모는 없지만 대기가 있는** 바디도 자기권과
비슷한 구조를 갖습니다. 햇빛이 상층 대기를 광이온화하고, 전도성 전리층이 항성풍이 끌고 온 자기장을
밀어내며, 그때 생기는 경계가 **이오노포즈 / 유도 자기권 경계**입니다(Bertucci 2011,
[`2011SSRv..162..113B`](https://ui.adsabs.harvard.edu/abs/2011SSRv..162..113B)의 화성·금성·타이탄 리뷰. Luhmann 1991,
[`1991SSRv...55..201L`](https://ui.adsabs.harvard.edu/abs/1991SSRv...55..201L)). 가끔 생기는 것이 아니라 거의 상시 존재합니다(Zhang 2009,
[`2009GeoRL..3620203Z`](https://ui.adsabs.harvard.edu/abs/2009GeoRL..3620203Z)).

**Standoff.** 여기서의 균형은 자기압 대 램압이 아니라 전리층의 *열압* 대 충격을 거친 항성풍
압력이므로, Part A의 `^(1/6)` 법칙이 적용되지 않습니다. 대신 실측 스케일을 쓰십시오. 금성의 평균
이오노포즈는 **직하점 위 330 km, 황혼 명암경계선 700 km, 새벽 쪽 1000 km**이고 풍압에 따라
부풀었다 줄었다 합니다(Brace 1980, [`1980JGR....85.7663B`](https://ui.adsabs.harvard.edu/abs/1980JGR....85.7663B)). 즉 **직하 1.05 R_V,
명암경계선 1.12–1.17 R_V**입니다. 지구~금성급 대기라면 `1.05–1.2 R_p`를 채택하고 어느 쪽 끝을
골랐는지 밝히십시오. 여기서 끌어낼 만한 자기장 파라미터는 없습니다.

**어느 갈래인지 판정.** "다이나모가 있느냐"로 나뉘지 않습니다. *약한* 쌍극자는 없느니만 못할 수
있습니다. 화성 크기 행성의 하이브리드 시뮬레이션에서, 자기장을 키우면 쌍극자의 standoff가 유도
경계를 넘어설 때까지 이온 유실이 오히려 **늘고**, 그 지점을 넘어서야 비로소 차폐가 시작됩니다
(Egan 2019, [`2019MNRAS.488.2108E`](https://ui.adsabs.harvard.edu/abs/2019MNRAS.488.2108E)). 따라서 교차 판정은 `B_eq > 0`이 아니라
`R_mp(B_eq) > r_ionopause`입니다. 그 아래면 유도 갈래로 다루십시오.

**근접 궤도 주의.** IMF가 거의 방사 방향이 되면 유도 자기권이 통째로 사라질 수 있고(Zhang 2009),
근접 궤도의 극단적 풍압에서도 같은 일이 예상됩니다. 0.1 AU 안쪽의 조석고정 행성이라면 경계가 상시
존재한다고 가정하지 말고 이 단서를 함께 적으십시오.

**단일 α Shue로는 표현할 수 없지만, 2-α 형태면 됩니다.** 기존 기계를 그대로 쓰고 싶어지므로 짚고
갑니다. Shue 계열은 `r(θ) = r0 (2/(1+cos θ))^α`라 **α 하나**가 주간면 벌어짐과 꼬리를 동시에
지배합니다. 유도 자기권은 그 둘이 분리돼 있습니다. 노즈→명암경계선 벌어짐은 *작고*
(금성 1.14/1.055 = 1.08) 꼬리는 *깁니다*(5~11 R_V). 꼬리를 만드는 것이 주간면의 벌어짐이 아니라
끌려온 자기력선의 드레이핑과 질량적재이기 때문입니다. 명암경계선에 맞춰 α를 잡으면 0.113이고,
그 값으로는 11 R_V에 θ = 179.9964°에서야 닿습니다. 사실상 구이고 마지막 각도에서 급히 닫힙니다.
반대로 꼬리에 맞추면 주간면이 부풀어 오릅니다.

해법은 지수를 각도의 함수로 두는 것입니다. 계열은 그대로 두고 손잡이 하나만 늘립니다
(**우리 확장이고 발표된 모델이 아닙니다**).

    r(θ) = r0 · [ (1+ε) / (ε + cos²(θ/2)) ]^α(θ)
    α(θ) = α_day                                     θ ≤ 90°
         = α_day + (α_night − α_day)·u²(3−2u),       u = (θ−90°)/90°
    ε    = 1 / ( (L/r0)^(1/α_night) − 1 )

smoothstep 덕분에 α가 명암경계선에서 값과 기울기 모두 연속이라 두 영역이 만나는 자리가 매끄럽고,
`ε`은 여전히 꼬리를 `L`에서 닫습니다. 이제 제약이 서로 다른 파라미터에 얹힙니다. **`r0`와
`α_day`는 실측 노즈·명암경계선이, `L`은 관측된 꼬리 길이가 고정하고, `α_night`이 그 사이에서
꼬리가 벌어지는 정도를 정합니다.** **`α_night` 고르기, 그리고 주의할 인공물.** `ε`이 꼬리를 유한한 `L`에서 닫기 때문에 폭은 늘 커졌다가
목이 잘립니다. 조절할 수 있는 것은 불룩함의 크기뿐이고, `α_night`이 크면 꼬리가 눈에 띄는 렌즈가
됩니다. 폭 프로파일을 재면 이렇습니다.

| `α_night` | 최대 꼬리 폭(금성) | 명암경계선 대비 | 위치 |
|---|---|---|---|
| 0.30 | 1.16 R_V | 1.01배 | 명암경계선 바로 뒤 |
| **0.34** | **1.16 R_V** | **1.02배** | x ≈ 0.5 R_V |
| 0.40 | 1.26 R_V | 1.10배 | x ≈ 2.6 R_V |
| 0.50 | 1.56 R_V | 1.37배 | x ≈ 4.4 R_V |

채택 기준은 **최대 꼬리 폭이 명암경계선 폭의 몇 % 안에 머무는 가장 큰 `α_night`**입니다. 그래야
꼬리가 불룩한 렌즈가 아니라 거의 원통형 항적이 완만히 닫히는 모양으로 읽힙니다. 금성·화성 모두
**0.34**이고(화성은 0.34에서 1.04배, 0.5에서 1.22배), 프로파일을 재기 전에 오너가 눈으로 고른 값과
같습니다.

정직하게 적어 둡니다. `r0`·`α_day`·`L`은 측정에서 오지만 `α_night`은 아닙니다. 위 기준으로 정한
형상 손잡이일 뿐이고, Pioneer Venus가 보고한 벌어짐(Saunders 1986,
[`1986JGR....91.5589S`](https://ui.adsabs.harvard.edu/abs/1986JGR....91.5589S))도 정성 서술입니다. 꼬리 반경 대 거리 프로파일이 생기면 제대로
고정하십시오. 단조롭게 벌어지는 꼬리를 원한다면 유한 닫힘 자체를 버려야 하는데, 엔진은 유계
부피가 필요합니다.

**Kerbalism 매핑.** 엔진에 이미 이 갈래가 있습니다. `ionosphere` 모델은 **pause만 있는** 껍질로,
`pause_radius` 1.1 R에 `pause_extension` 0.2(긴 유도 꼬리)이며 벨트 필드가 아예 없고
`radiation_pause` ≈ −0.005를 답니다. 쌍극 자기권계면보다 약한 값인데, 유도 경계가 GCR을 훨씬 덜
가리므로 옳습니다. 금성과 타이탄이 이 모델로 배포됩니다. NearStars 규칙은 이렇습니다.

- **다이나모 없음 + 대기 있음** → 이오노포즈 추정값에 `ionosphere`형 pause, 벨트 없음, 작은 음수
  `radiation_pause`
- **다이나모 없음 + 무대기** → `RadiationModel` 자체를 두지 않음. 표면 선량은 직접 풍/GCR
  플럭스이고 그 사슬은 `surface-radiation-dose-methodology.md`
- **약한 다이나모** → 벨트가 있다고 가정하기 전에 위의 교차 판정을 먼저 돌릴 것

모델별 cfg 값과 그것을 쓰는 바디는
[`solar-system-radiation-belts.md`](solar-system-radiation-belts.md)에 표로 있습니다.

## Part B — 벨트 강도는 다요인 (자기장 세기 아님)

벨트 강도는 **공급원 − 손실 균형, 場/플라스마 상한으로 캡**됩니다.

1. **공급원**이 바닥을 정합니다. 항성풍 포획, **CRAND**(우주선 알베도 중성자 붕괴,
   내부벨트 양성자원, Lenchek 1961 [`1961JGR....66.4027L`](https://ui.adsabs.harvard.edu/abs/1961JGR....66.4027L)), 안쪽으로의 방사확산(Schulz &
   Lanzerotti 1974 [`1974pdrb.book.....S`](https://ui.adsabs.harvard.edu/abs/1974pdrb.book.....S)), 그리고 **내부 플라스마원** — 화산 위성 하나가
   전부를 지배할 수 있습니다(Io가 목성 벨트에 ~1 ton/s 주입, Bagenal 1994 Io torus
   [`1994JGR....9911043B`](https://ui.adsabs.harvard.edu/abs/1994JGR....9911043B), Divine & Garrett 1983 목성 모델 [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D)).
2. **Kennel–Petschek 상한**이 캡합니다. *최대 안정포획 플럭스*가 존재해, 그 위에서는
   입자 자신의 whistler-mode 파동이 성장해 loss cone으로 산란시킵니다(Kennel & Petschek
   1966, [`1966JGR....71....1K`](https://ui.adsabs.harvard.edu/abs/1966JGR....71....1K), 2600+ 인용). 이 한계는 場과 냉플라스마 밀도에 의존하지만
   **공급원 세기와 무관**합니다 — 그래서 강공급원 자기권(지구·목성)은 K–P 천장에서
   *포화*하고, 공급을 더 늘려도 강도가 오르지 않습니다.
3. **손실**이 끌어내립니다. 파동–입자 산란(chorus/hiss/EMIC, Thorne 2010
   [`2010GeoRL..3722107T`](https://ui.adsabs.harvard.edu/abs/2010GeoRL..3722107T), 리뷰 Ripoll 2020 [`2020JGRA..12526735R`](https://ui.adsabs.harvard.edu/abs/2020JGRA..12526735R)), Coulomb/대기 손실,
   그리고 **위성·고리에 의한 흡수** — 토성 벨트는 고리/위성에 쓸려나갑니다(Cooper 1983,
   [`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C)).

도출 상의 귀결: **벨트 강도를 B_eq에서 읽을 수 없습니다.** 같은 場을 가진 두 바디도
공급원(화산 위성 유무)과 손실(고리/위성 sweeping)에 따라 벨트 선량이 자릿수로 다를 수
있습니다. 場은 벨트가 *어디서 포획되는가*를 알려주고, 공급원/손실/K–P 균형이 *얼마나
강한가*를 정합니다. 따라서 벨트 강도는 공식 출력이 아니라 **공급원·손실을 명시한 regime
판정**으로 남습니다.

### 정확한 K–P 천장(계산 가능)과 그것이 정하는 것 — 그리고 정하지 못하는 것

K–P 한계는 이제 어떤 바디에 대해서든 **직접 계산할 수 있습니다**.
[`scripts/refs/kp_limit.py`](../../../scripts/refs/kp_limit.py)는 Mauk & Fox가 직접 발표한
구현을 검증해 옮긴 Python 포트입니다(그들의 공개 Zenodo 소프트웨어
[`10.5281/zenodo.4782323`](https://zenodo.org/records/4782323), bibcode
[`2021zndo...4782323M`](https://ui.adsabs.harvard.edu/abs/2021zndo...4782323M) — 논문 본체인
[`2010JGRA..11512220M`](https://ui.adsabs.harvard.edu/abs/2010JGRA..11512220M)은
유료이고 preprint가 없음). 계산 사슬은 이렇습니다. 유연한 미분 스펙트럼
`j(E) = C·E·(kT(γ₁+1)+E)^(−γ₁−1)/(1+(E/E₀)^γ₂)`에 pitch 계수 sin^2s α를 곱해 →
상대론적 사이클로트론 공명(Summers, Tang & Thorne 2009
[`2009JGRA..11410210S`](https://ui.adsabs.harvard.edu/abs/2009JGRA..11410210S),
eqs A4–A8) → A1/A2 적분에서 나오는 whistler 성장률 → 한계 안정성
`CmCk = L·R_p·w_i/(3·v_g)`(파동 이득 3; Mourenas 2024
[`2024JGRA..12932193M`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932193M)이
독립적으로 확인). 제한된 스펙트럼은 ~E⁻¹입니다(상대론적 계수가 비상대론의 2배; Summers
2014 [`2014JGRA..119.6313S`](https://ui.adsabs.harvard.edu/abs/2014JGRA..119.6313S)).


**검증 (자화 5행성 전부).** 원 논문 3편이 로컬 캐시에 확보되면서(AGU 24개월
무료 아카이브, 오너가 받은 PDF를 `docs/phase3/_papers/`에 보관) 포트의 정규화
항은 *출판된* Summers 2009 A2/A3 프리팩터 그대로가 됐고, 노트북의 지구 L=5
중간값들은 ~10⁻⁶ 수준으로 재현됩니다(w_i 0.658455, CmCk 피크 0.607879 @
102.9 keV — 인쇄 자릿수까지 일치). 이어서 Mauk & Fox의 행성별 분석(Table 1
스펙트럼 + 그림별 B/N/D)을 그들의 그림이 말하는 수준에서 재현합니다.

| 케이스 (그들의 그림) | 그들의 판정 | 우리 CmCk 피크 |
|---|---|---|
| 지구 L=4 (Fig 7) | 상한보다 한참 아래 | 0.28 ✓ |
| 지구 L=5 (Fig 5) | 0.60, 상한 근접 | 0.6079 (정확) |
| 지구 L=6 (Fig 7) | 상한 근접 | 1.46 ✓ |
| 천왕성 L=4.73 (Fig 8, N=5) | 도달/초과 | 1.11 ✓ |
| 목성 L=8.3 (Fig 9, N=200, D=3) | 상한 근접 | 0.68 ✓ |
| 해왕성 L=7.4 (Fig 11, N=0.3) | 1 MeV서 ~30배 아래 | 피크 0.91, 1 MeV 27.8배 아래 ✓ |

이 케이스들은 모듈의 `__main__` 자가검증으로 실행됩니다.

이 정밀 기계가 확립하는 구조적 사실 2가지.

1. **천장의 지배 변수는 We/wpe ∝ B/√n_cold**입니다(스펙트럼·pitch 지수도 함께) — B
   단독도 B²도 *아닙니다*. 국소 場이 강하고 냉플라스마가 희박한 곳(작은 L의 깊은 내대)
   에서는 공명 에너지가 수십 MeV로 치솟아 ~MeV 천장이 사실상 구속력을 잃습니다 — 그런
   벨트는 **K–P가 아니라 공급원/손실이 정합니다**. 워크드 체크(Alpha Centauri A b (Polyphemus) 내대 피크,
   L = 2.07, B_local ≈ 지구 L=5 場의 129배): 토러스 밀도 10²–5×10³ cm⁻³ 전 구간에서
   계산된 1 MeV 천장이 지구의 ≥ 5×10²–10¹⁶배 — 구속 조건이 된 적이 없습니다.
2. **K–P 캡은 행성 간 선량 대비를 정하지 않습니다.** Mauk & Fox는 지구·목성·천왕성이
   모두 ~0.1–1 MeV 부근에서 비슷한 미분 캡에 *걸려 있는데도* 선량이 자릿수로 다름을
   발견합니다. 선량은 스펙트럼 적분·차폐 수송을 거친 양이라, 차폐 투과 컷오프 위의
   **꼬리 경도**(1 MeV 전자의 CSDA 사거리 ≈ 2.0 mm Al)와 벨트 크기가 지배합니다.
   커뮤니티 표준 수송은 SHIELDOSE-2입니다(Seltzer
   [`1979ITNS...26.4896S`](https://ui.adsabs.harvard.edu/abs/1979ITNS...26.4896S),
   [`1992STIN...9315580S`](https://ui.adsabs.harvard.edu/abs/1992STIN...9315580S)).
   교과서 자유장 계수는 1 MeV에서 e⁻ cm⁻²당 ≈ 2.3×10⁻⁸ rad(Si), ~2.5 mm Al 뒤에서
   ~10배 감쇠.

**실용 rad/h 레시피(정정된 상태).** 공급원 포화된 목성-아키텍처 계에서는 감사된 두 포화
*선량 앵커* — 지구 31 µT → 10.4 rad/h, 목성 428 µT → ~1500 rad/h — 사이를 보간합니다.
`dose ≈ 10.4 × (B_eq/31 µT)^1.9`. 이것은 경도 + 벨트-크기 효과를 뭉뚱그린 **경험적
선량-앵커 보간**이지 K–P 스케일링이 *아닙니다*(이전 개정판이 그렇게 잘못 라벨한 것을
철회). 외/내 비는 토러스-구동(목성)이 ~0.1, 항성풍-공급(지구)이 ~0.2. 그다음 두 하드
체크를 적용합니다. (a) 고른 강도는 그 벨트의 (B, L, n_cold)에서 `kp_limit.py`로 계산한
K–P 천장 아래에 있어야 하고(A b 300 rad/h ≈ 지구 29배 ≪ 가장 조밀한 토러스에서도
천장 ≥ 지구 5×10²배 — 통과), (b) 공급원 기아·gap 기아 벨트는 이 모든 것 *아래*에 있으며
평범한 regime 판정으로 남습니다(Alpha Centauri A b III (Pandora) 지구 0.4배). 신뢰도는 여전히 낮습니다 — 보간
지수가 2-앵커 적합이고 픽션 토러스의 n_cold는 명시된 가정이므로 — 그러나 이제 모든 요인이
기계론적이고, 핀되고, 경계지어졌습니다.

**작업 사례 — Proxima d (16 G SPI 극자기장, 항성풍/플레어 공급, 토러스 없음).**
B_eq = 800 µT → 앵커 보간으로 내대 ~5×10³ rad/h, 외대 ~1×10³(wind-fed 0.2 비).
목성 앵커의 1.9배 밖 외삽이라 신뢰도는 낮고, 장 범위 3–280 G를 넣으면
2×10²–10⁶ rad/h까지 벌어집니다. `kp_limit.py`를 L = 4에서 돌리면(B_local
1.25×10⁴ nT; n_cold 1–100 cm⁻³ — 무대기 행성은 전리층발 플라스마권을 못 먹임)
모든 밀도에서 CmCk ≪ 1: K–P 상한은 전혀 구속하지 않고 벨트는 source/loss가
정하는, 강한 장 + 작은 L 사례들과 같은 구조적 regime입니다. 시각화 항목:
`render_belts_bodies.py proxima_d_phys`.

## Part C — Kerbalism 매핑

| 물리량 | Kerbalism 필드 | 도출 |
|---|---|---|
| 자기권계면 standoff | `pause_radius` (+ `has_pause`) | **`pause_radius = R_mp × pause_compression`** — 주간측 x는 구 검사 전에 압축되므로 sub-solar 코는 `pause_radius/pause_compression`에 놓임(옆구리 = `pause_radius`). Part A의 R_mp가 *코* |
| 자기권계면 차폐 | `radiation_pause` (작은 음수) | 차폐는 `pause_radius`에 pause가 *있다는 것*에서 나옴. 값 자체는 작고 스톡 균일(~−0.01)이며 standoff에 비례하지 않음 |
| 벨트 범위 | `inner_dist`/`inner_radius`, `outer_dist`/`outer_radius` (바디 반경 단위) | Part A 경계 |
| 벨트 강도(rad/h) | `radiation_inner`/`radiation_outer` | Part B regime: 공급원 − 손실, K–P 캡 — **B가 아니라 명시된 공급원/손실에서** |
| 쌍극축 방향 | `geomagnetic_pole_lat`/`lon` | = `magnetic_dipole_tilt_deg` |
| 벨트 존재 게이트 | (벨트가 아예 있나) | `B_eq ≳ 0.1× 지구`. 이하면 안정 포획 없음 |

### RadiationModel 지오메트리 (Kerbalism 소스 근거)

Kerbalism은 각 field를 signed-distance 형상으로 모델링하며 길이는 전부 **바디 반경 단위**
입니다([Kerbalism 모딩 문서](https://kerbalism.readthedocs.io/en/latest/modders/radiation.html);
스톡 값은 `KerbalismConfig/System/Radiation.cfg`).

- **내대(inner)** = 토러스에서 border 토러스를 뺀 것. `inner_dist`(장반경) + `inner_radius`
  (단면 반경)를 `inner_border_dist/radius/deform_xy`로 도려냅니다(`border_dist ≈ 0`인 border는
  구 컷 — loss-cone D 모양). 전부 `deform_xy`로 눌린 좌표계입니다. 적도 범위 =
  `(dist ± radius)/√deform_xy`. (`*_border_start/end`는 일부 출하 cfg에 아직 남아 있지만 레거시
  입니다 — 현재 파서는 `border_dist/radius/deform_xy`만 읽습니다.)
- **외대(outer)** = 같은 구조. `outer_dist` + `outer_radius`에서 그 border를 뺍니다.
- **자기권계면(pause)** = 구 `pause_radius`, 별 방향 압축(`*_compression`)·꼬리 방향 신장(`*_extension`) 가능. `*_deform`/`*_quality`는 렌더용.
- 강도·축은 `RadiationBody`에: `radiation_inner/outer/pause`(rad/h, pause 음수), `geomagnetic_pole_lat/lon`.

**`inner`과 `outer`는 항상 `inner_dist < outer_dist`인 두 토러스**입니다 — 다만 이게 분리된
밴 앨런 두 벨트로 *보이는지*, 하나의 동심 구조로 보이는지는 단면반경 대 간격 비가 결정합니다.

| 스톡 모델 | inner `dist / radius` | outer `dist / radius` | `pause_radius` | `radiation_inner / outer / pause` | 외형 |
|---|---|---|---|---|---|
| **earth**(Kerbin) | 0.81 / 0.70 | 2.63 / 2.48 | 13.65 | 10.4 / 2.2 / −0.011 | 분리된 두 벨트 |
| **giant**(Jool) | 2.2 / 1.0 | 6.0 / 6.0 | 60 | 200 / 11 / −0.012 | outer 단면=반경이라 구멍이 닫혀 inner를 감싸는 **동심** 외형 |

즉 바디 클래스 선택은: **암석/지구형 → `earth` 스타일(뚜렷한 두 토러스, 분리 벨트),
자이언트 → `giant` 스타일(뚱뚱한 겹치는 토러스, 동심 외형).** 둘 다 `dist/radius` 비만 다른
inner+outer이며, NearStars에서 반복된 "동심이냐 분리냐"는 별개 메커니즘이 아니라 렌더 결과입니다.

이전 NearStars 초안을 정정하는 스톡 근거 2가지.
- `radiation_pause`는 **스톡에서 작고 바디에 거의 무관**(Kerbin −0.011, Jool −0.012) — standoff에
  비례하는 큰 차폐항이 아닙니다. (이전 A b III 초안의 −3.8은 Promised Worlds 팩 튜닝값 → ~−0.01 스톡 스케일로 재앵커.)
- 지구식 기울기 바디의 `geomagnetic_pole_lat ≈ 80`은 스톡 Kerbin(80.37)과 일치.

### Sol / RSS 앵커 (NearStars는 Sol 기반 — 스톡보다 이걸 우선)

NearStars는 Sol 실스케일이라 스톡 Kerbin/Jool보다 **ROKerbalism / RSS** 방사선 cfg가 더
정확한 앵커입니다(ROKerbalism `KerbalismConfig/System/Radiation.cfg` + KerbalismConfig
`Support/RSS.cfg`).

| 바디 | 지오메트리(R_body) | `radiation_inner / outer / pause` | 비고 |
|---|---|---|---|
| 태양 | heliopause, `pause_radius` 1000 | surface 46.5, cycle 11 yr | 선량원 + GCR 차폐 |
| 지구 | inner 0.81/0.70, outer 2.63/2.48, pause 15 | 10.4 / 2.2 / **−0.010**, pole 80.4 | **분리** 벨트 |
| 목성 | inner 6.0/1.0, outer 6.5/6.5, pause 60 | 300 / 50 / **−0.010**, pole −81 | **동심**(inner이 outer 셸 안쪽 가장자리에) |
| 토성 | outer 7/7만(**inner 없음**), pause 20 | — / 150 / **−0.011** | 내대 없음 — **고리가 쓸어냄**(Cooper 1983) |
| 천왕성 | offset 쌍극 | 75 / 4 / −0.010, pole 31, `geomagnetic_offset` 0.3 | 기울기/offset |
| 해왕성 | offset 쌍극 | 39 / 2.5 / −0.007, pole 43, `geomagnetic_offset` 0.55 | 강한 offset |

NearStars에 대해 이게 확정하는 3가지.
1. **`radiation_pause`가 모든 바디에서 ≈ −0.01**(지구/목성 −0.010, 토성 −0.011, 해왕성
   −0.007) — 작고 바디무관한 항이지 차폐 크기가 아님 확정. (A b III −0.01이 맞음.)
2. **가스자이언트 → 동심, 암석 → 분리**가 스톡뿐 아니라 실제 바디에서도 성립.
3. **고리 손실 vs 화산 공급원의 경쟁** — 토성은 고리 흡수(Part D 손실)가 이겨 내대가 도려져
   *outer만, inner 없음*으로 모델링됨. 목성은 Io 플라스마 공급원(Part D 공급)이 이겨 강렬한
   내대 유지. 고리 가진 자이언트는 둘 중 어느 쪽도 될 수 있음. **Polyphemus는 토성이 아니라
   목성을 따름**: 화산 내측 위성 Alpha Centauri A b I (Dante)(~820× Io)가 고리 sweeping을 압도하는 공급원 → *강화된*
   내대, 그리고 거주가능 위성 Pandora의 강한 고유장이 그걸 막음(설계의 핵심 드라마).
   `geomagnetic_offset`(천왕성 0.3, 해왕성 0.55)은 Proxima c 같은 빙거성의 offset/다극 쌍극 핸들.

### `radiation_*_gradient` — 껍질 안쪽의 선량 상승 기울기

벨트 껍질은 지오메트리일 뿐이고, 그 안에서 실제로 받는 선량은 이렇게 계산됩니다.

    dose = clamp( gradient · (−SDF) / radius , 0 , 1 ) · radiation_inner|outer

(`Radiation.cs`. `scripts/viz/render_belts.py:50`과 벨트 뷰어가 이 식을 원문 그대로 옮겼기
때문에 뷰어의 선량 표시를 미리보기로 신뢰할 수 있습니다.) `−SDF`는 껍질 표면에서 파고든
깊이이고 `radius`는 그 벨트 자신의 `*_radius`이므로, 선량은 **경계에서 0으로 시작해 다음
깊이에서 최대 강도에 도달하는 선형 램프**입니다.

    d* = *_radius / gradient          (바디 반경 단위, deform_xy로 눌린 좌표계 기준)

즉 단면 반경의 `1/gradient`만큼을 최대치까지 올라가는 데 씁니다. 배포된 값은 내대 **3.3**
(단면 반경의 30 %에서 평탄부 진입), 외대 **2.2**(45 %)이고, emitter와 뷰어는 이 둘을 같으면
생략하는 기본값으로 취급합니다. 그래서 cfg에 `radiation_inner_gradient` 줄이 적혀 있다면 항상
의도적인 이탈입니다.

**구하는 방법.** gradient는 벨트의 경계나 최대치가 아니라 반경방향 **프로파일의 모양**을
담는 유일한 필드라, Part B가 이미 필요로 하는 그 프로파일에서 나옵니다.

1. 자기적도를 따라간 반경방향 선량(또는 >MeV 플럭스) 프로파일을 Part B의 공급−손실 모형에서
   가져옵니다. 앵커 바디는 발표된 모형에서 바로 읽어도 됩니다(목성 벨트는 Divine & Garrett
   1983 [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D), 반경확산 프로파일은 Schulz & Lanzerotti 1974
   [`1974pdrb.book.....S`](https://ui.adsabs.harvard.edu/abs/1974pdrb.book.....S)).
2. 그 피크 위치에서 껍질 **자신의 SDF**를 적도면 기준으로 계산합니다. `d* = −SDF(r_peak)`.
   `|r_peak − r_edge|`로 손으로 재지 말고 수치로 구하십시오. border 컷과 `deform_xy`,
   `deform`이 모두 "가장 가까운 경계"를 바꿔놓기 때문이고, 실제로 지구 내대에서 깊이를
   결정하는 것은 토러스 벽이 아니라 손실원뿔 컷입니다. SDF로 구하면 눌린 좌표계 환산도
   따로 할 필요가 없습니다.
3. `d*`를 `d_max`로 클램프합니다. `d_max`는 **border 컷을 견디고 살아남은 가장 깊은 점**의
   깊이이고, 같은 방식으로 껍질 전체의 SDF를 훑어 구합니다. 컷이 토러스 핵심을 잘라내는 것이
   보통이라 실제 `d_max`는 `*_radius`의 0.5~0.65 수준이고, 근거상의 피크가 이미 껍질이
   차지하지 않는 자리에 떨어질 수 있습니다.
4. `gradient = *_radius / d*`. 따라서 실제 하한은 `≥ 1`이 아니라
   **`gradient ≥ *_radius / d_max`**입니다. 이 아래로 내려가면 벨트 어디에서도 명시한
   `radiation_*`에 도달하지 못하고, 벨트 전체가 `gradient · d_max / *_radius` 배로 조용히
   깎입니다.
5. **자기 프로파일이 없는 바디라면** 스톡 숫자를 쓰지 말고 같은 등급 아날로그의 *평탄부
   비율*을 물려받습니다. CRAND 양성자대는 지구 내대, 항성풍·확산이 먹이는 전자대는 지구
   외대, 토러스가 먹이는 벨트는 목성 내대입니다. 근거 없는 바디를 둥근 기본값이 아니라
   실측된 형상 위에 앉히는 것이 요점입니다.

핵심 원 근처에서야 최대가 되는 프로파일은 `gradient ≈ 1`(길고 완만한 상승)이고, 경계 바로
안쪽에서 포화하는 프로파일은 큰 gradient(단단한 경계)입니다.

**앵커 검산.** 태양계 피팅에 이 레시피를 돌리면 지구 **외대**가 2.15로 나옵니다. 배포값 2.2를
알려주지 않았는데 되찾아온 값이고, 이것이 검증입니다. 지구 **내대**는 배포값 3.3에 대해
2.09가 나오므로, 근거가 없는 쪽은 내대의 급한 기울기였습니다. L ≈ 1.5의 양성자 피크
(AE9/AP9는 Ginet 2013 [`2013SSRv..179..579G`](https://ui.adsabs.harvard.edu/abs/2013SSRv..179..579G), 슬롯은 Ripoll 2016
[`2016GeoRL..43.5616R`](https://ui.adsabs.harvard.edu/abs/2016GeoRL..43.5616R))가 손실원뿔 컷에서 0.23 R_E가 아니라 0.37 R_E
아래에 있습니다. 목성 내대(피크 1.5–2 R_J, Divine & Garrett 1983)는 2.24입니다. 천왕성이
바로 하한 규칙이 필요한 사례입니다. 전자 프로파일이 위성이 쓸어낸 극소 사이의 넓은 최대
(Cheng 1987, [`1987JGR....9215315C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215315C))라 피크가 껍질 핵심으로 읽히는데, 그 핵심은 컷으로
잘려나가 없으므로 값이 하한인 내대 **1.57**, 외대 **1.85**로 붙습니다. 문자 그대로 핵심을
피크로 보고 `gradient` 1.0을 넣었다면 벨트가 어디서도 포화하지 못하고 명시 강도의 0.64배로
돌아갔을 것입니다. 바디별 피크 위치와 출처는
[`solar-system-radiation-belts.md`](solar-system-radiation-belts.md)에 표로 있습니다.

미리 알아둘 결과가 하나 있습니다. 램프가 이렇게 길면 **완전히 포화한 심부가 얇습니다.**
자오면 단면에서 재면 지구 외대가 껍질의 9 %, 내대는 1.5 %뿐입니다(스톡 3.3에서는 23 %).
좁은 실측 피크의 정직한 반영이고 계산 오류가 아니지만, 명시한 `radiation_inner`는 벨트의
심장 근처에서만 닿는 값이라는 뜻이기도 합니다. 위성들이 받는 선량 사다리는 표제 숫자가 아니라
SDF에서 읽어야 합니다.

**실제로 발목을 잡는 결합 두 가지.**

- **`gradient` ↔ `*_radius`.** 둘은 `radius/gradient` 비로만 등장하므로, 단면 반경을 다시
  피팅하면 램프 깊이도 조용히 따라 움직입니다. `fit_belts.py`를 다시 돌렸다면 gradient도
  다시 구해야 합니다.
- **`gradient < 1`이면 적어놓은 강도에 끝내 도달하지 못합니다.** clamp가 1에서 잘리고 껍질의
  가장 깊은 점도 `−SDF = radius`까지밖에 못 가므로, 실현되는 최대 선량은
  `gradient · radiation_*`입니다. 완만한 프로파일 때문에 `gradient < 1`을 택한다면 강도를 그
  값으로 나눠 넣어야 최대 선량이 정직해집니다. 그러지 않으면 보드에 적힌 rad/h가 게임이 적용하는
  값과 다릅니다. (Proxima c 내대의 `gradient 1.9`는 안전 구간이고, 현재 NearStars에 1 미만은
  없습니다.)

A b 내대 예시. 설계상 피크가 A b II의 L-셸(2.07 R_p)에 있고 SDF로 재면 경계에서 0.70 R_p
아래이므로, `inner_radius` 1.159와 함께 `gradient` **1.65**가 나옵니다. 보드가 아직 들고 있는
기본값 3.3보다 훨씬 완만하고, 300 rad/h 전량이 실제로 그 위성이 도는 자리까지 나옵니다.

### 나머지 값들 — 무엇이 정하고, 무엇을 끌고 가는가

도출 순서가 중요합니다. `R_mp` 아래의 모든 값이 자기장이나 항성풍이 바뀌면 함께 바뀌므로,
단일 필드를 손보는 대신 사슬을 위에서 아래로 다시 돌리십시오.

    B_eq + P_ram  →  R_mp (Part A)  →  pause 필드
                                   →  벨트 L-셸 경계  →  fit_belts.py  →  벨트 지오메트리
    공급 − 손실 (Part B) + K–P 천장  →  radiation_inner/outer
    반경방향 프로파일 모양           →  radiation_*_gradient
    조화 성분 / 기울기 / offset      →  deform, pole_lat/lon, geomagnetic_offset

| 필드 | 무엇이 정하나 | 도출 | 무엇과 묶이나 |
|---|---|---|---|
| `has_pause` | 애초에 가두는지 | `B_eq ≳ 0.1×` 지구 (regime 5는 `false`) | 이게 없으면 벨트도 없음 |
| `pause_radius` | Part A 노즈 | `R_mp × pause_compression`. 압축은 구 판정 *전에* x에 적용됨 | `pause_compression`. 둘은 함께 다시 구할 것 |
| `pause_compression` | 주야면 비대칭 | 측면/노즈 비. Shue 등가로 `α = log₂(comp)`이라 ROK 지구 1.5 ⇒ α 0.585 | `pause_radius`, 그리고 아래 Shue `α` |
| `pause_extension` | 꼬리를 닫는 길이 | `L = pause_radius / extension`. `L`은 lobe 자기장이 GCR에 무의미해지는 거리로(지구 ≈ 200 R_E) | 꼬리 길이만. 노즈는 무관 |
| `pause_height_scale` | pause의 극방향 편평 | 극 standoff 대 적도 standoff 비(1.0=구, 자이언트 ~1.1) | 독립 |
| `radiation_pause` | GCR 차폐의 유무 | standoff에 비례하지 **않음**. 스톡에서 ~−0.01로 일정 | 없음(위 정정 참조) |
| `inner_dist` / `outer_dist` | 벨트 핵심의 L-셸 | 드리프트 셸 `r = L cos²λ`의 `L_core`, `fit_belts.py` 피팅 | `*_radius`·`*_deform_xy`(한 번에 같이 피팅) |
| `inner_radius` / `outer_radius` | 껍질 두께 | L-셸 띠의 반폭, 같은 피팅 | `gradient`(위의 비) |
| `*_deform_xy` | 드리프트 셸의 위도방향 눌림 | `cos²λ` 닫힘에서. 적도 범위 = `(dist ± radius)/√deform_xy` | 보고하는 범위값. 프로파일과 비교 전 환산 |
| `*_border_dist` / `*_border_radius` / `*_border_deform_xy` | 대기 손실원뿔 | 빼내는 껍질. `border_dist ≈ 0`이면 손실원뿔 고도(~1.05 R_p)의 구면 절단으로 퇴화 | 선량 영역의 내측 경계 |
| `*_compression` / `*_extension` (벨트) | 경계 비대칭이 껍질까지 얼마나 닿는지 | pause 비대칭을 `(r_core/R_mp)³`로 감쇠 — 아래 절 | `pause_compression`·`pause_extension`, `R_mp` |
| `*_deform` | 비쌍극 요철 | SDF에 더하는 진폭(바디 반경 단위)이라 경계가 최대 ±A만큼 흔들림. ROKerbalism 앵커(`mercury`/`irregular` 0.1, `metallic`/`solidiron`/`anomaly` 0.04–0.1) | 요철의 *크기*는 아래 미구현 `*_deform_scale`이 정함 |
| `radiation_inner` / `radiation_outer` | Part B regime call | 공급 − 손실, K–P 상한. `scripts/refs/kp_limit.py`로 검산 | `gradient`가 1 미만일 때 |
| `radiation_*_gradient` | 반경방향 프로파일 모양 | `*_radius / d*`(위) | `*_radius` |
| `geomagnetic_pole_lat` / `_lon` | 쌍극 기울기 | `lat = 90° − magnetic_dipole_tilt_deg`. 역전 쌍극은 부호가 따라감(목성 −80) | aurora 행의 오벌 편심 |
| `geomagnetic_offset` | 쌍극 중심의 이동 | 자기축 방향 이동거리 / R_p (수성 0.198, 천왕성 0.3, 해왕성 0.55). `deform`과 달리 축대칭 유지 | 벨트도 함께 이동. `deform`과 이중계상 금지 |
| `*_quality` | 레이마치 스텝 수 | 렌더 전용, 물리 없음 | 없음 |
| `radiation_surface` | 항성 레벨 필드 | **항성 전용**. 행성 표면 선량은 여기 없음(그 사슬은 `surface-radiation-dose-methodology.md`) | 없음 |

### 벨트 `*_compression` / `*_extension` — 경계의 비대칭을 안쪽으로 감쇠시켜 상속

벨트 껍질은 자기권계면도 아니고 원도 아닙니다. 둘 사이에 있으니, 정직한 질문은 경계의 주야
비대칭이 그 껍질까지 **얼마나** 닿느냐입니다. 답은 두 극한이 고정합니다.

- 깊은 안쪽(`r ≪ R_mp`)은 왜곡되지 않은 쌍극장이라 껍질이 **대칭**입니다. `compression =
  extension = 1`.
- 경계에서는 껍질이 곧 경계이므로 pause의 비대칭을 그대로 가집니다. 그 바깥에서는 드리프트
  셸이 갈라지고 열립니다(Pfitzer 1969, [`1969JGR....74.4687P`](https://ui.adsabs.harvard.edu/abs/1969JGR....74.4687P); Öztürk & Wolf 2007,
  [`2007JGRA..112.7207O`](https://ui.adsabs.harvard.edu/abs/2007JGRA..112.7207O)).

두 극한 사이의 가중치는 그 반경에서의 **외부(경계전류) 자기장 대 쌍극장 비**입니다.
Chapman–Ferraro 전류는 내부 영역에 거의 균일한 자기장을 만들고 그 크기가 경계에서의 쌍극장
정도인데, 이것이 Part A가 이미 쓰고 있는 `f ≈ 2` 배가와 같은 이야기입니다. 그래서

    ε(r) = ( r / R_mp )³ ,      r_core = *_dist / √(*_deform_xy)

이고, 껍질은 pause 왜곡의 그 비율만큼을 물려받습니다.

    *_compression = 1 + ε · (pause_compression − 1)
    *_extension   = 1 − ε · (1 − pause_extension)

ε는 껍질의 **핵심 원**에서 계산하십시오. 바깥 에지가 아닙니다. Kerbalism은 껍질 전체에 x-스케일
하나만 적용하고, 핵심이 선량 피크와 껍질의 대표 L을 함께 들고 있으므로 핵심 값이 껍질 평균에
해당합니다. 에지 값은 상한으로 함께 계산해 둘 만합니다. 지구 외대는 핵심 `ε 0.05`에 에지
`ε 0.35`인데, 이 차이가 "껍질당 스케일 하나"라는 Kerbalism 설계가 강요하는 근사의 크기입니다.

왜곡의 형태에 대한 근거는 Mead 1964([`1964JGR....69.1181M`](https://ui.adsabs.harvard.edu/abs/1964JGR....69.1181M))입니다. Chapman–Ferraro 해는
주간면과 야간면 **양쪽** 자기력선을 압축하고, 주야 비대칭 자체는 위성 관측으로 정량화된 분산
전류에서 나옵니다(Mead & Fairfield 1975, [`1975JGR....80..523M`](https://ui.adsabs.harvard.edu/abs/1975JGR....80..523M)). 채택한 pause 형상으로
보간하는 것은 그 비대칭 항의 대리이지 도출이 아니므로 이 레시피는 **중저 신뢰**입니다. 다만
양 끝이 고정되어 있고, 이전의 복사한 상수를 대체합니다. Mead의 *수치*는 정량 작업에서는
위성 피팅 Tsyganenko 계열(T02, [`2002JGRA..107.1179T`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1179T))로 오래전에 대체됐습니다. 보간보다
정확해야 할 일이 생기면 ansatz를 다듬는 대신 T 계열 자기장을 피팅해 셸 비대칭을 직접 읽는
것이 정답입니다.

**검증.** 이 레시피는 ROKerbalism 가니메데의 벨트 compression 1.05를 알려주지 않았는데
되찾아옵니다(핵심 `ε` 0.139. 임베디드 위성은 벨트가 2 R_moon 짜리 standoff의 큰 몫을 채우기
때문입니다). 지구 내대의 거의 대칭인 상태도 재현합니다(배포값 1.01에 대해 1.001). 정지궤도에서는
`ε` 0.29로 야간면이 1.36배 늘어나는데, 잘 알려진 그곳의 주야 비대칭과 같은 급입니다. 어긋나는
쪽이 오히려 유익합니다. 자이언트의 배포값 1.05 / 0.9는 도달 불가입니다. 63 R_J standoff 안의
8 R_J 벨트는 `ε`이 0.002이니, 그 숫자는 물리가 아니라 연출입니다. 이 항이 실제로 무는 바디는
눌린 쪽입니다. **Proxima d**(외대 `ε` 0.107 → 1.05 / 0.90. 지금 들고 있는 값은 지구에서 복사한
1.01 / 1.0)와 임베디드 위성 가니메데·A b III(`ε` 0.099 → 1.015 / 0.96)입니다.

재현성을 지키는 습관 두 가지. 벨트 지오메트리는 손으로 맞추지 말고 `fit_belts.py`로 구하십시오
(실제 SDF에 대해 IoU를 최적화하므로 적어 넣는 숫자가 엔진이 렌더하는 숫자와 같아집니다). 그리고
출력값 옆에 **입력값**(`B_eq`, `P_ram`, `L` 경계, 공급항)을 보드에 함께 남기십시오. 위 필드는
전부 물리량 네댓 개의 하류입니다.

### ⚗ 아직 없는 필드 — KerbalismShuePause 플러그인

벨트 뷰어가 노출하는 손잡이 셋은 **현재 배포된 어떤 Kerbalism도 읽지 않습니다.** 값은 지금
구해서 기록해 두고, 인하우스 Harmony 2 패치(또는 업스트림 PR)를 기다립니다. 기각한 대안까지
포함한 브리프는
[`plugins/KerbalismShuePause/README.md`](../../../plugins/KerbalismShuePause/README.md)입니다.
파이프라인 규율은 이렇습니다. emitter는 이들을 `PENDING_MODEL_KEYS`에 두고 cfg 줄로 **절대**
쓰지 않으며, 뷰어는 `⚗`로 표시하고 주석으로만 내보내며, 보드는 미사용 표시를 달아 값을 실을
수 있습니다. 도출은 한 번만 하고, 플러그인이 오기 전까지 게임은 스톡 거동을 렌더합니다.

**`*_deform_scale`** (`pause_`/`inner_`/`outer_`). Kerbalism의 deform은 SDF에
`sin(x·5)·sin(y·7)·sin(z·6)·A`를 더합니다. 진폭 `A`는 조절되지만 파수가 하드코딩이라 요철이
*얼마나 큰지*는 정할 수 없습니다. 수성 수준인 standoff 1.54 R_p에서 저 파수는 경계에 8–11개
lobe를 만드는데, dynamo 레시피가 실제로 내놓는 다극장보다 훨씬 잘게 쪼갠 값입니다. scale은 그
파수에 걸리는 배수이고(`1.0`이 스톡과 완전히 동일하므로 배포된 cfg는 하나도 바뀌지 않습니다),
보기 좋게 고르는 값이 아니라 자기장에서 나옵니다.

    k = ℓ / R_mp                deform_scale = k / 5

`ℓ`은 그 자기장의 지배적 구면조화 차수입니다(dynamo 레시피의 regime call에서 옵니다). `ℓ = 4`
까지 파워가 있는 dynamo가 `R_mp` 1.54에 있으면 `k ≈ 2.6`, 즉 `deform_scale ≈ 0.52`입니다.
진폭과 scale은 서로 독립입니다. `A`는 경계가 얼마나 멀리 흔들리는지, scale은 몇 개의 lobe로
흔들리는지입니다.

**Shue 기반 pause** (`pause_shue`, `pause_nose` = r0, `pause_alpha` = α, `pause_tail` = L).
Kerbalism의 pause는 구를 x방향으로 구간별 스케일한 것이라 노즈가 지나치게 뭉툭하고, 최대
단면이 바디 평면에 못 박히며, 꼬리가 방추형으로 닫힙니다. Shue et al. 1997/1998
([`1997JGR...102.9497S`](https://ui.adsabs.harvard.edu/abs/1997JGR...102.9497S) / [`1998JGR...10317691S`](https://ui.adsabs.harvard.edu/abs/1998JGR...10317691S))이 물리량 둘로 하는 일을 결합된 필드
셋으로 대신하는 셈입니다. 채택한 형태는 이음매 없는 C∞ 닫힌 곡선 하나인 **연화 Shue**입니다.

    r(θ) = r0 · [ (1+ε) / (ε + cos²(θ/2)) ]^α        ε = 1 / ( (L/r0)^(1/α) − 1 )

`ε → 0`이면 정확한 Shue로 돌아가고, `ε > 0`이면 `r(180°) = L`에서 기울기 0으로 꼬리가 닫히며
어디에도 이음매가 없습니다. 세 필드의 도출은 이렇습니다. **r0**은 Part A의 Chapman–Ferraro
노즈를 그대로 씁니다(압축비로 인코딩하지 않습니다). **α**는 Shue 98의 램압력·IMF `Bz` 적합에서
나오고, 조용한 항성풍 기본값이 0.58입니다(`α ≥ 0.5`는 본질적으로 열린 꼬리라는 뜻이고, 닫는
일은 α가 아니라 `ε` 항의 몫입니다). **L**은 lobe 자기장이 GCR에 무의미해지는 거리입니다.
기존 필드에서의 환산은 별도 비용이 없습니다. `α = log₂(compression)`, `r0 = pause_radius / compression`,
`L = pause_radius / extension`. 다만 이 환산이 형상을 보존하는 것은 지구형 cfg뿐입니다. RSS
목성의 `compression` 1.05는 α 0.07로 환산되어 주야면이 비물리적으로 구에 가까워지므로,
자이언트는 환산 후 α를 다시 조율해야 합니다. (이 문단의 이전 개정본은 "자이언트 자기권계면은 Shue 형식으로 적합되지 않는다"고 단정했습니다.
틀렸으므로 철회하고, 아래 적합 α 표로 대체합니다.)

**바디별 적합 α.** 발표된 α가 있으면 그것을 쓰고, 없을 때만 compression 환산으로 내려가되 그
사실을 밝히십시오.

| 바디 | α | 출처 |
|---|---|---|
| 지구 | 0.58 (조용한 항성풍. Dp·Bz 의존) | Shue 1998, [`1998JGR...10317691S`](https://ui.adsabs.harvard.edu/abs/1998JGR...10317691S) |
| 수성 | **0.5**, `R_ss` 1.45 R_M | Winslow 2013, [`2013JGRA..118.2213W`](https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W) — MESSENGER 통과를 바로 이 형식으로 적합 |
| 목성 | **α = 0.28 + 1.08·p_SW** (nPa), `r_SS = 38.0·p_SW^−0.25` R_J → 관측 압력대에서 0.31–0.42 | Rutala 2025, [`2025JGRA..13033842R`](https://ui.adsabs.harvard.edu/abs/2025JGRA..13033842R) / [2502.09186](https://arxiv.org/abs/2502.09186), 그들의 "S97*" 형식 Table 2 |
| 토성 | Shue 형식 적합 있음. Dp가 오르면 flaring이 **감소**, 크기 ∝ Dp^−1/4.3 | Arridge 2006, [`2006JGRA..11111227A`](https://ui.adsabs.harvard.edu/abs/2006JGRA..11111227A) — 계수는 유료 본문에 있어 아직 확보 못 함 |
| 천왕성·해왕성 | Shue 형식 적합 못 찾음 | — |

배울 점은 *방향*입니다. 목성의 flaring은 지구보다 **작습니다**(0.31–0.42 대 0.58). 자전이
지배하고 플라스마로 부푼 자기권이 지구보다 축대칭 타원체에 가깝기 때문입니다. 따라서 자이언트의
α가 지구보다 작은 것 자체는 오류가 아닙니다. 오류는 그 값을 `pause_compression`에서 읽는 것이고,
그 숫자는 적합이 아니라 저작 선택입니다. Shue 형식을 원치 않을 때의 대안으로 목성의 옛 다항식
모델(Joy 2002, [`2002JGRA..107.1309J`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1309J))과 토성의 압력균형 형상
(Kanani 2010, [`2010JGRA..115.6207K`](https://ui.adsabs.harvard.edu/abs/2010JGRA..115.6207K); Achilleos 2008,
[`2008JGRA..11311209A`](https://ui.adsabs.harvard.edu/abs/2008JGRA..11311209A))이 남아 있습니다.

**`pause_offset`**은 전체 Shue 모드가 기각될 때의 값싼 대안입니다. 스케일 전에 구의 중심을
꼬리쪽으로 옮기면(`p.x += pause_offset`) "최대 폭이 바디 평면에 박힌다"는 결함이 한 줄로
고쳐집니다. Proxima c의 연화 Shue 곡선(노즈 11.905, α 0.5, 꼬리 125)에 최소제곱으로 맞추면
`pause_offset` 19.7 / radius 21.5 / compression 0.68 / extension 0.204가 노즈, 바디 평면 폭,
최대 폭, 꼬리 닫힘을 모두 수 % 안에서 재현합니다. 배포된 스톡·ROKerbalism pause는 전부 같은
방식으로 꼬리 폭을 과소평가하므로(지구는 측면 15인데 관측된 꼬리 반경이 25–30 R_E), 이건
NearStars만의 문제가 아닙니다.

## Part D — 위성 ↔ 모행성 상호작용 (임베디드 자기권)

거대행성 자기권 *안*을 도는 위성은 NearStars에서 흔한 경우입니다(A b 위성 전부).
축소판 행성이 아닙니다. 세 가지 커플링이 지배하며 모두 방사선과 직결되고, 위성 *자체*
자기장은 조연입니다.

1. **위성은 모행성 벨트 안에 산다.** 위성 표면이 받는 방사선은 압도적으로 위성이 만드는 게
   아니라 그 L-shell에서의 *모행성* 포획 플럭스입니다. 그래서 첫 질문은 늘 *위성이 모행성
   벨트의 어디에 있나*(R_parent 단위 궤도거리, Part A의 모행성 standoff에 갇힘)입니다. 벨트
   한복판이면 구워지고(Io. A b I 1.54 R_p), 벨트 gap이면 살 만합니다(A b III 3.53 R_p).
   위성 자체 장은 이 주변 선량을 차폐로 *조절*할 뿐입니다.

2. **위성은 모행성 벨트의 손실(또는 공급)항이다.** 고체 위성·고리는 스쳐가는 포획 입자를
   **흡수**해 고갈 통로를 파고, 위성+고리 계 전체로는 모행성 벨트를 Kennel–Petschek 천장
   *아래로* 끌어내립니다(Cooper 1983 — 토성이 원형, 고리·위성이 벨트를 도려냄). 위성이 많은
   거대행성이 자동으로 목성급이 **아닌** 이유입니다 — 위성+고리가 큰 분산 sink입니다. 반대로
   화산 위성은 **공급원** — Io / Dante가 플라스마 토러스를 먹여 벨트를 천장 쪽으로 밀어올립니다
   (Bagenal 1994). 한 위성이 둘 다일 수 있습니다: Dante는 전역으로 토러스를 먹이면서 국소로는
   입자를 쓸어냅니다.

3. **위성 자체 미니자기권** (고유 다이나모가 있을 때만). standoff는 위성 場을 항성풍이 아니라
   **모행성의 공회전 자기권 플라스마**에 대해 잡습니다 — Part A에서 `P_ram` = 모행성 플라스마.
   태양계 유일 사례가 가니메데입니다(Kivelson 1996). 특성.
   - **작고 부분적으로 열림.** 모행성 場이 위성을 관통하고, 위성 場이 국소 모행성 場의 몇 배
     정도인 곳에서 자기력선이 재결합해 극에서 샙니다(가니메데: 국소 목성 場의 ~6배 → standoff
     ~2 R_G, 열린 극관). 위성 場이 강할수록 더 크고 덜 새는 미니자기권.
   - **자체 벨트는 약하고 공급원 기아.** 폐쇄 포획 부피가 작고, 공급원은 모행성 벨트로부터의
     안쪽 확산(gap에 있으면 빈약) + 대기 CRAND뿐. 그래서 자체 벨트는 K–P 천장에 거의 못
     닿습니다 — **場-한계가 아니라 공급원-한계**이며, 단일 좁은 벨트입니다(지구식 2벨트 불가).
   - **주역할 = 발생기 아닌 차폐.** 미니자기권이 표면 거주가능성에 미치는 주효과는 *모행성*
     벨트 플럭스를 막는 것이고, 실제로 가두고 정출시키는 입자는 지표를 굽기보다 오로라를
     먹입니다. 고유 위성 자기장은 위협이 아니라 보호입니다.

**강장 임베디드 위성 (별도 sub-regime — 가니메데 유추가 깨짐).** 위 항목들은 위성 場이 *약한*
경우(가니메데, 국소의 ~6배 → 새고 자체 벨트가 무시할 만함)를 전제합니다. 고유 다이나모가
**행성급** — 국소 모행성 場의 몇 배가 아니라 *절대값*으로 지구급 이상 — 인 위성은 질적으로
다른 경우라, 가니메데 틀에 억지로 끼우면 **안 됩니다**.

- **작은 크기, 반대되는 원인.** 고립 상태라면 그런 위성은 *지구 이상*의 자기권을 가집니다
  (위성 場 대 항성풍 램으로 잡은 독립 standoff가 지구를 넘음). 임베딩이 그걸 압축하는데,
  이제 외부 압력이 모행성의 **국소 자기압** `B_parent²/2μ₀`이고 거대행성 場 깊숙이서는 이 값이
  항성풍 램보다 *자릿수로* 크기 때문입니다 — 그래서 standoff는 **위성 場이 아무리 강해도**
  위성 반경 몇 배로 붕괴합니다. 이 작은 크기는 약한 場이 아니라 *고압 환경이 강제*한 것입니다.
  場 교차 standoff는 `R_mp/R_moon ≈ (B_eq^moon / B_parent^local)^(1/3)`(위성 쌍극 크기가 주변
  모행성 場과 같아지는 반경)이고, 공회전 플라스마 램이 조금 더 깎습니다.
- **벨트는 지구-*류*이지 가니메데식 무시 수준이 아님.** 높은 지배비(≳15–20배)는 *대부분 닫힌*
  자기력선을 줍니다 — 극 cusp가 작고 재결합 누출이 적어 — 그래서 실제 폐쇄 포획 부피가
  존재하고, **두꺼운 대기가 CRAND**(Lenchek 1961), 즉 지구 내대를 채우는 바로 그 내부
  양성자원을 공급합니다. 그래서 가니메데와 달리 실제 내대가 형성됩니다. 두 모행성 효과가 이를
  여전히 *완화*합니다. 모행성 자기권이 **은하우주선을 차단**해 CRAND 구동을 조이고, 벨트-gap
  궤도가 방사확산을 굶깁니다. 순 강도는 **완만하지만 무시 못 할** 수준입니다 — 차폐 없는 지구보다
  훨씬 아래, 가니메데보다 훨씬 위. 여전히 단일 벨트입니다(압축된 부피엔 지구식 2벨트 여지 없음).
- **주역할 = 강한 차폐 + 실제 궤도고도 벨트.** 큰 지배비가 차폐를 튼튼하게 만들고(표면 선량 ≈
  위성 L-shell에서의 주변 모행성 플럭스를 크게 줄인 값), 그것이 유지하는 CRAND 벨트는 표면이
  아니라 *궤도* 비행체에 대한 위협이며, 그 정출이 진짜 오로라 오벌을 구동합니다. Heller & Zuluaga
  2013([`2013ApJ...776L..33H`](https://ui.adsabs.harvard.edu/abs/2013ApJ...776L..33H), arXiv 1309.0811)이 외계위성에 대해 바로 이 차폐-대-벨트 긴장을
  다루고, 형성 모델상 지구질량·강장 위성은 *가능성이 낮다*고 지적합니다 — 그래서 이 sub-regime은
  물리적으로 일관되지만 **관측적으로 전례가 없습니다**(픽션 전제 regime. 신뢰도 low로 표기하고,
  태양계 전형을 주장하지 말 것 — 실제 고유-다이나모 위성은 가니메데뿐이고 그마저 약함).

**Kerbalism 매핑(임베디드 위성):** 위성에 자체 소형 `RadiationModel`(위성 반지름 단위의 작은
`pause_radius`, 단일 좁은 벨트) + 작은 스톡 스케일 `radiation_pause`(~−0.01. 차폐는
`pause_radius`에 pause가 *있다는 것*이지 큰 값이 아님)를 가진 `RadiationBody`를 줍니다. 위성 순
표면 선량 = 그 L-shell의 모행성 벨트를 자체 pause로 감쇠한 값. `radiation_inner`는 sub-regime별로
나눕니다. **약장** 위성(가니메데)은 공급원 기아라 → *약함*(~0.2× 스톡 Kerbin). **강장**
위성(A b III)은 실제 CRAND 벨트를 유지해 → *완만함*(~0.3–0.5× Kerbin), GCR 차단으로 지구 아래지만
가니메데식 무시 수준보다는 훨씬 위. 어느 쪽도 場 읽기가 아니라(Part B) 둘 다 공급원–손실 regime
판정입니다.

**워크드(A b III = 강장, vs 가니메데 = 약장):** A b III(75 µT eq, 3.53 R_p, A b 벨트 gap)
→ 場이 국소 모행성 場 3.9 µT의 ~19배. 고립 상태라면 *지구보다 큰* 자기권을 가집니다(독립
standoff ~17 R_moon, A b 항성풍 램 대비). 임베딩하면 모행성 국소 자기압(~6 µPa, 항성풍
램의 ~3000배)이 ~7배 압축해 場 교차 standoff `(75/3.9)^(1/3) ≈ 2.6 R_moon`로 만듭니다. 높은
19배 지배비가 대부분 닫힌 상태를 유지하므로 그 두꺼운 거주가능 대기가 가니메데식 무시 수준이
아니라 **실제 CRAND 내대**를 유지합니다 — `radiation_inner ≈ 4` rad/h(스톡 Kerbin 10.4의 ~0.4배.
Polyphemus의 GCR 차단 + gap 기아지만 진짜 지구-*류* 벨트), `radiation_pause ≈ −0.01`. 가니메데
(0.72 µT, 국소 목성 場의 ~6배, 대기 없음) → standoff ~2 R_G, 열린 극관, 무시할 만한 자체 벨트.
**둘 다 표면 발생기가 아니라 차폐입니다.** Pandora의 거주가능성은 (gap + 차폐)의 주변 선량
감소에 기대고, 그 CRAND 벨트는 오로라를 먹이는 궤도고도 위협이지 표면 위협이 아닙니다.

## 검증

- **지구**: B_eq = 31 µT, 항성풍 P_ram ≈ 2 nPa → R_mp/R_p = [2²·(3.1e-5)²/(2μ₀·2e-9)]^(1/6) ≈ **9.6** — 관측된 ~10 R_E sub-solar 자기권계면과 일치. 내부벨트 ~1.2 R_E(CRAND 양성자), 외부 ~3–7 R_E(확산 + chorus), 강도는 K–P 천장 부근. ✓
- **목성**: 場만으로는(~4.3 G 적도) 극단적 벨트를 예측하지 못함. Io 플라스마원이 전자 K–P 한계까지(그 이상까지) 몰아붙임 — 강도 ≠ f(B)의 교과서적 증거. ✓
- **A b**(NearStars): 170 µT vs α Cen A 풍 램 0.38 nPa → R_mp ≈ **22 R_p**(Phase 4 보드의 독립 23.5 R_p와 같은 균형). ✓

## 유효 범위: regime

1. **쌍극 고유**(지구, A b III): standoff 공식 적용; 벨트는 L-shell 위; 공급원이 강하면
   K–P 캡.
2. **다극 고유**(천왕성/해왕성, Proxima c; `Ro_ℓ > 0.12` 암석 다극 regime): offset/기운
   場 → **비대칭·얼룩진 벨트**와 틀어진 오로라 오벌. standoff 공식은 근사일 뿐이고, 여기서
   **극/적도 비 ≠ 2**가 다극 성분을 실제로 인코딩합니다 — 두 場을 다 들고 있는 게 redundant
   가 아니라 정보값이 되는 유일한 경우입니다.
3. **임베디드 위성**(거대행성 자기권 안의 위성): standoff를 항성풍이 아니라 **모행성의 공회전
   자기권 플라스마 / 場**에 대해 잡습니다. 결과는 미니자기권. 위성 위치의 벨트 선량은 *모행성*의
   그 L-shell 벨트(모행성엔 손실/공급항) + 위성 자체 차폐로 결정됩니다. 두 sub-regime이 있습니다
   (Part D 참조).
   - **3a 약장**(가니메데, Kivelson 1996 [`1996Natur.384..537K`](https://ui.adsabs.harvard.edu/abs/1996Natur.384..537K)): 국소의 몇 배 → 새고, 열린
     극관, 무시할 만한 자체 벨트. 순수 차폐.
   - **3b 강장**(행성급 다이나모, 예: A b III; Heller & Zuluaga 2013 [`2013ApJ...776L..33H`](https://ui.adsabs.harvard.edu/abs/2013ApJ...776L..33H)):
     본질적으로 지구 이상이지만 모행성 자기압에 위성 반경 몇 배로 압축됨. ≳15–20배 지배비 →
     대부분 닫힘 → (대기가 있으면) 실제 CRAND 벨트, 모행성 GCR 차단으로 완화됨. 강한 차폐 **에
     더해** 진짜 궤도고도 벨트. 태양계 전형 없음(신뢰도 low).
4. **유도 / 다이나모 없음** (레시피는 Part A의 유도 자기권 절)(금성, Io, 사멸 암석행성): 고유 포획 없음, 벨트 없음.
   상호작용은 전리층/유도형이고 표면 선량은 직접 풍 + GCR입니다.
5. **약장/무대기**: `B_eq < 0.1× 지구` → 안정 벨트 없음, 표면 선량 직접.

## 워크드 예제 (NearStars)

- **A b**: 170 µT → R_mp ≈ 22 R_p. **5개 위성 전부 자기권 안**에서 공전. 벨트
  강도는 場 읽기가 아니라 *공급원 − 손실* 이야기입니다. Dante의 극단적 화산(~820× Io)이
  강한 내부벨트를 먹이고(공급원), 고리 + 5위성이 입자를 쓸어냅니다(손실, 토성 참조).
  고리 + 5위성이 입자를 쓸어내지만(손실), A b I 화산(~820× Io)이 훨씬 큰 항이라 Polyphemus는
  **토성식 고리-sweep이 아니라 목성식 공급원 지배**입니다. Kerbalism 템플릿은 목성(RSS): 강한
  A b I-공급 *내대*(`radiation_inner` ~300, 목성 값 또는 그 이상) + 약한 외대, 큰 `pause_radius`,
  작은 스톡 스케일 `radiation_pause`(~−0.01). 설계의 핵심이 바로 이것 — 강화된 내대가 내측
  위성을 구우면서(A b I >4500 rem/day), 거주가능 Pandora는 gap에서 자체 강한 자기장 차폐로 생존.
- **A b III**(임베디드, **강장** sub-regime 3b — 가니메데 아날로그 *아님*): 자체 75 µT
  쌍극 → 본질적으로 지구 이상의 자기권(독립 ~17 R_moon)이 A b 場 *안*에서 ~7배 압축돼
  ~2.6 R_moon 미니자기권. **A b 두 벨트 사이 gap**에 위치하고 자체 場이 차폐를 더함 →
  거주가능의 물리 근거. 높은 19배 지배비 + 두꺼운 대기가 실제 CRAND 벨트를 유지합니다
  (`radiation_inner ≈ 4` rad/h, 오로라를 먹이는 궤도고도 위협이지 표면 위협 아님). standoff는
  항성풍이 아니라 A b 국소 場에 대해 잡습니다.
- **Proxima b**(약 쌍극 ~0.06–0.1 ℳ⊕): 작은 자기권, standoff 몇 R_p뿐; 벨트 미미;
  표면 선량은 직접 M왜성 풍 + 플레어 지배.
- **Proxima c**(빙거성, offset/기운 다극): 비대칭 벨트, 틀어진 오벌; standoff 공식 근사;
  47° 틀림이 off-axis 오로라 구동.

신뢰도: standoff 지오메트리는 **medium**(강건한 `^(1/6)` 법칙, 지구/Polyphemus 검증).
벨트 강도는 본질상 **low** — 외계행성에서 그 자체로 불확실한 공급원·손실 항에 의존하며,
바로 그래서 계산값이 아니라 documented regime 판정으로 둡니다.

## 인용

- **Chapman & Ferraro 1931**, Terr. Magn. Atmos. Electr. 36, 77 ([`1931TeMAE..36...77C`](https://ui.adsabs.harvard.edu/abs/1931TeMAE..36...77C)).
  자기권계면 / 압력균형 개념의 기원.
- **Shue et al. 1997 / 1998**, JGR 102, 9497 ([`1997JGR...102.9497S`](https://ui.adsabs.harvard.edu/abs/1997JGR...102.9497S)) / JGR 103, 17691
  ([`1998JGR...10317691S`](https://ui.adsabs.harvard.edu/abs/1998JGR...10317691S)). 경험적 자기권계면 standoff + 풍 변화에 따른 형상.
- **Kennel & Petschek 1966**, JGR 71, 1 ([`1966JGR....71....1K`](https://ui.adsabs.harvard.edu/abs/1966JGR....71....1K)). 안정포획 플럭스 한계 —
  벨트 강도의 공급원-무관 천장. Part B의 핵심.
- **Summers, Tang & Thorne 2009**, JGRA 114, A10210 ([`2009JGRA..11410210S`](https://ui.adsabs.harvard.edu/abs/2009JGRA..11410210S));
  **Summers et al. 2014**, JGRA 119, 6313 ([`2014JGRA..119.6313S`](https://ui.adsabs.harvard.edu/abs/2014JGRA..119.6313S)).
  상대론적 K–P 정식화(eqs A1–A8)와 ~E⁻¹ 제한 스펙트럼(상대론적 계수가 비상대론의 2배).
  둘 다 유료·preprint 없음 — 방정식은 아래 Mauk & Fox Zenodo 소프트웨어로 복원.
- **Mauk & Fox 2010**, JGRA 115, A12220 ([`2010JGRA..11512220M`](https://ui.adsabs.harvard.edu/abs/2010JGRA..11512220M)).
  행성 간 미분 K–P 프레임워크: 지구/목성/천왕성이 캡에, 해왕성은 아래(주입 기아),
  토성도 아래(물질 손실). 유료. **그들의 공개 구현**([Zenodo 10.5281/zenodo.4782323](https://zenodo.org/records/4782323),
  [`2021zndo...4782323M`](https://ui.adsabs.harvard.edu/abs/2021zndo...4782323M))은 캐시(`_papers/mauk_fox_KP.nb` + 실행)되어
  `scripts/refs/kp_limit.py`로 포팅됨(출력 중간값 11개에서 ≤0.05 %로 검증).
- **Mourenas et al. 2024**, JGRA 129, e32193 ([`2024JGRA..12932193M`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932193M)).
  ~3 파동-이득 기준의 독립 확인(ELFIN).
- **Seltzer 1979 / 1992**(SHIELDOSE / SHIELDOSE-2,
  [`1979ITNS...26.4896S`](https://ui.adsabs.harvard.edu/abs/1979ITNS...26.4896S),
  [`1992STIN...9315580S`](https://ui.adsabs.harvard.edu/abs/1992STIN...9315580S)).
  표준 전자/양성자 fluence → Al 뒤 선량 수송 — 선량 대비가 ~1 MeV 미분 캡이 아니라
  스펙트럼 경도로 정해지는 이유.
- **Schulz & Lanzerotti 1974**, *Particle Diffusion in the Radiation Belts* ([`1974pdrb.book.....S`](https://ui.adsabs.harvard.edu/abs/1974pdrb.book.....S)).
  벨트를 채우는 방사확산 수송.
- **Lenchek et al. 1961**, JGR 66, 4027 ([`1961JGR....66.4027L`](https://ui.adsabs.harvard.edu/abs/1961JGR....66.4027L)). CRAND 내부벨트 공급원.
- **Divine & Garrett 1983**, JGR 88, 6889 ([`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D)); **Bagenal 1994**,
  JGR 99, 11043 ([`1994JGR....9911043B`](https://ui.adsabs.harvard.edu/abs/1994JGR....9911043B)). 목성 방사선 + Io 내부 플라스마원 — "강도는 場이
  아니라 공급원이 정한다"의 canonical 사례.
- **Ripoll et al. 2016**, GRL 43, 5616 ([`2016GeoRL..43.5616R`](https://ui.adsabs.harvard.edu/abs/2016GeoRL..43.5616R)); **Cheng et al. 1987**, JGR 92,
  15315 ([`1987JGR....9215315C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215315C)). 각 벨트의 플럭스가 실제로 어디서 최대인지. 지구 내대 피크와
  슬롯, 천왕성의 위성-소거 극소 사이 넓은 최대. `radiation_*_gradient` 레시피가 `d*`를 읽어오는
  프로파일 형상이 이들입니다.
- **Ginet et al. 2013**, SSRv 179, 579 ([`2013SSRv..179..579G`](https://ui.adsabs.harvard.edu/abs/2013SSRv..179..579G)). AE9/AP9/SPM, 현행 표준
  포획입자 플럭스 규격이며 AE8/AP8의 후속. 지구의 반경방향 프로파일은 여기서 읽습니다. "AP9"라고
  뭉개지 말고 이 논문을 인용할 것.
- **Mead 1964**, JGR 69, 1181 ([`1964JGR....69.1181M`](https://ui.adsabs.harvard.edu/abs/1964JGR....69.1181M)); **Mead & Fairfield 1975**, JGR 80,
  523 ([`1975JGR....80..523M`](https://ui.adsabs.harvard.edu/abs/1975JGR....80..523M)); **Tsyganenko 2002**, JGRA 107, 1179
  ([`2002JGRA..107.1179T`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1179T)). 경계전류가 내부 자기장을 어떻게 변형하는지. Mead는
  Chapman–Ferraro 해의 형태(주간·야간 양쪽 압축), Mead & Fairfield는 이론이 과소평가한 분산 전류,
  Tsyganenko는 현행 정량 표준입니다. Mead의 *서술*은 오늘도 canonical로 인용되지만 *계수*는 T 계열로
  대체됐습니다. 벨트 `*_compression`/`*_extension` 레시피의 근거입니다.
- **Pfitzer et al. 1969**, JGR 74, 4687 ([`1969JGR....74.4687P`](https://ui.adsabs.harvard.edu/abs/1969JGR....74.4687P)); **Öztürk & Wolf 2007**,
  JGRA 112, A07207 ([`2007JGRA..112.7207O`](https://ui.adsabs.harvard.edu/abs/2007JGRA..112.7207O)). 왜곡된 자기권에서의 드리프트 셸 분열. 관측으로
  확인된 뒤 주간면 자기권계면 근처에서 매핑됐습니다. 비대칭 레시피의 바깥 한계, 즉 셸이 더는 닫힌
  면이 아니게 되는 지점입니다.
- **Thorne 2010**, GRL 37, L22107 ([`2010GeoRL..3722107T`](https://ui.adsabs.harvard.edu/abs/2010GeoRL..3722107T)); **Ripoll et al. 2020**,
  JGRA 125, e26735 ([`2020JGRA..12526735R`](https://ui.adsabs.harvard.edu/abs/2020JGRA..12526735R)). 파동–입자 가속·손실; 현대 벨트 동역학 리뷰.
- **Cooper 1983**, JGR 88, 3945 ([`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C)). 벨트 손실로서의 고리/위성 흡수 —
  A b 고리 + 위성 케이스.
- **Kivelson et al. 1996**, Nature 384, 537 ([`1996Natur.384..537K`](https://ui.adsabs.harvard.edu/abs/1996Natur.384..537K)). 가니메데 임베디드
  자기권 — 약장 임베디드 위성(sub-regime 3a) 전형.
- **Heller & Zuluaga 2013**, ApJ 776, L33 ([`2013ApJ...776L..33H`](https://ui.adsabs.harvard.edu/abs/2013ApJ...776L..33H), arXiv
  **[1309.0811](https://arxiv.org/abs/1309.0811)**). 거대행성 자기권 안에서의 외계위성 자기
  차폐 — 차폐-대-벨트 긴장, 그리고 지구질량·강장 위성은 형성 가능성이 낮다는 지적. 강장
  임베디드 위성(sub-regime 3b)을 일관되지만 전례 없는 것으로 근거화(픽션 전제).
- **Bertucci et al. 2011**, SSRv 162, 113 ([`2011SSRv..162..113B`](https://ui.adsabs.harvard.edu/abs/2011SSRv..162..113B)); **Luhmann 1991**, SSRv
  55, 201 ([`1991SSRv...55..201L`](https://ui.adsabs.harvard.edu/abs/1991SSRv...55..201L)); **Brace et al. 1980**, JGR 85, 7663
  ([`1980JGR....85.7663B`](https://ui.adsabs.harvard.edu/abs/1980JGR....85.7663B)); **Zhang et al. 2009**, GRL 36, L20203
  ([`2009GeoRL..3620203Z`](https://ui.adsabs.harvard.edu/abs/2009GeoRL..3620203Z)); **Egan et al. 2019**, MNRAS 488, 2108
  ([`2019MNRAS.488.2108E`](https://ui.adsabs.harvard.edu/abs/2019MNRAS.488.2108E)). 유도 자기권 갈래. 리뷰, 금성 전리층 자기장, 실측 이오노포즈
  고도, 방사 방향 IMF에서의 소멸(근접 외계행성 함의), 그리고 자기장이 유실을 늘리는 대신 차폐를
  시작하는 약장 교차점.

- **Griessmeier et al. 2004**, A&A 425, 753 ([`2004A&A...425..753G`](https://ui.adsabs.harvard.edu/abs/2004A%26A...425..753G)); **Vidotto et al.
  2013**, A&A 557, A67 ([`2013A&A...557A..67V`](https://ui.adsabs.harvard.edu/abs/2013A%26A...557A..67V)). 항성풍/조석고정 대비 외계행성 자기권 크기 —
  근접 행성 standoff 적용.

## Related

- [`rocky-planet-dynamo-methodology.md`](rocky-planet-dynamo-methodology.md), 
  [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md) — 이 방법이 소비하는
  `B_eq`를 공급.
- `../../.claude/skills/nearstars-phase3/references/mod-grounded-fields.md` — 이 방법이
  방출 대상으로 삼는 Kerbalism `RadiationBody`/`RadiationModel` 필드 스키마.
- `methodology-index.md` — 모든 도출값 레시피의 살아있는 인덱스.
