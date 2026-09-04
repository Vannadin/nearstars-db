<!-- 병렬석 조사 기록 (원문 무편집). C33 batch H: anchor phrases for the ten refs that were already wrong, and the heat:119 census. -->
<!-- Preserved verbatim from the parallel seat's scratch on 2026-09-05, so it stays Korean and keeps its
     numbers, quotations and tables exactly as measured; the .ko.md name declares that (check_language.py).
     C33 batch H: anchor phrases for the ten refs that were already wrong, and the heat:119 census. -->
# H — 이미 어긋나 있던 ref 열 개의 앵커 구절, + heat:119 의 30군데 점검
Parallel seat, 2026-09-05. 엔진 워크트리 HEAD `a01d7277`, 읽기 전용, 레포 쓰기 없음.
`heat` = `docs/reference/internal-heat-luminosity-methodology.md`,
`tidal` = `docs/reference/tidal-heating-methodology.md`.

## 방법 (재현용)
각 ref 의 **한 홉 앞 값**(`0ace3863` 이 heat 에 +1, `b29b556e` 가 tidal 에 +18 을 넣었으므로 heat 는
n−1, tidal 은 n−18)을 `git log -S` 로 도입 커밋까지 되짚어, **그 커밋의 그 줄 원문**을 꺼내고, 그 원문을
현재 문서에서 **축자 일치**로 찾았습니다. 열 개 전부 도입 커밋이 **`08f25e64` (2026-08-24)** 이고, 그때는
**전부 정확했습니다.** 지휘석이 찍은 표본 다섯(heat:61→223, 188→350, 309→484, 473→648,
tidal:735→795)과 제 결과가 전부 일치합니다.

⚠ **감사석 지적을 논리까지 적어 둡니다** — 제 `REF-DRIFT-b29b556e.md` 의 `old[n] == cur[shift(n)]`
검사는 **시프트가 충실한지만** 증명하고 **ref 가 애초에 옳았는지는 증명하지 못합니다.** 문서가 균일하게
밀렸으면 그 등식은 임의의 n 에서 성립하기 때문입니다(전사 오류가 없다는 것과, 가리키는 곳이 옳다는 것은
다른 명제입니다). ref 가 옳았는지를 묻는 검사는 **도입 커밋으로 되짚어 그때의 원문을 보는 것**이고,
그것이 이 노트의 방법입니다. 다음 세션이 같은 검사를 재발명하지 않게 여기 적습니다.

## H-1. 열 개의 앵커 구절

`uniq` = 그 구절이 현재 문서에서 **몇 줄에** 나오는가(전부 1 = 유일). `§` = 그 줄이 속한 절.

| chain 줄 | 간선 | 현재 ref | **정답 줄** | 시프트 | 앵커 구절 (uniq=1) | § |
|---|---|---|---|---|---|---|
| `837`·`838` | `internal_heat_nontidal → t_eff_body via t_int` · `t_eq_stellar → t_eff_body` | `heat:61` | **`heat:223`** | +163 | `` ⇒  T_eff⁴  =  T_eq⁴  +  T_int⁴ `` (⚠ 이중 공백 포함 — 절 제목의 단일 공백판과 구별됨) | `## 1. The relation: T_eff⁴ = T_eq⁴ + T_int⁴` |
| `823` | `body_class → internal_heat_nontidal, selects` | `heat:188` | **`heat:350`** | +163 | `The body class decides which mechanism dominates` | `## 5. Domain of validity: internal heat by body class` |
| `689` | `internal_heat_nontidal → dynamo_rocky via geotherm` (gap) | `heat:203` | **`heat:370`** | +168 | `core convection → a dynamo magnetic field` | `## 5. …` |
| `795` | `internal_heat_nontidal → atmosphere_choice via outgassing` (gap) | `heat:209` | **`heat:376`** | +168 | `mantle convection → volcanism → outgassing` | `## 5. …` |
| `824` | `star_metallicity → internal_heat_nontidal, influences` (gap) | `heat:255` | **`heat:422`** | +168 | `Spiegel, Burrows & Milsom 2011 pinned the deuterium-burning mass limit` | `## 6. Helium rain and deuterium burning: the extra terms` |
| `896` | `internal_heat_nontidal → t_eff_body, excludes, scope: self` | `heat:309` | **`heat:484`** | +176 | ⚠ 원래 후보 `(0.087/σ)^(1/4) ≈ 35 K` 는 **두 줄(`:362`·`:484`)에 나옵니다.** 유일한 대안 → `` against Earth's `T_eq ≈ 255 K` `` (또는 바로 위 `:483` 의 `Plug the flux into §1:`) | `## 7. Worked examples` |
| `661` | `internal_heat_nontidal → dynamo_giant via l_int` | `heat:473` | **`heat:648`** | +176 | `[planetary-dynamo-scaling](planetary-dynamo-scaling.md)` | `## Related` ⚠ |
| `836` | `internal_heat_nontidal → mass_radius_relation, influences +` | `heat:478` | **`heat:653`** | +176 | `[mass-radius-relation-methodology](mass-radius-relation-methodology.md)` | `## Related` ⚠ |
| `646` | `tidal_heating → ice_stability, requires` | `tidal:735` | **`tidal:795`** | +78 | `` [`ice-stability-methodology.md`](../docs/reference/ice-stability-methodology.md) `` | `## Related` ⚠ |
| `647` | `tidal_heating → crater_state, requires` | `tidal:738` | **`tidal:798`** | +78 | `` [`crater-degradation-methodology.md`](../docs/reference/crater-degradation-methodology.md) `` | `## Related` ⚠ |

시프트가 heat 에서 **163 / 168 / 176** 세 값으로 뭉치고 tidal 은 **78** 하나 — 08-24 이후 문서가
블록 단위로 자란 결과이고, 지휘석이 이미 확인한 그림과 같습니다.

## H-2. 앵커가 원래 의도와 맞는지 (간선별 대조)

여섯 개는 간선의 payload 를 문장이 이름으로 적어 확인이 쉽습니다.
- `heat:223` `⇒ T_eff⁴ = T_eq⁴ + T_int⁴` ↔ `→ t_eff_body via t_int` 및 `t_eq_stellar → t_eff_body`
  — 그 식이 두 간선의 두 항입니다.
- `heat:350` "The body class decides which mechanism dominates and how confident the estimate is" ↔
  `body_class → …, selects`.
- `heat:370` "core convection → a dynamo magnetic field … a **thermal-history question** … the **rocky
  regime of `planetary-dynamo-scaling.md`**" ↔ `→ dynamo_rocky via geotherm`.
- `heat:376` "mantle convection → volcanism → outgassing … the **outgassing supply** that feeds
  **Gate 3** of `exoplanet-atmosphere-methodology.md`" ↔ `→ atmosphere_choice via outgassing`.
- `heat:422` Spiegel+ 2011 의 중수소 연소 질량 한계 ↔ `star_metallicity → …`(금속도 ↔ 중수소 한계).
- `heat:484` "`T_int = (0.087/σ)^(1/4) ≈ 35 K`: against Earth's `T_eq ≈ 255 K` … `≈ 0.001 K`
  correction, i.e. **completely negligible for the surface temperature**" ↔
  `internal_heat_nontidal → t_eff_body, **excludes**, scope: self` — 배제의 근거 문장 그대로입니다.

## H-3. "Related" 넷에 대한 소견 — **§ 로 갈아타는 편이 낫습니다**

`heat:473`·`heat:478`·`tidal:735`·`tidal:738` 네 개는 전부 각 문서의 `## Related` 목록 항목입니다.
지적대로 가장 약한 타깃입니다 — 목록은 형제 문서가 하나 늘 때마다 항목이 끼어들어 **줄이 움직이고**,
자란 폭이 그 목록 자체를 지나가기 때문에 오늘의 176/78 시프트가 정확히 여기서 가장 큽니다.

**소견 셋, 값싼 것부터.**
1. **줄 대신 § 앵커.** `internal-heat-luminosity-methodology.md#related` /
   `tidal-heating-methodology.md#related` — 두 문서 다 `## Related` 라 앵커가 안정적이고
   (`#related`), 링크가 깨졌는지는 dead-link 게이트가 이미 봅니다.
2. **아예 줄을 떼는 것도 정당합니다.** 이 네 간선의 ref 가 실어 오는 정보는 "형제 문서가 이 결합을
   목록에 적어 두었다"뿐이고, **간선 자신이 이미 두 노드를 이름으로 적고 있습니다**(`tidal_heating →
   ice_stability` 등). 즉 줄번호가 없어도 잃는 것이 없습니다. `ref: "tidal-heating-methodology.md"`
   처럼 파일만 남기는 형태.
3. **더 나은 타깃이 있으면 그쪽으로.** 예컨대 `tidal:795-797` 의 Related 항목은 본문에 대응 문장이
   따로 있습니다("the internal flux derived here must be added before judging ice survival"). 본문
   문장이 있는 경우 목록 대신 본문을 가리키는 편이 의미가 더 큽니다 — 다만 그건 항목마다 확인이
   필요해서, 일괄로는 ①/② 를 권합니다.

⚠ 그리고 **나머지 여섯도 줄번호로 다시 박으면 같은 일이 반복됩니다.** 여섯은 앵커 구절이 유일하므로
(위 표 `uniq=1`), 수리 커밋이 `ref: "heat…md:370"` 대신 구절이나 `§5` 를 실을 수 있으면 그쪽이
드리프트에 면역입니다. 형식 결정은 판단 사항이라 제안만 합니다.

## H-4. 덤 — `heat:119` 의 30군데: **6개만 맞고 24개가 틀립니다** (출생부터)

`heat:119` 는 오늘 `**Needs** — mass_earth · core_mass_fraction · core_radius · cmb_pressure …` 이고,
이 줄은 **`core_energy_balance` 계약 블록의 Needs 줄**입니다(블록 제목 `heat:113`). 문서에는 계약 블록이
다섯 개 있습니다.

| 블록 | 제목 | Needs |
|---|---|---|
| `internal_heat_nontidal` | `:37` | **`:47`** |
| `cmb_heat_flux` | `:83` | **`:89`** |
| `core_energy_balance` | `:113` | **`:119`** ← 30군데가 지금 가리키는 곳 |
| `core_entropy_production` | `:146` | **`:152`** |
| `core_thermal_history` | `:183` | **`:189`** |

**각 간선이 추가된 커밋으로 되짚어 그때의 `heat:118` 원문을 확인했습니다** — 이게 "출생 시점에 맞았나"를
가르는 유일한 검사입니다.

| chain 줄 | 소비 노드 | 개수 | 추가 커밋 | 그때 `heat:118` 이었던 것 | 출생 시 | 맞는 타깃 |
|---|---|---|---|---|---|---|
| `706`–`711` | **`core_energy_balance`** | **6** | `3a304019` (09-03) | `**Needs** — mass_earth · core_mass_fraction · core_radius · cmb_pressure …` (= 자기 블록) | ✅ **맞음** | **`:119` 그대로** |
| `699`–`704` | `cmb_heat_flux` | 6 | `b73d7293` (09-03) | **`10. [Related](#related)`** — 목차 줄 | ❌ **출생부터 틀림** | **`:89`** |
| `713`–`717` | `core_entropy_production` | 5 | `ffd9602c` (09-04) | 이웃 블록(`core_energy_balance`)의 Needs | ❌ **출생부터 틀림** | **`:152`** |
| `718`–`726` | `core_thermal_history` | 9 | `d5ac48b7` (09-04) | 같음 — 이웃 블록의 Needs | ❌ **출생부터 틀림** | **`:189`** |
| `818` · `822` · `897` | `internal_heat_nontidal` | 3 | `08f25e64` (08-24) | `'mass is self-luminous** (the directly imaged regime, §3). **Age and mass, not the host**'` | ✅ 그때는 맞음, 지금은 밀림 | `818`·`822` → **`:47`**(자기 Needs) 또는 **`:281-282`**; `897` → **`:281-282`** |
| `821` | `internal_heat_nontidal` | 1 | `fc46d6a3` (09-03) | `Far enough out, the fixed \`T_int\` floor exceeds the vanishing \`T_eq\`.` | ❌ **출생부터 틀림** | **`:47`** |

**합계: 30군데 중 맞는 것은 `core_energy_balance` 로 가는 6개뿐이고, 24개가 틀립니다.** 그중
**20개는 출생부터 틀렸습니다**(`699`–`704`·`713`–`717`·`718`–`726`·`821`), **4개는 08-24 에는 맞았고
문서가 자라며 밀렸습니다**(`818`·`822`·`897` + 그 계열).

⚠ **`897` 이 가장 분명합니다.** 그 간선의 note 는 한글로 "**나이와 질량이 정하지 호스트가 정하지
않는다**" 인데, 도입 시점 `heat:118` 원문이 정확히 그 문장이었습니다. 오늘 그 문장은 **`heat:281-282`**
(`## 2. The cooling track: L_int(M, age) behaviour`)에 있습니다 —

> "an old, low-mass giant has a faint cooling luminosity and is irradiation-dominated (A b, §7), whereas a
> **young giant of any mass is self-luminous** (the directly imaged regime, §3). **Age and mass, not the host
> star, decide which regime a giant is in.**"

앵커 구절: `Age and mass, not the host` (`heat:281`).

**기전** — 값 하나가 여섯 소비처에 재사용되면서, 새 간선을 그릴 때마다 **그 시점에 우연히 `:118` 에 있던
줄**을 물려받았습니다. 09-03·09-04 에 계약 블록이 하나씩 늘 때마다 `:118` 이 다른 블록의 Needs 줄로
바뀌었고, 그래서 다섯 소비처가 **전부 `core_energy_balance` 의 Needs 를 가리키게** 되었습니다.
같은 문서·같은 종류(Needs 줄)라서 읽는 사람이 눈치채기 가장 어려운 형태입니다 — `cmb_heat_flux` 6개가
목차 줄에서 출발한 것과 `821` 이 본문 산문에서 출발한 것만 종류가 달랐습니다.
