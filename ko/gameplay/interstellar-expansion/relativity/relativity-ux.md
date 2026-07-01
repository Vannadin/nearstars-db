---
title: 상대성이론 레이어 — 대시보드 UX / UI 명세
status: draft
created: 2026-06-30
---

# 상대성이론 레이어 — 대시보드 UX / UI

> **분리된 상대성 mod 소속(2026-07-01).** 상대성 코드는 이제 독립 레포(`~/Desktop/ksp-relativity/`)다.
> 이 대시보드 명세는 [relativity-mod.md](relativity-mod.md)와 함께 그 레포로 이관 예정. 그 문서의 승격
> 노트 참조.

**무엇인가.** 아광속 상대론 메커닉([relativity-mod.md](relativity-mod.md))의 디스플레이
명세다. 이 메커닉의 정체성 *자체*가 그 표시값에 있다("β가 올라갈수록 명목 추력과
실효 추력이 갈라지는 것을 플레이어가 본다", §1). 그래서 대시보드는 곁다리 장식이
아니라 일급 디자인 표면이다. 이 노트는 초안 스텁
`RelativityDashboard.cs`(`ksp-relativity` 레포)를
확장하기 위한 브리프다. 범위는 비행 중 HUD에 한정된다 — 셰이더/시각 레이어는
다루지 않는다(명세 §2.5, 우리 레인 아님).

**해소하는 디자인 긴장.** relativity-mod §0은 *체감되는* 메커닉에 수식이 필요 없다고
하고, §1은 갈라지는 표시값이 곧 정체성이라고 한다. 답은 **2-모드 대시보드**다.
수식 없는 Simple 모드와 전체를 보여주는 Expert 모드.

---

## 1. 표시값 세트

| 행 | 표시 내용 | Source | Mode |
|-----|-------|--------|------|
| **Speed** | `β`를 `c`의 분수로, 광속 벽 게이지와 함께 | `RelativityState.Beta` | both |
| **Thrust** | 실효 / 명목 kN과 % (`1/γ³`) | `ThrustFactor(γ)` | both |
| **Brake authority** | 역추진 실효 추력 % + "⚠ decel now" 신호 | `1/γ³` (방향 무관) + 플래너 | both |
| **Mission clock** | 좌표시(UT) 경과 | game UT | both |
| **Crew clock** | 고유시간 경과 + 미션 시계와의 Δ | 함선별 `∫dt/γ` 누적기 | both |
| **γ** | 로렌츠 인자 | `RelativityState.Gamma` | Expert |
| **Life support** | 소비율 `×1/γ` | `ResourceFactor(γ)` | Expert |
| **Radiation dose** | `×1.00 (not dilated)` — 대비 행 | constant 1.0 | Expert |

**방사선 대비 행**은 의도적이다. `dose ×1.00`을 `life support ×0.39` 바로 옆에
놓으면 명세 §4의 결론이 가르쳐진다 — 빠른 승무원은 덜 늙지만 같은 양의 방사선을
받으므로, **묶이는 제약은 굶주림이 아니라 방사선이다**. 절대 선량은 Kerbalism 자체
UI에 남겨두고, 여기서는 배수 대비만 보여준다.

---

## 2. 광속 벽 속도 게이지 (§ decision ③)

**0에서 1 c까지의 선형 바에 1.0 지점의 단단한 벽 마커**를 더하고, 숫자값 `0.923 c`도
함께 표시한다. 약 0.9c 위에서는 마지막 구간이 **비선형 꼬리**로 채워져, `c`로의 최종
접근이 눈에 띄게 결코 완료되지 않게 한다 — "채울 수 없는 점근선"이 rapidity 없이도
한눈에 읽힌다. (rapidity 스케일링도 검토했으나 덜 직관적이라 기각했다.)

---

## 3. 두 시계 (§ decision ④)

- **승무원(고유) 시계**는 `τ = ∫ dt/γ`를 **함선 발사 시점부터** 적분하므로 진짜
  승무원 나이 적산계다. 좌표시(UT) 미션 시계 옆에 그 차이와 함께 표시한다.
- 격차는 **영구적**이다 — 감속해도 결코 되따라잡히지 않는다(쌍둥이 역설의 결과).
  누적기는 결코 리셋되지 않는다.
- 세이브에 **함선별**로 저장된다. 표시는 활성 함선을 추적한다.
- **표시 전용 / 장부 기록.** 이것은 고유시간을 적분해 보여줄 뿐, 게임의 UT나
  타임워프를 **조작하지 않는다**. 보류된 "시간 요소"(relativity-mod 범위)는 *시계
  조작*이고, 수동 적산계는 그와 양립 가능하며 지금 출시해도 안전하다.
- 워프 중에는 `γ = 1`이므로 누적기는 UT와 **1:1**로 진행한다(새 격차 없음). 배경에서
  계속 돌지만 워프 모드 패널에서는 숨겨진다(§5).

---

## 4. 브레이크 권한 신호 (§ decision ⑤)

`1/γ³` 페널티는 **방향 무관**이다 — `c` 근처에서는 제동도 가속만큼 무력하므로, 도착
감속을 터무니없이 일찍 시작해야 한다(relativity-mod §0, 플래너의 leg-3 제동과 연결).

- **브레이크 권한 %** = 역추진 실효/명목 추력 = `1/γ³`(같은 인자).
- **`⚠ decel now`**는 도착을 맞추려면 감속을 시작해야 하는 시점에 발동한다. 이는
  **상대론적 순항** 사안이다 — 0.3~0.9c 순항(realist 토치 주행, 또는 포크 연속순항)을
  떨구는 것으로, `1/γ³`가 제동을 무력하게 만든다. 신호원은 선행-요격 **플래너**의 leg-3
  ([planner-spec §4.5](../planner-spec.md))이 남은 거리 / 트랜짓을 공급하고, 플래너가 없을
  때의 MVP 대체안은 남은 거리 대 현재 감속 능력 휴리스틱이다. 이 신호는 **computed-jump
  플로어에서는 휴면**이다 — 거기서는 도착 시 별의 km/s 고유속도만 제동하면 되고, 그건
  비상대론적이라 싸다(planner §4.5).

이 하나의 신호가 메커닉이 그러지 않으면 일으킬 "왜 멈출 수가 없지?" 소프트락을
방지한다.

---

## 5. 상태 & 레이아웃

가시성은 명세 §2.6 가드를 따른다. 대시보드는 레이어가 활성화되면(`β > β_min`)
**자동으로 나타나고** 그 외에는 숨겨진다. ApplicationLauncher 토글로 강제 표시(계획용)
하거나 고정/숨김 할 수 있다. 창은 드래그 가능하다.

스텁은 현재 `st.Active`가 false일 때마다 창을 숨겨, "아상대론적" 상태와 "워프 중"
상태를 한데 뭉뚱그린다. 확장에서는 이 둘을 **분리**해야 한다.

| 조건 | 패널 |
|-----------|-------|
| `β > β_min`, 워프/글리치 아님 | **전체 대시보드** (Simple 또는 Expert) |
| **워프/점프 중** (WarpFlag up) | **접힌 WARP 패널** — 속도를 `c` 배수로만 |
| `β ≤ β_min` (아상대론적) | 숨김 (고정 시 `off (sub-relativistic)`) |
| 비현실적 β (kraken, §2.6 iii) | `disabled — implausible β` |

### Active (아광속 순항) — Simple
```
┌─ RELATIVITY ───────────── ● ACTIVE ─┐
│ Speed   0.923 c  ▓▓▓▓▓▓▓▓░│1c         │
│ Thrust  8.9 / 154 kN  ( 5.8% )       │
│ Brake authority  5.8%   ⚠ decel now  │
│ Mission   12.4 yr                    │
│ Crew       4.8 yr   (−7.6)           │
└───────────────────────────────────────┘
```
**Expert**는 다음을 추가한다. `γ = 2.59`, `life support ×0.39`, `dose ×1.00 (not dilated)`.

### 워프 감지됨 (WarpFlag up) — 접힘
```
┌─ WARP ───────────── ◆ ─┐
│ Speed   23.4 c        │
└───────────────────────┘
```
상대론-메커닉 행은 전부 사라진다(γ/추력/물자/선량/브레이크는 워프 중 항등이거나
NaN이다). `c` 배수의 워프 속도만 남는다. **여기 속도는 워프 플러그인(`WarpCruise`)에서
읽은 워프 `β_s`이지, 상대성 레이어의 물리적 β가 아니다** — 두 플러그인을 잇는
브리지(`WarpFlagBridge`)는 이미 존재한다.

---

## 6. 구현 브리프 — `RelativityDashboard.cs` 확장

스텁은 `st = RelativityState.Evaluate(v, WarpFlag.IsWarpingOrJumping(v))`를 계산하고
`st.Active`일 때 β/γ/추력%/물자%를 그린다. 이를 확장한다.

1. **워프를 먼저 분기한다.** `WarpFlag.IsWarpingOrJumping(v)`이면, 워프 플러그인의
   워프 속도를 써서 접힌 WARP 패널을 그린다 — 읽기 경로를 **VERIFY**할 것(예: 활성
   함선의 `WarpDriveModule`에서 `WarpCruise.State.WarpBeta`를, `WarpFlagBridge`가 쓰는
   동일 채널을 통해). 여기서 속도를 위해 `st`를 읽지 **말 것**(설계상 워프 중에는
   항등이다).
2. **두 모드.** Simple/Expert 토글(창 헤더의 버튼 또는 런처 메뉴). Simple = Speed,
   Thrust, Brake, 두 시계. Expert는 γ, 생명유지 `×1/γ`, 선량 `×1.00`을 추가한다.
3. **광속 벽 게이지.** 밋밋한 `β` 라벨을 0→1 바 + 벽 마커 + 비선형 꼬리로 교체한다(§2).
4. **두-시계 누적기.** 함선별 `τ += dt/γ` 적분기(γ≈1일 때는 워프 포함 1:1 진행).
   함선의 세이브 노드에 영속화한다 — `ProtoVessel`/`VesselModule` 영속화 훅을
   **VERIFY**할 것. UT, 승무원, Δ를 표시한다.
5. **브레이크 행.** `1/γ³`을 브레이크 권한 %로 표시한다. `⚠ decel now`는 플래너가
   있으면 플래너에, 없으면 휴리스틱에 연결한다(§4).
6. **kraken/비활성 텍스트.** 고정된 경우, 사라지는 대신 `off (sub-relativistic)`이나
   `disabled — implausible β`를 표시해 레이어가 살아 있되 유휴 상태임을 플레이어가
   알게 한다.

NearStars DB / cfg 델타는 없다. 이것은 기존 힘/자원 훅 위에 얹는 디스플레이 + 고유시간
누적기다.

## Related

- [relativity-mod.md](relativity-mod.md) — 이것이 표시하는 메커닉 (§1 표시값 정체성, §2.6 가드, §4 방사선 대 굶주림)
- `RelativityDashboard.cs`(`ksp-relativity` 레포, `src/`) — 이 브리프가 확장하는 스텁
- [warp/warp-patch-draft.md](../../../../gameplay/interstellar-expansion/warp/warp-patch-draft.md) — 워프 중 그 `β_s`와 `WarpFlag`을 읽어 오는 워프 레이어
- [planner-spec.md](../planner-spec.md) — `⚠ decel now` 신호를 먹이는 선행-요격 플래너
