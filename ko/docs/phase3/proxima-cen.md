<!-- Proxima Cen Phase 3 synthesis: cfg-ready 시각 결정과 근거 -->
# Proxima Cen — Phase 3 Synthesis

NearStars KSP mod 의 Phase 3 항성 synthesis (2026-05-22 작성).

Proxima Cen 은 1.302 pc 거리의 M5.5 Ve 완전 대류 dwarf — 태양계와 가장
가까운 별이자 확인 행성 두 개 (b, d) + 후보 한 개 (c, 논란) 의 호스트.
질량 0.1221 ± 0.0022 M☉ (Suárez Mascareño et al. 2025 진화 모델, Mann
et al. 2019 의 K-band 보정과 일관), 반지름 0.1410 ± 0.0070 R☉ (Boyajian
et al. 2012 의 CHARA 간섭계), 광도 0.00155 ± 0.00006 L☉ (Boyajian 2012
볼로미터 플럭스). 이 광도에서 고전 거주 가능 영역은 ~0.04–0.08 AU 에
있고 그 안의 궤도 주기는 5–20 일.

Proxima 는 ~8700 AU 장반경, e ≈ 0.5, P ≈ 547 kyr (Kervella, Thévenin
& Lovis 2017) 의 wide hierarchical 궤도로 Alpha Cen AB 에 중력적으로
묶여 있어 시스템을 삼중성계로, Proxima 를 공유 나이 동반자 (~5 Gyr;
AB 에 적용되는 Joyce & Chaboyer 2018) 로 만듭니다. 이 노년에도 불구하고
Proxima 는 가장 자기적으로 활동적인 근거리 M dwarf 중 하나 — 완전 대류
dwarf 가 포화 dynamo 영역에서 가지는 전형적 속성.

NearStars 에서의 목표는 두드러진 flare 활동, 고대비 흑점 지도, Alpha Cen
AB 와의 "가장 가까운 이웃" 관계를 시각화하는 행성계를 가진 deep-red M5.5
Ve 디스크.

**NearStars 시나리오 선택. 디스크 표면 최대 20% 를 덮는 흑점 complex 와
현실적 flare 일정을 가진 deep-red flare-active M dwarf** — flare 는 궤도
행성에 가끔 극적인 밝기 증가 이벤트, 드문 superflare (~10 yr cadence) 는
게임플레이 관련 rad-storm 이벤트.

## Decisions

Kopernicus 별 cfg-ready 값.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `mass_msun` | 0.1221 | high | Suárez Mascareño 2025; Mann 2019 K-band |
| `radius_rsun` | 0.1410 | high | Boyajian et al. 2012 CHARA 간섭계 |
| `teff_k` | 2904 | high | Passegger et al. 2019 CARMENES 고분해 |
| `luminosity_lsun` | 0.00155 | high | Boyajian et al. 2012 볼로미터 플럭스 |
| `spectype` | M5.5 Ve | high | Bessell 1991, Bidelman & MacConnell 1973 의 현대적 개정 |
| `metallicity_fe_h_dex` | +0.05 | medium | Passegger et al. 2019 CARMENES; M dwarf 금속함량 불확실성 큼 |
| `age_gyr` | 4.85 ± 0.5 | medium | 운동학 (Kervella 2017 의 AB 결합) |
| `rotation_period_days` | 83.0 | high | Suárez Mascareño et al. 2016 장기 baseline 측광 |
| `obliquity_deg` | 0 | low | 채택 |
| `surface_color_temp_k` | 2900 | high | limb-darkened 평균 쪽 가중 |
| `surface_tint_rgb_hex` | `#ff6028` | medium | 흑체 2900 K → CIE 색도, deep red-orange (시각적으로 ~580 nm dominant) |
| `corona_tint_rgb_hex` | `#ff8030` | low | 더 밝은 flare-loop 색조 |
| `limb_darkening_coeff_quadratic_a` | 0.55 | medium | 강한 M-dwarf limb darkening; Claret 2017 + TiO 밴드 불투명도 |
| `limb_darkening_coeff_quadratic_b` | 0.25 | medium | 동일 |
| `granulation_cell_size_arcsec` | 0.4e-3 | medium | G/K dwarf 보다 작음; M-dwarf grad-Brun 대류 |
| `convective_overshoot_pct` | 30 | medium | 완전 대류; 복사 core 없음 |
| `magnetic_cycle_period_yr` | 7 | medium | Wargelin et al. 2017 X-ray + Suárez Mascareño 2016 Hα 사이클 |
| `spot_coverage_max_pct` | 20 | medium | Reiners & Basri 2008 Bcoll 제약 + Tregloan-Reed 2024 분광편광 매핑 |
| `spot_temperature_offset_k` | -500 | low | M-dwarf umbra T_spot/T_quiet ≈ 0.85; spot 2400 K vs 광구 2900 K |
| `xray_log_lx_erg_s` | 27.2 | high | Wargelin et al. 2017 Chandra 평온 + flare 평균 |
| `xray_cycle_factor` | 2.0 | medium | Wargelin 2017 사이클 진폭 |
| `flare_rate_per_day_amplitude_log10` | -1.4 | high | Howard et al. 2018 + Vida et al. 2019 + MacGregor 2018 |
| `superflare_rate_per_yr_amplitude_log33_5_erg` | 0.1 | medium | Howard 2018 — 1 superflare/decade 차원 |
| `wind_mass_loss_rate_msun_yr` | 1e-13 | medium | Wood et al. 2021 (개정) — 태양의 5–7× 더 높음 |
| `wind_terminal_velocity_km_s` | 1500 | medium | Garraffo et al. 2017 MHD wind 모델 |
| `chromosphere_h_alpha_ew_angstrom` | 4.5 | high | Newton et al. 2017 카탈로그 평균 |
| `chromosphere_log_rhk` | -5.55 | high | Suárez Mascareño et al. 2016 |
| `magnetic_field_strength_kg` | 0.6 | high | Reiners & Basri 2008 — Bcoll ≈ 600 G; Klein et al. 2021 ZDI |
| `apparent_diameter_arcsec_from_sol` | 0.0010 | high | derived |
| `apparent_magnitude_v_from_sol` | 11.29 | high | Gaia DR3 변환 |
| `companion_alpha_ab_separation_au` | 8700 | medium | Kervella et al. 2017 |
| `interstellar_extinction_av_mag` | 0.0 | high | LIC, 무시 가능 reddening |

## Stellar disk synthesis

Proxima Cen 은 노년 완전 대류 M dwarf 의 가장 가까운 예. 0.1410 R☉ 의
물리 디스크는 태양의 7× 작지만 Boyajian et al. 2012 의 CHARA Array
간섭계가 지구 기준 시직경 1.044 ± 0.080 mas 측정 — 현재 baseline 간섭계
(CHARA, VLTI) 에서 여전히 분해 가능. 근거리 별들 중 가장 작은 물리적,
시직경.

**색 선택.** Teff = 2904 K (Passegger 2019, 추천 고분해 분광값; Suárez
Mascareño 2025 항목의 기존 raw teff = 3498 K 는 대부분 M5.5Ve 결정 대비
이상하여 Phase 2 큐레이션에서 조정). 2904 K 에서 흑체는 1.0 μm 근처
(deep 근적외) 에서 피크이고, 600 nm 이하 가시 스펙트럼은 크게 억제됨.
디스크 적분 색도는 장파장 발광이 지배 — RGB ≈ `#ff6028` (deep red-
orange). G2 V 별과 비교하면 분명히 적색, Alpha B 의 `#ffe9c4` warm
yellow K1 V 를 한참 지나침. 시각적으로 이는 M dwarf 와 흔히 결합되는
"화성형" 적색.

**Limb darkening.** 상부 광구의 TiO 밴드 불투명도가 견인하는 강한
M-dwarf limb darkening (a ≈ 0.55, b ≈ 0.25). 가장자리 밝기는 디스크
중심의 ~25%, 가장자리 근처에서 상당한 추가 적색 편이. TiO 밴드는 또한
M dwarf 에 그들의 독특한 스펙트럼 모양을 부여하는 특징적 broadband
흡수를 만듭니다.

**입상.** M dwarf 는 G/K dwarf 보다 작은 입상 셀 (Brun & Browning 2017
완전 대류 dynamo 이론). 지구 거리에서 셀 규모 ~0.4e-3 arcsec — 현재
장비로 미분해이나 시간 분해 측광 노이즈에서 검출 가능. 대류 속도는 상부
광구에서 ~1.5 km/s.

**흑점.** Reiners & Basri 2008 이 Stokes I + V 에서 Bcoll ≈ 600 G 검출;
Klein et al. 2021 ZDI 지도가 ~kG 흑점 영역 우세의 복잡한 다극 기하 확인.
사이클 극대기 측광 변광 진폭 (V 에서 ~1.5%) 은 ~20% 디스크 표면이 흑점으로
덮임을 의미, Tregloan-Reed et al. 2024 분광편광 매핑과 일관. 흑점 온도
~2400 K (umbra) vs 2900 K (평온 광구) — G/K dwarf (500 K vs ~1500 K)
보다 더 작은 상대 온도 차이.

흑점 패턴은 동적 — 여러 complex 가 ~30–60일 시간 척도에 wax 와 wane,
지배 complex 가 경도 이동 (Klein 2021 ZDI 의 강한 차등 회전; 적도-극
주기 비 ~1.4 와 일관).

**Flare rate.** Howard et al. 2018 이 MOST + ASAS-SN 장기 baseline 데이터로
flare 누적 분포 도출.
- M-class flare (~10³² erg). ~1/day
- 더 큰 flare (~10³³ erg). ~1/week
- X-class superflare (~10³⁴ erg). ~1/month
- Superflare (>10³⁵ erg). ~1/decade (MacGregor et al. 2018 이 2016년 3월
  에 평온 14,000× 진폭의 한 건 검출)

가장 격렬한 superflare 는 분 동안 평온의 ~1000× 밝기 도달. 궤도 행성에는
생물학적/전기적으로 catastrophic — 방사선 dose 가 평균 수준의 10⁵× 까지
치솟을 수 있음.

**진동 또는 oscillation 검출 안됨.** 완전 대류 M dwarf 는 G/K dwarf 처럼
p-mode 진동을 보일 것이 기대 안됨. Suárez Mascareño 2025 의 RV 잔차는
활동과 자전 modulation 만 보이고 oscillation 신호 없음.

## Activity and variability synthesis

**자전주기. 83.0 ± 0.8 일** (Suárez Mascareño et al. 2016 의 장기 baseline
ASAS + HARPS 측광에서; Benedict et al. 1998 의 83.5 d 와 일관). M dwarf
로서 *느림* — 이 나이의 대부분 M5.5 dwarf 는 10–30 d 로 자전. Proxima 의
느린 자전은 자기 제동과 노년과 일관이나 완전 대류 내부와 결합되면 관찰된
강한 활동을 예측하지 못함. 설명. 완전 대류 dwarf 는 활동이 saturation
임계값 너머 자전 속도와 decouple 되는 포화 dynamo 가 있음.

**자기 사이클. ~7 년** (Wargelin et al. 2017 Chandra X-ray 모니터링;
Suárez Mascareño 2016 Hα). 더 느린 자전임에도 태양 11-yr 사이클보다
주목할 만하게 짧음. 사이클 진폭은 X-ray 에서 factor ~2 — 태양 factor ~10
대비 약함.

**log R'_HK = -5.55** (Suárez Mascareño 2016). "비활동" Ca II H&K 진단
값임에도 Proxima 의 Hα 발광 (EW ~4.5 Å, Newton 2017) 과 X-ray 광도
(log L_X ≈ 27.2, 태양 log L_X = 25.6 보다 ~30× 높음) 는 강한 채층 및 corona
가열 시사. 불일치는 log R'_HK 가 완전 대류 dwarf 측정을 억제하는 saturation
floor 가 있기 때문 — Hα 가 M dwarf 의 더 민감한 활동 진단.

**자기장. ~600 G longitudinal 평균** (Reiners & Basri 2008). Zeeman Doppler
이미지 (Klein et al. 2021) 는 지배적 고위도 흑점 complex 와 약한 dipolar
구성요소를 가진 복잡한 다극 topology 표시. 기하는 사이클 동안 변하나
태양만큼 정렬된 적은 없음.

**Coronal mass ejection.** 1.3 pc 의 Proxima 에서 CME 직접 검출은 도전적.
MacGregor et al. 2018 은 2016년 3월 superflare 의 간접 증거 (millimeter-
wave continuum) 가 동반 CME 시사 보고. ALMA 후속 관측 (Howard 2018) 은
CME 질량과 속도를 큰 태양 CME 와 비슷하지만 훨씬 빈번 — 사이클 극대기
동안 일일 다수 이벤트 — 으로 제약.

**항성풍.** Wood et al. 2021 의 개정된 Ly-α 흡수 분석은 질량 손실 ~1e-13
M☉/yr — 단위 면적당 mass 로는 태양 질량 손실의 ~5× 더 높음이나 절대 단위
로는 낮음. b 의 궤도 (~30 R★) 에서 wind 속도는 supersonic 으로 1500 km/s
도달, 지구 자기권에 대한 태양풍보다 ~30× 더 많은 입자 flux 를 b 의
자기권에 부착.

**별 위의 oroal 진단.** Proxima 자체의 채층 Hα 발광이 자기 활동의 "오로라
서명" 으로 작용. flare 이벤트 동안 라인 코어가 빠르게 채워짐. 채층 Lyman-α
발광도 활동과 유사하게 상관.

## System geometry synthesis

Proxima 는 현 에포크에서 Alpha AB 중심에서 ~15,000 AU 거리, 투영 시각
분리 ~2°. Kervella, Thévenin & Lovis 2017 의 hierarchical-orbit 분석.
- 장반경. 8700 AU
- 이심률. 0.5
- 주기. 547,000 년
- Periastron 통과. ~280 kyr 후 (Proxima 가 다음 AB 에 접근하는 시점)

현 에포크의 궤도 phase 는 periastron 에서 먼 위치 — Proxima 는 ~270 kyr
동안 계속 외향으로 drift 후 되돌아옴.

**Proxima 프레임에서** Alpha AB 는 찬란한 단일 별로 출현 (apastron 에서
분리 ~12", 작은 광학 보조로 분해 가능하나 육안에는 한 점으로 출현).
합산 시각 등급 V ≈ -7 — 지구에서 보는 금성보다 ~100× 더 밝아, Proxima
행성 표면에 야간 가시 그림자 던짐. 색. cream-yellow (Alpha A 의 더 높은
광도 지배).

**Proxima 행성에서** (b 는 0.0485 AU, d 는 0.0288 AU) Proxima 자체가
하늘을 지배.
- b 에서. Proxima 시직경 1.5° (지구에서 보는 태양의 3× 시직경). 디스크는
  깊은 적색, 가시 흑점 complex (디스크 대비 흑점 큼).
- d 에서. Proxima 시직경 2.4° (지구에서 보는 태양의 5× 시직경). 더 극적.

flare 동안 디스크 밝기는 초 안에 10–100× 치솟을 수 있어, 분 동안 일시적
"두 번째 일광" 생성. superflare (~10 yr 마다) 의 경우, 밝기가 1000× 치솟아
deep-red 평소 디스크 전반에 UV-blue shift 된 빛으로 30초 동안 태양 등가
플럭스 전달.

## Visual styling

- **전체 모습.** Deep red-orange 디스크 (~`#ff6028` 색도). warm-yellow
  Alpha B 와 white-yellow Alpha A 와 분명히 구분. "red M dwarf" archetype.
- **궤도체에 대한 dayside 조명.** 색온도 ~2900 K — Proxima b 의 대기 산란이
  적-주황 하늘 (푸르지 않음) 생성, 표면 조명이 장파장으로 편향. 임의 생물군
  이 이용 가능한 가시광 photosynthesis envelope 가 심하게 제약됨; deep-red
  와 근적외 광자가 지배.
- **디스크 밝기 프로파일.** 강한 limb darkening (가장자리 ~25% of 중심);
  TiO 밴드 onset 으로 가장자리가 추가 적색화. 디스크는 태양의 golden-edged
  디스크보다 모든 sector 에 걸쳐 더 균일하게 적색으로 출현.
- **흑점 가시성.** 사이클 극대기에 디스크 표면 최대 20% 를 덮는 여러 큰
  어두운 흑점 complex, 각각 ~10–20° 시직경. 흑점은 ~500 K 차가움 (G/K
  dwarf 흑점만큼 깊은 contrast 아님) 이지만 *분수* 면적이 훨씬 큼.
  KSP 등가. 83-day 자전에 가시적으로 디스크를 가로지르는 절차적 어두운
  패치; 패턴은 ~50일마다 재구성.
- **Flare.** 불규칙 간격의 밝은 flare 밝기 증가 이벤트. 밝기 비. M-class
  ~5×, X-class ~50×, superflare ~1000× 평온. 지속 시간. 분 ~ 시간.
  KSP 등가. 가끔의 UV-blue 섬광 이벤트와 국지 밝기 증가; 드문 full-디스크
  superflare 이벤트.
- **동반성 Alpha AB.** V = -7 의 찬란한 점광원, 색 cream-yellow, 수 세기에
  걸친 하늘 가로 느린 drift. 주요 feature. Proxima 행성에서 가시 Proxima
  이외의 가장 밝은 광원.
- **분광선.** TiO 밴드 지배 (5448, 6159, 6651 Å); Hα 발광 (사이클 변광);
  적색에서 강한 CaH 밴드; 태양 등가 파장의 K I, Na D, Mg I b 이지만 강하게
  포화된 코어. 근적외가 밝음 (피크 발광), λ > 1.4 μm 에서 H₂O 와 CO 밴드.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2012ApJ...757..112B** Boyajian et al. 2012 — CHARA 간섭계 시직경
  (1.044 ± 0.080 mas) 과 볼로미터 광도 (0.00155 ± 0.00006 L☉). 결정적
  반지름/광도 소스.
- **2019A&A...627A.161P** Passegger et al. 2019 — CARMENES 고분해 근적외
  분광. Teff = 2904 ± 51 K, [Fe/H] = +0.05 ± 0.16. 더 오래된
  Anglada-Escudé 2016 SED-fit 값보다 추천.
- **2016MNRAS.459.3565S** Suárez Mascareño et al. 2016 — 장기 baseline
  ASAS+HARPS 측광 모니터링. 결정적 자전주기 83.0 ± 0.8 d, 부분 7-yr Hα
  사이클, log R'_HK = -5.55.
- **1607.05636** Anglada-Escudé et al. 2016 — Proxima b 발견 (P=11.2 d,
  Msini=1.27 M⊕). 호스트 별 insolation 환경 cfg 에 시각 정보.
- **2204.09270** Diamond-Lowe et al. 2022 — Proxima 의 동시 X-ray + FUV
  모니터링. 임의 행성 대기 화학 관련 EUV/UV 플럭스 수준.
- **1907.12580** Vida et al. 2019 — Proxima flare 활동의 TESS 관측.
  flare 동안 quasi-periodic oscillation; superflare 특성화.
- **1608.06672** Davenport et al. 2016 — MOST 위성 모니터링; 기준 flare
  rate 측정.
- **MacGregor et al. 2018 (1803.07581)** — 2016년 3월 거대 superflare
  의 ALMA 검출 (mm 파장에서 평온 14,000×). 간접 CME 증거.
- **2102.06318** Howard et al. 2018 — ASAS-SN 장기 baseline flare 누적
  분포. ~1/decade superflare rate 제공.
- **2021MNRAS.500.1844K** Klein et al. 2021 — 여러 에포크의 Proxima
  Zeeman Doppler Imaging. 자기 기하 + 흑점 매핑.
- **2017A&A...598L...7K** Kervella, Thévenin & Lovis 2017 — Proxima 가
  AB 에 중력적으로 묶임; cfg 의 시스템 기하.

### Read (context / methodology, not decision-driving)

- **2410.01621** Garraffo et al. 2024 — M dwarf 의 magnetized stellar
  wind. cfg 에 사용하는 1500 km/s wind 속도 제공.
- **1706.04617** Garraffo et al. 2017 — TRAPPIST-1 에서의 star-planet
  자기 상호작용 MHD 시뮬레이션; Proxima b/d 의 analog framework.
- **2402.12253** Schreyer et al. 2024 — Habitable M-Earth 의 water vapour
  통과 모호성. 임의 Proxima 행성 대기 retrieval 컨텍스트.
- **2312.01893** Lichtenberg et al. 2024 — HZ 암석 외계행성의 물 함량.
  Phase 3 b reads.
- **2306.03004** Chen et al. 2023 — 동기적으로 회전하는 외계행성의 성층권
  오존. tidally locked Proxima 행성 컨텍스트.
- **2506.19779** Schmidt 2025 — 젊은 M dwarf mm 스펙트럼. Proxima 의
  채층/corona 기여 reference.
- **2410.19108** Way et al. 2024 — spin-orbit resonance 의 Earth-like
  외계행성. Proxima b 와 관련한 기후 역학.
- **2209.12502** Braam et al. 2023 — tidally locked Earth-like 세계의
  번개 화학. 대기 시각 관련.
- **2211.11887** Cohen et al. 2022 — aquaplanet 의 구름 변광.

### Read (instrument-only, not visual-informative)

- **2503.18538** PIAA + nuller 코로나그라프 paper. 방법론.
- **2602.08929** RedDots GJ 887 paper. 다른 시스템, 방법론 교차 reference.
- **2310.07827** 다른 시스템의 APRIO+RV 해. 방법론.

### Not read — no arXiv preprint available (90 papers)

2008년 이전 reference 와 학회 proceedings 포함. 미독 핵심 예시.

- "Pre-WISE" M dwarf 인구 surveys. Skip.
- 자전/활동 요약 IAU 심포지엄 proceedings. Skip.
- "TRAPPIST monitoring" 다중 타겟 compendium 요약 (Gillon 초기 작업).
  Skip — TRAPPIST-1 phase 3 가 다룸.

**사용자 액션 요청.** 2024년 이후 ZDI 캠페인이 Proxima 의 자기 기하 업데이트
출판하면 흑점 지도와 자기장 강도 정제가 필요할 수 있습니다. MacGregor 2018
ALMA 검출이 특히 중요 — superflare rate 의 더 높은 cadence follow-up 은
게임플레이 관련 superflare 일정을 정제합니다.

---

## Open items for follow-up

- 문헌 전반에 걸친 ~600 K teff 불일치 (Cifuentes 2020 의 3000 K,
  Passegger 2019 의 2904 K, Suárez Mascareño 2025 raw 항목의 3498 K)
  조정. Phase 2 는 Passegger 를 가장 신뢰할 만한 것으로 추천; consensus
  측정 출현 시 Phase 4 재방문 가능.
- 사이클 주기 (~7 yr) 가 부분 사이클 데이터로 제약; Wargelin 2017 X-ray
  데이터셋은 14년 (1.5 사이클) 걸침. 더 정밀한 결정은 2030 까지 ALMA/
  Chandra 모니터링 계속 필요.
- Superflare rate (~10³⁵ erg 이벤트의 1/decade) 가 ~30년 광학 모니터링
  기반 (한 이벤트 관측. MacGregor 2018). Poisson 불확실성 큼; rate 는
  0.3–3 per decade 가능.
- 차등 회전 진폭 (~1.4 적도-극 비, Klein 2021) 확인에 추가 ZDI 에포크 필요.
- wind 질량 손실 rate 의 Wood 2021 vs 2005 개정은 임의 Proxima-b 대기 escape
  모델에 유의; Phase 3 행성 docs 가 새 값을 reference 해야 합니다.
