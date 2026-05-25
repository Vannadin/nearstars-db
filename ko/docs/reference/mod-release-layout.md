# NearStars 모드 릴리즈 저장소 레이아웃

> 2026-05-20 에 `guideline.md §4–6` 에서 분리되었습니다. 이 파일은 모드 릴리즈 저장소(`NearStars-Configs/` + `NearStars-Textures/`)를 다루며, 이 파일이 들어있는 `nearstars-db` 데이터 엔진 저장소와는 **별개**입니다. 모드 릴리즈 저장소는 아직 독립 Git 저장소로 분리되지 않았습니다. 아래 레이아웃은 분리 시점의 목표 구조입니다.

---

## 1. 저장소 구조

Sol-Configs 레이아웃을 따릅니다. `Patches/` 폴더는 모드별 호환성 설정 파일을 담도록 확장됩니다.

```
NearStars/
├── NearStars-Configs/
│   ├── Configs/
│   │   ├── 00_NearStars-Localization.cfg
│   │   ├── 01_[SystemName]/
│   │   │   ├── 01_[StarName]/
│   │   │   │   ├── [Star]-Kopernicus.cfg
│   │   │   │   ├── [Star]-Localization.cfg
│   │   │   │   └── [Star]-ScienceDefs.cfg
│   │   │   └── 01-01_[PlanetName]/
│   │   │       ├── [Planet]-Kopernicus.cfg
│   │   │       ├── [Planet]-Localization.cfg
│   │   │       ├── [Planet]-ScienceDefs.cfg
│   │   │       ├── [Planet]-ParallaxTerrain.cfg
│   │   │       └── [Planet]-ParallaxScatters.cfg
│   │   └── 02_[SystemName]/
│   │       └── ...
│   ├── Patches/
│   │   ├── Sol/                   // Sol 전용 오버라이드 (NEEDS[SolSystem])
│   │   └── RSS/                   // RSS 전용 오버라이드 (NEEDS[RSSConfig])
│   ├── Rescale/
│   │   ├── NearStars-Rescale-Quarter.cfg   // Sol 1/4 스케일
│   │   ├── NearStars-Rescale-Stock.cfg     // Sol 기본 스케일
│   │   └── NearStars-Rescale-RSS.cfg       // RSS 1:1 실제 스케일
│   ├── NearStars-Configuration.cfg
│   ├── NearStars-KopernicusSettings.cfg
│   └── Credits-License.md
└── NearStars-Textures/
    └── PluginData/
        └── 01_[SystemName]/
            └── 01_[BodyName]/
                └── Kopernicus/
                    ├── [Body]_Icon.png
                    ├── [Body]_VertexHeight.dds
                    ├── [Body]_VertexColor.dds
                    └── [Body]_Biomes.dds
```

---

## 2. 설정 파일 컨벤션

### 2.1 패치 태그와 이중 호환 전략

> 상태. Sol 전용이 현재 MVP. 아래 RSS 측 패치는 향후 목표 구조로서 문서화한 것이며, 현재 릴리스에는 포함되지 않습니다.
>
> 예외. Principia 패치 (`@principia_gravity_model`, `@principia_initial_state`) 는 아래 `:NEEDS:FOR[NearStarsSystem]` 형식에서 의도적으로 벗어납니다 — 그 이유는 [`principia-cfg` 스킬](../../../.claude/skills/principia-cfg/SKILL.md) 참고 (Sol-Configs 가 이미 만든 노드를 편집하기 때문에 `:FOR[NearStarsSystem]` 이 작성자임을 잘못 주장하게 됨).

RSS와 Sol 모두 중심별을 `name = Sun`으로 정의하므로, `referenceBody = Sun`은 수정 없이 양쪽에서 동작합니다. 호환성 분기는 두 곳에서만 발생합니다.

**A. 메인 천체 정의** — 중립 태그를 사용하며, 어떤 태양계 모드가 설치되어 있든 로드됩니다.

```cfg
@Kopernicus:FOR[NearStarsSystem]
{
    Body
    {
        name = StarName
        referenceBody = Sun     // Sol과 RSS 양쪽에서 유효
        ...
    }
}
```

**B. 모드별 패치** — `Patches/Sol/` 또는 `Patches/RSS/`에 배치되며 조건부로 로드됩니다.

```cfg
// Patches/Sol/StarName-EVE.cfg  — Sol이 설치된 경우에만 로드
@EVE_CLOUDS:NEEDS[SolSystem]:FOR[NearStarsSystem]
{
    ...
}

// Patches/RSS/StarName-EVE.cfg  — RSS가 설치된 경우에만 로드
@EVE_CLOUDS:NEEDS[RSSConfig]:FOR[NearStarsSystem]
{
    ...
}
```

**패치와 메인 설정 파일에 들어가는 내용.**

| 항목 | 메인 설정 파일 | Sol 패치 | RSS 패치 |
|------|-------------|---------|---------|
| 천체 정의, 궤도, PQS | 예 | — | — |
| EVE 구름 설정 | — | 예 (V5) | 예 (V3/V5) |
| Scatterer 대기 | — | 예 | 예 |
| 스케일 의존 궤도 값 | — | 필요 시 | 필요 시 |
| Principia 중력 모델 | — | 예 | 예 |

### 2.2 천체 식별자

Sol 패턴을 따릅니다. `identifier = NearStars/BodyName`

### 2.3 최소 별 정의

```cfg
@Kopernicus:FOR[NearStarsSystem]
{
    Body
    {
        name = StarName
        identifier = NearStars/StarName
        flightGlobalsIndex = 1001   // Sol-Configs 인덱스와 충돌하지 않아야 함

        Orbit
        {
            referenceBody = Sun
            semiMajorAxis = ...     // 실제 천문 데이터 기반
            eccentricity = ...
            inclination = ...
            iconTexture = NearStars-Textures/PluginData/.../Icon.png
        }

        Properties
        {
            displayName = #NearStars_StarName_name
            description = #NearStars_StarName_desc
            radius = ...
            gravParameter = ...
            rotationPeriod = ...
            ScienceValues { ... }
        }

        ScaledVersion
        {
            type = Star
            ...
        }
    }
}
```

### 2.4 최소 행성 정의

Earth-Kopernicus.cfg 패턴을 따릅니다.
- `Template { name = Kerbin; removeAllPQSMods = True }` — 템플릿 초기화
- `PQS > Mods > VertexHeightMapBicubic` — 16비트 높이맵
- `PQS > Mods > VertexColorMap` — 컬러 맵
- `PQS > Mods > Parallax` — Parallax Continued 연동
- 대기 있는 천체. `Atmosphere` 블록 + `AtmosphereFromGround`

### 2.5 천체별 파일 분리

| 파일 | 내용 |
|------|------|
| `[Body]-Kopernicus.cfg` | 궤도, 물리, 대기, PQS, 바이옴 |
| `[Body]-Localization.cfg` | 표시 이름과 설명 (현지화 키) |
| `[Body]-ScienceDefs.cfg` | 과학 실험 결과 텍스트 |
| `[Body]-ParallaxTerrain.cfg` | Parallax 지형 설정 |
| `[Body]-ParallaxScatters.cfg` | Parallax 스캐터 오브젝트 |

---

## 3. 텍스처 컨벤션

| 용도 | 포맷 | 해상도 |
|------|------|--------|
| 높이맵 | DDS BC4 | 8k–16k |
| 컬러 맵 | DDS BC7 | 8k–16k |
| 바이옴 맵 | DDS | 4k |
| 아이콘 | PNG | 256x256 |
| 노멀 맵 | DDS BC5 | 4k–8k |

텍스처 경로 패턴.
```
NearStars-Textures/PluginData/[##_SystemFolder]/[##_BodyFolder]/Kopernicus/[BodyName]_[Type].dds
```

참고. BC5/BC7은 macOS에서 공식적으로 지원되지 않으며, Sol과 동일한 제한입니다.

## Related

- [methodology](methodology.md) — 클러스터 허브.
- [mod-reference](mod-reference.md) — 이 레이아웃이 패치하는 모드.
- [guideline](guideline.md) — `flightGlobalsIndex` 할당, phase-of-work 정의.
- [principia-cfg-reference](principia-cfg-reference.md) — Principia 패치 레이아웃 (§2.1 에서 참조).
