---
title: WS4 minimal-fork warp — C#/어댑터 구현 인수인계 (Windows 세션)
status: READY — C++ side verified done (no fork needed); C#/cruise side to implement
owner decision: minimal-fork chosen (2026-07-04); see R7 for the alternative rejected
grounds: R7 §4/§9, gameplay/interstellar-expansion/warp/warp-patch-draft.md, plugins/NearStarsWarp/
target base: fork head 1727a86fa, gate 184
---

# WS4 minimal-fork warp — 구현 인수인계

오너는 **minimal-fork** 경로를 골랐다(R7). 이 문서는 Windows/C# 세션(슐츠의 레인)을 위한
실행 목록이다. 이미 검증된 것 vs 남은 것을 정리해, 구현이 그것을 다시 도출하지 않게 한다.
`gameplay/interstellar-expansion/warp/warp-patch-draft.md`(패치 스케치 + 순항-플러그인
뼈대)와 R7(`research/R7-warp-support.md`)을 함께 읽어라.

## minimal-fork warp가 무엇인가 (한 문단)

NearStars warp 하의 선체는 순항 기간 동안 **Principia에 의해 놓여난다**(관리 집합에서
드롭됨). 커스텀 순항 레이어가 stock KSP 호출로 그것을 움직이고, dropout 시 플래그가 해제되며
Principia가 목적지 별 둘레의 새 stock 궤도로부터 그것을 **다시-adopt**한다. C++
trajectory/flight-plan은 놓여날 때 파괴되고 도착 시 신선하게 재구성된다(warp 시 flight-plan
소실은 수용됨). 새 C++ API 없음, `VesselSetState` ABI 없음.

## C++ 쪽 — VERIFIED DONE, fork할 것 없음

이 세션은 포크에서 headless 테스트로 두 load-bearing C++ 가정을 검증했다(코드 변경은 필요
없었다 — 기존 기계장치가 이미 옳은 일을 한다).

- **Subsystem 할당은 자동이다.** `PluginIntegrationTest.WarpReadoptionLandsInDestination‑
  Subsystem`(commit `1727a86fa`). 다른 subsystem의 별 둘레로 다시-adopt된 선체는 그 subsystem
  으로 생성되고(부모 천체로부터, `vessel.cpp:93`) trajectory가 그 subsystem의 로컬 원점에
  앵커된다 — 성간 거리만큼 오프셋되지 않는다. 그래서 void를 가로지르는 warp는 **C++ 다시-seed
  fork가 필요 없다**. 목적지 별을 부모로 삼아 다시-adopt하기만 하면 된다.
- **Save/load + reanimation이 선체 상태를 보존한다.** `OnRailsBurnHistorySurvivesReanimation`
  (commit `280cf4d9b`). 다시-adopt된 선체가 save/load를 온전히 round-trip한다. (추력을 가로지른
  reanimation의 coast 근사는 드문, mid-session-drop-전용 경로다 — R7 발견, 수용됨.)

⇒ **Windows 세션은 C#(어댑터 + 순항 플러그인)만 건드린다. C++ 코어는 준비됐다.**

## C# 작업 — 실행 목록

### 1. fork 한 줄 (어댑터)
포크의 `ksp_plugin_adapter/ksp_plugin_adapter.cs`, `UnmanageabilityReasons(Vessel)`
(패치 초안은 2026-06 master에서 ~620–660을 인용 — **포크 head에서 시그니처 + 줄을 재확인하라**,
갈라졌다). OR-항 하나를 추가해 NearStars warp 플래그를 단 선체가 관리 불가로 보고되게(따라서
놓여나게) 한다. 플래그는 stock 채널(`KSPField`/GUID-맵을 이름으로)에서 읽어 Principia↔NearStars
컴파일 의존을 피한다. 이것이 Principia-쪽 변경의 전부다.

### 2. 순항 레이어 (fork 없음 — `plugins/NearStarsWarp/`)
`warp-patch-draft.md` §2에 따라. `WarpCruise.cs` 상태 기계(Idle→Spooling→Cruising→Dropout),
engage 시 Sol-barycentric 프레임에서 v0 캡처, 놓여난 동안 연속 이동, `WarpDriveModule.cs`
(PartModule + ExoticMatter 연료, `warp_exotic_matter.py`), `WarpFlagBridge.cs`(relativity
레이어의 `WarpFlag.Provider`를 채움).

### 3. dropout 시 속도 — 제대로 해야 할 유일한 것 (순항-쪽, fork 없음)
Principia는 stock 궤도로부터 다시-adopt하며 barycentric 속도 = `v_deststar + v_orbit`로
설정한다(R7 §9.2). 그래서 순항 레이어는 의도한 도착을 얻으려 dropout stock 궤도의 **상대
속도**를 써야 한다.
- **현실적(기본).** `v_orbit = v0 − v_deststar` → barycentric 속도 = v0 보존 → 참된 성간
  접근 속도를 실은 쌍곡선 도착(제동 leg가 깎아냄). 항법 planner가 이미 이 도착 속도를 계산한다.
- **캐주얼(난이도 토글, 오너의 아이디어).** 속박 parking 궤도를 씀 → 선체가 목적지 별과 함께
  움직이며 도착(성간 Δv 면제). 같은 코드 경로, 다른 선택된 `v_orbit` — 자유 게임-설정 토글,
  버그가 아님(R7 §7.4).
v0 캡처가 Principia가 다시-adopt하는 그 barycentric 프레임과 같은 프레임인지 확인하라(속도의
World→Barycentric은 완전한 RigidMotion이 필요, R7 §9.2).

### 4. 다시-adoption 메커니즘 (인게임 확인)
Dropout 시. 플래그를 해제하고, 목적지 별 둘레로 목적지 stock 궤도를 설정하고(그래서
`vessel.mainBody` = 목적지 별), 다음 Principia tick이 `CreateTrajectoryIfNeeded`로 다시-adopt
하게 둔다 — 위에서 검증됐듯, 그것이 목적지 subsystem을 할당하고 올바른 원점에 앵커한다. 추가
동작 없음.

## 수용 기준 (인게임, Windows)
- 선체가 Sol→목적지 계로 warp하고, 순항 중 놓여나고, 목적지 별 둘레의 올바른 subsystem으로
  다시-adopt된다(NaN/정밀도 폭발 없음 확인 — C++ 테스트가 headless 경우를 커버. 인게임에서
  확인).
- 현실적 모드. 선체가 성간 접근 속도(쌍곡선)로 도착, 제동 가능.
- 캐주얼 모드. 쓰인 parking 궤도로 도착.
- warp 시 flight-plan 소실은 예상됨(수용됨).
- 순항 중 save/load(선체 놓여남, 순전히 stock-쪽)와 도착 후 둘 다 살아남는다.

## Related
- `research/R7-warp-support.md` — 전체 실현가능성/실패-카탈로그/결정. §9는 C++ 심층 분석.
- `gameplay/interstellar-expansion/warp/warp-patch-draft.md` — 패치 스케치 + 순항 뼈대.
- `ws4-warp-support-backlog.md` — workstream 스텁.
- `ws3-adapter-handoff.md` — 형제 격인 WS3 어댑터 인수인계(같은 Windows 세션 레인).
