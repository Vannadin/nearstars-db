<!-- b29b556e 계약 블록 삽입이 chain.yaml ref 줄번호를 얼마나 밀었는지의 전수 대조(tidal +18 / heat +1) — 병렬석 기록, 원문 무편집 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (REF-DRIFT-b29b556e.md, 20:32:13 KST), body unedited. The repair commit that follows b29b556e applies exactly this table. -->

# chain.yaml ref 드리프트 — b29b556e 이후
Parallel seat, 2026-09-04. HEAD `b29b556e`, 워크트리 clean, 읽기 전용.
경로는 `/Users/vana/Desktop/NearStars-wt/engine-prototype/` 기준.
아래 본문은 2026-09-04 에 nearstars-77 로 보낸 메시지 그대로입니다.

**요약: 두 문서를 가리키는 ref 는 서로 다른 값 23개(chain 줄로는 57군데). 그중 22개가 어긋나고,
드리프트는 완전히 균일합니다 — tidal +18, heat +1. 어긋난 22개 전부 `shift(n)` 위치에 원래 문장이
그대로 있습니다.** 그리고 **`b29b556e` 는 ref 줄번호를 하나도 갱신하지 않았습니다** — 그 커밋의 chain
diff 에서 세 ref(`heat:34`·`tidal:266`·`tidal:273`)가 `-`/`+` 양쪽에 나오는데 **값은 동일하고 note 만
재작성**된 것입니다.

이동 규칙(확인): tidal 은 hunk `@@ -42,6 +42,24 @@` 이라 **n ≤ 44 불변, n ≥ 45 → n+18**.
heat 은 `@@ -42,9 +42,10 @@` 이라 **n ≤ 44 불변, n ≥ 46 → n+1**(n = 45 는 두 줄로 분화).

# tidal-heating-methodology.md

| chain 줄 | 간선 | ref | 현재 그 줄 내용(앞 60자) | 의도한 문장 위치 | 판정 |
|---|---|---|---|---|---|
| `543` | `body_class → k2q_class_table, selects` | `:194` | `resonance, which in turn forces Io's \`e ≈ 0.0041\` against da` | **`:212`** — "`k₂/Q` is the **dominant uncertainty**: it spans ~3 orders o…" | **불일치** |
| `555` | `k2q_class_table → tidal_heating, requires via k2_over_q` | `:194` | 위와 같음 | **`:212`** | **불일치** |
| `609` | `body_figure → crater_state, requires via relief` | `:471` | `\| **521 km (adopted)** \| **1.552×10²¹** \| **78×** \| **2,231 ` | **`:489`** — "- The absolute relief does scale. Dante's `J₂ = 0.039` / `C₂…" | **불일치** |
| `617` | `orbit_elements → tidal_heating, requires via [a,e,n]` | `:61` | `**Grade** — analog. \`resurfacing_rate\` is not emitted (no fo` ← **이 커밋이 새로 넣은 계약 블록 안** | **`:79`** — `Ė ∝ (k₂/Q)·R⁵·e²·M_p^(3/2)·a^(−15/2)` | **불일치** |
| `619` | `resonance_architecture → tidal_heating, requires via forced_e` (gap) | `:182` | `## 4. The eccentricity-maintenance requirement` | **`:200`** — "Practical rule: **if you are claiming sustained tidal heatin…" | **불일치** |
| `622` | `tidal_heating → interior_layers, influences non-monotonic` | `:199` | (빈 줄) | **`:217`** — `\| **Rocky / silicate** (Io-like, terrestrial) \| ~0.1–0.3 \| ~` | **불일치** |
| `631` | `tidal_heating → mass_radius_relation, requires via radius_ceiling` · **status: gap (C30 2026-09-04)** | `:442` | `> observed does.` | **`:460`** — "it. Size is therefore the strongest transport knob, and the …" | **불일치** |
| `632` | `tidal_heating → heat_transport_mode, requires via surface_flux` — **이 커밋에서 note 갱신됨(ref 값은 그대로)** | `:273` | `\`e\` is *maintained* (§4): name the resonance, or flag the he` | **`:291`** — "A body's surface has exactly three ways to pass internal hea…" | **불일치** |
| `633` | `internal_heat_nontidal → heat_transport_mode, requires via radiogenic_power` — **이 커밋에서 via 개명 + note 갱신됨(ref 값 그대로)** | `:266` | `\| ≳ 1 W/m² \| vigorous silicate volcanism, possible magma oce` | **`:284`** — "primordial). For an Earth-mass body radiogenic heating alone…" | **불일치** |
| `634` | `global_fluid_layer → heat_transport_mode, selects` | `:332` | `Heat piping *"produces a thick, cold, and strong lithosphere` | **`:350`** — "> the globe. Where a **global fluid layer** exists, it redis…" | **불일치** |
| `635` | `t_eq_stellar → heat_transport_mode, requires` | `:341` | `So the design rule is the inverse of the intuitive one: **yo` | **`:359`** — "**inert**: it sits at radiative equilibrium with its externa…" | **불일치** |
| `646` | `tidal_heating → ice_stability, requires` | `:717` | `**Surface heat transport (§6.2–§6.5).** Verified in the same` | **`:735`** — `([\`2019JGRE..124..114K\`](…` | **불일치** |
| `647` | `tidal_heating → crater_state, requires` | `:720` | `([\`1981GeoRL...8..313O\`](…` | **`:738`** — "- **Spencer, D. C., Katz, R. F. & Hewitt, I. J. (2020)**: *J…" | **불일치** |
| `654` | `tidal_heating → surface_albedo, requires via plains_temperature` · **status: gap (C30 2026-09-04)** | `:460` | `it. Size is therefore the strongest transport knob, and the ` | **`:478`** — "leaves the plains at their external-budget 223 K — cold enou…" | **불일치** |

⚠ `617` 은 특히 눈에 띕니다 — `:61` 이 지금 **이 커밋이 새로 넣은 `heat_transport_mode` 계약 블록의
Grade 줄**을 가리킵니다. 조석 법칙의 축약형(`:79`)을 가리키려던 ref 가 계약 블록 안을 가리키게 됐습니다.

# internal-heat-luminosity-methodology.md

| chain 줄 | 간선 | ref | 현재 그 줄 내용(앞 60자) | 의도한 문장 위치 | 판정 |
|---|---|---|---|---|---|
| `655` | `tidal_heating → internal_heat_nontidal, requires via power` — **이 커밋에서 note 갱신됨(ref 값 그대로), C30 built** | `:34` | `here folds in only the non-tidal sources (add the tidal flux` | **`:34`** (동일) | **일치** — hunk 가 `:42` 부터라 이 줄은 안 움직임 |
| `699`–`726`, `818`·`821`·`822`·`897` (총 32군데) | radiogenic 계열 간선 다수 | `:118` | `\`core_profile_mass_residual\` [—] · \`core_center_pressure_sol` | **`:119`** — `**Needs** — \`mass_earth\` [M_earth] · \`core_mass_fraction\` [—` | **불일치** |
| `661` | `internal_heat_nontidal → dynamo_giant, requires via l_int` | `:472` | `**Earth (the rocky calibration: the heat goes into the inter` | **`:473`** — "global heat loss is **~46–47 TW** (Davies 2013; Sclater+ 198…" | **불일치** |
| `689` | `internal_heat_nontidal → dynamo_rocky, requires via geotherm` (gap) | `:202` | `1. [The relation: T_eff⁴ = T_eq⁴ + T_int⁴](#1-the-relation-t` | **`:203`** — "2. [The cooling track: L_int(M, age) behaviour](#2-the-cooli…" | **불일치** |
| `795` | `internal_heat_nontidal → atmosphere_choice, requires via outgassing` (gap) | `:208` | `7. [Worked examples](#7-worked-examples)` | **`:209`** — "8. [Honesty & uncertainty](#8-honesty--uncertainty)" | **불일치** |
| `823` | `body_class → internal_heat_nontidal, selects` | `:187` | `\`inner_core_nucleation_gyr_ago\` [Gyr] · \`delta_e_min_3gyr_lo` | **`:188`** — "`delta_e_present_hi` [W/K] · `entropy_history_verdict` [—] ·…" | **불일치** |
| `824` | `star_metallicity → internal_heat_nontidal, influences` (gap) | `:254` | (빈 줄) | **`:255`** — `---` | **불일치** |
| `836` | `internal_heat_nontidal → mass_radius_relation, influences +` | `:477` | `radiogenic elements at present, so the rest should be suppor` | **`:478`** — "that the convective ratio is *lower* than conventionally ass…" | **불일치** |
| `837` | `internal_heat_nontidal → t_eff_body, requires via t_int` | `:60` | `the **radiogenic flux alone** (Earth ≈ 29 K; §1's ≈ 35 K use` | **`:61`** — "so this `t_int` is a floor on that). `mantle_radiogenic_powe…" | **불일치** |
| `838` | `t_eq_stellar → t_eff_body, requires (textbook)` | `:60` | 위와 같음 | **`:61`** | **불일치** |
| `896` | `internal_heat_nontidal → t_eff_body, excludes (self)` | `:308` | (빈 줄) | **`:309`** — "**NearStars rule:** for a young (≲ few hundred Myr) self-lum…" | **불일치** |

# 성질 정리 (판단 아님)

- **23개 중 22개 불일치, 1개 일치(`heat:34`)**. 일치하는 하나는 유일하게 hunk 위(`:42` 이전)에 있는
  ref 입니다.
- **드리프트가 균일합니다.** tidal 13개 전부 정확히 +18, heat 9개 전부 정확히 +1. 각 경우
  `old[n] == cur[shift(n)]` 를 프로그램으로 대조해 확인했습니다 — 즉 커밋 전에는 23개 모두 맞았고,
  지금은 문장이 이동한 만큼만 어긋납니다. 다른 종류의 오지시는 없습니다.
- **heat 문서의 `:118` 하나가 chain 32군데에 걸려 있습니다**(`699`–`726` 연속 +
  `818`·`821`·`822`·`897`). 이동폭은 +1 이므로 영향은 작지만 수정 대상 수가 가장 많은 값입니다.
- 이번 커밋이 chain 에서 실제로 바꾼 것은 노드 outputs 두 개(`@@ -397,15`), 간선 note·via·status
  (`@@ -624,12`·`@@ -648,9`·`@@ -683,7`)입니다.
- ko 미러(`ko/docs/reference/…`)를 가리키는 ref 는 chain 에 **0개**라 생략했습니다.

## 대조 방법 (재현용)
`git show b29b556e~1:<file>` 로 커밋 직전 본문을, 워킹카피로 현재 본문을 읽고, chain.yaml 에서
`(tidal-heating-methodology\.md|internal-heat-luminosity-methodology\.md):(\d+)` 를 정규식으로 전부
수집한 뒤, 각 ref n 에 대해 `cur[n] == old[n]`(일치 여부)과 `old[n] == cur[shift(n)]`(드리프트 확인)을
대조했습니다.
