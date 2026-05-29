<!-- Vega Phase 3 합성. cfg-ready 결정과 근거 -->
# Vega — Phase 3 합성

Vega (α Lyrae, HD 172167, HIP 91262) 는 밤하늘에서 다섯 번째로 밝은 별이자 A0Va 왜성의 원형입니다. 거리는 7.679 pc (시차 130.23 mas, SIMBAD). 역사적으로 Johnson 측광 시스템의 영점이었으며, 1983 년 IRAS 가 적외선 초과를 검출한 이후로 잔해 원반의 원형이 되었습니다. "Vega-like" 라는 표현 자체가 여기서 만들어졌습니다 (Aumann 외 1984, `1984ApJ...278L..23A`). NearStars DB 가 기록하고 있는 항성 매개변수 — M = 2.135 ± 0.075 M☉ (Yoon 외 2010, `2010ApJ...708...71Y`), 적도 반지름 R = 2.726 ± 0.006 R☉ (Monnier 외 2012, `2012ApJ...761L...3M`) — 는 모두 Vega 가 천천히 자전하는 측광 표준이 아니라 거의 극을 향해 회전하는 빠른 자전체라는 현대적 이해의 산물입니다. 유효 온도는 9692 K 입니다 (SIMBAD harmonized; Aufdenberg 외 2006 의 CHARA 간섭계가 극 10150 K vs 적도 7900 K 의 기울기를 직접 측정, `2006ApJ...645..664A`).

Vega 에는 확정된 행성이 없습니다. 가장 깊은 RV 탐색 (Hunsch & Schmitt 2019 및 후속 연구; Hurt 외 2021, `2021AJ....161..157H`) 도 ~7 AU 안쪽에서 0.3 M_Jup 보다 큰 동반체를 배제하고, 내부 소행성대 영역 전반에 ~토성 질량 상한을 둡니다. Hurt 2021 이 보고한 ~0.6 일 0.04 AU 신호 후보가 있으나 현 시점에서 확정 상태가 아닙니다. Vega 의 시각적 정체성을 결정짓는 것은 두 띠 (two-belt) 잔해 원반입니다 — 소행성대 유사 구조에 해당하는 ~14 AU 의 따뜻한 내부 영역, 그리고 ~70 AU 부터 ~200 AU 까지 분해된 차가운 외부 고리. 둘 사이의 비워진 간극은 14–70 AU 사이에 미발견 행성이 행성소체 띠를 휘젓고 있다는 가장 강한 간접 증거입니다 (Su 외 2013, `2013ApJ...763..118S`; Sibthorpe 외 2010, `2010A&A...518L.130S`; Hughes 외 2012, `2012ApJ...750...82H`).

**NearStars 의 시나리오 선택. 거의 극을 향한 A0Va 빠른 자전체 (i ≈ 6°). 중력 감광으로 극 ~10150 K 에서 적도 ~7900 K 로 떨어지는 기울기를 가지고, 정면에서 보이는 두 띠 잔해 원반의 중심에 자리잡고 있는 별입니다.** Pole-on 기하가 시각적으로 가장 정의적인 특징입니다. 대부분의 A형 별 일러스트는 균일한 백청색 원반을 보여주지만, cfg 는 Vega 의 뜨겁고 밝은 극이 플레이어를 직접 바라보고 차가운 적도는 어두운 limb 띠를 형성하도록 묘사합니다. 원반은 IRAS 발견 시대의 정면 dust ring 으로 렌더링됩니다. Confidence=high 줄들은 모두 관측을 추종하고, 원반 기하 행 (row) 들은 분해 영상은 있으나 모델 매개변수화가 갈리는 (Su 2013 vs Sibthorpe 2010 의 inner radius 가 ~3 AU 차이) 부분이라 Confidence=medium 으로, tint hex 와 opacity 같은 합성-전용 필드는 Basis 컬럼에 명시된 tie-break 로 Confidence=low 입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | A0Va | high | SIMBAD harmonized MK; Gray & Garrison 1987 측광 표준 |
| `mass_msun` | 2.135 ± 0.075 | high | Yoon 외 2010 (`2010ApJ...708...71Y`) — CHARA 간섭계 R 과 SED 에 회전 진화 모델을 fit |
| `radius_rsun` (적도) | 2.726 ± 0.006 | high | Monnier 외 2012 (`2012ApJ...761L...3M`) — CHARA/MIRC 영상; 편구 형 빠른 자전체의 적도 반지름 (R_pole ≈ 2.36 R☉, R_eq/R_pole ≈ 1.15) |
| `teff_k` (유효) | 9692 | high | SIMBAD harmonized 값. Aufdenberg 2006 의 면적 평균 Teff 와 일치 |
| `luminosity_lsun` | 47 ± 5 | high | Aufdenberg 2006 / Monnier 2012 — 중력 감광 모델의 총 적분 광도; 볼로메트릭 출력 |
| `metallicity_fe_h_dex` | −0.5 | medium | Yoon 2010 best-fit 모델이 λ Boo 류 표면 metal weak 조성을 채택. Vega 는 알려진 λ Boo 등급 A형으로 광구가 금속 결핍 (Adelman & Gulliver 1990). DB 에 metallicity_measurements 없음, 문헌 합의값 |
| `age_gyr` | 0.455 ± 0.013 | high | Yoon 외 2010 — 회전 모델 isochrone. Monnier 2012 는 중력 감광 fit 으로 0.7 ± 0.075 Gyr 보고; cfg 는 Yoon 표제값을 채택, Monnier 값은 Open items 에 보존 |
| `rotation_v_eq_km_s` | 274 ± 14 | high | Aufdenberg 2006 (`2006ApJ...645..664A`) — CHARA 중력 감광 fit; ω/ω_crit ≈ 0.91. 중력 감광 자전체에서 주기는 정의가 모호하므로 v_eq 가 cfg 안정 핸들 |
| `rotation_period_hours` (적도) | 12.5 | medium | 기하 유도값. 2π R_eq / v_eq = 2π · 2.726 R☉ / 274 km/s ≈ 12.5 h. Petit 외 2010 의 ZDI 주기 0.732 d ≈ 17.6 h 는 자기 구조 (고위도 anchored) 반영이며, cfg 는 적도 기하 사용 |
| `limb_darkening_alpha_h` | n/a (중력 감광 모델로 대체) | high | Aufdenberg 2006 / Monnier 2012 — Vega 는 단일 α limb-darkening law 로 잘 맞지 않음. 2D von Zeipel 중력 감광 β = 0.231 이 cfg 에 유의미한 매개변수 |
| `visual_gravity_darkening_pole_equator_temp_diff_k` | 2250 (T_pole 10150 K, T_eq 7900 K) | high | Aufdenberg 2006 — CHARA H 밴드 간섭계가 기울기를 직접 분해 |
| `visual_surface_tint_hex_primary` | `#cfe0ff` (pole-on 핫화이트블루, 적도 limb 는 약간 차가운 톤) | low | Tie-break. 면적 평균 9692 K 의 흑체는 거의 순수한 white-blue (~`#d8e6ff`). cfg 는 pole-on 시야를 지배하는 뜨거운 극면을 강조해 약간 더 푸르게 조정하고, limb 는 `#e8e2d6` (~7900 K) 적도 띠로 어두워짐. `conflict-resolution.md` 의 interesting-first 원칙 적용 |
| `stellar_color_temp_k` | 9692 | high | 인게임 조명용으로 면적 평균 Teff 에서 유도 |
| `visual_pole_on_inclination_deg` | 6.2 ± 0.3 | high | Aufdenberg 2006 / Monnier 2012 — 자전축이 지구 시선과 거의 일치 |
| `activity_log_rhk` | n/a (A형은 대류 Ca II H&K 원이 없음) | high | A0V 왜성은 복사 외피라 채층 활동 지수가 정의 안 됨. Robrade & Schmitt 2011 (`2011A&A...531A..58R`) 의 log L_X ≈ 25.5–26.0 erg/s X-ray 검출은 이상하게 약함 — 논쟁적이며 자기 극 면 기하 (Petit 2010) 에서 비롯되었을 가능성 |
| `disk_present` | true | high | Aumann 외 1984 — IRAS 60/100 μm 초과. Vega-like 원반의 *정의적* 관측 |
| `disk_belts` | warm, cold | high | Su 외 2013 두 성분 SED. 따뜻한 내부 띠 + 차가운 외부 띠가 cleared gap 으로 분리 |
| `disk_warm_inner_radius_au` | 14 ± 2 | medium | Su 외 2013 — ~14 AU 따뜻한 소행성대 유사 내부 띠 (Spitzer-IRS + Herschel-PACS) |
| `disk_warm_dust_temperature_k` | 170 | medium | Su 외 2013 두 성분 SED — 따뜻한 dust 분포 |
| `disk_warm_mass_mearth` | 0.0003 | medium | Su 외 2013 — 따뜻한 띠 dust 질량 |
| `disk_warm_tint_rgb_hex` | `#f0d0a0` (따뜻한 amber, 더 뜨거운 내부 띠) | low | Tie-break. 170 K 가공된 규산염 grain 이 A0V 빛을 차가운 외부 띠보다 더 따뜻하게 산란. 무채색 대신 interesting-first |
| `disk_warm_opacity` | 0.02 | low | Tie-break. τ ~ 10⁻⁴ (Su 2013); 희미하지만 보이는 값으로 boost |
| `disk_cold_inner_radius_au` | 110 ± 9 | medium | Su 외 2013 — 차가운 카이퍼대 유사 내부 가장자리 ~110 AU (2026-05-29 감사: 62 에서 정정) |
| `disk_cold_outer_radius_au` | 200 ± 20 | medium | Sibthorpe 외 2010 (`2010A&A...518L.130S`) Herschel-PACS — 차가운 띠가 ~200 AU 까지 확장 |
| `disk_cold_dust_temperature_k` | 50 | medium | Su 외 2013 — 차가운 dust 분포 |
| `disk_cold_mass_mearth` | 0.013 | medium | Su 외 2013 — 차가운 띠 dust 질량. 모천체 질량은 훨씬 크지만 미관측 |
| `disk_cold_tint_rgb_hex` | `#d8d8e4` (희미한 차가운 회색, 얼음 외부 띠) | low | Tie-break. 50 K 얼음 grain 이 A0V 빛을 따뜻한 띠보다 더 푸르고 희미하게 산란. interesting-first |
| `disk_cold_opacity` | 0.06 | low | Tie-break. τ ~ 10⁻⁴ (Su 2013); 가시성 위해 boost. 보수적 값은 Open items 에 |
| `disk_morphology` | 두 띠. ~14 AU 따뜻한 소행성대 유사 + ~110–200 AU 차가운 카이퍼대 유사 + cleared gap (14→110 AU) = 행성소체 휘젓는 행성 함의 | high | Su 외 2013 두 성분 SED + Spitzer-MIPS 영상. Cleared gap 이 Vega 의 가장 강한 간접 행성 증거 |
| `disk_resolved_imaging` | true | high | Holland 1998 SCUBA 850 μm (`1998Natur.392..788H`); Wilner 2002 OVRO 1.3 mm; Su 2013 Spitzer-MIPS; Sibthorpe 2010 Herschel-PACS; Hughes 2012 ALMA |
| `disk_imaging_observatory` | IRAS (1983) → JCMT-SCUBA (Holland 1998) → Spitzer-MIPS (Su 2013) → Herschel-PACS (Sibthorpe 2010) → ALMA (Hughes 2012) | high | Vega-like 표준 관측 사슬 |
| `disk_imaging_inclination_deg` | 6.2 (정면, 별의 pole-on 기하에 lock) | medium | Sibthorpe 2010 / Su 2013 — 원반 i ≈ 6° 가 별 자전축과 일치 (두 띠 coplanar) |
| `disk_planetesimal_belt_inferred` | true | high | 110–200 AU 의 dust 수명이 0.45 Gyr 시스템 연령보다 훨씬 짧음. 행성소체 보충 필수 (Sibthorpe 2010 §5) |

## Surface synthesis

Vega 의 "표면" 은 단일 온도 광구가 아닙니다. Aufdenberg 외 2006 과 Monnier 외 2012 의 CHARA Array 간섭계 캠페인은 자전축이 지구 시선에서 6.2° 만 기울어진 거의 pole-on 으로 보이는 편구형 자전체로 별을 분해합니다. ω/ω_crit ≈ 0.91 — 적도가 breakup 속도의 91% 로 회전합니다. 고전적 von Zeipel 정리 (1924) 는 복사 외피에서 flux ∝ g_eff^β 와 β = 0.25 를 예측하며, 경험적 fit 은 β ≈ 0.231 (Monnier 2012) 입니다. 가시적 결과는 뜨겁고 밝은 극 — T_pole ≈ 10150 K — 이 관측자를 직접 향하고, 그 주위를 T_eq ≈ 7900 K 의 차가운 적도 띠가 limb 에서 어둡고 약간 노랗게 두른 환형으로 감쌉니다. 이 2250 K 의 극-적도 온도 기울기가 Vega 의 결정적 시각 속성이고, 모든 고전 "Vega 는 뜨거운 청백색 A0" 교과서 그림이 세부에서 틀린 이유입니다. 관측자가 실제로 보는 모습은 미세하게 차가운 후광을 두른, 작고 강렬하게 빛나는 백청색 점에 더 가깝습니다.

Pole-on 기하에는 NearStars 렌더러에 관련된 두 번째 결과가 있습니다. 적도 limb 어둠은 고전적 limb darkening 이 아니라 중력 감광이 지배합니다. Claret 2011 / Kervella 2017 류의 단일 매개변수 α exponent 는 Vega 의 H 밴드 간섭계 visibility 에 맞지 않습니다. cfg 에 유의미한 필드는 중력 감광 β 계수와 경사이며, 둘이 결합해 관측된 밝기 프로필을 만듭니다. NearStars 는 단일 α 로 압축하지 않고 경사와 극/적도 온도를 명시적으로 저장합니다.

Vega 는 또한 화학적으로 특이한 λ Boötis 등급 A형의 일원입니다 (Adelman & Gulliver 1990; Yoon 2010 의 best-fit 모델이 [M/H] ≈ −0.5 를 채택). 광구는 별 전체 조성 대비 무거운 원소가 결핍되어 보이며, gas-depleted 성간 물질의 선택적 강착 또는 원반 분별 작용으로 설명됩니다. 표면 metallicity 가 SED 를 약간 푸른쪽으로 (UV line blanketing 감소) 이동시켜, cream 같은 흑체 매칭보다 `#cfe0ff` 의 시각 선택을 강화합니다.

광구는 의미 있는 대류 입상 구조를 호스트하기에 너무 뜨겁습니다. 외피가 복사이며, 표면 구조는 대류 cell 이 아니라 회전이 지배하고, spot coverage 는 본질적으로 0 입니다. Petit 외 2010 (`2010A&A...523A..41P`) 이 ~0.6 G longitudinal 약자기장을 검출했고 ZDI 가 극 자기 spot 을 시사 — 이는 "non-Ap" A형의 첫 자기 검출 중 하나이고 비정상적으로 약한 X-ray 방출을 설명할 가능성이 있지만, 일반적인 cfg 시간 단위에서 가시 측광 변동은 만들지 않습니다.

## Atmosphere synthesis

A0V 왜성은 차가운 별 의미의 채층을 가지지 않습니다. 복사 외피가 Ca II H&K 방출을 구동할 대류 다이나모를 제공하지 않으므로 표준 log R'HK 활동 지수는 Vega 에 정의되지 않습니다. Mg II h+k 와 Ca II H&K 선은 채층 core 반전 없이 순수 광구 흡수로만 나타나며, 이는 A0V 측광 표준의 정의적 특징입니다.

그럼에도 X-ray 방출이 log L_X ≈ 25.5–26.0 erg/s 로 약하게 검출되었습니다 (Robrade & Schmitt 2011, `2011A&A...531A..58R`). 태양 코로나 출력의 7 차수 약함이며 다이나모 부재 상황에서 다소 곤혹스러운 결과입니다. 두 가설이 경쟁 — Petit 2010 의 ZDI 극 spot 검출과 일치하는 자기 극 정렬 약한 코로나 (이 경우 X-ray 는 자기 극 근처 hot ring 에서 다시 거의 정면으로 보이는 형태) 와, 저질량 동반체 오염 또는 원반에서 비롯된 CME 류 활동. NearStars 는 Vega 에 인게임 플레어 모델을 채택하지 않습니다 — 관여 시간 단위와 에너지가 플레이어 인지 수준을 한참 밑돕니다.

다만 적분 UV 출력은 막대합니다. 47 L☉ 와 근자외선 SED peak 로 Vega 는 동등 거리에서 태양 UV flux 의 ~30 배를 전달합니다. XUV 광증발이 (Wilner 2002; Sibthorpe 2010) 내부 원반에서 작은 dust grain 을 제거하고 따뜻한 띠와 차가운 띠 사이 간극 형성에 부분적으로 기여한 메커니즘으로 제기되었습니다. 가상의 내부 행성은 극단적 UV 환경을 겪을 텐데, 행성 미검출이라 flavor text 수준의 관심사입니다.

확장된 광학 깊이 구조의 의미로 Vega 의 가시 "하늘" 은 채층이 아니라 작은 각거리에서 산란광으로 보이는 둘러싼 잔해 원반과, 광구 자체의 중력 감광 극-적도 기울기가 지배합니다. 대기 haze 도 없고, G 왜성처럼 limb 위 코로나 특징도 없고, 관측 가능한 확장 outflow 도 없습니다.

## Rotation & spin synthesis

Vega 는 고전 line broadening 측정 (Gulliver 외 1994) 에서 v_eq sin i = 22 ± 2 km/s 로 회전합니다. 이 작은 값이 역사적으로 Vega 를 느린 자전체로 분류시켰습니다. CHARA 간섭계 분해 (Aufdenberg 2006; Peterson 2006, `2006Natur.440..896P`) 가 그 작은 sin i 가 작은 v_eq 가 아니라 작은 i 임을 밝혔습니다. 진짜 적도 속도는 i ≈ 6.2° 로 보이는 274 ± 14 km/s 입니다. Vega 를 ω/ω_crit ≈ 0.91 — 밝은 별 중 가장 빠르게 회전하는 부류 — 에 위치시킵니다.

기하에서 유도되는 적도 자전 주기는 P_eq = 2π · R_eq / v_eq ≈ 2π · 2.726 · 696000 km / 274 km/s ≈ 12.5 시간 입니다. Petit 외 2010 이 자기장 회전 변조 ZDI 에서 0.732 일 (~17.6 시간) 주기를 유도한 것은 자기 구조가 v_phys 가 더 작은 고위도에 anchor 되어 있는 것과 일관됩니다 (중력 감광 외피의 차등 회전). NearStars 는 cfg 안정 회전 핸들로 12.5 시간 적도 주기를 사용하고, ZDI 값은 미래 "magnetic surface" cfg variant 용 Open item 으로 보존합니다.

자전축은 전체 별에서 가장 잘 제약된 방향 매개변수입니다. i ≈ 6.2° ± 0.3° (Aufdenberg 2006), 즉 Kerbal 프레임에서 Vega 의 극이 거의 정확히 Sol 을 향합니다. NearStars 렌더러에서의 시각적 결과는, 지구/Kerbin 근처 어떤 시점에서든 플레이어는 Vega 의 뜨겁고 밝은 극을 내려다보고, 차가운 적도 띠는 edge-on 으로 어두운 rim 으로 보입니다. 이것이 cfg 가 묘사하는 기하 — tilt 를 발명할 필요 없고, 문헌이 직접 제공.

원반과 자전축의 obliquity 는 오차 내에서 정렬됩니다 (Sibthorpe 2010; Su 2013). 원반과 자전 spin 이 원래 원시 행성계 원반 각운동량 벡터를 공유하는 coeval-formation 시나리오와 일관됩니다. cfg 에는 세차나 secular axis drift 가 구현되지 않습니다.

## Visual styling

- **글로벌 외관 (궤도 뷰).** 작고 강렬한 백청색 별 원반 (정면 극, T ≈ 10150 K) 주변에 차가운 적도가 어두운 limb 띠를 형성하는 옅은 따뜻한 크림 후광. KSP 렌더링 거리에서 Vega 는 거의 점광원이며 중력 감광 기울기는 매우 가까운 fly-by 에서만 간신히 분해 가능 — 시각은 둘러싼 정면 잔해 원반이 압도.
- **표면 디테일.** 입상 구조 없음, 흑점 없음, faculae 없음. 지배적인 가시 특징은 2250 K 극-적도 온도 기울기. 시야 중심 근처의 찬란한 `#cfe0ff` 가 적도 limb 근처의 `#e8e2d6` 로 페이드. 전환은 매끄럽고 (선명한 경계 없음) pole-on 관측자에게는 거의 축대칭.
- **극/적도 특징.** Petit 2010 의 옅은 ZDI 극 자기 spot — 현 cfg 에서는 미렌더링이지만 Open items 의 확장 후보.
- **대기 haze.** 없음. A형은 채층이 없고, limb 가 부드러운 haze 띠 없이 깨끗하게 잘림.
- **잔해 원반 시각 (간판 특징).** Vega 는 IRAS 원형 잔해 원반이고 cfg 는 이를 거리에서 시스템의 시각적 지배 요소로 묘사. 원반은 두 개의 구분된 성분을 가진 정면 luminous 구조로 렌더링됩니다. ~14 AU 의 내부 따뜻한 띠는 `#f0d0a0` 의 따뜻한 amber (170 K dust 의 산란광) 로 빛나는 옅고 좁은 환형, 궤도 뷰 zoom 에서는 본질적으로 비가시이고 플레이어가 내부 시스템에 접근할 때 보이기 시작; 14–110 AU 의 cleared gap 은 미발견 행성소체-휘젓는 행성이 존재해야 할 위치를 시각적으로 식별하는 빈 환형 — cfg 가 Vega 의 "잃어버린 행성" 을 가장 강력하게 암시; 110–200 AU 의 외부 차가운 띠는 주된 시각 요소, `#d8d8e4` 희미한 차가운 회색 톤 (50 K 얼음 dust 의 산란광 proxy 색), opacity 0.06, Sibthorpe 2010 morphology 따라 외부보다 내부 가장자리가 더 선명한 정면 밝은 ring — IRAS 가 발견한 구조이자 cfg 의 "당신은 Vega 에 있다" 단서.
- **별이 하늘에서 보이는 모습 (1 AU 의 가상 내부 행성에서).** 각 지름 ≈ 2 · R_eq / a · (180·60/π) ≈ 0.087° (~5.2 arcmin) — 지구에서 본 태양의 ~16% 각 크기이지만 단위 면적당 ~7 배 밝음 (Teff 비율)^4. 조명 색온도 ~9700 K 는 약간 푸른 daylight 로 렌더링 — sunlight 가 태양 참조 대비 눈에 띄게 더 푸른 톤.
- **가상 내부 행성에서 본 원반.** 110–200 AU 의 외부 띠가 정면 ring 으로 하늘에서 ~30° 에서 ~90° 까지 차지 — NearStars 에서 가장 시각적으로 두드러진 특징 중 하나인 striking 한 야간 "Vega ring". Pole-on 기하 덕에 ring 이 edge-on streak 가 아니라 진짜 ring (완전 환형) 으로 보입니다.
- **자매 행성이 하늘에서.** 확정 없음. cfg 에 Vega 의 행성 body 없음. Su 2013 의 gap-clearer 행성이 미래 cfg variant 에 추가되면 내부 시스템 점광원으로 등장할 예정.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Aumann H. H. 외 1984** — *Discovery of a Shell Around Alpha Lyrae*, ApJ 278, L23 (`1984ApJ...278L..23A`). "Vega 현상" 을 명명한 IRAS 발견 논문. 60 + 100 μm 초과. 최초로 식별된 잔해 원반.
- **Aufdenberg J. P. 외 2006** — *First results from the CHARA Array. VII. Long-baseline interferometric measurements of Vega consistent with a pole-on, rapidly rotating star*, ApJ 645, 664 (`2006ApJ...645..664A`, arXiv:astro-ph/0603327). CHARA H 밴드 간섭계. v_eq = 274 km/s, i = 5° ± 2°, T_pole = 10150 K, T_eq = 7900 K, ω/ω_crit = 0.91. Vega 의 현대적 그림을 정의.
- **Peterson D. M. 외 2006** — *Vega is a rapidly rotating star*, Nature 440, 896 (`2006Natur.440..896P`). 독립적 NPOI 간섭계 확인. Aufdenberg 와 동일 결론.
- **Yoon J. 외 2010** — *A New View of Vega's Composition, Mass, and Age*, ApJ 708, 71 (`2010ApJ...708...71Y`). 간섭계 R + SED 에 회전 진화 모델 fit. M = 2.135 ± 0.075 M☉, 연령 0.455 ± 0.013 Gyr, [M/H] = −0.5. 오래된 Vega "metallicity problem" 을 정상 metallicity 외피에서 λ Boo 표면 결핍으로 해소.
- **Monnier J. D. 외 2012** — *Resolving Vega and the Inclination Controversy with CHARA/MIRC*, ApJ 761, L3 (`2012ApJ...761L...3M`). 더 높은 해상도 CHARA/MIRC 영상. R_eq = 2.726 ± 0.006 R☉. 작은 Aufdenberg 경사와 후속 우려를 조정. 연령 0.7 ± 0.075 Gyr (Yoon 과 다름에 주의).
- **Su K. Y. L. 외 2013** — *Asteroid Belts in Debris Disk Twins: Vega and Fomalhaut*, ApJ 763, 118 (`2013ApJ...763..118S`, arXiv:1211.7298). Spitzer-IRS + Herschel-PACS 두 성분 SED fit. 14 AU 따뜻한 170 K 내부 띠 + ~110–200 AU 차가운 50 K 외부 띠. 행성소체-휘젓는 행성을 함의하는 cleared gap. 두 띠 cfg morphology 를 정의.
- **Sibthorpe B. 외 2010** — *The Vega debris disc: A view from Herschel*, A&A 518, L130 (`2010A&A...518L.130S`). Herschel-PACS 70/100/160 μm 분해 영상. 외부 가장자리보다 내부 가장자리가 선명한 원반 radial profile. 작은 grain 의 radiation pressure / PR-drag 제거 지지. 외부 가장자리 반지름 ~200 AU.
- **Holland W. S. 외 1998** — *Submillimetre images of dusty debris around nearby stars*, Nature 392, 788 (`1998Natur.392..788H`). JCMT-SCUBA 850 μm. Vega 원반의 첫 서브밀리미터 분해 영상. 차가운 잔해 ring 구조 확립.
- **Hughes A. M. 외 2012** — *Confirmation of the Vega Asteroid Belt with Combined Spitzer and Submillimeter Array Observations*, ApJ 750, 82 (`2012ApJ...750...82H`, arXiv:1203.0598). SMA / 초기 ALMA 시대 880 μm 관측. 차가운 띠 구조 확인. 내부 가장자리 제약.
- **Petit P. 외 2010** — *A weak magnetic field at the surface of Vega*, A&A 523, A41 (`2010A&A...523A..41P`, arXiv:1006.5868). NARVAL spectropolarimetry. ~0.6 G longitudinal 자기장. 가능한 극 자기 spot. P_rot ZDI 추정 0.732 d (적도 12.5 h 보다 길음, 고위도 anchored).

### Read (context / methodology, not directly decision-driving)

- **Adelman S. J. & Gulliver A. F. 1990** — Vega 의 abundance 분석. λ Boötis 분광 특이성 식별. [M/H] = −0.5 광구값의 methodology 참조.
- **Gulliver A. F. 외 1994** — *The Spectrum of Vega: A Pole-on View of a Rapidly Rotating Star*, ApJ 429, L81. Vega 의 작은 v sin i 가 큰 v 를 숨긴다는 (CHARA 이전) 분광학적 첫 시사.
- **Robrade J. & Schmitt J. H. M. M. 2011** — *X-ray detection of the very low-mass companion of Vega-like α Lyrae*, A&A 531, A58 (`2011A&A...531A..58R`). XMM-Newton 검출 log L_X ≈ 25.5–26 erg/s. 약한 코로나 vs 동반체 오염의 논쟁적 해석.
- **Hurt S. A. 외 2021** — *A Decade of Radial Velocity Monitoring of Vega*, AJ 161, 157 (`2021AJ....161..157H`). 현재까지 가장 깊은 RV 상한. 0.04 AU 의 0.6 일 후보 신호, 미확인. ~7 AU 이내 토성 질량 동반체 배제.
- **Wilner D. J. 외 2002** — *Toward Imaging the Vega Belt*, ApJ 569, L115. OVRO 1.3 mm 간섭 영상. 초기 서브밀리미터 구조 매핑.
- **Hunsch M. & Schmitt J. H. M. M. 2019** — Vega 포함 A형 행성 host 에 대한 RV 제약 리뷰. no-planet RV 상한의 methodology 참조.

### Read (instrument-only, not visual-informative)

- **Decin G. 외 2003** — Vega 의 ISO 측광 cross-calibration. 장비 논문.
- **Marsh K. A. 외 2006** — Vega 를 측광 표준으로 사용하는 서브밀리미터 영상 장비 검증. morphology 제약 없음.
- **Absil O. 외 2006** — CHARA/FLUOR K 밴드 초과 검출. 뜨거운 exozodiacal dust vs 장비 systematic 의 모호한 해석.
- **Defrère D. 외 2011** — KIN nulling 간섭 exozodi 상한. 관련 baseline 에서 검출 없음.

### Not read — no arXiv preprint or low-priority (~40 papers)

전체 filtered bib 는 미래 작업으로 보존됩니다. 스킵된 항목에는 측광 표준 검증 논문 (Bohlin 2007, 2014, 2020 — Vega 측광 영점, methodology only), SETI laser-emission 탐색 (Stone 2005, Tellis 2017 — cfg 결정 콘텐츠 없음), WASP/CHARA 파이프라인 개발 맥락의 Vega 컨퍼런스 abstract 가 포함됩니다. 가장 눈에 띄는 5개 스킵 항목. Bohlin R. C. 2007 STIS 스펙트로포토메트릭 표준 재보정 (순수 측광 methodology); Hinz P. M. 외 2001 MMT 적응광학 영상 시도 (Spitzer 이상의 morphology 제약 없음); Greaves J. S. 외 2014 JCMT POL-2 편광 후속 (장비 개발 논문, 새 기하 없음); Defrère D. 외 2021 Vega 포함 LBTI exozodi survey 결과 (non-detection 과 일관); Su K. Y. L. 외 2005 Spitzer-MIPS first-look (Su 2013 으로 대체됨).

## Open items for follow-up

- **disk 지오메트리가 `disks_curated.json` 에 multi-belt 로 기록됨** (2026-05-29 감사). Vega 의 따뜻한 띠 + 차가운 띠가 별도 `belt` 항목이며, Decisions 표가 belt별 `disk_<belt>_*` 필드로 렌더 → belt당 Kopernicus Ring 하나씩. 남은 것은 tie-break per-belt tint 를 대체할 grain-size / Mie 색 합성.
- **Yoon 2010 (0.455 ± 0.013 Gyr) 과 Monnier 2012 (0.7 ± 0.075 Gyr) 의 연령 불일치.** 두 논문 모두 회전 모델 isochrone 을 사용하지만 boundary condition 이 다름. cfg 는 Yoon 표제값 채택. 해결에는 Monnier 2012 §4 의 deep-read 와 Tetzlaff 2011 운동학 연령 cross-check 가 필요.
- **Hurt 2021 의 0.04 AU 0.6 일 후보.** 2026 년 이후 후속 관측이 이를 진짜 행성으로 확정하면 (현재 미확인, 별 활동일 가능성) 새 Decisions 항목 `circumstellar_planet_present: true` 가 필요하고 행성 body cfg 가 추가되어야 함.
- **Su 2013 의 14–110 AU gap-clearer 행성.** 현재는 원반 morphology 에서만 유도. 미래 JWST-NIRCam 또는 extreme-AO 직접 영상 확인이 추론을 확정된 행성 body 로 전환하면 cfg 추가 트리거.
- **보수적 opacity 원반 variant.** 현 cfg 는 `disk_opacity` = 0.06 (interesting-first tie-break) 사용. 관측 일치 값은 τ ~ 10⁻⁴ (본질적으로 비가시). 물리적으로 충실한 opacity 를 가진 "realistic" cfg variant 를 플레이어 선택 옵션으로 작성해야 함.
- **Petit 2010 의 극 자기 spot.** 현재 미렌더링. 미래 cfg variant 가 ZDI 구조에 맞춰 가까운 fly-by 뷰에 극에 옅은 푸른 spot 을 추가할 수 있음.
- **원반 dust 크기 + 색 합성 업그레이드.** 현 `disk_tint_rgb_hex` 는 HST-STIS Fomalhaut 팔레트 관행 사용. tie-break 가 아닌 grain size 분포 + Vega 조명 스펙트럼 (Mie scattering) 에서 물리적으로 유도된 색이 적절.
- **Cycle phase / 에포크 동기화.** Vega 는 (복사 외피라) 관측된 활동 cycle 이 없어 α Cen A 와 달리 에포크 동기화가 불필요. 다만 Petit 2010 자기 기하가 천천히 회전하는 극 특징으로 구현되면 에포크 참조가 필요해질 것.

## Related

- [alpha-centauri-a](alpha-centauri-a.md) — 다른 시나리오 archetype. 조용한 G2V 태양 유사 vs Vega 의 젊은 빠른 자전체 A0V archetype. stellar Phase 3 의 canonical 구조 템플릿으로 참조.
- [methodology](../reference/methodology.md) — Decisions table 의 스키마 출처.
- [data-sources](../reference/data-sources.md) — `db/systems/vega.json` 의 SIMBAD 유래 천체측정 + 분광 필드의 provenance.
- [mod-reference](../reference/mod-reference.md) — Kopernicus + Firefly + Scatterer cfg 필드 맵. circumstellar disk 필드는 star body 에 attach 되는 Kopernicus Ring 컴포넌트로 매핑.
