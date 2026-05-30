<!-- GJ 896 A b Phase 3 합성. cfg-ready 결정과 근거 -->
# GJ 896 A b — Phase 3 Synthesis

GJ 896 A b 는 젊고 활동적인 M3.5 Ve flare star GJ 896 A 를
a = 0.63965 ± 0.00067 AU 에서 284.39 ± 1.47 d 주기로, 적당히 이심적인
궤도 e = 0.35 ± 0.19 (Curiel et al. 2022) 으로 도는 따뜻한 ~2.3 M_Jup
가스 거성입니다. VLBA + 광학/적외선 천체측정으로 발견되었고, 이는 최소
질량이 아니라 **진질량** 을 줍니다. m_b = 2.26 ± 0.57 M_Jup
(= 718.29 ± 181.16 M⊕), 궤도 경사 i = 69.2° 입니다. 이로써 GJ 896 A b
는 천체측정으로 발견된 쌍성계 별의 첫 행성 동반체이고 — 6.26 pc 에서 —
알려진 가장 가까운 Jovian-질량 행성 중 하나입니다. 투과나 열-방출
스펙트럼은 없습니다. 행성의 대기 조성, 반지름, 자전, 그리고 위성이나
고리는 제약되지 않으므로, 그 필드들은 적색왜성 조명 아래의 jovian-analog
tie-break 입니다.

**NearStars 시나리오 선택. 따뜻하고 (장반경에서 T_eq ≈ 130 K, 이심
궤도에서 ~110–165 K 를 오감), 성숙한 ~2.3 M_Jup jovian 으로, 0.64 AU
궤도에서 깊은 붉은 M3.5 Ve flare star 의 빛을 받는 모습으로
렌더링합니다.** 호스트의 좁은 거주가능영역 (Curiel 2022: 0.18–0.26 AU)
밖에 있고 snow line (~0.51 AU) 주위를 진동하므로, 궤도가 물-얼음선
바로 안쪽에서 한참 바깥쪽까지 데려가는 cold-to-warm Jovian 입니다.
시각 styling 은 이를 Jupiter-질량 analog 로 다뤄, M-왜성 조명 아래
따뜻하게 렌더링되는 암모니아-얼음 구름 띠, 활동적 호스트의 높아진
UV/flare 에서 오는 옅은 광화학 haze, 고리 없음, Jupiter-스케일 자기권
으로 처리합니다. 궤도와 진질량이 high-confidence Phase 2 앵커이고,
반지름, 대기, 구름, 자전, 자기권은 jovian-analog tie-break (아직
스펙트럼이나 열 지도 없음) 입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | false | high | 0.44 M☉ 별 주위 0.64 AU 의 284 일 궤도 — 이 거리에서 조석 spin-down 시간척도 ≫ 시스템 나이. Jovian 은 빠른 원시 spin 을 유지 |
| `obliquity_deg` | 25 | low | Tie-break. 측정 없음. 시각적으로 뚜렷한 축 기울기를 위해 Jupiter 식 3° 대신 Saturn 식 ~26° 선택. 0.64 AU jovian 의 동역학 창 안. Curiel 2022 의 행성면 대 쌍성면 148° mutual inclination 이 비자명 obliquity 를 그럴듯하게 만듦 |
| `eccentricity` | 0.35 ± 0.19 | high | Curiel et al. 2022 — 천체측정 피팅 (Phase 2 recommended). 근일점 0.42 AU, 원일점 0.86 AU |
| `argument_of_periastron_deg` | 353.11 | high | Curiel et al. 2022 (Phase 2 recommended) |
| `sidereal_period_days` | 284.39 ± 1.47 | high | Curiel et al. 2022 — 천체측정 피팅 (Phase 2 recommended). 단일-동반체 피팅은 281.56 ± 1.67 d (`recommended:false`) |
| `semi_major_axis_au` | 0.63965 ± 0.00067 | high | Curiel et al. 2022 — 전체 결합 천체측정 피팅 (Phase 2 recommended) |
| `inclination_deg` | 69.2 ± 25.61 | medium | Curiel et al. 2022 (Phase 2 recommended). 큰 불확실도는 천체측정 궤도 해를 반영 |
| `longitude_of_ascending_node_deg` | 45.62 | medium | Curiel et al. 2022 (Phase 2 recommended). 천체측정이 Ω 를 직접 제약 — 비-통과 행성에 드문 일 |
| `mass_mjup` | 2.26 ± 0.57 | high | Curiel et al. 2022 — 전체 결합 천체측정 피팅의 **진질량** (Phase 2 recommended). 천체측정이 sin i 축퇴를 깨므로 최소 질량이 아님 |
| `mass_mearth` | 718.29 ± 181.16 | high | Curiel et al. 2022 (= 2.26 M_Jup × 317.8). Phase 2 recommended 진질량 |
| `radius_rjup` | 1.1 | low | Tie-break. 통과 없음. 성숙한 2.3 M_Jup jovian (Fortney 2007 / Burrows 진화 트랙) 은 ~1.0–1.1 R_Jup 부근. cfg 가 1.1 R_Jup 선택. DB `radius_rearth = 13.3` (≈ 1.19 R_Jup) 은 NASA-archive 모델 placeholder 로 측정이 아님 — 이 범위와 일관 |
| `surface_gravity_g_earth` | ~58 | medium | 유도. g = G M / R² 에 M = 2.26 M_Jup, R = 1.1 R_Jup → ~570 m/s² ≈ 58 g⊕. 고중력의 무거운 jovian |
| `density_g_cc` | ~2.1 | medium | 유도. 2.26 M_Jup / (1.1 R_Jup)³ × ρ_Jup ≈ 2.1 g/cc. Jupiter (1.33 g/cc) 보다 조밀한, 콤팩트하고 무거운 성숙 가스 거성 |
| `insolation_s_earth` | ~0.05 | low | 유도. S = L_star / a² 에 합성 L ≈ 0.02 L☉ (Phase 2 광도 없음) / (0.64 AU)² ≈ 0.05 S⊕. L 이 측정 아닌 합성이라 low-confidence |
| `equilibrium_temp_k_a0` | ~130 | low | 유도. T_eq = 278 K × (L/a²)^0.25 에 합성 L ≈ 0.02 L☉, a = 0.64 AU. ~110 K (원일점 0.86 AU) ~ ~165 K (근일점 0.42 AU). Phase 2 L 없어 low-confidence. Curiel 은 T_eq 미측정 (DB `equilibrium_temperature_k` null) |
| `equilibrium_temp_k_a03` | ~120 | low | 유도. Earth-analog A = 0.3. 같은 합성-L caveat |
| `bond_albedo` | 0.34 | low | Tie-break. 차가운 T_eq ≈ 130 K 가 구름 화학을 Jupiter 보다 Saturn 식 두꺼운 암모니아-얼음 deck 쪽으로 기울이므로, Jupiter 의 0.50 대신 Saturn-analog 0.34 선택 |
| `atmosphere_present` | true | high | 정의상 가스 거성. 2.3 M_Jup 질량과 jovian 반지름에서 H₂/He bulk 추론 |
| `atmosphere_reference_pressure_pa` | 100000 | medium | 가스 거성은 고체 표면 없음. 구름-deck 렌더링용 cfg-기준 1 bar 레벨. 관습적 jovian KSP 대기 원점 |
| `atmosphere_composition` | H₂ ~89%, He ~10%, CH₄ ~0.2%, NH₃ ~0.02%, H₂O (심부) ~0.01%, 미량 광화학 산물 | low | Tie-break. 스펙트럼 없음. 태양-조성 jovian 기본값 (Lodders 2003 protosolar). 응축 화학은 ~130 K 평형에서 끊기고 암모니아-얼음 구름 deck |
| `atmosphere_scale_height_km` | ~9 | medium | 유도. H = kT / (μ m_H g) 에 T ≈ 130 K, μ = 2.3, g ≈ 570 m/s² ≈ 9 km. 높은 표면 중력 때문에 작음 |
| `atmosphere_tint_rgb_hex` | `#d8b890` (M3.5 V 조명 아래 따뜻한-tan limb haze) | low | Tie-break. 암모니아-얼음 대기는 본질적으로 거의 흰색. 깊은 붉은 ~3300 K SED 가 인지 limb haze 를 따뜻/tan 으로, 태양-조명 jovian limb 보다 붉게 옮김 |
| `cloud_cover_fraction` | 0.85 | medium | jovian-analog. 띠/zone 대비를 가진 거의 완전한 zonal 띠. 0.85 가 균일한 overcast 대신 뚜렷한 어두운 띠 대 밝은 zone 을 남김 |
| `cloud_morphology` | zonal 띠. ≈ 0.5–1 bar 의 암모니아-얼음 구름 deck. 그 아래 가능한 물-구름 deck. 활동적 호스트의 높아진 UV/flare 에서 CH₄ 광분해로 100 mbar 위 옅은 광화학 haze | low | Tie-break. GCM 없음. Saturn-analog 띠 구조에, GJ 896 A 의 강한 flare/UV 활동이 조용한-호스트 jovian 보다 약간 더 두드러진 성층권 haze 를 구동 |
| `cloud_tint_rgb_hex` | `#e6d2b4` (따뜻한 크림 — M-왜성 조명 아래 NH₃ 얼음) | low | Tie-break. Saturn 의 암모니아 구름은 태양광 아래 크림-흰색. ~3300 K 깊은 붉은 SED 아래 인지 색조가 따뜻한 크림/tan 으로 더 옮김 |
| `planet_disk_tint_rgb_hex_primary` | `#e6d2b4` (크림-tan zone — 지배적 구름-deck 외형) | low | `cloud_tint_rgb_hex` 의 하류 |
| `planet_disk_tint_rgb_hex_accent` | `#c0a070` (따뜻한 tan-갈색 띠 — 더 깊은 구름층 + haze 가 비쳐 보임) | low | Tie-break. M-왜성 조명 아래 Jupiter/Saturn 띠-zone 대비. 낮은 일사량과 약한 대류 구동 때문에 띠 진폭은 중간 |
| `ring_present` | false | low | Tie-break. 검출 없음 (천체측정은 고리를 못 봄). cfg 가 "고리 없음" 으로 기본. search-and-verify 정책에 따라 지어낸 feature 없음 |
| `rotation_period_hours` | 10 | low | Tie-break. 자전 측정 없음. Jupiter-analog ~10 h 빠른 자전. 무겁고 젊은 jovian 은 큰 원시 spin 각운동량을 유지해, 느린 Saturn/Uranus 식 값보다 Jupiter-부류 빠른 자전을 선호 |
| `magnetic_field_microtesla_equator` | 900 | medium | 스케일된 jovian 다이너모. Jupiter 표면장 ≈ 430 μT. 활발한 대류와 빠른 자전을 가진 2.3 M_Jup 행성은 더 강한 장으로 스케일 — cfg 가 ~900 μT (~Jupiter 2배) 선택, 더 큰 질량과 내부 열을 반영 |
| `aurora_present` | true | medium | 호스트 GJ 896 A 는 kG 자기장과 잦은 전파/X-선 버스트를 가진 매우 활동적인 flare star (Curiel 2022). 0.64 AU 에서 높아진 항성풍 + flare 플라스마 flux 가 jovian 자기권에 포획되어 강한 오로라 방출을 구동 |
| `aurora_color_primary_hex` | `#c84080` (H₂-풍부 jovian 대기의 H-Balmer α 656 nm 적-분홍) | low | Tie-break. 가시-대역 jovian 오로라는 H-Balmer α 지배. 적-분홍으로 읽히며, 깊은 붉은 조명 맥락이 보강 |
| `star_apparent_angular_diameter_deg` | ~0.29 (근일점 0.44) | medium | 유도. a = 0.64 AU 에서 R ≈ 0.35 R☉ → ~0.29°. 근일점 0.42 AU 에서 → ~0.44° (지구에서 본 태양 겉보기 크기 부근) |
| `stellar_illumination_color_temp_k` | ~3300 (합성) | low | 호스트의 M3.5 V 분광형에서 합성 (Phase 2 Teff 없음). 깊은 붉은 M-왜성 조명 |

## Surface synthesis

GJ 896 A b 는 고체 표면이 없는 가스 거성입니다. 이 섹션은 관측자가 볼
구름-deck "표면" 과 그 뒤의 bulk-구조 논리를 다룹니다. 확실히 측정된
물리량은 질량입니다. m_b = 2.26 ± 0.57 M_Jup (Curiel 2022) 로, 최소
질량이 아니라 **진질량** 인데, 천체측정 궤도가 시선속도가 열어두는
sin i 축퇴를 깨기 때문입니다. 2.3 M_Jup 에서 행성은 무겁고 성숙한
jovian 입니다. 어떤 그럴듯한 시스템 나이에서든 이런 행성의 진화 트랙은
반지름을 ~1.0–1.1 R_Jup 부근에 두므로, cfg 는 R ≈ 1.1 R_Jup 을
채택합니다. DB 는 `radius_rearth = 13.3` (≈ 1.19 R_Jup) 을 저장하는데,
이는 측정이 아니라 NASA-archive 모델 placeholder 이지만 이 범위와
일관됩니다. 함의되는 bulk 밀도는 높고 (~2 g/cc, Jupiter 보다 조밀),
표면 중력은 큽니다 (~58 g⊕). 그래서 가시 대기는 작은 ~9 km scale
height 로 콤팩트합니다.

열 상태는 cold-to-warm 입니다. 호스트 광도가 Phase 2 에 측정되어 있지
않으므로, 평형온도는 L ≈ 0.02 L☉ (항성 합성의 Stefan-Boltzmann /
질량-광도 추정치) 에서 합성하고 low-confidence 로 표시합니다.
T_eq ≈ 130 K (0.64 AU 장반경) 로, 이심 궤도에서 원일점 (0.86 AU) ~110 K
부터 근일점 (0.42 AU) ~165 K 까지 오갑니다. Curiel 2022 는 호스트의
거주가능영역을 0.18–0.26 AU, snow line 을 ~0.51 AU 에 둡니다. 따라서
GJ 896 A b 는 HZ 한참 밖에 있고 snow line 주위를 진동합니다 — 근일점
근처에서는 안쪽, 궤도 대부분에서는 바깥쪽입니다. ~130 K 에서 지배적
응축물은 암모니아 얼음이므로, 가시 구름-deck "표면" 은 0.5–1 bar 레벨
부근의 암모니아-얼음 deck 입니다.

깊은 붉은 M3.5 V 조명 아래 렌더링되는 구름 deck 은 따뜻한 크림-tan
(`#e6d2b4` zone, `#c0a070` 띠) 입니다. Saturn 의 암모니아 구름은 태양광
아래 크림-흰색으로 보이고, ~3300 K 합성 SED 가 인지 색조를 따뜻한
크림으로 더 옮깁니다. 띠/zone 대비는 중간입니다 — 낮은 일사량이 Jupiter
보다 약한 대류 구동을 주므로 띠는 있지만 덜 선명합니다. 표면/구름 색과
형태 필드는 모두 jovian-analog tie-break 입니다. GJ 896 A b 의 투과나
열-방출 스펙트럼이 없으므로, cfg 는 featureless 원반 대신 가장 흥미롭고
스펙트럼적으로 그럴듯한 읽기 (띠를 두른 암모니아-얼음 jovian) 를
기본으로 합니다.

## Atmosphere synthesis

GJ 896 A b 는 2.3 M_Jup 질량과 jovian 반지름에서 추론된 깊은 H₂/He
외피를 가집니다. 대기가 곧 행성이므로, 이 섹션은 조성, 구름/haze 구조,
그리고 상층 대기 관측자가 볼 하늘을 다룹니다.

**조성.** 스펙트럼이 없으므로 cfg 는 태양-조성 jovian 기본값 (Lodders
2003 protosolar abundance) 을 채택합니다. H₂ ~89%, He ~10%, 주요 휘발성
물질로 CH₄ (~0.2%), NH₃ (~0.02%), 심부 H₂O, 그리고 미량 광화학 산물
입니다. 응축 화학은 ~130 K 평형온도에서 끊겨 암모니아 구름 deck 을
0.5–1 bar 부근에, 더 깊은 물-구름 deck 을 그 아래에 (가시 영상에는
접근 불가) 둡니다. 이는 다른 NearStars 차가운 jovian 에 쓴 것과 같은
조성 tie-break 이고, 스펙트럼이 얻어지면 교체됩니다.

**활동적 호스트 아래의 광화학.** 헤드라인 대기 modifier 는 호스트
별입니다. GJ 896 A 는 kG 규모 자기장과 잦은 전파/X-선 버스트를 가진
매우 활동적인 flare star 이므로 (Curiel 2022), 0.64 AU 에서 입사 UV 와
flare-입자 flux 가 조용한-호스트 jovian 보다 높습니다. 이는 ~100 mbar
레벨 위에서 CH₄ 광분해를 구동하고 옅은 탄화수소/광화학 haze 층을 쌓을
것으로 예상되며, 암모니아 deck 위 옅은 따뜻한-tan limb haze (`#d8b890`)
로 렌더링됩니다 — 조용한 별 주위 jovian 의 haze 보다 약간 더 두드러지나
여전히 지배적 색조가 아닌 옅은 limb 효과입니다. flare-입자 flux 는 또한
오로라 활동에 먹이를 줍니다 (아래).

**하늘 외형.** 상층 대기 안에서 하늘은 붉은 호스트 별이 따뜻한
크림-tan 으로 비추는 깊은 암모니아-구름 haze 입니다. 지배적 광원은
GJ 896 A 의 깊은 붉은 원반으로, 장반경에서 ~0.29° (근일점 근처 ~0.44°
까지 성장) 를 차지합니다 — 지구에서 본 태양 겉보기 크기의 절반 남짓이며,
깊은 적등색으로, 지구 일사량 수 % 의 적외선이 풍부한 빛으로 구름 꼭대기를
적십니다. 두 번째 태양 GJ 896 B 는 넓은 역행 궤도의 훨씬 작지만 뚜렷한
밝은 붉은 점입니다.

## Rotation & spin synthesis

GJ 896 A b 는 **조석 고정되어 있지 않습니다**. 0.44 M☉ 별 주위 0.64 AU
에서 조석 spin-down 시간척도가 시스템 나이를 크게 초과하므로, 행성은
태양계 거대행성처럼 빠른 원시 자전을 유지합니다. cfg 는 Jupiter-analog
~10 시간 자전 주기를 채택합니다 — 무겁고 젊은 jovian 은 큰 원시 spin
각운동량을 가져, 느린 Saturn 식 (10.7 h) 이나 Uranus 식 (17 h) 값보다
Jupiter-부류 빠른 자전을 선호합니다. 이는 tie-break 입니다. 자전 측정이
없습니다.

**KSP 구현 노트.** 행성 자전 주기 ≈ 10 h = 36 000 s 로, Kopernicus 에서
행성 바디에 초 단위로 설정합니다. 빠른 자전이 zonal 띠와 빠르게 자전하는
가스 거성에 전형적인 oblate 형태를 구동합니다.

**Obliquity 와 쌍성 architecture.** cfg 는 0.64 AU jovian 의 동역학 창
안에서 시각적으로 뚜렷한 축 기울기를 위해 Jupiter 식 ~3° 대신 Saturn 식
obliquity ~25° (tie-break, 측정 없음) 를 선택합니다. 여기엔 비자명
obliquity 의 물리적 hook 이 있습니다. Curiel 2022 는 행성 궤도면과 넓은
쌍성 궤도면 사이에 큰 mutual inclination Φ = 148° (역행 구성) 를
찾는데, 이는 항성 동반체의 세속적 forcing 으로 상당한 행성 obliquity 를
들뜨게 하고 유지할 수 있는 종류의 misaligned architecture 입니다. 이심
(e = 0.35) 궤도는 행성이 0.42 와 0.86 AU 사이를 오감에 따라 obliquity
계절 위에 진짜 계절/일사 주기를 줍니다 — 대부분 카탈로그 jovian 의
거의 원형인 궤도와 구별됩니다.

## Visual styling

NearStars 렌더러에서 GJ 896 A b 는 가시적으로 이심적인 궤도 위의
따뜻하고, 띠를 두른, 적색왜성-조명 Jovian 으로 그려집니다.

- **전체 외형 (궤도 뷰).** 따뜻한 크림-tan zonal 띠 (`#e6d2b4` zone,
  `#c0a070` 띠) 를 가진 무거운 ~1.1 R_Jup 가스 거성. M3.5 V 호스트가 깊은
  붉은빛으로 비추며, 낮은 일사량에서의 약한 대류 구동 때문에 띠는 있되
  대비는 중간입니다. 빠른 ~10 h 자전에서 온 oblate 형태.
- **주간면 상세.** 뚜렷한 Jupiter/Saturn 식 띠와 zone. 암모니아-얼음
  구름 deck 이 ~3300 K SED 아래 따뜻한 크림으로 읽히고, 띠 영역은 구름
  deck 이 얇아지는 곳에서 더 깊은 tan-갈색입니다.
- **종단 띠.** 옅은 따뜻한-tan 광화학 haze 층 (`#d8b890`) 이 구름 deck
  위 limb 을 따라 자리합니다 — GJ 896 A 의 높아진 UV 와 flare flux 때문에
  조용한-호스트 jovian 보다 약간 더 두드러집니다.
- **야간면.** 어둡고, 자기 극 근처에 가능한 오로라 glow (아래).
- **오로라.** GJ 896 A 의 강한 flare/전파 활동과 높아진 항성풍이 활발한
  자기권-feed 오로라를 구동. 자기 극에 적-분홍 H-Balmer-α 오로라 oval
  (`#c84080`) 로 렌더링되며, 호스트의 잦은 flare 에 맞춰 밝아집니다 —
  이례적으로 활동적인 호스트를 감안한 뚜렷하고 과학적으로 근거 있는
  효과입니다.
- **고리 없음.** 고리는 렌더링하지 않습니다 (tie-break. 검출 없음,
  search-and-verify 정책에 따라 지어낸 feature 없음).
- **하늘의 호스트 별.** GJ 896 A 의 깊은 붉은 원반은 장반경에서 ~0.29°,
  근일점 근처에서 ~0.44° 를 차지합니다 — 지구에서 본 태양 겉보기 크기의
  절반 남짓에서 거의 그 전부까지 — 그리고 구름 꼭대기를 적외선이 풍부한
  붉은빛으로 적십니다. 이심 궤도가 매 284 일 해마다 별을 눈에 띄게 부풀고
  줄어들게 만듭니다.
- **두 번째 태양.** M4.5 동반체 GJ 896 B 는 넓은 229 년 역행 궤도
  (a = 31.6 AU) 의 더 작지만 뚜렷한 밝은 붉은 점으로 나타납니다 — 두 태양
  모두 깊은 붉은빛인 진짜 두-태양 하늘입니다.

## Bibliography

### Read (drove Decisions above)

- **Curiel S. et al. 2022** — *3D orbital architecture of a dwarf
  binary system and its planetary companion*, AJ 164, 93
  (`2022AJ....164...93C`, doi:10.3847/1538-3881/ac7c66,
  arXiv:2208.14553). GJ 896 A b 의 VLBA + 광학/적외선 천체측정 발견.
  진질량 (2.26 ± 0.57 M_Jup = 718.29 M⊕), 전체 궤도 요소 세트
  (a = 0.63965 AU, P = 284.39 d, e = 0.35, i = 69.2°, Ω = 45.62°,
  ω = 353.11°), 행성의 열 영역을 정하는 거주가능영역 (0.18–0.26 AU) 과
  snow-line (~0.51 AU) 추정치, obliquity 논리에 쓴 큰 148° 행성-대-쌍성
  mutual inclination / 역행 architecture 의 Phase 2 recommended 출처.
  조명과 두-번째-태양 렌더링에 먹이를 주는 호스트 맥락 (M3.5 Ve flare
  star, GJ 896 B 동반체) 도 여기서 옴.

### Read (context / methodology, not decision-driving)

- **Fortney J.J. et al. 2007** & **Burrows A. et al.** (진화 거대행성
  질량-반지름-나이 트랙) — 성숙한 2.3 M_Jup jovian 의 ~1.0–1.1 R_Jup
  반지름 tie-break 의 근거. 반지름 행에만 읽음. GJ-896-고유 내용 없음.
- **Lodders K. 2003** — protosolar 원소 abundance. 태양-조성 대기
  tie-break 의 근거. 방법론 맥락.

### Read (instrument-only, not visual-informative)

- Curiel 2022 의 VLBA 천체측정 궤도-피팅 방법론 (AIPS phase-referencing,
  AGA / least-squares + MCMC 궤도 해) 은 진질량과 궤도-요소 측정의 기기적
  골격이지만, 위에서 이미 쓴 파라미터 이상의 직접 시각 필드를 주지는
  않습니다.

### Not read — no arXiv preprint or low-priority (~handful)

GJ 896 A b 의 투과, 방출, 반사광 스펙트럼이 없으므로, 대기/구름 조성과
색 필드는 모두 읽을 논문이 없는 jovian-analog tie-break 입니다. 일반적인
차가운-jovian 대기 / 광화학 서베이 (예: Sudarsky 알베도 부류, Marley
구름 모델) 는 정성적 띠-두른-암모니아-jovian 그림에 정보를 주지만
큐레이션할 GJ-896-b-고유 수치는 주지 않습니다. 단일-동반체 궤도 피팅
(Curiel 2022 Table 2 col 3: a = 0.6352 AU, P = 281.56 d, e = 0.30) 은
DB 에 `recommended:false` 대안으로 보존됩니다.

## Open items for follow-up

- **직접 영상 + 분광.** Curiel 2022 는 GJ 896 A b 가 알려진 가장 가까운
  Jovian 중 하나이며 직접 영상과 분광에 "잘 맞는다" 고 언급합니다. 미래
  스펙트럼이 tie-break 대기 조성, 구름 색조, haze 를 측정값으로 교체하고
  그 행들을 low 에서 high 신뢰도로 끌어올립니다.
- **호스트 Teff / 광도.** 행성의 일사량과 평형온도는 미측정 호스트 광도
  (L ≈ 0.02 L☉) 에서 합성합니다. GJ 896 A 의 큐레이션된 Teff/L 이 T_eq
  (현재 ~130 K, low confidence) 와 일사량 행을 sharpen 합니다.
- **반지름 측정.** 통과 없음 (천체측정 i = 69.2° 가 edge-on 이 아니고,
  행성이 통과하는 것으로 알려지지 않음) 이라 반지름은 모델-유도 ~1.1
  R_Jup tie-break 로 남습니다. DB `radius_rearth = 13.3` placeholder 는
  진짜 측정이 나올 때까지 그대로 취급해야 합니다.
- **GJ 896 B 를 DB 바디로.** 행성 하늘의 두 번째 태양은 아직 별도 DB
  바디가 아닙니다. 이를 (그리고 229 년 역행 쌍의 binary_orbit cfg 를)
  추가하면 두-태양 하늘과 세속적 obliquity forcing 을 충실히 렌더링할 수
  있습니다.
- **Obliquity / spin.** Saturn 식 ~25° obliquity 와 ~10 h 자전은
  tie-break 입니다. 148° mutual-inclination architecture 가 비자명
  obliquity 를 동기부여하지만 못박지는 않습니다. misaligned 시스템의
  동역학 연구가 행성 spin 상태를 제약하면 다듬습니다.

## Related

- [methodology](../reference/methodology.md) — Decisions 표의 스키마 출처
- [gj-896-a](gj-896-a.md) — 호스트 M3.5 Ve flare star. 조명 색, 일사량, 두-번째-태양 맥락의 출처
- [eps-eri-b](eps-eri-b.md) — 비교 차가운 jovian (~0.78 M_Jup, K2V 주위 3.5 AU). 그것의 거의 원형 궤도와 단일성계를 GJ 896 A b 의 이심 궤도 및 misaligned 쌍성 architecture 와 대비
