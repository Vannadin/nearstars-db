<!-- AU Mic e Phase 3 합성. cfg-ready 결정과 근거 -->
# AU Mic e — Phase 3 Synthesis

AU Microscopii e 는 22 Myr 의 M1Ve flare star AU Mic 주위를 도는
시선속도 후보 행성으로 논란 상태이며, Donati et al. 2025 (A&A 700,
A227. `2025A&A...700A.227D`. doi:10.1051/0004-6361/202555371) 가
다년간의 SPIRou + ESPRESSO RV 캠페인에서 보고했습니다. 보고된 궤도
주기는 33.11 ± 0.06 d, 최소 질량은 21.1 ± 5.4 M⊕ 입니다. 행성은
통과하지 않으며 다른 독립 관측 제약 (TTV, 직접 촬영, 천체측정) 은
존재하지 않습니다. 이 후보는 NASA Exoplanet Archive 에서
`pl_controv_flag = 1` 을 달고 있는데, RV 신호가 자리잡은 주기 영역
에서 AU Mic 의 항성 활동 자전 고조파 (4.86 d 자전 주기의 배수) 가
계통적 power 를 그럴듯하게 기여할 수 있기 때문입니다. 33.11 d 주기는
4.86 d 의 깔끔한 고조파가 아니지만 (자전의 ≈ 6.81 배), Donati 2025
가 행성 해석을 주장하는 근거이기도 하고, 그래도 super-saturated 활동
host 별 위에서는 RV 전용 후보가 본질적으로 확인이 어렵습니다.

e 의 모든 cfg 파라미터가 미확인 검출에 의존하기 때문에, 이 합성은
**시종일관 cfg-conservative** 입니다 — 모든 confidence 값은 `low`
이고, cfg-ready 섹션은 독립적인 확인을 명시적으로 조건으로 합니다.
e 가 미래 분석에서 철회되면 AU Mic 시스템은 NearStars cfg 에서
b/c/d 만으로 배포되어야 하고, 이 Phase 3 합성은 cfg 작성기로
승격되기보다는 아카이브에 들어가야 합니다.

**NearStars 시나리오 선택. AU Mic 주위 ~0.16 AU 의 33.1 d 궤도에
있는 ~21 M⊕ 따뜻한 sub-Neptune 후보로, AU Mic c (시스템에서 유일하게
잘 특성화된 sub-Neptune) 의 유사로 모델링합니다. 조석으로 묶인 따뜻한
sub-Neptune, 암석/철 내부 위에 얇은 H/He envelope. cfg 배포는 독립적인
확인을 조건으로 합니다 — 통과 탐색이 성공하거나, 확장된 모니터링
에서 TTV 신호가 검출되거나, 다른 기기에서의 RV 회수가 나타나기 전까지
cfg 작성기는 AU Mic e 를 기본 멤버가 아니라 선택적인 네 번째 행성
variant 로 다루어야 합니다.** 27 개 cfg 픽. 모두 low confidence. documented
divergence 없음 (여기서의 모든 선택은 제약 없는 윈도우 안의 tie-break
이거나, AU Mic c 의 더 잘 제약된 파라미터에서 직접 상속).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true (행성이 실재할 조건부) | low | 33.1 d 궤도. 0.51 M☉ 주위 0.16 AU 의 sub-Neptune 급 행성에서 조석 감쇠 ≪ 22 Myr. AU Mic c 와 동일한 논증 |
| `obliquity_deg` | 0 | low | 조석 감쇠 가정. 확인을 조건 |
| `eccentricity` | null | low | Donati 2025 가 e 를 발표하지 않음 (low-S/N RV 전용 fit). cfg 는 기본값으로 원형 채택 |
| `argument_of_periastron_deg` | null | low | 발표 없음. null 유지 |
| `sidereal_period_days` | 33.11 ± 0.06 | low | Donati 2025 ESPRESSO + SPIRou RV. 활동 유도로 신호가 논란 |
| `semi_major_axis_au` | 0.161 | low | 유도. a³ = M☉ · P²(yr) 가 M = 0.51 M☉, P = 33.11 d 에서 0.161 AU. Donati 2025 는 a 를 직접 발표하지 않음 |
| `inclination_deg` | null (b/c/d 와 coplanar 라면 ~89.5° 가정) | low | 통과 없음. e 가 실재하고 시스템의 가장자리 정면 구조와 coplanar 라면 (b/c/d 모두 i ≈ 88–89°, 잔해 원반 i = 89.5°) e 도 거의 edge-on 이어야 하지만 이는 추론 |
| `mass_mearth` | 21.1 ± 5.4 (최소 질량. coplanar 라면 sin i = 1) | low | Donati 2025. 인용된 질량은 coplanar 시스템 가정 하의 M (M sin i 아님). e 가 misaligned 라면 실제 질량은 더 큼 |
| `radius_rearth` | 2.9 | low | Tie-break. 통과 없음. 21 M⊕ 의 sub-Neptune 에 대한 Chen & Kipping 2017 질량-반지름 관계로 추정 (≈ 2.6–3.2 R⊕ 윈도우). cfg 는 AU Mic c 의 2.79 R⊕ 와 시각적 짝을 이루도록 2.9 채택 |
| `surface_gravity_g_earth` | 2.5 | low | 유도 = 21.1 / 2.9² (placeholder 반지름 가정). 반지름 가정에 강하게 의존 |
| `density_g_cc` | 4.7 | low | 유도. AU Mic c 의 3.7 g/cc 보다 살짝 큼 — 더 먼 거리에서의 더 작은 envelope 질량 분율과 일관 |
| `insolation_s_earth` | 3.6 | low | L = 0.092 L☉ 과 a = 0.161 AU 에서 유도 |
| `equilibrium_temp_k` (A=0) | 381 | low | 유도. 거리가 더 멀어 b/c/d 보다 상당히 차가움 |
| `equilibrium_temp_k` (A=0.1) | 371 | low | 유도. 적당한 sub-Neptune 알베도 |
| `bond_albedo` | 0.10 | low | sub-Neptune 유사 낮은 알베도. 측정 없음 |
| `dayside_surface_temp_k` | 410 | low | 얇은 envelope 이 AU Mic c 의 주야 재분배 패턴을 상속. 주간 측면이 T_eq 보다 살짝 높음 |
| `nightside_surface_temp_k` | 320 | low | 적당한 재분배. 야간 측면이 T_eq 보다 조금 낮음 |
| `atmosphere_present` | true (얇은 H/He envelope 가정) | low | 0.16 AU 의 21 M⊕ 질량은 M-왜성 XUV 하에서 작은 H/He envelope 이 22 Myr 동안 살아남을 수 있는 영역 (Owen & Wu 2017). 직접 검출 없음 |
| `atmosphere_surface_pressure_pa` | 1.0e6 | low | 얇은 H/He envelope 의 구름 데크 압력. AU Mic c 와 동일 analog |
| `atmosphere_composition` | H₂ ~80%, He ~15%, H₂O ~2%, CH₄ + NH₃ + CO 미량. 가능한 광화학 haze | low | AU Mic c sub-Neptune analog 에서 상속. 직접 측정 없음 |
| `atmosphere_scale_height_km` | 50 | low | 유도. kT/μg 에서 T = 380 K, μ = 2.5, g = 24.5 m/s² |
| `atmosphere_tint_rgb_hex` | `#8a6a4c` | low | Tie-break. AU Mic c 와 같은 계열 — M-왜성 SED 하의 sub-Neptune 광화학 haze. c 보다 차갑지만 (380 K vs 450 K) cfg 는 AU Mic sub-Neptune 짝 간의 시각적 일관성을 위해 같은 hex 유지 |
| `cloud_cover_fraction` | 0.60 | low | sub-Neptune analog. 온도가 낮고 광화학 haze 생성이 줄어 c 보다 살짝 작음 |
| `cloud_morphology` | 적도 superrotation 을 동반한 띠상 zonal 구름 구조. 자전 주기가 더 느리고 온도가 더 낮아 c 의 띠보다 약함. 저위도에서 가능한 H₂O/NH₃ 얼음 구름 응결 | low | Showman 2009 을 더 차가운 sub-Neptune 으로 스케일. 따뜻한 sub-Neptune 에 대한 canonical 해석. 관측 없이는 구체 형태 불확실 |
| `cloud_tint_rgb_hex` | `#a08868` | low | Tie-break. 온도가 낮아 고고도 구름 밝기가 줄어 c 의 `#b0987a` 보다 살짝 어두움. c 와 시각적 차별화를 위해 선택 |
| `surface_morphology` | n/a — 구름 데크 반지름에서 보이는 단단한 표면 없음. 내부는 물 풍부 mantle + 암석/철 코어 (혹은 envelope 가 없다면 암석 천체) 가능성 | low | density placeholder. 반지름 가정을 조건 |
| `magnetic_field_present` | true | low | H 풍부 envelope 의 sub-Neptune 은 적당한 dynamo 유지. Yadav & Thorngren 2017 스케일링 — 다만 느린 33-d 자전이 dynamo 를 약화 |
| `magnetic_field_strength_microtesla_equator` | 30 | low | Tie-break. 1:1 lock 의 느린 자전 때문에 c (50 μT) 보다 약함. 측정 없음 |
| `atmospheric_escape_rate_g_s` | 1e7 | low | AU Mic 에서 더 멀어 c 보다 작음. 0.16 AU 의 AU Mic XUV 에 대한 에너지 한정 추정 |
| `aurora_present` | true | low | H 풍부 상층 대기 + AU Mic 항성풍 → H Balmer-α 예상. 다만 거리가 더 멀고 대기 질량이 작아 b/c 보다 약함 |
| `aurora_color_primary_hex` | `#ff6e8c` | low | Tie-break. H-α 656.3 nm 지배. b/c 와 같은 색 계열이지만 더 옅음 |
| `star_apparent_angular_diameter_deg` | 2.7 | low | 유도. 2 × 0.82 R☉ / 0.161 AU × (180/π) ≈ 2.7° (R 은 Phase 2 anchor Donati 2023 ZDI) |
| `stellar_illumination_color_temp_k` | 3518 | high | host 별 광도 색-등가 흑체 (Gaia DR3 BP/RP). Phase 2 분광 Teff = 3700 ± 100 K (Plavchan 2020) 와 의도적으로 구분되며, SED 조명은 분광 값을 사용 — au-mic.md `stellar_color_temp_k` 참조 (e 의 확인 여부에 의존하지 않는 유일한 파라미터) |

## Surface synthesis

AU Mic e 의 "표면" 은 이 Phase 3 합성에서 가장 사변적인 요소입니다.
어떤 관측도 bulk 속성을 제약하지 않기 때문입니다. Donati 2025 의
RV 신호는 coplanar 시스템 가정 하에서 (잔해 원반과 b/c/d 가 모두
일관되게 거의 edge-on 이라 cfg 가 채택) 최소 질량 21.1 ± 5.4 M⊕ 를
주지만, 통과 관측이 없고 반지름도 측정되지 않았습니다. cfg 의
placeholder 반지름 2.9 R⊕ 는 21 M⊕ 에 적용한 Chen & Kipping 2017
확률적 질량-반지름 관계에서 옵니다. 이는 e 를 sub-Neptune 영역에
놓는데, AU Mic c (2.79 R⊕, 14.46 M⊕) 와 대체로 평행하지만 질량과
밀도가 더 높습니다.

NearStars 의 목적에서 e 는 따라서 c 의 sub-Neptune analog 로
모델링되며, 질량은 키우고 거리는 더 늘어난 형태입니다. e 가
확인되고 cfg 에 실린다면 플레이어가 보는 "가시 표면" 은 ~10⁶ Pa
의 얇은 H/He 구름 데크 꼭대기로, 띠상 가스 천체로 렌더링됩니다.
그 아래 암석/철 코어가 존재하는지, 혹은 e 가 사실은 envelope 가
거의 없는 물 풍부 mantle 인지는 미해결입니다. cfg 는 c 와의
평행 구성으로 얇은-envelope 해석을 헤드라인으로 채택합니다.

**반지름이 그렇게 불확실한 이유.** 21 M⊕ 의 질량-반지름 다이어그램
은 적어도 세 가지 서로 다른 조성 가족을 허용합니다. 상당한 물
mantle 을 가진 super-Earth 는 반지름 ~2.3 R⊕, 밀도 ~9 g/cc 일 수
있습니다 — 지구보다 밀도가 높고, sub-Neptune 골짜기에서 가장 밀도가
높은 멤버입니다. 암석 코어 위에 ~3% H/He envelope 를 가진
sub-Neptune 은 Chen & Kipping 2017 placeholder 의 ~2.9 R⊕, 밀도
~4.7 g/cc 와 맞습니다 — cfg 의 헤드라인 해석. ~10% H/He 의 더
부푼 sub-Neptune 은 ~3.5 R⊕, 밀도 ~2.7 g/cc 까지 갈 수 있어 작은
Neptune 과 비슷합니다. 통과 없이는 cfg 가 이들을 구분할 수 없고,
placeholder 값은 중간 추측입니다.

**e 가 envelope 가 없는 암석이라면.** AU Mic 주위 0.16 AU 의 21 M⊕
super-Earth 는 22 Myr 동안 심한 XUV 구동 대기 침식을 겪지만 두꺼운
envelope 를 스트립하기에는 부족합니다 (Owen & Wu 2017 광증발
골짜기가 envelope 스트립 임계점을 e 가 겪는 것보다 더 높은
일사량에 둠). envelope 없는 암석 variant 는 따라서 그럴듯하지만
광증발 프레임워크에서 강하게 선호되지는 않습니다. Open items 에
cfg variant 로 등재.

**조석 lock 하의 표면 형태.** e 가 sub-Neptune 이 아니라 암석
variant 라면, 조석 lock 하 380 K 주간, 320 K 야간의 표면 형태는
AU Mic d 의 양상 (substellar lava province + 야간 frost cap) 과
지구의 양상 (온건한 주야 대비) 사이의 중간 영역을 만들 것입니다.
cfg 는 e 에 대해 구체 표면 피처를 약속하지 않습니다. 암석 variant
시나리오 자체가 부차적이기 때문입니다.

## Atmosphere synthesis

e 의 대기는 구성상 현재 관측에서 검출 불가능합니다. 후보는 통과도
없고 직접 촬영도 없습니다. 유일한 제약은 RV 유도 질량이며, 이는
대기 조성이나 압력에 대해 직접적으로는 아무것도 말해주지 않습니다.

**압력.** cfg 는 AU Mic c 의 얇은 H/He envelope 해석에 대한 analog
로 ~10⁶ Pa 구름 데크 압력을 채택합니다. 이는 중간 추정값입니다.
실제 값은 10⁵ Pa (매우 얇은 envelope, 거의 airless 한 암석 variant)
에서 10⁷ Pa (더 두꺼운 H/He envelope, mini-Neptune variant) 까지
그럴듯하게 펼쳐질 수 있습니다. cfg 는 중간 범위의 c-analog 를
기본값으로 택합니다.

**조성.** AU Mic c (H₂ ~80%, He ~15%, 미량 H₂O/CH₄/NH₃/CO 와 광화학
haze) 와의 평행 구성으로 cfg 는 e 에도 같은 조성을 채택합니다. 이는
무원칙하지만 내부적으로 일관됩니다. flare 포화된 M1V 주위 0.16 AU
의 21 M⊕ 에서의 실제 조성은 현재 데이터에서 측정 불가능합니다.

**하늘 외관.** 가정된 얇은 H/He envelope 아래에서 (구름 데크로
내려가는) e 의 주간 하늘은 AU Mic 의 각지름 2.7° 가 비추는 더
깊은 크림 색조의 띠 표면으로 보일 것입니다. 표면 일사량은 지구의
3.6 배 — 상당하지만 b (18.8×) 나 c (6.5×) 보다는 낮습니다. 시각적
표현은 c 의 작고 차가운 사촌일 것입니다.

**대기 탈출.** AU Mic 의 포화 영역 하 0.16 AU 의 XUV 구동 탈출률은
c 의 0.119 AU 보다 대략 한 자릿수 작아, 에너지 한정 가정 하에서
~10⁷ g/s 입니다. envelope 가 존재한다면 시스템의 22 Myr 나이에
걸쳐 대부분 보존되기에 충분히 작습니다.

## Rotation & spin synthesis

0.51 M☉ 주위 0.161 AU 의 33.1-d sub-Neptune 에 대한 조석 감쇠는
~10⁷ 년 시간 척도로 진행됩니다 (Goldreich & Soter 1966, Neptune-like
Q ≈ 10⁴), 22-Myr 시스템 나이와 비슷하거나 약간 작은 정도입니다.
e 가 1:1 spin-orbit 으로 완전히 잠겨 있는지는 행성의 조석 Q 와
이심률 (측정되지 않음) 에 민감하게 의존합니다. cfg 는 sub-Neptune
analog 해석과 일관된 기본 시나리오로 1:1 lock 을 채택합니다.

**KSP 구현 노트 (확인 조건부).** 자전 주기 = 궤도 주기 = 33.11 일
(2 860 704 초). Kopernicus `rotationPeriod` 는 궤도 `period` 와
일치해야 합니다. cfg 가 e 를 선택적 네 번째 행성으로 배포한다면 이
자전 주기가 적용됩니다. e 가 생략된다면 cfg 작성기는 배포되지 않은
천체에 대한 자전 cfg 를 합성해서는 안 됩니다.

**계절 없음.** Obliquity 는 0 으로 감쇠 (lock 가정 하). 이심률은
측정되지 않음 — 원형 가정을 채택합니다.

**주야 재분배.** 얇은 H/He envelope 로 e 의 대기는 주간에서 야간
으로 적당히 잘 열을 운반하지만 b 의 더 두꺼운 envelope 보다는
못합니다. 예상 주야 대비. ~90 K (주간 410 K, 야간 320 K). e 의
낮은 일사량이 열 forcing 을 줄여 대비가 b/c 보다 작습니다.

**느린 자전 효과.** 33 일 자전 주기에서 Coriolis 효과는 b/c 보다
한 자릿수 약합니다. 대기 순환은 zonal jet 보다는 직접적인 주야
열 forcing 에 지배됩니다 (Sergeev 2020 substellar 대류 프레임워크).
띠상 구조는 c 보다 덜 발달할 수 있습니다.

## Visual styling

AU Mic e 의 시각적 표현은 (확인 조건부) AU Mic c 의 작고 차갑고
띠가 더 약한 사촌입니다.

- **전반 외관.** 옅은 zonal 띠를 가진 따뜻한 sub-Neptune 디스크.
  AU Mic 의 각지름 2.7° (지구에서 본 태양의 5 배 — 여전히 지배적
  이지만 안쪽 세 행성 대비 줄어듦) 가 비춥니다. 디스크는 muted
  red-brown 띠 (`#8a6a4c` 주 haze, `#a08868` zone 구름) 를 보입니다
  — 낮은 온도가 고고도 구름 밝기를 줄여 c 보다 살짝 더 차가운 색조.
- **띠 구조.** 적도 superrotation jet 이 옅은 적도 zone 과 더
  어두운 중위도 belt 를 만들지만, 자전 주기가 더 느리고 온도가
  낮아 c 보다 덜 두드러집니다. 띠는 넓은 zone 이 아니라 가는
  줄로 보입니다. Tie-break. 다른 AU Mic sub-Neptune 들과의 시각적
  연속성을 위해 균일 haze 가 아닌 띠를 선택.
- **구름 꼭대기 텍스처.** c 보다도 덜 격렬함 — e 의 작은 스케일
  높이 + 훨씬 느린 자전이 eddy 와 Rossby wave 를 최소화합니다.
  구름 꼭대기는 미묘한 섭동을 가진 비교적 매끈한 띠 표면으로
  읽힙니다.
- **두드러진 탈출 꼬리 없음.** b 와 달리 e 의 대기 탈출은 ~10⁷ g/s
  로 추정 — 실용적인 관측 기하에서는 보이지 않습니다. cfg 는 e 에
  확장된 halo 나 탈출 꼬리를 렌더링하지 않습니다.
- **하늘의 별.** AU Mic 이 e 의 하늘에서 2.7° 를 차지 (지구에서
  본 태양의 5 배) — 주간 하늘을 지배하는 적당한 크기의 붉은 디스크.
  substellar 구름 꼭대기에서의 표면 일사량은 지구의 3.6 배.
  Super-flare 는 10–60 분간 조명을 1–3 등급 밝게 만듭니다 — 거리가
  가장 멀어 네 행성 중 가장 덜 극적이지만, AU Mic 의 본질적 flare
  광도 때문에 여전히 상당합니다.
- **자매 행성.** b (가장 안쪽, puffy Neptune) 가 conjunction 에서
  지름 ~0.2° 의 작은 점으로 보임. c (그 다음 안쪽, sub-Neptune)
  비슷. d (가장 안쪽 암석) 는 ~0.05° 로 옅음. 35–210 AU 의 가장자리
  정면 잔해 원반은 AU Mic 양옆으로 가늘고 밝은 줄로 보이며, e 에서
  봤을 때 안쪽 가장자리는 별에서 ~3° 떨어져 있음.

35 AU 의 원반 안쪽 가장자리는 e 에서 본 각도 (~2.6°) 가 안쪽
행성들에서 본 것보다 좁지만, 시각적 차이는 미묘합니다 — 원반의
밝기와 기하는 AU Mic 어느 시점에서도 외관을 지배합니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Donati J.-F. et al. 2025** — *AU Mic system characterized with ESPRESSO*, A&A 700, A227 (`2025A&A...700A.227D`, doi:10.1051/0004-6361/202555371). AU Mic e 후보의 발견 논문. SPIRou + ESPRESSO RV 의 33.11-d 주기에서 최소 질량 21.1 ± 5.4 M⊕. **현재 유일한 검출이자 cornerstone.** AU Mic 의 super-saturated 활동이 RV 전용 검출을 확인하기 어렵게 만들어 NEA 에서 신호가 `pl_controv_flag = 1` 로 표시됨.
- **Mallorquin M. et al. 2024** — *AU Mic system characterized with ESPRESSO*, A&A 689, A132 (`2024A&A...689A.132M`). b/c 파라미터를 정밀화했지만 e 는 검출하지 못한 ESPRESSO + TESS 결합 분석 — AU Mic 에서 활동 모델링 민감도에 대한 맥락을 설정. Mallorquin 2024 의 미검출이 논란의 원천 중 하나. Donati 2025 의 더 후속 SPIRou 데이터 확장 분석이 Mallorquin 2024 의 파이프라인이 포착하지 못한 신호를 회수함.
- **Mallorquin M. et al. 2024b (비확인)** — *Revisiting the dynamical masses of the transiting planets in the young AU Mic system*, A&A 수락 (arXiv:2407.16461). 명시적 비확인. "33.4 일 궤도 주기를 가진 행성 후보 AU Mic 'e' 의 최근 제안된 존재를 확인하지 못함". 이전 Donati 2023 주기를 사용해 광학 RV 에서 K_e < 10 m/s 의 3σ 상한 설정. Donati 2025 의 응답. 수정된 더 낮은 진폭 (5.9 m/s, 4.9σ) 이 Mallorquin 의 광학 민감도 floor 아래에 있어 SPIRou 근적외선에서 주로 검출 가능 — 파장 의존 SNR 이지 반박이 아님.
- **Wittrock J. M. et al. 2023** — *Transit Timing Variation Measurements and Dynamical Mass Determination of the AU Mic System*, AJ 166, 232 (`2023AJ....166..232W`, arXiv:2310.10719). 안쪽 행성에 대한 TTV 동역학 질량. d 도입. Wittrock 의 N-body fit 은 33 d 의 추가 perturber 를 요구하지 않으며 (d-c TTV 잔차는 동역학 모델만으로 e 없이 설명 가능), 이는 e 논란 체인의 일부.
- **Owen J. E. & Wu Y. 2017** — *The Evaporation Valley in the Kepler Planets*, ApJ 847, 29 (`2017ApJ...847...29O`, arXiv:1705.10810). 광증발 프레임워크. 3.6 S⊕ + AU Mic XUV 의 e 는 22 Myr 에서 envelope 보전 임계점보다 훨씬 위에 있어, envelope 없는 암석 variant 보다 얇은-H/He-envelope cfg 픽을 뒷받침.
- **Chen J. & Kipping D. 2017** — *Probabilistic Forecasting of the Masses and Radii of Other Worlds*, ApJ 834, 17 (`2017ApJ...834...17C`, arXiv:1603.08614). RV 유도 질량에서 placeholder 반지름 2.9 R⊕ 를 추정하는 데 사용한 질량-반지름 관계.

### Read (context / methodology, not decision-driving)

- **Plavchan P. et al. 2020** — *A planet within the debris disk around the pre-main-sequence star AU Microscopii*, Nature 582, 497 (`2020Natur.582..497P`, arXiv:2006.13428). TESS 의 b 발견. e 논란과 관련된 시스템의 항성 활동 맥락 정의.
- **Martioli E. et al. 2021** — *AU Mic c: a second planet transiting the young M dwarf AU Mic*, A&A 649, A177 (`2021A&A...649A.177M`, arXiv:2102.05288). c 의 발견. e 의 cfg 파라미터 대부분이 상속되는 sub-Neptune analog.
- **Tristan I. I. et al. 2023** — *Catching the Flares of the AU Mic System with TESS*, ApJ 951, 33 (`2023ApJ...951...33T`, arXiv:2306.00077). TESS flare 센서스. 10³¹ erg 위 5.6/일 비율. e RV 신호에 대한 활동 오염 우려를 구동.
- **Klein B. et al. 2021** — *Investigating the young AU Mic system with SPIRou: stellar magnetic field and close-in planet mass*, MNRAS 502, 188 (`2021MNRAS.502..188K`, arXiv:2012.04970). AU Mic 의 SPIRou 근적외선 ZDI + RV. Donati 2025 의 SPIRou + ESPRESSO 결합 분석에 투입된 방법론.
- **Boldog Z. et al. 2025** — *Transit-timing variations in the AU Mic system observed with CHEOPS*, A&A 694, A137 (`2025A&A...694A.137B`, arXiv:2501.13575). CHEOPS TTV 가 b/c 궤도 정밀화 + d 가 내부 섭동자. 33 d 주기의 e 는 직접 다루지 않음 — Boldog 의 TTV fit 은 33 d 외부 섭동자를 요구하지 않음. e 를 확인하지도 반박하지도 않음. e 주기에서 시그너처가 없는 가장 최근 TTV 연구.
- **Donati J.-F. et al. 2023** — *The magnetic field topology and filling of the very active M dwarf AU Mic*, MNRAS 525, 2015 (`2023MNRAS.525.2015D`). host 별 ZDI. 가까운 모든 후보에 대한 항성 자기장 맥락 제공.
- **Goldreich P. & Soter S. 1966** — *Q in the Solar System*, Icarus 5, 375 (`1966Icar....5..375G`). 조건부 1:1 spin-orbit 결론에 사용한 조석 감쇠 시간 척도 프레임워크.
- **Sergeev D. E. et al. 2020** — *Atmospheric Convection Plays a Key Role in the Climate of Tidally Locked Terrestrial Exoplanets: Insights from High-Resolution Simulations*, ApJ 894, 84 (`2020ApJ...894...84S`, arXiv:2004.03007). 주야 재분배 논의에 적용된 substellar 대류 프레임워크.

### Read (instrument / non-decisive)

- **Cale B. L. et al. 2021** — *Diving Beneath the Sea of Stellar Activity: Chromatic Radial Velocities of AU Mic b*, AJ 162, 295 (`2021AJ....162..295C`, arXiv:2109.13996). Donati 2025 e 검출에 (간접적으로) 적용된 GP-detrending 방법론. e-결정적이지 않음.

### Not read — no arXiv preprint or low-priority (~15 papers)

AU Mic e 관련 문헌은 후보가 매우 최근 (Donati 2025) 이고 독립적인
후속 관측의 대상이 아직 되지 않았기 때문에 희소합니다. 진행 중인
여러 논문 (확장 SPIRou 모니터링, 가능한 TESS extended-mission 검출
시도, JWST 대기 특성화 제안) 이 있지만 현재로서는 cfg-결정적인 내용을
제공하지 않아 깊이 읽지 않았습니다. 전체 필터링된 bib 는 행성의
`_bib/au-mic-e.yaml` (생성 예정) 에 `status: skipped` annotation 으로
보존됩니다.

## Open items for follow-up

- **독립 확인 (최우선).** cfg 의 AU Mic e 포함은 독립 확인을 조건
  으로 합니다. 다른 기기에서의 RV 검출 (예. 확장된 HARPS-N 이나
  MAROON-X 모니터링), 확장된 b/c 통과 모니터링 (TESS, PLATO) 의 TTV
  신호, 혹은 성공적인 통과 탐색이 각각 e 를 후보에서 확인으로 승격
  시킬 수 있습니다. 대신 e 가 철회되면 (활동 오염 설명이 행성 설명을
  이기면) cfg 는 AU Mic 을 b/c/d 만으로 배포해야 하고, e Phase 3 는
  cfg 작성기로 승격되지 않고 `docs/phase3/_archived/au-mic-e.md` 에
  아카이브되어야 합니다.
- **통과 탐색.** e 의 경사각이 호의적이라면 (시스템 나머지와
  coplanar 라면 거의 edge-on 일 가능성 큼), 확장된 TESS sector 나
  미래 PLATO 관측에서 통과가 검출될 수 있습니다. 통과 검출은 반지름
  불확실도 (현재 Chen & Kipping placeholder 에서 ±~10%) 와 밀도
  불확실도를 low 에서 high confidence 로 collapse 시키고, 행성의
  존재도 독립적으로 확인할 것입니다.
- **대기 검출.** 확인 조건부로 e 의 어떤 JWST 투과 스펙트럼이라도
  가정된 얇은-H/He 조성을 제약할 것입니다. 높은 SNR 의 비검출은
  envelope 없는 암석 variant 를 선호하고, H₂O, CH₄, CO 검출은
  cfg 의 sub-Neptune-analog 해석을 뒷받침할 것입니다.
- **cfg variant. e 생략.** e 가 철회되면 cfg 는 AU Mic 을 b/c/d 만
  으로 배포합니다. 이것이 기본 보수 variant 입니다 — 확인된 행성만
  배포, e Phase 3 는 archive 에 보존, 독립 확인이 나타나면 재방문.
  이 variant 는 확인이 도착할 때까지의 **보수적 기본값** 입니다.
- **cfg variant. e 가 sub-Neptune 으로 확인.** e 가 확인되고 통과가
  검출되면 cfg 는 여기서 합성하는 그대로 — 0.16 AU, 33-d 주기, 21 M⊕
  의 c-analog sub-Neptune, 얇은 H/He envelope, 띠상 zonal 구름 구조
  로 배포합니다.
- **cfg variant. e 가 암석 super-Earth 로 확인.** e 가 확인되었지만
  통과가 검출되지 않고 질량-반지름 추론이 암석 조성 (밀도 > 6 g/cc)
  을 가리키면 sub-Neptune 이 아니라 AU Mic d 의 무거운 super-Earth
  analog 로 배포합니다. 표면 형태는 d 의 조석 lock 암석 패턴 쪽으로
  이동 (낮은 일사량으로 약화된 substellar lava province, 야간 cold
  trap, 얇거나 부재한 대기). 시각 스타일은 헤드라인 해석과 의미 있게
  달라질 것입니다.
- **cfg variant. 더 높은 질량의 e.** 확장 RV 모니터링이 실제 질량이
  더 높음을 발견하면 (예. 시스템이 완전히 coplanar 가 아니어서 RV 가
  M sin i 만 주는 경우) e 는 Neptune 질량 (~30–40 M⊕) 에 접근할 수
  있습니다. 이는 cfg 를 b-analog puffy Neptune 해석 쪽으로 밀어붙일
  것입니다. 더 높은 품질 데이터 대기 중의 가능한 variant 로 등재.

## Related

- [au-mic](au-mic.md) — disk 기하를 포함한 host 별 합성
- [au-mic-b](au-mic-b.md) — 자매 행성. 8.5 d 의 puffy hot Neptune
- [au-mic-c](au-mic-c.md) — 자매 행성. 18.9 d 의 sub-Neptune (e 의 파라미터를 상속하는 데 사용한 가장 가까운 analog)
- [au-mic-d](au-mic-d.md) — 자매 행성. 12.7 d 의 지구질량 TTV 후보
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — downstream cfg 작성기
