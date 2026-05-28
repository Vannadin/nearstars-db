# NearStars Tier 1 재시작 — 세션 시작 프롬프트

(다음 Claude Code 세션 첫 메시지로 붙여넣기용)

---

## 컨텍스트

NearStars repo 의 2026-05-28 Tier 1 작업 27 commit 이 citation 무결성 문제로 통째 revert 됨 (commit `a2ef49c`). 그 후 안전한 인프라 9 commit (Tier A) 만 선별 cherry-pick + build refresh 로 복구 (`a2ef49c..34ca024`). 현재 main HEAD = `34ca024`. 큐레이션 데이터 (Phase 2 + Phase 3) 는 여전히 `3ac7f55` 상태와 동일하지만, 빌드 파이프라인 / 스키마 / `_naming.py` / freshness gate / index UX 는 모두 살아 있음. 강화된 procedure 로 큐레이션만 처음부터 다시 시작.

## 먼저 읽어야 할 파일

1. **`phase2/2026-05-28-tier1-postmortem.md`** (repo 안, untracked) — 어제의 6 가지 실패 패턴 + 검증된 진짜 인용 + 다음 시도 권장 사항 전부 보존
2. `CLAUDE.md` — 기본 행동 규칙
3. `MEMORY.md` 와 관련 메모리 파일들

## 강화된 큐레이션 procedure (postmortem 의 7 권장사항)

어제 실패한 6 패턴 (citation fabrication / secondary-source misattribution / false-negative interferometry / multi-layer drift / Phase 2→3 desync / uncertainty drift) 을 막기 위해.

1. **Pre-curation lit search.** 호스트마다 첫 단계로 `"<host>" interferometry OR angular diameter` 검색. "없음" 결과는 explicit verify — 침묵을 "없음" 으로 해석 금지. HD 69830 + Delta Pav 가 이걸 안 해서 false-negative.
2. **Citation value-check.** 모든 `recommended:true` entry 의 값이 인용한 논문 abstract / Table 1 에 실제로 나오는지 확인. paraphrase / downstream citation 거부. Tanner 2015 의 Teff 5402 K 가 사실은 Adibekyan 2012 의 것이었음.
3. **Crossref DOI + 논문 본문 verify.** bibcode 형식 체크만으로는 부족. 적어도 abstract 까지 fetch 해서 저자 + 연도 + 주제 일치 확인. 어제 5 개 fabricated bibcode 가 형식은 통과했지만 논문이 안 맞았음.
4. **Multi-layer commit discipline.** Citation 수정 시 DB structured field (method/bibcode/doi) + meta_notes prose + Phase 3 narrative + bibliography section 을 **같은 commit 에 같이 수정**. "minimal" scope 가 multi-layer 모순 만드는 패턴.
5. **Phase 2 → Phase 3 reconciliation pass.** Phase 2 가 업데이트되면 Phase 3 markdown Decisions table 의 모든 행을 sweep 해서 새 recommended 추적하는지 검증.
6. **Delta Pav 템플릿 재작성.** 어제의 `4d26495` Delta Pav entry 는 false-negative interferometry 인식 모델을 가짐 (Rains 2020 VLTI/PIONIER 측정 무시). 새 시작은 Rains 2020 anchor 위에서.
7. **호스트별 검증 에이전트.** 큐레이션 직후 자동으로 verification subagent 가 인용 chain spot-check 하는 패턴.

## 검증된 정확한 인용 (postmortem 에서 가져옴, fabrication 반복 방지용)

| 호스트 | Primary anchor | 값 |
|---|---|---|
| HD 69830 | Tanner et al. 2015 `2015ApJ...800..115T` (CHARA Classic, arXiv:1412.5251) | θ_LD = 0.674 ± 0.014 mas (H-band) → R = 0.9058 ± 0.019 R☉. Teff 5394 ± 62 K (CHARA+SED) 또는 5385 ± 44 K (SME). age 10.6 ± 4 Gyr (isochrone) 또는 7.5 ± 3 Gyr (SME). mass 0.863 ± 0.043 M☉. [Fe/H] −0.04 ± 0.03 |
| Delta Pavonis | Rains et al. 2020 `2020MNRAS.493.2377R` (VLTI/PIONIER) | θ_LD = 1.828 ± 0.025 mas → R = 1.197 ± 0.016 R☉. Teff 5571 ± 48 K. δ Pav 는 그 paper sample 의 #11/16 |
| Barnard's star | Boyajian et al. 2012 `2012ApJ...757..112B` (CHARA) | R = 0.1867 ± 0.0012 R☉. 어제 Rains 2021 으로 misattributed 됐었음 (값은 정확) |
| 61 Vir | Rathsam et al. 2023 `2023MNRAS.525.4642R` Table A1 row HD 115617 / HIP 64924 | mass 0.93 ± 0.01, Teff 5568 ± 6 K, [Fe/H] +0.006 ± 0.004, age 5.50 +0.78/-0.74 Gyr. (어제 age 가 7.70 Gyr 로 fabricated 됐었음) |
| AU Mic [Fe/H] | Miles & Shkolnik 2017 `2017AJ....154...67M` (HAZMAT II) | β Pic MG mean +0.12 ± 0.05. (어제 Shkolnik 2017 ApJ 838 87 로 misattributed) |
| AU Mic radius | Donati et al. 2023 `2023MNRAS.525.2015D` (page 2015-2039) | (어제 page `..455` 로 typo) |
| AU Mic mass | Wittrock et al. 2023 `2023AJ....166..232W` DOI `10.3847/1538-3881/acfda8` | (어제 DOI `acfda7` 로 typo) |
| eps Eri | Baines & Armstrong 2012 `2012ApJ...744..138B` (`2012ApJ...761...57B` 는 HR 8799 논문) | R/Teff/L self-consistent. mass 0.82 ± 0.02 (Llop-Sayson 2021 의 re-quoted Baines & Armstrong 값) |

eps Eri / AU Mic / Vega / Fomalhaut 의 나머지 카테고리 — 처음부터 lit search.

## Tier 진척 (audit 표 기준)

| Tier | 내용 | 상태 |
|---|---|---|
| Tier 1 | Phase 3 ← Phase 1 stellar 워크플로우 역전 (7 호스트) | **0/7**. 어제 작업 전부 revert. Delta Pav 도 다시. (40 Eri A 까지 묶으면 0/8) |
| Tier 2 | Phase 2 카테고리 누락 (TRAPPIST-1 + 40 Eri B/C) | **사실상 완료** (2026-05-29 워밍업 12c1355 + 119114a). Deferred 후속: 40 Eri C [Fe/H] entry 추가, Cifuentes 2020 L VizieR verify, Kemmer/Suarez Mascareno P_rot follow-up. |
| Tier 3 | 40 Eri Phase 3 (40 Eri A Phase 2 prerequisite) | ⏸ 미시작. `phase2/40_eridani/` 작업 폴더 보존됨. 사용자 결정: "3 > 2 > 1 순" 으로 Tier 1 끝낸 후 마지막. |
| Tier 4 | TRAPPIST-1 planet schema Phase 1→2 | **부분 완료** — TRAPPIST-1 7 행성 `physical` block 은 2026-05-20 작업으로 이미 array form (3 entries each: Gillon 2017 + Grimm 2018 + Agol 2021). `orbital` 만 의도적 Phase 1 single dict (Agol 2021 canonical, paper-to-paper variation <5%). full array 화는 우선순위 낮음. |
| Tier 5 | controversial 행성 정리 | **사실상 종료**. Proxima c / tau Cet b/c/d 는 NASA Archive 정렬로 처리됨. HD 26965 b 만 refuted markdown 작성 여부 보류 — 사용자가 "안 만들 듯, 나중에" 결정. |

## 작업 폴더 보존 상태 (untracked, 검토 필요)

- `phase2/40_eridani/` — Tier 3 prep (어제 작성, 미체크 checklist)
- `phase2/barnards_star/` — 어제 commit workspace (작업은 revert 됨)
- `phase2/tau_cet/` — 어제 commit workspace
- `phase2/teegardens_star/` — 어제 commit workspace
- `phase2/disks-meta-migration/` — 어제 완료된 마이그레이션 workspace
- `phase3/barnards_star/_tag_categories.py` + `phase3/teegardens_star/_tag_triage.py` — 일회용 스크립트

이 중 어느 것을 다음 작업에 쓰고, 어느 것을 지울지 정해야 함. 어제 큐레이션이 오염됐기 때문에 측정값 fabrication 이 작업 폴더에도 묻어 있을 수 있음.

## 첫 결정 (사용자가 답하기)

어디서부터 시작할지.
- (a) Tier 2 (TRAPPIST-1 activity + 40 Eri B/C 카테고리 채우기) — 작고 mechanical, 새 procedure 워밍업
- (b) Delta Pav 재작성 (Rains 2020 anchor 로 처음부터) — Tier 1 새 템플릿 만들고 거기서 6 호스트 확장
- (c) Tier 3 (40 Eri Phase 2 A + Phase 3) — 작업 폴더 이미 준비됨
- (d) 작업 폴더 정리부터 — untracked 작업 트리 평가 후 결정
- (e) 다른 거

## 안 할 것 (어제의 함정)

- 6 호스트 병렬 worktree 에이전트 batch — Delta Pav 템플릿이 오염됐을 때 6 곳에 같은 결함 복제. 새 템플릿 검증 끝나기 전까지 병렬화 금지
- "minimal" scope citation fix — multi-layer commit discipline 의무
- 인용된 논문 본문 확인 없이 bibcode 만 보고 통과
- meta_notes 의 "no interferometry exists" 류 부정 단언 — explicit lit search 결과 인용 필수
