<!-- 미측정 항성/갈색왜성 자전축 시선경사 i★를 v sin i + 자전주기 + 반지름 결합으로 도출하는 방법(논문 근거) -->
# 자전축 시선경사 근거화 — v sin i + 자전주기 + 반지름 결합법

**직접 측정된 i★가 없는** 항성/갈색왜성의 **자전축 시선경사 i★**를 세 관측량 —
투영 자전속도(v sin i, 분광), 자전주기(P, 측광), 반지름(R) — 의 결합으로
도출하는 방법 레퍼런스입니다. i★ *측정치*가 있는 바디(tau Cet·Fomalhaut의
간섭계 해, 도플러 이미징 피팅)는 그 측정을 passthrough하며, 이 레시피는
결합 경로 전용입니다.

첫 소비자는 Luhman 16 A/B Phase 4 보드의 자전축 행입니다.

## 관계식

강체 회전 구로 보면 실제 적도 속도는

    v_eq = 2π R / P

이고 분광 선폭은 그 투영을 재므로

    sin i★ = v sin i / v_eq = (v sin i · P) / (2π R)

기하 자체는 교과서(허용 예외)지만, *경사 추정기로서의 사용*은 갈색왜성 변광
문헌의 표준 절차입니다. Vos, Allers & Biller 2017
([`2017ApJ...842...78V`](https://ui.adsabs.harvard.edu/abs/2017ApJ...842...78V),
arXiv [1705.06045](https://arxiv.org/abs/1705.06045), 캐시됨)이 절차와 가정을
명시하고(강체 회전 — 목성의 핵/구름 주기차가 ~5분에 불과해 측광 주기 정밀도
수준에서 정당) 변광 갈색왜성 19개에 적용했습니다.

## 실용 공식

R을 목성 반지름(R_Jup = 71 492 km), P를 시간 단위로 쓰면

    v_eq [km/s] = 124.78 · (R / R_Jup) / P_hr
    sin i★      = v sin i / v_eq

규약: i★ = 90°가 적도방향(equator-on), 0°가 극방향(pole-on)입니다. 분광
선폭은 i와 180° − i(북극이 보이는지 남극이 보이는지)를 구분하지 못하므로
결과는 0–90°로 적습니다(Masuda & Winn 2020 §II).

## 통계 규율 (Masuda & Winn 2020)

Masuda & Winn 2020
([`2020AJ....159...81M`](https://ui.adsabs.harvard.edu/abs/2020AJ....159...81M),
arXiv [2001.04973](https://arxiv.org/abs/2001.04973), 캐시됨)은 v sin i와
v_eq를 각자의 오차에서 독립으로 뽑아 sin i 히스토그램을 만드는 소박한 몬테
카를로가 **틀렸음**을 보였습니다. 두 양은 통계적으로 독립이 아니고(항상
v sin i ≤ v_eq), 소박한 절차는 "cos i ≈ 1(극방향) 확률밀도를 심하게
과대평가"합니다. 올바른 대상은 **cos i**의 사후분포(등방 축이면 평탄)입니다.

NearStars에서의 귀결(전체 베이지언 계산은 돌리지 않습니다).

1. **i★는 가우시안이 아니라 한계 또는 구간으로 보고합니다.** 입력 범위(R·P의
   최소/최대)를 공식에 끝값끼리 통과시켜 "i★ > X°" 또는 "X°–90°"로 적습니다.
   보드 행과 뷰어 레이어가 실제로 쓸 수 있는 형태입니다.
2. **명목 sin i★ > 1은 오류가 아닙니다.** 불확도 안에서 v sin i ≈ v_eq라는
   뜻이며, 적도방향(i★ ≈ 90°)으로 읽고 초과분은 입력 오차가 흡수합니다.
   가짜 정밀도의 90° ± 소량으로 "클리핑"하지 않습니다.
3. **낮은 경사 주장은 특히 조심합니다**(소박한 방법의 편향이 그쪽에서 가장
   큽니다). 적도방향 결론은 견고하지만 극방향 결론은 그렇지 않습니다.

## 유효 영역 / 분기

1. **직접 i★ 측정이 있는 경우**(간섭계 회전 해, 도플러 이미징): 측정을
   passthrough하고 도출하지 않습니다. (NearStars: tau Cet 7°±7° Korolik
   2023, Fomalhaut 90°±9° Hadjara 2014.)
2. **세 입력이 모두 측정된 경우**(v sin i + P + R): 위 통계 규율과 함께
   공식을 적용합니다. 신뢰도는 가장 약한 입력을 따르고, 주기가 논쟁 중이면
   i★는 주기 선택에 조건부가 되므로 행에 어느 주기를 가정했는지 명기합니다.
3. **반지름 미측정** — 갈색왜성의 보편 상황(직접 측정된 반지름을 가진 L/T
   왜성은 없음): 전자 축퇴의 필드 갈색왜성 반지름 0.8–1.2 R_Jup을 씁니다
   (Burrows et al. 2001,
   [`2001RvMP...73..719B`](https://ui.adsabs.harvard.edu/abs/2001RvMP...73..719B);
   필드 나이에서 반지름은 질량과 거의 무관). 큐레이션된 경우 해당 천체의
   진화모델 반지름(Filippazzo et al. 2015,
   [`2015ApJ...810..158F`](https://ui.adsabs.harvard.edu/abs/2015ApJ...810..158F))을
   우선합니다. 반지름 범위 전체를 i★ 구간에 전파합니다.
4. **느린 회전자, v_eq ≲ 2–2.5 km/s**: 정밀도 문제가 아니라 *원리적으로*
   레시피가 무너집니다. 분광 v sin i는 ~2–2.5 km/s 아래에서 신뢰할 수
   없고(난류·기기 선폭이 지배, Dumusque 2014,
   [`2014ApJ...796..133D`](https://ui.adsabs.harvard.edu/abs/2014ApJ...796..133D)),
   느린 회전자는 통째로 그 바닥 밑에 있습니다. 대체 경로를 씁니다 —
   활동/시선속도 모델링(SOAP: Dumusque 2014의 α Cen B i★ = 45°(+9/−19))
   또는 Zeeman-Doppler 이미징(Klein 2021의 Proxima i★ = 47°±7°).
   NearStars 사례: α Cen B(v_eq 1.07 km/s)와 Proxima(0.085 km/s)는 측정된
   대체 경로 값을 유지하며, 결합법으로는 검증 자체가 불가능합니다.
5. **주기나 v sin i가 없는 경우**: 레시피가 적용되지 않습니다. 등방 사전분포
   (cos i★ 평탄)가 정직한 상태이며, 그 위에 얹는 배향은 도출이 아니라 오너
   아트 선택(owner-override)입니다.

남는 주의점들. 차등회전(위 목성 5분 논거로 상한이 잡힘), 변하는 날씨에서 나온
측광 주기는 에포크마다 표류할 수 있음(Apai 2021의 Luhman 16 B 주기 분열 —
정본 주기를 쓰고 산포를 병기), 그리고 도출된 i★는 하늘에서의 자전축
*방위각*에 대해서는 아무것도 말하지 않습니다(별도의, 보통 자유로운 emit
배향).

## 계산 예 — Luhman 16 A·B (첫 소비자)

입력: v sin i 17.6 ± 0.1 km/s (A), 26.1 ± 0.2 km/s (B) (Crossfield et al.
2014, 캐시됨); P_A = 6.94시간(Apai et al. 2021, 잠정), P_B = 4.87시간
(Gillon et al. 2013, Apai 2021 TESS 분석은 4.9–5.3시간 산포);
R = 0.90–1.10 R_Jup (Burrows 2001 축퇴 반지름, Apai 2021이 채택한 구간).

| 바디 | P (hr) | v_eq (R 0.90–1.10 R_Jup) | sin i★ = v sin i / v_eq | i★ |
|---|---|---|---|---|
| A | 6.94 | 16.2–19.8 km/s | 0.89–1.09 | **> 62°** (적도 쪽) |
| B | 5.28 (TESS) | 21.3–26.0 km/s | 1.00–1.23 | **≈ 90°** (적도방향) |

검증: Apai et al. 2021 §6.2의 발표값을 그대로 재현합니다 — v_eq 구간
(A 16.3–19.9, B 21.2–25.9 km/s; 차이는 R_Jup 반올림 자리뿐)과 결론 "Luhman
16 A는 적도면에서 28° 안에서 보인다(i > 62°)", "B는 거의 정확히 적도방향
(i ≃ 90°)". B의 명목 sin i★가 작은 반지름 끝에서 1.23까지 가는 것이 규율
2번의 사례입니다 — 적도방향이고 초과분은 반지름 구간이 흡수합니다.

시스템 보너스: AB 궤도 경사는 79.21° ± 0.45°입니다(Bedin et al. 2017,
[`2017MNRAS.470.1140B`](https://ui.adsabs.harvard.edu/abs/2017MNRAS.470.1140B),
arXiv [1706.00657](https://arxiv.org/abs/1706.00657); 큐레이션된 Lazorenko &
Sahlmann 2018 궤도의 100.26°는 노드/방향 규약이 반대인 같은 평면으로,
180° − 100.26° = 79.74°). Apai 2021은 두 자전축과 궤도 법선이 "잘 정렬돼
있을 수 있다"고 적습니다 — 세 평면이 서로 ~28° 안에 있고, 비정렬의 증거는
없습니다.

## 계산 예 — α Centauri A (분기 2의 항성)

입력: v sin i 2.7 ± 0.7 km/s (Saar & Osten 1997), P 22 ± 3일 (DeWarf 2010,
DB recommended), R 1.2234 R☉ (Kervella 2017). v_eq = 2.81 km/s(주기 범위에서
2.48–3.26) → 명목 sin i★ = 0.96 → **i★ ≈ 74°, 구간 38°–90°**(끝값 전파).
자전-궤도 정렬(AB 궤도 경사 79°)과 정합합니다. Bazot et al. 2007은 같은
관계식을 거꾸로 돌렸습니다 — i = 79° 정렬을 가정하면 v sin i가 P = 22.5 ±
5.9일을 예측하고, 측광 22일과 맞습니다. 양방향이 같은 숫자로 닫히는 것이
교차검증입니다. 동반성들과 대비하면, α Cen B(v_eq 1.07 km/s)와 Proxima
(0.085 km/s)는 이 레시피가 돌 수 없는 분기 4의 느린 회전자입니다.

## 인용

- **Vos, Allers & Biller 2017**, ApJ 842, 78 ([`2017ApJ...842...78V`](https://ui.adsabs.harvard.edu/abs/2017ApJ...842...78V),
  arXiv [1705.06045](https://arxiv.org/abs/1705.06045), **캐시됨**). 결합법의
  갈색왜성 표준 적용 — 절차, 강체 구 정당화, 필드 갈색왜성 반지름 처방
  (0.8–1.2 R_Jup), 19천체 표본.
- **Masuda & Winn 2020**, AJ 159, 81 ([`2020AJ....159...81M`](https://ui.adsabs.harvard.edu/abs/2020AJ....159...81M),
  arXiv [2001.04973](https://arxiv.org/abs/2001.04973), **캐시됨**). 통계
  처리 — v sin i와 v_eq는 상관돼 있고, 소박한 샘플링은 극방향으로 편향되며,
  cos i에서 작업할 것. 보고 규율의 출처.
- **Apai et al. 2021**, ApJ 906, 64 ([`2021ApJ...906...64A`](https://ui.adsabs.harvard.edu/abs/2021ApJ...906...64A),
  arXiv [2101.02253](https://arxiv.org/abs/2101.02253), **캐시됨**). Luhman
  16 A/B에 이 방법을 적용(§6.2) — 검증 앵커이자 Phase 4 보드가 소비하는 값.
- **Crossfield et al. 2014**, Nature 505, 654 ([`2014Natur.505..654C`](https://ui.adsabs.harvard.edu/abs/2014Natur.505..654C),
  arXiv [1401.8145](https://arxiv.org/abs/1401.8145), **캐시됨**). 두 성분의
  v sin i 측정.
- **Burrows et al. 2001**, RvMP 73, 719 ([`2001RvMP...73..719B`](https://ui.adsabs.harvard.edu/abs/2001RvMP...73..719B),
  arXiv [astro-ph/0103383](https://arxiv.org/abs/astro-ph/0103383)).
  0.8–1.2 R_Jup 필드 갈색왜성 처방의 근거인 전자 축퇴 반지름 평탄역.
- **Filippazzo et al. 2015**, ApJ 810, 158 ([`2015ApJ...810..158F`](https://ui.adsabs.harvard.edu/abs/2015ApJ...810..158F),
  arXiv [1508.01767](https://arxiv.org/abs/1508.01767)). 천체별 진화모델
  반지름 — 큐레이션돼 있으면 일반 구간보다 우선.
- **Dumusque 2014**, ApJ 796, 133 ([`2014ApJ...796..133D`](https://ui.adsabs.harvard.edu/abs/2014ApJ...796..133D),
  arXiv [1409.3593](https://arxiv.org/abs/1409.3593)). 느린 회전자 바닥
  (v sin i는 ~2–2.5 km/s 아래에서 신뢰 불가)과 SOAP 대체 경로
  (α Cen B i★ = 45°).
- **Saar & Osten 1997**, MNRAS 284, 803 ([`1997MNRAS.284..803S`](https://ui.adsabs.harvard.edu/abs/1997MNRAS.284..803S)).
  α Cen A의 v sin i(2.7 ± 0.7 km/s; 캐시된 Bazot 2007,
  arXiv [0706.1682](https://arxiv.org/abs/0706.1682)가 원문 인용). *1997
  MNRAS, arXiv 프리프린트 없음*: bibcode + 캐시된 2차 인용으로 검증.
- **Bedin et al. 2017**, MNRAS 470, 1140 ([`2017MNRAS.470.1140B`](https://ui.adsabs.harvard.edu/abs/2017MNRAS.470.1140B),
  arXiv [1706.00657](https://arxiv.org/abs/1706.00657)). 자전-궤도 정렬
  노트에 쓴 Luhman 16 AB 궤도 경사.

## Related

- [cassini-state-obliquity-methodology](cassini-state-obliquity-methodology.md) —
  조석 감쇠 천체의 *평형 기울기* 상대편. 이 문서는 자유 회전체의 *관측 시선*
  경사입니다. 교차 적용 금지.
- [body-figure-methodology](body-figure-methodology.md) — 측정된 i★를 3-D
  회전 해와 J₂에 소비(Fomalhaut 계산 예).
- [methodology-index](methodology-index.md) — derived-value 레시피 전체 인덱스.
