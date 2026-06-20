<!-- τ Ceti f Phase 3 합성. cfg-ready 결정과 근거 -->
# τ Ceti f — Phase 3 Synthesis

τ Ceti f 는 metal-poor G8V τ Ceti 주위를 636 일 주기로 1.334 AU 에서
도는 3.93 M⊕ (M sin i) RV 후보 행성입니다 (Feng 2017,
`2017AJ....154..135F`). 현재 `db/systems/tau_cet.json` 에 들어 있는 세
행성 중 가장 바깥쪽이며 (f, g, h 모두 Feng 2017 출처. e 는 호스트
Phase 3 합성에서 큐레이션 갭으로 기록), 호스트 광도 0.488 L☉ 기준
조사량은 0.27 S⊕ 로 — G8V 의 보수적 거주가능영역 바깥 경계
(Kopparapu 2014 maximum-greenhouse 한계 ≈ 0.36 S⊕) **바깥**입니다.
f 의 평형 온도는 202 K (A=0) 또는 184 K (A=0.3) 이며, 이 호스트에서는
얇은 2차 대기로도 표면을 물 어는점 위로 데우지 못합니다. 행성은
NEA 에서 **disputed** (`pl_controv_flag = 1`) 로 표시됩니다 — RV 단독,
transit 없음, 직접 영상 없음, JWST 후속 관측 없음. Feng 2018
(`2018A&A...613A..76F`) 가 시스템을 재검토했을 때 636 일 신호 자체는
안정적이었지만, 일부 후속 분석 (Figueira 2025, 그리고 그 이전 Tuomi
2013 의 5-행성 주장 철회 이력) 은 SNR 을 마지널한 수준으로 봅니다.

**NearStars 시나리오 선택. 매장 가능 해양 위에 전구적 H₂O 얼음 외피를
덮은 차갑고 얇은 대기의 snowball super-Earth, 탈가스 잔존물인 희박한
N₂ + 미량 CO₂ 대기, 조용한 G8V 조명 아래 옅은 크림-그레이 표면
팔레트로 렌더링.** 직접 측정되지 않은 Decisions 항목에 대해서는 cfg 가
보수적입니다 — 압력, 조성, 표면 형태는 측정 제약이 아니라 조용한
G 왜성 주위 outer-HZ super-Earth 의 이론적 기본값입니다. 맨 암석
무대기 대안은 Open item 의 cfg variant 로 보존됩니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | P=636 d 는 0.78 M☉ 호스트에서의 조석 고정 시간 척도보다 훨씬 길며, 이 간격에서는 spin damping 이 작동하지 않습니다. Vinson 2017 |
| `obliquity_deg` | 23 | low | Tie-break. 비동기 super-Earth 의 기본값으로 지구형 obliquity 채택 (관측 제약 없음) |
| `eccentricity` | 0.16 | medium | Feng 2017 RV fit (낮은 신호 SNR 때문에 불확실. g/h 의 secular 강제와 일관) |
| `argument_of_periastron_deg` | 119.75 | medium | Feng 2017 RV fit |
| `sidereal_period_days` | 636.13 | high | Feng 2017 RV — 불확실성 ±11.7 d |
| `semi_major_axis_au` | 1.334 | high | Feng 2017 (호스트 질량 + Kepler 3 법칙에서 ±0.017) |
| `inclination_deg` | 35 | low | Tie-break. τ Ceti 잔해 원반 경사를 채택 (Lawler et al. 2014, MacGregor et al. 2016 이 채택. 공면 가정) — Feng 2017 §5.2 도 이 값을 기본으로 사용 |
| `mass_mearth` | 3.93 (M sin i. sin i ≈ 0.7 가정 시 실제 질량 ≳ 5 M⊕) | medium | Feng 2017 RV. RV 진폭 fit 에서 ±1.05 |
| `radius_rearth` | 1.81 | low | Feng 2017 이 mass–radius 관계 (Weiss & Marcy 2014 sub-Neptune) 로 카탈로그한 반지름. 직접 측정 아님 |
| `surface_gravity_g_earth` | 1.20 | medium | derived = 3.93 / 1.81² |
| `density_g_cc` | 3.66 | low | Msini 와 가정 R 에서 derived. 실제 질량이 같은 R 에서 5 M⊕ 라면 ρ 는 4.66 g/cc 로 올라가 행성이 더 지구형이 됩니다 |
| `water_mass_fraction` | 0.05–0.20 | low | 이론적. 바깥쪽 시스템에서 sub-Neptune 반지름 super-Earth 라면 iceline 너머 형성과 일관되게 휘발성 envelope 을 가질 가능성이 큼 |
| `insolation_s_earth` | 0.274 | high | derived L_bol/a²: 0.488 L☉ (Teixeira 2009, recommended) / (1.334 AU)² |
| `equilibrium_temp_k` (A=0) | 202 | high | derived 278 × (L/a²)^0.25 |
| `equilibrium_temp_k` (A=0.3) | 184 | high | 지구형 albedo 로 derived |
| `bond_albedo` | 0.50 | medium | 얇은 N₂/CO₂ 아래 얼음/눈 표면이 우세. Snowball-Earth bond albedo 와 유사 (Pierrehumbert 2011) |
| `surface_temp_global_mean_k` | 175 | low | Wordsworth 2015 의 얇은 대기 outer-HZ 스케일링. 모든 곳에서 H₂O 어는점 아래 |
| `surface_temp_substellar_k` | 195 | low | 비동기 느린 자전자 — dayside 가 다주 시간 척도로 순환하므로 substellar 가열은 일시적 |
| `surface_temp_nightside_k` | 155 | low | nightside 가 여러 날에 걸칠 경우 대략 N₂ frost point |
| `atmosphere_present` | true (얇은 잔존) | medium | 호스트의 basal FUV / 정적 XUV 환경 (Schmitt 1985, Judge 2004) 은 XUV 구동 탈출이 미미함을 의미. 탈가스로 누적된 N₂ + CO₂ 는 7 Gyr 동안 살아남을 것 |
| `atmosphere_surface_pressure_pa` | 10 000 | low | outer-HZ super-Earth 의 canonical "얇은 2차 대기" 로 0.1 bar 채택 (Wordsworth 2015). 측정 아님 |
| `atmosphere_composition` | N₂ ~80%, CO₂ ~10–20%, 미량 H₂O, Ar | low | Wordsworth 2015 cold-trap 논리. H₂O 대부분 동결, N₂ 는 후기 탈가스로 누적, CO₂ 분압은 ~190 K 의 frost-point 로 상한 (Bolmont 2018 review 프레임워크) |
| `atmosphere_scale_height_km` | 3.9 | medium | derived. kT/μg with T≈180 K, μ=32 (N₂/CO₂ 혼합), g=11.8 m/s² |
| `atmosphere_tint_rgb_hex` | `#7a7068` (아주 얇은 대기, 더 깨끗한 G8V SED 아래 희미한 Rayleigh) | low | Tie-break. 0.1 bar 는 가시 Rayleigh 임계값 아래. metal-poor 의 더 깨끗-푸른 호스트 SED 는 잔존 산란을 태양 주변보다 약간 더 차가운 톤으로 만듭니다 |
| `cloud_cover_fraction` | 0.20 | low | 차가운 tropopause 의 산발적 CO₂ 얼음 권운. 어는점 아래라 H₂O 구름 형성은 억제 |
| `cloud_tint_rgb_hex` | `#e8e0d0` (옅은 G8V 빛 아래 깨끗한 얼음 권운) | low | Tie-break. M 왜성 스타일 따뜻한 크림 대신 깨끗한 거의 흰색으로 — 호스트 SED 가 강하게 적색 편이된 것이 아니기 때문 |
| `ocean_present` | sub-glacial (가능) | low | 이론적. 수질량비 5–20% 가 방사성 + 미세 조석 가열과 결합하면 매장 액체층을 지지할 수 있음 (행성 규모의 Europa analog) |
| `ocean_extent_substellar_radius_deg` | 0 | high | 표면 액체 없음 — 전구적 빙하 표면 |
| `ocean_tint_rgb_hex` | n/a | high | 표면 해양 없음 |
| `surface_ice_caps` | 전구적 H₂O 얼음 외피. cold-trap 영역과 terminator/nightside 근처에 CO₂ 얼음 서리 | medium | Pierrehumbert 2011 snowball 템플릿 + Wordsworth 2015 얇은 대기 outer-HZ |
| `surface_tint_rgb_hex_primary` | `#dcd4c8` (G8V 빛 아래 깨끗한 크림-흰 H₂O 눈) | medium | 조용한 G8V 조명 아래 눈 albedo 0.6–0.8 — 옅은 크림-흰, M 왜성이 비추는 TRAPPIST analog 보다 살짝 더 깨끗 |
| `surface_tint_rgb_hex_accent` | `#a89a88` (충돌구 림과 능선 정상에서 노출된 풍화 기반암) | low | Tie-break. 두꺼운 전구 얼음 아래 기반암 노출은 제한적 — 액센트 전용 |
| `surface_morphology` | 압력 능선, 균열, 조석 응력 지역 근처에 cryovolcanic 분출 가능성을 가진 전구적 빙하 얼음 | low | Pierrehumbert 2011 snowball 얼음 동역학 템플릿. 관측 제약 없음 |
| `magnetic_field_present` | true (적당함) | low | super-Earth 질량 + 비조석 고정 느린 자전이 지속 dynamo 를 지지할 수 있음. 직접 제약 없음 |
| `magnetic_field_strength_microtesla_equator` | 25 | low | Tie-break. 다주 주기로 자전하는 4–5 M⊕ 암석체에 RM22 (Rodríguez-Mozos & Moya 2022, `2203.01065`) 적용 시 ~0.5× 지구 |
| `tidal_heating_w_m2` | 0.001–0.01 | medium | e = 0.16 은 무시할 수 없지만 a = 1.334 AU 는 멉니다. 통합 조석 플럭스는 적당함 |
| `induction_heating_w_m2` | < 0.001 | medium | 이 거리에서 의미 있는 induction 가열을 끌어내기에 호스트 항성 자기장이 너무 약함 (Boro Saikia 2018 ZDI) |
| `radiogenic_heat_w_m2` | 0.04 | low | 지구형 BSE(bulk-silicate-Earth) 방사성 열류속(현재값 ~0.04 W/m²)을 질량으로 스케일. 방법은 Wang et al. 2020 (`2020A&A...644A..19W`)의 외계행성 방사성 열 프레임워크를 따름. 다만 Eu→Th/U 호스트 원소비 보정은 호스트별 원소비를 큐레이션하지 않아 적용하지 않았고, 대신 지구형 원소비를 가정함(metal-poor 호스트라면 ²³²Th/²³⁸U 예산이 더 낮아지겠지만 여기서는 정량화하지 않음) |
| `aurora_present` | true (희미함) | low | 적당한 자기장 + 얇은 대기 → 확산 오로라 가능. 밝은 오로라에는 호스트 XUV 가 너무 약함 |
| `aurora_color_primary_hex` | `#4DFF4D` | low | Tie-break. 광분해로 미량 O₂ 가 있을 경우 [OI] 557.7 nm 녹색. 그렇지 않으면 N₂ Vegard-Kaplan 청록 |
| `aurora_intensity_kR_typical` | 1 | low | 조용한 호스트 — f 거리에서의 양성자 플럭스는 지구의 그것보다 한참 아래라서 오로라 강도는 지구 전형값 10 kR 보다 약 10× 약함 |
| `star_apparent_angular_diameter_deg` | 0.317 | high | derived. 2 × R★ / a = 2 × 0.793 R☉ / 1.334 AU × (180/π) — 지구에서 본 태양의 60% |
| `stellar_illumination_color_temp_k` | 5370 | high | 호스트 Teff (Pavlenko 2012) |

## Surface synthesis

τ Ceti f 는 보수적 거주가능영역 바깥 경계 한참 바깥에 놓입니다.
Kopparapu 2014 의 maximum-greenhouse outer 한계는 Teff = 5370 K G8V
기준 runaway-CO₂-cloud 경계를 S ≈ 0.36 S⊕ 에 두는데, 0.274 S⊕ 의 f 는
명확히 그 너머입니다. 활성 온실효과가 없으면 행성의 평형 온도는
albedo 0 에서 202 K, 지구형 0.3 bond albedo 아래에서는 184 K — 모두
편안하게 물 어는점 아래입니다. Wordsworth 2015 는 조용한 G 왜성
주위의 차가운 outer-HZ super-Earth 에 얹힌 얇은 2차 대기 (0.01–0.1
bar) 는 정상상태에서 표면 액체 수를 유지할 수 없음을 보입니다 —
nightside 나 극지방에서 CO₂ 가 cold-trap 응결되며 대기압을 상한
지우고 온실 구동력을 제거합니다.

cfg 는 **snowball super-Earth** 표면 형태를 채택합니다. 수 킬로미터
두께의 전구적 H₂O 얼음 외피가 e = 0.16 의 적당한 조석 응력으로
국지적으로 갈라지고, 가열이 큰 영역 근처에서는 cryovolcanic 재포장도
가능합니다. 압력 능선, 다각형 균열 패턴, 승화 cold-trap 의 희미한
CO₂ 서리가 지배적 지형 피처입니다. 표면은 TRAPPIST-1 e/f 의 안구
기하 (eyeball) 가 *아닙니다*. f 는 조석 고정되지 않으며 (P = 636 d 는
0.78 M☉ 호스트 1.33 AU 에서의 조석 고정 시간 척도보다 한참 길어),
다주 시간 척도로 dayside 가 회전함에 따라 substellar 가열은
일시적입니다. 따라서 얼음 덮개는 고정 substellar 핫스팟에 집중되지
않고 거의 균일합니다.

**색 선택 — G8V 빛 아래 깨끗한 크림-흰.** 호스트는 M 왜성 적색도
아니고 태양 노랑도 아닌, 살짝 더 차가운 G8V 에 metal-poor SED 가
미세하게 더 깨끗-푸른 연속체를 더한 것입니다 (호스트 Phase 3
합성의 Visual styling 참조). 이 조명 아래 눈은 옅은 크림-흰
(`#dcd4c8`) 으로 보이며, 같은 albedo 가 2566 K TRAPPIST-1 아래에서
만들었을 따뜻한 크림 `#d8d0c4` 와 대조적입니다. 충돌구 림, terminator
능선, cryovolcanic 흐름 가장자리에서 가끔 노출되는 기반암을 위한
액센트 `#a89a88` 는 metal-poor 원시 규산염 먼지와 일관된 풍화된
그레이-브라운입니다.

**기반암 노출은 제한적.** 수질량비 5–20% (Msini 추정에서 얻은
~3.7 g/cc 의 sub-Neptune 계열 밀도와 일관) 이면 표면 대부분이 얼음
아래 묻힙니다. M-R 관계 반지름 자체가 low-confidence 이며 — 실제
질량이 더 크면 (sin i ≲ 0.7, 실제 M ≈ 5–6 M⊕) f 는 얇은 얼음 위
밀도 높은 암석 세계일 수 있지만 — 휘발성 풍부 envelope 해석이
바깥쪽 시스템 super-Earth 에 대한 sub-Neptune 문헌과 부합합니다
(Owen & Wu 2017).

**sub-glacial 해양 가능성.** 매장 액체 수 층은 가능하지만 필수는
아닙니다. 두꺼운 단열 얼음 외피 없이 방사성 가열만으로는 (지구형
0.04 W/m²) 전구 지하 해양을 유지하기에 불충분합니다. e = 0.16 와
a = 1.33 AU 에서의 조석 가열은 작지만 0 은 아닙니다 (Bolmont 2020
스타일 스케일링에서 ~0.01 W/m² 추정). 두 열원이 결합하고 얼음 외피가
두껍다면 (≳ 50 km) Europa-analog 매장층이 가능합니다. low-confidence
피처로 로깅하고 Open item 으로 남깁니다.

## Atmosphere synthesis

f 대기에 대한 관측은 없습니다. JWST 는 행성을 타겟하지 않았고
(지구에서 검출 가능한 transit 없음. HST/Hubble RV 후속도 비생산적),
따라서 대기 합성은 (a) 조용한 호스트 XUV 환경과 (b) outer-HZ 얇은
2차 대기 문헌에 정박해 전적으로 이론적입니다.

**압력 선택 — 0.1 bar.** Wordsworth 2015 의 조용한 G/K 호스트
주위 super-Earth 프레임워크는, τ Ceti 처럼 log L_X ≤ 26.5 인 호스트
에서는 hydrodynamic 손실 없이 thermal-Jeans 탈출만으로도 얇은 2차
대기가 다-Gyr 시간 척도로 보존됨을 예측합니다. cold-trap 논리는
CO₂ 분압을 가장 차가운 표면 온도의 승화 평형 (~190 K → CO₂ 분압
≲ 10 mbar) 으로 상한 짓고, N₂ 는 80 K 이상에서 응결 트랩이 없으므로
탈가스된 N₂ 가 누적됩니다. 총 압력 0.1 bar 는 이 영역의 canonical
기본값입니다. 0.01 bar (Mars-thin) 와 1 bar (Earth-thin) 모두 미제약
윈도우 안에서 방어 가능한 대안입니다.

**조성.** N₂ 우세 (~80%) 에 지구 대비 상승한 CO₂ (~10–20%) — cold-trap
이 대기 질량 대비 CO₂ 분압을 따뜻한 지구보다 높게 허용합니다. 권운
높이 근처에만 미량 H₂O 증기. 대부분의 물은 표면에 동결. 원시 탈가스
에서 미량 Ar. metal-poor 호스트는 원시 성운 얼음이 철로 덜 물들었음을
뜻하지만, 이는 조성에 대한 2차 효과입니다.

**하늘 모습.** 0.1 bar 대기는 궤도에서 거의 보이지 않으며 — 림 안개는
희미하고, 경계에서 두께 약 10 km 정도입니다. 표면에서는 하늘이
호스트 SED 때문에 지구보다 살짝 더 차갑게 이동한 옅은 워시드-아웃
청-백 (`#7a7068`) 입니다. 한낮은 어둑함 — 조명은 지구 태양 조사량의
~27% 로, 두껍게 흐린 지구의 하루와 거의 같습니다. 호스트 별은
f 의 하늘에서 0.317° 를 채우며 (지구에서 본 태양의 60% 정도)
작은 옅은 노랑 원반으로 보입니다. TRAPPIST-1 e 의 거주자가 볼 적-주황
태양보다 한참 덜 위압적입니다.

**flare 변조 없음.** inner-edge M 왜성 HZ 행성들과 달리 f 는 XUV
flare 이벤트를 보지 않습니다. 호스트의 log R'HK = −4.95 는 지금까지
서베이된 G 왜성 중 가장 비활성인 부류에 들고, 따라서 대기 화학은
다-Myr 시간 척도로 안정적이며 에피소드 광화학 충격이 없습니다.

## Rotation & spin synthesis

τ Ceti f 는 **조석 고정되지 않습니다**. 0.78 M☉ 호스트 주위
P = 636 d, a = 1.334 AU 에서 조석 고정 시간 척도 (Vinson 2017 공식,
τ_lock ∝ a^6 / (M_p × Q × R_p^5)) 는 시스템 나이 7 Gyr 보다 편안하게
길며 — spin damping 이 작동할 시간이 없었습니다. 행성은 미지의
속도로 자전하며 cfg 는 지구형 ~24 h 일을 기본값으로 둡니다. 다주
자전 주기 (outer-HZ super-Earth 의 전형적 원시 spin 주기, Heller
2011) 도 가능하지만 관측으로 제약할 수 없습니다.

이심률 e = 0.16 은, 만약 행성이 초기 진화에서 3:2 spin-orbit
공명에 포획되었다면 그 공명이 안정했을 만큼 충분히 높습니다.
관측 증거 없이는 cfg 가 더 단순한 비동기 빠른 자전자 가정을
채택합니다.

**KSP 구현 노트.** 조석 고정이 없으므로 `rotationPeriod` 는
`period` 에 일치할 필요가 없습니다. 게임플레이상의 이유가 다른
값을 선호하지 않는 한 기본값 24 시간 (86 400 s) 으로 둡니다.

**Obliquity.** Tie-break 기본값으로 지구형 23° 채택 — 제약 없음,
선호 방향 없음. 약한 계절 강제 (이심 궤도에 걸쳐 조사량이 ~±9%
변동) 만이 유일한 "계절" 사이클이며, S = 0.27 S⊕ 에서 표면 온도
응답은 둔합니다 (≲ 4 K).

**자기 dynamo 기대치.** 다주 자전을 가진 4–5 M⊕ 암석체는 적당한
dynamo 를 지지할 수 있습니다. RM22 스케일링은 이 파라미터 조합에서
표면 자기장 강도를 ~25 μT (~0.5× 지구) 로 줍니다. 직접 제약 없음.
시각 cfg 의 중심 요소 아님.

## Visual styling

- **전구 외관.** 빙하 흐름, 다각형 균열, 충돌구로부터의 은은한 표면
  텍스처를 가진 옅은 크림-흰 snowball. 대기는 10–15 km 두께의
  희미한 청-그레이 림 안개로 거의 보이지 않습니다. 시각 캐릭터는
  살짝 더 큰 Europa 나 외태양계 Pluto-Charon variant 에 가장 가깝
  습니다 — 지형 디테일을 가진 얼음 우세 세계.
- **Dayside 디테일.** 전구 얼음 외피의 압력 능선과 균열이 PQS
  해상도에서 보이고, M 왜성 가열이 조용한 G8V 조명으로 대체되는
  곳은 따뜻한 크림 (깨끗한 거의 흰색, 황토 편이가 덜함). 조석/
  방사성 플럭스가 높은 영역 근처에 cryovolcanic 분출 가능 (희박,
  표면 ≪ 1%).
- **Terminator 밴드.** 얼음과 그림자가 뚜렷이 대비됩니다 — cryovolcanic
  봉우리, 충돌구 림, 압력 능선에서 긴 그림자. 얇은 대기는 최소
  산란만 일으켜 terminator 전이는 지구의 그것보다 더 또렷합니다.
- **Nightside 외관.** 어두움. 별빛이 얼음에 반사되는 아주 희미한
  cyan-white 광택. KSP nightside 환경광 ≈ dayside 의 0.5%.
- **대기 안개.** 희미한 옅은 청-그레이 (`#7a7068`) 림 글로우 ~10 km
  두께 — 지구의 푸른 림보다 훨씬 희미. 대기 질량이 지구의 1% 이고
  호스트 SED 가 태양보다 청색 플럭스가 적기 때문.
- **희미한 오로라.** 드문 호스트 자기장 교란 이벤트에 ~1 kR 의
  녹색 톤이 살짝 들어간 확산 극지 오로라 가능. 정의적 시각 피처로
  애니메이션 처리하지 않음.
- **하늘의 별.** τ Ceti 는 f 표면에서 0.317° 를 채웁니다 — 지구에서
  본 태양의 60% 의 작은 옅은 노랑 원반. 표면 조명은 두껍게 흐린
  지구의 하루나 맑은 날의 황혼과 비슷하며, 스펙트럼 피크는 태양
  보다 살짝 더 차갑게 이동.
- **하늘의 자매 행성들.** g (안쪽 다음) 는 합 위치에서 각지름 ~0.04°
  (밝은 "샛별" 점으로 보임). h 도 ~0.04°. 긴 궤도 주기 때문에
  합 이벤트는 드뭅니다. ≥ 6 AU 의 차가운 잔해 원반은 f 궤도
  *바깥*에 있고 하늘에서 희미한 호박-그레이 띠로 보입니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Feng F. et al. 2017** — *Color difference makes a difference:
  four planet candidates around τ Ceti*, AJ 154, 135
  (`2017AJ....154..135F`, arXiv:1708.02051). 발견 + f 궤도
  (P = 636.13 ± 11.7 d), 질량 (Msini = 3.93 ± 1.05 M⊕), 이심률
  (0.16), 호스트 질량 (0.783 ± 0.012 M☉) 의 최선 제약. 모든 궤도
  및 물리 Decisions 행을 정박.
- **Feng F. et al. 2018** — *Detection limits on τ Ceti's planet
  system from HARPS RV*, A&A 613, A76 (`2018A&A...613A..76F`,
  arXiv:1801.05415). 확장된 HARPS 데이터셋으로 4-행성 시스템 재검토.
  636 d 신호 안정적. NEA 의 controversial 플래그는 지속되는
  amplitude-to-noise 우려를 반영.
- **Wordsworth & Pierrehumbert 2015** (general atmospheric-escape
  argument) — f 에 채택한 0.1 bar N₂ / 미량 CO₂ 2차 대기의 일반
  대기-유지 참조로 사용. 구체적 제목은 핀하지 않음.
- **Kopparapu R. K. et al. 2014** — *Habitable zones around
  main-sequence stars*. Teff = 5344 K G8V 의 outer-edge
  maximum-greenhouse 한계는 S ≈ 0.36 S⊕. 0.26 S⊕ 의 f 는 명확히
  바깥.
- **Pierrehumbert R. T. 2011** — *Hydrology, climate and physical
  state of cold outer-HZ super-Earths*. snowball 얼음 동역학
  템플릿. 전구 얼음 덮개의 bond albedo ~0.5.

### Read (context / methodology, not directly decision-driving)

- **MacGregor M. A. et al. 2016** — *τ Ceti debris disk ALMA
  imaging*, ApJ 828, 113 (`2016ApJ...828..113M`). 원반면 경사
  ~35°, Lawler et al. 2014 (Herschel) 에서 가져온 값 — f 궤도면
  기본값으로 채택 (Feng 2017 도 공면 가정).
- **Tuomi M. et al. 2013** — *Signals embedded in the radial
  velocity noise: τ Ceti 5-planet claim*, A&A 551, A79
  (`2013A&A...551A..79T`). 초기 5-행성 검출. Feng 2017 가 4개
  (e/f/g/h) 를 유지하고 1개 (구 라벨링의 b) 를 떨어뜨림. controversial
  플래그 이력 이해에 유용.
- **Owen J. E. & Wu Y. 2017** — *The evaporation valley*. sub-
  Neptune envelope 유지 vs. 질량 프레임워크 — f 의 sub-Earth bulk
  density 에 대한 휘발성 풍부 해석을 지지.
- **Vinson A. M. & Hansen B. M. S. 2017** — *Spin-orbit dynamics
  of habitable-zone planets*. 3:2 vs. 1:1 포획 확률. P = 636 d 의
  f 는 비동기 자전자 영역.
- **Bolmont E. et al. 2020** — *Tidal evolution of compact
  planetary systems*. Maxwell-viscoelastic 조석 가열. f 의 적당한
  e = 0.16 가 1.33 AU 에서 ~0.01 W/m² 추정 플럭스.

### Read (instrument / non-cfg-decisive)

- **Pavlenko Y. V. et al. 2012** — 호스트 별 [Fe/H] = −0.55,
  log R'HK = −4.95, Teff = 5344 K. 세 행성 모두의 호스트 맥락 견인.
- **Schmitt J. H. M. M. et al. 1985** — 호스트 X 선
  log L_X ≤ 26.5 cgs. "XUV 구동 탈출 없음" 프레이밍 견인.

### Not read — no arXiv preprint or low-priority (~15 papers)

- **Tuomi 2013 erratum** — Tuomi 2014 (`2014MNRAS.441.1545T`) 가
  잡음 모델 정제. Feng 2017 로 대체.
- **SETI/레이저-탐색/technosignature 논문 다수** — 행성에 대한
  cfg 관련성 없음.
- **천체생물학 추측 리뷰** — 일반적으로 f 를 "거주가능" 보다는
  "marginal" 범주에 두며 개별적으로 cfg 결정적이지 않음.

## Open items for follow-up

- **Controversial 플래그 (`pl_controv_flag = 1`).** Feng 2017 세
  행성 모두 NEA 에서 disputed 로 플래그됩니다. cfg 는 이들을 존재
  하는 것으로 다루고 그에 맞게 합성하지만, Phase 2 / Phase 3
  후속이 Figueira 2025 나 추가 ESPRESSO RV 재분석이 636 d 신호를
  확인할지 철회할지 모니터링해야 합니다. 철회되면 이 Phase 3
  마크다운은 삭제가 아니라 archive 되어야 합니다.
- **실제 질량.** Msini = 3.93 ± 1.05 M⊕ 가 측정량입니다. 실제
  질량은 미지의 궤도 경사 i 에 의존. cfg 는 τ Ceti 잔해 원반면
  (공면 가정) 에서 i ≈ 35° 를 채택해 실제 질량 ≈ 6.8 M⊕ 를 얻음.
  미래 astrometric 검출 (Gaia DR4 binary 카탈로그) 이 i 를 제약해
  실제 질량을, 따라서 f 의 sub-Neptune vs. super-Earth bulk 분류를
  옮길 수 있음.
- **반지름은 가정 값, 측정 아님.** DB 는 sub-Neptune mass–radius
  관계에서 반지름 1.81 R⊕ 를 저장. f 는 transit 하지 않아 아래쪽
  으로는 미제약. 실제 질량이 더 크고 (sin i < 0.7) 행성이 두꺼운
  envelope 의 sub-Neptune 이 아닌 얇은 얼음의 암석체라면, R 은
  1.4 R⊕ 까지 낮아질 수 있고 ρ ≈ 8 g/cc.
- **사용자 입력. P=4562 d / 5 AU "h-후보".** 이 합성에 대한 사용자
  요청은 τ Cet h 를 P = 4562 d, a ≈ 5.0 AU (소행성-analog 벨트
  안쪽 가장자리 근처) 로 묘사했습니다. DB 의 권위 있는 h 는
  P = 49.41 d / a = 0.243 AU. 4562 d 후보는 Feng 2018 §3.4 의
  장주기 신호 또는 이후 RV 재분석 후보 중 DB 가 ingest 하지
  않은 것일 가능성. 큐레이션 질문은 `db/systems/tau_cet.json` 의
  Open item 에 로깅됨. 이 Phase 3 합성은 f 를 1.33 AU 의 *가장
  바깥쪽* 현재-DB 행성으로 다루며 DB 와 일치.
- **맨 암석 무대기 cfg variant.** 대안적 해석은, f 가 휘발성
  envelope 을 완전히 잃었을 가능성 (호스트의 노년 시기 거대 충돌로
  인해). 맨 암석 variant 는 G8V 조명 아래 노출된 규산염 기반암과
  풍화 패턴, 대기 안개 없음, 더 또렷한 terminator 를 보일 것.
  Open item 의 cfg variant 로 보존. canonical 픽은 아님.
- **Sub-glacial 해양 cfg 디테일.** 미래의 (super-Earth 영역으로
  확장된) Europa급 내부 모델이 매장 액체층을 확인하면, cfg 는
  열 플럭스가 높은 영역 근처에 cryovolcanic 분출 Region 패턴을
  추가할 수 있습니다. 현재는 Confidence=low 피처로 다루며 애니메이션
  처리 안 함.

## Related

- [tau-cet](tau-cet.md) — 호스트 별 Phase 3 (G8V metal-poor.
  조용함, 늙음, 잔해 원반 보유)
- [tau-cet-g](tau-cet-g.md) — 안쪽 자매. 뜨거운 맨 암석
- [tau-cet-h](tau-cet-h.md) — 안쪽-중간 자매. Venus-analog
- [methodology](../reference/methodology.md) — Decisions 스키마
- [rex-data-comparison](../reference/rex-data-comparison.md) — §6
  이 호스트 Phase 3 에서 참조한 τ Ceti e 큐레이션 갭을 문서화
