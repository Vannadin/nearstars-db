# R5 — 선체 좌표 표현(vessel coordinate representation) (WS1 commit 4, 설계로 승격)

작성. fable(WS1 commit 1-3 구현 후). 소스 head. 포크 브랜치
`nearstars-interstellar` @ 6c21c5563 (= master 440310a9 + WS1). 상태. 4d +
하드닝까지 IMPLEMENTED(§7 구현 후 부록 2026-07-03 참조). §6 B(commit 4e)는
재결정 중 — §8 참조.

## 0. 문제 (R1이 남겨둔 갭)

WS1은 **backbone**을 국소화했다. 즉 유질량 천체 위치를 서브시스템별 원점 기준으로
저장한다. 선체(vessel)는 손대지 않았다. `Vessel`은 절대 위치를 담은
`DiscreteTrajectory<Barycentric>`를 보유하므로(`vessel.hpp:436`), 4e16 m 떨어진
별에 있는 선체는 여전히 ULP = 8 m다 — 목적지에서의 궤도/착륙 정밀도가 깨지는데,
이게 바로 핵심 게임플레이 시나리오다. 더 나쁜 건, 이제 무질량 커널이 표현을 뒤섞는다는
것이다. `ComputeGravitationalAccelerationByMassiveBodyOnMasslessBodies`는 천체 위치는
LOCAL로 평가하지만(`trajectories_[b1]->EvaluatePositionLocked(t)`) 선체 위치는
호출자로부터 받는다 — 서브시스템이 활성화되는 순간 틀린다. R1 §4의 "렌더링만
globalizing accessor로 라우팅한다"는 이 전부를 과소하게 잡았다.

## 1. 설계가 기대는 아키텍처 사실 (코드로 검증됨)

1. **플러그인 경계에서 선체 상태 I/O는 부모 상대(parent-relative)이지 절대가 아니다.**
   `VesselFromParent`/`CelestialFromParent`는 `RelativeDegreesOfFreedom<AliceSun>`를
   반환하고(`plugin.hpp:334,344`), 언로드된 파트는 `from_parent` 오프셋으로 들어오며
   (`:209-213`), 로드된 파트는 `main_body`에 앵커된 `World`로 들어오고(`:222-233`),
   `InsertOrKeepVessel`은 KSP reference-body 인덱스를 실어 나른다(`:199-204`).
   ⇒ 부모의 저장 DoF가 서브시스템-로컬이면, 절대화된 선체 DoF는 자동으로 같은
   서브시스템-로컬 표현에 안착한다.
2. **ephemeris는 한 곳에서 구성된다** — `Plugin::EndInitialization`(`plugin.cpp:184-230`).
   축적된 `gravity_model_`/`initial_state_` 프로토로부터, 부모 계층 전체를 손에 쥔 채
   (`parents_` 맵) 만든다. ⇒ 파티션을 거기서 계산해 Ephemeris ctor(WS1의 `subsystems`
   파라미터)로 넘길 수 있다. 삽입마다 실을 꿸 필요가 없다.
3. Reference frame / 렌더러는 ephemeris trajectory를 직접 읽고(`plugin.cpp:263-269`,
   `physics/rigid_reference_frame*`), 그 결과를 선체 DoF에 적용한다. ⇒ 손을 봐야 하는
   소비자는 서로 다른 서브시스템의 객체를 섞는 것들뿐이다.

## 2. 설계 원칙

**Barycentric이 유일한 의미론적 프레임으로 남는다.** "서브시스템-로컬"은 *저장 표현*이다.
저장된 모든 `Position<Barycentric>`(천체든 선체든)은 암묵적으로 서브시스템 id로 태깅되며,
두 표현을 섞으려면 원점 간 오프셋을 DoublePrecision으로 재구성해야 한다(WS1 커널 기계장치를
그대로 재사용). 선체는 id 하나만 지닌다. 그 선체의 모든 trajectory(history, psychohistory,
prediction, flight plan)는 그 표현을 공유한다.

## 3. 구성 요소

1. **Ephemeris (headless)** — 공개 accessor `subsystem_of_body(body)`와
   `InterSubsystemOffset(s1, s2)`(DoublePrecision). 무질량 커널은 WS1 분할을 받는다.
   `...OnMasslessBodies`(`ephemeris_body.hpp:1478+`), potential(`:1529+`),
   jerk-on-massless, 그리고 단일 위치 쿼리들. API. `FlowWithAdaptiveStep`(두 overload
   모두)과 `ComputeGravitationalAcceleration/PotentialOnMasslessBody`는
   `int subsystem = 0`을 받고, `NewInstance`/fixed-step은 자신의 trajectory들과 나란한
   `std::vector<int> subsystems = {}`를 받는다(여러 개를 받는다). 기본값 ⇒ 바이트 단위로
   레거시와 동일.
2. **파티션 소스 (plugin)** — 구현된 대로(4b, 승인된 휴리스틱의 단순화). 계층은 아예
   필요 없다 — 클러스터링 패스 하나가 곧 규칙이다. `ClusterSubsystems(positions, threshold)`
   (자유 함수, `physics/ephemeris.hpp`)가 `R_subsystem` = 1e14 m로 단일 연결(single-linkage)
   클러스터링을 한다. 임계값 안에서 사슬로 이어진 천체들은 서브시스템을 공유하고(속박된
   쌍성은 native로 처리됨), 단일 클러스터 결과는 빈 파티션을 반환하므로 stock/RSS 계는
   바이트 단위로 동일한 레거시 경로에 머문다. `SolarSystem::MakeEphemeris`는
   `optional<Length> subsystem_clustering_threshold`를 받아 파티션을 내부에서 계산하고,
   `Plugin::EndInitialization`은 그 상수를 넘기고 결과 파티션을 로깅한다. cfg/proto 변경
   없음. [§6 결정 A]
3. **Vessel** — `subsystem_` int. 삽입 시 부모 천체의 서브시스템으로 설정된다
   (`InsertOrKeepVessel`은 이미 `parent_index`를 가진다). PileUp은 자신의 선체들로부터
   이를 상속한다(같은 위치에 있으므로 ⇒ 동일). 불변식. 선체의 모든 trajectory는 그 표현으로
   저장되고, 무질량-flow 호출이 이를 아래로 넘겨준다.
4. **크로스-서브시스템 소비자 (감사 목록, 수정 = 오프셋으로 globalize하되 double로 붕괴 —
   이 경로들은 mm가 아니라 km 정밀도가 필요하다).** 부모가 다른 서브시스템에 있을 때의
   `VesselFromParent`/`CelestialFromParent`(성간 순항. KSP 부모 = Sun). 중심 천체가 선체와
   다른 서브시스템에 있는 `RigidReferenceFrame`들(계 간 map view). 다른 서브시스템의 선체를
   타깃팅하기. apsides 선체↔천체. `geometric_potential_plotter_`. 같은-서브시스템 경우들 —
   정밀도가 결정적인 것들 — 은 오프셋을 절대 건드리지 않고 정확한 채로 남는다.
5. **Rebase (유일한 새 기계장치)** — 트리거. 선체 언로드됨 ∧ 가장 가까운 서브시스템 앵커 ≠
   현재 ∧ 두 앵커까지의 거리 > `R_void`(기본 1e15 m). 동작. 선체의 모든 trajectory를
   −(offset_new − offset_old)만큼 평행이동(DoublePrecision을 double로 붕괴), `subsystem_`
   설정. 정확성. 모든 앵커에서 >1e15 m 떨어진 곳에서 평행이동 오차는 ≤ ULP(~2e16) ≈ 4 m인데,
   그곳의 주변 중력은 ≲1e-10 m/s²다 — 동역학적으로 무시 가능하고 렌더 스케일에서 안 보인다.
   WS2의 taper가 걸리면 그곳의 힘은 정확히 0이라 rebase는 엄밀하게 glitch가 없다. 일회성
   O(points)이고, 성간 전이당 한 번. 예측과 flight plan은 어차피 일상적으로 재구성된다.
6. **직렬화(Serialization)** — Vessel(및 PileUp) 메시지에 `optional int32 subsystem`
   (`serialization/ksp_plugin.proto:164,114`). 없으면 ⇒ 0 ⇒ 레거시 세이브 그대로.

## 4. 의도적으로 바꾸지 않는 것

C 인터페이스 QP 구조체와 C# 어댑터(parent-relative I/O가 전부 숨긴다). stock-KSP/World
처리. 어디서나 타입으로 쓰이는 `Barycentric`. WS1의 backbone 기계장치.

## 5. 커밋 순서 (4c까지는 Mac에서 각각 headless 테스트 가능)

- **4a** Ephemeris accessor + 무질량 분할 + 파라미터. 테스트.
  `interstellar_precision_test`를 확장해 원격 행성을 도는 무질량 프로브를 넣고 —
  프로브-행성 이격 오차를, 컨트롤(4e16 m에서 subsystem 0 표현, meter 단위) vs
  `subsystem = 1`로 flow한 프로브(sub-mm)로 비교한다. WS1 게이트와 같은 구조.
- **4b** `EndInitialization`의 파티션 + `MakeEphemeris` 실 꿰기(+ `ksp_plugin_test`).
- **4c** `Vessel::subsystem_` + 선체/pile-up flow 전반에 실 꿰기 + rebase + 직렬화
  (+ vessel_test / pile_up_test).
- **4d** 크로스-서브시스템 소비자 감사(§3.4) + 수정. KSP를 건드림. 나중에 Windows에서
  인게임 스모크 테스트가 정말로 필요한 부분.
- **4e** Rebase-aware flight plan + prediction(§6 B). 세그먼트별 서브시스템 태그,
  void 경계에서의 coast-split, 소비자에서의 세그먼트별 globalization. `flight_plan_test`
  / precision 테스트의 크로스-계 plan 시나리오로 headless 테스트 가능.

## 6. 오너 결정이 필요한 사항

- **A. 파티션 규칙 — 결정됨 (오너, 2026-07-02). 계층+거리 휴리스틱 + 클러스터링 패스**
  (§3.2). 실제 팩 구조가 휴리스틱을 무너뜨릴 경우를 대비한 명시적 cfg override 키는 후일의
  탈출구로 남긴다. 상수 `R_subsystem` = 1e14 m, `R_void` = 1e15 m.
- **B. 서브시스템 간 flight-plan 정밀도 — 결정됨 (오너, 2026-07-02). 처음부터 정밀하게.**
  기법. 세그먼트별 서브시스템 태그. void 경계를 넘는 coast 세그먼트는(선체 rebase와 같은
  트리거 규칙) 넘는 지점에서 분할되고, 다음 하위 세그먼트는 목적지 표현으로 이어진다.
  Prognostication/prediction도 같은 처리를 받는다(같은 `FlowWithAdaptiveStep` 이음매).
  plan/prediction trajectory의 소비자는 세그먼트별로 globalize한다. 이는 `flight_plan.cpp`
  (세그먼트 체인)와 `vessel.cpp`(prognosticator)를 범위에 추가한다 — 아래 commit 4e로 추적.
  **[재결정됨 (오너, 2026-07-03). §8의 옵션 1 — 전체-plan rebase를 유지하고 세그먼트별
  태그는 유보. commit 4e는 MVP 경로에서 제외. 인게임 사용에서 원점 쪽 8 m 표시 양자화가
  문제되는 경우가 나타날 때만 재검토. 받아들인 트레이드오프. 선체가 다른 서브시스템으로
  넘어간 후, 자기 과거 trajectory(원점 계에서 비행한 history, map view에 그려짐)와 flight
  plan의 원점 쪽 세그먼트들의 표시 정확도가 ~8 m ULP 격자로 저하된다. 적분 정확도, 다른
  선체들, 원점 계의 backbone은 영향받지 않는다.]**

## 7. 구현 후 부록 (2026-07-03, 4a–4d + 리뷰 + 하드닝 이후)

버틴 것, 그리고 이 설계가 과소 모델링한 것 — WS2/WS3가 교훈을 물려받도록 기록한다.

- **버틴 것.** 저장-표현 원칙(§2), parent-relative 경계 논증(§1.1),
  파티션-at-EndInitialization 단순화(§3.2), 기본값을 통한 하위 호환(upstream 전체 스위트 +
  stock 벤치마크로 바이트 단위 레거시 동일함이 검증됨), 그리고 rebase 트리거 기하(§3.5의
  오차 분석). 전용 부호 규약 감사에서 ~40개 변환 지점이 모두 방향적으로 옳았다.
- **과소 모델링된 것. 상태 라이프사이클.** §3.5는 rebase를 "유일한 새 기계장치 … 예측과
  flight plan은 어차피 일상적으로 재구성된다"고 불렀다. 실제로는 선체 상태의 *stale 사본*을
  쥔 곳이 다섯 군데 있었고 rebase는 그중 어느 것에도 통지하지 않았다. checkpointer(이 문서에서
  아예 빠져 있었다), reanimator 스레드, prognosticator 스레드, 지연 직렬화된 flight plan,
  그리고 optimization-driver 사본. 12각도 리뷰(2026-07-03)의 CONFIRMED 발견 10건 전부가 이
  다섯 경로에 있었고, 전부 저장된 모든 trajectory를 *스스로를 서술하게*(checkpoint별 / plan별 /
  prognostication별 서브시스템 태그) 만듦으로써 수정된다 — 누적 오프셋으로 땜질하는 대신.
  **미래 기계장치를 위한 규칙. 선체/plan 상태의 어떤 변형이든, 코딩 전에 그 상태 사본을 쥔
  비동기·직렬화 보유자들을 전부 열거하라.**
- **§3.4 감사 목록은 범주적으로는 옳았으나 수치적으로 절반만 완성됐다.** 실제 4d 감사는
  ~2배의 지점을 찾았다(렌더러 World/sun 앵커링, planetarium 차폐 구, main-body 프레임을 통한
  파트 로딩, navball, orbit-analyser 내부, optimizer 거리들).
- §4의 "C 인터페이스가 전부 숨긴다"에는 딱 하나의 누수가 있었고
  (`FlightPlanGetManoeuvreInitialPlottedVelocity`), 수정됐다.

## 8. 4e 옵션 (§6 B에 대한 오너의 재결정용)

2026-07-02 결정 이후 바뀐 맥락. (a) 전체-plan `FlightPlan::Rebase` — 결정 시점엔 (모르게)
깨져 있었는데 — 이제 수정·테스트됐다. (b) 4d가 ~15개 소비자 시그니처에 TRAJECTORY당 표현
하나의 `int subsystem`을 꿰었는데, 세그먼트별 표현으로 가면 이걸 다시 열게 된다.

**옵션 1(전체-plan rebase 유지, 4e 생략/유보)의 잔여 오차.**
- rebase 시의 일회성 seed 평행이동 오차. ≤ 4 m(붕괴된 4×10¹⁶ m 오프셋의 half-ULP). 그곳의
  주변 중력은 ≤ ~1.3×10⁻¹⁰ m/s²(10¹⁵ m에서 μ ≈ 1.3×10²⁰ m³/s²)이므로, 4 m의 동역학 효과는
  ~10⁻²⁴ m/s²로 없는 셈이다. WS2의 taper가 걸리면 그곳의 힘은 정확히 0.
- rebase 후 전체 plan은 목적지 표현으로 재적분되므로, 여전히 원점 별 근처에 있는 세그먼트들은
  표현 원점에서 ~4×10¹⁶ m에 앉는다. 그 위치들은 8 m ULP 격자 위에 있다(WS1 이전 정밀도) — 다만
  그것들은 *과거*(이미 비행했거나 출발 인접) 세그먼트다. 목적지 근처의 남은/미래 세그먼트는
  정확하다. 원점 계에서 여전히 파라미터화된 기동은 정확한 시각과 Δv를 유지하고, 표시되는
  기하만 ~8 m로 양자화된다.
- 순효과. 불연속 없음, 드리프트 없음. rebase 이벤트에서의 일회성 미터 스케일 계단과 원점 쪽
  history의 8 m 표시 양자화. 렌더 스케일에서 안 보인다.

**옵션 2(세그먼트별 태그, 원래의 4e)의 비용.**
- FlightPlan. 세그먼트별 서브시스템 태그 + void 경계에서의 coast split(트리거 = §3.5 규칙) +
  태그 직렬화(proto 변경) + 분할 너머의 기동 부기.
- Prognostication/prediction. 같은 분할 처리.
- 소비자. 4d에서 꿴 ~15개 시그니처는 trajectory당 표현 하나를 가정한다
  (`Plugin::ComputeAndRender*`, `Renderer::Render*`, `Planetarium::PlotMethod4`, 인터페이스
  호출자들) — 각각이 세그먼트-aware가 되거나, FlightPlan이 소비용으로 정규화된 단일-표현 뷰를
  노출해야 한다(그러면 피하려던 붕괴가 다시 들어온다).
- 새 세그먼트별 상태에 대한 추가 라이프사이클 감사(§7 규칙에 따라).
- 예상 공수. 4c-1+4c-2를 합친 것과 비슷(~2–3 커밋 + 리뷰) vs 옵션 1은 ~0.

**옵션 2가 옵션 1보다 사는 것.** mid-void rebase 후 원점 쪽 plan 세그먼트의 *표시* 정밀도가
8 m 대신 sub-mm가 되고, 아직 rebase 안 된 상태에서의 크로스-void plan 기하가 mm-정확해진다.
비행된 trajectory의 적분 정확도는 바꾸지 않는다(선체 자체는 항상 자기 표현으로, 정확하게
적분한다).

**권고 (fable).** 지금은 옵션 1(활성화 + end-to-end 테스트로 진행). 인게임 사용에서 원점 쪽
8 m 표시 양자화가 문제되는 경우가 나타날 때만 옵션 2를 재검토.

**결정됨 (오너, 2026-07-03). 옵션 1.** rebase된 선체의 과거-trajectory 표시(map view에서의
원점-계 history)와 flight plan의 원점 쪽 부분이 넘어간 후 ~8 m로 양자화된다는 트레이드오프를
명시적으로 받아들인다.
