---
title: R7 — Principia 하의 Warp/FTL 지원 — 현재 코드 재근거화, 실패 카탈로그, 접근 결정
status: research complete (2026-07-04)
grounds: WS4 (ws4-warp-support-backlog.md)
---

# R7 — Warp/FTL 지원. 실현 가능성, 접근법, 그리고 철저한 실패 카탈로그

## 0. 이 문서가 무엇인가 — 그리고 무엇을 의도적으로 다시 도출하지 않는가

NearStars는 **이미 성숙한 warp 코퍼스를 가지고 있다**(2026-06-30 작성, WS1/WS2/WS3가
성간 포크에 안착하기 전). 이 R7은 그것을 **중복하지 않는다** — 먼저 그것들을 읽어라.

- `gameplay/interstellar-expansion/warp/warp-and-navigation-brainstorm.md` — `[src]`
  소스 분석 + **옵션 사다리**(no-fork / minimal-fork / big-fork C ABI) + 순항 아키텍처 +
  도착-속도 프레임 논의.
- `gameplay/interstellar-expansion/warp/warp-patch-draft.md` — **선택된 minimal-fork
  패치**(`UnmanageabilityReasons` OR-항 하나) + 순항-플러그인 뼈대.
- `gameplay/interstellar-expansion/warp/warp-drive-energetics.md` — ADS 인용 Alcubierre
  물리(warp가 왜 적분 가능한 힘이 아니라 **상태 불연속**인지). `warp_exotic_matter.py`
  = 게임플레이 연료 모델.
- `plugins/NearStarsWarp/` — 초안 C#(`WarpCruise`, `WarpDriveModule`, `PrincipiaInterop`,
  `WarpFlagBridge`), `VERIFY`/`REQUIRES FORK` 마커 포함.
- `plans/principia-interstellar-branch/ws4-warp-support-backlog.md` — 오너 승인 백로그
  스텁. big-fork `VesselWarpTo` C ABI를 "예상되는 형태(리서치 패스로 확정할 것)"로
  스케치했다 — **이 문서가 그 리서치 패스다.**

**R7의 고유 기여**(2026-06-30 코퍼스가 할 수 없었던 것). **현재** 포크 코드에 대한 재근거화
— 이제 그 코드는 subsystem(WS1), checkpointer/reanimator + rebase 라이프사이클(R5),
무힘 void(WS2/WS2b), WS3 journalled-API 레시피를 실었다 — 여기에 철저한 실패 카탈로그와
해결된 접근 결정을 더한다. 방법. 살아 있는 코드에 대한 다섯 개의 병렬 소스-매핑 패스
(DiscreteTrajectory, prediction/flight-plan, checkpointer/rebase, WS3 API 레시피, warp-mod
선행 기법). Line 앵커는 head `e6a0225cd`의 포크 기준이다. **코딩 전에 재확인하라**(Principia는
매달 rebase한다).

---

## 1. 실현 가능성 판정

**실현 가능하고, WS3보다 실질적으로 더 단순하다** — KB가 이미 고른 minimal-fork 경로로.
big-fork `VesselWarpTo` C ABI *또한* 실현 가능하지만, minimal-fork가 거의 전부 우회하는
크고 취약한 표면(§3.A–B)에 부딪힌다. 물리가 틀을 결정짓는다. Alcubierre warp는 **proper
가속도도, 국소 운동량 변화도 만들지 않으므로**(승무원은 버블 안에서 자유낙하 중이다), warp에는
**정직한 연속 trajectory 표현이 없다** — 그것은 선체 자유도의 불연속이다. 그래서 아래의 모든
설계는 어떤 형태로든 "옛 trajectory를 종료하고 새 것을 다시 seed한다"이다. 다른 점은 불연속을
*어디서* 표현하고 *얼마만큼의 기계장치*가 그것을 견뎌야 하는가뿐이다.

---

## 2. 두 전략 (plan의 스텁을 KB 코퍼스와 화해시키기)

WS4 스텁(plan 디렉토리)과 warp 코퍼스(gameplay 디렉토리)는 **서로 다른** 구현 전략을
가리킨다. 이것은 오너가 비준해야 하는 진짜 갈림길이다. R7은 minimal-fork를 권한다.

| | **Minimal-fork (KB 선택)** | **Big-fork `VesselWarpTo` (스텁 스케치)** |
|---|---|---|
| 메커니즘 | `ksp_plugin_adapter.cs`의 `UnmanageabilityReasons(Vessel)`에 OR-항 하나를 추가. warp 플래그가 올라간 동안 Principia는 그 선체 관리를 멈추고, NearStars 순항 레이어가 stock KSP 호출로 그것을 움직인다. dropout 시 플래그 해제 → Principia가 새 stock 궤도로부터 `CreateTrajectoryIfNeeded`(`trajectory_.empty()` 가드, `vessel.cpp` ~232–256)로 신선한 trajectory를 다시 seed. | 새 journalled 플러그인 API(WS3 레시피). history를 종료하고, 목적지 DoF에서 불연속-표시된 점을 append / 새 세그먼트를 열고, subsystem rebase를 트리거하고, prediction을 갱신. |
| Trajectory 불연속 | **표현할 것 없음** — C++ `Vessel` + 그 `DiscreteTrajectory`가 detach 시 파괴되고 새로 다시 만들어진다. | 제자리에서. 전체 DiscreteTrajectory + reanimation 지뢰밭에 부딪힌다(§3.A–B). |
| Fork 표면 | **1줄, 어댑터 안**(NearStars가 이미 포크하는 곳). 안정적 필터에 살아 → 가벼운 월간 rebase. | journal.proto + 생성물 ×5 + plugin.cpp + interface + trajectory-reseed + reanimation checkpoint 강제 + 렌더링 break. 적분기 인접. |
| warp 시 flight plan | 소실, 목적지에서 replan(수용됨). | 원칙적으론 살아남을 수 있으나, §3.C가 속도 변경 점프에서는 어차피 reset해야 함을 보인다. |
| Principia-관리 timewarp 중 작동 | 아니오 — warp는 unmanaged인 동안 일어난다(자체 순항 시계). | 예 — 하지만 warp는 *순간적*이라 이득이 작다. |
| History 정직성 | **간극(gap)**(Principia에는 순항 구간의 trajectory가 없다). | 불연속-표시된 준-연속 기록. |
| Save/load | Trajectory가 파괴/재생성됨 → 직렬화할 exotic한 것 없음. GUID/parts/crew는 살아남는다. | 다시-seed가 직렬화된 trajectory를 바꿈 → 지속되지만, history 중간 불연속은 로드 시 `ConsistencyStatus` CHECK(§3.F) 위험. |
| 판정 | **권장.** | 미래 기능이 in-sim warp-기동 계획을 필요로 할 때만. 유보. |

실패 카탈로그(§3)가 논거다. big-fork 경로의 추가 능력은 크고 취약한 표면을 대가로 치르고,
그것이 제공하는 유일한 정직한 것(기록된 불연속)은 warp가 어차피 존중할 수 있는 물리적 의미가
없다.

---

## 3. 실패-모드 카탈로그 (핵심 산출물)

**[big]** = big-fork 전용, **[both]** = 어느 전략이든 영향, **[min]** = minimal-fork
특유. 대략 심각도순.

### A. DiscreteTrajectory는 세그먼트 이음매에 불연속을 담을 수 없다 **[big]**
- 점프는 **단일 세그먼트 안**, 연속한 두 점 사이에서만 존재할 수 있다 — 세그먼트 경계에서는
  결코 안 된다. `ConsistencyStatus`는 세그먼트 N의 마지막 점 == 세그먼트 N+1의 첫 점을 시간과
  자유도 모두에서 요구하고(`discrete_trajectory_body.hpp:862-904`), 모든 mutator가
  `CHECK_OK(ConsistencyStatus())`로 끝난다(`:181,199,240,265,308,460`) → 즉시 abort.
  `AttachSegments`는 일치하는 DoF를 hard-`CHECK_EQ`한다(`:211`). `NewSegment`는 이전 마지막
  점을 *강제로 복제*하므로(`:172-174`), 깨끗한 이음매를 만들어낼 수조차 없다.
- **세그먼트 내부(intra-segment)** 점프 → 두 점 사이의 Hermite cubic이 양 끝점의 위치+속도로
  만들어지는데(`discrete_trajectory_segment_body.hpp:137-169,646-659`), 큰 Δposition이나
  불일치 속도는 보간을 미친 듯이 overshoot하게 한다. 끝점은 정확하고, 내부는 쓰레기다 — 그리고
  중간 시각을 샘플링하는 모든 소비자(렌더링, flight-plan seeding, prognostication)가 그
  쓰레기를 읽는다.
- Downsampling 오차 누적이 점프 주변에서 오염된다(`:443-475`). 점프 항이
  `downsampling_error_`를 지배하고, baseline은 retained-point 분기에서만 리셋되므로(`:470`),
  인근의 정당한 점들이 잘못 버려지거나 유지될 수 있다.
- zfp 손실 압축은 non-endpoint, non-`exact` 점을 `tolerance`까지만 재구성한다
  (`:725-796`). 미터 스케일 점들 사이의 km 스케일 점프는 이웃을 번지게 한다.
- **A 전체가 minimal-fork에서는 사라진다** — 파괴+재생성된 trajectory에는 표현할 점프가 없다.

### B. Reanimation은 불연속한 과거를 *지운다* **[big]**
- Reanimation은 각 과거 세그먼트를 물리 적분기로 **재적분**해 꿰맞춘다
  (`ephemeris_body.hpp:1268-1314`. 선체. `FlowWithFixedStep`, `vessel.cpp:1304`). 위치 점프는
  적분으로 재현 불가능하다 → 재구성된 과거는 매끄러운 물리 trajectory가 되어 저장된 warp-이후
  점들과 **모순**된다. warp 순간에 **정확히** checkpoint를 강제해 점프가 checkpoint 경계에
  안착하지 않는 한, 불연속은 사라진다.
- 꿰맞춤은 이어서 `CHECK_EQ(t_initial, reanimated.back().time)`을 assert하고
  (`vessel.cpp:1283`), 불일치 시 경고/간극을 낸다(`ephemeris_body.hpp:1302-1305`). `Merge`는
  구간이 겹치면 `LOG(FATAL)`한다(`discrete_trajectory_segment_body.hpp:551-556`). checkpoint
  구간에 걸친 warp는 잠복 크래시다.
- **Minimal-fork는 이를 피한다** — warp-이전 `Vessel`은 사라졌고, reanimate할 불연속한 과거가
  없다.

### C. Prediction, flight plan, 기동 **[both, 단 minimal-fork에서는 저렴]**
- Prediction은 `psychohistory_->back()`에 앵커된다(`vessel.cpp:664-669`). 새 prognostication이
  없으면 stale prediction 세그먼트가 **재사용**된다(`:461-465`). warp는 `prediction_`을
  강제로 버리고, prognosticator를 멈추고(`StopPrognosticator`, `:691-693`), 다시 예측해야
  한다 — 안 그러면 옛 상태로 seed된 async 결과가 쓰레기로 붙는다(`AttachPrognostication`은
  *subsystem*만 교정하지 물리적 점프는 못 한다, `:1457-1463`).
- flight plan은 자기 자신의 고정된 `initial_degrees_of_freedom_`을 쥐고 있고
  (`flight_plan.hpp:254`), `FlightPlan::Rebase`는 *위치만 평행이동하고 속도는 유지*한다
  (`flight_plan.cpp:462-464`). 그래서 속도 변경 warp는 기존 rebase로 **표현할 수 없다** —
  plan을 reset해야 한다. 계획된 burn window 안에 착지하는 warp는 명시적으로 거부된다
  (`UnavailableError`, `vessel.cpp:618-621`).
- 기동 추력/Frenet 프레임은 캡처된 초기 상태에서 파생되고(`manœuvre_body.hpp:231-234`),
  전체 `ComputeSegments` 재계산으로만 갱신된다 — 유효한 새 앵커 없는 rebase는 조용히 틀린 Δv
  방향을 준다(크래시 없음).
- 돌고 있는 `FlightPlanOptimizationDriver`는 warp-이전 plan의 사본을 쥐고 있다
  (`flight_plan_optimizer.hpp:223`). `RebaseIfNeeded`가 하는 그대로 정확히 중단해야 한다
  (`vessel.cpp:196-198`).
- **Minimal-fork에서는 이 모두가 공짜다.** flight plan/prediction은 파괴된 Vessel과 함께
  죽고 목적지에서 다시 만들어진다. 이것이 수용된 "warp 시 flight-plan 소실"이다.

### D. 다시-seed 시 subsystem 할당 — WS1 교차점 **[해결됨. minimal-fork에서는 자동 교정. big-fork는 처리해야 함]**
- warp 목적지는 *다른* subsystem(다른 별)에 있으므로, 다시-seed된 선체는 목적지 subsystem으로
  태깅되고 그 subsystem의 로컬 원점 기준으로 trajectory가 표현되어야 한다 — 안 그러면 잘못된
  원점 대비 광년 스케일에 착지한다. 이것이 WS1이 막으려 존재하는 FP-정밀도 재앙이다
  (`ToRemoteSystem`은 테스트에서 4e16 m다).
- **라이프사이클이 minimal-fork에 대해 이를 자동으로 해결한다(§9.1 참조).** unmanaged 선체는
  지속되지 않고 *파괴*된다. 어댑터가 그 선체에 대해 `InsertOrKeepVessel`을 건너뛰므로
  (`ksp_plugin_adapter.cs:1314-1321`) `kept_vessels_`에서 빠지고,
  `FreeVesselsAndPartsAndCollectPileUps`가 `vessels_.erase(it)`을 한다(`plugin.cpp:626`).
  다시-adopt 시 **완전히 새로운** `Vessel`이 `subsystem_ = ephemeris->subsystem_of_body(parent->body())`로
  생성되고(`vessel.cpp:93`), 부모는 `vessel.mainBody`인데 순항 레이어가 이를 목적지 별로
  설정해 두었다. 그래서 신선한 선체는 목적지 subsystem을 *공짜로* 얻고, 파트들의 DoF는
  `InsertUnloadedPart`(`plugin.cpp:446-455`)에 의해 그 (올바른) 원점으로 변환된다.
  **다시-seed subsystem fork는 필요 없다.** (내 이전 "subsystem fork 필요" 판단은 일어나지
  않는 persist-and-reseed 모델에 기반했다 — 선체는 파괴된다.)
- **Big-fork(제자리 다시-seed)는 이를 필요로 한다.** 지속된 `Vessel`은 옛 `subsystem_`을
  유지하고(`set_parent`은 이를 바꾸지 않음, `vessel.cpp:206-210`), `RebaseIfNeeded`는 가까운
  도착에서는 발동을 거부한다(`nearest_distance <= 1e15 m` early-return, `vessel.cpp:167-169`).
  재사용 가능한 프리미티브는 `RebaseIfNeeded`의 본문이다(`vessel.cpp:172-190`.
  `subsystem_conversion` → `trajectory_.Translate` → `subsystem_ = target` →
  `ForAllParts(set_subsystem)` → `PileUp::Rebase`). 이를 거리 게이트를 우회하는
  `Rebase(int target_subsystem)`로 뽑아내고, DoF가 쓰이기 *전에* subsystem을 설정하라(그래야
  `DoublePrecision`을 단일 `Displacement`로 붕괴시키는 `subsystem_conversion`,
  `ephemeris_body.hpp:312-316`이, 올바른 subsystem에 앵커하는 것의 대용이 아니라 오직 원점
  *사이*를 옮기는 데만 쓰인다).

### E. 동시성 / 백그라운드 스레드 **[both]**
- rebase 평행이동은 reanimator가 `trajectory_.front()`를 그 락 아래에서 읽기 때문에 의도적으로
  `lock_` 아래로 옮겨졌다(`vessel.cpp:177-182`, commit `aa557ec4e`). `trajectory_`/`subsystem_`을
  락 밖에서, 또는 pile-up이 전진되는 동안(불변식 `plugin.cpp:845-846`) 변형하는 warp는
  reanimator/prognosticator와 경쟁(race)한다.
- `PileUp::Rebase`는 "pile-up이 전진되는 동안 호출되면 안 된다"고 문서화한다
  (`pile_up.hpp:139`) — 어떤 다시-seed든 같은 제약이다. 안전한 호출 지점.
  `CatchUpLaggingVessels`(`plugin.cpp:842-851`)와 `CatchUpVessel`(`:888-890`).

### F. Save/load **[both, 전략에 따라 다름 — subsystem-파티션 세부는 §9.3 참조]**
- Minimal-fork. exotic한 것 없음. 순항 동안 선체는 순전히 stock-쪽이므로(Principia가 파괴함),
  순항 중 세이브는 그냥 그것을 직렬화하지 않고, 로드 시 KSP가 다시 만들고 warp가 끝날 때
  Principia가 신선하게 adopt한다. 다시-adopt된 선체의 `subsystem_`은 기존 WS1 필드로 round-trip
  한다(`vessel.cpp:746`, 없으면⇒0). GUID/parts/crew는 내내 살아남는다.
- Big-fork. 세그먼트 내부 불연속은 연속으로 다시-append될 때만 round trip을 견딘다. 이음매
  표현은 `ReadFromMessage`의 `CHECK_OK(ConsistencyStatus())`를 크래시시킨다
  (`discrete_trajectory_body.hpp:736`). rebase-이전의 누적-오프셋 방식은 이미 save/load를 한 번
  실패시켰다(commit `7a21103d3`) — checkpoint별 subsystem 태그 대신 어떤 암묵/누적 오프셋에라도
  기대는 warp는 round-trip하지 않는다.

### G. 렌더링 **[big]**
- `RenderBarycentricTrajectoryInPlotting`은 gap 검출 없이 모든 점을 append한다
  (`renderer.cpp:104-125`) → 점프에 걸친 psychohistory→prediction 사슬이 warp를 가로지르는
  가짜 직선을 그린다. warp 순간에 명시적 trajectory break가 필요하다. **Minimal-fork.**
  간극에 걸친 렌더 경로가 없다(옛 trajectory가 사라졌다).

### H. warp-mod interop은 기본적으로 적대적이다 **[both]**
- Principia의 권위적-상태 모델은 **매 프레임 KSP transform을 덮어쓴다**
  (`ksp_plugin_adapter.cs UpdateVessel` ~516-525). stock warp mod의 어떤 외부
  `SetPosition`/`Orbit.UpdateFromStateVectors`든 읽히고 그 평행이동은 같은 프레임에 버려진다.
  이것이 HyperEdit/Blueshift가 "효과가 없는" 문서화된 이유이고(Principia issue #1420, wontfix),
  FAQ가 Blueshift를 비호환으로 나열하는 이유다("이 변경들은 Principia에 의해 즉시 되돌려진다…
  Principia가 이긴다").
- ⇒ 우리는 stock warp mod를 그냥 설치할 **수 없다.** (min) 권위 레이어에서 선체를 detach해
  순항 구간 동안 stock 호출이 먹히게 하거나, (big) Principia 자체 모델 안에서 이동을 한다.
  외래 warp mod들(KSPIE = `Orbit.UpdateFromStateVectors` 속도 주입. Blueshift = 프레임별
  `Vessel.SetPosition`)은 각각 우리 hook을 호출해야 한다. 우리 자체의 최소 warp 파트를 배포하는
  것(`plugins/NearStarsWarp/` 초안처럼)이 외래 mod를 패치하는 것보다 깔끔하다.

### I. 속도-프레임 / 도착 상대 속도 **[해결됨. 속도는 subsystem 간 프레임-불변. v0 보존은 순항-쪽이지 fork 아님 — §9.2 참조]**
- KB는 **(a) barycentric 보존**을 골랐다. 선체의 Sol-barycentric 관성 속도 v0을 warp 내내
  유지해, 참된 성간 상대 속도 `v_rel = v0 − v_deststar`를 실은 채 도착하게 한다(제동 leg가
  깎아내는 *쌍곡선* 도착 — 의도된 리얼리즘. 항법 planner가 이미 이를 계산한다).
- **핵심 사실(확인됨).** subsystem 로컬 원점들은 **상수** 변위만큼 차이 난다(상대 속도 0.
  `subsystem_origin_offset_`은 시간-독립 `Displacement`, `ephemeris_body.hpp:194,325`. jerk
  커널 주석 "속도는 영향받지 않는다. 원점 오프셋이 상수다", `:1524`). 그래서 속도 벡터는 모든
  subsystem 프레임에서 **동일**하다 — subsystem 변경은 순수 위치 rebase다
  (`SubsystemConversionMotion`은 항등 회전과 정지 프레임 속도를 가진 RigidMotion,
  `plugin.cpp:1911-1921`).
- **전략별 결과(§9.2 참조).** *직접-DoF* 다시-seed(big-fork)는 v0을 자동 보존한다. *stock-궤도*
  다시-seed(minimal-fork)는 barycentric 속도를 `v_deststar + v_orbit`로 설정하므로
  (`plugin.cpp:446-447`), 순진한 속박 stock 궤도는 선체를 **목적지 별과 함께 움직이는 parking
  궤도에 놓아 성간 Δv 전부(수십 km/s)를 플레이어에게 조용히 공짜로 넘겨준다.** 수정은
  **순항-쪽, fork 없음**이다. dropout stock 궤도를 상대 속도 `v_orbit = v0 − v_deststar`로 쓰면
  barycentric은 `v_deststar + (v0 − v_deststar) = v0`이 되어 — 현실적인 쌍곡선 도착이 된다.
  순항 레이어는 이미 v0을 캡처했고 `v_deststar`를 조회할 수 있다.
- 속도의 World→Barycentric은 회전만 하는 `OrthogonalMap`(`renderer.cpp:344-347`)이 아니라
  완전한 `RigidMotion`(ω×r 항 포함, `plugin.cpp:481-496,762-816`의 손으로 조립한 motion)이
  필요하다 — warp가 게임 프레임에서 속도를 읽을 때만 유관하다.

---

## 4. 권장 구현 계획 (minimal-fork)

**심층 분석(§9)이 minimal-fork가 정말로 ~어댑터 한 줄임을 확인한다** — subsystem 할당은
자동(목적지 부모로부터 신선하게 생성)이고 속도 보존은 순항-쪽(dropout stock 궤도의 상대 속도를
고름)이다. `warp-patch-draft.md` §1–5를 따르되, R7의 다음 **현재-코드 델타**를 적용한다.

1. **유일한 fork.** 포크의 `ksp_plugin_adapter.cs`에서 `UnmanageabilityReasons`에 OR-항 하나를
   추가한다(초안의 ~620–660은 2026-06 master 기준. 포크는 갈라졌다 — 줄을 재확인하라).
   stock-필드 warp 플래그를 키로 삼되(Principia↔NearStars 컴파일 의존을 피하려 `KSPField`/GUID-맵을
   이름으로 읽음). unmanaged ⇒ 선체는 파괴된다(§9.1). dropout 시 목적지-별 stock 궤도로부터 신선하게
   다시-adopt된다.
2. **Subsystem. 할 것 없음(§9.1).** 다시-adopt된 선체는
   `subsystem_ = subsystem_of_body(mainBody = 목적지 별)`(`vessel.cpp:93`)로 생성됨 → 자동으로
   올바르다. 다시-seed subsystem fork 없음. (이전의 "§3.D는 fork가 필요"는 철회. big-fork
   제자리 경로에만 적용된다.)
3. **속도. 순항-쪽(§9.2).** dropout stock 궤도는 상대 속도 `v_orbit = v0 − v_deststar`를 실어
   barycentric seed가 v0(현실적 쌍곡선 도착)이 되게 해야 한다. 속박 parking 궤도(성간 Δv를
   선물함)가 아니다. `WarpCruise`의 순수 C#. fork 없음. v0 캡처 프레임 == Principia가 seed하는
   barycentric 프레임임을 확인하라.
4. **WS2가 warp 진입/이탈을 깨끗하게 만든다** — mid-void에서 detach/다시-seed하는 선체는 정확히
   0의 배경 힘을 본다(WS2/WS2b. 기계 정밀도까지 무힘). 그래서 화해할 tail 힘이 없다. 긍정적
   교차점. warp는 정확히 일어나는 곳에서 수치적으로 가장 깨끗하다.
5. **목적지는 파티션된 천체여야 한다(§9.3)** — 로스터에서는 항상 참이다(모든 별은 초기 ephemeris
   구성 시 파티션된 천체다). 런타임에 새 subsystem은 생성될 수 없다. 기존 subsystem이 아닌 warp
   타깃은 hard-CHECK-fail한다.
6. 순항 레이어(`plugins/NearStarsWarp/`)는 NearStars-쪽(슐츠의 레인)이다. `WarpCruise` 상태
   기계, ExoticMatter 연료, `WarpFlagBridge`. patch-draft §5 체크리스트를 검증하라(detach가
   kept-set에서 드롭. dropout이 올바른 subsystem/속도로 다시-adopt. 파트/승무원 손실 없음.
   detach→cruise→re-adopt에 걸친 save/load).

만약 오너가 대신 **big-fork** 경로를 원하면, WS3 레시피가 그대로 적용된다(journal.proto 확장 +
generator 실행 + plugin.cpp 메서드 + interface_vessel.cpp 마셜링). 여기에 더해. `RebaseIfNeeded`에서
뽑아낸 명시적 `Rebase(target_subsystem)` 프리미티브(§3.D), warp 순간의 강제 checkpoint(§3.B),
한 세그먼트 이음매의 `ConsistencyStatus`/`AttachSegments` CHECK 완화(§3.A), 렌더 경로 break(§3.G).
속도는 여기서 *자동으로* 보존된다(§9.2). 추정 공수는 minimal-fork의 3–5배 — 그리고 그것이 사는
것은 in-sim managed-timewarp warp + 기록된 불연속뿐인데, mod 기능에는 둘 다 필요 없다.

---

## 5. 안정성 계획

- **골든 테스트(어느 전략이든).** 선체를 Sol→원격-계로 warp한 뒤 10년 coast를 하고, 목적지 별
  둘레의 도착 궤도가 안정적이며 올바른 subsystem에 표현됨을 assert한다(WS1의
  `FarFieldDampedCoast`/rebase e2e 테스트를 확장).
- **Reanimation 테스트(big-fork 전용).** warp 직후 세이브, warp 순간을 지나 reanimation을 강제,
  `ConsistencyStatus`/`Merge` 크래시가 없고 warp 순간이 checkpoint 경계에 앉음을 assert.
- **동시성.** reanimator/prognosticator가 활성인 동안 warp를 돌리고(§3.E race), 락 규율이
  유지됨을 assert.
- **Interop 회귀.** warp 플래그가 없는 선체는 여전히 완전 관리됨을 확인(OR-항의 스코프가 정확해야
  한다).
- **Save/load.** 순항 중 세이브(minimal-fork. 선체가 unmanaged — 로드 시 올바르게 다시-adopt됨을
  확인)와 방금-warp한 세이브를 round-trip.

## 6. 최적화

- warp는 **순간적**이다 — step별 비용이 없으므로 최적화할 hot path가 없다. 유일한 비용은 일회성
  다시-seed + (big-fork) 강제 checkpoint + prediction 갱신이다.
- 유관한 효율 관심사는 매 warp마다 전체 reanimation을 다시 트리거하지 **않는** 것이다. warp 순간의
  강제 checkpoint(big-fork)가 reanimation을 warp-이후 세그먼트로 제한한다. Minimal-fork는 이런 게
  전혀 없다 — 신선한 Vessel은 animate-at-birth checkpointer로 시작한다(`ephemeris.hpp:698` 근거).

## 7. 미해결 질문 / 오너 결정

1. **Minimal-fork vs big-fork** — R7은 **minimal-fork**를 권한다(§3 카탈로그가 논거이고, §9는
   그것이 정말로 ~어댑터 한 줄임을 보인다). 오너 비준. 이는 plan 스텁(big-fork를 스케치)을 KB
   코퍼스(minimal-fork를 선택)와 화해시킨다.
2. ~~다시-seed 시 subsystem 할당~~ — **해결됨(§9.1).** minimal-fork에서 자동(목적지-별 부모로부터
   신선 생성). big-fork만의 관심사.
3. ~~도착 속도 프레임~~ — **해결됨(§9.2).** 속도는 subsystem 간 프레임-불변. barycentric-보존은
   순항-쪽(dropout 궤도의 상대 속도를 고름). fork 없음.
4. **도착 난이도를 옵션으로(신규 — 오너의 아이디어 2026-07-04).** v0 보존이 전적으로 순항 레이어의
   dropout stock-궤도 속도 선택(§9.2)이므로, 도착 체제는 추가 코드 0의 **자유 난이도 토글**이다.
   - *현실적 / 어려움.* `v_orbit = v0 − v_deststar` → 쌍곡선 도착, 플레이어는 참된 성간 접근
     속도(수십 km/s)를 제동으로 깎아내야 한다.
   - *캐주얼 / 쉬움.* 속박 parking 궤도 → 선체가 목적지 별과 함께 움직이며 도착(성간 Δv 면제).
     이것이 "순진한" 거동이지만 — 버그가 아니라 *선택된* 옵션이다. 난이도/게임-설정 또는
     `WarpCruise`의 drive별 tunable로 노출.
5. **우리 자체 warp 파트를 배포할까 외래 mod를 패치할까(§3.H)?** KB는 자체 배포로 기운다
   (`plugins/NearStarsWarp/`). 외래-mod interop은 mod별 작업이다.

## 8. WS4 스텁 정정 — issue #2347

WS4 백로그 스텁과 브레인스토밍은 warp를 "PersistentThrust와 같은 비호환(Principia issue #2347)"
이라 부른다. **Issue #2347은 실은 "Burn in time warp with RO ion engines"**로 — timewarp 하에서의
지속 저추력 기능 요청이며, 여전히 **열려 있고** teleport 이슈가 아니다. 유지보수자들의 anti-warp
입장은 트래커가 아니라 **FAQ**에 산다. "엔진 없이 (1) 또는 timewarp 중에 (2) 선체를 움직이거나
궤도를 바꾸려는 어떤 mod든 Principia와 비호환"이라며 **Blueshift를 명시적으로** 이름 짓는다.
Principia 트래커에는 전용 Alcubierre/warp/teleport 이슈가 없다(검색됨. #2347, #2185 warp-*to-node*,
#4223 표면-teleport 버그뿐). 근본 원인 특징화("엔진 없이 / timewarp 중에 못 움직임")는 방향적으로
옳다. 이슈 번호/제목은 아니다. → 스텁의 인용을 고쳐라.

## 9. 심층-분석 부록 (2026-07-04) — minimal-fork를 단순화하는 세 발견

세 개의 후속 소스 패스(subsystem 할당, 속도 프레임, 직렬화) + unmanaged-vessel 라이프사이클의
직접 읽기. 이들이 함께 minimal-fork가 **C++ 다시-seed fork가 필요 없고** — 어댑터 한 줄만 필요함을
보인다.

### 9.1 Unmanaged ⇒ 파괴 ⇒ 신선 생성 ⇒ 올바른 subsystem (load-bearing 라이프사이클)
- 어댑터는 관리 불가 선체에 대해 `InsertOrKeepVessel`을 건너뛴다. `if (unmanageability_reasons
  != null) { … continue; }`(`ksp_plugin_adapter.cs:1314-1321`). 선체는 `InsertOrKeepVessel`
  *안*에서만 `kept_vessels_`에 추가되므로(`plugin.cpp:425`), unmanaged 선체는 유지되지 않는다.
- 이어 `FreeVesselsAndPartsAndCollectPileUps`가 그것을 **파괴**한다. kept 선체는
  `CreateTrajectoryIfNeeded` 분기를 타고(`plugin.cpp:617-619`), non-kept 선체는
  `vessels_.erase(it)`에 부딪힌다(`plugin.cpp:626`) — 소유 `unique_ptr<Vessel>`(trajectory,
  flight plan, subsystem)이 해제된다. KSP GUID/parts/crew는 stock-쪽에서 살아남는다.
- 다시-adopt 시 GUID가 다시 나타나고, `InsertOrKeepVessel`이 `inserted=true`로 돌며,
  **완전히 새로운** `Vessel`이 생성된다.
  `subsystem_(ephemeris->subsystem_of_body(parent->body()))`(`vessel.cpp:93`), 여기서 부모는
  `main_body_index = vessel.mainBody`(`ksp_plugin_adapter.cs:1312,1323-1326`)다. 순항 레이어가
  dropout stock 궤도를 목적지 별 둘레로 설정했으므로 `mainBody` = 목적지 별 ⇒ **목적지 subsystem,
  자동으로.**
- 이어 파트들이 (이제 올바른) 선체 subsystem으로 변환된 DoF와 함께 삽입되고(`InsertUnloadedPart`,
  `plugin.cpp:446-455`), `CreateTrajectoryIfNeeded`가 그것들을 barycentre한다(`vessel.cpp:267-285`).
  그래서 trajectory는 태생부터 목적지 원점에 앵커된다 — `Translate` 없음, rebase 없음, fork 없음.
  (대조. `set_parent` 단독으로는 `subsystem_`을 바꾸지 *않는다*, `vessel.cpp:206-210` — 이것이
  Vessel이 지속되는 *big-fork* 제자리 경로가 이를 명시적으로 재할당해야 하는 이유다. §3.D 참조.)

**파괴/재생성에 걸친 상태 상속(설계상 "완벽한 상속"은 아니다).** 다시-adopt된 선체가 유지하는
것은 세 범주로 나뉜다.
- *살아남음(stock-쪽, C++ Vessel에 결코 없었음).* 파트, 승무원, 자원(warp ExoticMatter 포함 —
  stock 자원이라 순항-시간 소모가 지속됨), GUID, 이름, stock 궤도. C++ `Part` 객체는 Vessel이
  소유하고(`parts_`, `vessel.hpp:461`) 그것과 함께 파괴되지만, 재-삽입 시 권위적 KSP 파트로부터
  충실히 **재구성**된다(질량, 자원, DoF 재-읽기) — 사본이 아니라 같은 결과.
- *GUID로 보존됨("좀비" 맵).* `prediction_adaptive_step_parameters_`는 파괴 시 stash되고
  (`plugin.cpp:624`), 재-생성 시 GUID로 복원되며(`plugin.cpp:401-407`), 직렬화까지 된다
  (`plugin.cpp:1673`). 이것이 넘겨지는 *유일한* Principia-쪽 선체별 설정이다.
- *설계상 소실됨(해제된 Vessel 안).* `trajectory_`(순항에 걸친 history 간극),
  `flight_plans_` + 기동(목적지에서 replan — 수용된 "flight-plan 소실"), 타깃 지정
  (`ClearTargetVesselIf`, `plugin.cpp:623`). `subsystem_`/orbit-analyser/checkpointer는 상속이
  아니라 올바르게 *재구성*된다. 이 소실들은 정확히 warp — 진짜 trajectory 불연속 — 이 어차피 실을
  수 없는 양들이라, 파괴/재생성은 정확히 옳은 집합을 버린다.

### 9.2 속도는 subsystem 간 프레임-불변. v0 보존은 순항-쪽
- subsystem 로컬 원점들은 **상수** 변위만큼 차이 난다 — `subsystem_origin_offset_[s]`는 생성 시
  한 번 설정되고(`ephemeris_body.hpp:194`), 시간-독립 `DoublePrecision<Displacement>`로
  저장되며(`ephemeris.hpp:680`), inter-subsystem 오프셋도 마찬가지다(`:325`). jerk 커널이
  말한다. "속도는 영향받지 않는다. 원점 오프셋이 상수다"(`ephemeris_body.hpp:1524`). 그래서
  속도는 모든 subsystem 프레임에서 동일하고, subsystem 변경은 위치만 옮긴다(`RebaseIfNeeded`는
  속도를 건드리지 않고 `trajectory_.Translate(disp)`, `vessel.cpp:172-181`.
  `SubsystemConversionMotion` = RigidMotion, 항등 회전, 정지 프레임 속도, `plugin.cpp:1911-1921`).
- **직접-DoF 다시-seed(big-fork).** Barycentric DoF 속도를 유지 ⇒ v0 공짜 보존.
- **stock-궤도 다시-seed(minimal-fork).** `InsertUnloadedPart`가 barycentric DoF =
  `parent->current_degrees_of_freedom(t) + PlanetariumRotation⁻¹(from_parent)`
  (`plugin.cpp:444-447`)로 설정, 즉 속도 = `v_deststar + v_orbit`.
  `CreateTrajectoryIfNeeded`는 그것을 barycentre할 뿐이므로(`vessel.cpp:267-285`), seed 속도는
  dropout stock 궤도가 지정한 무엇이든이다. ⇒ v0을 보존하려면 순항 레이어가
  `v_orbit = v0 − v_deststar`를 쓰고(barycentric 결과 = v0), 쉬운 속박 도착을 주려면 parking-궤도
  속도를 쓴다. **어느 쪽이든 순항-쪽 C# 선택이지 fork가 아니다.**
- 따라서 도착 상대 속도 = `v0 − v_deststar`(현실 성간 접근 속도, 제동 leg가 깎는 것) — 현실적
  모드에서.

### 9.3 subsystem 파티션은 직렬화된다(재계산 아님). 목적지는 파티션된 subsystem이어야 한다
- 파티션은 명시적으로 쓰이고 그대로 복원된다. `Ephemeris`가
  `repeated int32 body_subsystem = 14`와 `repeated DoublePrecision subsystem_origin_offset = 15`
  를 얻고(`serialization/physics.proto:196-200`), `subsystem_origin_offset_.size() > 1`일 때만
  쓰이며(`ephemeris_body.hpp:1017-1024`) 그대로 다시 읽혀 오프셋을 덮어쓴다(`:1065-1099`).
  `ClusterSubsystems`는 **초기 생성 시에만** 돌고(`solar_system_body.hpp:173`) `ReadFromMessage`
  에서는 결코 안 돈다 — 그래서 로드는 세이브-시점 파티션을 정확히 재현한다. **재-클러스터링 위험
  없음**, 그리고 파티션은 게임 내내 고정된다(런타임에 새 subsystem이 안 나타남).
- Vessel/checkpoint/flight-plan subsystem 태그. `Vessel.subsystem`(`ksp_plugin.proto`,
  `vessel.cpp:746`에서 `!= 0`이면 쓰임, `:859`에서 없으면⇒0으로 읽힘), `Checkpoint.subsystem = 4`,
  `FlightPlan.subsystem = 14`. commit `7a21103d3`이 이것들을 추가한 건 옛 인-메모리 `rebase_offset_`
  누산기가 "…save와 load를 견디는데, 누적 rebase 오프셋은 그러지 못했다"이기 때문이다. reanimation은
  이제 각 checkpoint를 그것이 쓰인 subsystem에서 적분하고
  `subsystem_conversion(checkpoint_subsystem, subsystem_)`으로 변환한다.
- **Warp 요건.** 목적지 subsystem은 지속된 파티션에 이미 존재해야 한다. 아니면
  `subsystem_conversion`/`inter_subsystem_offset`의 `CHECK_LT(subsystem, …size())`
  (`ephemeris_body.hpp:518,585,623`)가 로드/reanimation에서 hard-fail한다. 이것은 NearStars
  로스터에 대해 **자동으로 충족**된다. 모든 별은 초기 생성 시 파티션된 천체이고, warp 타깃은 항상
  그런 천체다. Minimal-fork는 **새 직렬화를 추가하지 않는다** — 다시-adopt된 선체는 기존 WS1
  `subsystem` 필드로 round-trip한다.
- 하위 호환. subsystem-이전 또는 stock 세이브는 필드가 없는 채 로드됨 ⇒ 단일 subsystem 0, 거동
  불변(`has_...()` 가드 / 없으면⇒0 기본값).

## Related
- `ws4-warp-support-backlog.md` — 이 리서치가 근거화하는 workstream 스텁.
- `research/R4-thrust-under-warp.md` — WS3. big-fork 경로가 재사용하는 journalled-API 레시피.
- `research/R5-vessel-frames.md` — checkpointer/reanimator + rebase 라이프사이클 규칙(§3.B/D/E).
- `gameplay/interstellar-expansion/warp/*` — 물리 + minimal-fork 패치 초안 + 플러그인.
