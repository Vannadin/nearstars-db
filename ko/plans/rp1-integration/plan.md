---
title: RP-1 / RealSolarSystem compatibility integration
status: active
created: 2026-06-26
---

# RP-1 호환 통합

**NearStars와의 관계.** NearStars는 Sol-Configs(ballisticfox / RSS-Reborn 계열, `FOR[SolSystem]`) 위에 올라가 있다. 반면 RP-1(Realistic Progression One)은 RealismOverhaul + Principia + ROKerbalism 기반의 리얼리즘 커리어 모드이며, **공식적으로 Sol-Configs가 아니라 고전 `KSP-RO/RealSolarSystem`을 요구한다**. 그런데 Sol-Configs 쪽(ballisticfox)이 **자체 RP-1 호환을 준비 중**이다(업스트림에서 진행 중, 출시 대기). 따라서 NearStars는 고전 RSS 브랜치를 따로 만들지 **않는다**. 대신 **Sol 기반을 유지하면서 Sol-Configs가 내놓을 RP-1 브리지에 얹어 간다**. NearStars가 직접 책임져야 하는 **베이스 독립적인 RP-1 커리어 레이어 패치**만 추가하면 된다. 이 문서는 업스트림 모드 소스를 근거로 그 레이어들을 정리해 두어, Sol-Configs의 RP-1 호환이 도착했을 때 곧바로 쓸 수 있도록 준비해 둔 것이다.

**범위.** 대상은 **Sol V1.0 위의 RP-1뿐**이다(오너 결정 2026-06-26). 고전 RealSolarSystem 위의 RP-1(현재 표준 설치 형태)은 **명시적으로 범위 밖**이다. NearStars 바디는 `SolSystem` 게이트가 걸려 있어 고전 RSS 베이스에서는 나타나지 않으며, `:NEEDS[RealSolarSystem]` 바디 변종을 따로 만들지 않기로 했다. 포함되는 것은 NearStars가 소유하는 RP-1 커리어 레이어 패치(ResearchBodies, ROKerbalism 방사선, Principia 바디 append, RealAntennas 노트)와 그 MM 태그 / 노드 이름 / 재배치 타깃이다. **제외(폐합):** 고전 RSS용 Kopernicus 변종이나 RSS 전용 Principia 좌표 변종은 만들지 않는다. 또한 제외되는 것은 지금 당장 테스트된 cfg를 출하하는 일(emit은 프로젝트 말미로 연기), 인게임 검증(Sol V1.0 RP-1 호환 + 오너의 Windows 설치를 기다림)이다. C#/Harmony 작업은 [[project-nearstars-mod-plugins-schultz]]에 따라 슐츠 담당이다.

**외부 참조.**
- https://github.com/KSP-RO/RP-1 (커리어 모드; MM 토큰 `RP-0`)
- https://github.com/KSP-RO/RealismOverhaul (태그 `RealismOverhaul`)
- https://github.com/KSP-RO/ROKerbalism (프로파일 `RealismOverhaul` → 태그 `ProfileRealismOverhaul`)
- https://github.com/mockingbirdnest/Principia
- https://github.com/JPLRepo/ResearchBodies
- https://github.com/KSP-RO/RealAntennas
- https://github.com/RSS-Reborn/Sol-Configs (우리 베이스; RP-1 호환은 업스트림에서 계획 중)

---

## 1. 전략 (방향 전환)

핵심은 이것이다. **RP-1과 Sol-Configs는 서로 배타적인 베이스이고, RP-1 플레이어의 베이스는 결국 Sol-Configs가 RP-1 호환 버전으로 내놓는 그것이 된다. 따라서 NearStars가 고전 RSS 자체를 직접 겨냥할 필요는 전혀 없다.**

- **바디는 `FOR[SolSystem]`로 유지한다.** Sol-Configs가 RP-1 호환이 되면 NearStars 바디는 RP-1 게임에서 자동으로 로드된다(같은 Sol 베이스에 붙기 때문이다). RSS 태그도, 좌표 분기도, 이중 베이스 게이팅도 필요 없다.
- **NearStars는 베이스 독립적인 커리어 레이어만 소유한다.** 이들은 RP-1 / RO / ROKerbalism / Principia의 존재 여부로만 게이트하고 **베이스 시스템 태그로는 게이트하지 않는다**. 그래서 Sol-Configs가 RP-1 브리지를 *어떤 방식으로* 구현하든 견고하게 동작하며, 지금 미리 작성해 둘 수 있다.
- **의존성.** 최종 인게임 검증은 Sol-Configs의 RP-1 호환이 도착해야 가능하다(업스트림, 대기 중). 그동안 우리 쪽은 "준비 완료" 상태로 만들어 둔다.

| Decisive convention | Value | Source |
|----------------------|-------|--------|
| RP-1 detection tag | `RP-0` (not `RP-1`) | `:FOR[RP-0]` throughout `RP-1/GameData/RP-1/` |
| RealismOverhaul tag | `RealismOverhaul` | `:FOR[RealismOverhaul]` in RO cfgs |
| ROKerbalism profile tag | `ProfileRealismOverhaul` (profile name `RealismOverhaul`) | `ROKerbalism/.../Profiles/ROKerbalism.cfg` |
| Principia epoch | `JD2433282.5` — already our convention | Principia `astronomy/sol_initial_state_*.cfg` |
| flightGlobalsIndex | 1000+ avoids RO 0–99 — already safe | `guideline.md §7` |

---

## 2. NearStars가 소유하는 커리어 레이어 (베이스 독립적)

### WS3 — RP-1 하에서의 ResearchBodies  *(주력; 기존 rp1-compat.md 스케치를 대체)*

- **RP-1에는 관측소 메커니즘이 없다.** 스톡 TrackingStation은 DSN/통신 시설이지 천문 관측 호스트가 아니다. 발견은 **부품 기반**이다.
- RB 망원경 부품은 `TechRequired = spaceExploration`에 걸려 있는데, RP-1은 이 노드를 만들 수 없는 `orphanParts` 싱크로 흘려보낸다. **`scienceSatellite`로 재배치한다**(RP-1이 자체 `spaceExploration` 태그 필름 카메라를 두는 곳이며, 더 늦은 게이트가 필요하면 대안으로 `deepSpaceScience`). 게이트는 `:NEEDS[ResearchBodies&RP-0]`.
- RB의 `CC_RB_*` 계약은 RP-1의 정교하게 튜닝된 진행 흐름을 오염시킨다(RP-1은 서드파티 팩을 억제하지 않는다). **`:NEEDS[!RP-0]`로 출하한다** — RP-1 커리어에서는 절대 보이지 않고, 비-RP-1 설치에서는 망원경 발견 계약이 유지된다.
- RB가 넓혀 둔 `observatorylvl*range`가 선택한 TS 레벨에서 우리 거리들을 커버하는지 다시 검증한다.

### WS4 — ROKerbalism 방사선

우리 DB의 방사선/항성풍 필드는 이미 ROKerbalism의 태양 기준선(`radiation_surface = 46.5`)에 앵커되어 있으므로 모델이 RO와 정합한다.

- 바디별 방사선을 ROKerbalism의 `GameData/KerbalismConfig/System/Radiation.cfg` 스타일로 작성한다. 즉 `RadiationModel`(벨트/포즈 지오메트리) + `RadiationBody`(CelestialBody → 모델 바인딩) 구조에, 거기서 쓰는 **언더스코어** 필드 이름을 사용한다. `name`은 Kopernicus 내부 바디 이름이다. 폭풍 강도는 전역이므로 건드리지 않는다.
- 게이트는 `:NEEDS[ProfileRealismOverhaul]`. 이는 (향후) kerbalism-cfg 라이터의 RO 프로파일 출력 모드가 된다. [[project-nearstars-stellar-wind-kerbalism]] 참조.

### WS2′ — Principia (Sol 유지, RSS 변종 없음)

NearStars는 이미 `@principia_gravity_model` / `@principia_initial_state`를 통해 단일 Principia 루트에 바디 블록을 append한다(두 번째 루트를 만들면 크래시한다). RP-1-on-Sol-Configs 하에서도 동일한 Sol 패치가 그대로 적용되며 에포크도 이미 일치한다(`JD2433282.5`). **RSS 좌표 변종은 필요 없다.** 한 가지 잠복 제약이 있다. 만약 베이스가 *완전한* `principia_initial_state`를 출하한다면 Principia는 그것이 모든 바디를 포함하기를 요구하므로, NearStars는 자신의 모든 바디에 대해 데카르트 상태를 공급해야 한다(우리는 `derived.icrs_*_km`에 저장해 둔다). Keplerian 폴백에 의존해서는 안 된다.

### WS5 — RealAntennas (문서만)

하드 거리 상한은 없다. 우리의 실제 거리(~10¹³–10¹⁴ km)에서는 링크 버짓이 데이터 전송률 0으로 매끄럽게 떨어진다(안전하게 실패하고 크래시는 없다). RP-1 하에서 항성간 통신은 성립하지 않는다 — 예상된 동작이다. cfg는 없고, 한계만 문서화한다.

### WS6 — flightGlobalsIndex / RO 바디 리얼리즘 (작업 없음)

인덱스는 이미 RO의 0–99를 피한다. 바디는 실측 데이터 기반이므로 자연스럽게 RO/FAR/RealHeat와 정합한다. 패치는 예상되지 않는다.

---

## 3. NearStars에 미치는 함의

1. **Sol 기반을 유지한다.** 고전 RSS용 Kopernicus나 Principia 변종은 없다. 앞서 검토했던 이중 베이스 / RSS 좌표 워크스트림은 폐기한다.
2. **커리어 레이어를 지금 만들되, RP-0 / RealismOverhaul / ProfileRealismOverhaul / Principia로 게이트한다** — Sol-Configs의 브리지 메커니즘과 독립적이므로, 업스트림의 설계 선택이 이들을 깨뜨릴 수 없다.
3. **Emit은 프로젝트 말미로 연기한 채 둔다.** 이 문서와 스킬 업데이트로 컨벤션을 지금 canonical하게 못박는다.
4. **검증은 업스트림에 게이트된다.** 엔드투엔드 테스트 전에 Sol-Configs의 RP-1 호환이 도착해야 한다. 그때까지 우리 쪽은 "준비됨, 미검증" 상태다.
5. **업데이트할 스킬.** `researchbodies-cfg/references/rp1-compat.md`(근거 기반 재배치 + 계약 발견에 맞춰 재작성 — 현재로서는 적극적으로 틀린 상태다), 그리고 kerbalism-cfg 라이터 스펙(RO 프로파일 모드). principia-cfg와 kopernicus-cfg는 방향 전환 이후 RSS 변종 작업이 필요 없다.

---

## 4. 미해결 질문

- **[업스트림] Sol V1.0 RP-1 호환의 형태 + 타임라인.** 근거가 된 메커니즘은 이렇다. MM은 cfg가 아니라 **로드된 DLL 어셈블리 이름**에서 `:NEEDS[X]`/`:FOR[X]`를 도출한다. 고전 RSS는 `RealSolarSystem.dll`을 출하해 RP-1/RO 패치가 게이트하는 `RealSolarSystem` 태그를 등록한다. **Sol-Configs는 config 전용(DLL 없음)이라** `SolSystem`만 등록하므로, 오늘날 RP-1/RO 패치는 그 위에서 발화하지 않는다. ballisticfox(Patreon 2025-05-29)는 Sol **V1.0이 "100% RP-1 밸런스 및 호환"**이 될 것이며 "RSS와 Sol 사이를 매끄럽게 전환"하면서 RSS를 대체하리라고 선언했다(RSS-Reborn 오버레이 지원은 폐지 예정). Sol은 이미 `Patches/Sol-RP1.cfg`를 출하한다. 따라서 V1.0이 `RealSolarSystem` 태그 브리지 자체를 제공할 것으로 기대된다. 이것은 **선언되었으나 아직 출하되지 않은** 목표다. 이는 우리의 커리어 레이어 작성을 막지 않으며(우리는 `RP-0`/`RealismOverhaul`/`ProfileRealismOverhaul`/`Principia`로 게이트하고, 이들은 RP-1/RO가 로드되면 모두 존재한다), 최종 검증만 막는다. 바디 명명과 발사장도 이미 들어맞는다(Sol의 Moon 내부 `name = Moon`; Sol은 `SolSystem` 하에서 `us_cape_canaveral`을 복제한다).
- **[기존] Principia에서의 실제 거리.** 우리는 별을 실제 ~10¹³–10¹⁴ km에 emit한다. Principia가 이들을 안정적으로 적분하는지 확인한다(REBOUND 시뮬레이션 교차 검증). 이는 Sol 경로에서 물려받은 것이지 RP-1이 들여온 것이 아니다.
