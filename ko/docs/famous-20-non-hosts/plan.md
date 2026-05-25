# 50광년 이내 유명 비행성 호스트 20개 — 계획

## 범위

50광년 이내의 가장 유명한 비행성 호스트 별 객관적 상위 20개. DB에 이미 있는 것은 재조사하고, 없는 것은 새로 추가합니다.

## 20개 목록 (밝기 + 역사 + 문화 + 과학적 중요성 기준 객관적 선정)

### 이미 DB에 있음 → 재조사 (12개 컴포넌트)

| # | 별 | 유명한 이유 | 현재 큐레이션 상태 |
|---|---|---|---|
| 1 | Sirius A | 밤하늘에서 가장 밝은 별 | unverified — 일괄 채우기 |
| 2 | Sirius B | 최초로 발견된 백색왜성 | unverified |
| 3 | α Cen A | 가장 가까운 항성계 (Proxima의 동반성) | binary_orbit Pourbaix 2016 (PRESERVED) |
| 4 | α Cen B | 동일 | binary_orbit Pourbaix 2016 (PRESERVED) |
| 5 | Vega | 측광 표준성 | unverified |
| 6 | Altair | 여름 대삼각형 | unverified |
| 7 | Fomalhaut | α PsA, 잔해 원반 | unverified |
| 8 | 61 Cygni A | Bessel의 첫 시차 측정 (1838) | unverified |
| 9 | 61 Cygni B | 동일 | unverified |
| 10 | Kapteyn | 헤일로 준왜성, 빠른 고유운동 | unverified Anglada-Escude 2014 |
| 11 | Eta Cassiopeiae A | Achird, 육안 이중성 | unverified |
| 12 | Eta Cassiopeiae B | 동일 | unverified |

### 새로 추가 (8개 컴포넌트)

| # | 별 | 유명한 이유 | 접근 방식 |
|---|---|---|---|
| 13 | Arcturus | 4번째로 밝은 별, K형 거성 | 단일, SIMBAD 천체측정, HIPPARCOS_V |
| 14 | Capella | 6번째로 밝은 별, 근접 이중성 | 단일 항목 (Aa+Ab 동역학적 병합) |
| 15 | Procyon A | 8번째로 밝은 별, α CMi | B와 이중성, SIMBAD 천체측정 |
| 16 | Procyon B | 전형적인 백색왜성 동반성 | 동일 이중성 |
| 17 | Wolf 359 | 스타트렉/SF 팬덤 명성 | 단일, Gaia 확인 |
| 18 | 70 Ophiuchi A | Bessel의 이중성, 역사적 의의 | B와 이중성, Gaia 확인 |
| 19 | 70 Ophiuchi B | 동일 | 동일 이중성 |
| 20 | Van Maanen's Star | 최초의 고립 백색왜성 (1917) | 단일, Gaia 확인, SIMBAD alias "Wolf 28" |

## 접근 방식

### 8개 신규 추가

1. `target_list.json` — 5개 시스템 항목 추가: Arcturus, Capella, Procyon (A+B), Wolf 359, 70 Ophiuchi (A+B), Van Maanen's Star
2. `fetch_photometry.py HIPPARCOS_V` — Arcturus (-0.05), Capella (0.08), Procyon B (10.92) 추가
3. `fetch_stellar_props.py SIMBAD_ALIASES` — Van Maanen's Star → "Wolf 28"
4. `stellar_props_curated.json` — 컴포넌트별 질량 + 반지름 + spectype, 논문 출처 표기 포함
5. `binary_orbits.json` — Procyon (Bond et al. 2017), 70 Ophiuchi (Pourbaix orb6 grade 2)
6. `./run_pipeline.sh` 실행 (새 별에 대한 신규 조회 필요)

### 12개 기존 별 재조사

파이프라인에 이미 데이터가 있으므로 가벼운 방식으로 진행합니다.
- 현재 curated `method`와 `bibcode` 확인
- method="unverified"인 경우, 권위 있는 논문 탐색 시도 (Boyajian 2012/2013의 간섭계 반지름, FGK 별은 Stassun TICv8 2019, M형 별은 Mann 2015)
- 적절한 method 레이블 + bibcode + DOI로 항목 업데이트
- α Cen A/B 보존 (Pourbaix 2016이 이미 최적)

## 성공 기준

- 20개 컴포넌트 전체에 대해.
  - `principia.gravitational_parameter_km3_s2` != null
  - `principia.mean_radius_km` != null
  - 적절한 `method` (not "unverified")와 bibcode를 가진 질량 측정값 최소 1개
- `validate.py` FAIL 0
- `db/systems/`에 8개의 새 시스템 파일 존재
- target_list.json이 136 → 141 시스템으로 증가

## Related

- [methodology hub](../../docs/reference/methodology.md) — 이 워크스페이스가 기여하는 상위 토픽.
