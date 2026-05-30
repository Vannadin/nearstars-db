<!-- τ Ceti g Phase 3 합성. cfg-ready 결정과 근거 -->
# τ Ceti g — Phase 3 Synthesis

τ Ceti g 는 metal-poor G8V τ Ceti 주위를 20.0 일 주기로 0.133 AU 에서
도는 1.75 M⊕ (M sin i) RV 후보 행성입니다 (Feng 2017,
`2017AJ....154..135F`). 현재 `db/systems/tau_cet.json` 에 들어 있는
세 행성 중 가장 안쪽이며, 호스트 광도 0.488 L☉ 기준 조사량은
**27.59 S⊕** — 더 어둡고 차가운 호스트라는 점을 빼면 거의 수성급
조명입니다. 평형 온도는 albedo 0 에서 638 K, 지구형 albedo 에서
584 K 로, H₂O 임계점보다 한참 위이고 일부 광물상의 규산염 기화에
접근합니다. 행성은 NEA 에서 **disputed** (`pl_controv_flag = 1`) 로
표시됩니다 — RV 단독, transit 없음, 직접 영상 없음.

**NearStars 시나리오 선택. 조용한 호스트 XUV 환경에도 불구하고 원시
대기 대부분을 잃은 뜨거운 맨 암석 super-Earth — 광분해 산화 패치를
가진 노출된 규산염 표면, substellar 점 근처에 가능한 규산염-증기 캡,
조용한 G8V 조명 아래 재-그레이 팔레트.** 호스트의 metal-poor SED 와
basal XUV 는 대기 탈출이 *thermal Jeans 만* 이고 hydrodynamic 손실은
없다는 의미지만, 638 K dayside 와 0.13 AU 간격에서는 7 Gyr 동안 저
분자량 종 (H₂O, CH₄) 에 대해 Jeans 탈출도 효율적입니다. 두꺼운 CO₂
Venus-analog 해석 대안은 cfg variant 로 보존. 이 합성은
**interesting-first** 룰에 따라 시각적으로 구별되는 맨 암석 결과를
픽합니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `tidally_locked` | 가능 (3:2 or 1:1. cfg 는 3:2 수성-analog 픽) | medium | Vinson 2017 / Makarov 2018. 0.78 M☉ 호스트에서 P=20 d, 7 Gyr 조석 damping 은 borderline. e = 0.06 은 g 를 3:2 포획 허용 영역에 두며, cfg 는 interesting-first 로 비동기 대안 대신 3:2 픽 |
| `obliquity_deg` | 0 | medium | 7 Gyr 조석 damping. 단주기 암석 행성의 표준 |
| `eccentricity` | 0.06 | medium | Feng 2017 RV (h/f 의 secular 강제와 일관) |
| `argument_of_periastron_deg` | 395.341 | medium | Feng 2017 RV |
| `sidereal_period_days` | 20.00 | high | Feng 2017 RV — 불확실성 ±0.02 d |
| `semi_major_axis_au` | 0.133 | high | Feng 2017 (호스트 질량 + Kepler 3 법칙에서 ±0.001) |
| `inclination_deg` | 35 | low | Tie-break. τ Ceti 잔해 원반 경사 (Lawler et al. 2014, MacGregor et al. 2016 이 채택. 공면 가정) |
| `mass_mearth` | 1.75 (M sin i. sin i ≈ 0.7 가정 시 실제 질량 ≳ 2.2 M⊕) | medium | Feng 2017 RV (±0.25) |
| `radius_rearth` | 1.18 | low | Feng 2017 이 mass–radius 관계 (Weiss & Marcy 2014 암석) 로 카탈로그한 반지름. 직접 측정 아님 |
| `surface_gravity_g_earth` | 1.26 | medium | derived = 1.75 / 1.18² |
| `density_g_cc` | 5.84 | medium | derived. 지구형 암석 조성이 mass–radius 관계 픽과 일관 |
| `water_mass_fraction` | < 0.01 | low | 높은 조사량 + 저-XUV thermal Jeans 탈출이 7 Gyr 에 걸쳐 → 원시 수분 대부분 손실. 표면 휘발성 인벤토리는 미미 |
| `insolation_s_earth` | 27.59 | high | derived L_bol/a²: 0.488 L☉ (Teixeira 2009, recommended) / 0.133² |
| `equilibrium_temp_k` (A=0) | 638 | high | derived 278 × (L/a²)^0.25 |
| `equilibrium_temp_k` (A=0.3) | 584 | high | 지구형 albedo 로 derived |
| `bond_albedo` | 0.10 | low | Tie-break. 저-albedo 현무암 / 규산염 표면. 맨 암석 무대기, 수성-analog albedo |
| `surface_temp_substellar_k` | 700 | low | 느린 자전자 (3:2 공명, 40 일 태양일) → 열 재분배가 불완전해 substellar 가 평형 온도 초과 |
| `surface_temp_nightside_k` | 200 | low | 3:2 공명은 긴 열 감쇠 시간을 줌. nightside 는 식지만 deep-space 한계까지는 아님 |
| `surface_temp_global_mean_k` | 500 | low | 느린 자전에서의 비대칭 열 분포. 전도가 subsolar–antisolar 대비를 완화 |
| `atmosphere_present` | false | medium | Tie-break. 맨 암석 무대기 채택. 조용한 호스트 XUV 가 무거운 분자를 보존하지만, 638 K Teq 에서는 ~2 M⊕ 체에서 N₂ 와 CO₂ 도 7 Gyr 에 걸쳐 Jeans 탈출. 차가운 내부 super-Earth 에서는 탈가스도 너무 느림 |
| `atmosphere_surface_pressure_pa` | 0 | medium | 채택 시나리오 (맨 암석). 1–100 mbar 미량 CO₂ + Na 외기권 가능하지만 cfg 에는 없음 |
| `atmosphere_composition` | n/a (미량 규산염-증기 + Na 외기권 가능) | low | 대기가 있다면 수성-analog. substellar 에서 regolith 로부터 광분해로 풀려난 Na, K, Si |
| `atmosphere_scale_height_km` | n/a | high | bulk 대기 없음 |
| `atmosphere_tint_rgb_hex` | `#000000` (감지 불가) | high | 대기 없음 → 산란 없음 |
| `cloud_cover_fraction` | 0 | high | 대기 없음 |
| `cloud_tint_rgb_hex` | n/a | high | 구름 없음 |
| `ocean_present` | false | high | 물 임계점 한참 위 + 대기 없음 |
| `ocean_extent_substellar_radius_deg` | 0 | high | 표면 액체 없음 |
| `ocean_tint_rgb_hex` | n/a | high | 해양 없음 |
| `surface_ice_caps` | none | high | 모든 곳에서 물 어는점 한참 위 |
| `surface_tint_rgb_hex_primary` | `#6c655c` (G8V 조명 아래 현무암 재-그레이. metal-poor 호스트가 Sol 보다 살짝 더 깨끗-푸름) | low | Tie-break. 수성-analog 현무암 regolith. metal-poor 호스트는 철-염색된 원시 먼지를 덜 만듦 → Sol-system 현무암보다 적-갈 톤이 덜함. 황토색 대신 재-그레이 |
| `surface_tint_rgb_hex_accent` | `#8a4a30` (regolith 가 가장 가열되는 substellar 근처의 광분해 산화철 패치) | low | Tie-break. 7 Gyr 의 직접 G8V 조사는 substellar 에 국지적 산화철 풍화를 만들 것. 균일-그레이 대안 대신 interesting-first |
| `surface_morphology` | 충돌구가 가득한 기반암. dayside 탈가스에서 terminator/nightside 의 국지적 규산염-증기 서리. 광분해로 어두워진 용암류 잔재 가능 | low | 수성 / 달 analog. 7 Gyr 동안 재포장 없음. 충돌구 포화 지형 시사 |
| `magnetic_field_present` | false | low | 3:2 느린 자전과 아마도 차가운 내부를 가진 1.75 M⊕ 체에 활성 dynamo 가능성 낮음. 작은 화석 외피 자기장 가능 |
| `magnetic_field_strength_microtesla_equator` | 0.5 | low | Tie-break. 수성-analog 외피-잔재만 (수성 표면 자기장 ≈ 0.4 μT) |
| `tidal_heating_w_m2` | 0.01–0.1 | medium | 0.78 M☉ 호스트 주위 a = 0.133 AU 에서 e = 0.06. Bolmont 2020 스타일 스케일링은 적당한 조석 플럭스를 주지만 Io 한참 아래 |
| `induction_heating_w_m2` | < 0.001 | medium | 호스트 자기장 너무 약함. 조용한 G 왜성 자기 토크 무시 가능 |
| `radiogenic_heat_w_m2` | 0.04 | medium | 지구형 맨틀 방사성을 질량으로 스케일 |
| `aurora_present` | false | high | 대기 없음. 오로라 불가능 |
| `star_apparent_angular_diameter_deg` | 3.17 | high | derived. 2 × R★ / a × (180/π). 지구에서 본 태양의 6× |
| `stellar_illumination_color_temp_k` | 5370 | high | 호스트 Teff (Pavlenko 2012) |

## Surface synthesis

τ Ceti g 는 **맨 암석** 영역에 있습니다. 27.59 S⊕ 조사량은
runaway-greenhouse 한계 (Kopparapu 2014 G8V inner edge ~1.0 S⊕) 한참
안쪽에 두지만, Venus 와 달리 g 는 7 Gyr 동안 Jeans 탈출에 맞서
두꺼운 CO₂ 대기를 유지할 2차 탈가스 속도가 부족합니다. 결과를 결정
하는 두 경쟁 효과.

1. 호스트 별이 예외적으로 조용함 — log L_X ≤ 26.5 cgs (Schmitt 1985),
   log R'HK = −4.95 (Pavlenko 2012), basal FUV (Judge 2004). XUV
   구동 hydrodynamic 탈출은 무시 가능. 무거운 분자 (N₂, CO₂, SO₂)
   는 blow-off 제한이 아님.
2. 그러나 Teq = 638 K 에서의 thermal Jeans 탈출은 무시할 수 없음.
   반지름 1.18 R⊕, 질량 1.75 M⊕ 행성의 탈출 속도는 13.7 km/s.
   638 K 에서 N₂ 의 열 속도는 0.67 km/s 로 Jeans 파라미터 21 —
   형식적으로는 유지 — 이지만, 상부 대기 유효 온도 (얇은/무대기
   영역에서 일반적으로 표면의 2–4×) 에서는 Jeans 파라미터가
   ~5–10 으로 떨어져 Gyr 시간 척도에 걸친 marginal-loss 범위.

cfg 는 **interesting-first** 결과를 채택합니다 — 맨 암석 무대기.
Venus-analog 대안보다 시각적으로 더 구별되는 수성-analog 를 만들고
시스템 맥락과 잘 맞습니다 — τ Ceti 의 가장 안쪽 행성은 바깥쪽 행성
들과 달라 보여야 하고, "g 는 대기를 잃고 h 는 두꺼운 CO₂ envelope 을
유지" 는 시각적으로 유익한 시스템 내 대비입니다.

표면은 지질학적 시간 척도로 재포장되지 않은, 충돌구가 가득한 기반암.
조석 가열 (0.133 AU 에서 e = 0.06) 은 적당함 (~0.05 W/m², Io 의
2 W/m² 한참 아래) 이며 활성 화산을 구동하지 않습니다. 방사성 가열은
지구형 0.04 W/m². 결합한 내부 플럭스는 유체 맨틀이나 지속 dynamo 를
유지하기엔 너무 낮지만, 시스템 나이에 걸쳐 원시 열을 천천히 흘려
보내기엔 충분합니다.

**색 선택 — 재-그레이 현무암 regolith.** 수성과 달은 무대기 체의
풍화되지 않은 규산염 regolith 에 대한 경험적 템플릿을 제공합니다 —
둘 다 ejecta 나 철 부족 현무암에서 오는 국지적 밝은 패치와 함께
지배적으로 어두운 그레이 (`#6c655c` 에서 `#8c8478`). τ Ceti g 에서는
metal-poor 원시 먼지가 ([Fe/H] = −0.55 호스트로부터) 태양 주위보다
원래 입자 모집단의 철-염색이 덜했을 것임을 시사하며 — cfg 픽
`#6c655c` 은 Sol-system 수성 기준보다 살짝 더 깨끗한 재-그레이로,
황토 대신 그레이 쪽으로 편향. 광분해 산화철 풍화가 substellar
영역에 7 Gyr 동안 누적되어 ~5% 표면적 수준의 국지적 녹슨 갈색 패치
(`#8a4a30`) 를 줍니다 — 균일 그레이 대안 위에 시각적 차별성을 더하는
tie-break.

**광물학 노트.** 관측 없이 광물학은 형성에서 추론. metal-poor G 왜성
의 iceline 안쪽에서 형성된 2 M⊕ 암석체는 Mg/Si ≈ 1.1–1.2 (Fe 가
고갈되어 살짝 상승) 를 가져 plagioclase 우세 melt 보다 olivine 과
pyroxene 을 선호. olivine 풍부 현무암 regolith 는 지구 현무암보다
살짝 더 푸른-그레이로 보일 것이며, cfg 픽은 hex 수준에서 이를
인코딩하지 않지만 표면 형태 산문이 힌트를 줍니다.

**규산염-증기 캡 없음.** 700 K dayside 온도에서 규산염 증기압은
10⁻⁶ bar 한참 아래 (규산염 응결 온도 ~1500–2000 K). g 는 뜨겁지만
마그마 바다 만큼은 아님. substellar 규산염-증기 구름 렌더링 없음.

## Atmosphere synthesis

cfg 는 **bulk 대기 없음** 을 채택합니다. 논리는 위의 Surface synthesis
에 있음 — 638 K Teq 에서 적당한 상부 대기 가열로 thermal Jeans 탈출이
2 M⊕ 체에서 N₂ 와 CO₂ 를 7 Gyr 에 걸쳐 흘려보내고, 조용한 호스트가
의미 있는 광화학 보충을 만들지 못함. 따라서 대기는 사라질 정도로
얇음 — substellar 핫스팟 regolith 에서 광분해로 풀려난 Na, K, Si, O
의 수성-analog 외기권으로, 표면 스케일에서 동역학적으로 ballistic
하며 정수압 평형이 아님.

**전구 Rayleigh 안개 없음.** cfg `atmosphere_tint_rgb_hex` 는 `#000000`
(감지 불가) 이고 림은 PQS 해상도에서 또렷.

**하늘 모습.** 표면에서 하늘은 검고, 호스트 별이 3.17° 각지름으로
지배 — 지구에서 본 태양 각지름의 약 6×. 표면은 substellar 점에서
27.59 S⊕ 의 옅은 노랑 G8V 조명을 받고, dayside 표면 온도는 700 K
초과. 호스트 빛을 산란하는 대기가 없으므로 dayside 에도 다른 별들이
쉽게 보임. 밤하늘은 달과 비슷하며 deep field 별들이 전 magnitude 로
보임. 호스트의 metal-poor SED 는 태양 스펙트럼보다 살짝 더 깨끗한
옅은 노랑 색을 만들어 marginal 하게 덜 따뜻한 원반으로 감지됨.

**Counterfactual — Venus-analog cfg variant.** "g 가 Venus, h 가
Mercury" 대안 시스템 설명에 흥미가 있는 독자는 둘을 바꿀 수 있음.
그러나 주기와 조사량 순서 (g 가 가장 뜨겁고, h 가 다음, f 가 가장
차가움) 는 Venus 급 runaway-greenhouse 를 h (살짝 더 시원한 7.7 S⊕
이웃) 에 두는 게 최선임을 의미. 탈가스 속도가 지속 두꺼운 CO₂ 대기를
지지함. 수성-analog g 가 물리적으로 더 방어 가능한 픽.

## Rotation & spin synthesis

τ Ceti g 의 spin 상태는 세 행성 중 가장 불확실합니다. 두 경쟁 시나리오.

1. **3:2 spin-orbit 공명 (수성 analog).** e = 0.06 에서 3:2 포획 확률
   은 ~50–70% (Makarov 2018 Figure 7, 이 주기와 이심률의 super-Earth
   질량체). 3:2 포획은 libration 영역들 간 상당한 열 비대칭을
   가진 40 일 태양일을 만듦.
2. **비동기 느린 자전자.** 3:2 포획이 실패했다면 행성은 원시 주기
   (시간에서 일까지 어디든 가능) 로 자전하며 3:2 나 1:1 쪽으로
   꾸준한 damping. 이 궤도 주기에서 7 Gyr 에 걸친 damping 은 거의
   완성에 가까울 것.

cfg 는 **3:2 (수성 analog)** 를 interesting-first 픽으로 채택. 40 일
태양일은 표면 온도의 상당한 일주 사이클 (subsolar 가 태양일에 걸쳐
200 → 700 → 200 K 사이를 swing) 을 만들고, 표면을 가로지르는 시각
적으로 구별되는 열 비대칭을 만듦. 1:1 고정 대안은 Open item 의
cfg variant 로 보존.

**KSP 구현 노트.** 3:2 의 경우. `rotationPeriod` = (2/3) × 궤도 주기
= 13.33 일 (1.152×10⁶ s). 1:1 대안은 20 일 (1.728×10⁶ s).

**Obliquity.** 7 Gyr 조석 damping 은 obliquity 를 0 으로 끌어내릴
것. cfg 는 0° 채택. libration 유도 조사량 변동 (e = 0.06 에서 ~12%)
은 20 일 궤도 주기에 걸쳐 적당한 "계절" 을 주지만 — 밝아짐/식어짐
사이클로는 감지되어도 반구 계절로는 아님.

**자기 dynamo 기대치.** 1.75 M⊕ 체에 3:2 느린 자전 (~40 일 태양일)
과 아마도 차가운 내부는 전구 dynamo 를 유지하기 어려움. 수성의
dynamo 는 부분적으로 녹은 코어에 의해 비정상적으로 유지됨. 같은
것이 metal-poor super-Earth 에 적용되는지는 불분명. cfg 는 비관적
으로 활성 dynamo 없음 + ~0.5 μT 의 수성-analog 외피 잔재 자기장
가능을 가정.

## Visual styling

- **전구 외관.** substellar libration 영역 근처에 국지적 녹슨 갈색
  풍화 패치 (`#8a4a30`) 를 가진 어두운 재-그레이 암석 세계
  (`#6c655c`). 충돌구가 많고, 더 젊은 충돌의 ray 시스템이 보임.
  시각 캐릭터는 살짝 큰 수성에 가장 가까움 — 거의 무대기, 어둡고,
  충돌구가 많음.
- **Substellar 영역 (libration 존).** 가장 가열됨, 가장 오래된
  산화 패치가 여기 집중. 녹슨 갈색 풍화가 기본 재-그레이 위에
  ~5% 표면적 패치로 PQS 해상도에서 보임. 가장 큰 충돌구 림 근처에
  규산염-증기-증착된 밝은 패치 가능 (충격에서 휘발성 재증착).
- **중위도 / 경도.** 차등 풍화에서 오는 albedo 의 미세한 변동을
  가진 재-그레이 현무암. 충돌구 ray 가 밝은 lineation 으로 보임.
- **Terminator.** grazing 5370 K G8V 빛 아래 높은 대비. 지형 그림자
  가 충돌구 깊이를 드러냄. 대기 부재가 산란을 만들지 않으므로
  terminator 밴드는 또렷함.
- **Nightside.** 별빛이 regolith 에 반사되는 희미한 cyan-white
  광택과 함께 어두운 그레이-블랙. KSP nightside 환경광 ≈ dayside 의
  0.5%. 보이는 피처. 충돌구 림이 비스듬한 각도에서 별빛을 잡음.
- **대기 안개.** 없음 — 림은 PQS 해상도에서 또렷. 지구 관측에서
  수성이 보이는 0.1° Rayleigh 산란 후광은 렌더링하지 않음.
- **하늘의 별.** τ Ceti 는 g 하늘에서 3.17° 를 채움 (지구에서 본
  태양의 6×). 원반은 metal-poor SED 아래 옅은 노랑이며, 지구에서
  본 태양보다 한참 크고 밝지만 더 낮은 Teff 때문에 다소 더
  차가운 노랑. dayside 피크의 표면 조명은 불편할 정도로 밝지만
  regolith 를 백열시킬 정도는 아님.
- **하늘의 자매 행성들.** h (바깥쪽 다음) 는 합 위치에서 각지름
  ~0.05°. f (훨씬 더 멀음) 는 ~0.03°. ≥ 6 AU 의 차가운 잔해
  원반은 한참 바깥에 있고 희미한 외곽 띠로 보임.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Feng F. et al. 2017** — *Color difference makes a difference:
  four planet candidates around τ Ceti*, AJ 154, 135
  (`2017AJ....154..135F`, arXiv:1708.02051). 발견 + g 궤도
  (P = 20.00 ± 0.02 d), 질량 (Msini = 1.75 ± 0.25 M⊕), 이심률
  (0.06) 의 최선 제약. 모든 궤도 및 물리 Decisions 행을 정박.
- **Feng F. et al. 2018** — *Detection limits on τ Ceti's planet
  system*, A&A 613, A76 (`2018A&A...613A..76F`,
  arXiv:1801.05415). 20 일 신호 안정성 확인. NEA 의 controversial
  플래그는 amplitude-to-noise 우려 반영.
- **Vinson A. M. & Hansen B. M. S. 2017** — *Spin-orbit dynamics
  of habitable-zone planets*. 3:2 vs. 1:1 spin-orbit 공명 포획
  확률. e = 0.06 의 g 에 대한 3:2 cfg 픽을 지지.
- **Makarov V. V. 2018** — *Tidal locking timescales and 3:2
  capture for rocky planets*. Figure 7 이 g 의 파라미터에서 3:2
  포획 확률 ~50–70% 를 줌.
- **Zahnle K. J. et al. 2017** — *Cosmic shoreline*. 대기 유지
  임계값의 경험적 프레임워크. g 는 조용한 호스트의 shoreline 바로
  안쪽에 위치, 대기 유지로는 marginal.

### Read (context / methodology, not directly decision-driving)

- **Kopparapu R. K. et al. 2014** — *Habitable zones*. G8V 의
  inner-edge runaway-greenhouse 한계는 ~1.0 S⊕. 25.85 S⊕ 의 g 는
  한참 안쪽.
- **Lawler S. M. et al. 2014** — τ Ceti 잔해 원반 경사 ~35°
  (Herschel). MacGregor et al. 2016 (ALMA) 이 채택했고 여기서는
  g 의 궤도면 기본값으로 사용.
- **Bolmont E. et al. 2020** — 조석 진화 프레임워크. g 의 적당한
  e = 0.06 가 0.133 AU 에서 ~0.05 W/m² 플럭스.
- **Owen J. E. & Wu Y. 2017** — *Evaporation valley*. sub-Neptune
  envelope 유지 vs. 질량 + 조사량 프레임워크. g 는 sub-Neptune
  질량 한참 아래이고 맨 암석 유지 임계값 위.

### Read (instrument / non-cfg-decisive)

- **Pavlenko Y. V. et al. 2012** — 호스트 별 맥락.
- **Schmitt J. H. M. M. et al. 1985** — 호스트 X 선 미검출.

### Not read — no arXiv preprint or low-priority (~12 papers)

- **Tuomi 2013 + 2014 erratum** — Feng 2017 로 대체.
- **SETI / technosignature 논문 다수** — cfg 관련성 없음.
- **천체생물학 추측 리뷰** — 일반적으로 g 를 개별 다루지 않음
  (보수적 거주가능 범주에는 너무 뜨거움).

## Canonical alternatives

### Diverged cfg picks

| Field | Gameplay (in cfg) | Canonical alternative | Why diverged |
|---|---|---|---|
| `atmosphere_present` | false (맨 암석 수성 analog) | true, 두꺼운 CO₂ Venus analog (~10 bar, T_surf ~700 K) | 둘 다 미제약 윈도우 안에서 방어 가능. 수성-analog 는 시각적으로 구별되는 충돌구 기반암 표면을 줌. Venus-analog 는 τ Cet h 와 시각적으로 비슷한 구름 가린 노랑 행성을 줌. interesting-first 가 g 를 h 와 시각적으로 구분하기 위해 수성-analog 픽. Venus-analog 는 cfg variant 로 보존. |
| `tidally_locked` | 가능 (3:2 공명, 40 일 태양일) | 1:1 완전 고정 | Vinson 2017 / Makarov 2018 이 e = 0.06 에서 3:2 포획 확률 ~50–70% 를 줌. cfg 는 시각 비대칭 (수성 analog substellar libration 존 vs. 완전 고정의 균일 열장) 을 위해 3:2 픽. 1:1 대안은 cfg variant 로 보존. |

## Open items for follow-up

- **Controversial 플래그 (`pl_controv_flag = 1`).** f 와 마찬가지로
  Lubin 2024 또는 미래 ESPRESSO RV 재분석에 의한 철회 모니터링.
- **실제 질량.** Msini = 1.75 ± 0.25 M⊕. 실제 질량은 미지의 i 에
  의존. cfg 는 원반에서 i ≈ 35° 채택 → 실제 질량 ≈ 3.0 M⊕.
- **반지름은 가정 값, 측정 아님.** mass-radius 관계에서 R = 1.18 R⊕.
  아래쪽으로 미제약. 실제 질량이 더 크고 행성이 더 밀도 높은 암석
  이라면 R 은 1.05 R⊕ 까지 가능하며 ρ ≈ 7 g/cc.
- **Venus-analog cfg variant.** H₂SO₄ 구름을 가진 10-bar CO₂ 대기가
  맨 암석 픽에 대한 보수적 대안. 시각적으로는 τ Cet h 와 비슷해
  보일 것 — 노랑-크림 가려진 구름 데크 — 그래서 cfg 는 시각
  차별성을 위해 수성-analog 픽. variant 는 보존.
- **1:1 spin-lock cfg variant.** metal-poor 호스트의 super-Earth 에
  대한 미래 조석 소산 모델링 캠페인이 τ_tidal 을 정제하면 spin
  상태가 수정될 수 있음. 현재는 3:2 vs. 1:1 질문이 본질적으로
  열려 있음.
- **광물학 정제.** metal-poor (Mg/Si 상승) 암석체는 olivine 풍부
  여야 함. 미래 cfg shader 가 광물학-특이 표면 틴팅을 지원하면
  `surface_tint` 가 현재 재-그레이 기본값 대신 올리브-그레이로
  이동할 수 있음.
- **미량 외기권.** 광분해 regolith 해방에서 오는 수성-analog
  Na/K/Si 외기권이 plausible 하지만 KSP 렌더링 스케일에서 보이지
  않음. 미래 cfg 정제를 위해 로깅.

## Related

- [tau-cet](tau-cet.md) — 호스트 별 Phase 3 (G8V metal-poor.
  조용함, 늙음, 잔해 원반 보유)
- [tau-cet-h](tau-cet-h.md) — 중간 자매. 두꺼운 CO₂ 대기의
  Venus-analog
- [tau-cet-f](tau-cet-f.md) — 가장 바깥쪽 자매. snowball
- [methodology](../reference/methodology.md) — Decisions 스키마
- [rex-data-comparison](../reference/rex-data-comparison.md) — §6
  τ Ceti e 큐레이션 갭
