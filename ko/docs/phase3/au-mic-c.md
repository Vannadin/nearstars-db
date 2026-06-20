<!-- AU Mic c Phase 3 합성. cfg-ready 결정과 근거 -->
# AU Mic c — Phase 3 Synthesis

AU Microscopii c 는 22 Myr 의 M1Ve flare star AU Mic 주위 18.86 d
궤도를 도는 2.79 ± 0.18 R⊕, 14.46 ± 3.24 M⊕ 의 따뜻한 sub-Neptune
입니다. Martioli et al. 2021 (A&A 649, A177. `2021A&A...649A.177M`.
arXiv:2102.05288) 이 더 긴 주기 때문에 원래의 Sector 1 탐색에서
놓쳤던 TESS Sector 27 통과에서 행성을 발견했고, Mallorquin et al.
2024 (A&A 689, A132. `2024A&A...689A.132M`) 가 결합된 ESPRESSO + TESS
재분석으로 질량과 반지름을 모두 정밀화했습니다. bulk 밀도는 ≈ 3.7
g/cc — 지구의 약 2/3 — 로, 통상의 암석 super-Earth 보다는 낮지만
b 의 0.45 g/cc puffy 영역보다는 상당히 높습니다. c 는 가스 우세
sub-Neptune 과 물 풍부 암석 행성 사이의 질량-반지름 "골짜기" 에
앉습니다 — bulk 조성이 암석/철 코어 위의 ~5% H/He envelope 또는
최소한의 수소 envelope 위의 상당한 물 풍부 mantle 중 어느 것과도
일관됩니다. 이 글 작성 시점까지 대기 검출은 보고되지 않았습니다.

**NearStars 시나리오 선택. 조석 lock 된 따뜻한 sub-Neptune 으로,
물 풍부 암석/철 코어 위에 얇은 H/He envelope (~5% 질량). 구름 데크
표면 압력 ~10⁶ Pa, M-왜성 조명 하의 띠상 구조를 가진 적당한 구름
형태, 뜨거운 주간 측면, 그리고 c 의 더 깊은 중력 우물과 더 낮은
일사 때문에 b 보다 덜 두드러진 대기 탈출 시그너처.** 26 개 cfg 픽
모두 sub-Neptune 문헌 윈도우 안에서 canonical-aligned. 두 개는 tie-break
(대기 색 hex, 구름 색 hex). documented divergence 없음.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false (pseudo-synchronous; 3:2 candidate) | high | 18.86 d 궤도. 0.51 M☉ 주위 0.119 AU 의 sub-Neptune 에서 조석 감쇠 ≪ 22 Myr. 다만 e = 0.18 이 의사 동기 자전을 구동 (Hut 1981 ω/n ≈ 1.24) — 순수 1:1 이 아닌 3:2-capture 영역 |
| `obliquity_deg` | 5 | high | 조석 감쇠가 0 을 향하지만, 이심 의사 동기 spin 상태를 위해 작은 잔차를 유지 |
| `eccentricity` | 0.18 | medium | Mallorquin 2024 ESPRESSO + TESS 결합 fit |
| `argument_of_periastron_deg` | 72.8 | medium | Mallorquin 2024 |
| `sidereal_period_days` | 18.859023 | high | Martioli 2021 TESS Sector 27 + Sector 1 |
| `semi_major_axis_au` | 0.119 | high | Mallorquin 2024 (M☉ + P 에서 케플러 제3) |
| `inclination_deg` | 89.46 | high | Martioli 2021 통과 fit. Mallorquin 2024 가 정밀화 |
| `mass_mearth` | 14.46 ± 3.24 | high | Mallorquin 2024 ESPRESSO RV with GP detrending |
| `radius_rearth` | 2.79 ± 0.18 | high | Mallorquin 2024 TESS 재분석 |
| `surface_gravity_g_earth` | 1.86 | high | 유도 = 14.46 / 2.79² |
| `density_g_cc` | 3.7 | high | 유도. ≈ 0.67 ρ_Earth — 얇은 H/He + 암석 코어 또는 물 풍부 mantle 과 일관 |
| `insolation_s_earth` | 7.2 | high | L = 0.102 L☉ (Donati 2023, recommended) 과 a = 0.119 AU 에서 유도 |
| `equilibrium_temp_k` (A=0) | 454 | high | 유도. TEPCat 의 albedo 0 아닌 값 보고 428 K 와 일관 |
| `equilibrium_temp_k` (A=0.1) | 442 | high | 유도. 적당한 sub-Neptune albedo |
| `bond_albedo` | 0.10 | medium | sub-Neptune 유사 낮은 albedo. 구름 데크 반사율 |
| `dayside_surface_temp_k` | 500 | medium | b 보다 얇은 envelope → 주야 재분배가 적음. 주간이 T_eq 보다 살짝 높음. Cowan & Agol 2011 (`1001.0012`) 의 주야 열재순환(+ 내부열) 매개변수화를 약(弱)재순환 극한에서 적용해 추정함 |
| `nightside_surface_temp_k` | 380 | medium | 얇은 H/He envelope 의 적당한 재분배. Cowan & Agol 2011 (`1001.0012`) 의 열재순환(+ 내부열) 매개변수화로 추정함 |
| `atmosphere_present` | true (얇은 H/He envelope) | medium | 밀도가 envelope 질량 ~5% 와 일관. Lopez & Fortney 2014 스케일링. 아직 직접 대기 검출 없음 |
| `atmosphere_surface_pressure_pa` | 1.0e6 | medium | 얇은 envelope 의 구름 데크 압력. sub-Neptune analog. Owen & Wu 2017 광증발 골짜기 프레임워크 |
| `atmosphere_composition` | H₂ ~80%, He ~15%, H₂O ~2%, CH₄ + NH₃ + CO 미량. 가능한 광화학 haze | medium | sub-Neptune analog. water-world variant 라면 H₂O 가 더 높을 수 있음 (5–10%) |
| `atmosphere_scale_height_km` | 82 | high | 유도. T = 450 K, μ = 2.5 (H/He + 무거운 admixture), g = 18.2 m/s² 의 kT/μg |
| `atmosphere_tint_rgb_hex` | `#8a6a4c` | low | Tie-break. interesting-first. M-왜성 SED 하 sub-Neptune 광화학 haze → muted red-brown. b 와 비슷하지만 인플레이션이 덜해 덜 두드러짐 |
| `cloud_cover_fraction` | 0.65 | medium | sub-Neptune analog 의 띠상 구조이지만 puffy Neptune 보다는 변동성 큼 |
| `cloud_morphology` | 적도 superrotation 의 띠상 zonal 구름 구조. b 보다 덜 두드러짐. terminator 에서의 H₂O/NH₃ 얼음 구름 응결 가능 | medium | Showman 2009 을 sub-Neptune 온도 + 자전으로 스케일. 따뜻한 sub-Neptune 에 대한 canonical |
| `cloud_tint_rgb_hex` | `#b0987a` | low | Tie-break. M1V 의 붉은빛 하 muted 크림. b 의 더 밝은 구름과 시각적 차별화를 위해 선택 |
| `surface_morphology` | n/a — 구름 데크 반지름에서 보이는 단단한 표면 없음. 더 깊은 내부는 물 풍부 mantle + 암석/철 코어일 가능성 | medium | 밀도와 질량-반지름 위치가 c 를 sub-Neptune envelope 영역 안쪽에 놓음 |
| `magnetic_field_present` | true | medium | sub-Neptune H 풍부 envelope 이 적당한 dynamo 를 유지 (얼음 거대 행성 analog) |
| `magnetic_field_strength_microtesla_equator` | 50 | low | 자릿수 수준의 **얼음 거대 행성 analog** (Neptune/Uranus ~0.1–0.5 G. Connerney 1991). envelope 가 작아 b 아래로 스케일. Christensen 2009 / Reiners & Christensen 2010 에너지플럭스 스케일링의 검증 영역 (≥0.3 M_Jup) 아래에 있다 (He 분리, Stevenson 1980) → 추정이지 측정이 아니다. (논문 캐시에 없는 Yadav & Thorngren 2017 인용을 대체.) docs/reference/planetary-dynamo-scaling.md 참고 |
| `atmospheric_escape_rate_g_s` | 1e8 | medium | Lecavelier des Etangs 2007 (`astro-ph/0609744`) 을 따른 에너지 한정 탈출. b 의 Allart-2023 기반 ~1e10 g/s 값에서 c 의 더 깊은 중력 우물과 낮은 일사를 반영해 축소 |
| `aurora_present` | true | low | H 풍부 상층 대기 + AU Mic 항성풍 → H Balmer-α 예상. 다만 대기 질량이 작아 b 보다 약함 |
| `aurora_color_primary_hex` | `#ff6e8c` | low | Tie-break. H-α 656.3 nm 지배. b 와 같은 색 계열이지만 더 옅음 |
| `star_apparent_angular_diameter_deg` | 3.9 | high | 유도. 2 × 0.862 R☉ / 0.119 AU × (180/π) ≈ 3.9° |
| `stellar_illumination_color_temp_k` | 3665 | high | host 별 Teff 에서 |

## Surface synthesis

AU Mic c 는 sub-Neptune 영역의 하단 가장자리에 앉습니다. 질량 14.46
M⊕ 와 반지름 2.79 R⊕ 가 밀도 3.7 g/cc 를 줍니다 — 다음 둘 중
하나와 일관됩니다.

1. **얇은 H/He envelope** (질량 ~5%) 위의 암석/철 코어. Lopez &
   Fortney 2014 질량-반지름 다이어그램은 2.79 R⊕ / 14.46 M⊕ 를
   ≤ 10% H/He envelope 가 암석 코어를 관측 크기로 부풀리는 영역에
   둡니다. 이것이 canonical sub-Neptune 해석이고 cfg 의 기본 reading
   입니다.

2. **water-world variant**. 상당한 H₂O mantle (질량 30–40% 정도) 과
   최소한의 수소 envelope. 이도 bulk 밀도와 일관 (water world 에 대한
   Zeng 2019 질량-반지름) 이고 의미 있는 대안 — 하지만 sub-Neptune
   골짜기 (Fulton 2017. Owen & Wu 2017) 가 c 의 영역에 있는 행성에
   대해 H/He-envelope 해석을 통계적으로 선호하고, AU Mic 의 어린
   나이 (22 Myr) 가 나이 든 시스템보다 primordial H/He envelope 가
   더 잘 유지되었을 가능성을 만듭니다.

NearStars 의 목적에서 플레이어가 보는 "가시 표면" 은 ~10⁶ Pa 의
H/He 구름 데크 꼭대기로, b 보다 덜 두드러진 띠 패턴의 띠상 가스
천체로 렌더링됩니다 (더 작은 envelope 질량 + 더 느린 자전 때문).
렌더링할 암석 지형은 없습니다. 내부 구조 — 암석/철 코어, H₂O/규산염
mantle, H/He envelope — 는 밀도 inversion 에 영향을 주지만 가시
외관에는 영향을 주지 않습니다.

시스템의 어린 나이가 여기서도 계속 중요합니다. 22 Myr 에서 c 는
아직 수축 중입니다. 현재 밀도 3.7 g/cc 는 envelope 가 식고 행성이
반지름에서 ~10–15% 축소되면서 Gyr 나이에 약 4.5 g/cc 로 증가할
것입니다. 이는 단일 cfg 에서 렌더링하기엔 너무 미묘하지만, 나이 든
시스템 동급보다는 현재의 inflated 상태를 기본값으로 다루는 것을
정당화합니다.

## Atmosphere synthesis

c 의 대기는 직접 검출되지 않았지만 그 존재와 속성은 간접적으로
제약됩니다.

**압력.** 통과 유도 반지름이 얇은 H/He envelope 의 구름 데크 압력을
대략 10⁶ Pa 로 고정합니다. c 가 water-world variant 라면 이 압력의
지배적 가스가 H₂ 가 아니라 초임계 증기일 것이지만, 가시 구름 데크
위치는 비슷할 것입니다. cfg 는 thin-envelope 해석을 headline reading
으로 채택합니다.

**조성.** 이 글 작성 시점까지 c 에 대한 직접 대기 측정이 없습니다.
조성은 bulk 밀도 + sub-Neptune 질량-반지름 골짜기에서 추론됩니다.
H₂ ~80%, He ~15%, 미량 H₂O, CH₄, NH₃, CO 가 거의 태양 풍부도. AU Mic
의 강한 XUV 하 CH₄ 광분해로부터의 광화학 haze 가 예상됩니다. 이들이
Titan 에 견줄 만한 haze 층으로 응결할지는 상층 대기 C/O 비율 (c 에
대해 측정되지 않음) 에 의존합니다. cfg 는 cloud_cover_fraction 0.65
의 적당한 haze 층을 채택합니다 — c 의 인플레이션이 덜하고 직접 구름
검출 증거가 없어 b 의 0.70 보다 살짝 낮습니다.

**하늘 외관.** 저궤도에서 c 는 b 의 더 작고 덜 인플레이션된 버전
처럼 보입니다. 깊은 붉은 M1V 조명 하의 muted red-brown 띠. 적도
superrotation jet 이 보이지만 b 보다 덜 두드러집니다. 구름 꼭대기
색 (`#b0987a`) 은 b 의 (`#c0a880`) 보다 더 muted 입니다 — 더 높은
중력과 줄어든 대기 스케일 높이 때문에 가시 column 의 haze 축적이
적습니다. 별이 c 의 하늘에서 3.9° 를 채우고 (지구에서 본 태양의 약
7 배) 지배적 조명원입니다. substellar 구름 꼭대기에서 표면 일사량은
지구의 7.2 배. red-shift 됩니다.

**대기 탈출.** c 가 0.119 AU 에서 지구의 7.2 배 일사를 받으므로,
XUV 구동 탈출률은 b 의 약 한 자릿수 낮습니다. AU Mic 의 포화 영역
XUV 플럭스 하 에너지 한정 가정에서 ~10⁸ g/s. 이는 시스템의 예상
수명에 걸쳐 H/He envelope 의 몇 % 를 잃기에는 충분합니다 — 장기
진화에 대해서는 의미 있지만 현재 시각 외관에 대해서는 미미합니다.
c 등가 정밀도의 He I 10830 Å 검출이 시도된 적 없습니다. 현재
기기로 시도한다면 b 에 견줄 만한 탈출 꼬리가 가능하지만 낮은
유의성일 것입니다.

## Rotation & spin synthesis

0.51 M☉ 주위 0.119 AU 의 18.86-d sub-Neptune 에 대한 조석 감쇠는
~10⁶–10⁷ 년 시간 척도로 진행됩니다 (Goldreich & Soter 1966, Neptune-
like Q ≈ 10⁴). 22-Myr 시스템 나이에 걸쳐 c 는 조석적으로 진화했습니다
(감쇠 ≪ 나이, 다만 b 보다 시스템 나이에 더 가까움). 이심률 0.18
(Mallorquin 2024) 에서 spin 은 순수 1:1 이 아니라 의사 동기
(super-synchronous) 상태로 정착하며, Mercury 식 3:2 공명도 충분히 가능합니다.
cfg 는 의사 동기 상태를 채택하고 (`tidally_locked = false`), 3:2 변형은
Open items 에 보존됩니다. 이 글
작성 시점까지 c 에 대한 spin–orbit 각도 측정 (Rossiter–McLaughlin)
은 출판되지 않았습니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 18.859023 일 (1 629 419.6
초). Kopernicus `rotationPeriod` 는 궤도 `period` 와 일치해야 함.

**약한 계절 변조.** Obliquity 는 0 으로 감쇠. 다만 이심률 0.18 이
궤도 따라 상당한 일사 변동을 구동 (1 +/- 36%). Periapsis 일사 ~11 S⊕,
apoapsis ~5 S⊕ — 2 배 변동. 두꺼운 대기가 이를 ~30 K 구름 꼭대기
온도 변동으로 평탄화하며, periapsis 근처에서 주간이 적당히 밝아지는
것으로 보입니다.

**주야 재분배.** b 보다 얇은 H/He envelope 로 c 의 대기는 야간으로
열을 재분배하는 효율이 떨어집니다. 예상 주야 대비. ~120 K (주간
500 K, 야간 380 K). phase 곡선 관측 시도 없음. AU Mic c 통과 깊이
에서 host 별 흑점 신호가 지배할 것입니다.

## Visual styling

AU Mic c 의 시각 표현은 b 의 더 부드럽고 작은 사촌입니다.

- **전반 외관.** muted zonal 띠를 가진 따뜻한 sub-Neptune 디스크.
  AU Mic 의 각지름 3.9° (지구에서 본 태양의 7 배 — 여전히 지배적
  이지만 더 이상 압도적이지는 않음) 가 비춥니다. 디스크는 muted
  red-brown 띠 (`#8a6a4c` 주 haze, `#b0987a` zone 구름) 를 보입니다
  — 렌더링할 대기 질량이 적어 b 보다 살짝 더 muted.
- **띠 구조.** 적도 superrotation jet 이 옅은 적도 zone 과 더 어두운
  중위도 belt 를 만듭니다. 극 영역은 미묘한 hood-like 어두워짐을
  보입니다. 더 작은 대기 스케일 높이 (82 km vs. 567 km) 때문에 띠가
  b 보다 좁습니다 — 넓은 zone 이 아니라 가는 줄로 보입니다. Tie-break.
  시각적 흥미를 위해 균일 haze 가 아닌 띠 선택.
- **구름 꼭대기 텍스처.** b 보다 덜 격렬함 — c 의 더 작은 스케일
  높이 + 더 느린 자전이 eddy 와 Rossby wave 가 더 천천히 발달함을
  의미합니다. 구름 꼭대기는 fine-scale 섭동을 가진 비교적 매끈한
  띠 표면으로 읽힙니다.
- **두드러진 탈출 꼬리 없음.** b 와 달리 c 의 대기 탈출은 ~10⁸ g/s
  로 추정 — 혜성-like 꼬리가 아니라 옅은 확장 halo 로만 보임. cfg
  는 이를 super-flare 이벤트 동안 주야 terminator 의 미묘한 상층
  대기 glow 로 렌더링하며, 이산적 후행 구조는 아닙니다.
- **하늘의 별.** AU Mic 이 c 의 하늘에서 3.9° 를 차지 (지구에서 본
  태양의 7 배) — 주간 하늘을 지배하는 적당한 크기의 깊은 붉은
  디스크. substellar 구름 꼭대기에서 표면 일사량 지구의 7.2 배.
  Super-flare 가 10–60 분간 조명을 1–3 등급 밝힙니다 — 거리가 더
  멀어 b 에서보다는 살짝 덜 극적입니다.

35–210 AU 의 가장자리 정면 잔해 원반은 AU Mic 양옆으로 가늘고 밝은
줄로 보이며 b 에서 본 시야와 비슷하지만, c 가 더 바깥에 있어 원반의
안쪽 가장자리가 이제 각도상 더 가까워졌습니다 (c 에서 본 AU Mic 으로
부터의 원반 안쪽 가장자리 ~3.3°. b 에서 본 것은 ~5°). 자매 행성 b
(안쪽) 와 d (안쪽) 가 conjunction 에서 작은 점으로 보입니다. e (바깥
쪽, 확인된다면) 도 보임. AU Mic 의 디스크를 가로지르는 b 의 통과가
c 에서 보입니다 (b 의 궤도면이 같은 가장자리 정면 기하 안에 있음).
이는 항성 디스크를 가로지르는 작은 어두운 점으로 ~3 시간 동안 보일
것입니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Martioli E. et al. 2021** — *AU Mic c: a second planet transiting the young M dwarf AU Mic*, A&A 649, A177 (`2021A&A...649A.177M`, arXiv:2102.05288). TESS Sector 27 + 지상 확인으로 18.86 d 의 c. 통과 유도 반지름 2.79 R⊕. cornerstone 발견 논문.
- **Mallorquin M. et al. 2024** — *AU Mic system characterized with ESPRESSO*, A&A 689, A132 (`2024A&A...689A.132M`). ESPRESSO + TESS 결합 분석. c 의 질량을 14.46 ± 3.24 M⊕, 반지름을 2.79 ± 0.18 R⊕ 로 정밀화. **질량과 밀도에 대한 headline 출처로 채택**.
- **Lopez E. D. & Fortney J. J. 2014** — *Understanding the Mass-Radius Relation for Sub-Neptunes*, ApJ 792, 1 (`2014ApJ...792....1L`, arXiv:1311.0329). 질량-반지름 envelope 질량 분율 보정. c 의 파라미터가 ~5% H/He envelope 를 줌. cfg 표면 압력 픽을 구동.
- **Fulton B. J. et al. 2017** — *The California-Kepler Survey III: Gap in the Radius Distribution of Small Planets*, AJ 154, 109 (`2017AJ....154..109F`, arXiv:1703.10375). ~1.8 R⊕ 의 sub-Neptune / super-Earth 반지름 골짜기. c 는 골짜기의 sub-Neptune 쪽에 앉아, water-world variant 보다 H/He envelope 해석을 통계적으로 선호.
- **Owen J. E. & Wu Y. 2017** — *The Evaporation Valley in the Kepler Planets*, ApJ 847, 29 (`2017ApJ...847...29O`, arXiv:1705.10810). sub-Neptune 골짜기에 대한 광증발 프레임워크. 6.5 S⊕ + AU Mic XUV 의 c 는 Gyr 시간 척도에서 envelope 보전 임계점 위에 적당히 있지만 22 Myr 에서는 그 한참 아래.

### Read (context / methodology, not decision-driving)

- **Plavchan P. et al. 2020** — *A planet within the debris disk around the pre-main-sequence star AU Microscopii*, Nature 582, 497 (`2020Natur.582..497P`, arXiv:2006.13248). TESS 의 b 발견. 시스템 전반의 항성 활동 환경과 AU Mic 광도곡선의 다-흑점 복잡도에 대한 맥락 제공.
- **Cale B. L. et al. 2021** — *Diving Beneath the Sea of Stellar Activity: Chromatic Radial Velocities of AU Mic b*, AJ 162, 295 (`2021AJ....162..295C`, arXiv:2109.13996). GP detrending 으로 b 의 첫 견고한 RV 질량. c 에 적용된 방법론.
- **Wittrock J. M. et al. 2023** — *Transit Timing Variation Measurements and Dynamical Mass Determination of the AU Mic System*, AJ 166, 232 (`2023AJ....166..232W`, arXiv:2310.10719). b 와 c 에 대한 TTV 기반 동역학 질량. d 후보 도입. Mallorquin 2024 의 불확실도 안에서 c 의 질량 확인.
- **Zeng L. et al. 2019** — *Growth model interpretation of planet size distribution*, PNAS 116, 9723 (`2019PNAS..116.9723Z`, arXiv:1906.04253). c water-world variant 해석에 사용된 water-world 질량-반지름 모델.
- **Showman A. P. et al. 2009** — *Atmospheric Circulation of Hot Jupiters*, ApJ 699, 564 (`2009ApJ...699..564S`, arXiv:0809.2089). 적도 superrotation GCM 프레임워크. 띠 형태 픽을 위해 sub-Neptune 온도와 자전으로 스케일.

### Read (instrument / non-decisive)

- **Szabó Gy. M. et al. 2021** — *Spi-Ops campaign on AU Mic c* (`2021A&A...654A.159S`, arXiv:2108.07984). c 의 CHEOPS 통과 타이밍. 주기와 경사각을 정밀화하지만 시각 cfg 를 구동하지 않음.

### Not read — no arXiv preprint or low-priority (~20 papers)

c 의 특성화에 대한 학회 초록과 제안 요약 (NIRSpec 제안, 지상 RM
시도) 은 출판된 결과 없이는 cfg-결정적 내용을 기여하지 않습니다.
시도된다면 c 의 He I 10830 Å 관측이 대기 탈출률을 의미 있게 제약할
것입니다. 이 글 작성 시점까지 그런 관측은 출판되지 않았습니다.

## Open items for follow-up

- **대기 검출.** c 에 대해 JWST 나 지상 기반 투과 스펙트럼이 출판
  되지 않았습니다. NIRSpec/NIRISS 관측이 조성을 제약하고 headline
  thin-H/He 해석이 옳은지 water-world variant 가 옳은지 드러낼 수
  있습니다. H₂O 피처가 높은 유의성으로 검출되고 H₂ 피처가 부재 하면
  cfg 를 H₂O/CH₄/CO₂ 가 지배하는 `atmosphere_composition` 의
  water-world variant 로 전환.
- **He I 10830 Å 관측.** c 에서 He I 탈출 비검출이 더 작은 탈출
  꼬리 그림을 보강할 것입니다. 검출은 H/He envelope 가 추정보다
  더 빠르게 스트립되고 있음을 함의하고 cfg 의 atmospheric_escape_rate
  가 상향 조정되어야 함을 의미합니다.
- **Phase 곡선.** c 의 Spitzer/JWST phase 곡선이 주야 온도 대비와
  구름 꼭대기 분포를 제약할 것입니다. 측정될 때까지 500 K / 380 K
  픽은 medium confidence 에 남아 있습니다.
- **3:2 spin-orbit-resonance cfg variant.** e = 0.18 에서 의사 동기
  평형 (Hut 1981 ω/n ≈ 1.24) 은 순수 1:1 이 아니라 3:2 spin-orbit-
  capture 영역에 놓입니다. 3:2 cfg variant (자전 주기 = (2/3) ×
  18.859023 d ≈ 12.57 d) 는 고정된 주간 면 대신 천천히 이주하는
  substellar 점과 이심률 구동 일사 계절을 만들어냅니다.
- **cfg variant. water world.** 물 풍부 해석 (Zeng 2019 질량-반지름
  branch) 은 thin-H/He envelope 의 의미 있는 대안입니다. "c water
  world" cfg variant 가 H₂O 얼음 구름과 살짝 다른 시각 외관 (더
  푸르스름한 구름, 더 적은 haze) 을 가진 증기 우세 대기를 배포할
  수 있습니다. follow-up cfg variant 로 등재.
- **성숙한 시스템 variant.** 1 Gyr 에서 c 는 envelope 가 식으면서
  ~2.5 R⊕ 로 축소될 것입니다. "성숙한 AU Mic c" cfg variant 가
  비교를 위해 deflated 상태를 배포할 수 있습니다.

## Related

- [au-mic](au-mic.md) — disk 기하를 포함한 host 별 합성
- [au-mic-b](au-mic-b.md) — 자매 행성. 8.5 d 의 puffy hot Neptune
- [au-mic-d](au-mic-d.md) — 자매 행성. 12.7 d 의 지구질량 TTV 후보
- [au-mic-e](au-mic-e.md) — 자매 행성. 33.1 d 의 ESPRESSO RV 후보
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — downstream cfg 작성기
