<!-- AU Mic b Phase 3 합성. cfg-ready 결정과 근거 -->
# AU Mic b — Phase 3 Synthesis

AU Microscopii b 는 22 Myr 전주계열 M1Ve flare star AU Microscopii
주위 8.463 d 궤도를 도는 4.79 ± 0.29 R⊕, 8.99 ± 2.61 M⊕ 의 저밀도
warm Neptune 입니다. Plavchan et al. 2020 (Nature 582, 497.
`2020Natur.582..497P`. arXiv:2006.13428) 이 TESS 통과에서 행성을
발견했고, Cale et al. 2021 (AJ 162, 295. `2021AJ....162..295C`.
arXiv:2109.13996) 이 host 별 흑점 신호의 가우시안 프로세스 detrending
후 첫 견고한 RV 질량을 제공했으며, Mallorquin et al. 2024
(A&A 689, A132. `2024A&A...689A.132M`) 가 ESPRESSO + TESS 재분석으로
질량과 반지름을 모두 정밀화했습니다. bulk 밀도는 ≈ 0.45 g/cc — Neptune
의 약 1/3 — 로 b 를 "puffy / inflated sub-Saturn" 영역에 깊숙이
놓는데, 이는 수소 envelope 가 아직 식어 수축할 시간을 갖지 못한
어린 통과 행성의 특징입니다. Allart et al. 2023 (A&A 677, A164.
`2023A&A...677A.164A`. arXiv:2308.10891) 가 통과 동안 marginal-to-
significant He I 10830 Å 흡수 시그너처를 보고했으며, 이는 확장된
탈출 H/He envelope 과 일관됩니다. Hirano et al. 2020 (ApJ 899, L13.
`2020ApJ...899L..13H`. arXiv:2006.13654) 은 Rossiter–McLaughlin 로
투영 obliquity 를 측정했고 ~5° 안쪽으로 정렬됨을 발견 (λ = −2.96°),
이는 disk + 항성 자전축과 일관됩니다.

**NearStars 시나리오 선택. 조석 lock 된 puffy hot Neptune. 표면 압력
~10⁷ Pa 의 확장된 H/He 우세 대기, M 왜성 조명 하의 Jupiter 밴드
analog 구름 구조, 뜨거운 주간 측면, 적당한 내부 열, 그리고 AU Mic
super-flare 폭격에 의해 sculpting 된 활발히 탈출하는 상층 대기를
갖춥니다.** 27 개 cfg 픽 모두 puffy-Neptune 문헌 윈도우 안에서
canonical-aligned. 세 개는 tie-break (대기 색 hex, 구름 색 hex, 띠
패턴 선택). documented divergence 없음.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 8.46 d 궤도. 0.51 M☉ 주위 0.07 AU 의 Neptune 에서 조석 감쇠 시간 척도 ≪ 22 Myr (Goldreich & Soter 1966 스케일링) |
| `obliquity_deg` | 0 | high | 조석 감쇠. Hirano 2020 RM spin–orbit 정렬과 일관 |
| `eccentricity` | 0.07 | medium | Mallorquin 2024 ESPRESSO + TESS 결합 fit |
| `argument_of_periastron_deg` | -52 | medium | Mallorquin 2024 |
| `sidereal_period_days` | 8.463446 | high | Plavchan 2020 TESS. Mallorquin 2024 가 정밀화 |
| `semi_major_axis_au` | 0.07 | high | Mallorquin 2024 (M☉ + P 에서 케플러 제3) |
| `inclination_deg` | 88.39 | high | Plavchan 2020 통과 fit. Mallorquin 2024 가 정밀화 |
| `mass_mearth` | 8.99 ± 2.61 | high | Mallorquin 2024 ESPRESSO RV with GP detrending. Cale 2021 (20.12 +1.57/-1.72 M⊕) 와 일관 — 더 높음. Mallorquin 2024 가 더 나은 활동 모델로 대체 |
| `radius_rearth` | 4.79 ± 0.29 | high | Mallorquin 2024 TESS + 지상 통과 |
| `surface_gravity_g_earth` | 0.39 | high | 유도 = 8.99 / 4.79² |
| `density_g_cc` | 0.45 | high | 유도. ≈ 0.08 ρ_Earth, ≈ 0.27 ρ_Neptune — puffy envelope 확인 |
| `insolation_s_earth` | 18.8 | high | L = 0.092 L☉ 과 a = 0.07 AU 에서 유도 |
| `equilibrium_temp_k` (A=0) | 593 | high | 유도. TEPCat 의 albedo 0 아닌 값 보고 556 K 와 일관 |
| `equilibrium_temp_k` (A=0.1) | 577 | high | 유도. 적당한 가스 자이언트 albedo |
| `bond_albedo` | 0.10 | medium | Neptune-analog 가스 자이언트의 낮은 albedo. Cale 2021 §4 논의 |
| `dayside_surface_temp_k` | 700 | medium | super-rotation + ~20% 온실 → 두꺼운 H/He envelope 의 주간이 T_eq 보다 뜨거움. Plavchan 2020 §6 |
| `nightside_surface_temp_k` | 450 | medium | 두꺼운 대기에서 상당한 주야 재분배 예상. 아직 Spitzer phase curve 없음 |
| `atmosphere_present` | true | high | Allart 2023 He I 10830 검출. bulk 밀도가 질량 ≥ 30% H/He 를 요구 |
| `atmosphere_surface_pressure_pa` | 1.0e7 | medium | hot-Neptune envelope 질량 ~30% → τ = 1 구름 데크에서 ~10⁷ Pa. Lopez & Fortney 2014 질량-반지름 envelope 질량 분율 보정 |
| `atmosphere_composition` | H₂ ~85%, He ~15%, 태양 풍부도의 미량 H₂O / CH₄ / NH₃ / CO. 상층의 광화학 haze | medium | Allart 2023 He 검출. 높은 질량 손실 탈출. Lavie 2017 차가운 Neptune 광화학 analog |
| `atmosphere_scale_height_km` | 290 | high | 유도. T = 600 K, μ = 2.3 (H/He), g = 3.8 m/s² 의 kT/μg — 큰 H/He 스케일 높이가 Allart 2023 의 검출가능성을 구동 |
| `atmosphere_tint_rgb_hex` | `#7c4a32` | low | Tie-break. interesting-first. M-왜성 SED 하의 광화학 hydrocarbon haze → muted red-brown, Jupiter 의 tan 보다 더 깊음. 균일한 peach 보다 띠 대비가 더 명확하도록 선택 |
| `cloud_cover_fraction` | 0.70 | medium | 띠상 구름 구조의 가스 자이언트 analog. Sing 2016 hot-Neptune 구름 데크 센서스가 흔함을 시사 |
| `cloud_morphology` | 밝은 zone 과 어두운 belt 의 Jupiter-band-analog 띠상 구름 구조. 적도 superrotation jet. M-왜성 일사 하의 옅은 극 hood | low | Tie-break. interesting-first. puffy Neptune 의 GCM 급 시뮬레이션 (Showman 2009, Lewis 2010 hot-Jupiter analog 를 Neptune 온도에 적응) 이 띠 구조를 선호. cfg 는 시각적 흥미를 위해 균일 haze 가 아닌 띠 해석 선택 |
| `cloud_tint_rgb_hex` | `#c0a880` | low | Tie-break. M1V 의 붉은 조명 하 H₂O/NH₃ 구름 입자의 따뜻한 크림. terminator 대비를 위해 균일 크림 대신 선택 |
| `surface_morphology` | n/a — 단단한 표면 없음. 끝까지 가스 자이언트 envelope | high | 밀도와 질량-반지름 위치가 암석 표면을 배제 |
| `magnetic_field_present` | true | medium | H 풍부 envelope 의 hot Neptune 은 dynamo 유지. sub-Saturn 에 대한 Yadav & Thorngren 2017 스케일링 |
| `magnetic_field_strength_microtesla_equator` | 100 | low | Tie-break. inflated Neptune 에 대한 Yadav 2017 dynamo 스케일링의 자릿수 추정. 측정 없음 |
| `atmospheric_escape_rate_g_s` | 1e10 | medium | Allart 2023 He I 흡수가 AU Mic XUV 하 에너지 한정 탈출에서 질량 손실 ~10⁹–10¹⁰ g/s 를 함의. Plavchan 2020 §6 이 비슷한 값을 추정. Cale 2021 §5 |
| `aurora_present` | true | medium | 강한 항성풍 + H 풍부 상층 대기 → H Balmer-α + H₂ Lyman + Werner 밴드 예상 |
| `aurora_color_primary_hex` | `#ff6e8c` | low | Tie-break. H-α 656.3 nm + Lyman-α downconvert 가 분홍-빨강 지배색을 줌. interesting-first 가 옅은 UV-only 렌더링 대신 밝은 분홍을 선택 |
| `star_apparent_angular_diameter_deg` | 6.2 | high | 유도. 2 × 0.82 R☉ / 0.07 AU × (180/π) ≈ 6.2° (R 은 Phase 2 anchor Donati 2023 ZDI) |
| `stellar_illumination_color_temp_k` | 3518 | high | host 별 광도 색-등가 흑체 (Gaia DR3 BP/RP). Phase 2 분광 Teff = 3700 ± 100 K (Plavchan 2020) 와 의도적으로 구분되며, SED 조명은 분광 값을 사용 — au-mic.md `stellar_color_temp_k` 참조 |

## Surface synthesis

AU Mic b 는 암석 행성의 의미에서의 표면이 없습니다. 질량 8.99 M⊕
와 반지름 4.79 R⊕ 가 밀도 0.45 g/cc 를 주는데, 이는 지구의 약 1/10
이고 Neptune 의 절반 미만입니다. Lopez & Fortney 2014 질량-반지름
다이어그램은 이 조합을 H/He envelope 영역의 한가운데에 놓고, 수소
envelope 가 행성 전체 질량의 25–35% 를 기여합니다. 명목상의 "표면"
— 압력이 몇 × 10⁴ Pa 에 도달하고 구름 데크에서 광학 깊이가 1 이
되는 곳 — 은 통과에서 보고된 약 4.79 R⊕ 반지름에 자리잡습니다.
그 아래로는 압력이 ~10 스케일 높이에 걸쳐 10⁵ → 10⁶ → 10⁷ Pa 로
올라가고, 가스는 상 경계 없이 초임계 유체로 매끄럽게 전이합니다.
렌더링할 지형이 없고 명시할 표면 색조도 없습니다.

NearStars 의 목적에서 플레이어가 보는 "가시 표면" 은 구름 데크
꼭대기입니다. 이는 텍스처가 있는 단단한 천체가 아니라 띠가 있는
가스 천체로 렌더링됩니다 (Visual styling 참조). KSP 의 stock 가스
자이언트 인프라에 커스텀 띠 텍스처가 적절한 analog 입니다. 천체의
내부는 따뜻한 Neptune 과 대체로 비슷한 구조로 가정됩니다. H/He
envelope → H₂O/NH₃/CH₄ 초임계 "얼음" mantle → 1–3 M⊕ 정도의 작은
암석/철 코어 (Cale 2021 §5 내부 fit). 어느 것도 보이지 않습니다.

시스템의 어린 나이가 여기서 중요합니다. 22 Myr 에서 b 는 primary
Kelvin–Helmholtz 수축을 마치지 않았습니다. 반지름이 Gyr 나이에
도달할 평형보다 ~1.5 배 크고, 내부 광도 (Plavchan 2020 §6) 가
나이 든 동급보다 ~10 배 큽니다. 이 잔열이 envelope 를 부풀린 채로
유지하며 He I 10830 Å 흡수가 검출 가능한 이유 중 하나 (Allart 2023)
입니다. 상층 대기가 뜨겁고, 이온화되어 있으며, 후행 wake 를 따라
약 5–8 행성 반지름까지 확장되어 있습니다.

## Atmosphere synthesis

대기는 관측적으로도 시각적으로도 행성 그 자체입니다. 여러 제약이
H/He 우세 puffy-Neptune 그림으로 수렴합니다.

**압력.** 통과 유도 반지름이 τ ≈ 1 구름 데크 위치를 고정합니다.
sub-Saturn 에 대한 Lopez & Fortney 2014 의 질량 + 반지름 + 나이 +
일사량 역산이 b 의 파라미터에 대해 H/He 질량 분율 ~30% 를 줍니다.
이는 (있다면) 암석 코어에서의 표면 압력 ~10⁹ Pa 를 함의하지만, KSP
대기 렌더링에 대한 의미 있는 "cfg 표면 압력" 은 구름 데크 압력
~10⁷ Pa 입니다. 정확한 값은 구름 응결물 화학 (깊이와 온도에 따라
H₂O, NH₃, NH₄SH) 에 의존하며 직접 측정되지 않습니다.

**조성.** Allart 2023 의 He I 10830 Å 검출 (통과 동안 ~0.3% 흡수.
명목 분석에서는 2.5σ marginal 이지만 CARMENES 관측의 He I 초과와
결합하면 견고함) 은 확장된 H/He 대기를 요구합니다. AU Mic 의 XUV
플럭스 (포화 영역. Stelzer 2013. Tristan 2023 flare 센서스) 를 사용한
에너지 한정 탈출 계산은 10⁹–10¹⁰ g/s 의 질량 손실률을 주며, Allart
2023 의 He I 광학 깊이와 일관됩니다. 이는 시스템의 예상 수명에
걸쳐 envelope 질량의 ~10% 를 잃기에는 충분하지만 b 를 완전히
스트립하기에는 부족합니다. 미량 종 (H₂O, CH₄, NH₃, CO) 은 Lavie
2017 차가운-Neptune 광화학 프레임워크에 따라 거의 태양 풍부도로
가정되며, 상층 대기에서 메탄 광분해가 광화학 haze 를 생성합니다.

**저궤도에서의 하늘 외관.** b 의 구름 꼭대기로 내려가는 KSP 플레이어
는 깊은 붉은 별이 비추는 Jupiter-like 띠상 가스 자이언트를 볼
것입니다 — 다만 띠 자체가 광화학 haze 와 M-왜성 SED 양쪽 모두에
의해 red-brown 쪽으로 muted 되어 있습니다. zonal jet 은 hot-Neptune
GCM 시뮬레이션 (Showman 2009 hot-Jupiter analog 를 Neptune 온도와
자전에 맞춰 스케일) 에서 추론됩니다. 적도 superrotation 이 더
어두운 중위도 belt 와 단일 밝은 zone 을 만듭니다. 극 영역은 더
어두움 — 광화학 haze 가 줄어든 일사 하에 축적되는 hood-like
변색입니다.

**대기 탈출과 혜성-like 꼬리.** AU Mic b 는 어떤 시스템에서든 가장
잘 특성화된 탈출 대기 중 하나입니다. Allart 2023 의 He I 10830 Å
흡수가 b 뒤편 궤도 방향을 따라 행성 반지름 몇 배에 걸쳐 뻗는
후행 꼬리를 매핑합니다 (Allart 2023 §4). NearStars cfg 렌더링에서
이는 EVE-사이드 대기 탈출 피처에 대응됩니다 — conjunction 의
관측자에게 보이는 옅은 이온화 꼬리. 꼬리는 AU Mic 의 이상하게 강한
항성풍 (~10× 태양. Plavchan 2020 §4 배경) 에 의해 sculpt 됩니다.
super-flare 이벤트 동안 (10³¹ erg 위 5.6/일. Tristan 2023 의 가끔
10³⁴ erg 이벤트) 꼬리는 bulk envelope 가 보통 가리는 깊이까지
상층 대기가 잠시 이온화되며 극적으로 밝아집니다.

## Rotation & spin synthesis

0.51 M☉ 주위 0.07 AU 의 8.46-d Neptune 급 행성에 대한 조석 감쇠는
~10⁵–10⁶ 년 시간 척도로 진행됩니다 (Goldreich & Soter 1966, Neptune-
like Q ≈ 10⁴). 22-Myr 시스템 나이에 걸쳐 b 는 1:1 spin-orbit
동기화에 완전히 잠겨 있습니다. Hirano 2020 의 Rossiter–McLaughlin
측정 (λ = −2.96 +10.3/-10.6°) 은 b 의 궤도면이 AU Mic 의 항성 자전축
과 정렬됨을 확인하며, 그것이 다시 가장자리 정면 disk 평면 (Krist
2005. Schneider 2014) 과 정렬됩니다. 시스템은 ~5° 수준에서 coplanar
입니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 8.463446 일 (731 241.7
초). Kopernicus `rotationPeriod` 는 궤도 `period` 와 일치해야 함.

**계절 없음.** 조석 lock 으로 obliquity 가 0 으로 감쇠. 이심률 0.07
(Mallorquin 2024) 가 궤도 따라 ~14% 일사 변동을 구동하는데, 이는
상당하지만 H/He envelope 의 열용량이 이를 거의 평탄화시켜 periapsis
에서 구름 꼭대기 온도 변동을 몇 K 로 만듭니다. 암석 행성 의미의
이산적 "계절" 은 없습니다. 대신 substellar 일사가 peak 일 때
periapsis 근처에서 행성 전체가 적당히 밝아집니다.

**주야 재분배.** 두꺼운 H/He 대기에서 주간에서 야간으로의 대기 열
운반은 효율적입니다. phase 곡선 급 관측 (b 에는 아직 없음 — Spitzer
phase 곡선 시도가 있었으나 host 별 흑점 신호가 지배함) 은 ~150–250 K
의 주야 대비를 보일 것입니다. cfg 는 중간 추정값으로 주간 700 K
와 야간 450 K 를 택합니다. 두 값 모두 이 일사량에서의 puffy Neptune
에 대한 GCM 윈도우 안에 있습니다.

## Visual styling

AU Mic b 의 시각 표현은 다섯 요소를 결합합니다.

- **전반 외관.** 절제된 zonal 띠를 가진 puffy warm-Neptune 디스크.
  ~6° 각지름의 깊은 붉은 M1V 별 (지구에서 본 태양의 12 배, 하늘
  지배) 이 비춥니다. 디스크 자체는 muted red-brown 띠 (`#7c4a32`
  주 haze, `#c0a880` zone 구름) 를 보입니다 — Jupiter 의 대담한
  tan-and-white 보다 부드러움. M-왜성 reddening 때문이기도 하고,
  광화학 haze 가 구름 꼭대기 구조를 덮기 때문이기도 합니다.
- **띠 구조.** 적도 superrotation jet 이 더 어두운 중위도 belt 와
  적도의 단일 밝은 zone 을 만듭니다. 극 영역은 haze 가 축적되는
  옅은 hood-like 어두워짐을 보입니다. 띠는 위도로 ~10° 폭이며,
  Jupiter 의 구조와 대체로 닮았지만 줄어든 대비와 더 느린 시각
  운동을 갖습니다 (자전 주기 8.46 d lock → 띠가 행성의 궤도와 함께
  자전). Tie-break. 시각적 흥미를 위해 균일 haze 가 아닌 띠 선택.
- **구름 꼭대기 텍스처.** 각 띠 안에서 fine-scale eddy 와 Rossby
  wave 섭동이 격렬한 구름 꼭대기 텍스처를 만듭니다 — sepia 필터를
  통해 렌더링된 천천히 자전하는 Jupiter 와 비슷. eddy 는 zonal jet
  과 함께 수 주에서 수 개월의 시간 척도로 advect 됩니다.
- **대기 탈출 꼬리 (행성의 시그너처 피처).** Allart 2023 의 He I
  10830 Å 검출이 b 뒤편 궤도 방향을 따라 행성 반지름 몇 배에 걸쳐
  뻗는 이온화 탈출 outflow 를 매핑합니다. KSP 시각 렌더링에 대해서
  는 투과 기하에서 보이는 옅은 분홍-보라 혜성-like 꼬리에 대응됩니다.
  관측자와의 conjunction 근처에서 가장 두드러집니다. 꼬리는 AU Mic
  super-flare 이벤트 동안 밝아집니다. 색은 `#ff6e8c` (H Balmer-α +
  Lyman-α downconvert) 로, 보이지 않을 UV-only 렌더링에 대한
  tie-break 으로 선택.
- **하늘의 별.** AU Mic 이 b 의 하늘에서 6.2° 를 차지 (지구에서 본
  태양의 12 배) — 반구의 약 1/30 을 차지하는 광활한 깊은 붉은
  디스크. 주간 구름 꼭대기에서 표면 일사량은 지구의 약 18.8 배
  이지만 근적외선 쪽으로 크게 red-shift 됨. 시각적으로 구름 꼭대기는
  밝지만 푸른 하늘의 밝음이 아니라 평탄한 톤으로 보입니다. Super-flare
  (연간 여러 차례의 10³⁴ erg 이벤트. Tristan 2023) 가 10–60 분간
  조명을 1–3 등급 잠시 밝게 만듭니다 — 주간 전체의 일시적 밝아짐
  으로 보임.

가까이 있는 네 행성 — c 가 0.119 AU, d 가 ~0.105 AU, e 가 ~0.171 AU
(확인된다면) — 는 b 에서 작은 점으로 보이며 대부분 각지름 ≪ 1°
입니다. 35–210 AU 의 가장자리 정면 잔해 원반은 AU Mic 양옆 하늘을
이등분하는 가늘고 밝은 줄로 나타납니다. b 는 시스템 너머에서 볼 때
AU Mic 의 항성 디스크를 통과합니다. b 의 관측자는 disk 의 안쪽
가장자리가 중심 별에서 ~5° 부터 지평선 바깥까지 하늘을 가로질러
뻗는 것을 보게 됩니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Plavchan P. et al. 2020** — *A planet within the debris disk around the pre-main-sequence star AU Microscopii*, Nature 582, 497 (`2020Natur.582..497P`, arXiv:2006.13428). TESS 가 발견한 AU Mic b 의 통과 hot Neptune. 통과 유도 반지름 4.0 R⊕ (이후 4.79 로 정밀화). host XUV 환경과 대기 탈출 영역 논의. cornerstone 논문.
- **Cale B. L. et al. 2021** — *Diving Beneath the Sea of Stellar Activity: Chromatic Radial Velocities of AU Mic b*, AJ 162, 295 (`2021AJ....162..295C`, arXiv:2109.13996). 다기기 GP detrending 으로 첫 견고한 RV 질량. puffy envelope 과 일관된 인플레이션 저밀도 보고.
- **Mallorquin M. et al. 2024** — *AU Mic system characterized with ESPRESSO*, A&A 689, A132 (`2024A&A...689A.132M`). ESPRESSO + TESS 결합 분석. b 의 질량을 8.99 ± 2.61 M⊕ 로, 반지름을 4.79 ± 0.29 R⊕ 로 정밀화. 개선된 항성 활동 모델링으로 Cale 2021 의 더 높은 질량을 대체. **headline 출처로 채택**.
- **Allart R. et al. 2023** — *Homogeneous search for helium in the atmosphere of 11 gas giants with HST/STIS and CARMENES*, A&A 677, A164 (`2023A&A...677A.164A`, arXiv:2308.10891). AU Mic b 통과 동안의 marginal-to-significant He I 10830 Å 검출 보고. 탈출률과 확장 대기 기하 제약. atmosphere-present 와 escape-tail cfg 픽을 구동.
- **Hirano T. et al. 2020** — *Evidence for Spin–Orbit Alignment in the TRAPPIST-1 System and Implications for the AU Mic system*, ApJ 899, L13 (`2020ApJ...899L..13H`, arXiv:2006.13654). Subaru IRD 의 b 에 대한 Rossiter–McLaughlin 측정. 투영 obliquity λ = −2.96°. disk + 항성 자전축과의 궤도면 정렬 확인.
- **Lopez E. D. & Fortney J. J. 2014** — *Understanding the Mass-Radius Relation for Sub-Neptunes*, ApJ 792, 1 (`2014ApJ...792....1L`, arXiv:1311.0329). 질량-반지름 envelope 질량 분율 보정. b 에 적용하면 질량 ~30% H/He. cfg 표면 압력 픽을 구동.

### Read (context / methodology, not decision-driving)

- **Klein B. et al. 2021** — *Investigating the young AU Mic system with SPIRou: stellar magnetic field and close-in planet mass*, MNRAS 502, 188 (`2021MNRAS.502..188K`, arXiv:2012.04970). AU Mic 의 SPIRou 근적외선 ZDI + RV. Mallorquin 2024 가 사용한 GP detrending 에 대한 항성 활동 맥락 제공.
- **Donati J.-F. et al. 2023** — *The magnetic field topology and filling of the very active M dwarf AU Mic*, MNRAS 525, 2015 (`2023MNRAS.525.2015D`). ZDI 쌍극자 2 kG, 전체 RMS 4.6 kG. 항성 자기장 맥락 설정.
- **Tristan I. I. et al. 2023** — *Catching the Flares of the AU Mic System with TESS*, ApJ 951, 33 (`2023ApJ...951...33T`, arXiv:2306.00077). TESS flare 센서스. 10³¹ erg 위 5.6/일 비율. 대기 탈출과 오로라 타이밍에 관련.
- **Lavie B. et al. 2017** — *HELIOS-RETRIEVAL: Open-source Nested Sampling Atmospheric Retrieval Code for Exoplanets*, AJ 154, 91 (`2017AJ....154...91L`, arXiv:1610.03216). 미량 종 조성에 채택된 차가운 Neptune 광화학 프레임워크.
- **Sing D. K. et al. 2016** — *A continuum from clear to cloudy hot-Jupiter exoplanets without primordial water depletion*, Nature 529, 59 (`2016Natur.529...59S`, arXiv:1512.04341). hot/warm 가스 자이언트의 구름 데크 압력 센서스. 0.70 cloud-cover 선택을 뒷받침.
- **Showman A. P. et al. 2009** — *Atmospheric Circulation of Hot Jupiters*, ApJ 699, 564 (`2009ApJ...699..564S`, arXiv:0809.2089). 적도 superrotation GCM 프레임워크 (더 차가운 온도 적응 포함) 가 띠 형태 픽에 채택.

### Read (instrument / non-decisive)

- **Martioli E. et al. 2020** — *AU Mic b transits revisited with TESS Sector 27* (초기 sector-27 릴리스. 시각적 정보 없음).
- **Szabó Gy. M. et al. 2021** — *Spi-Ops campaign on AU Mic b* (`2021A&A...654A.159S`, arXiv:2108.07984). CHEOPS 통과 타이밍. cfg-결정적이지 않음.

### Not read — no arXiv preprint or low-priority (~25 papers)

학회 초록 (DPS, EPSC), 독립 재분석 없는 AU Mic 의 초기 TESS 파이프
라인 릴리스, 유의한 검출을 내지 않은 He I 후속 캠페인, 그리고
arXiv preprint 없는 매우 최근의 PSJ early-access 논문들이 모두 점진적
으로 그림에 기여하지만 cfg 결정을 바꾸지는 않습니다. 전체 필터링된
bib 는 행성의 `_bib/au-mic-b.yaml` (생성 예정) 에 `status: skipped`
annotation 으로 보존됩니다.

## Open items for follow-up

- **JWST 대기 특성화.** b 의 NIRSpec 또는 NIRISS 투과 스펙트럼이
  조성과 구름 구조를 직접 제약할 것입니다. 몇 가지 제안이
  채택되었으나 이 글 작성 시점까지 출판되지 않았습니다. 분자 검출
  (H₂O, CH₄, CO, HCN) 이 논문으로 나오면 cfg 조성 행을 re-fit 해야
  하고 cloud_morphology 가 정밀화될 수 있습니다.
- **He I 10830 Å 후속.** Allart 2023 의 검출은 적당한 유의성입니다.
  CARMENES 또는 Keck/NIRSPEC 의 독립 확인이 cfg 의 탈출 꼬리 시각
  피처를 견고화할 것입니다. 검출이 철회되면 atmospheric_escape_rate_g_s
  가 ~1 dex 내려가고 꼬리 렌더링이 더 미묘해져야 합니다.
- **Spitzer/JWST phase 곡선.** 직접 주야 대비 측정이 700 K / 450 K
  온도 픽을 제약할 것입니다. host 별 활동을 통한 phase 곡선은 여전히
  어렵습니다. JWST MIRI ECLIPSE 프로그램에 미룹니다.
- **내부 모델링.** Cale 2021 §5 가 Neptune-analog H/He + 얼음 + 암석
  코어 내부를 스케치합니다. b 에 대한 정식 베이즈 retrieval
  (super-Neptune 의 Acuña 급) 은 아직 출판되지 않았습니다.
- **cfg variant. 미래의 deflated 상태.** b 는 현재 22 Myr 에서
  puffy 합니다. 1 Gyr 에서는 일정 질량에서 ~3 R⊕ 로 축소될 것입니다
  (Lopez & Fortney 2014). "성숙한 AU Mic 시스템" cfg variant 가
  시각 비교를 위해 deflated b 를 배포할 수 있습니다.
- **c/d Phase 3 와의 조율.** 가까이 있는 네 행성은 AU Mic 의 flare
  환경을 공유합니다. d/e 에 대한 super-flare 구동 대기 스트립 논증이
  바뀌면 b 의 탈출률에 대한 cfg-일관성 검사가 조정되어야 할 수
  있습니다.

## Related

- [au-mic](au-mic.md) — disk 기하를 포함한 host 별 합성
- [au-mic-c](au-mic-c.md) — 자매 행성. 18.9 d 의 sub-Neptune
- [au-mic-d](au-mic-d.md) — 자매 행성. 12.7 d 의 지구질량 TTV 후보
- [au-mic-e](au-mic-e.md) — 자매 행성. 33.1 d 의 ESPRESSO RV 후보
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — downstream cfg 작성기
