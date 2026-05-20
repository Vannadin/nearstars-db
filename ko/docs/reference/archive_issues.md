# NASA Exoplanet Archive 데이터 이슈

SIMBAD/Gaia DR3 교차 검증 중 발견된 문제들입니다 (2026-05-16).
연락처. exoplanetarchive@ipac.caltech.edu

---

## 이슈 1: GJ 411 — 오래된 거리 값, Gaia DR3 링크 누락

**테이블.** pscomppars  
**필드.** sy_dist, gaia_dr3_id

| 필드 | Archive 값 | 정확한 값 | 출처 |
|-------|--------------|---------------|--------|
| sy_dist | 5.676 pc (18.5 ly) | 2.546 pc (8.3 ly) | SIMBAD plx 392.75 mas |
| gaia_dr3_id | NULL | 존재해야 함 | Lalande 21185 / HD 95735 |

Archive의 거리 값은 Gaia 이전 측정값으로 아직 업데이트되지 않은 것으로 보입니다.
GJ 411 (Lalande 21185 / HD 95735)은 5번째로 가까운 항성계이며 Gaia DR3 관측 범위 내에 있습니다.

---

## 이슈 2: GJ 273 — 오래된 거리 값, Gaia DR3 링크 누락

**테이블.** pscomppars  
**필드.** sy_dist, gaia_dr3_id

| 필드 | Archive 값 | 정확한 값 | 출처 |
|-------|--------------|---------------|--------|
| sy_dist | 5.922 pc (19.3 ly) | 3.786 pc (12.4 ly) | SIMBAD plx 264.13 mas |
| gaia_dr3_id | NULL | 존재해야 함 | Luyten's Star / GJ 273 |

GJ 411과 동일한 패턴으로, Gaia 이전 거리 값이 그대로 남아 있고 Gaia DR3 교차 대응이 없습니다.

---

## 이슈 3: VHS J125601.92-125723.9 — Archive와 Gaia DR3 간 거리 충돌

**테이블.** pscomppars  
**필드.** sy_dist

| 출처 | 거리 |
|--------|----------|
| Archive sy_dist | 12.7 pc (41.4 ly) — 측광 추정값 |
| Gaia DR3 시차 | 47.27 mas → 21.15 pc (69.0 ly) |

차이(8.45 pc)는 이 프로젝트에서 사용하는 50 ly 선별 경계를 초과합니다.
참고. VHS J125601.92-125723.9는 M7.5 갈색왜성으로, 매우 붉은 천체(bp_rp = 4.46, G = 15.1)이므로
Gaia 광학 시차의 신뢰도가 낮을 수 있습니다.
독립적인 적외선 시차 측정으로 이 충돌을 해소할 수 있을 것입니다.

---

## 이슈 4 (TEPCat): TRAPPIST-1 d — 질량이 10배 과다 계상

**출처.** https://www.astro.keele.ac.uk/jkt/tepcat/allplanets-csv.csv  
**필드.** M_b (Mjup), 열 인덱스 26  
**발견.** 2026-05-18, NASA Exoplanet Archive와 교차 검증 중

| 출처 | 값 | 참고 문헌 |
|--------|-------|-----------|
| TEPCat allplanets-csv | 0.0122 Mjup = 3.8775 M⊕ | 2021PSJ.....2....1A |
| NASA Exoplanet Archive | 0.00122 Mjup = 0.388 M⊕ | 같은 논문 |

나머지 TRAPPIST-1 행성들(b, c, e, f, g, h)은 두 출처 간 1% 이내로 일치합니다.
차이가 정확히 10배라는 점은 TEPCat 데이터 입력 시 소수점 아래 0 하나가 누락된 것과 일치합니다
(`0.00122` 대신 `0.0122`). 두 출처 모두 Agol et al. 2021 (2021PSJ.....2....1A)을 인용합니다.

TEPCat 수정 문의. https://www.astro.keele.ac.uk/jkt/tepcat/

---

## 이슈 5 (내부 데이터 갭): mass 값이 없는 14개 별

**2026-05-20 기준.** 다음 컴포넌트들은 `stellar_props_curated.json` 에 mass 측정값이 없습니다 (SIMBAD `mesMass` 테이블도 자동 fetch 되지 않음 — `fetch_stellar_props.py` 가 해당 테이블을 쿼리하지 않기 때문. `docs/reference/methodology.md` "Known limits" 참조). JSON 파일은 `principia.gravitational_parameter_km3_s2 = null` 로 빌드되며, 이 때문에 `principia-cfg` 스킬이 Principia 패치 emit 을 중단합니다 (스킬이 해당 별 목록과 함께 명시적 에러로 abort).

```
36 Ophiuchi A / B / C
40 Eridani A / B / C
Beta Hydri
Chi-1 Orionis A
Delta Pavonis
GJ 163
Mu Herculis A
Ross 458
Sigma Draconis
Zeta Tucanae
```

**해결 경로.** (a) 별 단위 문헌 mass 값을 `stellar_props_curated.json` 에 method + bibcode 와 함께 큐레이션, 또는 (b) `scripts/pipeline/dev_backfill_spt_mass.py` (principia-cfg 스킬의 일회성 헬퍼) 출력을 Curation Phase 1 폴백으로 수용. `.claude/skills/principia-cfg/checklist.md` "Open / deferred" 에서 추적 중.

---

## 발견 경위

쿼리. `SELECT hostname, sy_dist, gaia_dr3_id FROM pscomppars WHERE sy_dist <= 15.307`

반환된 각 시스템을 다음과 교차 검증했습니다.
- Gaia DR3 TAP (gaiadr3.gaia_source, gaia_dr3_id로 매칭)
- SIMBAD TAP (basic 테이블, plx_value)

gaia_dr3_id가 NULL인 시스템은 SIMBAD 측성으로 폴백했으며,
이를 통해 GJ 411과 GJ 273의 거리 불일치가 드러났습니다.
