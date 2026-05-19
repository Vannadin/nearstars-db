# Phase 1 큐레이션 — 컨텍스트 노트

이 큐레이션 과정에서 내린 결정의 추가 전용 로그입니다.

## 2026-05-19 — 세션 시작

**트리거:** 사용자가 `nearstars-add-star` 스킬을 "50광년 이내 행성 호스트 전체에 대한 Phase 1 자료조사"로 호출했습니다.

**기준 상태 (리셋 커밋 `1f023d0` 이후).**
- `planets_curated.json`: 비어 있음 `{}`
- `stellar_props_curated.json`: 3개 항목 (α Cen A, α Cen B, Barnard) — 고품질 항목 보존됨
- `validate.py`: FAIL 0, WARN 282 (일괄 채우기 이전으로 복귀)
- `db/systems/*.json`에 자동 조회된 raw 데이터로부터 행성 호스트 121개, 행성 223개 존재.

**현재 상황:** 이전 커밋 `0e42da6`에서 NASA Archive `pscomppars`(복합)으로 curated 항목을 일괄 채웠습니다. 정책 [[feedback-planet-curation]]은 논문별 출처 표기를 요구합니다. 스킬 검증 테스트: 이번에는 올바르게 다시 수행합니다.

## 결정 사항

### 소스 테이블: `pscomppars` 아닌 `ps`

`fetch_planets.py`는 현재 `pscomppars`(행성당 1행, NASA 병합 복합 값)를 쿼리합니다. Phase 1에서는 `ps` 테이블에서 `default_flag=1`로 필터링한 논문별 행이 필요합니다. NASA는 행성당 하나의 논문을 권위 있는 것으로 표시하며, 해당 값과 그 논문의 bibcode가 우리의 출처가 됩니다.

트레이드오프: `ps` default가 최신 논문보다 늦을 수 있습니다. Phase 1에서는 허용 가능합니다(단일 출처 정책). Phase 2에서는 어차피 전체 문헌을 탐색합니다.

### PoC 선택: 주요 케이스를 대표하는 3개 호스트

- **GJ 179** — RV 행성 1개, 단일별, 단순한 케이스.
- **GJ 581** — RV 행성 3개, 잘 연구된 시스템, 다중 행성 처리 테스트와 Pourbaix/Mann 스타일 호스트 논문 존재 가능성 검증.
- **GJ 1132** — 행성 2개, transit + RV 혼합, TEPCat 상호작용 테스트 (`build_systems`이 `curated > tepcat > nasa_archive` 순서 적용).

### 워크플로 선택 (사용자 프롬프트 이후)

사용자가 단일 워크플로를 미리 확정하지 않고 "PoC 먼저"를 선택했습니다. PoC를 통해 다음을 결정합니다.
- ADS WebFetch per 행성이 223개 규모에서 실현 가능한지, 또는
- raw HTML 참조 필드에서 bibcode를 추출하고 표본 기반 검증으로 충분한지.

행성당 WebFetch가 약 2분 걸린다면 223 × 2 = 7.5시간 — 5-15시간 정책 예산 이내입니다. 훨씬 느리다면 표본 검증으로 대체합니다.

### 고품질 수동 항목 보존

α Cen A, α Cen B (Pourbaix & Boffin 2016), Barnard's star (Mann 2015 / Rains 2021)가 이미 `stellar_props_curated.json`에 있습니다. **덮어쓰지 않습니다.** 모든 자동 큐레이션 단계에서 기존 항목이 있는지 먼저 확인해야 합니다.

### 파일 위치

plan/checklist/context-notes는 `docs/phase1-50ly/`에 위치합니다 (저장소 루트가 아닌). 이렇게 하면 저장소 루트가 깔끔하게 유지되고, 이 파일들이 프로젝트 전체 문서가 아닌 이번 큐레이션 과정에 한정된 것임을 나타냅니다.

## 작업 진행 중 발견 사항 (아래에 계속 추가)

### 2026-05-19 — ADS 페이지가 JS 렌더링 방식

`https://ui.adsabs.harvard.edu/abs/<bibcode>/abstract`(및 `/exportcitation`, `/link_gateway/...`)에 대한 WebFetch는 ADS UI가 JavaScript SPA이기 때문에 빈 콘텐츠를 반환합니다. ADS API 토큰 없이는 bibcode별 WebFetch 검증이 불가능합니다.

**결정 사항.**
- NASA `ps` 테이블의 `pl_refname` HTML에서 파싱된 bibcode가 1차 출처 식별자입니다 — 이미 정식 ADS 코드이며 구조적으로 유효성 검증 가능합니다 (연도-저널-권-페이지-저자 패턴).
- DOI는 Crossref 공개 서지 검색을 통해 bibcode 파생 검색어(저자, 연도, 저널명, 권, 페이지)로 최선 노력으로 기록합니다. Crossref 미인증 API는 정상 작동합니다.
- Crossref에서 확신 있게 확인되지 않는 경우 DOI는 null로 유지됩니다. curated 항목에는 여전히 bibcode + 참조 출처 표기가 있으며, 이는 [[feedback-planet-curation]] 정책의 "bibcode/doi 명시" 조건을 만족합니다.

### 2026-05-19 — build_systems.py dedup 제한

643번째 줄: 행성 curated 출처는 `doi`가 있을 때만 `sources[]`에 추가됩니다 (bibcode 폴백 없음). curated 항목에 bibcode가 있어도 647번째 줄에 `"bibcode": None`이 하드코딩되어 있습니다.

**결정 사항.** dedup을 `bibcode or doi` 를 허용하도록 확장하고, curated 항목의 `bibcode`를 `sources[]` 행으로 전파합니다. 간단한 수정으로 이번 과정에 적용합니다.

### 2026-05-19 — 항성 질량/반지름의 method 레이블이 측정값이 아닌 휴리스틱

`ps` 테이블은 행별 `st_mass` / `st_rad`와 `st_refname`을 제공하지만 `st_method` 필드는 없습니다. 일괄 빌더는 항성 질량에 `method: "spectroscopic_calibration"`, 반지름에 `method: "evolutionary_model"`을 하드코딩합니다 — 이는 50광년 샘플의 M형 왜성 중심 분포에서 일반적인 기본값이지만, 소스 논문에서 추출한 것은 아닙니다.

**Phase 1에서 허용 가능한 이유.**
- 출처 표기(bibcode + 참조 + DOI)는 올바르며 실제 논문을 식별합니다.
- method 레이블은 동일한 별에 대해 여러 측정값이 있을 때 `recommended` 선택에만 영향을 줍니다. Phase 1에서는 별당 정확히 하나의 측정값이 있으므로, method에 관계없이 `recommended: true`가 설정됩니다.
- Phase 2 격상은 각 논문을 개별적으로 읽고 method 레이블을 수정합니다 — 이는 Phase 2가 명시적으로 수행하는 작업 중 하나입니다 ([[feedback-planet-curation]] 참조).

**향후 개선 사항.** `method_inferred: true` 플래그를 추가하거나, default-flag 논문이 비기본적인 방법을 사용하는 것으로 알려진 호스트 (예: 간섭계 반지름)에 대한 논문별 method 오버라이드 테이블을 추가합니다.

### 2026-05-19 — 백업 규칙

일괄 채우기 전 백업이 `/tmp/nearstars_backup/`에 저장됩니다 (저장소 외부, 재귀 위험 없음).

### 2026-05-19 — `st_refname`의 URL 인코딩된 bibcode

NASA Archive는 ADS URL의 `&`를 일관성 없이 인코딩합니다. 일부 행은 리터럴 `&`를 보내고 (예: `pl_refname`의 `2024A&A...688A.112V`), 다른 행은 URL 인코딩된 `%26`을 보냅니다 (예: HD 40307의 `st_refname`에서 `2013A%26A...549A..48T`). 기존 정규식 `[0-9A-Za-z\.\&\+\-]+`는 인코딩된 것을 놓쳐 10개 이상의 호스트에 대한 A&A bibcode를 자동으로 누락시켰습니다.

**수정 사항.** 정규식 문자 클래스에 `%`를 추가하고 캡처된 그룹에 `urllib.parse.unquote()`를 적용했습니다. 115개의 고유한 행성 bibcode와 114개의 호스트 bibcode 모두 정상적으로 파싱됨을 확인했습니다.

### 2026-05-19 — 남은 공백은 실제 공백

모든 수정 후에도 2개의 행성 호스트가 여전히 질량 없음 (GJ 163, Ross 458), 22개는 반지름 없음. NASA TAP 직접 쿼리를 통해 이 호스트들이 해당 파라미터에 대해 **행이 전혀 없음**을 확인했습니다 — 파서 버그가 아니라, NASA Archive가 단순히 해당 값을 보유하지 않는 것입니다. Phase 2에서는 이를 위해 NASA 외부 자료 (Mann 2015 교정, Gaia DR3 GSP-Phot, 간섭계 카탈로그 등)를 조회해야 하며 — 이는 여기서는 범위 외입니다.

### 2026-05-19 — `ps` default 행에서 실제 논문별 출처 표기 확인

PoC 호스트 정상성 검사 결과, `ps` 테이블 `default_flag=1` 행이 Phase 1에 필요한 것을 정확히 제공합니다.

| 행성 | Default 논문 | 발견 논문인가. |
|---|---|---|
| GJ 179 b | Howard et al. 2010 | 예 — 발견 논문 |
| GJ 1132 b | Xue et al. 2024 | 아니오 — 재분석 (발견은 2015년) |
| GJ 1132 c | Wang et al. 2026 (preprint) | 예 — 발견 논문 |
| GJ 581 b, c, e | Vincenzi et al. 2024 (또는 유사한 2024 A&A) | 아니오 — 전체 시스템 재분석 |

NASA의 default는 맥락에 따라 다릅니다 — 때로는 발견 논문, 때로는 가장 최근의 재분석입니다. 둘 다 유효한 Phase 1 출처입니다. 이전의 `pscomppars` 일괄 채우기는 이를 불분명하게 만들었지만, `ps`는 이를 명확히 드러냅니다.
