<!-- Alpha Centauri B Phase 3 synthesis: cfg-ready 시각 결정과 근거 -->
# Alpha Centauri B — Phase 3 Synthesis

NearStars KSP mod 의 Phase 3 항성 synthesis (2026-05-22 작성).

Alpha Centauri B 는 Alpha Centauri AB 쌍성계의 K1 V 부성으로, A 에
23.5 AU 장반경 P = 79.91 yr 의 궤도로 묶여 있음. 질량
0.9373 ± 0.0033 M☉, 반지름 0.8632 ± 0.0037 R☉, 광도 0.503 ± 0.007 L☉
(A 의 1/3). 금속함량 높음 ([Fe/H] = +0.25 ± 0.04, Porto de Mello 2008),
A 보다 약간 더 활동적 (log R'_HK = -4.85; 41일 자전주기), 측광 모니터링
(DeWarf 2010) 과 X-ray 플럭스 변조 (Robrade & Schmitt 2005, 2012) 로 ~7년
활동 사이클 추론됨.

NearStars 에서의 목표는 K1 V 별이되 시각적으로 A 나 Sol 보다 분명히 더
따뜻하고 노랗지만 후기 K 진짜 dwarf 처럼 "주황색"으로는 보이지 않게 — G-
class 와 K-class 분광 외관 사이 다리에 해당. Dumusque 2012 의 phantom
행성 (Alpha Cen Bb) 과 2015년 Rajpaul 의 철회라는 역사적 컨텍스트가 이
별 주위 RV 신호 해석을 형성 — cfg 는 B 주위에 행성 없음으로 채택.

**NearStars 시나리오 선택. super-solar 금속함량과 7년 활동 사이클을 가진
K1 V warm-yellow dwarf** — A 보다 약간 강한 limb darkening, 사이클 극대기
검출 가능한 적당한 흑점 점유, 태양형 자기 다이나모 기하.

## Decisions

Kopernicus 별 cfg-ready 값.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `mass_msun` | 0.9373 | high | Pourbaix & Boffin 2016 binary_orbit |
| `radius_rsun` | 0.8632 | high | Kervella et al. 2017 VLTI/PIONIER |
| `teff_k` | 5316 | high | Porto de Mello et al. 2008 고분해 분광 |
| `luminosity_lsun` | 0.503 | high | Kervella et al. 2017 볼로미터 플럭스 |
| `spectype` | K1 V | high | Keenan & McNeil 1989 |
| `metallicity_fe_h_dex` | +0.25 | high | Porto de Mello et al. 2008 |
| `age_gyr` | 4.81 ± 0.5 | medium | Joyce & Chaboyer 2018 — A 와 동일 (coeval) |
| `rotation_period_days` | 41 | high | DeWarf et al. 2010 |
| `obliquity_deg` | 0 | low | 채택 — 측정 없음 |
| `surface_color_temp_k` | 5290 | high | limb-darkened 평균 쪽 가중 |
| `surface_tint_rgb_hex` | `#ffe9c4` | medium | 흑체 5290 K → CIE 색도, warm-yellow (태양과 진짜 K dwarf 주황 사이) |
| `corona_tint_rgb_hex` | `#ffd9a0` | low | 디스크보다 살짝 더 따뜻; 채층 라인비에서 관측 |
| `limb_darkening_coeff_quadratic_a` | 0.35 | medium | Claret 2017 K-dwarf 축소; 태양보다 적당히 강함 |
| `limb_darkening_coeff_quadratic_b` | 0.30 | medium | 동일 |
| `granulation_cell_size_arcsec` | 1.0e-3 | medium | Bigot et al. 2008 / Teff 낮아서 G/K dwarf 보다 작은 셀 |
| `convective_overshoot_pct` | 14 | medium | A 보다 깊은 대류 envelope |
| `magnetic_cycle_period_yr` | 7 | medium | Robrade & Schmitt 2005/2012, Ayres 2014 X-ray 사이클 |
| `spot_coverage_max_pct` | 5 | medium | DeWarf 2010 — V 에서 peak-to-peak 측광 진폭 ~3% |
| `spot_temperature_offset_k` | -1700 | medium | 전형적 K-dwarf umbra ~3600 K → 평균 광구보다 -1700 K |
| `xray_log_lx_erg_s` | 27.3 | high | Robrade & Schmitt 2005, XMM-Newton |
| `xray_cycle_factor` | 4.5 | medium | Robrade & Schmitt 2012 — 2003–2010 모니터링의 명확한 사이클 |
| `flare_rate_per_day_amplitude_log10` | -2 | medium | Ayres 2014 — 적당한 superflare rate; A 보다 ~10× 높음 |
| `wind_mass_loss_rate_msun_yr` | 2e-14 | medium | Wood et al. 2005 (AB 합산 측정) |
| `wind_terminal_velocity_km_s` | 650 | medium | 낮은 escape velocity 로 A 보다 느림 |
| `chromosphere_ca_ii_log_rhk` | -4.85 | high | DeWarf et al. 2010 |
| `helioseismic_p_mode_max_freq_mhz` | 4.1 | high | Carrier & Bourban 2003 — 높은 log g 로 A 보다 높은 p-mode envelope |
| `apparent_diameter_arcsec_from_sol` | 0.0060 | high | derived. 2 × 0.8632 R☉ / 1.347 pc × 206265 |
| `apparent_magnitude_v_from_sol` | 1.33 | high | Hipparcos/SIMBAD |
| `companion_a_max_separation_arcsec` | 12 | high | A 기하의 거울 |
| `companion_a_min_separation_arcsec` | 1.7 | high | A 기하의 거울 |
| `proxima_separation_au_from_b` | 8700 | medium | Kervella, Thévenin & Lovis 2017 — 묶인 외곽 궤도 |
| `interstellar_extinction_av_mag` | 0.0 | high | LIC, 무시 가능 reddening |

## Stellar disk synthesis

Alpha Cen B 는 K-class 특성이 시각적으로 명확한 첫 근거리 별. 5316 K
(Porto de Mello 2008) 는 A 보다 ~500 K 차갑고 태양보다 ~460 K 차가움.
디스크 적분 색도는 인지된 색을 warm-yellow 영역으로 확고히 이동 — CIE-D55
→ 흑체 매핑 후 RGB ≈ `#ffe9c4`. A 의 `#fff6e0` 와 비교하면 B 는 분명히
더 따뜻한 톤이고, 나란히 비교하면 "K dwarf" 로 인지됨.

**색 선택.** 흑체 피크 ~545 nm (vs A 의 496 nm, 태양의 502 nm). B-V 색
(~0.90, Hipparcos) 은 다른 K1 V 비교별과 유사 (61 Cyg A. K5 V at B-V =
1.06; 70 Oph A. K0 V at B-V = 0.86). KSP 색조는 A 와 시각적으로 다르되
61 Cyg A 만큼 주황이지 않게.

**시직경.** Kervella 2017 의 PIONIER 측정으로 지구 기준 5.999 ± 0.025 mas
— A 의 8.502 mas 보다 약 30% 작음. B 주위 L=0.503 플럭스 등가 거리
(0.71 AU) 의 가상 지구 analog 에서 디스크는 ~0.71° 시직경, 지구에서 보는
태양의 0.53° 보다 크고 solid angle 기준 ~33% 더 큼 (closer orbit 에서
낮은 광도를 보상).

**Limb darkening.** K-dwarf limb darkening 은 태양보다 강함. 가장자리 밝기는
디스크 중심의 ~30% (태양 ~40%). Quadratic (a,b) = (0.35, 0.30) 채택. 더
차가운 상부 광구의 TiO band onset 으로 가장자리가 약간 더 적색 (A 나
태양과 달리 B 의 스펙트럼에서 이미 검출 가능).

**입상.** Bigot et al. 2008 은 B 가 A 보다 작은 입상 셀을 가짐을 도출 —
낮은 질량 깊은 대류 기대와 일관. 셀은 지구 거리에서 ~1.0e-3 arcsec (A 의
1.3e-3 보다 약간 더 미세). 시각 깜빡임 노이즈는 다소 큰 진폭 (~0.15
magnitude/cell vs 태양의 0.10) 이지만 유사한 ~10분 시간 척도.

**P-mode 진동.** Carrier & Bourban 2003 이 envelope peak ~4.1 mHz (주기 ~4
분), 진폭 ~9 cm/s RV 의 p-mode 검출. A 나 태양보다 높은 주파수 (높은 표면
중력 log g = 4.54 vs A 의 4.32 와 일관). p-mode 시각 영향은 분 단위
sub-percent 깜빡임; A 와 동일한 KSP 처리.

**ASTERIA-class 통과 없음.** Knapp 2020 ASTERIA CubeSat 통과 탐색과
지상 RV 탐색 (Dumusque 2012, Rajpaul 2015 철회) 은 가까운 (P < 50 d 에서
Earth-mass) 행성에 엄격한 한계 부여. Phase 3 cfg 는 현 관측 상태와 일관되게
B 행성 미포함.

## Activity and variability synthesis

Alpha Cen B 는 AB 쌍의 더 자기적으로 활동적인 멤버. 여러 독립 모니터링
캠페인이 확인.

- **자전주기. 41 ± 3 일** (DeWarf et al. 2010 측광 변광에서; 분광
  v sin i = 1.0 ± 0.5 km/s 와 i = 56° 기울기 가정으로 일관). A 보다 낮은
  질량으로 인해 더 느림 — Brun & Browning 2017 다이나모 이론은 K-dwarf
  자전이 ~5 Gyr 나이에 보통 30–60 d 라 예측.
- **자기 사이클 주기. ~7 년**. Robrade & Schmitt 2005 가 XMM-Newton X-ray
  플럭스에서 첫 검출; DeWarf 2010 측광에서 확인. 주목할 점은 자전이 더 느림에도
  태양의 11년 Schwabe 사이클보다 *짧다*는 것 — 자기 다이나모 구조가 태양
  Babcock-Leighton 그림과 다름을 시사.
- **log R'_HK = -4.85** (DeWarf et al. 2010 사이클 평균). 자전 속도 대비
  적당히 활동적. Bcoll (longitudinal field strength) ≈ 사이클 극대기 동안
  5–15 G (Boro Saikia et al. 2018 ZDI).
- **X-ray 광도. log L_X ≈ 27.3 erg/s** (Robrade & Schmitt 2005). 평온
  상태에서 A 보다 factor ~2 높음. X-ray 사이클 진폭은 factor 4.5 — 적당하나
  2003–2012 모니터링에서 잘 측정.

**흑점 점유와 가시성.** DeWarf 2010 은 사이클 극대기에 peak-to-peak V 측광
진폭 ~3% 를 도출, ~5% 디스크 면적 흑점 점유 의미. 흑점 온도 ~3600 K (umbra),
~4800 K (penumbra). 시각. 극대기에 ±15–40° 중위도에 3–5개 어두운 흑점
그룹 분포, 각각 ~8° 시직경. 강한 limb darkening + 흑점 contrast 가 결합되어
극대기 고분해 이미징 시 B 는 눈에 띄게 "주근깨가 있는" 모습.

**Flare rate.** Ayres 2014 가 FUV/UV 모니터링에서 적당한 flare rate 도출 —
log-진폭 분포가 A 보다 평평하며 M-class 등가 flare 의 rate 는 ~10× 높음.
다년간 baseline 에서 superflare 확인 없음. K1 V 노년 별은 대개 더 젊거나
완전 대류인 M dwarf 와 비교해서 적당한 flare emitter.

**Corona 가열.** Robrade & Schmitt 2005 는 T_corona ~ 2-3 MK at 사이클
극대, ~1-1.5 MK at 극소 — 태양과 같은 범위지만 약간 이동. 뜨거운 loop 는
자기 네트워크 경계 근처에 집중, 태양 coronal hole 기하와 유사하나 더 조밀.

**자기 기하.** Boro Saikia et al. 2018 의 Zeeman Doppler 이미징은 사이클
극소기에 dipole-dominant 자기 기하, 극대기에 multipole-dominant 로 전이 —
태양형 행동이나 7년 사이클로 응축. dipole 기울기는 자전축 기준 ~30°.

## System geometry synthesis

B 프레임에서의 AB 쌍성 상호 가시성은 A 의 거울 이미지.

- B 는 A 를 23.5 AU 장반경 e = 0.5179 로 공전.
- B 표면에서 A 는 apastron 에서 V ≈ -22 (그러나 0.022° 시직경의 점광원에
  가까움) ~ periastron 에서 V ≈ -24 (0.066° 시직경) 의 찬란한 변광 별.
- B 의 HZ 등가 궤도 (B 주위 ~0.71 AU) 에서 A 의 플럭스는 쌍성 궤도 주기에
  걸쳐 factor (35.7/11.4)² = 9.8× 변하여 계절형 기후 forcing 제공.

**B 주위 가상 지구 analog** (0.71 AU, 고전 HZ) 의 경우. 하늘의 태양은
Alpha B 가 시직경 ~0.71° (지구 태양보다 33% 큰 시직경) 이지만 0.71 AU 에서
L=0.503 매칭으로 1× 광도. 색도는 채택된 warm-yellow K1 V.

이 궤도에서 A 플럭스는 다음 사이에서 변동.
- Apastron. A 는 B-지구에서 36.0 - 0.71 ≈ 35.3 AU → 플럭스는 1.52 /
  35.3² ≈ 0.0012 L_eff (B 자체 1.0 대비). Magnitude ~-19.5 (~2× 보름달
  밝기).
- Periastron. A 는 B-지구에서 11.4 - 0.71 ≈ 10.7 AU → 플럭스 0.013 L_eff.
  Magnitude ~-22 (~30× 보름달 밝기, 가시 그림자 생성).

B-지구 주변의 낮-밤이 극적이 됨. periastron 단계 동안 A 가 밤하늘에 있을 때
~30× 보름달의 야간 조명 제공 — 인공 조명 없이 표면 활동 가능한 밝기.

**Proxima 가시성.** B 표면에서 Proxima 는 동일한 시각 등급 ~+5, A 에서 ~2°.

**B 주위 확인 행성 없음.** Dumusque et al. 2012 가 P = 3.236 d, K = 0.51 m/s
의 Alpha Cen Bb 를 보고했으나 Rajpaul et al. 2015 가 반박 (Gaussian-process
활동 모델이 그 신호가 sampling artifact 임을 보여줌). Rajpaul 철회는 고정밀
RV M-dwarf 행성 검출이 명시적 활동 모델링을 요구하는 대표 사례. 2026 기준
B 주위 확인 행성 없음.

## Visual styling

- **전체 모습.** warm-yellow K1 V 디스크, A 나 Sol 보다 분명히 더
  차갑고/노랑. 관찰자는 "amber" 또는 "warm cream" 으로 묘사 — 아직
  주황이지 않지만 순수 백색 태양 외관을 넘어선 모습.
- **궤도체에 대한 dayside 조명.** 색온도 ~5290 K — 지구 analog 의 대기 산란이
  태양 조명보다 약간 더 따뜻한 하늘 톤 (하늘은 순수 `#87ceeb` 대신 `#a0c0e0`
  정도), 일몰/일출이 적-주황 과장.
- **디스크 밝기 프로파일.** A 보다 강한 limb darkening; 가장자리가 중심
  대비 ~30% 밝기, 약간 적색 편이.
- **흑점 가시성.** 사이클 극대기에 가시 반구 전반에 3–5개 흑점 그룹 분포,
  각각 ~5–8° 시직경, 광구보다 ~1700 K 차가움. KSP 등가. 7년 사이클로
  대형/소형 절차적 어두운 패치, 렌더링된 디스크에 주근깨로 가시.
- **동반성 A.** B 의 어느 궤도에서나 늘 하늘에 존재. apastron 에서 A 는
  찬란한 ~0.02° 디스크, periastron 에서 ~0.07° 디스크 미세 분해 (A 가
  높은 Teff 로 B 의 1.42× 표면 밝기). 79.91-yr 궤도에 걸쳐 장관의 변광
  야간 조명 제공.
- **Proxima Cen.** A 에서 ~2° 의 ~+5 등급 점광원. 시각적으로 평범.
- **분광선.** A 와 동일한 우세선이되 적색 파장에서 추가 TiO 밴드 발달.
  H-α 흡수는 더 깊음 (차가운 광구), Ca II H/K core 는 사이클 극대기 동안
  더 강한 emission reversal 표시.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2017A&A...597A.137K** Kervella et al. 2017 — VLTI/PIONIER 간섭계
  반지름 (5.999 ± 0.025 mas; R = 0.8632 ± 0.0037 R☉) 와 볼로미터 광도
  (0.503 ± 0.007 L☉).
- **2008A&A...488..653P** Porto de Mello et al. 2008 — 차등 고분해
  분광 Teff (5316 ± 28 K), [Fe/H] (+0.25 ± 0.04). A 와 짝 측정.
- **2010ApJ...722..343D** DeWarf et al. 2010 — 7년 측광 + Ca II H&K
  모니터링. 자전주기 41 ± 3 d, 부분 활동 사이클, log R'_HK = -4.85.
- **2016A&A...586A..90P** Pourbaix & Boffin 2016 — 역학 질량 0.9373
  ± 0.0033 M☉.
- **2006A&A...446..635B** Bigot et al. 2006 — VLTI/VINCI 의 Alpha B
  간섭계, 입상 노이즈 제약. R = 0.863 ± 0.005 R☉ (Kervella 2017 의
  precursor).
- **2018ApJ...864...99J** Joyce & Chaboyer 2018 — 시스템 나이 4.81 ±
  0.50 Gyr; A 와 coeval. MESA + 진동학으로 독립 질량 M_B = 0.934 ±
  0.0061 M☉.
- **2003A&A...404.1087K** Kervella et al. 2003 — VLTI/VINCI 초기
  간섭계. 후속 Kervella 2017 와 일관된 precursor 측정.
- **1009.1652 (2010ApJ...717.1279A)** Ayres 2010 — B 의 X-ray, FUV,
  UV 다파장 모니터링, 활동 사이클 phase 진화 포함. cfg 의 사이클
  진폭 factor 4.5 제공.
- **1202.1265** Carrier & Bourban 2003 — HARPS 진동학 p-mode 검출.
  log g = 4.54 ± 0.02 확인; p-mode envelope 4.1 mHz.
- **1401.2211** Heller & Armstrong 2014 — K-dwarf 세계의
  "Superhabitability". B 의 HZ 행성을 그저 거주 가능 너머의 흥미로움으로
  만드는 무엇인지 컨텍스트.

### Read (context / methodology, not decision-driving)

- **0811.0673** Quintana 2002 — B 의 HZ 에서 행성 형성. AB perturbation
  에도 HZ 행성이 역학적으로 가능함을 보여줌.
- **1009.1652** Robrade & Schmitt 2012 — 2010 까지의 X-ray 모니터링
  계속, Robrade & Schmitt 2005 의 사이클 검출 확장.
- **1506.07304** Rajpaul et al. 2015 — RV 시계열용 Gaussian-process
  활동 모델. Dumusque 2012 의 Alpha Cen Bb 주장을 철회한 방법론 paper.
  B 주위 행성 null result 의 중요 컨텍스트.
- **1902.10711** Coffinet et al. 2019 — Alpha B 관측의 HARPS 활동과
  telluric contamination. Dumusque/Rajpaul 논쟁과 관련.
- **1805.00929** Morel 2018 — AB 의 화학 조성 재검토. [Fe/H] = +0.24
  의 독립 확인과 상세 개별 원소 abundance. Porto de Mello 2008 교차 검증.
- **1711.06320** Zhao et al. 2018 — 다양한 장비에서의 AB 주위 행성
  검출 가능성. 현재 RV/통과 한계 컨텍스트.
- **2211.11756** Foster et al. 2022 — 광학 SETI 탐색.

### Read (instrument-only, not visual-informative)

- **2405.13247** Pasquini et al. 2024 — RV 검출용 딥러닝. 방법론.
- "Going to Alpha Centauri B and setting up a Radio Bridge" — 사변적
  성간 통신 paper. 과학 아님.

### Not read — no arXiv preprint available (78 papers)

대부분 2010년 이전 reference 와 학회 요약. 미독 핵심 예시.

- "Fe II fluorescence in main-sequence K-dwarfs" — 아마 Ayres
  2008년 이전 paper. Skip.
- 다수 AAS abstract 및 IAU 심포지엄 proceedings 가 이미 읽은 paper 결과
  요약.
- ASTERIA CubeSat 학위논문 (Knapp 2020) — null 통과 탐색, 컨텍스트로만
  인용; 시각 정보 없음.

**사용자 액션 요청.** Alpha B 에 대한 새로운 ZDI 자기 이미징 캠페인이
온라인되면 (예. 예상되는 SPIRou 또는 NIRPS 결과 2026+), 흑점 점유와 dipole
기울기 숫자 수정이 필요할 수 있습니다.

---

## Open items for follow-up

- 7년 활동 사이클 타이밍은 Robrade & Schmitt 2012 가 phase 로 제약하나
  주기 불확실성 ~1.5 yr. 추가 사이클을 2030 까지 추적해야 주기가 더
  좁아짐.
- 흑점 온도 offset (-1700 K vs 광구) 은 K-dwarf 일반값, B 에 직접 측정
  안됨. TESS 나 CHEOPS 다색 측광이 제약 가능.
- Boro Saikia 2018 ZDI 의 dipole 기울기 (~30°) 는 단일 에포크; 사이클
  분해 자기 매핑 진행 중 (NIRPS/SPIRou).
- 확인 행성 없음, 그러나 RV 상한 (P < 50 d 에서 M sin i < 4 M⊕,
  Rajpaul 2015) 이 작은 동반자 여지 남김. ESPRESSO 장기 baseline 이
  검출하면 Phase 3 cfg 수정.
- Knapp 2020 ASTERIA null 통과 결과는 P < 28 d 에서 Earth-radius 행성을
  높은 신뢰도로 배제; 어떤 행성 인벤토리 결정도 이에 좌우되지 않음.
- 역사적 Bb 철회는 사용자 대상 문서가 B 의 행성 인벤토리를 단지 공란
  대신 명시적 "확인된 행성 없음" 으로 표시하도록 형성.
