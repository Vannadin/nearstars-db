<!-- Fomalhaut Phase 3 합성. cfg-ready 결정과 근거 -->
# Fomalhaut — Phase 3 Synthesis

Fomalhaut (α Piscis Austrini, HD 216956, HIP 113368, HR 8728) 는
남쪽 하늘 물고기자리(Piscis Austrinus)에서 가장 밝은 별이자, 태양과
가까운 A 형 주계열성 중 손꼽히는 별입니다. 분광형은 A4V 로,
Gray & Garrison 1989 의 MK 시스템 개정에서 A3V/A4V 경계에 놓이며,
Hipparcos / Gaia DR3 시차 129.81 mas 가 거리 **7.704 pc ≈ 25.13 ly**
를 줍니다. 기본 파라미터는 Mamajek 2012 에 정박돼 있는데, 이
논문은 Absil 2009 의 excess 보정 VLTI/VINCI 각지름 (θ_LD =
2.223 mas) 과 Davis 2005 의 볼로메트릭 플럭스를 결합해
R = 1.842 ± 0.019 R☉, Teff = 8590 K, L = 16.63 ± 0.48 L☉, 그리고
Y² 진화 모델 질량 M = 1.92 ± 0.02 M☉ 를 유도합니다. 이 값들 덕분에
Fomalhaut 는 볼로메트릭 기준 태양보다 약 17 배, 가시광 밴드에서는
약 24 배 밝게 빛납니다. ~440 Myr 의 나이도 같은 논문에서 나옵니다
(Fomalhaut A 의 등시선 + 동반성 TW PsA 의 자이로/Li/X 선 나이).

Fomalhaut 는 **계층적 광폭 삼중계의 주성**입니다. K4V 별 TW Piscis
Austrini (HD 216803, V = 6.48) 는 Fomalhaut 와 공통 고유운동을
공유하며 투영 분리 ~0.91 ly (≈ 5.7 × 10⁴ AU) 에 위치하고, 세 번째
성분인 M4V 플레어 별 LP 876-10 (Gaia DR3 6638942675812506240) 은
Mamajek 2013 이 투영 분리 ~5.7 ly (≈ 1.6 × 10⁵ AU) 에서 식별했습니다.
세 별 모두 운동학적/등시선상 나이 **440 ± 40 Myr** (Mamajek 2012)
를 공유하며, 이 시스템은 **Castor 운동성단**에 속합니다. NearStars
DB 는 현재 Fomalhaut A 만 추적하며, TW PsA 와 LP 876-10 은 향후
후보 엔트리로 Open items 에 기록돼 있습니다. 두 별이 추가되면
Fomalhaut 계 어느 행성에서든 게임 내 하늘에서 고정된 적위에 떠
있는 희미한 맨눈급 "제2의 태양" 두 점을 볼 수 있게 됩니다.

Fomalhaut 가 학술적으로 유명한 까닭은 **분해된 별주위 잔해 원반**
때문입니다. Kalas et al. 2005 의 HST/ACS 코로나그래프 영상이
장반경 a ≈ 140 AU, 이심률 e ≈ 0.11 의 좁고 편심한 고리를 처음 찍어
냈는데, 안쪽 가장자리가 날카로워 보이지 않는 양치기 천체가 중력
적으로 조각하고 있음을 시사했습니다. ALMA 밀리미터 영상 (Boley
2012; White 2017) 은 기하를 정밀화해 이심률, 좁은 폭 (Δa/a ≈ 0.13),
경사 i ≈ 65–67° 를 확정했습니다. Gáspár et al. 2023 의 JWST/MIRI
영상은 ~10 AU 의 **안쪽 소행성대 analog** 와 ~83–104 AU 의 (넓은 안쪽 디스크와 ~78 AU gap 으로 분리되는) **중간
벨트** 를 분해해, 태양계 소행성대 + 카이퍼대 + scattered disk 와
유사하지만 온도와 질량 모두 크게 부풀린 3 벨트 구조를 완성했습니다.
Kalas et al. 2008 이 HST 가시광 영상에서 보고한 그 유명한
"**Fomalhaut b**" 점광원은 이후 행성소체 충돌에서 발생한 팽창
먼지 구름으로 재해석됐습니다 (Gáspár & Rieke 2020; JWST 2023 의
미검출과도 일관). 이 합성은 현재 컨센서스를 따르며, Fomalhaut b
를 **별주위 행성으로 포함하지 않습니다**.

**NearStars 시나리오 선택. 다중 벨트 편심 잔해 원반계로 둘러싸인
젊고 뜨거운 고광도 A4V 별로, 광폭 궤도의 희미한 맨눈급 동반성
두 개가 어느 행성 밤하늘에든 시각적 흥미를 더하는 모습으로
렌더링합니다.** 항성 레이어는 Mamajek 2012 (Absil 2009 의 excess
보정 간섭계) 에 다시 정박했으며, 보정 안 한 Davis 2005 대비
반지름/Teff divergence 를 문서화했습니다. cfg 픽은 canonical
파라미터 셋을 따르며, tie-break 픽은 시각 hex 색 (A4V SED 백청색)
과 원반 RGB 색조 (먼지 온도 → 광학 색) 에 한정됩니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | A4V | high | Gray & Garrison 1989 — MK 표준. Mamajek 2012 가 A3V/A4V 경계로 채택 |
| `mass_msun` | 1.92 ± 0.02 | high | Mamajek 2012 — 간섭계 R 에 정박된 Y² 진화 트랙 등시선 fit |
| `radius_rsun` | 1.842 ± 0.019 | high | Mamajek 2012 — Absil et al. 2009 의 excess 보정 θ_LD = 2.223 ± 0.022 mas (VLTI/VINCI) + Davis 2005 f_bol 에 van Belle 1999 관계 적용 (Phase 2 recommended. 원래 θ_LD 는 Di Folco 2004) |
| `teff_k` | 8590 | high | Mamajek 2012 — 간섭계 (Absil θ_LD + Davis f_bol. Phase 2 recommended. SIMBAD 8689 을 대체). Davis 2005 의 보정 안 한 8819 K 는 documented divergence |
| `luminosity_lsun` | 16.63 ± 0.48 | high | Mamajek 2012 — 볼로메트릭 플럭스 (Davis f_bol + 개정 시차. Phase 2 recommended) |
| `metallicity_fe_h_dex` | −0.03 | medium | Dunkin et al. 1997 — 고분해 분광 (Phase 2 recommended. 거의 태양값). A 형 별 분광 [Fe/H] 는 산포가 큼 (Erspamer 2003 +0.43). Mamajek 2012 는 protosolar Z = 0.017 을 가정 |
| `age_gyr` | 0.44 ± 0.04 | high | Mamajek 2012 — Fomalhaut A 의 등시선 나이 (450 ± 40) 를 동반성 TW PsA 의 자이로/Li/X 선 나이와 조정. 이전 200 Myr 추정치를 대체 |
| `rotation_period_days` | 0.97 | low | DERIVED ONLY — 측정된 주기는 없음. v sin i ≈ 93 km/s (Royer 2007) + R 1.842 + 가정 i ≈ 65° (원반 경사) 에서 유도. v sin i 가 유일한 직접 자전 제약 |
| `limb_darkening_alpha_h` | 0.211 ± 0.020 | high | Davis et al. 2005 — SUSI 광학 간섭계. A 형 별 limb darkening 이 태양형 G 형보다 살짝 강함 |
| `visual_surface_tint_hex_primary` | `#cfe0ff` (시원한 청백, A 형 별) | medium | Tie-break. 8590 K A4 V 흑체 + 볼로메트릭 보정. Vega 의 살짝 더 푸른 A0V 색조와 시각적으로 구분 가능 (hex 유지. 8689→8590 K 변화는 인지 임계 아래) |
| `stellar_color_temp_k` | 8590 | high | = Teff (Mamajek 2012) |
| `stellar_oblateness_ratio` | 1.021 | low | Absil 2009 — 겉보기 적도/극 지름 비 (약함. Fomalhaut 은 극단이 아닌 중간 정도의 A 형 자전체) |
| `visual_companion_event_tw_psa_apparent_diameter_arcmin` | 0.00006 (점광원, Fomalhaut 계 어느 행성에서든 V ≈ 6.5) | medium | 유도. 2 R(K4V) / 0.91 ly ≈ 0.004 arcsec ≈ 점광원. 디스크가 아닌 희미한 주황색 별로 보임 |
| `visual_companion_event_lp_876_10_apparent_diameter_arcmin` | 0.00001 (점광원, Fomalhaut 계 어느 행성에서든 V ≈ 11) | medium | 유도. 5.7 ly 의 M4V 는 맨눈 한계 아래지만 게임 내 망원경 뷰에서는 손쉽게 보임 |
| `disk_present` | true | high | Kalas et al. 2005 의 HST/ACS 분해 코로나그래프 영상 |
| `disk_belts` | warm, intermediate, cold | high | Gáspár 외 2023 JWST/MIRI 가 3 벨트 구조를 분해. 안쪽 warm + intermediate + 고전적 편심 cold 주 고리 (Kalas 2005 / Boley 2012 / White 2017) |
| `disk_warm_inner_radius_au` | 10 | high | Gáspár 외 2023 (`2023NatAs...7..790G`) JWST/MIRI — 안쪽 warm 벨트 안쪽 가장자리 |
| `disk_warm_outer_radius_au` | 78 | high | Gáspár 외 2023 — 넓은 안쪽/warm 디스크가 intermediate 벨트와 분리되는 ~78 AU gap 까지 뻗음 |
| `disk_warm_tint_rgb_hex` | `#ffffff` (중성. vivid `#fefeff`) | low | 광학 색 측정값 없음 (열복사/간섭계 자료만). Mie 반사율 합성. 탄소질 입자는 어둡지만 입자가 커서 중성 반사율 (B/I 1.00). 렌더러가 A4 V 청백색 별빛을 위에 입히면 게임 내에서 옅은 청백색. vivid 팩. `#fefeff` |
| `disk_warm_opacity` | 0.30 | low | Tie-break. 실제로는 광학적으로 얇음. 가시성 위해 boost |
| `disk_intermediate_inner_radius_au` | 83 | high | Gáspár 외 2023 JWST/MIRI — intermediate 벨트 안쪽 긴반지름 (e ≈ 0.31) |
| `disk_intermediate_outer_radius_au` | 104 | high | Gáspár 외 2023 — intermediate 벨트 바깥쪽 긴반지름 (e ≈ 0.265) |
| `disk_intermediate_tint_rgb_hex` | `#fff9f6` (거의 중성. vivid `#ffece4`) | low | 광학 색 측정값 없음 (중적외선만). Mie 반사율 합성. 규산염 입자가 광학 파장 대비 커서 거의 중성 반사율 (B/I 0.76). 렌더러가 A4 V 별빛을 위에 입힘. vivid 팩. `#ffece4` |
| `disk_intermediate_opacity` | 0.25 | low | Tie-break. 희미한 intermediate 먼지, 가시성 위해 boost |
| `disk_cold_inner_radius_au` | 133 | high | Boley 2012 / White 2017 ALMA — 편심 궤도 보정 후 주 고리 안쪽 가장자리 |
| `disk_cold_outer_radius_au` | 158 | high | Boley 2012 / White 2017 ALMA — 주 고리 바깥쪽 가장자리 |
| `disk_cold_dust_temperature_k` | 65 | high | Stapelfeldt 2004 Spitzer. Acke 2012 Herschel 의 차가운 성분 SED fit |
| `disk_cold_tint_rgb_hex` | `#d6d8da` (거의 중성 회백색) | medium | 실측. Kalas 2005 HST/ACS + Acke 2012 — 희미하고 저알베도(~0.05–0.1), 큰 입자 → A3V 백색 별에 가까운 거의 중성/회색 산란광 ("파란 Fomalhaut" 은 행성후보지 고리가 아님) |
| `disk_cold_opacity` | 0.35 | low | Tie-break. 실제로는 광학적으로 얇음 (τ ≈ 10⁻⁴). 가시성 위해 boost |
| `disk_cold_aspect_ratio` | 0.0175 ± 0.004 (H ≈ 2.4 AU, r ≈ 140 AU) | medium | Boley 2012 ALMA — cold 주 고리의 수직 구조. midplane 에서 1.0° ± 0.25 opening angle (지수 분포) 이므로 h = H/r = tan θ ≈ 0.0175. 이 디스크의 유일한 수직 구조 측정입니다 (MacGregor 2017 은 2D 모델로 이것을 인용만 함). 평면 Kopernicus Ring 은 소비하지 않으며, 완전성과 향후 볼류메트릭/Parallax 렌더링용으로 기록합니다 |
| `disk_morphology` | 3 벨트 편심 구조. warm 내부 디스크 (~10–78 AU) + intermediate 벨트 (~83–104 AU), ~78 AU gap 으로 분리, + 고전적 편심 cold 주 고리 (133–158 AU, 날카로운 안쪽 가장자리) | high | Kalas 2005 + Boley 2012 + Gáspár 2023 JWST/MIRI — 완전한 다중 벨트 구조 |
| `disk_resolved_imaging` | true | high | HST/ACS (Kalas 2005), ALMA (Boley 2012, White 2017), JWST/MIRI (Gáspár 2023) |
| `disk_imaging_observatory` | HST-ACS + ALMA + JWST-MIRI | high | 위와 동일 |
| `disk_imaging_inclination_deg` | 65.6 ± 0.4 (cold 고리); ~47.8 (내부 디스크, Gáspár 2023 — cold 고리와 크게 어긋남) | high | cold 고리는 Le Bouquin 2009 / Boley 2012 ALMA. 내부 디스크는 Gáspár 2023 (i ≈ 47.8° vs 외곽 고리 64.4° — JWST 핵심 misalignment 결과) |
| `disk_mass_mearth` | 0.015 (cold 주 고리, mm-cm 입자) ~ 4–10 (행성소체 reservoir) | medium | Holland 2017 SCUBA-2 + ALMA. 하한은 영상 입자, 상한은 충돌 cascade 모델링 |
| `disk_planetesimal_belt_inferred` | true | high | cold 고리의 날카로운 안쪽 가장자리 (Kalas 2005) 는 양치기 천체를 요구. 충돌 cascade 보충에 부모 행성소체 종족 필요 (Wyatt 2008, Boley 2012 적용) |

## Surface synthesis

Fomalhaut 의 광구는 Teff = 8590 K 로 A 형 주계열의 한가운데에
자리잡으며, 태양보다 약 2800 K 뜨겁고 canonical A0V 표준성 Vega
보다는 약 700 K 차갑습니다. 이 온도에서 연속체 불투명도는 수소의
Balmer / Paschen jump 가 지배하며 볼로메트릭 SED 의 정점은 ~334 nm
로 UV 영역 깊숙이 들어갑니다. 따라서 가시 디스크는 강하게 청백색
으로 빛나며, H I Balmer 흡수선이 분광형을 정의하는 깊고 넓은
Hα/Hβ/Hγ 피처를 만듭니다. 색채권 Ca II H&K 방출 핵은 없습니다.
A 형 별에는 자기적으로 가열되는 색채권을 유지하는 데 필요한 깊은
대류 envelope 가 없기 때문에, 태양형 활동도 합성을 정박하는 log
R'HK 지표는 Fomalhaut 에 대해 **정의되지 않으며** Decisions
테이블에서 생략합니다.

VLTI/VINCI 의 간섭계 반지름 R = 1.842 R☉ (Di Folco 2004) 는 limb-
darkened uniform-disk 각지름 θ_LD = 2.223 ± 0.022 mas 에 정박돼
있으며 — 1% 정밀도 측정으로, NearStars 카탈로그 안에서는 α Cen A
와 Vega 다음 정밀도입니다. A4V 대기의 limb-darkening 법칙은 태양
보다 더 가파릅니다. Davis 2005 의 SUSI 간섭계가 가시광에서 power-
law 지수 α ≈ 0.21 을 주는데, 이는 G 형 왜성 값 ~0.14 보다 약 50%
큰 값입니다. 이 더 가파른 limb darkening 은 수소 이온화 영역의
강한 온도 구배에 기인하며, 게임 내에서 Fomalhaut 에 가까이 접근
할 때 태양형 별보다 "limb-dimmed" 효과가 더 강한 디스크를 보게
됩니다. 중심 밝기가 limb 밝기보다 30–40% 높으며, 태양형의
15–20% 대비를 넘어섭니다.

Granulation 은 태양형 별보다 훨씬 미세합니다. 대류 영역은 얕고
(상부 ~0.05 R★ 에 불과) granule 스케일도 작아 (태양의 ~1000 km
대신 ~50 km), 행성 시점에서 분해 가능한 셀이 없는 매끄러운 광구가
형성됩니다. 살짝 sub-solar 한 금속도 ([Fe/H] = −0.03, Dunkin 1997. A 형 별
분광 [Fe/H] 는 산포가 커서 Mamajek 2012 는 protosolar Z = 0.017 을
가정) 는 SED reddening 에 무시할 만한 영향을 줍니다.
cfg 가 채택한 시각 색조 `#cfe0ff` 는 A4V 흑체 정점을 Vega 의 A0V
`#bdd5ff` 기준선보다 살짝 적색 쪽으로 옮긴 값을 인코딩해, 두 A 형
별을 NearStars 카탈로그 안에서 시각적으로 구분되게 합니다.

## Atmosphere synthesis

A4V 별에는 **자기적 의미에서 차가운 별과 유사한 chromosphere–
transition-region–corona 구조가 없습니다**. 바깥 대기는 광구–
항성풍 경계까지 줄곧 복사 평형이며, 뜨거운 코로나를 유지할 음향
가열이나 자기 가열 메커니즘이 없습니다. 그래서 Fomalhaut 의 X 선
검출은 매우 약합니다. ROSAT 상한 (Schröder & Schmitt 2007) 은
log L_X < 27.5 (erg/s, 0.1–2.4 keV) 를 주며, XMM-Newton 의 경계선
검출은 Fomalhaut A 자체가 아니라 **작은 분리 거리의 자기 활동성
후기형 동반성** 에 기인할 가능성이 큽니다. 코로나 X 선 사이클은
예상되지 않으며 관측되지도 않습니다.

UV/FUV 플럭스는 본질적으로 높습니다. 8590 K 광구의 Wien 꼬리가
200 nm 아래에 상당한 에너지를 두기 때문이며, 이는 A 형 별 주위
안쪽 행성 어디에서든 대기 침식의 지배적인 구동력입니다. 다만
볼로메트릭 대비 XUV/EUV 플럭스는 낮습니다 (색채권 Lyα 방출 핵이
없음). 따라서 거주가능영역 행성 (Kopparapu 2013 에 따르면
Fomalhaut 의 HZ 는 ~3.5–6 AU 에 위치) 의 XUV 구동 침식은 색채권
선 방출이 아니라 광구 UV 연속체로 제한됩니다. 플레어도 없습니다.
대류 envelope 의 부재는 M 형/K 형 왜성의 플레어를 일으키는 다이나모
메커니즘을 원천 차단합니다.

440 Myr 의 나이는 Fomalhaut 가 아직 주계열 초기에 머문다는 뜻
입니다 (A4V 진화 수명은 ~1.0 Gyr. Mamajek 2012 는 MS 수명의 ~44%
지점에 위치시킵니다). 아직 준거성 가지로 진화하지 않았지만, 너무
뜨거워 1 AU 의 행성은 ~17 배 태양 일사량을 받게 됩니다 — 익혀지는
/ 폭주 온실 효과 경계 한참 안쪽입니다. cfg 는 활동도에 대해 코로나
없음, 색채권 방출 없음, 플레어 없음의 canonical A 형 별 처방을
채택합니다.

## Rotation & spin synthesis

Fomalhaut 는 **빠른 자전체** 입니다. 자기 제동이 별을 늦추기에는
너무 뜨거운 A 형 별의 전형적인 모습입니다. Royer 2007 은 Mg II
4481 Å 피처의 line broadening 에서 v sin i = 93 ± 3 km/s 를
측정합니다. 잔해 원반 궤도 평면에서 추정한 경사 i ≈ 65.6° (Le
Bouquin 2009 — 별과 원반의 spin-orbit 정렬을 가정하며, Greaves
2014 의 젊은 잔해 원반 A 형 별 서베이에서 모두 관측적으로 일관)
와 결합하면 deprojected 적도 속도는 v_eq ≈ 102 km/s 입니다.

대응하는 자전 주기는 P_rot = 2πR/v_eq ≈ **0.97 일** 입니다
(DERIVED ONLY — 측정된 주기는 없음. v sin i ≈ 93 km/s + R + 가정
i ≈ 65° 에서 유도하며, v sin i 가 유일한 직접 자전 제약). 태양보다
약 25 배 빠릅니다. 임계 분열 속도 ~390 km/s 의 약 25% 에 해당하는
수준이라 별이 유의미하게 oblate 하지는 않습니다. 다만 빠른 자전은
측정 가능한 **중력 어두워짐(gravity-darkening) 위도 온도 구배**
를 만듭니다. Monnier 2010 의 CHARA/MIRC 간섭계가 비슷한 빠른
자전체 A 형 별 (Altair, Vega) 에서 ΔT(pole−equator) ≈ 500–1500 K
를 측정했습니다. Fomalhaut 자체에 분해된 중력 어두워짐 지도는
존재하지 않지만, von Zeipel 스케일링은 ΔT ≈ 300 K (극이 적도보다
뜨거움) 를 예측합니다 — 고경사 관측자에게는 cfg 디스크 셰이더에서
미묘한 "극 방향 밝아짐"으로 관측 가능한 효과입니다.

잔해 원반과의 spin-orbit 정렬은 자전축에 대한 가장 강력한 제약
입니다. Le Bouquin 2009 의 간섭계는 Fomalhaut 의 자전축이 원반
법선과 ~3° 안에서 공-정렬돼 있음을 확립했습니다. NearStars 는 이
공-정렬 배치를 채택해, 별의 자전 적도와 잔해 고리 궤도 평면이
공통 기준 좌표계를 공유하도록 합니다 — 원반 평면 위쪽에 자리한
게임 내 관측자에게는 작지만 진짜 같은 디테일입니다.

## Canonical alternatives

**반지름 / Teff — excess 보정 간섭계 vs 보정 안 한 간섭계.**
cfg 는 Mamajek 2012 값 (R 1.842 R☉, Teff 8590 K) 을 채택하는데,
이는 분해된 별주위 K 밴드 excess 를 빼낸 Absil et al. 2009 의
각지름 (θ_LD = 2.223 mas) 에서 유도한 값입니다. 문서화된 대안은
Davis et al. 2005 로, 그쪽 SUSI fit 은 excess 를 제거하지 않아 더
작은 R (1.744 R☉) 과 더 뜨거운 Teff (8819 K) 를 줍니다. 둘 다
자기일관적이지만 excess 보정한 Absil/Mamajek 해가 원칙에 맞는
기본값이며, L (~16.5–16.6 L☉) 은 같은 볼로메트릭 플럭스에서
나오므로 양쪽이 일치합니다.

**금속도.** A 형 별 분광 [Fe/H] 는 신뢰도가 낮습니다. cfg 는 거의
태양값인 Dunkin 1997 의 −0.03 을 기록하지만, 측정값은 넓게 산포
하므로 (Erspamer 2003 +0.43) Mamajek 2012 는 등시선용으로 그냥
protosolar Z = 0.017 을 가정합니다. [Fe/H] 는 ≈ 태양값으로 보면
됩니다.

## Visual styling

NearStars 렌더러에서 Fomalhaut 는 `#cfe0ff` 로 색을 입힌 **시원한
청백색 A4V 디스크** 로 묘사됩니다 — 카탈로그의 G/K 형 별 (따뜻한
크림에서 주황까지) 보다 뚜렷이 푸르지만, Vega 의 거의-A0V `#bdd5ff`
기준선보다는 살짝 따뜻한 색입니다. 지구에서 본 V = 1.16 으로
Fomalhaut 는 밤하늘 18 번째로 밝은 별이자, 남반구 가을 사분면에서
가장 밝은 별입니다.

거주가능영역 안쪽 가장자리 (Kopparapu 2013 기준 ~3.5 AU) 의 후보
행성에서 보면 별이 채우는 각지름은 2R★/a × (180·60/π) ≈ 0.06° —
지구에서 본 태양 각지름의 약 1/8 입니다. 각 크기는 작지만 표면
밝기는 T⁴ 스케일링 (Teff = 8590 K vs 5772 K → 단위 입체각당 5.0
배) 때문에 태양보다 훨씬 높아서, HZ 에서 받는 볼로메트릭 플럭스는
1 AU 의 solar constant 의 약 5 배입니다. 가시광 밴드 조명은 청색
쪽에 더 강하게 가중되어, HZ 행성의 한낮 하늘 스펙트럼은 태양 아래
지구가 가질 모습보다 눈에 띄게 차갑게 보입니다.

이 시스템의 시각적 중심은 **잔해 고리** 입니다. 안쪽 행성계의 어느
행성에서 보든 133–158 AU 의 주 고리는 하늘을 가로지르는 ~25–30
arcminute 의 얇은 타원 띠를 형성합니다 (이심률 e ≈ 0.11 이 별과
고리 중심 사이에 가시 오프셋을 만듭니다 — 14 AU 오프셋으로,
어떤 광시야 뷰에서도 손쉽게 보임). cold 주 고리는 자체 Kopernicus
`Ring` 으로 `disk_cold_tint_rgb_hex = #d6d8da` — ~65 K 먼지가 A 형
별 빛을 재산란하는, 거의 중성 회백색 (실측: Kalas 2005 저알베도 큰입자
산란) 으로 렌더링되며, 안쪽 warm (`#dedede`) 과 intermediate
(`#d8d8da`) 벨트는 같은 `Rings {}` 블록
안의 별도 Ring 으로 렌더됩니다. `disk_cold_opacity = 0.35` 는 물리
광학적 깊이 (~10⁻⁴) 에서 끌어올린 tie-break boost 로, 고리가 수치적
잡티가 아니라 게임 내에서 실제로 보이는 대상으로 읽히도록 보정한 값입니다.

**83–104 AU 의 중간 벨트** (Gáspár 2023 JWST) 는 동일한 먼지 색조에
opacity 를 절반으로 낮춘 더 희미한 보조 고리로 렌더링되어, Saturn
같은 이중 고리 구조를 만들지만 스케일은 비교가 안 될 정도로
거대합니다. **~10 AU 의 안쪽 따뜻한 소행성대 analog** (역시 Gáspár
2023) 는 대부분의 카메라 거리에서는 고리로 렌더링하기에 너무
작아서, cfg 안에서 저밀도 입자 필드로 표현합니다 — 별과 충분히
가까워 그 산란광이 안쪽 행성계의 황도광에 기여합니다.

**두 별 동반성**은 게임 내 하늘에서 고정된 점광원으로 나타납니다.
TW Piscis Austrini 는 0.91 ly 투영 분리에 위치하며 Fomalhaut 계
어느 행성에서든 겉보기 등급 V ≈ 6.5 입니다 — 맨눈 가시성의
경계선이지만 어떤 별 필드 뷰에서든 뚜렷한 **주황색 K 왜성 점**
으로 쉽게 보입니다. LP 876-10 은 5.7 ly 에 있어 더 어둡고 (V ≈ 11)
맨눈 가시성 아래지만 망원경 뷰에서는 희미한 **붉은 M 왜성** 점
으로 보입니다. 어느 쪽도 분해된 디스크를 보이지 않으며, 둘 다 cfg
에서 `visual_companion_event_*` 점광원으로 플래그돼 있어 렌더러가
디스크를 그리려 시도하지 않고 정확한 위치에 점만 찍습니다.

Fomalhaut A 와 광폭 분리 동반성들 사이에는 식 / 엄폐 이벤트가
없습니다. ~0.91 ly 와 ~5.7 ly 의 투영 분리는 인간 시간 척도에서
어떠한 게임 내 정렬 현상도 만들 수 없을 만큼 너무 큽니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Mamajek E. E. 2012** — *On the age and binarity of Fomalhaut*,
  ApJ 754, L20 (`2012ApJ...754L..20M`, arXiv:1206.6353). **항성
  레이어 전체의 Phase 2 anchor.** Absil 2009 의 excess 보정 θ_LD +
  Davis 2005 f_bol 에서 R 1.842 ± 0.019 R☉, Teff 8590 ± 73 K,
  L 16.63 ± 0.48 L☉ 를 재유도. 질량 1.92 ± 0.02 M☉ (Y² 트랙).
  나이 440 ± 40 Myr (A 의 등시선 + 동반성 TW PsA 의 자이로/Li/X 선).
- **Absil O. et al. 2009** — *A near-infrared interferometric survey of
  debris-disc stars II: Fomalhaut*, ApJ 704, 150 (`2009ApJ...704..150A`,
  arXiv:0908.3133). excess 보정 VLTI/VINCI θ_LD = 2.223 ± 0.022 mas
  (분해된 0.88% K 밴드 별주위 방출을 빼냄) — Mamajek 2012 가 R/Teff
  에 쓰는 각지름. 겉보기 oblateness 1.021.
- **Mamajek E. E. et al. 2013** — *Discovery of a Faint Companion to
  Alpha PsA Using MMT/AO 5 μm Imaging*, AJ 146, 154
  (`2013AJ....146..154M`, arXiv:1310.0764). LP 876-10 을 Fomalhaut
  계층적 삼중계의 M4V 세 번째 성분으로 5.7 ly 투영 분리에서 식별.
  공통 고유운동 + 등시선 나이 일치.
- **Di Folco E. et al. 2004** — *VLTI near-IR interferometric
  observations of Vega-like stars*, A&A 426, 601
  (`2004A&A...426..601D`, arXiv:astro-ph/0408390). 원래의 VLTI/VINCI
  K 밴드 각지름. Mamajek 2012 가 채택하는 Absil 2009 의 excess
  보정으로 정밀화됨.
- **Dunkin S. K. et al. 1997** — *High-resolution spectroscopy of
  Vega-like stars*, MNRAS 286, 604 (`1997MNRAS.286..604D`). Fomalhaut
  의 [Fe/H] = −0.03 — Phase 2 recommended (거의 태양값) 금속도. A 형
  별 [Fe/H] 측정은 산포가 큼.
- **Kalas P. et al. 2005** — *A planetary system as the origin of
  structure in Fomalhaut's dust belt*, Nature 435, 1067
  (`2005Natur.435.1067K`). HST/ACS 코로나그래프가 133 AU 의 좁고
  편심한 (e ≈ 0.11) 주 고리와 날카로운 안쪽 가장자리를 처음 분해
  — 보이지 않는 행성에 의한 중력적 조각으로 해석 (원조 "양치기"
  추론).
- **Kalas P. et al. 2008** — *Optical Images of an Exosolar Planet
  25 Light-Years from Earth*, Science 322, 1345
  (`2008Sci...322.1345K`). 원조 "Fomalhaut b" HST 검출 논문.
  **철회 맥락**. Gáspár & Rieke 2020 의 후속 재분석과 JWST 2023
  미검출 (Gáspár 2023) 이 이 광원을 묶인 행성이 아닌 행성소체
  충돌에서 발생한 일과성 팽창 먼지 구름으로 재해석. 이 합성은 현재
  컨센서스를 따름.
- **Gáspár A. & Rieke G. H. 2020** — *New HST data and modeling
  reveal a massive planetesimal collision around Fomalhaut*, PNAS
  117, 9712 (`2020PNAS..117.9712G`, arXiv:2004.08736). HST 아카이브
  재분석으로 "Fomalhaut b" 가 2004–2014 사이에 팽창하고 어두워
  졌음을 확인. 묶인 점광원이 아니라 ~200 km 행성소체 충돌에서
  나온 팽창 먼지 구름과 일관.
- **Gáspár A. et al. 2023** — *Spatially resolved imaging of the
  inner Fomalhaut disk using JWST/MIRI*, Nature Astronomy 7, 790
  (`2023NatAs...7..790G`, arXiv:2305.03789). 15.5 µm + 23 µm JWST/MIRI
  영상이 이전에 알려지지 않았던 **~83–104 AU 의 중간 벨트** 를
  (~78 AU gap 으로 안쪽 디스크와 분리. 안쪽 디스크 경사 ~47.8° vs 외곽 고리 64.4°)
  분해하고 **~10 AU 의 안쪽 따뜻한 소행성대 analog** 를 확인.
  Fomalhaut b 시점 위치에 점광원 없음, 먼지 구름 해석과 일관.
- **Boley A. C. et al. 2012** — *Constraining the planetary system
  of Fomalhaut using high-resolution ALMA observations*, ApJ 750,
  L21 (`2012ApJ...750L..21B`, arXiv:1204.0007). ALMA Cycle 0 의 주
  고리 영상. 이심률 e = 0.11 ± 0.01, 안쪽 가장자리 133 AU, 바깥쪽
  가장자리 158 AU, 폭 Δa/a ≈ 0.13. 양치기 행성 질량을 < 3 M_Jup
  으로 제약.
- **White J. A. et al. 2017** — *ALMA observations of Fomalhaut's
  outer dust ring*, ApJ 842, 80 (`2017ApJ...842...80W`,
  arXiv:1705.10670). 더 높은 분해능의 ALMA Cycle 4 follow-up. 좁은
  편심 고리를 재확인하고 경사를 65.6 ± 0.4° 로 정밀화. 원반 기하
  cfg 필드를 결정.
- **Le Bouquin J.-B. et al. 2009** — *Spin axis of α PsA from
  interferometry*, A&A 498, L41 (`2009A&A...498L..41L`,
  arXiv:0904.1688). VLTI/AMBER 의 별 oblateness + 자전축 방향 측정.
  잔해 원반과의 spin-orbit 정렬이 ~3° 안에서 성립함을 입증.
- **Davis J. et al. 2005** — *Limb-darkening determinations for
  Fomalhaut and α Cen A from SUSI*, MNRAS 356, 1362
  (`2005MNRAS.356.1362D`). 광학 간섭계 limb-darkening power-law
  α(V) ≈ 0.21 for Fomalhaut. `limb_darkening_alpha_h` 를 결정.

### Read (context / methodology, not directly decision-driving)

- **Royer F. et al. 2007** — *Rotational velocities of A-type stars*,
  A&A 463, 671 (`2007A&A...463..671R`, arXiv:astro-ph/0610785).
  Fomalhaut 에 대해 v sin i = 93 ± 3 km/s. 원반 경사와 결합해 자전
  주기 유도.
- **Acke B. et al. 2012** — *Herschel images of Fomalhaut: An
  extrasolar Kuiper Belt at the height of its dynamical activity*,
  A&A 540, A125 (`2012A&A...540A.125A`, arXiv:1204.5037). 차가운 주
  고리의 Herschel/PACS 원적외선 영상. SED fit 으로 T_dust ≈ 65 K.
  `disk_dust_temperature_k` 필드를 채움.
- **Holland W. S. et al. 2017** — *SONS: The JCMT legacy survey of
  debris discs at submillimetre wavelengths*, MNRAS 470, 3606
  (`2017MNRAS.470.3606H`, arXiv:1706.01218). SCUBA-2 서브밀리
  측광. mm-cm 입자에서 주 고리 먼지 질량 ~1.5 × 10⁻² M⊕.
- **Saffe C. et al. 2008** — *Spectroscopic metallicities of Vega-
  like stars*, A&A 490, 297 (`2008A&A...490..297S`,
  arXiv:0805.3936). Castor 운동성단 [Fe/H] = −0.03 ± 0.05 — 보강용
  금속도 (cfg 는 Phase 2 recommended 값으로 Dunkin 1997 을 인용.
  둘 다 거의 태양값).
- **Stapelfeldt K. R. et al. 2004** — *First Look at the Fomalhaut
  Debris Disk with Spitzer*, ApJS 154, 458
  (`2004ApJS..154..458S`). Spitzer/MIPS 24/70/160 µm 측광. 먼지
  원반의 첫 다중 밴드 열복사 특성화.
- **Currie T. et al. 2012** — *A Direct-Imaging Survey of the
  Fomalhaut Planetary System with the Hubble Space Telescope*, ApJ
  760, L32 (`2012ApJ...760L..32C`, arXiv:1210.6555). "Fomalhaut b"
  의 독립 HST 재분석. 광원이 자체발광 행성이 아니라는 초기 증거.
- **Schröder C. & Schmitt J. H. M. M. 2007** — *X-ray emission from
  A-type stars*, A&A 475, 677 (`2007A&A...475..677S`). A 형 별 X 선
  플럭스 ROSAT 서베이. Fomalhaut 의 log L_X 상한을 결정.
- **Greaves J. S. et al. 2014** — *Alignment of the host star spin
  with the orbit of debris discs*, MNRAS 438, L31
  (`2014MNRAS.438L..31G`, arXiv:1311.3431). A 형 별 잔해 원반
  호스트의 종족 전체 spin-orbit 정렬. Le Bouquin 2009 의 정렬
  가정을 뒷받침.

### Read (instrument / non-cfg-decisive)

- **Gray R. O. & Garrison R. F. 1989** — *The Late A-Type Stars:
  Refined MK Classification* (`1989ApJS...70..623G`). MK 시스템
  재분류. Fomalhaut 를 A3V/A4V 경계에 배치.
- **Monnier J. D. et al. 2010** — *Imaging the surface of Altair*,
  Science 317, 342 (`2007Sci...317..342M`). 비교 가능한 빠른 자전체
  A 형 별의 중력 어두워짐 지도 참조.
- **Kopparapu R. K. et al. 2013** — *Habitable zones around main-
  sequence stars*, ApJ 765, 131 (`2013ApJ...765..131K`,
  arXiv:1301.6674). A4V 별 HZ 안쪽/바깥쪽 경계.
- **Wyatt M. C. 2008** — *Evolution of Debris Disks*, ARA&A 46, 339
  (`2008ARA&A..46..339W`). 분해된 잔해 원반의 충돌 cascade 보충
  이론 프레임워크. `disk_planetesimal_belt_inferred` 필드를 뒷받침.

### Not read — no arXiv preprint or low-priority (~30 papers)

학회 초록 (AAS / DPS / EPSC), 간섭계 방법 논문 (CHARA / PTI
commissioning), 후속 먼지 입자 광물학 작업 (Spitzer IRS 분광) 은
Di Folco 2004 + Boley 2012 + Gáspár 2023 가 이미 확립한 내용을
넘어서는 cfg-결정적 기여를 하지 않습니다. "Fomalhaut b" 위치의
SETI / 전파 방출 모니터링 (Tusay 2022, Saide 2023) 도 제외합니다.
필터링된 bib 는 `docs/phase3/_bib/fomalhaut.yaml` 에 `status:
skipped` annotation 으로 보존됩니다.

## Open items for follow-up

- **TW Piscis Austrini (HD 216803, K4V) 와 LP 876-10 (M4V) 의 별도
  NS DB 엔트리화.** 광폭 공통 고유운동 동반성 두 개는 현재 152
  시스템 NearStars 쇼트리스트에 들어 있지 않습니다. Mamajek
  2012/2013 은 두 별이 중력적으로 연합돼 있고 같은 나이 (440 Myr)
  의 Castor 운동성단 멤버임을 0.91 ly 와 5.7 ly 투영 분리에서
  확립합니다. 별도 DB 엔트리로 추가되면 게임 내 플레이어가 실제
  성간 궤적을 따라 세 별 사이를 비행할 수 있게 됩니다. Phase 2
  DB 확장 후보로 플래그.
- **disk 지오메트리가 `disks_curated.json` 에 multi-belt 로 기록됨**
  (2026-05-29 감사). Fomalhaut 의 warm + intermediate + cold 벨트가
  별도 `belt` 항목이며, Decisions 표가 belt별 `disk_<belt>_*` 필드로
  렌더 → belt당 Kopernicus Ring 하나씩. 남은 것은 tie-break per-belt
  tint 를 대체할 grain-size / Mie 색 합성.
- **"Fomalhaut b S1" 후보 재방문.** 2026+ 의 JWST/MIRI 또는 지상
  ELT follow-up 이 Gáspár & Rieke 2020 의 먼지 구름 해석을 뒤집고
  ~115 AU 의 묶인 행성을 다시 확립한다면, 새 Decisions 엔트리
  `circumstellar_planet_present: true` (후보명 "S1") 가 필요해지며
  cfg 는 현재 컨센서스로부터의 divergence 를 문서화해야 합니다.
  그 전에는 어떤 행성도 포함하지 않습니다.
- **Phase 2 `teff_measurements` 와 `metallicity_measurements`
  채움.** DB 는 `teff_k = 8689` 를 출처 엔트리 없이 SIMBAD
  컴파일레이션 스칼라로 갖고 있고 Saffe 2008 금속도도 DB 에 없습
  니다. 둘 다 논문 인용된 Phase 2 엔트리로 추가해야 합니다.
- **중력 어두워짐 지도.** Fomalhaut 의 분해된 간섭계 중력 어두워짐
  지도는 존재하지 않습니다 (Vega, Altair, Regulus 와 달리).
  CHARA/MIRC 또는 VLTI/GRAVITY 가 von-Zeipel 극-적도 온도 구배를
  관측하면 cfg 가 현재의 uniform-disk 색조를 위도 구배로 바꿀 수
  있게 됩니다 (`visual_gravity_darkening_delta_t_k` 필드, 현재
  부재).

## Related

- [methodology](../reference/methodology.md) — Decisions 테이블의 스키마 출처
- [alpha-centauri-a](alpha-centauri-a.md) — canonical 항성 합성 템플릿. G2V 비교 대상
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — TW PsA / LP 876-10 이 향후 NS DB 로 격상될 경우 관련될 광폭 동반성 CPM 처리
