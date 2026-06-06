<!-- Proxima Cen c Phase 3 합성. cfg-ready 결정과 근거 -->
# Proxima Centauri c — Phase 3 Synthesis

Proxima Centauri c 는 **논쟁 중인 시선속도 후보** 입니다 — 가장 가까운
별에 딸린 장주기·저질량 동반체로, Damasso et al. 2020 (Sci. Adv. 6,
eaax7467) 이 a = 1.48 ± 0.08 AU 에서 최소 질량 5.8 ± 1.9 M⊕ 의 ~1900일
신호로 보고했습니다. 실재한다면 놀랍도록 차가운 세계일 것입니다. 0.001567
L☉ 의 플레어별 Proxima 주위 1.48 AU 에서 평형 온도는 **T_eq ≈ 39
(+16/−18) K** 에 불과하고 (Damasso 2020) — 해왕성보다도 차갑습니다 —
일사량은 지구의 S ≈ 7.2 × 10⁻⁴ 수준입니다. 이 신호는 **독립적으로 확인된
적이 단 한 번도 없습니다**. Artigau et al. 2022 의 HARPS 데이터 재추출은
그 증거를 찾지 못했고, 2025년 NIRPS 캠페인 (Suárez Mascareño et al.) 은
더 낮은 진폭의 장주기 신호에 대한 "결론을 내릴 수 없는" 힌트만 회수했습니다.
Proxima c 는 tau Cet e 나 40 Eri A b 와 동일하게 **문서화된 후보**로
NearStars 에 포함됩니다 — 공개 기록에 실재하는 항목이되, 미확인으로
표기됩니다.

Damasso 2020 의 과학적 헤드라인은 이 행성의 위치입니다. 1.48 AU 는
원시행성 눈선 (snow line) 보다 한참 바깥인데, 이렇게 어두운 별 주위에서
눈선은 ~0.15 AU 안쪽에 있었습니다. 이렇게 멀리 떨어진 슈퍼지구 (또는 그
이상) 는 in-situ 형성으로는 설명하기 어렵고, 현재 거리의 몇 배 지점에서
일어난 type-II 이주를 가리킵니다. 질량이 두 번째 갈림길입니다. RV 최소
질량은 5.8 M⊕ 이지만, Damasso 2020 은 Gaia–Hipparcos 고유운동 이상
(Kervella et al. 2020) 이 1–2 AU 에서 **~10–20 M⊕ 의 진질량**과 양립한다고
지적합니다 — 정확히 해왕성급입니다. 차가운 외곽 원반에서 형성되는 10–20 M⊕
핵은 교과서적 얼음 거인 경로이므로 (천왕성과 해왕성이 각각 ~14.5, ~17 M⊕),
이 합성은 진질량 독법을 채택하고 Proxima c 를 **차가운 얼음 거인**으로
렌더링합니다.

**NearStars 시나리오 선택. Proxima 주위 넓은 1.48 AU 원궤도 위의
짙은-청색 ~40 K 해왕성급 얼음 거인으로 — 암석질 내행성 b·d 와 대비되는,
포피 (envelope) 를 두른 차가운 짝으로, 흐릿한 붉은 점광원 별이 비추고 그
거대 플레어에 노출된 모습으로 — 렌더링합니다.** 궤도와 ~39 K 온도만이
측정/유도된 유일한 앵커이며 canonical-aligned 입니다. 시각 요소 전부 —
얼음 거인이라는 본성 자체, 메탄-블루 색조, 자전, 오프셋 자기장, 그리고
플레어가 구동하는 오로라 — 는 해왕성 유사체 interesting-first 독법으로
기본값을 잡은 within-window tie-break 입니다. 암석질 슈퍼지구 대안 (5.8
M⊕ 최소-질량 독법) 은 `## Canonical alternatives` 에 보존됩니다. **고리
없음**. 널리 퍼진 "Proxima c 에 고리가 있을 수 있다"는 이야기는 Gratton
et al. 2020 의 논쟁적 SPHERE 짝과 논란 중인 항성주위 먼지 고리 (Anglada
2017 / MacGregor 2018) 에서 비롯한 것으로, 어느 쪽도 행성 고유의 고리
증거가 아닙니다 — 고리 가드레일에 따라 `ring_present = false` 입니다.

## Decisions

Kopernicus / 대기 cfg-ready 값. `Confidence`. high = 직접 측정되거나
강하게 제약됨, medium = 강한 지지를 가진 이론, low = 허용 윈도 안의 미적
선택. 전반적으로 낮은 신뢰도 바닥을 유념하십시오. 행성 자체가 **미확인·논쟁
중인 후보**이므로, "high" 행조차 그 존재를 전제로 한 조건부입니다.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 0.122 M☉ 별 주위 1.48 AU / 1900일 궤도 — 조석-감쇠 시간척도가 4.85 Gyr 나이보다 ≫. spin–orbit 결합 불가 |
| `eccentricity` | 0.0 | medium | Damasso et al. 2020 — 원궤도 채택 (e 를 0 으로 고정). 자유-이심률 런은 e = 0.41 (+0.34/−0.26) 을 줬으나 유의 임계 이하였고, 베이지안 증거도 이심 모델을 선호하지 않음. 진정으로 미제약 — Open items 참조 |
| `semi_major_axis_au` | 1.48 (±0.08) | high | Damasso et al. 2020 — Table 1 유도 파라미터 (RV + GLS 주기 분석) |
| `sidereal_period_days` | 1900 (+96/−82) | high | Damasso et al. 2020 — GLS 피크 ~1907 d, FAP 0.01%. P = 5.21 (+0.26/−0.22) yr |
| `inclination_deg` | unconstrained | low | Damasso et al. 2020 은 Hipparcos–Gaia 고유운동 이상에 i/Ω 피팅을 시도했으나 그 Δμ 가 Proxima c 때문인지 단정할 수 없었음. 원반-공면 해 (i ≈ 45°, m = 8.2 M⊕) 가 하나의 문헌 옵션. cfg 는 궤도 경사를 낮은-신뢰도 선택으로 남김 |
| `mass_mearth` | ~14 | low | Tie-break. Gaia–Hipparcos PMa 진질량 ~10–20 M⊕ (Kervella et al. 2020, Damasso 2020 인용). 얼음-거인 독법으로 중간값 ~14 M⊕ 채택. RV 최소 질량은 5.8 ± 1.9 M⊕ — Canonical alternatives 참조 |
| `mass_mjup` | ~0.044 | low | = ~14 M⊕ / 317.8 |
| `radius_rearth` | ~3.8 | low | Tie-break. transit 없음 (TESS/지상 탐색 모두 비검출). ~14 M⊕ 얼음 거인의 질량–반지름 추론 ≈ 해왕성 (3.88 R⊕). cfg 는 ~3.8 R⊕ 선택 |
| `surface_gravity_g_earth` | ~1.0 | low | 유도. g = M/R² = 14/3.8² ≈ 0.97 g⊕ (해왕성 1.14 대비) |
| `density_g_cc` | ~1.4 | low | 유도. 3.8 R⊕ 구 안의 14 M⊕ ≈ 1.4 g/cc — 얼음-거인 범위 (해왕성 1.64 대비) |
| `insolation_s_earth` | 0.00072 | high | 유도. S = L/a² = 0.001567 L☉ / (1.48 AU)² ≈ 7.2 × 10⁻⁴ S⊕ — 무시할 만함. 깊이 차가운 세계 |
| `equilibrium_temp_k` | 39 (+16/−18) | high | Damasso et al. 2020 (Table 1 유도). 독립 재계산. T_eq = 278.3 × (L/a²)^0.25 ≈ 45 K (A = 0), ≈ 42 K (A = 0.3) — 일관 |
| `bond_albedo` | 0.30 | low | Tie-break. 해왕성 유사체 (해왕성 ≈ 0.29). 차가운 메탄 대기의 고층-구름/연무 알베도. 측정 없는 윈도 안의 미적 선택 |
| `atmosphere_present` | true | low | Tie-break. 차가운 외곽 원반에서 형성되는 ~10–20 M⊕ 핵은 H₂/He 포피를 보존 (얼음-거인 경로). 진질량이 5.8 M⊕ 최소값이라면 더 얇은 휘발성 포피도 가능 — Canonical alternatives 참조 |
| `atmosphere_reference_pressure_pa` | 100000 | low | 얼음 거인은 고체 표면이 없음. 구름층 렌더링용 1 bar cfg 기준 |
| `atmosphere_composition` | H₂/He bulk with CH₄ (methane), Neptune-class; condensed CH₄/N₂ haze likely at ~40 K | low | Tie-break. 측정 없음. 해왕성/천왕성 얼음-거인 화학을 모델로 함. ~40 K 에서 메탄은 상층에서 대부분 응결되어, 잔류 기상 CH₄ 흡수 + 얼음 연무를 남김 |
| `atmosphere_tint_rgb_hex` | `#2f5fb0` (deep methane blue, dimmer/cooler than Neptune) | low | Tie-break. 기상 CH₄ 가 적색광을 흡수 → 해왕성 청색. ~40 K 에서 메탄 응결이 더 많아 해왕성의 선명한 `#4170d0` 보다 다소 옅고 연무가 짙음. interesting-first 선명한 얼음-거인 청색 |
| `cloud_cover_fraction` | 0.6 | low | Tie-break. 균일한 구름층이 아니라 군데군데 흩어진 메탄-얼음/연무 구름 밴드를 가진 차가운 얼음 거인 (해왕성형). 측정 없음 |
| `cloud_morphology` | faint zonal banding with patchy bright methane-ice clouds over a deep blue methane atmosphere; Neptune-analog, muted by the cold | low | Tie-break. 더 차갑고 더 흐리게 비추는 세계로 스케일한 해왕성/천왕성 형태. 7 × 10⁻⁴ S⊕ 에서는 폭풍 활동이 최소로 예상됨 |
| `cloud_tint_rgb_hex` | `#cfe0ec` (pale icy-white methane clouds) | low | Tie-break. 메탄-얼음 구름은 짙은-청색 가스에 대비해 거의 흰색에 차가운-청색 기운이 옅게 섞임. 해왕성의 밝은 구름 줄무늬 유사체 |
| `rotation_period_hours` | 16 | low | Tie-break. 측정 없음. 해왕성 유사체 (~16 h) 채택 — 얼음 거인은 큰 각운동량 예산을 물려받음. 빠른 자전이 흐릿한 띠상 줄무늬를 구동 |
| `obliquity_deg` | 28 | low | Tie-break. 시각적으로 뚜렷한 기울기를 위해 해왕성 유사체 28.3° 채택. 측정 없음. 이 일사량에서는 계절 효과가 무시할 만함 |
| `magnetic_field_strength_microtesla_equator` | 1.4 | low | Tie-break. 해왕성 표면장 (~1.4 µT 적도 평균) 으로 스케일한 얼음-거인 오프셋/기울어진 다이나모. 비대칭 오로라를 위해 오프셋 쌍극자 가정. 측정 없음 |
| `magnetic_dipole_tilt_deg` | 47 | low | Tie-break. 목성형 정렬 자기장 대신 해왕성의 강하게 기울어진 (47°) 오프셋 쌍극자 채택 — 얼음 거인의 특징이며 축-바깥 오로라로 시각적으로 흥미로움 |
| `aurora_present` | true | low | Tie-break (물리적 게이팅). Proxima 는 슈퍼플레어별임 (Howard 2018; Vida 2019). 1.48 AU 의 얼음-거인 자기권은 플레어가 구동하는 플라스마를 오로라로 유도. 흐릿함 (행성이 멀고 자기장이 약함), 낮은-신뢰도 표기 |
| `aurora_color_primary_hex` | `#e0507a` (H Balmer / H₂ pink-red) | low | Tie-break. H₂/CH₄ 대기 오로라는 수소 Balmer + H₂ 밴드 (분홍-적색) 로 방출되며, 지구의 녹색 [O I] 와 구별됨 — 목성/얼음-거인 H₂ 오로라 유사체 |
| `aurora_emission_species_primary` | H Balmer (Hα 656 nm) + H₂ Lyman/Werner bands | low | Tie-break. 수소 우세 대기. 측정 없음 |
| `ring_present` | false | high | 행성 고유의 고리 증거 없음. "Proxima c 고리" 이야기는 Gratton et al. 2020 의 논쟁적 SPHERE 직접촬영 짝과 논란 중인 항성주위 내부 먼지 고리 (Anglada et al. 2017; MacGregor et al. 2018 이 반박) 에서 비롯 — 어느 쪽도 행성주위 고리가 아님. 고리 가드레일. 생략 |
| `ring_observed` | false | high | Damasso 2020 은 RV 검출. 어떤 영상도 고리를 분해하지 못했고, 후보 자체가 미확인 |
| `star_apparent_angular_diameter_deg` | 0.051 | high | 유도. 2 R_star / a = 2 × 0.141 R☉ / 1.48 AU ≈ 0.051° — 지구에서 본 태양 각크기의 약 1/10. Proxima 는 작고 흐릿한 붉은 점광원 |
| `stellar_illumination_color_temp_k` | 2904 | high | 호스트 Phase 3 에서 상속 (`docs/phase3/proxima-cen.md`) — Teff 2904 K, 짙은-적색 M5.5Ve |

## Surface synthesis

채택한 얼음-거인 독법에서 Proxima c 는 렌더링할 고체 표면이 없습니다 —
얼음/암석 핵 위에 H₂/He 포피를 두른 ~14 M⊕ 의 해왕성급 세계입니다.
렌더링 목적의 "표면"은 구름층이며, ~39 K 에서 그 층은 메탄이 지배합니다.

온도가 결정적 사실입니다. 0.001567 L☉ 별 주위 1.48 AU 에서 평형 온도는
~39–45 K 에 불과하며 (Damasso 2020; 재계산), 해왕성의 ~47 K 보다도
차갑습니다. 이 온도에서 메탄은 상층 대기에서 대부분 얼음 구름과 연무로
응결되는 한편, 응결 고도 아래의 잔류 기상 CH₄ 는 여전히 적색광을 흡수해
얼음 거인 특유의 청색을 만들어냅니다. cfg 는 Proxima c 를 **짙은 메탄-블루
세계** (`#2f5fb0`) 로 렌더링합니다 — 추가적인 추위가 더 많은 메탄 응결을
일으키기 때문에 해왕성의 선명한 청색보다 다소 옅고 연무가 짙습니다. 밝은
메탄-얼음 구름 줄무늬 (`#cfe0ec`) 가 짙은-청색 가스 위에 흐릿한 띠상
밴드로 놓이는데, 약한 일사량이 밴드 대비를 억누릅니다. 지구 햇빛의 7 ×
10⁻⁴ 에서는 폭풍을 구동할 항성 동력이 거의 없으므로, 구름층은 해왕성보다
더 잔잔하고 균일합니다.

이는 의도적으로 Proxima 내행성들에 대비되는 **포피를 두른 차가운 짝**
입니다. Proxima b 는 0.0485 AU 에 있는 온화하고 바다를 품었을 수 있는
암석 세계, Proxima d 는 0.029 AU 의 뜨거운 수성 유사체입니다. 멀리 1.48
AU 에 있는 Proxima c 는 이 계의 얼음 거인입니다 — 질량으로는 안쪽 한 쌍의
암석 천체의 1/10 크기에 불과한 단일 흐릿한 청색 원반이지만, 별을 제외하면
시각적으로 이 계에서 가장 큰 천체입니다.

## Atmosphere synthesis

**압력 기준.** 얼음 거인은 고체 표면이 없습니다. cfg 기준 압력은 1 bar
(100 000 Pa) 로, 구름층 렌더링을 고정하는 데에만 쓰입니다. 물리적으로
의미 있는 고도는 상부 대류권의 메탄 응결층입니다.

**조성.** Proxima c 의 대기는 측정된 적이 없습니다 — transit 도 스펙트럼도
없고 확인된 존재조차 없는 RV 후보입니다. 조성은 전적으로 채택한 ~14 M⊕
얼음-거인 질량으로부터 추론됩니다. 해왕성·천왕성과 똑같이, 메탄을 지배적
미량종으로 하는 H₂/He bulk 포피입니다. ~40 K 에서 메탄은 응결점 부근이거나
그 아래에 있으므로, 상층 대기는 기상 CH₄ 가 고갈되고 (얼음 연무 형성)
더 깊은 층은 행성을 청색으로 물들이기에 충분한 양을 유지합니다. cfg 는
이것을 낮은 신뢰도로 인코딩합니다 — 측정이 아니라 해왕성 유사체 기본값
입니다.

**구름-꼭대기 / 위성 관측자에서 본 하늘.** 구름 꼭대기에서 하늘은 작고
흐릿한 짙은-적색 별이 비추는 짙은 메탄-블루 잔뜩 흐린 모습입니다. Proxima
는 1.48 AU 에서 ~0.051° 밖에 차지하지 않습니다 — 지구에서 본 태양 각크기의
약 1/10 — 지구 일사량의 ~7 × 10⁻⁴ 을 보내는 흐릿한 붉은 점광원이라,
낮쪽은 낮이라기보다 깊은 황혼에 가까울 만큼 극도로 어둡습니다. 하늘 건너편,
Proxima 보다 훨씬 밝게 보이는 것은 멀리 떨어진 한 쌍 α Centauri A 와 B
입니다 (Proxima 는 AB 쌍을 ~13 000 AU 에서 공전). 이들은 눈부신 가까운
이중성 "저녁별"로 나타납니다.

**밤쪽과 플레어.** 일사량이 무시할 만하므로 행성은 차갑고 어둡지만,
Proxima 는 슈퍼플레어별입니다. 그 거대 플레어 (Howard 2018; 2019년
ASAS-SN/Evryscope 슈퍼플레어, Vida 2019) 가 고에너지 입자로 계를 적십니다.
1.48 AU 의 얼음-거인 자기권 — 해왕성의 강하게 기울어진 오프셋 쌍극자를
모델로 함 — 은 그 플라스마를 수소 Balmer 와 H₂ 방출로 분홍-적색
(`#e0507a`) 으로 빛나는 **흐릿한 축-바깥 오로라**로 유도할 것이며, 이는
지구의 녹색 산소 오로라와 구별됩니다. 플럭스는 1.48 AU 거리와 약한
자기장에 의해 희석되므로, cfg 는 오로라를 흐릿하고 낮은-신뢰도로 표기합니다
— 측정이 아니라 tie-break 이되, 플레어 호스트를 고려하면 물리적으로 동기가
있는 선택입니다.

## Rotation & spin synthesis

Proxima c 의 자전 측정은 존재하지 않습니다 — 분해된 원반이 없는 미확인
RV 후보입니다.

**조석 감쇠 논거.** 0.122 M☉ 별 주위 1.48 AU 에서 해왕성급 행성의 조석
시간척도는 4.85 Gyr 나이를 한참 초과하므로, Proxima c 는 조석 고정이
**아닙니다** (`tidally_locked = false`) — 조석 고정된 내행성 형제 b·d 와
다릅니다.

**자전 주기 선택.** 얼음 거인은 원반 강착에서 큰 각운동량 예산을 물려받아
빠르게 자전합니다. cfg 는 within-window tie-break 로 해왕성 유사체
`rotation_period_hours = 16` 을 선택합니다. 빠른 자전이 흐릿한 띠상
줄무늬를 구동하지만, 매우 약한 일사량이 밴드 대비를 억누릅니다.

**경사.** Tie-break 미적 선택. 시각적으로 뚜렷한 기울기를 위해 28° (해왕성
유사체 28.3°). 지구 일사량의 7 × 10⁻⁴ 에서 경사는 관측 가능한 계절 효과를
일으키지 않습니다 — 행성은 균일하게 차갑습니다.

**KSP 구현 노트.** 자전 주기 = 16 h = 57 600 s (`rotationPeriod =
57600`). 경사 ≈ 궤도 법선 기준 28°.

## Visual styling

표면 (구름층) 과 대기 결정을 결합하면, Proxima c 는 차갑고 짙은-청색
얼음 거인으로 렌더링됩니다 — 별을 제외하면 이 계의 가장 바깥쪽이자 가장
큰 천체입니다.

- **전역 외관.** 궤도에서 보면 폭 약 3.8 R⊕ (~48 000 km) 의 짙은 메탄-블루
  원반 (`#2f5fb0`) — 해왕성급 세계로, 추가적인 추위 (~40 K vs 해왕성의
  ~47 K) 가 더 많은 메탄 응결을 일으키기 때문에 해왕성 본체보다 옅고 다소
  연무가 짙습니다.
- **구름층 디테일.** 짙은-청색 가스 위에 군데군데 흩어진 밝은 메탄-얼음
  구름 줄무늬 (`#cfe0ec`) 를 가진 흐릿한 띠상 밴드. 7 × 10⁻⁴ 지구 일사량에서
  폭풍 활동은 최소입니다 — 해왕성의 띠상 원반보다 더 잔잔하고 균일합니다.
- **림 연무.** 가장자리의 옅고 차가운-청색 메탄-얼음 연무로, 짙은-청색
  본체 위 얇고 밝은 후광.
- **밤쪽과 오로라.** 밤쪽은 어둡고 차가우며, Proxima 의 플레어 플라스마가
  강하게 기울어진 얼음-거인 자기장에 도달하는 축-바깥 타원에서 흐릿한
  분홍-적색 (`#e0507a`) 수소 오로라가 나타납니다. 흐릿하고 간헐적이며,
  플레어 사건에 연동됩니다.
- **하늘의 별.** Proxima 는 ~0.051° 밖에 차지하지 않습니다 — 지구에서 본
  태양 각크기의 약 1/10 — 지구 일사량의 ~7 × 10⁻⁴ 을 보내는 흐릿한
  짙은-적색 (M5.5Ve, `#c54c2a`) 점광원입니다. 낮쪽은 진짜 낮이 아니라
  깊은 붉은 황혼입니다.
- **하늘의 α Cen AB.** ~13 000 AU 에 있는 밝은 G2V + K1V 쌍 α Centauri
  A 와 B 가 눈부신 가까운 이중성으로 나타납니다 — Proxima 자신 다음으로
  Proxima c 하늘에서 가장 두드러진 "별"입니다.
- **고리 없음.** `ring_present = false` — 행성 고유의 고리 증거가 없습니다
  (논쟁적 영상 이야기는 Canonical alternatives / Open items 참조).

## Canonical alternatives

cfg 는 **얼음-거인 (진질량) 독법**을 렌더링합니다. 공존하는 문헌 독법은
RV 최소 질량에서의 암석/얼음 슈퍼지구입니다.

| cfg pick | Canonical alternative | Why cfg diverges |
|---|---|---|
| `mass_mearth ≈ 14` (Neptune-class ice giant, H₂/He envelope) | **`mass_mearth = 5.8 ± 1.9` (RV minimum mass, Damasso 2020)** — 기껏해야 얇은 휘발성 포피를 가진 암석/얼음 슈퍼지구. `radius ≈ 1.8–2.2 R⊕`, 유의한 가스 포피 없음, ~40 K 의 대기 없는 또는 얇은-대기 동결 천체 | 5.8 M⊕ 값은 **최소값** (m sin i) 입니다. Gaia–Hipparcos PMa 진질량은 ~10–20 M⊕ (Kervella 2020) 로, 얼음-거인 영역에 들어갑니다. cfg 가 진질량 독법을 채택하는 이유는 (a) 차가운 외곽 원반의 10–20 M⊕ 핵에서 물리적으로 기대되는 결과이고 (b) 작은 동결 암석보다 시각적으로 훨씬 뚜렷하기 때문입니다. 최소-질량 독법을 원하는 사용자는 대신 ~2 R⊕ 동결 슈퍼지구를 렌더링해야 합니다 |

Damasso 2020 이 언급한 두 번째 대안. Proxima c 가 **후보 ALMA 차가운
먼지 띠와 공면** (i ≈ 45°) 이라면 진질량은 ~8.2 M⊕ 로 — 여전히
슈퍼지구/서브-해왕성이며, 위 두 독법 사이에 있습니다. cfg 의 ~14 M⊕ 는
PMa 범위 안에 있고, 8.2 M⊕ 는 더 낮은-경사 가장자리입니다.

## Bibliography

### Read (drove decisions above)

- **Damasso M. et al. 2020** — *A low-mass planet candidate orbiting
  Proxima Centauri at a distance of 1.5 AU*, Sci. Adv. 6, eaax7467
  (`2020SciA....6.7467D`, doi:10.1126/sciadv.aax7467). **유일한 1차
  출처.** RV 후보. P = 1900 (+96/−82) d, a = 1.48 ± 0.08 AU,
  m sin i = 5.8 ± 1.9 M⊕, T_eq ≈ 39 (+16/−18) K, e 0 고정 (자유 런
  e = 0.41, 유의하지 않음). Gaia–Hipparcos PMa 가 진질량 ~10–20 M⊕ 와
  양립 (Kervella 2020 인용). 눈선 바깥 형성 → type-II 이주. 후속 관측이
  필요한 후보라고 명시. **arXiv 프리프린트 없음**. 전문은 오픈액세스
  PMC6962037 에서 캐시. 모든 궤도/질량/온도 행을 구동합니다.

### Read (context — dispute / non-recovery)

- **Suárez Mascareño A. et al. 2025** — NIRPS Proxima 캠페인
  (`2507.21751`). 1900-d 신호에 대해 **결론을 내릴 수 없는 증거**를 보고.
  ~1800 d 의 저진폭 (58 ± 28 cm/s, 99.7% 에서 < 1.4 m/s) 장주기 힌트로,
  Damasso 의 진폭과 "완전히 양립하지는 않음". "Proxima c 에 대한 결정적
  증거는 발견되지 않았다." 가장 최근 시험. 신뢰도 바닥을 낮춥니다.
- **Faria J. P. et al. 2022** — ESPRESSO Proxima d 발견
  (`2202.05188`). Proxima c 가 "지금까지 직접촬영이나 측성으로 명확한
  검출을 회피해왔다 (Gratton 2020; Kervella 2020; Benedict & McArthur
  2020)" 고 언급. ESPRESSO 의 ~815-d 베이스라인은 1900-d 신호를 시험하기엔
  너무 짧음 (P_c 의 ~2.3배 짧음) — 반박이 아니라 비시험.
- **Suárez Mascareño A. et al. 2020** — "Revisiting Proxima with
  ESPRESSO" (`2005.12114`). Proxima c 재시험은 (짧은-베이스라인) 논문의
  범위를 벗어난다고 명시. 비시험.
- **Artigau É. et al. 2022** (캐시에 없음; NIRPS 2025 경유) — 다른 RV
  방법을 쓴 HARPS 재추출이 Proxima c 의 **증거를 찾지 못함**. 핵심
  논쟁입니다.

### Not read — cited only, no full text in cache

- **Kervella P. et al. 2020** (Gaia–Hipparcos PMa 진질량) — ~10–20 M⊕
  진질량 범위의 출처로, Damasso 2020 을 통해 인용. 전문 미캐시.
- **Gratton R. et al. 2020** (SPHERE 직접촬영 짝) 과
  **Benedict & McArthur 2020** (HST 측성) — 둘 다 Proxima c 가 "명확한
  검출을 회피"한 사례로 인용. 논쟁적 Gratton SPHERE 후보는 널리 퍼진
  "고리" 이야기의 기원이지만 캐시-검증이 불가능하고 비검출로 규정됩니다.
- **Anglada G. et al. 2017** / **MacGregor M. et al. 2018** — 1–4 AU
  의 후보 ALMA 내부 먼지 고리와 그 반박 (ALMA 점광원을 항성 플레어로
  귀속). 항성주위 특징이며 논쟁적이고 행성 고리가 아닙니다.

## Open items for follow-up

- **존재 여부.** Proxima c 는 카탈로그에서 가장 논쟁적인 행성 항목입니다.
  확인하려면 지금 축적 중인 더 긴 RV 베이스라인 (ESPRESSO + NIRPS) 이나
  Gaia DR4 측성 검출이 필요합니다. 완전히 반박된다면 재분류해야 하고
  (강화된 tau Cet e 처럼), 확인되고 진질량이 고정되면 질량/반지름/본성
  행을 재유도해야 합니다.
- **질량과 본성.** 얼음-거인 vs 암석-슈퍼지구 갈림길
  (`## Canonical alternatives`) 은 전적으로 진질량에 달려 있습니다. Gaia
  DR4 측성이 이를 해결할 것입니다. 진질량이 5.8 M⊕ 최소값 부근으로
  나오면 cfg 는 암석 독법으로 전환해야 합니다.
- **이심률.** 원궤도 채택 (Damasso 가 e = 0 고정) 했으나, 자유-이심률
  런은 e = 0.41 (+0.34/−0.26) 을 줬습니다 — 진정으로 미제약. 후속 관측이
  지지하면 향후 cfg 가 적당한 이심률을 채택할 수 있습니다. 합성-이심률
  레이어 (프로젝트 정책) 는 여기 적용하지 **않습니다**. e 가 (느슨하게나마)
  측정된 양이기 때문입니다.
- **경사.** 미제약. 원반-공면 i ≈ 45° / m = 8.2 M⊕ 옵션이 하나의 문헌
  앵커입니다. 측정된 측성 경사가 궤도와 진질량을 모두 고정할 것입니다.
- **대기.** 전적으로 추론 (transit 도 스펙트럼도 없음). 메탄-블루
  얼음-거인 조성은 해왕성 유사체 기본값입니다. 현재 장비로는 1.48 AU 의
  비-통과 RV 후보에 대해 측정할 수 없습니다.

## Related

- [proxima-cen](proxima-cen.md) — 호스트별 Phase 3 합성. M5.5Ve Teff /
  L / 질량 / 반지름, 슈퍼플레어 맥락, 조명-색온도 기준을 제공
- [proxima-cen-b](proxima-cen-b.md) — 온화한 안쪽 암석 행성. b 의
  바다-가능 안구 세계를 c 의 차가운 얼음 거인과 대비
- [proxima-cen-d](proxima-cen-d.md) — 뜨거운 안쪽 수성 유사체.
  Proxima 계의 세 번째 일원
- [eps-ind-a-b](eps-ind-a-b.md) — 인근 왜성 주위 차가운 거대 행성 비교.
  ε Indi A b 의 질량 크고 내부열이 지배하는 슈퍼목성을 Proxima c 의
  작고 일사-차가운 얼음 거인과 대비
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — 이 얼음 거인의 대기 +
  오로라 결정을 소비하는 하류 Kopernicus / EVE cfg 작성기
