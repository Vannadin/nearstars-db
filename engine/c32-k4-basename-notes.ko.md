<!-- 병렬석 조사 기록 (원문 무편집). C33: the base-name collision measured, and the parallel seat's three corrections to its own report. -->
<!-- Preserved verbatim from the parallel seat's scratch on 2026-09-05. C33: the base-name collision measured, and the parallel seat's three corrections to its own report. -->
<!--     The author corrected this note before it was committed: the first-edition sentences are kept in
     place with the correction marked beside them, so it reads as a record of both. That is the author's
     own revision, not an edit by the work seat. -->
# K-4 (모호한 basename) + 2-8 실측 (payload 리터럴 WARN 의 정밀도)
Parallel seat, 2026-09-05. HEAD 1a837cb0, 읽기 전용, 레포 쓰기 없음. 게이트 안 돌렸습니다.

# ⚠ K-4 — 발주의 전제 둘을 정정해야 합니다. 그리고 그중 하나는 제 잘못입니다.

## ① 결함은 **이미 수리돼 있습니다**
`engine/check_refs.py` 현재 상태(`ambiguous()`, `:147-159`):

> "Resolution used to walk `docs/reference` → the citing file's directory → `engine/` → the repo
> root and stop at the first hit, so a citation to `checklist.md` quietly meant whichever one sat
> next to the citing file — and the repo has 68 of those, 68 `context-notes.md`, 22 `README.md`.
> Choosing by proximity is choosing without saying so, which is the thing this checker exists to
> stop. **A bare name that could mean more than one file is now a failure**, and the fix is to
> write the path."

그리고 지금 체커는 **PASS** 합니다 — 모호한 bare 이름으로 인한 FAIL 이 **0건**입니다.
즉 "18개의 정답 경로 표"를 만들 대상이 오늘 레포에는 없습니다.

## ② 제 2-3 서술의 "이미 깨져 있는 두 건"은 **부류를 잘못 붙였습니다**
제가 `C32-O-ANCHOR-RISK.md` 2-3 에 적은 두 건은 **basename 모호성이 아니라 해석 순서 미탐**입니다.
- `backflow-checklist.md:73` 의 `…geometry-methodology.md` — 파일명이 **생략표(…)로 잘려** 레포에
  그 이름의 파일이 **아예 없습니다**. 모호한 것이 아니라 존재하지 않는 이름입니다.
- `interior-core.md:964` 의 `make_hhe_table.py` — 레포에 **경로가 하나뿐**(`engine/tools/…`)이라
  모호하지 않고, 4단계 순서(`docs/reference/` → citer 디렉터리 → `engine/` → 루트)가 그
  `engine/tools/` 를 시도하지 않아 못 찾은 것입니다.
**두 건 다 "경로를 못 찾는" 결함이고 "여러 경로 중 조용히 고르는" 결함이 아닙니다.** 2-3 의
"오늘 두 건이 이 부류로 이미 깨져 있었습니다" 는 정정합니다.

## ③ 제 "18개" 숫자도 **제 스캐너의 산물**이었습니다
저는 `[A-Za-z0-9_.-]+\.md` 로 잡았고 그 패턴은 **`/` 를 제외**합니다. 그래서 이미 경로가 붙은 인용
(`phase3/stellar_wind_synthesis/context-notes.md:28-30`)의 **꼬리만 잘라내** bare 이름처럼 세었습니다.
체커의 패턴은 `FILE = r"[A-Za-z0-9_./-]+\.(?:md|yaml|yml|py|json|tex|sh)"` 로 **`/` 를 포함**하므로
그런 잘림이 없습니다. **체커 버그가 아니라 제 스캐너 버그입니다.** 하마터면 제 버그를 남의 결함으로
보고할 뻔했습니다.

## ④ 그래서 실제로 남은 것 — **모호성 위험은 오늘 딱 한 자리**

제 스캐너로 잡은 273건(부풀려진 수)을 체커의 4단계 순서로 다시 해석해 보면:

| 해석된 단계 | 건수 | 그 선택이 옳은가 |
|---|---|---|
| `docs/reference/` (step 0) | **257** | ✅ 옳습니다 — citer 가 `engine/` 의 노트·코드이고 뜻한 것은 en 원본입니다 |
| citer 디렉터리 (step 1) | 1 | ⚠ 아래 |
| `engine/` (step 2) | 2 | ⚠ 아래 |
| 넷 다 실패 | 13 | 안전(보임) — 그리고 대부분 위 ③의 잘림 산물입니다 |

**근접성이 조용히 골라서 틀린 자리는 하나입니다** —
`ko/docs/reference/internal-heat-luminosity-methodology.md:100` 이 bare `core-state-methodology.md` 를
인용하고, step 0 이 **en 원본**을 고릅니다. ko 쌍둥이가 있고 그 줄(ko:60)은 **다른 문장**입니다.
⚠ 그리고 이건 **체커가 일부러 잡지 않습니다** — `sharing_the_name()` 이 `skip = {…, "ko", …}` 로
ko 를 제외하며 그 이유를 적어 둡니다: *"`ko/` holds a translation of the same document, not a
different file, so a mirror is not a second meaning"*. **설계 판단이 맞고, 그래서 미러 위험은
모호성 규칙으로 닫히지 않습니다** — 이미 오너 아침 목록에 올라간 그 항목입니다.

나머지 셋(step 1·2)은 전부 **인용이 아니거나 레포 밖입니다**, 즉 고칠 것이 없습니다:
| 자리 | 실제 뜻 |
|---|---|
| `.agents/skills/researchbodies-cfg-workspace/research-notes.md:89` | 원문이 "GitHub `README.md:5`" — **업스트림 프로젝트의 GitHub README**. 레포 밖 인용 |
| `plans/wiki/checklist.md:21` | `- [x] README.md: add a wiki link (+ ko mirror)` — **고칠 파일을 적은 체크리스트 항목**이고 줄 인용이 아님(줄번호도 없음). 스캐너 오탐 |
| `phase4/field-standard/FINDINGS.md:77` | 원문이 `emit-hardening/checklist.md:49` 로 **이미 경로가 붙어 있음**. 제 스캐너가 꼬리만 자른 산물(③) |

**K-4 결론**: 표로 낼 "18개 정답 경로"는 없습니다. 실제 작업 대상은 ⓐ 미러 규칙(오너 결정 대기) 과
ⓑ 배치 B 에 이미 올린 두 건(`…geometry-methodology.md` 파일명 복원, `make_hhe_table.py` → `engine/tools/`)
입니다. ⓑ 는 모호성이 아니라 경로 미탐이므로, **해석 순서에 `engine/tools/` 같은 하위 디렉터리를
넓히기보다 인용 쪽에 레포 상대 경로를 쓰게 하는 편**이 같은 값에 더 안전합니다(찾기가 넓어지면
③처럼 조용히 맞히는 경우가 늘고, 그게 이 체커가 없애려는 것입니다).

# 2-8 실측 — payload 리터럴 WARN 을 전수로 켜면 정밀도가 **0 %** 입니다

## 방법
앵커형 chain 간선 중 `via:` payload 가 있는 **91건**에 대해, payload 이름(과 `_` 로 쪼갠 토큰)이
**앵커 문자열 안에** 리터럴로 있는지 봤습니다. **없는 것 61건 (67 %)**. 그중 **무작위 20건(seed 7)** 을
손으로 갈랐습니다.

## 결과 — 20건 중 **진짜 느슨한 조준 0건**

| 분류 | 건수 | 내용 |
|---|---|---|
| **(A) 정당한데 표기만 다름** | **9** | payload 가 같은 양을 **다른 표기**로 적은 것 |
| **(C) 의도적인 계약·절 제목** | **11** | 제목을 앵커로 쓴 결과 payload 는 블록 본문에 있음 |
| **(B) 진짜 느슨** | **0** | — |

**(A) 아홉 건**
- `555` `k2_over_q` ↔ 앵커 `` `k₂/Q` is the **dominant uncertainty** `` — 같은 양, 유니코드 표기
- `556` `k2_over_q` ↔ `` `Q/k₂` is the shared interior unknown `` — 같은 양, 역수 표기
- `558` `t_exo` ↔ `` **`T_exo` is the weak input.** `` — **대소문자만 다름**
- `583` `j2` ↔ `**(c) Eccentricity + permanent quadrupole → …**` — "permanent quadrupole" = J₂
- `590` `p_rot` ↔ `| **Fomalhaut A** | star (A4V) | P_rot ≈ 24 h` — **대소문자만 다름** (`'p_rot' in …` = False, `'P_rot' in …` = True — 실측)
- `618` `radius` ↔ `the tidal-heating rate goes as` … 다음 줄이 `R⁵, so the radius assigned here is **high-leverage**` — **앵커가 한 줄이라 잘렸을 뿐** payload 가 바로 다음 줄에 있음
- `686` `layer_fractions` ↔ `from mass, radius and the declared ice fraction` — payload ≡ ice fraction
- `689` `geotherm` ↔ `core convection → a dynamo magnetic field` — H 에서 정답으로 확정한 자리
- `814` `t_eq_4term` ↔ `- [\`moon-energy-budget-methodology.md\`](…)` — 4항 Teq 를 **정의하는 문서**를 지목

**(C) 열한 건** — `680`·`699`·`700`·`708`·`715`·`720`·`724`·`818`·`821` 은 `## Contract — \`X\`` 제목,
`582` 는 `## 7. Procedure (per body)`, `636` 은 `### What sets the contrast: advection vs radiation`.
전부 **우리가 어젯밤 일부러 고른 앵커**입니다(주인 일치 규칙 / 절 단위 인용).

## 판정 — **전수로 켜지 마십시오. 재사용에만 두는 것이 맞습니다.**
- 전수(단일-사용 포함) 정밀도: 표본 20건에서 **0/20**. 61건 전체도 같은 두 부류로 보입니다.
- 실패 원인 셋 — ① **표기 차이**(유니코드 수식 `k₂/Q`·`T_exo`, 대소문자 `P_rot`, 동의어 "quadrupole"),
  ② **앵커가 한 줄이라 payload 가 다음 줄에 있는 것**, ③ **제목 앵커는 payload 를 담지 않는 것이 정상**.
- 지휘석이 "101 이라는 수만 보고 듣지 않는다고 판단했다"고 하셨는데, **표본으로 보면 그 판단이
  맞았습니다** — 다만 이유가 "너무 많아서"가 아니라 **"세 부류의 구조적 오탐이라서"** 입니다.
- ⚠ **재사용에만 둘 때도 오탐이 납니다**: 지금 체커가 내는 WARN 목록에 `chain:684`
  (`Ro_ℓ` 앵커, payload `locked`)와 `chain:773/774`(`C [g cm⁻²] = 0.1 · P [Pa] / g [m s⁻²]`,
  payload `column`/`gravity`)가 들어 있는데, **후자는 제가 L 에서 "재사용의 모범 사례"로 판정한
  자리**입니다 — payload 가 `C` 와 `g` 라는 **기호**로 식 안에 있고 `column`·`gravity` 라는
  **이름**으로는 없습니다. 즉 이 규칙은 **기호↔이름 대응을 모릅니다.**

## ⚠ 그리고 지금 구현에 버그가 하나 있습니다
체커 WARN 메시지가 payload 를 **다음 YAML 키까지 묶어** 보고합니다 —
`does not name cmb_temperature/ref` · `mass/ref` · `t_body/ref` · `locked/ref` · `rossby/status` ·
`mass/radius`. payload 는 `cmb_temperature` 하나이고 `ref`·`status` 는 그 뒤의 키입니다.
`via:` 값을 쉼표에서 끊지 않고 다음 키 이름까지 삼킨 것으로 보입니다. 메시지만의 문제일 수도 있고
판정에도 쓰인다면 오탐이 늘어납니다 — 작업석 확인 대상입니다.

## 권고 (판단 사항은 표시)
1. 규칙은 **재사용(2회 이상) 앵커에만 WARN** 으로 유지 — 전수 확장은 정밀도 0 %.
2. 오탐을 줄일 값싼 두 가지: **대소문자 무시**, 그리고 **앵커 뒤 한 줄까지 창 확대**.
   (표본에서 이 둘만으로 `558`·`590`·`618` 세 건이 사라집니다 — 20건 중 15 %)
3. **기호↔이름 사전은 만들지 않기를 권합니다** — `column`→`C`, `gravity`→`g`, `k2_over_q`→`k₂/Q` 를
   손으로 유지하는 비용이 규칙의 값보다 큽니다. 대신 **제목 앵커는 규칙에서 면제**(제목이면 payload 를
   담지 않는 것이 정상)하면 표본의 (C) 11건이 전부 사라집니다.
4. ⚠ **결정 필요**: 위 2·3 을 적용하면 표본 20건 중 남는 것은 **0건**입니다. 즉 이 규칙은
   "재사용 + 제목 아님 + 대소문자 무시 + 두 줄 창" 까지 좁히면 **오늘 레포에서 아무것도 잡지 않습니다.**
   규칙을 남길지(미래의 오조준을 위한 그물) 지울지(지금 값이 0)는 **오너 판단**입니다.
