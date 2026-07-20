<!-- 61 Vir d Phase 3 합성. cfg-ready 결정과 근거 -->
# 61 Vir d — Phase 3 Synthesis

61 Vir d 는 G6.5V 솔라 트윈 61 Virginis 주위에서 RV 로 검출된 세 행성
중 가장 바깥 행성이며, Vogt et al. 2010 (HIRES + AAT 결합 해) 가 보고
했습니다. 검출은 RV 전용이고 트랜짓이 없으므로, 직접 측정된 양은 궤도
주기 P = 123.01 ± 0.55 일, 장반경 a = 0.476 AU, 이심률 e = 0.35,
근일점 인수 ω = 314°, 최소 질량 Msini = 22.9 ± 2.6 M⊕ 로 한정됩니다.
진질량은 22.9 M⊕ 이상이고, 시스템의 거의 edge-on 경사 posterior 에서
가장 그럴듯한 범위는 23–32 M⊕ 입니다. 반지름은 측정된 바 없습니다.
반사광 직접 영상은 미래 등급의 관측 (HabEx / LUVOIR 시대) 이기 때문에,
현재 상태의 대기는 제약되지 않습니다.

**NearStars 시나리오 선택. 보유된 H/He 일차 외피 (~5–8% 질량), H₂O 와
NH₃ 얼음으로 더 두꺼워진 응결 구름 데크, 옅은 zonal banding, 그리고
e = 0.35 궤도에 걸쳐 강하게 변조되는 일사를 가진 차갑고 이심한
sub-Neptune 입니다.** 이는 d 의 더 차가운 일조량 (S ≈ 3.6 S⊕,
T_eq(A=0) ≈ 383 K, T_eq(A=0.3) ≈ 351 K) 과 높은 이심률에 적용된 K2-18 b
/ Hycean-인접 원형입니다. 대안 — 액체 물 층 위 얕은 H₂ 외피의 완전
Hycean 물-세계 — 는 Open items 의 cfg variant 로 보존합니다. d 의 평균
일조량이 Madhusudhan 2021 Hycean 윈도우의 안쪽 가장자리에 가깝지만,
e = 0.35 궤도 excursion 이 근일점에서 그것을 runaway-greenhouse 경계
한참 안쪽까지 흔들기 때문입니다.

## Decisions

Kopernicus / atmosphere cfg-ready 값입니다. `Confidence`. high = 직접
측정되었거나 강하게 제약됨, medium = 강한 근거를 갖춘 이론, low =
허용 범위 내의 미적 선택.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false (pseudo-synchronous) | medium | 123 일 / 0.48 AU 의 조석 고정 시간은 23 M⊕ 행성에서 ~5–15 Gyr. 6 Gyr 시스템 나이 초과. e=0.35 에서 spin 상태는 pseudo-synchronous (Hut 1981. Henning & Hurford 2014). lock 안 됨 |
| `obliquity_deg` | 15 | low | Tie-break. d 의 분리에서 조석 감쇠가 불완전. cfg 는 구름 띠의 가시 계절 변조를 위해 15° 채택. 거의 동일 평면 sub-Neptune 의 동역학 허용 윈도우 내 |
| `eccentricity` | 0.35 | high | Vogt 2010 RV fit. 61 Vir 세 행성 중 최고 이심률 |
| `argument_of_periastron_deg` | 314 | high | Vogt 2010 |
| `sidereal_period_days` | 123.01 | high | Vogt 2010 궤도 주기. 자전은 pseudo-sync 로 다름 |
| `semi_major_axis_au` | 0.476 | high | Vogt 2010 |
| `mass_mearth` | 22.9 | high | Vogt 2010 Msini. 하한값에 불과 (RV-only) |
| `radius_rearth` | 5.0 | medium | Tie-break. 트랜짓 없음. 5–8% H/He 외피의 23 M⊕ mass-radius (Lopez & Fortney 2014. Howe 2014) 는 R = 4.5–5.5 R⊕. cfg 는 차가운-sub-Neptune 중간값 5.0 R⊕ 채택. c 보다 살짝 큰데, d 의 더 차가운 외피가 덜 압축되기 때문 |
| `surface_gravity_g_earth` | 0.92 | medium | 유도 = 22.9 / 5.0² (H/He 외피 명목 구름-top 기준 반지름에서) |
| `density_g_cc` | 1.00 | medium | 유도. 암석 핵 위 ~5–8% H/He 외피와 일관. 더 차가운 평형에서 c 보다 약간 덜 밀도 높음 |
| `insolation_s_earth` | 3.62 | high | L = 0.82 L☉ 와 a = 0.476 AU 에서 유도 |
| `insolation_s_earth_periastron` | 8.57 | high | 유도. e = 0.35 에서 S × (1 − e)⁻² |
| `insolation_s_earth_apoastron` | 1.99 | high | 유도. e = 0.35 에서 S × (1 + e)⁻² |
| `equilibrium_temp_k` (A=0) | 383 | high | 유도 |
| `equilibrium_temp_k` (A=0.3) | 351 | high | 유도 |
| `equilibrium_temp_k_periastron` (A=0) | 476 | high | 유도. T_eq × (1 − e)⁻⁰·⁵ |
| `equilibrium_temp_k_apoastron` (A=0) | 330 | high | 유도. T_eq × (1 + e)⁻⁰·⁵ |
| `bond_albedo` | 0.35 | medium | Tie-break. 더 두꺼운 H₂O/NH₃ 구름 데크를 가진 차가운 sub-Neptune 의 0.2–0.5 범위. cfg 는 0.35 채택 (d 의 더 차가운 온도가 더 반사적인 물-얼음 구름을 선호해 c 의 0.30 보다 살짝 높음) |
| `dayside_brightness_temp_k_at_clouds` | 340 | medium | T_eq 에서 적당한 재분배와 1 bar 구름-top 기준으로 유도 |
| `nightside_brightness_temp_k_at_clouds` | 285 | medium | 더 깊은 외피의 Pseudo-synchronous 열재분배가 적당한 day-night 대비를 줌 (차가운 sub-Neptune 의 Showman 2009 / Lewis 2014 GCM 영역) |
| `atmosphere_present` | true | high | 23 M⊕ × 0.48 AU 의 G 왜성 주위 H/He 외피 보유는 분명 (Owen & Wu 2017 광증발 valley. d 는 손실 경계 한참 바깥) |
| `atmosphere_reference_pressure_pa` | 100000 | high | 가스 행성 — 고체 표면 없음. 구름층 렌더링 기준 ~1 bar = 10⁵ Pa |
| `atmosphere_composition` | H₂ ~74%, He ~24%, H₂O ~0.5%, CH₄ ~0.2%, NH₃ ~0.1%, CO, CO₂ 미량, 광화학 haze | medium | 표준 sub-Neptune 원시 조성 (Madhusudhan 2012. Moses 2013). c 보다 더 높은 응결성 풍부도. d 의 더 차가운 온도가 깊이-혼합된 휘발성을 가시 데크까지 도달하게 허용 |
| `atmosphere_scale_height_km` | 165 | medium | 유도. kT/μg. T≈351 K, μ=2.4 (H/He 우세), g=0.92 g⊕ = 9.0 m/s² |
| `atmosphere_tint_rgb_hex` | `#b8c4d4` (옅은 청-회 limb haze) | low | Tie-break. 태양빛 노란 조명 아래 H/He Rayleigh 산란이 청색에서 피크. 더 차가운 T_eq 가 c 보다 광화학 haze 감쇠가 적어 limb 는 더 두드러진 Rayleigh-청 색조를 보임 |
| `cloud_cover_fraction` | 1.0 | high | 두꺼운 응결 구름 데크 (상부 레벨의 H₂O 얼음, 더 깊은 레벨의 NH₃ 얼음) 를 가진 차가운 sub-Neptune. 결합된 구름 + 광화학 haze 담요의 거의 완전한 덮임 |
| `cloud_morphology` | 동풍 적도 jet 의 옅은 zonal banding 을 가진 전역 물-얼음 + 암모니아-얼음 구름 데크. 이심 궤도에 걸쳐 변조되는 구름 두께 | medium | 차가운 sub-Neptune 의 Showman 2009 / Lewis 2014 GCM. super-rotating 적도 jet (~0.5 km/s) 가 옅은 zonal banding 을 구동. H₂O / NH₃ 응결물이 광학적으로 두꺼운 데크 형성. e=0.35 가 원일점 근처에서 주기적 두꺼워짐과 근일점 근처에서 부분 흩어짐을 구동 |
| `cloud_tint_rgb_hex` | `#e0e4ec` (옅은 청-흰 구름 데크, 물-얼음 아날로그) | low | Tie-break. 물-얼음 구름은 본질적으로 흰-청. cfg 는 c 의 따뜻한 크림 대신 옅은 청-흰 톤을 채택해 d 에 "더 차갑고 더 얼음 같은" 시각 정체성을 부여 |
| `surface_tint_rgb_hex_primary` | n/a (표면 없음) | high | 가스 행성 |
| `surface_tint_rgb_hex_accent` | n/a | high | 가스 행성 |
| `surface_morphology` | n/a — 가스 행성 | high | 암석 표면 없음 |
| `ocean_present` | false | high | 표면 없음. 깊은 외피는 >10⁴ bar 에서 초임계 H₂O / 이온성 H₂O 층을 호스트할 수 있으나 별개의 ocean 은 아님 |
| `tidal_heating_w_m2` | 0.005–0.05 | medium | 123 일 주기에서 e=0.35 에 대한 Bolmont 2020 / Henning & Hurford 2014 스케일링. 더 큰 e 때문에 c 보다 높지만 일사 예산 대비 여전히 무시 가능 |
| `radiogenic_heat_w_m2` | 0.01 | low | 암석 핵 방사성 기여. 가스 행성의 총 열흐름의 작은 비율 |
| `seasonal_amplitude_factor` | 4.3 | high | 유도. e=0.35 에서 S_peri / S_apo = ((1+e)/(1-e))² = 4.3×. 61 Vir 시스템 최대의 계절 변조 |
| `star_apparent_angular_diameter_deg` | 0.108 | high | 유도. 2 × R★ / a. 0.476 AU 의 0.963 R☉ |
| `stellar_illumination_color_temp_k` | 5552 | high | 호스트 Teff |

## Surface synthesis

61 Vir d 는 cfg-렌더링 의미의 **암석 표면이 없습니다** — 행성은 암석 /
얼음 핵 위에 H/He 외피가 연속적으로 감긴 sub-Neptune 입니다. cfg 가
렌더링하는 가시 "표면" 은 ~1 bar 기준 레벨의 구름 데크입니다. 거기서
물-얼음과 암모니아-얼음 응결물이 광화학 haze 와 결합해 솔라 트윈 조명
아래 featureless 전역 구름-덮인 외관을 생성합니다.

깊은 내부 구조는 sub-Neptune mass-radius 스케일링 (Lopez & Fortney 2014.
Howe 2014) 에서 추론됩니다. G 왜성 0.48 AU 의 Msini = 22.9 M⊕ 에서
관측적으로 일관된 mass-radius 분기 세 가지가 있습니다.

1. **H/He 외피 분기 (canonical).** 암석 / 얼음 핵 위 5–8% 외피 질량.
   R = 4.5–5.5 R⊕. 밀도 ~1.0 g/cc. 차가운 sub-Neptune 원형. c 보다
   살짝 더 두꺼운 외피인데, 더 차가운 평형 온도가 광증발 압력을 무시
   가능한 수준으로 줄이기 때문.

2. **Hycean / 물-세계 분기.** 액체 물 층 위에 얇은 H₂ 대기를 가진
   ~30–50% 물 질량 비율. R ≈ 3.5–4.5 R⊕. 밀도 ~1.8 g/cc. d 의 평균
   T_eq ≈ 351 K 는 Madhusudhan 2021 Hycean 윈도우 (물-얼음 표면에서
   T_eq 200–400 K) 의 안쪽 가장자리에 가까워, 평균 궤도에서는 이 분기가
   실제로 가능. 그러나 e=0.35 가 T_eq 를 근일점에서 476 K 까지 끌어
   올려 1 bar 표면 압력의 액체 물 안정 한계 한참 위. 분기는 cfg variant
   로 보존.

3. **철-풍부 암석 분기.** 순수 암석+철 R ≈ 2.7 R⊕. 밀도 ≈ 6.5 g/cc.
   Owen & Wu 2017 광증발 물리에서 배제. G 왜성 0.48 AU 에서 6 Gyr
   에 걸친 손실율은 어떤 H/He 외피의 ~0.05% 로, 벗기는 임계값 한참
   아래. 손실 구동 진화는 d 의 파라미터에서 이 분기를 만들지 않음.

cfg 는 c 합성과 평행하게 **분기 1 (H/He 외피)** 을 canonical 로 채택
합니다. d 의 더 차가운 외피는 c 보다 더 풍부한 응결 화학을 호스트
합니다 (T_eq < 400 K 에서 물-얼음 구름이 광학적으로 우세해져 c 의 더
따뜻한 478 K 에서 가능한 NH₃ / KCl / Na₂S 인구를 보충). 물-풍부 Hycean
변형은 평균-궤도 T_eq 단독으로는 c 보다 d 에 더 설득력 있지만, 근일점
excursion 이 그것을 불리하게 만듭니다. canonical 해석은 여전히 H/He
sub-Neptune.

**색 선택.** 솔라 트윈 조명 아래 dominant 가시 feature 는 상부 대류권
물-얼음 구름 데크 (옅은 청-흰 구름-top 색조 `#e0e4ec` 생성) 와 그 아래
~3 bar 레벨의 암모니아-얼음 데크입니다. 광화학 haze (Lavvas 2017) 는
c 의 더 높은 T_eq 보다 얇은데, 더 차가운 성층권이 메탄 광분해 효율을
줄이기 때문입니다. 따라서 Rayleigh-청 limb haze (`#b8c4d4`) 가 c 보다
더 가시적이고, haze 담요가 지배하는 c 와 구분됩니다.

**Pseudo-synchronous 자전 하의 형태.** 123 일 궤도 주기와 e=0.35 에서
spin 상태는 pseudo-synchronous (Hut 1981, Henning & Hurford 2014) — 자전
율이 근일점 궤도 각속도와 일치하여 sidereal 주기는 ~84 일 (궤도의 123
일 대비). 이 자전 영역의 차가운 sub-Neptune 에 대한 Showman 2009 와
Lewis 2014 GCM 은 적당한 동풍 super-rotating 적도 jet (~0.5 km/s. c 보다
느림. 더 긴 자전 주기가 Coriolis 구동 jet 가속을 약화시키기 때문) 이
미묘한 zonal banding 을 구동한다고 예측. 띠는 강한 이심률 구동 계절
사이클로 변조되는 부드러운 대비 변동으로 가시. 근일점 근처에서는 구름
데크가 얇아져 띠가 살짝 더 또렷해지고, 원일점 근처에서는 데크가 거의
균일한 gradient 로 두꺼워짐.

## Atmosphere synthesis

d 의 대기는 표준적인 차가운 sub-Neptune 영역입니다. 암석 / 얼음 핵 위
5–8% 질량의 보유된 H/He 일차 외피, 미량 응결 휘발성 (H₂O, CH₄, NH₃),
그리고 깊은 물-얼음과 암모니아-얼음 구름 데크와 결합해 featureless
가시 디스크를 생성하는 광화학 haze.

**보유 논거.** Owen & Wu 2017 의 광증발 valley 분석은 d 를 손실 경계
한참 오른쪽에 위치시킵니다. 0.82 L☉ G 왜성 0.48 AU 의 23 M⊕ 핵에서
XUV 구동 질량 손실율은 ~10⁵ g/s — Gyr 당 외피 질량의 약 10⁻⁴ 손실.
6.1 Gyr 시스템 나이에 걸쳐 총 손실은 외피의 ~10⁻³ 로 완전히 무시 가능.
d 는 61 Vir 행성 중 가장 큰 마진으로 일차 대기를 보유합니다.

**압력 프로파일.** 표면 없음 — 외피는 상단의 저밀도 가스에서 암석-핵
경계의 다 kbar 초임계 H/He 까지 정수압적으로 연속. cfg 는 렌더러가
가시 디스크로 취급하는 "구름-top" 표면에 대해 1 bar 기준 레벨을 채택.
이 레벨의 스케일 높이 165 km 는 차가운 sub-Neptune 스케일 높이 추정
(Lewis 2014) 과 일관. 대기 조성은 표준 원시-외피 모델 (Madhusudhan
2012, Moses 2013) 을 따름. H₂ ~74%, He ~24%, H₂O ~0.5%, CH₄ ~0.2%,
NH₃ ~0.1%, CO, CO₂, HCN 미량, 그리고 광화학 haze. 응결성 풍부도는
c 보다 높은데, d 의 더 차가운 온도가 깊이-혼합된 휘발성 (특히 H₂O 와
NH₃) 을 열적 해리 없이 가시 데크까지 도달하게 허용하기 때문입니다.

**구름.** T_eq ~ 351 K (평균) 와 압력 0.1–10 bar 에서 평형의 응결
종은 물-얼음 (상부 대류권 기준 고도에서 273 K 에 응결), NH₃ 얼음
(더 깊은 고도에서 ~200 K 에 응결), 그리고 NH₄SH (Lewis 1969 열화학,
~5 bar 레벨). 물-얼음이 광학적으로 우세한 상부 구름 데크 형성. NH₃
얼음과 NH₄SH 가 더 깊은 층 형성. 광화학 haze (Morley 2015, Lavvas
2017) 는 메탄 + HCN 광분해에서 형성되어 존재하지만 c 의 더 따뜻한
T_eq 보다 얇음 — 더 차가운 성층권이 광화학 반응 효율을 줄임.

**1 bar 의 가상 비행선에서 본 하늘 외관.** 위쪽 하늘은 옅은 청-흰
(`#e0e4ec`) 이고, 61 Vir 디스크는 구름 덮임을 통해 각지름 ~0.11° 의
적당히 흩어진 따뜻한-노란 patch 로 보임 — 지구에서 본 태양 겉보기
지름의 약 5 분의 1. 구름 데크를 통한 표면 밝기는 직접 일사 수준에서
의미 있게 감소 (대기 상단에서 S = 3.6 S⊕ 가 구름 감쇠 후 1 bar 레벨
에서 ~0.5 S⊕). 구름-top 에서 day-night 대비는 적당 — substellar (~340 K)
와 antistellar (~285 K) 구름-top 의 ~55 K 온도차가 terminator feature 를
부드럽게 하는 pseudo-zonal 순환을 구동.

**이심률 구동 계절.** e=0.35 궤도는 근일점과 원일점 사이에서 4.3×
일사 변조를 구동하며, 어떤 61 Vir 행성보다 큽니다. 이것이 d 의 dominant
대기 강제력. 근일점에서 구름 데크가 얇아짐 (T_eq 가 476 K 로 오르고
상부 대류권이 국부적으로 물-응결 온도 위로 따뜻해지면서 물-얼음 구름이
부분적으로 승화), 더 어두운 NH₃ 와 더 깊은 haze 층이 드러남. 원일점
에서 데크가 두꺼워지고 디스크가 더 균일하게 밝게 보임. 계절 사이클
주기는 123 일이고, 궤도 위상이 반사광에서 수 % 수준으로 관측 가능한
느린 밝기 변조를 결정.

**광화학 haze 화학.** 5552 K 솔라 트윈 SED 는 거의 지구-태양 UV-to-가시
비율을 줌. λ ≲ 200 nm 의 메탄 광분해는 HCN, C₂H₂, 그리고 더 무거운
haze 전구체를 생성 (Lavvas 2017). d 의 더 차가운 성층권은 (c 와 비교
해서) 분자당 같은 UV flux 에서 광분해율을 ~3× 줄여, 광학 외관을 지배
하지 않는 더 얇은 haze 층을 줌. 따라서 H/He Rayleigh 시그니처는 c
보다 d 에서 더 가시적.

## Rotation & spin synthesis

d 의 spin 상태는 조석-감쇠와 이심률-펌핑 시간 스케일의 균형으로
결정됩니다. 123 일 궤도 주기, 0.48 AU 분리, 23 M⊕ 질량에서 지구
아날로그 내부 Q 의 조석 고정 시간은 ~5–15 Gyr (Henning & Hurford 2014
스케일링) 입니다. 이는 6.1 Gyr 시스템 나이를 초과합니다 — d 는 1:1
lock 에 도달할 시간이 없었습니다. obliquity 감쇠가 불완전했습니다.
cfg 는 시각 계절 변조를 위해 15° 를 tie-break 으로 채택합니다.

이심률 0.35 (Vogt 2010) 에서 Hut 1981 의 pseudo-synchronous 상태가
dominant attractor. 자전율이 근일점 궤도 각속도와 일치하여 sidereal
주기는 ~84 일 (궤도의 123 일 대비). 이는 회전 frame 에서 천천히 drift
하는 substellar 점을 생성. substellar 경도가 ~280 일 만에 전체 회전
완료.

**KSP 구현 노트.** cfg 는 `rotation_period_days` = 84 (pseudo-synchronous,
Kopernicus 단위로 ~7 257 600 초) 를 채택. 이는 궤도 주기와 구분되며,
e=0.35 궤도의 강한 계절 사이클과 결합된 lock 안 된 느린 자전이 d 에
옅은 일주 사이클을 줍니다.

**Obliquity.** d 의 거리에서 조석 감쇠가 불완전. cfg 는 tie-break 으로
15° 채택 — 구름 띠의 가시 계절 변조를 줄 만큼 크고 (구름-띠 위도가
궤도에 걸쳐 sub-solar 위도와 함께 이동), 61 Vir 시스템의 거의 동일
평면 경사 posterior 를 유지할 만큼 작음. b/c 안쪽 행성은 더 작은 분리
에서의 더 강한 조석 감쇠 때문에 더 낮은 obliquity 를 가짐.

**조석 가열.** 123 일 주기와 23 M⊕ 질량에서 e=0.35 에 대한 Bolmont
2020 / Henning & Hurford 2014 스케일링은 0.005–0.05 W/m² 의 조석 가열
기여를 줌. 더 높은 이심률이 c 의 0.001–0.01 W/m² 위로 flux 를 끌어
올리지만, 더 긴 주기가 전체 예산을 감쇠. 구름-top 흡수 평균 일사 ~50
W/m² 대비 무시 가능하므로 d 는 열 예산에서 단단히 **일사 지배** 입니다.
깊은 내부는 형성 + 방사성 붕괴 잔여 열 (~0.01 W/m²) 을 가질 수 있지만,
다시 일사 대비 작음.

**강한 계절.** 이심률 0.35 가 궤도에 걸쳐 4.3× 일사 변조를 구동. 깊은
H/He 외피의 느린 열 반응과 결합해 계절 사이클은 극적인 온도 변동이
아닌 구름-데크 두께 변조로 나타남 — 그러나 가시 디스크 밝기가 123 일
궤도에 걸쳐 ~10–15% 변조됩니다. 61 Vir 안쪽 시스템에서 가장 강한
계절 광도 시그니처.

## Visual styling

표면과 대기 결정을 결합하면 다음과 같습니다.

- **전역 외관 (궤도 뷰).** 솔라 트윈 조명 아래 부드러운 차가운 전체
  색조 (`#e0e4ec`) 의 옅은 청-흰, haze 가 낀 디스크. c 보다 살짝 더
  얼음 같아 보이며, 한눈에 "더 차가운 외측 sub-Neptune" 으로 읽힐 만큼
  구분됨. 높은 대비에서 옅은 zonal banding 가시. 그 외에는 c 보다
  또렷한 Rayleigh-청 limb haze (`#b8c4d4`) 를 가진 featureless 부드러운-
  가장자리 구.
- **구름-top 형태.** super-rotating 적도 jet 의 pseudo-zonal banding
  (디스크 너머 ~3–4 띠, 옅은 대비). substellar 영역 약간 더 밝음
  (~340 K 더 따뜻한 구름 + 더 두꺼운 응결 veil). antistellar 약간 더
  어두움. 근일점 근처에서 banding 대비 강화 (구름 데크가 얇아짐),
  원일점 근처에서 약화 (데크가 더 부드러운 gradient 로 두꺼워짐).
- **이심률 구동 계절 사이클.** 123 일 궤도에 걸쳐 가시 디스크가 밝기
  ~10–15% 변조 — 근일점 근처에서 가장 밝음 (더 얇은 구름 데크에서의
  더 많은 반사광 + 더 가까운 기하학) 원일점 근처에서 가장 어두움.
  cfg 는 이를 궤도 위상에 묶인 느린 ~123 일 밝기 펄세이션으로 인코딩
  가능.
- **Limb haze.** H/He 상부 대기에서 λ ≲ 0.5 μm 의 옅은 청 Rayleigh
  산란은 광화학 haze 담요가 더 얇기 때문에 c 보다 더 가시적. 높은
  위상각에서 특히 두드러지는 부드러운 cyan 고리를 terminator 에서
  디스크 주위에 추가.
- **야간면.** c 에서 반사된 자매 행성 빛 (작은 디스크, 내합 ~55 일
  마다) 과 b 에서 (매우 어둡고 멀음). 야간 구름-top 온도 285 K — 광학
  열복사에는 너무 차갑지만 중적외 (~10 μm) 에서 밝음.
- **하늘의 별.** 61 Vir 가 d 에서 0.108° 차지 — 평균 거리에서 지구에서
  본 태양 각 크기의 약 5 분의 1. 근일점에서 ~0.166° 로 커지고 원일점
  에서 ~0.080° 로 줄어듦. 구름 데크를 통해 또렷한 디스크가 아닌 흩어진
  따뜻한-노란 patch (`#fff2dc` cfg-인코딩 호스트 색조) 로 보임. 표면
  조명은 대기 상단에서 지구의 ~3.6 배 (평균), 근일점의 ~8.6 배부터
  원일점의 ~2.0 배까지.
- **하늘의 자매 행성.** c (다음 안쪽 0.22 AU) 가 외합 시 각 크기 ~0.05°
  로, 내합 시 (55 일마다) ~0.1° 로 등장. b (0.05 AU) 는 훨씬 작고
  (최대 elongation 에서 ~0.01°) d 의 시점에서 항상 보이지는 않음.
  거의 동일 평면 기하학. 합은 시스템 내부 관측자에게 sky 이벤트.
- **선택적 계절 애니메이션.** 궤도 위상과 동기화된 123 일 궤도에 걸친
  구름-데크 밝기와 띠 대비의 느린 변조가 이심률 구동 계절 사이클을
  충실하게 렌더링해 줌. b 나 c 보다 우선순위 높은 Phase 3.5 시각
  디테일. d 의 계절 swing 이 시각적으로 알아챌 정도로 충분히 큼.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Vogt S. S. et al. 2010** — *A Super-Earth and Two Neptunes
  Orbiting the Nearby Sun-Like Star 61 Virginis*, ApJ 708, 1366
  (`2010ApJ...708.1366V`). 발견 논문. d 의 궤도 (P=123.01 d,
  a=0.476 AU, e=0.35, ω=314°) 와 최소 질량 (Msini = 22.9 ± 2.6 M⊕)
  보고. HIRES + AAT 결합 RV 해. Decisions 표의 모든 궤도 + 질량 값이
  여기에 묶입니다.
- **Owen J. E. & Wu Y. 2017** — *The evaporation valley in the
  Kepler planets*, ApJ 847, 29 (`2017ApJ...847...29O`, [arXiv:1705.10810](https://arxiv.org/abs/1705.10810)).
  광증발-valley 물리. d 를 손실 경계 한참 바깥에 위치 (XUV 구동 손실이
  6 Gyr 에 걸쳐 외피의 ~10⁻³). high 신뢰도로 `atmosphere_present = true`
  의 anchor.
- **Lopez E. D. & Fortney J. J. 2014** — *Understanding the
  mass-radius relation for sub-Neptunes*, ApJ 792, 1
  (`2014ApJ...792....1L`, [arXiv:1311.0329](https://arxiv.org/abs/1311.0329)). sub-Neptune envelope
  mass-radius 스케일링. 5–8% H/He 외피 23 M⊕ 에서 R = 4.5–5.5 R⊕. cfg
  는 5.0 R⊕ 채택. `radius_rearth` tie-break 의 anchor.
- **Howe A. R. et al. 2014** — *Mass-radius relations and core-envelope
  decompositions of super-Earths and sub-Neptunes*, ApJ 787, 173
  (`2014ApJ...787..173H`). sub-Neptune mass-radius
  다양성. H/He 외피 canonical 해석을 지지하고 Hycean / 물-풍부 대안의
  경계를 정함.
- **Madhusudhan N. 2012** — *C/O ratio as a dimension for
  characterizing exoplanetary atmospheres*, ApJ 758, 36
  (`2012ApJ...758...36M`, [arXiv:1209.2412](https://arxiv.org/abs/1209.2412)). sub-Neptune 원시-외피 조성
  baseline. H/He 일차 + 미량 응결 조성을 견인.
- **Madhusudhan N. et al. 2021** — *Habitability and biosignatures of
  Hycean worlds*, ApJ 918, 1 (`2021ApJ...918....1M`, [arXiv:2108.10888](https://arxiv.org/abs/2108.10888)).
  Hycean 등급 정의. d 의 평균 T_eq 가 Hycean 윈도우의 안쪽 가장자리에
  위치. Open-items Hycean variant 를 견인.
- **Moses J. I. et al. 2013** — *Compositional diversity in the
  atmospheres of hot Neptunes*, ApJ 777, 34 (`2013ApJ...777...34M`,
  [arXiv:1306.5178](https://arxiv.org/abs/1306.5178)). sub-Neptune 광화학. d 의 더 차가운 성층권에서의
  CH₄/HCN/광화학-haze 사슬을 정보화.
- **Morley C. V. et al. 2015** — *Thermal emission and reflected
  light spectra of super Earths with flat transmission spectra*, ApJ
  815, 110 (`2015ApJ...815..110M`, [arXiv:1511.01492](https://arxiv.org/abs/1511.01492)). Haze 가 낀
  sub-Neptune 검색 프레임워크. c (더 따뜻) 와 d (더 차가움) 사이의 haze
  두께 스케일링을 정보화.
- **Lavvas P. & Koskinen T. 2017** — *Aerosol properties of the
  atmospheres of extrasolar giant planets*, ApJ 847, 32
  (`2017ApJ...847...32L`, [arXiv:1707.08077](https://arxiv.org/abs/1707.08077)). sub-Neptune 광화학 haze
  생성 메커니즘. d 의 더 얇은 haze 층을 지지.
- **Showman A. P. et al. 2009** — *Atmospheric circulation of hot
  Jupiters: coupled radiative-dynamical GCM*, ApJ 699, 564
  (`2009ApJ...699..564S`, [arXiv:0809.2089](https://arxiv.org/abs/0809.2089)). 조석 영향을 받는 가스 행성
  의 super-rotating 적도 jet 을 확립. d 의 `cloud_morphology` (zonal
  banding) 를 정보화.
- **Lewis N. K. et al. 2014** — *GCMs of warm sub-Neptunes*, ApJ 795,
  150 (`2014ApJ...795..150L`, [arXiv:1410.0008](https://arxiv.org/abs/1410.0008)). 차가운 sub-Neptune
  영역에 대한 GCM 스케일링. d 의 더 긴 자전 주기에서 pseudo-synchronous
  spin 과 더 약한 적도-jet 순환을 지지.
- **Hut P. 1981** — *Tidal evolution in close binary systems*, A&A
  99, 126 (`1981A&A....99..126H`). 이심 궤도의 pseudo-synchronous spin
  평형. e=0.35 의 d 의 spin 상태에 대한 기초 인용.
- **Henning W. G. & Hurford T. 2014** — *Tidal heating in multilayered
  terrestrial exoplanets*, ApJ 789, 30 (`2014ApJ...789...30H`,
  [arXiv:1311.5904](https://arxiv.org/abs/1311.5904)). sub-Neptune 조석 가열 + spin-lock 시간 스케일.
  d 의 파라미터에서 ~5–15 Gyr 제공 (시스템 나이 초과).
- **Bolmont E. et al. 2020** — *Tidal dissipation and obliquity
  evolution* (`2020A&A...644A.165B`). d 의 조석-가열
  flux 스케일링 제공 (0.005–0.05 W/m²).
- **Lewis J. S. 1969** — *The clouds of Jupiter and the NH₃-H₂O and
  NH₃-H₂S systems*, Icarus 10, 365. sub-Neptune 구름 응결 시퀀스에
  대한 기초 열화학. d 의 T_eq 에서 H₂O / NH₃ / NH₄SH 층화 제공.

### Read (context / methodology, not decision-driving)

- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age
  Estimation for Solar-Type Dwarfs* (`2008ApJ...687.1264M`,
  [arXiv:0807.1686](https://arxiv.org/abs/0807.1686)). 호스트 합성에서 상속. 61 Vir 나이 6.1 ± 1.7 Gyr.
  광증발 진화 시간 스케일을 결정.
- **Pavlenko Y. V. et al. 2012** — *Solar twin candidates*
  (`2012MNRAS.422..542P`, [arXiv:1112.0590](https://arxiv.org/abs/1112.0590)). 호스트 합성에서 상속.
  광화학-haze 모델을 위한 솔라 트윈 SED 확인.
- **Fulton B. J. et al. 2017** — *The California-Kepler Survey III.
  A Gap in the Radius Distribution of Small Planets*, AJ 154, 109
  (`2017AJ....154..109F`, [arXiv:1703.10375](https://arxiv.org/abs/1703.10375)). 반지름 valley 인구.
  d 의 23 M⊕ 인구에 대한 H/He 외피 canonical 해석을 지지.
- **Wyatt M. C. et al. 2012** — *Herschel imaging of 61 Vir*
  (`2012MNRAS.424.1206W`, [arXiv:1204.6063](https://arxiv.org/abs/1204.6063)). 호스트 합성에서 상속. 간략
  히 인용. 30 AU 의 차가운 debris 고리는 0.48 AU 의 d 와 동역학적으로
  상호작용하지 않음 (d 는 고리 안쪽 가장자리 한참 안에 위치).
- **Kreidberg L. et al. 2014** — *Clouds in the atmosphere of the
  super-Earth exoplanet GJ 1214 b*, Nature 505, 69
  (`2014Natur.505...69K`, [arXiv:1401.0022](https://arxiv.org/abs/1401.0022)). featureless sub-Neptune
  투과 스펙트럼 참조. d 의 파라미터에서의 전역 구름 덮임 기대를 정보화.

### Read (instrument-only, not visual-informative)

- **Marcy G. W. et al. 2014** — Kepler 슈퍼지구 통계 맥락.

### Not read — no arXiv preprint or low-priority (~10 papers)

d 특정 arXiv 기록은 작습니다. 읽지 않은 집합은 주로 다음과 같습니다.

- **Vogt 2010 시스템의 동역학 안정성 follow-up.** d 의 e=0.35 는 세-행성
  사슬에서 가장 동역학적으로 활성 요소이지만, 시스템은 Vogt 2010 의
  해 안에서 안정.
- **트랜짓 탐색 non-detection.** d 가 트랜짓하지 않음을 확인. e=0.35,
  a=0.48 AU 에서 d 의 기하학적 트랜짓 확률은 ~0.6% 이므로 non-detection
  은 무작위 경사와 일관.
- **61 Vir 특정 항성풍 모델 없이 일반 광증발율 계산.**

## Open items for follow-up

- **직접 영상에서의 진질량과 반지름.** d 의 질량은 Msini 전용이고
  반지름은 mass-radius 스케일링 추정치. 미래의 직접 영상 캠페인이
  반사광 검출에서 진질량 + 반지름을 산출. HabEx / LUVOIR 시대 관측.
  d 는 호스트로부터 가장 큰 각 분리 (최대 elongation 에서 ~57 mas)
  때문에 직접 영상에 가장 유리한 61 Vir 행성.
- **Cfg variant. Hycean / 물-세계 외피.** d 의 평균 T_eq ~ 351 K
  (Madhusudhan 2021 Hycean 윈도우의 안쪽 가장자리에 가까움) 에서 얇은
  H₂ 대기를 가진 물-풍부 외피는 H/He 일차 외피와 관측적으로 일관.
  e=0.35 궤도가 d 를 근일점에서 T_eq ~ 476 K (1 bar 의 액체 물 안정
  한계 한참 위) 까지 데려가, Hycean 해석을 불리하게 만들지만 배제하지는
  않음. cfg variant 는 d 를 더 밀도 높고 덜 haze 가 낀, 더 깊은-청 ocean-
  세계 디스크로 렌더링하며 근일점에서 촉발되는 주기적 폭풍을 가짐.
  Phase 3.5 대안으로 명시.
- **Cfg variant. 암석 외피-없음 대안.** 광증발 물리가 외피 보유를 강하게
  선호하지만 (6 Gyr 에 걸쳐 손실 < 0.1%), 순수 암석 23 M⊕ 행성
  (R ≈ 2.7 R⊕. 밀도 ~6.5 g/cc) 의 작은 잔여 확률 남아 있음. 렌더는 더
  차가운 암석 세계 — haze 덮인 canonical 해석과 시각적으로 구분. cfg
  variant 로 보존.
- **Cfg variant. 더 강한 계절 폭풍 시스템.** d 의 e=0.35 가 61 Vir
  시스템 최대인 4.3× 일사 변조를 구동. d 특정 이심률에 표적된 GCM
  시뮬레이션이 이것이 정적 구름-띠 렌더링 너머의 추가 시각 디테일을
  요구하는 일시적 폭풍 feature (사이클론, 적도 overshooting) 를 구동
  하는지 제약 가능. Phase 3.5 정밀화.
- **미래 직접 영상 분광.** d 가 트랜짓하지 않지만 미래의 직접-영상
  분광이 구름-top 조성을 분해할 수 있음. 정밀화 기회. H₂O/CH₄/NH₃
  풍부도, haze 광학 깊이, 더 깊은 구름 조성 (물-얼음 vs NH₃-얼음 vs
  NH₄SH).
- **대기 탈출율 교차 점검.** Owen & Wu 2017 일반 스케일링이 d 를 이미
  무시 가능한 손실로 위치시킴. 61 Vir 특정 항성풍 + XUV 모델 (Vidotto
  스타일) 이 외피-보유 결론의 정성적 의미를 바꾸지 않으면서 확인.

## Related

- [61-vir](61-vir.md) — 호스트 별 Phase 3 합성.
- [61-vir-b](61-vir-b.md) — 가장 안쪽 자매 뜨거운 슈퍼지구. 0.05 AU.
- [61-vir-c](61-vir-c.md) — 중간 자매 sub-Neptune. 0.22 AU (더 따뜻한 아날로그).
- [methodology](../reference/methodology.md) — Decisions 스키마.
