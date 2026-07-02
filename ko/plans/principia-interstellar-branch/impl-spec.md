---
title: "Principia interstellar branch — implementation spec (hand-off to fable)"
status: ready-for-implementation
created: 2026-07-02
audited_against: mockingbirdnest/Principia master @ 440310a9
research: research/R1-fp-precision.md, R2-soi-code-map.md, R3-soi-numerics.md, R4-thrust-under-warp.md
---

# Principia 성간(interstellar) 브랜치 — 구현 스펙

이 문서는 hand-off의 마스터 문서입니다. **세 개의 workstream**과 그 의존 순서,
그리고 핵심 cross-cutting 결정을 정의합니다. 각 workstream에는 `research/R*.md`에
근거가 갖춰진 상세 스펙이 따로 있습니다(해당 workstream 코딩 전에 대응하는 Rn을
먼저 읽으세요 — 이 파일이 지도이고, 그쪽이 실제 지형입니다).

**독자: 별도 세션에서 구동되는 코딩 모델(fable).** 셋업, 순서, 조정 완료된
설계가 모두 여기 담겨 있어 이 문서만으로 자립합니다.

## 0. 셋업 (어느 세션이든 가장 먼저)

```
git clone https://github.com/mockingbirdnest/Principia
cd Principia && git checkout -b nearstars-interstellar   # base = master @ 440310a9
```

이 문서와 `research/R*.md`의 모든 file:line 인용은 master head `440310a9` 기준입니다.
head가 이동했다면 심볼 이름으로 다시 앵커를 잡으세요(함수는 안정적이고, 줄 번호만
표류합니다). Principia의 빌드는 독자적입니다(MSVC/clang, 대형). KSP 쪽 커밋의
실질적 게이트는 빌드이니 그 부분이 가장 느릴 것으로 예상하고, KSP 설치가 필요
없는 headless C++ 테스트부터 먼저 검증하세요.

## 1. 세 개의 workstream

| # | Feature | Layer | Risk | Depends on |
|---|---|---|---|---|
| **WS1** | 장거리 FP 정밀도 (별별 local origin + DoublePrecision offset) | `physics/ephemeris*` | 낮음 (기본값이 back-compat) | — |
| **WS2** | SOI cutoff + 그룹별 상호작용 (block-diagonal N-body + force-free coasting) | `physics/ephemeris*` | 중간 (numerics) | **WS1** (partition 공유) |
| **WS3** | timewarp 중 연속 추력 | `ksp_plugin/*` + adapter | 중간 (KSP-facing) | 독립 |

**WS1 → WS2는 순차로 빌드합니다** (하나의 자료구조를 공유합니다 — §2 참고).
**WS3는 독립적**이라 병렬 진행이 가능합니다. 트리의 서로 겹치지 않는 부분
(`ksp_plugin/pile_up`, `manœuvre`, adapter)만 건드립니다.

## 2. 핵심 종합 결정 — WS1의 subsystem partition이 곧 WS2의 group 구조

R1은 `subsystem_of_body_`(별별 partition, origin 지역화 목적)를 도입합니다.
R2는 독립적으로 `group_ids_`/`groups_`(별별 partition, pair 루프 블록화 목적)를
도입합니다. **둘은 같은 객체입니다. 둘 다에 쓰이는 partition을 하나만 만드세요.**
`Ephemeris<Frame>` 위에 조정한 구조는 다음과 같습니다(R1 §1.2 + R2 §3 통합).

```cpp
// ONE per-star partition, serves both FP-locality (WS1) and interaction-grouping (WS2).
std::vector<int> subsystem_of_body_;                                   // parallel to bodies_; 0 == Sol
std::vector<DoublePrecision<Displacement<Frame>>> subsystem_origin_offset_;  // WS1: local origin per subsystem
struct BodyGroup { std::vector<std::size_t> oblate_members, spherical_members; };  // WS2: for grouped iteration
std::vector<BodyGroup> subsystem_members_;                             // derived from subsystem_of_body_
std::vector<Square<Length>> soi_cutoff_squared_;                       // WS2: per-body, fixed at ctor
```

따라서 WS1의 커밋 1이 이미 `subsystem_of_body_`를 만들고, WS2는 그것을 재사용하며
`subsystem_members_`(index-list 뷰) + `soi_cutoff_squared_` + taper만 추가합니다.
partition을 두 개 만들지 **마세요**.

**STATIC partition**으로 시작하세요(생성 시점에 할당하고 런타임에 절대 재계산하지
않음). NearStars 로스터에는 이것이 정답이고(별이 계를 옮겨 다니지 않음),
integrator-contract 위험(R2 §6)도 우회합니다. 멤버십은 하나의 적분 스텝 *안에서는*
절대 바뀌면 안 됩니다. 동적 re-grouping(R2 §5, `Prolong:338` 훅)은 실제 필요가
드러나기 전까지 미룹니다.

## 3. 핵심 종합 결정 — SOI cutoff는 매끈한 C² taper이지, 하드 제로가 아님

오너가 밝힌 의도(#2)는 "중력이 ~0으로 수렴하는 지점 너머에서는 *말 그대로 0*으로
취급하고 관성만 남기자"였습니다. R3에 따르면 의도 자체는 옳지만 *문자 그대로의
하드 제로*는 실격이고, **force-free coasting을 그대로 지켜주는** 올바른 메커니즘은
따로 있습니다.

- **공유된 오해의 교정:** Principia의 `QUINLAN_TREMAINE_1990_ORDER_12`는
  **symplectic이 아니라 symmetric linear multistep method**입니다
  (`integrators/methods.hpp:1041`). no-drift 성질은 symplecticity가 아니라
  **time-reversibility**(force = f(q)) + f의 **smoothness**에서 나옵니다.
- **하드 cutoff는 smoothness를 깹니다.** 경계에서 potential에 생기는 높이 μ/r_c의
  계단은 경계를 넘을 때마다 에너지를 주입해 **random-walk secular drift**를
  일으킵니다. Principia가 허용하는 유계 ~1e-13 진동보다 8–12자릿수 크고, 종류도
  잘못됐습니다(진동이 아닌 drift). Principia를 신뢰할 수 있게 만드는 그 성질을
  포기하는 셈입니다.
- **오너의 의도를 지키는 해법:** **POTENTIAL에 거는 C² quintic taper**,
  `Φ̃(r) = Φ(r)·S(r)`, `S(x)=1−10x³+15x⁴−6x⁵`, `x=(r−r₀)/(r_c−r₀)`,
  r≤r₀에서 S=1, r≥r_c에서 0. compact support이므로 r_c 너머에서는 **정확히 0**
  (진짜 force-free 관성 coasting — #2가 원한 바로 그것)이면서, 매끄럽게 램프되어
  잘라낸 계도 여전히 매끄러운 보존계 ⇒ drift 없음. 잔차는 drift가 아닌 *정적*
  모델링 편향(물리적으로 무시 가능)입니다.
- **속도**는 **Verlet neighbor list + skin + hysteresis**(taper와 직교)에서
  나옵니다. O(N²)→O(N·k). 둘을 결합하세요.

**적용 위치 (R3 §5).**
- **Vessel path = 주된 수확, 낮은 리스크** (one-way coupling, 이미 adaptive,
  꼬리는 정말로 무시 가능). vessel당 neighbor list, 각 massive body의 기여에
  C² taper, r_c 너머는 정확히 0. r₀는 a_cut/a_dominant = 1e-6에 배치.
  깔끔한 성간 coasting과 지배적인 speedup을 함께 줍니다. **WS2 안에서 이걸
  가장 먼저 하세요.**
- **Backbone = 부차적, 신중하게.** 각 속박된 항성계 *내부*는 full N². 계 *사이*
  (광년 단위 거리, round-off 아래)에서만 inter-block 항을 0으로 taper →
  block-diagonal force matrix. momentum을 정확히 지키려면 같은 S(r)를 각 pair의
  **양쪽에 대칭으로** 적용하세요(`ephemeris_body.hpp:1372-1378`). 확신이 없으면
  backbone cut은 건너뛰세요 — 병목이 아닙니다.
- **양보 불가 사항 (R3 §5C):** taper는 potential에 걸고 force는 거기서 유도할 것
  (force를 따로 자르면 장이 non-conservative가 됨). backbone에서는 per-pair
  대칭. 최소 C². 수용 게이트로 `physics/ephemeris_test.cpp` +
  `astronomy/ksp_system_test.cpp` / `ksp_resonance_test.cpp` 대비 에너지의
  유계·비-drift를 검증할 것.

R2의 per-pair `continue` cutoff(`:1368`/`:1435`에서의 하드 skip)는 μ/Δq²가 이미
기계적으로 무시 가능할 만큼 멀리 놓인 Tier-A 정합성 비계로서만 허용됩니다.
출시 가능한 형태는 smooth taper입니다. vessel path에는 처음부터 taper를 직접
만드는 쪽을 권합니다.

## 4. Workstream별 빌드 순서

### WS1 — FP 정밀도 (`research/R1-fp-precision.md` 참고)
1. **커밋 1 (headless 정밀도 증명, ~3파일):** `subsystem_of_body_` +
   `subsystem_origin_offset_` 멤버 추가. 기본값 `subsystems = {}` ctor 파라미터
   (비어 있으면 바이트 단위로 legacy와 동일). ctor에서 global→local ingest
   (`ephemeris_body.hpp:122-159`). `:1366`에서 kernel의 same/cross-subsystem
   분기. 호출부에 파라미터 전달. `astronomy/interstellar_precision_test.cpp` 추가
   (star+planet subsystem 두 개, 하나는 4e16 m, legacy control 대비 → 수정 후
   원거리 separation 오차 < 1 mm, control > 1 m 단언).
2. Jacobian(`:1193`) + jerk의 cross-subsystem 분기.
3. Serialization (`physics.proto:181-210` additive. 비어 있으면 legacy 로드 불변).
4. Global-position accessor + plugin 배선 (`plugin.cpp:128-138`). 렌더링만
   globalizing accessor를 경유하도록 라우팅.

### WS2 — SOI cutoff (`research/R2-soi-code-map.md` + `research/R3-soi-numerics.md` 참고)
WS1의 `subsystem_of_body_`를 재사용합니다. 빌드 순서는 다음과 같습니다.
1. massless kernel(`ephemeris_body.hpp:1412-1462`)에 vessel-path C² taper +
   vessel별 neighbor list(R3 §5A) — 깔끔한 coasting + 주된 speedup, 리스크 최저.
   에너지/궤적에 꺾임(kink)이 없는지 검증.
2. Backbone block-diagonal: `subsystem_members_` index list + massive kernel을
   index-list `b2`로 일반화(R2 §2 Tier B). inter-block taper만, pair마다 대칭.
   no-drift 에너지 검증(수용 게이트).
3. (필요할 때만) 일관성을 위해 Jacobian/jerk/potential kernel에도 같은 처리를
   미러링. `Prolong:338`에서 동적 re-grouping.

### WS3 — warp 중 추력 (`research/R4-thrust-under-warp.md` 참고) — 독립
1. `manœuvre_body.hpp:267-278`에서 `ThrustAcceleration` helper 추출.
2. `PileUp`에 `OnRailsBurn`(`pile_up.hpp:196-197`) + 새 AdvanceTime 분기
   (`pile_up.cpp:572-638`), 질량 소모 + dry-mass clamp 포함.
3. Plugin API `VesselSetOnRailsBurn`/`Clear` + C interface + P/Invoke.
4. C# adapter의 packed-branch harvest(throttle/방향/자원 소모, 소진 시
   warp-halt), feature-flag로 게이팅.
5. Prediction 일관성(`FlowPrognostication`) + PileUp serialization.
원칙: burn을 Principia history 위의 intrinsic acceleration으로 표현할 것.
**스톡 KSP `Orbit`에는 절대 쓰지 않습니다** (PersistentThrust가 비호환인 이유 —
Principia issue #2347).

## 5. 전역 수용 게이트
- **Back-compat:** 기존 Principia 테스트 전부가 손대지 않고 통과 (WS1/WS2는
  기본값이 single-subsystem·no-cutoff, WS3는 feature-flag off).
- **WS1:** `interstellar_precision_test`에서 4e16 m 거리 오차 ~9 m → sub-mm.
- **WS2:** taper 활성 상태로 `ephemeris_test` / `ksp_system_test` /
  `ksp_resonance_test`에서 에너지가 **유계이고 drift 없음**을 확인. pair-count /
  비용 절감을 측정.
- **WS3:** `PileUp::AdvanceTime` + `OnRailsBurn`의 headless 테스트가 같은
  thrust/Isp/duration의 기준 flight-plan `Manœuvre`와 일치 (질량 + Δv).

## 6. 의도적으로 범위 밖인 것
- Galactic frame / 은하 스케일 좌표 (오너가 기각. `Barycentric`이 유일한 frame으로
  유지 — WS1은 별별 local origin + DP offset만 사용).
- 동적(런타임 재계산) subsystem 멤버십 (static으로 시작).
- Frenet-locked on-rails 추력 방향 (MVP는 프레임별 관성 고정).
- US² 스타일 integrator/UX 차용 (별도 노트,
  `../universe-sandbox-nbody-comparison.md`).

## 7. 참고 문서
- `research/R1-fp-precision.md` — WS1 전체 스펙.
- `research/R2-soi-code-map.md` — WS2 코드 맵.
- `research/R3-soi-numerics.md` — WS2 numerics/정합성 (taper 논증).
- `research/R4-thrust-under-warp.md` — WS3 전체 스펙.
- `design-draft.md` — 초기 아키텍처 서사 (SOI 문제에 관해서는 R3가 대체.
  WS1은 일치).
- `schultz-dev0/principia-docs/interstellar-audit.md`, `theoretical_implementation.md`
  — 원 감사 문서 (참고: 감사가 제안한 galactic 레벨은 WS1에서 제외됨).
