<!-- 천체가 무엇인가 — 질량과 반지름을 발표된 경계에 대서 클래스를 좁히는 방법(논문 근거) -->
# 천체 클래스 근거화. 어느 물리가 이 천체에 적용되는가

`body_class` 에서 `selects` 엣지 여덟이 나가고, 그 하나하나가 어느 모형을 돌릴지 고릅니다.
내부 적분, 클래스 표 셋, 도형, 자전축, 다이나모 둘, 그리고 핵 상태입니다. 그 엣지들이 읽는
키는 취향의 문제가 아닙니다. 해왕성을 가스거대행성이라고 적어 넣으면 얼음 맨틀 위에서 H/He
폴리트로프가 돌고, 자신 있게 틀린 수가 나옵니다.

이 레시피는 그 키를 질량과 반지름에서, 발표된 경계에 대서 도출합니다. 고르지 않고
**좁힙니다**. 경계마다 띠가 있고, 띠 안에 든 천체는 양쪽 이웃을 다 살린 채로 돌아옵니다.

## 계약 — `body_class`

**Returns** — `class` [—] · `classes` [—] · `decided_by` [—] · `agrees_with_declared` [—]
**Needs** — `mass_earth` [M_earth] · `radius_earth` [R_earth] · `declared_class` [—] ·
`composition_intent` [—] · `gas_mass_fraction` [—] · `semi_major_axis_au` [au]
**분기키** — 반지름이 있는가(사다리의 아래쪽 절반을 읽을 수 있는지가 여기서 갈립니다),
그리고 봉투 조성이 선언됐는가(가스거대행성과 얼음거대행성을 관례가 아니라 근거로 가르는
유일한 것입니다).
**등급** — 좁히는 데 쓰인 경계 중 가장 약한 것을 따라가고, 살아남은 클래스가 둘 이상이면
아무리 좋아도 **judgment** 입니다. 측정된 개체군 특징이 선을 그으면 `calibrated`, 형성
모형이 그으면 `analog`, 관례가 그으면 `judgment` 입니다.

`class` 는 아래 여섯 중 하나이고, 둘 이상이 살아남으면 비어 있습니다. `classes` 는 살아남은
것을 늘 전부 싣습니다. `declared_class` 는 **읽지만 계산에 쓰지 않습니다**. 입력이 아니라
대조 상대입니다.

## 어휘

질량 오름차순으로 여섯입니다. `rocky` · `sub_neptune` · `ice_giant` · `gas_giant` ·
`brown_dwarf` · `star`. 이름이 여기 들어오려면 소비처가 그것으로 갈려야 하고, 여섯 전부
`interior.py` 에 이름이 있습니다. `FLUID_CLASSES` 가 위의 넷을 각각 다른 이유로 거절하고,
`GAS_GIANT_CLASSES` 가 거대행성을 받고, 나머지가 암석 경로입니다.

`giant` 은 `gas_giant` 의 두 번째 철자이고, 이 저장소 어디에도 둘을 가르는 것이 없습니다.
읽을 때만 정규화하고 내보내지 않습니다. [도출 규율](derivation-discipline.md) §7 이 적은
규칙이 그것입니다. 목록은 하나이고, 철자 변종은 그 목록에 들이지 않습니다.

클래스는 **무엇으로 만들어졌나** 입니다. 무엇의 주위를 도느냐는 `BodyState.kind` 가 따로
들고 있는 선언이고, 이 레시피는 그것을 읽지 않습니다. 소비처 여덟이 전부 재료의 물리에서
갈리고 궤도 역할에서 갈리는 것은 하나도 없기 때문입니다.

## 사다리

경계 다섯, 각각 양이 하나이고 띠가 하나입니다. 띠의 양 끝은 발표된 수입니다. 띠 아래면 아래
클래스가, 위면 위 클래스가 서고, 안이면 둘 다 살아남습니다.

    rocky ─── sub_neptune ─── ice_giant ─── gas_giant ─── brown_dwarf ─── star
          R                R              M             M               M

두 절반이 서로 다른 양을 읽는 것은 편의가 아닙니다. 거대행성 아래에서 판별하는 것은
**반지름** 입니다. 밸리가 반지름의 특징이고, Rogers 2015 의 논지가 바로 주어진 반지름에서
외피의 유무를 말할 수 있다는 것입니다. 거대행성 위에서는 **질량** 입니다. 핵융합 문턱은
질량 문턱이고, 그 영역에서 반지름은 거의 축퇴돼 있습니다 (Chen & Kipping 의 Jovian 거듭제곱
지수가 −0.04 ± 0.02 입니다).

중수소 한계는 두 양 어느 쪽에도 흔적이 없는 유일한 경계입니다. Chen & Kipping 은 갈색왜성이
"merely high-mass members of a continuum of Jovians" 라고 적습니다. 그래도 경계인 이유는
여기서 갈리는 소비처가 구조가 아니라 **열이력** 에서 갈리기 때문입니다. `interior.py` 와
`dynamo.py` 는 둘 다 중수소 연소가 주는 광도 이력을 이유로 갈색왜성을 거절하고, 그 이력은
어느 레시피에도 없습니다.

살아남는 클래스는 경계들이 남긴 연속 구간입니다. 경계들이 서로 어긋나면 구간이 비는 대신
뒤집히고, 그때 레시피는 겹치는 부분 전체를 돌려줍니다. 사다리가 질량에 대해 단조이므로
어긋남은 넘겨받은 질량과 반지름이 양립하지 않는다는 뜻이고, 그것은
`mass_radius.density_gate` 의 질문입니다.

## 상수

| 경계 | 양 | 띠 | 유효 범위 | 출처 |
|---|---|---|---|---|
| 암석 / 서브넵튠 | 반지름 | 1.5 – 1.8 R⊕ | 가까운 행성, P < 100 d. `mass_radius.py` 에서 가져다 쓰고 다시 적지 않습니다 | Fulton+ 2017 (실측 결핍 1.5–2.0 R⊕); Rogers 2015 (R_thresh 1.48 +0.07/−0.56); Van Eylen+ 2018 |
| ” (반지름 없음) | 질량 | 1.45 – 2.70 M⊕ | 왜소행성부터 만형 항성까지 316개 | Chen & Kipping 2017, T(1) = 2.04 (+0.66/−0.59) M⊕ |
| 서브넵튠 / 얼음거대행성 | 반지름 | 3.5 R⊕, 띠 없음 | **관례**. 측정된 특징이 아니라 구간표의 선입니다 | Kopparapu+ 2018 §2.1, Fulton+ 2017 의 분포에서 읽음 |
| 얼음거대행성 / 가스거대행성 | 봉투 | 가스질량분율 ≥ 0.5 | 조성이 선언됐을 때만 | Lambrechts & Johansen 2014, Fig. 4 |
| ” (조성 없음) | 질량 | M_iso – 50 M⊕ | M_iso = 20 M⊕ (a/5 au)^(8/7). 50 M⊕ = 관측된 최대 핵질량의 2배 | Lambrechts & Johansen 2014 §4.1; Otegi+ 2020 (~25 M⊕) |
| 가스거대행성 / 갈색왜성 | 질량 | 11.0 – 16.3 M_J | 금속도·헬륨·연소분율을 다 흔든 모형 전체 범위. 흔한 조건에서는 13.0 ± 0.8 M_J | Spiegel+ 2011, 초록 |
| 갈색왜성 / 항성 | 질량 | 0.070 – 0.083 M_sun | 태양조성부터 [M/H] = −2 까지, 먼지 있는 대기부터 없는 대기까지 | Chabrier & Baraffe 2000, Fig. 3 및 §4.5.2 |
| 사다리 아래 | 반지름 | 200 – 300 km | 얼음 위성과 암석 소행성. 조성이 아니라 강도의 문제입니다 | Lineweaver & Norman 2010, 초록 |

단위 환산비는 IAU 2015 명목값입니다 (317.8 M⊕/M_J, 332946 M⊕/M_sun, 11.209 R⊕/R_J).
M_J 값은 `dynamo.py` 의 것이라, 한 양에 상수가 하나로 유지됩니다.

## 봉투 경계가 무엇을 필요로 하는가, 그리고 나머지는 왜 아닌가

가스거대행성과 얼음거대행성을 가르는 것은 크기가 아닙니다. **질량의 대부분이 수소-헬륨인가
무거운 원소인가** 이고, Lambrechts & Johansen 2014 가 그것을 정의로 삼습니다. 페블 고립질량에
닿은 핵은 고체 강착이 끊기고 봉투가 붕괴해 가스거대행성이 되고, 못 닿은 핵은 핵이 지배하는
채로 남습니다. 그 논문 Fig. 4 의 캡션이 그 말을 한 줄로 적습니다.

그래서 이것이 `composition_intent` 가 짐을 지는 유일한 경계이고, 질량 쪽 양 끝은 같은 문장을
한쪽씩만 읽은 것입니다. 총질량이 고립질량보다 작으면 핵이 거기 닿았을 수가 없습니다.
총질량이 지금까지 잰 가장 큰 핵(Otegi+ 2020 의 ~25 M⊕)의 두 배를 넘으면 절반 이상이 핵일 수
없습니다. 곱하기 2 는 적합해서 나온 계수가 아니라 '지배한다'는 말의 뜻입니다. 둘 사이에서는
레시피가 그 사실을 말하고, 판정을 열어 줄 선언의 이름을 댑니다.

Kopparapu+ 2018 의 6.0 R⊕ 선은 여기서 **쓰지 않습니다**. 그 논문이 그 값을 "the *assumed*
upper limit on Neptune-size planets" 라고 적기 때문입니다. 출처가 스스로 가정이라고 표시한
수를 옮겨 적는 것은 근거화가 아닙니다.

## 검증

태양계 여덟 행성이 판정선입니다. 질량과 반지름이 측정돼 있고 클래스에 이견이 없습니다. 어느
경계도 이 여덟에 맞춰 잡지 않았습니다. 반지름은 Archinal+ 2011 Table 4 의 평균반지름을
6371.00 km 로 나눈 값이고, 질량은 IAU 2009 의 GM 비입니다.
`python3 engine/test_body_class.py --table` 이 다시 냅니다.

| body | M (M⊕) | R (R⊕) | derived | published | grade | decided by |
|---|---|---|---|---|---|---|
| Mercury | 0.05527 | 0.383 | rocky | rocky | calibrated | radius valley |
| Venus | 0.815 | 0.950 | rocky | rocky | calibrated | radius valley |
| Earth | 1 | 1.000 | rocky | rocky | calibrated | radius valley |
| Mars | 0.1074 | 0.532 | rocky | rocky | calibrated | radius valley |
| Jupiter | 317.8 | 10.973 | gas_giant | gas_giant | analog | envelope dominance + deuterium burning |
| Saturn | 95.16 | 9.140 | gas_giant | gas_giant | analog | envelope dominance + deuterium burning |
| Uranus | 14.54 | 3.981 | ice_giant | ice_giant | judgment | sub-Neptune ceiling + envelope dominance |
| Neptune | 17.15 | 3.865 | ice_giant | ice_giant | judgment | sub-Neptune ceiling + envelope dominance |

토성이 판별하는 행입니다. 그럴듯한 대안 경계(Chen & Kipping 의 T(2))가 틀리는 유일한
앵커이고, 등급 칸이 근거가 강한 자리와 관례인 자리를 그대로 보여 줍니다. 암석 판정은 측정된
개체군 특징에, 거대행성 판정은 형성 모형에, 얼음거대행성 판정은 구간표의 선에 기대고
있습니다.

## 유효 영역

| 레짐 | 조건 | 이 레시피가 하는 일 | 등급 |
|---|---|---|---|
| 반지름이 있다 | 감자 반지름 위의 모든 천체 | 사다리 전체를 읽습니다. 아래 절반은 반지름으로, 위 절반은 질량으로 | 경계에 따라 |
| **반지름이 없다** | 통과하지 않는 시선속도 행성처럼 질량만 있는 경우 | 암석 경계는 Chen & Kipping 의 질량 전이로 대체하고, 서브넵튠 천장은 아예 못 그으므로 아래 세 클래스가 열린 채로 남습니다 | judgment |
| **봉투가 선언됐다** | `gas_mass_fraction`, 또는 그것을 함의하는 `composition_intent` | 두 거대행성을 그 둘을 정의하는 기준으로 가릅니다 | analog |
| 봉투 선언 없음 | 질량이 고립질량과 50 M⊕ 사이 | 거대행성 둘을 다 돌려주고, 판정을 열어 줄 선언의 이름을 댑니다 | judgment |
| **어느 띠든 그 안** | 판정하는 양에서 경계에 붙어 있다 | 양쪽 이웃을 다 돌려줍니다. 띠의 폭은 발표된 읽기들이 어긋나는 폭이고, 그것이 정직한 폭입니다 | judgment |
| 감자-구 전이 구간 | 평균반지름 200 – 300 km | 분류하되 단서를 답니다. 정수압 평형이 보장되지 않고, `body_figure` 의 J₂ 는 그것을 가정하는 Radau–Darwin 에서 옵니다 | judgment |
| **전이 구간 아래** | 평균반지름 200 km 미만 | **거절합니다**. 이 크기에서는 조성이 아니라 강도가 모양을 정하고, 이 어휘의 클래스는 전부 자기중력이 정하는 도형을 전제합니다 | – |
| 질량이 양수가 아니다 | – | **거절합니다** | – |
| **경계들이 어긋난다** | 반지름 쪽 판정과 질량 쪽 판정이 반대를 가리킨다 | **좁히지 않습니다**. 사다리가 질량에 대해 단조이므로, 이것은 질량과 반지름이 양립하지 않는다는 뜻입니다 | judgment |

밸리는 움직입니다. Ho & Van Eylen 2023 이 그 위치를 궤도주기(∂log R/∂log P = −0.096
+0.023/−0.027)와 항성질량(+0.231 +0.053/−0.064)에 대해 잽니다. 여기의 띠는 고정이고, 그것이
띠 안에서 선 하나가 아니라 "둘 다"를 돌려주는 또 하나의 이유입니다.

## 출처

- **Chen, J. & Kipping, D. 2017**, ApJ 834, 17
  ([`2017ApJ...834...17C`](https://ui.adsabs.harvard.edu/abs/2017ApJ...834...17C), arXiv
  **[1603.08614](https://arxiv.org/abs/1603.08614)**). `docs/phase3/_papers/1603.08614.md`
  에 **캐시**. 꺾인 거듭제곱의 꺾임점을 자유 모수로 두고 뽑은 전이질량 셋. 그중 둘이 여기의
  경계입니다. T(1) = 2.04 M⊕ 가 암석 경계의 질량 쪽 읽기이고, T(3) = 0.0800 ± 0.0081 M_sun
  은 독립적인 방법으로 수소연소 띠 안에 떨어집니다. T(2) = 0.414 M_J 는 가스/얼음 거대행성의
  선이 **아니고**, 근거는 그 논문 자신입니다. "Saturn is close to being the largest
  occurring Neptunian world" 이므로 그들의 Neptunian 은 천왕성부터 토성까지입니다.
- **Fulton, B. J. et al. 2017**, AJ 154, 109
  ([`2017AJ....154..109F`](https://ui.adsabs.harvard.edu/abs/2017AJ....154..109F), arXiv
  **[1703.10375](https://arxiv.org/abs/1703.10375)**). **캐시**. 밸리 띠를 긋는 근거인
  1.5–2.0 R⊕ 의 2배 이상 결핍 실측이고, Kopparapu+ 2018 이 자기 구간선을 읽어 낸 반지름
  분포입니다.
- **Rogers, L. A. 2015**, ApJ 801, 41
  ([`2015ApJ...801...41R`](https://ui.adsabs.harvard.edu/abs/2015ApJ...801...41R), arXiv
  **[1407.4457](https://arxiv.org/abs/1407.4457)**). **캐시**. 그 위로는 대부분이 암석이
  아닌 문턱 반지름. 지구식 조성을 하한으로 두면 1.48 (+0.07/−0.56) R⊕ 이고, 판별하는 것이
  반지름이라는 논지가 여기서 나옵니다.
- **Van Eylen, V. et al. 2018**, MNRAS 479, 4786
  ([`2018MNRAS.479.4786V`](https://ui.adsabs.harvard.edu/abs/2018MNRAS.479.4786V), arXiv
  **[1710.05398](https://arxiv.org/abs/1710.05398)**). **캐시**. 별진동으로 잰 항성
  반지름으로 본 밸리와 그 음의 주기 기울기. 서브넵튠이 벗겨진 핵이라는 것이고, 그래서 이
  경계가 태생이 아니라 조성의 문제입니다.
- **Ho, C. S. K. & Van Eylen, V. 2023**, MNRAS 519, 4056
  ([`2023MNRAS.519.4056H`](https://ui.adsabs.harvard.edu/abs/2023MNRAS.519.4056H), arXiv
  **[2301.04062](https://arxiv.org/abs/2301.04062)**). **캐시**. 밸리가 궤도주기·항성질량·
  나이에 따라 움직이는 정도. 고정된 띠를 어디까지 믿을 수 있는지를 이것이 묶습니다.
- **Kopparapu, R. K. et al. 2018**, ApJ 856, 122
  ([`2018ApJ...856..122K`](https://ui.adsabs.harvard.edu/abs/2018ApJ...856..122K), arXiv
  **[1802.09602](https://arxiv.org/abs/1802.09602)**). **캐시**. 직접검출 수확량 추정용
  크기 구간. 3.5 R⊕ 천장은 관례로 여기서 가져왔고, 6.0 R⊕ 선은 그들이 가정이라고 표시했기
  때문에 가져오지 않았습니다.
- **Lambrechts, M. & Johansen, A. 2014**, A&A 572, A35
  ([`2014A&A...572A..35L`](https://ui.adsabs.harvard.edu/abs/2014A%26A...572A..35L), arXiv
  **[1408.6087](https://arxiv.org/abs/1408.6087)**). **캐시**. 페블 고립질량
  M_iso = 20 M⊕ (a/5 au)^(8/7), 그리고 그것이 거대행성 두 클래스를 가르는 것이라는 진술.
  그 아래면 핵이 지배한 채로 남고, 그 위면 봉투가 폭주합니다.
- **Otegi, J. F., Bouchy, F. & Helled, R. 2020**, A&A 634, A43
  ([`2020A&A...634A..43O`](https://ui.adsabs.harvard.edu/abs/2020A%26A...634A..43O), arXiv
  **[1911.04745](https://arxiv.org/abs/1911.04745)**). **캐시**. 암석 개체군이 25 M⊕ 부근에서
  끝나고, 저자들이 그것을 형성 가능한 최대 핵질량으로 읽습니다. 봉투 띠의 위쪽 끝이 그
  두 배입니다.
- **Spiegel, D. S., Burrows, A. & Milsom, J. A. 2011**, ApJ 727, 57
  ([`2011ApJ...727...57S`](https://ui.adsabs.harvard.edu/abs/2011ApJ...727...57S), arXiv
  **[1008.5150](https://arxiv.org/abs/1008.5150)**). **캐시**. 중수소 연소 질량과 그 실제
  폭. 흔한 원시갈색왜성 조건에서 13.0 ± 0.8 M_J 이고, 금속도와 헬륨과 연소분율 정의를 전부
  흔들면 11.0 ~ 16.3 M_J 입니다.
- **Chabrier, G. & Baraffe, I. 2000**, ARA&A 38, 337
  ([`2000ARA&A..38..337C`](https://ui.adsabs.harvard.edu/abs/2000ARA%26A..38..337C), arXiv
  **[astro-ph/0006383](https://arxiv.org/abs/astro-ph/0006383)**). **캐시**. 수소연소
  최소질량. 태양조성에서 0.075 M_sun, [M/H] = −2 에서 0.083 M_sun 이고, 대기의 먼지를 어떻게
  다루느냐에 따라 0.070–0.072 M_sun 까지 내려갑니다.
- **Lineweaver, C. H. & Norman, M. 2010**, 프리프린트
  ([`2010arXiv1004.1091L`](https://ui.adsabs.harvard.edu/abs/2010arXiv1004.1091L), arXiv
  **[1004.1091](https://arxiv.org/abs/1004.1091)**). 얼음 위성과 암석 소행성이 평균반지름
  ~200–300 km 에서 감자에서 구로 넘어간다는 전이. 초록에서 읽었습니다. *프리프린트뿐이고
  심사를 거치지 않았으며 ar5iv 가 전문을 주지 않습니다.* 거절 문턱에만 쓰고 그 아래로는
  아무것도 흐르지 않습니다. Tancredi & Favre 2008
  ([`2008Icar..195..851T`](https://ui.adsabs.harvard.edu/abs/2008Icar..195..851T)) 이 같은
  질문을 관측 쪽에서 다룹니다.
- **Archinal, B. A. et al. 2011**, Celest. Mech. Dyn. Astron. 109, 101
  ([`2011CeMDA.109..101A`](https://ui.adsabs.harvard.edu/abs/2011CeMDA.109..101A)) 과
  **Luzum, B. et al. 2011**, ibid. 110, 293
  ([`2011CeMDA.110..293L`](https://ui.adsabs.harvard.edu/abs/2011CeMDA.110..293L)). 앵커
  여덟의 평균반지름과 GM 비. *arXiv 프리프린트 없음*: bibcode 로 확인했습니다.

## 관련

- [질량-반지름 관계](mass-radius-relation-methodology.md) — 이 레시피가 가져다 쓰는 반지름
  밸리 상수를 소유하고, 같은 상수로 자기 영역을 다른 질문에 대해 지킵니다
- [내부 구조](interior-structure-methodology.md) — 가장 큰 소비처. 어느 상태방정식이
  적용되는지, 그리고 어느 클래스를 이름 대며 거절하는지
- [핵 상태](core-state-methodology.md) — 이 키로 핵 없는 여섯 클래스를 거절합니다
- [행성 다이나모 스케일링](planetary-dynamo-scaling.md) — 거대행성 갈래, 그리고 질량으로
  갈색왜성을 거절하는 자기 몫의 판정
- [도출 규율](derivation-discipline.md) — 왜 어휘가 하나여야 하는지, 그리고 거절이 왜
  반환값인지
