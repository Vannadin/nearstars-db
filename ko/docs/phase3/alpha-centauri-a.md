<!-- α Centauri A Phase 3 합성: cfg-ready 결정과 근거 -->
# α Centauri A — Phase 3 Synthesis

α Centauri A (HD 128620, HIP 71683, GJ 559 A) 는 가장 가까운 별쌍의 더
밝은 별이자 태양에 가장 가까운 G형 별입니다. 분광형은 G2V (Porto de
Mello 2008) 로 사실상 태양의 쌍둥이이며, 거리 1.3384 ± 0.0011 pc 에
있습니다 (Kervella 2017 의 Pourbaix & Boffin 2016 시차 747.17 ± 0.61 mas
유도). α Cen B 와 79.91 년 주기의 시각 이중성을 이루며, 궤도 이심률
e ≈ 0.52 로 근일점 11.2 AU, 원일점 35.6 AU 까지 벌어졌다 좁혀집니다.
Proxima Centauri 가 약 13 000 AU 거리에 중력적으로 묶여 삼중계를
완성합니다 (Kervella 2017).

기본 파라미터는 예외적으로 잘 제약돼 있습니다. VLTI/PIONIER 간섭계
각지름 (Kervella 2017) 으로 R = 1.2234 ± 0.0053 R☉ (0.43% 정밀도) 가
나오며, Pourbaix & Boffin 2016 의 분광 이중선 시각이중성 해는 역학질량을
1.1055 ± 0.0039 M☉ 로 고정합니다. Bouchy & Carrier (2001), de Meulenaer
2010 가 검출한 asteroseismic 진동을 고전 관측치와 결합하면 α Centauri
시스템 나이가 **5.3 ± 0.3 Gyr** 로 나옵니다 (Joyce & Chaboyer 2018). DB
Phase 2 attribution 에는 다소 부정확한 4.81 ± 0.5 Gyr 가 들어 있는데,
이는 논문 본문 표제값이 아니라 중간 단계 모델 fit 을 옮겨 적은 듯합니다.
이 합성은 논문 표제값을 사용하며, DB 오기 정정은 Open items 에 남겨
둡니다.

금속도는 약간 super-solar 인 [Fe/H] = +0.24 ± 0.03 (Porto de Mello 2008)
으로 원반 종족 운동학과 일관됩니다. 광도 변화로 측정한 회전 주기는
22 ± 3 일이며 (DeWarf 2010), 같은 캠페인이 색채권 활동도 log R'HK =
−4.95 를 잰 결과는 조용한 상태이지만 Robrade 2016 가 X 선에서 검출한
약 19 년 주기의 태양형 코로나 사이클이 있음을 함께 보여 줍니다. α Cen A
주위에는 확인된 행성이 없으며, Beichman & Sanghi 2025 가 MIRI 직접 촬영
으로 ≈ 1.5 AU 떨어진 점원 후보를 보고했지만 이 합성 시점에는 미확인
상태입니다.

**NearStars 시나리오 선택. 태양보다 살짝 더 밝고 따뜻한 조용한 G2V 별로,
K1V 동반자 B 와 시각적으로 가까이 보이며 Proxima 와는 엄청난 각도
분리로 보이는 모습으로 렌더링합니다.** 17 개 cfg 픽은 모두 canonical
파라미터 셋을 따르며, tie-break 4 개는 시각 hex 색상과 이중성 이벤트
지오메트리처럼 문헌이 침묵한 영역의 미적 선택입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G2V | high | Porto de Mello 2008. IAU MK 시스템 |
| `mass_msun` | 1.1055 ± 0.0039 | high | Pourbaix & Boffin 2016. 분광 이중선 시각이중성 fit |
| `radius_rsun` | 1.2234 ± 0.0053 | high | Kervella 2017. VLTI/PIONIER limb-darkened 간섭계 |
| `teff_k` | 5847 ± 27 | high | Porto de Mello 2008. 고분해 분광, 태양 대비 differential |
| `luminosity_lsun` | 1.519 | high | R 과 Teff 로 Stefan–Boltzmann 유도. Bigot 2008 일치 |
| `metallicity_fe_h_dex` | +0.24 ± 0.03 | high | Porto de Mello 2008. Joyce 2018 채택 |
| `age_gyr` | 5.3 ± 0.3 | high | Joyce & Chaboyer 2018. asteroseismic + 고전 관측 결합, DSEP 코드, 31 viable model pairs |
| `rotation_period_days` | 22 ± 3 | high | DeWarf 2010. 광도 변화 |
| `activity_log_rhk` | −4.95 | high | DeWarf 2010. 색채권 Ca II H&K |
| `activity_cycle_years` | 19 | medium | Robrade 2016. 코로나 X 선 사이클, 진폭 태양형 |
| `x_ray_log_lx_cgs_min` | 27.0 | medium | Robrade 2016 사이클 최소 |
| `x_ray_log_lx_cgs_max` | 27.6 | medium | Robrade 2016 사이클 최대 |
| `limb_darkening_alpha_h` | 0.1404 ± 0.0050 | high | Kervella 2017. H 밴드 power-law fit, 1D 모델 예측보다 살짝 약함 |
| `visual_surface_tint_hex_primary` | `#fff4e8` (태양보다 약간 더 노란빛이 도는 따뜻한 흰색) | medium | Tie-break. G2V 흑체 5847 K + 태양 기준과의 시각적 구분, interesting-first 룰 에 따른 interesting-first |
| `stellar_color_temp_k` | 5847 | high | Teff 유도 |
| `visual_in_planet_sky_apparent_diameter_arcmin` (평균 23 AU 에 있는 α Cen B 에서 본 값) | 0.5 | high | 유도. 2 R★ / a × (180·60/π) |
| `visual_companion_event_corona_visible_during_b_eclipse` | true | medium | Tie-break. 가상의 α Cen B 행성에서 본 conjunction 시 B 가 A 를 가리면 corona 가 드러남, 게임 내 드물고 극적인 이벤트 |

## Surface synthesis

α Centauri A 의 광구는 NearStars 카탈로그 전체에서 태양과 가장 비슷한
analog 입니다. 유효 온도 5847 K 는 태양보다 75 K 높으며, 절반 등급 더
높은 광도는 super-solar 금속도로 살짝 부풀린 1.22 R☉ envelope 에서
나옵니다. 3D 복사-유체역학 granulation 시뮬레이션 (Kervella 2017 §4 가
사용한 STAGGER 코드) 은 ~5% 의 스케일 차이를 빼면 granulation 대비와
시간 스케일이 태양과 거의 동일하다고 예측합니다. 가시 디스크는 canonical
태양형 중심 밝기와 완만한 limb darkening 을 보입니다. Kervella 가 측정한
H 밴드 power-law exponent α(A) = 0.1404 는 1D 대기 모델 예측보다 살짝
약하며, 이는 태양 자체가 해석적 limb-darkening 으로부터 벗어나는 양상과
같습니다.

흑점 면적은 적당합니다. log R'HK = −4.95 (DeWarf 2010) 는 A 를 현대
태양보다 분수만큼 덜 활동적인 위치에 놓습니다. 19 년 코로나 사이클
(Robrade 2016) 최대점에서 흑점 피크 면적은 태양 극대기와 비슷하며
(디스크의 ~0.5%), 활동 영역은 ±35° 위도에 형성됩니다. α Cen A
거주가능영역 (~1.3 AU, Wang 2022) 의 안정 궤도에서 관측자가 본다면
limb darkening 과 granulation 패턴, 활동 극대기의 흑점, 활동 영역
사이에 다리를 놓는 faculae 가 모두 있는 알아볼 수 있는 태양형 디스크를
보게 됩니다.

살짝 높은 금속도는 SED 를 미세하게 붉은 쪽으로 기울입니다. +0.24 dex 의
Fe/H 증가는 볼로메트릭 연속체를 ~10 K 등가로 reddening 시키는데, 게임 내
조명 색온도가 다루는 분광 분해능에서는 감지되지 않지만 순수 태양-백색
기준보다 따뜻한 크림 색조를 선택한 근거 중 하나가 됩니다.

## Atmosphere synthesis

α Cen A 는 표준 chromosphere–transition-region–corona 구조를 갖춘 조용한
G 왜성 대기를 가집니다. 색채권은 Hα 와 Ca II H&K 방출로 적당히 채워져
있으며, DeWarf 2010 의 FUV/UV 모니터링은 11 년 (색채권) 과 19 년 (코로나
X 선, Robrade 2016) 두 사이클 동안 태양형 활동과 일관된 방출선을 보입니다.
X 선 광도 범위 log L_X = 27.0–27.6 (cgs, 0.5–2 keV) 은 약 4 배 변동하며
여기서도 태양형입니다.

DeWarf 모니터링의 광도 잡음을 넘는 빈번한 flare 증거는 없으며, α Cen A
는 불활성 G 왜성 locus 의 한가운데에 위치해 어떤 안쪽 행성에도 우호적인
우주환경을 제공합니다. 코로나 질량 방출이 태양과 비슷하다면 사건당
~10²² g 의 질량을 분출하고, 사이클 최대기에 하루 ~1–10 회 일어날 텐데,
1 AU 부터의 방사 스케일을 고려하면 어떤 α Cen A 행성 후보 위치에서도
태양-지구 값과 거의 차이가 나지 않습니다.

전이 영역에서는 G2V 별답게 Lyman-α 연속체 + Lyα 라인이 나오며, Ayres
2015 의 Tier-B 참조들이 전체 UV-X 선 스펙트럼을 정리합니다. 통합 XUV
광도는 10⁻⁴ L_bol 이하이며, A 의 거주가능영역에서 지구형 대기를 Gyr
시간 스케일에 걸쳐 의미 있게 침식할 수 없습니다.

## Rotation & spin synthesis

DeWarf 2010 의 22 ± 3 일 광도 회전 주기는 태양 평균보다 약간 느립니다.
이는 α Cen A 가 태양보다 ~0.5 Gyr 더 나이가 많다는 점과 Skumanich
braking 법칙 P_rot ∝ √t 로 일관됩니다. asteroseismic 역해석 (Bazot
2007, de Meulenaer 2010, Bedding 2004) 으로는 p-mode 진동 스펙트럼이
주파수 분리 Δν = 105.9 ± 0.3 μHz, ν_max ~ 2200 μHz 로 검출되며, 특성
음향 시간 스케일 2π/Δν ≈ 2.6 h 는 태양의 5분 진동을 더 큰 반지름과
낮은 음속으로 스케일한 값과 비슷합니다.

차등 회전은 직접 분해되지 않지만 태양형으로, 적도가 극보다 ~20% 빠르게
회전할 것으로 예상됩니다. 회전축 경사는 잘 제약되지 않습니다. 시각
렌더링을 위해 NearStars 는 α Cen B 궤도면에 대한 시선 방향 기준 ~30°
기울어진 축을 채택했는데, 이는 오래된 이중성에서 무작위로 정렬된 자전축
가정과 일관됩니다.

## Visual styling

NearStars 렌더러에서 α Cen A 는 따뜻한 크림 G2V 별로 묘사됩니다. Sol
과 시각적으로 거의 구분되지 않지만 엄격한 태양형 `#fff8f0` 대신
`#fff4e8` 로 살짝 더 크림이 도는 색조를 코드화합니다. 순수한 태양 일치
에 대한 tie-break 선택이며, 이중성 페어 뷰에서 A 의 크림과 B 의 명확한
오렌지 색 대비가 시스템을 플레이어에게 즉시 알아보게 만들기 때문입니다.

지구에서 1.3 pc 거리에서 보면 겉보기 등급 V = 0.01 로 α Cen A 는 밤하늘
에서 가장 밝은 별 세 손가락 안에 듭니다. α Cen A 거주가능영역 후보 행성
(Wang 2022 모델 지구, 1.25 AU) 에서 보면 별이 각지름 0.5° 를 채웁니다.
지구에서 태양을 본 0.53° 보다 살짝 작은데, A 가 HZ 보다 더 멀리 있기
때문입니다.

~11-36 AU 분리 (궤도 위상에 따라) 의 동반자 B 는 원일점에서는 빛나는
K1V 점광원, 근일점에서는 ~0.04° 의 겉보기 항성 디스크로 보이는데,
α Cen A 행성에서 맨눈으로 분해되지는 않지만 깊은 하늘 망원경 뷰에서
인상적인 오렌지 "두 번째 태양"으로 보입니다. 79.91 년마다 일어나는
이중성 conjunction 은 극적인 정렬 이벤트를 만들어, α Cen B 행성에서 볼
때 A 가 잠시 B 의 디스크를 occult 하는 모습이 보입니다. 반대로 B 가
앞에 올 때는 A 의 corona 가 드러나는데, 이 드문 이벤트가 cfg
`visual_companion_event_corona_visible_during_b_eclipse` 필드로 표시됩니다.

흑점, faculae, prominence 는 활동 극대기 동안 태양형 스케일로 렌더링
되며, 19 년마다 피크를 찍습니다 (Robrade 2016 X 선 사이클이 주, 11 년
색채권 sub-cycle 이 더 빠른 진폭 변조로 들어옴).

## Bibliography

### Read (visual-informative, drove decisions above)

- **Pourbaix D. & Boffin H. M. J. 2016** — *Parallax and masses of α
  Centauri revisited*, A&A 586, A90 (`2016A&A...586A..90P`,
  arXiv:1601.01636). ESO/HARPS 아카이브를 이용한 분광 이중선 시각이중성
  fit. 수정된 궤도 시차 743 mas, M_A = 1.1055 ± 0.0039 M☉, M_B =
  0.9373 ± 0.0028 M☉. 시스템 역학질량의 기준을 설정합니다.
- **Kervella P. et al. 2017** — *The radii and limb darkenings of α
  Centauri A and B*, A&A 597, A137 (`2017A&A...597A.137K`,
  arXiv:1610.06185). H 밴드 VLTI/PIONIER 간섭계. 각지름 θ_LD(A) =
  8.502 ± 0.038 mas, θ_LD(B) = 5.999 ± 0.025 mas. 수정된 시차로 R_A =
  1.2234 ± 0.0053 R☉, R_B = 0.8632 ± 0.0037 R☉ 유도.
- **Joyce M. & Chaboyer B. 2018** — *Classically and Asteroseismically
  Constrained 1D Stellar Evolution Models of α Centauri A and B*,
  ApJ 864, 99 (`2018ApJ...864...99J`, arXiv:1806.07567). 고전 + p-mode
  제약을 동시에 만족시키는 DSEP 진화 모델. 31 viable model pairs, 시스템
  나이 5.3 ± 0.3 Gyr.
- **DeWarf L. E. et al. 2010** — *X-Ray, FUV, and UV Observations of α
  Centauri B: Determination of Long-term Magnetic Activity Cycle and
  Rotation Period* (`2010ApJ...722..343D`). A 와 B 모두의 색채권과
  코로나 모니터링. 회전 주기 22 ± 3 d (A), 36–40 d (B). B 의 8.1 년
  색채권 사이클과 A 의 태양형 ~19 년 사이클. **arXiv 프리프린트 없음**.
  Tier A manual followup. 값은 ApJ abstract 와 DB Phase 2 attribution
  에서 가져옴.
- **Robrade J. et al. 2016** — *Coronal activity cycles in action —
  X-rays from α Centauri A/B*, A&A 596, A53 (`2016A&A...596A..53R`,
  arXiv:1612.06570). XMM-Newton + Chandra 모니터링. A 의 ~19 년 코로나
  사이클 확인, log L_X 진폭 약 4 배.
- **Beichman C. et al. 2025** — *Worlds Next Door: A Candidate Giant
  Planet Imaged in the Habitable Zone of α Centauri A. I*
  (`2025NatAs.tmp.../...`, arXiv:2508.03814) 및 **Sanghi A. et al.
  2025** *Worlds Next Door II* (arXiv:2508.03812). ~1.5 AU 점원 후보의
  JWST/MIRI 직접 촬영. 거대 행성 후보 "S1" 으로 분류. 추후 follow-up
  대기 중 미확인 상태.

### Read (context / methodology, not directly decision-driving)

- **Porto de Mello G. F. et al. 2008** — *Photospheric, chromospheric,
  and coronal activity of α Cen A* (`2008A&A...488..653P`). A 의
  canonical [Fe/H] = +0.24 ± 0.03 과 Teff = 5847 ± 27 K 를 정의.
- **Bedding T. R. et al. 2004** — *Oscillation frequencies and mode
  lifetimes in α Centauri A* (`2004ApJ...614..380B`,
  arXiv:astro-ph/0406471). 28 개 p-mode 검출. A 의 asteroseismic 제약
  표를 설정.
- **de Meulenaer P. et al. 2010** — *Core properties of α Cen A
  using asteroseismology* (`2010A&A...523A..54D`, arXiv:1009.1237).
  44 개 p-mode. Δν = 105.9 μHz, ν_max ≈ 2200 μHz 로 정련.
- **Bigot L. et al. 2006** — α Cen B granulation 의 VLTI/VINCI 3D 복사-
  유체역학 제약. Kervella 2017 §4 를 통해 인용.
- **Wang H. S. et al. 2022** — *A Model Earth-sized Planet in the
  Habitable Zone of α Centauri A/B* (`2022ApJ...927..134W`,
  arXiv:2110.12565). cfg 의 거주가능영역 지오메트리를 framing. A 의
  hot edge 1.25 AU, cold edge 1.85 AU.
- **Quarles B. et al. 2022** — *Milankovitch cycles for a
  circumstellar Earth-analogue within α Centauri-like binaries*
  (arXiv:2108.12650). A 또는 B 의 행성에 대한 이중성 perturbation
  obliquity 진동 envelope 설정.

### Read (instrument / non-cfg-decisive)

- **Salmon S. J. A. J. et al. 2021** — α Cen AB asteroseismic 제약을
  최신 진동 코드로 재조사 (arXiv:2011.14932).
- **Akeson R. et al. 2021** — *Precision Millimeter Astrometry of the
  α Centauri AB System* (arXiv:2104.10086). Sub-milliarcsecond
  위치. 2025년 이전 ALMA 캠페인.
- **Krishnamurthy A. et al. 2021** — α Cen A, B 주위 ASTERIA 통과 탐색
  (`2021AJ....161..275K`). 미검출 한계.
- **Spada F. et al. 2019** — *Entropy calibration of the radii of
  cool stars: α Cen A and B* (arXiv:1909.00701). Kervella 2017 +
  Joyce 2018 의 그림을 엔트로피 기반 예측으로 검증.

### Not read — no arXiv preprint or low-priority (~50 papers)

학회 abstract (EPSC/AGU/DPS), 항성 간 추진 제안 (Heller 2017 photon
sail, Forgan 2018 Project Lyra), SETI / 레이저 방출 탐색 (Marcy 2022,
Tusay 2022, Saide 2023) 등은 cfg 결정에 영향이 없습니다. 전체 필터된
bib 는 `docs/phase3/_bib/alpha-centauri-a.yaml` 에 `status: skipped`
주석으로 보존됩니다.

## Open items for follow-up

- **DB erratum, Joyce & Chaboyer 2018 의 `age_measurements` recommended
  entry.** DB 는 `value_gyr = 4.81 ± 0.5` 를 저장하지만 논문 표제값은
  **5.3 ± 0.3 Gyr** 입니다. 4.81 숫자는 중간 단계 fit (논문이 여러 물리
  configuration 을 제시) 을 옮긴 것으로 보입니다. DB attribution 을
  논문 표제값으로 정정해야 합니다.
- **Beichman/Sanghi 2025 "S1" 거대 행성 후보.** 2026 년 follow-up 에서
  ~1.5 AU 에 묶인 동반자가 확정되면 새로운 Decisions 항목
  `circumstellar_planet_present: true` 가 필요하며, cfg `has_companion_b`
  (현재 없음) 가 추가되어야 합니다.
- **고정밀도 granulation 패턴.** STAGGER 시뮬레이션은 cfg 스칼라
  `limb_darkening_alpha_h` 가 모델링하지 않는 미세한 limb-to-center 대비
  변동을 예측합니다. 매우 가까운 fly-by 시퀀스를 위해 3D 구조를 잡는
  cfg 변형을 후속에 만들 수 있습니다.
- **게임 epoch (J2000.0) 의 사이클 위상.** 19 년 X 선 사이클과 색채권
  활동 사이클은 현재 cfg 에서 위상 동기화돼 있지 않습니다. Robrade 2016
  사이클 시작 epoch 를 기준으로 위상을 맞추면, 활동 driven CME 플럭스가
  실시간 게임 진행과 함께 추적될 수 있습니다.

## Related

- [alpha-centauri-b](alpha-centauri-b.md) — 79.91 년 주기 시각이중성 짝, K1V 동반성.
- [proxima-cen](proxima-cen.md) — 약 13 000 AU 거리의 광폭 공통 고유운동 동반성 (M5.5Ve 플레어성). capture 대 coeval 기원 미해결 (Feng & Jones 2018).
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — α Cen AB 는 Kepler→ICRS 파이프라인의 **정전 워크드 예시**입니다 (§9).
- [methodology](../reference/methodology.md) — Decisions 표 스키마의 원본.
- [rex-data-comparison](../reference/rex-data-comparison.md) — §3–4 가 α Cen 항성 파라미터, §5 가 REX 가 모델하지 못한 AB↔Proxima 토폴로지 갭을 다룹니다.
- [stellarium-binary-orbit-comparison](../../plans/stellarium-binary-orbit-comparison.md) — Stellarium 과의 α Cen 궤도 컨벤션 교차 검증 (Hilditch/Pourbaix 일치 확인).
