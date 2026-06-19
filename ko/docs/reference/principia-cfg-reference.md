# Principia CFG 기술 참조

> 출처: mockingbirdnest/Principia GitHub 저장소, 위키, `astronomy/*.cfg` 파일  
> 목적: KSP 행성 팩용 Principia 호환 CFG 파일 생성을 위한 참조 문서

> **관점.** 이 문서는 **외부 Principia CFG API 레퍼런스** 입니다 — Principia 가 받아들이는 노드/키의 전체 집합과 그 의미를 상위 코드와 문서로부터 정리한 것. 특정 행성 팩과 독립적입니다.
>
> **NearStars 고유 구현** — 실제로 emit 하는 노드 부분집합, `db/systems/*.json` 필드 → CFG 값 매핑, 지원 변형 (Sol Real / Sol Quarter / RSS), Principia 패치에서 `:NEEDS:FOR[NearStarsSystem]` 컨벤션을 벗어난 이유 — 는 [`principia-cfg` 스킬](../../../.claude/skills/principia-cfg/SKILL.md) 참고.

---

## 개요

Principia는 KSP의 패치드-코닉(영향권) 중력을 완전한 N체 물리학으로 대체합니다. KSP의 GameDatabase에서 설정을 읽으며(Kopernicus와 동일한 시스템), `GameDatabase.Instance.GetAtMostOneNode(name)`를 통해 Config 노드를 탐색합니다. ModuleManager 머지가 적용되며, 모든 패치 처리 이후 각 최상위 노드는 **최대 하나**만 존재해야 합니다.

---

## 최상위 CFG 노드

| 노드 이름 | 목적 |
|---|---|
| `principia_gravity_model` | 물리적 속성 (질량, 자전, 지오퍼텐셜) |
| `principia_initial_state` | 기준 에포크에서의 직교 좌표 위치 및 속도 |
| `principia_numerics_blueprint` | 수치 적분기 설정 |
| `principia_draw_styles` | 궤적 시각화 색상 및 선 스타일 |
| `principia_override_version_check` | KSP 버전 불일치 치명적 오류 억제 |

**규칙**: ModuleManager 처리 이후 각 노드는 **최대 하나**만 존재할 수 있습니다. `principia_gravity_model` 루트가 두 개이면 충돌합니다.

---

## `principia_gravity_model`

정확한 자전 및 중력 매개변수를 제공합니다. Principia가 `CelestialBody` 필드에서 파생할 값들을 덮어씁니다. 선택 사항이며, 없을 경우 KSP의 `gravParameter`, `angularV`, `initialRotation`으로 폴백합니다.

### 구조

```cfg
principia_gravity_model[:NEEDS[SomeMod]] {
  body { ... }
  body { ... }
}
```

애드온에서 패치하려면.

```cfg
@principia_gravity_model:NEEDS[OPM] {
  body { ... }
}
```

### `body` 노드 키

| 키 | 타입 | 필수 여부 | 비고 |
|---|---|---|---|
| `name` | string | Yes | `displayName`이 아닌 `CelestialBody.name` (Kopernicus `Body { name = X }`)과 일치해야 합니다 |
| `gravitational_parameter` | quantity (m³/s²) | 조건부* | μ = GM. `principia_initial_state`가 존재할 경우 필수 |
| `reference_instant` | instant | No | 자전 기준 에포크. 기본값: `JD2451545.000000000` (J2000) |
| `axis_right_ascension` | quantity (angle) | No | 북극의 ICRF 적경. 기본값: `-90 deg` |
| `axis_declination` | quantity (angle) | No | 북극의 ICRF 적위. 기본값: `90 deg` |
| `reference_angle` | quantity (angle) | No | `reference_instant` 시점의 본초 자오선 각도 W₀. 기본값: KSP의 `initialRotation` |
| `angular_frequency` | quantity (angle/time) | No | 항성 자전 속도. 기본값: KSP의 `angularV` |
| `reference_radius` | quantity (length) | 조건부 | `j2` 또는 `geopotential_row`가 존재할 경우 필수 |
| `j2` | float | No | 비정규화된 J₂ 대역 조화함수. `geopotential_row`와 상호 배타적 |
| `geopotential_row` | sub-node (반복) | No | 완전한 구면 조화함수 지오퍼텐셜. `j2`와 상호 배타적 |

*`principia_initial_state`가 존재할 경우 `gravitational_parameter`는 필수입니다.

**자전 모델 규약**: IAU 2009 WG on Cartographic Coordinates를 따릅니다. 기본값 `-90 deg` / `90 deg`는 극을 KSP 내부 프레임에 맞춥니다.

### J2 예시

```cfg
body {
  name                    = Sun
  gravitational_parameter = 1.3271244004193938e+11 km^3/s^2
  reference_instant       = JD2451545.000000000
  axis_right_ascension    = 286.13 deg
  axis_declination        = 63.87 deg
  reference_angle         = 84.176 deg
  angular_frequency       = 14.1844000 deg / d
  reference_radius        = 696000.0 km
  j2                      = 2.11060885327268404e-07
}
```

### 지오퍼텐셜 예시

```cfg
body {
  name             = Earth
  reference_radius = 6378.1363 km
  geopotential_row {
    degree = 2
    geopotential_column {
      order = 0
      cos   = -4.84169457320000017e-04
      sin   = 0.0
    }
    geopotential_column {
      order = 2
      cos   = 2.43937341593980011e-06
      sin   = -1.40029401183640008e-06
    }
  }
}
```

---

## `principia_initial_state`

관성 좌표계에서 모든 천체의 직교 초기 조건을 제공합니다. **없을 경우**, Principia는 KSP의 케플러 궤도 요소(야코비 좌표)에서 초기 상태를 파생합니다. **있을 경우**, 이 노드와 `principia_gravity_model` 모두 필수이며 모든 천체를 포함해야 합니다.

### 구조

```cfg
principia_initial_state[:NEEDS[RealSolarSystem]] {
  game_epoch         = JD2433647.5
  solar_system_epoch = JD2433282.500000000
  body { ... }
  body { ... }
}
```

### 최상위 필드

| 키 | 타입 | 비고 |
|---|---|---|
| `game_epoch` | instant | KSP Universal Time 0이 매핑되는 실제 시각 (인게임 시작 날짜) |
| `solar_system_epoch` | instant | 상태 벡터가 유효한 에포크. `game_epoch` 이하여야 합니다. Principia는 이 시점부터 순방향으로 적분합니다. |

**에포크 참고**: `solar_system_epoch`는 JPL 데이터 기준 에포크이고, `game_epoch`는 RSS/Sol 게임 시작 날짜입니다. Principia는 로드 시 그 간격을 사전 적분합니다.

### `body` 노드 키

| 키 | 타입 | 필수 여부 | 비고 |
|---|---|---|---|
| `name` | string | Yes | KSP 천체 이름과 일치해야 합니다 |
| `x`, `y`, `z` | quantity (length) | Yes | 중심 관성 프레임에서의 위치 |
| `vx`, `vy`, `vz` | quantity (length/time) | Yes | 중심 관성 프레임에서의 속도 |

**좌표 프레임**: 태양계 질량 중심이 원점인 중심 관성 프레임이며, 축은 Unity 월드 프레임과 정렬됩니다.

### 예시

```cfg
principia_initial_state:NEEDS[RealSolarSystem] {
  game_epoch         = JD2433647.5
  solar_system_epoch = JD2433282.500000000
  body {
    name = Earth
    x    = -2.720318042296709e+07 km
    y    = +1.329407956490104e+08 km
    z    = +5.764165538717468e+07 km
    vx   = -2.975363625990147e+01 km/s
    vy   = -5.189341029926219e+00 km/s
    vz   = -2.251484908750744e+00 km/s
  }
}
```

---

## `principia_numerics_blueprint`

수치 적분 알고리즘을 제어합니다. 선택 사항이며, 없을 경우 Principia는 컴파일된 기본값을 사용합니다.

### 구조

```cfg
principia_numerics_blueprint {
  downsampling {
    tolerance = 10 m
  }
  ephemeris {
    fixed_step_size_integrator = QUINLAN_TREMAINE_1990_ORDER_12
    integration_step_size      = 10 min
    fitting_tolerance          = 1 mm
    geopotential_tolerance     = 0x1.0p-24
  }
  history {
    fixed_step_size_integrator = QUINLAN_1999_ORDER_8A
    integration_step_size      = 10 s
  }
  psychohistory {
    adaptive_step_size_integrator = DORMAND_ELMIKKAWY_PRINCE_1986_RKN_434FM
    length_integration_tolerance  = 1 mm
    speed_integration_tolerance   = 1 mm/s
  }
}
```

### 하위 노드

- **`downsampling`**: `tolerance` (length) — 궤적 다운샘플링의 최대 위치 오차
- **`ephemeris`**: 배경 천체 적분
  - `fixed_step_size_integrator` — 적분기 이름 (아래 참조)
  - `integration_step_size` — 스텝 크기 (RSS/Sol 표준: `10 min`)
  - `fitting_tolerance` — 다항식 피팅 정확도
  - `geopotential_tolerance` — 조화함수 제거 임계값 (예: `0x1.0p-24`)
- **`history`**: 비행체 과거 궤적 적분기
- **`psychohistory`**: 비행체 미래/예측 적분기 (가변 스텝)

### 지원 적분기

**Symmetric Linear Multistep (에페메리스에 권장).**
- `QUINLAN_TREMAINE_1990_ORDER_8/10/12/14`
- `QUINLAN_1999_ORDER_8A` / `QUINLAN_1999_ORDER_8B`

**Symplectic Runge-Kutta-Nyström (SRKN).**
- `BLANES_MOAN_2002_SRKN_6B` / `_11B` / `_14A`

**Symplectic Partitioned Runge-Kutta (SPRK).**
- `MCLACHLAN_1995_SB3A_4` / `_5`
- `MCLACHLAN_ATELA_1992_ORDER_4_OPTIMAL` / `ORDER_5_OPTIMAL`
- `OKUNBOR_SKEEL_1994_ORDER_6_METHOD_13`

**Adaptive (psychohistory 전용).**
- `DORMAND_ELMIKKAWY_PRINCE_1986_RKN_434FM`

---

## `principia_draw_styles`

```cfg
principia_draw_styles {
  history           { colour = #aa0000  style = solid  }
  prediction        { colour = #00ff00  style = dashed }
  flight_plan       { colour = #0000ff  style = faded  }
  burn              { colour = #ffff00  style = solid  }
  target_history    { colour = #ff8800  style = dashed }
  target_prediction { colour = #ff00ff  style = faded  }
}
```

- `colour`: HTML RGB 16진수 (`#rrggbb`)
- `style`: `solid`, `dashed`, 또는 `faded`

---

## `principia_override_version_check`

```cfg
principia_override_version_check {
  version = 1.12.5
  version = 1.12.4
}
```

KSP 버전 불일치 치명적 충돌을 로그 경고로 대체합니다. 여러 `version` 값을 허용합니다.

---

## 타입 참조

### `quantity`

형식: `<number> <unit>` — 숫자는 `strtod` 구문을 사용합니다 (과학적 표기법 지원).

예시: `3.986004e+14 m^3/s^2`, `-2.975 km/s`, `14.1844 deg / d`, `10 min`, `1 mm`, `0.5 au`

**ModuleManager 수식 연산자 (`*=`, `+=`)는 quantity 값에 동작하지 않습니다.** 항상 완전히 계산된 값을 제공하십시오.

| 차원 | 지원 단위 |
|---|---|
| Length | `μm`, `mm`, `cm`, `m`, `km`, `au` |
| Time | `ms`, `s`, `min`, `h`, `d` |
| Angle | `deg`, `°`, `rad` |
| Compound | `km^3/s^2`, `deg / d`, `km/s`, `m^3/s^2`, `m s^-1` |

### `instant` (지구시)

| 형식 | 예시 |
|---|---|
| Julian Date | `JD2451545.000000000` |
| Modified Julian Date | `MJD51544.5` |
| ISO 8601 (TT) | `2000-01-01T12:00:00` |

J2000 = `JD2451545.0` = `2000-01-01T12:00:00` TT.

---

## Kopernicus 연동

### 천체 탐색

Principia는 `FlightGlobals.Bodies`(Kopernicus가 채움)에서 천체를 탐색합니다. Kopernicus `Body {}` 노드를 직접 읽지는 않습니다. `body { name = X }`의 `name`은 `displayName`이 아닌 `CelestialBody.name` (= Kopernicus `Body { name = X }`)과 일치해야 합니다.

### 두 가지 초기화 경로

**경로 1 — 직교 좌표 (`principia_initial_state` 있음).**
- 각 천체에 `InsertCelestialAbsoluteCartesian()`을 사용합니다
- `principia_initial_state`와 `principia_gravity_model` 모두 필수
- `FlightGlobals.Bodies`의 모든 천체가 두 노드에 항목을 가져야 합니다
- 모든 `body`에 `gravitational_parameter`가 필수
- Kopernicus 케플러 요소는 무시됩니다
- 적용 모드: Sol-Configs, RealSolarSystem

**경로 2 — 케플러 폴백 (`principia_initial_state` 없음).**
- 각 천체에 `InsertCelestialJacobiKeplerian()`을 사용합니다
- KSP/Kopernicus 궤도 요소를 접촉 요소(야코비 좌표)로 사용합니다
- `principia_gravity_model`은 선택 사항이며 `CelestialBody` 데이터를 보완합니다
- `gravitational_parameter`는 선택 사항 (기본값: `body.gravParameter`)
- 적용 모드: stock KSP, 가상 행성 팩

### Stock KSP Jool 시스템 안정화

`principia_initial_state` 없이 케플러 모드에서 Principia는 자동으로 `StabilizeKSP()`를 적용합니다.
- Vall과 Tylo의 평균 운동이 Laythe와의 1:2:4 공명에서 벗어나도록 조정됩니다
- Bop의 궤도가 역행으로 반전됩니다

코드에서 적용되며, CFG에서는 적용되지 않습니다. `principia_initial_state`가 있을 때는 적용되지 않습니다.

### 조석 고정

Principia는 모든 천체에 강제로 `body.tidallyLocked = false`를 설정합니다. 조석 고정 천체는 `principia_gravity_model`에서 `angular_frequency`를 궤도 주기에 맞게 설정해야 합니다.

---

## 실용 패턴

### 패턴 1: 가상 행성 팩 (케플러 모드)

`principia_gravity_model`만 필요합니다. `principia_initial_state`는 없습니다. Principia가 Kopernicus 궤도에서 위치를 파생합니다.

```cfg
principia_gravity_model:NEEDS[MyPack] {
  body {
    name                    = MyStar
    gravitational_parameter = 1.8e+18 m^3/s^2
    axis_right_ascension    = -90 deg
    axis_declination        = 89.5 deg
    reference_angle         = 0 deg
    angular_frequency       = 2.1e-05 rad/s
  }
  body {
    name                    = MyPlanet
    gravitational_parameter = 4.5e+12 m^3/s^2
    axis_right_ascension    = -90 deg
    axis_declination        = 75.0 deg
  }
}
```

### 패턴 2: 기존 gravity model 패치

```cfg
@principia_gravity_model:FOR[MyPack]:NEEDS[MyPack] {
  body {
    name                    = NewMoon
    gravitational_parameter = 8.5e+10 m^3/s^2
    axis_right_ascension    = 120 deg
    axis_declination        = -15.0 deg
  }
}
```

### 패턴 3: NearStars — Sol-Configs + RSS 이중 지원

NearStars는 Sol-Configs(ballisticfox) 위에서 실행됩니다. RSS 호환은 향후 목표이며, Sol Real 과 RSS 가 동일한 `solar_system_epoch` 및 `game_epoch` 을 공유하므로 동일한 직교 좌표 상태 벡터가 양쪽에 그대로 사용 가능합니다. Sol-Configs (및 향후 RSS) 가 자체 `principia_gravity_model` 과 `principia_initial_state` 를 포함하므로 NearStars 는 자체 천체만 패치합니다.

**에포크 참조.**

| 변형 | `solar_system_epoch` | `game_epoch` | NEEDS 태그 |
|---|---|---|---|
| Sol real scale | JD2433282.5 (1950-Jan-01) | JD2433647.5 (1951-Jan-01) | `SolSystem,!SolQuarterScale` |
| Sol quarter scale | JD2433465.0 | — | `SolSystem,SolQuarterScale` |
| RSS | JD2433282.5 (1950-Jan-01) | JD2433647.5 (1951-Jan-01) | `RSSConfig` |

Sol real-scale과 RSS는 동일한 에포크를 공유하므로 직교 좌표도 동일하게 사용할 수 있습니다.
Sol quarter-scale은 `solar_system_epoch`가 다르므로 별도의 좌표가 필요합니다.

**gravity_model**: 중력 매개변수는 스케일과 무관하므로 태양계 모드당 하나의 패치 (총 2개).
**initial_state**: 스케일별로 에포크가 다르므로 총 3개의 패치.

```cfg
// gravity model — Sol (all scales)
@principia_gravity_model:NEEDS[NearStarsSystem,SolSystem] {
  body { name = AlphaCentauriA  gravitational_parameter = ...  axis_right_ascension = ...  axis_declination = ... }
  // ... all NearStars bodies
}

// gravity model — RSS
@principia_gravity_model:NEEDS[NearStarsSystem,RSSConfig] {
  body { name = AlphaCentauriA  gravitational_parameter = ...  axis_right_ascension = ...  axis_declination = ... }
  // ... all NearStars bodies (same values — duplication unavoidable with MM)
}

// initial state — Sol real scale (solar_system_epoch = JD2433282.5)
@principia_initial_state:NEEDS[NearStarsSystem,SolSystem,!SolQuarterScale] {
  body { name = AlphaCentauriA  x = ...  y = ...  z = ...  vx = ...  vy = ...  vz = ... }
  // ... all NearStars bodies
}

// initial state — RSS (solar_system_epoch = JD2433282.5, same coords as Sol real)
@principia_initial_state:NEEDS[NearStarsSystem,RSSConfig] {
  body { name = AlphaCentauriA  x = ...  y = ...  z = ...  vx = ...  vy = ...  vz = ... }
  // ... all NearStars bodies
}

// initial state — Sol quarter scale (solar_system_epoch = JD2433465.0, different coords)
@principia_initial_state:NEEDS[NearStarsSystem,SolSystem,SolQuarterScale] {
  body { name = AlphaCentauriA  x = ...  y = ...  z = ...  vx = ...  vy = ...  vz = ... }
  // ... all NearStars bodies
}
```

**좌표 값**: `x/y/z`는 Sol 중심에서의 물리적 거리 (파섹 → km). `vx/vy/vz`는 중심 프레임에서의 고유 운동 + 시선 속도 (km/s). 항성 거리에서는 Sol 시스템에 대한 중력 영향이 무시할 수 있는 수준이므로, 항목은 오직 Principia의 일관성 검사를 통과하기 위해 존재합니다.

---

## 핵심 제약 사항

1. ModuleManager 처리 후 각 최상위 노드는 최대 하나만 존재할 수 있습니다.
2. `principia_initial_state`가 있으면 `principia_gravity_model`은 필수이며 `FlightGlobals.Bodies`의 모든 천체를 포함해야 합니다.
3. `principia_initial_state`가 있으면 `principia_gravity_model`의 모든 `body`에 `gravitational_parameter`가 필수입니다.
4. `j2`와 `geopotential_row`는 동일 천체에서 상호 배타적입니다.
5. `j2` 또는 `geopotential_row`가 있을 경우에만 `reference_radius`가 필수입니다.
6. ModuleManager 수식 연산자 (`*=`, `+=`)는 `quantity` 값에 동작하지 않습니다.
7. 천체 `name`은 `displayName`이 아닌 `CelestialBody.name`과 일치해야 합니다.
8. `solar_system_epoch` ≤ `game_epoch`.

---

## IAU 명목 단위 상수

Principia의 TRAPPIST 설정에서 단위 약어로 사용됩니다.

| 기호 | 값 |
|---|---|
| `GM☉` | 1.327124400419394e+20 m³/s² |
| `GM🜨` | 3.986004e+14 m³/s² |

---

## 제공 파일 위치 (Principia 저장소)

| 소스 경로 | 로드 시점 |
|---|---|
| `astronomy/sol_gravity_model.cfg` | `:NEEDS[RealSolarSystem]` |
| `astronomy/sol_initial_state_jd_2433282_500000000.cfg` | `:NEEDS[RealSolarSystem]` |
| `astronomy/sol_numerics_blueprint.cfg` | `:NEEDS[RealSolarSystem]` |

Sol-Configs는 `:FOR[SolSystem]`으로 자체 `Real_Sol-GravityModel.cfg`, `Real_Sol-InitialState.cfg`, `Quarter_Sol-GravityModel.cfg`, `Quarter_Sol-InitialState.cfg`를 제공합니다.

## Related

- [principia-geopotential-data](principia-geopotential-data.md) — Principia 가 천체별로 싣고 있는 **실제 지오포텐셜 값**(태양·거대행성·지구/화성/달)을 verbatim 으로, proto↔cfg 매핑 + Polyphemus 같은 가스자이언트 작성법까지.
- [methodology](methodology.md) — Principia 의 gravitational_parameter, mass, radius 에 공급되는 DB 측 스키마.
- [binary-epoch-pipeline](binary-epoch-pipeline.md) — 해당 문서 §9–11 이 만들어 내는 Cartesian 상태 벡터가 여기 `principia_initial_state` 의 body 블록에 공급됩니다.
- [mod-reference](mod-reference.md) — Principia 설치와 의존성 티어.
- [mod-release-layout](mod-release-layout.md) — §2.1 이 Principia 패치를 `Patches/Principia/` 에 어떻게 배치하는지 다룹니다.
- [alpha-centauri-a](../phase3/alpha-centauri-a.md), [alpha-centauri-b](../phase3/alpha-centauri-b.md) — Principia 의 body 별 gravity 모델 다운스트림의 정전 워크드 예시.
