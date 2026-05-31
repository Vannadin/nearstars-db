---
title: Universe Sandbox vs Principia n-body 엔진 비교
status: active
created: 2026-05-30
---
# Universe Sandbox vs Principia n-body 엔진 비교

**NearStars 와의 연관성.** NearStars 는 n-body KSP 모드인 **Principia**
에 각 컴포넌트의 ICRF Cartesian 상태 `(x, y, z, vx, vy, vz)` 를
`JD2433282.5` 시점 기준으로 공급하고, Principia 가 시스템 전체를 전방
적분합니다. 앞으로 가능한 방향 중 하나는 **커스텀 Principia 브랜치**
(슐츠 와 함께) 입니다. 그래서 이 노트는 Stellarium 비교와는 다른 질문을
던집니다. "우리 컨벤션이 맞는가" 가 아니라 **"실시간 인터랙티브 n-body
를 위해 Universe Sandbox 가 실제로 해낸 것 중 Principia 브랜치가 가져올
법한 것은 무엇이고, 무엇이 US² 의 목표에 종속된 결과라 *가져오면 안 되는
것*인가"** 입니다. 자매 노트는
[`stellarium-binary-orbit-comparison.md`](stellarium-binary-orbit-comparison.md)
를 참고하시기 바랍니다.

**⚠ 출처 품질에 관한 주의(중요).** Stellarium 노트는 Stellarium 이
오픈소스이기에 **실제 소스 라인**(`Star.hpp#L364-L373`) 을 인용할 수
있었습니다. **반면 Universe Sandbox 는 클로즈드소스 상용
소프트웨어입니다.** 여기 적힌 내용은 모두 공개된 개발자 발언(개발 블로그,
FAQ, 팀원의 Steam 포럼 게시글) 또는 팀이 관리하는 위키에서 온 것입니다.
각 주장에는 다음 태그를 붙였습니다.
- **[DEV]** — 개발자 직접 발언(블로그 / FAQ / 포럼 인용).
- **[WIKI]** — 팀 관리 위키, 개발자 발언 그대로는 아님.
- **[INFER]** — 관찰된 동작 / 설계로부터 추론.
- **[NO SRC]** — 출처를 찾지 못함. 미상으로 취급.

Principia 쪽은 오픈소스라 신뢰도가 높습니다(위키 + 배포된
`sol_numerics_blueprint.cfg` + 소스 헤더). 그쪽의 divergence flag 는
충실도 차이가 아니라 사소한 표현 차이에 불과합니다.

**범위.** 읽기 전용 연구. 이 레포에 코드 변경 없음.

**외부 참조.**
- Universe Sandbox 개발 블로그: https://universesandbox.com/blog/
- US² FAQ: https://universesandbox.com/faq/ (+ legacy /faq/original/)
- US² integrator 포럼 스레드(n-body 리드 개발자 "Greenleaf"):
  https://steamcommunity.com/app/230290/discussions/0/520518053429453785/
- Principia 위키: https://github.com/mockingbirdnest/Principia/wiki
- Principia Jool-stability 노트(symplectic 근거):
  https://github.com/mockingbirdnest/Principia/wiki/On-the-dynamical-stability-of-Principia's-modified-Jool-system
- 우리 파이프라인: [`../docs/reference/binary-epoch-pipeline.md`](../docs/reference/binary-epoch-pipeline.md),
  [`../docs/reference/principia-cfg-reference.md`](../docs/reference/principia-cfg-reference.md)

---

## 1. Executive summary

| 질문 | 답 |
|----------|--------|
| 수치적 목표가 같은가? | **아니오.** US² 는 **실시간 인터랙티비티**(바디를 잡고 던지고, 충돌·파편화하며, 어떤 속도에서도 반응) 를 최적화합니다. Principia 는 고정된 초기 상태를 타임워프 하에서 **결정론적이고 장기 안정적으로 전방 적분**하는 데 최적화합니다. |
| 기본 integrator | US²: **PEFRL**(4차 symplectic) [WIKI], velocity-Verlet, RK4, RKF, Adams, Hermite, Forest-Ruth 등을 포함하는 *선택 가능한 모음* 에서 고른 것 [DEV]. Principia: **`QUINLAN_TREMAINE_1990_ORDER_12`**(12차 symmetric linear multistep, conjugate-symplectic) — *모든* 천체에 고정. |
| Timestep | US²: **adaptive**, step-doubling 오차 추정으로 **길이 단위 tolerance** 를 사용자에게 노출해 제어 [DEV]. Principia: **fixed**(ephemeris 10분 / vessel history 10초), adaptive 는 vessel *prediction* 에만. |
| 정확도/속도 제어 | US²: **사용자에게 노출** — 시뮬레이션 속도 슬라이더는 자동 제한되는 target 으로, 오차가 가장 큰 단일 바디에 의해 캡 됨 [DEV+WIKI]. Principia: 런타임에 사용자 튜닝 없음. 정확성은 fixed step + symplecticity 의 성질로 보장. |
| 상대론 | US²: **Newtonian 전용**, GR 없음. 빛 속도 중력 전파 + PN 보정은 *지향점* 수준 [DEV]. Principia: Newtonian + geopotential 구면조화함수(J₂ / 전체 C̄ₙₘ,S̄ₙₘ), 마찬가지로 GR 없음. |
| 충돌 / 병합 / Roche | US²: **일급 기능** — overlap 검출, 운동량/에너지 보존 병합, cratering, 파편화, Roche 조석 붕괴 [DEV+WIKI]. Principia: **없음** — 바디는 연속 궤적 위의 점질량. |
| 다체 스케일링 | US²: 기본은 직접 O(N²), 수천 개 파편에는 **Barnes-Hut tree** opt-in [DEV]. Unity DOTS/Burst 로 CPU 멀티코어, **GPU 아님** [DEV]. Principia: massive body 는 n-body, vessel 은 무질량 test particle, N 은 작음(행성+항성 정도). |
| 결정론 / 가역성 | Principia: fixed-step **symmetric** 방법 → 결정론적, 시간 역행 가능, secular 에너지 drift 없음 [DEV-rationale]. US²: adaptive + 충돌 + RNG 파편 → 설계상 재현 **불가**. |
| Principia 브랜치가 US² 에서 가져와야 할 것? | **짧은 목록뿐이며, 대부분 코어 integrator 가 아니라 UX/ergonomics.** §6 참고. US² 의 선택 대부분은 "인터랙티브 샌드박스" 에서 따라 나온 것이고, KSP/Principia 는 그게 아닙니다. |

---

## 2. Universe Sandbox 가 실제로 하는 것

읽을 소스가 없어 Stellarium 노트보다 신뢰도가 낮습니다. 태그는 위에서
정의한 대로입니다.

### 2.1 하나의 integrator 가 아니라 integrator 모음

**[DEV]** n-body 리드 개발자("Steam 의 Greenleaf", Thomas Grønneløv /
"Naml" 로 알려짐) 가 역대 집합을 나열했습니다. explicit & semi-implicit
Euler, RK2, RK4, RKF(Runge-Kutta-Fehlberg), Adams-Bashforth 6차,
Adams-Moulton 6차, Hermite 5차, **PEFRL**, **Forest-Ruth**. "대규모
NBody 재작성" 과정에서 대부분이 일시적으로 빠졌고, 다시 추가되는
중이었습니다. 현재 노출된 기본값은 **PEFRL**(4차 symplectic 으로,
position-extended Forest-Ruth 계열) [WIKI] 이며, velocity-Verlet 가
명시적으로 문서화된 Verlet 변형입니다 [DEV].
> `x(t+dt)=x(t)+v(t)·dt+0.5·a(t)·dt²`, `v(t+dt)=v(t)+0.5·(a(t)+a(t+dt))·dt`

밝힌 철학 [DEV]. *"사용자가 작업에 맞는 integrator 를 고르게 하고,
합리적인 기본값을 정해 둔다 … 빠른 chaotic 시뮬레이션 → 속도가 중요,
장기 안정성 분석 → 정확도가 중요."*

### 2.2 길이 tolerance 를 사용자에게 노출하는 adaptive timestep

**[DEV]** 가장 흥미로운 설계 포인트입니다. 사용자는 step 당 최대 위치
오차에 해당하는 **길이 단위 tolerance** 를 설정합니다. 매 step 마다
엔진은 한 번의 전체 `dt` 와 두 번의 `½dt` step 을 밟아 비교하고(표준
step-doubling), tolerance 아래로 유지되도록 step 을 줄입니다.
> *"적분 step 길이는 이 tolerance 보다 큰 위치 오차를 만들지 않도록
> 조정된다."*

**[DEV]** 따라서 시뮬레이션 속도 슬라이더는 정확도를 지키기 위해 **자동
제한되는 target** 입니다. **[WIKI]** UI 는 심지어 지금 *어느 단일 바디*
가 오차가 가장 커서 속도를 캡 하고 있는지까지 표시합니다. **[DEV]**
tolerance 를 올리면 → 빨라지지만 오차가 누적되며 궤도가 "무너질" 수
있습니다.

### 2.3 Newtonian 전용

**[DEV]** *"Universe Sandbox 의 물리는 현재 Newtonian 뿐이다."* GR
없음. 중력파는 n-body 방법의 범위 밖이라고 명시했습니다. 지향하는 미래는
중력이 즉시가 아니라 `c` 로 전파되는 것, 그리고 가능하다면 post-Newtonian
보정입니다. GR 토글은 존재하지 않습니다 [NO SRC for any implemented GR
effect].

### 2.4 충돌, 병합, 파편화, Roche

**[DEV+WIKI]** 일급 기능이자 제품의 시그니처입니다.
- 충돌 = overlap 검출. **병합**("Combine") 또는 가상의 탄성
  **bounce** 로 해소하며, 운동량/에너지를 보존하고 충격 가열을
  동반합니다.
- Cratering. 충격 에너지가 더 큰 바디 질량의 일부를 녹이고, 녹은 질량
  → 질량/운동량/에너지를 보존하도록 무작위 질량/위치/속도로 뽑힌
  파편이 됩니다.
- 파편화 유형 세 가지. **collision**, **Roche**(조석 — 같은 step 당
  중력/조석력 평가에서 계산), **spin**.
- 파편 수는 성능을 위해 자동으로 캡 됩니다.

**[INFER]** 조석(Roche) 평가와 overlap 검출은 모두 step 당 중력 계산에
얹혀 돌아가고, 파편은 새로운 중력 바디가 됩니다. step 내부의 정확한
순서는 출처 없음입니다.

### 2.5 스케일링: O(N²) → Barnes-Hut, GPU 가 아닌 CPU

**[DEV]** 기본 중력은 직접 all-pairs **O(N²)** 입니다. 수천 개의
파편/링/은하 입자에는 **Barnes-Hut tree** 가 스케일링 답이며(정확도가
약간 떨어지고, "gravity tree ratio" 로 튜닝 가능) 실험적 opt-in 으로
배포됩니다 [WIKI]. 2025년 재작성에서 엔진은 **Unity DOTS / ECS / Burst /
Job System** 으로 옮겨졌습니다 — 캐시 친화적이고 멀티스레드인 **CPU**
방식입니다. **[NO SRC]** 중력 step 이 GPU 에서 돈다는 주장은 출처가
없습니다(GPU 라고 하는 검색 스니펫은 무관한 학술 논문과 혼동한 것으로
보입니다).

### 2.6 정밀도 / 프레임

**[NO SRC]** float64 위치나 floating-origin / origin-rebasing 방식을
확인해 주는 1차 발언이 없습니다. tolerance 가 "길이 단위" 라는 것만이
유일하게 인접한 사실입니다. 은하 스케일 시뮬레이션은 스스로 "대표적일
뿐 그다지 정확하지 않다" 고 설명하는데, 이는 *물리* 측 주의이지
부동소수점 측 이야기가 아닙니다.

---

## 3. Principia 가 하는 것(신뢰도 높음, 오픈소스)

### 3.1 천체에 대한 fixed-step symplectic

기본 ephemeris integrator: **`QUINLAN_TREMAINE_1990_ORDER_12`** — 12차
**symmetric linear multistep** 방법으로, **step 10분 고정**입니다.
Conjugate-symplectic 이라 **secular 에너지 drift 가 없고**, step 을
줄이면 작아지는 유계 진동만 남습니다. 밝힌 근거(Jool 노트).
> *"conjugate-symplectic 이라 에너지 drift 를 보이지 않는다 …
> 관측자는 여러 시점의 에너지를 측정해 비물리적인 계통적 drift 를
> 알아챌 수 없다."*

배포된 다른 fixed-step 계열들. Blanes-Moan SRKN, McLachlan /
McLachlan-Atela / Okunbor-Skeel SPRK, Quinlan-1999 SLMS.

### 3.2 vessel 미래에만 adaptive

Vessel **prediction / flight-plan** 은
**`DORMAND_ELMIKKAWY_PRINCE_1986_RKN_434FM`**(embedded RKN 4(3)4,
adaptive, tolerance 1 mm / 1 mm·s⁻¹) 를 쓰며 — **symplectic 이 아닙니다.**
Vessel *history* 는 fixed-step Quinlan-1999 order 8A, 10초입니다. 즉
Principia 는 이미 내부적으로 **adaptive embedded-RKN** 을 돌리고
있으며, 그것을 천체 백본이 아니라 test particle 의 미래에만 가두어 둔
것뿐입니다.

### 3.3 Geopotential, 정밀도, epoch, 결정론

- **Geopotential.** IERS-2010 normalized 구면조화함수, 또는 단일
  unnormalized J₂(`J₂ = −C̄₂₀·√5`). `geopotential_tolerance` 가 작은
  항을 잘라내 속도를 높입니다.
- **정밀도.** binary64 double, SI 단위, P/Invoke 를 통한 native
  C++14.
- **프레임/epoch.** `solar_system_epoch`(TT) 의 Cartesian 상태를
  `game_epoch` 까지 미리 적분, IAU-2009 극/회전 컨벤션. NearStars 의
  `JD2433282.5` 와 일치합니다.
- **결정론.** fixed-step *symmetric* 방법은 결정론적이고 시간 역행이
  가능합니다(이 성질 때문에 선택됨). adaptive vessel-prediction 구간은
  bit 단위로 역행되지 않습니다.
- **Warp.** 타임워프 하에서도 step 은 **고정**되며, warp 는 그저
  벽시계 초당 더 많은 step 을 돌릴 뿐입니다. vessel 이 없으면
  6,000,000× 까지 매끄럽고, vessel 이 있으면 ~1,000,000× 를 넘어가며
  버벅입니다.

---

## 4. 핵심 철학의 갈림

| | Universe Sandbox | Principia |
|---|---|---|
| **목표** | 실시간 *인터랙티브* 샌드박스 — 잡고, 던지고, 부수고, 지켜본다 | 게임플레이를 위한 *고정* 시스템의 결정론적 전방 적분 |
| **기본 integrator 차수** | 4차(PEFRL) | 12차(Quinlan-Tremaine) |
| **Step 제어** | Adaptive, 사용자 노출 길이 tolerance | Fixed step, 런타임 손잡이 없음 |
| **빠르게 돌릴 때 무엇이 양보되나** | 정확도가 점진적으로 저하, 궤도가 "무너질" 수 있음 | 아무것도 — 같은 step, 벽시계만 더 쓰며 정확성 보존 |
| **시스템을 라이브로 편집** | 핵심 기능 | use case 아님, 상태는 초기 상태 cfg 에서 옴 |
| **충돌/병합/Roche** | 일급 | 없음(점질량) |
| **재현성** | 목표 아님(RNG 파편, adaptive) | 설계상 결정론적 & 가역적 |

한 문장으로. **US² 는 인터랙티브 시뮬레이션을 살려 두려고 integrator 를
적응시키고, Principia 는 긴 시뮬레이션이 물리적으로 정직하게 유지되도록
integrator 를 고정합니다.** 다른 거의 모든 차이는 여기서 따라
나옵니다.

여기서 **천체 백본** 에 대해서는 흔한 "게임 = 덜 정확하다" 직관이
*뒤집힌다* 는 점에 주목하시기 바랍니다. Principia 의 기본값은 12차
symplectic 방법으로 — US² 의 4차 기본값보다 *차수가 높고* 장기 보장도
강합니다 — 이는 Principia 가 *알려져 있고 비교적 안정적인 위계* 를
적분하기 때문입니다. US² 는 *사용자가 임의로 구성한 혼돈에 충돌까지
얹힌 상황을 실시간으로* 견뎌야 하므로, 점진적 저하를 갖춘 더 낮은 차수의
adaptive 방식을 택합니다. "어느 쪽이 더 낫다" 가 아니라 서로 다른
문제입니다.

---

## 5. 둘이 일치하는 지점

Stellarium 사례보다는 적지만, 실재합니다.
1. **Newtonian 중력, GR 없음.** 둘 다 GR 을 n-body 엔진의 범위 밖으로
   봅니다(US² 는 지향점 수준, Principia 는 geopotential 조화함수는
   배포하지만 상대론은 없음). NearStars 의 항성/행성 스케일에서는 양쪽
   모두 옳은 선택입니다.
2. **안정한 경우엔 기본적으로 symplectic.** US² 의 기본 PEFRL 과
   Principia 의 Quinlan-Tremaine 은 둘 다 **symplectic/에너지 보존**
   계열입니다. 두 팀 모두 독립적으로, 장기간 도는 중력계에는 drift 하는
   순진한 RK4 가 아니라 symplectic 방법이 필요하다는 결론에
   이르렀습니다(US² 는 심지어 Euler 를 "그게 얼마나 나쁜지 보여주려고"
   남겨 둡니다 [DEV]).
3. **어렵고 불확실한 부분엔 adaptive embedded 방법.** US² 는 어디서나
   adaptive step-doubling 을 쓰고, Principia 는 vessel prediction 에
   adaptive embedded RKN 을 씁니다. 둘 다 궤적이 민감한 곳에서는
   adaptive 제어를 꺼내 드는데, 그 경계를 다르게 그을 뿐입니다.

---

## 6. 커스텀 Principia 브랜치에 대한 함의

정직한 헤드라인. **US² 를 인상적으로 만드는 대부분은 "인터랙티브
샌드박스" 에 종속된 것이고, KSP/Principia 는 그게 아닙니다.** KSP 에서는
별을 집어 던지지 않습니다. 결정론적이고 warp 안정적인 시스템 속에서
vessel 을 날립니다. 그래서 가져올 목록은 짧고 대부분 ergonomic
입니다. 실제로 고려할 만한 것을 대략의 우선순위로 정리합니다.

**진지하게 고려할 만함**
1. **사용자에게 노출하는 정확도/속도 tolerance + "최악 오차 바디"
   표시.** US² 의 최고의 UX 아이디어입니다. Principia 의 정확성은
   플레이어에게 보이지 않습니다(fixed step, 다이얼 없음). 브랜치는 단일
   "최대 위치 오차" tolerance 를 노출하고, 매끄러운 warp 를 묶고 있는
   *어느 바디* 가 현재 binding constraint 인지 드러낼 수 있습니다. 이는
   symplectic 천체 integrator 를 *건드리지 않고* 이식 가능합니다 —
   진단/UX 레이어에 살게 됩니다. **주의.** Principia 의 안정성 논증
   전체가 *fixed* step 위에 서 있습니다. 순진하게 "천체 step 을
   adaptive 하게 만든다" 면 conjugate-symplecticity 와 no-drift 보장이
   깨집니다. 가져올 것은 *표시와 step 크기 선택기* 이지 천체 adaptive
   stepping 이 아닙니다.

**조건부 — 브랜치의 목표가 이를 포함할 때만**
2. **충돌 / 병합 / Roche 붕괴.** 브랜치가 바디를 *충돌·병합* 시키길
   원한다면(US² 의 시그니처), Principia 에는 이를 위한 장치가 전혀
   없습니다 — US² 가 레퍼런스 설계입니다(overlap 검출, 운동량/에너지
   보존 병합, 파편 생성, step 당 조석 Roche). 이는 큰 기능이며,
   Principia 의 "점질량의 연속 궤적" 모델과 근본적으로 상충하고, 자체
   설계가 필요합니다. 가정하지 말고 flag 하시기 바랍니다.
3. **다체용 Barnes-Hut tree.** 브랜치가 *수천* 개 바디(잔해 링, 포획된
   무리) 를 시뮬레이션할 때만 관련됩니다. NearStars 의 footprint 는
   수십 개의 항성/행성 정도라 직접 O(N²) 로도 충분합니다. 브랜치 범위가
   N 을 자릿수 단위로 키우지 않는 한 보류합니다.

**가져올 가치가 별로 없음**
4. **낮은 차수의 adaptive 천체 integrator.** US² 의 adaptive PEFRL
   접근은 실시간으로 임의의 혼돈을 견디려 존재합니다. 고정되고
   큐레이션된 NearStars 시스템에는, 장기 안정성 목표에 대해 Principia 의
   fixed 12차 symplectic 이 *엄밀히 더 낫습니다.* 여기서 US² 방식을
   채택하는 것은 퇴보입니다.
5. **GPU offload.** US² 는 일부러 하지 않았습니다(CPU/DOTS/Burst).
   NearStars 의 N 규모에서 Principia 브랜치가 그럴 이유도 없습니다.

**브랜치의 열린 설계 질문.** 진짜로 어렵고 흥미로운 긴장은 #1 + #4 를
함께 두는 것입니다 — *천체 백본에 대해 Principia 의 fixed-step
symplectic 보장을 유지하면서, 플레이어에게 US² 식 정확도/속도 다이얼을
줄 수 있는가?* 깔끔한 답은 아마 per-step adaptivity 가 아니라
**step 크기 선택**(예: 10분 ↔ 2.5분, Principia 가 이미 대조 검증하는
Richardson 쌍) 을 노출하고 worst-offender 진단을 얹는 것입니다. 이러면
symplectic 성질을 지키면서 UX 를 전달합니다. 슐츠 와 함께 가장 먼저
프로토타이핑할 대상입니다.

---

## 7. 열린 질문

- **US² float 정밀도 & floating-origin.** [NO SRC]. 브랜치가 언젠가
  US² 와 수치적으로 상호운용하거나 교차 검증해야 한다면 float64 여부와
  origin-rebasing 방식을 확인해야 하는데, 현재로선 미상이고 출처가
  없습니다.
- **US² 충돌-step 순서.** [INFER only]. step 내부에서 overlap 해소가
  integrator advance 보다 앞에 도는지 뒤에 도는지는 출처가 없습니다.
  Principia 쪽 충돌을 설계할 일이 생길 때만 의미가 있습니다.
- **현재 US² 빌드의 PEFRL 정확한 계수.** [WIKI] 는 PEFRL 기본값이라고
  하지만, 배포 빌드의 정확한 방법/차수는 재작성 이후 개발자가 확인해
  주지 않았습니다.
- **브랜치가 충돌/병합을 원하긴 하는가?** 이 단일 결정이 §6 #2(US²
  에서 파생된 큰 기능) 가 범위 안인지 밖인지를 가릅니다. 엔진 작업에
  앞서 제품 차원의 판단이 필요합니다.

## Related

- [stellarium-binary-orbit-comparison](stellarium-binary-orbit-comparison.md) — 자매 노트. 그쪽은 소스 라인을 인용할 수 있고(오픈소스), 이쪽은 할 수 없다(US² 는 클로즈드)
- [binary-epoch-pipeline](../docs/reference/binary-epoch-pipeline.md) — NearStars 가 Principia 가 적분할 Cartesian 상태를 만드는 방식
- [principia-cfg-reference](../docs/reference/principia-cfg-reference.md) — 이 노트가 비교 대상으로 삼는 Principia cfg/numerics 레이어
