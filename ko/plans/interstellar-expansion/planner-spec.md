---
title: Interstellar navigation planner — spec + lead-intercept prototype
status: exploratory
created: 2026-06-28
---

# Interstellar navigation planner — spec

**단계: exploratory.** 성간 lead-intercept 플래너를 명세하고 수학 프로토타입을
기록한다. 엔진 비종속이다. 여기 담긴 수학은 이식 가능하며, 이쪽이 담당하는
절반이다. 인게임 C#(맵뷰 후킹, UI, 워프 engage)은 슐츠 몫이다
([[project-nearstars-mod-plugins-schultz]]). 맥락은 [`README`](README.md),
[`warp-and-navigation-brainstorm.md`](warp-and-navigation-brainstorm.md)를 참고하라.

**필요한 이유.** Principia 하에서 목적지 별은 *움직인다*(실제 공간 속도). 그래서
지금 있는 자리가 아니라 도착 시점에 별이 있을 자리를 겨눠야 한다. 이것이
lead-intercept다. Principia 자체의 비행 플래너는 워프 구간을 다루지 못한다(분리된,
비중력적, 비행 계획 폐기). Unity Editor는 필요 없다. 플래너는 코드만으로 이뤄진 C#
플러그인(IMGUI/스톡 UI + 맵뷰 라인)이며, 선례로 Transfer Window
Planner / Astrogator / MechJeb이 있다.

## 1. Inputs

- **Origin** — 함선 위치 `r0`(Sol-barycentric ICRF) + 속도 `v0`.
- **Destination star** — `db/systems`에서 가져온 ICRF 위치 `P0` + 속도 `v_star`.
  미래 위치는 **선형 외삽** `P(t) = P0 + v_star·t`으로 구한다(성간 중력 ≈ 0 ⇒
  거의 직선, Principia API 불필요). 이중성 목적지라면 DB 궤도요소에서 나온 알려진
  궤도 항을 더한다.
- **Warp model** — 속도 `v_w`(MVP에서는 상수, FTL 허용). 이후에는 중력 게이팅 /
  테크 티어화 ⇒ `v_w(distance)`.
- **Velocity-frame mode** — (a) barycentric-preserve / (b) destination-rest / (c) mid.

## 2. Algorithm — lead-intercept

상대 시작점 `R0 = P0 − r0`. **상수 `v_w`**에서는 닫힌 형식의 이차식이 된다(함선이
`v_w·T`만큼 이동하는 동안 별이 표류한다).

```
(v_w² − |v_star|²)·T² − 2(R0·v_star)·T − |R0|² = 0     →  positive root T
heading   = normalize(P0 + v_star·T − r0)
arrival   = P0 + v_star·T
arrivalRelV = (mode a: v0  |  mode b: v_star) − v_star   →  |·| = Δv-to-match
```

가변 `v_w(distance)`거나 이중성 목적지라면 고정점 반복으로 푼다(T 추정 → 거리/위치
→ v_w → T → 수렴). `v_w > v_star`일 때(워프에서는 항상 참) 둘 다 계산이 가볍고
잘 조건화되어 있다.

## 3. Outputs

`heading`(단위 벡터), 통과 시간 `T`, `arrival` 지점, `arrivalRelV`(+ 크기 =
정지/일치에 필요한 Δv), 그리고 경고(예: 도착 속도 과대).

## 4. Prototype results (real DB data, ship at barycenter, v0 = 0)

`no-lead miss` = 별의 *현재* 위치를 겨눴을 때 얼마나 빗나가는가.

| Target | warp | transit | no-lead miss | arrival rel v |
|--------|-----:|--------:|-------------:|--------------:|
| Alpha Cen A (4.40 ly, 28 km/s) | 1c | 4.40 yr | **26 AU** | 28 km/s |
| | 10c | 161 d | 2.6 AU | 28 km/s |
| | 1000c | 1.6 d | ~0 | 28 km/s |
| Barnard (5.99 ly, 142 km/s) | 1c | 5.99 yr | **180 AU** | 142 km/s |
| | 10c | 219 d | 18 AU | 142 km/s |
| | 1000c | 2.2 d | ~0 | 142 km/s |

**발견 사항.**
- **Lead는 실재하며 워프 속도에 반비례한다.** 1c에서는 26 AU(αCen) /
  180 AU(Barnard)만큼 빗나간다. 즉 안쪽 시스템을 통째로 놓친다. 10c에서도
  AU 규모다. ~1000c를 넘어야 무시할 만하다. ⇒ lead-intercept 플래너는 어떤 중간
  수준 워프에서도 필수이며, 반올림 오차 따위가 아니다.
- **도착 상대 속도는 워프 속도와 무관하다** — 별의 barycentric 속도와 같다
  (v0 = 0에서 28 / 142 km/s). 따라서 **velocity-frame 결정은 큰 결과를
  낳는다**. (a)에서는 Barnard를 142 km/s로 스쳐 지나가며 도착하고(실제 도착 난제 /
  거대한 정지 Δv), (b)에서는 워프가 그것을 흡수해 정지 상태로 도착한다. Barnard의
  고유운동이 이를 선명하게 보여준다.
- 상수 워프 lead-intercept는 사소한 닫힌 형식 이차식이다 — 수렴 위험이 없다.

프로토타입: `scratchpad/lead_intercept.py`(교과서적 intercept 운동학).

## 5. In-game UI surface (what the plugin shows)

- 맵뷰: 목표 별을 선택 → 그 별의 **예측 도착 지점**(lead 지점, 느린 워프에서는 별의
  현재 마커에서 눈에 띄게 어긋난다), heading 라인, 통과 시간, 도착 상대 속도 /
  정지 Δv를 표시.
- heading 방향으로 워프 engage. (이후) 조종하는 동안 연속 재계산.

## 6. Math ↔ C# boundary

- **Math (this spec + prototype — portable, done):** intercept 솔버, 별 외삽,
  도착 속도 계산. 슐츠가 이를 그대로 이식한다.
- **C# (Schultz):** 맵뷰 후킹 + 라인/마커 렌더링, Kopernicus/DB에서 바디 상태
  공급, 워프 engage, 순항 메커닉, 그리고 UI.

## 7. Open decisions

- 워프 속도 모델 — 상수(이차식) vs 중력 게이팅/티어화(반복).
- `v_w` 값 / 테크 티어(확장 테크 트리에 연동).
- velocity-frame 기본값(a / b / c) — §4가 그 무게를 보여준다.
- 이중성 목적지 궤도 항(DB 궤도요소 사용 vs barycenter-only 근사).
- `v0` 출처(engage 시점 함선의 발사 속도).

## Related

- [warp-and-navigation-brainstorm](warp-and-navigation-brainstorm.md) — §6 frame decision, §7 planner
- [feasibility](feasibility.md) — gate 0
