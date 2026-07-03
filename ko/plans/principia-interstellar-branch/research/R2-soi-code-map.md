# R2 — SOI cutoff + grouped interaction (code-mapping)

리서치 에이전트: opus. 소스 head 440310a9. 물리적 정합성 판단은 R3 소관입니다.

## 0. No existing SOI machinery
physics/, ksp_plugin/ 에서 `sphere_of_influence|SOI|dominant|HillRadius|LagrangeEquipotential` 를 grep 한 결과, 걸리는 것은 **Lagrange equipotential 플로팅 오버레이**(`physics/lagrange_equipotentials*.hpp`, 렌더링 전용이며 integrator 에 입력되지 않음)뿐입니다. `subsystem` → `hierarchical_system_body.hpp` 만 해당(구성 시점의 Jacobi helper 이지 런타임이 아님). **별 단위 subsystem 파티션 역시 코드에 존재하지 않습니다 — 아래의 `groups_` 구조가 곧 그 파티션이며, SOI cutoff 는 그 위에 얹히는 두 번째 필터입니다.** (R1 의 `subsystem_of_body_` 와 같은 개념으로 정합됩니다.)

## 1. Gravity path + cutoff insertion points
- Massive accel 바인딩: `MakeMassiveBodiesNewtonianMotionEquation` (`ephemeris_body.hpp:1133-1147`) → `ComputeGravitationalAccelerationBetweenAllMassiveBodies`; integrator 는 ctor `:166-170` 에서 생성됩니다.
- Massless 바인딩: `:366-385`, `:422-436`, `:453-470` → `...OnMasslessBodies`.
- 디스패처 `:1503-1552`: oblate-oblate + oblate-spherical + spherical-spherical 로 나뉘며, oblate-low-index 불변식(`:138-159`, `ephemeris.hpp:514-516`)을 활용해 각 쌍을 한 번만 방문하고 뉴턴 제3법칙 dual update 를 수행합니다.
- Pairwise kernel `:1342-1410`. **Cutoff 삽입 지점: `:1368` 의 `Δq²` 이후, `:1369` 의 Sqrt 이전**: `if (Δq² > cutoff²(b1,b2)) continue;` (제곱값 비교, Sqrt 불필요). 값은 정확히 0 이 되지만 O(N²) 이득은 아닙니다(여전히 모든 b2 를 방문).
- Massless kernel `:1412-1462`, 루프 `:1431-1460`; `Δq²` 는 `:1435`. SOI 테스트는 기존 충돌 테스트 `:1437-1441` 옆에 배치합니다: `if (Δq² > soi_cutoff²(b1)) continue;`. 모든 SOI 밖에 있는 vessel 은 accel 이 0 이 되어 관성 비행(coast)합니다.
- **동일한 cutoff 가 필요한 자매 kernel 들**(빠뜨리면 에너지/변분량이 어긋납니다): Jacobian `:1174-1208` (루프 :1187), jerk `:1210-1247` (:1224), potential `:1464-1501` (:1477), single-body query `:1249-1340`.

## 2. Grouped iteration (the O(N²)→O(Σnₖ²) win)
- **Tier A** (§1 의 per-pair skip): 구조 변경 없이 정확성만 확보하며, Δq 계산은 여전히 O(N²) 입니다. 먼저 수행합니다.
- **Tier B** (grouped): 연속 인덱스 범위(`:1514-1549`)를 그룹 내부(intra-group) 쌍 열거로 교체합니다. 그룹은 oblate/spherical 이 섞인 임의의 인덱스 집합이므로 → 그룹마다 두 개의 인덱스 리스트(`oblate_members`, `spherical_members`)를 유지하고, 세 개의 템플릿 kernel 을 그 리스트로 제한해 호출합니다. kernel 이 `[b2_begin,b2_end)` 대신 `std::vector<std::size_t> const& b2_indices` 를 받도록 일반화합니다(`:1360` 의 루프 헤더만 기계적으로 바꾸면 되고, 본문은 그대로입니다). 그룹 간(cross-group) 쌍은 아예 열거되지 않습니다.

## 3. Data structures (= the subsystem partition)
`Ephemeris` private, `ephemeris.hpp:535`/`:548` 근처에 추가합니다.
```cpp
std::vector<int> group_ids_ ABSL_GUARDED_BY(lock_);        // == subsystem_of_body_ (R1)
struct BodyGroup { std::vector<std::size_t> oblate_members, spherical_members; };
std::vector<BodyGroup> groups_ ABSL_GUARDED_BY(lock_);
std::vector<Square<Length>> soi_cutoff_squared_;           // per-body, fixed at ctor (0 ⇒ no cutoff)
```
`group_ids_`/`groups_` 는 mutable 이며 lock 으로 보호합니다(천체가 이동하면 소속이 바뀌므로). `soi_cutoff_squared_` 는 immutable 이며 — `MassiveBody` 에 `sphere_of_influence()` accessor 를 붙이는 방식을 권장합니다(직렬화/identity 와 함께 이동). **먼저 STATIC 파티션으로 시작하세요**(생성 시 할당하고 재계산하지 않음) — integrator-contract 관련 위험을 전부 우회할 수 있습니다.

## 4. Vessel zero-accel path
`compute_acceleration` 람다 → `...ByAllMassiveBodiesOnMasslessBodies` (`:1554-1591`) → b1 별 `...ByMassiveBodyOnMasslessBodies` 에서 SOI 테스트. 모든 b1 이 skip 되면 → accel 0 → 관성 coast. Intrinsic(엔진) accel 은 그 이후에 더해지므로(`:377-381,:432,:465`) → 심우주에서 연소 중인 vessel 도 정상적으로 추력을 냅니다. Single-body 래퍼 `:623-642` 도 이를 그대로 상속합니다.

## 5. Group-recompute hook (if dynamic)
fixed-step 경계에서만 수행합니다: `Ephemeris::Prolong` (`:312-344`), `:338` 의 `instance_->Solve` 직전에 `RecomputeGroups_locked()` 를 삽입합니다(:315 에서 이미 `lock_` 보유). `compute_acceleration` 내부에서는 절대 하지 않습니다. Static 파티션이라면 생성 이후 no-op 입니다.

## 6. Integrator-contract constraint (→ R3)
`compute_acceleration` 시그니처는 고정되어 있으므로(`:1138-1144`) — 그룹 데이터는 파라미터가 아닌 `this` 에서 읽습니다. SRKN/multistep 은 한 step 안에서 여러 stage point 의 accel 을 평가하므로 ⇒ (1) 힘 법칙은 step 내내 일정해야 하고(accel 안에서 그룹은 read-only), (2) 소속 변경은 step 사이에서만(Prolong hook), (3) per-pair 하드 cutoff 자체가 — 천체가 stage 사이에 cutoff² 를 넘나들면 — step 내부의 힘 불연속입니다. R3 가 결정합니다: 수치적으로 무시 가능한 꼬리에서의 cutoff 를 수용할지 vs C¹/C² smooth taper 를 쓸지. Static 파티션은 grouping 쪽 위험을 제거하며, SOI tail cut 만 남습니다. **[R3 verdict: potential 에 대한 smooth C² taper, 쌍마다 대칭, + Verlet skin+hysteresis. R3 참조.]**

## Files
- `physics/ephemeris.hpp`: :535/:548 근처의 멤버; `RecomputeGroups_locked()` 선언; index-list kernel overload.
- `physics/ephemeris_body.hpp`: :1368/:1435 의 cutoff + 미러 :1235/:1195/:1481; 디스패처 :1514-1549 재구성; :338 의 hook; ctor :96-171 에 `soi_cutoff_squared_` 배선.
- Schema (flag): `physics/massive_body.hpp` SOI radius source.
