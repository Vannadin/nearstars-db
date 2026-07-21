<!-- 행성·갈색왜성 내부열(잔여+Kelvin-Helmholtz+방사성) → T_int → 유효온도 T_eff를 도출하는 방법론 레퍼런스 -->
# 내부열 / 자발광 방법론: T_int와 유효온도

행성 또는 갈색왜성의 **비-조석 내부열**(자발광 `L_int`)을 도출하고, 그것을 내부 성분만으로
이루어진 유효온도 `T_int`로 변환한 다음, 복사 평형온도 `T_eq`와 결합해 바디의 실제 유효온도를
얻는 방법 레퍼런스다. [dynamo 스케일링 문서](planetary-dynamo-scaling.md)나
[조석가열 문서](tidal-heating-methodology.md)와 같은 정신을 따른다. 지어낸 측정치가 아니라,
관계식과 알려진 바디를 재현하는 calibration을 함께 인용한다.

이 값은 **NearStars에서 반복해 등장하는 도출값**이다. Polyphemus(α Cen A b), ε Ind A b, 그리고
이번 Proxima c에서 그때그때 쓰였기에, 여기에 canonical 근거 레시피로 정리해 둔다.

> 인용은 즉석 웹 검색이 아니라 NASA ADS(등록된 `ADS_API_TOKEN`)에 대조해 확정한다.
> arXiv id가 있으면 그것을, 없으면 권위 있는 ADS bibcode("no arXiv" 표시)를 쓴다.
> 검증된 목록은 §9를 참고하면 된다.
> 교과서가 아니라 실무용 레퍼런스다.

**범위 주의: 이 문서는 비-조석 내부열을 다룬다.** 아성단/행성 바디의 내부 에너지 수지에는
네 종류의 자매 열원이 있고, 두 문서로 나뉜다.

| Source | Covered where |
|---|---|
| Residual heat of formation (accretion + initial entropy) | **this doc** |
| Kelvin–Helmholtz gravitational contraction (the dominant giant-planet term) | **this doc** |
| Radiogenic (U/Th/K decay) + secular cooling (rocky bodies) | **this doc** |
| Helium rain / phase separation (Saturn-type), deuterium burning (>~13 M_J) | **this doc** |
| **Tidal dissipation** | [`tidal-heating-methodology.md`](tidal-heating-methodology.md) |

**복사 / 평형온도** `T_eq`(별이 전달하는 몫)는
[조석고정 온도 문서](tidally-locked-temperature-methodology.md)가 다룬다. 이 모든 항은 §1의 단일
관계식 `T_eff⁴ = T_eq⁴ + T_int⁴`로 **결합**되며, 여기서 `T_int`는 비-조석 열원만을 묶어 담는다
(조석 플럭스가 무시할 수 없는 수준이면 그 값을 `T_int`에 더한다, 해당 문서 참고).

## 목차

1. [관계식: T_eff⁴ = T_eq⁴ + T_int⁴](#1-관계식-t_eff--t_eq--t_int)
2. [냉각 트랙: L_int(M, age)의 거동](#2-냉각-트랙-l_intm-age의-거동)
3. [hot-start vs cold-start 초기 엔트로피 문제](#3-hot-start-vs-cold-start-초기-엔트로피-문제)
4. [Calibration: 관계식이 Neptune(과 Uranus 변칙)을 재현한다](#4-calibration-관계식이-neptune과-uranus-변칙을-재현한다)
5. [유효 영역: 바디 분류별 내부열](#5-유효-영역-바디-분류별-내부열)
6. [헬륨 비와 중수소 연소: 추가 항](#6-헬륨-비와-중수소-연소-추가-항)
7. [워크드 예제](#7-워크드-예제)
8. [정직함과 불확실성](#8-정직함과-불확실성)
9. [주석 달린 참고문헌](#9-주석-달린-참고문헌)
10. [관련 문서](#관련-문서)

---

## 1. 관계식: T_eff⁴ = T_eq⁴ + T_int⁴

바디는 표면에서 두 동력원의 합을 복사한다. 흡수한 뒤 재방출하는 별빛(평형 항)과 내부에서 새어
나오는 열(내부 항)이다. 둘 다 같은 표면에서 나오는 Stefan–Boltzmann 방출이므로 **플럭스가 더해지고**,
온도는 **네제곱으로** 더해진다.

    σ T_eff⁴  =  σ T_eq⁴  +  σ T_int⁴
    ⇒  T_eff⁴  =  T_eq⁴  +  T_int⁴

여기서

    T_int  =  ( L_int / (4 π R² σ) )^(1/4)

은 바디가 **자신의 내부 광도만으로** 가졌을 유효온도다(`L_int` = 내부 열 출력, `R` = 반경,
`σ` = Stefan–Boltzmann 상수). `T_eq`는 [조석고정 온도 문서](tidally-locked-temperature-methodology.md)에서
오는 복사 평형온도이며, 완전 재분배의 경우 `T_eq = T_★ √(R_★/2a) (1−A)^(1/4)`이다.

네제곱 덧셈 덕분에 영역(regime) 거동이 깔끔하다. **큰 항이 압도적으로 이긴다.**

- **복사 지배**(`T_eq ≫ T_int`, 가까운 궤도 또는 낮은 `L_int`)면 `T_eff ≈ T_eq`다.
  내부열은 무시할 만한 미미한 증분일 뿐이다. 대부분의 온대·고온 행성이 여기에 속한다.
- **내부열 지배**(`T_int ≫ T_eq`, 젊은 거대행성)면 `T_eff ≈ T_int`다. 바디는 **자발광** 상태로,
  별과 무관하게 자신의 열복사로 빛난다. 직접 촬영된 젊은 거대행성이 검출되는 방식이 정확히 이것이다
  (§3, Marois+ 2008).
- **비등**(`T_int ~ T_eq`, 멀리 떨어진 차가운 바디)이면 둘 다 중요하다. `T_eq` 자체가 작기 때문에
  *적당한* `L_int`만으로도 `T_eff`를 `T_eq`보다 눈에 띄게 끌어올릴 수 있다. 이것이 **Neptune 사례**(§4)와
  **Proxima c 사례**(§7)다.

별에서 멀어질수록 작은 내부 플럭스가 지배하게 되는 이유는, `T_eq`는 `a^(−1/2)`로 떨어지는 반면
`T_int`는 바디 자신의 냉각으로 정해져 *복사 입력과 무관*하기 때문이다. 충분히 멀어지면 고정된
`T_int` 바닥값이 사라져 가는 `T_eq`를 넘어선다.

> **에너지 수지 등가형.** 관측자들은 보통 **내부 플럭스 비**, 즉 바디가 흡수한 것보다 얼마나 더
> 많이 방출하는지를 인용한다. `f = L_int / L_absorbed`로 두면 `T_eff⁴ = T_eq⁴ (1 + f)`다. Neptune은
> `f ≈ 1.6`(흡수의 ~2.6배를 방출, §4)이고, 자발광 젊은 거대행성은 `f ≫ 1`, Polyphemus는 `f ≲ 0.06`(§7)다.

---

## 2. 냉각 트랙: L_int(M, age)의 거동

핵융합이 없는(또는 일시적 중수소 연소만 있는) 거대행성이나 갈색왜성에서 `L_int`는
**잔여 형성열 + Kelvin–Helmholtz 수축**이다. 바디가 천천히 수축하면서 중력 위치에너지를 열로
변환해 복사로 내보낸다. 이것은 [dynamo 문서](planetary-dynamo-scaling.md)가 자기장을 정하는 데 쓰는
**같은 내부 냉각 광도**다. 하나의 광도, 두 가지 결과(여기서는 열복사, 그쪽에서는 다이나모 자기장)인
셈이다. canonical 트랙은 Burrows, Baraffe/Chabrier, Fortney/Marley, Saumon/Marley 진화 모델
격자(§9)에서 온다.

그 트랙에서 나오는, 견고한 두 가지 정성적 스케일링이 있다.

- **젊을수록 밝고, 나이와 함께 단조 감소한다.** 거대행성은 형성 직후 가장 뜨겁고 밝으며, 이후로는
  영원히 식는다. Burrows 1997 / Baraffe 2003 트랙으로 추정한 차수는, ~1 M_J 행성의 `T_int`가 수 Myr에
  ~1000 K 이상이었다가 수 Gyr면 ~100 K 쪽으로 떨어지고, 10 Gyr면 ~100 K 아래로 내려간다. 감소는 초기에
  가파르고 그 뒤로는 느려서, Gyr 시간척도에서는 대략 `L_int ∝ age^(−1.3)`이다(이 거듭제곱이 dynamo
  문서의 *자기장* 지수 `age^(−0.33)`을 주는 바로 그것이다. `B ∝ L^(1/6)`이기 때문이다).
- **질량이 클수록 밝고, 더 오래 뜨겁게 유지된다.** 더 큰 중력 저장고와 더 느린 수축이 `L_int`(와
  `T_int`)를 더 오래 높게 유지한다. 10 M_J 천체는 ~Gyr 동안 자발광이지만, 토성 질량 천체는 ≲100 Myr
  안에 검출 한계 아래로 식는다.

NearStars에서의 실무적 함의는 이렇다. **늙고 저질량인 거대행성은 냉각 광도가 희미해 복사 지배**(Polyphemus,
§7)이고, **질량과 무관하게 젊은 거대행성은 자발광**(직접 촬영 영역, §3)이다. 거대행성이 어느 영역에
있는지는 host 별이 아니라 나이와 질량이 정한다.

여기서 `L_int(M, age)`를 처음부터 다시 도출하지는 **않는다**. dynamo 문서처럼 정직한 태도는 발표된
트랙(아성단 끝단은 Baraffe 2003 / Saumon & Marley 2008 / Sonora Bobcat, 행성 반경+광도는 Fortney 2007)에서
읽어 오거나, 태양계 얼음 거대행성이라면 *측정된* 내부 플럭스(§4)에 앵커링하는 것이다.

---

## 3. hot-start vs cold-start 초기 엔트로피 문제

**젊은** 거대행성(≲ 수백 Myr)에서 `L_int`는 행성이 태어날 때 가진 **초기 엔트로피**, 즉 형성 경로에
민감하게 의존하며, 이것이 젊은 나이에서 단연 가장 큰 불확실성이다.

- **hot start**: 행성이 중력적으로 붕괴하는 가스 덩어리(disk-instability류)의 높은 엔트로피를 유지한다.
  *밝게* 시작해서 ~100 Myr 동안 밝게 머문다.
- **cold start**: 강착 충격을 거치는 core-accretion(Pollack+ 1996)이 엔트로피의 상당 부분을 복사로
  날려 보내므로, 행성은 *훨씬 더 어둡게* 시작했다가 ~10²–10³ Myr 뒤에야 hot-start 트랙으로 수렴한다.

Marley+ 2007("On the Luminosity of Young Jupiters")는 두 시나리오가 ≲ 100 Myr 나이에서 `L_int`로 최대
~2 dex(`T_int`로 수백 K)까지 차이 난다는 것을 보였다. Spiegel & Burrows 2012는 둘을 구분하는
분광/측광 진단을 정리했다. 트랙은 바디가 ~1 Gyr보다 늙으면 **수렴**하므로, 이 모호성은 *오직* 젊고 직접
촬영된 거대행성에만 문제가 된다. Gyr 나이의 NearStars host에는 무관하다.

**NearStars 규칙.** 젊은(≲ 수백 Myr) 자발광 거대행성이라면 `L_int`를 점값이 아니라 **hot-start와
cold-start 트랙으로 둘러싸인 범위**로 보고한다. Gyr 나이의 바디(확정된 NearStars host 거대행성은 전부
여기 해당)라면 start 모호성이 이미 씻겨 나갔으니 식은 트랙을 그대로 쓴다.

---

## 4. Calibration: 관계식이 Neptune(과 Uranus 변칙)을 재현한다

이 관계식이 믿을 만한 이유는, 태양계 거대행성이 Voyager IRIS로부터 *측정된* 에너지 수지(방출 IR 대
흡수 별빛)를 갖고 있기 때문이다. 내부 플럭스는 가정이 아니라 직접 관측된 값이다.

| Body | T_eq (K) | T_eff measured (K) | emitted / absorbed | source |
|---|---|---|---|---|
| **Jupiter** | ~110 | ~124 | ~1.67 | Hanel+ 1981 |
| **Saturn** | ~81 | ~95 | ~1.78 | Hanel+ 1983 |
| **Neptune** | **~47** | **~59** | **~2.6** | Pearl & Conrath 1991 |
| **Uranus** | ~58 | ~59 | ~1.06 (≈ 1, anomalous) | Pearl+ 1990 |

**Neptune은 "내부열이 T_eff를 T_eq보다 끌어올린다"의 canonical 사례다.** Pearl & Conrath 1991(Voyager 2
IRIS)은 평형온도 `T_eq ≈ 46.6 K`에 대해 유효온도 `T_eff ≈ 59.3 K`를 측정했다. Neptune은 **흡수한 별빛의
~2.6배를 방출**한다. §1에 대입하면 `T_int = (T_eff⁴ − T_eq⁴)^(1/4) = (59.3⁴ − 46.6⁴)^(1/4) ≈ 52 K`,
즉 내부열만으로도 Neptune을 ~52 K까지 데울 수 있으며, 이는 태양이 30 AU에서 전달하는 ~47 K에 *비등*하다.
Neptune이 "겨우" 식고 있는 얼음 거대행성인데도 내부 항이 온도 수지를 지배하는데, 바로 그 거리에서는
복사 입력이 너무나 미약하기 때문이다.

**Uranus의 대조(이 부분을 읽어 두자).** Neptune과 질량·반경이 거의 쌍둥이인 Uranus는 흡수하는 만큼을
사실상 **그대로 방출**한다(Pearl+ 1990, 비 ≈ 1.06, 내부 플럭스가 오차 범위 안에서 0과 일치). 그래서
`T_eff ≈ T_eq`다. 그 외의 모든 면에서 비슷한 두 바디가 내부 플럭스로는 ~2.5배 차이 난다. 유력한 설명들(더
층상화·안정 성층화된 내부가 열을 가두거나, giant-impact 이력)은 아직 결론이 나지 않았다. Uranus는
**내부 플럭스가 (M, R, age)의 깔끔한 함수가 아니라는** 상시적 경고다. 두 쌍둥이가 큰 인자로 차이 날 수
있다. NearStars에서 이는 우리 신뢰도의 상한을 정한다. 얼음 거대행성 `L_int` 예측은 몇 배 인자 수준까지만
맞고, 그보다 정밀하지는 않다.

---

## 5. 유효 영역: 바디 분류별 내부열

바디 분류가 어느 메커니즘이 지배하는지와 추정이 얼마나 확실한지를 정한다.

1. **암석 행성: 방사성 + 영년 냉각이 지배하지만, 결실은 `T_eff`가 아니라 내부다.** 내부 플럭스는 장수명
   방사성 동위원소 붕괴(U, Th, ⁴⁰K) 더하기 잔여 강착열/영년열로 정해지며, Kelvin–Helmholtz 수축이 아니다
   (암석은 거의 수축하지 않는다). 그 규모는 **지구 열 플럭스 ~0.08–0.09 W/m²**(전역 ~46–47 TW, Sclater,
   Jaupart & Galson 1980; Davies 2013, 대략 절반은 방사성, 절반은 영년)다. 이는
   `T_int ≈ (0.087/σ)^(1/4) ≈ 35 K`에 대응하며, 어떤 온대·온난 `T_eq`에 대해서도 무시할 만하다. 그래서 거의
   모든 암석 행성에서 `T_eff ≈ T_eq`이고, §1의 표면온도 관계식은 암석 바디의 내부열에 아예 신경 쓰지 않는다.
   **바로 그것이 암석 영역이 위의 거대행성/얼음 거대행성 영역과 다른 이유다. 내부열의 적실성은 유효온도가
   전혀 아니라 *내부 열 수지*에 있다.** 같은 방사성 + 영년 광도가 **지온구배(geotherm)**를 정하고, 그
   지온구배가 NearStars가 암석 세계에 대해 실제로 art-direction하는 결과들을 끌고 간다.
   - **핵 대류 → 다이나모 자기장.** 핵이 다이나모를 유지할 만큼 오래 뜨겁게 대류하느냐는 열 이력의 문제다
     (Driscoll & Bercovici 2014는 지구의 *살아남은* geodynamo 대 금성의 *실패한* 다이나모를 바로 이 융해/
     방사능/전도도의 갈림에 묶는다). 이것이 [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md)의
     **암석 영역**이며(RM22 암석 스케일링, `2203.01065`), 거대행성의 `B ∝ L^(1/6)` 법칙은 암석에는 **적용되지
     않는다**.
   - **맨틀 대류 → 화산활동 → 탈가스.** 내부 열 수지가 화산활동 여부를 좌우하고, 이는
     [`exoplanet-atmosphere-methodology.md`](exoplanet-atmosphere-methodology.md)의 **Gate 3**에 공급되는
     **탈가스 공급량**을 정한다(죽어서 식은 내부는 2차 대기를 재공급할 수 없다).

   그러니 암석 바디라면 내부열을 `T_eff` 위의 증분이 아니라 *내부* 양(지온구배 → 화산활동/탈가스/다이나모)으로
   끌고 간다. §1 관계식은 극도로 차가운(멀리 있고 어두운 별을 도는) 암석 바디에서만 겨우 경쟁하고, 그조차
   약하다. 반면 **조석열**은 가까운 이심 궤도의 바디에서 방사성 열을 압도할 수 있고, 그러면 *같은* 내부 수지를
   지배하는데, 그것은 [조석가열 문서](tidal-heating-methodology.md)의 영역이다(지구 질량 바디의 방사성 열은
   ~0.08 W/m²이고, 조석가열은 그것을 넘어설 때만 주도권을 가져간다).
2. **얼음 거대행성 / mini-Neptune: 적당하지만, 바디가 차가울 때는 중요하다.** Neptune 규모의 잔여 냉각
   광도는 `T_int ~ 40–55 K`를 준다. 온난한 `T_eq`에는 무시할 만하지만, `T_eq` 자체가 수십 K일 때(멀리 있거나
   M-왜성 온대 궤도)는 **결정적**이어서 `T_eff`를 `T_eq`보다 한참 끌어올린다(Neptune §4, Proxima c §7).
   신뢰도는 **몇 배 인자** 수준이다(Uranus 변칙, §4).
3. **거대행성(0.3 ≲ M ≲ 13 M_J): Kelvin–Helmholtz 냉각 트랙(§2).** `L_int(M, age)`를
   Burrows/Baraffe/Fortney/Saumon-Marley 격자에서 읽어 온다. 늙고 + 저질량이면 → 희미 → 복사 지배(Polyphemus
   §7)이고, 젊으면 → 자발광(§3)이다.
4. **갈색왜성(13–70 M_J): 냉각 트랙 + 일시적 중수소 연소 평탄부(§6).** Gyr 동안 자발광이며, Sonora와
   Saumon & Marley 격자가 이 영역을 다룬다. 여기서 `L_int`는 충분히 커서, 넓은 동반자 궤도에서 오는 `T_eq`는
   보통 무관하다.
5. **젊은가 늙었는가가 마스터 스위치다.** 분류 3–4 안에서 젊은 바디는 자발광이고 늙은 바디는 평형에
   접근한다. 젊은(≲ 수백 Myr) 바디는 hot/cold-start 모호성(§3)이 `L_int`를 최대 ~2 dex 넓히고, Gyr 나이의
   바디는 그것이 해소되어 있다.

---

## 6. 헬륨 비와 중수소 연소: 추가 항

질량 범위의 양 끝에서 중요해지는 두 가지 추가 내부 열원이 있다.

- **헬륨 비 / 상분리(Saturn형).** Saturn의 내부 압력과 온도에서 헬륨은 금속성 수소에 섞이지 않게 되어
  아래로 비처럼 내린다. 이 분화로 방출되는 중력 에너지는 단순 Kelvin–Helmholtz 냉각 **위에 더해지는 추가
  광도 항**이다. Stevenson & Salpeter 1977은 H–He 상도와 메커니즘을 제시했고, Mankovich & Fortney 2020은
  그것이 *Saturn에서는 활발하고 Jupiter에서는 아직 대체로 비활성*임을 보여, Saturn의 측정된 내부 플럭스가
  질량에 비해 의외로 높은 까닭을 설명했다(순수 냉각 모델 대비 "초과 발광"이다, Hanel+ 1983, §4). NearStars용
  교훈은, Saturn급 거대행성의 내부 플럭스가 순진한 냉각 트랙 값을 넘어설 수 있다는 것이다. 워크드 바디가
  질량·나이에서 Saturn류라면 이를 표시한다.
- **중수소 연소(갈색왜성 경계, ~13 M_J).** ~13 M_J 위에서는 바디가 원시 중수소를 잠시 융합해, 냉각을 늦추는
  **일시적 광도 평탄부**를 더한다. Spiegel, Burrows & Milsom 2011은 중수소 연소 질량 한계를 못박았고(금속성/
  헬륨 비율에 의존해 ~11–14 M_J에 걸친다는 것도 보였다), 이것이 관례적인 행성/갈색왜성 경계선이다. 그 바로
  위의 바디(예: ~13–14 M_J 동반자)는 같은 나이의 순수 행성보다 더 오래 자발광을 유지한다. ~13 M_J 아래에서는
  중수소 연소가 없고 바디는 순수 냉각 트랙 위에 있다.

두 항 모두 §1 관계식을 바꾸지는 않는다. 단지 `L_int`를, 따라서 `T_int`를 바꿀 뿐이다.

---

## 7. 워크드 예제

**Neptune(calibration).** `T_eq ≈ 47 K`, 측정 `T_eff ≈ 59 K`, 방출/흡수 ≈ 2.6(Pearl & Conrath 1991).
내부 성분만의 `T_int = (59⁴ − 47⁴)^(1/4) ≈ 52 K`로 복사 입력에 비등하므로 `T_eff`가 `T_eq`보다 한참 위에
앉는다. **도출됨**(내부 플럭스 측정값). Uranus와 대비해 보자. 같은 분류인데 `T_eff ≈ T_eq`, 내부 플럭스 ≈ 0,
경계용 쌍둥이다(§4).

**젊은 자발광 거대행성(직접 촬영 영역).** ≲ 100 Myr의 수-M_J 행성은 `L_int`가 워낙 커서(`T_int`가 수백에서
~1000 K) **별과 무관하게 자신의 열로 빛난다**. HR 8799 행성들이 *직접 촬영*된 방식이 이것이다(Marois+ 2008).
검출된 빛이 곧 냉각 트랙 광도(§2)이며, 그 나이에서는 hot/cold-start 모호성(§3)을 함께 짊어진다.
*NearStars ε Ind A b*: 나이 **≈ 3.5 Gyr**(dynamo 문서 앵커)인 ~7.6 M_J 거대행성이다. 수 Gyr면 **자발광 단계를
한참 지난** 상태로, 냉각 트랙이 그 `T_int`를 ~150–250 K 정도로 떨궈 놓았다(질량이 커서 아직 다소 따뜻하지만,
더 이상 수백 K로 밝지는 않다). ε Ind A를 넓고 차가운 궤도로 돌기 때문에 `T_eq`가 낮고 *내부*열이 더 큰 항이다.
그 `T_eff`는 대부분 잔여 냉각으로 정해지지만, 촬영적 의미에서 자발광은 **아니다**(열적 IR로는 검출 가능하나,
젊고 뜨거운 게 아니라 식은 늙은 거대행성이다). `T_int`는 Gyr 나이 트랙에서 보고하고 start 모호성은 없다.

**Polyphemus = α Cen A b(늙고 + 저질량 = 희미함).** **늙고(~5 Gyr), ~0.38 M_J(Saturn급)**인 온대 거대행성이다.
두 손잡이 모두 *희미한* 냉각 광도를 가리킨다. 저질량(작은 저장고, 빠른 냉각) **그리고** 늙은 나이(이미 오래전에
식음)다. Phase-4 board는 `T_int < 110 K`에 내부 플럭스 **복사 입력의 ≲ 6 %**를 썼다. 즉 `f ≲ 0.06`이고, §1에
의해 `T_eff ≈ T_eq (1+0.06)^(1/4) ≈ 1.015 T_eq`, 약 ~1.5 % 증분이다. **복사 지배이지 자발광이 아니다.** 이것이
교과서적인 "늙은 저질량 거대행성" 사례이며, board가 그 온도를 사실상 `T_eq`로 취급한 이유다. 냉각 트랙이 5 Gyr와
0.38 M_J에서는 더 내놓을 게 없다. (Saturn급이니 §6의 작은 헬륨-비 증폭을 주의하되, 그래도 ≲6 % 예산 안에 충분히
머문다.)

**Proxima c(차가운 mini-Neptune: 새 사례).** Proxima를 넓은 궤도로 도는, 차가운(`T_eq ≈ 40 K`) 늙은 ~8 M⊕
super-Earth/mini-Neptune이다. 복사 입력이 거의 0이라 **적당한 Neptune-유사 내부 플럭스**조차 결정적이다.
Neptune류 `T_int ~ 45–50 K`를 취하면 §1은 `T_eff = (40⁴ + 48⁴)^(1/4) ≈ 53 K`를 준다. 내부열이 **유효 대기온도를
~40 K에서 어쩌면 ~50–60 K까지 끌어올린다**(Neptune 유사체). 이는 여전히 CH₄(~91 K 승화 영역)와 N₂를 얼리기에
충분히 차가워서 정성적 결말(얼음으로 덮인, 휘발성이 동결된 세계)은 바뀌지 않지만, 이 온도대에서는 내부 항이
*무시할 수 없으니* 함께 끌고 가야 한다. 점값이 아니라 **범위**로 제시한다(몇 배 인자 `L_int` 불확실성, §4 Uranus
경고).

**지구(암석 calibration: 열은 `T_eff`가 아니라 내부로 들어간다).** 지구의 전역 열 손실은 **~46–47 TW**(Davies
2013; Sclater+ 1980)로, 평균 표면 플럭스 **~0.087 W/m²**이며 **대략 절반은 방사성**(U/Th/⁴⁰K 붕괴), **절반은
영년**(잔여 강착열 + 핵/맨틀 냉각)이다. 그 플럭스를 §1에 대입하면 `T_int = (0.087/σ)^(1/4) ≈ 35 K`로, 지구의
`T_eq ≈ 255 K`에 대해서는 `(255⁴ + 35⁴)^(1/4) − 255 ≈ 0.001 K` 보정, 즉 **표면온도에는 완전히 무시할 만하다**.
그런데도 *같은* ~47 TW가 바로 맨틀을 대류시키고(판 구조론) 핵을 대류시키는(지구에 자기장을 주는 **geodynamo**)
것이다. Driscoll & Bercovici 2014는 그 대조를 깔끔하게 보여준다. 질량·반경이 지구의 쌍둥이인 금성은 다른 열
이력 경로(판-구조 heat-pipe 없음, 굼뜬 핵 냉각)를 밟아 오늘날 **다이나모가 없다**. 같은 `T_int` 무관성에, 반대의
*내부* 결말이다. **암석 교훈은, `T_eff` 증분이 아니라 수지(~0.08–0.09 W/m², 절반/절반)와 그 내부 결과(화산활동,
탈가스, 다이나모)를 보고하라는 것이다.** **도출/calibration**(측정된 수지).

**NearStars 암석 바디(Proxima b / Proxima d: 방사성 지배, 관건은 화산활동과 다이나모).** M 왜성을 도는
온대~온난 암석 행성이라면 내부열은 **지구 규모(~0.08 W/m², `T_int ~ 35 K`)**에서 방사성 지배이고 따라서
**표면온도에는 무관**하다. `T_eff ≈ T_eq`다(이런 세계는 전적으로 §1의 복사 지배 영역에 산다). 내부열이 *정하는*
것은 바디가 지질학적으로 살아 있는지다. 충분한 내부열 → 맨틀 대류 → **화산 탈가스**(2차 대기의 Gate 3 공급)와
가능한 **핵 다이나모**(dynamo 문서의 RM22 암석 영역)다. 질량/나이가 달리 말하지 않는 한 지구 수지를 기본값으로
삼아 **내부** 양으로 끌고 간다. 더 무거운 super-Earth는 방사성 인벤토리가 더 크고 더 오래 뜨겁게 머물며, 늙은
저질량 암석은 더 일찍 식는다. **가까운 조석고정 사례 주의.** 가장 안쪽 M-왜성 암석 행성에서는 **조석 소산이
방사성 열을 넘어설** 수 있고, 그러면 *그것이* 지온구배(화산활동/다이나모의 동력)를 정한다. 그 경우는
[조석가열 문서](tidal-heating-methodology.md)에 넘긴다. 어느 쪽이든 표면온도는 `≈ T_eq`로 남고, 내부열의 역할은
내부다.

---

## 8. 정직함과 불확실성

dynamo 문서와 조석 문서의 경고와 같은 정신에서다.

- **냉각 트랙은 초기 엔트로피, 조성, 나이에 의존한다.** 젊은(≲ 수백 Myr) 거대행성은 **hot/cold-start
  모호성**(§3)이 `L_int`에서 최대 ~2 dex에 걸치므로 범위로 인용한다. Gyr 나이의 바디는 그것이 해소되지만, 늙고
  저질량인 바디는 그때 *본질적으로 희미하고 제약하기 어려워서*(신호가 작다) 영역("복사 지배")이 확실하더라도
  절대 `L_int`는 잘 고정되지 않는다.
- **Uranus 변칙이 얼음 거대행성 신뢰도를 몇 배 인자로 묶는다.** 거의 쌍둥이인 두 얼음 거대행성이 내부
  플럭스로 ~2.5배 차이 난다(§4). `L_int`는 (M, R, age)의 깔끔한 함수가 아니다. 예측된 얼음 거대행성 `T_int`는
  무엇이든 차수+α 수준으로 다루고 범위로 끌고 간다.
- **조성이 중요하다.** 헬륨 비(Saturn형, §6)와 금속성(중수소 연소 한계, §6)이 `L_int`를 수십 퍼센트에서 몇 배까지
  움직인다. 중원소가 풍부한 내부는 태양 조성 내부와 다르게 식는다. 측정값이 있지 않은 한 바디별로 큐레이션하지
  않는다. 기본값으로 태양 조성 트랙을 쓰고 누락을 표시한다.
- **영역 판정은 수치가 그렇지 않을 때도 견고하다.** §1의 네제곱 덧셈 덕분에 *정성적* 판정("자발광",
  "복사 지배", 또는 "내부열이 차가운 바디를 끌어올린다")은 정밀한 `L_int`가 문제가 되기 한참 전에 (질량, 나이,
  `T_eq`)에서 보통 깔끔하게 떨어진다. NearStars가 art-direction에 실제로 필요한 것은 그 영역 판정이다. 정확한
  `T_int`는 범위이고, art가 그것을 덮어쓰는 경우(이를테면 일부러 빛나게 한 늙은 거대행성)는 silent upgrade가 아닌
  **documented divergence**다.

관계식은 근거가 있고 calibration도 되어 있다(Neptune의 측정된 내부 플럭스로 그 `T_eff`를 재현하고, Uranus의
null도 맞춘다). 불확실성을 짊어지는 것은 *입력*(냉각 트랙이나 측정된 에너지 수지로 얻는 `L_int`, start 시나리오,
조성)이다. 신뢰도는 **`T_int`로는 몇 배 인자, 영역 분류로는 높음**이다.

---

## 9. 주석 달린 참고문헌

각 항목은 저자, 연도, 저널, **검증된** arXiv id(또는 "no arXiv" + bibcode), ADS 인용 수, 그리고 기여 한 줄로
이루어진다.

- **Stevenson, D. J. & Salpeter, E. E. (1977)**: *ApJS* 35, 239 (dynamics) & 35, 221
  (phase diagram). **No arXiv** (`1977ApJS...35..239S`, `1977ApJS...35..221S`). Cites: 234 /
  225. Founding H–He phase-separation ("helium rain") theory: the giant-planet
  differentiation luminosity term. §6.
- **Hanel, R. et al. (1981)**: *JGR* 86, 8705. **No arXiv** (`1981JGR....86.8705H`).
  Cites: 133. Voyager IRIS albedo, internal heat and energy balance of **Jupiter** (emitted
  ≈ 1.67× absorbed). §4.
- **Hanel, R. A. et al. (1983)**: *Icarus* 53, 262. **No arXiv** (`1983Icar...53..262H`).
  Cites: 114. **Saturn** internal heat flux and energy balance (emitted ≈ 1.78× absorbed,
  high for its mass, the helium-rain signature). §4, §6.
- **Pearl, J. C. et al. (1990)**: *Icarus* 84, 12. **No arXiv** (`1990Icar...84...12P`).
  Cites: 135. Albedo, T_eff and energy balance of **Uranus** from Voyager IRIS: the
  anomalously *low* internal flux (ratio ≈ 1.06 ≈ zero), Neptune's twin that doesn't glow.
  §4.
- **Pearl, J. C. & Conrath, B. J. (1991)**: *JGR* 96, 18921. **No arXiv**
  (`1991JGR....9618921P`). Cites: 135. Albedo, T_eff (~59 K) and energy balance of
  **Neptune**: emits ~2.6× absorbed sunlight; the canonical "internal heat > insolation"
  calibration. §1, §4, §7.
- **Pollack, J. B. et al. (1996)**: *Icarus* 124, 62. **No arXiv** (`1996Icar..124...62P`).
  Cites: 2774. Core-accretion formation of the giant planets: the physical origin of the
  *cold-start* low-entropy initial condition. §3.
- **Burrows, A. et al. (1997)**: *ApJ* 491, 856. **arXiv:astro-ph/9705201**
  (`1997ApJ...491..856B`). Cites: 1300. Nongray theory and evolutionary cooling tracks for
  extrasolar giant planets and brown dwarfs: the foundational `L_int(M, age)` grid. §2.
- **Guillot, T. (1999)**: *Science* 286, 72. **No arXiv** (`1999Sci...286...72G`).
  Cites: 454. "Interiors of Giant Planets Inside and Outside the Solar System": review
  framing internal heat, contraction and energy balance. §2 context.
- **Chabrier, G. & Baraffe, I. (2000)**: *ARA&A* 38, 337. **arXiv:astro-ph/0006383**
  (`2000ARA&A..38..337C`). Cites: 537. Review of the theory of low-mass stars and substellar
  objects: the cooling/contraction physics behind the tracks. §2.
- **Baraffe, I. et al. (2003)**: *A&A* 402, 701. **arXiv:astro-ph/0302293**
  (`2003A&A...402..701B`). Cites: 1528. COND evolutionary models for cool brown dwarfs and
  EGPs: the most-cited substellar cooling grid; `L_int`/`T_int` vs (M, age). §2, §7.
- **Fortney, J. J., Marley, M. S. & Barnes, J. W. (2007)**: *ApJ* 659, 1661.
  **arXiv:astro-ph/0612671** (`2007ApJ...659.1661F`). Cites: 949. Planetary radii across
  five orders of magnitude in mass and insolation, from thermal-evolution models: radius +
  cooling luminosity coupling (internal heat inflates the radius). §2.
- **Marley, M. S. et al. (2007)**: *ApJ* 655, 541. **arXiv:astro-ph/0609739**
  (`2007ApJ...655..541M`). Cites: 454. "On the Luminosity of Young Jupiters": the
  hot-start vs cold-start initial-entropy dichotomy (~2 dex spread at young ages). §3.
- **Saumon, D. & Marley, M. S. (2008)**: *ApJ* 689, 1327. **[arXiv:0808.2611](https://arxiv.org/abs/0808.2611)**
  (`2008ApJ...689.1327S`). Cites: 619. Evolution of L and T dwarfs in color-magnitude
  diagrams: the substellar cooling-track grid for the brown-dwarf regime. §2, §5.
- **Marois, C. et al. (2008)**: *Science* 322, 1348. **[arXiv:0811.2606](https://arxiv.org/abs/0811.2606)**
  (`2008Sci...322.1348M`). Cites: 1513. Direct imaging of the HR 8799 planets: young giants
  detected by their *own* cooling-track thermal light (the self-luminous regime). §1, §3, §7.
- **Fortney, J. J. & Nettelmann, N. (2010)**: *Space Sci. Rev.* 152, 423.
  **[arXiv:0912.0533](https://arxiv.org/abs/0912.0533)** (`2010SSRv..152..423F`). Cites: 314. Review of giant-planet interior
  structure, composition and evolution: internal heat, contraction, helium rain in one
  place. §2, §6.
- **Spiegel, D. S., Burrows, A. & Milsom, J. A. (2011)**: *ApJ* 727, 57.
  **[arXiv:1008.5150](https://arxiv.org/abs/1008.5150)** (`2011ApJ...727...57S`). Cites: 276. The deuterium-burning mass limit
  for brown dwarfs and giant planets (~11–14 M_J, composition-dependent): the planet/BD
  boundary and the transient burning luminosity. §6.
- **Spiegel, D. S. & Burrows, A. (2012)**: *ApJ* 745, 174. **[arXiv:1108.5172](https://arxiv.org/abs/1108.5172)**
  (`2012ApJ...745..174S`). Cites: 357. Spectral and photometric diagnostics of giant-planet
  formation scenarios: how to tell hot- from cold-start young giants observationally. §3.
- **Marley, M. S. et al. (2021)**: *ApJ* 920, 85. **[arXiv:2107.07434](https://arxiv.org/abs/2107.07434)**
  (`2021ApJ...920...85M`). Cites: 375. The Sonora Bobcat brown-dwarf atmosphere and
  *evolution* models: the modern substellar cooling-track grid superseding/extending
  Saumon & Marley 2008. §2, §5.
- **Mankovich, C. R. & Fortney, J. J. (2020)**: *ApJ* 889, 51. **[arXiv:1912.01009](https://arxiv.org/abs/1912.01009)**
  (`2020ApJ...889...51M`). Cites: 69. Helium phase separation gives a Jupiter/Saturn
  dichotomy: quantifies the helium-rain luminosity active in Saturn but not yet Jupiter.
  §6.

**Earth / rocky internal heat (radiogenic + secular):**

- **Sclater, J. G., Jaupart, C. & Galson, D. (1980)**: *Rev. Geophys. Space Phys.* 18, 269.
  **No arXiv** (`1980RvGSP..18..269S`). Cites: 861. The classic global terrestrial heat-loss
  budget (oceanic + continental): the ~0.08 W/m² / ~tens-of-TW scale. §5.
- **Davies, J. Huw (2013)**: *G-cubed* 14, 4608. **No arXiv** (`2013GGG....14.4608D`).
  Cites: 241. Global map of solid-Earth surface heat flow: the modern ~46–47 TW
  (~0.087 W/m² mean) census. §5, §7.
- **Driscoll, P. & Bercovici, D. (2014)**: *Phys. Earth Planet. Inter.* 236, 36. **No arXiv** (`2014PEPI..236...36D`, doi 10.1016/j.pepi.2014.08.004). Cites: 108. Thermal and magnetic histories of Earth and Venus: ties a rocky body's interior heat budget (melting, radioactivity, core conductivity) to whether a **dynamo survives**; the heat → geodynamo link and the Earth/Venus divergence behind the §5 rocky regime and §7 Earth example. §5, §7.

**Topics with no single canonical paper:** the surface-flux → `T_int ≈ 35 K` rocky-planet
*scale* in §5 is a Stefan–Boltzmann conversion of the Earth heat-flow budget above, not a
separate citable law; the per-body cold-start composition corrections are read off the
grids (Baraffe 2003 / Sonora) rather than from one dedicated paper. The Davies & Davies
(2010) "Earth's surface heat flux" estimate is not cleanly ADS-indexed as a primary
article; the Davies 2013 map (`2013GGG....14.4608D`) and Sclater+ 1980 are the cited
anchors instead.

---

## 관련 문서

- [tidal-heating-methodology](tidal-heating-methodology.md): **자매 내부 열원**(조석 소산)이다. 이 문서는 *비-조석*
  항(잔여 + Kelvin–Helmholtz + 방사성 + 헬륨 비 + 중수소 연소)을 다룬다. 조석 플럭스가 무시할 수 없을 때(가까운
  이심 궤도 바디)는 그 값을 `T_int`에 더한다. 둘은 같은 §1 관계식으로 결합된다.
- [tidally-locked-temperature-methodology](tidally-locked-temperature-methodology.md): 여기서 `T_int`와 `T_eff⁴ = T_eq⁴ + T_int⁴`로
  결합되는 **`T_eq` 항**이다. 그 문서는 복사 쪽을, 이 문서는 내부 쪽을 전달한다.
- [planetary-dynamo-scaling](planetary-dynamo-scaling.md): 모범이 되는 자매 스케일링-법칙 문서이자, 자기장을 정하는 데
  **같은 냉각 광도 `L_int(M, age)`**를 쓰는 곳이다(`B ∝ L^(1/6)`). 하나의 광도, 두 가지 결과로, 여기서는 열복사,
  그쪽에서는 다이나모 자기장이다. 젊은 거대행성이 같은 이유로 *더 밝고* *더 자기적*이다.
- [mass-radius-relation-methodology](mass-radius-relation-methodology.md): 내부열은 **반경을 부풀린다**. 젊고 뜨거운 거대행성은
  물리적으로 더 크므로(Fortney+ 2007이 `L_int`와 `R`을 결합), `T_int = (L_int/4πR²σ)^(1/4)`에 쓰는 반경 자체가
  나이에 의존한다.
- [methodology-index](methodology-index.md) — 모든 도출값 방법론 레시피의 인덱스입니다.
