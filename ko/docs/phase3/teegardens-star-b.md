<!-- Teegarden's Star b Phase 3 합성. cfg-ready 결정과 근거 -->
# 티가든의 별 b — Phase 3 합성

티가든의 별 b 는 최소질량 1.16 M⊕ (Fujii 2026 이 채택한 중앙값 i = 60°
기하학적 경사에서 실제 질량은 ~1.34 M⊕) 의 암석 행성으로, M7.0 V 모성
둘레를 4.91 일 주기로 공전합니다. 궤도 장반경 0.0259 AU 와 모성
볼로메트릭 광도 7.3 × 10⁻⁴ L☉ 가 결합되어 입사 플럭스 1.08 ± 0.08 S⊕ 가
나옵니다. 지구보다 약간 강한 셈으로, b 를 보수적 거주가능 영역의 안쪽
가장자리에 위치시킵니다. Bond 알베도 0.3 의 평형 온도는 277 ± 5 K
(Dreizler 2024), 알베도 0 이면 ~280 K (Fujii 2026 기준값) 입니다. 두 값
모두 물의 어는 점을 끼고 있어, b 는 질량과 입사 플럭스 기준만으로도
NearStars 카탈로그에서 가장 진짜 지구-아날로그에 가까운 후보 중
하나입니다 (ESI 0.90, Dreizler 2024).

이 행성은 통과 관측되지 않으므로 질량과 반지름 모두 측정이 아니라 유도값
입니다. 질량은 다중 기기 RV 적합 (CARMENES + ESPRESSO + MAROON-X +
HPF, 야간 평균 355 회 측정, Dreizler 2024) 에서 나옵니다. cfg 의 반지름
1.05 R⊕ 는 DB 에 고정된 Zeng 2016 지구형 벌크 질량-반지름 값이며, 최근
GCM 논문들도 매우 비슷한 반지름을 채택합니다 (Boukrouche 2026 은 1.02
R⊕, Fujii 2026 은 1.1 R⊕). 질량은 최소 질량 (m sin i) 이므로 낮은 궤도
경사에서는 실제 질량-반지름이 더 클 수 있지만, 1.16-1.34 M⊕ 범위에서
반지름 예측은 여러 질량-반지름 척도에 걸쳐 ~5 % 안에서 안정적입니다.

b 에 관한 cfg 결정적 질문은 **runaway vs habitable** 입니다. Boukrouche
2025 (arXiv:2510.11940) 는 Phase 2 권장 별 광도 (입사 플럭스 = 1481
W/m²) 에서 3-D GCM 을 돌려, 표면 알베도 α = 0.07 (해양) 과 α = 0.30
(육지) 모두에서 b 가 runaway 온실 임계값 아래에 머문다고 결론
지었습니다. 즉 현재 지구형 조성의 1 bar 대기는 지속 가능합니다. Dreizler
2024 의 대안 별 매개변수 (더 높은 입사 플럭스를 주는 Teff/R) 를 쓰면
값이 1565 W/m² 로 올라가고 같은 GCM 이 b 를 runaway 임계값 너머로
보냅니다. Phase 2 는 Schweitzer 2019 의 R = 0.107 R☉ 를 권장으로
선택했고, 이 합성은 그에 대응하는 **habitable** cfg 시나리오를 채택합니다.
이는 가장 최근 입사 플럭스 추정과 일치하는 고증-정합 선택입니다. Runaway
변형 cfg 는 Open items 에 보존됩니다.

**NearStars 시나리오 선택: 1 bar 지구형 N₂/O₂/CO₂ 대기를 가지고, 바다를
보유하며, 조석 고정된 "안구" 기하학에서 substellar 점 근처에 열린 물,
1-10 mbar 의 성층권 상부 구름층, 그리고 그 외 지역의 해빙을 특징으로 하는
온화한 aquaplanet.** 티가든 시스템의 대표 habitable cfg 입니다. (Dreizler
2024 별 매개변수 측면과 일치하는) 대안 runaway-Venus cfg 는 Open items 에
백업 변형으로 보존됩니다.

## Decisions

Kopernicus / atmosphere cfg-ready 값. `Confidence` 는 high = 직접
측정 또는 단단히 제약, medium = 강한 지지의 이론값, low = 허용 범위 내
미적 선택을 의미합니다.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | Wandel 2019 (Griessmeier 2009 시간척도); Boukrouche 2025/26 GCM 도 1:1 가정 |
| `obliquity_deg` | 0 | high | 조석 감쇠; Wandel 2019 |
| `eccentricity` | 0.03 | high | Dreizler 2024 (h,k 작음; +0.04/−0.02) |
| `argument_of_periastron_deg` | 338 | medium | Dreizler 2024 (낮은 e 에서 약한 제약: +133/−100) |
| `sidereal_period_days` | 4.90634 | high | Dreizler 2024 |
| `semi_major_axis_au` | 0.0259 | high | Dreizler 2024 |
| `mass_mearth` | 1.16 (msini) | high | Dreizler 2024 — 다중 기기 RV |
| `mass_estimate_mearth_true` | 1.34 (기하학적 i ≈ 60°) | medium | Fujii 2026 §II.1 — 3D-GCM 기준 실제 질량으로 채택 |
| `radius_rearth` | 1.05 | medium | DB 고정 Zeng 2016 지구형 MR; GCM 논문은 1.02 (Boukrouche 2026) – 1.1 (Fujii 2026) 사용 |
| `surface_gravity_g_earth` | 1.05 | medium | 유도 = 1.16 / 1.05² = 1.05 (10.3 m/s²) |
| `density_g_cc` | 5.5 (지구형 가정) | low | 통과 없음; Zeng 2016 MR 에서 가정 (5.513·1.16/1.05³ ≈ 5.5) |
| `insolation_s_earth` | 1.08 | high | Dreizler 2024 (Phase 2 별 매개변수; = L/a²) |
| `equilibrium_temp_k` (A=0) | 280 | high | Fujii 2026 기준값 (알베도 0 의 T_eq) |
| `equilibrium_temp_k` (A=0.3) | 277 | high | Dreizler 2024 표 4 |
| `bond_albedo` | 0.30 | medium | 지구형; Boukrouche 2025 α_s=0.30 육지 사례를 cfg 표면 알베도 대용으로 사용 |
| `surface_temp_substellar_k` | 295 | medium | GCM 수준 지구형 추정 (Boukrouche 2025/26 1481 W/m² aquaplanet); 표에 명시된 값 아님 — Open items 참조 |
| `surface_temp_nightside_k` | 240 | medium | GCM 수준 야간측 cold-trap 추정 (Boukrouche 2025/26); 표에 명시된 값 아님 — Open items 참조 |
| `surface_temp_global_mean_k` | 280 | medium | 1481 W/m² 에서 runaway 임계값 아래로 habitable (Boukrouche 2025); GCM 수준 전 지구 평균 |
| `atmosphere_present` | true | medium | Tie-break: 직접 대기 검출 없음 (통과 없음); Wandel 2019 + Boukrouche 2025/26 GCM 지구형 시나리오 |
| `atmosphere_surface_pressure_pa` | 100 000 | medium | Tie-break: Boukrouche 2025/26 과 Fujii 2026 기준이 채택한 1 bar 지구형 |
| `atmosphere_composition` | N₂ 78%, O₂ 21% (광분해 비생물적), CO₂ 400 ppm, H₂O 0.1–1% 포화, Ar 0.5% | medium | Tie-break: Boukrouche 2026 의 명시적 지구형 조성 (N₂ 78.084%, O₂ 20.947%, CO₂ 400 ppmv, CH₄ 1 ppmv); 높은 M-왜성 XUV 하 H₂O 광분해에서 비생물적 O₂ 축적 |
| `atmosphere_scale_height_km` | 7.8 | medium | 유도: kT/μg 에서 T=280 K, μ=29, g=10.3 m/s² |
| `atmosphere_tint_rgb_hex` | `#5a3a40` (M7 V SED 가 더 빨강쪽으로 치우쳐 TRAPPIST-1 e 보다 더 어둑) | medium | Tie-break: 2904 K 조명 하 Rayleigh — M5.5V 보다도 단파장 플럭스 적음; 어둑한 청회보라 |
| `cloud_cover_fraction` | 0.55 | medium | Boukrouche 2026 Isca GCM — 1-10 mbar 의 상부 구름층 + 종단경계의 중고도 구름 |
| `cloud_morphology` | 주간측 1-10 mbar 의 성층권 상부 구름층; 종단경계의 200-500 mbar 중고도 고리에서 습한 공기가 응결 | medium | Boukrouche 2026 §III + Fig. 1-2 — 주간측 1-10 mbar 상부 구름층; substellar 습기가 종단경계 cold-trap 으로 이송 |
| `cloud_tint_rgb_hex` | `#c0a890` (M7 V 조명 하 빨강쪽으로 치우친 따뜻한 크림 — 물 구름) | medium | Tie-break: 물 구름 + 2904 K 조명; TRAPPIST-1 e 관례 일치 |
| `ocean_present` | true (substellar 열린 물 원반; 그 외 얼음) | medium | Tie-break: Boukrouche 2025 해양 알베도 사례 (α_s=0.07) — 주간측 열린 물 지속 가능 |
| `ocean_extent_substellar_radius_deg` | 45 | medium | Tie-break: GCM substellar 온대 반경 (명시 표는 없음); TRAPPIST-1 e 의 35° 보다 크게 — 입사 플럭스가 높기 때문 |
| `ocean_tint_rgb_hex` | `#1a2540` (희미한 빨강 별 아래 깊은 물 — 짙은 남색) | low | Tie-break: 깊은 바다 + M7 V 조명; TRAPPIST-1 e 관례 따름 |
| `surface_ice_caps` | substellar 열린 물 원반 바깥의 해빙 + 빙하 얼음; 표면의 ~50% | medium | GCM 수준 1481 W/m² 에서 substellar 로부터 ~45° 의 빙선 |
| `surface_tint_rgb_hex_primary` | `#d8d0c4` (M-왜성 조명 하 눈 / 해빙) | medium | 물 얼음 알베도 0.6-0.8 + 빨강쪽으로 치우친 조명; TRAPPIST-1 e 관례 일치 |
| `surface_tint_rgb_hex_accent` | `#8a6a48` (종단경계 산등성이의 노출된 암반) | low | 얇은 대기 + 얼음 흐름 기하학 |
| `surface_morphology` | substellar 로부터 ~45° 안의 바다; 고위도 / 고경도의 해빙 + 빙하 지형; 종단경계 압력 능선의 노출 암반 | medium | Boukrouche 2025/26 GCM; Pierrehumbert 2011 조석 고정 aquaplanet 템플릿 |
| `magnetic_field_present` | true (적당) | low | Tie-break: 직접 제약 없음; 조용한 오래된 M 왜성은 Wandel 2019 논거로 대기 보존 지지 |
| `magnetic_field_strength_microtesla_equator` | 25 | low | Tie-break: interesting-first; 측정 없음; 시각적 오로라 후크를 위해 지구형 장 가정 |
| `magnetic_dipole_tilt_deg` | 11 | low | Tie-break: 인식 가능한 오로라 기하학을 위한 지구형 11° |
| `magnetosphere_standoff_planet_radii` | 6 | low | Tie-break: TRAPPIST-1 e 의 Wang 2025 (5-9 R_p) 에서 스케일링, 티가든의 항성풍 램 압력이 TRAPPIST-1 보다 훨씬 약하므로 상향 조정 |
| `aurora_present` | true | medium | 대기 + 자기장 모두 상당; M-왜성 SEP 환경이 오로라 지원 |
| `aurora_color_primary_hex` | `#4DFF4D` | medium | Tie-break: N₂/O₂/CO₂ 대기에서 [OI] 557.7 nm 녹색 — 지구형 오로라 색 |
| `aurora_intensity_kR_typical` | 30 | medium | Tie-break: 지구의 10 kR 의 3 배 (조용한 별 + 적당한 장) — 티가든 플레어 빈도가 훨씬 낮아서 TRAPPIST-1 e 의 150 kR 보다 훨씬 낮음 |
| `radiation_belt_present` | true (약) | low | Tie-break: 닫힌 자기권 + 낮은 항성풍 램 압력 |
| `surface_radiation_dose_msv_yr` | 100 | low | Tie-break: 1 bar 대기 + 지구형 B-장 + 조용한 M7 V — 티가든의 항성 XUV 와 SEP 플럭스가 훨씬 약하므로 TRAPPIST-1 e 의 12 000 mSv/yr 보다 훨씬 낮음; 티가든 specific 한 Atri-style 발표 수치 없음 |
| `atmospheric_shielding_g_cm2` | 1000 | high | 1 bar 지구형 → ~1000 g/cm² 컬럼 |
| `star_apparent_angular_diameter_deg` | 2.20 | high | 유도: 2 × R★/a × (180/π) = 2 × 0.107×0.00465 / 0.0259 × 57.3 = 2.20° |
| `stellar_illumination_color_temp_k` | 2904 | high | Cifuentes 2020 |

## Surface synthesis

티가든 b 는 표준적인 모든 지표에서 시스템의 가장 거주가능 후보입니다.
세 가지 수렴하는 근거가 있습니다.

1. **입사 플럭스** S = 1.08 ± 0.08 S⊕ (Dreizler 2024) — 지구보다 약간
   높음. Phase 2 권장 별 매개변수에서는 1481 W/m² 의 입사 플럭스에
   해당합니다. Boukrouche 2025 (현재 지구의 대기 조성을 가진 3-D GCM)
   는 1481 W/m² 에서 b 가 해양 (α_s = 0.07) 과 육지 (α_s = 0.30) 표면
   알베도 모두에 대해 runaway 온실 임계값 아래에 머문다고 명시적으로
   결론짓습니다. 대안 1565 W/m² 시나리오 (Dreizler 2024 대안 별
   매개변수 사용) 는 runaway 에 빠지지만, Phase 2 는 더 낮은 광도의
   Schweitzer / Cifuentes 해를 선호합니다.

2. **질량과 벌크 밀도.** m sin i = 1.16 M⊕ 와 Zeng 2016 지구형
   반지름 1.05 R⊕ 가정에서 추정된 벌크 밀도는 ~5.5 g/cc 입니다. 지구형
   이며, 미세하지 않은 물 저장소를 가진 규산염-철 암석 내부와 일치합니다.
   표면 중력은 ~1.05 g⊕ (10.3 m/s²) 입니다. 중앙값 i = 60° 기하학적
   경사에서 실제 질량은 ~1.34 M⊕ (Fujii 2026) 이며, 반지름 예측은 ~5 %
   이상 바뀌지 않습니다.

3. **이론적 거주가능성.** Wandel 2019 (arXiv:1906.07704) 는 1D 기후-
   거주가능성 모델을 적용해 S ≈ 1.15 S⊕ 의 b 에 대해 f = 0.5 (적당한
   대기 순환) 에서 habitable 대기 가열 범위가 H_atm = 0.32 ~ 3.7 임을
   찾습니다. 즉 sub-Mars 온실에서 상당한 CO₂ 증강까지 폭넓습니다.
   지구형 대기 (H_atm ≈ 1) 는 이 범위 안에 편안히 들어옵니다.

표면 형태론에서는 조석 고정 aquaplanet 템플릿 (Pierrehumbert 2011, Hu &
Yang 2014, Boukrouche 2025/26 GCM 으로 여기에 적용) 이 TRAPPIST-1 e
아날로그보다 약간 더 따뜻한 "안구 지구" 패턴을 줍니다.

- **substellar 온대** (substellar 점에서 ≤ 45°): α_s = 0.07 사례에서
  열린 바다. substellar 표면 온도는 ~295 K 이고 빙선에서 ~265 K 로
  떨어집니다. TRAPPIST-1 e 의 35° 보다 ~10° 큰 온대 반경은 티가든 b 가
  1.6 배 더 많은 입사 플럭스를 받기 때문입니다.
- **중위도 / 중경도** (substellar 에서 45-90°): 빙선의 수 미터에서
  종단경계의 수십 미터에 이르는 해빙.
- **종단경계와 야간측** (substellar 에서 >90°): 얼어붙은 바다 기질 위
  의 두꺼운 빙하 얼음; 표면 온도 ~240 K (GCM 야간측 cold-trap).

**색조 선택.** TRAPPIST-1 e 와 동일합니다. 물 얼음 알베도는 본질적으로
0.6-0.8 이고 푸르스름한 흰색이지만, 2904 K M7 V 조명이 인지되는 색조를
빨강-주황 쪽으로 크게 옮깁니다. 결합되면 얼음 피복은 따뜻한 크림화이트
(`#d8d0c4`), 깊은 바다는 짙은 남보라 (`#1a2540`) 가 됩니다. substellar
영역은 가장 시각적으로 두드러진 특징입니다 — 어두운 "동공" 같은 열린 물이
프랙탈 해빙 전이 띠로 둘러싸이고, 그 바깥은 균일한 빙하 얼음입니다.

**노출된 암반.** 제한적 (~5-10% 표면적). 암반 노출은 빙하 흐름이 압력
능선 위의 얼음을 얇게 만든 종단경계와, 작은 지각 융기로 영원히 빨강 색조
의 조명 아래 어두운 마픽 지각이 드러난 곳에 집중됩니다. 액센트 색조
`#8a6a48` 는 M7 V 빛 아래 풍화 현무암으로 읽힙니다.

## Atmosphere synthesis

cfg 는 Boukrouche 2025 Isca GCM 과 Boukrouche 2026 (LIFE 반구 논문)
을 따라 **1 bar N₂ 지배 aquaplanet 대기** 를 채택합니다. Boukrouche
2026 Isca 런에서 사용된 명시적 조성은 본질적으로 현재 지구입니다.

- **압력** 1 bar (100 kPa) — 지구형, Boukrouche 2025 에 따라 1481 W/m²
  에서 runaway 임계값 아래에서 지속 가능.
- **조성** N₂ 78.084%, O₂ 20.947% (비생물적 광분해 — cfg 는 생물권 없음
  가정; Lincowski 2018 류의 M-왜성 비생물적 O₂ 축적), CO₂ 400 ppmv (지구
  현대), CH₄ 1 ppmv 미량, H₂O 는 강수/증발 평형으로 결정, 그리고
  Boukrouche 2026 이 쓴 미량 CO/H₂.
- **구름.** Boukrouche 2026 Isca GCM (§III, Fig. 1-2) 은 주간측의 1-10
  mbar (지구에서는 성층권에 해당) 높이의 상부 구름층을 보여주며, 이
  구름층은 주간측 행성 알베도를 매우 작게 만들 만큼 광학적으로 얇습니다.
  전 지구 구름 피복 ~55%. 주간측 상부 구름층은 알베도를 지배하지 않습니다
  — 외부 장파 복사 패턴은 구름 피복 자체로 주로 결정되며, 그 아래 장은
  비습으로 결정됩니다. 이는 cfg 의 핵심 구분점입니다. TRAPPIST-1 e
  (중고도 층적운이 지배) 와 달리 b 의 주간측 구름 시그너처는 성층권에
  있습니다.

**하늘 모습.** 1 bar N₂ 대기는 단파장에서 지구형 Rayleigh 산란을 가지지만,
2904 K 모성 SED 는 0.5 μm 이하에서 플럭스가 거의 없습니다. 따라서 산란된
하늘 색은 어둡고 강하게 빨강-주황으로 치우칩니다. 천정 하늘은 어둑한
빨강-파랑 혼합 (~`#3a3040`), 지평선 근처에서 따뜻한 주황 (~`#a06040`)
으로 전이됩니다. 물 구름 특징은 빨강 별빛을 받는 따뜻한 크림 패치
(`#c0a890`) 로 보입니다.

모성은 시지름 2.20° 로 주간 하늘을 지배합니다 (지구에서 본 태양의 약
4 배, TRAPPIST-1 e 에서 본 TRAPPIST-1 과 비슷). substellar 점의 표면
조명은 약 1.08 × 지구의 볼로메트릭 플럭스 — 하지만 스펙트럼 피크가
근적외선에 있으므로 가시광 조명은 흐린 지구 오후에 더 가깝습니다.

**야간측.** 직접 별 조명 없음; 광원은 (a) 대기 순환으로 주간측에서 이송
된 산란광 (GCM 은 야간측 온도를 이송된 열로 ~240 K 유지함), (b) 결합 시
자매 행성 c 와 d 의 반사광 (~0.3° 시지름, m_v ≈ −8 ~ −10), 그리고 (c)
배경별 별빛입니다. 야간측 하늘은 어둡지만 완전히 어둡지는 않습니다 — KSP
야간측 환경광은 주간측의 ~3-5% 가 적절합니다.

**대기 손실.** 오래된 나이 (~7–8 Gyr) + 낮은 현재 XUV 플럭스 + 조용한
별이 티가든 b 의 대기 보존 전망을 프록시마 b 나 TRAPPIST-1 d 보다 훨씬
좋게 만듭니다. Wandel 2019 §3.1 은 Lammer 류의 침식 모델을 리뷰하고,
현재의 항성풍은 지구 질량 대기를 벗기기에 너무 약하다고 언급합니다. 초기
전-주계열 단계 (티가든 질량 같은 극저온 왜성에서 ~1 Gyr 지속) 는 더
뜨겁고 더 활동적이었고 모든 원시 H/He 외피를 벗겨냈을 수 있지만, 후기
accretion / 외기 방출로 획득된 무거운 원소 2차 대기는 살아남아야 합니다.
현재의 log(L_X/L_bol) = −4.9 는 상대적으로 높지만, 행성 위치에서의 절대
X선 플럭스는 지구 위치 태양 X선의 극히 일부에 불과합니다. Boukrouche GCM
은 대기 탈출을 포함하지 않으며 지구형 조성이 유지된다고 가정합니다.

**오로라** 는 존재하지만 차분한 시각 특징입니다. 1 bar 대기와 지구형
자기장 (tie-break 가정) 으로 b 는 정전적인 ~60° 자기 위도의 극지 오로라
타원을 지지해야 합니다. 티가든이 abiogenesis-zone 플레어 (≳10³⁵ erg) 를
기껏해야 2.4 년에 한 번만 만들고 (Dreizler 2024 SPECULOOS FFD), 그 외에는
후기 M 왜성치고 조용하기 때문에 (Fuhrmeister 2025 는 10²⁹–10³² erg 의
적당한 TESS 플레어만 보고), 오로라 강도는 TRAPPIST-1 e 의 150 kR 보다
훨씬 낮습니다. cfg 는 30 kR (지구 전형 10 kR 의 3 배) 를 채택해, 인지
가능하지만 절제된 오로라 팔레트를 줍니다. 지배적 방출은 [OI] 557.7 nm
녹색 (지구형 색 `#4DFF4D`), 약한 N₂⁺ 391.4 nm 보라 성분이 보조합니다.

## Rotation & spin synthesis

~7–8 Gyr 에 걸친 4.91 일 주기의 조석 감쇠는 명백하게 동기 (1:1) 자전을
확립합니다 (Griessmeier 2009 시간척도가 이 궤도 거리와 질량에서 8 Gyr
보다 훨씬 짧음). 자전축 기울기는 0 으로 감쇠. 이심률 0.03 (Dreizler 2024)
은 3:2 스핀-궤도 공명에는 너무 낮습니다 (Vinson 2017).

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 4.90634 일 (423 668 s).
Kopernicus `rotationPeriod` 는 궤도 `period` (초) 와 일치해야 합니다.

**대기 순환 체제.** 이 부류의 조석 고정 GCM 들은 모두 적도 초회전을
찾습니다. substellar 주간측의 정적 열 강제력으로 구동되는 단일 광폭
순방향 동서 제트입니다. Hammond 2025 (ExoCAM, 자매 행성 c 용) 은
초회전 제트와 행성 규모의 Matsuno-Gill 패턴을 명시적으로 보여주며, 주간측
구름 장이 substellar 점 동쪽으로 이동합니다. Fujii 2026 (ROCKE-3D, b 용)
도 마찬가지로 substellar 구름 덱이 동쪽으로 늘어남을 찾습니다. b 에 대한
Boukrouche 2026 Isca GCM 은 이 그림과 정합적입니다 — 상부 구름층이
주간측에 자리 잡고 외부 장파 패턴을 구동합니다. b 는 동역학 위상도
(Haqq-Misra 2018) 의 "초회전" 측에 완전히 있는데, b 가 TRAPPIST-1 e 보다
더 뜨겁기 때문입니다 (1.08 대 0.66 S⊕).

**계절 없음.** 자전축 기울기 = 0; libration 유발 입사 플럭스 변동 < 0.3%.
substellar 점과 그 열린 물 원반은 표면 좌표계에서 고정.

**자기 다이나모.** b 의 질량 (1.16-1.34 M⊕) 과 가능한 활성 내부 (지구형
가정) 는 동기 4.91 일 자전에도 불구하고 지속적인 다이나모를 지지해야
합니다. 다이나모는 표면 자전이 아니라 핵 대류로 구동되며, 지구의 27 일
달-유도 동기 자전 사고 실험은 이론적으로 다이나모를 유지합니다. cfg 는
따라서 적당한 지구형 장 (25 μT 적도 표면) 을 interesting-first tie-break
으로 선택해, 플레이어 항법용 가시 오로라 구조를 줍니다.

## Visual styling

표면과 대기 결정을 결합하면, b 는 TRAPPIST-1 e 의 약간 더 따뜻한 사촌
으로 렌더링됩니다.

- **궤도에서 본 전체 모습.** substellar 에서 ~45° 의 따뜻한 크림 색
  열린 물 "동공" 을 가진 눈덩이가 프랙탈 해빙 전이 띠로 둘러싸이고,
  그 바깥은 전체적으로 흰-크림 빙하 얼음. 성층권 상부 구름층 (1-10
  mbar) 이 substellar 대비를 부드럽게 하는 높고 얇은 균일한 안개를
  만듭니다 — 구름 특징이 TRAPPIST-1 e 의 중고도 층적운보다 더 흩어져
  보입니다.
- **substellar 원반 (열린 물).** 강렬한 빨강-주황 조명 아래의 짙은 남색
  바다 (`#1a2540`) 에 따뜻한 크림 권운 등가물 구름 (`#c0a890`) 이 점점이.
  substellar 온대가 행성의 가장 시각적으로 두드러진 특징입니다.
- **얼음 전이 띠.** 따뜻한 크림 (`#d8d0c4`) 얼음과 짙은 바다 (`#1a2540`)
  의 프랙탈 패턴 — 열린 leads 가 있는 깨진 해빙. 전이 반경은 substellar
  로부터 ~45°.
- **빙하 얼음 영역.** 매끄러운 따뜻한 크림 (`#d8d0c4`) 에 빙하 흐름이
  암반과 만나는 곳의 미묘한 지형적 기복. 종단경계는 비스듬한 조명에서
  가장 밝은 영역 — 긴 그림자가 압력 능선과 크레바스를 드러내고, 여기에
  액센트 `#8a6a48` 노출 암반이 사이로 보입니다.
- **야간측.** 이송된 대기 열 재분배 온기 덕분에 어렴풋이 보임 (주간측의
  ~3-5%). 가시 특징: 압력 능선, 균열, 다시 얼어붙은 leads, ~60° 자기
  위도의 희미한 오로라 타원.
- **대기 안개.** 약 12-20 km 두께의 옅은 회청보라 림 빛 (`#5a3a40`) —
  Rayleigh 산란된 M7 V 빛. M-왜성 SED 가 산란할 단파장 플럭스가 적어서
  지구의 파란 림보다 훨씬 흐립니다.
- **하늘의 별.** 티가든의 별은 b 의 하늘에서 2.20° 시지름 (지구에서 본
  태양의 4 배) — 짙은 빨강-주황 원반 (`#b03020`) 으로 보이며 TRAPPIST-1
  e 에서 본 TRAPPIST-1 의 시지름과 비슷합니다. 조명은 substellar 에서
  "영원한 일몰" 이며, 종단경계로 가면서 황혼과 완전한 밤으로 사라집니다.
- **하늘의 자매 행성.** c 가 결합에서 (~0.3° 시지름, m_v ≈ −8); d 가
  결합에서 (~0.2°, m_v ≈ −5). c 와는 6-10 일마다, d 와는 ~26 일마다
  결합. RV 증거 (Dreizler 2024 동역학 안정성 분석) 로 거의 공면.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Zechmeister M. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Two temperate Earth-mass planet candidates around
  Teegarden's Star*, A&A 627, A49 (`2019A&A...627A..49Z`,
  arXiv:1906.07196). b 와 c 의 발견. 초기 질량과 궤도.
- **Dreizler S. et al. 2024** — *Teegarden's Star revisited*, A&A 684,
  A117 (`2024A&A...684A.117D`, arXiv:2402.00923). 정밀화된 b 궤도
  (P = 4.90634 d, e = 0.03, ω = 338°, msini = 1.16 M⊕, S = 1.08 S⊕,
  A=0.3 에서 T_eq = 277 K, ESI 0.90) 와 SPECULOOS 플레어 빈도 다이어그램.
- **Wandel A. & Tal-Or L. 2019** — *On the Habitability of Teegarden's
  Star planets*, ApJ 880, L21 (`2019ApJ...880L..21W`, arXiv:1906.07704).
  분석적 1D 거주가능성 모델 — f = 0.5 에서 b habitable 범위 H_atm =
  0.32-3.7; S(b) ≈ 1.15 S⊕.
- **Boukrouche R., Caballero R., Lewis N. T. 2025** — *Near the
  Runaway: The Climate and Habitability of Teegarden's Star b*
  (arXiv:2510.11940). 1481 W/m² 의 3-D GCM — α_s = 0.07 와 0.30
  양쪽에서 habitable; 1565 W/m² 는 runaway 너머. cfg 의 habitable
  시나리오 선택을 결정한 핵심 논문. (캐시는 초록만; 아래 표면 온도
  수치는 표에 명시된 값이 아니라 GCM 수준 추정.)
- **Boukrouche R., Caballero R., Janson M. 2024** — *The Impact of
  Water Clouds on the Prospective Emission Spectrum of Teegarden's
  Star b as Observed by LIFE* (arXiv:2411.07922). 1-D 물 구름 모델;
  ≥1 bar N₂ 에서 구름 피복 0–90% 시험 (Venus-아날로그 변형도 모델링).
  거주가능성 추적자로서의 구름 피복을 지지. (캐시는 초록만.)
- **Boukrouche R. & Janson M. 2026** — *Disentangling the Hemispheres
  of Teegarden's Star b with LIFE* (arXiv:2512.19231). Isca aquaplanet
  GCM 반구 지도; 명시적 지구형 조성; 1-10 mbar 의 상부 구름층 (§III
  verbatim); 1 bar 표면 압력, α_s 0.07.
- **Fujii Y. et al. 2026** — *Probing thermal gradients of habitable-
  zone rocky planets as an anti-indicator of a global surface ocean
  using direct imaging* (arXiv:2512.16575). 1 과 10 bar 의 b 에 대한
  ROCKE-3D 해양-vs-비해양 시나리오; i = 60° 의 실제 질량 1.34 M⊕ 와
  알베도 0 의 T_eq ≈ 280 K 기준값 제공; substellar 구름 덱이 동쪽으로
  늘어남.

### Read (context / methodology, not decision-driving)

- **Hammond T. et al. 2025** — *The climates and thermal emission
  spectra of prime nearby temperate rocky exoplanet targets*
  (arXiv:2504.00978). 티가든의 별 **c** (b 아님) 를 포함한 일곱 표적의
  ExoCAM GCM 격자; c 는 모든 pCO₂ 에서 완전히 얼음으로 덮인 눈덩이.
  b 로 외삽되는 초회전 / Matsuno-Gill / 동쪽 구름 동역학 체제에 사용.
  b 는 그들의 격자에 없습니다.
- **Schweitzer A. et al. 2019** — 별 매개변수 (arXiv:1904.03231), 모성
  통해 사용 (권장 해 R = 0.107 R☉).
- **Fuhrmeister B. et al. 2025** — *Coronal and chromospheric activity
  of Teegarden's star* (arXiv:2504.02338). 대기 보존을 위한 활동 맥락;
  10²⁹–10³² erg 의 TESS 플레어, 후기 M 왜성치고 낮은 전반적 활동.

### Read (instrument / non-cfg-decisive)

- **Mandell A. et al. 2022** — MIRECLE 미션 개념; PIE 맥락으로 인용.
- **Hill M. L. et al. 2023** — Catalog of Habitable Zone Exoplanets
  (`2023AJ....165...34H`, arXiv:2304.13417). 카탈로그-only 항목; b 는
  상위 랭크지만 측정값 추가 없음.

### Not read — no arXiv preprint or low-priority

b 의 참고문헌은 작습니다 (~14 개 논문, 9 개 arXiv). 다섯 개의 비-arXiv 논문은
카탈로그 항목이나 짧은 학회 절차들로, 모두 `docs/phase3/_bib/teegarden-s-
star-b.yaml` 에 적절한 곳에 `status: skipped` 로 보존됩니다.

## Open items for follow-up

- **runaway 임계값에 대한 별 매개변수 모호함** (핵심).
  Boukrouche 2025 는 1565 W/m² (Dreizler 2024 대안 별 매개변수) 에서 b
  가 runaway 온실 임계값 **너머** 라고 명시적으로 언급합니다. Phase 2 는
  더 낮은 광도의 Schweitzer 매개변수 (1481 W/m²) 를 선택해 b 를
  habitable 로 유지합니다. 미래의 별 매개변수 정밀화 (간섭계, JWST 차폐)
  가 Dreizler 의 더 큰 R 을 지지하면, cfg 는 **runaway Venus 아날로그
  변형** 으로 전환해야 합니다. 1-100 bar CO₂ 대기, 표면 물 없음, 뜨거운
  주간측 (~700 K), 두꺼운 황산 구름, 얼음 없음. 백업 변형으로 보존.
- **표면 온도 수치는 GCM 수준 추정**: substellar 295 K, 야간측 240 K,
  전 지구 평균 280 K 행은 Boukrouche 2025/26 의 1481 W/m² aquaplanet 과
  정합적이지만, 초록만 있는 Boukrouche 2025 캐시에는 표로 명시되어 있지
  않습니다. 전체 Boukrouche 2026 GCM 지도 (또는 Fujii 2026 ocean_Nc-6
  런) 가 확보되면 이 값들을 재적합해야 합니다.
- **낮은 경사에서의 실제 질량**: 궤도 경사가 60° 보다 훨씬 낮으면 실제
  질량은 1.5-3 M⊕ 가 될 수 있고 행성은 암석이 아니라 미니-Neptune 일
  수도 있습니다. Fujii 2026 은 1.34 M⊕ 추정을 위해 i = 60° (중앙값
  기하학적) 를 채택합니다. Gaia DR4 나 Theia 의 측성학적 검출이 경사를
  제약할 수 있습니다.
- **GCM 에 따른 구름 형태론**: Boukrouche 2026 의 Isca GCM 은 주간측
  방출 패턴을 지배하는 높은 성층권 구름층을 줍니다. Hammond 2025 의
  ExoCAM 은 자매 행성에 대해 중고도 구름을 줍니다. b 에 대한 미래 GCM
  intercomparison (THAI-style) 이 합의를 바꾸면 cfg 의 성층권 구름 선택
  도 이동할 수 있습니다.
- **통과 확인 없음**: 모든 행성 매개변수가 RV 유도. CHEOPS 의 통과
  검출이나 집중 TESS 재방문 (비-통과 기하학에서는 낮은 확률) 이 반지름
  을 직접 측정하고 대기 컬럼을 조여줄 것입니다.
- **오로라 강도 / 차폐**: cfg 의 30 kR 와 100 mSv/yr 수치는 활동 비율
  로 TRAPPIST-1 e 에서 스케일링한 것입니다. 티가든-specific SEP+대기
  모델 (Atri-style) 은 아직 없습니다.
- **자기장 강도**: 측정 없음. cfg 는 interesting-first 로 지구형 25 μT
  를 선택합니다. 더 약한 스케일링 (조석 고정 저질량 행성에 대한 RM22-
  style) 은 ~3 μT 와 더 약한 오로라를 줄 것입니다.

## Related

- [teegardens-star](teegardens-star.md) — M7 V 모성
- [teegardens-star-c](teegardens-star-c.md) — 바깥 자매, 눈덩이 후보
- [teegardens-star-d](teegardens-star-d.md) — 가장 바깥, HZ 밖
- [trappist-1-e](trappist-1-e.md) — 구조적으로 유사 (M-왜성 HZ aquaplanet); b 가 더 따뜻
- [proxima-cen-b](proxima-cen-b.md) — 직접 비교 대상; 프록시마 b 는 플레어 스트레스가 더 큼
- [methodology](../reference/methodology.md) — Decisions 스키마
- [rex-data-comparison](../reference/rex-data-comparison.md) — 티가든 b 는 HZ 카탈로그에서 가장 높은 ESI 행성 중 하나
