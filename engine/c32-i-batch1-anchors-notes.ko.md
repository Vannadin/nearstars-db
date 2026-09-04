<!-- 병렬석 조사 기록 (원문 무편집). C33 batch I: anchors for the mechanically wrong refs, traced to their introducing commits. -->
<!-- Preserved verbatim from the parallel seat's scratch on 2026-09-05, so it stays Korean and keeps its
     numbers, quotations and tables exactly as measured; the .ko.md name declares that (check_language.py).
     C33 batch I: anchors for the mechanically wrong refs, traced to their introducing commits. -->
# I — 배치 1: 본문이 아닌 곳에 착지하는 ref 전수 (HEAD 5dcf26c3)
Parallel seat, 2026-09-05. 읽기 전용, 레포 쓰기 없음.

## ⚠ 먼저: 발주 시점과 현재 상태가 다릅니다

작업석이 **`internal-heat-luminosity-methodology.md` 을 이미 앵커 형식으로 마이그레이션했습니다** —
`<doc>.md@«앵커 구절»`. 지금 chain.yaml 상태:

| 형식 | 건수 | 문서 수 |
|---|---|---|
| 앵커형 `…md@«…»` | **37** | 1 (heat 문서만) |
| 숫자형 `…md:NNN` | **160** | **21** (heat 문서는 `:34` 하나만 남음) |

**37개 앵커 전부가 문서에서 정확히 1회 매치됩니다**(제가 전수 검증). 그리고 제가 H 에서 제안한 구절이
그대로 쓰였습니다 — `«⇒  T_eff⁴  =  T_eq⁴  +  T_int⁴»` ·`«against Earth's \`T_eq ≈ 255 K\`»` ·
`«Age and mass, not the host»`, 그리고 소비처별 계약 제목 `«## Contract — \`cmb_heat_flux\`»` ×6 ·
`«core_energy_balance»` ×6 · `«core_entropy_production»` ×6 · `«core_thermal_history»` ×8 ·
`«internal_heat_nontidal»` ×3. **지휘석의 개수 정정(6·8)이 반영된 형태이고 제 표의 5·9 가 틀렸습니다.**

⚠ 그래서 **발주에 적힌 60건 중 heat 문서 몫 34건(30+4)은 이미 닫혔습니다.** 남은 것은 아래 **32건**
(고유 (문서,줄) 28개)입니다. 그리고 발주의 크기 수치(190/145/22)는 그 마이그레이션 전 값입니다 —
현재 실측은 **160/141/21(+앵커 37/1)** 입니다.

## 현재 분류 (숫자형 160건)

| 착지 종류 | 건수 |
|---|---|
| 본문(prose) | **128** |
| 표행(table-row) | 11 |
| 링크목록(link-list) | 9 |
| 제목(heading) | 6 |
| 계약 Needs/Returns | 4 |
| 빈줄(blank) | 2 |
| 목차(TOC) | **0** (heat:209 가 앵커로 옮겨감) |

## I-1. 정정이 필요한 것 — **6개** (고유 5)

전부 도입 커밋으로 되짚어 그때의 원문을 꺼내고, 그 원문을 현재 문서에서 축자로 찾았습니다.
`uniq=1` 은 그 구절이 오늘 문서에서 한 줄에만 나온다는 뜻(전부 확인).

| chain | 간선 | 현재 ref | 착지 | **정답 줄** | 앵커 구절 (uniq=1) | § |
|---|---|---|---|---|---|---|
| `618` | `tidal_heating → mass_radius_relation via radius_ceiling` (gap) | `mass-radius-relation:371` | **빈줄** | **424** | `- [tidal-heating-methodology](tidal-heating-methodology.md): the tidal-heating rate goes as` | `## Related` ⚠ |
| `679` | `interior_layers → dynamo_rocky via core_radius` | `rocky-planet-dynamo:258` | **빈줄** | **259** | `- [\`interior-structure-methodology.md\`](interior-structure-methodology.md): supplies the core radius` | `## Related` ⚠ |
| `584` | `body_figure → cassini_state` 계열 | `body-figure:353` | 링크목록(**다른 항목**) | **354** | `- [\`mass-radius-relation-methodology.md\`](mass-radius-relation-methodology.md): the radius input.` | `## Related` ⚠ |
| `508` | `mass_radius_relation` 계열 | `mass-radius-relation:62` | 표 구분선 `\|---\|---\|---\|---\|` | **98** | `So for almost every curated body we have one of {M, R} and must **assign the` | `## 1. Why One of M, R Is Almost Always Missing` |
| `658` | `mass_or_radius → dynamo_giant` | `planetary-dynamo-scaling:29` | 표행(stellar 레짐) | **53** | `B_dyn  =  4.8 · (M · L² / R⁷)^(1/6)   [kG]` | `## The law` |
| `664`·`669` | `body_class → dynamo_rocky` (×2, 하나는 `via: sub_neptune` gap) | `planetary-dynamo-scaling:97` | 표행(검증표 `1 M_J young end`) | **121** | `4. **Rocky planets**: the giant dynamo law does **not** apply. Use the rocky` | `## Domain of validity: three regimes` |

`658`·`664`·`669` 셋은 **드리프트 +24**, `508` 은 **+36**, `618` 은 **+53**, `584`·`679` 는 **+1** —
`0ace3863` 이 tidal/heat 만 손보고 나머지 문서는 손대지 않아 남은 것들입니다.

⚠ `664`·`669` 는 특히 눈에 띕니다 — 지금 가리키는 `1 M_J young end` 검증표 행은 제가 D 에서 "괄호
범위가 기계 검증 밖"이라고 보고한 그 표이고, 원래 노렸던 것은 **"거대행성 법칙은 암석에 적용되지
않는다"는 레짐 문장**입니다. 간선이 `body_class → dynamo_rocky` 라 원래 의도가 정확히 그 문장입니다.

## I-2. 의도적으로 보이는 것 — **26개** (고유 23) → **"정상"**

도입 시점 원문과 현재 그 줄이 **같습니다**(드리프트 0). 즉 표·제목·링크목록을 **일부러** 가리킨 것으로
읽힙니다.

| 종류 | 건 | 대상 (chain 줄) |
|---|---|---|
| **표행 8** | | `body-figure:238` ×2 (`74`,`587`) — α Cen A 의 J₂ 행; `body-figure:244` (`590`) — Fomalhaut A 행; `cassini-state:124` (`602`) — **식 (7)** `\|g\| = \|Ω̇\| ≈ (3/2)·J₂…` (표가 아니라 수식이고 `\|` 로 시작해 제 분류기가 표행으로 셌습니다); `hapke-shader:42` (`888`) — Mars 행; `planetary-dynamo-scaling:27` (`660`) — 갈색왜성 레짐 행; `tidal-heating:217` (`622`) — k₂/Q 클래스표 Rocky 행 |
| **제목 6** | | `body-figure:252` (`582`) `## 7. Procedure (per body)`; `crater-degradation:100` (`868`) `### 4. Fluvial / aeolian`; `tidally-locked-temperature:29` (`645`) `## 1. Why Tidally-Locked Planets Need Special Treatment`; `:61` (`638`) `## 2. Layer 1: Equilibrium Temperature`; `:117` ×2 (`636`,`637`) `### What sets the contrast: advection vs radiation` |
| **계약 4** | | `planetary-dynamo-scaling:18` ×2 (`661`,`662`) — `dynamo_giant` 의 **Needs 줄**, 소비처와 일치 ✅; `rocky-planet-dynamo:24` ×2 (`670`,`680`) — `dynamo_rocky` 의 **Needs 줄**, 일치 ✅ (둘 다 `5ad8f56c` 도입, 그때부터 지금까지 같은 줄) |
| **링크목록 8** | | `cassini-state:203`(`900`) · `tidal-locking:438`(`616`)·`:450`(`613`) · `moon-energy-budget:318`(`620`) · `exoplanet-atmosphere:522`(`796`) · `greenhouse-warming:439`(`813`)·`:441`(`814`) · `atmosphere-reflected-color:439`(`875`) |

**계약 4건은 heat:119 부류와 다릅니다** — 소비처 노드와 계약 블록 주인이 **일치**합니다
(`dynamo_giant`↔`planetary-dynamo-scaling`, `dynamo_rocky`↔`rocky-planet-dynamo`). heat:119 가 틀렸던
이유는 *주인이 달랐기* 때문이고, 그 판별은 "계약 착지 = 나쁨"이 아니라 "**주인 ≠ to:** = 나쁨"입니다.
체커에 넣을 규칙은 후자입니다.

## I-3. 링크목록 9건에 대한 권고 (§ 앵커 / 파일명만)

여덟은 지금 줄이 맞지만 **가장 약한 타깃**입니다(형제 문서가 하나 늘면 움직입니다 — `body-figure:353`
이 이미 +1 밀려 옆 항목을 가리키고 있는 것이 실물 증거입니다).

| ref | 권고 | 이유 |
|---|---|---|
| `atmosphere-reflected-color:439` · `body-figure:353→354` · `cassini-state:203` · `exoplanet-atmosphere:522` · `greenhouse-warming:439`·`:441` · `moon-energy-budget:318` · `tidal-locking:438`·`:450` · `mass-radius-relation:371→424` · `rocky-planet-dynamo:258→259` | ① **`…md@«## Related»`** (§ 앵커) 또는 ② **파일명만**(`ref: "<doc>.md"`) | 이 ref 들이 실어 오는 정보는 "형제 문서가 이 결합을 목록에 적어 뒀다"뿐이고, **간선 자신이 이미 두 노드를 이름으로 적습니다**. 줄을 떼도 잃는 것이 없습니다 |

⚠ 단 `## Related` 를 앵커로 쓰면 **한 문서 안에서 여러 간선이 같은 앵커를 공유**하게 됩니다
(예: greenhouse-warming 은 두 건). 체커의 "정확히 1회 매치" 규칙에는 걸리지 않지만(문서 안 `## Related`
는 한 번), *어느 항목*인지는 잃습니다. 항목 단위 정밀도가 필요하면 항목의 링크 텍스트 자체를
앵커로 쓰는 편이 낫습니다 — 위 표의 앵커 구절들이 이미 그 형태이고 전부 `uniq=1` 입니다.
그래서 실무 권고는 **③ 항목 링크 텍스트를 앵커로**(정밀도 유지 + 드리프트 면역)이고, § 앵커는
정밀도를 포기해도 되는 경우의 대안입니다.

## I-4. 체커(`check_refs.py`)에 넣을 규칙 세 개 (제안)
1. **앵커는 문서에서 정확히 1회 매치** — 현재 37개 전부 통과.
2. **계약 착지의 주인 일치**: 앵커/줄이 `## Contract — \`X\`` 블록 안이면 `X == 간선의 to:`(유출 간선은
   `from:`). heat:119 부류를 잡는 유일한 규칙입니다.
3. **비-본문 착지 경고**: 빈줄·목차·구분선(`---`)·표 구분선(`|---|`)에 착지하면 무조건 FAIL(의도일 수
   없습니다). 표행·제목·링크목록은 WARN — 위 I-2 처럼 의도적인 경우가 실제로 있습니다.
