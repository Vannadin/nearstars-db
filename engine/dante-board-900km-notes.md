<!-- Dante 보드의 900 km 잔존값 — 조석 행(:1524–1607)은 반지름을 언급하지 않고, 종속 행 목록과 문서의 521 km 대응값을 나란히 놓은 병렬석 기록, 원문 무편집 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (DANTE-BOARD-900KM.md, 19:35:27 KST), body unedited. Board line numbers refer to the engine worktree's phase4/alpha_centauri.yaml (committed state); the main checkout's copy carries uncommitted changes and is the board of record — not touched. Consumed by C30 note 7 and the C31 brief. -->

# Dante 900 km 잔존값 — 어디가 인정하고 어디가 안 하는지
Parallel seat, 2026-09-04. 읽기 전용, 레포 쓰기 없음. 인쇄된 문장만, 판단 없음.
경로는 워크트리(`/Users/vana/Desktop/NearStars-wt/engine-prototype/`) 기준.
아래 본문은 2026-09-04 에 nearstars-77 로 보낸 메시지 그대로입니다.

결론 한 줄 — **인정하는 곳은 반지름 행(`phase4/alpha_centauri.yaml:1473`)과 stability-sim 증거파일
(`:137`·`:141`·`:143`·`:155`)이고, 조석 행(`:1524-1607`) 자체는 900 km 를 한 번도 언급하지 않습니다.**

# 1. `bulk.tidal_heating` 블록(`:1524-1607`) 전문 요지 — 반지름 언급 0회

⚠ **이 블록 84행 안에 "900", "521", "km", "radius" 가 한 번도 나오지 않습니다.** 인쇄된 근거는
반지름이 아니라 궤도·유변 항뿐입니다 — `:1584-1585` evidence:
"Check, heating: **Io scaling (Ė∝M_p^2.5·R^5·e²·a^-7.5) at 1.54 R_p** with the measured e_rms 0.0186
from the stability timeseries (not an assumed mean) and k₂/Q 0.0155."
(`R^5` 는 식 안에만 있고 어느 R 인지는 적히지 않습니다.)

| 자리 | 인쇄된 내용 |
|---|---|
| `:1526-1529` provenance | "2026-07-26: e 가정 평균 0.0175 → 안정성 시계열 측정 e_rms 0.0186. **~820× Io → ~1200× Io, 표면 플럭스 ~11,500 W/m².** 구 행은 이 플럭스를 surface 행의 주변 230 K와 짝지어 에너지 보존을 위반했음…" |
| `:1530-1531` | "2026-08-03: 감사 C5 재마감(오너 결정) — 주변 673 K → 360 K, 발광 영역 973 K → 1350 K(노출 용융부), 면적 5.7%, 전도 지각 0.12 m → ~2.1 m. **플럭스·k₂/Q·조석 배율은 무변경이고 열의 분배만 바뀌었다.**" |
| `:1535-1538` | "2026-08-03: 같은 날 오너 지적으로 다이버전스 노트를 정정 … Veeder 1994는 … **수치 필드는 무변경이고 근거 서술만 정정했다.**" |
| `:1539` | `status: gated  # 2026-06-22 — 아바타 게임 설정+물리 합치` |
| `:1553` | `tidal_heating` = "~1200× Io (simulated e_rms 0.0186, k₂/Q ~0.0155)", note "**The old ~820× assumed e 0.0175**" |
| `:1554` | `tidal_surface_flux` = "~11,500 W/m² (360 K plains; the exposed melt at 1350 K covers ~5.7% of the area)", note "Conductive crust ~2.1 m thick (plains)…" |
| `:1555` refs | `["docs/reference/tidal-heating-methodology.md", "docs/reference/moon-energy-budget-methodology.md", "phase3/stability-sim/STABILITY_REPORT.md", "2012Icar..219..701V", "1994JGR....9917095V"]` — ⚠ **`DANTE_HEAT_TRANSPORT_EVIDENCE.md` 는 refs 에 없습니다**(반지름 행 note 에만 있음) |
| `:1556-1558` gate | criterion `[stability, canon-consistency]`, verdict `documented-divergence` |
| `:1560-1570` divergence_note | "tidal **11,500 W/m²** + starlight 141 W/m² fix the area-weighted radiating mean at **673 K** … NearStars keeps the sulfur and takes the plains to 360 K, which requires **92 %** of the heat to leave through exposed melt at the ~1350 K silicate ceiling over **5.7 %** … the implied conductive lid under our plains is **~2.4 m** where Io's is kilometres." |
| `:1587-1589` evidence | "Check, partition: **952 W/m² over 94.3 %** plus 1350 K melt over 5.7 % reproduces the **11,641 W/m²** total to the digit, so the 673 K area-weighted mean is preserved" |
| `:1592-1593` | "Lid follows the local flux, not the mean: **990 K over 952 W/m² at k ≈ 2 W/m/K**, against 0.12 m for a uniform 673 K surface. Caveat: the partition is the look, not a recipe output" |

**`:1486` 문단(bulk 축, tidal 축이 아님)**: "2026-07-28: internal_heat 에코를 ~820×→~1200× Io로 정정 —
소유 행 bulk.tidal_heating의 2026-07-26 재도출이 이 에코에 전파되지 않고 있었다(감사 C3)."
— 즉 이 정정은 **e 재도출(0.0175→0.0186)의 전파**이고, 반지름과 무관합니다. 그 축의 refs 는
`["docs/reference/body-figure-methodology.md", "docs/reference/tidal-locking-timescale-methodology.md"]` (`:1488`).

# 2. 반지름 행 ↔ 조석 행 상호 언급

| 방향 | 결과 |
|---|---|
| 반지름 행 → 열수송 | **언급합니다.** `:1472-1474` `radius` = 521 km, note: "INVENTED; the surface heat transport gate, **DANTE_HEAT_TRANSPORT_EVIDENCE.md rejected 900 km** — a 5 % melt lake would need 2.1x the observed maximum areal flux". 질량 행도 `:1469-1471` "INVENTED; **sized by the surface heat transport gate**, DANTE_HEAT_TRANSPORT_EVIDENCE.md 가 정함". ⚠ 다만 **`bulk.tidal_heating` 행을 이름으로 부르지는 않습니다** — 증거 파일만 가리킵니다. |
| 조석 행 → 반지름 변경 | **언급하지 않습니다.** `:1524-1607` 어디에도 900/714/521 도, `tidal:449-454`(=증거파일 `:139-144`)의 반지름 표도 나오지 않습니다. |
| 문서 `tidal:445-460` → 보드 | 문서 쪽은 명시합니다 — `:445-447` "**The body was drafted at 900 km, and the transport test is what rejected that.** Holding density at 2,620 kg/m³ and **scaling from the drafted 900 km / 1,200× Io / 11,500 W/m²**". 즉 **문서는 1,200×/11,500 을 "drafted"(초안) 값으로 라벨링하고, 보드의 그 두 필드는 라벨 없이 채택값 자리에 있습니다.** |

# 3. stability-sim(워크트리 커밋 버전)에서 네 수가 함께 나오는 줄

`phase3/stability-sim/DANTE_HEAT_TRANSPORT_EVIDENCE.md`
- `:136-137` — "Density held at 2,620 kg/m³; total output ∝ R⁵, surface flux ∝ R³, both anchored on **the shipped 900 km / 1,200× Io / 11,500 W/m²**." (문서는 같은 자리를 "drafted", 여기서는 "**shipped**" 로 적습니다 — 즉 그때 보드에 실려 있던 값이라는 표기)
- `:141` — `| 900 km (shipped) | 8.0e21 | 1,200× Io | 11,500 W/m² | 230 kW/m² | **2.1× the observed max — impossible** |`
- `:142` — `| 714 km | 3.99e21 | 377× | 5,742 | 114.8 kW/m² | at the record max |`
- `:143` — `| **521 km (chosen)** | **1.552e21** | **78×** | **2,231** | **44.6 kW/m²** | **Erta Ale class — inside the band** |`
- `:144` — `| 450 km | 1.0e21 | 38× | 1,438 | 28.8 kW/m² | Erebus class |`
- `:146-148` — "521 km also sits inside the published super-Io envelope (2,231 < 2,500 W/m²; the envelope caps radius at 541 km), gives an **area-averaged 452 K**, and keeps the plains at **starlight equilibrium 223 K**"
- ⚠ **`:154-155`** — "Hades e_rms 0.033–0.046 and Dante e_rms 0.017–0.022 both bracket the board's existing 0.0385 / 0.0186, **so the tidal-heating rows move because of SIZE, not eccentricity.**" ← 증거 파일이 조석 행이 움직여야 한다고 명시한 문장입니다.
- `:157-158` — "Figure (triaxial, **from the board's J₂ 0.039 / C₂₂ 0.0118, which are radius-independent at fixed density**): a = 549.6 km, b = 512.7, c = 500.7. Relief a−c = **48.9 km**"

`phase3/stability-sim/checklist.md`
- `:128` — `- [x] Dante 521 km chosen (78× Io, 2,231 W/m², 5 % lakes = 44.6 kW/m² = Erta Ale class)`
- `:129` — `- [x] Dynamics at 521 km + combo: **4/4 no moon lost**`
- ⚠ checklist 에 "11,500"·"1200"·"900 km" 는 나오지 않습니다(521 쪽만).

# 4. 900 km 값에 기대는 다른 Dante 행 — 문서의 521 km 대응값과 나란히

| 양 | 보드 값 (줄) | 증거파일/문서의 521 km 대응값 | 비 |
|---|---|---|---|
| 표면 플럭스 | **~11,500 W/m²** (`:1554`) | **2,231 W/m²** (증거 `:143`, `tidal:453`) | 5.155× |
| 조석 배율(출력) | **~1200× Io** (`:1553`, 에코 `:1482`) | **78×** (증거 `:143`, `tidal:453`) | 15.38× |
| 평원 온도 | **360 K** (`:1544`·`:1554`·`:1638`·`:1633`) | **223 K** (별빛 평형, 증거 `:148`, `tidal:460`) | — |
| 면적가중 복사 평균 | **673 K** (`:1560-1562`·`:1587-1588`) | **452 K** (area-averaged, 증거 `:147`, `tidal:459`) | — |
| 용융 면적분율 | **~5.7 %** (`:1554`·`:1583`·`:1638`) | 증거·문서는 **5 % 램프 가정**으로 요구 면적유속을 계산(`:141`·`:143`, "5 %-lake required areal flux") | — |
| 평원 국소 플럭스 | **952 W/m²** over 94.3 % (`:1587`) | (521 km 대응값 인쇄 없음) | — |
| 총합 재현 | **11,641 W/m²** (`:1587`) | (동일, 11,500 계열) | — |
| 전도 지각 두께 | **~2.1 m** (`:1554`·`:1583`) / 노트에 **~2.4 m** (`:1568`) | (521 km 대응값 인쇄 없음) | ⚠ 같은 축 안에서 2.1 과 2.4 두 수 |
| 알베도 근거 | 0.30, "it holds because solid orthorhombic sulfur is the stable phase on the **360 K** plains" (`:1637`) | 223 K 에서도 고체 황은 안정(증거 `:148-150`) | — |
| 발광 판정 | "**360 K** is far below the ~798 K Draper point" (`:1648`) | 223 K 면 더 아래 | — |
| 별빛 항 | starlight **141 W/m²** (`:1560`) | (반지름 무관) | — |

⚠ **그리고 반지름 자체가 한 행에 아직 900 으로 남아 있습니다** — `:1480`
`- { name: geopotential_j2, value: 0.039, **reference_radius_km: 900**, op: set, note: "= 10/3·C̄₂₂, φ0.80" }`,
반면 바로 위 `:1477` 은 `reference_radius, value: 521, unit: km, note: "J₂/C₂₂ reference radius = radius"`.
증거파일 `:157` 은 J₂ 0.039 / C₂₂ 0.0118 이 "**radius-independent at fixed density**" 라고 적습니다.

⚠ 워크트리 상태(작성 시점): 작업석 미커밋 변경(C28)은 `engine/` 안에만 있고, 이 보고가 인용한
`phase4/*`·`phase3/stability-sim/*`·`docs/reference/*` 는 전부 diff 밖(커밋된 상태)입니다.
