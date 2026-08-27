<!-- 핵이 다이나모를 돌릴 수 있는 액체인가 — 핵의 압력·온도를 철의 융해곡선에 대는 방법(논문 근거) -->
# 핵 상태 근거화. 금속 핵이 전도성 액체인가

[내부 구조](interior-structure-methodology.md) 는 핵의 **기하** 를 풉니다. 그 핵이
다이나모를 돌릴 수 있느냐는 별개의 질문이고 문헌도 따로입니다. 암석행성 다이나모 레시피가
요구하는 것은 "convective buoyancy flux through a conducting liquid-iron core" 이고, 여기서
하중을 받는 낱말은 *액체* 입니다. 이 레시피는 핵의 압력과 온도를 철의 융해곡선에 대서 그
질문에 답합니다.

## 계약 — `core_state`

**Returns** — `conductor_phase` [—] · `cmb_melt_temperature` [K] ·
`center_melt_temperature` [K] · `core_cmb_temperature_used` [K] ·
`core_center_temperature_used` [K] · `icb_pressure` [GPa]
**Needs** — `core_pressure` [GPa] · `cmb_pressure` [GPa] · `core_temperature` [K] ·
`cmb_temperature` [K] · `core_material` [—] · `core_cmb_temperature` [K] ·
`body_class` [—]
**분기키** — `core_cmb_temperature` 가 선언됐는가(하한 갈래냐 단열선 갈래냐를 가릅니다),
그리고 중심압(융해곡선의 어느 조각을 쓸지를 가릅니다).
**등급** — 아무리 좋아도 **analog** 이고, 판정이 `undecided` 인 자리에서는 **judgment**
로 내려갑니다. 어느 경로든 이 레시피가 도출할 수 없는 온도에 기댑니다. 선언이 있으면 그
값을 그대로 쓰고, 없으면 다른 레시피의 지오섬을 하한으로 읽습니다.

`conductor_phase` 는 `liquid` · `solid` · `liquid_outer_solid_inner` · `undecided` 중
하나입니다. `icb_pressure` 는 핵 안에 내핵 경계가 없으면 0 입니다.

`core_cmb_temperature` 는 핵-맨틀 경계의 **핵 쪽** 온도이고, `potential_temperature` ·
`initial_porosity` · `envelope_z` 와 같은 뜻의 선언입니다. 그 값을 정하는 것은 D″
열경계층을 가로지르는 열류이고, 그 열류는 `internal_heat_nontidal` 의 출력인데 아직
없습니다. `chain.yaml` 이 그 엣지를 gap 으로 적어 둔 이유가 그것입니다.

## 관계식

곡선 둘, 그리고 판정은 둘이 만나는 자리입니다.

    T_melt(P)                       ← 핵 재료의 융해곡선
    T(P) = T_cmb · (ρ(P)/ρ_cmb)^γ   ← 핵의 단열선. γ 는 상수

γ 가 변하지 않으면 `dT/dP = γT/K_S` 가 이 닫힌 형태가 됩니다. 핵 조건의 철에 대해 그렇다는
것이 아래 ab initio 결과입니다. `T > T_melt` 인 자리는 액체, `T < T_melt` 인 자리는
고체이고, 핵-맨틀 경계와 중심 사이에 교차가 하나 있으면 그게 내핵 경계라 그 압력을
돌려줍니다.

융해곡선이 이 구간 전체에서 단열선보다 가파르므로 교차는 늘 중심 쪽입니다. 결정화가 지구가
그렇듯 중심에서 시작합니다.

## 지오섬을 왜 하한으로 쓰는가

`interior_layers` 는 표면에서 중심까지 단열선 하나를 이어 적분하므로, 그 핵이 **맨틀** 의
단열선 위에 앉습니다. 거기 빠져 있는 것이 둘이고 둘 다 이름이 있습니다.

**D″ 열경계층.** 내부 구조 레시피의 온도가 기대고 있던 판정선인 Unterborn+ 2019 eq. 7 은
맨틀 단열선이고, 1 R⊕ 에서의 2635 K 는 맨틀 쪽 값입니다. 그 논문 자신이 Lay+ 2008 의
2500–2800 K 와 대조하면서 "as determined using a similar method to ours" 라고 적습니다.
지구의 핵 쪽 값은 3760 ± 290 K 입니다. 차이가 1200 K 를 넘고, 그 크기를 정하는 것은 핵-맨틀
경계의 열류인데 이 저장소는 그 열류를 도출하지 않습니다. Zhang & Rogers 2022 는 **자기
모형에서** 그 차이를 1 M⊕ 에서 ~240 K, 3 M⊕ 에서 ~1880 K 로 냅니다. 그 폭 자체가 이 값이
모형에 달렸다는 뜻입니다.

**철의 단열 기울기.** `eos.py` 는 γ 를 αK_T 와 c_V 에서 항등식으로 닫고, 얼음에서는 그것이
SeaFreeze 자신의 γ 와 소수 넷째 자리까지 맞습니다. 철에서는 그 항등식이 Seager+ 2007 의
αK₀ = 0.00121 GPa/K 를 받는데, 그건 밀도를 맞추려고 고른 열압력 상수이고, 핵 압력대에서
γ ≈ 0.22 를 냅니다. ab initio 값은 1.5 입니다.

두 편향이 다 **아래** 를 향합니다. 그래서 이 값은 잡음이 아니라 하한이고, 하한은 한쪽
방향의 판정을 떠받칩니다. 그것이 이 레시피의 첫 번째 갈래입니다. 어느 깊이의 융해온도가
하한보다 낮으면 거기는 액체이고, 경계층은 데우기만 하므로 그 판정은 뒤집히지 않습니다.
역은 성립하지 않으니 이 갈래는 `solid` 를 절대 내지 않습니다.

내부 구조 레시피가 1.05 R⊕ 위에서 기록해 둔 단열선의 **−17 % 편차** 도 같은 안전한 방향으로
움직입니다. 더 낮게 흐르는 하한은 `liquid` 판정을 줄이고 `undecided` 를 늘릴 뿐, 틀린
`liquid` 를 내지 않습니다. 선언 갈래는 맨틀 단열선을 아예 읽지 않으므로 그 편차가 닿지
않습니다.

## 상수

| 양 | 값 | 유효 범위 | 출처 |
|---|---|---|---|
| 철 융해, P ≤ 365 GPa | T_m = 1825 K (1 + P/57.723 GPa)^0.654 | 365 GPa 까지 적합. P = 0 에서 1825 K 대 실측 1811 K | Zhang+ 2015 초록 |
| 철 융해, P > 365 GPa | T_m = 6469 K (1 + (P − 300 GPa)/434.82 GPa)^0.54369 | 300–5000 GPa. 5 TPa 위는 거절 | González-Cataldo & Militzer 2023 초록 |
| 가벼운 원소 내림 | `fe_prem` 에 ×0.80, `fe_eps` 에는 없음 | 도출이 아니라 선언 | Stevenson+ 1983 관례, Zhang & Rogers 2022 가 사용 |
| 핵 그뤼나이젠 γ | 1.5 | 100–300 GPa · 4000–6000 K 에서 확인. 액체 Hugoniot 280–340 GPa 에서 1.51–1.52 | Alfè, Price & Gillan 2002 |

두 융해 조각은 300–365 GPa 에서 겹치고 거기서 **4.0 ~ 7.5 %** 어긋납니다. 높은 쪽이
González-Cataldo 조각입니다. 그 폭은 같은 압력의 두 정적압축 실험이 어긋나는 폭보다 좁습니다
— Anzellini+ 2013 의 6230 ± 500 K 대 Sinmyo+ 2019 의 5500 ± 220 K 로 13 % 차이입니다. 그래서
평균내지 않고 앞 조각의 저자가 자기 적합을 끝낸 자리에서 갈아타고, 그 벌어짐은 단정하는
대신 시험이 잽니다.

내림을 `fe_prem` 에만 적용하고 `fe_eps` 에는 적용하지 않는 것은 그 구분이 상태방정식에 이미
있기 때문입니다. `fe_prem` 은 PREM 외핵 적합이라 가벼운 원소를 이미 품고 있고, `fe_eps` 는
실험실 순수 ε-철입니다. 20 % 는 발표된 열진화 모형들이 쓰는 관례입니다. 독립 검산이 그 옆에
떨어집니다 — Sinmyo+ 2019 의 지구 내핵 경계 온도 5120 ± 390 K 를 순철 곡선의 329 GPa 값
6331 K 에 대면 19.1 % 입니다. 두 수는 같은 주장이 아니라서 이 일치는 도출이 아니라
검산입니다.

## 검증

판정선은 지구입니다. 지구 핵의 두 층이 측정된 사실이기 때문입니다. 오른쪽 칸은 전부 발표된
값이고 이 엔진의 출력이 아닙니다. `python3 engine/test_core_state.py --table` 이 다시 냅니다.

| 양 | 도출 | 발표 | 출처 | Δ |
|---|---|---|---|---|
| 핵-맨틀 경계 압력 | 135.2 GPa | 135.75 GPa | PREM | −0.4 % |
| PREM 내핵 경계에서의 핵 온도 | 5121 K | 5120 ± 390 K | Sinmyo+ 2019 | +0.0 % |
| 내핵 경계 압력 | 352 GPa | 328.85 GPa | PREM | +7.0 % |
| 핵의 상 | liquid_outer_solid_inner | 외핵 액체, 내핵 고체 | 지진학 | – |

둘째 행이 γ 에 대한 검산입니다. Sinmyo+ 2019 이 지구 핵 단열선 위의 두 점을 주고, 첫 점에서
γ = 1.5 로 올리면 둘째 점이 나옵니다. 셋째 행은 정직한 잔차입니다. 중심 근처에서 단열선과
융해곡선이 거의 나란해서 융해온도 1 % 가 경계를 수십 GPa 옮기고, 위의 두 실험은 13 %
어긋납니다.

## 유효 영역

| 레짐 | 조건 | 이 레시피가 하는 일 | 등급 |
|---|---|---|---|
| 핵 쪽 경계 온도가 선언됨 | `core_cmb_temperature` > 0 | 핵의 단열선을 적분해 `liquid` · `solid` · `liquid_outer_solid_inner` 를 경계 압력과 함께 낸다 | analog |
| **선언 없음, 하한이 곡선 위** | 융해온도가 `cmb_temperature` 와 `core_temperature` 아래 | `liquid` 를 낸다. 빠진 열은 더하기만 하므로 그 열을 넣어도 판정이 안 뒤집힌다 | analog |
| **선언 없음, 하한이 곡선 아래** | 그 밖의 경우 | `undecided` 를 내고 `solid` 는 절대 내지 않는다. 하한은 한쪽만 묶는다. 무엇을 선언하면 답이 나오는지를 이유가 이름 댄다 | judgment |
| 온도가 아예 없음 | 위쪽에서 `potential_temperature` 미선언 | **거절한다.** 내부 해가 등온이라 댈 지오섬이 없다 | — |
| **확인된 γ 구간 위의 단열선** | 중심압이 340 GPa 위 | 적분하되 note 를 단다. Alfè+ 2002 가 γ 를 확인한 압력 위로 상수인 채 끌고 간다 | analog |
| **중심이 융해곡선 밖** | 중심압이 5 TPa 위 | **거절한다.** 곡선이 끝나는 자리를 이름 댄다. 상태방정식은 12 TPa 까지 가지만 융해곡선은 5 TPa 에서 끝난다 | — |
| 핵이 없거나 미분화 | 핵-맨틀 경계 압력이 중심압 이상 | **거절한다.** 규산염에 섞인 금속은 녹는점 하나가 아니라 고상선과 액상선을 가진다 | — |
| 융해곡선 없는 핵 재료 | `fe_prem` · `fe_eps` 가 아닌 것 | **거절한다.** 그 재료의 이름을 댄다 | — |
| 거대행성·얼음거대행성·미니해왕성·갈색왜성·별 | `body_class` | **거절한다.** 그쪽 다이나모는 금속수소가 돌리고, `dynamo_giant` 의 갈래이며 철의 융해곡선과 무관하다 | — |
| **거꾸로 만남** | 경계에서 단열선이 곡선 아래이고 중심에서 위 | **거절한다.** 이 구간에서 융해선은 늘 단열선보다 가파르므로, 이 배치는 핵이 뒤집혔다는 뜻이 아니라 입력이 어긋났다는 뜻이다 | — |

## 출처

- **Zhang, W.-J., Liu, Z.-Y., Liu, Z.-L. & Cai, L.-C. 2015**, Phys. Earth Planet. Inter.
  244, 69 ([`2015PEPI..244...69Z`](https://ui.adsabs.harvard.edu/abs/2015PEPI..244...69Z)).
  365 GPa 아래에서 이 레시피가 쓰는 Simon 적합. 논문 자신의 초록에 실려 있고, 거기서 나오는
  내핵 경계 융해점 6345 K 도 함께 적혀 있습니다. *arXiv 프리프린트 없음*: bibcode 로
  확인했습니다.
- **González-Cataldo, F. & Militzer, B. 2023**, Phys. Rev. Research 5, 033194
  ([`2023PhRvR...5c3194G`](https://ui.adsabs.harvard.edu/abs/2023PhRvR...5c3194G)).
  300–5000 GPa 의 ab initio 융해선과 그 Simon 적합. 역시 초록에 실려 있고, 융해선이
  단열선보다 가팔라서 결정화가 늘 중심에서 시작한다는 문장도 같이 있습니다. *arXiv
  프리프린트 없음*: bibcode 로 확인했습니다.
- **Kraus, R. G. et al. 2022**, Science 375, 202
  ([`2022Sci...375..202K`](https://ui.adsabs.harvard.edu/abs/2022Sci...375..202K)). National
  Ignition Facility 에서 1000 GPa 까지 잰 철의 융해점. 위 고압 적합이 대조하는 실험이고, 핵
  응고를 4–6 M⊕ 행성의 다이나모 수명과 잇는 논문입니다. *arXiv 프리프린트 없음*: bibcode
  로 확인했습니다.
- **Anzellini, S., Dewaele, A., Mezouar, M., Loubeyre, P. & Morard, G. 2013**, Science 340,
  464 ([`2013Sci...340..464A`](https://ui.adsabs.harvard.edu/abs/2013Sci...340..464A)).
  내핵 경계의 두 실험 앵커 중 하나, 6230 ± 500 K. *arXiv 프리프린트 없음*: bibcode 로
  확인했습니다.
- **Sinmyo, R., Hirose, K. & Ohishi, Y. 2019**, Earth Planet. Sci. Lett. 510, 45
  ([`2019E&PSL.510...45S`](https://ui.adsabs.harvard.edu/abs/2019E%26PSL.510...45S)).
  나머지 앵커 5500 ± 220 K, 그리고 검증이 쓰는 지구 핵 온도 두 점 — 핵-맨틀 경계
  3760 ± 290 K 와 내핵 경계 5120 ± 390 K. *arXiv 프리프린트 없음*: bibcode 로
  확인했습니다.
- **Alfè, D., Price, G. D. & Gillan, M. J. 2002**, Phys. Rev. B 65, 165118
  ([`2002PhRvB..65p5118A`](https://ui.adsabs.harvard.edu/abs/2002PhRvB..65p5118A), arXiv
  **[cond-mat/0107307](https://arxiv.org/abs/cond-mat/0107307)**). `docs/phase3/_papers/cond-mat_0107307.md`
  에 **캐시** 돼 있습니다. 상수인 핵 그뤼나이젠 계수의 출처. γ 가 "varies little with
  pressure or temperature for 100 < p < 300 GPa and 4000 < T < 6000 K, and has a value of
  ca. 1.5" 이고, 액체 Hugoniot 에서 1.51–1.52 입니다.
- **Zhang, J. & Rogers, L. A. 2022**, ApJ 938, 131
  ([`2022ApJ...938..131Z`](https://ui.adsabs.harvard.edu/abs/2022ApJ...938..131Z), arXiv
  **[2208.06523](https://arxiv.org/abs/2208.06523)**). `docs/phase3/_papers/2208.06523.md`
  에 **캐시** 돼 있습니다. 가벼운 원소 20 % 내림을 실무 관례로 쓰는 예, 그리고 경계층이
  실재하고 크고 모형에 달렸음을 보이는 핵-맨틀 경계 온도차(1 M⊕ 에서 ~240 K, 3 M⊕ 에서
  ~1880 K). 이 논문이 옮겨 적은 Zhang+ 2015 의 Simon 계수는 그 논문 초록과 다릅니다. 여기
  계수를 원 논문에서 읽어 온 이유가 그것입니다.
- **Dziewonski, A. M. & Anderson, D. L. 1981**, Phys. Earth Planet. Inter. 25, 297
  ([`1981PEPI...25..297D`](https://ui.adsabs.harvard.edu/abs/1981PEPI...25..297D)). PREM.
  검증이 대조하는 핵-맨틀 경계와 내핵 경계의 압력이 여기서 옵니다.

## 관련

- [내부 구조](interior-structure-methodology.md) — 이 레시피가 하한으로 읽는 핵 압력과
  지오섬을 공급하고, 물의 융해곡선을 문서화합니다
- [암석행성 다이나모](rocky-planet-dynamo-methodology.md) — 소비처입니다. 전도성 액체 핵이
  필요하고, 그게 있는지를 말하는 것이 `conductor_phase` 입니다
- [내부 열과 광도](internal-heat-luminosity-methodology.md) — 선언을 대체할 핵-맨틀 경계
  열류가 나와야 하는 자리입니다
- [도출 규율](derivation-discipline.md) — 거절이 왜 반환값인가
