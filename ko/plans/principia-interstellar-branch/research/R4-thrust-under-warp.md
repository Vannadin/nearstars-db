# R4 — timewarp 중 연속 추력

리서치 에이전트: opus + web. 소스 head 440310a9.

## 0. 요약
Principia는 실제 n-body 궤적 위에서 질량이 감소하고 방향이 제어되는 연속 추력에 필요한 물리 프리미티브를 이미 전부 갖추고 있습니다. 기계 장치는 두 벌이 존재합니다. (1) 실시간 물리 추력(loaded vessel) — 어댑터가 매 FixedUpdate마다 `part.force`를 수집 → `PileUp::AdvanceTime`이 `FlowWithAdaptiveStep`으로 history를 적분합니다(`pile_up.cpp:596-620`). (2) 계획된 유한 연소(planned finite burn) — `Manœuvre`(상수 추력 + 치올콥스키 질량 감소, `manœuvre_body.hpp:267-278`)를 `FlightPlan::BurnSegment`(`flight_plan.cpp:469-495`)가 사용합니다. **유일한 공백 = warp 아래의 이음새로, force 수집이 `!v.packed` 조건으로 게이트되어 있다는 점입니다(`ksp_plugin_adapter.cs:1797-1798`).** 그래서 warp 중에는 `intrinsic_force_`=0이 되고 AdvanceTime은 coast 분기를 타게 됩니다. warp 중에는 엔진이 가속을 전혀 만들어내지 못합니다.

## 1. 현재의 연소 처리
- `Manœuvre`(`manœuvre.hpp:38-83`): `Force thrust`, `SpecificImpulse`(추력÷mass-flow = 배기 속도), Frenet 프레임, `is_inertially_fixed`. `mass_flow=thrust/Isp`, `final_mass=m₀−ṁ·dur`. **핵심 프리미티브**는 `ComputeIntrinsicAcceleration`(`manœuvre_body.hpp:267-278`)으로, 연소 구간 안에서는 `direction·thrust/(m₀−(t−t₀)·ṁ)`, 밖에서는 0을 반환합니다 — 순간 질량을 반영한 시간 가변 가속입니다. `InertialIntrinsicAcceleration`→`Ephemeris::IntrinsicAcceleration`(시간만 인자, `:188-197`)과 `FrenetIntrinsicAcceleration`→`GeneralizedIntrinsicAcceleration`(시간+상태, `:199-210`)으로 래핑됩니다. **연소는 순간 Δv가 아니라 유한 연속 가속입니다.**
- `FlightPlan`(`flight_plan.hpp:36-269`): coast/burn 체인이며, 질량은 manœuvre들 사이에 체이닝됩니다(`flight_plan.cpp:169`). `BurnSegment`(`:469-495`)가 적분 이음새입니다(inertial vs Frenet 가속으로 FlowWithAdaptiveStep). 다만 flight-plan 궤적 위에서만 돌고 vessel history에는 절대 닿지 않습니다 — 그것이 공백입니다.
- Vessel 궤적(`vessel.hpp`): history → backstory_ → psychohistory_ → prediction_. prediction은 비동기(prognosticator `:380-381`)이고 폐기 가능하며, **연소가 실제로 수정해야 하는 경로는 history입니다.**

## 2. RHS 훅 (추력이 ODE에 들어오는 지점)
`ephemeris.hpp:72-80`: `IntrinsicAcceleration = function<Vector<Acceleration,Frame>(Instant)>`, `GeneralizedIntrinsicAcceleration = function<...(Instant, DegreesOfFreedom)>`. 주입 방식은 `FlowWithAdaptiveStep`이 `accelerations[0] += intrinsic_acceleration(t)`를 수행하고(`ephemeris_body.hpp:431-433`), generalized 버전은 `:464-467`, fixed-step 인스턴스는 벡터를 합산합니다(`:366-381`). 질량 없는 적분기 = adaptive RKN `DormandElMikkawyPrince1986RKN434FM`(`integrators.cpp:84-92`). **단일하고 깨끗한 이음새**이므로, 어떤 연소든 IntrinsicAcceleration으로 표현하면 올바르게 적분됩니다.

## 3. Timewarp 매핑
프레임마다 `Plugin::AdvanceTime`(`plugin.cpp:754-767`)이 loaded intrinsic force를 비우고 ephemeris를 Prolong하지만, vessel은 적분하지 않습니다. Vessel 따라잡기는 `CatchUpLaggingVessels`/`CatchUpVessel`(`:769-826`) → 스레드 풀에서 `PileUp::DeformAndAdvanceTime` → `vessel->AdvanceTime`이 history를 연장하는 흐름입니다. `PileUp::AdvanceTime`(`pile_up.cpp:572-638`)은 `intrinsic_force_==0`이면 coast 분기(:575), `!=0`이면 추력 분기로 HISTORY를 적분합니다(:596-620). **즉 Principia는 warp 중에도 vessel history를 적분하고 있습니다 — 다만 warp 중에는 intrinsic_force_=0이라 항상 coast일 뿐입니다.**

## 4. 있는 것 vs 없는 것
있는 것: 질량 감소를 동반한 유한 연속 추력, intrinsic-accel RHS 주입, 추력을 포함한 history 적분, 체이닝된 질량 + Frenet/inertial 방향, 실시간 추력의 history 반영. **없는 것: packed/warp 중의 추력(수집이 `!v.packed`로 게이트됨), warp 중 자원 소모 + 고갈 시 자동 warp 정지.** 공백은 "warp 중 실시간 물리 추력" vs "계획된 flight-plan 연소"의 차이입니다. 성간 순항은 수개월에 걸친 라이브 throttle을 원하므로, flight plan은 참조 구현일 뿐 전달 수단이 아닙니다.

## 5. 선행 사례와 비호환성
PersistentThrust / BackgroundProcessing / Kerbalism은 rails 위에서 스톡 `Orbit`을 직접 수정하는(UpdateFromStateVectors) 방식이라 warp 도중 throttle/자세를 바꿀 수 없습니다. **Principia와는 비호환입니다.** Principia는 managed-vessel 궤적을 소유하며 상태를 스톡 orbit으로 내보내기만 하고(`ApplyToVesselsOnRails`→`UpdateVessel` `ksp_plugin_adapter.cs:1772-1774`) 되읽지 않으므로, 다른 모드가 orbit을 고쳐도 덮어써집니다. Principia issue #2347이 네이티브 메커니즘을 요청한 상태입니다. **따라서 내부 구현이어야 합니다. 연소는 Principia history 위의 intrinsic accel로 넣고, 스톡 Orbit은 절대 건드리지 않습니다.**

## 6. 추가할 메커니즘
vessel별 **OnRailsBurn**을 두어, AdvanceTime이 이미 수행하는 history 적분에 Manœuvre 스타일 intrinsic accel을 주입합니다. 프레임마다 piecewise-constant(구간 [current_time_, t]에서 추력/Isp/방향 상수, 질량은 감소)로 처리하면 여러 프레임에 걸친 가변 throttle 유한 연소가 재현됩니다.
- **데이터**(`pile_up.hpp:196-197`): `std::optional<OnRailsBurn> on_rails_burn_` {Force thrust; SpecificImpulse isp; Vector<double,Barycentric> direction; bool is_inertially_fixed;}. 프레임 단위 inertial 방향(어댑터가 world→Barycentric XYZ를 넘김, `:1382` 참조)으로 hot path에서 Frenet을 피합니다.
- **AdvanceTime 분기**(`pile_up.cpp:572-638`): `on_rails_burn_`이 설정되어 있고 intrinsic_force_==0일 때, psychohistory를 authoritative로 만들고 `a(t)=dir·thrust/(m₀−(t−t₀)·ṁ)`(`manœuvre_body.hpp:273-274`와 공유 헬퍼)로 `FlowWithAdaptiveStep(&trajectory_, accel, t, ...)`를 수행한 뒤, `mass_`를 `(t_end−t₀)·ṁ`만큼 감소시키고(실제 도달한 t_end 사용), 건조질량 클램프를 적용합니다(`t_dry`까지 적분, burn 해제, warp-stop 신호).
- **Plugin API**(`plugin.hpp/cpp`의 `:801-826` 부근): `VesselSetOnRailsBurn(guid, thrust, isp, direction)` / `VesselClearOnRailsBurn`(CatchUpVessel처럼 pile-up 탐색), CatchUpLaggingVessels 이전에 실행합니다. C 인터페이스는 `interface_vessel.cpp`(interface_part의 force 함수들을 미러) + P/Invoke 재생성.
- **C# 어댑터**(`ksp_plugin_adapter.cs`): `:1797-1894`에 병렬 PACKED 분기를 추가합니다. 엔진 추력 + mass-flow 합산 → 질량 기준 Isp 산출, world 자세→Barycentric XYZ 변환, throttle>0이고 자원이 충분할 때 VesselSetOnRailsBurn 호출, warp 스텝만큼 **추진제/EC 소모**(`part.RequestResource`), 고갈 시 warp 정지(`TimeWarp.SetRate(0,true)`, flight_planner.cs:613 참조). feature flag로 게이트합니다.
- **Prediction**(`vessel.cpp` FlowPrognostication): 연소 구간 동안 동일한 intrinsic accel을 공급해 화면에 그려지는 궤적이 추력을 미리 반영하게 합니다.

## 7. 파일
1. `manœuvre_body.hpp:267-278` — `ThrustAcceleration(dir,thrust,m₀,ṁ,t₀,t)` 헬퍼 추출.
2. `pile_up.hpp:196-197` — OnRailsBurn + 직렬화(intrinsic_force_ 미러).
3. `pile_up.cpp:572-638` — 새 분기 + 질량 장부 + 건조질량 클램프.
4. `plugin.hpp/cpp:801-826` — Set/Clear API.
5. `interface_vessel.cpp`(+interface_part 패턴) — C 진입점 + P/Invoke.
6. `ksp_plugin_adapter.cs` — packed 수집 분기, 자원 소모, warp 정지, feature flag.
7. `vessel.cpp` FlowPrognostication — prediction 일관성.
8. `serialization/ksp_plugin.proto` PileUp — warp 도중 세이브를 위한 on-rails burn 직렬화.

## 8. 질량/Isp/제어 노트
법칙 `a=dir·thrust/(m₀−(t−t₀)ṁ)`, ṁ=thrust/Isp. Isp는 질량 기준 specific impulse(배기 속도 = 총 추력 ÷ Σ 엔진 mass-flow)이며 무게 기준 Isp가 아닙니다. `mass_`(`pile_up.hpp:196`)는 프레임마다 감소시키고 탱크는 C#에서 소모하며, unpack 시 KSP part 질량이 다시 권위를 갖습니다(`InsertOrKeepLoadedPart :1354`). throttle과 방향을 매 프레임 다시 읽으므로 warp 중에도 완전한 라이브 제어가 됩니다(PersistentThrust 대비 우위). MVP는 inertial 고정 방향(시간 전용 오버로드)으로 하고, Frenet 고정은 이후에 추가합니다(generalized RHS `:464-467`). 스톡 Orbit은 절대 쓰지 않습니다.

출처: PersistentThrust (SpaceDock 2450, bld/PersistentThrust GitHub), Persistent Thrust Extended (KSP forums), Principia issue #2347.
