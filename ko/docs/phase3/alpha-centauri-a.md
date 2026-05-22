<!-- Alpha Centauri A Phase 3 synthesis: cfg-ready 시각 결정과 근거 -->
# Alpha Centauri A — Phase 3 Synthesis

NearStars KSP mod 의 Phase 3 항성 synthesis (2026-05-22 작성).

Alpha Centauri A 는 태양계 밖에서 가장 태양과 닮은 별이면서 거리가 가깝고
잘 측정된 별입니다. 분광형 G2 V (태양과 같은 MK 분류) 의 왜성으로 질량
1.1055 ± 0.0039 M☉ (Pourbaix & Boffin 2016 의 다중성계 역학 해), 반지름
1.2234 ± 0.0053 R☉ (Kervella et al. 2017 의 VLTI/PIONIER 간섭계), 광도
1.521 ± 0.013 L☉. 1.347 pc 거리에 있는 Alpha Centauri AB 쌍성의 약간 더
무거운 주성이며, Proxima Cen 이 약 8700 AU 거리에서 외곽 동반성으로 묶여
삼중성계를 구성합니다.

NearStars 에서의 목표는 Sun-twin 별이되 시각적으로는 지구 등가 거리에서
관찰했을 때 태양보다 시직경이 좀 더 크고, 광도가 약간 더 강하며, 유효
온도가 아주 살짝 낮다는 정도로 구분되도록 하는 것입니다. 2025년 기준으로
JWST/NIRCam 코로나그라프가 거주 가능 영역에 거대 행성 후보 (Beichman et al.
2025, arXiv:2508.03814 / "Worlds Next Door") 를 보고했는데 — 이 검출은 현재
후보 단계이며 NearStars 행성 인벤토리에는 *반영하지 않지만*, 시스템의
서사를 형성합니다.

**NearStars 시나리오 선택. 초태양 금속함량 시각 색조의 Sun-twin** —
태양보다 살짝 따뜻하고 노랗게 보이는 G2 V 디스크, 20 일 자전주기, 태양극대기
수준의 약한 흑점 점유.

## Decisions

Kopernicus 별 cfg-ready 값. `Confidence`. high = 직접 측정 또는 강한 제약,
medium = 강한 지지의 이론, low = 허용 윈도우 내 미적 선택.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `mass_msun` | 1.1055 | high | Pourbaix & Boffin 2016 binary_orbit |
| `radius_rsun` | 1.2234 | high | Kervella et al. 2017 VLTI/PIONIER |
| `teff_k` | 5847 | high | Porto de Mello et al. 2008 고분해 분광 |
| `luminosity_lsun` | 1.521 | high | Kervella et al. 2017 볼로미터 플럭스 |
| `spectype` | G2 V | high | Keenan & McNeil 1989 (교과서) |
| `metallicity_fe_h_dex` | +0.24 | high | Porto de Mello et al. 2008 |
| `age_gyr` | 4.81 ± 0.5 | medium | Joyce & Chaboyer 2018 MESA + 진동학 |
| `rotation_period_days` | 22 | medium | DeWarf et al. 2010 측광 모니터링 |
| `obliquity_deg` | 0 | low | 채택 (자전축 기울기 측정 없음); 태양 analog |
| `surface_color_temp_k` | 5810 | high | Teff 와 limb-darkened 평균 사이의 가중값 (약 30 K 더 차갑게) |
| `surface_tint_rgb_hex` | `#fff6e0` | medium | 흑체 5810 K → CIE D58 색도, 태양 `#fff5e6` 대비 아주 옅은 cream-yellow |
| `corona_tint_rgb_hex` | `#ffeacb` | low | 약간 더 따뜻한 corona 헤이즈 (cycle minimum); 적색 성분 미세 증가 |
| `limb_darkening_coeff_quadratic_a` | 0.30 | medium | Claret 2017 4계수 → KSP용 2계수 축약 |
| `limb_darkening_coeff_quadratic_b` | 0.30 | medium | 위와 동일 |
| `granulation_cell_size_arcsec` | 1.3e-3 | medium | Bigot et al. 2008 / Bedding 2014 — 태양형 입상 Mm 규모 |
| `convective_overshoot_pct` | 12 | medium | Joyce & Chaboyer 2018 best-fit overshoot 0.10–0.15 |
| `magnetic_cycle_period_yr` | 19 | medium | DeWarf et al. 2010 (태양 11 yr 와 비교) |
| `spot_coverage_max_pct` | 1 | low | 매우 낮은 활동; 극대기 태양 analog |
| `spot_temperature_offset_k` | -1500 | medium | 태양 umbra ~3800 K → 5800-3800 ≈ -2000 K; 태양 analog penumbra ~5000 K → -800 K; 중간값 -1500 K |
| `xray_log_lx_erg_s` | 27.0 | medium | Ayres 2014 — 태양형, 사이클 평균 |
| `xray_cycle_factor` | 3.0 | medium | DeWarf 2010 — 약한 사이클 진폭 |
| `flare_rate_per_day_amplitude_log10` | -3 | medium | 낮음 — 태양형 quiet 별; Howard 2023 의 노년 G dwarf 통계 |
| `wind_mass_loss_rate_msun_yr` | 1.5e-14 | medium | Wood et al. 2005 의 Ly-α astrosphere 흡수 |
| `wind_terminal_velocity_km_s` | 700 | medium | 태양풍 analog (slow-wind 지배) |
| `chromosphere_ca_ii_log_rhk` | -4.95 | high | DeWarf et al. 2010 |
| `helioseismic_p_mode_max_freq_mhz` | 2.4 | high | Bouchy & Carrier 2002, Bazot 2007 — p-mode 엔벨로프 2.4 mHz 부근 피크 |
| `apparent_diameter_arcsec_from_sol` | 0.0085 | high | derived. 2 × 1.2234 R☉ / 1.347 pc × 206265 |
| `apparent_magnitude_v_from_sol` | -0.01 | high | Hipparcos/SIMBAD |
| `companion_b_max_separation_arcsec` | 12 | high | a × (1+e) at apastron. 17.57" × 1.5179 → 36.0 AU 천구 투영 |
| `companion_b_min_separation_arcsec` | 1.7 | high | a × (1-e) at periastron. 11.4 AU 천구 투영 |
| `companion_b_orbit_period_yr` | 79.91 | high | Pourbaix 2002 / Kervella 2016 — WDS 14396-6050 AB 와 동일 |
| `proxima_separation_au_from_a` | 8700 | medium | Kervella, Thévenin & Lovis 2017 — 묶인 외곽 궤도 (e=0.5, P=547 kyr) |
| `interstellar_extinction_av_mag` | 0.0 | high | Local Interstellar Cloud; column density ≪ 1 |

## Stellar disk synthesis

Alpha Cen A 의 디스크는 태양계 가장 가까운 곳에서 태양과 가장 비슷한
analog 입니다. Kervella 2017 의 간섭계 시직경 8.502 ± 0.038 mas (지구
관측 기준) 에서 지구로부터의 시직경은 0.0085" — 태양 시직경 1924" 의 약
1/65. KSP 의 가상 모성 (Alpha A 자체 주위 1 AU analog 궤도 가정) 에서는
지구에서 보는 태양보다 시직경이 약 22% 더 크고, 광속(luminous flux) 은
약 52% 더 강하게 보입니다.

**색 선택.** Teff = 5847 K (Porto de Mello 2008 AB 쌍 고분해 분광) 에서
광구 흑체는 ~496 nm 에서 피크. 태양 limb darkening 커널과 함께 CIE 1931
적분하면, 인지되는 색도는 태양의 D55 reference white 와 매우 가까이 떨어집니다
— 옅은 cream-yellow, 육안으로는 구분 불가. KSP 는 `#fff6e0` (Sol 의 일반적
`#fff5e6` 보다 살짝 더 따뜻) 을 채택, 이는 +57 K 더 높은 Teff 와 super-solar
금속함량 ([Fe/H] = +0.24, Porto de Mello 2008) 의 약간 강화된 불투명도를
반영합니다.

**입상 (Granulation).** Bigot et al. 2008 은 진동학적 측광 잔차에서 입상
노이즈를 검출 — Mm 규모 "salt and pepper" 텍스처 (지구 기준 ~1.5e-3 arcsec,
현재 장비로는 미분해). KSP 렌더링 규모 (별은 빌보드로 렌더) 에서 이는 분
단위 시간 척도의 미세한 0.1 magnitude 깜빡임으로만 나타나며, 시뮬레이션
시. Phase 3 cfg 는 특성 시간만 노트로 남기고 활동 시뮬레이션은 요구하지 않습니다.

**Limb darkening.** Quadratic 계수 (a ≈ b ≈ 0.30) 의 태양 등가값이 디스크
가장자리 dimming 을 재현. Kervella 2017 의 PIONIER 분석은 Claret 4-parameter
법칙으로 피팅하나 KSP 에는 2계수 축약이 디스크 중심 밝기 충실도의 약 2% 만
손실시키며 충분합니다. Limb 는 적당히 어두워지고 (μ=0.1 에서 ~0.40 배),
경로 길이 증가로 인해 약간 더 적색.

**P-mode 진동.** Bouchy & Carrier 2002 와 Bazot 2007 이 envelope peak ~2.4 mHz
(주기 ~7분), 진폭 ~25 cm/s 의 태양형 p-mode 검출. 디스크 적분 밝기로 환산하면
5–10분 척도의 sub-percent 깜빡임 — 육안 불가시이나 이 별 주위 고정밀 RV
행성 탐색에는 중요. KSP 에서는 렌더링 안 함.

**Magnetic halo 플레어 없음.** 22일 자전은 매우 낮은 Rossby number 와 깊은
대류 envelope 결합으로 저활동 다이나모 결과. Howard 2023 통계는 태양 twin
플레어율을 ~10⁻³ M-class flare/day 로 보며, superflare (EX > 10³⁵ erg) 는
~5 Gyr 나이에서 무시 가능.

## Activity and variability synthesis

DeWarf et al. 2010 은 Alpha Cen A 를 측광으로 7년 (2003–2010), Ca II H&K 로
분광 모니터링하여 자전주기와 활동 사이클을 도출. 주요 결과.

- **자전주기**. 22 ± 3 일. 태양형 (태양 적도 P_rot = 25.4 d, 극 ~31 d,
  평균 ~26 d). ~80% 태양 나이 (Joyce & Chaboyer 2018 의 4.81 Gyr vs
  태양 4.57 Gyr) 와 일관되게 태양보다 약간 빠름.
- **자기 사이클**. ~19 yr (vs 태양 22-yr Hale / 11-yr Schwabe). DeWarf
  2010 이 베이스라인 안에서 부분 사이클 검출; 주기는 느슨하게 제약됨.
- **log R'_HK**. -4.95 (평균), 사이클 진폭 ~0.05 dex. 태양보다 평균 채층
  활동이 낮음 (태양 log R'_HK ≈ -4.91 활동 극대, -4.99 극소). Alpha A 는
  G2 V 활동 envelope 의 비활동 극단, 나이와 느린 자전과 일관.
- **X-ray 광도**. log L_X ≈ 27.0 erg/s (Ayres 2014; Robrade & Schmitt 2005).
  사이클 진폭 factor ~3× — 태양 ~10× X-ray 사이클 대비 약함.

**흑점 점유.** 측광 변광 진폭 (V 에서 peak-to-peak <1%) 과 채층 활동
지수에서 추정. 사이클 극대기 디스크 점유 <1%. 시각. 극대 시 1–3개 작은
(~5° 시직경) 흑점 그룹이 중위도에 분포. 흑점 온도 ~4300 K (umbra), ~5500 K
(penumbra) — 평온 광구 평균보다 약 1500 K 낮음.

**테크노시그너처 검출 안됨.** Foster et al. 2022 (arXiv:2211.11756) 의
광학 레이저 탐색과 Smith et al. 2024 (arXiv:2206.14807) 의 태양 중력렌즈
전파 탐색 모두 null. 완전성 목적으로만 언급; 시각 영향 없음.

**Corona 구조.** Wood et al. 2005 의 Ly-α astrosphere 흡수 검출은 항성풍
질량 손실 ~1.5e-14 M☉/yr, 태양 질량 손실의 ~7%. 뜨거운 corona (T ~ 2e6 K) 는
태양의 quiet-Sun 상태와 유사. KSP 에서는 totality/eclipse 렌더링 시 가시
coronal ray 구조 의미, flare 이벤트 시 적색 편이된 CME 분출 (드물게).

## System geometry synthesis

AB 쌍성계의 상호 가시성은 NearStars Alpha Cen 경험을 정의하는 특징입니다.

**Alpha A 의 국지 기준 프레임**에서 Alpha Cen B 는 타원 궤도를 그리며.
- 주기. 79.91 ± 0.01 yr (Pourbaix 2002, Kervella 2016)
- 장반경. 23.52 AU (a_arcsec = 17.57" × d = 1.347 pc)
- 이심률. 0.5179
- Periastron 분리. ~11.4 AU (~태양-토성 거리)
- Apastron 분리. ~35.7 AU (~태양-해왕성 거리)

AB 가 거주 가능 영역 circumbinary 행성을 안정적으로 호스팅하기에는 너무
넓지만, 각 별의 행성 인벤토리가 상대 별의 영향을 받기에는 충분히 좁음.
A 표면에서 B 의 겉보기 밝기는 periastron 에서 V ≈ -21 정도 (점광원이지만
지구에서 토성 거리의 태양 분광 등가), apastron 에서 V ≈ -19 (지구의 1/4 달
밝기 정도이지만 여전히 점광원).

**A 주위 가상 지구 analog** (1.25 AU, 고전 HZ) 의 경우. 하늘의 태양은
Alpha A 가 지구에서 보는 태양과 같은 시직경 (L=1.52 와 ~1.25 AU 궤도이므로).
B 는 V ≈ -20 (가장 어두움) ~ V ≈ -22 (가장 밝음) 범위의 변광 밝은 점광원.
지구의 금성보다 훨씬 밝아, 반대편 (opposition) 일 때 야간 반구를 극적으로
조명. B 의 빛이 던지는 그림자는 검출 가능하나 A 의 주광에 비해 10⁻³ 수준.

**Proxima 가시성.** Alpha A 표면에서 Proxima 는 ~+5 등급의 희미한 별로
보임 — 육안으로 보이지만 평범. 천구 운동 ~0.1"/yr (시스템 고유 운동 + AB
중심 주위 Proxima 소형 궤도 운동의 미분).

**A 주위 확인 행성 없음.** Wagner et al. 2021 NEAR 코로나그라프 탐색은
~1.1 AU 의 C1 후보를 보고했으나 후에 열복사 배경원으로 귀속. 2026-05-22
기준 가장 최근의 Beichman et al. 2025 (2508.03814) JWST/NIRCam 코로나그라프는
~1.5–2 AU HZ 내 *후보* 따뜻한 거대 행성을 보고; 단일 에포크이며 포화
혼동으로 검출 신뢰도 미정. NearStars cfg 는 확인 전까지 미포함.

## Visual styling

디스크와 활동 결정의 조합.

- **전체 모습.** 거의 완벽한 Sun-twin. 육안 관찰자는 Alpha A 와 Sol 을
  구분할 수 없음; 미세한 차이 (높은 Teff 로 인한 약간 높은 색온도, 높은
  금속함량으로 인한 약간 더 노랑-따뜻) 가 시각 그라데이션 인식 안에서
  상쇄.
- **궤도체에 대한 dayside 조명.** Sol 과 동일한 색온도 reference (표면
  조명 계산에 ~5810 K). 지구 analog 의 대기 산란은 Sol 의 지구 관측과
  유사한 푸른 하늘 / 노랑 태양 외관을 만듭니다.
- **디스크 밝기 프로파일.** 태양 등가 quadratic limb darkening; 디스크
  중심 밝음, 가장자리에서 ~40% 상대 밝기. 자전으로 인한 명확한 위도 띠
  없음.
- **흑점 가시성.** 사이클 극대기에 ±20–35° 위도에 1–3개 작은 어두운 흑점,
  각각 ~5° 시직경. 가장 큰 흑점은 직접 이미징되는 HZ 궤도에서 가시
  (KSP 등가. 활동 사이클 극대 시점에 절차적 어두운 패치 렌더).
- **동반성 B.** 어떤 Alpha A 궤도 어디에서나 늘 하늘에 존재. 1.25 AU HZ
  궤도에서 ~5° elongation min, ~16° at max. 79.91-yr 주기 동안 밝은
  아침/저녁 별 (apastron) 과 태양 가까이의 찬란한 동반성 (periastron) 사이를
  순환.
- **Proxima Cen.** ~+5 등급 점광원, Alpha B 에서 ~2° (수 세기에 걸친
  느린 drift). 육안으로 배경 별들과 구분 불가.
- **AR overlay 용 분광선.** H-α 6563 Å (적색, 채층 발광에서 지배적),
  Ca II H/K 3933/3968 Å (청-자색, 활동 진단), Mg I b triplet 5167-5184 Å,
  Na D doublet 5890/5896 Å.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2017A&A...597A.137K** Kervella et al. 2017 — VLTI/PIONIER 의 A 의
  시직경 (8.502 ± 0.038 mas) 과 B (5.999 ± 0.025 mas) 간섭계 측정.
  결정적 반지름 소스. 같은 데이터 + Hipparcos parallax 에서 볼로미터
  광도 도출.
- **2008A&A...488..653P** Porto de Mello et al. 2008 — A 와 B 의 차등
  고분해 분광 분석. 결정적 Teff 와 [Fe/H] 소스. 시스템을 super-solar
  금속함량으로 확립.
- **2018ApJ...864...99J** Joyce & Chaboyer 2018 — A 와 B 모두에 대한
  MESA + 진동학 모델링. 시스템 나이 4.81 ± 0.50 Gyr. 오랜 기간 더
  나이든 (~6 Gyr) Bazot 2007 와 Thévenin 2002 진동학 나이 간의 긴장을
  해소.
- **2010ApJ...722..343D** DeWarf et al. 2010 — 7년 지상 측광 + Ca II
  H&K 모니터링. 결정적 자전주기 (A 22 d, B 41 d), 부분 활동 사이클,
  log R'_HK 측정.
- **2016A&A...586A..90P** Pourbaix & Boffin 2016 — 역학 쌍성 궤도 해.
  질량 1.1055 ± 0.0039 M☉ (A), 0.9373 ± 0.0033 M☉ (B). 고정밀
  현대 reference 궤도.
- **2017A&A...598L...7K** Kervella, Thévenin & Lovis 2017 — Proxima 가
  AB 에 8700 AU 에서 중력적으로 묶여 있음을 운동학적으로 확인 (e = 0.5,
  P = 547 kyr).
- **2008A&A...488..635B** Bigot et al. 2008 — A 의 진동학적 입상 노이즈
  검출과 대류 overshoot 제약. 시각 cfg 에 쓰는 입상 셀 규모를 제공.
- **2007A&A...470..295B** Bazot et al. 2007 — HARPS 진동학 p-mode 검출.
  독립적 (비역학) 방법으로 M = 1.105 ± 0.007 M☉, R = 1.224 ± 0.003 R☉ 확인.

### Read (context / methodology, not decision-driving)

- **2508.03814** Beichman et al. 2025 — JWST/NIRCam 코로나그라프의 A 의
  HZ 내 따뜻한 거대 행성 후보 검출. 시스템 컨텍스트로만 서사에 언급.
  확인 (단일 에포크, 포화 systematics) 전까지 NearStars 행성 인벤토리에
  미포함.
- **2104.10086** Akeson et al. 2021 — AB 의 ALMA 밀리미터 천문측정.
  궤도를 개선하나 Pourbaix 2002 해를 의미있게 바꾸지 않음.
- **2110.12565** Wagner et al. 2021 — NEAR/VLT 열-IR 코로나그라프 탐색.
  C1 후보를 보고했지만 후에 배경원으로 귀속. 행성 제약 컨텍스트로 유용.
- **2105.00034** Quarles & Lissauer 2018 — Alpha Cen-like 쌍성계 안 외계
  위성 역학 안정성. 가능한 행성 인벤토리 컨텍스트.
- **2108.12650** AB 쌍성계 안 Earth-analogue 의 Milankovitch 사이클.
  Quarles et al. — HZ 행성 자전축 기울기 / 기후 진화 컨텍스트.
- **2015A&A...582A..49H** Heiter et al. 2015 — FGK Gaia benchmark 별
  분석. 독립적 Teff = 5792 ± 16 K, [Fe/H] = +0.26 ± 0.08, Porto de Mello
  교차 검증.

### Read (instrument-only, not visual-informative)

- **2211.11756** Foster et al. 2022 — AB 의 광학 SETI 레이저 탐색. Null.
  방법론만.
- **2206.14807** Smith et al. 2022 — 태양 중력렌즈 전파 테크노시그너처
  탐색. Null.
- **2304.13779** Saide et al. 2023 — 모바일 타워 전파 누출 시뮬레이션.
  방법론, Alpha 특화 과학 아님.
- **2301.11314** Trees & Stam 2023 — Earth-/Venus-analog 의 반사광 편광
  특징. 방법론.
- **2405.13247** Pasquini et al. 2024 — RV 행성 검출용 딥러닝. 방법론.

### Not read — no arXiv preprint available (96 papers)

대부분 2010년 이전 reference, 학회 abstract, 장비 paper 변형. 대부분이
mass/radius/age 교차 reference 로 이미 읽은 paper 가 제공하는 정보 외에
시각 정보를 추가하지 않음. 미독 핵심 예시.

- "Transit Search for Exoplanets around Alpha Centauri A and B with
  ASTERIA" (CubeSat — Knapp 2020 학위논문). Null-result 컨텍스트.
- 다수의 AB pre-Hipparcos paper (Demarque 1986 등) — 후속 자료로 대체.
- 이미 읽은 저널 paper 결과를 요약하는 다수의 proceedings (IAU 심포지엄,
  AAS abstract).

**사용자 액션 요청.** 후보 HZ 거대 행성 검출 관련 2025–2026 새 paper 가
나오면 (Beichman 2025 / 2508.03814 follow-up) 시스템 서사가 바뀌고 Phase 3
재작성이 정당화될 수 있습니다.

---

## Open items for follow-up

- Beichman 2025 후보 HZ 거대 행성을 확인/반박. 확인 시 NearStars 행성
  인벤토리에 추가하고 적절한 Phase 3 행성 synthesis 작성.
- AB 쌍에 대한 TESS 섹터 관측 (현재 다년간 측광 가능) 으로 활동 극대기
  흑점 점유 예측을 정밀화.
- Joyce & Chaboyer 2018 시스템 나이를 2024년 이후 진동학 재분석 (Gaia DR3
  SED + Tess oscillation modes) 과 교차 검증.
- 시각 디스크 색조 hex 는 순수 흑체가 아니라 5810-K 흑체에 태양-twin SED 를
  컨볼루션한 CIE 1931 색도로 렌더러를 사용하여 보정해야 합니다. Phase 4 작업.
- 대류 overshoot 0.10–0.15 H_p 값은 현재 모델 선호의 상한; 후속 MESA 재분석이
  더 낮은 값에 안착하면 입상 셀 크기 추정치가 ~10% 축소.
- 사이클 주기 불확실성 (DeWarf 2010 베이스라인 ~7 yr 이 부분 사이클만 다룸)
  으로 19-yr 값이 soft. ~2030 까지의 연속 모니터링이 이를 좁힐 것.
