# R6 리서치 프롬프트 — 중력 유의도 바닥(gravity significance floor) 근거화 (NearStars에서, ADS로 실행)

아래 선(line) 아래의 전부를 NearStars 세션에 복사해 넣어라(그 세션에 ADS API 토큰과
`https://api.adsabs.harvard.edu/v1/search/query`용 `scripts/phase3/build_bibliography.py`
패턴이 있다). 출력 리포트는 Principia 세션으로 돌아오고, 그쪽에서 파라미터를 확정한다.

---

## 과제

당신은 중력 절단(truncation) 방식의 두 수치 파라미터를 문헌으로 근거화하고 있다.
`plans/principia-interstellar-branch/research/R6-significance-floor.md`를 산출하라 —
숫자, bibcode, 짧은 축자 인용을 담은 자족적 리포트다. 다른 세션이 당신의 리포트만 보고
파라미터를 정할 것이므로, 결론만이 아니라 증거를 포함하라.

## 맥락 (이미 만들어진 것. 다시 도출하지 말 것)

Principia(KSP n-body 모드) 포크가 뉴턴 중력에 **쌍(pair)별 far-field 감쇠**를 추가해,
(a) 별계 사이 void의 선체가 정확히 무힘(force-free) 상태가 되게 하고 (b) 물리적으로
무의미한 쌍(예. 서로를, 그리고 40-ly 떨어진 계를 섭동하는 수백 개의 RSS-Origin
소행성들)에 대한 계산 낭비를 멈춘다.

기법. 각 천체는 cutoff 반경 **r_c = √(μ/a_floor)**를 가진다 — 그 천체의 점질량 가속도가
바닥 `a_floor`로 떨어지는 거리다. potential(힘이 아니라)에 C² 5차(quintic) 시그모이드 σ를
곱한다. r_c/3 아래에서는 손대지 않고, [r_c/3, r_c]에서 매끄럽게 램프되며, r_c 너머로는
**정확히 0**이다. 유질량-유질량 쌍에서는 σ 하나를 두 구성원에 대칭으로 적용하고(뉴턴 제3법칙,
운동량 정확 보존), 쌍 cutoff는 max(r_c_a, r_c_b)로 둔다 — 그래서 소행성은 자기 별을 결코
안 느끼게 되지 않고(별의 r_c가 지배), 소행성↔소행성 또는 별↔광년-너머-별 쌍은 사라진다.
짚어둘 만한 결과. 소행성↔행성 쌍은 살아남는다(행성 r_c ~ 133 AU). 그래서 벨트가 행성에
미치는 집합적 효과는 유지되고, 소행성↔소행성만 죽는다.

잠정적으로 `a_floor = 1e-12 m/s²`(태양질량 r_c ≈ 1.2 ly)이고 shell 비율 outer/inner = 3
(upstream HarmonicDamping 관행). 둘 다 아직 **임의값**이다 — 오너는 이것들이 정당화되거나
문헌 근거값으로 대체되기를 원한다.

대조해 저울질할 프로파일. 게임플레이 타임스케일은 최대 ~수 세기의 timewarp. 플레이어가
측정하는 것은 상대적 시뮬레이션 내 양(궤도, 근접 조우, 기동 계획)이지 절대 좌표가 아니다.
확인된 최악 드리프트는 ~500 m/yr(cutoff 경계에서의 coherent 최악 경우). 로스터. RSS-Origin
(수백 개의 소행성 천체)과 NearStars(다중성. 가장 가까운 속박 쌍 ~0.2 ly —
`db/binary_orbits.json`에서 실제 최솟값을 VERIFY해 보고하라).

## 리서치 각도

### A. 행성 ephemeris의 섭동체 선택 (가장 강한 선례)
DE, INPOP, EPM은 어떤 소행성을 섭동체로 포함할지 어떻게 정하며, 나머지는 어떻게 처리하나.
- JPL DE430/431. Folkner et al. 2014 (IPN Progress Report 42-196). DE440/441. Park,
  Folkner, Williams & Boggs 2021 (AJ 161, 105). 소행성 섭동체 개수(343?), 선택 기준
  (데이터 스팬에 걸친 Earth–Mars range에 미치는 효과? 질량 임계값?), 그리고 무시되는 것의
  명시된 크기.
- INPOP (Fienga et al., INPOP19a/21a 논문들). 개별 소행성 개수 + 임계값 미만 잔여를
  합산하는 데 쓰는 **소행성 링(asteroid ring)** — 링의 총질량과, 버리기 vs 합산하기의
  논거를 추출하라.
- EPM (Pitjeva & Pitjev). 개수(~301?) + 링.
- 산출물. 정량적 선택 임계값(위치-효과 미터 및/또는 가속도 단위), 그리고 "버리기" vs "합산"이
  우리 충실도에서 유의미한지 여부.

### B. 검출 가능성 하한 — 누군가 측정한 가장 작은 coherent 가속도
어떤 관측자(하물며 게임)가 알아챌 수 있는 것의 한계를 짓는다.
- NEA에 대한 Yarkovsky-효과 검출. 전형적으로 측정된 da/dt ↔ 가속도 ~1e-15–1e-13 m/s²,
  ≥ 10년에 걸친 레이더 ranging으로만 검출됨(Chesley et al. 2003, Golevka.
  Vokrouhlický et al. Farnocchia et al. 2013 카탈로그). 추출. 가속도 크기 vs 시간 스팬 vs
  필요한 ranging 정밀도.
- Pioneer 이상(~8.7e-10 m/s²)을 "수십 년에 걸친 우주선-추적 검출 가능성의 가장자리"라는
  고전 데이텀으로(Anderson et al. Turyshev et al.의 해소).
- 산출물. 가속도 ↔ 그것을 보는 데 어떤 기기/시간 스팬이 걸렸는지의 표.

### C. 항성 동역학 — 별–별 중력이 유의미한 물리이기를 멈추는 지점
우리가 모델링하지 *않는* Galactic tide가 어떤 이격 너머에서 상호 인력을 지배한다면, 거기서
자르는 것이 벌거벗은 2체 항을 유지하는 것보다 *더* 물리적이다.
- ~1 M☉ 쌍의 wide-binary 붕괴 / Jacobi(tidal) 반경(~1.7 pc?). Jiang & Tremaine 2010.
  Chanamé & Gould. El-Badry 리뷰들. 관측된 가장 넓은 속박 쌍성(~0.1–1 pc).
- 추출. 이격에 따른 tidal 가속도 스케일(Oort 상수), 1+1 M☉에서 a_tide ≈ a_mutual가 되는
  이격, 그리고 우리 r_c(1 M☉)와의 비교.

### D. N-body 수치 관행 — 힘-오차 허용 범위와 외곽 절단 선례
- 장기 행성 적분 오차 예산. 커뮤니티 표준으로 삼는 상대 힘/에너지 오차는 얼마인가
  (Wisdom & Holman. Rein & Spiegel 2015 IAS15. Rein & Tamayo WHFast. Hairer류의
  backward-error 논거). O(a_floor) 정적 힘 편향은 인정되는 적분기 절단과 어떻게 비교되나.
- 충돌 vs 무충돌 힘-정확도 표준. tree-code opening-angle ↔ 상대 힘 오차(Barnes & Hut 1986과
  후속들. Dehnen 2002). star-cluster 코드는 어느 정도의 힘 오차를 허용하나.
- 중력의 외곽(OUTER) 매끄러운 절단에 대한 선례(P³M/Ewald 단거리 스위칭, MOND-free 외곽 cutoff
  등), 그리고 있다면 스위칭-shell 폭(WIDTH)에 대한 지침(우리 outer/inner = 3은 현재 물리가
  아니라 관행이다). 문헌에 shell 폭에 관한 것이 아무것도 없으면 명시적으로 그렇게 말하라 —
  그러면 우리는 내부 에너지-보존 테스트로 정당화한 3× 관행을 유지한다.

### E. (부차적, non-ADS 허용) 운영 힘-모델 관행
우주선-항법 힘 모델. Mars 미션에 어떤 제3체/소행성을 포함하나(JPL "Big16"?), GMAT/Orekit
기본값은 무엇인가. 여기서는 문서 출처도 괜찮다. 짧게 — 한 문단.

## 종합 질문 (명시적으로 답하라)

설계는 **기준 유형(criterion type)**을 고른 뒤 값을 골라야 한다.
1. 절대 가속도 바닥(현재. a < 1e-12 m/s²에서 절단) vs
2. 상대 유의도(a_pair/a_dominant < ε에서 절단 — R3의 선체-경로 규칙) vs
3. 관측-효과 기반(스팬 T에 걸쳐 측정량을 < X만큼 바꾸는 것을 절단 — ephemeris-구성 방식).
자기-정합적 게임 시뮬레이션에 대해 증거는 어느 쪽을 지지하며, 값은 얼마인가. 다음을 제시하라.
권고 a_floor(또는 등가), 허용 범위, 범위의 각 끝이 무엇을 맞바꾸는지(드리프트 vs 살아남는 쌍
개수 — 소행성↔소행성 이득에는 r_c(μ~1e9 m³/s²)가 전형적 벨트 이격 아래여야 함을 상기),
그리고 NearStars 로스터에 대한 sanity check(주성의 r_c보다 넓은 속박 쌍성이 없어야 함. db에서
검증하라). shell 비율에 대한 권고도, 존재하는 근거가 무엇이든 함께 밝혀라.

## 방법 요건

- 각도별 표적 쿼리로 ADS API 사용(phase3 bibliography 파이프라인은 필요 없다 — 직접
  `search/query` 호출로 충분). 초록을 읽고, load-bearing 숫자는 arXiv/ar5iv로 full text를
  읽어라. WebFetch 요약의 숫자를 인용하지 말고, 원 소스를 읽어라. 모든 주장을 bibcode(가능하면
  + arXiv id)에 핀으로 고정하라.
- ~15–25편이 예상 규모다. 각도 C(관측된-개체군 숫자는 리뷰도 괜찮다)를 제외하면 리뷰보다
  1차 출처를 선호하라.
- 리포트를 각도(A–E)별로 구성하고, 각 각도는 박스 처리된 "추출된 숫자(numbers extracted)"
  목록으로 끝맺어라. 마지막 절 = 위의 종합 답변.
- 어떤 각도가 정말로 비어 나오면, 그것을 하나의 발견으로 기록하라(선례의 부재도 그 자체가
  입력이다 — 그러면 우리는 내부 테스트로 그 선택을 스스로 떠맡는다).
