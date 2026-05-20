# NearStars 데이터베이스에 별 추가하기

새로운 별(또는 별 구성 요소)을 파이프라인에 추가하는 방법을 설명합니다.

> **범위.** 이 문서는 별 추가 시 다루는 파일들에 대한 **필드/스키마 레퍼런스**입니다 — 각 키의 의미, 값을 얻는 방법, 파이프라인 스크립트의 동작, 별 단위 알려진 예외. 해당 사실들의 정본입니다.
>
> 에이전트 주도 별 추가 워크플로우 — Phase 1 / Curation Phase 2 격상, 한국어 트리거 문구, 판단 사항 (이중성 vs 단일성, SIMBAD 별칭 선택 등) — 은 **`nearstars-add-star` 스킬**을 호출하십시오. 스킬이 워크플로우를 주도하고, 이 문서는 스킬 (혹은 수동 작업자) 이 편집하는 데이터 형태를 정의합니다.

---

## 개요

파이프라인은 단일 입력 파일 `db/target_list.json`에 의해 구동됩니다.
별을 추가한다는 것은 해당 파일에 항목 하나를 추가한 뒤 파이프라인을 다시 실행하는 것을 의미합니다.

```
db/target_list.json
       │
       ├─ fetch_astrometry.py    → db/astrometry_raw.json
       ├─ fetch_photometry.py    → db/photometry_raw.json
       ├─ fetch_stellar_props.py → db/stellar_props_raw.json
       └─ fetch_planets.py       → db/planets_raw.json
                    │
               build_systems.py  → db/systems/<name>.json
                    │
              build_site.py      → docs/data.json
```

---

## 호스트명 규칙

- 모드에서 천체로 등장하는 **별 구성 요소** 하나당 항목 하나를 작성합니다.
- 다중 구성 요소 시스템은 여러 구성 요소를 하나의 항목으로 묶습니다.
  `"Alpha Centauri A"`, `"Alpha Centauri B"` → 단일 항목, `binary: true`.
- 단독 별의 경우. `"Vega"`, `"Altair"`.
- `build_systems.py`의 `to_filename()` 함수가 이름을 파일명으로 변환합니다.
  소문자로 변환, 아포스트로피 제거, 영숫자 이외의 문자는 `_`로 대체, 양쪽 끝 정리.
  예시. `"Chi-1 Orionis A"` → `chi_1_orionis_a.json`.

---

## 1단계 — `db/target_list.json`에 추가하기

배열 끝에 항목을 추가합니다.

```json
{
  "system": "New Star",
  "components": ["New Star"],
  "gaia_source_ids": ["1234567890123456789"],
  "hip_ids": [],
  "binary": false
}
```

필드 설명.

| 필드 | 값을 얻는 방법 |
|---|---|
| `system` | 표준 시스템 이름 (단독 별의 경우 호스트명과 동일) |
| `components` | 시스템 내 구성 요소 호스트명 목록 |
| `gaia_source_ids` | Gaia DR3 `source_id` — [Gaia Archive](https://gea.esac.esa.int/archive/) 또는 SIMBAD에서 조회. 구성 요소 순서와 동일하게 ID를 하나씩 입력. 없으면 `null` 사용. |
| `hip_ids` | 알고 있는 경우 Hipparcos ID — 선택 사항, 파이프라인에서 사용하지 않음 |
| `binary` | `db/binary_orbits.json`에 상호 궤도가 있는 시스템이면 `true` |
| `stellarium_ids` | `fetch_stellarium_ids.py`가 _자동으로 채움_. `{컴포넌트 이름 → Stellarium Web skysource_id}` 형태. 수동 편집 불필요. |

쌍성계의 경우 구성 요소를 모두 나열합니다.

```json
{
  "system": "New Binary",
  "components": ["New Binary A", "New Binary B"],
  "gaia_source_ids": ["111...", "222..."],
  "hip_ids": [12345, 12346],
  "binary": true
}
```

---

## 2단계 — `db/stellar_props_curated.json`에 항성 물성 추가하기

`fetch_stellar_props.py`는 SIMBAD에서 spectype, Teff, 간섭계 반지름을 자동으로 가져와
`stellar_props_raw.json`에 저장합니다(실행할 때마다 덮어씀).
질량 측정값과 정밀 문헌 반지름은 `stellar_props_curated.json`에 수동으로 추가해야 하며,
이 값들은 `build_systems.py`에서 raw 값보다 우선 적용됩니다.

구성 요소 호스트명을 키로 하여 항목을 추가합니다.

```json
"New Star": {
  "teff_k": 5500,        ← 선택 사항. 생략하면 SIMBAD 값을 사용
  "spectype": "G5 V",    ← 선택 사항. 생략하면 SIMBAD 값을 사용
  "mass_measurements": [
    {
      "value_msun": 0.92,
      "uncertainty_msun": 0.03,
      "method": "spectroscopic",
      "reference": "Author et al. (2020)",
      "bibcode": "2020ApJ...000..000A",
      "doi": "10.xxxx/...",
      "recommended": true
    }
  ],
  "radius_measurements": [
    {
      "value_rsun": 0.88,
      "uncertainty_rsun": 0.02,
      "method": "interferometry",
      "reference": "Author et al. (2020)",
      "bibcode": "2020ApJ...000..000A",
      "doi": "10.xxxx/...",
      "recommended": true
    }
  ]
}
```

최소한 질량과 반지름 측정값 각각 하나에 `recommended: true`를 설정해야 합니다.
이 값들은 출력 JSON의 `principia.gravitational_parameter_km3_s2`와
`principia.mean_radius_km` 필드를 계산하는 데 사용됩니다.

---

## 3단계 — Gaia를 사용할 수 없는 경우 vmag_v 처리하기

`fetch_photometry.py`는 Gaia G + BP-RP로부터 V 등급을 자동으로 계산합니다.
Gaia ID가 없는 별(예. 갈색왜성, Gaia 포화 밝은 별)의 경우
`fetch_photometry.py`의 `HIPPARCOS_V`에 V 등급을 직접 추가합니다.

```python
HIPPARCOS_V = {
    ...
    "New Star": 5.23,  # source: Hipparcos HIP 12345
}
```

광학 V 등급이 존재하지 않는 경우(Y형 왜성 같은 적외선 전용 천체),
생략해도 됩니다. 출력에서 `vmag_v: null`은 허용됩니다.

---

## 4단계 — 쌍성 궤도 처리하기 (해당하는 경우)

새 시스템이 중력으로 묶인 쌍성이라면 상호 궤도를 `db/binary_orbits.json`에 추가하고
`db/target_list.json`에서 `binary: true`로 설정합니다.

기존 항목(예. Alpha Centauri, Sirius)을 참고하여 스키마를 확인하세요.
자동 fetch는 없습니다. 공개된 궤도 해는 형태가 다양하고(시각 궤도 요소, 역표 파일, RV 피팅)
개별 큐레이션이 필요하기 때문에 `binary_orbits.json`은 수동으로 관리합니다.
`build_systems.py`는 관련 항목을 대표 구성 요소 파일에 자동으로 포함시킵니다.

---

## 5단계 — 파이프라인 재실행하기

```bash
cd /path/to/project
python3 scripts/pipeline/fetch_astrometry.py
python3 scripts/pipeline/fetch_photometry.py
python3 scripts/pipeline/fetch_stellar_props.py
python3 scripts/pipeline/fetch_planets.py
python3 scripts/pipeline/fetch_stellarium_ids.py
python3 scripts/pipeline/build_systems.py
python3 scripts/pipeline/validate.py
python3 scripts/pipeline/build_site.py
```

또는 편의 스크립트를 사용합니다.

```bash
./run_pipeline.sh
```

위 블록의 다섯 개 fetch 스크립트(1~5단계)는 독립적으로 실행되며 어떤 순서로도, 또는 병렬로 실행할 수 있습니다.

---

## 검증

`build_systems.py` 실행 후.
- `db/systems/<new_name>.json`이 생성되었는지 확인합니다.
- `stars[0].raw`에서 측성값, `stars[0].principia`에서 질량/반지름을 확인합니다.

`validate.py` 실행 후.
- FAIL이 0개여야 합니다. Gaia 미등록 별의 경우 vmag_v 누락 WARN은 허용됩니다.

`build_site.py` 실행 후.
- 브라우저에서 `docs/index.html`을 열고 새 별을 검색합니다.

---

## 알려진 예외 사항

| 별 | 이슈 |
|---|---|
| WISEP J121756.91+162640.2 A | SIMBAD 이름 불일치 — 실제 SIMBAD ID는 `WISE J121756.90+162640.8`. 측성 fetch 실패. 파일을 수동으로 패치함. |
| CWISEP J193518.59-154620.3 | Y형 왜성 — Gaia ID 없음, 광학 V 등급 없음. principia radius 누락 (예상된 상황). |
| GJ 273, GJ 411, HD 62509 | Gaia ID 없음 — V 등급은 `HIPPARCOS_V`에 하드코딩. |

---

## 파이프라인 스크립트

`run_pipeline.sh` 가 순서대로 실행하는 8개 스크립트.

| 스크립트 | 역할 |
|---|---|
| `fetch_astrometry.py` | Gaia DR3 TAP 배치 쿼리 + 밝은 포화 별에 대한 SIMBAD 폴백 |
| `fetch_photometry.py` | Gaia G+BP-RP → V 등급 변환. 밝은 별은 하드코딩된 Hipparcos V 사용 |
| `fetch_stellar_props.py` | SIMBAD. spectype, Teff, mesDiameter → R☉. 질량은 `stellar_props_curated.json`에서 가져옴 |
| `fetch_planets.py` | NASA Exoplanet Archive TAP → 행성 궤도 및 물리적 특성 |
| `fetch_stellarium_ids.py` | Stellarium Web API → 컴포넌트별 skysource ID 조회 (idempotent. 이미 채워진 항목은 건너뜀) |
| `build_systems.py` | 모든 raw + curated 파일 병합 → B1950 + J2000 에포크 전파 → systems/*.json |
| `validate.py` | 필수 필드, 에포크 일관성, vmag_v 존재 여부 확인 |
| `build_site.py` | systems/*.json → docs/data.json |

### 보조 스크립트 (`run_pipeline.sh` 미포함)

Curation Phase 1 배치와 일회성 유지보수에 수동으로 실행.

| 스크립트 | 역할 |
|---|---|
| `fetch_planets_ps.py` | NASA `ps` 테이블 (`default_flag=1` per-paper 행) fetch. `build_curated_from_ps.py` 의 입력. |
| `build_curated_from_ps.py` | `planets_ps_default.json` 으로부터 per-paper bibcode/DOI attribution 가진 `db/planets_curated.json` 생성. |
| `generate_target_list.py` | 유틸리티. `db/systems/` 에서 `target_list.json` 재생성. |
| `schema.py` | `validate.py` 가 import 하는 공용 validator 모듈. 직접 실행 불가. |
| `test_hierarchical.py` | `build_systems.py` 의 계층적 (3중성계) 궤도 리졸버에 대한 합성 fixture 단위 테스트. |

## 외부 API

| API | 엔드포인트 | 사용 목적 |
|---|---|---|
| Gaia DR3 TAP | gea.esac.esa.int/tap-server | 측성, 측광 |
| SIMBAD TAP | simbad.u-strasbg.fr/simbad/sim-tap | 밝은 별 폴백, mesDiameter, spectype, Teff |
| NASA Exoplanet Archive | exoplanetarchive.ipac.caltech.edu/TAP | 행성 데이터 |
| VizieR WDS TAP | tapvizier.cds.unistra.fr | 쌍성 교차 검증 (binary_orbits 전용) |
