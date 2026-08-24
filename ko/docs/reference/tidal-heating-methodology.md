<!-- 궤도·내부물성에서 조석가열 출력(Ė)을 도출하고 화산·지하해·플룸 가능성을 판정하는 방법론 레퍼런스 -->
# 조석가열 방법론: 내부 출력, 화산활동과 지하 바다

동주기 자전(synchronous rotation)하는 바디(행성을 도는 위성이든, 별을 도는 행성이든)
의 **내부 조석가열 출력** `Ė`를 그 궤도와 내부 구조로부터 도출하고, 그 열이 화산활동,
지하 바다, 또는 플룸을 지탱할 수 있는지를 판정하기 위한 방법 레퍼런스다.
[dynamo 스케일링 문서](planetary-dynamo-scaling.md)와 같은 정신을 따른다. 지어낸 측정치가
아니라 관계식과, 알려진 바디를 재현하는 calibration을 함께 인용한다.

이 값은 **NearStars Phase 4에서 가장 자주 반복된 도출값**이다(α Cen 한 세션에서만 위성
Alpha Centauri A b I~III과 A b V(Dante·Hades·Pandora·Chaos)를 두고 네 번이나 다시 계산했다). 그래서 여기에 canonical
근거 레시피로 정리해 둔다.

> 인용은 즉석 웹 검색이 아니라 NASA ADS(등록된 `ADS_API_TOKEN`)에 대조해 확정한다.
> arXiv id가 있으면 그것을, 없으면 권위 있는 ADS bibcode를 쓴다("no arXiv" 표시).
> 검증된 목록은 §9를 참고하면 된다.
> 교과서가 아니라 실무용 레퍼런스다.

> **범위 주의.** 이 문서는 조석 *가열*(소산된 출력)에 관한 것이다. 이와 관련된 조석
> *고정* 문제(애초에 바디가 동주기 상태가 되는지를 결정하는 despin 시간척도)는
> **별도의 자매 문서로 작성할 예정**이며, 둘을 혼동하지 말아야 한다. 아래 레시피는
> 동주기 자전을 *전제*한다(가열이 의미를 갖는 가까운 바디에서 흔한 상태다). 동주기가
> 아닌 바디라면 먼저 locking 처리가 필요하다.

## 목차

1. [법칙: fixed-Q 조석가열 공식](#1-법칙-fixed-q-조석가열-공식)
2. [Calibration: 공식이 Io와 Enceladus를 재현한다](#2-calibration-공식이-io와-enceladus를-재현한다)
3. [a⁻⁷·⁵ 거리 게이트 (혹독한 교훈)](#3-a⁷·⁵-거리-게이트-혹독한-교훈)
4. [이심률 유지 요건](#4-이심률-유지-요건)
5. [유효 영역: 바디 분류별 k₂/Q와 유변학 문제](#5-유효-영역-바디-분류별-kq와-유변학-문제)
6. [결과 판정: 화산활동 / 바다 / 플룸](#6-결과-판정-화산활동-바다-플룸)
   - [6.1 플럭스 → 영역 표](#61-플럭스--영역-표)
   - [6.2 열은 실제로 어떻게 빠져나가는가: 세 모드의 사다리](#62-열은-실제로-어떻게-빠져나가는가-세-모드의-사다리)
   - [6.3 평원은 배출구가 아니다](#63-평원은-배출구가-아니다)
   - [6.4 용암호 용량 시험 (그리고 두 분모의 함정)](#64-용암호-용량-시험-그리고-두-분모의-함정)
   - [6.5 super-Io 천장: 용암 위성은 얼마나 클 수 있는가](#65-super-io-천장-용암-위성은-얼마나-클-수-있는가)
7. [워크드 예제](#7-워크드-예제)
8. [정직함과 불확실성](#8-정직함과-불확실성)
9. [주석 달린 참고문헌](#9-주석-달린-참고문헌)
10. [관련 문서](#관련-문서)

---

## 1. 법칙: fixed-Q 조석가열 공식

Peale, Cassen & Reynolds 1979 (*Science* 203, 892, [`1979Sci...203..892P`](https://ui.adsabs.harvard.edu/abs/1979Sci...203..892P))는, 보이저가
분출 장면을 촬영하기 며칠 전이라는 유명한 일화와 함께, Io가 조석 소산으로 녹아 있으리라
예측했다. 그들의 일정 위상지연("fixed-Q") 결과는 지금도 1차 도구로 쓰인다. 섭동체 질량
`M_p`를 도는, 장반경 `a`·이심률 `e`의 이심 궤도 위에서 반경 `R`로 동주기 자전하는 바디에
대해, 궤도 평균 소산 출력은 다음과 같다.

    Ė  =  (21/2) · (k₂/Q) · (G M_p² R⁵ n e²) / a⁶

여기서 평균운동은 `n = √(G(M_p + m)/a³) ≈ √(G M_p / a³)`이다(`m ≪ M_p`일 때).
`n`을 대입하면 가파른 거리 의존성이 명시적으로 드러난다.

    Ė  ∝  (k₂/Q) · R⁵ · e² · M_p^(3/2) · a^(−15/2)

각 항은 다음과 같다.

| Symbol | Meaning | Where it comes from |
|---|---|---|
| `k₂` | degree-2 tidal Love number (potential response of the body) | interior structure (§5) |
| `Q` | tidal quality factor (1/Q ≈ phase lag = fraction of energy lost per cycle) | rheology (§5) |
| `G` | gravitational constant | – |
| `M_p` | mass of the **perturber** (the planet, for a moon; the star, for a planet) | DB |
| `R` | radius of the **heated** body | DB |
| `n` | mean motion = `2π/P_orb` = `√(G M_p / a³)` | orbit |
| `e` | orbital eccentricity | orbit (must be *maintained*, §4) |
| `a` | semi-major axis of the heated body's orbit about the perturber | orbit |

`(21/2)` 선행인자는 동주기·경사 0·작은 이심률 경우(조석 퍼텐셜 전개의 선행 `e²` 항)에
대한 표준값이다. `k₂/Q` 묶음은 바디의 물질이 기여하는 부분이고, 나머지는 모두 기하와
섭동체 질량이다.

실무에서는 두 가지 동등한 축약이 유용하다. **(a)** 지표 열플럭스는 `F = Ė / (4πR²)`이며,
화산활동/융해를 판가름하는 값이다(§6). **(b)** `k₂/Q`, `e`, `R`을 고정하면 `Ė ∝ a^(−15/2)`,
즉 **궤도거리가 2배가 되면 가열이 약 180배 변한다.** 이 `a⁻⁷·⁵` 붕괴가 지배적 거동이며,
§3에서 다룰 혹독한 교훈의 핵심이다.

fixed-Q 형식은 *1차* 도구다. `k₂`와 `Q`를 상수로 다루는데, 이는 실제 물질 응답의 온도·진동수
의존성을 전부 가려 버린다. 그것이 깨지는 경우와 그 자리를 무엇이 대체하는지는 §5에서 다룬다.

---

## 2. Calibration: 공식이 Io와 Enceladus를 재현한다

이 공식이 믿을 만한 것은 오직 내부 출력이 실제로 *측정된* 두 바디를 재현하기 때문이다.
이 관측값들이 `k₂/Q`를 calibration한다.

| Body | Perturber | a (R_p) | e (forced) | observed Ė | observed flux | formula reproduces with |
|---|---|---|---|---|---|---|
| **Io** | Jupiter | ~5.9 R_J | ~0.0041 | ~0.6–1.6 ×10¹⁴ W | ~2 W/m² (global) | k₂/Q ~ 0.015 (k₂≈0.3, Q≈20) |
| **Enceladus** | Saturn | ~3.95 R_Sat | ~0.0047 | ~5–16 GW (≈10¹⁰ W) | ~5 GW from the SPT | k₂/Q ~ 0.002–0.01 (soft ice + ocean) |

- **Io**는 calibration 앵커다. 적외선 복사측정(Veeder+ 1994 [`1994JGR....9917095V`](https://ui.adsabs.harvard.edu/abs/1994JGR....9917095V); Veeder+ 2012
  [`2012Icar..219..701V`](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V))은 전구 열출력을 ~10¹⁴ W, 즉 지표 플럭스 ~2 W/m²로 잡는다. 지구의
  ~0.08 W/m²보다 한 자릿수 높다. Lainey+ 2009([`2009Natur.459..957L`](https://ui.adsabs.harvard.edu/abs/2009Natur.459..957L))는 천체측정으로 Io–Jupiter
  계에서 *활동적인* 강한 소산을 확인해 고리를 닫았다. 공식이 요구하는 소산이 곧 궤도가 보여
  주는 소산이라는 것이다. Io의 `a`, `e`, `R`, `M_J`와 `k₂/Q ≈ 0.015`를 넣으면 공식은 ~10¹⁴ W를
  돌려준다. ✓
- **Enceladus**는 저질량 바디 앵커다. 카시니는 활동적인 남극 열 이상과 플룸을 발견했고(Spencer+ 2006
  [`2006Sci...311.1401S`](https://ui.adsabs.harvard.edu/abs/2006Sci...311.1401S)), Howett+ 2011([`2011JGRE..116.3003H`](https://ui.adsabs.harvard.edu/abs/2011JGRE..116.3003H))은 남극 지형에서 ~15.8 GW를
  측정했으며, 내인성 총량은 수 GW(~10¹⁰ W) 수준이다. Nimmo+ 2007([`2007Natur.447..289N`](https://ui.adsabs.harvard.edu/abs/2007Natur.447..289N))은
  타이거 스트라이프를 따라 일어나는 전단 가열을 플룸의 원인으로 본다. Enceladus는 아주
  작아서(`R ≈ 252 km`) 그 `R⁵`이 Io의 ~10⁹배 작은데, soft-ice + ocean `k₂/Q`(Meyer & Wisdom
  2007 [`2007Icar..188..535M`](https://ui.adsabs.harvard.edu/abs/2007Icar..188..535M))를 쓰면 공식이 ~GW 규모를 돌려준다. ✓

calibration은 **Ė에서 네 자릿수**(10¹⁴ → 10¹⁰ W)와 반경에서 ~25배를 가로지르며, 동일한
하나의 공식이 양쪽을 모두 포괄한다. 차수 수준 레시피가 건전하다는 증거가 바로 이것이다,
*단* `k₂/Q`를 올바른 바디 분류(§5)에 맞게 고르고, 이심률이 실제로 유지된다(§4)는 전제 아래서다.

---

## 3. a⁻⁷·⁵ 거리 게이트 (혹독한 교훈)

**한 절만 읽는다면 바로 이 절이다.** `Ė ∝ a^(−15/2)`이기 때문에 궤도거리가 다른 모든 손잡이를
압도한다. 아무리 유리한 `e`, `k₂/Q`, 공명을 갖다 대도 너무 멀리 도는 바디는 구제할 수 없다.

Io의 `k₂/Q`, `e`, `R`과 섭동체 Jupiter를 고정한 채 바디를 바깥으로 옮겨 보자.

| a (R_p) | relative Ė (Io = 1) | absolute scale |
|---|---|---|
| 6 (≈ Io) | 1 | ~10¹⁴ W |
| 10 | ~0.05 | ~10¹³ W |
| 15 | ~0.003 | ~10¹² W |
| 20 | ~5 ×10⁻⁴ | ~10¹¹ W |
| 30 | ~3 ×10⁻⁵ | ~10⁹ W |

**20 R_p에 있는 바디는 같은 바디가 6 R_p에 있을 때보다 조석 출력을 ~2000배 적게 받는다.**
반경을 Io 크기에서 작은 얼음 위성으로 낮추면(`R⁵`이 또 ~10²–10³배 떨어진다) 가열은 **MW
수준**으로 붕괴한다. 얼음을 녹이거나 플룸을 구동하기에는 전혀 무의미한 수준이다(반대로
Enceladus는 *가까운 안쪽*인 ~4 R_Sat에 있기에 252 km 위성이 그래도 GW를 끌어모은다).

**NearStars Chaos의 교훈.** α Cen Phase 4 작업에서, 행성 반경 ~20배에 있는 위성 **A b V(Chaos)**는
바로 이 계산으로 **~MW 수준**의 조석 출력만 받는다는 것이 드러났다. 지하 바다나 빙화산
플룸을 지탱하기에는 *몇 자릿수나 부족한* 양이다. 유리한 서사(공명, 무른 내부)로도 `a⁻⁷·⁵`
게이트를 넘길 수 없었다. 그래서 Chaos의 플룸은 Phase 4 보드에서 **아트 우선의 문서화된
divergence**로 받아들였다. 물리적으로 도출된 피처가 명시적으로 *아니다*. 반면 가까운
안쪽(R_p 몇 배)에 놓인 위성은 게이트를 통과하고 그 가열은 *도출 가능*하다.

이 게이트는 상세 추정에 앞서 한 줄로 정신을 차리게 하는 점검이다. **`a`를 섭동체 반경 단위로
계산하라.** ~10–15 R_p를 넘으면, 거대하고 이심률이 크며 공명으로 펌핑되는 바디가 아닌 한
가열은 무의미할 것으로 보면 된다. 그래도 디자인이 거기에 피처를 원한다면, 도출이 아니라
문서화된 divergence로 표시하면 된다.

---

## 4. 이심률 유지 요건

조석가열은 `e²`로 돌아간다. 그런데 조석 소산은 **`e`를 감쇠시킨다.** 바디를 데우는 바로 그
마찰이 궤도를 원형화하며, 그 시간척도가 시스템 나이보다 훨씬 짧을 수도 있다. 따라서 홀로
방치된 바디는 *일시적으로* 데워졌다가 `e → 0`이 되면서 가열이 **꺼진다.** 지속적인 가열을
위해서는 `e`를 계속 펌핑해 주는 무언가가 필요하다.

그 펌프는 거의 언제나 다른 바디와의 **평균운동 공명**이다.

- **Io**: Laplace 공명(Io:Europa:Ganymede 1:2:4). Yoder 1979([`1979Natur.279..767Y`](https://ui.adsabs.harvard.edu/abs/1979Natur.279..767Y))는
  Io의 조석가열이 이 공명을 *구동하고 잠그며*, 그 공명이 다시 감쇠에 맞서 Io의 `e ≈ 0.0041`을
  강제하는 과정을 보였다. 이것이 없으면 Io의 궤도는 원형화되고 화산활동도 사그라들 것이다.
- **Enceladus**는 Dione와의 2:1 평균운동 공명이 `e ≈ 0.0047`을 강제한다(Meyer & Wisdom 2007
  [`2007Icar..188..535M`](https://ui.adsabs.harvard.edu/abs/2007Icar..188..535M); Meyer & Wisdom 2008 [`2008Icar..193..213M`](https://ui.adsabs.harvard.edu/abs/2008Icar..193..213M)). 작은 위성을 지질학적으로
  살아 있게 만드는 것이 바로 이 공명이다.

실무 규칙은 이렇다. **지속적인 조석가열을 주장하려면 `e`를 유지하는 공명(또는 다른 강제력)을
명시하라.** 측정/가정된 `e`만 있고 유지 기구가 없는 단독 위성은 단지 원형화 도중일 수도 있다.
그 `e`(따라서 그 가열)는 정상상태가 아니라 스냅숏일 뿐이다. NearStars 합성계에서, *계속* 뜨거워야
하는 위성을 정당화하는 물리적으로 정직한 방법은 다중 위성 공명 사슬(Laplace식)이다. 단독 이심
위성은 원형화 시간이 시스템 나이를 넘지 않는 한 일시적인 것으로 표시해야 한다.

---

## 5. 유효 영역: 바디 분류별 k₂/Q와 유변학 문제

`k₂/Q`는 **지배적 불확실성**이다. 바디 종류에 걸쳐 ~3 자릿수를 가로지르며, 정작 다루는 바디에
대해서는 측정된 경우가 드물다. 분류별로 골라야 한다.

| Class | k₂ | Q | k₂/Q | notes |
|---|---|---|---|---|
| **Rocky / silicate** (Io-like, terrestrial) | ~0.1–0.3 | ~10–100 | ~10⁻³–10⁻² | strongly T-dependent; a partially molten interior raises k₂ and lowers Q (more dissipation) |
| **Icy + subsurface ocean** (Enceladus, Europa) | ~0.01–0.1 | ~1–100 | ~10⁻⁴–10⁻² | an ocean decouples the shell and can *raise* dissipation enormously; very model-dependent |
| **Gas / ice giant** | ~0.1–0.6 | ~10³–10⁵ | ~10⁻⁵–10⁻³ | high Q (low dissipation per cycle); relevant when the *giant itself* is the heated body close to a star |

fixed-Q 레시피가 애초에 옳은 도구인지를 결정하는 네 가지 영역/주의사항은 다음과 같다.

1. **암석질 동주기 바디, 작은 이심률**: 레시피의 본거지다(Peale+ 1979, Io로 calibration).
   암석질 `k₂/Q` 대역을 쓰고 차수로 보고하면 된다.
2. **바다를 품은 얼음 바디**: fixed-Q 값은 *하한*이다. 바다로 디커플된 껍질은 균질-Q 추정보다
   훨씬 크게 소산할 수 있으므로, 낮은 fixed-Q `Ė`라고 해서 활동적인 바다를 **배제하지 못한다.**
   위성을 죽었다고 선언하기 전에 점탄성 모형으로 교차 점검하라.
3. **점탄성 / 유변학 영역**: §1의 `Ė`가 융해 또는 바다 임계값 근처에 있을 때 fixed-Q 답은
   믿을 수 없으며, 진동수·온도 의존 **Maxwell / Andrade** 처리로 대체해야 한다. Segatz+ 1988
   ([`1988Icar...75..187S`](https://ui.adsabs.harvard.edu/abs/1988Icar...75..187S), 점탄성 Io 모형의 효시), Henning, O'Connell & Sasselov 2009
   ([`2009ApJ...707.1000H`](https://ui.adsabs.harvard.edu/abs/2009ApJ...707.1000H), 조석가열되는 지구형 외계행성), Henning & Hurford 2014
   ([`2014ApJ...789...30H`](https://ui.adsabs.harvard.edu/abs/2014ApJ...789...30H), 다층), Renaud & Henning 2018([`2018ApJ...857...98R`](https://ui.adsabs.harvard.edu/abs/2018ApJ...857...98R), Andrade 대 Maxwell,
   가열이 **큰 인자**로, 흔히 10배 이상 달라질 수 있고 공명 내부 온도에서 정점을 이룬다) 등이다.
   fixed-Q와 Andrade 답은 한 자릿수까지 어긋날 수 있는데, 그 간극이 *곧* 오차 막대다.
4. **스핀-궤도 / 비동주기, 또는 스핀-궤도 공명 근처**: `(21/2)e²` 선행 항이 틀린다. Efroimsky
   & Makarov의 진동수 의존 형식론을 쓴다(Efroimsky & Williams 2012 [`2012CeMDA.112..283E`](https://ui.adsabs.harvard.edu/abs/2012CeMDA.112..283E)).
   주로 아직 고정되지 *않은* 바디, 즉 문서 맨 위에서 표시한 locking 문서의 영역에 해당한다.

NearStars에서의 실무 자세는 이렇다. fixed-Q 공식을 분류 `k₂/Q` 대역과 함께 쓰고, **범위**(점값이
아니라)를 보고하며, 답이 화산활동/바다 임계값 근처에 떨어지면 점탄성 문헌에 맡기고 과장 대신
불확실성을 넓힌다.

---

## 6. 결과 판정: 화산활동 / 바다 / 플룸

§1–§5는 *출력이 얼마나 생성되는가*에 답한다. 그것은 문제의 절반일 뿐이다. 그 출력은
**지표를 통해 빠져나가야** 하며, 몇 W/m²를 넘어서면 구속 조건은 생성이 아니라 배출이 된다.
§6.1은 빠른 판정 표이고, §6.2–§6.5는 배출 쪽이다. 설계된 고플럭스 바디가 애초에 물리적으로
가능한지를 결정하는 것이 바로 이 배출 쪽이다.

### 6.1 플럭스 → 영역 표

`Ė`를 **지표 열플럭스** `F = Ė / (4πR²)`로 변환해 임계값과 비교한다(예리한 경계선이 아니라
지침이다).

| Surface flux F | regime | analog |
|---|---|---|
| ≳ 1 W/m² | vigorous silicate volcanism, possible magma ocean | Io (~2 W/m²) |
| ~0.1–1 W/m² | active resurfacing, episodic volcanism | active icy/rocky worlds |
| ~0.01–0.1 W/m² | enough to maintain a subsurface ocean under an ice shell | Enceladus SPT, Europa |
| ≲ 10⁻³ W/m² | geologically dead; no ocean, no plumes from tides alone | far/airless moons |

순서는 이렇다. **(1)** `a`를 R_p 단위로 계산해 §3 게이트를 먼저 적용한다(`a ≳ 10–15 R_p`이고
바디가 작으면 답은 거의 확실히 "죽음"이므로 거기서 멈춘다). **(2)** `e`가 *유지*되는지 확인한다(§4).
공명을 명시하거나, 가열을 일시적인 것으로 표시한다. **(3)** 분류 `k₂/Q` 대역을 고르고(§5) `Ė`와
`F`를 범위로 계산한다. **(4)** `F`를 표에 대응시킨다. 임계값 근처에 떨어지면 확정 전에 점탄성
교차 점검(§5 영역 3)으로 격상한다. **(5)** 선택한 `k₂/Q`, 유지 공명, 그 결과인 `F` 범위를 Phase 4
보드에 기록한다. 그리고 아트가 "죽음" 판정을 뒤집는 경우, 조용한 격상이 아니라 **문서화된
divergence**로 표시한다. **(6)** `F ≳ 1 W/m²`이면 "격렬한 화산활동"이라는 판정으로 점검이
끝나는 게 아니다. §6.2–§6.4의 배출 시험까지 돌려야 하며, 크기를 과하게 잡은 설계가 무너지는
지점이 바로 여기다.

조석가열은 여러 열원(방사성, 강착, 원시) 가운데 하나일 뿐임에 유의한다. 지구 질량 바디라면
방사성 가열만으로 ~0.08 W/m²이며, 조석가열은 그것을 *넘어설* 때 의미를 갖는다. 작은 얼음
위성에서는 방사성 열이 무시할 만하고 조석이 사실상 유일한 손잡이다. 그래서 거리 게이트가
그들에게 그토록 결정적인 것이다.

### 6.2 열은 실제로 어떻게 빠져나가는가: 세 모드의 사다리

바디의 지표가 내부열을 넘길 수 있는 길은 정확히 세 가지이며, 그 용량은 서로 **네 자릿수**
차이가 난다. 어느 모드에 놓이는지는 플럭스 자체가 정하므로, 모드는 자유로운 선택이 아니라
§6.1의 산출물이다.

| Mode | Mechanism | Capacity | Anchor body |
|---|---|---|---|
| **Plate tectonics** | the lid itself is recycled | ~0.09 W/m² | Earth, **92.1 mW/m²** (47±2 TW from 38,347 measurements, [`2010SolE....1....5D`](https://ui.adsabs.harvard.edu/abs/2010SolE....1....5D)) |
| **Stagnant lid** | conduction through an immobile lid | ceiling **10–30 mW/m²** | Venus 10–20, Mars 15–30 ([`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R)) |
| **Heat pipe** | melt migrates through the lid and erupts | ≥ ~2.5 W/m², no firm upper bound | Io; early Earth ([`2019JGRE..124..114K`](https://ui.adsabs.harvard.edu/abs/2019JGRE..124..114K)) |

~0.1 W/m²를 넘는 조석가열 바디에 대해 결정적인 사실은 이것이다. **전도는 선택지가 아니다.**
Reese, Solomatov & Moresi 1998([`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R))은 광범위한 융해가
시작되기 전 정체뚜껑(stagnant-lid) 전도 천장을 10–30 mW/m²로 잡는다. Io보다 두 자릿수 낮은
값이다. Moore 2003([`2003JGRE..108.5096M`](https://ui.adsabs.harvard.edu/abs/2003JGRE..108.5096M))은 고체상 대류조차 Io의 플럭스에
*"falls an order of magnitude short"*임을 보인다. 남는 것은 **이류**다. 멜트가 분리되어 상승하며
잠열을 지표까지 실어 나른다.

지배 방정식이 되는 지표 에너지 균형은 Spencer, Katz & Hewitt 2020
([arXiv:2003.08287](https://arxiv.org/abs/2003.08287))이며, 그 eq. 33은 소산률 `Ψ`를 곧바로
표면 재포장(resurfacing) 속도로 변환한다.

    q_s  =  Ψ / [ 4πR² ( ρL + ρ c (T_m − T_s) ) ]

여기서 `ρ`는 밀도, `L`은 융해 잠열, `c`는 비열, `T_m`은 융해 온도, `T_s`는 지표 온도다. 전도는
무시할 만하기에 **균형식에서 아예 빠진다.** 논문의 Io 기준해(Table 1: ρ=3000 kg/m³,
L=4×10⁵ J/kg, c=1200 J/kg/K, T_m=1500 K, T_s=150 K, Ψ=10¹⁴ W)는 **지표 열수송의 99.5 %가
화산성**이라는 결과와, Io의 관측값과 일치하는 1.25 cm/yr의 재포장 속도, 그리고 **80 km의 탄성
두께**를 준다. 이어지는 eqs. 34–35는 분출된 멜트와 관입된 멜트를 갈라놓는데, **Io 마그마의
~80 %는 분출되지 않고 지각 내부에 정착한다.** 열 예산을 눈에 보이는 용암으로 환산할 때 중요한
지점이다. 논문은 eq. 10을 재사용하라고 명시적으로 권한다 — *"provides a means of estimating
eruption rates for other tidally heated lava-worlds, utilising their tidal heating rate, size,
and surface temperature"* — 그러니 합성 바디에 쓸 때도 유비가 아니라 공인된 공식이다. 뚜껑
두께, 맨틀 온도, 잔여 전도 플럭스는 Kankanamge & Moore 2019([`2019JGRE..124..114K`](https://ui.adsabs.harvard.edu/abs/2019JGRE..124..114K),
doi 10.1029/2018JE005800)의 heat-pipe 파라미터화가 주며, 수치 시뮬레이션에 대해 15 % 이내로
검증되어 있다.

**직관에 반하는 귀결이 있다. 높은 플럭스는 얇은 뚜껑이 아니라 두꺼운 뚜껑을 만든다.** heat
piping은 *"produces a thick, cold, and strong lithosphere"*(Moore & Webb 2017,
[`2017E&PSL.474...13M`](https://ui.adsabs.harvard.edu/abs/2017E%26PSL.474...13M))하며, O'Reilly & Davies 1981
([`1981GeoRL...8..313O`](https://ui.adsabs.harvard.edu/abs/1981GeoRL...8..313O))은 이 기구를 제목에서부터 그렇게 불렀다 —
*a mechanism allowing a **thick** lithosphere*. 전도만으로는 Io의 리소스피어가 ~5 km까지 얇아져야
하지만, 이류가 있으면 두꺼워질 수 있다. 관측도 같은 방향이다. 산의 부피로부터 ≥12 km
([`2003JGRE..108.5093J`](https://ui.adsabs.harvard.edu/abs/2003JGRE..108.5093J)), 산의 분포로부터 ≥30 km
([`1998Icar..135..146C`](https://ui.adsabs.harvard.edu/abs/1998Icar..135..146C)), 모형에서 35–80 km이며, 이런 뚜껑은 전도로는
Io 플럭스의 **3–7 %**만 통과시킨다.

그래서 설계 규칙은 직관의 반대가 된다. **열을 올려서 더 두꺼운 지각을 살 수는 없고, 고플럭스
바디가 센티미터 규모의 지각을 갖는 것도 아니다.** 두껍고 차가운 뚜껑에 불연속적인 멜트 통로가
뚫려 있으며, 출력의 사실상 전부를 *그 통로들*이 실어 내야 한다.

### 6.3 평원은 배출구가 아니다

> **적용 범위 — 뚜껑형 천체에 한한다.** 이 절은 내부열이 고체 뚜껑을 뚫고 나가야 하는
> 천체를 다룬다. 전 지구 바다도 없고, 열을 지구 규모로 실어 나를 만큼 두꺼운 대기도 없는
> 경우다. **전 지구 유체층**이 있으면 그 층이 내부 플럭스를 재분배하므로 아래 논증은
> 통째로 무효다. 그때 조석 항은
> [`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md)를 통해
> 천체의 전 지구 에너지 수지로 들어간다. 둘 중 어느 쪽인지는 숫자가 아니라 **선택자**이니,
> 이 절을 더 읽기 전에 먼저 정하라. Dante(규산염, 대기 없음)는 이 갈래를 타고,
> 1.1기압 아래 표면 절반이 바다인 Alpha Centauri A b III(Pandora)는 반대쪽을 탄다.

뚜껑이 ~0.1 W/m²를 전도한다면, 화산 중심들 사이의 지형은 열적으로 **불활성**이다. 그 지형은
외부 예산(별빛, 위성이라면 모행성의 기여까지 —
[`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md) 참고)과 복사 평형을
이루는 온도에 머물며, 내부열은 조금도 나르지 않는다.

Io가 이를 직접 확인해 준다. 배경 평원은 **110–130 K이고 순전히 일사로 결정된다.** Bond
알베도 0.56, 열관성 250 MKS의 서리 모형이 22년치 데이터를 맞추고
([arXiv:2405.19253](https://arxiv.org/abs/2405.19253), 적도 서리 106–116 K), 핫스팟 사이의
내인성 기여는 **<1 W/m²**다([`2004Icar..169..127R`](https://ui.adsabs.harvard.edu/abs/2004Icar..169..127R)). 평균 2.5 W/m²를
복사하는 바디인데도 평원은 차갑다.

따라서 열은 지표의 아주 작은 일부에 집중된다.

- 활동 화산이 Io 표면의 **약 2 %**를 차지한다([arXiv:2310.12382](https://arxiv.org/abs/2310.12382)).
- **열류의 50 %가 표면의 1.2 %에서 나온다**([`2012Icar..219..701V`](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V)).
- patera 바닥은 표면의 2.5 %지만 검출된 핫스팟의 **64 %**를 품는다
  ([`2011Icar..214...91W`](https://ui.adsabs.harvard.edu/abs/2011Icar..214...91W)).

문헌은 이 형태를 Io만이 아니라 외계 바디에도 예측한다. Henning, O'Connell & Sasselov 2009
([arXiv:0912.1907](https://arxiv.org/abs/0912.1907))는 조석만으로 *지표* 마그마 바다가 열리기는
어렵다고 보며(*"half a million TW or more"*, 지구 반경 바디에서 ≈980 W/m²가 필요하다),
*"thin-layer global resurfacing as on Io is unlikely for viscous lavas. This supports the notion of
searching for small radiantly cooled hotspots on supertidal exoplanets."*라고 정리한다.

**Phase 4 작업에 주는 귀결이 둘 있다.** (a) 따뜻한 평원 온도는 아트 선택이 아니다. 뚜껑이
미터 두께라는 주장이고, 그런 뚜껑은 지형을 지탱하지 못한다. 평원은 외부 예산으로 정하고 그대로
둔다. (b) 보존 법칙은 여전히 구속한다. 면적가중 `σT⁴` 평균이 `F`와 같아야 하므로, 열을 집중시키면
핫스팟은 *더 뜨거워진다.* 배출 점검이 통과해야 하는 값은 평원이 아니라 그 핫스팟의 온도다.

### 6.4 용암호 용량 시험 (그리고 두 분모의 함정)

용암호가 그 전부를 실어 내는 만큼, 고플럭스 설계의 시험은 산수 한 줄이다.

    required areal flux  =  F / (lake area fraction)

그리고 이 값이 실제 용암호의 **측정된** 용량 안에 들어와야 한다.

**먼저 함정부터.** 문헌에는 서로 다른 두 분모가 쓰이며 둘은 두 자릿수 차이가 난다. patera의
출력을 *지질학적 바닥 면적*으로 나누면 지각이 지배하는 ~300 K 값이 나오고, *피팅된 등가 흑체
면적*으로 나누면 지각 보정된 600–940 K의 대용값이 나온다. **절대 섞지 말고, 인용한 플럭스가
어느 쪽 분모인지 늘 밝혀야 한다.** Loki Patera가 그 간극을 구체적으로 보여 준다.
9.6×10¹² W([`2012Icar..219..701V`](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V))를 21,500 km²의 바닥
([`2017Natur.545..199D`](https://ui.adsabs.harvard.edu/abs/2017Natur.545..199D))으로 나누면 **446–465 W/m², 즉 298–301 K**이며
— JIRAM의 지각 휘도온도 270–355 K([arXiv:2410.10686](https://arxiv.org/abs/2410.10686))가 독립적으로
이를 뒷받침한다 — 반면 Pele의 *피팅된* 6.5 km²는 **940 K에서 44.3 kW/m²**를 준다
([`2016Icar..264..198D`](https://ui.adsabs.harvard.edu/abs/2016Icar..264..198D)).

**천장.** 지각이 없는 맨멜트는 `σ T_erupt⁴`로 복사한다. Io의 분출 온도는 ~1600 °C에서
**~1340 °C = 1613 K**로 하향 수정되었고([`2007Icar..192..491K`](https://ui.adsabs.harvard.edu/abs/2007Icar..192..491K)), 이는
**384 kW/m²**에 해당한다. 절대적인 상한이며, **관측된 용암호는 어느 것도 근접하지 못한다.**
최고 기록이 그 59 %다.

| Object | Area | Areal flux | T_eff | Note |
|---|---|---|---|---|
| Nyamuragira 2014 | 900 m² | **111 kW/m²** | 1,199 K | observed MAXIMUM ([`2023FrEaS..1140199C`](https://ui.adsabs.harvard.edu/abs/2023FrEaS..1140199C) Table 1) |
| Kilauea 2008 / Ambrym 2015 | 300 / 4,000 m² | 100 kW/m² | 1,167 K | same table |
| Erta Ale (FLIR) | ~1,000 m² | 45–76 kW/m² | 944–1,076 K | [`2008GGG.....912008S`](https://ui.adsabs.harvard.edu/abs/2008GGG.....912008S) |
| Nyiragongo 2017 | 50,000 m² | 24 kW/m² | 817 K | large ⇒ crusted |
| Kilauea 2015 | 30,000 m² | 23.3 kW/m² | 811 K | large ⇒ crusted |
| Erebus Ray Lake | ~1,400 m² | 21–25 kW/m² | 784–815 K | [`2008JVGR..177..695C`](https://ui.adsabs.harvard.edu/abs/2008JVGR..177..695C); lidar area 535–1,709 m² ([`2015JVGR..295...43J`](https://ui.adsabs.harvard.edu/abs/2015JVGR..295...43J)) |
| Kupaianaha stages 1 / 3 | sub-m² | 22 / 4.9 kW/m² | 789 / 542 K | [`1993JGR....98.6461F`](https://ui.adsabs.harvard.edu/abs/1993JGR....98.6461F) |

384 kW/m²에 아무것도 도달하지 못하는 이유는 **지각**이다. 지각 없는 면적 비율은 10⁻⁵(정온,
두꺼운 지각)에서 ~0.3(격렬)까지 걸친다. 조직적인 용암호는 *">80 % covered by a cooling skin"*인
반면 혼돈스러운 용암호는 *"mostly crust-free and incandescent"*이다(Campion & Coppola 2023,
[`2019JVGR..381...16L`](https://ui.adsabs.harvard.edu/abs/2019JVGR..381...16L) 인용). Erta Ale은 흔히 90 %를 넘는 지각을
보이고 Marum은 ≤30 %다([`2016JVGR..322..105R`](https://ui.adsabs.harvard.edu/abs/2016JVGR..322..105R)).

표의 추세도 눈여겨볼 만하다. **큰 용암호일수록 지각이 두껍고, 따라서 단위 면적당 온도가 낮다.**
이는 용량 천장이 아니라 공급 제한이다. 표면 속도는 가스 플럭스와 용암호 면적과 상관하고
([`2019JVGR..381...16L`](https://ui.adsabs.harvard.edu/abs/2019JVGR..381...16L)) 지각 수명은 이동 속도가 커질수록 짧아지므로
([`2005JVGR..142..207H`](https://ui.adsabs.harvard.edu/abs/2005JVGR..142..207H)), 고플럭스의 큰 용암호를 원리적으로 금지하지는
않는다. 다만 정직한 시험은 상한이 아니라 대역이라는 뜻이다.

> **배출 시험.** `F / f_lake`가 측정된 대역 **≲111 kW/m²** 안에 들어가야 하고, 384 kW/m²의
> 맨멜트 천장보다 넉넉히 아래여야 한다. 그보다 더 필요한 설계는 용암호 전 면적에 지각 없는
> 노출 멜트를 깔아 달라는 요구이며, 관측된 어떤 것도 그렇지 않다.

거꾸로 풀면 이 관계는 크기에서 용암호 면적을, 또는 용암호 면적에서 크기를 고정해 준다. Io
자체로 검산해 보면, 면적의 ~0.05 %를 통해 2.5 W/m²를 내보내려면 5.0 kW/m², 즉 **545 K**가
필요하다. 관측 대역 한가운데이므로, 이 관계는 어떤 NearStars 바디에 맞춰 튜닝된 것이 아니다.

### 6.5 super-Io 천장: 용암 위성은 얼마나 클 수 있는가

Io를 얼마나 넘어선 바디까지 지속 가능한지는 이미 문헌이 한계를 잡아 두었다. **Io보다 1–3
자릿수 위, 즉 25–2,500 W/m²**이며, 지속 가능한 쪽 가지는 전지구적 멜트가 아니라 두껍고 차가운
뚜껑을 통한 heat piping이다([`2021PSJ.....2..119R`](https://ui.adsabs.harvard.edu/abs/2021PSJ.....2..119R),
[arXiv:2305.03410](https://arxiv.org/abs/2305.03410)이 이를 채택). 마그마 바다에는 ~0.45를 넘는
멜트 분율이 필요한데 그 값 자체도 논쟁 중이며(0.30 / 0.45 / 0.50), 두 모드를 가르는 **W/m²
경계는 발표된 바가 없다.** 실제 기준이 멜트 분율이고, 플럭스 임계값은 인용이 아니라 환산일
뿐이기 때문이다.

`Ė ∝ R⁵`인데 면적은 `R²`에 비례하므로, 밀도가 같다면 **지표 플럭스는 `R³`로 스케일링된다.**
위성 반경을 2배로 하면 플럭스가 8배가 되고, 필요한 용암호 플럭스도 함께 8배가 된다. 그래서
크기가 배출 쪽에서 가장 강한 손잡이이며, 위의 배출 시험은 곧 단단한 반경 천장으로 바뀐다.

**워크드 예제 — Dante(Alpha Centauri A b I), 2026-08-21.** 이 바디는 처음 900 km로 초안이
잡혔고, 그것을 기각한 것이 바로 배출 시험이다. 밀도를 2,620 kg/m³로 고정하고 초안값
900 km / Io의 1,200배 / 11,500 W/m²에서 스케일링하면 이렇다.

| R | mass (kg) | output | F | 5 %-lake required areal flux | verdict |
|---|---|---|---|---|---|
| 900 km (drafted) | 8.0×10²¹ | 1,200× Io | 11,500 W/m² | 230 kW/m² | **2.1× the observed max — impossible** |
| 714 km | 3.99×10²¹ | 377× | 5,742 W/m² | 114.8 kW/m² | exactly at the record max |
| **521 km (adopted)** | **1.552×10²¹** | **78×** | **2,231 W/m²** | **44.6 kW/m²** | **Erta Ale class — inside the band** |
| 450 km | 1.0×10²¹ | 38× | 1,438 W/m² | 28.8 kW/m² | Erebus class |

900 km에서 이 설계는 센티미터 규모의 지각과 녹은 암석보다 더 뜨거운 용암호를 암묵적으로
요구하고 있었다. §6.2는 지각이 얇을 수 없다고 하고, §6.4는 용암호가 그만큼 뜨거울 수 없다고
한다. **521 km**는 둘을 모두 만족하고, 발표된 super-Io 봉투 안에 들어가며(2,231 < 2,500 W/m²,
이 값이 반경을 541 km로 제한한다), 면적 평균 452 K를 주고, 평원은 외부 예산이 정하는 223 K에
남겨 둔다. 원소 황은 안정하지만 SO₂ 서리는 안정하지 않을 만큼 차가운 온도다(서리에는 ≤120 K가
필요하고([`1988Icar...75..450M`](https://ui.adsabs.harvard.edu/abs/1988Icar...75..450M)), 황은 ~500 K에서 진공 끓음을 시작한다).
표면이 흰색이 아니라 황색조로 읽히는 이유가 여기 있다.

이 점검을 다시 돌리는 비용을 낮춰 주는 부산물 둘은 기록해 둘 만하다.

- **밀도가 같다면 `J₂`와 `C₂₂`는 반경과 무관하다.** 조석 형상 파라미터는
  `q = M_p / ((4/3)πρa³)`이며, 가열되는 바디 자신의 반경은 여기에 등장하지 않는다. 위성 크기를
  바꾸면 질량·중력·플럭스는 바뀌지만, 편평도나 삼축 *비율*, 자전 주기는 **바뀌지 않는다.**
- 절대적인 기복은 스케일링된다. Dante의 `J₂ = 0.039` / `C₂₂ = 0.0118`은
  `a = 549.6`, `b = 512.7`, `c = 500.7 km`를 주어 sub-planet에서 극까지 기복이 **48.9 km**다.
  구형 해수면을 부여했을 때 협곡 벽에 쓸 수 있는 높이 예산이다.

---

## 7. 워크드 예제

**Io (calibration).** `M_p = M_Jupiter`, `R = 1822 km`, `a = 421,700 km`(~5.9 R_J),
`e = 0.0041`(Laplace 유지), 암석질 `k₂/Q ≈ 0.015`. fixed-Q 공식은 `Ė ~ 10¹⁴ W`, `F ~ 2 W/m²`를
돌려주며 Veeder+ 2012와 일치한다. 판정: 격렬한 규산염 화산활동, **도출됨**(공명 명시, 플럭스
측정). 다른 모든 추정이 이 값에 맞춰 스케일링되는 앵커다.

**Enceladus (저질량 바디 calibration).** `M_p = M_Saturn`, `R = 252 km`, `a ≈ 238,000 km`
(~3.95 R_Sat, *가까운 안쪽*), `e = 0.0047`(Dione 2:1), soft-ice + ocean `k₂/Q ~ 10⁻³`. `R⁵`이
Io의 ~10⁹배 작은데도 작은 `a` 덕분에 게이트 안에 머물러, 공식은 남극 지형에서 관측된 ~GW /
~10⁻² W/m²를 돌려준다. 판정: 지하 바다 + 플룸, **도출됨**. 교훈은 *가까움이 큼을 이긴다*:
4 R_p의 작은 위성이 20 R_p의 큰 위성을 능가한다.

**α Cen 적용: 가까움 대 멂(프로젝트 사례).** α Cen Phase 4 위성들을 정성적으로 다룬다(보드
값이며 여기서 재현하지 않는다).
- **가까운 안쪽(R_p 몇 배)**에, `e`를 유지하는 공명 사슬 안에 놓인 위성은 §3 게이트를 통과한다.
  그 `Ė`는 `R`과 `k₂/Q`에 따라 GW–TW 범위로, 활동적인 바다나 화산활동에 충분하다, 보드에
  공명을 명시한 **도출된** 피처다.
- **~20 R_p의 A b V**는 게이트를 통과하지 못한다. `a⁻⁷·⁵` 붕괴가 `Ė`를 **~MW 수준**으로,
  가까운 경우의 ~5×10⁻⁴까지 떨어뜨려 어떤 바다/플룸 임계값보다도 한참 아래다. 따라서 그
  빙화산 플룸은 Phase 4 보드에서 **아트 우선의 문서화된 divergence**다, 레시피가 만든 값이
  아니라 물리를 뒤집는 의도적 선택으로 기록된다. §8 정직함 규칙의 canonical 예시다.

**A b II — 남겨둘 만한 반론 격파 둘(2026-07-28, 보드에서 옮겨옴).** 그럴듯하게 들리지만 이
천체에서 무너진 논거 둘로, 어떤 Io형 사례에도 일반화된다.

1. *"내부열은 높지만 작은 강체 위성은 k₂/Q가 낮아 에너지가 용융 대신 텍토닉으로 흐른다"*는
   두 군데서 틀린다. 낮은 `k₂/Q`는 열의 방향을 바꾸는 게 아니라 애초에 열이 **생성되지 않게**
   한다(Io 배수 값은 이미 특정 `k₂/Q`를 가정하므로, 하나를 낮추면 다른 하나도 내려간다). 그리고
   텍토닉은 열의 배출구가 아니다. 변형에 쓰인 에너지도 결국 복사로 빠져나가므로, 열이 핫스팟에
   얼마나 몰리든 면적가중 `σT⁴` 평균은 보존 법칙이 고정한다. 뜨거운 내부로 차가운 표면을 살 수는
   없다.
2. *"초기 조건에서 이심률을 낮추면 된다."* 훨씬 큰 이웃이 `e`를 강제하는 구조에서는(A b II:
   질량 770배의 A b III, 주기비 2.22) 어떤 초기 `e`를 넣어도 안정성 시뮬이 같은 `e_max`를
   돌려준다 — `e_init` 0.005/0.010/0.020 세 런 모두 0.047~0.064로 복귀했다. 강제 이심률은
   초기 상태가 아니라 배치 구조의 속성이라, 열을 바꾸려면 구조를 옮기는 수밖에 없다.

---

## 8. 정직함과 불확실성

dynamo 문서의 단서들과 같은 정신으로 정리한다.

- **`k₂/Q`가 지배적 미지수다.** 바디 분류에 걸쳐 ~3 자릿수를 가로지르며(§5), 외계 바디에
  대해서는 사실상 측정된 적이 없다. 산출물은 **차수** 추정이니 점값이 아니라 범위로 인용하라.
- **fixed-Q와 점탄성은 큰 인자로 어긋날 수 있다.** 일정-Q 공식(§1)은 1차 도구다. Andrade/Maxwell
  모형(Renaud & Henning 2018)은 `Ė`를 10배 이상 다르게 줄 수 있고, 가열은 fixed-Q 모형이 표현할
  수 없는 공명 내부 온도에서 가파르게 정점을 이룬다. 어떤 임계값 근처에서든 모형 선택이 *곧*
  오차 막대다.
- **`e`는 유지되어야 하며, 그렇지 않으면 가열은 일시적이다**(§4). 공명 없는 스냅숏 `e`는 정상
  열원이 아니다.
- **`a⁻⁷·⁵` 게이트는 조정 손잡이가 아니라 단단한 물리다.** NearStars 바디가 게이트가 금지하는
  피처를 필요로 하는 경우(A b V), 그것은 **문서화된 divergence**다, 물리를 뒤집는 아트로 보드에
  표시할 뿐, 결코 도출인 양 꾸미지 않는다. 이 방법의 가치는 바로, 피처가 물리적으로 *지지되지
  않을* 때를 정직하게 알려 주어 그 우회가 명시적이고 기록된 선택이 되게 한다는 데 있다.

**배출** 쪽(§6.2–§6.5)의 불확실성은 종류가 다르다. 기구는 튼튼하지만 숫자가 지저분하다.

- **방출률(emissivity)은 논쟁 중이고 플럭스가 거기에 비례한다.** Erta Ale 현장에서 측정된 0.74
  ([`2002BVol...64..472B`](https://ui.adsabs.harvard.edu/abs/2002BVol...64..472B))와 Campion & Coppola가 가정한 0.95의
  차이는 §6.4의 모든 면적 플럭스에 **±28 %**로 실린다.
- **복사 출력은 방법에 따라 3배까지 벌어진다.** Erta Ale은 복사만 센 값인지 총 표면열인지에
  따라 5–30, 45–76, 100–400 MW로 제각기 인용된다. 어느 쪽인지 늘 밝혀야 한다. Campion &
  Coppola의 용암호 면적은 사진 기반 추정이므로 그 플럭스는 차수 수준이다.
- **피팅된 단일 흑체 온도는 물리적 온도가 아니다**
  ([arXiv:1906.05426](https://arxiv.org/abs/1906.05426)). 피팅 면적 분모와 짝을 이루는 대용값이며,
  그 용도 외에는 쓸 수 없다.
- **Io 열류의 41–46 %는 출처가 확인되지 않았다**
  ([`2012Icar..219..701V`](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V), [`2015Icar..245..379V`](https://ui.adsabs.harvard.edu/abs/2015Icar..245..379V)). 앵커
  바디조차 핫스팟 목록이 불완전하다는 뜻이다.
- **모드 경계는 W/m²로 인용할 수 없다.** §6.2의 사다리는 발표된 임계값 모음이 아니라 용량
  비교다. 물리적 기준은 멜트 분율이며 그 임계값도 논쟁 중이다(0.30 / 0.45 / 0.50).
- 배출 쪽 출처 몇 개는 arXiv 이전이거나 유료 장벽 뒤에 있어, 전문이 아니라 ADS bibcode와
  초록으로 검증했다. Kankanamge & Moore 2019, Moore 2003, Moore & Webb 2017, Reese 1998,
  Veeder 시리즈, Harris 1999/2005/2008, Lev 2019이다. 이 절을 정량적으로 더 밀어야 할 때 지각
  분율 스케일링을 가장 크게 개선해 줄 셋은 Harris 1999/2008과 Lev 2019이다.

이 방법은 근거를 갖추고 calibration되어 있다(`Ė`에서 4 dex를 가로질러 Io와 Enceladus를 재현한다).
불확실성을 짊어지는 것은 *입력값*(`k₂/Q`, 유변학, `e`의 유지)이다. 신뢰도는 **차수** 수준이며,
거의 모든 경우 화산활동/바다/플룸 판정을 올바르게 내리기에 그것으로 충분하다, `a⁻⁷·⁵` 거리
항이 대개 `k₂/Q`가 문제되기 한참 전에 답을 결정해 버리기 때문이다.

---

## 9. 주석 달린 참고문헌

각 항목: 저자, 연도, 저널, **검증된** arXiv id(없으면 "no arXiv" + bibcode), ADS 인용수, 그리고
기여 한 줄이다.

- **Peale, S. J., Cassen, P. & Reynolds, R. T. (1979)**: *Science* 203, 892.
  **No arXiv** ([`1979Sci...203..892P`](https://ui.adsabs.harvard.edu/abs/1979Sci...203..892P)). Cites: 530. The founding tidal-heating
  paper: the fixed-Q formula and the pre-Voyager prediction that Io would be melted.
  §1.
- **Yoder, C. F. (1979)**: *Nature* 279, 767. **No arXiv** ([`1979Natur.279..767Y`](https://ui.adsabs.harvard.edu/abs/1979Natur.279..767Y)).
  Cites: 178. How tidal heating in Io drives and locks the Galilean (Laplace)
  resonance that maintains Io's eccentricity. §4.
- **Segatz, M. et al. (1988)**: *Icarus* 75, 187. **No arXiv**
  ([`1988Icar...75..187S`](https://ui.adsabs.harvard.edu/abs/1988Icar...75..187S)). Cites: 258. Founding viscoelastic (Maxwell) Io model:
  tidal dissipation, surface heat flow and figure beyond fixed-Q. §5.
- **Veeder, G. J. et al. (1994)**: *JGR* 99, 17095. **No arXiv**
  ([`1994JGR....9917095V`](https://ui.adsabs.harvard.edu/abs/1994JGR....9917095V)). Cites: 217. Io's global heat flow from infrared
  radiometry (~10¹⁴ W): the Io calibration. §2.
- **Spencer, J. R. et al. (2006)**: *Science* 311, 1401. **No arXiv**
  ([`2006Sci...311.1401S`](https://ui.adsabs.harvard.edu/abs/2006Sci...311.1401S)). Cites: 518. Cassini's discovery of Enceladus's active
  south-polar thermal anomaly and plumes. §2.
- **Meyer, J. & Wisdom, J. (2007)**: *Icarus* 188, 535. **No arXiv**
  ([`2007Icar..188..535M`](https://ui.adsabs.harvard.edu/abs/2007Icar..188..535M)). Cites: 152. Tidal heating in Enceladus and the
  Enceladus–Dione 2:1 resonance maintaining its eccentricity. §2, §4.
- **Nimmo, F. et al. (2007)**: *Nature* 447, 289. **No arXiv**
  ([`2007Natur.447..289N`](https://ui.adsabs.harvard.edu/abs/2007Natur.447..289N)). Cites: 239. Shear heating along the tiger stripes as the
  origin of Enceladus's plumes and heat flux. §2.
- **Jackson, B., Barnes, R. & Greenberg, R. (2008)**: *ApJ* 681, 1631.
  **[arXiv:0803.0026](https://arxiv.org/abs/0803.0026).** Cites: 155. "Tidal Heating of Extrasolar Planets": applies
  the fixed-Q heating formula to close-in exoplanets and its surface-condition
  magnitude. §1, §3. (Companion: Jackson+ 2008 *ApJ* 678, 1396, **[arXiv:0802.1543](https://arxiv.org/abs/0802.1543)**,
  cites 382, the tidal-evolution / eccentricity-damping side.)
- **Lainey, V. et al. (2009)**: *Nature* 459, 957. **No arXiv**
  ([`2009Natur.459..957L`](https://ui.adsabs.harvard.edu/abs/2009Natur.459..957L)). Cites: 359. Astrometric detection of *active* strong tidal
  dissipation in the Io–Jupiter system: empirically closes the heating loop. §2.
- **Henning, W. G., O'Connell, R. J. & Sasselov, D. D. (2009)**: *ApJ* 707, 1000.
  **[arXiv:0912.1907](https://arxiv.org/abs/0912.1907).** Cites: 158. Tidally heated terrestrial exoplanets with a
  viscoelastic response model: the exoplanet-rheology bridge. §5.
- **Howett, C. J. A. et al. (2011)**: *JGR Planets* 116, E03003. **No arXiv**
  ([`2011JGRE..116.3003H`](https://ui.adsabs.harvard.edu/abs/2011JGRE..116.3003H)). Cites: 136. ~15.8 GW measured from Enceladus's south-polar
  region: the Enceladus calibration number. §2.
- **Veeder, G. J. et al. (2012)**: *Icarus* 219, 701. **No arXiv**
  ([`2012Icar..219..701V`](https://ui.adsabs.harvard.edu/abs/2012Icar..219..701V)). Cites: 92. Io's volcanic thermal sources and global heat
  flow: the updated ~10¹⁴ W census. §2.
- **Efroimsky, M. & Williams, J. G. (2012)**: *Celest. Mech. Dyn. Astron.* 112, 283.
  **[arXiv:1105.6086](https://arxiv.org/abs/1105.6086).** Cites: 128. Bodily tides near spin-orbit resonances: the
  frequency-dependent formalism beyond fixed-Q for non-synchronous bodies. §5.
- **Barnes, R. et al. (2013)**: *Astrobiology* 13, 225. **[arXiv:1203.5104](https://arxiv.org/abs/1203.5104).** Cites:
  120. "Tidal Venuses": tidal heating can trigger a runaway greenhouse, the upper
  habitability bound on tidal heat. §6 context.
- **Heller, R. & Barnes, R. (2013)**: *Astrobiology* 13, 18. **[arXiv:1209.5323](https://arxiv.org/abs/1209.5323).**
  Cites: 129. Exomoon habitability constrained by illumination *and* tidal heating:
  the moon-specific habitability bound directly relevant to NearStars moons. §6.
- **Henning, W. G. & Hurford, T. (2014)**: *ApJ* 789, 30. **No arXiv**
  ([`2014ApJ...789...30H`](https://ui.adsabs.harvard.edu/abs/2014ApJ...789...30H)). Cites: 55. Tidal heating in multilayered terrestrial
  exoplanets: layered viscoelastic structure. §5.
- **Driscoll, P. E. & Barnes, R. (2015)**: *Astrobiology* 15, 739.
  **[arXiv:1509.07452](https://arxiv.org/abs/1509.07452).** Cites: 108. Tidal heating of Earth-like planets around M
  stars and its coupling to thermal/magnetic evolution and habitability. §6.
- **Renaud, J. P. & Henning, W. G. (2018)**: *ApJ* 857, 98. **[arXiv:1707.06701](https://arxiv.org/abs/1707.06701).**
  Cites: 82. Increased tidal dissipation using advanced (Andrade) rheology: shows
  fixed-Q and Andrade can differ by large factors. §5, §8.

**지표 열수송(§6.2–§6.5).** 같은 ADS 검증 패스에서 확인했다(2026-08-21).

- **O'Reilly, T. C. & Davies, G. F. (1981)**: *Geophys. Res. Lett.* 8, 313. **No arXiv**
  ([`1981GeoRL...8..313O`](https://ui.adsabs.harvard.edu/abs/1981GeoRL...8..313O)). Io의 마그마 열수송을 *a mechanism
  allowing a **thick** lithosphere*로 규정한, 전도가 아니라 이류가 열을 나른다는 효시 논문. §6.2.
- **Reese, C. C., Solomatov, V. S. & Moresi, L.-N. (1998)**: *JGR* 103, 13643.
  **No arXiv** ([`1998JGR...10313643R`](https://ui.adsabs.harvard.edu/abs/1998JGR...10313643R)). 정체뚜껑 대류의 열수송 효율.
  평원을 배출구에서 제외시키는 10–30 mW/m² 전도 천장의 출처. §6.2.
- **Moore, W. B. (2003)**: *JGR Planets* 108, 5096. **No arXiv**
  ([`2003JGRE..108.5096M`](https://ui.adsabs.harvard.edu/abs/2003JGRE..108.5096M)). Io의 조석가열과 대류. 고체상 대류가
  *"falls an order of magnitude short"*이므로 멜트 분리가 지배해야 한다. §6.2.
- **Moore, W. B. & Webb, A. A. G. (2017)**: *Earth Planet. Sci. Lett.* 474, 13.
  **No arXiv** ([`2017E&PSL.474...13M`](https://ui.adsabs.harvard.edu/abs/2017E%26PSL.474...13M)). heat piping이
  *"produces a thick, cold, and strong lithosphere"*라는, 고플럭스=두꺼운 뚜껑 결과. §6.2.
- **Kankanamge, D. G. J. & Moore, W. B. (2019)**: *JGR Planets* 124, 114. **No arXiv**
  ([`2019JGRE..124..114K`](https://ui.adsabs.harvard.edu/abs/2019JGRE..124..114K), doi 10.1029/2018JE005800). heat-pipe의 정량적
  파라미터화(멜트 플럭스, 맨틀·뚜껑 하부 온도, **뚜껑 두께**, 잔여 전도 플럭스)로, 수치
  시뮬레이션에 대해 15 % 이내로 검증되었다. §6.2.
- **Spencer, D. C., Katz, R. F. & Hewitt, I. J. (2020)**: *JGR Planets* 125, e06443.
  **[arXiv:2003.08287](https://arxiv.org/abs/2003.08287).** 지배 지표 에너지 균형(eq. 33)과
  분출/관입 분할(eqs. 34–35). 99.5 % 화산성 수송, 80 km 탄성 두께, 그리고 다른 용암 세계에
  eq. 10을 적용하라는 명시적 초대까지. **§6.2의 하중을 지는 인용.**
- **Davies, J. H. & Davies, D. R. (2010)**: *Solid Earth* 1, 5. **No arXiv**
  ([`2010SolE....1....5D`](https://ui.adsabs.harvard.edu/abs/2010SolE....1....5D)). 38,347개 측정에서 얻은 지구 지표 열류
  47±2 TW = 92.1 mW/m². 사다리의 판구조 단. §6.2.
- **Rathbun, J. A. et al. (2004)**: *Icarus* 169, 127. **No arXiv**
  ([`2004Icar..169..127R`](https://ui.adsabs.harvard.edu/abs/2004Icar..169..127R)). Io의 배경 열복사. 핫스팟 사이의 내인성
  플럭스는 <1 W/m²다. §6.3.
- **Veeder, G. J. et al. (2015)**: *Icarus* 245, 379. **No arXiv**
  ([`2015Icar..245..379V`](https://ui.adsabs.harvard.edu/abs/2015Icar..245..379V)). Io 열류 목록 갱신. Veeder+ 2012와 함께
  "41–46 % 미확인" 단서의 출처. §8.
- **Veeder, G. J. et al. (2012)** — 위 §2 항목 참고. "열류의 50 %가 표면의 1.2 %에서"라는 집중
  통계와 Loki의 9.6×10¹² W도 여기서 나온다. §6.3, §6.4.
- **Williams, D. A. et al. (2011)**: *Icarus* 214, 91. **No arXiv**
  ([`2011Icar..214...91W`](https://ui.adsabs.harvard.edu/abs/2011Icar..214...91W)). Io 전구 지질도. patera 바닥은 표면의
  2.5 %지만 검출 핫스팟의 64 %를 품는다. §6.3.
- **Davies, A. G. et al. (2024)**: *Nature Astronomy* 8, 94.
  **[arXiv:2310.12382](https://arxiv.org/abs/2310.12382).** Io의 총 열복사 ≈106 TW, 그중 ≈56 TW가
  화산 구조에서 나오며, 활동 화산이 표면의 ≈2 %를 덮는다. §6.2, §6.3.
- **Giles, R. S. et al. (2024)**: *Icarus* 418, 116151.
  **[arXiv:2405.19253](https://arxiv.org/abs/2405.19253).** Io의 SO₂ 대기와 그 배경의 서리 온도
  모형. 22년치 데이터가 일사만으로 맞춰진다(Bond 알베도 0.56, 열관성 250 MKS, 적도 서리
  106–116 K). 평원이 복사 평형 지형이라는 증거. §6.3.
- **Mura, A. et al. (2025)**: *Planet. Sci. J.* 6, 43.
  **[arXiv:2410.10686](https://arxiv.org/abs/2410.10686).** Juno/JIRAM의 Loki Patera 관측. 지각
  휘도온도 270–355 K로, 지질 면적 분모를 독립적으로 뒷받침한다. §6.4.
- **Keszthelyi, L. et al. (2007)**: *Icarus* 192, 491. **No arXiv**
  ([`2007Icar..192..491K`](https://ui.adsabs.harvard.edu/abs/2007Icar..192..491K)). Io의 분출 온도를 ~1340 °C(1613 K)로
  하향 수정. 384 kW/m² 맨멜트 천장을 정하는 값이다. §6.4.
- **de Pater, I. et al. (2016)**: *Icarus* 264, 198. **No arXiv**
  ([`2016Icar..264..198D`](https://ui.adsabs.harvard.edu/abs/2016Icar..264..198D)). Pele과 Pillan의 시간 변화. 940 K에서
  44.3 kW/m²인 Pele의 피팅 면적 플럭스가 피팅 분모 쪽 앵커다. §6.4.
- **Campion, R. & Coppola, D. (2023)**: *Front. Earth Sci.* 11, 1140199. **No arXiv**
  ([`2023FrEaS..1140199C`](https://ui.adsabs.harvard.edu/abs/2023FrEaS..1140199C)). 용암호 집계 논문. 그 Table 1이 측정된
  용량 대역과 그 최대치 111 kW/m²를 제공한다. §6.4.
- **Rovira-Navarro, M. et al. (2021)**: *Planet. Sci. J.* 2, 119. **No arXiv**
  ([`2021PSJ.....2..119R`](https://ui.adsabs.harvard.edu/abs/2021PSJ.....2..119R)). "Tidally Heated Exomoons around Gas Giants".
  Io보다 1–3 dex 위의 super-Io 봉투와, 두꺼운 뚜껑을 통한 heat piping이 지속 가능한 가지라는
  결론. ε Eridani b 외계위성 관측가능성 연구인 Kleisioti+ 2023
  ([arXiv:2305.03410](https://arxiv.org/abs/2305.03410))이 이를 채택했다. §6.5.

**단일 canonical 논문이 없는 주제:** §6.1의 지표 플럭스 → "바다 대 죽음" *임계값*은 위의
Enceladus/Europa·Io 문헌을 종합한 것이지 인용 가능한 단일 임계값 논문이 아니며, 도출된
법칙이 아니라 차수 지침으로 다룬다. §6.2의 모드 경계도 마찬가지다. 발표된 임계값을 인용하는
것이 아니라 발표된 *용량*을 비교하는 것이다(§8).

---

## 관련 문서

- [`ice-stability-methodology.md`](ice-stability-methodology.md) — 강하게 가열되는 천체에
  얼음 표면이 있다는 것은 모순이다. 그 레시피의 예산은 외부 유입만 다루므로, 얼음 존속을 판정하기
  전에 여기서 구한 내부 플럭스를 더해야 한다.
- [`crater-degradation-methodology.md`](crater-degradation-methodology.md) — 이 문서의
  열류를 두 번 소비한다. 화산 매몰 속도로 한 번, 크레이터 점성 이완 스위치로 한 번.
- [`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md) — 위성 쪽 짝.
  위성이라면 이 문서의 Layer 1 `T_eq`를 그쪽의 4항 예산(식, 모행성 열복사+반사, 조석 가열)으로
  대체한다.
- [tidally-locked-temperature-methodology](tidally-locked-temperature-methodology.md): 동주기 바디의 표면/평형온도를
  다루는 자매 레시피. 여기서 다룬 조석가열은 그 문서가 다루는 복사에 더해지는 *추가* 내부
  열원이다.
- [exoplanet-atmosphere-methodology](exoplanet-atmosphere-methodology.md): 여기서 그대로 따른 "게이트한 뒤
  문서화" 틀과 "범위 안에서 원칙 있는 선택"이라는 정직함 관행의 출처다.
- [planetary-dynamo-scaling](planetary-dynamo-scaling.md): 이 문서가 본보기로 삼은 모범 자매
  스케일링 법칙 문서(법칙 + calibration 표 + 유효 영역 + 워크드 예제)다. Driscoll & Barnes 2015가
  조석가열을 그 문서가 도출하는 자기 진화에 연결한다는 점도 함께 본다.
- **조석 *고정* / despin 시간척도 방법론**: **작성 예정인 자매 문서**다. 고정(바디가 동주기로
  자전하는가?)은 가열(얼마나 많은 출력이 소산되는가?)과 *별개의* 문제다. 이 문서는 동주기
  자전을 전제하니 둘을 혼동하지 말아야 한다.
- [methodology-index](methodology-index.md) — 모든 도출값 방법론 레시피의 인덱스입니다.
