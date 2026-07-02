---
title: "Principia interstellar-precision branch — design draft"
status: draft
created: 2026-07-02
audited_against: mockingbirdnest/Principia master @ 440310a9
supersedes_line_numbers_in: schultz-dev0/principia-docs/interstellar-audit.md (head cc6522fc9)
---

# Principia 성간 정밀도 브랜치 — 설계 초안

**한 줄 목표.** 하나의 Principia 시뮬레이션이 **Sol과 하나(또는 소수)의 원거리 항성계를 동시에**, **각 별마다 완전한 궤도 정밀도로** 담을 수 있게 합니다. 즉 Sol계가 함께 시뮬레이션되는 상태에서 우주선이 알파 센타우리 행성의 저궤도를 돌 수 있고, 별들은 서로 물리적으로 섭동을 주고받습니다.

이 문서는 포크가 아니라 **설계 초안**입니다. 현재 `master`(head `440310a9`)를 새로 정독한 결과에 근거하며, 아래의 file:line 인용은 모두 그 head 기준으로 재검증되어 `cc6522fc9` 기준으로 작성된 이전 감사를 대체합니다. 산출물은 아키텍처, 구체적인 수정 지점, 그리고 슐츠(또는 우리)가 그대로 구현에 착수할 수 있는 단계별 프로토타입 계획입니다.

자매 문서로는 `schultz-dev0/principia-docs/interstellar-audit.md`(원래 감사), `theoretical_implementation.md`(데이터-only Option 1), `../universe-sandbox-nbody-comparison.md`(별개의 적분기/UX 문제 — **여기서는 범위 밖**)가 있습니다.

---

## 1. 문제를 정확하게 진술하면

Principia는 모든 위치를 **하나의 평평한 관성 프레임 안에서 IEEE-754 `double` 세 개**로 저장합니다. 이 체인은 정확히 정의되어 있어 해석의 여지가 없습니다.

- `Position<Frame> = Point<Displacement<Frame>>` → `Vector<Length, Frame>` →
  `R3Element<Length>` → `Quantity<Length>` = 단일 `double magnitude_`
  (`quantities/quantities.hpp:83`, `geometry/point.hpp:66`,
  `geometry/grassmann.hpp:67`, `geometry/r3_element.hpp:75-91`).
- `double`의 분해능은 ≈ `2⁻⁵² · |x|`. 미터 단위로 보면 다음과 같습니다.

| 프레임 원점으로부터의 거리 | ULP (위치 분해능) |
|---|---|
| 1 AU | ≈ 33 µm |
| Sol → 명왕성 | ≈ 1.6 mm |
| Sol → **알파 센타우리** (4.0e16 m) | **≈ 9 m** |
| Sol → 바너드 (5.6e16 m) | ≈ 12 m |
| Sol → Trappist-1 (3.8e17 m) | ≈ 84 m |

좌표 원점 하나가 Sol → 다른 별까지 걸쳐야 하는 순간, 그 별 근처의 위치는 수 미터에서 수십 미터의 분해능을 잃습니다. 순항에는 충분하지만 궤도역학에는 치명적입니다(저궤도를 수 년에 걸쳐 안정적으로 적분하려면 서브미터 정밀도가 필요합니다).

**손실이 실제로 아프게 다가오는 지점 — cancellation 발생지.** 저장 자체만의 문제가 아니라 중력 커널이 문제입니다. `physics/ephemeris_body.hpp:1366`에서 이렇게 계산합니다.

```cpp
Displacement<Frame> const Δq = position_of_b1 - positions[b2];   // :1366
```

여기서 `positions`는 `q_stage`인데, 적분기가 **`DoublePrecision` 상태를 평범한 double로 납작하게 만들면서 오차항을 버린 것**입니다
(`integrators/symplectic_runge_kutta_nyström_integrator_body.hpp:114`). 그래서 공유 원점에서 둘 다 ≈ 4e16 m 떨어진 행성과 그 별의 경우, `Δq`는 거의 같은 두 큰 double의 차 → **파국적 cancellation**이 일어나 ~1e10 m 규모의 궤도 변위에 유효숫자가 ~5자리밖에 남지 않습니다. 같은 `Δq = rᵢ − rⱼ` 관용구가 massless 커널(`:1433`), 야코비안(`:1184-1193`), jerk(`:1230-1232`), 퍼텐셜에도 반복되므로 헬퍼 하나로 전부 커버됩니다.

**`DoublePrecision<T>`가 이미 우리를 구해주지 못하는 이유.** 이는 보상 합산(compensated summation, `{T value; Difference<T> error;}`, `numerics/double_precision.hpp:59-60`)이고 적분기 상태 내부에서 실제로 쓰이지만(`ordinary_differential_equations.hpp:167-171`), 보상하는 것은 **스텝-대-누적합** 반올림이지 두 항성계 사이의 **값-빼기-값** cancellation이 아닙니다. 게다가 오차항은 `q_stage`를 만들 때(`:114`)와 궤적에 append할 때(`ephemeris_body.hpp:1111`) 모두 버려집니다. 저장은 단일 double입니다.

**자명한 두 옵션이 실패하는 이유** (`theoretical_implementation.md`).
- *Sol 원점, 별은 섭동자(데이터-only).* **항성 운동**(별이 Sol의 행성에 미치는 인력)에는 통하고 코드가 전혀 필요 없지만, `r_planet − r_star`가 위와 같이 cancel되어 **원거리 행성 정밀도는 확보되지 않습니다**.
- *은하 중심 원점.* Sol 자체가 ~55 km 분해능에 떨어집니다. 행성 하나 놓기도 전에 플레이 불가입니다.

어느 쪽도 원거리 별에서 *플레이*하게 해주지 못합니다. 이 브랜치가 메우는 갭이 바로 그것입니다.

---

## 2. 이미 우리를 보호해주는 것들 (브랜치 범위를 크게 좁혀줍니다)

플러그인 감사의 핵심 발견은 **렌더링과 버블 내 우주선 물리는 이미 floating-origin에 안전하다**는 것입니다. 디스플레이 문제는 우리가 풀 필요가 *없습니다*.

- **우주선 World는 매 프레임 재앵커링됩니다.** `Plugin::BarycentricToWorld`가
  Unity의 `World::origin`을 기준(루트) 파트에 놓고
  (`ksp_plugin/plugin.cpp:702-752`), 어댑터가 매 `FixedUpdate`마다 이를 구동하며
  모든 천체를 그 오프셋만큼 이동시킵니다
  (`ksp_plugin_adapter.cs:1596-1670`). 무게중심 좌표의 크기와 무관하게
  우주선 근처 좌표는 작게 유지됩니다.
- **P/Invoke 경계는 전부 `double`입니다** (`XYZ`/`QP` = `double`,
  `serialization/journal.proto:24-29`, `interface.cs:52-67`).
- **KSP로의 핸드오프는 부모-상대 `AliceSun`입니다**
  (`VesselFromParent`/`CelestialFromParent` → `RelativeDegreesOfFreedom<AliceSun>`,
  `ksp_plugin/plugin.hpp:334-345`). KSP 자체의 계층적 `Orbit`을 그대로 반영한 구조입니다.
  부모-상대 물리량은 본질적으로 스케일에 무관하며 — **per-star 설계가 기댈 자연스러운 이음새**가 바로 여기입니다.

따라서 고장 지점은 사방에 퍼져 있는 게 아니라 **세 곳에 집중**되어 있습니다.

1. **단일 `Ephemeris<Barycentric>`** — 적분과 Chebyshev 피팅이 1 mm 허용오차로
   돌아가는데(`ksp_plugin/integrators.cpp:34,41,80`) 원거리 별에서의 ULP는 ~4 m라서
   피팅이 수렴할 수 없고 천체 간 동역학에 미터급 노이즈가 실립니다. *실질적인 작업은 여기입니다.*
2. **단일-태양 가정** — `Plugin::sun_`(`plugin.hpp:588`, 유일성 CHECK가
   `plugin.cpp:250-256`)과 태양에 앵커된 맵 뷰
   (`renderer.cpp:197-205`, `Planetarium.fetch.Sun.position`이 공급됨).
3. **맵 뷰 float 경계** — `ScaledSpacePoint {float x,y,z}`
   (`planetarium.hpp:44-46`)는 앵커에서 1e16 m 떨어진 시스템을 볼 때 붕괴합니다.
   로컬 별 기준 재중심화가 필요합니다(어댑터 쪽 작업).

---

## 3. 아키텍처 — 별 단위 *subsystem* ephemeris

세 개의 서브시스템 감사(geometry, dynamic frames, ephemeris)가 하나의 답으로 수렴합니다. 성간 거리를 담는 오프셋은 **저장되는 `Position`에 기록되기 전에 분리**되어야 합니다. 피연산자가 이미 손실을 입은 변환 레이어에서 주입하는 방식(`geometry/affine_map_body.hpp:42`)으로는 안 됩니다. 구체적으로는 다음과 같습니다.

### 3.1 상태 표현

ephemeris 바디들을 **subsystem** `S(i)`로 분할합니다(Sol = subsystem 0, 원거리 별 각각 = 자체 subsystem). 그 다음.

- 각 subsystem `S`는 **원점** `O_S`(그 무게중심)를 가지며, 전역 관성 `Barycentric` 프레임에서
  **`DoublePrecision<Position<Barycentric>>`**로 유지됩니다.
  성간 규모의 크기가 사는 곳은 오직 여기뿐이고, double-double이 ~32자리의 여유를 줍니다.
- 각 바디의 **저장 위치는 로컬**입니다. `q̃ᵢ = qᵢ − O_{S(i)}`, 크기는
  시스템 크기 이하(넓은 쌍성이면 ~1e13 m, 행성이면 ~1e11 m) → **평범한 `double`로 서브밀리미터**.
  `Position` 자체의 저장 포맷은 바뀌지 않습니다. 여전히 `{double x,y,z}`이고, 다만 가까운 원점에서 잰다는 점만 다릅니다.
- 원점 간 오프셋 `Δ_{AB} = O_B − O_A`는 `DoublePrecision` 뺄셈으로 얻습니다
  (`TwoDifference`, Point−Point→Vector 오버로드,
  `numerics/double_precision.hpp:104-119`). 정확하며 cancellation 문제가 없습니다.

`Frame::is_inertial` static_assert(`ephemeris.hpp:69`, `reference_frame.hpp:47`)는 **그대로 유지**됩니다. subsystem 원점은 *평행이동*이고, 축은 공유되는 관성 `Barycentric` 방향을 유지합니다. 별마다 회전시키지 **않습니다**.

### 3.2 중력 커널 — same/cross-subsystem 분기

쌍별(pairwise) 커널(`ephemeris_body.hpp:1346-1410`, 디스패처 `:1505-1552`)에 새 헬퍼 `Displacement Δq(b1, b2)` 하나를 추가합니다.

- **같은 subsystem** (`S(b1) == S(b2)`): `Δq = q̃[b1] − q̃[b2]` — *오늘의 `:1366`과 동일*하되,
  두 피연산자가 모두 작으므로 이제 cancellation이 없습니다.
  **뜨거운 Sol 내부 루프는 변경도 비용도 없습니다.**
- **다른 subsystem**: `Δq = (q̃[b1] − q̃[b2]) + Δ_{S(b2)S(b1)}`. 여기서 요구되는
  정밀도는 오히려 *낮습니다*. 4e16 m 간격에서 cross 항 가속도는 intra 항의 ~1e-14 수준이라
  중요한 것은 자릿수가 아니라 크기(magnitude)입니다. `DoublePrecision`으로 계산해
  `.value`를 취하면 되고, 이득은 전적으로 *intra*-subsystem `Δq`를 정확하게 유지하는 데 있습니다.

subsystem 소속은 바디 인덱스의 속성이므로, 디스패처 루프(`:1514-1548`)는 **subsystem 블록 단위의 쌍 범위**를 순회합니다. 즉 same-vs-cross는 **쌍마다의 검사가 아니라 루프 수준의 분기**라 핫패스 비용이 없습니다. 편평도/geopotential 분기(`:1381-1407`)도 같은 `Δq`를 소비하므로 공짜로 고쳐집니다.

### 3.3 원점 운동 — 어려운 하위 결정 (플래그만, 아직 미결정)

subsystem 원점은 고정이 아닙니다. 별들은 서로를 가속시킵니다. 두 옵션이 있고, 프로토타입을 통해 슐츠와 함께 결정합니다.

- **(A) 각 원점을 추가 ODE 변수로 적분.**
  `DoublePrecision<Position<Barycentric>>` 타입으로 두고 RHS 전체에서 full double-double을 유지합니다.
  물리적으로 가장 깨끗하지만, 원점 변수에 한해 `error` 항을 `q_stage`까지 배관해야 합니다
  (오늘은 `symplectic_..._body.hpp:114`에서 버려짐).
- **(B) 운동학적 / 주기적 re-anchoring.** 원점을 측정된 공간속도로 전진시키고
  (성간 조석은 로컬 중력의 ~1e-15 수준이라 KSP 시간 규모에서 무시 가능 —
  `interstellar-audit.md §7.4`), 누적된 원점 드리프트를 `QuickTwoSum`으로 주기적으로
  로컬 좌표에 **접어 넣습니다(fold)**. `Prolong`의 고정 적분 스텝 사이에 들어가는
  "rebasing" 스텝입니다. 더 단순하고, 결합이 무시 가능하므로 충분히 정확합니다.

첫 프로토타입은 **(B)로 기울어** 있습니다. 성간 중력 결합은 물리적으로 무시 가능하므로, 원점을 완전 정밀도로 적분하는 (A)는 필요성이 입증되기 전까지는 과설계입니다. (B)는 적분기 루프를 건드리지 않습니다. 타이트한 항성 쌍성(α Cen A–B, 80년)에서 원점 드리프트 fold가 가시적 오차를 만드는 경우에만 재검토합니다.

### 3.4 궤적 저장

`AppendMassiveBodiesStateToTrajectories`(`ephemeris_body.hpp:1101-1116`)는 오늘 전역 `positions[i].value`를 append합니다(`:1111`). 대신 **로컬** `q̃ᵢ`를 각 바디의 `ContinuousTrajectory`에 append하고, 추가로 **subsystem별 원점 궤적**(`O_S(t)` — 작은 `ContinuousTrajectory`, 또는 옵션 B에서는 해석적 `O_S₀ + v·t`에 fold 지점을 더한 것)을 유지해야 합니다. Newhall/Chebyshev 피팅(`continuous_trajectory.hpp:186-201`)은 **평행이동 불변**이라 로컬 시계열을 그대로 피팅하며 — 그 1 mm `tolerance_`가 원거리 별에서 마침내 *달성 가능*해집니다. 전역 위치가 필요한 `EvaluatePosition` 호출자는 `q̃ + O_S`를 합성하고, 별-로컬 플로팅 프레임에 공급하는 호출자는 `q̃`를 직접 소비합니다(권장).

### 3.5 프레임 / 플로팅 레이어 — 기존 것 재사용

새로운 프레임 *대수*는 없습니다. Principia는 이미 `ReferenceFrame<InertialFrame, ThisFrame>`(`physics/reference_frame.hpp:45-47`)으로 궤적을 런타임 프레임에 재표현하고 `RigidMotion`을 합성합니다(`physics/rigid_motion_body.hpp:173`). **별-로컬 플로팅 프레임**은 `BodyCentredNonRotatingReferenceFrame`(`body_centred_non_rotating_reference_frame_body.hpp:25-79`)과 똑같은 방식으로 만든 새 `RigidReferenceFrame` 서브클래스입니다 — 단, 그 `ToThisFrameAtTime`은 **별-로컬** ephemeris 좌표(`q̃`)로부터 변환을 만들고, 우주선 위치를 절대 `Barycentric` double로 왕복시키지 않습니다. `GravitationalAcceleration(t, q)`(`rigid_reference_frame.hpp:183-185`)에 별-로컬 오버로드를 추가해 원거리 별 근처의 가속도가 작은 로컬 변위로부터 계산되도록 합니다.

필요한 것은 **소수의 새 컴파일타임 프레임 태그**(별마다 관성급 태그 하나씩, `Barycentric`이 선언된 방식 그대로, `ksp_plugin/frames.hpp:39-43`)와 각각에 짝지어진 **런타임 `DoublePrecision` 앵커**뿐입니다 — 프레임 템플릿 재작성이 *아닙니다*.

### 3.6 플러그인 레이어

- **멀티-태양.** `sun_` 유일성 가정을 제거합니다(`plugin.hpp:588`, CHECK는
  `plugin.cpp:250-256`). 플러그인은 **별들의 집합**을 들고, 활성 별은
  우주선의 현재 subsystem으로 선택됩니다.
- **맵 뷰 앵커링.** `Renderer::BarycentricToWorld`(`renderer.cpp:197-205`)의
  World 앵커링을 Sol의 태양에서 **로컬 별**로 전환하고, 어댑터는
  `Planetarium.fetch.Sun.position` 대신 그 별의 `ScaledSpace` 위치를 공급합니다.
- **ScaledSpace float 경계.** `plotting_to_scaled_space`
  (`interface_planetarium.cpp:100-109`)는 `float` 캐스트(`planetarium.hpp:44-46`)
  이전에 **로컬** scaled-space 원점을 빼야 합니다. 로컬 시스템 기준 재중심화이며 어댑터 쪽 작업입니다.
- **이음새는 그대로 둡니다.** 부모-상대 `AliceSun` API들(`plugin.hpp:334-345`)은
  **변경이 필요 없습니다** — 이미 계층적이고 스케일에 무관합니다.
- **직렬화 / 세이브 호환.** `Plugin::WriteToMessage`(`plugin.cpp:1512`)는
  하나의 ephemeris + `Barycentric` 궤적들을 저장하는데, 세이브 포맷에
  subsystem 분할 + subsystem별 `DoublePrecision` 원점이 추가됩니다.
  `serialization::DoublePrecision`은 이미 존재하므로
  (`double_precision.hpp:55-57`) 와이어 포맷 확장은 작고, 새 별-프레임 enum 값은
  `serialization/geometry.pb`의 `Frame` enum에 들어갑니다.

---

## 4. 대안들을 택하지 않는 이유

| 대안 | 판정 |
|---|---|
| **컴파일타임 프레임 중첩** (`Frame<Parent, …>`) | 기각. `Frame`은 빈 태그(`frame.hpp:52-79`)라 오프셋을 유의미하게 담을 수 없고, 이를 매개변수화하면 코드베이스의 모든 템플릿에 파문이 번지는데 얻는 게 없습니다. 중첩은 물리 레이어의 몫입니다. |
| **은하 중심 원점** | 기각. Sol 자체가 ~55 km로 분해됩니다(`theoretical_implementation.md`). 플레이 불가. |
| **`DoublePrecision<Position>` 전면 저장** | 주 메커니즘으로는 기각. 모든 궤적의 저장/대역폭이 2배가 되는데, 문제는 다이내믹 레인지가 아니라 **cancellation**입니다 — 로컬 원점이 큰 피연산자를 아예 제거하므로 subsystem 내부는 평범한 double로 충분합니다. `DoublePrecision`은 소수의 원점 간 오프셋에*만* 씁니다. |
| **데이터-only 섭동자 (Option 1)** | **별도의 출하 가능한 마일스톤**으로 유지 — §5 stage 0 참조. 코드 없이 항성 운동 결합을 주지만, 원거리 행성 플레이는 안 됩니다. |

---

## 5. 단계별 프로토타입 계획

각 단계가 독립적으로 테스트 가능하고 다음 단계의 리스크를 줄이도록 순서를 잡았습니다.

- **Stage 0 — 데이터-only 섭동자 (코드 없음).** `theoretical_implementation.md`에 따라
  알파 센타우리 A/B를 `sol_gravity_model.proto.txt` + 초기 상태에 추가합니다.
  Gaia→ICRS→Cartesian 파이프라인과 ephemeris가 두 번째 별을 애초에 받아들이는지를
  검증합니다. 오늘 바로 출하 가능하며, 기준선 오차(우리가 제거하려는 ~9 m)를 확립합니다.
- **Stage 1 — subsystem 분할 + 로컬 저장 (headless).** `physics/ephemeris*`에
  subsystem id, 로컬-원점 상태, `Δq` 헬퍼(§3.2), 원점 처리 옵션 B(§3.3)를 추가합니다.
  C++ 테스트로 검증합니다(`trappist_dynamics_test.cpp`를 본떠서). Sol + α Cen을 100년
  적분하고, 평평한 프레임에서 미터급 노이즈를 보이던 α Cen 내부 궤도 요소가 이제
  서브밀리미터로 안정적임을 확인합니다. **아직 KSP는 없습니다.** 이것이 핵심 증명입니다.
- **Stage 2 — 별-로컬 플로팅 프레임.** `RigidReferenceFrame` 서브클래스(§3.5)와
  프레임 태그를 추가합니다. α Cen b 근처의 우주선 상태가 로컬 프레임을 통해
  정밀도 손실 없이 왕복하는지 검증합니다.
- **Stage 3 — 플러그인 멀티-태양 + 맵 앵커링** (§3.6). KSP를 마주하는 작업입니다.
  멀티-별 플러그인 상태, 로컬-별 World/ScaledSpace 앵커링, 세이브 포맷.
  실제 KSP 빌드가 필요합니다 — 슐츠의 영역입니다(C#/어댑터 + Principia 빌드 체인).
- **Stage 4 — 우주선의 시스템 횡단.** 비행 중에 우주선의 `DiscreteTrajectory`를
  한 subsystem 프레임에서 다른 프레임으로 넘깁니다. 다른 모든 것의 하류이며,
  성간 순항 유스케이스입니다(`project_nearstars_interstellar_expansion`에 따라
  warp/relativity 프로파일 뒤로 게이트될 수 있습니다).

Stage 0–2는 **KSP 설치 없이** 빌드/테스트 가능해서(Principia 테스트 스위트는 독립 실행 C++), 짧은 시간 안에 의미 있는 초안이 가능한 이유가 바로 이것입니다. Stage 3–4는 슐츠가 맡을 더 무거운 KSP 통합 작업입니다.

---

## 6. 수정 지점 지도 (코드 수준 스케치)

| 레이어 | File:line (master 440310a9) | 변경 |
|---|---|---|
| 중력 커널 | `physics/ephemeris_body.hpp:1366,1433,1184-1193,1230-1232` | `Δq = rᵢ − rⱼ`를 subsystem-aware 헬퍼로 교체 (§3.2) |
| 디스패처 | `physics/ephemeris_body.hpp:1505-1552` | subsystem 블록 단위 쌍 범위 순회 |
| 상태 레이아웃 | `physics/ephemeris_body.hpp:95-171` | 바디를 subsystem으로 분할, 로컬 위치 시드, subsystem별 원점 추가 |
| 궤적 append | `physics/ephemeris_body.hpp:1101-1116` | 로컬 `q̃` append, 원점 궤적 유지 (§3.4) |
| 공개 접근자 | `physics/ephemeris.hpp:154-159,253-285` | `EvaluateAllPositions`, `ComputeGravitationalAcceleration…`의 로컬/전역 변형 |
| 원점 운동 | `integrators/symplectic_..._body.hpp:114` | (옵션 A일 때만) 원점 변수에 한해 `.error`를 `q_stage`로 배관 |
| DoublePrecision 오프셋 | `numerics/double_precision.hpp:104-119` | (그대로 사용) 정확한 원점 간 `Δ`에 `TwoDifference` |
| 별-로컬 프레임 | 신규 `physics/star_centred_inertial_reference_frame*.hpp` | `RigidReferenceFrame` 서브클래스, 패턴은 `body_centred_non_rotating_…` |
| 프레임 태그 | `ksp_plugin/frames.hpp:39-43` | 별마다 관성 태그 하나 + `DoublePrecision` 앵커 |
| 멀티-태양 | `ksp_plugin/plugin.hpp:588`, `plugin.cpp:250-256` | 별들의 집합, `sun_` 유일성 제거 |
| 맵 앵커링 | `ksp_plugin/renderer.cpp:197-205` | World를 로컬 별에 앵커 |
| ScaledSpace | `ksp_plugin/interface_planetarium.cpp:100-109`, `planetarium.hpp:44-46` | float 캐스트 전 로컬 scaled-space 원점 적용 |
| 세이브 포맷 | `ksp_plugin/plugin.cpp:1512,1572-1575`, `serialization/geometry.pb` | subsystem 분할 + `DoublePrecision` 원점 + 별 프레임 enum |
| 무변경 (이음새) | `ksp_plugin/plugin.hpp:334-345` | 부모-상대 `AliceSun` — 변경 없음 |

---

## 7. 리스크와 미결 질문

1. **원점 운동 선택 (A vs B, §3.3).** α Cen A–B(80년 쌍성)를 옵션 B로 프로토타입하고,
   rebasing fold가 가시적인 장기(secular) 오차를 보이면 A로 격상합니다.
   *사전 결정이 아니라 측정으로 결정합니다.*
2. **rebasing fold를 가로지르는 symplecticity.** 옵션 B의 주기적 re-anchoring이
   고정 스텝 대칭 방법의 무-드리프트 보장을 깨면 안 됩니다. fold는 모든 좌표를
   같은 벡터만큼 옮기는 정확한 `QuickTwoSum` 평행이동이라 원리상 적분기와
   교환(commute)하지만, 명시적인 에너지 드리프트 테스트가 필요합니다
   (Jool 안정성 방법론을 본떠서).
3. **subsystem 경계에서의 Chebyshev 피팅 차수.** 위치가 작아진 뒤 로컬 시계열의
   차수/허용오차가 잘 동작하는지 확인합니다. *개선*될 것으로 기대되지만(§3.4) 검증이 필요합니다.
4. **직렬화 마이그레이션.** 옛 세이브(단일 평평 ephemeris)도 여전히 로드되어야 합니다.
   subsystem 분할에 "모든 것이 subsystem 0"이라는 기본값이 필요합니다.
5. **KSP ScaledSpace / PQS float 경로** (`ksp_plugin_adapter.cs:1663-1665`가
   절대 double을 KSP `CelestialBody.position`에 씁니다). 어댑터가 KSP의 ScaledSpace까지
   재중심화하지 않는 한, 원거리 시스템의 바디들은 KSP 자체의 float 섞인 코드에서
   ~1e16 m가 됩니다. 가장 이해도가 낮은 KSP 쪽 리스크이며, stage 3에서 스파이크가 필요합니다.
6. **빌드 체인.** Principia의 빌드(전용 MSVC/clang, 대규모)가 stage 3–4의 실질적
   관문입니다 — 슐츠의 환경입니다.

---

## 8. 참고 문서

- `schultz-dev0/principia-docs/interstellar-audit.md` — 원래 감사(§7 =
  프레임 중첩 요구사항).
- `schultz-dev0/principia-docs/theoretical_implementation.md` — 데이터-only
  Option 1 + 기각된 두 원점.
- `../universe-sandbox-nbody-comparison.md` — 별개의 적분기/UX 차용 질문(이 브랜치 아님).
- 위의 file:line 인용은 `mockingbirdnest/Principia` master `440310a9`(2026-07-02) 기준으로 검증되었습니다.
