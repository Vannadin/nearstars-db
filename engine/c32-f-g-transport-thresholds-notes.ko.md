<!-- 병렬석 조사 기록 (원문 무편집). C32 facets F and G: what the heat-transport table is fed, and where its thresholds come from. -->
<!-- Preserved verbatim from the parallel seat's scratch on 2026-09-05, so it stays Korean and keeps its
     numbers, quotations and tables exactly as measured; the .ko.md name declares that (check_language.py).
     C32 facets F and G: what the heat-transport table is fed, and where its thresholds come from. -->
# C32 발주 F·G — §6.2 표의 "양이 다르다" 문제, 그리고 문턱 세 수의 근거
Parallel seat, 2026-09-05. 엔진 워크트리 HEAD `a01d7277`, 읽기 전용, 레포 쓰기 없음.
`tidal` = `docs/reference/tidal-heating-methodology.md`, `heat` =
`docs/reference/internal-heat-luminosity-methodology.md`.
코드 문턱은 지시대로 **0.135(= 0.09 × 1.5)** 기준으로 계산했습니다(docstring `:80` 의 "0.09 and 2.5"
와 어긋나는 것은 작업석 수리 발주 건).

현재 `engine/tidal_heating.py:78-88` 의 판정선:
`heat pipe ≥ 2.5` · `stagnant lid ≤ 0.03` · `plate tectonics ≤ 0.135` · 그 사이 `unclassified`.

# F-a. 경계에 걸리는 바디 전수 — **Venus 하나가 갈립니다**

대조군은 문서 자신이 §6.2 앵커로 인쇄한 천체(`tidal:297-299`)이고, 질량·반지름은 레포 안의
`engine/test_body_class.py:29-38` (`SOLAR_SYSTEM`, "반지름은 Archinal+ 2011 Table 4 의 km 를
6371.00 km 로 나눈 값")에서 읽었습니다. 엔진 값은 `radiogenic.budget()` 을 그 질량·반지름에 돌린
방사성-단독 플럭스입니다.

⚠ **제 가정 하나를 이름 붙입니다**: CMF 를 모든 바디에서 지구의 선언값 **0.325** 로 고정했습니다
(레포에 태양계 바디별 CMF 표가 없습니다). CMF 는 규산염 질량 `M(1−CMF)` 로만 들어가므로 효과가
단조적이고, 아래 Venus 행에 민감도를 함께 붙였습니다.

| 바디 | M/M⊕ | R/R⊕ | 방사성 TW | **엔진 mW/m²** | **엔진 라벨** | **문서 인쇄 측정치 mW/m²** | **문서 행** | 갈림 |
|---|---|---|---|---|---|---|---|---|
| Mercury | 0.0553 | 0.3829 | 1.18 | **15.75** | stagnant lid | ~5 (측정 없음) | stagnant lid | 같음 |
| **Venus** | 0.8150 | 0.9499 | 17.37 | **37.75** | **plate tectonics** | **10–20** (`tidal:298`) | **stagnant lid** | ⚠ **갈림** |
| Earth | 1.0000 | 1.0000 | 21.32 | **41.80** | plate tectonics | **92.1** (`tidal:297`) | plate tectonics | 같음(값은 **2.20×** 차) |
| Mars | 0.1074 | 0.5320 | 2.29 | **15.87** | stagnant lid | 15–30 (`tidal:298`) | stagnant lid | 같음 |

**Venus 가 유일한 갈림이고, 하필 문서 자신의 정체뚜껑 대표 바디입니다.** 그리고 견고합니다 —

| Venus CMF | 엔진 mW/m² | 라벨 |
|---|---|---|
| 0.200 | 44.74 | plate tectonics |
| 0.280 | 40.27 | plate tectonics |
| **0.325** (지구 선언값) | **37.75** | **plate tectonics** |
| 0.400 | 33.56 | plate tectonics |
| 0.500 | 27.96 | stagnant lid |

이분법으로 뒤집히는 지점은 **CMF = 0.4636** 입니다. 즉 Venus 를 정체뚜껑으로 만들려면 규산염 질량을
지구보다 훨씬 작게 잡아야 하고, 문헌의 Venus CMF(~0.31)나 지구 선언값(0.325)에서는 엔진이 **판구조**
라벨을 냅니다. 문서의 측정 앵커(10–20 mW/m²)와 엔진의 방사성-단독(37.75)은 **~2–3.8×** 벌어져 있고,
그 간극이 정확히 0.03 W/m² 문턱을 가로지릅니다.

## 로스터 쪽
| 바디 | 조석 W/m² | 방사성 W/m² | 비 | 총합 라벨 | 조석만 | 방사성만 |
|---|---|---|---|---|---|---|
| **Pandora** | 45.3304 | 0.033385 | **1358×** | heat pipe | heat pipe | **plate tectonics** |
| **Earth** | 조석 없음(cannot-say, no orbit) | 0.041796 | — | plate tectonics | — | plate tectonics |

Pandora 의 판정은 조석 지배로 안전합니다. ⚠ 다만 **Pandora 의 방사성 항 0.033385 W/m² 자체가
0.03 문턱 위 11 % 에 앉아 있습니다** — 조석을 끄면 그 한 항이 stagnant/plate 경계를 11 % 차로 넘습니다.
로스터의 다른 셋(alpha_centauri_a_b, luhman_16_a/b)은 암석 갈래가 아니라 이 표에 오지 않습니다.

**F-a 답: 갈리는 바디는 Venus 하나. 엔진 37.75 mW/m²(plate) vs 문서 앵커 10–20 mW/m²(stagnant lid).**

# F-b. 표에 먹여야 할 양은 셋 중 어느 것인가 — **문서는 정하지 않습니다**

Earth 에서 네 수가 다 다릅니다(전부 실행값):

| 후보 | Earth 값 | `transport_mode()` 결과 | 정체 |
|---|---|---|---|
| 문서의 **측정 표면 열류** (`tidal:297`) | **0.0921 W/m²** | plate tectonics | 47±2 TW / 38,347 측정, `2010SolE....1....5D` (`tidal:744` 재확인) |
| 엔진 **`radiogenic_heat_w_m2`** — **코드가 지금 먹이는 것** | **0.0418 W/m²** | plate tectonics | 방사성 단독. 실행 확인: `heat_transport_mode mode=plate tectonics, total_surface_flux=0.0418 W/m²` |
| 엔진 **`implied_surface_heat_flux`** | **0.0769 W/m²** | plate tectonics | `heat:65-69` — Nimmo+ 2004 eqs 34–36 을 **선언된** `potential_temperature` 에서 평가, 그리고 그 문장이 "**never the body's actual heat flux**" 라고 못 박습니다 |
| 문서 §6.1 자신이 쓰는 수 (`tidal:284`) | **~0.08 W/m²** | plate tectonics | "For an Earth-mass body radiogenic heating alone is ~0.08 W/m²". `heat:59-60` 이 그 0.08 의 정체를 밝힙니다 — "§1's ≈ 35 K uses the **total 0.087 W/m², radiogenic + secular**" |

**Earth 에서 최대·최소 비 = 0.0921 / 0.0418 = 2.20×.** 네 개가 다 plate 로 떨어지는 것은
`0.135` 상한이 넉넉하기 때문이고, 0.03 경계에서는 이 2.20× 가 라벨을 가릅니다(= Venus).

**문서가 어디서도 "어느 양"인지 정하지 않습니다.** 인용으로:
- `tidal:261` (§6.1) — "Convert `Ė` to a **surface heat flux** `F = Ė / (4πR²)`" → 여기서 F 는 **조석**
  플럭스입니다.
- `tidal:284-286` (§6.1 말미) — "tidal heating is one heat source among several (radiogenic, accretional,
  primordial). For an Earth-mass body radiogenic heating alone is ~0.08 W/m²; **tidal heating matters when
  it *exceeds* that**." → 문서는 두 항을 **비교**하고 **더하지 않습니다.**
- `tidal:295-299` (§6.2 표) — 열 이름이 **Capacity** 와 **Anchor body** 이고, 앵커 칸의 수는 전부
  **측정 표면 열류**(Earth 92.1 mW/m², Venus 10–20, Mars 15–30)입니다. 표는 "이 모드가 실어낼 수 있는
  용량"과 "그 모드에 있는 실제 천체의 측정 열류"를 나란히 두고, **입력이 무엇인지는 말하지 않습니다.**
- `tidal:291-293` — "Which one the body is in is set by **the flux itself**" → 정관사만 있고 정의가 없습니다.
- ⚠ **"total surface flux" 라고 적는 유일한 문장은 `b29b556e` 가 새로 넣은 계약 블록입니다** —
  `tidal:59` "the §6.2 table … read on the **total surface flux** (tidal + radiogenic/4πR²)". 즉 그 선택은
  **§6 의 진술이 아니라 레시피 자신의 선언**이고, 계약 블록이 문서에 들어간 날짜가 곧 그 선택의 날짜입니다.
- `tidal:454-456` — "there is **no published W/m² boundary** between the modes, because the real criterion is
  **melt fraction** and any flux threshold is a **conversion, not a citation**."

**F-b 답: 문서는 정하지 않습니다.** §6.1 은 조석 F 를, §6.2 의 앵커 칸은 측정 표면 열류를, §6.1 말미는
총 내부열(~0.08)을 쓰고, "총합"이라는 지시는 레시피 계약 블록에만 있습니다. `implied_surface_heat_flux`
는 그 자신의 정의 문장이 "actual heat flux 가 아니다"라고 배제합니다.

# G. 문턱 세(네) 수의 근거

| 수 | 코드 위치 | 문서 근거 | 판정 |
|---|---|---|---|
| **2.5 W/m²** (heat pipe 하한) | `tidal_heating.py:41` `IO_FLUX_KM2019_W_M2`, `:81-82` | ✅ `tidal:299` — "\| **Heat pipe** \| melt migrates through the lid and erupts \| **≥ ~2.5 W/m², no firm upper bound** \| Io; early Earth ([`2019JGRE..124..114K`] (…)) \|". 논문 **HELD**(제 `IO-ANCHOR.md`) | **근거 있음** — 단 **한쪽 경계**("no firm upper bound") |
| **0.03 W/m²** (stagnant lid 상한) | `tidal_heating.py:83` | ✅ `tidal:298` — "\| **Stagnant lid** \| conduction through an immobile lid \| ceiling **10–30 mW/m²** \| Venus 10–20, Mars 15–30 ([`1998JGR...10313643R`] (…)) \|". ⚠ 코드는 그 **밴드의 위쪽 끝만** 씁니다 — 아래 끝 **10 mW/m² 는 코드에서 쓰이지 않습니다**. Reese+ 1998 은 **ABSENT**(제 `IO-ANCHOR.md` 스윕) | **근거 있음, 인쇄된 밴드가 이미 있음** (10–30) |
| **0.09 W/m²** (plate tectonics 용량) | `tidal_heating.py:85` (기준값) | ✅ `tidal:297` — "\| **Plate tectonics** \| the lid itself is recycled \| **~0.09 W/m²** \| Earth, **92.1 mW/m²** (47±2 TW from 38,347 measurements, [`2010SolE....1....5D`] (…)) \|" | **근거 있음** — 단 **폭 없음**(용량 한 점 + 앵커 한 바디) |
| **×1.5 → 0.135** (plate 상한) | `tidal_heating.py:85` `0.09 * 1.5`, 주석 "the plate-tectonics anchor is one body, 92.1 mW/m²; **read ±50 % as its row**" | ❌ **없음.** `grep "50 %\|±50\|50%\|factor of 1.5\|×1.5\|1.5×"` 로 문서를 훑으면 히트가 둘인데 **둘 다 다른 양**입니다 — `tidal:374` "**50 % of the heat flow comes from 1.2 % of the surface**"(이오의 열 집중, `2012Icar..219..701V`)와 `tidal:752` 의 같은 인용. ±50 % 라는 폭은 문서 어디에도 없습니다 | **없음 → authored** |

그리고 문턱 전체에 대한 문서 자신의 유보가 있습니다 — `tidal:454-456` "**no published W/m² boundary**
between the modes … any flux threshold is a **conversion, not a citation**". 즉 세 수는 각 모드의
*용량/앵커*로는 인쇄돼 있지만, **모드 사이의 경계로는 문서가 스스로 근거를 부인합니다.**

## C32 밴드 후보로서의 성질 (한 줄씩)
- **0.03**: 밴드가 **이미 인쇄돼 있습니다**(10–30 mW/m²). 지금 상단만 쓰므로, 밴드화가 가장 값싼 곳 —
  10 과 30 을 두 끝으로 그대로 쓰면 새 authored 가 늘지 않습니다.
- **2.5**: 한쪽 경계만 인쇄("no firm upper bound"). 밴드로 만들려면 아래쪽 폭을 authored 로 만들어야 합니다.
- **0.09 / 0.135**: 용량 0.09 는 인쇄, **폭 ×1.5 는 없음**. 이 자리가 G 에서 유일하게 새 authored 를
  요구하는 곳입니다. 앵커가 한 바디(Earth 92.1 mW/m²)뿐이라 폭의 재료가 문서에 없습니다.
- 그리고 F-b 때문에, 문턱을 밴드로 만들더라도 **먹이는 양을 먼저 고정하지 않으면** Venus 급 갈림은
  남습니다 — 0.0418 / 0.0769 / 0.0921 의 2.20× 가 어떤 폭보다 큽니다.
