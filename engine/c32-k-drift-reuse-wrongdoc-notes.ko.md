<!-- 병렬석 조사 기록 (원문 무편집). C33 batch K: blame-delta drift, the reuse distribution, and the two refs that named the wrong document. -->
<!-- Preserved verbatim from the parallel seat's scratch on 2026-09-05, so it stays Korean and keeps its
     numbers, quotations and tables exactly as measured; the .ko.md name declares that (check_language.py).
     C33 batch K: blame-delta drift, the reuse distribution, and the two refs that named the wrong document. -->
# K — 드리프트 정정표 · 재사용 27건 · 엉뚱한 문서 축
Parallel seat, 2026-09-05. HEAD **6654d314**, 읽기 전용, 레포 쓰기 없음.
⚠ 작업석이 지금 `engine/chain.yaml`·`engine/radiogenic.py`·`engine/via-context-notes.md` 를 미커밋으로
들고 있습니다. 아래 다섯 건(`508`·`618`·`658`·`664`·`679`)은 blame 이 `00000000`(미커밋)으로 나와
저작 커밋을 되짚을 수 없었고, 그 다섯은 제 배치 I 결과로 답을 씁니다.

## ⚠ 방법 정정 — `--ignore-revs-file` 이 이 목적에는 역효과입니다

지휘석 제안대로 `0ace3863`·`b29b556e`·`25980fdc` 를 ignore 하고 돌렸더니 **Δ≠0 이 31~32건** 나왔는데,
그중 **tidal 문서의 Δ+18 열두 건이 전부 거짓 양성**이었습니다. 이유가 구조적입니다 —
**`0ace3863` 은 바로 그 +18 을 이미 적용해 준 커밋**입니다. 그것을 ignore 하면 blame 이 그 이전
저자로 돌아가고, Δ 가 **이미 반영된 이동을 다시 더합니다**. 검증: `chain:617` 의 `tidal:79` 는 오늘
`Ė ∝ (k₂/Q)·R⁵·e²·M_p^(3/2)·a^(−15/2)` 를 정확히 가리키는데(제가 H 에서 확정한 그 자리),
ignore 판에서는 "정답이 `:97`" 이라고 나옵니다. `:97` 은 엉뚱한 줄입니다.

**두 목적이 충돌합니다.** ignore-revs 는 "누가 **의도**를 저작했나"를 찾는 데 맞고, Δ 는 "그 **숫자**가
마지막으로 쓰인 뒤 문서가 얼마나 자랐나"를 재야 합니다. 리프레시 커밋은 숫자를 **고쳐 준** 커밋이라
Δ 의 기준점으로는 **포함**되어야 합니다.

**그래서 K-1 은 평범한 `git blame`(ignore 없음)으로 다시 돌렸습니다 → Δ≠0 = 16건 (고유 15).**
델타 분포 `{1:6, 24:3, 36:1, 43:1, 47:2, 53:2, 79:1}`. tidal 문서의 Δ+18 열두 건은 사라졌습니다 —
이미 고쳐져 있기 때문입니다.

## K-1. 드리프트 정정표 (16건)

각 건마다 blame 커밋의 문서 그 줄(= 저작 시점 의도)을 꺼내고, 그 원문을 오늘 문서에서 축자로 찾았습니다.
앵커는 그 원문 구절이며 전부 오늘 문서에서 한 줄에만 나옵니다.

| chain | 간선 | 현재 ref | Δ | **정답** | 앵커 구절 | § |
|---|---|---|---|---|---|---|
| `509` | `star_physical → mass_radius_relation via insolation` | mass-radius:191 | +47 | **238** | `Practical rule: **physical grid (Zeng) when the body is confidently rocky;` | `## 4. The Relation Is a Band, Not a Line` |
| `510` | `mass_radius_relation → mass_radius_relation via insolation` | mass-radius:107 | +43 | **150** | `envelopes and includes the stellar-irradiation dependence (insolation puffs up a` | `## 2. The Composition Grids: the Physical M–R Curves` |
| `535` | `mass_radius_relation → interior_layers` | rocky-planet-dynamo:187 | +79 | **266** | `supplies the M ↔ R ↔ density tie-break that seeds the internal-structure step.` | `## Related` |
| `538` | `mass_radius_relation → surface_albedo` | mass-radius:221 | +47 | **268** | `allowed up here; a larger radius **forces a volatile (H/He or steam) envelope**,` | `## 5. The Radius-Valley Classification Gate` |
| `539` | `mass_radius_relation → surface_albedo` | mass-radius:368 | +53 | **421** | `- [surface-color-albedo-methodology](surface-color-albedo-methodology.md): the rocky-vs-volatile` | `## Related` |
| `663` | `body_class → dynamo_rocky via l_int` | scaling:33 | +24 | **57** | `dwarfs, young exoplanets, and giants not tidally locked very close to their star.` | `## The law` |
| `684` · `685` | `tidal_locking → dynamo_rocky via rossby` (gap) · `composition_intent → dynamo_rocky via layer_fractions` | rocky-planet-dynamo:69 ×2 | +1 | **70** | `2. **Regime gate (local Rossby number)** — \`Ro_ℓ < 0.12\` → **dipolar** (strong,` | `## The law` |
| `686` | `body_age → dynamo_rocky` | rocky-planet-dynamo:27 | +1 | **28** | `low-density dry), from mass, radius and the declared ice fraction; the alive gate, which is three labels` | `## Contract — \`dynamo_rocky\`` |
| `687` | `heat_transport_mode → dynamo_rocky via cmb_heat_flux` (gap) | rocky-planet-dynamo:28 | +1 | **29** | `(\`conductor_phase\` from \`core_state\`, the declared \`stagnant_lid\`, the declared per-class death age) and` | `## Contract — \`dynamo_rocky\`` |
| `727` | `interior_layers → core_state via core_pressure` | rocky-planet-dynamo:183 | +1 | **184** | `C14-solved T_c falls ~90 K; the C15 entropy band moves (−69 → −68 → −82 MW/K) but still straddles zero, so the` | `## Domain of validity: regimes by body class` |
| `508` | `composition_intent → mass_radius_relation` | mass-radius:62 | +36 | **98** | `So for almost every curated body we have one of {M, R} and must **assign the` | `## 1. Why One of M, R Is Almost Always Missing` |
| `618` | `tidal_heating → mass_radius_relation via radius_ceiling` (gap) | mass-radius:371 | +53 | **424** | `- [tidal-heating-methodology](tidal-heating-methodology.md): the tidal-heating rate goes as` | `## Related` |
| `658` | `body_age → dynamo_giant via t_body` | scaling:29 | +24 | **53** | `B_dyn  =  4.8 · (M · L² / R⁷)^(1/6)   [kG]` | `## The law` |
| `664` · `669` | `body_class → dynamo_rocky` ×2 | scaling:97 ×2 | +24 | **121** | `4. **Rocky planets**: the giant dynamo law does **not** apply. Use the rocky` | `## Domain of validity: three regimes` |
| `679` | `core_state → dynamo_rocky via conductor_phase` | rocky-planet-dynamo:258 | +1 | **259** | `- [\`interior-structure-methodology.md\`](interior-structure-methodology.md): supplies the core radius` | `## Related` |

⚠ **`686`·`687`·`727` 세 건은 Δ+1 인데 성질이 다릅니다** — 지금 가리키는 줄과 정답 줄이 **같은 문단의
연속된 두 줄**입니다(계약 블록의 Discriminating-keys 가 세 줄로 이어지는 자리, 그리고 §Domain 의
측정 문단). 인용의 뜻은 사실상 같으므로 **긴급도가 낮습니다**. 다만 앵커로 옮기면 이 애매함 자체가
사라집니다.

⚠ **`535`·`539`·`618`·`679` 는 링크목록(`## Related`) 항목**입니다 — 배치 I 의 ③(항목 링크 텍스트를
앵커로) 권고가 그대로 적용됩니다. 위 표의 앵커가 이미 그 형태입니다.

## K-2. 재사용되는 값 — HEAD 6654d314 에서 **15개 값 / 34건**

지휘석 실측(12개/27건)과 다릅니다 — HEAD 가 그 사이 움직였습니다(`6654d314`).

| ×4 | `core-state-methodology.md:1` |
| ×3 | `body-figure-methodology.md:256` · `interior-structure-methodology.md:1` |
| ×2 | `body-figure:238` · `tidal-heating:212` · `cassini-state:166` · `tidally-locked-temperature:117` · `scaling:18` · `scaling:97` · `rocky-planet-dynamo:24` · `rocky-planet-dynamo:69` · `planetary-magnetosphere-geometry:4` · `surface-radiation-dose:45` · `exoplanet-atmosphere:66` · `moon-energy-budget:132` |

### `:1` 일곱 건 — **인용이 아니라 "이 문서 전체" 관용입니다. 파일명만 남기기를 권고합니다.**

두 문서의 첫 줄은 **한글 HTML 주석 헤더**입니다(§6 파일-헤더 규약).

| 문서 | `:1` 의 실제 내용 |
|---|---|
| `core-state-methodology.md` | `<!-- 핵이 다이나모를 돌릴 수 있는 액체인가 — 핵의 압력·온도를 철의 융해곡선에 대는 방법(논문 근거) -->` |
| `interior-structure-methodology.md` | `<!-- 질량과 조성에서 정수압 평형을 적분해 반지름·핵 경계·관성모멘트·중심압을 내는 방법(논문 근거) — J₂·다이나모·핵 상태의 입력 -->` |

즉 `:1` 은 **문서를 한 줄로 요약한 헤더**이고, 특정 주장을 짚는 인용이 아닙니다. 쓰는 간선도 그
읽기와 맞습니다 —

| chain | 간선 | ref |
|---|---|---|
| `730`·`731` | `interior_layers → core_state` ×2 | `core-state-methodology.md:1` |
| `736`·`737` | `body_class → core_state` ×2 | `core-state-methodology.md:1` |
| `695` | `internal_heat_nontidal → interior_layers` | `interior-structure-methodology.md:1` |
| `728`·`729` | `interior_layers → core_state` ×2 | `interior-structure-methodology.md:1` |

일곱 건 모두 **소비 노드의 소관 문서를 통째로 가리키는** 형태입니다(`core_state` ↔ core-state 문서,
`interior_layers` ↔ interior-structure 문서). **권고: `ref: "<doc>.md"` — 파일명만.** 줄번호를 유지하면
헤더 한 줄을 가리키는 인용이 되어 뜻이 좁아지고, 앵커로 옮기면 한글 주석을 앵커 문자열로 박아야 해서
더 나쁩니다. ⚠ 남는 위험은 "문서 전체" 라는 뜻이 **간선의 payload 를 특정하지 못한다**는 것인데,
그건 `via:` 가 이미 하고 있습니다.

### 나머지 8개 값(×2·×3) — 상속 위험 판정
`scaling:18`·`scaling:97`·`rocky-planet-dynamo:24`·`rocky-planet-dynamo:69`는 이미 배치 I/K-1 에서
다뤘습니다(전자 둘은 계약 주인 일치로 **정상**, 후자 둘은 K-1 정정 대상). 남은 넷
(`body-figure:256` ×3 · `cassini-state:166` · `planetary-magnetosphere-geometry:4` ·
`surface-radiation-dose:45` · `exoplanet-atmosphere:66` · `moon-energy-budget:132` · `tidal-heating:212` ·
`body-figure:238`)은 **Δ=0** 이라 저작 시점 자리에 그대로 있습니다. ⚠ 다만
`planetary-magnetosphere-geometry:4` 는 제가 앞선 자기권 조사에서 이미 지적한 자리입니다 — 그 줄은
"b_eq 의 출처를 말하는 산문 문장"이고 **식이 아닙니다**(그 문서의 식은 `:80`). 재사용 ×2 이고
**출생부터 조준이 느슨한** 부류라, K-1 의 드리프트와는 다른 종류로 남깁니다.

## K-3. 엉뚱한 문서 축 — **7건**

노드→소관문서는 `chain.yaml` 의 `recipe:` 키에서 뽑았습니다(`recipe` 가 없는 노드는 판정 불가로 제외).
단일행 간선 중 **양 끝점이 모두 recipe 를 가진 87건**을 검사해, ref 문서가 **양쪽 어느 소관도 아닌** 것:

| chain | 간선 | ref 문서 | from 소관 | to 소관 | 읽기 |
|---|---|---|---|---|---|
| `535` | `mass_radius_relation → interior_layers` | `rocky-planet-dynamo` | mass-radius | interior-structure | ⚠ K-1 에서 이미 드리프트로 잡힌 건. 정답 줄(`:266`)이 rocky-dynamo 문서의 `## Related` 항목 "supplies the M ↔ R ↔ density tie-break…" 이라 **제3 문서가 두 노드의 결합을 서술하는** 정당한 형태입니다 |
| `609` | `body_figure → crater_state via relief` | `tidal-heating` | body-figure | crater-degradation | 제3 문서. 조석열이 지형 완화를 먹인다는 서술이 tidal 문서에 있어 정당할 수 있습니다 — 다만 그 문서의 `## Related` 항목(`crater-degradation…` 항목)을 가리키는 편이 명확합니다 |
| `620` · `791` · `817` | `cassini_state → tidal_heating` · `tidal_heating → atmospheric_escape` · `tidal_heating → greenhouse` | `moon-energy-budget` ×3 | 각각 다름 | 각각 다름 | **위성 에너지 예산 문서가 세 결합의 공통 허브**입니다. 위성의 4항 예산이 그 세 양을 한자리에서 다루므로 정당한 제3 문서 인용으로 읽힙니다 |
| `664` · `669` | `body_class → dynamo_rocky` ×2 | `planetary-dynamo-scaling` | body-class | rocky-planet-dynamo | ⚠ **여기가 진짜 이상합니다.** 소비처가 `dynamo_rocky` 인데 ref 는 **거대행성** 문서입니다. K-1 의 정답 줄(`scaling:121`)이 `4. **Rocky planets**: the giant dynamo law does **not** apply. Use the rocky` — 즉 "거대행성 문서가 암석으로 넘기는 문장"이라 **인용 자체는 뜻이 있습니다.** 다만 그 뜻이 "이 간선의 근거"는 아니라 **문서를 바꿀 후보**입니다(`rocky-planet-dynamo` 의 대응 문장으로) |

⚠ **검사 범위의 한계를 이름 붙입니다**: 단일행 간선 87건만 봤습니다. `recipe` 가 없는 노드가 한쪽이라도
걸린 **95건**은 판정 불가로 제외했고, 다중행 간선도 제외했습니다. 즉 이 7건은 **하한**입니다.
`recipe` 미등록 7노드(제 이전 보고: `tidal_response`·`xuv_history`·`stellar_wind`·`global_fluid_layer`·
`t_eq_stellar`·`t_eff_body`·`surface_uv`)가 관여한 간선은 이 축으로 판정할 수 없습니다.
