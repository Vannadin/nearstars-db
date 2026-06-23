<!-- 고체 표면(암석·레골리스·얼음) 조성에서 가시광 색과 Bond/기하 알베도를 도출하는 방법론 레퍼런스 -->
# 표면색·알베도 방법론 — 조성 → 반사율 → sRGB + Bond 알베도

> 출처: 행성 표면 반사 분광 문헌 종합
> (Burns 1993, Sherman 1985, Morris+ 1985/2000, Clark 1981, Hapke 1981/1993/2012,
> Hapke 2001, Pieters+ 2000, Kokaly+ 2017 / USGS Spectral Library v7, Warren 1984 /
> Warren & Brandt 2008, Grundy & Schmitt 1998, Grundy+ 1999, Cruikshank+ 1993/1998,
> Grundy+ 2016, Buratti+ 2017) 에 종별 광학상수 포털
> (Polyanskiy 2024 / refractiveindex.info, **고체·액체상** 항목) 과 표준 행성과학
> 교과서의 Bond/기하 알베도 정의 (de Pater & Lissauer, *Planetary Sciences*) 를
> 더한 것이다.
> 인용은 임의 웹 검색이 아니라 NASA ADS(등록된 ADS_API_TOKEN)로 대조했고,
> arXiv 식별자가 있으면 그것을, 없으면 권위 있는 ADS bibcode를 쓴다.
> 목적은 고체 행성 표면(암석·레골리스·얼음)의 가시 색과, 평형온도 공식이 필요로 하는
> **Bond 알베도**를 조성에서 **선택하고 정당화**하는 재사용 가능한 레시피를 두는 것이다.
> 교과서가 아니라 작업용 레퍼런스다. 검증된 인용은 §8을 보라.

**범위 — 이 문서가 다루지 *않는* 것.** 이 문서는 **고체 표면**(암석·레골리스·얼음)이
**반사**하는 빛, 즉 그 원반 색조와 볼로메트릭 Bond 알베도를 다룬다. 대기 반사색
문서의 표면 짝꿍 격이다. 다음은 **다루지 않는다**.

- **대기 반사/산란 색**(하늘, 구름덱, 연무). 이것은 자매 문서
  `atmosphere-reflected-color-methodology.md`에 산다. 둘은 **합성**된다. 대기의
  반사색은 표면색 *위에* 얹힌다. 두꺼운 대기나 광학적으로 두꺼운 구름·연무 덱에서는
  표면이 **가려지므로** 이 문서가 무의미하다(금성, 타이탄, 거대행성). 표면색은 **얇거나
  대기가 없는** 바디에서 의미를 가진다(화성, 달, 얼음 위성, 대기 없는 암석체).
- **발광 / 플라스마 색**(재진입 발광, 기광, 오로라, 용암 열복사). 이것은 `firefly-cfg`
  스킬과 `composition-color.md`에 산다. 물리가 다르다. 별빛의 반사가 아니라 들뜨거나
  뜨거운 물질에서 나오는 *발광*이다.

두 반사 문서는 색측정 엔진(스펙트럼 → sRGB, 광원은 모항성) 하나를 공유한다. **이
문서는 그것을 다시 적지 않는다.** §5와 대기 문서 §6을 보라.

## 목차

1. [표면색·알베도가 원칙에 따른 선택인 이유](#1-표면색알베도가-원칙에-따른-선택인-이유)
2. [광물에 색이 있는 이유 — 전자 전이](#2-광물에-색이-있는-이유--전자-전이)
3. [조성에서 반사 스펙트럼으로 — 라이브러리와 Hapke 모델](#3-조성에서-반사-스펙트럼으로--라이브러리와-hapke-모델)
4. [수정 인자 — 우주 풍화, 입자 크기, 얼음과 유기물](#4-수정-인자--우주-풍화-입자-크기-얼음과-유기물)
5. [반사 스펙트럼 → sRGB (대기 문서의 엔진을 쓴다)](#5-반사-스펙트럼--srgb-대기-문서의-엔진을-쓴다)
6. [Bond·기하 알베도 — 에너지 수지의 `A`](#6-bond기하-알베도--에너지-수지의-a)
7. [워크드 예제](#7-워크드-예제)
8. [주석 참고문헌](#8-주석-참고문헌)
9. [관련 문서](#관련-문서)

---

## 1. 표면색·알베도가 원칙에 따른 선택인 이유

NearStars 외계 타깃 중 표면의 가시 색이나 Bond 알베도를 실제로 **측정**한 경우는
**없다**. 이 양들은 가까운 외계행성에서조차 사실상 분해되지 않는다(잘해야 한 위상에서의
광대역 기하 알베도이며, 그것도 뜨거운 통과 행성 몇몇뿐이다). 그래서 cfg에 넣는
표면색도, 온도 공식에 먹이는 `A`도 모두 **물리적 한계 안에서 원칙에 따라 내리는,
유사체에 근거한 선택**이며, 정확히 대기 문서 §1과 표면기압 문서 §1의 정신을 따른다.
조성이 대역을 정하고, 문서화된 타이브레이크가 값을 고른다.

답을 실제로 제약하는 것을, 그것을 가진 빈도가 높은 순서로 보면 이렇다.

- **조성**(Phase 2/3에서). 어떤 광물·얼음·유기물이 있느냐가 진단 흡수 띠(따라서 색조)와
  기준 밝기를 정한다. 가장 단단한 입력이며, 유사체 라이브러리(§3)가 스펙트럼으로
  바꿔주는 바로 그 입력이다.
- **표면 상태 — 입자 크기와 풍화**. *같은* 조성이라도 입자 크기와 노출 연령에 따라
  밝거나 어둡고, 중성이거나 붉어진다(§4). 그 차이는 크다. **알베도**를 가장 크게
  움직이는 고리이며, 외계 바디에서는 좀처럼 제약되지 않는다.
- **텍스처 / 혼합 기하**. 친밀 혼합 대 면적 혼합, 신선한 노출 대 레골리스로 덮인 표면.
  가장 제약이 약하다. 보통 의도적인 아트 선택이다(α Cen "절반 황, 절반 현무암" 예제,
  §7).

정직한 입장은 (§6의 불확실성 절에서 다시 나오듯) 이렇다. **광물 정체가 색조 계열을
정하고**(Fe³⁺ → 빨강, 마픽 → 1 µm 띠를 가진 어두움, 물얼음 → 밝은 중성, 톨린 →
적갈색), 이것은 단단한 물리다(§2). 그러나 **밝기/알베도와 붉어지는 정도가 약한
고리**이며, 풍화와 입자 크기가 끌고 가서 Bond 알베도를 2–5배 흔들 수 있다. 가정한
표면 상태를, 대기 문서가 가정한 발색단을 적는 것과 똑같은 방식으로 기록한다.

---

## 2. 광물에 색이 있는 이유 — 전자 전이

암석의 가시색은 거의 전적으로 광물 안에 든 **전이금속 이온**(압도적으로 철)의 **전자
전이**에서 온다. 분자 진동이 아니다(그것은 적외선에 앉는다). 두 메커니즘이 지배한다.

- **결정장(d–d) 전이.** 전이금속 양이온(Fe²⁺, Fe³⁺, 그리고 Cr³⁺, Ti)이 둘러싼 음이온이
  그 3d 궤도를 갈라놓는 배위 자리에 앉고, 전자가 갈라진 준위 사이를 뛰며 특정 가시/근적외
  파장을 흡수한다. 정전적이고 망라적인 표준 처리는 **Burns 1993**(*Mineralogical
  Applications of Crystal Field Theory*, 2nd ed.)이다. 어떤 띠가 어디 떨어지는지를
  이온별·자리별로 설명하는 교과서다. 행성에서 가장 중요한 경우는 **마픽 규산염 속
  Fe²⁺**(감람석, 휘석)으로, 넓은 **~1 µm 흡수 띠**를 만들고(휘석은 ~2 µm 띠를 더한다),
  현무암 표면을 어둡게 하며 달·화성·소행성의 띠 깊이/위치 광물학을 주는 진단 지표다.
- **전하이동(과 산화된 철의 빨강).** d–d보다 훨씬 강한 **O²⁻ → Fe³⁺ 리간드-금속
  전하이동** 띠는 **파랑/자외선**에 앉고 파랑 쪽으로 가파르게 오르는 날개를 가진다.
  **3가(산화된) 철** 광물(적철석, 침철석, 나노상 페릭 산화물)에서는 이 띠가 파랑 끝을
  먹고 강한 **빨간 가시 기울기**를 남긴다. *화성이 붉은 이유*이며 산화된 먼지 표면이
  녹슬어 보이는 이유다. 전자구조 토대는 **Sherman 1985**(Fe³⁺ 배위 자리 전자구조)와
  **Sherman & Waite / Sherman 1985–87**(철 산화물의 전하이동)이고, 이를 화성 색에 잇는
  실험실 반사 시연은 **Morris+ 1985**(서브미크론 페릭 산화물 분말), 화성 현장 확인은
  **Morris+ 2000**(Pathfinder 암석·토양)이다.

색에 대한 결론은 이렇다. **환원된/2가 마픽 암석 → 1 µm 띠를 가진 어둡고 중성에서
초록빛인 색. 산화된 3가 먼지 → 파랑을 가파르게 먹는 빨강.** 철의 산화 상태가 암석
색조의 가장 큰 단일 레버다.

---

## 3. 조성에서 반사 스펙트럼으로 — 라이브러리와 Hapke 모델

색측정 엔진(§5)이 필요로 하는 입력은 ~380–780 nm 범위의 **양방향 반사 스펙트럼**
`r(λ)`다. 조성에서 그 스펙트럼으로 가는 근거 있는 경로는 둘이며, 다음 순서로 쓴다.

**(a) 분광 라이브러리에서 찾는다 — 실험 데이터 등뼈.** 실제 광물·암석·얼음의 측정
반사 스펙트럼이 가능한 한 가장 단단한 입력이다. 정전적이고 공개적으로 인용 가능한
표준 데이터베이스는 **USGS Spectral Library Version 7**(**Kokaly+ 2017**)으로, 알려진
입자 크기에서 측정한 광물·암석·토양·얼음·식생의 실험실 반사 스펙트럼 수천 점이며,
splib06(Clark+ 2007)과 이전 릴리스의 후예다. 브라운 대학교의 **RELAB** 설비(PDS
"RELAB Spectral Library Bundle")는 보완적인 행성 유사체 데이터베이스다(운석, 달·소행성
유사체, 얼음). Phase 3 조성이 구체적 상을 지목하는 바디라면, 그 라이브러리 스펙트럼을
가져와 섞고((b) 참고) 결과를 §5에 먹인다. 진단 흡수 띠는 **Clark 1981**(물 서리/얼음
0.65–2.5 µm)의 분광 토대와 §2의 결정장 띠 할당에 따라 광물학으로 대응된다.

**(b) 입자 표면에서의 복사 전달 — Hapke 모델.** 라이브러리 스펙트럼은 한 입자 크기,
한 기하에 대한 것이다. 실제 표면은 채워 넣은 입자 혼합이라 흔히 (i) 단성분을 **섞고**
(ii) 입자 크기와 시야 기하에 맞춰 **재스케일**해야 한다. 정전적 틀은 **Hapke
1981**(*Bidirectional Reflectance Spectroscopy I — Theory*)과 그 후속편(거칠기 1984,
충효과/결맞음 후방산란 2002, 다공성 2008)이며, 교과서 **Hapke 1993/2012**(*Theory of
Reflectance and Emittance Spectroscopy*)에 모여 있다. Hapke 이론에서 **밝기/알베도**를
직접 끌고 가는 사실 두 가지.

- **단일산란 알베도 `w`가 입자별 성질이다**. 양방향 반사율과 반구 반사율 모두 `w`와
  단조 증가한다. 조성이 허수부 굴절률 `k(λ)`와 입자 크기를 통해 `w(λ)`를 정한다
  (흡수 경로 = 입자 크기 × `k`).
- **고운 입자 → 더 밝고, 띠가 약하다.** 입자가 작으면 입자당 흡수 경로가 짧고 산란
  면이 많아져, *같은* 광물이라도 잘게 부순 쪽이 더 밝고 흡수 띠가 얕다. "신선함 =
  밝음"의 메커니즘이며, 알베도를 움직이는 지배적 입자 크기 레버다(§4).

실무에서 섞으려면 라이브러리 스펙트럼을 결합하거나(면적 혼합 = 선형, 친밀 혼합 =
Hapke를 통한 `w`-공간 비선형) 종별 광학상수 `n(λ)+ik(λ)`를 단일산란 알베도로 바꿔
Hapke를 순방향으로 돌린다. 광학상수는 **refractiveindex.info** 포털(**Polyanskiy
2024**)에서 오고, **여기서는 고체·액체상 항목**(결정질 광물, 물얼음, N₂/CH₄/CO₂ 얼음,
톨린)을 쓴다. 같은 포털의 기체상 페이지를 쓰는 대기 문서와 정반대다. 각 행은 자체
1차 실험 출처에 핀한다(예: 물얼음은 Warren 1984 / Warren & Brandt 2008).

---

## 4. 수정 인자 — 우주 풍화, 입자 크기, 얼음과 유기물

조성이 색조 계열을 고정하면, 다음 세 과정이 **밝기, 채도, 붉어짐**을 움직인다. 흔히
조성 자체보다 더 크게 움직인다.

- **우주 풍화 — 대기 없는 바디는 나이 들며 어두워지고 붉어진다.** 대기가 없는 바디에서는
  미소운석 충돌과 태양풍 스퍼터링이 입자를 **나노상 금속철(npFe⁰)**로 입히고, 이것이
  시간이 가며 표면을 **어둡게**(알베도 하락) 하고 연속 기울기를 **붉히며** 흡수 띠를
  **눅인다**. 표준 리뷰는 **Hapke 2001**(*Space Weathering from Mercury to the Asteroid
  Belt* — npFe⁰ 메커니즘)과 **Pieters+ 2000**(*Space Weathering on Airless Bodies* —
  회수한 달 시료로 해명, 가장 고운 분율의 광학적 역할은 Pieters+ 1993 / Noble+)이다.
  실무 규칙은 이렇다. 대기 없는 표면이 **젊고 신선하면**(최근 충돌 크레이터, 신선한
  얼음) 같은 조성의 **성숙한** 레골리스보다 **더 밝고 더 파랗다/덜 붉다**. 달의 갓
  드러난 크레이터 광조가 밝고 둘러싼 마리아가 어두운 이유가 바로 이 한 과정이다.

- **입자 크기.** 풍화와 독립적으로, **고운 입자가 더 밝고 띠가 얕다**(§3, Hapke). 고운
  얼음 입자의 서리는 거의 흰색으로 읽히고, 같은 얼음이 맑은 판이나 거친 덩어리면 더
  어둡고 푸르게 반투명하다. 입자 크기와 풍화가 함께, 조성이 정할 수 없는 알베도 "노브"를
  정한다.

- **얼음과 유기물 — 외태양계 표면.** 휘발성 얼음 표면은 자기만의 색 논리를 가진다.
  - **물얼음**은 가시광에서 **밝고 약간 파랗다**(흡수가 가시광에서 약하고 근적외로
    오른다). 강한 진단 근적외 띠를 가진다. 광학상수는 **Warren 1984 / Warren & Brandt
    2008**, 온도 의존 근적외 스펙트럼은 **Grundy & Schmitt 1998**, 얼음 외태양계 표면의
    원격 탐사 레시피는 **Grundy+ 1999**다. 신선한 물얼음/눈은 흔한 자연 표면 중 가장
    밝다(§6).
  - **N₂, CH₄, CO₂ 얼음**은 밝고 대체로 중성/흰색이며, 명왕성과 트리톤의 고알베도
    지형을 지배한다(**Cruikshank+ 1993**, *Ices on the Surface of Triton*; 명왕성은
    Owen+ 1993).
  - **톨린 / 내화성 유기물이 얼음 표면을 붉히고 어둡게 한다.** CH₄/N₂ 얼음의 복사
    처리가 붉은 유기 잔류물을 쌓고, 소량만으로도 중성 얼음을 **주황-빨강**으로 바꾸며
    알베도를 낮춘다. 원형은 **Cruikshank+ 1998**(*The Composition of Centaur 5145
    Pholus* — 태양계에서 알려진 가장 붉은 표면)으로, 대기 문서가 연무에 쓰는 바로 그
    톨린 화학(Khare형 광학상수)을 여기서는 **표면** 코팅으로 쓴다. 명왕성의 창백한
    N₂-얼음 평원을 배경으로 어두운 빨강 "Cthulhu"/톨린 지형을 칠하는 것이 이것이다.

정직한 귀결은 이렇다. 풍화 + 입자 크기 + 미량 유기 코팅은, 벌크 조성을 전혀 바꾸지
않고도 표면의 **알베도를 2–5배, 색조를 중성에서 진한 빨강으로** 움직일 수 있다.
표면 *상태*를 기록된 선택으로 취급한다.

---

## 5. 반사 스펙트럼 → sRGB (대기 문서의 엔진을 쓴다)

반사 스펙트럼에서 sRGB 색으로 가는 변환은 대기 경우와 **동일**하며,
`atmosphere-reflected-color-methodology.md` §6에 **완전히 문서화**되어 있다. 여기서
다시 적지 않는다. 단 하나 다른 것은 **입력 스펙트럼**이다.

- 대기 문서: 입력은 대기의 **기하 알베도** `A(λ)`(레일리 + Mie + 발색단 흡수)다.
- 이 문서: 입력은 §3–4에서 나온 **표면 양방향 반사율** `r(λ)`(라이브러리 스펙트럼을
  Hapke로 입자 크기/풍화 보정한 것)다.

하류는 전부 같다. **모항성 SED** `S(λ)`를 곱하고(광원이다 — M왜성 표면은 따뜻하게,
A형 별 표면은 차게 읽힌다), CIE 1931 색대응함수와 적분해 XYZ로, IEC 61966-2-1 sRGB
행렬을 적용하고, 감마 인코딩하고, 색역으로 클립한다. 반사 스펙트럼은
`R(λ) = S(λ)·r(λ)`이고, 나머지는 대기 문서 §6 그대로다. 거기서처럼 **색측정 수학에
대한 표준 ADS 논문은 없다** — CIE/IEC 공학 표준이며 대기 문서가 그렇게 인용한다.

**얇은 대기** 바디라면 두 문서가 **합성**된다. 여기서 표면색을 렌더하고, 그 위에 대기
문서의 반사/산란 기여가 색조를 입힌다(밝은 지형 위 얇고 맑은 대기 → 표면이 옅은 레일리
색조와 함께 지배. 두꺼운 덱 → 표면이 가려지고 대기 문서만 적용).

---

## 6. Bond·기하 알베도 — 에너지 수지의 `A`

색(§5)은 눈에 적분한 *분광* 반사율이다. 에너지 수지는 *볼로메트릭* 스칼라가 필요하다.
두 알베도, 한 관계.

- **기하 알베도 `p`** — 영위상(완전 조명, 후방 산란)에서의 원반 적분 밝기를, 같은
  크기의 완벽한 확산(람베르트) 원반에 대해 잰 것이다. 충효과에서 측광으로 재는 양이다.
  분광 분해하면 `p(λ)`이고, 이것이 본질적으로 §5의 입력이다.
- **Bond 알베도 `A`** — 입사한 **모든** 항성 에너지(파장 **전체**와 모든 산란각에 걸쳐
  적분) 중 바디가 반사하는 분율이다. 에너지 수지의 알베도다.

둘은 **위상적분 `q`**(바디 위상함수의 각 적분)로 이어진다.

```
A_Bond = q · p_geometric        (per wavelength: A(λ) = q(λ)·p(λ);  bolometric: weight by the stellar SED)
```

위상적분 `q`(람베르트 표면에서 ≈ 1, 달처럼 어두운 후방산란 레골리스에서 ~0.3–0.5,
전방 산란을 하는 밝은 얼음/구름 바디에서 ~0.7–1.3)는 빛이 위상각에 따라 어떻게
분포하는지를 담는다. 정의와 `A = q·p` 관계는 표준 행성과학 교과서 자료다(**de Pater
& Lissauer, *Planetary Sciences***). 역사적 뿌리는 Russell의 반사 행성 측광과 Bond의
에너지 균형이다. 실무에서는 §5에서 `p`를 추정하고 표면 종류에 맞는 `q`를 채택하거나
(유사체 근거), 태양계 유사체에서 Bond 알베도를 직접 가져온다.

**표면 종류별 전형적 Bond 알베도**(유사체 앵커 — 조성+상태로 고른다).

| Surface type | Bond albedo `A` | Notes / analog |
|---|---|---|
| Fresh water-ice / snow | ~0.6–0.8 | brightest natural surface (Europa, Enceladus, fresh frost) |
| N₂/CH₄/CO₂ volatile-ice plains | ~0.5–0.85 | Pluto Sputnik / Triton bright terrain |
| Bright icy moon (mature) | ~0.3–0.6 | Europa ~0.6, mixed/old ice lower |
| Oxidized (ferric) dust / rust | ~0.2–0.3 | **Mars ~0.25** — bright but red |
| Tholin / dark-red organic ice | ~0.05–0.15 | Pholus-like; weathered icy terrain |
| Basalt / mare regolith, space-weathered | ~0.06–0.12 | **the Moon ~0.11** (very dark) |
| Anorthosite / fresh rock | ~0.15–0.25 | lunar highlands, fresh exposures |
| Carbonaceous / C-type regolith | ~0.02–0.06 | darkest common surfaces |

**이 `A`는 자매 온도 문서의 평형온도 공식이 소비하는 바로 그 알베도다.**

```
T_eq = [ S (1 − A) / (4 σ) ]^(1/4)
```

(`S` = 바디 위치에서의 항성 플럭스, `σ` = 슈테판–볼츠만 상수). 따라서 표면 선택은
**온도로 전파된다**. 현무암질 α Cen 바디(`A`~0.1)는 같은 일사에서 얼음으로 다시 입힌
같은 바디(`A`~0.6)보다 더 뜨겁게 돈다. 이 `A`를 입력으로 받는
`tidally-locked-temperature-methodology.md`를 보라.

**불확실성.** 외계 바디의 표면색과 알베도는 **결코 측정되지 않는다** — 유사체에 근거한
선택이다. 조성이 색조 *계열*을 고정하지만(§2), **우주 풍화와 입자 크기가 Bond 알베도를
큰 폭으로 움직이고**(2–5배, §4), 그것이 다시 `T_eq`를 움직인다(∝ (1−A)^¼, 더 약하지만
실재하는 의존성). 가정한 표면 상태와, 알베도를 가져온 유사체를 늘 기록한다. `A`가 온도
문서로 들어갈 때는 하나의 숫자가 아니라 범위로 취급한다.

---

## 7. 워크드 예제

각 예제는 조성 → 과정 → (색, Bond 알베도)를 근거짓는다.

**화성 — 산화철 빨강, 어두움.** 현무암 기반암을 **3가(산화된) 나노상 철 산화물 먼지**가
덮는다. O²⁻→Fe³⁺ 전하이동 띠(§2; Sherman 1985)가 파랑을 먹고, **Morris+ 1985**가
실험실에서 시연하고 **Morris+ 2000**이 현장에서 확인한 가파른 **빨간 가시 기울기**를
준다. "밝은 녹"처럼 들리지만 Bond 알베도는 **고작 ~0.25**다(§6) — 밝은 흰색이 아니라
빨강이다. 전하이동의 원형이다.

**유로파 — 물얼음, 밝고 푸르스름.** 거의 순수한 **물얼음** 지각. 물얼음은 가시광에서
밝고 약간 파랗며 강한 근적외 띠를 가진다(§4; Warren 1984, Grundy & Schmitt 1998).
**높은 Bond 알베도(~0.6+)**와 밝은 중성에서 푸르스름한 원반을 준다. 얼음 위성의 원형이며,
조성 → 밝은 중성으로, 알베도 표에서 달의 정반대 끝이다.

**명왕성 / 트리톤 — N₂/CH₄/CO₂ 얼음 + 톨린 붉어짐.** 휘발성 **N₂/CH₄/CO₂ 얼음**
(트리톤은 Cruikshank+ 1993; 명왕성은 Owen+ 1993)이 **밝고 창백한 고알베도** 평원을
만든다 — 명왕성의 Sputnik Planitia는 거의 흰색으로 읽히고, 반구별 Bond/기하 알베도는
**Buratti+ 2017**이, 조성은 **Grundy+ 2016**이 맵핑했다. *그것들 옆에서* **복사 처리된
톨린**(Cruikshank+ 1998, Pholus 화학, §4)이 **어두운 빨강** 지형(Cthulhu)을 칠한다.
그래서 한 바디가 **공간적으로 이중적**이다. 창백한 고알베도 얼음 옆에 어두운 빨강
저알베도 유기물 — 높지만 변동이 큰 알베도다.

**달 — 현무암/사장암 + 우주 풍화 → 회색, 매우 어두움.** 마픽 마리아 현무암과 사장암질
고지, 둘 다 Fe²⁺ 1 µm 띠를 가지며(§2) 심하게 **우주 풍화**되었다. 나노상 철(Hapke
2001; Pieters+ 2000)이 **어둡게·붉게 하고 띠를 눅여**, 매우 낮은 Bond 알베도(**~0.11**)의
**회색** 표면을 남긴다. 우주 풍화의 원형이며, *같은* 신선한 물질(밝은 크레이터 광조)과
성숙한 레골리스(어두운 마리아)가 풍화 상태만으로 알베도가 달라진다는 시연이다(§4).

**NearStars α Cen 적용(정성적).** **황 침전물을 가진 현무암질 화산 바디**는 단테풍
표면으로 정해졌다. **절반은 황-노랑, 절반은 현무암-회색**이다. 조성이 두 축을 모두
고른다. 현무암 절반은 마픽-Fe²⁺의 어두운 회색으로 낮은 Bond 알베도(~0.1, 달 같음, §6)고,
**원소 황** 침전물은 더 높은 국소 알베도에서 밝은 황-노랑 대역을 준다(황의 전자 흡수가
파랑을 자른다 → 노랑). 원반 적분 `A`는 다소 낮은 가중 혼합이다. 그 **얼음 위성**은 밝은
중성 물얼음 바디(유로파 같음, `A`~0.6, §6, 푸르스름)로 읽힌다. **대륙성 암석 "호수
세계"**는 신선한 규산염 암석(사장암 같음, 중간 알베도)과 액체 물 호수(낮은 알베도,
어두움)를 섞어 → 적당하고 공간적으로 다양한 `A`를 준다. 어느 경우든 조성이 **색**(§5)과
**Bond 알베도**(§6)를 고르고, 그 `A`가 평형온도 계산
(`tidally-locked-temperature-methodology.md`)으로 들어간다 — 같은 α Cen 일사에서 어두운
현무암 외피가 얼음 외피보다 더 뜨겁게 돈다.

---

## 8. 주석 참고문헌

각 항목. 저자, 연도, 저널/책, **검증된** arXiv 식별자(없으면 그 표시와 ADS bibcode),
그리고 기여 한 줄. 점검용으로 (조사 시점 ADS) 피인용 수를 적었다.

- **Burns, R. G. (1993)** — *Mineralogical Applications of Crystal Field Theory*, 2nd
  ed., Cambridge Univ. Press. **Book, no arXiv** (bibcode `1993macf.book.....B`). The
  canonical text on how transition-metal (Fe²⁺/Fe³⁺/Cr/Ti) crystal-field transitions
  set mineral color and the diagnostic ~1 µm mafic band. §2. (591 cites.)

- **Sherman, D. M. (1985)** — *Physics and Chemistry of Minerals* 12, 161. **No
  arXiv** (bibcode `1985PCM....12..161S`). Electronic structure of Fe³⁺ coordination
  sites in iron oxides — the basis for the blue/UV charge-transfer band that reddens
  oxidized iron. §2. (149 cites.)

- **Morris, R. V. et al. (1985)** — *JGR* 90, 3126. **No arXiv** (bibcode
  `1985JGR....90.3126M`). Spectral/physicochemical properties of submicron ferric-oxide
  powders — the lab demonstration of the Mars-red ferric slope. §2, §7. (371 cites.)

- **Morris, R. V. et al. (2000)** — *JGR Planets* 105, 1757. **No arXiv** (bibcode
  `2000JGR...105.1757M`). Mineralogy/alteration of Mars Pathfinder rocks and soils —
  in-situ confirmation of the oxidized-iron Mars color. §2, §7. (267 cites.)

- **Clark, R. N. (1981)** — *JGR* 86, 3087. **No arXiv** (bibcode `1981JGR....86.3087C`).
  Water frost and ice near-IR reflectance 0.65–2.5 µm — foundational ice-spectroscopy
  reference and band assignments. §3. (146 cites.)

- **Kokaly, R. F. et al. (2017)** — *USGS Data Series 1035*. **USGS report, no arXiv**
  (bibcode `2017usgs.rept...14K`, DOI 10.3133/ds1035). **USGS Spectral Library Version
  7** — the canonical openly citable laboratory reflectance library of minerals, rocks,
  soils and ices (successor to splib06, Clark+ 2007 `2007usgs.rept...16C`). §3. (352
  cites.)

- **Hapke, B. (1981)** — *JGR* 86, 3039. **No arXiv** (bibcode `1981JGR....86.3039H`).
  *Bidirectional Reflectance Spectroscopy I — Theory* — the canonical particulate-
  surface radiative-transfer model linking single-scattering albedo, grain size and
  geometry to reflectance. §3. (1519 cites — the field's most-cited surface paper.)

- **Hapke, B. (2012)** — *Theory of Reflectance and Emittance Spectroscopy*, 2nd ed.,
  Cambridge Univ. Press. **Book, no arXiv** (bibcode `2012tres.book.....H`, DOI
  10.1017/CBO9781139025683; 1st ed. 1993 `1993tres.book.....H`, 507/682 cites). The
  textbook collecting the Hapke model and its grain-size/porosity/roughness
  corrections. §3. (507 cites, 2012 ed.)

- **Hapke, B. (2001)** — *JGR Planets* 106, 10039. **No arXiv** (bibcode
  `2001JGR...10610039H`). *Space Weathering from Mercury to the Asteroid Belt* — the
  nanophase-iron darkening/reddening mechanism on airless bodies. §4, §7. (815 cites.)

- **Pieters, C. M. et al. (2000)** — *Meteoritics & Planetary Science* 35, 1101. **No
  arXiv** (bibcode `2000M&PS...35.1101P`). *Space Weathering on Airless Bodies* —
  resolved with returned lunar samples; the optical effects of the finest fraction.
  §4, §7. (611 cites.)

- **Warren, S. G. (1984)** — *Applied Optics* 23, 1206. **No arXiv** (bibcode
  `1984ApOpt..23.1206W`). Optical constants of water ice from the UV to the microwave —
  the canonical ice `n+ik` (revised compilation Warren & Brandt 2008,
  `2008JGRD..11314220W`, 820 cites). §3, §4, §7. (1319 cites.)

- **Grundy, W. M. & Schmitt, B. (1998)** — *JGR Planets* 103, 25809. **No arXiv**
  (bibcode `1998JGR...10325809G`). Temperature-dependent near-IR absorption spectrum
  of hexagonal H₂O ice — the lab basis for cold-surface water-ice modeling. §4, §7.
  (298 cites.)

- **Grundy, W. M. et al. (1999)** — *Icarus* 142, 536. **No arXiv** (bibcode
  `1999Icar..142..536G`). Near-IR spectra of icy outer-solar-system surfaces — the
  remote-determination recipe for ice on distant bodies. §4. (121 cites.)

- **Cruikshank, D. P. et al. (1993)** — *Science* 261, 742. **No arXiv** (bibcode
  `1993Sci...261..742C`). *Ices on the Surface of Triton* — N₂/CH₄/CO₂/H₂O/CO ices on
  a bright high-albedo surface. §4, §7. (256 cites.)

- **Cruikshank, D. P. et al. (1998)** — *Icarus* 135, 389. **No arXiv** (bibcode
  `1998Icar..135..389C`). *The Composition of Centaur 5145 Pholus* — the tholin/organic
  reddening archetype (reddest known solar-system surface). §4, §7. (239 cites.)

- **Grundy, W. M. et al. (2016)** — *Science* 351, aad9189. **arXiv:1604.05368.**
  *Surface compositions across Pluto and Charon* (New Horizons) — maps the N₂/CH₄/CO/
  H₂O ices vs the dark-red tholin terrains. §7. (211 cites.)

- **Buratti, B. J. et al. (2017)** — *Icarus* 287, 207. **arXiv:1604.06129.** Global
  albedos of Pluto and Charon from New Horizons LORRI — the resolved geometric/Bond
  albedo maps for the Pluto example. §6, §7. (77 cites.)

- **de Pater, I. & Lissauer, J. J.** — *Planetary Sciences*, Cambridge Univ. Press
  (2001 1st / 2010 2nd / 2015 3rd ed.). **Book, no arXiv** (bibcode
  `2010plsc.book.....D`). Standard text for the geometric-albedo, phase-integral and
  Bond-albedo definitions and the `A = q·p` relation. §6. (63/33 cites by ed.)

- **Polyanskiy, M. N. (2024)** — *Scientific Data* 11, 94. **No arXiv** (bibcode
  `2024NatSD..11...94P`). The **refractiveindex.info** database — the optical-constant
  portal; **here the solid/liquid-phase entries** (minerals, water/N₂/CH₄/CO₂ ices,
  tholins) for the Hapke `n+ik` step (§3), vs the gas-phase entries used by the
  atmosphere doc. Cite each dataset's own primary source per row. (335 cites.)

- **RELAB Spectral Library Bundle** — PDS Geosciences Node / Brown University (bibcode
  `2020pds..data...98M`, DOI 10.17189/1519032). **Database, no journal-paper
  descriptor.** Complementary planetary-analog reflectance library (meteorites, lunar/
  asteroid analogs, ices). §3. (23 cites on the PDS bundle record.)

- **CIE 1931 / IEC 61966-2-1 (sRGB)** — engineering standards (not ADS works); the
  colorimetry kernel is **not restated here** — see `atmosphere-reflected-color-
  methodology.md` §8. §5.

**No clean canonical ADS paper for**: (a) the spectrum→sRGB colorimetry math (CIE/IEC
standard, owned by the atmosphere doc §6); (b) a single definitive journal paper for
"Bond albedo / phase integral" — it is textbook material (de Pater & Lissauer above),
with historical roots in Russell's and Bond's photometry rather than one citable modern
paper. (c) RELAB has no peer-reviewed descriptor paper of record; cite the PDS bundle.

---

## 관련 문서

- `docs/reference/atmosphere-reflected-color-methodology.md` — 여기서 재사용하는
  **색측정 엔진**(§6: 스펙트럼 → XYZ → sRGB, 광원은 모항성 SED)과
  **refractiveindex.info 포털**(Polyanskiy 2024; 거기서는 기체상, 여기서는 고체·액체상)을
  소유한 **자매** 문서다. 대기의 반사색은 이 문서가 도출한 표면색 **위에** 얹힌다.
  두꺼운 덱에서는 표면이 가려진다.
- `docs/reference/tidally-locked-temperature-methodology.md` — §6의 **Bond 알베도
  `A`를** `T_eq = [S(1−A)/4σ]^¼`에서 **소비한다**. 표면 선택은 `(1−A)^¼`를 통해 온도로
  전파된다.
- `docs/reference/tidal-heating-methodology.md` — 바디 에너지 수지의 다른 쪽(내부
  가열)으로, 흡수된 항성 항(이 `A`)과 함께 표면 온도를 정한다.
- `docs/reference/planetary-dynamo-scaling.md` — 인용 엄밀성과 유효 영역 정직성의 금본위
  자매 문서다(no-arXiv 표시, 영역 경계 단서).
- **발광 색**(재진입 플라스마, 기광, 오로라, 용암 열복사)은 `firefly-cfg` 스킬과
  `composition-color.md`에 산다 — 다른 메커니즘(반사가 아니라 발광)이다. 여기의 반사
  표면색과 혼동하지 말 것.
- Phase 3 합성 스킬(`nearstars-phase3`) — 고른 표면색과 가정한 표면 상태, Bond 알베도가
  하류의 cfg 라이터(Kopernicus 표면색 / Scatterer)와 온도 계산으로 들어가기 전에
  바디별로 기록되는 곳이다.
