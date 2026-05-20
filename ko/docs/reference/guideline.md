# 근접 항성계 KSP 모드 — 프로젝트 가이드라인

**목표.** KSP 1.12.x 의 Sol-Configs (실제 태양계) 위에 근접 항성계를 추가합니다. RSS 호환은 향후 목표입니다.

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 모드명 | NearStars |
| KSP 버전 | 1.12.x |
| 라이선스 | CC-BY-NC-SA-4.0 (Sol과 동일) |
| 유형 | Sol 기반 애드온. RSS 호환은 미지원 (향후 목표). |

이 모드는 새로운 항성계를 추가하며, Sol의 기존 천체는 수정하거나 교체하지 않습니다. RSS 호환은 계획 중이지만 현재 릴리스에는 포함되지 않습니다.

---

## 2. 의존성

**필수.**

| 모드 | 역할 |
|------|------|
| Sol-Configs (ballisticfox) | 실제 태양계 베이스 (`FOR[SolSystem]`) |
| Kopernicus (ballisticfox fork) | 천체 정의 프레임워크 |
| Module Manager | 조건부 패칭 (`NEEDS[]`) |
| Parallax Continued | 지형 셰이더 및 스캐터 |
| EVE Volumetrics V5 | 구름 레이어 (대기 있는 천체 전용) |
| BurstPQS | 지형 생성 최적화 |

**향후 목표 (현재 미지원).**

| 모드 | 태그 |
|------|------|
| RealSolarSystem | `FOR[RSSConfig]` |

참고. RSS-Origin v1.x는 Sol을 지원하지 않습니다. Sol 지원이 포함된 v2는 개발 중이지만 아직 릴리스되지 않았습니다. §5.1 의 패치 템플릿은 추후 RSS 지원 시 자연스럽게 확장될 수 있도록 설계되어 있습니다.

---

## 3. 대상 항성계

### 3.1 거리 제한

| 엔진 | 최대 범위 | 출처 |
|------|----------|------|
| Kopernicus (렌더링 + SOI) | ~50 ly | REX 개발자 |
| Principia (중력 섭동체) | ~80 ly | RSS-Origin 개발자 |

~50 ly를 초과하는 Kopernicus 천체는 맵 뷰 오류, 렌더러의 부동소수점 결함, 또는 엔진 충돌이 발생할 수 있습니다. 이는 엄격한 제약 조건으로, 모든 Kopernicus 천체는 반드시 50 ly 이내에 있어야 합니다.

Principia는 KSP의 렌더링 제한을 받지 않는 별도의 메커니즘을 통해 별을 중력 섭동체로 등록합니다. 따라서 50–80 ly 범위의 별은 **Principia 전용 항목** (Kopernicus 천체 없음, 시각적 존재 없음, 중력 효과만) 후보가 됩니다.

### 3.2 범위

현재 데이터 파이프라인은 50 ly 이내의 모든 확인된 행성계와 주목할 만한 항성계를 포함하며, 2026-05-18 기준으로 136개 시스템 / 144개 항성 구성 요소입니다. 이는 Kopernicus 범위를 완전히 커버합니다. 50–80 ly 구간의 Principia 전용 패스는 필요 시 나중에 추가할 수 있습니다.

### 3.3 개발 순서

**하나의 완전한 시스템을 먼저 빌드하고, 그 다음 확장합니다.** 첫 번째 시스템은 이후 모든 시스템의 템플릿이자 참조 구현이 됩니다. 첫 번째 시스템이 완전히 플레이 가능해지기 전에 (해당 시스템의 Phase 1 + Phase 2 완료) 두 번째 시스템을 시작하지 않습니다.

최종 시스템 목록과 선택 순서는 미정이며, 후보로는 Proxima Centauri (가장 가깝고, 단일 별, 행성 2개), Barnard's Star (5.96 ly), Alpha Centauri (유명하지만 삼중성계 복잡도), 그 외 여러 시스템이 있습니다.

---

## 4. 저장소 구조

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

## 5. 설정 파일 컨벤션

### 5.1 패치 태그와 이중 호환 전략

> 상태. Sol 전용이 현재 MVP. 아래 RSS 측 패치는 향후 목표 구조로서 문서화한 것이며, 현재 릴리스에는 포함되지 않습니다.

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

### 5.2 천체 식별자

Sol 패턴을 따릅니다. `identifier = NearStars/BodyName`

### 5.3 최소 별 정의

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

### 5.4 최소 행성 정의

Earth-Kopernicus.cfg 패턴을 따릅니다.
- `Template { name = Kerbin; removeAllPQSMods = True }` — 템플릿 초기화
- `PQS > Mods > VertexHeightMapBicubic` — 16비트 높이맵
- `PQS > Mods > VertexColorMap` — 컬러 맵
- `PQS > Mods > Parallax` — Parallax Continued 연동
- 대기 있는 천체. `Atmosphere` 블록 + `AtmosphereFromGround`

### 5.5 천체별 파일 분리

| 파일 | 내용 |
|------|------|
| `[Body]-Kopernicus.cfg` | 궤도, 물리, 대기, PQS, 바이옴 |
| `[Body]-Localization.cfg` | 표시 이름과 설명 (현지화 키) |
| `[Body]-ScienceDefs.cfg` | 과학 실험 결과 텍스트 |
| `[Body]-ParallaxTerrain.cfg` | Parallax 지형 설정 |
| `[Body]-ParallaxScatters.cfg` | Parallax 스캐터 오브젝트 |

---

## 6. 텍스처 컨벤션

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

---

## 7. flightGlobalsIndex 할당

Sol-Configs **및** RSS-Origin과 충돌하지 않아야 합니다. NearStars는 1000+ 구간을 사용하며 시스템당 100개 인덱스를 배정합니다.

| 범위 | 소유자 |
|------|--------|
| 0–99 | 기본 KSP / RealSolarSystem (KSP-RO/RealSolarSystem은 1–25, 50, 60, 91–95 사용) |
| 100–199 | Sol-Configs (RSS-Reborn) |
| 1000–1099 | NearStars — 첫 번째 항성계 (미정) |
| 1100–1199 | NearStars — 두 번째 항성계 (미정) |
| 1200–1299 | NearStars — 세 번째 항성계 (미정) |
| 1300+ | NearStars — 이후 시스템 (시스템당 +100) |

각 100-인덱스 블록 내에서는 천체당 1씩 증가합니다. 별, 행성, 위성, 질량 중심은 같은 블록을 공유합니다.

---

## 8. 천문 데이터 출처

모든 궤도 파라미터와 물리 상수는 실제 관측 데이터에서 가져와야 합니다.

- **궤도 데이터.** NASA JPL Horizons, SIMBAD
- **외계행성.** NASA Exoplanet Archive
- **항성 물리.** SIMBAD Astronomical Database
- 텍스처 출처는 `Credits-License.md`에 문서화해야 합니다.

---

## 9. 개발 단계

**규칙. 다음 시스템을 시작하기 전에 하나의 시스템을 처음부터 끝까지 완성합니다.**

### Phase 1 — 첫 번째 시스템: 별 스켈레톤 (MVP)
- [ ] 파일럿 시스템 선택 (권장: Proxima Centauri)
- [ ] 저장소 구조 설정
- [ ] 별 천체 정의: 궤도, ScaledVersion, Properties
- [ ] 아이콘 및 현지화 키 스켈레톤
- [ ] Kopernicus 로드 확인 (Sol + RSS)

### Phase 2 — 첫 번째 시스템: 행성
- [ ] 행성 정의 (대기, PQS, 바이옴)
- [ ] 모든 천체가 올바르게 로드되고 공전하는지 확인

### Phase 3 — 첫 번째 시스템: 비주얼
- [ ] 텍스처 제작 (높이맵, 컬러 맵)
- [ ] Parallax 지형 및 스캐터
- [ ] 대기 있는 천체용 EVE 구름 레이어
- [ ] Scatterer 대기 설정

### Phase 4 — 첫 번째 시스템: 마무리 + 확장
- [ ] 모든 천체에 대한 과학 실험 텍스트
- [ ] 호환성 패치 (Principia, 해당 시 Kerbalism)
- [ ] 성능 최적화 패스
- [ ] Phase 1–3을 템플릿으로 삼아 두 번째 시스템 시작

---

## 10. 미결 결정 사항

- [x] 최종 모드명 — `NearStars`로 확정
- [ ] 파일럿 시스템 선택 (Proxima Centauri 권장)
- [ ] 항성 간 거리 스케일링 전략 — 실제 거리는 KSP에서 물리적으로 불가능하므로 상징적 압축이 필요합니다. Sol 기본, Sol 1/4, RSS 1:1 스케일 전반에 걸쳐 일관성을 유지해야 합니다. Kopernicus 하드 제한: ~50 ly (§3.1 참고).
- [x] macOS 텍스처 포맷 호환성 전략 — Windows 전용 모드이므로 BC5/BC7/BC4 DDS를 제한 없이 사용 가능
- [ ] RSS EVE 버전: V3 (무료) vs V5 (Patreon) — 둘 다 지원할지, Sol처럼 V5만 지원할지
- [ ] Principia 호환성: 스케일 변형별 별도 중력 모델 cfg가 필요하며, 50–80 ly 별에 대한 Principia 전용 항목 가능 (Kopernicus 천체 불필요)
