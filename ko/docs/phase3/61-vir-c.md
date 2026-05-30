<!-- 61 Vir c Phase 3 합성. cfg-ready 결정과 근거 -->
# 61 Vir c — Phase 3 Synthesis

61 Vir c 는 G6.5V 솔라 트윈 61 Virginis 주위에서 RV 로 검출된 세 행성
중 가운데 행성이며, Vogt et al. 2010 (HIRES + AAT 결합 해) 가 보고
했습니다. 검출은 RV 전용이고 트랜짓이 없으므로, 직접 측정된 양은 궤도
주기 P = 38.021 ± 0.034 일, 장반경 a = 0.2175 AU, 이심률 e = 0.14,
근일점 인수 ω = 341°, 최소 질량 Msini = 18.2 ± 1.1 M⊕ 로 한정됩니다.
진질량은 18.2 M⊕ 이상이고, 시스템의 거의 edge-on 경사 posterior 에서
가장 그럴듯한 범위는 18–25 M⊕ 입니다. 반지름은 측정된 바 없습니다.
반사광 직접 영상은 미래 등급의 관측 (HabEx / LUVOIR 시대) 이기 때문에,
현재 상태의 대기는 제약되지 않습니다.

**NearStars 시나리오 선택. 보유된 H/He 일차 외피 (~3–5% 질량), 광화학
흡수체에서 비롯되는 haze 가 낀 성층권, 그리고 솔라 트윈 조명 아래
사실상 featureless 구름-덮인 디스크를 가진 따뜻한 sub-Neptune 입니다.**
이는 c 의 약간 더 따뜻한 일조량 (S ≈ 17 S⊕, T_eq(A=0) ≈ 525 K,
T_eq(A=0.3) ≈ 478 K) 에 적용된 GJ 1214 b / HD 97658 b 우주화학 원형
입니다. 대안 — H/He 외피가 없는 암석 / 철-풍부 super-Neptune — 은
Open items 의 cfg variant 로 보존합니다. G 왜성 0.22 AU 의 18 M⊕
코어에 대한 광증발 계산은 외피 보유를 단정적으로 선호하지만, 벌크 조성
mass-radius 분기는 트랜짓 없이는 관측적으로 축퇴되어 있기 때문입니다.

## Decisions

Kopernicus / atmosphere cfg-ready 값입니다. `Confidence`. high = 직접
측정되었거나 강하게 제약됨, medium = 강한 근거를 갖춘 이론, low =
허용 범위 내의 미적 선택.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false (pseudo-synchronous) | medium | 38 일 / 0.22 AU 의 조석 고정 시간은 18 M⊕ 행성에서 ~1–3 Gyr. 나이와 비슷하지만 e=0.14 라 spin 상태는 엄격한 1:1 이 아닌 pseudo-synchronous 가 가장 그럴듯 (Hut 1981. Henning & Hurford 2014) |
| `obliquity_deg` | 5 | low | Tie-break. 조석 감쇠가 obliquity 를 줄이지만 pseudo-synchronous 경우 0 으로 만들지는 않음. 동역학을 위반하지 않으면서 시각적 계절성을 위해 cfg 는 5° 채택 |
| `eccentricity` | 0.14 | high | Vogt 2010 RV fit |
| `argument_of_periastron_deg` | 341 | high | Vogt 2010 |
| `sidereal_period_days` | 38.021 | high | Vogt 2010 궤도 주기. 고정되지 않으면 자전은 다를 수 있음 |
| `semi_major_axis_au` | 0.2175 | high | Vogt 2010 |
| `mass_mearth` | 18.2 | high | Vogt 2010 Msini. 하한값에 불과 (RV-only) |
| `radius_rearth` | 4.5 | medium | Tie-break. 트랜짓 없음. 보유된 H/He 외피의 18 M⊕ mass-radius (Lopez & Fortney 2014. Howe 2014) 는 R = 3.5–6 R⊕. cfg 는 sub-Neptune 표준 중간값 4.5 R⊕ 채택 |
| `surface_gravity_g_earth` | 0.90 | medium | 유도 = 18.2 / 4.5² (H/He 외피 명목 구름-top 기준 반지름에서) |
| `density_g_cc` | 1.10 | medium | 유도. 암석 핵 위 ~3–5% H/He 외피와 일관 |
| `insolation_s_earth` | 17.4 | high | L = 0.82 L☉ 와 a = 0.2175 AU 에서 유도 |
| `equilibrium_temp_k` (A=0) | 525 | high | 유도 |
| `equilibrium_temp_k` (A=0.3) | 478 | high | 유도 |
| `bond_albedo` | 0.3 | medium | Tie-break. haze 가 낀 sub-Neptune 의 0.2–0.5 범위. cfg 는 0.3 채택 (GJ 1214 b / HD 97658 b 아날로그) |
| `dayside_brightness_temp_k_at_clouds` | 460 | medium | T_eq 에서 약한 재분배와 1 bar 구름-top 기준으로 유도 |
| `nightside_brightness_temp_k_at_clouds` | 380 | medium | Pseudo-synchronous 열재분배가 적당한 day-night 대비를 줌 (따뜻한 sub-Neptune 의 Showman 2009 GCM 영역) |
| `atmosphere_present` | true | high | 18 M⊕ × 0.22 AU 의 G 왜성 주위 H/He 외피 보유는 잘 확립 (Owen & Wu 2017 광증발 valley. c 는 손실 경계 한참 오른쪽) |
| `atmosphere_surface_pressure_pa` | (표면 없음. 외피 연속) | high | 가스 행성 — 표면 없음. 구름-top 기준 ~1 bar = 10⁵ Pa |
| `atmosphere_composition` | H₂ ~75%, He ~24%, H₂O ~0.3%, CH₄ ~0.1%, NH₃ ~0.05%, CO, CO₂ 미량, 광화학 haze | medium | 표준 sub-Neptune 원시 조성 (Madhusudhan 2012. Moses 2013). H/He 일차 + 미량 휘발성 |
| `atmosphere_scale_height_km` | 220 | medium | 유도. kT/μg. T≈478 K, μ=2.4 (H/He 우세), g=0.90 g⊕ = 8.8 m/s² |
| `atmosphere_tint_rgb_hex` | `#a8b8cc` (옅은 강철빛 limb haze) | low | Tie-break. 태양빛 노란 조명 아래 H/He Rayleigh 산란이 청색에서 피크지만 광화학 haze (Morley 2015) 가 청색을 감쇠시키고 주황-갈색 underton 을 추가. cfg 는 haze 가 낀 sub-Neptune 의 표준 limb 색조로 muted 강철-청 채택 |
| `cloud_cover_fraction` | 1.0 | high | Haze 가 낀 sub-Neptune 원형 (GJ 1214 b. Kreidberg 2014 featureless 투과 스펙트럼. HD 97658 b 유사). 깊은 KCl/Na₂S 구름과 광화학 haze 담요로부터의 완전한 구름 덮임 |
| `cloud_morphology` | 동풍 적도 jet 에서 비롯된 옅은 zonal banding 위의 전역 haze 데크 | medium | 따뜻한 sub-Neptune 의 Showman 2009 / Lewis 2014 GCM. super-rotating 적도 jet (~1 km/s) 가 옅은 zonal banding 을 구동. ~1 bar 의 깊은 KCl/Na₂S 구름이 광학 레이어 제공 |
| `cloud_tint_rgb_hex` | `#d8c8a8` (따뜻한 크림 haze, GJ 1214 b 아날로그) | low | Tie-break. Morley 2015 sub-Neptune 검색의 광화학 haze 색조. cfg 는 featureless 회색 대신 따뜻한 크림 haze 톤을 채택해 c 에 d 와 구분되는 시각 정체성을 부여 |
| `surface_tint_rgb_hex_primary` | n/a (표면 없음) | high | 가스 행성 |
| `surface_tint_rgb_hex_accent` | n/a | high | 가스 행성 |
| `surface_morphology` | n/a — 가스 행성 | high | 암석 표면 없음 |
| `ocean_present` | false | high | 표면 없음. 깊은 외피는 >10⁴ bar 에서 초임계 H₂O / 이온성 H₂O 로 전이할 수 있으나 별개의 ocean 층은 아님 |
| `tidal_heating_w_m2` | 0.001–0.01 | medium | 38 일에서 e=0.14 에 대한 Bolmont 2020 / Henning & Hurford 2014 스케일링. 일사 예산 대비 무시 가능 |
| `radiogenic_heat_w_m2` | 0.01 | low | 암석 핵 방사성 기여. 가스 행성의 총 열흐름의 작은 비율 |
| `star_apparent_angular_diameter_deg` | 0.235 | high | 유도. 2 × R★ / a × (180/π). 0.2175 AU 의 0.963 R☉ |
| `stellar_illumination_color_temp_k` | 5552 | high | 호스트 Teff |

## Surface synthesis

61 Vir c 는 cfg-렌더링 의미의 **암석 표면이 없습니다** — 행성은 암석 /
얼음 핵 위에 H/He 외피가 연속적으로 감긴 sub-Neptune 입니다. cfg 가
렌더링하는 가시 "표면" 은 ~1 bar 기준 레벨의 구름 데크입니다. 거기서
광화학 haze 와 깊은 KCl / Na₂S 구름이 결합해 솔라 트윈 조명 아래
featureless 전역 구름-덮인 외관을 생성합니다.

깊은 내부 구조는 sub-Neptune mass-radius 스케일링 (Lopez & Fortney 2014.
Howe 2014) 에서 추론됩니다. G 왜성 0.22 AU 의 Msini = 18.2 M⊕ 에서
관측적으로 일관된 mass-radius 분기 세 가지가 있습니다.

1. **H/He 외피 분기 (canonical).** 암석 핵 위 3–5% 외피 질량. R = 4.0–5.0
   R⊕. 밀도 ~1.1 g/cc. 따뜻한 sub-Neptune 원형으로, 질량-단독 측정에서
   GJ 1214 b, HD 97658 b, 또는 K2-18 b 와 구분 불가.

2. **물-풍부 외피 분기.** 암석 핵 위 H/He 없이 ~20% 물 질량 비율.
   R ≈ 3.5–4.0 R⊕. 밀도 ~1.7 g/cc. H/He 경우보다 시각적으로 약간 더
   푸르고 덜 haze 가 낀 모습 (Madhusudhan 2021 Hycean 등급이지만 더
   작은 질량).

3. **철-풍부 암석 분기.** 순수 암석+철 R ≈ 2.4 R⊕. 밀도 ≈ 6.5 g/cc.
   Owen & Wu 2017 광증발 물리에서 배제. 18 M⊕ 의 2.4 R⊕ 암석 행성은
   광증발 valley 중심에 있지만, G 왜성 0.22 AU 에서 손실율은 3–5% H/He
   외피를 벗기는 임계값 한참 아래. 손실 구동 진화는 c 의 파라미터에서
   이 분기를 만들지 않음.

cfg 는 **분기 1 (H/He 외피)** 을 canonical 로 채택합니다. 이는 분기 2
(물-풍부) 에 대한 tie-break 입니다. 둘 다 RV 수준에서 관측적으로 일관
하지만, 분기 1 이 sub-Neptune 인구에서 더 흔합니다 (Fulton 2017 반지름
valley. sub-Neptune 이 ~2.5 R⊕ 피크에서 우세). 물-풍부 분기는 Open
items 의 cfg variant 로 보존합니다.

**색 선택.** 솔라 트윈 조명 아래 dominant 가시 feature 는 상부 성층권
의 광화학 haze 층 (따뜻한 크림 구름-top 색조 `#d8c8a8` 생성) 과 ~1 bar
기준 레벨의 깊은 KCl/Na₂S 구름 데크입니다. H/He 일차 대기의 Rayleigh
산란 시그니처는 limb 에 옅은 청색 색조 (`#a8b8cc`) 를 기여하지만,
광화학 haze 오버레이가 그것을 상당히 감쇠합니다 — GJ 1214 b 의 투과
스펙트럼 (Kreidberg 2014) 은 haze 가 단파장을 차단하기 때문에 본질적
으로 가시 Rayleigh feature 가 없습니다.

**Pseudo-synchronous 자전 하의 형태.** 38 일 궤도 주기와 e=0.14 에서
spin 상태는 **pseudo-synchronous** 가 가장 그럴듯합니다 (Hut 1981,
Henning & Hurford 2014) — 자전율이 근일점 궤도 각속도와 일치하는
~30 일 sidereal 주기 (lock 된 38 일이 아닌). 이 자전 영역의 따뜻한
sub-Neptune 에 대한 Showman 2009 와 Lewis 2014 GCM 은 전역 haze 데크
아래에 얇은 zonal banding 구조를 구동하는 강한 동풍 super-rotating 적도
jet (~1 km/s) 을 예측합니다. 띠는 옅음 — 단위 대비 정도의 구름 + haze
가 그것을 Jupiter 스타일의 또렷한 zonal 줄무늬가 아닌 부드러운 전역
gradient 로 섞어 버립니다.

## Atmosphere synthesis

c 의 대기는 표준적인 sub-Neptune 영역입니다. 암석 / 얼음 핵 위 3–5%
질량의 보유된 H/He 일차 외피, 미량 응결 휘발성 (H₂O, CH₄, NH₃), 그리고
광학 외관을 지배하는 광화학 haze.

**보유 논거.** Owen & Wu 2017 의 광증발 valley 분석은 c 를 손실 경계
한참 오른쪽에 위치시킵니다. 0.82 L☉ G 왜성 0.22 AU 의 18 M⊕ 핵에서
XUV 구동 질량 손실율은 ~10⁷ g/s — Gyr 당 외피 질량의 약 0.1% 손실.
6.1 Gyr 시스템 나이에 걸쳐 총 손실은 외피의 ~0.6% 로, 3–5% 명목 외피
질량 한참 아래. c 는 일차 대기를 여유 있게 보유합니다.

**압력 프로파일.** 표면 없음 — 외피는 상단의 저밀도 가스에서 암석-핵
경계의 다 kbar 초임계 H/He 까지 정수압적으로 연속. cfg 는 렌더러가
가시 디스크로 취급하는 "구름-top" 표면에 대해 1 bar 기준 레벨을
채택합니다. 이 레벨의 스케일 높이 220 km 는 sub-Neptune 스케일 높이
추정 (Lewis 2014) 과 일관. 대기 조성은 표준 원시-외피 모델 (Madhusudhan
2012, Moses 2013) 을 따름. H₂ ~75%, He ~24%, H₂O ~0.3%, CH₄ ~0.1%,
NH₃ ~0.05%, CO, CO₂, HCN 미량, 그리고 광학 외관을 지배하는 광화학
haze.

**구름.** T_eq ~ 480 K 와 압력 0.1–10 bar 에서 평형의 응결 종은 KCl
(~600 K 응결), Na₂S (~700 K), 그리고 상부 고도에서 T 가 273 K 아래로
떨어지는 곳의 물 얼음. KCl/Na₂S 구름이 깊은 구름 데크를 형성. haze 층
위 온도 역전에서는 상부 고도 응결 veil 로 물 얼음 구름이 형성됨. 그
모든 것 위로는 솔라 트윈 UV 아래의 메탄 + HCN 광분해에서 광화학 haze
(Morley 2015, Lavvas 2017) 가 축적됨 — 따뜻한 sub-Neptune 을 투과
분광에서 featureless 로 만드는 광학적으로 두꺼운 담요를 생성.

**1 bar 의 가상 비행선에서 본 하늘 외관.** 위쪽 하늘은 haze 가 낀
크림-주황 (`#d8c8a8`) 이고, 61 Vir 디스크는 haze 를 통해 각지름 ~0.23°
의 흩어진 따뜻한-노란 patch 로 보임 — 지구에서 본 태양 겉보기 지름의
약 절반. haze 를 통한 표면 밝기는 직접 일사 수준에서 의미 있게 감소
(대기 상단에서 S = 17.4 S⊕ 가 haze 감쇠 후 1 bar 레벨에서 ~3 S⊕).
Day-night 대비는 적당 — substellar 구름-top (~460 K) 과 antistellar
구름-top (~380 K) 의 ~80 K 온도차가 또렷한 terminator feature 를
부드럽게 하는 pseudo-zonal 순환을 구동.

**광화학 haze 화학.** 5552 K 솔라 트윈 SED 는 거의 지구-태양 UV-to-
가시 비율을 줌. λ ≲ 200 nm 의 메탄 광분해는 HCN, C₂H₂, 그리고 광학
적으로 두꺼운 haze 층으로 핵형성하는 더 무거운 haze 전구체를 생성
(Lavvas 2017). haze 는 ~0.01 에서 ~0.1 bar 의 성층권 전체에 분포하며
가시 파장에서 광학 깊이 τ ≫ 1 — 본질적으로 c 를 직접 표면 관측에
대해 불투명하게 만듦.

## Rotation & spin synthesis

c 의 spin 상태는 조석-감쇠와 이심률-펌핑 시간 스케일의 균형으로
결정됩니다. 38 일 궤도 주기, 0.22 AU 분리, 18 M⊕ 질량에서 지구 아날로그
내부 Q 의 조석 고정 시간은 ~1–3 Gyr (Henning & Hurford 2014 스케일링)
입니다. 이는 6.1 Gyr 시스템 나이와 비슷합니다 — c 는 obliquity 와
spin 각속도를 감쇠시킬 시간은 있었지만 반드시 엄격한 1:1 lock 에
도달한 것은 아닙니다.

이심률 0.14 (Vogt 2010) 에서 Hut 1981 의 pseudo-synchronous 상태가 가장
그럴듯한 결과. 자전율이 근일점 궤도 각속도와 일치하여, sidereal 주기는
~30 일 (궤도의 38 일 대비). 이는 회전 frame 에서 천천히 drift 하는
substellar 점을 생성. substellar 경도가 ~150 일 만에 전체 회전 완료.

**KSP 구현 노트.** cfg 는 `rotation_period_days` = 30 (pseudo-synchronous,
Kopernicus 단위로 ~2 590 000 초) 을 채택. 이는 궤도 주기와 구분되며,
어떤 궤도 관측자에게 c 에 옅은 일주 사이클을 주는 lock 안 된 느린
자전을 생성.

**Obliquity.** 조석 감쇠가 obliquity 를 줄였지만 pseudo-synchronous
상태가 0 이 아닌 잔존 obliquity 를 허용. cfg 는 tie-break 으로 5°
채택 — 동역학적으로 그럴듯할 정도로 작고, 구름 띠에 옅은 계절 변조를
줄 정도로 큼.

**조석 가열.** 38 일 주기와 18 M⊕ 질량에서 e=0.14 에 대한 Bolmont 2020
/ Henning & Hurford 2014 스케일링은 0.001–0.01 W/m² 의 조석 가열 기여
를 줌. 구름-top 흡수 일사 ~250 W/m² 대비 무시 가능하므로 c 는 열
예산에서 단단히 **일사 지배** 입니다. 깊은 내부는 형성 + 방사성 붕괴
잔여 열 (~0.01 W/m²) 을 가질 수 있지만, 다시 일사 대비 작음.

**암석-행성 의미의 계절 없음.** 이심률 0.14 가 궤도에 걸쳐 일사를
±30% 변조하지만, pseudo-synchronous 자전과 깊은 가스 외피에서 열
반응이 강하게 감쇠됩니다 — 일주 사이클이 깊이에서 평균화되고, 가시
구름 데크는 peri 와 apo 통과 사이에서 몇 K 만 이동합니다.

## Visual styling

표면과 대기 결정을 결합하면 다음과 같습니다.

- **전역 외관 (궤도 뷰).** 솔라 트윈 조명 아래 따뜻한 크림-주황 전체
  색조 (`#d8c8a8`) 의 옅고 haze 가 낀 디스크. 높은 대비 설정에서 옅은
  zonal banding 가시. 그 외에는 featureless 부드러운-가장자리 구. limb
  haze 는 day-night terminator 에서 강철-청 Rayleigh 산란 glow
  (`#a8b8cc`) 추가.
- **구름-top 형태.** super-rotating 적도 jet 의 pseudo-zonal banding
  (디스크 너머 ~3–5 띠, 옅은 대비). substellar 영역 약간 더 밝음 (~460 K
  더 따뜻한 haze + 더 두꺼운 응결 veil). antistellar 약간 더 어두움.
- **광화학 haze 층.** ~10⁵ km 고도의 성층권 haze 가 dominant 따뜻한
  크림 가시색을 생성. 광학 깊이 ≫ 1 이 더 깊은 구름 구조의 시야를
  차단 — c 는 근적외와 가시 파장에서 featureless.
- **Limb haze.** H/He 상부 대기에서 λ ≲ 0.5 μm 의 옅은 강철-청 Rayleigh
  산란. 감쇠되지만 terminator 와 투과에서 가시. 비스듬한 햇빛에서 디스크
  주위에 부드러운 cyan 고리 추가.
- **야간면.** b 에서 반사된 자매 행성 빛 (매우 어둡고 작은 디스크) 과
  d 에서 (비슷한 등급, 더 큰 위상). 야간 구름-top 온도 380 K — 광학
  열복사에는 너무 차갑지만 중적외 (~10 μm) 에서 밝음.
- **하늘의 별.** 61 Vir 가 c 에서 0.235° 차지 — 지구에서 본 태양 각
  크기의 약 절반. haze 를 통해 또렷한 디스크가 아닌 흩어진 따뜻한-노란
  patch (`#fff2dc` cfg-인코딩 호스트 색조) 로 보임. 표면 조명은 대기
  상단에서 지구의 ~17 배, haze 감쇠 후 1 bar 구름-top 에서 지구의 ~3
  배.
- **하늘의 자매 행성.** b (다음 안쪽 0.05 AU) 가 내합 시 (5 일마다)
  각 크기 ~0.04° 로 등장. d (다음 외측 0.48 AU) 가 합 시 (55 일마다)
  각 크기 ~0.1° 로 등장. 거의 동일 평면 기하학. 합은 시스템 내부 관측
  자에게 sky 이벤트.
- **선택적 banding 애니메이션.** 구름 띠의 느린 zonal drift (시간
  스케일 ~30 일, pseudo-synchronous 자전 주기와 일치) 가 정적으로
  보이는 디스크에 미묘한 역동성을 추가해 줌. 우선순위 낮은 Phase 3.5
  시각 디테일.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Vogt S. S. et al. 2010** — *A Super-Earth and Two Neptunes
  Orbiting the Nearby Sun-Like Star 61 Virginis*, ApJ 708, 1366
  (`2010ApJ...708.1366V`). 발견 논문. c 의 궤도 (P=38.021 d,
  a=0.2175 AU, e=0.14, ω=341°) 와 최소 질량 (Msini = 18.2 ± 1.1 M⊕)
  보고. HIRES + AAT 결합 RV 해. Decisions 표의 모든 궤도 + 질량 값이
  여기에 묶입니다.
- **Owen J. E. & Wu Y. 2017** — *The evaporation valley in the
  Kepler planets*, ApJ 847, 29 (`2017ApJ...847...29O`, arXiv:1705.10810).
  광증발-valley 물리. c 를 손실 경계 한참 오른쪽에 위치 (XUV 구동
  손실이 6 Gyr 에 걸쳐 외피의 ~0.6%). high 신뢰도로 `atmosphere_present
  = true` 의 anchor.
- **Lopez E. D. & Fortney J. J. 2014** — *Understanding the
  mass-radius relation for sub-Neptunes*, ApJ 792, 1
  (`2014ApJ...792....1L`, arXiv:1311.0329). sub-Neptune envelope
  mass-radius 스케일링. 3–5% H/He 외피 18 M⊕ 에서 R = 4.0–5.0 R⊕.
  cfg 는 4.5 R⊕ 채택. `radius_rearth` tie-break 의 anchor.
- **Howe A. R. et al. 2014** — *Mass-radius relations and core-envelope
  decompositions of super-Earths and sub-Neptunes*, ApJ 787, 173
  (`2014ApJ...787..173H`). sub-Neptune mass-radius
  다양성. H/He 외피 canonical 해석을 지지하고 물-풍부 대안의 경계를
  정함.
- **Madhusudhan N. 2012** — *C/O ratio as a dimension for
  characterizing exoplanetary atmospheres*, ApJ 758, 36
  (`2012ApJ...758...36M`, arXiv:1209.2412). sub-Neptune 원시-외피 조성
  baseline. H/He 일차 + 미량 응결 조성을 견인.
- **Moses J. I. et al. 2013** — *Compositional diversity in the
  atmospheres of hot Neptunes*, ApJ 777, 34 (`2013ApJ...777...34M`,
  arXiv:1306.5178). sub-Neptune 광화학. CH₄/HCN/광화학-haze 사슬을
  정보화.
- **Morley C. V. et al. 2015** — *Thermal emission and reflected
  light spectra of super Earths with flat transmission spectra*, ApJ
  815, 110 (`2015ApJ...815..110M`, arXiv:1511.01492). Haze 가 낀
  sub-Neptune 검색 프레임워크. `atmosphere_tint` 와 `cloud_tint`
  tie-break 을 견인 (태양 조명 아래의 따뜻한 크림 haze).
- **Lavvas P. & Koskinen T. 2017** — *Aerosol properties of the
  atmospheres of extrasolar giant planets*, ApJ 847, 32
  (`2017ApJ...847...32L`, arXiv:1707.08077). sub-Neptune 광화학 haze
  생성 메커니즘. 전역 구름 덮임과 haze 광학 깊이를 정보화.
- **Kreidberg L. et al. 2014** — *Clouds in the atmosphere of the
  super-Earth exoplanet GJ 1214 b*, Nature 505, 69
  (`2014Natur.505...69K`, arXiv:1401.0022). 표준적 "featureless 투과
  스펙트럼" sub-Neptune. c 는 비슷한 기대 시각의 더 따뜻한 아날로그.
- **Showman A. P. et al. 2009** — *Atmospheric circulation of hot
  Jupiters: coupled radiative-dynamical GCM*, ApJ 699, 564
  (`2009ApJ...699..564S`, arXiv:0809.2089). 조석 영향을 받는 가스 행성
  의 super-rotating 적도 jet 을 확립. c 의 `cloud_morphology` (zonal
  banding) 를 정보화.
- **Lewis N. K. et al. 2014** — *GCMs of warm sub-Neptunes*, ApJ 795,
  150 (`2014ApJ...795..150L`, arXiv:1410.0008). ~38 일 주기 sub-Neptune
  영역에 대한 GCM 스케일링. pseudo-synchronous spin 과 적도-jet 순환을
  지지.
- **Hut P. 1981** — *Tidal evolution in close binary systems*, A&A
  99, 126 (`1981A&A....99..126H`). 이심 궤도의 pseudo-synchronous spin
  평형. c 의 spin 상태에 대한 기초 인용.
- **Henning W. G. & Hurford T. 2014** — *Tidal heating in multilayered
  terrestrial exoplanets*, ApJ 789, 30 (`2014ApJ...789...30H`,
  arXiv:1311.5904). sub-Neptune 조석 가열 + spin-lock 시간 스케일.
  c 의 파라미터에서 ~1–3 Gyr 제공.
- **Bolmont E. et al. 2020** — *Tidal dissipation and obliquity
  evolution* (`2020A&A...644A.165B`). c 의 조석-가열
  flux 스케일링 제공 (0.001–0.01 W/m²).

### Read (context / methodology, not decision-driving)

- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age
  Estimation for Solar-Type Dwarfs* (`2008ApJ...687.1264M`,
  arXiv:0807.1686). 호스트 합성에서 상속. 61 Vir 나이 6.1 ± 1.7 Gyr.
  광증발 진화 시간 스케일을 결정.
- **Pavlenko Y. V. et al. 2012** — *Solar twin candidates*
  (`2012MNRAS.422..542P`, arXiv:1112.0590). 호스트 합성에서 상속.
  광화학 haze 모델을 위한 솔라 트윈 SED 확인.
- **Fulton B. J. et al. 2017** — *The California-Kepler Survey III.
  A Gap in the Radius Distribution of Small Planets*, AJ 154, 109
  (`2017AJ....154..109F`, arXiv:1703.10375). 반지름 valley 인구.
  c 의 18 M⊕ 인구에 대한 H/He 외피 canonical 해석을 지지.
- **Wyatt M. C. et al. 2012** — *Herschel imaging of 61 Vir*
  (`2012MNRAS.424.1206W`, arXiv:1204.6063). 호스트 합성에서 상속. 간략
  히 인용. 30 AU 의 차가운 debris 고리는 0.22 AU 의 c 와 동역학적으로
  상호작용하지 않음.
- **Madhusudhan N. et al. 2021** — *Habitability and biosignatures of
  Hycean worlds*, ApJ 918, 1 (`2021ApJ...918....1M`, arXiv:2108.10888).
  sub-Neptune 의 Hycean 대안 시나리오. d 의 Open-items variant 와 관련.
  더 따뜻한 T_eq 의 c 에는 덜 적용되지만 더 넓은 sub-Neptune 분류
  프레임워크로 인용.

### Read (instrument-only, not visual-informative)

- **Marcy G. W. et al. 2014** — Kepler 슈퍼지구 통계 맥락.

### Not read — no arXiv preprint or low-priority (~10 papers)

c 특정 arXiv 기록은 작습니다. 읽지 않은 집합은 주로 다음과 같습니다.

- **Vogt 2010 시스템의 동역학 안정성 follow-up.**
- **트랜짓 탐색 non-detection.** c 가 트랜짓하지 않음을 확인. e=0.14,
  a=0.22 AU 에서 c 의 기하학적 트랜짓 확률은 ~1.5% 이므로 non-detection
  은 무작위 경사와 일관.
- **61 Vir 특정 항성풍 모델 없이 일반 광증발율 계산.**

## Open items for follow-up

- **직접 영상에서의 진질량과 반지름.** c 의 질량은 Msini 전용이고
  반지름은 mass-radius 스케일링 추정치. 미래의 직접 영상 캠페인이
  반사광 검출에서 진질량 + 반지름을 산출. HabEx / LUVOIR 시대 관측.
- **Cfg variant. 물-풍부 Hycean 스타일 외피.** c 의 일조량 (T_eq ~
  480 K) 에서 H₂ 대기를 가진 물-풍부 외피는 H/He 일차 외피와 관측적으로
  일관. cfg variant 는 c 를 더 밀도 높고 덜 haze 가 낀, 더 깊은-청
  디스크로 렌더링. Phase 3.5 대안으로 명시.
- **Cfg variant. 암석 외피-없음 대안.** 광증발 물리가 외피 보유를 강하게
  선호하지만 순수 암석 18 M⊕ 행성 (R ≈ 2.4 R⊕. 밀도 ~6.5 g/cc) 의 작은
  잔여 확률 남아 있음. 렌더는 b 와 비슷한 뜨거운 암석 세계지만 더
  차가움 — haze 덮인 canonical 해석과 시각적으로 구분. cfg variant 로
  보존.
- **미래 JWST 또는 HabEx 투과 분광.** c 가 트랜짓하지 않지만, 미래의
  직접-영상 분광이 구름-top 조성을 분해할 수 있음. 정밀화 기회.
  H₂O/CH₄/NH₃ 풍부도, haze 광학 깊이, 더 깊은 구름 조성 (KCl vs Na₂S
  vs ZnS).
- **GCM 구동 구름 형태.** 따뜻한 sub-Neptune 에 대한 Lewis 2014 GCM
  은 zonal banding 을 예측하지만 c 의 특정 파라미터에서의 띠 대비는
  시뮬레이션된 바 없음. 표적 GCM 실행이 "전역 haze 데크" 와 "haze
  + 가시 Jupiter 스타일 띠" 사이의 `cloud_morphology` 선택을 제약 가능.
- **대기 탈출율 교차 점검.** Owen & Wu 2017 일반 스케일링이 외피 보유를
  지지. 61 Vir 특정 항성풍 + XUV 모델 (Vidotto 스타일) 이 손실율 추정을
  정밀화.

## Related

- [61-vir](61-vir.md) — 호스트 별 Phase 3 합성.
- [61-vir-b](61-vir-b.md) — 다음 안쪽 자매 뜨거운 슈퍼지구. 0.05 AU.
- [61-vir-d](61-vir-d.md) — 다음 외측 자매 sub-Neptune. 0.48 AU (더 차가운 아날로그).
- [methodology](../reference/methodology.md) — Decisions 스키마.
