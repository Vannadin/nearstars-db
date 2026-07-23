<!-- 태양계 자기권 천체 7종의 실제 방사선대 물리 vs Kerbalism 스톡 cfg 비교 (ADS 근거, 위키 시각화 연동) -->
# 태양계 방사선대: 스톡 Kerbalism cfg vs 실제 물리

**포획 입자 벨트를 가진 자기권**(또는 그저 자기권을 가진) 태양계 천체를 하나씩 훑으며,
**Kerbalism / ROKerbalism 스톡 cfg**를 **ADS로 근거화한 실제 물리**와 대조하는 감사입니다.
NearStars의 자기권 지오메트리 레시피가 가상 천체용 벨트를 뽑아내기 전에 실제 바디로 먼저
보정하고, 스톡 모델이 러프한 자리채움에 그친 곳에는 물리 정확 cfg 값을 되먹이려고 존재합니다.

단면 시각화는 위키에 있습니다.
**[Radiation Belts](https://github.com/Vannadin/nearstars-db/wiki/Radiation-Belts)** —
바디마다 두 렌더 모두 인게임 `RadiationModel` SDF입니다. **스톡**은 출하 cfg, **물리**는 같은
토러스 모델을 실제 벨트에 재적합한 것입니다(맞는 standoff·L-shell 위치, 초승달용 D컷 border).
산출물은 이 최선의 cfg 근사 — 인게임에서 멀쩡히 보입니다 — 이지, emit 못 하는 필드라인 렌더가
아닙니다. 2-셸 토러스로는 실제 특징 일부(필드라인 곡률, 위성/고리 간극)를 못 담습니다(아래 명시).
렌더러는 `scripts/viz/render_belts.py`, SDF는 [`Radiation.cs`](https://github.com/Kerbalism/Kerbalism/blob/master/src/Kerbalism/Radiation/Radiation.cs)
재현(출처 [Kerbalism](https://github.com/Kerbalism/Kerbalism), [Unlicense](https://github.com/Kerbalism/Kerbalism/blob/master/LICENSE)·퍼블릭 도메인). 場 모양 스키마는
[`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md)
를 보세요.

## Scope — 자기화된 바디만

벨트가 생기려면 입자를 가둘 만큼 강한 고유 다이나모가 필요합니다. 태양계에서는 **7개 바디**
입니다. 지구, 목성, 토성, 천왕성, 해왕성(행성 다이나모), 수성(아주 작음), 그리고 가니메데
(임베디드 위성 다이나모)입니다. **금성, 화성, 달, Io, Europa, Callisto, Titan, Triton, 명왕성**
은 고유 전역장이 없어 → 벨트가 없고 → 표면 선량이 곧 직접 풍/GCR 플럭스입니다
(`radiation_surface`만, `RadiationModel` 벨트 없음). 여기서는 범위 밖입니다.

## Summary table — 물리 앵커 (전부 ADS 핀)

| Body | Magnetopause standoff | Dipole tilt | Offset | Belt structure | Peak dose (order) |
|---|---|---|---|---|---|
| **Earth** | ~10 R_E | 11° | small | two separated belts (D inner + hollow outer) | ~10² rad/day (peak) |
| **Jupiter** | **63 R_J** (compressed) / 92 (expanded) | 10.3° | ~0.13 R_J | dipolar inner (D-cut) + flat magnetodisc | ~10³–10⁴ rad/day |
| **Saturn** | **22–27 R_S** | **<0.007°** | 0.047 R_S N | **no classic inner belt** (rings sweep it); weak moon-chopped outer; CRAND-only | ≪ Jupiter |
| **Uranus** | **18 R_U** | **59°** | **0.3 R_U** | offset+tilted, moon-swept, helical tail | e⁻ ≥1.2 MeV |
| **Neptune** | **26.5 R_N** | **47°** | **0.55 R_N** | offset+tilted, peak L≈7, Triton cut ~14 R_N | e⁻ >1 MeV |
| **Mercury** | **1.45 R_M** (1.35–1.55) | <3° | 0.20 R_M N (484 km) | **no stable belt** — surface is the loss cone | (surface direct) |
| **Ganymede** | **~2 R_G** (upstream) | ~176° (≈anti-aligned) | — | weak embedded, **open polar caps**, source-starved | shield −50–60% of ambient |

핵심 발견 세 가지. **(1)** 스톡 Kerbalism/RSS는 빙거성의 offset-기운 쌍극(천왕성/해왕성)과
수성의 offset을 이미 제법 잡아냅니다. **(2)** 큰 스톡 오류는 **목성**(벨트가 너무 바깥,
D-cut 없음, magnetodisc 없음)과, 어디서나 나타나는 **벨트 강도의 출처 문제**(스톡 값은 튜닝된
것이지 도출된 게 아님)입니다. **(3)** **토성의 "외대만, 내대 없음"** 스톡 선택은 *물리적으로
옳습니다* — 고리가 내대 자리를 차지하고 흡수해 버립니다.

---

## 바디별: 스톡 cfg vs 물리

각 블록은 스톡 `RadiationBody`/`RadiationModel`(ROKerbalism `System/Radiation.cfg` + RSS
앵커), ADS 핀이 붙은 물리값, 그리고 그 차이(delta)를 제시합니다.

### Earth (캘리브레이션 앵커 — 단, 스톡 = 물리는 아님)
| Field | Stock (`earth`) | Physical | Source |
|---|---|---|---|
| pause_radius | 15 | **~10 R_E** (subsolar) | Shue 1997 [`1997JGR...102.9497S`](https://ui.adsabs.harvard.edu/abs/1997JGR...102.9497S), Fairfield 1971 [`1971JGR....76.6700F`](https://ui.adsabs.harvard.edu/abs/1971JGR....76.6700F) |
| inner belt | 0.813/0.70, border 0.915 (D-cut) | 피크 **L≈1.5**, ~1.1–2 R_E | (AP9; Ripoll 2016) |
| outer belt | 2.63/2.48 (피크 ~2.6 R_E) | **heart L≈4–5**, L 3–7 | Reeves 2013 [`2013Sci...341..991R`](https://ui.adsabs.harvard.edu/abs/2013Sci...341..991R), Thorne 2013 [`2013Natur.504..411T`](https://ui.adsabs.harvard.edu/abs/2013Natur.504..411T) |
| slot region | (D-cut 간극) | **L≈2–3** (hiss가 비움) | Ripoll 2016 [`2016GeoRL..43.5616R`](https://ui.adsabs.harvard.edu/abs/2016GeoRL..43.5616R) |
| radiation_inner/outer | 10.376 / 2.214 | 자릿수 일치 | — |
| geomagnetic_pole_lat / offset | 80.37 (tilt 9.6°) / 0.07 | tilt ~11° / ~0.08 R_E | IGRF (정확) |

앵커는 *성격은 좋습니다* — D컷 내대, 속 빈 외대, 정확한 쌍극 tilt/offset, 관측 양성자 피크와
맞는 내대 선량 ~10.4 rad/h. 다만 **위치 두 가지가 어긋납니다**. 자기권계면이 ~1.5배 넉넉하고
(15 vs ~10 R_E), 외대 중심이 ~2.6 R_E로 실제 외대 heart(L≈4–5)보다 안쪽입니다 — 물리적으론
벨트가 L≈1.5와 L≈4–5에 있고 그 사이를 슬롯(L≈2–3)이 가릅니다. 그래서 캘리브레이션 앵커인
지구조차 깔끔한 스톡 = 물리는 아닙니다.

### Jupiter
| Field | Stock (RSS `jupiter`) | Physical | Source |
|---|---|---|---|
| inner_dist / radius | 6.0 / 1.0 | **2.0 / 2.0** (dipolar, ~1.5–2 R_J peak) | Divine & Garrett 1983 [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D) |
| inner_border_radius | (none) | **1.3** (loss-cone D-cut) | (belt physics) |
| outer_dist / radius | 6.5 / 6.5 (concentric) | **4.17 / 2.5, deform_xy 0.174** (flat magnetodisc) | Khurana 1989 [`1989JGR....9411791K`](https://ui.adsabs.harvard.edu/abs/1989JGR....9411791K) |
| pause_radius | 60 | **63** (compressed; 92 expanded) | Joy 2002 [`2002JGRA..107.1309J`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1309J) |
| radiation_inner | 300 | **~1500** (order 10³–10⁴; conf low) | Divine & Garrett 1983 |
| geomagnetic_pole_lat | −81.4 | **−80** (tilt 10.3°, reversed) | Connerney 2022 JRM33 [`2022JGRE..12707055C`](https://ui.adsabs.harvard.edu/abs/2022JGRE..12707055C) |
| geomagnetic_offset | (none) | **0.1** (eccentric dipole) | JRM33 |

내대는 **쌍극형**(적도 + 비적도 전자, 피치각 0–90°. Santos-Costa 2001 [`2001P&SS...49..303S`](https://ui.adsabs.harvard.edu/abs/2001P%26SS...49..303S))
이라 → 납작하지 않고 둥급니다. 외대는 **경첩식 magnetodisc**(적도에 갇힌 전류 시트. Khurana
1989)라 → 납작합니다. Io/Amalthea/고리 흡수 gap(Santos-Costa 2001)은 두 셸로 표현할 수
없습니다 — 정밀도 천장입니다. 스톡은 강한 벨트를 ~3배 너무 바깥에 두고(6 vs ~2 R_J),
D-cut과 magnetodisc 평탄화를 둘 다 뺍니다.

### Saturn
| Field | Stock (RSS anchor) | Physical | Source |
|---|---|---|---|
| has_inner | false (outer only) | **false — correct** (rings absorb) | Cooper 1983 [`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C) |
| pause_radius | 20 | **~24** (22–27 bimodal) | Achilleos 2008 [`2008JGRA..11311209A`](https://ui.adsabs.harvard.edu/abs/2008JGRA..11311209A) |
| outer belt | 7/7 | ~2.3–6 R_S, moon-chopped corridors | Kollmann 2013 [`2013Icar..222..323K`](https://ui.adsabs.harvard.edu/abs/2013Icar..222..323K) |
| radiation_outer | 150 | **weak** (CRAND-only, ≪ Jupiter) | Kollmann 2017 [`2017NatAs...1..872K`](https://ui.adsabs.harvard.edu/abs/2017NatAs...1..872K) |
| dipole tilt | (near 0) | **<0.007°** (25.2 arcsec!) | Cao 2020 [`2020Icar..34413541C`](https://ui.adsabs.harvard.edu/abs/2020Icar..34413541C) |
| offset | — | 0.047 R_S north | Cao 2020 |

**스톡의 "외대만, 내대 없음"은 물리적으로 옳습니다**. 조밀한 A–C 고리가 정확히 내대가
형성될 자리에 앉아 그것을 흡수합니다(Cooper 1983). 살아남은 벨트는 위성 사이 통로로
잘게 잘립니다(Kollmann 2013, Roussos 2007 [`2007JGRA..112.6214R`](https://ui.adsabs.harvard.edu/abs/2007JGRA..112.6214R)). 공급원이 수동적 CRAND
라 강도는 목성보다 자릿수로 낮습니다(Kollmann 2017). 대기와 D-고리 사이에 얇은 고립
양성자 벨트가 있습니다만(Roussos 2018 [`2018Sci...362.1962R`](https://ui.adsabs.harvard.edu/abs/2018Sci...362.1962R)) — 실재하되 게임플레이엔
무시할 만합니다. 쌍극은 거의 완벽히 축대칭이라(Cao 2020) tilt ≈ 0입니다.

### Uranus
| Field | Stock (RSS anchor) | Physical | Source |
|---|---|---|---|
| geomagnetic tilt | pole_lat 31 (=59°) | **59–60°** ✓ | Ness 1986 [`1986Sci...233...85N`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...85N) |
| geomagnetic_offset | 0.3 | **0.3 R_U** ✓ | Ness 1986 |
| pause_radius | (≈18) | **18.0 R_U** (bow shock 23.7) | Ness 1986 |
| belt peak | — | **413 nT at 4.19 R_U** | Ness 1986 |
| radiation_inner | 75 | e⁻ ≥1.2 MeV, p ≥4 MeV | Krimigis 1986 [`1986Sci...233...97K`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...97K) |
| quadrupole | — | large (Q3 model) | Connerney 1987 [`1987JGR....9215329C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215329C) |

**스톡은 극단적인 offset-기운 쌍극을 이미 잡아냅니다**(tilt 59°, offset 0.3) — 주된 결함은
벨트 강도가 도출값이 아니라 튜닝된 자리채움이라는 점뿐입니다. 위성들(Miranda→Titania)이
17.24 h마다 거대한 L-범위에 걸쳐 벨트를 쓸어냅니다(Stone 1986 [`1986Sci...233...93S`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...93S)).
태양 쪽을 거의 가리키는 자전축이 꼬리를 나선으로 감아올립니다(pitch 5.5°. Behannon 1987
[`1987JGR....9215354B`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215354B)). 극성 부호는 1차 초록에서 언급되지 않았습니다(지어내지 않음).

### Neptune
| Field | Stock (RSS anchor) | Physical | Source |
|---|---|---|---|
| geomagnetic tilt | pole_lat 43 (=47°) | **47°** ✓ | Ness 1989 [`1989Sci...246.1473N`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1473N) |
| geomagnetic_offset | 0.55 | **0.55 R_N** ✓ | Ness 1989 |
| pause_radius | 26.5 | **26.5 R_N** ✓ (bow shock 34.9) | Ness 1989 |
| belt peak | — | **magnetic L ≈ 7** | Stone 1989 [`1989Sci...246.1489S`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1489S) |
| outer cutoff | — | **~14 R_N (Triton)** | Krimigis 1989 [`1989Sci...246.1483K`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1483K) |
| quadrupole/octupole | — | quad ≈ dipole at surface | Connerney 1991 [`1991JGR....9619023C`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619023C) |

천왕성처럼 **스톡이 offset-기운 쌍극을 잡아냅니다**(tilt 47°, offset 0.55). 벨트는 L≈7
(Proteus 4.75 R_N 바로 바깥)에서 피크를 찍고, 고리/위성 흡수로 도려집니다(Paranicas 1991
[`1991JGR....9619131P`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619131P)). 바깥은 Triton 궤도에서 딱 잘립니다. 행성 근처의 場은 강하게 비쌍극적
입니다(사극/팔극이 쌍극에 맞먹음).

### Mercury
| Field | Stock (ROKerbalism `mercury`) | Physical | Source |
|---|---|---|---|
| pause_radius | 1.6 | **1.45 R_M** (1.35–1.55, → 1.28 in storms) | Winslow 2013 [`2013JGRA..118.2213W`](https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W) |
| belts | none | **none** ✓ (too small/dynamic) | Schriver 2015 [`2015AGUFM.P53A2089S`](https://ui.adsabs.harvard.edu/abs/2015AGUFM.P53A2089S) |
| geomagnetic_offset | 0.208 | **0.198** (484 km north) | Anderson 2011 [`2011Sci...333.1859A`](https://ui.adsabs.harvard.edu/abs/2011Sci...333.1859A) |
| tilt | (small) | **<3°** (<0.8° refined) | Anderson 2011/2012 |
| moment | — | 190–195 nT·R_M³, southward | Anderson 2011, Korth 2015 [`2015JGRA..120.4503K`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.4503K) |

**스톡이 벨트 없음으로 옳게 모델링합니다** — 수성 자기권은 안정 개체를 가두기엔 너무 작고
동적입니다(준포획된 1–10 keV 적도 구름 + 일시적 버스트만 있음). 북향 offset(484 km ≈ 0.2 R_M)
이 표면 선량을 **남**반구/커스프에 몰아넣습니다. SEP 전자는 열린 자기력선을 타고 거의 즉시
표면에 닿습니다(Gershman 2015 [`2015JGRA..120.8559G`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.8559G)). 스톡 pause 1.6은 물리값 1.45보다 살짝
넉넉합니다.

### Ganymede
| Field | Stock (ROKerbalism `ganymede`) | Physical | Source |
|---|---|---|---|
| surface dipole | (implicit) | **719 nT eq** (tilt 176°) | Kivelson 2002 [`2002Icar..157..507K`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..507K) |
| has_pause | (none) | **~2 R_G upstream** (5.5 across) | Kivelson 1998 [`1998JGR...10319963K`](https://ui.adsabs.harvard.edu/abs/1998JGR...10319963K) |
| inner belt | 0.8/0.6, rad 0.33 | single weak, source-starved | Allioux 2013 [`2013AdSpR..51.1204A`](https://ui.adsabs.harvard.edu/abs/2013AdSpR..51.1204A) |
| open caps | — | **poleward of 30–45°** (leaky) | Pappalardo 1998 [`1998DPS....30.5401P`](https://ui.adsabs.harvard.edu/abs/1998DPS....30.5401P) |
| net role | — | **shield −50–60%** of ambient | Allioux 2013 |

태양계 유일의 **약장 임베디드 위성** — 거대행성 자기권 안의 다이나모입니다(지오메트리
방법론의 약장 sub-regime). 가니메데의 719 nT는 국소 목성 場을 살짝 넘길 뿐이라 →
작은 ~2 R_G standoff, **열린 극관**(목성과의 재결합), bow shock 없음(sub-Alfvénic → Alfvén
wings. Saur 2018 [`2018ASSL..448..153S`](https://ui.adsabs.harvard.edu/abs/2018ASSL..448..153S)). <~100 keV 이온만 얇은 벨트로 빚어냅니다. 지배적인
선량은 ~15 R_J의 목성 주변 벨트이고, 가니메데의 場은 저궤도 비행체에 대해 그걸 ~50–60%
감쇠시킵니다. **스톡은 pause를 통째로 뺍니다** — 추가할 가치가 있는 수정입니다.

---

## 두-셸 모델이 표현할 수 없는 것 (정밀도 천장)

- **위성/고리 흡수 gap**(토성 통로, 해왕성 Proteus 노치, 천왕성 위성 sweeping) — Kerbalism은
  내대+외대 토러스만 있고 L별 고갈이 없습니다.
- **시간 변동** — 빙거성 벨트는 매 자전마다 흔들립니다(tilt+offset). cfg는 정적입니다.
- **행성 근처 다극 왜곡**(천왕성/해왕성 사극≈쌍극) — 쌍극 `geomagnetic_offset`이 유일한 핸들입니다.
- **제1원리에서 나오는 벨트 강도** — 場 세기가 아니라 공급원/손실/Kennel–Petschek이 지배합니다
  (지오메트리 방법론 Part B 참조). 모든 `radiation_*` 값은 regime 판정이며 신뢰도 low입니다.

## 인용 (ADS 핀, 바디별)

- **Jupiter**: Joy 2002 [`2002JGRA..107.1309J`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1309J); Divine & Garrett 1983 [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D);
  Connerney 2022 (JRM33) [`2022JGRE..12707055C`](https://ui.adsabs.harvard.edu/abs/2022JGRE..12707055C); Santos-Costa 2001 [`2001P&SS...49..303S`](https://ui.adsabs.harvard.edu/abs/2001P%26SS...49..303S);
  Khurana 1989 [`1989JGR....9411791K`](https://ui.adsabs.harvard.edu/abs/1989JGR....9411791K).
- **Saturn**: Cooper 1983 [`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C); Achilleos 2008 [`2008JGRA..11311209A`](https://ui.adsabs.harvard.edu/abs/2008JGRA..11311209A);
  Kollmann 2013 [`2013Icar..222..323K`](https://ui.adsabs.harvard.edu/abs/2013Icar..222..323K); Kollmann 2017 [`2017NatAs...1..872K`](https://ui.adsabs.harvard.edu/abs/2017NatAs...1..872K); Roussos 2007
  [`2007JGRA..112.6214R`](https://ui.adsabs.harvard.edu/abs/2007JGRA..112.6214R); Roussos 2018 [`2018Sci...362.1962R`](https://ui.adsabs.harvard.edu/abs/2018Sci...362.1962R); Cao 2020 [`2020Icar..34413541C`](https://ui.adsabs.harvard.edu/abs/2020Icar..34413541C).
- **Uranus**: Ness 1986 [`1986Sci...233...85N`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...85N); Krimigis 1986 [`1986Sci...233...97K`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...97K); Stone
  1986 [`1986Sci...233...93S`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...93S); Connerney 1987 [`1987JGR....9215329C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215329C); Behannon 1987
  [`1987JGR....9215354B`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215354B).
- **Neptune**: Ness 1989 [`1989Sci...246.1473N`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1473N); Krimigis 1989 [`1989Sci...246.1483K`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1483K); Stone
  1989 [`1989Sci...246.1489S`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1489S); Connerney 1991 [`1991JGR....9619023C`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619023C); Paranicas 1991
  [`1991JGR....9619131P`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619131P).
- **Mercury**: Winslow 2013 [`2013JGRA..118.2213W`](https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W); Anderson 2011 [`2011Sci...333.1859A`](https://ui.adsabs.harvard.edu/abs/2011Sci...333.1859A);
  Schriver 2015 [`2015AGUFM.P53A2089S`](https://ui.adsabs.harvard.edu/abs/2015AGUFM.P53A2089S); Gershman 2015 [`2015JGRA..120.8559G`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.8559G); Korth 2015
  [`2015JGRA..120.4503K`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.4503K).
- **Ganymede**: Kivelson 2002 [`2002Icar..157..507K`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..507K); Kivelson 1998 [`1998JGR...10319963K`](https://ui.adsabs.harvard.edu/abs/1998JGR...10319963K);
  Kivelson 1996 [`1996Natur.384..537K`](https://ui.adsabs.harvard.edu/abs/1996Natur.384..537K); Pappalardo 1998 [`1998DPS....30.5401P`](https://ui.adsabs.harvard.edu/abs/1998DPS....30.5401P); Allioux 2013
  [`2013AdSpR..51.1204A`](https://ui.adsabs.harvard.edu/abs/2013AdSpR..51.1204A); Saur 2018 [`2018ASSL..448..153S`](https://ui.adsabs.harvard.edu/abs/2018ASSL..448..153S).

## Related

- [`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md)
  — 이 감사가 렌더하는 場 모양 레시피 + Kerbalism SDF 스키마.
- [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md) /
  [`rocky-planet-dynamo-methodology.md`](rocky-planet-dynamo-methodology.md) — B-field
  입력값.
- Wiki: [Radiation Belts](https://github.com/Vannadin/nearstars-db/wiki/Radiation-Belts)
  (단면 이미지).
- [methodology-index](methodology-index.md).
