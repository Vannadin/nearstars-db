---
title: Interstellar navigation planner — spec + Δv lead-intercept prototype
status: exploratory
created: 2026-06-28
updated: 2026-06-29
---

# 성간 항법 플래너 — spec

**단계: 탐색.** **Δv 기반 lead-intercept** 플래너를 규정하고 수식 프로토타입을
기록한다. 엔진 무관 — 여기 수식은 이식 가능하고 이쪽이 맡는 절반이다. 인게임
C#(맵뷰 훅·UI·점프/워프 engage)은 슐츠 레인
([[project-nearstars-mod-plugins-schultz]]). 맥락은 [`README`](README.md),
[`warp-and-navigation-brainstorm.md`](warp-and-navigation-brainstorm.md).

## 왜 필요한가 (그리고 왜 무겁지 않고 *가벼운가*)

원래 걱정은 Principia 자체 flight planner가 성간 여정을 못 버틴다는 것 — 수백 년짜리
트랙을 실시간 적분해야 하니까. 이 걱정은 실제로 맞다(그 스팬을 인게임 실시간 prediction
하면 **렉이 심하게 걸린다**). 다만 커스텀 플래너가 필요한 진짜 이유는 더 날카롭다.

- 이동 구간이 **Principia 바깥**이다 — 추력도 중력도 아닌 위치 이동이라 Principia에
  표현할 maneuver가 없고 매틱 되돌려버린다(워프 문서 §2). detach되어 flight plan에서 빠진다.
- 목표 별이 **이동**한다 — 도착 시점에 별이 가 있을 곳을 겨냥해야 하는데(lead-intercept),
  Principia 플래너는 그걸 안 한다.

설계는 **worst-case: 커스텀 Principia 브랜치를 못 쓰는 경우**로 깐다. 포크가 없으면
연속 순항은 불가능하고(no-fork ⇒ 점프만, 워프 문서 §3), 그래서 바닥 메커니즘은
**계산된 점프**다 — (heading·소요시간 `T`·도착점)을 closed-form으로 풀고, **시계를
`T`만큼 빨리감기 + lead 지점에서 vessel re-seed**. 스텝별 실시간 적분 없음(렉 없음),
포크 없음(stock re-seed). 연속 순항은 *포크가 생기면 붙는 업그레이드*가 된다.

이게 걱정을 뒤집는다 — 성간 중력 ≈ 0이라 **적분할 게 없어서**, 플래너는 트랙 솔브가
아니라 closed-form 2차식이다. **Principia read API에 일절 안 기대고**(어차피 제거 중)
오프라인으로 돈다.

유니티 에디터 불필요 — 플래너는 코드 전용 C# 플러그인(IMGUI/stock UI + 맵뷰 라인).
선례: Transfer Window Planner / Astrogator / MechJeb.

## 1. 입력

- **출발** — 함선 위치 `r0`(Sol-바리센터 ICRF) + 속도 `v0`(engage 시점 실제 vessel
  state에서 읽음. 빠져나온 그대로).
- **목표 별** — ICRF 위치 `P0` + 속도 `v_star`. `db/systems` astrometry(RA/Dec·시차·
  pmRA·pmDec·RV → 3D 벡터)로 구성. 미래 위치는 **선형 외삽** `P(t) = P0 + v_star·t`
  (성간 중력 ≈ 0 ⇒ 거의 직선). 쌍성 목표는 **DB 궤도항을 더한다**(옵션 아님, §4.5).
- **Δv 예산** — 함선 드라이브 능력. 이게 *속도 입력*이다. 브라키스토크론(중점까지 가속,
  플립, 정지까지 감속)이 Δv → 소요시간으로 환산. 뉴턴 `T = 4d/Δv`, 광속 근처는 아래
  상대론 형태 사용.

## 2. 알고리즘 — Δv → 소요시간 → lead-intercept

정지-종단 브라키스토크론의 평균속도는 `v_avg = Δv/4`(뉴턴). 상대론 형태(rapidity,
feasibility §2)는 **두 영역을 다 덮고 빛을 못 넘는** 한 줄이다.

```
v_avg = c · tanh(Δv / 4c)          // 저Δv에서 Δv/4, Δv→∞에서 →c (광속 하한 자동)
```

그다음 lead-intercept는 closed-form 2차식 — 함선이 `v_avg·T`를 가는 동안 별이
`v_star·T`만큼 흐른다.

```
R0 = P0 − r0
(v_avg² − |v_star|²)·T² − 2(R0·v_star)·T − |R0|² = 0     →  양근 T
target    = P0 + v_star·T            // 조준점으로 락할 미래 별 위치
heading   = normalize(target − r0)
arrivalRelV = v0 − v_star            // frame-(a). |·| = 도착 감속 Δv
```

`v_avg < c`가 항상 성립 ⇒ 양근이 항상 존재하고 `T > d/c`(광속 하한)가 **별도 FTL 가드
없이** 보장된다. 쌍성 목표는 `v_star`가 위치 의존이라 fixed-point 한 패스(T 추정 → 궤도
위치 → T) 필요. 싸고 well-conditioned.

## 3. 출력

`소요시간 T`, **미래 `target` 지점**(플레이어가 조준을 락하는 곳), `heading`,
`arrivalRelV`(크기 = 도착지 감속 Δv). 도착 *프레임*(v0 유지냐, 드라이브가 별 기준으로
죽이냐)은 **플래너 소관이 아니다** — 워프/드라이브 메커니즘 결정(워프 문서 §6). 플래너는
그 결과를 *표시만* 한다.

## 4. 프로토타입 결과 (실제 DB astrometry, 함선 바리센터, v0 = 0)

`lead offset` = 미래 타겟이 별의 *현재* 위치에서 얼마나 떨어져 있나 — 즉 "지금"을
겨냥하면 얼마나 빗나가나. 광속 하한 `d/c`는 참고로 표시.

| 목표 (거리, \|v_star\|) | Δv | v_avg | T | lead offset | arrive rel-v |
|------------------------|---:|------:|--:|------------:|-------------:|
| Alpha Cen (4.39 ly, 28 km/s) | 1c | 24.5%c | 17.9 yr | 107 AU | 28 km/s |
| | 4c | 76.2%c | 5.8 yr | 34 AU | 28 km/s |
| | 12c | 99.5%c | 4.4 yr | 26 AU | 28 km/s |
| Barnard (5.96 ly, 142 km/s) | 1c | 24.5%c | 24.3 yr | 731 AU | 142 km/s |
| | 4c | 76.2%c | 7.8 yr | 235 AU | 142 km/s |
| TRAPPIST-1 (40.7 ly, 84 km/s) | 1c | 24.5%c | 165.9 yr | 2927 AU | 84 km/s |
| | 4c | 76.2%c | 53.4 yr | 942 AU | 84 km/s |
| | 12c | 99.5%c | 40.9 yr | 721 AU | 84 km/s |

**발견.**
- **`v_avg = c·tanh(Δv/4)`가 FTL 가드를 없앤다.** Δv = 12c에서도 속도는 99.5%c이고
  `T > d/c`가 어디서나 성립 — 광속 하한이 공식에서 떨어진다.
- **lead가 *모든* 현실 속도에서 크다.** 광속에 거의 닿는 Δv = 12c에서도 TRAPPIST-1
  타겟은 현재 마커에서 **721 AU** 떨어져 있고, 1c면 수천 AU다. 시스템이 ~AU 스케일이라
  ⇒ **플래너 없이는 못 맞춘다.** 존재 이유 완전 정당화.
- **"TRAPPIST-1 30~50년"은 Δv ≈ 4~5c**(`v_avg` ~0.76~0.81c) — 반응추진으론 불가능한
  Δv라, 워프-equivalent 드라이브가 그 자리를 채운다는 게 확인된다.
- **도착 rel-v는 별 자신의 속도**(frame-(a), v0 = 0) — Fomalhaut 15 km/s vs Barnard
  142 km/s. 고유운동이 도착 난이도로 살아남는다.

프로토타입: [`prototypes/lead_intercept_dv.py`](../../../gameplay/interstellar-expansion/prototypes/lead_intercept_dv.py)
(Δv → T → 미래 타겟, 실제 DB 벡터).

## 4.5 여정은 3-leg다 (심화 분석, 2026-06-29)

워프/점프는 항성 중력이 무시 가능한 곳에서만 engage 가능하다(깨끗한 detach / re-seed).
그 경계 `r_g`(`GM/r² < ~1e-10 m/s²`)는 **태양급 별 기준 ~0.12 ly**
(`r_g ≈ 0.12·√(M/M☉) ly`. TRAPPIST-1 ≈ 0.037 ly). 그래서 실제 여정은 **leg 1** sublight로
`r_g`까지 상승 → **leg 2** 점프/워프 lead-intercept → **leg 3** 반대편 `r_g` 진입 + 감속 번.

- **leg 2가 거리를 지배** — sublight 양끝은 트립의 0.6 %(TRAPPIST)~5.5 %(αCen) ⇒
  intercept를 단일 Δv-브라키스토크론으로 모델링하는 게 정당. 단 경계가 `v0`(진입)과
  도착 감속을 결정.
- **`r_g` = 워프 engage/disengage 경계** — Blueshift식 중력-게이팅 속도 모델(우물 안
  느림, 평지 빠름)과 맞물린다.
- **감속은 벽이 아니라 싸다.** Barnard의 142 km/s를 토치(Isp 1e6 s)로 죽여도
  **추진제 1.4 %**, 0.007 AU에서 ~4시간 번. 그래서 frame-(a) "빠르게 도착"은 짧은 감속
  비트지 Δv 게이트가 아니다 — 프레임 선택이 블로커가 아니라 flavor인 이유(그 결정은
  워프 문서 소관).
- **쌍성 궤도항은 옵션이 아니라 필수.** Alpha Cen 1c 트랜짓 동안 A 성분은 바리센터 궤도를
  따라 **6.1 AU** 움직인다 — 내부 시스템보다 크다. 바리센터 lead만 겨냥해도 A를 ~6 AU
  빗나간다. αCen이 #1 타깃 ⇒ 쌍성 목표엔 DB 궤도항이 필수.

숫자는 [`prototypes/planner_deep.py`](../../../gameplay/interstellar-expansion/prototypes/planner_deep.py)로 재현 가능.

## 5. 인게임 UI 표면 (플러그인이 보여주는 것)

- 맵뷰: 목표 별 선택 → **Δv** 입력/읽기 → **소요시간 T**, **미래 타겟 마커**(별의 현재
  마커에서 눈에 띄게 오프셋), heading 라인, 도착 rel-v / 감속 Δv 표시.
- 미래 타겟 락 → engage(계산된 점프: 시계 `T` 빨리감기 + re-seed. 또는 포크가 있으면
  순항을 직접 비행하며 연속 re-solve).

## 6. 수식 ↔ C# 경계

- **수식 (이 spec + 프로토타입 — 이식 가능, 완료):** Δv→v_avg, astrometry→별 벡터,
  intercept 솔버, 도착 속도. 슐츠가 그대로 포팅.
- **C# (슐츠):** 맵뷰 훅 + 마커/라인 렌더, Kopernicus/DB에서 바디 state, 점프(시계
  빨리감기 + re-seed) 또는 순항 메커니즘, UI.

## 7. 결정

**분석으로 닫힌 것.**
- 속도 모델 — **Δv 구동**, `v_avg = c·tanh(Δv/4)`. 공식 하나, 광속 하한 안전.
- 쌍성 궤도항 — **필수**(αCen 6 AU 스윙, §4.5).
- re-solve — 단일항성 등Δv는 one-shot 정확, **쌍성 목표는 fixed-point 패스 필요**
  (궤도 곡률).
- `v0` 소스 — engage 시점 **vessel state에서 읽음**.

**남은 것 (대부분 플래너 밖).**
- Δv 값 / 테크 티어 — 확장 테크트리에 연동(게임플레이 설계).
- 속도-프레임 기본값(v0 유지 vs 별 기준 null) — **워프/드라이브 메커니즘 결정**,
  워프 문서 §6. 플래너는 도착 rel-v만 표시.

## Related

- [warp-and-navigation-brainstorm](warp-and-navigation-brainstorm.md) — §6 프레임 결정, §3 점프 vs 순항
- [feasibility](feasibility.md) — gate 0 (Δv 수식, 광속 하한, 상대성)
