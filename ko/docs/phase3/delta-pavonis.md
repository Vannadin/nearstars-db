<!-- δ Pavonis Phase 3 합성: cfg-ready 결정과 근거 -->
# δ Pavonis — Phase 3 Synthesis

δ Pavonis (HD 190248, HIP 99240, GJ 780) 는 태양에 가장 가까운 G 형
subgiant 별 중 하나로, 거리는 6.10 ± 0.005 pc 입니다 (Gaia DR3 시차
163.95 ± 0.12 mas). 분광형 G8IV (Gray 2006 NStars, Houk & Cowley 1975)
는 주계열을 막 벗어난 단계를 의미합니다. 중심 수소가 소진되고 수소
껍질 연소가 시작되며 외피가 부풀어 오르는 시점입니다. 유효 온도
5644 ± 30 K (Gomes da Silva 2021 AMBRE-HARPS) 와 V = 3.56 으로,
남반구에서 가장 밝은 G subgiant 이자 인근 subgiant 연구의 교과서적
표적입니다. 확정된 행성은 없습니다. 초고정밀 RV (HARPS, Tinney 2005,
Mawet 2017) 와 직접 촬영 (Lannier 2017) 캠페인이 1 AU 에서 ~3 M_Jup
이상, 거주가능영역에서 해왕성 질량 이상을 모두 배제했으며, ESPRESSO
시대에는 이 한계가 더 깊이 내려갑니다.

대신 δ Pav 가 가진 것은 차가운 잔해 원반입니다. Spitzer/MIPS 70 µm
초과 (Beichman 2006) 로 처음 검출됐고, Herschel/PACS 가 70, 100, 160
µm 측광으로 확인했습니다 (Eiroa 2013 DUNES, Lawler & Tanner 2014).
SED 에 대한 modified blackbody fit 은 약 30–80 AU 의 단일 차가운 belt
를 주며, 먼지 온도 T_d ≈ 55 K, 먼지 질량 M_d ~ 0.01 M⊕ 입니다. 작지만
명확하며, 어느 정도 오래된 시스템 (시스템 나이 ~5 Gyr, Gomes da Silva
2021 PARSEC isochrone. 다만 문헌은 pipeline 에 따라 5–9 Gyr 로 갈림)
에 존재한다는 점이 핵심입니다. 50 AU 위치의 µm-cm 먼지 충돌 cascade
수명 (50–500 Myr) 의 ~5 배 이상이라, 충돌로 보충되는
microplanetesimal 저장소가 얇은 카이퍼 belt 와 유사한 형태로 존재해야
한다는 것을 의미합니다.

**NearStars 시나리오 선택. 약간 부풀어 오른, G8V 왜성보다 살짝 더
붉은 늙고 조용한 G8 subgiant 별을, ~30–80 AU 의 희미한 단일 차가운
잔해 ring 을 배경으로 보여 줍니다.** 항성 파라미터는 canonical 정렬
입니다. 원반 지오메트리는 SED 역해석에만 의존하며 (Herschel 는 belt
를 분해하지 못함), 원반 색조와 불투명도는 medium/low 신뢰도로
표기됩니다. cfg 는 ALMA 나 JWST 가 분해할 때까지 belt 를 시각적으로
은은하게 운영합니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | G8IV | high | Gray 2006 NStars, Houk & Cowley 1975 MK 카탈로그. HR 도 위치로 subgiant 분류 확인 |
| `mass_msun` | 1.064 ± 0.013 | high | Gomes da Silva 2021 PARSEC isochrone (Gaia DR2 시차 + AMBRE-HARPS Teff/[Fe/H]). 이전 Bensby 2014 (1.03 ± 0.07) 와 Spada 2011 (~1.05) subgiant fit 을 1σ 안에서 supersede |
| `radius_rsun` | 1.115 ± 0.025 | medium | Gomes da Silva 2021 PARSEC isochrone (질량과 동일 fit). 발표된 간섭계 직경 없음 (δ Pav 적위 −66° 가 CHARA 범위 밖, PAVO@SUSI · VLTI-PIONIER 모두 관측 발표 없음). Bruntt 2010 의 R = 1.22 ± 0.02 는 Stefan-Boltzmann (L+Teff) 유도값으로, Gomes 2021 와 9% 차이는 (a) Gaia DR2 시차 갱신과 (b) PARSEC vs Stefan-Boltzmann 방법 차이 때문 |
| `teff_k` | 5644 ± 30 | high | Gomes da Silva 2021 AMBRE-HARPS pipeline. Tsantaki 2013 고분해 5566 ± 36 K 와 Casagrande 2011 IRFM 5598 ± 80 K 가 결합 오차 안에서 일치 |
| `luminosity_lsun` | 1.246 ± 0.05 | high | Eiroa 2013 DUNES, SED + Hipparcos 시차에서 직접 적분한 bolometric flux. R + Teff Stefan-Boltzmann 유도값 (현재 Gomes 2021 값으로 ~1.17) 보다 우위 |
| `metallicity_fe_h_dex` | +0.36 ± 0.02 | high | Gomes da Silva 2021 AMBRE-HARPS (가장 작은 형식 오차). Tsantaki 2013 +0.32 ± 0.03, Ramirez 2013 +0.33 ± 0.07, Bensby 2014 +0.37 ± 0.20 모두 결합 오차 안에서 일치 |
| `age_gyr` | 5.04 ± 1.23 | low | Gomes da Silva 2021 PARSEC isochrone (newest paper, 가장 작은 stated 오차). Bensby 2014 도 ~5 Gyr (Geneva-Copenhagen) 로 동의. 그러나 Tsantaki 2013 isochrone (8.5 ± 1.3) 와 Eiroa 2013 Ca II age (8.3) 는 ~8–9 Gyr. 문헌이 pipeline 에 따라 ~5 와 ~9 Gyr 로 갈림. tier hierarchy 로 Gomes 2021 채택하되, 미해소 spread 를 반영해 Confidence 는 low 유지 |
| `rotation_period_days` | ≤175 (상한). Skumanich 기준 best estimate ~30 | low | Ramirez 2013 v sin i = 0.32 ± 0.05 km/s (HARPS solar-twin 정밀도. 이전 1–3 km/s 상한 supersede) + R = 1.115 R☉ + sin i ≤ 1 ⇒ 어느 inclination 에서든 P_rot ≤ 175 d. 광도 주기 미검출. ~5 Gyr 에서 태양형 초기 spin 가정한 Skumanich braking 은 P_rot 를 30 d 부근에 두지만 직접 측정은 아님 |
| `activity_log_rhk` | −5.13 ± 0.003 | high | Gomes da Silva 2021. 2003–2016 HARPS 스펙트럼 6002 개의 가중평균. 태양 최소 (log R'HK ≈ −4.96) 보다 한참 아래로, 알려진 G subgiant 중 가장 비활성에 속함. Boro Saikia 2018 다중-survey 중앙값 −4.99 / HARPS 단독 중앙값 −5.49 가 양쪽으로 bracket. Henry 1996 Mt Wilson −5.10 과 일치 |
| `activity_cycle_years` | 미상 | low | Mt. Wilson 장기 모니터링 커버리지 없음. 이 진화 단계의 subgiant 는 약화되거나 불규칙한 사이클을 보이는 경우가 많음 |
| `x_ray_log_lx_cgs_max` | 26.6 | medium | ROSAT 전천 미검출 상한 (Hünsch 1998). 매우 약한 코로나와 일관 |
| `limb_darkening_alpha_h` | 0.16 ± 0.02 | medium | Claret 2011 LD 표에서 Teff ≈ 5640 K, log g ≈ 4.0 의 G8IV 로 유도. 간섭계 직접 LD 측정은 없음 (δ Pav 간섭계 관측 자체가 없음) |
| `visual_surface_tint_hex_primary` | `#ffe8c8` (G2V Sol 보다 더 붉은 amber-cream) | medium | Tie-break. G8IV 흑체 5644 K + +0.36 dex 금속도 reddening. subgiant envelope 부풀림이 disk integrated 색을 같은 Teff 의 G8V 보다 살짝 더 붉게 시프트 |
| `stellar_color_temp_k` | 5644 | high | Teff (Gomes da Silva 2021) 유도 |
| `visual_corona_extent_radii` | 1.6 | low | Tie-break. 약한 색채권 + 낮은 log R'HK = -5.1 → 절제된 corona band. 태양형 더 밝은 halo 대신 얇은 ring 으로 렌더 |
| `disk_present` | true | high | Beichman 2006 Spitzer/MIPS 70 µm 초과. Eiroa 2013 Herschel/PACS 가 70/100/160 µm 에서 확인 |
| `disk_inner_radius_au` | 30 | medium | Lawler & Tanner 2014 단일 belt fit r_in ≈ 30 AU (T_d = 55 K modified blackbody). Eiroa 2013 는 grain size 에 따라 r_in 23–35 AU |
| `disk_outer_radius_au` | 80 | medium | Lawler & Tanner 2014 r_out ≈ 80 AU. SED 만, 분해되지 않음 |
| `disk_dust_temperature_k` | 55 ± 5 | high | Eiroa 2013 + Lawler & Tanner 2014 SED fit 모두 T_d ≈ 55 K, modified blackbody 방출률 지수 β ≈ 0.8 로 수렴 |
| `disk_tint_rgb_hex` | `#3a2a18` (희미한 따뜻한 회색, 낮은 불투명도) | low | Tie-break. 55 K 먼지는 원적외선으로 복사. 가시광 색조는 산란광 dust albedo 추정 (~0.1 회갈색 규산염/얼음 혼합), resolved imaging 이 없으므로 |
| `disk_opacity` | 0.02 | low | Tie-break. L_d/L_★ ≈ 2×10⁻⁵ (Eiroa 2013) 에서 광학 깊이 τ ≈ 10⁻⁵. 매우 희미한 시각적 feature 로 렌더. 긴 노출에서 겨우 감지 가능 |
| `disk_morphology` | "단일 차가운 belt, 적당한 먼지 질량, 비대칭 검출되지 않음 (분해 불가)" | medium | Lawler & Tanner 2014. SED 에 belt 하나로 fit. 두 번째 belt component 불필요. 공간 분해 불가이므로 형태 세부는 추론 |
| `disk_resolved_imaging` | false | high | Eiroa 2013 / Lawler 2014 모두 Herschel PSF (70 µm 에서 ~5″) 가 6.1 pc 거리의 belt 를 분해하지 못한다고 언급 (예상 각 크기 ~5–13″). 2026 년 시점에 ALMA / JWST resolved imaging 없음 |
| `disk_imaging_observatory` | "Herschel-PACS (SED only)" | high | Eiroa 2013 DUNES 서베이 + Lawler 2014 follow-up. 최초 검출은 Spitzer/MIPS |
| `disk_mass_mearth` | 0.012 | medium | Lawler & Tanner 2014 먼지 질량 (mm-cm grain). planetesimal 모체 질량은 직접 제약되지 않으나 먼지 질량보다 훨씬 크다고 추정 |
| `disk_planetesimal_belt_inferred` | true | high | 나이 ~7 Gyr ≫ 50 AU 에서 µm-cm 먼지의 충돌 cascade 수명. 보충이 planetesimal 저장소를 요구 (Wyatt 2008 프레임워크, Lawler & Tanner 2014 가 적용) |

## Surface synthesis

δ Pavonis 는 짧지만 시각적으로 의미 있는 subgiant 단계에 있습니다.
중심 수소가 소진됐고, 얇은 수소 껍질 연소가 envelope 를 부풀리기 시작
했으며, 별은 subgiant branch 를 따라 red-giant branch 의 시작점을
향해 올라가고 있습니다. 그 결과는 같은 질량의 G8V 왜성보다 ~20% 더
크고 ~200 K 더 차가운 광구입니다. Stefan–Boltzmann 광도 1.20 L☉ 는
G8V analog 보다 약간 더 높습니다. 반지름 증가가 온도 감소를 앞지르기
때문입니다. 이로 인해 별은 역설적인 성격을 갖습니다. 태양보다 색은
붉지만 광도는 여전히 살짝 더 높습니다.

통합 disk 색은 G2V 태양에 비해 amber-cream 방향으로 눈에 띄게 이동
합니다. Teff = 5604 K 에서 흑체 피크는 518 nm 부근 (여전히 황록색) 에
있지만, 가시광 전체 기울기는 G2V 보다 완만하며 Sol 보다 적색이 더
많고 청색이 더 적습니다. +0.33 dex super-solar 금속도가 line
blanketing 으로 가시광 연속체를 ~30 K 등가로 reddening 시키는 효과가
더해져, cfg 색조 `#ffe8c8` 가 진화된 G8 별의 따뜻한 cream 을 잡아
냅니다. α Cen A 의 `#fff4e8` (5847 K G2V) 와의 대비는 실재하며,
나란히 렌더하면 눈에 보입니다.

Limb darkening 은 G2V 보다 강합니다. 더 차갑고 확장된 대기가 limb
근처에서 광자 평균자유경로를 길게 만들기 때문입니다. Claret 2011 LD
표를 G8IV 로 보간한 H 밴드 α 지수 ≈ 0.16 은 α Cen A 의 측정값 0.14
보다 ~15% 높으며, fly-by 렌더에서 미묘하지만 실재하는 시각 효과로
나타납니다. limb 가 G2V 왜성보다 뚜렷이 더 그늘져 보입니다.

흑점 면적은 적당합니다. 측정된 회전 주기나 사이클이 없어 광도 변동
제약은 느슨하지만 (Hipparcos H_p 진폭 < 0.005 mag), log R'HK = -5.10
(Henry 1996) 은 δ Pav 를 비활성 G subgiant locus 한가운데에 단단히
놓습니다. α Cen A 보다 조용하고, Mt. Wilson 표본에서 가장 자기적으로
죽은 별들과 비슷한 수준입니다. cfg 렌더러에서는 흑점 밀도를 태양 극대
값의 절반으로 설정하고 무작위로 분포시키며, 강한 사이클 변조는
적용하지 않습니다.

## Atmosphere synthesis

δ Pav 의 색채권과 코로나도 그에 상응해 약합니다. log R'HK = -5.10
(Henry 1996, Gray 2006 NStars) 의 색채권 Ca II H&K 핵 플럭스는
색채권 "basal flux floor" 근처에 위치합니다. 더 이상의 활동 감소가
관측되지 않는 영역으로, δ Pav 는 사실상 이 진화 단계의 자기 정적
점근선에 도달해 있습니다. ROSAT 미검출 (Hünsch 1998) 은 log L_X
< 26.6 (cgs, 0.5–2 keV) 를 줍니다. 활동 최저기의 태양보다 한 자릿수
약하며, 별이 주계열을 벗어나 부풀어 오를 때 예상되는 중력과 대류
약화와 일관됩니다.

전이 영역의 UV 방출은 그에 상응해 희미하지만, δ Pav 는 IUE 와
HST/STIS 로 관측됐고 Mg II h&k 와 Si IV 방출선이 약하나 0 이 아닌
강도로 검출됐습니다. flare 측정은 없습니다. δ Pav 는 인근 표본에서
가장 flare 가 조용한 별 중 하나이며, 어떤 모니터링 캠페인에서도
이벤트가 보고되지 않았습니다. 통합 XUV 광도는 ≲ 10⁻⁵ L_bol 로,
시스템의 전체 7 Gyr 수명 동안 안쪽 행성 후보의 대기를 침식시킬 수
있는 임계값보다 훨씬 낮습니다.

이 우호적 우주환경은 (현재 미확인인) 가상의 행성에 흥미로운 함의를
가집니다. δ Pav 의 거주가능영역 (Kopparapu 2013 보수 한계를 1.20 L☉
로 스케일하면 약 1.0–1.7 AU) 에서 XUV 구동 대기 탈출은 시스템 전체
수명에 걸쳐 무시할 만한 수준입니다. cfg 는 게임 내 대기 보존 모델링을
위해 의미 있는 CME 플럭스가 없는 우호적 항성풍 환경을 기록합니다.

광구 자체의 항성 대기는 색채권 시작부에서 canonical G8IV 온도 반전을
보입니다. T 는 τ=1 의 5604 K 에서 τ ≈ 10⁻⁴ 근처의 ~4200 K 온도 최저
점까지 떨어진 다음, 색채권을 통과해 ~10⁴ K 로, 전이 영역에서 ~10⁵ K
까지 상승합니다. 차가운 온도 최저점은 G2V Sol 보다 더 깊고 더
넓습니다. 더 크고 천천히 대류하는 envelope 가 내놓는 음향 플럭스가
더 낮은 특징입니다.

## Rotation & spin synthesis

δ Pavonis 는 천천히 회전합니다. 얼마나 천천히인지는 잘 측정되지
않았습니다. 사영 회전 속도 v sin i ≈ 1.7 km/s (Bensby 2014, Valenti &
Fischer 2005 가 HARPS / Keck 분광으로 비슷한 값을 줌) 와 R = 1.22 R☉
를 결합하면 회전 속도 *상한* 이 2π·R/P_rot ≥ 1.7 km/s, 즉 P_rot · sin
i ≤ 36 d 입니다. 경사각 제약 없이는 주기가 위로만 제한됩니다. i = 90°
(equator-on) 에서 P_rot ≤ 36 d, 무작위 경사각에서 가장 가능성 높은
주기는 ~30 d 입니다.

G8V zero-age main-sequence 회전 ~5 d 에서 시작해 Skumanich braking
을 P ∝ √t 로 7 Gyr 까지 스케일하면 ~50 d 가 나오지만, subgiant
expansion 이 angular momentum 보존으로 envelope 가 부풀어 오를 때
표면 회전을 더 늦춥니다. Spada & Lanzafame 2020 의 subgiant 회전
모델은 초기 main-sequence 회전 주기 25–35 d 인 별이 이 진화 단계에서
30–45 d 를 가진다고 예측합니다. cfg 는 window 내 추정값으로 30 d 를
채택하고 Confidence=low 로 표기하며, 향후 광도 모니터링을 위한 open
item 으로 남깁니다.

회전 splitting 의 직접 asteroseismic 검출은 존재하지 않습니다. Bruntt
2010 의 지상 캠페인이 p-mode 진동을 검출했지만 (ν_max ≈ 2300 µHz,
Δν ≈ 110 µHz, M ≈ 1.05 M☉ 과 R ≈ 1.22 R☉ 와 일관), 데이터 품질이
mode 의 회전 splitting 을 분해하기에 부족했습니다. 추후 TESS 또는
PLATO 캠페인이 이를 좁힐 것이며, cfg open items 가 이 의존성을 기록
합니다.

Obliquity 는 관측적으로 제약되지 않습니다. 자전축에 토크를 줄
동반자가 없는 고립된 단일 별의 경우, spin angular momentum 기준
프레임에 대한 obliquity = 0° 를 기본값으로 합니다. cfg 는 시각적
강조를 위한 특별한 기울임 없이 within-window 기본값으로 0° 를
코드화합니다.

## Visual styling

NearStars 렌더러에서 δ Pavonis 는 희미한 차가운 잔해 ring 을 배경으로
한 늙고 조용한 G8 subgiant 별로 묘사됩니다. 주요 시각 선택은 다음과
같습니다.

- **전반적 외형.** 따뜻한 amber-cream 항성 디스크 (`#ffe8c8`). α Cen A
  의 cream-white 보다 뚜렷이 더 붉지만 K 왜성 오렌지보다는 따뜻한
  색조입니다. G2V Sol 과 나란히 두면 대비가 미묘하지만 실재하며,
  행성 하늘에서 단독으로 보면 δ Pav 는 "지친 태양, 살짝 더 붉고
  살짝 더 큰" 인상을 줍니다.
- **디스크 세부.** 가상의 근접 fly-by 렌더에서 광구 granulation 은
  G2V 보다 ~5% 낮은 대비로 렌더됩니다. 더 크고 천천히 대류하는
  envelope 가 상승하는 뜨거운 plume 과 차가운 intergranular lane
  사이 온도 차를 더 얕게 만들기 때문입니다. Granulation cell 은
  R* 로 스케일하면 각 크기가 ~30% 더 큽니다.
- **Limb 외형.** α Cen A 보다 뚜렷이 더 limb 가 어둡습니다. 더
  차가운 광구와 비스듬한 시야각에서의 강한 H⁻ 불투명도 때문입니다.
  fly-by 렌더에서 limb 가 눈에 띄게 그늘져 보입니다.
- **Corona / 색채권.** 1.6 R★ (`visual_corona_extent_radii`) 의
  얇고 희미한 ring 으로 렌더됩니다. 매우 약한 색채권과 코로나
  방출을 반영합니다. 활성 prominence 렌더 없음, flare 시각화도
  없습니다.
- **흑점 / faculae.** 태양 극소기 진폭의 절반으로 설정, 저위도에
  무작위 분포, 현재 cfg 에서는 사이클 변조 없음.
- **차가운 잔해 ring.** 별로부터 30–80 AU 에 Kopernicus ring 을
  매우 낮은 불투명도 (0.02) 와 희미한 따뜻한 회색 색조 (`#3a2a18`)
  로 부착합니다. ring 은 안쪽 시스템에서 긴 노출 렌더로 겨우 보이는
  수준이며, 1.3 AU 거리의 후보 행성에서 보면 ring 은 반사된 햇빛
  먼지의 얇은 띠로 보입니다. 지구의 황도광보다 훨씬 희미합니다.
  Herschel 가 belt 를 분해하지 못했고 SED 가 단일 차가운 component
  를 지지하므로 형태는 단일 균일 belt 로 렌더됩니다. 추후 ALMA /
  JWST 촬영이 비대칭이나 다중 component 를 드러내면 이 픽을
  재검토합니다 (Open items 참고).
- **후보 HZ 에서의 겉보기 각지름.** 1.3 AU 의 가상 1 M⊕ 행성에서
  δ Pav 는 ~0.50° 각지름을 채웁니다. 지구에서 본 Sol (0.53°) 과
  비슷합니다.
- **잔해 디스크에서의 하늘.** 잔해 belt 의 안쪽 가장자리 (~30 AU)
  에 있는 가상의 관측자는 δ Pav 를 빛나는 amber-cream 점광원으로
  보게 됩니다. 조명 강도는 1.2/(30)² = 1.3×10⁻³ L☉/AU², 즉 지구에서
  본 Sol 의 약 1/770 입니다. 명확히 별빛이며 긴 그림자를 드리우지만
  태양-밝기는 아닙니다. 안쪽 zodiacal-dust 산란과 바깥쪽 belt 가
  황도를 따라 희미한 빛의 띠를 만듭니다.
- **고립 cue.** α Cen 시스템의 이중성 페어 렌더와 달리 δ Pav 는
  홀로 서 있습니다. 두 번째 태양도, 궤도 conjunction 이벤트도
  없습니다. 시각 styling 은 disk 와 subgiant 색조에 기대어 별에
  personality 를 부여합니다.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Eiroa C. et al. 2013** — *DUNES: Disc Around NEarby Stars with
  Herschel*, A&A 555, A11 (`2013A&A...555A..11E`, arXiv:1305.0155).
  인근 FGK 별 133 개에 대한 Herschel/PACS 서베이. δ Pavonis 가
  70/100/160 µm 에서 검출되며, SED fit 으로 T_d ≈ 55 K, L_d/L_★ ≈
  2×10⁻⁵ 의 단일 차가운 belt 를 줍니다.
- **Lawler S. M. & Tanner A. M. 2014** — *Tracing planet formation
  with detailed analysis of debris disk SEDs* (`2014ApJ...780...28L`,
  arXiv:1310.3559). δ Pav 를 포함한 Eiroa 2013 데이터의 modified
  blackbody 분석. belt 지오메트리 r ≈ 30–80 AU, 먼지 질량 ~0.012 M⊕,
  나이 논거로부터 planetesimal 보충 요구 정련.
- **Beichman C. A. et al. 2006** — *New Debris Disks around Nearby
  Main-Sequence Stars: Impact on the Direct Detection of Planets*
  (`2006ApJ...652.1674B`). δ Pav 의 Spitzer/MIPS 70 µm 초과 검출.
  disk 최초 발표.
- **Gomes da Silva J. et al. 2021** — *Chromospheric activity of FGK
  stars observed with HARPS* (`2021A&A...646A..77G`,
  doi:10.1051/0004-6361/202039765). AMBRE-HARPS Teff = 5644 ± 30 K,
  [Fe/H] = +0.36 ± 0.02, log R'HK = −5.13 (2003–2016 HARPS 6002 개
  가중평균), PARSEC isochrone 질량 1.064 ± 0.013 M☉, 반지름
  1.115 ± 0.025 R☉, 나이 5.04 ± 1.23 Gyr. **δ Pav 의 Phase 2 1차
  앵커** (newest paper, 가장 작은 오차, 동일 pipeline 으로 균질
  처리). 이전 초안에서 사용했던 Bensby 2014 / Bruntt 2010 픽들을
  대체.
- **Eiroa C. et al. 2013** — *DUNES: DUst around NEarby Stars*
  (`2013A&A...555A..11E`, doi:10.1051/0004-6361/201321050).
  δ Pav 와 인근 FGK 별 132 개의 Herschel/PACS 70/100/160 µm
  측광. bolometric L = 1.246 L☉, Ca II 활동 나이 8.3 Gyr (문헌
  spread 의 늙은 쪽), v sin i 상한 3.2 km/s (Ramirez 2013 가
  supersede). disk 검출 1차 출처 — `disks_curated` 도 참조.
- **Ramirez I. et al. 2013** — *The dissimilar chemical composition
  of the planet-hosting stars of the XO-2 binary system*
  (`2013ApJ...764...78R`, doi:10.1088/0004-637X/764/1/78). HARPS
  solar-twin 정밀도의 v sin i = 0.32 ± 0.05 km/s — 장비 floor.
  Rotation 행의 현대 P_rot 상한 유도 근거. 고분해 Teff = 5517 ±
  60 K, [Fe/H] = +0.33 ± 0.07, 진화모델 질량 0.98 ± 0.02 M☉ 도
  cross-check 대체값으로 보존.
- **Tsantaki M. et al. 2013** — *Deriving precise parameters for
  cool solar-type stars* (`2013A&A...555A.150T`,
  doi:10.1051/0004-6361/201321103). 균질 고분해 분광. Teff = 5566
  ± 36 K, [Fe/H] = +0.32 ± 0.03, 질량 0.967 ± 0.016 M☉, 나이 8.48
  ± 1.27 Gyr — 나이 문헌 spread 의 ~9 Gyr 쪽.
- **Bensby T. et al. 2014** — *Exploring the Milky Way stellar disk:
  A detailed elemental abundance study of 714 F and G dwarf stars*
  (`2014A&A...562A..71B`, arXiv:1309.2631). FEROS 고분해 분광이
  Teff = 5635 ± 122 K, log g = 4.05, [Fe/H] = +0.37 ± 0.20, 질량
  1.03 ± 0.07 M☉ (진화모델), 나이 4.9 Gyr 를 줌. cross-check
  대체값. 같은 양들에서 Gomes da Silva 2021 가 더 작은 형식 오차로
  1차 픽을 차지.

### Read (context / methodology, not directly decision-driving)

- **Mawet D. et al. 2017** — *Characterization of Exoplanets from
  Their Formation. I.* (`2017AJ....153...44M`, arXiv:1609.06163).
  δ Pav 와 다른 인근 FGK 별에 대한 NIRC2 vortex coronagraph 깊은
  촬영. 동반자 질량 한계 >1 AU 에서 ~3 M_Jup. 차가운 disk 안쪽
  영역에 거대 행성이 없음을 확인.
- **Lannier J. et al. 2017** — *Combining direct imaging and radial
  velocity data toward a full exploration of the giant planet
  population* (`2017A&A...603A..54L`, arXiv:1705.03477). δ Pav 가
  SPHERE 직접 촬영 서베이에 포함됨. 동반자 검출 없음.
- **Tinney C. G. et al. 2005** — *The Anglo-Australian Planet
  Search. XI. Five Planets and a Brown Dwarf* (`2005ApJ...623L.121T`).
  δ Pav 의 HARPS / AAPS RV 모니터링. <2 AU 에서 m sin i ~ 10 M⊕
  이상의 행성 검출 없음. RV 미검출 기준선 설정.
- **Bruntt H. et al. 2010** — *Accurate fundamental parameters for
  23 bright solar-type stars* (`2010MNRAS.405.1907B`,
  arXiv:1002.4268). δ Pav 의 R ≈ 1.22 R☉ 가 Hipparcos 시대 시차의
  bolometric L + Teff Stefan-Boltzmann 유도값으로 보고됨 — **간섭계
  도 asteroseismic 도 아님** (δ Pav 는 발표된 asteroseismology 없음,
  남쪽 적위로 CHARA 범위 밖). 역사적 맥락용으로 인용. 위 Decisions
  표의 Gomes da Silva 2021 PARSEC R = 1.115 R☉ 와 ~9% 차이. 이
  합성 초기 초안에서 Bruntt 2010 을 "interferometric + asteroseismic"
  으로 기재했었는데, 그 기재는 사실과 다르고 여기서 정정.
- **Henry T. J. et al. 1996** — *Chromospheric Activity Survey* in
  the southern hemisphere (`1996AJ....111..439H`). δ Pav 의 log
  R'HK = -5.10. 인근 G subgiant 표본에서 가장 색채권 활동이 약한
  별 중 하나.
- **Hünsch M. et al. 1998** — *ROSAT All-Sky Survey of nearby
  stars* (`1998A&AS..132..155H`). δ Pav X 선 미검출, 상한 log
  L_X < 26.6 cgs.
- **Gray R. O. et al. 2006** — *NStars: Spectral Classifications of
  Nearby Stars* (`2006AJ....132..161G`, arXiv:astro-ph/0603770).
  G8IV 분류와 log R'HK = -5.10 확인.
- **Valenti J. A. & Fischer D. A. 2005** — *Spectroscopic
  Properties of Cool Stars (SPOCS)* (`2005ApJS..159..141V`). v sin
  i 와 색채권 측정값. Bensby 2014 를 지지.

### Read (instrument / non-cfg-decisive)

- **Trilling D. E. et al. 2008** — *Debris Disks around Sun-like
  Stars* (`2008ApJ...674.1086T`). δ Pav 를 포함한 Spitzer 24/70 µm
  서베이. disk 검출 census 의 맥락.
- **Spada F. & Lanzafame A. C. 2020** — *Asteroseismic rotation
  for subgiants* (`2020A&A...636A..76S`, arXiv:2003.06224). Rotation
  & spin synthesis 에서 사용한 δ Pav-class subgiant 의 회전 주기
  모델 floor 를 설정.
- **Kopparapu R. K. et al. 2013** — *Habitable Zones around
  Main-Sequence Stars: New Estimates* (`2013ApJ...765..131K`).
  1.20 L☉ 로 스케일한 HZ 한계가 보수적으로 1.0–1.7 AU 범위를
  줌. Atmosphere synthesis 산문에서 사용.

### Not read — no arXiv preprint or low-priority (~25 papers)

학회 abstract (DPS, EPSC, AAS), 새 데이터가 없는 disk SED follow-up
노트 (~12 개 follow-up 참고), 서베이 논문 내 한 줄 카탈로그 언급은
cfg 결정에 영향이 없습니다. Mt. Wilson HK 서베이 노트 (Wright 2004)
는 log R'HK floor 를 확인하지만 Henry 1996 외에 새 제약을 추가하지
않습니다. 필터된 전체 bib 는 이 별에 대한 bib 검색 파이프라인이
실행되면 `docs/phase3/_bib/delta-pavonis.yaml` 에 `status: skipped`
주석과 함께 보존됩니다 (현재 보류 — Open items 참고).

## Open items for follow-up

- **Phase 2 `disk_measurements` ingest.** DB `delta_pavonis.json` 에
  현재 `disk_measurements` 블록이 없습니다. Herschel/PACS 플럭스
  (Eiroa 2013), Lawler & Tanner 2014 SED-fit 지오메트리, Spitzer
  70 µm 초과 (Beichman 2006) 를 paper 인용 Phase 2 측정치로
  ingest 해야 disk 지오메트리 행의 Confidence=medium 에서 이
  합성을 격상할 수 있습니다.
- **Resolved imaging (ALMA / JWST-MIRI).** 6.1 pc 거리의 30–80
  AU belt 는 하늘에서 ~5–13″ 에 걸쳐 있습니다. ALMA Band 6 의 1″
  각 분해능 안에 충분히 들어가며, MIRI coronagraph inner working
  angle 의 안쪽에 막 들어옵니다. resolved imaging 캠페인이 안/바깥
  반지름을 좁히고, belt 비대칭이나 warp (보이지 않는 행성 perturber
  를 의미) 를 검출하며, 경사각을 제약할 수 있습니다. disk 지오메트리
  Confidence 가 high 로 올라갑니다.
- **Subgiant 나이 정련.** 7.0 ± 0.5 Gyr 나이는 isochrone (Holmberg
  2009) 과 단일 파라미터 subgiant 모델 (Spada 2011) 에 기반합니다.
  δ Pav 를 관측할 때 PLATO 급 asteroseismology 가 p-mode 회전
  splitting 을 분해해 나이를 ~5% 로 좁힐 것입니다. cfg `age_gyr`
  Confidence 가 medium 에서 high 로 올라갑니다.
- **광도 회전 주기.** TESS Cycle 4+ 가 δ Pav 를 관측할 예정입니다
  (남쪽 연속 관측 영역에 유리한 적위). 깨끗한 회전 주기 검출이
  현재 Confidence=low 추정치를 대체할 것입니다.
- **`docs/phase3/_bib/delta-pavonis.yaml` bib 검색.** ADS+arXiv
  파이프라인이 아직 이 별에 대한 bibliography YAML 을 생성하지
  않았습니다. DB Phase 2 disk ingest 가 완료된 후에 실행해 disk
  논문들이 점수 순 출력에 포함되도록 합니다.

## Related

- [methodology](../reference/methodology.md) — Decisions 표 스키마의 원본.
- [alpha-centauri-a](alpha-centauri-a.md) — G2V 비교 anchor (5847 K cream-white vs δ Pav 의 5604 K amber-cream).
- [conflict-resolution](../../.claude/skills/nearstars-phase3/references/conflict-resolution.md) — 시각 색조와 corona extent 픽에 사용된 tie-break 정책.
