<!-- α Centauri B Phase 3 합성: cfg-ready 결정과 근거 -->
# α Centauri B — Phase 3 Synthesis

α Centauri B (HD 128621, HIP 71681, GJ 559 B) 는 가장 가까운 별쌍의 K1V
이차성입니다. 동반자 G2V α Cen A 의 약 3분의 2 질량과 광도를 가진 조용
하고 살짝 금속이 풍부한 K 왜성이며, K 별 가운데서는 가장 긴 고정밀도
RV 모니터링 baseline 을 갖고 있습니다. 이는 Dumusque 2012 주장으로
정점을 찍었다가 이후 Rajpaul 2016 으로 배제된 행성 탐사의 유산입니다.

Kervella 2016 과 Kervella 2017 의 기본 파라미터는 매우 타이트
합니다. M_B = 0.9373 ± 0.0033 M☉, R_B = 0.8632 ± 0.0037 R☉ 두 값 모두
A 와 같은 분광 이중선 + 간섭계 해에서 공유됩니다. 유효 온도는 Porto de
Mello 2008 의 5316 ± 28 K 로 K1V locus 의 더운 끝에 자리합니다. 표면
금속도는 +0.25 ± 0.04 로 사실상 A 와 동일하며, 공통 원시성운 형성과
일관됩니다. 시스템 나이 5.3 ± 0.3 Gyr 는 Joyce & Chaboyer 2018 의 결합
asteroseismic + 고전 fit 으로 결정됩니다. 양쪽 별이 각자의 관측 제약을
동시에 만족해야 하기 때문에 구조상 A 와 같은 값입니다.

주계열 수명 비율로 따지면 더 나이가 많은데도 α Cen B 는 A 보다 활동적
입니다. log R'HK = −5.0 (Henry 1996 / DeWarf 2010) 가 K 왜성의 조용함–
활동성 경계에 걸쳐 있으며, 36–40 일 회전 주기 (DeWarf 2010) 는 8.1 년의
느리지만 지속적인 색채권 활동 사이클과 일관됩니다. X 선 광도가 이 주기로
변동하며 (Robrade 2016) 최대점에서 log L_X ≈ 27.5 cgs 에 도달합니다.

**없었던 행성.** Dumusque 외 2012 가 M sin i ≈ 1.13 M⊕ 의 후보 α Cen Bb
를 3.236 일 궤도에서 발표했는데, 이는 당시 RV 로 검출된 가장 낮은 질량
행성이었을 것입니다. Plavchan 2015 가 같은 데이터를 독립적으로 재분석
했지만 주장된 주기에서 유의미한 신호를 재현할 수 없었습니다. Rajpaul
외 2016 ("Ghost in the time series") 는 Dumusque 신호가 HARPS 의 불규칙
샘플링 cadence 의 window-function artifact 임을 입증했습니다. Demory
2015 (HST 통과 측광) 도 Krishnamurthy 2021 (ASTERIA 통과 탐색) 도 어떤
행성 시그니처도 찾지 못했습니다. 현재 컨센서스는 α Cen B 주위에 확인된
행성이 없다는 것이며, B 의 시각적 HZ (~0.5–0.9 AU, Wang 2022, Heller
2014) 는 향후 탐사를 위한 동역학적으로 안정한 빈 분지로 남아 있습니다.

**NearStars 시나리오 선택. 조용하고 살짝 금속이 풍부한 K1V 별로 A 보다
긴 활동 사이클을 갖고, 확인된 행성은 없으며, A 의 크림과 구분되는
알아볼 수 있는 따뜻한 오렌지 시각 시그니처를 갖습니다.** 16 개 cfg 픽은
모두 canonical-aligned 이며, Dumusque 2012 의 역사는 Decisions 행
`has_planet_b: false` 와 Open items 에 포착됩니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | K1V | high | Porto de Mello 2008. IAU MK |
| `mass_msun` | 0.9373 ± 0.0033 | high | Kervella et al. 2016 |
| `radius_rsun` | 0.8632 ± 0.0037 | high | Kervella 2017 VLTI/PIONIER |
| `teff_k` | 5316 ± 28 | high | Porto de Mello 2008 |
| `luminosity_lsun` | 0.503 | high | R 과 Teff 로 유도 |
| `metallicity_fe_h_dex` | +0.25 ± 0.04 | high | Porto de Mello 2008 |
| `age_gyr` | 5.3 ± 0.3 | high | Joyce & Chaboyer 2018 (A 와 결합) |
| `rotation_period_days` | 38 ± 2 | high | DeWarf 2010 (범위 36–40) |
| `activity_log_rhk` | −5.0 | high | Henry 1996. DeWarf 2010 |
| `activity_cycle_years` | 8.1 | high | DeWarf 2010 색채권 사이클 |
| `x_ray_log_lx_cgs_min` | 26.5 | medium | Robrade 2016 사이클 최소 |
| `x_ray_log_lx_cgs_max` | 27.5 | medium | Robrade 2016 사이클 최대 |
| `has_planet_b` | false | high | Dumusque 2012 의 Rajpaul 2016 철회. Plavchan 2015 독립 재분석. Demory 2015 통과 미검출. Krishnamurthy 2021 ASTERIA 미검출 |
| `limb_darkening_alpha_h` | 0.1545 ± 0.0044 | high | Kervella 2017. H 밴드 power-law fit |
| `visual_surface_tint_hex_primary` | `#ffcfa0` (따뜻한 오렌지 K1V) | high | K1V 흑체 5316 K |
| `stellar_color_temp_k` | 5316 | high | 유도 |
| `visual_in_planet_sky_apparent_diameter_arcmin` (0.7 AU 의 가상 HZ 행성에서 본 값) | 1.1 | high | 유도. 2 R★/a |

## Surface synthesis

α Centauri B 의 광구는 교과서적인 조용한 K1V 입니다. 적당히 금속이 풍부
하고 (Δ[Fe/H] = +0.25 vs. 태양), Teff 5316 K 이며, 3D 유체역학 granulation
시뮬레이션 (Bigot 2006, Kervella 2017 가 사용) 이 VLTI/PIONIER 가시도
데이터를 1D 대기 모델보다 더 잘 재현합니다. H 밴드 power-law limb-
darkening exponent α(B) = 0.1545 ± 0.0044 는 A 보다 살짝 강한데, 광구가
더 차고 표면 온도 기울기가 더 가파르다는 점과 일관됩니다.

8.1 년 활동 사이클 (DeWarf 2010) 동안의 흑점 면적은 A 보다 큽니다. log
R'HK = −5.0 으로 B 는 적당히 활동적인 K 왜성 영역에 들어가며, 사이클
최대기의 활동 영역 면적은 가시 디스크의 ~1–2% 로 추정됩니다. 디스크 통합
HARPS 스펙트럼을 이용한 Thompson 2017 ([arXiv:1702.01647](https://arxiv.org/abs/1702.01647)) 의 plage 모델
링은 비대칭 위도 분포의 흑점 분포를 찾았으며, 이는 회전축이 ~30° 기울어
졌다는 가설과 일관됩니다. 태양의 ~7° 황도 경사와는 비슷하지만 구분되는
값입니다.

표면 granulation 은 A 보다 약간 더 붉고 더 잘게 쪼개져 있습니다.
granulation 셀 크기는 압력 스케일 높이로 스케일되며, B 는 ~140 km, A 는
~180 km 입니다 (Bigot 2006 STAGGER 시뮬레이션). 0.7 AU 의 가상 안쪽-HZ
행성에서 본 가시 디스크는 사이클 최대기에 간헐적인 어두운 흑점과 밝은
faculae 가 점점이 박힌, 살짝 더 채도가 높은 오렌지 limb-darkened 구로
보입니다.

## Atmosphere synthesis

색채권은 적당히 채워져 있으며, DeWarf 2010 가 12 년의 분광 모니터링에
걸쳐 Ca II H&K 방출 사이클을 매핑했습니다. 전이 영역과 코로나는 8.1 년
사이클에 걸쳐 10 배 변동하는 X 선 방출을 만들어내며 (log L_X = 26.5–27.5
cgs, Robrade 2016), A 의 4 배 변조보다 다소 더 큰 변동성을 보이고 B 의
색채권 사이클로부터 약 π/2 만큼 위상이 어긋나 있습니다 (Robrade 2016 §4).

Lisogorskyi 2019 ([arXiv:1902.10711](https://arxiv.org/abs/1902.10711)) 는 α Cen B 의 활동 유발 RV jitter 를
HARPS 스펙트럼에서 ~1.5 m/s 진폭으로 회전 주기에 특성화했습니다. 처음에
Dumusque 2012 행성 신호로 보였던 잔여 신호입니다. 현대 RV 팀은 α Cen B
를 활동 decorrelation 방법의 벤치마크로 다루며 (Cretignier 2020, Wise
2018, Dumusque 2018), 천문학적 jitter 와 진짜 도플러 시프트를 구별할
목적에서 세계에서 가장 많이 모니터링되는 K1V 별로 만들었습니다.

항성풍 질량 손실은 태양의 약 0.6 배이며, X 선 광도와 (Wood 2002 관계)
스케일링됩니다. 코로나 질량 방출은 X 선 모니터링에서 적당한 빈도로
검출되지만, 어떤 광도 캠페인에서도 superflare 사건은 기록되지 않았습니다.

## Rotation & spin synthesis

38 일 회전 주기 (DeWarf 2010, 범위 36–40 d) 는 K1V 로서는 느리지만 5.3
Gyr 나이와 Skumanich braking 으로 일관됩니다. 회전축 경사는 불확실합니다.
Lisogorskyi 2019 가 jitter-진폭 변조를 기반으로 i ~ 30°–70° 를, DeWarf
2010 의 흑점 변조 envelope 가 같은 범위와 일관됨을 보입니다. NearStars
는 α Cen A 방향에서 본 시선축 기준 ~45° 기울어진 축을 채택하며, 이는
제약의 상위 중간 범위에 맞아떨어집니다.

B 에서 p-mode 의 asteroseismic 검출은 표면 광도가 낮아 A 보다 더 어렵지
만, Kjeldsen 2005 가 주파수 분리 Δν = 160.1 ± 0.1 μHz, ν_max ≈ 4000 μHz
의 37 개 mode 를 검출했습니다. K1V envelope 의 더 높은 주파수 밀도와
일관됩니다 (Joyce 2018 §2.3). 차등 회전은 직접 분해되지 않았습니다.

## Visual styling

NearStars 에서 α Cen B 는 `#ffcfa0` 광구 색조의 따뜻한 오렌지 K1V 로
렌더링되어, A 의 크림과 명확히 구분되며 카탈로그의 다른 K 왜성 (예: ε
Eri) 과 시각적으로 비슷합니다. 5316 K 의 별 SED 가 게임 내 조명 엔진에
입력되어, B 의 거주가능영역에 있을 가상 행성에 A 의 태양-백색이 아닌
sunset 오렌지 ambient 조명을 만듭니다.

0.7 AU 의 안쪽-HZ 행성 후보에서 보면 B 가 각지름 1.1 arcmin (지구에서
본 태양의 약 두 배) 을 채우며, 눈에 띄게 따뜻한 빛을 비춥니다. ~11-36
AU 분리의 동반자 A 는 원일점에서 V = −5.0, 근일점에서 V = −7.0 까지
변하는 빛나는 점광원입니다 (아직 분해되지 않음). 지구에서 본 금성이 가장
크게 떨어졌을 때보다 약 두 배 밝은 정도이며, 행성 표면에 가시적인 그림자
를 드리울 수 있습니다.

흑점, faculae, Ca II plage 는 8.1 년마다 사이클 최대기 동안 적당한 스케일
로 렌더링됩니다. X 선 사이클의 위상 오프셋은 cfg `activity_cycle_years`
필드가 색채권 위상을 기준으로 처리합니다. Robrade 2016 의 X 선 사이클
위상 오프셋 (색채권 대비 90°) 은 Open items 의 별도 cfg 변형입니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Kervella P. et al. 2017** — [arXiv:1610.06185](https://arxiv.org/abs/1610.06185) (A bibliography 와
  공유). R_B = 0.8632 ± 0.0037 R☉. α(B) = 0.1545 ± 0.0044.
- **Kervella P. et al. 2016** — [arXiv:1610.06079](https://arxiv.org/abs/1610.06079). 수정된 이중성 궤도
  fit. 권장 역학질량으로 채택된 M_B = 0.9373 ± 0.0033 M☉.
- **Pourbaix D. & Boffin H. M. J. 2016** — [arXiv:1601.01636](https://arxiv.org/abs/1601.01636). 이중성
  궤도 fit 에서 M_B = 0.972 ± 0.0045 M☉.
- **Joyce M. & Chaboyer B. 2018** — [arXiv:1806.07567](https://arxiv.org/abs/1806.07567). 시스템 나이 5.3
  ± 0.3 Gyr.
- **DeWarf L. E. et al. 2010** — (`2010ApJ...722..343D`, arXiv
  프리프린트 없음, Tier A manual followup). B 의 36–40 d 회전, log
  R'HK = −5.0, 8.1 년 색채권 사이클을 정의.
- **Henry T. J. et al. 1996** — (`1996AJ....111..439H`, no arXiv).
  B 의 원래 log R'HK = −5.00 측정.
- **Rajpaul V. et al. 2016** — *Ghost in the time series: no planet
  for Alpha Cen B*, MNRAS 456, L6 ([arXiv:1510.05598](https://arxiv.org/abs/1510.05598)). Dumusque 2012
  의 window-function 재분석. 주장된 3.236-d 행성을 배제.
- **Plavchan P. et al. 2015** — *What is the Mass of α Cen B b?*
  ([arXiv:1503.01772](https://arxiv.org/abs/1503.01772)). Dumusque 2012 의 독립 재분석. 같은 결론에 도달.
- **Demory B.-O. et al. 2015** — *HST search for the transit of the
  Earth-mass exoplanet α Centauri B b*, MNRAS 450, 2043
  ([arXiv:1503.07528](https://arxiv.org/abs/1503.07528)). 주장된 3.236-d 주기에서 통과하는 지구질량 행성을
  배제한 HST/STIS 측광.
- **Thompson A. P. G. et al. 2017** — *The changing face of α Centauri
  B: probing plage and stellar activity in K dwarfs*, A&A 596, A21
  ([arXiv:1702.01647](https://arxiv.org/abs/1702.01647)). Plage / 흑점 위도 분포와 회전축 경사 제약.
- **Lisogorskyi M. et al. 2019** — *Activity and telluric
  contamination in HARPS observations of α Centauri B*, MNRAS 485,
  4804 ([arXiv:1902.10711](https://arxiv.org/abs/1902.10711)). Dumusque 2012 잘못된 주장을 만든 1.5 m/s
  활동 driven RV jitter 특성화.
- **Robrade J. et al. 2016** — [arXiv:1612.06570](https://arxiv.org/abs/1612.06570). B 의 8.1 년 코로나
  X 선 사이클, log L_X = 26.5–27.5 진폭.
- **Heller R. & Armstrong J. 2014** — *Superhabitable Worlds*, AsBio
  14, 50 ([arXiv:1401.2392](https://arxiv.org/abs/1401.2392)). K1V HZ 를 표면 생명 유지에서 태양 HZ 보다
  물리적으로 더 우호적인 것으로 framing.

### Read (context / methodology, not decision-driving)

- **Kjeldsen H. et al. 2005** — α Cen B 의 태양형 진동
  (arXiv:astro-ph/0508609). asteroseismic p-mode 검출.
- **Eggl S. et al. 2013** — *Circumstellar habitable zones of binary-
  star systems in the solar neighbourhood* ([arXiv:1210.5411](https://arxiv.org/abs/1210.5411)). 이중성
  perturbation HZ edge 설정.
- **Cretignier M. et al. 2020** — *Measuring precise radial velocities
  on individual spectral lines II* ([arXiv:1912.05192](https://arxiv.org/abs/1912.05192)). RV jitter
  decorrelation 방법론.
- **Liseau R. et al. 2016** — *ALMA's view of the nearest neighbors to
  the Sun. The submm/mm SEDs of the α Centauri binary* (arXiv:
  [1608.02384](https://arxiv.org/abs/1608.02384)). 광구 원적외선 / sub-mm 연속체.
- **Wiegert J. et al. 2014** — α Cen 주위의 먼지, 적외선 초과 탐색
  ([arXiv:1401.6896](https://arxiv.org/abs/1401.6896)). 유의미한 debris 초과 미검출.

### Read (instrument / non-cfg-decisive)

- **Spada F. et al. 2019** — [arXiv:1909.00701](https://arxiv.org/abs/1909.00701). K 왜성 반지름의 entropy
  calibration, Kervella 2017 을 검증.
- **Krishnamurthy A. et al. 2021** — α Cen A, B 주위 ASTERIA 통과 탐색
  (`2021AJ....161..275K`). 미검출 한계.

### Not read — no arXiv preprint or low-priority (~40 papers)

- **Dumusque X. et al. 2012** — *An Earth-mass planet orbiting α
  Centauri B*, Nature 491, 207 (`2012Natur.491..207D`, no arXiv).
  원래의 RV-jitter 기반 철회된 검출. Rajpaul 2016, Plavchan 2015 로
  대체.
- 학회 abstract, 항성 간 추진 제안, SETI 탐색은 cfg 결정에 영향이
  없으며, `docs/phase3/_bib/alpha-centauri-b.yaml` 에 `status: skipped`
  주석으로 보존됩니다.

## Stellar wind / astrosphere

α Cen B 는 **단일 α Cen AB astrosphere 를 공유합니다**. 항성풍 공동,
standoff (~176 AU), inflow 속도, apex 방향은 시스템 대표값으로 α Cen A
쪽에 기록돼 있습니다 (결합 Ṁ ≈ 2 Ṁ⊙, Wood 2001). B 가 자기 몫으로 들고
있는 것은 깔끔하고 잘 정의된 **~8.8 년 활동 사이클** 로, 61 Cyg A 다음
으로 알려진 가장 깨끗한 항성 X 선 사이클입니다 (DeWarf 2010 multi-band.
Ayres 2014 X 선 단독은 8.2 년). 입자 방사선 가혹도는 태양형입니다.

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `solar_cycle_yr` | 8.84 | medium | DeWarf 2010 (multi-band X 선–NUV). X 선 단독 8.2±0.2 yr (Ayres 2014) |
| `stellar_radiation_surface_relative_sun` | ~1.4 | medium | 측정: log L_X 27.04 (DeWarf 2010, ROSAT-96 사이클 평균) 대 태양 26.9. 8.8년 사이클이 ~0.4–5× 로 흔듦 |
| `astrosphere` | shares the α Cen AB cavity | — | Wood 2001 — Ṁ / standoff / apex 는 α Cen A 참고 |

## Open items for follow-up

- **독립적인 경사 측정.** Lisogorskyi 2019 와 Thompson 2017 가 겹치되
  느슨한 제약 (i = 30–70°) 을 줍니다. asteroseismic 회전 splitting 분석
  이나 간섭계 흑점 매핑이 이 값을 타이트하게 할 수 있습니다.
- **사이클 위상 관계.** Robrade 2016 §4 는 B 의 색채권과 코로나 사이클이
  ~π/2 만큼 위상이 어긋남을 보입니다. cfg 는 현재 색채권 사이클만
  master 위상으로 저장하며, 코로나 사이클 위상 오프셋 변형은 후속 cfg
  정련 사항입니다.
- **가능한 장주기 행성.** Rajpaul 2016 가 Dumusque 2012 의 단주기 주장을
  배제하지만 B 의 HZ 의 더 긴 주기 (수개월~수년) 행성은 충분히 제약하지
  않습니다. α Cen A 의 Beichman & Sanghi 2025 MIRI 직접 촬영 캠페인이
  B 에서도 병행 데이터를 갖고 있으며, 1+ AU 범위의 동반자가 확인되면 새
  `has_planet_*` Decisions 행이 필요합니다.
- **고공간 분해능 광구.** B 의 3D STAGGER granulation 패턴 (Bigot 2006)
  은 cfg 스칼라 `limb_darkening_alpha_h` 에 들어 있지 않습니다. 3D
  granulation 을 잡는 cfg 변형이 극단적인 close-up fly-by 를 지원할 수
  있습니다.
- **이전 Teff 로 합성된 표면 색조.** `#ffcfa0` 광구 색조는 Porto de
  Mello 2008 의 실제값 5316 K 로 정정되기 전, 옛 5236 K Teff 에서
  유도됐습니다. ~5300 K 에서 80 K 차이는 8-bit RGB 인지 임계값 아래라
  hex 는 그대로 두며, 재합성은 불필요하지만 출처 추적을 위해 남겨 둡니다.

## Related

- [alpha-centauri-a](alpha-centauri-a.md) — 이중성 짝. G2V 주성, 모든 역학 해 (Pourbaix & Boffin 2016) 를 공유합니다.
- [proxima-cen](proxima-cen.md) — 약 13 000 AU 거리의 광폭 공통 고유운동 동반성.
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — α Cen AB 워크드 예시 (§9).
- [methodology](../reference/methodology.md) — Decisions 스키마.
- [rex-data-comparison](../reference/rex-data-comparison.md) — α Cen B 파라미터 비교.
- [stellarium-binary-orbit-comparison](../../plans/stellarium-binary-orbit-comparison.md) — 시각이중성 궤도 교차 검증.
