<!-- τ Ceti e Phase 3 합성. 역사적 / 철회된 검출. 아카이브용 cfg-ready 기록만 유지 -->
# τ Ceti e — Phase 3 Synthesis (Historical / Refuted)

τ Ceti e 는 본래 Feng et al. 2017 (`2017AJ....154..135F`,
arXiv:1708.02051) 이 metal-poor G8V τ Ceti 주위에서 발표한 네 개
RV 행성 후보 중 하나였습니다 — 162.87 일 주기로 0.538 AU 에서 도는
3.93 M⊕ (M sin i) super-Earth 로, optimistic 거주가능영역 (Güdel 2014)
의 안쪽 가장자리 바로 안에 자리잡고 있었습니다. 네 검출 중에서
처음부터 가장 disputed 한 신호였으며 — amplitude-to-noise 비가
가장 낮았고, Feng 2017 §6 가 항성 활동도에 의한 오염 우려를 직접
플래그했습니다.

**현재는 존재 가능성이 철회됨 — NEA 2026-04-09 가 False Positive 로
재분류**. Figueira et al. 2025 (`2025A&A...700A.174F`,
doi:10.1051/0004-6361/202553869) 의 ESPRESSO sub-10 cm/s RV 정밀도가
162 일 신호를 검출하지 못한 결과를 인용. Cretignier et al. 2021
(`2021A&A...653A..43C`) 은 그보다 앞서 HARPS 데이터에 YARARA 항성-활동
후처리를 적용해 같은 부정적 결론에 도달했고, ESPRESSO 는 원래 신호가
행성이 아니라 항성 활동임을 기기 차원에서 확정했습니다. e 는
`db/systems/tau_cet.json::planets[]` 에 **없습니다**.

**이 Phase 3 합성은 cfg 로 방출되는 천체가 아니라 역사적 / 문화적
기록으로 존재합니다.** 이 Decisions 로부터 어떤 KSP 행성도 만들어지지
않으며, 모든 행은 Confidence=low 입니다 — 근거 신호 자체가 이제는
아티팩트로 간주되기 때문입니다. 합성은 문화적 교차참조를 위해 Feng
2017 의 그림을 보존합니다 (이 행성은 Andy Weir 의 *Project Hail Mary*
(2021) 에 등장하는 "Adrian" 의 실세계 모델이었습니다). rex-data-comparison
§6 의 큐레이션 thread 와, 한때 확정으로 다뤄지던 검출이 False Positive
재분류 아래에서 어떻게 보이는지의 워크드 예시도 함께 보존합니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `disposition` | False Positive Planet (NEA 2026-04-09) | high | Figueira 2025 ESPRESSO 반박, Cretignier 2021 YARARA 의 선행 미검출. 이 표에서 유일한 high-confidence 행 |
| `tidally_locked` | false | low | P = 162.87 d 와 a = 0.538 AU, 0.78 M☉ 호스트 주위에서 조석 고정 시간 척도는 7 Gyr 를 넘어섭니다. 존재했다 해도 고정되지 않았을 것 (Vinson 2017). 행성이 존재하지 않으므로 Confidence low |
| `obliquity_deg` | 23 | low | Tie-break. 비동기 super-Earth 에 대한 지구형 기본값. 관측 제약이 없을 뿐 아니라 제약할 천체 자체가 없음 |
| `eccentricity` | 0.18 (+0.18 / −0.14) | low | Feng 2017 RV fit. 불확실성 구간이 너무 넓어 1σ 안에 0 이 들어가는 것 — 이 자체가 신호가 마지널했다는 힌트 |
| `argument_of_periastron_deg` | 22 (+75 / −46) | low | Feng 2017 RV fit. 잘 제약되지 않음. 네 행성 중 최악 |
| `sidereal_period_days` | 162.87 (+1.08 / −0.46) | low | Feng 2017 RV. 이 신호는 이제 항성 활동에 귀속됨 (Figueira 2025) |
| `semi_major_axis_au` | 0.538 | low | Feng 2017 가 Kepler 3 법칙 + 호스트 질량으로 유도. 기하학적으로는 유효, 물리적으로는 공허 |
| `inclination_deg` | 35 | low | Tie-break. 공면 가정 위에서라면 τ Ceti 잔해 원반 경사 (MacGregor 2016) 를 상속했을 값. 철회된 신호에 대해서는 의미 없음 |
| `mass_mearth` | 3.93 (M sin i) | low | Feng 2017 RV. 진폭 fit 에서 ±0.4. 신호가 철회된 현재, 이는 어떤 천체의 속성이 아니라 원래 측정의 기록 |
| `radius_rearth` | 1.81 | low | Feng 2017 이 mass–radius 관계 (Weiss & Marcy 2014 sub-Neptune) 로 카탈로그한 반지름. 결코 측정된 적 없음 |
| `surface_gravity_g_earth` | 1.20 | low | derived = 3.93 / 1.81². 같은 caveat |
| `density_g_cc` | 3.66 | low | derived. 존재했다면 sub-Neptune 계열 |
| `water_mass_fraction` | 0.10–0.30 | low | 이론적. 0.538 AU, metal-poor G8V 주위의 inner-edge optimistic-HZ super-Earth 라면 Feng 2017 그림에서 적당한 휘발성 인벤토리를 가졌을 것 |
| `insolation_s_earth` | 1.58 | low | derived L_bol/a²: 0.457 L☉ / (0.538 AU)² — 지구 (1.0) 와 금성 (1.91) 사이. G8V 보수적 HZ 안쪽 가장자리 안 (Kopparapu 2014: ~1.05 S⊕) |
| `equilibrium_temp_k` (A=0) | 313 | low | derived 278 × (L/a²)^0.25 — 지구의 255 K 보다 살짝 위 |
| `equilibrium_temp_k` (A=0.3) | 286 | low | 지구형 albedo 로 derived — 액체 수 영역 안에 편하게 위치 |
| `bond_albedo` | 0.30 | low | Tie-break. 원래 Feng 2017 그림의 온대 super-Earth 에 대한 지구형 기본값 |
| `surface_temp_global_mean_k` | 295 | low | 역사적 reading 의 지구형 적당한 온실 시나리오 — 적당한 H₂O 증기를 가진 얇은 N₂/CO₂ 대기 가정 |
| `surface_temp_substellar_k` | 310 | low | 비동기 느린 자전자 — 일주 substellar 피크가 평균보다 적당히 높음 |
| `surface_temp_nightside_k` | 280 | low | 역사적 reading 에서 충분히 두꺼운 대기가 nightside 냉각을 제한 |
| `atmosphere_present` | true (지구형) | low | 역사적 Feng 2017 그림은 온대 대기를 가정. 행성이 존재하지 않으므로 어떤 관측도 시도된 적 없음 |
| `atmosphere_surface_pressure_pa` | 100 000 | low | 1 bar 를 역사적 시나리오의 canonical 지구형 기본값으로 채택. 측정 아님 |
| `atmosphere_composition` | N₂ ~78%, CO₂ ~2–5%, H₂O 가변, 미량 O₂ 불확실 | low | 역사적 지구형 reading. metal-poor 호스트가 원시 휘발성 인벤토리를 살짝 줄임. 생물권 가정 없음 |
| `atmosphere_scale_height_km` | 8.5 | low | derived: kT/μg with T≈290 K, μ=29, g=11.8 m/s² |
| `atmosphere_tint_rgb_hex` | `#8a99aa` (깨끗한 G8V SED 아래 옅은 청-그레이) | low | Tie-break. 1 bar 의 Rayleigh 산란은 지구형 푸름을 주지만, metal-poor SED 때문에 태양의 옅은 푸름보다 살짝 더 차가운 톤 |
| `cloud_cover_fraction` | 0.50 | low | 역사적 그림의 지구형 기본값 |
| `cloud_tint_rgb_hex` | `#ece6dc` (G8V 빛 아래 깨끗한 크림-흰 H₂O 구름) | low | Tie-break. 더 깨끗-노란 G8V SED 아래 표준 H₂O 구름 상층 반사율 |
| `ocean_present` | true (역사적 reading 에서 부분 커버리지) | low | 역사적 Feng 2017 그림은 표면 액체 수를 지지. 휘발성 인벤토리 + 조사량이 허용했을 것. 철회됨 |
| `ocean_extent_substellar_radius_deg` | n/a (비동기 자전자) | low | 안구 기하 아님 — 느린 비동기 자전이 모든 해양 커버리지를 substellar 패치가 아니라 전구적으로 분포 |
| `ocean_tint_rgb_hex` | `#2a4a68` (깨끗한 G8V SED 아래 심해) | low | Tie-break. Rayleigh-푸름 해양. metal-poor 호스트 SED 때문에 지구의 그것보다 살짝 더 차가운 톤 |
| `surface_ice_caps` | 계절성 극지 만년설 가능 | low | 적당한 이심률 (0.18) + 비동기 자전이 적당한 계절 사이클을 줌. 역사적 그림에서 극지 얼음 형성이 그럴듯 |
| `surface_tint_rgb_hex_primary` | `#7a6a58` (G8V 조명 아래 대륙형 현무암-퇴적물 표면) | low | Tie-break. 지구형 대륙 혼합. metal-poor 원시 먼지는 지구 토양보다 살짝 덜 철-염색됨 |
| `surface_tint_rgb_hex_accent` | `#4a6840` (식생-analog 또는 olivine 풍부 표면 패치) | low | Tie-break. Project Hail Mary 의 "Adrian" 은 식생 같은 표면 피처를 가진 것으로 렌더링됨. Confidence low. 데이터로 어떤 생물권도 함의되지 않음 — 픽션 교차참조 전용 |
| `surface_morphology` | 역사적 reading 의 혼합 대륙/해양 지구형 | low | Feng 2017 그림. 표면 형태는 관측된 적 없음 |
| `magnetic_field_present` | true (적당함) | low | 다주 비동기 자전을 가진 4–5 M⊕ 암석체라면 존재했을 때 적당한 dynamo 를 지지할 수 있음 |
| `magnetic_field_strength_microtesla_equator` | 30 | low | Tie-break. 가정 파라미터에 RM22 스케일링. 지구와 유사한 값 |
| `tidal_heating_w_m2` | 0.001–0.01 | low | 0.538 AU 에서 e = 0.18. 역사적 시나리오에서 적당한 조석 플럭스 |
| `induction_heating_w_m2` | < 0.001 | low | 조용한 호스트 (log L_X ≤ 26.5). induction 무시 가능 |
| `radiogenic_heat_w_m2` | 0.04 | low | 질량으로 스케일된 지구형 맨틀 방사성 |
| `aurora_present` | true (적당함) | low | 역사적 시나리오의 적당한 자기장 + 대기. 희미한 확산 오로라 가능 |
| `aurora_color_primary_hex` | `#4DFF4D` | low | Tie-break. 어떤 O₂ 라도 있다면 [OI] 557.7 nm 녹색. 없다면 N₂ Vegard-Kaplan 청록 |
| `aurora_intensity_kR_typical` | 1 | low | 조용한 호스트 — 오로라 여기율이 지구의 그것보다 한참 아래 |
| `star_apparent_angular_diameter_deg` | 0.786 | low | derived: 2 × R★ / a × (180/π). 지구에서 본 태양의 약 1.5× |
| `stellar_illumination_color_temp_k` | 5344 | low | 호스트 Teff (Pavlenko 2012). 역사적 시나리오에만 적용 |

## Surface synthesis

Feng 2017 그림에서 τ Ceti e 는 1.58 S⊕ 에 있었습니다 — G8V 호스트의
보수적 거주가능영역 안쪽 가장자리 (Kopparapu 2014: ~1.05 S⊕) 와
비슷하거나 살짝 안쪽. 이 조사량에서 e 는 네 행성 중 "흥미로운"
하나였습니다 — 지구보다 따뜻하지만 금성형 runaway 영역은 아니며,
평형 온도는 albedo 0 에서 313 K, 지구형 0.3 bond albedo 아래
286 K — 액체 수 영역 안에 편하게 자리잡았습니다. Güdel 2014 의
optimistic 거주가능영역 (지구질량 천체에 대해 0.75 S⊕ 까지 안쪽으로
확장) 은 2017 년과 2025 년 사이 e 가 거주가능 타겟으로 논의될 때
가장 자주 인용된 프레임워크였습니다.

**역사적 시나리오는 부분 해양 커버 super-Earth 를 가정합니다.**
3.93 M⊕ (M sin i) 와 sub-Neptune-관계 반지름 1.81 R⊕ 를 가진 Feng
2017 그림은, 적당한 1 bar N₂/CO₂ 대기와 행성의 30–60% 정도를 덮는
표면 해양, 그리고 0.18 이심률로 변조되는 계절성 극지 만년설을 가진
온대 세계를 지지했습니다. 이 reading 에서 표면 온도는 전구적으로
~295 K, substellar 일주 피크는 ~310 K, nightside 는 ~280 K — 느린
비동기 자전 때문에 지구보다 강한 극-적도 그래디언트를 가진
지구-온대 조건입니다.

**색 선택 — 지구형에 metal-poor 호스트 보정.** e 가 존재해 렌더링
된다면, 1차 표면 색조 `#7a6a58` 은 더 깨끗-노란 G8V SED 아래 대륙
혼합 (현무암 + 퇴적물) 을 인코딩합니다. 액센트 `#4a6840` 은 식생-
analog 또는 olivine 풍부 패치 용입니다 — Andy Weir 의 "Adrian" 픽션
렌더링이 식생 같은 피처를 묘사했음을 명시적으로 끄덕이는
tie-break. *이는 픽션 교차참조이지 물리적 예측이 아닙니다.* 어떤
데이터도 e 에 생물권을 지지한 적 없으며, False Positive 처분 아래
질문 자체가 무의미합니다.

**철회 맥락.** Feng 2017 의 162 d 신호는 τ Ceti 의 느린 자기 사이클
과 상관된 항성-활동 아티팩트로 밝혀졌습니다 — 162 d 주기는 대략
P_rot / 4–5 (호스트는 Baliunas 1996 프레임에서 34 d, Boro Saikia 2018
ZDI 로는 46 d 로 자전) 로, 조용한 G 왜성의 활동-유도 RV 잡음에
전형적인 고조파 영역에 놓입니다. Cretignier 2021 가 YARARA 후처리
기법으로 이를 처음 식별했고, Figueira 2025 가 ESPRESSO 의 sub-10 cm/s
정밀도로 확인 — 더 깨끗한 기기의 데이터에 162 d 신호가 나타나지
않습니다.

## Atmosphere synthesis

대기 합성은 이 문서에서 가장 철저히 역사적인 부분입니다. 어떤 대기도
관측된 적 없습니다. Feng 2017 그림이 지구형 조건을 가정한 것은 추정된
조사량이 e 를 optimistic HZ 에 위치시켰기 때문이지만, 근거 신호 자체가
이제 아티팩트로 간주됩니다.

**압력 선택 — 1 bar (역사적).** Feng 2017 그림의 지구형 기본값은
표면 압력 1 bar 입니다. 이것이 거주가능성 논의와 대중 과학 다룸 (이
중에는 *Project Hail Mary* 의 Adrian 렌더링이 포함됩니다) 에서의
작업 가정이었습니다. Wordsworth 2015 프레임워크 아래, 1.58 S⊕ 의
metal-poor 조용한 G 왜성 주위 inner-HZ super-Earth 는 다-Gyr 시간
척도로 1 bar N₂-우세 대기를 유지할 수 있습니다 — XUV 구동
hydrodynamic 손실은 무시 가능 (log L_X ≤ 26.5. Schmitt 1985), Teq =
286 K 에서 N₂ Jeans 탈출은 비효율적.

**조성 (역사적).** metal-poor 호스트 보정이 들어간 지구형. N₂ ~78%,
CO₂ ~2–5% (G8V 의 더 낮은 조사량 아래 온대 Teff 를 유지하기 위해
지구 대비 약간 상승), H₂O 증기 가변, 미량 O₂ 불확실 (증거 없이는
생물권 가정 없음). metal-poor 호스트는 같은 궤도 영역의 지구가
가졌던 것보다 살짝 적은 원시 휘발성 인벤토리를 함의합니다.

**하늘 모습 (역사적).** 깨끗한 G8V SED 아래 옅은 청-그레이 (`#8a99aa`)
Rayleigh 산란 — 호스트가 청색 연속체를 덜 방출하므로 지구 하늘보다
살짝 더 차가운 톤. 호스트 별은 e 표면에서 0.786° 를 채웁니다 (지구
에서 본 태양의 약 1.5×) — metal-poor SED 아래 밝은 옅은 노랑 원반.
구름은 지구의 더 따뜻한 톤 구름이 아니라 깨끗한 크림-흰 (`#ece6dc`)
으로 보였을 것. 표면 조명은 지구 조사량의 약 1.6× — 살짝 더 차가운
색 온도를 가진 밝은 지구형 하루.

**손실 메커니즘 (역사적 맥락).** 호스트의 조용한 XUV 환경이 가장
중요한 인자입니다. log R'HK = −4.95 의 조용한 G 왜성 주위 0.538 AU
의 e 는 7 Gyr 동안 본질적으로 어떤 hydrodynamic 탈출도 겪지 않았을
것입니다. Feng 2017 그림의 대기는 따라서 예외적으로 안전한 1 bar
envelope 이었습니다 — 적당한 태양풍 침식을 겪는 지구 자신의 대기보다
오히려 더 안전했다고 주장할 수 있습니다. 이 점이 Adrian 을 Andy Weir
서사에서 그럴듯한 장기 거주가능 세계로 만든 근거의 일부였습니다.

## Rotation & spin synthesis

τ Ceti e 가 존재한다면, **조석 고정되지 않습니다**. 0.78 M☉ 호스트
주위 P = 162.87 d, a = 0.538 AU 에서 조석 고정 시간 척도 (Vinson 2017
공식, τ_lock ∝ a^6 / (M_p × Q × R_p^5)) 는 대략 30 Gyr — 시스템
나이를 한참 넘어섭니다. spin damping 이 작동할 시간이 없었습니다.

**Pseudo-synchronous spin 후보.** 이심률 0.18 에서 e 는 고차 spin-orbit
공명 (Hut 1981 pseudo-synchronous 자전, ω_spin ≈ ω_orb × f(e)) 으로의
포획 강력 후보였을 것입니다. e = 0.18 에서 Hut 의 f(e) ≈ 1.4 가
pseudo-synchronous 자전 주기 ~116 d 를 줍니다 — 길지만 고정되지 않은
자전. 이 이심률에서 3:2 공명도 가능합니다 (Vinson 2017 포획 확률
~30–50%, 자전 주기 ~109 d).

**비동기 빠른 자전자 대안.** pseudo-synchronous 도 3:2 포획도
일어나지 않았다면, e 는 시간에서 일 단위의 원시 주기로 자전했을
것이며, 긴 궤도 주기 때문에 7 Gyr 에 걸쳐 조석 damping 이 불완전.
이 합성의 cfg-역사적 기본값은 정확한 값을 지정하지 않고 일반적인
"다주 비동기 느린 자전자" 를 채택합니다 — 철회된 천체에 대해 질문이
무의미하기 때문.

**Obliquity.** Tie-break 기본값으로 지구형 23° 채택. 0.18 이심률은
±36% peak-to-trough 의 궤도 조사량 변동을 줍니다 — 지구의 ±3.4% 보다
유의미하게 강함 — 162 일 궤도에 걸쳐 상당한 "이심률 계절" 을 일으킬
것. 역사적 그림에서 이것이 극지 만년설 형성과 계절성 반구 날씨 패턴을
구동했을 것입니다.

**자기 dynamo 기대치 (역사적).** 다주 자전을 가진 4–5 M⊕ 암석체는
적당한 dynamo 를 지지할 수 있습니다. RM22 (Reiners-Christensen)
스케일링은 표면 자기장 ~30 μT (지구의 25–65 μT 와 유사) 를 줍니다.
cfg 천체가 만들어지지 않으므로 cfg 와 무관.

## Visual styling

이 절은 합성에서 가장 문화적인 부분으로, 행성을 "존재하는 그대로"
가 아니라 "묘사되었던 그대로" 로 프레이밍합니다 (존재하지 않으므로).

- **전구 외관 (존재했다면).** 대륙 land mass, 부분 해양 커버리지,
  계절성 극지 얼음을 가진 청-녹-크림 지구형 세계. 시각 캐릭터는
  살짝 더 크고 따뜻한 지구에 가장 가깝습니다 — 2017–2025 대중 과학
  다룸과 Andy Weir 의 Adrian 묘사를 지배한 표준 "거주가능 super-
  Earth" 렌더링.
- **Dayside 디테일 (역사적 reading).** 현무암-퇴적물 혼합 톤
  `#7a6a58` 의 대륙에 식생-analog 또는 olivine 풍부 패치 `#4a6840`.
  metal-poor G8V SED 때문에 지구의 해양보다 살짝 더 차가운 톤의
  `#2a4a68` Rayleigh-푸름 해양이 30–60% 커버. 낮은 위도에서는
  Hadley-cell 순환으로 인한 구름 띠.
- **Terminator 밴드 (역사적).** 온대 대기의 특징적 부드러운 구름-
  그림자 그래디언트 — 무대기 Mercury-analog 자매 g 보다 한참 덜
  또렷하고, snowball 외곽 자매 f 보다 한참 더 발달함.
- **Nightside 외관 (역사적).** 어둠. 별빛 반사로 인한 cyan-white
  구름 하이라이트. 데이터로 어떤 생물권도 함의되지 않으므로 도시
  불빛 없음 — *Project Hail Mary* 의 Adrian 도 인간 원정 이전에는
  무인으로 묘사됩니다.
- **대기 안개 (역사적).** ~30–50 km 두께의 옅은 청-그레이 (`#8a99aa`)
  Rayleigh 림 글로우. 지구의 푸른 림과 캐릭터는 비슷하지만 살짝
  더 차가운 톤.
- **희미한 오로라 (역사적).** ~1 kR 의 녹색 톤이 살짝 들어간 확산
  극지 오로라 가능. 렌더링의 정의적 피처는 아님.
- **하늘의 별 (역사적).** τ Ceti 는 e 표면에서 0.786° 를 채웠을 것
  — 지구에서 본 태양의 약 1.5×. metal-poor G8V 조명 아래 밝은 옅은
  노랑 원반으로, substellar 지점에서 지구 조사량의 1.58× 를 전달.
- **"Adrian" 문화적 교차참조.** Andy Weir 의 *Project Hail Mary*
  (2021) 가 e 를 Adrian 이라 부르고 주인공의 임무 타겟으로 사용.
  소설은 Feng 2017 의 궤도 파라미터 (P ≈ 168 d, a ≈ 0.55 AU,
  M sin i = 3.93 M⊕) 를 채택하지만 거주가능 Earth-analog 프레이밍
  과는 다른 환경을 구축 — 아래 "Weir's Adrian" 글머리표 참조. 2025
  ESPRESSO 철회는 소설보다 4 년 늦습니다. 근거 천체가 존재하지
  않으므로 NearStars 는 인게임에서 Adrian 을 렌더링하지 않습니다.
  이 Phase 3 마크다운이 `docs/reference/cultural-context.md
  § Tau Ceti` 와 짝을 이룬 문화적 교차참조 홈입니다.
- **Weir 의 Adrian — 위의 역사적 Earth-analog 렌더링과 다름.**
  *Project Hail Mary* 는 Adrian 을 Earth-analog 푸른 해양 세계로
  묘사하지 않습니다. 소설의 명시된 파라미터 (Weir 인터뷰 + 소설
  내 측정값 종합). 표면 중력 1.4 g, 대기 91% CO₂ / 7% CH₄ / 1% Ar
  / 미량 (N₂ 없음 — Taumoeba 가 질소 불내성이라 plot 핵심), 우주
  에서 본 녹색 외관, 91.2 km 고도에서 sampling 수행 (그 고도에서
  p = 0.02 bar, T = −51 °C). Weir 의 압력 구조는 다 bar CO₂ 우세
  표면 대기를 함의 — Earth 보다 Venus 온대 analog 에 가깝습니다.
  소설에 묘사된 해양 없음. sampling 임무는 10 km xenonite chain
  으로 대기 상층 클라우드를 타겟. 표면 도달 안 함. 위 Decisions
  표의 식물 accent 톤 `#4a6840` 가 Weir 의 "녹색 행성" 묘사에
  가장 근접하지만, Weir 의 렌더링은 *광화학 haze 녹색* (CH₄ +
  CO₂ + 대기 부유 Taumoeba 생물) 이지 식물 녹색이 아닙니다. 표면
  중력 1.4 g 는 Weir 가 popular-science sub-Neptune 핏 (1.81 R⊕,
  1.20 g) 보다 더 암석질 (반지름 더 작은) mass-radius 관계를
  채택했음을 함의 — 같은 3.93 M⊕ 에서 1.68 R⊕ 근방. 역사적
  Earth-analog (위 표) 와 Weir 의 CO₂-haze 둘 다 현 시점에서
  픽션. 관측된 게 아닙니다.

## Bibliography

### Read (signal history + refutation)

- **Feng F. et al. 2017** — *Color difference makes a difference:
  four planet candidates around τ Ceti*, AJ 154, 135
  (`2017AJ....154..135F`, arXiv:1708.02051). 원래 발견 논문.
  e 를 P = 162.87 d, M sin i = 3.93 M⊕, e = 0.18 로 보고. 위
  역사적 Decisions 행을 정박. Feng 2017 §6 자체가 e 가 네 행성 중
  amplitude 가 가장 마지널함을 경계.
- **Cretignier M. et al. 2021** — *YARARA: HARPS RV 의 항성-활동
  후처리*, A&A 653, A43 (`2021A&A...653A..43C`). 항성-활동
  탈상관 후 162 d 신호의 첫 미검출. 신호를 행성이 아니라 활동-상관
  으로 식별.
- **Figueira P. et al. 2025** — *τ Ceti ESPRESSO RV 모니터링.
  e 의 철회와 f/g/h 의 더 엄격한 한계*, A&A 700, A174
  (`2025A&A...700A.174F`, doi:10.1051/0004-6361/202553869).
  e 가 항성-활동 아티팩트임을 기기 차원에서 확정. ESPRESSO 의
  sub-10 cm/s 정밀도는 원래 Feng 2017 진폭 아래. 162 d 신호 부재.
  NEA 2026-04-09 이 채택한 False Positive 처분을 견인.

### Read (context for habitability framing)

- **Güdel M. et al. 2014** — *optimistic 안쪽 가장자리를 포함한
  거주가능영역 한계*, A&A 571, A85 (`2014A&A...571A..85G`).
  G8V 의 안쪽 가장자리 optimistic 한계는 ~0.75 S⊕. Feng 2017 의
  e 를 1.58 S⊕ 의 optimistic HZ 안에 편안하게 놓음. e 를 "거주가능"
  으로 묘사한 대중 과학 프레이밍을 견인.
- **Kopparapu R. K. et al. 2014** — *주계열별 주위 거주가능영역*.
  G8V 의 보수적 HZ 안쪽 가장자리는 ~1.05 S⊕. 1.58 S⊕ 의 e 는
  보수적 reading 에서 runaway-greenhouse 경고 밴드 바로 안. Güdel
  와 Kopparapu 안쪽 가장자리 간의 불일치는 철회 이전 e 의 거주가능성
  분류 논쟁의 일부였음.
- **Wordsworth R. & Pierrehumbert R. 2015** — *조용한 G/K 호스트
  주위 super-Earth 의 대기 유지*. 역사적 reading 에서 가정한 1 bar
  지구형 대기 바닥의 프레임워크.

### Read (host star context)

- **Pavlenko Y. V. et al. 2012** — 호스트 별 [Fe/H] = −0.55,
  log R'HK = −4.95, Teff = 5344 K. e 대기와 색 선택에 대한 역사적
  metal-poor-host 프레이밍 견인.
- **Mamajek E. E. & Hillenbrand L. A. 2008** — gyrochronological
  나이 7 ± 1.5 Gyr. 다-Gyr 시간 척도의 역사적 대기-유지 논의에 관련.
- **Schmitt J. H. M. M. et al. 1985** — 호스트 X 선
  log L_X ≤ 26.5. 조용한 XUV 환경이 역사적 reading 의 "안전한 대기"
  프레이밍의 중심이었음.
- **Boro Saikia S. et al. 2018** — ZDI 46 d 자전. 철회된 162 d
  신호가 호스트 자전의 고조파에 놓이며, 활동-유도 false-detection
  과 일관됨에 관련.

### Read (cultural cross-reference)

- **Weir A. 2021** — *Project Hail Mary* (소설). e 를 "Adrian"
  이라 부르고 주인공의 임무 타겟으로 사용. 소설은 2025 철회보다 4년
  앞서며, e 검출의 가장 두드러진 문화적 앵커. `docs/reference/
  cultural-context.md § Tau Ceti` 에 문서화.

### Read (fiction worldbuilding reference — Weir 의 Adrian 파라미터)

- **Weir A. — Scientific American Science Quickly 팟캐스트, "The real science and the fun fiction behind Project Hail Mary"**. Weir 가 중력 / 대기 유도를 설명. Feng 2017 의 M sin i = 3.93 M⊕ 를 채택하고 암석질 mass-radius 관계로 표면 중력 ~1.4 g 를 역계산. 또 Tau Ceti 를 고른 이유 — ~9 Gyr 항성 나이가 지구보다 생명에 head start 를 부여.
- **Weir A. — Astronomy.com, "Andy Weir on the science of Project Hail Mary"**. 의도된 single-genesis panspermia 디자인의 출처. Adrian 이 Astrophage 의 기원이자 *유일한* Astrophage-저항 생물권 (Taumoeba 가 그곳에 endemic).
- **Weir A. — Space.com, "Sci-fi author Andy Weir explains the astrobiology behind Project Hail Mary"**. 비교 가능한 Erid 파라미터 제공 (29 atm, ammonia, 2.1 g, 6시간 day) — Adrian 을 소설 3-세계 천체생물학의 lower-gravity, CO₂-우세 카운터파트로 frame. 중요. ammonia + 2.1 g + 6h day 는 **Erid** 파라미터지 Adrian 아님. 두 세계는 자주 혼동됨.
- **Sky & Telescope — "Explore the Worlds of Project Hail Mary" (2021)**. Weir 가 철회 이전 Feng 2017 검출 그림으로 집필했음을 확인. Tau Cet e 와 40 Eri A b 를 Adrian + Erid 의 두 앵커 실제 외계행성 검출로 framing.
- **Project Hail Mary Fandom Wiki — Adrian / Taumoeba / Astrophage 페이지**. 소설 내 측정값의 팬-편찬 인덱스 (1.4 g, 91% CO₂ / 7% CH₄ / 1% Ar 대기, 녹색 외관. Taumoeba 서식지 91.2 km / 0.02 bar / −51 °C. 질소 불내성). 소설 텍스트로의 citation 포인터이지 primary authority 아님.
- **Wheeler D. — "Project Hail Mary Stellar Map" (dwheeler.com/essays/project-hail-mary-map.html)**. Wheeler 가 Feng 2017 에서 직접 Adrian 의 궤도를 재구성 (P = 168 d, a = 0.552 AU) 했음을 보여주는 third-party 유도. 소설이 이 숫자들을 명시적으로 기재 안 함. e 식별에서 inferred.

### Not read — superseded or low-priority (~10 papers)

- **Tuomi M. et al. 2013** + **Tuomi 2014 erratum** — e 를 살짝
  다른 파라미터로 포함한 더 이른 τ Ceti 5-행성 주장. Feng 2017 로
  대체. 둘 다 철회에 비추어 이제 역사적.
- **천체생물학 추측 논문 다수 (2017–2024)** — Feng 2017 그림 아래
  e 의 거주가능성 평가. False Positive 처분 아래 cfg 관련성 없음.
  이 합성에서는 미독.
- **e 를 타겟한 SETI / technosignature 논문** — 철회 이전에
  이루어진 역사적 관측. cfg 관련성 없음.

## Open items for follow-up

- **처분은 확정됨.** f / g / h (이들은 `pl_controv_flag = 1` 로
  남아 있고 retraction watch 위에 있음 — 자매 Phase 3 합성의 open
  Lubin 2024 / 미래-ESPRESSO 질문을 참조) 와 달리, e 의 처분은
  최종입니다 — NEA 2026-04-09 의 False Positive Planet. e 를 다시
  승격할 후속은 예상되지 않습니다.
- **Cultural-context 교차참조가 canonical 홈.** 미래의 어떤 "Adrian"
  렌더링이든 — 예를 들어 NearStars 패치의 flavor-text Easter egg —
  cfg 천체를 생성하지 말고 `docs/reference/cultural-context.md
  § Tau Ceti` 를 참조해야 합니다. 소설은 픽션이고 근거 행성은 아닙
  니다.
- **자매 retraction watch.** Figueira 2025 는 f / g / h 에 대해서도
  더 엄격한 한계를 보고합니다. 셋 모두 아직 공식 철회된 것은 아니지만
  (NEA 는 여전히 disputed 로 들고 있음), f / g / h Phase 3 합성의
  Open item 들이 retraction-watch 질문을 추적합니다. 미래 ESPRESSO
  재분석이 그 중 어느 것이라도 철회한다면, 이 템플릿 (모든 Confidence
  low 의 역사적 전용 Phase 3) 이 선례입니다.
- **`db/systems/tau_cet.json::meta.notes` 가 e 에 대한 false-positive
  처분을 문서화해야 함.** 현재 DB 는 단순히 e 를 `planets[]` 에서
  생략. Figueira 2025 + NEA 2026-04-09 을 인용한 명시적 `meta.notes`
  엔트리가 있으면 미래 독자에게 큐레이션 갭처럼 보이지 않고 생략이
  self-documenting 이 됩니다.

## Related

- [tau-cet](tau-cet.md) — 호스트 별 Phase 3 (G8V metal-poor.
  조용함, 늙음, 잔해 원반 보유)
- [tau-cet-f](tau-cet-f.md) — 자매. 가장 바깥쪽, snowball
- [tau-cet-g](tau-cet-g.md) — 자매. 가장 안쪽, 뜨거운 맨 암석
- [tau-cet-h](tau-cet-h.md) — 자매. 중간, Venus-analog
- [cultural-context](../reference/cultural-context.md) — §
  Tau Ceti, *Project Hail Mary* 의 "Adrian"
- [rex-data-comparison](../reference/rex-data-comparison.md) — §6
  τ Ceti e 의 역사적 큐레이션 갭 (NEA 2026-04-09 False Positive
  처분으로 해소됨)
- [methodology](../reference/methodology.md) — Decisions 스키마
