<!-- 61 Virginis Phase 3 합성. cfg-ready 결정과 근거 -->
# 61 Virginis — Phase 3 Synthesis

61 Virginis (HD 115617, HIP 64924, GJ 506) 은 8.534 ± 0.001 pc (Gaia
DR3 시차 117.17 ± 0.15 mas, 27.83 광년) 거리의 처녀자리에 위치한
맨눈 가시 G6.5V 솔라 트윈입니다. Gaia 라벨의 G6.5V 분광형은 Gray
2003 의 G7V 분류와 호환되며, 유효 온도 Teff = 5552 K (Gaia DR3) 는
태양보다 약 220 K 낮습니다. Vogt 2010 이 HIRES + 장기선 간섭 분석으로
유도한 질량 0.942 ± 0.034 M☉, 반지름 0.963 ± 0.011 R☉ 가 DB Phase 2
recommended 값입니다. 볼로메트릭 광도 L = 0.82 L☉ 는 반지름과 Teff
에서 따라옵니다. 금속도는 오차 범위 내에서 사실상 태양과 같으며
([Fe/H] ≈ +0.00 ± 0.05, Pavlenko 2012, Bensby 2014, Brewer 2016),
색채권 활동도-나이 관계로 ≈ 6.1 ± 1.7 Gyr 가 나옵니다 (Mamajek &
Hillenbrand 2008). 61 Vir 는 태양보다 10 억 년쯤 더 오래된 원반종족
솔라 트윈입니다. 별 자체는 조용한 상태로, 광구 회전 주기 P_rot ≈
29 일 (Wright 2004, S_HK 변동에서. Vogt 2010 §4 가 RV jitter 로 확인),
log R'HK ≈ −5.0 (Isaacson & Fischer 2010), 그리고 X 선 광도 log L_X
≈ 26.7–27.0 cgs (Schmitt & Liefke 2004 NEXXUS-2) 로 모두 비활성
locus 에 있습니다.

61 Vir 는 RV 로 검출된 행성 세 개를 거느립니다 (Vogt 2010 의 HIRES +
AAT 결합 해). b 는 4.215 일 주기 5.1 M⊕ Msini 의 슈퍼지구, c 는
38.021 일 주기 18.2 M⊕ 의 따뜻한 sub-Neptune, d 는 123.01 일 주기
22.9 M⊕ 의 sub-Neptune 입니다. 행성대 바깥에서는 **Wyatt et al.
2012 의 Herschel/PACS 영상이 ≈ 30 AU 부근을 중심으로 하는 차가운
debris 띠를 분해**하며, 바깥쪽은 ≈ 96 AU 까지 뻗고 dust 온도 ~50 K
인 전형적 KBO 아날로그입니다. dust 질량은 태양의 Edgeworth–Kuiper
띠 잔존량의 6–8 배에 달합니다.

**NearStars 시나리오 선택. 약간 더 차가운 G6.5V 솔라 트윈, ~30 AU 의
단일 차가운 debris 띠가 분해되며, 안쪽 행성 세 개가 전경의 점광원으로
함께 보이는 모습으로 렌더링합니다.** Stellar Physical 일곱 행은 모두
canonical-aligned 이며, tie-break 세 행은 시각 색조, debris 띠 산란
색조, debris 띠 불투명도로 Herschel 의 원적외선 검출이 광학 외관을
제약하지 않는 영역의 미적 선택입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G6.5V | high | Gaia DR3 분광 라벨. Gray 2003 의 G7V 와 일관되며 더 세분된 subtype 해상도 |
| `mass_msun` | 0.942 ± 0.034 | high | Vogt 2010. HIRES + 장기선 간섭 분석, DB Phase 2 recommended |
| `radius_rsun` | 0.963 ± 0.011 | high | Vogt 2010. 같은 분석에서 간섭계 각지름과 시차 결합 |
| `teff_k` | 5552 | high | Gaia DR3. Pavlenko 2012 의 5538 K 가 오차 범위 내에서 일치 |
| `luminosity_lsun` | 0.82 | high | Vogt 2010. R, Teff 로 Stefan–Boltzmann 유도. R²·(T/T☉)⁴ = 0.79 닫힌 식과 반올림 오차 내 일치 |
| `metallicity_fe_h_dex` | +0.00 ± 0.05 | high | Pavlenko 2012 솔라 트윈 differential 분석. Bensby 2014, Brewer 2016 SPOCS 가 ±0.03 dex 내에서 동의 |
| `age_gyr` | 6.1 ± 1.7 | medium | Mamajek & Hillenbrand 2008. 색채권 활동도-나이 + isochrone 결합. 61 Vir 의 표준 나이 인용 |
| `rotation_period_days` | 29 | high | Wright 2004. 색채권 S_HK 변동 주기. Vogt 2010 §4 가 RV jitter 모델로 확인 |
| `activity_log_rhk` | −5.0 | high | Isaacson & Fischer 2010. California HK 카탈로그. 장기 모니터링 결과 조용한 G 왜성 locus 에서 안정 |
| `x_ray_log_lx_cgs_min` | 26.7 | medium | Schmitt & Liefke 2004. NEXXUS-2 ROSAT 서베이 하한 |
| `x_ray_log_lx_cgs_max` | 27.0 | medium | Schmitt & Liefke 2004. NEXXUS-2 ROSAT 서베이 상한. 아직 분해된 사이클 없음 |
| `visual_surface_tint_hex_primary` | `#fff2dc` (태양보다 더 호박색이 도는 따뜻한 크림) | medium | Tie-break. G6.5V 5552 K 흑체 + interesting-first. 플레이어의 태양 기준보다 더 차가운 G 왜성이라는 단서를 시각으로 전달 |
| `stellar_color_temp_k` | 5552 | high | Teff 유도 |
| `disk_present` | true | high | Wyatt et al. 2012. Herschel/PACS 분해된 차가운 띠. Tanner 2014, Su 2017 SED 로 확인 |
| `disk_inner_radius_au` | 30 | high | Wyatt 2012. Herschel/PACS 분해 지오메트리. modified-blackbody SED fit 으로 온도-가중 반경이 30 AU 근방 |
| `disk_outer_radius_au` | 96 | medium | Wyatt 2012. 70/100/160 μm 에서 분해된 바깥쪽 경계. 안쪽보다 약간 덜 제약됨 |
| `disk_dust_temperature_k` | 50 | high | Wyatt 2012. modified-blackbody SED fit (범위 30–60 K) |
| `disk_tint_rgb_hex` | `#9ca4b5` (차가운 강철빛 산란 색조) | low | Tie-break. 50 K 열복사 피크는 원적외선에 있어 사람 눈에는 안 보임. cfg 는 궤도 뷰 렌더러에서 띠가 인식 가능하도록 차가운 회색 산란 색조를 선택 |
| `disk_opacity` | 0.10 | low | Tie-break. Herschel τ ~ 10⁻⁵ (원적외선 광학 깊이) 는 플레이어 가시성 한참 아래. cfg 는 렌더러 가시 값을 채택하되 띠가 분명히 희미하게 보이도록 유지 |
| `disk_morphology` | single cold belt, KBO analog | high | Wyatt 2012. 단일한 넓은 띠. warp/gap/이중대 구조 보고 없음 |
| `disk_resolved_imaging` | true | high | Wyatt 2012. Herschel/PACS 70/100/160 μm 에서 분해 |
| `disk_imaging_observatory` | Herschel/PACS (Wyatt 2012) | high | 직접 인용 |
| `disk_mass_mearth` | 0.07 | medium | Wyatt 2012. dust 질량을 태양 KBO 잔존량의 ~6–8 배로 인용. 중간값 채택. 표준 5×10⁻³ M⊕ Edgeworth–Kuiper dust 기준으로 M⊕ 환산 |
| `disk_planetesimal_belt_inferred` | true | high | Wyatt 2012 §5. PR drag + 충돌 분쇄에 대한 dust 수명상 관측된 dust 를 채우려면 부모 천체 띠가 필요 |

## Surface synthesis

61 Vir 의 광구는 태양보다 ~220 K 더 차갑습니다. Teff 5552 K 대 태양
기준 5772 K 입니다. 다른 솔라 트윈 파라미터에서는 거의 같으며, 질량
0.942 M☉, 반지름 0.963 R☉, [Fe/H] 가 태양과 0.05 dex 이내입니다. 광도
0.82 L☉ 는 거의 태양과 같은 반지름에 더 낮은 온도가 결합된 자연스러운
결과입니다. 가시 영역에서 스펙트럼은 canonical G 왜성 Ca II H&K, Mg b,
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

시각 색조의 약한 호박색 변위는 tie-break 입니다. 5552 K 흑체 피크는
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

29 일 회전 주기 (Wright 2004 가 색채권 S_HK 변동에서, Vogt 2010 §4
가 RV 잔차에서 28–30 일 power 로 확인) 는 태양의 25.4 일 Carrington
회전보다 약간 느립니다. Skumanich braking 법칙 P_rot ∝ √t 에 따라
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
  띠를 본다면 보일 모습과 비슷하되 dust 질량이 6–8 배 더 많아 더 밝습니다.
- **조용한 별 애니메이션**. 흑점 렌더링은 절제됩니다. 피크 면적은 디스크의
  ≲ 0.3% 로 태양 극대기보다 훨씬 덜 극적입니다. 두드러진 flare 나 CME
  시각 효과는 없습니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Vogt S. S. et al. 2010** — *A Super-Earth and Two Neptunes
  Orbiting the Nearby Sun-Like Star 61 Virginis*, ApJ 708, 1366
  (`2010ApJ...708.1366V`). 61 Vir 의 항성 파라미터 (M = 0.942 ± 0.034 M☉,
  R = 0.963 ± 0.011 R☉, L = 0.82 L☉) 와 세 행성 검출 (b 4.215 일, c
  38.021 일, d 123.01 일) 의 기초 논문. HIRES + AAT RV 결합 해. DB
  recommended 물리 파라미터의 attribution 출처.
- **Wyatt M. C. et al. 2012** — *Herschel imaging of 61 Vir: implications
  for the prevalence of debris in low-mass planetary systems*, MNRAS
  424, 1206 (`2012MNRAS.424.1206W`, arXiv:1204.6063). Herschel/PACS
  로 70/100/160 μm 에서 차가운 debris 띠를 분해 영상화. ~30 AU 중심,
  ~96 AU 까지 뻗는 단일한 넓은 띠, dust 온도 ~50 K, dust 질량 태양 KBO
  잔존량의 6–8 배. Circumstellar-disk 모든 Decisions 행의 anchor.
- **Mamajek E. E. & Hillenbrand L. A. 2008** — *Improved Age Estimation
  for Solar-Type Dwarfs Using Activity-Rotation Diagnostics*, ApJ 687,
  1264 (`2008ApJ...687.1264M`, arXiv:0807.1686). 색채권 활동도-나이 +
  isochrone 결합. 61 Vir 의 표준 나이 인용으로 6.1 ± 1.7 Gyr.
- **Wright J. T. et al. 2004** — *Chromospheric Ca II Emission in
  Nearby F, G, K, and M Stars*, ApJS 152, 261 (`2004ApJS..152..261W`).
  Mt-Wilson S-index 와 유도된 회전 주기 카탈로그. 61 Vir P_rot ≈ 29 일
  을 S_HK 변동에서.
- **Pavlenko Y. V. et al. 2012** — *Effective temperatures, gravities,
  metallicities, and ages of 18 solar twin candidates*
  (`2012MNRAS.422..542P`, arXiv:1112.0590). 61 Vir 를 포함한 솔라 트윈
  후보의 고분해 분광. Teff = 5538 K 와 태양으로부터 0.05 dex 이내의
  [Fe/H] 를 확인.

### Read (context / methodology, not directly decision-driving)

- **Isaacson H. & Fischer D. 2010** — *Chromospheric Activity and Jitter
  Measurements for 2630 Stars on the California Planet Search*, ApJ
  725, 875 (`2010ApJ...725..875I`, arXiv:1009.2301). California HK
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
  A71 (`2014A&A...562A..71B`, arXiv:1309.2631). 얇은 원반 금속도 샘플
  의 61 Vir. [Fe/H] 가 태양과 일관.
- **Brewer J. M. et al. 2016** — *Spectral Properties of Cool Stars
  (SPOCS): extended catalog of 1626 stars*, ApJS 225, 32
  (`2016ApJS..225...32B`, arXiv:1606.07929). SPOCS 확장 카탈로그.
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
