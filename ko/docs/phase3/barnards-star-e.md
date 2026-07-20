<!-- Barnard's Star e Phase 3 합성. 4행성 중 가장 차갑고 가장 가벼운 외곽 sub-Earth, 얇은 CO2 secondary 시나리오 -->
# Barnard's Star e — Phase 3 Synthesis

Barnard's Star e 는 시스템에서 가장 바깥이며 가장 가벼운 4개 확정
sub-Earth 행성으로, 0.0381 AU 의 6.74-일 궤도에서 Msini = 0.193 ±
0.033 M⊕ 입니다. González Hernández 2024 ESPRESSO 데이터에서 가장
약한 후보였고, Basant 2025 가 공동 분석에 112 개의 MAROON-X RV 를
추가한 후에야 확정 상태로 격상되었습니다 — e analog 의 공동 피팅
검출 확률은 (ESPRESSO 단독) 59% 에서 (공동) 79% 로 상승해 정식 확인
임계값을 넘었습니다. 0.19 M⊕ 로 Proxima d 와 함께 RV 로 검출된 가장
가벼운 행성의 자리를 나눕니다.

지구의 2.45× 일사에서, e 는 네 행성 중 가장 차가우며 평형 온도 340
K (Basant 2025 Table 3, A = 0, 완전 열재분배) — 금성의 232 K 에 가까
우며 어떤 액체 물 거주 가능 임계값보다 한참 위입니다. Kopparapu
2014 보수적 HZ 안쪽 가장자리는 Barnard 의 M4 V 호스트에 대해 P ≈
10 d (a ≈ 0.05 AU) 에 있으며, e 는 6.74 d (0.0381 AU) 에서 그 경계
바로 안쪽에 자리합니다 — 네 행성 중 HZ 에 가장 가깝지만 여전히 폭주
온실 매개변수 공간에 단단히 위치합니다. cfg 는 e 를 경계선 금성
analog 로 해석합니다 — XUV-구동 escape 를 통해 10 Gyr 에 걸쳐 어떤
1차 물 대기도 잃기에 충분히 뜨겁지만, France 2020 의 손실 속도에
대해 모데스트한 2차 CO₂ 대기가 plausible 하게 유지될 수 있는 네 중
유일한 것입니다.

궤도 이심률은 e = 0.04 (−0.03/+0.04) (Basant 2025 β-prior). 원과 일관
합니다. 안정성은 장기 4-행성 공존을 위해 e < 0.02 를 요구합니다
(SPOCK 분석 당). 6.74-일 주기는 조석 despinning 시간 척도를 10 Gyr
시스템 나이보다 한참 아래 (대부분의 plausible 한 암석 rheology 에서
10³–10⁶ 년. Walterová 2020) 에 두므로 동기 spin-orbit 구성이 예상됩
니다. c 와의 궤도 주기 비 (6.739 / 4.124 = 1.634) 는 5:3 mean-motion
공명에 가깝지만 정확하지는 않습니다.

**NearStars 시나리오 선택. 가능한 대기 유지 윈도우의 안쪽 가장자리에
있는 조석잠금 sub-Earth 질량 암석 행성입니다 — 네 형제 중 가장 차가운
(T_eq = 340 K) 으로, b/c/d 에 사용된 노출 암석 기준선에 대한 tie-break
업그레이드로 plausible 한 얇은 CO₂ 우위 2차 대기를 가집니다. 시각적
으로 미세한 Rayleigh 헤이즈가 있는 더 어둡고 더 차가운 톤의 노출 암석
세계.** 34 cfg 픽. 16 canonical-aligned, 18 tie-break. 노출 암석 대신
얇은 대기를 선택한 것이 네 행성 중 가장 흥미로운 tie-break 입니다.
문서화된 divergence 없음.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 6.74-d 궤도 → despin ≪ 10 Gyr 나이 (Walterová 2020) |
| `obliquity_deg` | 0 | high | 조석 감쇠 |
| `eccentricity` | 0.04 | medium | Basant 2025 β-prior 피팅 (−0.03/+0.04). 원과 일관 |
| `sidereal_period_days` | 6.7392 ± 0.0028 | high | Basant 2025 |
| `semi_major_axis_au` | 0.0381 ± 0.0005 | high | Basant 2025 |
| `argument_of_periapsis_deg` | −27.5 | low | Basant 2025 (낮은 ecc → 약한 제약, −96.1/+137.5) |
| `epoch_jd` | 2460245.3 | high | Basant 2025 t_peri |
| `mass_mearth` | 0.193 ± 0.033 | high | Basant 2025 Msini. RV 최저 질량 행성으로 Proxima d 와 동률 |
| `radius_rearth` | 0.64 | medium | Tie-break. 비-transit. 0.19 M⊕ 지구 analog 암석의 질량-반지름 → 0.58–0.69 R⊕. interesting-first 가 0.64 선택 (DB 질량-반지름 = 0.637) |
| `surface_gravity_g_earth` | 0.47 | medium | 유도 = 0.193 / 0.64² = 0.471 |
| `density_g_cc` | 4.0 | medium | Tie-break. 네 중 가장 낮은 밀도 (질량-반지름 기울기, 5.513·0.193/0.64³ ≈ 4.06). 약간 휘발성-농축 가능 |
| `insolation_s_earth` | 2.45 | high | L = 0.003558 L☉ 와 a = 0.0381 AU 로 유도 (L/a² = 2.451) |
| `equilibrium_temp_k` (A=0, full redistribution) | 340 | high | Basant 2025 Table 3 |
| `equilibrium_temp_k` (A=0, no redistribution) | 405 | high | dayside-반구 공식으로 유도 (340 × 2^¼ = 404) |
| `equilibrium_temp_k` (A=0.3) | 311 | high | 유도 (340 × 0.7^¼ = 311) |
| `bond_albedo` | 0.20 | medium | Tie-break. 노출 암석 또는 얇은 대기 범위 0.10–0.35. 얇은 CO₂ 시나리오가 Rayleigh 산란을 통해 약간 더 높은 albedo 선호 |
| `surface_temp_substellar_k` | 470 | medium | Tie-break. 얇은 CO₂ 대기 + 모데스트한 온실 → ~470 K. 노출 암석 무대기 ~400 K |
| `surface_temp_nightside_k` | 250 | medium | Tie-break. 얇은 대기가 미미한 nightside 열 수송 허용. 노출 암석은 ~150 K |
| `atmosphere_present` | true (얇은 CO₂ 우위. 금성 analog 2차) | medium | Tie-break. 더 차가운 T_eq + 더 큰 궤도 거리가 b/c/d 대비 손실 속도를 ~5× 감소. interesting-first 가 완전 노출 암석 대신 대기-얇음 시나리오 선택 |
| `atmosphere_surface_pressure_pa` | 1000 (0.01 bar) | low | Tie-break. 금성의 92 bar 한참 아래 (이 크기에는 무거운 대기 비현실적). 더 높은 일사의 Mars analog 에서 스케일된 얇은 2차 CO₂ |
| `atmosphere_composition` | CO₂ 90%, N₂ 7%, 미량 H₂O / SO₂ / Ar | low | Tie-break. 금성 / 뜨거운 Mars analog. CO₂ 우위 outgassed 2차 |
| `atmosphere_scale_height_km` | 14 | medium | 유도. kT/μg with T = 340 K, μ = 44, g = 4.6 m/s² → 14 km |
| `atmosphere_tint_rgb_hex` | `#6a3a3a` (M 왜성 SED 아래 흐릿한 Rayleigh-적색화 얇은 CO₂) | medium | Tie-break. M 왜성 SED 에 의해 크게 적색화된 Rayleigh-blue + 낮은 대기 두께 → 흐릿한 빨강-violet 헤이즈 |
| `cloud_cover_fraction` | 0.05 | low | Tie-break. 건조한 얇은 대기 → 최소 물 구름. 금성 스타일 구름에 충분히 강력한 SO₂ 광화학 없음 |
| `cloud_morphology` | 희소한 고적운만 (있다면) | low | Tie-break. 얇은 대기 |
| `cloud_tint_rgb_hex` | `#8a6050` (따뜻한 토프 — 최소 기여) | low | Tie-break. M 왜성 조명된 얇은 구름 |
| `ocean_present` | false | high | T > 350 K dayside 가 액체 물 배제 (얇은 CO₂ 가 있어도 표면 물 사이클 없음) |
| `surface_tint_rgb_hex_primary` | `#503020` (더 차가운 다크 basalt. 네 중 가장 차가움) | medium | Tie-break. 네 중 가장 낮은 substellar T 에서 노출 basalt × M 왜성 SED |
| `surface_tint_rgb_hex_accent` | `#6a4030` (terminator/고지대. 미세한 따뜻한 액센트) | low | Tie-break. bedrock 톤 |
| `surface_morphology` | basalt 평원. 더 이른 wet 단계로부터의 가능한 relict aqueous-weathering 특징. antistellar cold-trap | medium | Tie-break. 더 이른 (더 차가운) 단계로부터의 aqueous 지형 가능성을 가진 금성 / 뜨거운 Mars analog |
| `magnetic_field_present` | true (약함) | low | Tie-break. 더 작은 코어 → 더 약한 다이나모. 자기 차폐 제한 |
| `magnetic_dipole_moment_normalized_earth` | 0.0003 | low | Tie-break. 네 중 가장 작음 (Mercury 유추, 다이너모 모델링 아님) |
| `radiation_belt_present` | false | medium | 얇은 대기 + 약한 B-field → 기껏해야 marginal trapped 집단 |
| `surface_radiation_dose_msv_yr` | 3000 | low | Atri 2020 스케일링 (context-cite, 캐시에 없음). 얇은 대기 차폐 (~10 g/cm²) + 2.45 S⊕ XUV × France 2020 듀티 사이클 |
| `atmospheric_shielding_g_cm2` | 10 | medium | 유도. 0.47 g 표면 위 0.01 bar 칼럼 |
| `aurora_present` | true (희미) | medium | Tie-break. 얇은 대기 + 약한 B-field 가 flare 동안 모데스트한 오로라 허용 |
| `aurora_color_primary_hex` | `#88ff88` (CO₂⁺ Fox–Duffendack–Barker 녹황 + 미세 O I 방출) | low | Tie-break. CO₂ 우위 광화학. flare 피크 XUV 동안에만 가시 |
| `aurora_intensity_kR_typical` | 5 | low | Tie-break. 약한 B-field + 얇은 대기 + 모데스트한 Barnard XUV → 지구의 전형 10 kR 의 0.5× |
| `star_apparent_angular_diameter_deg` | 2.61 | high | 유도. 2 R★ / a × (180/π) = 2.62 |
| `stellar_illumination_color_temp_k` | 3195 | high | Barnard Teff |

## Surface synthesis

Barnard e 의 표면 조건은 네 행성 중 가장 "거주 가능에 인접" 합니다
— 비록 여전히 어떤 보수적 HZ 의 한참 바깥에 있지만. cfg 의 얇은 CO₂
대기 시나리오 하에서 ~470 K 의 substellar dayside 온도는 partial melt
없이 basalt regolith 를 허용합니다. 표면 톤 (`#503020`) 은 네 중 가장
어둡고 차가워, 가장 낮은 일사를 반영합니다. terminator 산능 액센트
(`#6a4030`) 가 모데스트한 시각 변동을 제공합니다.

얇은 대기 시나리오는 무대기 형제들에서 부재한 미묘한 지형 특징의
가능성을 엽니다. 만약 e 가 누적 XUV escape 가 desiccate 시키기 전에
더 이른 wet 단계를 경험했다면, relict 배수 네트워크 또는 화학적으로
weathered 된 basalt 지형이 보존될 수 있습니다. cfg 의 `surface_morphology`
필드는 "가능한 relict aqueous-weathering 특징" 을 시각적 nuance 로
포함합니다 — 네-행성 앙상블의 더 차가운 끝에서 동기 부여된 tie-break
선택입니다.

antistellar 반구는 cold-trap 으로 남지만, ~250 K (b/c/d 의 ~100–130 K
보다 상당히 더 따뜻) 에서. 얇은 대기가 nightside 열 수송을 허용하기
때문입니다. substellar-to-antistellar 주야 온도 대비는 ~220 K — 다른
행성들의 무대기 600 K 대비보다 훨씬 작습니다.

0.19 M⊕ 지구 analog 암석의 질량-반지름은 0.58–0.69 R⊕ 를 줍니다. cfg
의 0.64 R⊕ 선택은 중간값으로 DB 의 질량-반지름 값 (0.637) 과 일치합니
다. 4.0 g/cc 의 밀도는 네 행성 중 가장 낮음 — (a) 약간의 휘발성 농축
(mantle 의 H₂O / CO₂ 가 몇 wt%) 또는 (b) 단순히 작은 암석 행성에 대한
질량-반지름 기울기와 일관. 직접 반지름 측정이 구분할 수 있지만 transit
검출은 존재하지 않습니다 (Stefanov 2024, i < 87.9°).

## Atmosphere synthesis

cfg 는 b/c/d 에 사용된 노출 암석 기준선에 대한 canonical tie-break
업그레이드로 e 에 대해 얇은 CO₂ 우위 2차 대기를 채택합니다. 동기
부여 물리학. 2.45 S⊕ 일사와 0.0381 AU 궤도 거리에서, France 2020 의
대기 손실 속도는 단위 면적당 내부 시스템 값의 약 1/5 로 스케일 다운
됩니다. 10 Gyr 에 걸친 누적 손실은 여전히 높지만 (~10²–10³ 지구대기
등가), plausibly 0.19 M⊕ 행성의 같은 시간 척도에 걸친 지속적인 화산
outgassing 의 예산 내. 이는 금성의 칼럼 밀도의 작은 비율로 금성-analog
2차 대기를 생성합니다. cfg 의 0.01 bar 표면 압력은 금성의 92 bar 의
~10⁻⁴. (France 2020 은 여기서 손실-속도 framing 에 인용되지만 로컬
논문 캐시에는 없습니다 — 손실-속도 스케일링은 인용된 수치가 아니라
이 리포트 자체의 차수 추정입니다.)

조성. CO₂ 90%, N₂ 7%, 미량 H₂O / SO₂ / Ar. CO₂ 지배는 금성 / 뜨거운
Mars analog 에 공통적인 광-해리 저항성 outgassing 화학에서 따릅니다.
수증기는 낮은 abundance 에 잠겨 있는데, 표면 온도가 액체 물을 배제
하고 어떤 H₂O outgas 도 H escape 와 함께 빠르게 XUV-광분해되기 때문
입니다. SO₂ 미량은 basalt 화산 활동이 황 화합물을 전달하기 때문에
포함됩니다. 얇은 대기 영역에서 SO₂ 광화학은 지속적인 황산 구름
데크 (금성의 두꺼운 대기와 다름) 를 생성하지 않습니다.

cfg 의 `atmosphere_tint_rgb_hex = #6a3a3a` 는 Barnard 의 M4 V SED 아래
크게 적색화된 Rayleigh 산란을 나타냅니다 — 지구의 푸른 하늘보다 훨씬
어둑하고 빨갛고, Proxima b 에 대해 검토된 M 왜성 거주 가능 영역 행성
색 모델링과 일관됩니다. 대기는 너무 얇아서 궤도에서 강한 산란 특징
을 생성하지 못합니다. limb 헤이즈는 흐릿하고 따뜻한 톤입니다.

구름 면적은 건조한 조성을 고려해 최소 (5%) 입니다. 금성-스타일 황산
구름 없음 (대기가 너무 얇고 SO₂ abundance 가 너무 낮음). 물 구름
없음 (표면 물 소스 없음). 미량 물의 상부 대기 응축으로부터의 희소한
고도-고적운 (cfg `cloud_morphology`) 이 가능하지만 minor 시각 변동만
제공합니다.

오로라 렌더링은 이 합성의 어떤 행성보다도 가장 미묘합니다. 약한
B-field + 얇은 대기 + 모데스트한 Barnard XUV 가 ~5 kR 강도 (지구의
전형의 절반) 를 생성하며, 피크 flare 상태 동안에만 가시 (~25% 듀티
사이클). 1차 방출 색 `#88ff88` 는 CO₂⁺ Fox–Duffendack–Barker 밴드를
추적합니다. 이는 CO₂ 우위 대기에 의해 동기 부여된 빨강-오렌지 N₂⁺
대안에 대한 tie-break 선택입니다.

## Rotation & spin synthesis

e 는 1:1 (동기) 로 조석 잠겨 있습니다. 0.16 M☉ M 왜성 주위 0.0381
AU 의 0.19 M⊕ 암석 행성에 대한 조석 despinning 시간 척도는 대부분의
plausible 한 암석 rheology 에서 10³–10⁶ 년 범위에 듭니다 (Walterová
2020 은 초기 despinning 을 "수천에서 수백만 년 척도" 로 보며, 가장
낮은 dissipation 의 매개변수 구석에서만 1 Gyr 를 넘습니다) — 모든
경우 10 Gyr 나이보다 한참 짧으므로 동기 회전이 예상되는 종착 상태
입니다. 경사는 0° 로 감쇠.

Basant 2025 의 최적합 e = 0.04 (−0.03/+0.04) 는 원과 일관. SPOCK
안정성은 장기 4-행성 거주를 위해 e < 0.02 를 요구합니다. 권장 낮은
이심률에서의 libration 진폭은 < 1° 이며 측정 가능한 diurnal 변조를
만들지 않습니다.

e 의 6.74-일 궤도는 네 행성 중 가장 깁니다. 보수적 HZ 안쪽 가장자리
(10 d) 와의 근접성은 ~10–42 d 의 실제 HZ 행성에 대한 미래 RV 기반
검출에 가장 관련된 타겟이 되게 합니다. Basant 2025 는 10–42 d 윈도우
에서 0.37–0.57 M⊕ 보다 큰 행성을 99% 신뢰도로 명시적으로 배제합니다.
미래 MAROON-X / ESPRESSO 데이터는 이 한계를 더 낮출 수 있습니다.

## Visual styling

e 는 가족의 시각적 "차가운 형제" 입니다 — 가장 어두운 1차 톤
(`#503020`), 가시 (희미할지라도) 대기를 가진 유일한 것, 그리고 미묘한
오로라조차 가진 유일한 것. 궤도에서는 거의 인지할 수 없는 빨강-violet
limb 헤이즈 (`#6a3a3a`) 와 Barnard 의 flare 상태 동안의 occasional
오로라 밴드를 가진 어두운 빨강-갈색 디스크로 나타날 것입니다.

Barnard 는 e 의 하늘에서 2.6° 를 차지 — 지구에서 본 태양의 약 5×
— 네-행성 가족 중 가장 작은 각지름이지만 여전히 낮 하늘의 지배적
특징. 얇은 대기는 Barnard 의 SED 에 의해 크게 적색화된 어둑한 빨강-
violet 낮 하늘 색을 만들며, terminator 에서 거의 검은색으로 전환됩
니다.

표면 형태는 네 중 가장 다양합니다 — canonical basalt regolith 너머
로, 더 이른 (더 차가운) 대기 단계에서의 가능한 relict aqueous-weathering
특징이 보존될 수 있습니다. 게임 내 렌더링은 낮은 밀도에서 occasional
"강바닥" 또는 "화학적으로 변형된 패치" 지형 특징의 옵션을 포함해야
합니다.

Barnard flare 동안의 오로라 밴드는 25% flare 듀티 사이클 동안 높은
자기 위도 (~60°) 에서 흐릿한 녹색 리본 (`#88ff88`) 으로 나타납니다.
강도는 어떤 지구 analog 레퍼런스보다 현저히 낮습니다. 게임 내 밝기
는 극적인 빛의 쇼보다는 미묘한 주변 글로우에 가까운 sub-cinematic
이어야 합니다. 누적 표면 dose (cfg 3000 mSv/yr) 는 네 행성 중 가장
낮지만 여전히 어떤 거주 가능 임계값보다 잘 위에 있습니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Basant R. et al. 2025** — *Four Sub-Earth Planets Orbiting
  Barnard's Star from MAROON-X and ESPRESSO* (`2025ApJ...982L...1B`,
  [arXiv:2503.08095](https://arxiv.org/abs/2503.08095)). e 를 후보 (ESPRESSO 단독 59% 검출 확률) 에서
  확정 (공동 MAROON-X + ESPRESSO 79%) 으로 격상한 MAROON-X 논문. P =
  6.7392 d, Msini = 0.193 ± 0.033 M⊕, a = 0.0381 AU, e = 0.04,
  ω = −27.5°, T_eq = 340 K (A=0, full redistribution). HZ = P 10–42 d.
  안정성을 위해 e < 0.02 선호.
- **González Hernández J. I. et al. 2024** — *A sub-Earth-mass planet
  orbiting Barnard's star* (`2024A&A...690A..79G`, [arXiv:2410.00569](https://arxiv.org/abs/2410.00569)).
  ESPRESSO 데이터가 e (6.74 d) 를 후보 신호로 처음 식별 (검출 민감도
  로는 "예상 밖").
- **Stefanov A. K. et al. 2024** — *TESS photometry of Barnard's Star*
  ([arXiv:2410.00577](https://arxiv.org/abs/2410.00577)). i < 87.9° → 네 행성 모두 비-transit. 질량-반지름
  유도 반지름을 동기 부여.
- **France K. et al. 2020** — *The High-Energy Radiation Environment
  Around a 10 Gyr M Dwarf: Habitable at Last?* ([arXiv:2009.01259](https://arxiv.org/abs/2009.01259)).
  대기 손실 기준선. e 의 0.0381 AU 로 스케일. "habitable at last"
  헤드라인이 e 에 대해 노출 암석 대신 얇은 대기 tie-break 동기 부여.
  *(Context-cite — 로컬 논문 캐시에 없음. framing 용도, 인용 수치 없음.)*
- **Duvvuri G. et al. 2021** — *Reconstructing the EUV Emission of
  Cool Dwarfs* ([arXiv:2102.08493](https://arxiv.org/abs/2102.08493)). quiescent EUV 재구성. 대기 escape
  모델링 입력.
- **Walterová M. & Běhounková M. 2020** — *Thermal and Orbital
  Evolution of Low-mass Exoplanets* ([arXiv:2007.12459](https://arxiv.org/abs/2007.12459)). 조석 despin
  시간 척도 (수천에서 수백만 년. 가장 낮은 dissipation rheology 에서만
  1 Gyr 초과).

### Read (context / methodology, not decision-driving)

- **Toledo-Padrón B. et al. 2019** — *Stellar activity analysis of
  Barnard's Star* ([arXiv:1812.06712](https://arxiv.org/abs/1812.06712)). 호스트 활동 사이클 + 회전
  (P_rot = 145 d).

### Read (instrument-only, not visual-informative)

- (e-특화 없음.)

### Not read — no arXiv preprint or low-priority (~15 papers)

e 의 bib 은 네 중 가장 작습니다 — e 는 개별 발견 논문이 없고 bib 은
이름 충돌 역사 논문 (혜성 Barnard e 1881, 1885, 1887) 이 지배합니다.
radiation-dose Basis 가 인용하는 Atri 2020 (우주선 표면-dose 스케일링)
은 로컬 논문 캐시에 없으며 차수 proxy 로만 쓰입니다.
`docs/phase3/_bib/barnards-star-e.yaml` 에 `status: skipped` 로 보존.

## Open items for follow-up

- **직접 반지름 측정**. 네 행성 모두와 마찬가지로 transit 없음.
  미래 직접 영상화 또는 astrometry 가 cfg 의 `radius_rearth = 0.64`
  placeholder 를 개선할 수 있습니다. e 는 가장 작아 제약하기 가장
  어려울 것입니다.
- **노출 암석 vs. 얇은 대기 변이**. cfg 의 얇은 CO₂ 시나리오는
  노출 암석에 대한 tie-break. 새로 발견된 차가운 sub-Earth USP 행성
  (예. TOI-700 류) 에 대한 미래 대기 모델링이 얇은 CO₂ 유지를 배제
  한다면, cfg 는 e 를 노출 암석으로 되돌려야 합니다. France 2020 의
  대기 질량 손실 계산은 시사적이지만 결정적이지 않습니다.
- **Wet 더 이른 단계 형태**. cfg 는 "relict aqueous-weathering 특징"
  을 시각 변동으로 포함. 이는 순수 추측. 네 Barnard 행성 중 어느
  것에 대해서도 더 이른 wet 단계의 직접 증거는 없습니다.
- **오로라 가시성**. cfg 는 flare 동안 흐릿한 오로라를 인코딩하지만
  강도는 극적인 게임 내 렌더링 임계값 아래. 사용자는 시각적 흥미를
  위해 이를 올리거나 사실성을 위해 내릴 수 있습니다.
- **HZ 안쪽 가장자리 행성 후보**. Basant 2025 는 HZ 의 P > 10 d
  의 가상 Barnard f 를 명시적으로 탐색해 > 0.37–0.57 M⊕ 의 행성을
  배제. 미래 MAROON-X 모니터링이 더 낮은 질량 HZ 행성을 검출할 수
  있고, 발견되면 e 를 시스템의 가장 바깥으로 대체할 것입니다.
- **c 와의 공명**. 주기 비 1.634 ≈ 5/3 = 1.667. e 가 근-공명 trap
  에 있는지 단순히 우연으로 근-공명인지가 장기 동역학에 영향을 미
  칩니다.
- **France 2020 / Atri 2020 재페치**. 둘 다 대기-손실과 radiation-
  dose 스케일링에 인용되지만 로컬 논문 캐시에 없습니다. cfg 출하 전
  arXiv preprint 를 재페치해 차수 추정을 인용 수치로 교체해야 합니다.

## Related

- [barnards-star](barnards-star.md) — 호스트 별. 조용한 노쇠 M4 V. France 2020 당 "habitable at last?" 헤드라인
- [barnards-star-b](barnards-star-b.md) — 가장 안쪽 (Ribas-반박 후). 노출 암석
- [barnards-star-c](barnards-star-c.md) — 가장 무거움. 노출 암석
- [barnards-star-d](barnards-star-d.md) — 가장 뜨거움. substellar partial-melt
- [proxima-cen-b](proxima-cen-b.md) — analog 비교. 또 다른 M 왜성 HZ 인접 행성이지만 0.65 S⊕ 에서 보수적 HZ 내부 (e 의 2.45 S⊕ 와 대비)
- [methodology](../reference/methodology.md) — Decisions 스키마
- [mod-reference](../reference/mod-reference.md) — 하류 cfg writer
