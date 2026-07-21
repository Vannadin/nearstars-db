<!-- Phase 3 디스크색 합성: Mie 산란광 reflectance로 disk_tint_rgb_hex 도출, 고증/vivid 변종 + B/I 검증 -->
# Debris-Disk Color Methodology: 조성 + 입자 크기 → Mie 산란 → reflectance → sRGB

> 출처: debris disk 산란광 및 입자 광학 문헌 종합
> (Mie 커널은 Bohren & Huffman 1983, 충돌 입자 크기 분포는 Dohnanyi 1969,
> 조성별 광학상수는 Draine 2003, Rouleau & Martin 1991, Warren & Brandt 2008,
> Jäger+ 2003, Khare+ 1984, 측정된 산란광 색은 AU Mic의 Krist 2005 / Fitzgerald
> 2007 / Graham 2007과 Fomalhaut의 Kalas 2005 / Acke 2012) 에 종별 광학상수
> 포털(Polyanskiy 2024 / refractiveindex.info, **고체·얼음상** 항목) 과,
> 대기 문서에서 재사용한 공학용 색측정 표준(CIE 1931; IEC 61966-2-1 sRGB) 을
> 더한 것이다.
> 인용은 임의 웹 검색이 아니라 NASA ADS(등록된 ADS_API_TOKEN)로 대조했고,
> arXiv 식별자가 있으면 그것을, 없으면 권위 있는 ADS bibcode를 쓴다.
> 목적은 분해된 산란광 색이 없을 때, 항성 주위 **debris disk**의 가시 색
> (`disk_tint_rgb_hex`)을 입자 조성과 입자 크기 분포에서 **합성하고 정당화**하는
> 재사용 가능한 레시피를 두는 것이다.
> 교과서가 아니라 작업용 레퍼런스다. 검증된 인용은 §8을 보라.
> 도구: `scripts/phase3/disk_color_mie.py`.

**범위: 이 문서가 다루지 *않는* 것.** 이 문서는 **항성 주위 먼지 입자가 모항성에서
산란**하는 빛, 즉 `disk_tint_rgb_hex`로 저장되는 원반 고유의 가시 색조를 다룬다.
대기·표면 반사율 문서의 **산란광 속 먼지** 짝꿍으로, 세 번째 반사율 자매 문서다.
다음은 **다루지 않는다**.

- **열복사 / mm 원반 방출**. 대부분의 벨트에서 Spitzer, Herschel, ALMA가 실제로
  검출하는 원적외선/서브-mm/mm 플럭스는 **다른 관측량**이다(별빛 산란이 아니라 온도와
  방사율이 정하는 입자 *열* 방출). NearStars 벨트 대부분은 이것밖에 없으며, 바로
  그래서 그 *색*을 여기서 합성해야 한다(§6의 측정-대-합성 규칙).
- **대기 반사/산란 색**(하늘, 구름, 연무). 자매 문서
  `atmosphere-reflected-color-methodology.md`에 산다. 같은 색측정 엔진을 쓰되 기체상
  광학상수를 쓴다.
- **고체 표면 색**(암석, 레골리스, 얼음). 자매 문서
  `surface-color-albedo-methodology.md`에 산다. 같은 엔진에, 여기 입자 물질과 겹치는
  **고체·얼음상** 광학상수(물 얼음, 규산염, 톨린)를 쓴다.
- **행성 고리 색 그 자체**. 토성 같은 항성 *주위가 아닌 행성 주위* 고리도 입자에서의
  산란광이고 같은 물리를 공유하지만, 그 입자는 µm 먼지가 아니라 cm–m 급 바위라
  Mie 크기 영역이 무관하다(기하 광학, 고리색 ≈ 구성 얼음/암석의 표면색). 고리는 표면
  문서로 다루라. 이 문서는 `x = 2πa/λ ~ 1`인 µm-입자 *debris* 영역을 위한 것이다.

세 반사율 문서는 색측정 엔진(스펙트럼 → sRGB, 광원은 모항성) 하나를 공유한다. **이
문서는 그것을 다시 적지 않는다.** §5와 대기 문서 §6을 보라.

## 목차

1. [디스크 색이 원칙에 따른 선택인 이유](#1-디스크-색이-원칙에-따른-선택인-이유)
2. [원리: 산란된 별빛과 reflectance 컨벤션](#2-원리-산란된-별빛과-reflectance-컨벤션)
3. [방법: Mie Q_sca, 입자 크기 적분, 조성별 n,k](#3-방법-mie-q_sca-입자-크기-적분-조성별-nk)
4. [Q_sca(λ) → sRGB (대기 문서의 엔진을 쓴다)](#4-qscaλ--srgb-대기-문서의-엔진을-쓴다)
5. [faithful / vivid 2변종 컨벤션](#5-faithful--vivid-2변종-컨벤션)
6. [검증, 그리고 측정-대-합성 규칙](#6-검증-그리고-측정-대-합성-규칙)
7. [워크드 예제](#7-워크드-예제)
8. [주석 참고문헌](#8-주석-참고문헌)
9. [관련 문서](#관련-문서)

---

## 1. 디스크 색이 원칙에 따른 선택인 이유

NearStars debris 벨트 중 측정된 가시 산란광 색을 가진 것은 **거의 없다**. 광학에서
분해된 산란광 영상은 가장 밝고 가까운 소수의 원반에만 존재하고, 나머지는 순전히
**열복사/mm 방출**(적외선/서브-mm 초과 또는 ALMA 맵)로만 검출되는데 이것은 가시 색
정보를 전혀 담지 않는다. 그래서 cfg에 넣는 `disk_tint_rgb_hex`는, 영상화된 두 원반을
제외한 모든 벨트에 대해, **한계 안에서 물리에 근거해 내리는 원칙적 합성**이며, 정확히
대기 문서 §1과 표면 문서 §1의 정신을 따른다. 조성과 입자 크기가 색조를 정하고, Mie
물리가 그것을 스펙트럼으로 바꾸며, 문서화된 화이트밸런스 컨벤션(§2)이 채도를 고정한다.

답을 제약하는 것을, 그것을 가진 빈도가 높은 순서로 보면 이렇다.

- **입자 크기 분포**(작은 쪽 컷오프, 기울기). 색조에 대한 **단일 최대 지렛대**다. 가장
  작은 입자가 광학 파장에 대해 어디에 앉느냐가, 원반이 파랗게 산란할지(작은 입자,
  레일리 같은 상승) 중성 회색으로 산란할지(큰 입자, 기하 광학)를 정한다. 작은 쪽 끝은
  **복사압 blowout 크기** `a_blow`(§3)로 앵커되며, 이는 모항성의 `L/M`에서 결정론적으로
  도출되므로, 다른 것을 아무것도 몰라도 모항성 광도가 컷오프를 핀으로 박는다.
- **조성**(Phase 2/3에서). 규산염 대 탄소 대 얼음 대 유기물이 복소 굴절률 `n+ik`을
  정하고, 그래서 입자가 파란빛을 얼마나 강하게 흡수하는지를 정한다(흡수성 탄소/톨린
  입자는 붉어지고, 투명한 얼음/포르스테라이트 입자는 크기만으로 색을 가진다). 두 번째로
  큰 지렛대다.
- **충돌 기울기 `q`**. 정상상태 충돌 캐스케이드에서는 정준값 `q = 3.5`(Dohnanyi 1969)
  근처로 고정되므로, 자유 선택인 경우가 드물다.

정직한 입장(§6의 불확실성 노트에서 되울린다)은 이렇다. **입자 크기 + 조성이 색조
계열을 정한다**(작은 입자 → 파랑, 큰 입자 → 회색, 흡수성 물질 → 붉은 쪽)는 것은
탄탄한 Mie 물리다. 그러나 **조성 클래스별 정확한 `n,k`는 벨트별 측정이 아니라 대표적인
문헌값**이고, 절대 채도는 관측량이 아니라 화이트밸런스/채도 컨벤션(§5)이다. 표면 문서가
가정한 표면 상태를 기록하듯, 가정한 조성과 blowout 크기 입력을 똑같이 기록하라.

---

## 2. 원리: 산란된 별빛과 reflectance 컨벤션

debris disk의 **가시** 색은 열복사가 아니라 **산란된 별빛**이다. 입자는 고유의
파장 의존 산란 효율 `Q_sca(λ)`를 가지며, 광학에서 우리가 보는 원반은

```
scattered_SED(λ) ∝ S(λ) · Q_sca(λ)
```

이고 `S(λ)`는 모항성 SED다. `Q_sca(λ)`가 *바로* 원반의 reflectance 스펙트럼이다.

**저장 컨벤션은 별을 제거한 먼지 고유색이다.** cfg tint는 `Q_sca(λ)`를 **회색
밸런스**해서 인코딩한다, 즉 렌더러가 모항성 빛을 다시 입히므로, 저장값은 **별과
무관**해야 한다. 화이트밸런스는 **파장에 평탄한 `Q_sca`가 중성 회색으로 매핑**되도록
정의된다.

```
reflectance_color  =  whitebalance[ Q_sca(λ) ]  =  sRGB[ Q_sca(λ) / Q_flat(λ) ]
```

여기서 나눗수는 같은 색측정 아래에서 평탄한 reflectance의 sRGB 색이다(도구에서는
`_lin_rgb(np.ones_like(WL))`). 이것이 **얼음 같은 파란 원반을 붉은 M 왜성 주위에서도
파랗게** 유지하는 장치다. 파란 성질은 *입자*의 속성이고, 별의 붉음을 저장 tint에
구워 넣으면 그것을 잘못 덮어버리게 된다. 광원은 렌더러가 소유하고, 먼지 고유색은
DB가 소유한다.

(도구는 **절대** 컨벤션 `color_absolute()`도 노출한다: `S(λ)·Q_sca(λ)`를 **태양**에
화이트밸런스해서, 태양 같은 별 아래 중성 입자 → 흰색, K/M 별 아래 → 따뜻한 색, A 별
아래 → 청백색이 되게 한다. 이는 별을 구워 넣는 repo 컨벤션을, 조잡한 "별 색 × 알베도"
에서 제대로 된 입자 크기 Mie 산란으로 업그레이드한 것이다. 위의 **reflectance**
컨벤션이 `disk_tint_rgb_hex`의 정준값이고, 절대 컨벤션은 별 색을 포함하는 슬롯을 위해
존재한다.)

---

## 3. 방법: Mie Q_sca, 입자 크기 적분, 조성별 n,k

합성은 벨트당 네 가지 입력에서 완전히 결정론적이다. 조성 클래스, 입자 크기 범위
`[a_min, a_max]`, 기울기 `q`, 모항성 `L/M/Teff`. 단계는 이렇다(각각
`scripts/phase3/disk_color_mie.py`의 함수에 대응한다).

**1. Mie 산란 효율: Bohren & Huffman.** 크기 매개변수 `x = 2πa/λ`와 복소 굴절률
`m = n − ik`를 가진 단일 구에 대해, `Q_sca(x, m)`은 **Bohren & Huffman (1983)**의
`bhmie` 알고리즘에서 나온다(로그 미분에 대한 하향 점화, 이어서 Mie `a_n, b_n` 계수).
`mie_qsca()`는 의존성 없는 `bhmie`의 numpy 포팅이다. 크기 매개변수 `x`(즉 **광학
파장 대비 입자 반지름**)이 지배적인 색 동인이며, 알고리즘이 이를 정확히 포착한다.

**2. 충돌 캐스케이드 위의 입자 크기 적분.** 실제 벨트는 입자 하나가 아니라 크기의
멱법칙 분포다. 단면적 가중 **충돌 크기 분포**

```
dn/da ∝ a^(−q),   q ≈ 3.5   (Dohnanyi 1969 정상상태 캐스케이드)
```

로 가중한 `Q_sca`를, 작은 쪽 바닥 `a_min`에서 큰 쪽 `a_max`까지 적분한다. 각 크기를
`a^(−q) · a²`(개수 × 기하 단면적)로 가중하고 재규격화한다. 작은 쪽 바닥은 **복사압
blowout 반지름**이다. 그보다 작은 입자는 항성 복사압에 의해 방출되므로 쌓일 수 없다.

```
a_blow ≈ 0.5 µm · (L/L☉)/(M/M☉) · (2.5 g cm⁻³ / ρ)
```

(`ρ = 2.5 g cm⁻³`는 측정이 아니라 대표적인 입자 밀도 가정이다.) **광도가 큰 모항성은
더 큰 입자를 날려보내** `a_min`을 올리고, 이는 원반 색을 파랑에서 회색 쪽으로 민다.
그래서 같은 얼음 조성이 AU Mic 주위(M 왜성, 아주 작은 `a_blow`)에서는 파랗게,
Fomalhaut 주위(A 별, 큰 `a_blow`)에서는 회색으로 읽힌다. Phase 2가 명시적인 최소 입자
크기를 보고한 경우(예: ε Eri 차가운 고리의 ~15 µm 입자)에는 그것이 `a_blow`를
오버라이드한다.

**3. 조성별 광학상수 `n(λ), k(λ)`.** 조성 클래스별로 광학 밴드(400–800 nm)에 걸쳐
샘플링해서 작업 그리드에 보간한다. 허수부 `k`가 흡수성 물질을 붉게 만드는 **파란빛
흡수**를 담당하고, 투명한 입자(얼음, 포르스테라이트)는 입자 크기만으로 색을 가진다.
도구가 탑재하는 클래스는 각각 1차 실험실 출처(§8)에 핀으로 박혀 있다.

| Class | Material | Optical constants |
|---|---|---|
| `astrosil` | astronomical silicate | Draine 2003 |
| `carbon` | amorphous carbon | Rouleau & Martin 1991 |
| `ice` | water ice | Warren & Brandt 2008 |
| `olivine` | Mg-rich crystalline forsterite | Jäger+ 2003 |
| `tholin` | Titan-type organic tholin | Khare+ 1984 |

2성분 입자(`ice_sil`, `sil_org`)는 **Maxwell–Garnett 유효매질 이론**으로 혼합한다.
host 매질 안에 부피 분율 `f`의 구형 함유물을 두고, 유전함수 `ε = (n+ik)²`를 혼합한다
(비물리적인 선형 `n,k` 평균이 아니다). 함유물 부피 분율은 50/50 *질량* 분할과 벌크
밀도(얼음 1.0, 규산염 3.3, 유기물 1.3 g cm⁻³)에서 도출하며, 부피 다수 성분을 host로
삼는다. MG는 침투 임계값(~0.3) 아래의 `f`에서 유효하고, 여기서는 충족된다.

**4. 조성은 두 번째 지렛대, 크기가 첫 번째다.** `n,k` 값은 *클래스별 대표 광학 밴드
값*으로, 1차 가정으로 문서화한다. 벨트별 측정이 아니며, 지배적인 색 동인은 적분이
올바르게 포착하는 크기 매개변수 `x`라는 점을 문서는 정직하게 밝힌다. 조성 클래스는
**색조 계열**을 정하고 blowout 크기는 **회색 쪽으로 얼마나 가는지**를 정하는 것으로
다루라.

---

## 4. Q_sca(λ) → sRGB (대기 문서의 엔진을 쓴다)

reflectance 스펙트럼 `Q_sca(λ)`에서 sRGB 헥스로의 변환은 대기·표면 경우와 **동일**하며
**`atmosphere-reflected-color-methodology.md` §6에 완전히 문서화**되어 있다. 여기서
행렬을 다시 적지 않는다. 파이프라인은 이렇다. 스펙트럼을 **CIE 1931 2° 색대응함수**에
대해 적분해 XYZ로 만들고, **IEC 61966-2-1** 선형-sRGB 행렬을 적용하고, 감마 인코딩한
뒤 색역으로 클리핑한다. **색측정 수식에 정준 ADS 논문은 없다**. 이는 CIE/IEC 공학
표준이며, 대기 문서 §8에서 그렇게 인용한다.

디스크 특유의 구현 노트 두 가지가 있다.

- **CMF 커널.** 도구는 CIE 1931 CMF를 표 값이 아니라 **Wyman, Sloan & Shirley (2013)의
  다중 로브 해석적 가우스 피팅**으로 평가한다, `x̄/ȳ/z̄(λ)`에 대한 닫힌 형태 근사로,
  색 작업에 충분히 정확하고 의존성이 없다. (이 논문은 *Journal of Computer Graphics
  Techniques* 기사이며 **ADS에 색인되어 있지 않다**, §8을 보라.) 같은 CIE 1931 표준의
  구현 디테일일 뿐, 다른 관측자가 아니다.
- **reflectance 화이트밸런스(§2)가 입력의 차이다.** 대기 문서는 기하 알베도 `A(λ)`를,
  표면 문서는 양방향 reflectance `r(λ)`를 먹인다. 여기 입력은 `Q_sca(λ)`이고, 정준
  저장색은 **회색 밸런스** 버전이다(평탄한 `Q_sca` → 중성 회색, 별 제거). 그 정규화(
  `Q_sca(λ)`를 평탄한 스펙트럼의 sRGB 색으로 나눈 것)가 대기 문서 §6 위에 더해진
  유일한 비틀기다.

광학상수 `(n,k)`는 대기 문서에서 소개한 **refractiveindex.info 포털(Polyanskiy 2024)**
에서 오며, 여기서는 **고체·얼음상** 항목(표면 문서와 같은 상)이고, 각 행은 자기 자신의
1차 실험실 출처에 핀으로 박혀 있다(§3 표, §8).

---

## 5. faithful / vivid 2변종 컨벤션

Sol-Configs 모델을 따라, cfg 라이터는 벨트마다 **두** 색 변종을 emit하며, 둘은 오직
**채도**(회색 점 주위의 채도)로만 구분되고 색조는 같다.

- **faithful**(`SAT_FAITHFUL = 0.82`): 살짝 *탈*채도된, 물리적으로 정직한 값. 먼지
  산란광 색은 네온이 아니라 진정으로 미묘하며, 이것이 근거 있는 값이다.
- **vivid**(`SAT_VIVID = 2.6`): 인게임에서 원반 색이 또렷이 보이도록 채도를 끌어올린,
  더 예쁜 팩.

둘 다 화이트밸런스된 회색 점 주위로 채도를 스케일링해 계산하므로
(`rgb = mean + sat·(rgb − mean)`), **같은 색조**를 공유하고 회색에서 얼마나 떨어져
앉느냐만 다르다. 팩은 사용자가 고르며, Phase 3 리포트에는 둘 다 기록한다.

---

## 6. 검증, 그리고 측정-대-합성 규칙

**합성이 믿을 만한 이유는 오직, blowout/조성 물리가 측정된 산란광 색을 가진 두 벨트를
재현하기 때문이다.** tint를 확정하기 전에, `band_ratio()` 헬퍼(blue/near-IR
reflectance 비 `B/I`(445 nm / 806 nm))로 새 벨트를 올바른 측정 아날로그와 대조하라.

| Belt | Measured | Synthesis | Verdict |
|---|---|---|---|
| **AU Mic** | **blue**, `B/I ~ 1.6` (Krist 2005) | `B/I ≈ 1.74` | ✓ blue reproduced |
| **Fomalhaut main ring** | **~neutral/grey**, `B/I ~ 1.0` (Kalas 2005) | `B/I ≈ 0.87` | ✓ grey reproduced |

AU Mic은 M 왜성이다. 아주 작은 `a_blow`가 파랗게 산란하는 서브-마이크론 입자를 남긴다.
Fomalhaut은 A 별이다. 큰 `a_blow`가 회색으로 산란하는 큰 입자만 남긴다. 모델은
**모항성 `L/M`만으로** 양 끝을 모두 맞히며, 이것이 그 사이의 미측정 벨트를 합성하는
근거가 된다.

**측정-대-합성 규칙은 이렇다.**

- **산란광으로 영상화된 벨트**(Fomalhaut main ring = Kalas 2005; AU Mic = Krist 2005)
  → **측정** 색을 쓴다. 합성으로 덮어쓰지 **말라**. 합성은 그것을 대체하는 게 아니라
  *맞히기* 위해 존재한다.
- **열복사 / mm 전용 벨트**(광학 산란광 영상 없음, 흔한 경우) → 이 방법으로
  **합성**한다. `confidence: low`로 플래그하고 모항성의 Phase 3 Open items에 적는다.

---

## 7. 워크드 예제

각각 모항성 + 조성 + 입자 크기 → reflectance 색을, 도구의 `BELTS` 표를 통해 근거화한다.

**AU Mic (검증, 측정된 blue).** M1V 모항성, `L/L☉ ≈ 0.10`이라 서브-마이크론 `a_blow`.
서브-마이크론 astrosilicate 입자가 파란 쪽으로 강하게 산란해 `B/I ≈ 1.74`, 측정된 파란
원반과 일치(Krist 2005; Fitzgerald 2007 다파장; Graham 2007은 편광 측광으로 파란색을
원시 입자 *성장*/다공성에 귀속). 작은 입자의 원형이다.

**Fomalhaut main ring (검증, 측정된 grey).** A3V 모항성, `L/L☉ ≈ 16.6`이라 큰 `a_blow`
: 큰 입자만 살아남아 중성으로 산란해 `B/I ≈ 0.87`, 측정된 ~회색 고리와 일치(Kalas
2005; 혜성형 푹신한 응집체, Acke 2012). 큰 입자의 원형이다. Fomalhaut의 안쪽 따뜻한
먼지와 중간 먼지는 *같은* 바깥 벨트의 PR-drag 파편이므로(부피로 물 얼음 ~50–80%,
Sommer+ 2025), 도구는 그것들에 차가운 고리와 같은 얼음질 `ice_sil` 조성을, 따라서 같은
합성 색조를 부여한다.

**ε Eri (합성, 열복사/mm 전용).** K2V 모항성. 안쪽 소행성대형 규산염 벨트(Backman
2009)와 ~64 au의 ~15 µm 입자를 가진 얼음/규산염 차가운 고리(`ice_sil`, Su+ 2017)가
있다. 광학 산란광 검출은 **없다**: HST/STIS는 깊은 상한만 둘 뿐이다(Sai+ 2024). 그래서
색은 합성하고 저신뢰로 플래그한다. 명시적 15 µm 입자 바닥(`a_blow`가 아니라)이 얼음
조성에도 불구하고 차가운 고리를 회색 쪽으로 민다.

**HD 69830 (합성, 열복사/mm 전용).** K0V 모항성에 **결정질 olivine/forsterite**로 된
따뜻한 ~1 au 벨트가 있다(Beichman 2005; Lisse 2007). 포르스테라이트는 광학에서 투명해
(`k` ~ 1e-4) 색이 흡수가 아니라 입자 크기만으로 나온다. 거의 중성인 합성 색조다. 투명
입자의 원형이다.

**τ Ceti (합성, 열복사/mm 전용).** G8V 모항성에 무정형 규산염 + 유기물로 된 넓은 벨트
(Lawler 2014)가 있고, Maxwell–Garnett `sil_org` 입자(유기물 host 안의 규산염 함유물)로
다룬다. 유기물 성분의 파란빛 흡수성 `k`가, 순수 규산염 벨트에 비해 약간 붉어진 합성
색조를 준다. 흡수성 입자의 원형이다.

---

## 8. 주석 참고문헌

각 항목은 저자, 연도, 저널/책, **검증된** arXiv 식별자(없으면 플래그와 ADS bibcode),
그리고 기여 한 줄로 이루어진다. 인용수(ADS, 조사 시점)는 점검용으로 적었다.

**Mie 커널과 크기 분포.**

- **Bohren, C. F. & Huffman, D. R. (1983)**: *Absorption and Scattering of Light by
  Small Particles*, Wiley. **Book, no arXiv** (bibcode `1983asls.book.....B`). The
  canonical Mie-scattering text; its `bhmie` algorithm is the `Q_sca(x, m)` kernel
  ported in the tool. §3. (4180 cites, the field's standard reference.)

- **Dohnanyi, J. S. (1969)**: *JGR* 74, 2531. **No arXiv** (bibcode
  `1969JGR....74.2531D`). *Collisional Model of Asteroids and Their Debris*: the
  origin of the `dn/da ∝ a^(−3.5)` steady-state collisional-cascade size distribution.
  §3. (1033 cites.)

**조성별 광학상수 `n(λ)+ik(λ)`** (각각 하나의 `_NK` 클래스를 핀으로 박는다).

- **Draine, B. T. (2003)**: *ApJ* 598, 1017. **arXiv:astro-ph/0304060.** *Scattering
  by Interstellar Dust Grains. I. Optical and Ultraviolet*: the astronomical-silicate
  optical constants (`astrosil`). §3. (581 cites.) *(The script comment names "Draine
  2003"; ADS confirms this is the correct paper. Note the alternative canonical
  silicate reference Draine & Lee 1984 is the older compilation; the tool uses the 2003
  update, as cited.)*

- **Rouleau, F. & Martin, P. G. (1991)**: *ApJ* 377, 526. **No arXiv** (bibcode
  `1991ApJ...377..526R`). *Shape and Clustering Effects on the Optical Properties of
  Amorphous Carbon*: the amorphous-carbon constants (`carbon`). §3. (579 cites.)

- **Warren, S. G. & Brandt, R. E. (2008)**: *J. Geophys. Res. Atmos.* 113, D14220.
  **No arXiv** (bibcode `2008JGRD..11314220W`). *Optical constants of ice from the
  ultraviolet to the microwave: a revised compilation*, the water-ice constants
  (`ice`); the revised successor to Warren 1984 (`1984ApOpt..23.1206W`). The tool uses
  the 2008 revision, as cited. §3. (820 cites.)

- **Jäger, C., Dorschner, J., Mutschke, H., Posch, Th. & Henning, Th. (2003)**:
  *A&A* 408, 193. **No arXiv** (bibcode `2003A&A...408..193J`). *Steps toward
  interstellar silicate mineralogy VII*: sol-gel Mg-silicate (crystalline
  forsterite/olivine) constants (`olivine`). §3. (250 cites.)

- **Khare, B. N., Sagan, C., Arakawa, E. T., Suits, F., Callcott, T. A. & Williams,
  M. W. (1984)**: *Icarus* 60, 127. **No arXiv** (bibcode `1984Icar...60..127K`).
  *Optical constants of organic tholins produced in a simulated Titanian atmosphere*:
  the Titan-tholin constants (`tholin`); the same Khare-type optical constants the
  atmosphere doc uses for haze and the surface doc uses for tholin coatings. §3.
  (612 cites.)

**색측정 커널.**

- **Wyman, C., Sloan, P.-P. & Shirley, P. (2013)**: *Journal of Computer Graphics
  Techniques* 2(2), 1. **NOT INDEXED IN ADS** (confirmed absent; it is a graphics-
  journal article, not an astronomy work). The multi-lobe analytic Gaussian fit to the
  CIE 1931 2° color-matching functions used by `cie_xyz()`. An implementation of the
  CIE 1931 standard, not a separate observer. §4.

- **CIE 1931 / IEC 61966-2-1 (sRGB)**: engineering standards (not ADS works); the
  colorimetry math is **not restated here**: see `atmosphere-reflected-color-
  methodology.md` §6/§8. §4.

**검증 원반 (측정된 산란광 색 둘).**

- **Krist, J. E. et al. (2005)**: *AJ* 129, 1008. **No arXiv** (bibcode
  `2005AJ....129.1008K`). *HST ACS Coronagraphic Imaging of the AU Microscopii Debris
  Disk*: the measured **blue** color (`B/I ~ 1.6`) that the small-grain synthesis must
  reproduce. §6, §7. (119 cites.)

- **Kalas, P., Graham, J. R. & Clampin, M. (2005)**: *Nature* 435, 1067.
  **arXiv:astro-ph/0506574.** *A planetary system as the origin of structure in
  Fomalhaut's dust belt*: the measured ~**neutral/grey** main ring that the large-
  grain synthesis must reproduce. §6, §7. (357 cites.)

**벨트별 조성 / 입자 크기 출처** (`BELTS` 표의 Phase 2 입력).

- **Fitzgerald, M. P. et al. (2007)**: *ApJ* 670, 536. **[arXiv:0705.4196](https://arxiv.org/abs/0705.4196).**
  *The AU Microscopii Debris Disk: Multiwavelength Imaging and Modeling.* §7.
  (70 cites.)

- **Graham, J. R. et al. (2007)**: *ApJ* 654, 595. **arXiv:astro-ph/0609332.**
  *The Signature of Primordial Grain Growth in the Polarized Light of the AU Mic Debris
  Disk*: porous-aggregate grains. §7. (137 cites.)

- **Acke, B. et al. (2012)**: *A&A* 540, A125. **[arXiv:1204.5037](https://arxiv.org/abs/1204.5037).** *Herschel images
  of Fomalhaut*: cometary fluffy-aggregate grains in the main ring. §7. (112 cites.)

- **Sommer, M. et al. (2025)**: *MNRAS* 539, 439. **[arXiv:2503.18127](https://arxiv.org/abs/2503.18127).** *A PR-drag
  origin for the Fomalhaut disc's pervasive inner dust*: the inner/intermediate dust
  is PR-drag debris of the outer belt, ~50–80% water ice by volume. §7. (11 cites.)

- **Backman, D. et al. (2009)**: *ApJ* 690, 1522. **[arXiv:0810.4564](https://arxiv.org/abs/0810.4564).** *Epsilon
  Eridani's Planetary Debris Disk: Structure and Dynamics*: silicate inner +
  icy/silicate cold ring. §7. (126 cites.)

- **Su, K. Y. L. et al. (2017)**: *AJ* 153, 226. **[arXiv:1703.10330](https://arxiv.org/abs/1703.10330).** *The Inner
  25 au Debris Distribution in the ε Eri System.* §7. (32 cites.)

- **Sai, K. P. M. et al. (2024)**: *AJ* 168, 169. **[arXiv:2408.06973](https://arxiv.org/abs/2408.06973).** *Deepest
  Limits on Scattered Light Emission from the Epsilon Eridani Debris Disk*: the
  HST/STIS optical **non-detection** (so ε Eri's color is synthesized, not measured).
  §7. (8 cites.)

- **Su, K. Y. L. et al. (2013)**: *ApJ* 763, 118. **[arXiv:1301.1331](https://arxiv.org/abs/1301.1331).** *Asteroid
  Belts in Debris Disk Twins: Vega and Fomalhaut*: featureless silicate, large blowout
  grains (Vega; thermal/mm only). (138 cites.)

- **Beichman, C. A. et al. (2005)**: *ApJ* 626, 1061. **arXiv:astro-ph/0504491.**
  *An Excess Due to Small Grains around the Nearby K0 V Star HD 69830*: crystalline
  silicate warm belt. §7. (168 cites.)

- **Lisse, C. M. et al. (2007)**: *ApJ* 658, 584. **arXiv:astro-ph/0611452.** *On
  the Nature of the Dust in the Debris Disk around HD 69830*: crystalline
  olivine/forsterite. §7. (95 cites.)

- **Wyatt, M. C. et al. (2012)**: *MNRAS* 424, 1206. **[arXiv:1206.2370](https://arxiv.org/abs/1206.2370).** *Herschel
  imaging of 61 Vir*: no spectral features (61 Vir; thermal/mm only). (107 cites.)

- **Lawler, S. M. et al. (2014)**: *MNRAS* 444, 2665. **[arXiv:1408.2791](https://arxiv.org/abs/1408.2791).** *The
  debris disc of solar analogue τ Ceti*: amorphous silicate + organics. §7. (40 cites.)

**광학상수 포털.**

- **Polyanskiy, M. N. (2024)**: *Scientific Data* 11, 94. **No arXiv** (bibcode
  `2024NatSD..11...94P`). The **refractiveindex.info** database; **here the solid/ice-
  phase entries** (silicate, water ice, forsterite, tholin) for the per-composition
  `n+ik` step (§3), the same portal/phase as the surface doc and the gas-phase
  counterpart used by the atmosphere doc. Cite each material's own primary source per
  row (the five papers above). (335 cites.)

**정준 ADS 논문이 깔끔하게 없는 항목**: (a) 스펙트럼→sRGB 색측정 수식(CIE/IEC 표준,
대기 문서 §6이 소유); (b) **Wyman+ 2013** CMF 피팅: *Journal of Computer Graphics
Techniques* 기사이며 **ADS에 색인되어 있지 않다**(부재 확인). 그래서 CIE 1931 표준의
구현으로서, 저널 레퍼런스로만 인용한다. 위의 모든 천문 인용은 직접 ADS bibcode/arXiv
조회로 확인했다.

---

## 관련 문서

- `docs/reference/atmosphere-reflected-color-methodology.md`: 여기서 재사용하는
  **색측정 엔진**(§6: 스펙트럼 → XYZ → sRGB, 광원은 모항성 SED)과
  **refractiveindex.info 포털**(Polyanskiy 2024; 거기서는 기체상, 여기서는 고체·얼음상)
  을 소유하는 **자매 문서**. 대기 반사색은 디스크 산란광과 *다른* 관측량이다. 둘을
  혼동하지 말라.
- `docs/reference/surface-color-albedo-methodology.md`: 고체 표면용 **자매 문서**. 그
  입자 광학상수가 여기 디스크 입자 물질과 **겹친다**(물 얼음 = Warren & Brandt 2008,
  톨린 = Khare-type, 규산염). cm–m 바위로 된 행성 *주위* 고리는 이 문서(µm Mie 영역)
  보다 그 문서(기하 광학)에 더 가깝다.
- `docs/reference/planetary-dynamo-scaling.md`: 인용 엄밀성과 유효 영역 정직성(arXiv
  없음 플래그, 영역 단서)의 **금본위 자매 문서**. 이 문서는 그 참고문헌 규율을 따른다.
- **도구:** `scripts/phase3/disk_color_mie.py`: 구현체(Mie `bhmie`, 입자 크기 적분,
  Maxwell–Garnett 혼합, CIE→sRGB, faithful/vivid). 벨트별 입자 크기/조성/인용 출처는
  그 `BELTS` 표 주석에 살며, 그 인용들을 여기 §8로 끌어올렸다.
- **스킬:** `nearstars-phase3`가 이 방법을 소비해 벨트의 `disk_tint_rgb_hex` 결정을
  고르고, faithful/vivid 변종을 호스트별 Phase 3 리포트에 기록한다.
- `db/disks_curated.json`은 디스크 **기하만**(반지름, 폭, 경사, 종횡비) 저장하고
  tint는 **저장하지 않는다**. 색 출처는 DB가 아니라 도구/Phase 3 리포트에 있다(JSON
  왕복이 깔끔하지 않았다). `project-nearstars-ring-fabrication`을 보라.
