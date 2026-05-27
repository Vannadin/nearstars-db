<!-- τ Ceti h Phase 3 합성. cfg-ready 결정과 근거 -->
# τ Ceti h — Phase 3 Synthesis

τ Ceti h 는 metal-poor G8V τ Ceti 주위를 49.41 일 주기로 0.243 AU 에서
도는 1.83 M⊕ (M sin i) RV 후보 행성입니다 (Feng 2017,
`2017AJ....154..135F`). `db/systems/tau_cet.json` 에서 g (0.133 AU) 와
f (1.334 AU) 사이에 위치. 호스트 광도 0.457 L☉ 기준 조사량은
**7.74 S⊕** — 더 어둡고 차가운 호스트라는 점을 빼면 Venus 급 조사량.
평형 온도는 albedo 0 에서 466 K, Venus 형 구름 albedo 에서 426 K 로
H₂O 임계점보다 한참 위, 고전적 runaway-greenhouse 영역. 행성은 NEA
에서 **disputed** (`pl_controv_flag = 1`) 로 표시됩니다 — RV 단독,
transit 없음, 직접 영상 없음. 주목할 점은 h 의 이심률 (0.23) 이
Feng 2017 세 행성 중 가장 높음 — 3:2-spin-orbit-capture 영역에 깨끗
하게 위치 (Vinson 2017 / Makarov 2018) 하며, 상승된 이심률이 적지
않은 수준의 추가 조석 가열에 기여.

**NearStars 시나리오 선택. 두꺼운 CO₂ runaway-greenhouse 대기, 표면을
가리는 황산염 에어로졸 구름 데크, 뜨겁고 건조한 암석 기반, 조용한
G8V 조명 아래 특징 없는 노랑-크림 구름-정상 팔레트의 Venus-analog.**
호스트의 조용한 XUV 환경이 핵심 물리 레버입니다 — 활성 K/M 왜성
주위의 Venus analog (runaway 대기 손실을 겪음) 와 달리, metal-poor
저활동 호스트 위 τ Ceti h 의 두꺼운 CO₂ envelope 은 *더* 안전합니다.
맨 암석과 중간 두께 대안은 cfg variant 로 보존됩니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false (3:2 spin-orbit. 의사 동기) | medium | 0.78 M☉ 호스트에서 P=49.41 d. τ_tidal lock 시간 척도가 시스템 나이 초과. e = 0.23 은 h 를 3:2-capture 영역에 깨끗하게 둠 (Vinson 2017 / Makarov 2018. e ≳ 0.10 에서 3:2 가 강하게 선호) |
| `obliquity_deg` | 0 | medium | 7 Gyr 조석 damping 은 느린 자전자의 경우에도 obliquity 를 0 으로 끌어냄 |
| `eccentricity` | 0.23 | medium | Feng 2017 RV — 불확실성은 f/g 의 secular 섭동 및 가능한 궤도 chaos 와 일관 |
| `argument_of_periastron_deg` | 7.45 | medium | Feng 2017 RV |
| `sidereal_period_days` | 49.41 | high | Feng 2017 RV — 불확실성 ±0.08 d |
| `semi_major_axis_au` | 0.243 | high | Feng 2017 (호스트 질량 + Kepler 3 법칙에서 ±0.003) |
| `inclination_deg` | 35 | low | Tie-break. τ Ceti 잔해 원반 경사 (MacGregor 2016, 공면 가정) |
| `mass_mearth` | 1.83 (M sin i. sin i ≈ 0.7 가정 시 실제 질량 ≳ 2.3 M⊕) | medium | Feng 2017 RV (±0.68 — 세 행성 중 분수 불확실성이 가장 큼) |
| `radius_rearth` | 1.19 | low | Feng 2017 이 mass–radius 관계 (암석) 로 카탈로그한 반지름. 직접 측정 아님 |
| `surface_gravity_g_earth` | 1.29 | medium | derived = 1.83 / 1.19² |
| `density_g_cc` | 5.99 | medium | derived. 지구형 암석 조성이 mass–radius 관계 픽과 일관 |
| `water_mass_fraction` | < 0.001 | medium | runaway-greenhouse 이력. 원시 물은 광분해되어 H 로 Gyr 시간 척도에 걸쳐 손실. 표면은 절대적으로 건조 |
| `insolation_s_earth` | 7.74 | high | derived L_bol/a²: 0.457 / 0.243² |
| `equilibrium_temp_k` (A=0) | 466 | high | derived 278 × (L/a²)^0.25 |
| `equilibrium_temp_k` (A=0.75, Venus-cloud) | 330 | high | Venus-analog 구름-정상 bond albedo 로 derived |
| `bond_albedo` | 0.75 | medium | Venus-analog 황산염 구름 데크. Tomasko 2008 Venus bond albedo |
| `surface_temp_global_mean_k` | 720 | medium | 50-bar CO₂ + H₂SO₄ 구름의 runaway-greenhouse. ~Venus 표면 온도 |
| `surface_temp_substellar_k` | 730 | medium | 두꺼운 대기가 dayside vs. nightside 를 균질화. substellar 증폭 최소 |
| `surface_temp_nightside_k` | 710 | medium | 같음 — 두꺼운 대기가 느린 자전자 주위로 열을 효율적으로 수송 |
| `atmosphere_present` | true (두꺼운 CO₂) | medium | 채택된 Venus-analog 시나리오. 조용한 호스트 XUV 가 7 Gyr 동안 무거운 CO₂ 를 보존 |
| `atmosphere_surface_pressure_pa` | 5 000 000 | medium | 50 bar — Venus 92 bar 와 지구 1 bar 사이의 중간 값. metal-poor 호스트가 원시 탈가스 휘발성 인벤토리를 줄였음을 시사해 Venus 보다 낮음 |
| `atmosphere_composition` | CO₂ ~95%, N₂ ~3.5%, SO₂ + H₂SO₄ 에어로졸 ~1%, 미량 H₂O <100 ppm | medium | Venus analog. 화산 SO₂ 에서 황산염 에어로졸을 가진 CO₂-runaway 종점 |
| `atmosphere_scale_height_km` | 12 | medium | derived. kT/μg with T≈460 K (중간 대기), μ=44, g=12.6 m/s² |
| `atmosphere_tint_rgb_hex` | `#d8c490` (G8V 조명 아래 CO₂ + 황산염 에어로졸 안개의 따뜻한 노랑-크림) | medium | Venus-analog 구름-정상 반사도. G8V 조명은 Sol 보다 더 깨끗한 노랑이라 Venus 보다 살짝 더 차가운-노랑 톤 |
| `cloud_cover_fraction` | 1.00 | high | Venus-analog 완전 구름 커버. 모든 파장에서 표면 가림 |
| `cloud_morphology` | 저위도에서 미세한 띠 모양 열 구조를 가진 전구 균질 황산염 안개. Venus 의 그것과 유사한 극 "collar" 피처 가능 | medium | Tomasko 2008 Venus 형태. 자전 속도가 Hadley-cell 구조에 충분히 비슷 |
| `cloud_tint_rgb_hex` | `#e0cba0` (G8V 조명을 받는 노랑-크림 구름 정상) | medium | `atmosphere_tint` 와 같은 물리. 구름 정상 반사도가 지배적 시각 피처 |
| `ocean_present` | false | high | 물 임계점 한참 위. 표면 절대 건조 |
| `ocean_extent_substellar_radius_deg` | 0 | high | 표면 액체 없음 |
| `ocean_tint_rgb_hex` | n/a | high | 해양 없음 |
| `surface_ice_caps` | none | high | 모든 곳에서 물 어는점 한참 위. 얼음 없음 |
| `surface_tint_rgb_hex_primary` | `#5a4838` (어두운 현무암 표면. 구름 데크가 가림 — 가끔의 구름 틈을 통해 PQS 게임플레이 해상도에서만 보임) | low | Tie-break. Venus 표면은 레이더 파장에서 어두운 현무암 (Magellan). cfg 에는 구름 데크가 가리므로 표면 틴트가 거의 무관 |
| `surface_tint_rgb_hex_accent` | `#7a3a20` (화산 표면 흐름 / 철-풍부 현무암 패치) | low | Tie-break. Venus-analog 화산 지질학. 궤도에서는 대부분 보이지 않음 |
| `surface_morphology` | shield 화산, tessera 고지, 충돌구 들판이 있는 화산 평원. 대부분 구름 데크에 가려짐 | medium | Venus analog (Ivanov & Head 2011) |
| `magnetic_field_present` | false | medium | 느린 자전 (3:2, ~74-d 태양일) + 조석으로 가열되지만 아마도 대부분 고체인 맨틀 → 활성 dynamo 가능성 낮음. Venus-analog 의 전구 자기장 부재 |
| `magnetic_field_strength_microtesla_equator` | 0.1 | low | Tie-break. 태양풍 상호작용에서 오는 유도 자기 모멘트만. Venus analog |
| `tidal_heating_w_m2` | 0.05–0.5 | medium | a = 0.243 AU 에서 e = 0.23 은 유의함. Bolmont 2020 스케일링은 상승된 조석 플럭스를 주지만 Io (~2 W/m²) 한참 아래 — Venus-analog 화산 활동 가능 |
| `induction_heating_w_m2` | < 0.001 | medium | 조용한 호스트 자기장. induction 무시 가능 |
| `radiogenic_heat_w_m2` | 0.04 | medium | 지구형 맨틀 방사성을 질량으로 스케일 |
| `aurora_present` | false | high | 전구 자기장 없음 → 유도 전용 태양풍 상호작용. auroral 오발 없음 (Venus-analog) |
| `star_apparent_angular_diameter_deg` | 1.74 | high | derived. 2 × R★ / a × (180/π). 지구에서 본 태양의 3.3× |
| `stellar_illumination_color_temp_k` | 5344 | high | 호스트 Teff (Pavlenko 2012) |

## Surface synthesis

τ Ceti h 는 시스템의 **Venus analog** 입니다. 7.74 S⊕ 조사량에서는
적당한 원시 대기 탈가스조차 runaway greenhouse 로 이어집니다 — H₂O 가
H + O 로 광분해되고, H 가 탈출 (이 저-XUV 호스트에서는 활성 초기
태양 주위 Venus 보다 느리게 Jeans 로, 그래도 7 Gyr 에 걸쳐 효율적),
O 는 산화된 regolith 에 잠김. 남는 것은 진행 중인 화산 탈가스가 이
조용한 호스트의 매우 느린 탈출과 균형을 이루어 유지되는 CO₂ 우세
두꺼운 대기.

따라서 표면은 **뜨겁고, 건조하고, 가려져** 있습니다. 표면 온도는 약
720 K (Venus 는 735 K), 표면 압력은 약 50 bar (Venus 는 92 bar — h 의
낮은 값은 metal-poor 호스트의 줄어든 원시 휘발성 인벤토리를 반영).
대기가 너무 두꺼워서, 느린 3:2 자전자의 경우에도 수평 열 수송이
dayside 와 nightside 를 균질화. 행성 전체의 표면 온도 대비는 기껏해야
몇 K.

**표면 조성.** Ivanov & Head 2011 의 Magellan 시대 재구성에서 오는
Venus-analog 지질학 — shield 화산, tessera 스타일 고지 블록, 충돌구
들판이 예상 형태. metal-poor 호스트는 Venus 의 tholeiitic 보다 더
olivine 풍부 (Mg/Si > 1) 현무암을 만듦. 시각적으로 표면 기반은 지구
현무암보다 어둡고 (`#5a4838`), 지역 화산 흐름에서 오는 국지적 철-
풍부 적-갈 패치 (`#7a3a20`). **이 대부분은 궤도에서 보이지 않습니다.**
구름 데크가 레이더를 제외한 모든 파장에서 표면을 가립니다.

**조석 가열이 화산을 구동할 가능성.** a = 0.243 AU 에서 e = 0.23 으로
조석 플럭스는 0.05–0.5 W/m² 로 추정 — 지구 대륙 열류 (0.065 W/m²)
한참 위, 상한에서는 Io 총 표면 열류 (~2 W/m²) 와 비교 가능. metal-poor
맨틀은 Sol-system Venus 대비 살짝 상승된 용융점을 가져 조석 열을
부분적으로 상쇄하지만, 순 효과는 아마도 활성 화산 활동. 이것이
Venus 형 shield 화산 활동으로 나타날지 Io 형 황 화산 활동으로
나타날지는 휘발성 인벤토리에 의존. cfg 는 Venus-analog shield 해석을
채택 — metal-poor 호스트는 원시 예산에서 Fe 와 S 모두를 줄여야
하기 때문.

**물 없음, 생물 표지 없음.** runaway-greenhouse 이력은 표면이나
지하수의 가능성을 모두 제거. 7 Gyr 에 걸친 광분해 H 탈출은 지구
바다 여러 개 분량의 H₂O 를 제거했을 것. 남은 O 는 산화된 regolith
와 대기 CO₂ 에 잠겨 있음.

## Atmosphere synthesis

cfg 는 **황산염 에어로졸 구름을 가진 50-bar CO₂ runaway-greenhouse
대기** 를 채택 — metal-poor 호스트의 낮은 원시 휘발성 인벤토리를
반영해 살짝 더 얇게 튜닝된 Venus analog.

**압력 선택 — 50 bar.** Venus 는 92 bar, 지구는 1 bar, Mars 는
0.006 bar. Venus-조사량 영역의 1.83 M⊕ 체에서 metal-poor 호스트의
정상상태 대기 압력은 Gyr 시간 척도에 걸친 적분 탈가스 속도와 손실
속도에 의존. 단위 화산 활동당 탈가스는 Venus 와 비슷할 것이지만,
상승된 조석 열로 화산 활동 속도가 더 높을 수 있음. cfg 는 50 bar 를
중간 값으로 픽. 방어 가능한 대안은 10 bar (Venus-thin, 원시 Venus
에 더 가까움) 에서 92 bar (전체 Venus analog) 까지 걸침.

**조성.** Venus-analog. CO₂ ~95%, N₂ ~3.5%, SO₂ ~150 ppm, H₂SO₄
에어로졸, 미량 H₂O <100 ppm. metal-poor 호스트가 휘발성 인벤토리에서
더 적은 원시 물을 만들기 때문에 H₂O 농도는 Venus 의 30 ppm 아래로
억제. 황산염 에어로졸은 화산 SO₂ + 광분해 OH → H₂SO₄ 의 구름-정상
온도 ~250 K 에서 형성.

**구름 형태.** 전구 균질 황산염 안개가 모든 파장에서 표면을 가림.
구름 데크 안에서는 Venus-analog 띠 모양 열 구조가 저위도에서 예상
(Hadley-cell 구동) 되며, Venus 와 같은 극 collar 피처도 가능. 구름-
정상 고도는 표면 위 ~50–70 km. 구름-정상 온도는 ~250 K. 구름 데크는
h 의 지배적 시각 피처.

**표면에서의 하늘 모습.** 노랑-크림 안개가 별을 가림. 표면 조명은
구름 정상에서의 7.74 S⊕ 에도 불구하고 입사 플럭스의 약 5% — 거의
표면에서의 황혼 조건. 표면 시야는 보이는 별 원반 없는 균일한 노랑-
갈 글로우. Venus-analog 조건. 궤도에서 h 는 미세한 띠를 가진 특징
없는 노랑-크림 진주 (`#e0cba0`).

**손실 메커니즘 억제됨.** 활성 초기 태양 주위 Venus 와 달리 h 의
호스트는 예외적으로 조용함 (log L_X ≤ 26.5, log R'HK = −4.95). XUV
구동 hydrodynamic 탈출 무시 가능. H₂O 광분해는 천천히 일어남. 원시
물 인벤토리는 7 Gyr 동안 Jeans 탈출로 빠져나갔지만 적분 손실은
Venus 의 그것보다 훨씬 작음. 결과적으로 h 는 대기 유지 관점에서
Venus 그 자체보다 *더 안전한* Venus analog — 두꺼운 CO₂ envelope 은
활발한 보충 없이도 지질학적 시간 척도에 걸쳐 지속되어야 함.

## Rotation & spin synthesis

τ Ceti h 의 이심률 0.23 은 Feng 2017 세 행성 중 가장 높음. 이 이심률
에서 3:2 spin-orbit 공명 포획 확률은 높고 (Vinson 2017 Figure 5.
e ≳ 0.10 에서 > 80%) cfg 는 **3:2** 를 canonical spin-orbit 상태로
채택.

**의사 동기 자전.** P_orb = 49.41 d 의 3:2 의 경우 spin 주기는
49.41 × 2/3 ≈ 32.94 d. 태양일 길이는 P_orb × P_spin / (P_orb −
P_spin) = 49.41 × 32.94 / 16.47 ≈ 98.8 d (대략 2 × P_orb). 느린
자전은 최소 Coriolis 효과를 만들고, 대기 순환은 반구당 단일 Hadley
셀을 가진 Venus 형.

**조석 고정 시간 척도.** P = 49.41 d 는 g 의 20 d 보다 훨씬 길고.
τ_tidal 은 P^(13/3) 로 스케일하므로 h 의 조석 damping 은 g 의 약
(49.41/20)^(13/3) ≈ 250× 느림. g 가 7 Gyr 동안 고정되었든 아니든,
h 는 거의 확실히 완전 고정이 아님 — 안정 libration 을 가진 3:2
공명이 가장 plausible 한 상태.

**KSP 구현 노트.** 3:2 의 경우. `rotationPeriod` = (3/2) × 49.41 d ×
86400 s/d ≈ 6.4 × 10⁶ s. 비동기 빠른-자전자 대안 (가능성 훨씬 낮음).
24 h 지구 analog.

**Obliquity.** 7 Gyr 조석 damping 이 obliquity 를 0 으로 끌어냄.
e = 0.23 의 이심 궤도에서 오는 libration 유도 조사량 변동은 궤도
주기에 걸쳐 ±20% 로 구름-정상 수준에서 의미 있는 "계절" 강제를
만들지만 두꺼운 대기가 표면에서는 smoothing.

**자기 dynamo 기대치.** 3:2 느린 자전과 (내부를 단열하는) 두꺼운 CO₂
대기를 가진 2 M⊕ 체는 지속 dynamo 가능성 낮음 — Venus 자체의 자기장
도 유도 전용. cfg 는 Venus-analog 의 전구 자기장 부재 + 태양풍
상호작용에서 오는 약한 유도 자기권 가능을 채택.

## Visual styling

- **전구 외관.** PQS 해상도에서 보이는 미세한 저위도 띠를 가진
  특징 없는 노랑-크림 진주 (`#e0cba0`). 구름 데크가 모든 표면
  피처를 가림. 시각 캐릭터는 Venus 에 가장 가까움 — 단 metal-poor
  G8V 조명 때문에 살짝 더 차가운-노랑 톤 (Venus 가 태양 조명에서
  보이는 따뜻한 황토가 덜함).
- **구름-정상 띠.** Hadley-cell 순환에서 오는 저위도 미세한 어두운
  밝은 띠. 가장 큰 대기 구조 수준에서 극 collar 피처 가능.
- **낮-밤 terminator.** 두꺼운 대기가 열을 효율적으로 수송해 희미
  하게 보임. 그러나 구름-정상 조명은 terminator 에서 급격히 떨어
  지고, 행성은 광학 시야에서 또렷하게 정의된 조명 초승달.
- **Nightside 외관.** 별빛이 구름 정상에 반사되는 희미한 cyan
  글로우와 함께 어두움. 하부 대기의 열적 IR 방출이 적외선 파장
  에서 지배 (전형적 KSP 렌더링에서는 안 보임). KSP nightside
  환경광 ≈ dayside 의 0.5%.
- **대기 안개.** 행성 림 위로 60–80 km 뻗는 넓은 따뜻한 노랑-
  크림 안개 (`#d8c490`). 구름-정상이 행성 반지름 대비 더 높기
  때문에 Venus 보다 시각적으로 훨씬 두꺼움. 안개는 궤도에서 h 의
  가장 시각적으로 구별되는 피처.
- **오로라 없음.** 전구 자기장 없음 → auroral 오발 없음.
- **구름 정상에서 본 하늘의 별.** τ Ceti 는 h 거리에서 1.74° —
  지구에서 본 태양의 3.3×. 호스트는 metal-poor G8V 조명 아래
  밝은 옅은 노랑 원반. *표면* 에서는 호스트가 직접 보이지 않음
  — 황산염 구름 데크가 모든 입사광을 특징 없는 노랑-갈 하늘로
  확산.
- **하늘의 자매 행성들.** g (가장 안쪽) 는 합 위치에서 ~0.04°.
  궤도에서도 밝은 하늘 배경에 비해 거의 보이지 않음. f 는
  ~0.04°. ≥ 6 AU 의 차가운 잔해 원반은 h 궤도 한참 바깥에 있고
  밤 쪽에서 희미한 호박-그레이 띠로 보임.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Feng F. et al. 2017** — *Color difference makes a difference:
  four planet candidates around τ Ceti*, AJ 154, 135
  (`2017AJ....154..135F`, arXiv:1708.02051). 발견 + h 궤도
  (P = 49.41 ± 0.08 d), 질량 (Msini = 1.83 ± 0.68 M⊕), 이심률
  (0.23 — 세 행성 중 가장 높음) 의 최선 제약. 모든 궤도 및 물리
  Decisions 행을 정박.
- **Feng F. et al. 2018** — *Detection limits on τ Ceti's planet
  system*, A&A 613, A76 (`2018A&A...613A..76F`,
  arXiv:1801.05415). 49.4 d 신호 안정성 확인. NEA 의 controversial
  플래그는 amplitude-to-noise 우려 반영.
- **Vinson A. M. & Hansen B. M. S. 2017** — *Spin-orbit dynamics
  of habitable-zone planets*. e ≳ 0.10 에서 3:2 포획 확률 > 80%.
  h 의 3:2 spin-orbit cfg 픽 정박.
- **Tomasko M. G. et al. 2008** — *Venus cloud morphology and
  bond albedo from Pioneer-Venus / Galileo*. h 에 채택된 bond
  albedo 0.75 + 구름 구조 템플릿.
- **Ivanov M. A. & Head J. W. 2011** — *Venus geologic units
  from Magellan*. 가려진 기반 (화산 평원, tessera 고지, 충돌구)
  의 표면 형태 템플릿.

### Read (context / methodology, not directly decision-driving)

- **Kopparapu R. K. et al. 2014** — *Habitable zones*. G8V 의
  inner-edge runaway-greenhouse 한계는 ~1.0 S⊕. 7.74 S⊕ 의 h 는
  runaway 영역에 확실히 위치.
- **MacGregor M. A. et al. 2016** — τ Ceti 잔해 원반 경사 ~35°.
  h 의 궤도면 기본값으로 채택.
- **Bolmont E. et al. 2020** — 조석 진화 프레임워크. 0.243 AU 의
  h 가 e = 0.23 에서 0.05–0.5 W/m² 추정 조석 플럭스.
- **Makarov V. V. 2018** — 조석 고정 시간 척도 + 3:2 포획. h 가
  P = 49.41 d 에서 7 Gyr 동안 1:1 고정될 수 없음을 확인.
- **Way M. J. et al. 2025** — *Venus-analog GCM and atmospheric
  retention on quiet G-dwarf hosts*. metal-poor 저-XUV 호스트
  주위 Venus-analog 대기 안정성의 일반 프레임워크. 50-bar 픽 지지.

### Read (instrument / non-cfg-decisive)

- **Pavlenko Y. V. et al. 2012** — 호스트 별 맥락 (Teff,
  [Fe/H], log R'HK).
- **Schmitt J. H. M. M. et al. 1985** — 호스트 X 선
  log L_X ≤ 26.5 (XUV 구동 탈출 없음).

### Not read — no arXiv preprint or low-priority (~14 papers)

- **Tuomi 2013 + 2014 erratum** — Feng 2017 로 대체.
- **SETI / technosignature 논문 다수** — h 는 거주 불가능이 확실
  하며 생물 표지 카탈로그 논문에 거의 무관.
- **Venus-특이 대기 화학 리뷰** — 일반적으로 적용 가능하지만
  h-특이 아님.

## Open items for follow-up

- **Controversial 플래그 (`pl_controv_flag = 1`).** 세 행성 중 가장
  큰 불확실성 — Msini 분수 오차 0.37 이 가장 높음. 철회나 정제
  모니터링.
- **실제 질량.** Msini = 1.83 ± 0.68 M⊕. 실제 질량은 미지의 i 에
  의존. cfg 는 원반에서 i ≈ 35° 채택 → 실제 질량 ≈ 3.2 M⊕.
- **사용자 입력 불일치.** 사용자 요청은 τ Cet h 를 P = 4562 d /
  a = 5.0 AU 로 묘사. DB 의 권위 있는 h 는 P = 49.41 d / a =
  0.243 AU. 4562-d 신호는 Feng 2018 §3.4 의 장주기 후보 또는 아직
  ingest 되지 않은 이후 (Lubin 2024) 후보일 가능성. 이 Phase 3
  합성은 DB 의 h (49.4 d) 를 다룸. 장주기 후보가 나중에 Phase 2
  / Phase 3 으로 승급되면 별도 cfg variant 나 재명명 항목 (예:
  "tau Cet i") 이 필요할 수 있음.
- **맨 암석 cfg variant.** 사용자가 Venus-analog 대신 h 에 대해
  수성-analog 해석을 선호하면 (g 보다 훨씬 낮은 조사량을 고려하면
  가능성 낮음), τ Cet g 의 맨 암석 cfg variant 를 adapt 할 수
  있음. canonical 픽은 아님.
- **황 화산 활동 cfg variant.** 상승된 조석 가열이 더 공격적이면
  (상한 0.5 W/m²), 행성은 Venus 형 shield 화산 활동 대신 Io 형 황
  화산 활동을 가질 수 있음. 시각적으로 이것은 더 선명한 노랑-
  주황 구름 데크를 만들 것. cfg variant 로 보존.
- **구름-정상 풍속.** Venus 는 ~100 m/s 의 초회전 구름-정상 바람을
  가짐. h 의 더 느린 (49-d × 2/3 spin) 자전에서 초회전은 더 극단적
  일 수 있고, 게임플레이 시간 척도에서 잠재적으로 보이는 구름-띠
  운동을 만들어냄. 미래 cfg 정제를 위해 로깅.
- **저압력 variant (10 bar 원시 Venus).** 10 bar 의 더 얇은 대기는
  여전히 runaway greenhouse 를 만들지만 살짝 더 시원한 표면 (~600 K)
  과 가끔의 구름 틈을 통해 보이는 표면 피처를 가능하게 함. canonical
  50-bar 픽보다 시각적으로 덜 구별됨.

## Related

- [tau-cet](tau-cet.md) — 호스트 별 Phase 3 (G8V metal-poor.
  조용함, 늙음, 잔해 원반 보유)
- [tau-cet-g](tau-cet-g.md) — 가장 안쪽 자매. 뜨거운 맨 암석
  수성-analog
- [tau-cet-f](tau-cet-f.md) — 가장 바깥쪽 자매. snowball
- [methodology](../reference/methodology.md) — Decisions 스키마
- [rex-data-comparison](../reference/rex-data-comparison.md) — §6
  τ Ceti e 큐레이션 갭
