<!-- 대기 온실 상승폭(T_surf − T_eq)을 문헌 iso-Ts 격자로 도출하는 방법(논문 근거) -->
# 온실 상승폭 근거화: 문헌 iso-Ts 격자

실제 대기를 가진 암석 천체의 **온실 상승폭**

    ΔT_gh  =  T_surface  −  T_eq

을 도출하는 방법 문서다. 복사 평형 온도는 교과서 닫힌 형태로 구할 수 있지만 상승폭은 그렇지 않다.
상승폭은 복사-대류 모형이나 대순환 모형이 내놓는 결과값이고, 레시피 없이 숫자만 적는 것은
[도출값 근거화 규율](methodology-index.md)이 금지하는 back-of-envelope에 해당한다.

상승폭의 canonical 문서는 여기다. `T_eq` 자체와 동기 자전 천체의 낮밤 구조는
[`tidally-locked-temperature-methodology.md`](tidally-locked-temperature-methodology.md)가,
그 대기가 애초에 유지되는지는
[`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md)가 담당한다.

계산기는 [`scripts/refs/greenhouse_dt.py`](../../../scripts/refs/greenhouse_dt.py)다.

## 복사강제력 × 기후민감도로 가지 않는 이유

가장 손이 가는 방법은 복사강제력(W/m²)에 기후민감도(K per W/m²)를 곱하는 것이다. 두 항 자체는
문헌에 있다. [Byrne & Goldblatt 2014a](https://ui.adsabs.harvard.edu/abs/2014GeoRL..41..152B)는
CO₂ 강제력을 100 ppmv에서 50,000 ppmv까지 계산해(최대 38.1 W/m²) 고농도에서 어긋나는 IPCC
간이식을 대체하는 표현식을 제시했고,
[Byrne & Goldblatt 2014b](https://arxiv.org/abs/1409.1880)는 이를 시생대 기체 28종으로 확장했다.
문제는 곱이다. 민감도 자체가 수증기 되먹임과 얼음-알베도 되먹임을 통해 온도에 의존하므로,
얼어붙은 세계와 온화한 세계를 하나의 λ로 이을 수 없다. NearStars 천체들이 바로 그 전이 구간에
있어서, 이 레시피는 곱셈 대신 발표된 모형 출력을 직접 앵커로 쓴다.

## 관계식: (입사량, CO₂ 컬럼) 평면의 iso-Ts 등온선

1 bar 배경 대기를 가정한 1차원 복사-대류 계산들은 한 가지 결론으로 모인다. 목표 지표온도를
정해놓으면, 입사량이 줄어들 때 필요한 CO₂ 분압이 급격히 올라간다. **Ts = 273 K** 등온선을
고정하는 세 점은 이렇다.

| S/S₀ | Ts = 273 K에 필요한 pCO₂ | 출처 |
|---|---|---|
| 0.80 | 0.01 bar | [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1, 후기 시생대 |
| 0.75 | 0.06 bar | [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1, 초기 시생대 |
| 0.346 | ~8 bar | [Kopparapu 2013](https://arxiv.org/abs/1301.6674), 최대온실 한계(1.70 AU) |

**Ts = 288 K** 등온선은 두 점으로 고정한다([Feulner 2012](https://arxiv.org/abs/1204.4449) §5.1).
S/S₀ = 0.80에서 0.1 bar, S/S₀ = 0.75에서 0.3 bar다.

Kopparapu 앵커는 격자점 하나가 아니라 등온선의 물리적 끝이다. 약 8 bar를 넘기면 CO₂의 레일리
산란이 온실 심화보다 빠르게 알베도를 올려서 **CO₂를 더 넣어도 더워지지 않는다**. 거주가능대의
바깥 경계가 여기다.

## 실용 공식

각 등온선을 `S/S₀`에 대해 `log₁₀ pCO₂`의 구간별 선형으로 보간하고, 천체가 273 K 등온선에서
얼마나 떨어져 있는지 읽는다.

    pCO₂_eff  =  pCO₂ · 3            (CH₄ 혼합비가 대략 1e-4 이상일 때)

    Ts  =  273 K  +  m(S) · log₁₀(pCO₂_eff / pCO₂_273(S))  −  ΔT_haze  +  ΔT_N2

    m(S)  =  15 K / log₁₀( pCO₂_288(S) / pCO₂_273(S) )      [CO₂ 10배당 K]

    ΔT_gh  =  Ts  −  T_eq,        T_eq = 278.6 K · (S/S₀)^¼ · (1 − A)^¼

항마다 근거가 붙는다.

- **CH₄ 보정, 3배.** [Feulner 2012](https://arxiv.org/abs/1204.4449) §5.3(Kiehl & Dickinson
  1987을 인용)에 따르면 CH₄ 혼합비 1e-4는 같은 지표온도에 필요한 CO₂를 "약 3배" 낮춘다. 이
  보정을 더 큰 CH₄ 양에 비례해 키우면 안 된다.
  [Byrne & Goldblatt 2015](https://ui.adsabs.harvard.edu/abs/2015CliPa..11..559B)는 태양 흡수선
  때문에 시생대 CH₄의 온난화가 오히려 *약해진다*는 것을 보였고,
  [Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H)은 흡수계수 오류를
  고치면서 CH₄ 온실을 하향 수정했다.
- **ΔT_haze = 20 K**, haze가 형성된 경우.
  [Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A)은 프랙탈 유기 haze가 지표를
  "약 20 K" 식히지만 그 냉각이 **자기제한적**이라는 것을 보였다(두꺼워지면 스스로를 가린다).
  따라서 20 K는 기울기가 아니라 상한이다. haze는 CH₄/CO₂가 대략 0.1을 넘으면 생기고
  ([Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H);
  [Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A)), 계산기가 기본으로 이
  조건을 검사한다.
- **ΔT_N2 = 총압 2배당 4.4 K.**
  [Goldblatt 2009](https://ui.adsabs.harvard.edu/abs/2009NatGe...2..891G)는 시생대 CO₂·CH₄
  수준에서 현재 대기 N₂ 총량을 두 배로 늘리면 기존 흡수선의 압력 확장으로 4.4 °C가 더워진다는
  것을 보였다.

### 검증: 공식 대 발표된 계산

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
| Kopparapu 2013 최대온실 | 0.346 | 8 bar | — | 273.0 K | 273 K | 앵커 |

이 중 진짜 시험은 두 줄이다. **현재 지구가 1.1 K 낮게**, **Charnay의 3차원 GCM이 2.0 K 낮게**
나오는데 둘 다 별도 튜닝이 없다. Kiehl & Dickinson 줄은 CH₄ 보정을 독립적으로 시험해 288 K를
정확히 재현한다.

가장 강한 검증은 애초에 맞추지 않은 쪽에서 나온다. 등온선을 조기 화성(`S/S₀ = 0.32`)까지
연장하면 **pCO₂ ≈ 11 bar**가 필요한데, 이는 최대온실 컬럼 약 8 bar를 넘으므로 도달 불가다.
CO₂와 H₂O만으로는 조기 화성을 273 K까지 데울 수 없다는 발표된 결론
([Kasting 1991](https://ui.adsabs.harvard.edu/abs/1991Icar...94....1K);
[Ramirez 2014](https://arxiv.org/abs/1405.6701);
[Hayworth 2020](https://arxiv.org/abs/2004.09076))이 시생대 지구 앵커만으로 복원된다.

## 적용 범위

1. **보정된 상자: `0.75 ≤ S/S₀ ≤ 1.0`, `pCO₂ ≤ 0.3 bar`, 총압 ~1 bar, N₂ 배경, 무산소 또는
   지구형.** 이 안에서는 ±5 K를 기대한다.
2. **외삽 구간: `0.35 ≲ S/S₀ < 0.75`.** 여기서 등온선은 초기 시생대 앵커와 최대온실 앵커를
   (S, log pCO₂) 평면에서 직선으로 이은 것이다. 양 끝은 발표된 점으로 묶여 있지만 중간은 자유롭다.
   **±10 K**로 보고 그 사실을 함께 적어야 한다. NearStars의 폴리페무스 위성들이 이 구간에 있다.
3. **최대온실 한계 아래(`S/S₀ ≲ 0.35`)**에서는 CO₂ 경로가 닫힌다. 이곳의 천체가 따뜻하려면
   환원성 충돌유발흡수가 필요하다. [Ramirez 2014](https://arxiv.org/abs/1405.6701)는 조기 화성을
   1.3~4 bar CO₂ **+ H₂ 5~20 %**로 273 K 위에 올리고,
   [Wordsworth & Pierrehumbert 2013](https://ui.adsabs.harvard.edu/abs/2013Sci...339...64W)은
   태양 플럭스 75 %에서 현재 N₂ 총량의 2~3배와 H₂ 혼합비 0.1로 초기 지구를 0 °C 위에 올린다
   (CO₂는 현재의 2~25배만 필요). **미량 H₂로는 이 효과를 살 수 없다.** CIA 항은 퍼센트 수준의
   H₂를 요구하고, 그러려면 강하게 환원된 맨틀과 탈출을 앞지르는 활발한 탈기체가 필요하다.
4. **구름은 제외되어 있다.** 모든 앵커가 구름 없는 계산이고, Kopparapu는 CO₂ 구름 온난화를
   빼놓았기 때문에 자기 바깥 경계가 보수적이라고 명시한다. 목표보다 몇 K 모자란 천체를 구름
   온난화로 변호할 수는 있지만, 그것은 추가 가정이므로 반드시 가정으로 기록해야 한다.
5. **폭주 온실이나 수증기 대기에는 쓰지 않으며**, H₂/He 외피에도 적용되지 않는다.

## 적용 예: 폴리페무스 위성들

α Cen A의 광도는 `L = 1.521 L☉`(큐레이션값, `db/systems/alpha_centauri_a.json`)이고 폴리페무스는
1.6 AU를 돈다. 따라서 모든 위성이 받는 값은 `S/S₀ = 1.521 / 1.6² = 0.594`로, **초기 시생대
지구(0.75)보다도 어둡고** 최대온실 한계(0.346)보다는 충분히 안쪽이다. 즉 원리적으로 물이 액체로
있을 수 있지만, 지구보다 훨씬 두꺼운 CO₂ 컬럼이 필요하다.

이 입사량에서 273 K 등온선은 **pCO₂ ≈ 0.40 bar**(CO₂만)이고, CH₄ 수 mbar가 있으면
**≈ 0.13 bar**로 내려간다. CO₂ 민감도는 10배당 21.4 K다.

| 천체 | 기록된 대기 | T_eq | 레시피 Ts | ΔT_gh | 기록된 ΔT |
|---|---|---|---|---|---|
| Cassandra | 1 bar N₂, CO₂ 3 %, CH₄ 3 mbar, 얇은 haze, A 0.35 | 220 K | haze 포함 **246 K** / haze 없이 **266 K** | +26 / +46 K | +45~50 K |
| Pandora | 1.1 bar, CO₂ 18 % + CH₄ + H₂S, A 0.30 | 224 K | **275 K** | +52 K | +70 K |

- **Cassandra**는 haze 문턱에 정확히 걸쳐 있다. CH₄/CO₂가 딱 0.1이라, haze 항이 논지 전체를
  좌우한다. haze를 인정하면 246 K의 얼음 세상이고, haze가 전혀 없다고 하면 266 K까지 오른다.
  이 위성은 애초에 눈에 보이는 호박색 haze를 갖도록 설계되었으므로 방어 가능한 창은
  **250~265 K**다. 물이 따뜻한 적도나 계절에만 열리는 부분 동결 세계이며, 이미 표면 서술이 그렇게
  말하고 있다. 전 지구 평균 270~275 K를 유지하려면 CO₂를 0.13 bar(1 bar 대기의 13 %, 기록값의
  네 배)까지 올리거나 퍼센트 수준의 H₂를 넣어야 한다.
- **Pandora**는 캐넌 조성 그대로 275 K가 나온다. 거주 가능하고 어는점 위이지만 기록된 290 K보다
  약 15 K 차다. 이 입사량에서 290 K에 닿으려면 pCO₂가 약 2 bar여야 하는데, 캐넌의 총압 ~1.1 atm과
  모순된다. 일관된 선택은 평균 지표온도를 275 K로 내리거나, CO₂ 구름 온난화를 명시적 가정으로
  끌어들이는 것이다(위 4번).

두 기록값은 모두 레시피 없이 부여되었고 둘 다 낙관적으로 나왔다. ±10 K 구간에 대해 Cassandra는
약 20 K, Pandora는 약 15 K 높다. 방법 자체의 신뢰도는 중간, 입력값(CO₂ 비율, haze 광학깊이,
알베도)의 신뢰도는 낮다.

## 인용

- **[Feulner 2012](https://arxiv.org/abs/1204.4449)**, Rev. Geophys. 50, 2006
  (`2012RvGeo..50.2006F`). 흐린 젊은 태양 문제 리뷰. §5.1이 등온선 앵커 다섯 중 넷을, §5.3이
  CH₄ 3배 보정을 준다. `docs/phase3/_papers/1204.4449.md`에 **캐시**.
- **[Kopparapu 2013](https://arxiv.org/abs/1301.6674)**, ApJ 765, 131
  (`2013ApJ...765..131K`). 갱신된 거주가능대 한계. 최대온실 앵커(1.70 AU에서 pCO₂ ~8 bar,
  Ts를 273 K로 고정하고 CO₂를 1~37.8 bar로 변화). `docs/phase3/_papers/1301.6674.md`에 **캐시**.
- **[Charnay 2013](https://arxiv.org/abs/1310.4286)**, JGR-Atmospheres 118, 10414
  (`2013JGRD..11810414C`). 시생대 3차원 GCM. 조성 C(3.8 Ga에 CO₂ 0.1 bar + CH₄ 2 mbar → 약 17 °C)가
  독립 검증 줄이다. `docs/phase3/_papers/1310.4286.md`에 **캐시**.
- **[Hayworth 2020](https://arxiv.org/abs/2004.09076)**, Icarus 345, 113770
  (`2020Icar..34513770H`). 조기 화성의 CO₂–H₂ CIA. "현재 지구 플럭스의 32 %" 수치와 Ramirez의 H₂
  문턱값 출처. `docs/phase3/_papers/2004.09076.md`에 **캐시**.
- **[Ramirez 2014](https://arxiv.org/abs/1405.6701)**, Nature Geoscience 7, 59
  (`2014NatGe...7...59R`). CO₂ 1.3~4 bar + H₂ 5~20 %로 조기 화성을 어는점 위로 올린다.
  *ar5iv에 쓸 만한 전문이 없어서*, 여기 쓴 수치는 논문 자체의 ADS 초록에서 가져왔고 캐시된
  Hayworth 2020의 서술과 교차 확인했다.
- **[Wordsworth & Pierrehumbert 2013](https://ui.adsabs.harvard.edu/abs/2013Sci...339...64W)**,
  Science 339, 64 (`2013Sci...339...64W`). 초기 지구의 H₂–N₂ CIA 온난화.
  *Science 리포트로 프리프린트 없음*. bibcode로 인용하고 수치는 ADS 초록에서 가져왔다.
- **[Goldblatt 2009](https://ui.adsabs.harvard.edu/abs/2009NatGe...2..891G)**,
  Nature Geoscience 2, 891 (`2009NatGe...2..891G`). N₂ 압력 확장 항(N₂ 총량 2배당 +4.4 °C).
  *프리프린트 없음*, bibcode만.
- **[Haqq-Misra 2008](https://ui.adsabs.harvard.edu/abs/2008AsBio...8.1127H)**,
  Astrobiology 8, 1127 (`2008AsBio...8.1127H`). 수정된 hazy CH₄ 온실. CH₄ 흡수계수 정정,
  pCO₂ ≥ 0.03 bar 요구, haze 형성은 기후를 식힌다. 프리프린트 없음, bibcode만.
- **[Arney 2016](https://ui.adsabs.harvard.edu/abs/2016AsBio..16..873A)**,
  Astrobiology 16, 873 (`2016AsBio..16..873A`, arXiv
  [1610.04515](https://arxiv.org/abs/1610.04515)). 기후-광화학-미세물리 결합 hazy 시생대. 약 20 K
  냉각, 자기제한적, 200 nm에서 τ ~5, 지표 UV 약 97 % 감소. *ar5iv 추출 실패*, 수치는 ADS 초록에서.
- **[Byrne & Goldblatt 2014a](https://ui.adsabs.harvard.edu/abs/2014GeoRL..41..152B)**,
  GRL 41, 152, 그리고 **[2014b](https://arxiv.org/abs/1409.1880)**, Clim. Past 10, 1779
  (`2014CliPa..10.1779B`). 고농도 복사강제력과 시생대 기체 28종. 여기서 수치로 쓰지는 않았고,
  강제력 경로를 왜 버렸는지의 근거이자 이 레시피를 강제력×민감도로 다시 짤 때의 출발점이다.
- **[Byrne & Goldblatt 2015](https://ui.adsabs.harvard.edu/abs/2015CliPa..11..559B)**,
  Clim. Past 11, 559. 태양 흡수선에 의한 시생대 CH₄ 온난화 약화. CH₄ 보정을 비례가 아니라
  상한으로 둔 이유다.
- **[Wolf & Toon 2013](https://ui.adsabs.harvard.edu/abs/2013AsBio..13..656W)**,
  Astrobiology 13, 656 (`2013AsBio..13..656W`). 온화한 시생대 기후를 뒷받침하는 시생대 GCM.
  완결성을 위해 적어두지만 ADS에 초록이 없고 프리프린트도 없어서 **이 문서의 어떤 수치도 여기서
  오지 않았다**.
- **[Kasting 1991](https://ui.adsabs.harvard.edu/abs/1991Icar...94....1K)**, Icarus 94, 1
  (`1991Icar...94....1K`), "CO₂ condensation and the climate of early Mars". 최대온실 한계 뒤에
  있는 CO₂ 구름·알베도 논지. Kopparapu 2013과 Hayworth 2020을 통해 인용.

## Related

- [`tidally-locked-temperature-methodology.md`](tidally-locked-temperature-methodology.md)
  — 이 레시피가 상승폭을 얹는 대상인 `T_eq`와 낮밤 구조를 담당한다. 닫힌 형태는 그 문서의
  Layer 1에서, 대기 몫은 이 문서에서 가져온다.
- [`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md) — 여기서 가정한
  대기가 애초에 유지되는지를 판정한다.
- [`atmosphere-reflected-color-methodology.md`](atmosphere-reflected-color-methodology.md)
  — 여기서 지표를 식히는 그 haze가 천체의 반사색을 정한다.
- [methodology-index](methodology-index.md) — 모든 도출값 레시피의 인덱스.
