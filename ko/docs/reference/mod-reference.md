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

## Time-Warp & Relativity (interstellar-play 세트) — Principia-fork 호환성 (2026-07-18 검증)

sub-light 성간 플레이는 스톡을 훨씬 넘어서는 warp 배율이 필요합니다 (0.1c 로 40 ly 는
400 년이며, 스톡 100,000배에서는 실시간 35시간이 걸립니다). 그래서 이 두 모드는
Principia fork 와 함께 다닙니다. 호환성은 upstream FAQ 의 규칙 — "엔진을 사용하지 않고
(1) vessel 을 움직이거나 궤도를 바꾸는가, 또는 (2) time warp 중에 그렇게 하는가" 를
기준으로 비호환을 판단 — 에 두 모드의 소스 코드를 직접 읽고 대조해 평가했습니다.

| 모드 | 판정 | GitHub |
|-----|------|--------|
| **BetterTimeWarpContinued** | 호환 (rate-table 모드로 vessel 을 전혀 움직이지 않음). Upstream 측정치. 100,000배에서는 매끄럽고, 1,000,000배에서는 "덜컹거림"(정합성이 아닌 CPU 문제), vessel 이 없으면 6,000,000배에서도 매끄러움. 지속적인 ultra-warp 의 실질적 한계는 Principia 의 CPU + **RAM 증가**(우리 PR 이 겨냥하는 upstream eviction 이슈)이며, 인게임 kit 의 장거리 순항 시나리오로 측정해야 합니다. physics warp 보다는 rails warp 를 우선하세요. physics warp 를 부스트해도 unpacked integration 부하만 곱해질 뿐입니다. fork 의 WS4 dead-man switch 는 설계상 warp 배율과 무관하고, WS3 burn integration 은 임의의 Δt 청크를 받아들입니다. | [linuxgurugamer/BetterTimeWarpContinued](https://github.com/linuxgurugamer/BetterTimeWarpContinued) |
| **Relativity** (Vannadin) | 설계상 일반(unpacked) 비행에서 호환. γ³ 추력 억제가 Principia 의 TimingManager 읽기보다 앞서 보정용 part-force 로 주입되며, 이는 Principia force profile 로 인게임에서 검증되었습니다. proper-time ledger 는 로드/언로드 vessel 모두에서 매 FixedUpdate 마다 틱합니다(time-warp 에서도 유효). "warp guard" 는 time warp 가 아니라 FTL-drive Provider 훅입니다. **알려진 공백. fork 의 WS3 on-rails burn 은 γ³ 보정을 전혀 받지 않습니다** — burn harvest 가 엔진 모듈 데이터(maxThrust × throttle × 진공 Isp)로 추력을 합성하는데, 보정용 force 는 (packed-idle 상태의) part-force 채널에만 존재합니다. 그 결과 c 근처에서 warp-burning 하면 Newtonian 추력이 그대로 적분되어 c 를 넘을 수 있습니다. 해법의 형태. WS3 harvest 가 Relativity 에게 1/γ³ 배율을 질의하도록 만듭니다(reflection, present-guarded, Relativity 의 Kerbalism adapter 와 같은 패턴). 질량 유량은 그대로 둡니다(Relativity 의 설계와 일치). Principia-fork 쪽에서 추적 중입니다. | [Vannadin/Relativity](https://github.com/Vannadin/Relativity) |

또한 참고. upstream 은 **Blueshift**(warp drive)를 비호환으로 분류하는데, fork 의
WS4 release channel (`PrincipiaWarpStatus.warpEngaged`) 은 정확히 그 비호환 부류를
해소하기 위해 존재합니다 — warp 모드가 vessel 을 Principia 관리에서 풀어주고
도착 시 재편입시킵니다. warp 중 궤도를 직접 편집하는 non-standard 추진
(Persistent-Thrust 방식) 은 WS3 를 경유하지 않는 한 upstream 규칙상 여전히
비호환입니다 (표준 `ModuleEngines` 상속 모듈이 WS3 harvest 가 읽는 대상입니다).

## 참고 저장소 (다른 행성 팩 예시)

| 저장소 | 용도 |
|--------|------|
| [SPACEMAN9813/Firefly-Planet-Pack-Configs](https://github.com/SPACEMAN9813/Firefly-Planet-Pack-Configs) | 여러 행성 팩의 Firefly cfg 예시 |
| [OneSaltyPringle/OPM-Parallax](https://github.com/OneSaltyPringle/OPM-Parallax) | OPM의 Parallax Continued cfg 예시 |

## Related

- [methodology](methodology.md) — 클러스터 허브.
- [mod-release-layout](mod-release-layout.md) — 이 모드들을 소비하는 repo 레이아웃.
- [data-sources](data-sources.md) — 여기 인용된 모드의 라이선스/어트리뷰션 측면 (Kopernicus, Principia, Sol-Configs).
- [guideline](guideline.md) — 프로젝트 차원의 범위 (어떤 모드가 필수인지 vs 선택인지).
- [principia-cfg-reference](principia-cfg-reference.md) — Principia 모드의 cfg API.
