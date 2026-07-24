# NearStars — 작업 컨벤션

**이 문서는.** NearStars의 작업 컨벤션 — 행동 규칙과 프로젝트별 큐레이션·데이터 규율 — 을 한곳에 모은 것이다(이전엔 메모리에 산재). `CLAUDE.md`가 항상 켜지는 핵심을 담고 이 문서를 가리킨다. 이 파일은 전체 레퍼런스다. **PORTABLE** 컨벤션(모든 프로젝트에 적용 가능)과 **NEARSTARS-SPECIFIC** 컨벤션을 따로 표시했고, PORTABLE 세트는 형제 repo가 재사용하는 기준이 된다.

---

## 1. 의사소통 및 언어 — PORTABLE

### 1.1 한국어 존댓말 사용
**규칙:** 모든 사용자 응답에서 형식적인 한국어(존댓말/합쇼체 또는 해요체)를 항상 사용한다.
**이유:** 사용자 직접 요청.
**출처:** `feedback_speech_level.md`

### 1.2 마크다운 원문 언어
**규칙:** 모든 공개 `.md` 문서(`docs/`, `plans/`, `README.md`)는 **영어를 원문으로** 작성한다. 한글 미러는 자동으로 `ko/<같은-경로>`로 생성된다.
**이유:** (1) 코드베이스 언어와 일관성 유지, (2) 향후 협력자가 문서 참조 가능, (3) 미러를 통해 한/영 토글 용이. 정규 읽기는 영어이고, LLM 에이전트도 반복 파싱 오버헤드를 피하기 위해 영어로 읽는다.
**상세:**
- 미러 대상: `docs/`, `plans/`, 루트의 `README.md` → 같은 커밋에 `ko/` 트리 자동 동기화
- 미러 제외: `CLAUDE.md`, `AGENTS.md`, `db/**`, `scripts/**`, PR/이슈 템플릿, 언더스코어 프리픽스 디렉터리
- 승격: 플랜이 레퍼런스로 졸업하면 `docs/reference/`의 EN+KO로 이동 후 원본 플랜 파일 삭제(git 로그로 아카이브)
**출처:** `feedback_md_language.md`

### 1.3 한글 미러 문체
**규칙:** 한글 미러는 자연스럽게 쓴 한국어처럼 읽혀야 하며, 단어 대 단어로 번역한 것처럼 느껴지면 안 된다. 각 문단 블록 내에서 문장을 자유롭게 재구성하되(build_html.py를 위해 블록 개수는 영문과 일치), 한국어 관용어와 자연스러운 절 순서를 사용한다.
**이유:** 직역은 어색한 문체를 낳는다. 문장 구조가 근본적으로 다르다(동사 최종형, 조사 중심).
**상세:** 문장 끝을 `.` / `?` / `!`로 마치며 `:`는 절대 사용하지 않는다. 표 구조는 동일하게 유지하되, 흐르는 산문 칼럼만 번역한다.
**출처:** `feedback_ko_mirror_style.md`

### 1.4 문서 열기(preview-md.sh)
**규칙:** 사용자가 "열어줘"라고 하면 한글 미러(`ko/<같은-경로>`)를 `scripts/preview-md.sh`로 HTML 렌더링하여 브라우저에서 자동 오픈한다(macOS `open` 명령).
**이유:** 사용자가 한국어로 읽는 것이 편하다. 미러 정책이 정확히 읽기 시나리오를 위해 존재한다.
**상세:** 한글 미러가 없으면(`AGENTS.md`, `CLAUDE.md`, `db/**` 등) 영문 원본으로 대체. 명시적인 "영문으로 열어줘" 요청이 우선.
**출처:** `feedback_open_doc.md`

### 1.5 플랜 검토 언어 및 구조
**규칙:** 플랜이나 긴 문서를 검토 제시할 때 **이중 언어**로 작성한다: 한국어(읽기용) + 영어(실행/코드 참조용). 이중 언어 플랜 파일은 EN/KO 섹션 쌍을 사용하여 Obsidian과 승인 UI에서 한국어가 먼저 나타나도록 한다.
**이유:** 사용자가 모국어로 검토 가능하고, 실제 구현은 영어 기반으로 유지된다.
**출처:** `feedback_plan_review_korean.md`

### 1.6 설명에서 궤도요소 약어 금지
**규칙:** 설명적 글쓰기에서는 궤도요소를 풀어서 쓴다: 이심률(e 아님), 경사각(i 아님), 장반경(a 아님), 근일점/원일점(q/Q 아님).
**이유:** 사용자가 설명에서 약어가 혼동스럽다고 느꼈다.
**상세:** 코드 필드명, 차트 축, 정식 표기(방정식)는 약어를 유지한다. "라벨할 때는 e/i/a 사용, 설명할 때는 풀어서 쓰기"가 규칙이다.
**출처:** `feedback_no_orbital_abbreviations.md`

### 1.7 휴식 제안 금지
**규칙:** 작업 단위를 완료한 후 상태를 보고하고 다음 단계를 제안한다. "쉬세요 / 휴식 / 에너지 관리" 류 제안은 **절대 하지 않는다**.
**이유:** 사용자가 페이스 조절을 스스로 한다("ㄱㄱ"로 진행, 턴 종료로 멈춤). 원하지 않는 휴식 제안은 무시하는 느낌을 준다.
**상세:** 실제 차단 요인이 있으면(외부 의존성, 누락된 결정) "진행하기 전에 X가 필요함"이라고 말하고, "휴식 취하세요" 같은 건 하지 않는다.
**출처:** `feedback_no_rest_suggestions.md`

### 1.8 Git 커밋 메시지 언어
**규칙:** 모든 git 커밋 메시지(주제 + 본문)는 **영어**로 작성한다. Co-Authored-By 트레일러 포함.
**이유:** 공개 GitHub 표면; 영어는 같은 줄의 코드/파일명/식별자 언어. `feedback_md_language`의 영문 원본-진리 원칙과 일관성.
**상세:** 커밋에서 도메인 용어는 영어로("synthesis", "curation", "audit pass" — 합성/큐레이션/감사 아님). 과거 한글 커밋은 수정 없음. 대화는 한국어 존댓말로 진행.
**출처:** `feedback_commit_language.md`

### 1.9 Git 정체성(고정)
**규칙:** 모든 커밋은 다음 정체성을 사용한다: **user.name = `VaNnadin`**, **user.email = `vannadin00@gmail.com`**(로컬 config, --global 아님).
**이유:** 사용자가 명시적으로 통일된 작성자 정체성을 요청.
**출처:** `feedback_git_identity.md`

---

### 1.10 산문에 엠대시 금지
**규칙.** 모든 `.md` 문서에서 영어 원본이든 한국어 미러든 엠대시(U+2014 문자)를 쓰지 않습니다. 문맥에 맞는 부호로 바꿉니다. 뒤가 설명·부연이면 콜론, 가벼운 삽입구는 쉼표, 두 문장으로 나누면 마침표, 감싼 삽입구는 괄호를 씁니다.
**이유.** 오너 스타일 지시(2026-07-21). 엠대시는 LLM 티가 나고 문장을 어수선하게 만듭니다.
**세부.**
- 숫자 범위(`227–299 K`)나 합성어(`Radau–Darwin`)에 쓰는 엔대시(–, U+2013)는 올바른 표기이므로 그대로 둡니다.
- 표의 "데이터 없음"을 뜻하는 단독 엠대시 셀은 엔대시(`–`)로 바꿉니다.
- 엠대시를 쓰던 제목은 콜론으로 바꾸고, 그 제목을 가리키는 페이지 내 목차 앵커도 새 슬러그에 맞춰 함께 고쳐 링크가 깨지지 않게 합니다.
- GitHub 위키와 방법론 18편은 이미 정리됐고, 나머지 레퍼런스 문서는 손댈 때 함께 변환합니다.
**출처.** 오너 지시 2026-07-21.

## 2. 워크플로우 및 자율성 — PORTABLE

### 2.1 자율 실행
**규칙:** 방향이 정해지면 단계별 승인을 기다리지 않고 완료까지 진행한다. 원래 범위에 포함되지 않은 진정한 비가역 작업(파일 삭제, 파괴적 git 작업)만 멈춘다.
**이유:** 반복되는 "진행해도 되나?" 질문은 흐름을 깬다. 명확한 작업 방향은 중간 단계를 안전하게 만든다.
**상세:** 파일 쓰기, 스크립트 실행, 데이터 변환은 확인 없이 진행한다. 다만 판단력 유지: 수정 전에 먼저 읽기, 삭제 전에는 항상 확인.
**출처:** `feedback_autonomy.md`

### 2.2 서브에이전트 위임(토큰 경제)
**규칙:** 무거운 읽기(캐시 그렙, 논문 본문, DB JSON 생성, Phase 3 초안, 한글 미러 문체)는 동결 캐시를 가진 서브에이전트에 위임한다. 메인 스레드는 **스펙을 통한 값 검증**(결정론적 그렙 + 패리티, 재읽기 아님)만 한다.
**이유:** 읽기를 소수 에이전트에 집중시켜 동결된 bibcode/arxiv 캐시로 재다운로드 팽창을 방지하고 메인 컨텍스트를 깔끔하게 유지.
**상세:** 서브에이전트는 구조화된 출력 + 인용문을 반환. 메인은 `check.sh` + 블록 패리티 검증 수행. 큐레이션된 DB: `json.dump` 직접 사용 금지 — `apply_phase2.py` 또는 `schema.write_canonical` 사용하여 들여쓰기/키 순서 불변식 보존.
**출처:** `feedback_agent_token_saving.md`

### 2.3 감사 비용 규율
**규칙:** **리포트당**(에이전트 하나가 리포트 하나의 전체 발견 세트를 재확인), 발견당 아님으로 배치 검증한다. 대부분의 발견은 결정론적(그렙, 재계산); "논문 값 다름"만 에이전트 읽기 필요. 제약은 **일일 토큰 쿼터**이며, 세션 컨텍스트 아님.
**이유:** 발견당 팬아웃은 에이전트 수를 발견 수로 곱한다(232개 발견 → 232개 에이전트 = 일일 쿼터 소진). 세션 컨텍스트는 계속 살아있고, 일일 쿼터가 진정한 희소 자원.
**상세:** 큰 팬아웃 전 비용 추정. 일일 한계에 가까우면 지속 가능한 상태 저장 후 다음 세션에서 재개.
**출처:** `feedback_audit_cost_discipline.md`

### 2.4 도구 조회(`docs/reference/tools.md` canonical)
**규칙:** 사용자가 "X에 쓸 도구 있어?"라고 물으면 먼저 `docs/reference/tools.md`(EN) 또는 `ko/docs/reference/tools.md`(KO)을 읽는다. 그 인덱스가 정규. 없으면 그렙으로만 확장.
**이유:** ~30개 도구가 7개 디렉터리에 산재; canonical 인덱스는 중복 검색 + 불일치 방지. 인덱스가 오래되면 메모리 무용지물.
**상세:** 새 도구는 인덱스 업데이트 + 한글 미러 동기화 + check-mirrors.sh 검증 의무.
**출처:** `feedback_tools_lookup.md`

### 2.5 레퍼런스 문서 위치
**규칙:** 읽을 가치가 있는 문서 → `docs/reference/`(EN) + `ko/docs/reference/`(KO 미러). 스킬은 **링크**, 복사본 금지.
**이유:** `check.sh` §2에서 이미 레퍼런스 문서 미러 검증. 문서는 사용자 읽기용; 스킬 폴더는 순수 스캐폴딩(conflict 타이브레이크, 채점 루브릭)이나 EA 보호 콘텐츠만 보유.
**상세:** EA 파생 문서는 `.claude/skills/*/references/`에 유지(영어만, gitignore). 공개 지식은 먼저 `docs/reference`로 이동.
**출처:** `feedback_reference_doc_location.md`

### 2.6 서브에이전트 팬아웃은 Opus로
감사·리뷰·대량 위임 서브에이전트는 세션 모델(Fable일 수 있음)이 아니라 `model: "opus"`로 돌린다. `subagent_type: "fork"`는 override를 무시하므로, 중요할 땐 비-fork 에이전트를 쓴다.
**출처:** `feedback_agent_model_opus.md`

---

## 3. 논문, 데이터 근거 및 규율 — PORTABLE + NEARSTARS-SPECIFIC

### 3.1 도출값 근거화(PORTABLE)
**규칙:** 비자명 천체물리 도출값(J2, 조석 가열, 대기 이탈, 유효 온도(온실 포함), 내부 구조, Love 수, 자전 진화)은 **방법 논문을 인용**해야 한다. 뒷면 계산 추정은 인정 안 됨.
**이유:** 프로젝트 DNA = Phase 2는 논문 인용. 소박한 근사는 실제 모델 가정을 숨긴다(예: 내부 구조 → J2 범위 0.105–0.165; 0.028 추측은 이 범위를 숨김).
**상세:**
- 방법은 근거화 필요: 도형 이론 논문 + 캘리브레이션 출처(예: 가스 자이언트 측정 J2, Iess 2018)
- 교과서 폐형(Roche, Hill, Kepler, 입체각, 단위 변환)은 자체 정당
- 가정과 결과 범위 명시
- 위조 논문 인용 금지; 실제 ADS bibcode나 arxiv_id 사용
**출처:** `feedback_derived_value_grounding.md`

### 3.2 ADS 논문 규율(NEARSTARS)
**규칙:** 모든 논문/인용 작업은 **등록된 ADS API 키**(`~/.zshrc`의 `ADS_API_TOKEN`)를 사용한다. 임의 WebSearch 금지. `scripts/phase3/fetch_arxiv_texts.py`로 arxiv 텍스트를 캐시에 저장하고 캐시만 읽는다(live web 재쿼리 금지). 문헌 발견은 에이전트가 ADS `citation_count DESC` 쿼리를 독립 실행(종이 목록 직접 제공 금지).
**이유:** 2026-06-23 사건: 서브에이전트가 WebSearch + 내 하드코딩 arXiv ID 사용 → 여러 잘못 ID(Pierrehumbert 논문은 무관 수학, Hu & Yang ID는 실제로 Leconte 2013) + canonical 논문 누락. ADS-큐레이션 권한 + 동결 캐시로 전환.
**상세:**
- 흐름: `docs/phase3/_bib/<slug>.yaml`에서 arxiv_id 핀 → `fetch_arxiv_texts.py` 실행 → 캐시 읽기(웹 아님) → 서브에이전트 캐시 라인 인용으로 값 검증 → 메인 검증
- 유령 논문 방지(2026-06-20 교훈): 논문을 위조로 플래그하기 전에 **웹/ADS/arXiv로 비존재 검증**. "우리 캐시에 없음" ≠ "존재하지 않음". Yadav & Thorngren 2017([1709.05676](https://arxiv.org/abs/1709.05676))과 Reiners & Christensen 2010([1007.1514](https://arxiv.org/abs/1007.1514))은 둘 다 실제지만 범위 밖/미캐시.
**출처:** `feedback_ads_paper_discipline.md`

### 3.3 논문 레퍼런스는 링크로(NEARSTARS)
**규칙:** 사람이 읽는 문서의 논문 레퍼런스는 전부 **마크다운 링크**로 쓴다. bibcode는
`[2018Icar..305..262I](https://ui.adsabs.harvard.edu/abs/2018Icar..305..262I)`,
arXiv id는 `[1007.1514](https://arxiv.org/abs/1007.1514)` 형태. bibcode가 없으면 DOI
링크도 허용. 맨 id는 기계 필드(YAML `bibcode:`/`arxiv_id:`, JSON, 코드)와 코드 블록
안에서만 남긴다.
**이유:** 오너 지시(2026-07-20). 문서 검토 때 레퍼런스가 한 클릭 거리여야 하고, 맨
bibcode는 ADS 왕복을 강요한다.
**세부:** `docs/`·`plans/`·`phase2–4/*.md` 본문 + ko 미러에 적용. 기존 문서는
스크립트로 일괄 변환(pipeline-flow-program WP6), 새 문서는 즉시 준수.
인용이 나타나는 모든 곳(GitHub 위키, emit된 cfg 주석 같은 생성 아티팩트 포함)에 적용된다. 평문 아티팩트는 `https://ui.adsabs.harvard.edu/abs/<bibcode>` 전체 URL을 붙인다.
**출처:** `feedback_citation_links.md`, `feedback_derived_value_grounding.md`.

### 3.4 일반화 우선(PORTABLE)
**규칙:** 새 기능은 **데이터 주도 config**로 모든 경우 작동해야 하며, 한 인스턴스용 하드코딩 금지. 첫 번째 경우가 일반 경로의 첫 소비자.
**이유:** 일회성 해킹은 규모 확장 안 됨. 다음 시스템은 코드 재작성 아닌 코드+config 필요.
**예:** Polyphemus stability-sim 시각화는 일반 `load_stability()`(이미 바디명 무관) 재사용, Polyphemus 커스텀 파서 아님.
**출처:** `feedback_generalize_over_hardcode.md`

---

## 4. NearStars 별 및 행성 큐레이션 — NEARSTARS-SPECIFIC

### 4.1 별 추가 의사결정 자동화
**규칙:** 별 추가 요청 시: (1) SIMBAD TAP로 Gaia DR3 source_id 조회(`ident` → `oidref`), 질문 금지. (2) `recommended` 측정은 stellar_db_methodology 방법 우선순위로, 질문 금지.
**이유:** 사용자가 명확한 방법론 규칙으로 이미 위임. 자율성 원칙 [[feedback_autonomy]].
**상세:**
- 방법 우선순위: 질량 = binary_orbit > 진동 분광 > 진화 모델 > 분광학 > 분광학 캘리브레이션. 반지름 = 간섭 측량 > 식쌍성 > 진화 모델.
- 타이브레이크: 가장 낮은 상대 불확실 승리. 메타.notes에 한 줄 이유 기록.
- 폴백: SIMBAD Gaia 조회 실패(포화) 시 HIPPARCOS_V 경로 사용.
**출처:** `feedback_star_addition.md`

### 4.2 행성 큐레이션 깊이(두 단계)
**규칙:** **Phase 1(기본, 모든 별):** 방법론 표준. ADS에서 검출 논문(또는 최신 재분석) 찾기 → 큐레이션 항목. 배치 재빌드: NASA Archive `ps` 테이블 + 행성별 bibcode 검증 사용; 방법 검증 스킵 "배치 지름길" 금지. RV 행성: DACE에서 누락된 ω, T_peri 확인. **Phase 2(인게임 구현 결정 시):** 전체 출처 풀. 방법론 우선순위 1–5 전부 확인; 발표된 모든 측정 축적; 방법-계층 충돌 보고.
**이유:** Phase 1 전부 = 144개 별 × 5시간 이상 = 불가능. Phase 2는 인게임 시스템만(릴리스 사이클당 1–2개) = 합리적 깊이. DB 완성도 + 작업 효율 트레이드오프.
**상세:**
- Phase 1: 방법 라벨은 `unverified` 가능(Phase 2 대상 표시)
- Phase 2: 각 논문 직접 읽고, 방법 종류 검증
- 절대 금지: 방법 라벨 조작 또는 배치 가명사 사용
- 배치의 경우: NASA Archive 합성(`pscomppars`) 사용 금지; 논문별 행(`ps`) + `default_flag=1` 사용
**출처:** `feedback_planet_curation.md`

### 4.3 금속량[Fe/H] 스킵
**규칙:** 신규 Phase 2 호스트: 금속량 조사 스킵. 기존 항목은 유지(삭제 금지).
**이유:** KSP 게임플레이 영향 무시할 수준. (1) 항성 색: [Fe/H]는 3차 선 블랭킹 타이브레이크, 모든 Phase 3 노트가 "인지 이하"라고 함. (2) 자기장: 자전과 활동 주도, [Fe/H] 무관. (3) Kopernicus: 금속량 필드 없음. (4) 나이: 약한 2차 용도; 나이 자체가 KSP 렌더에 영향 없음.
**상세:** 우선순위 순서(높음→낮음 영향): 자전 > 활동 > Teff/R/L/mass > 나이 > 금속량(스킵).
**출처:** `feedback_skip_metallicity.md`

### 4.4 흥미-우선 및 연쇄 값
**규칙:** Decisions 값에 흥미-우선 적용 시, 물리적으로 연결된 모든 값(albedo, extent, 온도 기반, 대기 프레이밍, 문체, 시각)을 연쇄시켜 내부 일관성 유지. "## Canonical alternatives" 표에 정규(문헌 충실) 대안 문서화.
**이유:** 한 셀 변경이 연쇄 효과 낳음. 이론은 여전히 "흥미" 선택을 지지해야 함(이론 배제 흥미 = 나쁨). 정규는 병기 유지.
**예:** TRAPPIST-1 f 안구-대양 지지는 눈덩이 GCM 붕괴 → Europa 유사 빙저 대양 대신 선택(여전히 흥미, 이론 지지).
**출처:** `feedback_interesting_first_cascade.md`

### 4.5 게임플레이 다양성 편향
**규칙:** "반드시 존재 금지"(확인된 비존재, 철회, 위조) 아니면 항상 게임플레이 풍성함 선택. 경계선 경우 포함: 잠정 검출, M sin i 후보, 천측 단일. "Canonical alternatives" + cultural-context.md에 문화적 발산 문서화.
**이유:** NearStars는 KSP 콘텐츠 우선; 과학적 보수주의는 2차.
**상세:**
- 위성: 관대히 추가; stability-sim으로 동역학 검증
- 고리 주의: search-and-verify만; delta Pav 위조 화상으로 생성 금지
- 문화적 무게 철회 행성(Trek, PHM Adrian): 이의 문체 + 변형으로 유지, 재철회 금지
**출처:** `feedback_gameplay_variety.md`

### 4.6 Phase 4 예술-방향 facet 및 선택
**규칙:** Phase 4는 모든 시각 facet(색, 기능, 표면, 대기)을 사용자에게 2–4개 옵션 각각으로 제시. 사용자는 facet당 최소 1회 명시적 선택. 예술-방향 문서(`phase4/<body>-art-direction.md`)는 간결한 보드(`phase4/*.yaml`)와 분리하여 풍부 컨텍스트(palette hex, feature scale, mood, signature landscapes) 축적.
**이유:** 사용자는 모든 시각 결정에 명시적 주도권 원함, 풍부 참고자료 지원.
**상세:** 침묵 통과 금지. 보드 항목은 gated 출력; 예술-방향 문서는 연구 깊이 보유(Parallax grain size, EVE cloud physics, Firefly temperature anchors) 텍스처/시각 패스용. 과학-리포트 텍스트(per-biome context)는 별도 향후 작업.
**출처:** `feedback_phase4_facet_choices.md`

---

## 5. 데이터베이스 및 파이프라인 아키텍처 — NEARSTARS-SPECIFIC

### 5.1 DB 원칙: null ≠ zero
**규칙:** `db/systems/*.json`의 `derived` 블록은 **단위 변환 + 측정 병합만** 수행. 측정 없음 → `null`(0이나 90° 같은 기본값 아님). 기본값(경사각=90, 이심률=0)은 Kopernicus cfg 책임.
**이유:** 측정된 0(예: Proxima b 이심률=0)은 가정-부재와 구별 가능해야 함. 다운스트림 cfg 작성자가 mod 적절 기본값 선택하려면 null 필요.
**상세:** `build_planet_derived`는 우선순위 병합(curated > tepcat > raw) → null 사용, 절대 `0.0` 폴백 아님.
**출처:** `project_nearstars_db_principle.md`

### 5.2 정규 명명: _naming.py 단일 모듈
**규칙:** 모든 slug/파일명 변환(`to_url_slug`, `to_file_slug`, `to_filename`)은 **`scripts/pipeline/_naming.py`에만** 존재. 모든 빌더는 그것을 임포트; 재구현 금지.
**이유:** Barnard split into `barnard-s` / `barnards`(git 히스토리) → manifest 불일치. 단일 출처는 발산 방지.
**상세:** URL slug는 `-` 구분자; 파일 slug는 `_` 구분자. 소문자 → 아포스트로피 제거 → 비알파뉴메릭 압축.
**출처:** `project_naming_canonical.md`

### 5.3 큐레이션 데이터 계약 및 수렴 규율
**규칙:** `phase2/curation-data-contract/SPEC.md`는 Phase 2/3 데이터 요구사항의 정규 정의. 수렴 규율: 모든 인용 값의 arxiv_id를 `docs/phase3/_bib/<slug>.yaml`에 핀 → `fetch_arxiv_texts.py`로 gitignore 캐시에 **한 번만** 가져오기 → 캐시만 읽기(live web 절대 아님). 한 번에 한 호스트; 다중 계층 편집(DB + narrative + 한글 미러)은 한 커밋에; 각 후 `check.sh` 게이트.
**이유:** 결정론 불명 live web 검색이 감사 발산 유발(매번 다른 논문, 다른 값 발견). 동결 캐시 + 단일 패스 + 호스트 하나씩 = 재현 가능.
**상세:** 호스트 1 템플릿이 검증 패턴 됨; 템플릿 증명 후에만 병렬 서브에이전트 배치. 40 Eri A/B/C 검증 깔끔(모든 20 arxiv_id 해결) 2026-05-29.
**출처:** `project_nearstars_curation_contract.md`

### 5.4 db/systems/*.json은 순수 파생(수동 편집 금지)
**규칙:** `db/systems/*.json`은 `build_systems.py` **출력**. 직접 편집 금지. 모든 enrichment는 출처 계층에 존재: `stellar_props_curated.json`, `planets_curated.json`, `binary_orbits.json`, `disks_curated.json`. 재빌드 재현성 불변식: 출처 계층 변경 없으면 실질 diff 없음.
**이유:** 2026-05-27 수정(commit 3ac7f55). Phase 3 작업이 수동 큐레이션 항목을 시스템 파일에 직접 작성; 다음 빌드는 자동으로 삭제(~44 디스크 항목 + narrative notes). 기계적 불변식은 인간 오류 놀람 방지.
**상세:** 확장 지점 존재(`meta_notes`, `sources_extra`, 측정별 빌드 제어 필드) enrichment용. 출력 수동 편집 대신 사용.
**출처:** `project_build_systems_wipes_phase3_enrichment.md`

### 5.5 고리/디스크 위조 — search-and-verify 규율
**규칙:** "고리 있는 별 추가해줘" 요청을 만족시키려 debris/circumplanetary 고리 지어내기 금지. 항상 인용 출처에서 search-and-verify.
**이유:** 2026-05-29 delta Pav 위조("Lawler & Tanner 2014" 위조 논문 + 30–80 AU 기하 조작). DUNES는 실제로 비검출. 긍정 선례: Alpha Cen A b 고리(Beichman 2025 JWST F1550C 밝기는 광학 농밀 고리 모델 지지)는 search-검증.
**상세:** 모든 디스크 호스트는 출처 타당성 감사(7개 완료 2026-05-29). 다중-벨트 지원 추가; 디스크 색은 Mie scattering(입자+조성) 합성으로 IR/mm-only 디스크(Vega, Fomalhaut inner, eps Eri); 측정-색 디스크(Fomalhaut main = grey, AU Mic = blue) 직접 고정.
**출처:** `project_nearstars_ring_fabrication.md`

---

## 6. 롤백된 패턴 — 재제안 금지

### 6.1 LLM 위키(Karpathy 패턴) — 2026-05-25 롤백
**규칙:** YAML frontmatter, wikilink 흐름-목록, `[[related]]` 메타데이터 주입, slash 명령어 `/wiki-*`, pre-commit hook, 주간 lint cron(문서 자동화) 제안 금지. 시도(commit 5661c4d → 7f40a77) 후 1d1c43b에서 롤백.
**이유:** (1) 사용자 목표 = "프로젝트 파일 최소 개입"; 59개 파일의 14줄 YAML은 위반. (2) YAML의 wikilink는 스펙 위반(Obsidian 특수 케이스; 다른 뷰어 깨짐). (3) 주간 cron + 4 slash 명령어 = 개인 프로젝트 규모에 과도. (4) 표준 `## Related` 섹션(마크다운 링크)이 파일 본문 수정 없이 Obsidian 그래프 밀도 동일 제공.
**상세:** 구조 지원은 `.obsidian/` overlay + entity/concept/synthesis 파일 사용(롤백 시 유지). 의미 유사성 시도(Smart Connections + Ollama)했으나 Pro 가입 필요($30/월).
**출처:** `feedback_llm_wiki_rolled_back.md`

### 6.2 NearStars 논문(방법론) — 2026-06-18 파킹
**규칙:** 정식 논문 작성(그림, venue 제출, 정량화 재현성)은 **파킹**. 현 액션 = context-notes.md에 방법론 엄격함 축적(작업공간별). 논문 그림 주도, venue 제안, 활발 초안 금지.
**이유:** 사용자가 "지금은 context-notes 꼼꼼히 쓰기만 하기" 말함. 논문 작업은 핵심 Phase 2/3/4 게임플레이 빌드에서 주의 분산.
**상세:** 4개 기초 칼럼 확인(재현 가능 파이프라인, 다중 별 에포크 전파, 안정성 재검증, 외부 관측자 벤치마크)은 한 astro-ph.IM 논문 형성. 플랜은 `plans/paper-scoping.md`(PARKED 태그) 저장. 재개 신호 대기.
**출처:** `project_nearstars_paper_parked.md`

---

## 규칙 간 조정

두 규칙이 상충해 보일 때의 정리.

- **서브에이전트 활용 vs. 비용:** 무거운 읽기는 동결 캐시 서브에이전트에 위임하되(§2.2), 검증은 발견당이 아니라 리포트당 배치한다(§2.3). 에이전트는 읽고, 메인 스레드는 `check.sh` + parity를 돌린다.
- **흥미-우선 vs. 이론:** §4.4는 *지지되는* 흥미로운 reading을 고르고, §4.5는 풍성함으로 편향된다. 이론-배제만이 유일한 hard stop이고, 경계선 경우는 게임플레이로 쏠린다.
- **파생 vs. 근거화:** §5.1은 `derived`에 기본값을 금지하고, §3.1은 방법 인용을 요구한다. 충돌 아님. 큐레이션 항목이 인용을 지니고, `derived`는 변환만 한다.
