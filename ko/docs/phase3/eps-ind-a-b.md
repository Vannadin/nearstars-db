<!-- eps Ind A b Phase 3 합성. cfg-ready 결정과 근거 -->
# ε Indi A b — Phase 3 Synthesis

ε Indi A b 는 **태양에 가장 가까운 직접 촬영 차가운 거대 외계행성** 입니다 —
조용한 K5 V 왜성 ε Indi A (11.9 ly) 를 a = 20.9 (+5.8/−3.3) AU 에서
공전하는 ~7.6 M_Jup 슈퍼목성으로, 이심률 e = 0.244 (+0.11/−0.083),
궤도 주기 P ≈ 108 (+49/−25) yr 입니다 (Matthews et al. 2026, JWST/MIRI
영상 + Hipparcos–Gaia 측성 + 30 년치 RV). JWST/MIRI 가 10.6 과 15.5 µm
에서 먼저 촬영했고 (Matthews 2024), 두 번째 epoch 에서 11.3 µm 로 재검출
(Matthews 2026), 공통 고유운동으로 확인했습니다. 이 행성은 차갑고 태양-나이
(~3.5 Gyr) 인 거대 행성으로 대기 온도가 ~275 K 부근입니다 — 그리고 결정적으로,
그 온도는 별빛이 아니라 스스로의 내부열로 설정됩니다. 20.9 AU 에서 0.239 L☉
별 주위의 일사량은 S ≈ 5.5 × 10⁻⁴ S⊕ 에 불과해, 복사-평형 온도는 겨우
~43 K 입니다. 따라서 ε Indi A b 는 스스로 빛나며 수축하는 슈퍼목성으로,
주변보다 ~230 K 더 뜨겁게 복사합니다.

대기가 헤드라인입니다. Matthews 2026 은 F1065C–F1140C 색 0.88 ± 0.08 mag
를 측정했는데 — 10–11 µm 암모니아 밴드를 가로지르는 11σ 밝기 차이로 —
**암모니아 (NH₃) 를 확인**하며, ε Indi A b 를 지금까지 암모니아가 검출된
가장 차가운 행성으로 만듭니다. 이 특징은 cloud-free solar-metallicity 모델
예측보다 얕은데, 저자들의 **선호 설명은 암모니아 특징과 근적외선 (3–5 µm)
방출 둘 다를 억제하는 두꺼운 물-얼음 구름** 입니다 (지상 아카이브 비검출과
일관). best-fit cloudy 모델은 275 K, log g ≈ 4.5, ~3× solar 금속도, ~2.5×
solar C/O 대기에 매우 광학적으로 두꺼운 H₂O 구름 (column optical depth ~416,
0.7 bar 부근에서 τ = 1 도달) 을 가집니다.

**NearStars 시나리오 선택. 넓은 ~20.9 AU 이심 궤도의 차가운 (~275 K,
내부 가열) 슈퍼목성으로, 따뜻한 Jovian 호박색이 아니라 무채색에 가까운
창백한 메탄/암모니아-부류 거대 행성으로 — 밴드를 억제하는 두꺼운 물-얼음
구름, 확인된 암모니아, 그리고 선택적 예술적 토성형 얼음 고리 (표기. 미관측)
와 함께 — 렌더링합니다.** 궤도와 암모니아 + 물-얼음-구름 대기는 측정됐으므로
(Matthews 2026), 핵심 Decisions 행들은 canonical-aligned 입니다. 정확한
색조, 밴드 형태, 자전, 경사, 그리고 고리는 차가운-거대-행성 interesting-first
독법으로 기본값을 잡은 within-window tie-break 입니다. 관측된 고리는 없습니다.
cfg 기본값은 `ring_present = false` 이고, 얼음 고리는 Open items 에 cfg
변종으로 보존됩니다.

## Decisions

Kopernicus / 대기 cfg-ready 값. `Confidence`. high = 직접 측정되거나
강하게 제약됨, medium = 강한 지지를 가진 이론, low = 허용 윈도 안의 미적
선택.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 0.78 M☉ 별 주위 20.9 AU 궤도 — 조석-감쇠 시간척도가 시스템 나이보다 ≫. spin–orbit 결합 불가 |
| `obliquity_deg` | 27 | low | Tie-break. 측정 없음. 시각적으로 뚜렷한 축 기울기를 위해 목성의 3.1° 대신 토성형 26.7° 채택. 선택적 얼음 고리 축과도 일관. 넓은 궤도 거대 행성의 역학 윈도 안 |
| `eccentricity` | 0.244 (+0.11/−0.083) | high | Matthews et al. 2026 — orvara 결합 피팅 (영상 + Hipparcos–Gaia 가속도 + RV). Feng 2025 보다 ~1.9σ 낮음. a 와 상관 (불완전 위상 커버리지) |
| `argument_of_periapsis_deg` | 62 (+48/−27) | high | Matthews et al. 2026 (DB curated, recommended) |
| `inclination_deg` | 102.3 (+1.9/−1.7) | high | Matthews et al. 2026 — 두 JWST epoch 이 경사 정밀도를 두 배로 |
| `longitude_of_ascending_node_deg` | 44.6 ± 1.3 | high | Matthews et al. 2026 |
| `sidereal_period_yr` | ~108 (+49/−25) | high | Matthews et al. 2026 유도 (DB period_days 39447). a ≈ 19 AU 의 거의-원형 해도 허용. Feng 2019 의 ~45 yr 를 대체 |
| `semi_major_axis_au` | 20.9 (+5.8/−3.3) | high | Matthews et al. 2026 (Phase 2 recommended). Feng 2019 (11.6 AU) 와 Feng 2018 (12.8 AU) 을 대체. ~108 yr 궤도에 ~30 yr RV 라 a–e 축퇴 |
| `mass_mjup` | 7.6 ± 0.7 | high | Matthews et al. 2026 — orvara 역학 (참) 질량, 7.63 (+0.73/−0.70) M_Jup. Feng 2019 (~3.25 M_Jup 측성) 과 Feng 2018 (M sin i ~2.7 M_Jup) 을 대체 |
| `mass_mearth` | 2425 ± 232 | high | DB curated (= 7.63 M_Jup × 317.8). Matthews et al. 2026 |
| `radius_rjup` | 1.12 | medium | DB 반지름 12.6 R⊕ = 1.12 R_Jup. ~7.6 M_Jup, ~3.5 Gyr 거대 행성에 전형적 (질량 큰 차가운 거대 행성은 ~1 R_Jup 부근. 예. Matthews 2026 best-fit log g 4.5 가 ~1.1 R_Jup 함의). transit 측정 아님 |
| `surface_gravity_g_earth` | ~15 | medium | DB M (7.63 M_Jup) 과 R (12.6 R⊕) 에서 유도. g = GM/R² ≈ 1.5 × 10³ cm/s² ≈ 15 g⊕ (log g ≈ 4.18 cgs). Matthews best-fit log g 4.5 는 더 작은-반지름 모델용 |
| `density_g_cc` | ~5.3 | medium | 유도. 1.12 R_Jup 구 안의 7.63 M_Jup ≈ 5.3 g/cc — 질량 크고 압축된 성숙한 거대 행성 (목성 1.33 g/cc 대비). 근-목성 반지름에서의 큰 질량을 반영 |
| `insolation_s_earth` | 0.00055 | high | 유도. S = L_star / a² = 0.239 L☉ (Feng 2019) / (20.9 AU)² ≈ 5.5 × 10⁻⁴ S⊕ — 무시할 만함. 행성은 일사 가열 아님 |
| `equilibrium_temp_k_a0` | ~43 | high | 유도. T_eq = 278.3 × (L/a²)^0.25 = 278.3 × 0.239^0.25 / √20.9 ≈ 43 K (A = 0). A = 0.3 에서 ~39 K. 근일점 (15.8 AU) ~49 K, 원일점 (26 AU) ~38 K |
| `effective_temp_k` | ~275 | high | Matthews et al. 2024, 2026 — JWST 측광 + cloudy 대기 피팅 (~250–300 K). 행성의 실제 복사 온도로, 내부열 (~3.5 Gyr 에 수축 중인 7.6 M_Jup 거대 행성) 이 지배. ~43 K 평형 온도보다 ~230 K 위 |
| `bond_albedo` | 0.35 | low | Tie-break. ~275 K 에서 두꺼운 물-얼음 + 암모니아 구름이면 토성 (0.34) 에 가까운 높은 구름 알베도가 적절. 직접 측정 없는 윈도 안의 미적 선택 |
| `atmosphere_present` | true | high | 거대 행성. 측정된 NH₃ 와 추론된 H₂O-얼음 구름을 가진 H₂/He 본체 (Matthews 2026) |
| `atmosphere_reference_pressure_pa` | 100000 | medium | 거대 행성은 고체 표면 없음. 구름-데크 렌더링용 1 bar cfg 기준. 물-얼음 구름 τ = 1 은 0.7 bar 부근 (Matthews 2026 best-fit) |
| `atmosphere_composition` | H₂/He 본체. **확인된 NH₃** (cloud-free 모델보다 얕음). 두꺼운 H₂O-얼음 구름. best-fit cloudy 모델에서 elevated 금속도 (~3× solar) 와 C/O (~2.5× solar) | high (NH₃, 구름) / medium (혼합비) | Matthews et al. 2026 — F1065C–F1140C = 0.88 mag (11σ) 에서 NH₃. 얕은 특징 + 3–5 µm 흐림의 선호 설명이 H₂O-얼음 구름. [M/H] 와 C/O 는 PICASO/Virga best fit 에서 |
| `atmosphere_scale_height_km` | ~25 | medium | 유도. H = kT/(μ m_H g), T = 275 K, μ = 2.3, g ≈ 15 m/s²-등가 (≈ 150 m/s²) → ~25 km |
| `atmosphere_tint_rgb_hex` | `#b8bcb0` (무채색에 가까운 창백한 회녹색 limb, 차가운 메탄/암모니아 부류) | low | Tie-break. 차가운 (~275 K) 물-얼음 + 암모니아 구름은 창백하고 탈채도된 색을 줌 — 따뜻한 Jovian 호박색이 아님. WISE 0855 유사체 (Matthews 2026. 거의 동일한 mid-IR 색) 를 모델로. K5 V 조명이 약한 따뜻한 편향 추가 |
| `cloud_cover_fraction` | 0.95 | medium | Matthews et al. 2026 — 두껍고 광학적으로 매우 깊은 (τ ~416) 물-얼음 구름. 거의 완전한 커버리지가 억제된 암모니아 특징 + 3–5 µm 흐림에 가장 잘 맞음 (WISE 0855 의 patchy 구멍 가능성과 달리 균일 커버) |
| `cloud_morphology` | 확인된-암모니아 대기 위에 두껍고 거의-전지구적인 물-얼음 구름 데크 (0.7 bar 부근 τ = 1). 기껏해야 약한 zonal 밴딩. NH₃ 특징과 근적외 방출을 억제 | medium | Matthews et al. 2026 — PICASO/Virga best fit. 275 K, log g 4.5, 3× solar [M/H], 2.5× solar C/O, f_sed 6, H₂O column optical depth ~416 |
| `cloud_tint_rgb_hex` | `#dfe2dc` (창백한 얼음빛 off-white — K5 V 빛 아래 H₂O-얼음 + NH₃) | low | Tie-break. 물-얼음 + 암모니아 구름은 본질적으로 약한 cold-blue 기를 띤 근-백색. 따뜻한 K5 V (4700 K) 조명이 지각 색조를 중성 창백한 off-white 로 이동시켜, 목성의 cream-amber 와 구별 |
| `planet_disk_tint_rgb_hex_primary` | `#dfe2dc` (창백한 off-white 데크 — 지배적 외형) | low | `cloud_tint_rgb_hex` 의 하류. 무채색에 가까운 창백한 차가운 거대 행성 |
| `planet_disk_tint_rgb_hex_accent` | `#b8bcb0` (데크가 얇아지는 곳의 희미한 회녹색 밴드 그림자) | low | Tie-break. 275 K 의 약한 대류 구동에서 belt–zone 대비 최소. 차가운 거대 행성은 거의 특징 없게 읽혀 목성보다 훨씬 균일 |
| `rotation_period_hours` | 10 | low | Tie-break. 자전 측정 없음. 더 느린 토성/천왕성 값 대신 목성형 ~10 h 채택. 질량 큰 거대 행성의 각운동량 예산은 빠른 자전을 선호. within-window, 제약 안 됨 |
| `ring_present` | false | medium | 어떤 JWST/MIRI epoch 에서도 고리 미관측 (Matthews 2024, 2026). cfg 기본값은 고리 없음. 얼음 고리는 선택적 cfg 변종으로 보존 — Open items 참조 |
| `ring_observed` | false | high | Matthews et al. 2024/2026 JWST/MIRI 영상은 분해된 고리 성분 없이 행성을 밝은 점광원으로 보임 |
| `magnetic_field_strength_microtesla_equator` | 1000 | low | Tie-break. 격렬한 내부 대류와 빠른 자전을 가진 7.6 M_Jup 거대 행성은 강한 다이나모로 스케일 — 질량/대류 스케일링으로 목성의 ~430 µT 의 대략 2 배. 미적, 측정 없음 |
| `aurora_present` | false | medium | 호스트의 조용한 항성풍 (log R'HK = −4.72) 이 20.9 AU 에 매우 약한 플라스마 구동을 전달. 활동적-호스트 jovian 과 달리 강한 오로라 기대 안 됨. cfg 는 렌더 안 함 |
| `companion_to_brown_dwarf_pair` | ε Indi B (Ba T1–1.5 66.9 M_Jup + Bb T6 53.3 M_Jup), ~1459 AU | high | Chen et al. 2022 — 계층적 삼중성계의 넓은 갈색왜성-쌍 성분. 행성의 호스트는 아니지만 그 하늘의 일부 |
| `star_apparent_angular_diameter_deg` | 0.018 | high | 유도. 2 R_star / a = 2 × 0.713 R☉ / 20.9 AU × (180/π) ≈ 1.1 arcmin ≈ 0.018°. 지구에서 본 태양 각크기의 약 1/30 |
| `stellar_illumination_color_temp_k` | 4700 | high | 호스트 Phase 3 (`docs/phase3/eps-ind-a.md`) 에서 상속 |

## Surface synthesis

ε Indi A b 는 고체 표면이 없습니다 — ~7.6 M_Jup H₂/He 슈퍼목성입니다.
렌더링에 관련된 "표면" 은 구름 데크이고, ε Indi A b 의 데크가 바로 정의적
과학 결과입니다. 0.7 bar 부근에서 τ = 1 에 도달하는 두꺼운 물-얼음 구름층
(Matthews 2026 best fit) 이 암모니아가 확인된 대기 위에 얹혀 있습니다.

온도 영역이 색조의 열쇠입니다. 행성은 ~275 K 로 복사하지만 (Matthews
2024/2026), 이는 일사 온도가 **아닙니다** — 0.239 L☉ 별 주위 20.9 AU 에서
복사-평형 온도는 겨우 ~43 K (유도) 이고, 일사량은 지구의 ~5.5 × 10⁻⁴ 배
입니다. ~275 K 는 행성 스스로의 내부열로 설정됩니다. ~3.5 Gyr 의 7.6 M_Jup
거대 행성은 여전히 천천히 수축하며 형성 에너지를 복사하므로, 주변보다
~230 K 더 뜨겁게 빛납니다. 이는 ε Indi A b 를 **스스로 빛나는 차가운 거대
행성** 으로 만드는데, Matthews 2026 이 거의 동일한 mid-IR 색을 발견한 차가운
갈색왜성 WISE 0855 (~285 K) 와 같은 영역입니다.

~275 K 에서 응결 화학은 뜨거운 거대 행성의 규산염/철 구름이 아니라 물 얼음과
암모니아가 지배합니다. 암모니아는 기체상에서 확인됐고 (Matthews 2026), 그
유난히 얕은 특징의 선호 설명은 두꺼운 물-얼음 구름이 대기를 덮어 이를
억제한다는 것입니다. 따라서 cfg 는 ε Indi A b 를 **무채색에 가까운 창백한
메탄/암모니아-부류 거대 행성** 으로 렌더링합니다 — 물-얼음과 암모니아 구름은
본질적으로 약한 cold-blue 기를 띤 근-백색이고, 따뜻한 K5 V (4700 K) 조명
아래에서 지각 색조는 중성 창백한 off-white (`#dfe2dc` 구름, `#b8bcb0` limb)
로 정착합니다. 이는 태양이 비춘 목성이나 더 어리고/따뜻한 jovian 의 따뜻한
cream-amber 와 의도적으로 구별됩니다. ε Indi A b 는 차갑고 탈채도된
세계입니다.

belt–zone 대비는 최소로 렌더링됩니다. 거의-전지구적 두꺼운 구름 데크를 가진
~275 K 에서 대류 구동은 약하고, 억제된 암모니아 특징과 3–5 µm 흐림 둘 다
밴드 지고 틈이 있는 것보다 균일하고 광학적으로 깊은 커버를 가리킵니다
(Matthews 2026 은 ε Indi A b 의 균일한 커버 가능성을 WISE 0855 의 patchy
구멍 가능성과 대비). cfg 는 거의-특징-없는 데크 (`cloud_cover_fraction ≈
0.95`) 에 데크가 얇아지는 곳의 희미한 회녹색 밴드 그림자 (`#b8bcb0`) 만
선택합니다 — 목성의 선명한 belt 보다 훨씬 균일합니다.

## Atmosphere synthesis

**압력 기준.** 거대 행성은 고체 표면이 없습니다. cfg 기준 압력은 1 bar
(100 000 Pa) 입니다. 물리적으로 의미 있는 고도는 물-얼음 구름 정상입니다.
Matthews 2026 의 best-fit cloudy 모델은 0.7 bar 부근에서 광학 깊이 τ = 1 에
도달하므로, ε Indi A b 의 가시 "표면" 은 1 bar 레벨 조금 위의 구름 데크입니다.

**조성.** 본체는 어떤 거대 행성처럼 H₂/He 입니다. 측정된 성분은. F1065C–F1140C
= 0.88 ± 0.08 mag 색에서 **11σ 로 확인된 암모니아 (NH₃)** (Matthews 2026) —
이로써 암모니아가 검출된 가장 차가운 행성 — 와, 예상보다 얕은 암모니아 특징
및 흐린 3–5 µm 방출의 선호 설명인 **두꺼운 물-얼음 구름** 입니다. best-fit
cloudy 대기는 elevated 금속도 (~3× solar) 와 elevated C/O 비 (~2.5× solar) 를
가지는데, Matthews 2026 은 이것이 이렇게 질량 큰 행성에 대해 형성 모델의
난제로 남는다고 언급합니다. 얕은 암모니아 특징에 대한 두 대안 설명이
고려됐다 기각됐습니다. 저-금속도 대기 (3–5 µm flux 를 지상 상한 위로
밝히므로 기각) 와 85–95% 질소 고갈 (가능하나 형성 모델 예측보다 극단적)
입니다. cfg 는 확인된 암모니아와 물-얼음 구름을 high 신뢰도로, 정확한 혼합비를
medium 신뢰도로 인코딩합니다.

**구름 정상 / 위성 관측자에서의 하늘 외형.** 구름 정상에서 하늘은 두껍고
창백한 얼음빛 흐림입니다 — 밴딩이 거의 없는 근-균일 off-white 로, 작고 멀고
따뜻한 오렌지-호박색 별이 비춥니다. ε Indi A 는 20.9 AU 에서 ~1.1 arcmin
(0.018°) 만 차지해, 지구에서 본 태양 각크기의 약 1/30 — 원반이 아니라 눈부신
오렌지-호박색 점입니다. 빛은 약하고 (지구 일사량의 ~5.5 × 10⁻⁴), 그래서
주간면은 어둡습니다. 행성 에너지의 대부분은 내부에서 옵니다. 하늘 건너편
멀리, ~1459 AU 에서, 갈색왜성 쌍 ε Indi B (Ba + Bb) 가 두 개의 희미한
깊은-적색 T-왜성 점으로 걸려 있습니다 — 이 시스템에 고유한, 희미하나마
인상적인 "별" 의 쌍입니다.

**야간면.** 의미 있는 항성 조명 없음. 행성 스스로의 내부 flux 가 구름 정상을
~275 K 로 유지하며 중적외선 (정점 ~10 µm) 으로 복사합니다 — 눈에는 보이지
않지만 정확히 JWST/MIRI 가 검출한 밴드입니다. 기대되는 가시 오로라는
없습니다. 20.9 AU 에서 호스트의 조용한 항성풍은 매우 약한 플라스마 구동으로,
카탈로그의 활동적-호스트 jovian 과 다릅니다.

## Rotation & spin synthesis

ε Indi A b 의 자전 측정은 없습니다. 호스트로부터의 각거리 (~3.65 arcsec,
Matthews 2026) 가 넓고 행성이 mid-IR 에서 밝아, 미래의 고분해 Doppler-broadening
측정 (Snellen 2014 의 β Pic b 기법) 은 상상할 수 있으나 아직 이뤄지지
않았습니다.

**조석 감쇠 논거.** 0.78 M☉ 별 주위 20.9 AU 에서 목성-부류 행성의 조석
시간척도는 시스템 나이를 여러 자릿수 초과합니다. ε Indi A b 는 조석 고정이
**아닙니다**. cfg 는 `tidally_locked = false` 로 설정합니다.

**자전 주기 선택.** 태양계 거대 행성 중 자전 주기는 질량과 약하게 스케일하고,
질량 큰 거대 행성은 원반 강착에서 큰 각운동량 예산을 물려받습니다. cfg 는
목성형 `rotation_period_hours = 10` 을 선택합니다 — 어떤 측정으로도 제약되지
않은 within-window tie-break 입니다. ~7.6 M_Jup 거대 행성의 ~10 h 자전은 원칙적
으로 강한 코리올리 밴딩을 만들지만, ~275 K 에 두꺼운 균일 구름 데크라 가시
밴드 대비는 억제됩니다 (Surface 참조).

**경사 (obliquity).** Tie-break 미적 선택. cfg 는 27° (토성형) 를 선택해
선택적 얼음 고리와도 자연스럽게 읽히는 시각적으로 뚜렷한 축 기울기를 줍니다.
목성의 근-제로 3.1° 는 덜 흥미롭고 천왕성의 극단적 기울기는 동기가 없습니다.
~108 yr 궤도 주기와 약한 일사로, obliquity 는 관측 가능한 계절 효과를 만들지
않습니다 — 행성의 에너지 예산은 내부적입니다.

**KSP 구현 노트.** 자전 주기 = 10 h = 36 000 s (`rotationPeriod = 36000`).
obliquity ≈ 27° (궤도 법선 기준).

## Visual styling

표면 (구름-데크) 과 대기 결정을 결합하면, ε Indi A b 는 차갑고 무채색에
가까운 창백한 슈퍼목성으로 렌더링됩니다 — 카탈로그에서 가장 차갑고 가장
탈채도된 거대 행성입니다.

- **전체 외형.** 궤도에서 ε Indi A b 는 약 1.12 R_Jup (~80 000 km) 폭의
  창백한 off-white 원반 (`#dfe2dc`) 입니다 — 반지름은 목성보다 약간 크지만
  질량은 ~7.6 배라, 밀도 높고 압축된 세계입니다. 외형은 무채색에 가깝고
  거의-특징-없습니다. belt–zone 대비가 최소인 두꺼운 물-얼음 구름 데크로,
  태양이 비춘 목성의 따뜻한 cream-amber 와 의도적으로 구별됩니다. 시각적으로
  WISE 0855 유사체를 모델로 한 메탄/암모니아-부류 차가운 거대 행성입니다.
- **구름-데크 세부.** 거의-전지구적인, 광학적으로 매우 깊은 물-얼음 구름
  커버 (~95%) 에 데크가 얇아지는 곳의 희미한 회녹색 밴드 그림자 (`#b8bcb0`)
  만 있습니다. 제약된 선명한 폭풍이나 대적반 유사체는 없습니다. cfg 는
  차갑고 약-대류 영역을 위해 차분하고 균일한 데크를 선택합니다.
- **Limb 헤이즈.** 창백하고 무채색에 가까운 회녹색 limb (`#b8bcb0`) — 따뜻한
  K5 V 조명 아래 차가운 물-얼음 + 암모니아 산란으로, 밝은 cream limb 가 아니라
  얇은 탈채도된 halo 입니다.
- **야간면.** 말할 만한 항성 조명 없음. 구름 정상이 내부열에서 중적외선으로
  희미하게 빛납니다 (~275 K) — 눈에는 보이지 않고 플레이어 시야에는 어두우며,
  가시 오로라는 없습니다.
- **하늘의 별.** ε Indi A 는 행성에서 ~0.018° (1.1 arcmin) 만 차지합니다 —
  지구에서 본 태양 각크기의 약 1/30 — 눈부신 따뜻한 오렌지-호박색 (K5 V,
  `#ffb870`) 점으로, 지구 일사량의 ~5.5 × 10⁻⁴ 만 전달합니다. 주간면은
  어둡고 차갑습니다.
- **하늘의 갈색왜성 쌍.** ~1459 AU 에서 ε Indi Ba + Bb (Chen 2022) 가 두 개의
  희미한 깊은-적색 T-왜성 점으로 나타납니다 — 행성을 비추기엔 너무 어둡지만
  광역 렌더에서는 뚜렷한 쌍으로, ε Indi A b 를 K-왜성 + 슈퍼목성 + 갈색왜성-쌍
  계층 시스템의 일부로 표시합니다.
- **선택적 얼음 고리 (예술적 — 미관측).** 토성형 얼음 고리는 기본값이 아니라
  cfg *변종* 으로 제공됩니다. 어떤 JWST/MIRI epoch 에서도 **고리는 관측되지
  않았고** (Matthews 2024, 2026), cfg 기본값은 `ring_present = false` 입니다.
  이 변종은 물리적으로 그럴듯합니다 — 차가운 (~275 K) 거대 행성은 물-얼음 /
  암모니아-얼음 고리계를 쉽게 유지합니다 — 그리고 27° obliquity 에 맞춰
  기울어진 창백하고 약간 푸르스름한-흰 고리띠로 렌더링됩니다. Open items 에
  opt-in 으로, 예술적이라고 분명히 표기해 보존됩니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Matthews E. C. et al. 2026** — *A second visit to ε Ind Ab with
  JWST: new photometry confirms ammonia and suggests thick clouds in the
  exoplanet atmosphere of the closest super-Jupiter*, ApJL
  (doi:10.3847/2041-8213/ae5823, arXiv:2603.08780). 두 번째 JWST/MIRI
  관상 epoch (F1140C, 11.3 µm) + 아카이브 데이터. **암모니아 확인**
  (F1065C–F1140C = 0.88 ± 0.08 mag, 11σ). 얕은 특징은 **두꺼운 물-얼음
  구름** 으로 가장 잘 설명 (best fit. 275 K, log g 4.5, 3× solar [M/H],
  2.5× solar C/O, H₂O 구름 τ = 416, 0.7 bar 부근 τ = 1). 재-피팅 궤도.
  M = 7.63 (+0.73/−0.70) M_Jup, a = 20.9 (+5.8/−3.3) AU, e = 0.244
  (+0.11/−0.083), i = 102.3°, Ω = 44.6°, ω = 62°, P ≈ 108 yr. **핵심
  논문** — 궤도, 질량, 대기 Decisions 행을 구동. Phase 2 recommended 앵커.
- **Matthews E. C. et al. 2024** — ε Indi A b 의 JWST/MIRI 직접 촬영
  발견 (`2024Natur.633..789M`, arXiv:2503.01599). 10.6 과 15.5 µm 의
  첫-epoch 측광. ~275 K 차가운 거대 행성, elevated 금속도를 함의하는 3–5 µm
  흐림 (NaCo 비검출), 공통-고유운동 논거를 확립. **핵심 논문.** (캐시에
  ar5iv 전문 없음 — HTML-only stub. 숫자는 초록과 Matthews 2026 의 요약에서
  취함.)
- **Feng F. et al. 2019** — *Detection of the nearest Jupiter analog in
  radial velocity and astrometry data*, MNRAS 490, 5002
  (`2019MNRAS.490.5002F`, doi:10.1093/mnras/stz2912, arXiv:1910.06804).
  RV + Hipparcos/Gaia 측성 검출. 호스트 광도 (0.239 L☉) 의 Phase 2 출처.
  여기서의 행성 파라미터 (a ≈ 11.6 AU, ~3.25 M_Jup, P ~45 yr) 는 pre-JWST
  값으로 Matthews 2026 이 대체. DB 에 `recommended:false` 로 보존.

### Read (context / methodology, not decision-driving)

- **Lundkvist M. S. et al. 2024** — *Low-amplitude solar-like
  oscillations in the K5 V star ε Indi A*, ApJ 964, 110
  (`2024ApJ...964..110L`, arXiv:2403.04509). 호스트 별 측성지진 질량
  (0.782 M☉), R (0.713 R☉), Teff (4700 K), 그리고 ~7.1 yr 활동 주기. 일사와
  조명-색온도 행을 설정하는 호스트 항성 파라미터를 제공. 호스트 Phase 3
  (`docs/phase3/eps-ind-a.md`) 에 상술.
- **Chen M. et al. 2022** — *Precise Dynamical Masses of ε Indi Ba and
  Bb* (`2022AJ....163..288C`, arXiv:2205.08077). 넓은 갈색왜성 쌍의 역학
  질량 (Ba T1–1.5 66.9 M_Jup, Bb T6 53.3 M_Jup, ~1459 AU) 과 ε Indi A b 를
  "태양-나이" 거대 행성으로 틀 짓는 시스템 활동-나이 (~3.5 Gyr). 갈색왜성-쌍
  맥락 행을 구동.
- **Feng F. et al. 2018** — *Detection of the closest Jovian exoplanet in
  the ε Indi triple system* (`2018arXiv180308163F`, arXiv:1803.08163).
  RV 발견 프리프린트. 가장 이른 행성 파라미터 (M sin i ~2.7 M_Jup,
  a ~12.8 AU) 로, Feng 2019 / Matthews 2026 이 대체. DB 에 `recommended:false`
  로 보존.

### Read (instrument-only, not visual-informative)

- Matthews 2026 의 JWST/MIRI 관상 환원 (spaceKLIP / pyKLIP RDI, four-quadrant
  phase mask, glow-stick 배경 차감) 과 orvara 궤도-피팅 기계는 측광과 질량의
  기기적 골격이지만, 위에서 쓴 숫자 이상의 직접 시각 필드를 주지는 않습니다.
  PICASO/Virga cloudy-대기 모델링이 구름 τ 와 best-fit 파라미터를 공급하며
  이미 인용됐습니다.

### Not read — no arXiv preprint or low-priority (~handful)

Matthews 2026 안에 인용된 Sonora Flame Skimmer / Elf Owl / Bobcat 모델
그리드와 WISE 0855 냉각-모델 참고문헌 (Mukherjee 2024. Marley 2021. Kühnle
2025) 은 맥락용으로 읽었지만, 이미 쓴 best-fit 파라미터 이상의 ε-Indi-A-b cfg
수치를 주지는 않습니다. 다가오는 JWST 3–20 µm 분광 (GO #8438, #8714) 은 아직
출판되지 않았습니다. 이 행성에 대해 핀된 세트 이상의 논문은 fetch 되지
않았습니다.

## Open items for follow-up

- **JWST 3–20 µm 분광 (GO #8438, #8714).** 다가오는 JWST 관측은 얕은
  암모니아 특징이 물-얼음 구름·저-금속도·질소 고갈 중 무엇 때문인지 가려야
  하고, 금속도·C/O·구름 f_sed 를 못박아야 합니다. 스펙트럼이 나오면
  `atmosphere_composition`, `cloud_morphology`, `bond_albedo`, 색조 hex 를
  재유도합니다.
- **얼음-고리 cfg 변종 (예술적).** 기본값은 `ring_present = false` 입니다 —
  관측된 고리가 없습니다 (Matthews 2024/2026). 원하는 사용자를 위해 선택적
  창백한 얼음-고리 변종을 보존합니다. 차가운 ~275 K 거대 행성에 물리적으로
  그럴듯하며, 27° obliquity 에 기울어진 희미한 푸르스름한-흰 고리띠로
  렌더링됩니다. 데이터 기반이 아니라 예술적이라고 분명히 표기.
- **a–e 축퇴.** ~108 yr 궤도에 ~30 yr RV 라 반장축과 이심률이 강하게 상관
  됩니다 (Matthews 2026). a ≈ 19 AU 의 거의-원형 해도 허용됩니다. 지속
  모니터링 (Rajpoot et al. in prep.) 이 둘 다 조일 것입니다. 궤도가
  정밀화되면 cfg 를 갱신해야 합니다.
- **자전과 경사.** 둘 다 within-window tie-break (10 h, 27°) 입니다. ~3.65
  arcsec 분리에서의 미래 Doppler-broadening 측정이 자전 추정을 교체할 것
  입니다. 경사는 곧 측정될 가능성이 낮습니다.
- **유효 온도 대 평형 온도.** cfg 는 측정된 ~275 K 유효 온도 (내부-가열 지배)
  와 유도된 ~43 K 복사-평형 온도를 모두 인코딩합니다. 미래 cfg 는 스스로
  빛나는 차가운 거대 행성을 충실히 렌더링하려면 행성의 열 빛을 일사가 아니라
  ~275 K 내부값으로 구동해야 합니다.
- **Phase 2 대기 ingest.** ε Indi A b 는 DB 에 Phase 2 대기 블록이 없습니다
  (궤도 + 물리만). 스키마가 확장되면 Matthews 2026 의 암모니아 검출과 물-얼음-
  구름 best-fit 을 위 cfg 선택에 맞춘 `atmosphere_measurements` 레코드로
  ingest 해야 합니다.

## Related

- [eps-ind-a](eps-ind-a.md) — 호스트 별 Phase 3 합성. K5 V M_star / R_star /
  L_star / 나이 와 조명-색온도 기준, 그리고 갈색왜성-쌍 맥락을 제공
- [eps-eri-b](eps-eri-b.md) — 비교용 가까운 K 왜성 주위 차가운 jovian
  (~0.78 M_Jup, 3.5 AU, ~110 K). ε Eri b 의 저-질량, 일사로-설정된 따뜻한-cream
  토성-유사체를 ε Indi A b 의 질량 크고, 내부-열-지배, 물-얼음-구름 차가운 거대
  행성과 대비
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — 이 거대 행성의 대기 결정을
  소비하는 하류 Kopernicus / EVE / Scatterer cfg 작성기
- [rex-data-comparison](../reference/rex-data-comparison.md) — REX 는 ε Indi A b
  엔트리가 없음. 가장 가까운 직접 촬영 차가운 슈퍼목성은 NearStars 추가분
