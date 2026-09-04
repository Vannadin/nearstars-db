<!-- 병렬석 조사 기록 (원문 무편집). C33: what the citation checker does and does not scan, and what an extension would cost. -->
<!-- Preserved verbatim from the parallel seat's scratch on 2026-09-05. C33: what the citation checker does and does not scan, and what an extension would cost. -->
# N — 체커 SCAN 밖 세 범위 (조사만, 손대지 않음)
Parallel seat, 2026-09-05. HEAD db1b1fd0, 읽기 전용. **확장 여부는 오너 결정입니다.**

해석 규칙: 인용된 파일명을 ① citer 의 디렉터리 ② 레포 루트 ③ 레포 전체 basename 색인
순으로 찾고, 착지 줄을 빈줄/괘선/목차/표행/링크목록/계약/제목/산문으로 분류했습니다.

## ① `docs/reference/*.md` 본문끼리 — **2건, 썩은 것 0**

방법론 문서는 서로를 거의 **줄번호 없이 링크로만** 가리킵니다(`[name](name.md)`). 줄번호가 붙은
것은 전부 두 건입니다.

| citer | ref | 착지 | 상태 |
|---|---|---|---|
| `internal-heat-luminosity-methodology.md:112` | `core-state-methodology.md:60` | 산문 | ✅ 정확 — `using a similar method to ours". The core-side value on Earth is 3760 ± 290 K.` |
| `planetary-magnetosphere-geometry-methodology.md:585` | `scripts/viz/render_belts.py:50` | 산문 | ✅ 정확 |

**확장 비용: 거의 0.** 두 건이고 둘 다 이미 맞습니다. ⚠ 그런데 **`core-state-methodology.md:60` 은
`cmb_flux.py:148`·`cmb-heat-flux-context-notes.md:170` 도 쓰는 값**이라(배치 B A 절), 앵커화하면
네 곳이 한 앵커를 공유합니다 — 같이 처리하는 편이 값쌉니다.

## ② `ko/docs/**` 미러 — **2건, 그런데 하나가 실제로 어긋납니다**

| citer | ref | en 기준 | **ko 기준** |
|---|---|---|---|
| `ko/…/internal-heat-luminosity-methodology.md:100` | `core-state-methodology.md:60` | ✅ 정확 | ⚠ **어긋남** — `ko/…/core-state-methodology.md:60` 은 `모형에서** 그 차이를 1 M⊕ 에서 ~240 K, 3 M⊕ 에서 ~1880 K 로 냅니다` 로 **다른 문장**입니다. 의도한 문장(`지구의 핵 쪽 값은 3760 ± 290 K 입니다`)은 **ko:58** — 2줄 위 |
| `ko/…/planetary-magnetosphere-geometry-methodology.md:557` | `scripts/viz/render_belts.py:50` | ✅ (코드는 미러가 없음) | 해당 없음 |

**즉 ko 미러 안의 인용은 "어느 쪽 문서를 뜻하는가"가 명시되지 않는 한 절반이 틀립니다.**
한글 문서 안에서 `core-state-methodology.md:60` 이라 적으면 독자는 ko 미러를 열고, 그러면
다른 문장을 봅니다.

**하드 수치 — 미러는 구조적으로 줄이 갈립니다.**
- 미러쌍이 있는 방법론 문서 **58종**
- 그중 **en/ko 줄 수가 다른 쌍 54종 = 93 %**
  (예: `core-state-methodology.md` en 193행 / ko 186행)

**확장 비용: 낮음(2건) 이지만 규칙 결정이 필요합니다.** 세 길 — ⓐ ko 문서 안의 인용은 항상 `ko/` 를
경로에 명시, ⓑ ko 문서 안에서는 줄번호를 쓰지 않고 앵커만(한글 문장이 앵커가 됨), ⓒ 미러 인용을
en 원본으로 강제. **결정 필요.**

## ③ `phase4/**` 보드 — **35건, 썩은 것 1**

citer 는 세 파일뿐이고 **전부 감사/표준 문서**입니다 — 보드 본문(`phase4/*.yaml`)은 줄번호 인용을
쓰지 않습니다.

| citer | 건수 |
|---|---|
| `phase4/_audit/emit-readiness-review.md` | **28** |
| `phase4/_audit/consistency-audit-FINDINGS.md` | 4 |
| `phase4/field-standard/FINDINGS.md` | 3 |

가리키는 대상: `alpha_centauri.yaml` 9 · `40_eridani.yaml` 6 · `proxima_cen.yaml` 3 ·
`fomalhaut.yaml` 3 · `barnards_star.yaml` 2 · `tau_cet.yaml` 1 · 나머지는 스크립트·문서 각 1.

| 이미 썩은 것 | 착지 |
|---|---|
| `phase4/_audit/emit-readiness-review.md:130` → `tau_cet.yaml:24` | **빈줄** |

⚠ **경로 모호 1건**: `fomalhaut.yaml` 은 레포에 두 곳(`docs/phase3/_bib/fomalhaut.yaml`,
`phase4/fomalhaut.yaml`)이라 basename 만으로는 갈립니다.

**확장 비용: 중간.** 35건이고 대부분 정확하지만 **보드는 계속 갱신되는 파일**이라 앞으로 썩을
확률이 방법론 문서보다 높습니다(제 배치 A 의 `phase4/alpha_centauri.yaml` 두 건이 이미 그 증거).
그리고 이 세 문서는 **감사 기록**이라 배치 A #2 와 같은 "과거 상태의 기록" 부류가 섞여 있을 수
있습니다 — 앵커화 전에 그 구분이 필요합니다. **결정 필요.**

## 세 범위 종합

| 범위 | 건수 | 이미 썩음 | 확장 비용 | 결정 필요 |
|---|---|---|---|---|
| ① docs/reference 본문끼리 | **2** | 0 | 거의 0 | 없음 — 넣으면 그냥 통과 |
| ② ko 미러 | **2** | **1** (ko 기준으로 읽으면) | 낮음 | **예** — en/ko 해석 규칙 |
| ③ phase4 보드 | **35** | 1 | 중간 | **예** — 감사기록/살아있는인용 구분 |
| (합) | **39** | 2 | | |

⚠ **한 가지 더 — 오늘 SCAN 안에 있었지만 성질이 같은 것**: `docs/phase3/**` 의 per-host 보고서와
`phase3/stability-sim/**` 은 이미 체커가 봅니다(배치 B 에 `validation-manifest.yaml`·
`hypotheticals/alpha_centauri.json` 이 들어 있습니다). 즉 세 범위를 넣으면 **레포의 인용은
사실상 전부 게이트 아래**로 들어옵니다.
