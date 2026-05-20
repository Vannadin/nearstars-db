# NearStars — Mod Reference

> **관점.** 이 문서는 **KSP 모드 설치 레퍼런스** 입니다. 어떤 모드를 설치해야 하는지, 무엇을 하는지, 어디서 받는지를 의존성 등급별 (Required / Graphics / Compatibility / Optional) 로 정리합니다.
>
> **저작권/라이선스** 관점 — NearStars 가 어떤 외부 모드의 콘텐츠를 reproduce 하고 그 라이선스 의무를 어떻게 이행하는지 — 은 [`data-sources.md`](data-sources.md) 를 참고하십시오. 그 문서는 Kopernicus, Principia, Sol-Configs 만 다룹니다. 나머지는 모두 설치 전용이며 attribution 의무가 없습니다.

## 필수 의존성 (없으면 모드가 로드되지 않음)

| 모드 | 설명 | GitHub |
|------|------|--------|
| **Kopernicus** (ballisticfox fork) | 커스텀 행성계 프레임워크. 없으면 NearStars 천체가 존재하지 않음. 라이선스: LGPL-3.0 — [data-sources.md §2](data-sources.md#kopernicus-ballisticfox-fork) 참조. | [ballisticfox/Kopernicus](https://github.com/ballisticfox/Kopernicus) |
| **Module Manager** | cfg 패치 언어 런타임. `NEEDS[]`, `FOR[]`, `@` 패치 문법을 제공. 없으면 모든 패치가 무효화됨 | [sarbian/ModuleManager](https://github.com/sarbian/ModuleManager) |
| **BurstPQS** | Burst 컴파일 지형 생성. 기본 대비 약 15배 빠르며, 씬 전환 시 버벅임 제거 | [Phantomical/BurstPQS](https://github.com/Phantomical/BurstPQS) |
| **Sol** (ballisticfox) | 실제 스케일, 1/4 스케일, 스톡 스케일로 구현된 현대적인 실제 태양계 재현. NearStars는 이 기반 시스템에 새로운 항성계를 부착함. 라이선스: CC-BY-NC-SA 4.0 — [data-sources.md §2](data-sources.md#sol-configs-rss-reborn--ballisticfox) 참조. | [RSS-Reborn/Sol-Configs](https://github.com/RSS-Reborn/Sol-Configs) |

---

## 그래픽 모드

### 직접 의존성 (NearStars cfg 파일이 직접 참조함)

| 모드 | 설명 | GitHub |
|------|------|--------|
| **Parallax Continued** | PBS 지형 셰이더 및 3D 산란 오브젝트. NearStars는 `[Body]-ParallaxTerrain.cfg`와 `[Body]-ParallaxScatters.cfg`를 직접 작성함 | [Gameslinx/Parallax-Continued](https://github.com/Gameslinx/Parallax-Continued) |
| **EVE-Redux / EVE Volumetrics V5** | 구름 및 오로라 레이어. V5는 체적 구름 추가 (Patreon 빌드). NearStars는 `EVE_CLOUDS` cfg를 직접 작성함 | [LGhassen/EnvironmentalVisualEnhancements](https://github.com/LGhassen/EnvironmentalVisualEnhancements) |

### 호환성 패치 — Priority 1 (없으면 비주얼이 깨짐)

| 모드 | 설명 | GitHub |
|------|------|--------|
| **Scatterer** | Rayleigh/Mie 대기 산란, 해양 반사, 태양 플레어. 행성마다 `Scatterer_atmosphere`, 별마다 `Scatterer_sunflare` 필요 | [LGhassen/Scatterer](https://github.com/LGhassen/Scatterer) |
| **Firefly** | 대기권 재진입 및 초음속 비행 시 공기역학적 가열 효과. `ATMOFX_PLANET_PACK` + `ATMOFX_BODY` 노드로 행성별 색상 및 강도 정의 | [M1rageDev/Firefly](https://github.com/M1rageDev/Firefly) |
| **Deferred Rendering** | KSP용 지연 렌더링 파이프라인. 별도 cfg 패치는 불필요하나, Scatterer/EVE 버전이 Deferred 호환인지 확인 필요. Parallax는 이미 호환됨 | [LGhassen/Deferred](https://github.com/LGhassen/Deferred) |

### 호환성 패치 — Priority 2 (없어도 로드되지만 품질 차이 있음)

| 모드 | 설명 | GitHub |
|------|------|--------|
| **Distant Object Enhancement** | 멀리 있는 행성과 별을 실제 겉보기 크기 및 색상으로 렌더링. 새 별마다 커스텀 플레어 색상 등록 필요 | [KSPModStewards/DistantObjectEnhancement](https://github.com/KSPModStewards/DistantObjectEnhancement) |
| **PlanetShine** | 행성과 위성이 우주선에 반사광을 비춤. 천체마다 반사광 색상 설정 필요 | [PapaJoesSoup/ksp-planetshine](https://github.com/PapaJoesSoup/ksp-planetshine) |
| **TUFX** | Unity Post Process Package v2 래퍼. 항성계별 블룸 및 색보정 프로파일 제공 가능 | [KSPModStewards/TUFX](https://github.com/KSPModStewards/TUFX) |

### 호환성 패치 — 선택

| 모드 | 설명 | GitHub |
|------|------|--------|
| **Textures Unlimited** | PBR 반사 셰이더. 금속성 또는 얼음 천체 표면에 물리 기반 반사 활성화 | [shadowmage45/TexturesUnlimited](https://github.com/shadowmage45/TexturesUnlimited) |
| **True Volumetric Clouds** | blackrack의 고급 체적 구름 시스템. EVE V5와 호환 불가 — 장기 로드맵으로 이연 | Patreon only |

---

## 비그래픽 호환성 패치

| 모드 | 설명 | GitHub |
|------|------|--------|
| **Principia** | N-body 중력 시뮬레이션. 별마다 중력 파라미터 등록 필요. Sol, Sol-Quarter, RSS 스케일별 별도 cfg. 라이선스: MIT — [data-sources.md §2](data-sources.md#principia-mockingbirdnest) 참조. | [mockingbirdnest/Principia](https://github.com/mockingbirdnest/Principia) |
| **Kerbalism** | 방사선, 생명유지, 과학 오버홀. 항성계마다 방사선 환경 cfg 필요. 지원 미정 | [Kerbalism/Kerbalism](https://github.com/Kerbalism/Kerbalism) |
| **ResearchBodies** | 망원경 기반 천체 발견 메커닉. 새 천체를 발견 목록에 등록 필요 | [JPLRepo/ResearchBodies](https://github.com/JPLRepo/ResearchBodies) |

---

## 참고 저장소 (다른 행성 팩 예시)

| 저장소 | 용도 |
|--------|------|
| [SPACEMAN9813/Firefly-Planet-Pack-Configs](https://github.com/SPACEMAN9813/Firefly-Planet-Pack-Configs) | 여러 행성 팩의 Firefly cfg 예시 |
| [OneSaltyPringle/OPM-Parallax](https://github.com/OneSaltyPringle/OPM-Parallax) | OPM의 Parallax Continued cfg 예시 |
