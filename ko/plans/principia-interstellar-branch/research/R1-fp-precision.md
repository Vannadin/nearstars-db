# R1 — Long-distance FP precision fix (per-star local origin + DoublePrecision offset)

리서치 에이전트: opus. 소스: mockingbirdnest/Principia 브랜치 `nearstars-interstellar`, head 440310a9. 오너 공리는 다음과 같습니다. 은하 좌표계(galactic frame)는 도입하지 않고, `Barycentric`이 유일한 적분 프레임으로 유지되며, subsystem(0 = 로컬 원점의 Sol, 원거리 항성 각각 = subsystem 하나)이 Sol 기준 `DoublePrecision<Displacement<Barycentric>>` offset을 보유합니다.

## 0. Root cause (verified)
- `Position<Barycentric>` = 축당 `double` 하나입니다 (`quantities.hpp:83` → r3_element → grassmann → space.hpp).
- Cancellation 발생 지점은 `ephemeris_body.hpp:1366`의 `Δq = position_of_b1 - positions[b2]`입니다. 두 값 모두 ~4e16 m → ULP ≈ 9 m가 되어, 시스템 내부의 작은 separation이 소실됩니다.
- 적분기 `symplectic_runge_kutta_nyström_integrator_body.hpp:114,133`는 바디별 DoublePrecision을 유지하지만 *증분(increment)*만 보상합니다. 해상도를 결정하는 것은 절대 크기이므로, 원점을 로컬화해 |q.value|를 ~1e13 m로 줄이면 ULP ~2e-3 m이 됩니다. 즉 원점 재배치(relocation)가 해법입니다.

## 1. Data structures
Subsystem별로 `DoublePrecision<Displacement<Barycentric>> origin_offset`을 저장합니다 (Position이 아니라 Displacement입니다 — 4e16짜리 Position double을 절대 실체화하지 않습니다). 두 offset의 차는 다시 DoublePrecision<Displacement>입니다 (`double_precision.hpp:149-151`). Offset은 상수이며 적분 대상이 아닙니다.

`Ephemeris<Frame>` 멤버는 `ephemeris.hpp:534-535` 근처에 둡니다.
```cpp
std::vector<int> subsystem_of_body_;                                    // parallel to bodies_; 0 == Sol
std::vector<DoublePrecision<Displacement<Frame>>> subsystem_origin_offset_;  // index == subsystem id; [0] zero
```
생성자에는 후행 인자 `std::vector<int> const& subsystems = {}`를 추가합니다 (기본값 ⇒ 단일 subsystem 0 ⇒ 레거시와 바이트 단위로 동일).

## 2. Ingest global→local (Ephemeris ctor `ephemeris_body.hpp:122-159`)
`CHECK_EQ(bodies.size(), initial_state.size())` (:114) 이후에 처리합니다. Subsystem 벡터를 정규화하고, 각 subsystem의 anchor는 그 첫 입력 바디의 global position으로 잡으며, `subsystem_origin_offset_[s] = TwoDifference(anchor[s], anchor[0])`로 계산합니다 (Point×Point 오버로드, `double_precision.hpp:104-119`). 바디별 루프에서 global DoF를 로컬로 치환합니다. 즉 `local_position = Frame::origin + (dof.position() - anchor[s])`로 만들어 `local_dof`를 `trajectory->Append` (:136)와 `state.positions` (:146-147,:155)에 공급합니다. 속도는 변경하지 않습니다 (평행이동 불변). 인덱스는 루프 후 (:161-163)에 body 포인터 기준 매핑으로 `subsystem_of_body_`를 채웁니다 (oblate 재정렬은 :144-150).

## 3. Gravity kernel (`ComputeGravitationalAccelerationByMassiveBodyOnMassiveBodies`, static, decl `ephemeris.hpp:426`, body `ephemeris_body.hpp:1342-1410`)
Static 함수이므로 `subsystem_of_body`, `subsystem_origin_offset` 파라미터를 추가하고 호출 지점(`:1516-1548`, `:1274-1311`)에 관통시킵니다. `:1366`을 다음으로 교체합니다.
```cpp
int s1 = subsystem_of_body[b1], s2 = subsystem_of_body[b2];
Displacement<Frame> Δq;
if (s1 == s2) {
  Δq = position_of_b1 - positions[b2];             // unchanged, full precision
} else {
  DoublePrecision<Displacement<Frame>> inter = subsystem_origin_offset[s1] - subsystem_origin_offset[s2];
  Displacement<Frame> local_diff = position_of_b1 - positions[b2];
  Δq = inter.value + (inter.error + local_diff);   // cross-system 1/r² negligible; collapse safe
}
```
하류(`Δq²`, geopotential `:1386,:1399`)는 변경하지 않습니다. 동일한 split을 Jacobian (`:1193`)과 jerk 커널에도 적용해야 하며, 그렇지 않으면 energy/variational 계산이 어긋납니다 (Prolong 경로에 없다면 commit 1에서는 미룰 수 있습니다 — grep으로 검증할 것).

## 4. Trajectory storage
`AppendMassiveBodiesStateToTrajectories` (`:1101-1116`)는 이미 `.value`를 append하는데 이제 그 값이 로컬이므로 변경 불필요(UNCHANGED)입니다. ContinuousTrajectory는 로컬로 유지됩니다 (~4e16이 아닌 ~1e13에서 Chebyshev fit을 수행해 유효숫자 ~5자리를 회복). `subsystem_origin_offset(body)` accessor를 추가하고, `EvaluateAllPositions`는 기본적으로 LOCAL로 두며, 렌더링 경로 전용으로만 `EvaluateGlobalPosition`(offset 가산)을 추가합니다 — 절대 암묵적으로 globalize하지 않습니다.

## 5. Serialization
`serialization::DoublePrecision`은 이미 존재합니다 (`numerics.proto:26-44`, Multivector value). `message Ephemeris` (`physics.proto:181-210`, 마지막 tag 13)를 확장해 `repeated int32 body_subsystem = 14;` `repeated DoublePrecision subsystem_origin_offset = 15;`를 추가합니다. 비어 있으면 ⇒ 레거시 단일 subsystem ⇒ 기존 세이브가 그대로 로드됩니다. 기존 `Subsystem` message (`:231`, Kepler hierarchy — 무관)는 재사용하지 않습니다.

## 6. Validation test (`astronomy/interstellar_precision_test.cpp`, mirror `trappist_dynamics_test.cpp:985-1153`)
동일한 항성+행성 subsystem 두 벌을 두고, subsystem 1을 +4.0e16 m x̂에 배치합니다. `subsystems={0,0,1,1}`. 대조군(control) = `subsystems={}` (레거시). 100년간 Prolong합니다. 검증 조건은 다음과 같습니다. 수정 브랜치 `max_t |‖r1‖−‖r0‖| < 1 mm`, control은 `> 1 m`. 선택적 energy 검증으로 수정 후 <1e-11, control ~1e-6. 수치 근거는 ULP(4e16)=9 m, ULP(1.5e11)=3.3e-5 m, 약 2.7e5배 개선입니다.

## 7. Commit order
1. **정밀도를 headless로 증명 (파일 3개)**: 멤버 + ctor 파라미터 + kernel split + 호출 지점 + 테스트. 완전한 하위 호환.
2. Jacobian/jerk cross split.
3. Serialization + round-trip 테스트.
4. Global accessor + plugin 배선 (`plugin.cpp:128-138` InsertCelestialAbsoluteCartesian → subsystem 관통, 렌더링만 globalizing accessor 경유).
