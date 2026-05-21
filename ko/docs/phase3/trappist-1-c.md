<!-- TRAPPIST-1 c Phase 3 synthesis: cfg-ready 결정과 근거 -->
# TRAPPIST-1 c — Phase 3 Synthesis

TRAPPIST-1 c 는 M8V ultra-cool dwarf 를 2.42 일 주기로 도는 1.10 R⊕,
1.31 M⊕ 암석 행성. 바깥쪽에서 두 번째 행성으로 지구의 2.27× insolation
을 받음. JWST MIRI 15 μm secondary-eclipse (Zieba 2023) 과 phase-curve
(Ducrot 2025) 측정이 dayside brightness 온도 369–380 K 를 제시 — 맨
암석 또는 얇은 O₂ 지배 대기 어느 쪽과도 일관. 10 bar (10 ppm CO₂) 부터
0.1 bar (순수 CO₂) 까지 cloud-free O₂/CO₂ 혼합은 배제; 황산 구름의
Venus-analog 은 2.6σ 에서 disfavor.

**NearStars 시나리오 선택. 미량 H₂O vapor 를 가진 얇은 O₂ 지배 대기
(~0.1 bar), 유의미한 CO₂ 없음, 어두운 basaltic 표면 위.** Luger & Barnes
2015 / Lincowski 2018 / Lincowski 2023 의 "fossil oxygen" 시나리오 채택.
초기 H₂O-rich 증기 대기가 어린 M-dwarf 의 high-luminosity pre-main-
sequence 페이즈 동안 hydrodynamic H escape 를 겪어 수소를 stripping
하고 광분해 O₂ 를 뒤에 남김. 남은 표면은 풍화됨 (b 의 신선한 ultramafic
과 달리), 성숙한 regolith. b (대기 없음, 신선함) 및 d (terminator H₂O
얼음 구름이 있는 얇은 대기) 와 구별되면서도 관측 일관성 유지.

## 결정

Kopernicus / atmosphere cfg-ready 값. `Confidence`. high = 직접 측정
또는 강하게 제약, medium = 강한 지지를 가진 이론, low = 허용 윈도우 내
미적 선택.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 2.42 d 궤도, 조석 damping; Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping; Agol 2021 |
| `eccentricity` | 0.00654 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 282 | medium | Agol 2021 (low ecc → 약한 제약) |
| `sidereal_period_days` | 2.4219 | high | Agol 2021 |
| `semi_major_axis_au` | 0.01580 | high | Agol 2021 |
| `mass_mearth` | 1.308 | high | Agol 2021 TTV |
| `radius_rearth` | 1.097 | high | Agol 2021 |
| `surface_gravity_g_earth` | 1.087 | high | derived = 1.308 / 1.097² |
| `density_g_cc` | 6.36 | high | derived; Agol 2021 은 ~5.7 보고 (불확실성 bar 겹침) |
| `insolation_s_earth` | 2.27 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 339 | high | Agol 2021 |
| `dayside_brightness_temp_k_15um` | 380 | high | Zieba 2023 MIRI F1500W eclipse |
| `dayside_brightness_temp_k_phase_curve` | 369 | high | Ducrot 2025 MIRI 15 μm phase curve |
| `bond_albedo` | 0.05 | medium | Ducrot 2025 에 의해 0 (맨 암석) 과 ~0.3 (반사적) 사이로 제약 |
| `atmosphere_present` | true (thin) | low | 채택된 O₂ 지배; (A) 대기 없음도 방어 가능 |
| `atmosphere_surface_pressure_pa` | 10 000 | medium | Lincowski 2023 의 1σ-consistent envelope 의 상단 가장자리에 0.1 bar O₂ |
| `atmosphere_composition` | O₂ 98%, 미량 H₂O / O₃ / CO₂ ≲100 ppm | medium | Lincowski 2018 광분해 산소 예측; Lincowski 2023 fit |
| `atmosphere_scale_height_km` | 10 | medium | derived. kT/μg with T≈370 K, μ=32 (O₂), g=10.7 m/s² |
| `atmosphere_tint_rgb_hex` | `#3a3a40` (매우 옅은 O₂ Rayleigh + 얇은 O₃ Chappuis 흡수) | low | 0.1 bar 에서 scattering 최소; O₃ 가 M-dwarf 조명 아래 약한 gray-blue tint 추가 |
| `dayside_surface_temp_k` | 369 | high | phase-curve 측정 brightness 와 일치 |
| `substellar_peak_temp_k` | 430 | medium | derived bare-surface subsolar (A=0.05, ε=1, 약한 advection) |
| `nightside_surface_temp_k` | 140 | medium | 얇은 O₂ 대기에서의 약한 advection; Ducrot 2025 nightside < ~150 K |
| `surface_tint_rgb_hex_primary` | `#2c2218` (풍화된 basalt) | medium | 노화된 basaltic 표면, 최근 화산 활동 없음; Mercury-mature regolith analog |
| `surface_tint_rgb_hex_accent` | `#604030` (산화철 patch, 광분해) | low | 장기 tidally-locked 표면의 UV 광분해; Turbet 2018 mechanism |
| `surface_morphology` | 풍화된 basaltic 평원; 노화된 충돌 분화구; 잔잔한 기복 | medium | 새로운 resurfacing 추론 안 됨 (b 와 달리); 누적 ~8 Gyr 충돌 |
| `surface_ice_caps` | substellar 에서 ≳60° 떨어진 좁은 띠의 nightside CO₂ / H₂O frost | medium | 얇은 대기가 미량 H₂O 운반 가능; nightside T < CO₂ frost point |
| `induction_heating_w_m2` | 0.05–0.5 | medium | Grayver 2022 — 더 먼 거리로 b 보다 낮음; 활발한 화산 활동에 부족 |
| `tidal_heating_w_m2` | 0.005–0.05 | medium | Bolmont 2020 — b 보다 ~10× 낮음 |
| `star_apparent_angular_diameter_deg` | 4.02 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## 표면 합성

c 의 eclipse + phase-curve 데이터는 맨 어두운 low-albedo 표면 또는
최소 CO₂ 의 얇은 O₂ 지배 대기 어느 쪽과도 일관 (Zieba 2023, Lincowski
2023, Ducrot 2025). b 의 경우 Ducrot 2024 가 신선한 ultramafic 표면의
model-consistency 논거를 발견했지만 — c 의 eclipse 데이터는 unweathered
표면을 요구하지 않음. 역 해석도 가능. c 의 표면은 c 가 tidal + induction
heating 이 더 적기 때문에 b 의 표면보다 상당히 노화됐을 수 있음
(Bolmont 2020 은 c 에서 tidal heating 이 ~10× 낮다고 추정하고, Grayver
2022 induction heating 도 같은 이유로 ~10× 낮음).

유의미한 resurfacing 없이 c 의 표면은 ~8 Gyr 의 충돌 폭격과 광화학적
풍화를 누적. 결과는 lunar highlands 또는 Mercury 의 intercrater 평원
(broadband visible albedo ≈ 0.06–0.10) 과 유사한 성숙한 어두운 low-
albedo 표면, 그러나 후기 충돌로 전달된 표면 휘발성 물질의 UV 광분해로
substellar 반구 근처에 농축된 산화철 patch 포함.

**색 선택.** M8V 조명 아래의 풍화된 basalt. 어두운 basaltic primary
`#2c2218` 는 풍화된 regolith 성숙도를 반영하기 위해 b 의 `#1a1612`
신선한 ultramafic 보다 약간 밝음. 산화철 accent `#604030` 은 b 보다
더 두드러짐. 이유는. (1) 표면이 더 노화되어 산화 시간이 더 있었고,
(2) 얇은 O₂ 대기가 연속적인 저수준 산화제 공급을 제공.

**모양.** 활발한 resurfacing 없음은 보존된 충돌 기록 의미. 모든 크기
범위의 명확한 분화구, lunar highlands 에 접근하는 saturation 밀도.
초기 100–500 Myr 페이즈의 마그마 바다 잔존 feature (Krissansen-Totton
2022, TRAPPIST-1 시스템 마그마 바다 진화 논문) 는 후기 충돌 분지와
구별되는 넓은 highland 영역으로 여전히 부분적으로 보일 것.

## 대기 합성

Zieba 2023 (MIRI F1500W secondary eclipse, 4회 방문) 이 15 μm 에서
Fp/F★ = 421 ± 94 ppm 측정. 이는 380 ± 31 K 의 dayside brightness 온도에
해당, low albedo 의 맨 암석 또는 얇은 low-greenhouse 대기와 일관. 데이터
배제.

- ≥10 ppm CO₂ 의 10 bar cloud-free 대기
- 유의미한 CO₂ 의 1 bar cloud-free 대기
- 0.1 bar 순수 CO₂ 대기
- 황산 구름의 Venus-analog 대기 (2.6σ)

Lincowski 2023 는 two-column climate-photochemistry coupled 모델을
사용해 더 넓은 대기 유형을 포함하도록 모델 공간 확장. 2σ 내에서.

- 0.1 bar 에서 낮은 CO₂ (≲100 ppm) 의 **얇은 O₂ 대기** 가 데이터와
  일관
- 1–10 bar O₂ + 100 ppm CO₂ at 2.0–2.2σ
- 1–10 bar O₂ + 최대 0.5% CO₂ at 2.9σ
- 최대 10% H₂O vapor 의 얇은 O₂ (1σ 내)

Ducrot 2025 phase-curve 가 케이스를 더 닫음. c 의 dayside 는 369 ± 23 K,
nightside 비검출 (15 μm 에서 ≲ 110 ppm), 유의미한 phase offset 없음.
맨 암석 또는 얇은 O₂ 둘 다 일관 유지.

NearStars 에서는 **0.1 bar O₂ 지배 얇은 대기** 채택.

- **압력** 0.1 bar (10 kPa). 낮은 CO₂ 의 O₂ 지배 조성에 대한 Lincowski
  2023 의 1σ 일관성 envelope 내.
- **조성** 은 O₂ 지배 (~98%), 미량 H₂O vapor (~1%) 와 광분해의 미량
  O₃ (~100 ppm). CO₂ 는 Zieba 2023 / Lincowski 2023 제약을 존중하기
  위해 매우 낮게 유지 (~100 ppm). O₂ 기원은 hydrodynamic-escape
  fossil. Luger & Barnes 2015 는 초기 TRAPPIST-1 세계의 H₂O 증기
  대기가 H 를 우주로 잃고 ~10 bar O₂ 를 남길 것이라 보임; 이후 광분해
  + 표면 산화가 이를 관측된 얇은 O₂ 잔재로 감소시킴.
- **구름 없음** canonical 상태에서. 얇은 O₂ 대기는 steady state 에서
  구름 형성에 충분한 물이 없고, CO₂ 는 CO₂-얼음 구름에 너무 낮음.

**하늘 외관.** 0.1 bar O₂ 대기는 약한 Rayleigh scattering 가짐 (지구의
1 bar N₂+O₂ 대비 0.5 μm 에서 약 5%). substellar 점 근처 하늘은 천정에서
옅게 dark-violet, stellar disk 가 밝은 limb 근처에서는 옅은 gray-orange
로 전환. nightside 쪽으로는 하늘이 본질적으로 검음. O₃ Chappuis 흡수
(0.6 μm 근처 피크) 가 dayside 산란광에 미묘한 회색 overtone 추가.
호스트 별이 4.02° 각 크기로 dayside 하늘 지배 (지구에서 본 태양 각
크기의 약 8배).

## 자전 & spin 합성

7.6 Gyr 에 걸친 2.42 일 주기의 c 에 대한 조석 damping 은 모호하지 않게
동기 (1:1) 구성을 확립. 황도 경사각은 0 으로 damping. eccentricity 는
0.00654 (Agol 2021) — 3:2 공명을 지지하기에는 너무 낮음 (Vinson 2017 은
3:2 가 e ≳ 0.01 에서만 안정적임을 발견).

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 2.4219 일 (209 254 s).
Kopernicus `rotationPeriod` 는 초 단위 궤도 `period` 와 일치해야 함.

**계절 없음.** 황도 경사각 = 0; libration 유도 insolation 변동 < 0.5%.
substellar 점은 표면 frame 에서 지질학적 시간 척도에 고정 (b 에서 지적된
느린 세차운동 modulo).

**Eccentricity 유도 조석 굴곡.** e = 0.00654 와 ultra-cool dwarf 호스트
로, 강제 libration 으로부터의 조석 가열 비율은 적당함 (Bolmont 2020.
c 에 대해 ~0.005–0.05 W/m²). 활발한 화산 활동을 구동하기에 불충분;
"풍화된 표면" 추론과 일관.

## 비주얼 스타일

표면과 대기 결정 결합.

- **전역 색 팔레트.** 어두운 풍화된 basalt body (`#2c2218` primary,
  `#604030` accent) 가 강렬한 적-오렌지 별빛 아래 → substellar 반구
  쪽으로 편향된 미묘한 산화철 banding 의 깊은 brown-charcoal 세계로
  나타남. 얇은 O₂ 대기는 옅은 limb haze 외에는 궤도에서 본질적으로
  보이지 않음.
- **Dayside.** Substellar 영역 (~430 K subsolar 피크, ~370 K 일반
  dayside) 의 산화철 patch 가 substellar 점 30° 이내에서 가장 강함.
  잔잔한 지형 기복 — 성숙한 충돌 cratering, 활발한 화산 활동 없음.
  nightside 로의 열 재분배는 약하지만 0 이 아님 (얇은 O₂ 대기로 인해
  ~140 K nightside floor).
- **Terminator band.** 2566 K 비스듬한 빛 아래의 적당한 지형 그림자
  대비. 낮은 태양 천정각에서 옅은 limb glow 로 보이는 high-altitude
  옅은 gray Rayleigh-산란 haze 가능.
- **Nightside.** 차가움 (~140 K) 하고 어두움. substellar 에서 ≳60°
  떨어진 좁은 띠에 CO₂/H₂O frost 가능; 자매 행성에서 반사된 빛 아래
  옅은 더 밝은 patch 로 나타남. visible 대역에서 열적외 emission 만.
  KSP nightside ambient ≈ dayside 의 5–10%.
- **Atmosphere haze.** 얇은 옅은 gray-violet limb haze (`#3a3a40`),
  3–8 km 두께, 행성 limb 의 우주 배경에서만 보임.
- **하늘의 별.** TRAPPIST-1 이 c 의 하늘에서 4.02° 차지 (지구에서 본
  태양의 8배). 색 `#ff7a1a` (2566 K). 표면 밝기 ~2.27 S⊕ (지구 궤도
  에서의 Venus insolation 과 유사). flare 활동은 b 와 동일 — 가끔
  두드러진 IR flare.
- **하늘의 자매 행성.** b (다음 안쪽) 가 inferior conjunction 시 ~0.6°
  로 나타남; d (다음 바깥쪽) 가 4–6 일마다 conjunction 시 ~0.5°.
  Agol 2021 에서 거의 동일 평면 geometry.

## 참고 문헌

### 읽음 (시각-정보 제공, 위 결정 견인)

- **2306.10150** Zieba 2023 — c 의 JWST/MIRI F1500W secondary eclipse.
  Fp/F★ = 421 ± 94 ppm, dayside T ≈ 380 K. Venus-analog 와 대부분의
  CO₂-rich 대기 배제. c 의 대기 상한에 대한 발견 논문.
- **2308.05899** Lincowski 2023 — two-column climate+photochemistry
  사용한 c 의 더 넓은 대기 탐색. 얇은 O₂ 낮은 CO₂ 대기가 1σ 내에서
  일관 발견. 채택된 O₂ 지배 시나리오 견인.
- **2509.02128** Ducrot 2025 — b 와 c 의 MIRI 15 μm phase curve.
  c dayside 369 ± 23 K, nightside 비검출. 대기 시나리오 공간을 맨
  암석 / 얇은 O₂ 쪽으로 닫음.
- **2305.01250** Acuña 2023 — 내부-대기 모델링. c 가 맨 표면일
  가능성이 가장 높지만 얇은 대기를 배제할 수 없음 발견. Lincowski
  2023 가 해결한 표면-대기 degeneracy 지지.
- **2412.11987** Nicholls 2024 — lava-world 대기의 convective shutdown.
  c 를 케이스 스터디로 사용; non-convective 대기 아래에서 마그마
  바다가 지속될 수 있을 때 탐색. "풍화된 표면" vs. "신선한 ultramafic"
  선택 알림 (c 는 풍화 쪽에 위치).

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **2412.16541** back-to-back b/c transit 사용한 stellar contamination
  보정. 모든 TRAPPIST-1 transmission 에 관련된 방법론; 직접 시각
  정보는 아님.
- **2412.11627** Ducrot 2024 — b 의 결합 12.8+15 μm eclipse 분석. 맨
  암석 vs. CO₂-haze 해석이 c 의 옵션과 평행하기 때문에 여기 언급.
- **2507.02052** JWST MIRI 15 μm eclipse 의 균일 재분석 (frame-
  normalized PCA). cross-check; 일관된 결과.
- **2505.03672** TRAPPIST-1 행성의 secondary-atmosphere 소스로서 water
  outgassing 에 대한 통계적 지구화학적 제약. "fossil O₂" 추론의 배경
  맥락.

### 읽음 (instrument-only, 시각 정보 아님)

- **2409.19333** Stellar contamination 보정 방법론 논문. 완전성을
  위해 인용; c 에 대한 직접 시각 콘텐츠 없음.

### 읽지 않음 — arXiv preprint 없음 또는 낮은 우선순위 (~20 편)

c 참고문헌은 b 의 것보다 작음 (32 vs 66). 비-arXiv 논문 대부분은
conference 요약 또는 자매 행성 biosignature 연구. 건너뛴 주목할 항목.

- **2026NatAs.tmp...65G** "No thick atmosphere around TRAPPIST-1 b
  and c from JWST thermal phase curves" — Ducrot 2025 의 Nature
  Astronomy 출판일 가능성 높음 (arXiv 2509.02128 통해 다룸). Skip.
- **2025arXiv...** 다양한 retraction / re-fit conference 요약. c
  eclipse depth 를 업데이트하는 경우가 아니라면 skip.

---

## 후속 follow-up 항목

- 더 짧은 파장의 MIRI 필터 (예. c 의 F1280W) 에서의 향후 c emission
  분광에 대해 0.1 bar O₂ 대기 선택 검증 — 대기 없음 대안은 통계적
  으로 동등하게 일관되며 향후 renderer 가 "맨 암석 형제" b+c 페어링
  이 필요하다면 선호될 수 있음.
- Way 2024 / Cohen 2024 (TRAPPIST-1 표면 산화 모델링) 의 c-특화 예측에
  대해 산화철 accent 두드러짐 cross-check, 이들이 사용 가능해질 때.
- "대기 없는 맨 암석" 해석을 위한 cfg 변형, b 의 대기 없는 cfg 와
  조율된 팔레트로 페어링.
- `density_g_cc` 항목 정교화. derived 값 (6.36) 은 Agol 2021 의 보고
  5.7 보다 약간 높으며, 다른 불확실성 전파 반영. Phase 2 가 조정해야
  함.
