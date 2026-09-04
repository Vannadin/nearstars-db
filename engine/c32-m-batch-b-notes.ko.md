<!-- 병렬석 조사 기록 (원문 무편집). C33 batch M-B: the anchor phrase for every remaining target, each verified to occur once. -->
<!-- Preserved verbatim from the parallel seat's scratch on 2026-09-05. C33 batch M-B: the anchor phrase for every remaining target, each verified to occur once. -->
# M 배치 B — 남은 미이행 전건 앵커표 (HEAD db1b1fd0)
Parallel seat, 2026-09-05. 읽기 전용, 레포 쓰기 없음. 게이트 안 돌렸습니다.
앵커는 전부 **체커의 접기 규칙을 흉내내어**(`\n[ \t]*` → 공백 하나) `n=1` 을 검증했습니다.
⚠ 앵커에 **앞쪽 들여쓰기를 넣지 않았습니다.**

체커 헤더(현재): 앵커 359 · 문서전체 7 · 레포밖 11 · 보존노트 130 · 인용문안인용 5 · **미이행 34**.
`--list` 의 `[미이행]` 행은 45 줄이고(같은 값이 여러 citer 에서 쓰임), 고유 (citer, ref) 는 45,
고유 **타깃** 은 아래 27 개입니다.

## A. 정정 없이 앵커화만 — **23건** (착지가 이미 그 파일에서 고유)

| 타깃 | 쓰는 citer | 앵커 구절 (`n=1` 검증) |
|---|---|---|
| `engine/rheology.py:47` | `SESSION-HANDOFF.md:138` · `property-consumer-audit-context-notes.md:172` | `"Mantle solidus viscosity" 1·10¹⁶ Pa·s and "Activation energy" 300 kJ/mol, footnote 4 =` |
| `engine/rheology.py:90-101` | `property-consumer-audit-context-notes.md:33` | `"unobtained Karato & Wu 1993; the temperature is the top of the convecting adiabat "` |
| `engine/radiogenic.py:183` | `tidal-heating-context-notes.md:36`·`:60`·`:92` | `ζ 상단은 모듈 선언 {mantle_flux.ZETA_RANGE[1]:.3f} (Table 2 의 ±0.5) 이고 논문이` |
| `engine/eos.py:2073` | `figure-relaxation-context-notes.md:34` | `"그 수가 그림에만 산다(인쇄 표는 100 GPa 까지). 규산염 EOS 사다리는 "` |
| `engine/eos.py:2449` | `superionic-ceiling-context-notes.md:124` | `얼음 기둥의 온도 {t_k:.0f} K 가 '{phase}' 적합의 상한` |
| `engine/interior.py:2099` | `SESSION-HANDOFF.md:630` | `"brown_dwarf": ("중수소가 탄다. 13 M_J 위는 광도가 시간에 따라 변하고 "` |
| `engine/interior.py:82` | `SESSION-HANDOFF.md:854` | `"iron":       (1.000, 0.00, 0.00, "fe_eps"),` |
| `engine/cmb_flux.py:166` | `class-defaults-context-notes.md:38` | `grade="analog", inputs=inputs, values=values, units=units, refs=REFS, notes=notes)` |
| `engine/core_energy.py:289` | `class-defaults-context-notes.md:38` | 같은 문장(다른 파일이라 각자 `n=1`) |
| `engine/dynamo_rocky.py:263` | `interior-dynamo-handoff-context-notes.md:26` | `(다극자면 {values['b_eq_multipolar_min']:.3g}–{values['b_eq_multipolar_max']:.3g} µT).` |
| `engine/dynamo.py:257` | `interior-dynamo-handoff-context-notes.md:29` | `radius_rj=state["radius_rj"], age_gyr=state["age_gyr"],` (두 줄 접힘) |
| `engine/test_interior.py:455` | `surveys-2026-08-31-context-notes.md:24` | `# 시험압이 버려질 자리에서 깨지는 결함에 걸렸다. 그 대비가 이 행의 내용이다.` |
| `engine/tools/make_hhe_table.py:113` | `interior-core.md:964` | `"# 외피가 닿지 않고, 배포 표의 결함(밀도 자리의 sentinel 7칸, 0.1/0.5 로 눌린 grad_ad)이",` ⚠ **경로도 고쳐야 합니다** — citer 는 `make_hhe_table.py` 로 적는데 실제 경로는 `engine/tools/make_hhe_table.py` (배치 A 의 `backflow-checklist.md:73` 와 같은 부류) |
| `docs/reference/core-state-methodology.md:60` | `cmb_flux.py:148` · `cmb-heat-flux-context-notes.md:170` | `using a similar method to ours". The core-side value on Earth is 3760 ± 290 K.` |
| `docs/reference/internal-heat-luminosity-methodology.md:34` | `radiogenic.py:278` | `here folds in only the non-tidal sources (add the tidal flux into \`T_int\` if it is` |
| `phase3/stability-sim/validation-manifest.yaml:55` | `bindings.yaml:427` | `args: ["--acen-a-au", "1.6", "--acen-e", "0.1", "--acen-incl-deg", "16"]` |
| `phase3/stability-sim/validation-manifest.yaml:58` | `bindings.yaml:412` · `backflow-checklist.md:14` | `args: ["--j2", "0.023", "--j2-obliquity-deg", "5"]` |
| `phase3/stability-sim/hypotheticals/alpha_centauri.json:33` | `bodies/pandora.yaml:29` | `"semi_major_axis_km": 252393,` |
| `phase4/luhman_16.yaml:80` | `interior-core.md:2196` | `- { name: age, value: 0.5, unit: Gyr, op: passthrough, note: "Phase 3 resolved: Oceanus moving group` |
| `scripts/pipeline/build_systems.py:307-313` | `validate.py:187` | `"ra_deg":      bary["ra_deg"], "dec_deg":     bary["dec_deg"],` (두 줄 접힘) |
| `docs/reference/planetary-dynamo-scaling.md:18` | `chain.yaml:661` | `## Contract — \`dynamo_giant\`` ⚠ 이미 "의도적 계약 착지"로 판정한 건(배치 I-2). 계약 **제목**을 쓰면 주인 일치 규칙과도 맞습니다 |
| `docs/reference/body-figure-methodology.md:238` | `chain.yaml:74` | `\| **α Cen A** \| star (G2V) \| P_rot 22 d \| 4.6e-5 \| **4.8e-7** \| – \|` ⚠ `chain.yaml:74` 는 **주석**입니다(ref 필드가 아님) — 이행 대상인지 지휘석 확인 필요 |

## B. 착지가 그 파일에서 반복돼 두 줄을 묶은 것 — **4건**

| 타깃 | dup | 앵커 (두 줄 접힘, `n=1`) |
|---|---|---|
| `engine/eos.py:509` (`#` 한 글자, **파일 안 114회**) | 114 | `#   * 이성분 — "deviations of the linear mixing approximation from the results of the real` — 즉 **다음 줄**을 앵커로. citer: `coverage-review.md:130` · `interior-core.md:819` |
| `engine/interior.py:3161` (`RECIPE, VERSION,`, **45회**) | 45 | `"3층 역산에는 포텐셜 온도 선언이 있어야 한다. 바다의 자리를 정하는 것이 녹는곡선에 "` — 다음 줄. citer: `property-consumer-audit-context-notes.md:34`·`:115` |
| `phase4/luhman_16.yaml:133` (`refs: [...]`, 2회) | 2 | `조건부이며, ~8시간이면 명목 각도가 더 올라가지만 구간 안에 머문다. refs: ["docs/reference/spin-axis-inclination-methodology.md", "2021ApJ...906...64A"]` — 앞줄+그 줄. citer: `interior-core.md:2199` |
| `phase4/alpha_centauri.yaml:1524–1607` (`axis: bulk.tidal_heating`, 2회 — Dante·Hades) | 2 | `- body: Dante                    # A b I axis: bulk.tidal_heating` — 앞줄+그 줄. citer: `tidal-heating-context-notes.md:79` |

## C. 범위 인용 — **1건**

| 타깃 | 읽기 | 앵커 |
|---|---|---|
| `engine/dynamo.py:122–135` (citer `giant-dynamo-age-context-notes.md:18`) | `:122` 는 거절 메시지, `:135` 는 `width = (b_hi - b_lo) / b` — 둘 다 **한 함수 안**(`_bd_field`, `:90` 시작)입니다. 즉 "이 함수" 를 뜻합니다 | `def _bd_field(mass_mj, radius_rj, radius_rj_min, radius_rj_max, luminosity_lsun,` (`n=1`) |

## D. **결정 필요** — 억지로 고르지 않은 것

### D-1. `main.tex` × **11건** → 오너 결정
`radiogenic.py:16`·`:55`·`:64` · `field_tooltips.py:178`·`:179` ·
`radiogenic-budget-context-notes.md:24`·`:35`·`:40`·`:180` · `radiogenic-context-notes.md:104` ·
`core-thermal-history-context-notes.md:311`.

**Nimmo & Primack 2020 의 미발표 LaTeX 초안**이라 레포에 없고 앵커를 걸 수 없습니다.
**왜 갈리는가**: 세 길이 다 정당해 보입니다 —
① 체커의 "레포 밖 인용" 통으로 옮기고 그대로 둔다(현상 유지, 검증 불가를 인정),
② 파일명 앞에 식별자를 붙여 사람이 찾을 수 있게 한다 —
`Nimmo & Primack 2020 (unpublished draft) main.tex:494-499`,
③ 그 초안을 `docs/phase3/_papers/` 에 provenance 와 함께 캐시하고 그때 앵커화한다.
**②는 값싸고 ③은 검증 가능해집니다.** 어느 쪽이든 **오너 판단**이라 이름만 붙입니다.

### D-2. 출하 문자열 안의 줄번호 — `radiogenic.py:249-251` → 오너 결정
배치 A 에서 보고한 건입니다. `HEAD_PIPE_FLOOR` 가 사용자에게 나가는 verdict 인데
`radiogenic.py _total_heat:265-267` 을 담고 있고, 실제 가드는 `:268-270` 입니다.
**갈리는 이유**: 줄번호를 떼면(`radiogenic.py _total_heat`) 다시 썩지 않지만 정밀도가 줄고,
유지하면 리팩터마다 썩습니다. **출하 문자열의 정밀도 정책**이라 오너 몫입니다.

### D-3. `chain.yaml:74` — 이행 대상인지 확인 필요
그 줄은 `ref:` 필드가 아니라 **노드 정의 위의 한글 주석**입니다
(`# (:body-figure-methodology.md:238, α Cen A P_rot 22 d 측정 경로)이 "오배선" 으로 분류됐다가`).
주석 안의 인용도 이행 대상인지, 아니면 "인용문 안 인용"처럼 INFO 로 낮출지 **규칙 결정**이 필요합니다.

## E. 실측 하나 — 앵커에 들여쓰기를 넣으면 정말 0
확인: `engine/interior.py:82` 의 원문은 `    "iron":       (1.000, ...` 로 4칸 들여쓰기입니다.
접힘 규칙이 `\n[ \t]*` 를 공백 하나로 바꾸므로, **앵커를 `    "iron":` 로 시작하면 매치 0**,
`"iron":` 로 시작하면 `n=1` 입니다. 위 표의 앵커는 전부 앞 공백을 뺀 형태입니다.
