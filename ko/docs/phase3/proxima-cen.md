<!-- Proxima Centauri Phase 3 합성: cfg-ready 결정과 근거 -->
# Proxima Centauri — Phase 3 Synthesis

Proxima Centauri (α Cen C, GJ 551) 는 태양에 가장 가까운 별로 1.301 ±
0.001 pc 에 있습니다. α Cen AB 쌍에 투영 분리 ~13 000 AU 로 중력적으로
묶여 있으며, 추정 궤도 주기는 약 547 000 년입니다 (Kervella 2017
astrometry). 분광형 M5.5Ve flare star 로 질량은 단 0.122 M☉, 반지름은
0.141 ± 0.011 R☉ (Demory et al. 2009 VLTI/VINCI 간섭계), 유효 온도 2904 ± 51 K 이며,
주계열의 깊은 빨강 끝에 자리합니다. 확인된 행성을 2개 (Proxima b —
Anglada-Escudé 2016, Proxima d — Faria 2022, Suárez Mascareño et al.
2025 확정) 와 5.2 AU 의 sub-Neptune 후보 Proxima c (3σ 수준에서 아직
미확정) 를 거느립니다.

0.27 pc 떨어진 조용한 α Cen AB 쌍과 비교하면, Proxima 는 극적으로 더
에너지가 크고 변동이 심한 별입니다. 83.5 ± 0.5 일의 회전 주기 (Benedict
et al. 1998 HST 광도. 최근 Suárez Mascareño 연구도 ~83 일을 뒷받침하며,
SM2020 은 83.2 일을 채택하고 SM2025 GP fit 은 83.2 ± 1.6 일을 줍니다) 는
M 왜성으로서는 느린 편이며, 오래된 나이와 일관됩니다. 오래되고 느리게
도는 별이라 정상상태 색채권 지표로 보면 활동도는 중간에서 약한 수준에
그칩니다. log R'HK ≈ −5.65 ± 0.17 (Suárez Mascareño 외 2016 Ca II H&K)
입니다. 그럼에도 flare 는 여전히 빈번하며, Hα 가 자주 방출 상태에 있고,
moderate ~0.6 kG 평균 표면장 (Reiners & Basri 2008; Reiners 2022 CARMENES) 과
~0.2 kG 의 주로 poloidal 대규모장 (Klein 2021 SPIRou ZDI) 이 측정됐습니다. X 선, FUV, UV 출력은 약 7 년 주기로 변동하며
(Wargelin 2024) flare 가 빈번합니다. Vida 2019 의 TESS 관측이 광도
잡음 위에서 여러 flare/일 을 분해했고, 그 가운데 quasi-periodic
oscillation 을 decay 단계에서 보이는 거대 superflare 도 포함됩니다.
Fuhrmeister 2022 (arXiv:2204.09270) 의 X 선 + FUV 동시 flare 분광은
이 사건들의 코로나 – 색채권 동시 반응을 기록합니다.

Proxima 가 α Cen AB 와 어떤 관계를 갖는가는 중력 결합이 시사하는 만큼
확실하지는 않습니다. Feng & Jones 2018 (arXiv:1709.03560) 가 조우
역학을 모델링한 결과, Proxima 가 α Cen AB 시스템과 공동 형성된 것이
아니라 포획됐을 수 있음을 결론지었습니다. 시스템 무게중심 운동학 일치는
양쪽 형성 시나리오를 모두 살려둡니다. 나이는 ~4.85 Gyr (DB Phase 2
attribution) 로 추정되어 α Cen AB 와 비슷하지만 불확실성이 상당합니다.

**NearStars 시나리오 선택. ~83 일 회전, moderate ~0.6 kG 평균 표면장 (sub-kG 대규모 쌍극자), 7 년 활동
사이클, 빈번한 superflare 를 가진 저질량의 깊은 빨강 M5.5Ve flare star
로, 시각적으로는 강한 빨강 연속체와 Hα flare 의 잦은 brightening,
근접 행성에서 본 가시 광채를 강조합니다.** 18 cfg 픽 가운데 16 은
canonical-aligned, 2 는 tie-break 입니다 (limb darkening 보간 + 특정
flare hex 색상).

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M5.5Ve | high | Hawley 1996. DB |
| `mass_msun` | 0.1221 | high | Mann 2015 M–K 관계. DB recommended |
| `radius_rsun` | 0.141 ± 0.011 | high | Demory et al. 2009 (VLTI/VINCI 간섭계) |
| `teff_k` | 2904 ± 51 | high | Passegger et al. 2019 고분해능 분광 (SM2020/2025 채택값 2900 ± 100 과 일치) |
| `luminosity_lsun` | 0.001567 | high | R, Teff 로 유도 |
| `metallicity_fe_h_dex` | +0.21 | medium | Passegger 2019 H 밴드 |
| `age_gyr` | 4.85 | medium | 역학 + 활동 proxy. Feng & Jones 2018 capture vs. coeval 모호 |
| `rotation_period_days` | 83.5 ± 0.5 | high | Benedict et al. 1998 (HST 광도). 최근 SM 도 ~83 일을 뒷받침 (SM2020 은 83.2 채택. SM2025 GP 83.2 ± 1.6). Zapatero Osorio 2026 (`2605.22925`) 의 ESPRESSO 광구 측정값은 84.9 ± 0.6 일로 ~2σ 이내에서 일치. 기존 값 유지 |
| `activity_log_rhk` | −5.65 ± 0.17 | high | Suárez Mascareño 외 2016 (Ca II H&K. SM2020 은 −4.98 로 재보정) — 오래되고 느린 자전성, 정상상태 활동도 낮음에서 중간 |
| `activity_cycle_years` | 7 | medium | Wargelin 2024 X 선 + UV + 광학 사이클 |
| `x_ray_log_lx_cgs_quiescent` | 27.0 | medium | Damonte 2026 XMM 시간 분해 스펙트라 |
| `x_ray_log_lx_cgs_flare_peak` | 28.5 | medium | Fuhrmeister 2022 X 선 + FUV 동시 피크 |
| `magnetic_dipole_strength_kG` | 0.135 | high | Klein 외 2021 — SPIRou ZDI 대규모 쌍극자 성분 (135 G. 대규모장 ~200 G, 주로 poloidal) |
| `magnetic_total_field_kG_rms` | 0.6 | high | Reiners & Basri 2008 / Reiners 2022 — 평균(소규모) 표면장 Bf ≈ 0.6 kG. moderate, 긴 ~83 일 회전과 일관 |
| `flare_rate_per_day_total` | 1.49 | high | Vida 2019 TESS — ≈ 50 d 에 72 events (에너지 범위 10²⁹–10³² erg) |
| `flare_rate_superflare_per_year` | 3 (≥ 10³³ erg); 0.5 (≥ 10³⁴ erg) | high | Vida 2019 TESS — §4 의 누적 flare 빈도 분포로부터 명시 |
| `orbital_role_around_acen_ab` | ~13 000 AU 에 묶임. P ≈ 547 000 yr | medium | Kervella 2017 astrometric 추적. Feng & Jones 2018 capture 분석 |
| `limb_darkening_alpha_h` | ~0.4 | low | Tie-break. Proxima 에 직접 측정값 없음. M 왜성 모델 grid (Claret 2018) 에서 보간. interesting-first 룰 에 따른 interesting-first 로 미세한 시각 변동 |
| `visual_surface_tint_hex_primary` | `#ffcc75` (옅은 따뜻한 주황, M5.5V) | high | 실제 광구 색. 2904 K 에서의 Pickles 1998 관측 late-M SED 를 공유 CIE→sRGB 엔진 (`scripts/refs/stellar_photospheric_color.py`) 으로 적분하고 peak-channel 정규화한 값. 옅은 따뜻한 주황으로, 2904 K 흑체가 그럴듯한 1차 근사이며 TiO/VO/H₂O 밴드는 표시 색도를 약간만 이동시킵니다 (큰 효과는 가시 색조가 아니라 색지수에 나타남). 더 이른 분광형 M 왜성들보다 아주 살짝 더 따뜻할 뿐이며 (파란 채널이 조금 낮음), 모두 옅은 따뜻한 주황 계열입니다. (앞서의 렌더-포화된 brick-red 짐작값 `#c54c2a` 를 대체합니다.) |
| `visual_flare_color_hex` | `#ff5e2a` (Hα 우위 광학 flare 와 광대역 연속체 brightening) | medium | Tie-break. Vida 2019 + Anglada-Escudé 2016 보충 flare 스펙트라. 게임 내 어두운 빨강 quiescent 연속체 대비 가시성을 위해 특정 hex 선택 |
| `stellar_color_temp_k` | 2904 | high | 유도 |

## Surface synthesis

Proxima Centauri 의 광구는 NearStars 카탈로그에서 가장 어둡고 빨간
편입니다. Teff 2904 K, 0.141 R☉ 이며 총 광도는 단 0.00157 L☉ — 태양의
약 1/640 입니다. 6500 Å 이하의 가시 연속체는 TiO, VO, 물 밴드로 크게
가라앉아 있으며, 복사 출력 대부분이 근적외선 ~ 중적외선으로 나옵니다.
H 밴드 광구 구조는 1D 대기로 잘 모델링되지 않으며 (M 왜성 모델 대기가
깊은 빨강 분자 밴드를 검증 범위 밖으로 외삽함), cfg
는 phenomenological 어두운-에지 모델에 대한 tie-break 으로 Claret 2018
M 왜성 grid 에서 보간한 limb-darkening exponent α ≈ 0.4 를 잠정적으로
채택합니다.

extreme close-up 렌더링에서 광구는 sub-arcsecond 수준으로 granulation
이 분해됩니다. 전형적인 M 왜성 granulation 셀은 ~30 km 너비 (압력 스케일
높이와 스케일). 활동 극대기 동안 흑점 면적은 TiO 밴드 깊이 모델링
(Berdyugina 2017 리뷰) 기반으로 5–10% 로 추정됩니다. faculae 와 밝은
plage 도 보이지만 더 이른 분광형 별보다 통합 광도에 적게 기여합니다.

## Atmosphere synthesis

Proxima 의 색채권과 코로나가 관측 가능한 에너지 출력의 대부분을
지배합니다. Reiners & Basri 2008 과 Reiners 2022 (CARMENES) 가 moderate
평균 표면장 Bf ≈ 0.6 kG 를, Klein 2021 (SPIRou ZDI) 이 ~0.2 kG 주로 poloidal
대규모장과 ~0.135 kG 쌍극자 성분을 측정했습니다. 이 자기 forcing 이 높은 UV / X 선 방출을 구동합니다. 정상상태
X 선 광도는 log L_X ≈ 27.0 cgs (Damonte 2026) 이며, flare 동안 한 자리
수 증가합니다 (Fuhrmeister 2022).

Flare 가 정의적 특징입니다. Vida 2019 (arXiv:1907.12580) 가 TESS 광도로
flare 분포를 특성화했습니다. 백색광 밴드의 전형적인 flare 진폭은
정상상태 위 0.01–0.1 등급으로, 10²⁹–10³² erg 에너지 범위에서 1.49 회/일
빈도를 보이며 (Vida 의 ≈ 50 d 동안 72 events), super-flare (≥ 10³³ erg)
는 연 ~3 회, ≥ 10³⁴ erg 사건은 2 년에 한 번 일어납니다. 기록된 가장 극적인
사건은 decay 단계에서 quasi-periodic oscillation 을 보이는데, flare loop
의 플라즈마 진동에 기인합니다. Burton et al. 2025 (arXiv:2503.21890) 가
ALMA 로 flare 검사를 밀리미터 파장까지 확장했고, 밀리미터-bright flare
의 발생률이 광학과 비슷함을 발견했습니다.

활동 사이클 — Wargelin 2017 가 ~15 년의 X 선과 광학 광도에서 처음
검출하고 Wargelin 2024 가 ~7 년으로 정련 — 은 평균 flare 비율과 흑점
유도 회전 변조 진폭을 함께 변조합니다. Anglada-Escudé 2016 도 Proxima b
발견에 사용된 HARPS + UVES timeseries 에 걸쳐 Hα 등가 폭에서 같은 변조를
기록합니다.

Proxima 행성계로의 대기 손실은 막대합니다. Garraffo et al. 2022
(arXiv:2211.15697) 는 b 거리에서의 항성풍 ram pressure 가 sub-Alfvénic
및 super-Alfvénic transit 동안 태양값의 10⁴ – 10⁶ 배 범위에 있다고
보입니다. 코로나 질량 방출은 Vida 2019 의 superflare 샘플에서 사건당
최대 10³⁴ erg 의 총 운동 에너지를 운반합니다.

## Rotation & spin synthesis

~83.5 일 회전 주기 (Benedict et al. 1998 HST 광도) 는 최근 광학 광도와
색채권 활동 tracer 로 뒷받침됩니다 — SM2020 은 83.2 일을 채택하고
SM2025 GP fit 은 83.2 ± 1.6 일을 줍니다. M5.5V 로서는 길어서 오래된 나이를
시사하고 (Newton 2018 M 왜성 gyrochronology 로부터 ≥ 4 Gyr), DB Phase
2 attribution 의 ~4.85 Gyr 와 일관됩니다. 차등 회전은 분해되지 않았습니다.

p-mode 의 asteroseismic 검출은 M 왜성에서는 불가능합니다. 표면 중력이
너무 높고 진동 진폭이 너무 낮기 때문입니다. 따라서 회전은 전적으로 흑점
변조와 색채권 tracer 에서만 옵니다. Suárez Mascareño 2020 §4 는 흑점
변조 진폭 대 평균 활동 패턴으로 회전축 경사를 i ≈ 35° 로 추정합니다.
Proxima b 의 궤도 경사가 90° 미만이라는 점과 일관됩니다.

## Visual styling

Proxima 는 NearStars 에서 옅은 따뜻한 주황빛의 M5.5V 로 렌더링됩니다.
광구 색조 `#ffcc75` 는 실제 적분-SED 색으로 2904 K 흑체에 가까우며,
적분된 SED 대부분이 V 밴드 피크 아래에 있습니다. Proxima b 의
0.0485 AU 에서 보면 Proxima 가 각지름 1.5° 를 채웁니다 (지구에서 본
태양 겉보기 지름의 약 3 배). Proxima d 의 0.029 AU 에서 보면 2.5°
입니다. 어두운 광도 (색도가 아니라 본질 밝기의 효과) 와 큰 각도
크기가 결합해 근접 거주가능영역 행성에서 본 시각적으로 인상적인
"거대한 따뜻한 색조의 별" 외관을 만듭니다.

Flare 는 일시적인 brightening 이벤트로 렌더링됩니다. 게임 내 flare cfg
키 `visual_flare_color_hex = #ff5e2a` 가 피크 방출 동안 색을 살짝
오렌지 쪽으로 옮겨, Hα 우세 광학 flare 스펙트럼 (Vida 2019 + Anglada-
Escudé 2016 스펙트라) 을 모방합니다. Superflare (~3 회/년 의 10³³ erg,
~0.5 회/년 의 10³⁴ erg) 는 수십 분간 1–2 등급 brightening 이벤트를
만들며, QPO 변조가 광도 decay tail 에서 보입니다.

코로나는 정상상태 동안 희미한 푸른빛 halo 로 렌더링되며, 7 년 사이클의
X 선 활성 단계에서 극적으로 밝아집니다. 항성풍 streamer 는 직접 보이지
않지만, 인근 행성 대기에 대한 게임 내 우주환경 효과로 전파됩니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Demory B.-O. et al. 2009** — *Mass-radius relation of low and very
  low-mass stars revisited with the VLTI*, A&A 505, 205
  (`2009A&A...505..205D`, arXiv:0906.0602). VLTI/VINCI 간섭계
  R = 0.141 ± 0.011 R☉ — 추천 Proxima 반지름.
- **Passegger V. M. et al. 2019** — *The CARMENES search for exoplanets
  around M dwarfs. Photospheric parameters of target stars from
  high-resolution spectroscopy* (`2019A&A...627A.161P`,
  arXiv:1907.00807). 고분해능 분광 Teff = 2904 ± 51 K 와 H 밴드
  금속함량.
- **Suárez Mascareño A. et al. 2016** — *Characterization of the radial
  velocity signal induced by rotation in late-type dwarfs*
  (`2016A&A...595A..12S`, arXiv:1506.08039). GJ 551 의 Ca II H&K 활동
  지표 log R'HK = −5.65 ± 0.17 (SM2020 에서 −4.98 로 재보정).
- **Suárez Mascareño A. et al. 2020** — *Revisiting Proxima with
  ESPRESSO* (`2020A&A...639A..77S`, arXiv:2005.12114). ESPRESSO RV
  모니터링. 회전 주기 ~83.2 d 채택 (측정값 87 ± 12 d). 재보정된 활동
  인덱스 timeseries.
- **Suárez Mascareño A. et al. 2025** — *Diving into the planetary
  system of Proxima with NIRPS: Breaking the m/s barrier*
  (`2025A&A...700A..11S`, arXiv:2507.21751). Proxima b 의 현재 best
  궤도 fit (e ≈ 0, P = 11.18465 d, Msini = 1.055 M⊕) 과 Proxima d
  확정. GP 회전 주기 83.2 ± 1.6 d.
- **Benedict G. F. et al. 1998** — *Photometry of Proxima Centauri and
  Barnard's Star Using Hubble Space Telescope Fine Guidance Sensor 3*,
  AJ 116, 429 (`1998AJ....116..429B`). HST/FGS3 광도 회전 주기
  83.5 ± 0.5 d — 추천 Proxima 회전 주기.
- **Anglada-Escudé G. et al. 2016** — *A terrestrial planet candidate
  in a temperate orbit around Proxima Centauri*, Nature 536, 437
  (`2016Natur.536..437A`, arXiv:1609.03449). Proxima b 의 원래 발견.
  supplementary Hα flare 빈도 측정.
- **Faria J. P. et al. 2022** — *A candidate short-period sub-Earth
  orbiting Proxima Centauri*, A&A 658, A115 (`2022A&A...658A.115F`,
  arXiv:2202.05188). P = 5.122 d, Msini = 0.26 M⊕ 의 Proxima d 후보.
- **Reiners & Basri 2008 / Reiners et al. 2022 / Klein et al. 2021** —
  Proxima 자기장. Reiners & Basri 2008 (`2008A&A...489L..45R`,
  arXiv:0808.2986) 과 Reiners 2022 (`2022A&A...662A..41R`,
  arXiv:2204.00342, CARMENES) 는 moderate 평균 표면장 Bf ≈ 0.6 kG 를,
  Klein 2021 (`2021MNRAS.500.1844K`, arXiv:2010.14311, SPIRou ZDI) 은
  ~0.2 kG 주로 poloidal 대규모장과 ~0.135 kG 쌍극자를 측정. (자기장
  측정이 없는 Reiners 2018 CARMENES 스펙트럼 atlas `1711.06576` 로의
  기존 오인용을 대체.)
- **Vida K. et al. 2019** — *Flaring Activity of Proxima Centauri from
  TESS Observations*, ApJ 884, 160 (`2019ApJ...884..160V`,
  arXiv:1907.12580). Flare 통계, QPO super-flare, 연 3 회의 superflare.
- **Fuhrmeister B. et al. 2022** — *The high energy spectrum of
  Proxima Centauri simultaneously observed at X-ray and FUV
  wavelengths*, A&A 663, A119 (arXiv:2204.09270). 코로나 + 색채권
  flare 응답.
- **Wargelin B. J. et al. 2024** — *X-Ray, UV, and Optical
  Observations of Proxima Centauri's Stellar Cycle*, A&A in press
  (arXiv:2411.04252). 정련된 7 년 활동 사이클.
- **Damonte A. et al. 2026** — *Time-resolved X-ray spectra of
  Proxima Centauri as seen by XMM-Newton* (arXiv:2512.18011).
  정상상태 X 선 분광과 사이클 변조.
- **Burton K. et al. 2025** — *The Proxima Centauri Campaign: First
  Constraints on Millimeter Flare Rates from ALMA*
  (arXiv:2503.21890). mm 밴드 flare 발생률.

### Read (context / methodology, not decision-driving)

- **Feng F. & Jones H. R. A. 2018** — *Was Proxima captured by α
  Centauri A and B?* (arXiv:1709.03560). 궤도 역사 역학.
- **Kervella P. et al. 2017** — *Proxima's orbit around α Centauri*,
  A&A 598, L7 (arXiv:1611.03495). 결합 삼중성을 확인하는 astrometric
  추적.

### Read (instrument / non-cfg-decisive)

- **De Luca P. et al. 2024** — Proxima b 지구 analog 의 오존-기후 동역학
  (arXiv:2404.17972). Proxima-b 합성에 재사용되는 대기 화학 framework.
- **Boldog Á. et al. 2024** — 암석 HZ 행성의 물 함량 모델링
  (arXiv:2312.01893). Proxima-b 내부 합성에 교차 인용.

### Not read — no arXiv preprint or low-priority (~150 papers)

- **Proxima 회전/사이클의 DeWarf-equivalent.** 불필요 (Suárez Mascareño
  2020 + Wargelin 2024 가 현재 정밀도로 같은 관측 base 를 커버).
- 학회 abstract, SETI / 레이저 통신 타겟팅, 항성 간 미션 제안 등은
  `docs/phase3/_bib/proxima-cen.yaml` 에 `status: skipped` 주석으로
  보존됩니다.

## Stellar wind / astrosphere

Proxima 는 **조밀한 astrosphere** 를 가집니다 — 약한 항성풍 (Ṁ ≤ 0.2 Ṁ⊙
상한, Wood 2001) 이 국소 ISM 을 겨우 **≲55 AU** 에서 막아냅니다. 방사선
레이어에서 결정적인 점은 이것입니다. Proxima 는 색채권 지표로 보면
정적으로 보이지만 (log R'HK 가 M 왜성 활동도를 과소 대변함), 사실 격렬한
**flare star** 라서 승무원에게 영향을 주는 입자 방사선은 태양보다 훨씬 더
가혹합니다 — 항성풍이 아니라 flare 가 지배합니다. 활동도는 ~7 yr 주기로
순환하고 (Wargelin 2017), α Cen 과 같은 국소 성간 흐름을 공유합니다
(V_ISM ≈ 25 km/s).

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `solar_cycle_yr` | 7 | medium | Wargelin 2017 (ASAS V-band + X-ray/UV) |
| `stellar_wind_mass_loss_solar` | ≤ 0.2 (upper limit) | medium | Wood 2001 astrospheric Lyα |
| `local_ism_inflow_speed_kms` | ~25 | medium | Wood 2005 (LIC. α Cen 과 같은 흐름) |
| `astrosphere_standoff_au` | ≲ 55 (upper bound) | medium | 120·√(Ṁ_rel)·(V_⊙/V_ISM), Ṁ 상한에서. 태양과 같은 항성풍 속도 (V_⊙ ≈ 400 km/s, Wood et al. 2002/2005 의 고정 속도 가정) 를 전제하며, 별마다 Ṁ 과 V_ISM 만 달라집니다 |
| `stellar_radiation_surface_relative_sun` | ~5 | medium | 정온 L_X 가 태양의 0.3–2× 로 측정됨 (Wargelin R_X −4.4; NEXXUS 27.22). 그 위에 flare 가중 boost (5-mmag flare ~63회/일, U-band ~1.4회/시간). 정온-만 canonical 대안: ~0.3 |
| `astrosphere_apex_ra_deg` / `_dec_deg` | ~185 / +42 | low | 6D astrometry 대 LIC. **plugin-only** |

## Open items for follow-up

- **Proxima c (5.2 AU 의 sub-Neptune 후보).** Damasso 2020 + Benedict
  2020 이 세 번째 행성에 대한 astrometric + RV 증거를 보고했지만,
  3σ 신뢰도 임계치를 아직 넘지 못했습니다. 확정되면 새 `has_planet_c`
  Decisions 행이 필요하며, 현재 cfg 는 행성을 빼놓고 갑니다.
- **활동 영역 위도 분포.** Suárez Mascareño 2020 §4 의 경사 i ≈ 35°
  는 흑점 위도를 분해하지 않습니다. 향후 Doppler-imaging 캠페인이
  Proxima 의 활동 영역이 주로 적도형 (태양처럼) 인지 극형 (일부 빠른
  자전성처럼) 인지를 제약할 수 있습니다.
- **포획 vs. 공동 형성 기원.** Feng & Jones 2018 가 구분하지 못합니다.
  나이에 대한 함의 (4.85 Gyr 공동 형성 vs. 별 형성 영역 조우에서
  포획됐다면 잠재적으로 훨씬 어림) 가 cfg `age_gyr` 신뢰도로 전파됩니다.
  향후 Gaia DR4 astrometric 해가 조우 역학을 더 타이트하게 할 수
  있습니다.

## Related

- [alpha-centauri-a](alpha-centauri-a.md), [alpha-centauri-b](alpha-centauri-b.md) — 약 13 000 AU 거리의 광폭 공통 고유운동 동반성 (P ≈ 547 kyr; Kervella 2017). capture 대 coeval 기원은 여전히 미해결 (Feng & Jones 2018).
- [proxima-cen-b](proxima-cen-b.md), [proxima-cen-d](proxima-cen-d.md) — 확인된 행성계. b 는 HZ 암석 행성, d 는 USP sub-Earth.
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — Proxima 가 AB 무게중심을 도는 외곽 궤도는 hierarchical/static-CPM 의 정전 예시입니다 (§6).
- [methodology](../reference/methodology.md) — DB 스키마 원본.
- [rex-data-comparison](../reference/rex-data-comparison.md) — §3 Proxima T_eff 는 Phase 3 → REX 의 주요 불일치 지점 (3498 K 대 3042 K, NS 는 Suárez Mascareño 2025 사용).
