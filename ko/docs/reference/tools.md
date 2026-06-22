# 툴 목록 — NearStars

프로젝트가 커지면서 약 서른 개의 스크립트와 여러 에이전트 스킬이 여러 디렉터리에 흩어졌습니다. 이 문서는 그것들을 **위치가 아니라 목적별로** 묶어 인덱스화합니다. 각 섹션은 하나의 논리적 작업 단위 (데이터 페치, 뷰어 빌드, 모드 cfg 생성 등) 에 해당하며 거기에 참여하는 모든 파일을 함께 나열합니다.

## 한눈에 보기

| # | 묶음 | 하는 일 | 진입점 |
|---|-----|--------|-------|
| 1 | 데이터 엔진 | raw 페치 → 시스템별 JSON 조립 → 검증 | `./run_pipeline.sh` |
| 2 | DB → HTML 뷰어 | `db/systems/` 를 정적 사이트로 렌더링 | `scripts/pipeline/build_site.py` |
| 3 | Phase 3 합성 | ADS+arXiv triage → cfg-ready 결정표 + 이중 언어 뷰어 | `nearstars-phase3` 스킬 |
| 4 | 안정성 샌드박스 | 가상 위성·추가 행성에 대한 REBOUND N-body 검증 | `phase3/stability-sim/scripts/run.py` |
| 5 | 외부 교차검증 | DB 위치를 Stellarium 과 비교 | `scripts/verification/stellarium_crosscheck.py` |
| 6 | Kopernicus cfg | DB → Kopernicus `.cfg` 패치 | `kopernicus-cfg` 스킬 |
| 7 | Principia cfg | DB → Principia n-body 패치 | `principia-cfg` 스킬 |
| 8 | Firefly cfg | Phase 3 대기 합성 → Firefly 재진입 효과 cfg | `firefly-cfg` 스킬 |
| 9 | ResearchBodies cfg | Phase 4 discoverability → ResearchBodies 숨김/발견 패치 | `researchbodies-cfg` 스킬 |
| 10 | 별 추가 / Phase 2 큐레이션 | 새 별 DB 진입 절차 | `nearstars-add-star` 스킬 |
| 11 | 개발 헬퍼 | 마크다운 미리보기, ko/ 미러 정합성, 레포 전체 건강 점검 | `scripts/preview-md.sh`, `scripts/check-mirrors.sh`, `scripts/check.sh` |
| 12 | 3D 성도 | `db/systems/` → 인터랙티브 3D 지도 (광년 스케일 + 시스템별 AU 뷰) | `scripts/viz/build_starmap.py` |

## 검증 & QA — 인덱스

정확성 검사 도구들은 기능별 묶음 여러 곳에 흩어져 있습니다. 이 표는 그것들을 한 자리에 모아 가시성을 확보합니다 — 각 툴은 자기 묶음 섹션에도 그대로 등장합니다.

| 검증 대상 | 툴 / 활동 | 묶음 | 언제 실행 |
|----------|----------|:----:|----------|
| `db/systems/*.json` 의 스키마 무결성 | `scripts/pipeline/validate.py` | [1](#1-데이터-엔진) | 빌드 직후 (`run_pipeline.sh` 가 자동 호출) |
| 위계적 다성계 구조 | `scripts/pipeline/test_hierarchical.py` | [1](#1-데이터-엔진) | 다성계 궤도 편집 후 smoke test |
| Stellarium 과 비교한 DB 위치 | `scripts/verification/stellarium_crosscheck.py` | [5](#5-외부-교차검증) | 퍼블리시 전 spot-check |
| 큐레이션된 + 가상 바디의 동역학적 안정성 | `phase3/stability-sim/scripts/run.py` | [4](#4-안정성-샌드박스) | 위성·추가 바디 cfg 출시 전, 혹은 기준 DB sanity 확인 |
| `ko/` 미러 파일 정합성 | `scripts/check-mirrors.sh` | [11](#11-개발-헬퍼) | 커밋 / 릴리스 전 |
| Phase 3 합성 정책 적합성 | `nearstars-phase3` 의 audit-pass 절차 | [3](#3-phase-3-합성-파이프라인) | 합성 배치 후 — 수동, 결과는 `phase3/<system>/audit-pass-<YYYY-MM-DD>.md` |
| 빌드 산출물 신선도 + 매니페스트 커버리지 | `scripts/check_build_freshness.py` | [11](#11-개발-헬퍼) | push 전 — `scripts/check.sh` 7번 항목에서 호출 |

## 1. 데이터 엔진

**목적.** 공개 카탈로그에서 측성·측광·항성 물리량·행성 측정값을 끌어와 시스템별 JSON 으로 조립하고 검증합니다.

**언제.** target list 에 새 별 추가, 카탈로그 갱신, 스키마 변경 시.

**파일.**
- `scripts/pipeline/fetch_astrometry.py` — Gaia DR3 TAP, SIMBAD 폴백 (RA, Dec, 시차, 고유운동, RV)
- `scripts/pipeline/fetch_photometry.py` — Gaia G + Hipparcos V-mag
- `scripts/pipeline/fetch_stellar_props.py` — SIMBAD 에서 Teff, 분광형, 질량, 반지름
- `scripts/pipeline/fetch_planets.py` — NASA Exoplanet Archive TAP
- `scripts/pipeline/fetch_planets_ps.py` — Planetary Systems 기본값 테이블
- `scripts/pipeline/fetch_stellarium_ids.py` — Stellarium Web skysource ID 조회
- `scripts/pipeline/build_systems.py` — raw + curated → `db/systems/*.json`
- `scripts/pipeline/build_curated_from_ps.py` — PS 기본값에서 `planets_curated.json` 시드
- `scripts/pipeline/generate_target_list.py` — `db/systems/` 에서 `target_list.json` 재생성
- `scripts/pipeline/validate.py` — 스키마 검증, 실패 시 non-zero exit
- `scripts/pipeline/schema.py` — 공용 스키마 + 검증기
- `scripts/pipeline/_naming.py` — 호스트/행성 이름 → 슬러그/파일명 변환의 단일 정의 (모든 빌더가 여기서 import, 재구현 금지)
- `scripts/pipeline/test_hierarchical.py` — 위계적 다성계 구조 테스트

**오케스트레이터.** `./run_pipeline.sh` 가 fetch → build → validate → site build 를 순서대로 돌립니다.

**I/O.** `db/target_list.json` → `db/*_raw.json` → `db/systems/*.json`.

## 2. DB → HTML 뷰어

**목적.** `db/systems/` 와 Phase 2 측정값을 `docs/` 의 정적 HTML 뷰어로 렌더링합니다.

**파일.**
- `scripts/pipeline/build_site.py` — `docs/data.json` 과 메인 `index.html` 생성
- `scripts/pipeline/build_phase2_html.py` — 시스템별 Phase 2 (논문별 측정치) 뷰어
- `scripts/pipeline/build_reports_index.py` — Phase 2/3 리포트 랜딩 인덱스

**출력.** `docs/{data.json, index.html, phase2/*.html, reports.html}`.

## 3. Phase 3 합성 파이프라인

**목적.** Phase 2 측정값을 cfg-ready 합성 결정으로 변환하고, 행성별 이중 언어 HTML 뷰어를 생성합니다.

**언제.** "Phase 3 진행", "<행성> 합성", "이 행성 Phase 3 까지 올려줘" 같은 요청.

**파일.**
- `scripts/phase3/run_phase3.py` — Steps 2–6 (bib build → system bib → expand → score → inject → fetch) 드라이버. `phase3/<system>/system.yaml` 을 읽어 모든 stage 실행
- `scripts/phase3/build_bibliography.py` — ADS + arXiv 행성별 (혹은 `--system`) bibliography 빌더
- `scripts/phase3/expand_citations.py` — 1-hop citation graph walk
- `scripts/phase3/score_papers.py` — authority + relevance 점수 + filter
- `scripts/phase3/inject_papers.py` — `system.yaml` 기반으로 ADS 검색이 놓친 paper 일괄 inject (시스템별 `add_missing_papers.py` 대체)
- `scripts/phase3/fetch_arxiv_texts.py` — pending paper 의 arXiv 전문을 ar5iv 로 수집
- `scripts/phase3/build_manual_fetch.py` — 수동 다운로드 필요 논문 HTML 인덱스
- `scripts/phase3/verify_triage.py` — 게이트: score ≥ 14 paper 전부 triage 분류 확인
- `scripts/phase3/check_block_parity.py` — preflight: en/ko 블록 구조 일치 검사
- `scripts/phase3/field_tooltips.py` — 뷰어 용 용어 툴팁
- `scripts/phase3/build_html.py` — 행성별 HTML (en + ko 미러, 토글)
- `scripts/phase3/disk_color_mie.py` — 잔해 벨트의 산란광 반사율 색 합성 (Bohren-Huffman Mie, 입자 크기 분포 + 조성 n,k, 등에너지 백색 균형 → sRGB hex). 입력: a_min/a_max/slope/composition/Teff. AU Mic 청색, Fomalhaut 회색 등 측정된 색 2건으로 검증. numpy only.
- `phase3/<system>/system.yaml` — planets, score thresholds, paper injections 선언형 설정

**드라이버.** `nearstars-phase3` 스킬이 절차를 정의합니다 (triage → 정독 → 합성 → 검증 → ko 미러 → 시각 확인).

**Audit pass.** 합성 배치가 끝나면 스킬은 외부 감사를 지시합니다 — 결정표의 각 행을 post-retrofit 정책 (mod-grounded fields, documented divergence) 에 대조합니다. 결과는 `phase3/<system>/audit-pass-<YYYY-MM-DD>.md` 에 수동으로 작성됩니다. 표준 예시는 `phase3/trappist_1/audit-pass-2026-05-22.md`.

**출력.** `docs/phase3/*.html`, `phase3/<system>/manual-paper-followup.md`, `phase3/<system>/audit-pass-*.md`.

## 4. 안정성 샌드박스

**목적.** 가상 위성이나 추가 행성을 Kopernicus / Principia cfg 에 박기 전에 동역학적으로 살아남는지 검증합니다. 큐레이션된 본 시스템의 기준 안정성 검사도 같이 됩니다.

**언제.** 위성·추가 바디를 후보로 올릴 때, 또는 출시 직전 큐레이션된 DB 의 sanity check.

**파일.**
- `phase3/stability-sim/scripts/load.py` — DB JSON → REBOUND `Simulation`
- `phase3/stability-sim/scripts/run.py` — WHFast + MEGNO 메인 엔트리
- `phase3/stability-sim/scripts/ring_clearing.py` — 위성 주변 고리 청소·간극 측정용 테스트 입자 시뮬. 공급 위성의 반장축을 둘러싸는 무질량 입자 원반을 깔고 적분한 뒤 어느 반경이 살아남는지 보고합니다(위성이 간극을 여는지, 묻힌 채 도는지). 폴리페무스의 Chaos 공급 E고리가 연속임을 확인하는 데 썼습니다(Chaos 질량비 μ≈7.5e-7 로 간극을 못 비움 — `results/_ring_clearing.log`).
- `phase3/stability-sim/hypotheticals/<system>.json` — 추가 바디 스펙

**스택.** `.venv/` 의 REBOUND 5.0, AU / yr / Msun 단위, 기본 horizon 10⁴ 년.

**출력.** `phase3/stability-sim/results/{system}_summary.json` + `_timeseries.csv`, `phase3/stability-sim/STABILITY_REPORT.md`.

## 5. 외부 교차검증

**목적.** DB 가 계산한 위치를 독립적인 출처와 대조합니다.

**파일.**
- `scripts/verification/stellarium_crosscheck.py` — DB 의 RA/Dec 를 Stellarium Web 과 비교

**출력.** 콘솔 diff 리포트.

## 6. Kopernicus cfg 생성

**목적.** `db/systems/` 와 Phase 3 합성을 Kopernicus `.cfg` 패치로 변환합니다.

**거리 범위.** ~50 ly (Kopernicus 의 지형 예산 한계).

**드라이버.** `kopernicus-cfg` 스킬.

**파일.**
- `.claude/skills/kopernicus-cfg/scripts/emit_kopernicus_cfg.py` — 일괄 emitter (v1.1, 2026-05-27). 범위: 항성 주위 disk Rings (별 body) + 행성 ring Rings (행성 body). `stars[0].raw.disk_measurements` + Phase 3 `disk_tint_rgb_hex` + `disk_opacity` 를 읽어 AU → body-radius multiplier 변환, 같은 belt 의 multi-paper merge 로 null 백필. 전체 Properties / Orbit / PQS / Atmosphere 는 여전히 `.claude/skills/kopernicus-cfg/references/*.md` 템플릿 따라 수동 작성.

**출력.** `dist/NearStars-Configs/Patches/Kopernicus/`.

## 7. Principia cfg 생성

**목적.** `db/systems/` 를 Principia 의 `gravity_model` + `initial_state` 패치로 변환해 n-body 중력을 구현합니다.

**거리 범위.** ~80 ly (지형 메시가 없어서 Kopernicus 보다 멀리까지).

**드라이버.** `principia-cfg` 스킬.

**출력.** `dist/NearStars-Configs/Patches/Principia/`.

## 8. Firefly cfg 생성

**목적.** Phase 3 대기 합성을 Firefly 의 `ATMOFX_BODY` cfg (재진입 플라즈마 색, 강도 multiplier, 입자 임계값) 로 변환하고, NearStars 의 대기 보유 천체 전체를 묶는 `ATMOFX_PLANET_PACK` 까지 함께 emit 합니다.

**언제.** "Firefly cfg 만들어줘", "이 행성 재진입 색", "ATMOFX_BODY", 재진입 플라즈마·shockwave·streak 화학 관련 질문.

**드라이버.** `firefly-cfg` 스킬. Firefly `mod_version: 1.0.6` (M1rageDev/Firefly, GPL-3.0) 에 핀. 모든 스키마 주장은 `ConfigManager.cs:line` 형태로 출처 인용.

**파일.**
- `.claude/skills/firefly-cfg/scripts/emit_firefly_cfg.py` — 제네릭 emitter: Phase 3 Decisions → ATMOFX_BODY + planet pack. Bulk-gas 팔레트 6종을 emitter 안에 박아두고, streak 종은 원소 DB 참조.
- `db/refs/element_plasma_colors.yaml` — 원소별 불꽃/플라즈마 hex DB (118 entries). Helmenstine 2017 차트의 그라디언트 픽셀 샘플링을 대체.
- `scripts/refs/validate_element_colors.py` — DB 스키마 점검.
- `scripts/refs/render_element_colors_doc.py` — companion doc 재렌더 (en + ko 미러).
- `docs/reference/element-plasma-colors.md` — 사람용 view (생성물, 직접 편집 금지).
- `scripts/refs/cie_color.py` — 공용 색측정 모듈. Planck 흑체 + CIE 1931 등색함수(Wyman 2013) + XYZ→sRGB hue + 스펙트럼→hex. 엔진과 온도-색 빌더가 함께 씀.
- `scripts/refs/build_atomic_lines.py` + `db/refs/atomic_lines.yaml` — 원자 라인·준위·이온화 데이터(H I, He I, C I/II, N I/II, O I/II, S I/II, Mg I/II, Ti I/II, V I/II, Fe I/II — 18종)를 NIST ASD(lines1.pl + energy1.pl)에서 받아 생성. H/He/C/N/O/S면 현실적 대기 화학(N2/O2/CO2/SO2/H2O/H2/He/CH4/NH3)을 사실상 다 덮고, Mg/Ti/V/Fe는 금속산화물 밴드 + 그 해리→원자 행진용. 추가는 같은 2줄 레시피로. 캐시 우선(`/tmp/nist`), `--refresh`로 실시간 재페치. LTE 엔진 입력.
- `db/refs/molecular_bands.yaml` — 분자 밴드 시스템(N2 1P/2P, N2+ 1NG, C2 Swan, CH/NH/OH, CN violet, CO Ångström, 금속산화물 TiO/VO/FeO/MgO) + 해리 평형용 Huber-Herzberg 상수. 밴드 헤드·항값은 Pearse & Gaydon / ExoMol / airglow 문헌. LTE 엔진 입력.
- `scripts/refs/saha_boltzmann.py` — 1차원리 LTE 플라스마 발광색 엔진. 열복사 연속 + 원자선 + 분자 밴드를 합치고 Saha 이온화·Boltzmann 들뜸·해리를 모두 계산. 직접 실행하면 자체검증 + 색 행렬 출력. LTE 한계 주의(공기 재진입 청보라는 비-LTE라 재현 안 됨, 문서화됨).
- `scripts/refs/build_plasma_temperature_colors.py` — 엔진을 돌려 조성별 온도분해 플라스마 색표(500K 간격) 생성. `_blackbody` 연속복사는 정확(Planck→CIE 1931), 조성색은 LTE 엔진 산출. cfg 입력이 아니라 레퍼런스/물리 도구. `--sanity`로 색 행렬 출력.
- `db/refs/plasma_temperature_colors.yaml` — 생성물: `_blackbody` 색온도표(1000–20000K) + 조성별 온도(1000–15000K) 색에 이온화·분자·방출 분율 + 우세 영역 라벨 포함.
- `scripts/refs/reentry_color.py` — 행성별 재진입 색을 **진입 속도** + 대기에서 산출. 속도→대표 충격층 온도 매핑(경험식, 공기 재진입에 앵커), 엔진 실행, **비-LTE 기본 ON**(빠른 진입 → 높은 전자온도 → N2 계열 청보라). 예 `--velocity 11 "N2:0.78,O2:0.21"` → 선명한 재진입 청색, `--velocity 5.5 "CO2:0.95,N2:0.05"` → 화성 그린. 의도한 행성별 색 선택기.
- `scripts/refs/emit_atmosphere_color.py` — 임의 대기 조성(분자 몰분율, 예 `"CO2:0.95,N2:0.05"`) → 온도별 LTE 플라스마 색. `--t-elec K`로 2온도 비-LTE 모드(N2 계열 청색). 원자분율 변환 + 분자 밴드 자동선택 + 엔진 실행(스펙트럼 레벨 혼합 후 CIE). 혼합 대기 색을 얻는 올바른 방법(색이 아니라 스펙트럼을 합침). 발광 원소는 H/He/C/N/O/S/Mg/Ti/V/Fe, 나머지는 드롭+재정규화. `--html`로 스와치.
- `scripts/refs/build_aurora_colors.py` + `db/refs/aurora_lines.yaml` + `db/refs/aurora_colors.yaml` — 비-LTE 오로라 색을 대기별 밀도(고도)로. 금지선 quenching `φ=A/(A+Σk·n)`(O ¹D 적/¹S 녹) + N₂ 밴드 → CIE, 축은 밀도(온도 아님 — 오로라는 비열적). 지구 적색(고)→녹색(중)→분홍(저) 층리 재현. aurora/EVE용이지 Firefly 재진입 아님.
- `scripts/refs/build_element_temperature_colors.py` + `db/refs/element_temperature_colors.yaml` — 원소별 플라스마 색을 온도별(500K 간격)로. 조성별 표의 원소 버전. 백열 대용 + 중성 및 1차이온(X II) 원자선 발광(Boltzmann)을 Saha 중성/이온 분율로 가중. 원자 전용, NIST A계수 있는 75개 원소(나머지 제외). 뷰어 주기율표를 구동. `validate_plasma_temp.py`가 구조 검증.
- `scripts/refs/build_molecular_temperature_colors.py` + `db/refs/molecular_temperature_colors.yaml` — 분자별 플라스마 색을 온도별(500K 간격)로. 원소 표의 분자 버전. 패널 30종을 각각 단일 조성으로 엔진에 돌림. 저온 밴드 → 해리 → 원자 → 이온. 엔진 미지원 원자(Cl/F/Si)는 드롭(`dropped` 플래그). 뷰어 분자 패널을 구동. `validate_plasma_temp.py`가 재현성 강제(오프라인 빌드).
- `scripts/refs/build_lte_plasma_colors.py` + `db/refs/lte_plasma_colors.yaml` — 원소별 계산 원자 발광색(주기율표 `lte_plasma` regime). A계수 있는 ~73개는 3500K Boltzmann(Na 노랑·Cu 초록), A 없는 복잡 스펙트럼(Zr·Nb·란타넘·악티늄)은 NIST 관측 세기 상위 N개로 채우고 저신뢰 플래그. 98/118 채움, At + 초중원소는 측정 스펙트럼 없음(null). curl 캐시 우선, **부하 시 NIST가 응답을 잘라서 순차·저동시성으로 받아야 함**. 이건 원자색이라 분자 불꽃색(CaOH·SrOH)과 다름 — 큐레이션 불꽃 regime 참조.
- `scripts/refs/render_color_visualizer.py` — `docs/firefly-colors.html` 렌더. 주기율표와 분자 패널은 **온도 슬라이더**(1000–15000K)로 색이 칠해짐(`element_temperature_colors` + `molecular_temperature_colors` 읽음). 움직이면 분자→원자→이온 행진이 보임. 아래 섹션은 조성/원소 온도 그리드, bulk/streak Firefly 팔레트, 태양계 **엔진 vs Firefly 기본 비교**, emit된 행성들, 오로라 **밀도 슬라이더** + 발광종 카탈로그(비-LTE).

**스킬 내 references.** 다섯 개 노드 타입 (`atmofx-body`, `atmofx-planet-pack`, `atmofx-part`, `atmofx-particles`, `atmofx-settings`), `color-format` (HDR), `composition-color` (대기 조성 → 재진입 팔레트, bulk-gas 플라즈마 표 기반), `phase3-mapping` (Phase 3 행 → Firefly 필드 매핑), `pitfalls`.

**출력.** `dist/NearStars-Configs/Patches/Firefly/<Body>.cfg` 행성당 1개 + `NearStarsPlanetPack.cfg`.

## 9. ResearchBodies cfg 생성

**목적.** 옵셔널 **discoverability** 레이어를 emit 합니다. 플레이어가 관측소/망원경으로 발견하기 전까지 NearStars 천체를 숨기는 `RESEARCHBODIES { loadAs = mod ... }` ModuleManager 패치입니다. 각 천체의 실제 검출 상태 (Phase 4 `identity > discoverability`) 를 `IGNORELEVELS` 시작-가시 튜플 + `ONDISCOVERY` 메시지로 매핑합니다 (후보 천체는 실제 검출 논문을 인용).

**언제.** "ResearchBodies cfg 만들어줘", "discoverability 패치", "IGNORELEVELS / ONDISCOVERY", "이 바디 숨김 처리".

**드라이버.** `researchbodies-cfg` 스킬. RB `mod_version: 1.13.0.0` (JPLRepo/ResearchBodies) 에 고정. 스키마 주장은 `<file>.cs:line` 인용. 난도 등급 = Scheme A, emit 은 프로젝트 말미로 보류. 타깃은 비-RP-1 (RSS 의 Sandbox/Science). RP-1 통합은 추후 업데이트로 보류 (`references/rp1-compat.md`).

**파일.**
- `.claude/skills/researchbodies-cfg/scripts/emit_researchbodies_cfg.py` — Phase 4 `discoverability:` 블록을 읽어 카테고리 → IGNORELEVELS 튜플 (Scheme A) 로 매핑, 단일 패치로 출력. `--dry-run` / `--input` 지원.

**출력.** `dist/NearStars-Configs/Patches/ResearchBodies/NearStars.cfg`.

## 10. 별 추가 / Phase 2 큐레이션

**목적.** 새 별을 추가하는 절차 (target list → fetch → 큐레이션 → 검증) 와 기존 별의 Phase 2 큐레이션 깊이를 올리는 절차.

**드라이버.** `nearstars-add-star` 스킬.

**파일.**
- `scripts/pipeline/apply_phase2.py` — 제네릭 applier. `phase2/<system>/measurements.yaml` 을 읽어 `stellar_props_curated.json` + `planets_curated.json` 에 머지. `--check` 플래그로 diff 만 확인 가능.
- `phase2/<system>/measurements.yaml` — Phase 2 측정 array 선언형 (논문별, recommended 플래그). 시스템당 한 파일. 기존 시스템별 `apply_phase2.py` 를 대체합니다.

**워크플로.** `target_list.json` 편집 → `./run_pipeline.sh` → Phase 2 격상 시 `phase2/<system>/measurements.yaml` 작성 → `python3 scripts/pipeline/apply_phase2.py <system>` → 재검증.

## 11. 개발 헬퍼

**목적.** 일상 작업에서 쓰는 보조 유틸리티.

**파일.**
- `scripts/preview-md.sh <md-file>` — 마크다운을 HTML 로 렌더해 브라우저에서 열기
- `scripts/check-mirrors.sh` — `ko/` 미러의 누락·구버전 상태 확인
- `scripts/check_dead_links.py` — 추적되는 모든 .md 파일의 상대 링크 깨짐 스캔
- `scripts/check_language.py` — 영문 source-of-truth 영역의 .md 파일 중 한글 dominant (25%+) 검출. `phase3/_audit/*` 는 allowlist.
- `scripts/check_build_freshness.py` — `docs/data.json` 이 최신 `db/systems/*.json` 보다 오래됐는지, `docs/reports.html` / `reports-manifest.json` 이 최신 `docs/phase{2,3}/*.html` 보다 오래됐는지 확인. 매니페스트의 고아 키 / dangling html 도 검사 (build_site.py 스킵 + 슬러그 컨벤션 drift 감지).
- `scripts/check.sh` — 릴리스 전 통합 점검. 스키마 검증 + 미러 상태 (stale 은 경고, missing 은 실패) + dead-link 스캔 + 컨벤션 점검 + 경로 마이그레이션 잔여물 점검 + 한글 dominant 검사 + 빌드 신선도. 수동 실행 전용.

## 12. 3D 성도 뷰어

**목적.** `db/systems/*.json` 을 브라우저용 인터랙티브 3D 지도로 만든다. 카탈로그가 공간상 *어디에* 있는지 보고, 시스템을 골라 줌인하면 그 행성들까지 본다.

**트리거.** "DB 3D로 시각화", "성도 만들어줘", 새 별·행성을 한 묶음 추가한 뒤.

**파일.**
- `scripts/viz/build_starmap.py` — `db/systems/` 를 읽어 중력적으로 구분되는 위치마다 마커 하나로 컴포넌트를 묶고(union-find 0.4 ly, `binary_orbit_ref` 로 가드), Teff 에서 흑체 RGB·광년 ICRS 좌표·광도 기반 마커 크기를 베이크한다. 태양계(canonical 하드코딩 요소)를 원점에 주입한 뒤 자기완결 뷰어를 emit. `--self-check` 는 파일을 쓰지 않고 카운트만 검증.
- `scripts/viz/starmap_template.html` — Three.js 뷰어 템플릿(CDN importmap). 빌더가 임베드 JSON 페이로드를 끼워 넣는다.

**출력.** `docs/starmap.html` — 단일 자기완결 파일, GitHub Pages 호스팅 가능. 광년 스케일 맵 뷰(원점에 태양, ICRS 거리 링, 분광형 범례, 거리 필터, 50광년 밖 토글), 클릭하면 정보 패널, 더블클릭하면 AU 스케일 시스템 뷰로 들어가 행성 궤도를 본다. 한/영 UI 토글.

**서빙.** `cd docs && python3 -m http.server` 후 `http://localhost:8000/starmap.html` 열기 (CDN 모듈은 `file://` 가 아니라 http 필요).

**참고.** 색은 지각적 흑체 근사(보정된 SED 아님), 마커 크기는 광도 proxy(물리 반경 아닌 빌보드). 표 형태 DB 브라우저인 `docs/index.html`(2번 툴)과 별개로, 이쪽은 공간 배치를 본다.

**관련 — 폴리페무스 위성계 뷰어.** `phase4/polyphemus-moon-viewer.html` 은 α Cen A b(폴리페무스) 위성계 + 고리 설계를 보는 독립형 인터랙티브 3D 뷰어다. 명명 5위성(Dante·Hades·Pandora·Cassandra·Chaos), 경사·승교점, 흐릿한 Chaos 공급 E고리를 시각화한다. 카탈로그 전체 성도와 별개인 Phase 4 아트디렉션 보조 도구로, `phase4/alpha_centauri.yaml` 에 기록된 게이트 통과 로스터를 그려 보여준다. **동결(2026-06-22):** 설계 탐색 임무가 끝나(로스터·고리·obliquity 확정) 아티팩트로 보존하며, 이후 결정은 여기 동기화하지 않는다. 성도에 없는 고유 기능은 Pandora 지표 1인칭 시점+일식뿐이고, canonical·유지보수 시각화는 `docs/starmap.html` 이다.

## 스킬 디렉터리 배치

라이브 스킬은 모두 `.claude/skills/<name>/` 아래에 둡니다. `.agents/skills/` 는 `<name>-workspace/` 빌드 환경과 gitignored Patreon-EA 스킬 (scatterer, eve, volumetrics) 전용입니다.

| 스킬 | 위치 |
|------|------|
| `kopernicus-cfg` | `.claude/skills/kopernicus-cfg/` |
| `principia-cfg` | `.claude/skills/principia-cfg/` |
| `firefly-cfg` | `.claude/skills/firefly-cfg/` |
| `nearstars-add-star` | `.claude/skills/nearstars-add-star/` |
| `nearstars-phase3` | `.claude/skills/nearstars-phase3/` |
| `find-skills` (범용) | `.claude/skills/find-skills/` |

`.agents/skills/firefly-cfg-workspace/` 와 `nearstars-phase3-workspace/` 는 해당 라이브 스킬의 빌드 환경 — 별개의 스킬이 아니라 작업 디렉터리입니다.

## 의존 그래프

```
target_list.json
     ↓
[1] 데이터 엔진 ──→ db/systems/*.json
                          │
                          ├──→ [2] HTML 뷰어 ─────→ docs/
                          │
                          ├──→ [3] Phase 3 합성 ───→ docs/phase3/
                          │
                          ├──→ [4] 안정성 샌드박스 ──→ phase3/stability-sim/results/
                          │
                          ├──→ [5] Stellarium 교차검증
                          │
                          ├──→ [6] kopernicus-cfg ──→ dist/.../Kopernicus/
                          │
                          ├──→ [7] principia-cfg ──→ dist/.../Principia/
                          │
                          └──→ [8] firefly-cfg (대기 보유 천체만) ──→ dist/.../Firefly/

[9] nearstars-add-star — 새 별에 대해 위 체인 전체를 구동하는 절차
[10] 개발 헬퍼 — 체인과 직교
```

## 관련 문서

- [methodology](methodology.md) — 클러스터 허브. 데이터 엔진과 검증 툴이 이 방법론을 문서화
- [adding_stars](adding_stars.md) — 여기 있는 스크립트 인덱스를 활용하는 실무 시퀀스
- [mod-reference](mod-reference.md) — 다운스트림 모드 측 툴
- [guideline](guideline.md) — 툴들의 컨텍스트가 되는 프로젝트 범위 (단계, 거리 한계)
