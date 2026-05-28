<!-- Barnard's Star Phase 3 합성. 정적이고 노쇠한 M4 V 호스트와 4개 sub-Earth 행성 시스템을 위한 cfg-ready 결정과 근거 -->
# Barnard's Star — Phase 3 Synthesis

Barnard's Star (GJ 699, HIP 87937) 는 태양으로부터 두 번째로 가까운
항성계로, α Centauri 삼중계 다음 1.828 pc 거리에 있습니다 (Gaia DR3
시차 547.0 ± 0.04 mas). 단독 M4.0 V 왜성이며 질량 0.161 ± 0.006 M☉
(Mann 2015 M–K 보정), 반지름 0.1868 ± 0.0011 R☉ (Rains 2021 CHARA
간섭계), 유효온도 3195 ± 28 K (González Hernández 2024 SED + 볼로미터릭
플럭스) 를 가집니다. 알려진 별 가운데 가장 큰 고유운동 (연 10.3 초각)
과 −110 km/s 의 시선속도를 보이는 운동학은 이 별을 명백히 은하 헤일로
인구에 위치시킵니다. Toledo-Padrón 외 2019 는 헤일로 멤버십에서
도출한 운동학적 나이를 10 ± 2 Gyr 로 추정하는데, 이는 Barnard 를 10 pc
이내에서 가장 오래된 별 중 하나로 만듭니다.

이 시스템에는 길고 복잡한 행성 탐색 역사가 있습니다. 1960–80 년대 Van
de Kamp 의 astrometric 캠페인이 목성급 동반자를 주장했지만 확인되지
않았고, Ribas 외 2018 은 HARPS RV 앙상블에서 0.4 AU·233 일 주기의
super-Earth "b" 를 보고했지만 Lubin 외 2021 이 항성 활동의 1년
alias 로 반박했습니다. 현재 행성 목록은 González Hernández 외 2024 의
ESPRESSO 발견 — P = 3.15 d 의 sub-Earth, 완전히 다른 천체에 "b"
라벨을 재사용 — 과 Basant 외 2025 의 MAROON-X 확인 (후보 c, d, e
의 격상) 에 근거합니다. 네 행성 모두 단주기 (P < 7 d), sub-Earth
Msini 이며, 보수적 거주 가능 영역 안쪽 가장자리보다 한참 안쪽에
자리합니다 (Kopparapu 2014 의 inner HZ ≈ 0.1 AU, 이 항성 질량에서 P ≈ 10 d 에
해당).

활동도는 Barnard 의 결정적 항성 특징입니다. M4 왜성 중에서도 예외적으로
조용해서, log R'HK = −5.69 (Toledo-Padrón 2019) 는 활동 극소기의 태양보다
더 비활동적이며, 회전 주기는 145 ± 15 d 로 길고, 장기 자기 사이클은
10 ± 2 yr 로 González Hernández 2024 가 3200 d 에서 독립적으로 회수합니다.
그럼에도 Mega-MUSCLES 프로그램 (France 외 2020) 은 단일 HST + Chandra
캠페인에서 FUV 2건과 X선 1건의 flare 를 탐지했고, 이는 약 25% 의 flare
듀티 사이클을 의미합니다. 이 나이의 별로서는 높지만, 개별 flare 에너지
(~10²⁹·² – 10²⁹·⁵ erg) 는 Proxima 의 super-flare 영역보다 수 자리수 작습니다.
France 2020 은 *정상상태* XUV 출력이 현대 지구의 태양 극대기와 비슷해서
대기 가열률이 파국적이지 않다고 결론짓지만, 25% 듀티 사이클을 적분한
누적 손실은 열적 하이드로다이내믹 escape 로 약 87 지구대기 Gyr⁻¹,
이온 픽업 escape 로 약 3 지구대기 Gyr⁻¹ 입니다. 이들의 헤드라인 — "habitable
at last?" — 은 진정한 긴장을 포착합니다. Barnard 는 오래되고 조용한
M 왜성의 벤치마크이지만, 10 Gyr 누적 flare 환경은 여전히 대기를
침식합니다.

**NearStars 시나리오 선택. 145 일 회전, 약 200 G 의 모데스트한 표면
자기장, 양호한 정상상태 XUV 환경, 그리고 낮은 (~25%) flare 듀티
사이클을 ~10 년 사이클로 변조하는 헤일로-노쇠 M4 V 딥 레드 왜성입니다.
시각 스타일링은 차가운 3195 K 연속체, 금속성 부족이 금속이 풍부한 M4
대비 분자 밴드를 약간 푸르게 만드는 효과, 그리고 네 개의 뜨거운 암석
행성이 가까이서 받는 어둑한 조명을 강조합니다.** 17 cfg 픽 중 12 는
canonical-aligned, 5 는 tie-break 입니다 (X선 정상상태 수준, 자기장 RMS,
시각 hex 색상, flare 빈도 정규화, limb darkening 지수). 문서화된
divergence 는 없습니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M4.0 V | high | DB curated. 헤일로 노쇠 + 낮은 활동도는 일부 카탈로그의 "Ve" 보다 "V" 가 적절 |
| `mass_msun` | 0.161 ± 0.006 | high | Mann 2015 M–K 관계. DB recommended |
| `radius_rsun` | 0.1868 ± 0.0011 | high | Rains 2021 CHARA 간섭계 |
| `teff_k` | 3195 ± 28 | high | González Hernández 2024 SED 피팅. Cristofari 2024 NIR 3231 ± 21 K 와 약 1.5σ 이내 일치 |
| `luminosity_lsun` | 0.003558 ± 0.00007 | high | González Hernández 2024 볼로미터릭 플럭스 |
| `metallicity_fe_h_dex` | −0.15 ± 0.16 | medium | Marfil 2021 고해상도 광학 분광. Cristofari 2024 는 모델 입력으로 ~−0.5 dex 선호. 광범위한 합의는 sub-solar |
| `age_gyr` | 10 ± 2 | high | Toledo-Padrón 2019 헤일로 멤버십 운동학적 나이 |
| `rotation_period_days` | 145 ± 15 | high | Toledo-Padrón 2019 색채권 + 광도 |
| `activity_log_rhk` | −5.69 | high | Toledo-Padrón 2019. 알려진 M 왜성 중 가장 조용한 그룹 |
| `activity_cycle_years` | 10 ± 2 | high | Toledo-Padrón 2019 (10 yr). González Hernández 2024 가 3200 d ≈ 8.8 yr 회수 |
| `x_ray_log_lx_cgs_quiescent` | 25.5 | medium | Tie-break. France 2020 Chandra 단일 epoch 저 S/N 검출. 노쇠 M 왜성 포화 영역과 일관된 등급 |
| `x_ray_log_lx_cgs_flare_peak` | 27.5 | medium | Tie-break. France 2020 개별 사건 ~10²⁹·² erg, ~5000 s 적분 → 피크 속도와 일관 |
| `flare_duty_cycle` | 0.25 | high | France 2020 Mega-MUSCLES — HST + Chandra 동시 검출에서 flare 상태에 있는 시간 비율 |
| `flare_rate_per_day_total` | 0.1 | medium | Tie-break. ~50 ks (HST + Chandra) 에 3 flare → FUV 전용 외삽 시 ~5/일. 보수적으로 0.1 백색광 flare/일이 광도 상한과 일치 |
| `magnetic_total_field_G_mean` | 200 | medium | Tie-break. Reiners 2022 CARMENES Zeeman 분석은 수백 G 표면장 추정. SPIRou 폴라리메트리 (Cristofari 2024) 의 ordered 성분은 훨씬 약함 |
| `xuv_quiescent_flux_at_1au_erg_cm2_s` | 0.018 | medium | Duvvuri 2021 DEM EUV 100–912 Å 정상상태 재구성 |
| `xuv_flare_flux_at_1au_erg_cm2_s` | 0.146 | medium | Duvvuri 2021 DEM 재구성. flare 상태 (~8× quiescent) |
| `limb_darkening_alpha_h` | ~0.4 | low | Tie-break. 직접 측정 없음. M4 V 의 Claret 2018 grid 보간 |
| `visual_surface_tint_hex_primary` | `#bd4a2c` (딥 레드 M4 V. sub-solar [Fe/H] 로 M5.5 보다 약간 푸르게) | medium | Tie-break. Teff 3195 K 흑체 × 분자 밴드 흡수. [Fe/H] = −0.15 가 TiO 깊이를 약간 약화 |
| `visual_flare_color_hex` | `#ff5e36` (약한 FUV flare 시 Hα + 푸른 연속체 brightening) | medium | Tie-break. France 2020 FUV flare 스펙트럼. 게임 내 가시성을 위해 특정 hex 선택 |
| `stellar_color_temp_k` | 3195 | high | 유도 |

## Surface synthesis

Barnard 의 광구는 NearStars 카탈로그에서 가장 어두운 편에 속합니다.
0.003558 L☉, 0.187 R☉, Teff 3195 K 로 볼로미터릭 출력은 태양의
약 1/280 입니다. M4 V 로서 Proxima (M5.5V, 2980 K) 보다 두 서브타입
더 뜨겁고 HD 69830 / 61 Vir 류 analog 보다 두 단계 더 차갑습니다.
가시 영역 SED 는 여전히 TiO 와 VO 분자 밴드가 지배하지만, 더 깊은
빨강의 M5–M7 영역보다 "열린" pseudocontinuum 을 이미 보입니다. sub-solar
[Fe/H] = −0.15 는 태양 금속성 M4 대비 TiO 밴드 깊이를 약간 약화시키며,
이는 더 푸른 연속체 톤에 기여합니다. cfg 의 `#bd4a2c` 는 금속성이
풍부한 M4 V 의 더 깊은 빨강-갈색이 아닌 밝은 빨강-오렌지 쪽으로
편향됐습니다.

CHARA 간섭계 limb darkening (Rains 2021) 은 반지름을 0.5% 정밀도로
제약하지만 H 밴드 limb darkening 지수를 직접 분해하지는 않습니다.
cfg 는 Claret 2018 PHOENIX grid 보간에서 가져온 α ≈ 0.4 를 tie-break
으로 채택합니다. 실제 프로파일은 이 Teff 의 1D 대기에서 잘 모델링되지
않는 색채권 filling 에 의존합니다. Cristofari 2024 의 SPIRou NIR 스펙트럼은
관측 데이터에서 18000 개 이상의 흡수 특징을 식별했지만 대응하는
PHOENIX-ACES 모델에서는 약 6800 개만 식별되며, 이 2.7× 격차는 지속적인
M 왜성 대기 모델 불완전성을 강조합니다.

게임 내 초근접 렌더링에 필요한 해상도의 granulation 시뮬레이션은
수행되지 않았습니다. M 왜성 granulation 셀은 이 압력 스케일 높이에서
~20–30 km 너비로 스케일되어야 하며, 이는 Proxima 보다 약간 크지만 중간 M
태양 analog 보다는 작습니다. 활동 사이클 동안 흑점 면적은 낮은 활동
수준 때문에 Barnard 에 대해 직접 TiO 밴드 모델링되지 않았습니다.
게임 내 흑점 비율은 Toledo-Padrón 2019 회전 변조 진폭과 일관된 1–2%
상한에 머물러야 합니다.

## Atmosphere synthesis

Barnard 의 색채권과 코로나는 잘 연구된 모든 M4 왜성 중 가장 조용합니다.
log R'HK = −5.69 (Toledo-Padrón 2019) 는 현대 태양 (log R'HK ≈ −4.9)
보다도 비활동적인 수준이며, 145 d 회전 주기에서의 색채권 활동 유도
RV 신호는 상한이 단지 1 m s⁻¹ 입니다. 너무 작아서 같은 논문이 14.5
년의 멀티 분광기 결합 분석을 통해서야 회전을 회수할 수 있었습니다.
색채권 Hα 프로파일은 방출이 아닌 약한 흡수 상태이며, 일부 카탈로그에
채택된 legacy "Ve" 분류와 모순됩니다. cfg 는 이에 따라 "M4.0 V" 를
사용합니다.

코로나는 희미합니다. France 외 2020 (Mega-MUSCLES) 은 HST STIS/COS
와 Chandra ACIS-S 동시 스펙트럼을 얻어 약 50 ks 의 결합 노출에서
세 개의 개별 flare (FUV 2건, X선 1건) 를 탐지했고, 이로부터 헤드라인의
25% flare 듀티 사이클을 도출했습니다. 정상상태 X선 광도는 M 왜성
영역의 하단 (log L_X ~ 25.5 cgs, 보수적으로) 이며 flare 상태에서는
log L_X ~ 27.5 까지 상승해서 ~5000 s decay 시간 스케일에 걸쳐 개별
사건 에너지 ~10²⁹·² erg 를 보입니다. cfg 는 정상상태 + flare 피크 속도
및 듀티 사이클을 함께 인코딩해서, 하류의 Kerbalism 복사 환경 루틴이
시간 평균 노출을 샘플링할 수 있도록 합니다.

XUV 환경은 광학 활동도가 시사하는 것보다 가상의 거주 가능 영역 행성에
더 까다롭습니다. Duvvuri 2021 이 differential emission measure 모델링으로
EUV (100–912 Å) 스펙트럼을 재구성한 결과, 1 AU 에서의 정상상태 적분
플럭스는 0.018 erg cm⁻² s⁻¹, flare 플럭스는 0.146 erg cm⁻² s⁻¹ (~8×
부스트) 입니다. France 2020 은 이 플럭스를 HZ (0.1 AU) 의 가상 자기장
없는 지구형 행성에 열적 + 이온 손실 escape 모델로 전파한 결과, 정상상태
XUV 만으로는 대기 가열률이 현대 지구의 태양 극대기 수준 — *파국이 아닌*
— 임을 발견했습니다. 그러나 25% flare 듀티 사이클에 걸쳐 적분하면 누적
손실은 ~87 지구대기 Gyr⁻¹ (열적 하이드로다이내믹 escape) + ~3 지구대기
Gyr⁻¹ (이온 픽업 escape) 입니다. a = 0.019–0.038 AU 의 내부 시스템 행성에
대해 이 속도는 단위 면적당 7–28× 더 커지며, 유지된 1차 대기에 대한 강한
제약이 됩니다.

자기장은 SPIRou Legacy Survey 가 2018 년부터 Stokes V (원편광) 으로
특성화해 왔습니다. Cristofari 2024 는 자세한 자기 측정의 존재를 언급하지만
종방향 자기장 자체를 추출하지는 않습니다. Reiners 2022 CARMENES Zeeman
broadening 추정은 약 200 G 의 평균 표면장을 시사합니다 — M 왜성 기준으로는
모데스트한 수준이며 (Proxima 는 약 4 kG 에 도달, AU Mic 같은 어린 중간
M 은 1 kG 초과), 분광 폴라리메트리에서 추론한 ordered 쌍극자 성분은
더 작아서 노쇠한 나이와 느린 회전과 일관됩니다.

## Rotation & spin synthesis

145 ± 15-d 회전 주기 (Toledo-Padrón 2019) 는 모든 field M 왜성에 대해
측정된 가장 긴 회전 주기 중 하나이며, 10 Gyr 자기 제동의 동역학적
서명입니다. González Hernández 2024 가 ESPRESSO 색채권 지표에서
주기를 140 d 로, 2차 고조파를 71 d 로 독립적으로 회수해 잘 일치합니다.
느린 회전은 표준 Newton 2018 / Engle 2018 noisy M 왜성용 자이로
크로놀로지 관계를 통해 운동학적 나이 추정을 강화합니다.

10 ± 2 yr 의 활동 사이클 (Toledo-Padrón 2019) 또는 3200 d ≈ 8.8 yr
(González Hernández 2024) 는 색채권 활동 인덱스와 장기 평균 RV 를
수 m s⁻¹ 변조합니다. 사이클은 지속 시간 측면에서 태양과 비슷하지만
훨씬 약한 다이나모로 구동되며, 진폭은 Reiners & Mohanty 2012 가 예측한
느린 회전자 영역과 일관됩니다.

Barnard 에서 asteroseismic 진동은 검출되지 않습니다. 모든 M 왜성과
마찬가지로 표면 중력이 너무 크고 대류 진폭이 너무 작기 때문입니다.
미분 회전은 분해되지 않았으며 회전축의 경사도 제약되지 않았습니다.

## Visual styling

Barnard 는 NearStars 에서 딥 레드 M4 V 로 렌더링됩니다. 광구 톤
`#bd4a2c` 는 Proxima 의 더 깊은 빨강 `#c54c2a` 와 GJ 1214 / AU Mic
analog 같은 중간 M 레퍼런스의 따뜻한 빨강-오렌지 사이에 위치합니다.
sub-solar [Fe/H] = −0.15 는 5500–7000 Å 영역을 지배하는 TiO 및 VO
분자 밴드 흡수를 약화시킴으로써 가시 연속체를 태양 금속성 M4 대비
오렌지 쪽으로 약간 밀어냅니다.

별은 절대 각도 크기는 작지만 가까운 행성들에서는 큽니다. d 의 0.0188
AU 에서 5.3°, b 의 0.0229 AU 에서 4.3°, c 의 0.0274 AU 에서 3.6°,
e 의 0.0381 AU 에서 2.6° 를 차지합니다. 네 행성 모두에서 별은 지구에서
본 태양의 5–10× 각지름을 채우며, 낮 하늘을 지배하는 일정한 어둑한
빨강 원반으로 보입니다.

Flare 는 Proxima 대비 가시적이지만 드뭅니다. France 2020 의 25% 듀티
사이클은 HST/Chandra 민감 밴드에서 연속 관측 4 일당 약 1 flare 의
검출 가능성을 의미하지만, 개별 flare 에너지는 가시 영역에서 강한
brightening 을 일으키는 임계값 아래입니다. cfg 의 `visual_flare_color_hex
= #ff5e36` 은 peak 방출 동안 색을 약간 오렌지 쪽으로 이동시켜 모데스트한
Hα + 푸른 연속체 brightening 을 흉내냅니다. 강도는 Proxima analog 보다
현저히 낮습니다. Superflare (≥ 10³³ erg) 는 Barnard 에 대해 문서화된
바 없으며, cfg 는 별도 superflare 항목을 포함하지 않습니다. 기존 flare
cfg 가 관측된 에너지 분포를 커버합니다.

코로나는 매우 흐릿한 청백색 halo 로 렌더링되며 10 년 사이클의 X선 밝은
위상 동안 약간 밝아집니다. 확장된 FUV 플럭스가 고에너지 SED 를 지배
하지만 맨눈 관측에는 보이지 않습니다. 게임 내 효과는 flare 동안의
주변광 색 이동과 항성 디스크의 가시 Hα brightening 으로 제한됩니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star* (`2024A&A...690A..79G`, arXiv:2410.00569).
  현재 Barnard b 의 ESPRESSO 발견. 회전 주기 140 d, 장기 사이클
  3200 d, Ribas 2018 반박.
- **Basant R. et al. 2025** — *Four Sub-Earth Planets Orbiting
  Barnard's Star from MAROON-X and ESPRESSO* (`2025ApJ...982L...1B`,
  arXiv:2503.08095). 30 cm/s 정밀도의 b, c, d, e MAROON-X 확인.
  전체 4-행성 궤도 + 질량 테이블.
- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star: very slow rotation and evidence for long-term
  activity cycle* (`2019MNRAS.488.5145T`, arXiv:1812.06712). P_rot
  = 145 ± 15 d, 10-yr 사이클, log R'HK, 나이 추정.
- **Cristofari P. et al. 2024** — *Comprehensive High-resolution
  Chemical Spectroscopy of Barnard's Star with SPIRou* (arXiv:2310.12125).
  T_eff = 3231 ± 21 K 대안 피팅, 15-원소 abundance, B-field 의 SPIRou
  분광 폴라리메트리 기준선.
- **Duvvuri G. et al. 2021** — *Reconstructing the Extreme Ultraviolet
  Emission of Cool Dwarfs Using Differential Emission Measure
  Polynomials* (arXiv:2102.08493). DEM EUV 재구성, Barnard 정상상태
  및 flare EUV 플럭스.
- **France K. et al. 2020** — *The High-Energy Radiation Environment
  Around a 10 Gyr M Dwarf: Habitable at Last?* (arXiv:2009.01259).
  Mega-MUSCLES HST + Chandra, 25% flare 듀티 사이클, HZ 에서의 대기
  손실률.
- **Mann A. W. et al. 2015** — *How to Constrain Your M Dwarf*
  (`2015ApJ...804...64M`, arXiv:1501.01635). M–K 질량 관계, DB
  recommended 질량.
- **Rains A. D. et al. 2021** — *Characterization of 92 southern TESS
  candidate planet hosts* (`2021MNRAS.504.5788R`, arXiv:2102.08133).
  Barnard CHARA 간섭계 반지름.
- **Boyajian T. S. et al. 2012** — *Stellar Diameters and Temperatures
  II* (`2012ApJ...757..112B`, arXiv:1208.2431). 독립적 간섭계 R + Teff
  확인.
- **Marfil E. et al. 2021** — *The CARMENES search for exoplanets
  around M dwarfs: Stellar atmospheric parameters* (`2021A&A...656A.162M`,
  arXiv:2110.07329). [Fe/H] = −0.15.

### Read (context / methodology, not decision-driving)

- **Lubin J. et al. 2021** — *Stellar Activity Manifesting at a
  One-year Alias Explains Barnard b as a False Positive*
  (`2021AJ....162...61L`. no arXiv). Ribas 2018 super-Earth 반박.
  abstract 인용.
- **Ribas I. et al. 2018** — *A candidate super-Earth planet orbiting
  near the snow line of Barnard's star* (`2018Natur.563..365R`,
  arXiv:1811.05955). 역사적 클레임, 반박됨. 문헌 연속성을 위해
  보존.
- **Stefanov A. K. et al. 2024** — *A sub-Earth-mass planet orbiting
  Barnard's star: No evidence of transits in TESS photometry*
  (arXiv:2410.00577). González Hernández 2024 와 짝을 이루는 transit
  배제 논문.
- **Choi J. et al. 2013** — *Precise Doppler Monitoring of Barnard's
  Star* (arXiv:1208.2273). 장기 RV 제약, 발견 이전 상한.
- **Paulson D. B. et al. 2006** — *Optical Spectroscopy of a Flare on
  Barnard's Star* (arXiv:astro-ph/0511281). 단일 flare 사건 특성화.
- **Kürster M. et al. 2003** — *Low-level RV variability in Barnard's
  Star* (arXiv:astro-ph/0303528). secular acceleration + 활동 서명.
- **Reiners A. et al. 2022** — M 왜성 CARMENES Zeeman 분석, Barnard
  평균장 제약 (특정 Phase 3 arXiv 미인출 — sample 작업에서 추론).

### Read (instrument-only, not visual-informative)

- **Liebert J. et al. 2005** — *Barnard's Star and the M Dwarf
  Temperature Scale*. 캘리브레이션 방법론만.
- **Benedict G. F. et al. 1998** — *HST Fine Guidance Sensor
  photometry of Proxima and Barnard*. astrometric 방법론만.

### Not read — no arXiv preprint or low-priority (~130 papers)

Barnard 문헌은 행성 탐색 벤치마크 + 근접성 때문에 큽니다. 스킵된 풀
은 다음을 포함합니다.

- 2000 년 이전 분광형 확인 및 고유운동 측정
- 역사적 Van de Kamp astrometric 클레임 (1960–80 년대)
- Barnard 를 RV 표준으로 사용하는 기기 개발 논문
- 중적외선 직접 영상화 상한 (CanariCam 1507.01254 등)
- SETI / 성간 미션 타겟팅 제안서

`docs/phase3/_bib/barnards-star.yaml` 에 `status: skipped` 로 보존.

## Open items for follow-up

- **Stokes V 를 통한 자기 쌍극자 강도**. Cristofari 2024 는 SPIRou
  분광 데이터를 사용하지만 종방향 자기장을 추출하지는 않습니다.
  같은 데이터셋의 표적화된 ZDI (Zeeman Doppler Imaging) 분석은
  현재 200 G 의 tie-break 인 cfg `magnetic_total_field_G_mean`
  항목을 더 단단히 만들 수 있습니다.
- **Lubin 2021 미인출**. Ribas 2018 의 canonical 반박은 arXiv
  preprint 가 없습니다. 사용자가 붙여넣은 abstract 나 본문이
  있다면 Ribas 2018 의 논의를 "abstract 인용" 에서 "deep-read" 로
  격상할 수 있습니다.
- **Flare 빈도 캘리브레이션**. France 2020 은 단일 HST + Chandra
  epoch 에서 25% 듀티 사이클을 보고 — 한 번의 관측 스냅샷입니다.
  cfg `flare_rate_per_day_total = 0.1` 는 tie-break 입니다.
  Barnard 의 TESS 섹터 모니터링이 ~10²⁹-erg flare 영역의 광도
  감도에 도달하면 이를 개선할 수 있습니다.
- **Phase 3 금속성 범위**. Marfil 2021 은 −0.15 ± 0.16 dex 를
  보고하고, Cristofari 2024 는 PHOENIX 모델 입력으로 ~ −0.5
  dex 를 선호하며, Duvvuri 2021 은 Ribas 의 −0.32 를 채택합니다.
  광학 + NIR 에 걸쳐 일관된 가정으로 동질화된 재유도가 범위를
  좁힐 수 있습니다.
- **흑점 면적 비율**. 게임 내 흑점 렌더링은 현재 1–2% 광도
  상한을 사용합니다. 직접 TiO 밴드 깊이 변조 분석 (Berdyugina
  2017 프레임워크) 은 사이클 변조 면적을 개선할 수 있습니다.
- **DB 분광형 "M4.0 Ve"**. 방출 한정자가 붙은 legacy 분류는 깊이
  비활동적 log R'HK 와 흡수 상태 Hα 프로파일과 충돌합니다. DB
  를 "M4.0 V" 로 업데이트할 것을 권장합니다. cfg 는 이미 "e"
  를 제거했습니다.

## Related

- [barnards-star-b](barnards-star-b.md), [barnards-star-c](barnards-star-c.md), [barnards-star-d](barnards-star-d.md), [barnards-star-e](barnards-star-e.md) — HZ 안쪽 가장자리 내부의 확정된 sub-Earth 행성 가족
- [proxima-cen](proxima-cen.md) — 비슷한 거리 + 분광 서브타입. 활동도 대비 (Barnard 조용, Proxima 활동적)
- [methodology](../reference/methodology.md) — Decisions 스키마 출처
- [data-sources](../reference/data-sources.md) — 논문 인용 정책
- [mod-reference](../reference/mod-reference.md) — 이 별 필드를 소비하는 하류 cfg writer
- [rex-data-comparison](../reference/rex-data-comparison.md) — Barnard 는 REX 에 폐기된 Ribas 2018 행성과 함께 등장. NS 는 2024–2025 ESPRESSO/MAROON-X 시스템 반영
