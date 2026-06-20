<!-- 거대행성·아성단 자기장을 에너지플럭스 dynamo 스케일링으로 도출하는 방법(논문 근거) -->
# 행성/아성단 자기장 근거 — 에너지플럭스 다이나모 스케일링

**가스 거대 행성 및 아성단(substellar)** 천체의 dipole 자기장을 도출하기 위한
방법 레퍼런스다. [J₂ Radau–Darwin worked example](principia-geopotential-data.md)
과 같은 "가짜 측정이 아니라 관계식 + calibration 을 인용한다" 는 정신을 따른다.
거대 행성의 자기장은 결코 직접 측정되지 않으므로 (in-situ 자력계도, 분해된 Zeeman
신호도 없음), 큐레이션 값은 근거 있는 스케일링 법칙에서 나와야 한다. "Jupiter 를
질량으로 스케일한다" 는 식이 아니다. 그것은 물리적으로 틀렸다 (아래 참고).

이 문서가 거대 행성/아성단 다이나모 방법의 canonical 거처다. 암석 행성 자기장
방법 (RM22 = Rodríguez-Mozos & Moya 2022, `2203.01065`) 은 TRAPPIST-1 계열
decisions 와 Phase 3 스킬의 `mod-grounded-fields.md` 에 있다.

## 법칙

Christensen, Holzwarth & Reiners 2009 (Nature 457, 167, `2009Natur.457..167C`)
는 빠르게 자전하는 천체의 다이나모 자기장 세기가, 자전 속도나 질량이 직접
결정하는 것이 아니라, 대류성 내부를 관통하는 **에너지 플럭스** (단위 면적당
광도) 로 결정된다는 것을 보였다. 다이나모 표면에서의 평균 자기장은 다음과 같이
스케일한다.

    B_dyn  ∝  (energy flux)^(1/3)  ·  ρ^(1/6)

폭넓은 천체 부류에 대해 열역학-효율 인자가 ≈ 1 이다. Reiners & Christensen
2010 (A&A 522, A13, `2010A&A...522A..13R`, arXiv **1007.1514**, cached) 은 이를
질량, 광도, 반지름 (태양 단위) 으로 쓴다.

    B_dyn  =  4.8 · (M · L² / R⁷)^(1/6)   [kG]

결정적으로, 천체가 임계 (포화) 한계 이상으로 자전하는 한 자기장은 **자전 속도와
무관하다**. 이 조건은 고립된 갈색왜성, 젊은 외계행성, 그리고 별에 매우 가깝게
조석 고정되지 않은 거대 행성에 대해 성립한다. 선형 질량 스케일링을 깨뜨리는
물리적 결과는 이것이다. **L 은 천체 자신의 내부 (냉각) 광도이며, 천체가 젊을 때
크고 식으면서 감소한다.** 따라서 젊은 거대 행성은 같은 질량의 늙은 거대 행성보다
*더 강한* 자기장을 가지며, 젊은 sub-Jupiter 가 늙은 Jupiter 를 능가할 수 있다.
"Jupiter 의 430 µT 를 질량으로 축소한다" 는 방향을 거꾸로 잡는다.

### 행성 표면에서의 dipole 자기장

거대 행성 (M < 13 M_J) 의 경우 다이나모는 가시 표면 아래에 자리한다 (Jupiter 에서
≈ 0.83 R). Reiners & Christensen 은 적도 표면 dipole 을 다이나모 표면 자기장과
다음과 같이 관계 짓는다.

    B_dip^eq  =  B_dyn / (2√2)

(인자 2: dipole 은 다이나모 표면 rms 자기장의 절반. 인자 √2: 적도 dipole 은
rms dipole 의 1/√2), 여기에 질량 의존적인 깊이 감쇠가 더해진다. 극 dipole 은
적도의 두 배다. B_dip^pol = 2·B_dip^eq.

## 실용 보간 공식 (논문 자체 값에 calibrate)

내부 냉각 광도 L(M, age) 를 처음부터 다시 도출하는 대신 (그 자체가
Burrows/Fortney 트랙으로 근거화되어야 한다), Reiners & Christensen 2010 이
표로 제시한 **발표된, 깊이 보정된 dipole 값** 에 앵커를 잡고 (질량, 나이) 에서
보간한다.

    B_dip^pol(M, age) = 9 G · (age / 4.5 Gyr)^(−0.33) · (M / M_Jup)^0.93
    B_dip^eq = B_dip^pol / 2          (1 G = 100 µT)

- **0.93 질량 지수** 는 논문의 "5 M_J 행성은 모든 나이에서 1 M_J 보다 4–5배
  강하다" 를 재현한다 (5^0.93 ≈ 4.5).
- **−0.33 나이 지수** 는 그들의 1 M_J 냉각 트랙을 재현한다 (수 Myr 에 극
  ~100 G → 4.5 Gyr 에 ~9 G → 10 Gyr 에 <10 G).

### 검증 — 공식이 논문의 발표된 천체를 재현한다

| Body | M (M_J) | age (Gyr) | formula B_pol | paper B_pol | match |
|---|---|---|---|---|---|
| Jupiter | 1.00 | 4.5 | 9.0 G | 9 G (Connerney polar 8.4 G) | ✓ |
| ε Eri b (paper's M sin i) | 1.55 | 1.7 | 18.7 G | 19 G (their Table 4.3) | ✓ |
| 1 M_J young end | 1.00 | 0.003 | 101 G | ~100 G | ✓ |
| 1 M_J old end | 1.00 | 10 | 6.9 G | <10 G | ✓ |

공식에서 나온 적도 Jupiter = 4.5 G = 450 µT 로, Jupiter 의 실제 ~4.3 G 적도
표면 자기장과 일치한다. 이 보간은 **calibrate 된 거대 행성 영역 안에서만**
사용한다 (0.3 ≲ M ≲ 10 M_J, age ≳ 0.2 Gyr, 빠른 자전).

## 유효 영역 — 세 가지 regime

이 법칙은 **H/He 가스 거대 행성과 갈색왜성** 을 위해 만들어졌고 그 위에서
검증되었다. 어떤 방법을 적용할지는 천체 부류가 결정한다.

1. **진짜 거대 행성, 0.3 ≲ M ≲ 13 M_J** — 위의 보간 공식을 적용한다.
   (NearStars: ε Eri b, GJ 896 A b, ε Ind A b.)
2. **갈색왜성, 13–70 M_J** — B_dyn 을 직접 사용한다 (다이나모가 표면 근처).
   질량이 큰 BD 는 젊을 때 수 kG 에 이르고 10 Gyr 에 ~10배 약해진다.
3. **Sub-Saturn / sub-Neptune / Neptune-질량 (M ≲ 0.3 M_J)** — **검증 영역
   밖이다.** Reiners & Christensen 은 Saturn 이하를 명시적으로 제외한다.
   헬륨 분리가 전도 영역을 층화시키고 (Stevenson 1980) 표면 자기장 감소가
   "정량화하기 어렵기" 때문이다. 태양계 얼음 거대 행성 analog 를 사용하고
   (Neptune/Uranus ~0.1–0.5 G, 강하게 비-dipolar. Connerney 1991/Ness 1986),
   젊음/팽창이 내부 flux 를 높인다는 점에 유의하며, 값을 근거 있는 도출이 아니라
   자릿수 수준의 analog 로 표시한다.
   (NearStars: AU Mic b, c, e.)
4. **암석 행성** — 거대 행성 다이나모 법칙은 적용되지 **않는다**. 암석
   스케일링 RM22 (Rodríguez-Mozos & Moya 2022, `2203.01065`) + 조석-고정 패널티
   + Garraffo 2017 을 사용한다. (NearStars: AU Mic d.)

거대 행성/BD 논문을 암석 행성에 잘못 적용하는 것은 — 예컨대 지구질량 천체에
Reiners & Christensen 2010 을 인용하는 것은 — 논문이 실재해도 인용 오류다.

## Worked examples (NearStars 거대 행성)

입력은 큐레이션된 질량/반지름/나이 (Phase 2 앵커) 다. B_eq = B_pol/2.
Earth 대비 dipole moment = (B_eq / 4.5 G) · (R/R_Jup)³ · 20000 (Jupiter 의
moment ≈ B_eq = 4.5 G 에서 Earth 의 20000배).

| Body | M (M_J) | R (R_J) | age (Gyr) | B_eq | dipole (×Earth) | conf |
|---|---|---|---|---|---|---|
| ε Eri b | 0.66 | 1.05 | 0.44 | **660 µT** (540–810) | ~34 000 | low–med |
| GJ 896 A b | 2.26 | 1.10 | 0.1–0.95 | **2000 µT** (1600–3400) | ~120 000 | low |
| ε Ind A b | 7.6 | 1.12 | 3.5 | **3200 µT** (2600–3700) | ~3700 / 2600 → med | low–med |

Notes:
- **ε Eri b** — 젊어서 (0.44 Gyr gyrochronology, high conf) 0.66 M_J 인데도
  자기장이 Jupiter 를 *능가한다*. 예전의 "축소판 jovian, Jupiter 보다 ~7% 아래"
  (400 µT) 는 젊음 효과의 부호를 거꾸로 잡았다.
- **GJ 896 A b** — 호스트 나이가 실제로 불확실하며 (≲100 Myr PMS 대 ~950 Myr),
  그 범위에서 자기장이 ~2배 걸친다. 중앙값 2000 µT, 젊은 쪽 최대 3400.
- **ε Ind A b** — 7.6 M_J 는 갈색왜성 경계 가까이다. 0.93 질량 지수가 1–5 M_J
  calibration 위로 외삽되므로 중앙값이 추가 ~25% 계통오차를 안는다. 그래도
  여전히 "Jupiter 보다 훨씬 강함" regime 에 확고히 있다.

신뢰도는 **low–medium** 에 머문다. *방법* 은 근거 있고 검증되었지만, 입력
(나이를 통한 내부 광도, M sin i 인 경우의 질량, non-transit 거대 행성의 반지름)
이 각각 실질적 불확실성을 안고, dipole moment 가 R³ 로 스케일하기 때문이다.

## 인용

- **Christensen, Holzwarth & Reiners 2009**, Nature 457, 167 (`2009Natur.457..167C`).
  에너지플럭스 스케일링 법칙의 기원. *Nature letter, arXiv preprint 없음* —
  bibcode 로 인용 (ADS/Nature/PubMed 로 검증 가능. ar5iv `_papers/` 캐시에는 없음).
- **Reiners & Christensen 2010**, A&A 522, A13 (`2010A&A...522A..13R`, arXiv
  **1007.1514**). 거대 행성 + 갈색왜성에 대한 적용. 이 방법이 calibrate 된
  진화 트랙과 표로 제시된 dipole 값. `docs/phase3/_papers/1007.1514.md` 에
  **캐시됨** (au-mic / eps-eri / gj-896-a / eps-ind-a 참고문헌에 핀).
- **Yadav & Thorngren 2017**, ApJL 849, L12 (`2017ApJ...849L..12Y`, arXiv
  **1709.05676**, cached) — Christensen 2009 에너지플럭스 스케일링을 inflate 된
  **hot Jupiter** 에 적용한다 (Thorngren & Fortney 의 반지름-inflation 광도 사용).
  이 방법을 외계행성에 가장 직접적으로 적용한 사례. AU Mic 행성들에는 hot Jupiter
  영역 아래로 내려가는 하향 외삽으로 사용했다 (sub-Saturn He 분리 caveat 포함).
- **Rodríguez-Mozos & Moya 2022** (RM22), `2203.01065` — 암석 행성 자기장
  스케일링 (cached). 거대 행성이 아니라 AU Mic d 에 사용.
