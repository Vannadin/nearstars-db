# 데이터 출처 및 저작권 표기

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

- **사용처.** Phase 1 / Phase 2 큐레이션 중 `omega_deg` / `tperi_bjd`가 없는
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

---

## 2. KSP 모드 참조

NearStars는 여러 KSP 모드의 하위 프로젝트입니다. `.agents/skills/`의 스킬들은
이러한 모드와 호환되는 cfg 파일을 생성하는 방법을 설명하며,
때로는 상위 저장소의 예시 코드 조각을 인용합니다.

### Kopernicus (ballisticfox fork)

- **저장소.** `ballisticfox/Kopernicus`
- **라이선스.** LGPL-3.0
- **NearStars 사용.** 스킬 `kopernicus-cfg`는 공개 소스 코드와 문서를 참고하여
  파악한 cfg 문법을 설명합니다. 이 저장소에는 C# 소스가 그대로 복사되지 않습니다.

### Principia (mockingbirdnest)

- **저장소.** `mockingbirdnest/Principia`
- **라이선스.** MIT
- **NearStars 사용.** `docs/reference/principia-cfg-reference.md`는
  매개변수 테이블과 간단한 문법 예시와 함께 cfg 노드 구조를 설명합니다.
  표시된 수치(예. Sun μ = 1.327e+11 km³/s²)는 IAU 2009의 공공 도메인 물리 상수이며
  Principia 고유 데이터가 아닙니다.

### Sol-Configs (RSS-Reborn / ballisticfox)

- **저장소.** `RSS-Reborn/Sol-Configs`
- **라이선스.** CC-BY-NC-SA 4.0 (NearStars 와 동일. 상위 NOTICE 기준).
- **NearStars 사용.** 스킬 `kopernicus-cfg` 참조 파일
  (`planet-body.md`, `star-body.md`, `ocean.md`)은 raw URL을 통해 상위 Sol-Configs
  파일에 링크하고 각 링크에 일반적인 KSP-Kopernicus 패턴을 함께 제공합니다.
  라이선스가 동일(CC-BY-NC-SA 4.0)하므로 verbatim 재현도 가능하지만, 상위 변경이 자동으로 반영되도록 raw-link 방식을 사용합니다.

### Module Manager, Parallax Continued, EVE, Scatterer, Firefly 등

- **사용.** cfg 호환 맥락을 위한 스킬 참조 파일에 이름으로 언급됩니다.
  소스나 cfg 내용은 복사되지 않습니다. 전체 의존성 목록 및 상위 링크는
  [`docs/reference/mod-reference.md`](mod-reference.md)를 참조하세요.

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
