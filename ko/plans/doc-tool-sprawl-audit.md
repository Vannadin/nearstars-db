---
title: 문서 / 툴 난립 감사 — 발견 + 라이프사이클 게이트 플랜
status: promoted   # active | promoted | archived
created: 2026-06-03
promoted: 2026-07-19 → phase2/sprawl-lifecycle-gate/
---

# 문서 / 툴 난립 감사 — 발견 + 라이프사이클 게이트 플랜

> **2026-07-19 승격** → [`phase2/sprawl-lifecycle-gate/`](../../phase2/sprawl-lifecycle-gate/plan.md).
> 재감사 결과(F1 해결, F3 부분 해결, F4/F5/F7 + §2.4 + sprawl 게이트는 미해결,
> 여기에 페이즈별 컨벤션 발산이라는 새 발견 추가) 실제 작업으로 넘어갔다. 이 노트는 이제 역사 기록이다.

**NearStars 연결고리.** 세션마다, 스킬 실행마다 사이드 산출물이 튀어나온다.
working dir(`phase3/<system>/`, `_recovered/`, `_audit/`), scratch JSON/MD,
`scripts/refs/`의 1회성 population 스크립트, ground-truth 파일, errata,
manual-followup 로그가 그것이다. 이 노트는 그런 산출물이 **체계적으로 생성·관리되는지**
아니면 그냥 쌓이기만 하는지를 감사하고 고칠 거리를 스코핑한다.
`scripts/check.sh`와 `AGENTS.md`에 라이프사이클/청소 규칙이 필요한지를 판단하는 근거가 된다.
2026-06-03에 아이디어로 제기됐다.

**범위.** 포함. 무엇이 어디서 생기는지의 인벤토리(커밋-canonical vs scratch vs
gitignore-재생성 가능 vs 고아), `AGENTS.md §2`의 4-홈 컨벤션 준수 여부, 그리고 구체적 수정 플랜.
제외. 실제 수정 구현 — 이 노트는 **아직 greenlit 아님**. greenlit되면 추후 세션이
`phase2/sprawl-lifecycle-gate/`로 승격한다. 청소 한 건(고아 scratch 제거, §2 F2)은
감사 세션에서 이미 실행했고, 나머지는 전부 보류다.

**외부 참조.** 없음 — 내부 감사다. 앵커.
[`AGENTS.md §2`](../../AGENTS.md), [`scripts/check.sh`](../../scripts/check.sh),
[`docs/reference/tools.md`](../../docs/reference/tools.md). 관련 메모리.
`project-doc-tool-sprawl-audit`, `reference-check-command`, `project-naming-canonical`.

---

## 1. 요약

| 질문 | 답 |
|------|-----|
| 산출물 생성이 체계적인가 난립인가? | **설계상 체계적, 가장자리에서 새고 있음.** 4-홈 + ko 미러 + 7게이트 시스템은 실재하고 대체로 지켜진다(미러 90/90, dead-link 0, 스키마 PASS). |
| 진짜 갭은 어디인가? | **위치가 아니라 라이프사이클.** 컨벤션은 "새 산출물이 어디로 가나"는 규율하지만 "scratch를 언제 버리거나 승격하나"는 규율하지 않는다. |
| 가장 나쁜 단일 발견은? | **F1 — 썩은 가드레일.** `check.sh` 게이트 5가 stale 오탐으로 계속 실패해 왔고, 그래서 다들 빨간불을 무시하게 길들여졌다. |
| 이미 고친 건? | **F2 고아 scratch** — 감사 세션에서 죽은 디렉토리 5개 삭제(빈 디렉토리 + `_recovered/`). |
| 수정의 모양은? | 게이트 5 빠른 수리 + sprawl/orphan 게이트 신설 + `AGENTS.md §2.4` 라이프사이클 규칙 + 툴 인덱스 backfill. |

---

## 2. 발견 (심각도순)

증거는 2026-06-03에 `git ls-files` / `git status` / `bash scripts/check.sh`로 채집했다.
카운트는 재현 가능하다.

### F1 — 썩은 가드레일. `check.sh` 게이트 5가 빨간불 [높음]

게이트 5("경로 마이그레이션 잔여물")는 추적 파일의 *내용*을 패턴
`alpha-cen-proxima-system|trappist-1-system|docs/wiki|llm-wiki|skills-lock`로 grep한다.
이 중 `docs/wiki` 토큰이 이제 [`scripts/build_docs.py`](../../scripts/build_docs.py)에 걸린다.
이 스크립트는 `docs/wiki/`를 **정상적으로 생성**하는 생성기다(렌더된 HTML 17개. LLM-위키 롤백 이후
재도입돼 현재도 관리 중 — 마지막 변경 커밋 `9df6ae3`, 2026-05-31). 즉 게이트가 자기 생성기를
오탐하면서 `check.sh`가 매 실행 비정상 종료한다. 항상 빨간 가드레일은 없는 것보다 나쁘다 —
"일부 점검 실패" 줄이 무시당하게 된다.

**수정.** 게이트 5 패턴에서 `docs/wiki`를 뺀다(마이그레이션으로 떠난 건 *옛 flat 경로* 형태였지
살아 있는 `docs/wiki/` 렌더가 아니다). 이후 `bash scripts/check.sh`가 0으로 종료하는지 확인.

### F2 — 산출물 커밋 후 남는 고아 scratch [중간] — *청소 완료*

`phase3/<system>/` working dir 6개가 순수 로컬 scratch(추적 0개)였는데, 그 산출물
(`docs/phase3/*.html` + `.md` + `_bib/*.yaml`)은 이미 커밋돼 있었다.
**감사 세션에서 삭제함**(전부 untracked → git 무영향).

- 빈 디렉토리. `phase3/55_cnc/`, `phase3/yz_cet/`, `phase2/disk-vertical-structure/`
- 복구 잔여물. `phase3/barnards_star/_recovered/`(12파일),
  `phase3/teegardens_star/_recovered/`(9파일) + 각 `.DS_Store`

**보존**(고아 아님 — 떠도는 결정 로그다. F3 참조).
`phase3/eps_ind_a/context-notes.md`, `phase3/hd_219134/context-notes.md`.

남은 리스크는 재발이다. 다음 세션이 다시 어지르는 걸 *막는* 장치가 없다.
그건 F-fix 게이트(§3.2)가 다룬다.

### F3 — trio 커밋 라이프사이클 불일치 [중간]

`AGENTS.md §2`는 `phase3/<system>/`가 `phase2/`처럼 trio(plan + checklist + context-notes)를
가진다고 규정한다. 실제로는 커밋 결정이 임기응변이다. 어떤 디렉토리는 커밋하고
(`trappist_1`=10파일, `stability-sim`=16, `au_mic`=3, `vega`=3, `61_vir`=3), 어떤 건 아예 안 한다
(`eps_ind_a` / `hd_219134`는 *미추적* `context-notes.md`만 있고, `55_cnc` / `yz_cet`는 비어 있었다).
그래서 "이 합성의 결정 로그가 어디 있나"의 답이 시스템마다 다르다. working dir를 결정 로그로
커밋할지 폐기할지를 정하는 규칙이 없다.

**필요한 결정.** 보존한 context-notes 2개 — 제안된 §2.4 규칙대로 커밋(결정 로그가 남길 가치 있는 산물)할지,
삭제할지. **커밋 권장.** 렌더된 리포트보다 상세한 append-only 합성 근거를 담고 있다.

### F4 — `scripts/refs/`의 미등록 1회성 스크립트 [중간]

`scripts/refs/*.py` 10개 중 7개가 [`docs/reference/tools.md`](../../docs/reference/tools.md)에
**없다**. "새 툴은 전부 인덱스" 규칙 위반(메모리 `feedback-tools-lookup`).
`build_molecular_db`, `migrate_element_db_v2`, `populate_phosphor_emission`,
`populate_reentry_aurora`, `populate_spectro_refinements`, `populate_tier_c_upgrades`,
`wavelength_to_rgb`. (등록됨. `render_element_colors_doc`, `validate_element_colors`,
`build_plasma_temperature_colors`.) 대부분 1회성 DB-population / 마이그레이션 스크립트로,
출력 YAML은 커밋되는데 스크립트는 인덱스 항목도, 재실행-가능/1회용 마커도 없이 남는다.

**수정.** 누락된 7개를 `tools.md`에 backfill(+ ko 미러), 그리고 1회성 마이그레이션과 재실행 builder를
구분하도록 `# one-shot:` / `# regenerable:` 한 줄 헤더 컨벤션 추가.

### F5 — scratch와 canonical 혼재, 라이프사이클 마커 없음 [낮음]

`phase3/_audit/`가 중간 scratch(`harvested-audit-*.json`, `triaged-*.json`,
`findings-all-63-*.json`, `static-flags-*.json`)와 canonical 산출물(`errata-2026-06-03.md`,
`integrity-audit-*.md`, `F1-ground-truth.md`)을 "보존" vs "버릴 중간물" 마커 없이 함께 커밋한다.
같은 모양으로, `phase2/` 루트에 날짜 박힌 세션 로그 2개(`2026-05-28-tier1-postmortem.md`,
`2026-05-29-next-session-prompt.md`)가 `<topic>/` 안이 아니라 루트에 loose하게 있다.

**수정.** §2.4 라이프사이클 규칙으로 커버한다(중간 JSON은 gitignore된 `_scratch/` 서브디렉토리로
보내거나, canonical 산출물이 안착하면 삭제).

### F6 — 결정 대기 중인 미추적물 [낮음]

현재 working tree(대부분 다른 세션의 진행 중 스트림 — 건드리지 말 것).
`title-candidates.md`(루트에 loose, 유지한다면 `plans/`가 자리), `docs/phase2/yz-cet.html`
(미커밋 렌더), `plugins/NearStarsFluxTube/`(의도된 백로그 프로토타입, 메모리
`project-nearstars-flux-tube-plugin` — 난립 아님).

### F7 — 문서 ↔ 툴 drift. `AGENTS.md`의 미러 범위가 실제 enforcer보다 좁음 [낮음]

`AGENTS.md §2.1`의 영어-전용 제외 목록은 `phase2/<topic>/{checklist,context-notes}.md`만 열거한다.
실제 enforcer인 [`scripts/check-mirrors.sh`](../../scripts/check-mirrors.sh)는 두 축에서 더 넓다.
(a) 애초에 `docs/`·`plans/`·`README.md`만 스캔한다 — `phase2/`·`phase3/` 트리 전체는 미러 검사 대상이 아니다.
(b) `should_exclude()`가 더해서 모든 `*/_*` 경로 component(`_papers/`, `_bib/`, `_audit/`, `_archive/`)와
모든 `*/{checklist,context-notes}.md`를 제외한다. 툴 동작이 옳다 — `phase3/_audit/*.md` 같은
감사/작업 문서는 레퍼런스가 아니라 운영 문서라 한글 미러가 필요 없다. 다만 문서가 따라오지 못했을 뿐이다.
`AGENTS.md`만 읽은 사람은 `phase3/_audit/`에 미러가 필요하다고 오해한다.
2026-06-03 "왜 `_audit/` 문서엔 ko 미러가 없나?" 질문에서 표면화됐다.

**수정.** §2.1 제외 조항을 개별 파일 열거 대신 "미러 대상은 `docs/`·`plans/`·`README.md`뿐.
`phase2/`·`phase3/` 작업 트리와 모든 `_*` 서브트리는 영어 전용"으로 일반화. §2.4 AGENTS.md 편집(§3.3)에 묶는다.

---

## 3. NearStars에의 함의 — 수정 플랜

갭은 **라이프사이클 규칙**이지 위치 규칙이 더 필요한 게 아니다. 세 가지 변경을 각각 별도 커밋으로,
순서대로. 추후 세션이 실행하고, 착수할 때 이 노트를 `phase2/sprawl-lifecycle-gate/`로 승격한다.

### 3.1 게이트 5 오탐 수정 (health check 잠금 해제) [먼저]

- [`scripts/check.sh`](../../scripts/check.sh) 게이트 5 편집. `patterns`에서 `docs/wiki` 제거
  (`llm-wiki` / `skills-lock` / `-system` 슬러그는 유지).
- 검증. `bash scripts/check.sh`가 0으로 종료(현재는 이것 하나로 1 종료).
- 커밋 1개. `fix(check): drop stale docs/wiki false-positive from gate 5`.

### 3.2 `check.sh`에 sprawl / orphan 게이트 추가 [게이트 8]

새 게이트가 경고 또는 실패로 플래그(임계값은 결정).

- (a) `phase2/` 또는 `phase3/` 바로 아래의 **빈 디렉토리**(`find phase2 phase3 -type d -empty`).
- (b) **수거 대상 working dir** — 추적 0개이면서 커밋된 `docs/phase3/<slug>*.html`이 존재하는
  `phase3/<system>/` 또는 `phase2/<topic>/`(산출물은 나갔고 working dir는 이제 scratch).
- (c) **미등록 refs 스크립트** — basename이 `docs/reference/tools.md`에 없는 `scripts/refs/*.py`.
- 커밋 1개. `feat(check): add gate 8 — sprawl/orphan detection`.

### 3.3 `AGENTS.md §2` 편집 — 라이프사이클 규칙(§2.4) + 미러 범위 수정(§2.1, F7)

`AGENTS.md §2`에 두 편집을 한 커밋으로. 첫째, §2.1 영어-전용 조항 일반화(F7).
파일 열거를 "미러 대상은 `docs/`·`plans/`·`README.md`뿐. `phase2/`·`phase3/` 작업 트리와 모든 `_*`
서브트리는 영어 전용"으로 교체 — `check-mirrors.sh`가 이미 강제하는 동작과 일치시킨다.
둘째, §2.4 추가. 빠진 수거/승격 규칙을 명시.

- working dir의 산출물이 `docs/`로 안착하면, **trio를 커밋**(결정 로그가 됨)하거나 **디렉토리 삭제**.
  추적 0개인데 산출물이 나간 working dir를 절대 방치하지 않는다.
- `_recovered/`와 빈 scratch 디렉토리는 **절대 커밋하지 않으며** 병합 후 삭제.
- 중간 audit/scratch JSON은 canonical errata 옆이 아니라 gitignore된 `_scratch/` 서브디렉토리에.
- 1회성 스크립트는 `tools.md` 한 줄 + `# one-shot:` / `# regenerable:` 헤더.
- 커밋 1개. `docs(agents): generalize §2.1 mirror scope + add §2.4 artifact-lifecycle rule`.

### 3.4 툴 인덱스 backfill (F4) + F3 context-notes 결정

- 누락된 `scripts/refs/*.py` 7개 줄을 `tools.md`에 추가(+ ko 미러).
- `phase3/{eps_ind_a,hd_219134}/context-notes.md`를 커밋 또는 삭제(커밋 권장 — F3 참조).
  커밋한다면 새 §2.4 trio 규칙을 따른다.
- 커밋. `docs(tools): index 7 scripts/refs builders` 그리고 (노트 커밋 시)
  `docs(phase3): commit eps Ind A / HD 219134 synthesis decision logs`.

---

## 4. 미해결 질문

- 게이트 8의 **경고 vs 실패** — 수거 대상 working dir를 CI 실패로 볼지 경고만 할지.
  경고 쪽으로 기운다(로컬 전용이라 git엔 무해). 단 빈 디렉토리·미등록 스크립트 하위 점검은 hard fail.
- 중간 audit JSON의 **`_scratch/` vs 삭제** — 재-triage용 gitignore 흔적을 남길지, `git log`를 믿을지.
  `phase3/_audit/`는 지금 전부 보존한다. 디스크-색·F1 감사 경험상 중간 JSON을 가끔 다시 읽으므로,
  완전 삭제보다 gitignore된 `_scratch/`가 낫다는 쪽으로 기운다.
- 게이트가 `plans/` 라이프사이클(삭제 안 된 archived 상태 파일)도 커버해야 하나? v1 범위 밖.
