<!-- 태양계 자기권 천체 7종의 실제 방사선대 물리 vs Kerbalism 스톡 cfg 비교 (ADS 근거, 위키 시각화 연동) -->
# 태양계 방사선대: 스톡 Kerbalism cfg vs 실제 물리

**포획 입자 벨트를 가진 자기권**(또는 그저 자기권을 가진) 태양계 천체를 하나씩 훑으며,
**Kerbalism / ROKerbalism 스톡 cfg**를 **ADS로 근거화한 실제 물리**와 대조하는 감사입니다.
NearStars의 자기권 지오메트리 레시피가 가상 천체용 벨트를 뽑아내기 전에 실제 바디로 먼저
보정하고, 스톡 모델이 러프한 자리채움에 그친 곳에는 물리 정확 cfg 값을 되먹이려고 존재합니다.

단면 시각화는 위키에 있습니다.
**[Radiation Belts](https://github.com/Vannadin/nearstars-db/wiki/Radiation-Belts)** —
바디마다 두 렌더 모두 인게임 `RadiationModel` SDF입니다. **스톡**은 출하 cfg(2026-07-24에
`KSP-RO/ROKerbalism`의 `System/Radiation.cfg` + `Support/RSS.cfg`로 검증), **물리**는 같은 SDF에서
여섯 개 벨트 모양 파라미터를 ADS로 앵커한 자기력선 사이의 실제 쌍극 drift-shell 영역
(r = L cos²λ, 대기 상단에서 loss-cone 컷)에 **수치적으로 적합**한 것입니다
(`scripts/viz/fit_belts.py`, Nelder-Mead 다중 시작). 적합 품질은 벨트별 IoU(단면 면적 겹침)로
명시합니다. **어디서나 ≥ 0.96**이고 목성의 납작한 magnetodisc만 예외입니다(0.87, 토러스 모델의
천장). 적합된 파라미터 세트는 렌더 드라이버에 들어 있습니다. 2-셸 토러스로는 실제 특징 일부
(위성/고리 간극, 시간 변동)를 여전히 못 담습니다(아래 명시). 렌더러는
`scripts/viz/render_belts.py`(+ `render_belts_bodies.py` 드라이버), SDF는
[`src/Kerbalism/Radiation/Radiation.cs`](https://github.com/Kerbalism/Kerbalism/blob/master/src/Kerbalism/Radiation/Radiation.cs)
재현(출처 [Kerbalism](https://github.com/Kerbalism/Kerbalism), [Unlicense](https://github.com/Kerbalism/Kerbalism/blob/master/LICENSE)·퍼블릭 도메인). 場 모양 스키마는
[`planetary-magnetosphere-geometry-methodology.md`](planetary-magnetosphere-geometry-methodology.md)
를 보세요.

## Scope — 자기화된 바디만

벨트가 생기려면 입자를 가둘 만큼 강한 고유 다이나모가 필요합니다. 태양계에서는 **7개 바디**
입니다. 지구, 목성, 토성, 천왕성, 해왕성(행성 다이나모), 수성(아주 작음), 그리고 가니메데
(임베디드 위성 다이나모)입니다. **금성, 화성, 달, Io, Europa, Callisto, Titan, Triton, 명왕성**
은 고유 전역장이 없어 → 벨트가 없고 → 표면 선량이 곧 직접 풍/GCR 플럭스입니다
(`radiation_surface`만, `RadiationModel` 벨트 없음). 여기서는 범위 밖입니다.

## cfg를 올바로 읽기 (함정 둘)

이 감사의 이전 개정본(그리고 손으로 배치한 "물리" 렌더)은 SDF 파라미터 둘을 오독했습니다.
둘 다 전체에 걸쳐 바로잡았고 기록해 둘 값이 있습니다.

1. **벨트의 `dist`/`radius`는 `deform_xy`로 눌린 좌표계에 있습니다.** SDF는
   `√((x²+z²)·deform_xy) − dist`를 검사하므로 벨트의 *적도* 범위는
   `(dist ± radius)/√deform_xy`이고, 여기에 border 토러스가 더 도려냅니다. 스톡 지구의 외대
   (2.6338/2.48, deform_xy 0.7225, border 1.4412/1.4875)는 실제로 **적도에서 3.45–6.0 R_E**에
   걸칩니다 — `outer_dist`를 순진하게 읽어 짐작하는 "2.6 R_E 중심"이 아니라, 물리적 외대 heart
   (L 3–7)에 가깝습니다.
2. **`pause_radius`는 sub-solar standoff가 아닙니다.** 주간측 x는 구 검사 전에
   `pause_compression`이 곱해지므로 코 = `pause_radius/pause_compression`, 옆구리 = `pause_radius`,
   꼬리 = `pause_radius/pause_extension`입니다. 스톡 지구(15, comp 1.5) → 코가 정확히
   **10 R_E** = Shue standoff이고, 옆구리/코 = 1.5 = 2^0.585(Shue α)입니다. 따라서
   Chapman–Ferraro standoff를 NearStars가 emit하려면 반드시 `pause_radius = R_mp × pause_compression`
   으로 설정해야 합니다.

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

핵심 발견. **(1)** 스톡 ROKerbalism의 **지구는 cfg를 올바로 읽으면 성격과 위치 둘 다 잘
보정되어 있습니다**(D컷 내대 1.3–2.0 R_E, 속 빈 외대 3.45–6.0, 자기권계면 코 10 R_E) — 이전
개정본은 위의 cfg 함정 둘 때문에 위치 어긋남을 주장했으나 철회합니다. **(2)** 진짜 스톡 오류는
**목성**(벨트가 ~3배 너무 바깥, D-cut 없음, magnetodisc 없음)과, 범용 `saturn` 모델의 튜닝
안 된 사본을 공유하는 **빙거성들**입니다(0–14 R에 걸치는 outer 7/7 덩어리, pause 20 — 바디별로
다른 건 tilt/offset뿐이고, 천왕성 `radiation_inner = 75`와 해왕성 `= 39`는 죽은 cfg입니다.
모델이 `has_inner = false`이기 때문입니다). **(3)** **토성의 "외대만, 내대 없음"** 스톡 선택은
*물리적으로 옳습니다* — 고리가 내대 자리를 차지하고 흡수해 버립니다 — 다만 그 7/7 덩어리는
여전히 쓸려나간 고리 영역을 넘쳐 채웁니다. **(4)** **벨트 강도의 출처**는 어디서나 도출값이
아니라 튜닝값입니다.

---

## 바디별: 스톡 cfg vs 물리

각 블록은 스톡 `RadiationBody`/`RadiationModel`(ROKerbalism `System/Radiation.cfg` + RSS
앵커), ADS 핀이 붙은 물리값, 그리고 그 차이(delta)를 제시합니다.

### Earth (캘리브레이션 앵커 — 그리고, 올바로 읽으면 좋은 앵커)
| Field | Stock (`earth`) | Physical | Source |
|---|---|---|---|
| pause | 15 / comp 1.5 → **코 10 R_E** | ~10 R_E sub-solar ✓ | Shue 1997 [`1997JGR...102.9497S`](https://ui.adsabs.harvard.edu/abs/1997JGR...102.9497S), Fairfield 1971 [`1971JGR....76.6700F`](https://ui.adsabs.harvard.edu/abs/1971JGR....76.6700F) |
| inner belt | 0.813/0.70 dxy 0.572, border 0.915 → 적도 **1.29–2.0 R_E** | 피크 **L≈1.5**, ~1.1–2 R_E, 하한 ~1000 km(그 아래는 loss-cone 고갈. SAA에선 dipole offset 때문에 ~200 km까지 내려옴) ✓ | (AP9; Ripoll 2016) |
| outer belt | 2.63/2.48 dxy 0.7225, border 도려냄 → 적도 **3.45–6.0 R_E** | **heart L≈4–5**, L 3–7 (≈; 가장자리 6 vs 7) | Reeves 2013 [`2013Sci...341..991R`](https://ui.adsabs.harvard.edu/abs/2013Sci...341..991R), Thorne 2013 [`2013Natur.504..411T`](https://ui.adsabs.harvard.edu/abs/2013Natur.504..411T) |
| slot region | 2.0–3.45 R_E 간극 ✓ | **L≈2–3** (hiss가 비움) | Ripoll 2016 [`2016GeoRL..43.5616R`](https://ui.adsabs.harvard.edu/abs/2016GeoRL..43.5616R) |
| radiation_inner/outer | 10.376 / 2.214 | 자릿수 일치 | — |
| geomagnetic_pole_lat / offset | 80.37 (tilt 9.6°) / 0.07 | tilt ~11° / ~0.08 R_E | IGRF (정확) |

올바른 SDF 의미로 읽으면 스톡 앵커는 **성격과 위치 둘 다 좋습니다**. D컷 내대 1.29–2.0 R_E,
슬롯, 속 빈 외대 3.45–6.0, 자기권계면 코가 정확히 10 R_E, 정확한 tilt/offset, 관측 양성자
피크와 맞는 내대 선량 ~10.4 rad/h. (이 문서의 이전 개정본은 pause가 1.5배 넉넉하고 외대가
2배 안쪽이라 주장했으나 — 둘 다 위의 cfg 읽기 함정이었고 철회합니다.) 물리 렌더는 정확한
L-shell을 재적합합니다(내대 L 1.1–2에 하한 ~1000 km, 외대 L 3–7. IoU 0.99/0.98). 스톡 대비 눈에 보이는
차이는 작습니다 — 외대 가장자리 7 vs 6 R_E, 그리고 살짝 더 두꺼운 내대 초승달입니다. 외대 혼(horn)의 저고도 컷(~300 km)은 그대로 둡니다 — 내대와 달리 외대 전자는 bounce/drift loss cone을 타고 저고도로 일상적으로 강수합니다(POES 관측. Liu 2024 [`2024JGRA..12932171L`](https://ui.adsabs.harvard.edu/abs/2024JGRA..12932171L)).

### Jupiter
| Field | Stock (RSS `jupiter`) | Physical | Source |
|---|---|---|---|
| inner belt | 6.0/1.0 (dxy 없음) → 적도 **5–7 R_J** | 쌍극형 셸 **L 1.2–3** (피크 ~1.5–2 R_J; 적합 IoU .98) | Divine & Garrett 1983 [`1983JGR....88.6889D`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.6889D) |
| inner border | (none) | 대기에서의 loss-cone D-cut | (belt physics) |
| outer belt | 6.5/6.5 (동심 블롭) | **자기원반 슬래브 3–16 R_J × ±3**(정준 반두께 ~3–3.5 R_J. 3–16은 50 R_J 너머까지 뻗는 원반의 프레임 절단)(피팅 IoU .87 — 토러스 한계) | Khurana 1989 [`1989JGR....9411791K`](https://ui.adsabs.harvard.edu/abs/1989JGR....9411791K) |
| pause | 60 / comp 1.05 → 코 57 | 코 **63** (compressed; 92 expanded) | Joy 2002 [`2002JGRA..107.1309J`](https://ui.adsabs.harvard.edu/abs/2002JGRA..107.1309J) |
| radiation_inner | 300 | **~1500** (order 10³–10⁴; conf low) | Divine & Garrett 1983 |
| geomagnetic_pole_lat | −81.4 | **−80** (tilt 10.3°, reversed) | Connerney 2022 JRM33 [`2022JGRE..12707055C`](https://ui.adsabs.harvard.edu/abs/2022JGRE..12707055C) |
| geomagnetic_offset | (none) | **0.1** (eccentric dipole) | JRM33 |

내대는 **쌍극형**(적도 + 비적도 전자, 피치각 0–90°. Santos-Costa 2001 [`2001P&SS...49..303S`](https://ui.adsabs.harvard.edu/abs/2001P%26SS...49..303S))
이라 → 납작하지 않고 둥급니다. 외대는 **경첩식 magnetodisc**(적도에 갇힌 전류 시트. Khurana
1989)라 → 납작합니다. Io/Amalthea/고리 흡수 gap(Santos-Costa 2001)은 두 셸로 표현할 수
없습니다 — 정밀도 천장입니다. 스톡은 강한 벨트를 ~3배 너무 바깥에 두고(6 vs ~2 R_J),
D-cut과 magnetodisc 평탄화를 둘 다 뺍니다.

### Saturn
| Field | Stock (`saturn` 모델, RSS.cfg) | Physical | Source |
|---|---|---|---|
| has_inner | false (outer only) | **false — correct** (rings absorb) | Cooper 1983 [`1983JGR....88.3945C`](https://ui.adsabs.harvard.edu/abs/1983JGR....88.3945C) |
| pause | 20 / comp 1.02 → 코 19.6 | 코 **~24** (22–27 bimodal) | Achilleos 2008 [`2008JGRA..11311209A`](https://ui.adsabs.harvard.edu/abs/2008JGRA..11311209A) |
| outer belt | 7/7 → 적도 **0–14 R_S** (쓸려나간 고리 영역을 넘쳐 채움) | 셸 **L 2.3–6** (적합 IoU .98), 위성이 잘라낸 통로 | Kollmann 2013 [`2013Icar..222..323K`](https://ui.adsabs.harvard.edu/abs/2013Icar..222..323K) |
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
| Field | Stock (범용 `saturn` 모델, RSS.cfg) | Physical | Source |
|---|---|---|---|
| geomagnetic tilt | pole_lat 31.4 (=58.6°) | **59–60°** ✓ | Ness 1986 [`1986Sci...233...85N`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...85N) |
| geomagnetic_offset | 0.3 | **0.3 R_U** ✓ | Ness 1986 |
| pause | 20 / comp 1.02 → 코 19.6 | 코 **18.0 R_U** (bow shock 23.7) | Ness 1986 |
| belts | generic `saturn` 외대 7/7 블롭(0–14 R_U). **radiation_inner 75는 죽은 cfg**(`has_inner = false`) | 위성 스위핑이 경계 짓는 두 셸 **L 1.5–5 / L 5–10** — Miranda L 5.1("Miranda 궤도 안쪽 예외역"), 전자 극소가 Miranda/Ariel/Umbriel L 5.1/7.5/10.4에, 그 사이 넓은 극대. 포획은 Titania ~L 17까지 검출(피팅 IoU .98/.97) | Krimigis 1986, Cheng 1987 [`1987JGR....9215315C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215315C) |
| radiation_inner | 75 (미사용) | e⁻ ≥1.2 MeV, p ≥4 MeV | Krimigis 1986 [`1986Sci...233...97K`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...97K) |
| quadrupole | — | large (Q3 model) | Connerney 1987 [`1987JGR....9215329C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215329C) |

**스톡은 극단적인 offset-기운 쌍극축을 잡아냅니다**(pole_lat 31.4, offset 0.3). 하지만 場의
*모양*은 범용 `saturn` 모델의 튜닝 안 된 사본(단일 7/7 외대 덩어리, pause 20)이고 해왕성과
그대로 공유됩니다 — 게다가 모델에 내대가 없으므로 그 `radiation_inner = 75`는 결코 발동하지
않습니다. 벨트 강도는 튜닝된 자리채움입니다. 위성들(Miranda→Titania)이 17.24 h마다 거대한
L-범위에 걸쳐 벨트를 쓸어냅니다(Stone 1986 [`1986Sci...233...93S`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...93S)). 태양 쪽을 거의
가리키는 자전축이 꼬리를 나선으로 감아올립니다(pitch 5.5°. Behannon 1987
[`1987JGR....9215354B`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215354B)). 극성 부호는 1차 초록에서 언급되지 않았습니다(지어내지 않음).

### Neptune
| Field | Stock (범용 `saturn` 모델, RSS.cfg) | Physical | Source |
|---|---|---|---|
| geomagnetic tilt | pole_lat 43 (=47°) | **47°** ✓ | Ness 1989 [`1989Sci...246.1473N`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1473N) |
| geomagnetic_offset | 0.55 | **0.55 R_N** ✓ | Ness 1989 |
| pause | 20 / comp 1.02 → 코 19.6 (이전 개정본은 26.5 ✓라 했으나 — 틀렸고, 모델은 공유된 `saturn` 것임) | 코 **26.5 R_N** (bow shock 34.9) | Ness 1989 |
| belts | 범용 outer 7/7 덩어리; **radiation_inner 39는 죽은 cfg** (`has_inner = false`) | 셸 **L 1.5–5 / L 5–14** (적합 IoU .98/.97), 피크 **L ≈ 7** | Stone 1989 [`1989Sci...246.1489S`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1489S) |
| outer cutoff | — | **~14 R_N (Triton)** | Krimigis 1989 [`1989Sci...246.1483K`](https://ui.adsabs.harvard.edu/abs/1989Sci...246.1483K) |
| quadrupole/octupole | — | quad ≈ dipole at surface | Connerney 1991 [`1991JGR....9619023C`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619023C) |

천왕성처럼 **스톡이 offset-기운 쌍극축을 잡아냅니다**(tilt 47°, offset 0.55) — 공유된 범용
場 모양 위에 얹은 것입니다. 벨트는 L≈7(Proteus 4.75 R_N 바로 바깥)에서 피크를 찍고, 고리/위성
흡수로 도려집니다(Paranicas 1991 [`1991JGR....9619131P`](https://ui.adsabs.harvard.edu/abs/1991JGR....9619131P)). 바깥은 Triton 궤도에서 딱
잘립니다. 행성 근처의 場은 강하게 비쌍극적입니다(사극/팔극이 쌍극에 맞먹음).

### Mercury
| Field | Stock (ROKerbalism `mercury`) | Physical | Source |
|---|---|---|---|
| pause | 1.6 / comp 1.4 → 코 **1.14** | 코 **1.45 R_M** (1.35–1.55, → 1.28 in storms) | Winslow 2013 [`2013JGRA..118.2213W`](https://ui.adsabs.harvard.edu/abs/2013JGRA..118.2213W) |
| belts | none | **none** ✓ (too small/dynamic) | Schriver 2015 [`2015AGUFM.P53A2089S`](https://ui.adsabs.harvard.edu/abs/2015AGUFM.P53A2089S) |
| geomagnetic_offset | 0.208 | **0.198** (484 km north) | Anderson 2011 [`2011Sci...333.1859A`](https://ui.adsabs.harvard.edu/abs/2011Sci...333.1859A) |
| tilt | (small) | **<3°** (<0.8° refined) | Anderson 2011/2012 |
| moment | — | 190–195 nT·R_M³, southward | Anderson 2011, Korth 2015 [`2015JGRA..120.4503K`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.4503K) |

**스톡이 벨트 없음으로 옳게 모델링합니다** — 수성 자기권은 안정 개체를 가두기엔 너무 작고
동적입니다(준포획된 1–10 keV 적도 구름 + 일시적 버스트만 있음). 북향 offset(484 km ≈ 0.2 R_M)
이 표면 선량을 **남**반구/커스프에 몰아넣습니다. SEP 전자는 열린 자기력선을 타고 거의 즉시
표면에 닿습니다(Gershman 2015 [`2015JGRA..120.8559G`](https://ui.adsabs.harvard.edu/abs/2015JGRA..120.8559G)). 스톡의 코(1.6/1.4 = 1.14 R_M)는
물리값 1.45보다 살짝 *빡빡합니다* — 이전 개정본(pause_radius를 standoff로 읽은)이 말한 것처럼
넉넉한 게 아닙니다.

### Ganymede
| Field | Stock (ROKerbalism `ganymede`) | Physical | Source |
|---|---|---|---|
| surface dipole | (implicit) | **719 nT eq** (tilt 176°) | Kivelson 2002 [`2002Icar..157..507K`](https://ui.adsabs.harvard.edu/abs/2002Icar..157..507K) |
| has_pause | (none) | **~2 R_G upstream** (5.5 across) | Kivelson 1998 [`1998JGR...10319963K`](https://ui.adsabs.harvard.edu/abs/1998JGR...10319963K) |
| inner belt | 0.8/0.6, rad 0.33 | 단일 약벨트 **L 1.1–1.9**, 표면 자체에서 흡수(무대기 — 고도 컷 없음)(피팅 IoU .97), 소스 부족 | Allioux 2013 [`2013AdSpR..51.1204A`](https://ui.adsabs.harvard.edu/abs/2013AdSpR..51.1204A) |
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
- **납작한 magnetodisc의 날카로운 방사상 가장자리** — 최선의 토러스 적합은 렌즈입니다(목성
  외대 IoU 0.87 vs 모든 쌍극형 셸 ≥0.96). 실제 disc는 가장자리가 점점 얇아지므로, 렌즈가
  오히려 판(slab) 타깃 자체보다 자연에 더 가깝다고 볼 수도 있습니다.
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
- **Uranus**: Ness 1986 [`1986Sci...233...85N`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...85N); Krimigis 1986 [`1986Sci...233...97K`](https://ui.adsabs.harvard.edu/abs/1986Sci...233...97K); Cheng 1987 [`1987JGR....9215315C`](https://ui.adsabs.harvard.edu/abs/1987JGR....9215315C); Stone
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
- `scripts/viz/fit_belts.py` — 수치 적합기(쌍극-셸 타깃 → SDF 파라미터, IoU 채점).
  적합된 파라미터 세트는 `render_belts_bodies.py`에 들어 있습니다.
- [`planetary-dynamo-scaling.md`](planetary-dynamo-scaling.md) /
  [`rocky-planet-dynamo-methodology.md`](rocky-planet-dynamo-methodology.md) — B-field
  입력값.
- Wiki: [Radiation Belts](https://github.com/Vannadin/nearstars-db/wiki/Radiation-Belts)
  (단면 이미지).
- [methodology-index](methodology-index.md).
