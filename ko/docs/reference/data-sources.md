# 데이터 출처 및 저작권 표기

> **관점.** 이 문서는 **저작권/라이선스** 레퍼런스입니다. NearStars 가 reproduce 하는 외부 콘텐츠 (천문 데이터 값, 모드 cfg 패턴), 각각의 라이선스 의무, NearStars 가 그것을 어떻게 이행하는지를 정리합니다.
>
> **KSP 모드 설치 목록**(Required / Graphics / Compat 분류)은 [`mod-reference.md`](mod-reference.md) 참고. 아래 §2는 NearStars가 건드리는 **모든** 모드를 링크와 라이선스와 함께 싣고, 실제 attribution 의무가 있는 쪽(알고리즘을 이식한 Kerbalism, cfg 형식을 서술하는 Kopernicus·Principia·Sol-Configs·Firefly)과 이름만 참조하는 쪽을 나눕니다.
>
> 이 저장소의 라이선스/attribution 파일 삼각형.
> - [`LICENSE`](../../../LICENSE) — NearStars 자체 라이선스 (CC-BY-NC-SA 4.0).
> - [`NOTICE`](../../../NOTICE) — 이 저장소가 reproduce 하거나 묘사하는 외부 콘텐츠의 원문 라이선스 텍스트.
> - 이 문서 — *정책*. 어떤 출처를 쓰는지, 어떤 인용 의무가 있는지, NearStars 가 실제로 어떻게 이행하는지.

NearStars DB는 공개된 천문 측정 데이터와 KSP 모드 설정 패턴을 통합하여
시스템별 단일 JSON 레코드로 구성합니다. 이 파일은 파이프라인이 사용하는
모든 외부 출처, 해당 출처의 인용 정책, NearStars가 제공하는 저작권 표기를 정리합니다.

---

## 1. 천문 데이터 출처

### NASA Exoplanet Archive

- **사용처.** `scripts/pipeline/fetch_planets.py`, `fetch_planets_ps.py`,
  `build_curated_from_ps.py`
- **사용 테이블.** `pscomppars` (복합, 참조 전용),
  `ps` (`default_flag=1`인 논문별 행)
- **라이선스.** 공공 도메인 데이터, 인용 권장
- **인용문.**
  > This research has made use of the NASA Exoplanet Archive, which is
  > operated by the California Institute of Technology, under contract
  > with the National Aeronautics and Space Administration under the
  > Exoplanet Exploration Program.
- **참고 문헌.** Akeson, R. L. et al. 2013, PASP, 125, 989
- **행별 논문 저작권 표기**는 `db/planets_curated.json`의 `bibcode`, `doi` 필드에
  그대로 보존되어, 채택된 각 값이 원래 게재 논문의 bibcode를 유지하도록 합니다.

### Gaia DR3 (ESA)

- **사용처.** `scripts/pipeline/fetch_astrometry.py`
- **TAP 엔드포인트.** `https://gea.esac.esa.int/tap-server/tap`
- **라이선스.** CC BY 4.0 (데이터). 논문 게재 시 인용 필수
- **인용문.**
  > This work has made use of data from the European Space Agency (ESA)
  > mission Gaia (https://www.cosmos.esa.int/gaia), processed by the
  > Gaia Data Processing and Analysis Consortium (DPAC). Funding for
  > the DPAC has been provided by national institutions, in particular
  > the institutions participating in the Gaia Multilateral Agreement.
- **참고 문헌.**
  - Gaia Collaboration et al. 2016, A&A, 595, A1 (미션)
  - Gaia Collaboration et al. 2023, A&A, 674, A1 (DR3)

### SIMBAD (CDS Strasbourg)

- **사용처.** `scripts/pipeline/fetch_astrometry.py` (폴백),
  `fetch_stellar_props.py`
- **TAP 엔드포인트.** `https://simbad.u-strasbg.fr/simbad/sim-tap/sync`
- **라이선스.** 학술 목적 무료 사용. 인용 권장
- **인용문.**
  > This research has made use of the SIMBAD database, operated at CDS,
  > Strasbourg, France.
- **참고 문헌.** Wenger, M. et al. 2000, A&AS, 143, 9
- **사용 테이블.** `basic`, `ident`, `mesDiameter`, `mesFe_H`

### TEPCat (Transiting Exoplanet Catalogue)

- **사용처.** `scripts/pipeline/fetch_planets.py` (통과 폴백)
- **URL.** `https://www.astro.keele.ac.uk/jkt/tepcat/allplanets-csv.csv`
- **라이선스.** 학술 목적 무료 사용. 인용 권장
- **인용문.**
  > This paper makes use of data from the TEPCat catalogue available at
  > https://www.astro.keele.ac.uk/jkt/tepcat/
- **참고 문헌.** Southworth, J. 2011, MNRAS, 417, 2166

### DACE (Geneva Observatory)

- **사용처.** Curation Phase 1 / Curation Phase 2 중 `omega_deg` / `tperi_bjd`가 없는
  RV 검출 행성의 수동 조회
- **URL.** `https://dace.unige.ch/exoplanets/`
- **라이선스.** 학술 목적 무료 사용. 인용 권장
- **참고 문헌.** Buchschacher, N. & Alesina, F. 2019, ASP Conf. Series

### Crossref

- **사용처.** `scripts/pipeline/build_curated_from_ps.py` (DOI 조회)
- **API.** `https://api.crossref.org/works/<bibcode>`
- **라이선스.** 무료, 인증 불필요
- **참고.** Crossref 데이터는 bibcode → DOI 변환에 사용됩니다. 기반이 되는
  논문 메타데이터는 원래 출판사의 소유입니다.

### [NASA ADS](https://ui.adsabs.harvard.edu) (Astrophysics Data System)

- **사용.** `scripts/phase3/build_bibliography.py`, `expand_citations.py`,
  `scripts/check_citation_links.py`, 그리고 모든 큐레이션 세션(논문 발견·검증은
  웹 검색이 아니라 ADS를 거치는 것이 프로젝트 규칙입니다)
- **API.** 등록 토큰으로 [`api.adsabs.harvard.edu`](https://ui.adsabs.harvard.edu/help/api/)
- **라이선스.** 계정만 있으면 무료, 사용 사실을 밝혀 달라고 요청
- **인용문.**
  > This research has made use of NASA's Astrophysics Data System
  > Bibliographic Services.
- **이행.** 이 저장소의 모든 인용은 ADS bibcode 또는 arXiv id로 핀되고 클릭 가능한
  링크로 렌더됩니다(게이트 `check_citation_links.py`).

### [arXiv](https://arxiv.org) / [ar5iv](https://ar5iv.labs.arxiv.org)

- **사용.** `scripts/phase3/fetch_arxiv_texts.py`
- **라이선스.** 논문별(arXiv 비독점 라이선스 또는 CC 계열). ar5iv는 HTML 렌더 서비스
- **이행.** 전문은 `docs/phase3/_papers/`에 **검증 목적으로만** 캐시하며 재배포하거나
  발행하지 않습니다. 미러가 아니라 에이전트의 읽기 경로입니다.

### [Stellarium Web](https://stellarium-web.org)

- **사용.** `scripts/pipeline/fetch_stellarium_ids.py`,
  `scripts/verification/stellarium_crosscheck.py`
- **라이선스.** Stellarium은 GPL-2.0-or-later. skysource ID와 표시 위치만 읽어
  우리 측성값을 독립 대조하는 용도입니다
- **참고.** Stellarium 데이터는 `db/`에 들어가지 않습니다. 검증 오라클입니다.

### [NIST Atomic Spectra Database](https://physics.nist.gov/asd)

- **사용.** `scripts/refs/build_atomic_lines.py`, `build_lte_plasma_colors.py`
  (플라스마 발광색 엔진)
- **라이선스.** 미국 정부 저작물, 자유 사용. NIST가 인용을 요청
- **문헌.** Kramida, A., Ralchenko, Yu., Reader, J. and NIST ASD Team,
  *NIST Atomic Spectra Database* (version 5.11), <https://physics.nist.gov/asd>
- **이행.** [`element-plasma-colors.md`](element-plasma-colors.md)와 거기서 생성한 원소별
  색 표에 인용을 답니다.

### [USGS Spectral Library](https://pubs.usgs.gov/ds/1035/)

- **사용.** 표면색 작업([`surface-color-albedo-methodology.md`](surface-color-albedo-methodology.md))
- **라이선스.** 미국 정부 저작물, 자유 사용. 인용 요청
- **문헌.** Kokaly, R. F. et al. 2017, USGS Data Series 1035
  (*USGS Spectral Library Version 7*)

---

## 2. KSP 모드 참조

NearStars는 여러 KSP 모드의 하위 프로젝트입니다. `.claude/skills/`의 스킬들이
이 모드들과 호환되는 cfg 생성법을 설명하며, 스키마 주장에는 상위 소스의 줄 번호를
근거로 답니다. 항목 순서는 의무의 강도입니다. 이식한 알고리즘, 서술한 cfg 형식,
타깃으로만 이름을 쓰는 모드 순입니다.

### [Kerbalism](https://github.com/Kerbalism/Kerbalism)

- **라이선스.** [Unlicense](https://github.com/Kerbalism/Kerbalism/blob/master/LICENSE)(퍼블릭 도메인). 허가가 필요 없고, 출처 표기는 예의상 답니다.
- **NearStars 사용.** 이 저장소에서 **유일하게 이식한 알고리즘**입니다.
  `scripts/viz/render_belts.py`와 `scripts/viz/fit_belts.py`가
  [`src/Kerbalism/Radiation/Radiation.cs`](https://github.com/Kerbalism/Kerbalism/blob/master/src/Kerbalism/Radiation/Radiation.cs)의
  방사선장 부호거리 함수와 선량 램프 `clamp(gradient·−SDF/radius,0,1)·intensity`를 재현하고,
  [`docs/belt-viewer.html`](../../../docs/belt-viewer.html)이 같은 함수를 브라우저에서 계산합니다.
  프레임 규칙(벨트는 기울어진 프레임, 자기권계면은 항성정렬)도 이 파일에서 읽었습니다.
- **함께.** [ROKerbalism](https://github.com/KSP-RO/ROKerbalism)이 이 프로젝트가 대조하는
  RSS 스케일 `RadiationModel` 값을 제공합니다([`solar-system-radiation-belts.md`](solar-system-radiation-belts.md)).

### [Kopernicus](https://github.com/ballisticfox/Kopernicus) (ballisticfox fork)

- **라이선스.** LGPL-3.0
- **NearStars 사용.** 스킬 `kopernicus-cfg`는 공개 소스 코드와 문서를 참고하여
  파악한 cfg 문법을 설명합니다. 이 저장소에는 C# 소스가 그대로 복사되지 않습니다.

### [Principia](https://github.com/mockingbirdnest/Principia) (mockingbirdnest)

- **라이선스.** [MIT](https://github.com/mockingbirdnest/Principia/blob/master/LICENSE.txt), Copyright (c) 2014 Robin Leroy
- **NearStars 사용.** `docs/reference/principia-cfg-reference.md`는
  매개변수 테이블과 간단한 문법 예시와 함께 cfg 노드 구조를 설명합니다.
  표시된 수치(예. Sun μ = 1.327e+11 km³/s²)는 IAU 2009의 공공 도메인 물리 상수이며
  Principia 고유 데이터가 아닙니다.

### [Sol-Configs](https://github.com/RSS-Reborn/Sol-Configs) (RSS-Reborn / ballisticfox)

- **라이선스.** CC-BY-NC-SA 4.0 (NearStars 와 동일. 상위 NOTICE 기준).
- **NearStars 사용.** 스킬 `kopernicus-cfg` 참조 파일
  (`planet-body.md`, `star-body.md`, `ocean.md`)은 raw URL을 통해 상위 Sol-Configs
  파일에 링크하고 각 링크에 일반적인 KSP-Kopernicus 패턴을 함께 제공합니다.
  라이선스가 동일(CC-BY-NC-SA 4.0)하므로 verbatim 재현도 가능하지만, 상위 변경이 자동으로 반영되도록 raw-link 방식을 사용합니다.

### [Firefly](https://github.com/M1rageDev/Firefly)

- **라이선스.** 코드 GPL-3.0, **모델·텍스처 자산은 All Rights Reserved**
  ([LICENSE](https://github.com/M1rageDev/Firefly/blob/master/LICENSE)).
- **NearStars 사용.** `firefly-cfg` 스킬이 `ConfigManager.cs:line` 인용과 함께 cfg 스키마를
  문서화하고, 이 저장소가 바디별 재진입 효과 cfg를 씁니다. 자산은 하나도 복사하지 않으며
  플라스마 색은 Firefly 텍스처가 아니라 우리 분광 작업([`element-plasma-colors.md`](element-plasma-colors.md))에서
  나옵니다. 팩 컨벤션은 [Firefly-Planet-Pack-Configs](https://github.com/SPACEMAN9813/Firefly-Planet-Pack-Configs)와 교차 확인했습니다.

### 이름만 참조하는 나머지 KSP 모드

NearStars는 이들의 패치 문법을 *타깃으로* cfg를 쓸 뿐, 소스·자산·cfg 내용을 재현하지
않으므로 attribution 의무가 없습니다. 집합이 빠짐없이 드러나고 각각에 닿을 수 있도록
여기 싣습니다. 설치 측 분류는 [`mod-reference.md`](mod-reference.md)에 있습니다.

| 모드 | 여기서의 역할 |
|---|---|
| [Module Manager](https://github.com/sarbian/ModuleManager) | 우리 cfg가 쓰이는 패치 런타임(`NEEDS[]`, `FOR[]`, `@`) |
| [BurstPQS](https://github.com/Phantomical/BurstPQS) | PQS 바디 지형 생성 가속 |
| [Parallax Continued](https://github.com/Gameslinx/Parallax-Continued) | 지형 셰이더·스캐터. 바디별 cfg를 emit |
| [OPM-Parallax](https://github.com/OneSaltyPringle/OPM-Parallax) | 그 cfg의 컨벤션 참고 |
| [Scatterer](https://github.com/LGhassen/Scatterer) | 대기 산란. 바디별 cfg를 emit |
| [EVE (Redux / Volumetrics)](https://github.com/LGhassen/EnvironmentalVisualEnhancements) | 구름·오로라. Volumetrics EA 빌드는 Patreon 배포이며 **EA 자산·스키마는 이 저장소에 커밋하지 않습니다** |
| [Deferred Rendering](https://github.com/LGhassen/Deferred) | 시각 작업이 가정하는 조명 경로 |
| [Textures Unlimited](https://github.com/shadowmage45/TexturesUnlimited) | PBR 셰이더 스택 |
| [TUFX](https://github.com/KSPModStewards/TUFX) | 후처리 프로파일 |
| [Distant Object Enhancement](https://github.com/KSPModStewards/DistantObjectEnhancement) | 원거리 천체 가시성 |
| [PlanetShine](https://github.com/PapaJoesSoup/ksp-planetshine) | 알베도 조명 |
| [ResearchBodies](https://github.com/JPLRepo/ResearchBodies) | 발견 여부. 우리 패치 층은 은퇴했으나 문서로 남김 |
| [BetterTimeWarpContinued](https://github.com/linuxgurugamer/BetterTimeWarpContinued) | 성간 항행용 워프 배율 |
| [Relativity](https://github.com/Vannadin/Relativity) | 우리가 만든 동반 모드 |

Kerbal Space Program 자체는 © Squad / Private Division / Intercept Games이며,
NearStars는 비공식 팬 모드입니다.

---

## 2b. 사이트에 포함된 웹 자산

이들은 `docs/` **안에** 함께 배포되므로 라이선스가 이 저장소를 따라다닙니다.

| 자산 | 위치 | 라이선스 |
|---|---|---|
| [marked](https://github.com/markedjs/marked) 12.0.2 | `docs/assets/marked.min.js` | MIT |
| [github-markdown-css](https://github.com/sindresorhus/github-markdown-css) 5.5.0 | `docs/assets/github-markdown-{dark,light}.min.css` | MIT |
| [Plotly.js](https://github.com/plotly/plotly.js) | `docs/assets/plotly.min.js` | MIT |
| [Geist / Geist Mono](https://github.com/vercel/geist-font) | `docs/assets/fonts/*.woff2` | SIL OFL 1.1 |
| [three.js](https://github.com/mrdoob/three.js) 0.160.0 | **미포함** — 성도·궤도 뷰어가 [jsDelivr](https://cdn.jsdelivr.net/npm/three@0.160.0)에서 ES 모듈로 로드 | MIT |

모드가 아닌 문헌에서 이식한 구현이 하나 더 있습니다. **Mauk & Fox 2010**의 자체
Kennel–Petschek 코드([Zenodo](https://zenodo.org/records/4782323))를
`scripts/refs/kp_limit.py`로 이식하고 논문에 인쇄된 중간값으로 검증했습니다.
[REBOUND](https://github.com/hannorein/rebound)(GPL-3.0)는 안정성 샌드박스가 설치본을
라이브러리로 쓰며 저장소에 포함하지 않습니다.

---

## 3. NearStars 자체 제작 콘텐츠

다음 항목들은 NearStars 자체적으로 생산된 것으로 위의 어떤 출처에서도 파생되지 않았습니다.

- `scripts/pipeline/`의 파이프라인 스크립트
- `scripts/pipeline/schema.py`의 스키마 설계 및 `docs/reference/methodology.md`의
  cfg 레이어 결정 사항
- 쌍성계 에포크 해석 로직
  ([`binary-epoch-pipeline.md`](binary-epoch-pipeline.md))
- 큐레이션된 JSON 파일(`db/*_curated.json`) — 인용된 측정값들의 집계본이며,
  집계 방식, 방법 등급 선택, `recommended` 플래그는 NearStars 편집 결정 사항입니다.

이 항목들은 NearStars 저장소가 채택한 라이선스를 따릅니다
(최상위 `LICENSE` 파일 참조).

---

## 4. 업스트림 이슈 보고

NearStars 교차 검증 과정에서 위 데이터 출처의 결함이 발견되면,
해당 이슈는 [`archive_issues.md`](archive_issues.md)에 기록되고,
적절한 경우 해당 파일에 명시된 연락처를 통해 카탈로그 관리자에게 보고됩니다.
