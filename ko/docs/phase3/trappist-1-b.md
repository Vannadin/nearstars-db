<!-- TRAPPIST-1 b Phase 3 synthesis: cfg-ready 결정과 근거 -->
# TRAPPIST-1 b — Phase 3 Synthesis

TRAPPIST-1 b 는 M8V ultra-cool dwarf 를 1.51 일 주기로 도는 1.12 R⊕,
1.37 M⊕ 의 암석 행성. TRAPPIST-1 의 7개 세계 중 가장 안쪽에 위치하며
지구 일사량의 4.3 배를 받음. JWST MIRI 의 12.8 μm 과 15 μm 에서의
secondary-eclipse 측정 (Greene 2023, Ducrot 2024) 과 전체 thermal phase
curve (Ducrot 2025) 가 시스템에서 가장 깨끗한 "맨 암석" 답을 제공.
dayside brightness temperature ≈ 490–503 K, 검출 가능한 nightside
emission 없음, thermal phase offset 없음. ~0.3 bar 보다 두꺼운 (현실적
CO₂ 함량을 가진) 그럴듯한 대기는 3σ 에서 배제.

**NearStars 시나리오 선택. substellar 점 근처의 국지적 신선한 마그마
feature 를 가진 대기 없는 ultramafic 암석 표면.** 이는 선호되는 Ducrot
2024 해석(미풍화 ultramafic 표면은 최근 / 진행 중인 지질학적 재포장을
함의) 과 일치하며 Grayver 2022 / Bolmont 2020 의 induction-heating
"exo-Io" 힌트를 통합. 대안인 — 광화학 안개와 성층권 inversion 을 가진
순수 CO₂ 대기 — 도 데이터로 공식적으로 허용되지만 우주화학적 근거로
불선호 (b 가 하나 유지했다면 두 자리 바깥의 TRAPPIST-1 c 에 CO₂ 가 살아
남을 수 없음).

## 결정

Kopernicus / atmosphere cfg-ready 값. `Confidence`. high = 직접 측정
또는 강하게 제약, medium = 강한 지지를 가진 이론, low = 허용 윈도우 내
미적 선택.

| 항목 | 값 | 신뢰도 | 근거 |
|---|---|---|---|
| `tidally_locked` | true | high | 1.51 d 궤도, 조석 damping; Agol 2021 |
| `obliquity_deg` | 0 | high | 조석 damping; Agol 2021 |
| `eccentricity` | 0.00622 | high | Agol 2021 TTV |
| `argument_of_periastron_deg` | 337 | medium | Agol 2021 (low ecc → 약한 제약) |
| `sidereal_period_days` | 1.5109 | high | Agol 2021 |
| `semi_major_axis_au` | 0.01154 | high | Agol 2021 |
| `mass_mearth` | 1.374 | high | Agol 2021 TTV |
| `radius_rearth` | 1.116 | high | Agol 2021; Greene 2023 transit fit |
| `surface_gravity_g_earth` | 1.103 | high | derived = 1.374 / 1.116² |
| `density_g_cc` | 5.43 | high | Agol 2021 |
| `insolation_s_earth` | 4.25 | high | Agol 2021 |
| `equilibrium_temp_k` (A=0)   | 397 | high | Agol 2021 |
| `dayside_brightness_temp_k_15um` | 503 | high | Greene 2023 F1500W eclipse |
| `dayside_brightness_temp_k_phase_curve` | 490 | high | Ducrot 2025 MIRI 15 μm phase curve |
| `bond_albedo` | 0.0 | high | Greene 2023; Ducrot 2025 — dayside-only re-radiation |
| `atmosphere_present` | false | high | Ducrot 2025 phase curve 가 ≳1 bar greenhouse 배제 |
| `atmosphere_surface_pressure_pa` | 0 | high | Ih 2023 이 > 0.3 bar 의 그럴듯한 대기 배제 |
| `atmosphere_composition` | n/a (airless) | high | Greene 2023; Zieba 2023 (자매 행성 제약) |
| `atmosphere_scale_height_km` | n/a | high | airless |
| `atmosphere_tint_rgb_hex` | n/a | high | airless |
| `dayside_surface_temp_k` | 503 | high | 측정된 brightness temp 과 일치; Ducrot 2025 |
| `substellar_peak_temp_k` | 620 | medium | derived 맨 암석 subsolar (A=0, ε=1, advection 없음) |
| `nightside_surface_temp_k` | 80 | medium | airless + redistribution 없음; passive radiative 한계 |
| `surface_tint_rgb_hex_primary` | `#1a1612` (어두운 ultramafic basalt) | medium | Ducrot 2024 "신선한 ultramafic" + 달 mare analog |
| `surface_tint_rgb_hex_accent` | `#7a2a10` (substellar 근처 식어가는 용암 + 산화철) | low | induction heating + 신선한 용융 patch; Grayver 2022 |
| `surface_morphology` | substellar 점 근처에 신선한 용암 흐름과 어두운 마그마 pond 가 있는 basaltic 평원 | medium | Ducrot 2024 미풍화 표면 추론; Grayver 2022 induction heating |
| `induction_heating_w_m2` | 0.4–4 | medium | Grayver 2022 — 항성풍에 의한 자기 induction heating, 행성 특화 |
| `surface_ice_caps` | 없음 (nightside 에서 승화/광분해) | high | dayside 500 K, volatile 을 가둘 대기 없음 |
| `star_apparent_angular_diameter_deg` | 5.51 | high | derived: 2 × R★ / a × (180/π) |
| `stellar_illumination_color_temp_k` | 2566 | high | Agol 2021 SED fit |
| `tidal_heating_w_m2` | 0.04–0.2 | medium | Bolmont 2020 — 내부 구조 의존적 |

## 표면 합성

Ducrot 2024 는 결합된 12.8 / 15 μm eclipse fit 을 통과하는 두 대기-또는-
표면 모델을 찾음. 광화학 안개를 가진 두꺼운 순수 CO₂ 대기 (성층권
inversion 과 emission 에서의 CO₂ feature 를 생성) 와 — 선호되는 — **미풍화
ultramafic 표면**을 가진 대기 없는 행성. ultramafic 해석이 중요. 달의
풍화된 basalt (regolith 노화) 는 낮은 broadband albedo 를 가지지만 특정
15 μm emissivity 는 데이터와 일치하지 않는 반면, 신선한 (지질학적으로
젊은) ultramafic 표면은 일치. 이는 진행 중이거나 최근의 지질학적
재포장을 함의.

Ducrot 2025 phase curve 가 이를 공고화. 검출된 nightside emission 없음
(15 μm 에서 ≲39 ppm), phase offset 없음, dayside flux 는 낮은 Bond
albedo 와 비효율적인 열 재분배를 가진 맨 암석 모델과 일치. b 의 문헌
전반의 결론은 일관. **b 는 맨, 신선한, 어두운, 뜨거운 암석.**

**재포장 메커니즘.** 두 가지 물리적으로 그럴듯한 동인. (1) resonant
chain 의 조석 가열 (Bolmont 2020 은 내부 dissipation 파라미터 Q 에 따라
b 에 대해 0.04–0.2 W/m² 추정). 비교를 위해 달-지구 조석 flux 는 ~1
mW/m²; Bolmont 범위의 하단조차 이를 초과하며, Io 의 ~2 W/m² 에는
도달하지 않지만 상단은 화성의 방사성 flux ~0.04 W/m² 에 접근. (2) 별의
바람을 통한 행성 운동에서 비롯되는 자기 induction heating (Grayver
2022, Cohen 2024), b 에 대해 0.4–4 W/m² 의 추정 — 부분 용융 화산활동을
유지하기에 충분. 시스템의 7.6 Gyr 나이를 고려하면 누적 효과는 지각
약점 영역에서 용암 흐름에 의해 지속적으로 새로워지는 표면이며, 일사량이
상부 지각을 solidus 에 가장 가깝게 미는 substellar 반구 쪽으로 편향.

**색 선택.** 호스트 별은 SED peak 이 1.1 μm 근처인 2566 K M8V dwarf —
인간 관찰자가 인지하는 표면 reflectance 는 본래 광물 색과 무관하게
강하게 적색-이동 (일반 M-dwarf 표면 조명 처리는 Domagal-Goldman 2010).
신선한 ultramafic 표면 (komatiite / olivine-pyroxene analog, broadband
visible albedo ≈ 0.03–0.08) 의 경우 가장 가까운 태양계 reference 는
수성의 어두운 dorsa 또는 젊은 달 크레이터의 미풍화 floor. 우리는
`#1a1612` (매우 어두운 ultramafic) 을 primary, `#7a2a10` (식어가는-용암
빨강) 을 substellar 사분면 쪽으로 편향된 accent 로 선택.

**산화철.** d 보다 덜 두드러짐. Ducrot 2024 의 "신선한" ultramafic 추론은
유의미한 풍화에 적극 반대하므로, d 대비 산화철 patch 를 최소화. 존재하는
산화물은 표면 물질이 stellar UV 에 노출되지만 최근에 재포장되지 않은
terminator 와 antistellar 반구로 편향되어야 함.

**모양.** 세 가지 기여 과정. (1) 조석 + induction heating 에 의해 구동되는
부분 용융 화산활동에 의한 지속적 재포장 (Bolmont 2020, Grayver 2022) 으로,
주로 substellar 반구에서 신선한 용암 흐름과 shield-volcano feature 를
생성. (2) 잠긴 frame 에서 leading 반구 쪽으로 편향된 ~8 Gyr 의 누적 충돌,
다만 진행 중인 화산활동에 의해 부분적으로 지워짐. (3) 초기 ~500 Myr 강착
이후 단계의 마그마 바다 relict feature (b 는 더 강렬한 초기 에너지 flux 를
경험했고 마그마 바다를 더 오래 유지했을 것이므로 Piaulet 2025 §8 의 d 에
대한 논거를 b 까지 확장 가능). 기본 텍스처. substellar 점에서 방사하는
visible 용암 흐름 채널과 trailing 반구 highland 쪽에 충돌 크레이터가
집중된, 어둡고 유리질의 basaltic 평원.

## 대기 합성

JWST MIRI 15 μm 광도측정 eclipse (Greene 2023, 다섯 visit, 8.7σ 검출)
이 Fp/F★ = 861 ± 99 ppm 산출, dayside brightness temperature ≈ 503
+26/-27 K 에 해당. Ih 2023 은 이로 대기 질량을 제한. ≥100 ppm CO₂ 를
함유한 그럴듯한 대기는 3σ 에서 0.3 bar 위에서 배제되고, 화성형 6.5 mbar
순수 CO₂ 대기도 3σ 에서 배제.

Ducrot 2024 는 12.8 μm eclipse (CO₂ 의 15 μm feature 의 in-band) 를
추가하고 12.8 μm 에서 Fp/F★ = 452 ± 86 ppm, 15 μm 에서 775 ± 90 ppm 을
발견 (결합 재분석). 2σ 에서 두 모델이 살아남음. 대기 없는 ultramafic
표면 (선호) 과 성층권 inversion 을 생성하는 광화학 안개를 가진 두꺼운
순수 CO₂ 대기 (caveat: 특정 안개 화학 필요).

Ducrot 2025 가 사건을 종결. MIRI 15 μm phase curve 는 dayside
brightness temperature 490 ± 17 K, 검출된 nightside flux 없음
(F_night,max = 39 +55/−27 ppm), 측정 가능한 phase offset 없음을 보여줌.
표면 압력 ≥1 bar 와 유의미한 greenhouse 효과를 가진 대기 모델은 배제;
b 는 "어떤 실질적인 대기도 보유하지 않을 가능성이 높음."

NearStars 는 **완전히 대기 없는** 해석을 채택.

- **압력.** 정확히 0 Pa. 12.8/15 μm 일관 "CO₂ + 안개" 시나리오는 이웃
  행성 c 에 CO₂ 의 부재와 충돌하기 때문에 폐기 (Zieba 2023). 더 낮은
  일사량의, cosmic shoreline 에 더 가까운 c 가 CO₂ 를 유지하지 않는다면,
  b 가 더 두꺼운 것을 보유하는 것은 그럴듯하지 않음.
- **표면 volatile 없음.** ~500 K 의 dayside 온도는 표면 H₂O, CO₂,
  또는 SO₂ 를 즉시 광분해하고 열적으로 desorb. nightside 는 차갑지만
  (~80 K) 대기 수송이 없어 volatile 이 거기에 cold-trap 될 수 없음.

**하늘 외관.** 대기 없음은 Rayleigh scattering 도 sky-color 도 없음을
의미. 하늘은 모든 고도에서 균일하게 검음. TRAPPIST-1 이 각 크기 5.51°
로 하늘을 지배 (지구에서 본 태양 각 크기의 10배 이상) — 하늘에서 단연
가장 큰 단일 천체. 색은 깊은 적-오렌지 (≈2566 K blackbody → CIE
chromaticity 가 `#ff7a1a` 근처). 다른 6개 TRAPPIST-1 행성은 합에서 밝은
별로 나타나며, c (다음 외행성) 는 내합에서 ~0.7° 에 도달.

## 자전 & spin 합성

TRAPPIST-1 b 시스템 파라미터가 강한 동기 회전 구성을 강제. 궤도 이심률은
작음 (0.00622; Agol 2021), 황도 경사각은 ≳7.6 Gyr 시스템 나이 동안 조석력에
의해 0 으로 damping (Agol 2021 §6.2), 회전-궤도 공명은 가장 그럴듯하게
1:1. Vinson 2017 과 Makarov 2018 은 안쪽 TRAPPIST-1 행성에 대해 3:2
대안을 탐색했고 b 의 이심률에서 1:1 이 압도적으로 선호된다고 결론
(3:2 는 e ≳ 0.01 에 대해서만 안정).

**KSP 구현 노트.** 자전 주기 = 궤도 주기 = 1.5109 일 (130 540 s).
Kopernicus 에서 body 의 `rotationPeriod` 가 궤도 `period` 와 초 단위로
같아야 함.

**계절 없음.** 황도 경사각 = 0 과 본질적으로 0 인 eccentricity-driven
libration 으로, substellar 점이 표면 frame 에서 고정.

**회전-궤도 drift.** Lustig-Yaeger 2024 (2409.12065) 는 체인의 n-체
세차로 인한 substellar 점의 작은 secular drift 를 계산 — b 의 거리에서
drift 는 Myr 당 ~0.6°, KSP 게임플레이 시간 척도에서 무시할 만하지만
"substellar 점" 이 장기 평균임을 cfg 에 기록할 가치 있음.

## 비주얼 스타일

표면과 대기 결정 결합.

- **전역 색 팔레트.** 어두운 ultramafic body (`#1a1612` primary,
  `#7a2a10` 용암-빨강 accent) 가 강렬한 적-오렌지 별빛 아래 → 빛나는
  charcoal 세계로 나타남. substellar 반구는 별빛을 받는 visible
  식어가는-용암 patch 가 있음; antistellar 반구는 거의 검음.
- **Dayside.** 밝은 substellar 영역 (~503 K, ~230 °C) 과 텍스처가 있는
  저-기복 용암 평원. cfg 의 PQS 에서 substellar peak 밝기는 substellar
  점에서 ~15° 이내에 `#a04020` (용암 적-오렌지) 에 도달해야 함.
- **Terminator band.** 직접적, 낮은-재분배 조명으로 인해 좁음. 높은
  지형 대비 — basaltic 능선과 충돌 크레이터 림이 스치는 2566 K 빛 아래
  긴 그림자를 던짐.
- **Nightside.** 차가움(~80 K) 하고 완전히 어두움; 열적외 emission 만,
  visible 대역 feature 없음. KSP nightside 조명은 거의 0 의 ambient 여야.
  유일한 visible 광원은 이웃 행성에서 반사된 빛 (c 는 합에서 mv ≈ −13 에
  도달, 지구의 달과 비슷).
- **Atmosphere haze 없음.** Limb 가 sharp — scattering, 굴절, glow 없음.
  disk 에서 space 로의 전환은 깨끗한 가장자리.
- **하늘의 별.** TRAPPIST-1 이 b 의 하늘에서 5.51° 차지 (지구에서 본
  태양 각 크기의 약 11×). 색은 깊은 적-오렌지 (≈2566 K → `#ff7a1a`),
  표면 밝기는 Mercury-from-Mercury 태양 밝기와 비슷 (~4.25 S⊕). 1 μm
  이상 파장에서 별이 두드러진 solar flare 를 보일 만큼 밝음 (d
  bibliography 의 Howard 2023; TRAPPIST-1 flare 통계는 Glazier 2020
  직접) — KSP 에서 가끔 flare 조명 깜빡임이 충실하지만 선택적인 터치가
  될 것.
- **하늘의 자매 행성.** b 와 내합 시, TRAPPIST-1 c (다음 외행성) 가 각
  크기 ~0.7° 에 나타남 (지구 달의 1.5×). 거의 동일 평면 geometry; 이
  conjunction 은 ~4 일마다 발생 (b-c 회합 주기).
- **마그마 바다 glow (선택).** substellar 표면이 정말 solidus 에
  가깝다면, λ ≳ 2 μm 에서 매우 희미한 적-오렌지 thermal emission 이
  KSP 의 깊은 nightside flyover 동안 substellar 점에서 보일 수 있음 —
  낮은 우선순위의 시각적 이스터에그.

## 참고 문헌

### 읽음 (시각-정보 제공, 위 결정 견인)

- **2303.14849** Greene 2023 — JWST/MIRI F1500W secondary eclipse.
  다섯 visit, 8.7σ 검출, Fp/F★ = 861 ± 99 ppm. Dayside brightness
  temperature ≈ 503 K. b 를 맨 암석 후보로 확립한 발견 논문.
- **2412.11627** Ducrot 2024 — 결합된 12.8 + 15 μm MIRI eclipse 분석.
  살아남는 두 모델 식별. 미풍화 ultramafic 대기 없는 표면 (선호) 대
  성층권 inversion 을 가진 두꺼운 CO₂ + 광화학 안개. 표면 조성 결정과
  "신선한 / 지질학적으로 활성" 해석을 견인.
- **2509.02128** Ducrot 2025 — b 와 c 의 JWST MIRI 15 μm thermal phase
  curve. Dayside T = 490 ± 17 K, nightside emission 없음, phase
  offset 없음. ≳1 bar 대기를 결정적으로 배제. 대기 없음 해석을 종결.
- **2305.10414** Ih 2023 — b 의 대기 두께를 제한하는 자기-일관 복사-대류
  모델. Greene 2023 데이터만으로 3σ 에서 > 0.3 bar 의 그럴듯한 CO₂
  대기를 배제.
- **2509.02120** 3D GCM 의 제약 (익명화 — 저자는 YAML 참조). eclipse 와
  호환되지만 phase curve 로 배제되는 대기군을 탐색. 대기 없음 결론을
  강화.

### 읽음 (맥락 / 방법론, 결정 견인 안 함)

- **2309.07047** Lim 2023 — b 의 NIRISS transmission. 강한 stellar
  contamination (visit 1 의 spot, visit 2 의 faculae). Cloud-free
  수소-rich 대기 거부; 2차 대기는 제약 불가. TRAPPIST-1 b 의 transmission
  spectroscopy 가 stellar variability 에 의해 근본적으로 제한된다는
  중요한 맥락.
- **2412.16541** back-to-back b/c transit 을 사용한 stellar
  contamination 보정. 모든 TRAPPIST-1 transmission 작업에 관련된
  방법론 논문; 직접 시각-정보 아님.
- **2507.02052** JWST MIRI 15 μm eclipse 의 균일 재분석
  (frame-normalized PCA). Greene 2023 / Zieba 2023 reduction 에 대한
  교차 검증; 일관된 결과.
- **1905.00512** Bolmont 2019 — b 와 c 의 조석 파라미터. 내부 Q 에
  따라 b 에 대해 0.04–0.2 W/m² 의 조석 가열 flux 추정. "재포장
  메커니즘" 논의에 사용.
- **2502.00132** Way 2025 — TRAPPIST-1 d 초점이지만 서론에서 b 의
  exo-Venus / exo-Dead 후보로서의 상태를 리뷰. d Phase 3 에 이미
  읽음.

### 읽음 (instrument-only, 시각 정보 아님)

- **2203.04173** Rustamkulov 2022 — JWST NIRSpec lab time-series
  성능. 방법론만.

### 읽지 않음 — arXiv preprint 없거나 비시각 콘텐츠 (~30 편)

b bibliography 는 arXiv preprint 가 없는 ~30 편의 논문에 추가로 arXiv
가 있지만 시각-정보가 아닌 ~5 편 (instrument-only, biosignature
biosphere 모델링 등) 을 포함. read-안 함 세트에서 시각-정보 가능성이
가장 높은 항목.

- **2026NatAs.tmp...88** "The innermost planets in the TRAPPIST-1
  system do not have thick atmospheres" — Lustig-Yaeger 가 이끄는 최근
  Nature Astronomy 요약일 가능성. arXiv preprint 가 곧 나올 예정이지만
  검색 시점 (2026-05-21) 에 아직 색인되지 않음. **몇 주 후 재검색을
  위해 flag.**
- **2026NatAs.tmp...65G** "No thick atmosphere around TRAPPIST-1 b
  and c from JWST thermal phase curves" — Ducrot 2025 의 Nature
  Astronomy 출판일 가능성 (arXiv preprint 2509.02128 로 이미 다룸).
  Skip.
- **2306.10150** Zieba 2023 — c 의 eclipse 논문. c 합성을 위해 자세히
  읽음; b 가 전반에서 비교 행성이기 때문에 여기에 언급.

---

## 후속 follow-up 항목

- arXiv preprint 가 나오면 2026 Nature Astronomy 논문 재검색, 출판된
  버전이 Ducrot 2025 / Greene 2023 값 아래로 대기 상한을 조이는 경우에
  대비.
- 특정 광물학적 feature 를 분해할 수 있는 향후 고해상도 JWST 분광
  (예. MIRI MRS) 에 대해 "신선한 ultramafic" 표면 결정 검증.
- 가능하다면 더 최근의 TRAPPIST-1 항성풍 모델에 대해
  `induction_heating_w_m2` 범위 교차 검증 — Cohen 2024 이후.
- Cfg 변형. visible substellar 용암 호수를 가진 "마그마 바다 잔존"
  해석. 더 낮은 확률이지만 시각적으로 독특함; Phase 3.5 대안으로
  구현 가능.
