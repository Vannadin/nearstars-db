# NearStars

실제 천문 관측 데이터를 기반으로 실존하는 근방 항성계를 **Kerbal Space Program 1.12.x**에 추가하는 데이터 파이프라인 및 데이터베이스.

이 저장소는 모드의 **데이터 엔진**입니다. 공개 천문 카탈로그에서 관측 데이터를 가져와 시스템별 구조화된 JSON 파일로 조립하고, Kopernicus 및 Principia 설정 파일 생성기가 다운스트림에서 소비할 수 있도록 검증합니다.

이 모드는 KSP 1.12.x 의 실제 태양계 기반인 [Sol-Configs](https://github.com/RSS-Reborn/Sol-Configs) (ballisticfox) 위에서 동작합니다. RSS 호환은 향후 목표입니다.

항성계 소개, 방법론, 뷰어 등의 개요는 [프로젝트 위키](https://github.com/Vannadin/nearstars-db/wiki)에서 볼 수 있습니다 (영어/한국어).
현재 데이터베이스는 [라이브 뷰어](https://vannadin.github.io/nearstars-db/) 에서 확인할 수 있습니다.
Phase 2 큐레이션 리포트 샘플 (논문별 측정값).
[TRAPPIST-1](https://vannadin.github.io/nearstars-db/phase2/trappist-1.html).
Phase 3 인게임 표현 합성 샘플.
[TRAPPIST-1 d](https://vannadin.github.io/nearstars-db/phase3/trappist-1-d.html).

---

## 프로젝트 배경

NearStars 는 KSP 1.8.0 시절의 **REX 모드의 정신적 후계작**입니다. 현실적인 Sol 태양계에서 출발해 실제로 존재하는 근거리 항성계 — Alpha Centauri, Barnard's Star, Sirius 등 — 으로 날아간다는 컨셉을 되살립니다. 기존 시도들과의 가장 큰 차별점은 **Principia (N체 중력) 완전 호환** 입니다.

**최종 모드 수록 범위.** 항성계 약 10개. 본 저장소의 폭넓은 연구 데이터베이스 안에서 선별 예정. 최종 목록과 선택 순서는 아직 결정 중입니다.

**현재 단계.** 데이터 연구가 큐레이션 마일스톤에 도달. 데이터 엔진 작업에서 실제 모드 cfg 생성 (Kopernicus 및 Principia 패치) 으로 전환 중입니다.

---

## 주요 기능

- Gaia DR3, SIMBAD, NASA Exoplanet Archive, ORB6 등 라이브 카탈로그에서 천체측정, 측광, 항성 물성, 외행성 데이터를 수집
- 모든 별에 대해 km / km·s⁻¹ 단위의 SSB-ICRF 직교 좌표 위치 및 속도를 계산
- 이중성 및 다중성계를 처리 — 질량 가중 평균 및 케플러 궤도 전파를 통해 질량 중심 위치를 계산
- Kopernicus 및 Principia에 바로 사용 가능한 데이터를 생성 (각각 약 50 ly 및 약 80 ly 범위)
- 빌드 단계 완료 전 전체 데이터베이스를 엄격한 스키마에 대해 검증
- 전체 데이터베이스의 정적 HTML 뷰어를 게시 (`docs/`)

---

## 저장소 구조

```
db/
  target_list.json          # 목표 항성계 마스터 목록
  astrometry_raw.json       # 수집: RA, Dec, 시차, 고유운동, RV
  photometry_raw.json       # 수집: V등급, Gaia G, BP-RP
  stellar_props_raw.json    # 수집: Teff, 분광형, 질량, 반지름 측정값
  planets_raw.json          # 수집: 외행성 궤도 및 물리 파라미터
  planets_ps_default.json   # NASA Planetary Systems 기본값 (큐레이션 전)
  binary_orbits.json        # 수작업 큐레이션된 케플러 궤도 요소 (ORB6 기반)
  stellar_props_curated.json # 질량/반지름/분광형 수동 오버라이드
  planets_curated.json      # 행성 데이터 수동 오버라이드
  systems/                  # 컴포넌트별 조립 출력 (항성 컴포넌트당 1개 파일)
    alpha_centauri_a.json
    alpha_centauri_b.json
    sirius_a.json
    ...

scripts/pipeline/
  fetch_astrometry.py       # Gaia DR3 TAP 배치 → SIMBAD 폴백
  fetch_photometry.py       # Gaia G/BP-RP + Hipparcos V등급
  fetch_stellar_props.py    # SIMBAD에서 Teff, 분광형, 질량, 반지름 수집
  fetch_planets.py          # NASA Exoplanet Archive TAP
  fetch_planets_ps.py       # Planetary Systems 기본 파라미터 테이블
  fetch_stellarium_ids.py   # Stellarium Web 스카이소스 ID 조회
  build_systems.py          # raw + curated → db/systems/*.json 조립
  build_curated_from_ps.py  # PS 기본값으로 planets_curated 초기 생성
  build_site.py             # docs/data.json + docs/index.html 생성
  generate_target_list.py   # 유틸리티: systems/에서 target_list 재생성
  validate.py               # 스키마 검증 (실패 시 비정상 종료)
  schema.py                 # 공유 스키마 정의 및 검증기

docs/
  index.html                # 정적 DB 뷰어 (다크 테마, 필터 가능)
  data.json                 # 뷰어 데이터 소스

dist/                       # 빌드 산출물 (gitignored). principia-cfg
                            # 스킬이 NearStars-Configs/Patches/Principia/
                            # 아래 .cfg 패치를 emit.

run_pipeline.sh             # 전체 파이프라인 일괄 실행 스크립트
```

---

## 파이프라인

전체 파이프라인 실행 방법.

```bash
./run_pipeline.sh
```

단계는 순서대로 실행됩니다.

| # | 스크립트 | 동작 |
|---|---------|------|
| 1 | `fetch_astrometry.py` | `target_list.json`의 모든 `gaia_source_id`에 대해 Gaia DR3 TAP 쿼리. 누락된 항목은 SIMBAD TAP으로 폴백 |
| 2 | `fetch_photometry.py` | V등급 (Hipparcos/하드코딩) 및 Gaia G, BP-RP 수집 |
| 3 | `fetch_stellar_props.py` | Teff, 분광형, 사용 가능한 모든 질량/반지름 측정값 수집 |
| 4 | `fetch_planets.py` | NASA Exoplanet Archive에서 각 목표 주변의 확인된 외행성 쿼리 |
| 5 | `fetch_stellarium_ids.py` | 각 컴포넌트를 Stellarium Web 스카이소스 ID에 매핑 (멱등성 보장, 이미 매핑된 항목 건너뜀) |
| 6 | `build_systems.py` | raw + curated 데이터 병합, 에포크 전파, ICRF 위치 계산, 이중성 처리 |
| 7 | `validate.py` + `build_site.py` | `db/systems/` 스키마 검증 후 정적 뷰어 재생성 |

모든 fetch 스크립트는 **멱등성**을 가집니다. 재실행 시 누락되거나 null인 항목만 쿼리하므로 새 별을 점진적으로 추가해도 안전합니다.

---

## 데이터 레이어

`db/systems/`의 각 파일은 세 개의 레이어로 구성됩니다.

### `raw`
카탈로그에서 수집한 원본 값. 출처(provenance) 포함.
- 천체측정: RA, Dec, 시차, 고유운동 (pmra, pmdec), 시선속도, 에포크
- 측광: V등급, Gaia G, BP-RP
- 항성 물성: Teff, 분광형, 메서드 레이블(`interferometry`, `binary_orbit`, `eclipsing_binary`, `asteroseismology` 등)과 `recommended` 플래그가 붙은 사용 가능한 모든 질량 및 반지름 측정값
- 행성 데이터: 궤도 요소, 질량, 반지름 (가용 시)

### `derived`
`raw`에서 계산된 값. 소스 데이터가 null이면 derived 값도 null을 유지하며 기본값을 가정하지 않습니다.
- B1950 및 J2000 에포크에서의 ICRF 직교 위치 및 속도 (SSB 원점, km / km·s⁻¹)
- pc 및 km 단위 거리
- 이중성 컴포넌트의 경우: 질량 중심 오프셋, 궤도 역할 (primary/secondary), 질량비
- 에포크 전파 방법: 이중성의 경우 `kepler_thiele_innes`, 단독성의 경우 표준 ICRF 운동학

### `principia`
KSP Principia에 바로 사용 가능한 값.
- 중력 파라미터 μ = GM (km³·s⁻²), 권장 질량으로 계산
- 평균 반지름 (km), 권장 반지름으로 계산

---

## 이중성 및 다중성계 처리

이중성 및 다중성계는 카탈로그 천체측정이 일반적으로 질량 중심이 아닌 광중심 기준이므로 특별한 처리가 필요합니다.

`db/binary_orbits.json`의 각 시스템에 대해.
- 케플러 궤도 요소를 저장합니다 (주기, 근성점 통과 에포크, 이심률, 반장축, 경사각, ω, Ω). ORB6 및 공개된 해 기반.
- `build_systems.py`는 **Kepler + Thiele-Innes** 방법을 사용해 게임 에포크까지 궤도를 전파하여 진근점이각을 계산한 뒤 직교 분리 벡터로 변환합니다.
- 각 컴포넌트의 위치는 질량비 q = M_B / (M_A + M_B)를 이용해 질량 중심에서 분리됩니다.
- 질량 중심 위치 자체는 컴포넌트 카탈로그 위치의 질량 가중 평균으로 계산됩니다.

현재 추적 중인 이중성 및 다중성계.

| 시스템 | 유형 | 출처 |
|--------|------|------|
| Alpha Centauri (A + B + Proxima Cen) | 계층적 삼중성 | Pourbaix & Correia 2017 (내곽) / Kervella 2017 (외곽) |
| Sirius AB | 이중성 | ORB6 |
| 61 Cygni AB | 이중성 | ORB6 |
| 40 Eridani ABC | 계층적 삼중성 | ORB6 |
| Eta Cassiopeiae AB | 이중성 | ORB6 |
| 36 Ophiuchi ABC | 계층적 삼중성 | ORB6 |
| Procyon AB | 이중성 | ORB6 |
| 70 Ophiuchi AB | 이중성 | ORB6 |

---

## 행성 큐레이션

행성 데이터는 두 단계를 거칩니다.

**Curation Phase 1 (기본)** — NASA Exoplanet Archive 최선 가용값 사용. 궤도 요소는 기본 Kopernicus 배치에 그대로 사용됩니다. 대부분의 별이 이 수준입니다.

**Curation Phase 2 (정밀 큐레이션)** — `planets_curated.json`을 통한 수동 오버라이드. 완전한 출처 정보(DOI, bibcode)를 포함한 정밀 궤도 요소를 추가합니다. Principia n-body 물리로 인게임 구현될 시스템에 사용됩니다. curated 데이터의 각 `orbital` 및 `physical` 블록에는 출처 필드(`source`, `bibcode`, 또는 `doi`) 중 적어도 하나가 필요합니다.

> 참고. "Curation Phase" 는 데이터 큐레이션 깊이를 의미하며, `docs/reference/guideline.md §9` 에 나오는 모드 개발 Phase 와는 별개입니다.

---

## 스키마 검증

`scripts/pipeline/schema.py`는 모든 데이터 레이어에 대한 필수 및 선택 키를 정의합니다. `validate.py`는 파이프라인 종료 시 모든 검사를 실행하며, 실패 시 비정상 종료합니다.

검증 대상 레이어.
- `astrometry_raw.json` — 필수 천체측정 필드, 에포크 형식
- `photometry_raw.json` — vmag_v 필수, source 필수
- `stellar_props_raw.json` — 질량/반지름 측정 구조, `value_*` 접두사 강제, `error_*` 접두사 금지 (`uncertainty_*` 사용 필수)
- `binary_orbits.json` — 궤도 요소, 컴포넌트 상호 참조, barycenter 블록 요건
- `stellar_props_curated.json` — 메서드 화이트리스트, 측정 유형별 단일 `recommended: true`
- `planets_curated.json` — 모든 orbital/physical 블록에 출처 필수

---

## 다운스트림 사용

이 저장소는 데이터를 생성합니다. KSP 설정 파일을 직접 작성하지는 않습니다.

**Kopernicus** (약 50 ly 범위): `db/systems/*.json`을 읽어 KSP 태양계에 별과 행성을 추가하는 `.cfg` 파일을 생성합니다. `derived.icrs_*` 좌표와 `principia.*` 값을 사용합니다.

**Principia** (약 80 ly 범위): 동일한 JSON 파일을 읽어 B1950 ICRF 기준 n-body 초기 조건 블록을 생성합니다. `derived.icrs_x_km`, `derived.icrs_vx_km_s`, `principia.gravitational_parameter_km3_s2`가 필요합니다.

다운스트림 설정 파일 생성기는 이 파이프라인과 무관하게 각자의 거리 제한을 적용합니다.

---

## 요구 사항

- Python 3.10+
- [`PyAstronomy`](https://github.com/sczesla/PyAstronomy) — Markley 케플러 방정식 풀이기

```bash
pip install PyAstronomy
```

그 외 외부 의존성은 없습니다. 모든 카탈로그 쿼리는 TAP/HTTP 위의 표준 `urllib`을 사용합니다.

---

## 데이터 출처

| 출처 | 사용 용도 |
|------|----------|
| [Gaia DR3](https://www.cosmos.esa.int/web/gaia/data-release-3) | 1차 천체측정 (RA, Dec, 시차, PM, RV) |
| [SIMBAD](https://simbad.u-strasbg.fr/) | 폴백 천체측정, Teff, 분광형, 질량/반지름 문헌값 |
| [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/) | 확인된 외행성 파라미터 |
| [ORB6 / WDS](https://www.astro.gsu.edu/wds/orb6.html) | 이중성 및 다중성계 궤도 요소 |
| [Stellarium Web](https://stellarium-web.org/) | 인게임 스카이박스 연동용 스카이소스 ID |
| 발표 논문 | 시스템별 큐레이션 값 (측정값별 인라인 인용) |

---

## 라이선스

CC-BY-NC-SA-4.0 — [LICENSE](../LICENSE) 참조.

서드파티 데이터 저작권 표시: [NOTICE](../NOTICE) 참조.
