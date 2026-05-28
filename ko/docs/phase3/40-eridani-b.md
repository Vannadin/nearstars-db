<!-- 40 Eridani B Phase 3 합성. cfg-ready 결정과 근거 -->
# 40 Eridani B — Phase 3 Synthesis

40 Eridani B (HD 26976, WD 0413−077, EG 11) 은 5.01 pc 거리의 40 Eri
삼중계에서 호스트가 아닌 두 동반자 중 더 밝은 쪽으로, Sirius B 다음
가는 두 번째로 가까운 백색왜성입니다. K0.5 V 주성 40 Eri A 로부터
83″ 떨어진 V = 9.53 의 천체로, 맨눈으로 보이는 별과 시각적으로 가장
가까운 백색왜성이기도 합니다. M 왜성 40 Eri C 와 함께 230.09 년 주기의
시각 이중성을 이루며 (Mason, Hartkopf & Miles 2017), HST/FGS 에 정박한
이 시스템의 역학 해는 가까운 들녘 백색왜성 중 가장 정밀한 질량 측정을
제공합니다. **M = 0.573 ± 0.018 M☉** (Bond et al. 2017). 여기에
SED-fit 으로 R = 0.01308 ± 0.00020 R☉, log g = 7.957 ± 0.020,
Teff = 17,200 ± 110 K 를 묶으면 40 Eri B 는 CO-core 질량-반지름 관계
위에서 표준 이론이 예측하는 위치와 거의 정확히 일치합니다.

다만 Bond 2017 의 핵심 발견은 질량이 **아닌** **얇은** 수소 외피
입니다. 관측된 (M, R, Teff, L) 점에 냉각 곡선이 맞으려면 표면 H 층의
질량 분율이 q_H ≈ 10⁻¹⁰ 이어야 하며, 이는 canonical "두꺼운" 값
q_H ≈ 10⁻⁴ 보다 4 차수가 작습니다. Bond 2017 은 이를 상당 비율의
DA 백색왜성이 얇은 H 층을 갖고 태어났거나 그렇게 진화했다는 직접
증거로 읽으며, H 대류대 바닥이 결국 아래쪽 He 층에 닿아 별이
헬륨 대기로 섞여 들어가는 DA → DC 진화 시나리오를 지지합니다.
40 Eri B 는 17,200 K 의 **완전 복사 대기** 라 이 혼합 사건이
지금 일어나기에는 너무 뜨겁지만, 얇은 H 결과는 이 별의 장기적
운명을 고정합니다.

**NearStars 시나리오 선택. 40 Eri C 와 평균 ~33 AU 떨어져 도는
눈부신 청백색 점광원 백색왜성으로, canonical Bond 2017 파라미터
셋으로 렌더링합니다.** 측정 행 20 개 모두가 canonical 문헌과
일치하며, tie-break 은 표면 색조 hex 코드 (`#cfd9ff`) 한 개뿐
입니다. 태양형 흰색 동반자들과 게임 내에서 구분되도록 더 채도가
높은 청백색을 선택했습니다. divergence 가 없으므로 `## Canonical
alternatives` 섹션도 없습니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | DA2.9 | high | Gianninas, Bergeron & Ruiz 2011 (GBR11). DA 분광-온도 부분류 서베이 |
| `mass_msun` | 0.573 ± 0.018 | high | Bond et al. 2017. BC 페어의 HST/FGS astrometry + Mason 2017 시각 궤도 |
| `radius_rsun` | 0.01308 ± 0.00020 | high | Bond et al. 2017. BVRI + ubvy + JHK + Hipparcos 시차 + 대기 Teff 결합 SED fit |
| `teff_k` | 17200 ± 110 | high | Bond et al. 2017. Balmer-line 대기 fit (Tremblay & Bergeron 2009 grid) |
| `luminosity_lsun` | 0.01349 ± 0.00054 | high | Bond et al. 2017. 볼로메트릭 플럭스 적분 |
| `log_g_cgs` | 7.957 ± 0.020 | high | Bond et al. 2017. 대기 fit 에서 유도한 표면 중력 |
| `gravitational_redshift_km_s` | 27.82 ± 0.97 | high | Bond et al. 2017. M, R 로 유도. 역학 질량의 GR-일치 cross-check 역할 |
| `cooling_age_myr` | ~122 | medium | Bond et al. 2017 §6.2. 얇은 H 냉각 곡선. 논문이 명시한 σ 없음 |
| `progenitor_initial_mass_msun` | ~1.8 | medium | Bond et al. 2017 §6.2. Salaris et al. 2009 의 IFMR 역산 |
| `pre_wd_lifetime_gyr` | ~1.7 | medium | Bond et al. 2017 §6.2. 1.8 M☉ progenitor 의 주계열 + post-MS 수명 |
| `total_age_gyr` | 1.8 ± 0.5 | medium | Bond et al. 2017 §6.2 (cooling age + pre-WD 수명). σ 는 큐레이터 추정, 논문 명시 없음 |
| `h_envelope_mass_fraction_log_qh` | ≈ −10 | high | Bond et al. 2017 §6.1. 얇은 H 결과. canonical 두꺼운 H (q_H ≈ 10⁻⁴) 는 냉각 곡선 fit 으로 배제 |
| `magnetic_field_upper_limit_gauss` | <250 | high | Landstreet & Bagnulo 2015. ESPaDOnS spectropolarimetry, σ⟨Bz⟩ ≈ 85 G, 검출 없음 |
| `core_composition` | CO | high | Bond et al. 2017 §6.3. CO-core 질량-반지름 관계가 오차 내 fit. M_init ~ 1.8 M☉ 에서 표준 |
| `metal_pollution_dazness` | none (clean DA, 광구 금속 없음) | high | Bond et al. 2017. Balmer-only 대기 fit. Fabrika 2003 의 미약한 금속 흡수선은 광구가 아닌 circumstellar/ISM 가스로 귀속 |
| `convective_envelope` | none (완전 복사) | high | Bond et al. 2017 §6.1. 17,200 K 에서 대기는 완전 복사. DA H-대류 onset (~13,000 K) 보다 충분히 위쪽 |
| `companion_a_separation_arcsec` | ~83 | high | Tokovinin MSC 2018. 40 Eri A↔BC 광역 이중성 형상. 적합된 Kepler 해 없음 |
| `companion_c_orbit_period_yr` | 230.09 ± 0.68 | high | Mason, Hartkopf & Miles 2017 Table 4. grade-1 시각 궤도 |
| `companion_c_orbit_eccentricity` | 0.4300 ± 0.0027 | high | Mason, Hartkopf & Miles 2017 Table 4 |
| `companion_c_orbit_a_arcsec` | 6.9310 ± 0.0500 | high | Mason, Hartkopf & Miles 2017 Table 4. 투영 장반경. 5.01 pc 에서 ≈ 34.7 AU |
| `visual_surface_tint_hex_primary` | `#cfd9ff` (채도 높은 청백색) | medium | Tie-break. 17,200 K 에서 Planck-locus 가 청백색 영역. 태양형 흰색 동반자들과 시각 구분을 위해 더 채도가 높은 색을 선택 |
| `stellar_color_temp_k` | 17200 | high | clean 복사 DA 광구에서 Teff 와 동일 |
| `visual_apparent_diameter_arcsec_at_1au` | 25.09 | high | 기하학적 유도. 2 R★ / a × (180·3600/π), R★ = 0.01308 R☉ = 9.10×10⁶ m (~1.43 R⊕) |

## Surface synthesis

40 Eri B 의 광구는 Teff = 17,200 K 의 **완전 복사** 층입니다.
가시 대기에 대류대가 없습니다. Bond 2017 §6.1 가 이를 명시하며,
이 값은 canonical DA H-대류 onset (약 13,000 K) 보다 충분히 위쪽에
있습니다. Granulation, supergranulation, sunspot, plage 등 고전적인
FGK 별의 표면 구조는 모두 **없습니다**. 가시 디스크는 H Balmer 선
의 surface gravity 광폭화 효과로만 변조되는, 거의 균일한 흑체
방사기로 나타납니다.

표면 자기 구조를 찾는 spectropolarimetric 탐색도 빈손이었습니다.
Landstreet & Bagnulo 2015 는 CFHT 의 ESPaDOnS 로 새로운 광역
원편광 기법을 적용해 어떤 조직화된 장 (organized field) 의 상한을
약 250 G 수준까지 낮췄으며, 평균 잡음 σ⟨Bz⟩ ≈ 85 G — 발표 당시
"백색왜성에 대해 얻은 자기장 측정 표준 오차 중 가장 작은 값" 이
었습니다. 그 이전 Fabrika et al. 2003 BSAO 프로그램은 반진폭
~4–5 kG 의 잠정 변동성과 두 후보 자전 주기 (2시간 25분, 5시간 17분)
를 보고했지만, Fabrika 본인이 단일 주기를 "확실히" 결정할 수
없다고 밝혔습니다. Landstreet & Bagnulo 2015 의 더 민감한 비검출은
이 kG 급 주장을 사실상 반박합니다. NearStars 렌더링 관점에서는
**자기 관련 애니메이션을 일체 두지 않는다** 는 뜻이 됩니다. Zeeman
지도도 없고, 점박이 패턴도 없고, 오로라도 없습니다.

표면 중력 log g = 7.957 ± 0.020 (cgs) 은 광자 탈출 속도 v_esc ≈
4,250 km/s 와 27.82 ± 0.97 km/s 의 중력 적색편이 (Bond 2017) 로
번역됩니다. 이 적색편이는 정밀 GR cross-check 역할을 합니다.
독립적으로 ESPaDOnS 분광에서 얻은 중력 적색편이가 1σ 안에서 일치
하여, 역학 질량과 SED 반지름이 상호 일관됨을 확인해 줍니다. KSP cfg
입장에서 이는 보디의 중력과 시각적 크기가 얇은 H 외피를 가진 CO-core
WD 의 canonical 질량-반지름 관계와 충실히 스케일링한다는 의미입니다.

## Atmosphere synthesis

40 Eri B 는 검출 가능한 금속 오염이 없는 **순수 수소** 광구를
가집니다. Bond 2017 의 Balmer-only 분광 fit 은 Tremblay & Bergeron
2009 의 순수-H LTE 모델 그리드를 채택하며, 깨끗한 Balmer 프로파일이
Teff 와 log g 를 높은 정밀도로 고정합니다. Fabrika 2003 의 미약한
금속 흡수 흔적을 빼고 나면 남는 금속 잔재가 없으며, Fabrika 본인은
그 흡수선을 광구 오염이 아니라 ISM 및 dM4e 동반자 40 Eri C 로부터의
약 10⁻¹⁹ M☉/yr 추정 유입으로 흘러 들어오는 circumstellar/interstellar
가스로 귀속했습니다. 따라서 40 Eri B 는 DAZ 가 아니라 clean DA 입니다.
KSP cfg 에 금속 흡수 층을 따로 둘 필요가 없습니다.

장기적인 이야기는 분광형 진화입니다. Bond 2017 §6.1 은 H 층이 너무
얇아서 (q_H ≈ 10⁻¹⁰) 별이 계속 냉각하면 더 낮은 Teff 에서 형성될
H 대류대의 바닥이 결국 아래쪽 헬륨 외피에 닿게 된다고 지적합니다.
두 층이 섞이면서 40 Eri B 는 **DA 에서 헬륨 대기 DC 백색왜성으로
전이** 합니다. 임박한 사건은 아닙니다. 40 Eri B 는 현재 17,200 K
에서 DA2.9 이며 천천히 냉각 중인데, DA → DC 혼합은 보통 6,000 K
이하 (얇은 H DA 의 경우) 에서 일어납니다. NearStars 의 canonical
시간 스케일 (인게임 연 단위) 에서 이 전이는 무의미하며, cfg 는
현재 DA2.9 상태로만 40 Eri B 를 렌더링합니다.

색채권도, 천이 영역도, 코로나도 없습니다. FGK 와 M 왜성에서 활동도를
교정하는 지표들 (log R'HK, Hα 방출, X 선 L_X 사이클) 은 복사 대기
백색왜성에 대해 물리적 의미가 없습니다. Phase 2 DB 가 해당 필드를
N/A 로 정확히 기록합니다. XUV 방출은 17,200 K 흑체의 열적 Wien
꼬리 한계까지로 제한되며, 그마저도 어떤 가상의 궤도 천체에 화학적
영향을 미칠 임계값 아래입니다. 볼로메트릭 광도 자체가 0.0135 L☉
에 불과하기 때문입니다.

## Rotation & spin synthesis

40 Eri B 의 자전은 **잘 제약되지 않습니다**. 현대 모니터링을 견디는
광도 변동성이 없습니다. spectropolarimetric Doppler 영상으로 주기를
복원해 줄 검출 가능한 Zeeman 편광도 없습니다 (Landstreet & Bagnulo
2015 가 Fabrika 2003 의 변동성 주장을 가능하게 했던 kG 급 장을
사실상 반박했기 때문). 광폭화된 Balmer 프로파일에서 얻을 수 있는
sub-projected v sin i 상한은 17,200 K 에서의 압력 광폭화와 모델
축퇴를 일으킵니다. Phase 2 DB 는 40 Eri B 에 대해 **회전 entry 가
아예 없습니다**. Phase 3 합성도 그 null 을 그대로 이어받습니다.

KSP cfg 관점에서 이는 누락된 필드가 아니라 명시적 부재입니다. 보디
cfg 는 백색왜성 물리와 일관된 어떤 회전율도 고를 수 있으며, 관습적인
선택은 AGB progenitor 의 자전이 감속되어 핵에 남겨진 느린 회전 (시간
~ 일 단위 P_rot) 입니다. 단, AGB common-envelope 또는 wind-loss
단계가 각운동량을 M 왜성 동반자 40 Eri C 로 옮겼을 가능성도 있습니다
(Bond 2017 §6.2 가 C 의 AGB-스핀업 시나리오로 Fuhrmann 2014 를
인용). NearStars 스케일의 시각 렌더링에서는 자전율이 감지되지
않습니다. 보디가 고배율에서도 점광원에 가깝게 보이기 때문입니다.

40 Eri B 는 DAV ZZ-Ceti 불안정 영역 **바깥** 에 있습니다. DA 백색왜성
의 경험적 불안정 영역은 대략 10,500 K 부터 12,500 K 사이에 있으며
(Gianninas et al. 2011 등), 17,200 K 는 청색 가장자리보다 충분히
위쪽에 위치합니다. 관측된 맥동도 없고 예상되는 맥동도 없습니다.
따라서 렌더러는 어떤 표면 밝기 진동도 애니메이션화하지 않습니다.

## Visual styling

NearStars 렌더러에서 40 Eri B 는 눈부신 **청백색 점광원** 으로
표현됩니다. canonical 태양 흰색에 대비되는 채도 높은 cyan-tinted
white 를 `#cfd9ff` 로 인코딩했습니다. 17,200 K 에서 Planck-locus
색도는 Kelvin 스케일의 청백색 영역에 자리합니다 (Vega 의 ~9,600 K
와 가장 뜨거운 O 별의 ~30,000+ K 사이). 순수 흰색으로 렌더링하면
세 컴포넌트를 함께 프레임에 담을 때 K 왜성 40 Eri A 와 M 왜성
40 Eri C 와의 시각 구분이 사라집니다. tie-break 은 interesting-first
룰에 따라 채도가 더 강한 톤으로 기본값을 잡습니다.

5.01 pc 거리에서 본 Earth 시점 외관 등급은 V = 9.53. 가까움에도
망원경 없이 맨눈으로는 보이지 않습니다. 백색왜성의 작은 반지름
(0.013 R☉, ~1.4 R⊕) 이 볼로메트릭 출력을 0.0135 L☉ 로 제한하기
때문입니다. 보디 cfg 는 별을 물리 스케일 그대로 렌더링합니다.
1 AU 분리에서 외관 각지름은 ~25″ 입니다. Earth 에서 본 태양이
~30′ 디스크를 차지하는 것과 비교해 한참 작은 값이라, 시스템 내
근접 fly-by 거리에서도 40 Eri B 는 해상된 구가 아니라 작고 밝은
원반으로 보입니다.

이중 짝 40 Eri C 는 평균 ~34.7 AU 분리 (Mason 2017 a = 6.93″ ×
5.01 pc) 로 공전하며, 230 년 궤도에 걸쳐 근일점 ~19.8 AU (e =
0.43) 와 원일점 ~49.6 AU 사이를 움직입니다. 40 Eri B 를 도는
보디 시점에서 보면 M 왜성 40 Eri C 는 분각 분리에서 가변 밝기의
어두운 붉은 점 (DY Eri 는 flare star) 으로 보입니다. 더 멀리 있는
40 Eri A 는 ~83″ (5.01 pc 에서 ~415 AU) 떨어져 있으며, Kopernicus
궤도 시간 스케일에서 무묶임이지만 밝은 주황색 K 왜성 "두 번째 태양"
으로 보입니다. V = 4.43 으로, 가상의 40 Eri B 행성에서 보면 밤
하늘의 등급-1 별과 비슷한 밝기입니다.

이 삼중계는 시스템 전체 시점에서 가장 잘 음미됩니다. A 는 밝은
주황 디스크, B 는 청백색 점광원, C 는 어두운 붉은 flare star —
서로 다른 세 가지 stellar 진화 종점이 5 pc 한 화면 안에 배열돼
있습니다. Visual styling cfg 는 B 를 중성 흰색 쪽으로 섞지 말고
이 색채 삼중주를 보존해야 합니다.

## Bibliography

### Read (decision-driving)

- **Bond H. E., Bergeron P. & Bédard A. 2017** — *Astrophysical
  Implications of a New Dynamical Mass for the Nearby White Dwarf 40
  Eridani B*, ApJ 848, 16 (`2017ApJ...848...16B`,
  arXiv:1709.00478, DOI 10.3847/1538-4357/aa8a63). Mason 2017
  시각 궤도에 정박해 BC 페어를 HST/FGS 로 astrometry 한 결과를,
  순수-H 모델 대기 Balmer-line fit 과 BVRI + ubvy + JHK +
  Hipparcos 시차 SED fit 과 결합. 표제 파라미터.
  M = 0.573 ± 0.018 M☉, R = 0.01308 ± 0.00020 R☉,
  Teff = 17,200 ± 110 K, log g = 7.957 ± 0.020,
  L = 0.01349 ± 0.00054 L☉, 중력 적색편이 27.82 ± 0.97 km/s.
  §6.1 얇은 H 외피 (q_H ≈ 10⁻¹⁰) + 완전 복사 대기. §6.2 IFMR
  유도 progenitor M_init ≈ 1.8 M☉, pre-WD 수명 1.7 Gyr, 총
  나이 1.8 Gyr. §6.3 가까운 WD 4 개에 걸친 CO-core MRR 일치
  검사. §6.4 얇은 H DA 가 흔하다는 결론.

- **Landstreet J. D. & Bagnulo S. 2015** — *A novel and
  sensitive method for measuring very weak magnetic fields
  of DA white dwarfs — A search for a magnetic field at the
  250 G level in 40 Eridani B*, A&A 580, A120
  (`2015A&A...580A.120L`, DOI 10.1051/0004-6361/201526434).
  CFHT 의 ESPaDOnS 광역 원편광. 개별 ⟨Bz⟩ 측정이 σ ≈ 80–90 G
  안에서 0 과 일치. 어떤 장이든 ⟨Bz⟩ ≲ 250 G 의 잠정 상한을
  결론. 잡음이 "백색왜성에 대해 얻은 자기장 측정 표준 오차 중
  가장 작은 값" 임을 명시. Fabrika 2003 의 kG 변동성 주장을
  반박.

- **Mason B. D., Hartkopf W. I. & Miles K. N. 2017** —
  *Binary Star Orbits V. The Nearby White Dwarf — Red Dwarf
  Pair 40 Eri BC*, AJ 154, 200 (`2017AJ....154..200M`,
  arXiv:1707.03635, DOI 10.3847/1538-3881/aa803e). 2016 년
  까지의 speckle interferometry 를 포함하는 시각 궤도 재유도.
  grade-1 definitive 해 Table 4. P = 230.09 ± 0.68 yr,
  T = 1847.60 ± 1.10, e = 0.4300 ± 0.0027, a = 6.9310 ±
  0.0500″, i = 107.53° ± 0.29°, ω = 318.20° ± 1.10°,
  Ω = 151.44° ± 0.12°. 역학 질량 M_B = 0.575 ± 0.018 M☉,
  M_C = 0.2041 ± 0.0064 M☉ — Bond 2017 과 오차 내 일치.

- **Gianninas A., Bergeron P. & Ruiz M. T. 2011** —
  *A Spectroscopic Survey and Analysis of Bright,
  Hydrogen-Rich White Dwarfs*, ApJ 743, 138
  (`2011ApJ...743..138G`, arXiv:1109.3171). DA 분광-온도 부분류
  서베이의 결정판이며 DA1–DA9 Sion 분류를 채택. 40 Eri B
  (WD 0413−077) 는 이 작업에서 DA2.9 부분류를 받았고, 이 값이
  2011 년 이후 Bond 2017 과 후속 문헌의 canonical 분광형이
  됩니다.

### Read (context / methodology)

- **Tremblay P.-E. & Bergeron P. 2009** — *Spectroscopic
  Analysis of DA White Dwarfs: Stark Broadening of Hydrogen
  Lines Including Nonideal Effects*, ApJ 696, 1755
  (`2009ApJ...696.1755T`). Bond 2017 이 Balmer-line Teff 및
  log g fit 에 채택한 순수-H 모델 대기 그리드.

- **Salaris M. et al. 2009** — *Semi-empirical White Dwarf
  Initial–Final Mass Relations: A Thorough Analysis of
  Systematic Uncertainties due to Stellar Evolution Models*,
  ApJ 692, 1013 (`2009ApJ...692.1013S`). Bond 2017 §6.2 가
  뒤집어서 측정 M_final = 0.573 M☉ 에서 M_init ≈ 1.8 M☉ 을
  복구할 때 쓴 관계 M_final = 0.134 M_init + 0.331.

- **Fabrika S. N. et al. 2003** — *Looking for magnetic
  fields in white dwarfs. The B and M components of 40 Eri*,
  BSAO 55, 17 (arXiv:astro-ph/0006050). 앞선 kG 변동성 주장
  (B_max ~ 4–5 kG, 후보 주기 2시간 25분 / 5시간 17분). 저자
  본인은 단일 주기를 firmly 정할 수 없다고 명시. Landstreet &
  Bagnulo 2015 의 비검출에 의해 사실상 대체됨.

- **Tokovinin A. 2018** — *The Updated Multiple Star Catalog*,
  ApJS 235, 6 (`2018ApJS..235....6T`). 40 Eri 의 MSC entry 가
  A↔BC 외곽 페어를 ~83″ 분리, ~8,000 년 근사 주기로 기록.
  적합된 Kepler 해는 없습니다.

### Read (instrument-only / context)

- **Mason B. D. et al. 2021** — *Speckle Interferometry at
  the US Naval Observatory. XXIV*, AJ 162, 53
  (`2021AJ....162...53M`, DOI 10.3847/1538-3881/abfaa2).
  최신 BC 궤도 fit. P = 233.20 ± 0.65 yr, e = 0.4141 ±
  0.0072, a = 6.88788 ± 0.03488″. 현 Sixth Orbit Catalog
  엔트리로 등재. Phase 3 cfg 는 Bond 2017 의 질량 유도와
  자기 일관성을 유지하려고 Mason 2017 을 그대로 두며,
  2021 업데이트는 아래 follow-up 항목에 남깁니다.

- **Holberg J. B. et al. 2013** — *Where are all the
  Sirius-like binary systems?*, MNRAS 435, 2077
  (`2013MNRAS.435.2077H`). 40 Eri BC 를 들녘 Sirius-like
  (FGK + WD) 시스템 집단의 맥락에 둡니다. 40 Eri B
  파라미터를 새로 측정하지는 않습니다.

### Not read — no decision impact (~12 papers)

Bond 이전의 legacy 시차 / 궤도 기록 (Heintz 1974, Wegner 1974
spectroscopic redshift, McCook & Sion 1999 WD catalog 분류),
40 Eri B 를 개별 측정 없이 비검출로만 포함하는 DA
spectropolarimetric 서베이 (Kawka & Vennes 2007, Aznar Cuadrado
2004), 그리고 Bond 2017 을 독립 측정 없이 인용한 최근 catalog /
Gaia DR3 cross-match 논문들. 전체 필터링된 목록은 Phase 2
meta_notes 의 인용 사슬에서 함축적으로 잡힙니다. 어느 하나도
Decisions 표를 바꾸지 않습니다.

## Open items for follow-up

- **Mason 2021 궤도 업데이트.** Mason et al. 2021
  (`2021AJ....162...53M`) 가 Mason 2017 시각 궤도를 P = 233.20 ±
  0.65 yr, e = 0.4141 ± 0.0072, a = 6.88788 ± 0.03488″ 로 갱신
  합니다. 후속 reconciliation 단계에서 2021 elements 를 채택하고
  Bond 2017 의 동일한 HST/FGS astrometry 와 결합해 역학 질량을
  다시 유도해야 합니다. 결과 질량은 현재 ±0.018 M☉ 오차보다 작게
  움직일 것이지만, 궤도 주기 자체는 Principia long-period n-body
  적분에 영향을 줍니다.

- **DA → DC 전이 Teff 임계값.** Bond 2017 §6.1 은 얇은 H 층이
  17,200 K 보다 훨씬 낮은 어떤 Teff 에서 He 외피로 섞이리라
  예측하지만 q_H ≈ 10⁻¹⁰ 에 대한 구체적 전이 온도는 인용하지
  않습니다. 차후 cfg 변종은 Bergeron-Wesemael 냉각 곡선들 사이를
  보간해 미래 DC 상태를 렌더링할 수 있습니다. 현재 cfg 는 현
  DA2.9 상태만 사용합니다.

- **ZZ Ceti 맥동 상태.** 40 Eri B 는 DAV 불안정 영역
  (10,500–12,500 K) 의 한참 바깥 (17,200 K) 에 있으며 어떤 진동도
  관측되지 않습니다. 만약 TESS 또는 CHEOPS 의 향후 장기 기준선
  모니터링이 sub-mmag 광도 변동성을 검출한다면 cfg 가 낮은 진폭의
  맥동 효과를 얻을 수 있겠지만, 현재 기록은 없습니다.

- **Astrometric Gaia DR4 질량 정밀화.** Gaia DR4 (10 년대 후반
  공개 예정) 는 BC 페어의 다중 epoch astrometry 를 epoch 당
  sub-microarcsecond 정밀도로 제공할 것입니다. 0.573 ± 0.018 M☉
  의 역학 질량은 한 자릿수 정도로 좁아질 수 있습니다.

- **Phase 2 DB 총 나이 σ.** Bond 2017 은 "~1.8 Gyr" 만 보고하며
  논문에 명시된 불확실성이 없습니다. Phase 2 DB 가 σ = 0.5 Gyr
  를 큐레이터 추정으로 들고 있습니다. Phase 3 Decisions 행도 같은
  추정을 따라갑니다. 후속 reconciliation 단계는 이 값을 그대로
  유지하거나 (문서화된 채로), 추후 냉각 곡선 + IFMR Monte-Carlo
  분석이 출판된다면 논문 인용 σ 로 교체할 수 있습니다.

## Related

- [40-eridani-a](40-eridani-a.md) — ~83″ (~415 AU) 떨어진 K0.5 V 주성. 반박된 "Vulcan" 행성의 호스트 (Burrows et al. 2024)
- [40-eridani-c](40-eridani-c.md) — M4.5 Ve flare star DY Eri. 40 Eri B 와 230 년 궤도로 결합
- [methodology](../reference/methodology.md) — Decisions 표의 스키마 출처
- [binary-epoch-pipeline](../reference/binary-epoch-pipeline.md) — BC 시각 궤도의 Kepler→ICRS 변환
