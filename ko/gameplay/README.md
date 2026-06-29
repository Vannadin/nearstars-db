---
title: Gameplay — playing NearStars (axis overview)
status: active
created: 2026-06-29
---

# 게임플레이 — NearStars를 플레이하기

NearStars의 작업은 서로 다른 두 축으로 나뉜다.

- **바디 모델링** — `phase2/` → `phase3/` → `phase4/`. 실제 천체물리를 게임용
  cfg로 바꾸는 큐레이션·합성·아트디렉션.
- **모드 플레이** — *이 디렉터리*. 모델링된 항성계를 실제로 **도달·항법·보상**
  가능하게 만드는 모든 것.

둘은 직교한다. 완벽히 모델링된 항성계라도 플레이어가 끝내 가지 못하거나 도착해서
할 게 없으면 죽은 콘텐츠다([`interstellar-expansion/README.md`](interstellar-expansion/README.md)
참고). 게임플레이 축은 **나중에 붙이는 광택이 아니라 1급 요구사항**이라, phase
파이프라인과 나란히 자기만의 최상위 자리를 가진다.

## 여기 들어오는 것

- [`rp1-integration/`](rp1-integration/plan.md) — RP-1 / RO 커리어 스택(Sol 기반)에
  올라타기. NearStars가 소유하는 베이스무관 커리어 레이어 — ResearchBodies,
  ROKerbalism 방사선, Principia 게이팅, RealAntennas.
- [`interstellar-expansion/`](interstellar-expansion/README.md) — post-RP-1
  엔드게임, 즉 간극 건너기. 실현가능성(Δv / 광속 하한 / 상대성), Principia 하 워프,
  lead-intercept 항법 플래너.
  - `interstellar-expansion/prototypes/` — 이식 가능한 수식 프로토타입(이쪽이
    맡는 절반. 인게임 C#은 슐츠 레인).
- *(추후)* `science-values/` — 확장 테크트리에 맞춘 per-system 과학 보상.
- *(추후)* `tech-tree/` — 성간 분기가 완주한 RP-1 트리 뒤 어디에 붙고, 밸런스는
  어떻게 잡는가.

## 상태

**탐색/브레인스토밍.** 프로젝트의 far-future 레이어다 — 확정 v1 로스터와 RP-1 커리어
통합이 착지한 다음에 온다. 인게임 C#/C++(워프 플러그인, 플래너 UI, Principia 포크
등)은 슐츠 레인([[project-nearstars-mod-plugins-schultz]])이고, 이쪽은 설계·spec·cfg·
수식 프로토타입을 맡는다.

## Related

- [science-system](../docs/reference/science-system.md) — 보상이 올라탈 per-body
  과학 레퍼런스(cross-cutting이라 `docs/reference`에 유지)
- `phase4/` — 이게 나란히 서는 바디 모델링 축
