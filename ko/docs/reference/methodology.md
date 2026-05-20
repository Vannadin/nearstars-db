# 항성계 데이터 조사 방법론

이 문서는 공개 천문 카탈로그를 출처로 삼아 항성 및 행성 데이터의 구조화된 JSON 데이터베이스를
구축하는 워크플로를 정의합니다.
데이터베이스는 두 개의 하위 소비자에게 공급됩니다. 각각 별도 세션 또는 에이전트에서 작성되는
Principia proto 파일과 Kopernicus cfg 파일입니다.

---

## 목표

항성계당 JSON 파일 하나. 각 파일에는 다음이 포함됩니다.
- 출처 카탈로그로부터 받은 그대로의 원시 관측값
- Principia 및 Kopernicus에 바로 사용할 수 있도록 변환된 파생값
- 완전한 출처 정보: 소스명, 카탈로그 ID, 취득일, 에포크

데이터베이스는 유일한 진실의 원천입니다. 하위 에이전트가 외부 카탈로그를 직접 조회하거나
독립적으로 단위 변환을 수행할 필요가 없어야 합니다.

---

## 출력 구조

```
db/
  target_list.json            # 파이프라인 입력
  astrometry_raw.json         # 자동 fetch — Gaia DR3 + SIMBAD
  photometry_raw.json         # 자동 fetch — Gaia DR3
  stellar_props_raw.json      # 자동 fetch — SIMBAD (Teff, 스펙형, mesDiameter)
  stellar_props_curated.json  # 수동 입력 — 질량/반지름 정밀 문헌값
  planets_raw.json            # 자동 fetch — NASA Exoplanet Archive
  planets_curated.json        # 수동 입력 — 궤도/환경/대기 상세 문헌값
  binary_orbits.json          # 수동 입력 — 쌍성 궤도
  systems/
    alpha_centauri_a.json
    barnards_star.json
    tau_cet.json
    ...                       # 항성 컴포넌트별 1파일
  backups/                    # 이전 스냅샷 보관 (수동 백업 시점)
```

파이프라인 실행 순서, 스크립트 설명, 새 별 추가 절차는 [`adding_stars.md`](adding_stars.md) 참조.

---

## JSON 스키마

### 최상위 수준

```json
{
  "system_name": "Alpha Centauri A",
  "stars": [ ... ],
  "planets": [ ... ],
  "sources": [ ... ],
  "meta": { ... }
}
```

JSON 파일은 시스템 단위가 아닌 **항성 컴포넌트** 단위로 작성합니다. `system_name`은
컴포넌트 이름과 일치합니다 (예: `Alpha Centauri A`, `Alpha Centauri B`,
`Proxima Centauri`는 각각 별도 파일). `stars` 배열에는 항상 정확히 하나의 항목이
담깁니다 — 해당 파일이 기술하는 컴포넌트입니다. 이중성/다중성계의 상호 궤도 데이터는
`binary_orbits.json`에 저장되며, 대표 컴포넌트 파일(일반적으로 `A`)에 임베드됩니다.
형제 컴포넌트는 `binary_orbit_ref`를 통해 이를 참조합니다.

이 선택은 하위 Kopernicus/Principia cfg 작성자가 데이터를 소비하는 방식을 반영합니다.
각 `CelestialBody`(단일 별)가 cfg `Body { }` 노드와 1:1로 대응하기 때문에,
컴포넌트별 파일 구조를 사용하면 cfg 생성 시 인덱싱이 필요 없습니다.

### `meta`

```json
{
  "retrieval_date": "2026-05-16",
  "solar_system_epoch_jd": 2433282.5,
  "solar_system_epoch_label": "B1950.0",
  "game_epoch_jd_sol": 2433647.5,
  "game_epoch_jd_rss": 2433647.5,
  "coordinate_origin": "SSB",
  "coordinate_frame": "ICRF",
  "coordinate_units": "km, km/s",
  "notes": ""
}
```

`solar_system_epoch_jd`는 모든 상태 벡터가 표현되는 에포크입니다.
Sol과 RSS 모두 `solar_system_epoch`으로 **JD2433282.5** (명목상 B1950.0, 1950-01-01 TDB)를
사용합니다. JPL Horizons 조회 시 이 값과 일치시켜야 합니다.

참고: 엄밀히 말하면 Besselian 에포크 B1950.0 = JD2433282.423이며, JD2433282.5는
1950-01-01.0 TT 자정으로 약 1.85시간 차이가 납니다. Sol과 RSS 모두 관례적으로
2433282.5를 사용하며, JPL Horizons도 이 날짜를 직접 수락합니다.
B1950.0을 정밀하게 계산하는 소프트웨어와 교차 검증하는 경우에는 알아둘 만한 차이지만,
KSP 목적으로는 무시할 수 있는 수준입니다.

`game_epoch_jd`는 상태 벡터에 영향을 주지 않습니다. Sol과 RSS는 동일한 값을 사용합니다.
- Sol: `JD2433647.5`
- RSS: `JD2433647.5`

좌표 원점은 태양이 아닌 **태양계 무게중심(SSB)** 입니다.
태양 자체는 이 파일들에서 SSB로부터 약 10⁵ km 떨어진 위치에 있습니다.
모든 상태 벡터는 동일한 SSB-ICRF 기준계로 표현되어야 합니다.

---

### `stars[]`

`stars` 배열의 길이는 항상 1입니다 — 해당 파일이 기술하는 단일 컴포넌트입니다.
(이중성/다중성계는 컴포넌트별로 파일을 분리합니다. 위의 "최상위 수준" 참조.)

```json
{
  "name": "Alpha Centauri A",
  "component": "A",

  "raw": {
    "source": "Gaia DR3",
    "source_id": "5853498713160606720",
    "epoch_jd": 2457389.0,
    "epoch_label": "J2016.0",
    "ra_deg": 219.90085,
    "dec_deg": -60.83562,
    "parallax_mas": 742.12,
    "parallax_error_mas": 1.40,
    "pmra_mas_yr": -3678.19,
    "pmdec_mas_yr": 481.84,
    "radial_velocity_km_s": -22.4,
    "radial_velocity_source": "Gaia DR3",

    "vmag_v": -0.01,
    "vmag_source": "hipparcos_hardcoded",

    "teff_k": 5790,
    "spectype": "G2 V",

    "mass_measurements": [
      {
        "value_msun": 1.1055,
        "uncertainty_msun": 0.0039,
        "method": "binary_orbit",
        "reference": "Pourbaix et al. 2002",
        "doi": "10.1051/0004-6361:20021249",
        "recommended": true
      },
      {
        "value_msun": 1.100,
        "uncertainty_msun": 0.006,
        "method": "evolutionary_model",
        "reference": "Thevenin et al. 2002",
        "doi": "10.1051/0004-6361:20021791",
        "recommended": false
      }
    ],

    "radius_measurements": [
      {
        "value_rsun": 1.2234,
        "uncertainty_rsun": 0.0053,
        "method": "interferometry",
        "reference": "Kervella et al. 2017",
        "doi": "10.1051/0004-6361/201629505",
        "recommended": true
      },
      {
        "value_rsun": 1.227,
        "uncertainty_rsun": 0.005,
        "method": "evolutionary_model",
        "reference": "Thevenin et al. 2002",
        "doi": "10.1051/0004-6361:20021791",
        "recommended": false
      }
    ]
  },

  "derived": {
    "epoch_jd": 2433282.5,
    "epoch_label": "B1950.0",
    "propagation_method": "linear",
    "distance_pc": 1.3475,
    "distance_km": 4.153e+13,
    "icrs_x_km":  2.634e+13,
    "icrs_y_km": -3.197e+13,
    "icrs_z_km": -1.272e+13,
    "icrs_vx_km_s": 1.3204,
    "icrs_vy_km_s": -4.4012,
    "icrs_vz_km_s":  0.8913,
    "position_ulp_km": 5.9e-3,
    "icrs_x_j2000_km":  2.557e+13,
    "icrs_y_j2000_km": -3.127e+13,
    "icrs_z_j2000_km": -1.255e+13,
    "icrs_vx_j2000_km_s": 1.3204,
    "icrs_vy_j2000_km_s": -4.4012,
    "icrs_vz_j2000_km_s":  0.8913
  },

  "principia": {
    "gravitational_parameter_km3_s2": 146713602439.899,
    "mean_radius_km": 851119.4
  }
}
```

`derived`에 관한 참고사항.
- 모든 단위는 Principia/Sol 관례를 따릅니다. **km** 및 **km/s**.
- `propagation_method: "linear"`는 일정한 공간 속도(고유운동 + 시선 속도)로
  위치를 전파했음을 의미합니다. KSP 시간 규모(수십~수백 년)에서 항성 섭동체에 적합합니다.
- `position_ulp_km`은 `abs(largest_coordinate_km) * 2^-52`입니다. Alpha
  Centauri(~4e13 km)의 경우 약 0.009 km (9 m)으로, 중력 섭동체로서는 허용 가능한
  수준이지만 별 주변의 근거리 궤도 역학에는 부적합합니다.
- 좌표 원점은 태양이 아닌 **SSB**입니다. 이 파일들에서 태양 자체는 SSB로부터
  약 10⁵ km 떨어진 위치에 있습니다.

`mass_measurements` 및 `radius_measurements`에 관한 참고사항.
- 공개된 모든 값을 개수에 관계없이 배열에 넣습니다.
- `recommended: true`는 `principia` 블록에서 사용하는 값을 표시합니다.
  각 배열에서 정확히 하나의 항목만 `recommended: true`를 가져야 합니다.
- `recommended` 우선순위는 출판일이나 저널 권위가 아닌 측정 방법으로 결정됩니다.
  방법 계층 구조는 다음과 같습니다.

  질량:
  1. `binary_orbit` — 직접 역학적 측정, 가장 신뢰성 높음
  2. `asteroseismology` — 모델 의존적이나 잘 제약됨
  3. `evolutionary_model` — 간접적; 더 나은 방법이 없을 때만 사용
  4. `spectroscopic` / `spectroscopic_calibration` — 스펙트럼 피팅 기반
  99. `unverified` — Curation Phase 1 batch에서 method 검증 안 함; 항상 최하위로 처리. 출처(bibcode)는 정확하나 paper가 실제 어떤 방법을 썼는지는 미검증.

  반지름:
  1. `interferometry` — 직접 각지름 측정
  2. `eclipsing_binary` — 직접 기하학적 측정
  3. `sed_fitting` — 볼로메트릭 플럭스 + Teff + 거리 (준직접적)
  4. `evolutionary_model` — 간접적; 더 나은 방법이 없을 때만 사용
  99. `unverified` — Curation Phase 1 batch 동일 의미.

  허용되는 method 라벨의 전체 화이트리스트는 `scripts/pipeline/schema.py STELLAR_ALLOWED_METHODS` 에 정의되어 있습니다. 위 계층은 실제 사용 라벨의 우선순위만 정렬하며, 신규 method 추가 시 두 곳을 모두 갱신해야 합니다.

- 두 항목이 동일한 방법 계층을 공유한다면 분수 불확도가 더 작은 것을 선택합니다.
  선택 근거는 `meta.notes`에 기록합니다.

---

### `planets[]`

확인된 행성은 각각 별도의 항목으로 등록합니다.

```json
{
  "name": "Proxima Centauri b",
  "host_star": "Proxima Centauri",

  "raw": {
    "pl_name": "Proxima Cen b",
    "reference": "Anglada-Escude et al. 2016",
    "retrieval_date": "2026-05-16",
    "period_days": 11.1868,
    "period_err_days": 0.0002,
    "semi_major_axis_au": 0.04856,
    "semi_major_axis_err_au": 0.00030,
    "eccentricity": 0.0,
    "inclination_deg": null,
    "inclination_err_deg": null,
    "omega_deg": null,
    "tperi_bjd": null,
    "tperi_err_bjd": null,
    "tranmid_bjd": null,
    "tranmid_err_bjd": null,
    "mass_mearth": 1.27,
    "mass_err_mearth": 0.18,
    "mass_type": "Msini",
    "radius_rearth": null,
    "radius_err_rearth": null,
    "discoverymethod": "Radial Velocity",
    "pl_controv_flag": 0,
    "pubdate": "2016-08",
    "tepcat": null
  },

  "derived": {
    "semi_major_axis_m": 7.265e+09,
    "eccentricity": 0.0,
    "inclination_deg": null,
    "longitude_of_ascending_node_deg": null,
    "argument_of_periapsis_deg": null,
    "mean_anomaly_at_epoch_deg": null,
    "orbital_epoch_jd": null,
    "mass_kg": 7.548e+24,
    "mass_type": "minimum (M sin i)",
    "radius_m": null
  }
}
```

`raw` 블록은 `fetch_planets.py` 출력을 그대로 반영합니다.
- 궤도 필드는 NASA Exoplanet Archive의 `pscomppars` 열 이름을 사용합니다
  (`tperi_bjd`, `tranmid_bjd`, `omega_deg` 등). 근일점 통과 시각(`tperi_bjd`)과
  트랜짓 중점(`tranmid_bjd`) 모두 저장됩니다. 평균 근점 이각의 기준으로
  어느 것을 사용할지는 검출 방법에 따라 다릅니다.
- `tepcat`은 TEPCat이 트랜짓 행성의 질량/반지름을 독립적으로 도출한 경우 채워지는
  중첩 객체입니다. `null`일 수 있습니다.

`derived` 블록은 단위 변환만 수행합니다(AU → m, M⊕ → kg, R⊕ → m).
우선순위 체인은 `curated > tepcat > nasa_archive`입니다. 측정값이 없으면
`null`로 유지합니다 — 기본값 가정(에지온 경사, 원형 이심률, 게임 시작 시 평균 근점 이각)은
DB가 아닌 Kopernicus cfg 생성 단계에서 처리합니다. cfg를 작성하는 하위 에이전트가
이러한 기본값을 선택하고 문서화할 책임을 집니다.

### `sources[]`

조사 과정에서 참고한 모든 논문과 카탈로그를 여기에 기록합니다. 파일의 전체 참고문헌 목록입니다.

```json
[
  {
    "title": "Constraining the difference in convective blueshift between the components of alpha Centauri with precise radial velocities",
    "doi": "10.1051/0004-6361:20021249",
    "bibcode": "2002A&A...394..151P",
    "accessed": "2026-05-16",
    "used_for": ["Alpha Centauri A mass", "Alpha Centauri B mass"]
  },
  {
    "title": "Gaia Data Release 3",
    "doi": null,
    "bibcode": "2023A&A...674A...1G",
    "accessed": "2026-05-16",
    "used_for": ["Alpha Centauri A astrometry", "Alpha Centauri B astrometry"]
  }
]
```

- `doi`와 `bibcode`는 가능한 경우 둘 다 제공합니다. 하나가 없으면 `null`로 설정합니다.
- `used_for`에는 해당 출처에서 가져온 내용을 기록합니다. 참고했지만 사용하지 않은 항목도
  괜찮습니다 — `"used_for": ["consulted; superseded by Pourbaix et al. 2002"]`처럼
  기록하세요.

---

`null` 필드에 관한 참고사항.
- null은 데이터 부재를 의미하며, 0이 아닙니다. DB는 누락된 측정값에 대해 기본값을
  대입하지 않습니다 — 그것은 Kopernicus cfg 작성자의 역할입니다.
- 하위 에이전트는 null을 확인하고, 가정한 기본값(예: RV 전용 검출에서 `inclination = 90 deg`)을
  cfg 자체에 문서화해야 합니다.

---

## 에포크 처리

### 대상 에포크

Sol과 RSS 모두 `solar_system_epoch`으로 **JD2433282.5** (B1950.0, 1950-01-01 TDB)를
사용합니다. `derived`의 모든 상태 벡터는 이 에포크의 SSB-ICRF 좌표로 표현되어야 합니다.

`game_epoch`은 별개이며 상태 벡터에 영향을 주지 않습니다. Sol과 RSS는 동일한 값을 사용합니다.
- Sol: `JD2433647.5`
- RSS: `JD2433647.5`

MM 패치 작성 시 Sol과 RSS 변형은 NEEDS 태그(`SolSystem` vs `RSSConfig`)만 다르며, 에포크 값은 동일합니다.

### 전파가 필요한 이유

Gaia DR3 위치는 **J2016.0** (JD2457389.0)을 기준으로 합니다.
대상 에포크는 JD2433282.5이며, 차이는 약 24,000일(~66년)입니다.

Alpha Centauri(공간 속도 ~25 km/s)의 경우, 66년간의 위치 이동은
~5.2e10 km(~350 AU)입니다. 따라서 전파는 항상 필요합니다.

### 선형 전파

SSB-ICRF에서의 등속(균일 직선) 전파는 Gaia와 Hipparcos가 사용하는 표준 모델입니다.
KSP 관련 시간 규모에서 항성 섭동체에 충분합니다.

선형 전파에서 생략되는 주요 고차 효과는 **투시 가속도(perspective acceleration)** 입니다.
이는 별의 거리가 변함에 따라 나타나는 고유운동 변화율의 겉보기 변화입니다. 대부분의
대상 별에서는 섭동체 정밀도 수준에서 무시할 수 있습니다.

**예외: Barnard's Star** (μ ≈ 10,300 mas/yr, ϖ ≈ 548 mas,
RV ≈ −110 km/s)는 투시 가속도만으로 66년간 약 0.5 AU의 위치 오차가 누적됩니다.
이는 KSP 중력 효과의 섭동체 정밀도 허용 범위 내이므로, 파이프라인은 다른 별들과
동일하게 선형 전파를 적용합니다. 알려진 불일치는 `barnards_star.json`의 `meta.notes`에
기록됩니다. 향후 Barnard's Star에 대해 sub-AU 정밀도가 필요하다면,
JPL Horizons에서 JD2433282.5의 상태 벡터를 직접 가져와 `derived` 블록을
수동으로 덮어쓰세요.

참고문헌.
- Butkevich & Lindegren (2014), A&A 570, A62 — `doi:10.1051/0004-6361/201424483`, `arXiv:1407.4664`
  Gaia 시대의 에포크 전파에 관한 기준 논문. 균일 직선 운동의 엄밀한 폐형식 표현을
  도출하며, Gaia 파이프라인에서 직접 사용됩니다.
- ESA SP-1200 (1997), Vol. 1, Sec. 1.2 (Hipparcos Catalogue, Lindegren et al.)
  Hipparcos 정밀도에서도 1세기 미만의 시간 규모에서 균일 공간 운동이 대부분의
  별에 유효함을 명시합니다.

```python
def propagate_icrs(x0, y0, z0, vx, vy, vz, jd_from, jd_to):
    """
    Linear propagation from jd_from to jd_to.
    Units: km and km/s (matching Principia/Sol convention).
    See Butkevich & Lindegren (2014) Eq. 4-7 for the full derivation.
    """
    dt_s = (jd_to - jd_from) * 86400.0
    return (
        x0 + vx * dt_s,
        y0 + vy * dt_s,
        z0 + vz * dt_s
    )
```

### `propagation_method` 값

| 값 | 의미 | 소스 에포크 |
|---|---|---|
| `"linear"` (Gaia) | Gaia DR3 → 일정 공간 속도 → 대상 에포크 | J2016.0 (JD2457389.0) |
| `"linear"` (SIMBAD) | Gaia 포화 밝은 별에 대한 SIMBAD 폴백 → 선형 전파 | J2000.0 (JD2451545.0) |
| `"kepler_thiele_innes"` | 궤도 결합된 다성계 컴포넌트 → Markley Kepler + Thiele-Innes 회전 (Hilditch 컨벤션) → ICRS 직교 | 궤도 fit 의 카탈로그 에포크. `build_systems.py:solve_orbit_relative` 가 대상 에포크로 전파 |
| `"horizons_direct"` | JPL Horizons 상태 벡터를 JD2433282.5 에서 직접 import — 전파 안 함 | JD2433282.5 (대상 에포크) |

SIMBAD 폴백 경로는 Gaia DR3 ID가 없는 별, 즉 Gaia에서 포화된 밝은 별(V < ~6)인
Alpha Centauri A와 B, Sirius, Procyon, Pollux 등에 적용됩니다. `fetch_astrometry.py`는
SIMBAD의 `basic` 테이블을 조회하며, 해당 천체측정은 J2000.0 기준(Gaia의 J2016.0보다
약 16년 이전)입니다. `raw.epoch_jd` 필드에 실제 소스 에포크가 기록되므로,
`build_systems.py`는 소스에 관계없이 올바르게 전파합니다.

현재 `"horizons_direct"`는 Barnard's Star에만 적용됩니다. 향후 Horizons에서 이용 가능한
별이 있다면 동일한 처리를 평가해야 합니다.

### 에포크 필드 요약

| 필드 | 위치 | 내용 |
|---|---|---|
| `raw.epoch_jd` | 별 | 소스 에포크 — Gaia의 경우 J2016.0, SIMBAD 폴백의 경우 J2000.0 |
| `derived.epoch_jd` | 별 | 대상 에포크 (JD2433282.5) |
| `meta.solar_system_epoch_jd` | 시스템 | JD2433282.5 (Sol과 RSS 공통) |
| `meta.game_epoch_jd_sol` | 시스템 | JD2433647.5 |
| `meta.game_epoch_jd_rss` | 시스템 | JD2433647.5 |
| `raw.tperi_bjd` / `raw.tranmid_bjd` | 행성 | 아카이브 기준 에포크 (근일점 또는 트랜짓 중점) |
| `derived.orbital_epoch_jd` | 행성 | 큐레이션 출처의 에포크 (있는 경우). 없으면 null |

---

## 다중성계 에포크

> 수학적 파이프라인 전체와 워크드 예시(α Cen, Sirius)는
> [`docs/reference/binary-epoch-pipeline.md`](binary-epoch-pipeline.md) 참조.
> 이 섹션은 DB에 영향을 미치는 결정 사항과 스키마만 다룹니다.

### 다중성계에서 선형 역전파가 실패하는 이유

단일 별의 경우, Gaia/SIMBAD 천체측정의 JD2433282.5까지의 선형 외삽으로 충분합니다
("선형 전파" 참조). 다중성계에서는 컴포넌트들이 상호 궤도 운동 중이기 때문에
이 방법이 **틀립니다**. 상대 위치가 직선 이동이 아닌 회전을 하기 때문입니다.

예를 들어 Alpha Centauri AB는 궤도 주기가 79.762년입니다. JD2433282.5는 Gaia의
J2016 에포크보다 ~66년 이전 — 거의 한 바퀴에 해당합니다. 선형 전파는 A–B 벡터를
0° 회전시키지만, 실제 기하학적 구조는 ~300° 회전했습니다. 그 결과 생성된 cfg는
잘못된 중력 기하학을 가지게 되고, Principia의 N체 적분기가 가짜 이심률과 에너지로
시작하게 됩니다.

해법은 다음과 같습니다. 각 다중성계는 피팅된 Kepler 해를 저장하며, 빌드 시
컴포넌트들의 공통 **무게중심**을 선형으로 전파한 뒤, JD2433282.5에서 평가한
Kepler 파생 (B−A) 오프셋을 적용하여 개별 컴포넌트를 배치합니다.

### 파이프라인 개요

```
barycenter_astrometry  → linear propagation (J2016 / J2000 → JD2433282.5)
                          → R_bary, V_bary at target epoch
                                  +
orbits[].(P,T,e,a,i,ω,Ω)  → Kepler solver (M → E → ν)
                          → Thiele-Innes rotation → (B−A) in ICRS (N,E,W)
                                  +
mass ratio q             → r_A = R_bary − q_B · r_AB
                          → r_B = R_bary + q_A · r_AB
```

삼중성계의 경우 동일한 파이프라인이 중첩 형태로 실행됩니다(AB 내부 궤도, (AB)–C 외부 궤도).
binary-epoch-pipeline.md §6 참조.

### `binary_orbits.json` 스키마 (신규)

기존 스키마는 시스템별 단일 `raw` 블록에 Kepler 요소를 임베드했습니다.
새 스키마는 **컴포넌트별** 사실(질량, 천체측정 소스)과 **궤도별** 사실(관련 두 천체,
Kepler 요소, 출처 논문, 등급, 위상 신뢰성)을 배열로 분리합니다.
시스템당 여러 궤도(삼중성계)도 자연스럽게 표현됩니다.

```json
{
  "Alpha Centauri": {
    "system_id": "alpha_centauri",
    "hierarchy": "triple",
    "components": [
      {
        "name": "Alpha Centauri A",
        "mass_msun": 1.0788,
        "mass_source": "pourbaix_correia_2017",
        "astrometry_source": "mass_weighted_average",
        "astrometry_quality": "barycentric"
      },
      { "name": "Alpha Centauri B", "mass_msun": 0.9092, ... },
      { "name": "Proxima Cen",     "mass_msun": 0.1221, ... }
    ],
    "orbits": [
      {
        "orbit_id": "AB",
        "relates": ["Alpha Centauri A", "Alpha Centauri B"],
        "primary":   "Alpha Centauri A",
        "secondary": "Alpha Centauri B",
        "source":    "akeson_2021",
        "doi":       "10.3847/1538-3881/abfaff",
        "equinox":   "J2000",
        "P_yr":      79.762,
        "T_jd_tt":   2435291.6,
        "e":         0.51947,
        "a_arcsec":  17.4930,
        "i_deg":     79.2430,
        "omega_deg": 231.519,
        "Omega_deg": 205.073,
        "grade":           1,
        "node_resolved":   true,
        "phase_reliable":  true
      }
    ]
  }
}
```

삼중성계는 두 개의 궤도를 나열하고 외부 궤도에 `primary_is_barycenter_of`를 사용합니다.
전체 삼중성 예시는 binary-epoch-pipeline.md §6 참조.

### 스키마 필드 참조

| 필드 | 필수 여부 | 참고 |
|---|---|---|
| `system_id` | 필수 | 파일명 기반으로 사용하는 슬러그. 소문자, 밑줄 사용. |
| `hierarchy` | 필수 | `"binary"`, `"triple"`, `"binary+cpm"` (CPM = 공통 고유운동 동반성). |
| `components[].name` | 필수 | `target_list.json`의 컴포넌트 이름과 정확히 일치해야 함. |
| `components[].mass_msun` | 필수 | `mass_source`와 함께 기재 (논문 bibcode 또는 `gaia_dr3_nss`). |
| `components[].astrometry_source` | 필수 | `gaia_dr3` / `simbad` / `mass_weighted_average` / `gaia_dr3_nss_barycenter` / `hipparcos_barycenter` / `single_component:<Name>` 중 하나. 빌드가 무게중심 천체측정을 어디서 가져올지 결정합니다 — 아래 "하이브리드 저장" 참고. |
| `components[].astrometry_quality` | 필수 | `barycentric` / `photocenter_contaminated` / `single_component`. 정보용. validate.py가 경고에 활용. |
| `barycenter_astrometry` (시스템 수준) | 조건부 | `ra_deg`/`dec_deg`/`parallax_mas`/`pm_ra_masyr`/`pm_dec_masyr`/`radial_velocity_km_s`/`epoch_jd` 블록. `astrometry_source`가 `gaia_dr3_nss_barycenter` 또는 `hipparcos_barycenter`인 경우 **필수** (컴포넌트 천체측정에서 도출 불가한 공개 카탈로그 무게중심값). 나머지 경우 생략 — 빌드가 `astrometry_raw.json`에서 질량 가중 평균을 실시간 계산. |
| `orbits[].orbit_id` | 필수 | `"AB"`, `"inner"`, `"outer"`. 항목 내에서 고유. |
| `orbits[].relates` | 필수 | 이 궤도가 다루는 컴포넌트 또는 무게중심. |
| `orbits[].primary` / `secondary` | 필수 | 하나는 컴포넌트이거나 `primary_is_barycenter_of`여야 함. |
| `orbits[].primary_is_barycenter_of` | 조건부 | 삼중성의 외부 궤도용. 내부 시스템을 구성하는 컴포넌트 이름 목록. |
| `orbits[].source` | 필수 | `"akeson_2021"` (논문 키) 또는 `"orb6:grade=1"` 또는 `"gaia_dr3_nss:OrbitalAlternative"`. |
| `orbits[].P_yr` / `T_jd_tt` / `e` | 필수 | Kepler 핵심 요소. `T`는 근일점 통과 시각 JD (TT). |
| `orbits[].a_arcsec` 또는 `a_au` | 필수 | 상대 장반경. 카탈로그 관례는 `arcsec`; 시차로 변환. |
| `orbits[].i_deg`/`omega_deg`/`Omega_deg` | 필수 | 경사각, 근일점 편각, 승교점 경도. |
| `orbits[].A`/`B`/`F`/`G` (`C`/`H` 선택) | 선택 | 직접 공개된 경우의 Thiele-Innes 상수 (arcsec). `a`/`i`/`omega`/`Omega` 대체 가능 (Gaia NSS). |
| `orbits[].grade` | 필수 | Orb6 품질 등급 1–9. ≤3이면 출판 품질. |
| `orbits[].node_resolved` | 필수 | RV 데이터가 있어 (i,ω,Ω)가 물리적으로 올바른 교점 직선을 반영하면 `true`. 카탈로그가 거울 축퇴 해를 제시하면 `false`. |
| `orbits[].phase_reliable` | 필수 | `grade ≥ 4`이거나 관측 커버리지 대비 외삽이 0.5×P를 초과하면 `false`. false인 경우에도 빌드는 실행되지만 영향받은 컴포넌트 파일의 `meta.notes`에 경고가 기록됨. |

#### 하이브리드 천체측정 저장

DB는 컴포넌트별 파생/계산 천체측정값을 저장하지 않습니다.
공개 무게중심 해(Gaia DR3 NSS, Hipparcos 다중성계 부록)만 시스템 수준의
`barycenter_astrometry` 블록에 저장됩니다. `astrometry_source = "mass_weighted_average"`인
경우 빌드가 `astrometry_raw.json`에서 질량 가중 평균을 실시간 계산합니다.
[[project-nearstars-db-principle]] 참조.

#### Thiele-Innes 관례 (Hilditch / Pourbaix)

`build_systems.py`는 Hilditch / Pourbaix 관례를 적용합니다.

```
ΔN = A · x_p + F · y_p     (북)
ΔE = B · x_p + G · y_p     (동)
ΔW = C · x_p + H · y_p     (관측자 반대 방향)
```

이 관례는 NearStars 모든 문서와 코드에서 통일된 표준입니다. `binary-epoch-pipeline.md` §2 step 5 와 §10 워크드 예시도 동일한 공식을 사용합니다. 위 형식이 α Cen 과 Sirius 의 레거시 `individual_states.b1950` 값을 < 0.05 % 이내로 재현합니다.

### 무게중심 천체측정 결정 트리 (요약)

각 다중성계에서 `components[].astrometry_source` 필드는 다음 결정 트리에 따라
선택됩니다. 컴포넌트 중 `astrometry_source: "unset"`인 항목이 있으면 빌드가 실행을 거부합니다.

```
Gaia DR3 NSS row exists for this system?
├── YES → astrometry_source = gaia_dr3_nss_barycenter
│         astrometry_quality = barycentric
│
└── NO  → resolved pair (separation > ~1″, both have Gaia 5-param)?
          ├── YES → astrometry_source = mass_weighted_average
          │         astrometry_quality = barycentric
          │         (PM averaging cancels orbital tangent velocity)
          │
          └── NO  → Hipparcos multi-star annex (DMSA flag C/O/V/X)?
                    ├── YES → astrometry_source = hipparcos_barycenter
                    │         astrometry_quality = barycentric
                    │
                    └── NO  → astrometry_source = gaia_dr3 (or simbad if saturated)
                              astrometry_quality = photocenter_contaminated
                              (flag, allow but warn)
```

광도 중심 흔들림 오차 모델은 binary-epoch-pipeline.md §8 참조.

### 시스템별 옵션 평가 (최선 추정치; 구현 시 검증 필요)

| 시스템 | 계층 구조 | 권장 옵션 | 소스 논문 오버라이드 |
|---|---|---|---|
| Alpha Centauri AB | binary | gaia_dr3_nss_barycenter | Akeson et al. 2021 |
| Sirius AB | binary | hipparcos_barycenter (A saturated; B is WD) | Bond et al. 2017 |
| 61 Cygni AB | binary | mass_weighted_average (wide, both in Gaia) | Malkov et al. 2012 — `phase_reliable: false` (P~679 yr, grade ≥3) |
| 40 Eridani ABC | triple | A: gaia_dr3 / B+C close pair: NSS or mass-weighted | 조사 필요 |
| Eta Cassiopeiae AB | binary | mass_weighted_average | Tokovinin 2021 — P=480 yr, `phase_reliable: false` 가능성 높음 |
| 36 Ophiuchi ABC | triple | A,B: mass-weighted on close pair / C: static CPM at fixed offset | 조사 필요 |

실제 `astrometry_source` 값은 구현 세션에서 확정됩니다 — 위 표는 출발점이며
확정값이 아닙니다.

### 위상 신뢰성 의미론

다음 경우에 `phase_reliable: false`로 설정합니다.
- Orb6 grade ≥ 4, 또는
- 관측 커버리지가 주기의 절반 미만(외삽 > 0.5 P), 또는
- 근일점 통과 시각 오차가 주기의 5%를 초과하는 경우

`phase_reliable: false`인 경우 빌드는 계속 실행됩니다(가용 해에서 구한 최선 추정치를
출력). 그러나 영향받은 컴포넌트 파일의 `meta.notes`에 경고가 기록됩니다. 하위
Kopernicus cfg는 여전히 값을 사용할 수 있지만, Principia 장기 시뮬레이션 사용자는
~0.5 P 이후의 상대 기하학을 신뢰해서는 안 됩니다.

위상 불신뢰 광시야 CPM 동반성(P > 1000년, 피팅된 궤도 없음)의 경우,
`orbit_type: "static_cpm"`을 사용합니다 — binary-epoch-pipeline.md §6 참조 —
이는 상대 위치를 카탈로그 기준 에포크에 동결합니다.

---

## 출처 기록 프로토콜

참고한 모든 논문과 카탈로그를 기록합니다. 값을 사용하지 않은 경우에도 `used_for`에 이유를
기재하세요.

SIMBAD bibcode는 출처가 아닙니다. `https://ui.adsabs.harvard.edu/abs/<bibcode>`를 통해
원본 논문으로 해석하고 거기서 DOI를 기록하세요.

동일 방법 계층의 두 논문이 충돌하면 둘 다 `sources[]`와 측정값 배열에 추가하고,
선택 근거를 `meta.notes`에 문서화하세요.

---

## 데이터 소스

아래의 모든 소스는 자유롭게 접근 가능합니다. astroquery가 대부분을 통합 Python 인터페이스로
지원합니다. 직접 접근이나 폴백을 위한 raw TAP 엔드포인트도 나열합니다.

---

### 근처 항성계

**RECONS (Research Consortium on Nearby Stars)**
10파섹(~32.6광년) 이내의 모든 항성계에 관한 권위 있는 목록.
별이 프로젝트의 50광년 범위 내에 있음을 확인하고, 별의 상태를 갱신하는 새로 측정된
거리를 파악하는 데 사용하는 기본 참고 자료.

- URL: `https://www.recons.org`
- 새 시차가 측정될 때마다 정기 업데이트
- 사용 시기: 후보 별이 실제로 50광년 이내인지 확인할 때, 다른 데이터베이스에 아직
  두드러지지 않은 새로 발견된 근처 시스템을 찾을 때

---

### 천체측정 및 항성 위치

**Gaia DR3**
근처 별의 위치, 고유운동, 시차, 시선 속도의 주요 소스.

- TAP endpoint: `https://gea.esac.esa.int/tap-server/tap`
- astroquery: `from astroquery.gaia import Gaia`
- Table: `gaiadr3.gaia_source`
- Key columns: `source_id`, `ra`, `dec`, `parallax`, `parallax_error`,
  `pmra`, `pmdec`, `radial_velocity`
- Epoch: J2016.0 (JD2457389.0)
- Caveat: `radial_velocity`는 희미한 적색 왜성에서 null.

**Hipparcos**
Gaia 이전 카탈로그. 근처 별 모두에서 Gaia DR3로 대체됐지만, 밝기 포화(V < ~6 mag)로
Gaia에 누락된 별의 교차 확인이나 대체 소스로 유용.

- Access via VizieR: catalogue `I/311`
- TAP endpoint: `https://tapvizier.cds.unistra.fr/TAPVizieR/tap`

**JPL Horizons**
태양계 천체 및 일부 근처 별의 SSB-ICRF 직접 상태 벡터(위치 + 속도).
출력값이 Principia/Sol 단위(km, km/s) 및 에포크(B1950.0 = JD2433282.5)와
직접 일치합니다.

- Web: `https://ssd.jpl.nasa.gov/horizons/`
- Batch API: `https://ssd.jpl.nasa.gov/horizons_batch.cgi`
- astroquery: `from astroquery.jplhorizons import Horizons`
- Settings: `VECTORS`, frame `ICRF`, center `@SSB`, epoch `1950-Jan-01`
- Coverage: Alpha Centauri, Barnard's Star 확인 가능. 다른 대상 시스템 커버리지는
  다를 수 있음.

---

### 항성 물리 파라미터 (질량, 반지름, Teff)

**SIMBAD**
문헌 집성 서비스. 질량/반지름을 직접 열로 저장하지 않고 TAP를 통해
`mesMass` 및 `mesDiameter` 측정 테이블을 조회합니다.

- TAP endpoint: `https://simbad.u-strasbg.fr/simbad/sim-tap/sync`
- astroquery: `from astroquery.simbad import Simbad`
- 사용 용도: 질량, 반지름, 스펙트럼형, 교차 ID, RV 폴백, bibcode → 논문 추적

**VizieR**
출판된 천문 카탈로그 라이브러리. 개별 논문의 수천 개 항성 파라미터 테이블을 호스팅하며,
문헌값의 가장 완전한 집성 서비스.

- TAP endpoint: `https://tapvizier.cds.unistra.fr/TAPVizieR/tap`
- astroquery: `from astroquery.vizier import Vizier`
- 이 프로젝트와 관련된 주요 호스팅 카탈로그.
  - `I/355` — Gaia DR3
  - `I/311` — Hipparcos
  - `B/pastel/pastel` — PASTEL (아래 참조)
  - `J/A+A/556/A150` — SWEET-Cat (아래 참조)
  - 개별 간섭측정 논문 (CHARA, VLTI/GRAVITY 결과)

**PASTEL**
문헌에서 도출된 항성 대기 파라미터(Teff, log g, [Fe/H])의 편집본. 진화 모델
질량 추정을 교차 확인하는 공개 Teff 값을 찾는 데 유용.

- URL: `https://pastel.obs.u-bordeaux1.fr/`
- Access via VizieR: `B/pastel/pastel`
- 참고: 질량이나 반지름을 직접 제공하지 않으며, 이를 도출하는 데 사용하는
  분광 파라미터를 제공.

**SWEET-Cat**
행성 호스트 별의 대기 파라미터 및 질량 카탈로그. 확인된 행성이 있는 대부분의 별을
다루며, 가능한 경우 균일하게 도출됨.

- URL: `https://sweetcat.iastro.pt/`
- Access via VizieR: `J/A+A/556/A150`
- 제공 항목: Teff, log g, [Fe/H], 항성 질량
- 주의: 질량은 보정 공식에서 도출된 것이며 직접 측정값이 아님.
  이중성 궤도나 간섭측정 값보다 낮은 우선순위.

---

### 행성 궤도 요소 및 물리 파라미터

#### 조사 우선순위 순서

행성 시스템을 조사할 때 아래 소스를 순서대로 확인하고 가장 정밀한 값을 사용합니다.
NASA Archive만으로는 충분하지 않습니다.

| 우선순위 | 소스 | 최적 용도 |
|---|---|---|
| 1 | Individual paper (ADS) | 가장 최신/확정적인 궤도 해 |
| 2 | DACE | RV 궤도 요소 (T₀, ω, 이심률 상세) |
| 3 | TEPCat | 트랜짓 시스템 — 동일 피트에서 질량 + 반지름 |
| 4 | exoplanet.eu | 교차 확인; NASA Archive보다 최근 발견 조기 포착 |
| 5 | NASA Exoplanet Archive | 기준값; 파이프라인 자동 fetch에서 사용 |

값을 사용하지 않더라도 참고한 모든 소스를 기록하세요.
각 행성에 대해 `planets_curated.json` 항목은 출처 DOI와 함께 가용한 최선의 값을
반영해야 합니다.

---

**NASA Exoplanet Archive**
TAP 지원을 갖춘 가장 포괄적인 행성 데이터베이스. 궤도 요소의 주요 소스.

- TAP endpoint: `https://exoplanetarchive.ipac.caltech.edu/TAP/sync`
- astroquery: `from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive`
- Table: `ps` (Planetary Systems); filter `default_flag = 1`
- Table: `pscomppars` (composite best parameters per planet)
- Key columns: `pl_orbper`, `pl_orbsmax`, `pl_orbeccen`, `pl_orbincl`,
  `pl_orblper`, `pl_bmasse`, `pl_rade`, `pl_tranmid`, `pl_refname`
- 주의: `default_flag = 1`은 아카이브의 최선 파라미터 선택이며, 항상 최신이 아닐 수
  있음. `pl_refname`을 확인하고 출처 논문과 대조하세요.

**DACE (Data & Analysis Center for Exoplanets)**
제네바 천문대의 RV 행성 데이터베이스. RV 검출 행성에 대해 NASA Archive보다
상세한 궤도 해를 제공합니다 — T₀, ω, 이심률 신뢰 구간, 전체 RV 시계열 포함.

- URL: `https://dace.unige.ch/exoplanets/`
- 특히 강점: 근처 M 왜성 행성, HARPS/ESPRESSO 대상
- 사용 시기: NASA Archive 궤도 요소가 희소하거나 구식인 경우

**Extrasolar Planets Encyclopaedia (exoplanet.eu)**
유럽 카탈로그. 새로 발표된 행성에 대해 NASA Archive보다 빠르게 업데이트됩니다.
교차 확인 및 NASA Archive에 아직 없는 최근 발견을 파악하는 데 유용.

- URL: `https://exoplanet.eu`
- TAP endpoint: `http://voparis-tap-planeto.obspm.fr/tap`
- astroquery: `import pyvo; pyvo.dal.TAPService("http://voparis-tap-planeto.obspm.fr/tap")`
- Table: `exoplanet.epn_core`
- 웹사이트에서 벌크 CSV 다운로드도 가능.

**TEPCat (Transiting Extrasolar Planet Catalogue)**
트랜짓 시스템의 물리적·궤도 특성에 관한 중요 편집본. 독립적으로 도출되었으며
NASA Archive의 단순 미러가 아닙니다. 도출 방법론이 문서화된 트랜짓 측정 반지름과
질량에 특히 유용.

- URL: `https://www.astro.keele.ac.uk/jkt/tepcat/`
- 벌크 다운로드용 기계 가독형 테이블 제공.
- 재현성을 위한 월간 스냅샷 아카이브.
- 제공 항목: 항성 질량/반지름, 행성 질량/반지름, 궤도 요소, 자전축 기울기, 평형 온도.

**Open Exoplanet Catalogue**
커뮤니티 유지 GitHub 리포지토리. JSON/XML 형식. 대형 아카이브에서 충분히 다루지
않는 시스템의 빠른 조회에 유용.

- URL: `https://github.com/openexoplanetcatalogue/open_exoplanet_catalogue`
- 접근: 직접 다운로드 또는 `git clone`.

---

### 트랜짓 타이밍 및 역표 데이터

**NASA Exoplanet Archive Transit and Ephemeris Service**
아카이브의 확인된 행성에 대한 트랜짓 시각 계산. TRAPPIST-1과 같이 TTV가 지배적인
시스템에 필수.

- URL: `https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TransitView/nph-visibletbls`

**Exoplanet Transit Database (ETD)**
아마추어 및 전문 트랜짓 관측. 동료 심사 TTV 분석보다 정밀도는 낮지만 광범위한
커버리지를 제공하며 에포크 정제에 유용.

- URL: `http://var2.astro.cz/ETD/`

---

### 문헌 및 논문 접근

**NASA ADS (Astrophysics Data System)**
천문학의 권위 있는 문헌 데이터베이스. 다음 용도로 사용.
- SIMBAD에서 bibcode를 전체 논문으로 추적
- 특정 시스템의 가장 최근 궤도 분석 찾기
- 모든 측정 항목의 DOI 취득

- URL: `https://ui.adsabs.harvard.edu`
- API: `https://api.adsabs.harvard.edu/v1/`

**arXiv (astro-ph.EP, astro-ph.SR)**
프리프린트 서버. 많은 궤도 분석과 항성 파라미터 논문이 저널 출판 전 여기에 등장.

- URL: `https://arxiv.org/list/astro-ph.EP/recent`

---

### 아카이브 및 우주 임무 데이터

**MAST (Mikulski Archive for Space Telescopes)**
Kepler, K2, TESS, HST 데이터를 호스팅. 특정 시스템의 raw 광도 곡선이나
트랜짓 측광이 필요한 경우 관련.

- URL: `https://mast.stsci.edu`
- astroquery: `from astroquery.mast import Observations`

---

### 접근 우선순위 요약

| 데이터 유형 | 주요 소스 | 보조 소스 | 교차 확인 |
|---|---|---|---|
| 위치, PM, 시차 | Gaia DR3 | Hipparcos (밝은 별) | JPL Horizons |
| 시선 속도 | Gaia DR3 | SIMBAD | 발견 논문 |
| 상태 벡터 (km, km/s) | Gaia DR3 → 변환 | JPL Horizons (직접) | -- |
| 항성 질량 | SIMBAD `mesMass` | SWEET-Cat | VizieR (논문별) |
| 항성 반지름 | SIMBAD `mesDiameter` | TEPCat | VizieR (간섭측정 논문) |
| 궤도 요소 | NASA Exoplanet Archive | exoplanet.eu | TEPCat |
| 행성 질량 | NASA Exoplanet Archive | TEPCat | 발견 논문 |
| 행성 반지름 | NASA Exoplanet Archive | TEPCat | 발견 논문 |
| 트랜짓 타이밍 | NASA Archive ephemeris | ETD | 출처 논문 (TTV 분석) |
| 논문 검색 | ADS | arXiv | -- |

---

## 알려진 이슈 및 미결 결정 사항

### 성간 거리에서의 KSP 렌더링 엔진 한계

Principia는 거리에 관계없이 먼 별을 중력 섭동체로 올바르게 등록합니다.
Alpha Centauri(~4e13 km)에서의 배정밀도 위치 ULP는 약 9 m으로, 힘 계산에
허용 가능한 수준입니다.

그러나 KSP의 렌더링 엔진은 별개의 문제입니다. 성간 거리에서 렌더러(Principia가 아닌)의
부동 소수점 정밀도가 시각적 결함, SOI/맵 뷰 실패, 또는 엔진 충돌을 일으킬 수 있습니다.
이 규모에서는 테스트된 바 없습니다.

**cfg 생성을 시작하기 전에 이 절충안을 결정해야 합니다.**
- 실제 거리 사용 → Principia 물리 정확, KSP 렌더러 동작 미확인
- 거리 축소 → KSP 렌더러 안정, Principia 물리 부정확

각 시스템 파일의 `meta.notes`에 결정 사항과 그 근거를 기록하세요.

---

## 범위 외 항목

다음 사항은 여기가 아닌 별도 세션 또는 에이전트에서 처리합니다.

- Kopernicus cfg 생성
- Principia 패치 작성 (Sol Real 변형, Sol Quarter 변형, RSS 변형)
- 시각 및 아트 파라미터 (atmosphere, terrain, Scatterer, EVE)
- 포함할 시스템에 관한 커뮤니티 투표
- 성간 거리 스케일링 결정 (위의 알려진 이슈 참조)
