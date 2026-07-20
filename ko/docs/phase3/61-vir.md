<!-- 61 Virginis Phase 3 합성. cfg-ready 결정과 근거 -->
# 61 Virginis — Phase 3 Synthesis

61 Virginis (HD 115617, HIP 64924, GJ 506) 은 8.534 ± 0.001 pc (Gaia
DR3 시차 117.17 ± 0.15 mas, 27.83 광년) 거리의 처녀자리에 위치한
맨눈 가시 G6.5V 솔라 트윈입니다. 분광형 G6.5V (Gray 2003 은 G7V) 는
이제 von Braun 2014 에 anchor 되어 있습니다. 이 연구는 CHARA 간섭계로
별을 직접 분해해 θ_LD = 1.073 ± 0.005 mas → R = 0.9867 ± 0.0048 R☉,
Teff = 5538 K (θ_LD + 볼로메트릭 플럭스), L = 0.8222 ± 0.0033 L☉, 그리고
Y² 질량 0.93 M☉ 를 얻었습니다. 나머지 파라미터는 솔라 트윈에 가깝지만
태양보다 ~230 K 더 차갑다는 뜻입니다. 금속도는 사실상 태양과 같습니다
([Fe/H] = −0.01 ± 0.01, Santos/Sousa 2013). 나이는 documented divergence
(~6–9 Gyr) 로, cfg 는 Gomes da Silva 2021 의 isochrone 7.69 ± 1.44 Gyr 를
채택합니다. von Braun 의 8.6 Gyr, Mamajek 2008 의 활동도-나이 6.1–6.6 Gyr
와 견주어, 61 Vir 는 태양보다 더 나이 든 원반종족 솔라 트윈입니다. 별
자체는 조용한 상태로, 회전 주기 P_rot ≈ 29 일 (Baliunas 1996 Ca II HK),
log R'HK = −5.013 (Gomes da Silva 2021), 그리고 희미한 X 선 방출
(log Lx/Lbol ~ −6.9, Wright 2011) 을 보입니다.

61 Vir 는 RV 로 검출된 행성 세 개를 거느립니다 (Vogt 2010 의 HIRES +
AAT 결합 해). b 는 4.215 일 주기 5.1 M⊕ Msini 의 슈퍼지구, c 는
38.021 일 주기 18.2 M⊕ 의 따뜻한 sub-Neptune, d 는 123.01 일 주기
22.9 M⊕ 의 sub-Neptune 입니다. 행성대 바깥에서는 **Wyatt et al.
2012 의 Herschel/PACS 영상이 ≈ 30 AU 부근을 중심으로 하는 차가운
debris 띠를 분해**하며, 바깥쪽은 ≈ 96 AU 까지 뻗고 dust 온도 ~68 K
인 전형적 KBO 아날로그입니다. dust 질량은 태양의 Edgeworth–Kuiper
띠 잔존량과 비슷합니다.

**NearStars 시나리오 선택. 조용하고 약간 더 차가운 G6.5V 솔라 트윈,
~30 AU 의 단일 차가운 debris 띠가 분해되며, 안쪽 행성 세 개가 전경의
점광원으로 함께 보이는 모습으로 렌더링합니다.** 항성 레이어는 von Braun
2014 CHARA 간섭계 + Gomes da Silva 2021 활동도에 다시 anchor 했습니다
(나이는 documented divergence). tie-break 세 행은 시각 색조, debris 띠
산란 색조, debris 띠 불투명도로, Herschel 의 원적외선 검출이 광학 외관을
제약하지 않는 영역의 선택입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G7 V | high | von Braun 2014 (Table 4). Gray 2003 과 일관 |
| `mass_msun` | 0.93 | high | von Braun 2014. 간섭계 R, Teff 위의 Y² isochrone (Phase 2 recommended. Vogt 2010 을 대체) |
| `radius_rsun` | 0.9867 ± 0.0048 | high | von Braun 2014. CHARA 간섭계, θ_LD 1.073 ± 0.005 mas (Phase 2 recommended. 유일한 간섭계 반지름. Boyajian 2012/2013 에는 61 Vir 가 없음) |
| `teff_k` | 5538 | high | von Braun 2014. 간섭계 θ_LD + 볼로메트릭 플럭스 (Phase 2 recommended. Gaia 의 5552 를 대체) |
| `luminosity_lsun` | 0.8222 ± 0.0033 | high | von Braun 2014. 볼로메트릭 플럭스 F_bol 36.06e-8 erg/s/cm² + 시차 (Phase 2 recommended) |
| `metallicity_fe_h_dex` | −0.01 ± 0.01 | high | Santos/Sousa 2013 (Phase 2 recommended. 태양 근방. Sousa 2008 −0.02 가 보강) |
| `age_gyr` | 7.69 ± 1.44 | medium | Gomes da Silva 2021 isochrone (Phase 2 recommended). DOCUMENTED DIVERGENCE. von Braun 2014 isochrone 8.6 대 Mamajek 2008 활동도-나이 6.1–6.6 Gyr. 모두 늙은 별, ~6–9 Gyr (Canonical alternatives 참조) |
| `rotation_period_days` | 29 | high | Baliunas 1996. Mt Wilson Ca II HK 주기 (Phase 2 recommended. Wright 2011 이 정리, Vogt 2010 이 채택) |
| `activity_log_rhk` | −5.013 ± 0.003 | high | Gomes da Silva 2021. AMBRE-HARPS, 1251 스펙트라 (Phase 2 recommended. Mamajek 2008 −5.001 이 보강). 비활성 |
| `x_ray_log_lx_lbol` | ~ −6.9 | low | Wright 2011 (ROSAT/Voges 1999 정리). 희미한 X 선, log(Lx/Lbol) ~ −6.9. VizieR-only, 동결된 Phase 2 측정치 아님 |
| `visual_surface_tint_hex_primary` | `#fff2dc` (태양보다 더 호박색이 도는 따뜻한 크림) | medium | Tie-break. G7 V 5538 K 흑체 + 플레이어의 태양 기준보다 더 차가운 G 왜성이라는 interesting-first 단서 (hex 불변. 5552→5538 K 변위는 지각 한계 아래) |
| `stellar_color_temp_k` | 5538 | high | Teff 유도 (von Braun 2014) |
| `activity_cycle_years` | null | low | 분해된 사이클 없음. null/미측정으로 기록 |
| `visual_spot_coverage_max` | 0.003 | low | Synthesis. 매우 비활성 (log R'HK −5.013), 디스크 면적 ≤0.3% |
| `disk_present` | true | high | Wyatt et al. 2012. Herschel/PACS 분해된 차가운 띠. Tanner 2014, Su 2017 SED 로 확인 |
| `disk_inner_radius_au` | 30 | high | Wyatt 2012. Herschel/PACS 분해 지오메트리. modified-blackbody SED fit 으로 온도-가중 반경이 30 AU 근방 |
| `disk_outer_radius_au` | 96 | medium | Wyatt 2012 는 ~30 AU 부터 적어도 ~100 AU 까지 분해. 96 AU 수치는 Tanner 2009 의 SED 에서 유래 |
| `disk_dust_temperature_k` | 68 | high | Wyatt et al. 2012 — 단일 온도 흑체 SED fit, 68 K |
| `disk_tint_rgb_hex` | `#fff0e7` (옅은 따뜻한색. vivid `#ffd7b9`) | low | 측정된 광학 색이 없음 (열복사/mm 만, 분광 특징 없음, Wyatt 2012). Mie 반사율 합성. blowout 크기의 규산염 입자 (a_min ~0.44 µm) → 따뜻한 쪽으로 기운 반사율 (B/I 0.64). 렌더러가 그 위에 G7 V 별빛을 입힘. vivid 팩. `#ffd7b9` |
| `disk_opacity` | 0.10 | low | Tie-break. Herschel τ ~ 10⁻⁵ (원적외선 광학 깊이) 는 플레이어 가시성 한참 아래. cfg 는 렌더러 가시 값을 채택하되 띠가 분명히 희미하게 보이도록 유지 |
| `disk_morphology` | single cold belt, KBO analog | high | Wyatt 2012. 단일한 넓은 띠. warp/gap/이중대 구조 보고 없음 |
| `disk_resolved_imaging` | true | high | Wyatt 2012. Herschel/PACS 70/100/160 μm 에서 분해 |
| `disk_imaging_observatory` | Herschel/PACS (Wyatt 2012) | high | 직접 인용 |
| `disk_mass_mearth` | 0.07 | low | Wyatt 2012 는 61 Vir disk 질량이 카이퍼대와 비슷하다고 명시. cfg 의 0.07 M_earth 은 그 범위 안의 mm-grain 추정치 |
| `disk_planetesimal_belt_inferred` | true | high | Wyatt 2012 §5. PR drag + 충돌 분쇄에 대한 dust 수명상 관측된 dust 를 채우려면 부모 천체 띠가 필요 |

## Surface synthesis

61 Vir 의 광구는 태양보다 ~230 K 더 차갑습니다. Teff 5538 K 대 태양
기준 5772 K (von Braun 2014 간섭계) 입니다. 다른 솔라 트윈 파라미터
에서는 거의 같으며, 질량 0.93 M☉, 반지름 0.9867 R☉, [Fe/H] 가 태양과
0.01 dex 이내입니다. 광도 0.8222 L☉ 는 거의 태양과 같은 반지름에 더
낮은 온도가 결합된 자연스러운 결과입니다. 가시 영역에서 스펙트럼은 canonical G 왜성 Ca II H&K, Mg b,
Na D, Hα 시그니처를 가지며, 선 깊이는 태양형 G2V 와 약간 더 붉은 K0V
의 중간쯤에 위치합니다. Pavlenko et al. 2012 의 고분해 분광은 미량
원소까지 솔라 트윈 풍부도 패턴을 확인했으며, 비정상적인 리튬 결핍이나
빠른 회전 veiling 은 없습니다.

3D 복사-유체역학 시뮬레이션 (비슷한 G6/G7V 타깃에 적용된 Magic 2013
의 STAGGER/CO5BOLD 계열 그리드) 은 granulation 셀 크기가 태양보다
~10% 더 크고 대비가 약간 더 강할 것으로 예측합니다. 더 차가운 Teff
에서 대류 turnover 가 느려지는 효과입니다. 흑점 면적은 색채권 log
R'HK = −5.0 (Isaacson & Fischer 2010) 을 따라가며, 61 Vir 를 τ Ceti
나 α Cen B 같은 조용한 왜성 locus 에 놓습니다. 추정된 활동 사이클의
최대점에서도 흑점 피크 면적은 가시 디스크의 ≲ 0.3% 로, 태양 극대기
보다도 살짝 적습니다.

H 밴드 limb darkening 은 61 Vir 에 대해 직접 측정된 적이 없습니다.
α Cen A 의 Kervella 2017 같은 PIONIER 캠페인이 없기 때문입니다.
다만 1D 대기 예측은 α_H ≈ 0.20 을 줍니다. α Cen A 의 측정값 0.14
보다 살짝 더 강한 값으로, 더 차가운 Teff 와 일관됩니다. NearStars 는
직접 간섭 후속 관측이 나오기 전까지는 Confidence=medium 으로 1D
예측을 채택합니다.

시각 색조의 약한 호박색 변위는 tie-break 입니다. 5538 K 흑체 피크는
λ_max 기준 태양보다 8% 더 붉은 쪽으로 이동해 있으며, 이는 순수한 태양
일치가 아닌 약간 더 크림이 도는 시각 단서를 채택한 근거 중 하나입니다.

## Atmosphere synthesis

61 Vir 는 오래되고 자기적으로 비활성인 솔라 트윈답게 조용한 G 왜성
chromosphere–transition-region–corona 구조를 가집니다. 색채권 S-index
(Wilson 1968 Mt Wilson 컨벤션) 는 log R'HK ≈ −5.0 으로 환산됩니다
(Isaacson & Fischer 2010). 현대 태양의 극소기보다 약 0.05 dex 더 조용
하며, 전형적인 어린 G 왜성보다는 0.20 dex 더 낮습니다. 전이 영역
UV 방출과 X 선 광도 log L_X = 26.7–27.0 cgs (0.1–2 keV, Schmitt &
Liefke 2004 NEXXUS-2 카탈로그) 는 61 Vir 를 비활성 G 왜성 locus 한가운데
에 분명히 배치합니다.

α Cen A 의 Robrade 2016 가 검출한 19 년 사이클에 견줄 만한 장기 활동
사이클은 61 Vir 에서 아직 분해되지 않았습니다. 색채권 모니터링 기록이
더 짧고, 잠재된 사이클 진폭도 작을 것으로 예상됩니다. 광도 잡음 위로
올라오는 flare 도 보고된 바 없습니다. 61 Vir 는 모든 안쪽 행성에 우호적인
우주환경을 제공합니다 (Vogt 2010 세 행성 모두 < 0.5 AU 안에 들어 있습니다).

통합 XUV 광도는 10⁻⁴ L_bol 이하로 태양과 비슷하거나 더 조용하며,
~0.3 AU 이상에 있는 어떤 지구 질량 행성의 일차 대기도 Gyr 시간 스케일
에 걸쳐 의미 있게 침식할 수 없습니다. 안쪽 행성 b (0.050 AU, 별도 Phase 3
워크스페이스) 는 광증발 영향 영역에 있지만, 별의 XUV 기여는 동일 일조량
에서 태양보다 더 공격적이지 않습니다.

## Rotation & spin synthesis

29 일 회전 주기 (Baliunas 1996 Mt Wilson Ca II HK. Wright 2011 이 정리
하고 Vogt 2010 §4 가 RV 잔차의 28–30 일 power 로 확인) 는 태양의 25.4 일
Carrington 회전보다 약간 느립니다. Skumanich braking 법칙 P_rot ∝ √t 에 따라
61 Vir 가 태양보다 ~1 Gyr 더 오래된 점과 일관됩니다. 오래된 원반종족
솔라 트윈에 맞춰진 지수 (Mamajek & Hillenbrand 2008 gyrochronology) 는
6 Gyr G6.5V 의 기대 회전 주기를 28–31 일로 주는데, 61 Vir 는
gyrochronology locus 위에 정확히 올라옵니다.

61 Vir 에는 아직 asteroseismic 검출이 없습니다. Vmag = 4.71 이라
관측은 가능하지만, α Cen A 의 Bedding 2004 같은 전용 p-mode 캠페인이
수행된 적이 없습니다. 원칙적으로는 HARPS RV 시계열로 검출이 가능합니다.
차등 회전은 직접 분해되지 않지만, Skumanich locus 솔라 아날로그를
따라 적도가 극보다 ~20% 빠르게 회전할 것으로 예상됩니다.

회전축 경사는 제약되지 않습니다. 시각 렌더링을 위해 NearStars 는
안쪽 행성계 황도에 대해 30° 기울어진 축을 채택하며, 이는 무작위로
정렬된 자전축 가정과 일관됩니다. Vogt 2010 의 b/c/d 경사 posterior 는
거의 정렬된 거의 edge-on 시스템과 호환되지만, 별의 spin 과 직접 연결
짓기는 어렵습니다.

## Canonical alternatives

**나이 — isochrone 대 활동도.** cfg 는 Gomes da Silva 2021 의 isochrone
나이 7.69 ± 1.44 Gyr 를 채택하며, 그 범위 (~6.2–9.1 Gyr) 가 전체 산포를
감쌉니다. documented 대안은 von Braun 2014 의 간섭계-isochrone 8.6 Gyr 와
Mamajek & Hillenbrand 2008 의 활동도/gyrochronology 나이 6.1–6.6 Gyr
입니다. 신뢰할 만한 방법 모두 61 Vir 가 태양보다 더 나이 든 원반종족
솔라 트윈 (~6–9 Gyr) 임에 동의하며, divergence 는 어느 늙은 값을 가져갈
것인가뿐입니다.

**반지름/Teff — 간섭계 대 이전의 Vogt/Gaia 값.** cfg 는 von Braun 2014
CHARA 간섭계 (R 0.9867, Teff 5538) 를 씁니다. Phase 2 이전 서술은 Vogt
2010 (R 0.963) 과 Gaia 의 5552 K 를 썼습니다. von Braun 이 유일한 간섭계
출처이며, Boyajian 2012/2013 에는 61 Vir 가 없음이 확인되었습니다.

## Visual styling

NearStars 렌더러에서 61 Vir 는 따뜻한 크림 G6.5V 별로 묘사됩니다.
태양과 시각적으로 가깝지만 220 K 더 차가운 광구를 호박색으로 살짝
가미한 색조를 인코딩합니다. 시각 hex `#fff2dc` 는 순수한 태양 일치
에 대한 tie-break 선택입니다. 플레이어에게 자기 태양 기준보다 더
차가운 G 왜성이라는 즉각적인 단서를 주고, α Cen A 의 `#fff4e8` 크림
이나 47 UMa 같은 다른 근태양 Phase 3 타깃들과 61 Vir 를 구분하는 데
도움이 됩니다.

- **궤도 뷰 (시스템 진입)**. 태양빛 점광원이 ~30 AU 반경 중심의 거의
  원형 debris 띠로 둘러싸여 있으며, 띠는 ~96 AU 까지 뻗어 있습니다.
  띠는 가는 회청색 산란 밴드로 불투명도 0.10 으로 렌더링됩니다. 보이지만
  분명히 희미하며, 토성급 고리가 아닙니다.
- **근접 뷰 (행성대 안, < 1 AU)**. debris 띠는 배경으로 멀어지고, 안쪽
  행성 세 개 (b 0.05 AU, c 0.22 AU, d 0.48 AU) 가 행성 위상 동안 전경
  점광원으로 나타납니다. b 의 슈퍼지구 디스크와 c/d 의 sub-Neptune
  디스크는 매우 가까운 거리에서만 분해됩니다.
- **표면 뷰 (행성에서)**. 완만한 limb darkening, granulation 패턴,
  활동 시기의 희미한 흑점이 있는 알아볼 만한 태양형 디스크입니다. 0.48 AU
  (행성 d) 의 0.96 R☉ 별은 각지름 ~0.53° 를 차지하는데, 지구에서 본
  태양의 겉보기 크기와 거의 같습니다. 외행성 관측자에게는 거의 완벽한
  태양 아날로그입니다.
- **지구에서 본 별**. Vmag 4.71 로 맨눈 가시이지만 두드러지지 않으며,
  처녀자리 황도 근처에 들어 있습니다. NearStars 의 실제 별 모드에서는
  Gaia DR3 J2016.0 sky 위치가 게임 epoch 까지 선형 propagation 된 자리에
  나타납니다.
- **가상의 외행성에서 본 debris 띠**. 예를 들어 10 AU 위치에서 띠는
  황도를 따라 얇고 흐릿한 밴드로 형성됩니다. 뒷쪽에서 비추일 때 산란광
  으로 가장 밝아지는데, 해왕성 궤도 관측자가 태양계 Edgeworth–Kuiper
  띠를 본다면 보일 모습과 비슷하되 광학 깊이가 한 자릿수 더 높아 더 밝습니다 (Wyatt 2012).
- **조용한 별 애니메이션**. 흑점 렌더링은 절제됩니다. 피크 면적은 디스크의
  ≲ 0.3% 로 태양 극대기보다 훨씬 덜 극적입니다. 두드러진 flare 나 CME
  시각 효과는 없습니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **von Braun K. et al. 2014** — *Stellar diameters and temperatures
  VI: high-resolution angular diameters of exoplanet host stars*,
  MNRAS 438, 2413 (`2014MNRAS.438.2413V`, [arXiv:1312.1792](https://arxiv.org/abs/1312.1792)). 61 Vir 의
  CHARA 간섭계. θ_LD = 1.073 ± 0.005 mas → R = 0.9867 ± 0.0048 R☉.
  F_bol 36.06e-8 → Teff 5538 ± 13 K, L 0.8222 ± 0.0033 L☉. Y² 질량
  0.93 M☉, 나이 8.6 Gyr. **항성 레이어의 Phase 2 anchor** (61 Vir 의
  유일한 간섭계 반지름).
- **Gomes da Silva J. et al. 2021** — *Stellar chromospheric activity
  of the AMBRE-HARPS sample*, A&A 646, A77 (`2021A&A...646A..77G`,
  [arXiv:2012.10199](https://arxiv.org/abs/2012.10199)). log R'HK = −5.013 (1251 스펙트라) 과 isochrone
  나이 7.69 ± 1.44 Gyr. Phase 2 recommended 활동도 + 나이.
- **Santos N. C. et al. 2013** — *SWEET-Cat*, A&A 556, A150
  (`2013A&A...556A.150S`). [Fe/H] = −0.01 ± 0.01 (Phase 2 recommended
  금속도. Sousa 2008 −0.02 가 보강).
- **Vogt S. S. et al. 2010** — *A Super-Earth and Two Neptunes
  Orbiting the Nearby Sun-Like Star 61 Virginis*, ApJ 708, 1366
  (`2010ApJ...708.1366V`). 세 행성 검출 (b 4.215 일, c 38.021 일,
  d 123.01 일). 항성 파라미터 (M 0.942, R 0.963, L 0.82) 는 위의 von
  Braun 2014 간섭계로 대체됨.
- **Wyatt M. C. et al. 2012** — *Herschel imaging of 61 Vir: implications
  for the prevalence of debris in low-mass planetary systems*, MNRAS
  424, 1206 (`2012MNRAS.424.1206W`, [arXiv:1204.6063](https://arxiv.org/abs/1204.6063)). Herschel/PACS
  로 70/100/160 μm 에서 차가운 debris 띠를 분해 영상화. ~30 AU 중심,
  ~96 AU 까지 뻗는 단일한 넓은 띠, dust 온도 ~68 K, dust 질량 태양 KBO
  잔존량과 비슷. Circumstellar-disk 모든 Decisions 행의 anchor.
- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age Estimation
  for Solar-Type Dwarfs Using Activity-Rotation Diagnostics*, ApJ 687,
  1264 (`2008ApJ...687.1264M`, [arXiv:0807.1686](https://arxiv.org/abs/0807.1686)). 활동도/gyrochronology
  나이 6.1–6.6 Gyr 과 log R'HK −5.001. Gomes da Silva 2021 isochrone
  나이에 대한 documented-divergence 대안.
- **Baliunas S. L. et al. 1996** / **Wright J. T. et al. 2004** — 61 Vir
  의 Mt Wilson Ca II HK 회전 P_rot ≈ 29 일 (`2004ApJS..152..261W`).
  Baliunas 1996 이 Phase 2 recommended 회전 출처이며, Wright 2011 이
  정리.
- **Pavlenko Y. V. et al. 2012** — *Effective temperatures, gravities,
  metallicities, and ages of 18 solar twin candidates*
  (`2012MNRAS.422..542P`, [arXiv:1112.0590](https://arxiv.org/abs/1112.0590)). 61 Vir 를 포함한 솔라 트윈
  후보의 고분해 분광. Teff = 5538 K 와 태양으로부터 0.05 dex 이내의
  [Fe/H] 를 확인.

### Read (context / methodology, not directly decision-driving)

- **Isaacson H. & Fischer D. 2010** — *Chromospheric Activity and Jitter
  Measurements for 2630 Stars on the California Planet Search*, ApJ
  725, 875 (`2010ApJ...725..875I`, [arXiv:1009.2301](https://arxiv.org/abs/1009.2301)). California HK
  카탈로그 refit. 61 Vir log R'HK ≈ −5.0 이 여러 시즌에 걸쳐 안정함을
  확인.
- **Schmitt J. H. M. M. & Liefke C. 2004** — *NEXXUS: A Comprehensive
  ROSAT survey of coronal X-ray emission among nearby solar-like
  stars*, A&A 417, 651 (`2004A&A...417..651S`). NEXXUS-2 카탈로그. 61
  Vir log L_X ≈ 26.7–27.0 cgs, 조용한 G 왜성 locus.
- **Tanner A. et al. 2014** — 61 Vir disk SED + 영상 follow-up 의
  context 논문. Wyatt 2012 의 차가운 띠 지오메트리를 강화.
- **Su K. Y. L. et al. 2017** — *Hot extended Solar System dust and
  cold debris disks in the Spitzer + Herschel surveys*, AJ 153, 226
  (`2017AJ....153..226S`). 차가운 disk 샘플의 61 Vir. Wyatt 2012 와
  일관.
- **Bensby T. et al. 2014** — *Exploring the Milky Way stellar disk: a
  detailed elemental abundance study of 714 F and G dwarfs*, A&A 562,
  A71 (`2014A&A...562A..71B`, [arXiv:1309.2631](https://arxiv.org/abs/1309.2631)). 얇은 원반 금속도 샘플
  의 61 Vir. [Fe/H] 가 태양과 일관.
- **Brewer J. M. et al. 2016** — *Spectral Properties of Cool Stars
  (SPOCS): extended catalog of 1626 stars*, ApJS 225, 32
  (`2016ApJS..225...32B`, [arXiv:1606.07929](https://arxiv.org/abs/1606.07929)). SPOCS 확장 카탈로그.
  61 Vir 의 [Fe/H], Teff, log g refit 이 Pavlenko 2012 의 솔라 트윈
  값과 일관.

### Read (instrument-only, not visual-informative)

- **Gray R. O. et al. 2003** — *Contributions to the Nearby Stars
  (NStars) Project*, AJ 126, 2048 (`2003AJ....126.2048G`). 원래의 G7V
  분류. Gaia DR3 의 G6.5V 는 더 세분된 후속.
- **Lawler S. M. et al. 2014** — 태양형 별 주위 차가운 disk 인구의
  context 논문. 61 Vir 가 인용됨.
- **Magic Z. et al. 2013** — 차가운 왜성용 STAGGER 3D RHD 그리드.
  granulation 논의에서 인용.

### Not read — no arXiv preprint or low-priority (~30 papers)

학회 abstract (DDA, EPSC), SETI / 레이저 방출 탐색, 매우 큰 분리에서의
brown-dwarf 동반자 radial-velocity follow-up, 그리고 astrobiology white
paper 등은 cfg 결정에 영향이 없습니다. 전체 필터된 bib 는
system.yaml 기반 Stage 5 필터가 실행되면 `docs/phase3/_bib/61-vir.yaml`
에 보존됩니다. 이 literature-direct 항성 합성에서는 아직 bib yaml 이
존재하지 않습니다.

## Open items for follow-up

- **Phase 2 `disk_measurements` ingest.** 이 합성은 Wyatt 2012, Tanner
  2014, Su 2017 을 직접 인용합니다. `db/systems/61_vir.json` 에 구조화된
  `disk_measurements` 배열을 추가하면 (Wyatt 2012 의 지오메트리 + dust
  질량을 recommended 항목으로) 감사 추적이 정식화됩니다. disk 지오메트리
  행의 Confidence 는 바뀌지 않지만 (이미 high), Basis 의 literature-direct
  플래그가 깔끔한 DB 참조로 대체됩니다.
- **행성 b/c/d Phase 3 follow-up.** 별도 워크스페이스
  (`phase3/61_vir_planets/`) 에서 Vogt 2010 의 세 행성을 합성합니다. b
  는 0.050 AU 의 5.1 M⊕ 슈퍼지구 (뜨거운 암석 / 증기 대기 범주에 가능성),
  c 는 0.22 AU 의 따뜻한 sub-Neptune (~18 M⊕), d 는 0.48 AU 의 더 차가운
  sub-Neptune (~23 M⊕) 입니다. 셋 다 transit 하지 않으므로 (RV-only),
  대기 특성화는 직접 영상 제안서를 통한 반사광 영역에서 이루어집니다.
- **Asteroseismic 캠페인.** Vmag 4.71 의 61 Vir 는 HARPS/ESPRESSO 로
  접근 가능합니다. 전용 p-mode 검출이 이루어지면 asteroseismic 나이를
  더 좁힐 수 있습니다. 현재는 Mamajek 2008 의 6.1 ± 1.7 Gyr 이며, Δν +
  ν_max 에 묶인 나이는 불확실도를 약 3 배 줄일 것입니다.
- **debris 띠의 직접 영상 follow-up.** ALMA 밀리미터 영상 (CO + dust
  연속체) 은 Herschel 의 공간 분해능을 넘어 띠 지오메트리를 정련합니다.
  날카로운 안쪽 경계나 비대칭이 검출되면 `disk_morphology` 필드를
  "single cold belt, KBO analog" 에서 더 상세한 모양으로 격상할 수 있습니다.
- **장기 활동 사이클.** 61 Vir 의 색채권 모니터링 기록은 태양형 사이클을
  확인하거나 부정하기에는 너무 짧습니다. 향후 10 년 동안의 Mt Wilson /
  California HK follow-up 이 `activity_cycle_years` 필드를 채울 것입니다.

## Related

- [alpha-centauri-a](alpha-centauri-a.md) — 솔라 트윈 비교. 61 Vir 는 8.53 pc 거리의 더 차갑고 더 조용한 아날로그. α Cen A 는 1.34 pc.
- [methodology](../reference/methodology.md) — Decisions 표 스키마의 원본.
- [data-sources](../reference/data-sources.md) — 이 합성이 따르는 논문 인용 정책.
