<!-- YZ Cet b Phase 3 합성. cfg-ready 결정과 근거 -->
# YZ Cet b — Phase 3 Synthesis

YZ Cet b 는 M4.5 V flare star YZ Cet 을 도는 세 행성 중 최내측으로,
2.02087 일 주기, a = 0.0163 AU 궤도에 있습니다 (Stock et al. 2020).
비통과 시선속도(RV) 행성이라 최소질량 M sin i = 0.70 ± 0.09 M⊕ (Stock
2020) 은 측정되지만 반지름은 **측정되지 않습니다** — DB 에 실린
0.913 R⊕ 수치는 관측이 아니라 준경험적 질량-반지름 추정 (Stock 2020 /
Astudillo-Defru 2017) 입니다. 호스트의 L = 0.0022 L☉ 에서 평형온도는
알베도 0 에서 T_eq ≈ 471 K (여기서 계산. T_eq = 278.3·L^0.25/√a) 이라,
b 는 **따뜻한 암석 세계** 입니다 — 뜨겁지만 용암 행성과는 거리가 멉니다.
M 왜성이 어둡고 b 는 작은 궤도에도 지구 일사량의 ~8.2 배만 받기
때문입니다.

**NearStars 시나리오 선택. 따뜻하고 조석 고정된 암석 행성으로, 얇거나
없는 이차 대기를 가지며 — 독특하게 — 자기권을 가집니다.** YZ Cet b 는
시스템의 확인된 항성-행성 자기 상호작용의 구동체입니다. Trigilio et
al. 2023 은 오로라 전파 방출에서 **행성 극자기장이 최소 0.4 G** 임을
추론했는데, 이는 외계행성 자기장의 첫 (간접) 측정이고, Pineda &
Villadsen 2023 은 b 의 궤도로 folding 되는 SPI 전파 버스트를
검출합니다. 자기권이 이 행성의 헤드라인 특징입니다. 통과나 식,
투과 스펙트럼이 없으므로 표면과 대기는 low confidence 에 둡니다.

## Decisions

Kopernicus / atmosphere cfg-ready 값입니다. `Confidence` 표기는
high = 직접 측정되었거나 강하게 제약됨, medium = 강한 근거를 갖춘
이론, low = 허용 범위 안에서의 미적 선택을 뜻합니다.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | true | high | 0.0163 AU 의 2.02 d 궤도. 중간-M 호스트에서 조석 고정 시간이 시스템 나이보다 훨씬 짧음 |
| `obliquity_deg` | 0 | high | 이 궤도에서 조석 damping |
| `eccentricity` | 0.06 | medium | Stock et al. 2020 (Phase 2 recommended). 제약 약함 (σ ≈ 0.06), 원궤도와 일관 |
| `argument_of_periastron_deg` | 197 | low | Stock et al. 2020 (낮은 ecc 라 제약 약함) |
| `sidereal_period_days` | 2.02087 | high | Stock et al. 2020 (Phase 2 recommended). Astudillo-Defru 2017 의 1.96876 d 를 대체 |
| `semi_major_axis_au` | 0.01634 | high | Stock et al. 2020 (Phase 2 recommended) |
| `mass_mearth` | ≥ 0.70 ± 0.09 (M sin i) | high | Stock et al. 2020 RV 최소질량 (Phase 2 recommended). 실제 질량은 1/sin i 만큼 더 큼 (RV 라 경사 없음) |
| `radius_rearth` | ~0.913 (ESTIMATE) | low | 측정 아님 — 통과 없음. 준경험적 M-R 추정 (Stock 2020). Pineda & Villadsen 2023 은 지구형 밀도 가정 시 0.89–1.0 R⊕ 로 bracket |
| `surface_gravity_g_earth` | ~0.84 | low | 유도값 = 0.70 / 0.913² (최소질량 + 추정 반지름). 하한 (실제 질량 더 큼) |
| `density_g_cc` | ~5 (암석 가정) | low | 측정 반지름 없음 → 측정 밀도 없음. 지구형 암석 조성 가정 |
| `insolation_s_earth` | 8.2 | high | 유도값 = L / a² = 0.0022 / 0.01634² |
| `equilibrium_temp_k` (A=0) | 471 | high | 유도값 = 278.3 · L^0.25 / √a (L = 0.0022 L☉, a = 0.01634 AU) |
| `equilibrium_temp_k` (A=0.3) | 431 | high | 유도값, 지구형 Bond 알베도 |
| `bond_albedo` | 0.1 | low | Tie-break. 따뜻한 암석 표면에 대해 낮게 가정. 측정 없음 |
| `atmosphere_present` | thin or absent | low | 투과 스펙트럼 없음. 활동적 flaring M 왜성 주위 따뜻한 암석 RV 행성 — 대기 유지가 marginal. cfg 는 시각적으로 흥미로운 얇은 대기를 렌더링 |
| `atmosphere_surface_pressure_pa` | ~10000 (0.1 bar, tie-break) | low | 측정 없음. airless 보다 흥미로운 얇은 이차 대기 선택. 보수적 airless 변형은 Open items 에 보존 |
| `atmosphere_composition` | CO₂ / N₂ secondary (가정) | low | 스펙트럼 없음. 대기가 남아 있다면 탈가스 암석 행성 조성 가정 |
| `atmosphere_tint_rgb_hex` | `#caa37a` (얇은 따뜻한 haze) | low | Tie-break. 얇은 대기가 있다면 3100 K 조명 아래 희미한 따뜻한 사지 haze |
| `dayside_surface_temp_k` | ~520 | medium | substellar 맨 암석 정점이 471 K 전역 T_eq 위 (A=0, 낮은 재분배) |
| `nightside_surface_temp_k` | depends on atmosphere | low | airless → 매우 차가운 nightside. 얇은 대기 → 부분 재분배 |
| `surface_tint_rgb_hex_primary` | `#5a4438` (따뜻한 basalt 암석) | low | Tie-break. 붉은 M-왜성 빛 아래 따뜻한 색조의 철 함유 basalt. b 는 확인된 용암 세계가 아니라 airless-검정 안쪽 TRAPPIST 세계보다 따뜻함 |
| `surface_tint_rgb_hex_accent` | `#7a3a22` (산화철 patch) | low | Tie-break. 노출된 따뜻한 암석 표면의 광분해 / 산화철 |
| `surface_morphology` | cratered rocky plains, tidally-locked | low | 데이터 없음. 조석 고정 아래 일반적인 따뜻한 암석 형태 |
| `planet_magnetic_field_polar_g` | ≥ 0.4 | medium | Trigilio et al. 2023 — ARE 전력 균형의 하한 (R_MP ≥ 1.6–2.0 R_planet). 첫 간접 외계행성 B-장 측정. Pineda & Villadsen 2023 의 Alfvén-Wing 시나리오는 ≳ 수 G 필요 |
| `magnetosphere_present` | true | medium | Trigilio 2023 — 복사된 SPI 전력이 R_MP ≥ 1.6 R_planet 인 magnetopause 를 요구. 즉 b 는 단순 ionosphere 장애물이 아니라 실제 자기권을 가져야 함 |
| `magnetosphere_standoff_planet_radii` | 1.6–2.0 | medium | Trigilio et al. 2023 — ARE 단면 요건에서 R_MP ≥ 1.6–2.0 R_planet |
| `spi_flux_tube_to_star` | true | high | Pineda & Villadsen 2023. Trigilio 2023 — b 가 sub-Alfvénic 영역에 있고 (a/R★ ≈ 21.9, R_Alf ≈ 100 R★) 항성 극으로 목성-이오 식 flux tube 를 구동 |
| `aurora_present` | true (radio; optical if atmosphere) | medium | 확인된 SPI 가 에너지 입자 침전을 함의. 전파 ARE 는 항성 극에 있지만 b 자신의 자기권이 입자를 그 극으로 channel |
| `star_apparent_angular_diameter_deg` | 5.12 | high | 유도값 = 2 · R★ / a · (180/π), R★ = 0.1571 R☉ |
| `stellar_illumination_color_temp_k` | 3100 | high | Cifuentes et al. 2020 호스트 Teff |

## Surface synthesis

YZ Cet b 는 통과나 식, 투과 측정이 없어, 표면에 관한 모든 것이
최소질량과 궤도, 호스트 조명에서 추론됩니다. 반지름 (0.913 R⊕) 은
관측이 아니라 준경험적 질량-반지름 추정입니다. SPI 단면에 반지름이
필요했던 Pineda & Villadsen 2023 은 지구형 밀도를 가정해 0.89–1.0 R⊕
로 bracket 했습니다. 최소질량 M sin i = 0.70 M⊕ (Stock 2020) 은 진짜
하한이고, 실제 질량은 1/sin i 만큼 더 큽니다. cfg 목적상 b 는
sub-지구질량~지구질량 암석 행성으로 다룹니다.

핵심 열적 사실은 b 가 **녹은 게 아니라 따뜻하다** 는 것입니다.
알베도 0 평형온도는 T_eq ≈ 471 K (여기서 L = 0.0022 L☉, a = 0.01634
AU 로 계산) 이고 일사량은 지구의 ~8.2 배입니다 — 높지만, M 왜성이
너무 어두워서 0.0163 AU 에서도 b 는 작은 궤도만으로 짐작되는 것보다
훨씬 차갑습니다. 이는 안쪽 TRAPPIST 세계와 같은 교훈입니다. 어두운
적색왜성을 바싹 끌어안은 행성이 자동으로 용암 세계가 되지는 않습니다.
substellar 맨 암석 정점 온도는 ~520 K 로, 마그마 바다가 아니라
금성 표면에 필적합니다.

**색 선택.** 호스트의 3100 K 적등색 조명 아래 b 는 따뜻한 색조의 철
함유 basalt 표면 (`#5a4438` primary) 에 산화철 patch accent
(`#7a3a22`) 으로 렌더링합니다. 이는 JWST 로 확인된 용암-암석
TRAPPIST-1 b 의 매우 어두운 airless ultramafic 검정 (`#1a1612`) 보다
의도적으로 따뜻하고 밝습니다. YZ Cet b 에는 신선-ultramafic, near-zero
알베도 표면을 강제하는 JWST 식이 없기 때문입니다 — 여기서 interesting
-first tie-break 는 밋밋한 검정 구체보다 눈에 띄게 텍스처가 있는
철-색조 따뜻한 암석을 선호합니다. 표면 색조는 low-confidence 입니다.
식이나 반사율 데이터가 없어 광물학이 제약되지 않고, 선택은 허용 범위
안의 미적 결정입니다.

**형태.** 조석 고정 (2.02 일 궤도가 시스템 나이 안에서 spin 을 동기
자전으로 damping) 이라 substellar 점이 고정됩니다. 기본 텍스처는
따뜻한 dayside 와 차가운 nightside 를 가진 cratered 암석 평원입니다.
확인된 재포장 메커니즘이 없으므로 TRAPPIST-1 b 와 달리 강제된 신선
-용암 지형은 없습니다 — 다만 얇은 substellar warm-spot 밝아짐은
허용되는 시각 터치입니다.

## Atmosphere synthesis

YZ Cet b 의 투과 스펙트럼이 없어, 대기는 전적으로 허용 범위 안의
합성 선택입니다. 두 물리적 고려가 이를 bracket 합니다. (1) T_eq ≈
471 K 와 ~8.2 배 지구 일사량에서 얇은 이차 대기는 열적으로 그럴듯하나
끊임없는 침식을 받고, (2) 호스트는 kG 자기장과 강한 항성풍을 가진
적당히 활동적인 flaring M 왜성이며 b 는 sub-Alfvénic 영역에서 항성
자기권 깊숙이 공전합니다 — 대기 유지에 적대적인 XUV·입자 환경입니다.

b 만의 결정적 반전은 **자신의 자기권** 입니다. Trigilio 2023 의 SPI
전력 균형은 b 가 항성풍에 대해 R_MP ≥ 1.6–2.0 R_planet 의 magnetopause
를 제시하기를 요구하고, 이는 b 가 단순 ionosphere 장애물이 아니라
실제 자기장 (극에서 ≥ 0.4 G) 을 가져야 함을 뜻합니다. 그 정도 자기권
이면 얇은 대기를 직접적인 항성풍 stripping 으로부터 부분적으로 보호할
것이라 — "얇은 대기" 해석이 비자화 근접 M-왜성 행성보다 b 에 대해 더
방어 가능합니다.

NearStars 에는 interesting-first tie-break 로 **얇은 이차 대기
(~0.1 bar, CO₂/N₂)** 를 채택하고, 보수적 airless 변형은 Open items 에
보존합니다. 이는 low-confidence 미적 선택입니다. 대기가 있으면 b 는
희미한 따뜻한 사지 haze (`#caa37a`) 와 약간의 주야 열 재분배를 가지며,
이는 맨 airless 구체보다 시각적으로 독특하고 — 요구되지는 않지만 —
자기권 추론과 일관됩니다.

**하늘 외형.** 얇은 대기가 있으면 3100 K 별 아래 낮 하늘은 천정 부근에
약한 Rayleigh 파랑을 띤 흐린 적등색입니다. b 가 대신 airless 라면
하늘은 검고 별 원반은 sharp-edged 입니다. 어느 쪽이든 호스트 별이
~5.1° 각지름 (지구에서 본 태양의 약 10 배) 으로 하늘을 지배하는 깊은
적등색이고, 두 바깥 형제 (c, d) 는 밝게 움직이는 "별" 로 보입니다.

## Rotation & spin synthesis

YZ Cet b 는 조석 고정입니다. 0.137 M☉ 별 주위 a = 0.0163 AU 에서 조석
고정 시간척도는 시스템 나이 (수 Gyr) 보다 훨씬 짧아, 행성은 2.02087
일 궤도와 동기 자전합니다. 이심률 (0.06 ± 0.06. Stock 2020) 은 제약이
약하고 원궤도와 일관됩니다. e ≲ 0.06 에서 1:1 spin-orbit 공명이 3:2
보다 강하게 선호됩니다 (Vinson 2017 / Makarov 2018. 3:2 는 상당한
삼축성과 함께 e ≈ 0.01 이상에서만 안정이고, 낮은-e RV 해는 이를
뒷받침하지 않음). 자전축 기울기는 0 으로 damping 됩니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 2.02087 일 = 174 603 s.
Kopernicus 에서 바디의 `rotationPeriod` 는 궤도 `period` 와 초 단위로
같습니다.

**계절 없음.** 자전축 기울기 = 0 과 거의 0 인 이심률에서 substellar
점은 표면 좌표계에 고정됩니다.

**SPI synodic 기하.** 전파 오로라의 가시성은 b 의 궤도와 항성 자전
사이 synodic 주기로 좌우됩니다. P_syn = [P_orb⁻¹ − P_rot⁻¹]⁻¹ ≈
2.082 d (Pineda & Villadsen 2023, P_rot = 68.46 d 사용). 이는 b 가
기울어진 항성 쌍극자에 대해 같은 위치로 돌아오는 cadence 이고, SPI
버스트가 b 의 궤도 위상 부근에서 — 정확히는 아니게 — 재발하는
이유입니다. cfg 에서 flux-tube footpoint 애니메이션은 2.02 일 궤도에
키잉하고 느린 68 일로 변조합니다.

## Visual styling

표면, 대기, 자기권 결정을 결합하면.

- **전체 색 팔레트.** 깊은 적등색 3100 K 빛 아래 따뜻한 철-색조 암석
  세계 (`#5a4438` primary, `#7a3a22` 산화 accent) — 확인된 용융 표면이
  없는 b 를 반영해, 검은 airless 용암-암석 안쪽 TRAPPIST 세계보다 밝고
  따뜻합니다.
- **Dayside.** 따뜻한 substellar 반구 (~520 K 정점) 에 텍스처 있는
  암석 평원. 얇은 대기가 있으면 희미한 따뜻한 사지 haze.
- **Terminator 띠.** airless 면 sharp 하고 고대비. 채택 시나리오에서는
  얇은-대기 산란으로 부드러워집니다.
- **Nightside.** 차가움. 얇은-대기 해석에서는 대기 재분배로 부분
  가열되고, airless 면 near-black. 충시 형제 c, d 의 반사광이 주된
  nightside 광원.
- **자기권 / 오로라 (헤드라인).** b 는 NearStars 에서 자기장이 간접
  측정된 (≥ 0.4 G. Trigilio 2023) 유일한 행성입니다. cfg 는 b 자신의
  자기권과 자기 극의 오로라 oval, 그리고 b 를 항성 자기 극에 잇는
  목성-이오 식 flux tube — 확인된 SPI 의 시각 표현 — 를 렌더링해야
  합니다. 오로라 밝아짐은 2.02 일 궤도에 키잉.
- **하늘의 별.** YZ Cet 은 b 의 하늘에서 ~5.1° (지구에서 본 태양의 약
  10 배) 를 차지하는 깊은 적등색 (3100 K → `#cf5630`) 으로, 적외선이
  풍부한 빛 ~8.2 배 지구 일사량으로 표면을 적십니다. 폭발 변광성
  호스트의 잦은 flare 가 조명을 점점이 끊습니다.
- **하늘의 형제 행성.** c 와 d 가 밝게 움직이는 점으로 보입니다.
  거의 동일평면 조밀계라 충이 잦습니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **2305.00809** Trigilio et al. 2023 — uGMRT 550–900 MHz 로 SPI 의 ARE
  를 4.37σ 로 확인. **행성 b 자기장 하한 B ≥ 0.4 G** (ARE 전력 균형에서
  R_MP ≥ 1.6–2.0 R_planet), magnetosphere-present 결정, sub-Alfvénic
  flux-tube 기하의 출처. 이 행성에서 가장 중요한 단일 논문이고 첫
  간접 외계행성 B-장 측정입니다.
- **2304.00031** Pineda & Villadsen 2023 — b 의 2.02087 d 궤도로
  folding 되는 VLA 2–4 GHz coherent 전파 버스트. SPI 구동체 식별
  (c/d 가 아니라 b), 반지름 bracket (지구형 밀도 시 0.89–1.0 R⊕),
  synodic-period 기하, 그리고 b 를 flux-tube 구동체로 만드는
  sub-Alfvénic 영역의 출처.
- **2020A&A...636A.119S** Stock et al. 2020 — b 의 궤도 (P = 2.02087 d,
  a = 0.01634 AU, e = 0.06) 와 최소질량 (0.70 M⊕), 준경험적 반지름
  추정 (0.913 R⊕) 의 Phase 2 recommended 출처.

### Read (context / methodology, not decision-driving)

- **2017A&A...605L..11A** Astudillo-Defru et al. 2017 — b/c/d 발견
  논문. 이전 궤도/질량 해 (P = 1.96876 d) 는 `recommended:false` 로
  보존. 시스템 구조의 맥락.
- 항성 합성 (`yz-cet.md`) — b 의 조명과 SPI 환경을 정하는
  Teff/L/R/M/활동/자기장 값.

### Read (instrument-only, not visual-informative)

- 두 SPI 논문의 전파-간섭계 방법론 (CASA 처리, Stokes V 동적 스펙트럼,
  hollow-cone ARE 모델) 은 자기장 수치를 떠받치지만 추가 시각 필드는
  주지 않습니다.

### Not read — no arXiv preprint or low-priority (~handful)

b 의 JWST, 통과, 투과-분광 논문은 없습니다 (b 는 통과하지 않음). 따라서
읽을 식/대기 문헌이 없습니다. 두 SPI 논문 안에 인용된 일반적인 M-왜성-풍
및 SPI-이론 참고문헌 (Saur 2013, Lanza 2009, Turnpenney 2018, Vidotto
2019) 은 맥락용으로 읽었지만 b-고유 cfg 수치는 주지 않습니다.

## Open items for follow-up

- **cfg 변형: airless b.** 채택된 얇은-대기 해석은 interesting-first
  tie-break 입니다. 보수적 airless 변형 (0 Pa, 검은 하늘, sharp 사지)
  은 작성자가 ship 할 수 있는 대안 cfg 로 여기 보존합니다. 자기권
  (≥ 0.4 G) 은 두 변형 모두에서 유지됩니다.
- **반지름은 측정이 아니라 추정.** b 는 통과하지 않습니다. 0.913 R⊕
  수치는 준경험적입니다. 미래 천체측정/직접영상 질량·반지름이 나오면
  표면 중력, 밀도, SPI 단면을 갱신해야 합니다.
- **자기장 정밀화.** ≥ 0.4 G 하한 (Trigilio 2023) 은 전체 ARE 고주파
  cutoff 가 측정되거나 미래 모니터링이 Alfvén-Wing 시나리오 (≳ 수 G
  필요. Pineda & Villadsen 2023) 를 선호하면 좁혀집니다. 자기장 강도와
  magnetopause standoff 를 그에 맞게 갱신.
- **대기 검출.** 미래 방출/위상-곡선 캠페인 (비통과 행성에는 도전적)
  만이 얇은 대기를 확인하거나 배제할 수 있습니다. 그때까지 압력은
  low-confidence 입니다.

## Related

- [yz-cet](yz-cet.md) — 호스트 별. kG 자기장이 이 행성에 SPI 를 정박시키는 M4.5 V flare star
- [yz-cet-c](yz-cet-c.md) — 다음 바깥 행성 (조밀계 중간)
- [yz-cet-d](yz-cet-d.md) — 최외측 행성
- [trappist-1-b](trappist-1-b.md) — 비교 최내측 M-왜성 암석 행성이나 JWST 로 확인된 airless 용암-암석. YZ Cet b 의 미측정 표면 및 확인된 자기권과 대비
- [methodology](../reference/methodology.md) — Decisions 표와 confidence 태그의 스키마
