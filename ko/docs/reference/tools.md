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
| 9 | 별 추가 / Phase 2 큐레이션 | 새 별 DB 진입 절차 | `nearstars-add-star` 스킬 |
| 10 | 개발 헬퍼 | 마크다운 미리보기, ko/ 미러 정합성 | `scripts/preview-md.sh`, `scripts/check-mirrors.sh` |

## 검증 & QA — 인덱스

정확성 검사 도구들은 기능별 묶음 여러 곳에 흩어져 있습니다. 이 표는 그것들을 한 자리에 모아 가시성을 확보합니다 — 각 툴은 자기 묶음 섹션에도 그대로 등장합니다.

| 검증 대상 | 툴 / 활동 | 묶음 | 언제 실행 |
|----------|----------|:----:|----------|
| `db/systems/*.json` 의 스키마 무결성 | `scripts/pipeline/validate.py` | [1](#1-데이터-엔진) | 빌드 직후 (`run_pipeline.sh` 가 자동 호출) |
| 위계적 다성계 구조 | `scripts/pipeline/test_hierarchical.py` | [1](#1-데이터-엔진) | 다성계 궤도 편집 후 smoke test |
| Stellarium 과 비교한 DB 위치 | `scripts/verification/stellarium_crosscheck.py` | [5](#5-외부-교차검증) | 퍼블리시 전 spot-check |
| 큐레이션된 + 가상 바디의 동역학적 안정성 | `phase3/stability-sim/scripts/run.py` | [4](#4-안정성-샌드박스) | 위성·추가 바디 cfg 출시 전, 혹은 기준 DB sanity 확인 |
| `ko/` 미러 파일 정합성 | `scripts/check-mirrors.sh` | [10](#10-개발-헬퍼) | 커밋 / 릴리스 전 |
| Phase 3 합성 정책 적합성 | `nearstars-phase3` 의 audit-pass 절차 | [3](#3-phase-3-합성-파이프라인) | 합성 배치 후 — 수동, 결과는 `phase3/<system>/audit-pass-<YYYY-MM-DD>.md` |

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
- `scripts/phase3/score_papers.py` — 들어오는 bibcode triage
- `scripts/phase3/fetch_arxiv_texts.py` — arXiv 에서 전문 PDF 수집
- `scripts/phase3/build_bibliography.py` — bibcode → reference 딕셔너리
- `scripts/phase3/build_manual_fetch.py` — 수동 다운로드 필요 논문 목록 작성
- `scripts/phase3/expand_citations.py` — 합성문에 인용 인라인 삽입
- `scripts/phase3/field_tooltips.py` — 뷰어 용 용어 툴팁
- `scripts/phase3/build_html.py` — 행성별 HTML (en + ko 미러, 토글)
- `phase3/<system>/add_missing_papers.py` — 시스템별 후속 추가

**드라이버.** `nearstars-phase3` 스킬이 절차를 정의합니다 (triage → 정독 → 합성 → 검증 → ko 미러 → 시각 확인).

**Audit pass.** 합성 배치가 끝나면 스킬은 외부 감사를 지시합니다 — 결정표의 각 행을 post-retrofit 정책 (mod-grounded fields, documented divergence) 에 대조합니다. 결과는 `phase3/<system>/audit-pass-<YYYY-MM-DD>.md` 에 수동으로 작성됩니다. 표준 예시는 `phase3/trappist_1/audit-pass-2026-05-22.md`.

**출력.** `docs/phase3/*.html`, `phase3/<system>/manual-paper-followup.md`, `phase3/<system>/audit-pass-*.md`.

## 4. 안정성 샌드박스

**목적.** 가상 위성이나 추가 행성을 Kopernicus / Principia cfg 에 박기 전에 동역학적으로 살아남는지 검증합니다. 큐레이션된 본 시스템의 기준 안정성 검사도 같이 됩니다.

**언제.** 위성·추가 바디를 후보로 올릴 때, 또는 출시 직전 큐레이션된 DB 의 sanity check.

**파일.**
- `phase3/stability-sim/scripts/load.py` — DB JSON → REBOUND `Simulation`
- `phase3/stability-sim/scripts/run.py` — WHFast + MEGNO 메인 엔트리
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

**스킬 내 references.** 다섯 개 노드 타입 (`atmofx-body`, `atmofx-planet-pack`, `atmofx-part`, `atmofx-particles`, `atmofx-settings`), `color-format` (HDR), `composition-color` (대기 조성 → 재진입 팔레트, thunderchild 차트 + bulk-gas 플라즈마 표 기반), `phase3-mapping` (Phase 3 행 → Firefly 필드 매핑), `pitfalls`.

**출력.** `dist/NearStars-Configs/Patches/Firefly/`.

## 9. 별 추가 / Phase 2 큐레이션

**목적.** 새 별을 추가하는 절차 (target list → fetch → 큐레이션 → 검증) 와 기존 별의 Phase 2 큐레이션 깊이를 올리는 절차.

**드라이버.** `nearstars-add-star` 스킬.

**파일.**
- `phase2/<system>/apply_phase2.py` — 시스템별 스크립트. 논문별 측정치를 `db/planets_curated.json` (array form, recommended 플래그 포함) 에 적재합니다. 특정 시스템을 Phase 1 → Phase 2 로 격상할 때 실행합니다.

**워크플로.** `target_list.json` 편집 → `./run_pipeline.sh` → `stellar_props_curated.json`·`planets_curated.json`·`binary_orbits.json` 수동 큐레이션 (또는 논문 배치 스크립트가 있는 시스템은 `apply_phase2.py` 실행) → 재검증.

## 10. 개발 헬퍼

**목적.** 일상 작업에서 쓰는 보조 유틸리티.

**파일.**
- `scripts/preview-md.sh <md-file>` — 마크다운을 HTML 로 렌더해 브라우저에서 열기
- `scripts/check-mirrors.sh` — `ko/` 미러의 누락·구버전 상태 확인

## 스킬 디렉터리 배치

프로젝트 전용 스킬은 현재 두 트리에 병행 배치되어 있습니다 — 추후 통합 예정.

| 스킬 | `.claude/skills/` | `.agents/skills/` |
|-----|:----:|:----:|
| `kopernicus-cfg` | ✓ | ✓ |
| `principia-cfg` | ✓ | — |
| `firefly-cfg` | — | ✓ |
| `nearstars-add-star` | ✓ | ✓ |
| `nearstars-phase3` | — | ✓ |
| `find-skills` (범용) | ✓ | ✓ |

`.agents/skills/` 의 `firefly-cfg-workspace/` 와 `nearstars-phase3-workspace/` 는 해당 라이브 스킬의 빌드 환경 — 별개의 스킬이 아니라 작업 디렉터리입니다.

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
