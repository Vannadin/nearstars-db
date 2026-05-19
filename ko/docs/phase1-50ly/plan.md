# Phase 1 큐레이션 — 50광년 이내 행성 호스트 전체 (계획)

스킬 검증 테스트가 2026-05-19에 트리거되었습니다. 리셋 커밋 `1f023d0`은 이전의 `pscomppars` 일괄 채우기를 제거했으며, 해당 작업은 논문별 출처 표기 정책([[feedback-planet-curation]])을 위반했습니다.

## 목표

DB에 현재 등록된 50광년 이내의 모든 행성 호스트(121개 호스트, 223개 확인된 행성)에 대해, `db/planets_curated.json`에 논문 출처가 명기된 항목과 `db/stellar_props_curated.json`에 해당 호스트의 질량/반지름 항목을 생성합니다. 각 측정값에는 명시적인 `bibcode`와 (가능한 경우) `doi`가 포함됩니다. 파이프라인 재빌드 결과 `validate.py`에서 FAIL 0이 나와야 합니다.

## 이전 시도가 잘못된 이유

`fetch_planets.py`는 `pscomppars`(복합 파라미터) 테이블을 쿼리하여 행성별로 `disc_refname`(발견 논문 참조)을 저장합니다. `pscomppars`의 값은 NASA가 여러 논문을 병합하여 최선 추정으로 만든 것으로, 발견 논문이 질량/반지름/공전주기 값의 실제 출처인 경우는 드뭅니다. 이전 일괄 채우기는 `disc_refname`을 모든 파라미터의 출처인 것처럼 기록했습니다. 이는 사용자가 금지한 "Phase 0.5" 지름길에 해당합니다.

## 올바른 Phase 1 워크플로

1. 각 행성에 대해 NASA Exoplanet Archive `ps` 테이블(논문별 행)을 쿼리하고 `default_flag = 1`로 필터링합니다. NASA는 해당 행성에 대해 현재 권위 있다고 판단하는 논문 하나를 default로 표시합니다.
2. 해당 행의 파라미터 값과 `pl_refname`을 함께 가져옵니다. `pl_refname`이 그 특정 값들의 출처입니다.
3. `pl_refname` HTML 링크에서 bibcode를 추출합니다 (`<a refstr=... href=https://ui.adsabs.harvard.edu/abs/{bibcode}/abstract>` 형식으로 이미 포함되어 있음).
4. WebFetch로 bibcode가 ADS에서 확인되는지 검증합니다 (일괄 실행에서는 표본 검사, PoC에서는 전수 검사).
5. 가능한 경우 bibcode를 DOI로 변환합니다 (ADS 초록 페이지에 DOI가 포함됨).
6. 값 + bibcode + doi가 명시된 `planets_curated.json` 항목을 작성합니다.
7. 호스트 질량/반지름의 경우, `stellar_props_raw.json` 측정값 배열에서 동일한 패턴을 따릅니다 — 많은 항목에 bibcode가 이미 있으며, 단지 curated로 승격시키기만 하면 됩니다.

## 접근 방식

PoC를 먼저 진행(대표 호스트 2-3개)한 후 전체 일괄 처리합니다.

- **PoC 호스트:** GJ 179 (RV, 단일), GJ 581 (RV, 다중 행성), GJ 1132 (transit + RV 혼합).
- PoC 이후: fetch 스크립트를 확장하여 `ps` 테이블 행을 가져오도록 하면, 223개 행성에 대해 기계적으로 처리할 수 있습니다.
- 일괄 실행 후 validate 수행.

## 범위 외

- Phase 2 (전체 문헌 조사) — 시스템별 사용자 요청 시에만 트리거됩니다.
- 천체측정 / 측광 / SIMBAD 재조회 (이미 캐시되어 안정적임).
- Kopernicus / Principia cfg 생성 (다운스트림 스킬).
- 행성 없는 별 (DB의 21개 호스트) — 현재 큐레이션 수준 유지. Phase 1은 행성 호스트 전용입니다.

## 성공 기준

- `db/planets_curated.json`: 223개 행성 항목, 각각 `bibcode` 포함.
- `db/stellar_props_curated.json`: 최소 121개 항목 (기존 고품질 3개 + 신규 최소 118개).
- `validate.py`: FAIL 0. WARN 수는 이전 일괄 채우기 기준선(52)과 비슷하거나 더 적어야 합니다.
- 행성별로: 출처에 해당 값이 있는 경우 `derived.semi_major_axis_m`, `mass_kg` 채워짐.
- 출처 표기: `pscomppars`를 출처로 가리키는 항목 없음.
