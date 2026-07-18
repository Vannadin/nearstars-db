# WS4 — Principia 하의 warp(FTL) 지원 [BACKLOG — 오너 승인 2026-07-03, 미착수]

오너 결정(2026-07-03). 네 번째 workstream이며, WS1–3가 인게임에서 검증된 뒤에 한다. 이
파일은 아이디어와 그 근거가 살아남도록 하는 스텁이다.

**리서치 완료(2026-07-04). `research/R7-warp-support.md` 참조** — 현재-코드 재근거화, 실패
카탈로그, 접근 결정. **오너는 minimal-fork를 골랐다(2026-07-04).** C++ 쪽은 **검증 완료,
fork 필요 없음** — `WarpReadoptionLandsInDestinationSubsystem`(포크 commit `1727a86fa`)이
다시-adopt된 선체가 목적지 별의 subsystem에 올바른 원점으로 착지함을 확인한다. **C#/어댑터 구현
인수인계. `ws4-minimal-warp-adapter-handoff.md`**(Windows 세션). 아래 §3에 스케치된 big-fork
`VesselWarpTo` C ABI는 기각된 대안이다.

## 문제

FTL/warp-drive 모드(Alcubierre류)는 stock `Orbit`을 쓰거나 선체를 teleport하는데, Principia는
이를 금한다. WS1–3는 이를 바꾸지 않는다. Native 지원이란 선체를 새 위치/속도에서 정직하게
다시-seed하는 것이다 — Principia 자체 모델 안의 플러그인 API로(big-fork), 또는 선체를 detach해
순항 레이어가 움직이게 하고 dropout 시 Principia가 다시-seed하게 함으로써(minimal-fork,
R7-권장). [정정. 비호환은 이전에 "PersistentThrust, Principia issue #2347"로 귀속됐다 —
#2347은 실은 여전히 열려 있는 "Burn in time warp with RO ion engines" 요청이다. anti-warp
입장은 Principia FAQ에 있고, Blueshift를 명시적으로 이름 짓는다. R7 §8 참조.]

## 왜 이제 실현 가능한가 (WS1–3가 이미 제공하는 것)

- WS1. subsystem별 표현 + `Ephemeris::subsystem_conversion` — 광년 떨어진 warp 목적지가 완전
  정밀도로 표현 가능하고, 선체 rebase 기계장치(vessel.cpp `rebase_distance_threshold`)가
  도착 시 표현 전환을 이미 처리한다.
- WS2. void는 정확히 무힘이다(far-field 감쇠) — mid-void warp 진입/이탈 상태가 수치적으로
  깨끗하다. 화해할 tail 힘 없음.
- WS3. `VesselSetOnRailsBurn` 패턴(journal.proto 확장 + interface + 어댑터 harvest 분기)이
  새 API의 템플릿이다. "선체 변위" 호출은 엄밀히 더 단순하다(적분 변경 없음, trajectory
  다시-seed 하나).

## 예상되는 형태 (R6 리서치 패스로 확정할 것)

1. 플러그인 API `VesselWarpTo(guid, degrees_of_freedom, …)`(이름 TBD). psychohistory를
   종료하고, 불연속-표시된 점을 append(또는 새 history를 시작 — DiscreteTrajectory 세그먼트 +
   downsampling이 teleport에 어떻게 반응하는지 확인), 목적지가 void 너머면 subsystem rebase를
   트리거.
2. Journal 메시지 + C 인터페이스 + 어댑터 hook(WS3 레시피에 따라).
3. 기존 warp 모드용 interop 레이어는 mod별 작업이다(그것들이 우리 API를 호출해야 함).
   우리 자체의 최소 warp 파트/모듈을 배포하는 것이 외래 mod를 패치하는 것보다 단순할 수 있다.
4. 리서치 패스를 위한 미해결 질문. 에너지 부기(신경 쓰나?), 불연속의 history 의미론(warp를
   가로지르는 flight plan/prediction, R5 §7 라이프사이클 규칙에 따른 checkpointer/reanimator),
   save 호환성, 그리고 upstream이 이것을 언젠가 받아들일지 여부(아마 fork-전용 — 매 커밋에
   플래그).

## 우선순위

이후. WS2 게이트(Mac에서 완료), 크로스-workstream 상호작용 테스트, Windows 어댑터 + WS1–3의
인게임 검증. 오너. "이거는 나중에 하자."
