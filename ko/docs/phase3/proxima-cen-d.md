<!-- Proxima Centauri d Phase 3 합성: cfg-ready 결정과 근거 -->
# Proxima Centauri d — Phase 3 Synthesis

Proxima Centauri d 는 Faria 외 2022 (`2022A&A...658A.115F`,
arXiv:2202.05188) 가 5.122 일 주기의 0.26 M⊕ 천체로 처음 보고하고, 그
뒤 Suárez Mascareño 외 2025 (`2025A&A...700A..11S`, arXiv:2507.21751)
의 NIRPS + ESPRESSO 결합 분석에서 높은 유의도로 확정된 sub-Earth-mass
ultra-short-period (USP) 행성 후보입니다. 0.029 AU 의 짧은 sma 로
어떤 거주가능영역 해석에서도 안쪽 끝 안에 들어가며, 궤도가 너무 빠듯해
Proxima 의 희미한 M5.5V 조명에도 일조량이 지구의 ~17 배에 달하고,
평형 온도는 326 K (A = 0.3) — Mercury 와 비슷하며 어떤 액체 물 임계점
보다도 한참 높습니다.

행성은 통과로 보이지 않습니다. Suárez Mascareño 2025 §4 가 확인한 높은
궤도 경사가 통과 지오메트리를 광도 모니터링 envelope 밖에 둡니다. 결과
적으로 최소 질량과 궤도 주기만 관측으로 제약되며, 거의 모든 다른 Decisions
행은 가장 잘 연구된 USP analog 인 Mercury 비교와 M 왜성 조사 + Proxima
flare 환경 제약을 결합해 추론합니다.

**NearStars 시나리오 선택. 노출된 basalt 표면, 부분 용융 magma pond 가
있는 substellar, vestigial sodium-vapor exosphere 를 가진 뜨거운 조석
고정 Mercury-like sub-Earth-mass 암석 행성으로, Proxima 의 flare 출력
에 대한 대기 차폐가 없습니다.** 32 cfg 픽. 17 은 canonical-aligned
(궤도 + 벌크 파라미터), 15 는 tie-break (표면 시각, 약한 대기 / exosphere
선택, 자기장 추론) 로 문헌이 특정 값에 침묵하는 영역입니다. documented
divergence 는 없습니다 — Proxima d 는 너무 최근에 발견되어 canonical
기후 모델이 아직 존재하지 않습니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 5.12 d USP → 조석 고정 < 10⁵ yr (Walterová 2020 스케일링) |
| `obliquity_deg` | 0 | high | 조석 damping |
| `eccentricity` | 0 | high | SM25 — fit 이 USP 의 원형과 일관 |
| `sidereal_period_days` | 5.122 ± 0.001 | high | Faria 2022. SM25 확정 |
| `semi_major_axis_au` | 0.029 | high | Kepler 3 법칙으로 유도 |
| `mass_mearth` | 0.26 | high | Faria 2022 Msini. SM25 가 살짝 정련 |
| `radius_rearth` | 0.65 | medium | Tie-break. 비통과. ~0.3 M⊕ 암석에 대한 mass-radius → 0.6–0.7 R⊕. interesting-first 가 지구와의 시각 구분을 위해 0.65 선택 |
| `surface_gravity_g_earth` | 0.62 | medium | 유도 = 0.26 / 0.65² |
| `density_g_cc` | 5.2 | medium | Tie-break. 지구형 암석 가정. Mercury 밀도 5.4 가 윈도우 내 대안 |
| `insolation_s_earth` | 17 | high | L = 0.00157 L☉, a = 0.029 AU 로 유도 |
| `equilibrium_temp_k` (A=0) | 357 | high | 유도 |
| `equilibrium_temp_k` (A=0.3) | 326 | high | 유도. 암석 bond albedo |
| `bond_albedo` | 0.15 | medium | Tie-break. 뜨거운 암석 범위 0.06–0.2. Mercury analog 0.12. interesting-first 가 어두운 basalt 와 더 밝은 regolith 사이에서 0.15 선택 |
| `surface_temp_substellar_k` | 800 | medium | Tie-break. airless 1100 K, 완전 대기 수송 700 K. 부분 수송 (Mercury-analog vestigial exosphere) 으로 중간 800 K |
| `surface_temp_nightside_k` | 80 | medium | Tie-break. airless cold trap (Mercury 야측 ~100 K). 약간의 열 inertia → ~80 K |
| `atmosphere_present` | false (vestigial Na vapor 만) | medium | Tie-break. 17 S⊕ + Proxima flare 환경에서 escape ratio 가 강하게 손실 favor. interesting-first 가 완전 airless 보다 Mercury-analog vestigial exosphere 선택 |
| `atmosphere_surface_pressure_pa` | 10⁻⁹ | medium | Tie-break. Mercury Na exosphere 컬럼 밀도 10¹⁰ /cm² ≈ 10⁻⁹ Pa 등가 (analogy 로 Killen 2007 Mercury exosphere 리뷰) |
| `atmosphere_composition` | 소듐 우세 vapor (sputter-produced) | low | Tie-break. Mercury analog. basalt 표면에 대한 Proxima 항성풍 sputtering |
| `atmosphere_tint_rgb_hex` | n/a (가시 대기 없음) | high | 유도 |
| `cloud_cover_fraction` | 0 | high | 대기 없음 |
| `ocean_present` | false | high | T > 600 K 가 표면 물 배제 |
| `surface_tint_rgb_hex_primary` | `#5a3a2a` (빨강 별 아래 iron-oxidized basalt regolith) | medium | Tie-break. Mercury 표면 색조 × M 왜성 SED. interesting-first 가 중립 회색보다 따뜻한 흙 톤 선택 |
| `surface_tint_rgb_hex_accent` | `#8a5a30` (substellar 부분 용융 magma 광채) | low | Tie-break. T_substellar > 800 K → terminator 면 경사면에 부분 silicate 용융 가시. 차가운 야측 대비 두드러지게 보이도록 시각 광채 선택 |
| `surface_morphology` | impact-cratered basalt 지형. substellar 부분 용융 pond. antistellar volatile cold-trap regolith | medium | Tie-break. Mercury analog + 17 S⊕ 일조량 driven 부분 용융 열 기울기 |
| `magnetic_field_present` | true (약한, 유도된) | medium | Tie-break. conducting 철핵 + Proxima 항성풍 → 유도된 자기장. 직접 측정되지 않았지만 Mercury 와의 analogy 로 가능 |
| `magnetic_dipole_moment_normalized_earth` | 0.001 | medium | Tie-break. Mercury-analog 매우 작은 핵 쌍극자. interesting-first 가 cfg 에서 aurora-equivalent flare-magnetosphere 상호작용을 유지하도록 작은 0 이 아닌 값 선택 |
| `radiation_belt_present` | false | high | 대기 없음 + 무시할 만한 B 필드 → 갇힌 입자 population 없음 |
| `surface_radiation_dose_msv_yr` | 10⁵ | high | Atri 2020 (1910.09871) 스케일링, 대기 차폐 없음 × 17× 일조량 |
| `atmospheric_shielding_g_cm2` | 0 | high | airless |
| `aurora_present` | false | high | 자극할 대기 없음 |
| `flare_dose_event_msv` | 10⁴ | high | Atri 2020 + Vida 2019 superflare 통합 양성자 도즈, d 거리 |
| `star_apparent_angular_diameter_deg` | 2.5 | high | 유도. 2 R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2980 | high | Proxima Teff |

## Surface synthesis

Proxima d 의 표면은 두 가지 경쟁하는 열 regime 에 의해 지배됩니다.
airless 초고온 dayside 와 깊이 차가운 nightside 가 sharp 한 terminator
기울기를 만듭니다. 17 배 지구 일조량과 albedo 0.15 에서 평형 온도 (326
K) 는 전역 평균값입니다. substellar 온도는 훨씬 높이 치솟습니다 (tie-break
명목 값 800 K, airless 극한이 1100 K 쪽으로 밀어붙임).

substellar 반구는 silicate melt 와 volatilization 이 지배합니다. 지속
적인 substellar T ≥ 800 K 에서 iron-rich basalt 가 부분 용융하여 깊이
유체 pocket 을 만들고, Io 의 silicate 화산활동을 연상시키는 표면 특징을
만듭니다 (조석 가열 엔진은 없음 — Proxima d 는 의미 있는 조석 가열이
없음). substellar magma pond 는 보수적인 "완전 고화 암석" 대안보다
tie-break 선택입니다. 부분 용융 지오메트리가 가상 우주선이 행성에
접근하면서 mid-day terminator 에 다가가는 모습에서 보이는 광채 액센트를
만듭니다 (`surface_tint_rgb_hex_accent = #8a5a30`).

antistellar 반구는 Mercury 의 영구 그늘진 극지방 크레이터의 volatile
cold-trap analog 입니다. 온도가 80 K 가까이 떨어지면 물 얼음, 메탄,
소듐 volatile 을 sequester 할 수 있는데, 이들은 드문 인터스텔라 / 혜성
전달로 들어옵니다. Ipatov 2023 의 먼지 / 얼음 planetesimal 전달 모델
(시스템 bibliography 통해 인용) 은 안쪽 Proxima 시스템에 지속적인 낮은
플럭스의 volatile 유입을 시사합니다. antistellar cold-trap 의 volatile
보유는 가능하지만 직접 측정 불가능합니다.

표면 morphology — 4 Gyr 의 폭격에서 온 충돌 크레이터, 더 오래된 지형 위에
overprint 된 substellar 부분 용융 변형 — 는 전부 Mercury analog 에서
추론됩니다. cfg `surface_morphology` 필드가 표준 Mercury 식 hummocky
basalt 텍스처로 이를 잡으며, M 왜성 조명 스펙트럼이 silicate 팔레트의
빨강-갈색 끝 쪽으로 편향시킵니다.

## Atmosphere synthesis

Proxima d 는 일반적인 의미에서 효과적으로 대기를 갖지 않습니다. 표면
중력 0.62 g_⊕ 와 substellar 온도 ~800 K 에서 어떤 그럴듯한 secondary
atmosphere 의 Jeans-escape 파라미터도 H₂ 에 대해 > 100, H₂O 에 대해
> 30, CO₂ 에 대해 > 5 입니다 — 모두 Gyr 시간 스케일에서 thermal escape
에 우호적입니다. 17 배 일조량은 XUV-driven hydrodynamic escape 도
강하게 구동합니다. Lee 2021 (2109.06963) 은 Proxima b 도 0.05 AU 에서
Venus-analog escape rate 를 경험한다고 발견했으며, d 의 훨씬 더 가까운
0.029 AU 에서는 손실 비율이 한 자리수 더 스케일됩니다.

남는 것은 vestigial sodium-vapor exosphere 입니다 — 완전 airless 모델에
대한 cfg tie-break 선택입니다. basalt 표면에 대한 Proxima 항성풍 sputtering
이 feldspar / pyroxene 격자에서 Na 원자를 지속적으로 해방시켜, 컬럼 밀도
~10¹⁰ atoms/cm² (Mercury analogy, Killen 2007) 의 얇고 중력적으로 자유로운
exosphere 를 만듭니다. 관련된 등가 압력 (10⁻⁹ Pa) 은 가시 Rayleigh 산란
이나 흡수 시그니처 한참 아래 있어서, cfg `atmosphere_tint_rgb_hex` 는
"n/a" 로 설정됩니다 — 가시 외관은 전적으로 표면 색조가 지배합니다.

Na exosphere 의 일시적 enhancement 는 Proxima superflare 동안 예상할 수
있습니다 (연 ~3 회 의 10³³ erg, Vida 2019). 증가한 XUV 와 입자 플럭스가
sputtering 산출을 극적으로 증가시키기 때문입니다. 이 사건들은 cfg 스칼라
색조 해상도에서 가시 플룸을 만들지 않지만, 향후 cfg 변형으로 Open items
에 표시됩니다.

## Rotation & spin synthesis

Proxima d 는 조석 고정 상태이며, substellar 점은 0° meridian 에 고정되고
sidereal 회전 주기가 5.122 일 궤도와 동일합니다. 0.12-M☉ M 왜성 주위
0.029 AU 의 0.26-M⊕ 암석 행성에 대한 조석 damping 시간 스케일은 < 10⁵
년입니다 (Walterová 2020 가 Proxima b 의 더 긴 주기 계산에서 스케일).
시스템 ~4.85 Gyr 나이 안에 충분합니다. 황도 경사도 비슷하게 0° 로
damping 됐습니다.

spin-orbit resonance 는 1:1 (동기) 로 가정합니다. Mercury 가 가진 3:2
resonance 보다는 동기 상태인데, 궤도 이심률이 실질적으로 0 (SM25 fit) 이고
더 높은 차수 resonance trap 을 구동하려면 적당한 e 가 필요하기 때문입니다
(Makarov 2012). cfg `tidally_locked: true` 와 `obliquity_deg: 0` 이 이
동기 상태를 잡습니다.

동기 상태 주변 libration 진폭은 작습니다 (< 1°). 무시할 만한 궤도 이심률로
제한되기 때문입니다. substellar 점이 행성 frame 에 고정되고, 일간 diurnal
cycle 이 완전히 사라지며, 이는 substellar 온도의 7 년 항성 활동 사이클
변조라는 훨씬 느린 modulation 으로 대체됩니다.

## Visual styling

Proxima d 는 이 합성의 5 entry 가운데 시각적으로 가장 muted 합니다. 깊은
빨강 M5.5V 조명 (`stellar_color_temp_k = 2980`) 과 iron-oxidized basalt
표면이 결합해 따뜻하고 채도가 높은 빨강-갈색 글로벌 색조 (`#5a3a2a`) 를
만들고, substellar 부분 용융 영역에 미묘하게 더 따뜻한 액센트 (`#8a5a30`)
가 들어갑니다. cratering 과 ridge 지오메트리는 Mercury-analog 템플릿을
따릅니다.

궤도에서 보면 행성이 클래식한 뜨거운-Mercury 위상 곡선을 보입니다. 대기
haze 없는 sharp 한 terminator, 광도 잡음 너머의 거의 0 인 limb darkening,
어두운 야측으로 빠르게 fading 하는 완전 조명된 dayside. Proxima 가 d 의
하늘에서 각지름 2.5° 를 채우며 — 지구에서 본 태양 겉보기 지름의 5 배 —
그 깊은 빨강 빛이 시각 장면을 지배합니다.

Proxima superflare 동안 행성의 dayside 는 증가한 UV / 광학 플럭스가
표면에 산란되면서 짧은 brightening 을 겪습니다. cfg 가 이를 가시 면에
대한 일시적 색조 modifier 로 인코딩합니다. 표면의 어떤 객체에 대해서도
누적 flare 도즈가 lethal level 에 도달하며 (≥ 10³³-erg superflare 당
10⁴ mSv, Atri 2020 스케일링), 게임 내 거주 가능성은 불가능합니다. 행성은
플레이어 탐사를 위한 순수한 뜨거운 암석 시각 destination 입니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Faria J. P. et al. 2022** — *A candidate short-period sub-Earth
  orbiting Proxima Centauri*, A&A 658, A115
  (`2022A&A...658A.115F`, arXiv:2202.05188). 발견 논문. P = 5.122 d,
  Msini = 0.26 M⊕ 보고. 궤도 이심률은 fit 의 정밀도에서 원형과 일관.
- **Suárez Mascareño A. et al. 2025** — *Diving into the planetary
  system of Proxima with NIRPS: Breaking the m/s barrier*, A&A 700,
  A11 (arXiv:2507.21751). Proxima d 를 높은 유의도로 확정. 궤도 fit
  정련. 광도 모니터링 envelope 에서 통과를 배제하는 높은 값으로 경사
  제약.
- **Suárez Mascareño A. et al. 2020** — *Revisiting Proxima with
  ESPRESSO* (arXiv:2005.12114). 5 d 의 0.3-M⊕ 행성과 일관된 발견
  이전 상한.
- **Anglada-Escudé G. et al. 2016** — *A terrestrial planet candidate
  in a temperate orbit around Proxima Centauri*, Nature 536, 437
  (arXiv:1609.03449). 호스트 별 컨텍스트 — Proxima b 발견이 d 의 최종
  식별을 제약한 같은 데이터 baseline 을 사용했습니다.
- **Boyajian T. S. et al. 2012** — *Stellar Diameters and Temperatures
  II*, ApJ 757, 112 (arXiv:1208.2431). Proxima R = 0.1542 R☉. 일조량
  계산의 기준.
- **Atri D. et al. 2020** — *Stellar Proton Event-induced surface
  radiation dose as a constraint on the habitability of terrestrial
  exoplanets* (arXiv:1910.09871). 방사선 도즈 Decisions 행에 사용.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets*, ApJ 900, 24 (arXiv:2007.12459).
  조석 고정 시간 스케일 스케일링.
- **Vida K. et al. 2019** — *Flaring Activity of Proxima Centauri
  from TESS Observations* (arXiv:1907.12580). 도즈 스케일링을 위한
  superflare 빈도 + 에너지 분포.

### Read (context / methodology, not decision-driving)

- **Lee Y. et al. 2021** — *Exosphere Modeling of Proxima b*
  (arXiv:2109.06963). d 의 escape rate 에 대한 자릿수 스케일링.
- **Kossakowski D. et al. 2023** — *The CARMENES search for
  exoplanets around M dwarfs: Wolf 1069 b* (arXiv:2301.02477).
  자매 시스템 analog. USP 암석 행성 시나리오 교차 확인에 유용.

### Read (instrument / non-cfg-decisive)

- (없음. d 의 deep_read set 은 작음.)

### Not read — no arXiv preprint or low-priority (~10 papers)

- 대부분 확장된 bibliography 의 Wolf 1069 b 와 TOI-2095 자매 시스템
  논문들이며, `docs/phase3/_bib/proxima-cen-d.yaml` 에 `status: skipped`
  주석으로 보존됩니다.

## Open items for follow-up

- **직접 반지름 측정.** SM25 가 현재 모니터링 envelope 에서 통과 미검출을
  확정. 향후 직접 촬영이나 고정밀 astrometric 캠페인이 진짜 질량 +
  반지름을 산출할 수 있습니다 (현재는 Msini 만 제약). cfg `radius_rearth
  = 0.65` 는 placeholder tie-break.
- **질량-반지름 관계로 구성.** Msini 만 있어서 구성 (암석 vs. 얼음 풍부)
  은 제약되지 않습니다. cfg 는 지구형 암석 밀도 (5.2 g/cc) 로 디폴트.
  확정된 더 작은 반지름은 더 높은 밀도 (Mercury 형 iron 풍부) 쪽으로
  미는 것을 시사합니다.
- **Volatile cold-trap 시그니처.** antistellar cold-trap 은 혜성 플럭스로
  전달된 물 얼음과 다른 volatile 을 보유할 수 있습니다. 향후 cfg 변형이
  antistellar 극에 작은 `subsurface_ice` 패치를 추가할 수 있습니다.
- **항성풍 sputtering 산출.** cfg 는 tie-break 으로 Mercury-analog Na
  exosphere 를 채택하지만, Proxima d 의 항성풍 환경에 맞춘 직접 모델링은
  없습니다. d 에 맞춘 향후 Garraffo 식 3D MHD 항성풍 시뮬레이션이
  exosphere 컬럼 밀도와 종 구성을 정련할 수 있습니다.
- **Superflare albedo modulation.** cfg 는 현재 시간 평균 Bond albedo
  만 인코딩합니다. ~3 superflare/년 cadence (Vida 2019) 가 XUV-bright
  단계 동안 일시적인 albedo enhancement 를 만듭니다.
