<!-- 조석고정(despin) 타임스케일로 동기자전 여부와 자전 상태(1:1·3:2·유사동기)를 판정하는 방법론 레퍼런스 -->
# 조석고정 방법론: despin 시간척도, 자전 상태, 그리고 열조석 예외

바디의 조석 동기화(despin) 시간척도 `τ_lock`을 시스템 나이와 견주어 **그 바디가 조석으로
고정되는지, 또 어떤 자전 상태로 고정되는지**를 판정하기 위한 방법 레퍼런스다.
[조석가열 문서](tidal-heating-methodology.md)와 [dynamo 스케일링 문서](planetary-dynamo-scaling.md)와
같은 정신을 따른다. 지어낸 측정치가 아니라 관계식과, 알려진 바디를 재현하는 calibration을 함께
인용한다.

가열·온도 자매 문서가 선행 조건으로 필요하다고 짚어 둔 바로 그 문서다. 두 문서는 모두 가까운
안쪽 바디가 동주기로 자전한다고 *전제*하는데, 이 문서가 그 전제를 **정당화**한다. 그리고 전제가
깨지는 경우에는 그 바디가 대신 어떤 상태로 고정되는지를 말해 준다(더 높은 자전-공전 공명,
유사동기, 또는 대기가 구동하는 비동기 상태).

> 인용은 즉석 웹 검색이 아니라 NASA ADS(등록된 `ADS_API_TOKEN`)에 대조해 확정한다.
> arXiv id가 있으면 그것을, 없으면 권위 있는 ADS bibcode를 쓴다("no arXiv" 표시).
> 검증된 목록은 §8을 참고하면 된다.
> 교과서가 아니라 실무용 레퍼런스다.

**범위 주의.** 이 문서는 바디가 *고정되는지*, 또 *어떤 상태로* 고정되는지를 결정한다:
[온도 문서](tidally-locked-temperature-methodology.md)(직하점 기하)와
[조석가열 문서](tidal-heating-methodology.md)(`(21/2)e²` 동기 형식)가 함께 전제하는 **동기 가정을
떠받친다.** 이 문서는 가열 그 자체가 **아니다.** 가열 문서는 소산 출력 `Ė`를, 이 문서는 자전 진화를
준다. 둘은 **같은 `Q/k₂` 내부 미지수**를 공유하며, 다행히도 궤도거리의 가파른 거듭제곱이 그 미지수에도
*불구하고* 대개 판정을 견고하게 만든다는 같은 교훈도 공유한다(여기서는 `a⁶`, 거기서는 `a⁻⁷·⁵`).

## 목차

1. [시간척도: despin(동기화) 공식](#1-시간척도-despin동기화-공식)
2. [Calibration: 공식이 고정된 태양계 바디를 재현한다](#2-calibration-공식이-고정된-태양계-바디를-재현한다)
3. [a⁶ 거리 게이트 (지배적 항)](#3-a-거리-게이트-지배적-항)
4. [자전 상태 분류: 1:1, p:q 공명, 유사동기](#4-자전-상태-분류-11-pq-공명-유사동기)
5. [대기 열조석 예외](#5-대기-열조석-예외)
6. [유효 영역과 정직함: Q/k₂와 초기 자전](#6-유효-영역과-정직함-qk와-초기-자전)
7. [워크드 예제](#7-워크드-예제)
8. [주석 달린 참고문헌](#8-주석-달린-참고문헌)
9. [관련 문서](#관련-문서)

---

## 1. 시간척도: despin(동기화) 공식

어떤 원시 자전 `ω₀`로 출발한 바디는 섭동체(행성이라면 별, 위성이라면 행성)로부터 조석 토크를
받는다. 솟아오른 조석 팽대부는 내부 마찰이 정하는 작은 각만큼 뒤처지고, 그 뒤처진 팽대부가
가하는 토크가 자전을 궤도 평균운동 `n` 쪽으로 끌어간다. **despin(동기화) 시간척도**는 그 토크가
초과 자전 각운동량을 제거하는 데 걸리는 시간이다. 관성모멘트 `I = α m R²`인 균질 바디에 대해,
일정 위상지연("fixed-Q") 결과는, Goldreich & Soter 1966(`1966Icar....5..375G`)이 유도하고
Murray & Dermott 1999 *Solar System Dynamics*(`1999ssd..book.....M`) §5에서 교과서 형태로
정리한 것, 다음과 같다.

    τ_lock  ≈  (ω₀ − n) · (Q / k₂) · (I a⁶) / (3 G M_p² R⁵)

차수 단위의 자전 초과분을 떼어 내고 `I = α m R²`로 쓰면, 실무용 스케일링은 다음과 같다.

    τ_lock  ∝  (Q / k₂) · ω₀ · a⁶ · I / (G M_p² R⁵)
            ∝  (Q / k₂) · ω₀ · α · (m / R³) · a⁶ / (G M_p²)

각 항은 다음과 같다.

| Symbol | Meaning | Where it comes from |
|---|---|---|
| `Q` | tidal quality factor (1/Q ≈ phase lag = fraction of energy lost per cycle) | rheology (§6) |
| `k₂` | degree-2 tidal Love number (potential response of the body) | interior structure (§6) |
| `ω₀` | initial (primordial) spin rate of the **locking** body | unknown; order-of-magnitude (§6) |
| `n` | orbital mean motion = `2π/P_orb` = `√(G M_p / a³)`, the target spin | orbit |
| `I = α m R²` | moment of inertia of the locking body (`α ≈ 0.33–0.4` for differentiated rock) | interior |
| `m`, `R` | mass and radius of the **locking** body | DB / [mass-radius doc](mass-radius-relation-methodology.md) |
| `M_p` | mass of the **perturber** (the star, for a planet; the planet, for a moon) | DB |
| `a` | semi-major axis of the locking body's orbit about the perturber | orbit |
| `G` | gravitational constant | – |

가열 문서와 비교하면 **역할이 뒤집혀** 있음에 주목하라. 거기서는 `R⁵`과 `M_p²`가 분자에
들어가(큰 섭동체와 큰 바디가 더 큰 출력을 소산한다), 여기서는 같은 인자가 *분모*에 들어간다
(더 강한 솟구침 토크가 자전을 *더 빨리* 감속시키므로 `τ_lock`이 짧아진다). 같은 조석 물리를 열이
아니라 자전으로 읽는 것일 뿐이다. `Q/k₂` 묶음은(가열 공식의 `k₂/Q`에 대해 **뒤집힌** 형태임에
주의) 바디의 물질이 기여하는 부분이고, 나머지는 모두 기하, 섭동체 질량, 그리고 알 수 없는 초기
자전이다.

판정 규칙은 단 하나의 비교다.

> `τ_lock`을 계산해 **시스템 나이** `t_sys`와 견준다.
> **`τ_lock ≪ t_sys` → 고정**(§5가 적용되지 않는 한 동기로 가정).
> **`τ_lock ≳ t_sys` → 반드시 고정되지는 않음**: 측정/원시 자전을 유지한다.

fixed-Q 형식은 *1차* 도구다. `Q`와 `k₂`를 상수로 다루며 `ω₀`는 알 수 없다. 그것이 언제 문제가
되는지, 그리고 왜 대개는 고정/비고정 판정을 바꾸지 않는지는 §6에서 다룬다.

---

## 2. Calibration: 공식이 고정된 태양계 바디를 재현한다

이 공식이 믿을 만한 것은, 분류에 맞는 `Q/k₂`를 넣으면 태양계에서 어느 바디가 고정되어 *있고*
어느 바디가 아닌지를 재현하기 때문이다. 가열 문서가 Io와 Enceladus로 calibration하는 것과
같은 논리다.

| Body | Perturber | a | class Q/k₂ | τ_lock (order) | t_sys | observed state | match |
|---|---|---|---|---|---|---|---|
| **Moon** | Earth | 3.84×10⁵ km | rocky ~10²–10³ | ~10⁷–10⁸ yr | 4.5 Gyr | 1:1 synchronous | ✓ locked |
| **Mercury** | Sun | 0.39 AU | rocky ~10²–10³ | ~few ×10⁸–10⁹ yr | 4.5 Gyr | **3:2** (not 1:1!) | ✓ despun, §4 |
| **Galilean moons** | Jupiter | 6–26 R_J | icy/rocky | ≪ Gyr (close in) | 4.5 Gyr | all 1:1 | ✓ locked |
| **Venus** | Sun | 0.72 AU | rocky + atmosphere | ~10⁹ yr (gravitational) | 4.5 Gyr | **slow retrograde** | ✗ thermal tide, §5 |

- **달**: 1:1 고정의 정석이다. 섭동체 지구가 3.84×10⁵ km에 있고 암석질 `Q/k₂`를 쓰면 `τ_lock`은
  Gyr보다 한참 아래로 나온다. 달은 태양계 역사 초기에 동기자전으로 감속되어, 그 뒤로 줄곧 한쪽
  면만 보여 준다. 교과서적 앵커다(Murray & Dermott 1999 §5; Peale 1977, `1977plsa.conf...87P`,
  "Rotation Histories of the Natural Satellites"). ✓
- **Mercury**: 자전이 감속되었으나(원시의 빠른 자전은 사라진 지 오래라 `τ_lock ≪ t_sys`)
  1:1이 아니라 **3:2 자전-공전 공명**으로 고정되었다. 이심률과 영구 사극자 모멘트가 함께 작용한
  결과다(Goldreich & Peale 1966, `1966AJ.....71..425G`; 포획의 설명은 Correia & Laskar 2004,
  `2004Natur.429..848C`). "감속은 일어났다"는 판정은 옳고, "1:1"은 틀렸을 것이다. §4의 예시다.
  despin은 ✓, 순진하게 1:1로 가정하는 것은 ✗.
- **Venus**: *중력* 조석만 따진 `τ_lock`은 시스템 나이보다 작거나 비슷해서, 순진하게 적용하면
  "거의 동기여야 한다"고 말한다. 그러나 금성은 **느린 역행** 자전을 한다. 해답은 대기 **열조석**이다
  (Gold & Soter 1969, `1969Icar...11..356G`; Dobrovolskis & Ingersoll 1980, `1980Icar...41....1D`).
  두꺼운 대기의 열적으로 구동된 팽대부가 중력 조석과 반대 방향의 토크를 가해, 자전을 1:1에서
  벗어난 곳에 세워 둔다. §5의 예외다. 맨 공식만으로는 ✗.

calibration의 메시지는 이렇다. despin *시간척도*는 Mercury, 달, 갈릴레이 위성이 모두 나이 안에
감속되었음을 정확히 알려 준다. 행성/위성과 암석/얼음을 가로지르는 바디들에 걸쳐 공식은
**예/아니오**를 옳게 맞힌다. 공식 단독으로 알 수 *없는* 것은 최종 **상태**(Mercury의 3:2)나 **대기에
의한 뒤집힘**(Venus)이다. 그것은 §4와 §5가 필요하다.

---

## 3. a⁶ 거리 게이트 (지배적 항)

**한 절만 읽는다면 바로 이 절이다**: 가열 문서의 `a⁻⁷·⁵` 게이트를 거울로 비춘 것이다.
`τ_lock ∝ a⁶`이기 때문에 궤도거리가 다른 모든 손잡이를 압도한다. 거리가 2배가 되면 고정 시간이
`2⁶ = 64배` 변한다.

암석질 바디의 `Q/k₂`, `ω₀`, `m`, `R`과 섭동체 질량을 고정한 채 바깥으로 옮겨 보자.

| relative a | relative τ_lock | implication |
|---|---|---|
| 0.5× | ~1/64 | locks ~60× faster, essentially instant if it was marginal |
| 1× | 1 | reference |
| 2× | ~64× | a marginal case becomes "may never lock within the age" |
| 4× | ~4000× | almost certainly never locks (Earth-like → Gyr ≫ age) |

NearStars가 신경 쓰는 두 영역에 대한 함의는 이렇다.

- **가까운 안쪽(M형 왜성 HZ 행성, 행성 반경 몇 배에 도는 위성).** M형 왜성의 거주가능 영역은
  ~0.02–0.2 AU에 있고, 위성은 행성 반경 몇 배 거리에서 공전한다. `a⁶` 항이 `τ_lock`을 **≪ Gyr**로,
  어떤 현실적인 시스템 나이보다도 한참 아래로 떨어뜨린다. **이런 바디는 고정된다.** 온도·가열
  문서가 그들에 대해 동기자전을 가정할 자격이 있는 이유가 *바로* 이것이다(Kasting, Whitmire &
  Reynolds 1993, `1993Icar..101..108K`는 M형 왜성 HZ에서의 고정을 짚었고, Barnes 2017,
  `2017CeMDA.129..509B`은 그 크기를 준다, §7 참조).
- **먼 바깥(태양형 별을 1 AU에서 도는 지구, 멀리 떨어진 위성).** 같은 `a⁶`이 `τ_lock`을 ≫ 나이로
  부풀린다. **이런 바디는 고정되지 않으며** 원시 자전을 유지한다. 1 AU의 지구는
  `τ_lock ≫ 4.5 Gyr`이며, 지구가 태양에 조석 고정되어 있지 않은 이유가 이것이다.

**견고함.** 고정/비고정 판정은 `Q/k₂`와 `ω₀`의 차수 수준 불확실성(§6)에도 *불구하고* 대개
안전하다. `a⁶`이 지배하기 때문이다. 가까운 안쪽의 M형 왜성 HZ 행성은 10⁶–10⁸ yr에 고정되며,
`Q/k₂`가 ×100 흔들려도 여전히 ≪ Gyr다. 이 게이트는 상세 추정에 앞서 한 줄로 정신을 차리게 하는
점검이다. **`a`를 공식에 넣고 나이와 10의 거듭제곱 단위로 비교하라.** `τ_lock ≈ t_sys` 경계
*근처*에 놓인 바디만(K/M형 별 주위 몇 ×0.1 AU 같은 중간 경우) `Q/k₂`에 주의가 필요하고, 깊은
안쪽과 먼 바깥의 경우는 견고하다.

---

## 4. 자전 상태 분류: 1:1, p:q 공명, 유사동기

"고정"이 "1:1"과 같은 말은 아니다. `τ_lock ≪ t_sys`가 바디가 감속*되었음*을 확립하고 나면, 최종
상태를 결정하는 것은 **이심률**이다. 어느 상태인지 기록해 두어야 한다: 온도 문서의 직하점 기하는
*고정된* 직하점을 전제하는데, 이를 제공하는 것은 1:1 상태뿐이기 때문이다.

**(a) 원궤도(e ≈ 0) → 1:1 동기.** 평형 자전이 평균운동과 같다. 한쪽 면이 영구히 섭동체를 향하고,
직하점이 고정된다. 조석으로 원형화된 가까운 안쪽 바디의 기본값이며, 자매 문서가 전제하는
상태다. *(달; 갈릴레이 위성; 거의 원궤도인 대다수 M형 왜성 HZ 행성.)*

**(b) 유의미한 이심률 → 유사동기(초동기).** 이심 궤도에서 매끄러운(강한 영구 사극자가 없는)
응답을 가진 바디라면, 평형은 `ω = n`이 **아니다.** 조석 토크는 바디가 가장 빨리 움직이는 근점
근처에서 가장 강하므로, 평형 자전은 평균운동보다 *위*에 자리 잡는다. Hut 1981(`1981A&A....99..126H`)은
평형 조석 모형의 평형 자전율을 다음과 같이 준다.

    ω_eq / n  =  (1 + (15/2)e² + (45/8)e⁴ + (5/16)e⁶) / [(1 + 3e² + (3/8)e⁴)(1 − e²)^{3/2}]

작은 `e`에서는 `ω_eq/n ≈ 1 + 6e²`로 환원되어 동기보다 약간 빠르므로, 직하점은 고정되지 않고
**표류한다.** Dobrovolskis 2007(`2007Icar..192....1D`)이 이런 이심 자전 상태의 기후 결과를 다룬다.
*내부가 유체에 가깝고 큰 영구 형상이 없는 이심 NearStars 바디에 부여할 상태가 바로 이것이다.*

**(c) 이심률 + 영구 사극자 → 더 높은 p:q 자전-공전 공명.** 동결된 영구 사극자(비축대칭 형상)를
가진 암석질 바디는 **p:q 공명으로 포획**될 수 있어, `q`번 공전하는 동안 `p`번 자전한다: Mercury의
**3:2**가 전형적인 예다(Goldreich & Peale 1966, `1966AJ.....71..425G`). 포획은 *확률적*이며 이심률과
조석 모형에 달려 있다. Correia & Laskar 2004(`2004Natur.429..848C`)는 Mercury의 혼돈적 궤도 진화가
3:2를 가장 가능성 높은 결말로 만든다는 것을 보였고, Makarov 2012(`2012ApJ...752...73M`)와
Noyelles et al. 2014(`2014Icar..241...26N`)는 포획 확률을 주며 현실적인(진동수 의존) 조석 모형에서는
Mercury의 `e`에 대해 3:2 포획이 사실상 확실함을 보인다. 3:2 상태의 바디는 **천천히 움직이는
직하점**을 가지므로(한 공전 동안 두 개의 "뜨거운 경도"), 온도 문서의 고정-직하점 기하가 그대로
**적용되지 않는다.**

NearStars 실무 규칙은 이렇다. **고정된 모든 바디의 `e`를 기록하고 상태를 고른다.** 거의 원궤도면
1:1(자매 문서가 그대로 유효). 이심·유체면 유사동기(Hut). 이심·암석질이고 영구 형상이 있을 법하면
**p:q 공명의 가능성**(Mercury 3:2)을 표시하고 직하점이 움직인다고 적는다, 표면 온도 매핑에서
게임플레이상 의미 있는 구분이다.

---

## 5. 대기 열조석 예외

`τ_lock`상 고정되는 거주가능 영역 바디라도, 두꺼운 대기를 두르고 있으면 **자동으로 1:1이
아니다.** 항성 가열이 매일의 **열조석**(대기의 압력 팽대부)을 구동하고, 그 팽대부가 행성에
가하는 중력 끌림이 토크를 낳는다. 결정적으로 이 열조석 토크는 고체 중력 조석과 **반대 방향**으로
작용할 수 있고, 충분히 두꺼운 대기라면 그것과 균형을 이루거나 압도해, 자전을 1:1에서 벗어난
**비동기** 상태에 세워 둘 수 있다.

- **Venus가 태양계의 증거다.** 느린 *역행* 자전이 그 표식이다. Gold & Soter 1969(`1969Icar...11..356G`)가
  대기 조석 기구를 제안했고, Dobrovolskis & Ingersoll 1980(`1980Icar...41....1D`)이 토크 균형을
  계산했다: 열조석이, 중력 조석이라면 강제했을 1:1 상태에서 금성을 떼어 놓고 있다.
- **지구형 외계행성이 이를 일반화한다.** Leconte et al. 2015(`2015Sci...347..632L`, [arXiv:1502.01952](https://arxiv.org/abs/1502.01952))는
  **저질량 별 주위 지구 질량 HZ 행성이 대기 열조석에 의해 비동기 자전으로 몰릴 수 있음**을 보였다:
  즉 순진한 "M형 왜성 HZ 행성 ⇒ 1:1 고정" 추론은 대기가 충분히 두꺼우면 실패할 수 있다. 그보다
  앞서 Correia, Levrard & Laskar 2008(`2008A&A...488L..63C`, [arXiv:0808.1071](https://arxiv.org/abs/0808.1071))이 대기 조석 가지를
  포함한 평형 자전 영역들을 지도화했다.

**언제 적용되는가.** 열조석은 대기 질량/지표 기압에 비례하므로, 이 단서는 **주로 두꺼운 대기에서
중요하다**(≳ 지구 수준, 특히 금성 수준 ≫ 1 bar). **대기가 얇거나 없는 바디는 1:1로 고정된다**:
공기 없는 달과 Mercury는 이에 휘둘리지 않으며, 그들의 상태는 §4만으로 정해진다. 대기 두께에
대한 이 결합이, 이 예외를 [외계행성 대기 문서](exoplanet-atmosphere-methodology.md)와 공동으로
관할하는 이유다. 두꺼운 대기 HZ 행성의 최종 자전 상태를 despin 시간척도만으로 결정할 수는 없다.

실무 규칙은 이렇다. NearStars HZ 바디가 `τ_lock ≪ t_sys`이고 **동시에** 대기가 얇거나 없으면 →
1:1을 단언한다(온도 문서 유효). **두꺼운** 대기를 가지면 → **Leconte 열조석 단서**를 표시한다.
바디가 비동기일 수 있고 직하점이 순환할 수 있으며, 1:1 직하점 기후는 여러 가능성 중 하나일 뿐이다,
조용한 기본값이 아니라 명시적으로 문서화된 아트/물리 선택으로 골라야 한다.

---

## 6. 유효 영역과 정직함: Q/k₂와 초기 자전

dynamo·가열 문서의 단서들과 같은 정신으로, **방법은 근거를 갖추고 불확실성은 입력값이
짊어진다**, 그리고 `a⁶` 게이트가 대개 그 불확실성을 압도한다.

- **`Q/k₂`는 공유된 내부 미지수다**(가열 문서가 짊어지는 바로 그것, 뒤집힌 형태). 바디 분류에
  걸쳐 ~2–3 자릿수를 가로지르며: 암석질 `Q/k₂ ~ 10²–10³`, 얼음 ~10²–10⁴, 자이언트 ~10⁴–10⁶,
  외계 바디에 대해서는 사실상 측정된 적이 없다. `τ_lock`에 **선형으로** 들어가므로 ×100 흔들리면
  `τ_lock`도 ×100 움직인다.
- **초기 자전 `ω₀`는 알 수 없다.** 역시 선형으로 들어가지만 유계다. 시간–일 단위의 원시 자전
  주기는 ~1–2 dex만 차지하며, 제거해야 할 초과 각운동량이 *얼마인지*를 정할 뿐 스케일링을 바꾸지
  않는다. 게이트의 깊은 안쪽이나 먼 바깥에 있는 바디의 고정/비고정 판정을 바꾸지 못한다.
- **그래도 판정이 견고한 이유.** `τ_lock ∝ a⁶`이기 때문에 거리 항이 지배한다. 가까운 안쪽
  바디(`a`가 작음)는 `τ_lock`이 나이보다 한참 아래라, `Q/k₂`의 ×100과 `ω₀`의 ×10이 함께 작용해도
  (×1000) 여전히 ≪ Gyr다. 여전히 고정된다. 먼 바깥 바디(1 AU의 지구)는 나이보다 한참 위라
  같은 흔들림에도 ≫ Gyr다. 여전히 비고정이다. **`τ_lock ≈ t_sys`에서 ~1 dex 이내의 바디만**
  진짜로 불확실하며, 그런 바디는 판정을 *범위*로 보고하고 자전 상태를 하나로 단언하지 말고
  미정으로 다룬다.
- **공식은 fixed-Q / 평형 조석이다.** 자전-공전 공명 경계 근처거나, 포획 *확률*(§4 (c))을 따질
  때는 일정-`Q` 모형이 너무 거칠다. *어느* 공명에 얼마의 확률로 들어가는지를 결정하려면 진동수
  의존 처리(Makarov 2012; Noyelles et al. 2014; Correia & Laskar 2009)가 필요하다. despin *시간척도*는
  견고하지만, 이심 암석질 바디의 *포획된 상태*는 그렇지 않으니 그렇게 표시해야 한다.
- **열조석에 의한 뒤집힘(§5)은 공식에 아예 들어 있지 않다.** 두꺼운 대기 바디는 `τ_lock ≪ t_sys`
  이면서도 1:1이 아닐 수 있다. 두꺼운 대기 HZ 바디에 대해 `τ_lock`만 믿고 1:1을 단언하지 마라.

NearStars의 정직한 자세는 이렇다. `τ_lock`을 계산해 나이와 견주고, **판정을 그 자전 상태와 함께
명시한다.** 깊은 안쪽 바디 → 고정, 1:1(또는 §4에 따라 유사동기 / p:q), 높은 신뢰도이며, 이것이
자매 문서를 정당화한다. 경계선 바디 → "나이의 몇 배 인자 안에서 고정", 상태 미정. 두꺼운 대기
HZ 바디 → 고정되었으나 비동기일 수 있음, Leconte 단서를 표시한다. 물리가 열어 둔 상태 가운데
아트가 특정 상태를 원하는 경우, 그것은 조용한 기본값이 결코 아닌 **문서화된 선택**이다, 가열
문서가 자신의 `a⁻⁷·⁵` 게이트를 다루는 방식과 정확히 같다.

---

## 7. 워크드 예제

**달: 1:1 고정의 정석.** 섭동체 지구, `a = 3.84×10⁵ km`, 암석질 `Q/k₂ ~ 10²–10³`, `α ≈ 0.39`.
공식은 ~10⁷–10⁸ yr 차수의 `τ_lock`을 돌려준다, **≪ 4.5 Gyr**. 달은 일찍 감속되었고, 거의 원궤도
위에서 **1:1 동기** 자전에 안착했다(한쪽 면이 지구를 향함). 판정: 고정, 1:1, 교과서적 앵커이자
자매 문서가 전제하는 가장 단순한 경우다.

**Mercury: "항상 1:1은 아니다"의 사례.** 섭동체 태양, `a = 0.39 AU`, `e ≈ 0.206`, 암석질.
`τ_lock`은 나이보다 한참 아래이지만(Mercury는 감속*되었다*), 이심률과 영구 사극자가 함께 작용해
**3:2 자전-공전 공명**으로 포획되었다(Goldreich & Peale 1966; Correia & Laskar 2004가 포획을
가능하게, Makarov 2012 / Noyelles+ 2014가 현실적 조석으로 거의 확실하게 만들었다). 두 번 공전하는
동안 세 번 자전하므로 직하점이 **움직인다**: 이심 암석질 바디에 온도 문서의 고정-직하점 기하를
무턱대고 적용하는 데 대한 경고 사례다. 판정: 감속됨, 그러나 **1:1이 아닌 3:2**.

**Venus: 열조석 예외.** 섭동체 태양, `a = 0.72 AU`, 두꺼운 CO₂ 대기(~92 bar). 중력 조석
`τ_lock`은 나이보다 작거나 비슷해서, 순진하게 읽으면 "거의 동기"라고 한다. 그러나 금성은 **느린
역행** 자전을 한다. 대기 **열조석**(Gold & Soter 1969; Dobrovolskis & Ingersoll 1980)이 중력
조석에 맞서 이를 압도하기 때문이다. 판정: **비동기, 대기가 이긴다.** 자매 문서가 새겨야 할
교훈은, `τ_lock`이 "고정"이라 말해도 두꺼운 대기가 1:1 가정을 깨뜨릴 수 있다는 것이다.

**Proxima b / 일반적인 M형 왜성 HZ 행성: 가정을 정당화하는 사례.** 모성은 M형 왜성, HZ가
`a ~ 0.05 AU`(Proxima b: 0.0485 AU). `a⁶` 항이 `τ_lock`을 **≪ Gyr**로 몬다, Barnes 2017
(`2017CeMDA.129..509B`)은 그런 궤도에 대해 10⁶–10⁸ yr 차수의 고정 시간을 주며, 이는 수 Gyr인
모성 나이보다 한참 아래다. **그래서 이 바디는 고정되고**, 거의 원궤도라면 그것은 **1:1 동기**를
뜻한다, NearStars 지구형 명단(Proxima b, TRAPPIST-1 행성들 등)에 대해
[온도](tidally-locked-temperature-methodology.md) 문서와 [가열](tidal-heating-methodology.md)
문서가 전제하는 바로 그 상태다. **단서.** 그런 행성이 *두꺼운* 대기를 가지면 Leconte 2015
(`2015Sci...347..632L`) 열조석 단서(§5)가 적용되어 1:1 상태가 더 이상 보장되지 않는다: 단언하지
말고 표시하라. Turbet et al. 2016(`2016A&A...596A.112T`)이 바로 이 범위의 가능한 Proxima b
자전/기후 상태를 탐색한다.

**행성에 고정된 NearStars 위성(α Cen 계, 정성적).** 행성 반경 몇 배에서 행성을 도는 위성은
`a⁶` 게이트의 깊은 안쪽에 있다. `τ_lock ≪ t_sys`이므로 시스템 시간척도에서 **사실상 즉시
1:1로** 고정된다. [조석가열 문서](tidal-heating-methodology.md)가 α Cen Phase 4 위성들(Dante,
Hades, Pandora)에 `(21/2)e²` 동기 가열 형식을 적용할 때 *전제*하는 상태가 바로 이것이며, 그
전제를 정당화하는 것이 이 문서다. (가까운 안쪽 위성을 빠르게 고정시키는 그 `a⁶`은, 가까운 안쪽
위성을 세게 *데우는* `a⁻⁷·⁵`의 역이다. 가까운 안쪽 위성은 가장 빨리 고정되고 **동시에** 가장 많이
데워지므로, 지질학적으로 흥미로운 것들이다.) 먼 바깥 위성(예: 가열 문서의 Chaos, ~20 R_p)은
`τ_lock`이 훨씬 길어 1:1로 가정할 필요가 없다, 조석적으로도 차갑다는 점과 일관된다.

---

## 8. 주석 달린 참고문헌

각 항목: 저자, 연도, 저널/책, **검증된** arXiv id(없으면 "no arXiv" + bibcode), ADS 인용수, 그리고
기여 한 줄이다.

- **Goldreich, P. & Soter, S. (1966)**: *Icarus* 5, 375. **No arXiv**
  (`1966Icar....5..375G`). Cites: 977. "Q in the Solar System": the founding treatment
  of the tidal quality factor and the despin/tidal-evolution timescales; the source of
  the `Q/k₂` framing used throughout. §1.
- **Goldreich, P. & Peale, S. (1966)**: *AJ* 71, 425. **No arXiv**
  (`1966AJ.....71..425G`). Cites: 351. "Spin-orbit coupling in the solar system": the
  founding theory of spin–orbit resonance capture; why an eccentric body with a
  permanent quadrupole locks into a p:q resonance (Mercury 3:2) rather than 1:1. §4.
- **Gold, T. & Soter, S. (1969)**: *Icarus* 11, 356. **No arXiv**
  (`1969Icar...11..356G`). Cites: 111. "Atmospheric Tides and the Resonant Rotation of
  Venus": proposes the atmospheric thermal-tide torque that holds a thick-atmosphere
  body off 1:1; the origin of the §5 exception. §5.
- **Peale, S. J. (1977)**: in *Planetary Satellites* (IAU Colloq. 28). **No arXiv**
  (`1977plsa.conf...87P`). Cites: 58. "Rotation Histories of the Natural Satellites":
  the classic review of how satellites despin and reach their present rotation states;
  the worked-physics companion to the Moon/Galilean-moon calibration. §2.
- **Dobrovolskis, A. R. & Ingersoll, A. P. (1980)**: *Icarus* 41, 1. **No arXiv**
  (`1980Icar...41....1D`). Cites: 73. "Atmospheric tides and the rotation of Venus I":
  the quantitative torque balance between the gravitational and thermal tides that sets
  Venus's spin; the mechanism behind §5. §5.
- **Hut, P. (1981)**: *A&A* 99, 126. **No arXiv** (`1981A&A....99..126H`). Cites: 1367.
  "Tidal evolution in close binary systems": the equilibrium-tide model giving the
  **pseudo-synchronous** equilibrium spin (`ω_eq/n ≈ 1 + 6e²`) for eccentric orbits; the
  source of the §4 (b) formula. §4.
- **Kasting, J. F., Whitmire, D. P. & Reynolds, R. T. (1993)**: *Icarus* 101, 108.
  **No arXiv** (`1993Icar..101..108K`). Cites: 1951. "Habitable Zones around Main
  Sequence Stars": defines the classical HZ and notes that HZ planets around low-mass
  stars are close enough to become tidally locked; the locking motivation for the
  M-dwarf HZ. §3.
- **Murray, C. D. & Dermott, S. F. (1999)**: *Solar System Dynamics* (Cambridge Univ.
  Press). **Book** (`1999ssd..book.....M`). Cites: 2002. The standard textbook
  derivation of the tidal torque, the despin timescale, and spin–orbit dynamics (§5);
  the canonical source for the §1 formula rather than any single journal paper. §1, §2.
- **Correia, A. C. M. & Laskar, J. (2004)**: *Nature* 429, 848. **No arXiv**
  (`2004Natur.429..848C`). Cites: 122. "Mercury's capture into the 3/2 spin-orbit
  resonance as a result of its chaotic dynamics": explains why Mercury sits in 3:2 (the
  capture-probability problem) via chaotic orbital evolution. §4, §7.
- **Dobrovolskis, A. R. (2007)**: *Icarus* 192, 1. **No arXiv** (`2007Icar..192....1D`).
  Cites: 40. "Spin states and climates of eccentric exoplanets": works out the
  rotation states (including pseudo-synchronous) and the climate consequences for
  eccentric exoplanets. §4.
- **Correia, A. C. M., Levrard, B. & Laskar, J. (2008)**: *A&A* 488, L63.
  **[arXiv:0808.1071](https://arxiv.org/abs/0808.1071).** Cites: 44. "On the equilibrium rotation of Earth-like extra-solar
  planets": maps the equilibrium-rotation regimes including the atmospheric-thermal-tide
  branch; the exoplanet bridge for §5. §5.
- **Makarov, V. V. (2012)**: *ApJ* 752, 73. **[arXiv:1110.2658](https://arxiv.org/abs/1110.2658).** Cites: 56. "Conditions
  of Passage and Entrapment of Terrestrial Planets in Spin-orbit Resonances": capture
  probabilities for p:q resonances with a realistic (frequency-dependent) tidal model;
  3:2 capture near-certain for Mercury's eccentricity. §4, §6.
- **Noyelles, B., Frouard, J., Makarov, V. V. & Efroimsky, M. (2014)**: *Icarus* 241,
  26. **[arXiv:1307.0136](https://arxiv.org/abs/1307.0136).** Cites: 77. "Spin-orbit evolution of Mercury revisited":
  the modern frequency-dependent-rheology treatment of Mercury's 3:2 capture; shows the
  fixed-Q model is too crude for the *captured state* (not the timescale). §4, §6.
- **Leconte, J., Wu, H., Menou, K. & Murray, N. (2015)**: *Science* 347, 632.
  **[arXiv:1502.01952](https://arxiv.org/abs/1502.01952).** Cites: 166. "Asynchronous rotation of Earth-mass planets in the
  habitable zone of lower-mass stars": the key result that the atmospheric thermal tide
  can drive HZ terrestrial exoplanets into asynchronous rotation; the modern form of the
  §5 caveat that breaks the naive "M-dwarf HZ ⇒ 1:1" inference. §5, §7.
- **Barnes, R. (2017)**: *Celest. Mech. Dyn. Astron.* 129, 509. **[arXiv:1708.02981](https://arxiv.org/abs/1708.02981).**
  Cites: 190. "Tidal locking of habitable exoplanets": the review-level treatment of
  whether and how fast HZ planets lock, with the locking-timescale magnitudes; the
  source for the "M-dwarf HZ planet locks in 10⁶–10⁸ yr" magnitudes that license the
  sibling docs' synchronous assumption. §3, §7.

Cross-referenced (from the sibling temperature doc, not re-derived here):

- **Turbet, M. et al. (2016)**: *A&A* 596, A112. **[arXiv:1608.06827](https://arxiv.org/abs/1608.06827).** Cites: 230. "The
  habitability of Proxima Centauri b. II": explores the range of possible spin/climate
  states (including the thermal-tide-driven ones) for the Proxima b worked example. §7.

**단일 canonical 논문이 없는 주제:** §6의 분류별 `Q/k₂` *대역*은 Goldreich & Soter 1966 /
Murray & Dermott 문헌을 종합한 것이지(가열 문서 §5와 공유) 인용 가능한 단일 표가 아니다, 차수
지침으로 다룬다. *초기 자전* `ω₀`은 canonical 값이 없으며(원시의 미지수다) 인용이 아니라 논증으로
유계 지어진다.

---

## 관련 문서

- [tidal-heating-methodology](tidal-heating-methodology.md): 이 문서가 확립하는 **고정을 전제하는** 자매
  문서다. 가까운 안쪽 바디에 `(21/2)e²` 동기 가열 형식을 적용하는데, 그것이 유효한 것은 바로
  여기서 그들의 `τ_lock ≪ 나이`이기 때문이다. 둘은 같은 `Q/k₂` 내부 미지수를 공유하며(뒤집힌
  형태로, 가열은 `k₂/Q`, 고정은 `Q/k₂` 사용), "`a`의 가파른 거듭제곱이 판정을 견고하게 한다"는 같은 교훈도
  공유한다(거기서는 `a⁻⁷·⁵`, 여기서는 `a⁶`).
- [tidally-locked-temperature-methodology](tidally-locked-temperature-methodology.md): 그 문서의 직하점 기하는 이 문서가
  확인하는 **1:1 상태를 전제한다.** 이심 유사동기 / 3:2 경우(§4)와 열조석 예외(§5)는 그 기하를
  **복잡하게** 만드므로(직하점이 움직이거나 순환함), 적용 전에 자전 상태를 확인해야 한다.
- [exoplanet-atmosphere-methodology](exoplanet-atmosphere-methodology.md): **열조석 예외(§5)가 대기 두께에
  결합한다.** 두꺼운 대기는 1:1 고정을 막을 수 있으므로, HZ 행성의 최종 자전 상태를 `τ_lock`
  만으로 결정할 수는 없다.
- [mass-radius-relation-methodology](mass-radius-relation-methodology.md): `R`(그리고 `I`를 통해 `m`)이 despin
  시간척도에 들어간다. 통과하지 않는 / 질량만 아는 바디는 반경을 여기서 가져온다.
- [planetary-dynamo-scaling](planetary-dynamo-scaling.md): 이 문서가 본보기로 삼은 모범 자매 스케일링 법칙
  문서(법칙 + calibration + 유효 영역 + 워크드 예제)다.
- [methodology-index](methodology-index.md) — 모든 도출값 방법론 레시피의 인덱스입니다.
