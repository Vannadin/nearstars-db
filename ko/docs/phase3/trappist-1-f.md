<!-- TRAPPIST-1 f Phase 3 synthesis: cfg-ready 결정과 근거 -->
# TRAPPIST-1 f — Phase 3 Synthesis

TRAPPIST-1 f 는 M8V ultra-cool dwarf 를 9.21 일 주기로 도는 1.04 R⊕,
1.04 M⊕ 의 암석 행성입니다. 안쪽에서 다섯 번째 행성이며 지구 일조량의
0.38배를 받습니다 — 보수적 거주 가능 영역의 바깥, maximum-greenhouse
한계 근처에 자리합니다 (Kopparapu 2013). 질량과 반경이 시스템 전체에서
지구와 가장 비슷하지만, Agol 2021 의 bulk density 가 4.92 g/cc 로 충분히
낮아 f 는 상당량의 물을 품은 워터 월드일 가능성이 높습니다. Acuña 2025
(2504.16201) 는 water mass fraction 을 16.2% ± 9.9% 로 추정합니다.
f 에 대한 첫 NIRISS 대기 정찰 (Lim 2024, ADS bibcode 2024ESS.....510106L;
arXiv preprint 없음) 은 구름 없는 수소 풍부 대기를 배제했지만 2차 대기에는
강한 제약을 걸지 못했습니다.

**NearStars 시나리오 선택. 얇은 CO₂-rich 대기 (~0.1 bar) 를 가진 전역
얼음 덮인 해양 세계로, 상승된 CO₂ 온실효과와 radiogenic heat 에 의한
basal melting 이 substellar 점 근처에 작은 open-water lens 를
유지합니다.** Wolf 2017 / Wunderlich 2020 의 outer-HZ frozen-ocean
시나리오를 채택하되, substellar open water 는 Pierrehumbert 2011 /
Hu 2014 의 조석 lock aquaplanet hysteresis 에서 동기를 얻습니다. 대안인
substellar open water 가 없는 완전한 snowball 해석은 cfg 변형으로
보존합니다.

## 결정

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 9.21 d 궤도, 조석 damping; Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping; Agol 2021 |
| `eccentricity` | 0.01007 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 8.81 | medium | Agol 2021 |
| `sidereal_period_days` | 9.2075 | high | Agol 2021 |
| `semi_major_axis_au` | 0.03849 | high | Agol 2021 |
| `mass_mearth` | 1.039 | high | Agol 2021 TTV |
| `radius_rearth` | 1.045 | high | Agol 2021 |
| `surface_gravity_g_earth` | 0.952 | high | derived = 1.039 / 1.045² |
| `density_g_cc` | 4.92 | high | Agol 2021 |
| `water_mass_fraction` | 0.07–0.16 | high | Acuña 2025 — MAGRATHEA 내부 fit; mantle-to-core 비율에 따라 달라짐 |
| `insolation_s_earth` | 0.38 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 215 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0.5, snowball) | 188 | high | derived; high-albedo snowball 케이스 |
| `bond_albedo` | 0.45 | medium | snowball 얼음 + 부분 구름 cover; Wolf 2017 |
| `surface_temp_substellar_k` | 260 | medium | Wolf 2017 + 0.1 bar CO₂ 온실효과로 좁은 open-water disk 유지 |
| `surface_temp_nightside_k` | 165 | medium | Wolf 2017 GCM; 얼음으로 덮인 차가운 nightside |
| `surface_temp_global_mean_k` | 220 | medium | Wolf 2017 GCM cold-snowball 범위 |
| `atmosphere_present` | true (얇은 CO₂-rich) | medium | Lim 2024 가 H₂-rich 배제, 얇은 CO₂ 는 허용; Wolf 2017 outer-HZ snowball 케이스 |
| `atmosphere_surface_pressure_pa` | 10 000 | medium | 0.1 bar CO₂ — substellar 부분 open water 를 유지할 수 있는 최소값 (Wolf 2017) |
| `atmosphere_composition` | CO₂ 95%, N₂ 4%, 미량 H₂O / Ar | medium | outgassing 주도; Wolf 2017 cold-snowball + Wunderlich 2020 dry-f branch |
| `atmosphere_scale_height_km` | 6.5 | medium | derived. kT/μg, T≈220 K, μ=43 (CO₂-rich), g=9.3 m/s² |
| `atmosphere_tint_rgb_hex` | `#604040` (매우 얇은 CO₂ Rayleigh + 먼지 haze) | low | 0.1 bar 에서 산란이 미미; CO₂ ice haze 약간 가능 |
| `cloud_cover_fraction` | 0.25 | medium | Wolf 2017 — 차갑고 얇은 대기에서는 구름 형성이 제한됨 |
| `cloud_tint_rgb_hex` | `#d8c8b8` (CO₂ 얼음 + 물 얼음 혼합, M-dwarf 적색 이동) | medium | terminator + substellar cirrus |
| `ocean_present` | true (sub-glacial; 작은 substellar open-water lens) | medium | Acuña 2025 wmf 16%; basal melting + 온실효과로 marginal 한 open water |
| `ocean_extent_substellar_radius_deg` | 8 | medium | Wolf 2017 — 0.1 bar CO₂ 아래에서 좁은 open-water disk |
| `ocean_tint_rgb_hex` | `#1a1c30` (깊고 어두운 navy, 대부분 얼음 아래) | low | sub-glacial / 작은 lens; 궤도에서 거의 보이지 않음 |
| `surface_ice_caps` | substellar ~8° disk 바깥 전역 cover; 표면의 ~95% | medium | snowball / "lobster-pot" eyeball; Pierrehumbert 2011 |
| `surface_tint_rgb_hex_primary` | `#e0d8d0` (깨끗한 눈 / 빙하 얼음) | medium | 눈 albedo + M-dwarf 조명 |
| `surface_tint_rgb_hex_accent` | `#888070` (먼지로 얼룩진 CO₂ frost + 능선 정상의 노출된 기반암) | low | nightside CO₂ frost over ice; 얇은 sublimation lag |
| `surface_morphology` | 얼어붙은 해양 위의 전역 빙하 얼음; pressure-ridge 지형; terminator 능선에 기반암 노출 | medium | tidally-locked snowball; Wolf 2017 |
| `magnetic_field_present` | true (약함, ~0.05× 지구) | low | 작은 질량 + 차가운 내부 + 느린 자전 |
| `induction_heating_w_m2` | 0.005–0.05 | medium | Grayver 2022 — f 의 거리에서는 미미 |
| `tidal_heating_w_m2` | 0.0005–0.005 | medium | Bolmont 2020 — f 에서는 최소 |
| `radiogenic_heat_w_m2` | 0.04 | medium | 지구 analog mantle radiogenics × 1 |
| `star_apparent_angular_diameter_deg` | 1.65 | high | derived. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |

## 표면 합성

TRAPPIST-1 f 는 보수적 거주 가능 영역 (Kopparapu 2014) 의 바깥 가장자리에
자리하며 지구 일조량의 38% 를 받습니다. 유의미한 온실 가열이 없으면 표면이
전역적으로 얼어붙습니다 (Wolf 2017 §5). 0.1 bar CO₂ 가 있을 때 Wolf 2017
는 좁게 갇힌 substellar open-water disk 가 유지될 수 있음을 보였지만,
그 기하 구조는 취약하고 초기 상태에 의존합니다 (Pierrehumbert 2011 의
aquaplanet 와 snowball 사이 bifurcation).

Acuña 2025 (2504.16201) 가 현재 최선의 내부 fit 을 제공합니다. 모든 내부
파라미터의 변화를 허용하면 water mass fraction 이 16.2% ± 9.9%, 또는
mantle-to-core 비율을 지구형으로 고정하면 6.9% ± 2.0% 입니다. 어느 쪽이든
f 는 지구보다 상당히 더 hydrated 된 행성이며 — 전역 얼음 cover 아래에
전역 액체 물 층을 가진 진정한 "ocean world" 일 가능성이 큽니다.

Bourgeois 2024 (2008.09599) 의 magma-ocean 진화 작업은 f 가 100 Myr
이상 지속된 magma ocean 단계를 거치며 상당량의 대기 물과 산소를 만들어냈음을
시사합니다. 그 후 대부분의 물은 mantle 로 재평형되거나, 광분해 탈출로
우주로 손실되거나, 행성이 식으면서 표면에 응결되었습니다. 지금 남아 있는
sub-glacial ocean 과 얇은 CO₂ 대기가 장기적 endpoint 에 해당합니다.

표면 morphology 의 경우 tidally-locked snowball 템플릿은 다음의 구조를
줍니다.

- **Substellar disk** (substellar 점에서 ≲8°). open-water lens 가능;
  그렇지 않다면 국지적 균열을 동반한 얇은 얼음. 표면 T ≈ 260 K 는 얼음과
  물 평형의 marginal 케이스에 해당.
- **빙하 얼음 영역** (substellar 에서 8–180°). sub-glacial 액체 물 ocean
  위의 두꺼운 (>1 km) 빙하 얼음. 표면 T 는 ice line 의 ~250 K 에서
  antistellar 점의 ~170 K 까지 단조 감소.
- **Terminator** (substellar 에서 ~90°). 차갑고 (~190 K) 어두움; 가장
  사진발이 좋은 영역으로, 2566 K 빛이 비스듬히 비추는 가운데 pressure
  ridge 가 긴 그림자를 드리움. 빙하 흐름이 지각 highs 위에서 얼음을 얇게
  만든 곳에서는 기반암 노출도 가능.

**색 선택.** 눈과 빙하 얼음의 albedo 는 깨끗하고 신선한 경우 0.6–0.8,
먼지로 얼룩져 노화된 경우 0.4–0.6 입니다. M-dwarf 조명 아래에서는 청-백색이
아닌 따뜻한 크림색 (`#e0d8d0`) 으로 보입니다. nightside 의 CO₂ frost 가
어두운 패치에 약간의 황갈색 tint 를 더합니다 (`#888070`).

**산화철 / 기반암.** 노출은 제한적입니다 — terminator 근처 능선 정상에서
빙하 흐름이 얼음을 얇게 만든 곳에서만 드러납니다. f 의 거리에서는 별의 UV
가 약하고 지속적인 얼음 cover 가 대부분의 기반암을 광분해 산화로부터
보호하기 때문에, 산화철 tint 는 안쪽 행성 (b, c) 에 비해 훨씬 희미합니다.

**조석 lock 하의 morphology.** 얼음 순환이 핵심입니다. substellar 점의
표면 가열이 얼음을 sublimate 시키며 (얇은 대기 탓에 속도는 낮음), CO₂ 와
미량 H₂O 는 대기 순환을 통해 더 차가운 terminator 와 nightside 로 운반되어
응결합니다. 그 후 빙하 흐름이 얼음을 다시 substellar disk 쪽으로 되돌리며,
결과적으로 substellar 점에 지속적인 얇은 open-water lens 를 유지하는 안정한
얼음 순환이 성립합니다.

## 대기 합성

f 에 대한 Lim 2024 NIRISS 정찰 (arXiv preprint 없음, conference abstract
ADS bibcode 2024ESS.....510106L) 은 f 의 첫 JWST transmission 관측을
보고합니다. 결과는 다음과 같습니다. H₂-rich 대기는 배제되며 Moran 2018
(1810.05210) 의 HST 한계와 일관되지만, 2차 대기 (CO₂, N₂, H₂O-rich) 는
현재 가용한 transit baseline 으로는 제약되지 않습니다. 즉 f 의 관측적 그림은
b, c, d, e 보다 훨씬 더 열려 있습니다.

이론적 모델링 (Wolf 2017 §5, Lincowski 2018, Wunderlich 2020) 은 f 가
조금이라도 거주 가능하거나 온화하려면 유의미한 CO₂ 온실효과가 필요하다는
점에 일치합니다 — Wolf 2017 는 완전한 open ocean 에는 1 bar CO₂, 0.1 bar
에서는 좁은 substellar disk, 그보다 낮으면 완전한 snowball 이 된다고
봅니다.

NearStars 는 **substellar open-water lens 를 가진 0.1 bar CO₂-rich
snowball** 을 채택합니다.

- **압력** 0.1 bar (10 kPa). Wolf 2017 §5 는 이 값이 f 의 일조량 아래에서
  부분 substellar open water 를 유지할 수 있는 최소값임을 보였습니다.
- **조성** CO₂ 지배 (95%), 미량 N₂ (4%), 미량 H₂O (terminator cold-trap
  에서 포화), 미량 Ar. CO₂ 가 풍부한 이유는 표면이 얼어붙어 액체 물 풍화로
  CO₂ 를 제거할 carbonate-silicate cycle 이 작동하지 않는 행성에 화산
  outgassing 이 시간에 걸쳐 누적되기 때문입니다.
- **구름.** 제한적 (~25% 전역). substellar disk 근처의 물 얼음 cirrus
  와 terminator 의 희미한 CO₂ 얼음 구름.

**하늘 외관.** 0.1 bar CO₂ 대기는 Rayleigh scattering 이 지구의 ~5% 정도이고,
M-dwarf SED 가 단파장 기여를 추가로 깎아 내립니다. substellar 근처 하늘은
별이 압도적으로 지배하는 가운데 희미한 dark-rust (`#604040`) 톤을 띠며,
terminator 근처에서는 CO₂ 얼음 구름의 forward-scattering 으로 limb 에
희미한 cyan-white 가 비치는 것을 제외하면 하늘이 어둡습니다.

## 자전 & spin 합성

7.6 Gyr 에 걸친 9.21 일 주기의 조석 damping 이 f 의 동기 (1:1) 구성을
확립합니다. 황도 경사각은 0 으로 damping 됩니다. 이심률은 0.01007 로 —
3:2 spin-orbit 가 marginally 안정해지는 상단 가장자리에 해당하지만
(Vinson 2017), 1:1 이 여전히 압도적 확률의 상태로 남습니다.

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 9.2075 일 (795 528 s).

**계절 없음.** 황도 경사각 = 0; libration 유도 일조량 변동은 ~ 1%
입니다 (e 보다 이심률이 높아 안쪽 행성보다 약간 큼). substellar 점은
본질적으로 고정되어 있습니다.

## 비주얼 스타일

- **전역 외관.** 궤도에서 본 f 는 substellar 점에 작은 어두운 spot
  (open-water lens, `#1a1c30`) 이 박힌, 거의 균일한 따뜻한 크림색 snowball
  (`#e0d8d0`) 입니다. 구름 cover 는 제한적이며 substellar disk 위로 가끔
  cirrus 가 지나갑니다. antistellar 반구는 CO₂ frost 로 약간 황갈색이
  얼룩진 얼음을 보입니다.
- **Substellar disk (open water).** ~16° 너비 (반경 8°) 의 작은 어두운
  패치. 주변의 따뜻한 크림색 얼음과 대비가 극적입니다.
- **빙하 얼음.** 보이는 표면의 대부분을 차지합니다. 큰 스케일에서는
  매끄럽지만 terminator 의 비스듬한 빛 아래에서는 pressure ridge 와
  crevasse 가 드러납니다. 신선한 눈 (`#e0d8d0`) 과 먼지로 얼룩지거나 다시
  얼어붙은 얼음 (`#c8c0b0`) 사이에 미묘한 색 변화가 있습니다.
- **Terminator band.** 비스듬한 빛 아래 지형 대비가 큽니다. 능선 정상에
  기반암 노출이 있을 수 있습니다 (`#888070` accent).
- **Nightside.** CO₂ frost 가 만든 어둑한 크림-황갈색 톤. KSP nightside
  ambient 는 dayside 의 2–5% 수준.
- **Atmosphere haze.** 매우 얇은 따뜻한 회-적색 limb glow (`#604040`),
  두께는 5–10 km, 행성 limb 의 공간 배경에 대해서만 보입니다.
- **하늘의 별.** TRAPPIST-1 은 f 의 하늘에서 1.65° 를 차지합니다 (지구에서
  본 태양의 3배) — 깊은 적-오렌지 disk 로 나타납니다. 표면 조명은
  0.38 S⊕ 로 지구의 깊은 황혼과 비슷하며, 별의 어둑한 적색 빛이 설경에
  영구적인 새벽빛 tint 를 부여합니다.
- **하늘의 자매 행성.** e (다음 안쪽) 가 inferior conjunction 시 각 크기
  ~0.3°; g (다음 바깥쪽) 가 outer conjunction 시 ~0.3°. 합은 약 25 일
  마다 일어납니다 (f-g synodic 주기).

## 참고 문헌

### 읽음 (시각-정보 제공, 위 결정 견인)

- **2504.16201** Acuña 2025 — MAGRATHEA 를 이용한 f 의 내부 구조 분석.
  wmf 16.2% ± 9.9% (free CMF) 또는 6.9% ± 2.0% (지구형 mantle-to-core).
  f 를 ocean world 로 확립하며, sub-glacial ocean cfg 를 견인.
- **2008.09599** Bourgeois 2024 — e/f/g 의 magma ocean 진화. f 가 진화를
  거치며 상당량의 물을 보유했다고 예측.
- **2006.11349** Wunderlich 2020 — e 와 f 의 wet vs. dry 대기. f 의 대기를
  CO₂-rich (snowball branch) 또는 dry desiccated post-runaway 상태로 제약.
- **1809.07498** Lincowski 2018 — TRAPPIST-1 세계들의 진화한 기후. f 는
  Lincowski 의 모델링이 차갑고 CO₂-rich 한 대기를 평형으로 보여주는 행성
  중 하나. d Phase 3 / e Phase 3 에서 이미 읽음.

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **2605.06964** TRAPPIST-1 기후의 에너지 균형 모델. 방법론 논문이며 f 의
  snowball 상태를 지지.
- **2506.21351** SEPHI 2.0 거주 가능성 지수. 카탈로그 맥락만.
- **2502.00132** Way 2025 — d 중심 논문이지만 f 에도 적용되는 tidally-locked
  GCM 의 유용한 방법론 reference.
- **1810.05210** Moran 2018 — HST haze 한계. d Phase 3 에서 이미 읽음.

### 읽음 (instrument-only, 시각 정보 아님)

(이 깊이에서 f 에 특화된 항목 없음.)

### 읽지 않음 — arXiv preprint 없음 또는 낮은 우선순위 (~9 편)

f 의 참고 문헌은 매우 작습니다 (15 편, arXiv 6 편).

- **2024ESS.....510106L** Lim 2024 — TRAPPIST-1 f NIRISS 대기 정찰.
  **f 의 핵심 관측 논문이지만 arXiv preprint 가 없음.** ADS 초록만 가용.
  대기 추론 (H₂-rich 배제, 2차 대기 미제약) 은 초록에서 가져왔음. **arXiv
  preprint 가 등장하면 fetch 하도록 flag.**
- **2025arXiv...** biosignature feasibility 와 ELT 특성화에 관한 다양한
  conference 요약. Skip.

---

## 후속 follow-up 항목

- arXiv preprint 가 가용해지면 Lim 2024 NIRISS f 논문을 재fetch. 공식
  출판 버전이 2차 대기 제약을 강화할 가능성이 있음.
- 0.1 bar CO₂ 선택은 Wolf 2017 의 모델링으로 bracket 되지만 f 특화 관측으로
  직접 제약되는 값은 아님. 미래의 JWST emission 분광이 f 의 dayside 가
  현재 모델 예측보다 더 차갑다는 점을 드러내면, CO₂ 압력을 낮추거나 (혹은
  0 으로 설정해 완전한 snowball 로) 조정해야 함.
- "완전한 snowball" (substellar open water 없음) 해석을 위한 cfg 변형 —
  시각적으로 더 단순한 완전 백색 크림 세계. substellar lens 가 KSP 에서
  의미 있게 렌더되기에 너무 marginal 한 것으로 드러나면 사용.
- "1 bar CO₂ + 완전한 ocean" 해석을 위한 cfg 변형 (Wolf 2017 §5
  best-case). 시각적으로 e 와 비슷하지만 더 차갑고 얼음 띠가 많은 모습.
  더 깊은 거주 가능 영역 대안을 원할 때 사용.
- water mass fraction (7–16%) 이 충분히 높아서 f 는 Europa 와 비교 가능한
  sub-glacial 액체 물 층을 가질 가능성이 있음 — 조석이나 radiogenic 가열이
  해저까지 닿는다면 hydrothermal 활동까지 동반할 수도 있음. 직접적인 시각
  요소는 아니지만 Principia annotation 으로 남길 만한 가치가 있음.
