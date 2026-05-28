# TRAPPIST-1 — Phase 3 Synthesis

TRAPPIST-1 (2MASS J23062928−0502285) 은 가까운 7행성 공명 사슬을 거느린
ultra-cool dwarf 입니다. Gaia DR3 거리 12.47 pc (시차 80.21 mas) 에
위치한 M8 V 별이고, 1.5–19 일 주기에 걸쳐 일곱 개의 지구 크기 세계가
공전합니다. 지금까지 특성화된 외계행성 host star 중에서 가장 작고
가장 차갑고 가장 어두운 별 중 하나로, log L*/L☉ = −3.28, 즉
태양 볼로메트릭 출력의 0.052% 에 불과합니다. 기본 매개변수는 2016년
발견 이후 여러 차례 정제되어 왔고 — 가장 최근에는 Agol 2021 의
TTV 기반 모델이 권장 세트로 자리잡았으며 DB Phase 2 층도 이를
채택합니다. M* = 0.0898 ± 0.0023 M☉, R* = 0.1192 ± 0.0013 R☉,
T_eff = 2566 ± 26 K 입니다.

이 별은 자신의 분광형 기준으로는 활동도가 중간 정도입니다. K2 측광은
3.295 ± 0.003 일의 자전 주기를 주고 (Vida 2017, Luger 2017 확인), K2
광도곡선에는 80 일 동안 42 개의 flare 가 검출됐는데 에너지는
10³⁰–10³³ erg 범위에 걸쳐 있습니다 (Vida 2017). Evryscope 의 더 긴
모니터링은 superflare (≥10³³ erg) 발생률을 연 4.2 +1.9/−0.2 회로
좁혀 줍니다 (Glazier 2020). XMM-Newton 은 log L_X (cgs) = 26.6–26.9 의
부드러운 2온도 코로나를 검출하고 (Wheatley 2017), HST/STIS 는
Ly-α 라인을 분해해 — TRAPPIST-1 을 UV 라인이 측정된 가장 차가운
exoplanet host 로 만듭니다 (Bourrier 2017). 별의 나이는 7.6 ± 2.2 Gyr
이며 (Burgasser & Mamajek 2017, CMD·밀도·운동학·리튬 없음 조건·자전·
활동도 지표의 합치), 행성계는 pre-main-sequence 이후의 긴 평형 단계에
들어가 있습니다.

**NearStars 시나리오 선택은 깊은 적색을 띠고 천천히 자전하는 ultra-cool
dwarf 입니다. 중간 정도의 chromospheric 활동, 부드러운 X-ray 코로나,
빈번한 저에너지 flare 와 드문 superflare, 진화하는 magnetic feature
패턴, 그리고 일곱 개의 강하게 조사된 암석 행성을 오랫동안 빚어 온 7.6
Gyr 의 나이를 함께 가진 모습입니다.** cfg 결정 24 개 — 22 개는
canonical 일치, 2 개는 tie-break (점 충진율과 점-광구 온도 대비.
Roettenbacher 의 어두운 점 해석과 Morris 의 밝은 점 해석이 모두
관측과 양립 가능합니다).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M8 V | high | Liebert & Gizis 2006; Gillon 2016; Burgasser 2017 (Gonzales 2019 는 M7.5 로 분류 — DB 태그는 Gaia 변환을 거친 M7.5e. M8 가 최빈 분류) |
| `mass_msun` | 0.0898 ± 0.0023 | high | Agol 2021 의 TTV 기반 진화 모델 적합. Van Grootel 2018 의 0.089 ± 0.006 과 1σ 안에서 수렴 |
| `radius_rsun` | 0.1192 ± 0.0013 | high | Agol 2021 의 SED+transit-density 적합. Van Grootel 2018 은 0.121 ± 0.003, Gonzales 2019 는 0.119 ± 0.003 |
| `teff_k` | 2566 ± 26 | high | Agol 2021 SED 적합. Van Grootel 2018 은 2516 ± 41, Gonzales 2019 는 2628 ± 42 |
| `luminosity_lsun` | 5.22e-4 ± 0.19e-4 | high | Van Grootel 2018 — 시차 갱신 볼로메트릭 flux. Gonzales 2019 는 FIRE NIR SED 로 6.09e-4 |
| `metallicity_fe_h_dex` | +0.04 ± 0.08 | medium | Gillon 2017 NIR 저해상도 분광. Burgasser 2017 의 CMD 위치는 +0.06 을 시사하고, Van Grootel 은 밀도를 화해시키려면 +0.4 도 가능하다고 언급 |
| `age_gyr` | 7.6 ± 2.2 | high | Burgasser & Mamajek 2017 — CMD·밀도·Li 없음·운동학·자전·활동도 지표의 합치 |
| `log_g_cgs` | 5.21 ± 0.06 | high | Gonzales 2019 SED 유도 |
| `rotation_period_days` | 3.295 ± 0.003 | medium | Vida 2017 K2 short-cadence. Roettenbacher & Kane 2017 의 경고: 표면이 진화함. Spitzer epoch 은 0.819 일 주기를 보였으므로 실제 자전은 ~1 일 (v sin i 6 km/s × R*) 에 가깝고, K2 의 3.3 일 신호는 활동 영역의 수명일 가능성 |
| `v_sin_i_km_s` | 6 ± 2 | high | Reiners & Basri 2010 의 FeH Zeeman 선폭 측정 |
| `activity_log_lhalpha_lbol` | −4.7 (범위 −4.85 ~ −4.60) | high | Burgasser 2017 의 Gizis 2000 / Reiners & Basri 2010 / Schmidt 2007 collation |
| `activity_log_lx_lbol` | −3.52 ± 0.17 | high | Wheatley 2017 XMM-Newton APEC fit |
| `x_ray_log_lx_cgs_quiescent` | 26.6–26.9 | high | Wheatley 2017 — L_X (0.1–2.4 keV) = (3.8–7.9) × 10²⁶ erg/s |
| `xuv_log_lxuv_lbol` | −3.1 (범위 6–9 × 10⁻⁴) | high | Wheatley 2017 의 XMM 외삽 |
| `lyman_alpha_flux_erg_s_cm2_at_earth` | 0.05 +0.01/−0.02 | high | Bourrier 2017 HST/STIS 의 복원 본래선 (d = 12 pc 에서). L_X 관계가 예측하는 값보다 훨씬 약함 → 채층이 코로나보다 조용함 |
| `magnetic_field_gauss_mean` | 600 +200/−400 | medium | Reiners & Basri 2010 FeH Zeeman; Wheatley 2017 가 "~600 G" 로 인용. 중-M 평균 1.6 ± 0.9 kG 보다 약함 |
| `flare_rate_per_day_e_above_e30_erg` | 0.53 | high | Vida 2017 — K2 Campaign 12 의 ~80 일 baseline 동안 42 개 flare. 에너지는 1.26×10³⁰ – 1.24×10³³ erg |
| `flare_rate_superflare_per_year_e_above_e33_erg` | 4.2 +1.9/−0.2 | high | Glazier 2020 — Evryscope+K2 결합 누적 FFD |
| `flare_xuv_contribution_relative_quiescent_per_yr` | 1.35 +2.0/−0.15 | medium | Howard 2025 RADYN beam-heating 모델 + TESS 대역 FFD 를 6–912 Å 으로 환산 |
| `spot_filling_fraction_max` | 0.02 (1–5% 허용) | low | Tie-break (interesting-first). Roettenbacher 2017 의 어두운 점 모델과 Morris 2018a 의 밝은 점 모델 모두 관측과 일치. cfg 는 중간값 ~2% (이 활동도의 M8 에 대해 Berdyugina 스타일의 TiO band depth 모델은 최대 5% 까지 허용) |
| `spot_temperature_contrast_k` | +2800 (밝은 facular-plage 해석) | low | Tie-break (interesting-first). Morris 2018a 의 밝은 점 (T_spot ≈ 5300 K) 은 K2 의 변조와 Spitzer 의 미검출을 동시에 설명. Roettenbacher 의 어두운 점 (T = 2200 K) 은 대안. cfg 는 (a) 파장 의존 K2 vs Spitzer 불일치를 설명하고 (b) 깊은 적색 광구를 배경으로 시각적으로 두드러진 facular 영역을 제공하기 때문에 밝은 점을 채택 |
| `visual_surface_tint_hex_primary` | `#ff5520` (깊은 적-주황의 ultra-cool M8 V) | high | 2566 K 흑체 + 6500 Å 이하의 TiO/VO 흡수대 억제. 2566 K 의 CIE 색좌표는 1 μm 부근으로 치우친 열복사 연속에 해당 |
| `visual_spot_tint_hex` | `#ffa860` (따뜻한 노란-주황의 밝은 facular plage) | low | Tie-break — 밝은 점 해석과 짝지어진 색. ~5300 K 의 더 따뜻한 점이 적색 광구를 배경으로 따뜻한 크림-노란 패치로 보임 |
| `stellar_color_temp_k` | 2566 | high | cfg 조명 색온도로 Teff 그대로 사용 |
| `limb_darkening_alpha_h` | ~0.4 | low | Tie-break — M8 V 에 대한 직접 간섭계 측정이 없음. Proxima Cen 과 마찬가지로 Claret 2018 M-dwarf 그리드에서 보간 |

## Surface synthesis

TRAPPIST-1 의 광구는 NearStars 의 행성을 확인된 host star 중 가장 작고
가장 차갑습니다. 가시 원반은 T_eff = 2566 K (Agol 2021) 에서 방출되고,
SED 는 6500 Å 보다 짧은 파장 영역에서 분자 TiO·VO opacity 로 강하게
억눌립니다 — 복사 flux 의 대부분은 1–3 μm 범위에서 흘러나옵니다
(Wilson 2021 Mega-MUSCLES). 볼로메트릭 광도는 5.22 × 10⁻⁴ L☉ 에
불과하고 (Van Grootel 2018), 이는 태양의 약 1/1900 입니다.

**색 선택.** 2566 K 흑체의 색좌표는 인간이 지각하는 색을 깊은
주황-적색의 `#ff5520` 근처에 놓고, 푸른 쪽 연속의 흡수대 억제는 시각
신호를 더 깊은 적색으로 밀어 넣습니다. Proxima Centauri 색조 `#c54c2a`
(2980 K) 와 비교하면 TRAPPIST-1 은 더 어둡고 더 채도가 높습니다. e 와
f (0.029 와 0.038 AU) 같은 거주 가능 영역 행성에서 보면, 별은
1.8–2.5° 의 시직경을 채워 지구에서 본 태양 시직경의 몇 배에 해당합니다.

**광구 팽창.** TRAPPIST-1 의 측정 항성 밀도 (51 ρ☉, Delrez via Van
Grootel 2018) 는 0.089 M☉, 7.6 Gyr 별에 대한 태양 metallicity 진화
모델 예측보다 낮습니다. 반지름은 BHAC15 / CLES isochrone 예측 대비
8–14% 가량 팽창돼 보입니다 (Burgasser 2017, Van Grootel 2018). 두
가지 해석이 살아 있습니다 — 강화된 metallicity ([Fe/H] = +0.40 정도
까지) 가 increased opacity 를 통해 외피를 팽창시키는 시나리오, 그리고
magnetic-activity 가 convective transport 를 억제해 팽창시키는
시나리오. Gonzales 2019 는 세 번째 가설을 추가합니다 — 일곱 행성의
조석 forcing 이 별의 외층을 약간 부풀린 채로 유지한다는 안입니다. 현재
데이터로는 어느 쪽인지 결정적으로 가리지 못합니다. cfg 목적상 채택된
R = 0.1192 R☉ (Agol 2021) 는 transit duration 과 TTV 유도 질량으로
직접 잘 측정된 값이고, 팽창 메커니즘과 무관합니다.

**표면 특징.** TRAPPIST-1 의 점 패턴은 활동도 문헌에서 가장 논란이 큰
주제이며, 두 해석이 모두 살아 있습니다. Roettenbacher & Kane 2017 은
K2 의 3.3 일 변조를 T_spot ≈ 2200 K 의 차가운 어두운 점으로 모델링
합니다 — 대비는 전형적 중-M dwarf 수준입니다. 이 모델은 K2 광도곡선은
설명하지만 Spitzer 4.5 μm 에서도 비슷한 변조를 예측하는데 관측은 그렇지
않습니다 (Spitzer epoch 은 0.819 일 주기를 보여 진화된 활동 영역을
시사합니다). Morris 2018a 는 파장 의존 관측을 T_spot ≳ 5300 ± 200 K
의 밝은 점 세 개로 설명하고, 각 점의 면적은 매우 작습니다 (R_spot / R* ≈
0.004). 분자 흡수대로 광구 방출이 강하게 억제된 Kepler bandpass 에서는
이 뜨거운 패치가 지배하지만, 광구의 Planck 함수가 우세한 4.5 μm 에서는
거의 기여하지 않습니다. Vasilyev 2025 는 JWST/NIRISS 에서 차가운
magnetic feature 의 증거를 추가했고 — "광구보다 기껏해야 몇백 K 낮은"
온도이며 flare 와 함께 가끔 사라집니다.

NearStars cfg 에서는 밝은 점 그림을 시각적 주역으로 채택했습니다.
이유는 (a) 파장 의존 측광 신호를 자기 일관적으로 설명하고, (b) 다른
부분은 균질한 적색 원반에 대해 시각적으로 두드러진 특징을 제공하며,
(c) Vasilyev 2025 가 magnetic feature 의 사라짐으로 돌리는 flare 후
밝아짐과 부합하기 때문입니다. 어두운 점 해석은 cfg 변형으로 Open items
에 보존됩니다. 현실적으로 두 집단은 원반 위에 공존할 가능성이 높습니다.

## Atmosphere synthesis

TRAPPIST-1 의 항성 대기 — 채층, 천이층, 코로나 — 는 Bourrier 2017
(Ly-α), Wheatley 2017 (X-ray), Wilson 2021 (Mega-MUSCLES 프로그램의
전체 UV-to-X-ray SED) 으로 특성화됩니다. 핵심 긴장 관계는 X-ray
luminosity 가 Proxima Centauri 수준 (log L_X cgs = 26.6–26.9 vs
Proxima 의 quiescent ≈ 27.0) 인 반면, Ly-α 라인 방출은 더 따뜻한 M
dwarf 에서 보정된 L_X → L_Lyα 관계가 예측하는 값보다 약 3 배
약하다는 점입니다. Bourrier 2017 은 이를 TRAPPIST-1 의 채층은 적당히
활동적이지만 코로나는 더 따뜻한 M dwarf 의 flux 수준을 유지한다는
증거로 해석합니다 — 후기 M dwarf 에서 시원한 대기 층이 뜨거운 코로나와
탈동조화되는 추세와 일치하는 결과입니다.

**Chromospheric 활동도.** log L_Hα / L_bol = −4.85 ~ −4.60 (Burgasser
2017 이 여러 epoch 자료를 collation). 이 값은 TRAPPIST-1 을 M8 V 의
중간 활동도 구간에 둡니다 — 매우 조용한 비활동 M8 도, 포화 방출의
빠른 회전 별도 아닙니다. 등가폭 측정은 Hα 방출 2.3–7.7 Å 범위에 걸쳐
있고 (Reiners & Basri 2010 / Schmidt 2007 / Burgasser 2015), 변동은
회전 변조 또는 Roettenbacher 2017 이 기록한 점 충진율 진화를 따를
가능성이 높습니다.

**Coronal X-ray.** XMM-Newton 은 2014년 12월에 TRAPPIST-1 을 30 ks
관측했고 (Wheatley 2017), kT = 0.15 와 0.83 keV 의 부드러운 2온도
APEC 플라스마를 드러냈습니다. 7.8 시간 관측 동안의 변동은 통계적으로
유의하며 — 그 당시 가정된 1.4 일 주기의 약 23% 를 덮는 회전 변조와
가능한 작은 flare 의 조합일 가능성이 큽니다. log L_X / L_bol = (2–4)
× 10⁻⁴ 는 별을 포화 영역에 둡니다 (Rossby 수 << 0.1, Roettenbacher
2017 §3.2). 적분 XUV luminosity 는 log L_XUV / L_bol = (6–9) × 10⁻⁴
로, 모든 일곱 행성에서 hydrodynamic mass loss 를 구동할 만큼 충분합니다
(Bourrier 2017 계산: 행성들에 걸쳐 총 escape rate 13–46 ton/s).

**Flare 와 포화 활동도 영역.** Vida 2017 은 K2 의 사용 가능한 80 일
cadence 동안 1.26 × 10³⁰ ~ 1.24 × 10³³ erg 사이의 42 개 flare 를
목록화했고, 이는 10³⁰ erg 이상에서 약 0.53/일의 flare 발생률을
줍니다. Glazier 2020 은 Evryscope 지상 측광 2년치를 더해 누적 FFD
분석으로 분포를 superflare 까지 확장하고, 연 4.2 +1.9/−0.2 회의
superflare (≥10³³ erg) 발생률을 얻습니다 — ultracool dwarf 기준으로는
중간이고, 거주 가능 영역의 오존 보호 대기 (만약 존재한다면) 가 이벤트
사이에 회복할 수 있을 정도로 낮은 수준입니다. Howard 2025 는 RADYN
복사-유체역학 beam-heating 모델을 JWST 관측 6 개 flare (2.2–8.7 ×
10³⁰ erg) 에 적용해, 전형적 M dwarf flare 보다 비교적 약한 전자 빔
(F_e = 10¹² erg/s/cm², E_cutoff ≤ 37 keV) 을 발견했습니다 — Maas
2022 와 Howard 2023 이 지적한 예상보다 낮은 광학 flare 온도와 일치하는
결과입니다. 누적적으로 flare 는 1년 적분 기준으로 정온 XUV 방출의 1.35
+2.0/−0.15 배를 기여하므로, 시스템의 7.6 Gyr 동안 flare 성분은 동일
정온 광도의 비flare 별 대비 행성에서의 총 XUV 조사 이력을 대체로 2 배
키워 왔습니다.

**자기장과 dynamo.** Reiners & Basri 2010 은 FeH 흡수선의 Zeeman
선폭에서 평균 자기장 약 600 G 를 측정했습니다 — 중-M 평균인 1.6 ± 0.9
kG 보다 약합니다. TRAPPIST-1 은 완전 대류 (M < 0.35 M☉) 이므로
dynamo 는 α-Ω 이 아니라 필연적으로 turbulent 입니다. 비교적 느린 회전
(3.3 일이 진짜 주기라면. Spitzer 의 더 빠른 변조가 실제 회전이라면
~1 일) 과 kG 급 자기장이 결합하면 별은 포화 활동도 영역에 들어가
(Roettenbacher 2017 §3.2), 회전이 더 빨라져도 자기 flux 가 늘어나지
않습니다. Wilson 2021 Mega-MUSCLES 는 관측되지 않는 100–912 Å EUV 를
위한 Differential Emission Measure 모델을 포함한 전체 UV-to-X-ray SED
를 제공합니다 — 행성에서의 대기 escape 계산에 결정적인 입력입니다.

## Rotation & spin synthesis

TRAPPIST-1 의 측광 자전 주기는 상당한 혼란의 원천이었습니다. 발견
논문 (Gillon 2016) 은 TRAPPIST-South 의 지상 측광에서 P_rot = 1.40 ±
0.05 일을 보고했고, 이는 R = 0.117 R☉, i = 90° 가정 시 Reiners &
Basri 2010 의 v sin i = 6 ± 2 km/s 와 일치합니다. K2 Campaign 12 의
short-cadence 관측은 3.295 ± 0.003 일의 강한 신호를 주었고 (Vida 2017,
Luger 2017), 이것이 표준적 문헌 값입니다. 그러나 K2 epoch 76 일 전의
Spitzer 관측은 v sin i 예측과 일치하는 0.819 일 주기성을 보입니다
(Roettenbacher & Kane 2017).

Spitzer 와 K2 의 불일치는 표면이 수 주에서 수 개월의 시간 척도에서
진화함을 시사합니다 — 어쩌면 측광으로 측정된 "회전 주기"가 실제로는
별의 spin 주기가 아니라 활동 영역의 수명일 만큼 빠를 수도 있습니다
(Morris 2018a 도 같은 주장). cfg 에서는 P_rot = 3.295 일 (Vida 2017)
을 표준 문헌 값으로 채택하되, 진짜 spin 주기는 ~1 일에 가까울 수
있다는 caveat 를 함께 둡니다. 이는 포화 활동도 dynamo 논의 (§4) 에서
중요하지만, 일반적인 KSP framerate 의 cfg 시각 렌더링은 크게 바뀌지
않습니다.

**Differential rotation.** Vida 2017 은 K2 광도곡선을 3.295 일 신호로
pre-whitening 한 뒤 2.915 일의 측광 2차 주기를 검출했습니다. 두 신호가
서로 다른 위도의 실제 회전이라면, 함의된 표면 shear (P_1 − P_2)/P̄ ≈
0.12 는 완전 대류 M dwarf 에 비해 너무 크고 깊은 대류 물리와
모순됩니다. 2차 신호는 differential rotation 의 흔적이라기보다 유한
수명의 활동 영역일 가능성이 더 높습니다.

**Spin 축 경사.** TRAPPIST-1 의 자전축에 대한 직접 측정은 없습니다.
행성 궤도면은 시선과 89.7°–89.9° 기울어 있고 (Agol 2021), 항성 spin 이
궤도면과 대체로 정렬돼 있다면 (Brady 2022 MAROON-X obliquity 제약
처럼), 자전축은 시선으로부터 약 60° 기울어집니다 (cfg 채택값). KSP
렌더링에서는 동기 binary 의 정확한 정렬 시야가 아니라, 가시적인
극축 기울기를 줍니다.

**KSP 구현 노트.** Sidereal 자전 주기 (초 단위) = 3.295 일 × 86400 s/d
= 284,688 s. Kopernicus 의 `rotationPeriod` 는 이 값으로 설정하면
됩니다 (또는 cfg 변형이 Spitzer-epoch 해석을 채택한다면 대안 값 0.819
일 ≈ 70,766 s).

**활동 주기 미검출.** Roettenbacher & Kane 2017 은 K2+Spitzer 결합
epoch 에서 자전 주기보다 긴 주기성을 탐색했고 설득력 있는 cycle 신호를
찾지 못했습니다. Wargelin 2024 는 비슷한 X-ray + UV 모니터링으로
Proxima Centauri 에서 ~7 년 주기를 발견했지만, TRAPPIST-1 은 비슷한
검출이 가능할 만큼 길게 관측되지 않았습니다. 다년 XMM/Swift 캠페인이
이 공백을 메우기 전까지, cfg 는 X-ray + Hα 방출을 quiescent 수준의
정상 상태로 다루고 그 위에 확률적 flare 이벤트를 얹습니다.

## Visual styling

NearStars 렌더러에서 TRAPPIST-1 은 작고 깊은 적-주황의 ultra-cool dwarf
로 묘사됩니다 — Proxima Centauri 보다 눈에 띄게 작고 더 붉은 모습입니다.

- **전체 외관.** 원반 색상 `#ff5520` (2566 K 흑체 정점의 깊은
  주황-적색). 전형적인 거주 가능 영역 거리에서의 시직경 1.5–5.5° (b 에서
  5.5°, e 에서 1.8°, h 에서 0.85°). 0.1192 R☉ (약 82,930 km 반경,
  목성 적도 반경과 비슷한 수준) 의 절대 물리 크기는 카탈로그에서 가장
  작은 축에 속합니다. b 의 0.0115 AU 에서 보면 TRAPPIST-1 은 하늘에서
  가장 큰 단일 천체입니다.
- **광구 텍스처.** 서브 arcsec 척도의 granulation 패턴 (M dwarf granule
  ~30 km, 압력 척도고에 따라 조정) — 극단적 close-up 렌더링에서만
  보입니다. 원반은 약한 limb darkening 을 보이며 (Claret 2018 M-dwarf
  그리드 외삽 기반 H 대역에서 cfg α ≈ 0.4), 가장 깊은 적색은 limb 에
  나타납니다.
- **밝은 점.** T ≈ 5300 K 의 facular plage 특징 3–5 개가 깊은 적색
  원반을 배경으로 작은 따뜻한 노란-크림 패치 (cfg `#ffa860` accent)
  로 나타나고, 각 패치는 가시 원반의 ~0.005% 를 차지합니다. 이 밝은
  점들은 3.3 일 주기로 시야 안팎을 돕니다. Vasilyev 2025 에 따르면 가끔
  flare 가 차가운 어두운 magnetic feature 의 소멸을 유발하는데 — 이
  시각 효과는 cfg 에서 flare 시점의 점 인구 변동으로 구현할 수 있습니다.
- **어두운 점 (cfg 변형).** 대안 해석 (Roettenbacher 2017): T ≈ 2200 K
  의 차가운 어두운 점이 원반의 ~1–5% 를 패치 분포로 덮습니다. 어두운
  점 변형은 표준적 M dwarf 어두운 점 그림을 선호하는 사용자를 위해 cfg
  variant 로 보존됩니다.
- **Flare.** 10³⁰ erg 이상의 누적 발생률 ~0.5/일 (Vida 2017), superflare
  (≥10³³ erg) 는 4.2/년 (Glazier 2020). Vida 의 데이터에서는 flare 의
  ~12% 가 복잡한 다중 피크 이벤트입니다. 시각적으로 cfg 는 10³¹ erg
  이벤트에서 별을 광학 0.5–2 mag 만큼 밝게 해야 하고, 10 분 ~ 1 시간
  지속되며 Davenport 2014 의 빠른 상승 / 느린 감쇠 특징적 형태를
  보입니다. 백색광 flare 스펙트럼은 hydrogen Balmer 연속 + Hα 방출이
  지배하므로, flare 시점 색은 주황-적색 쪽으로 약간 이동합니다 (Howard
  2025 RADYN 모델은 2000–4500 K 의 유효 flare 온도 예측).
- **코로나.** 정온 X-ray 단계에서는 약 2 R* 까지 뻗는 흐릿한 푸른-흰
  halo 가 보이고 (Wheatley 2017 cycle 최저), flare 시점과 (미관측인)
  활동 주기 정점에서 밝아집니다.
- **항성풍.** 직접 보이지는 않지만, 행성 magnetosphere 에 영향을 주는
  인게임 우주기상 이벤트로 전파됩니다 (Garraffo 2017 시뮬레이션).
- **Lyman-α 방출.** HST/STIS 로 분해 (Bourrier 2017) — KSP 의 렌더링
  문턱 아래이지만 행성 대기 UV 광분해의 주요 원천에 해당합니다.

일곱 행성은 서로의 시야에서 시각적으로 빽빽이 모여 있어서 — 회합 시점에
이웃 행성은 0.5–1° 의 시직경에 도달해 host 시스템의 두드러진 "위성" 처럼
보입니다. 거의 동일면 구조 (Agol 2021 에서 i = 89.7°–89.9°) 때문에
대부분의 행성-행성 회합은 동시에 거의 일식·엄폐가 되고, 며칠마다 빈번한
상호 occultation 이 일어납니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Van Grootel V. et al. 2018** — *Stellar Parameters for TRAPPIST-1*,
  ApJ 853, 30 (`2018ApJ...853...30V`, arXiv:1712.01911). 갱신된 시차
  82.4 ± 0.8 mas. 최종 항성 매개변수 M = 0.089 ± 0.006 M☉, R = 0.121 ±
  0.003 R☉, T_eff = 2516 ± 41 K, L = (5.22 ± 0.19) × 10⁻⁴ L☉. 태양
  metallicity 진화 모델과의 반지름 팽창 긴장 관계를 기록.
- **Burgasser A. J. & Mamajek E. E. 2017** — *On the Age of the
  TRAPPIST-1 System*, ApJ 845, 110 (`2017ApJ...845..110B`,
  arXiv:1706.02018). CMD, 밀도, Li 없음, 표면 중력, 운동학, 자전,
  자기 활동도 지표의 합치에서 도출한 7.6 ± 2.2 Gyr. log L_Hα/L_bol =
  −4.85 ~ −4.60 dex, log L_X/L_bol = −3.52 ± 0.17 dex, v sin i = 6
  km/s 정의.
- **Vida K. et al. 2017** — *Frequent flaring in the TRAPPIST-1 system
  — unsuited for life?*, ApJ 841, 124 (`2017ApJ...841..124V`,
  arXiv:1703.10130). K2 Campaign 12 의 short-cadence Fourier 분석.
  P_rot = 3.295 ± 0.003 일. 에너지 1.26 × 10³⁰ ~ 1.24 × 10³³ erg 의
  flare 42 개. 12% 가 complex.
- **Wheatley P. J. et al. 2017** — *Strong XUV irradiation of the
  Earth-sized exoplanets orbiting the ultracool dwarf TRAPPIST-1*,
  MNRAS 465, L74 (`2017MNRAS.465L..74W`, arXiv:1605.01564). XMM-Newton
  30 ks. 2온도 APEC 코로나. L_X/L_bol = 2–4 × 10⁻⁴. L_XUV/L_bol =
  6–9 × 10⁻⁴.
- **Bourrier V. et al. 2017** — *Reconnaissance of the TRAPPIST-1
  exoplanet system in the Lyman-α line*, A&A 599, L3
  (`2017A&A...599L...3B`, arXiv:1702.07004). HST/STIS Ly-α 복원 라인
  프로파일. UV 측정된 가장 차가운 exoplanet host. L_X 관계 예측보다
  Ly-α 훨씬 약함 → 시원한 대기가 코로나보다 조용함.
- **Roettenbacher R. M. & Kane S. R. 2017** — *The Stellar Activity of
  TRAPPIST-1 and Consequences for the Planetary Atmospheres*, ApJ 851,
  77 (`2017ApJ...851...77R`, arXiv:1711.02676). K2 vs Spitzer 측광
  주기 불일치 (3.30 일 vs 0.819 일). 진화하는 점 패턴. T_spot ≈ 2200 K
  의 어두운 점 모델.
- **Morris B. M. et al. 2018** — *Possible Bright Starspots on
  TRAPPIST-1*, ApJ 857, 39 (`2018ApJ...857...39M`, arXiv:1803.04543).
  R_spot/R* ≈ 0.004, T_spot ≳ 5300 K 의 점 세 개를 가진 밝은 점 해석.
  K2/Spitzer 의 파장 의존 진폭 불일치를 해결.
- **Wilson D. J. et al. 2021** — *The Mega-MUSCLES Spectral Energy
  Distribution of TRAPPIST-1*, ApJ 911, 18 (`2021ApJ...911...18W`,
  arXiv:2102.11415). HST COS+STIS, XMM-Newton, DEM 모델을 결합한 5 Å
  ~ 100 μm SED. 행성 대기 모델링용 반경험적 UV 스펙트럼.
- **Glazier A. L. et al. 2020** — *Evryscope and K2 Constraints on
  TRAPPIST-1 Superflare Occurrence and Planetary Habitability*, ApJ
  900, 27 (`2020ApJ...900...27G`, arXiv:2006.14712). Evryscope 170 일
  + K2 80 일 결합. 누적 superflare 발생률 (≥10³³ erg) = 4.2 +1.9/−0.2
  회/년.
- **Vasilyev V. et al. 2025** — *Flares on TRAPPIST-1 Reveal the
  Spectrum of Magnetic Features on Its Surface*, ApJ 989, L53
  (`2025ApJ...989L..53V`, arXiv:2508.04793). JWST/NIRISS 에서 flare
  후 flux 증가. flare 가 유발한 어두운 magnetic feature 의 사라짐으로
  해석. M8 활동 영역의 첫 추정 스펙트럼.
- **Howard W. S. et al. 2025** — *Separating Flare and Secondary
  Atmospheric Signals with RADYN Modeling of JWST Transmission
  Spectroscopy*, ApJ 994, L31 (`2025ApJ...994L..31H`,
  arXiv:2512.04265). 6 개 JWST flare 의 RADYN beam-heating 모델.
  TESS-XUV 환산 인자 R_XUV/TESS = 3.6 +0.6/−2.5. 누적 flare XUV =
  1.35 × quiescent.
- **Gonzales E. C. et al. 2019** — *A Reanalysis of the Fundamental
  Parameters and Age of TRAPPIST-1*, ApJ 886, 131
  (`2019ApJ...886..131G`, arXiv:1909.13859). FIRE NIR 분광 + Gaia
  시차. log L_bol = −3.216 ± 0.016. T_eff = 2628 ± 42 K. 자기 inflation
  또는 행성 조석 상호작용을 시사하는 intermediate-gravity 분류.

### Read (context / methodology, not decision-driving)

- **Gillon M. et al. 2016** — *Temperate Earth-sized planets transiting
  a nearby ultracool dwarf star*, Nature 533, 221
  (`2016Natur.533..221G`, arXiv:1605.07211). 발견 논문. 원래 항성
  매개변수 M = 0.082 ± 0.011 M☉, R = 0.114 ± 0.006 R☉, T = 2555 ± 85
  K. P_rot = 1.40 ± 0.05 일 (지금은 K2 가 대체).
- **Gillon M. et al. 2017** — *Seven temperate terrestrial planets
  around the nearby ultracool dwarf star TRAPPIST-1*, Nature 542, 456
  (`2017Natur.542..456G`, arXiv:1703.01424). Spitzer 20 일 캠페인과
  행성 발견. NIR 분광에서 [Fe/H] = +0.04 ± 0.08.
- **Luger R. et al. 2017** — *A seven-planet resonant chain in
  TRAPPIST-1*, Nature Astronomy 1, E.129 (`2017NatAs...1E.129L`,
  arXiv:1703.04166). K2 Campaign 12 관측. P_rot = 3.3 일 확인.
  TRAPPIST-1 을 "낮은 활동도의 중년 후기 M dwarf" 로 특성화.
- **Reiners A. & Basri G. 2010** — *A Volume-Limited Sample of 63
  M7-M9.5 Dwarfs II*, ApJ 710, 924 (`2010ApJ...710..924R`,
  arXiv:0912.4259). M7-M9.5 표본의 평균 자기장 1.6 ± 0.9 kG.
  TRAPPIST-1 은 ~600 G (Wheatley 2017, Burgasser 2017 에서 참조).
- **Filippazzo J. C. et al. 2015** — *Fundamental Parameters and
  Spectral Energy Distributions of Young and Field Age Objects with
  Masses Spanning the Stellar to Planetary Regime*, ApJ 810, 158
  (`2015ApJ...810..158F`, arXiv:1508.01767). TRAPPIST-1 을 포함하는
  ultracool dwarf 들의 기준 SED-적합 기본 매개변수. Van Grootel 이전의
  참조.
- **Reiners A. et al. 2018** — *The CARMENES search for exoplanets
  around M dwarfs. High-resolution optical and near-infrared spectra
  of 324 survey stars*, A&A 612, A49 (`2018A&A...612A..49R`,
  arXiv:1711.06576). CARMENES Zeeman 선폭 조사 방법론. TRAPPIST-1 이
  M dwarf 비교 표본에 포함.
- **Garraffo C. et al. 2017** — *The Threatening Magnetic and Plasma
  Environment of the TRAPPIST-1 Planets*, ApJ 843, L33
  (`2017ApJ...843L..33G`, arXiv:1706.04617). MHD 항성풍 시뮬레이션.
  안쪽 행성 궤도의 ~50% 가 sub-Alfvénic 통과.
- **Ducrot E. et al. 2020** — *TRAPPIST-1: Global results of the
  Spitzer Exploration Science Program SPECULOOS*, A&A 640, A112
  (`2020A&A...640A.112D`, arXiv:2006.13826). 5년 Spitzer 캠페인. 대안
  항성 밀도 / R = 0.1234 R☉ 측정. DB 에서는 Agol 2021 이 대체.
- **Paudel R. R. et al. 2018** — *K2 Ultracool Dwarfs Survey III.
  White Light Flares Are Ubiquitous in M6-L0 Dwarfs*, ApJ 858, 55
  (`2018ApJ...858...55P`, arXiv:1803.07708). M6-L0 의 flare 통계.
  TRAPPIST-1 을 ultracool dwarf 의 flare-rate-vs-age 맥락에 둠.
- **Morris B. M. et al. 2018b** — *Non-detection of Contamination
  by Stellar Activity in the Spitzer Transit Light Curves of
  TRAPPIST-1*, ApJ 863, L32 (`2018ApJ...863L..32M`,
  arXiv:1808.02808). Spitzer transit timing 잔차에서 spot-crossing
  특징 없음. transit-chord 위의 점 분포에 제약.

### Read (instrument / non-cfg-decisive)

- **Davoudi F. et al. 2024** — *Updated Spectral Characteristics for
  the Ultracool Dwarf TRAPPIST-1*, ApJ 970, L4 (`2024ApJ...970L...4D`).
  NIR 분광 지수 갱신. cfg 결정에 영향 줄 매개변수 변경 없음.
- **Seli B. et al. 2021** — *Activity of TRAPPIST-1 analogue stars
  observed with TESS*, A&A 650, A138 (arXiv:2103.13540). M8 V dwarf
  비교 표본. flare-rate 맥락은 제공하지만 TRAPPIST-1 특정 새 측정은
  없음.
- **TRAPPIST-1 JWST Community Initiative et al. 2024** — *A roadmap
  for the atmospheric characterization of terrestrial exoplanets with
  JWST* (arXiv:2310.15895). 시스템 수준 관측 프로그램 동기. Agol 2021
  의 항성 매개변수와 Wilson 2021 의 활동도를 인용.
- **Howard W. S. et al. 2023** — *Characterizing the Near-infrared
  Spectra of Flares from TRAPPIST-1 during JWST Transits*, ApJ 959,
  64 (`2023ApJ...959...64H`, arXiv:2310.03792 — 전체 텍스트 fetch
  실패, abstract 만 가용). Howard 2025 의 선행 작업. 예상보다 낮은
  flare 온도를 특성화.

### Not read — no arXiv preprint or low-priority (~280 papers)

항성 중심 bibliography 에는 `_bib/trappist-1.yaml` 에서 `status:
skipped` 로 필터링된 관련도 낮은 논문이 ~280 편 포함됩니다. 분류는
다음과 같습니다.

- TRAPPIST-1 을 표본에 포함하지만 개별 특성화는 하지 않는 중-후기 M
  dwarf 통계 논문 (~80 편)
- TRAPPIST-1 의 항성 매개변수를 인용하지만 새로운 항성 측정은 기여
  하지 않는 행성-대기 모델링 논문 (~50 편. 다수가 행성별 b–h bib 에
  이미 커버됨)
- arXiv 가 없는 컨퍼런스 proceedings, abstract, 미션 컨셉 논문 (~80 편)
- TRAPPIST-1 을 표적으로 한 SETI / radio-technosignature 조사 (~10 편)
- 다른 많은 표적과 함께 TRAPPIST-1 이 들어간 발견 이전 갈색왜성 /
  ultracool dwarf 조사 (~30 편)
- TRAPPIST-1 을 참조 표적으로 사용한 이론적 M dwarf habitability 논문
  (~30 편)

필터링된 전체 bib 는 `docs/phase3/_bib/trappist-1.yaml` 에 dropped
항목마다 `status: skipped` 주석이 달린 채 보존됩니다.

## Open items for follow-up

- **점 모델 해결.** 어두운 점 (Roettenbacher 2017) 과 밝은 점 (Morris
  2018a) 해석은 관측적으로 여전히 축퇴 상태입니다. 다중 대역 JWST +
  지상 동시 관측 캠페인 (또는 미래 ELT 의 고분해능 원반 영상) 이
  축퇴를 깰 수 있습니다. cfg 변형: T_spot = 2200 K, 1–5% 충진율의
  어두운 점 시나리오.
- **실제 자전 주기.** 실제 항성 spin 이 K2 의 3.295 일 (Vida 2017)
  인지, Spitzer epoch 의 0.819 일 (Roettenbacher 2017) 에 더 가까운지
  해소되지 않았습니다. v sin i = 6 km/s 는 합리적인 R 에 대해 더 짧은
  주기를 선호합니다. 다중 대역의 긴 baseline 측광 캠페인이
  epoch-vs-주기 진화를 추적하면, 측광 신호가 회전인지 활동-영역-수명
  기원인지 명확히 할 수 있습니다.
- **활동 주기 검출.** 명확한 chromospheric 또는 coronal cycle 이
  검출되지 않았습니다. Proxima Cen 의 7년 X-ray cycle (Wargelin 2024)
  과의 비교는 TRAPPIST-1 의 다년 XMM/Chandra 모니터링 프로그램의
  근거가 됩니다. cfg 의 J2000.0 위상 동기화는 현재 임의 — cycle 이
  검출되면 cfg 의 활동-구동 CME flux 가 실시간 진행을 추적할 수
  있습니다.
- **반지름 팽창 메커니즘.** 태양 metallicity 진화 모델 대비 8–14% 의
  반지름 팽창 (Burgasser 2017, Van Grootel 2018) 은 미해명 상태입니다.
  α-원소 abundance 의 고해상도 광학 분광 (Veyette 2016 방법) 이 고
  metallicity 가설을 검증할 수 있습니다. 또는 더 깊은 자기 활동도
  모델링 (Feiden & Chaboyer 2014) 이 spot-blocking 해석을 테스트할
  수 있습니다.
- **Howard 2023 (arXiv:2310.03792) 전체 텍스트 재조회.** 이 합성
  과정에서 arXiv 전체 텍스트 fetch 가 실패했고, bibliography 항목에는
  abstract 만 사용 가능했습니다. ar5iv 에 재시도하거나 (수동 paste)
  하면 cfg 가 특정 NIR flare 유효 온도를 기록할 수 있습니다.
- **Gillon 2016 TRAPPIST-South 1.40 일 측광 주기 재검토.**
  Roettenbacher 2017 은 이를 활동-영역 패턴의 아티팩트로 일축합니다.
  만약 Morris 2018a 의 밝은 점 해석이 맞다면 1.40 일은 물리적일 수
  있습니다 — 대칭적 두 점 구성에서 K2 주기의 절반이 되는 식입니다.
  cfg 는 편견 없이 3.295 일을 채택합니다.

## Related

- [trappist-1-b](trappist-1-b.md) ~ [trappist-1-h](trappist-1-h.md) — 공명 사슬의 일곱 개 지구 크기 행성
- [proxima-cen](proxima-cen.md) — 가장 가까운 M dwarf 비교 대상. 더 따뜻 (2980 K vs 2566 K), 더 빠른 회전 (82.6 일 vs 3.3 일), 더 강한 flare
- [methodology](../reference/methodology.md) — Decisions 표의 DB 스키마
- [mod-reference](../reference/mod-reference.md) — 이 Phase 3 stellar 값을 소비하는 하류 KSP 모드
- [rex-data-comparison](../reference/rex-data-comparison.md) — §10 가 TRAPPIST-1 시스템의 Phase 3 → REX delta 를 정량화
