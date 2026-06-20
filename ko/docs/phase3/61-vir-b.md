<!-- 61 Vir b Phase 3 합성. cfg-ready 결정과 근거 -->
# 61 Vir b — Phase 3 Synthesis

61 Vir b 는 G6.5V 솔라 트윈 61 Virginis 주위에서 RV 로 검출된 세 행성
중 가장 안쪽에 있으며, Vogt et al. 2010 (HIRES + AAT 결합 해) 가 보고
했습니다. 검출은 RV 전용이고 트랜짓이 없으므로, 직접 측정된 양은 궤도
주기 P = 4.215 ± 0.0006 일, 장반경 a = 0.0502 AU, 이심률 e = 0.12,
근일점 인수 ω = 105°, 최소 질량 Msini = 5.1 ± 0.5 M⊕ 로 한정됩니다.
진질량은 5.1 M⊕ 이상이고, 시스템의 거의 edge-on 경사 posterior 에서
가장 그럴듯한 범위는 5–7 M⊕ 입니다. 반지름은 측정된 바 없습니다.
반사광 직접 영상은 미래 등급의 관측 (HabEx / LUVOIR 시대) 이기 때문에,
현재 상태의 대기는 제약되지 않습니다.

**NearStars 시나리오 선택. 조석 고정된 뜨거운 슈퍼지구로, 마그마-바다
주광면, 식은 야간면, 잔여 규산염 증기 외기권, 가시 Rayleigh 대기 부재
입니다.** 이는 b 의 약간 더 차가운 일조량 (S ≈ 326 S⊕, T_eq(A=0) ≈
1180 K, T_eq(A=0.3) ≈ 1080 K) 에 적용된 CoRoT-7b / 55 Cnc e 우주화학
원형입니다. 대안 — 보유된 증기-CO₂ runaway-Venus 대기 — 는 Open items
의 cfg variant 로 보존합니다. 326 S⊕ 에서의 b 의 탈출 예산이 무대기
해석을 단정적으로 강제하지는 않기 때문입니다.

## Decisions

Kopernicus / atmosphere cfg-ready 값입니다. `Confidence`. high = 직접
측정되었거나 강하게 제약됨, medium = 강한 근거를 갖춘 이론, low =
허용 범위 내의 미적 선택.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 0.050 AU 의 4.215 일 궤도. 조석 고정 시간 ~10⁵–10⁶ 년 (표준 평형-조석 추정, Hut 1981) 이 6 Gyr 시스템 나이보다 한참 짧음 |
| `obliquity_deg` | 0 | high | 조석 감쇠 |
| `eccentricity` | 0.12 | high | Vogt 2010 RV fit |
| `argument_of_periastron_deg` | 105 | high | Vogt 2010 |
| `sidereal_period_days` | 4.215 | high | Vogt 2010 |
| `semi_major_axis_au` | 0.0502 | high | Vogt 2010 |
| `mass_mearth` | 5.1 | high | Vogt 2010 Msini. 하한값에 불과 (RV-only) |
| `radius_rearth` | 1.65 | medium | Tie-break. 트랜짓 없음. Zeng 2016 의 5–7 M⊕ 지구 조성 암석 핵 mass-radius 스케일링은 R ≈ 1.5–1.8 R⊕. cfg 는 지구 조성 중간값 1.65 R⊕ 채택 |
| `surface_gravity_g_earth` | 1.87 | medium | 유도 = 5.1 / 1.65² (지구 조성 핵) |
| `density_g_cc` | 6.27 | medium | 유도. 지구형 암석-철 조합과 일관 |
| `insolation_s_earth` | 326 | high | L = 0.82 L☉ 와 a = 0.0502 AU 에서 유도 |
| `equilibrium_temp_k` (A=0) | 1180 | high | 유도 |
| `equilibrium_temp_k` (A=0.3) | 1080 | high | 유도 |
| `bond_albedo` | 0.1 | medium | Tie-break. 뜨거운 어두운 규산염 / 부분 용융 표면에서 0.05–0.2 범위. cfg 는 0.1 채택 (CoRoT-7b / 55 Cnc e 아날로그) |
| `dayside_surface_temp_k` | 1450 | medium | Tie-break. 무대기 극한 (재분배 없음) 에서 substellar T_substellar = T_eq × √2 × (1−A)^0.25 ≈ 1450 K. Léger 2009 CoRoT-7b 템플릿과 일치. 규산염 solidus (basalt 의 ~1500 K, 1300+ K 에서 부분 용융) 위 |
| `nightside_surface_temp_k` | 200 | medium | Tie-break. 부분 용융 dayside 에 열관성을 가진 무대기 cold-trap. cfg 는 200 K 채택. b 의 야간이 4.2 일로 길기 때문에 수성 야간 ~100 K 보다 차가움 |
| `atmosphere_present` | false (잔여 규산염 증기만) | medium | Tie-break. 일차 H/He 외피는 오래전 광증발 (G 왜성 0.05 AU 의 5 M⊕ 에 대한 Owen & Wu 2017 valley 물리. ≲ 50 Myr 손실). 이차 증기 대기는 ~10⁹ g/s XUV 손실율을 초과하는 지속적 outgassing 이 필요하나 보장되지 않음. cfg 는 수성 아날로그 광물 증기 외기권을 가진 무대기 채택 |
| `atmosphere_surface_pressure_pa` | 10⁻⁷ | medium | Tie-break. substellar 맨틀 / 마그마 승화로부터의 규산염 증기 외기권. 컬럼 밀도 ~10¹² atoms/cm² → 표면 환산 압력 ~10⁻⁷ Pa (Schaefer & Fegley 2009 뜨거운 암석 outgassing 스케일링) |
| `atmosphere_composition` | Na, K, SiO, O₂ 규산염 증기 외기권 (스퍼터 + 열) | low | Tie-break. 뜨거운 암석 outgassing 화학 (CoRoT-7b 등급에 대한 Schaefer & Fegley 2009). 증기압상 Na/K 우세, SiO/O₂ 차순위 |
| `atmosphere_scale_height_km` | n/a | high | 외기권. 정수압 대기 없음 |
| `atmosphere_tint_rgb_hex` | n/a (가시 대기 없음) | high | 외기권 컬럼이 가시 산란/흡수에 비해 너무 낮음 |
| `cloud_cover_fraction` | 0 | high | 대기 없음 |
| `cloud_morphology` | n/a | high | 대기 없음 |
| `cloud_tint_rgb_hex` | n/a | high | 대기 없음 |
| `ocean_present` | false | high | T_dayside > 1400 K 가 표면 물을 배제. 야간면은 너무 차갑지만 휘발성 운반을 위한 대기 수송 없음 |
| `surface_tint_rgb_hex_primary` | `#3a2a22` (어두운 부분 용융 basalt 지각) | medium | Tie-break. G 왜성 조명 아래 dayside 마그마 + 식은 basalt 평원. CoRoT-7b / 55 Cnc e 기대와 일관된 어두운 갈색-검정 톤 채택 |
| `surface_tint_rgb_hex_accent` | `#c84a18` (substellar 마그마-바다 glow) | low | Tie-break. ~1450 K 의 substellar 부분 용융 영역이 적-주황으로 복사 (Wien 피크 2 μm 이지만 가시광 꼬리 두드러짐). interesting-first 가 균일한 어두운 표면 대신 가시 lava-glow accent 채택 |
| `surface_morphology` | substellar 마그마 바다 ~1500 km 반경. 중위도 식은 basalt 평원. 휘발성 제거된 야간 regolith | medium | Tie-break. Léger 2009 CoRoT-7b 마그마-바다 템플릿. 규산염 solidus 의 substellar isotherm 에서 ~30° 마그마-pond 반경 |
| `tidal_heating_w_m2` | 0.1–1 | medium | 4.2 일 주기에서 e=0.12 에 대한 Bolmont 2020 스케일링. 이심률 기여는 이 질량에서 적당하지만 자명하지 않음. 일사 예산을 보충하지만 지배하지는 않음 |
| `radiogenic_heat_w_m2` | 0.05 | low | 지구형 BSE(bulk-silicate-Earth) 방사성 열류속(현재값 ~0.04 W/m²)을 ~5 M⊕로 질량 스케일했으며 부분 용융 내부와 일관됨. 방법은 Wang et al. 2020 (`2020A&A...644A..19W`)의 외계행성 방사성 열 프레임워크를 따름. 다만 Eu→Th/U 호스트 원소비 보정은 호스트별 원소비를 큐레이션하지 않아 적용하지 않았고, 대신 지구형 원소비를 가정함 |
| `star_apparent_angular_diameter_deg` | 1.02 | high | 유도. 2 × R★ / a × (180/π). 0.0502 AU 의 0.963 R☉ |
| `stellar_illumination_color_temp_k` | 5552 | high | 호스트 Teff |

## Surface synthesis

61 Vir b 는 솔라 트윈 호스트 주위의 RV-only 안쪽 행성 슈퍼지구 원형
입니다. 관측적 anchor 세 가지가 합성을 고정합니다.

1. **일조량 326 S⊕** 는 표준적인 "용암 세계" 영역입니다. Léger 2009 가
   CoRoT-7b (4.8 M⊕, S ≈ 2500 S⊕, T_eq ≈ 1810 K) 로 이 영역을 도입하고
   55 Cnc e (8 M⊕, S ≈ 2400 S⊕, T_eq ≈ 2000 K) 가 확장했습니다. b 는
   T_eq ≈ 1180 K 로 용암-세계 가족의 차가운 끝쪽에 위치합니다. 이 온도
   에서 basalt 표면은 본체는 고체이고 substellar 반구에서만 부분 용융
   이며, dayside 전체가 완전 용융하지는 않습니다.

2. **트랜짓 없음, JWST follow-up 없음.** 행성의 진질량과 반지름은
   제약되지 않습니다. 미래의 천체측정 경사각이나 직접 영상 캠페인
   없이는 b 가 트랜짓 특성화되지 않습니다. cfg 는 지구 조성 암석 핵에
   대한 Zeng 2016 mass-radius 스케일링을 채택. Msini = 5.1 M⊕ 에서
   R ≈ 1.65 R⊕, 표면중력 1.87 g⊕, 벌크 밀도 6.27 g/cc.

3. **우주화학적 맥락.** 61 Vir 의 [Fe/H] ≈ 0.0 dex (Pavlenko 2012) 와
   ~6 Gyr 나이는 b 에 지구 아날로그 초기 휘발성 inventory 를 주지만,
   대기 손실 이력은 훨씬 가혹합니다. Owen & Wu 2017 의 광증발 valley
   물리는 b 를 "코어만" 영역에 단단히 위치시킵니다. G 왜성 0.05 AU 의
   5 M⊕ 코어 위 초기 H/He 외피는 ≲ 50 Myr 시간 안에 손실되는데, 6 Gyr
   시스템 나이보다 한참 짧습니다. 이차 대기 보유는 outgassing 과
   XUV 손실의 균형에 달려 있는데, b 의 파라미터에서는 그 균형이 위태로
   운 경계입니다.

cfg 는 **부분 용융 substellar 마그마-바다** 시나리오를 채택합니다.
substellar 점 주위 ~30° 안의 substellar 반구가 표면 온도가 규산염
solidus (tholeiitic basalt 의 T ≈ 1500 K, 휘발성 풍부 용융의 경우 더
낮음) 를 초과하는 얕은 마그마-바다 구조를 호스트합니다. 이는 완전
고화된 "더 강한 일조량을 받는 수성" 해석에 대한 tie-break 선택입니다.
interesting-first 가 마그마 바다를 선택한 이유는 그것이 시스템의 다른
어디에도 없는 시각적으로 두드러진 feature 를 b 에게 주기 때문입니다.

**색 선택.** 솔라 트윈 조명 (Teff 5552 K, 거의 태양 SED) 아래에서
표면 색조는 사실상 지구에서 보이는 그대로 인식됩니다. 의미 있는 M
왜성 적색 변위 보정이 필요 없습니다. primary 표면 색조 `#3a2a22` 는
어두운 부분 용융 basalt 지각 톤으로, 신선한 ultramafic 검정 (~`#1a1612`)
과 풍화된 수성 regolith (~`#5a4a3a`) 사이입니다. accent `#c84a18` 는
substellar 마그마-바다 glow 를 가시 적-주황 patch 로 인코딩합니다.
1450 K 열복사의 Wien 피크는 λ ≈ 2 μm (근적외) 에 있지만 가시 꼬리는
차가운 중위도 지각 대비 충분히 밝게 인식됩니다.

**조석 고정 하의 형태.** substellar 마그마 pond 는 천천히 librate 하는
substellar feature 입니다 (e = 0.12 libration). 내부 가열이 아닌 항성 일사로 유지되는
마그마 pond 내 대류 열흐름이 부분 규산염 증기 outgassing 을 외기권
으로 구동합니다. 중위도는 지각화된 basalt 평원이고, 야간면은 시스템의
6 Gyr 에 걸쳐 차갑고 어두우며 휘발성이 제거된 상태입니다. 수성
아날로그 충돌 크레이터화된 regolith 가 antistellar 반구를 덮습니다.
dayside 에서 신선한 휘발성을 운반해 줄 대기 수송이 없으므로 검출
가능한 휘발성 cold-trap 도 없습니다.

## Atmosphere synthesis

b 에 대한 대기 추론은 완전히 이론적입니다. JWST 트랜짓이나 식 측정이
없고, 행성은 현 세대 직접 영상에 대비비로 너무 어둡습니다. cfg 는
**가시 Rayleigh 대기 없는 잔여 규산염 증기 외기권** 을 채택합니다 —
진행 중인 마그마-pond outgassing 으로 수정된 무대기 해석입니다.

**압력 선택.** 표면 압력 10⁻⁷ Pa 는 substellar 마그마 승화로 생성된
규산염 증기 외기권의 컬럼-밀도 등가 표현입니다 (뜨거운 암석 행성에
대한 Schaefer & Fegley 2009 스케일링). 어떤 Rayleigh 산란 임계값보다도
한참 아래라 가시 limb haze 가 생기지 않습니다. 완전한 정수압 대기는
부재합니다 — 컬럼 밀도 ~10¹² atoms/cm² 는 수성 외기권 몇 개에 해당
하는 질량으로, 마그마 pond 가 활성으로 규산염을 승화시키는 substellar
반구 쪽으로 편향됩니다.

**조성.** Schaefer & Fegley 2009 는 1400–1500 K 의 부분 용융 규산염
마그마 바다 위 dominant outgassing 종으로 Na, K, SiO, O₂, Fe-증기를
제시합니다. 이 온도에서 증기압상 Na 와 K 가 우세하고, SiO 와 O₂ 가
차순위이며, Fe-증기는 외기권 고도에 도달하기 전에 응결합니다. cfg
는 조성 문자열로 "Na, K, SiO, O₂ 규산염-증기" 를 인코딩합니다 —
용암-세계 영역에 대한 표준 Léger 2009 / Schaefer & Fegley 2009 조성
입니다.

XUV 손실 예산은 b 의 파라미터에서 ~10⁹ g/s 로 작동합니다 (Owen & Wu
2017 스케일링. ~10⁻⁵ M⊕/Gyr). 마그마 pond 에서의 지속적 outgassing
이 외기권을 정상상태 컬럼 밀도로 유지시킵니다. 손실율이 어떤 그럴
듯한 맨틀 조성에 대해서도 outgassing 율을 초과하므로 의미 있는 이차
대기 축적은 없습니다. 행성은 축적이 아닌 **탈출** 상태입니다.

**표면에서 본 하늘 외관.** 대기가 없으니 Rayleigh 산란도 없습니다 —
모든 고도에서 하늘은 검습니다. 61 Vir 는 각지름 1.02° 로 dayside
하늘을 지배하며 (지구에서 본 태양 겉보기 크기의 ~2 배), 태양빛
디스크는 흐림이나 산란 없이 또렷합니다. substellar 점의 표면 밝기는
~326× 지구 정오 등가입니다. 별의 스펙트럼은 본질적으로 태양형 —
b 의 dayside 에 서 있는 플레이어는 지구에서 본 태양보다 훨씬 크고
밝은 노란 디스크를 보며, 부분 용융 지형 위로 또렷한 그림자가
드리워집니다.

**야간면.** 대기 수송이 없으므로 야간면은 진정 어둡고, 합 시 자매
행성의 반사광 (c 가 가장 두드러지고, d 는 더 멀리) 과 먼 별빛으로만
조명됩니다. ~200 K 의 야간 표면 온도와 승화 가능한 휘발성의 부재는
antistellar 반구를 수성 야간면의 더 어두운 아날로그로 만듭니다.

## Rotation & spin synthesis

0.94 M☉ 호스트 주위 0.050 AU 의 4.215 일 궤도 주기는 조석 고정 시간
~10⁵–10⁶ 년 (표준 평형-조석 추정, Hut 1981)
을 주는데, 6 Gyr 시스템 나이보다 4–5 자릿수 더 짧습니다.
1:1 spin-orbit 공명이 완전히 자리잡혀 있습니다. 황도경사각은 같은
시간 스케일에 걸쳐 0 까지 감쇠했습니다.

**고차 공명.** 이심률 0.12 (Vogt 2010 fit) 에서 spin-orbit 안정성
분석은 1:1 의 대안으로 3:2 공명 trap 을 허용합니다.
e = 0.205 의 수성 3:2 lock 과의 유추입니다. 경계는 이 궤도 주기에서
b 의 질량의 암석 행성에 대해 e ≈ 0.1–0.15 입니다. b 는 그 경계 **위**
에 앉아 있습니다. cfg 는 canonical 선택으로 1:1 을 채택 (행성 사슬
에서의 느린 이심률 감쇠의 가장 그럴듯한 결과) 하고 3:2 대안은 Open
items 에서 cfg variant 로 명시합니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 4.215 일 (364 176 초).
Kopernicus `rotationPeriod` 는 궤도 `period` 와 초 단위로 일치해야
합니다.

**계절 없음.** obliquity 가 0 까지 감쇠. 이심률 기반 일조량 변동
(e=0.12) 은 궤도에 걸쳐 S = (1 ± e)⁻² × 326 = 263 → 416 S⊕ 의 peri-to-apo
S 범위를 주지만, substellar 점이 고정되어 있어 그 변동은 계절 날씨가
아닌 마그마 pond 의 깊이와 outgassing 율의 변조로 나타납니다. cfg 의
정적 마그마-pond 렌더링은 시간-평균 시나리오입니다. 주기적 outgassing
burst 가 있는 변형 렌더링은 Phase 3.5 시각 디테일 레이어에서 추가할
수 있습니다.

**조석 가열.** 4.2 일 주기에서 e=0.12 에 대한 Bolmont 2020 스케일링은
지구 아날로그 내부 rheology 에서 0.1–1 W/m² 의 조석 가열 기여를
줍니다. 326 S⊕ 일조 flux (substellar 흡수 ~4.4 × 10⁵ W/m²) 에 비해
적당하지만, 지구의 ~0.1 W/m² 내부 열흐름에 비해서는 무시할 수 없습
니다. 따라서 substellar 마그마 pond 는 **일사 구동이지 조석 구동이
아니며**, Io 의 조석-열-지배 화산활동과는 다릅니다.

## Visual styling

궤도와 표면 렌더러를 위해 표면과 대기 결정을 결합하면 다음과 같습니다.

- **전역 외관 (궤도 뷰).** substellar 점에서 빛나는 적-주황 spot 과
  어두운 거의 균일한 중위도 basalt 평원을 가진 어두운 본체의 슈퍼
  지구로, 검은 야간면으로 페이드 아웃됩니다. substellar 마그마-바다
  glow 는 61 Vir 안쪽 시스템 전체에서 가장 시각적으로 두드러진 feature
  입니다.
- **substellar 마그마 바다.** substellar 점을 중심으로 하는 ~30° 반경
  의 디스크. 표면 색조 `#c84a18` (lava 적-주황) 과 λ ≳ 1 μm 의 열복사
  glow 가 IR cfg 에서 추가 밝기를 기여합니다. pond 는 영구적 (일사
  구동) 이지만 그 깊이는 이심률 궤도에 따라 살짝 변조됩니다.
- **중위도 basalt 지각.** 색조 `#3a2a22` (어두운 갈색-검정 부분 용융
  basalt). 6 Gyr 의 폭격에서 누적된 드문 충돌 크레이터, 높은 e
  excursion 동안의 과거 마그마-pond 확장으로 일부 리서피스됨. 매끈한
  lava 평원이 주를 이룹니다.
- **야간면.** 차갑고 (~200 K) 어두움. 표면 색조는 중위도와 같지만
  조명이 없습니다. 자매 행성 반사광으로만 보입니다. 휘발성이 제거된
  수성 아날로그 regolith.
- **Terminator 밴드.** 대기 산란이 없어 또렷합니다. 지형 feature 가
  스치는 태양빛 노란빛 아래로 긴 그림자를 드리웁니다.
- **대기 haze.** 가시광에서 없음. 규산염-증기 외기권은 ~10⁻⁷ Pa 로
  Rayleigh 임계값 한참 아래입니다. limb 는 디스크에서 우주로의 깨끗한
  가장자리.
- **하늘의 별.** 61 Vir 가 b 에서 1.02° 차지 — 지구에서 본 태양 각
  크기의 약 2 배. 색은 본질적으로 태양빛 노란 (Teff 5552 K → `#fff2dc`
  cfg-인코딩 색조). 326× 지구 정오 밝기에서 표면은 뜨거운 수성 dayside
  처럼 조명됩니다.
- **하늘의 자매 행성.** c (다음 외측 0.22 AU) 가 b 의 시점에서 내합 시
  각 크기 ~0.05° (회합 주기 ~5 일 마다). d (0.48 AU) 는 훨씬 작고 항상
  보이지는 않습니다.
- **선택적 마그마-pond 애니메이션.** 마그마-pond accent 색조의 미묘한
  열 펄세이션 (이심률 사이클에 걸쳐 `#c84a18` 에서 더 밝은 `#e85a28`
  으로 변조) 이 일사 구동 열흐름 변조를 충실하게 렌더링해 줍니다. 우선
  순위 낮은 시각 이스터에그.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Vogt S. S. et al. 2010** — *A Super-Earth and Two Neptunes
  Orbiting the Nearby Sun-Like Star 61 Virginis*, ApJ 708, 1366
  (`2010ApJ...708.1366V`). 발견 논문. b 의 궤도 (P=4.215 d,
  a=0.0502 AU, e=0.12, ω=105°) 와 최소 질량 (Msini = 5.1 ± 0.5 M⊕)
  보고. HIRES + AAT 결합 RV 해. Decisions 표의 모든 궤도 + 질량 값이
  여기에 묶입니다.
- **Léger A. et al. 2009** — *Transiting exoplanets from the CoRoT
  space mission VIII. CoRoT-7b: the first super-Earth with measured
  radius*, A&A 506, 287 (`2009A&A...506..287L`, arXiv:0908.0241).
  용암-세계 템플릿. 뜨거운 암석 슈퍼지구에 대한 마그마-바다 dayside
  시나리오를 확립. b 는 약간 더 차가운 아날로그. 표면 형태 + 마그마-
  pond 시각 결정을 견인.
- **Schaefer L. & Fegley B. 2009** — *Chemistry of silicate
  atmospheres of evaporating super-Earths*, ApJ 703, L113
  (`2009ApJ...703L.113S`, arXiv:0905.4045). 뜨거운 암석 표면의
  outgassing 화학. `atmosphere_composition` 선택을 견인 (1400–1500 K
  substellar 에서 Na, K, SiO, O₂ 규산염 증기 우세).
- **Zeng L. et al. 2016** — *Mass-radius relation for rocky planets*,
  ApJ 819, 127 (`2016ApJ...819..127Z`, arXiv:1512.08827). 지구 조성
  암석 행성의 mass-radius 스케일링. 5.1 M⊕ 에서 R ≈ 1.65 R⊕. `radius_rearth`
  tie-break 을 견인.
- **Owen J. E. & Wu Y. 2017** — *The evaporation valley in the
  Kepler planets*, ApJ 847, 29 (`2017ApJ...847...29O`,
  arXiv:1705.10810). 광증발-valley 물리. b 를 단단히 "코어만" 영역에
  위치시킴 — 초기 H/He 외피는 ≲ 50 Myr 에 손실. `atmosphere_present =
  false` 선택을 견인.
- **Hut P. 1981** — *Tidal evolution in close binary systems*, A&A
  99, 126 (`1981A&A....99..126H`). 표준 평형-조석 모델. b 의 파라미터
  에서의 조석 고정 시간 추정 (~10⁵–10⁶ 년) 이 여기서 따라옵니다.
  `tidally_locked = true` 선택의 anchor.
- **Bolmont E. et al. 2020** — *Tidal dissipation and obliquity
  evolution of TRAPPIST-1 planets* (`2020A&A...644A.165B`). 암석
  외계행성의 조석 가열 스케일링. e=0.12, P=4.2 d 에서 0.1–1 W/m²
  추정값 제공.

### Read (context / methodology, not decision-driving)

- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age
  Estimation for Solar-Type Dwarfs Using Activity-Rotation
  Diagnostics*, ApJ 687, 1264 (`2008ApJ...687.1264M`, arXiv:0807.1686).
  호스트 합성에서 상속. 61 Vir 나이 6.1 ± 1.7 Gyr. 대기 손실의 시스템
  진화 시간 스케일을 결정.
- **Pavlenko Y. V. et al. 2012** — *Effective temperatures, gravities,
  metallicities, and ages of 18 solar twin candidates*
  (`2012MNRAS.422..542P`, arXiv:1112.0590). 호스트 합성에서 상속. 61
  Vir 솔라 트윈 풍부도 패턴 확인.
- **Wyatt M. C. et al. 2012** — *Herschel imaging of 61 Vir*, MNRAS
  424, 1206 (`2012MNRAS.424.1206W`, arXiv:1204.6063). 호스트 합성에서
  상속. ~30 AU 의 차가운 debris 띠가 b 의 분리에서 안쪽 행성과 동역학
  적으로 상호작용하지 않으므로 간략히 인용.
- **Lopez E. D. & Fortney J. J. 2014** — *Understanding the
  mass-radius relation for sub-Neptunes*, ApJ 792, 1
  (`2014ApJ...792....1L`, arXiv:1311.0329). sub-Neptune envelope
  mass-radius 스케일링. b 의 잠재적 광증발되지 않은 H/He 외피에 대한
  경계를 정보화 (논의된 대로 배제).
- **Howe A. R. et al. 2014** — *Mass-radius relations and core-envelope
  decompositions of super-Earths and sub-Neptunes*, ApJ 787, 173
  (`2014ApJ...787..173H`). envelope-vs-rocky 결정의
  맥락에서 간략히 사용. b 는 암석.

### Read (instrument-only, not visual-informative)

- **Marcy G. W. et al. 2014** — Kepler 슈퍼지구 통계. b 는 Kepler
  샘플이 아니지만 후속 연구의 보정 anchor 로 사용.

### Not read — no arXiv preprint or low-priority (~10 papers)

b 특정 arXiv 기록은 작습니다 (행성은 2010 년 발견되었고 트랜짓이나
대기 특성화 follow-up 이 없습니다). 읽지 않은 집합은 주로 다음과
같습니다.

- **동역학 안정성 follow-up.** Vogt 2010 + 확장. b 는 Vogt 2010 의
  동역학 해 안에서 안정. cfg 목적으로 추가 정밀화 불필요.
- **트랜짓 탐색 non-detection.** b 가 트랜짓하지 않음을 확인. 이미
  사용된 경사각 posterior 너머의 정보 없음.
- **대기 탈출율 계산.** 61 Vir 특정 항성풍 모델이 아닌 일반 XUV
  스케일링을 사용.

## Open items for follow-up

- **진질량과 반지름.** b 의 질량은 Msini 전용이고 반지름은 mass-radius
  스케일링 추정치. 미래의 직접 영상 캠페인 (HabEx / LUVOIR 시대) 이나
  Gaia DR5+ 의 정밀 천체측정 경사각이 Msini 를 진질량으로 변환하고
  열복사 검출에서 반지름을 제약합니다. 그때까지는 반지름 의존 필드는
  모두 Confidence=medium 유지.
- **Cfg variant. runaway-Venus 보유 대기.** 광증발 valley 논거에도
  불구하고 작은 비율의 이차 대기 (증기 + CO₂ + N₂, ~1–10 bar) 가
  무대기 cfg 파라미터와 일관됩니다. 두꺼운 증기 대기가 있는 cfg
  variant 는 b 를 구름 덮인 featureless 흰-노란 디스크 (금성 아날로그)
  로 렌더링하며 마그마-pond 시각과 구분됩니다. "보유 대기" 해석을
  선호하는 사용자를 위한 cfg 스위치로 보존.
- **Cfg variant. 3:2 spin-orbit 공명.** e=0.12 에서 b 는 1:1/3:2 경계
  위에 위치. 3:2 cfg variant (수성 아날로그) 는 고정된 substellar 마그마
  pond 대신 천천히 drift 하는 것으로 렌더링됩니다 — 시각적으로 두드러
  지지만 KSP 스케일에서 애니메이션화하기 더 어려움. Phase 3.5 대안
  으로 명시.
- **미래 JWST 또는 HabEx 분광에서의 표면 광물학.** 현재 b 의 표면
  조성을 분해할 수 있는 도구는 없음. 반사광 직접 영상 캠페인이 열복사
  스펙트럼을 산출하면 추론된 basalt 조성 (basalt vs ultramafic vs
  실리카-풍부) 에서 표면-색조 hex 코드를 정밀화 가능.
- **마그마-pond outgassing 율.** Schaefer & Fegley 2009 의 outgassing
  스케일링은 잘 확립되어 있으나 행성 특정 외기권 모델링은 부재. 미래의
  Vidotto 스타일 3D MHD 항성풍 + outgassing 모델이 외기권 컬럼 밀도를
  정밀화 가능.
- **자매 행성 합 가시성.** 이심 d (e=0.35) 와 적당히 이심한 c (e=0.14)
  가 시간 가변 합 기하학을 생성. sub-Neptune c (~5 R⊕) 는 b 의 내합
  거리에서 mv ≈ −4 에 도달 — 두드러진 sky feature 일 만큼 밝음. Phase
  3.5 cfg 를 위한 정확한 가시성 계산.

## Related

- [61-vir](61-vir.md) — 호스트 별 Phase 3 합성.
- [61-vir-c](61-vir-c.md) — 다음 외측 자매 sub-Neptune. 0.22 AU.
- [61-vir-d](61-vir-d.md) — 최외 자매 sub-Neptune. 0.48 AU.
- [trappist-1-b](trappist-1-b.md) — 인접 뜨거운 암석 아날로그. M 왜성 주위 (호스트 조명은 다르지만 표면 카테고리 동일).
- [proxima-cen-d](proxima-cen-d.md) — sub-Earth USP RV-only 아날로그 (더 작고, M 왜성 주위).
- [methodology](../reference/methodology.md) — Decisions 스키마.
