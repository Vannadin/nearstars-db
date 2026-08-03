<!-- 노출/매장 얼음의 승화 수명과 존속 알베도 임계를 증기압 곡선+Hertz-Knudsen으로 도출하는 방법(논문 근거) -->
# 표면 얼음 존속 근거: 승화 수명과 알베도 임계

어떤 천체가 자기 궤도에서 **노출된 얼음을 유지할 수 있는지**, 그리고 그러려면
알베도가 얼마여야 하는지를 판정하기 위한 방법 레퍼런스다. 이건 겉모습만의 문제가
아니다. 얼음 표면, 밝은 알베도, 극관(ice cap) 맵, 저온화산 룩이 모두 같은 주장
하나에 기대고 있으므로, 그 주장에는 직관이 아니라 레시피가 필요하다. "별에서
멀리 있으니 얼음은 괜찮다" 가 바로 이 문서가 막으려는 실패 방식이다. 태양 기준
1.6 AU 상당의 일사량에 놓인 천체가 수 Myr 만에 반지름 전체를 승화로 잃을 수도
있다.

이 레시피를 구현한 계산기는 [`docs/ice-stability.html`](../ice-stability.html)
이다 (브라우저 안에서 도는 단일 페이지). 이 문서는 계산기의 숫자가 인용하는
근거이고, 계산기는 도구일 뿐 권위의 출처가 아니다.

## 관계식

세 조각이 이 순서로 결합한다.

**1. 고체의 증기압.** Fray & Schmitt 2009
([`2009P&SS...57.2053F`](https://ui.adsabs.harvard.edu/abs/2009P%26SS...57.2053F))
는 53종 순수 분자 고체에 대해 발표된 모든 측정과 열역학 관계식을 정리하고,
유효 범위와 편차를 명시한 피팅 곡선을 제시한다. 그들의 다항식 형태 (논문 Eq. 4) 는

    ln(P / bar)  =  A₀ + Σ Aᵢ / Tⁱ

이며, 계수는 종별·상(phase) 구간별로 주어지고 (논문 Table 5) 유효 구간도 함께
제시된다 (논문 Table 4). 단 H₂O 의 삼중점 아래에서는 Feistel & Wagner 2007 의
준경험 곡선
([`2007GeCoA..71...36F`](https://ui.adsabs.harvard.edu/abs/2007GeCoA..71...36F))
을 권고한다. 2006년 ice Ih Gibbs 포텐셜에서 만들어졌고 20–273.16 K 에서 유효하다
(논문 Eqs. 5–6).

    ln(P / P_t)  =  1.5 · ln θ  +  (1 − 1/θ) · Σ eᵢ θⁱ ,        θ = T / T_t

**2. 자유 승화 질량 플럭스.** 되돌아오는 플럭스가 없는 진공으로의 승화라면,
Hertz–Knudsen 관계식이 단위 면적당 손실을 준다.

    Φ(T)  =  P_vap(T) · √( m / 2πkT )        [kg m⁻² s⁻¹]

Schörghofer 2008
([`2008ApJ...682..697S`](https://ui.adsabs.harvard.edu/abs/2008ApJ...682..697S))
이 행성 얼음 손실에 쓰는 형태가 이것이며, 동시에 손실의 상한이다. 대기든 lag
층이든 혼합 얼음 기질이든, 있으면 손실은 줄어든다.

**3. 승화 냉각을 포함한 표면 온도.** 표면은 복사 평형에 있지 *않다*. 승화가
잠열을 실어 나가기 때문이다. 다음을 T 에 대해 푼다.

    σT⁴  +  L_sub(T) · Φ(T)  =  F_abs

이 자기제한이 휘발성 종의 답을 결정한다. Chaos 궤도의 CO₂ 표면은 복사 평형값
234 K 가 아니라 105 K 에 앉는다. 복사가 입력을 상쇄하기 훨씬 전에 승화 항이
지배하기 때문이다. `F_abs` 는
[`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md) 의
네 항 위성 에너지 수지 (별빛에서 식(eclipse) 손실을 뺀 값, 더하기 모행성의
열복사와 반사광) 에서 온다.

**잠열은 독립 입력이 아니다.** 별도 출처에서 가져오면 증기압 곡선과 어긋날 위험이
있으므로, 같은 곡선에서 Clausius–Clapeyron 으로 유도한다.

    L_sub(T)  =  −R · d(ln P) / d(1/T)  /  M

## 실용 공식

전체 풀이 없이 빠르게 판정하려면, 노출된 물얼음은 연간 미터 단위 손실률로
지배된다고 보면 된다.

    ṙ(T)  =  Φ(T) / ρ_ice ,        ρ_ice = 930 kg m⁻³ (H₂O)

**존속 기준** 은 천체 나이에 걸쳐 누적된 손실이 천체 자신의 규모 (반지름, 또는
그게 문제라면 얼음 껍질 두께) 에 비해 작게 남는 것이다. Φ 가 T 에 지수적이므로
이 기준은 사실상 온도 임계이고, T 는 흡수 플럭스를 따라가므로 주어진 궤도에서
**알베도 임계** 로 환산된다. T 가 그 아래로 떨어질 때까지 알베도를 올리면 된다.

| exposed H₂O ice | loss rate | loss in 5.3 Gyr |
|---|---|---|
| 110 K | 1.5 × 10⁻¹⁰ m/yr | 0.8 m |
| 120 K | 1.4 × 10⁻⁸ m/yr | 76 m |
| 134 K | 2.6 × 10⁻⁶ m/yr | 14 km |
| 145 K | 7.9 × 10⁻⁵ m/yr | 420 km |
| 160 K | 3.9 × 10⁻³ m/yr | 20 000 km |

읽는 법은 이렇다. 수백 km 급 천체에서 **노출된 물얼음이 Gyr 시간 규모를 버티지
못하게 되는 지점이 ~145 K** 이고, 그 위로 10–15 K 마다 손실이 한 자릿수씩 더
불어난다.

## 검증

이 구현은 피팅에 쓰지 않은 발표값들을 재현한다.

| Check | Reference value | This recipe | Match |
|---|---|---|---|
| H₂O triple-point pressure | 611.657 Pa | 611.657 Pa | exact |
| L_sub(H₂O) at 200 K | 2.83 × 10⁶ J/kg | 2.833 × 10⁶ J/kg | 0.1 % |
| H₂O vapour pressure, 170–250 K | Marti & Mauersberger 1993 experimental fit | ratio 0.981–0.995 | within 2 % |
| CO₂ / CH₄ / CO triple-point pressures | Fray & Schmitt Table 4 | 0.35 % / 1.5 % / 0.08 % | ✓ |
| Exposed-ice Gyr threshold | ~145 K mean surface (Schörghofer 2008, buried under dust) | 145 K (exposed, 400 km body) | see caveat |
| Ceres illuminated polar cap | stable only if albedo > 0.5 (Hayne & Aharonson 2015) | same direction, same magnitude | ✓ |
| Ceres perennial cold traps | < ~110 K for 1 Gyr stability (Hayne & Aharonson 2015) | 110 K → 0.8 m in 5.3 Gyr | ✓ |

**145 K 일치에 대한 주의.** Schörghofer 의 임계는 먼지 lag 층에 *매장된* 얼음이
태양계 나이에 걸쳐 표층 수 미터 안에서 살아남는 조건이다. 우리 쪽은 400 km 천체
위의 *노출된* 얼음이 5.3 Gyr 를 버티는 조건이다. 두 기준은 같은 진술이 아니며,
같은 온도로 떨어진 이유는 양쪽 모두 "Gyr 에 걸쳐 손실 ≲ 문제가 되는 규모" 를 묻기
때문일 뿐이다. 이 일치는 공유 임계가 아니라 플럭스 법칙에 대한 sanity check 로만
받아들인다.

알려진 천체를 이용한 독립 앵커 확인 (계산기의 태양계 preset). Europa 와
Enceladus 는 안정한 얼음 지각을 돌려주고, Ceres 는 영구 음영 밖에서 노출 얼음이
불안정하다고 돌려주며, 1 AU 의 맨 얼음 표면은 근일점 규모 통과당 ~1 m 를 돌려준다.
혜성 침식에서 관측되는 자릿수와 같다.

## 유효 영역: 네 가지 regime

1. **노출된 얼음, refractory 가 적은 경우.** 레시피가 그대로 적용되며 Φ 가 답이다.
2. **lag 층 아래 매장된 얼음.** 손실이 자릿수 단위로 떨어지고, 건조 mantle 을 통한
   확산이 제한 인자가 된다. `z = √(2 D ρ_v t / ρ_ice)` 다. Schörghofer 2008 과
   Schörghofer 2016
   ([`2016Icar..276...88S`](https://ui.adsabs.harvard.edu/abs/2016Icar..276...88S))
   가 표준 처리법이다. 다만 확산 계수 D 는 우리 계산기에서 가정 입력이므로
   **후퇴 깊이는 자릿수 수준이고, 도출값으로 인용할 수 있는 건 노출 경우뿐이다.**
   lag 층이 애초에 형성되는지 여부는 얼음 대 refractory 비에 달려 있고, 그건 별개
   질문이다.
3. **에너지 제한 (해당 종이 고체로 존재할 수 없음).** 삼중점에서의 승화조차 흡수
   플럭스를 복사로 내보내지 못하는 경우, 그 궤도에서 그 종의 고체 표면은 불가능하다.
   이때 손실률은 흡수 플럭스 전량을 상전이로 돌렸을 때의 상한이 된다. 표면 온도는
   삼중점에서 상한이 걸리고, 판정은 느린 손실이 아니라 "고체 불가" 라는 단호한
   결론이다.
4. **내부 열이 상당한 천체.** 여기서 쓰는 에너지 수지는 외부 항만 포함한다. 조석
   가열되는 천체라면 먼저 내부 플럭스로 표면 온도를 올려야 하며
   ([`tidal-heating-methodology.md`](tidal-heating-methodology.md) 참고), 그 결과
   regime 이 몇 단계 이동할 수 있다. 강하게 가열되는 천체 위의 얼음 표면은 모순이고,
   이 레시피는 스스로 그걸 잡아내지 못한다.

전 구간에 걸리는 한계가 둘 더 있다. 계산은 **순수 단일 종** 에 대해서만 하는데,
실제 표면은 혼합물이고 혼합물의 증기압은 어떤 순수 성분보다도 낮으므로 손실률은
상한이다. 그리고 고체 밀도는 종별 명목값이다. 깊이와 수명에는 선형으로 들어가지만
승화 물리 자체에는 들어가지 않는다.

## Worked example: Chaos (Alpha Centauri A b V)

Phase 2/3 앵커에서 온 입력은 L = 1.521 L☉, 궤도 거리 1.6 AU 상당, 반지름 400 km,
나이 5.3 Gyr, 그리고 위성 에너지 수지에서 오는 모행성 항 (열복사 0.33 W/m²,
반사광 0.14 W/m², 식 손실 1.3 %) 이다.

| albedo | F_abs | T_rad | T_surf | loss rate | 400 km lost in | loss over 5.3 Gyr |
|---|---|---|---|---|---|---|
| 0.70 | 60.0 W/m² | 180 K | 175 K | 8.8 × 10⁻² m/yr | 4.5 Myr | body destroyed |
| 0.80 | 40.0 | 163 | 162 | 6.7 × 10⁻³ | 60 Myr | body destroyed |
| 0.85 | 30.0 | 152 | 152 | 4.8 × 10⁻⁴ | 830 Myr | body destroyed |
| **0.875** | 25.0 | 145 | 145 | 7.7 × 10⁻⁵ | 5.2 Gyr | **≈ the whole radius: the threshold** |
| 0.91 | 18.0 | 134 | 134 | 2.3 × 10⁻⁶ | 180 Gyr | 12 km of 400 km |
| 0.95 | 10.1 | 115 | 115 | 2.0 × 10⁻⁹ | 2 × 10⁵ Gyr | 10 m |

board 가 이걸 읽는 방식은 이렇다. 원래의 알베도 0.70 은 그냥 어두운 게 아니라
**불가능** 했다. 5.3 Gyr 나이를 상대로 이 위성은 4.5 Myr 만에 승화로 사라졌을
것이다. 존속에는 알베도 ≥ 0.875 가 필요한데, 이는
[`surface-color-albedo-methodology.md`](surface-color-albedo-methodology.md) §6 의
신선한 물얼음 대역 (0.6–0.8) 을 넘고, 알려진 가장 밝은 천체인 Enceladus (0.81) 도
넘는다. 채택값 0.91 은 임계를 간신히가 아니라 손실률 기준 ~33배 여유로 넘긴다.
요구 알베도가 측정된 모든 analog 를 초과한다는 사실이 바로 Phase 4 행이 pass 가
아니라 오너 override 를 다는 이유다. 레시피는 0.91 을 허가하는 게 아니라 그 값의
대가를 매긴다.

## 인용

- **Fray & Schmitt 2009**, Planet. Space Sci. 57, 2053
  ([`2009P&SS...57.2053F`](https://ui.adsabs.harvard.edu/abs/2009P%26SS...57.2053F)).
  모든 종의 증기압 출처다. 정리된 측정값, 피팅 곡선, 구간별 유효 범위와 편차를
  담고 있다. *Elsevier 유료, arXiv preprint 없음*. 오너의 기관 접근으로 입수해
  git 밖 `docs/phase3/_papers/_fray2009.pdf` 에 캐시했고 출처는
  `_fray2009.PROVENANCE.txt` 에 기록했다 (해당 폴더는 gitignored 이므로 논문 자체는
  repo 에 없다).
- **Feistel & Wagner 2007**, Geochim. Cosmochim. Acta 71, 36
  ([`2007GeCoA..71...36F`](https://ui.adsabs.harvard.edu/abs/2007GeCoA..71...36F)).
  삼중점 아래에서 쓰는 H₂O 승화 곡선. 2006년 ice Ih Gibbs 포텐셜 기반이고
  20–273.16 K 에서 유효하다. Fray & Schmitt 가 물에 대해 권고한 곡선이다.
- **Marti & Mauersberger 1993**, Geophys. Res. Lett. 20, 363
  ([`1993GeoRL..20..363M`](https://ui.adsabs.harvard.edu/abs/1993GeoRL..20..363M)).
  170–250 K 물얼음 증기압의 독립 실험값. 검증 표의 교차 확인용으로만 쓰고 입력으로는
  쓰지 않는다.
- **Schörghofer 2008**, ApJ 682, 697
  ([`2008ApJ...682..697S`](https://ui.adsabs.harvard.edu/abs/2008ApJ...682..697S)).
  대기 없는 천체의 얼음 수명에 대한 표준 처리다. Hertz–Knudsen 손실, 먼지 lag 층
  regime, 그리고 태양계 나이에 걸친 ~145 K 매장 얼음 임계를 다룬다.
- **Schörghofer 2016**, Icarus 276, 88
  ([`2016Icar..276...88S`](https://ui.adsabs.harvard.edu/abs/2016Icar..276...88S)).
  온도, 얼음 손실, 충돌 교반의 비동기 결합. lag 층 regime 이 문제가 될 때 얼음까지의
  깊이를 구하는 레퍼런스다.
- **Hayne & Aharonson 2015**, JGR Planets 120, 1567
  ([`2015JGRE..120.1567H`](https://ui.adsabs.harvard.edu/abs/2015JGRE..120.1567H)).
  Ceres 열안정성 모델링. 영구 표면 얼음에 대한 ~110 K / 1 Gyr 기준과, 햇빛 받는
  극관에는 알베도 > 0.5 가 필요하다는 결론을 담는다. 여기서 쓴 알베도 임계 논리에
  가장 가까운 발표 사례이며, 임계가 옳은 방향으로 작동하는지에 대한 독립 확인이다.
- **Brown & Ziegler 1979**, Adv. Cryogenic Engineering 25, 662. Fray & Schmitt 가
  정리한 CO₂ 및 CH₄ 계수의 상류 출처다. *비-ADS 예외*. ADS 레코드가 없는 단행본
  시리즈 권이며, Fray & Schmitt 의 정리를 통해서만 쓰인다. 우리가 인용하고 검증하는
  대상도 그 정리다.
- **Heller & Barnes 2013** ([arXiv:1209.5323](https://arxiv.org/abs/1209.5323), cached).
  `F_abs` 를 공급하는 위성 에너지 수지.
  [`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md) 참고.

## Related

- [`moon-energy-budget-methodology.md`](moon-energy-budget-methodology.md) — `F_abs`
  를 공급한다. 이 레시피가 가장 민감하게 반응하는 입력이다.
- [`surface-color-albedo-methodology.md`](surface-color-albedo-methodology.md) —
  임계를 판정할 기준이 되는 표면별 Bond 알베도 대역. 알베도 0.91 을 선택이 아니라
  override 로 만드는 근거가 §6 이다.
- [`tidal-heating-methodology.md`](tidal-heating-methodology.md) — 여기 수지에서는
  내부 열을 제외했으므로, 가열된 천체를 판정하기 전에 더해야 한다.
- [`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md) —
  대기 탈출 쪽 대응편. "가진 것을 유지할 수 있는가" 라는 같은 질문을 한 층 위에서
  묻는다.
- [methodology-index](methodology-index.md) — 모든 도출값 레시피의 살아있는 인덱스.
