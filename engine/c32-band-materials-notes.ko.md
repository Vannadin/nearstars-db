<!-- 병렬석 조사 기록 (원문 무편집). C32 band materials: what a min/max band can be built from, per facet. -->
<!-- Preserved verbatim from the parallel seat's scratch on 2026-09-05, so it stays Korean and keeps its
     numbers, quotations and tables exactly as measured; the .ko.md name declares that (check_language.py).
     C32 band materials: what a min/max band can be built from, per facet. -->
# C32 재료 조사 — 밴드 폭의 출처 · 묶음 경계 · heat ref 앵커 후보
Parallel seat, 2026-09-04 (23:54 KST). 엔진 워크트리 HEAD `a01d7277` clean, 읽기 전용, 레포 쓰기 없음.
경로는 `/Users/vana/Desktop/NearStars-wt/engine-prototype/` 기준. `rocky` =
`docs/reference/rocky-planet-dynamo-methodology.md`(271행), `scaling` =
`docs/reference/planetary-dynamo-scaling.md`(190행), `heat` =
`docs/reference/internal-heat-luminosity-methodology.md`.
추정 없음 — 근거가 문서에 없는 축은 "**없음**"으로 이름을 붙였습니다.

# A. 세기류 출력별 "밴드 폭이 어디서 오는가"

## A-1. `dynamo_rocky`

문서가 인쇄하는 Returns(`rocky:21-23`)에 밴드 필드가 넷 있습니다 —
`dipole_moment_min`/`_max`, `b_eq_multipolar_min`/`_max`. `b_eq`·`b_pol` 자체는 **점값**이고
min/max 짝이 없습니다.

| 출력 | 밴드 폭의 출처 | 판정 |
|---|---|---|
| `b_eq` · `b_pol` | **없음.** 두 값에 대응하는 min/max 필드가 계약에 없습니다. 코드도 `b_eq_ut(moment)` 로 단일 moment 에서 한 값만 냅니다(`engine/dynamo_rocky.py:236-238`). 닫는 관계식 `B_s^eq = 30·(ℳ/ℳ⊕)·(R/R⊕)^(−3)`(`rocky:99-100`)에는 폭이 붙어 있지 않습니다 | **없음 → authored** |
| `dipole_moment_min/max`, 레짐 1 (건조, M < 2 M⊕) | `rocky:159-161` "`ℳ_base` **up to ~1 ℳ⊕**". 코드는 `M_BASE[1] = (1.0, 1.0)`(`dynamo_rocky.py:79`) — **폭 0 의 점값**. 문서의 "up to ~1" 은 상한만 말하고 하한을 인쇄하지 않습니다 | **하한 없음 → authored**(현재는 상·하한을 같게 두어 폭을 안 만드는 선택) |
| `dipole_moment_min/max`, 레짐 2 (건조, 2–2.5 M⊕) | `rocky:162-164` "Thermal dynamo, **can exceed Earth's moment while young**" — **수치 없음**. 코드 `M_BASE[2] = (1.0, 2.0)` 이고 그 줄의 주석이 스스로 "**NO VALUE IN THE DOC**"(`dynamo_rocky.py:80`) | **없음 → authored** (2.0 이 authored) |
| `dipole_moment_min/max`, 레짐 3 (슈퍼지구, > 2.5 M⊕) | `rocky:165-167` "dynamo is **weaker and shorter-lived** than a naive mass-scaling suggests. Flag confidence low." — **수치 없음**. 코드 `M_BASE[3] = (0.3, 1.0)`, 주석 "**NO VALUE IN THE DOC**"(`:81`) | **없음 → authored** (0.3 과 1.0 둘 다) |
| `dipole_moment_min/max`, 레짐 4 (물 풍부) | `rocky:168-170` "Ganymede analog (`ℳ ≈ 2×10⁻³`)". 코드 `(2.0e-3, 2.0e-3)` — 점값. ⚠ 문서 자신이 `rocky:170` 에 "**No source is cited for this item**" 를 적고, `rocky:144-147` 은 RM22 Table 8 이 Ganymede 에 **0.003(모델)과 0.002(관측)** 두 값을 인쇄하므로 "어느 쪽을 앵커로 쓸지는 열린 선택(C17), 여기서 결정하지 않음"이라고 적습니다 | **폭의 재료는 있음(0.002–0.003), 폭으로 쓰이지 않음** |
| `dipole_moment_min/max`, 레짐 5 (저밀도 건조) | `rocky:187-188` "likely dynamo-dead by a few Gyr → `ℳ = 0`". 코드 `(0.0, 0.0)` | 점값 0, 폭 불필요 |
| `b_eq_multipolar_min/max` (다극자 계수) | **있음, 문서에 인쇄됨.** `rocky:81-83`: "The engine's grid is **OC06's own width, {0.05, 0.10}** — text *'nearly a factor of 20'*, abstract *'a factor of 10 or more'* — with RM22's Solar-System point 0.06 inside it (RM22 adopts 0.05, its reading of OC06; **OC06 prints no 0.05**)." 재확인 `rocky:235`. 코드 `MULTIPOLAR_FACTORS = (0.05, 0.10)`(`dynamo_rocky.py:86-90`), `MULTIPOLAR_SOLAR_SYSTEM = 0.06`(`:91`) | **근거 있음 — 한 양에 대한 OC06 자신의 두 인쇄 진술, 2× 폭** |

⚠ 다극자 계수에 붙은 조건 두 개도 문서에 인쇄돼 있습니다.
- **base-heated 전용**: `rocky:83-86` "OC06: internally heated cases are *'more gradual, show more scatter,
  and begin at smaller Ro_l'*; RM22 carries the condition (*'as is the case on Earth'*). Whether a roster
  body's core is base-heated is **not something this recipe can decide**, and the label rides on every
  multipolar value and on the 0.12 threshold itself." (코드 `MULTIPOLAR_CONDITION`, `:93`)
- **제거된 오항목**: `rocky:75-79` Grießmeier 2009 의 0.15 는 "**not a value of this quantity**" 라
  2026-09-04 에 격자에서 빠졌습니다(그 논문에 Rossby 수도 0.12 도 없음).

## A-2. `dynamo_giant`

계약(`scaling:17`)에서 **거대행성 가지는 `b_pol`·`b_eq`·`dipole_moment` 세 점값뿐이고 min/max 가 없습니다.**
min/max 는 **갈색왜성 가지 전용**(`b_dyn_min/max`, `b_eq_min/max`)입니다. 코드가 그대로입니다 —
거대행성 출력 블록 `engine/dynamo.py:235-238` 은 세 값만, 갈색왜성 블록 `:144-151` 이 밴드를 냅니다.

| 출력 | 밴드 폭의 출처 | 판정 |
|---|---|---|
| 거대행성 `b_pol`·`b_eq`·`dipole_moment` | **없음.** 법칙 `B_dip^pol(M, age) = 9 G · (age/4.5 Gyr)^(−0.33) · (M/M_Jup)^0.93`(`scaling:83`)에 폭이 없습니다. 문서가 폭 대신 적는 것은 신뢰도 문장입니다 — `scaling:158-160` "Confidence stays **low–medium**: the *method* is grounded and validated, but the inputs (internal luminosity via age, mass for M sin i cases, radius for non-transit giants) each carry real uncertainty, and the dipole moment scales as R³." 폭을 만드는 규칙은 아닙니다 | **없음 → authored** |
| 거대행성 검증표의 괄호 범위 | ⚠ **표에는 범위가 있는데 레시피에는 없습니다.** `scaling:136-138`: ε Eri b **660 µT (540–810)**, GJ 896 A b **1980 µT (1600–3400)**, ε Ind A b **3220 µT (2600–3700)**. 그중 두 개만 유래가 인쇄돼 있습니다 — GJ 896 A b 는 나이 범위(`scaling:152-153` "host age is genuinely uncertain (≲100 Myr PMS vs ~950 Myr); the field spans a **factor ~2** across that range"), ε Ind A b 는 질량지수 외삽(`scaling:154-156` "the 0.93 mass exponent is extrapolated above its 1–5 M_J calibration, so the central value carries an **extra ~25 %** systematic"). **ε Eri b 의 540–810 은 유래가 인쇄돼 있지 않습니다**(`scaling:149-151` 은 청년기 효과의 부호 정정만 적습니다) | 두 개는 **근거 있음(입력 불확실성 전파)**, ε Eri b 는 **없음** |
| 같은 괄호 범위의 기계 검증 | ⚠ **검증되지 않습니다.** `engine/dynamo_table.py:22-25` 의 `BODIES` 는 중심값(660·1980·3220)과 모멘트만 담고, 대조는 `abs(beq - doc_beq)/doc_beq <= 0.03` 로 **중심값만** 봅니다. 괄호 범위는 생성물도 아니고 게이트 대상도 아닙니다(문서 `scaling:140-141` 은 "Generated by `engine/dynamo_table.py`, not hand-keyed" 라고 적지만 그 진술은 중심값에 대한 것) | **불일치 표시 대상** |
| 갈색왜성 `b_dyn_min/max`·`b_eq_min/max` | **있음, 문서에 인쇄됨.** `scaling:27` "emitted as a **band over the declared radius** (`R^(−7/6)`); refuses when the luminosity, rotation period, **radius band** or `isolated` is missing". 코드 `dynamo.py:130-131` 이 `b_hi = b_dyn_kg(radius_rj_min)`, `b_lo = b_dyn_kg(radius_rj_max)` 로 그대로 구현하고, note 가 "band is radius-driven: R enters as R^(-7/6) and R is declared, not measured"(`:155`) | **근거 있음 — 선언된 반지름 밴드 + 인쇄된 지수** |

## A-3. A 요약 — authored 가 붙을 자리

| 자리 | 이유 |
|---|---|
`dynamo_rocky.b_eq` / `b_pol` 의 폭 | 계약에 필드가 없고 닫는 식에 폭이 없음 |
`M_BASE[1]` 의 하한 | 문서는 "up to ~1 ℳ⊕" 로 상한만 인쇄 |
`M_BASE[2] = (1.0, 2.0)` | 문서에 수치 0개 ("can exceed Earth's moment while young") |
`M_BASE[3] = (0.3, 1.0)` | 문서에 수치 0개 ("weaker and shorter-lived") |
`dynamo_giant` 거대행성 가지의 폭 전체 | 법칙에 폭 없음, 신뢰도 문장만 |
ε Eri b 괄호 범위 540–810 | 표에만 있고 유래가 인쇄돼 있지 않음 |

근거가 **있는** 두 곳은 다극자 격자 {0.05, 0.10}(OC06 두 인쇄 진술)과 갈색왜성 반지름-구동 밴드
(선언 반지름 + `R^(−7/6)`)입니다. C32 가 "밴드로 낸다"를 할 때 문서를 그대로 인용할 수 있는 곳은
이 둘뿐입니다.

# B. 묶음 경계 — 엔진 값 ↔ 선언 값 ↔ 보드 값

로스터 다섯 바디를 `run.py bodies/<b>.yaml` 로 돌려 얻은 엔진 값과, `phase4/*.yaml` 의
`magnetic_field` 행 전수(19행)를 대조했습니다.

| # | 천체 | 엔진 값 | 보드 값 (줄) | 갈림 | 후보값·출처·등급 |
|---|---|---|---|---|---|
| **1** | **Pandora** (A b III) | `b_eq` **41.37 µT** / `b_pol` 82.75 µT · `dipole_moment` 1.0 ℳ⊕ (레짐 1, 밴드 1.0–1.0) | **75 µT** eq / 150 µT pol (`alpha_centauri.yaml:2296-2297`, `op: set`) | **1.81×** | 보드가 인쇄한 근거는 "**the upper bound of the rocky-dynamo ℳ⁺ ladder**"(`:2296`)이고 evidence 는 "the ℳ⁺ upper bound, ~1.8× Earth … the interesting-first high end"(`:2303-2305`). 75 µT 를 역산하면 **ℳ ≈ 1.81 ℳ⊕** 인데, 엔진 레짐 1 의 밴드는 **1.0 점값**입니다 — 즉 보드가 말하는 "상한"은 **엔진에 대응물이 없습니다**(그 값은 레짐 2 의 authored 밴드 (1.0, 2.0) 안에 들어가는데 Pandora 는 0.6447 M⊕ 로 레짐 1). 후보: ① 41.37(엔진, 레짐 1 상한 그대로) ② 75(보드, interesting-first) ③ 밴드 41.4–82.7 을 내고 오너가 고름. 등급: ①은 analog, ②③은 **authored** |
| **2** | **Alpha Centauri A b** (Polyphemus) | `b_eq` **172.3 µT** / `b_pol` 344.7 µT · `dipole_moment` 7660 ×Earth | **170 µT** (`:658`, `op: set`, `phase3_default: "170 µT (Phase 3's grounding was corrected too)"`) | **1.4 %** | 사실상 일치. 다만 하류가 **보드의 170** 을 쓰고 있습니다(자기권 `R_mp` 계산이 170 µT 로 도출 — 제 `TIDAL-CHECK`/자기권 보고 참조). 후보: 엔진 172.3 로 통일하고 리플(R_mp)을 재계산하거나, 보드 170 을 계속 쓰고 1.4 % 차를 라벨. 등급: 엔진 값 = calibrated(`scaling:21`), 보드 값 = passthrough-with-rounding |
| **3** | **Luhman 16 A** | `b_dyn` **1246 G** (밴드 **1102–1431 G**) · `b_eq` 440.5 G | **1250 G** (`luhman_16.yaml:268`, note "R 0.08-0.10 spread gives **1100-1430 G**") | **0.3 %** | 일치. **밴드까지 일치**(1102–1431 vs 1100–1430) — 이미 밴드로 나가 있는 유일한 자리 |
| **4** | **Luhman 16 B** | `b_dyn` **1176 G** (밴드 **1041–1351 G**) | **1180 G** (`:919`, note "1040-1350 G") | **0.3 %** | 일치, 밴드도 일치 |
| **5** | **Earth** | `b_eq` 30 µT / `b_pol` 60 µT (앵커, 구성상 정의값) | 보드 없음(태양계) | — | 앵커. `rocky:96-97` 이 30/60 µT 를 정규화 기준으로 인쇄 |
| **6** | **Cassandra** (A b IV) | **엔진 바디 파일 없음** | "~0.4 µT eq / ~0.8 µT pol (a Ganymede-class intrinsic dipole … **M ~ 2e-3 M⊕**)" (`:2801`) | 미측정 | 보드가 레짐 4 앵커(2×10⁻³)를 명시적으로 쓰고 있습니다. R 3400 km = 0.5337 R⊕ 로 닫는 식에 넣으면 **0.395 µT** — 보드 0.4 과 일치. **바디 파일만 만들면 엔진이 재현할 자리.** 등급: analog. ⚠ 단 레짐 4 앵커 자체가 `rocky:144-147` 의 미결 선택(0.002 vs 0.003)에 걸려 있음 |
| **7** | **Dante** (A b I) | 바디 파일 없음 | "none (no intrinsic dynamo; only an Io-style induced field)" (`:1506`) | — | 엔진 대응: 레짐 5 또는 `dynamo_alive` 게이트의 이름 있는 거절. 등급: declared |
| **8** | **Hades** (A b II) | 바디 파일 없음 | "none (a 750 km rocky moon cannot run a dynamo)" (`:1856`) | — | 같음 |
| **9** | **Chaos** (A b V) | 바디 파일 없음 | "none (a small icy body cannot run a dynamo)" (`:3165`) | — | 같음 |
| **10** | **40 Eridani A b** | 바디 파일 없음 | "**~25× 지구** (Weir canon; 강한 이유=높은 코어 열플럭스, 자전 아님 — Weir 자전-논리는 dated)" (`40_eridani.yaml:568`, `op: set`) | 미측정 | ⚠ **삼중 갈림**: canon(Weir 소설) + 보드 확정 + 엔진 미평가. 25× 지구 = ℳ 25 ℳ⊕ 로, 레짐 1–3 의 어떤 authored 상한(최대 2.0)보다 **한 자릿수 큽니다**. 후보: ① 사다리 값 ② canon 25× 유지 + documented-divergence ③ 밴드+선택지. 등급: ②는 **authored / fiction-canon** |
| **11** | 항성 5개 (α Cen A·B, Barnard, τ Cet, 40 Eri A) | `dynamo_giant` 가 M > 70 M_J 로 거절(`scaling:29`) | 각각 측정·유비값 (`alpha_centauri:1030`·`1161`, `barnards_star:83` 0.43 kG, `tau_cet:81` 0.17 G, `40_eridani:78`) | — | 항성은 이 레시피 밖. `op: passthrough` 인 것과 `op: set` 인 것이 섞여 있음(α Cen A·B 는 `set` 이지만 값이 "~1–2 G" 같은 유비 서술) |
| **12** | Fomalhaut · 40 Eri B·C · 그 외 소형체 | 바디 파일 없음 | "none/미검출", "비자성 DA", "강한 (kG급 예상 …)", "무시급/없음" (`fomalhaut:101`, `40_eridani:155`·`237`·`804`·`1028`) | — | 전부 서술형 선언. 엔진이 낼 축이 아닌 것과, 낼 수 있는데 바디 파일이 없는 것이 섞여 있음 |

**B 요약** — 실제로 값이 갈리는 자리는 **두 곳**입니다: **Pandora 1.81×** 와 **40 Eri A b 의 canon 25×**.
나머지는 (a) 1.4 % / 0.3 % 수준의 반올림 차(#2·#3·#4), (b) 엔진 바디 파일이 없어 아직 대조 자체가 안 된
자리(#6–#10, #12), (c) 레시피 밖(#11)입니다. 그리고 **밴드로 이미 나가 있는 자리는 갈색왜성 둘뿐**이고,
그 둘은 보드와 밴드까지 맞습니다 — C32 가 목표로 하는 형태의 선례가 이미 존재합니다.

# C. `heat:203` · `:209` · `:255` — 어느 문장을 가리키려던 것인가

⚠ **찾았습니다. 세 ref 는 도입 시점에 정확했고, 그 뒤 문서가 자라면서 밀렸습니다.**
`git log -S` 로 각 값의 도입 커밋을 찾아 그 커밋의 문서 줄을 찍었습니다.

| chain 줄 | 간선 | 도입 커밋 | 도입 당시 그 줄 | 지금 그 문장의 위치 |
|---|---|---|---|---|
| `689` | `internal_heat_nontidal → dynamo_rocky, requires via geotherm` (gap) | **`08f25e64` (2026-08-24), ref `:202`** | `- **core convection → a dynamo magnetic field.** Whether the core stays hot and convecting` | **`heat:370`** |
| `795` | `internal_heat_nontidal → atmosphere_choice, requires via outgassing` (gap) | **`08f25e64` (2026-08-24), ref `:208`** | `- **mantle convection → volcanism → outgassing.** The interior heat budget governs whether` | **`heat:376`** |
| `824` | `star_metallicity → internal_heat_nontidal, influences` (gap) | **`08f25e64` (2026-08-24), ref `:254`** | `Spiegel, Burrows & Milsom 2011 pinned the deuterium-burning mass limit (and showed it` | **`heat:422`** |

세 ref 값 `:203`·`:209`·`:255` 는 **`0ace3863`(2026-09-04)이 만든 것**입니다 — 그 커밋이 이미 밀려 있던
`:202`·`:208`·`:254` 에 균일하게 +1 을 적용했기 때문입니다. 즉 `0ace3863` 은 b29b556e 의 이동만 되돌렸고,
그 전부터 누적돼 있던 드리프트는 그대로 옮겼습니다.

**앵커 후보 구절** (줄번호가 아니라 구절로 — 다시 밀리지 않게)

| chain 줄 | 제안 앵커 구절 | 그 구절이 왜 이 간선인지 |
|---|---|---|
| `689` (geotherm → dynamo_rocky) | `**core convection → a dynamo magnetic field.**` — 전체 문장은 "Whether the core stays hot and convecting long enough to sustain a dynamo is a **thermal-history question** (Driscoll & Bercovici 2014 …). This is the **rocky regime of `planetary-dynamo-scaling.md`** …, the giant `B ∝ L^(1/6)` law does **not** apply to rock."(`heat:370-375`) | 간선 note 가 요구하는 "핵이 지금도 대류하는가는 열진화 모형이 필요하다"를 문서가 정확히 그 말로 적는 자리이고, 소비처(dynamo_rocky)를 이름으로 지목합니다 |
| `795` (outgassing → atmosphere_choice) | `**mantle convection → volcanism → outgassing.**` — "The interior heat budget governs whether the body is volcanically active, which sets the **outgassing supply** that feeds **Gate 3** of `exoplanet-atmosphere-methodology.md` (a dead, cold interior cannot resupply a secondary atmosphere)."(`heat:376-379`) | payload(outgassing)와 소비처(atmosphere_choice = 그 문서의 Gate 3)를 둘 다 이름으로 적습니다 |
| `824` (star_metallicity → internal_heat_nontidal) | `Spiegel, Burrows & Milsom 2011 pinned the deuterium-burning mass limit` (`heat:422`). ⚠ 대안 후보 하나: `**Composition matters.** Helium rain (Saturn-type, §6) and **metallicity** (deuterium-burning limit, §6) move `L_int` by tens of percent to factors … default to the solar-composition track and **flag the omission**.`(`heat:525-528`) | 도입 시점 원본은 Spiegel 문장이고, 그것이 metallicity ↔ 중수소 연소 한계의 출처입니다. 다만 **`:525-528` 쪽이 간선의 `status: gap` 을 더 직접 설명합니다**("per-body 로 큐레이션하지 않고 태양조성 트랙을 기본으로 두고 누락을 표시한다") — 어느 쪽을 앵커로 할지는 판단 사항이라 둘 다 올립니다 |

⚠ **제 이전 보고 한 줄 정정.** `REF-DRIFT-b29b556e.md` 에서 "커밋 전에는 23개 모두 맞았고"라고 썼는데,
정확히는 "**커밋 전 각 ref 가 가리켰던 줄과 지금 가리키는 줄이 shift 만큼만 다르다**"입니다. 이 세 개는
b29b556e **이전에도** 의도 문장이 아니라 목차·괘선을 가리키고 있었고, 그 사실은 같은 보고의 뒤쪽 문단과
후속 검증 메시지에 별도로 적어 뒀습니다. 위 표가 그 "왜"를 이제 채웁니다 — 원인은 `08f25e64`(08-24) 이후의
문서 성장입니다.
