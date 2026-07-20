<!-- NearStars 파이프라인 계약 문서 — Phase 1~4의 단계·인터페이스·게이트 canonical 정의 -->
# NearStars 파이프라인 계약 — 단계, 인터페이스, 게이트

**상태.** canonical (2026-07-20). 이 문서는 Phase 1~4 파이프라인의 유일한 현행 정의입니다.
각 단계가 무엇인지, 경계마다 어떤 기계-소비 아티팩트가 넘어가는지, 그것을 어떤 키로 잇는지,
어떤 게이트가 지키는지를 규정합니다. `guideline.md` §9가 원래 프로젝트 스케치에서 물려받은
구식 per-system 개발 단계(별 골격 / 행성 / 비주얼 / 마무리 — 지금은 폐기된 다른 넘버링)를
이 문서가 대체합니다.

2026-07-20의 두 감사(per-system 정합성 + 데이터 흐름 추적)에 근거하며,
작업 노트는 `phase2/pipeline-flow-program/`에 있습니다.

## 0. 단계 정의 (현행)

| Phase | 무엇인가 | Canonical store | 구동 주체 |
|---|---|---|---|
| **1** | 공개 카탈로그(Gaia DR3, SIMBAD, NASA EA, ORB6) 기반 baseline 큐레이션. 식별정보·측성·쌍성 궤도 | `db/*.json` raw layers → `db/systems/*.json` (strictly derived) | `scripts/pipeline/` |
| **2** | 논문 인용 측정치(per-paper `bibcode` 귀속)를 큐레이션 레이어에 추가 | `db/stellar_props_curated.json`, `db/planets_curated.json`, `db/disks_curated.json` | `nearstars-add-star` 스킬, `apply_phase2.py` |
| **3** | cfg-ready 합성. 측정치 → per-body 결정(window + interesting-first 기본값) | `docs/phase3/<slug>.md` — `## Decisions` 테이블이 기계 인터페이스(§2) | `nearstars-phase3` 스킬 |
| **4** | 오너 아트디렉션을 Phase 2/3 window에 대고 게이트. frozen override | `phase4/<system>.yaml` (schema v2, SPEC.md) | `nearstars-phase4` 스킬 |
| **emit** | 결정론적 cfg 작성, `cfg = f(db, phase3, phase4)` — 프로젝트 말미로 유예 | `dist/` | writer 스킬 (kopernicus/principia/firefly/researchbodies-cfg) |

Phase 2 vs 3 불변식. Phase 3의 입력은 반드시 Phase 2 측정치여야 하고, Phase 4는 Phase 2/3를 절대
변형하지 않습니다(`phase4/SPEC.md`의 "Phase distinction" 참조).

## 1. 경계 테이블 — 무엇이 어떤 키로 넘어가고 무엇이 지키는가

| 경계 | 넘어가는 기계 아티팩트 | Join key | 게이트 |
|---|---|---|---|
| 1→2 | `phase2/<host>/measurements.yaml` → `apply_phase2.py`로 curated JSON | `system_name` + body `name` | `validate.py` (check.sh 1) |
| 2→db | curated JSON → `build_systems.py`로 `db/systems/*.json` (strictly derived, 손으로 편집 금지) | `system_name`; file stem = `to_file_slug(system_name)` | `validate.py`; snake_case guard (check.sh 4b); freshness (7) |
| 2→3 | curated 측정치(합성 작성자가 읽음) + `phase3/<system>/system.yaml` (**bibliography 파이프라인 입력 전용** — §5 참조) | db names / `system_slug` | — (사람 판단; bib 스크립트는 자기 스키마를 검증) |
| 3→4, 3→emit | `docs/phase3/<slug>.md`의 `## Decisions` 테이블 — `Field / Value / Confidence / Basis` 컬럼, `scripts/pipeline/phase3_decisions.py`가 파싱 | report slug = `to_url_slug(body name)`; row key = `Field` label | Decisions parse check (check.sh 10c) |
| 4→emit | `phase4/<system>.yaml`의 `decisions[].fields[]` (+ `discoverability_cfg`) | board filename = `to_file_slug(system_name)`; `body:` = db `name`과 **정확히 일치**(SPEC §3 naming contract); fiction body는 `discoverability: fictional` 표기 | schema gate (check.sh 8); body↔db + roster gates (10a/10b) |
| all→emit | resolver 출력(§3) | body name | dry-run (WP1) |

## 2. Join-key 레지스트리

하나의 천체는 아래 표기만을 가지며, 다른 것을 지어내지 않습니다.

- **`system_name` / body `name`** (db JSON) — display-form 정확 문자열
  (`tau Cet`, `Proxima Cen b`, `Alpha Centauri A`). master 키입니다. phase4의
  `body:`는 이것과 정확히 같아야 합니다.
- **file slug** = `to_file_slug(name)` — snake_case, 작업 트리 + db 파일명
  (`tau_cet.json`, `phase4/tau_cet.yaml`, `phase3/tau_cet/`).
- **url slug** = `to_url_slug(name)` — kebab-case, docs 트리 전용
  (`docs/phase3/tau-cet.md`, `docs/phase4/tau-cet/`). 행성 **리포트** slug는
  `to_url_slug(호스트 이름) + "-" + 행성 문자`다. db 행성명 자체의 slug와 거의 모든
  곳에서 같지만, 행성명이 호스트 접미를 생략하는 호스트에서만 갈라진다
  (`Barnard b` → `barnards-star-b.md`이지 `barnard-b.md`가 아님).
- **`kopernicus_name`** (선택, phase4 row 필드) — 인게임 cfg 천체 이름
  (`Polyphemus`). 문화적 이름이 키가 되는 유일한 자리입니다.

두 slug 모두 같은 `name`에서 `scripts/pipeline/_naming.py`를 거쳐 나옵니다. display variant에서
slug를 만들지 마세요(2026-07-20의 `tau_ceti` 사고).

## 3. 값 해소 순서 (목표 아키텍처)

per-body 실효값 = 레이어 머지, 뒤가 이깁니다.

```
db/systems derived  <  phase3 Decisions (parsed)  <  phase4 fields[] (gated)
```

- 머지는 **단일 모듈** `scripts/pipeline/resolve_emit_values.py`(WP1)에 있습니다.
  emitter는 resolver 출력에서 cfg 문법을 포매팅할 뿐, 출처를 스스로 고르지 않습니다.
- **현재 상태(재배선 이전).** principia는 db만 읽고, kopernicus/firefly는 Decisions md를
  직접 스크레이핑하며, researchbodies는 phase4를 직접 읽습니다. 넷 모두를 resolver 위로
  재배선하는 일은 emit 시점 작업으로 `phase4/emit-hardening/checklist.md`에 추적됩니다.
  그때까지 phase4-only 편집은 principia/kopernicus/firefly 출력에 **도달하지 않습니다** —
  그렇게 가정하지 마세요.
- 값은 정확히 하나의 권위 레이어에만 존재해야 합니다. 산문(board `narrative:`)에서 다시
  말하는 것은 표시일 뿐, 출처가 아닙니다.
- **필드 정렬(2026-07-20 해소).** phase3 Decision 이름과 phase4 `fields[]` 이름이
  겹치지 않는 건 설계상 당연한 결과입니다. 보드는 오너가 메뉴에서 고른 선택을 단위 없이
  기록하고(`mass`, `radius`, `rotation_period`), Decisions 행은 단위를 키에 박아
  씁니다(`mass_msun` / `mass_mearth` / `mass_mjup`). 그대로 두면 영원히 만나지 않으니
  레이어 머지가 조용히 아무것도 오버라이드하지 않았던 것입니다. 다리 역할은
  **`scripts/pipeline/field_alignment.yaml`**이 맡습니다 — 보드 메뉴명마다 후보 phase3
  키를 우선순위 순으로, 바디 클래스별 함의 단위와 하류 cfg 타깃을 함께 적어 둡니다.
  해석기는 그 바디의 리포트가 실제로 쓴 첫 후보를 고르며, 이것이 단위 없는 보드 값이
  클래스에 맞는 단위 변형으로 정확히 안착하는 방식입니다. 커버리지는 가정하지 않고
  강제합니다. 게이트 10f가 정렬표에 없는 보드 필드명을 경고합니다(현재 93/93 매핑).
  `phase3:`가 빈 항목은 설계상 보드가 최종 권한을 갖는 축이며(게임플레이, 고리 텍스처,
  창작 바디) 대항 없이 emit됩니다.

## 4. 클래스별 완료 기준 (단계별 "완성"의 의미)

Phase 2 측정 최저선(카테고리는 `stellar_props_curated.json`; [Fe/H]는 상시 skip-metallicity
결정에 따라 어디서나 선택).

| 별 클래스 | 최저선 카테고리 |
|---|---|
| FGK / M host | teff, radius, luminosity, mass, age, rotation, activity (7) |
| A-type | teff, radius, luminosity, mass, age, rotation (activity N/A — 채층 지표 없음; N/A를 기록) |
| White dwarf | teff, radius, mass, age |
| Brown dwarf | teff, radius, luminosity, mass, age |

미분해 동반성은 자기 스펙트럼 클래스의 최저선을 따릅니다(eps Ind Ba/Bb → BD 최저선).
최저선 범위(오너, 2026-07-20 당일 재조정). **인게임 구현 후보군 — `db/roster.yaml`
시스템의 host들**입니다. Phase 2 깊이는 카탈로그 소속이 아니라 구현 의도를 따릅니다.
처음의 "50 ly 이내 전부" 결정은 오너 착오였고 당일 정정됐습니다(넓은 범위로 하루 진행된
백필 데이터는 논문 인용이 온전해 그대로 보존하되, 비로스터 host는 최저선 대상이
아닙니다). 게이트 10d가 워크리스트를 보고합니다(`check_pipeline_flow.py
--floor-detail`). 최저선 전체 정의는 `phase2/curation-data-contract/SPEC.md` §A0,
행성 블록 형태 규칙(list+method가 canonical)은 §A1에 있습니다.

Phase 3. 구현 host의 모든 db 행성이 리포트를 받고, host 별은 star-level 리포트를 받습니다
(디스크 내용은 여기 접힘 — 별도 디스크 리포트 없음).
Phase 4. confirmed-roster 시스템은 모든 db 천체(별 + 행성)와 게이트된 fiction 천체를 아우르는
board를 받습니다. non-roster host는 board가 필요 없습니다.

## 5. Write-only / 특수역할 아티팩트 (누군가 잘못 "고치지" 않도록)

- `phase3/<system>/system.yaml` — **bibliography** 스크립트(`run_phase3.py` 등)만의 입력.
  합성-값 저장소가 아니며, 하류의 어떤 것도 읽지 않습니다. 손으로 triage한 시스템에는
  없어도 되고, 그래도 괜찮습니다.
- `docs/phase3/*.html`, `docs/phase4/**/*.html` — 사람용 렌더. 기계 소비자 없음.
- `phase3/<system>/kopernicus_extras.yaml` — **첫 사용 전에 폐기됨**. kopernicus emitter가
  참조하지만 실제 인스턴스는 없습니다. 고리/디스크 emit 값은 대신 resolver를 거쳐 phase4
  `fields[]`로 해소됩니다(WP1).
- `gameplay/`, `phase3/stellar_wind_synthesis/`, `phase4/figure/values.md`,
  `phase4/viewers/` — 설계/참조 레이어. 작성 시점에 소비되고 emit이 소비하지 않습니다.
  (`figure/values.md`에는 알려진 stale mass가 있음 — board 노트 참조.)

## 6. 과거 phase2 레이아웃 인덱스 (작성 세대 — 재구조화 금지)

Phase 2는 세 세대에 걸쳐 작성되었고, 한 host의 노트는 그 세대가 둔 자리에 있습니다.
이 인덱스는 조회용이며 이력은 다시 쓰지 않습니다.

- **Per-host dir + measurements.yaml.** alpha_centauri_proxima (A/B/Proxima),
  trappist_1, luhman_16, hd_219134, eps_ind_a, yz_cet, gj_896_a, gj_9066, 55_cnc.
- **Per-host dir, 노트만** (데이터는 db에 직접 적용). 40_eridani,
  delta_pavonis.
- **Batch dirs** (per-host dir 없음). `tier1-stellar/` → eps Eri, tau Cet, AU Mic,
  HD 69830, 61 Vir, Vega, Fomalhaut (+delta Pav follow-ups); `tier1-batch2/` →
  Barnard's star, Teegarden's star; `xray_sweep/`, `visual-batch-1/`,
  `disk-measurements-ingest/` → cross-host sweeps.
- **앞으로.** 신규 host는 항상 per-host dir + measurements.yaml 형태를 씁니다
  (`nearstars-add-star` 스킬).

## 관련 문서

- [guideline.md](guideline.md) — 프로젝트 개요. §9가 이제 이 문서를 가리킵니다.
- [methodology.md](methodology.md) — 스키마와 레이어 시맨틱.
- `phase2/curation-data-contract/SPEC.md` — Phase 2/3 required-data 계약.
- `phase4/SPEC.md` — Phase 4 board 스키마 + naming contract (§3).
- [tools.md](tools.md) — 도구 인덱스(파서, 게이트, resolver).
