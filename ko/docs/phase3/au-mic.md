<!-- AU Mic Phase 3 합성. cfg-ready 결정과 근거 -->
# AU Microscopii — Phase 3 Synthesis

AU Microscopii (HD 197481, GJ 803, HIP 102409) 는 9.714 pc 거리의
가까운 M1Ve 전주계열 왜성으로 (Gaia DR3 시차 102.94 ± 0.02 mas,
이 DB), NearStars 카탈로그 전체에서 가장 어린 별 중 하나입니다.
나이는 ~22 Myr (Mamajek & Bell 2014 의 β Pictoris 운동성단
isochrone 나이) 이고, AU Mic 은 그 운동성단의 대표 멤버입니다.
기본 파라미터는 frozen Phase 2 레이어에서 가져옵니다.
R = 0.862 ± 0.052 R☉ (Gallenne 2022 VLTI/PIONIER, 유일한 refereed
간섭계 반지름 — 널리 인용되는 0.75 R☉ 는 refereed 가 아닌 White 2019
AAS 초록으로 거슬러 올라갑니다. Canonical alternatives 참조),
M = 0.50 ± 0.03 M☉ (Plavchan 2020 PMS isochrone), Teff = 3665 ± 31 K
(Cristofari 2023 SPIRou 대기 fit) 입니다. 광도는 L = 0.102 L☉
(Donati 2023, log L/L☉ = −0.99 ± 0.01) 로, M1V 치고는 높은데
AU Mic 이 아직 주계열로 수축 중이라 약간 부풀어 있기 때문입니다.

카탈로그의 다른 M 왜성과 AU Mic 을 가르는 결정적 특징은
**분해된 가장자리 정면 잔해 원반** (HST/STIS — Krist 2005, 더 깊은
HST/STIS 재방문 — Schneider 2014, VLT/SPHERE 편광 영상 — Boccaletti
2015, 2018) 입니다. 안쪽 가장자리 ~35 AU 부터 바깥쪽 후광 ~210 AU
까지 뻗어 있으며, edge-on 에서 ≈ 1° 안쪽 각도로 관측됩니다.
Multi-epoch SPHERE 영상은 원반 남동쪽 ansa 의 **움직이는 substructure**
를 분해했고 (Boccaletti 2015 최초 검출, 2018 후속), 바깥 방향으로
4–10 km/s 로 움직입니다 — 케플러 운동보다 빠르며, 현재로서는
항성풍 / 복사압이 planetesimal 충돌과 상호작용해 발생시킨 먼지
ridge 로 가장 잘 설명됩니다 (Chiang & Fung 2017). 거기에 자기 활동도
얹힙니다. kG 급 표면 자기장 (Donati 2023 Zeeman-Doppler imaging),
10³⁴–10³⁵ erg 까지 가는 super-flare (Cully 1993, Smith 1981,
eRosita, Tristan 2023 TESS 센서스), 광도 측정 자전 주기 4.86 d 와
다-흑점 복잡도 (Plavchan 2020 TESS), 조용한 태양 평균보다 수십
배 이상인 X 선 광도까지. AU Mic 은 어느 기준으로 보든 NearStars
카탈로그에서 가장 극적인 단독 광원입니다.

알려진 네 행성 (AU Mic b — Plavchan 2020 의 통과 hot Neptune,
AU Mic c — Martioli 2021 의 통과 sub-Neptune, AU Mic d — Wittrock
2023 의 TTV 전용 지구질량 후보, AU Mic e — Donati 2025 ESPRESSO RV
후보, 논란 있음) 은 모두 ~0.2 AU 안쪽을 돌며 원반 안쪽 가장자리
훨씬 안쪽에 있습니다. 이 항성 합성에서는 행성은 다루지 않고
follow-up 워크스페이스용으로 표시만 해 둡니다. AU Mic 은 넓은
공통 고유운동 동반자 **AT Microscopii** (그 자체로 단주기 M-왜성
이중성) 도 거느리는데, ~46 400 AU (~1.22°) 떨어져 있고 AT Mic
역시 β Pic MG 멤버이며 AU Mic 과 ~22 Myr 나이를 공유합니다.
이 글 작성 시점에 별도의 NS DB 엔트리는 없습니다.

**NearStars 시나리오 선택. 매우 어리고 깊은 붉은빛의 M1Ve flare star
로, 살짝 부풀고 전주계열에 있으며, kG 급 자기장과 잦은 super-flare,
> 10% 흑점 면적, 그리고 35–210 AU 까지 뻗는 분해된 가장자리 정면
잔해 원반에 애니메이션된 방사형 움직임 substructure 가 얹힌 모습으로
렌더링합니다.** 항성 레이어는 frozen Phase 2 출처 (Gallenne 2022
간섭계, Plavchan 2020, Cristofari 2023, Donati 2023, Mamajek & Bell
2014) 위에 다시 정박했고, 반지름 / 질량 / 광도의 divergence 는
문서화했습니다. tie-break 픽은 시각 hex 색조, 원반 substructure
애니메이션 선택, flare 색, 흑점 면적 사이클 위상에 관한 것입니다.

## Decisions

| Field | Value | Confidence | Basis |
|---|---|---|---|
| `spectral_type` | M1Ve | high | Hawley 1996. Gaia DR3 spectype = M1VeBa1 |
| `mass_msun` | 0.50 ± 0.03 | high | Plavchan 2020 — PMS isochrone (Phase 2 recommended, 커뮤니티 표준). Donati 2023 Dartmouth 0.60 과 DOCUMENTED DIVERGENCE (Canonical alternatives 참조) |
| `radius_rsun` | 0.862 ± 0.052 | high | Gallenne 2022 — VLTI/PIONIER 간섭계, θ_LD 0.825 mas (Phase 2 recommended. 유일한 refereed 간섭계 반지름). refereed 가 아닌 White 2019 AAS 초록의 0.75 와 DOCUMENTED DIVERGENCE (Canonical alternatives 참조) |
| `teff_k` | 3665 ± 31 | high | Cristofari 2023 — 자기장 포함 SPIRou 대기 fit (Phase 2 recommended. Gaia 3518 을 대체). Donati 2023 V−I 색은 3700 ± 70 |
| `luminosity_lsun` | 0.102 ± 0.002 | high | Donati 2023 — log(L/L☉) = −0.99 ± 0.01 (M_bol + BC + 거리. Phase 2 recommended). Plavchan 2009 SED 는 0.09 (Canonical alternatives 참조) |
| `metallicity_fe_h_dex` | +0.12 ± 0.10 | medium | Cristofari 2023 — SPIRou 직접 분광 [M/H] (Phase 2 recommended. [α/Fe] = 0 이라 [M/H] ≈ [Fe/H]. β Pic MG 평균을 대체) |
| `age_gyr` | 0.023 ± 0.003 | high | Mamajek & Bell 2014 — β Pic MG isochrone 22 ± 3 Myr 를 리튬 결핍 경계 나이와 조화. ~12 Myr 운동학 나이는 명시적으로 기각 |
| `rotation_period_days` | 4.86 | high | Plavchan 2020. TESS 광도 자전 변조 (다-흑점, 주성분 4.863 d) |
| `activity_cycle_years` | null | low | AU Mic 나이에서 사이클 분해 불가 — 전주계열 포화 dynamo, 장기 변조 관측 없음. null 유지, 임의값 금지 |
| `x_ray_log_lx_cgs` | 29.35 | high | Tsikoudi & Kellett 2000 — ROSAT 정적 Lx = 2.24e29 erg/s, log(Lx/Lbol) ≈ −3.24, 포화 영역 (Phase 2 recommended 활동 proxy). NOTE. AU Mic 의 frozen Phase 2 레이어에는 색채권 log R'HK 가 없음 — X 선 지수가 활동 proxy 임 (앞서의 −3.9 log R'HK 행은 출처 없는 placeholder 라 제거) |
| `flare_rate_per_day` | 5.6 | high | Tristan 2023. TESS Sectors 1+27 flare 센서스. TESS sector 당 (~27.4 d) 26.3 flare, ~10³¹ erg 위 적분 |
| `flare_energy_log_erg_max` | 34.5 | medium | Cully 1993 EUVE 1992 mega-flare. Tristan 2023 의 백색광 대역 ≥ 10³⁴ erg TESS 광학 이벤트 상단과 일관 |
| `magnetic_dipole_strength_kG` | 0.55 | high | Donati 2023 — 대규모 자기장 550 ± 30 G (ZDI, 대부분 poloidal/axisymmetric) |
| `magnetic_total_field_kG_rms` | 2.61 ± 0.05 | high | Donati 2023 — Zeeman broadening 으로 구한 소규모 평균 자기장 ⟨B⟩ (Phase 2 DB meta_notes) |
| `spot_coverage_max_fraction` | 0.12 | high | Plavchan 2020 + Donati 2023. 다-흑점 모델은 디스크 ≥ 10% 면적을 요구. TESS 광도곡선의 가시적 비대칭 |
| `limb_darkening_alpha_h` | ~0.45 | low | Tie-break. AU Mic 직접 측정 없음. Claret 2018 M-왜성 격자에서 Teff = 3500 K interpolation. interesting-first 가 가장자리 어두워짐을 살짝 보존 |
| `visual_surface_tint_hex_primary` | `#e0743a` (M1V 의 깊은 주황-빨강) | medium | Teff 3665 K 흑체 + 분자 밴드 억제 (hex 유지. 3518→3665 K 이동은 렌더 허용 오차 안이라 M5.5 Proxima `#c54c2a` 보다 살짝 더 따뜻/덜 붉음. Teff 가 ~620 K 더 높음) |
| `visual_flare_color_hex` | `#ff9050` (백색광 flare 연속체. T_bb ~9000 K flare ribbon 으로 정적 상태보다 살짝 푸름) | medium | Kowalski 2013 dM-flare 연속체 분해. 순수 Hα reddening 과의 tie-break — 어두운 붉은 정적 디스크 위에서 flare 가 눈에 띄게 밝아지도록 선택 |
| `v_sin_i_km_s` | ~9.0 | medium | R = 0.862 R☉ 과 P_rot = 4.86 d 에서 유도 (edge-on, sin i ≈ 1). Kochukhov & Reiners 와 일관. 옛 0.82 R☉ 에 묶인 ~8.5 를 대체 |
| `stellar_color_temp_k` | 3665 | high | Teff 유도 (Cristofari 2023) |
| `visual_spot_coverage_max` | 0.12 | high | `spot_coverage_max_fraction` 과 동일. 활동 애니메이션 레이어용 |
| `disk_present` | true | high | Krist 2005 HST/STIS 최초 분해 edge-on 영상 |
| `disk_inner_radius_au` | 35 | high | Schneider 2014 HST/STIS 깊은 영상. ~35 AU 표면 밝기 break. Strubbe & Chiang 2006 SED-fit 과 일관 |
| `disk_outer_radius_au` | 210 | high | Schneider 2014. ~210 AU 까지 확장된 후광, 그 너머로는 STIS 감도 아래로 떨어짐 |
| `disk_dust_temperature_k` | 50 | high | Chen 2005 Spitzer SED-fit 차가운 성분. 0.092 L☉ host 주위 35 AU planetesimal 휘저음 벨트와 일관 |
| `disk_tint_rgb_hex` | `#fbeacb` (옅은 크림색, 붉은 M1V 빛 아래 푸른 쪽으로 기우는 반사율) | medium | CORRECTED. 원반은 무채색이 아니라 반사율이 측정상 푸릅니다 (Krist 2005, B/I ~ 1.6. Fitzgerald 2007 근적외선에서 푸름. Graham 2007 의 a ~0.1 µm 다공성 blowout 미세입자). Mie 산란 합성 결과, 그 강한 청색 산란이 붉은 M1V 별빛을 무채색 회색보다 더 푸르고 밝은 쪽으로 옮겨 옅은 크림색 절대색이 나옵니다 (유명한 "AU Mic 블루" 는 원반과 별의 상대 반사율이지 절대 색조가 아닙니다) |
| `disk_opacity` | 0.4 | medium | Boccaletti 2018 SPHERE 편광 강도비. 중간 범위 opacity 렌더가 원반 가시성과 배경별 가시성을 모두 보존 |
| `disk_morphology` | edge-on planetesimal 휘저음, 애니메이션된 방사형 움직임 substructure (바깥 방향 4–10 km/s) | high | Boccaletti 2015 + 2018 multi-epoch SPHERE 의 빠르게 움직이는 피처 검출. Chiang & Fung 2017 의 항성풍 발사 먼지 ridge 모델 |
| `disk_resolved_imaging` | true | high | HST/STIS (Krist 2005, Schneider 2014). VLT/SPHERE (Boccaletti 2015, 2018) |
| `disk_imaging_observatory` | HST-STIS + VLT-SPHERE | high | 위와 동일 |
| `disk_imaging_inclination_deg` | 89.5 | high | Krist 2005. Schneider 2014. SPHERE 가 i ≈ 89° 확인 (edge-on 에서 ~1° 안쪽) |
| `disk_planetesimal_belt_inferred` | true | high | 풍압이 바깥으로 가속할 먼지를 공급할 부모 벨트가 필요. Strubbe & Chiang 2006 의 표준 birth-ring 모델 |
| `visual_companion_event_disk_substructures_animated` | true | low | Tie-break. 문헌이 substructure 를 4–10 km/s 로 움직인다고 기술. cfg 는 (정적 텍스처가 아닌) 애니메이션을 채택 — 애니메이션이 AU Mic 원반의 시각적 정체성이므로 interesting-first 적용 |

## Surface synthesis

AU Mic 의 광구는 카탈로그에서 가장 깊은 붉은 연속체 중 하나입니다 —
다만 Proxima 나 TRAPPIST-1 host 보다는 따뜻합니다. Teff = 3665 K
(Cristofari 2023) 와 R = 0.862 R☉ (Gallenne 2022) 에서 광도는
0.102 L☉ (Donati 2023. 태양의 약 1/10) 로, 대부분의 플럭스가
0.7–2.0 μm 사이로 나옵니다. TiO 밴드가 6500 Å 아래 가시 연속체를
가파르게 억제하고, VO 와 물 밴드가 근적외선을 빚어냅니다. AU Mic
이 전주계열 (~22 Myr) 이라 반지름은 정착된 M1V 보다 부풀어 있는데,
Gallenne 2022 간섭계 반지름 0.862 R☉ 는 22 Myr / 0.50 M☉ 의 PARSEC
및 Baraffe 전주계열 진화 트랙과 일관됩니다.

표면의 결정적 특징은 **흑점 복합체** 입니다. Plavchan 2020 TESS
광도는 적어도 세 개의 지속적인 활동 경도를 요구하는 다중 모드
자전 변조를 보이며, Donati 2023 ZDI inversion 은 이를 ±30° 부터
±60° 사이 위도 띠로 분해합니다 (전체 디스크의 > 10% 면적). cfg
렌더링에서는 `spot_coverage_max_fraction = 0.12` 로 표현되며,
활동 애니메이션 레이어가 4.86 일 자전 주기에 맞춰 흑점 위치를
순환시킵니다. 가시 흑점은 광구보다 ~500 K 어둡고 (Δ(B-V)_spot
≈ +0.3), flare 없는 구간에서도 V 밴드 광도 진폭 ~3% 를 만듭니다.

Granulation, faculae, plage 도 있지만 통합 광도에 대한 기여는
흑점 신호보다 작습니다. 전주계열 수축 덕에 대류 envelope 가
정착한 M-왜성보다 더 격렬합니다 — granulation 셀은 압력 스케일
높이로 스케일하는데, 부푼 반지름 덕에 그 값이 더 큽니다. 서브-각초
렌더링 기준으로 ~50 km granule 을 예상합니다. Beeck et al. (2013,
Donati 2023 §3 경유 인용) 의 3D-RHD 모델이 게임 내 애니메이션
광구 텍스처에 쓸 granulation 대비와 시간 스케일 격자를 제공합니다.

광물학적으로 광구는 super-solar [Fe/H] ≈ +0.12 (β Pic MG 평균 —
Shkolnik 2017. DB 에 AU Mic 직접 측정은 없음) 로, 태양형 metallicity
M1V 보다 SED 를 장파장 쪽으로 살짝 reddening 시킵니다. 게임 내
조명 색온도의 분광 분해능에서는 보이지 않지만, 순수한 3665 K
Planckian 보다 더 깊은 붉은빛의 `#e0743a` 를 정당화하는 근거가
됩니다.

## Atmosphere synthesis

AU Mic 은 태양 근방에서 색채권과 코로나가 가장 활동적인 별 중
하나입니다 — 외곽 대기가 행성 b/c/d/e 와 잔해 원반의 우주환경
물리 대부분을 구동합니다. 정적 X 선 광도는 log L_X ≈ 29.35 cgs
(Tsikoudi & Kellett 2000 ROSAT, Lx = 2.24e29 erg/s) 로, AU Mic 을
**포화 영역** 에 놓습니다. log(L_X/L_bol) ≈ −3.24 은 빠르게 자전
하는 M-왜성에 대한 경험적 상한 근처입니다. 코로나는 flare 동안
~10⁷ K 까지 도달합니다.

**Super-flare 가 에너지 예산을 지배합니다.** Cully 1993 EUVE 의
1992 년 9 월 이벤트는 EUV 만 ~10³⁴–10³⁵ erg 를 방출했고 — 당시
까지 기록된 항성 단일 flare 로는 가장 컸습니다. Tristan 2023
(arXiv:2306.00077) 은 TESS Sectors 1+27 flare 센서스에서 sector
당 ~10³¹ erg 위 ≥ 150 이벤트를 셌습니다. 적분하면 이 에너지
임계값 위 평균 flare 율은 5.6 이벤트/일이며, 누적 flare 빈도
분포는 연간 ≥10³⁴ erg 이벤트가 여러 번 발생하는 수준까지 뻗습니다.
Davenport et al. 2020 (TESS 첫해 M-왜성 flare 서베이) 도 같은
flare 율 분포 형태를 확인하며, AU Mic 은 활동적 M1V locus 의
고에너지 꼬리에 위치합니다.

색채권은 Hα 방출 (정적에서 EW ≈ 1 Å, flare 동안 수 Å), He I
10830 Å 흡수-방출 순환, 폭이 넓은 Mg II h&k 로 채워집니다. Lyman-α
의 UV 플럭스는 태양의 10²–10³ 배 높습니다. 전이 영역은 매우
밝습니다 — Loyd et al. 2018 이 포화 활동 locus 와 일관된 FUV
플럭스를 측정했습니다. 활동 사이클이 이를 변조하지 않는데 —
AU Mic 은 사이클을 보이기에는 너무 어리고 너무 포화돼 있어 —
고에너지 출력은 수십 년 단위에서 거의 일정하며, 준-확률적인
super-flare 가 박자를 찍습니다.

항성풍도 그에 맞춰 강합니다. 질량 손실률은 ~10× 태양으로
추정됩니다 (Plavchan 2020 §4 배경 맥락. Boccaletti 2015 + Chiang &
Fung 2017 의 원반 substructure inversion). 이 바람이 움직이는 원반
substructure 를 발사하는 엔진입니다 — 35 AU 에서 원반 먼지에
가해지는 바람의 ram 압이 작은 입자를 4–10 km/s 로 바깥쪽으로
가속하기에 충분하며, 이는 Boccaletti 가 측정한 피처 속도와 견줄
만하고 같은 반지름 케플러 운동보다 수십 배 큽니다. NearStars
cfg 렌더링에서는 이 사실이 원반 애니메이션을 항성 활동 레이어에
묶습니다 — super-flare 이벤트 후 substructure 가 더 빨라지고
사이에는 느려집니다. 이벤트 빈도가 충분히 높아 관측 시간 척도
에서 원반이 사실상 "정적" 으로 보이지 않습니다.

게임 내 행성 대기에 대한 함의는 가혹합니다 — AU Mic b 거리
(0.07 AU) 에서 XUV 플럭스는 지구의 ~10⁴ 배이며, super-flare 피크는
거기서 또 한 자릿수 더 큽니다. 가까운 어떤 행성이든 대기 보전을
위해서는 강한 자기 차폐 또는 지속적인 outgassing 원천이 필요하며,
이것이 b/c/d/e 의 Phase 3 follow-up 선택지를 제약합니다.

## Rotation & spin synthesis

4.86 일 자전 주기 (Plavchan 2020 — TESS 광도 변조) 는 주계열 M-왜성
기준으로 빠르지만 전주계열 M1V 의 특징입니다. 22 Myr 의 AU Mic
에서 Skumanich 식 braking 은 막 작동하기 시작했을 뿐이라, 자기
braking 으로 spin down 할 시간이 없어 자전이 빠릅니다. 자전축은
edge-on 과 일관됩니다 (v sin i ≈ 9 km/s 는 R = 0.862 R☉ 과 P =
4.86 d 에서 sin i ≈ 1 을 함의), 자전축을 원반의 edge-on 경사 ~89°
와 정렬시킵니다. 이는 일관된 각운동량 장에서 태어난 별에 기대되는
결과입니다.

여러 활동 경도가 단일 사인파로는 모델링할 수 없는 복잡한 자전
광도곡선을 만듭니다. Plavchan 2020 은 적어도 세 개의 서로 다른
경도에서 흑점 영역을 찾았고, Donati 2023 ZDI 가 이를 위도 띠로
분해했습니다. cfg 의 활동 애니메이션 레이어는 4.86 d 자전에 맞춰
흑점 위치를 순환시키며, 다-경도 패턴은 게임 내 광도곡선이 단일-흑점
별의 자전 고조파 함량의 약 3 배를 갖게 만듭니다.

Asteroseismic 제약은 불가능합니다 — AU Mic 은 너무 차갑고, 너무
작고, 자기 활동이 너무 강해 p-mode 진동이 검출 가능하지 않습니다.
차등 회전은 α ≈ 0.04 (Donati 2023, 태양 값과 견줄 만함) 로
제약되지만 cfg 에 렌더링하기에는 너무 미묘합니다.

자전축 경사는 원반과 v sin i 로 90° 의 ~1° 안쪽에 고정됩니다.
NearStars cfg 는 시각적 일관성을 위해 원반면과 정렬한 자전축을
채택합니다 — 플레이어가 AU Mic 을 edge-on (원반이 보이는 유일한
방향) 으로 볼 때, 자전축도 거의 천구면 안에 놓입니다. 이는
흑점 피처의 자전 단축 (고위도에서의 foreshortening) 이 상당하며
반드시 렌더링되어야 함을 의미합니다.

## Canonical alternatives

**반지름 — refereed 간섭계 vs 커뮤니티 표준값.** cfg 는 Gallenne
2022 (VLTI/PIONIER, θ_LD 0.825 mas) 의 R = 0.862 ± 0.052 R☉ 를
채택합니다. 유일한 *refereed* 간섭계 반지름이기 때문입니다. 널리
인용되는 0.75 R☉ 는 White et al. 2019 로 거슬러 올라가는데, 이는
refereed 가 아닌 AAS 학회 초록으로만 존재합니다 (저널 논문도 arXiv
도 없음). Donati 2023 은 L + Teff 로부터 0.78–0.82 R☉ 를 추정해 둘
사이에 놓이면서 더 큰 값을 지지합니다. 미래 cfg 가 0.75 커뮤니티
값을 대체 시나리오로 노출할 수는 있지만, 원칙적 기본값은 refereed
간섭계 반지름입니다.

**질량 — Plavchan vs Donati.** cfg 는 M = 0.50 ± 0.03 M☉ (Plavchan
2020 PMS isochrone, 모든 행성 논문에 전파된 커뮤니티 표준) 를
씁니다. Donati 2023 은 Dartmouth 트랙에서 더 높은 0.60 ± 0.04 M☉
를 유도합니다.

**광도 — Donati vs Plavchan.** cfg 는 L = 0.102 L☉ (Donati 2023,
log L = −0.99) 를 씁니다. Plavchan 2009 의 SED 는 0.09 L☉ 를
줍니다. 둘은 ~10% 안에서 일치합니다.

**활동 지수.** AU Mic 은 대류 dynamo 를 가진 M 왜성이라 log R'HK
가 원리상 물리적으로 정의 가능하지만, frozen Phase 2 레이어에는
색채권 log R'HK 가 없습니다 — cfg 활동 proxy 는 X 선 log(Lx/Lbol)
≈ −3.24 (Tsikoudi & Kellett 2000) 로, 포화 천장 근처입니다. (앞서의
−3.9 log R'HK 수치는 출처 없는 placeholder 였습니다.)

## Visual styling

AU Mic 의 시각적 표현은 NearStars 카탈로그에서 가장 독특하며 네
요소를 결합합니다.

- **항성 디스크** — `#e0743a` 로 색조 입힌 깊은 붉은빛의 M1V 로,
  AU Mic b (0.07 AU) 에서 본 각지름 1.5° 를 채우며 c (0.119 AU)
  에서는 0.8° 입니다. 지구에서 본 일몰의 태양과 비슷한 색이지만
  스펙트럼은 훨씬 더 붉으며, 렌더링은 광도 hex 색조와 SED 조명
  색온도 (3665 K) 를 모두 사용해 가까운 천체의 장면 조명을
  구동합니다.
- **흑점과 faculae** — 활동 피크 동안 가시 디스크의 > 10% 를
  덮는 다-흑점 복합체. 흑점 사이를 잇는 faculae 와 함께 어두운
  패치로 렌더링됩니다. 흑점 위치는 4.86 d 주기에서 자전하며,
  자전 광도곡선 진폭은 정적 상태에서도 V 밴드 ~3% 입니다.
- **Flare** — 일시적 밝아짐 이벤트로 렌더링되며 `visual_flare_color_hex
  = #ff9050` (백색광 flare 연속체, ~9000 K 흑체 온도가 가시광
  으로 이동) 입니다. 10³¹ erg 위 5.6/일 flare 율은 플레이어가
  게임 내 하루에 여러 차례 flare 를 본다는 뜻이며, 10³⁴ erg
  super-flare 는 연간 여러 번 발생해 10–60 분간 1–3 등급의
  극적인 밝아짐을 만듭니다. Cully 1993 EUVE 이벤트가 특징적으로
  보였던 QPO 변조는 flare 감쇠 꼬리의 느린 맥동으로 렌더링됩니다.
- **가장자리 정면 잔해 원반** — 시스템에서 단연 가장 그림이 되는
  요소입니다. 원반은 ~35 AU 안쪽 가장자리 (0.1 AU 의 가상 행성
  에서 본 AU Mic 중심과의 각거리 ~3.6°) 부터 ~210 AU 바깥쪽
  후광까지 뻗습니다. edge-on (i = 89.5°) 으로 보면 AU Mic
  양쪽 하늘을 이등분하는 가늘고 밝은 줄로 보이며, 표면 밝기는
  배경으로 부드럽게 사라집니다. cfg 원반 색조 `#9a8a78` 는
  따뜻한 무채색 회색입니다 — 게임 내 렌더 분해능에서 산란광은
  무채색이고, 먼지 온도 ~50 K 는 광학 대역에서 원반 자체의
  열복사가 보이기에는 너무 차갑습니다. SPHERE 편광 영상
  (Boccaletti 2018) 은 산란에서 약간 붉은 색을 보이는데, hex
  선택에서 따뜻한 편향으로 보존되되 과도하게 채도를 올리지는
  않았습니다.
- **원반의 움직이는 substructure (애니메이션)** — cfg 의 가장
  야심찬 시각 피처입니다. Multi-epoch SPHERE 영상 (Boccaletti
  2015, 2018) 은 남동쪽 ansa 를 따라 식별 가능한 다섯 개의 밀도
  피처를 추적했고, 이들이 바깥 방향으로 4–10 km/s 로 — 케플러
  자전으로는 너무 빠른 속도로 — 움직였습니다. 항성풍 / 복사압
  가속에 기인한다고 봅니다 (Chiang & Fung 2017). cfg 는 정적
  텍스처가 아니라 애니메이션 렌더링을 선택합니다 — 움직이는
  피처가 문헌에서 AU Mic 을 구별짓는 특성이며, 정적 원반은 이를
  잃습니다. 한 피처가 가시 원반 (35 부터 210 AU) 을 가로지르는
  시간이 게임 내 환산 수개월 정도가 되도록 애니메이션 주기를
  스케일했습니다. Tie-break. 관측은 애니메이션이나 정적 렌더
  둘 다 허용하지만 cfg 는 애니메이션을 택합니다.

가까이 있는 네 행성 — AU Mic b 가 0.07 AU, c 가 0.119 AU, d 가
~0.105 AU (TTV 유도), e 가 ~0.19 AU (Donati 2025 RV 후보) — 모두
원반 안쪽 가장자리 안쪽에서 통과합니다. AU Mic 시스템의 먼 지점
같은 가상의 관측 지점에서 본다면, 전경에서는 행성이 밝은 항성
디스크를 가로지르고 배경에서는 밝은 원반이 양옆으로 1–6° 펼쳐지는
— 카탈로그의 어떤 시스템과도 비교할 수 없는 시각적 장면이
펼쳐집니다. b/c/d/e 의 행성별 합성은 별도의 follow-up 워크스페이스
로 미룹니다.

AU Mic 의 넓은 동반자 AT Mic 은 ~46 400 AU (천구상 1.22°) 떨어진
M-왜성 이중성으로, AU Mic 하늘에서는 적당한 밝기의 붉은 점광원으로
보이며 AU Mic 의 어떤 행성에서 봐도 맨눈 거리에서 이중성으로
분해되지 않습니다. 현재 NS DB 에 별도 엔트리가 없습니다. Open
items 참조.

## Bibliography

### Read (visual-informative, drove decisions above)

- **Gallenne A. et al. 2022** — *The radius and effective temperature
  of the pre-main-sequence M dwarf AU Mic via VLTI/PIONIER*, A&A 665,
  A41 (`2022A&A...665A..41G`, arXiv:2207.04116). 유일한 *refereed*
  간섭계 반지름. θ_LD = 0.825 ± 0.033 ± 0.038 mas → R = 0.862 ± 0.052
  R☉. Phase 2 recommended 반지름.
- **Cristofari P. I. et al. 2023** — *Atmospheric parameters and
  magnetic fields of M dwarfs from SPIRou*, MNRAS 522, 1342
  (`2023MNRAS.522.1342C`, arXiv:2303.11241). 자기장 포함 SPIRou 대기
  fit. Teff = 3665 ± 31 K, [M/H] = +0.12 ± 0.10, log g = 4.52.
  Phase 2 recommended Teff + 금속도.
- **Tsikoudi V. & Kellett B. J. 2000** — *ROSAT all-sky survey X-ray
  emission from late-type stars*, MNRAS 319, 1147 (`2000MNRAS.319.1147T`).
  AU Mic 정적 Lx = 2.24 × 10²⁹ erg/s (log Lx 29.35, log Lx/Lbol ≈
  −3.24). Phase 2 recommended X 선 활동 proxy. (앞서의 Stelzer 2013
  인용을 대체. 온라인에서 인용되는 NEXXUS 2.51e29 값은 AU Mic 에
  대해 틀림 — NEXXUS 는 G/K 표본임.)
- **Plavchan P. et al. 2020** — *A planet within the debris disk
  around the pre-main-sequence star AU Microscopii*, Nature 582,
  497 (`2020Natur.582..497P`, arXiv:2006.13248). TESS 가 발견한
  AU Mic b 의 통과 hot Neptune. 4.86 d 자전 주기. PMS-isochrone
  질량 0.50 ± 0.03 M☉ (Phase 2 recommended 질량). 다-흑점 복잡도.
- **Krist J. E. et al. 2005** — *Hubble Space Telescope Advanced
  Camera for Surveys Coronagraphic Imaging of the AU Microscopii
  Debris Disk*, AJ 129, 1008 (`2005AJ....129.1008K`). HST 분해
  coronagraphic 영상의 첫 사례. 안쪽 가장자리 ~17–43 AU, 바깥 확장
  > 200 AU. 이후 모든 영상이 다듬어 간 기하학적 골격을 제공.
- **Schneider G. et al. 2014** — *Probing for Exoplanets Hiding in
  Dusty Debris Disks: Disk Imaging, Characterization, and
  Exploration with HST/STIS Multi-Roll Coronagraphy*, AJ 148, 59
  (`2014AJ....148...59S`, arXiv:1406.7303). HST/STIS 깊은 재방문.
  표면 밝기 프로파일 정밀화. 바깥 후광을 ~210 AU 까지 추적. 안쪽
  가장자리 ~35 AU 확인.
- **Boccaletti A. et al. 2015** — *Fast-moving features in the
  debris disk around AU Microscopii*, Nature 526, 230
  (`2015Natur.526..230B`, arXiv:1510.06434). VLT/SPHERE 편광 영상
  에서 남동쪽 ansa 의 빠르게 움직이는 다섯 피처 최초 검출. 바깥
  방향 4–10 km/s.
- **Boccaletti A. et al. 2018** — *Two years of monitoring the AU
  Microscopii debris disk with SPHERE: New properties for the
  fast-moving features*, A&A 614, A52 (`2018A&A...614A..52B`,
  arXiv:1804.04574). Multi-epoch 추적으로 피처 운동 확인. 속도
  정밀도 확보. 운동이 케플러가 아니라 항성풍 발사라는 cfg 관련
  제약 확정.
- **Chiang E. & Fung J. 2017** — *Stellar-wind-driven Dust Ridges
  in the AU Mic Debris Disk*, ApJ 848, 4
  (`2017ApJ...848....4C`, arXiv:1707.08970). 움직이는 substructure
  의 물리 모델. 항성풍 / 복사압이 작은 입자를 가속하며, ~35 AU
  에 planetesimal 벨트 birth ring 이 자리잡음. cfg `disk_morphology`
  와 애니메이션 선택을 구동.
- **Strubbe L. E. & Chiang E. 2006** — *Dust Dynamics, Surface
  Brightness Profiles, and Thermal Spectra of Debris Disks: The
  Case of AU Microscopii*, ApJ 648, 652 (`2006ApJ...648..652S`,
  arXiv:astro-ph/0606435). planetesimal 벨트를 ~35 AU 에 놓는
  birth-ring 모델. SED fit 이 먼지 온도를 ~50 K 로 제약.
- **Chen C. H. et al. 2005** — *Spitzer IRS Spectroscopy of
  IRAS-Discovered Debris Disks*, ApJ 634, 1372
  (`2005ApJ...634.1372C`). Spitzer 차가운 성분 SED-fit 이 먼지
  온도를 정박.
- **Mamajek E. E. & Bell C. P. M. 2014** — *On the age of the
  beta Pictoris moving group*, MNRAS 445, 2169
  (`2014MNRAS.445.2169M`, arXiv:1409.2737). β Pic MG (와 따라서
  AU Mic) 의 isochrone 나이 22 ± 3 Myr. LDB 로 확인.
- **Donati J.-F. et al. 2023** — *The magnetic field topology and
  filling of the very active M dwarf AU Mic*, MNRAS 525, 455
  (`2023MNRAS.525..455D`, arXiv:2304.09642). SPIRou ZDI. 소규모 평균
  자기장 ⟨B⟩ = 2.61 ± 0.05 kG, 대규모 자기장 550 ± 30 G (Phase 2
  recommended 자기 값). log L/L☉ = −0.99 ± 0.01 → L 0.102 (Phase 2
  recommended 광도). V−I Teff 3700 ± 70 과 Dartmouth 질량 0.60
  (divergence 대안).
- **Wittrock J. M. et al. 2023** — *Transit Timing Variation
  Measurements and Dynamical Mass Determination of the AU Mic
  System*, AJ 166, 232 (`2023AJ....166..232W`, arXiv:2310.10719).
  host 별 N-body + TTV 동역학 질량 0.51 ± 0.028 M☉. 행성 d 를
  TTV 전용 후보로 도입.
- **Tristan I. I. et al. 2023** — *Catching the Flares of the AU Mic
  System with TESS*, ApJ 951, 33 (`2023ApJ...951...33T`,
  arXiv:2306.00077). TESS Sectors 1+27 flare 센서스. 10³¹ erg 위
  비율 5.6 이벤트/일. 누적 flare 빈도 분포.
- **Davenport J. R. A. et al. 2020** — *The Evryscope Fast
  Transient Engine: real-time detection for rapidly evolving
  transients*, ApJ 905, 107 (`2020ApJ...905..107D`,
  arXiv:2010.02392). TESS 첫해 M-왜성 flare 서베이 맥락. AU Mic
  은 M1V flare 활동의 고에너지 꼬리에 위치.
- **Cully S. L. et al. 1993** — *The EUVE observation of the 1992
  September X-ray flare on AU Mic*, ApJ 414, L49
  (`1993ApJ...414L..49C`). 최초의 mega-flare 검출. EUV 에서
  ~10³⁴–10³⁵ erg.
- **Stelzer B. et al. 2013** — *The UV and X-ray activity of the M
  dwarfs within 10 pc of the Sun*, MNRAS 431, 2063
  (`2013MNRAS.431.2063S`, arXiv:1302.1061). AU Mic 정적 X 선. 맥락
  정보뿐 — frozen Phase 2 bib 에는 없음 (cfg X 선 proxy 는 Tsikoudi
  & Kellett 2000, log Lx 29.35).

### Read (context / methodology, not decision-driving)

- **Martioli E. et al. 2021** — *AU Mic c: a second planet
  transiting the young M dwarf AU Mic* (`2021A&A...649A.177M`,
  arXiv:2102.05288). TESS + 지상 후속으로 AU Mic c 확인. 항성
  결정적이지 않지만 행성 명단을 정의.
- **Mallorquin M. et al. 2024** — *AU Mic system characterization
  with ESPRESSO* (`2024A&A...689A.132M`). b/c 의 궤도와 질량
  파라미터 정밀화. 항성 결정적이지 않음.
- **Donati J.-F. et al. 2025** — *AU Mic system characterized with
  ESPRESSO* (`2025A&A...700A.227D`). AU Mic e 후보 추가. 항성
  합성에는 맥락 정보뿐.
- **Shkolnik E. L. et al. 2017** — *HAZMAT II: Ultraviolet
  Variability of Low-Mass Stars in the GALEX Archive*, ApJ 838,
  87 (`2017ApJ...838...87S`, arXiv:1611.02835). β Pic MG 와 어린
  M-왜성 활동 보정. AU Mic 포화 상태에 대한 맥락.
- **Smith B. A. & Terrile R. J. 1981** — *A Circumstellar Disk
  Around AU Microscopii?* (분해 이전, 초기 IR 초과 검출).

### Read (instrument / non-cfg-decisive)

- **Boyajian T. S. et al. 2012** — *Stellar Diameters and
  Temperatures II*, ApJ 757, 112 (`2012ApJ...757..112B`,
  arXiv:1208.2431). CHARA M-왜성 간섭계 보정. Donati 2023 반지름
  의 맥락이지만 AU Mic 직접 측정은 없음.
- **Loyd R. O. P. et al. 2018** — *MUSCLES Treasury Survey V:
  FUV Flares On Active and Inactive M Dwarfs*, ApJ 867, 71
  (`2018ApJ...867...71L`, arXiv:1809.07322). AU Mic 을 포함한
  어린 M-왜성 비교 집합의 FUV flare 통계.
- **Beeck B. et al. 2013** — *3D radiative-hydrodynamic simulations
  of cool main-sequence stars* (Donati 2023 §3 경유 인용).
  Granulation 모델 격자.
- **Kowalski A. F. et al. 2013** — *Time-resolved Properties and
  Global Trends in dM Flares from Simultaneous Photometry and
  Spectra*, ApJS 207, 15 (`2013ApJS..207...15K`, arXiv:1307.2099).
  cfg flare 색에 채택된 백색광 flare 연속체 분해를 정의.

### Not read — no arXiv preprint or low-priority (~40 papers)

학회 초록 (DPS / EPSC / IAU), 초기 IRAS 시기 특성화 (Krist 2005
이전), 가까운 M-왜성에 대한 SETI / 레이저 방출 모니터링,
성간 전구 미션 제안은 항성 합성에 cfg-결정적인 내용을 더하지
않습니다. 행성별 JWST 와 지상 대기 논문 (Allart 2024 He I,
Hirano 2020 Rossiter-McLaughlin) 은 행성 Phase 3 follow-up
워크스페이스로 미룹니다. 전체 필터링된 bib 는
`docs/phase3/_bib/au-mic.yaml` 에 `status: skipped` annotation 으로
보존됩니다.

## Open items for follow-up

- **AT Microscopii DB 엔트리**. AT Mic 은 AU Mic 의 넓은 공통
  고유운동 동반자로 ~46 400 AU (~1.22°) 떨어져 있으며, 그 자체로
  단주기 M-왜성 이중성이자 β Pic MG 멤버입니다. 이 글 작성 시점
  까지 별도의 NS DB 엔트리가 없습니다. follow-up Phase 2 가 AT Mic
  A 와 B 를 ingest 하고 `db/systems/` 에서 시스템을 연결해야 하며,
  AU Mic 과 AT Mic 은 공통 `system_name` 또는 `cpm_group` 필드를
  공유해야 합니다.
- **Phase 2 `disk_measurements` ingest**. `db/systems/au_mic.json`
  에는 `disk_measurements` 블록이 없습니다. 여기서 채택한 기하
  (35–210 AU, 50 K, i = 89.5°, edge-on) 는 Krist 2005, Schneider
  2014, Boccaletti 2015/2018, Chen 2005 에서 직접 가져왔습니다.
  표준 Phase 2 스키마와의 일관성을 위해, 그리고 Kopernicus
  주변원반 cfg 작성기가 canonical 위치에서 읽을 수 있도록
  `disk_measurements` 배열로 DB 에 추가해야 합니다.
- **행성 b/c/d/e Phase 3 follow-up 워크스페이스**. 알려진 네 행성은
  이 항성 합성의 범위 밖입니다. 전용 follow-up 워크스페이스가
  최소한 b (hot Neptune — super-flare 폭격 하의 대기 보전) 와 d
  (~지구질량 TTV 후보, 시각적으로 가장 관련 있는 암석 천체) 의
  Phase 3 합성을 만들어야 합니다. c 는 sub-Neptune. e 는 현재
  논란 상태입니다 (pl_controv_flag = 1).
- **사이클 위상 / 활동 변조**. AU Mic 은 포화된 전주계열 영역에
  있어 관측된 활동 사이클이 없습니다. 미래의 관측 캠페인이
  사이클을 검출하면 (존재한다면 전형적 시간 스케일은 ~1–3 년)
  `activity_cycle_years` 엔트리를 채울 수 있습니다.
- **Birth-ring planetesimal 질량**. Strubbe & Chiang 2006 은 부모
  planetesimal 벨트 질량을 대략 0.01–0.1 M⊕ 로 추정합니다. 미래의
  cfg 필드 `disk_planetesimal_mass_mearth` 가 게임 내 lore 일관성을
  위해 이를 파라미터화할 수 있습니다. 현재는 표준 Decisions
  스키마에 없습니다.
- **원반 substructure 애니메이션 주기 보정**. cfg 는 SPHERE 가
  측정한 4–10 km/s 유출 속도로 substructure 를 애니메이션 하지만,
  정확한 게임 내 시간 매핑은 Kopernicus 주변원반 cfg 작성기를
  실제로 돌릴 때 게임플레이-vs-사실성 trade-off 결정이 필요합니다.
  cfg variant 의 tie-break 로 보존합니다.
- **보수적 cfg variant**. 같은 `disk_inner_radius_au` /
  `disk_outer_radius_au` / `disk_dust_temperature_k` 를 유지하면서
  `visual_companion_event_disk_substructures_animated = false` 로
  바꾼 정적-원반 variant 가 저사양 하드웨어용 fallback 으로
  배포 가능해야 합니다.

## Related

- [methodology](../reference/methodology.md) — Decisions 테이블의 스키마 출처
- [alpha-centauri-a](alpha-centauri-a.md) — canonical 항성 합성 구조 템플릿 (이 파일은 그 8-섹션 레이아웃을 따름)
- [proxima-cen](proxima-cen.md) — 비교 M 왜성 (M5.5Ve, ~4.85 Gyr) — AU Mic 의 어린 전주계열 M1Ve 상태와 대비
