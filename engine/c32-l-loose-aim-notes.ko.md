<!-- 병렬석 조사 기록 (원문 무편집). C33 batch L: loosely aimed anchors, measured against a month of edit history. -->
<!-- Preserved verbatim from the parallel seat's scratch on 2026-09-05, so it stays Korean and keeps its
     numbers, quotations and tables exactly as measured; the .ko.md name declares that (check_language.py).
     C33 batch L: loosely aimed anchors, measured against a month of edit history. -->
# L — `planetary-magnetosphere-geometry:4` 두 건, 그리고 "출생부터 느슨" 부류 전수
Parallel seat, 2026-09-05. HEAD 6654d314, 읽기 전용, 레포 쓰기 없음.

## ⚠ 자기 정정 먼저 — `magnetosphere:4` 는 **느슨하지 않습니다**

제가 K-2 에서 "산문이고 식이 아니라 출생부터 조준이 느슨하다"고 이름 붙였는데, 도입 커밋으로 확인해
보니 **틀렸습니다.**

두 간선(`chain:742`·`743`)은 `08f25e64` (2026-08-24) 저작이고, **그 커밋의 문서 `:4` 와 오늘의 `:4` 가
글자까지 같습니다**(Δ=0, 문서 머리 12줄 전체가 무변경). 그 줄은 —

> `:4-6` **Method reference for turning a body's **dipole field strength** (from the
> [rocky](../docs/reference/rocky-planet-dynamo-methodology.md) or [giant](../docs/reference/planetary-dynamo-scaling.md)
> dynamo recipes) into the **shape and size of its magnetosphere** …**

두 간선은 `dynamo_giant → magnetosphere_geometry, requires, via: b_eq` 와
`dynamo_rocky → …, via: b_eq` 입니다. 즉 이 문장은 **payload(dipole field strength = b_eq)와 두 공급
노드(rocky·giant dynamo recipes)를 한 문장에 전부 이름으로 적습니다.** `requires via b_eq` 라는 간선이
가리킬 수 있는 **가장 정확한 한 문장**입니다. 제가 "식이 아니다"를 근거로 삼은 것이 잘못이었습니다 —
`requires` 간선의 근거는 소비 공식이 아니라 **그 입력이 어디서 오는지**입니다.

### 앵커 후보 셋 (전부 `uniq=1` 확인)

| 후보 | 줄 | 무엇을 말하는가 | 판정 |
|---|---|---|---|
| **`«Method reference for turning a body's **dipole field strength** (from the»`** | `:4` | b_eq 의 **출처**(두 다이나모 레시피)와 소비처의 산출을 함께 | ✅ **권고** — 두 간선 공용, 현 상태 유지 + 앵커화 |
| `«Only the **equatorial (sub-solar) field** enters»` | `:107` | **어느** b_eq 인가(적도장, 극장이 아님) | 대안 — 간선의 뜻을 "어느 b_eq" 로 좁히려면 이쪽 |
| `«R_mp / R_p  =  [ f² · B_eq² / (2 μ₀ · P_ram) ]^(1/6)»` | `:80` | b_eq 를 **소비하는 식** | 권하지 않음 — 그 식의 근거는 `P_ram` 쪽 간선(`chain:739`)이 이미 `:83` 로 가리킵니다. 두 간선이 같은 식을 중복 인용하게 됩니다 |

**결론: 정정 불필요. `:4` → `@«Method reference for turning a body's **dipole field strength** (from the»`
로 앵커화만 하면 됩니다.** (제가 이전 자기권 조사에서 "`:4` 는 식이 아니라 산문 줄"이라고 적은 것은
사실 서술로는 맞지만, **그것이 결함이라는 함의는 철회합니다.**)

## L-2. "출생부터 느슨" 부류 전수 — 재사용 8개 값 판정

`via:` payload / `to:` 노드가 착지 문장에 실제로 서술돼 있는지로 판정했습니다. 간선은 chain.yaml 원문을
직접 읽었습니다(제 정규식 창 추출이 이웃 간선을 잡는 일이 있어 손으로 대조).

| 값 (재사용) | 착지 줄 | 쓰는 간선 | 판정 |
|---|---|---|---|
| **`body-figure:256` ×3** | `(Helled+2011 convention; the emit \`reference_radius\` is the equatorial radius).` — §7 절차의 **2단계 괄호** | `542` `body_class → nmoi_class_table, selects` · `553`·`569` `nmoi_class_table → body_figure via nmoi` | ⚠ **느슨 — 한 줄 위 조준.** 세 간선 전부 NMoI 이야기인데 착지는 **반지름 규약** 괄호입니다. 정답은 바로 아래 **`:257`** — `3. Pick NMoI from the body class (giant 0.20–0.26; rocky 0.30–0.36; star 0.05–0.08)` (uniq=1). 앵커 후보: `@«3. Pick NMoI from the body class (giant 0.20–0.26; rocky 0.30–0.36; star 0.05–0.08)»` |
| **`exoplanet-atmosphere:66` ×2** | `The first question is not *how much* atmosphere but *whether any survives at all*.` — `## 2. Gate 1: Retention (the Cosmic Shoreline)` 의 **단락 첫 줄** | `787` `xuv_history → atmospheric_escape, requires` · `788` `mass_or_radius → atmospheric_escape via v_esc` | ⚠ **약하게 느슨 — 단락 머리 조준.** 두 payload 는 바로 다음 두 줄(`:67-68` "the planet's gravity (escape velocity)" / "XUV + insolation")에 있고, 판정식은 **`:74`** `space, roughly \`v_esc ∝ I_XUV^(1/4)\`. It is empirical and remarkably sharp.` (uniq=1). "절을 가리킨다"로 읽으면 틀린 건 아니지만, 두 payload 를 한 줄에 담는 앵커가 있습니다 — `@«roughly \`v_esc ∝ I_XUV^(1/4)\`»`, 또는 절 단위로 갈 거면 `@«## 2. Gate 1: Retention (the Cosmic Shoreline)»`(uniq=1) |
| `tidal-heating:212` ×2 | `\`k₂/Q\` is the **dominant uncertainty**: it spans ~3 orders of magnitude across body` | `543` `body_class → k2q_class_table, selects` · `555` `k2q_class_table → tidal_heating via k2_over_q` | ✅ **정확.** "**across body** [classes]" 가 `body_class → k2q_class_table` 그 자체이고, k₂/Q 가 payload 이름으로 적혀 있습니다 |
| `cassini-state:166` ×2 | `- **J₂** and, for locked bodies, **C̄₂₂**  · **C/MR²** (body class) · **spin ω**` — 입력 목록 | `554` `nmoi_class_table → cassini_state via nmoi` · `579` `interior_layers → cassini_state via nmoi` | ✅ **정확.** payload(nmoi = C/MR²)가 목록에 이름으로 있습니다 |
| `surface-radiation-dose:45` ×2 | `C [g cm⁻²]  =  0.1 · P [Pa] / g [m s⁻²]` | `773` `atmosphere_choice → surface_dose via column` · `774` `mass_or_radius → surface_dose via gravity` | ✅ **정확.** 두 payload(`column` = C, `gravity` = g)가 **같은 식 안에 둘 다** 있습니다 — 재사용의 모범 사례 |
| `moon-energy-budget:132` ×2 | `6. **The solid-body tidal term is global only when something makes it global.** Averaging` | `809` `global_fluid_layer → moon_energy_budget, selects` · `810` `heat_transport_mode → moon_energy_budget, selects` | ✅ **정확.** "something makes it global" 이 바로 그 두 선택자(전지구 유체층 / 수송 모드)입니다 |
| `body-figure:238` ×2 | `\| **α Cen A** \| star (G2V) \| **P_rot 22 d** \| 4.6e-5 \| …` | `587` `star_physical → body_figure via p_rot` (다른 하나 `74` 는 **주석**이고 ref 가 아닙니다) | ✅ **정확** — payload(`p_rot`)가 그 행의 칸입니다. 실질 재사용 ×1 |
| `tidally-locked-temperature:117` ×2 | `### What sets the contrast: advection vs radiation` | `636` 은 **이미 앵커로 이관됨**(`@«### What sets the contrast: advection vs …»`), `637` 은 다중행 | ✅ 이관 진행 중 |

## L-3. 정리

- **재사용 8개 값 중 느슨한 것은 둘**: `body-figure:256` ×3 (**한 줄 위**, 확실) 와
  `exoplanet-atmosphere:66` ×2 (**단락 머리**, 약함).
- **`magnetosphere:4` ×2 는 느슨하지 않습니다** — 제 이전 라벨을 철회합니다.
- 남은 다섯(`tidal-heating:212`·`cassini-state:166`·`surface-radiation-dose:45`·`moon-energy-budget:132`·
  `body-figure:238`)은 **payload 가 착지 줄에 이름으로 적혀 있어** 재사용에도 정확합니다.
- ⚠ 관찰 하나: **정확한 다섯은 전부 payload 이름이 착지 줄 안에 리터럴로 있습니다.** 느슨한 둘은
  없습니다. 즉 제가 J-② 에서 폐기했던 키워드 대조가 **재사용 값에 한정하면** 판정력이 있습니다
  (8건 중 8건 정답). 전수 145건에서 못 쓴 이유는 단일-사용 값이 대부분 산문을 가리키기 때문이고,
  재사용 값은 "여러 간선이 공유할 만큼 명시적인 문장"을 가리키는 경향이 있어 리터럴 매치가 듣습니다.
  체커에 넣는다면 **재사용 값(2회 이상)에만 켜는 WARN 규칙**으로는 값이 있습니다.
