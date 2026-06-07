<!-- Alpha Centauri A b Phase 3 합성. cfg-ready 결정과 근거 -->
# α Centauri A b — Phase 3 Synthesis

α Centauri A b ("S1") 는 **JWST 직접 촬영 후보**입니다. 토성급 거대
행성의 점광원으로, 2024년 8월에 JWST/MIRI 의 F1550C 코로나그래프
(15.5 µm) 로 단 한 번 검출되었으며, 가장 가까운 태양형 별로부터 투영
이격 1.51″ (~2 AU) 지점에 있었습니다 (Beichman et al. 2025,
"Worlds Next Door I"; Sanghi & Beichman et al. 2025, "II"). 검출 신호는
어두워서 3.5 ± 1.0 mJy, S/N 4–6 (≈4σ) 수준이었고, 2025년 두 차례의
후속 관측에서는 **재검출되지 않았습니다**. 다만 궤도 피팅에 따르면
역학적으로 안정한 궤도의 ~52% 가 행성이 단순히 저감도 영역으로
이동했다는 설명과 양립합니다. 저자들은 S1 을 2019년 VLT/NEAR 후보
**C1** (Wagner et al. 2021) 과 동일한 천체로 연결하며, 검출기, PSF,
배경, 태양계 천체로 인한 설명을 배제합니다. 이것은 진짜이며 충분히
검증된 **후보**로서, NearStars 에는 문서화된 후보로 포함됩니다
(tau Cet e / 40 Eri A b 패턴). 태양 쌍둥이 별 주위에서 가장 가까운
후보 가스 행성입니다.

모든 물리량은 **두 개의 중적외선 측광점과 하나의 궤도 패밀리로부터
모델로 유도된 값**이며, 측정된 것이 아닙니다. 궤도는 네 개의 안정한
패밀리 — {순행, 역행} × {a < 2 AU, a > 2 AU} — 로 나뉘고, 이심률
e ≈ 0.4, 주기 2–3 년입니다. 저자들은 **a < 2 AU 패밀리** (a ≈ 1.6 AU,
T_eq ≈ 225 K) 를 선호하는데, 더 높은 온도가 F1550C 밝기에 더 잘 맞기
때문입니다. 질량은 **토성급 90–150 M⊕** 로, RV 상한 (Zhao et al. 2018)
을 존중하기 위해 log g 2.5–3.0 으로 제한한 대기 피팅에서 정해집니다.
선호되는 대기는 차갑고 (~225 K) 금속이 농축된 ([M/H] +0.5 ~ +1.0) H₂/He
거대 행성으로 **물 구름**을 가집니다. 이 온도에서는 암모니아가 비로
씻겨 내려가고 물이 응결종이 되며, 따라서 α Cen A b 는 Sudarsky Class
I/II 물-구름 경계 근처에 놓입니다.

발견 논문은 같은 밝기에 대해 인상적인 대안을 하나 제시합니다.
**더 작은 (~1 R_Jup, ~120 M⊕) 행성이 광학적으로 두꺼운 환주 고리로
둘러싸였다는 해석** (Beichman §5.3) 입니다. 단면적 ~64 000 km
(≈ 0.9 R_Jup, 토성 고리 폭의 약 절반) 의 고리가 로슈 영역 (행성 반지름
의 1.4–2.5 배) 안에 ~209–257 K 로 자리하며, 소행성과 유사한 어두운
알베도를 가집니다. 이 고리 해석은 **논문에 근거한 것** (지어낸 것이
아님) 이고, 가장 가까운 태양형 별 주위의 고리 두른 거대 행성이 더
독특한 렌더이기 때문에, cfg 는 이 해석을 채택합니다.

**NearStars 시나리오 선택. G2V 태양 쌍둥이 α Centauri A 주위에서
이심 궤도 (e ≈ 0.4) ~1.6 AU 를 도는 온화한 (~225 K) 토성급 가스 행성으로,
어둡고 광학적으로 두꺼운 암석 고리에 둘러싸인 단일-관측 JWST 후보이며,
가깝고 이심한 α Cen AB 쌍성계 안에 상호 경사 ~50° 로 놓여 있습니다.**
궤도 패밀리, 질량, 온도, 물-구름 대기는 논문이 선호하는 해이며
canonical 과 정렬됩니다. 고리 (고리 없는 1.1 R_Jup 팽창 거대 행성 대신),
옅은 구름 색조, 자전, obliquity 는 tie-break 입니다. 고리 없는 해석은
`## Canonical alternatives` 에 보존됩니다.

## Decisions

Kopernicus / atmosphere cfg-ready 값입니다. `Confidence`. high = 직접
측정되었거나 강하게 제약됨, medium = 강한 근거를 갖춘 이론, low =
허용 범위 내의 미적 선택. 전체 하한선. 이 행성은 **확인되지 않은
단일-관측 후보**이므로, "high" 행도 행성의 존재와 선호 궤도 패밀리를
전제로 합니다.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 1.1 M☉ 별 주위 ~1.6 AU 궤도. 조석 시간이 5.3 Gyr 나이를 훨씬 초과하므로 spin-orbit 결합 없음 |
| `eccentricity` | 0.4 | medium | Beichman et al. 2025. 안정한 궤도 패밀리들이 네 해 전반에 걸쳐 e ≈ 0.33–0.46 으로 모임. 대표값 0.4 |
| `semi_major_axis_au` | 1.6 | medium | Beichman et al. 2025 §5.3. **a < 2 AU 패밀리가 선호됨** (더 높은 T_eq 가 F1550C 에 맞음). a ≈ 1.58–1.68 AU. Phase 2 DB 대표값을 1.9 AU 에서 1.6 AU (P 705 d) 로 조정해 이 선호 패밀리에 맞췄으므로, 인게임 궤도가 합성을 따름 |
| `sidereal_period_yr` | ~2.0 | medium | Beichman et al. 2025. 2–3 년 범위. 선호되는 a ≈ 1.6 AU / 1.1 M☉ 에 대해 ~2 년 |
| `mutual_inclination_deg` | 50 | medium | Beichman et al. 2025 (Table 4). α Cen AB 궤도면 (i_AB = 79.24°) 에 대한 경사. 순행 패밀리 ≈ 49–70°, 대표값 50°. 깨끗하고 물리적으로 의미 있는 경사 |
| `inclination_deg` | ~55 (bimodal, weak) | low | Tie-break. 시선 방향 경사는 bimodal (≈ 55° 또는 ≈ 124°, 패밀리 의존. Beichman Table 4) 이라 단일하고 깨끗한 값이 아님. cfg 는 순행 ~55° 를 대표 궤도 기울기로 사용 |
| `mass_mearth` | 120 | medium | Beichman et al. 2025. 토성급 90–150 M⊕ (토성 = 95). 고리 모델 해 ~120 M⊕. RV 한계 (Zhao 2018: P ≲ 1000 d 에서 M sin i < 100 M⊕) 를 존중하기 위해 대기 피팅을 log g 2.5–3.0 으로 제한 |
| `mass_mjup` | 0.38 | medium | = 120 M⊕ / 317.8 |
| `radius_rjup` | 1.0 | low | Tie-break. **고리 모델** 반지름 (Beichman §5.3). 고리 없는 대기 피팅은 ~1.1–1.15 R_Jup (5 Gyr 거대 행성치고 팽창). cfg 는 1.0 R_Jup 을 채택하고 추가 단면적은 고리가 담당 |
| `radius_rearth` | 11.2 | low | = 1.0 R_Jup |
| `surface_gravity_g_earth` | ~0.96 | low | 유도. g = M/R² = 120/11.2² ≈ 0.96 g⊕ (log g ≈ 2.97 cgs). 논문이 가정한 log g 2.75–3.0 과 일관 |
| `density_g_cc` | ~0.5 | low | 유도. 120 M⊕ 가 1.0 R_Jup 구에 들어가면 ≈ 0.47 g/cc. 저밀도 토성급 거대 행성 (참고: 토성 0.69) |
| `insolation_s_earth` | 0.59 | medium | 유도. S = L/a² = 1.521 L☉ / (1.6 AU)² ≈ 0.59 S⊕ (비선호 a ≈ 2.1 AU 패밀리면 ≈ 0.34 S⊕). 외곽 거주 가능 영역 (EEID ≈ 1.23 AU) 너머. 온화한 세계가 아니라 차가운 거대 행성 |
| `equilibrium_temp_k` | 225 | medium | Beichman et al. 2025. 선호되는 a < 2 AU 패밀리에 대해 A_B = 0.3, f = 1 의 플럭스 평균 T_eq (a > 2 AU 면 ~195 K). 재계산: a = 1.6 AU 에서 278.3 × (L/a²)^0.25 × 0.7^0.25 ≈ 224 K 로 일관 |
| `effective_temp_k` | ~225 | medium | Beichman et al. 2025. 내부열 무시 가능 (T_int < 110 K, 목성/토성 아날로그). 복사 온도 ≈ 평형 온도로, 자체발광하는 ε Indi A b 와 다름 |
| `bond_albedo` | 0.30 | medium | Beichman et al. 2025. T_eq 유도를 위해 뜨거운 목성형과 태양계 거대 행성 사이의 중간값으로 가정 |
| `atmosphere_present` | true | high | 가스 행성. 금속 농축과 물 구름을 동반한 H₂/He 본체 (Beichman 모델 피팅) |
| `atmosphere_reference_pressure_pa` | 100000 | medium | 가스 행성은 고체 표면이 없음. 구름층 렌더링용 1 bar cfg 기준 |
| `atmosphere_composition` | H₂/He 본체. 금속 농축 [M/H] +0.5 ~ +1.0. **H₂O 가 응결 구름종** (225 K 에서 NH₃ 는 비로 씻김). rainout 화학의 CH₄/NH₃/H₂O | medium | Beichman et al. 2025. C/O 는 피팅 의존. §5.2 의 흐린 물-구름 피팅에서는 태양의 2.5배 (Sonora Flame Skimmer / PICASO, log g 2.75, K_zz 10⁹, f_sed 6), 채택된 고리와 짝지은 §5.3 의 맑은 모델에서는 1.5배. 태양 금속도 및 더 뜨거운 (≥250 K) 모델은 측광을 통과하지 못함. cfg 는 225 K 에서 물리적으로 예상되는 데크로 물 구름을 렌더 |
| `atmosphere_tint_rgb_hex` | `#dfe3e8` (옅은 차가운-흰 물-구름 거대 행성) | low | Tie-break. 가시광 데이터 없음 (중적외선 두 점뿐). Sudarsky Class I/II 경계 근처의 ~225 K 물-구름 거대 행성은 밝고 옅으며 고알베도 천체로 읽힘. 목성의 따뜻한 크림색과 구별되며, G2V (5847 K) 빛에서 옅은 따뜻한 편향 |
| `cloud_cover_fraction` | 0.9 | low | Tie-break. 차가운 물-구름 데크 (f_sed 6 ⇒ 적당히 조밀한 구름). Class II 거대 행성에 전형적인 높은 덮임. 측정 없음 |
| `cloud_morphology` | 옅은 zonal banding 을 동반한 거의 전역적인 옅은 물-구름 데크. 차가운 Class-I/II 거대 행성으로 목성보다 더 균일하고 밝음 | low | Tie-break. Beichman 물-구름 최적 피팅에서 스케일. 금속 농축을 동반한 225 K 에서 적당한 belt-zone 대비 |
| `cloud_tint_rgb_hex` | `#eef1f4` (거의 흰 물 구름) | low | Tie-break. 물 구름은 본질적으로 거의 흰색. G2V 빛 아래 데크는 밝고 옅은 흰색으로 읽히며 limb 보다 밝음 |
| `rotation_period_hours` | 10 | low | Tie-break. 측정 없음. 토성/목성 아날로그 ~10 h. Beichman §5.3 은 1.1 R_Jup 대기 피팅이 거의 pole-on 으로 본 빠른 자전을 시사할 수 있다고 언급하며, 이는 빠른 spin 과 일관 |
| `obliquity_deg` | 27 | low | Tie-break. 고리면과 자연스럽게 읽히는 시각적으로 구별되는 기울기를 위해 토성 아날로그 26.7° 채택. 측정 없음 |
| `ring_present` | true | low | **문서화된 발산** (Canonical alternatives 참조). Beichman et al. 2025 §5.3 은 F1550C 밝기에 대한 동등한 설명으로 광학적으로 두꺼운 환주 고리를 제시. 논문에 근거 (고리 가드레일 통과). cfg 는 더 독특한 렌더로 이를 선택 |
| `ring_inner_radius_bodyradii` | 1.4 | low | Beichman §5.3. 고리는 로슈 영역, 행성 반지름의 ~1.4–2.5 배에 자리. Kopernicus `Ring` innerRadius 는 body-radius 배수 |
| `ring_outer_radius_bodyradii` | 2.5 | low | Beichman §5.3. 로슈 영역 외곽 가장자리. 단면적 ~64 000 km ≈ 0.9 R_Jup, 토성 고리 폭의 약 절반 |
| `ring_color_hex` | `#6e6253` (어두운 따뜻한 회색 — 암석/먼지, 저알베도) | low | Tie-break. Beichman §5.3 은 고리에 소행성과 유사한 본드 알베도 A_B ≈ 0.1 을 가정 → **어둡고 암석/먼지질 고리**로, 토성의 밝은 얼음이 아님. 고리 T ≈ 209–257 K |
| `ring_opacity` | 0.85 | low | Beichman §5.3. "광학적으로 두꺼운" 고리 (밝기에 맞추기에 충분한 단면적을 더하는 것이 핵심) |
| `ring_observed` | false | high | 고리는 F1550C 밝기에 대한 **모델 해석**이며 분해된 것이 아님. S1 은 분해되지 않은 점광원 |
| `magnetic_field_strength_microtesla_equator` | 500 | low | Tie-break. 토성질량 거대 행성을 위한 토성 아날로그 dynamo (~500 µT 급). 측정 없음 |
| `aurora_present` | false | medium | 1.6 AU 의 조용한 G2V 항성풍 (log R'HK = −4.95) 은 약한 플라스마 구동체. 다른 조용한 호스트 거대 행성들처럼 강한 오로라는 기대되지 않음. cfg 는 렌더하지 않음 |
| `star_apparent_angular_diameter_deg` | 0.41 | high | 유도. 2 R_star / a = 2 × 1.2234 R☉ / 1.6 AU ≈ 0.41° — 지구에서 본 태양 (0.53°) 보다 약간 작음. 이심 궤도에서 변동. 근일점 (0.96 AU) ~0.68°, 원일점 (2.24 AU) ~0.29° |
| `stellar_illumination_color_temp_k` | 5847 | high | 호스트 Phase 3 에서 상속 (`docs/phase3/alpha-centauri-a.md`). G2V, 거의 흰 따뜻한 햇빛 |
| `companion_stars_in_sky` | α Cen B (K1V) 11.2–35.6 AU. Proxima (M5.5Ve) ~13 000 AU | high | Akeson et al. 2021 / Kervella 2017. 이심한 K형 왜성 동반성은 눈부신 두 번째 "태양". Proxima 는 희미한 붉은 점 |

## Surface synthesis

α Centauri A b 는 고체 표면이 없습니다. ~120 M⊕ 토성급 H₂/He 거대
행성입니다. 렌더링에서 "표면"은 구름 데크이며, ~225 K 에서 그 데크는
물이 결정합니다.

온도 영역이 팔레트의 핵심입니다. 1.521 L☉ G2V 별 주위 1.6 AU 에서
평형 온도는 선호 궤도 패밀리에 대해 ~225 K 입니다 (Beichman 2025.
A_B = 0.3 에서 재계산하면 ≈ 224 K). 이것은 목성 (~165 K) 과 토성
(~134 K) 보다 따뜻하며, **암모니아가 비로 씻겨 내려가고** **물이
응결 구름종**이 될 만큼 따뜻하여 α Cen A b 를 Sudarsky Class I/II 경계
근처에 놓습니다. 이 영역의 물-구름 거대 행성은 밝고 옅으며 고알베도이므로,
cfg 는 이 천체를 옅은 zonal banding 만 있는 **옅은 차가운-흰 세계**
(`#dfe3e8` 대기, `#eef1f4` 구름) 로 렌더합니다 — 목성의 따뜻한
크림-호박색과 구별됩니다. 금속 농축 ([M/H] +0.5 ~ +1.0, C/O ~태양의
2.5배. Beichman §5.2) 과 적당한 구름 조밀도 (f_sed 6) 는 적당한
belt-zone 대비를 남겨, 목성보다 밝고 더 균일합니다.

내부열이 무시할 만하므로 (T_int < 110 K. Beichman §5.1), 외관은
**일사로 결정됩니다** — 자체발광하는 슈퍼-목성 ε Indi A b 와 달리,
α Cen A b 는 별빛이 데우는 만큼만 따뜻하게 빛납니다. e ≈ 0.4 궤도는
행성을 ~0.96 AU (근일점) 에서 ~2.24 AU (원일점) 까지 흔들어 ~4배의
일사 범위를 만들므로, 구름 데크는 근일점 근처에서 밝아지고 banding 이
선명해질 가능성이 큽니다 — ~2 년 주기의 계절 순환입니다.

대표적인 시각 요소는 **고리**입니다. Beichman §5.3 을 채택하면,
α Cen A b 는 로슈 영역 (행성 반지름의 1.4–2.5 배) 에 어둡고 광학적으로
두꺼운 암석 고리를 두르고 있으며, 단면적은 ~0.9 R_Jup — 토성 고리 폭의
약 절반입니다. 소행성과 유사한 알베도 (A_B ≈ 0.1) 와 ~209–257 K 의
온도로, 이것은 토성의 눈부신 얼음이 아니라 **어두운 먼지질 고리**
(`#6e6253`) 입니다 — 옅은 거대 행성을 두른 음울한 먼지색 띠입니다.

## Atmosphere synthesis

**압력 기준.** 가스 행성은 고체 표면이 없습니다. cfg 기준 압력은
1 bar (100 000 Pa) 로, 구름 데크 렌더를 고정합니다. 물리적으로 의미
있는 층은 물-구름 상단입니다.

**조성.** 여느 거대 행성과 마찬가지로 본체는 H₂/He 입니다. 두 중적외선
점에 맞는 Beichman 2025 대기 피팅은 **금속 농축** ([M/H] +0.5 ~ +1.0)
과 차가운 ~225 K 프로파일을 요구하며, 그 안에서 암모니아, 메탄, 물이
rainout 화학에 있습니다 — 225 K 에서 암모니아는 가시 데크 아래로
응결/씻겨 내려가고 **물이 응결 구름종**이 됩니다. C/O 비는 피팅
의존적입니다. §5.2 의 흐린 물-구름 피팅은 C/O ~태양의 2.5배를 쓰고,
채택된 고리와 짝지은 §5.3 모델은 C/O 1.5배, [M/H] +1.0 의 맑은
대기입니다. 태양 금속도 및 더 뜨거운 (≥250 K) 모델은 측광을 통과하지
못했으므로, 금속이 풍부한 해석이 논문이 선호하는 피팅입니다. cfg 는
225 K 에서 물리적으로 예상되는 데크로 물 구름을 렌더하고 조성을 medium
신뢰도로 인코딩합니다 (모델 제약. 정확한 혼합비는 그보다 덜 제약).

**구름 상단 / 위성 관측자에서 본 하늘.** 구름 상단에서 하늘은 거의
태양 같은 별이 비추는 밝고 옅은 흰 흐린 하늘입니다. α Cen A 는
1.6 AU 에서 ~0.41° 를 가립니다 — 우리 태양보다 약간 작고, 근일점에서
~0.68°, 원일점에서 ~0.29° 로 흔들립니다 — 따뜻한 흰 G2V 원반
(`#fff4e8`) 이 지구 일사의 ~0.6배를 전달합니다. 어두운 고리는 별빛에
가장자리가 비추는 먼지 띠로 하늘을 가로질러 호를 그립니다. 시스템의
볼거리는 **동반성**입니다. K1V 별 α Cen B 는 AB 무게중심을 e ≈ 0.52
경로로 11.2 에서 35.6 AU 까지 돌므로, α Cen A b 에서 보면 눈부신 주황색
두 번째 "태양"입니다 — 최근접에서 보름달보다 수백 배 밝지만 결코 진짜
원반은 아닌 강렬한 점입니다. 그 너머로 Proxima 가 ~13 000 AU 에 희미한
붉은 점으로 걸려 있습니다.

**밤면.** 내부열이 무시할 만하므로 밤면은 어둡고 차갑습니다 (~225 K,
JWST 가 검출한 중적외선 대역에서 복사). 조용한 G2V 항성풍은 약한
플라스마 구동체이므로, 카탈로그의 플레어-호스트 거대 행성들과 달리
유의미한 오로라는 렌더하지 않습니다 (`aurora_present = false`).

## Rotation & spin synthesis

α Centauri A b 의 자전 측정은 존재하지 않습니다 — 단일-에포크 촬영
후보입니다.

**조석 감쇠 논증.** 1.1 M☉ 별 주위 ~1.6 AU 에서, 토성급 거대 행성의
조석 시간은 5.3 Gyr 나이를 크게 초과하므로, α Cen A b 는 조석 고정되어
있지 **않습니다** (`tidally_locked = false`).

**자전 주기 선택.** cfg 는 토성/목성 아날로그 `rotation_period_hours
= 10` 을 채택하며, 범위 내 tie-break 입니다. Beichman §5.3 은 1.1 R_Jup
대기 전용 반지름이 성숙한 거대 행성치고 비정상적으로 팽창한 값이 되는데,
**빠르게 자전하며 거의 pole-on 으로 보는** 경우라면 가능하다고
언급합니다 — 이것이 cfg 가 채택한 더 작은 고리 모델의 동기 중 하나이며,
빠른 ~10 h spin 과 일관됩니다.

**Obliquity.** Tie-break 미학. 고리면과 자연스럽게 읽히는 시각적으로
구별되는 기울기를 위해 27° (토성 아날로그) 채택. 고리는 이 obliquity 에서
행성의 적도면에 렌더됩니다.

**KSP 구현 노트.** 자전 주기 = 10 h = 36 000 s
(`rotationPeriod = 36000`). obliquity ≈ 27° (궤도 법선 기준), `Ring`
블록은 적도면을 공유합니다.

## Visual styling

표면 (구름 데크), 대기, 고리 결정을 종합하면, α Cen A b 는 옅고 고리를
두른 온화한 토성급 거대 행성으로 렌더됩니다 — 태양 쌍둥이 별 주위에서
가장 가까운 후보 가스 행성입니다.

- **전역 외관.** 궤도에서 보면 폭 약 1.0 R_Jup (~71 000 km) 의 옅은
  차가운-흰 원반 (`#dfe3e8`) — 밝고 고알베도로 (Class I/II 경계 근처의
  물 구름) 렌더된 토성질량 세계로, 목성의 따뜻한 크림-호박색과 의도적으로
  구별됩니다.
- **구름 데크 디테일.** 옅은 zonal banding (`#eef1f4` 구름) 과 적당한
  belt-zone 대비를 동반한 거의 전역적인 옅은 물-구름 데크 (~90% 덮임)
  — 목성보다 밝고 더 균일하며, 일사가 정점에 달하는 근일점 근처에서
  선명해집니다.
- **고리.** 로슈 영역 (행성 반지름의 1.4–2.5 배) 에 있는 어둡고 먼지질
  이며 광학적으로 두꺼운 암석 고리 (`#6e6253`), 단면적 ~0.9 R_Jup (~토성
  폭의 절반), ~209–257 K 에 소행성과 유사한 저알베도 — 토성의 눈부신
  얼음이 아닌 음울한 띠입니다. 27° obliquity 로 기울어져 있습니다.
- **Limb.** 옅고 밝은 물-구름 limb. 얇고 거의 흰색입니다.
- **밤면.** 어둡고 차가움. 유의미한 오로라 없음 (조용한 G2V 항성풍).
- **하늘의 별.** α Cen A 는 ~0.41° (근일점 ~0.68°, 원일점 ~0.29°) 를
  가립니다 — 따뜻한 흰 G2V (`#fff4e8`) 근거리 태양으로, 지구 일사의
  ~0.6배입니다.
- **동반성 태양들.** α Cen B (K1V) 는 e ≈ 0.52 궤도에서 11.2 에서
  35.6 AU 까지 휩쓸고 지납니다 — 눈부신 주황색 두 번째 태양으로 근일점
  에서 강렬합니다. 그 너머로 Proxima (M5.5Ve) 가 ~13 000 AU 에 희미한
  붉은 점입니다. 쌍성 배경은 이 행성의 시그니처입니다. 가깝고 밝은
  두-별 (게다가 먼 붉은 별) 하늘 속의 이심한 S-type 거대 행성입니다.

## Canonical alternatives

cfg 는 **고리 두른** 해석을 렌더합니다. Beichman et al. 2025 §5.3 은
같은 F1550C 밝기에 대한 동등한 고리 없는 해석을 제시합니다.

| cfg pick | Canonical alternative | Why cfg diverges |
|---|---|---|
| `ring_present = true`, `radius_rjup = 1.0` (더 작은 행성 + 광학적으로 두꺼운 어두운 고리) | **고리 없는 팽창 거대 행성: `radius_rjup ≈ 1.1–1.15`, 고리 없음** — 대기 전용 최적 피팅 (Beichman §5.2). 더 큰 반지름 단독으로 F1550C 밝기를 만드는 단면적을 공급 | 둘 다 Beichman 이 데이터에 동등하게 맞는다고 명시적으로 제시. §5.3 은 1.1 R_Jup 이 "더 뜨거운 행성에서 더 흔히 관측된다"고 언급하며, 성숙한 거대 행성에서는 빠르게 자전 / pole-on 인 경우에만 그럴듯하다고 보아 고리 대안의 동기가 됨. cfg 는 시각적 독특함 (interesting-first) 을 위해 고리를 선택하는데, 논문에 근거하며 더 인상적인 렌더이기 때문. 보수적 해석을 선호하는 사용자는 `ring_present = false` 와 `radius_rjup = 1.1` 로 설정 |

논문 내부의 두 번째 분기점은 **궤도 패밀리**입니다. cfg 는 선호되는
a < 2 AU 패밀리 (a ≈ 1.6 AU, T_eq ≈ 225 K) 를 씁니다. a > 2 AU 패밀리
(a ≈ 2.1 AU, T_eq ≈ 195 K) 는 허용되지만 비선호입니다 (더 낮은 T_eq 가
F1550C 밝기에 덜 맞음). Phase 2 DB 궤도는 이제 선호되는 a ≈ 1.6 AU
패밀리로 설정돼 있습니다 (이전 1.9 AU 중간값에서 조정함).

## Bibliography

### Read (drove decisions above)

- **Beichman C. et al. 2025** — *JWST Observations of the Nearest Sun-Like
  Stars: Worlds Next Door I* (`2025ApJ...989L..22B`,
  doi:10.3847/2041-8213/adf53f, arXiv:2508.03814). 발견 논문.
  S1 = F1550C (15.5 µm) 검출, 3.5 ± 1.0 mJy, 1.51″ (~2 AU), 2024년 8월.
  네 개의 안정한 궤도 패밀리 (e ≈ 0.4, P 2–3 년, 상호 i ≈ 50°/130°),
  a < 2 AU 선호. 질량 90–150 M⊕. T_eq ≈ 225 K. 금속이 풍부한 물-구름
  대기 피팅. **§5.3 의 고리 대안** (~1 R_Jup + 광학적으로 두꺼운 고리,
  로슈 영역, A_B ≈ 0.1). 핵심 근거 — 궤도, 질량, 온도, 대기, 고리 행을
  견인.
- **Sanghi & Beichman et al. 2025** — *Worlds Next Door II*
  (arXiv:2508.03812). 검출 검증 + 궤도 역학 논문.
  S/N 5.4 (≈4σ) PCA-KLIP 검출. 검출기 / ε Mus PSF /
  α Cen B speckle / 배경 / 태양계 천체 설명을 배제. S1 을 2019년
  VLT/NEAR **C1** (Wagner et al. 2021) 과 연결. 안정 궤도의 ~52% 가
  2025년 비재검출과 양립. 검출 상태 프레이밍과 후보 플래그를 견인.

### Read (context / instrument-only, not decision-driving)

- **Wagner K. et al. 2021** (VLT/NEAR, 인용) — 2019년 **C1** 후보
  (11.25 µm, 1.2 ± 0.4 mJy, ~1.1 AU). 원래는 ≳300 K 행성
  (반지름 ≳ 3.3 R⊕) 또는 60-zodi 먼지 덩어리로 읽혔으나,
  JWST exozodi 비검출이 행성 해석을 선호하며 S1+C1 은 하나의 천체로 취급.
- **Zhao et al. 2018** (인용) — α Cen A RV 상한 (P ≲ 1000 d 에서
  M sin i ≲ 100 M⊕) 으로 질량을 한정. α Cen A b 는 이를 존중하도록 구성.
- **Akeson R. et al. 2021** (인용) — 상호 경사를 시선 방향으로 변환하는
  데 쓰인 α Cen AB 궤도 (i_AB = 79.24°, Ω_AB = 205.07°).

### Not read — no arXiv full text / superseded

- 대기 피팅의 기반이 되는 PICASO / Sonora Flame Skimmer / ATMO2020++
  모델 그리드는 이미 인용된 최적 피팅 파라미터를 위해 읽었으나 추가
  cfg 수치를 제공하지 않음. 유사 시스템 참조 (HD 196885 Ab, γ Cep Ab
  — 가깝고 이심한 쌍성계의 S-type 행성) 는 아키텍처를 틀짓지만 행성별
  시각 필드를 추가하지 않음.

## Open items for follow-up

- **존재 / 재검출.** S1 은 2025년에 재검출되지 않은 단일-관측 검출입니다.
  확인을 위해서는 검출 가능 이격 범위로 돌아온 행성을 포착하는 JWST
  에포크 (다음 유리한 에포크에서 궤도의 ~52% 가 재검출 예측) 나 독립적인
  촬영 검출이 필요합니다. 반증되면 엔트리는 재분류되어야 합니다.
- **DB 장반경 (해결됨).** Phase 2 DB 궤도는 원래 a = 1.9 AU (P = 2.5 년)
  를 썼는데, 이는 **비선호** a > 2 AU 패밀리 쪽으로 기우는 중간값이었습니다.
  저자들이 선호하는 a ≈ 1.6 AU / P 705 d (T_eq ≈ 225 K) 로 조정해 인게임
  궤도가 이 합성과 일치하도록 했습니다. a > 2 AU 패밀리 (a ≈ 2.1 AU) 는
  비선호 대안으로 본문에만 남겨 둡니다.
- **동역학 안정성 (Kozai-Lidov) — 궤도 패밀리에 따라 달라짐.** REBOUND/TRACE
  안정성 시뮬 (`phase3/stability-sim`, `STABILITY_REPORT.md` 참고) 결과, AB
  면에 대해 상호경사 ~50° 인 favored prograde a ≈ 1.6 AU 패밀리는 **Kozai-Lidov
  불안정**입니다. eccentric KL 이 수천 년 안에 e 를 ~0.998 까지 끌어올려
  근일점이 별 반경 수준까지 추락합니다 (조석 파괴). 여기 시각 / 대기 합성은
  그 favored 구성을 전제하므로 조건부입니다. 상호경사 스윕 결과 Beichman 4개
  패밀리 중 3개는 생존하며 (retrograde 내측 + a ≈ 2.1 AU 양쪽 모두 e_max ≲ 0.88),
  안정 경사대는 i_mut ≲ 30° 또는 ≳ 110° 입니다. A b 가 실재한다면 생존 여부 —
  나아가 이 천체를 실제로 넣을지 — 는 어느 패밀리에 속하는지에 달려 있습니다.
- **고리 대 팽창 반지름.** 고리 (`ring_present = true`) 와 고리 없는
  1.1 R_Jup 거대 행성은 동등한 논문 해석입니다
  (`## Canonical alternatives`). 분해된 영상이나 NIRCam 4–5 µm 측정
  (맑은 모델 대 흐린/고리 모델을 분리) 이 이를 판가름할 것입니다.
- **대기 ingest.** α Cen A b 는 DB 에 Phase 2 대기 블록이 없습니다
  (궤도 + 물리량만). 스키마가 확장되면 Beichman 2025 금속이 풍부한
  물-구름 최적 피팅을 여기 cfg pick 에 맞춰 `atmosphere_measurements`
  로 ingest 해야 합니다.
- **자전 / obliquity.** 둘 다 범위 내 tie-break (10 h, 27°) 이며,
  어떤 측정으로도 제약되지 않습니다.

## Related

- [alpha-centauri-a](alpha-centauri-a.md) — 호스트 별 Phase 3 합성.
  G2V Teff / L / R / 질량 / 나이, 쌍성 이벤트 기하, 조명-색온도 기준을
  제공. (그 인트로는 후보를 "확인되지 않음"으로 언급 — 이 행성 수준
  합성보다 앞섬.)
- [alpha-centauri-b](alpha-centauri-b.md) — K1V 동반성. α Cen A b 의
  하늘에서 눈부신 두 번째 태양
- [proxima-cen-c](proxima-cen-c.md) — 이 삼중계의 또 다른 새 후보.
  Proxima c 의 차가운 얼음 거대 행성을 α Cen A b 의 온화한 고리 두른
  토성급 거대 행성과 대조
- [eps-ind-a-b](eps-ind-a-b.md) — 가까운 왜성 주위의 비교 거대 행성.
  ε Indi A b 의 무거운 자체발광 슈퍼-목성을 α Cen A b 의 더 가벼운,
  일사로 결정되는, 고리 두른 온화한 거대 행성과 대조
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — 이 거대 행성의 대기 +
  고리 결정을 소비하는 하류 Kopernicus / EVE / Scatterer cfg 작성기
