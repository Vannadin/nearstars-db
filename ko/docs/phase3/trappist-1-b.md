<!-- TRAPPIST-1 b Phase 3 합성. cfg-ready 결정과 그 근거 -->
# TRAPPIST-1 b — Phase 3 Synthesis

TRAPPIST-1 b 는 M8V ultra-cool dwarf 를 1.51 일 주기로 도는 1.12 R⊕,
1.37 M⊕ 의 암석 행성입니다. TRAPPIST-1 의 일곱 세계 중 가장 안쪽에
있고, 지구 일사량의 4.3 배를 받습니다. JWST MIRI 의 12.8 μm 과 15 μm
secondary-eclipse 측정(Greene 2023, Ducrot 2024)과 전체 thermal phase
curve(Ducrot 2025)가 결합되어, 이 시스템에서 가장 깨끗한 "맨 암석"
답을 내놓고 있습니다. dayside brightness temperature 는 약 490–503 K,
nightside emission 은 검출되지 않고, thermal phase offset 도 없습니다.
~0.3 bar 이상의 두께를 가지면서 현실적인 CO₂ 함량을 가진 대기는 3σ
수준에서 모두 배제됩니다.

**NearStars 시나리오 선택은 substellar 점 부근에 국지적인 신선한
마그마 지형을 갖는 대기 없는 ultramafic 암석 표면입니다.** 이는
Ducrot 2024 가 선호한 해석(미풍화 ultramafic 표면은 최근 또는 진행 중인
지질학적 재포장을 함의)과 부합하며, Grayver 2022 / Bolmont 2020 의
induction-heating "exo-Io" 정황을 통합한 것입니다. 대안으로 광화학
haze 와 성층권 inversion 을 갖는 순수 CO₂ 대기 시나리오도 데이터상
형식적으로는 허용되지만, 우주화학적 근거에서 선호되지 않습니다 — b
가 그런 CO₂ 대기를 가졌다면 두 칸 바깥의 c 에는 CO₂ 가 살아남을 수
없기 때문입니다.

## 결정

Kopernicus / atmosphere cfg-ready 값입니다. `Confidence` 표기는
high = 직접 측정되었거나 강하게 제약됨, medium = 강한 근거를 갖춘
이론, low = 허용 범위 안에서의 미적 선택을 뜻합니다.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 1.51 d 궤도와 조석 damping. Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping. Agol 2021 |
| `eccentricity` | 0.00622 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 337 | medium | Agol 2021 (낮은 ecc 라 제약이 약함) |
| `sidereal_period_days` | 1.5109 | high | Agol 2021 |
| `semi_major_axis_au` | 0.01154 | high | Agol 2021 |
| `mass_mearth` | 1.374 | high | Agol 2021 TTV |
| `radius_rearth` | 1.116 | high | Agol 2021, Greene 2023 transit fit |
| `surface_gravity_g_earth` | 1.103 | high | 유도값 = 1.374 / 1.116² |
| `density_g_cc` | 5.43 | high | Agol 2021 |
| `insolation_s_earth` | 4.25 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 397 | high | Agol 2021 |
| `dayside_brightness_temp_k_15um` | 503 | high | Greene 2023 F1500W eclipse |
| `dayside_brightness_temp_k_phase_curve` | 490 | high | Ducrot 2025 MIRI 15 μm phase curve |
| `bond_albedo` | 0.0 | high | Greene 2023, Ducrot 2025 — dayside-only 재복사 |
| `atmosphere_present` | false | high | Ducrot 2025 phase curve 가 ≳1 bar greenhouse 를 배제 |
| `atmosphere_surface_pressure_pa` | 0 | high | Ih 2023 이 0.3 bar 이상의 그럴듯한 대기를 배제 |
| `atmosphere_composition` | n/a (airless) | high | Greene 2023, Zieba 2023 (자매 행성 제약) |
| `atmosphere_scale_height_km` | n/a | high | airless |
| `atmosphere_tint_rgb_hex` | n/a | high | airless |
| `dayside_surface_temp_k` | 503 | high | 측정 brightness temp 과 일치. Ducrot 2025 |
| `substellar_peak_temp_k` | 620 | medium | 맨 암석 subsolar 유도값 (A=0, ε=1, advection 없음) |
| `nightside_surface_temp_k` | 80 | medium | airless 이고 재분배 없음, passive radiative 한계 |
| `surface_tint_rgb_hex_primary` | `#1a1612` (어두운 ultramafic basalt) | medium | Ducrot 2024 의 "fresh ultramafic" + 달 mare 유사체 |
| `surface_tint_rgb_hex_accent` | `#7a2a10` (substellar 부근의 식어가는 용암 + 산화철) | low | induction heating 과 신선한 용융 patch. Grayver 2022 |
| `surface_morphology` | substellar 점 부근에 신선한 용암류와 어두운 마그마 pond 가 있는 basalt 평원 | medium | Ducrot 2024 미풍화 표면 추론, Grayver 2022 induction heating |
| `induction_heating_w_m2` | 0.4–4 | medium | Grayver 2022 (2211.06140) — 비자화 층상 전도도 가정의 결과값입니다. 자화된 지구형 다이나모 분기에서는 최대 ~200 W/m² (표면적 환산 139 TW) 까지 올라가지만, b 가 다이나모를 가졌다는 관측적 증거는 없습니다 |
| `surface_ice_caps` | 없음 (nightside 에서 승화 / 광분해) | high | dayside 500 K, volatile 을 가둘 대기 없음 |
| `star_apparent_angular_diameter_deg` | 5.51 | high | 유도값. 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |
| `tidal_heating_w_m2` | 0.5–1 (낮은 e) 에서 최대 ~400 (max-e, JWST 캡) | medium | Bolmont 2026 (2601.03408) — 내부 구조 의존. JWST nightside 비검출이 Φ 를 ~407 W/m² (Φ_2σ) 로 캡 |

## 표면 합성

Ducrot 2024 는 결합 12.8 / 15 μm eclipse fit 을 통과하는 대기-또는-표면
모델을 두 개 찾아냈습니다. 하나는 광화학 haze 를 가진 두꺼운 순수 CO₂
대기(성층권 inversion 을 만들고 emission 으로 나타나는 CO₂ feature 를
생성)이고, 다른 하나는 — 그리고 더 선호되는 — **미풍화 ultramafic
표면**을 가진 대기 없는 행성입니다. ultramafic 해석은 중요한 의미를
갖습니다. 달의 풍화된 basalt(regolith 노화)는 broadband albedo 는 낮지만
15 μm 영역의 emissivity 가 데이터와 맞지 않는 반면, 신선한(지질학적으로
어린) ultramafic 표면은 데이터에 부합합니다. 이는 진행 중이거나 최근에
일어난 지질학적 재포장을 함의합니다.

Ducrot 2025 phase curve 는 이 결론을 굳혔습니다. nightside emission 은
검출되지 않고(15 μm 에서 ≲39 ppm), phase offset 도 없으며, dayside flux
는 낮은 Bond albedo 와 비효율적인 열 재분배를 갖는 맨 암석 모델과
일치합니다. b 관련 문헌 전반의 결론은 한결같습니다. **b 는 맨, 신선하고
어두우며 뜨거운 암석입니다.**

**재포장 메커니즘.** 물리적으로 그럴듯한 두 가지 동인이 있습니다.
(1) 공명 사슬에서 비롯되는 조석 가열입니다. Bolmont 2026 (2601.03408)
은 과거 추정치를 상당히 상향 조정했는데, b 의 측정된 핵 질량비
범위(Agol 2021. 약 21 wt%)와 가장 작은 그럴듯한 이심률 조합에서 표면
flux 는 **명목상 약 0.5–1 W/m²**로, Io 의 ~2 W/m² 에 견줄 만합니다. 더
높은 이심률 해는 10²–10³ W/m² 까지 올라가지만, JWST nightside 제약
(Gillon 2025. T_2σ ≤ 291 K → Φ_2σ ≤ 407 W/m²)에 의해 배제됩니다. 보수적인
~0.5 W/m² 값만 잡아도 화성의 방사성 ~0.04 W/m² 를 한 자릿수 차이로
압도합니다. (2) 자기 induction heating (Grayver 2022, Cohen 2024) 은
행성이 항성풍 속을 가르면서 추가로 0.4–4 W/m² 를 보탭니다. 이 둘을
합친 열 예산은 부분 용융 화산활동을 충분히 유지할 수 있습니다. 시스템
나이가 7.6 Gyr 임을 감안하면, 표면은 지각 약점부에서 용암류로 끊임없이
새로워지고, 일사가 상부 지각을 solidus 쪽으로 가장 가깝게 미는
substellar 반구로 그 활동이 편향됩니다.

**색 선택.** 호스트별은 SED 피크가 1.1 μm 근처인 2566 K M8V dwarf 라,
인간 관찰자가 인지하는 표면 reflectance 는 본래 광물색과 무관하게 강하게
적색쪽으로 치우칩니다 (일반적인 M-dwarf 표면 조명 처리는 Domagal-Goldman
2010 참조). 신선한 ultramafic 표면(komatiite / olivine-pyroxene 유사체,
broadband visible albedo ≈ 0.03–0.08) 에 가장 가까운 태양계 reference 는
수성의 어두운 dorsa 또는 어린 달 크레이터의 미풍화 floor 입니다. primary
는 `#1a1612` (매우 어두운 ultramafic), accent 는 `#7a2a10` (식어가는 용암의
적색)으로 substellar 사분면 쪽으로 치우치게 잡았습니다.

**산화철.** d 보다는 덜 두드러집니다. Ducrot 2024 의 "fresh" ultramafic
추론은 의미 있는 풍화를 적극적으로 배제하기 때문에, d 에 비해 산화철
patch 는 최소화합니다. 산화물이 존재한다면 표면 물질이 항성 UV 에 노출은
되지만 최근에 재포장되지 않은 terminator 와 antistellar 반구로
치우치도록 배치하는 것이 맞습니다.

**지형.** 기여하는 과정은 세 가지입니다. (1) 조석과 induction heating 이
구동하는 부분 용융 화산활동에 의한 지속적 재포장(Bolmont 2020, Grayver
2022)으로, 주로 substellar 반구에 신선한 용암류와 shield-volcano
지형이 형성됩니다. (2) ~8 Gyr 에 걸친 누적 충돌은 조석 고정된 frame
에서 leading 반구 쪽으로 편향되지만, 진행 중인 화산활동에 의해 부분적으로
지워집니다. (3) 강착 직후 ~500 Myr 단계의 마그마 바다 잔존 지형도 있습니다
(Piaulet 2025 §8 가 d 에 대해 제시한 논거를 b 로 확장한 것 — b 는 초기
에너지 flux 가 더 강했고, 그래서 마그마 바다를 더 오래 유지했을 것임).
기본 텍스처는 substellar 점에서 방사상으로 뻗어 나가는 용암류 채널이
보이고 trailing 반구 고지대 쪽으로 충돌 크레이터가 집중되는, 어둡고
유리질의 basalt 평원입니다.

## 대기 합성

JWST MIRI 15 μm 광도측정 eclipse(Greene 2023, 다섯 visit, 8.7σ 검출)
가 Fp/F★ = 861 ± 99 ppm 을 내놓았고, 이는 dayside brightness
temperature 약 503 +26/-27 K 에 해당합니다. Ih 2023 은 이 값으로 대기
질량을 제한했는데, CO₂ 가 100 ppm 이상 들어 있는 어떤 그럴듯한 대기도
0.3 bar 이상에서 3σ 로 배제되며, 화성형 6.5 mbar 순수 CO₂ 대기도 3σ
로 배제됩니다.

Ducrot 2024 는 12.8 μm eclipse(CO₂ 의 15 μm feature 의 in-band) 를
추가하여 12.8 μm 에서 Fp/F★ = 452 ± 86 ppm, 15 μm 에서 775 ± 90 ppm
을 얻었습니다(결합 재분석). 2σ 에서 살아남는 모델은 두 개입니다. 대기
없는 ultramafic 표면(선호)과, 성층권 inversion 을 만드는 광화학 haze
를 갖는 두꺼운 순수 CO₂ 대기입니다(단, 후자는 특정 haze 화학을 요구한다는
단서가 붙습니다).

Ducrot 2025 가 사실상 사건을 종결시켰습니다. MIRI 15 μm phase curve
는 dayside brightness temperature 490 ± 17 K, nightside flux 비검출
(F_night,max = 39 +55/−27 ppm), 측정 가능한 phase offset 부재를
보여줍니다. 표면 압력 ≥1 bar 와 의미 있는 greenhouse 효과를 갖는 대기
모델은 배제되고, b 는 "어떤 실질적인 대기도 보유하지 않을 가능성이
높음"으로 정리됩니다.

이론 쪽에서 두 편의 논문이 독립적인 근거로 airless 해석을 보강합니다.
**2412.05188** (Chatterjee & Pierrehumbert 2024) 은 b 를 수정된 cosmic
shoreline 의 "catastrophic escape" 영역 깊숙이 위치시킵니다. 현재 b 의
XUV flux(지구 XUV 의 ~10³ 배, pre-main-sequence 초광도 시기에는
~10⁴–10⁵ 배)에 맞서서는 지속적인 화산 outgassing 으로도 2차 대기를
재건할 수 없습니다. **1911.08878** (Turbet 2020) 은 지구형 핵 조성과
측정된 손실율 0.19%/Gyr 을 가정할 때 b 가 보유할 수 있는 최대 물 질량비가
≤ 2% 임을 보여, b 가 "오늘날 거의 완전히 건조"라는 추론을 뒷받침합니다 —
airless 표면과 일관됩니다.

**초기 수분 역산.** Gialluca 2024 (2405.02401) 는 "b 는 airless, c 는 얇은 O₂ 대기 보유"라는 결합 제약 아래 MCMC fit 을 수행하여 초기 표면 수분량을 8.2 +1.5/-1.0 지구 해양(1σ)으로 산출합니다. 메커니즘별로 풀어보면, ~3 TO 는 마그마 바다에 격리되고, ~4 TO 분량의 산소는 유체역학적 drag 로 손실되며, 건조화 이후 ~385 bar 가량이 건조 지각 산화로 소비되는 그림입니다. 역사적 baseline 인 Bolmont 2017 (1605.00616) 은 시스템 수명 동안 b 한 행성에서만 최대 13.5 EO 의 수소가 손실되었고, 산소 sink 가 비효율적이었다면 그 결과로 ~422 bar 까지 무기 기원 O₂ 가 축적될 수도 있었다고 봤습니다. Gialluca 의 정밀화는 그 상한과 하한을 동시에 좁혀 줍니다.

방법론적 단서가 하나 있습니다. **2601.12556** (Wirth, Powell & Wordsworth
2026) 은 b 가 Λ ≤ 1 (Weak Temperature Gradient 가정이 깨지는 영역)
이라는 점을 짚어, 열 재분배만으로 b 의 대기에 부과하는 상한은 흔히
가정하는 것보다 약하다고 지적합니다. 다만 Ih 2023 의 0.3 bar 상한은
재분배가 아니라 15 μm CO₂ 분자 흡수를 직접 사용한 결과라 여전히
유효하고, Ducrot 2025 phase curve 는 재분배 자체를 직접 측정한 것이라,
이 단서가 airless 결정을 흔들지는 않습니다.

NearStars 에서는 **완전 airless** 해석을 채택합니다.

- **압력.** 정확히 0 Pa 입니다. 12.8/15 μm 데이터와 호환되는 "CO₂ +
  haze" 시나리오는 이웃 행성 c 에서 CO₂ 가 부재한다는 사실(Zieba 2023)
  과 충돌하므로 폐기합니다. 일사가 더 낮고 cosmic shoreline 에 더 가까운
  c 가 CO₂ 를 유지하지 못한다면, b 가 그보다 두꺼운 대기를 보유한다는
  것은 그럴듯하지 않습니다.
- **표면 volatile 없음.** ~500 K 의 dayside 온도는 표면의 H₂O, CO₂,
  SO₂ 를 곧장 광분해하고 열적으로 desorb 시켜 버립니다. nightside 는
  ~80 K 로 차갑지만 대기 수송이 없어 volatile 이 거기로 cold-trap 될
  수도 없습니다.

**하늘 외관.** 대기가 없으니 Rayleigh scattering 도 없고 하늘색도
없습니다. 하늘은 모든 고도에서 균일하게 검습니다. TRAPPIST-1 이 각
크기 5.51° 로 하늘을 지배하고(지구에서 본 태양 각 크기의 10 배가 넘음),
하늘에서 단연 가장 큰 단일 천체입니다. 별빛은 짙은 적-오렌지(≈2566 K
blackbody → CIE chromaticity 가 `#ff7a1a` 근처)이고, 나머지 여섯 개의
TRAPPIST-1 행성은 합 시에 밝은 별처럼 보입니다. 그중 다음 외측 행성인
c 는 inferior conjunction 에서 ~0.7° 까지 커집니다.

## 자전 & spin 합성

TRAPPIST-1 b 시스템 파라미터는 강한 동기 자전 구성을 강제합니다.
궤도 이심률은 작고(0.00622, Agol 2021), 황도경사각은 ≳7.6 Gyr 의
시스템 나이에 걸쳐 조석력으로 0 까지 damping 되었으며(Agol 2021 §6.2),
회전-궤도 공명은 가장 그럴듯하게 1:1 입니다. Vinson 2017 과 Makarov
2018 은 내측 TRAPPIST-1 행성들에 대해 3:2 대안도 탐색했지만, b 의
이심률에서는 1:1 이 압도적으로 선호된다고 결론지었습니다 (3:2 는
e ≳ 0.01 에서만 안정).

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 1.5109 일 (130 540 s)
입니다. Kopernicus 에서 body 의 `rotationPeriod` 는 궤도 `period` 와
초 단위로 동일하게 설정합니다.

**계절 없음.** obliquity = 0 이고 이심률 기반 libration 도 사실상
0 이라, substellar 점은 표면 frame 에서 고정됩니다.

**Spin-orbit drift.** Lustig-Yaeger 2024 (2409.12065) 는 공명 사슬의
n-body 세차로 인해 substellar 점에 작은 secular drift 가 생긴다고
계산합니다 — b 거리에서는 Myr 당 약 0.6° 로, KSP 게임플레이 시간
스케일에서는 무시할 수준이지만, cfg 에서는 "substellar 점"이 장기
평균이라는 주석을 달아 두는 것이 정직합니다. Revol 2024 (Bolmont 2026 /
2601.03408 에 인용)는 사슬 전체의 동역학을 고려할 때 b 에 대해 무려 69 년
짜리 "sidereal day" 가 나온다고 봅니다 — 마찬가지로 게임플레이상
무관하지만, 충실한 주석거리는 됩니다.

**조석 Love number 신호.** Bolmont 2020 (2002.02015) 은 TRAPPIST-1 b 의 TTV 가 비정상적으로 큰 행성 Love number (k₂ ≳ 1.5, 지구의 0.299 를 한참 웃돔) 를 시사한다고 봅니다. 이 값이 사실이라면, 이는 액체층 — 표면 합성에서 이미 채택한 substellar 마그마 저장소일 가능성이 높음 — 에 대한 **직접적인 동역학적 증거**가 됩니다. 신호 자체는 현재 TTV fit 의 noise floor 부근에 머물러 추론의 강도는 잠정적이지만, 재포장 해석을 독립적으로 뒷받침한다는 점이 중요합니다.

## 비주얼 스타일

표면과 대기 결정을 종합하면 다음과 같습니다.

- **전역 색 팔레트.** 어두운 ultramafic body(`#1a1612` primary,
  `#7a2a10` 용암-적색 accent)가 강렬한 적-오렌지 별빛 아래에서는
  벌겋게 달궈진 charcoal 같은 행성으로 보입니다. substellar 반구에는
  별빛을 받는 식어가는 용암 patch 가 보이고, antistellar 반구는
  거의 새까맣습니다.
- **Dayside.** 밝은 substellar 영역(~503 K, ~230 °C)과 텍스처가 살아
  있는 저-기복 용암 평원입니다. cfg 의 PQS 에서 substellar 정점 밝기는
  substellar 점 반경 ~15° 안에서 `#a04020` (용암 적-오렌지)에 도달하도록
  맞춥니다.
- **Terminator band.** 조명이 직접적이고 재분배가 적어 폭이 좁습니다.
  지형 대비는 큽니다 — basalt 능선과 충돌 크레이터 림이 스치는 2566 K
  빛 아래로 긴 그림자를 드리웁니다.
- **Nightside.** 차갑고(~80 K) 완전히 어두우며, 열적외 emission 만 있고
  가시광 대역의 feature 는 없습니다. KSP nightside 조명은 ambient
  값을 거의 0 으로 두는 것이 맞습니다. 유일한 가시광원은 이웃 행성에서
  반사된 빛으로, c 는 합 시 mv ≈ −13 까지 도달해 지구의 달과 비슷합니다.
- **대기 haze 없음.** Limb 가 또렷합니다 — scattering, 굴절, glow 모두
  없고, 행성 디스크에서 우주로의 전환은 깔끔한 가장자리로 끝납니다.
- **하늘의 별.** TRAPPIST-1 이 b 의 하늘에서 5.51° 를 차지합니다
  (지구에서 본 태양 각 크기의 약 11 배). 색은 짙은 적-오렌지(≈2566 K →
  `#ff7a1a`)이고, 표면 밝기는 수성에서 본 태양 정도(~4.25 S⊕)입니다.
  1 μm 이상의 파장에서는 별이 두드러진 항성 플레어를 보일 만큼 밝기 때문에
  (d 의 bibliography 에 있는 Howard 2023, TRAPPIST-1 플레어 통계는
  Glazier 2020) KSP 에서 가끔 플레어 조명의 깜빡임을 넣으면 충실하지만
  선택적인 디테일이 됩니다.
- **하늘의 자매 행성.** b 와 내합인 시점에 TRAPPIST-1 c (다음 외측 행성)
  가 각 크기 ~0.7° 로 보입니다 (지구 달의 1.5 배). 기하학적으로 거의
  동일 평면이고, 이 conjunction 은 약 4 일 주기(b-c 회합 주기)로
  돌아옵니다.
- **마그마 바다 glow (선택).** substellar 표면이 정말 solidus 에
  가깝다면, λ ≳ 2 μm 에서 매우 희미한 적-오렌지 thermal emission 이
  KSP 의 깊은 nightside 비행 중 substellar 점에서 잠시 보일 수도
  있습니다 — 우선순위 낮은 시각 이스터에그입니다.

## 참고 문헌

### 읽음 (시각 정보 제공, 위 결정을 견인)

- **2303.14849** Greene 2023 — JWST/MIRI F1500W secondary eclipse.
  다섯 visit, 8.7σ 검출, Fp/F★ = 861 ± 99 ppm. dayside brightness
  temperature 약 503 K. b 를 맨 암석 후보로 처음 확립한 발견 논문.
- **2412.11627** Ducrot 2024 — 12.8 + 15 μm MIRI eclipse 결합 분석.
  살아남는 모델 두 개를 식별. 미풍화 ultramafic airless 표면(선호) 대
  성층권 inversion 을 갖는 두꺼운 CO₂ + 광화학 haze. 표면 조성 결정과
  "fresh / geologically active" 해석을 견인.
- **2509.02128** Ducrot 2025 — b 와 c 의 JWST MIRI 15 μm thermal phase
  curve. dayside T = 490 ± 17 K, nightside emission 없음, phase offset
  없음. ≳1 bar 대기를 결정적으로 배제하면서 airless 해석을 종결지음.
- **2305.10414** Ih 2023 — b 의 대기 두께를 제한하는 자기일관 복사-대류
  모델. Greene 2023 데이터만으로 0.3 bar 이상의 그럴듯한 CO₂ 대기를
  3σ 로 배제.
- **2509.02120** 3D GCM 기반 제약 (저자 익명화 — YAML 참조). eclipse
  와는 호환되지만 phase curve 로 배제되는 대기군을 탐색. airless 결론을
  강화.
- **2412.05188** Chatterjee & Pierrehumbert 2024 — 유체역학적 escape
  물리를 포함한 cosmic shoreline. b 를 "catastrophic escape" 영역에
  확고히 위치시켜, outgassing 으로도 2차 대기를 재건할 수 없음을 보임.
  JWST 데이터와 독립적인 airless 의 이론적 정당화.
- **2601.03408** Bolmont 2026 — 전체 내부 구조와 JWST nightside 캡을
  활용한 조석 가열 정밀화. `tidal_heating_w_m2` 를 0.04–0.2 에서 명목값
  ~0.5–1 W/m² 로 상향 조정하게 만든 근거이며, JWST 하드 캡은 407 W/m²
  (Φ_2σ). b 에 대해 고이심률, 저점성 내부 모델은 관측적으로 배제됨을
  확정.
- **1911.08878** Turbet 2020 — 강한 일사를 받는 암석 행성의 질량-반지름-
  수분 관계. 지구형 핵에서 b 의 보유 가능 수분이 ≤ 2% 임을 캡 처리하여,
  "오늘날 거의 건조" 추론을 뒷받침.
- **2405.02401** Gialluca 2024 — b/c JWST 제약을 입력으로 한 MCMC 초기 수분 역산. 초기 수분량 8.2 +1.5/-1.0 TO. b 의 airless 해석을 강화하면서 c 의 얇은 O₂ 대기와도 자연스럽게 연결.
- **2002.02015** Bolmont 2020 — b 의 TTV 에서 유도되는 조석 Love number. k₂ ≳ 1.5 라는 큰 값은 액체 마그마층의 동역학적 신호가 될 수 있음. 다만 현재 TTV fit 은 noise floor 부근에 있음.
- **1605.00616** Bolmont 2017 — 초저온 왜성 주위 지구형 행성의 수분 손실에 대한 역사적 baseline. 시스템 나이 동안 b 한 행성에서만 최대 13.5 EO 의 수소가 손실되고, 최대 ~422 bar 의 무기 O₂ 가 축적될 수 있음. airless 해석의 토대 인용.

### 읽음 (맥락 / 방법론, 결정을 견인하지 않음)

- **2309.07047** Lim 2023 — b 의 NIRISS transmission. stellar
  contamination 이 강함 (visit 1 의 spot, visit 2 의 faculae).
  cloud-free 수소 풍부 대기는 기각, 2차 대기는 제약 불가. TRAPPIST-1 b
  의 transmission spectroscopy 가 stellar variability 에 의해 근본적으로
  제한된다는 중요한 맥락 제공.
- **2412.16541** 등시간 b/c transit 짝을 활용한 stellar contamination
  보정. 모든 TRAPPIST-1 transmission 작업에 적용되는 방법론 논문으로,
  직접 시각 정보를 주지는 않음.
- **2507.02052** JWST MIRI 15 μm eclipse 의 균일 재분석 (frame-normalized
  PCA). Greene 2023 / Zieba 2023 reduction 의 교차 검증으로 일관된 결과
  도출.
- **1905.00512** Bolmont 2019 — b 와 c 의 조석 파라미터. 내부 Q 값에
  따라 b 의 조석 가열 flux 를 0.04–0.2 W/m² 로 추정. "재포장 메커니즘"
  논의에 활용.
- **2502.00132** Way 2025 — TRAPPIST-1 d 가 주제이지만 서론에서 b 의
  exo-Venus / exo-Dead 후보 지위를 리뷰. d 의 Phase 3 작업에서 이미
  읽음.
- **2601.12556** Wirth, Powell & Wordsworth 2026 — 조석 고정된 암석 행성
  대기의 해석적 모델링. b 가 Λ ≤ 1 (WTG 가정이 깨지는 영역)에 있어,
  열 재분배 기반 상한은 약하다는 점을 짚음. 대기 합성 절에서 방법론적
  단서로 인용. 다만 분자 흡수 기반 상한(Ih 2023)과 phase curve 직접 측정
  (Ducrot 2025)은 WTG 와 독립이라 airless 결정을 바꾸지는 않음.
- **2512.07695** Allen 2025 — JWST TRAPPIST-1 e/b Program 첫 관측.
  b 를 e 의 stellar-contamination proxy 인 airless 행성으로 활용.
  airless 해석을 재확인하지만 b 자체에 대한 새 제약은 없음.
- **1806.10084** Unterborn 2018 — b/c 의 갱신된 조성 모델. 내부 축퇴성
  논의. 작은 핵은 무수 조성과 일치하고, 큰 핵은 휘발성 envelope 을 요구.
  수분 함량 문제에 대해서는 Agol 2021 + Turbet 2020 으로 대체됨.

### 읽음 (instrument-only, 시각 정보 아님)

- **2203.04173** Rustamkulov 2022 — JWST NIRSpec 실험실 시계열 성능.
  방법론만 다룸.

### 읽지 않음 — arXiv preprint 가 없거나 비시각 내용 (~30 편)

b bibliography 에는 arXiv preprint 가 없는 ~30 편의 논문이 있고, arXiv
는 있지만 시각 정보가 아닌(instrument-only, 생체신호 생물권 모델링 등)
논문도 ~5 편 추가됩니다. 그중 시각 정보를 줄 가능성이 가장 높은
항목들을 적습니다.

- **2026NatAs.tmp...88** "The innermost planets in the TRAPPIST-1
  system do not have thick atmospheres" — Lustig-Yaeger 가 주도한 최근
  Nature Astronomy 종합일 가능성. arXiv preprint 가 곧 올라올 예정이지만
  수집 시점(2026-05-21)에는 아직 색인되지 않음. **몇 주 뒤 재수집
  대상으로 flag.**
- **2026NatAs.tmp...65G** "No thick atmosphere around TRAPPIST-1 b
  and c from JWST thermal phase curves" — Ducrot 2025 의 Nature
  Astronomy 출판판일 가능성 (arXiv preprint 2509.02128 로 이미 다룸).
  Skip.
- **2306.10150** Zieba 2023 — c 의 eclipse 논문. c 합성을 위해 자세히
  읽었고, b 문서 전반에서 비교 행성으로 등장하기에 여기에도 언급.

---

## 후속 항목

- 2026 Nature Astronomy 논문들의 arXiv preprint 가 올라오는 대로
  재수집. 출판판이 Ducrot 2025 / Greene 2023 값보다 대기 상한을 더
  조여 놓았을 가능성에 대비.
- 향후 고해상도 JWST 분광(예. MIRI MRS)이 특정 광물학적 feature 를
  분해해 낼 경우, "fresh ultramafic" 표면 결정을 그에 맞춰 재검증.
- 더 최근의 TRAPPIST-1 항성풍 모델 — Cohen 2024 이후 — 이 가용하다면
  `induction_heating_w_m2` 범위를 교차 검증.
- cfg 변형으로 "마그마 바다 잔존" 해석(visible substellar 용암 호수)
  도 고려 가능. 확률은 더 낮지만 시각적으로 독특해서, Phase 3.5 대안
  구현 후보로 적합.
