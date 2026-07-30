<!-- 임의 기체 조합의 온실 상승폭(T_surf − T_eq)을 4개 층으로 도출하는 방법(논문 근거) -->
# 온실 상승폭 근거화: 임의 기체 조합에서 지표온도까지, 네 개의 층

대기를 가진 천체의 **온실 상승폭**

    ΔT_gh  =  T_surface  −  T_eq

을 임의의 기체 조합에 대해 도출하는 방법 문서다. 복사 평형 온도는 교과서 닫힌 형태로 구할 수
있지만 상승폭은 그렇지 않다. 상승폭은 복사 전달 계산의 결과값이고, 레시피 없이 숫자만 적는 것은
[도출값 근거화 규율](methodology-index.md)이 금지하는 back-of-envelope에 해당한다.

담당 범위를 나누면, `T_eq`와 동기 자전 천체의 낮밤 구조는
[`tidally-locked-temperature-methodology.md`](tidally-locked-temperature-methodology.md)가,
그 대기가 애초에 유지되는지는
[`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md)가 맡는다. 이
문서는 조성을 주어진 것으로 받아 온난화를 돌려준다.

계산기는 [`scripts/refs/greenhouse_dt.py`](../../../scripts/refs/greenhouse_dt.py)다
(Layer 3과 모항성 보정을 구현).

## 발상

**1단계 — 대기가 없을 때의 온도는 공짜로 나온다.** `T_eq`는 천체가 받는 별빛과 반사율만으로
정해진다. 닫힌 식 한 줄이면 되고 모형이 필요 없다.

**2단계 — 대기가 얹는 몫은 공짜가 아니다.** 상승폭은 대기가 방출 적외선에 얼마나 불투명한지로
정해지고, 그것은 *어떤* 기체가 *어느 분압으로* 있는지, 그리고 어떤 분자 *쌍*이 충돌하는지에
달려 있다. 닫힌 식이 없다. 정직한 숫자는 모두 누군가 돌린 복사 계산에서 나온다.

**3단계 — 그래서 내 경우를 덮는 가장 싼 층을 고른다.** 아래 네 층은 "완전히 일반적이지만 손이
많이 감"에서 "한 줄이지만 적용 범위가 좁음"까지 늘어서 있다. 라우팅 표를 읽고, 조건을 만족하는
가장 얕은 층을 쓰고, 어느 층에서 나온 숫자인지 기록한다.

## 어느 층을 쓸까

| | 층 | 적용 대상 | 비용 | 쓰는 상황 |
|---|---|---|---|---|
| **1** | [해석적 복사-대류 모형](#layer-1--해석적-모형-임의-조성) | 임의 조성, 임의 기압, 얇은 대기부터 두꺼운 대기까지 | 불투명도 파라미터 2개 결정 | 두꺼운 대기, 이례적 조성, 또는 P-T 프로파일 전체가 필요할 때 |
| **2** | [기체별·쌍별 불투명도 자료](#layer-2--기체별쌍별-불투명도-기체-조합에-대한-답) | 임의 혼합, 분자 자료부터 | 불투명도 조립 후 Layer 1이나 모형에 투입 | 발표된 유사 사례가 없는 조합. 낯선 기체, 낯선 CIA 쌍 |
| **3** | [앵커된 iso-Ts 등온선](#layer-3--앵커된-iso-ts-등온선-단축-경로) | N₂ 배경 + CO₂ (+CH₄), 약 1 bar, 태양형 모항성 | 한 줄 | 흔한 암석행성 사례이고 ±5~10 K를 받아들일 때 |
| **4** | [실제 모형을 빌리거나 돌리기](#layer-4--실제-모형을-빌리거나-돌릴-때) | 전부 | 수 시간~수 일 | 답이 결정적이고 Layer 1~3이 엇갈리거나 적용되지 않을 때 |

NearStars 천체 대부분은 Layer 3을 쓰므로 적용 예가 거기 붙어 있다. 동시에 가장 좁은 층이고,
계산기의 `layer_check()`가 적용되지 않는 이유를 출력한다.

## Layer 1 — 해석적 모형 (임의 조성)

[Robinson & Catling 2012](https://arxiv.org/abs/1209.1833)는 대기 열구조의 **완전히 해석적인
1차원 복사-대류 모형**을 제시했다. 열복사 전달은 two-stream 근사에서 회색으로 다루고, 대기는
정역학 평형이며, 핵심 모형 선택은 **기압과 회색 열 광학깊이 사이의 거듭제곱 스케일링**이다. 대류
영역은 휘발성 응결을 반영하는 스케일 파라미터를 가진 단열선을 따른다. 이 가정들을 합치면 P-T
프로파일과 복사·대류 플럭스 프로파일의 닫힌 형태 표현이 나온다.

이 층이 일반적인 이유는 **조성이 두 개의 손잡이로만 들어오기** 때문이다. 광학깊이-기압 스케일링
(내 기체 조합이 열적외선을 얼마나 강하게 흡수하고 그것이 기압과 함께 어떻게 커지는지)과 단열선
파라미터(어느 응결물이 지배하는지)다. 이 둘을 정하면 어떤 조합이든, 어떤 기압이든 지표온도가
나온다.

저자들은 이 모형을 **금성·목성·타이탄**의 관측된 열구조로 검증했다. 조성이 서로 전혀 다른 세
대기이고, 여기에 더 복잡한 모형과의 플럭스 비교도 있다. 이 검증 범위가 곧, 시생대 지구형 상자를
벗어난 천체에서 이 층을 먼저 집어야 하는 이유다.

동반 문서 둘.

- [Robinson & Catling 2014](https://arxiv.org/abs/1312.6859)는 적외선 투명도의 기압 의존성이
  **사실상 모든 두꺼운 대기에서 대류권계면을 0.1 bar 근처에** 놓는다는 것을 보였다. 공짜로 얻는
  구조 제약이다. 모형이나 아트 디렉션이 계면을 다른 곳에 두면 경고 신호다.
- [Pierrehumbert 2010](https://ui.adsabs.harvard.edu/abs/2010ppc..book.....P),
  *Principles of Planetary Climate*는 밑에 깔린 회색·밴드 모형 온실 관계식의 교과서적 유도다.
  교과서이므로 추가 근거가 필요 없다.

식과 계수는 논문에 있다. ar5iv에 기계 판독 가능한 전문이 없어서 이 문서는 식을 옮겨 적지 않았다.
이 층을 쓰려면 논문을 먼저 읽어야 한다.

## Layer 2 — 기체별·쌍별 불투명도 (기체 조합에 대한 답)

혼합물의 불투명도를 처음부터 쌓으려면 두 종류의 자료가 필요하고, 이 둘이 서로 다른 물리라는
점을 분명히 해두는 게 좋다.

**단일 기체 흡수선.** [Gordon 2017](https://ui.adsabs.harvard.edu/abs/2017JQSRT.203....3G)의
HITRAN2016이 표준 선 목록이다. 이미 적분된 답이 필요하면
[Byrne & Goldblatt 2014b](https://arxiv.org/abs/1409.1880)가 **시생대 후보 온실기체 28종의
복사강제력**을 발표했고, 이는 창작한 대기 안의 미량 종 가운데 무엇이 애초에 의미가 있는지 순위를
매기는 가장 빠른 방법이다.
[2014a](https://ui.adsabs.harvard.edu/abs/2014GeoRL..41..152B)는 CO₂·CH₄·N₂O를 아주 높은
농도까지(CO₂는 50,000 ppmv까지, 최대 강제력 38.1 W/m²) 다루며, 통상의 로그 표현식이 깨지는
영역을 메운다.

**충돌유발흡수(CIA).** 충돌하는 분자쌍은 어느 쪽 분자에도 선이 없는 파장에서 흡수한다. 두껍거나
환원성인 대기에서는 이쪽이 온난화를 지배하는 경우가 많아서, 사용 가능한 *쌍*이 어떤 조합이
따뜻할 수 있는지를 제한한다.
[Karman 2019](https://ui.adsabs.harvard.edu/abs/2019Icar..328..160K)가 현행 HITRAN CIA
섹션이며 존재하는 쌍을 정확히 열거한다.

| 대기 유형 | 중요한 CIA 쌍 | HITRAN CIA 수록 |
|---|---|---|
| N₂ 주도 환원성 (시생대 지구, 타이탄) | N₂–N₂, N₂–H₂, N₂–CH₄ | 있음 |
| N₂ 주도 산화성 (현재 지구) | N₂–O₂, O₂–O₂, N₂–H₂O | 있음 |
| CO₂ 주도 (화성형, 약한 금성형) | CO₂–CO₂, CH₄–CO₂, O₂–CO₂ | 있음 |
| CO₂ + H₂ (환원성 두꺼운 대기) | CO₂–H₂ | **없음 — 아래 참조** |
| H₂/He 풍부 | H₂–H₂, H₂–He, H₂–CH₄, H₂–H, H–He | 있음 |
| 비활성기체 완충 | CH₄–He, CH₄–Ar, CH₄–CH₄ | 있음 |

CO₂–H₂의 공백은 이 문서의 누락이 아니라 문헌 자체의 한계다. 캐시된
[Hayworth 2020](https://arxiv.org/abs/2004.09076) 본문이 기록하듯, Ramirez 등은 "CO₂가 CIA
들뜨기에서 N₂만큼 효율적이라고 가정하고 N₂–H₂ CIA 계수를 조기 화성 조건에 적용"했다. 이 문서가
인용하는 것을 포함해 발표된 모든 CO₂–H₂ 온난화 추정치가 그 대리값 위에 서 있다. NearStars
천체의 온기가 CO₂–H₂에 달려 있다면 그 사실을 명시해야 한다.

고전적 CO₂+H₂O가 아닌 조합, 즉 CO₂+CH₄나 CO₂+H₂ 아래의 거주가능대 한계는
[Ramirez 2018](https://arxiv.org/abs/1807.09504)이 최신 HZ 정식화들을 리뷰해 두었다. 불투명도를
손으로 조립하기 전에 들를 곳이다.

## Layer 3 — 앵커된 iso-Ts 등온선 (단축 경로)

흔한 사례(N₂ 배경, 주 온실기체는 CO₂, 선택적으로 CH₄, 약 1 bar, 태양형 모항성)라면 발표된 모형
계산을 그대로 재사용할 수 있고 불투명도 작업이 아예 필요 없다.

기후 논문들은 같은 질문을 반복해서 푼다. *이 별빛 세기에서 지표를 273 K로 유지하려면 CO₂가
얼마나 있어야 하는가?* 답 하나하나가 (별빛, CO₂) 평면의 점이 되고, 점들이 등온선을 그린다.
천체를 그 등온선에 대고 읽으면 된다. CO₂가 등온선보다 많으면 273 K보다 따뜻하고, 적으면 춥다.
**얼마나**는 288 K 등온선이 알려준다. 두 등온선 사이의 가로 간격이 15 K에 해당하므로,
"등온선에서 떨어진 거리"를 켈빈으로 환산할 수 있다.

등온선 모양에 물리가 담긴다.

- **별빛이 줄면 급격히 치솟는다.** `S/S₀`를 0.80에서 0.75로 낮추면 273 K에 필요한 CO₂가 여섯
  배가 된다.
- **끝이 있다.** CO₂가 대략 8 bar를 넘으면 레일리 산란이 온실 심화보다 빠르게 행성을 밝게 만들어
  **CO₂를 더 넣어도 더워지지 않는다.** 그 끝점이 거주가능대 바깥 경계이므로, 별도 규칙 없이
  등온선이 거주가능대를 품고 있다.

### 앵커 점

발표된 1차원 복사-대류 계산, 1 bar 배경, 구름 없음. **Ts = 273 K** 등온선을 고정하는 세 점.

| S/S₀ | Ts = 273 K에 필요한 pCO₂ | 출처 |
|---|---|---|
| 0.80 | 0.01 bar | [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1, 후기 시생대 |
| 0.75 | 0.06 bar | [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1, 초기 시생대 |
| `Seff_maxgh(Teff)` | ~8 bar | [Kopparapu 2013](https://arxiv.org/abs/1301.6674), 최대온실 한계 |

**Ts = 288 K** 등온선은 두 점([Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1)으로
고정한다. `S/S₀` = 0.80에서 0.1 bar, 0.75에서 0.3 bar다.

### 모항성 일반화

세 번째 앵커는 고정된 숫자가 아니다. 붉은 별의 빛은 레일리 산란되기보다 흡수되므로, 최대온실
한계는 모항성 스펙트럼에 따라 움직인다.
[Kopparapu 2013](https://arxiv.org/abs/1301.6674)은 이를 파라미터 형태(그들의 Table 3)로
발표했고 `2600 ≤ Teff ≤ 7200 K`에서 유효하다.

    Seff  =  Seff⊙  +  a·T★  +  b·T★²  +  c·T★³  +  d·T★⁴,      T★ = Teff − 5780 K

| 한계 | Seff⊙ | a | b | c | d |
|---|---|---|---|---|---|
| Recent Venus | 1.7753 | 1.4316e-4 | 2.9875e-9 | −7.5702e-12 | −1.1635e-15 |
| 폭주 온실 | 1.0512 | 1.3242e-4 | 1.5418e-8 | −7.9895e-12 | −1.8328e-15 |
| 습윤 온실 | 1.0140 | 8.1774e-5 | 1.7063e-9 | −4.3241e-12 | −6.6462e-16 |
| **최대온실** | **0.3438** | **5.8942e-5** | **1.6558e-9** | **−3.0045e-12** | **−5.2983e-16** |
| Early Mars | 0.3179 | 5.4513e-5 | 1.5313e-9 | −2.7786e-12 | −4.8997e-16 |

그래서 등온선의 끝점은 태양에서 `Seff` = 0.344, α Cen A(5847 K)에서 0.348, 4400 K K형에서
0.272, Proxima급 3050 K M형에서 0.227에 놓인다. `greenhouse_dt.py --seff-table`이 곡선을
출력한다.

**반면 시생대 앵커 두 점은 움직이지 않는다.** 태양 스펙트럼으로 계산된 값이기 때문이다. 따라서
Layer 3은 태양형 `Teff` 근처 모항성에서만 유효하고, 계산기는 ±800 K를 넘으면 경고한다. M형이면
M형 모형 계산으로 앵커를 다시 잡거나 Layer 1/2로 내려가야 한다. 이걸 놓치는 것이 전형적인
오류다. M형의 붉은 출력은 알베도와 흡수를 함께 바꾸고, 그에 따라 CO₂ 요구량도 바뀐다.

### 공식

앵커 사이는 `S/S₀`에 대해 `log₁₀ pCO₂`를 선형 보간한다.

    pCO₂_eff  =  pCO₂ · 3            (CH₄ 혼합비가 대략 1e-4 이상일 때)

    Ts  =  273 K  +  m(S) · log₁₀(pCO₂_eff / pCO₂_273(S))  −  ΔT_haze  +  ΔT_N2

    m(S)  =  15 K / log₁₀( pCO₂_288(S) / pCO₂_273(S) )      [CO₂ 10배당 K]

    ΔT_gh  =  Ts  −  T_eq,        T_eq = 278.6 K · (S/S₀)^¼ · (1 − A)^¼

말로 풀면 이렇다. `pCO₂_eff / pCO₂_273`은 천체가 273 K 등온선에서 얼마나 떨어져 있는지를 비율로
잰 값이다. `m(S)`는 그 비율이 열 배가 될 때 몇 K인지이며 두 등온선 사이 간격에서 얻는다. 마지막
두 항은 haze와 총압 보정이다. `S/S₀` = 0.75 아래에서는 288 K 등온선을 273 K 등온선과 같은 양만큼
평행 이동시키므로 두 등온선 간격이, 따라서 `m`도 0.75에서의 값인 CO₂ 10배당 21.5 K로 고정된다.
보정 항마다 근거가 붙는다.

- **CH₄ 보정, 3배.** [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.3(Kiehl & Dickinson
  1987 인용)에 따르면 CH₄ 혼합비 1e-4는 같은 지표온도에 필요한 CO₂를 "약 3배" 낮춘다. CH₄ 양이
  더 많다고 이 보정을 비례로 키우면 안 된다.
  [Byrne & Goldblatt 2015](https://ui.adsabs.harvard.edu/abs/2015CliPa..11..559B)는 태양 흡수선
  때문에 시생대 CH₄ 온난화가 오히려 *약해진다*는 것을 보였고,
  [Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H)은 흡수계수 오류를
  고치면서 CH₄ 온실을 하향 수정했다.
- **ΔT_haze = 20 K**, haze가 형성된 경우.
  [Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A)은 프랙탈 유기 haze가 지표를
  "약 20 K" 식히지만 그 냉각이 **자기제한적**(두꺼워지면 스스로를 가린다)이라는 것을 보였다.
  따라서 20 K는 기울기가 아니라 상한이다. haze는 CH₄/CO₂가 대략 0.1을 넘으면 생기고
  ([Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H);
  [Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A)), 계산기가 기본으로 이
  조건을 검사한다.
- **ΔT_N2 = 총압 2배당 4.4 K.**
  [Goldblatt 2009](https://ui.adsabs.harvard.edu/abs/2009NatGe...2..891G): 시생대 CO₂·CH₄
  수준에서 현재 N₂ 총량을 두 배로 늘리면 기존 흡수선의 압력 확장으로 4.4 °C가 더워진다. 조성과
  무관하게 총압이 따로 중요해지는 항이다.

### 검증

`python3 scripts/refs/greenhouse_dt.py`

| 사례 | S/S₀ | pCO₂ | CH₄ | 공식 Ts | 발표 Ts | 차이 |
|---|---|---|---|---|---|---|
| 현재 지구(관측) | 1.00 | 280 ppm | 1.7 ppm | 286.9 K | 288 K | −1.1 |
| Feulner 후기 시생대, 273 K | 0.80 | 0.01 bar | — | 273.0 K | 273 K | 앵커 |
| Feulner 후기 시생대, 288 K | 0.80 | 0.10 bar | — | 288.0 K | 288 K | 앵커 |
| Feulner 초기 시생대, 273 K | 0.75 | 0.06 bar | — | 273.0 K | 273 K | 앵커 |
| Feulner 초기 시생대, 288 K | 0.75 | 0.30 bar | — | 288.0 K | 288 K | 앵커 |
| Kiehl & Dickinson 1987, +CH₄ | 0.75 | 0.10 bar | 1e-4 | 288.0 K | 288 K | 0.0 |
| Charnay 2013 3D GCM, 조성 C | 0.75 | 0.10 bar | 2 mbar | 288.0 K | 290 K | −2.0 |
| Kopparapu 2013 최대온실 | 0.344 | 8 bar | — | 273.0 K | 273 K | 앵커 |

앵커가 아닌 진짜 시험은 두 줄이다. **현재 지구가 1.1 K 낮게**, **Charnay의 3차원 GCM이 2.0 K
낮게** 나오는데 둘 다 별도 튜닝이 없다. Kiehl & Dickinson 줄은 CH₄ 보정을 독립적으로 시험해
288 K를 정확히 재현한다.

가장 강한 검증은 애초에 맞추지 않은 쪽에서 나온다. 등온선을 조기 화성(`S/S₀` = 0.32)까지
연장하면 **pCO₂ ≈ 10.7 bar**가 필요한데, 이는 최대온실 컬럼 약 8 bar를 넘으므로 도달 불가다.
CO₂와 H₂O만으로는 조기 화성을 273 K까지 데울 수 없다는 발표된 결론
([Kasting 1991](https://ui.adsabs.harvard.edu/abs/1991Icar...94....1K);
[Ramirez 2014](https://arxiv.org/abs/1405.6701);
[Hayworth 2020](https://arxiv.org/abs/2004.09076))이 시생대 지구 앵커만으로 복원된다.

## Layer 4 — 실제 모형을 빌리거나 돌릴 때

숫자가 결정적이고 위의 층들이 엇갈리거나 적용되지 않으면 line-by-line 또는 correlated-k
복사-대류 모형까지 내려간다. 실무에서는 "빌린다"가 거의 항상 옳은 동사다. 조성·기압·모항성
스펙트럼이 대상 천체를 감싸는 발표된 계산을 찾고, Layer 3이 하듯 발표된 사례들 사이를 보간한다.

환원성 두꺼운 대기라면 발표된 격자가 이미 충분하다.
[Ramirez 2014](https://arxiv.org/abs/1405.6701)는 CO₂ 1.3~4 bar **+ H₂ 5~20 %**로 조기 화성을
273 K 위에 올리고, [Wordsworth & Pierrehumbert 2013](https://ui.adsabs.harvard.edu/abs/2013Sci...339...64W)은
태양 플럭스 75 %에서 현재 N₂ 총량의 2~3배와 H₂ 혼합비 0.1로 초기 지구를 0 °C 위에 올린다(CO₂는
현재의 2~25배만 필요). 이 수치들이 요구하는 조건을 보라. **퍼센트 수준의 H₂이며 미량이 아니다.**
미량 H₂로는 아무것도 살 수 없고, 퍼센트 수준을 유지하려면 강하게 환원된 맨틀과 탈출을 앞지르는
탈기체가 필요하다.

## 적용 범위, 천체 종류별

1. **Layer 3 보정 상자: `0.75 ≤ S/S₀ ≤ 1.0`, `pCO₂ ≤ 0.3 bar`, 총압 약 1 bar, N₂ 배경,
   태양형 Teff.** ±5 K를 기대한다.
2. **Layer 3 외삽 구간: `Seff_maxgh ≲ S/S₀ < 0.75`.** 여기서 등온선은 초기 시생대 앵커와
   최대온실 앵커를 잇는 직선이다. 양 끝은 발표된 점으로 묶여 있고 중간은 자유롭다. **±10 K**로
   보고 그 사실을 적는다. A b(폴리페무스) 위성들이 여기 있다.
3. **최대온실 한계 아래**에서는 양이 얼마든 CO₂ 경로가 닫힌다. 환원성 CIA만이 따뜻해지는 길이며,
   Layer 4의 격자와 Layer 2의 CO₂–H₂ 대리값 주의사항이 함께 적용된다.
4. **두꺼운 대기(≳ 2 bar)와 금성형 상태**는 Layer 1이다. Layer 3은 크게 틀린다. 금성의 실제
   상승폭은 약 +510 K로, 등온선이 다루는 범위를 한참 벗어난다.
5. **비태양형 모항성**: Layer 3의 시생대 앵커가 태양 스펙트럼이다. K형은 경계선, M형은 범위 밖.
6. **Layer 2~3 전체에서 구름은 제외되어 있다.** 모든 앵커가 구름 없는 계산이고, Kopparapu는
   CO₂ 구름 온난화를 빼놓았기 때문에 자기 바깥 경계가 보수적이라고 명시한다. 목표보다 몇 K
   모자란 천체를 구름 온난화로 변호할 수는 있지만, 추가 가정이므로 반드시 가정으로 기록한다.
7. **폭주·수증기 대기와 H₂/He 외피에는 쓰지 않는다**(후자는 H₂–H₂·H₂–He CIA를 쓰는 Layer 1이고,
   "지표"가 정의의 문제가 된다).

## 적용 예: A b(폴리페무스) 위성들

α Cen A는 `L = 1.521 L☉`, `Teff = 5847 K`(큐레이션값,
`db/systems/alpha_centauri_a.json`)이고 A b는 1.6 AU를 돈다. 따라서 모든 위성이 받는 값은
`S/S₀ = 1.521 / 1.6² = 0.594`로, **초기 시생대 지구(0.75)보다 어둡지만** 이 별의 최대온실
한계(0.348)보다는 충분히 안쪽이다. 원리적으로 물이 액체로 있을 수 있지만 지구보다 훨씬 두꺼운
CO₂ 컬럼이 필요하다. 태양형 모항성과 약 1 bar N₂/CO₂/CH₄ 조합이므로 두 천체 모두 Layer 3
외삽 구간, ±10 K다.

이 입사량에서 273 K 등온선은 **pCO₂ ≈ 0.39 bar**(CO₂만), CH₄ 수 mbar가 있으면 **≈ 0.13 bar**이고
CO₂ 민감도는 10배당 21.5 K다.

| 천체 | 기록된 대기 | T_eq | Layer 3 Ts | ΔT_gh | 기록된 ΔT |
|---|---|---|---|---|---|
| Alpha Centauri A b IV (Cassandra) | 1 bar N₂, CO₂ 3 %, CH₄ 3 mbar, 얇은 haze, A 0.35 | 220 K | haze 포함 **239 K** / haze 없이 **259 K** | +20 / +40 K | +45~50 K |
| Alpha Centauri A b III (Pandora) | 1.1 bar, CO₂ 18 % + CH₄ + H₂S, A 0.30 | 224 K | **277 K** | +54 K | +70 K |

- **A b IV**는 haze 문턱에 정확히 걸쳐 있다. CH₄/CO₂가 딱 0.1이라 haze 항이 논지 전체를
  좌우한다. haze를 인정하면 239 K의 얼음 세상이고, haze가 전혀 없다고 하면 259 K까지 오른다.
  이 위성은 애초에 눈에 보이는 호박색 haze를 갖도록 설계되었으므로 방어 가능한 창은
  **240~260 K**다. 물이 따뜻한 적도나 계절에만 열리는 부분 동결 세계이며, 이미 표면 서술이 그렇게
  말하고 있다. 전 지구 평균 270~275 K를 유지하려면 CO₂를 0.13 bar(1 bar 대기의 13 %, 기록값의
  네 배)까지 올리거나 퍼센트 수준의 H₂를 넣어야 한다.
- **A b III**는 영화 설정 조성 그대로 277 K가 나온다. 거주 가능하고 어는점 위이지만 기록된 290 K보다
  약 13 K 차다. 이 입사량에서 290 K에 닿으려면 pCO₂가 약 0.8 bar, 즉 CO₂ 비율이 18 %가 아니라
  70 % 가까이여야 해서 영화 설정 조성과 모순된다. 일관된 선택은 평균 지표온도를 277 K로 내리거나,
  CO₂ 구름 온난화를 명시적 가정으로 끌어들이는 것이다(적용 범위 6번). 영화 설정 구성 성분인 H₂S는
  HITRAN CIA에 쌍이 없어서 인정하려면 Layer 2의 선 자료가 필요하고, 지금 이 온난화의 어느
  부분도 담당하지 않는다.

두 기록값 모두 레시피 없이 부여되었고 둘 다 낙관적으로 나왔다. ±10 K 구간에 대해 Cassandra는
haze를 얼마나 인정하느냐에 따라 15~35 K, Pandora는 약 13 K 높다. 방법 자체의 신뢰도는 중간,
입력값(CO₂ 비율, haze 광학깊이, 알베도)의 신뢰도는 낮다.

### 같은 천체를 다른 별 주위에 놓으면

`greenhouse_dt.py`는 `S/S₀` = 0.594에 있는 같은 1 bar / CO₂ 3 % / CH₄ 3 mbar 천체를 세 모항성
아래에서 계산하며 끝난다. 모항성 축과 그 한계를 함께 보여주기 위해서다.

| 모항성 | 최대온실 Seff | 273 K에 필요한 pCO₂ | Layer 3 Ts | 판정 |
|---|---|---|---|---|
| α Cen A, 5847 K | 0.348 | 0.40 bar | 259 K | 범위 내 |
| K형, 4400 K | 0.272 | 0.30 bar | 262 K | 경계선 |
| Proxima급, 3050 K | 0.227 | 0.26 bar | 263 K | **범위 밖** |

추세 자체는 물리적이다. 차가운 별의 최대온실 한계가 더 낮은 플럭스에 놓이므로 같은 천체가 더
적은 CO₂로 충분해진다. 하지만 인용 가능한 것은 첫 줄뿐이다. 나머지 두 줄은 태양 스펙트럼 시생대
앵커를 물려받으므로, M형이라면 Layer 1/2의 영역이다.

## 복사강제력 × 기후민감도로 가지 않는 이유

교과서적으로 보이는 대안은 강제력을 W/m²로 더한 뒤 민감도(K per W/m²)를 곱하는 것이다. 두 항은
다 존재한다(Layer 2의 강제력 표가 바로 앞의 절반이다). 문제는 곱하는 순간이다. 민감도는 상수가
아니다. 수증기와 얼음 알베도 때문에 지금 구하려는 그 온도에 민감도가 의존하므로, 하나의 λ로
얼어붙은 세계와 온화한 세계를 함께 덮을 수 없다. NearStars 천체들이 정확히 그 전이 구간에 있다.
나중에 강제력 기반으로 다시 짠다면 Byrne & Goldblatt이 출발점이고, 민감도는 숫자가 아니라 상태의
함수가 되어야 한다.

## 인용

**Layer 1 — 일반 이론**

- **[Robinson & Catling 2012](https://arxiv.org/abs/1209.1833)**, ApJ 757, 104
  ([`2012ApJ...757..104R`](https://ui.adsabs.harvard.edu/abs/2012ApJ...757..104R)). 해석적 회색 two-stream 복사-대류 모형. 조성은 광학깊이-기압 거듭제곱
  법칙과 단열선 스케일링으로 들어온다. 저자들이 금성·목성·타이탄으로 검증했다. *ar5iv에 쓸 만한
  전문이 없어서*, 이 문서는 모형의 구조와 검증 대상을 ADS 초록에서 인용하고 식은 옮기지 않았다.
- **[Robinson & Catling 2014](https://arxiv.org/abs/1312.6859)**, Nature Geoscience 7, 12
  ([`2014NatGe...7...12R`](https://ui.adsabs.harvard.edu/abs/2014NatGe...7...12R)). 적외선 투명도의 기압 의존성에서 나오는, 두꺼운 대기 공통의 약 0.1 bar
  대류권계면. 구조 정합성 점검에 사용.
- **[Pierrehumbert 2010](https://ui.adsabs.harvard.edu/abs/2010ppc..book.....P)**,
  *Principles of Planetary Climate* ([`2010ppc..book.....P`](https://ui.adsabs.harvard.edu/abs/2010ppc..book.....P)). 회색·밴드 모형 온실 관계식의 교과서
  유도. 허용되는 교과서 예외.

**Layer 2 — 불투명도 자료**

- **[Karman 2019](https://ui.adsabs.harvard.edu/abs/2019Icar..328..160K)**, Icarus 328, 160
  ([`2019Icar..328..160K`](https://ui.adsabs.harvard.edu/abs/2019Icar..328..160K)). HITRAN 충돌유발흡수 섹션. 위 CIA 쌍 표의 출처이며 CO₂–H₂ 부재도
  여기서 나온다. 프리프린트 없음, bibcode만.
- **[Gordon 2017](https://ui.adsabs.harvard.edu/abs/2017JQSRT.203....3G)**, JQSRT 203, 3
  ([`2017JQSRT.203....3G`](https://ui.adsabs.harvard.edu/abs/2017JQSRT.203....3G)). HITRAN2016 선 목록. 표준 자료원으로 인용.
- **[Byrne & Goldblatt 2014a](https://ui.adsabs.harvard.edu/abs/2014GeoRL..41..152B)**,
  GRL 41, 152, 그리고 **[2014b](https://arxiv.org/abs/1409.1880)**, Clim. Past 10, 1779
  ([`2014CliPa..10.1779B`](https://ui.adsabs.harvard.edu/abs/2014CliPa..10.1779B)). 고농도 강제력(CO₂ 50,000 ppmv까지, 최대 38.1 W/m²)과 시생대 후보 기체
  28종의 강제력.
- **[Ramirez 2018](https://arxiv.org/abs/1807.09504)**, Geosciences 8, 280
  ([`2018Geosc...8..280R`](https://ui.adsabs.harvard.edu/abs/2018Geosc...8..280R)). 고전적 CO₂+H₂O를 넘어선 거주가능대 정식화 리뷰. 비고전 조합의 진입점.
  ar5iv 추출 실패로 ADS 초록만 확인했고, 값을 위해서가 아니라 라우팅 참고로 인용한다.

**Layer 3 — 등온선 앵커**

- **[Feulner 2012](https://arxiv.org/abs/1204.4449)**, Rev. Geophys. 50, 2006
  ([`2012RvGeo..50.2006F`](https://ui.adsabs.harvard.edu/abs/2012RvGeo..50.2006F)). 흐린 젊은 태양 리뷰. §5.1이 등온선 앵커 다섯 중 넷을, §5.3이 CH₄ 3배
  보정을 준다. `docs/phase3/_papers/1204.4449.md`에 **캐시**.
- **[Kopparapu 2013](https://arxiv.org/abs/1301.6674)**, ApJ 765, 131
  ([`2013ApJ...765..131K`](https://ui.adsabs.harvard.edu/abs/2013ApJ...765..131K)). 거주가능대 한계. 최대온실 앵커(태양의 경우 1.70 AU에서 pCO₂ ~8 bar,
  Ts를 273 K로 고정하고 CO₂를 1~37.8 bar로 변화)와 위에 옮긴 Table 3 파라미터.
  `docs/phase3/_papers/1301.6674.md`에 **캐시**.
- **[Charnay 2013](https://arxiv.org/abs/1310.4286)**, JGR-Atmospheres 118, 10414
  ([`2013JGRD..11810414C`](https://ui.adsabs.harvard.edu/abs/2013JGRD..11810414C)). 시생대 3차원 GCM. 조성 C(3.8 Ga에 CO₂ 0.1 bar + CH₄ 2 mbar → 약
  17 °C)가 독립 검증 줄. `docs/phase3/_papers/1310.4286.md`에 **캐시**.
- **[Goldblatt 2009](https://ui.adsabs.harvard.edu/abs/2009NatGe...2..891G)**,
  Nature Geoscience 2, 891 ([`2009NatGe...2..891G`](https://ui.adsabs.harvard.edu/abs/2009NatGe...2..891G)). N₂ 압력 확장 항(N₂ 총량 2배당 +4.4 °C).
  프리프린트 없음, bibcode만.
- **[Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H)**,
  Astrobiology 8, 1127 ([`2008AsBio...8.1127H`](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H)). 수정된 hazy CH₄ 온실. CH₄ 흡수계수 정정,
  pCO₂ ≥ 0.03 bar 요구, haze 형성은 기후를 식힌다. 프리프린트 없음.
- **[Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A)**, Astrobiology 16,
  873 ([`2016AsBio..16..873A`](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A), arXiv [1610.04515](https://arxiv.org/abs/1610.04515)).
  기후-광화학-미세물리 결합 hazy 시생대. 약 20 K 냉각, 자기제한적, 200 nm에서 τ ~5, 지표 UV 약
  97 % 감소. *ar5iv 추출 실패*, 수치는 ADS 초록에서.
- **[Byrne & Goldblatt 2015](https://ui.adsabs.harvard.edu/abs/2015CliPa..11..559B)**,
  Clim. Past 11, 559. 태양 흡수선에 의한 시생대 CH₄ 온난화 약화. CH₄ 보정을 비례가 아니라
  상한으로 둔 이유.
- **[Wolf & Toon 2013](https://ui.adsabs.harvard.edu/abs/2013AsBio..13..656W)**,
  Astrobiology 13, 656 ([`2013AsBio..13..656W`](https://ui.adsabs.harvard.edu/abs/2013AsBio..13..656W)). 온화한 시생대 기후를 뒷받침하는 GCM. 완결성을
  위해 적어두지만 ADS에 초록이 없고 프리프린트도 없어서 **이 문서의 어떤 수치도 여기서 오지
  않았다**.

**Layer 4 — 빌려온 모형 계산**

- **[Ramirez 2014](https://arxiv.org/abs/1405.6701)**, Nature Geoscience 7, 59
  ([`2014NatGe...7...59R`](https://ui.adsabs.harvard.edu/abs/2014NatGe...7...59R)). CO₂ 1.3~4 bar + H₂ 5~20 %로 조기 화성을 어는점 위로. *ar5iv에 쓸 만한
  전문이 없어서* 수치는 논문 자체의 ADS 초록에서 가져왔고, 캐시된 Hayworth 2020의 서술과 교차
  확인했다.
- **[Hayworth 2020](https://arxiv.org/abs/2004.09076)**, Icarus 345, 113770
  ([`2020Icar..34513770H`](https://ui.adsabs.harvard.edu/abs/2020Icar..34513770H)). 조기 화성의 CO₂–H₂ CIA. "현재 지구 플럭스의 32 %" 수치, Ramirez의 H₂
  문턱값, 그리고 N₂–H₂를 CO₂–H₂ 대리로 쓴다는 진술의 출처.
  `docs/phase3/_papers/2004.09076.md`에 **캐시**.
- **[Wordsworth & Pierrehumbert 2013](https://ui.adsabs.harvard.edu/abs/2013Sci...339...64W)**,
  Science 339, 64 ([`2013Sci...339...64W`](https://ui.adsabs.harvard.edu/abs/2013Sci...339...64W)). 초기 지구의 H₂–N₂ CIA 온난화. *Science 리포트,
  프리프린트 없음*. bibcode로 인용하고 수치는 ADS 초록에서.
- **[Kasting 1991](https://ui.adsabs.harvard.edu/abs/1991Icar...94....1K)**, Icarus 94, 1
  ([`1991Icar...94....1K`](https://ui.adsabs.harvard.edu/abs/1991Icar...94....1K)), "CO₂ condensation and the climate of early Mars". 최대온실 한계 뒤에
  있는 CO₂ 구름·알베도 논지. Kopparapu 2013과 Hayworth 2020을 통해 인용.

## Related

- [`tidally-locked-temperature-methodology.md`](tidally-locked-temperature-methodology.md)
  — 이 레시피가 상승폭을 얹는 대상인 `T_eq`와 낮밤 구조를 담당한다.
- [`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md) — 위성이라면
  `T_eq`가 별빛 값이 아니다. 식, 모행성의 열복사와 반사광, 조석 가열이 모두 들어온다. 이 문서의
  `Ts`를 그대로 쓰지 말고 그 `T_eq`에 `greenhouse_increment()`를 합성하되, 그쪽 적용 범위 4번을
  유념할 것.
- [`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md) — 여기서 가정한
  대기가 애초에 유지되는지를 판정하고, 조성·기압을 소유한다.
- [`atmosphere-reflected-color-methodology.md`](atmosphere-reflected-color-methodology.md)
  — 여기서 지표를 식히는 그 haze가 천체의 반사색을 정한다.
- [methodology-index](methodology-index.md) — 모든 도출값 레시피의 인덱스.
