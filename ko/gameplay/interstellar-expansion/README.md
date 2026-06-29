---
title: Interstellar expansion — purpose & scope
status: exploratory
created: 2026-06-28
---

# 성간 확장 — 목적

**핵심 명제.** 도달할 수도 플레이할 수도 없는 항성계는 죽은 콘텐츠다. NearStars가
근방 항성계를 아무리 완벽하게 모델링해도 — 실측 궤도·대기·비주얼·과학 정의까지 —
**플레이어가 끝내 거기 가지 못하거나 도착해서 할 게 없다면 아무 가치가 없다.** 항성계
구현은 *필요조건이지 충분조건이 아니다.* 게임플레이 레이어 — 성간 이동, 항법, 그리고
여정을 정당화하는 과학적 보상 — 는 **나중에 붙이는 광택이 아니라 1급 요구사항이다.**

이 디렉터리가 존재하는 이유 — 바로 그 게임플레이 레이어가 진짜 어려운 부분으로 드러났고,
모드 전체가 의미를 가지려면 그것이 풀려야(혹은 풀 수 있음이 증명되어야) 하기 때문이다.

## "게임플레이가 작동해야 한다"의 구체적 의미

도달 가능하고 플레이 가능한 NearStars엔 다음이 전부 필요하다.

1. **이동이 물리적으로 가능한가.** 함선이 그럴듯한 추진으로 플레이 가능한 시간 안에 그
   간극을 실제로 건널 수 있는가? → `feasibility.md` (게이트 0: Δv, 광속 하한, 상대성,
   워프 mod 조사).
2. **이동이 엔진에서 기계적으로 가능한가.** 이동 메커니즘이 플레이어가 쓰는 스택
   (Principia + RP-1)과 공존하는가? → `warp-and-navigation-brainstorm.md`
   (Principia 하 워프, 옵션 사다리, 최소 포크 경로).
3. **항법이 되는가.** Principia에선 별이 움직이므로 도착 시점에 목표가 가 있을 곳을
   겨냥해야 한다 → 성간 lead-intercept 플래너.
4. **도착할 가치가 있는가.** 제공되는 과학(과 그 외)이 수년~수십 년 미션을 정당화해야
   한다 → per-body science value ([[reference-science-system]]), 확장 테크트리와
   균형 잡아서.
5. **진행에 들어맞는가.** 이건 **post-RP-1 엔드게임 확장**이다 — 완주한 실세계
   테크트리 뒤에 붙고, 자체 추진과 밸런스를 가진다.

이 중 하나라도 실패하면 항성계는 맵에서 바라보기만 하고 영영 못 가는 배경이 된다. 이
작업은 바로 그 실패 모드를 막기 위해 존재한다.

## 상태

**탐색/브레인스토밍.** 토대는 기록됐으나 확정된 것은 없다. 이건 프로젝트의 far-future
레이어다(확정 v1 로스터와 RP-1 커리어 통합이 착지한 다음). 인게임 C#/C++(워프 플러그인,
플래너 UI, Principia 포크 등)은 슐츠 담당
([[project-nearstars-mod-plugins-schultz]])이고, 이쪽은 설계·spec·cfg·수식 프로토타입을 맡는다.

## 문서

- [`feasibility.md`](feasibility.md) — 게이트 0. 실거리에서 성간 이동이 물리적으로
  빌드/플레이 가능한가 (Δv, 광속 하한, 상대성, 워프 mod).
- [`warp-and-navigation-brainstorm.md`](warp-and-navigation-brainstorm.md) —
  Principia 하 워프 메커니즘, 옵션 사다리(no-fork / 최소 포크 / 큰 포크), cruise
  아키텍처, 속도 연속성, lead-intercept 플래너.
- [`planner-spec.md`](planner-spec.md) — Δv 기반 lead-intercept 플래너. 수식 spec,
  `v_avg = c·tanh(Δv/4)`, 3-leg 프로파일, DB 데이터 프로토타입.
  프로토타입은 [`prototypes/`](../../../gameplay/interstellar-expansion/prototypes/).

## Related

- [rp1-integration](../rp1-integration/plan.md) — 이 확장이 올라타는 커리어 스택
- [science-system](../../docs/reference/science-system.md) — per-body 과학 보상 (4번)
