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
| 13 | Phase 4 보드 도구 | 결정 보드 검증(emit 게이트) + 바디별 보드 HTML 렌더 | `scripts/check_phase4_gate.py`, `scripts/phase4/build_phase4_html.py` |
| 14 | 방사선대 + 도출값 계산기 | 벨트 단면, Kerbalism 이미터, `scripts/refs/` 방법론 계산기 | `scripts/viz/render_belts_bodies.py`, `scripts/refs/*.py` |
| 15 | 표면 얼음 안정성 | 노출된 얼음(6종)이 이 일사량에서 존속하는가? 알베도 → 손실률·수명·lag 맨틀 깊이 | `docs/ice-stability.html` |
| 16 | 자기장 기하(쌍극 vs 다중극) | 자오면 자기력선 + 표면 B_r 지도 + 열린 자기력선 추적 오로라 발자국. Ro_l 게이트의 *형태* 귀결 | `scripts/viz/render_field_geometry.py` |
| 17 | 사이트맵 + 연결성 감사 | 발행 페이지 인벤토리, 허브, 고아·막다른·CDN 결함 | `scripts/build_sitemap.py` |

## 일회성 설명물 — 인덱스

이 저장소의 시각화는 두 종류이고 관리 방식이 다릅니다. **상시 도구**는 입력이 바뀌면 다시 생성됩니다.
DB 브라우저, 성도, 벨트 뷰어, 색·얼음 계산기가 그렇습니다. **일회성 설명물**은 큐레이션 중 한 가지
논점을 매듭짓기 위해 만든 것이고 데이터가 움직여도 다시 만들지 않습니다. 각각은 그때 그 논증의
스냅숏이며, 도출값 뒤의 근거를 눈으로 확인할 수 있어야 하기에 남겨 둡니다. 이 인덱스는 두 번째
종류를 모은 것입니다. 각 항목은 아래 해당 그룹에도 문서화돼 있고, 전부
[`docs/tools.html`](../../../docs/tools.html)에서 같은 구분으로 열립니다.

| 설명물 | 산출물 | 매듭지은 질문 | 그룹 |
|---|---|---|:-:|
| 천왕성 pole-on 기하 | [`uranus-geometry.html`](../../../docs/uranus-geometry.html) | Voyager 2 단일 통과가 천왕성 자기꼬리를 대표하지 못할 수 있는 이유 | 14 |
| 자기장 형상 — 쌍극 vs 다중극 | [`img/field-geometry.png`](../../../docs/img/field-geometry.png) | 다중극 자기장이 세기가 아니라 *모양*으로 어떻게 보이는가 | 14 |
| 프록시마 d 알펜 윙 | [`img/proxima-d-alfven-wing.png`](../../../docs/img/proxima-d-alfven-wing.png) | sub-Alfvénic 항성-행성 상호작용 기하. 꼬리가 아니라 날개 | 14 |
| 알펜 날개 해부 | [`img/alfven-wing-anatomy-ganymede.png`](../../../docs/img/alfven-wing-anatomy-ganymede.png) | 날개의 기울기·굵기·처짐·접촉부를 한 장에 | 14 |
| 페트로바선 — 기하 | [`img/petrova/petrova-geometry.png`](../../../docs/img/petrova/petrova-geometry.png) | 꺾임점이 어디이고 왜 문턱값이 필요 없는가 | 14 |
| 페트로바선 — 채움 | [`img/petrova/petrova-aurora-exterior.png`](../../../docs/img/petrova/petrova-aurora-exterior.png) | 볼류메트릭 마칭으로 낸 커튼 드레이프, 영화 스틸에 맞춤 | 14 |
| 페트로바선 — 허리 | [`img/petrova/petrova-waist.png`](../../../docs/img/petrova/petrova-waist.png) | 가장 얇은 구간을 옆에서·안에서 | 14 |
| 위성 대기 보유 가능성 | [`img/moon-atmosphere-feasibility.png`](../../../docs/img/moon-atmosphere-feasibility.png) | 프록시마 c I 이 대기를 붙잡을 수 있는가 | 4 |
| 프록시마 c 계 실척 | [`img/proxima-c-system-to-scale.png`](../../../docs/img/proxima-c-system-to-scale.png) | 고리·벨트·위성 궤도가 실제로 서로 어떻게 놓이는가 | 4 |
| 프록시마 c I 궤도 — edge 비교 | [`img/proxima-c-i-orbit-edge-compare.png`](../../../docs/img/proxima-c-i-orbit-edge-compare.png) | c I 의 내측 대 외측 벨트 가장자리 궤도와 각각이 만드는 편평도 | 4 |

`img/field-geometry-proxima-c.png` 도 존재하지만 어디서도 참조되지 않습니다. 누가 쓰겠다고 하기
전까지는 잔여물로 봅니다.

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
| Phase 4 보드 스키마 v2 / emit-게이트 정합성 | `scripts/check_phase4_gate.py` | [13](#13-phase-4-결정-보드-도구) | 보드를 고칠 때마다 — `scripts/check.sh` 게이트 8에서 호출 |
| 논문 캐시: 이 논문을 보유 중인가? (bibcode **와** arXiv 이름, 하위 폴더) | `scripts/refs/check_paper_held.py <bibcode …>` · `--scan <doc.md …>` | [11](#11-개발-헬퍼) | 필요할 때만, `check.sh` 에는 넣지 않음. 캐시가 파일을 bibcode *또는* arXiv id 로 이름 짓고 일부는 하위 폴더에 두므로, bibcode 접두 glob 하나가 2026-09-03/04 에 거짓 미보유 여섯을 만들었다(RM22 · Nettelmann 2011 · Reiners & Christensen · Garraffo · Yadav & Thorngren · Zhang & Rogers). 설치 당일(2026-09-04) 자체 결함 둘. 구형 arXiv id(`astro-ph/0103383` → `astro-ph_…`, 캐시 이름 52개)를 못 잡아 거짓 미보유를 막으려던 도구가 Burrows+ 2001 에 거짓 미보유를 냈고, ABSENT 줄이 "무엇을 대조했는지" 출력하기 때문에 잡혔다(그 형식은 유지). 또 "보유" 가 "파일 존재" 였는데 캐시 이름 셋이 arXiv 초록 페이지라, 이제 본문(pdf · `ltx_document` html · 2 KB 넘는 md)이 있어야 HELD 이고 아니면 **ABSTRACT-ONLY**(ABSENT 와 구분). arXiv id 는 ADS 의 `identifier` 필드에서 **읽는다**(`ADS_API_TOKEN` 필요, 없으면 추측하지 않고 종료). 게이트에 안 넣는 이유: 토큰 없는 환경에서 게이트가 죽고, 이 도구의 부정은 캐시 상태이지 저장소 결함이 아니다. 두 다이나모 문서 `--scan`: 10 중 7 보유, 그중 4 가 arXiv 이름. |
| 논문 캐시: `.md` 렌더가 떨어뜨린 표 | `scripts/check_paper_tables.py` | [11](#11-개발-헬퍼) | 필요할 때만, `check.sh` 에는 넣지 않음 — 재확인 목록(값을 어느 렌더에서 읽었나)이지 결함 목록이 아님. gitignored 캐시의 두 렌더가 필요 |

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
- `phase3/stability-sim/scripts/ring_clearing.py` — 위성 주변 고리 청소·간극 측정용 테스트 입자 시뮬. 공급 위성의 반장축을 둘러싸는 무질량 입자 원반을 깔고 적분한 뒤 어느 반경이 살아남는지 보고합니다(위성이 간극을 여는지, 묻힌 채 도는지). A b의 A b V(Chaos) 공급 E고리가 연속임을 확인하는 데 썼습니다(A b V 질량비 μ≈7.5e-7 로 간극을 못 비움 — `results/_ring_clearing.log`).
- `scripts/pipeline/phase3_decisions.py` — `docs/phase3/<slug>.md`의 `## Decisions` 표 공용 파서(3→4/3→emit 기계 인터페이스, [pipeline-contract](pipeline-contract.md) §1). 기존 emitter 정규식이 조용히 덮어쓰던 qualifier 중복 라벨(`equilibrium_temp_k (A=0)` vs `(A=0.3)`)을 보존한다. 소비자는 `check_pipeline_flow.py`·`resolve_emit_values.py`이고, emitter 스킬은 emit 재배선 때 이 모듈로 갈아탄다.
- `scripts/check_pipeline_flow.py` + `db/roster.yaml` — check.sh 게이트 10. phase4 `body:` 키 ↔ db 이름 대조(창작 바디는 `discoverability=fictional`로 통과), 확정 로스터 완결성 매트릭스(보드·보드 행 커버리지·phase3 리포트 — 갭은 경고, 구조 위반은 실패), 전 phase3 리포트 Decisions 표 파싱 검증. `db/roster.yaml`이 확정 세트의 단일 데이터 소스이며 emit 범위도 이걸 읽는다.
- `scripts/pipeline/field_alignment.yaml` — phase4 메뉴명 ↔ phase3 Decisions 키 ↔ cfg 타깃 정렬표([pipeline-contract](pipeline-contract.md) §3). 생성물이 아니라 손으로 큐레이션하는 계약 데이터다. 보드는 오너의 선택을 단위 없이 적고(`mass`) Decisions는 단위를 키에 박으므로(`mass_msun`/`mass_mearth`), 항목마다 후보 phase3 키를 우선순위 순으로 + 바디 클래스별 함의 단위를 함께 적는다. `resolve_emit_values.py`가 읽어 phase4-over-phase3 오버라이드를 실제로 발동시키고, 게이트 10f가 커버리지를 검사한다.
- `scripts/pipeline/resolve_emit_values.py` — emit 값 해석기. 세 저장소가 만나는 단일 지점([pipeline-contract](pipeline-contract.md) §3)으로, 바디별로 db → phase3 Decisions(공용 파서) → phase4 `fields[]`(gated/emitted 행, `*` 와일드카드는 db 행성 전체 적용)를 레이어 머지한다. 창작 바디는 phase4 단독으로 해석. 드라이런 전용 — emitter들은 emit 재배선 때 이 출력을 읽는다(`phase4/emit-hardening/checklist.md`). `python3 scripts/pipeline/resolve_emit_values.py <board_stem> [--json]`.
- `scripts/retrofit_paper_links.py` — **one-shot(멱등)**. CONVENTIONS §3.3 일괄 변환 — md 본문의 맨 논문 id를 마크다운 링크로(bibcode→ADS, `arXiv:` 접두→arXiv, 맨 arXiv id는 `_bib/*.yaml` 화이트리스트에 있을 때만; 코드 스팬·펜스·frontmatter·기계 필드는 보호). 2026-07-20 실행, 217개 파일에 링크 1,967개. 변환된 링크는 보호 스팬이라 재실행해도 안전하다.
- `phase3/stability-sim/scripts/plot_orbits.py` — **행성 레벨** 런용 경량 2패널 PNG(top-down 궤도 + 이심률(t)). `results/<label>_summary.json` + `_timeseries.csv`를 읽어 `<label>_orbits.png`를 생성한다. summary에 MEGNO가 있어야 하며, leapfrog·trace 런이나 위성계는 표준 4패널인 plot_moons.py를 쓸 것. `python3 scripts/plot_orbits.py [label]`.
- `phase3/stability-sim/scripts/plot_moons.py` — **궤도분석 표준 시각화**(정적 4패널 PNG: top-down 궤도 / 이심률(t) / 반장축 드리프트 Δa/a₀(t) / 시뮬 기준면 경사(t)), 상단 제목에 판정 + 적분기 + dt + |ΔE/E| + 위성별 최대 Hill 비율. 시뮬 출력만으로 두 계층 다 처리 — 행성-중심(위성, R_p)이나 별-중심(행성, AU)을 `--center`로 선택(기본: 위성 있으면 부모, 없으면 별). `<label>_orbits.png` 생성. 행성 전용 `plot_orbits.py`와 달리 leapfrog·trace 런(megno=None)도 처리. `--theme light`는 사이트 `<picture>` 교체용 `<label>_orbits_light.png` 짝을 만든다(plasma의 노란 끝은 흰 배경에서 날아가므로 팔레트 범위를 당긴다). `--dir <결과폴더> [--label <시스템>] [--center <천체>] [--theme dark|light]`.
- `phase3/stability-sim/scripts/plot_interactive.py` — **인터랙티브** 4패널 뷰어(Plotly, self-contained HTML). plot_moons.py와 같은 패널·데이터지만 범례 클릭으로 천체를 전 패널 동시 토글, 호버로 정확한 값, 박스줌·팬으로 조밀한 내위성 분리. 브라우저의 `prefers-color-scheme`을 그대로 따라간다(실시간 반영, 토글 버튼 없음 — 사이트 전체가 같은 방식이라 버튼으로 한 번 더 묻던 것을 뺐다). plasma 팔레트(다른 뷰어와 통일). `--dir <결과폴더> [--label <시스템>] [--center <천체>]`.
- `phase3/stability-sim/validation-manifest.yaml` — 시스템별 **검증 매트릭스** 단일 소스. 어떤 계층을 가진 시스템인지, 정확 적분기는 무엇인지, 플레이 구간은 얼마인지, 그리고 `long_inner_orbits`(장기 구간은 연수가 아니라 가장 안쪽 궤도 바퀴 수로 세며 기준은 딱 떨어지는 1e8. 위성 계층은 10⁴년 예외 유지)를 담습니다. 페이지 산문(한/영)도 여기 들어갑니다.
- `phase3/stability-sim/scripts/validate_orbits.py` — 검증 세트 드라이버. 매니페스트의 각 시스템을 `행성계|위성계 × leapfrog|정확적분` 셀로 펼쳐, 기준 구간에 못 미치는 셀만 다시 돌리고(정확 셀은 몇 시간씩 걸리므로 도달 연수로 stale 판정), 각각을 렌더한 뒤 `docs/phase4/orbit-viewers/<slug>/index.html`와 시스템 인덱스를 씁니다(궤도 뷰어 전체가 여기로 합쳐졌습니다 — 옛 `build_viewers.py` 갤러리는 같은 leapfrog 적분을 애니메이션용으로 촘촘히 샘플하려고 한 번 더 돌리던 것이라, 그 런이 leapfrog 셀 자체가 되었습니다 — 스냅샷은 균일 10,000개로, 어느 계층이든 장주기 세차가 살아나면서 애니메이션(`anim_years` 창)에도 200프레임쯤 남습니다). 장기 구간과 위성 질량 합산은 시스템마다 유도합니다. 갤러리 인덱스는 결과가 있는 매니페스트 시스템을 항상 전부 싣기 때문에, `--systems`로 좁혀도 실행 대상만 줄고 사이트가 깎이지는 않습니다. 셀끼리 독립이고 REBOUND는 런 하나당 싱글스레드라 `--jobs N`으로 N개를 동시에 돌립니다(코어 하나씩, 로그는 `<cell-dir>/run.log`). `--systems`·`--cells`·`--force`·`--jobs`·`--pages-only`·`--dry-run`.
- `phase3/stability-sim/scripts/hades_rescue_scan.py` — **궤도 구제 스캐너**. 가상 위성(α Cen의 Hades)의 요소 하나를 목록대로 훑으면서 후보마다 검증 셀과 같은 설정으로 10⁵년을 돌리고, 판정을 양옆 위성과의 저차 공명 위치와 나란히 표로 냅니다. 완주한 후보는 건너뛰므로 중간에 끊겨도 그대로 이어집니다. `--grid MIN:MAX:STEP`(반장축 km)·`--vary FIELD:v1,v2`(`a|e|i|ma`)·`--combo f=v,f=v`·`--jobs N`. 결과와 결론은 `results/hades_rescue/README.md`에 있습니다.
- `phase3/stability-sim/scripts/plot_rescue_scan.py` — 위 스캔의 생존 지형도. 후보별 최대 이심률을 그 판정을 설명하는 공명 빗살 위에 얹어 그립니다(`plot_moons.py`가 런 하나를 그리는 반면 이쪽은 스캔 전체). 사이트 두 팔레트로 스캔 디렉토리에 저장합니다. `[--theme dark|light|both]`.
- `phase3/stability-sim/scripts/verify_j2c.py` — C로 컴파일한 J2 힘(`j2force.c` + `j2c.py`, stride 버그 수정 후 기본값)의 인수 검사. α Cen 위성계를 C 힘과 파이썬 콜백으로 각각 만들어 모든 입자의 위치·속도를 **비트 단위로** 비교합니다(leapfrog 런과 ias15+MEGNO 런 두 가지 — 후자는 `init_megno`가 일으키는 입자 배열 재할당까지 검증). 속도 향상(실측 27.6배 / 9.2배)도 같이 보고합니다. 두 파일을 건드렸으면 이걸 돌리고, `STAB_J2_C=0`으로 파이썬 경로를 강제할 수 있습니다.
- `phase3/stability-sim/hypotheticals/<system>.json` — 추가 바디 스펙

**스택.** `.venv/` 의 REBOUND 5.0, AU / yr / Msun 단위, 기본 horizon 10⁴ 년. Principia와 동일한 방식의 런은 `--integrator leapfrog --dt-minutes 10`(Principia의 고정 10분 ephemeris 스텝 모사)을 씁니다.

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
- `scripts/make_placeholder_textures.py` — emit 된 항성 body 가 참조하는 텍스처 경로에 임시 `<Body>_Sunspots.dds` / `<Body>_Corona.dds` (무압축 64×64 A8R8G8B8) 를 써넣습니다. 실제 아트가 나오기 전에도 테스트 빌드가 로드되게 하는 용도이고, 바디 목록은 emit 된 `stars.cfg` 에서 읽으므로 emitter 실행 뒤에 돌립니다.

**출력.** `dist/NearStars-Configs/Patches/Kopernicus/`, `dist/NearStars-Textures/PluginData/`.

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
- `scripts/refs/migrate_element_db_v2.py` — **일회용 마이그레이션, 재실행 금지**(`element_plasma_colors.yaml`를 v1 → v2 멀티-regime 스키마로, 산출물 커밋 완료). 각 원소의 평평한 hex를 `regimes.atomic_flame` 블록으로 감싸고, `hex_basis`를 cie_computed(큐레이션한 NIST 라인에서 계산) / canonical_descriptor(명명된 불꽃색) / chart_approx(Helmenstine 차트 폴백)로 태깅. 마이그레이션 이후 편집은 v2 YAML에 바로 들어감.
- `scripts/refs/populate_reentry_aurora.py` — **일회용 채움(멱등), 산출물 커밋 완료**. 대기 관련 종에 `reentry_plasma`(~8000–15000K, X I + X II 이온 + 연속복사)와 `aurora`(금지선 O I 녹/적 + N2+ 밴드) regime을 추가하고, 다원자 분자는 `not_emitter` + 해리 주석을 붙임. v2 마이그레이션 뒤에 실행.
- `scripts/refs/populate_phosphor_emission.py` — **일회용 채움, 산출물 커밋 완료**. 란타넘족에 `phosphor_emission` regime(고체 호스트 속 Ln3+ — 디스플레이 업계의 희토류 형광체 색)을 추가해, `atomic_flame`은 대체로 희미한 기상(gas-phase) Ln 화학에 솔직하게 남겨둠. 출처는 Phosphor Handbook(2007), Blasse & Grabmaier(1994).
- `scripts/refs/populate_tier_c_upgrades.py` — **일회용 재분류(멱등), 산출물 커밋 완료**. 분광 재검토 후 `chart_approx` 원소 항목을 canonical_descriptor(명명된 불꽃색) / cie_computed(뚜렷한 NIST 가시선) / not_visible_to_humans(UV·IR 우세)로 격상·격하. v2 마이그레이션 뒤에 실행.
- `scripts/refs/populate_spectro_refinements.py` — **일회용 정밀화, 산출물 커밋 완료**. 2026-05-26 서브에이전트의 NIST + 형광체 문헌 검토를 `chart_approx` 항목에 반영. 여섯 건의 실질 재분류(예 Zr→brilliant white, Gd/Yb→비가시, Tm→cie_computed 청색)와 란타넘·내화금속 약 13개 항목의 basis만 솔직하게 고치는 수정. 출처는 NIST ASD, Phosphor Handbook, Conkling *Pyrotechnics*.
- `scripts/refs/build_molecular_db.py` + `db/refs/molecular_plasma_colors.yaml` — 원소 색 DB의 분자 버전을 만드는 재생성 가능 빌더. 분자별 `reentry_plasma` + `aurora` CIE 계산색(또는 CO2/NH3/CH4처럼 광해리하는 다원자 분자는 `not_emitter` + `dissociation_products`). 원자 원소 DB가 놓치는 분자 밴드 시그니처를 담음. `wavelength_to_rgb.py` 사용.
- `scripts/refs/cie_color.py` — 공용 색측정 모듈. Planck 흑체 + CIE 1931 등색함수(Wyman 2013) + XYZ→sRGB hue + 스펙트럼→hex. 엔진과 온도-색 빌더가 함께 씀.
- `scripts/refs/wavelength_to_rgb.py` — 재생성 가능한 **라이브러리 모듈**. Bruton 1996 조각별 파장 → sRGB(`wavelength_to_rgb`), 세기 가중 가산 라인 혼합(`mix_lines`), `rgb_to_hex`. "스펙트럼 라인이 디스플레이에서 어떤 색으로 보이나" 경로(cie_color.py의 색측정용 CIE 1931과는 구분됨). cie_color.py, build_molecular_db.py, element-DB migrate/populate 스크립트들, phase3/build_html.py가 import.
- `scripts/viz/render_moon_atmosphere.py` — 대형 위성 대기 성립성 그림(`docs/img/moon-atmosphere-feasibility.png`). "이 위성이 대기를 붙잡을 수 있나"를 3패널로 답한다. (A) 모행성 반지름 단위 계 배치에 고리와 **동기궤도선**(그 안쪽이면 포보스처럼 조석으로 감겨 들어감), (B) 같은 축척으로 그린 위성 크기 비교, (C) 반지름 대 표면온도 보유 도표에 Jeans `λ = GMμ/kTR`의 25/60 등고선과 실측 천체(타이탄 125·가니메데 115·트리톤 93·명왕성 62·카론 11·엔셀라두스 1.3). 보유는 필요조건일 뿐이라는 주석도 함께 담는다(가니메데는 보유 영역인데 110 K에서 N₂ 얼음이 불안정해 공급원이 없어 대기가 없다). 프록시마 c I 크기 결정을 위해 만들었고, 위성 대기 판단 전반에 쓴다. `--scale` 를 주면 실제 비율 계 도면도 그린다(`docs/img/proxima-c-system-to-scale.png`). 프록시마 c와 2중 고리 띠, 얼음 Roche 한계, 동기궤도, 방사선 외대, 두 후보 궤도의 c I을 모두 같은 축척으로 그리고, c I 확대 인셋과 c I 하늘에서 본 c의 겉보기 크기(4 R_c 28.9°, 7 R_c 16.4°, 지구에서 본 달 0.52° 대비)를 함께 담는다. `--all` 은 두 그림 모두. 세 번째 모드 `--edge` 는 벨트 안쪽/바깥쪽 경계 궤도 비교를 그린다(`docs/img/proxima-c-i-orbit-edge-compare.png`). 두 후보 궤도를 나란히 놓고 모행성 자전이 정하는 동기궤도선과, 궤도가 만들어내는 편평도 차이를 함께 보여준다(q_s는 크기가 아니라 궤도에 의존).
- `scripts/refs/body_figure.py` — 천체 형상 계산기(근거: `docs/reference/body-figure-methodology.md`). Radau–Darwin 자전 `J2`, 동기 조석 `C22`, 천체마다 시딩된 Kaula 스펙트럼 고차 지오이드, 그리고 `ellipsoid_ratios()` → VertexHeightOblateAdvanced `CustomEllipsoid` a:b:c 시각 emit. 캘리브레이션 자체검증이 Earth/Jupiter/Callisto를 재현(`python scripts/refs/body_figure.py`).
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
- `scripts/refs/stellar_photospheric_color.py` — `docs/reference/stellar-photospheric-color-methodology.md`를 뒷받침하는 재생성 가능 도구. Teff·스펙트럼형 → 가시 sRGB 광구 색조를 공용 `cie_color.py` 엔진으로 계산. FGK·백색왜성은 Teff의 Planck 흑체를 쓰고, M왜성은 실측 Pickles 1998 SED(TiO/VO/H2O 밴드 → 벽돌빛 적색이 아니라 옅은 따뜻한 주황)를 씀. Pickles 스펙트럼은 VizieR에서 받아 `scripts/refs/.cache/pickles/`(gitignored)에 캐시. 파이프라인 자체검증은 G2V → ~#fff4f2.
- `scripts/refs/bd_visual_color.py` — 갈색왜성 가시 지각색 도구. (Teff, logg)의 BT-Settl(Allard & Homeier 2012) 스펙트럼을 SVO 이론 서비스에서 받아 `cie_color.py`로 적분하고, 클리핑 전 선형 RGB·CIE xy·색역 매핑 색조 헥스(흰색 방향 감채도, 하드 클리핑 금지)·40% 명도 렌더 틴트를 출력. `stellar-photospheric-color-methodology.md`의 갈색왜성 분기를 뒷받침하며, 검증 앵커는 Burrows 2001 실측 L5 + Cranmer 2021 발표 RGB 표. 예: `900 5.0` → 색조 #a300ff (채도는 모델 상한).

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
- `scripts/check_site_links.py` — 배포되는 docs/ HTML의 사이트 내부 404 스캔. 정적 href에 더해 `<script type="text/markdown">` 임베드 블록 안의 마크다운 링크(클라이언트 렌더라 href 스캔에 안 잡힘)까지 검사하고 `_papers/` 미러는 제외. check.sh 3b 단계에 배선
- `scripts/check_citation_links.py` — docs/reference(+ko 미러)에서 클릭 가능한 링크로 감싸지지 않은 bibcode/arXiv ID를 실패 처리([`bibcode`](ADS abs URL, `&`는 `%26`) 형식). 코드펜스와 긴 인라인 코드 예시는 제외. check.sh 3c 단계에 배선
- `scripts/check_methodology_coverage.py` — check.sh 게이트 12. 방법론 문서는 두 인덱스에 모두 등재돼야 하므로 파일 존재가 아니라 항목 *집합*을 대조한다. 영문 인덱스와 한글 미러(원본보다 레시피가 적어도 미러 게이트는 통과해버린다). 인덱스가 가리키지 않는 `*-methodology.md` 파일도 실패 처리한다. 세 번째 surface였던 GitHub 위키 `Methodology-Library` 포털은 발행을 Pages로 통합하면서 폐기했고(2026-08-13), 그와 함께 이 게이트의 유일한 네트워크 의존도 사라졌다
- `scripts/check_language.py` — 영문 source-of-truth 영역의 .md 파일 중 한글 dominant (25%+) 검출. `phase3/_audit/*` 는 allowlist.
- `scripts/check_build_freshness.py` — `docs/data.json` 이 최신 `db/systems/*.json` 보다 오래됐는지, `docs/reports.html` / `reports-manifest.json` 이 최신 `docs/phase{2,3}/*.html` 보다 오래됐는지 확인. 매니페스트의 고아 키 / dangling html 도 검사 (build_site.py 스킵 + 슬러그 컨벤션 drift 감지). `docs/wiki/*.html` 이 생성 원본 markdown 보다 오래됐는지도 확인 — 이 프로젝트는 위키를 **둘** 발행하므로(별도 git 저장소인 GitHub 저장소 위키, 그리고 `build_docs.py` 가 만드는 Pages 미러) 레퍼런스 문서를 고치고 빌더를 안 돌리면 발행된 쪽이 옛 내용을 계속 보여준다.
- `scripts/build_sitemap.py` — 발행되는 docs/ 표면의 사이트맵 + 연결성 감사. 구획별 페이지 수·용량, 허브, 그리고 결함 세 종류(인바운드 없는 고아, 아웃바운드 없는 막다른 페이지, CDN 의존)를 보고한다. `docs/reference/site-map.md` + ko 미러를 생성하고, `--audit-only`는 쓰기 없이 **신규** 고아가 생기면 1로 종료한다(승인된 집합은 스크립트의 `BASELINE_ORPHANS`)
- `scripts/check.sh` — 릴리스 전 통합 점검. 스키마 검증 + 미러 상태 (stale 은 경고, missing 은 실패) + dead-link 스캔 + 컨벤션 점검 + 경로 마이그레이션 잔여물 점검 + 한글 dominant 검사 + 빌드 신선도 + Phase 4 emit-게이트 (게이트 8, 도구 13). 수동 실행 전용.

## 12. 3D 성도 뷰어

**목적.** `db/systems/*.json` 을 브라우저용 인터랙티브 3D 지도로 만든다. 카탈로그가 공간상 *어디에* 있는지 보고, 시스템을 골라 줌인하면 그 행성들까지 본다.

**트리거.** "DB 3D로 시각화", "성도 만들어줘", 새 별·행성을 한 묶음 추가한 뒤.

**파일.**
- `scripts/viz/build_starmap.py` — `db/systems/` 를 읽어 중력적으로 구분되는 위치마다 마커 하나로 컴포넌트를 묶고(union-find 0.4 ly, `binary_orbit_ref` 로 가드), Teff 에서 흑체 RGB·광년 ICRS 좌표·광도 기반 마커 크기를 베이크한다. 태양계(canonical 하드코딩 요소)를 원점에 주입한 뒤 자기완결 뷰어를 emit. `--self-check` 는 파일을 쓰지 않고 카운트만 검증.
- `scripts/viz/starmap_template.html` — Three.js 뷰어 템플릿(CDN importmap). 빌더가 임베드 JSON 페이로드를 끼워 넣는다.

**출력.** `docs/starmap.html` — 단일 자기완결 파일, GitHub Pages 호스팅 가능. 광년 스케일 맵 뷰(원점에 태양, ICRS 거리 링, 분광형 범례, 거리 필터, 50광년 밖 토글), 클릭하면 정보 패널, 더블클릭하면 AU 스케일 시스템 뷰로 들어가 행성 궤도를 본다. 한/영 UI 토글.

**서빙.** `cd docs && python3 -m http.server` 후 `http://localhost:8000/starmap.html` 열기 (CDN 모듈은 `file://` 가 아니라 http 필요).

**참고.** 색은 지각적 흑체 근사(보정된 SED 아님), 마커 크기는 광도 proxy(물리 반경 아닌 빌보드). 표 형태 DB 브라우저인 `docs/index.html`(2번 툴)과 별개로, 이쪽은 공간 배치를 본다.

**관련 — Dante 크기 검토 뷰어.** `phase4/viewers/dante-size-study.html` 는 동결된 위성 뷰어의 사본으로, 2026-08 Dante 크기 재검토용입니다. 반지름 슬라이더(200~900 km, 밀도 고정)를 붙여 질량·표면중력·조석출력(∝R⁵)·표면플럭스(∝R³)·면적가중 복사온도(열 분배로 우회할 수 없는 하한)·판도라에서 본 겉보기 지름을 즉시 다시 계산하고, 온도에 따라 천체를 암석색에서 백열색으로 물들입니다. 값은 설계값에 동기화했습니다(동결 원본은 의도적으로 미동기화) — Chaos e 0.10→0.02, 폴리페무스 120→120.873 M⊕. 역행 위성의 (경사각, 노드)는 설계값과 등가인 표현이며 오류가 아닙니다.

**관련 — 폴리페무스 위성계 뷰어.** `phase4/viewers/polyphemus-moon-viewer.html` 은 α Cen A b(폴리페무스) 위성계 + 고리 설계를 보는 독립형 인터랙티브 3D 뷰어다. 명명 5위성(A b I~V = Dante·Hades·Pandora·Cassandra·Chaos), 경사·승교점, 흐릿한 A b V 공급 E고리를 시각화한다. 카탈로그 전체 성도와 별개인 Phase 4 아트디렉션 보조 도구로, `phase4/alpha_centauri.yaml` 에 기록된 게이트 통과 로스터를 그려 보여준다. **동결(2026-06-22):** 설계 탐색 임무가 끝나(로스터·고리·obliquity 확정) 아티팩트로 보존하며, 이후 결정은 여기 동기화하지 않는다. 성도에 없는 고유 기능은 A b III 지표 1인칭 시점+일식뿐이고, canonical·유지보수 시각화는 `docs/starmap.html` 이다.

**관련 — 프록시마 c 몸체+고리 뷰어.** `phase4/viewers/proxima-c-ring-viewer.html` (2026-08-04): 프록시마 c의 게이트 확정 형태를 보는 독립형 3D 뷰어다. 적/흰 2중 고리 띠(24.0~32.7k / 41.3~51.6k km, 경계·줄무늬 수 조절), J₂ 편평도(실제 0.45%, 과장 슬라이더), 자전축 기울기 17°, 50° 기울고 0.4 R_c 이탈한 자기축, 얼음 Roche 한계, M왜성 적색광 토글을 담는다. **지구 시선 밝기 계산기**(폴리페무스 뷰어의 ΔR 기능 이식)도 실려 있다. Gratton 2020의 `c = φ·A·r²/(4d²)`로 반사광 대비(행성 원반 + 고리 투영 × 피복률)를 실시간 계산해 실측 `(3.5±2.0)e-7` 목표와 대조하고, 피복률 맞춤 키를 제공한다. 이 도구가 드러내는 판정: 게이트 고리는 Gratton 초과 밝기의 ~0.2%뿐이고 Roche를 가득 채운 정면 고리조차 ~4%라, hook은 테마적 근거이지 측광 근거가 아니다(후보가 실재라면 포말하우트 b급 먼지구름이 필요하거나 배경원). 전문 캐시는 `docs/phase3/_papers/2004.06685.md`. Erid 뷰어들과 같은 three@0.160 CDN 스택이며, `phase4/proxima_cen.yaml` 의 아트디렉션 보조 도구다.

## 13. Phase 4 결정 보드 도구

**목적.** Phase 4 아트 디렉션 보드(`phase4/<system>.yaml`, 스키마 v2)를 emit-안전하고 리뷰 가능한 상태로 유지한다. 모든 보드를 SPEC 계약에 대해 검증하고, 게이트 리뷰용으로 바디별 HTML 페이지를 렌더한다.

**트리거.** 보드를 고칠 때마다 (validator는 `check.sh` 게이트 8로 자동 실행). "Phase 4 진행/돌리자"는 `nearstars-phase4` 스킬을 타며, 스킬이 두 도구를 모두 호출한다.

**파일.**
- `scripts/check_phase4_gate.py` — 보드 validator. `schema_version: 2` 보드는 hard-check (status/verdict/op enum, 축 메뉴, typed `fields[]` 형태 검사 — 숫자가 prose에만 있는 행 거부 포함 —, `(body, axis)` 유일성, `refs` 리스트 타입, `colors` hex 형식, divergence-note 필수, passthrough는 gate 금지). 레거시 v1 보드는 한 줄 soft 요약만 내서 파일 단위 마이그레이션이 가능하다. 계약 문서: `phase4/SPEC.md` §0/§3.1.
- `scripts/phase4/build_phase4_html.py <system>` — v2 보드를 `docs/phase4/<system-slug>/` (인덱스 + 바디별 1페이지)로 렌더. 산문 narrative + typed spec 표(hex 칩, window, 바이옴 색 스와치, 필드별 note), 게이트 evidence/divergence, 한/영 토글. 슬러그는 `scripts/pipeline/_naming.py` 사용. 결정론적 (재실행해도 diff 없음).

**출력.** validator: exit 0/1 + 행 단위 진단. 빌더: `docs/phase4/<system-slug>/*.html`.

## 14. 방사선대 시각화 + Kerbalism emitter

태양계 방사선대의 스톡 vs 물리 단면 렌더(위키)와 물리 근거 Kerbalism cfg 패치.
감사 문서는 `solar-system-radiation-belts.md`.

- `scripts/viz/render_belts.py` — 자오면 단면 PNG 렌더러. 인게임 Kerbalism
  `RadiationModel` SDF를 그대로 재현(Unlicense 알고리즘).
- `scripts/viz/render_belts_bodies.py` — 바디별 드라이버. `*_phys` 엔트리가 피팅된
  벨트 지오메트리의 **단일 소스**(emitter도 여기서 읽음).
- `scripts/viz/render_alfven_wing.py` — Proxima d 알펜 윙 개념도
  (`docs/img/proxima-d-alfven-wing.png`). sub-Alfvénic 항성풍(M_A ~ 0.3 가정) →
  bow shock 없음. 별 쪽/반대쪽 두 가닥 윙(기울기 arctan M_A ≈ 17°)이 phase-lock
  플레어를 만드는 별-행성 자기 연결 통로임을 그리고, 근접 뷰에 닫힌 쌍극자 코어,
  Shue nose 7 R_d, 풍화 극관을 함께 표시.
- `scripts/refs/magnetopause_geometry.py` — 자기장에서 자기권계면 형상을 구하는 계산기이자,
  NearStars 모든 pause 값의 단일 재현 출처. Chapman-Ferraro 노즈(자이언트는 magnetodisc 팽창
  인자를 곱한다. 목성에서 Rutala 2025 피팅 대 진공 쌍극자 예측의 비로 실측되며 p^−1/12로 감소),
  레짐 판정(내장 위성은 알펜 마하수로 가르되, 불확실한 토러스 프로파일이 결론에 끼어들지 않도록
  M_A=1에 필요한 밀도로 뒤집어 보고), α에서 나오는 Kerbalism pause 4필드, 그리고 연화 Shue 곡선에
  offset 구 근사를 최소제곱으로 맞추는 `fit_offset_emulation()`. 인자 없이 실행하면 전체 표가 나온다.
  **알펜 날개 기하**도 여기 있다. 스케치가 아니라 도출이다. 기울기 `arctan M_A`, 관 반경(= 장애물
  반경. 플럭스 보존에서 나오며, 포인팅 플럭스용 `R_eff = √3 R_obst`와는 다른 양이다. 후자는 출력만
  정한다), 직선 구간 `√(2 R_tube R_curv)`, 그리고 모천체 자기력선을 타고 휘어 `1/√B`로 좁아지다
  전리층에 오로라 발자국으로 착지하는 실제 곡선 플럭스관 `dipole_wing_path()`. 하류 변위는 모천체
  자전축 둘레의 **방위각 회전**이지 평행이동이 아니다. 평행이동으로 넣으면 끝이 전리층을 벗어나
  허공에 뜬다(2026-08-16 발견, 가니메데에서 78 R_moon 오차).
- `scripts/viz/render_alfven_wing.py` — 위 필드를 3D 스피어 트레이싱으로 렌더. 2D 슬라이스 렌더가
  자르는 평면이 하필 날개가 없는 평면이라 따로 만들었다. 4패널로 근거리(B–v 평면 + 3/4 뷰)와
  모천체까지 가는 전 구간을 보여주며, 직선 구간은 파랑·꺾인 구간은 주황으로 칠해 어디서 꺾이는지를
  캡션 숫자가 아니라 그림으로 보게 한다. `--selftest`는 numpy 필드가 `magnetopause_geometry.py`의
  스칼라 구현과 1e-9까지 일치하는지 검사한다.
- `scripts/refs/petrova_line_geometry.py` + `scripts/viz/render_petrova_line.py` — 『프로젝트
  헤일 메리』의 페트로바선. 같은 계약으로 짓고 튜브 렌더러를 공유해, 이 기계가 자기 기하 밖으로도
  일반화되는지 확인하는 첫 시험대다. 경로는 자전축 상승 → 아크 → 목표 지름으로 벌어지며 직진.
  꺾임점에 문턱값이 필요 없다. 목표가 항성 림에서 떨어진 각도는 **비단조**라(올라가면 림에서
  떨어지지만 동시에 아래쪽 축으로 쏠린다) 최대가 존재하고, 그 높이가 `H = √(R★·a)` — 항성 반경과
  궤도의 기하평균이다(솔→금성 12.5 R☉, 여유 81°). 꺾임이 모서리가 아닌 이유도 같은 곡선에서 나온다.
  최대 부근이 넓어서(최대의 99% 이상이 8.3~19.1 R☉) 돌아야 할 단일 높이가 없고, 그 밴드 폭이 곧
  선회 반경이 된다. 광속 이동이라 6분 비행 중 경로가 24초각 휘는 건 안 보이지만, 보는 빛도 그만큼
  묵은 것이라 **겨냥점은 보이는 위치보다 목표 지름 2.09개 앞**이다. 그림과 함께 [`petrova-line-geometry.md`](petrova-line-geometry.md) 에 정리했다. 장기 소비자 = 별도 시각화 모드
  ([`plugins/NearStarsFluxTube`](../../../plugins/NearStarsFluxTube/README.md)).
- `scripts/refs/proxima_d_belt_dose.py` — Proxima d 벨트 선량 도출(방법론 Part B).
  dose-anchor 보간 10.4×(B_eq/31 µT)^1.9 → 내대 ~5×10³ / 외대 ~1×10³ rad/h(신뢰
  낮음, 목성 앵커 1.9배 밖 외삽; 장 범위 3–280 G면 2×10²–10⁶), `kp_limit.py`
  CmCk 검증으로 K–P 상한 비구속(source/loss-set) 확인. `proxima_d_phys` 시각화
  항목의 근거.
- `scripts/viz/fit_belts.py` — 수치 피터. 쌍극자 드리프트-셸 타깃(r = L cos²λ,
  loss-cone 컷)을 Nelder-Mead로 Kerbalism SDF 파라미터에 피팅, IoU로 채점.
- `scripts/pipeline/emit_kerbalism_radiation.py` —
  `dist/.../Patches/Kerbalism/NearStars-SolarSystemRadiation.cfg` 방출(RadiationModel +
  RadiationBody 재바인드, 7바디, 클릭 가능한 ADS 출처 주석, 라운드트립 자가검증).
  Kerbalism/ROKerbalism 메인테이너 업스트림 제안용.
- `scripts/viz/build_belt_viewer.py` (+ `belt_viewer_template.html`) —
  `docs/belt-viewer.html` 빌드. 브라우저 인터랙티브 뷰어(실시간 SDF 단면 + 3D
  레이마칭, 필드별 슬라이더, `render_belts_bodies.BODIES`에서 주입한 17개 프리셋,
  Shue 오버레이, 원클릭 cfg 내보내기). 위키 Radiation-Belts 페이지에서 링크.
  깊은 링크를 지원한다. `?body=<보드 천체명 또는 body_key>[&variant=stock|phys][&embed=1]`
  로 특정 천체에 바로 진입하고, `embed=1`은 페이지 크롬과 피커를 감춰 Phase 4 천체 페이지가
  그 천체로 한정해 iframe 할 수 있게 한다.
- `scripts/viz/capture_belt_stills.py` — 벨트 뷰어의 단면을 NearStars 천체별 정지 이미지로
  캡처해 두 팔레트로 `docs/img/belts/nearstars/`에 저장한다. `?body=<보드 천체명>&variant=phys&still=1`
  로 뷰어를 몰아 피커·호버 리드아웃·2D/3D 토글·슬라이더 패널을 끄므로, 렌더러를 하나 더
  만들어 동기화할 필요 없이 뷰어와 같은 그림이 나온다. Phase 4가 이 결과를 각 천체의 magnetism
  결정 행 안에 붙인다. 천체마다 두 프레이밍을 만든다. `<key>.png`는 프리셋 기본 줌의 클로즈업,
  `<key>_shape.png`는 자기권계면 전체를 계면 자신의 길이 기준으로 잡는다(중심 x를 nose..tail 중점에
  두며, 뷰어에 새로 생긴 `R`·`cx` 쿼리 파라미터를 쓴다). 둘 다 뷰어의 정사각 프레임을 유지한다 —
  결정 행에서 나란히 놓이므로 두 장의 비율이 같아야 한다. `playwright` 필요(캡처 전용 의존성).
- `scripts/viz/build_uranus_geometry.py` (+ `uranus_geometry_template.html`) —
  [`docs/uranus-geometry.html`](../../../docs/uranus-geometry.html) 빌드. 지구의 평범한
  자기권과 천왕성의 극-정면(pole-on) 자기권을 나란히 비교하는 three.js 페이지. 목적은 딱
  하나를 눈에 보이게 하는 것. 보이저 2호 조우 당시 천왕성 자전축은 태양 방향에서 ~8° 안쪽을
  향했고, 그래서 59° 쌍극자 기울기가 자전 한 바퀴마다 전류판을 355°나 휘젓는다(지구는 24°만
  펄럭인다). 그곳에서 단 한 번의 플라이바이로 잰 X-line 값이 대표성을 갖지 못할 수 있는 이유다.
- `scripts/refs/kp_limit.py` — Kennel–Petschek 포획 플럭스 상한 계산기. Mauk & Fox
  원저자 Zenodo 구현의 검증된 파이썬 포팅(인쇄 중간값 11개 ≤0.05% 재현). 자기권
  지오메트리 방법론 Part B의 벨트 강도 상한 체크에 사용.
- `scripts/refs/greenhouse_dt.py` — 온실 상승폭(T_surf − T_eq) 추정기. 문헌 iso-Ts 등온선
  격자(Feulner 2012 / Kopparapu 2013 앵커)에 CH₄ 보정, Arney haze 상한, Goldblatt N₂ 압력확장을
  더한다. `--s/--pco2/--ch4` 로 단발 조회, 인자 없이 실행하면 검증 표와 A b 위성 결과.
  `docs/reference/greenhouse-warming-methodology.md` 의 계산 근거.
- `scripts/refs/moon_energy_budget.py` — 위성 T_eq를 4항 에너지 예산(별빛−식, 행성 열복사+반사,
  조석)으로 계산. 폭주 천장과 A b 적용 예 포함, `--pandora-27h-vs-32h`로 궤도 선택 표만 출력.
  이오 조석 플럭스와 이오 식 지속시간으로 검증.
  `docs/reference/moon-energy-budget-methodology.md` 의 계산 근거.
- `scripts/refs/jeans_escape.py` — 기체 종별 대기 보유 판정. 종마다 Jeans 파라미터를 구하고
  Volkov 2011의 체제 임계값으로 판정하며, 지구·타이탄·화성으로 검증. `--mass/--radius/--texo`로
  단발 조회. `docs/reference/exoplanet-atmosphere-methodology.md` 관문 4의 계산 근거.

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
