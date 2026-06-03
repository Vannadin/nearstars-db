<!-- Vega Phase 3 합성. cfg-ready 결정과 근거 -->
# Vega — Phase 3 합성

Vega (α Lyrae, HD 172167, HIP 91262) 는 밤하늘에서 다섯 번째로 밝은 별이자 A0Va 왜성의 원형입니다. 거리는 7.679 pc (시차 130.23 mas, SIMBAD). 역사적으로 Johnson 측광 시스템의 영점이었으며, 1983 년 IRAS 가 관측한 이후로 잔해 원반의 원형이 되었습니다. "Vega-like" 초과라는 표현 자체가 여기서 만들어졌습니다 (Aumann 외 1984, `1984ApJ...278L..23A`). NearStars DB 가 기록하는 항성 매개변수는 가장 최근의 CHARA/MIRC 영상 개정인 Monnier 외 2012 (`2012ApJ...761L...3M`) 에 anchor 되어 있습니다. M = 2.15 (+0.10/−0.15) M☉, 적도 반지름 R = 2.726 ± 0.006 R☉ (극 2.418), 표면적 평균 유효 온도 Teff = 9360 ± 90 K (극 10070 K vs 적도 8910 K), 볼로메트릭 광도 L = 47.2 ± 2.0 L☉. 이 값들은 모두 Vega 를 천천히 자전하는 측광 표준이 아니라 거의 극을 향해 회전하는 빠른 자전체로 보는 현대적 이해의 산물입니다. Monnier 는 이전의 Aufdenberg 외 2006 / Yoon 외 2010 작업보다 더 약한 중력 감광과 더 느린 자전 (ω/ω_crit = 0.774) 을 발견했습니다.

Vega 에는 확정된 행성이 없습니다. 가장 깊은 RV 탐색 (Hunsch & Schmitt 2019 및 후속 연구; Hurt 외 2021, `2021AJ....161..157H`) 도 ~7 AU 안쪽에서 0.3 M_Jup 보다 큰 동반체를 배제하고, 내부 소행성대 영역 전반에 ~토성 질량 상한을 둡니다. Hurt 2021 이 보고한 ~0.6 일 0.04 AU 신호 후보가 있으나 현 시점에서 확정 상태가 아닙니다. Vega 의 시각적 정체성을 결정짓는 것은 두 띠 (two-belt) 잔해 원반입니다 — 소행성대 유사 구조에 해당하는 ~14 AU 의 따뜻한 내부 영역, 그리고 ~70 AU 부터 ~200 AU 까지 분해된 차가운 외부 고리. 둘 사이의 비워진 간극은 14–70 AU 사이에 미발견 행성이 행성소체 띠를 휘젓고 있다는 가장 강한 간접 증거입니다 (Su 외 2013, `2013ApJ...763..118S`; Sibthorpe 외 2010, `2010A&A...518L.130S`; Hughes 외 2012, `2012ApJ...750...82H`).

**NearStars 의 시나리오 선택. 거의 극을 향한 A0 Va 빠른 자전체 (i ≈ 6.5°). 중력 감광으로 극 ~10070 K 에서 적도 ~8910 K 로 떨어지는 기울기를 가지고, 정면에서 보이는 광도 높은 두 띠 잔해 원반의 중심에 자리잡고 있는 별입니다.** Pole-on 기하가 시각적으로 가장 정의적인 특징입니다. 대부분의 A형 별 일러스트는 균일한 백청색 원반을 보여주지만, cfg 는 Vega 의 뜨겁고 밝은 극이 플레이어를 직접 바라보고 차가운 적도는 어두운 limb 띠를 형성하도록 묘사합니다. 원반은 IRAS 발견 시대의 정면 dust ring 으로 렌더링됩니다. Confidence=high 줄들은 모두 관측을 추종하고, 원반 기하 행 (row) 들은 분해 영상은 있으나 모델 매개변수화가 갈리는 (Su 2013 vs Sibthorpe 2010 의 inner radius 가 ~3 AU 차이) 부분이라 Confidence=medium 으로, tint hex 와 opacity 같은 합성-전용 필드는 Basis 컬럼에 명시된 tie-break 로 Confidence=low 입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | A0 Va | high | Keenan & McNeil 1989; SIMBAD harmonized MK |
| `mass_msun` | 2.15 (+0.10/−0.15) | high | Monnier 외 2012 (`2012ApJ...761L...3M`) — 회전을 고려한 Geneva-track fit (Phase 2 recommended; Yoon 2010 의 2.135 와 일치) |
| `radius_rsun` (적도) | 2.726 ± 0.006 | high | Monnier 외 2012 — CHARA/MIRC 영상; 편구형 빠른 자전체의 적도 반지름 (R_pole = 2.418 ± 0.012 R☉, R_eq/R_pole ≈ 1.13) |
| `teff_k` (유효) | 9360 ± 90 | high | Monnier 외 2012 — 표면적 평균 Teff (Phase 2 recommended; T_pole 10070 / T_eq 8910; SIMBAD 9692 를 대체) |
| `luminosity_lsun` | 47.2 ± 2.0 | high | Monnier 외 2012 — 볼로메트릭 (Phase 2 recommended; pole-on 으로 부풀려진 겉보기 값은 58.4 ± 2.2) |
| `metallicity_fe_h_dex` | −0.5 | medium | Yoon 2010 — metal-weak λ Boo 표면 조성 (Z = 0.006–0.008). Vega 는 알려진 λ Boo 등급 A형 (Adelman & Gulliver 1990) |
| `age_gyr` | 0.7 (+0.15/−0.075) | high | Monnier 외 2012 — 회전을 고려한 진화 트랙 (Phase 2 recommended). Yoon 2010 의 비회전 isochrone 0.455 ± 0.013 Gyr 와 DOCUMENTED DIVERGENCE (Canonical alternatives 참조) |
| `rotation_v_eq_km_s` | ~195 | high | Monnier 외 2012 — 개정된 (더 느린) 자전; ω/ω_crit = 0.774 ± 0.012 (Aufdenberg/Peterson 의 이전 274 km/s 는 더 빠른 ω ≈ 0.91 을 가정) |
| `rotation_period_days` | 0.71 ± 0.03 | high | Petit 외 2010 (`2010A&A...523A..41P`) — spectropolarimetric 자기 자전 주기 (≈17.0 h; Alina 2012 가 확인; Phase 2 recommended) |
| `limb_darkening_alpha_h` | n/a (중력 감광 모델로 대체) | high | Vega 는 단일 α limb-darkening law 로 잘 맞지 않음. 2D von Zeipel 중력 감광 β = 0.231 ± 0.028 (Monnier 2012) 이 cfg 에 유의미한 매개변수 |
| `visual_gravity_darkening_pole_equator_temp_diff_k` | 1160 (T_pole 10070 K, T_eq 8910 K) | high | Monnier 2012 — CHARA/MIRC; 현대 개정값은 Aufdenberg 2006 의 2250 K (10150/7900) 보다 더 약한 중력 감광을 발견 |
| `visual_surface_tint_hex_primary` | `#cfe0ff` (pole-on 핫화이트블루, 적도 limb 는 약간 차가운 톤) | low | Tie-break. 면적 평균 9360 K 의 흑체는 거의 순수한 white-blue. cfg 는 pole-on 시야를 지배하는 뜨거운 극면을 강조해 약간 더 푸르게 조정하고, limb 는 적도 띠에서 `#e8eef8` (~8910 K) 로 어두워짐. `conflict-resolution.md` 의 interesting-first 원칙 적용 |
| `stellar_color_temp_k` | 9360 | high | 인게임 조명용으로 면적 평균 Teff 에서 유도 |
| `radius_rsun_polar` | 2.418 ± 0.012 | high | Monnier 외 2012 — 편구형 자전체의 극 반지름 (cfg 는 별을 편구형으로 렌더해야 함; 평균 ~2.6 R☉) |
| `rotation_omega_crit_ratio` | 0.774 ± 0.012 | high | Monnier 외 2012 — 임계 (break-up) 각속도 대비 비율 (Aufdenberg 의 0.91 대비 개정된 더 느린 값) |
| `visual_pole_on_inclination_deg` | ~6.5 | high | Monnier 외 2012 (i = 6.2 ± 0.4°); 자전축이 지구 시선과 거의 일치 |
| `activity_log_rhk` | n/a (A0 V 는 대류 다이나모/채층이 없음 — 의도적으로 미기록) | high | A0 V 복사 외피 — log R'HK 가 정의되지 않음. Vega 자체는 X-ray 비검출, L_X < 2 × 10²⁵ erg/s (Pease, Drake & Kashyap 2006). Robrade & Schmitt 2011 이 검출한 log L_X ≈ 25.5–26 X-ray 는 Vega 가 아니라 저질량 COMPANION 에서 비롯된 것으로 본다 |
| `disk_present` | true | high | Aumann 외 1984 — IRAS 60/100 μm 초과. Vega-like 원반의 *정의적* 관측 |
| `disk_belts` | warm, cold | high | Su 외 2013 두 성분 SED. 따뜻한 내부 띠 + 차가운 외부 띠가 cleared gap 으로 분리 |
| `disk_warm_inner_radius_au` | 14 ± 2 | medium | Su 외 2013 — ~14 AU 따뜻한 소행성대 유사 내부 띠 (Spitzer-IRS + Herschel-PACS) |
| `disk_warm_dust_temperature_k` | 170 | medium | Su 외 2013 두 성분 SED — 따뜻한 dust 분포 |
| `disk_warm_mass_mearth` | 0.0003 | medium | Su 외 2013 — 따뜻한 띠 dust 질량 |
| `disk_warm_tint_rgb_hex` | `#fffefe` (거의 중성; vivid `#fffdfc`) | low | 측정된 광학 색 없음 (열복사/mm 만). Mie 반사율 합성. 큰 규산염 입자 (a_min ~11 µm) 가 거의 중성 반사율 (B/I 0.91) 을 가지므로, 렌더러가 그 위에 A0V 청백색 별빛을 입혀 인게임에서 옅은 청백색으로 보입니다. vivid 팩은 `#fffdfc` |
| `disk_warm_opacity` | 0.02 | low | Tie-break. τ ~ 10⁻⁴ (Su 2013); 희미하지만 보이는 값으로 boost |
| `disk_cold_inner_radius_au` | 110 ± 9 | medium | Su 외 2013 — 차가운 카이퍼대 유사 내부 가장자리 ~110 AU (2026-05-29 감사: 62 에서 정정) |
| `disk_cold_outer_radius_au` | 200 ± 20 | medium | Sibthorpe 외 2010 (`2010A&A...518L.130S`) Herschel-PACS — 차가운 띠가 ~200 AU 까지 확장 |
| `disk_cold_dust_temperature_k` | 50 | medium | Su 외 2013 — 차가운 dust 분포 |
| `disk_cold_mass_mearth` | 0.013 | medium | Su 외 2013 — 차가운 띠 dust 질량. 모천체 질량은 훨씬 크지만 미관측 |
| `disk_cold_tint_rgb_hex` | `#fffefe` (거의 중성; vivid `#fffdfc`) | low | 측정된 광학 색 없음 (열복사 IR/mm 만). Mie 반사율 합성. 따뜻한 띠와 동일한 거의 중성인 큰 입자 (B/I 0.91). 렌더러가 그 위에 A0V 청백색 별빛을 입힙니다. 두 벨트는 색조가 아니라 반지름/밝기로 구분됩니다. vivid 팩은 `#fffdfc` |
| `disk_cold_opacity` | 0.06 | low | Tie-break. τ ~ 10⁻⁴ (Su 2013); 가시성 위해 boost. 보수적 값은 Open items 에 |
| `disk_morphology` | 두 띠. ~14 AU 따뜻한 소행성대 유사 + ~110–200 AU 차가운 카이퍼대 유사 + cleared gap (14→110 AU) = 행성소체 휘젓는 행성 함의 | high | Su 외 2013 두 성분 SED + Spitzer-MIPS 영상. Cleared gap 이 Vega 의 가장 강한 간접 행성 증거 |
| `disk_resolved_imaging` | true | high | Holland 1998 SCUBA 850 μm (`1998Natur.392..788H`); Wilner 2002 OVRO 1.3 mm; Su 2013 Spitzer-MIPS; Sibthorpe 2010 Herschel-PACS; Hughes 2012 ALMA |
| `disk_imaging_observatory` | IRAS (1983) → JCMT-SCUBA (Holland 1998) → Spitzer-MIPS (Su 2013) → Herschel-PACS (Sibthorpe 2010) → ALMA (Hughes 2012) | high | Vega-like 표준 관측 사슬 |
| `disk_imaging_inclination_deg` | 6.2 (정면, 별의 pole-on 기하에 lock) | medium | Monnier 2012 의 항성 자전축 경사 i = 6.2° (원반은 coplanar/정면). Sibthorpe 2010 과 Su 2013 은 원반을 정면으로 기술하지만 수치 원반 경사는 보고하지 않으므로, 이 6.2° 는 원반 측정값이 아니라 항성 자전축에서 차용한 값 |
| `disk_planetesimal_belt_inferred` | true | high | 110–200 AU 의 dust 수명이 0.7 Gyr 시스템 연령보다 훨씬 짧음. 행성소체 보충 필수 (Sibthorpe 2010 §5) |

## Surface synthesis

Vega 의 "표면" 은 단일 온도 광구가 아닙니다. Aufdenberg 외 2006 과 Monnier 외 2012 의 CHARA Array 간섭계 캠페인은 자전축이 지구 시선에서 ~6.5° 만 기울어진 거의 pole-on 으로 보이는 편구형 자전체로 별을 분해합니다. Monnier 의 개정된 ω/ω_crit = 0.774 — 적도가 breakup 속도의 ~77% 로 회전합니다 (이전 Aufdenberg fit 은 0.91 을 주었음). 고전적 von Zeipel 정리 (1924) 는 복사 외피에서 flux ∝ g_eff^β 와 β = 0.25 를 예측하며, 경험적 fit 은 β ≈ 0.231 (Monnier 2012) 입니다. 가시적 결과는 뜨겁고 밝은 극 — T_pole ≈ 10070 K — 이 관측자를 직접 향하고, 그 주위를 T_eq ≈ 8910 K 의 차가운 적도 띠가 limb 에서 약간 어두운 환형으로 감쌉니다. 이 ~1160 K 의 극-적도 온도 기울기 (Monnier 2012; Aufdenberg 2006 의 2250 K 보다 약함) 가 Vega 의 결정적 시각 속성이고, 모든 고전 "Vega 는 뜨거운 청백색 A0" 교과서 그림이 세부에서 틀린 이유입니다. 관측자가 실제로 보는 모습은 미세하게 차가운 후광을 두른, 작고 강렬하게 빛나는 백청색 점에 더 가깝습니다.

Pole-on 기하에는 NearStars 렌더러에 관련된 두 번째 결과가 있습니다. 적도 limb 어둠은 고전적 limb darkening 이 아니라 중력 감광이 지배합니다. Claret 2011 / Kervella 2017 류의 단일 매개변수 α exponent 는 Vega 의 H 밴드 간섭계 visibility 에 맞지 않습니다. cfg 에 유의미한 필드는 중력 감광 β 계수와 경사이며, 둘이 결합해 관측된 밝기 프로필을 만듭니다. NearStars 는 단일 α 로 압축하지 않고 경사와 극/적도 온도를 명시적으로 저장합니다.

Vega 는 또한 화학적으로 특이한 λ Boötis 등급 A형의 일원입니다 (Adelman & Gulliver 1990; Yoon 2010 의 best-fit 모델이 [M/H] ≈ −0.5 를 채택). 광구는 별 전체 조성 대비 무거운 원소가 결핍되어 보이며, gas-depleted 성간 물질의 선택적 강착 또는 원반 분별 작용으로 설명됩니다. 표면 metallicity 가 SED 를 약간 푸른쪽으로 (UV line blanketing 감소) 이동시켜, cream 같은 흑체 매칭보다 `#cfe0ff` 의 시각 선택을 강화합니다.

광구는 의미 있는 대류 입상 구조를 호스트하기에 너무 뜨겁습니다. 외피가 복사이며, 표면 구조는 대류 cell 이 아니라 회전이 지배하고, spot coverage 는 본질적으로 0 입니다. Petit 외 2010 (`2010A&A...523A..41P`) 이 ~0.6 G longitudinal 약자기장을 검출했고 ZDI 가 극 자기 spot 을 시사 — 이는 "non-Ap" A형의 첫 자기 검출 중 하나이고 비정상적으로 약한 X-ray 방출을 설명할 가능성이 있지만, 일반적인 cfg 시간 단위에서 가시 측광 변동은 만들지 않습니다.

## Atmosphere synthesis

A0V 왜성은 차가운 별 의미의 채층을 가지지 않습니다. 복사 외피가 Ca II H&K 방출을 구동할 대류 다이나모를 제공하지 않으므로 표준 log R'HK 활동 지수는 Vega 에 정의되지 않습니다. Mg II h+k 와 Ca II H&K 선은 채층 core 반전 없이 순수 광구 흡수로만 나타나며, 이는 A0V 측광 표준의 정의적 특징입니다.

사실 Vega 자체는 X-ray 비검출입니다. Pease, Drake & Kashyap 2006 (`2006ApJ...636..426P`) 은 이 A형 별에 L_X < 2 × 10²⁵ erg/s 라는 깊은 상한을 두었습니다 — "가장 어두운 밝은 별". Robrade & Schmitt 2011 (`2011A&A...531A..58R`) 이 검출한 약한 log L_X ≈ 25.5–26 X-ray 는 Vega 의 복사 외피가 아니라 저질량 COMPANION 에서 비롯된 것으로 본다 (논문 제목 자체가 명시적입니다. "X-ray detection of the very low-mass companion of Vega-like α Lyrae"). 따라서 cfg 는 Vega 자체에 코로나 활동을 부여하지 않습니다. NearStars 는 Vega 에 인게임 플레어 모델을 채택하지 않습니다 — A0 V 복사 외피는 플레어를 만들지 않습니다.

다만 적분 UV 출력은 막대합니다. 47 L☉ 와 근자외선 SED peak 로 Vega 는 동등 거리에서 태양 UV flux 의 ~30 배를 전달합니다. XUV 광증발이 (Wilner 2002; Sibthorpe 2010) 내부 원반에서 작은 dust grain 을 제거하고 따뜻한 띠와 차가운 띠 사이 간극 형성에 부분적으로 기여한 메커니즘으로 제기되었습니다. 가상의 내부 행성은 극단적 UV 환경을 겪을 텐데, 행성 미검출이라 flavor text 수준의 관심사입니다.

확장된 광학 깊이 구조의 의미로 Vega 의 가시 "하늘" 은 채층이 아니라 작은 각거리에서 산란광으로 보이는 둘러싼 잔해 원반과, 광구 자체의 중력 감광 극-적도 기울기가 지배합니다. 대기 haze 도 없고, G 왜성처럼 limb 위 코로나 특징도 없고, 관측 가능한 확장 outflow 도 없습니다.

## Rotation & spin synthesis

Vega 는 고전 line broadening 측정 (Gulliver 외 1994) 에서 v_eq sin i = 22 ± 2 km/s 로 회전합니다. 이 작은 값이 역사적으로 Vega 를 느린 자전체로 분류시켰습니다. CHARA 간섭계 분해 (Aufdenberg 2006; Peterson 2006, `2006Natur.440..896P`) 가 그 작은 sin i 가 작은 v_eq 가 아니라 작은 i 임을 밝혔습니다. Aufdenberg/Peterson 은 ω/ω_crit ≈ 0.91 에서 v_eq ≈ 274 km/s 를 추론했으나, 이후 더 높은 해상도의 Monnier 2012 CHARA/MIRC 영상이 이를 ω/ω_crit = 0.774 (v_eq ≈ 195 km/s) 로 하향 개정하면서 중력 감광도 더 약하게 나타났습니다 — 여전히 밝은 별 중 가장 빠르게 회전하는 부류이지만, 처음 생각보다는 덜 극단적입니다.

cfg 는 Petit 외 2010 의 자전 주기 0.71 ± 0.03 d (≈ 17.0 h) 를 채택합니다. 이는 spectropolarimetric (ZDI) 자기장 회전 변조에서 측정되었고 Alina 2012 가 확인한 Phase 2 recommended 값입니다. (단순한 2π·R_eq/v_eq 추정은 옛 274 km/s v_eq 에서 ~12.5 h 를 주지만, Monnier 의 개정된 더 느린 자전 v_eq ≈ 195 km/s 와 ω/ω_crit = 0.774 는 더 긴 자기 주기와 일관됩니다.)

자전축은 전체 별에서 가장 잘 제약된 방향 매개변수입니다. i ≈ 6.2° ± 0.3° (Aufdenberg 2006), 즉 Kerbal 프레임에서 Vega 의 극이 거의 정확히 Sol 을 향합니다. NearStars 렌더러에서의 시각적 결과는, 지구/Kerbin 근처 어떤 시점에서든 플레이어는 Vega 의 뜨겁고 밝은 극을 내려다보고, 차가운 적도 띠는 edge-on 으로 어두운 rim 으로 보입니다. 이것이 cfg 가 묘사하는 기하 — tilt 를 발명할 필요 없고, 문헌이 직접 제공.

원반과 자전축의 obliquity 는 오차 내에서 정렬됩니다 (Sibthorpe 2010; Su 2013). 원반과 자전 spin 이 원래 원시 행성계 원반 각운동량 벡터를 공유하는 coeval-formation 시나리오와 일관됩니다. cfg 에는 세차나 secular axis drift 가 구현되지 않습니다.

## Visual styling

- **글로벌 외관 (궤도 뷰).** 작고 강렬한 백청색 별 원반 (정면 극, T ≈ 10150 K) 주변에 차가운 적도가 어두운 limb 띠를 형성하는 옅은 따뜻한 크림 후광. KSP 렌더링 거리에서 Vega 는 거의 점광원이며 중력 감광 기울기는 매우 가까운 fly-by 에서만 간신히 분해 가능 — 시각은 둘러싼 정면 잔해 원반이 압도.
- **표면 디테일.** 입상 구조 없음, 흑점 없음, faculae 없음. 지배적인 가시 특징은 ~1160 K 극-적도 온도 기울기 (Monnier 2012). 시야 중심 근처의 찬란한 `#cfe0ff` 가 적도 limb 근처의 `#e8eef8` 로 페이드 (Aufdenberg 2006 의 2250 K 가 함의했을 것보다 더 미묘한 기울기). 전환은 매끄럽고 (선명한 경계 없음) pole-on 관측자에게는 거의 축대칭.
- **극/적도 특징.** Petit 2010 의 옅은 ZDI 극 자기 spot — 현 cfg 에서는 미렌더링이지만 Open items 의 확장 후보.
- **대기 haze.** 없음. A형은 채층이 없고, limb 가 부드러운 haze 띠 없이 깨끗하게 잘림.
- **잔해 원반 시각 (간판 특징).** Vega 는 IRAS 원형 잔해 원반이고 cfg 는 이를 거리에서 시스템의 시각적 지배 요소로 묘사. 원반은 두 개의 구분된 성분을 가진 정면 luminous 구조로 렌더링됩니다. ~14 AU 의 내부 따뜻한 띠는 거의 중성인 반사율 `#fffefe` (vivid 팩 `#fffdfc`) 로, 큰 중성 입자가 A0V 청백색 별빛을 반사하는 옅고 좁은 환형, 궤도 뷰 zoom 에서는 본질적으로 비가시이고 플레이어가 내부 시스템에 접근할 때 보이기 시작; 14–110 AU 의 cleared gap 은 미발견 행성소체-휘젓는 행성이 존재해야 할 위치를 시각적으로 식별하는 빈 환형 — cfg 가 Vega 의 "잃어버린 행성" 을 가장 강력하게 암시; 110–200 AU 의 외부 차가운 띠는 주된 시각 요소, 같은 거의 중성인 반사율 `#fffefe` (광학 색 미측정. A0V 별이 청백색을 공급), opacity 0.06, Sibthorpe 2010 morphology 따라 외부보다 내부 가장자리가 더 선명한 정면 밝은 ring — IRAS 가 발견한 구조이자 cfg 의 "당신은 Vega 에 있다" 단서.
- **별이 하늘에서 보이는 모습 (1 AU 의 가상 내부 행성에서).** 각 지름 ≈ 2 · R_eq / a · (180·60/π) ≈ 2 · 2.726 · 696000 / 1.496×10⁸ · (60·180/π) ≈ 0.087° (~5.2 arcmin) — 지구에서 본 태양의 ~16% 각 크기이지만 단위 면적당 ~7 배 밝음 (Teff 비율)^4. 조명 색온도 ~9360 K 는 약간 푸른 daylight 로 렌더링 — sunlight 가 태양 참조 대비 눈에 띄게 더 푸른 톤.
- **가상 내부 행성에서 본 원반.** 110–200 AU 의 외부 띠가 정면 ring 으로 하늘에서 ~30° 에서 ~90° 까지 차지 — NearStars 에서 가장 시각적으로 두드러진 특징 중 하나인 striking 한 야간 "Vega ring". Pole-on 기하 덕에 ring 이 edge-on streak 가 아니라 진짜 ring (완전 환형) 으로 보입니다.
- **자매 행성이 하늘에서.** 확정 없음. cfg 에 Vega 의 행성 body 없음. Su 2013 의 gap-clearer 행성이 미래 cfg variant 에 추가되면 내부 시스템 점광원으로 등장할 예정.

## Canonical alternatives

**연령 — 회전 고려 vs 비회전 isochrone.** cfg 는 회전을 고려한 Geneva 트랙에서 나온 Monnier 2012 의 연령 0.7 (+0.15/−0.075) Gyr 를 채택합니다. 문서화된 대안은 비회전 모델 isochrone 에서 나온 Yoon 2010 의 0.455 ± 0.013 Gyr 입니다. Monnier 가 빠른 자전을 명시적으로 다루면서 연령이 상당히 더 오래된 쪽으로 밀렸습니다. 두 값 모두 고전적인 ~350 Myr 추정을 대체합니다.

**자전 / 중력 감광 — Monnier vs Aufdenberg/Peterson.** cfg 는 Monnier 2012 의 개정된 ω/ω_crit = 0.774 (v_eq ≈ 195 km/s) 와 더 약한 1160 K 극-적도 기울기 (T_pole 10070, T_eq 8910) 를 사용합니다. 이전의 Aufdenberg 2006 / Peterson 2006 fit 은 더 빠른 ω ≈ 0.91 (v_eq 274 km/s) 과 더 강한 2250 K 기울기 (10150/7900) 를 주었습니다. Monnier 의 더 높은 해상도 CHARA/MIRC 영상이 현대 개정값이자 cfg 기본값입니다. 특히 적도 Teff 는 중력 감광 모델 전반에 걸쳐 7557 K (Peterson) 에서 8910 K (Monnier) 까지 분포합니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Aumann H. H. 외 1984** — *Discovery of a Shell Around Alpha Lyrae*, ApJ 278, L23 (`1984ApJ...278L..23A`). "Vega 현상" 을 명명한 IRAS 발견 논문. 60 + 100 μm 초과. 최초로 식별된 잔해 원반.
- **Aufdenberg J. P. 외 2006** — *First results from the CHARA Array. VII. Long-baseline interferometric measurements of Vega consistent with a pole-on, rapidly rotating star*, ApJ 645, 664 (`2006ApJ...645..664A`, arXiv:astro-ph/0603327). CHARA H 밴드 간섭계. v_eq = 274 km/s, i = 5° ± 2°, T_pole = 10150 K, T_eq = 7900 K, ω/ω_crit = 0.91. Vega 의 현대적 그림을 정의.
- **Peterson D. M. 외 2006** — *Vega is a rapidly rotating star*, Nature 440, 896 (`2006Natur.440..896P`). 독립적 NPOI 간섭계 확인. Aufdenberg 와 동일 결론.
- **Monnier J. D. 외 2012** — *Resolving Vega and the Inclination Controversy with CHARA/MIRC*, ApJ 761, L3 (`2012ApJ...761L...3M`, arXiv:1211.6055). **Phase 2 anchor.** 더 높은 해상도 CHARA/MIRC 영상. R_eq 2.726 ± 0.006 / R_pol 2.418 R☉, 표면 평균 Teff 9360 ± 90 (T_pole 10070 / T_eq 8910), L_bol 47.2 ± 2.0, 질량 2.15, 연령 0.7 (+0.15/−0.075) Gyr, ω/ω_crit 0.774, β 0.231. 이전 작업보다 더 약한 중력 감광과 더 느린 자전을 발견.
- **Yoon J. 외 2010** — *A New View of Vega's Composition, Mass, and Age*, ApJ 708, 71 (`2010ApJ...708...71Y`). 회전 모델 isochrone. M 2.135, 연령 0.455 ± 0.013 Gyr (Monnier 의 회전 고려 0.7 Gyr 에 대한 documented-divergence 대안 — Canonical alternatives 참조), [M/H] = −0.5 (cfg metallicity 출처; Vega "metallicity problem" 을 λ Boo 표면 결핍으로 해소).
- **Pease D. O., Drake J. J. & Kashyap V. L. 2006** — *The Darkest Bright Star: Chandra X-Ray Observations of Vega*, ApJ 636, 426 (`2006ApJ...636..426P`). Vega 의 깊은 Chandra 비검출, L_X < 2 × 10²⁵ erg/s — "no coronal activity" 의 Phase 2 근거. Robrade 2011 의 X-ray 는 Vega 가 아니라 동반체.
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
- **Yoon 2010 (0.455 ± 0.013 Gyr) 과 Monnier 2012 (0.7 ± 0.075 Gyr) 의 연령 불일치.** cfg 는 Monnier 의 0.7 Gyr 표제값(회전 고려 Geneva 트랙)을 채택하고, Yoon 0.455 Gyr 는 canonical alternative 로 둡니다 — Decisions 행과 일관. Yoon 의 회전/비회전 성격은 이 리포트 안에서도 (Decisions 행 vs bibliography) 엇갈리므로 논문 대조로 reconcile 해야 합니다. 해결에는 Monnier 2012 §4 의 deep-read 와 Tetzlaff 2011 운동학 연령 cross-check 가 필요.
- **Hurt 2021 의 0.04 AU 0.6 일 후보.** 2026 년 이후 후속 관측이 이를 진짜 행성으로 확정하면 (현재 미확인, 별 활동일 가능성) 새 Decisions 항목 `circumstellar_planet_present: true` 가 필요하고 행성 body cfg 가 추가되어야 함.
- **Su 2013 의 14–110 AU gap-clearer 행성.** 현재는 원반 morphology 에서만 유도. 미래 JWST-NIRCam 또는 extreme-AO 직접 영상 확인이 추론을 확정된 행성 body 로 전환하면 cfg 추가 트리거.
- **보수적 opacity 원반 variant.** 현 cfg 는 `disk_opacity` = 0.06 (interesting-first tie-break) 사용. 관측 일치 값은 τ ~ 10⁻⁴ (본질적으로 비가시). 물리적으로 충실한 opacity 를 가진 "realistic" cfg variant 를 플레이어 선택 옵션으로 작성해야 함.
- **Petit 2010 의 극 자기 spot.** 현재 미렌더링. 미래 cfg variant 가 ZDI 구조에 맞춰 가까운 fly-by 뷰에 극에 옅은 푸른 spot 을 추가할 수 있음.
- **원반 dust 크기 + 색 합성 — 완료 (2026-05-30).** 팔레트 관행 tint 를 Mie 반사율 합성 (`scripts/phase3/disk_color_mie.py`, 분산 n,k) 으로 교체. 큰 규산염 입자 (a_min ~11 µm) 가 거의 중성 반사율 `#fffefe` (B/I 0.91) 을 가지므로, 두 벨트 모두 인게임에서 A0V 청백색 별빛을 반사. vivid 팩은 `#fffdfc`. 측정된 두 원반 색 (AU Mic 의 파란색 B/I 1.74, Fomalhaut 의 회색) 으로 검증.
- **Cycle phase / 에포크 동기화.** Vega 는 (복사 외피라) 관측된 활동 cycle 이 없어 α Cen A 와 달리 에포크 동기화가 불필요. 다만 Petit 2010 자기 기하가 천천히 회전하는 극 특징으로 구현되면 에포크 참조가 필요해질 것.

## Related

- [alpha-centauri-a](alpha-centauri-a.md) — 다른 시나리오 archetype. 조용한 G2V 태양 유사 vs Vega 의 젊은 빠른 자전체 A0V archetype. stellar Phase 3 의 canonical 구조 템플릿으로 참조.
- [methodology](../reference/methodology.md) — Decisions table 의 스키마 출처.
- [data-sources](../reference/data-sources.md) — `db/systems/vega.json` 의 SIMBAD 유래 천체측정 + 분광 필드의 provenance.
- [mod-reference](../reference/mod-reference.md) — Kopernicus + Firefly + Scatterer cfg 필드 맵. circumstellar disk 필드는 star body 에 attach 되는 Kopernicus Ring 컴포넌트로 매핑.
