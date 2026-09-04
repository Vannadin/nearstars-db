<!-- C30 이오 앵커 근거 — 문서 인쇄 입력으로 Ė 9.343e13 W·F 2.24 W/m² 재현, 두 플럭스 앵커의 출처 차이, §6.1/§6.2 라벨 표 전사, heat_transport_mode 노드 상태. 병렬석 기록, 원문 무편집 + 작업석 재실행 절 -->
<!-- Landed 2026-09-04 from the parallel seat's scratch (IO-ANCHOR.md, 19:34:31 KST), body unedited. The work seat re-ran io_anchor.py and appends the script and its output as a dated section at the end. -->

# C30 자기대조 근거 — 이오 앵커·레짐표·노드
Parallel seat, 2026-09-04. 스크립트 `io_anchor.py`. 읽기 전용, 레포 쓰기 없음.
판단 없이 인쇄값과 계산값만. 문서는 워크트리 사본
(`/Users/vana/Desktop/NearStars-wt/engine-prototype/docs/reference/tidal-heating-methodology.md`, 799행).
아래 본문은 2026-09-04 에 nearstars-77 로 보낸 메시지 그대로입니다.

# 1. 이오 앵커 입력 — 인쇄된 값

| 양 | 인쇄된 값 (표기 그대로) | 자리 |
|---|---|---|
| a | `~5.9 R_J` | `tidal:100` |
| a | `a = 421,700 km` `(~5.9 R_J)` | `tidal:479-480` |
| e | `~0.0041` (forced) | `tidal:100` |
| e | `e = 0.0041` (Laplace-maintained) | `tidal:479-480` |
| k₂/Q | `k₂/Q ~ 0.015 (k₂≈0.3, Q≈20)` | `tidal:100` |
| k₂/Q | rocky `k₂/Q ≈ 0.015` | `tidal:480` |
| R | `R = 1822 km` | `tidal:479` |
| M_p | `M_p = M_Jupiter` (수치는 인쇄되지 않음) | `tidal:479` |
| **m (이오 질량)** | **인쇄 없음** — 식이 `m ≪ M_p` 를 쓰므로(`:58`) 문서 어디에도 없습니다 | — |
| 관측 Ė | `~0.6–1.6 ×10¹⁴ W` | `tidal:100` |
| 관측 Ė | `at ~10¹⁴ W` | `tidal:105`, `:109`, `:481` |
| 관측 flux | `~2 W/m² (global)` | `tidal:100` |
| 관측 flux | `a surface flux ~2 W/m², an order of magnitude above Earth's ~0.08 W/m²` | `tidal:105` |
| 관측 flux | `Io (~2 W/m²)` (레짐표 anchor 열) | `tidal:248` |
| 관측 flux | `F ~ 2 W/m², matching Veeder+ 2012` | `tidal:481` |
| **2.5 W/m²** | `**Heat pipe** … ≥ ~2.5 W/m², no firm upper bound` (수송 용량 문턱) | `tidal:281` |
| **2.5 W/m²** | `On a body radiating 2.5 W/m² on average, the plains are cold.` | `tidal:350-351` |
| **2.5 W/m²** | `2.5 W/m² through ~0.05 % of its area needs 5.0 kW/m², i.e. **545 K**` | `tidal:427` |
| **2.5 W/m²** | `At the 2.5 W/m² printed beside it, Io's actual surface area gives **104 TW** — reproduced here … 2.5 W/m² itself agrees with Io's measured output.` | `tidal:620-623` |

⚠ **두 플럭스 수의 출처가 다릅니다.** `~2 W/m²`는 문서가 Veeder 계열 관측에 붙이는 값(`:100`·`:105`·`:248`·`:481`)이고,
`2.5 W/m²`는 **Kankanamge & Moore 2019 가 인쇄한 값**으로 문서가 `:620-623` 에서 그 출처를 명시합니다
("At the 2.5 W/m² printed beside it"). `:281` 의 heat-pipe 용량 문턱도 그 논문(`2019JGRE..124..114K`)에 달려 있습니다.

**논문 HELD 상태** (`check_paper_held.py` + `ls` 전수 대조 — 서술형·밑줄 파일명까지 확인)

| bibcode | 논문 | 판정 |
|---|---|---|
| `2019JGRE..124..114K` | Kankanamge & Moore 2019 (2.5 W/m² 의 출처) | **HELD** (`2019JGRE..124..114K.pdf`) |
| `1994JGR....9917095V` | Veeder+ 1994 | **ABSENT** (`ls` 에 veeder 히트 0) |
| `2012Icar..219..701V` | Veeder+ 2012 (`~2 W/m²` 의 출처) | **ABSENT** |
| `2009Natur.459..957L` | Lainey+ 2009 (천체측량 소산 확인) | **ABSENT** |
| `2004Icar..169..127R` | Rathbun+ 2004 (핫스팟 사이 <1 W/m²) | **ABSENT** |
| `2003JGRE..108.5096M` | Moore 2003 | **ABSENT** |
| `1998JGR...10313643R` | Reese, Solomatov & Moresi 1998 | **ABSENT** |

즉 **이오 플럭스 앵커 `~2 W/m²` 의 출처 논문(Veeder+ 2012)은 보유하지 않고, `2.5 W/m²` 의 출처 논문은 보유합니다.**
(arXiv 로 인용된 것들은 보유: `2310.12382`·`2405.19253`·`0912.1907`·`2305.03410`, 그리고 `2021PSJ.....2..119R.pdf`.)

## ≈1.016e14 W 가 어느 값에 해당하는가

문서 §7 인쇄 입력을 그대로 식에 넣으면
(G = 6.67430e-11 CODATA 2018, M_J = 1.89813e27 kg IAU 2015 B3 nominal, R_J = 71 492 km):

    a/R_J = 5.8986  (문서 인쇄 '~5.9 R_J')
    n = 4.110176e-05 rad/s -> P_orb = 1.76932 d  (이오 실측 1.769 d)
    Edot = 9.3430e+13 W
    F    = 2.2396 W/m2

| 대조 대상 | 비율 |
|---|---|
| 인쇄 관측대 `~0.6–1.6e14 W` | 하한의 1.557× · 상한의 0.584× — **밴드 안** |
| `~10¹⁴ W` (`:105`·`:109`·`:481`) | 0.934× |
| `~2 W/m²` | 1.120× |
| `2.5 W/m²` | 0.896× |

그리고 **앞선 보고에서 Dante 두 행(`tidal:451`/`:453`)에서 역산한 ≈1.016e14 W 는 R = 1822 km 에서
F = 2.4365 W/m² 에 해당합니다** — 즉 인쇄된 두 플럭스 중 **2.5 W/m² 쪽**입니다
(2.5 → Ė 1.0429e14 W, 비율 0.974). `~2 W/m²` 쪽은 Ė 8.3433e13 W 여서 1.22× 어긋납니다.
참고로 1.016e14 는 인쇄 관측대 0.6–1.6e14 의 42 % 지점입니다.

# 2. §6.1 레짐 표 — 축자 전사 (`tidal:241-251`)

    :241  ### 6.1 The flux → regime table
    :243  Convert `Ė` to a **surface heat flux** `F = Ė / (4πR²)` and compare to thresholds
    :244  (these are guides, not sharp lines):
    :246  | Surface flux F | regime | analog |
    :247  |---|---|---|
    :248  | ≳ 1 W/m² | vigorous silicate volcanism, possible magma ocean | Io (~2 W/m²) |
    :249  | ~0.1–1 W/m² | active resurfacing, episodic volcanism | active icy/rocky worlds |
    :250  | ~0.01–0.1 W/m² | enough to maintain a subsurface ocean under an ice shell | Enceladus SPT, Europa |
    :251  | ≲ 10⁻³ W/m² | geologically dead; no ocean, no plumes from tides alone | far/airless moons |

라벨 문자열 넷(그대로): `vigorous silicate volcanism, possible magma ocean` /
`active resurfacing, episodic volcanism` /
`enough to maintain a subsurface ocean under an ice shell` /
`geologically dead; no ocean, no plumes from tides alone`.
⚠ **0.001 과 0.01 사이(10⁻³ ~ 10⁻²)는 표에 행이 없습니다** — `≲ 10⁻³` 과 `~0.01–0.1` 사이가 비어 있습니다.

`tidal:436-438` 축자:

    :436  melt fraction above ~0.45 — itself disputed (0.30 / 0.45 / 0.50), and there is **no
    :437  published W/m² boundary** between the modes, because the real criterion is melt
    :438  fraction and any flux threshold is a conversion, not a citation.

참고로 §6.2 의 **수송 모드** 표(`tidal:277-281`)는 이것과 별개의 세 라벨입니다 —
`**Plate tectonics**` (~0.09 W/m²; Earth **92.1 mW/m²**, 47±2 TW / 38,347 measurements, `2010SolE....1....5D`) ·
`**Stagnant lid**` (ceiling **10–30 mW/m²**; Venus 10–20, Mars 15–30, `1998JGR...10313643R`) ·
`**Heat pipe**` (≥ ~2.5 W/m², no firm upper bound; Io, early Earth, `2019JGRE..124..114K`).
chain 의 `outputs: [mode, …]` 가 어느 쪽 라벨 집합을 뜻하는지는 노드 정의에 적혀 있지 않습니다.

# 3. `heat_transport_mode` 노드와 간선 전부

노드 (`engine/chain.yaml:402-408`), 축자:

    heat_transport_mode:
      layer: "3층. 갈래"
      domain: tidal
      kind: computed
      recipe: tidal-heating-methodology
      outputs: [mode, resurfacing_rate]
      note: 내부 열이 표면까지 어떻게 나오는가. 별빛 열의 재분배는 day_night_contrast 다.

⚠ recipe **키는 있고**, `registry.registered()` 에는 없습니다(11개 목록에 `heat_transport_mode` 부재).

**들어가는 간선 4개**

| 줄 | 간선 | ref | status |
|---|---|---|---|
| `:631` | `tidal_heating → heat_transport_mode, requires, via: surface_flux` | `tidal-heating-methodology.md:273` | (없음) |
| `:632` | `internal_heat_nontidal → heat_transport_mode, requires, via: mantle_radiogenic_power` | `…:266` | (없음) |
| `:633` | `global_fluid_layer → heat_transport_mode, selects` | `…:332` | (없음) |
| `:634` | `t_eq_stellar → heat_transport_mode, requires` | `…:341` | (없음) |

**나가는 간선 3개**

| 줄 | 간선 | ref | status |
|---|---|---|---|
| `:686` | `heat_transport_mode → dynamo_rocky, selects, via: cmb_heat_flux` | `rocky-planet-dynamo-methodology.md:113` | **gap** — note 에 "this edge's from-node heat_transport_mode still has no recipe" |
| `:808` | `heat_transport_mode → moon_energy_budget, selects` | `moon-energy-budget-methodology.md:132` | (없음) |
| `:897` | `heat_transport_mode → surface_albedo, excludes` | `surface-color-albedo-methodology.md:191` | (없음), note "화산 재표면화 → 알베도는 어느 문서도 서술하지 않는다" |

⚠ `:631`·`:632` 는 둘 다 `requires` 인데 하나는 조석 플럭스(W/m²), 하나는 맨틀 방사성 **출력**(W)입니다 —
단위가 다른 두 양이 같은 kind 로 들어옵니다. 그리고 `:633` 의 공급자 `global_fluid_layer` 는
recipe 없는 7노드 중 하나입니다.

⚠ 워크트리 상태(작성 시점): 작업석 미커밋 변경(C28)이
`engine/chain.yaml`·`dynamo_rocky.py`·`interior-core.md`·`test_dynamo_rocky.py` 에 있었습니다.
이 보고에서 인용한 chain 줄(`:402-408`·`:631-634`·`:686`·`:808`·`:897`)은 그 diff 이후에 다시 찍어 확인했고,
`docs/reference/*` 는 diff 밖입니다.

---

## Appendix (work seat, 2026-09-04 19:40 KST) — `io_anchor.py` re-run, script and output verbatim

```python
# 이오 앵커: 문서 §7 인쇄 입력으로 Ė·F 를 내고 인쇄값들과 대조 — 스크래치 전용
import math
G = 6.67430e-11          # CODATA 2018
M_JUP = 1.89813e27       # kg, IAU 2015 B3 nominal Jupiter mass (nominal GM_J 1.2668653e17 / G)
R_JUP = 71_492e3         # m, IAU 2015 B3 nominal equatorial Jupiter radius
R_IO = 1822e3            # m, tidal:479 "R = 1822 km"
A_IO = 421_700e3         # m, tidal:479 "a = 421,700 km"
E_IO = 0.0041            # tidal:100 / :479
KQ = 0.015               # tidal:100 / :479

n = math.sqrt(G*M_JUP/A_IO**3)
E = 10.5*KQ*G*M_JUP**2*R_IO**5*n*E_IO**2/A_IO**6
F = E/(4*math.pi*R_IO**2)
print(f"M_J = {M_JUP:.6e} kg (IAU 2015 B3 nominal); R_J = {R_JUP/1e3:,.0f} km")
print(f"a/R_J = {A_IO/R_JUP:.4f}   (doc prints '~5.9 R_J')")
print(f"n = {n:.6e} rad/s -> P_orb = {2*math.pi/n/86400:.5f} d   (Io's observed 1.769 d)")
print(f"Edot = {E:.4e} W")
print(f"F    = {F:.4f} W/m2")
print()
print("against the doc's printed numbers:")
print(f"  observed range ~0.6-1.6e14 W  -> ours / 0.6e14 = {E/0.6e14:.3f} ; / 1.0e14 = {E/1.0e14:.3f} ; / 1.6e14 = {E/1.6e14:.3f}")
print(f"  '~10^14 W' (:105, :109, :481)  -> ours = {E/1e14:.3f} x 1e14")
print(f"  '~2 W/m2 (global)' (:100, :105, :248, :481) -> ours/2.0 = {F/2.0:.3f}")
print(f"  '2.5 W/m2' (:281, :350, :427, :620) -> ours/2.5 = {F/2.5:.3f}")
print()
print("what Edot the two printed fluxes imply at R = 1822 km:")
for f0 in (2.0, 2.5):
    print(f"  F = {f0} W/m2 -> Edot = {f0*4*math.pi*R_IO**2:.4e} W")
print()
print("the 1.016e14 W recovered from the doc's Dante rows (tidal:451/453):")
print(f"  as a flux at R = 1822 km: {1.0164e14/(4*math.pi*R_IO**2):.4f} W/m2")
print(f"  vs the printed observed band 0.6-1.6e14: sits at {(1.0164-0.6)/(1.6-0.6)*100:.0f}% of the way up")
```

```
M_J = 1.898130e+27 kg (IAU 2015 B3 nominal); R_J = 71,492 km
a/R_J = 5.8986   (doc prints '~5.9 R_J')
n = 4.110176e-05 rad/s -> P_orb = 1.76932 d   (Io's observed 1.769 d)
Edot = 9.3430e+13 W
F    = 2.2396 W/m2

against the doc's printed numbers:
  observed range ~0.6-1.6e14 W  -> ours / 0.6e14 = 1.557 ; / 1.0e14 = 0.934 ; / 1.6e14 = 0.584
  '~10^14 W' (:105, :109, :481)  -> ours = 0.934 x 1e14
  '~2 W/m2 (global)' (:100, :105, :248, :481) -> ours/2.0 = 1.120
  '2.5 W/m2' (:281, :350, :427, :620) -> ours/2.5 = 0.896

what Edot the two printed fluxes imply at R = 1822 km:
  F = 2.0 W/m2 -> Edot = 8.3433e+13 W
  F = 2.5 W/m2 -> Edot = 1.0429e+14 W

the 1.016e14 W recovered from the doc's Dante rows (tidal:451/453):
  as a flux at R = 1822 km: 2.4365 W/m2
  vs the printed observed band 0.6-1.6e14: sits at 42% of the way up
```
