# 2026-05-28 Tier 1 Batch — Postmortem

## TL;DR

오늘 작업한 27 commit (Tier 1 6 호스트 + Delta Pav 템플릿 + 기타) 을 전량 롤백합니다. 두 차례 동일-일 감사 + 사용자 PDF 검증 + 두 개의 후행 검증 에이전트가 단순 citation typo 가 아닌 **체계적 인용 무결성 문제** 를 드러냈고, 패치보다 처음부터 다시 가는 게 안전하다는 판단입니다.

이 문서는 오늘의 시도, 발견된 문제 패턴, 다음 시도를 위한 교훈을 보존합니다.

## 시도한 것

**Tier 1.** "Phase 3 가 Phase 1 stellar 위에 올라간 워크플로우 역전" 해소. 7 호스트 (Delta Pav + eps Eri / AU Mic / HD 69830 / 61 Vir / Vega / Fomalhaut). Delta Pav `4d26495` 가 첫 시범, 나머지 6 호스트가 이번 세션 대상.

**목표.** 호스트별로 `db/stellar_props_curated.json` 에 8/8 measurement category Phase 2 entry 신규 작성 + `docs/phase3/<host>.md` Decisions 행을 Phase 2 picks 로 재정렬 + `ko/docs/phase3/<host>.md` 미러 동시 갱신.

## 어떻게 했나

1. 6 호스트별 worktree 격리 background 에이전트 1 개씩 launch
2. 각자 Delta Pav `4d26495` 를 템플릿으로 읽고 자율 수행
3. 30~60 분씩 걸려 순차 callback → main 으로 cherry-pick 직렬 머지
4. `db/stellar_props_curated.json` append 충돌은 git auto-merge, `docs/data.json` + `reports-manifest.json` 만 `--theirs` 로 받고 끝에 빌드 재실행
5. 동일-일 감사 subagent → 🔴 citation blocker 5 + 🟡 yellow 2 발견
6. `d0a204b fix(citations)` 로 1 차 패치 + 사용자가 Rathsam 2023 PDF 직접 verify → 61 Vir age fabrication (7.70 → 5.50 Gyr) 발견 → 함께 fix
7. push 후 사용자 요청으로 **두 번째 감사** (오늘 27 commit 전체) → 🔴 blocker 2 추가 발견
8. R3/R4 검증 에이전트가 더 깊은 문제 (Tanner 2015 Teff 값 misattribution, Delta Pav VLTI/PIONIER 측정 존재) 노출
9. 이 시점에서 롤백 결정

## 발견된 문제 패턴

### 패턴 1. Citation fabrication

에이전트 (또는 초기 Phase 1 ingest) 가 **존재하지 않는** bibcode / DOI / year 를 생성. 확인된 예.

| 호스트 | DB 에 있던 인용 | 실제 |
|---|---|---|
| HD 69830 | Tanner 2019 `2019ApJ...873...91T` | 존재하지 않음. 실제 = Tanner 2015 `2015ApJ...800..115T` |
| eps Eri | Baines & Armstrong 2012 `2012ApJ...761...57B` | 그 bibcode 는 HR 8799 논문. eps Eri 논문은 `2012ApJ...744..138B` |
| AU Mic | Wittrock 2023 DOI `acfda7` | 한 글자 typo. 실제 = `acfda8` |
| AU Mic | Donati 2023 `2023MNRAS.525..455D` | 페이지 오류. 실제 = `.2015D` |
| AU Mic | Shkolnik 2017 `2017ApJ...838...87S` | DOI 404. 실제 HAZMAT II = Miles & Shkolnik 2017 `2017AJ....154...67M` |
| 61 Vir | Rathsam 2023 age 7.70 +0.28/-0.26 Gyr | Table A1 실제 = 5.50 +0.78/-0.74 Gyr |
| HD 69830 | Tanner 2015 Teff 5402 ± 11 K | 그 값은 Adibekyan 2012 의 것. Tanner 2015 본문은 5394 ± 62 K (CHARA) 또는 5385 ± 44 K (SME) |
| HD 69830 | Tanner 2015 alt-age 10.6 ± 2 Gyr | 실제 = 10.6 ± 4 Gyr (uncertainty 2 → 4) |

### 패턴 2. Secondary source 인용을 primary 로 표기

원본 측정 논문 대신 그 값을 re-quote 한 후속 논문을 인용. `method: interferometry` 라벨이 secondary source 에 붙는 형태.

- **Barnard's star** 반지름 0.1868 ± 0.0011 → Rains et al. 2021 (`2021MNRAS.504.5788R`, "Characterization of 92 **southern** TESS candidate planet hosts and a new photometric [Fe/H] relation") 로 인용. 그러나 Rains 2021 은 광도 [Fe/H] calibration 논문이고 Barnard 미포함 (dec +04°, 남쪽 아님) + 새 interferometry 없음. 진짜 CHARA 소스 = Boyajian et al. 2012 (`2012ApJ...757..112B`, R = 0.1867 ± 0.0012) 이며 이미 같은 array 에 recommended:false 로 있었음.
- **HD 69830** Teff 5402 K → Tanner 2015 가 아니라 Adibekyan 2012 출처.
- **eps Eri** mass 0.82 ± 0.02 → Llop-Sayson 2021 (downstream joint fit) 이 primary. 실제로는 Baines & Armstrong 2011/2012 의 값을 re-quote 한 것.

### 패턴 3. False-negative interferometry 주장

meta_notes 가 "no direct interferometric measurement exists" 라 단언하지만 실제로 존재.

- **HD 69830**. meta_notes: "no direct interferometric angular diameter exists — not included in any CHARA or VLTI-PIONIER programme through 2026". 실제. Tanner 2015 가 정확히 CHARA Classic H-band θ_LD = 0.674 ± 0.014 mas 직접 측정 논문.
- **Delta Pavonis** (Tier 1 템플릿 호스트). 본문: "dec -66° too far south for CHARA; never observed by PAVO@SUSI or VLTI-PIONIER". 실제. **Rains et al. 2020 MNRAS 493** (`2020MNRAS.493.2377R`, "Precision angular diameters for 16 southern stars with VLTI/PIONIER") 가 δ Pav θ_LD = 1.828 ± 0.025 mas 측정. VLTI@Paranal 위도 -24°, SUSI@Narrabri 위도 -30° — 둘 다 dec -66° 관측 가능.
- **이 패턴이 Delta Pav 템플릿 자체에 있다** = 그걸 copy 한 6 개 호스트 전부가 같은 false-negative 인식 모델을 상속.

### 패턴 4. Multi-layer drift

수정이 한 layer 만 들어가서 다른 layer 와 모순. `d0a204b` 의 "minimal fix" 가 정확히 이 패턴.

- meta_notes 의 "no interferometry" 주장은 정정했는데 같은 entry 의 `method: sed_fitting` 은 안 건드림 → 두 필드가 self-contradictory
- Phase 3 markdown narrative 도 옛 주장 그대로 유지

세 layer (meta_notes / structured fields / narrative) 가 따로 노는 구조적 문제.

### 패턴 5. Phase 2 → Phase 3 desync

Phase 2 가 새 paper 로 업데이트되어도 Phase 3 markdown 이 자동 추적하지 않음.

- **tau Cet**. Phase 2 에서 Korolik 2023 (`2023AJ....166..123K`) 이 radius/Teff/rotation 의 recommended:true. 그러나 Phase 3 markdown 은 여전히 Teixeira 2009 / Pavlenko 2012 / Baliunas 1996 인용. documented divergence 없음.

### 패턴 6. Uncertainty drift

논문이 보고한 unc 보다 더 좁거나 넓은 값을 DB 에 기록.

- 61 Vir Rathsam Table A1 의 Teff 가 ±6 K 인데 DB 가 ±4 K (더 좁음)
- mass / [Fe/H] 도 다른 시점에 같은 종류 drift 존재했음 (audit 시점에 ±0.012 / ±0.018 → 현재 ±0.01 / ±0.004 로 정정됨, 어느 commit 에서 정정됐는지 불명)

## 무엇이 작동했나

- **병렬 worktree agent 패턴.** 6 호스트 ~10 분씩 동시. 충돌 해소도 깔끔.
- **Cherry-pick + 직렬 merge.** `db/stellar_props_curated.json` append 충돌 git auto-merge 통과.
- **Block parity check.** en/ko 미러 sync 유지.
- **동일-일 감사 subagent.** Surface-level citation bibcode/DOI 5 개 잡음 (push 전).
- **사용자 PDF 검증.** Web fetch 가 못 잡은 fabrication 발견 (Rathsam Table A1).
- **두 번째 감사 + 검증 에이전트.** Multi-layer drift, false-negative pattern 노출.

## 왜 패치보다 롤백인가

1. **Delta Pav 템플릿 자체가 오염**. 6 호스트가 그걸 copy 했다는 건 false-negative interferometry 인식 모델을 6 곳에 복제했다는 것. 호스트별 패치로 처리하면 surface 만 닦는 셈.
2. **Citation chain verification 이 procedure 에 없었음**. 인용된 논문이 실제로 그 값을 보고하는지 확인하는 step 이 없어서, 감사가 surface citation 만 통과해도 진짜 결합이 남음.
3. **다층 fix discipline 부재**. d0a204b 가 보여준 대로, "minimal" 으로 한 layer 만 고치면 다른 layer 와 contradictory 상태가 됨.
4. **누적 신뢰도 하락**. 27 commit 중 어느 entry 가 정확하고 어느 게 misattribution 인지 호스트별로 다시 verify 해야 함. 그 verify 비용이 처음부터 다시 하는 것보다 안 작음.

## 다음 시도를 위한 권장 사항

1. **Pre-curation lit search.** 호스트마다 `"<host>" interferometry OR angular diameter` 검색을 명시적 step 으로 포함. 침묵을 "없음" 으로 해석하지 말 것.
2. **Citation value-check.** 각 measurement entry 의 value 가 인용한 논문의 abstract / Table 1 에 실제로 나오는지 확인. paraphrase 나 downstream citation 거부.
3. **Audit protocol upgrade.** Crossref DOI 형식 체크 + 논문 본문 verification 까지 모든 `recommended:true` entry 에 의무화.
4. **Multi-layer commit discipline.** Citation 수정 시 DB structured field + meta_notes prose + Phase 3 narrative + bibliography section 을 같은 commit 에 같이 처리.
5. **Delta Pav 템플릿 재작성.** Rains 2020 VLTI/PIONIER 측정 (θ_LD = 1.828 ± 0.025 mas) 을 anchor 로 처음부터 다시. 4d26495 entry 재사용 금지.
6. **Phase 2 → Phase 3 reconciliation pass.** Phase 2 가 업데이트되면 Phase 3 markdown 의 Decisions table 을 다시 sweep 하는 explicit step.
7. **호스트별 검증 에이전트.** 큐레이션 직후 자동으로 verification subagent 가 인용 chain 을 spot-check 하는 패턴 — 이번 R3/R4 검증이 그 valuable 함을 보여줌.

## 검증 에이전트가 확인해준 사실 (롤백 후에도 보존할 가치)

### HD 69830 Tanner et al. 2015 (arXiv:1412.5251)
- 정식 제목. *"Stellar Parameters for HD 69830, a Nearby Star with Three Neptune Mass Planets and an Asteroid Belt"*
- 저자. Tanner, Boyajian, von Braun et al.
- CHARA Classic H-band θ_LD = 0.674 ± 0.014 mas (Table 2)
- 두 Teff 값. 5394 ± 62 K (CHARA + SED Stefan-Boltzmann inversion) / 5385 ± 44 K (SME 분광)
- 두 age 값. 10.6 ± 4 Gyr (isochrone) / 7.5 ± 3 Gyr (SME)
- Mass 0.863 ± 0.043 M☉, Radius 0.9058 ± 0.019 R☉, L 0.622 ± 0.014 L☉, [Fe/H] -0.04 ± 0.03

### Delta Pavonis Rains et al. 2020 (`2020MNRAS.493.2377R`)
- 정식 제목. *"Precision angular diameters for 16 southern stars with VLTI/PIONIER"*
- θ_LD = 1.828 ± 0.025 mas (δ Pav = star #11 of 16)
- 유도 반지름. 1.197 ± 0.016 R☉
- Teff. 5571 ± 48 K
- 이 값들은 Gomes da Silva 2021 PARSEC isochrone (DB 가 anchor 로 쓴 것) 보다 **더 직접적** — 다음 시도에서 Delta Pav 의 새 primary anchor 가 되어야 함.

### Rathsam et al. 2023 (`2023MNRAS.525.4642R`, arXiv:2309.00471)
- 정식 제목. *"Lithium depletion in solar analogs: age and mass effects"*
- Sample. 74 solar twins + 79 from Carlos 2019 = 153 stars
- 61 Vir (HD 115617 / HIP 064924) Table A1 row.
  - Teff 5568 ± 6 K
  - log g 4.390 ± 0.012
  - [Fe/H] 0.006 ± 0.004
  - Mass 0.93 ± 0.01 M☉
  - Age 5.50 +0.78/-0.74 Gyr (DB 의 7.70 Gyr 은 fabrication)

### Barnard 's star Boyajian et al. 2012 (`2012ApJ...757..112B`)
- 정식 CHARA interferometric source.
- R = 0.1867 ± 0.0012 R☉
- DB 가 이 값을 Rains 2021 에 misattribute 했었음 (값은 정확).

## 롤백 세부

- 대상 commit. `3ac7f55 refactor(db): migrate enrichment from db/systems/ to source layer` (2026-05-27 22:29 +0900)
- 되돌릴 commit 수. 27
- 이미 origin 으로 push 됨 — `git push --force` 필요
- Untracked working dirs (`phase2/40_eridani/`, `phase2/barnards_star/`, `phase2/tau_cet/`, `phase2/teegardens_star/`, `phase2/disks-meta-migration/`, `phase3/barnards_star/_tag_categories.py`, `phase3/teegardens_star/_tag_triage.py`) 는 reset --hard 후에도 보존됨 (git 가 untracked 안 건드림)
- 이 postmortem 파일 (`phase2/2026-05-28-tier1-postmortem.md`) 도 untracked 이므로 보존됨

## 메모리 갱신 권장

`/Users/vana/.claude/projects/-Users-vana-Desktop-NearStars/memory/` 에 다음 정보 추가/갱신 권장.
- Delta Pav / HD 69830 / Barnard 의 정확한 interferometric source (다시 fabricate 하지 않도록)
- "오늘 27 commit 롤백" 사실 + 사유 (다음 세션이 같은 작업을 반복하지 않도록)
- Citation value-check + multi-layer fix discipline 이 새 procedure 가 됐다는 사실
