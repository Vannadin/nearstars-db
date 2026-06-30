---
title: Warp mechanics under Principia + interstellar navigation — brainstorm
status: active
created: 2026-06-28
---

# Warp under Principia + interstellar navigation — brainstorm

**단계: 브레인스토밍 / 탐색 — 아직 확정 아님.** 2026-06-28 세션에서 나온 워프 메커니즘과
항법 아이디어를 정리한 문서다. [`feasibility.md`](../feasibility.md)(gate 0)의 연장선이다.
소스로 근거화된 발견은 **[src]** 로 표시했으며(Principia `mockingbirdnest/Principia` @ master),
나머지는 검증이 필요한 설계 아이디어다. 인게임 C#/C++ 작업은 슐츠 담당이고
([[project-nearstars-mod-plugins-schultz]], [[project-principia-custom-branch]]),
이쪽에서는 설계/스펙/cfg + 수학 프로토타입을 맡는다.

---

## 1. Requirements (owner)

- **연속 순항(continuous cruise)** 이어야 하며, 이산 점프가 아니다. 조종 가능하고, 인게임
  시간을 소모하며, 비행 중 중단·경로 변경이 가능하고, "별이 지나가는 것을 볼 수 있어야" 한다.
- **워프 시작 시점의 속도 연속성** — 진입 시의 상대속도 v₀ 를 그대로 끌고 가서 그 속도로 빠져나온다
  (Alcubierre 의 "운동량 변화 없음" 성질).
- **반드시 Principia 와 공존해야 한다.** Principia 가 없는 프로파일은 너무 단순하고(그냥 Principia 를
  설치하지 않으면 그만) 목표가 *아니다*. 이 작업 전체의 핵심은 워프 + Principia 를 함께 굴리는 것이다.

## 2. Why warp is hard under Principia  [src]

- 권위 있는(authoritative) 함선 상태는 C++ `DiscreteTrajectory`(`vessel.cpp`)다. KSP 의 transform 은
  매 프레임 Principia 의 적분 결과로 덮어쓰인다(`ksp_plugin_adapter.cs` 의 `UpdateVessel` ~516–525,
  `part_rb.position = …` 쓰기). 주석 왈, *"nobody will know that they're not the ones obtained by Unity."*
- 겉보기 운동(apparent-motion) 채널은 **무게중심(CoM) 병진 운동을 버린다** — `DeformPileUpIfNeeded`
  (`pile_up.cpp` ~445–578)는 자세(attitude)만 유지하고(Davenport q-method), `NudgeParts` 가
  적분된 CoM 에 다시 고정한다. *"We cannot use the apparent motion of the centre of mass, because the
  game does not conserve momentum."* → 외부 `SetPosition` 이 읽혀 들어와도 그 병진 성분은 버려지고,
  같은 프레임에 적분된 위치가 다시 쓰인다. 이것이 HyperEdit/Blueshift 가 "효과가 없는" 이유다
  (issue #1420, wontfix).
- Principia 는 **관리되는 모든 함선을 지배한다** — 로드된 것뿐 아니라 언로드/패킹된 것까지
  (`adapter.cs` vessel loop ~1311–1327; 백그라운드 catch-up ~1700–1768). 관리되는 함선에 대해
  **stock OrbitDriver 가 지배하는 상태는 존재하지 않으며**, 온레일(on-rails) 상태도 덮어쓰인다
  (`vessel.orbit.UpdateFromStateVectors` ~522). stock orbit 을 설정해도 ⇒ 고정되지 않는다.
- 권위 있는 자유도(DoF)는 **KSP stock orbit 에서 단 한 번만 시드(seed)된다** — 미지의 GUID 가 처음
  삽입될 때(`CreateTrajectoryIfNeeded` 가 `trajectory_.empty()` 로 가드됨, `vessel.cpp` ~232–256).
  Vessel 객체가 살아 있는 동안 다시 시드되는 일은 없다. **in-place 재시드 / `ResetVessel` 같은 건 없다.**
- `ExternalInterface` 는 **읽기 전용이며 제거되는 중이다**(Landau last → Laplace 미구현 → Laurent 제거,
  2025년 말). 따라서 향후 "set state" 훅이 업스트림에 들어올 일은 없다. CONTRIBUTING 왈,
  "unsolicited contributions seldom welcome."
- **"그냥 되돌리기를 비활성화"는 틀린 계층이다** — 쓰기-되돌림은 증상일 뿐이고, 권위는 적분된
  궤적에 있다. 그것을 억눌러봤자 ⇒ 함선이 다음 프레임에 원래대로 튕겨 돌아오고, pile-up/예측/세이브-로드가
  깨진다.
- **점프는 맞고, 순항은 싸운다.** 이산 점프 = 새 초기 조건 하나를 앞으로 적분 — 깔끔하게 맞아떨어진다.
  연속 순항 = 적분된 CoM 을 초당 ~50회 덮어쓰는 것 — 바로 `DeformPileUpIfNeeded`/`NudgeParts` 가
  거부하는 동작이다.

## 3. The options ladder (how to get cruise anyway)

| Path | Cruise? | Flight plan | Fork | Rebase burden |
|------|:------:|------------|------|---------------|
| **No-fork (crude free + re-seed)** | ✗ jump only | lost | none | none |
| **Minimal fork — `UnmanageabilityReasons` flag** | ✓ | lost (acceptable) | small, stable area | light |
| Big fork — `VesselSetState` C ABI | ✓ | can preserve | large, integrator internals | heavy |

- **No-fork crude  [src]** — Principia 가 함선의 C++ `Vessel` 을 ≥1 프레임 동안 풀어주게 만들고
  (kept-set 에서 빠지면 → `FreeVesselsAndPartsAndCollectPileUps` 가 그것을 지움, `plugin.cpp` ~688–704),
  stock vessel 을 옮긴 뒤 다시 삽입되게 하면 → 새 stock orbit 에서 재시드된다. **Principia 궤적 기록 +
  비행 계획을 잃는다**(이들은 파괴된 C++ 객체 안에 있고, "좀비" 맵에는 예측용 adaptive-step 파라미터만
  남는다). **KSP GUID/파츠/승무원은 살아남는다.** 본질적으로 이산 점프다. 함선을 순항 내내 분리 상태로
  잡아둘 만한 심우주 호환 "비관리(unmanaged) 상황"이 존재하지 않으므로(LANDED/PRELAUNCH 는 지표 전용)
  ⇒ no-fork = 점프 전용이다.
- **Minimal fork (the sweet spot)** — Principia 의 분리 게이트는 `UnmanageabilityReasons` 필터
  하나뿐이다(`adapter.cs` ~620–660; ORBITING/FLYING 등이 아닌 경우, DEAD, pos==0, hack-gravity 를
  제외; **VesselType 검사는 없다**). 여기에 **함선별 제외 조건 하나**("flag X ⇒ unmanaged")를 추가한다.
  그러면: engage → 플래그 → Principia 가 함선을 풀어줌 → 커스텀 연속 순항(v₀ 를 끌고 감) → 드롭아웃이
  목적지에 stock orbit 을 설정 + 플래그 해제 → Principia 가 기존 첫-삽입 경로를 통해 재시드한다.
  **순항은 작동하고, 비행 계획은 잃으며, GUID 는 유지된다.** 이것은 적분기가 아니라 *안정적인 필터*
  안에 살기 때문에 → `VesselSetState` 에 비해 매월 리베이스 위험이 훨씬 가볍다. *(확인된 메커니즘에서
  나온 설계 추론이므로 슐츠와 함께 검증할 것.)*
- **Big fork** — `VesselSetState(guid, barycentric DoF)` C ABI 를 추가해 궤적을 그 자리에서 비우고
  재시드한다. 정체성/비행 계획을 보존할 수는 있으나 적분기 내부를 건드리고(무거운 리베이스),
  비행 계획 손실을 감수할 수 있다면 불필요하다.

**작업 가정: 워프 시 비행 계획 손실은 감수 가능** — 어차피 목적지 시스템에서 다시 계획을 짜게 된다.

## 4. Cruise architecture (ⓑ2)

연속 순항은 Principia 의 틱(tick) 적분 안이 아니라, **Principia 의 물리 씬(scene) 위에 얹은 커스텀
항성간 이동 계층(layer)** 에 산다:

1. **Engage** → 함선을 비관리로 표시(minimal-fork 플래그) → Principia 가 함선을 풀어줌.
2. **Cruise** → 커스텀 propagator 가 v₀ 를 끌고 함선을 연속적이고 조종 가능하게 이동시킴.
   다른 함선/천체는 각자의 Principia 궤적을 유지하고, 시간은 정상적으로 흐른다.
3. **Dropout** → 목적지 stock orbit 설정 + 플래그 해제 → Principia 가 그 상태로부터 다시 채택한다.

Principia 는 두 끝점(분리 / 재시드)만 건드리므로 틱마다 싸우는 일이 없다.

## 5. Fork reality  [src]

- **License: MIT** (`LICENSE.txt`, Robin/Pascal Leroy = eggrobin). 수정한 `principia.dll` 을
  자유롭게 포크·수정·재배포할 수 있고, notices(Principia 의 것 + 번들 의존성 abseil/protobuf/zfp/…)만
  유지하면 된다. 우리 data-sources 의 "MIT" 표기는 정확하다.
- **Build: heavy** — 고정된 MSVC 2022(VS 2026 비호환) / Clang 20, 다수의 `deps` 서브모듈 + 실제 KSP
  어셈블리가 필요하고, OOM 함정이 있다. macOS 빌드는 "best-effort/untested" 이며, *배포되는* 산출물은
  반드시 Windows DLL 이어야 한다(NearStars 는 Windows 전용).
- **Upstream won't take it** — 모드 API 가 삭제되는 중이고 "unsolicited contributions seldom welcome."
  ⇒ **영구적으로 갈라진 포크(permanent divergent fork).**
- **Distribution** — `GameData/Principia/x64/principia.dll` 에 단일 DLL 이므로 ⇒ **공식 Principia 와
  상호 배타적**이고 CKAN 을 깬다. Principia 는 매월 릴리스되며(KSP 버전 잠금) ⇒ 리베이스 쳇바퀴가 생긴다.
  minimal-fork 플래그가 이를 완화하지만(안정적인 코드 영역) 포크 부담 자체는 실재한다.

## 6. Velocity continuity + the inter-stellar frame decision

- **Mechanical carry** — engage 시점에 v₀ 를 캡처해 순항 내내 끌고 가다가 dropout 에서 복원한다.
  KSPIE/Blueshift 는 이미 "진입 속도로 빠져나오기"를 한다.
- **열린 결정 — 그 간극을 가로질러 어느 프레임의 속도를 보존하는가?** 별들은 움직이므로
  (Barnard 의 고유운동 ~140 km/s) 출발-프레임 v₀ 를 끌고 간다는 것은 도착 시 항성간 상대속도가 더해진
  채로 도착한다는 뜻이다.
  - (a) **barycentric preserve** — 실제 상대속도를 안고 도착(현실적; 도착이 도전 과제가 됨).
  - (b) **destination-rest** — 목표 별에 대해 정지 상태로 도착(편리함; 게임적임).
  - (c) middle.
  NearStars 에 고유한 문제다(기존 워프 모드들은 stock 스케일의 가짜 쌍성이다).

## 7. Interstellar navigation planner

Principia 가 별들을 움직이므로(실제 우주속도를 가진 섭동체; 쌍성은 궤도도 돈다) 항성간 항법은
**리드-인터셉트(lead-intercept)** 가 된다 — 별이 지금 있는 곳이 아니라 도착 시점에 있을 곳을 겨냥한다.
Principia 자신의 비행 계획기(flight planner)는 워프 구간을 다룰 수 없으므로(분리됨, 비중력, 비행 계획
폐기) ⇒ **커스텀 계획기가 필요하다.**

- **핵심 단순화** — 항성간 거리에서는 상호 중력 ≈ 0 이므로 단일 별은 거의 **선형**으로 움직인다:
  `P(T) = P₀ + v_star·T`, DB 의 ICRF 위치 + 속도로부터 계산한다. 쌍성은 알려진 궤도 항을 더한다
  (요소는 DB 에 있음). ⇒ **Principia 의 read API 에 의존하지 않는다**(그 API 는 제거되는 중). 큰 이득이다.
- **Solver** — 고정점(fixed-point) 리드-인터셉트: 통과 시간 T 를 추정 → 별 위치 P(T) → 거리 →
  그 거리에 대한 워프 시간 → T 갱신 → 수렴. 출력: **방위(heading) + 통과 시간 + 도착 상대속도**
  (마지막 항은 §6 프레임 결정에 묶임).
- **Profiles** — Principia 프로파일은 리드-인터셉트가 *필요하고*(별들이 표류함), stock 프로파일은
  거의 정적일 가능성이 커서 ⇒ 더 단순한 직접 조준(direct-aim)으로 충분하다.

## 8. Open decisions / next

- 속도-프레임 결정(§6: a / b / c).
- minimal-fork `UnmanageabilityReasons` 플래그가 실제로 깔끔하게 분리되고 재시드되는지 검증
  (슐츠와 함께).
- 리드-인터셉트 수학 프로토타입 작성(수렴 검증 + 프레임 결정이 도착을 어떻게 바꾸는지 제시),
  Δv 맵처럼.
- 워프 시 비행-계획-손실이 감수 가능한지 확인.

## Source anchors

- `ksp_plugin_adapter.cs`: vessel loop ~1311–1327; `UnmanageabilityReasons`
  ~620–660; one-time seed 1396/1432; `UpdateVessel` ~516–525; on-rails ~1772;
  warp catch-up ~1700–1768.
- `plugin.cpp`: `InsertOrKeepVessel` ~573–604; free/zombie ~688–704.
- `vessel.cpp`: `CreateTrajectoryIfNeeded` ~232–256. `pile_up.cpp`:
  `DeformPileUpIfNeeded` ~445–578, `NudgeParts` ~404.
- FAQ + issues #1420 (HyperEdit no-effect, wontfix), #1659 (read-only
  `FlowBodyCentric` musing), #2457 (zombies); Interface wiki (read-only, removed);
  `LICENSE.txt` (MIT); `Setup.md`; `CONTRIBUTING.md`.

## Related

- [feasibility](../feasibility.md) — gate 0 (Δv map, light floor, relativity, warp-mod survey, two-profile)
