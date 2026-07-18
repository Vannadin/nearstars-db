# WS3 어댑터 인수인계 — timewarp 중 추력, C# 쪽 (Windows/Opus 세션)

상태. C++ 코어는 DONE이고 Mac에서 게이트-테스트됐다(브랜치 `nearstars-interstellar`.
커밋 해시는 Principia 클론의 `.nearstars/context-notes.md` 참조). 이 파일은 남은
`ksp_plugin_adapter`(C#) 작업을 명세한다. 코딩 전에 `research/R4-thrust-under-warp.md`
(특히 §6과 §9 부록 — 설계 결정, 검증된 API, 인용)를 읽어라.

## C++ 코어가 이미 제공하는 것

- `PileUp` on-rails burn. 일정 추력 / 비추력(질량별) / 게임이 공급한 초기 질량 /
  관성 고정 방향 / 최대 지속시간을, catch-up 적분이 within-step 질량 소모의 Tsiolkovsky와
  추진제 창이 끝날 때의 정확한 mid-step cutoff로 적용한다. 이 burn은 **ONE-SHOT**이다.
  모든 catch-up이 소비한다(할 일이 없는 catch-up이든, 진짜 intrinsic force가 우선하는
  catch-up이든). 어댑터는 엔진이 타는 매 catch-up 전에 그것을 다시 설정해야 한다.
- 예측은 마지막 catch-up이 적용한 burn을 예상한다(자기-유지 사본. burn 없는 catch-up은
  그것을 지운다).
- C ABI(Windows에서도 generator가 돌면 이미 `interface.generated.cs`에 있음).
  ```csharp
  void plugin.VesselSetOnRailsBurn(string vessel_guid,
                                   double thrust_in_kilonewtons,
                                   double specific_impulse_in_seconds_g0,  // Isp by WEIGHT, s
                                   double initial_mass_in_tonnes,  // CURRENT vessel mass
                                   XYZ direction,          // World axes; need not be unit
                                   double max_duration);   // s of propellant available
  void plugin.VesselClearOnRailsBurn(string vessel_guid);
  ```
  C++ 쪽이 s·g₀ → 배기 속도, World → Barycentric(회전만) 변환을 하고, 방향을 정규화하며,
  pile up을 찾는다(없으면 경고와 함께 no-op). **어댑터가 질량 부기를 소유한다**(리뷰 발견,
  2026-07-03). 파트 질량은 packed인 동안 C++ 쪽에서 stale하므로, 매 프레임 참된 현재 선체
  질량을 넘겨라 — Σ(part.mass + part.GetResourceMass())가 RequestResource 소모를 즉시
  반영한다. 퇴화 파라미터(비양수/비유한 추력, Isp, 질량, 지속시간, 또는 0 방향)는
  ClearVesselOnRailsBurn으로 취급된다 — 그것들이 에러를 낼 거라 기대하지 마라.

## 어댑터 작업 항목 (MVP = packed ACTIVE 선체. feature-flag 게이트)

1. **Packed harvest 분기**를 `!v.packed` force census와 나란히
   (`ksp_plugin_adapter.cs` ~1797-1894). 활성 선체가 warp 하에서 packed이고, throttle > 0이며
   GATE(항목 3)를 통과하면 다음을 계산한다.
   - 총 추력(kN) = 현재 throttle에서 엔진 `finalThrust`-등가의 합(점화·작동 중인 엔진.
     `thrustTransforms` 합 의미론 사용),
   - Isp by mass → 초-g₀로 넘김(교환 단위). 총 추력 ÷ Σ(thrustᵢ/Ispᵢ),
   - 방향. World에서 명령된 축(항목 5 참조),
   - `max_duration` = 관여 추진제 전체에 대한 (가용량 ÷ 초당 소모)의 최솟값, 즉 자원-제한 burn
     시간,
   그리고 그 프레임의 catch-up 호출 전에 `VesselSetOnRailsBurn`을 호출한다.
2. **자원 소모.** 그런 매 프레임, 추진제별로
   `ṁᵢ/ρᵢ · TimeWarp.fixedDeltaTime`(이미 warp-확장됨)을 `part.RequestResource`로 소모하고
   (packed인 동안 작동 — 검증됨, R4 §9), 컨트롤 조건용 EC도. unpacked일 때의 이중-소모를
   방지하라. packed 분기에서만 소모한다(unpacked는 stock이 처리. cf. PersistentThrust의
   `simulate`-플래그 반전, PersistentEngine.cs:1181 @sswelm 8f2fbb4).
3. **GATE, 매 warp 프레임**(모든 API가 packed-valid. R4 §9).
   - 순 추력 토크 Σ (rᵢ − CoM) × Fᵢ, 엔진 `thrustTransforms` 전반에서(RCS Build Aid
     알고리즘. MechJeb2 VesselState.cs가 flight-time 레퍼런스),
   - 자세-제어 권능. ModuleGimbal / ModuleReactionWheel / ModuleControlSurface 전반에서
     Σ `ITorqueProvider.GetPotentialTorque(out pos, out neg)`, 축별 envelope,
   - 조건. |순 토크| ≤ 권능 × 마진(마진 TBD, 0.5로 시작), AND EC 존재.
4. **위반 / 고갈 반응.** burn을 끊고(`VesselClearOnRailsBurn` — 또는 그냥 다시 설정하지
   않음), LATCHED 화면 메시지를 띄우고(넘김당 한 번, Kerbalism `SupplyData.message` 패턴)
   warp를 멈춘다.
   `TimeWarp.fetch.CancelAutoWarp(); TimeWarp.SetRate(0, true);`
   (KAC + PersistentThrust 프로덕션 패턴). C++는 어쨌든 추진제 고갈에서 정확히 mid-step으로
   추력을 끊으므로, 어댑터가 한 프레임 늦게 반응해도 물리는 안전하다.
5. **방향 소스**(MVP). hold-current-attitude(이 프레임의 World에서의 엔진 축), 더하기
   prograde/retrograde/target-relative 모드용 어댑터-계산 관성 벡터 — 전부 프레임별 World
   벡터로 환원됨. C++ 변경 없음. 진짜 Frenet-following 모드는 후일의 C++ 확장이다(일반화된
   RHS. R4 §8).
6. **Feature flag.** 전체 분기를 Principia 설정 플래그 뒤로 게이트(인게임 검증 전까지 기본
   off).
7. **인게임 스모크 테스트**(Mac이 못 하는 부분). stock 계, 프로브 + 이온/화학 스테이지,
   100×–10⁶× warp에서 burn. trajectory가 휘고, 탱크가 소모되고, 고갈 시 warp가 멈추고,
   예측이 burn을 보여주고, burn 중 save/load가 깔끔히 이어지고, burn 중 unpack될 때 선체가
   제대로 거동하는지 검증(KSP가 파트 질량을 재확언하고, stock이 추력을 넘겨받음).

## Phase 2 (명시적으로 MVP 밖) — 언로드 백그라운드 burn

밑바닥부터의 백그라운드 패스가 필요하다(stock은 언로드 선체에 대해 아무것도 시뮬레이션하지
않음). `protoPartSnapshots`를 열거하고, `moduleValues` ConfigNode에서 엔진 상태를 읽고,
`ProtoPartResourceSnapshot.amount`를 직접 쓴다. tick당 가장 stale한 선체 하나 + clamp
(Kerbalism 스케줄러 규율, Unlicense. PersistentThrust `BackgroundProcessing/`가 유일한 엔진
선행 기법 — `Helpers/DetectPrincipia.cs`도 함께 배포하니 interop 기대를 위해 읽어라). 오너
요건. 백그라운드 선체의 게이트 위반도 warp를 멈춰야 한다(Kerbalism의 Message.Post choke-point
패턴).

## Kerbalism 입장

의존 없음 — 위의 전부는 stock-API 전용이다. Kerbalism이 설치돼 있으면 자체 EC 알람이 무해하게
공존한다(같은 stock TimeWarp API). 검출을 Kerbalism에 기대지 마라. 우리 어댑터가 burn-조건
모니터링을 소유한다.
